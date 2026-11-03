// Bildschirm der Stube (La Maison) für die Reihe der Werkzeuge im Angebot, Fassung A (Werkbank-Chat 18.10.2026). Server 8917 muss laufen.
const pw = require(process.env.HOME + '/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
(async () => { const br = await pw.chromium.launch(); const c = await br.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  await c.route(/^(mailto|tel):/, r => r.abort());
  const p = await c.newPage(); await p.goto('http://localhost:8917/_werkzeuge/maison/?cb=' + Date.now(), { waitUntil: 'networkidle' }); await p.waitForTimeout(2500);
  await p.screenshot({ path: __dirname + '/ansichten/Angebot/maison.jpg', type: 'jpeg', quality: 88 }); await br.close(); })();
// Das Markenbuch des Hausbuchs als PDF (wie «Als PDF sichern»), daraus zwei Seiten für das aufgeschlagene Buch
(async () => { const br = await pw.chromium.launch(); const p = await br.newPage();
  await p.goto('http://localhost:8917/_werkzeuge/livre/buch.html?cb=' + Date.now(), { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  await p.emulateMedia({ media: 'print' }); await p.pdf({ path: __dirname + '/ansichten/Angebot/markenbuch.pdf', preferCSSPageSize: true, printBackground: true }); await br.close(); })();
