module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { webkit, devices } = require('playwright');
(async () => {
  const b = await webkit.launch(); const c = await b.newContext({ ...devices['iPhone 13'], locale: 'de-CH' }); const p = await c.newPage();
  await p.goto('https://www.schloessli-bottighofen.ch/', { waitUntil: 'load', timeout: 90000 }); await p.waitForTimeout(5000);
  await p.evaluate(() => { const x = [...document.querySelectorAll('button')].find(e => e.textContent.trim() === 'ablehnen'); if (x) x.click(); });
  await p.evaluate(() => { const a = [...document.querySelectorAll('a')].find(e => e.textContent.trim() === 'Reservation'); a.scrollIntoView({ block: 'center' }); });
  await p.waitForTimeout(2000);
  const st = await p.evaluate(() => [...document.querySelectorAll('a')].filter(e => ['Reservation', 'Lunch-Menü', 'Gutschein'].includes(e.textContent.trim())).map(e => { const s = getComputedStyle(e); return [e.textContent.trim(), e.className, s.backgroundColor, s.borderTopWidth + ' ' + s.borderTopStyle + ' ' + s.borderTopColor, s.color, s.letterSpacing]; }));
  console.log(JSON.stringify(st, null, 1));
  await p.screenshot({ path: __dirname + '/probe/webkit-reservation.png', timeout: 30000 });
  await b.close();
})();
