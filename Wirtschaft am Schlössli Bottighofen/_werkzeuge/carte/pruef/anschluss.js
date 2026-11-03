// Die Tafel (La Carte) · Berghotel Gasterntal — Anschluss an die Website (C11, C18, C20–C22) an einer APFS-Kopie des Projekts (17.10.2026, nach
// der Probe der Tafel des Ruedihus). Das Projekt, aus dem das Skript läuft, bleibt unberührt.
//   node _werkzeuge/carte/pruef/anschluss.js            (Port 8971, der eigene Server der Tafel muss vorher beendet sein)
// 1 Kopie des Projekts per APFS-Klon (cp -c -R) in einen Temp-Ordner, dort inhalt.py mit anschluss/patch_inhalt.py ergänzt, Daten frisch eingelesen.
//   Bau mit Patch, ohne Veröffentlichung: alle Seiten Byte für Byte wie vorher.
// 2 Die Tafel der Kopie startet auf 8971, Anschluss an (Direktion). Preis des Chäsefondues ändern, neues Gericht in «Gäng guet», Preis der
//   Tagessuppe ändern, veröffentlichen → PDF unter unterlagen/pdf/ und assets/pdf/ der Kopie, essen.html mit neuem Preis und Gericht, die Zeile
//   der Tagessuppe im Wortlaut des Hauses («Tagesssuppe») mit neuem Preis, Startseite mit dem neuen Preis, jede andere Seite Byte für Byte gleich,
//   ein späterer Bau ergibt dieselben Seiten.
// 3 «Beleits Chäsbrot» ausblenden → essen.html und picknick.html ohne die Zeile. 4 Ansicht «Website» mit Entwurf. 5 Seite weicht vom Bau ab → nur
//   der Abschnitt. 6 Ursprung zurückholen und veröffentlichen → Seiten wieder Byte für Byte wie vorher. 7 Ohne Patch: Meldung, PDF trotzdem.
const path = require('path'), fs = require('fs'), os = require('os'), cp = require('child_process'), crypto = require('crypto');
const HIER = path.join(__dirname, '..'), PROJ = path.join(HIER, '..', '..');
const PORT = +(process.env.LAUF_PORT || 8971), BASIS = `http://127.0.0.1:${PORT}`;
let rot = 0, nr = 0;
const ok = (n, b, mehr = '') => { nr++; if (!b) rot++; console.log(`${b ? 'ok    ' : 'FEHLER'} ${n}${mehr ? ' · ' + mehr : ''}`); return b; };
const warte = ms => new Promise(r => setTimeout(r, ms));
const sha = f => fs.existsSync(f) ? crypto.createHash('sha1').update(fs.readFileSync(f)).digest('hex') : '-';
const PDF = ['unterlagen/pdf/karte-2026.pdf', 'assets/pdf/Karte-2026.pdf'];
const abschnitt = h => { const m = /<section\b[^>]*\bid="karte"[^>]*>/.exec(h); if (!m) return null; const i = m.index; let t = 0; const re = /<(\/?)section\b/g; re.lastIndex = i; let x; while ((x = re.exec(h))) { t += x[1] ? -1 : 1; if (!t) { const e = h.indexOf('>', x.index) + 1; return [i, e]; } } return null; };
const bauen = (K, ziel, env = {}) => { fs.mkdirSync(ziel, { recursive: true }); cp.execFileSync('python3', [path.join(K, 'bau.py')], { cwd: K, env: { ...process.env, BG_ZIEL: ziel, PYTHONDONTWRITEBYTECODE: '1', ...env }, stdio: 'ignore' }); return fs.readdirSync(ziel).filter(f => f.endsWith('.html')).sort(); };

