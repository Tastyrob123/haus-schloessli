/* Das Besucherbuch (Le Registre) · Wirtschaft am Schlössli: Zählung auf der Website (Tasty Studios 19.10.2026). VORSCHLAG, noch nicht eingebaut: der Einbau
   in bau.py und das Hochladen gehören dem Werkbank-Chat des Schlössli (Station 14; Anleitung: _werkzeuge/registre/STAND.md, «Anschluss an die Website»).
   Ziel: assets/js/messung.js, auf jeder Seite vor </body> als <script src="assets/js/messung.js?v=…" defer></script>, nach haus.js, funktionen.js und fuss.js.
   Vorbild: messung.js des Berghotel Gasterntal (dort nach Doldenhorn, nur gelesen), Ereignisse des Schlössli.

   Je Seite geht eine Zeile an /api/registre (lokal der Server des Besucherbuchs, online die Funktion api/registre.py, gleiche Adresse):
       r1 <seitenaufruf> <datei> <sprache> <geraet> <sekunden> <ereignisse|-> <herkunft|->
   einmal beim Öffnen (0 Sekunden), bei jedem gezählten Klick und beim Verlassen (Sekunden, in denen die Seite sichtbar war).
   Ohne Cookies und ohne Kennung im Gerät: «seitenaufruf» ist eine Zufallsfolge, die nur in dieser Variablen lebt und mit der Seite endet.
   Dass die Seiten eines Besuchs zusammenfinden, Land und Ort bestimmt der Server aus der Verbindung (registre.py); die Adresse speichert er nicht.
   «herkunft» ist nur der Name der Website, von der der Gast kam (zum Beispiel www.gaultmillau.ch), nie die ganze Adresse.
   «sprache» ist die Sprache des Browsers (die Website gibt es nur deutsch), sonst «xx».
   Nicht gezählt: automatische Browser (Prüfläufe), Seiten im Rahmen, die Werkzeuge und Beigaben des Hauses, Varianten- und Studienseiten und Geräte
   mit der Marke «schloessli-nicht-zaehlen» im localStorage (das Einzige, was je im Gerät steht).
   Die Fenster der Website (assets/js/haus.js Teil 7, funktionen.js Reiter) bleiben unberührt: gezählt wird nur, dass etwas geöffnet oder abgeschickt wurde,
   nie ein Inhalt.

   Ereignisse (Schlüssel wie in allen Häusern, Bedeutung im Schlössli):
     fenster  Fenster «Reservation» geöffnet (Knopf oder Link mit data-fenster="fe-reservation")
     buchung  Tisch angefragt: im Fenster «Reservation» das Formular «Mit Wünschen anfragen» abgeschickt (das Fenster zeigt danach «gesendet»)
     booking  «Direkt buchen» gewählt (Reiter im Fenster, der die Buchungsmaske von gastronovi lädt, oder ein Link zu gastronovi)
     tisch    Fenster «Bankettanfrage» geöffnet (data-fenster="fe-bankett")
     anfrage  Bankettanfrage oder Gutschein-Bestellung abgeschickt (Fenster zeigt «gesendet»)
     anruf    Telefonnummer des Hauses angeklickt (+41 71 688 90 92)
     mail     Mail-Adresse angeklickt (mailto:)
     chat     weiter zum Schwesterhaus Taverne zum Schäfli (Link zur Seite des Schäfli, zum Tisch im Schäfli bei zenchef oder Nummer des Schäfli);
              die Website hat keinen Gäste-Chat, der Schlüssel bleibt wie in den anderen Häusern
     route    Route zum Hafen geöffnet (Link «Route» zu OpenStreetMap) */
