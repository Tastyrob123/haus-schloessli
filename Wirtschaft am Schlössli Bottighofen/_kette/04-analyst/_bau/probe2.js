module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright');
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
(async () => {
  const b = await chromium.launch(); const desk = process.argv[3] === 'desk';
  const c = await b.newContext(desk ? { viewport: { width: 1440, height: 900 }, locale: 'de-CH' } : { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, userAgent: UA, locale: 'de-CH' });
  const p = await c.newPage(); const hosts = new Set(); p.on('request', r => { try { hosts.add(new URL(r.url()).host); } catch (e) {} });
  await p.goto('https://www.schloessli-bottighofen.ch' + (process.argv[2] || '/'), { waitUntil: 'load', timeout: 90000 });
  await p.waitForTimeout(5000);
  await p.evaluate(() => { const x = [...document.querySelectorAll('button')].find(e => e.textContent.trim() === 'ablehnen'); if (x) x.click(); });
  await p.evaluate(async () => { const h = document.body.scrollHeight; for (let y = 0; y < h; y += 400) { scrollTo(0, y); await new Promise(r => setTimeout(r, 150)); } scrollTo(0, 0); });
  await p.waitForTimeout(1000);
  const info = await p.evaluate(() => {
    const vis = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
    const btn = [...document.querySelectorAll('a,button')].filter(vis).map(e => { const r = e.getBoundingClientRect(); return [e.innerText.trim().replace(/\s+/g, ' ').slice(0, 50), Math.round(r.x), Math.round(r.y + scrollY), Math.round(r.width), Math.round(r.height), (e.getAttribute('href') || '').slice(0, 90)]; });
    const imgs = [...document.querySelectorAll('img')].filter(vis).map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.y + scrollY), Math.round(r.width), Math.round(r.height), (e.alt || '').slice(0, 60), e.src.split('/').pop().slice(0, 50)]; });
    const caps = [...document.querySelectorAll('figcaption, .image-caption, .image-subtitle, .gallery-caption')].filter(vis).map(e => [Math.round(e.getBoundingClientRect().y + scrollY), e.innerText.trim().slice(0, 90)]);
    const h = [...document.querySelectorAll('h1,h2,h3,h4')].filter(vis).map(e => [e.tagName, Math.round(e.getBoundingClientRect().y + scrollY), e.innerText.trim().slice(0, 70)]);
    return { H: document.documentElement.scrollHeight, title: document.title, desc: (document.querySelector('meta[name=description]') || {}).content, btn, imgs, caps, h };
  });
  console.log(JSON.stringify(info));
  console.log('HOSTS', [...hosts].join(' '));
  await b.close();
})();
