// Abnahme Der Gastgeber (La Réception) · Landgasthof Ruedihus (übernommen vom Doldenhorn, dort vom Carlton-Europe, pruefung/abnahme.js; Master Werkzeug-Bau Abschnitt 8): was gegenprobe.js nicht bedient.
//   node abnahme.js <url-des-werkzeugs> [chromium|webkit|firefox] [breite] [höhe]
// Läuft gegen einen Prüf-Server mit Wegwerf-Daten und Probe-Antworten: RECEPTION_KI=0 RECEPTION_DATEN=<leer> python3 server.py <port>
// Ergebnis: pruefung/lauf/abnahme-<motor>-<breite>.json, Bildschirmfotos in pruefung/belege/.
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const [, , BASIS, MOTOR = 'chromium', BREITE = '1440', HOEHE] = process.argv;
const W = +BREITE, H = +(HOEHE || (W < 700 ? 844 : 900)), HANDY = W < 700;
const OUT = path.join(__dirname, 'lauf'), BEL = path.join(__dirname, 'belege'); fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(BEL, { recursive: true });
const ORIGIN = new URL(BASIS).origin;
const res = [], fehlerSeite = [];
const sleep = ms => new Promise(r => setTimeout(r, ms));
const zeig = r => console.log(`${r.stand === 'grün' ? 'ok  ' : r.stand === 'rot' ? 'ROT ' : '–   '} ${r.name} · ${String(r.info || '').slice(0, 150)}`);
const ok = (b, was) => { if (!b) throw new Error(was); };
const NUR = (process.env.NUR || '').split(',').filter(Boolean);

