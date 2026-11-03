/* Die Hausdruckerei der Wirtschaft am Schlössli (Stamm 28.10.2026, Schlössli 3.11.2026): Werkzeug-Oberfläche «Die Bühne».
   Die Werkstatt hat ein eigenes Gerüst (Übersicht #start mit .ms-leiste/.ms-kopf, Arbeitsfläche mit header.kopf/aside.links); der Kern bleibt unberührt.
   Diese Hausschicht legt nur an, was in allen Werkzeugen des Hauses gleich ist: die Marke im Kopf (Zeichen, Name in der Titelschrift, Unterzeile), die runden
   Knöpfe und «Website ansehen», die Startbilder (Übersicht «voll» mit dem Haus, jede Ansicht «buehne» mit ihrem Raum). Ids, Knoten und Handler bleiben.
   Geladen nach buehne.js (index.html, HAUS_STIL). Entfernen = vorheriger Stand. */
(function () {
  if (!window.WO) return;
  var BASIS = 'haeuser/schloessli/kopf/';
  /* Kopf-Fotos mit 800er-Fassung (kopf/<name>-800.webp) und Breite des Originals: das Foto steht bei 1440 rund 660, bei 1000 rund 385, am Handy rund 265 px breit,
     die 800er reicht dort; ab rund 1700 px Fensterbreite oder bei doppelter Dichte nimmt der Browser das Original (30.10.2026, Oberchef) */
  var B800 = { abend: 900, abendschiff: 1200, anguria: 900, apero: 900, bar: 900, bootshafen: 1200, fliesen: 1200, gaststube: 1200, morgen: 1200, platanen: 900, regal: 1200, saentis: 1200, schild: 900, start: 1200, team: 1200, wein: 901 };
  var FOTO = { msAbend: 'platanen', msMotive: 'bootshafen', msEvents: 'moni', msAbteilungen: 'gaststube', msHinweise: 'schild', msNewsletter: 'abend', msFotos: 'thon', msMarke: 'fliesen', msLivre: 'regal', msMeine: 'bar', msFreigegeben: 'glas', msNeu: 'tortelloni' };
  var WEBSITE = location.port === '9287' ? 'http://127.0.0.1:' + ((window.WO_HAUS && WO_HAUS.ports && WO_HAUS.ports.website_lokal) || 8982) + '/' : '/';
  var MARKE = function () { return WO.zeichen() + '<span><b>' + WO.esc(WO.name('druck')) + '</b><small>Drucksachen · ' + WO.esc(WO.haus.name) + '</small></span>'; };

  /* Marke, runde Knöpfe und Website-Pille in beiden Köpfen */
  function koepfe() {
    var mk = document.getElementById('kopfMarke');
    if (mk && !mk.__wo) {   // die alten Knoten (#kopfZeichen, #kopfName) bleiben verborgen darin, studio.js schreibt sie beim Start
      mk.__wo = 1; mk.classList.add('wo-marke-w');
      var alt = document.createElement('span'); alt.className = 'ws-alt'; alt.hidden = true;
      while (mk.firstChild) alt.appendChild(mk.firstChild);
      mk.innerHTML = MARKE(); mk.appendChild(alt);
    }
    var ms = document.querySelector('.ms-kopf');
    if (ms && !ms.__wo) {
      var z = ms.querySelector('#msKopfZeichen'), n = ms.querySelector('.ms-kopf-name');
      if (z && n) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'wo-marke-w ws-marke'; b.setAttribute('data-ansicht', 'start'); b.setAttribute('aria-label', WO.name('druck') + ', Übersicht');
        b.innerHTML = MARKE(); ms.insertBefore(b, z); z.hidden = true; n.hidden = true; ms.__wo = 1;
      }
    }
    [].forEach.call(document.querySelectorAll('.ms-kopf .rund, .kopf__werk .rund'), function (r) { r.classList.add('ws-rund'); /* eigene Klasse: .wo-kn des Pakets würde die Anzeige der Werkstatt (verborgene Knöpfe am Handy) überstimmen */ });
    var web = document.querySelector('.ms-kopf .zur-website');
    if (web && !web.__wo) {
      web.__wo = 1;
      var pille = document.createElement('span'); pille.innerHTML = WO.knopf('Website ansehen', 'welt', 'gold', { href: WEBSITE, neu: true, klein: true, klasse: 'ws-web' });
      var p = pille.firstChild, neu = document.querySelector('.ms-kopf .ms-kn-neu');
      web.hidden = true; web.parentNode.insertBefore(p, neu ? neu.nextSibling : null);
    }
  }

  /* Startbild der Übersicht: WO.startbild «voll», Gruss und Satz bleiben dieselben Knoten (start.js schreibt sie), das Feld steht darunter */
  function startbild() {
    var g = document.querySelector('#msStart .ms-gruss');
    if (!g || g.__wo) return; g.__wo = 1; g.__b = 1;
    var h = document.getElementById('msGruss'), s = document.getElementById('msSatz');
    var hilf = document.createElement('div');
    hilf.innerHTML = WO.startbild({ werkzeug: 'druck', art: 'voll', h1: ' ', satz: ' ', knoepfe: ' ' });
    var sb = hilf.firstChild; sb.classList.add('ws-sb');
    if (h) { h.classList.add('wo-sb__h'); sb.querySelector('.wo-sb__h').replaceWith(h); }
    if (s) { s.classList.add('wo-sb__satz'); sb.querySelector('.wo-sb__satz').replaceWith(s); }
    var kn = sb.querySelector('.wo-sb__kn'); kn.textContent = '';
    [].slice.call(g.querySelectorAll(':scope>.ms-feld, :scope>#msAlle')).forEach(function (x) { kn.appendChild(x); });
    g.replaceWith(sb);
  }
  /* Startbild jeder Ansicht: die Titelzeile (.ms-titel) wird WO.startbild «buehne» mit dem Raum der Ansicht; h1 und Satz bleiben dieselben Knoten */
  function buehnen() {
    [].forEach.call(document.querySelectorAll('#start .ms-titel'), function (t) {
      if (t.__wo) return; t.__wo = 1; t.__b = 1;   // __b: buehne.js legt hier keine eigene Bühne mehr an
      [].forEach.call(t.querySelectorAll(':scope>.ms-bue__foto'), function (x) { x.remove(); });
      var v = t.closest('[id^="ms"]'), h1 = t.querySelector('h1'), satz = t.querySelector('.ms-leise');
      var hilf = document.createElement('div');
      var fn = FOTO[v && v.id] || 'start', gr = B800[fn];
      hilf.innerHTML = WO.startbild({ werkzeug: 'druck', art: 'buehne', h1: ' ', satz: satz ? ' ' : '', foto: BASIS + fn + '.webp',
        srcset: gr ? BASIS + fn + '-800.webp 800w, ' + BASIS + fn + '.webp ' + gr + 'w' : '', sizes: '(max-width:700px) 70vw, (max-width:1100px) 39vw, 50vw' });
      var sb = hilf.firstChild; sb.classList.add('ws-sb');
      if (h1) { h1.classList.add('wo-sb__h'); sb.querySelector('.wo-sb__h').replaceWith(h1); }
      if (satz) { satz.classList.add('wo-sb__satz'); sb.querySelector('.wo-sb__satz').replaceWith(satz); }
      [].slice.call(t.children).forEach(function (x) { sb.querySelector('.wo-sb__text').appendChild(x); });   // was sonst in der Titelzeile steht (Knöpfe, Wahl), bleibt dabei
      t.classList.remove('ms-bue', 'ms-bue--knapp'); t.textContent = ''; t.appendChild(sb); t.classList.add('ws-titel');
    });
  }
  function alles() { koepfe(); startbild(); buehnen(); }
  function los() {
    alles();
    var lauf = 0, st = document.getElementById('start');
    new MutationObserver(function () { if (lauf) return; lauf = 1; try { alles(); } finally { lauf = 0; } }).observe(st || document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', los); else los();
})();
