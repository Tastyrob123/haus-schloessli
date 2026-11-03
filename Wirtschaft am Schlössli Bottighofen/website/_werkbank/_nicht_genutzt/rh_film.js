// Handy-Filme der Rezeption im Chat, Landgasthof Ruedihus (Werkbank-Chat 17.10.2026; Kopie von dh_film.js des Waldhotel Doldenhorn, nur gelesen. Dort: Robert: «wenn die Buchstaben die rechte Kante erreichen, dann gibt es
// einen Absatz» und «nicht … dasselbe Videomaterial. Bitte verwende da zwei verschiedene»). Mechanik von _Rezeption im Chat/film2.js (nur gelesen):
// die Uhr der Seite steht und wird je Bild um 1/30 s weitergestellt, so gibt es keine ausgelassenen Bilder und keine Wartezeit im Film.
// Ablauf: Frage tippen (das Feld bricht am rechten Rand um und wächst mit), senden, die Rezeption denkt, Antwort, Buchungsmaske, Blick auf «Zur Buchung».
// Das Buchungssystem wird nicht geöffnet (keine Preise in Werkbank und Film). Die Antwort ist eine echte Antwort der Funktion /api/gast vom 10.10.2026
// (Familie Maeder — Vier Häuser/_gast_landing), sie wird für die Aufnahme geliefert; kein KI-Aufruf.
//   node _werkbank/dh_film.js <dreh.json> <ausgabe.mp4> [port] [probe]
//   dreh.json = [Frage, Antwort]   →  Bilder in einem Wegwerf-Ordner, dann ffmpeg: 540 × 1168, 30 Bilder je Sekunde, dazu <ausgabe>-m.mp4 (360 breit)
const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
const fs = require('fs'), path = require('path'), os = require('os'), { execFileSync } = require('child_process');
const [drehDatei, ausgabe, port = '8917', modus = ''] = process.argv.slice(2);
const PROBE = modus === 'probe';
const [FRAGE, ANTWORT] = JSON.parse(fs.readFileSync(drehDatei, 'utf8'));
const LEISTE = fs.readFileSync('/Users/robertreff/Desktop/Website-Projekte/Carlton-Europe Interlaken/_gast/handy/schirm.js', 'utf8').match(/const LEISTE = `([\s\S]*?)`;/)[1];
const B = 393, H = 850, BPS = 30, DT = 1000 / BPS;
const AUS = fs.mkdtempSync(path.join(os.tmpdir(), 'rh-film-'));
const SEITE = `<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="assets/css/main.css">
<style>html,body{margin:0;height:100%;overflow:hidden;overscroll-behavior:none}
.gast{position:fixed!important;inset:50px 0 0 0!important;width:auto!important;height:auto!important;max-height:none!important;border-radius:0!important;box-shadow:none!important;transform:none!important;opacity:1!important;visibility:visible!important}
.gast-knopf,.gast-dunkel{display:none!important}
#tipp{position:fixed;z-index:9999;left:0;top:0;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;background:rgba(255,255,255,.3);box-shadow:0 0 0 1.5px rgba(255,255,255,.55),0 4px 14px rgba(0,0,0,.35);opacity:0;pointer-events:none}
</style></head><body><div class="leiste-film"></div><div id="tipp"></div><script src="assets/js/gast.js"></script></body></html>`;

