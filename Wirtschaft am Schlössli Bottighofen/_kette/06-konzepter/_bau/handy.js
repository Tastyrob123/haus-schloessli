const path = require('path'), os = require('os');
module.paths.push(path.join(os.homedir(), 'Aussen-Pruefung', 'node_modules'));
const pw = require('playwright');
const URL = 'http://127.0.0.1:8978/haus/Wirtschaft%20am%20Schl%C3%B6ssli%20Bottighofen/_kette/06-konzepter/konzept.html';
(async () => {
  const motor = process.argv[2] || 'webkit';
  const b = await pw[motor].launch({ headless: true });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 })).newPage();
  await p.goto(URL, { waitUntil: 'load' });
  const ziele = ['#auftakt', '#laestermeile .buehne-hulle', '#karte .buehne-hulle', '#feiern .buehne-hulle'];
  for (let i = 0; i < ziele.length; i++) {
    await p.locator(ziele[i]).first().scrollIntoViewIfNeeded(); await p.waitForTimeout(1800);
    await p.screenshot({ path: path.join(__dirname, '..', '_qa', `handy-${motor}-${i}.jpg`), type: 'jpeg', quality: 70 });
  }
  const top = await p.evaluate(() => { scrollTo(0, 0); return 0; }); await p.waitForTimeout(800);
  await p.screenshot({ path: path.join(__dirname, '..', '_qa', `handy-${motor}-kopf.jpg`), type: 'jpeg', quality: 70 });
  await b.close();
})();
