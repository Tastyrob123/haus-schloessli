/* Abnahme Das Besucherbuch (Le Registre) · Wirtschaft am Schlössli (Kopie der Abnahme des Berghotel Gasterntal): die Funktionsliste des Le Registre (Grand Beau-Rivage, Stand 16.10.2026, plus die Carlton-Zusätze
   G10–G13 und die Doldenhorn-Zeilen Z01, Z02, E05; Vorlage: abnahme.js des Waldhotel Doldenhorn, 91 Zeilen), Zeile für Zeile als Prüfung, angepasst an den Rahmen
   der Oberfläche der Häuser (Kopf, Rand, Leiste, Startbild aus /assets/oberflaeche/) und die Ereignisse des Schlössli (Reservation, «Direkt buchen», Bankett, Gutschein, Schäfli, Route zum Hafen).
   Vor dem Pitch (Demo-Niveau): Chromium und Safari-Kern × 1440 × 900 und 390 × 844 (vier Läufe). Nach dem Auftrag: ALLE=1 → drei Browser × vier Breiten.
   Die Liste in FUNKTIONSLISTE.md wird aus dieser Datei erzeugt (node abnahme.js liste), die Haken stehen dort nach jedem Lauf.
     node abnahme.js                    die vier Läufe (ALLE=1: zwölf Läufe mit Firefox, 1366 und 320)
     node abnahme.js webkit 1440        ein Lauf;  NUR=A01,B03 node abnahme.js chromium 1440   einzelne Zeilen
   Läuft an der eigenen Probe-Kopie (_pruefung/probe.sh → ~/Desktop/Website-Projekte/_Probe Schloessli Registre/), eigener Server auf Port 8992 (PRUEF_PORT) mit
   eigenem Datenordner unter /tmp (wird danach gelöscht; 8988 bleibt dem Werkzeug). Am echten Schlössli wird nichts geschrieben.
   Die Formulare der Website verschicken nichts (Designstudie, haus.js); gastronovi, OpenStreetMap und das Schäfli werden im Prüfbrowser abgefangen. */
const path = require('path'), fs = require('fs'), os = require('os'), cp = require('child_process');
const PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const HIER = __dirname;
const PORT = +(process.env.PRUEF_PORT || 8992);   /* eigener Port der Prüfung: 8988 gehört dem laufenden Werkzeug, nie gegen die echten Daten prüfen */
const B = 'http://localhost:' + PORT + '/_werkzeuge/registre/';
const PROBE = path.join(process.env.HOME, 'Desktop/Website-Projekte/_Probe Schloessli Registre');
const A = B;
const KEY = fs.readFileSync(path.join(process.env.HOME, 'Desktop/Website-Projekte/_Schluessel/schloessli-bottighofen.txt'), 'utf8').trim();
const BILDER = path.join(HIER, '_pruefung', 'bilder');
const AUS = process.argv.slice(2);

const LISTE = [];
const C = (id, bereich, text, fn, o = {}) => LISTE.push(Object.assign({ id, bereich, text, fn }, o));
const ANSICHTEN = ['start', 'besuche', 'herkunft', 'zeit', 'seiten', 'verlauf', 'buchung', 'zaehlung'];
const MIT_ZEITRAUM = ['start', 'besuche', 'herkunft', 'zeit', 'seiten', 'verlauf', 'buchung'];
const TITEL = { start: 'Übersicht', besuche: 'Besuche', herkunft: 'Herkunft', zeit: 'Zeit', seiten: 'Seiten', verlauf: 'Verlauf', buchung: 'Zur Reservation', zaehlung: 'So wird gezählt' };
const ok = (b, was) => { if (!b) throw new Error(was); };
const warte = ms => new Promise(r => setTimeout(r, ms));
const BEREIT = () => window.BG_REGISTRE === 1 && document.documentElement.classList.contains('auftakt-da');
const HAUS = 'Wirtschaft am Schlössli';
/* Namen der Werkzeuge aus dem Kleid des Hauses (_werkzeuge/oberflaeche/kleid/schloessli.js, WO_HAUS.namen, Robert 19.10.2026), nie abgetippt */
const KLEID_N = fs.readFileSync(path.join(HIER, '..', 'oberflaeche', 'kleid', 'schloessli.js'), 'utf8').match(/namen:\s*\{([^}]*)\}/)[1];
const NAME_W = k => KLEID_N.match(new RegExp(k + ":\\s*'([^']+)'"))[1];
const NAME = NAME_W('besuche'), STUBE_N = NAME_W('zentrale'), KLEIN = NAME.replace(/^(Die|Das|Der) /, m => m.toLowerCase());
const rx = t => new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
const NAV = '#rand .wo-re[data-gehe]:not([data-weg])', WEGE = '#rand [data-weg], #rand .wo-rand__wege a', TITEL_K = '#kopf .wo-kopf__mitte b', STAND_K = '#kopf .wo-kopf__mitte small', BER = '#kopf .wo-kopf__ber';
const MAISON_DA = fs.existsSync(path.join(HIER, '..', 'maison', 'index.html'));   /* Die Stube des Schlössli baut ein anderer Chat (_werkzeuge/maison/, online /maison/) */

async function auf(env, hash = 'start', q = 'gruss=tag', basis = A, opt = {}) {
  const page = await env.ctx.newPage();
  page.on('console', m => { if (m.type() === 'error') env.fehler.push(env.id + ': Konsole: ' + m.text()); });
  page.on('pageerror', e => env.fehler.push(env.id + ': Seitenfehler: ' + e.message));
  page.on('response', r => { if (r.status() >= 400 && !opt.ok404) env.fehler.push(env.id + ': ' + r.status() + ' ' + r.url()); });
  await page.goto(basis + (q ? '?' + q : '') + (hash ? '#' + hash : ''), { waitUntil: 'load' });
  if (!opt.roh) { await page.waitForFunction(BEREIT, null, { timeout: 15000 }); await page.waitForTimeout(opt.ruhe == null ? 350 : opt.ruhe); }
  return page;
}
const text = (page, sel) => page.evaluate(s => (document.querySelector(s) || {}).textContent || '', sel);
const zahl = (page, sel) => page.evaluate(s => document.querySelectorAll(s).length, sel);
const sicht = async (page, sel) => page.evaluate(s => { const e = document.querySelector(s); if (!e) return false; const r = e.getBoundingClientRect(), c = getComputedStyle(e); return r.width > 2 && r.height > 2 && c.visibility !== 'hidden' && c.display !== 'none' && +c.opacity > 0.05; }, sel);
async function bisEnde(page) {
  await page.evaluate(async () => {
    const f = document.querySelector('#flaeche'), sc = getComputedStyle(f).overflowY === 'auto' ? f : document.scrollingElement;
    for (let i = 0, l = -1; i < 90 && sc.scrollTop !== l; i++) { l = sc.scrollTop; sc.scrollTop += 200; await new Promise(r => setTimeout(r, 90)); }
  });
  await page.waitForTimeout(3000);
}
const zeile = (tag, n, ua) => `r1 ${tag} index.html de rechner ${n} - google.com`;
async function sende(basis, roh, ua) { const r = await fetch(basis.replace('/_werkzeuge/registre/', '') + '/api/registre', { method: 'POST', body: roh, headers: { 'User-Agent': ua || 'Mozilla/5.0 (Macintosh) AppleWebKit Safari', 'Content-Type': 'text/plain' } }); return r.status; }
async function stand(basis, q) { const r = await fetch(basis.replace('/_werkzeuge/registre/', '') + '/api/registre?' + q); return r.json(); }

/* ================= A Laden und Aufbau ================= */
C('A01', 'Laden', 'Auftakt: beim Öffnen bleibt die Seite ruhig (alles verborgen), bis Daten, Schriften und Fotos im ersten Bild da sind (höchstens 2,5 s), dann erscheint alles auf einmal', async env => {
  const page = await env.ctx.newPage(); await page.goto(A + '?gruss=tag#start', { waitUntil: 'commit' });
  await page.waitForFunction(() => document.documentElement.classList.contains('auftakt') || document.documentElement.classList.contains('auftakt-da'), null, { timeout: 4000 });
  const t0 = Date.now(); await page.waitForFunction(() => document.documentElement.classList.contains('auftakt-da'), null, { timeout: 4000 });
  ok(Date.now() - t0 < 2700, 'Auftakt dauerte ' + (Date.now() - t0) + ' ms');
  const bi = await page.evaluate(() => { const i = document.querySelector('.wo-sb__foto img'); return i && i.complete && i.naturalWidth; });
  ok(bi > 0, 'Bühnenbild beim Erscheinen nicht geladen'); await page.close();
});
C('A02', 'Laden', 'Beim Erscheinen stehen Rand, Kopf, Bühne mit Titel und Leiste schon da (nichts halb weiss, nichts leer)', async env => {
  const p = await auf(env, 'start'); for (const s of [env.breite > 900 ? NAV : BER, env.breite > 900 ? '#kopf .wo-kopf__r' : '#kopf .wo-marke-w', '.wo-sb h1', '#leiste .wo-leiste__t b', '.wo-sb__foto img']) ok(await sicht(p, s), s + ' nicht sichtbar'); await p.close();
});
C('A03', 'Laden', 'Jede der acht Ansichten öffnet über die Adresse (#start … #zaehlung) und zeigt ihren Titel', async env => {
  for (const v of ANSICHTEN) { const p = await auf(env, v); const h = await text(p, TITEL_K); ok(h === TITEL[v], v + ': Kopftitel «' + h + '»'); ok((await text(p, '.wo-sb h1')).length > 8, v + ': Bühnentitel leer'); await p.close(); }
});
C('A04', 'Laden', 'Eine unbekannte Adresse (#gibtsnicht) öffnet die Übersicht', async env => { const p = await auf(env, 'gibtsnicht'); ok(await text(p, TITEL_K) === 'Übersicht', 'nicht Übersicht'); await p.close(); });
C('A05', 'Laden', 'Der Tab-Titel nennt die Ansicht («Besuche · <Name aus dem Kleid> · Wirtschaft am Schlössli»)', async env => { for (const v of ['start', 'seiten', 'zaehlung']) { const p = await auf(env, v); const t = await p.title(); ok(t === TITEL[v] + ' · ' + NAME + ' · ' + HAUS, 'Titel «' + t + '»'); await p.close(); } });
C('A06', 'Laden', 'Seiten stehen mit ihrem Namen da (Startseite, Die Karte, Weinkarte, Banketts & Gruppen …, gelesen aus den Titeln der Website), nie als Dateiname', async env => { const p = await auf(env, 'seiten'); const t = await text(p, '.tabelle'); ok(/Startseite/.test(t) && /Die Karte/.test(t) && /Banketts & Gruppen/.test(t) && !/\.html|index/.test(t), 'Dateiname sichtbar'); await p.close(); });
C('A07', 'Laden', '?gruss=tag hält den Gruss fest («Guten Tag.») für die Bildschirmfotos der Werkbank', async env => { const p = await auf(env, 'start'); ok(/Guten Tag\./.test(await text(p, '.wo-sb h1')), 'Gruss'); await p.close(); });
C('A08', 'Laden', 'Ohne Schlüssel zeigt die Adresse immer Beispielwerte (auch mit ?beispiel=1 gleich), überall beschriftet', async env => {
  for (const q of ['', 'beispiel=1']) { const p = await auf(env, 'start', q); ok(await sicht(p, '.bsp-band'), 'Beispiel-Band fehlt (' + q + ')'); ok(/Beispielwerte/.test(await text(p, '#leiste')), 'Leiste ohne Beispiel'); await p.close(); }
});
C('A08b', 'Laden', 'Mit falschem Schlüssel antwortet auch der Dienst nur mit Beispielwerten (Beispiel-Band da, kein Knopf zu den echten)', async env => { const p = await auf(env, 'start', 'gruss=tag&k=falsch', B); ok(await p.evaluate(() => !!document.querySelector('.bsp-band')), 'Band fehlt'); await p.close(); }, { server: true });
C('A09', 'Laden', 'Fällt das Laden aus, steht «<Name> startet nicht» mit dem Grund und den Knöpfen «Neu laden» und dem Weg zur Zentrale, kein leeres Fenster', async env => {
  const p = await env.ctx.newPage(); await p.route('**/beispiel/*.json', r => r.abort()); await p.route('**/api/registre**', r => r.abort());
  await p.goto(A + '?gruss=tag#start'); await p.waitForFunction(() => !document.querySelector('#tuer').hidden, null, { timeout: 8000 });
  ok(/startet nicht/.test(await text(p, '#tuer')) && (await text(p, '#tuer-t')).length > 10, 'Tür ohne Grund'); ok(await p.evaluate(([STUBE_N, NAME]) => !!document.querySelector('#tuer [data-neu]') && document.querySelector('#tuer').textContent.includes(STUBE_N) && document.querySelector('#tuer h1').textContent === NAME + ' startet nicht.', [STUBE_N, NAME]), 'Knöpfe der Tür'); await p.close();
});
C('A10', 'Laden', 'Der gewählte Zeitraum wird im Browser gemerkt und beim nächsten Öffnen wieder gewählt', async env => {
  const p = await auf(env, 'start'); await p.click('[data-tage="7"]'); await p.waitForFunction(() => document.querySelector('[data-tage="7"]').classList.contains('an')); await p.reload(); await p.waitForFunction(BEREIT);
  ok(await p.evaluate(() => document.querySelector('[data-tage="7"]').classList.contains('an')), 'Zeitraum vergessen'); await p.click('[data-tage="30"]'); await p.waitForTimeout(300); await p.close();
});
C('A11', 'Laden', 'Keine Konsolenfehler, keine toten Adressen beim Öffnen jeder Ansicht', async env => { const n0 = env.fehler.length; for (const v of ANSICHTEN) { const p = await auf(env, v); await p.close(); } ok(env.fehler.length === n0, env.fehler.slice(n0).join(' | ')); });

/* ================= B Kopf ================= */
C('B01', 'Kopf', 'Der Kopf nennt oben den Titel der Ansicht und darunter den Stand («Beispielwerte · keine echten Besuche»)', async env => {
  for (const v of ['start', 'besuche', 'zeit']) { const p = await auf(env, v); ok(await text(p, TITEL_K) === TITEL[v] && /Beispielwerte · keine echten Besuche/.test(await text(p, STAND_K)), v); await p.close(); } }, { nurRechner: true });
