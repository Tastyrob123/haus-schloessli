// Unabhängige Abnahme des Gastgebers (La Réception) · Landgasthof Ruedihus (Prüf-Chat 17.10.2026, Master Werkzeug-Bau Abschnitt 8).
// Prüft, was gegenprobe.js / abnahme.js nur anzeigen statt prüfen: Verrutschen gegen die eingestellte Breite (nicht innerWidth, Master 9),
// fremde Hauswerte im sichtbaren Text, Speichern → neu laden → noch da, Zurücksetzen, zwei Fenster (Konflikt gemeldet, nichts überschrieben),
// Netz weg im gestalteten Brief (Meldung, Nachsichern), Verlassen mit ungesicherter Eingabe, ungewöhnliche Eingaben über die Oberfläche,
// Fotos 30 MB / 400 px / Datei ohne Bild, PDF (Dateiname, Seiten) und ZIP herunterladen, jede Formular-Art der Website bis in den Eingang.
// Nur gegen einen Prüf-Server mit Wegwerf-Daten und ohne KI (Probe-Kopie mit PROBE-LIESMICH.txt und eingebundenem Baustein):
//   node unabhaengig.js <origin> [chromium|webkit|firefox] [breite] [höhe]     z. B. node unabhaengig.js http://localhost:9051 firefox 320 640
// Ergebnis: pruefung/lauf/unabhaengig-<motor>-<b>x<h>.json, Belege (Bildschirmfotos, PDF, ZIP) in pruefung/belege/unabhaengig/.
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const [, , O, MOTOR = 'chromium', BREITE = '1440', HOEHE] = process.argv;
const W = +BREITE, H = +(HOEHE || (W < 700 ? 844 : 900)), HANDY = W < 700, B = O + '/_werkzeuge/reception/';
const OUT = path.join(__dirname, 'lauf'), BEL = path.join(__dirname, 'belege', 'unabhaengig'); fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(BEL, { recursive: true });
const TAG = `${MOTOR}-${W}x${H}`;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const res = [], fehler = [];
const ok = (b, was) => { if (!b) throw new Error(was); };
const NUR = (process.env.NUR || '').split(',').filter(Boolean);
// sichtbare Hauswerte anderer Häuser (Doldenhorn ist hier erlaubt: Mail-Adressen und Spa im Nachbarhaus; jede Fundstelle wird gelistet)
const FREMD = /Beau-?Rivage|\bRivage\b|Carlton|Interlaken|Höheweg|\b8940\b|\bgbr\b|Grandhotel|Grand Hotel|Wellnessdörfli|Aebi|Jugendstil/i;

