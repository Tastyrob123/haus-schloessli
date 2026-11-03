/* Rücksprung (Robert 1.11.2026): Zurück/Vor im Browser landet auf der alten Höhe der Seite, nie ganz oben.
   Merkt je Seite in sessionStorage (rs:<Pfad>) die Höhe und das Inhaltsstück am oberen Fensterrand (beim Scrollen, beim Klick auf einen Link, bei pagehide).
   Kommt man mit Zurück/Vor wieder (Navigation «back_forward»), richtet sich die Seite nach dem Aufbau an diesem Stück aus, nicht nur an der Pixelzahl:
   Abschnitte mit content-visibility:auto stehen nach dem Laden als 1400-px-Platzhalter da, dieselbe Pixelhöhe zeigt sonst anderen Inhalt.
   Für den Moment des Sprungs: alles einmal gezeichnet, keine Übergänge, keine Auftakt-Bewegung (rs-sofort); alles bis zum Fensterrand gilt als gezeigt (.da).
   Aus dem bfcache stellt der Browser die Höhe selbst her. Keine unload-Handler. Seiten mit eigenem Rückweg (#rh-zurueck, «wb-y») und Rahmen bleiben unberührt, ausser der Rückweg trägt data-rs (dann führt er nur ?y= aus, Zurück/Vor macht der Rücksprung).
   Merkpunkt: das nächste feststehende Stück auf einem Drittel der Höhe; liegt dort eine mitlaufende Bühne (sticky), gilt der Abschnitt, der sie trägt (Robert 1.11.2026, Werkbänke mit Handy-/Laptop-Bühnen). */