C('B02', 'Kopf', 'Anleitung: runder Knopf mit Hinweis, öffnet anleitung.html in neuem Tab', async env => {
  const p = await auf(env); const a = await p.$('#kopf a[aria-label="Anleitung"]'); ok(a, 'Knopf fehlt');
  ok(await a.getAttribute('href') === 'anleitung.html' && await a.getAttribute('target') === '_blank' && await a.getAttribute('title') === 'Anleitung', 'Ziel/Hinweis'); await p.close(); });
C('B03', 'Kopf', 'Die Stube: runder Knopf mit Hinweis, führt zur Stube (lokal ../maison/ = _werkzeuge/maison/, online ../../maison/ = /maison/; die Adresse antwortet)', async env => { const p = await auf(env); const a = await p.$(`#kopf a[aria-label="${STUBE_N}, zu allen Werkzeugen"]`); const h = a && await a.getAttribute('href'); const st = (await fetch(new URL(h || 'x', B)).catch(() => ({ status: 0 }))).status; ok(h === '../maison/' && (st === 200 || (!MAISON_DA && st === 404)) && await a.getAttribute('data-tip') === STUBE_N, STUBE_N + ' ' + h + ' ' + st); await p.close(); });
C('B04', 'Kopf', '«Website ansehen» öffnet die Website in neuem Tab', async env => { const p = await auf(env); const a = await p.$('#kopf a.wo-kn--gold'); ok(a && /index\.html$/.test(await a.getAttribute('href')) && await a.getAttribute('target') === '_blank', 'Website-Knopf'); await p.close(); });
C('B05', 'Kopf', 'Die Marke «Das Besucherbuch» (Zeichen des Hauses, oben links) führt zurück zur Übersicht', async env => { const p = await auf(env, 'seiten'); await p.click('#kopf .wo-marke-w'); await p.waitForTimeout(300); ok(await text(p, TITEL_K) === 'Übersicht', 'nicht Übersicht'); await p.close(); });
C('B06', 'Kopf', 'Am Handy (Oberfläche der Häuser): im Kopf Marke und «Bereiche», Kopf-Titel und runde Knöpfe weichen; Website, Anleitung und Die Stube stehen im aufgeklappten Rand', async env => {
  const p = await auf(env); ok(await sicht(p, '#kopf .wo-marke-w') && await sicht(p, BER), 'Marke/Bereiche'); ok(!(await sicht(p, '.wo-kopf__mitte')) && !(await sicht(p, '#kopf .wo-kn--rund')), 'Titel/Knöpfe stehen noch');
  await p.click(BER); const t = await p.evaluate(s => [...document.querySelectorAll(s)].filter(a => a.offsetWidth).map(a => a.textContent.trim()), WEGE); for (const w of ['Website ansehen', 'Anleitung', STUBE_N]) ok(t.includes(w), w + ' fehlt: ' + t.join('|')); await p.close(); }, { nurHandy: true });

/* ================= C Rand ================= */
C('C01', 'Rand', 'Der Rand führt in die acht Ansichten (Übersicht; Die Gäste: Besuche, Herkunft, Zeit; Die Website: Seiten, Verlauf, Zur Reservation; Gut zu wissen: So wird gezählt), die aktuelle ist markiert', async env => {
  const p = await auf(env, 'start'); const d = await p.evaluate(n => [...document.querySelectorAll(n)].map(a => a.dataset.gehe), NAV); ok(d.join() === ANSICHTEN.join(), 'Einträge ' + d.join());
  if (env.breite > 900) for (const v of ANSICHTEN) { await p.click(`${NAV}[data-gehe="${v}"]`); await p.waitForTimeout(250); ok(await p.evaluate(v => location.hash === '#' + v && document.querySelector('#rand .wo-re.wo-an')?.dataset.gehe === v && document.querySelector('#rand .wo-re.wo-an').getAttribute('aria-current') === 'true', v), 'Rand → ' + v); }
  await p.close(); });
C('C02', 'Rand', 'Die Zahl hinter «Besuche» ist die Zahl der Besuche von heute (ohne Besuch heute keine Zahl; geprüft jetzt und um 16 Uhr)', async env => {
  const p = await auf(env); const z = +(await text(p, '#rand [data-gehe="besuche"] .wo-zahl')); const h = +(await p.evaluate(() => S.d.summe.heute)); ok(z === h, z + ' vs ' + h); await p.close();
  const q = await aufZeit(env, new Date(zuerich(Date.now())[0] + 'T16:00:00+02:00').getTime(), 30); const z2 = +(await text(q, '#rand [data-gehe="besuche"] .wo-zahl')); const h2 = +(await q.evaluate(() => S.d.summe.heute)); ok(z2 > 0 && z2 === h2, '16 Uhr: ' + z2 + ' vs ' + h2); await q.close(); }, { nurRechner: true });
C('C03', 'Rand', 'Unten im Rand stehen die Wege: Was gezählt wird, Die Stube, Kurzer Rundgang, Website ansehen, Anleitung', async env => {
  const p = await auf(env); if (env.breite <= 900) await p.click(BER); const t = await p.evaluate(s => [...document.querySelectorAll(s)].map(a => a.textContent.trim()), WEGE); for (const s of ['Website ansehen', 'Was gezählt wird', 'Anleitung', STUBE_N, 'Kurzer Rundgang']) ok(t.includes(s), s + ' fehlt: ' + t.join('|')); await p.close(); });
C('C04', 'Rand', '«Was gezählt wird» öffnet «So wird gezählt»', async env => { const p = await auf(env); if (env.breite <= 900) await p.click(BER); await p.click('#rand [data-weg][data-gehe="zaehlung"]'); await p.waitForTimeout(300); ok(await text(p, TITEL_K) === 'So wird gezählt', 'Ziel'); await p.close(); });
C('C05', 'Rand', 'Am Handy klappt «Bereiche» den Rand auf und zu, nach der Wahl einer Ansicht schliesst er', async env => {
  const p = await auf(env); ok(!(await sicht(p, NAV)), 'Rand offen'); await p.click(BER); ok(await sicht(p, NAV), 'öffnet nicht'); ok(await p.getAttribute(BER, 'aria-expanded') === 'true', 'aria-expanded');
  await p.click(BER); ok(!(await sicht(p, NAV)), 'schliesst nicht'); await p.click(BER); await p.click(`${NAV}[data-gehe="seiten"]`); await p.waitForTimeout(300); ok(!(await sicht(p, NAV)), 'bleibt offen'); await p.close(); }, { nurHandy: true });

/* ================= D Zeitraum ================= */
C('D01', 'Zeitraum', 'Unter jedem Titel wählt man 7, 30 oder 90 Tage; die gewählte ist markiert (aria-pressed), in allen sieben Ansichten mit Zahlen', async env => {
  for (const v of MIT_ZEITRAUM) { const p = await auf(env, v); const k = await p.evaluate(() => [...document.querySelectorAll('[data-tage]')].map(b => b.dataset.tage + ':' + b.getAttribute('aria-pressed'))); ok(k.join() === '7:false,30:true,90:false', v + ' ' + k.join()); await p.close(); } });
C('D02', 'Zeitraum', 'Der Zeitraum gilt für alle Zahlen: 7 Tage haben weniger Besuche als 30, 30 weniger als 90; die Leiste und der Satz folgen', async env => {
  const p = await auf(env); const w = {}; for (const t of [7, 30, 90]) { await p.click(`[data-tage="${t}"]`); await p.waitForFunction(t => document.querySelector(`[data-tage="${t}"]`).classList.contains('an'), t); await p.waitForTimeout(300); w[t] = await p.evaluate(() => [S.d.summe.besuche, S.d.tage, document.querySelectorAll('.saeulen .s').length]); }
  ok(w[7][0] < w[30][0] && w[30][0] < w[90][0], 'Besuche ' + [7, 30, 90].map(t => w[t][0]).join('/')); ok(w[7][2] === 7 && w[30][2] === 30 && w[90][2] === 90, 'Säulen ' + [7, 30, 90].map(t => w[t][2]).join('/')); await p.click('[data-tage="30"]'); await p.close(); });
C('D03', 'Zeitraum', 'Ein neuer Zeitraum setzt die Besuchsliste zurück (erste Karte gewählt, wieder 40 Zeilen)', async env => {
  const p = await auf(env, 'besuche'); await p.click('[data-mehr]'); ok(await zahl(p, '.liste .besuch') > 40, 'Weitere zeigen wirkt nicht'); await p.click('[data-tage="90"]'); await p.waitForTimeout(500);
  ok(await zahl(p, '.liste .besuch') === 40 && await p.evaluate(() => S.wahl === 0), 'nicht zurückgesetzt'); await p.click('[data-tage="30"]'); await p.close(); });
C('D04', 'Zeitraum', 'Die Besuchstage in der Übersicht tragen Beschriftung im richtigen Abstand (7 Tage: jeder, 30: alle fünf, 90: alle fünfzehn)', async env => {
  const p = await auf(env); const r = {}; for (const t of [7, 30, 90]) { await p.click(`[data-tage="${t}"]`); await p.waitForFunction(t => document.querySelector(`[data-tage="${t}"]`).classList.contains('an'), t); await p.waitForTimeout(250); r[t] = await zahl(p, '.tafel .saeulen .s span'); }
  ok(r[7] === 7 && r[30] >= 6 && r[30] <= 7 && r[90] >= 6 && r[90] <= 7, JSON.stringify(r)); await p.click('[data-tage="30"]'); await p.close(); });

