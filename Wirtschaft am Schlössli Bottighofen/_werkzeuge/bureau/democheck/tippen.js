/* tippen.js · Demo-Check: Tippen/Klicken auf Texte in der Vorschau, je Motor und Breite (Fehlersuche). node tippen.js <motor> <breite> [tap|click] [ansicht] */
const fs = require('fs'), path = require('path'), os = require('os'); const { spawn, execFileSync } = require('child_process');
const pw = require(path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const [M, BR, ART = 'tap', A = 'b:start'] = process.argv.slice(2); const W = +BR, HANDY = W < 700;
const BUREAU = path.resolve(__dirname, '..'), WS = path.join(os.homedir(), 'Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website');
const DATEN = fs.mkdtempSync(path.join(os.tmpdir(), 'dc-tip-')), PROBE = path.join(WS, `_probe-tip-${process.pid}`), PORT = 9123, B = `http://127.0.0.1:${PORT}`;
const warte = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  execFileSync('python3', [path.join(WS, 'probe.py'), 'schloessli'], { env: { ...process.env, WEBSITE_PROBE: PROBE } });
  const srv = spawn('python3', [path.join(BUREAU, 'serve.py'), String(PORT)], { env: { ...process.env, WERKZEUGE_DATEN: DATEN, WEBSITE_PROBE: PROBE, BUREAU_PRUEFLAUF: '1' }, stdio: 'ignore' });
  for (let i = 0; i < 60; i++) { try { if ((await fetch(B + '/_werkzeuge/bureau/')).ok) break; } catch (e) { } await warte(250); }
  const br = await pw[M].launch({ headless: true });
  try {
    const ctx = await br.newContext({ viewport: { width: W, height: HANDY ? 844 : 900 }, hasTouch: HANDY, isMobile: HANDY && M === 'chromium' });
    const p = await ctx.newPage(); p.on('console', m => console.log('KONSOLE', m.type(), m.text().slice(0, 200))); p.on('pageerror', e => console.log('FEHLER', e.message));
    await p.goto(B + '/_werkzeuge/bureau/?ansicht=' + encodeURIComponent(A), { waitUntil: 'load' }); await warte(5000);
    const fr = p.frameLocator('iframe[data-ws-frame="entwurf"]');
    const liste = await p.evaluate(() => { const d = document.querySelector('iframe[data-ws-frame="entwurf"]').contentDocument; return [...d.querySelectorAll('main [data-ws-e]')].filter(e => !e.closest('[data-ws-zu]') && e.getBoundingClientRect().width > 40).map(e => ({ h: e.dataset.wsE, n: e.dataset.wsN, t: e.textContent.trim().slice(0, 40), tag: e.tagName })); });
    console.log('Stellen in der Vorschau:', liste.length);
    let gut = 0, schlecht = [];
    for (const st of liste.filter((x, i) => i % Math.max(1, Math.floor(liste.length / 12)) === 0).slice(0, 12)) {
      await p.evaluate(() => document.querySelectorAll('.ws-ed').forEach(x => x.remove()));
      const e = fr.locator(`[data-ws-e="${st.h}"][data-ws-n="${st.n}"]`).first();
      await e.evaluate(x => x.scrollIntoView({ block: 'center' }));
      await warte(300);
      const oben = await e.evaluate(x => { const r = x.getBoundingClientRect(); const t = x.ownerDocument.elementFromPoint(r.left + Math.min(20, r.width / 2), r.top + r.height / 2); return t === x || x.contains(t) ? 'frei' : (t ? t.tagName + '.' + t.className : 'nichts'); });
      try { if (ART === 'tap') await e.tap({ timeout: 5000 }); else await e.click({ timeout: 5000 }); } catch (x) { schlecht.push(st.t + ' (' + x.message.split('\n')[0].slice(0, 80) + ')'); continue; }
      const ok = await p.waitForSelector(`[data-ws-form="text"][data-ws-wahl$="|${st.h}|${st.n}"]`, { timeout: 6000 }).then(() => true).catch(() => false);
      if (ok) gut++; else schlecht.push(st.tag + ' «' + st.t + '» oben:' + oben);
    }
    console.log(`${M} ${W} ${ART}: ${gut} geöffnet, ${schlecht.length} nicht`); schlecht.forEach(x => console.log('  nicht: ' + x));
    if (process.env.BILD) await p.screenshot({ path: process.env.BILD });
  } finally { await br.close(); srv.kill(); fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true }); }
})();
