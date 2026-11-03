/* pruefung-haus.js · Prüfseite im Rahmen der Wirtschaft am Schlössli (Nachtbau 3.11.2026, Aufbau aus dem Culinarium): Name des Werkzeugs aus der einen Stelle, «Zum Werkzeug» führt in dieses Werkzeug, nicht in den Stamm. */
(function () {
  var z = document.getElementById('wsp-zurueck'); if (z) z.href = '/_werkzeuge/bureau/';
  var n = window.WO_HAUS && WO_HAUS.namen && WO_HAUS.namen.website;
  if (n) { document.querySelectorAll('[data-werkzeug]').forEach(function (e) { e.textContent = n; e.removeAttribute('data-werkzeug'); });   /* ohne das Merkmal füllt welt.js den Namen des Stamms («Der Schreibtisch») nicht nachträglich ein */ document.title = 'Prüfung · ' + n + ' · ' + WO_HAUS.name; }
})();
/* Termine (Schlössli 3.11.2026): eigener Teil der Prüfung (Quelle haus.json › ferien_iso, Speicher, Sicherung) und die Lexikon-Einträge der Stichworte aus
   termine.py und termine-ansicht.js. Das Lexikon des Stamms bleibt unverändert; diese Einträge stehen darunter mit eigener Kennung lex-<stichwort>
   und öffnen sich, wenn «Was tun?» dorthin führt. */
