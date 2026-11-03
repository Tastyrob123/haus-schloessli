/* erkunden.js · Demo-Check 21.10.2026: Werkzeug mit Wegwerf-Daten und Wegwerf-Kopie starten, Ansicht öffnen, Knöpfe/Links auflisten, Bild.
   node erkunden.js <motor> <breite> <ansicht...> */
const fs = require('fs'), path = require('path'), os = require('os');
const { spawn, execFileSync } = require('child_process');
const pw = require(path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const [MOTOR = 'chromium', BR = '1440', ...ANS] = process.argv.slice(2); const BREITE = +BR, HOEHE = BREITE < 700 ? 844 : 900;
const BUREAU = path.resolve(__dirname, '..'), WS = path.join(os.homedir(), 'Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website');
const DATEN = fs.mkdtempSync(path.join(os.tmpdir(), 'dc-bureau-')), PROBE = path.join(WS, `_probe-democheck-${process.pid}`);
const PORT = +(process.env.PORT || 9121), B = `http://127.0.0.1:${PORT}`, BILD = process.env.BILD || path.join(__dirname, 'bilder'); fs.mkdirSync(BILD, { recursive: true });
const warte = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  execFileSync('python3', [path.join(WS, 'probe.py'), 'schloessli'], { env: { ...process.env, WEBSITE_PROBE: PROBE } });
  const srv = spawn('python3', [path.join(BUREAU, 'serve.py'), String(PORT)], { env: { ...process.env, WERKZEUGE_DATEN: DATEN, WEBSITE_PROBE: PROBE, BUREAU_PRUEFLAUF: '1' }, stdio: 'ignore' });
  for (let i = 0; i < 60; i++) { try { if ((await fetch(B + '/_werkzeuge/bureau/')).ok) break; } catch (e) { } await warte(250); }
  const br = await pw[MOTOR].launch({ headless: true });
  try {
    const ctx = await br.newContext({ viewport: { width: BREITE, height: HOEHE }, hasTouch: BREITE < 700, isMobile: BREITE < 700 && MOTOR === 'chromium' });
    const p = await ctx.newPage(); const log = [];
    p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') log.push(m.type() + ': ' + m.text()); }); p.on('pageerror', e => log.push('SEITE: ' + e.message));
    p.on('response', r => { if (r.status() >= 400) log.push('HTTP ' + r.status() + ' ' + r.url()); });
    for (const a of (ANS.length ? ANS : ['start'])) {
      await p.goto('about:blank'); await p.goto(B + '/_werkzeuge/bureau/?ansicht=' + encodeURIComponent(a), { waitUntil: 'networkidle' }); await warte(2500);
      const info = await p.evaluate(() => ({ bereit: document.querySelector('#ws-mitte')?.getAttribute('data-ws-bereit'), sw: document.documentElement.scrollWidth,
        knoepfe: [...document.querySelectorAll('button, a[href], [role=button]')].filter(e => e.getClientRects().length).map(e => (e.tagName + ' ' + (e.getAttribute('href') || '') + ' ' + (e.dataset.wsNav || '') + ' | ' + (e.innerText || e.getAttribute('aria-label') || e.title || '').replace(/\s+/g, ' ').slice(0, 60))) }));
      console.log('=== ' + a + ' bereit=' + info.bereit + ' scrollWidth=' + info.sw); info.knoepfe.forEach(k => console.log('  ' + k));
      await p.screenshot({ path: path.join(BILD, `${a.replace(/[:/]/g, '-')}-${MOTOR}-${BREITE}.png`), fullPage: !!process.env.GANZ });
    }
    console.log('LOG:\n' + [...new Set(log)].join('\n'));
  } finally { await br.close(); srv.kill(); fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true }); }
})();
