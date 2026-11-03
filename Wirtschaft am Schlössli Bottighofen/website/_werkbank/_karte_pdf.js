
const path = require('path');
const { chromium } = require(process.env.HOME + '/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('http://127.0.0.1:8982/werkbank/karte.html', { waitUntil: 'load' }); await p.evaluate(() => document.fonts && document.fonts.ready);
  await p.pdf({ path: process.argv[2], format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); console.log('PDF', process.argv[2]); })();
