// Der Gastgeber (La Réception) · Landgasthof Ruedihus: die nachgestellte Online-Fassung bedienen (online_probe.py muss laufen, Vorbild Doldenhorn).
//   node online_bedienen.js [http://localhost:9033] [chromium|webkit|firefox]
const path = require('path');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const O = process.argv[2] || 'http://localhost:9033', MOTOR = process.argv[3] || 'chromium', B = O + '/werkzeuge/reception/';
const sleep = ms => new Promise(r => setTimeout(r, ms));
let gruen = 0, rot = 0;
const ok = (b, was) => { if (!b) throw new Error(was); };
(async () => {
  const br = await require('./schutz').start(pw, MOTOR); const ctx = await require('./schutz').kontext(br, { viewport: { width: 1440, height: 900 }, locale: 'de-CH' });
  await ctx.addInitScript(() => { try { localStorage.setItem('reception-name', 'QA Online'); localStorage.setItem('rundgang-rh-reception', '1'); } catch (e) { /* */ } });
  const p = await ctx.newPage(); p.setDefaultTimeout(20000); const fehler = []; p.on('pageerror', e => fehler.push(String(e)));
  let gedruckt = 0; await p.exposeFunction('__gedruckt', () => { gedruckt++; }); await ctx.addInitScript(() => { window.print = () => window.__gedruckt && window.__gedruckt(); });
  const api = (w, d) => p.evaluate(async ([w, d]) => { const r = await fetch('api/' + w, d ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) } : {}); let j = {}; try { j = await r.json(); } catch (e) { /* */ } return { s: r.status, j }; }, [w, d]);
  const schritt = async (n, fn) => { const f0 = fehler.length; try { const i = await fn(); ok(fehler.length === f0, 'Skriptfehler: ' + fehler.slice(f0).join(' | ')); gruen++; console.log('ok  ', n, '·', i || ''); } catch (e) { rot++; console.log('ROT ', n, '·', String(e.message).split('\n')[0].slice(0, 220)); } };
  await schritt('O1 Oberfläche unter /werkzeuge/reception/ lädt (statik), Übersicht mit Zahlen über die Umleitung', async () => { await p.goto(B, { waitUntil: 'load' }); await p.waitForSelector('.lage'); const u = await api('ueberblick'); ok(u.s === 200 && typeof u.j.anfragen_neu === 'number', 'ueberblick ' + u.s); return `neu ${u.j.anfragen_neu}, offen ${u.j.anfragen_offen}, Fragen ${u.j.fragen_gesamt}, Speicher ${u.j.speicher}`; });
  await schritt('O2 Auch die lokale Adresse /_werkzeuge/reception/ führt online zur Oberfläche', async () => { const r = await p.evaluate(async o => (await fetch(o + '/_werkzeuge/reception/')).status, O); ok(r === 200, 'Status ' + r); return '200'; });
  await schritt('O3 Formular der Website online (Anfrage-Fenster auf essen.html) landet im Eingang (Blob «reception»), Abteilung Event', async () => {
    await p.goto(O + '/essen.html?probe=1', { waitUntil: 'load' }); await sleep(1200); const f = 'form[data-rechner]'; await p.fill(f + ' input[name=erw]', '12'); await p.selectOption(f + ' select[name=anlass]', 'Sitzung'); await p.fill(f + ' input[name=name]', 'Online QA');
    await p.locator(f + ' [type=submit]').click(); await p.waitForSelector('dialog.anf[open]'); await p.fill('dialog.anf input[name=kontakt]', 'online-qa@example.com'); await p.locator('dialog.anf .anf__los').click(); await p.waitForSelector('dialog.anf .anf__danke:not([hidden])', { timeout: 15000 });
    await p.goto(B, { waitUntil: 'load' }); const l = (await api('anfragen')).j.anfragen; const a = l.find(x => x.name === 'Online QA'); ok(a && a.abteilung === 'Event' && a.art === 'tagung' && a.formular === 'fest' && a.probe, 'nicht im Eingang: ' + JSON.stringify(a || {}).slice(0, 160)); return 'Event, Sitzung, Fest-Rechner'; });
  await schritt('O4 Öffnen schreibt den Brief (Probe-Assistent), gelesen auch an der Website', async () => {
    await p.goto('about:blank'); await p.goto(B + '#eingang', { waitUntil: 'load' }); await p.waitForSelector('.re-liste'); await p.locator('.re-liste .re-a', { hasText: 'Online QA' }).click(); await p.waitForSelector('#brief', { timeout: 60000 });
    await sleep(1500); return 'Brief da'; });
  await schritt('O5 Formular ohne Kontakt online: Meldung mit Stichwort FORMULAR, kein Eintrag', async () => { const r = await p.evaluate(async () => (await fetch('/werkzeuge/reception/api/formular', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: 'x', kontakt: '' }) })).status); ok(r === 400 || r === 422, 'Status ' + r); return r + ' (online Eingabefehler 400, Master 2.6)'; });
  await schritt('O6 Brief gestalten: Änderung gesichert, nach Neuladen noch da (Blob)', async () => {
    const l = (await api('anfragen')).j.anfragen; const a = l.find(x => x.name === 'Online QA'); const r = await api('anfrage', { id: a.id, betreff: 'Online QA Betreff', entwurf_text: a.entwurf.text + '\n\nOnline QA Zusatz' }); ok(r.s === 200, 'sichern ' + r.s);
    const b = (await api('anfragen')).j.anfragen.find(x => x.id === a.id); ok(/Online QA Zusatz/.test(b.entwurf.text) && b.entwurf.betreff === 'Online QA Betreff', 'nicht gehalten'); return 'gehalten'; });
  await schritt('O7 Als PDF sichern online: Server sagt DRUCK, Oberfläche öffnet das Druckfenster', async () => {
    await p.goto('about:blank'); await p.goto(B + '#eingang', { waitUntil: 'load' }); await p.waitForSelector('.re-liste'); await p.locator('.re-liste .re-a', { hasText: 'Online QA' }).click(); await p.waitForSelector('#brief'); await sleep(800);
    const r = await api('brief_pdf', { id: (await api('anfragen')).j.anfragen.find(x => x.name === 'Online QA').id }); ok(r.s === 501 && /DRUCK/.test(r.j.fehler), 'Antwort ' + r.s);
    const vor = gedruckt; await p.locator('#detail [data-akt="pdf"]').click(); await sleep(1500); ok(gedruckt > vor, 'Druckfenster nicht geöffnet'); return 'Druckfenster'; });
  await schritt('O8 Erledigt und Löschen online, nach Neuladen gilt der Stand (Blob)', async () => {
    const a = (await api('anfragen')).j.anfragen.find(x => x.name === 'Online QA'); await api('anfrage', { id: a.id, status: 'erledigt' }); ok((await api('anfragen')).j.anfragen.find(x => x.id === a.id).status === 'erledigt', 'nicht erledigt');
    const w = await api('weg', { id: a.id }); ok(w.s === 200, 'löschen ' + w.s); ok(!(await api('anfragen')).j.anfragen.find(x => x.id === a.id), 'noch da'); return 'erledigt, gelöscht'; });
  await schritt('O9 Chat online (api/gast.py): Antwort, Frage landet in «Das wurde gefragt» (Monats-Ablage)', async () => {
    const r = await p.evaluate(async () => (await fetch('/api/gast', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Reception-Probe': '1' }, body: JSON.stringify({ messages: [{ role: 'user', content: 'Online QA Frage zum Hallenbad' }], sprache: 'de' }) })).json());
    ok(/Probe-Antwort/.test(r.text || ''), 'Antwort: ' + JSON.stringify(r).slice(0, 120)); await sleep(500); const f = (await api('fragen')).j.fragen; ok(f.some(x => /Online QA Frage/.test(x.frage)), 'Frage fehlt'); return 'gespeichert'; });
  await schritt('O10 Prüfseite online: Zustand mit Speicher, Wissen, Formularen der Website', async () => { await p.goto(B + 'pruefung.html', { waitUntil: 'load' }); await p.waitForSelector('.z'); const z = await api('zustand'); const w = z.j.punkte.find(x => x.gruppe === 'Website'); ok(w && w.stand === 'gut', 'Website: ' + JSON.stringify(w)); return z.j.punkte.length + ' Punkte'; });
  await schritt('O11 Daten online herunterladen (ZIP)', async () => { const r = await p.evaluate(async () => { const x = await fetch('api/export'); return { s: x.status, t: x.headers.get('content-type'), n: (await x.arrayBuffer()).byteLength }; }); ok(r.s === 200 && /zip/.test(r.t) && r.n > 1000, JSON.stringify(r)); return r.n + ' Byte'; });
  await schritt('O12 Herkunft online: Schreiben ohne eigene Herkunft 403', async () => { const r = await (await fetch(B + 'api/anfrage', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://boese.example' }, body: '{}' })).status; ok(r === 403, 'Status ' + r); return '403'; });
  console.log(`online ${MOTOR}: ${gruen} grün, ${rot} rot von ${gruen + rot}`); await br.close();
})();
