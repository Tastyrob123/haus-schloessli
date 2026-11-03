// Prüfung der eigenen Seite (unsichtbar): Konsole, Bilder geladen, seitlicher Überlauf, Aufnahmen in Bildschirmhöhen.
module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const pw = require('playwright');
const URL = 'http://127.0.0.1:8978/haus/Wirtschaft%20am%20Schl%C3%B6ssli%20Bottighofen/_kette/04-analyst/potential/';
(async () => {
  for (const [name, w, h, motor] of [['rechner', 1440, 900, 'chromium'], ['handy', 390, 844, 'webkit']]) {
    const b = await pw[motor].launch(); const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 }); const p = await c.newPage();
    const fehler = []; p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); }); p.on('pageerror', e => fehler.push(String(e)));
    p.on('response', r => { if (r.status() >= 400) fehler.push(r.status() + ' ' + r.url()); });
    await p.goto(URL, { waitUntil: 'load' });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
    await p.waitForTimeout(800);
    const m = await p.evaluate(() => ({ H: document.documentElement.scrollHeight, ueber: document.documentElement.scrollWidth - innerWidth,
      kaputt: [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src), erster: Math.round(document.querySelector('.punkt').getBoundingClientRect().top + scrollY) }));
    console.log(name, JSON.stringify({ ...m, bildschirme: (m.H / h).toFixed(1), ersterPunkt_bs: (m.erster / h).toFixed(1), fehler }));
    for (let k = 0; k < Math.min(Math.ceil(m.H / h), 40); k += 1) { await p.evaluate(y => scrollTo(0, y), k * h); await p.waitForTimeout(120); await p.screenshot({ path: `${__dirname}/../_qa/${name}-${String(k).padStart(2, '0')}.png` }); }
    await b.close();
  }
})();
