/* blick2.js · wie blick.js, aber mit einer offenen Änderung im Entwurf (Wegwerf-Daten), dann Ausdruck in «entwurf» auswerten. */
const fs = require('fs'), path = require('path'), os = require('os'); const { spawn, execFileSync } = require('child_process');
const pw = require(path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const [M, BR, JS] = process.argv.slice(2); const W = +BR;
const BUREAU = path.resolve(__dirname, '..'), WS = path.join(os.homedir(), 'Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website');
const DATEN = fs.mkdtempSync(path.join(os.tmpdir(), 'dc-blick-')), PROBE = path.join(WS, `_probe-blick-${process.pid}`), PORT = 9125, B = `http://127.0.0.1:${PORT}`;
const warte = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  execFileSync('python3', [path.join(WS, 'probe.py'), 'schloessli'], { env: { ...process.env, WEBSITE_PROBE: PROBE } });
  const srv = spawn('python3', [path.join(BUREAU, 'serve.py'), String(PORT)], { env: { ...process.env, WERKZEUGE_DATEN: DATEN, WEBSITE_PROBE: PROBE, BUREAU_PRUEFLAUF: '1' }, stdio: 'ignore' });
  process.on('exit', () => { try { srv.kill(); fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true }); } catch (e) { } });
  for (let i = 0; i < 60; i++) { try { if ((await fetch(B + '/_werkzeuge/bureau/')).ok) break; } catch (e) { } await warte(250); }
  const br = await pw[M].launch({ headless: true });
  try { const p = await (await br.newContext({ viewport: { width: W, height: W < 700 ? 844 : 900 } })).newPage();
    await p.goto(B + '/_werkzeuge/bureau/?ansicht=hinweis', { waitUntil: 'load' }); await warte(2500);
    await p.locator('#ws-h-text').fill('Probe'); await p.locator('#ws-speichern').click(); await warte(1500);
    await p.goto(B + '/_werkzeuge/bureau/?ansicht=entwurf', { waitUntil: 'load' }); await warte(3000);
    console.log(JSON.stringify(await p.evaluate(JS), null, 1)); if (process.env.BILD) await p.screenshot({ path: process.env.BILD });
  } finally { await br.close(); process.exit(0); }
})();
