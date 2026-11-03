/* blick.js · ein Ausdruck in einer Ansicht auswerten (Demo-Check). node blick.js <motor> <breite> <ansicht> '<js>' */
const fs = require('fs'), path = require('path'), os = require('os'); const { spawn, execFileSync } = require('child_process');
const pw = require(path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const [M, BR, A, JS] = process.argv.slice(2); const W = +BR;
const BUREAU = path.resolve(__dirname, '..'), WS = path.join(os.homedir(), 'Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website');
const DATEN = fs.mkdtempSync(path.join(os.tmpdir(), 'dc-blick-')), PROBE = path.join(WS, `_probe-blick-${process.pid}`), PORT = +(process.env.PORT || 9122), B = `http://127.0.0.1:${PORT}`;
(async () => {
  execFileSync('python3', [path.join(WS, 'probe.py'), 'schloessli'], { env: { ...process.env, WEBSITE_PROBE: PROBE } });
  const srv = spawn('python3', [path.join(BUREAU, 'serve.py'), String(PORT)], { env: { ...process.env, WERKZEUGE_DATEN: DATEN, WEBSITE_PROBE: PROBE, BUREAU_PRUEFLAUF: '1' }, stdio: 'ignore' });
  for (let i = 0; i < 60; i++) { try { if ((await fetch(B + '/_werkzeuge/bureau/')).ok) break; } catch (e) { } await new Promise(r => setTimeout(r, 250)); }
  const br = await pw[M].launch({ headless: true });
  try { const p = await (await br.newContext({ viewport: { width: W, height: W < 700 ? 844 : 900 } })).newPage();
    await p.goto(B + (A.startsWith('/') ? A : '/_werkzeuge/bureau/?ansicht=' + encodeURIComponent(A)), { waitUntil: 'load' }); await new Promise(r => setTimeout(r, 3000));
    console.log(JSON.stringify(await p.evaluate(JS), null, 1)); if (process.env.BILD) await p.screenshot({ path: process.env.BILD });
  } finally { await br.close(); srv.kill(); fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true }); process.exit(0); }
})();
