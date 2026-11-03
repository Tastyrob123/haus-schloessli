// Das Hausbuch · Wirtschaft am Schlössli · Funktionsliste Zeile für Zeile bedient (FUNKTIONEN.md, Zeilen 1–70 und 84), Vorlage Doldenhorn und Carlton _werkzeuge/livre/pruefung/funktionen.js.
//   BASIS=http://localhost:9049/ node _werkzeuge/livre/pruefung/funktionen.js chromium|webkit|firefox 1440x900|1366x650|390x844|320x700
// Gegen eine Probe-Kopie mit eigenem Server (Markenprüfung ohne Claude, Probe-Antwort). Jede Zeile meldet ✓ oder ✗ mit Messwert; Belegbilder in belege/<motor>-<grösse>/.
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Aussen-Pruefung/node_modules/playwright'));
const BASIS = process.env.BASIS || 'http://localhost:9049/', URL0 = BASIS + '_werkzeuge/livre/';
const motor = process.argv[2] || 'chromium', [breite, hoehe0] = (process.argv[3] || '1440x900').split('x').map(Number), hoehe = hoehe0 || (breite > 600 ? 900 : 844);
const BELEG = path.join(__dirname, 'belege', `${motor}-${breite}x${hoehe}`); fs.mkdirSync(BELEG, { recursive: true }); fs.mkdirSync(path.join(__dirname, 'ergebnisse'), { recursive: true });
const PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAAFUlEQVR4nGPklndgwA2Y8MgxjFxpAIylAH608qaWAAAAAElFTkSuQmCC';
const handy = breite < 600;

