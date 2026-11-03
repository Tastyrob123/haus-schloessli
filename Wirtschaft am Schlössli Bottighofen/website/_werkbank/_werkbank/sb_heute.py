#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli: «Heute und neu» (Nachtbau 3.11.2026; Bauart sb_heute.py des Culinarium). «Heute» ist die heutige Website
schloessli-bottighofen.ch, aufgenommen am 19.10.2026 für die Werkbank des alten Schlössli-Stands (ansichten/Vorher/<slug>-alt.jpg, Rechner 1440, aus dem
Ordner des Spähers und der Werkbank vom 21.10.); «neu» die Aufnahmen der neuen Seite (ansichten/Rechner, ansicht_lang.js). Nichts wird online abgerufen.
   python3 _werkbank/sb_heute.py  → ansichten/Vorher/<slug>-neu.jpg frisch aus ansichten/Rechner (gelesen von H.VORHER im Kit-Bau)"""
import os
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(W, 'ansichten', 'Vorher')
PAARE = [('startseite', 'Rechner/Startseite.jpg'), ('karte', 'Rechner/Die Karte.jpg'), ('events', 'Rechner/Events.jpg'),
         ('team', 'Rechner/Über uns.jpg'), ('kontakt', 'Rechner/Kontakt.jpg')]


def bau():
    os.makedirs(Z, exist_ok=True)
    for slug, neu in PAARE:
        a, n = os.path.join(Z, slug + '-alt.jpg'), os.path.join(W, 'ansichten', neu)
        if not (os.path.exists(a) and os.path.exists(n)):
            print('fehlt', slug); continue
        breite = Image.open(a).width
        im = Image.open(n).convert('RGB')
        if im.width != breite:   # beide Hälften gleich gross, sonst springt der Schieber
            im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
        im.save(os.path.join(Z, slug + '-neu.jpg'), quality=90)
        print('Vorher', slug)


if __name__ == '__main__':
    bau()
