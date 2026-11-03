// «Rund um den Aufenthalt»: die kleinen Seiten und Abschnitte des Entwurfs als Bild, 16:10.   node _werkbank/sammlung.js [name …]
//   → _werkbank/ansichten/Sammlung/<name>.jpg   (gelesen von rundum.py)
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ZIEL = path.join(__dirname, 'ansichten', 'Sammlung'), B = 'http://127.0.0.1:' + (process.env.WB_PORT || 8917) + '/';
const LISTE = [   // Name, Seite, Abschnitt (id) oder '', Versatz nach oben in px
  ['anreise', 'anreise.html', '', 0],
  ['mappe', 'mappe.html', '', 0],
  ['weg', 'haus.html', 'anreise', 40],
  ['spa', 'haus.html', 'spa', 40],
  ['jahr', 'essen.html', 'jahr', 40],
  ['stellen', 'haus.html', 'stellen', 40],
  ['gutschein', 'zimmer.html', 'gutschein', 40],
];
const nur = process.argv.slice(2);
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  const b = await chromium.launch({ headless: true });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5, locale: 'de-CH' });
  for (const [n, seite, id, ab] of LISTE) {
    if (nur.length && !nur.includes(n)) continue;
    const p = await ctx.newPage();
    await p.goto(B + seite, { waitUntil: 'load' }); await p.evaluate(() => document.fonts && document.fonts.ready);
    await p.waitForTimeout(3600);
    if (id) {
      // einmal langsam hinunter, damit alles geladen und eingeblendet ist, dann an den Abschnitt
      await p.evaluate(async (i) => { const z = document.getElementById(i).getBoundingClientRect().top + scrollY; for (let y = 0; y < z; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); } }, id);
      await p.evaluate(([i, a]) => scrollTo(0, document.getElementById(i).getBoundingClientRect().top + scrollY - a), [id, ab]);
      await p.waitForTimeout(3200);
    }
    await p.evaluate(() => { const g = document.querySelector('.gast-knopf,#gast-knopf,.gast__knopf'); if (g) g.style.visibility = 'hidden'; });
    await p.screenshot({ path: path.join(ZIEL, n + '.jpg'), quality: 88 });
    await p.close(); console.log('Sammlung', n);
  }
  await b.close();
})();
