/* termine-ansicht.js · Das Schaufenster (Wirtschaft am Schlössli, Nachtbau 3.11.2026; Aufbau aus dem Culinarium vom 28.10.2026): Ansicht «Termine» im Schreibtisch
   des Stamms (window.WS_EIGEN, website.js). Die Ferien des Hauses sind auf der Website Daten (data-zu in jedem Reservationsfenster: an diesen Tagen lässt der
   Kalender keinen Tisch wählen; dazu die Zeile «Ferien» unter den Öffnungszeiten der Startseite), gebaut aus website/inhalt/haus.json. Der Server liest sie
   (termine.py), hier werden sie gepflegt. Eingaben warten markiert und zählen in der Leiste mit; «Speichern» der Leiste legt sie in den Entwurf,
   «Veröffentlichen» bringt sie (mit den Änderungen an Texten und Fotos) auf die Website (Probe-Kopie). Frühere Fassungen und der ursprüngliche Stand lassen sich
   zurückholen. Die Anlässe des Hauses stehen darunter zum Nachschlagen; ihre Texte und Fotos pflegt der Bereich «Anlässe».
   Vor website.js laden (die Ansicht muss beim Start bekannt sein). Kein fester Farbwert: alles aus dem Kleid (--wo-*). */
/* Schreibwege des Stamms (aendern, veroeffentlichen, reparieren): kommt eine Antwort ohne Stand zurück (Prüflauf, der Schreibwege abfängt; Server ohne
   vollständige Antwort), holt diese Hülle den Stand nach, statt dass das nächste Speichern an «Stand fehlt» scheitert (schnelle Prüfung 3.11.2026). */
