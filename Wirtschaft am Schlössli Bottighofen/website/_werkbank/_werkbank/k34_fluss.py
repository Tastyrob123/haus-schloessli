#!/usr/bin/env python3
"""Werkbank Schlössli: flüssig scrollen (Kriterium 34, Prüftor misst in Chromium: höchstens 2–3 Bilder über 50 ms, 95 % unter 34 ms).
Gemessen mit Chromium bei 2-facher CPU-Drosselung (4.11.2026). Aussehen und Bewegung bleiben, nur billiger (Kriterium 37: nur transform/opacity,
reduced-motion ruhig):
  - Absätze [data-a="worte"] kommen zeilenweise statt Wort für Wort herein: eine Ebene je Zeile statt je Wort (451 Wortebenen auf der Startseite);
    nach dem Hereinkommen fliesst der Absatz wieder frei (Zeilen werden aufgelöst).
  - Der Scroll-Takt (lauf) liest Seitenhöhe und Lage der Abschnitte höchstens alle 300 ms statt in jedem Bild (erzwungenes Layout).
  - Fotos blenden nur im Fenster ein, erst nach img.decode(); was beim Vorausladen ausserhalb fertig wird, steht ohne Einblenden da.
  - Endlos-Bewegungen (Wiegen, Pfeil, Welle, Glanz) halten ausserhalb des Fensters an (IntersectionObserver → animation-play-state).
  - will-change nur noch, wo sich etwas dauernd bewegt (Stapel, Fächer und Polaroids sind nach dem Hereinkommen still).
  - Fotos haben für Bildschirme mit einfacher Dichte eine kleinere Fassung (img/1x/, srcset 1x/2x): halbe bis Viertel-Dekodierarbeit;
    Handy und Retina laden wie bisher das Original. Die Grösse auf der Seite bleibt (width/height).
  (material/: Ordner mit content-visibility und Leiste ohne backdrop-filter, direkt in material_seite.py.)
Läuft in haus.nach_bau als letzter Schritt vor dem Rücksprung, wiederholbar.   python3 _werkbank/k34_fluss.py [<website/_werkbank>]"""
import os, re, sys

MARKE = '/* k34-fluss */'

# ---------- werkbank.js: Zeilen statt Wörter ----------
JS_ALT = "  function zeig(el) {\n    el.classList.add('da');"
JS_NEU = ("  /* k34-fluss: Absätze zeilenweise hereinholen (eine Ebene je Zeile statt je Wort), danach wieder frei fliessen lassen */\n"
          "  function zeilen(el) {\n"
          "    el.__zl = 1; var w = $$('.wt', el); if (!w.length) return;\n"
          "    el.classList.add('zl');\n"
          "    var reihen = [], oben = null;\n"
          "    w.forEach(function (s) { var t = s.offsetTop; if (oben === null || Math.abs(t - oben) > 4) { reihen.push([]); oben = t; } reihen[reihen.length - 1].push(s); });\n"
          "    for (var i = reihen.length - 1; i >= 0; i--) {\n"
          "      var r = doc.createRange(), l = doc.createElement('span'), z = reihen[i];\n"
          "      r.setStartBefore(z[0]); r.setEndAfter(z[z.length - 1]);\n"
          "      l.className = 'wl'; l.style.setProperty('--l', i); l.appendChild(r.extractContents()); r.insertNode(l);\n"
          "    }\n"
          "    void el.offsetWidth;\n"
          "    var vz = parseFloat(getComputedStyle(el).getPropertyValue('--vz')) || 0;\n"
          "    setTimeout(function () { $$('.wl', el).forEach(function (l) { while (l.firstChild) l.parentNode.insertBefore(l.firstChild, l); l.parentNode.removeChild(l); }); }, vz + reihen.length * 120 + 1300);\n"
          "  }\n"
          "  function zeig(el) {\n"
          "    if (!ruhig && !el.__zl && el.getAttribute('data-a') === 'worte') zeilen(el);\n"
          "    el.classList.add('da');")

