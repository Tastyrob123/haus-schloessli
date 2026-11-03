// Das Kartenpult · misst die Teile der Weinkarte im echten Satz (satz_bau.py wein_messen): node satz_messen.js <datei.html>
// Letzte Zeile: { h: [Höhe je Teil in px], frei: [freie Höhe erste Seite, folgende Seiten] }
const path = require('path');
const WEGE = ['/Users/robertreff/Aussen-Pruefung/node_modules/playwright', path.join(process.env.HOME || '', 'Aussen-Pruefung/node_modules/playwright'), 'playwright'];
let pw = null; for (const w of WEGE) { try { pw = require(w); break; } catch (e) { /* nächster Weg */ } }
if (!pw) { console.error('Playwright fehlt'); process.exit(2); }
(async () => {
  const b = await pw.chromium.launch();
  try {
    const p = await b.newPage({ viewport: { width: 1300, height: 1400 } });
    await p.emulateMedia({ media: 'print' });
    await p.goto('file://' + process.argv[2]);
    await p.evaluate(() => document.fonts.ready);
    const r = await p.evaluate(() => {
      const h = [...document.querySelectorAll('.mi')].map(x => x.getBoundingClientRect().height);
      const frei = [...document.querySelectorAll('.fr')].map(x => x.getBoundingClientRect().height);
      return { h, frei };
    });
    process.stdout.write(JSON.stringify(r));
  } finally { await b.close(); }
})().catch(e => { console.error(String(e && e.stack || e)); process.exit(1); });
