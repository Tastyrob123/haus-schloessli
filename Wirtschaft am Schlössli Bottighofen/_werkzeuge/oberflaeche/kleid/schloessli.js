/* kleid/schloessli.js · Hauswerte für oberflaeche.js (Wirtschaft am Schlössli, Seestrasse 50, 8598 Bottighofen TG, direkt im Hafen am Bodensee; Oberchef Nachtbau 3./4.11.2026).
   Im <head> VOR allen Stilen laden (ohne defer). Rahmen «Die Bühne»: Kopf dunkel wie die Nacht über dem See (#0b1d3d), Raum hell wie das Papier im Seespiegel (#E7ECF3).
   Liegt unter _werkzeuge/oberflaeche/ und wird von den Werkzeug-Servern unter /assets/oberflaeche/ ausgeliefert (einziger Schreiber: Hafenbüro bzw. Oberchef).
   Fotos und Schriften kommen aus der Website (/assets/img/<schlüssel>-<breite>.webp, Register website/inhalt/bilder.json; /assets/fonts/), Wortmarke aus /assets/oberflaeche/kleid/schloessli-marke.svg#wm.
   Stamm: kleid/schloessli.js (Culinarium Hannover) bzw. kleid/wildside.js; Werte des Hauses aus dem Kleid vom 19.10.2026 und der gebauten Website (assets/css/haus.css :root). */
window.WO_HAUS = { kurz: 'schloessli', name: 'Wirtschaft am Schlössli', voll: 'Wirtschaft am Schlössli Bottighofen', ort: 'Bottighofen', bar: 'Lästermeile', welt: 'land', rahmen: 'buehne', anrede: 'sie',   /* das Haus siezt («Mehr Wirtschaft, weniger feine Pinkel», herzlich, Schweizer Schreibung mit ss) */
  /* Aussenfoto des Startbilds: die blauen Stühle auf der Terrasse am Mittag, dahinter der Bodensee und die Alpen (Bildregister der Website, Schlüssel «start», Stufen 480/800/1200/1800/2400) */
  foto: '/assets/img/start-1200.webp', fotoKlein: '/assets/img/start-800.webp', fotoFarbe: '#7d94ab',
  fotoStufen: [480, 800, 1200], fotoAlt: 'Blaue Stühle auf der Terrasse am Mittag, dahinter der Bodensee und die Alpen',
  /* Zeichen im Ring: die Zeiger der Wortmarke (website/assets/svg/zeichen.svg, unverändert); die ganze Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» in Open Sans als Symbol #wm */
  zeichen: '/assets/oberflaeche/kleid/schloessli-zeichen.svg', zeichenMass: 0.605, wortmarke: '/assets/oberflaeche/kleid/schloessli-marke.svg#wm', wortmarkeMass: 21.01,
  /* Namen der sieben Werkzeuge: die EINE Stelle. Robert 19.10.2026 «passt» (über den Chef-Chat Kuchler); «Das Bildarchiv» heisst seit 29.10.2026 bei allen Häusern «Das Markenbuch» (Kriterium 17: Namen passen zum Inhalt).
     Dateien, Schlüssel und Adressen bleiben (maison, bureau, carte …), die Prüf-Schlüssel ebenso (tresen, schaufenster, pairing-karte, gaestebuch, plakatarchiv, besucherliste, plakatwerkstatt). */
  namen: { zentrale: 'Das Hafenbüro', website: 'Das Schaufenster', karten: 'Das Kartenpult', gaeste: 'Das Reservationsbuch', marke: 'Das Markenbuch', besuche: 'Die Besucherliste', druck: 'Die Hausdruckerei' },
  saetze: { zentrale: 'Hier beginnt alles: ein Blick auf alle Werkzeuge und ihren Stand.',
    website: 'Die Website selbst pflegen: Texte, Fotos, Zeiten, Ferien, Anlässe, Hinweise.',
    karten: 'Speisekarte, Lunch, Lästermeile, Weinkarte und Bankett schreiben, daraus entstehen Karte und PDF.',
    gaeste: 'Fragen der Gäste zu Tisch, Terrasse, Banketts und Allergien, mit Antwortentwurf.',
    marke: 'Zeichen, Wortmarke, Fotos, Farben und Schriften des Hauses an einem Ort.',
    besuche: 'Wer die Website besucht: woher, wann, welche Seiten, wer reservieren oder feiern will.',
    druck: 'Aushänge, Karten, Einladungen und Beiträge in der Sprache des Hauses entwerfen.' },
  wege: { zentrale: '/_werkzeuge/maison/', website: '/_werkzeuge/bureau/', karten: '/_werkzeuge/carte/', gaeste: '/_werkzeuge/reception/', marke: '/_werkzeuge/livre/', besuche: '/_werkzeuge/registre/', druck: '/_werkzeuge/imprimerie/' },
  /* Prüfserver je Werkzeug (cloud/haus.json); Wege zwischen Werkzeugen immer 127.0.0.1, nie localhost (Fehlerbuch 10a) */
  ports: { zentrale: 9281, website: 9282, karten: 9283, gaeste: 9284, marke: 9285, besuche: 9286, druck: 9287, werkbank: 9288, website_lokal: 8982 } };
