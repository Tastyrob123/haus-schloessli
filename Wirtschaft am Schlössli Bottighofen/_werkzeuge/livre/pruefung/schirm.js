/* Das Hausbuch · Schlössli · Bildschirmbilder 1440 × 900 für Die Stube und den Laptop der Werkbank (Safari-Kern).  node _werkzeuge/livre/pruefung/schirm.js _werkzeuge/livre/schirm  (Server :9049) */
const pw = require(process.env.HOME + '/Aussen-Pruefung/node_modules/playwright');
(async () => { const out = process.argv[2]; const b = await pw.webkit.launch();
 for (const [a, n] of [['start', 'uebersicht'], ['bilder', 'bildarchiv'], ['dateien', 'dateien'], ['pruefung', 'pruefung']]) {
  const c = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }); await c.addInitScript(() => localStorage.setItem('rundgang-sl-livre', '1'));
  const p = await c.newPage(); await p.goto('http://localhost:9049/_werkzeuge/livre/#' + a, { waitUntil: 'load' }); await p.waitForTimeout(3000);
  if (a === 'pruefung') { await p.locator('#li-bsp').click(); await p.waitForTimeout(1500); await p.evaluate(() => scrollTo(0, 0)); }
  await p.screenshot({ path: out + '/schirm-' + n + '-1440x900.png' }); await c.close(); }
 await b.close(); })();
