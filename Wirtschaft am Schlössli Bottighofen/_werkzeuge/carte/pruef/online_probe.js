// Die Tafel (La Carte) · Berghotel Gasterntal · Probe der Online-Fassung auf dem Rechner (17.10.2026, aus La Carte des Carlton-Europe), ohne Vercel und ohne Hochladen:
//   node _werkzeuge/carte/pruef/online_probe.js [chromium|webkit]
// Baut aus _werkzeuge/carte/online.json einen Online-Ordner im Temp-Ordner (Funktionen, lib, statik, gemeinsame Speicher-Schicht aus _werkzeuge/online/api),
// «Blob» als Ordner (BLOB_LOKAL, wie werkzeuge_online.py probe), startet die Python-Funktion api/carte.py (freier Port vom Betriebssystem) und einen
// Vorschalt-Server :8971, der die Umleitungen aus online.json nachstellt und api/carte_druck.js wie Vercel aufruft. Dann wird La Carte bedient
// wie online: ändern, speichern, neu laden, Probe-PDF, veröffentlichen, PDF gegen die Änderung, Verlauf, zurückholen, Konflikt zweier Fenster,
// Herkunft, Grösse, Rollen. Alles mit Wegwerf-Daten; danach wird der Temp-Ordner gelöscht.
const path = require('path'), fs = require('fs'), os = require('os'), cp = require('child_process'), http = require('http');
const PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const HIER = path.join(__dirname, '..'), PROJ = path.join(HIER, '..', '..');
const BROWSER = process.argv[2] || 'chromium';
const PORT = +(process.env.LAUF_PORT || 8971), BASIS = `http://127.0.0.1:${PORT}`;   // Vorschalt-Server auf dem Port der Tafel (8971)
let PY = 0;   // die Python-Funktion bekommt einen freien Port vom Betriebssystem (nie den eines anderen Werkzeugs)
const Z = fs.mkdtempSync(path.join(os.tmpdir(), 'carte-online-'));
let rot = 0, nr = 0;
const ok = (n, b, mehr = '') => { nr++; if (!b) rot++; console.log(`${b ? 'ok    ' : 'FEHLER'} ${n}${mehr ? ' · ' + mehr : ''}`); return b; };
const warte = ms => new Promise(r => setTimeout(r, ms));

function kopiere(q, z) {
  const st = fs.statSync(q);
  if (st.isDirectory()) { for (const f of fs.readdirSync(q)) kopiere(path.join(q, f), path.join(z, f)); return; }
  fs.mkdirSync(path.dirname(z), { recursive: true }); fs.copyFileSync(q, z);
}
// ---------------------------------------------------------------- Online-Ordner wie werkzeuge_online.py stell (nur La Carte)
const A = JSON.parse(fs.readFileSync(path.join(HIER, 'online.json'), 'utf8'));
// gemeinsame Speicher-Schicht: im Haus (_werkzeuge/online/api, legt der Werkbank-Chat an), sonst die des Carlton (nur gelesen, gleiche Schicht)
const SPQ = fs.existsSync(path.join(PROJ, '_werkzeuge/online/api/_speicher.py')) ? path.join(PROJ, '_werkzeuge/online/api') : path.join(PROJ, '..', 'Carlton-Europe Interlaken', '_werkzeuge/online/api');
for (const f of ['_speicher.py', '_speicher.cjs']) kopiere(path.join(SPQ, f), path.join(Z, 'api', f));
for (const [ziel, f] of Object.entries(A.funktionen)) kopiere(path.join(PROJ, f.von), path.join(Z, ziel));
for (const [q, z] of Object.entries(A.lib)) kopiere(path.join(PROJ, q), path.join(Z, z));
for (const [q, z] of Object.entries(A.statik)) kopiere(path.join(PROJ, q), path.join(Z, z));
fs.mkdirSync(path.join(Z, 'blob'), { recursive: true });
const ENV = { ...process.env, BLOB_LOKAL: path.join(Z, 'blob'), WERKZEUG_TMP: path.join(Z, '_tmp'), BLOB_READ_WRITE_TOKEN: '', VERCEL: '' };
for (const k of ['BLOB_READ_WRITE_TOKEN', 'BLOB_PUBLIC_READ_WRITE_TOKEN', 'VERCEL', 'VERCEL_ENV']) delete ENV[k];
Object.assign(process.env, { BLOB_LOKAL: ENV.BLOB_LOKAL }); delete process.env.BLOB_READ_WRITE_TOKEN; delete process.env.VERCEL;
const druck = require(path.join(Z, 'api', 'carte_druck.js'));