# ---------- werkbank.js: Takt liest die Lage der Abschnitte nicht in jedem Bild (erzwungenes Layout je Scrollbild), sondern höchstens alle 300 ms ----------
JS2_ALT = "    abschn.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < vh * 0.42) an = i; });"
JS2_NEU = "    lauf.o.forEach(function (o, i) { if (o - y < vh * 0.42) an = i; });   /* k34-fluss */"
JS3_ALT = "    var y = scrollY, vh = innerHeight, h = doc.documentElement.scrollHeight - vh;\n"
JS3_NEU = ("    var y = scrollY, vh = innerHeight, jetzt = performance.now();\n"
           "    if (!lauf.t || jetzt - lauf.t > 300) { lauf.t = jetzt; lauf.h = doc.documentElement.scrollHeight; lauf.o = abschn.map(function (s) { return s ? s.getBoundingClientRect().top + y : 1e9; }); }   /* k34-fluss: Lage höchstens alle 300 ms lesen */\n"
           "    var h = lauf.h - vh;\n")

# ---------- werkbank.js: Fotos blenden nur im Fenster ein (vorher dekodiert); was ausserhalb fertig lädt, steht ohne Einblenden da ----------
JS4_ALT = "    function fertig(im) { if (im.__d) return; im.__d = 1; im.classList.add('da'); }\n"
JS4_NEU = ("    /* k34-fluss: Einblenden nur im Fenster und erst nach dem Dekodieren; ausserhalb (Vorausladen) ohne Einblenden, das sieht niemand */\n"
           "    var sicht = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) { es.forEach(function (e) { var im = e.target; im.__s = e.isIntersecting; if (im.__w) { im.__w = 0; fertig(im); } }); }, { rootMargin: '8% 0px' }) : null;\n"
           "    function fertig(im) {\n"
           "      if (im.__d) return;\n"
           "      if (sicht && im.__s === undefined) { im.__w = 1; return; }\n"
           "      im.__d = 1; if (sicht) sicht.unobserve(im);\n"
           "      if (ruhig || (sicht && !im.__s)) { im.classList.add('k34-sofort', 'da'); return; }\n"
           "      var z = function () { im.classList.add('da'); };\n"
           "      if (im.decode && im.naturalWidth) im.decode().then(z, z); else z();\n"
           "    }\n"
           "    if (sicht) alle.forEach(function (im) { sicht.observe(im); });\n")

# ---------- werkbank.js: Endlos-Bewegungen ausserhalb des Fensters anhalten ----------
JS_ENDE = ("\n/* k34-fluss: Endlos-Bewegungen (Glanz, Wiegen, Pfeil, Welle …) halten an, solange sie nicht im Fenster sind */\n"
           "(function () {\n"
           "  if (!('IntersectionObserver' in window) || !document.getAnimations) return;\n"
           "  function such() {\n"
           "    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('k34-ruh', !e.isIntersecting); }); }, { rootMargin: '12% 0px' }), da = [];\n"
           "    document.getAnimations().forEach(function (a) {\n"
           "      var ef = a.effect, t = ef && ef.target, z = ef && ef.getComputedTiming ? ef.getComputedTiming() : null;\n"
           "      if (!t || !z || z.iterations !== Infinity || da.indexOf(t) >= 0) return;\n"
           "      da.push(t); io.observe(t);\n"
           "    });\n"
           "  }\n"
           "  if (document.readyState === 'complete') setTimeout(such, 1200); else addEventListener('load', function () { setTimeout(such, 1200); });\n"
           "})();\n")

CSS = (MARKE + '\n'
       '.js img.ld.da.k34-sofort{animation:none}\n'
       '.k34-ruh,.k34-ruh::before,.k34-ruh::after{animation-play-state:paused!important}\n'
       '.stapel>*,.pk__b>*,.feedb__r>*,.tb__r>.abzug,.tb__r>.tel,.kt__tisch>*,.wg>*,.brief__a,.fst__s,.kopfzeile .zt .z>span,.da[data-drift]{will-change:auto!important}\n'
       '[data-a="worte"].zl .wt{opacity:1;transform:none;transition:none}\n'
       '[data-a="worte"] .wl{display:block;opacity:0;transform:translateY(.75em);transition:opacity .8s var(--e1),transform 1s var(--e1);transition-delay:calc(var(--vz,0ms) + var(--l)*120ms)}\n'
       '[data-a="worte"].da .wl{opacity:1;transform:none}\n'
       '@media (prefers-reduced-motion:reduce){[data-a="worte"] .wl{opacity:1!important;transform:none!important;transition:none!important}}\n'
       '@media print{[data-a="worte"] .wl{opacity:1!important;transform:none!important}}\n')


