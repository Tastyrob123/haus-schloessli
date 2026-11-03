module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const pw = require('playwright');
(async () => { const b = await pw.chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
  const f = []; p.on('console', m => { if (m.type() === 'error') f.push(m.text()); }); p.on('pageerror', e => f.push(String(e)));
  // Seite selbst: alle Bilder eager laden und zählen
  await p.goto('http://127.0.0.1:8978/haus/Wirtschaft%20am%20Schl%C3%B6ssli%20Bottighofen/_kette/04-analyst/potential/', { waitUntil: 'load' });
  await p.evaluate(() => document.querySelectorAll('img').forEach(i => i.loading = 'eager')); await p.waitForTimeout(3000);
  console.log('bilder', JSON.stringify(await p.evaluate(() => ({ n: document.images.length, kaputt: [...document.images].filter(i => !i.naturalWidth).map(i => i.src) }))));
  await p.goto('http://127.0.0.1:8978/?haus=Wirtschaft%20am%20Schl%C3%B6ssli%20Bottighofen', { waitUntil: 'load' }); await p.waitForTimeout(2500);
  console.log('karte', JSON.stringify(f), (await p.evaluate(() => document.body.innerText)).match(/Potentialanalyse[^\n]*\n?[^\n]*/g));
  await b.close(); })();
