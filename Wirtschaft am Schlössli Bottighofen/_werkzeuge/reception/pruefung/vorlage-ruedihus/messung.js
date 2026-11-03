// Flüssigkeit des Gastgebers gedrosselt messen (Regel 55): Öffnen bis Inhalt, Wechsel zum Eingang, Rollen (Bildzeit p95), Verschieben beim Laden.
//   node messung.js <url-des-werkzeugs> [drossel 1|4|6] [breite] [höhe]     nur werten, wenn die Rechnerlast unter 8 liegt
const path = require('path'), os = require('os');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const [, , B, D = '4', W = '1440', H = '900'] = process.argv;
(async () => {
  const last = os.loadavg()[0];
  const br = await require('./schutz').start(pw, 'chromium'); const ctx = await require('./schutz').kontext(br, { viewport: { width: +W, height: +H }, locale: 'de-CH', isMobile: +W < 700, hasTouch: +W < 700 });
  await ctx.addInitScript(() => { try { localStorage.setItem('reception-name', 'QA'); localStorage.setItem('rundgang-rh-reception', '1'); } catch (e) {}
    window.__cls = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
  const p = await ctx.newPage(); const c = await ctx.newCDPSession(p);
  await c.send('Emulation.setCPUThrottlingRate', { rate: +D });
  await c.send('Network.enable'); await c.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 2e6, uploadThroughput: 1e6 });
  const t0 = Date.now(); await p.goto(B + '#start', { waitUntil: 'load' }); await p.waitForSelector('#ansicht .lage'); await p.waitForFunction(() => !document.documentElement.classList.contains('auftakt') && !document.body.classList.contains('auftakt'), null, { timeout: 8000 }).catch(() => {});
  const auf = Date.now() - t0;
  if (+W < 700) { await p.click('#rand .rand__auf'); await p.waitForTimeout(400); } const t1 = Date.now(); await p.click('#rand [data-gehe="eingang"]'); await p.waitForSelector('#detail'); const wechsel = Date.now() - t1;
  const bild = await p.evaluate(async () => { const z = []; let v = performance.now(); let n = 0; await new Promise(r => { function f(t) { z.push(t - v); v = t; scrollBy(0, 40); if (++n < 120) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); }); z.sort((a, b) => a - b); return z[Math.floor(z.length * .95)]; });
  const cls = await p.evaluate(() => window.__cls);
  console.log(JSON.stringify({ drossel: D + '×', breite: +W, last: +last.toFixed(1), oeffnen_ms: auf, wechsel_eingang_ms: wechsel, bildzeit_p95_ms: +bild.toFixed(1), verschieben: +cls.toFixed(3), werten: last < 8 }));
  await br.close();
})();
