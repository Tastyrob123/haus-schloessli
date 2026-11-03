// Wirtschaft am Schlössli, Potentialanalyse (Entwurf ohne Blender): Aufnahmen der heutigen Seite, wie ein Gast sie sieht.
// iPhone 390 × 844 (dreifache Dichte) oder Rechner 1440 × 900 (doppelte), Chromium. Je Stelle: Bild + Lage der gemeinten Texte/Elemente.
// node stellen.js [id …] → stellen/<id>.png + stellen/stellen.json (Rechtecke in CSS-Pixeln des Bildes)
module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright'); const fs = require('fs');
const OUT = __dirname + '/stellen/';
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const L = JSON.parse(fs.readFileSync(__dirname + '/stellen.json')); const nur = process.argv.slice(2);
const INFO = fs.existsSync(OUT + 'stellen.json') ? JSON.parse(fs.readFileSync(OUT + 'stellen.json')) : {};
(async () => {
  const b = await chromium.launch();
  for (const s of L) {
    if (nur.length && !nur.includes(s.id)) continue;
    const W = s.desk ? 1440 : 390, H = s.desk ? 900 : 844, f = s.desk ? 2 : 3;
    const c = await b.newContext(s.desk ? { viewport: { width: W, height: H }, deviceScaleFactor: f, locale: 'de-CH' }
      : { viewport: { width: W, height: H }, deviceScaleFactor: f, isMobile: true, hasTouch: true, userAgent: UA, locale: 'de-CH' });
    const p = await c.newPage(); await c.route(/^mailto:|^tel:/, r => r.abort());
    try { await p.goto('https://www.schloessli-bottighofen.ch' + s.pfad, { waitUntil: 'load', timeout: 90000 }); } catch (e) { console.log(s.id, e.message.split('\n')[0]); }
    await p.waitForTimeout(s.warte || 5000);
    if (s.cookie !== 'lassen') { await p.evaluate(() => { const x = [...document.querySelectorAll('button')].find(e => e.textContent.trim() === 'ablehnen'); if (x) x.click(); }); await p.waitForTimeout(700); }
    if (!s.oben) await p.evaluate(async () => { const h = document.body.scrollHeight; for (let y = 0; y < h; y += 400) { scrollTo(0, y); await new Promise(r => setTimeout(r, 140)); } scrollTo(0, 0); });
    await p.waitForTimeout(600);
    if (s.klick) { await p.evaluate(t => { const x = [...document.querySelectorAll('button,a')].find(e => e.textContent.trim() === t); x.click(); }, s.klick); await p.waitForTimeout(2500); }
    if (s.innen) await p.evaluate(t => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (n.data.trim() === t) { let e = n.parentElement; while (e && !(e.scrollHeight > e.clientHeight + 5 && /auto|scroll/.test(getComputedStyle(e).overflowY))) e = e.parentElement; const r = n.parentElement.getBoundingClientRect(); if (e) e.scrollTop += r.top - innerHeight * 0.3; else n.parentElement.scrollIntoView({ block: 'center' }); return; } }, s.innen);
    if (s.zentriere) await p.evaluate(([t, h]) => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (n.data.includes(t)) { const r = n.parentElement.getBoundingClientRect(); scrollTo(0, r.top + scrollY - innerHeight * h); return; } }, [s.zentriere, s.hoch ?? 0.35]);
    if (s.unten) await p.evaluate(() => scrollTo(0, document.body.scrollHeight));
    await p.waitForTimeout(1500);
    const marks = await p.evaluate((ms) => ms.map(m => {
      if (m.sel) { const e = [...document.querySelectorAll(m.sel)].filter(e => e.getBoundingClientRect().width > 0)[m.i || 0]; if (!e) return { fehlt: m.sel }; const r = e.getBoundingClientRect(); return { t: m.sel, x: r.left, y: r.top + (m.voll ? scrollY : 0), w: r.width, h: r.height }; }
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, hits = [];
      while ((n = w.nextNode())) { const i = n.data.indexOf(m.t); if (i < 0) continue; const g = document.createRange(); g.setStart(n, i); g.setEnd(n, i + m.t.length); const q = g.getBoundingClientRect(); if (q.width > 1 && q.height > 1) hits.push({ t: m.t, x: q.left, y: q.top + (m.voll ? scrollY : 0), w: q.width, h: q.height }); }
      return hits[m.i || 0] || { fehlt: m.t };
    }), (s.marks || []).map(m => ({ ...m, voll: !!s.clip })));
    const opt = { path: OUT + s.id + '.png' };
    if (s.clip) { opt.fullPage = true; opt.clip = { x: 0, y: s.clip[0], width: W, height: s.clip[1] - s.clip[0] }; }
    await p.screenshot(opt);
    INFO[s.id] = { url: p.url(), pfad: s.pfad, desk: !!s.desk, W, H: s.clip ? s.clip[1] - s.clip[0] : H, f, y0: s.clip ? s.clip[0] : 0, marks, zeit: new Date().toISOString(),
      scrollH: await p.evaluate(() => document.documentElement.scrollHeight) };
    console.log(s.id, JSON.stringify(marks.map(m => m.fehlt ? 'FEHLT ' + m.fehlt : [m.t.slice(0, 20), Math.round(m.x), Math.round(m.y), Math.round(m.w), Math.round(m.h)])));
    fs.writeFileSync(OUT + 'stellen.json', JSON.stringify(INFO, null, 1)); await c.close();
  }
  await b.close();
})();