(function () {
  var RH = document.getElementById('rh-zurueck');   /* eigener Rückweg: nur wenn er Zurück/Vor ausdrücklich dem Rücksprung überlässt (data-rs) */
  if (RH && !RH.hasAttribute('data-rs')) return;
  try { if (window.top !== window) return; } catch (e) { return; }
  var K = 'rs:' + location.pathname, H = document.documentElement, sperre = false, t = 0;
  var SEL = 'h1,h2,h3,h4,h5,p,li,figure,img,picture,video,blockquote,table,tr,section,article,header,footer,div';
  function festAb(e) {   /* das äusserste mitlaufende (fixed/sticky) Element über e, sonst null */
    var f = null; for (; e && e !== document.body && e !== H; e = e.parentElement) { var p = getComputedStyle(e).position; if (p === 'fixed' || p === 'sticky') f = e; } return f;
  }
  function stand(e) {   /* das nächste feststehende Inhaltsstück: in einer mitlaufenden Bühne (sticky) gilt der Abschnitt, der sie trägt; schwebende Leisten (fixed) nie */
    for (var n = 0; e && n < 30; n++) {
      var c = e.closest && e.closest(SEL); if (!c || c === document.body || c === H) return null;
      var f = festAb(c); if (!f) return c;
      if (getComputedStyle(f).position === 'fixed') return null;
      e = f.parentElement;
    }
    return null;
  }
  function text(e) { return (e.textContent || e.getAttribute('src') || '').replace(/\s+/g, ' ').trim().slice(0, 40); }
  function anker() {   /* das Inhaltsstück auf einem Drittel der Fensterhöhe (nicht die schwebende Leiste) */
    if (!document.elementsFromPoint) return null;
    var l = null, xs = [.5, .25, .75];
    for (var k = 0; k < xs.length; k++) {
      var st = document.elementsFromPoint(innerWidth * xs[k], innerHeight * .3);
      for (var j = 0; j < st.length; j++) { var c = stand(st[j]); if (c) { l = c; break; } }
      if (l) break;
    }
    if (!l) return null;
    /* lieber der Abschnitt drumherum (section, article, Kopf, Fuss, Stück mit id): bewegte Teile darin (Chat, Film, Bühne) verrutschen, der Abschnitt nicht */
    var g = l.closest('section,article,header,footer,[id]');
    if (g && g !== document.body && g !== H && g.tagName !== 'MAIN' && g.matches(SEL) && !festAb(g) && g.getBoundingClientRect().height <= innerHeight * 4) l = g;
    var alle = document.querySelectorAll(SEL), i = [].indexOf.call(alle, l);
    return i < 0 ? null : { i: i, d: l.id || '', n: l.tagName, t: text(l), o: Math.round(l.getBoundingClientRect().top) };
  }
  function merk(mitAnker) {
    if (sperre) return;
    var w = { y: Math.round(window.scrollY || 0) };
    if (mitAnker) { try { var a = anker(); if (a) w.a = a; } catch (e) {} }
    else { try { var alt = JSON.parse(sessionStorage.getItem(K) || '{}'); if (alt.a && Math.abs(alt.y - w.y) < 2) w.a = alt.a; } catch (e) {} }
    try { sessionStorage.setItem(K, JSON.stringify(w)); } catch (e) {}
  }
  addEventListener('scroll', function () { if (!t) t = setTimeout(function () { t = 0; merk(false); }, 150); }, { passive: true });
  document.addEventListener('click', function (ev) { if (ev.target.closest && ev.target.closest('a[href]')) merk(true); }, true);
  addEventListener('pagehide', function () {   /* beim Verlassen übernimmt der Rücksprung die Höhe ganz: sonst setzt Chrome beim Zurück die alte Pixelhöhe noch mehrmals nach */
    try { history.scrollRestoration = 'manual'; } catch (e) {}
    merk(true);
  });

  var nav; try { nav = performance.getEntriesByType('navigation')[0]; } catch (e) {}
  if (!nav || (nav.type !== 'back_forward' && nav.type !== 'reload')) return;   /* Zurück/Vor und Neuladen landen an der alten Stelle */
  var w; try { w = JSON.parse(sessionStorage.getItem(K)); } catch (e) {}
  if (!w || typeof w.y !== 'number' || w.y < 2) return;
  sperre = true;
  try { history.scrollRestoration = 'manual'; } catch (e) {}
  var st = document.createElement('style');
  st.textContent = 'html.rs-sofort,html.rs-sofort *{transition:none!important;animation-duration:0s!important;animation-delay:0s!important;scroll-behavior:auto!important}'
    + 'html.rs-ganz *{content-visibility:visible!important}';
  (document.head || H).appendChild(st);
  H.classList.add('rs-sofort', 'rs-ganz');
  var weg = false;
  function fertig() { sperre = false; H.classList.remove('rs-ganz'); }
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (k) { addEventListener(k, function () { weg = true; fertig(); }, { once: true, passive: true }); });
  function stueck() {   /* das gemerkte Stück wiederfinden: über seine id, sonst gleiche Stelle, sonst gleiche Art mit gleichem Anfang, die nächste zur alten Stelle
                           (Seiten bauen nach dem Laden noch Teile dazu, z. B. Chat-Vorführungen: die Stelle im Aufbau verschiebt sich) */
    var a = w.a; if (!a) return null;
    if (stueck.e && stueck.e.isConnected) return stueck.e;
    var e = a.d && document.getElementById(a.d);
    if (e && e.tagName === a.n) return e;
    var alle = document.querySelectorAll(SEL); e = alle[a.i];
    if (e && e.tagName === a.n && text(e) === a.t) return e;
    var best = null, bd = 1e9;
    for (var k = 0; k < alle.length; k++) { var x = alle[k]; if (x.tagName === a.n && Math.abs(k - a.i) < bd && text(x) === a.t) { best = x; bd = Math.abs(k - a.i); } }
    return (stueck.e = best);
  }
  function ziel() { var e = stueck(); return e ? Math.max(0, Math.round(window.scrollY + e.getBoundingClientRect().top - w.a.o)) : w.y; }
  function zeig() {
    var g = window.scrollY + innerHeight;
    [].forEach.call(document.querySelectorAll('[data-a],.odo,.zt,.roll,img.ld'), function (e) {
      if (!e.classList.contains('da') && e.getBoundingClientRect().top + window.scrollY < g) e.classList.add('da');
    });
  }
  function geh() { if (weg) return; var y = ziel(); if (Math.abs(window.scrollY - y) > 2) window.scrollTo(0, y); zeig(); }
  function los() {
    geh();
    requestAnimationFrame(function () { geh(); requestAnimationFrame(function () { geh(); H.classList.remove('rs-sofort'); }); });
    var n = 0, iv = setInterval(function () {
      n++; geh();
      if (n >= 16 || weg) { clearInterval(iv); geh(); fertig(); requestAnimationFrame(function () { geh(); merk(true); }); }
    }, 150);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', los); else los();
  addEventListener('load', function () { if (sperre) geh(); });
})();