// ---------------------------------------------------------------- Python-Funktion und Vorschalt-Server (Umleitungen wie vercel.json)
const pyCode = `import importlib.util, sys\nfrom http.server import ThreadingHTTPServer\nspec = importlib.util.spec_from_file_location('carte_fn', sys.argv[1])\nm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\nsrv = ThreadingHTTPServer(('127.0.0.1', 0), m.handler)\nprint(srv.server_address[1], flush=True)\nsrv.serve_forever()\n`;
const py = cp.spawn(process.env.CARTE_PY || 'python3',   // braucht PyMuPDF wie online (requirements.txt); auf dem Rechner z. B. eine venv
  ['-c', pyCode, path.join(Z, 'api', 'carte.py')], { env: ENV, stdio: ['ignore', 'pipe', 'pipe'] });
py.stdout.on('data', d => { const n = parseInt(String(d), 10); if (!PY && n) PY = n; });
let pyFehler = ''; py.stderr.on('data', d => { pyFehler += d; });
const TYP = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.ttf': 'font/ttf', '.woff2': 'font/woff2', '.pdf': 'application/pdf', '.ico': 'image/x-icon', '.png': 'image/png' };
function statisch(res, p) {
  if (!fs.existsSync(p) || !fs.statSync(p).isFile()) { res.writeHead(404, { 'content-type': 'text/plain' }); return res.end('nicht da'); }
  res.writeHead(200, { 'content-type': TYP[path.extname(p)] || 'application/octet-stream', 'cache-control': 'no-store' }); fs.createReadStream(p).pipe(res);
}
const srv = http.createServer((req, res) => {
  const u = new URL(req.url, BASIS);
  if (u.pathname.startsWith('/_werkzeuge/carte/api/')) {   // → /api/carte?__weg=…
    const ziel = '/api/carte?__weg=' + encodeURIComponent(u.pathname) + (u.search ? '&' + u.search.slice(1) : '');
    const v = http.request({ host: '127.0.0.1', port: PY, path: ziel, method: req.method, headers: { ...req.headers, host: `127.0.0.1:${PORT}`, 'x-forwarded-proto': 'http' } }, r => { res.writeHead(r.statusCode, r.headers); r.pipe(res); });
    v.on('error', e => { if (!res.headersSent) { res.writeHead(502); res.end(String(e)); } });
    const teile = []; req.on('data', d => teile.push(d)); req.on('end', () => v.end(Buffer.concat(teile)));   // wie Vercel: ganze Anfrage, dann die Funktion
    return;
  }
  if (u.pathname === '/api/carte_druck') {   // Vercel-Node-Funktion
    let roh = ''; req.on('data', d => { roh += d; }); req.on('end', async () => {
      const r = { _s: 200, status(s) { this._s = s; return this; }, setHeader() {}, json(o) { res.writeHead(this._s, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); } };
      try { await druck({ method: req.method, headers: { ...req.headers, 'x-forwarded-proto': 'http' }, body: roh, query: {} }, r); } /* Vercel setzt x-forwarded-proto bei jeder Anfrage */ catch (e) { res.writeHead(500); res.end(String(e)); }
    }); return;
  }
  if (u.pathname === '/_werkzeuge/carte' || u.pathname === '/_werkzeuge/carte/') return statisch(res, path.join(Z, 'werkzeuge/carte/index.html'));
  if (u.pathname.startsWith('/_werkzeuge/carte/')) return statisch(res, path.join(Z, 'werkzeuge/carte', decodeURIComponent(u.pathname.slice(18))));
  const imOrdner = path.join(Z, decodeURIComponent(u.pathname));
  if (fs.existsSync(imOrdner)) return statisch(res, imOrdner);
  if (/^\/(assets\/(img|fonts|logo)|unterlagen\/pdf)\//.test(u.pathname)) return statisch(res, path.join(PROJ, decodeURIComponent(u.pathname)));   // gibt es online in der Website
  res.writeHead(404); res.end('nicht da');
});

(async () => {
  srv.listen(PORT);
  for (let i = 0; i < 60; i++) { try { const r = await fetch(BASIS + '/_werkzeuge/carte/api/status'); if (r.status < 500) break; } catch (e) { /* noch nicht */ } await warte(200); }
  const B = PW[BROWSER], br = await B.launch();
  const fehler = [];
  const neu = async (rolle = 'direktion', wer = 'Probe Online') => {
    const c = await br.newContext({ viewport: { width: 1440, height: 900 } });
    await c.addInitScript(([w, r]) => { localStorage.setItem('lc-wer', w); localStorage.setItem('lc-rolle', r); }, [wer, rolle]);
    const p = await c.newPage();
    p.on('pageerror', e => fehler.push('Skript: ' + String(e).slice(0, 160)));
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) fehler.push('Konsole: ' + m.text().slice(0, 160)); });
    p.on('response', r => { if (r.status() >= 400 && !/api\/(pdf|entwurf|einstellungen|veroeffentlichen)/.test(r.url())) fehler.push(r.status() + ' ' + r.url().replace(BASIS, '')); });
    return p;
  };
  const gesetzt = async p => { await p.waitForFunction(() => /Seite/.test(document.querySelector('#v-zahl')?.textContent || ''), null, { timeout: 30000 }); await warte(500); };
  try {
    const s0 = await (await fetch(BASIS + '/_werkzeuge/carte/api/status')).json();
    ok('Online-Funktion antwortet, die Karte des Hauses, «online» gesetzt', s0.karten && s0.karten.length === 1 && s0.online === true, (s0.karten || []).map(k => k.ziel).join(', ') + ' · online=' + s0.online);
    const p = await neu();
    await p.goto(BASIS + '/_werkzeuge/carte/#karte-2026', { waitUntil: 'load' }); await gesetzt(p);
    ok('Oberfläche lädt unter /_werkzeuge/carte/ (Umleitung), Rahmen aus /assets/oberflaeche/', /Karte 2026/.test(await p.textContent('.wo-kopf__mitte')) && await p.evaluate(() => document.documentElement.dataset.woHaus === 'gasterntal' && !!window.WO));
    const reihe = p.locator('.r', { hasText: 'Tomatesalat' }).first();
    await reihe.hover(); await reihe.locator('[data-akt="edit"]').click(); await warte(400);
    await p.fill('#fenster .felder .feld:has(> span:text-is("Preis")) input', '33.75');
    await p.click('#f-ok'); await p.waitForFunction(() => /gespeichert/.test(document.getElementById('meldung').textContent), null, { timeout: 30000 }).catch(() => {}); await warte(500);
    let k = await (await fetch(BASIS + '/_werkzeuge/carte/api/karte?z=karte-2026')).json();
    ok('Speichern legt den Entwurf in die Ablage (Blob)', !!k.entwurf && JSON.stringify(k.entwurf).includes('33.75') && fs.existsSync(path.join(Z, 'blob/private/ablage/carte.json.gz')));
    await p.reload({ waitUntil: 'load' }); await gesetzt(p);
    ok('Neu laden: Entwurf noch da', /Entwurf/.test(await p.textContent('.wo-leiste__t b')));
    // Probe
    const pr = await p.evaluate(async () => { const r = await fetch('/_werkzeuge/carte/api/probe', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Carte-Rolle': 'direktion', 'X-Carte-Wer': 'Probe' }, body: JSON.stringify({ z: 'karte-2026' }) }); return { s: r.status, j: await r.json() }; });
    ok('Probe-PDF über die Druck-Funktion', pr.s === 200 && pr.j.seiten === 2, JSON.stringify(pr.j).slice(0, 160));
    const prPdf = await fetch(BASIS + (pr.j.url || '')); const prB = Buffer.from(await prPdf.arrayBuffer());
    ok('Probe-PDF abrufbar (aus dem Blob)', prPdf.status === 200 && prB.slice(0, 4).toString() === '%PDF', prPdf.status + ' · ' + prB.length + ' Bytes');
    // Veröffentlichen über die Oberfläche
    await p.click('[data-akt="veroeffentlichen"]'); await warte(800);
    const okK = p.locator('#v-ok'); if (await okK.count()) await okK.click();
    await p.waitForSelector('#fenster:not([hidden]) h2:has-text("Veröffentlicht"), .quit.fehl', { timeout: 240000 });
    const titel = await p.textContent('#fenster h2').catch(() => '');
    ok('Veröffentlichen online: «Veröffentlicht.»', /Veröffentlicht/.test(titel || ''), ((await p.textContent('#fenster .satz').catch(() => '')) + ' // ' + (await p.textContent('#meldung').catch(() => '')) + ' // ' + JSON.stringify((await (await fetch(BASIS + '/_werkzeuge/carte/api/status')).json()).bau)).slice(0, 600));
    const live = await fetch(BASIS + '/_werkzeuge/carte/api/pdf?z=karte-2026&q=live'); const liveB = Buffer.from(await live.arrayBuffer());
    fs.writeFileSync(path.join(Z, 'live.pdf'), liveB);
    const txt = cp.execFileSync('pdftotext', [path.join(Z, 'live.pdf'), '-']).toString();
    ok('Veröffentlichte PDF aus dem Speicher enthält 33.75', live.status === 200 && txt.includes('33.75'));
    const s1 = await (await fetch(BASIS + '/_werkzeuge/carte/api/status')).json();
    const sp = s1.karten.find(x => x.ziel === 'karte-2026');
    ok('Status: kein Entwurf mehr, PDF-Zeit gesetzt (für La Maison)', !sp.entwurf && /\d\d\.\d\d\.\d{4}/.test(sp.pdf_zeit), JSON.stringify({ entwurf: sp.entwurf, pdf_zeit: sp.pdf_zeit }));
    const vl = await (await fetch(BASIS + '/_werkzeuge/carte/api/verlauf?z=karte-2026')).json();
    ok('Verlauf hat die vorige Fassung', vl.liste.length >= 1);
    // Zurückholen (Ursprung) und noch einmal veröffentlichen = wieder wie vorher
    const zh = await p.evaluate(async () => { const r = await fetch('/_werkzeuge/carte/api/zurueckholen', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Carte-Rolle': 'direktion', 'X-Carte-Wer': 'Probe' }, body: JSON.stringify({ z: 'karte-2026', datei: 'grundstand' }) }); return r.status; });
    const pub2 = await p.evaluate(async () => { const r = await fetch('/_werkzeuge/carte/api/veroeffentlichen', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Carte-Rolle': 'direktion', 'X-Carte-Wer': 'Probe' }, body: JSON.stringify({ z: 'karte-2026' }) }); return r.json(); });
    const live2 = Buffer.from(await (await fetch(BASIS + '/_werkzeuge/carte/api/pdf?z=karte-2026&q=live')).arrayBuffer()); fs.writeFileSync(path.join(Z, 'live2.pdf'), live2);
    const txt2 = cp.execFileSync('pdftotext', [path.join(Z, 'live2.pdf'), '-']).toString();
    ok('Zurückholen und veröffentlichen: Tomatesalat wieder 11.00, 33.75 weg', zh === 200 && pub2.fertig && /Tomatesalat/.test(txt2) && txt2.includes('11.00') && !txt2.includes('33.75'), JSON.stringify(pub2).slice(0, 120));
    const vpdf = fs.readdirSync(path.join(Z, 'blob/private/carte/pdf/verlauf/karte-2026')).filter(x => x.endsWith('.pdf'));
    ok('Vorige PDF liegt im Verlauf (Blob)', vpdf.length >= 1, vpdf.join(', '));
    // Zwei Fenster: der zweite bekommt Konflikt, nichts überschrieben
    const p2 = await neu('service', 'Zweites Fenster');
    await p2.goto(BASIS + '/_werkzeuge/carte/#karte-2026', { waitUntil: 'load' }); await gesetzt(p2);
    await p.goto(BASIS + '/_werkzeuge/carte/#karte-2026', { waitUntil: 'load' }); await gesetzt(p);
    const lies = pg => pg.evaluate(async () => { const k = await (await fetch('/_werkzeuge/carte/api/karte?z=karte-2026')).json(); const d = k.entwurf || k.stand; return { d, t: k.entwurf_zeit || d.veroeffentlicht }; });
    const schreib = (pg, x, w, rolle) => pg.evaluate(async ([x, w, rolle]) => { const s = JSON.stringify(x.d).replace('"Hobelchäs"', '"' + w + ' Hobelchäs"'); const r = await fetch('/_werkzeuge/carte/api/entwurf', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Carte-Rolle': rolle, 'X-Carte-Wer': w }, body: JSON.stringify({ z: 'karte-2026', daten: JSON.parse(s), was: w, erwartet: x.t || '' /* wie carte.js */ }) }); return { s: r.status, j: await r.json() }; }, [x, w, rolle]);
    const x1 = await lies(p), x2 = await lies(p2);
    const a1 = await schreib(p, x1, 'Erst', 'direktion'), a2 = await schreib(p2, x2, 'Zweit', 'service');
    const nachher = await lies(p);
    ok('Zwei Fenster: erstes speichert, zweites mit altem Stand bekommt 409 KONFLIKT, nichts überschrieben', a1.s === 200 && a2.s === 409 && a2.j.stichwort === 'KONFLIKT' && JSON.stringify(nachher.d).includes('Erst Hobelchäs') && !JSON.stringify(nachher.d).includes('Zweit'), `${a1.s} / ${a2.s} ${a2.j.stichwort || ''}`);
    // Herkunft, Form, Grösse, Rolle
    const post = (weg, body, kopf = {}) => fetch(BASIS + '/_werkzeuge/carte/api/' + weg, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Carte-Rolle': 'direktion', ...kopf }, body });
    ok('Fremde Herkunft: 403', (await post('entwurf', '{}', { Origin: 'https://boese.example' })).status === 403);
    ok('Nur JSON: 415', (await fetch(BASIS + '/_werkzeuge/carte/api/entwurf', { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: 'x' })).status === 415);
    { let st = 0; try { st = (await post('entwurf', 'x'.repeat(3100000))).status; } catch (e) { st = 'abgebrochen: ' + e.message; } ok('Zu gross: 413', st === 413, String(st)); }
    ok('Service darf nicht veröffentlichen: 403', (await post('veroeffentlichen', JSON.stringify({ z: 'karte-2026' }), { 'X-Carte-Rolle': 'service' })).status === 403);
    ok('Programmcode wird abgewiesen: 400', (await post('entwurf', JSON.stringify({ z: 'karte-2026', daten: { seiten: [{ fn: 'blatt', a: [[{ fn: 'p', a: ['<script>alert(1)</script>'] }]] }] } }))).status === 400);
    ok('Anschluss an die Website online gesperrt (ONLINE)', (await (await post('einstellungen', JSON.stringify({ anschluss_pdf: true }))).json()).stichwort === 'ONLINE');
    const dr = await fetch(BASIS + '/api/carte_druck', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ z: 'karte-2026', daten: {} }) });
    ok('Druck-Funktion ohne Schlüssel: 403', dr.status === 403);
    const pru = await (await fetch(BASIS + '/_werkzeuge/carte/api/pruefung')).json();
    ok('Prüfung online: Speicher, Druck, Prüfung der PDF in Ordnung', pru.werkzeug && pru.werkzeug.druck && pru.werkzeug.pdfpruefung, JSON.stringify(pru.werkzeug));
    await p.goto(BASIS + '/_werkzeuge/carte/pruefung.html', { waitUntil: 'load' }); await warte(1500);
    ok('Prüfseite online', /online/.test(await p.textContent('#p-server')));
    ok('Keine Skriptfehler', fehler.length === 0, fehler.slice(0, 3).join(' | '));
  } catch (e) { ok('Ablauf', false, String(e && e.stack || e).slice(0, 400)); }
  if (pyFehler.trim()) console.log('Python:', pyFehler.slice(-800));
  await br.close(); srv.close(); py.kill(); fs.rmSync(Z, { recursive: true, force: true });
  console.log(`\nOnline-Probe ${BROWSER}: ${nr - rot} von ${nr} grün${rot ? ', ' + rot + ' ROT' : ''}`);
  process.exit(rot ? 1 : 0);
})();
