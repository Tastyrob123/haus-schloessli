/* L’Imprimerie · Newsletter-Baukasten, Oberfläche. Vorlagen (Inhalte aus katalog.js NEWSLETTER, nur Belegtes, Unbelegtes in [Klammern]),
   Bausteine anklicken und rechts bearbeiten, Reihenfolge ändern, Fotos des Hauses wählen, Prüfung, Export als .html und «HTML kopieren».
   Gespeichert wird im Browser (localStorage «ds-mails»), erst sobald etwas geändert wird. Satz der Mail: mail-satz.js. */
(function () {
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const PFEIL = '<svg viewBox="0 0 24 24"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>';
  const WEB = 'https://www.instagram.com/schloessli_bottighofen/', TEL = 'tel:+41716889092', MAIL = 'mailto:kontakt@schloessli-bottighofen.ch', RES = 'https://services.gastronovi.com/restaurants/118851/reservation/widget';
  const LOKAL = location.origin + location.pathname.replace(/[^/]*$/, '');
  let M = null;

  /* ---------- Vorlagen: Fakten aus katalog.js (NEWSLETTER), dort gepflegt ---------- */
  const NL = n => ((window.DSKATALOG && DSKATALOG.NEWSLETTER || []).find(x => x.n === n) || {}).inhalt || {};
  const VORLAGEN = [
    { key: "kreuzfahrt", n: "Four-Hands auf dem Rhein", wo: "an alle Gäste", foto: "moni", bau() {
      return { betreff: "Four-Hands an Bord: die Excellence Gourmetkreuzfahrt", vorschau: "Monika Huber kocht mit ihrem Mentor Dieter Koschina auf der Excellence Countess, vom 13. bis 15. November 2026.", versand: "mailchimp",
        kopf: { foto: "moni", alt: "Monika Huber, Küchenchefin, auf der Terrasse" }, fuss: { abmelden: true },
        bloecke: [
          {"typ": "titel", "ueber": "Excellence Gourmetkreuzfahrt", "titel": "Four-Hands an Bord", "unter": "13. bis 15. November 2026"},
          {"typ": "text", "text": "Guten Tag [Name]\n\nGemeinsam mit einem ihrer grossen Mentoren, Dieter Koschina, geht unsere Küchenchefin Monika Huber an Bord der Excellence Countess. Start ist am Freitag in Basel, über Nacht geht es nach Strassburg, am Samstag denselben Weg zurück.", "ausr": "mitte"},
          {"typ": "termine", "titel": "", "eintraege": [{"wann": "Freitag, 13. November · 15:00", "was": "Start in Basel", "wo": "Excellence Countess"}, {"wann": "Sonntag, 15. November · 14:00", "was": "Ankunft in Basel", "wo": ""}]},
          {"typ": "foto", "foto": "iberia", "alt": "Fisch in grüner Sauce in einer gerippten Schale, daneben ein Weinglas", "unterschrift": "Welcome-Apéro, Live-Musik, Gala-Dinner und DJ", "voll": false},
          {"typ": "text", "text": "Unser Restaurant ist über diese drei Tage geschlossen, da unser Team geschlossen mit an Bord ist.", "ausr": "mitte"},
          {"typ": "knopf", "text": "Zur Reise auf excellence.ch", "link": "https://www.excellence.ch/flusskreuzfahrten/gourmetfestival-dieter-koschina-monika-huber-eobas88-gf"},
        ] };
    } },
    { key: "ferien", n: "Wir machen Ferien", wo: "an alle Gäste", foto: "morgen", bau() {
      return { betreff: "Betriebsferien vom 22. Dezember bis 10. Februar", vorschau: "Danke für dieses Jahr am See. Ab dem 11. Februar 2027 sind wir wieder für Sie da.", versand: "mailchimp",
        kopf: { foto: "morgen", alt: "Morgen am Bodensee, hinten die Alpen und die Schifflände Bottighofen" }, fuss: { abmelden: true },
        bloecke: [
          {"typ": "titel", "ueber": "Betriebsferien", "titel": "Wir machen Ferien", "unter": "22. Dezember 2026 - 10. Februar 2027"},
          {"typ": "text", "text": "Guten Tag [Name]\n\nDanke für dieses Jahr am See. Vom 22. Dezember 2026 bis zum 10. Februar 2027 bleibt die Wirtschaft am Schlössli geschlossen.", "ausr": "mitte"},
          {"typ": "trenner"},
          {"typ": "termine", "titel": "", "eintraege": [{"wann": "Ab 11. Februar 2027", "was": "Wieder für Sie da", "wo": "Donnerstag - Montag · 11:30 Uhr - 23:00 Uhr"}]},
          {"typ": "knopf", "text": "Tisch reservieren", "link": RES},
        ] };
    } },
    { key: "lunch", n: "Das Lunch-Menü", wo: "an Stammgäste", foto: "tortelloni", bau() {
      return { betreff: "Lunch am See: drei Gänge am Mittag", vorschau: "Kürbissuppe, Risi e bisi und Joghurt Panna Cotta, Donnerstag bis Montag am Mittag.", versand: "mailchimp",
        kopf: { foto: "tortelloni", alt: "Tortelloni mit Tomate, Burrata und Taggiasca-Olive" }, fuss: { abmelden: true },
        bloecke: [
          {"typ": "titel", "ueber": "Am Mittag", "titel": "Lunch am See", "unter": "Drei Gänge"},
          {"typ": "text", "text": "Guten Tag [Name]\n\nAm Mittag gibt es bei uns ein Lunch-Menü mit drei Gängen, direkt im Hafen von Bottighofen.", "ausr": "mitte"},
          {"typ": "termine", "titel": "", "eintraege": [{"wann": "Kürbissuppe", "was": "Wachtelei · Serrano Schinken", "wo": ""}, {"wann": "Risi e bisi", "was": "Reis · Miesmuschel · Erbsen · Spinat", "wo": ""}, {"wann": "Joghurt Panna Cotta", "was": "Apfelcrumble", "wo": ""}]},
          {"typ": "text", "text": "Küche 11:30 Uhr - 13:30 Uhr. Dienstag & Mittwoch Ruhetag.", "ausr": "mitte"},
          {"typ": "knopf", "text": "Tisch reservieren", "link": RES},
        ] };
    } },
    { key: "bankett", n: "Banketts & Gruppen", wo: "an Anfragen", foto: "gaststube", bau() {
      return { betreff: "Ihr Fest in der Wirtschaft am Schlössli", vorschau: "Auf zwei Etagen für jeweils bis zu 26 Personen, Tavolata oder gesetztes Menü.", versand: "anderes",
        kopf: { foto: "gaststube", alt: "Die Gaststube mit grossen Fenstern zum Hafen" }, fuss: { abmelden: false },
        bloecke: [
          {"typ": "titel", "ueber": "Banketts & Gruppen", "titel": "Ihr Fest am See", "unter": ""},
          {"typ": "text", "text": "Guten Tag [Name]\n\nGerne übernehmen wir die Bewirtung Ihrer Familien- oder Firmenfeier. Sie geben den Rahmen vor, ob Tavolata oder gesetztes Menü. Welches Gericht darf auf keinen Fall fehlen, welche Allergien müssen wir bedenken?", "ausr": "mitte"},
          {"typ": "termine", "titel": "", "eintraege": [{"wann": "Zwei Etagen", "was": "für jeweils bis zu 26 Personen", "wo": ""}, {"wann": "Menüs", "was": "Frühling, Sommer, Herbst: drei bis fünf Gerichte nach Wahl", "wo": ""}]},
          {"typ": "text", "text": "Wir richten uns individuell nach Ihnen und Ihren Wünschen und besprechen alles gerne auch vor Ort in Ruhe.", "ausr": "mitte"},
          {"typ": "knopf", "text": "Anfrage per Telefon", "link": TEL},
        ] };
    } },
    { key: "reservation", n: "Ihr Tisch am See", wo: "Bestätigungsmail", foto: "platanen", bau() {
      return { betreff: "Ihr Tisch in der Wirtschaft am Schlössli", vorschau: "[Datum] · [Uhrzeit] · Seestrasse 50 · 8598 Bottighofen", versand: "anderes",
        kopf: { foto: "platanen", alt: "Gedeckte Tische unter den Platanen, Sonnenschirme, dahinter der Hafen" }, fuss: { abmelden: false },
        bloecke: [
          {"typ": "titel", "ueber": "Wirtschaft am Schlössli", "titel": "Ihr Tisch am See", "unter": ""},
          {"typ": "text", "text": "Guten Tag [Name]\n\nwir freuen uns auf Ihren Besuch."},
          {"typ": "termine", "titel": "", "eintraege": [{"wann": "[Datum · Uhrzeit]", "was": "[Personen]", "wo": ""}, {"wann": "Wo", "was": "Seestrasse 50 · 8598 Bottighofen", "wo": ""}]},
          {"typ": "text", "text": "Am Kreisverkehr beim Restaurant Bären in die Seestrasse Richtung Hafen, über den Bahnübergang bis zu unserem Parkplatz."},
          {"typ": "knopf", "text": "Bei Fragen anrufen", "link": TEL},
        ] };
    } },
    { key: "danke", n: "Danke für Ihren Besuch", wo: "Dankesmail", foto: "abend", bau() {
      return { betreff: "Danke für Ihren Besuch", vorschau: "Schön, dass Sie bei uns am Hafen waren.", versand: "anderes",
        kopf: { foto: "abend", alt: "Abend unter der Platane mit Lichterkette, Gäste am Tisch über dem See" }, fuss: { abmelden: false },
        bloecke: [
          {"typ": "titel", "ueber": "Wirtschaft am Schlössli", "titel": "Danke für Ihren Besuch", "unter": ""},
          {"typ": "text", "text": "Guten Tag [Name]\n\nSchön, dass Sie bei uns am Hafen waren. Wir freuen uns, Sie bald wieder auf der Terrasse oder an der Lästermeile zu sehen.", "ausr": "mitte"},
          {"typ": "trenner"},
          {"typ": "text", "text": "Donnerstag - Montag · 11:30 Uhr - 23:00 Uhr. Dienstag & Mittwoch Ruhetag.", "ausr": "mitte"},
          {"typ": "knopf", "text": "Wieder reservieren", "link": RES},
        ] };
    } },
    { key: 'leer', n: 'Leere E-Mail', wo: 'selbst aufbauen', foto: '', bau() {
      return { betreff: '', vorschau: '', versand: 'mailchimp', kopf: { foto: '' }, fuss: { abmelden: true },
        bloecke: [{ typ: 'titel', ueber: 'Wirtschaft am Schlössli', titel: 'Titel', unter: '' }, { typ: 'text', text: 'Ihr Text.' }] };
    } },
  ];

  const ARTEN = {
    titel: { n: 'Titel', ic: '<path d="M5 6h14M12 6v13"/>', neu: () => ({ typ: 'titel', ueber: 'Wirtschaft am Schlössli', titel: 'Titel', unter: '' }) },
    text: { n: 'Text', ic: '<path d="M4 6h16M4 10h16M4 14h16M4 18h10"/>', neu: () => ({ typ: 'text', text: 'Ihr Text.' }) },
    foto: { n: 'Foto', ic: '<path d="M4 5h16v14H4zM4 16l5-5 4 4 2.5-2.5L20 17"/>', neu: () => ({ typ: 'foto', foto: 'start', alt: 'Blaue Stühle auf der Terrasse am Mittag, dahinter der Bodensee und die Alpen', unterschrift: '', voll: false }) },
    knopf: { n: 'Knopf', ic: '<rect x="3" y="6" width="18" height="12" rx="6"/><path d="M14 12h3m-1.5-1.5L17 12l-1.5 1.5"/>', neu: () => ({ typ: 'knopf', text: 'Mehr erfahren', link: WEB }) },
    termine: { n: 'Termine', ic: '<path d="M4 6h16v14H4zM4 10h16M8 3v4M16 3v4"/>', neu: () => ({ typ: 'termine', titel: '', eintraege: [{ wann: '[Datum · Zeit]', was: '[Anlass]', wo: '[Ort]' }] }) },
    liste: { n: 'Preisliste', ic: '<path d="M4 7h11M4 12h11M4 17h11M18 7h2M18 12h2M18 17h2"/>', neu: () => ({ typ: 'liste', titel: '', eintraege: [{ name: '[Name]', detail: '[Beschreibung]', preis: 'CHF [Preis]' }] }) },
    trenner: { n: 'Zierlinie', ic: '<path d="M3 12h6M15 12h6M12 9l3 3-3 3-3-3z"/>', neu: () => ({ typ: 'trenner' }) },
  };

  /* ---------- Ablage im Browser ---------- */
  const lies = () => { try { return JSON.parse(localStorage.getItem('ds-mails') || '[]'); } catch (e) { return []; } };
  const schreib = l => { try { localStorage.setItem('ds-mails', JSON.stringify(l)); } catch (e) {} };
  let doc = null, id = null, wahl = null, geraet = 600, speicherT = 0;
  function neu(v) { doc = Object.assign({ name: v.n }, v.bau()); doc.vorlage = v.key; id = null; wahl = null; zeichne(); zeigeWahl(); markiere(); }
  function oeffne(e) { doc = JSON.parse(JSON.stringify(e.doc)); id = e.id; wahl = null; zeichne(); zeigeWahl(); markiere(); }
  let zeichneT = 0;
  function geaendert() {
    clearTimeout(zeichneT); zeichneT = setTimeout(() => zeichne(true), 140);
    clearTimeout(speicherT); speicherT = setTimeout(() => {
      const l = lies(); if (!id) id = 'm' + Date.now().toString(36);
      const e = { id, name: doc.name, vorlage: doc.vorlage, geaendert: Date.now(), doc };
      const i = l.findIndex(x => x.id === id); if (i >= 0) l[i] = e; else l.unshift(e);
      schreib(l); zeichneMeine(); markiere(); $('#mlGespeichert').classList.add('an'); setTimeout(() => $('#mlGespeichert').classList.remove('an'), 1400);
    }, 400);
  }

  /* ---------- Vorschau ---------- */
  let ifrScroll = 0;
  function zeichne(behalte) {
    const f = $('#mlRahmen'); if (behalte && f.contentWindow) ifrScroll = f.contentWindow.scrollY || 0;
    f.srcdoc = DSMAIL.html(doc, { basis: LOKAL, editor: true, M });
    $('#mlBetreff').textContent = doc.betreff || 'Kein Betreff';
    $('#mlVorschau').textContent = doc.vorschau || '';
    $('#mlName').value = doc.name || '';
    pruefung();
  }
  function rahmenGeladen() {
    const f = $('#mlRahmen'), d = f.contentDocument; if (!d || !d.body) return;
    const hoehe = () => { f.style.height = Math.max(600, d.documentElement.scrollHeight) + 'px'; };
    hoehe(); d.querySelectorAll('img').forEach(i => i.complete || i.addEventListener('load', hoehe));
    if (d.fonts) d.fonts.ready.then(hoehe);
    if (wahl != null) { const el = d.querySelector(`[data-b="${wahl}"]`); if (el) el.classList.add('an'); }
    d.addEventListener('pointermove', e => { if (e.pointerType !== 'mouse') return; const r = f.getBoundingClientRect(), k = r.width / f.offsetWidth; kippe(r.left + e.clientX * k, r.top + e.clientY * k); });
    d.addEventListener('click', e => { e.preventDefault(); const t = e.target.closest('[data-b]'); if (!t) return; const b = t.dataset.b; waehle(/^\d+$/.test(b) ? +b : b); });
  }
  /* 3D wie die Kacheln der Startseite: das Blatt neigt sich zur Maus, Licht wandert mit; gedreht wird um die Mitte des sichtbaren Ausschnitts */
  let kippRaf = 0, kippXY = null;
  function kippe(cx, cy) {
    kippXY = [cx, cy]; if (kippRaf) return;
    kippRaf = requestAnimationFrame(() => {
      kippRaf = 0; const b = $('#mlBlatt'), m = $('.ml-mitte'); if (!b || !kippXY) return;
      const r = b.getBoundingClientRect(), mr = m.getBoundingClientRect(), [x0, y0] = kippXY;
      const x = Math.max(-.5, Math.min(.5, (x0 - r.left) / r.width - .5)), y = Math.max(-.5, Math.min(.5, (y0 - mr.top) / mr.height - .5));
      b.style.transformOrigin = `50% ${Math.round(mr.top + mr.height / 2 - r.top)}px`;
      b.classList.add('kipp');
      b.style.setProperty('--ry', (x * 5).toFixed(2) + 'deg'); b.style.setProperty('--rx', (-y * 3.5).toFixed(2) + 'deg');
      b.style.setProperty('--gx', Math.round(x0 - r.left) + 'px'); b.style.setProperty('--gy', Math.round(y0 - r.top) + 'px');
    });
  }
  function loeseKipp() { kippXY = null; const b = $('#mlBlatt'); if (!b) return; b.classList.remove('kipp'); ['--rx', '--ry'].forEach(v => b.style.removeProperty(v)); }
  function markiereRahmen() { const d = $('#mlRahmen').contentDocument; if (!d) return; d.querySelectorAll('[data-b]').forEach(el => el.classList.toggle('an', String(wahl) === el.dataset.b)); }

  /* ---------- Rechte Platte: Baustein bearbeiten ---------- */
  const feld = (k, n, val, art = 'input', extra = '') => art === 'textarea'
    ? `<label class="ml-f"><span>${n}</span><textarea data-k="${k}" rows="${extra || 5}">${esc(val)}</textarea></label>`
    : `<label class="ml-f"><span>${n}</span><textarea class="ml-zeile" rows="1" data-k="${k}" spellcheck="${/link|url/.test(k) ? 'false' : 'true'}"${extra}>${esc(val)}</textarea></label>`;   // eine Zeile, die mitwächst statt den Text abzuschneiden (Messlauf 29.10.)
  /* Felder wachsen mit ihrem Text (Messlauf 29.10.2026: Vorschauzeile und Betreff ragten aus dem Kasten) */
  const wachse = box => (box || document).querySelectorAll('#mlFelder textarea').forEach(t => { t.style.height = 'auto'; t.style.height = t.scrollHeight + 2 + 'px'; });
  const ausr = (b, std) => `<label class="ml-f"><span>Ausrichtung</span><select data-k="ausr"><option value="mitte"${(b.ausr || std) === 'mitte' ? ' selected' : ''}>Mittig</option><option value="links"${(b.ausr || std) === 'links' ? ' selected' : ''}>Linksbündig</option></select></label>`;
  function fotoFeld(b, kopf) {
    const src = b.url ? b.url : (b.foto ? DSMAIL.bildUrl(b.foto, LOKAL) : '');
    return `<div class="ml-f"><span>Foto</span><button class="ml-foto" data-akt="foto">${src ? `<img src="${esc(src)}" alt="">` : '<i>Kein Foto</i>'}<b>Foto wählen</b></button>
      ${kopf && (b.foto || b.url) ? '<button class="ml-mini" data-akt="ohnefoto">Ohne Kopfbild</button>' : ''}</div>
      ${feld('alt', 'Bildbeschreibung (für Mailprogramme ohne Bilder)', b.alt || '')}
      <details class="ml-mehr"${b.url ? ' open' : ''}><summary>Eigenes Foto über eine Adresse</summary>${feld('url', 'Bildadresse (https://…, zum Beispiel aus Mailchimp)', b.url || '')}</details>`;
  }
  function eintraege(b) {
    const sp = b.typ === 'termine' ? [['wann', 'Wann'], ['was', 'Was'], ['wo', 'Wo / Zusatz']] : [['name', 'Name'], ['detail', 'Beschreibung'], ['preis', 'Preis']];
    return `<div class="ml-eintraege">${(b.eintraege || []).map((e, j) => `<div class="ml-eintrag" data-j="${j}"><div class="ml-eintrag__kopf"><em>${j + 1}</em>
      <button class="rund rund--klein" data-akt="ehoch" title="Nach oben" ${j ? '' : 'disabled'}><svg viewBox="0 0 24 24"><path d="m6 15 6-6 6 6"/></svg></button>
      <button class="rund rund--klein" data-akt="eweg" title="Entfernen" aria-label="Entfernen"><svg viewBox="0 0 24 24"><path d="M5 7h14M10 7V5h4v2M7 7l1 12h8l1-12"/></svg></button></div>
      ${sp.map(([k, n]) => `<label class="ml-f ml-f--klein"><span>${n}</span><input type="text" data-e="${k}" value="${esc(e[k] || '')}"></label>`).join('')}</div>`).join('')}
      <button class="kn kn--klein kn--ohne ml-dazu" data-akt="edazu"><span>Eintrag hinzufügen</span></button></div>`;
  }
  function zeigeWahl() {
    const box = $('#mlFelder'), n = (doc.bloecke || []).length;
    if (wahl == null || wahl === 'mail') {
      box.innerHTML = `<div class="ml-kopfzeile"><h2><small>Einstellungen</small>Die E-Mail</h2></div>
        ${feld('name', 'Name in Ihrer Ablage', doc.name || '')}
        ${feld('betreff', 'Betreff', doc.betreff || '')}
        ${feld('vorschau', 'Vorschauzeile (erscheint im Posteingang nach dem Betreff)', doc.vorschau || '', 'textarea', 2)}
        <label class="ml-f"><span>Verschickt mit</span><select data-k="versand">${Object.entries(DSMAIL.VERSAND).map(([k, v]) => `<option value="${k}"${doc.versand === k ? ' selected' : ''}>${v.name}</option>`).join('')}</select></label>
        <p class="ml-leise ml-versand">Von hier aus wird nichts verschickt. Wählen Sie hier das Programm, mit dem Sie Ihren Newsletter schon verschicken: Der Abmeldelink wird so gesetzt, wie dieses Programm ihn braucht, und gibt Ihnen die fertige Mail zum Einfügen dort. Haben Sie kein solches Programm, wählen Sie «Anderes Programm»: Dann steht im Fuss [Abmeldelink], den ersetzen Sie vor dem Versand.</p>
        <p class="ml-leise ml-tipp">Tipp: Tippen Sie in der Vorschau einen Teil der E-Mail an, öffnet er sich hier zum Bearbeiten.</p>`;   // Versand und Bearbeiten getrennt erklärt (Robert 29.10.2026)
    } else if (wahl === 'kopf') {
      box.innerHTML = `<div class="ml-kopfzeile"><h2><small>Teil der E-Mail</small>Kopf</h2></div><p class="ml-leise">Oben stehen Zeichen und Name des Hauses, darunter das Kopfbild.</p>${fotoFeld(doc.kopf || {}, true)}`;
    } else if (wahl === 'fuss') {
      const f = doc.fuss || {};
      box.innerHTML = `<div class="ml-kopfzeile"><h2><small>Teil der E-Mail</small>Fuss</h2></div><p class="ml-leise">Adresse, Telefon, E-Mail und Website des Hauses stehen fest im Fuss.</p>
        <label class="haken"><input type="checkbox" data-k="abmelden"${f.abmelden !== false ? ' checked' : ''}> Abmeldelink zeigen (Pflicht bei Newslettern)</label>
        ${feld('text', 'Zusatz im Fuss (freiwillig)', f.text || '', 'textarea', 2)}`;
    } else {
      const b = doc.bloecke[wahl]; if (!b) { wahl = null; return zeigeWahl(); }
      let f = '';
      if (b.typ === 'titel') f = feld('ueber', 'Kleine Zeile darüber', b.ueber || '') + feld('titel', 'Titel', b.titel || '') + feld('unter', 'Unterzeile kursiv', b.unter || '') + ausr(b, 'mitte');
      if (b.typ === 'text') f = feld('text', 'Text (Leerzeile = neuer Absatz)', b.text || '', 'textarea', 8) + ausr(b, 'links');
      if (b.typ === 'foto') f = fotoFeld(b) + `<label class="haken"><input type="checkbox" data-k="voll"${b.voll ? ' checked' : ''}> Über die ganze Breite</label>` + feld('unterschrift', 'Bildunterschrift (freiwillig)', b.unterschrift || '') + feld('link', 'Link beim Antippen (freiwillig)', b.link || '');
      if (b.typ === 'knopf') f = feld('text', 'Beschriftung', b.text || '') + feld('link', 'Adresse (https://… oder tel:)', b.link || '')
        + `<div class="ml-chips"><button data-akt="lnk" data-l="${WEB}">Website</button><button data-akt="lnk" data-l="${TEL}">Telefon</button></div>`;
      if (b.typ === 'termine' || b.typ === 'liste') f = feld('titel', 'Überschrift (freiwillig)', b.titel || '') + eintraege(b);
      if (b.typ === 'trenner') f = '<p class="ml-leise">Eine feine Linie mit dem Zeichen des Hauses.</p>';
      box.innerHTML = `<div class="ml-kopfzeile"><h2><small>Baustein</small>${String(ARTEN[b.typ].n).replace(/ (\S+)$/, '\u00a0$1')}</h2><span class="ml-werk">
        <button class="rund rund--klein" data-akt="hoch" title="Nach oben" ${wahl ? '' : 'disabled'}><svg viewBox="0 0 24 24"><path d="m6 15 6-6 6 6"/></svg></button>
        <button class="rund rund--klein" data-akt="runter" title="Nach unten" ${wahl < n - 1 ? '' : 'disabled'}><svg viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button>
        <button class="rund rund--klein" data-akt="doppeln" title="Doppeln"><svg viewBox="0 0 24 24"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/></svg></button>
        <button class="rund rund--klein" data-akt="weg" title="Entfernen"><svg viewBox="0 0 24 24"><path d="M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13"/></svg></button></span></div>${f}`;
    }
    $$('.ml-nav [data-teil]').forEach(x => x.classList.toggle('an', String(wahl ?? 'mail') === x.dataset.teil));
  }
  function waehle(w) { wahl = w; zeigeWahl(); markiereRahmen(); }
  function ziel() { if (wahl === 'kopf') return doc.kopf = doc.kopf || {}; if (wahl === 'fuss') return doc.fuss = doc.fuss || {}; if (wahl == null || wahl === 'mail') return doc; return doc.bloecke[wahl]; }

  function eingabe(e) {
    const t = e.target, z = ziel(); if (!z) return;
    if (t.dataset.k) { const k = t.dataset.k; z[k] = t.type === 'checkbox' ? t.checked : t.value; if (k === 'url' && t.value.trim()) z.foto = z.foto; }
    else if (t.dataset.e) { const j = +t.closest('[data-j]').dataset.j; z.eintraege[j][t.dataset.e] = t.value; }
    else return;
    geaendert();
  }
  function aktion(a, el) {
    const bl = doc.bloecke, z = ziel();
    if (a === 'hoch' || a === 'runter') { const j = wahl + (a === 'hoch' ? -1 : 1); [bl[wahl], bl[j]] = [bl[j], bl[wahl]]; wahl = j; }
    else if (a === 'doppeln') { bl.splice(wahl + 1, 0, JSON.parse(JSON.stringify(bl[wahl]))); wahl++; }
    else if (a === 'weg') { bl.splice(wahl, 1); wahl = bl.length ? Math.min(wahl, bl.length - 1) : null; }
    else if (a === 'edazu') { z.eintraege.push(z.typ === 'termine' ? { wann: '', was: '', wo: '' } : { name: '', detail: '', preis: '' }); }
    else if (a === 'eweg') { z.eintraege.splice(+el.closest('[data-j]').dataset.j, 1); }
    else if (a === 'ehoch') { const j = +el.closest('[data-j]').dataset.j; [z.eintraege[j - 1], z.eintraege[j]] = [z.eintraege[j], z.eintraege[j - 1]]; }
    else if (a === 'lnk') { z.link = el.dataset.l; }
    else if (a === 'ohnefoto') { z.foto = ''; z.url = ''; }
    else if (a === 'foto') return fotoWahl();
    else return;
    zeigeWahl(); geaendert();
  }
  function einfuegen(typ) {
    const b = ARTEN[typ].neu(), pos = typeof wahl === 'number' ? wahl + 1 : (wahl === 'kopf' ? 0 : doc.bloecke.length);
    doc.bloecke.splice(pos, 0, b); wahl = pos; zeigeWahl(); geaendert();
    setTimeout(() => { const d = $('#mlRahmen').contentDocument, el = d && d.querySelector(`[data-b="${pos}"]`); if (el) el.scrollIntoView({ block: 'center' }); }, 250);
  }

  /* ---------- Fotos des Hauses ---------- */
  let fGruppe = 'Alle';
  function fotoWahl() {
    const dlg = $('#mlFotos'), gruppen = ['Alle', ...new Set(M.bilder.map(b => b.gruppe))];
    $('#mlFotoGruppen').innerHTML = gruppen.map(g => `<button data-g="${esc(g)}" class="${g === fGruppe ? 'an' : ''}">${esc(g)}</button>`).join('');
    fotoRaster(); dlg.showModal(); $('#mlFotoSuche').focus();
  }
  function fotoRaster() {
    const q = $('#mlFotoSuche').value.trim().toLowerCase(), z = ziel() || {};
    const l = M.bilder.filter(b => (fGruppe === 'Alle' || b.gruppe === fGruppe) && (!q || (b.alt + ' ' + b.key + ' ' + b.gruppe).toLowerCase().includes(q)));
    $('#mlFotoRaster').innerHTML = l.map(b => `<button data-foto="${b.key}" class="${z.foto === b.key && !z.url ? 'an' : ''}" title="${esc(b.alt)}"><img loading="lazy" src="haeuser/schloessli/mini/${b.key}.webp" alt=""><span>${esc(b.alt)}</span></button>`).join('') || '<p class="ml-leise">Nichts gefunden.</p>';
  }

  /* ---------- Prüfung, Ausgabe ---------- */
  function pruefung() {
    const p = DSMAIL.pruefe(doc), z = $('#mlPruefZahl');
    z.textContent = p.length; z.parentElement.classList.toggle('gut', !p.length);
    $('#mlPruefListe').innerHTML = p.length ? p.map(x => `<button data-zu="${x.b}"><i></i><span>${esc(x.t)}</span></button>`).join('') : '<p class="ml-gut">Alles bereit zum Versand.</p>';
  }
  const dateiname = () => (doc.name || 'E-Mail').toLowerCase().replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') + '.html';
  const fertig = () => DSMAIL.html(doc, { M });
  function hinweis(t) { const h = $('#mlHinweis'); h.innerHTML = t; h.hidden = false; h.classList.remove('an'); void h.offsetWidth; h.classList.add('an'); clearTimeout(h._t); h._t = setTimeout(() => { h.hidden = true; }, 5200); }
  async function kopiere() {
    const h = fertig();
    try { await navigator.clipboard.writeText(h); }
    catch (e) { const t = document.createElement('textarea'); t.value = h; document.body.appendChild(t); t.select(); document.execCommand('copy'); t.remove(); }
    const p = DSMAIL.pruefe(doc).length;
    hinweis(`<b>HTML kopiert.</b> Im Versandprogramm die Gestaltung mit eigenem Code wählen und einfügen.${p ? ` Vorher noch ${p} ${p === 1 ? 'Punkt' : 'Punkte'} der Prüfung erledigen.` : ''}`);
  }
  function speichere() {
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([fertig()], { type: 'text/html;charset=utf-8' })); a.download = dateiname();
    document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 800);
    hinweis(`<b>${esc(dateiname())}</b> gespeichert. Die Datei lässt sich im Browser öffnen oder im Versandprogramm hochladen.`);
  }

  /* ---------- Linke Platte: Vorlagen, Meine E-Mails, Teile ---------- */
  function zeichneVorlagen() {
    $('#mlVorlagen').innerHTML = VORLAGEN.map(v => `<button data-vorlage="${v.key}"><span class="ml-vb"${v.foto ? ` style="background-image:url('haeuser/schloessli/mini/${v.foto}.webp')"` : ''}></span><span><b>${esc(v.n).replace(/ (\S+)$/, '\u00a0$1')}</b><small>${esc(v.wo)}</small></span></button>`).join('');
  }
  function zeichneMeine() {
    const l = lies(); $('#mlMeineZahl').textContent = l.length; $('#mlMeineBox').hidden = !l.length;
    $('#mlMeine').innerHTML = l.map(e => `<div class="ml-meine__e" data-id="${e.id}"><button data-mail="${e.id}"><b>${esc(e.name || 'E-Mail')}</b><small>${new Date(e.geaendert).toLocaleString('de-CH', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}</small></button><button class="ml-x" data-loesch="${e.id}" title="Löschen" aria-label="Löschen"><svg viewBox="0 0 24 24"><path d="M5 7h14M10 7V5h4v2M7 7l1 12h8l1-12"/></svg></button></div>`).join('');
  }
  function markiere() {
    $$('#mlVorlagen [data-vorlage]').forEach(b => b.classList.toggle('an', !id && doc.vorlage === b.dataset.vorlage));
    $$('#mlMeine [data-mail]').forEach(b => b.classList.toggle('an', id === b.dataset.mail));
  }

  async function los() {
    M = await (await fetch('haeuser/schloessli/marke.json')).json();
    const z = M.zeichen, svg = `<svg viewBox="${z.vb.join(' ')}">${z.pfade.map(d => `<path d="${d}"/>`).join('')}</svg>`;
    $('#mlZeichen').innerHTML = svg; $('#mlKapitelZeichen').innerHTML = svg;
    zeichneVorlagen(); zeichneMeine();
    $('#mlEinfuegen').innerHTML = Object.entries(ARTEN).map(([k, a]) => `<button data-neu="${k}"><svg viewBox="0 0 24 24">${a.ic}</svg><span>${String(a.n).replace(/ (\S+)$/, '\u00a0$1')}</span></button>`).join('');
    const q = new URLSearchParams(location.search), v = VORLAGEN.find(x => x.key === q.get('vorlage')), l = lies();
    const gesp = l.find(x => x.id === q.get('mail'));
    if (gesp) oeffne(gesp); else if (v) neu(v); else if (l.length) oeffne(l[0]); else neu(VORLAGEN[0]);

    $('#mlRahmen').addEventListener('load', () => { rahmenGeladen(); const w = $('#mlRahmen').contentWindow; if (ifrScroll) { w.scrollTo(0, ifrScroll); } });
    $('#mlFelder').addEventListener('input', eingabe); $('#mlFelder').addEventListener('change', eingabe);
    $('#mlFelder').addEventListener('input', e => { if (e.target.tagName === 'TEXTAREA') wachse(); });
    $('#mlFelder').addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.classList.contains('ml-zeile')) { e.preventDefault(); e.target.blur(); } });
    new MutationObserver(() => requestAnimationFrame(() => wachse())).observe($('#mlFelder'), { childList: true }); addEventListener('resize', () => wachse()); wachse(); document.fonts.ready.then(() => wachse());
    document.addEventListener('click', e => {
      const t = e.target;
      const ak = t.closest('[data-akt]'); if (ak && !ak.disabled) return aktion(ak.dataset.akt, ak);
      const vo = t.closest('[data-vorlage]'); if (vo) return neu(VORLAGEN.find(x => x.key === vo.dataset.vorlage));
      const me = t.closest('[data-mail]'); if (me) return oeffne(lies().find(x => x.id === me.dataset.mail));
      const lo = t.closest('[data-loesch]'); if (lo) { if (!confirm('Diese E-Mail aus der Ablage löschen?')) return; schreib(lies().filter(x => x.id !== lo.dataset.loesch)); if (id === lo.dataset.loesch) id = null; zeichneMeine(); markiere(); return; }
      const nb = t.closest('[data-neu]'); if (nb) return einfuegen(nb.dataset.neu);
      const te = t.closest('[data-teil]'); if (te) return waehle(te.dataset.teil);
      const zu = t.closest('[data-zu]'); if (zu) { $('#mlPruefen').open = false; const b = zu.dataset.zu; waehle(/^\d+$/.test(b) ? +b : b); return; }
      const ge = t.closest('[data-geraet]'); if (ge) { geraet = +ge.dataset.geraet; $$('[data-geraet]').forEach(x => x.classList.toggle('an', x === ge)); $('#mlBuehne').style.setProperty('--w', geraet + 'px'); $('#mlBuehne').classList.toggle('ml-handy', geraet < 600); setTimeout(rahmenGeladen, 80); return; }
      const fo = t.closest('[data-foto]'); if (fo) { const z = ziel(), b = M.bilder.find(x => x.key === fo.dataset.foto); z.foto = b.key; z.url = ''; z.alt = b.alt; $('#mlFotos').close(); zeigeWahl(); geaendert(); return; }
      const g = t.closest('#mlFotoGruppen [data-g]'); if (g) { fGruppe = g.dataset.g; $$('#mlFotoGruppen button').forEach(x => x.classList.toggle('an', x === g)); fotoRaster(); return; }
    });
    $('.ml-mitte').addEventListener('pointermove', e => { if (e.pointerType === 'mouse') kippe(e.clientX, e.clientY); });
    $('.ml-mitte').addEventListener('pointerleave', loeseKipp);
    $('#mlRahmen').addEventListener('pointerleave', e => { const m = $('.ml-mitte').getBoundingClientRect(); if (e.clientX < m.left || e.clientX > m.right) loeseKipp(); });
    $('#mlFotoSuche').addEventListener('input', fotoRaster);
    $('#mlFotoZu').addEventListener('click', () => $('#mlFotos').close());
    $('#mlFotos').addEventListener('click', e => { if (e.target === $('#mlFotos')) $('#mlFotos').close(); });
    $('#mlName').addEventListener('input', e => { doc.name = e.target.value; geaendert(); });
    $('#mlKopieren').addEventListener('click', kopiere);
    $('#mlDatei').addEventListener('click', speichere);
    $('#mlFenster').addEventListener('click', () => { const w = window.open('', '_blank'); if (w) { w.document.open(); w.document.write(DSMAIL.html(doc, { basis: LOKAL, M })); w.document.close(); } });
    document.addEventListener('click', e => { const p = $('#mlPruefen'); if (p.open && !e.target.closest('#mlPruefen')) p.open = false; });
    document.body.classList.add('an');
    /* K5 (Tor 2, 30.10.2026): reicht die mittlere Spalte nicht (z. B. 1000 px), wird die Vorschau als Ganzes kleiner, nie angeschnitten und nie seitlich scrollend */
    /* Ohne Sperre über requestAnimationFrame (4.11.2026, Prüftor WebKit 390): lief kein Bild dazwischen, blieb die Sperre stehen, und beim Wechsel auf 390 px
       behielt die Bühne Verkleinerung und negative Ränder der breiten Ansicht (Posteingang 137…662 px im 390-px-Fenster). Jetzt wird nur geschrieben, was sich ändert
       (offsetWidth/offsetHeight hängen weder an scale noch an den Rändern), dann ruft der Beobachter nichts nach. zoom schneidet in Safari das iframe ab, darum scale. */
    const passe = () => { const m = $('.ml-mitte'), b = $('#mlBuehne'); if (!m || !b) return;
      let soll = { scale: '', transformOrigin: '', marginLeft: '', marginRight: '', marginBottom: '' };
      if (innerWidth > 980) { const g = getComputedStyle(m), frei = m.clientWidth - parseFloat(g.paddingLeft) - parseFloat(g.paddingRight), W = b.offsetWidth, H = b.offsetHeight, z = Math.min(1, frei / W);
        if (z < 1) soll = { scale: z.toFixed(3), transformOrigin: '50% 0', marginLeft: `${-(W - z * W) / 2}px`, marginRight: `${-(W - z * W) / 2}px`, marginBottom: `${-(H - z * H)}px` }; }
      const key = JSON.stringify(soll); if (b.__passe === key) return; b.__passe = key; Object.assign(b.style, soll); };
    addEventListener('resize', passe); new MutationObserver(passe).observe($('#mlBuehne'), { attributes: true, attributeFilter: ['style', 'class'] }); passe();
  }
  window.__ML = { get doc() { return doc; }, VORLAGEN, neu: k => neu(VORLAGEN.find(x => x.key === k)), html: o => DSMAIL.html(doc, o || { M }) };
  los();
})();