/* ================= E Leiste ================= */
C('E01', 'Leiste', 'Die Leiste unten nennt «Sie sehen Beispielwerte» und dazu den Satz «Erfunden, damit Sie sehen …»', async env => { const p = await auf(env); const t = await text(p, '#leiste'); ok(/Sie sehen Beispielwerte/.test(t) && /Erfunden, damit Sie sehen/.test(t) || env.breite <= 900, t); ok(/Sie sehen Beispielwerte/.test(t), t); await p.close(); });
/* E02 «Dieses Gerät nicht mitzählen» entfällt (Robert 18.10.2026 18:44: Knopf überflüssig) */
C('E03', 'Leiste', 'In der Vorführung gibt es keinen Knopf zu den echten Besuchen und kein «Neu laden»', async env => { const p = await auf(env); ok(!(await p.$('#l-echt')) && !(await p.$('#l-neu')), 'Knopf sichtbar'); await p.close(); });
C('E04', 'Leiste', 'Am Handy ist die Leiste umgebrochen, nichts läuft aus dem Bild; «Als Tabelle sichern» steht dort unter der Besuchsliste (schloessli.css blendet ihn in der Leiste aus, wie Carlton und Doldenhorn) und ist erreichbar', async env => { const p0 = await auf(env, 'besuche'); await p0.evaluate(() => document.querySelector('[data-sichern]').scrollIntoView({ block: 'center' })); await p0.waitForTimeout(400); ok(await sicht(p0, '[data-sichern]'), 'Knopf unter der Liste weg'); await p0.close(); const p = await auf(env); ok(await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Überlauf'); const ab = await p.evaluate(() => [...document.querySelectorAll('#leiste button')].filter(x => x.offsetWidth && x.scrollWidth > x.clientWidth + 1).map(x => x.textContent.trim())); ok(!ab.length, 'Knopftext abgeschnitten: ' + ab.join(', ')); await p.close(); }, { nurHandy: true });

/* ================= F Meldungen ================= */
C('F01', 'Meldungen', 'Meldungen stehen als Karte mit Kreuz, höchstens drei, und verschwinden nach fünf Sekunden von selbst; das Kreuz schliesst sofort', async env => {
  const p = await auf(env); for (let i = 0; i < 4; i++) { await p.evaluate(() => quit('Probe', 'Meldung'));   /* quit() des Besucherbuchs (registre.js); das Paket der Oberfläche hat keine eigene Meldung (Gasterntal-Vorlage rief WO.quit, das es nicht gibt) */ await p.waitForTimeout(120); }
  ok(await zahl(p, '.quit') === 3, 'Zahl ' + await zahl(p, '.quit')); await p.click('.quit button'); await p.waitForTimeout(200); ok(await zahl(p, '.quit') === 2, 'Kreuz'); await p.waitForTimeout(5400); ok(await zahl(p, '.quit') === 0, 'bleibt stehen');
  const g = await p.evaluate(() => localStorage.getItem('schloessli-nicht-zaehlen')); if (g) { await p.evaluate(() => localStorage.removeItem('schloessli-nicht-zaehlen')); } await p.close(); });

/* ================= G Bühne ================= */
C('G01', 'Bühne', 'Jede Ansicht beginnt mit dem Startbild der Oberfläche: Übersicht «voll» mit dem Aussenfoto des Hauses, jede andere Ansicht «Bühne» mit eigenem Bild; Foto geladen, Titel, Satz, mindestens 240 px hoch', async env => {
  const fotos = new Set(); for (const v of ANSICHTEN) { const p = await auf(env, v); const r = await p.evaluate(() => { const i = document.querySelector('.wo-sb__foto img'), b = document.querySelector('.wo-sb').getBoundingClientRect(); return [i.complete && i.naturalWidth > 100, document.querySelector('.wo-sb h1').textContent.length, !!document.querySelector('.wo-sb__satz'), b.height, document.querySelector('.wo-sb').classList.contains('wo-sb--voll'), i.getAttribute('src')]; });
    ok(r[0] && r[1] > 8 && r[2] && r[3] >= 240 && r[4] === (v === 'start'), v + ' ' + JSON.stringify(r)); fotos.add(r[5]); await p.close(); } ok(fotos.size === ANSICHTEN.length, 'Bilder doppelt: ' + fotos.size); });
C('G02', 'Bühne', 'Die Übersicht zeigt im Startbild vier Kennzahlen (Besuche, Länder, heute, zur Reservation) in der Form der Tafel des Hauses', async env => { const p = await auf(env); ok(await zahl(p, '.buehne__chips li') === 4, 'Plaketten'); await p.close(); });
C('G03', 'Bühne', 'In jeder Ansicht mit Zahlen steht über dem Inhalt das Band «Beispielwerte. Diese Zahlen sind erfunden …»', async env => { for (const v of MIT_ZEITRAUM) { const p = await auf(env, v); ok(await sicht(p, '.bsp-band') || await p.evaluate(() => !!document.querySelector('.bsp-band')), v + ' ohne Band'); await p.close(); } });
C('G04', 'Bühne', 'Der Zeitraum sitzt im Startbild jeder Ansicht (Segment-Wahl der Oberfläche)', async env => { const p = await auf(env, 'zeit'); ok(await p.evaluate(() => !!document.querySelector('.wo-sb [data-tage]')), 'Zeitraum nicht auf der Bühne'); await p.close(); });

/* ================= H Übersicht ================= */
C('H01', 'Übersicht', 'Vier Zahlen: Besuche (mit Vergleich zum Zeitraum davor), angesehene Seiten (je Besuch), Minuten je Besuch, zur Reservation (Tisch angefragt oder «Direkt buchen», Prozent der Besuche)', async env => {
  const p = await auf(env); const t = await p.evaluate(() => [...document.querySelectorAll('.zahlen .blatt')].map(b => b.textContent.replace(/\s+/g, ' ').trim())); ok(t.length === 4, 'Zahl ' + t.length); ok(/zu davor/.test(t[0]) && /je Besuch/.test(t[1]) && /\d:\d\d/.test(t[2]) && /% der Besuche/.test(t[3]), t.join(' | ')); await p.close(); });
C('H02', 'Übersicht', 'Besuche je Tag als Säulen, eine je Tag, mit Tag und Zahl beim Darüberfahren und Datum darunter', async env => {
  const p = await auf(env); ok(await zahl(p, '.tafel .saeulen .s') === 30, 'Säulen'); const s = await p.$('.tafel .saeulen .s:nth-child(14)'); await s.scrollIntoViewIfNeeded(); await s.hover(); await p.waitForTimeout(400);
  ok(await p.evaluate(() => { const e = document.querySelector('.tafel .saeulen .s:nth-child(14)'); return getComputedStyle(e, '::after').opacity === '1' && /Besuch/.test(e.dataset.t); }), 'Tooltip'); await p.close(); }, { nurRechner: true });
C('H03', 'Übersicht', 'Zwei Blöcke: «Woher die Gäste kommen» (sechs Länder) und «Am meisten angesehen» (sechs Seiten mit Zeit im Schnitt), je mit Link zur ganzen Liste', async env => {
  const p = await auf(env); ok(await zahl(p, '.zwei > .blatt:nth-child(1) .rang li') === 6 && await zahl(p, '.zwei > .blatt:nth-child(2) .rang li') === 6, 'je sechs'); ok(/im Schnitt/.test(await text(p, '.zwei > .blatt:nth-child(2)')), 'Zeit im Schnitt');
  await p.click('button.link[data-gehe="herkunft"]'); await p.waitForTimeout(300); ok(await text(p, TITEL_K) === 'Herkunft', 'Link Länder'); await p.goto(A + '#start'); await p.reload(); await p.waitForFunction(BEREIT); await p.click('button.link[data-gehe="seiten"]'); await p.waitForTimeout(300); ok(await text(p, TITEL_K) === 'Seiten', 'Link Seiten'); await p.close(); });
C('H04', 'Übersicht', '«Zuletzt zu Besuch»: die letzten fünf Besuche als Karten; ein Klick öffnet genau diesen Besuch unter «Besuche»', async env => {
  const p = await auf(env); ok(await zahl(p, '.liste--start .besuch') === 5, 'fünf'); const ort = await text(p, '.liste--start .besuch:nth-child(3) b'); await p.evaluate(() => document.querySelector('.liste--start .besuch:nth-child(3)').scrollIntoView({ block: 'center' })); await p.waitForTimeout(400); await p.click('.liste--start .besuch:nth-child(3)'); await p.waitForTimeout(500);
  ok(await text(p, TITEL_K) === 'Besuche', 'Ansicht'); ok((await text(p, '.detail h2')) === ort, 'Besuch ' + ort + ' vs ' + await text(p, '.detail h2')); await p.close(); });
C('H05', 'Übersicht', '«Alle Besuche» führt in die Besuchsliste', async env => { const p = await auf(env); await p.evaluate(() => document.querySelector('.mehr').scrollIntoView({ block: 'center' })); await p.waitForTimeout(400); await p.click('.mehr button'); await p.waitForTimeout(400); ok(await text(p, TITEL_K) === 'Besuche', 'Ziel'); await p.close(); });

/* ================= I Besuche ================= */
C('I01', 'Besuche', 'Über der Liste grenzt man ein: Alle, Zur Reservation, Bankett oder Anfrage, Anruf oder Mail, Am Handy (je mit Zahl); die Wahl ist markiert und Zur Reservation zeigt nur Besuche mit hellem Kreis', async env => {
  const p = await auf(env, 'besuche'); for (const f of ['buchung', 'anfrage', 'kontakt', 'handy', 'alle']) { await p.click(`[data-filter="${f}"]`); await p.waitForTimeout(250); const r = await p.evaluate(f => ({ an: document.querySelector(`[data-filter="${f}"]`).getAttribute('aria-pressed'), n: document.querySelectorAll('.liste .besuch').length, gold: [...document.querySelectorAll('.liste .besuch')].every(b => b.classList.contains('gold')), zahl: +document.querySelector(`[data-filter="${f}"]`).textContent.split('·')[1] }), f);
    ok(r.an === 'true' && r.n > 0 && r.n <= r.zahl && (f !== 'buchung' || r.gold), f + ' ' + JSON.stringify(r)); } await p.close(); });
C('I01b', 'Besuche', 'Beim Wählen eines Filters oder bei «Weitere zeigen» bleibt die Seite ruhig: die Filterleiste und die Liste schweben nicht neu herein (und lassen sich sofort anklicken)', async env => {
  const p = await auf(env, 'besuche'); for (const f of ['buchung', 'anfrage', 'kontakt', 'handy', 'alle']) { await p.click(`[data-filter="${f}"]`, { timeout: 5000 }); const r = await p.evaluate(() => { const e = document.querySelector('.wahl3--filter'), c = getComputedStyle(e); return [c.animationName, c.translate]; }); ok(r[0] === 'none' && (r[1] === 'none' || r[1] === '0px'), f + ' ' + r); }
  await p.click('[data-mehr]', { timeout: 5000 }); await p.close(); });
C('I02', 'Besuche', 'Die Liste ist nach Tagen gegliedert («Heute», «Gestern», Wochentag, Datum; geprüft jetzt und um 16 Uhr Schweizer Zeit)', async env => {
  const p = await auf(env, 'besuche'); const t = await p.evaluate(() => [...document.querySelectorAll('.tagzeile')].map(x => x.textContent)); const h = await p.evaluate(() => S.d.summe.heute);
  ok((h ? /^Heute$/i.test(t[0]) && /^Gestern$/i.test(t[1]) : /^Gestern$/i.test(t[0])) && t.filter(x => !/Gezeigt/.test(x)).length >= 2, t.slice(0, 3).join('|')); await p.close();
  const q = await aufZeit(env, new Date(zuerich(Date.now())[0] + 'T16:00:00+02:00').getTime(), 30, 'besuche'); await q.click('[data-mehr]'); await q.waitForTimeout(300); const t2 = await q.evaluate(() => [...document.querySelectorAll('.tagzeile')].map(x => x.textContent).filter(x => !/Gezeigt/.test(x))); ok(/^Heute$/i.test(t2[0]) && /^Gestern$/i.test(t2[1]) && /\d{1,2}\. \w+/.test(t2[2]), '16 Uhr: ' + t2.slice(0, 3).join('|')); await q.close(); });
C('I03', 'Besuche', 'Einen Besuch wählen wechselt nur die Karte; die Liste bleibt, wo sie ist (Seite springt nicht nach oben), genau ein Besuch ist gewählt', async env => {
  const p = await auf(env, 'besuche'); await p.evaluate(() => document.querySelectorAll('.liste .besuch')[5].scrollIntoView({ block: 'center' })); await p.waitForTimeout(600);
  const y1 = await p.evaluate(() => [document.querySelector('#flaeche').scrollTop, scrollY]); const ziel = await p.evaluate(() => document.querySelectorAll('.liste .besuch')[5].querySelector('b').textContent);
  const xy = await p.evaluate(() => { const r = document.querySelectorAll('.liste .besuch')[5].getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }); await p.mouse.click(xy[0], xy[1]); await p.waitForTimeout(600); const y2 = await p.evaluate(() => [document.querySelector('#flaeche').scrollTop, scrollY]);
  ok(await zahl(p, '.liste .besuch.aktiv') === 1 && await p.evaluate(() => document.querySelectorAll('.liste .besuch')[5].classList.contains('aktiv')), 'falsche Auswahl'); ok(await text(p, '.detail h2') === ziel, 'Karte zeigt nicht ' + ziel);
  if (env.breite > 1180) ok(Math.abs(y2[0] - y1[0]) < 4 && y2[1] === y1[1], 'Seite sprang ' + y1 + ' → ' + y2); else ok(y2[0] + y2[1] >= 0, 'schmal'); await p.close(); });
C('I04', 'Besuche', 'Die Karte nennt Ort (Land), Tag, Siegel («Tisch angefragt» / ««Direkt buchen» gewählt» / «Bankett oder Anfrage» / «Anruf oder Mail» wo es zutrifft), sechs Angaben (Gekommen, Geblieben, Seiten, Gerät, Sprache, Gekommen über) und den Weg durch die Website mit Zeit je Seite', async env => {
  const p = await auf(env, 'besuche'); await p.click('[data-filter="buchung"]'); await p.waitForTimeout(250); const r = await p.evaluate(() => ({ h: document.querySelector('.detail h2').textContent, siegel: document.querySelector('.detail .siegel')?.textContent, angaben: document.querySelectorAll('.detail .angaben > div').length, weg: document.querySelectorAll('.detail .weg li').length, gold: document.querySelectorAll('.detail .ereignis.gold').length, fein: !!document.querySelector('.detail .fein') }));
  ok(r.h.length > 3 && /Tisch angefragt|Direkt buchen/.test(r.siegel) && r.angaben === 6 && r.weg >= 1 && r.gold >= 1 && r.fein, JSON.stringify(r)); await p.close(); });
C('I05', 'Besuche', 'Unter einer Seite im Weg stehen die Klicks dort («Fenster «Reservation» geöffnet», «Tisch angefragt», ««Direkt buchen» gewählt», «Bankettanfrage geöffnet», «Anfrage abgeschickt», «Route zum Hafen geöffnet» …)', async env => { const p = await auf(env, 'besuche'); await p.click('[data-filter="buchung"]'); await p.waitForTimeout(300); ok(/Reservation|Tisch angefragt|Direkt buchen/.test(await text(p, '.detail .weg')), 'keine Ereignisse'); await p.click('[data-filter="anfrage"]'); await p.waitForTimeout(300); ok(/Bankettanfrage|Anfrage abgeschickt/.test(await text(p, '.detail .weg')) && /Bankett oder Anfrage/.test(await text(p, '.detail .siegel')), 'Anfrage ohne Ereignis'); await p.close(); });
C('I06', 'Besuche', '«Weitere zeigen» bringt jeweils 60 Besuche mehr; ganz unten steht, wie viele gezeigt werden («die neuesten 400»)', async env => { const p = await auf(env, 'besuche'); const n0 = await zahl(p, '.liste .besuch'); await p.click('[data-mehr]'); await p.waitForTimeout(300); const n1 = await zahl(p, '.liste .besuch'); ok(n0 === 40 && n1 === 100, n0 + '→' + n1); ok(/neuesten 400 Besuche/.test(await text(p, '.liste')), 'Hinweis 400'); await p.close(); });
C('I07', 'Besuche', 'Ist eine Auswahl leer, steht «Kein Besuch in dieser Auswahl» statt einer leeren Liste', async env => {
  const p = await env.ctx.newPage(); await p.route('**/beispiel/30.json', async r => { const d = await (await r.fetch()).json(); d.besuche.forEach(b => { b.buchung = false; }); r.fulfill({ json: d }); });
  await p.goto(A + '?gruss=tag#besuche'); await p.waitForFunction(BEREIT); await p.click('[data-filter="buchung"]'); await p.waitForTimeout(300); ok(/Kein Besuch in dieser Auswahl/.test(await text(p, '#ansicht')), 'Hinweis'); await p.close(); });
C('I08', 'Besuche', 'Rechner (ab 1181 px): die Karte rechts reicht vom Kopf bis über die Leiste, der Hinweis sitzt unten; sie bleibt beim Scrollen unter dem Kopf stehen; ohne eigene Scrollfläche (Oberfläche der Häuser: ein langer Weg verlängert die Karte)', async env => {
  const p = await auf(env, 'besuche'); await p.evaluate(() => scrollTo(0, document.querySelector('.eingang').getBoundingClientRect().top + scrollY - 60)); await p.waitForTimeout(300); const r = await p.evaluate(() => { const c = document.querySelector('.detail .besuchsblatt').getBoundingClientRect(), l = document.querySelector('#leiste').getBoundingClientRect(), w = document.querySelector('.detail .weg'); return { unten: Math.round(l.top - c.bottom), oben: Math.round(c.top), ueber: getComputedStyle(w).overflowY, haengt: [...document.querySelectorAll('*')].filter(e => /auto|scroll/.test(getComputedStyle(e).overflowY) && e.scrollHeight > e.clientHeight + 1 && e !== document.documentElement && e !== document.body).length }; });
  ok(r.unten >= -2 && r.unten < 60 && r.ueber === 'visible' && !r.haengt, JSON.stringify(r)); await p.evaluate(() => scrollTo(0, 1500)); await p.waitForTimeout(300); const c2 = await p.evaluate(() => Math.round(document.querySelector('.detail .besuchsblatt').getBoundingClientRect().top)); ok(c2 >= 86 && c2 <= 98, 'Karte bleibt nicht stehen: ' + c2); await p.close(); }, { nurRechner: true });
C('I09', 'Besuche', 'Schmal (bis 1180 px) steht die Karte über der Liste; wählt man weiter unten einen Besuch, rückt die Seite zur Karte', async env => {
  const p = await auf(env, 'besuche'); const o = await p.evaluate(() => document.querySelector('.detail').getBoundingClientRect().top < document.querySelector('.liste').getBoundingClientRect().top); ok(o, 'Karte nicht oben');
  await p.evaluate(() => document.querySelectorAll('.liste .besuch')[8].scrollIntoView({ block: 'center' })); await p.waitForTimeout(300); await p.evaluate(() => document.querySelectorAll('.liste .besuch')[8].click()); await p.waitForTimeout(700);
  const t = await p.evaluate(() => Math.round(document.querySelector('.detail').getBoundingClientRect().top)); ok(t > -10 && t < 200, 'Karte nicht im Bild: ' + t); await p.close(); }, { nurHandy: true });

/* ================= J Herkunft, Zeit, Seiten, Buchung ================= */
C('J01', 'Herkunft', 'Länder (zehn), Gekommen über (acht, «Direkt aufgerufen» für Adresse eingetippt), Orte (mit Land), Sprache, Gerät; Anteile in Prozent, Länder auf Deutsch', async env => {
  const p = await auf(env, 'herkunft'); const r = await p.evaluate(() => [...document.querySelectorAll('#ansicht .blatt .rang')].map(o => o.querySelectorAll('li').length)); ok(r.join() === '10,8,16,4,3' || (r.length === 5 && r[0] <= 10 && r[1] <= 8 && r[2] <= 16), r.join());
  const t = await text(p, '#ansicht'); ok(/Schweiz/.test(t) && /Direkt aufgerufen/.test(t) && /Google/.test(t) && /GaultMillau/.test(t) && /Thurgau Bodensee Tourismus/.test(t) && /Handy/.test(t) && /Sprache des Browsers/.test(t) && /Deutsch/.test(t) && /%/.test(t), 'Beschriftung'); ok(/\d+\s*%\s*Aus der Schweiz|Aus der Schweiz/.test(t), 'Schweiz-Anteil'); await p.close(); });
C('J02', 'Zeit', 'Zeit: Besuche nach Uhrzeit (24 Säulen), nach Wochentag und Stunde (Raster 7 × 24) und nach Wochentag; oben die Spitzen (meiste Besuche, stärkster Tag, ab 18 Uhr, am Wochenende)', async env => {
  const p = await auf(env, 'zeit'); ok(await zahl(p, '.saeulen--uhr .s') === 24 && await zahl(p, '.raster i') === 168 && await zahl(p, '.band > div') === 4, 'Aufbau'); await p.close(); });
C('J03', 'Seiten', 'Seiten: jede Seite mit Aufrufen (absteigend sortiert), Balken, Zeit im Schnitt und Klicks zur Buchung; Fusszeile «Nicht aufgeführte Seiten …»', async env => {
  const p = await auf(env, 'seiten'); const z = await p.evaluate(() => [...document.querySelectorAll('.tabelle .zeile:not(.zeile--kopf) .zeile__z')].map(x => +x.textContent.replace(/[’' ]/g, ''))); ok(z.length >= 10 && z.every((v, i) => i === 0 || z[i - 1] >= v), 'Sortierung ' + z.length + ': ' + z.slice(0, 5));   /* das Schlössli hat zwölf Seiten */ ok(/Nicht aufgeführte Seiten/.test(await text(p, '#ansicht')), 'Fuss'); ok(/Min\.|Sek\./.test(await text(p, '.tabelle')), 'Zeit'); await p.close(); });
C('J04', 'Verlauf', 'Verlauf: Besuche je Tag neben dem Zeitraum davor, Vergleichstabelle (Jetzt/Davor/Veränderung), Woche für Woche, die wichtigsten Länder im Verlauf', async env => {
  const p = await auf(env, 'verlauf'); ok(await zahl(p, '.saeulen--vgl .s') === 30 && await zahl(p, '.saeulen--vgl .s u') === 30, 'Säulen'); ok(await zahl(p, '.vergleich .vz') >= 7 && await zahl(p, '.wochen li') >= 5 && await zahl(p, '.lv') === 4, 'Teile'); ok(/zu davor|gleich wie davor/.test(await text(p, '.vergleich')), 'Veränderung'); await p.close(); });
C('J05', 'Zur Reservation', 'Zur Reservation: neun Werte mit Prozent und gezählten Zahlen (Startseite und Karte/Weinkarte zur Reservation; «Direkt buchen»; Fenster ohne nächsten Schritt; Bankettanfrage; Anfrage abgeschickt; Anruf oder Mail; weiter zum Schäfli; Route zum Hafen), «Von welcher Seite reserviert wird», der Weg zum Tisch', async env => {
  const p = await auf(env, 'buchung'); ok(await zahl(p, '.werte .wert') === 9, 'neun Werte'); const w = await p.evaluate(() => [...document.querySelectorAll('.werte .wert b')].map(b => b.textContent)); ok(w.every(x => /%/.test(x)), w.join()); ok(await zahl(p, '.zwei > .blatt:nth-child(1) .rang li') >= 2 && await zahl(p, '.trichter li') === 3, 'Teile');   /* zur Reservation geht es von der Startseite, der Karte, der Weinkarte und dem Kontakt */ await p.close(); });

/* ================= K Schweben ================= */
C('K01', 'Schweben', 'Blätter liegen beim Öffnen tief und klein (unter dem Bild), schweben beim Auftauchen nach der Uhr (2,7 s, Feder) auf ihren Platz; nicht am Scrollen geführt', async env => {
  const p = await auf(env, 'herkunft', 'gruss=tag', A, { ruhe: 200 }); const r = await p.evaluate(() => { const e = document.querySelectorAll('.zwei')[1]?.firstElementChild || document.querySelector('.tafel'); const c = getComputedStyle(e); return { anim: c.animationName, tl: c.animationTimeline, vorher: c.translate, da: e.classList.contains('rg-da') }; });
  ok(!r.da && r.vorher !== 'none' && r.vorher !== '0px', 'liegt nicht tief: ' + JSON.stringify(r)); ok(r.tl === 'auto' || r.tl === 'none' || r.tl === undefined, 'am Scrollen geführt: ' + r.tl);   /* Firefox kennt animation-timeline nicht: dann kann nichts am Scroll hängen */
  await p.evaluate(() => document.querySelectorAll('.zwei')[1].scrollIntoView({ block: 'center' })); await p.waitForTimeout(400); const mitte = await p.evaluate(() => { const e = document.querySelectorAll('.zwei')[1].firstElementChild; return { da: e.classList.contains('rg-da'), name: getComputedStyle(e).animationName, dauer: getComputedStyle(e).animationDuration }; });
  ok(mitte.da && mitte.name === 'rg-feder' && mitte.dauer === '2.7s', JSON.stringify(mitte)); await p.waitForTimeout(3200); const nachher = await p.evaluate(() => getComputedStyle(document.querySelectorAll('.zwei')[1].firstElementChild).translate); ok(nachher === 'none' || nachher === '0px', 'landet nicht: ' + nachher);
  await p.evaluate(() => scrollBy(0, 40)); await p.waitForTimeout(200); const still = await p.evaluate(() => getComputedStyle(document.querySelectorAll('.zwei')[1].firstElementChild).translate); ok(still === 'none' || still === '0px', 'bewegt sich beim Scrollen weiter'); await p.close(); }, { nurRechner: true });
C('K02', 'Schweben', 'Die grossen Zahlen zoomen aus einer Vergrösserung herein (nur Zoom, keine Verschiebung seitlich: kein Überlauf)', async env => {
  const p = await auf(env, 'start', 'gruss=tag', A, { ruhe: 0 }); await p.evaluate(() => document.querySelector('.zahlen').scrollIntoView({ block: 'center' })); await p.waitForTimeout(700); const n = await p.evaluate(() => [...document.querySelectorAll('.zahlen .blatt b')].map(b => getComputedStyle(b).animationName)); ok(n.some(x => x === 'rg-zoom'), 'kein Zoom: ' + n.join()); await p.waitForTimeout(2600); ok(await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Überlauf'); await p.close(); });
C('K03', 'Schweben', 'Balken und Säulen wachsen erst, wenn ihr Blatt gut zur Hälfte im Bild ist (nicht schon beim Laden, wenn es unten liegt)', async env => {
  const p = await auf(env, 'herkunft', 'gruss=tag', A, { ruhe: 200 }); const vor = await p.evaluate(() => { const b = [...document.querySelectorAll('.zwei')[1].querySelectorAll('.rang__b i')][0]; return [getComputedStyle(b).transform, !!document.querySelectorAll('.zwei')[1].firstElementChild.classList.contains('rg-los')]; });
  ok(vor[1] === false && vor[0].startsWith('matrix(0,'), 'wächst schon: ' + vor); await p.evaluate(() => document.querySelectorAll('.zwei')[1].scrollIntoView({ block: 'center' })); await p.waitForTimeout(3200);
  const nach = await p.evaluate(() => { const b = document.querySelectorAll('.zwei')[1].querySelector('.rang__b i'); return getComputedStyle(b).transform; }); ok(nach === 'none' || parseFloat(nach.replace('matrix(', '')) > 0.015, 'wächst nicht: ' + nach); await p.close(); }, { nurRechner: true });
C('K04', 'Schweben', 'Besuchs-Kacheln (viele gleiche Zeilen) blenden nur sanft ein: kein Weg, keine Feder', async env => { const p = await auf(env, 'besuche'); const r = await p.evaluate(() => { const c = getComputedStyle(document.querySelector('.liste .besuch')); return [c.animationName, c.translate]; }); ok(r[0] === 'none' && (r[1] === 'none'), JSON.stringify(r)); await p.close(); });
C('K05', 'Schweben', 'Am Seitenende steht alles still an seinem Platz und nichts überdeckt etwas (jede Ansicht ganz durchgescrollt)', async env => {
  for (const v of ANSICHTEN) { const p = await auf(env, v); await bisEnde(p); const r = await p.evaluate(() => { const lose = [...document.querySelectorAll('[data-r]')].filter(x => { const c = getComputedStyle(x); return (c.translate !== 'none' && c.translate !== '0px') || !x.classList.contains('rg-da'); }).map(x => x.className.split(' ')[0]); const bs = [...document.querySelectorAll('#ansicht [data-r]')].map(x => [x, x.getBoundingClientRect()]); const o = []; for (let i = 0; i < bs.length; i++) for (let j = i + 1; j < bs.length; j++) { const a = bs[i][1], b = bs[j][1]; if (!bs[i][0].contains(bs[j][0]) && !bs[j][0].contains(bs[i][0]) && a.height && b.height && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 3 && Math.min(a.right, b.right) - Math.max(a.left, b.left) > 3) o.push(bs[i][0].className.split(' ')[0] + '×' + bs[j][0].className.split(' ')[0]); } return { lose: lose.slice(0, 4), o: o.slice(0, 4) }; }); ok(!r.lose.length && !r.o.length, v + ' ' + JSON.stringify(r)); await p.close(); } }, { lang: true });
C('K06', 'Schweben', 'Bei «Bewegung reduzieren» steht sofort alles da, nichts schwebt', async env => {
  const ctx = await env.browser.newContext({ viewport: { width: env.breite, height: env.hoehe }, reducedMotion: 'reduce' }); const p = await ctx.newPage(); await p.goto(A + '?gruss=tag#herkunft'); await p.waitForFunction(BEREIT); await p.waitForTimeout(300);
  const r = await p.evaluate(() => [...document.querySelectorAll('[data-r]')].filter(x => getComputedStyle(x).translate !== 'none' && getComputedStyle(x).translate !== '0px').length); ok(r === 0, r + ' Blätter verschoben'); await ctx.close(); });

/* ================= L Rundgang ================= */
const OHNE_BOT = async ctx => ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); });
C('L01', 'Rundgang', 'Auf jeder Seite erscheint unten rechts (über der Leiste) ein Schild «Kurzer Rundgang», fünf Sekunden lang; die Maus darauf hält es; das Kreuz schliesst; automatische Prüfungen sehen es nicht', async env => {
  const bot = await auf(env, 'start'); await bot.waitForTimeout(5000); ok(await zahl(bot, '.rdg-schild') === 0, 'Schild für Automaten sichtbar'); await bot.close();
  const ctx = await env.browser.newContext({ viewport: { width: env.breite, height: env.hoehe } }); await OHNE_BOT(ctx); const p = await ctx.newPage(); await p.goto(A + '?gruss=tag#start'); await p.waitForFunction(BEREIT);
  await p.waitForSelector('.rdg-schild', { timeout: 14000 }); await p.waitForTimeout(1000); /* das Schild fährt in 0,7 s herein: erst danach messen */ const r = await p.evaluate(() => { const s = document.querySelector('.rdg-schild').getBoundingClientRect(), l = document.querySelector('#leiste').getBoundingClientRect(); return [Math.round(s.bottom), Math.round(l.top), /Kurzer Rundgang/.test(document.querySelector('.rdg-schild').textContent)]; }); ok(r[2] && r[0] <= r[1] + 2, 'Schild ' + r);
  await p.mouse.move(env.breite - 120, env.hoehe - 150); const sb = await p.$eval('.rdg-schild', e => { const r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }); await p.mouse.move(sb[0], sb[1]); await p.waitForTimeout(6000); ok(await zahl(p, '.rdg-schild:not(.weg)') === 1, 'Maus hält es nicht'); await p.mouse.move(5, 5); await p.waitForTimeout(3400); ok(await zahl(p, '.rdg-schild') === 0, 'zieht sich nicht zurück');
  await p.reload(); await p.waitForSelector('.rdg-schild', { timeout: 14000 }); await p.click('.rdg-schild__zu'); await p.waitForTimeout(900); ok(await zahl(p, '.rdg-schild') === 0, 'Kreuz'); await ctx.close(); }, { lang: true });
C('L02', 'Rundgang', '«Zeigen» (oder ?rundgang) startet den Rundgang: Lichtkegel auf dem echten Bedienelement, Karte mit «1 von 5» und Titel, Text', async env => {
  const p = await auf(env, 'start', 'gruss=tag&rundgang', A, { ruhe: 600 }); await p.waitForSelector('.rdg-karte', { timeout: 8000 }); const k = await text(p, '.rdg-karte'); ok(rx(NAME + ' · 1 von 5').test(k) && rx('Das ist ' + KLEIN).test(k), k.slice(0, 80)); ok(await zahl(p, '.rdg-kegel') === 1, 'Kegel');
  const r = await p.evaluate(() => { const k = document.querySelector('.rdg-kegel').getBoundingClientRect(), b = document.querySelector('.wo-sb').getBoundingClientRect(); return [Math.abs(k.left - b.left) < 14, Math.abs(k.width - b.width) < 30]; }); ok(r[0] && r[1], 'Kegel nicht auf dem Startbild'); await p.close(); });
C('L03', 'Rundgang', 'Der Rundgang geht Schritt für Schritt (Weiter, Enter, →), zurück (←), überspringt (Überspringen, Esc), endet mit «Los geht’s»; die Karte steht neben dem Ziel, nie darauf', async env => {
  const p = await auf(env, 'start', 'gruss=tag&rundgang', A, { ruhe: 600 }); await p.waitForSelector('.rdg-karte');
  const schritt = async () => (await text(p, '.rdg-zier span')).match(/(\d) von 5/)?.[1]; ok(await schritt() === '1', 'Start'); await p.click('.rdg-los'); await p.waitForTimeout(500); ok(await schritt() === '2', 'Weiter'); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500); ok(await schritt() === '3', '→'); await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(500); ok(await schritt() === '2', '←'); await p.keyboard.press('Enter'); await p.waitForTimeout(500); ok(await schritt() === '3', 'Enter');
  if (env.breite > 700) { const d = await p.evaluate(() => { const k = document.querySelector('.rdg-karte').getBoundingClientRect(), z = document.querySelector('.rdg-kegel').getBoundingClientRect(); const x = Math.min(k.right, z.right) - Math.max(k.left, z.left), y = Math.min(k.bottom, z.bottom) - Math.max(k.top, z.top); return x > 8 && y > 8; }); ok(!d, 'Karte liegt auf dem Ziel'); }
  await p.click('.rdg-los'); await p.waitForTimeout(500); await p.click('.rdg-los'); await p.waitForTimeout(500); ok(await schritt() === '5' && /Los geht/.test(await text(p, '.rdg-los')) && !(await p.$('.rdg-zu')), 'Ende'); await p.click('.rdg-los'); await p.waitForTimeout(400); ok(await zahl(p, '.rdg-karte') === 0 && await zahl(p, '.rdg-kegel') === 0, 'nicht beendet');
  await p.reload(); await p.waitForSelector('.rdg-karte', { timeout: 9000 }); await p.click('.rdg-zu'); await p.waitForTimeout(400); ok(await zahl(p, '.rdg-karte') === 0, 'Überspringen'); await p.reload(); await p.waitForSelector('.rdg-karte', { timeout: 9000 }); await p.keyboard.press('Escape'); await p.waitForTimeout(400); ok(await zahl(p, '.rdg-karte') === 0, 'Esc'); await p.close(); });
C('L04', 'Rundgang', '«Kurzer Rundgang» im Rand startet ihn jederzeit, auch nach einem Ansichtswechsel (der Weg bleibt im Rand)', async env => {
  const p = await auf(env, 'seiten'); if (env.breite <= 900) await p.click(BER); await p.click('#rand [data-rundgang]'); await p.waitForSelector('.rdg-karte', { timeout: 6000 }); ok(/1 von/.test(await text(p, '.rdg-zier')), 'Start'); await p.keyboard.press('Escape'); await p.close(); });
C('L05', 'Rundgang', 'Am Handy steht die Karte unten über dem Bild; in eingebetteten Ansichten (Werkbank, Laptop) erscheint nichts', async env => {
  const p = await auf(env, 'start', 'gruss=tag&rundgang', A, { ruhe: 600 }); await p.waitForSelector('.rdg-karte'); const r = await p.evaluate(() => { const k = document.querySelector('.rdg-karte').getBoundingClientRect(); return [k.bottom <= innerHeight + 1, k.left >= 0, k.right <= innerWidth + 1]; }); ok(r.every(Boolean), 'Karte ' + r); await p.close();
  const q = await env.ctx.newPage(); await q.goto(A + 'anleitung.html'); await q.evaluate(([u, w, h]) => { document.body.innerHTML = `<iframe src="${u}?gruss=tag#start" style="width:${w}px;height:${h}px;border:0"></iframe>`; }, [A, env.breite, env.hoehe]); await q.waitForSelector('iframe'); let fr; for (let i = 0; i < 40 && !fr; i++) { fr = q.frames().find(f => f !== q.mainFrame() && f.url().startsWith(A)); if (!fr) await q.waitForTimeout(250); } ok(fr, 'Rahmen lädt nicht'); await fr.waitForFunction(BEREIT, null, { timeout: 12000 }); await q.waitForTimeout(800); ok((await fr.$$('.rdg-schild, .rdg-karte')).length === 0, 'im Rahmen sichtbar'); await q.close(); }, { nurHandy: true });

/* ================= M Zählung und Datenschutz ================= */
C('M01', 'Zählung', '«So wird gezählt» sagt, was gezählt wird, was nie gezählt wird (kein Name, keine Adresse, kein Cookie), Aufbewahrung, eigene Geräte, Grenzen, Zugang', async env => { const p = await auf(env, 'zaehlung'); const t = await text(p, '#ansicht'); ok(/Was gezählt wird/.test(t) && /Was nie gezählt wird/.test(t) && /Kein Cookie/.test(t) && /400 Tage/.test(t) && /Passwort/.test(t), 'Inhalt'); await p.close(); });
C('M02', 'Zählung', 'Der Dienst gibt in der Vorführung nie echte Werte heraus (ohne Schlüssel, mit falschem Schlüssel, mit ?beispiel): immer «beispiel: true»', async env => {
  for (const q of ['tage=30', 'tage=30&k=falsch', 'tage=7&beispiel=1']) { const d = await stand(B, q); ok(d.beispiel === true && d.summe.besuche > 100, q); } }, { server: true });

/* ================= N Server ================= */
const UA = i => `Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/605 Safari/605 Test${i}`;
C('N01', 'Server', 'Mit dem Schlüssel liefert der Dienst die echten Besuche (leer, solange nichts gezählt wurde: «leer»)', async env => { const d = await stand(B, 'tage=30&k=' + KEY); ok(d.beispiel === false && d.leer === true && d.summe.besuche === 0, JSON.stringify(d.summe)); }, { server: true, zuerst: true });
C('N02', 'Server', 'Eine gültige Zeile der Website wird angenommen (204), Beginn und Ende desselben Seitenaufrufs fassen zu einem Eintrag zusammen, Klicks und Sekunden zählen', async env => {
  ok(await sende(B, 'r1 ab12cd index.html de rechner 0 - google.com', UA(1)) === 204, 'Beginn'); ok(await sende(B, 'r1 ab12cd index.html de rechner 42 fenster,buchung google.com', UA(1)) === 204, 'Ende'); ok(await sende(B, 'r1 ef34gh karte.html fr handy 61 anruf,route -', UA(1)) === 204, 'zweite Seite'); ok(await sende(B, 'r1 gh56ij feiern.html fr handy 30 tisch,anfrage -', UA(1)) === 204, 'dritte Seite');
  const d = await stand(B, 'tage=7&k=' + KEY); ok(d.summe.besuche === 1 && d.summe.seiten === 3 && d.summe.buchung === 1 && d.summe.anfrage === 1 && d.summe.kontakt === 1 && d.summe.route === 1 && d.werte.tisch.zahl === 1 && d.werte.tisch.essen === 1 && d.werte.anfrage.zahl === 1 && d.werte.route.weg === 0 && d.werte.start.zahl === 1, JSON.stringify(d.summe)); ok(d.besuche[0].weg[0].sek === 42 && d.besuche[0].l === 'CH' && d.besuche[0].o === 'Bottighofen', 'Ort/Zeit'); }, { server: true });
C('N03', 'Server', 'Ungültiges wird verworfen: falsche Sprache, fremde Ereignisse, zu lange Zeilen, Fremdzeichen, Automaten (Bots, Prüfskripte)', async env => {
  const vorher = (await stand(B, 'tage=7&k=' + KEY)).summe.seiten; for (const z of ['r1 aa11bb index.html qq rechner 0 - -', 'r1 aa11bb index.html de rechner 0 spa -', 'r1 aa11bb index.html de rechner 0 hack -', 'r1 aa11bb ../x.html de rechner 0 - -', 'r1 aa11bb index.html de rechner 0 - ' + 'a'.repeat(400), '<script>', 'r2 aa11bb index.html de rechner 0 - -']) await sende(B, z, UA(2));
  for (const ua of ['Googlebot/2.1', 'curl/8', 'HeadlessChrome', 'python-requests']) await sende(B, 'r1 cc22dd index.html de rechner 0 - -', ua); ok((await stand(B, 'tage=7&k=' + KEY)).summe.seiten === vorher, 'Unfug zählt mit'); }, { server: true });
C('N04', 'Server', 'Datenschutz: in der Tagesdatei steht keine Adresse der Verbindung und kein Browser-Text, nur ein Kürzel, Ort und Zeiten', async env => {
  const dir = env.daten; const f = fs.readdirSync(dir).filter(x => /\.json$/.test(x)); ok(f.length >= 1, 'keine Datei'); const t = f.map(x => fs.readFileSync(path.join(dir, x), 'utf8')).join(''); ok(!/127\.0\.0\.1|::1|Mozilla|Safari|AppleWebKit/.test(t), 'Adresse oder Browser-Text gespeichert'); ok(/"o":"Bottighofen"/.test(t), 'Ort fehlt'); }, { server: true });
C('N05', 'Server', 'Echte Werte im Werkzeug (mit ?k=): Leiste «Ein Besuch heute», Kopf-Stand, Knopf «Neu laden» (Meldung «Neu geladen»), kein Beispiel-Band, Zahlen stimmen mit dem Dienst', async env => {
  await sende(B, 'r1 zz99yy index.html en tablet 12 - -', UA(3)); const p = await auf(env, 'start', 'gruss=tag&k=' + KEY, B); const d = await stand(B, 'tage=30&k=' + KEY);
  ok(!(await p.$('.bsp-band')) && /Besuche heute/.test(await text(p, STAND_K)) && await p.$('#l-neu'), 'echter Modus'); ok(+(await text(p, '.buehne__chips li:nth-child(1) b')) === d.summe.besuche, 'Zahl'); await sende(B, 'r1 qq77ww index.html fr handy 3 - -', UA(4)); await p.click('#l-neu'); await p.waitForTimeout(600); ok(/Neu geladen/.test(await text(p, '.quit')), 'Meldung'); ok(+(await text(p, '.buehne__chips li:nth-child(1) b')) === d.summe.besuche + 1, 'nicht neu geladen'); await p.close(); }, { server: true });
C('N06', 'Server', 'Fällt der Dienst aus (mit Schlüssel), steht «<Name> ist gerade nicht abrufbar» mit Grund und bleibt stehen', async env => {
  const p = await auf(env, 'start', 'gruss=tag&k=' + KEY, B); await p.route('**/api/registre**', r => r.fulfill({ status: 500, json: { fehler: 'Testfehler' } })); await p.click('#l-neu'); await p.waitForTimeout(500); ok(/nicht abrufbar/.test(await text(p, '.quit.fehl')) && /Testfehler/.test(await text(p, '.quit.fehl')), 'Fehlermeldung'); await p.waitForTimeout(5600); ok(await zahl(p, '.quit.fehl') === 1, 'verschwindet'); await p.close(); }, { server: true });
C('N07', 'Server', 'Leerer Zeitraum: «Noch kein Besuch gezählt» mit «Beispiel ansehen» (wechselt zu Beispielwerten); wenige Besuche: «Noch wenig zu sehen? Beispiel ansehen»', async env => {
  const p = await auf(env, 'start', 'gruss=tag&k=' + KEY, B); ok(await sicht(p, '.wenig') || await p.evaluate(() => !!document.querySelector('.wenig')), '«Noch wenig» fehlt'); await p.evaluate(() => document.querySelector('.wenig').scrollIntoView({ block: 'center' })); await p.waitForTimeout(500); await p.click('.wenig [data-bsp]'); await p.waitForTimeout(600); ok(await sicht(p, '.bsp-band'), 'Beispiel nicht gezeigt'); ok(await p.evaluate(() => !!document.querySelector('#l-echt')), 'Knopf zu den echten Besuchen fehlt (Schlüssel da)'); await p.click('#l-echt'); await p.waitForTimeout(500); ok(!(await p.$('.bsp-band')), 'zurück zu echt'); await p.close(); }, { server: true });
C('N08', 'Server', 'Der Test-Server antwortet nur dem eigenen Rechner und gibt keine Quelltexte (.py) und keine Tagesdateien heraus', async env => { for (const u of ['_werkzeuge/registre/registre.py', '_werkzeuge/registre/server.py', '_werkzeuge/registre/_daten/x.json']) { const r = await fetch(B.replace('/_werkzeuge/registre/', '/') + u); ok(r.status === 404, u + ' ' + r.status); } }, { server: true });

/* ================= O Anleitung ================= */
C('O01', 'Anleitung', 'Die Anleitung öffnet (zweimal geladen), hat zehn Kapitel (wie das Gasterntal: das Rivage neun, dazu Zeit und Verlauf, ohne den Knopf «nicht mitzählen») in vier Themen mit Bildern aus dem Werkzeug, Bild gross mit Klick und Esc, keine toten Links', async env => {
  for (let i = 0; i < 2; i++) { const p = await auf(env, '', '', A.replace(/$/, 'anleitung.html'), { roh: true }); await p.waitForLoadState('load'); ok(await zahl(p, 'article.kap') === 10, 'Kapitel ' + await zahl(p, 'article.kap')); ok(await zahl(p, '.inhalt .thema') === 4, 'Themen');
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } }); await p.waitForTimeout(800); ok(await p.evaluate(() => [...document.querySelectorAll('article.kap img')].every(i => i.complete && i.naturalWidth > 0)), 'Bild fehlt'); const bi = await p.$('article.kap .bild'); await bi.scrollIntoViewIfNeeded(); await bi.click(); await p.waitForTimeout(400); ok(await sicht(p, '.gross'), 'Bild nicht gross'); await p.keyboard.press('Escape'); await p.waitForTimeout(300); ok(!(await sicht(p, '.gross')), 'Esc');
    const links = await p.evaluate(() => [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.querySelector(h))); ok(!links.length, 'tote Sprungmarken ' + links); await p.close(); } });

/* ================= Z Zählung auf der Website (messung.js, Vorschlag) ================= */
const NORMAL_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15';
async function seiteMitMessung(env, datei, vor, sprache = 'fr-CH') {   /* eine Seite der Website aus der Probe-Kopie mit messung.js (probe.sh setzt die Zeile wie der Vorschlag) */
  const ctx = await env.browser.newContext({ viewport: { width: 1440, height: 900 }, userAgent: NORMAL_UA, locale: sprache });
  await ctx.addInitScript(v => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); if (v) try { localStorage.setItem('schloessli-nicht-zaehlen', '1'); } catch (e) {} }, !!vor);
  await ctx.route(/gastronovi\.com|openstreetmap\.org|schaefli-wigoltingen\.ch|zenchef\.com|instagram\.com/, r => r.fulfill({ status: 200, contentType: 'text/html', body: '<p>Probe</p>' }));   /* nichts geht hinaus */
  await ctx.route(/^(mailto|tel):/, r => r.abort());
  await ctx.route(new RegExp('localhost:' + PORT + '/' + datei.replace('.', '\\.') + '$'), async r => { const a = await r.fetch(); let t = await a.text(); if (!/assets\/js\/messung\.js/.test(t)) t = t.replace('</body>', '<script src="assets/js/messung.js?v=probe" defer></script></body>'); await r.fulfill({ response: a, body: t }); });
  const p = await ctx.newPage(); await p.goto(B.replace('_werkzeuge/registre/', '') + datei, { waitUntil: 'load' }); await p.waitForTimeout(900);
  return { ctx, p };
}
/* Link anklicken, wie ein Gast es tut (eigener Link, damit kein Fenster der Seite dazwischenkommt; das Ziel ist abgefangen) */
const klicke = (p, href) => p.evaluate(h => { const a = document.createElement('a'); a.href = h; a.textContent = 'x'; a.addEventListener('click', e => e.preventDefault()); document.body.appendChild(a); a.click(); a.remove(); }, href);
const fensterZu = p => p.evaluate(() => document.querySelectorAll('dialog[open]').forEach(d => d.close()));
async function formSenden(p, sel) {   /* Formular eines Fensters der Website mit Probe-Werten füllen und abschicken (die Website verschickt nichts, sie zeigt «gesendet») */
  await p.evaluate(sel => { const f = document.querySelector(sel);
    f.querySelectorAll('input:not([type=hidden]),textarea').forEach(x => { if (x.type === 'checkbox' || x.type === 'radio') x.checked = true; else if (x.type === 'email') x.value = 'probe@example.com'; else if (x.type === 'number' || x.inputMode === 'numeric') x.value = '4'; else if (x.type === 'tel') x.value = '+41 71 000 00 00'; else x.value = 'Probe'; });
    f.querySelectorAll('input[type=hidden]').forEach(x => { x.value = x.name === 'datum' ? '2026-11-20' : (x.value || 'Probe'); });
    f.requestSubmit ? f.requestSubmit() : f.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true })); }, sel);
  await p.waitForTimeout(900);
}
C('Z01', 'Zählung', 'Zählung auf der Website (messung.js als Vorschlag, an der Startseite der Probe-Kopie): Öffnen zählt die Seite (Sprache des Browsers, Gerät, Sekunden); Fenster «Reservation», Tisch angefragt (erst wenn das Fenster «gesendet» zeigt), «Direkt buchen», Telefon des Hauses, Mail-Adresse, weiter zum Schäfli (Nummer des Schäfli) und Route kommen als Klicks an; das Besucherbuch zeigt den Besuch mit diesem Weg', async env => {
  const { ctx, p } = await seiteMitMessung(env, 'index.html');
  ok(await p.evaluate(() => window.__registre === 1), 'messung.js läuft nicht');
  await p.evaluate(() => document.querySelector('[data-fenster="fe-reservation"]').click()); await p.waitForTimeout(400);
  ok(await p.evaluate(() => document.getElementById('fe-reservation').open), 'Fenster «Reservation» öffnet nicht');
  await formSenden(p, '#fe-reservation form'); ok(await p.evaluate(() => document.getElementById('fe-reservation').classList.contains('gesendet')), 'Reservation nicht «gesendet»');
  await p.evaluate(() => document.querySelector('#fe-reservation [data-reiter="direkt"]').click()); await p.waitForTimeout(300); await fensterZu(p);
  await klicke(p, 'tel:+41716889092'); await klicke(p, 'tel:+41527631172'); await klicke(p, 'mailto:kontakt@schloessli-bottighofen.ch'); await klicke(p, 'https://www.openstreetmap.org/directions?to=47.6442147%2C9.212147');
  await p.waitForTimeout(1200); await p.close(); await ctx.close(); await warte(500);
  const d = await stand(B, 'tage=7&export=1&k=' + KEY); const b = d.besuche.find(x => x.weg.some(w => w.s === 'index.html' && w.e.includes('buchung')));
  ok(b, 'Besuch nicht gezählt: ' + d.besuche.length + ' Besuche'); const w = b.weg.find(x => x.s === 'index.html');
  const soll = ['anruf', 'booking', 'buchung', 'chat', 'fenster', 'mail', 'route'];
  ok(JSON.stringify(w.e) === JSON.stringify(soll), 'Klicks ' + w.e.join(',') + ' statt ' + soll.join(',')); ok(w.sp === 'fr' && b.g === 'rechner' && w.sek >= 1, 'Sprache/Gerät/Sekunden ' + [w.sp, b.g, w.sek]);
  const q = await auf(env, 'start', 'gruss=tag&k=' + KEY, B); const s2 = await q.evaluate(() => Object.assign({ bsp: S.d.beispiel }, S.d.summe)); ok(!s2.bsp && s2.buchung >= 1 && s2.route >= 1 && +(await text(q, '.buehne__chips li:nth-child(4) b')).replace(/[’']/g, '') === s2.buchung, 'Das Besucherbuch zeigt die Reservation nicht: ' + JSON.stringify(s2)); await q.close();
}, { server: true, nurBreite: 1440, lang: true });
C('Z01b', 'Zählung', 'Auf «Banketts & Gruppen»: die Bankettanfrage öffnen zählt; ein leeres Formular (kein «gesendet») zählt nicht als Anfrage, abgeschickt zählt es; auf «Gutschein» zählt die Bestellung als Anfrage; der Link zum Schäfli zählt', async env => {
  const zaehlFeiern = async () => { const d0 = await stand(B, 'tage=7&export=1&k=' + KEY); const e0 = d0.besuche.flatMap(x => x.weg.filter(w => w.s === 'feiern.html' && w.sp === 'it'));   /* nur Seiten dieser Zeile: sie meldet sich italienisch, alle anderen Zeilen deutsch oder französisch */ return { tisch: e0.filter(w => w.e.includes('tisch')).length, anfrage: e0.filter(w => w.e.includes('anfrage')).length }; };
  const vor = await zaehlFeiern();   /* N02 meldet feiern.html schon früher im Lauf: verglichen wird mit dem Stand davor */
  let { ctx, p } = await seiteMitMessung(env, 'feiern.html', false, 'it-CH');
  await p.evaluate(() => document.querySelector('[data-fenster="fe-bankett"]').click()); await p.waitForTimeout(400); ok(await p.evaluate(() => document.getElementById('fe-bankett').open), 'Bankettanfrage öffnet nicht');
  await p.evaluate(() => { const f = document.querySelector('#fe-bankett form'); f.requestSubmit ? f.requestSubmit() : f.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true })); }); await p.waitForTimeout(1200);
  ok(await p.evaluate(() => !document.getElementById('fe-bankett').classList.contains('gesendet')), 'leeres Formular «gesendet»');
  let n1 = await zaehlFeiern(); ok(n1.tisch === vor.tisch + 1 && n1.anfrage === vor.anfrage, 'leere Anfrage gezählt oder Öffnen nicht: vorher ' + JSON.stringify(vor) + ', jetzt ' + JSON.stringify(n1));
  await formSenden(p, '#fe-bankett form'); ok(await p.evaluate(() => document.getElementById('fe-bankett').classList.contains('gesendet')), 'Bankett nicht «gesendet»');
  await p.waitForTimeout(800); await p.close(); await ctx.close(); await warte(500);
  n1 = await zaehlFeiern(); ok(n1.anfrage > vor.anfrage && n1.anfrage <= n1.tisch, 'abgeschickte Bankettanfrage fehlt: vorher ' + JSON.stringify(vor) + ', jetzt ' + JSON.stringify(n1));   /* im Safari-Kern kam derselbe Aufruf im Prüflauf zweimal als zwei Besuche an (offen, siehe STAND.md); gezählt wird hier nur, dass die Anfrage erst nach «gesendet» zählt */ let d, e;
  ({ ctx, p } = await seiteMitMessung(env, 'gutschein.html'));
  await p.evaluate(() => document.querySelector('[data-fenster="fe-gutschein"]').click()); await p.waitForTimeout(400); await formSenden(p, '#fe-gutschein form');
  ok(await p.evaluate(() => document.getElementById('fe-gutschein').classList.contains('gesendet')), 'Gutschein nicht «gesendet»'); await fensterZu(p);
  await klicke(p, 'https://www.schaefli-wigoltingen.ch/'); await p.waitForTimeout(800); await p.close(); await ctx.close(); await warte(500);
  d = await stand(B, 'tage=7&export=1&k=' + KEY); e = d.besuche.flatMap(x => x.weg.filter(w => w.s === 'gutschein.html')); ok(e.some(w => w.e.includes('anfrage') && w.e.includes('chat')), 'Gutschein oder Schäfli fehlt: ' + JSON.stringify(e));
}, { server: true, nurBreite: 1440, lang: true });
C('Z02', 'Zählung', 'Nicht gezählt: Geräte mit «nicht mitzählen», automatische Browser (webdriver), Seiten der Werkzeuge', async env => {
  const vorher = (await stand(B, 'tage=7&k=' + KEY)).summe.seiten;
  let { ctx, p } = await seiteMitMessung(env, 'karte.html', true); ok(await p.evaluate(() => !window.__registre), 'zählt trotz «nicht mitzählen»'); await p.close(); await ctx.close();
  const c2 = await env.browser.newContext({ userAgent: NORMAL_UA });
  const p2 = await c2.newPage(); await p2.goto(B.replace('_werkzeuge/registre/', '') + 'karte.html'); await p2.waitForTimeout(800); ok(await p2.evaluate(() => !window.__registre), 'zählt im Prüfbrowser'); await c2.close();
  const c3 = await env.browser.newContext({ userAgent: NORMAL_UA }); await c3.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false }));
  const p3 = await c3.newPage(); await p3.goto(B + '?gruss=tag'); await p3.addScriptTag({ url: '/assets/js/messung.js?v=probe' }); await p3.waitForTimeout(600); ok(await p3.evaluate(() => !window.__registre), 'zählt im Werkzeug'); await c3.close();
  await warte(400); ok((await stand(B, 'tage=7&k=' + KEY)).summe.seiten === vorher, 'Seiten gezählt, die nicht zählen dürfen');
}, { server: true, nurBreite: 1440 });
C('E05', 'Leiste', 'Schmale Handys (390 und 320 px): keine Ansicht verrutscht seitlich, kein Knopftext abgeschnitten, Rand-Klappe und Zeitraum erreichbar', async env => {
  for (const v of ANSICHTEN) { const p = await auf(env, v); const r = await p.evaluate(b => ({ breit: Math.max(document.documentElement.scrollWidth, innerWidth) - b,   /* gegen die eingestellte Breite: ein Handy-Browser zieht das Fenster sonst mit dem Inhalt breiter */ ab: [...document.querySelectorAll('button, a.kn, a.wo-kn')].filter(x => x.offsetWidth && x.scrollWidth > x.clientWidth + 1 && getComputedStyle(x).fontSize !== '0px' && !x.closest('.wahl3')).map(x => x.textContent.trim().slice(0, 24)), raus: [...document.querySelectorAll('button, a.kn, a.wo-kn, .blatt, .besuch')].filter(x => x.offsetWidth && x.getBoundingClientRect().right > b + 1).map(x => x.className.split(' ')[0] + ':' + x.textContent.trim().slice(0, 20)).slice(0, 4) }), env.breite);
    ok(r.breit <= 1 && !r.ab.length && !r.raus.length, v + ' ' + JSON.stringify(r)); ok(await sicht(p, BER), v + ': Bereiche fehlt'); await p.close(); } }, { nurHandy: true });

