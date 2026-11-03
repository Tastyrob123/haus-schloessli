/* Unterlagen ohne heutige Fassung (Brief, Angebot): nur die Idee, mittig (Werkbank Papier 3.11.2026) */
(function () {
  var U = window.UNTERLAGEN, s = document.querySelector('.uschau'); if (!U || !s) return;
  var wahl = [].slice.call(document.querySelectorAll('.uwahl button'));
  function pruef() { var i = wahl.findIndex(function (w) { return w.getAttribute('aria-pressed') === 'true'; }); var x = U[i < 0 ? 0 : i]; s.classList.toggle('ohne-alt', !!x && !x.alt.length); }
  new MutationObserver(pruef).observe(document.querySelector('.uwahl'), { attributes: true, subtree: true, attributeFilter: ['aria-pressed'] }); pruef();
})();