(async () => {
  const erg = [], fehler = [];
  const Z = (nr, text, ok, mass) => erg.push({ nr, text, ok: !!ok, mass: mass == null ? '' : String(mass) });
  const b = await pw[motor].launch();
  const ctx = await b.newContext({ viewport: { width: breite, height: hoehe }, hasTouch: handy && motor !== 'firefox', acceptDownloads: true, permissions: motor === 'chromium' ? ['clipboard-read', 'clipboard-write'] : [] });
  const p = await ctx.newPage();
  p.on('pageerror', e => fehler.push('JS ' + e.message)); p.on('console', m => { if (m.type() === 'error' && !/favicon|NS_BINDING|cancelled/i.test(m.text())) fehler.push('Konsole ' + m.text()); });
  p.on('response', r => { if (r.status() >= 400 && !/favicon|api\/pruefen/.test(r.url())) fehler.push(r.status() + ' ' + r.url().replace(BASIS, '/')); });
  const warte = ms => p.waitForTimeout(ms);
  const n = async s => p.locator(s).count();
  const text = async s => (await p.locator(s).first().innerText().catch(() => '')).replace(/\s+/g, ' ').trim();
  const status = async u => p.evaluate(async u => { try { const r = await fetch(u, { cache: 'no-store' }); const bl = await r.blob(); return [r.status, bl.size, r.headers.get('content-type') || '', r.headers.get('content-disposition') || '']; } catch (e) { return [0, 0, '', '']; } }, u);
  const foto = async name => p.screenshot({ path: path.join(BELEG, name + '.jpg'), type: 'jpeg', quality: 72 }).catch(() => {});
  const ansicht = async a => { await p.evaluate(a => { location.hash = '#' + a; }, a); await warte(1000); };
  const klickKachel = async loc => { await loc.evaluate(e => e.scrollIntoView({ block: 'center' })); await warte(250); await loc.click(); };
  const randKlick = async sel => { if (handy && !(await n('#rand.auf'))) { await p.locator('.rand__auf').click(); await warte(400); } await p.locator(sel).click(); };
  const ohneSchild = async () => p.evaluate(() => { try { localStorage.setItem('rundgang-sl-livre', '1'); } catch (e) {} });

  // ---- Übersicht (1–7)
  await p.goto(URL0 + '#start', { waitUntil: 'load' }); await ohneSchild(); await p.waitForSelector('#ansicht .li-k', { timeout: 30000 }); await warte(2600);
  await foto('01-uebersicht');
  Z(1, 'Übersicht lädt, Gruss nach Tageszeit im Titel', /Guten (Morgen|Tag|Abend)\./.test(await text('#ansicht h1')), await text('#ansicht h1'));
  Z(2, 'Drei Karten Bildarchiv, Dateien, Prüfung', (await n('#ansicht .li-k')) === 3, await n('#ansicht .li-k'));
  Z(3, 'Vier Zahlen unter den Karten', (await n('#ansicht .li-zahlen > div')) === 4, (await text('#ansicht .li-zahlen')).slice(0, 60));
  Z(4, 'Karte Markenbuch mit Knopf «Lesen»', (await n('#ansicht a.li-buch')) === 1 && /lesen/i.test(await text('#ansicht a.li-buch .kn')));
  Z(5, 'Rand: Arbeiten, Nachschlagen, Zahlen je Eintrag', (await n('#rand .nw')) === 5 && (await n('#rand .nw em')) >= 3 && (await n('#rand .nav > p')) === 2, await n('#rand .nw'));
  Z(6, 'Kopf: Zeichen und Name, Titel und Stand, Anleitung, Die Stube, Website', (await n('#kopf .kopf__marke')) && (await n('#kopf .kopf__stand')) && (await n('#kopf a.rund')) === 2 && (await n('#kopf a.kn')) === 1);
  Z(7, 'Leiste unten: Bildrechte und ZIP', /Bildrechte/.test(await text('#leiste')) && (await n('#leiste a[download]')) === 1);

  // ---- Sprache, vorgebaut (8–13)
  const ohneWahl = await n('#kopf .li-sp');
  await p.goto(URL0 + '?sprachen=probe#start', { waitUntil: 'load' }); await p.waitForSelector('#ansicht .li-k'); await warte(1200);
  await p.locator('.li-sp__k').click(); await warte(400);
  Z(8, 'Sprachwahl vorgebaut: mit einer Sprache verborgen, mit ?sprachen=probe sichtbar und offen', ohneWahl === 0 && (await n('.li-sp.offen [data-sp]')) === 2, `ohne ${ohneWahl}, mit ${await n('.li-sp.offen [data-sp]')}`);
  const vorher = await text('#ansicht h1');
  await p.locator('[data-sp="pr"]').click(); await warte(900);
  Z(9, 'Sprache wechselt Titel, Rand, Leiste (Probe-Sprache)', /‹/.test(await text('#ansicht h1')) && /‹/.test(await text('#leiste')) && (handy || /‹Bildarchiv›/.test(await text('#rand'))), (await text('#ansicht h1')).slice(0, 30));
  await p.reload({ waitUntil: 'load' }); await p.waitForSelector('#ansicht .li-k'); await warte(1200);
  Z(10, 'Gewählte Sprache bleibt nach Neuladen', /‹/.test(await text('#leiste')));
  await p.goto(URL0 + '?sprache=xx#start', { waitUntil: 'load' }); await p.waitForSelector('#ansicht .li-k'); await warte(900);
  Z(11, 'Unbekannte Sprache in der Adresse fällt auf Deutsch zurück', !/‹/.test(await text('#leiste')) && /Bildrechte/.test(await text('#leiste')));
  await p.goto(URL0 + '?sprachen=probe#start', { waitUntil: 'load' }); await p.waitForSelector('#ansicht .li-k'); await warte(900);
  await p.locator('.li-sp__k').click(); await p.locator('[data-sp="de"]').click(); await warte(700);
  Z(12, 'Zurück auf Deutsch', /Bildrechte/.test(await text('#leiste')) && (await text('#ansicht h1')) === vorher);
  await p.locator('.li-sp__k').click(); await warte(300); await p.mouse.click(breite - 30, hoehe - 200); await warte(300);
  Z(13, 'Sprachwahl schliesst beim Klicken daneben', (await n('.li-sp.offen')) === 0);
  await p.goto(URL0 + '#start', { waitUntil: 'load' }); await p.waitForSelector('#ansicht .li-k'); await warte(900);

  // ---- Links, ZIP (14–15)
  const links = await p.evaluate(() => [...document.querySelectorAll('#kopf a[href], #rand a[href], #leiste a[href]')].map(a => a.getAttribute('href')));
  const tot = [];
  for (const l of new Set(links)) { const u = new URL(l, p.url()).href; const s = await status(u); if (s[0] !== 200) tot.push(l + ' ' + s[0]); }
  Z(14, 'Alle Links in Kopf, Rand und Leiste antworten', tot.length === 0, tot.join(' | ') || new Set(links).size + ' Links');
  const zip = await status(new URL(await p.locator('#leiste a[download]').getAttribute('href'), p.url()).href);
  Z(15, 'ZIP mit allen Dateien lädt', zip[0] === 200 && zip[1] > 500000 && /zip/.test(zip[2]), Math.round(zip[1] / 1024) + ' KB');

  // ---- Ansichten (16–21)
  let nr = 16;
  for (const [a, sel, nm] of [['bilder', '#li-raster', 'Bildarchiv'], ['dateien', '.li-d', 'Logo & Dateien'], ['pruefung', '#li-pr', 'Markenprüfung']]) {
    await randKlick(`#rand [data-gehe="${a}"]`); await warte(1200);
    Z(nr++, 'Rand → ' + nm, (await n(sel)) >= 1 && (await p.locator(`#rand [data-gehe="${a}"]`).getAttribute('aria-current')) === 'true' && p.url().endsWith('#' + a));
  }
  await p.locator('#kopf [data-gehe="start"]').click(); await warte(900);
  Z(19, 'Marke im Kopf führt zur Übersicht', (await n('#ansicht .li-k')) === 3);
  await klickKachel(p.locator('#ansicht .li-k[data-gehe="dateien"]')); await warte(900);
  Z(20, 'Karte «Logo & Dateien» öffnet die Ansicht', (await n('.li-d')) === 7, await n('.li-d'));
  await p.goto('about:blank'); await p.goto(URL0 + '#bilder', { waitUntil: 'load' }); await p.waitForSelector('#li-raster .li-f', { timeout: 30000 }); await warte(1200);
  Z(21, 'Adresse mit #bilder öffnet gleich das Bildarchiv', (await n('#li-raster .li-f')) > 0);

  // ---- Bildarchiv (22–31)
  const LJ = await p.evaluate(async u => (await fetch(u)).json(), URL0 + 'livre.json');
  const gesamt = LJ.fotos.length; const FOTOS = Object.fromEntries(LJ.fotos.map(f => [f.k, f]));
  const erste = await n('#li-raster .li-f');
  await foto('02-bildarchiv');
  Z(22, 'Raster zeigt zuerst 48 Kacheln', erste === Math.min(48, gesamt), erste + ' von ' + gesamt);
  for (let i = 0; i < 4; i++) { await p.evaluate(() => scrollTo(0, document.body.scrollHeight)); await warte(1200); }
  Z(23, 'Nachladen beim Scrollen hängt Kacheln an, bis alle da sind', (await n('#li-raster .li-f')) === gesamt, await n('#li-raster .li-f'));
  await p.evaluate(() => scrollTo(0, 0));
  await p.locator('#li-q').fill('terrasse'); await warte(700);
  const nSuche = await n('#li-raster .li-f');
  Z(24, 'Suche «terrasse» filtert', nSuche > 0 && nSuche < gesamt, nSuche);
  Z(25, 'Zähler «x von y» stimmt zur Suche', (await text('#li-n')).replace(/[’']/g, '').toLowerCase().startsWith(nSuche + ' von ' + gesamt), await text('#li-n'));
  await p.locator('#li-q').fill('qqqqqq'); await warte(700);
  Z(26, 'Leere Suche zeigt Hinweis statt Kacheln', (await n('#li-raster .li-leer')) === 1 && (await n('#li-raster .li-f')) === 0);
  await p.locator('#li-reset').click(); await warte(900);
  Z(27, '«Filter zurücksetzen» zeigt wieder alle', (await text('#li-n')).toLowerCase().includes(String(gesamt) + ' von') && (await p.locator('#li-q').inputValue()) === '');
  const soll = { b: 8, s: 3, f: 2, h: 2 }; nr = 28;
  for (const g of ['b', 's', 'f', 'h']) {
    const knoepfe = p.locator(`[data-f="${g}"]:not([data-w="alle"])`); const k = await knoepfe.count();
    let ok = k === soll[g], m = [];
    for (let i = 0; i < k; i++) {
      await knoepfe.nth(i).click(); await warte(350);
      const c = await n('#li-raster .li-f, #li-raster .li-leer'); m.push(await n('#li-raster .li-f'));
      const w = await knoepfe.nth(i).getAttribute('data-w');
      const keys = await p.locator('#li-raster .li-f').evaluateAll(a => a.map(x => x.dataset.k));
      const feld = { b: 'b', s: 's', f: 'f', h: 'art' }[g];
      const passt = keys.every(k => { const f = FOTOS[k]; return f && (f[feld] === w || (g === 'f' && w === 'quer' && f.f === 'quadrat')); });
      if ((await knoepfe.nth(i).getAttribute('aria-pressed')) !== 'true' || !c || !passt) ok = false;
    }
    await p.locator(`[data-f="${g}"][data-w="alle"]`).click(); await warte(400);
    Z(nr++, 'Filter ' + { b: 'Bereich', s: 'Saison', f: 'Format', h: 'Herkunft' }[g] + ': ' + k + ' Knöpfe, Wahl wirkt, «Alle» löst', ok && (await n('#li-raster .li-f')) === erste && m.some(x => x > 0 && x < gesamt), m.join('/'));
  }

  // ---- Detail (32–46)
  const KK = 'platanen', kachel = p.locator(`#li-raster .li-f[data-k="${KK}"]`);
  await klickKachel(kachel); await p.waitForSelector('#fenster:not([hidden]) .li-det', { timeout: 8000 }); await warte(900);
  await foto('03-foto-gross');
  Z(32, 'Foto öffnet gross im Fenster mit Titel, Quelle, Original', (await n('#fenster h2')) && (await n('#fenster .li-meta dt')) === 2, await text('#fenster h2'));
  Z(33, 'Vier Grössen Instagram, Story, Website, Druck', (await n('#fenster .li-gr')) === 4);
  Z(34, 'Hinweis zum Beschneiden: «Ausschnitt: Feld ziehen»', /Ausschnitt/.test(await text('#fenster .li-det__hilfe')));
  const gr = p.locator('#fenster .li-gr');
  const fahr = async i => { if (handy) await gr.nth(i).dispatchEvent('mouseenter'); else await gr.nth(i).hover(); await warte(450); return p.locator('#li-rahmen').getAttribute('data-g'); };
  const sch = [await fahr(1), await fahr(2), await fahr(3)];
  Z(35, 'Über jede Grösse fahren zeigt den Rahmen mit Mass', /1920/.test(sch[0]) && sch[0] !== sch[1] && sch[1] !== sch[2], sch.join(' | '));
  await fahr(0);
  await p.locator('#li-rahmen').evaluate(e => e.scrollIntoView({ block: 'center' })); await warte(200);
  const rb = await p.locator('#li-rahmen').boundingBox();
  const href0 = await p.locator('[data-laden="instagram"]').getAttribute('href');
  await p.mouse.move(rb.x + rb.width / 2, rb.y + rb.height / 2); await p.mouse.down(); await p.mouse.move(rb.x + rb.width / 2 + 60, rb.y + rb.height / 2 + 30, { steps: 6 }); await p.mouse.up(); await warte(400);
  const href1 = await p.locator('[data-laden="instagram"]').getAttribute('href'), imp1 = await p.locator('[data-imp="instagram"]').getAttribute('href');
  Z(36, 'Rahmen ziehen ändert den Ausschnitt im Download- und Imprimerie-Link', href0 !== href1 && /x=0\.[0-9]{3}/.test(imp1) && !/x=0\.500/.test(imp1), (href1 || '').replace(/^.*[?]/, ''));
  const dl = {};
  for (const g of ['instagram', 'story', 'web', 'druck']) dl[g] = await status(new URL(await p.locator(`[data-laden="${g}"]`).getAttribute('href'), p.url()).href);
  Z(37, 'Download Instagram 1080 × 1350 (Server)', dl.instagram[0] === 200 && /jpeg/.test(dl.instagram[2]) && /1080x1350/.test(dl.instagram[3]), dl.instagram[3].slice(-44));
  Z(38, 'Download Story 1080 × 1920 (Server)', dl.story[0] === 200 && /1080x1920/.test(dl.story[3]), dl.story[3].slice(-44));
  Z(39, 'Download Website 2000 px (Server)', dl.web[0] === 200 && /-web-2000x/.test(dl.web[3]), dl.web[3].slice(-44));
  Z(40, 'Download Druck volle Auflösung (Server)', dl.druck[0] === 200 && new RegExp(`-druck-${FOTOS[KK].w}x${FOTOS[KK].h}`).test(dl.druck[3]) && !/websitegroesse/.test(dl.druck[3]), dl.druck[3].slice(-44) + ' ' + Math.round(dl.druck[1] / 1024) + ' KB');
  const [dlg] = await Promise.all([p.waitForEvent('download', { timeout: 20000 }), p.locator('[data-laden="web"]').click()]);
  Z(41, 'Klick auf «Laden» speichert eine JPG-Datei', /^wirtschaft-am-schloessli-platanen-web-.*\.jpg$/.test(dlg.suggestedFilename()), dlg.suggestedFilename());
  const imps = await p.locator('#fenster [data-imp]').evaluateAll(a => a.map(x => x.href));
  Z(42, 'Zwei Wege in Die Werkstatt (Beitrag, Story) mit Foto und Ausschnitt', imps.length === 2 && imps.every(u => /\/_werkzeuge\/imprimerie\/\?/.test(u) && /foto=platanen/.test(u) && /haus=schloessli/.test(u) && /art=(insta|story)/.test(u) && /x=/.test(u)), imps.map(u => u.replace(/^.*[?]/, '')).join(' | ').slice(0, 100));
  await p.keyboard.press('Escape'); await warte(300);
  Z(43, 'Esc schliesst das Fenster', (await n('#fenster[hidden]')) === 1);
  await klickKachel(kachel); await warte(600); await p.locator('#fenster [data-zu]').click(); await warte(300);
  Z(44, 'Kreuz schliesst das Fenster', (await n('#fenster[hidden]')) === 1);
  await klickKachel(kachel); await warte(600); await p.mouse.click(3, 3); await warte(300);
  Z(45, 'Klick neben das Fenster schliesst es', (await n('#fenster[hidden]')) === 1);
  await p.locator('[data-f="h"][data-w="frei"]').click(); await warte(500);
  await klickKachel(p.locator('#li-raster .li-f').first()); await warte(900);
  const tFrei = await text('#fenster .li-det__t'); const qLink = await p.locator('#fenster .li-meta a.link').getAttribute('href').catch(() => '');
  Z(46, 'Frei lizenziertes Foto: Hinweis «Namen und Lizenz», Quelle mit Urheber und Weg zur Quelle (Wikimedia Commons)', /Frei lizenziert/.test(tFrei) && /commons\.wikimedia\.org/.test(qLink || '') && (await n('#fenster .li-hinweis')) === 1, (qLink || '').slice(0, 70));
  await p.keyboard.press('Escape'); await warte(200); await p.locator('[data-f="h"][data-w="alle"]').click(); await warte(300);

  // ---- Dateien (47–53)
  await ansicht('dateien'); await p.waitForSelector('.li-d'); await warte(1500);
  await foto('04-dateien');
  Z(47, 'Dateien: Zeichen, Logo, Name, Tapete, Farben, Schriften, Logo der heutigen Website', (await p.locator('.li-d').evaluateAll(a => a.map(x => x.id).join(','))) === 'd-zeichen,d-logo,d-name,d-tapete,d-farben,d-schriften,d-website', await n('.li-d'));
  const dls = await p.locator('#ansicht a[download], #leiste a[download]').evaluateAll(a => [...new Set(a.map(x => x.href))]);
  const schlecht = []; for (const u of dls) { const s = await status(u); if (s[0] !== 200 || s[1] < 200) schlecht.push(s[0] + ' ' + u.replace(/^https?:\/\/[^/]+/, '')); }
  Z(48, 'Jede Datei der Ansicht ist abrufbar', schlecht.length === 0 && dls.length >= 30, schlecht.join(' | ') || dls.length + ' Dateien');
  const farbe = p.locator('.li-farbe').first(); const wert = await farbe.getAttribute('data-kopie');
  await farbe.evaluate(e => e.scrollIntoView({ block: 'center' })); await farbe.locator('.li-farbe__w span').first().click(); await warte(500);
  const zw = motor === 'chromium' ? await p.evaluate(() => navigator.clipboard.readText().catch(() => '')) : wert;
  Z(49, 'Farbe antippen kopiert den Hexwert, Meldung erscheint', zw === wert && /kopiert/i.test(await text('#meldung')), wert + ' ' + zw);
  Z(50, 'Farben: neun Töne und das Rot der Geranien wie in der Handschrift der Werkbank, dazu fünf weitere der Website', (await n('.li-fg')) === 5 && (await n('.li-farbe')) === 15 && /Nur als Punkt/i.test(await text('.li-fg:nth-of-type(4) h3')) && (await n('.li-fg--druck')) === 0, (await n('.li-farbe')) + ' Farben');
  await farbe.locator('.li-farbe__w span').nth(1).click(); await warte(400);
  const zr = motor === 'chromium' ? await p.evaluate(() => navigator.clipboard.readText().catch(() => '')) : 'rgb(';
  Z(51, 'Zweite Zeile einer Farbe kopiert den RGB-Wert', /^rgb\(\d+, \d+, \d+\)$/.test(zr) || (motor !== 'chromium' && /rgb/i.test(await text('#meldung'))), zr);
  Z(52, 'Schriften mit WOFF2-Knopf', (await n('.li-schrift a[download]')) === 5, await n('.li-schrift a[download]'));
  const regeln = await p.locator('#ansicht .titel__kn a.kn--linie').getAttribute('href');
  Z(53, 'Knopf «Regeln im Markenbuch» führt ins Markenbuch', /^buch\.html#zeichen$/.test(regeln) && (await status(new URL(regeln, p.url()).href))[0] === 200, regeln);

  // ---- Markenprüfung (54–68)
  await ansicht('pruefung'); await p.waitForSelector('#li-pr'); await warte(1800);
  Z(54, 'Prüfung: Feld mit «Datei wählen», Beispiel-Link, Hinweis «nichts gespeichert»', (await n('#li-waehle')) && (await n('#li-bsp')) && /Nichts wird gespeichert/.test(await text('.li-privat')));
  Z(55, 'Unter dem leeren Feld steht schon ein Beispiel', (await n('#li-bsp-erg .li-erg')) === 1 && (await n('#li-bsp-erg .li-hinweis--bsp')) === 1);
  await p.locator('#li-datei').setInputFiles({ name: 'falsch.txt', mimeType: 'text/plain', buffer: Buffer.from('x') }); await warte(500);
  Z(56, 'Falscher Dateityp wird abgewiesen, Meldung erscheint', (await n('#li-los')) === 0 && /kein Bild/i.test(await text('#meldung')));
  await p.locator('#li-datei').setInputFiles({ name: 'entwurf.png', mimeType: 'image/png', buffer: Buffer.from(PNG, 'base64') }); await warte(700);
  Z(57, 'Gewählte Datei: Vorschau, Name, Grösse, «Prüfen»', (await n('.li-feld__vor img')) === 1 && (await n('#li-los')) === 1 && (await text('.li-feld__name')).includes('entwurf.png'));
  Z(58, 'Nach der Wahl verschwindet das Beispiel darunter', (await n('#li-bsp-erg .li-erg')) === 0);
  await p.locator('#li-los').click(); await warte(120);
  Z(59, 'Prüfen zeigt drei Schritte mit Abtastung', (await n('.li-schritte li')) === 3 && (await n('.li-scan')) === 1);
  await p.waitForFunction(() => { const e = document.querySelector('#li-pr'); return e && !e.querySelector('.li-lauf'); }, null, { timeout: 60000 }); await warte(1500);
  await foto('05-pruefung-ergebnis');
  const hatErg = await n('#li-pr .li-erg');
  Z(60, 'Prüfung endet mit Ergebnis (Messung) oder mit Meldung und Feld', hatErg === 1 || (await n('#li-pr #li-feld')) === 1, hatErg ? 'Ergebnis' : (await text('#meldung')).slice(0, 80));
  Z(61, 'Ergebnis: Vorschau, gemessene Farben, Prozent im Rahmen', (await n('#li-pr .li-erg__bild img')) === 1 && (await n('#li-pr .li-ton')) >= 1 && (await n('#li-pr .li-rahmen-z')) === 1, (await n('#li-pr .li-ton')) + ' Töne');
  Z(62, 'Ergebnis: Probe-Antwort deutlich beschriftet, wenn Claude aus ist, sonst Punkte', (await n('#li-pr .li-hinweis--probe')) === 1 && /Probe-Antwort ohne Claude/.test(await text('#li-pr .li-hinweis--probe')) && (await n('#li-pr .li-pk')) >= 4, (await n('#li-pr .li-pk')) + ' Punkte');
  await p.locator('#li-pr [data-kopie-erg]').click(); await warte(400);
  Z(63, '«Als Text kopieren» legt die Rückmeldung in die Zwischenablage', motor !== 'chromium' ? /kopiert/i.test(await text('#meldung')) : /^Das Hausbuch · Markenprüfung · entwurf\.png/.test(await p.evaluate(() => navigator.clipboard.readText().catch(() => ''))));
  const [d2] = await Promise.all([p.waitForEvent('download', { timeout: 15000 }), p.locator('#li-pr [data-sichern]').click()]);
  Z(64, '«Ergebnis sichern» speichert eine HTML-Datei auf dem Rechner', d2.suggestedFilename() === 'hausbuch-pruefung-entwurf.html', d2.suggestedFilename());
  await p.locator('#li-pr [data-neu]').click(); await warte(900);
  Z(65, '«Neuen Entwurf prüfen» setzt das Feld zurück', (await n('#li-waehle')) === 1 && (await n('.li-feld__vor')) === 0 && (await n('#li-bsp-erg .li-erg')) === 1);
  await p.locator('#li-bsp').click(); await warte(1500);
  Z(66, '«Beispiel ansehen» zeigt die unveränderte Antwort der Prüfung zum Beispiel-Entwurf, als Beispiel beschriftet', (await n('.li-erg')) >= 1 && /unverändert die der Prüfung/.test(await text('.li-hinweis--bsp')), (await n('.li-pk')) + ' Punkte');
  Z(67, 'Beispiel: Punkte sortiert, «passt nicht» zuerst', await p.evaluate(() => { const l = [...document.querySelectorAll('.li-erg')].pop(); const k = [...l.querySelectorAll('.li-pk')].map(x => x.className.match(/li-pk--(\w+)/)[1]); const r = { passt_nicht: 0, achten: 1, passt: 2 }; return k.length > 3 && k.every((x, i) => i === 0 || r[k[i - 1]] <= r[x]); }));
  await p.goto(URL0 + '?beispiel=1#pruefung', { waitUntil: 'load' }); await warte(2500);
  Z(68, 'Adresse mit ?beispiel=1#pruefung öffnet das Beispiel gleich', (await n('#li-pr .li-erg')) === 1 && (await n('#li-pr .li-hinweis--bsp')) === 1);

  // ---- Breite, Handy, Fehler (69, 84, 70)
  let ue = 0;
  for (const a of ['start', 'bilder', 'dateien', 'pruefung']) { await ansicht(a); await warte(500); ue = Math.max(ue, await p.evaluate(() => document.documentElement.scrollWidth - innerWidth)); }
  Z(69, 'Kein seitliches Verrutschen (' + breite + ' px, vier Ansichten)', ue <= 1, ue + ' px');
  if (handy) {
    await p.goto(URL0 + '#bilder', { waitUntil: 'load' }); await warte(1500);
    await p.locator('.rand__auf').click(); await warte(500);
    await foto('06-handy-menue');
    const auf = (await n('#rand.auf .nw')) >= 4;
    await p.locator('#rand [data-gehe="dateien"]').click(); await warte(900);
    const zu = (await n('.li-d')) === 7 && (await n('#rand.auf')) === 0;
    await p.goto(URL0 + '#bilder', { waitUntil: 'load' }); await p.waitForSelector('#li-raster .li-f'); await warte(900);
    await klickKachel(p.locator('#li-raster .li-f').first()); await warte(1000);
    const fb = await p.locator('#fenster .fenster__k').boundingBox();
    Z(84, 'Handy: Menü «Bereiche» öffnet, Wahl wechselt und schliesst, Foto-Fenster passt', auf && zu && fb && fb.x >= -1 && fb.x + fb.width <= breite + 1, `${auf}/${zu}/${fb && Math.round(fb.width)}`);
  }
  Z(70, 'Keine Fehler in der Konsole, keine toten Anfragen', fehler.length === 0, fehler.slice(0, 3).join(' | ').slice(0, 200));
  await b.close();
  erg.sort((a, b) => a.nr - b.nr);
  console.log(`Das Hausbuch · Schlössli · ${motor} ${breite} × ${hoehe}`);
  for (const r of erg) console.log(`${String(r.nr).padStart(2)} ${r.ok ? '✓' : '✗'} ${r.text}${r.mass ? '  · ' + r.mass : ''}`);
  const gut = erg.filter(r => r.ok).length;
  console.log(`\nSumme: ${gut}/${erg.length}`);
  fs.writeFileSync(path.join(__dirname, 'ergebnisse', `funktionen-${motor}-${breite}x${hoehe}.json`), JSON.stringify(erg, null, 1));
  process.exit(gut === erg.length ? 0 : 1);
})().catch(e => { console.log('ABBRUCH', String(e && e.stack || e).slice(0, 600)); process.exit(2); });
