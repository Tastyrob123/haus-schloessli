#!/usr/bin/env python3
"""Feste Druckschnitte von Open Sans für die Werkbank der Wirtschaft am Schlössli (Nachtbau 3.11.2026; Bauart wie druckschrift.py des Culinarium).
Der Kit (schriften.py) setzt nur die Achse «wght» fest; Open Sans hat dazu «wdth». Hier werden alle Achsen fest gesetzt (wdth 100), sonst schreibt
Chromium die Schrift als «Type 3» in die PDF.   python3 _werkbank/druckschrift.py → _werkbank/fonts/OpenSans-*.ttf (nach schriften.py)"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

W = os.path.dirname(os.path.abspath(__file__))
Q = os.path.join(os.path.dirname(os.path.dirname(W)), 'assets', 'fonts')
Z = os.path.join(W, 'fonts'); os.makedirs(Z, exist_ok=True)
SCHNITTE = [('OpenSans-var.woff2', 'OpenSans-Regular', 'Open Sans', 'Regular', 400),
            ('OpenSans-var.woff2', 'OpenSans-Medium', 'Open Sans', 'Medium', 500)]


def bau():
    for quelle, ziel, fam, stil, g in SCHNITTE:
        f0 = TTFont(os.path.join(Q, quelle))
        achsen = {a.axisTag: (g if a.axisTag == 'wght' else (100 if a.axisTag == 'wdth' else a.defaultValue)) for a in f0['fvar'].axes} if 'fvar' in f0 else {}
        f = instancer.instantiateVariableFont(f0, achsen, inplace=False) if achsen else f0
        for rec in f['name'].names:
            if rec.nameID in (1, 16): rec.string = fam
            if rec.nameID in (2, 17): rec.string = stil
            if rec.nameID == 4: rec.string = f'{fam} {stil}'
            if rec.nameID == 6: rec.string = f'{fam.replace(" ", "")}-{stil}'
        f['OS/2'].usWeightClass = g
        f.flavor = None
        f.save(os.path.join(Z, ziel + '.ttf'))
        print(ziel + '.ttf', 'variabel' if 'fvar' in f else 'fest')


if __name__ == '__main__':
    bau()
