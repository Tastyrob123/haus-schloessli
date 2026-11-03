// Ansicht des Briefs (Gestalten, Nur Text, gewählter Baustein) als Bilder: node brief_ansicht.js <chromium|webkit> <Zielordner> [url]
const path = require('path');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const motor = process.argv[2] || 'chromium', OUT = process.argv[3] || '.', B = process.argv[4] || 'http://localhost:8938/_werkzeuge/reception/';
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function foto(p, datei) { const b = await p.evaluate(() => { const r = document.querySelector('#brief, .brief--bearb').getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, width: r.width, height: r.height }; }); await p.screenshot({ path: datei, fullPage: true, clip: b }); }
(async () => {
  const br = await require('./schutz').start(pw, motor);
  for (const [w, h, sf] of [[1440, 900, 1], [390, 844, 2]]) {
    const ctx = await require('./schutz').kontext(br, { viewport: { width: w, height: h }, locale: 'de-CH', deviceScaleFactor: sf, hasTouch: w < 700, isMobile: w < 700 && motor !== 'firefox' });
    await ctx.addInitScript(() => { try { localStorage.setItem('reception-name', 'Elke Johannes'); } catch (e) {} });
    const p = await ctx.newPage(); p.setDefaultTimeout(20000);
    await p.goto(B + '#eingang?probe=1', { waitUntil: 'load' }); await sleep(3500);
    await p.locator('.re-liste .re-a', { hasText: 'Brunner' }).first().click(); await p.waitForSelector('#brief'); await sleep(900);
    const ueberlauf = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, b: document.querySelector('#brief').getBoundingClientRect().width }));
    await foto(p, path.join(OUT, `brief-gestalt-${w}-${motor}.png`));
    await p.evaluate(() => { const e = document.querySelector('#brief [data-b="p1"]'); e.scrollIntoView({ block: 'center' }); e.dispatchEvent(new MouseEvent('click', { bubbles: true })); }); await sleep(500);
    await foto(p, path.join(OUT, `brief-wahl-${w}-${motor}.png`));
    await p.evaluate(() => document.querySelector('#detail [data-akt="bearbeiten"]').click()); await p.waitForSelector('#e-betreff'); await sleep(600);
    await foto(p, path.join(OUT, `brief-text-${w}-${motor}.png`));
    console.log(w, motor, JSON.stringify(ueberlauf));
    await ctx.close();
  }
  await br.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
