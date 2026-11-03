// Prüft das Board unsichtbar: Konsole, kaputte Bilder, seitliches Überlaufen; ganze Seite als Aufnahme in _qa/.
const path = require('path'), os = require('os');
module.paths.push(path.join(os.homedir(), 'Aussen-Pruefung', 'node_modules'));
const pw = require('playwright');
const URL = 'http://127.0.0.1:8978/haus/Wirtschaft%20am%20Schl%C3%B6ssli%20Bottighofen/_kette/06-konzepter/konzept.html';
(async () => {
  for (const motor of ['chromium', 'webkit']) {
    const browser = await pw[motor].launch({ headless: true });
    for (const w of [1440, 390]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: w > 500 ? 900 : 844 }, deviceScaleFactor: w > 500 ? 1 : 2 });
      const page = await ctx.newPage(); const fehler = [];
      page.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); });
      page.on('pageerror', e => fehler.push(String(e)));
      page.on('requestfailed', r => fehler.push('fehlt: ' + r.url()));
      page.on('response', r => { if (r.status() >= 400) fehler.push(r.status() + ' ' + r.url()); });
      await page.goto(URL, { waitUntil: 'load' }); await page.waitForTimeout(800);
      const H = await page.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < H; y += 500) { await page.evaluate(v => scrollTo(0, v), y); await page.waitForTimeout(90); }
      await page.waitForTimeout(1800);
      const r = await page.evaluate(() => {
        const imgs = [...document.images]; const kaputt = imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src);
        const da = document.querySelectorAll('[data-a]').length, ok = document.querySelectorAll('[data-a].da').length;
        const breit = [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.right > innerWidth + 1 && getComputedStyle(e).position !== 'fixed'; }).slice(0, 5).map(e => e.className || e.tagName);
        return { bilder: imgs.length, kaputt, ueberlauf: document.documentElement.scrollWidth - document.documentElement.clientWidth, da, ok, breit, hoehe: document.documentElement.scrollHeight };
      });
      await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(300);
      const ziel = path.join(__dirname, '..', '_qa', `${motor}-${w}.jpg`);
      await page.screenshot({ path: ziel, fullPage: w > 500, type: 'jpeg', quality: 60 });
      console.log(JSON.stringify({ motor, w, fehler, ...r }));
      await ctx.close();
    }
    await browser.close();
  }
})().catch(e => { console.error(String(e)); process.exit(1); });