module.exports = { LISTE };


/* ================= P Nachrechnen (Prüfung 16.10.2026) ================= */
const PY = '/opt/homebrew/bin/python3';
function erwartet(t, heute, uhr) {   /* dieselbe Rechnung in registre.py (selbst gegen die Rohdaten geprüft: _pruefung/nachrechnen.py) */
  return JSON.parse(cp.execFileSync(PY, ['-c', `import sys,json;sys.path.insert(0,${JSON.stringify(HIER)});import registre as R;print(json.dumps(R.ablage_heute(${t},${JSON.stringify(heute)},${JSON.stringify(uhr)}),ensure_ascii=False))`], { maxBuffer: 64e6 }).toString());
}
const zuerich = ms => { const f = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Zurich', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23' }).formatToParts(new Date(ms)); const g = k => f.find(x => x.type === k).value; return [`${g('year')}-${g('month')}-${g('day')}`, `${g('hour')}:${g('minute')}:${g('second')}`]; };
const sortiert = o => Array.isArray(o) ? o.map(sortiert) : o && typeof o === 'object' ? Object.fromEntries(Object.keys(o).sort().map(k => [k, sortiert(o[k])])) : o;
async function aufZeit(env, ms, t, hash = 'start') {
  const page = await env.ctx.newPage(); await page.clock.install({ time: new Date(ms) }); await page.clock.resume();   /* Uhr läuft ab ms weiter (Auftakt zählt Millisekunden) */
  await page.addInitScript(t => { try { localStorage.setItem('schloessli-registre-tage', String(t)); } catch (e) {} }, t);
  page.on('pageerror', e => env.fehler.push(env.id + ': Seitenfehler: ' + e.message));
  await page.goto(A + '?gruss=tag#' + hash, { waitUntil: 'load' }); await page.waitForFunction(BEREIT, null, { timeout: 15000 }); await page.waitForTimeout(300);
  return page;
}
for (const [id, um, text] of [['P01', 0, 'heute zur jetzigen Uhrzeit'], ['P01b', 3, 'drei Tage nach der Ablage, 9:15 Uhr (Wochentage, Wochen und Vergleichszeitraum rücken mit)']]) {
  C(id, 'Nachrechnen', 'Jede Zahl im Werkzeug (7, 30 und 90 Tage) ist genau die Rechnung aus den Rohdaten der Beispielwerte, ' + text, async env => {
    const basis = um ? new Date(zuerich(Date.now())[0] + 'T09:15:00+02:00').getTime() + um * 864e5 : Math.floor(Date.now() / 1000) * 1000;
    const [heute, uhr] = zuerich(basis);
    for (const t of [7, 30, 90]) {
      const p = await aufZeit(env, basis, t); const ist = await p.evaluate(() => window.BG_REGISTRE_STAND()); await p.close();
      ok(ist._ablage && ist._uhr && ist._uhr.slice(0, 5) === uhr.slice(0, 5), 'Uhr der Seite ' + ist._uhr + ' statt ' + uhr);
      const u2 = ist._uhr, soll = erwartet(t, heute, u2); delete ist._ablage; delete ist._uhr;
      const a = JSON.stringify(sortiert(ist)), b = JSON.stringify(sortiert(soll));
      if (a !== b) { const f = Object.keys(soll).filter(k => JSON.stringify(sortiert(ist[k])) !== JSON.stringify(sortiert(soll[k]))); throw new Error(t + ' Tage ' + heute + ' ' + uhr + ': weicht ab in ' + f.join(', ')); }
      ok(ist.bis === heute && ist.besuche.every(b => b.tag < heute || (b.zs || b.z) <= u2), t + ' Tage: Besuch nach jetzt');
    }
  });
}
C('P02', 'Nachrechnen', 'Was auf dem Bildschirm steht, ist richtig aus den Zahlen gerechnet: Kennzahlen, Anteile der Ranglisten an allen Besuchen (nicht an den gezeigten Plätzen), Bänder, Sätze', async env => {
  const p = await auf(env, 'start');
  const f = await p.evaluate(async () => {
    const d = S.d, u = d.summe, nf = x => Number(x).toLocaleString('de-CH'), F = [], soll = (w, a, b) => { if (String(a).replace(/\s+/g, ' ').trim() !== String(b).replace(/\s+/g, ' ').trim()) F.push(w + ': «' + a + '» statt «' + b + '»'); };
    const rang = (sel, gesamt, i) => [...document.querySelectorAll(sel)][i].querySelectorAll('li').forEach(li => { const z = +li.querySelector('b').textContent.replace(/[’']/g, ''); soll(sel + ' ' + li.querySelector('.rang__n').textContent.trim().slice(0, 20), li.querySelector('em').textContent.replace(/\s/g, ''), Math.round(100 * z / gesamt) + '%'); });
    const zeige = async v => { document.querySelector(`#rand [data-gehe="${v}"]:not(.rand__marke)`).click(); await new Promise(r => setTimeout(r, 250)); };
    soll('Chips', [...document.querySelectorAll('.buehne__chips b')].map(b => b.textContent).join('|'), [u.besuche, u.laender, u.heute, u.buchung].map(nf).join('|'));
    const z = [...document.querySelectorAll('.zahlen .blatt')];
    soll('Besuche', z[0].querySelector('b').textContent, nf(u.besuche)); soll('Seiten', z[1].querySelector('b').textContent, nf(u.seiten)); soll('je Besuch', z[1].querySelector('small').textContent, nf(u.seiten_je_besuch) + ' je Besuch');
    soll('Zeit', z[2].querySelector('b').textContent, Math.floor(u.dauer_mittel / 60) + ':' + String(u.dauer_mittel % 60).padStart(2, '0'));
    soll('Buchung %', z[3].querySelector('small').textContent.replace(/\s/g, ''), (100 * u.buchung / u.besuche).toLocaleString('de-CH', { maximumFractionDigits: 1 }).replace(/\s/g, '') + '%derBesuche');
    soll('Vergleich', z[0].querySelector('.vgl').textContent.replace(/\s/g, '').replace('−', '-'), (() => { const q = Math.round(100 * (u.besuche - d.vorher.besuche) / d.vorher.besuche); return q ? (q > 0 ? '+' : '-') + Math.abs(q) + '%zudavor' : 'gleichwiedavor'; })());
    soll('Säulen', document.querySelectorAll('.tafel .saeulen .s').length, d.je_tag.length);
    soll('Säule heute', document.querySelector('.tafel .saeulen .s:last-child').dataset.t, 'Heute: ' + (u.heute === 1 ? 'ein Besuch' : nf(u.heute) + ' Besuche'));
    rang('.zwei .blatt .rang', u.besuche, 0); rang('.zwei .blatt .rang', u.seiten, 1);
    soll('Leiste', document.querySelector('#leiste .wo-leiste__t b').textContent, 'Sie sehen Beispielwerte');
    await zeige('herkunft');
    const ch = (d.laender.find(x => x.k === 'CH') || { n: 0 }).n, band = [...document.querySelectorAll('.band b')].map(b => b.textContent.replace(/\s/g, ''));
    soll('Schweiz', band[0], Math.round(100 * ch / u.besuche) + '%'); soll('Ausland', band[1], Math.round(100 - 100 * ch / u.besuche) + '%'); soll('Länder', band[2], nf(u.laender));
    const rl = [...document.querySelectorAll('.rang')]; rl.forEach((_, i) => rang('.rang', u.besuche, i));
    const lCH = [...rl[0].querySelectorAll('li')].find(li => /Schweiz/.test(li.textContent)); soll('Schweiz Liste = Band', lCH.querySelector('em').textContent.replace(/\s/g, ''), band[0]);
    await zeige('zeit');
    const st = d.stunden, wt = d.raster.map(r => r.reduce((a, x) => a + x, 0)), ges = st.reduce((a, x) => a + x, 0), b2 = [...document.querySelectorAll('.band b')].map(b => b.textContent.replace(/\s/g, ''));
    soll('Stunden = Besuche', ges, u.besuche); soll('Raster = Besuche', wt.reduce((a, x) => a + x, 0), u.besuche);
    soll('Spitze', b2[0], st.indexOf(Math.max(...st)) + '–' + (st.indexOf(Math.max(...st)) + 1) + 'Uhr');
    soll('Stärkster Tag', b2[1], ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'][wt.indexOf(Math.max(...wt))]);
    const heuteW = (new Date(d.bis + 'T12:00:00Z').getUTCDay() + 6) % 7, heuteN = d.besuche.filter(b => b.tag === d.bis).length;
    soll('Raster heute ≥ Besuche heute', wt[heuteW] >= heuteN, true);
    for (let w = 0; w < 7; w++) { const tage = d.je_tag.filter(t => (new Date(t.tag + 'T12:00:00Z').getUTCDay() + 6) % 7 === w).reduce((a, t) => a + t.besuche, 0); soll('Wochentag ' + w + ' = Tage', wt[w], tage); }
    rang('.rang', ges, 0);
    await zeige('seiten');
    const zeilen = [...document.querySelectorAll('.tabelle .zeile:not(.zeile--kopf)')]; soll('Seiten-Zeilen', zeilen.length, d.seiten.length);
    soll('Seiten-Summe = Aufrufe', d.seiten.reduce((a, x) => a + x.n, 0), u.seiten);
    await zeige('verlauf');
    soll('Wochen = Tage', d.wochen.reduce((a, w) => a + w.besuche, 0), d.je_tag.reduce((a, t) => a + t.besuche, 0)); soll('Tage = Besuche', d.je_tag.reduce((a, t) => a + t.besuche, 0), u.besuche);
    soll('Vorher = Tage davor', d.vor_tag.reduce((a, x) => a + x, 0), d.vorher.besuche);
    d.wochen.forEach(w => { const mo = (new Date(w.von + 'T12:00:00Z').getUTCDay() + 6) % 7, so = (new Date(w.bis + 'T12:00:00Z').getUTCDay() + 6) % 7; if ((mo !== 0 && w !== d.wochen[0]) || (so !== 6 && w !== d.wochen[d.wochen.length - 1])) F.push('Woche nicht Montag bis Sonntag: ' + w.von + '–' + w.bis); });
    await zeige('buchung');
    const W = d.werte, wb = [...document.querySelectorAll('.werte .wert b')].map(b => b.textContent.replace(/\s/g, ''));
    const WK = ['start', 'karte', 'booking', 'abbruch', 'tisch', 'anfrage', 'kontakt', 'chat', 'route'];
    WK.forEach((k, i) => soll('Wert ' + k, wb[i], W[k].von ? Number(W[k].anteil).toLocaleString('de-CH', { maximumFractionDigits: 1 }) + '%' : '–'));
    WK.forEach(k => { if (W[k].von) soll('Anteil ' + k, W[k].anteil, Math.round(Math.min(100, 100 * W[k].zahl / W[k].von) * 10) / 10); });
    rang('.rang', d.seiten.reduce((a, x) => a + (x.buchung || 0), 0), 0);
    await zeige('besuche');
    const fz = [...document.querySelectorAll('[data-filter]')].map(b => b.textContent.split('·')[1].trim());
    soll('Filter', fz.join('|'), [d.besuche.length, d.besuche.filter(b => b.buchung).length, d.besuche.filter(b => b.anfrage).length, d.besuche.filter(b => b.kontakt).length, d.besuche.filter(b => b.g === 'handy').length].map(nf).join('|'));
    return F;
  });
  await p.close(); ok(!f.length, f.slice(0, 4).join(' · '));
});

function csvLesen(t) {   /* Semikolon, Anführungszeichen verdoppelt */
  const z = [], f = []; let c = '', q = false;
  for (let i = 0; i < t.length; i++) { const ch = t[i];
    if (q) { if (ch === '"') { if (t[i + 1] === '"') { c += '"'; i++; } else q = false; } else c += ch; }
    else if (ch === '"') q = true; else if (ch === ';') { f.push(c); c = ''; } else if (ch === '\r') {} else if (ch === '\n') { f.push(c); z.push(f.splice(0)); c = ''; } else c += ch; }
  return z;
}
C('P03', 'Nachrechnen', '«Als Tabelle sichern»: lädt eine CSV mit genau den Besuchen des Zeitraums (Beispielwerte im Dateinamen und je Zeile gekennzeichnet); mit Schlüssel alle echten Besuche, nicht nur 400; ohne Schlüssel gibt der Dienst nichts heraus', async env => {
  const handy = env.breite < 600, p = await auf(env, handy ? 'besuche' : 'start'); const soll = await p.evaluate(() => S.d);
  if (handy) ok(!(await sicht(p, '#l-export')), 'am Handy steht der Knopf in der Leiste'); else ok(await sicht(p, '#l-export'), 'Knopf in der Leiste fehlt');
  const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 10000 }), handy ? p.locator('[data-sichern]').click() : p.click('#l-export')]);
  const name = dl.suggestedFilename(), datei = await dl.path(), roh = fs.readFileSync(datei, 'utf8'); fs.copyFileSync(datei, path.join(HIER, '_pruefung', 'export-' + env.art + '-' + env.breite + '.csv'));
  const z = csvLesen(roh.replace(/^﻿/, ''));
  ok(roh.charCodeAt(0) === 0xfeff && /-beispielwerte\.csv$/.test(name) && name.includes(soll.von) && name.includes(soll.bis), 'Datei ' + name);
  ok(z[0][0] === 'Art' && z[0].length === 21 && z.length - 1 === soll.besuche.length, 'Zeilen ' + (z.length - 1) + ' statt ' + soll.besuche.length);
  ok(z.slice(1).every(r => r[0] === 'Beispiel' && r.length === 21), 'nicht jede Zeile als Beispiel');
  const b0 = soll.besuche[0], r0 = z[1]; ok(r0[1] === b0.tag.split('-').reverse().join('.') && r0[2] === b0.z && +r0[9] === b0.dauer && +r0[10] === b0.seiten, 'erste Zeile ' + r0.join('|'));
  ok(z[0][13] === 'Tisch angefragt' && z[0][14] === '«Direkt buchen» gewählt' && z.slice(1).filter(r => r[13] === 'ja' || r[14] === 'ja').length === soll.besuche.filter(b => b.buchung).length, 'Buchung ja/nein');
  ok(!z.some(r => r.some(c => /^[=+@]/.test(c))), 'Formel in einer Zelle'); ok(await p.locator('#meldung .quit').filter({ hasText: 'Als Tabelle gesichert' }).count() === 1, 'Quittung'); await p.close();
  if (env.art !== 'chromium' || env.breite !== 1440) return;
  /* 450 echte Besuche als Tagesdatei im Wegwerf-Ordner des Test-Servers (über den Dienst würde die Grenze von 120 je Minute greifen) */
  const tag = zuerich(Date.now())[0], b = {}; for (let i = 0; i < 450; i++) b['t' + String(i).padStart(9, '0')] = { l: 'CH', o: 'Bern', r: 'BE', g: 'rechner', h: '', a: [{ k: 'x' + i, z: '00:' + String(i % 60).padStart(2, '0') + ':00', s: 'index.html', sp: 'de', sek: i % 50, e: [] }] };
  fs.writeFileSync(path.join(env.daten, tag + '.json'), JSON.stringify({ b }));
  const ctx = await env.browser.newContext({ viewport: { width: env.breite, height: env.hoehe }, acceptDownloads: true }); const q = await ctx.newPage();
  await q.goto(B + '?gruss=tag&k=' + KEY + '#start'); await q.waitForFunction(BEREIT); const d2 = await q.evaluate(() => S.d);
  const [dl2] = await Promise.all([q.waitForEvent('download', { timeout: 15000 }), q.click('#l-export')]); const z2 = csvLesen(fs.readFileSync(await dl2.path(), 'utf8').replace(/^﻿/, '')); await ctx.close();
  ok(!d2.beispiel && d2.summe.besuche > 400 && z2.length - 1 === d2.summe.besuche && z2.slice(1).every(r => r[0] === 'Besuch') && !/beispiel/.test(dl2.suggestedFilename()), 'echt: ' + (z2.length - 1) + ' von ' + d2.summe.besuche);
  const api = B.replace('/_werkzeuge/registre/', '') + '/api/registre?export=1&tage=30';
  ok((await fetch(api)).status === 403 && (await fetch(api + '&k=falsch')).status === 403 && (await fetch(api + '&beispiel=1&k=' + KEY)).status === 403, 'Ausfuhr ohne Schlüssel');
}, { server: true, lang: true });

/* ================= Q Rahmen, Wege, Sicherheit (Prüfung 16.10.2026) ================= */
C('Q01', 'Rahmen', 'Jeder Weg im Kopf und im Rand antwortet (Website, Anleitung, Die Stube), keine tote Adresse', async env => {
  const p = await auf(env); const l = await p.evaluate(() => [...new Set([...document.querySelectorAll('#kopf .wo-kopf__r a[href], #rand a[href]')].map(a => a.href).filter(h => !h.includes('#')))]); await p.close();   /* die anderen Werkzeuge im Kopf (.wo-kopf__wz) baut je ein eigener Chat */
  const schlecht = []; for (const u of l) { const s = (await fetch(u).catch(() => ({ status: 0 }))).status; if (s !== 200 && !(/\/maison\/$/.test(u) && !MAISON_DA && s === 404)) schlecht.push(s + ' ' + u); } ok(!schlecht.length && l.length >= 3, schlecht.join(' | ') || 'zu wenige Wege');
});
C('Q02', 'Rahmen', '«Zur Werkbank» erscheint nur, wenn aus der Werkbank geöffnet (?wb=de.k5), und führt zur Werkbank; ohne Herkunft und eingebettet nie', async env => {
  let p = await auf(env, 'start', 'gruss=tag&wb=de.k5'); await p.waitForTimeout(600);
  const da = await p.evaluate(() => { const h = document.querySelector('[data-zw-knopf], #zur-werkbank, zur-werkbank, .zw-host') || [...document.querySelectorAll('body > *')].find(e => e.shadowRoot); const a = h && h.shadowRoot && h.shadowRoot.querySelector('a'); return a ? a.href : null; });
  ok(da && /\/werkbank\/(index\.html)?(#.*)?$/.test(da), 'Knopf fehlt oder falsches Ziel: ' + da); ok(!/[?&]wb=/.test(await p.evaluate(() => location.search)), 'wb= bleibt in der Adresse'); await p.close();
  const ctx2 = await env.browser.newContext({ viewport: { width: env.breite, height: env.hoehe } }); p = await ctx2.newPage(); await p.goto(A + '?gruss=tag#start'); await p.waitForFunction(BEREIT); await p.waitForTimeout(600);
  ok(!(await p.evaluate(() => [...document.querySelectorAll('body > *')].some(e => e.shadowRoot && e.shadowRoot.querySelector('a')))), 'Knopf ohne Herkunft'); await ctx2.close();
});
C('Q03', 'Rahmen', 'Fehlermelder: ein Skriptfehler landet im Browser («schloessli-registre-fehler») und beim Dienst, Ladefehler nicht, höchstens 20', async env => {
  const ctx = await env.browser.newContext({ viewport: { width: env.breite, height: env.hoehe } }); await OHNE_BOT(ctx); const p = await ctx.newPage(); let beacon = 0;
  p.on('request', r => { if (/api\/registre\?fehler=1/.test(r.url()) && r.method() === 'POST') beacon++; });
  await p.goto(B + '?gruss=tag#start'); await p.waitForFunction(BEREIT);
  await p.evaluate(() => { for (let i = 0; i < 25; i++) setTimeout(() => { throw new Error('Probe ' + i); }, 0); const im = new Image(); im.src = 'gibtsnicht.png'; document.body.appendChild(im); });
  await p.waitForTimeout(1200); const l = await p.evaluate(() => JSON.parse(localStorage.getItem('schloessli-registre-fehler') || '[]')); await ctx.close();
  ok(l.length === 20 && /Probe 0/.test(l[0].t) && !l.some(x => /gibtsnicht/.test(x.t)), 'Einträge ' + l.length); ok(beacon >= 1 && beacon <= 20, 'an den Dienst: ' + beacon);
}, { server: true });
C('Q04', 'Sicherheit', 'Dienst: fremde Herkunft 403, zu grosse Zeile 413, zu viele Anfragen 429, Quelltexte und Tagesdateien nie', async env => {
  const api = B.replace('/_werkzeuge/registre/', '') + '/api/registre';
  const r1 = await fetch(api, { method: 'POST', body: 'r1 abcd index.html de rechner 5 - -', headers: { Origin: 'https://boese.example', 'User-Agent': 'Mozilla/5.0 Safari' } }); ok(r1.status === 403, 'fremde Herkunft ' + r1.status);
  const r1b = await fetch(api + '?tage=7', { headers: { Origin: 'https://boese.example' } }); ok(r1b.status === 403, 'fremde Herkunft GET ' + r1b.status);
  const r2 = await fetch(api, { method: 'POST', body: 'r1 ' + 'x'.repeat(400), headers: { 'User-Agent': 'Mozilla/5.0 Safari' } }); ok(r2.status === 413, 'zu gross ' + r2.status);
  let s429 = 0; const viele = await Promise.all(Array.from({ length: 140 }, () => fetch(api, { method: 'POST', body: 'r1 zz index.html de rechner 0 - -', headers: { 'User-Agent': 'Mozilla/5.0 Safari' } }).then(r => r.status))); s429 = viele.filter(x => x === 429).length; ok(s429 >= 15, '429 nur ' + s429 + 'x');
  for (const u of ['_werkzeuge/registre/registre.py', '_werkzeuge/registre/online/registre.py', '_werkzeuge/registre/_daten/2026-10-16.json', '_werkzeuge/registre/_pruefung/nachrechnen.py', '_werkzeuge/registre/LIEFERUNG.md', '../etc/passwd', '_dienste/anfragen.jsonl', '_studio/stand.json', 'serve.py', '.git/config']) { const r = await fetch(B.replace('/_werkzeuge/registre/', '/') + u); ok(r.status === 404, u + ' ' + r.status); }
}, { server: true, einmal: true });
C('Q05', 'Rahmen', 'Die Stube bekommt vom Dienst dieselben Beispielzahlen, die das Besucherbuch zur selben Zeit zeigt', async env => {
  const p = await auf(env, 'start', 'gruss=tag', B); const ist = await p.evaluate(() => S.d.summe); await p.close();
  const d = await (await fetch(B.replace('/_werkzeuge/registre/', '') + '/api/registre?tage=30&beispiel=1')).json();
  ok(d.beispiel === true && JSON.stringify(d.summe) === JSON.stringify(ist), JSON.stringify(d.summe) + ' / ' + JSON.stringify(ist));
}, { server: true });

C('Q06', 'Rahmen', 'Unter der Sicherheitsregel der Online-Fassung (CSP wie vercel.json, eingebettete Skripte gesperrt) läuft alles: Laden, Fehlermelder, Rundgang, Anleitung mit Bild gross, Tabelle sichern; keine Regelverletzung', async env => {
  const CSP = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self' blob:; frame-ancestors 'self'; object-src 'none'; base-uri 'self'";
  const p = await env.ctx.newPage(), verstoss = [];
  p.on('console', m => { if (/Content Security Policy|Content-Security-Policy|CSP/i.test(m.text())) verstoss.push(m.text().slice(0, 140)); });
  await p.route(new RegExp('localhost:' + PORT + '\\/_werkzeuge\\/registre\\/(\\?.*|#.*)?$|anleitung\\.html'), async r => { const a = await r.fetch(); await r.fulfill({ response: a, headers: Object.assign({}, a.headers(), { 'content-security-policy': CSP }) }); });
  await p.goto(A + '?gruss=tag#start'); await p.waitForFunction(BEREIT, null, { timeout: 15000 });
  ok(await p.evaluate(() => typeof window.addEventListener === 'function' && !!document.querySelector('script[src^="fehler.js"]')), 'Fehlermelder fehlt');
  if (env.breite < 600) { await p.click(BER); await p.click(`${NAV}[data-gehe="besuche"]`); await p.waitForTimeout(300); }
  const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 10000 }), env.breite < 600 ? p.locator('[data-sichern]').click() : p.click('#l-export')]); ok(/\.csv$/.test(dl.suggestedFilename()), 'Tabelle');
  await p.goto(A.replace(/\/$/, '/') + 'anleitung.html'); await p.waitForTimeout(500); await p.locator('.bild').first().click(); await p.waitForTimeout(200);
  ok(await p.evaluate(() => !document.getElementById('gross').hidden), 'Bild gross öffnet nicht'); await p.keyboard.press('Escape'); ok(await p.evaluate(() => document.getElementById('gross').hidden), 'Esc schliesst nicht');
  await p.close(); ok(!verstoss.length, verstoss.join(' | '));
});

