// Aufnahmen für die Ideen-Karten der Werkbank, jede an ihrer Stelle und, wo es etwas zu öffnen gibt, im geöffneten Zustand (Robert 10.10.2026):
//   node _werkbank/ideen.js  →  _werkbank/ansichten/Ideen/<name>.jpg
//   frage     «Was führt Sie zu uns?», zweite Karte gewählt · stuben: fünf Stuben auf zwei Tafeln · grundsatz: das Fenster mit dem Satz aus der Karte
//   zimmer    ein Zimmer mit seinen drei Fotos · buehne: «Alle Fotos» geöffnet · film: «Am Morgen die Vorhänge auf»
//   zahlen    1753 · 1908 · 1990 · 2000 · anlaesse: Metzgete, Stubete, Ruedi-Tag auf dem Jahreslineal · noten: Booking.com und Google
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = process.env.BASE || 'http://127.0.0.1:8917/', A = path.join(__dirname, 'ansichten', 'Ideen');
(async () => {
  fs.mkdirSync(A, { recursive: true });
  const br = await chromium.launch();
  const p = await (await br.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, locale: 'de-CH' })).newPage();
  const foto = n => p.screenshot({ path: path.join(A, n + '.jpg'), quality: 90 });
  const ruhe = ms => p.waitForTimeout(ms);
  const zu = async (sel, luft = 90) => { await p.evaluate(([s, l]) => { const k = document.querySelector(s); if (k) scrollTo(0, k.getBoundingClientRect().top + scrollY - l); }, [sel, luft]); await ruhe(1600); };
  const seite = async f => { await p.goto(B + f + (f.includes('?') ? '&' : '?') + 'nomotion', { waitUntil: 'load' }); await ruhe(1800); await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); } scrollTo(0, 0); }); await ruhe(800); };

  await seite('index.html');
  await zu('#frage', 30); await p.locator('#frage .rk__b').nth(1).click().catch(() => {}); await ruhe(1400); await p.evaluate(() => { const k = document.querySelector('#frage'); scrollTo(0, k.getBoundingClientRect().top + scrollY - 30); }); await ruhe(900); await foto('frage');
  await zu('.prunk', 120); await ruhe(2200); await foto('zahlen');
  await zu('#gaeste', 60); await ruhe(2000); await foto('noten');
  console.log('ok start');

  await seite('zimmer.html');
  await zu('#liebeslaube, [id="liebeslaube"]', 150).catch(() => {}); await ruhe(600); await foto('zimmer');
  const alle = p.locator('button:has-text("Alle")').first();
  if (await alle.count()) { await alle.scrollIntoViewIfNeeded(); await alle.click(); await p.waitForSelector('dialog.buehne[open]', { timeout: 8000 }).catch(() => {}); await ruhe(1600); await foto('buehne'); await p.keyboard.press('Escape'); await ruhe(400); }
  await zu('#wissen', 0).catch(() => {});
  await p.evaluate(() => { const v = document.querySelector('video'); if (v) { const b = v.closest('section') || v.parentElement; scrollTo(0, b.getBoundingClientRect().top + scrollY - 40); } }); await ruhe(1800); await foto('film');
  console.log('ok zimmer');

  await seite('essen.html');
  await zu('#stuben', 40); await ruhe(800); await foto('stuben');
  await p.evaluate(() => { const f = [...document.querySelectorAll('section')].find(x => /vergebens/i.test(x.textContent) && !/Stockwerke/.test(x.textContent)); if (f) scrollTo(0, f.getBoundingClientRect().top + scrollY - 10); }); await ruhe(2000); await foto('grundsatz');
  await zu('#jahr', 40); await ruhe(1200); await foto('anlaesse');
  console.log('ok essen');
  await br.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
