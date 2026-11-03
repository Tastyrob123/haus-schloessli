// Wetter-Ansichten für die Werkbank von der Online-Fassung (lokal antwortet der Wetterdienst nicht): node _werkbank/wetter.js
//   ansichten/Gaeste/finder.jpg (Zimmer-Finder mit Wetter der Tage), vergleich.jpg, wetter-buchen.jpg (Ausschnitte), heute.jpg («Heute draussen oder in der Stube?»), anreise-3.jpg (Vor Ihrer Anreise, Wetter)
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = process.env.BASE || 'https://ruedihus.tastystudios.ch/', A = path.join(__dirname, 'ansichten', 'Gaeste');
const an = '2026-12-12', ab = '2026-12-14';
(async () => {
  const br = await chromium.launch();
  const ctx = await br.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, locale: 'de-CH' });
  const p = await ctx.newPage();
  const foto = (n, o) => p.screenshot(Object.assign({ path: path.join(A, n + '.jpg'), quality: 90 }, o || {}));
  const ruhe = ms => p.waitForTimeout(ms);
  const zu = async (sel, luft = 70) => { await p.evaluate(([s, l]) => { const k = document.querySelector(s); if (k) scrollTo(0, k.getBoundingClientRect().top + scrollY - l); }, [sel, luft]); await ruhe(1500); };
  const ausschnitt = async (sel, n, luft = 24) => { const el = p.locator(sel).first(); if (!(await el.count())) { console.log('fehlt', n); return; } await el.scrollIntoViewIfNeeded().catch(() => {}); await ruhe(800); const b = await el.boundingBox(); if (!b) return; await foto(n, { clip: { x: Math.max(0, b.x - luft), y: Math.max(0, b.y - luft), width: Math.min(1440, b.width + 2 * luft), height: b.height + 2 * luft } }); console.log('ok', n); };
  await p.goto(B + 'zimmer.html?nomotion', { waitUntil: 'load' }); await ruhe(1800);
  await p.click('[data-buchen="zimmer"]'); await ruhe(700);
  await p.fill('dialog.buchen [name=an]', an); await p.fill('dialog.buchen [name=ab]', ab); await p.selectOption('dialog.buchen [name=gaeste]', '2');
  await p.click('dialog.buchen form[data-zimmer] button[type=submit]');
  await p.waitForSelector('.dn-treffer:not([hidden]) .dn-zi', { timeout: 40000 }).catch(() => console.log('kein Treffer'));
  await p.waitForSelector('.dn-rw', { timeout: 40000 }).catch(() => console.log('kein .dn-rw'));
  await ruhe(3200); await foto('finder'); console.log('ok finder');
  await ausschnitt('.dn-pv', 'vergleich'); await ausschnitt('.dn-rw', 'wetter-buchen');
  await p.goto(B + 'essen.html?nomotion', { waitUntil: 'load' }); await ruhe(1500);
  await zu('#heute'); await p.waitForSelector('#heute .dn-tag, #heute .dn-ort, #heute [data-vorschlag]:not([hidden])', { timeout: 40000 }).catch(() => console.log('kein Wetter heute')); await ruhe(1800); await zu('#heute'); await foto('heute'); console.log('ok heute');
  await p.goto(B + `anreise.html?nomotion&an=${an}&ab=${ab}&name=Anna%20Muster`, { waitUntil: 'load' }); await ruhe(1500);
  await zu('#wetter', 80); await p.waitForSelector('#wetter .dn-tag, #wetter .dn-rw, #wetter .dn-ort', { timeout: 40000 }).catch(() => console.log('kein Wetter Anreise')); await ruhe(1800); await zu('#wetter', 80); await foto('anreise-3'); console.log('ok anreise-3');
  await br.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