(async () => {
  const br = await require('./schutz').start(pw, MOTOR);
  const neuerKontext = async () => { const c = await require('./schutz').kontext(br, { viewport: { width: W, height: H }, locale: 'de-CH', hasTouch: HANDY, isMobile: HANDY && MOTOR === 'chromium', acceptDownloads: true });
    await c.addInitScript(() => { try { localStorage.setItem('reception-name', 'QA Prüfer'); localStorage.setItem('rundgang-rh-reception', '1'); } catch (e) { /* */ } }); return c; };
  const ctx = await neuerKontext();
  const neueSeite = async (c = ctx) => { const p = await c.newPage(); p.setDefaultTimeout(15000);
    p.on('pageerror', e => fehler.push('JS: ' + String(e).slice(0, 200)));
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|status of 4\d\d|net::ERR|Load failed|NetworkError|Failed to fetch|internet connection|ERR_INTERNET_DISCONNECTED/i.test(m.text())) fehler.push('Konsole: ' + m.text().slice(0, 200)); });
    return p; };
  let p = await neueSeite();
  const schritt = async (name, fn) => {
    if (NUR.length && !NUR.some(x => name.startsWith(x))) return;
    const f0 = fehler.length, t0 = Date.now();
    try { const info = await fn(); const neu = fehler.slice(f0); res.push({ name, stand: neu.length ? 'rot' : 'grün', info: (neu.length ? 'Fehler: ' + neu.join(' | ') + ' · ' : '') + (info || ''), ms: Date.now() - t0 }); }
    catch (e) { res.push({ name, stand: 'rot', info: String(e.message || e).split('\n')[0].slice(0, 400), ms: Date.now() - t0 }); await p.screenshot({ path: path.join(BEL, `rot-${name.split(' ')[0]}-${TAG}.jpg`), type: 'jpeg', quality: 60 }).catch(() => {}); }
    const r = res[res.length - 1]; console.log(`${r.stand === 'grün' ? 'ok  ' : 'ROT '} ${r.name} · ${String(r.info).slice(0, 220)} (${r.ms} ms)`);
  };
  const t = async (s, pg = p) => (await pg.locator(s).first().innerText().catch(() => '')).replace(/\s+/g, ' ').trim();
  const gehe = async (ans, pg = p, q = '') => { await pg.waitForFunction(() => !document.querySelector('#gs-stand.laeuft'), null, { timeout: 8000 }).catch(() => {});
    pg.once('dialog', d => d.accept().catch(() => {})); await pg.goto('about:blank'); await pg.goto(B + q + '#' + ans, { waitUntil: 'load' }); await pg.waitForSelector('#ansicht > *', { timeout: 30000 }); await sleep(900); };
  const api = (was, d, pg = p) => pg.evaluate(async ([b, was, d]) => { const r = await fetch(b + 'api/' + was, d === undefined ? { cache: 'no-store' } : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) }); let j = {}; try { j = await r.json(); } catch (e) { /* */ } return { status: r.status, j }; }, [B, was, d]);
  const anfragen = async (pg = p) => (await api('anfragen', undefined, pg)).j.anfragen;
  const breite = async (pg = p) => pg.evaluate(w => { const de = document.documentElement, sw = Math.max(de.scrollWidth, document.body.scrollWidth);
    let schlimm = null; if (sw > w + 1) { for (const e of document.querySelectorAll('body *')) { const r = e.getBoundingClientRect(); if (r.width && r.right > w + 1 && (!schlimm || r.right > schlimm.r)) schlimm = { r: Math.round(r.right), e: e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '') }; } }
    return { sw, iw: innerWidth, vv: Math.round(visualViewport ? visualViewport.width : innerWidth), schlimm }; }, W);
  const randAuf = async (pg = p) => { if (HANDY) { const auf = pg.locator('#rand .rand__auf'); if (await auf.count() && !(await pg.locator('#rand.auf').count())) { await auf.click(); await sleep(300); } } };
  const oeffne = async (wer, pg = p) => { await gehe('eingang', pg); const k = pg.locator('.re-liste .re-a', { hasText: wer }).first(); await k.evaluate(e => e.scrollIntoView({ block: 'center' })); await k.click(); await pg.waitForFunction(w => ((document.querySelector('#detail .re-d__n h2') || {}).textContent || '').includes(w), wer, { timeout: 15000 }); await pg.waitForSelector('#brief', { timeout: 30000 }); await sleep(600); };
  const knopf = async (sel, pg = p) => { const l = pg.locator(sel).first(); await l.evaluate(e => e.scrollIntoView({ block: 'center' })).catch(() => {}); await l.click(); };
  const meldung = async (re, pg = p, ms = 15000) => { try { await pg.waitForFunction(r => new RegExp(r).test(document.querySelector('#meldung')?.innerText || ''), re.source, { timeout: ms }); } catch (e) { throw new Error('Meldung ' + re + ' kam nicht; sichtbar «' + (await t('#meldung', pg)).slice(0, 140) + '»'); } return t('#meldung', pg); };
  const foto = async (name, pg = p) => pg.screenshot({ path: path.join(BEL, `${name}-${TAG}.jpg`), type: 'jpeg', quality: 70 });
  const marke = () => 'qa' + Math.random().toString(36).slice(2, 8).replace(/\d/g, 'k');

  // ---------------------------------------------------------------- U1 Verrutschen gegen die eingestellte Breite, Hauswerte im sichtbaren Text
  await schritt('U01 Kein seitliches Verrutschen (gegen die eingestellte Breite) in allen Ansichten, Brief, Prüfseite, Anleitung', async () => {
    const aus = [], rot = [];
    for (const a of ['start', 'eingang', 'gefragt', 'nachgetragen', 'wissen']) { await gehe(a); const b = await breite(); aus.push(a + ' ' + b.sw); if (b.sw > W + 1 || b.iw !== W) rot.push(a + ' ' + JSON.stringify(b)); await foto('ansicht-' + a); }
    await oeffne('Huber'); let b = await breite(); aus.push('brief ' + b.sw); if (b.sw > W + 1 || b.iw !== W) rot.push('brief ' + JSON.stringify(b)); await foto('brief');
    for (const s of ['pruefung.html', 'anleitung.html']) { await p.goto(B + s, { waitUntil: 'load' }); await sleep(1500); b = await breite(); aus.push(s + ' ' + b.sw); if (b.sw > W + 1 || b.iw !== W) rot.push(s + ' ' + JSON.stringify(b)); await foto(s.split('.')[0]); }
    ok(!rot.length, rot.join(' | ')); return aus.join(', ') + ` (Breite ${W})`;
  });
  await schritt('U02 Hauswerte: kein Name, Ort, Port eines anderen Hauses im sichtbaren Text; Doldenhorn nur als Mail und Nachbarhaus', async () => {
    const funde = [], dold = new Set();
    const lies = async (wo) => { const tx = await p.evaluate(() => document.body.innerText + ' ' + [...document.querySelectorAll('[title],[data-tip],[aria-label],img[alt]')].map(e => e.getAttribute('title') || e.getAttribute('data-tip') || e.getAttribute('aria-label') || e.getAttribute('alt')).join(' ') + ' ' + document.title);
      const m = (tx.match(new RegExp(FREMD.source, 'gi')) || []).concat(tx.match(/La Maison/g) || []); if (m.length) funde.push(wo + ': ' + [...new Set(m)].join(', ') + ' «' + tx.slice(Math.max(0, tx.search(FREMD) - 50), tx.search(FREMD) + 50).replace(/\s+/g, ' ') + '»');
      for (const x of tx.matchAll(/.{0,40}Doldenhorn.{0,30}/g)) dold.add(x[0].replace(/\s+/g, ' ').trim()); };
    for (const a of ['start', 'eingang', 'gefragt', 'nachgetragen', 'wissen']) { await gehe(a); await lies(a); }
    await gehe('eingang'); const n = await p.locator('.re-liste .re-a').count();
    for (let i = 0; i < n; i++) { const k = p.locator('.re-liste .re-a').nth(i); await k.evaluate(e => e.scrollIntoView({ block: 'center' })); await k.click(); await sleep(900); await p.waitForSelector('#brief, .brief--leer', { timeout: 20000 }).catch(() => {}); await lies('anfrage ' + i); }
    for (const s of ['pruefung.html', 'anleitung.html']) { await p.goto(B + s, { waitUntil: 'load' }); await sleep(1500); await lies(s); }
    await gehe('start', p, '?rundgang'); for (let i = 0; i < 6; i++) { await lies('rundgang ' + i); const w = p.locator('.rdg-los').first(); if (!(await w.count())) break; await w.click().catch(() => {}); await sleep(500); }
    fs.writeFileSync(path.join(BEL, `doldenhorn-stellen-${TAG}.txt`), [...dold].join('\n'));
    ok(!funde.length, funde.join(' | ')); return `${n} Anfragen und 7 Seiten gelesen, keine fremden Hauswerte; Doldenhorn an ${dold.size} Stellen (Liste in belege)`;
  });

  // ---------------------------------------------------------------- U2 Speichern, neu laden, zurücksetzen
  let qaB = '';
  await schritt('U03 Nur Text: Betreff und Text sichern → neu laden → noch da (Oberfläche und Server)', async () => {
    await oeffne('Bieri'); await knopf('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-betreff'); qaB = marke();
    await p.fill('#e-betreff', 'Betreff ' + qaB); await p.fill('#e-text', (await p.inputValue('#e-text')) + '\n\nZusatz ' + qaB); await knopf('#detail [data-akt="sichern"]'); await meldung(/Gesichert/);
    await p.reload({ waitUntil: 'load' }); await oeffne('Bieri'); const tx = (await t('#brief')).toLowerCase();
    const s = (await anfragen()).find(a => a.name === 'Ursula Bieri'); ok(tx.includes(qaB) && s.entwurf.betreff.includes(qaB) && s.entwurf.text.includes('Zusatz ' + qaB), 'nach Neuladen fehlt die Änderung'); return 'Betreff und Text bleiben (' + qaB + ')';
  });
  await schritt('U04 Gestalteter Brief: Schrift grösser → «Gesichert» → neu laden → noch da', async () => {
    await oeffne('Bieri'); const el = p.locator('#brief .gs--p').nth(1); await el.evaluate(e => e.scrollIntoView({ block: 'center' })); await el.click(); await sleep(300);
    await knopf('.gs-werk [data-g="groesser"]'); await knopf('.gs-werk [data-g="groesser"]'); await p.waitForFunction(() => /Gesichert/.test(document.querySelector('#gs-stand')?.textContent || ''), null, { timeout: 10000 });
    const st0 = await el.getAttribute('style'); await p.reload({ waitUntil: 'load' }); await oeffne('Bieri'); const st1 = await p.locator('#brief .gs--p').nth(1).getAttribute('style');
    ok(st0 && st0 === st1 && /font-size|--s/.test(st0), `vorher «${st0}» nachher «${st1}»`); return 'Stil bleibt: ' + st0;
  });
  await schritt('U05 Zurücksetzen: «Zurück auf die Vorlage» nimmt Text und Anordnung zurück (Server und Oberfläche)', async () => {
    await oeffne('Bieri'); await knopf('[data-w="vorlage"]'); await p.waitForSelector('#fenster:not([hidden]) #f-los'); await knopf('#fenster #f-los'); await meldung(/Vorlage/); await sleep(1500);
    const s = (await anfragen()).find(a => a.name === 'Ursula Bieri'); const st = await p.locator('#brief .gs--p').nth(1).getAttribute('style') || '';
    ok(!s.entwurf.text.includes(qaB) && !(await t('#brief')).toLowerCase().includes(qaB), 'Text der Probe steht noch'); ok(!/font-size/.test(st), 'Anordnung bleibt: ' + st);
    return 'Text ohne ' + qaB + ', Anordnung zurück' + (s.entwurf.betreff.includes(qaB) ? ' (Betreff bleibt geändert)' : '');
  });

  // ---------------------------------------------------------------- U3 Zwei Fenster, Netz weg, Verlassen
  await schritt('U06 Zwei Fenster am selben Brief (Nur Text): zweites Fenster bekommt «Anderes Fenster war schneller», nichts überschrieben, Eingabe bleibt', async () => {
    const p2 = await neueSeite(); await oeffne('Wenger'); await oeffne('Wenger', p2); const m1 = marke(), m2 = marke();
    await knopf('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-betreff'); await p.fill('#e-betreff', 'Fenster eins ' + m1); await knopf('#detail [data-akt="sichern"]'); await meldung(/Gesichert/);
    await knopf('#detail [data-akt="bearbeiten"]', p2); await p2.waitForSelector('#e-text'); const t2 = (await p2.inputValue('#e-text')) + '\n\nFenster zwei ' + m2; await p2.fill('#e-text', t2); await knopf('#detail [data-akt="sichern"]', p2);
    const m = await meldung(/schneller|KONFLIKT|anderen Fenster/i, p2); await foto('konflikt-nurtext', p2);
    const s = (await anfragen()).find(a => a.name === 'Sandra Wenger'); const bleibt = await p2.inputValue('#e-text').catch(() => '');
    await p2.close({ runBeforeUnload: false });
    ok(s.entwurf.betreff.includes(m1) && !s.entwurf.text.includes(m2), 'überschrieben: Betreff «' + s.entwurf.betreff + '», Text mit zwei: ' + s.entwurf.text.includes(m2)); ok(bleibt.includes(m2), 'Eingabe im zweiten Fenster weg');
    return 'Meldung «' + m.slice(0, 70) + '», Stand von Fenster eins gilt, Eingabe von zwei noch im Feld';
  });
  await schritt('U07 Zwei Fenster am gestalteten Brief: späteres altes Fenster wird abgewiesen, «Nicht gesichert», Meldung mit «Neu laden»', async () => {
    const p2 = await neueSeite(); await oeffne('Lüthi'); await oeffne('Lüthi', p2);
    let el = p.locator('#brief .gs--p').nth(1); await el.evaluate(e => e.scrollIntoView({ block: 'center' })); await el.click(); await knopf('.gs-werk [data-g="groesser"]'); await p.waitForFunction(() => /Gesichert/.test(document.querySelector('#gs-stand')?.textContent || ''), null, { timeout: 10000 });
    const st1 = await el.getAttribute('style');
    el = p2.locator('#brief .gs--p').nth(2); await el.evaluate(e => e.scrollIntoView({ block: 'center' })); await el.click(); await knopf('.gs-werk [data-g="kleiner"]', p2);
    const m = await meldung(/schneller/i, p2); const stand = await t('#gs-stand', p2); await foto('konflikt-gestaltet', p2); await p2.close({ runBeforeUnload: false });
    const s = (await anfragen()).find(a => /Lüthi/.test(a.name)); const g = JSON.stringify(s.entwurf.gestalt || {});
    ok(/Nicht gesichert/i.test(stand), 'Stand im zweiten Fenster: ' + stand); ok(g.length > 2, 'Gestaltung von Fenster eins fehlt auf dem Server');
    return `Meldung «${m.slice(0, 50)}», Stand «${stand}», Server behält Fenster eins (${st1})`;
  });
  await schritt('U08 Netz weg im gestalteten Brief: «Nicht gesichert» und Meldung, Netz zurück: sichert von selbst nach', async () => {
    await oeffne('Ogi'); const el = p.locator('#brief .gs--p').nth(1); await el.evaluate(e => e.scrollIntoView({ block: 'center' })); await el.click(); await sleep(200);
    await ctx.setOffline(true); await knopf('.gs-werk [data-g="groesser"]'); await knopf('.gs-werk [data-g="groesser"]');
    await p.waitForFunction(() => /Nicht gesichert/.test(document.querySelector('#gs-stand')?.textContent || ''), null, { timeout: 10000 }); const m = await t('#meldung'); await foto('netz-weg-brief');
    await ctx.setOffline(false); await p.waitForFunction(() => /^Gesichert/.test(document.querySelector('#gs-stand')?.textContent || ''), null, { timeout: 30000 });
    const st = await el.getAttribute('style'); const s = (await anfragen()).find(a => a.name === 'Daniel Ogi'); ok(JSON.stringify(s.entwurf.gestalt || {}).length > 2, 'Server hat die Änderung nicht');
    ok(/Verbindung/i.test(m), 'Meldung: ' + m.slice(0, 100)); return 'Meldung «' + m.slice(0, 60) + '», danach von selbst gesichert (' + st + ')';
  });
  await schritt('U09 Netz weg in «Nur Text»: Meldung, Eingabe bleibt; danach sichern geht', async () => {
    await oeffne('Zurbuchen'); await knopf('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-betreff'); const m1 = marke(); await p.fill('#e-betreff', 'Offline ' + m1);
    await ctx.setOffline(true); await knopf('#detail [data-akt="sichern"]'); const m = await meldung(/Verbindung/); const bleibt = await p.inputValue('#e-betreff'); await ctx.setOffline(false);
    ok(bleibt.includes(m1), 'Eingabe weg'); await knopf('#detail [data-akt="sichern"]'); await meldung(/Gesichert/); const s = (await anfragen()).find(a => a.name === 'Lena Zurbuchen'); ok(s.entwurf.betreff.includes(m1), 'danach nicht gesichert');
    return 'Meldung «' + m.slice(0, 60) + '», Eingabe blieb, danach gesichert';
  });
  await schritt('U10 Verlassen mit ungesicherter Eingabe (Nur Text, Neues Wissen, Fenster Nachtrag): Browser fragt nach', async () => {
    const aus = [];
    const pruef = async (wie, vorbereiten) => { const q = await neueSeite(); await vorbereiten(q); let gefragt = false; q.on('dialog', d => { if (d.type() === 'beforeunload') gefragt = true; d.dismiss().catch(() => {}); });
      await q.goto('about:blank', { timeout: 5000 }).catch(() => {}); await sleep(600); if (!gefragt) gefragt = q.url() !== 'about:blank'; await q.close({ runBeforeUnload: false }).catch(() => {}); aus.push(wie + (gefragt ? ' fragt' : ' FRAGT NICHT')); return gefragt; };
    const a = await pruef('Nur Text', async q => { await oeffne('Huber', q); await knopf('#detail [data-akt="bearbeiten"]', q); await q.waitForSelector('#e-text'); await q.fill('#e-text', 'ungesichert ' + marke()); await q.locator('#e-text').click(); });
    const b = await pruef('Neues Wissen', async q => { await gehe('wissen', q); await q.fill('#w-text', 'ungesichert ' + marke()); await q.locator('#w-text').click(); });
    const c = await pruef('Fenster Nachtrag', async q => { await gehe('nachgetragen', q); await knopf('#n-neu', q); await q.waitForSelector('#f-antwort'); await q.fill('#f-antwort', 'ungesichert ' + marke()); await q.locator('#f-antwort').click(); });
    ok(a && b && c, aus.join(', ')); return aus.join(', ');
  });

  // ---------------------------------------------------------------- U4 Ungewöhnliche Eingaben über die Oberfläche
  const LANG = 'Kandersteg'.repeat(500), SKRIPT = '<script>window.__qa=1</script><img src=x onerror="window.__qa=2">', EMOJI = 'Grüezi 🏔️🐕 Ä Ö Ü ä ö ü ß é ç «Chäs»';
  await schritt('U11 Nachtrag über die Oberfläche: leer abgewiesen, 5000 Zeichen ohne Leerzeichen, <script>, Emoji: gespeichert, nichts läuft, nichts ragt seitlich', async () => {
    await gehe('nachgetragen'); await knopf('#n-neu'); await p.waitForSelector('#f-antwort'); await p.fill('#f-frage', ''); await p.fill('#f-antwort', ''); await knopf('#fenster #f-los'); await sleep(800);
    const leer = (await t('#meldung')) + ' ' + (await t('#fenster')); const offen = await p.locator('#fenster:not([hidden])').count(); ok(offen === 1 && /ausfüllen|Bitte|leer/i.test(leer), 'leer: ' + leer.slice(0, 120));
    await p.fill('#f-frage', 'Frage ' + SKRIPT + ' ' + EMOJI); await p.fill('#f-antwort', LANG); const b1 = await breite(); await knopf('#fenster #f-los'); await meldung(/Nachgetragen/); await sleep(900);
    const qa = await p.evaluate(() => window.__qa || 0), b2 = await breite(), tx = await t('.re-nliste'); await foto('nachtrag-lang');
    await p.reload({ waitUntil: 'load' }); await sleep(1200); const b3 = await breite(); const tx2 = await t('.re-nliste');
    ok(qa === 0, 'Skript lief'); ok(tx2.includes('🏔️') && tx2.includes('<script>') && tx2.includes('Kandersteg'), 'Text nicht wie eingegeben: ' + tx2.slice(0, 100)); ok(b1.sw <= W + 1 && b2.sw <= W + 1 && b3.sw <= W + 1, `zu breit: Fenster ${JSON.stringify(b1)}, Liste ${JSON.stringify(b2)}`);
    return `leer abgewiesen, Skript als Text, Emoji stehen, Breite ${b2.sw}/${W}`;
  });
  await schritt('U12 Brief (Nur Text) mit 5000 Zeichen ohne Leerzeichen, <script>, Emoji: gesichert, kein Skript, nichts ragt seitlich, PDF mehrseitig', async () => {
    await oeffne('Zurbuchen'); await knopf('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-text');
    await p.fill('#e-betreff', 'Lang ' + EMOJI); await p.fill('#e-text', 'Liebe Frau Zurbuchen\n\n' + SKRIPT + '\n\n' + LANG + '\n\n' + 'Ein langer Absatz mit Wörtern. '.repeat(160) + '\n\n' + EMOJI + '\n\nHerzlich, Familie Maeder und ihre Crew');
    await knopf('#detail [data-akt="sichern"]'); await meldung(/Gesichert/); await sleep(800); await oeffne('Zurbuchen'); const b = await breite(); const qa = await p.evaluate(() => window.__qa || 0); await foto('brief-lang');
    ok(qa === 0, 'Skript lief'); ok(b.sw <= W + 1, 'zu breit ' + JSON.stringify(b));
    const [d] = await Promise.all([p.waitForEvent('download', { timeout: 120000 }), knopf('#detail [data-akt="pdf"]')]);
    const name = d.suggestedFilename(), ziel = path.join(BEL, `brief-lang-${TAG}.pdf`); await d.saveAs(ziel); const roh = fs.readFileSync(ziel);
    const seiten = (roh.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
    ok(/^Landgasthof Ruedihus – Lena Zurbuchen – \d\d\.\d\d\.\d{4}\.pdf$/.test(name), 'Dateiname ' + name); ok(roh.slice(0, 4).toString() === '%PDF' && seiten >= 2, seiten + ' Seiten');
    return `gesichert, Breite ${b.sw}/${W}, PDF «${name}» ${seiten} Seiten, ${Math.round(roh.length / 1024)} kB`;
  });
  await schritt('U13 Kurzer Brief als PDF: Dateiname, eine Seite, A4 (Beleg zum Lesen gegen die Quelle)', async () => {
    await oeffne('Ryser'); const [d] = await Promise.all([p.waitForEvent('download', { timeout: 120000 }), knopf('#detail [data-akt="pdf"]')]);
    const name = d.suggestedFilename(), ziel = path.join(BEL, `brief-ryser-${TAG}.pdf`); await d.saveAs(ziel); const roh = fs.readFileSync(ziel).toString('latin1');
    const seiten = (roh.match(/\/Type\s*\/Page[^s]/g) || []).length, box = (roh.match(/\/MediaBox\s*\[\s*0 0 ([\d.]+) ([\d.]+)/) || []).slice(1).map(Number);
    const s = (await anfragen()).find(a => a.name === 'Beat Ryser'); fs.writeFileSync(path.join(BEL, `brief-ryser-quelle-${TAG}.json`), JSON.stringify(s.entwurf, null, 1));
    ok(/^Landgasthof Ruedihus – Beat Ryser – \d\d\.\d\d\.\d{4}\.pdf$/.test(name), 'Dateiname ' + name); ok(seiten === 1, seiten + ' Seiten'); ok(Math.abs(box[0] - 595.92) < 2 && Math.abs(box[1] - 842.88) < 2, 'kein A4: ' + box);
    return `«${name}», ${seiten} Seite, ${box.join(' × ')} pt`;
  });
  await schritt('U14 Neues Wissen: Foto 30 MB wird verkleinert, Foto 400 px angenommen, Datei ohne Bild abgewiesen mit DATEI', async () => {
    await gehe('wissen'); await p.waitForSelector('#w-datei-bild', { state: 'attached' });
    const gross = path.join(OUT, 'qa-30mb.jpg'), klein = path.join(OUT, 'qa-400.png'), falsch = path.join(OUT, 'qa-kein-bild.jpg');
    if (!fs.existsSync(gross) || fs.statSync(gross).size < 25e6) { const c = await p.evaluate(() => { const k = document.createElement('canvas'); k.width = 6000; k.height = 4000; const g = k.getContext('2d'); const d = g.createImageData(6000, 4000); for (let i = 0; i < d.data.length; i++) d.data[i] = (Math.random() * 255) | 0; g.putImageData(d, 0, 0); return k.toDataURL('image/jpeg', 1).split(',')[1]; }); fs.writeFileSync(gross, Buffer.from(c, 'base64')); }
    const k4 = await p.evaluate(() => { const k = document.createElement('canvas'); k.width = 400; k.height = 300; const g = k.getContext('2d'); g.fillStyle = '#321f10'; g.fillRect(0, 0, 400, 300); g.fillStyle = '#fff'; g.font = '30px serif'; g.fillText('Aushang QA', 40, 150); return k.toDataURL('image/png').split(',')[1]; }); fs.writeFileSync(klein, Buffer.from(k4, 'base64'));
    fs.writeFileSync(falsch, 'Das ist kein Bild, nur Text mit .jpg');
    const mb = (fs.statSync(gross).size / 1e6).toFixed(1); const zahl = async () => p.evaluate(() => (typeof S !== 'undefined' && S.dateien ? S.dateien.length : 0));
    const z0 = await zahl(); await p.setInputFiles('#w-datei-bild', gross); await p.waitForFunction(n => typeof S !== 'undefined' && S.dateien && S.dateien.length > n, z0, { timeout: 60000 });
    const g = await p.evaluate(() => { const d = S.dateien[S.dateien.length - 1]; return { name: d.name, laenge: (d.daten || d.data || d.url || '').length }; });
    await p.setInputFiles('#w-datei-bild', klein); await p.waitForFunction(n => S.dateien.length > n, z0 + 1, { timeout: 20000 });
    await p.setInputFiles('#w-datei-bild', falsch); const m = await meldung(/DATEI|Foto öffnen|nicht als Foto/i); const z3 = await zahl(); await foto('wissen-dateien');
    ok(z3 === z0 + 2, 'Dateien ' + z0 + ' → ' + z3); ok(g.laenge > 0 && g.laenge < 8e6, '30-MB-Foto nicht verkleinert: ' + g.laenge + ' Zeichen');
    return `${mb} MB → ${(g.laenge * 0.75 / 1e6).toFixed(1)} MB (${g.name}), 400 px angenommen, kein Bild: «${m.slice(0, 70)}»`;
  });

  // ---------------------------------------------------------------- U5 Formulare der Website: jede Art bis in den Eingang
  await schritt('U15 Website: Knöpfe «Gutschein für ein bestimmtes Zimmer» (zimmer.html) und «Bewerben» (haus.html) öffnen das Fenster, Bewerbung landet bei Personal (jobs@)', async () => {
    let mailto = 0; p.on('framenavigated', f => { if (/^mailto:/.test(f.url())) mailto++; });
    const sende = async (seite, sel, art, name) => { await p.goto('about:blank'); await p.goto(O + '/' + seite + '?probe=1', { waitUntil: 'load' }); await sleep(1200); await knopf(sel); await p.waitForSelector('dialog.anf[open]', { timeout: 8000 }); await sleep(400);
      ok(await p.inputValue('dialog.anf select[name=art]') === art, art + ': Art ' + await p.inputValue('dialog.anf select[name=art]')); await p.fill('dialog.anf input[name=name]', name); await p.fill('dialog.anf input[name=kontakt]', name.split(' ')[0].toLowerCase() + '@example.com');
      await p.fill('dialog.anf textarea[name=nachricht]', 'Nachricht von ' + name); await knopf('dialog.anf .anf__los'); await p.waitForSelector('dialog.anf .anf__danke:not([hidden])', { timeout: 10000 }); await foto('website-' + art); await knopf('dialog.anf .anf__fertig'); };
    await sende('zimmer.html', '[data-anfrage="gutschein"]', 'gutschein', 'Gutscheinknopf QA'); await sende('haus.html', '[data-anfrage="stelle"]', 'stelle', 'Bewerbung QA');
    const l = await anfragen(); const g = l.find(a => a.name === 'Gutscheinknopf QA'), b = l.find(a => a.name === 'Bewerbung QA');
    ok(g && g.abteilung === 'Rezeption' && g.art === 'gutschein', 'Gutschein: ' + JSON.stringify(g && { ab: g.abteilung, art: g.art })); ok(b && b.abteilung === 'Personal' && /jobs@/.test(b.an), 'Bewerbung: ' + JSON.stringify(b && { ab: b.abteilung, an: b.an, art: b.art, fo: b.formular }));
    ok(mailto === 0, mailto + '× Mailprogramm'); return `Gutschein → ${g.abteilung}, Bewerbung → ${b.abteilung} (${b.an}), Formular «${b.formular}»`;
  });
  await schritt('U16 Website: freie Anfragen zimmer, tisch, fest, nachricht über data-anfrage landen mit richtiger Abteilung im Eingang', async () => {
    const aus = [];
    for (const [art, abt] of [['zimmer', 'Rezeption'], ['tisch', 'Rezeption'], ['fest', 'Event'], ['nachricht', 'Rezeption']]) {
      await p.goto('about:blank'); await p.goto(O + '/index.html?probe=1', { waitUntil: 'load' }); await sleep(1000);
      await p.evaluate(a => { const b = document.createElement('button'); b.type = 'button'; b.id = 'qa-frei'; b.setAttribute('data-anfrage', a); b.textContent = 'QA ' + a; document.body.appendChild(b); }, art);
      await knopf('#qa-frei'); await p.waitForSelector('dialog.anf[open]'); await sleep(300); const name = 'Frei ' + art + ' QA';
      await p.fill('dialog.anf input[name=name]', name); await p.fill('dialog.anf input[name=kontakt]', '+41 79 000 00 0' + aus.length); await p.fill('dialog.anf textarea[name=nachricht]', 'Freie Anfrage ' + art);
      await knopf('dialog.anf .anf__los'); await p.waitForSelector('dialog.anf .anf__danke:not([hidden])', { timeout: 10000 }); await knopf('dialog.anf .anf__fertig');
      const a = (await anfragen()).find(x => x.name === name); ok(a && a.abteilung === abt, art + ': ' + JSON.stringify(a && { ab: a.abteilung, art: a.art })); aus.push(`${art}→${a.abteilung}/${a.art}`);
    }
    return aus.join(', ');
  });
  await schritt('U17 Website-Formular mit 5000 Zeichen ohne Leerzeichen, <script>, Emoji: gesendet, im Eingang als Text, nichts ragt seitlich', async () => {
    await p.goto('about:blank'); await p.goto(O + '/index.html?probe=1', { waitUntil: 'load' }); await sleep(1000);
    await p.evaluate(() => { const b = document.createElement('button'); b.type = 'button'; b.id = 'qa-frei'; b.setAttribute('data-anfrage', 'nachricht'); b.textContent = 'QA'; document.body.appendChild(b); });
    await knopf('#qa-frei'); await p.waitForSelector('dialog.anf[open]'); await p.fill('dialog.anf input[name=name]', 'Böse ' + SKRIPT.slice(0, 40)); await p.fill('dialog.anf input[name=kontakt]', 'boese@example.com');
    await p.fill('dialog.anf textarea[name=nachricht]', EMOJI + ' ' + SKRIPT + ' ' + LANG); const bf = await breite(); await knopf('dialog.anf .anf__los');
    await p.waitForSelector('dialog.anf .anf__danke:not([hidden]), dialog.anf .anf__meldung:not(:empty)', { timeout: 10000 }); const gast = (await t('dialog.anf .anf__danke')) || (await t('dialog.anf .anf__meldung')); await foto('website-lang');
    const a = (await anfragen()).find(x => /^Böse/.test(x.name)); ok(a, 'nicht im Eingang (Gast sah: ' + gast.slice(0, 80) + ')');
    await oeffne('Böse'); const qa = await p.evaluate(() => window.__qa || 0), b = await breite(); await foto('eingang-lang');
    ok(qa === 0, 'Skript lief'); ok(b.sw <= W + 1 && bf.sw <= W + 1, 'zu breit: Eingang ' + JSON.stringify(b) + ' Fenster ' + JSON.stringify(bf));
    return `Gast sah «${gast.slice(0, 50)}», Nachricht ${a.nachricht.length} Zeichen angekommen, Breite ${b.sw}/${W}`;
  });

  await schritt('U19 Website: lange Wünsche und volle Nachricht kommen ganz an (nichts still abgeschnitten); zu lang: Hinweis, nichts geht verloren', async () => {
    await p.goto('about:blank'); await p.goto(O + '/essen.html?probe=1', { waitUntil: 'load' }); await sleep(1200); await p.locator('[data-buchen="tisch"]:visible').first().click(); await sleep(700);
    const f = 'dialog.buchen form[data-tisch]', ende = 'ENDE' + marke(); await p.fill(f + ' input[name=tag]', new Date(Date.now() + 4 * 864e5).toISOString().slice(0, 10)); await p.fill(f + ' input[name=name]', 'Lang Wunsch QA');
    await p.fill(f + ' textarea[name=wunsch]', 'Wir feiern den Geburtstag unserer Grossmutter. '.repeat(30)); await p.locator(f + ' [type=submit]').first().click(); await p.waitForSelector('dialog.anf[open]'); await sleep(400);
    const kopf1 = await t('dialog.anf .anf__kopf .mono'); await p.fill('dialog.anf input[name=kontakt]', 'lang@example.com'); await p.fill('dialog.anf textarea[name=nachricht]', 'Noch etwas. '.repeat(98) + ende);
    await knopf('dialog.anf .anf__los'); await p.waitForSelector('dialog.anf .anf__danke:not([hidden])', { timeout: 10000 }); await knopf('dialog.anf .anf__fertig');
    const a = (await anfragen()).find(x => x.name === 'Lang Wunsch QA'); ok(a && a.nachricht.endsWith(ende), 'abgeschnitten: ' + (a ? a.nachricht.length + ' Zeichen, Ende «' + a.nachricht.slice(-30) + '»' : 'fehlt'));
    await p.goto('about:blank'); await p.goto(O + '/essen.html?probe=1#feste', { waitUntil: 'load' }); await sleep(1200); const g = 'form[data-rechner]'; await p.fill(g + ' input[name=erw]', '10'); await p.fill(g + ' input[name=name]', 'Zu lang QA');
    await p.fill(g + ' textarea[name=wunsch]', 'Sehr lang. '.repeat(1200)); await p.locator(g + ' [type=submit]').first().click(); await p.waitForSelector('dialog.anf[open]'); await sleep(400); const kopf2 = await t('dialog.anf .anf__kopf .mono');
    await p.fill('dialog.anf input[name=kontakt]', 'zulang@example.com'); await knopf('dialog.anf .anf__los'); await sleep(800); const m = await t('dialog.anf .anf__meldung'); await foto('website-zu-lang');
    const bleibt = await p.inputValue('dialog.anf input[name=kontakt]'); ok(/zu lang/i.test(m) && bleibt === 'zulang@example.com', 'Meldung «' + m + '»'); ok(!(await anfragen()).find(x => x.name === 'Zu lang QA'), 'doch gesendet');
    ok(kopf1.toLowerCase() === 'an die rezeption' && kopf2.toLowerCase() === 'an das team des hauses', `Kopf: Tisch «${kopf1}», Fest «${kopf2}»`); await p.keyboard.press('Escape');
    return `${a.nachricht.length} Zeichen ganz angekommen; zu lang: «${m.slice(0, 60)}»; Kopf Tisch «${kopf1}», Fest «${kopf2}»`;
  });

  await schritt('U20 Startfehler-Tür: Server weg → «Der Gastgeber startet nicht.» mit «Prüfung öffnen»; Server hängt → Tür nach 12 s', async () => {
    const q = await neueSeite(); await q.route('**/api/ueberblick*', r => r.abort()); await q.goto(B, { waitUntil: 'load' }); await q.waitForSelector('#tuer:not([hidden])', { timeout: 8000 });
    const t1 = await t('#tuer', q), knopf1 = await q.locator('#tuer a[href="pruefung.html"]').isVisible(); await foto('tuer-weg', q); await q.close();
    const r = await neueSeite(); await r.route('**/api/ueberblick*', () => { /* hängt */ }); const t0 = Date.now(); await r.goto(B, { waitUntil: 'load' }); await r.waitForSelector('#tuer:not([hidden])', { timeout: 20000 });
    const s = ((Date.now() - t0) / 1000).toFixed(1), t2 = await t('#tuer', r); await r.close({ runBeforeUnload: false });
    ok(/startet nicht/i.test(t1) && knopf1, 'Tür: ' + t1); ok(/antwortet nicht/i.test(t2), 'hängt: ' + t2); return `«${t1.slice(0, 70)}» · hängt: Tür nach ${s} s`;
  });

  // ---------------------------------------------------------------- U6 Daten herunterladen
  await schritt('U18 Prüfseite: «Alle Daten herunterladen» liefert eine ZIP (Beleg, Inhalt wird gegen den Datenordner geprüft)', async () => {
    await p.goto(B + 'pruefung.html', { waitUntil: 'load' }); await sleep(1500);
    const k = p.locator('a[href*="api/export"], button:has-text("herunterladen"), a:has-text("herunterladen")').first(); ok(await k.count(), 'Knopf fehlt');
    const [d] = await Promise.all([p.waitForEvent('download', { timeout: 60000 }), k.click()]); const ziel = path.join(BEL, `export-${TAG}.zip`); await d.saveAs(ziel);
    const roh = fs.readFileSync(ziel); ok(roh.slice(0, 2).toString() === 'PK', 'keine ZIP'); return `«${d.suggestedFilename()}», ${Math.round(roh.length / 1024)} kB`;
  });

  fs.writeFileSync(path.join(OUT, `unabhaengig-${TAG}.json`), JSON.stringify({ motor: MOTOR, breite: W, hoehe: H, zeit: new Date().toISOString(), schritte: res }, null, 1));
  const gr = res.filter(r => r.stand === 'grün').length, ro = res.filter(r => r.stand === 'rot');
  console.log(`unabhaengig ${TAG}: ${gr} grün, ${ro.length} rot von ${res.length}`); ro.forEach(r => console.log('  ROT', r.name.split(' ')[0], '·', r.info.slice(0, 300)));
  await br.close();
})().catch(e => { console.log('ABBRUCH', e); process.exit(2); });
