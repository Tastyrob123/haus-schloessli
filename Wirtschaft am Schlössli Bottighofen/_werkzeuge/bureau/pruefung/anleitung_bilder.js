/* anleitung_bilder.js · echte Bildschirme für anleitung.html (Das Schaufenster, Wirtschaft am Schlössli; Aufbau aus dem Culinarium), 1440 × 900, mit eigenem
   Wegwerf-Server, Wegwerf-Daten und Wegwerf-Kopie der Seiten (ein Beispiel-Entwurf: ein Anlass der Ferien und ein Google-Titel), am Ende gelöscht.
   node anleitung_bilder.js → ../anleitung/*.webp */
const fs = require('fs'), path = require('path'), os = require('os'), net = require('net');
const { spawn, execFileSync } = require('child_process');
const pw = require(process.env.PLAYWRIGHT_PFAD || '/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const BUREAU = path.resolve(__dirname, '..'), HAUS = path.resolve(BUREAU, '..', '..'), WS = path.resolve(HAUS, '..', '_Werkzeuge', 'werkzeuge', 'website');
const DATEN = fs.mkdtempSync(path.join(os.tmpdir(), 'bureau-anl-')), PROBE = path.join(WS, `_probe-anl-${process.pid}`), ZIEL = path.join(BUREAU, 'anleitung');
const warte = ms => new Promise(r => setTimeout(r, ms));
const frei = () => new Promise(r => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => r(p)); }); });
(async () => {
  const PORT = await frei(), B = `http://127.0.0.1:${PORT}`;
  execFileSync('python3', [path.join(WS, 'probe.py'), 'schloessli'], { env: Object.assign({}, process.env, { WEBSITE_PROBE: PROBE }) });
  const srv = spawn('python3', [path.join(BUREAU, 'serve.py'), String(PORT)], { cwd: HAUS, env: Object.assign({}, process.env, { WERKZEUGE_DATEN: DATEN, WEBSITE_PROBE: PROBE, BUREAU_PRUEFLAUF: '1' }), stdio: 'ignore' });
  /* Aufräumen auch bei Abbruch: keine Prüfserver und Wegwerf-Kopien bleiben liegen */
  const weg = () => { try { srv.kill('SIGKILL'); } catch (e) {} try { fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true }); } catch (e) {} };
  process.on('exit', weg); process.on('SIGINT', () => process.exit(130)); process.on('SIGTERM', () => process.exit(143)); process.on('unhandledRejection', e => { console.log('FEHLT  Lauf ohne Abbruch  → ' + (e && e.stack || e)); process.exit(1); });
  for (let i = 0; i < 80; i++) { try { if ((await fetch(B + '/_werkzeuge/bureau/')).ok) break; } catch (e) {} await warte(250); }
  const br = await pw.chromium.launch({ headless: true });
  const ctx = await br.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-schloessli-bureau', '1'); } catch (e) {} });
  const p = await ctx.newPage();
  const geh = async a => { await p.goto(B + '/_werkzeuge/bureau/?ansicht=' + encodeURIComponent(a), { waitUntil: 'load' }); await p.waitForSelector('#ws-mitte[data-ws-bereit]', { timeout: 30000 }); await warte(1600); };
  const bild = async n => { const f = path.join(DATEN, n + '.png'); await p.screenshot({ path: f }); return f; };
  const fertig = [];
  await geh('start'); fertig.push(['uebersicht', await bild('uebersicht')]);
  await geh('e:termine'); await p.locator('[data-cu-termin="f2"] input[name="grund"]').fill('Winterferien'); await p.locator('#ws-speichern').click(); await warte(1500);
  await geh('e:termine'); await p.evaluate(() => window.scrollTo(0, 400)); await warte(900); fertig.push(['termine', await bild('termine')]);
  await geh('b:start'); await warte(1500); await p.waitForFunction(() => !document.body.innerText.includes('Seite wird gesetzt'), null, { timeout: 20000 }).catch(() => {}); await warte(1200); fertig.push(['bereich', await bild('bereich')]);
  await geh('haus:team'); const ein = p.locator('details.ws-eintrag').nth(1); await ein.locator('summary').click(); await warte(500);
  await ein.locator('button.ws-foto').first().click({ force: true }); await p.waitForSelector('[data-ws-fenster="bild"]'); await warte(1500); fertig.push(['foto', await bild('foto')]);
  await geh('angaben'); fertig.push(['angaben', await bild('angaben')]);
  await geh('google'); await p.locator('[data-ws-seo="abend.html"] [data-ws-gt="titel"]').fill('Ihr Abend am Tisch · Wirtschaft am Schlössli Bottighofen'); await p.locator('#ws-speichern').click(); await warte(1500);
  await geh('google'); await p.locator('[data-ws-seo="abend.html"]').scrollIntoViewIfNeeded(); await warte(800); fertig.push(['google', await bild('google')]);
  await geh('entwurf'); fertig.push(['entwurf', await bild('entwurf')]);
  await geh('verlauf'); fertig.push(['verlauf', await bild('verlauf')]);
  await br.close(); srv.kill();
  fs.mkdirSync(ZIEL, { recursive: true });
  execFileSync('python3', ['-c', 'import sys\nfrom PIL import Image\nfor a,b in zip(sys.argv[1::2],sys.argv[2::2]): Image.open(a).convert("RGB").save(b,"WEBP",quality=82)', ...fertig.flatMap(([n, f]) => [f, path.join(ZIEL, n + '.webp')])]);
  console.log('Anleitung: ' + fertig.length + ' Bilder in ' + ZIEL);
})();
