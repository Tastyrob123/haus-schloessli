/* democheck.js · Demo-Check «Das Schaufenster» (Le Bureau) der Wirtschaft am Schlössli, 21.10.2026.
   node democheck.js <chromium|webkit> <1440|390>
   Eigener Server (PORT, Standard 9121) mit Wegwerf-Daten (WERKZEUGE_DATEN) und Wegwerf-Kopie der Seiten (WEBSITE_PROBE), beides am Ende gelöscht,
   eigener Prozess am Ende beendet, Browser unsichtbar. Die Website des Hauses (website/) und die echten Daten werden nie angefasst: Prüfsummen vorher/nachher.
   Handy (390): Tippen statt Klicken (hasTouch, tap). Jede Ansicht wird bedient, nicht nur geladen. Bilder nach BILDER. */
const fs = require('fs'), path = require('path'), os = require('os'), crypto = require('crypto');
const { spawn, execFileSync } = require('child_process');
const pw = require(path.join(os.homedir(), 'Aussen-Pruefung/node_modules/playwright'));
const MOTOR = process.argv[2] || 'chromium', BREITE = +(process.argv[3] || 1440), HOEHE = BREITE < 700 ? 844 : 900, HANDY = BREITE < 700;
const BUREAU = path.resolve(__dirname, '..'), PROJEKT = path.resolve(BUREAU, '../..');
const STAMM = path.join(os.homedir(), 'Desktop/Website-Projekte/_Werkzeuge'), WS = path.join(STAMM, 'werkzeuge/website');
const DATEN = fs.mkdtempSync(path.join(os.tmpdir(), 'dc-bureau-')), PROBE = path.join(WS, `_probe-democheck-${process.pid}`);
const PORT = +(process.env.PORT || 9121), B = `http://127.0.0.1:${PORT}`;
const BILDER = process.env.BILDER || path.join(os.homedir(), 'Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/bureau');
fs.mkdirSync(BILDER, { recursive: true });
let n = 0; const rot = [];
function pruef(ok, was, mehr) { n++; console.log((ok ? 'gut    ' : 'FEHLT  ') + was + (!ok && mehr ? '  → ' + String(mehr).slice(0, 400) : '')); if (!ok) rot.push(was); return ok; }
const warte = ms => new Promise(r => setTimeout(r, ms));
async function bis(fn, ms = 8000) { for (const e = Date.now() + ms; Date.now() < e; await warte(120)) { try { if (await fn()) return true; } catch (x) { } } return false; }
const sha = f => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
function baum(d, flach) { const o = {}; (function g(x) { for (const e of fs.readdirSync(x, { withFileTypes: true })) { const p = path.join(x, e.name); if (e.isDirectory()) { if (!flach) g(p); } else if (/\.(html|json|js|css)$/.test(e.name)) o[path.relative(d, p)] = sha(p); } })(d); return o; }   // flach: nur die Seiten der Website (website/werkbank/ gehört anderen Chats)

