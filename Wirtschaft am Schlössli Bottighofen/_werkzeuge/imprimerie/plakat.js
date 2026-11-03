/* Die Hausdruckerei · Wirtschaft am Schlössli Bottighofen (Nachtbau 3.11.2026, Form der Plakatwerkstatt des Stammhauses): zwei Ansichten.
   1. «Motive vom See» (#msMotive): Hafen, Terrasse und See aus den Fotos des Hauses (motive.json), Filter nach Ort; jedes Motiv als Ansichtskarte
      mit Rückseite, «Als Postkarte öffnen» öffnet sie im Editor (Regel des Hauses: Ansichtskarten zeigen nur Hafen, Terrasse oder See).
   2. «Anlass anlegen» (#msAbend): Titel, Datum, Uhrzeit, ein Satz und das Foto → drei bis fünf fertige Drucksachen im Stil des Hauses (Aushang A4,
      Instagram-Beitrag, Story, Einladung, Tischkarte), sofort und ohne KI; eine wählen und im Editor fertig machen.
   Gesetzt wird mit den Aufbauten des Hauses (vorlagen.js, haeuser/schloessli/dokumente.js). Nur Lesen: Marke (DS.M), motive.json. */
(function () {
  const $ = s => document.querySelector(s);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const TAGE = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
  const MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  const PFEIL = '<svg viewBox="0 0 24 24"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>';
  let MOTIVE = [], filter = 'alle';

  /* nächste offene Tage: Donnerstag bis Montag, Dienstag und Mittwoch Ruhetag, nie in den Ferien des Hauses (haus.json › ferien_iso) */
  const FERIEN = [['2026-11-13', '2026-11-15'], ['2026-12-22', '2027-02-10']];
  const iso = d => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  function offeneTage(n) {
    const l = [], d = new Date(); d.setHours(12, 0, 0, 0); d.setDate(d.getDate() + 1);
    for (let k = 0; l.length < n && k < 400; k++, d.setDate(d.getDate() + 1)) {
      if (d.getDay() === 2 || d.getDay() === 3) continue;
      if (FERIEN.some(([a, b]) => iso(d) >= a && iso(d) <= b)) continue;
      l.push(new Date(d));
    }
    return l;
  }
  const lang = d => `${TAGE[d.getDay()]}, ${d.getDate()}. ${MONATE[d.getMonth()]} ${d.getFullYear()}`;

  /* Ansichtskarte als Drucksache: vorn das Motiv randlos mit Schild (Ort und Zeile), hinten der Kartengruss */
  function karteDoc(m, ton) {
    return DS.dokument(DS.M, { name: 'Postkarte · ' + m.titel, format: 'a6q', seiten: [
      { vorlage: 'ansicht', ton: ton || 'dunkel', inhalt: { bild: m.key, titel: m.ort, unter: m.ort === 'Bodensee' ? 'Wirtschaft am Schlössli · Bottighofen' : 'Wirtschaft am Schlössli · Am Hafen' } },
      { vorlage: 'kartengruss', ton: 'creme', inhalt: { titel: 'Grüsse vom See', text: 'Direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen.' } }] });
  }

  /* Anlass als Satz von Drucksachen: jede Seite ein eigenes Stück, Texte sind Ebenen im Editor */
  function anlassDocs(o, zahl) {
    const M = DS.M, d = o.datum, wann = lang(d) + (o.zeit ? ' · ' + o.zeit : ''), kurzD = `${d.getDate()}. ${MONATE[d.getMonth()]}`;
    const titel = o.titel, satz = o.satz || M.satz, bild = o.bild || 'start';
    const l = [
      { n: 'Aushang A4', format: 'a4h', vorlage: 'aushang', ton: 'dunkel', inhalt: { ueber: kurzD + (o.zeit ? ' · ' + o.zeit : ''), titel, text: satz, aktion: 'Reservation ' + M.tel } },
      { n: 'Instagram-Beitrag', format: 'insta', vorlage: 'buehne', ton: 'dunkel', inhalt: { bild, ueber: wann, titel, text: satz, aktion: M.web } },
      { n: 'Story', format: 'story', vorlage: 'fenster', ton: 'dunkel', inhalt: { bild, ueber: kurzD, titel, unter: o.zeit || 'Wirtschaft am Schlössli', text: satz } },
      { n: 'Einladung', format: 'q148', vorlage: 'einladung', ton: 'creme', inhalt: { ueber: 'Wirtschaft am Schlössli', titel, wann, wo: M.adr, text: satz, aktion: 'Antwort an ' + M.tel } },
      { n: 'Tischkarte', format: 'a7q', vorlage: 'deckel', ton: 'hell', inhalt: { ueber: kurzD, titel, unter: '', text: '' } },
    ];
    return l.slice(0, zahl).map(x => ({ x, doc: DS.dokument(M, { name: titel + ' · ' + x.n, format: x.format, seiten: [{ vorlage: x.vorlage, ton: x.ton, inhalt: x.inhalt }] }) }));
  }

  /* Grösse der Karten nach der Spaltenbreite */
  function fach(raster, n) {
    const w = raster.clientWidth || 900, breit = matchMedia('(min-width:700px)').matches;
    let sp = !breit ? 1 : n == 4 ? 2 : n == 5 ? 3 : (getComputedStyle(raster).gridTemplateColumns || '').split(' ').filter(Boolean).length || 3;
    const spalte = (w - (sp - 1) * 26) / sp;
    return Math.round(Math.max(230, Math.min(400, spalte / 1.5)));
  }
  const fachStil = g => `--vorn:${g}px;--hinten:${Math.round(g * .72)}px;height:${g + 40}px;max-width:${Math.round(g * 1.5)}px`;
  function karte(doc, titel, unter, knopf, extra, groesse, laden) {
    const k = document.createElement('div'); k.className = 'pk-karte';
    const box = groesse || 230, S = window.DSStudio;
    const b = document.createElement('div'); b.className = 'pk-blaetter';
    if (groesse) { b.classList.add('pk-blaetter--gross'); b.style.cssText = fachStil(groesse); }
    try {
      if (doc.seiten.length > 1) { const h = S.miniBox(doc, 1, box * (groesse ? .72 : .62), laden); h.classList.add('pk-hinten'); b.appendChild(h); }
      const v = S.miniBox(doc, 0, box, laden); v.classList.add('pk-vorn'); b.appendChild(v);
    } catch (e) { console.warn(e); }
    if (doc.seiten.length < 2) b.classList.add('pk-blaetter--eins');
    k.appendChild(b);
    k.insertAdjacentHTML('beforeend', `<div class="pk-text"><b>${esc(titel)}</b><small>${esc(unter)}</small>${extra || ''}</div>
      <button class="kn knopf--voll pk-los" type="button"><span>${esc(knopf)}</span><i>${PFEIL}</i></button>`);
    k.querySelector('.pk-los').addEventListener('click', () => { DSStudio.oeffne(doc); if (DSStart.offen()) DSStart.zu(); });
    return k;
  }

  /* ---------- 1 Motive vom See ---------- */
  function zeichneMotive() {
    const box = $('#pkMotive'); if (!box) return;
    const orte = [...new Set(MOTIVE.map(m => m.ort))];
    $('#pkFilter').innerHTML = `<div class="ms-chips pk-chips" data-pkf="ort"><span class="pk-chips__n">Ort</span><button data-w="alle" class="${filter === 'alle' ? 'an' : ''}">Alle</button>` +
      orte.map(w => `<button data-w="${esc(w)}" class="${filter === w ? 'an' : ''}">${esc(w)}</button>`).join('') + '</div>';
    const l = MOTIVE.filter(m => filter === 'alle' || m.ort === filter);
    box.innerHTML = '';
    $('#pkMotivZahl').textContent = `${l.length} von ${MOTIVE.length} Motiven`;
    l.forEach((m, i) => box.appendChild(karte(karteDoc(m, i % 3 === 2 ? 'hell' : 'dunkel'), m.titel, m.alt, 'Als Postkarte öffnen', '', 0, i < 6 ? { laden: 'eager', prio: 'high' } : { laden: 'lazy', prio: 'low' })));
  }

  /* ---------- 2 Anlass anlegen ---------- */
  function formular() {
    const f = $('#pkFreitag'); if (!f || f.options.length) return;
    offeneTage(40).forEach((d, i) => { const o = document.createElement('option'); o.value = iso(d); o.textContent = lang(d); if (!i) o.selected = true; f.appendChild(o); });
    const b = $('#pkBild');
    if (b && !b.options.length) (DS.M.bilder || []).filter(x => !/^(Eigene Fotos|Instagram des Hauses)$/.test(x.gruppe)).forEach(x => { const o = document.createElement('option'); o.value = x.key; o.textContent = x.alt; if (x.key === 'platanen') o.selected = true; b.appendChild(o); });
  }
  function vorschlagen(ev) {
    if (ev) ev.preventDefault();
    const titel = $('#pkThema').value.trim(), satz = $('#pkKonzept').value.trim(), zeit = $('#pkGast').value.trim();
    const zahl = +(document.querySelector('[data-pkzahl].an') || { dataset: { pkzahl: 4 } }).dataset.pkzahl;
    const datum = new Date($('#pkFreitag').value + 'T12:00:00'), bild = ($('#pkBild') || {}).value;
    const box = $('#pkVorschlaege');
    if (titel.length < 3) { $('#pkThema').focus(); box.innerHTML = '<p class="pk-leer">Bitte einen Titel für den Anlass eintragen, zum Beispiel «Four-Hands-Lunch».</p>'; return; }
    box.innerHTML = '';
    box.dataset.n = zahl;
    const gr = fach(box, zahl);
    anlassDocs({ titel, satz, zeit, datum, bild }, zahl).forEach(({ x, doc }) => box.appendChild(karte(doc, x.n, DS.FORMATE[x.format].name, 'Diese bearbeiten', '', gr)));
  }
  /* Beispiel unter dem Formular, solange nichts eingetragen ist: der nächste Anlass des Hauses (haus.json › anlaesse), damit die Ansicht nie leer ist */
  function beispiel() {
    const box = $('#pkVorschlaege'); if (!box || box.children.length) return;
    box.insertAdjacentHTML('beforeend', '<p class="pk-hinweis">So sieht ein Anlass aus: die Excellence Gourmetkreuzfahrt vom 13. bis 15. November 2026. Eigene Angaben oben eintragen und «Vorschläge anlegen».</p>');
    const r = document.createElement('div'); r.className = 'pk-raster'; r.dataset.n = 4; box.appendChild(r);
    const gr = fach(r, 4);
    anlassDocs({ titel: 'Four-Hands auf der Excellence Countess', satz: 'Monika Huber und Dieter Koschina kochen zusammen an Bord, von Basel nach Strassburg und zurück.', zeit: '15:00 Uhr', datum: new Date('2026-11-13T12:00:00'), bild: 'moni' }, 4)
      .forEach(({ x, doc }) => r.appendChild(karte(doc, x.n, DS.FORMATE[x.format].name, 'Diese bearbeiten', '', gr)));
  }

  function zeige(a) { if (a === 'motive') zeichneMotive(); if (a === 'abend') { formular(); beispiel(); } }
  async function los() {
    try { MOTIVE = await (await fetch(DS.M.basis + 'motive.json', { cache: 'no-cache' })).json(); } catch (e) { MOTIVE = []; }
    const z = $('#pkZahl'); if (z) z.textContent = MOTIVE.length;
    $('#pkFilter') && $('#pkFilter').addEventListener('click', e => { const b = e.target.closest('[data-w]'); if (!b) return; filter = b.dataset.w; zeichneMotive(); });
    $('#pkForm') && $('#pkForm').addEventListener('submit', vorschlagen);
    document.querySelectorAll('[data-pkzahl]').forEach(b => b.addEventListener('click', () => { document.querySelectorAll('[data-pkzahl]').forEach(x => x.classList.toggle('an', x === b)); }));
    formular();
  }
  window.DSPlakat = { zeige, karteDoc, anlassDocs, offeneTage, motive: () => MOTIVE };
  if (window.DS && DS.M && window.DSStudio) los(); else document.addEventListener('ds:bereit', los, { once: true });
})();
