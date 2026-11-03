// Abnahme-Tor · gezielte Nachprüfung der Wild-Side-Logo-Stellen auf der Website (Oberchef 31.10.2026: nur das Logo ist neu, kein Volllauf)
// Je Seite (Deutsch und Englisch) und Grösse (1440, 1000, 390): jede Logo-Stelle suchen, ins Bild holen, messen (sichtbar, Seitenverhältnis wie
// das Original 1:1, nicht verdeckt, nicht angeschnitten, im Fenster) und als Bild sichern.
// Aufruf: node logo-nachpruefung.js <basis-url> <ausgabe> [--version 26218]
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const fs = require('fs'), path = require('path');
const [BASIS, AUS] = process.argv.slice(2);
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const VERSION = arg('version', '');
const SEITEN = ['index.html', 'abend.html', 'abende.html', 'bar.html', 'dirty-chicken.html', 'leute.html', 'weg.html', 'impressum.html', 'datenschutz.html'];
const GROESSEN = [[1440, 900], [1000, 650], [390, 844]];
fs.mkdirSync(path.join(AUS, 'bilder'), { recursive: true });
(async () => {
  const b = await pw.webkit.launch(); const erg = [];
  for (const sprache of ['', 'en/']) for (const s of SEITEN) for (const [w, h] of GROESSEN) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2 }); const p = await ctx.newPage();
    const url = BASIS + sprache + s + '?cb=' + Date.now(); const r = await p.goto(url, { waitUntil: 'load', timeout: 45000 }).catch(e => null);
    const status = r ? r.status() : 0; if (status !== 200) { erg.push({ seite: sprache + s, w, status }); await ctx.close(); continue; }
    const html = await p.content(); const version = VERSION ? html.includes('v=' + VERSION) : true;
    await p.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
    const stellen = await p.evaluate(() => [...document.querySelectorAll('svg, img')].filter(e => {
      const u = e.querySelector && e.querySelector('use'); const href = u ? (u.getAttribute('href') || u.getAttribute('xlink:href') || '') : (e.getAttribute('src') || '');
      return /#ws\b|zn-ws|wildside-logo|ws-logo|logo-ws/i.test(href + ' ' + (e.getAttribute('class') || '')) || (e.tagName === 'IMG' && /^walk on the wild side$/i.test(e.alt || ''));
    }).map((e, i) => { e.setAttribute('data-logo-nr', i); const u = e.querySelector && e.querySelector('use'); return { i, cls: String(e.getAttribute('class') || ''), href: u ? u.getAttribute('href') : e.getAttribute('src'), vb: e.getAttribute('viewBox') || '' }; }));
    for (const st of stellen) {
      const loc = p.locator(`[data-logo-nr="${st.i}"]`);
      await loc.scrollIntoViewIfNeeded({ timeout: 4000 }).catch(() => { }); await p.waitForTimeout(900);
      const m = await loc.evaluate(e => { const r = e.getBoundingClientRect(); const cx = r.x + r.width / 2, cy = r.y + r.height / 2;
        const oben = document.elementFromPoint(Math.min(innerWidth - 1, Math.max(0, cx)), Math.min(innerHeight - 1, Math.max(0, cy)));
        const c = getComputedStyle(e); const sicht = r.width > 4 && r.height > 4 && c.visibility !== 'hidden' && c.display !== 'none' && +c.opacity > .05;
        let anc = e.parentElement, schnitt = null; while (anc) { const ca = getComputedStyle(anc); if (/(hidden|clip)/.test(ca.overflow + ca.overflowX + ca.overflowY)) { const ra = anc.getBoundingClientRect(); if (r.left < ra.left - .5 || r.right > ra.right + .5 || r.top < ra.top - .5 || r.bottom > ra.bottom + .5) { schnitt = (anc.className || anc.tagName).toString().slice(0, 40); break; } } anc = anc.parentElement; }
        return { x: r.x, y: r.y, w: r.width, h: r.height, verh: r.width / r.height, sicht, oben: oben ? (oben === e || e.contains(oben) || oben.closest('svg') === e) : false, obenWas: oben ? (oben.tagName + '.' + String(oben.className && oben.className.baseVal !== undefined ? oben.className.baseVal : oben.className).slice(0, 30)) : '', imFenster: r.left >= -1 && r.right <= innerWidth + 1, schnitt, nat: e.tagName === 'IMG' ? [e.naturalWidth, e.naturalHeight] : null };
      }).catch(e => ({ fehler: String(e).slice(0, 80) }));
      const vb = (st.vb || '').split(/\s+/).map(Number); const soll = vb.length === 4 && vb[3] ? vb[2] / vb[3] : (m.nat && m.nat[1] ? m.nat[0] / m.nat[1] : null);
      const funde = [];
      if (!m.sicht) funde.push('nicht sichtbar');
      if (soll && m.verh && Math.abs(m.verh / soll - 1) > .03) funde.push(`Seitenverhältnis ${m.verh.toFixed(3)} statt ${soll.toFixed(3)} (verzerrt)`);
      if (m.sicht && !m.oben) funde.push('verdeckt von ' + m.obenWas);
      if (!m.imFenster) funde.push('ragt aus dem Fenster');
      if (m.schnitt) funde.push('angeschnitten von ' + m.schnitt);
      const bild = `${(sprache || 'de/').replace('/', '')}-${s.replace('.html', '')}-${w}-${st.i}.png`;
      if (m.w) await p.screenshot({ path: path.join(AUS, 'bilder', bild), clip: { x: Math.max(0, m.x - 60), y: Math.max(0, m.y - 60), width: Math.min(w - Math.max(0, m.x - 60), m.w + 120), height: Math.min(h - Math.max(0, m.y - 60), m.h + 120) } }).catch(() => { });
      erg.push({ seite: sprache + s, w, version, stelle: st.cls || st.href, href: st.href, mass: m.w ? `${m.w.toFixed(0)}×${m.h.toFixed(0)}` : '', funde, bild });
      console.log(sprache + s, w, st.cls || st.href, m.w ? `${m.w.toFixed(0)}×${m.h.toFixed(0)}` : '-', funde.length ? 'FUND ' + funde.join('; ') : 'ok');
    }
    if (!stellen.length) erg.push({ seite: sprache + s, w, version, stelle: '(keine Logo-Stelle)', funde: [] });
    await ctx.close();
  }
  fs.writeFileSync(path.join(AUS, 'logo.json'), JSON.stringify(erg, null, 1));
  const n = erg.filter(e => e.funde && e.funde.length).length, alt = erg.filter(e => e.version === false).length;
  console.log(`FERTIG ${erg.length} Stellen, ${n} mit Fund, ${alt} Seiten ohne Version ${VERSION}`); await b.close();
})();