/* Lokal (Prüfserver je Werkzeug) zeigen die Wege zu den ANDEREN Werkzeugen auf deren eigenen Server unter 127.0.0.1, nie auf den eigenen Port
   (Fund culinarium-reception 28.10.2026: der Knopf «La Maison» öffnete /_werkzeuge/maison/ auf 9284 ohne Stand-Wege; Fehlerbuch 10a). Online bleiben sie relativ.
   Wer selbst schon absolute Wege setzt: nur Wege umschreiben, die noch mit «/» beginnen (WO_HAUS.wegeLokal = true zeigt, dass es hier geschah). */
(function () {
  if (!/^(127\.0\.0\.1|localhost)$/.test(location.hostname)) return;
  Object.keys(WO_HAUS.wege).forEach(function (k) {
    var p = WO_HAUS.ports[k], w = WO_HAUS.wege[k];
    if (p && String(p) !== location.port && w.charAt(0) === '/') WO_HAUS.wege[k] = 'http://127.0.0.1:' + p + w;
  });
  WO_HAUS.wegeLokal = true;
})();
document.documentElement.setAttribute('data-wo-haus', WO_HAUS.kurz);
document.documentElement.setAttribute('data-wo-rahmen', WO_HAUS.rahmen);
try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
/* Bewegung der Werkzeuge (29.10.2026): bewegung.js neben oberflaeche.js, async und mit wenig Vorrang nachgeladen, damit es nie vor dem ersten Knopf steht */
(function () {
  var me = document.currentScript, s = document.createElement('script');
  s.src = (me && me.src ? new URL('../bewegung.js', me.src).href : '/assets/oberflaeche/bewegung.js') + '?v=3';   /* Fassung hochzählen, wenn bewegung.js sich ändert */
  s.async = true; s.setAttribute('fetchpriority', 'low'); document.head.appendChild(s);
})();
/* Titel fliegen zeilenweise hoch (Kriterium 37, 30.10.2026). WO_ZEILEN(el) setzt jedes Wort eines Titels in <span class="wo-w"> und schreibt die Zeile als --z daran;
   die Wörter einer Zeile steigen zusammen, Zeile für Zeile gestaffelt. Ändert sich dabei der Umbruch (Silbentrennung, sehr lange Wörter), bleibt der Titel unberührt.
   Hier im Kleid (ohne defer), damit der Titel des Startbilds schon vor dem ersten Bild geteilt ist; bewegung.js nutzt dieselbe Funktion für die Zwischentitel. */
window.WO_ZEILEN = function (el) {
  if (!el || el.hasAttribute('data-wo-zl')) return !!(el && el.classList.contains('wo-zl'));
  var h0 = el.offsetHeight; if (!h0) return false;   /* verborgen: später, wenn er zu sehen ist */
  el.setAttribute('data-wo-zl', '');
  var w0 = Math.max(el.scrollWidth, el.clientWidth), roh = el.innerHTML, tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), t, ts = [];
  while ((t = tw.nextNode())) if (/\S/.test(t.data) && !t.parentNode.closest('svg')) ts.push(t);
  if (!ts.length) return false;
  ts.forEach(function (t) {
    var f = document.createDocumentFragment();
    t.data.split(/(\s+)/).forEach(function (s) {
      if (!s) return;
      if (/^\s+$/.test(s)) { f.appendChild(document.createTextNode(s)); return; }
      var w = document.createElement('span'); w.className = 'wo-w'; w.textContent = s; f.appendChild(w);
    });
    t.parentNode.replaceChild(f, t);
  });
  if (el.offsetHeight !== h0 || el.scrollWidth > w0 + 1) { el.innerHTML = roh; return false; }
  var z = -1, oben = -1e9, halb = parseFloat(getComputedStyle(el).fontSize) * 0.5;
  el.querySelectorAll('.wo-w').forEach(function (w) { var y = w.getBoundingClientRect().top; if (y > oben + halb) { z++; oben = y; } if (z) w.style.setProperty('--z', z); });
  el.classList.add('wo-zl');
  return true;
};
/* Der Titel des Startbilds: geteilt, sobald er im Dokument steht (vor dem ersten Bild, der Auftritt beginnt erst nach 0,18 s) */
(function () {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('MutationObserver' in window)) return;
  var plan = 0;
  function teile() {
    plan = 0;
    document.querySelectorAll('.wo-sb__h:not([data-wo-zl])').forEach(function (h) {
      if (document.documentElement.classList.contains('still')) return;
      var a = h.getAnimations ? h.getAnimations() : [];
      if (a.some(function (x) { return (x.currentTime || 0) > 120; })) { h.setAttribute('data-wo-zl', ''); return; }   /* läuft schon: bleibt ein Block, nie zurückspringen */
      WO_ZEILEN(h);
    });
  }
  new MutationObserver(function () { if (!plan && document.querySelector('.wo-sb__h:not([data-wo-zl])')) { plan = 1; Promise.resolve().then(teile); } })
    .observe(document.documentElement, { childList: true, subtree: true });
})();
