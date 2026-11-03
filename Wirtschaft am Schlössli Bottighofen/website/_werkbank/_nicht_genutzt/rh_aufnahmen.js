// Werkbank Landgasthof Ruedihus, Werkbank-Chat 17.10.2026: einzelne Aufnahmen für die Bühne «Einmal ändern, überall richtig.» (rh_strom.py)
//   node _werkbank/rh_aufnahmen.js [http://127.0.0.1:8917]   → _werkbank/ansichten/Strom/<name>.jpg
// Headless Chromium, eigenes Profil, nichts im Vordergrund; mailto- und tel-Links werden abgefangen, Formulare schicken nichts ab.
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = (process.argv[2] || 'http://127.0.0.1:8917').replace(/\/$/, '');
const ZIEL = path.join(__dirname, 'ansichten', 'Strom');
const AUF = [   // Name, Seite mit Anker, Breite, Höhe
  ['karte-rechner', '/essen.html#karte', 1440, 900],
  ['karte-handy', '/essen.html#karte', 390, 844],
  // ['vorschlag', …] raus (Robert 18.10.2026 23:23): die Aufnahme kam ohne Gestaltung heraus; ansichten/Strom/vorschlag.jpg ist jetzt die gestaltete Karte (Kopf, I, II mit Paketen, III), aus karte.html im Safari-Kern aufgenommen
  ['analyse', 'https://ruedihus-analyse.tastystudios.ch/', 1440, 900],   // die Potenzialanalyse für das Objekt «analyse» (Register, Fuss)   // die Karte «Ein Vorschlag.» für das Objekt im Fuss (objekte_bau.py)
];
const NUR = process.argv.slice(3);
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  const b = await chromium.launch({ headless: true });
  for (const [n, s, w, h, ganz] of AUF) {
    if (NUR.length && !NUR.includes(n)) continue;
    const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: w < 700, hasTouch: w < 700 });
    const p = await c.newPage();
    await p.route('**/*', r => (r.request().method() === 'GET' || r.request().method() === 'HEAD') ? r.continue() : r.fulfill({ status: 204, body: '' }));
    await p.goto((s.startsWith('http') ? '' : B) + s.split('#')[0], { waitUntil: 'load' });
    await p.evaluate(async () => { const H = document.documentElement.scrollHeight; for (let y = 0; y < H; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } });
    if (s.includes('#')) await p.evaluate(a => { const el = document.querySelector(a); if (el) el.scrollIntoView({ block: 'start' }); }, '#' + s.split('#')[1]); else await p.evaluate(() => scrollTo(0, 0));
    await p.waitForTimeout(2600);
    await p.screenshot({ path: path.join(ZIEL, n + '.jpg'), type: 'jpeg', quality: 86, fullPage: !!ganz });
    console.log('ok', n);
    await c.close();
  }
  await b.close();
})();
