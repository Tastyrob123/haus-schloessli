/* Bilder für die Anleitung (anleitung.html): ein Bildschirmfoto je Kapitel aus dem echten Werkzeug, Beispielwerte, 1512×900, gleich als JPEG 1200 px breit.
   node anleitung_bilder.js [basis] [browser]   (Server der Besucherliste muss laufen, eigener Port 9286; browser chromium oder webkit) */
const path = require('path'), fs = require('fs');
const PW = (() => {
  for (const p of [process.env.PLAYWRIGHT_PFAD, '/Users/robertreff/Aussen-Pruefung/node_modules/playwright', path.join(process.env.HOME || '', 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'), 'playwright']) {
    if (!p) continue; try { return require(p); } catch (e) { /* nächster Weg */ }
  }
  throw new Error('playwright nicht gefunden');
})();
const A = process.argv[2] || 'http://127.0.0.1:9286/_werkzeuge/registre/';
const BROWSER = process.argv[3] || 'chromium';
const AUS = path.join(__dirname, 'anleitung');
const K = [
  ['k01', 'start', 0, null], ['k02', 'start', 520, null], ['k03', 'besuche', 540, null], ['k04', 'besuche', 540, async p => { await p.click('[data-filter="buchung"]'); await p.waitForTimeout(500); }],
  ['k05', 'herkunft', 400, null], ['k06', 'zeit', 470, null], ['k07', 'seiten', 470, null], ['k08', 'verlauf', 470, null], ['k09', 'buchung', 470, null],
  ['k10', 'zaehlung', 0, null]];
(async () => {
  const b = await PW[BROWSER].launch(); fs.mkdirSync(AUS, { recursive: true });
  for (const [id, v, y, vor] of K) {
    const c = await b.newContext({ viewport: { width: 1512, height: 900 }, deviceScaleFactor: 1200 / 1512 }); await c.addInitScript(() => { try { localStorage.setItem('rundgang-schloessli-registre', '1'); } catch (e) {} }); const p = await c.newPage();
    await p.goto(A + '?gruss=tag#' + v); await p.waitForFunction(() => window.BG_REGISTRE === 1 && document.documentElement.classList.contains('auftakt-da')); await p.waitForTimeout(3800);
    if (y) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(3600); }
    if (vor) await vor(p);
    await p.screenshot({ path: path.join(AUS, id + '.jpg'), type: 'jpeg', quality: 82 });
    await c.close();
  }
  await b.close();
  console.log('Bilder:', fs.readdirSync(AUS).join(' '));
})();