(async () => {
  const br = await require('./schutz').start(pw, MOTOR);
  const neuerKontext = () => require('./schutz').kontext(br, { viewport: { width: W, height: H }, locale: 'de-CH', hasTouch: HANDY, isMobile: HANDY && MOTOR === 'chromium', acceptDownloads: true });
  const ctx = await neuerKontext();
  await ctx.addInitScript(() => { try { localStorage.setItem('reception-name', 'QA Prüfer'); } catch (e) { /* */ } });
  let p;
  const neueSeite = async () => { p = await ctx.newPage(); p.setDefaultTimeout(15000); p.on('pageerror', e => fehlerSeite.push('JS: ' + String(e).slice(0, 200)));
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|status of 4\d\d|ERR_INTERNET_DISCONNECTED|net::ERR|Load failed|NetworkError|Failed to fetch/.test(m.text())) fehlerSeite.push('Konsole: ' + m.text().slice(0, 200)); });
    p.on('dialog', d => d.dismiss().catch(() => {})); };
  await neueSeite();
  if (0) p.on('pageerror', e => fehlerSeite.push('JS: ' + String(e).slice(0, 200)));
  p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|status of 4\d\d|ERR_INTERNET_DISCONNECTED|net::ERR|Load failed|NetworkError|Failed to fetch/.test(m.text())) fehlerSeite.push('Konsole: ' + m.text().slice(0, 200)); });
  p.on('dialog', d => d.dismiss().catch(() => {}));
  const schritt = async (name, fn) => {
    if (NUR.length && !NUR.some(x => name.startsWith(x))) return;
    const f0 = fehlerSeite.length;
    try { const info = await fn(); const neu = fehlerSeite.slice(f0); res.push({ name, stand: neu.length ? 'rot' : 'grün', info: (neu.length ? 'Fehler: ' + neu.join(' | ') + ' · ' : '') + (info || '') }); }
    catch (e) { res.push({ name, stand: 'rot', info: String(e.message || e).split('\n')[0].slice(0, 300) + ' · Adresse ' + p.url() + ' · #ansicht ' + (await p.locator('#ansicht').innerHTML().catch(() => '?')).length + ' Zeichen' }); await p.screenshot({ path: path.join(BEL, 'fehler-' + name.split(' ')[0].replace(/\W/g, '') + '-' + MOTOR + '-' + W + '.jpg'), type: 'jpeg', quality: 60 }).catch(() => {}); }
    zeig(res[res.length - 1]);
  };
  const t = async s => (await p.locator(s).first().innerText().catch(() => '')).replace(/\s+/g, ' ').trim();
  const gehe = async (ans, q = '') => { await p.goto('about:blank'); await p.goto(BASIS + q + '#' + ans, { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *', { timeout: 30000 }); await sleep(900); };
  const foto = async name => { await p.screenshot({ path: path.join(BEL, `${name}-${MOTOR}-${W}x${H}.jpg`), quality: 70, type: 'jpeg' }); };
  const api = (was, d) => p.evaluate(async ([was, d]) => { const r = await fetch('api/' + was, d === undefined ? {} : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) }); let j = {}; try { j = await r.json(); } catch (e) { } return { status: r.status, j }; }, [was, d]);
  const ersteAnfrage = async () => { await gehe('eingang'); await p.locator('.re-liste .re-a', { hasText: /Beispiel/i }).first().click(); await sleep(700); await p.waitForSelector('#brief'); };
  const ueberlauf = async () => p.evaluate(() => document.documentElement.scrollWidth - innerWidth);

  // ---------- R: Rahmen in dieser Grösse
  await schritt('R01/R05 Aufbau und Kopf (Zeichen, Name, Titel, Prüfung, Anleitung, Die Stube)', async () => {
    await gehe('start'); await foto('start');
    for (const s of ['#kopf', '#rand', '#haupt', '#leiste', '#fenster', '#meldung']) ok(await p.locator(s).count() === 1, s + ' fehlt');
    const tips = await p.$$eval('#kopf .rund', a => a.map(x => x.getAttribute('data-tip')));
    ok(tips.includes('Prüfung') && tips.includes('Anleitung') && tips.includes('Die Stube'), 'runde Knöpfe: ' + tips.join(', '));
    ok(await p.getAttribute('#meldung', 'aria-live') === 'polite', '#meldung ohne aria-live');
    return 'Knöpfe ' + tips.join(', ') + ' · Titel «' + (await t('.titel h1')).slice(0, 40) + '»';
  });
  await schritt('R07 Kein seitliches Verrutschen in allen Ansichten', async () => {
    const aus = []; for (const a of ['start', 'eingang', 'gefragt', 'nachgetragen', 'wissen']) { await gehe(a); const o = await ueberlauf(); aus.push(a + ' ' + o); ok(o <= 0, a + ' ' + o + ' px zu breit'); await foto('ansicht-' + a); }
    await ersteAnfrage(); const o = await ueberlauf(); ok(o <= 0, 'Brief ' + o + ' px zu breit'); await foto('brief');
    return aus.join(', ') + ', brief ' + o;
  });
  await schritt('R07 Handy: «Bereiche» klappt auf und schliesst sich nach der Wahl', async () => {
    if (!HANDY) return 'nur Handy';
    await gehe('start'); await p.click('#rand .rand__auf'); await sleep(300); ok(await p.locator('#rand.auf').count() === 1, 'klappt nicht auf'); await foto('bereiche-offen');
    await p.click('#rand [data-gehe="gefragt"]'); await sleep(900); ok(await p.locator('#rand.auf').count() === 0, 'bleibt offen nach der Wahl'); return 'auf und zu';
  });
  await schritt('R11 Fehler als Quittung mit Stichwort und «Was tun?», höchstens drei, ×', async () => {
    await gehe('start');
    await p.evaluate(() => { for (let i = 0; i < 4; i++) fehler(new Error('PDF · Probefehler ' + i)); });
    await sleep(200); const n = await p.locator('#meldung .quit').count(); ok(n === 3, n + ' Quittungen statt höchstens 3');
    const q = await t('#meldung .quit:last-child'); ok(/Stichwort PDF/i.test(q) && /Was tun\?/i.test(q), 'Quittung: ' + q);
    const [neu] = await Promise.all([ctx.waitForEvent('page'), p.locator('#meldung .quit:last-child button', { hasText: 'Was tun?' }).click()]);
    await neu.waitForLoadState('load'); const u = neu.url(); await sleep(400); const ziel = await neu.evaluate(() => { const e = document.getElementById('PDF'); return e ? e.innerText.slice(0, 60) : ''; }); await neu.close();
    ok(/pruefung\.html#PDF$/.test(u) && ziel, 'führt nicht zum Lexikon: ' + u);
    const vorX = await p.locator('#meldung .quit').count(); await p.locator('#meldung .quit:last-child button[aria-label="Schliessen"]').click(); ok(await p.locator('#meldung .quit').count() === vorX - 1, '× schliesst nicht');
    return q.slice(0, 80) + ' → ' + ziel.replace(/\s+/g, ' ');
  });
  await schritt('R15 Letzte Ansicht gemerkt, aus La Maison immer Übersicht', async () => {
    await gehe('start'); await p.click('#rand [data-gehe="gefragt"]').catch(async () => { await p.click('#rand .rand__auf'); await p.click('#rand [data-gehe="gefragt"]'); }); await sleep(800); await p.goto(BASIS, { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *'); await sleep(600);
    ok(/gefragt/.test(p.url()) || /Gäste|wissen wollen/.test(await t('.titel h1')), 'nicht gemerkt: ' + p.url());
    await p.goto(ORIGIN + '/_werkzeuge/maison/', { waitUntil: 'domcontentloaded' }).catch(() => {});
    await p.evaluate(u => { const a = document.createElement('a'); a.href = u; document.body.appendChild(a); a.click(); }, BASIS); await p.waitForURL(/reception/); await p.waitForSelector('#ansicht > *'); await sleep(800);
    const tit = await t('.titel h1'); ok(/Guten|Wer hat geschrieben/.test(tit), 'aus La Maison nicht Übersicht: ' + tit); return 'gemerkt, aus La Maison: ' + tit.slice(0, 30);
  });
  await schritt('R18 Rundgang über ?rundgang: Kegel auf echtes Stück, Schritte, schliessen', async () => {
    await p.goto(BASIS + '?rundgang#start', { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *'); await p.waitForSelector('.rdg-karte', { timeout: 15000 }).catch(() => {}); await sleep(800);
    const da = await p.evaluate(() => [...document.querySelectorAll('div,section,aside')].filter(e => /rdg-/.test(e.className) && e.offsetWidth > 0).length);
    ok(da > 0, 'kein Rundgang sichtbar'); await foto('rundgang');
    const txt = await p.evaluate(() => document.body.innerText.match(/Das ist der Gastgeber[^\n]*/)?.[0] || ''); ok(txt, 'Text des ersten Schritts fehlt');
    await p.keyboard.press('Escape'); await sleep(500); return txt.slice(0, 60);
  });
  await schritt('R19 «Zur Werkbank» nur, wenn aus der Werkbank geöffnet', async () => {
    await gehe('start'); const ohne = await p.locator('#zur-werkbank').count();
    await p.goto(BASIS + '?wb=de.5#start', { waitUntil: 'load' }); await p.waitForSelector('#ansicht > *'); await sleep(1500);
    const mit = await p.evaluate(() => { const w = document.getElementById('zur-werkbank'); if (!w) return 0; const a = (w.shadowRoot || w).querySelector('a'); return a && /Zur Werkbank|Alles auf einen Blick/.test(a.textContent) && /werkbank\/index\.html#5$/.test(a.href) ? 1 : 0; });
    if (mit) await foto('zur-werkbank');
    ok(ohne === 0 && mit >= 1, `ohne ${ohne}, mit ${mit}`); return `ohne Werkbank ${ohne}, aus der Werkbank ${mit}`;
  });
  await schritt('R23 Prüfseite: Zustand, Lexikon, Fehlerliste, Reparatur mit zweitem Klick', async () => {
    await p.evaluate(() => fetch('api/fehler', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: 'QA Probefehler' }) }));
    await p.goto(BASIS + 'pruefung.html', { waitUntil: 'load' }); await p.waitForSelector('.z'); await sleep(500); await foto('pruefseite');
    const z = await p.locator('.z').count(), rot = await p.locator('.z.rot').count(), lex = await p.locator('.lex article').count();
    ok(z >= 10 && lex >= 20, `Zeilen ${z}, Lexikon ${lex}`); ok(/QA Probefehler/.test(await t('#fehler')), 'Fehler nicht gelistet');
    const b = p.locator('[data-rep="fehler"]'); await b.click(); ok(/Wirklich/.test(await b.innerText()), 'kein zweiter Klick verlangt'); await b.click(); await sleep(1200);
    ok(!/QA Probefehler/.test(await t('#fehler')), 'Fehlerliste nicht geleert'); return `${z} Punkte, ${rot} rot, ${lex} Stichworte, Fehlerliste geleert`;
  });

  // ---------- E: was gegenprobe.js nicht abdeckt
  await schritt('E12 Anfrage-Fenster der Website: Weg «formular» legt Anfrage in den Eingang, Feld «website» hält Maschinen ab', async () => {
    await gehe('start'); const vor = (await api('ueberblick')).j.anfragen_gesamt;
    const r1 = await api('formular', { name: 'Formular QA', kontakt: 'qa-formular@example.ch', art: 'spa', datum: 'Samstag, 24. Oktober 2026', personen: 2, anliegen: 'Zwei Plätze in der Sauna am Nachmittag.' });
    const r2 = await api('formular', { name: 'Robot', kontakt: 'x@y.z', website: 'http://spam', anliegen: 'spam' });
    const r3 = await api('formular', { name: 'Ohne Kontakt', kontakt: '' });
    const nach = (await api('ueberblick')).j.anfragen_gesamt;
    ok(r1.status === 200 && r2.status === 200 && nach === vor + 1, `vorher ${vor}, nachher ${nach}`); ok(r3.status === 422 && /FORMULAR/.test(r3.j.fehler), 'leerer Kontakt: ' + r3.status);
    await gehe('eingang'); const k = p.locator('.re-liste .re-a', { hasText: 'Formular QA' }); ok(await k.count() === 1, 'nicht im Eingang'); await k.click(); await p.waitForSelector('#brief', { timeout: 30000 }); await foto('formular-im-eingang');
    return `Eingang ${vor} → ${nach}, Art Spa, Brief geschrieben, Maschine abgewiesen, ohne Kontakt 422`;
  });
  await schritt('E13 Anfrage löschen, Frage löschen (Quittung «Gelöscht»)', async () => {
    await gehe('eingang'); const k0 = await p.locator('.re-liste .re-a').count();
    await p.locator('.re-liste .re-a', { hasText: 'Formular QA' }).click(); await sleep(600); await p.click('#detail [data-akt="weg"]'); await p.click('#fenster:not([hidden]) #f-los'); await sleep(900);
    const q = await t('#meldung'); const k1 = await p.locator('.re-liste .re-a').count(); ok(k1 === k0 - 1 && /Gelöscht/.test(q), `Karten ${k0} → ${k1}, Meldung ${q.slice(0, 40)}`);
    const f = (await api('fragen')).j; const id = (f.fragen || [])[0]?.id; const r = await api('weg', { id }); const f2 = (await api('fragen')).j;
    ok(r.status === 200 && (f2.fragen || []).length === (f.fragen || []).length - 1, 'Frage nicht gelöscht'); return `Anfrage weg, Frage weg (${(f.fragen || []).length} → ${(f2.fragen || []).length})`;
  });
  await schritt('E14 Neues von selbst: Uhr fragt «ueberblick» nach und zeichnet neue Anfrage ohne Neuladen', async () => {
    await p.clock?.install?.().catch(() => {});
    await gehe('start'); const n0 = await t('#rand [data-gehe="eingang"]');
    await api('formular', { name: 'Uhr QA', kontakt: 'uhr@example.ch', art: 'tisch', anliegen: 'Tisch für zwei' });
    if (p.clock && p.clock.runFor) { await p.clock.runFor(121000); } else { await p.evaluate(() => new Promise(r => setTimeout(r, 0))); }
    await sleep(1500); const n1 = await t('#rand [data-gehe="eingang"]');
    ok(n1 !== n0, `Rand unverändert «${n0}»`); return `Rand «${n0}» → «${n1}»`;
  });
  await schritt('C Nur Text: Wechsel zu einer anderen Anfrage verliert keine Eingabe', async () => {
    await ersteAnfrage(); const wer = await t('#detail .re-d__n h2'); await p.click('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-text');
    await p.fill('#e-betreff', 'QA Wechsel-Probe'); await p.locator('.re-liste .re-a').nth(1).click(); await sleep(900);
    await p.locator('.re-liste .re-a', { hasText: wer.split(' ').slice(-1)[0] }).first().click(); await sleep(900);
    const d = (await api('anfragen')).j.anfragen.find(a => a.name && wer.includes(a.name.split(' ').slice(-1)[0]));
    ok(d && d.entwurf && d.entwurf.betreff === 'QA Wechsel-Probe', 'Betreff verloren: ' + (d && d.entwurf && d.entwurf.betreff)); return 'Betreff gesichert beim Wechsel';
  });
  await schritt('R13 Verlassen mit ungesicherter Eingabe: Browser fragt nach', async () => {
    await ersteAnfrage(); await p.click('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-text'); await p.fill('#e-text', 'QA ungesichert ' + Date.now());
    let gefragt = false; const h = d => { if (d.type() === 'beforeunload') gefragt = true; d.dismiss().catch(() => {}); }; p.on('dialog', h);
    await p.goto('about:blank').catch(() => {}); await sleep(500); p.off('dialog', h);
    if (!gefragt) gefragt = await p.url() !== 'about:blank';
    await p.close({ runBeforeUnload: false }).catch(() => {}); await neueSeite();
    ok(gefragt, 'keine Nachfrage beim Verlassen'); return 'nachgefragt';
  });

  // ---------- Ungewöhnliche Eingaben
  const BOES = { leer: '', lang: 'Ä'.repeat(5000), skript: '<script>window.__qa=1</script><img src=x onerror="window.__qa=2">', emoji: 'Grüezi 🏔️🐕 «Höheweg» ÄÖÜ äöü ß é', umlaut: 'Schöne Grüsse aus Zürich, Genève und Tübingen' };
  await schritt('U Nachtrag mit leer, 5000 Zeichen, <script>, Emoji, Umlauten', async () => {
    await gehe('nachgetragen'); const aus = [];
    for (const [k, v] of Object.entries(BOES)) { const r = await api('nachtragen', { frage: 'QA ' + k + ' ' + v.slice(0, 40), antwort: v }); aus.push(k + ' ' + r.status); }
    await gehe('nachgetragen'); await foto('nachtrag-eingaben');
    const qa = await p.evaluate(() => window.__qa || 0); ok(qa === 0, 'Skript lief: ' + qa);
    const txt = await t('.re-nliste'); ok(txt.includes('🏔️') && txt.includes('Zürich'), 'Emoji/Umlaute fehlen');
    const r = await api('nachtragen', { frage: '', antwort: '' }); ok(r.status === 422 || r.status === 400, 'leer angenommen: ' + r.status);
    return aus.join(', ') + ' · Skript lief nicht, Emoji und Umlaute stehen';
  });
  await schritt('U Brief: 5000 Zeichen, <script>, Emoji im Text, PDF setzt sauber', async () => {
    await gehe('eingang'); await p.locator('.re-liste .re-a', { hasText: /Beispiel/i }).nth(3).click(); await sleep(700); await p.waitForSelector('#brief'); const id = await p.evaluate(() => S.wahl);   // eigene Karte: Emoji im Betreff stören sonst das Tippen der folgenden Schritte (Chromium-Eigenheit beim Ersetzen markierter Emoji)
    const r = await api('anfrage', { id, betreff: 'QA ' + BOES.emoji, entwurf_text: 'Sehr geehrte Damen und Herren\n\n' + BOES.skript + '\n\n' + 'Langer Absatz. '.repeat(330) + '\n\n' + BOES.emoji + '\n\nHerzliche Grüsse vom Höheweg' });
    ok(r.status === 200, 'nicht gesichert: ' + r.status); await gehe('eingang'); await p.locator('.re-liste .re-a[data-wahl="' + id + '"]').click(); await sleep(900); await p.waitForSelector('#brief');
    ok(await p.evaluate(() => window.__qa || 0) === 0, 'Skript lief im Brief'); await foto('brief-lang');
    const [d] = await Promise.all([p.waitForEvent('download', { timeout: 120000 }), p.evaluate(() => document.querySelector('#detail [data-akt="pdf"]').click())]);
    const ziel = path.join(BEL, `brief-lang-${MOTOR}.pdf`); await d.saveAs(ziel); const b = fs.readFileSync(ziel);
    const s = (b.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length; ok(b.slice(0, 4).toString() === '%PDF' && s >= 2, s + ' Seiten'); return `PDF ${s} Seiten, ${Math.round(b.length / 1024)} kB (${path.basename(ziel)})`;
  });
  await schritt('U Neues Wissen: Foto 30 MB, Foto 400 px, Datei ohne Bild', async () => {
    await gehe('wissen'); await p.waitForSelector('#w-datei-bild', { state: 'attached' });
    const gross = path.join(OUT, 'qa-30mb.jpg'), klein = path.join(OUT, 'qa-400.png'), falsch = path.join(OUT, 'qa-kein-bild.jpg');
    if (!fs.existsSync(gross)) { const c = await p.evaluate(() => { const k = document.createElement('canvas'); k.width = 6000; k.height = 4000; const g = k.getContext('2d'); const d = g.createImageData(6000, 4000); for (let i = 0; i < d.data.length; i++) d.data[i] = (Math.random() * 255) | 0; g.putImageData(d, 0, 0); return k.toDataURL('image/jpeg', 1).split(',')[1]; }); fs.writeFileSync(gross, Buffer.from(c, 'base64')); }
    const k4 = await p.evaluate(() => { const k = document.createElement('canvas'); k.width = 400; k.height = 300; const g = k.getContext('2d'); g.fillStyle = '#0b1f40'; g.fillRect(0, 0, 400, 300); g.fillStyle = '#fff'; g.font = '30px serif'; g.fillText('Aushang QA', 40, 150); return k.toDataURL('image/png').split(',')[1]; }); fs.writeFileSync(klein, Buffer.from(k4, 'base64'));
    fs.writeFileSync(falsch, 'Das ist kein Bild, nur Text mit .jpg');
    const mb = (fs.statSync(gross).size / 1e6).toFixed(1); const aus = [];
    for (const [name, f] of [['30 MB', gross], ['400 px', klein], ['kein Bild', falsch]]) {
      await p.setInputFiles('#w-datei-bild', f); await sleep(name === '30 MB' ? 6000 : 1500);
      const chips = await p.evaluate(() => [document.querySelector('#w-dateien')?.innerText.replace(/\s+/g, ' ').slice(0, 90) || ''].filter(Boolean));
      aus.push(name + ': ' + (chips.join(' | ') || '') + ' · Meldung ' + (await t('#meldung')).slice(0, 80));
    }
    await foto('wissen-dateien');
    await p.fill('#w-text', ''); await p.click('#w-los'); await sleep(3000); const m = await t('#meldung');
    ok(/qa-30mb/.test(aus[0]) && /qa-400/.test(aus[1]) && /nicht als Foto|DATEI/i.test(aus[2]), 'Dateien: ' + aus.join(' / '));   // Prüf-Chat 17.10.2026: vorher ohne Prüfung, immer grün
    return `Datei ${mb} MB · ` + aus.join(' · ') + ' · Senden: ' + m.slice(0, 120);
  });

  // ---------- Zwei Fenster, Netz weg
  await schritt('Z Zwei Fenster am selben Brief: nichts überschrieben, späterer Stand gilt', async () => {
    await ersteAnfrage(); const id = await p.evaluate(() => S.wahl);
    const p2 = await ctx.newPage(); await p2.goto(BASIS + '#eingang', { waitUntil: 'load' }); await p2.waitForSelector('.re-liste .re-a'); await p2.locator('.re-liste .re-a', { hasText: /Beispiel/i }).first().click(); await p2.waitForSelector('#brief');
    await p.click('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-betreff'); await p.fill('#e-betreff', 'QA Fenster eins'); await p.click('#detail [data-akt="sichern"]').catch(async () => { await p.click('#detail [data-akt="lesen"]'); }); await sleep(900);
    await p2.click('#detail [data-akt="bearbeiten"]'); await p2.waitForSelector('#e-betreff'); const sieht = await p2.inputValue('#e-betreff');
    await p2.fill('#e-text', (await p2.inputValue('#e-text')) + '\n\nQA Fenster zwei'); await p2.click('#detail [data-akt="sichern"]').catch(async () => { await p2.click('#detail [data-akt="lesen"]'); }); await sleep(900);
    const m2 = await p2.locator('#meldung').innerText().catch(() => ''); const bleibt = await p2.inputValue('#e-text').catch(() => '');
    const d = (await api('anfragen')).j.anfragen.find(a => a.id === id); await p2.close();
    ok(d.entwurf.betreff === 'QA Fenster eins' && !/QA Fenster zwei/.test(d.entwurf.text), 'überschrieben: Betreff «' + d.entwurf.betreff + '»');   // Prüf-Chat 17.10.2026: vorher ohne Prüfung, immer grün
    ok(/schneller|anderen Fenster/i.test(m2) && /QA Fenster zwei/.test(bleibt), 'kein Konflikt-Hinweis oder Eingabe weg: «' + m2.slice(0, 80) + '»');
    const beide = d.entwurf.betreff === 'QA Fenster eins' && /QA Fenster zwei/.test(d.entwurf.text);
    return (beide ? 'beide Änderungen erhalten' : `Fenster zwei sah «${sieht}», gespeichert: Betreff «${d.entwurf.betreff}», Text mit zwei: ${/QA Fenster zwei/.test(d.entwurf.text)}`) + ' · Konflikt gemeldet («' + m2.replace(/\s+/g, ' ').slice(0, 50) + '»), Eingabe bleibt';
  });
  await schritt('N Netz weg beim Speichern: Meldung, Eingabe bleibt', async () => {
    await ersteAnfrage(); await p.click('#detail [data-akt="bearbeiten"]'); await p.waitForSelector('#e-betreff'); await p.fill('#e-betreff', 'QA offline');
    await ctx.setOffline(true); await p.click('#detail [data-akt="sichern"]'); await sleep(1500); const m = await t('#meldung'); const bleibt = await p.inputValue('#e-betreff').catch(() => '');
    await ctx.setOffline(false); await foto('offline');
    ok(/Keine Verbindung/i.test(m) && bleibt === 'QA offline', `Meldung «${m.slice(0, 80)}», Feld «${bleibt}»`);
    await p.click('#detail [data-akt="sichern"]'); await sleep(1200); return 'Meldung «' + m.slice(0, 60) + '», Eingabe blieb, danach gesichert';
  });

  fs.writeFileSync(path.join(OUT, `abnahme-${MOTOR}-${W}x${H}.json`), JSON.stringify({ motor: MOTOR, breite: W, hoehe: H, zeit: new Date().toISOString(), fehlerSeite, schritte: res }, null, 1));
  const gr = res.filter(r => r.stand === 'grün').length, ro = res.filter(r => r.stand === 'rot');
  console.log(`abnahme ${MOTOR} ${W}x${H}: ${gr} grün, ${ro.length} rot von ${res.length}`);
  ro.forEach(r => console.log('  ROT', r.name, '·', r.info));
  await br.close();
})().catch(e => { console.log('ABBRUCH', e); process.exit(2); });
