// Aufnahmen für die Werkbank der Wirtschaft am Schlössli (19.10.2026): Ideen (Rechner 1440 × 900) und Gäste-Funktionen (Rechner + Handy 390 × 844).
//   node _werkbank/sb_ideen.js [name …]  →  _werkbank/ansichten/Ideen/<name>.jpg, ansichten/Gaeste/<name>.jpg und <name>-h.jpg
// Jede Stelle: Seite, Anker (Abschnitt oben an den Rand), Verschiebung in px, optional ein Klick vor der Aufnahme. Nichts wird abgeschickt.
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const HIER = __dirname, B = 'http://127.0.0.1:' + (process.env.WB_PORT || 9288) + '/';
const IDEEN = [
  ['start', 'index.html', null, 0], ['willkommen', 'index.html', '#willkommen', 0], ['laestermeile', 'index.html', '#laestermeile', 0],
  ['karte', 'index.html', '#karte', 0], ['kueche', 'index.html', '#kueche', 0], ['keller', 'index.html', '#keller', 0], ['besen', 'index.html', '#besen', 0],
  ['laender', 'karte.html', '#laender', 0], ['mittag', 'karte.html', '#mittag', 0], ['etagen', 'feiern.html', '#etagen', 0],
  ['naechster', 'anlaesse.html', '#naechster', 0], ['schaefli', 'team.html', '#schaefli', 0],
];
const GAESTE = [   // name, Seite, Anker, Verschiebung, Klick (Selektor) oder null
  ['berater', 'weinkarte.html', '#berater', 0, null], ['wein-gang', 'karte.html', '#wein-zum-gang', 0, null],
  ['abend', 'abend.html', '#zusammenstellen', 0, null], ['gutschein', 'gutschein.html', '#gestalten', 0, null],
  ['kalender', 'anlaesse.html', '#kalender', 0, null], ['see', 'kontakt.html', '#see', 0, null],
  ['reservation', 'index.html', null, 0, '.ecke--r a[data-fenster="fe-reservation"]'], ['bankett', 'index.html', '#feiern', 0, null],
];
const nur = process.argv.slice(2);
async function stelle(p, seite, anker, dy, klick) {
  await p.goto(B + seite, { waitUntil: 'load' }); await p.evaluate(() => document.fonts && document.fonts.ready);
  await p.waitForTimeout(seite === 'index.html' ? 5200 : 2600);
  await p.evaluate(async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); } });
  if (anker) await p.evaluate(([a, dy]) => { const e = document.querySelector(a); if (e) scrollTo(0, e.getBoundingClientRect().top + scrollY + dy); }, [anker, dy]);
  else await p.evaluate(() => scrollTo(0, 0));
  await p.waitForTimeout(2600);
  if (klick) { const k = await p.$(klick); if (k) { await k.click().catch(() => {}); await p.waitForTimeout(1600); } else console.log('  kein Ziel für Klick', klick); }
}
(async () => {
  for (const d of ['Ideen', 'Gaeste']) fs.mkdirSync(path.join(HIER, 'ansichten', d), { recursive: true });
  const b = await chromium.launch({ headless: true });
  const r = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 }); const p = await r.newPage(); p.setDefaultTimeout(240000);
  for (const [n, s, a, dy] of IDEEN) { if (nur.length && !nur.includes(n)) continue; await stelle(p, s, a, dy); await p.screenshot({ path: path.join(HIER, 'ansichten/Ideen', n + '.jpg'), quality: 88 }); console.log('Idee', n); }
  for (const [n, s, a, dy, k] of GAESTE) { if (nur.length && !nur.includes(n)) continue; await stelle(p, s, a, dy, k); await p.screenshot({ path: path.join(HIER, 'ansichten/Gaeste', n + '.jpg'), quality: 88 }); console.log('Gast', n); }
  const h = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }); const q = await h.newPage(); q.setDefaultTimeout(240000);
  for (const [n, s, a, dy, k] of GAESTE) { if (nur.length && !nur.includes(n)) continue; await stelle(q, s, a, dy, k); await q.screenshot({ path: path.join(HIER, 'ansichten/Gaeste', n + '-h.jpg'), quality: 88 }); console.log('Gast Handy', n); }
  await b.close();
})();
