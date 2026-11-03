// Bildschirmfotos für die Anleitung (bilder/rez-*.jpg) · Wirtschaft am Schlössli (Nachtbau 3.11.2026, Muster aus dem Stamm).
// Aufruf: node _bau/anleitung_bilder.js http://127.0.0.1:9284/_werkzeuge/reception/   (danach daten/ löschen und den Server neu starten: frische Beispiele)
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = process.argv[2] || 'http://127.0.0.1:9284/_werkzeuge/reception/';
const OUT = path.join(__dirname, '..', 'bilder'); fs.mkdirSync(OUT, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const br = await chromium.launch();
  const ctx = await br.newContext({ viewport: { width: 1440, height: 900 }, locale: 'de-CH', deviceScaleFactor: 1 });
  await ctx.route(/^(mailto|tel|sms):/, r => r.abort());
  await ctx.addInitScript(() => { try { localStorage.setItem('reception-name', 'Team Schlössli'); localStorage.setItem('rundgang-reception', '1'); localStorage.setItem('rundgang-savoir', '1'); } catch (e) { /* */ } });
  const p = await ctx.newPage(); p.setDefaultTimeout(15000);
  const foto = async n => { await sleep(900); await p.screenshot({ path: path.join(OUT, `rez-${n}.jpg`), type: 'jpeg', quality: 82 }); console.log('Bild', n); };
  const gehe = async a => { await p.goto('about:blank'); await p.goto(B + '#' + a, { waitUntil: 'load' }); await sleep(3200); };
  await gehe('start'); await foto('uebersicht');
  await gehe('eingang'); await p.locator('.re-liste .re-a', { hasText: 'Sandra Keller' }).click(); await sleep(900); await foto('eingang');
  await p.locator('#brief .gs--p').nth(1).scrollIntoViewIfNeeded(); await p.locator('#brief .gs--p').nth(1).click(); await sleep(500); await foto('gestalten');
  await p.click('[data-w="foto"]'); await sleep(900); await foto('foto'); await p.keyboard.press('Escape'); await sleep(300);
  await gehe('eingang'); await p.locator('.re-liste .re-a', { hasText: 'Emma Clarke' }).click(); await sleep(900); await p.click('#detail [data-akt="deutsch"]'); await p.waitForSelector('.re-de__text'); await sleep(600); await p.locator('.re-de').scrollIntoViewIfNeeded(); await foto('deutsch');
  await gehe('gefragt'); await foto('gefragt');
  await p.click('.filter [data-wahl="luecke"]'); await sleep(600); await p.locator('.re-f [data-akt="nachtragen"]').first().click(); await p.waitForSelector('#f-antwort'); await foto('nachtragen'); await p.keyboard.press('Escape');
  await gehe('nachgetragen'); await foto('nachgetragen');
  await gehe('wissen'); await foto('wissen');
  await p.click('#k-probe'); await p.waitForSelector('.ws-handy'); await sleep(1200); await p.click('.probe__fragen [data-frage]'); await p.waitForFunction(() => document.querySelectorAll('#probe-l .ws-bl--haus').length >= 2 && !document.querySelector('.ws-bl--wartet'), null, { timeout: 20000 }); await foto('probe');
  await br.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
