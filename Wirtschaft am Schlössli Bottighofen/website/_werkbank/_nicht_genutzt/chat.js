// Aufnahmen der Rezeption im Chat für die Werkbank: node _werkbank/chat.js  →  _werkbank/ansichten/Chat/<name>.jpg
//   chat        Startseite mit geöffnetem Chat und der Antwort auf die Fondue-Frage
//   rezeption   Seite «Rezeption im Chat» oben · rezeption-2: «Ein Gast fragt nach dem Fondue» · rezeption-3: «Die Stube kennt jede Frage» · rezeption-4: «Buchen, ohne die Seite zu verlassen»
//   mappe       Zimmermappe (mappe.html) am Handy · chat-h: Chat am Handy
// Die Antworten kommen nicht aus der Funktion (sie läuft nur online und kostet je Frage), sondern stehen hier im Wortlaut der Antworten
// vom 10.10.2026, wie sie auf der Seite «Rezeption im Chat» dokumentiert sind. Vorschau-Server des Hauses muss laufen.
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = process.env.BASE || 'http://127.0.0.1:8917/', A = path.join(__dirname, 'ansichten', 'Chat');
const ANTWORT = {
  fondue: 'Ja, sehr gerne. Das Restaurant ist am Abend geöffnet und Fondue ist eine unserer Spezialitäten.\n- Restaurant geöffnet: 11:30 bis 21:00 Uhr\n- Friburger Original Chäsfondue: CHF 29.00\n- Tisch reservieren: +41 33 675 81 81 oder info@doldenhorn.ch',
  alter: 'Das Ruedihus wurde 1753 erbaut und ist damit über 270 Jahre alt. Es gilt als Spitzenleistung der Zimmermannskunst im 18. Jahrhundert.',
};
const antworte = (ctx, text) => ctx.route('**/api/gast*', r => r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ text }) }));
(async () => {
  fs.mkdirSync(A, { recursive: true });
  const br = await chromium.launch();
  const ctx = await br.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, locale: 'de-CH' });
  await antworte(ctx, ANTWORT.fondue);
  const p = await ctx.newPage();
  const foto = n => p.screenshot({ path: path.join(A, n + '.jpg'), quality: 90 });
  const ruhe = ms => p.waitForTimeout(ms);

  await p.goto(B + 'index.html?nomotion', { waitUntil: 'load' }); await ruhe(2500);
  await p.evaluate(() => scrollTo(0, Math.round(innerHeight * 1.15))); await ruhe(1200);
  await p.click('.gast-knopf'); await ruhe(900);
  await p.locator('.gast__feld input').first().click().catch(() => {});
  await p.keyboard.type('Wir sind zu zweit und möchten am Abend Fondue essen. Geht das?', { delay: 18 }); await p.keyboard.press('Enter'); await ruhe(4200);
  await foto('chat');
  console.log('ok chat');

  // Seite «Rezeption im Chat»
  await p.goto(B + 'rezeption/?nomotion', { waitUntil: 'load' }); await ruhe(3500); await foto('rezeption');
  await p.addStyleTag({ content: 'header.leiste,.leiste,.rz-leiste{display:none!important}' });
  const zuH2 = async (re, n) => { await p.evaluate(r => { const h = [...document.querySelectorAll('h2')].find(x => new RegExp(r).test(x.textContent)); if (h) scrollTo(0, h.getBoundingClientRect().top + scrollY - 60); }, re); await ruhe(2400); await foto(n); };
  await zuH2('Gast fragt', 'rezeption-2');
  await zuH2('Stube kennt', 'rezeption-3');
  await zuH2('Buchen, ohne', 'rezeption-4');
  console.log('ok rezeption');
  await ctx.close();

  // Handy: Chat offen und die Zimmermappe
  const c2 = await br.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, locale: 'de-CH' });
  await antworte(c2, ANTWORT.alter);
  const q = await c2.newPage();
  await q.goto(B + 'index.html?nomotion', { waitUntil: 'load' }); await q.waitForTimeout(2000);
  await q.evaluate(() => document.querySelector('.gast-knopf').click()); await q.waitForTimeout(900);
  await q.locator('.gast__feld input').first().click().catch(() => {}); await q.keyboard.type('Wie alt ist das Haus?', { delay: 20 }); await q.keyboard.press('Enter'); await q.waitForTimeout(3200);
  await q.screenshot({ path: path.join(A, 'chat-h.jpg'), quality: 90 });
  console.log('ok chat-h');
  const r = await q.goto(B + 'mappe.html?nomotion', { waitUntil: 'load' }).catch(() => null);
  if (r && r.ok()) {
    await q.waitForTimeout(1800);
    await q.locator('.gast__feld input').first().click().catch(() => {}); await q.keyboard.type('Wie alt ist das Haus?', { delay: 20 }); await q.keyboard.press('Enter'); await q.waitForTimeout(3200);
    await q.screenshot({ path: path.join(A, 'mappe.jpg'), quality: 90 }); console.log('ok mappe');
  } else console.log('mappe.html fehlt');
  await br.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
