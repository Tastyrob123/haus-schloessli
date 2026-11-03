// «Vier Häuser, eine Startseite.»: die gemeinsame Startseite der Familie Maeder und die Startseiten der vier Häuser als Bild (nur zum Zeigen, keine Links).
// node _werkbank/vision_aufnahme.js  → _werkbank/ansichten/Vision/<name>.jpg   (die fünf Vorschau-Server müssen laufen: 8925, 8916, 8917, 8918, 8912; gelesen wird nur)
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ZIEL = path.join(__dirname, 'ansichten', 'Vision');
const LISTE = [['familie', 'http://127.0.0.1:8925/', 11000], ['doldenhorn', 'http://127.0.0.1:8916/', 6500], ['ruedihus', 'http://127.0.0.1:8917/', 6500], ['gasterntal', 'http://127.0.0.1:8918/', 6500], ['carlton', 'http://127.0.0.1:8912/', 6500]];
const nur = process.argv.slice(2);
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  const b = await chromium.launch({ headless: true });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5, locale: 'de-CH' });
  for (const [n, u, warte] of LISTE) {
    if (nur.length && !nur.includes(n)) continue;
    const p = await ctx.newPage();
    try {
      await p.goto(u, { waitUntil: 'load', timeout: 30000 }); await p.evaluate(() => document.fonts && document.fonts.ready);
      await p.waitForTimeout(warte);
      await p.screenshot({ path: path.join(ZIEL, n + '.jpg'), quality: 88 });
      console.log('Vision', n, await p.title());
    } catch (e) { console.log('fehlt', n, String(e).slice(0, 120)); }
    await p.close();
  }
  await b.close();
})();