# ---------- Bilder: am Bildschirm mit einfacher Dichte eine kleinere Fassung (1x), am Handy und Retina wie bisher (2x); halbe Dekodierarbeit beim Scrollen ----------
BILDER = {   # Datei unter werkbank/: Breite der Fassung für einfache Bildschirmdichte (grösste gezeigte Breite bei 1440 und 1920 px, +8 %)
    'eigen/fo-analyse-h.webp': 544, 'eigen/fo-drucksachen.webp': 384, 'eigen/fo-etiketten.webp': 360, 'eigen/fo-gaeste.webp': 272,
    'eigen/fo-geprueft.webp': 248, 'eigen/fo-livre.webp': 360, 'eigen/fo-maison.webp': 384, 'eigen/fo-unterlagen.webp': 384,
    'eigen/fo-vorschlag.webp': 360, 'eigen/fo-website.webp': 544, 'eigen/fpo-20.webp': 256, 'eigen/fpo-35.webp': 256, 'eigen/fpo-40.webp': 256,
    'eigen/fpo-42.webp': 256, 'eigen/fpo-44.webp': 256, 'eigen/fpo-45.webp': 248, 'eigen/fpo-46.webp': 248, 'eigen/fpo-48.webp': 248,
    'eigen/unterschrift.webp': 184, 'img/a-apero-2400-webp.webp': 280, 'img/a-bar-900-webp.webp': 208, 'img/a-dessert-2400-webp.webp': 296,
    'img/a-lounge-1761-webp.webp': 280, 'img/a-platanen-2400-webp.webp': 272, 'img/a-regal-1920-webp.webp': 296, 'img/a-suppe-1536-webp.webp': 336,
    'img/a-tortelloni-900-webp.webp': 168, 'img/auftakt-h.webp': 224, 'img/auftakt.webp': 784, 'img/b-couvert.webp': 336,
    'img/b-platzkarte.webp': 328, 'img/b-visitenkarte.webp': 312, 'img/bf-h-01.webp': 376, 'img/bf-h-02.webp': 376, 'img/bf-h-03.webp': 376,
    'img/bf-h-04.webp': 376, 'img/bf-n-01.webp': 400, 'img/bf-n-03.webp': 408, 'img/bf-n-04.webp': 408, 'img/fb-0-0.webp': 256,
    'img/fb-0-1.webp': 256, 'img/fb-0-2.webp': 256, 'img/fb-0.webp': 576, 'img/fb-1-0.webp': 256, 'img/fb-1-1.webp': 256, 'img/fb-1-2.webp': 256,
    'img/fb-1.webp': 576, 'img/fb-2-0.webp': 256, 'img/fb-2-1.webp': 256, 'img/fb-2.webp': 576, 'img/fb-3-0.webp': 256, 'img/fb-3-1.webp': 256,
    'img/fb-3.webp': 576, 'img/fb-4-0.webp': 256, 'img/fb-4-1.webp': 256, 'img/fb-4.webp': 576, 'img/fb-5-0.webp': 256, 'img/fb-5-1.webp': 256,
    'img/fb-5.webp': 576, 'img/feed-geraet.webp': 488, 'img/feed-schirm.webp': 320, 'img/gf-abend.webp': 608, 'img/gf-bankett.webp': 608,
    'img/gf-berater.webp': 632, 'img/gf-gutschein.webp': 608, 'img/gf-kalender.webp': 608, 'img/gf-reservation.webp': 632, 'img/gf-see.webp': 608,
    'img/gf-wein-gang.webp': 632, 'img/gp-0.webp': 112, 'img/gp-1.webp': 112, 'img/gp-2.webp': 112, 'img/gp-3.webp': 112, 'img/hs-glas.webp': 480,
    'img/hs-morgen.webp': 480, 'img/hs-start.webp': 480, 'img/i-0.webp': 632, 'img/i-1.webp': 632, 'img/i-10.webp': 696, 'img/i-11.webp': 696,
    'img/i-2.webp': 632, 'img/i-3.webp': 696, 'img/i-4.webp': 696, 'img/i-5.webp': 696, 'img/i-6.webp': 696, 'img/i-7.webp': 696, 'img/i-8.webp': 696,
    'img/i-9.webp': 696, 'img/ins-bild-bureau-2.webp': 760, 'img/ins-bild-bureau.webp': 760, 'img/ins-bild-carte-2.webp': 760,
    'img/ins-bild-carte.webp': 760, 'img/ins-bild-imprimerie-2.webp': 760, 'img/ins-bild-imprimerie.webp': 760, 'img/ins-bild-livre-2.webp': 760,
    'img/ins-bild-livre.webp': 760, 'img/ins-bild-maison.webp': 760, 'img/ins-bild-reception-2.webp': 760, 'img/ins-bild-reception.webp': 760,
    'img/ins-bild-registre-2.webp': 760, 'img/ins-bild-registre.webp': 760, 'img/ins-geraet.webp': 936, 'img/k-u01.webp': 216, 'img/k-u02.webp': 208,
    'img/k-u03.webp': 208, 'img/k-u04.webp': 208, 'img/k-u05.webp': 216, 'img/k-u06.webp': 216, 'img/ki-geraet-imprimerie.webp': 832,
    'img/ki-geraet-livre.webp': 712, 'img/ki-geraet-reception-2.webp': 712, 'img/ki-geraet-reception.webp': 832, 'img/ki-team.webp': 688,
    'img/ml-01.webp': 168, 'img/ml-02.webp': 168, 'img/ml-03.webp': 168, 'img/ml-04.webp': 168, 'img/ml-05.webp': 168, 'img/ml-06.webp': 168,
    'img/pdf-0.webp': 376, 'img/pdf-1.webp': 320, 'img/pdf-2.webp': 328, 'img/pdf-3.webp': 368, 'img/robert.webp': 184, 'img/sag-haus.webp': 584,
    'img/staender.webp': 728, 'img/startseite-h.webp': 256,
}
SEITEN = ('werkbank/index.html', 'werkbank/ki.html')
MASS_DAZU = ('img/ki-geraet-', 'img/ki-team.webp')   # ohne width/height im Bau (sb_ki.py), CSS setzt width:100% und height: Mass des Originals dazu, damit die Grösse bleibt