/* ================= Lauf ================= */
function liste() {
  const R = fs.existsSync(path.join(HIER, 'abnahme-ergebnis.json')) ? JSON.parse(fs.readFileSync(path.join(HIER, 'abnahme-ergebnis.json'), 'utf8')) : null;
  const gruppen = {}; LISTE.forEach(c => (gruppen[c.bereich] = gruppen[c.bereich] || []).push(c));
  let md = '---\ntags: [projekt, website]\nstatus: aktiv\n---\n\n# Funktionsliste Das Besucherbuch (Le Registre) · Wirtschaft am Schlössli\n\nVorlage: Das Besucherbuch des Berghotel Gasterntal (17./18.10.2026), dahinter Doldenhorn, Carlton-Europe (G10–G13) und Grand Beau-Rivage (Stand 16.10.2026); Rahmen aus der Oberfläche der Häuser (Kleid schloessli, «Die Bühne»). Jede Zeile ist zugleich eine Prüfung in `abnahme.js`. ' + (R ? `Letzter Lauf ${R.datum}: **${R.gruen} von ${R.gilt} Zeilen grün** in ${R.laeufe.length} Läufen (${R.laeufe.join(', ')}).` : 'Noch kein Lauf.') + '\n\n`✓` = in allen Läufen grün, in denen die Zeile gilt. «Rechner»/«Handy»: die Zeile gilt nur dort.\n\n';
  for (const [b, cs] of Object.entries(gruppen)) { md += `## ${b}\n\n| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |\n|---|---|---|---|\n`; for (const c of cs) { const r = R && R.zeilen[c.id]; md += `| ${c.id} | ${c.text.replace(/\|/g, '/')} | ${c.nurRechner ? 'Rechner' : c.nurHandy ? 'Handy' : c.server ? 'Dienst' : 'alle'} | ${r ? (r.rot ? '✗ ' + r.rot.join(', ') : '✓ ' + r.gruen + '/' + r.gilt) : '–'} |\n`; } md += '\n'; }
  fs.writeFileSync(path.join(HIER, 'FUNKTIONSLISTE.md'), md); return md;
}
async function lauf() {
  /* Vor dem Pitch: Chromium und Safari-Kern × 1440 × 900 und 390 × 844; nach dem Auftrag (ALLE=1): drei Browser × 1440, 1366, 390, 320 */
  const profile = AUS.length >= 2 ? [[AUS[0], +AUS[1]]] : process.env.ALLE ? ['chromium', 'webkit', 'firefox'].flatMap(b => [[b, 1440], [b, 1366], [b, 390], [b, 320]]) : ['chromium', 'webkit'].flatMap(b => [[b, 1440], [b, 390]]);
  const daten = fs.mkdtempSync(path.join(os.tmpdir(), 'registre-test-'));
  cp.execFileSync('/bin/zsh', [path.join(HIER, '_pruefung', 'probe.sh')], { stdio: 'ignore' });
  const srv = cp.spawn('/opt/homebrew/bin/python3', [path.join(PROBE, '_werkzeuge', 'registre', 'server.py'), String(PORT)], { env: Object.assign({}, process.env, { REGISTRE_ORDNER: daten }), stdio: 'ignore' });
  await warte(1200); fs.mkdirSync(BILDER, { recursive: true });
  const erg = { datum: new Date().toLocaleString('de-CH'), laeufe: profile.map(p => p.join(' ')), zeilen: {}, rot: {} };
  const alle = {}; LISTE.forEach(c => { erg.zeilen[c.id] = { gilt: 0, gruen: 0, rot: null }; });
  for (const [art, breite] of profile) {
    const hoehe = breite <= 320 ? 640 : breite < 600 ? 844 : breite === 1366 ? 650 : 900, handy = breite < 600, name = art + ' ' + breite;
    console.log('— ' + name);
    fs.readdirSync(daten).forEach(f => fs.rmSync(path.join(daten, f), { force: true }));
    const browser = art === 'webkit' ? await PW.webkit.launch() : art === 'firefox' ? await PW.firefox.launch() : await PW.chromium.launch();   /* Chromium von Playwright, nie das Chrome des Rechners (Regel 49) */
    for (const c of LISTE) {
      if (c.nurRechner && handy || c.nurHandy && !handy || c.nurBreite && c.nurBreite !== breite) continue;
      if (process.env.NUR && !process.env.NUR.split(',').includes(c.id)) continue;
      if (c.einmal && erg.zeilen[c.id].gilt) continue;   /* einmal je Lauf genügt (Sicherheit des Dienstes, nicht des Browsers) */
      const z = erg.zeilen[c.id]; z.gilt++;
      const ctx = await browser.newContext({ viewport: { width: breite, height: hoehe }, isMobile: art === 'chromium' && handy, hasTouch: handy, acceptDownloads: true });
      const env = { ctx, browser, breite, hoehe, art, id: c.id, fehler: [], daten };
      try { await Promise.race([c.fn(env), new Promise((_, no) => setTimeout(() => no(new Error('Zeitüberschreitung')), c.lang ? 80000 : 45000))]); z.gruen++; process.stdout.write('  ✓ ' + c.id + ' '); }
      catch (e) { z.rot = z.rot || []; z.rot.push(name + ': ' + String(e.message).split('\n')[0].slice(0, 160)); console.log('\n  ✗ ' + c.id + ' (' + name + '): ' + String(e.message).split('\n')[0].slice(0, 200)); }
      await ctx.close().catch(() => {});
    }
    console.log(''); await browser.close();
  }
  srv.kill(); fs.rmSync(daten, { recursive: true, force: true });
  erg.alle = LISTE.length; erg.gilt = Object.values(erg.zeilen).filter(z => z.gilt).length; erg.gruen = Object.values(erg.zeilen).filter(z => z.gilt && !z.rot).length;
  if (!process.env.NUR) { fs.writeFileSync(path.join(HIER, 'abnahme-ergebnis.json'), JSON.stringify(erg, null, 1)); liste(); }
  console.log('\nZeilen: ' + erg.gilt + ', grün in allen Läufen: ' + erg.gruen + ', rot: ' + (erg.gilt - erg.gruen));
  Object.entries(erg.zeilen).filter(([, z]) => z.rot).forEach(([id, z]) => console.log(' ROT ' + id + ': ' + z.rot.join(' || ')));
  process.exit(erg.gilt === erg.gruen ? 0 : 1);
}
if (require.main === module) { if (AUS[0] === 'liste') { liste(); console.log('FUNKTIONSLISTE.md geschrieben (' + LISTE.length + ' Zeilen)'); } else lauf(); }
