// Flüssigkeit des Gastgebers gedrosselt (Regel 55, Prüf-Chat 17.10.2026; Vorbild Carlton pruefung/fluss.js): je Drossel 1×/4×/6× Öffnen bis Inhalt,
// Wechsel jeder Ansicht über den Rand, Rollen jeder Ansicht (Bildabstände per requestAnimationFrame), Verschieben beim Laden. Bricht ab, wenn die
// Rechnerlast (1 Minute) bei 8 oder mehr liegt, und misst dann nichts (Master F26).
//   node fluss.js <url-des-werkzeugs> [breite] [höhe]        z. B. node fluss.js http://localhost:9051/_werkzeuge/reception/ 1440 900
const path = require('path'), os = require('os'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const [, , B, W = '1440', H = '900'] = process.argv;
const HANDY = +W < 700, ANS = ['start', 'eingang', 'gefragt', 'nachgetragen', 'wissen'];
(async () => {
  const aus = [];
  for (const D of [1, 4, 6]) {
    const last = os.loadavg()[0];
    if (last >= 8) { console.log(JSON.stringify({ drossel: D + '×', last: +last.toFixed(1), werten: false, grund: 'Rechnerlast ab 8, nicht gemessen' })); aus.push({ drossel: D, last, werten: false }); continue; }
    const br = await require('./schutz').start(pw, 'chromium'); const ctx = await require('./schutz').kontext(br, { viewport: { width: +W, height: +H }, locale: 'de-CH', isMobile: HANDY, hasTouch: HANDY });
    await ctx.addInitScript(() => { try { localStorage.setItem('reception-name', 'QA'); localStorage.setItem('rundgang-rh-reception', '1'); } catch (e) { /* */ }
      window.__cls = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
    const p = await ctx.newPage(); const c = await ctx.newCDPSession(p);
    await c.send('Emulation.setCPUThrottlingRate', { rate: D }); await c.send('Network.enable'); await c.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 2e6, uploadThroughput: 1e6 });
    const rollen = () => p.evaluate(async () => { const z = []; let v = performance.now(); let n = 0; scrollTo(0, 0); await new Promise(r => { function f(t) { z.push(t - v); v = t; scrollBy(0, 30); if (++n < 150) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
      z.shift(); z.sort((a, b) => a - b); return { median: +z[Math.floor(z.length / 2)].toFixed(1), p95: +z[Math.floor(z.length * .95)].toFixed(1), ueber50: z.filter(x => x > 50).length }; });
    const t0 = Date.now(); await p.goto(B + '#start', { waitUntil: 'load' }); await p.waitForSelector('#ansicht .lage', { timeout: 30000 }); await p.waitForFunction(() => !document.documentElement.classList.contains('auftakt') && !document.body.classList.contains('auftakt'), null, { timeout: 8000 }).catch(() => {});
    const r = { drossel: D + '×', breite: +W, last: +last.toFixed(1), oeffnen_ms: Date.now() - t0, ansichten: {} };
    for (const a of ANS) {
      if (HANDY) { await p.click('#rand .rand__auf'); await p.waitForTimeout(350); }
      const t1 = Date.now(); await p.click(`#rand [data-gehe="${a}"]`); await p.waitForFunction(x => location.hash === '#' + x && document.querySelector('#ansicht > *'), a, { timeout: 20000 }); await p.waitForTimeout(50); const wechsel = Date.now() - t1;
      await p.waitForTimeout(900); r.ansichten[a] = { wechsel_ms: wechsel, ...(await rollen()) };
    }
    r.verschieben = +(await p.evaluate(() => window.__cls)).toFixed(3); r.last_ende = +os.loadavg()[0].toFixed(1); r.werten = r.last_ende < 8;
    console.log(JSON.stringify(r)); aus.push(r); await br.close();
  }
  const ziel = path.join(__dirname, 'lauf', `fluss-${W}x${H}.json`); fs.mkdirSync(path.dirname(ziel), { recursive: true }); fs.writeFileSync(ziel, JSON.stringify(aus, null, 1));
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(2); });
