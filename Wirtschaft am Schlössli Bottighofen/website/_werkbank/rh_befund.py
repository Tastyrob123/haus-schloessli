#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus, Kapitel «Was wir gefunden haben» mit «Die Lupe» (Werkbank-Chat 17.10.2026; Robert wählte am 17.10. «Die Lupe»,
Baustein ~/Desktop/Website-Projekte/_Befund-Vorschlaege/lupe/, dort EINBAU.md; nur gelesen und aufgerufen, nichts darin geändert).
Inhalt bei jedem Bau frisch aus der heutigen Potenzialanalyse des Hauses (potenzialanalyse/_bau/inhalt.py, stellen/bahnen.json, site/assets/…)
über lupe/daten/ruedihus.py; Kleid lupe/kleider/ruedihus.css (Karte wie der Schpiszettel, Wappen über der Kante, Bühne als dunkle Stube).
Kein Satz und keine Zahl steht hier; nur Kopf und der Weg zur ganzen Analyse.
  abschnitt(k, kopfk)  → <section id="k1"> mit Kopf, Lupe und Knopf zur Analyse
  CSS                   Grundgerüst und Kleid der Lupe (nach dem ersten abschnitt()-Aufruf gesetzt)"""
import os, sys

LUPE = os.environ.get('RH_LUPE') or os.path.expanduser('~/Desktop/Website-Projekte/_Befund-Vorschlaege/lupe')   # RH_LUPE: freigegebener Stand, wenn der Baustein gerade in Arbeit ist (18.10.2026)
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
ANALYSE = 'https://ruedihus-analyse.tastystudios.ch/'
CSS = ''
FUNDE = []   # Rahmen, die nicht genau sitzen (lupe.rahmen_pruefen); vor dem Melden beheben


def _ohne_sprung(js):
    """Robert 19.10.2026 00:53: «Wenn ich auf den Weiter-Button klicke, dann werde ich immer automatisch in so eine gewisse Grundposition zurückgezwungen.»
    Der Baustein schob die Seite beim Blättern an den Kopf des Befunds, sobald dieser über dem Rand lag. Im Ruedihus bleibt die Seite jetzt, wo sie ist."""
    alt = "if(klick){var r=B.getBoundingClientRect();if(r.top<0)window.scrollBy({top:r.top-12,behavior:'smooth'})}"
    js = js.replace(alt, '')   # seit 19.10.2026 00:57 auch im Baustein selbst entfernt; dann bleibt hier nichts zu tun
    if 'window.scrollBy(' in js or 'scrollIntoView(' in js:
        raise SystemExit('rh_befund: der Befund verschiebt beim Blättern wieder die Seite (scrollBy/scrollIntoView im Baustein)')
    return js


def _laden():
    if LUPE not in sys.path:
        sys.path.insert(0, LUPE)
    import lupe
    from daten import ruedihus as LD
    return lupe, LD


def abschnitt(k, kopfk):
    global CSS
    lupe, LD = _laden()
    befunde = LD.befunde()   # jedes Mal frisch aus der heutigen Analyse
    FUNDE[:] = lupe.rahmen_pruefen(befunde)
    for f in FUNDE:
        print('Befund, Rahmen:', f)
    lupe.bilder(befunde, os.path.join(ROOT, 'werkbank', 'img'), 'img/')   # schreibt lu-*.webp, löscht nichts
    CSS = '\n/* ---------- Befund «Die Lupe» (rh_befund.py, Baustein _Befund-Vorschlaege/lupe) ---------- */\n' + lupe.css(LD.KLEID['name'])
    n = len(befunde)
    zahl = {13: 'dreizehn', 12: 'zwölf', 11: 'elf', 10: 'zehn', 9: 'neun', 8: 'acht', 7: 'sieben', 6: 'sechs', 5: 'fünf', 4: 'vier', 3: 'drei'}.get(n, str(n))
    return f'''
<section class="fl fl--nacht tapete-leicht blatt lu-kapitel" id="k1" tabindex="-1">
  <div class="in">
    {kopfk('k1', ['Ihre Seite,', 'genau gelesen.'], f'Bevor etwas Neues entstand, habe ich Ihre heutige Website gelesen wie ein Gast, Seite für Seite, mit Karten und Unterlagen daneben. Hier stehen {zahl} Stellen, an denen ein Gast hängen bleibt, jede mit ihrem Beleg; die übrigen stehen in der Analyse.')}
    {lupe.abschnitt(befunde, LD.KLEID)}
  </div>
  {_ohne_sprung(lupe.js())}
</section>'''
