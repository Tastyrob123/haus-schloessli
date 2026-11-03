// Beleg 13: die englische Seite des Guide Michelin zum Haus, am Rechner (unsichtbar). → stellen/michelin-en.png + Eintrag in stellen/stellen.json
module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const c = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, locale: 'en-GB' }); const p = await c.newPage();
  const url = 'https://guide.michelin.com/ch/en/thurgau/bottighofen_1149146/restaurant/wirtschaft-am-schlossli';
  await p.goto(url, { waitUntil: 'load', timeout: 90000 }); await p.waitForTimeout(6000);
  await p.evaluate(() => { const x = [...document.querySelectorAll('button')].find(e => /reject|decline|ablehnen|refuse/i.test(e.textContent)); if (x) x.click(); }); await p.waitForTimeout(1500);
  const t = await p.evaluate(() => document.body.innerText.slice(0, 600)); console.log(t);
  const m = await p.evaluate(() => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (n.data.trim() === 'Wirtschaft am Schlössli') { const r = n.parentElement.getBoundingClientRect(); if (r.width > 50 && r.top > 0 && r.top < 900) return { t: 'Wirtschaft am Schlössli', x: r.left, y: r.top, w: r.width, h: r.height }; } return null; });
  await p.screenshot({ path: __dirname + '/stellen/michelin-en.png' });
  const S = JSON.parse(fs.readFileSync(__dirname + '/stellen/stellen.json')); S['michelin-en'] = { url, pfad: url, desk: true, W: 1440, H: 900, f: 2, y0: 0, marks: m ? [m] : [], zeit: new Date().toISOString() };
  fs.writeFileSync(__dirname + '/stellen/stellen.json', JSON.stringify(S, null, 1)); console.log(JSON.stringify(m)); await b.close(); })();
