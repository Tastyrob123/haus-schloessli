// NOCH AUF DEN AUFBAU DES GASTERNTAL GESCHRIEBEN, im Schlössli nicht gelaufen (offen, STAND.md). Das Besucherbuch · Berghotel Gasterntal: Probe der Online-Fassung auf dem Rechner (17.10.2026), ohne Vercel und ohne Hochladen.
//   node _werkzeuge/registre/_pruefung/online_probe.js [chromium|webkit|firefox]
// Kopie der Online-Probe des Waldhotel Doldenhorn (dort nach Carlton _werkzeuge/carte/pruef/online_probe.js). Baut aus online.json einen Online-Ordner im Temp-Ordner (Funktion, lib, statik,
// Speicher-Schicht api/_speicher.py als Kopie aus Carlton _werkzeuge/online/api, nur gelesen), legt die Website-Teile, die das Werkzeug braucht
// (assets/fonts, assets/img), daneben und startet EINEN Server auf Port 8988: /api/registre geht an die Vercel-Funktion
// (handler aus api/registre.py, wie Vercel sie aufruft), alles andere statisch, mit der Sicherheitsregel (CSP) der Gasterntal-Website
// (~/maeder-online/berghotel-gasterntal-entwurf/vercel.json, ohne upgrade-insecure-requests, weil die Probe über http läuft).
// Die Oberfläche der Häuser (statik assets/oberflaeche) kommt aus dem Haus, solange sie dort fehlt aus _Werkzeuge/stamm/oberflaeche/ (nur gelesen).
// Geprüft wird wie online: Werkzeug lädt unter /werkzeuge/registre/ ohne Regelverletzung, Beispielwerte gleich wie der Dienst, Schlüssel ohne eigenen Speicher
// gibt nur Beispielwerte, Zählen nur von der eigenen Herkunft, Grösse 413, Menge 429, Ausfuhr nur mit Schlüssel, keine Fehlerspur, Schreiben nur nach
// /tmp/schloessli-bottighofen-registre-demo (danach gelöscht). Wegwerf-Daten, am echten Gasterntal nichts geändert. Ein anderer Server auf 8988 muss aus sein.
const path = require('path'), fs = require('fs'), os = require('os'), cp = require('child_process');
const PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const HIER = path.join(__dirname, '..'), PROJ = path.join(HIER, '..', '..');
const SPEICHER = path.join(process.env.HOME, 'Desktop/Website-Projekte/Carlton-Europe Interlaken/_werkzeuge/online/api/_speicher.py');
const BROWSER = process.argv[2] || 'chromium';
const PORT = 8988, BASIS = `http://localhost:${PORT}`;
const KEY = fs.readFileSync(path.join(process.env.HOME, 'Desktop/Website-Projekte/_Schluessel/schloessli-bottighofen.txt'), 'utf8').trim();
const CSP = "default-src 'self'; script-src 'self' 'sha256-eMjwBA8qHZK8ECdeB4hRHDeILcFBfQRNBqj5Qq/Id+w=' 'sha256-yOksYW1j5Os82N10X6Kyo2fEyOk/UjxLs1rzJ+uBa0U='; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src https://tasty-besuche.vercel.app 'self' blob:; media-src 'self' blob:; frame-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self' mailto:; object-src 'none'";
const Z = fs.mkdtempSync(path.join(os.tmpdir(), 'registre-online-'));
let rot = 0, nr = 0;
const ok = (n, b, mehr = '') => { nr++; if (!b) rot++; console.log(`${b ? 'ok    ' : 'FEHLER'} ${n}${mehr ? ' · ' + mehr : ''}`); return b; };
const warte = ms => new Promise(r => setTimeout(r, ms));
function kopiere(q, z) {
  const st = fs.statSync(q);
  if (st.isDirectory()) { for (const f of fs.readdirSync(q)) kopiere(path.join(q, f), path.join(z, f)); return; }
  fs.mkdirSync(path.dirname(z), { recursive: true }); fs.copyFileSync(q, z);
}
const A = JSON.parse(fs.readFileSync(path.join(HIER, 'online.json'), 'utf8'));
kopiere(SPEICHER, path.join(Z, 'api', '_speicher.py'));
for (const [ziel, f] of Object.entries(A.funktionen)) kopiere(path.join(PROJ, f.von), path.join(Z, ziel));
for (const [q, z] of Object.entries(A.lib)) kopiere(path.join(PROJ, q), path.join(Z, z));
const STAMM_OF = path.join(process.env.HOME, 'Desktop/Website-Projekte/_Werkzeuge/stamm/oberflaeche');
for (const [q, z] of Object.entries(A.statik)) kopiere(q === 'assets/oberflaeche' && !fs.existsSync(path.join(PROJ, q)) ? STAMM_OF : path.join(PROJ, q), path.join(Z, z));
for (const d of ['assets/fonts']) kopiere(path.join(PROJ, d), path.join(Z, d));
for (const f of fs.readdirSync(path.join(PROJ, 'assets/img')).filter(f => /^(haus-profil|haus-eingang|wegweiser|stube|d-bilder|tal-blick|z-doppel|haus-alt)-l\.webp$/.test(f))) kopiere(path.join(PROJ, 'assets/img', f), path.join(Z, 'assets/img', f));
const DEMO = '/tmp/schloessli-bottighofen-registre-demo';
fs.rmSync(DEMO, { recursive: true, force: true });
const pyCode = `
import importlib.util, os, sys, mimetypes, urllib.parse
from http.server import ThreadingHTTPServer
Z = sys.argv[1]
sys.path.insert(0, os.path.join(Z, 'api'))
spec = importlib.util.spec_from_file_location('registre_fn', os.path.join(Z, 'api', 'registre.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
CSP = sys.argv[2]
class H(m.handler):
    def _statisch(self):
        u = urllib.parse.urlsplit(self.path).path
        if u in ('/werkzeuge/registre', '/werkzeuge/registre/'): u = '/werkzeuge/registre/index.html'
        p = os.path.normpath(os.path.join(Z, u.lstrip('/')))
        if not p.startswith(Z) or not os.path.isfile(p) or '/api/' in u:
            self.send_response(404); self.end_headers(); return
        b = open(p, 'rb').read()
        self.send_response(200); self.send_header('Content-Type', (mimetypes.guess_type(p)[0] or 'application/octet-stream') + ('; charset=utf-8' if p.endswith(('.html', '.js', '.css', '.json')) else ''))
        self.send_header('Content-Security-Policy', CSP); self.send_header('X-Frame-Options', 'SAMEORIGIN'); self.send_header('Cache-Control', 'no-store'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path.startswith('/api/registre'): return super().do_GET()
        return self._statisch()
    def do_POST(self):
        if self.path.startswith('/api/registre'): return super().do_POST()
        self.send_response(404); self.end_headers()
ThreadingHTTPServer.request_queue_size = 256   # 130 Meldungen auf einmal: die Vorgabe 5 wies unter Last Verbindungen ab (Vercel nimmt sie alle an)
ThreadingHTTPServer(('127.0.0.1', ${PORT}), H).serve_forever()
`;
const ENV = { ...process.env };
for (const k of ['BLOB_READ_WRITE_TOKEN', 'BLOB_PUBLIC_READ_WRITE_TOKEN', 'REGISTRE_READ_WRITE_TOKEN', 'VERCEL', 'VERCEL_ENV']) delete ENV[k];
const py = cp.spawn('/opt/homebrew/bin/python3', ['-c', pyCode, Z, CSP], { env: ENV, stdio: ['ignore', 'ignore', 'pipe'] });
let pyFehler = ''; py.stderr.on('data', d => { pyFehler += d; });
async function hol(u, o) { const r = await fetch(BASIS + u, o); let j = null; try { j = await r.clone().json(); } catch (e) {} return { s: r.status, j, t: j ? '' : await r.text() }; }

