/* tippen2.js · Demo-Check: Tippen per Koordinate auf «Wenn es Abend wird am Hafen» in der Vorschau (Chromium 390, Handy-Nachbildung). */
const fs = require('fs'), path = require('path'), os = require('os'); const { spawn, execFileSync } = require('child_process');
const pw = require(path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const BUREAU = path.resolve(__dirname, '..'), WS = path.join(os.homedir(), 'Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website');
const DATEN = fs.mkdtempSync(path.join(os.tmpdir(), 'dc-tip-')), PROBE = path.join(WS, `_probe-tip-${process.pid}`), PORT = 9124, B = `http://127.0.0.1:${PORT}`;
const warte = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  execFileSync('python3', [path.join(WS, 'probe.py'), 'schloessli'], { env: { ...process.env, WEBSITE_PROBE: PROBE } });
  const srv = spawn('python3', [path.join(BUREAU, 'serve.py'), String(PORT)], { env: { ...process.env, WERKZEUGE_DATEN: DATEN, WEBSITE_PROBE: PROBE }, stdio: 'ignore' });
  for (let i = 0; i < 60; i++) { try { if ((await fetch(B + '/_werkzeuge/bureau/')).ok) break; } catch (e) { } await warte(250); }
  const br = await pw.chromium.launch({ headless: true });
  try {
    const p = await (await br.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true })).newPage();
    await p.goto(B + '/_werkzeuge/bureau/?ansicht=b:start', { waitUntil: 'load' }); await warte(5000);
    const f = p.locator('iframe[data-ws-frame="entwurf"]'); await f.scrollIntoViewIfNeeded(); await warte(400);
    const r = await p.evaluate(() => { const f = document.querySelector('iframe[data-ws-frame="entwurf"]'); const d = f.contentDocument; const e = [...d.querySelectorAll('[data-ws-e]')].find(x => /Wenn es Abend/.test(x.textContent)); e.scrollIntoView({ block: 'center' }); const a = e.getBoundingClientRect(), b = f.getBoundingClientRect(); return { x: b.left + a.left + 20, y: b.top + a.top + a.height / 2, h: e.dataset.wsE, n: e.dataset.wsN }; });
    await warte(500); await p.touchscreen.tap(r.x, r.y);
    const ok = await p.waitForSelector(`[data-ws-form="text"][data-ws-wahl$="|${r.h}|${r.n}"]`, { timeout: 6000 }).then(() => true).catch(() => false);
    console.log('Tippen per Koordinate öffnet die Stelle:', ok, JSON.stringify(r));
  } finally { await br.close(); srv.kill(); fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true }); }
})();
