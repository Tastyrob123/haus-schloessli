
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const auftraege = JSON.parse(fs.readFileSync(0, 'utf8'));
  const b = await chromium.launch({ headless: true });
  const fehler = [];
  for (const a of auftraege) {
    // der Satz misst in der Breite der bedruckten Fläche, im Druckmodus
    const p = await b.newPage({ viewport: { width: Math.round(a.breite_mm * 96 / 25.4), height: 1200 } });
    p.on('pageerror', e => fehler.push(a.html + ': ' + e));
    await p.emulateMedia({ media: 'print' });
    await p.goto('file://' + a.html, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const satz = await p.evaluate(() => window.SATZ_FEHLER || []);
    satz.forEach(f => fehler.push(a.html.split('/').pop() + ': ' + f));
    const o = { path: a.pdf, width: a.b + 'mm', height: a.h + 'mm', printBackground: true };
    if (a.kopf) Object.assign(o, { displayHeaderFooter: true, headerTemplate: a.kopf, footerTemplate: a.fuss, margin: a.rand });
    else Object.assign(o, { preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    await p.pdf(o);
    await p.close();
  }
  await b.close();
  process.stdout.write(JSON.stringify({ fehler }));
})();