(async () => {
  let b;
  try {
    for (let i = 0; i < 40; i++) { try { await fetch(BASIS + '/werkzeuge/registre/'); break; } catch (e) { await warte(150); } }
    // Dienst wie online
    const bsp = await hol('/api/registre?tage=30&beispiel=1');
    ok('Beispielwerte des Dienstes', bsp.s === 200 && bsp.j.beispiel === true && bsp.j.summe.besuche > 100, JSON.stringify(bsp.j && bsp.j.summe));
    const mitK = await hol('/api/registre?tage=30&k=' + KEY);
    ok('Schlüssel ohne eigenen Speicher: nur Beispielwerte (echte Werte erst mit REGISTRE_READ_WRITE_TOKEN)', mitK.s === 200 && mitK.j.beispiel === true);
    ok('Ausfuhr ohne Schlüssel 403', (await hol('/api/registre?export=1&tage=30')).s === 403);
    ok('Ausfuhr mit Schlüssel, aber ohne eigenen Speicher 403', (await hol('/api/registre?export=1&tage=30&k=' + KEY)).s === 403);
    const fremd = await hol('/api/registre', { method: 'POST', body: 'r1 abcd index.html de rechner 5 - -', headers: { Origin: 'https://boese.example', 'User-Agent': 'Mozilla/5.0 Safari' } });
    ok('fremde Herkunft 403', fremd.s === 403, String(fremd.s));
    const eigen = await hol('/api/registre', { method: 'POST', body: 'r1 abcd index.html de rechner 5 fenster,buchung -', headers: { Origin: BASIS, 'User-Agent': 'Mozilla/5.0 Safari' } });
    ok('eigene Herkunft 204', eigen.s === 204, String(eigen.s));
    ok('Zeile über 300 Zeichen 413', (await hol('/api/registre', { method: 'POST', body: 'r1 ' + 'x'.repeat(400), headers: { 'User-Agent': 'Mozilla/5.0 Safari' } })).s === 413);
    const viele = await Promise.all(Array.from({ length: 130 }, () => fetch(BASIS + '/api/registre', { method: 'POST', body: 'r1 zz00 index.html de rechner 0 - -', headers: { 'User-Agent': 'Mozilla/5.0 Safari' } }).then(r => r.status)));
    ok('mehr als 120 Meldungen je Minute 429', viele.filter(x => x === 429).length >= 9, viele.filter(x => x === 429).length + '× 429');
    const kaputt = await hol('/api/registre?tage=abc');
    ok('keine Fehlerspur in Antworten', !/Traceback|File "|line \d+/.test(JSON.stringify(kaputt.j || kaputt.t)), String(kaputt.s));
    ok('Schreiben nur in den eigenen Vorführ-Ordner (/tmp/schloessli-bottighofen-registre-demo)', fs.existsSync(DEMO) && fs.readdirSync(DEMO, { recursive: true }).some(f => /registre/.test(String(f))), fs.existsSync(DEMO) ? fs.readdirSync(DEMO, { recursive: true }).slice(0, 4).join(',') : 'fehlt');
    // Oberfläche wie online
    b = BROWSER === 'webkit' ? await PW.webkit.launch() : BROWSER === 'firefox' ? await PW.firefox.launch() : await PW.chromium.launch();
    const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, acceptDownloads: true }); const p = await ctx.newPage();
    const verstoss = [], fehl = [];
    p.on('console', m => { if (/Content Security Policy|Content-Security-Policy|CSP/i.test(m.text())) verstoss.push(m.text().slice(0, 140)); else if (m.type() === 'error') fehl.push(m.text().slice(0, 140)); });
    p.on('pageerror', e => fehl.push(e.message)); p.on('response', r => { if (r.status() >= 400) fehl.push(r.status() + ' ' + r.url()); });
    await p.goto(BASIS + '/werkzeuge/registre/?gruss=tag#start'); await p.waitForFunction(() => window.BG_REGISTRE === 1 && document.documentElement.classList.contains('auftakt-da'), null, { timeout: 15000 });
    const ui = await p.evaluate(() => S.d.summe);
    ok('Werkzeug lädt unter /werkzeuge/registre/, Zahlen = Dienst (die Stube liest dieselben)', JSON.stringify(ui) === JSON.stringify((await hol('/api/registre?tage=30&beispiel=1')).j.summe), JSON.stringify(ui));
    ok('Startbild mit Aussenfoto, Zeichen des Hauses und Rahmen der Oberfläche laden', await p.evaluate(() => { const i = document.querySelector('.wo-sb__foto img'); return i.complete && i.naturalWidth > 100 && !!document.querySelector('#zeichen path') && !!window.WO && getComputedStyle(document.querySelector('.wo-kopf')).position === 'sticky'; }));
    await p.evaluate(() => { location.hash = 'herkunft'; }); await p.waitForTimeout(500); ok('Bühnenfoto einer Ansicht lädt (Wegweiser)', await p.evaluate(() => { const i = document.querySelector('.wo-sb__foto img'); return /wegweiser/.test(i.src) && i.complete && i.naturalWidth > 100; }));
    for (const v of ['besuche', 'herkunft', 'zeit', 'seiten', 'verlauf', 'buchung', 'zaehlung']) { await p.evaluate(v => { location.hash = v; }, v); await p.waitForTimeout(350); }
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 10000 }), p.click('#l-export')]); ok('Als Tabelle sichern', /\.csv$/.test(dl.suggestedFilename()), dl.suggestedFilename());
    await p.goto(BASIS + '/werkzeuge/registre/anleitung.html'); await p.waitForTimeout(600); await p.locator('.bild').first().click(); await p.waitForTimeout(200);
    ok('Anleitung: Bild gross und Esc', await p.evaluate(() => !document.getElementById('gross').hidden) && (await p.keyboard.press('Escape'), await p.evaluate(() => document.getElementById('gross').hidden)));
    ok('keine Regelverletzung (CSP)', !verstoss.length, verstoss.join(' | '));
    ok('keine Fehler, keine toten Adressen', !fehl.length, fehl.slice(0, 4).join(' | '));
    await ctx.close();
  } catch (e) { ok('Ablauf', false, e.message + (pyFehler ? ' · ' + pyFehler.slice(-300) : '')); }
  if (b) await b.close();
  py.kill(); fs.rmSync(Z, { recursive: true, force: true }); fs.rmSync(DEMO, { recursive: true, force: true });
  console.log(`\nOnline-Probe ${BROWSER}: ${nr - rot} von ${nr} grün`);
  process.exit(rot ? 1 : 0);
})();
