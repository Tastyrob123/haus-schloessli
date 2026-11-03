/* karte.js · zeichnet eine Karte des Hauses aus ihren Daten (_karten/stand/<id>.json) in eine Seite.
   Eine Quelle für Website, PDF und La Carte: die Website liest dieselbe Datei, aus der bau.py die PDF druckt.
   Gebrauch (Station 14 verbindet, die Seiten selbst baut der Werkbank-Bauer):
     <div id="karte"></div>
     <script src="../_karten/karte.js"></script>
     <script>SchloessliKarte.lade('#karte', '../_karten/stand/speisekarte.json')</script>
   Gesetzt wird nur Text und Struktur mit Klassen «sk-…»; Schrift und Farbe kommen aus dem Stil der Seite.
   Ausgeblendete Einträge («aus»: true) erscheinen nicht. Es wird nichts verändert, was in den Daten steht. */
(function () {
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function preise(p) {
    if (!p.preise || !p.preise.length) return '';
    var ein = p.einheiten || [];
    return '<p class="sk-preise">' + p.preise.map(function (x, i) {
      return '<span class="sk-preis">' + esc(x) + (ein[i] ? ' <small>' + esc(ein[i]) + '</small>' : '') + '</span>';
    }).join('') + '</p>';
  }
  function posten(p, wein) {
    if (p.aus) return '';
    switch (p.t) {
      case 'rubrik': return '<h3 class="sk-rubrik">' + esc(p.titel) + '</h3>';
      case 'land': return '<h4 class="sk-land">' + esc(p.text) + '</h4>';
      case 'zw': return p.weingut ? '<h5 class="sk-gut">' + esc(p.text) + '</h5>' : '<h5 class="sk-zw">' + esc(p.text) + '</h5>';
      case 'notiz': return '<p class="sk-notiz">' + esc(p.text) + '</p>';
      case 'frei': return '<p class="sk-frei">' + (p.zeilen || []).map(function (z) { return esc(z.text); }).join('<br>') + '</p>';
      case 'gericht':
        return '<div class="sk-eintrag' + (wein ? ' sk-wein' : '') + '">' +
          (p.jahr ? '<span class="sk-jahr">' + esc(p.jahr) + '</span>' : '') +
          '<p class="sk-name">' + esc(p.name) + (p.zusatz ? ' <span class="sk-zusatz">' + esc(p.zusatz) + '</span>' : '') + '</p>' +
          (p.zeilen || []).map(function (z) { return '<p class="sk-text">' + esc(z.text) + '</p>'; }).join('') +
          preise(p) + '</div>';
    }
    return '';
  }
  function zeichne(ziel, eintrag) {
    var el = typeof ziel === 'string' ? document.querySelector(ziel) : ziel;
    var k = eintrag.karte, wein = k.kl === 'wein', html = '';
    k.teile.forEach(function (t) { if (t.art === 'inhalt') t.posten.forEach(function (p) { html += posten(p, wein); }); });
    if (k.fuss) html += '<p class="sk-fuss">' + k.fuss.split(' · ').map(esc).join('<br>') + '</p>';
    el.innerHTML = html;
    el.classList.add('sk-karte', 'sk-' + eintrag.id);
    return el;
  }
  function lade(ziel, adresse) {
    return fetch(adresse, { cache: 'no-cache' }).then(function (r) { if (!r.ok) throw new Error(adresse + ': ' + r.status); return r.json(); })
      .then(function (d) { return zeichne(ziel, d); });
  }
  window.SchloessliKarte = { zeichne: zeichne, lade: lade };
})();
