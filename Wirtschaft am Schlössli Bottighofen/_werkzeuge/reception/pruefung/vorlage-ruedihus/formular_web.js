// Formulare der Website → Eingang des Gastgebers (E12, E15/E22 im Ruedihus): das Anfrage-Fenster (baustein/anfrage.js) Zeile für Zeile bedienen.
// Läuft gegen die Probe-Kopie, deren Seiten den Baustein eingebunden haben (PROBE-LIESMICH.txt), Server des Gastgebers mit Wegwerf-Daten und ohne KI.
//   node formular_web.js <origin> [chromium|webkit|firefox] [breite] [höhe]      z. B. node formular_web.js http://localhost:9023 webkit 390 844
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const [, , O, MOTOR = 'chromium', BREITE = '1440', HOEHE] = process.argv;
const W = +BREITE, H = +(HOEHE || (W < 700 ? 844 : 900)), HANDY = W < 700, B = O + '/_werkzeuge/reception/';
const OUT = path.join(__dirname, 'lauf'), BEL = path.join(__dirname, 'belege'); fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(BEL, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const res = [], fehler = [];
const ok = (b, was) => { if (!b) throw new Error(was); };
(async () => {
  const br = await require('./schutz').start(pw, MOTOR);
  const ctx = await require('./schutz').kontext(br, { viewport: { width: W, height: H }, locale: 'de-CH', hasTouch: HANDY, isMobile: HANDY && MOTOR === 'chromium' });
  await ctx.addInitScript(() => { try { localStorage.setItem('reception-name', 'QA Prüfer'); localStorage.setItem('rundgang-rh-reception', '1'); } catch (e) { /* */ } });
  const p = await ctx.newPage(); p.setDefaultTimeout(15000);
  let mailto = 0;
  p.on('pageerror', e => fehler.push('JS: ' + String(e).slice(0, 200)));
  p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|status of 4\d\d|net::ERR|Load failed|NetworkError|Failed to fetch|internet connection/i.test(m.text())) fehler.push('Konsole: ' + m.text().slice(0, 200)); });
  p.on('request', r => { if (/^mailto:/.test(r.url())) mailto++; });
  p.on('framenavigated', f => { if (/^mailto:/.test(f.url())) mailto++; });
  const schritt = async (name, fn) => {
    const f0 = fehler.length;
    try { const info = await fn(); const neu = fehler.slice(f0); res.push({ name, stand: neu.length ? 'rot' : 'grün', info: (neu.length ? 'Fehler: ' + neu.join(' | ') + ' · ' : '') + (info || '') }); }
    catch (e) { res.push({ name, stand: 'rot', info: String(e.message || e).split('\n')[0].slice(0, 300) }); await p.screenshot({ path: path.join(BEL, `formular-rot-${name.slice(0, 3)}-${MOTOR}-${W}.jpg`), type: 'jpeg', quality: 60 }).catch(() => {}); }
    const r = res[res.length - 1]; console.log(`${r.stand === 'grün' ? 'ok  ' : 'ROT '} ${r.name} · ${String(r.info).slice(0, 160)}`);
  };
  const seite = async (s) => { const [pf, h] = s.split('#'); await p.goto('about:blank'); await p.goto(O + '/' + pf + (pf.includes('?') ? '&' : '?') + 'probe=1' + (h ? '#' + h : ''), { waitUntil: 'load' }); await sleep(1200); };
  const fenster = async () => { await p.waitForSelector('dialog.anf[open]', { timeout: 8000 }); await sleep(500); };
  const klick = async (sel) => { const l = p.locator(sel).first(); await l.scrollIntoViewIfNeeded().catch(() => {}); await l.click(); };
  const absenden = async (f) => { await p.locator(f + ' [type=submit]').first().scrollIntoViewIfNeeded().catch(() => {}); await p.locator(f + ' [type=submit]').first().click(); };
  const senden = async (kontakt) => { await p.fill('dialog.anf input[name=kontakt]', kontakt); await klick('dialog.anf .anf__los'); };
  const danke = async () => { await p.waitForSelector('dialog.anf .anf__danke:not([hidden])', { timeout: 10000 }); return (await p.locator('dialog.anf .anf__dt').innerText()).trim(); };
  const zu = async () => { await klick('dialog.anf .anf__fertig'); await sleep(400); ok(!(await p.locator('dialog.anf[open]').count()), 'Fenster bleibt offen'); };
  const eingang = async () => p.evaluate(async b => (await (await fetch(b + 'api/anfragen')).json()).anfragen, B);
  const morgen = new Date(Date.now() + 3 * 864e5).toISOString().slice(0, 10), spaeter = new Date(Date.now() + 5 * 864e5).toISOString().slice(0, 10);

  await schritt('W01 Seite mit Anfrage-Fenster lädt, Hinweis «öffnet Ihr Mailprogramm» ist ersetzt', async () => {
    await seite('essen.html'); const hat = await p.evaluate(() => !!document.querySelector('script[src*="assets/js/anfrage.js"]'));
    ok(hat, 'anfrage.js nicht eingebunden (Probe-Kopie?)'); const t = await p.evaluate(() => document.body.textContent.replace(/\s+/g, ' '));
    ok(!/öffnet Ihr Mailprogramm/.test(t), 'Hinweis aufs Mailprogramm steht noch'); ok(/geht direkt an das Team des Hauses/.test(t), 'neuer Hinweis fehlt'); return 'eingebunden, Hinweis ersetzt';
  });
  await schritt('W02 Tisch in der Stube: «Tisch anfragen» öffnet das Fenster mit den Angaben, kein Mailprogramm', async () => {
    await seite('essen.html'); await p.locator('[data-buchen="tisch"]:visible').first().click(); await sleep(700);
    const f = 'dialog.buchen form[data-tisch]'; await p.fill(f + ' input[name=tag]', morgen); await p.selectOption(f + ' select[name=pers]', '4'); await p.selectOption(f + ' select[name=menu]', 'Fondue oder Raclette Menu');
    await p.fill(f + ' input[name=name]', 'Tisch QA'); await p.fill(f + ' textarea[name=wunsch]', 'Ein Kind isst lieber Rösti.'); await absenden(f); await fenster();
    const z = await p.locator('dialog.anf .anf__zus').innerText(); ok(/Stube: Chäs- und Wystube/.test(z) && /Personen: 4/.test(z) && /Rösti/.test(z), 'Angaben fehlen: ' + z.slice(0, 120));
    ok(await p.inputValue('dialog.anf input[name=name]') === 'Tisch QA', 'Name nicht übernommen'); ok(mailto === 0, 'Mailprogramm geöffnet'); await p.screenshot({ path: path.join(BEL, `formular-tisch-${MOTOR}-${W}.jpg`), type: 'jpeg', quality: 70 });
    return 'Fenster mit ' + z.split('\n').length + ' Zeilen';
  });
  await schritt('W03 Kontakt fehlt oder ungültig: Meldung am Fenster, nichts geschickt; gültig: Dank', async () => {
    await p.fill('dialog.anf input[name=kontakt]', ''); await klick('dialog.anf .anf__los'); await sleep(300); const m1 = await p.locator('dialog.anf .anf__meldung').innerText();
    await senden('morgen'); await sleep(300); const m2 = await p.locator('dialog.anf .anf__meldung').innerText();
    ok(/E-Mail-Adresse oder Telefonnummer/.test(m1) && /E-Mail-Adresse oder Telefonnummer/.test(m2), 'Meldung fehlt: ' + m1 + ' / ' + m2);
    await senden('tisch-qa@example.com'); const d = await danke(); ok(/Ruedihus/.test(d), 'Dank: ' + d); await zu(); return d;
  });
  await schritt('W04 Fest-Rechner: Gäste, Menü, Cüpli → Fenster mit Richtpreis-Zeilen → Event-Team', async () => {
    await seite('essen.html#feste'); const f = 'form[data-rechner]'; await p.fill(f + ' input[name=erw]', '18'); await p.fill(f + ' input[name=kinder]', '4'); await p.selectOption(f + ' select[name=anlass]', 'Geburtstag');
    await p.fill(f + ' input[name=datum]', spaeter); await p.locator(f + ' input[name=cuepli]').check(); await p.fill(f + ' input[name=name]', 'Fest QA'); await sleep(300); await absenden(f); await fenster();
    const z = await p.locator('dialog.anf .anf__zus').innerText(); ok(/Anlass: Geburtstag/.test(z) && /Gäste: 22/.test(z) && /Richtpreis/.test(z) && /Cüpli/.test(z), 'Angaben: ' + z.slice(0, 160));
    await senden('+41 79 000 00 00'); await danke(); await zu(); return 'gesendet';
  });
  await schritt('W05 Vor Ihrer Anreise: Ankunft und Tisch → Rezeption', async () => {
    await seite('anreise.html'); const f = 'form[data-anreise]'; await p.fill(f + ' input[name=name]', 'Anreise QA'); await p.fill(f + ' input[name=an]', morgen); await p.fill(f + ' input[name=ab]', spaeter); await sleep(300);
    await absenden(f); await fenster(); const z = await p.locator('dialog.anf .anf__zus').innerText(); ok(/Anreise:/.test(z) && /Ankunft:/.test(z), 'Angaben: ' + z.slice(0, 120));
    await senden('anreise-qa@example.com'); await danke(); await zu(); return 'gesendet';
  });
  await schritt('W06 Ihre Abreise: Abreisetag und Nachricht → Rezeption', async () => {
    await seite('abreise.html'); const f = 'form[data-abreise]'; await p.fill(f + ' input[name=name]', 'Abreise QA'); await p.fill(f + ' input[name=tag]', spaeter);
    await p.fill(f + ' textarea[name=wunsch]', 'Dürfen wir das Gepäck bis 15 Uhr stehen lassen?'); await sleep(300); await absenden(f); await fenster();
    const z = await p.locator('dialog.anf .anf__zus').innerText(); ok(/Abreise:/.test(z) && /Gepäck/.test(z), 'Angaben: ' + z.slice(0, 120)); await senden('abreise-qa@example.com'); await danke(); await zu(); return 'gesendet';
  });
  await schritt('W07 Freie Anfrage über einen Knopf mit data-anfrage (Gutschein): Auswahl, Datum, Personen, Nachricht', async () => {
    await seite('zimmer.html'); await p.evaluate(() => { const b = document.createElement('button'); b.type = 'button'; b.className = 'kn'; b.id = 'qa-anf'; b.setAttribute('data-anfrage', 'gutschein'); b.textContent = 'Gutschein für ein Zimmer anfragen'; document.querySelector('main, body').appendChild(b); });
    await klick('#qa-anf'); await fenster(); ok(await p.inputValue('dialog.anf select[name=art]') === 'gutschein', 'Art nicht gewählt'); ok(/Gutschein/.test(await p.locator('#anf-t').innerText()), 'Titel');
    await p.fill('dialog.anf input[name=name]', 'Gutschein QA'); await p.fill('dialog.anf input[name=datum]', 'Dezember'); await p.fill('dialog.anf input[name=personen]', '2');
    const ta = p.locator('dialog.anf textarea[name=nachricht]'); const h0 = await ta.evaluate(e => e.offsetHeight); await ta.fill('Eine Nacht in der Liebeslaube\nzum Hochzeitstag\nmeiner Eltern\nmit Frühstück'); const h1 = await ta.evaluate(e => e.offsetHeight);
    ok(h1 > h0, `Feld wächst nicht (${h0} → ${h1})`); await senden('gutschein-qa@example.com'); await danke(); await zu(); return `Feld ${h0} → ${h1} px`;
  });
  await schritt('W08 Escape und Klick daneben schliessen das Fenster, Eingaben bleiben beim Wiederöffnen', async () => {
    await klick('#qa-anf'); await fenster(); await p.fill('dialog.anf input[name=kontakt]', 'bleibt@example.com'); await p.keyboard.press('Escape'); await sleep(400); ok(!(await p.locator('dialog.anf[open]').count()), 'Esc schliesst nicht');
    await klick('#qa-anf'); await fenster(); ok(await p.inputValue('dialog.anf input[name=kontakt]') === 'bleibt@example.com', 'Eingabe weg'); await p.mouse.click(4, 4); await sleep(400); ok(!(await p.locator('dialog.anf[open]').count()), 'Klick daneben schliesst nicht'); return 'ok';
  });
  await schritt('W09 Netz weg beim Senden: Meldung, Eingaben bleiben; Netz wieder da: gesendet', async () => {
    await klick('#qa-anf'); await fenster(); await p.selectOption('dialog.anf select[name=art]', 'nachricht'); await p.fill('dialog.anf input[name=name]', 'Netz QA'); await p.fill('dialog.anf textarea[name=nachricht]', 'Netz QA');
    await p.route('**/api/formular', r => r.abort()); await senden('netz-qa@example.com'); await sleep(800); const m = await p.locator('dialog.anf .anf__meldung').innerText();
    ok(/Keine Verbindung/.test(m) && await p.inputValue('dialog.anf textarea[name=nachricht]') === 'Netz QA', 'Meldung/Eingabe: ' + m); await p.unroute('**/api/formular');
    await klick('dialog.anf .anf__los'); await danke(); await zu(); return 'Meldung, danach gesendet';
  });
  await schritt('W10 Handy und Laptop: das Fenster passt in die Breite, nichts ragt seitlich heraus', async () => {
    await klick('#qa-anf'); await fenster(); const r = await p.evaluate(() => { const d = document.querySelector('dialog.anf'), b = d.getBoundingClientRect(); return { l: b.left, r: b.right, w: innerWidth, sw: d.scrollWidth, cw: d.clientWidth }; });
    ok(r.l >= 0 && r.r <= r.w && r.sw <= r.cw + 1, JSON.stringify(r)); await p.screenshot({ path: path.join(BEL, `formular-frei-${MOTOR}-${W}.jpg`), type: 'jpeg', quality: 70 }); await p.keyboard.press('Escape'); return `${Math.round(r.r - r.l)} von ${r.w} px`;
  });
  await schritt('W11 Im Eingang: jede Anfrage mit Abteilung, Formular, Seite und Probe-Kennzeichen', async () => {
    await p.goto(B + '#eingang', { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *'); await sleep(800); const l = await eingang();
    const soll = { 'Tisch QA': ['Rezeption', 'tisch', 'tisch'], 'Fest QA': ['Event', 'fest', 'feier'], 'Anreise QA': ['Rezeption', 'anreise', 'aufenthalt'], 'Abreise QA': ['Rezeption', 'abreise', 'aufenthalt'], 'Gutschein QA': ['Rezeption', 'gutschein', 'gutschein'] };
    const aus = [];
    for (const [n, [ab, fo, art]] of Object.entries(soll)) { const a = l.find(x => x.name === n); ok(a, n + ' fehlt'); ok(a.abteilung === ab && a.formular === fo && a.art === art && a.web && a.probe && a.seite, n + ': ' + JSON.stringify({ ab: a.abteilung, fo: a.formular, art: a.art, web: a.web, probe: a.probe, seite: a.seite })); aus.push(n.split(' ')[0] + '→' + ab); }
    return aus.join(', ');
  });
  await schritt('W12 Fest im Eingang: Abteilung Event, «Über Website, Fest-Rechner», Brief von event@doldenhorn.ch', async () => {
    if (HANDY) { const auf = p.locator('#rand .rand__auf'); if (await auf.count()) { await auf.click(); await sleep(300); } }
    await p.locator('.re-abt [data-abt="Event"]').click(); await sleep(500); await p.locator('.re-liste .re-a', { hasText: 'Fest QA' }).first().click(); await p.waitForSelector('#brief', { timeout: 30000 }); await sleep(600);
    const d = (await p.locator('#detail').innerText()).replace(/\s+/g, ' '); ok(/Event/.test(d) && /Fest-Rechner/.test(d) && /event@doldenhorn\.ch/.test(d), 'Detail: ' + d.slice(0, 200));
    await p.screenshot({ path: path.join(BEL, `formular-eingang-${MOTOR}-${W}.jpg`), type: 'jpeg', quality: 70 }); return 'Event, Fest-Rechner, event@';
  });
  await schritt('W13 Kein Mailprogramm über alle Formulare, kein seitliches Verrutschen der Seiten', async () => {
    ok(mailto === 0, mailto + '× mailto'); const aus = [];
    for (const s of ['essen.html', 'anreise.html', 'abreise.html']) { await seite(s); const o = await p.evaluate(w => document.documentElement.scrollWidth - w, W); ok(o <= 1, s + ' ragt ' + o + ' px'); aus.push(s + ':' + o); }
    return aus.join(' ');
  });
  const gr = res.filter(r => r.stand === 'grün').length, ro = res.filter(r => r.stand === 'rot');
  fs.writeFileSync(path.join(OUT, `formular-${MOTOR}-${W}x${H}.json`), JSON.stringify(res, null, 1));
  console.log(`formular ${MOTOR} ${W}x${H}: ${gr} grün, ${ro.length} rot von ${res.length}`); await br.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
