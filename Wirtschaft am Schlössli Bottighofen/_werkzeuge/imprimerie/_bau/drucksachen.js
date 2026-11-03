/* Die Hausdruckerei · Wirtschaft am Schlössli: die fertigen Drucksachen des Hauses als PDF (3 mm Beschnitt, Schriften eingebettet) und Vorschaubild,
   gesetzt mit dem Werkzeug selbst (DS.dokument, DS.pdf, DS.png) aus dem Katalog des Hauses (katalog.js) und der Bibliothek (vorlagen/<art>.json).
   Dazu Druckprüfung und Stilprüfung je Stück. Aufruf (Server :9287 läuft):
   NODE_PATH=/opt/node-tools/node_modules node _bau/drucksachen.js   → haeuser/schloessli/drucksachen/ + LISTE.md + liste.json */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ZIEL = path.join(__dirname, '..', 'haeuser', 'schloessli', 'drucksachen');
/* [Datei, Quelle (Abteilung, «hinweise», «newsletter», «motive:<anlass>» oder «bib:<art>»), Name im Katalog, was es ist] */
const STUECKE = [
  ['aushang-betriebsferien', 'hinweise', 'Betriebsferien im Winter', 'Aushang A4: Betriebsferien 22. Dezember 2026 bis 10. Februar 2027'],
  ['aushang-kreuzfahrt-geschlossen', 'hinweise', 'Geschlossen wegen Kreuzfahrt', 'Aushang A4: geschlossen 13. bis 15. November, das Team ist an Bord'],
  ['aushang-oeffnungszeiten', 'haus', 'Öffnungszeiten', 'Aushang A4: Donnerstag bis Montag, Küche, Ruhetag'],
  ['aushang-ruhetag', 'hinweise', 'Ruhetag', 'Aushang A5 an der Tür: Dienstag & Mittwoch Ruhetag'],
  ['aushang-besen', 'haus', 'Statt eines Schilds ein Besen', 'Aushang A4 zur Geschichte des Hauses'],
  ['plakat-terrasse', 'hafen', 'Die schönste Terrasse', 'Plakat A3 mit der Terrasse am Mittag'],
  ['einladung-gourmetkreuzfahrt', 'anlaesse', 'Excellence Gourmetkreuzfahrt', 'Einladung quadratisch 148 mm: Four-Hands an Bord'],
  ['programm-die-reise', 'anlaesse', 'Die Reise', 'Programm A5: Basel, Strassburg, zurück'],
  ['flyer-banketts', 'anlaesse', 'Banketts & Gruppen', 'Angebot A5: zwei Etagen, bis zu 26 Personen'],
  ['menuekarte-lunch', 'restaurant', 'Lunch-Menü', 'Menükarte DL hoch: drei Gänge am Mittag'],
  ['menuekarte-bankett-herbst', 'anlaesse', 'Bankettmenü Herbst', 'Bankettmenü A5: fünf Gerichte des Herbsts'],
  ['menuekarte-bankett-sommer', 'anlaesse', 'Bankettmenü Sommer', 'Bankettmenü A5: fünf Gerichte des Sommers'],
  ['einleger-italien', 'restaurant', 'Aus Italien', 'Menü-Einleger A5: Gerichte aus Italien, ohne Preise'],
  ['einleger-klassiker', 'restaurant', 'Die Klassiker', 'Menü-Einleger A5: die Klassiker, ohne Preise'],
  ['wein-buendner-herrschaft', 'wein', 'Bündner Herrschaft', 'Weinempfehlung DL hoch: Pinot Noir aus der Bündner Herrschaft'],
  ['wein-burgund', 'wein', 'Burgund', 'Weinempfehlung DL hoch: Weisswein aus dem Burgund'],
  ['wein-champagne', 'wein', 'Champagne', 'Weinempfehlung DL hoch: Champagne'],
  ['laestermeile-tapas', 'laestermeile', 'Tapas durchgehend', 'Karte A5 der Lästermeile, ohne Preise'],
  ['hinweiskarte-laestermeile', 'laestermeile', 'Den ganzen Tag', 'Tischaufsteller A6: die Karte der Lästermeile den ganzen Tag'],
  ['hinweiskarte-allergien', 'hinweise', 'Allergien', 'Hinweiskarte A6 am Tisch: Allergene'],
  ['tischkarte-reserviert', 'hinweise', 'Reserviert', 'Tischkarte A7 quer: Reserviert'],
  ['tischkarte-terrasse', 'bib:tischkarte', 'Reserviert · Die Seeterrasse', 'Tischkarte A7 quer: Reserviert auf der Seeterrasse'],
  ['postkarte-bottighofen', 'hafen', 'Postkarte Bottighofen', 'Postkarte A6 quer vom Bootshafen, mit Rückseite'],
  ['postkarte-bodensee', 'hafen', 'Postkarte Bodensee', 'Postkarte A6 quer bis zum Säntis, mit Rückseite'],
  ['gutschein', 'geschenk', 'Gutschein', 'Gutschein DL quer, Vorder- und Rückseite'],
  ['flyer-des-hauses', 'haus', 'Flyer des Hauses', 'Flyer A6, vorne die Terrasse, hinten die Zeiten'],
  ['pressemappe', 'haus', 'Pressemappe', 'Deckblatt A4 der Pressemappe'],
  ['teamaushang-ablauf-bankett', 'bib:teamaushang', 'Ablauf Bankett', 'Team-Aushang A4: Ablauf eines Banketts'],
  ['teamaushang-kuechenzeiten', 'bib:teamaushang', 'Küchenzeiten', 'Team-Aushang A4: Küchenzeiten und Lästermeile'],
  ['instagram-laestermeile', 'laestermeile', 'Die Lästermeile', 'Instagram-Beitrag 4:5: die Bar am Hafen'],
  ['instagram-monika-huber', 'haus', 'Monika Huber', 'Instagram-Beitrag 4:5: die Küchenchefin'],
  ['instagram-weinkeller', 'wein', 'Der Weinkeller', 'Instagram-Beitrag 4:5: GaultMillau über den Weinkeller'],
  ['story-four-hands', 'motive:kreuzfahrt-2026', 'Story', 'Story 9:16: Four-Hands an Bord'],
  ['story-terrasse', 'newsletter', 'Story: Die Terrasse', 'Story 9:16: unter den Platanen'],
];
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  for (const f of fs.readdirSync(ZIEL)) if (/\.(pdf|jpg)$/.test(f)) fs.unlinkSync(path.join(ZIEL, f));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const fehler = []; p.on('pageerror', e => fehler.push(e.message));
  await p.addInitScript(() => { try { localStorage.setItem('ds-schloessli-willkommen', '1'); } catch (e) {} });
  await p.goto('http://127.0.0.1:9287/_werkzeuge/imprimerie/', { waitUntil: 'load' });
  await p.waitForFunction(() => window.DS && DS.M && window.DSStudio && DS.pdf && DS.STIL && DS.STIL.haus, null, { timeout: 30000 });
  await p.waitForTimeout(1500);
  const zeilen = [];
  for (const [k, quelle, n, was] of STUECKE) {
    const r = await p.evaluate(async ({ quelle, n }) => {
      const K = window.DSKATALOG; let x = null;
      if (quelle === 'hinweise') x = K.HINWEISE.find(v => v.n === n);
      else if (quelle === 'newsletter') x = K.NEWSLETTER.find(v => v.n === n);
      else if (quelle.startsWith('motive:')) x = K.motive({ k: quelle.slice(7) }).find(v => v.n === n);
      else if (quelle.startsWith('bib:')) { const d = await (await fetch(DS.M.basis + 'vorlagen/' + quelle.slice(4) + '.json')).json(); const v = d.vorlagen.find(v => v.titel === n); if (v) x = { n: v.titel, format: v.format || d.format, vorlage: v.vorlage, ton: v.ton, inhalt: v.inhalt, stil: v.stil, rueck: v.rueck }; }
      else x = (K.ABTEILUNGEN.find(a => a.k === quelle) || { vorlagen: [] }).vorlagen.find(v => v.n === n);
      if (!x) return { fehlt: true };
      const seiten = [{ vorlage: x.vorlage, ton: x.ton, inhalt: x.inhalt, stil: x.stil }];
      if (x.rueck) seiten.push({ vorlage: x.rueck.vorlage, ton: x.ton, inhalt: x.rueck.inhalt });
      const doc = DS.dokument(DS.M, { name: 'Wirtschaft am Schlössli · ' + n, format: x.format, seiten });
      const alle = (DS.pruefe(DS.M, doc) || []);
      const pr = alle.filter(h => h.stufe === 'rot').map(h => h.text), gelb = alle.filter(h => h.stufe === 'gelb').map(h => h.text);
      const { bytes } = await DS.pdf(DS.M, doc, { marken: false });
      const b64 = u => { let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s); };
      const bilder = [];
      for (let i = 0; i < seiten.length; i++) { const bl = await DS.png(DS.M, doc, i, 1200), bm = await createImageBitmap(bl), cv = document.createElement('canvas'); cv.width = bm.width; cv.height = bm.height; const g = cv.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, cv.width, cv.height); g.drawImage(bm, 0, 0); const jp = await new Promise(ok => cv.toBlob(ok, 'image/jpeg', .86)); bilder.push(b64(new Uint8Array(await jp.arrayBuffer()))); }
      return { pdf: b64(bytes), bilder, rot: pr, gelb, format: DS.FORMATE[x.format].name, seiten: seiten.length };
    }, { quelle, n });
    if (r.fehlt) { console.log('FEHLT', quelle, n); continue; }
    fs.writeFileSync(path.join(ZIEL, k + '.pdf'), Buffer.from(r.pdf, 'base64'));
    r.bilder.forEach((bi, i) => fs.writeFileSync(path.join(ZIEL, k + (i ? '-' + (i + 1) : '') + '.jpg'), Buffer.from(bi, 'base64')));
    zeilen.push({ k, n, was, format: r.format, seiten: r.seiten, rot: r.rot, gelb: r.gelb });
    console.log(k, r.format, r.seiten, 'Seite(n)', r.rot.length ? 'ROT: ' + r.rot.join(' | ') : 'ohne roten Befund', r.gelb.length ? ' GELB: ' + r.gelb.join(' | ') : '');
  }
  zeilen.forEach(x => { x.pdf = x.k + '.pdf'; x.vorschau = Array.from({ length: x.seiten }, (_, i) => x.k + (i ? '-' + (i + 1) : '') + '.jpg'); });
  fs.writeFileSync(path.join(ZIEL, 'liste.json'), JSON.stringify(zeilen, null, 1));
  const md = ['# Drucksachen · Wirtschaft am Schlössli Bottighofen', '',
    'Gesetzt mit der Hausdruckerei (`_werkzeuge/imprimerie/`, Aufruf `node _bau/drucksachen.js`), Inhalte nur aus `website/inhalt/*.json` (Haus, Karte, Lunch, Lästermeile, Wein, Bankett) über `bau_vorlagen.py`. Keine Preise (Regel des Hauses).',
    'PDF mit 3 mm Beschnitt und eingebetteten Schriften (Open Sans, Instrument Sans, DM Mono als TrueType), Vorschaubild 1200 px breit (JPG). Druckprüfung je Stück: ' + (zeilen.every(x => !x.rot.length) ? 'ohne roten Befund.' : 'siehe liste.json.'), '',
    '| Datei | Drucksache | Was | Format | Seiten | Vorschau |', '|---|---|---|---|---|---|',
    ...zeilen.map(x => `| \`${x.pdf}\` | ${x.n} | ${x.was} | ${x.format} | ${x.seiten} | ${x.vorschau.map(v => '`' + v + '`').join(', ')} |`), '',
    'Offen: Die Einladung zum Bankett und die Bestätigungsmail tragen [Datum · Uhrzeit] als Feld zum Ausfüllen; Gutscheinwert und Nummer stehen leer zum Eintragen.'];
  fs.writeFileSync(path.join(ZIEL, 'LISTE.md'), md.join('\n') + '\n');
  if (fehler.length) console.log('Seitenfehler:', fehler.join('\n'));
  await b.close();
})();