def _schreib(f, alt, neu):
    if neu != alt:
        open(f, 'w', encoding='utf-8').write(neu)
        return 1
    return 0


def anwenden(root):
    n = 0
    wb = os.path.join(root, 'werkbank')
    f = os.path.join(wb, 'werkbank.js')
    if os.path.exists(f):
        s = open(f, encoding='utf-8').read()
        neu = s.replace(JS_ALT, JS_NEU, 1).replace(JS2_ALT, JS2_NEU, 1).replace(JS3_ALT, JS3_NEU, 1).replace(JS4_ALT, JS4_NEU, 1)
        neu = neu.split(JS_ENDE)[0].rstrip('\n') + '\n' + JS_ENDE
        n += _schreib(f, s, neu)
    f = os.path.join(wb, 'werkbank.css')
    if os.path.exists(f):
        s = open(f, encoding='utf-8').read()
        neu = re.sub(re.escape(MARKE) + r'.*\Z', '', s, flags=re.S).rstrip() + '\n' + CSS
        n += _schreib(f, s, neu)
    for seite in SEITEN:
        f = os.path.join(root, seite)
        if os.path.exists(f):
            s = open(f, encoding='utf-8').read()
            n += _schreib(f, s, re.sub(r'<img\b[^>]*>', lambda m: _einfach(m.group(0), wb), s))
    return n


def _einfach(tag, wb):
    """<img src="img/x.webp" width height> → srcset mit 1x-Fassung (img/1x/x.webp) und dem Original als 2x. Grösse bleibt durch width/height."""
    m = re.search(r'\ssrc="([^"]+)"', tag)
    if not m or m.group(1) not in BILDER or 'srcset=' in tag or 'data-src=' in tag or not ((' width=' in tag and ' height=' in tag) or m.group(1).startswith(MASS_DAZU)):
        return tag
    pfad = m.group(1)
    q = os.path.join(wb, pfad)
    if not os.path.exists(q):
        return tag
    d, name = os.path.split(pfad)
    klein = d + '/1x/' + name
    z = os.path.join(wb, klein)
    if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(q):
        from PIL import Image
        im = Image.open(q)
        breite = BILDER[pfad]
        if im.width <= breite * 1.15:
            return tag
        im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB')
        os.makedirs(os.path.dirname(z), exist_ok=True)
        im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS).save(z, 'WEBP', quality=86, method=5)
    mass = ''
    if ' width=' not in tag:
        from PIL import Image
        w, h = Image.open(q).size
        mass = f' width="{w}" height="{h}"'
    return tag.replace(m.group(0), f'{m.group(0)} srcset="{klein} 1x, {pfad} 2x"{mass}', 1)


if __name__ == '__main__':
    print('k34-fluss:', anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Dateien')