(function () {
  var LEX = [
    { id: 'termine-quelle', titel: 'Die Ferien der Website sind nicht lesbar', sehen: 'Die Ansicht «Termine» startet nicht, oder hier steht «Ferien der Website» rot.',
      grund: 'Die Ferien stehen in website/inhalt/haus.json als «ferien_iso» (erster und letzter Tag). Die Website wurde umgebaut und die Angabe fehlt oder hat eine neue Form.',
      tun: 'Nichts ist verloren: Entwurf und veröffentlichte Ferien liegen im Speicher des Werkzeugs. Die Angabe in haus.json wieder so bauen lassen, dann diese Seite neu laden.' },
    { id: 'termine-speicher', titel: 'Der Speicher der Ferien ist beschädigt', sehen: 'Meldung «SPEICHER · Die Datei der Ferien und ihre Sicherung sind beide unlesbar».',
      grund: 'Die Datei _werkzeuge/bureau/_daten/termine.json und ihre Sicherung termine.json.gut sind beide kaputt (zum Beispiel von Hand geändert).',
      tun: 'Die Website zeigt weiter die Ferien, wie sie gebaut ist. Die Datei aus einer Sicherung des Rechners zurückholen oder beide Dateien entfernen: dann gilt wieder der ursprüngliche Stand.' },
    { id: 'termin-datum', titel: 'Diesen Tag gibt es nicht', sehen: 'Meldung «DATUM · Der Tag fehlt oder gibt es nicht», die Karte zeigt «Den ersten Tag gibt es nicht».',
      grund: 'Tag und Monat passen nicht zusammen, zum Beispiel der 31. November.', tun: 'Tag, Monat und Jahr neu wählen, dann speichern.' },
    { id: 'termin-reihe', titel: 'Der letzte Tag liegt vor dem ersten', sehen: 'Meldung «REIHENFOLGE · Der letzte Tag liegt vor dem ersten».',
      grund: 'Beim Verschieben wurde nur der erste Tag geändert.', tun: 'Den letzten Tag nach dem ersten wählen, dann speichern.' },
    { id: 'termin-lang', titel: 'Ferien länger als 120 Tage', sehen: 'Meldung «DAUER · Ein Ferienblock dauert höchstens 120 Tage».',
      grund: 'Erster und letzter Tag liegen mehr als vier Monate auseinander, meist ein falsches Jahr.', tun: 'Jahr des letzten Tags prüfen. Längere Ferien als zwei Blöcke eintragen.' },
    { id: 'termin-grund', titel: 'Der Anlass passt nicht', sehen: 'Meldung «ANLASS · …».',
      grund: 'Der Anlass ist länger als 60 Zeichen oder enthält Klammern. Er steht auf der Website schon in Klammern hinter den Tagen.', tun: 'Kurz und ohne Klammern schreiben, zum Beispiel «Excellence Gourmetkreuzfahrt».' },
    { id: 'termin-doppelt', titel: 'Zwei Ferienblöcke überschneiden sich', sehen: 'Meldung «ÜBERSCHNEIDUNG · Zwei Ferienblöcke überschneiden sich».',
      grund: 'Ein Block wurde zweimal angelegt oder in einen anderen hinein verschoben.', tun: 'Die Tage eines der beiden ändern, ihn mit «Wieder entfernen» herausnehmen oder beide zu einem Block zusammenlegen.' },
    { id: 'termin-viele', titel: 'Zu viele Ferienblöcke', sehen: 'Meldung «FERIEN · Höchstens 12 Ferienblöcke stehen gleichzeitig auf der Website».',
      grund: 'Die Zeile «Ferien» auf der Startseite wird mit mehr als zwölf Blöcken unlesbar.', tun: 'Vergangene Ferien «Von der Seite nehmen», dann speichern.' },
    { id: 'termin-falsch', titel: 'Ein Eintrag ist unvollständig', sehen: 'Meldung «FERIEN · …» mit Kennung oder Liste.',
      grund: 'Die Anfrage kam nicht aus dem Werkzeug oder wurde unterwegs verändert.', tun: 'Die Seite neu laden und die Eingabe wiederholen. Bleibt es, den Wortlaut der Meldung Ihrem Ansprechpartner schicken.' },
    { id: 'fassung-unbekannt', titel: 'Diese frühere Fassung gibt es nicht mehr', sehen: 'Meldung «FASSUNG · Diese frühere Fassung gibt es nicht».',
      grund: 'Die Liste der früheren Fassungen hält die letzten 60; ältere fallen heraus.', tun: 'Die Seite neu laden und eine Fassung aus der Liste wählen, oder den ursprünglichen Stand.' },
    { id: 'netz', titel: 'Der Server antwortet nicht', sehen: 'Meldung «NETZ · Der Server des Werkzeugs antwortet nicht».',
      grund: 'Die Verbindung ist weg oder der Server des Werkzeugs läuft nicht.', tun: 'Ihre Eingaben bleiben stehen. Verbindung prüfen, dann noch einmal «Speichern». Läuft der Server nicht: python3 _werkzeuge/bureau/serve.py 9282 im Hausordner.' }
  ];
  function el(tag, attrs, kinder) { var e = document.createElement(tag); Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); }); (kinder || []).forEach(function (k) { e.append(k); }); return e; }
  var lex = document.querySelector('[aria-labelledby="wsp-t4"]');
  if (!lex) return;
  var teil = el('section', { class: 'wsp-teil', 'aria-labelledby': 'wsp-t-termine', 'data-cu-pruefung': 'termine' }, [
    el('div', {}, [el('p', { class: 'kap' }, [el('span', {}, ['Viertens'])]), el('h2', { class: 't-zwischen', id: 'wsp-t-termine' }, ['Ferien des Hauses'])]),
    el('div', { class: 'platte wsp-punkte', id: 'cu-termine-punkte' }, [el('p', { class: 'wsp-wartet' }, ['Wird geprüft …'])])]);
  lex.parentNode.insertBefore(teil, lex);
  var ort = el('div', { class: 'wsp-lexikon', id: 'cu-lexikon' });
  lex.append(el('p', { class: 'kap', style: 'margin-top:28px' }, [el('span', {}, ['Termine'])]), ort);
  LEX.forEach(function (l) {
    ort.append(el('details', { class: 'platte wsp-lex', id: 'lex-' + l.id }, [el('summary', {}, [l.titel]),
      el('dl', {}, [el('dt', { class: 'angabe' }, ['Sehen']), el('dd', {}, [l.sehen]), el('dt', { class: 'angabe' }, ['Grund']), el('dd', {}, [l.grund]), el('dt', { class: 'angabe' }, ['Tun']), el('dd', {}, [l.tun])])]));
  });
  function oeffne() {
    var e = location.hash.indexOf('#lex-') === 0 && document.getElementById(location.hash.slice(1));
    if (e && ort.contains(e)) { e.open = true; setTimeout(function () { e.scrollIntoView({ block: 'start' }); }, 0); }
  }
  window.addEventListener('hashchange', oeffne); oeffne();
  fetch('/_werkzeuge/bureau/api/termine/pruefung', { cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (d) {
    var p = document.getElementById('cu-termine-punkte'); p.textContent = '';
    (d.punkte || []).forEach(function (x) {
      p.append(el('div', { class: 'wsp-punkt', 'data-gut': x.gut ? 'ja' : 'nein', 'data-punkt': 'termine' }, [
        el('span', { class: 'wsp-punkt__z' }, [x.gut ? '✓' : '–']), el('span', { class: 'wsp-punkt__t' }, [x.titel]),
        el('span', { class: 'wsp-punkt__x' }, [x.text + ' ', !x.gut && x.stichwort ? el('a', { href: '#lex-' + x.stichwort }, ['Was tun?']) : ''])]));
    });
  }).catch(function () { var p = document.getElementById('cu-termine-punkte'); p.textContent = 'Der Server des Werkzeugs antwortet nicht (Stichwort netz).'; });
})();