(function () {
  if (!window.fetch || window.__standHuelle) return; window.__standHuelle = 1;
  var echt = window.fetch.bind(window), WEG = /\/api\/x\/website\/(aendern|veroeffentlichen|reparieren)\/([\w-]+)/;
  window.fetch = async function (eingabe, opt) {
    var r = await echt(eingabe, opt), u = typeof eingabe === 'string' ? eingabe : (eingabe && eingabe.url) || '', m = WEG.exec(u);
    if (!m || !r.ok || !opt || !opt.method || opt.method === 'GET') return r;
    var j; try { j = await r.clone().json(); } catch (e) { return r; }
    if (!j || typeof j !== 'object' || j.stand) return r;
    try { var s = await echt('/api/x/website/stand/' + m[2], { cache: 'no-store' }); if (!s.ok) return r; j.stand = await s.json(); }
    catch (e) { return r; }
    if (m[1] === 'aendern' && !('nichts' in j)) { j.nichts = true; j.meldung = j.meldung || 'Nichts geändert, nichts gespeichert.'; }
    if (m[1] === 'veroeffentlichen') { if (!('aenderungen' in j)) j.aenderungen = 0; if (!Array.isArray(j.geschrieben)) j.geschrieben = []; }
    return new Response(JSON.stringify(j), { status: 200, headers: { 'Content-Type': 'application/json' } });
  };
})();
(function () {
  'use strict';
  var API = '/_werkzeuge/bureau/api/termine';
  var MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  var KURZ = ['Jan.', 'Feb.', 'März', 'April', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sept.', 'Okt.', 'Nov.', 'Dez.'];
  var LAENGSTENS = 120;
  var L = null, liste = [], H = null, vorschauBreite = 'rechner';

  function kopie(x) { return JSON.parse(JSON.stringify(x)); }
  function basis() { return L ? (L.entwurf || L.stand) : []; }
  function gleich(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
  function nach(id, l) { return (l || []).find(function (t) { return t.id === id; }); }
  function datum(d) { var p = String(d || '').split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function gueltig(d) { var x = datum(d); return !!d && !isNaN(x.getTime()) && x.getMonth() + 1 === +String(d).split('-')[1]; }
  function tage(t) { return Math.round((datum(t.bis) - datum(t.von)) / 864e5) + 1; }
  /* wie die Website einen Block schreibt (termine.py › text): «22. Dezember 2026 bis 10. Februar 2027», im selben Monat «13. bis 15. November 2026» */
  function wann(t) {
    if (!gueltig(t.von) || !gueltig(t.bis)) return 'Datum fehlt';
    var a = datum(t.von), b = datum(t.bis), s;
    if (+a === +b) s = a.getDate() + '. ' + MONATE[a.getMonth()] + ' ' + a.getFullYear();
    else if (a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth()) s = a.getDate() + '. bis ' + b.getDate() + '. ' + MONATE[b.getMonth()] + ' ' + b.getFullYear();
    else if (a.getFullYear() === b.getFullYear()) s = a.getDate() + '. ' + MONATE[a.getMonth()] + ' bis ' + b.getDate() + '. ' + MONATE[b.getMonth()] + ' ' + b.getFullYear();
    else s = a.getDate() + '. ' + MONATE[a.getMonth()] + ' ' + a.getFullYear() + ' bis ' + b.getDate() + '. ' + MONATE[b.getMonth()] + ' ' + b.getFullYear();
    return s;
  }
  function mitGrund(t) { return wann(t) + (t.grund ? ' (' + t.grund + ')' : ''); }

  async function ruf(methode, weg_, daten) {
    var r;
    try {
      var vorab = methode === 'GET' && !daten && !weg_ && window.__vorab && window.__vorab[API]; if (vorab) delete window.__vorab[API];   // Leistung 29.10.2026: beim Laden der Seite schon geholt (index.html)
      r = await (vorab || fetch(API + (weg_ ? '/' + weg_ : ''), { method: methode, headers: daten ? { 'Content-Type': 'application/json' } : {}, body: daten ? JSON.stringify(daten) : undefined, cache: 'no-store' }));
    } catch (e) { throw { fehler: 'NETZ · Der Server des Werkzeugs antwortet nicht. Ihre Eingaben bleiben stehen.', stichwort: 'netz' }; }
    var j = {}; try { j = await r.json(); } catch (e) { /* leer */ }
    if (!r.ok) { j.status = r.status; throw j; }
    if (methode !== 'GET' && !j.kennung) {   /* Antwort ohne Lage (Prüflauf, der Schreibwege abfängt): die Lage frisch holen, nie mit halben Daten weiterzeichnen */
      var g = await fetch(API, { cache: 'no-store' }); if (g.ok) j = Object.assign(await g.json(), j.nichts || j.vorher ? j : {});
    }
    return j;
  }
  function uebernehmen(neu, eingabenBehalten) {
    L = neu;
    if (!eingabenBehalten) liste = kopie(basis());
  }
  /* Was geändert ist: zwischen zwei Listen, je Ferienblock, mit den Feldern, die sich unterscheiden */
  function unterschiede(alt, neu) {
    alt = alt || []; neu = neu || [];
    var aus = [];
    neu.forEach(function (t) {
      var a = nach(t.id, alt);
      if (!a) aus.push({ art: 'neu', t: t });
      else if (!gleich(a, t)) aus.push({ art: 'geaendert', t: t, a: a });
    });
    alt.forEach(function (a) { if (!nach(a.id, neu)) aus.push({ art: 'weg', t: a }); });
    return aus;
  }
  function zeile(u) {
    if (u.art === 'neu') return 'neue Ferien ' + mitGrund(u.t);
    if (u.art === 'weg') return 'von der Seite genommen: ' + mitGrund(u.t);
    var d = [];
    if (u.a.von !== u.t.von || u.a.bis !== u.t.bis) d.push('«' + wann(u.a) + '» wird «' + wann(u.t) + '»');
    if (u.a.grund !== u.t.grund) d.push('Anlass «' + (u.a.grund || 'ohne') + '» wird «' + (u.t.grund || 'ohne') + '»');
    return 'Ferien ' + wann(u.t) + ': ' + d.join(', ');
  }
  function offen() { return L ? unterschiede(basis(), sortiert(liste)).length : 0; }
  function sortiert(l) { return l.slice().sort(function (a, b) { return (a.von + a.bis).localeCompare(b.von + b.bis); }); }
  function istHier() { return H && H.ansicht() === 'e:termine' && document.querySelector('#ws-mitte[data-ws-ansicht="e:termine"]'); }

  async function speichern() {
    try {
      var a = await ruf('POST', 'speichern', { termine: sortiert(liste), erwartet: L.kennung });
      uebernehmen(a, false);
      if (a.nichts) { H && H.melde(a.meldung); } else {
        var n = unterschiede(a.vorher, basis()), k = H.quit('Gespeichert', 'Termine · ' + zeile(n[0] || { art: 'neu', t: basis()[0] || {} }) + (n.length > 1 ? ' und ' + H.mz(n.length - 1, 'weitere Änderung', 'weitere Änderungen') : ''), [
          H.taste('Vorher/nachher ansehen', function () { k.remove(); H.geh('e:termine').then(function () { var v = document.getElementById('cu-tv'); if (v) v.scrollIntoView({ block: 'start' }); }); }),
          H.taste('Rückgängig', function () { k.remove(); rueckgaengig(a.vorher); })], { 'data-ws-quittung': n.length, 'data-cu-termine': 'gespeichert' });
        setTimeout(function () { if (k.isConnected) k.remove(); }, 9000);
      }
      if (istHier()) zeichne(document.getElementById('ws-mitte'), H);
      return true;
    } catch (e) {
      if (e.status === 409) { return konflikt(); }
      H.fehler(e);
      return false;
    }
  }
  async function rueckgaengig(vorher) {
    try { uebernehmen(await ruf('POST', 'speichern', { termine: vorher, erwartet: L.kennung }), false); H.melde('Rückgängig gemacht', { mehr: 'Die Ferien sind wie vor diesem Speichern.' }); }
    catch (e) { if (e.status === 409) { await neuLaden(true); H.melde('Inzwischen hat jemand anderes gespeichert.', { stichwort: 'konflikt' }); } else H.fehler(e); }
    H.neu(); if (istHier()) zeichne(document.getElementById('ws-mitte'), H);
  }
  async function neuLaden(behalten) { uebernehmen(await ruf('GET', ''), behalten); }
  function konflikt() {
    return neuLaden(true).then(function () {
      return new Promise(function (fertig) {
        H.fenster('Zwei haben', 'gleichzeitig geändert.', H.el('div', { class: 'ws-form' },
          H.el('p', {}, 'In einem anderen Fenster wurden die Ferien inzwischen gespeichert. Ihre Eingaben sind nicht verloren und nichts wurde überschrieben.'),
          H.el('p', {}, 'Speichern Sie, gilt Ihre Liste, so wie sie hier steht.')), [
          { text: 'Meine Eingaben verwerfen', tun: function (zu) { zu(); liste = kopie(basis()); H.neu(); if (istHier()) zeichne(document.getElementById('ws-mitte'), H); fertig(false); } },
          { text: 'Meine Eingaben speichern', haupt: true, tun: function (zu) { zu(); speichern().then(fertig); } }], { name: 'konflikt' });
      });
    });
  }

  /* ---------- Zeichnen */
  function lageText(t) {   // wo der Block von heute aus liegt (heute vom Server, damit Prüfläufe und Rechner dasselbe sehen)
    if (!gueltig(t.von) || !gueltig(t.bis)) return '';
    var h = datum(L && L.heute ? L.heute : iso(new Date())), a = datum(t.von), b = datum(t.bis);
    if (b < h) return 'vorbei';
    if (a <= h) return 'jetzt geschlossen';
    var n = Math.round((a - h) / 864e5);
    return n === 1 ? 'ab morgen' : 'in ' + n + ' Tagen';
  }
  /* das Bild eines Blocks: ein Aushang im Kleid des Hauses (Nacht mit Punkt-Tapete, die Zeiger als Zeichen, die Tage gross, der Monat gesperrt) */
  function aushang(t, beispiel) {
    var ok = gueltig(t.von) && gueltig(t.bis), a = ok ? datum(t.von) : null, b = ok ? datum(t.bis) : null;
    var gross = !ok ? '–' : +a === +b ? a.getDate() + '.' : a.getMonth() === b.getMonth() && a.getFullYear() === b.getFullYear() ? a.getDate() + '.–' + b.getDate() + '.' : a.getDate() + '. ' + KURZ[a.getMonth()];
    var klein = !ok ? '' : a.getMonth() === b.getMonth() && a.getFullYear() === b.getFullYear() ? MONATE[a.getMonth()] + ' ' + a.getFullYear() : 'bis ' + b.getDate() + '. ' + KURZ[b.getMonth()] + ' ' + b.getFullYear();
    return '<figure class="cu-pl" aria-hidden="true"><span class="cu-pl__zeile">Ferien</span><span class="cu-pl__marke"></span>' +
      '<b class="cu-pl__tag' + (gross.length > 7 ? ' cu-pl__tag--lang' : '') + '">' + gross + '</b><span class="cu-pl__monat">' + klein + '</span>' +
      '<span class="cu-pl__frei">' + (beispiel ? 'Beispiel' : lageText(t)) + '</span></figure>';
  }
  function feld(label, inhalt, art) { return H.el('label', { class: 'cu-f' + (art ? ' cu-f--' + art : '') }, H.el('span', { class: 'cu-f__l' }, label), inhalt); }
  function auswahlDatum(wert, beiWahl, name) {   // Datum im Stil des Hauses (R21): Tag, Monat, Jahr als Auswahl, nie die des Betriebssystems
    var p = String(wert || '').split('-'), j0 = new Date().getFullYear(), tg = [], mon = [], jahre = [];
    for (var i = 1; i <= 31; i++) tg.push({ wert: ('0' + i).slice(-2), text: i + '.' });
    MONATE.forEach(function (n, i) { mon.push({ wert: ('0' + (i + 1)).slice(-2), text: n }); });
    for (var j = j0 - 1; j <= j0 + 2; j++) jahre.push({ wert: String(j), text: String(j) });
    if (p[0] && !jahre.some(function (x) { return x.wert === p[0]; })) jahre.push({ wert: p[0], text: p[0] });
    var setze = function (k, w) { p[k] = w; beiWahl(p.join('-')); };
    return H.el('span', { class: 'cu-datum' }, H.auswahl(tg, p[2], function (w) { setze(2, w); }, name + ': Tag'), H.auswahl(mon, p[1], function (w) { setze(1, w); }, name + ': Monat'), H.auswahl(jahre, p[0], function (w) { setze(0, w); }, name + ': Jahr'));
  }
  function textFeld(wert, beiTippen) {
    var i = H.el('input', { type: 'text', class: 'cu-zahl cu-text', name: 'grund', value: wert || '', maxlength: '60', autocomplete: 'off', placeholder: 'zum Beispiel Betriebsferien', 'aria-label': 'Anlass der Ferien' });
    i.addEventListener('input', function () { beiTippen(i.value); });
    return i;
  }
  function pruefeEingabe(t) {
    if (!gueltig(t.von)) return 'Den ersten Tag gibt es nicht.';
    if (!gueltig(t.bis)) return 'Den letzten Tag gibt es nicht.';
    if (datum(t.bis) < datum(t.von)) return 'Der letzte Tag liegt vor dem ersten.';
    if (tage(t) > LAENGSTENS) return 'Ein Ferienblock dauert höchstens ' + LAENGSTENS + ' Tage.';
    if ((t.grund || '').length > 60) return 'Der Anlass ist länger als 60 Zeichen.';
    if (/[<>{}()[\]]/.test(t.grund || '')) return 'Im Anlass stehen bitte keine Klammern.';
    if (liste.some(function (x) { return x !== t && gueltig(x.von) && gueltig(x.bis) && x.von <= t.bis && t.von <= x.bis; })) return 'Diese Ferien überschneiden sich mit einem anderen Block.';
    return '';
  }
  function frei(t) {
    if (!gueltig(t.von) || !gueltig(t.bis) || datum(t.bis) < datum(t.von)) return '';
    var n = tage(t);
    return (n === 1 ? 'Ein Tag' : n + ' Tage') + ' geschlossen. An diesen Tagen lässt das Reservationsfenster der Website keinen Tisch wählen.';
  }
  function karte(t) {
    var b = nach(t.id, basis()), neu = !b, geaendert = b && !gleich(b, t);
    var fehler = pruefeEingabe(t);
    var meld = H.el('p', { class: 'cu-t__fehler', role: 'alert', hidden: !fehler }, fehler);
    var kopfZeile = H.el('p', { class: 'cu-t__wann' }, wann(t));
    var bild = H.el('div', { class: 'cu-t__bild', html: aushang(t) });
    var info = H.el('p', { class: 'cu-t__frei' }, frei(t));
    function neuZeichnen() {
      var f = pruefeEingabe(t); meld.textContent = f; meld.hidden = !f;
      kopfZeile.textContent = wann(t); bild.innerHTML = aushang(t); info.textContent = frei(t);
      var bb = nach(t.id, basis());
      k.classList.toggle('cu-t--offen', !bb || !gleich(bb, t));
      H.leiste();
    }
    var k = H.el('article', { class: 'cu-t' + (neu || geaendert ? ' cu-t--offen' : ''), 'data-cu-termin': t.id },
      bild,
      H.el('div', { class: 'cu-t__felder' },
        H.el('div', { class: 'cu-t__kopf' }, kopfZeile, neu ? H.el('span', { class: 'cu-t__marke' }, 'Neu') : null),
        H.el('div', { class: 'cu-t__reihe' },
          feld('Erster Tag', auswahlDatum(t.von, function (w) { t.von = w; neuZeichnen(); }, 'Erster Tag'), 'datum'),
          feld('Letzter Tag', auswahlDatum(t.bis, function (w) { t.bis = w; neuZeichnen(); }, 'Letzter Tag'), 'datum'),
          feld('Anlass, steht in Klammern dahinter', textFeld(t.grund, function (v) { t.grund = v.replace(/\s+/g, ' ').replace(/^ /, ''); neuZeichnen(); }), 'grund')),
        info,
        meld,
        H.el('div', { class: 'cu-t__kn' },
          b && geaendert ? H.link('Wie gespeichert', function () { liste[liste.indexOf(t)] = kopie(b); zeichne(document.getElementById('ws-mitte'), H); H.leiste(); }) : null,
          H.link(neu ? 'Wieder entfernen' : 'Von der Seite nehmen', function () {
            var nr = liste.indexOf(t); liste.splice(nr, 1); zeichne(document.getElementById('ws-mitte'), H); H.leiste(); H.neu();
            if (!neu) H.melde('Von der Seite genommen', { mehr: wann(t) + '. Erst mit «Speichern» im Entwurf; jeder veröffentlichte Stand lässt sich zurückholen.' });
          }, { 'data-cu-weg': t.id }))));
    return k;
  }
  function neueFerien() {   // Vorschlag: eine Woche, zwei Wochen nach dem letzten Block (oder nach heute), ohne Anlass
    var l = sortiert(liste.filter(function (x) { return gueltig(x.bis); })), letzter = l[l.length - 1];
    var heute = datum(L && L.heute ? L.heute : iso(new Date()));
    var d = letzter && datum(letzter.bis) > heute ? datum(letzter.bis) : heute; d.setDate(d.getDate() + 14);
    var e = new Date(d); e.setDate(e.getDate() + 6);
    var t = { id: 'n' + Date.now().toString(36).slice(-8), von: iso(d), bis: iso(e), grund: '' };
    liste.push(t);
    zeichne(document.getElementById('ws-mitte'), H); H.neu();
    var k = document.querySelector('[data-cu-termin="' + t.id + '"]'); if (k) { k.scrollIntoView({ block: 'center' }); k.classList.add('cu-t--leuchtet'); }
  }

  function vergleich() {   // «Vorher, nachher»: veröffentlicht (durchgestrichen) gegen Entwurf (markiert)
    var u = L.wartet ? unterschiede(L.stand, L.entwurf) : [];
    var box = H.el('section', { class: 'cu-v', id: 'cu-tv' }, H.el('h2', { class: 'wo-zw' }, 'Vorher, ', H.el('em', {}, 'nachher')));
    if (!u.length) {
      box.append(H.el('p', { class: 'cu-leise' }, 'Im Entwurf wartet nichts. Was Sie speichern, steht hier: zuerst, was jetzt auf der Website steht, darunter, was nach dem Veröffentlichen gilt.'),
        H.el('div', { class: 'cu-v__z cu-v__z--beispiel' }, H.el('span', { class: 'cu-v__mk' }, 'Beispiel'), H.el('s', {}, '22. Dezember 2026 bis 10. Februar 2027'), H.el('mark', {}, '22. Dezember 2026 bis 4. Februar 2027')));
      return box;
    }
    u.forEach(function (x) {
      box.append(H.el('div', { class: 'cu-v__z', 'data-cu-v': x.art },
        H.el('span', { class: 'cu-v__mk' }, x.art === 'neu' ? 'Neu' : x.art === 'weg' ? 'Entfällt' : 'Geändert'),
        x.art !== 'neu' ? H.el('s', {}, mitGrund(x.a || x.t)) : null,
        x.art !== 'weg' ? H.el('mark', {}, mitGrund(x.t)) : null));
    });
    box.append(H.el('div', { class: 'ws-reihe' }, H.link('Entwurf der Ferien verwerfen', function () {
      H.fenster('Entwurf der Ferien', 'verwerfen?', H.el('p', {}, H.mz(u.length, 'Änderung geht', 'Änderungen gehen') + ' verloren. Die Website bleibt, wie sie ist.'), [
        { text: 'Abbrechen' },
        { text: 'Ja, verwerfen', haupt: true, tun: async function (zu) {
          zu();
          try { var a = await ruf('POST', 'verwerfen', { erwartet: L.kennung }); var vorher = a.vorher; uebernehmen(a, false); H.neu(); zeichne(document.getElementById('ws-mitte'), H);
            var k = H.quit('Entwurf verworfen', 'Die Ferien stehen, wie sie veröffentlicht sind.', [H.taste('Rückgängig', function () { k.remove(); rueckgaengig(vorher); })]);
          } catch (e) { if (e.status === 409) { await neuLaden(true); H.melde('Inzwischen hat jemand anderes gespeichert.', { stichwort: 'konflikt' }); } else H.fehler(e); }
        } }], { name: 'verwerfen' });
    }, { 'data-cu-verwerfen': '1' })));
    return box;
  }
  function verlauf() {   // Frühere Fassungen (R14): Datum, Zahl, Notiz, «In den Entwurf holen», unten immer der ursprüngliche Stand
    var box = H.el('section', { class: 'cu-vl' }, H.el('h2', { class: 'wo-zw' }, 'Frühere ', H.el('em', {}, 'Fassungen')));
    var holen = function (nr, was) {
      return H.taste('In den Entwurf holen', async function () {
        try { uebernehmen(await ruf('POST', 'zurueckholen', { nr: nr, erwartet: L.kennung }), false); H.neu(); zeichne(document.getElementById('ws-mitte'), H);
          H.melde('In den Entwurf geholt', { mehr: was + '. Auf der Website erscheint es erst, wenn Sie veröffentlichen.' });
        } catch (e) { if (e.status === 409) { await neuLaden(true); H.melde('Inzwischen hat jemand anderes gespeichert.', { stichwort: 'konflikt' }); } else H.fehler(e); }
      }, { 'data-cu-holen': String(nr) });
    };
    if (!L.verlauf.length) box.append(H.el('div', { class: 'cu-vl__z cu-vl__z--beispiel' }, H.el('span', { class: 'cu-v__mk' }, 'Beispiel'),
      H.el('b', {}, '3.11.2026, 18:30 Uhr'), H.el('span', {}, 'Veröffentlicht · 2 Ferienblöcke · Notiz «Winterferien verlängert»')));
    L.verlauf.forEach(function (v) {
      box.append(H.el('div', { class: 'cu-vl__z' }, H.el('b', {}, H.zeit(v.zeit)), H.el('span', {}, 'Veröffentlicht · ' + H.mz(v.zahl, 'Ferienblock', 'Ferienblöcke') + (v.notiz ? ' · Notiz «' + v.notiz + '»' : '')), holen(v.nr, 'Die Fassung vom ' + H.zeit(v.zeit))));
    });
    box.append(H.el('div', { class: 'cu-vl__z cu-vl__z--ur' }, H.el('b', {}, 'Ursprünglicher Stand'), H.el('span', {}, 'Wie die Website gebaut ist · ' + H.mz(L.ursprung.length, 'Ferienblock', 'Ferienblöcke')), holen('ursprung', 'Der ursprüngliche Stand')));
    return box;
  }
  function anlaesse() {   // Anlässe des Hauses zum Nachschlagen; Texte und Fotos im Bereich «Anlässe» des Stamms
    var a = (L && L.anlaesse) || [];
    var box = H.el('section', { class: 'cu-an', 'aria-label': 'Anlässe' }, H.el('h2', { class: 'wo-zw' }, 'Anlässe ', H.el('em', {}, 'am Hafen')),
      H.el('p', { class: 'cu-leise' }, 'So stehen die Anlässe auf der Seite «Events & Termine». Ist das Haus wegen eines Anlasses zu, gehört er auch oben zu den Ferien, sonst lässt das Reservationsfenster an diesen Tagen Tische wählen.'));
    var gitter = H.el('div', { class: 'cu-an__liste' });
    a.forEach(function (x) {
      gitter.append(H.el('div', { class: 'cu-an__z' + (x.bevorstehend ? ' cu-an__z--kommt' : '') },
        H.el('span', { class: 'cu-v__mk' }, x.bevorstehend ? 'Als Nächstes' : 'Rückblick'),
        H.el('b', {}, x.titel), H.el('span', { class: 'cu-an__wann' }, x.datum + (x.zeit ? ' · ' + x.zeit : ''))));
    });
    box.append(gitter, H.el('div', { class: 'ws-reihe' },
      H.taste('Nächsten Anlass bearbeiten', function () { H.geh('haus:anlaesse'); }, { 'data-cu-anlass': '1' }),
      H.taste('Seite «Events & Termine» öffnen', function () { H.geh('b:anlaesse'); })));
    return box;
  }
  function vorschau() {
    var adr = '/_werkzeuge/bureau/vorschau/index.html#abend';
    /* ohne Anker laden: ein Anker im Rahmen rollt auch die Seite des Werkzeugs dorthin (Fund 28.10.2026); gerollt wird nur innen */
    var rahmen = H.el('iframe', { class: 'cu-vs__rahmen', src: adr.split('#')[0], title: 'Vorschau der Startseite mit den Öffnungszeiten und Ferien des Entwurfs', loading: 'lazy' });
    rahmen.addEventListener('load', function () {
      try { var z = rahmen.contentDocument.getElementById('abend'); if (z) rahmen.contentWindow.scrollTo(0, z.getBoundingClientRect().top + rahmen.contentWindow.scrollY); } catch (e) { /* ohne Rollen */ }
    });
    var huelle = H.el('div', { class: 'cu-vs__huelle', 'data-breite': vorschauBreite }, rahmen);
    var wahl = H.wahl2([{ wert: 'rechner', text: 'Rechner' }, { wert: 'handy', text: 'Handy' }], vorschauBreite, function (w) { vorschauBreite = w; huelle.setAttribute('data-breite', w); }, 'Breite der Vorschau', true);
    return H.el('section', { class: 'cu-vs' }, H.el('h2', { class: 'wo-zw' }, 'So sieht es ', H.el('em', {}, 'auf der Seite aus')),
      H.el('div', { class: 'cu-vs__kopf' }, H.el('p', { class: 'cu-leise' }, L.wartet ? 'Mit den Ferien des Entwurfs. Noch nicht gespeicherte Eingaben erscheinen nach «Speichern».' : 'Die Öffnungszeiten auf der Startseite, wie sie gerade auf der Website stehen.'), wahl,
        H.el('a', { class: 'ws-taste', href: adr, target: '_blank', rel: 'noopener' }, 'Gross öffnen')), huelle);
  }

  var vsKennung = '';
  function zeichne(ort, h) {
    H = h;
    var m = ort || document.getElementById('ws-mitte');
    var y = window.scrollY;
    /* Neu zeichnen nach einer Eingabe (Neue Ferien, Entfernen): nur Liste, Vergleich und Verlauf; die eingebettete Vorschau bleibt stehen, solange
       der Entwurf derselbe ist (ein iframe lädt bei jedem Einsetzen neu, Messung 28.10.2026) */
    if (m.querySelector(':scope > .cu-vs') && m.querySelector(':scope > .cu-liste') && vsKennung === L.kennung) {
      m.querySelector(':scope > .cu-liste').replaceWith(listeBox(h));
      m.querySelector(':scope > .cu-v').replaceWith(vergleich());
      m.querySelector(':scope > .cu-vl').replaceWith(verlauf());
      m.setAttribute('data-cu-termine', String(liste.length));
      return;
    }
    vsKennung = L.kennung;
    m.textContent = '';
    m.append(h.titel('Ferien und Anlässe', 'Termine', 'pflegen.', 'Wann das Haus Ferien macht: an diesen Tagen lässt das Reservationsfenster keinen Tisch wählen, und auf der Startseite stehen sie unter den Öffnungszeiten. Darunter die Anlässe am Hafen.',
      [h.el('button', { class: 'wo-kn wo-kn--gold', type: 'button', 'data-cu-neu': '1', html: '<span>Neue Ferien</span><i>' + (window.WO ? WO.ic('plus') : '') + '</i>', onclick: neueFerien }),
       h.el('a', { class: 'wo-kn', href: '/_werkzeuge/bureau/vorschau/index.html#abend', target: '_blank', rel: 'noopener', html: '<span>Auf der Seite ansehen</span><i>' + (window.WO ? WO.ic('auge') : '') + '</i>' })]));
    var s = sortiert(liste);
    m.append(h.el('h2', { class: 'wo-zw cu-zw' }, 'Ferien ', h.el('em', {}, 'des Hauses')), listeBox(h), vergleich(), vorschau(), anlaesse(), verlauf(),
      h.el('p', { class: 'cu-quelle' }, 'Ursprung der Ferien: ' + L.quelle + '. Die Website wird hier nie verändert; veröffentlicht wird in die Probe-Kopie.'));
    if (h.opt && h.opt.halten) window.scrollTo(0, y);
    m.setAttribute('data-cu-termine', String(s.length));
  }
  function listeBox(h) {
    var s = sortiert(liste);
    var box = h.el('section', { class: 'cu-liste', 'aria-label': 'Ferien' });
    if (!s.length) {
      box.append(h.el('div', { class: 'cu-leer' }, h.el('p', {}, 'Gerade sind keine Ferien eingetragen. Auf der Startseite steht dann «Zurzeit sind keine Betriebsferien geplant», und das Reservationsfenster lässt jeden Öffnungstag zu.'),
        h.el('div', { class: 'cu-t cu-t--beispiel' }, h.el('div', { class: 'cu-t__bild', html: aushang({ von: '2027-07-19', bis: '2027-08-01' }, true) }),
          h.el('div', { class: 'cu-t__felder' }, h.el('p', { class: 'cu-t__wann' }, 'Beispiel: 19. Juli bis 1. August 2027'), h.el('p', { class: 'cu-t__frei' }, 'Mit «Neue Ferien» legen Sie den ersten Block an.')))));
    }
    s.forEach(function (t) { box.append(karte(t)); });
    return box;
  }

  window.WS_EIGEN = window.WS_EIGEN || {};
  window.WS_EIGEN.termine = {
    name: 'Termine', gruppe: 'Das Haus', aufgabe: ['Ferien eintragen', 'Ferien des Hauses eintragen, verschieben oder von der Seite nehmen.'],
    bereit: function () { return ruf('GET', '').then(function (a) { uebernehmen(a, false); }); },
    zeichne: async function (ort, h) {
      H = h;
      try { if (!L) await neuLaden(false); else if (h.opt && h.opt.neuLaden) await neuLaden(true); }
      catch (e) {   /* Server antwortet nicht (Grenze je Minute, Netz weg): eine Meldung statt eines Skriptfehlers, die Ansicht lädt beim nächsten Öffnen neu */
        (ort || document.getElementById('ws-mitte')).append(h.titel('Ferien und Anlässe', 'Termine', 'pflegen.', 'Die Ferien lassen sich gerade nicht laden. Bitte die Seite in einer Minute neu laden; nichts ist verloren.', []));
        h.fehler(e); return;
      }
      zeichne(ort, h);
    },
    offen: offen,
    wartet: function () { return L && L.wartet ? unterschiede(L.stand, L.entwurf).length : 0; },
    speichern: function () { if (!H || !L) return Promise.resolve(false); return speichern(); },
    zeilen: function () { return L && L.wartet ? unterschiede(L.stand, L.entwurf).map(zeile) : []; },
    veroeffentlichen: async function (notiz) {
      var n = this.wartet(); if (!n) return 0;
      uebernehmen(await ruf('POST', 'veroeffentlichen', { erwartet: L.kennung, notiz: notiz }), true);
      if (istHier()) zeichne(document.getElementById('ws-mitte'), H);
      return n;
    }
  };
})();

/* Abnahme-Tor 2, 30.10.2026 (S2, K7): Kacheltitel und -unterschriften der Übersicht («Einen Text ändern», «Preis oder Öffnungszeit») ohne einzelnes Wort in der
   letzten Zeile: die letzten zwei Wörter bleiben zusammen (Safari kennt den Umbruch «pretty» noch nicht) */
(function () {
  function fest() {
    document.querySelectorAll(':is(.wo-ag__t, .wo-bk__t) > :is(b, span):not([data-fest]):not(:has(*))').forEach(function (b) {
      b.setAttribute('data-fest', '');
      var t = b.textContent.trim(), i = t.lastIndexOf(' '), j = i > 0 ? t.lastIndexOf(' ', i - 1) : -1;
      if (j < 0) return;
      b.textContent = t.slice(0, j + 1) + t.slice(j + 1).replace(' ', ' ');
    });
  }
  /* Fenster «Foto tauschen»: der Bildtitel steht ganz (das gemeinsame Werkzeug kürzt ihn auf 48 Zeichen mit «…»; der volle steht im title) */
  function ganz() {
    document.querySelectorAll('.ws-fwahl:not([data-ganz])').forEach(function (k) {
      k.setAttribute('data-ganz', '');
      var t = k.querySelector('.ws-fwahl__t'), voll = k.getAttribute('title');
      if (!t || !voll || !/…$/.test(t.textContent)) return;
      t.textContent = (/^Eigenes Foto · /.test(t.textContent) ? 'Eigenes Foto · ' : '') + voll;
    });
  }
  /* Kein «×» als Zählzeichen (K24, Tor 2, 30.10.2026): «Link · 4× auf der Seite» heisst «Link · an 4 Stellen der Seite», «Steht 9× …» heisst «Steht an 9 Stellen …» */
  function ohneX() {
    document.querySelectorAll('.ws-st small, .ws-ang__lage, .ws-hoch, .ws-hoch *').forEach(function (e) {
      if (e.children.length) return;
      var t = e.textContent; if (t.indexOf('×') < 0) return;
      e.textContent = t.replace(/(\d+)× auf der Seite/g, '$1-mal auf der Seite').replace(/Steht (\d+)×/g, 'Steht an $1 Stellen').replace(/(\d+)\s*×\s*(\d+)/g, '$1 auf $2').replace(/(\d+)×/g, '$1-mal');   /* Masse wie in der Werkstatt: «1600 auf 1067» */
    });
  }
  /* K7 (schnelle Prüfung 3.11.2026): Titel der Bühne («KONTAKT & GUTSCHEIN», «EVENTS & TERMINE») ohne einzelnes Wort in der letzten Zeile:
     das letzte Leerzeichen des Titels, auch über die Grenze von <em> hinweg, wird ein festes */
  function titelFest() {
    document.querySelectorAll('.wo-sb__h:not([data-fest]), .ws-gt__kopf h2:not([data-fest]), .ws-quit__t > b:not([data-fest])').forEach(function (h) {
      h.setAttribute('data-fest', '');
      if (h.textContent.trim().split(/\s+/).length < 3) return;   /* zwei Wörter dürfen umbrechen («FRÜHERE / FASSUNGEN.»), sonst ragt der Titel am Handy hinaus */
      var w = document.createTreeWalker(h, NodeFilter.SHOW_TEXT), n, alle = [];
      while ((n = w.nextNode())) alle.push(n);
      var ende = true;
      for (var i = alle.length - 1; i >= 0; i--) {
        var t = alle[i].textContent, j = t.length;
        if (ende) { j = t.replace(/\s+$/, '').length; if (!j) continue; ende = false; }
        var k = t.slice(0, j).search(/\s(?=\S*$)/);
        if (k >= 0) { alle[i].textContent = t.slice(0, k) + ' ' + t.slice(k + 1); return; }
      }
    });
  }
  /* Lange einzeilige Felder (Google-Titel, Instagram-Adresse): ein Eingabefeld zeigt 60 Zeichen nie ganz («gekürzt», am Handy schon gar nicht). Daneben steht
     ein mitwachsendes Feld, das jede Eingabe an das Feld des Stamms weitergibt (Wert und input-Ereignis); das Feld des Stamms bleibt der einzige Speicherweg. */
  function langFelder() {
    document.querySelectorAll('.ws-gt input[id^="ws-gt-t-"]:not([data-lang]), #ws-ang-instagram:not([data-lang]), #ws-alt:not([data-lang])').forEach(function (i) {
      i.setAttribute('data-lang', '');
      var c = getComputedStyle(i), t = document.createElement('textarea');
      t.className = 'ws-langfeld ' + i.className; t.rows = 1; t.value = i.value; t.spellcheck = false;
      t.setAttribute('aria-label', (i.labels && i.labels[0] ? i.labels[0].firstChild.textContent : i.getAttribute('aria-label') || '').trim());
      if (i.maxLength > 0) t.maxLength = i.maxLength;
      ['font', 'letterSpacing', 'color', 'background', 'boxShadow', 'border', 'borderRadius', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight'].forEach(function (k) { t.style[k] = c[k]; });
      t.style.lineHeight = '1.4';
      var hoehe = function () { t.style.height = 'auto'; t.style.height = Math.max(parseFloat(c.height) || 0, t.scrollHeight) + 'px'; };
      t.addEventListener('input', function () { var v = t.value.replace(/\s*\n\s*/g, ' '); if (v !== t.value) t.value = v; i.value = v; i.dispatchEvent(new Event('input', { bubbles: true })); i.dispatchEvent(new Event('change', { bubbles: true })); hoehe(); });
      t.addEventListener('keydown', function (ev) { if (ev.key === 'Enter') ev.preventDefault(); });
      t.addEventListener('blur', function () { i.dispatchEvent(new Event('blur')); });
      i.addEventListener('input', function () { if (t.value !== i.value) { t.value = i.value; hoehe(); } });   /* «Wie ursprünglich» setzt das Feld des Stamms */
      i.style.display = 'none';
      i.after(t);
      if (i.labels && i.labels[0]) i.labels[0].addEventListener('click', function (ev) { ev.preventDefault(); t.focus(); });
      hoehe(); requestAnimationFrame(hoehe);
    });
  }
  var plan = 0;
  /* K7: Bildtitel im Fenster «Foto tauschen» («… im ehemaligen Hafenmeistergebäude») ohne einzelnes Wort in der letzten Zeile: die letzten zwei Wörter
     bleiben zusammen, wenn sie gemeinsam in die Zeile passen (sonst bleibt der Umbruch, wie er ist) */
  function bildtitelFest() {
    document.querySelectorAll('.ws-fwahl__t:not([data-fest2])').forEach(function (t) {
      if (t.children.length || !t.isConnected || !t.clientWidth) return;
      t.setAttribute('data-fest2', '');
      var s = t.textContent, i = s.trimEnd().lastIndexOf(' ');
      if (i < 0 || s.trim().split(/\s+/).length < 3) return;
      t.textContent = s.slice(0, i) + ' ' + s.slice(i + 1);
      if (t.scrollWidth > t.clientWidth + 1) t.textContent = s;
    });
  }
  function alles() { plan = 0; fest(); ganz(); ohneX(); titelFest(); langFelder(); bildtitelFest(); }
  if (window.MutationObserver) new MutationObserver(function () { if (!plan) plan = requestAnimationFrame(alles); }).observe(document.documentElement, { childList: true, subtree: true, characterData: true });
})();
