// Druckt die Karte «Ein Vorschlag.» als PDF: node karte_druck.js <karte.html> [<karte.html> …]  → neben jeder Seite vorschlag-landgasthof-ruedihus.pdf
// A4 ohne Rand, Hintergrund und Goldränder gedruckt, Schriften aus werkbank.css (lokal), Seitengrösse aus @page (preferCSSPageSize).
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const seiten = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 1400 }, deviceScaleFactor: 2 });
  let n = 0;
  for (const s of seiten) {
    const ziel = path.join(path.dirname(s), 'vorschlag-landgasthof-ruedihus.pdf');
    await p.goto('file://' + path.resolve(s), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.emulateMedia({ media: 'print' });
    // eine einzige Seite in A4-Breite, so hoch wie die Karte (die Goldränder brechen sonst an der Seitengrenze)
    await p.setViewportSize({ width: 794, height: 1123 });
    const h = await p.evaluate(() => Math.ceil(document.documentElement.scrollHeight));
    await p.pdf({ path: ziel, width: '794px', height: h + 'px', printBackground: true, preferCSSPageSize: false, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    n++;
  }
  await b.close();
  console.log('Karte als PDF: ' + n + ' Dateien');
})().catch(e => { console.error(e); process.exit(1); });
