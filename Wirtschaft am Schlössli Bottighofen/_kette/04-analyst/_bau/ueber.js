module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const pw = require('playwright');
(async () => { const b = await pw.webkit.launch(); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  await p.goto('http://127.0.0.1:8978/haus/Wirtschaft%20am%20Schl%C3%B6ssli%20Bottighofen/_kette/04-analyst/potential/', { waitUntil: 'load' });
  console.log(JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth + 1).slice(0, 12).map(e => [e.tagName, e.className, Math.round(e.getBoundingClientRect().right), (e.textContent || '').slice(0, 40)]))));
  await b.close(); })();