(function () {
  'use strict';
  var n = navigator, d = document, w = window;
  if (w.__registre || !n.sendBeacon || n.webdriver || w.self !== w.top) return;
  try { if (w.localStorage.getItem('schloessli-nicht-zaehlen') === '1') return; } catch (e) { /* privat: zählt normal */ }
  var teile = location.pathname.split('/'), datei = teile.pop() || 'index.html';
  if (teile.length > 2 || /^(studio|_werkzeuge|werkzeuge|werkbank|_werkbank|maison|marke|reception|registre|imprimerie|unterlagen|drucksachen|feed|material|bearbeitet)$/.test(teile[1] || '')) return;
  if (!/^[a-z0-9-]{1,60}\.html$/.test(datei) || /varianten|^konzept|^bildauswahl|^vorschau|^404/.test(datei)) return;
  w.__registre = 1;
  var SPRACHEN = ' de en fr it nl es pt zh ja ko ar ';
  var sp = String(n.language || 'de').slice(0, 2).toLowerCase();
  if (SPRACHEN.indexOf(' ' + sp + ' ') < 0) sp = 'xx';
  var breit = function (px) { return !!(w.matchMedia && w.matchMedia('(max-width:' + px + 'px)').matches); };
  var geraet = breit(700) ? 'handy' : breit(1060) ? 'tablet' : 'rechner';
  var her = '-';
  try { var r = d.referrer ? new URL(d.referrer).hostname.toLowerCase() : ''; if (r && r !== location.hostname && /^[a-z0-9.-]{3,60}$/.test(r)) her = r; } catch (e) {}
  var HAUS_TEL = /^tel:\+?(41716889092|0716889092)$/, SCHAEFLI_TEL = /^tel:\+?(41527631172|0527631172)$/;
  var pv, war, liste, sichtbar, seit, gesendet;
  function neu() {
    pv = (Math.random().toString(36) + '000000').slice(2, 8);
    war = {}; liste = []; sichtbar = 0; gesendet = '';
    seit = d.visibilityState === 'hidden' ? 0 : Date.now();
    sende();
  }
  function sek() { return Math.min(1800, Math.round((sichtbar + (seit ? Date.now() - seit : 0)) / 1000)); }
  function sende() {
    var zeile = 'r1 ' + pv + ' ' + datei + ' ' + sp + ' ' + geraet + ' ' + sek() + ' ' + (liste.length ? liste.join(',') : '-') + ' ' + her;
    if (zeile === gesendet) return;
    gesendet = zeile;
    try { n.sendBeacon('/api/registre', zeile); } catch (e) {}   /* wartet auf keine Antwort */
  }
  function zaehle(was) {
    if (war[was]) return;
    war[was] = 1; liste.push(was);
    sende();
  }
  function weg() { if (seit) { sichtbar += Date.now() - seit; seit = 0; } sende(); }
  neu();
  d.addEventListener('visibilitychange', function () { if (d.visibilityState === 'hidden') weg(); else if (!seit) seit = Date.now(); });
  w.addEventListener('pagehide', weg);
  w.addEventListener('pageshow', function (e) { if (e.persisted) neu(); });   /* zurück aus dem Seitenspeicher des Browsers: neuer Aufruf */

  d.addEventListener('click', function (e) {
    var t = e.target; if (!t || !t.closest) return;
    var f = t.closest('[data-fenster]');
    if (f) { var id = f.getAttribute('data-fenster'); if (id === 'fe-reservation') zaehle('fenster'); else if (id === 'fe-bankett') zaehle('tisch'); return; }
    var rt = t.closest('#fe-reservation [data-reiter="direkt"]'); if (rt) { zaehle('booking'); return; }
    var a = t.closest('a[href]'); if (!a) return;
    var h = (a.getAttribute('href') || '').replace(/\s/g, ''), host = (a.hostname || '').toLowerCase();
    if (/(^|\.)gastronovi\.com$/.test(host)) zaehle('booking');
    else if (/(^|\.)schaefli-wigoltingen\.ch$|(^|\.)zenchef\.com$/.test(host)) zaehle('chat');
    else if (/^tel:/i.test(h)) { if (HAUS_TEL.test(h)) zaehle('anruf'); else if (SCHAEFLI_TEL.test(h)) zaehle('chat'); }
    else if (/^mailto:/i.test(h)) zaehle('mail');
    else if (/(^|\.)openstreetmap\.org$/.test(host) && /\/directions/.test(a.pathname || '')) zaehle('route');
  }, true);
  /* Abgeschickt ist ein Formular erst, wenn das Fenster «gesendet» zeigt (haus.js setzt die Klasse nach der Prüfung der Felder).
     Nachgesehen wird kurz, höchstens 20 Sekunden; bleibt das Fenster ohne «gesendet» (Pflichtfeld leer), zählt nichts. */
  d.addEventListener('submit', function (e) {
    var fm = e.target; if (!fm || !fm.closest) return;
    var dlg = fm.closest('dialog.fe'); if (!dlg) return;
    var was = dlg.id === 'fe-reservation' ? 'buchung' : (dlg.id === 'fe-bankett' || dlg.id === 'fe-gutschein') ? 'anfrage' : '';
    if (!was) return;
    var bis = Date.now() + 20000;
    (function schau() {
      if (dlg.classList.contains('gesendet')) { zaehle(was); return; }
      if (Date.now() < bis && dlg.open) setTimeout(schau, 250);
    })();
  }, true);
})();
