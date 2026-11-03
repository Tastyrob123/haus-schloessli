// Erkundung der heutigen Seite (Analyst Schlössli): iPhone 390x844 Chromium, beim ersten Besuch; Cookie-Fenster, feste Knöpfe, sichtbare Texte.
module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright'); const fs = require('fs');
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
(async () => {
  const b = await chromium.launch();
  const desk = process.argv[3] === 'desk';
  const c = await b.newContext(desk ? { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, locale: 'de-CH' } : { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, userAgent: UA, locale: 'de-CH' });
  const p = await c.newPage(); const req = [];
  p.on('request', r => { try { req.push(new URL(r.url()).host); } catch (e) {} });
  await p.goto('https://www.schloessli-bottighofen.ch' + (process.argv[2] || '/'), { waitUntil: 'load', timeout: 90000 });
  await p.waitForTimeout(7000);
  await p.screenshot({ path: __dirname + '/probe/' + (desk ? 'd' : 'm') + '-erst.png' });
  const info = await p.evaluate(() => {
    const vis = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && r.top < innerHeight && r.bottom > 0; };
    const fixed = [...document.querySelectorAll('body *')].filter(e => ['fixed', 'sticky'].includes(getComputedStyle(e).position) && vis(e)).map(e => ({ tag: e.tagName, cls: String(e.className).slice(0, 60), t: e.innerText.slice(0, 200), r: e.getBoundingClientRect().toJSON(), z: getComputedStyle(e).zIndex }));
    const btn = [...document.querySelectorAll('a,button')].filter(vis).map(e => ({ t: e.innerText.trim().slice(0, 40), r: [e.getBoundingClientRect().x, e.getBoundingClientRect().y, e.getBoundingClientRect().width, e.getBoundingClientRect().height].map(Math.round), href: e.getAttribute('href') }));
    return { fixed, btn, text: document.body.innerText.slice(0, 1500) };
  });
  console.log(JSON.stringify(info, null, 1));
  console.log('HOSTS', [...new Set(req)].join(' '));
  await b.close();
})();
