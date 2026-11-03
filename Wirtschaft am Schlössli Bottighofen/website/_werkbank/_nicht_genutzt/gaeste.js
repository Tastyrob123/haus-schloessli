// Aufnahmen der Gäste-Funktionen des Ruedihus für die Werkbank: node _werkbank/gaeste.js  →  _werkbank/ansichten/Gaeste/<name>.jpg
//   finder          Buchen-Fenster mit dem Zimmer-Finder (Zimmer mit Tagespreis aus dem Buchungssystem 11517, sonst Ab-Preise, Beispiel-Vergleich, Wetter der Tage)
//   vergleich       Ausschnitt: Preisvergleich · wetter-buchen: Ausschnitt: Wetter für die gebuchten Tage
//   tisch           Reiter «Tisch» im Buchen-Fenster: Stube wählen, Tag, Uhrzeit, Menü
//   gutschein       Gutschein online auf der Zimmer-Seite · heute: «Heute draussen oder in der Stube?» · rechner: «Welche Stube für Ihr Fest?»
//   anreise, anreise-2   «Vor Ihrer Anreise» · besuche: Bereich «Besuche & Anfragen» im Studio (Online-Probe, lokal stünde überall 0)
//   finder-h, tisch-h, anreise-lang   dieselben Dinge am Handy (anreise-lang = ganze Seite, scrollt im Handy der Werkbank)
// Nichts wird abgeschickt: Formulare werden nur ausgefüllt. Vorschau-Server des Hauses muss laufen (python3 serve.py 8917).
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = process.env.BASE || 'http://127.0.0.1:8917/', A = path.join(__dirname, 'ansichten', 'Gaeste');
const an = '2026-12-12', ab = '2026-12-14';
(async () => {
  fs.mkdirSync(A, { recursive: true });
  const br = await chromium.launch();
  const ctx = await br.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, locale: 'de-CH' });
  const p = await ctx.newPage();
  const foto = (n, o) => p.screenshot(Object.assign({ path: path.join(A, n + '.jpg'), quality: 90 }, o || {}));
  const ruhe = ms => p.waitForTimeout(ms);
  const zu = async (sel, luft = 80) => { await p.evaluate(([s, l]) => { const k = document.querySelector(s); if (k) scrollTo(0, k.getBoundingClientRect().top + scrollY - l); }, [sel, luft]); await ruhe(1500); };
  const ausschnitt = async (sel, n, luft = 24) => { const el = p.locator(sel).first(); if (!(await el.count())) { console.log('fehlt', n); return; } await el.scrollIntoViewIfNeeded({ timeout: 8000 }).catch(() => {}); await ruhe(900); const b = await el.boundingBox(); if (!b) { console.log('kein Ausschnitt', n); return; } await foto(n, { clip: { x: Math.max(0, b.x - luft), y: Math.max(0, b.y - luft), width: Math.min(1440, b.width + 2 * luft), height: b.height + 2 * luft } }); };

  // Zimmer-Finder im Buchen-Fenster (Preis kommt vom Buchungssystem über den Vorschau-Server; antwortet es nicht, stehen die Ab-Preise des Hauses)
  await p.goto(B + 'zimmer.html?nomotion', { waitUntil: 'load' }); await ruhe(1500);
  await p.click('[data-buchen="zimmer"]'); await ruhe(700);
  await p.fill('dialog.buchen [name=an]', an); await p.fill('dialog.buchen [name=ab]', ab); await p.selectOption('dialog.buchen [name=gaeste]', '2'); await ruhe(300);
  await foto('buchen');
  await p.click('dialog.buchen form[data-zimmer] button[type=submit]');
  await p.waitForSelector('.dn-treffer:not([hidden]) .dn-zi', { timeout: 30000 }).catch(() => console.log('kein Treffer'));
  await ruhe(2800);
  await foto('finder');
  await ausschnitt('.dn-pv', 'vergleich');
  // Reiter «Tisch»
  await p.click('#t-tisch'); await ruhe(900);
  await p.selectOption('dialog.buchen .dn-tisch [name=lokal]', { index: 0 }).catch(() => {}); await p.fill('dialog.buchen .dn-tisch [name=tag]', an).catch(() => {}); await ruhe(600);
  await foto('tisch');
  console.log('ok finder, tisch');

  // Gutschein online
  await p.goto(B + 'zimmer.html?nomotion#gutschein-online', { waitUntil: 'load' }); await ruhe(1200);
  await zu('#gutschein-online', 60);
  await p.click('[data-betrag="200"]').catch(() => {}); await p.fill('form[data-gutschein] [name=fuer]', 'Anna und Peter').catch(() => {}); await ruhe(900);
  await zu('#gutschein-online', 60);
  await foto('gutschein');
  console.log('ok gutschein');

  // Heute draussen oder in der Stube? · Welche Stube für Ihr Fest?
  await p.goto(B + 'essen.html?nomotion', { waitUntil: 'load' }); await ruhe(1200);
  await zu('#rechner', 70); await p.click('#rechner [data-stube="0"]').catch(() => {}); await p.fill('#rechner [name=erw]', '28'); await p.dispatchEvent('#rechner [name=erw]', 'input'); await p.check('#rechner [name=cuepli]').catch(() => {}); await ruhe(900);
  await zu('#rechner', 70);
  await foto('rechner');
  console.log('ok heute, rechner');

  // Vor Ihrer Anreise
  await p.goto(B + `anreise.html?nomotion&an=${an}&ab=${ab}&name=Anna%20Muster`, { waitUntil: 'load' }); await ruhe(1800);
  await foto('anreise');
  await zu('#tisch', 80); await ruhe(600); await foto('anreise-2');
  console.log('ok anreise');

  // Besuche & Anfragen im Studio (Online-Probe zählt die Seite schon; lokal stünde überall 0)
  await p.goto((process.env.STUDIO || 'https://ruedihus.tastystudios.ch/') + 'studio/#/besuche', { waitUntil: 'load' }).catch(e => console.log('Studio online nicht erreichbar', e.message));
  await p.waitForSelector('.tuer, .in h2', { timeout: 60000 }).catch(() => {}); await ruhe(3500);
  await foto('besuche');
  console.log('ok besuche');
  await ctx.close();

  // Handy
  const c2 = await br.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, locale: 'de-CH' });
  const q = await c2.newPage();
  const fotoH = (n, o) => q.screenshot(Object.assign({ path: path.join(A, n + '.jpg'), quality: 90 }, o || {}));
  await q.goto(B + `anreise.html?nomotion&an=${an}&ab=${ab}&name=Anna%20Muster`, { waitUntil: 'load' }); await q.waitForTimeout(2200);
  await q.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); }); await q.waitForTimeout(1500);
  await fotoH('anreise-h');
  await fotoH('anreise-lang', { fullPage: true });
  await q.goto(B + 'zimmer.html?nomotion', { waitUntil: 'load' }); await q.waitForTimeout(1200);
  await q.evaluate(() => document.querySelector('[data-buchen="zimmer"]').click()); await q.waitForTimeout(600);
  await q.fill('dialog.buchen [name=an]', an); await q.fill('dialog.buchen [name=ab]', ab);
  await q.evaluate(() => document.querySelector('dialog.buchen form[data-zimmer]').requestSubmit());
  await q.waitForSelector('.dn-treffer:not([hidden]) .dn-zi', { timeout: 30000 }).catch(() => {}); await q.waitForTimeout(2500); await fotoH('finder-h');
  await q.evaluate(() => document.querySelector('#t-tisch').click()); await q.waitForTimeout(900); await fotoH('tisch-h');
  console.log('ok handy');
  await br.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
