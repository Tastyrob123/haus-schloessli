// Aufnahmen für die Ideen-Karten der Werkbank, Stand der Website vom 17.10.2026 (Werkbank-Chat; ersetzt ideen.js vom 10.10., dessen Stellen es nicht mehr gibt):
//   node _werkbank/rh_ideen.js  →  _werkbank/ansichten/Ideen/<name>.jpg   (Hausserver :8917 muss laufen)
//   frage    «Was führt Sie zu uns?» mit Einkerbung, zweite Wahl getippt · zimmer: vier Zimmer der Startseite in zwei Spalten · stuben: fünf Stuben auf zwei Tafeln
//   grundsatz das Fenster mit dem Satz aus der Karte · sockel: eine Zimmerseite, gross mit Sockel · jahr: «Durchs Jahr», Jahreslauf in der Kerbe
//   menu     Weihnachten mit kleiner Menukarte und drei Bildern · noten: So sehen es die Gäste · stellen: eine offene Stelle im Fenster
//   warum    «Warum im Ruedihus?» aus Sicht der Bewerber · bewerben: das kleine Bewerbungs-Fenster einer Stelle (nur geöffnet, nichts abgeschickt)
// Headless, eigenes Profil; nichts wird abgeschickt (nur GET), mailto/tel werden abgefangen.
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = process.env.BASE || 'http://127.0.0.1:8917/', A = path.join(__dirname, 'ansichten', 'Ideen');
(async () => {
  fs.mkdirSync(A, { recursive: true });
  const br = await chromium.launch({ headless: true });
  const p = await (await br.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, locale: 'de-CH' })).newPage();
  await p.route('**/*', r => ['GET', 'HEAD'].includes(r.request().method()) ? r.continue() : r.fulfill({ status: 204, body: '' }));
  await p.route(/^(mailto|tel):/, r => r.abort());
  const foto = n => p.screenshot({ path: path.join(A, n + '.jpg'), quality: 90 }).then(() => console.log('ok', n));
  const ruhe = ms => p.waitForTimeout(ms);
  const zu = async (sel, luft = 90) => { await p.evaluate(([s, l]) => { const k = document.querySelector(s); if (k) scrollTo(0, k.getBoundingClientRect().top + scrollY - l); }, [sel, luft]); await ruhe(1900); };
  const seite = async f => { await p.goto(B + f, { waitUntil: 'load' }); await ruhe(1800); await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 110)); } scrollTo(0, 0); }); await ruhe(900); };

  await seite('index.html');
  await zu('#frage', 20); await p.locator('#frage .ke__wb').nth(1).click().catch(() => {}); await ruhe(1600); await zu('#frage', 20); await foto('frage');
  await zu('#zimmer', 60); await foto('zimmer');
  await zu('#gaeste', 60); await foto('noten');

  await seite('essen.html');
  await p.evaluate(() => { const f = [...document.querySelectorAll('section')].find(x => /Stockwerke/.test(x.textContent)); if (f) scrollTo(0, f.getBoundingClientRect().top + scrollY - 30); }); await ruhe(1900); await foto('stuben');
  await p.evaluate(() => { const f = [...document.querySelectorAll('section')].find(x => /vergebens/i.test(x.textContent) && !/Stockwerke/.test(x.textContent)); if (f) scrollTo(0, f.getBoundingClientRect().top + scrollY - 10); }); await ruhe(2000); await foto('grundsatz');

  await seite('zimmer-hochzeitsstube.html');
  await zu('#zimmer', 40); await foto('sockel');

  await seite('veranstaltungen.html');
  await zu('#jahr', 40); await foto('jahr');
  await zu('#a-weihnachten', 60); await foto('menu');

  await seite('haus.html');
  await zu('#warum', 40); await foto('warum');
  await zu('#offen', 60); await p.locator('#offen [data-stelle]').first().click().catch(() => {}); await ruhe(1500); await foto('stellen');
  await p.locator('[data-bewerben]:visible').first().click().catch(() => {}); await ruhe(1500); await foto('bewerben');   // nur geöffnet, nichts abgeschickt
  await br.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