(async () => {
  try { cp.execSync(`lsof -tiTCP:${PORT} -sTCP:LISTEN`); console.error(`Port ${PORT} belegt: erst den eigenen Server der Tafel beenden (nie fremde).`); process.exit(3); } catch (e) { /* frei */ }
  const T = fs.mkdtempSync(path.join(os.tmpdir(), 'tafel-anschluss-')), K = path.join(T, 'haus');
  const t0 = Date.now();
  cp.execFileSync('cp', ['-c', '-R', PROJ, K]);
  ok('APFS-Kopie des Projekts', fs.existsSync(path.join(K, 'bau.py')), `${Math.round((Date.now() - t0) / 1000)} s`);
  const SEITEN_ALLE = bauen(K, path.join(T, 'liste'));   // die Seiten, die der Bau des Hauses setzt
  const SEITEN = [...SEITEN_ALLE, 'inhalt.py', ...PDF];
  const echtVor = Object.fromEntries(SEITEN.map(f => [f, sha(path.join(PROJ, f))]));
  const kopieVor = Object.fromEntries(SEITEN.map(f => [f, fs.existsSync(path.join(K, f)) ? fs.readFileSync(path.join(K, f)) : null]));
  const ohnePatch = SEITEN_ALLE.filter(f => !fs.readFileSync(path.join(T, 'liste', f)).equals(kopieVor[f]));
  ok(`Ausgangslage: der Bau des Hauses ergibt heute dieselben ${SEITEN_ALLE.length} Seiten wie im Projekt`, !ohnePatch.length, ohnePatch.join(', '));
  cp.execFileSync('python3', [path.join(K, '_werkzeuge/carte/anschluss/patch_inhalt.py'), K, '--setzen'], { stdio: 'ignore' });
  ok('Patch in inhalt.py der Kopie eingesetzt', fs.readFileSync(path.join(K, 'inhalt.py'), 'utf8').includes('die_tafel_web'));
  const D = path.join(K, '_werkzeuge/carte/_daten');
  fs.rmSync(D, { recursive: true, force: true });
  cp.execFileSync('python3', [path.join(K, '_werkzeuge/carte/einlesen.py')], { stdio: 'ignore' });
  const leer = path.join(T, 'leerbau'); bauen(K, leer);
  const anders0 = SEITEN_ALLE.filter(f => !fs.readFileSync(path.join(leer, f)).equals(kopieVor[f]));
  ok(`Bau mit Patch, noch nichts veröffentlicht: alle ${SEITEN_ALLE.length} Seiten Byte für Byte wie vorher`, !anders0.length, anders0.join(', '));
  const srv = cp.spawn('python3', [path.join(K, '_werkzeuge/carte/serve.py'), String(PORT)], { stdio: 'ignore' });
  for (let i = 0; i < 60; i++) { try { await fetch(BASIS + '/_werkzeuge/carte/api/gesund'); break; } catch (e) { await warte(150); } }
  const H = r => ({ 'X-Carte-Rolle': r, 'X-Carte-Wer': 'Probe%20Anschluss', 'Content-Type': 'application/json', Origin: BASIS });
  const api = async (was, d, r = 'direktion') => { const x = await fetch(`${BASIS}/_werkzeuge/carte/api/${was}`, d === undefined ? { headers: H(r) } : { method: 'POST', headers: H(r), body: JSON.stringify(d) }); return { s: x.status, j: await x.json().catch(() => ({})) }; };
  const fertig = async () => { for (let i = 0; i < 400; i++) { const b = (await api('status')).j.bau; if (!b.laeuft) return b; await warte(700); } return { fehler: 'Zeit' }; };
  const ganz = (x, f) => { if (x && typeof x === 'object') { if (f(x)) return x; for (const v of Object.values(x)) { const r = ganz(v, f); if (r) return r; } } return null; };
  const text = x => typeof x === 'string' ? x : x && x.fn === 'el' ? x.a.slice(2).map(text).join('') : '';
  const eintrag = (d, kl, wort) => ganz(d, x => x.fn === 'el' && new RegExp(`class="${kl}[ "]`).test(x.a[1]) && text(x).includes(wort));
  const preisB = n => ganz(n, x => x.fn === 'el' && x.a[0] === 'b' && /^\d+\.\d\d$/.test(text(x)));
  const lies = f => fs.readFileSync(path.join(K, f), 'utf8');
  const Z = 'karte-2026';
  try {
    ok('Anschluss einschalten (Direktion)', (await api('einstellungen', { anschluss_pdf: true })).j.anschluss_pdf === true);
    ok('Anschluss einschalten im Service: 403', (await api('einstellungen', { anschluss_pdf: false }, 'service')).s === 403);
    // ---- Preis Chäsefondue, neues Gericht, Preis der Tagessuppe
    let d = (await api(`karte?z=${Z}`)).j.stand;
    preisB(eintrag(d, 'po', 'Friburger Chäsefondue')).a[2] = '31.00';
    const tomate = eintrag(d, 'po', 'Tomatefondue');
    const neu = JSON.parse(JSON.stringify(tomate)); delete neu.id;
    ganz(neu, x => x.fn === 'el' && x.a[0] === 'h4').a[2] = 'Prüffondue Tal';
    preisB(neu).a[2] = '21.00';
    const vater = ganz(d, x => x.fn && Array.isArray(x.a) && x.a.includes(tomate)); vater.a.splice(vater.a.indexOf(tomate) + 1, 0, neu);
    preisB(eintrag(d, 'po', 'Tagessuppe')).a[2] = '11.00';
    ok('Entwurf gespeichert', (await api('entwurf', { z: Z, daten: d, was: 'Probe Anschluss' })).s === 200);
    ok('Veröffentlichen gestartet', (await api('veroeffentlichen', { z: Z })).s === 200);
    let b = await fertig();
    ok('Veröffentlicht mit Anschluss: PDF an beide Adressen, Seiten genannt', !b.fehler && /unterlagen\/pdf.*assets\/pdf/.test(b.bericht.anschluss || ''), b.fehler || b.bericht.anschluss);
    const live = fs.readFileSync(path.join(D, `live/${Z}.pdf`));
    ok('unterlagen/pdf/ und assets/pdf/ der Kopie = veröffentlichte PDF (Byte für Byte)', fs.readFileSync(path.join(K, PDF[0])).equals(live) && fs.readFileSync(path.join(K, PDF[1])).equals(live));
    const pdfT = cp.execFileSync('pdftotext', [path.join(K, PDF[1]), '-']).toString();
    ok('PDF der Website (Kopie) = neuer Stand (31.00, Prüffondue, Tagessuppe 11.00)', /31\.00/.test(pdfT) && /Prüffondue Tal/.test(pdfT) && /11\.00/.test(pdfT));
    const es = lies('essen.html'); const sek = es.slice(...abschnitt(es));
    ok('essen.html: Chäsefondue mit neuem Preis', /<b>Friburger Chäsefondue<\/b><em><span><small>pro Person<\/small>31\.00<\/span><\/em>/.test(sek), (sek.match(/<b>Friburger Chäsefondue<\/b><em>.*?<\/em>/) || [''])[0]);
    ok('essen.html: neues Gericht in «Gäng guet» nach dem Tomatefondue', /<b>Tomatefondue<\/b>(?:(?!<\/section>).)*<b>Prüffondue Tal<\/b><em><span><small>pro Person<\/small>21\.00<\/span><\/em>/s.test(sek));
    ok('essen.html: Tagessuppe bleibt im Wortlaut des Hauses («Tagesssuppe»), nur der Preis folgt (11.00)', /<b>Tagesssuppe<\/b><em><span>11\.00<\/span><\/em>/.test(sek), (sek.match(/<b>Tagess+uppe<\/b><em>.*?<\/em>/) || [''])[0]);
    ok('index.html: Bildzeile und Auszug folgen (pro Person 31.00)', /pro Person 31\.00/.test(lies('index.html')) && /<small>pro Person<\/small>31\.00/.test(lies('index.html')));
    const anders1 = SEITEN_ALLE.filter(f => !fs.readFileSync(path.join(K, f)).equals(kopieVor[f]));
    ok('Nur die Seiten mit der Karte sind neu (essen.html, index.html), alle anderen Byte für Byte gleich', anders1.join() === 'essen.html,index.html', anders1.join(', '));
    ok('Sicherung der vorigen Seiten im Verlauf', ['essen.html', 'index.html'].every(s => fs.readdirSync(path.join(D, `verlauf/${Z}`)).some(f => f.startsWith('seite-' + s))));
    ok('Sicherung der vorigen PDFs im Verlauf', fs.readdirSync(path.join(D, `verlauf/${Z}`)).filter(f => /^website-.*\.pdf$/.test(f)).length === 2);
    ok('Zeilen für den Bau abgelegt (_daten/web/karte.json)', fs.existsSync(path.join(D, 'web/karte.json')));
    const spaet = path.join(T, 'spaet'); bauen(K, spaet);
    const anders2 = SEITEN_ALLE.filter(f => !fs.readFileSync(path.join(spaet, f)).equals(fs.readFileSync(path.join(K, f))));
    ok('Späterer Bau der Website ergibt dieselben Seiten (Byte für Byte)', !anders2.length, anders2.join(', '));
    // ---- Öpis chalts: «Beleits Chäsbrot» ausblenden (Picknick)
    d = (await api(`karte?z=${Z}`)).j.stand;
    eintrag(d, 'po', 'Beleits Chäsbrot').aus = true;
    await api('entwurf', { z: Z, daten: d, was: 'Probe ausblenden' }); await api('veroeffentlichen', { z: Z }); b = await fertig();
    const es2 = lies('essen.html'), pk = lies('picknick.html');
    ok('Ausgeblendet: «Beleits Chäsbrot» fehlt auf essen.html und picknick.html, «Beleits Schinkebrot» steht', !/Beleits Chäsbrot/.test(es2.slice(...abschnitt(es2))) && !/Beleits Chäsbrot/.test(pk) && /Beleits Schinkebrot/.test(pk), b.fehler || b.bericht.anschluss);
    // ---- Ansicht Website mit Entwurf
    d = (await api(`karte?z=${Z}`)).j.stand;
    preisB(eintrag(d, 'po', 'Friburger Chäsefondue')).a[2] = '33.00';
    await api('entwurf', { z: Z, daten: d, was: 'Probe Ansicht' });
    const w = await (await fetch(`${BASIS}/_werkzeuge/carte/api/webseite?z=${Z}&seite=essen.html`)).text();
    ok('Ansicht «Website»: Seite «Ässe u trinke» mit dem Entwurf (33.00), gekennzeichnet', /data-carte-entwurf="1"/.test(w) && /<b>Friburger Chäsefondue<\/b><em><span><small>pro Person<\/small>33\.00/.test(w));
    const wp = await (await fetch(`${BASIS}/_werkzeuge/carte/api/webseite?z=${Z}&seite=index.html`)).text();
    ok('Ansicht «Website»: Startseite mit dem Entwurf (33.00)', /data-carte-entwurf="1"/.test(wp) && /pro Person 33\.00/.test(wp));
    ok('Ansicht «Website»: die Seite selbst bleibt beim Ansehen unverändert (31.00)', /<small>pro Person<\/small>31\.00/.test(lies('essen.html')));
    await api('verwerfen', { z: Z });
    // ---- Seite weicht vom Bau ab: nur der Abschnitt, andere Seite gemeldet und nicht angefasst
    fs.appendFileSync(path.join(K, 'index.html'), '\n<!-- Hand-Probe -->'); fs.appendFileSync(path.join(K, 'essen.html'), '\n<!-- Hand-Probe -->');
    const idxHand = lies('index.html');
    d = (await api(`karte?z=${Z}`)).j.stand;
    preisB(eintrag(d, 'po', 'Friburger Chäsefondue')).a[2] = '32.00';
    await api('entwurf', { z: Z, daten: d, was: 'Probe Abweichung' }); await api('veroeffentlichen', { z: Z }); b = await fertig();
    const es3 = lies('essen.html');
    ok('Seite weicht ab: essen.html bekommt nur die Karte (32.00), die Hand-Änderung bleibt', /<small>pro Person<\/small>32\.00/.test(es3.slice(...abschnitt(es3))) && /<!-- Hand-Probe -->/.test(es3) && /nur die Karte/.test(b.bericht.anschluss || ''), b.bericht.anschluss);
    const ix3 = lies('index.html');
    ok('Seite weicht ab: auch index.html bekommt nur ihren Abschnitt «karte» (Auszug und Bildzeilen, 32.00), die Hand-Änderung bleibt, gemeldet', /<!-- Hand-Probe -->/.test(ix3) && /pro Person 32\.00/.test(ix3.slice(...abschnitt(ix3))) && ix3.slice(0, abschnitt(ix3)[0]) === idxHand.slice(0, abschnitt(idxHand)[0]) && /index\.html \(nur die Karte/.test(b.bericht.anschluss || ''));
    fs.writeFileSync(path.join(K, 'index.html'), ix3.replace('\n<!-- Hand-Probe -->', '')); fs.writeFileSync(path.join(K, 'essen.html'), es3.replace('\n<!-- Hand-Probe -->', ''));
    bauen(K, K);   // was die Meldung verlangt: die Website einmal neu bauen (Werkbank), dann steht auch die Startseite auf 32.00
    ok('Nach dem Neubau steht der Preis auch auf der Startseite (32.00)', /pro Person 32\.00/.test(lies('index.html')));
    // ---- Ursprung zurück: Seiten wieder wie vorher
    await api('zurueckholen', { z: Z, datei: 'grundstand' }); await api('veroeffentlichen', { z: Z }); b = await fertig();
    const anders3 = SEITEN_ALLE.filter(f => !fs.readFileSync(path.join(K, f)).equals(kopieVor[f]));
    ok('Ursprünglichen Stand veröffentlicht: alle Seiten Byte für Byte wie vor dem Versuch', !anders3.length, (b.fehler || '') + anders3.join(', '));
    const pdf2 = cp.execFileSync('pdftotext', ['-layout', path.join(K, PDF[0]), '-']).toString();
    const pdf0 = cp.execFileSync('pdftotext', ['-layout', path.join(PROJ, PDF[0]), '-']).toString();
    ok('PDF nach dem Zurückholen: Text Zeichen für Zeichen wie die PDF unter unterlagen/pdf/ des Projekts', pdf2 === pdf0);
    // ---- Ohne Patch: Anschluss meldet es, PDF geht trotzdem
    fs.copyFileSync(path.join(K, 'inhalt.py.vor-die-tafel'), path.join(K, 'inhalt.py'));
    d = (await api(`karte?z=${Z}`)).j.stand;
    preisB(eintrag(d, 'po', 'Linzertorte')).a[2] = '6.80';
    await api('entwurf', { z: Z, daten: d, was: 'ohne Patch' }); await api('veroeffentlichen', { z: Z }); b = await fertig();
    ok('Ohne Patch im Bau: «Seiten: Anschluss im Bau fehlt», PDF trotzdem veröffentlicht, Seiten unverändert', /Anschluss im Bau fehlt/.test(b.bericht.anschluss || '') && /6\.80/.test(cp.execFileSync('pdftotext', [path.join(K, PDF[0]), '-']).toString()) && SEITEN_ALLE.every(f => fs.readFileSync(path.join(K, f)).equals(kopieVor[f])), b.bericht.anschluss);
  } catch (e) { ok('Ablauf', false, String(e && e.stack || e).slice(0, 300)); }
  srv.kill(); await warte(300);
  const echtNach = Object.fromEntries(SEITEN.map(f => [f, sha(path.join(PROJ, f))]));
  ok('Projekt, aus dem geprüft wurde, unberührt (Seiten, PDFs, inhalt.py)', SEITEN.every(f => echtVor[f] === echtNach[f]), SEITEN.filter(f => echtVor[f] !== echtNach[f]).join(', '));
  fs.rmSync(T, { recursive: true, force: true });
  console.log(`\nAnschluss an der Kopie: ${nr - rot} von ${nr} grün`);
  process.exit(rot ? 1 : 0);
})();
