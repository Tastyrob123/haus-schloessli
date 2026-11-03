// Bildschirm nach Klick (Gutschein, Kontaktformular) bzw. an Textstelle; Rechner oder Handy. node probe3.js <pfad> <desk|m> <klicktext|-> <scrolltext|-> <name>
module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright');
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
(async () => {
  const [pfad, art, klick, ziel, name] = process.argv.slice(2); const desk = art === 'desk';
  const b = await chromium.launch();
  const c = await b.newContext(desk ? { viewport: { width: 1440, height: 900 }, locale: 'de-CH' } : { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, userAgent: UA, locale: 'de-CH' });
  const p = await c.newPage();
  await p.goto('https://www.schloessli-bottighofen.ch' + pfad, { waitUntil: 'load', timeout: 90000 }); await p.waitForTimeout(5000);
  await p.evaluate(() => { const x = [...document.querySelectorAll('button')].find(e => e.textContent.trim() === 'ablehnen'); if (x) x.click(); });
  await p.evaluate(async () => { const h = document.body.scrollHeight; for (let y = 0; y < h; y += 400) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); });
  if (ziel !== '-') await p.evaluate(t => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (n.data.includes(t)) { n.parentElement.scrollIntoView({ block: 'center' }); break; } }, ziel);
  await p.waitForTimeout(1200);
  if (klick !== '-') { await p.evaluate(t => { const x = [...document.querySelectorAll('button,a')].find(e => e.textContent.trim() === t); x.click(); }, klick); await p.waitForTimeout(2500); }
  await p.screenshot({ path: __dirname + '/probe/' + name + '.png' });
  console.log((await p.evaluate(() => document.body.innerText)).slice(0, 2500));
  await b.close();
})();