(async () => {
  const echteSeiten = baum(path.join(PROJEKT, 'website'), true), echteDaten = baum(path.join(STAMM, 'daten/schloessli'));
  const besetzt = await fetch(B + '/').then(() => true).catch(() => false);
  if (besetzt) { console.log('Port ' + PORT + ' ist belegt. Der Lauf beendet nichts, was er nicht selbst gestartet hat.'); process.exit(2); }
  execFileSync('python3', [path.join(WS, 'probe.py'), 'schloessli'], { env: { ...process.env, WEBSITE_PROBE: PROBE } });
  const srv = spawn('python3', [path.join(BUREAU, 'serve.py'), String(PORT)], { env: { ...process.env, WERKZEUGE_DATEN: DATEN, WEBSITE_PROBE: PROBE, BUREAU_PRUEFLAUF: '1' }, stdio: 'ignore' });
  process.on('exit', () => { try { srv.kill(); } catch (e) { } try { fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true }); } catch (e) { } });
  process.on('uncaughtException', e => { console.log('FEHLT  Lauf ohne Abbruch  → ' + e.message); process.exit(1); });
  await bis(async () => (await fetch(B + '/_werkzeuge/bureau/')).ok, 15000);
  const ONLINE = path.join(PROBE, 'schloessli/online'), seiten = fs.readdirSync(ONLINE).filter(f => f.endsWith('.html'));
  const vorher = Object.fromEntries(seiten.map(f => [f, sha(path.join(ONLINE, f))]));
  const br = await pw[MOTOR].launch({ headless: true });
  const ctx = await br.newContext({ viewport: { width: BREITE, height: HOEHE }, deviceScaleFactor: 1, hasTouch: HANDY, isMobile: HANDY && MOTOR === 'chromium', acceptDownloads: false });
  await ctx.route(/^(mailto|tel):/, r => r.abort());
  const p = await ctx.newPage(); const konsole = [], fremd = [], schlecht = [];
  p.on('console', m => { if (m.type() === 'error' && !/409 \(Conflict\)|status of 4(09|22)/.test(m.text())) konsole.push(m.text().slice(0, 200)); });
  p.on('pageerror', e => konsole.push('SEITE: ' + e.message));
  p.on('dialog', d => d.accept());
  ctx.on('request', r => { const u = r.url(); if (!/^(http:\/\/127\.0\.0\.1|data:|blob:|about:)/.test(u)) fremd.push(u.slice(0, 120)); });
  ctx.on('response', r => { if (r.status() >= 400 && !/api\/x\/website\/(aendern|speichern)/.test(r.url())) schlecht.push(r.status() + ' ' + r.url().replace(B, '')); });
  const bild = async (name, ganz) => p.screenshot({ path: path.join(BILDER, `${name}-${MOTOR}-${BREITE}.png`), fullPage: !!ganz });
  const druck = async loc => { await loc.scrollIntoViewIfNeeded().catch(() => { }); await loc.evaluate(e => e.scrollIntoView({ block: 'center' })).catch(() => { }); if (HANDY) await loc.tap(); else await loc.click(); };
  const ueberlauf = async was => pruef(await p.evaluate(b => document.documentElement.scrollWidth <= b + 1 && document.body.scrollWidth <= b + 1, BREITE), `${was}: kein seitliches Verrutschen`);
  const ruhe = async () => { for (let i = 0, s = 0; i < 120 && s < 2; i++) { s = (await p.evaluate(() => document.documentElement.getAttribute('data-ws-laeuft')).catch(() => '0')) === '0' ? s + 1 : 0; await warte(120); } };
  const geh = async (ansicht) => { await p.goto('about:blank'); await p.goto(B + '/_werkzeuge/bureau/?ansicht=' + encodeURIComponent(ansicht), { waitUntil: 'load' }); return bis(() => p.evaluate(a => document.querySelector('#ws-mitte').getAttribute('data-ws-bereit') === a, ansicht), 20000); };
  const randAuf = async () => { if (!HANDY) return; const k = p.locator('[data-wo-rand-knopf]'); if (await k.count() && (await k.getAttribute('aria-expanded')) !== 'true') { await k.tap(); await warte(400); } };
  const stand = async () => (await fetch(B + '/api/x/website/stand/schloessli')).json();
  const speichern = async () => { await druck(p.locator('#ws-speichern')); await bis(() => p.locator('[data-ws-quittung], [data-ws-meldung]').count(), 10000); await ruhe(); };
  const frame = () => p.frameLocator('iframe[data-ws-frame="entwurf"]');
  const fotosOk = async sel => p.evaluate(async s => { const im = [...document.querySelectorAll(s)]; for (const i of im) { i.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 60)); } await new Promise(r => setTimeout(r, 900)); return im.map(i => i.getBoundingClientRect().width > 40 && i.naturalWidth > 0); }, sel);
  try {
    // ---------------- Übersicht
    pruef(await geh('start'), 'Übersicht öffnet');
    await warte(900);
    pruef((await p.locator('.wo-kopf').textContent()).includes('Das Schaufenster'), 'Kopf: Name «Das Schaufenster»');
    const ag = await p.locator('.wo-aufg > .wo-ag').count(); pruef(ag >= 6, 'Häufig gebraucht: Kacheln da (' + ag + ')');
    const bk = await fotosOk('.wo-ber .wo-bk__b img'); pruef(bk.length === 7 && bk.every(Boolean), 'Bereiche: sieben Kacheln, jede mit sichtbarem Foto (Fehlerbuch 10a)', JSON.stringify(bk));
    const af = await fotosOk('.wo-aufg .wo-ag img'); pruef(af.every(Boolean), 'Häufig gebraucht: jedes Foto geladen', JSON.stringify(af));
    pruef(!(await p.locator('#ws-raus').count()) && !(await p.locator('#ws-vgl').count()), 'Leiste: ohne Entwurf keine ausgegrauten Knöpfe (Fehlerbuch 10a)');
    await p.evaluate(() => scrollTo(0, 0)); await warte(300);
    await ueberlauf('Übersicht'); await bild('01-uebersicht'); await bild('01-uebersicht-ganz', true);
    // jede Kachel «Häufig gebraucht» führt in eine Ansicht
    const zielAg = await p.$$eval('.wo-aufg > .wo-ag', a => a.map(x => x.getAttribute('data-gehe') || x.getAttribute('href')));
    for (let i = 0; i < zielAg.length; i++) {
      await geh('start'); await warte(400);
      const k = p.locator('.wo-aufg > .wo-ag').nth(i), z = zielAg[i];
      if (z && /^(http|\/)/.test(z)) { pruef(/127\.0\.0\.1:\d+\/_werkzeuge\/carte\//.test(z) || z.startsWith('/'), `Häufig gebraucht ${i + 1} führt zum Kartenpult (${z})`); continue; }
      await druck(k);
      pruef(await bis(() => p.evaluate(a => document.querySelector('#ws-mitte').getAttribute('data-ws-bereit') === a, z), 20000), `Häufig gebraucht ${i + 1} öffnet «${z}»`);
    }
    // jede Bereich-Kachel
    const bks = await (async () => { await geh('start'); return p.$$eval('.wo-ber > .wo-bk', a => a.map(x => x.getAttribute('data-gehe'))); })();
    for (const z of bks) {
      await geh('start'); await warte(300);
      await druck(p.locator(`.wo-ber > .wo-bk[data-gehe="${z}"]`));
      pruef(await bis(() => p.evaluate(a => document.querySelector('#ws-mitte').getAttribute('data-ws-bereit') === a, z), 25000), `Bereich-Kachel öffnet «${z}»`);
    }
    // Rand: jeder Eintrag (Handy: Knopf «Bereiche», schliesst nach der Wahl)
    await geh('start');
    await randAuf();
    const navs = await p.$$eval('#ws-rand button[data-ws-nav]', a => a.map(x => x.getAttribute('data-ws-nav')));
    pruef(navs.length >= 12, 'Rand: alle Einträge da (' + navs.length + ')');
    if (HANDY) await bild('02-rand-offen');
    for (const z of navs) {
      await geh('start'); await randAuf();
      await druck(p.locator(`#ws-rand button[data-ws-nav="${z}"]`));
      pruef(await bis(() => p.evaluate(a => document.querySelector('#ws-mitte').getAttribute('data-ws-bereit') === a, z), 25000), `Rand öffnet «${z}»`);
      if (HANDY) pruef(!(await p.evaluate(() => document.documentElement.classList.contains('wo-rand-auf'))), `Handy: Rand schliesst sich nach «${z}»`);
      await ruhe(); await warte(600);
      await ueberlauf('Ansicht ' + z);
      const nm = z.replace(/[:]/g, '-');
      if (z.startsWith('b:')) {
        pruef(await bis(() => frame().locator('body').count(), 15000), `Vorschau lädt (${z})`);
        const st = await p.locator('#ws-gruppen .ws-st').count(); pruef(st > 0, `Stellen-Liste gefüllt (${z}: ${st})`);
        // jede Seite des Bereichs
        const reiter = await p.locator('.ws-reiter [role=radio], .ws-reiter button').count();
        if (reiter > 1) for (let r = 1; r < reiter; r++) {
          await druck(p.locator('.ws-reiter [role=radio], .ws-reiter button').nth(r)); await ruhe(); await warte(500);
          pruef(await p.locator('#ws-gruppen .ws-st').count() > 0 && await bis(() => frame().locator('body').count(), 15000), `${z}: Seite ${r + 1} von ${reiter} öffnet mit Stellen und Vorschau`);
        }
        // Suche
        const such = p.locator('#ws-such');
        if (await such.count()) { await such.fill('zzzqqq'); await warte(300); const sichtbar = await p.locator('#ws-gruppen .ws-st:visible').count(); await such.fill(''); pruef(sichtbar === 0, `${z}: Suche filtert die Stellen`); }
      }
      await bild('03-' + nm);
    }
    // ---------------- Text ändern: Klick/Tippen in der Vorschau, Vorschau schreibt mit, Speichern, neu laden, Rückgängig
    await geh('b:start'); await ruhe(); await bis(() => frame().locator('[data-ws-e]').count(), 15000); await warte(1500);
    const kand = await p.evaluate(() => { const d = document.querySelector('iframe[data-ws-frame="entwurf"]').contentDocument; const z = {}; [...d.querySelectorAll('[data-ws-e]')].forEach(e => z[e.dataset.wsE] = (z[e.dataset.wsE] || 0) + 1);
      return [...d.querySelectorAll('main p[data-ws-e]')].filter(e => !e.closest('[data-ws-zu]') && e.children.length === 0 && e.getBoundingClientRect().width > 40 && z[e.dataset.wsE] === 1).map(e => ({ h: e.dataset.wsE, n: e.dataset.wsN, t: e.textContent.trim() })).filter(x => x.t.length > 30 && x.t.length < 140)[0]; });
    pruef(!!kand, 'Startseite: Textstelle in der Vorschau gefunden', JSON.stringify(kand));
    const ziel = frame().locator(`[data-ws-e="${kand.h}"][data-ws-n="${kand.n}"]`);
    await ziel.evaluate(e => e.scrollIntoView({ block: 'center' }));
    try { if (HANDY && MOTOR === 'chromium') await ziel.tap({ timeout: 6000 }); else await ziel.click({ timeout: 6000 }); } /* Safari-Kern auf dem Mac macht aus Tippen keinen Klick (Prüfbrowser), dort Klick */ catch (e) { pruef(false, 'Stelle in der Vorschau direkt anklickbar (nichts liegt darüber)', e.message.split('\n')[0]); await ziel.dispatchEvent('click'); }
    pruef(await bis(() => p.locator(`[data-ws-form="text"][data-ws-wahl$="|${kand.h}|${kand.n}"]`).count(), 15000), (HANDY && MOTOR === 'chromium' ? 'Tippen' : 'Klick') + ' in der Vorschau öffnet das Feld der Stelle');
    await ruhe(); await warte(500); await bild('04-stelle-offen');
    const neu = 'Demo-Check: ' + kand.t.slice(0, 40);
    const ed = p.locator('[data-ws-form="text"] [contenteditable], [data-ws-form="text"] textarea, [data-ws-form="text"] input[type=text]').first();
    await ed.click(); await p.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A'); await p.keyboard.type(neu);
    pruef(await bis(() => frame().locator(`[data-ws-e="${kand.h}"][data-ws-n="${kand.n}"]`).textContent().then(t => t.includes('Demo-Check')), 4000), 'Tippen zeigt sofort in der Vorschau');
    pruef(await p.locator('#ws-speichern[data-ws-lage="offen"]').count() === 1, 'Speichern-Knopf gelb bei offener Eingabe');
    await speichern();
    pruef(await p.locator('[data-ws-quittung]').count() >= 1, 'Quittung nach dem Speichern'); await bild('05-quittung');
    let st = await stand(); pruef(st.aenderungen.some(a => a.art === 'text'), 'Änderung liegt im Entwurf (Wegwerf-Daten)');
    pruef(sha(path.join(ONLINE, 'index.html')) === vorher['index.html'], 'Speichern ändert die Seite noch nicht (erst Veröffentlichen)');
    await p.reload({ waitUntil: 'load' }); await bis(() => p.evaluate(() => document.querySelector('#ws-mitte').getAttribute('data-ws-bereit') === 'b:start'), 20000); await bis(() => frame().locator('[data-ws-e]').count(), 15000); await warte(800);
    pruef(await bis(() => frame().locator(`[data-ws-e="${kand.h}"][data-ws-n="${kand.n}"]`).textContent().then(t => t.includes('Demo-Check')), 8000), 'Speichern → neu laden → Änderung noch da');
    // Rückgängig über die Quittung: zweite Änderung, dann Rückgängig
    await geh('zahlen'); await ruhe();
    const zw = p.locator('.ws-zl__wert').nth(1); const zAlt = (await zw.textContent()).trim();
    await druck(zw); await bis(() => p.locator('[data-ws-form="text"]').count(), 8000);
    const ed2 = p.locator('[data-ws-form="text"] [contenteditable], [data-ws-form="text"] textarea, [data-ws-form="text"] input[type=text]').first();
    await ed2.click(); await p.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A'); await p.keyboard.type('11:00 bis 13:00 · 18:00 bis 21:00 Uhr');
    await speichern(); await bild('06-zahlen-gespeichert');
    const rk = p.locator('[data-ws-quittung] button, [data-ws-quittung] a').filter({ hasText: 'Rückgängig' }).first();
    pruef(await rk.count() === 1, 'Quittung hat «Rückgängig»');
    if (await rk.count()) { await druck(rk); await bis(async () => !(await stand()).aenderungen.some(a => a.nachher && /11:00 bis 13:00/.test(a.nachher)), 8000); }
    st = await stand(); pruef(!st.aenderungen.some(a => /11:00 bis 13:00/.test(JSON.stringify(a))), 'Rückgängig nimmt die letzte Änderung zurück', zAlt);
    // Filter und «In der Seite» in Zeiten & Preise
    await geh('zahlen'); await ruhe();
    for (const f of ['Preise', 'Zeiten', 'Grössen und Dauer', 'Alle']) { const k = p.locator('.ws-mitte-reihe [role=radio], .ws-mitte-reihe button').filter({ hasText: f }).first(); if (await k.count()) { await druck(k); await warte(250); pruef((await p.locator('.ws-zl').count()) > 0 || f === 'Grössen und Dauer', `Zeiten & Preise: Filter «${f}» zeigt Zeilen`); } }
    await p.locator('#ws-suche').fill('Seestrasse'); await warte(300); pruef(await p.locator('.ws-zl').count() >= 1, 'Zeiten & Preise: Suche findet'); await p.locator('#ws-suche').fill('');
    await druck(p.locator('.ws-zl a, .ws-zl button').filter({ hasText: 'In der Seite' }).first());
    pruef(await bis(() => p.evaluate(() => (document.querySelector('#ws-mitte').getAttribute('data-ws-bereit') || '').startsWith('b:')), 20000), '«In der Seite» springt in den Bereich');
    // ---------------- Foto tauschen
    await geh('b:start'); await ruhe(); await bis(() => frame().locator('[data-ws-e]').count(), 15000);
    const fk = p.locator('#ws-gruppen .ws-foto, #ws-gruppen button[data-ws-foto-st]').first();
    if (!(await fk.count())) { const grp = p.locator('#ws-gruppen summary, #ws-gruppen .ws-gr > button').first(); if (await grp.count()) await druck(grp); }
    const fk2 = p.locator('#ws-gruppen .ws-foto, #ws-gruppen [data-ws-foto-st]').first();
    pruef(await fk2.count() >= 1, 'Foto-Stelle in der Liste');
    if (await fk2.count()) {
      await druck(fk2);
      pruef(await bis(() => p.locator('[data-ws-fenster="bild"]').count(), 10000), 'Fenster «Foto tauschen» öffnet');
      const wahl = await p.locator('[data-ws-fenster="bild"] .ws-fwahl').count(); pruef(wahl > 20, 'Fotos des Hauses zur Wahl (' + wahl + ')');
      const ganz = await p.evaluate(() => [...document.querySelectorAll('[data-ws-fenster="bild"] .ws-fwahl__b')].slice(0, 12).map(b => b.getBoundingClientRect()).every(r => r.height > 50 && r.width > 50));
      pruef(ganz, 'Foto-Auswahl zeigt ganze Kacheln, nie gestaucht (Fehlerbuch 10a)');
      await bild('07-foto-fenster');
      await druck(p.locator('[data-ws-fenster="bild"] .ws-fwahl').nth(5));
      await druck(p.locator('[data-ws-fenster="bild"] button').filter({ hasText: 'Speichern' }).last());
      await bis(() => p.locator('[data-ws-quittung]').count(), 8000); await ruhe();
      st = await stand(); pruef(st.aenderungen.some(a => a.art === 'bild'), 'Getauschtes Foto im Entwurf');
    }
    // ---------------- Ausblenden und wieder zeigen
    await geh('haus:anlaesse'); await ruhe(); await warte(500);
    const eint = await p.locator('details.ws-eintrag').count(); pruef(eint >= 1, 'Anlässe: Einträge (' + eint + ')');
    const ebild = await fotosOk('.ws-eintrag__b img'); pruef(ebild.length >= 1 && ebild.every(Boolean), 'Anlässe: jeder Eintrag mit Foto', JSON.stringify(ebild));
    await bild('08-anlaesse');
    await druck(p.locator('details.ws-eintrag summary').first()); await warte(600); await bild('08b-anlass-offen');
    const aus = p.locator('details.ws-eintrag[open] button, details.ws-eintrag[open] a').filter({ hasText: /Ausblenden/ }).first();
    pruef(await aus.count() === 1, 'Anlass: «Ausblenden» da');
    if (await aus.count()) {
      await druck(aus); await bis(() => p.locator('[data-ws-quittung]').count(), 8000); await ruhe();
      st = await stand(); pruef(st.aenderungen.some(a => a.art === 'aus'), 'Ausblenden liegt im Entwurf');
      await geh('haus:anlaesse'); await ruhe(); await druck(p.locator('details.ws-eintrag summary').first()); await warte(600);
      const wz = p.locator('button, a').filter({ hasText: /Wieder zeigen/ }).first();
      pruef(await wz.count() === 1, '«Wieder zeigen» steht da');
      if (await wz.count()) { await druck(wz); await ruhe(); await warte(600); st = await stand(); pruef(!st.aenderungen.some(a => a.art === 'aus'), 'Wieder zeigen nimmt das Ausblenden zurück'); }
    }
    await geh('haus:team'); await ruhe(); await warte(500);
    const tb = await fotosOk('.ws-eintrag__b img'); pruef(tb.length >= 1 && tb.every(Boolean), 'Team: Einträge mit Foto (' + tb.length + ')', JSON.stringify(tb));
    await bild('09-team');
    // ---------------- Hinweis für Gäste
    await geh('hinweis'); await ruhe();
    await druck(p.locator('[data-ws-form="hinweis"] [role=radio], [data-ws-form="hinweis"] button').filter({ hasText: 'Eingeschaltet' }).first());
    await p.locator('#ws-h-text').fill('Am Montag, 26. Oktober, bleibt die Küche ab 14 Uhr geschlossen.');
    await p.locator('#ws-h-von').fill('22.10.2026'); await p.locator('#ws-h-bis').fill('27.10.2026');
    await speichern(); await bild('10-hinweis');
    st = await stand(); pruef(st.aenderungen.some(a => a.art === 'hinweis'), 'Hinweis für Gäste liegt im Entwurf');
    const vk = await (await fetch(B + '/api/x/website/vorschau/schloessli/entwurf/de/index.html').catch(() => null))?.json?.().catch(() => null);
    // ---------------- Entwurf & Vergleich
    await geh('entwurf'); await ruhe(); await warte(500);
    const zahlA = await p.locator('[data-ws-aenderung]').count(); pruef(zahlA >= 3, 'Entwurf listet die Änderungen (' + zahlA + ')');
    await bild('11-entwurf'); await ueberlauf('Entwurf');
    pruef(await p.locator('#ws-vgl').count() === 1 && await p.locator('#ws-raus').count() === 1, 'Leiste mit Entwurf: «Vorher, nachher» und «Veröffentlichen»');
    await druck(p.locator('#ws-vgl')); pruef(await bis(() => p.locator('#ws-vergleich, [data-ws-vgl]').count(), 10000), '«Vorher, nachher» öffnet den Vergleich'); await warte(900); await bild('12-vergleich');
    await p.keyboard.press('Escape'); await warte(400);
    const zn = p.locator('[data-ws-aenderung] button, [data-ws-aenderung] a').filter({ hasText: 'Zurücknehmen' }).first();
    if (await zn.count()) { const v0 = (await stand()).aenderungen.length; await druck(zn); await bis(async () => (await stand()).aenderungen.length < v0, 8000); pruef((await stand()).aenderungen.length < v0, 'Einzelne Änderung «Zurücknehmen»'); }
    else pruef(false, 'Knopf «Zurücknehmen» je Änderung');
    // ---------------- Veröffentlichen (nur in die Wegwerf-Kopie) und Frühere Fassungen
    await geh('entwurf'); await ruhe();
    await druck(p.locator('#ws-raus')); await bis(() => p.locator('[data-ws-fenster="veroeffentlichen"]').count());
    await bild('13-veroeffentlichen-fenster');
    if (await p.locator('#ws-notiz').count()) await p.locator('#ws-notiz').fill('Demo-Check');
    await druck(p.locator('[data-ws-fenster="veroeffentlichen"] .kn--d, [data-ws-fenster="veroeffentlichen"] button').filter({ hasText: /veröffentlichen/i }).last());
    pruef(await bis(() => p.locator('[data-ws-veroeffentlicht]').count(), 30000), '«Ist online.» nach Veröffentlichen'); await bild('14-veroeffentlicht');
    if (process.env.LAUT) { const s9 = await stand(); console.log('STAND', s9.offen, JSON.stringify(s9.aenderungen.map(a => [a.art, a.seite, (a.nachher || '').slice(0, 40)])), JSON.stringify(s9.zuletzt || '').slice(0, 300)); console.log('VERLAUF', (await (await fetch(B + '/api/x/website/verlauf/schloessli')).text()).slice(0, 800)); }
    const geaendert = seiten.filter(f => sha(path.join(ONLINE, f)) !== vorher[f]); pruef(geaendert.length >= 1 && /Küche ab 14 Uhr geschlossen/.test(fs.readFileSync(path.join(ONLINE, 'index.html'), 'utf8')), 'Veröffentlichen landet in der Wegwerf-Kopie (Hinweis für Gäste auf der Seite, ' + geaendert.length + ' Seiten neu)');
    const web = await (await fetch(B + '/werkzeuge/website/' + path.basename(PROBE) + '/schloessli/online/index.html')).text();
    pruef(/Küche ab 14 Uhr geschlossen/.test(web), '«Website ansehen» zeigt den neuen Stand');
    await geh('verlauf'); await ruhe(); await bild('15-verlauf');
    const fass = p.locator('[data-ws-fassung]'); pruef(await fass.count() >= 1, 'Frühere Fassungen mit Ursprung (' + await fass.count() + ')');
    pruef(/Ursprünglicher Stand/.test(await fass.last().textContent()), '«Ursprünglicher Stand» unten');
    await druck(fass.last().locator('button').filter({ hasText: /Zurückholen|In den Entwurf/ }).first());
    await bis(() => p.locator('.ws-fenster__blatt').count()); await druck(p.locator('.ws-fenster__blatt .kn--d').first());
    await bis(async () => (await stand()).offen, 8000);
    pruef((await stand()).offen && /Küche ab 14 Uhr geschlossen/.test(fs.readFileSync(path.join(ONLINE, 'index.html'), 'utf8')), 'Zurückholen legt in den Entwurf, Website bleibt bis zum Veröffentlichen');
    await geh('entwurf'); await druck(p.locator('#ws-raus')); await bis(() => p.locator('[data-ws-fenster="veroeffentlichen"]').count());
    await druck(p.locator('[data-ws-fenster="veroeffentlichen"] .kn--d, [data-ws-fenster="veroeffentlichen"] button').filter({ hasText: /veröffentlichen/i }).last());
    await bis(() => p.locator('[data-ws-veroeffentlicht]').count(), 30000);
    const anders = seiten.filter(f => sha(path.join(ONLINE, f)) !== vorher[f]);
    pruef(!anders.length, 'Zurück auf den Ursprung: alle Seiten Byte für Byte wie vorher', anders.join(','));
    // ---------------- Verwerfen mit Rückgängig
    await geh('hinweis'); await p.locator('#ws-h-text').fill('Probe zum Verwerfen'); await druck(p.locator('[data-ws-form="hinweis"] [role=radio], [data-ws-form="hinweis"] button').filter({ hasText: 'Eingeschaltet' }).first()); await speichern();
    await geh('entwurf'); const vw = p.locator('button, a').filter({ hasText: /^Verwerfen|Alles verwerfen|Entwurf verwerfen/ }).first();
    pruef(await vw.count() === 1, 'Entwurf: «Verwerfen» da');
    if (await vw.count()) { await druck(vw); await bis(() => p.locator('.ws-fenster__blatt').count()); await druck(p.locator('.ws-fenster__blatt button').filter({ hasText: 'Ja, verwerfen' }).first()); await bis(async () => !(await stand()).offen, 8000); pruef(!(await stand()).offen, 'Verwerfen leert den Entwurf'); }
    // ---------------- Kopf und Wege
    await geh('start');
    const links = await p.$$eval('a[href]', a => [...new Set(a.map(x => x.getAttribute('href')))]);
    for (const h of links) {
      if (/^(mailto|tel):/.test(h)) { pruef(false, 'kein mailto/tel im Werkzeug', h); continue; }
      const u = new URL(h, B + '/_werkzeuge/bureau/');
      if (u.host !== '127.0.0.1:' + PORT) { pruef(/^127\.0\.0\.1:\d+$/.test(u.host), 'Weg bleibt lokal: ' + h); continue; }
      const r = await fetch(u, { redirect: 'manual' });
      if (r.status === 302 || r.status === 301) { const loc = r.headers.get('location'); let ok = false; try { ok = (await fetch(new URL(loc, u))).ok; } catch (e) { } pruef(ok || /:898[0-9]|:90\d\d/.test(loc), `Weg ${h} → ${loc} antwortet`, loc); }
      else pruef(r.ok, `Weg ${h} antwortet (${r.status})`);
    }
    // Prüfseite
    await p.goto(B + '/werkzeuge/website/pruefung.html?haus=schloessli', { waitUntil: 'load' }); await warte(4000);
    await bis(() => p.locator('#wsp-server .wsp-punkt').count(), 10000); await warte(1500);
    const rotP = await p.$$eval('.wsp-punkt[data-gut="nein"]', a => a.map(e => e.innerText.replace(/\s+/g, ' ')));
    pruef(!rotP.length && await p.locator('.wsp-punkt').count() >= 12, 'Prüfseite: jeder Punkt in Ordnung (' + await p.locator('.wsp-punkt').count() + ')', rotP.join(' | '));
    pruef(!(await p.locator('[data-welt-knopf]').count()) && /Das Schaufenster/.test(await p.locator('.wsp-kopf').innerText()), 'Prüfseite: Name des Hauses, kein Weltknopf «Grandhotel»');
    pruef(/\/_werkzeuge\/bureau\/$/.test(await p.locator('#wsp-zurueck').getAttribute('href')), 'Prüfseite: «Zum Werkzeug» führt ins Schaufenster');
    await ueberlauf('Prüfseite'); await bild('16-pruefseite'); await bild('16-pruefseite-ganz', true);
    // Website ansehen (Kopie)
    await p.goto(B + '/werkzeuge/website/' + path.basename(PROBE) + '/schloessli/online/index.html', { waitUntil: 'load' }); await warte(1500);
    await bild('17-website-ansehen');
  } catch (e) { pruef(false, 'Lauf ohne Abbruch', (e.stack || e).toString().split('\n').slice(0, 3).join(' ')); await bild('zz-abbruch').catch(() => { }); }
  pruef(!konsole.length, 'keine Fehler in der Konsole', [...new Set(konsole)].join(' | '));
  pruef(!fremd.length, 'keine Anfrage an fremde Server', [...new Set(fremd)].slice(0, 6).join(' | '));
  pruef(!schlecht.length, 'keine Antwort 4xx/5xx', [...new Set(schlecht)].slice(0, 8).join(' | '));
  await br.close(); srv.kill();
  fs.rmSync(PROBE, { recursive: true, force: true }); fs.rmSync(DATEN, { recursive: true, force: true });
  const s2 = baum(path.join(PROJEKT, 'website'), true), d2 = baum(path.join(STAMM, 'daten/schloessli'));
  pruef(JSON.stringify(s2) === JSON.stringify(echteSeiten), 'Website des Hauses (website/) unberührt');
  pruef(JSON.stringify(d2) === JSON.stringify(echteDaten), 'Echte Daten des Werkzeugs (_Werkzeuge/daten/schloessli) unberührt');
  console.log((rot.length ? 'NICHT BESTANDEN · ' + rot.length + ' von ' : 'BESTANDEN · ') + n + ' Prüfungen · ' + MOTOR + ' ' + BREITE);
  process.exit(rot.length ? 1 : 0);
})();