(async () => {
  const b = await webkit.launch();
  const c = await b.newContext({ viewport: { width: B, height: H }, deviceScaleFactor: 2, locale: 'de-CH', hasTouch: false });
  const p = await c.newPage();
  await p.route(/^(mailto|tel):/, r => r.abort());
  let antwortFrei; const antwortTor = new Promise(r => { antwortFrei = r; });
  await p.route('**/film-aufnahme.html', r => r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: SEITE }));
  await p.route('**/api/gast', async r => { await antwortTor; r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ANTWORT) }); });
  await p.clock.install();
  await p.goto(`http://localhost:${port}/film-aufnahme.html`, { waitUntil: 'networkidle' });
  await p.waitForSelector('.gast-knopf', { state: 'attached' });
  await p.evaluate(() => document.querySelector('.gast-knopf').click());
  await p.waitForSelector('.gast__feld textarea', { state: 'attached' });
  await p.waitForFunction(() => [...document.querySelectorAll('.gast__k-bild img, .gast img')].every(i => i.complete && i.naturalWidth) && document.fonts.status === 'loaded');
  const grund = await p.evaluate(() => getComputedStyle(document.querySelector('.gast')).backgroundColor);
  await p.evaluate(([l, g]) => {
    document.documentElement.style.background = g; document.body.style.background = g;
    document.querySelector('.leiste-film').outerHTML = l.replace('position:fixed;z-index:999;', 'position:fixed;z-index:999;background:' + g + ';');
    const sanft = function (o) {
      if (!o || o.behavior !== 'smooth') return this.__st.apply(this, arguments);
      if (window.__nurFilm && !o.film) return;
      const el = this, von = el.scrollTop, nach = Math.max(0, Math.min(o.top, el.scrollHeight - el.clientHeight)), t0 = performance.now(), d = 620;
      el.__lauf = (el.__lauf || 0) + 1; const ich = el.__lauf;
      (function schritt() {
        if (el.__lauf !== ich) return;
        const t = Math.min((performance.now() - t0) / d, 1), e = t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        el.scrollTop = von + (nach - von) * e;
        if (t < 1) requestAnimationFrame(schritt);
      })();
    };
    Element.prototype.__st = Element.prototype.scrollTo; Element.prototype.scrollTo = sanft;
    window.__anim = dt => {
      for (const a of document.getAnimations()) {
        if (a.__t === undefined) { a.pause(); a.__t = 0; }
        a.__t += dt;
        const ende = a.effect && a.effect.getComputedTiming().endTime;
        if (isFinite(ende) && a.__t >= ende) { try { a.finish(); } catch (e) {} } else { try { a.currentTime = a.__t; } catch (e) {} }
      }
    };
  }, [LEISTE, grund]);
  // eigene Schreibmarke nach der Film-Uhr (die des Browsers flackert im Film); der Spiegel bricht genau wie das Feld um
  await p.evaluate(() => {
    const ta = document.querySelector('.gast__feld textarea'), cs = getComputedStyle(ta), sp = document.createElement('div');
    ta.parentNode.style.position = 'relative'; ta.parentNode.style.display = 'block';
    sp.style.cssText = 'position:absolute;left:0;top:0;right:0;pointer-events:none;white-space:pre-wrap;overflow-wrap:break-word;font-family:' + cs.fontFamily + ';font-size:' + cs.fontSize + ';font-weight:' + cs.fontWeight +
      ';line-height:' + cs.lineHeight + ';letter-spacing:' + cs.letterSpacing + ';color:' + cs.color + ';padding:' + cs.paddingTop + ' ' + cs.paddingRight + ' ' + cs.paddingBottom + ' ' + cs.paddingLeft;
    ta.parentNode.appendChild(sp); ta.style.color = 'transparent'; ta.style.caretColor = 'transparent';
    window.__spiegel = marke => {
      sp.textContent = ta.value;
      if (!marke) return;
      const m = document.createElement('span');
      m.style.cssText = 'display:inline-block;width:2px;height:1.2em;margin:0 -1px;vertical-align:text-bottom;border-radius:1px;background:#d2bf98';
      sp.appendChild(m);
      m.animate([{ opacity: 1 }, { opacity: 1, offset: .52 }, { opacity: 0, offset: .56 }, { opacity: 0, offset: .96 }, { opacity: 1 }], { duration: 1060, iterations: Infinity });
    };
  });
  await p.evaluate(() => document.activeElement && document.activeElement.blur());
  await p.clock.pauseAt(new Date(Date.now() + 3000));
  await p.clock.runFor(3000);

  let n = 0, rest = 0;
  const schuss = async name => p.screenshot({ path: path.join(AUS, name), type: 'jpeg', quality: 95, caret: 'hide' });
  const bild = async () => {
    rest += DT; const ms = Math.floor(rest); rest -= ms;
    await p.clock.runFor(ms);
    await p.evaluate(dt => window.__anim(dt), DT);
    await schuss(`bild-${String(++n).padStart(5, '0')}.jpg`);
  };
  const bilder = async sek => { for (let i = 0, m = Math.round(sek * BPS); i < m; i++) await bild(); };
  const tipp = async ort => {
    const r = await ort.boundingBox();
    await p.evaluate(([x, y]) => { const t = document.getElementById('tipp'); t.style.left = x + 'px'; t.style.top = y + 'px';
      t.animate([{ opacity: 0, transform: 'scale(1.5)' }, { opacity: 1, transform: 'scale(1)', offset: .35 }, { opacity: 1, transform: 'scale(.86)', offset: .6 }, { opacity: 0, transform: 'scale(1.1)' }], { duration: 620, easing: 'ease-out' }); }, [r.x + r.width / 2, r.y + r.height / 2]);
    await bilder(.36);
  };
  const zeilen = () => p.evaluate(() => { const t = document.querySelector('.gast__feld textarea'); return Math.round(t.getBoundingClientRect().height); });

  // 1 Start
  await bilder(1.1);
  // 2 Frage tippen: das Feld bricht am rechten Rand um und wächst mit
  await tipp(p.locator('.gast__feld textarea'));
  await p.evaluate(() => { document.querySelector('.gast__feld textarea').focus({ preventScroll: true }); window.__spiegel(true); });
  await bilder(.5);
  const hoeheVor = await zeilen();
  for (const z of FRAGE) { await p.keyboard.insertText(z); await p.evaluate(() => window.__spiegel(true)); await bild(); if (' .,?'.includes(z)) await bild(); }
  const hoeheNach = await zeilen();
  await bilder(.5);
  // 3 senden, die Rezeption denkt, die Antwort kommt
  await tipp(p.locator('.gast__send'));
  await p.evaluate(() => { const f = document.querySelector('.gast__feld'); f.requestSubmit ? f.requestSubmit() : f.dispatchEvent(new Event('submit', { cancelable: true })); document.querySelector('.gast__feld textarea').blur(); window.__spiegel(false); });
  await bilder(1.2);
  await p.evaluate(() => { window.__nurFilm = true; });
  antwortFrei();
  // bis die Buchungsmaske steht oder, bei einer Antwort ohne Maske, bis der Text der Antwort 24 Bilder lang still steht
  let still = 0, alt = -1;
  for (let i = 0; i < 400; i++) {
    const s = await p.evaluate(() => { const m = !!document.querySelector('.gast__maske'); const h = [...document.querySelectorAll('.gast__b--haus')].pop(); return { m, n: h && !h.classList.contains('gast__b--denkt') ? h.textContent.length : -1 }; });
    if (s.m) break;
    if (s.n > 0 && s.n === alt) { if (++still >= 24) break; } else still = 0;
    alt = s.n; await bild();
  }
  await bilder(2.8);
  // 4 die Buchungsmaske ganz zeigen, Blick auf «Zur Buchung»
  const zu = (sel, ab = 12) => p.evaluate(([s, ab]) => { const l = document.querySelector('.gast__lauf'), g = document.querySelector(s); if (g) l.scrollTo({ top: l.scrollTop + g.getBoundingClientRect().top - l.getBoundingClientRect().top - ab, behavior: 'smooth', film: true }); }, [sel, ab]);
  if (await p.evaluate(() => !!document.querySelector('.gast__maske'))) { await zu('.gast__maske'); await bilder(1.9); } else { await zu('.gast__b--haus:last-of-type', 30); await bilder(1.6); }
  await p.evaluate(() => { const l = document.querySelector('.gast__lauf'), f = document.querySelector('.gast__m-los'); if (!f) return; const u = f.getBoundingClientRect().bottom - l.getBoundingClientRect().bottom + 60; if (u > 0) l.scrollTo({ top: l.scrollTop + u, behavior: 'smooth', film: true }); });
  await bilder(2.4);
  const info = { bilder: n, sek: +(n / BPS).toFixed(2), feld_vor: hoeheVor, feld_nach: hoeheNach };
  await c.close(); await b.close();
  if (!PROBE) {
    const roh = ausgabe;
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(BPS), '-i', path.join(AUS, 'bild-%05d.jpg'), '-vf', 'scale=540:1168:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20',
      '-pix_fmt', 'yuv420p', '-g', '15', '-an', '-movflags', '+faststart', roh]);
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', roh, '-vf', 'scale=360:-2', '-c:v', 'libx264', '-preset', 'slow', '-crf', '27', '-g', '15', '-an', '-movflags', '+faststart', roh.replace(/\.mp4$/, '-m.mp4')]);
  } else {
    info.probe = AUS;
  }
  if (!PROBE) fs.rmSync(AUS, { recursive: true, force: true });
  console.log(JSON.stringify(info));
})().catch(e => { console.error(e); process.exit(1); });
