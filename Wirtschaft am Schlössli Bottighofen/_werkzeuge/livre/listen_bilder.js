/* Das Bildarchiv · Wirtschaft am Schlössli · Bilder für die Listen «Farben» und «Schriften» (Robert 20.10.2026: «in allen Tools Bilder dazu»).
   Nimmt je Schrift und je Ton, der nur auf der Website belegt ist, einen Ausschnitt der Website des Hauses, so wie er dort steht (nur lesen, unsichtbar,
   ein Browser). Aufruf aus bau.py: node listen_bilder.js <zielordner> <seite.html> …  → listen/<name>.png (danach in bau.py zu WebP) */
const path = require('path');
const { chromium } = require(path.join(process.env.HOME, 'Aussen-Pruefung/node_modules/playwright'));
const [, , ZIEL, ...SEITEN] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
  // je Wunsch: erstes sichtbares Element mit dieser Schrift (und, falls genannt, auf hellem Grund), 10 bis 90 Zeichen
  const WUNSCH = [
    ['schrift-t', "Open Sans", 'titel'], ['schrift-s', 'Instrument Sans', 'lauf'], ['schrift-m', 'DM Mono', 'klein'], ['schrift-h', 'Hand', 'hand'],
    ['farbe-tinte', 'Instrument Sans', 'lauf-hell'], ['farbe-papier', null, 'papier']];
  for (const [name, schrift, art] of WUNSCH) {
    let box = null;
    for (const SEITE of SEITEN) {
    await p.goto('file://' + SEITE, { waitUntil: 'load' });
    await p.evaluate(async () => { document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; }); await document.fonts.ready; });
    await p.waitForTimeout(600);
    box = await p.evaluate(([schrift, art]) => {
      const hell = el => { let e = el; while (e && e !== document.body) { const c = getComputedStyle(e).backgroundColor; const m = c.match(/\d+/g); if (m && +m[3] !== 0 && c !== 'rgba(0, 0, 0, 0)') { return (+m[0] + +m[1] + +m[2]) / 3 > 180; } e = e.parentElement; } return true; };
      let el;
      if (art === 'papier') el = document.querySelector('section.f-hell');
      else el = [...document.querySelectorAll('h1,h2,h3,p,span,small,a,b,li,div')].find(e => {
        const s = getComputedStyle(e), t = (e.textContent || '').trim(), r = e.getBoundingClientRect();
        if (!s.fontFamily.includes(schrift) || e.children.length > 3 || t.length < (art === 'hand' ? 3 : 10) || t.length > 90 || r.width < 40 || s.visibility === 'hidden' || +s.opacity === 0) return false;
        if (art === 'titel') return /^(H1|H2)$/.test(e.tagName);
        if (art === 'titel-hell') return /^(H2)$/.test(e.tagName) && hell(e) && !/^Willkommen/.test(t);
        if (art === 'lauf' || art === 'lauf-hell') return e.tagName === 'P' && t.length >= 30 && r.width < 760 && (art === 'lauf' || hell(e)) && !e.closest('nav,header');
        if (art === 'klein') return s.textTransform === 'uppercase' && r.height < 40 && r.width > 150 && r.width / r.height > 4 && !e.closest('svg,[style*=rotate]');
        return true;
      });
      if (!el) return null;
      el.scrollIntoView({ block: 'center' });
      const r = el.getBoundingClientRect();
      return art === 'papier' ? { x: 0, y: Math.max(0, r.top), width: Math.min(innerWidth, 1440), height: Math.min(r.height, 520) }
        : { x: Math.max(0, r.left - 28), y: Math.max(0, r.top - 22), width: Math.min(r.width + 56, innerWidth - Math.max(0, r.left - 28)), height: r.height + 44 };
    }, [schrift, art]);
    if (box) break;
    }
    if (!box) { console.log('nicht gefunden', name); continue; }
    await p.waitForTimeout(400);
    await p.screenshot({ path: path.join(ZIEL, name + '.png'), clip: box });
    console.log('ok', name);
  }
  await b.close();
})();
