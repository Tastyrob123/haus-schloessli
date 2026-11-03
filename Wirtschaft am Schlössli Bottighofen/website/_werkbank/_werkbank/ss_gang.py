#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli: Schweizer Schreibung (Nachtbau 3.11.2026; an Stelle von du_gang.py des Culinarium, das in die Ihr-Form umschrieb).
Das Schlössli siezt, wie der Kit und die Vorlagen; hier wird nur «ß» zu «ss» in jedem sichtbaren Text der Seiten des Kern-Reviers (werkbank/, befund/),
in Text, Attributen und Skripttexten. Adressen, Bilder und Schriften enthalten kein ß. Mehrfach anwendbar.   python3 _werkbank/ss_gang.py"""
import glob, os

W = os.path.dirname(os.path.abspath(__file__))


def anwenden(root=None):
    root = root or os.path.dirname(W)
    n = 0
    for p in glob.glob(os.path.join(root, 'werkbank', '**', '*.html'), recursive=True) + glob.glob(os.path.join(root, 'werkbank', '*.js')) + \
            [os.path.join(root, 'befund', 'index.html')]:
        if not os.path.exists(p):
            continue
        a = open(p, encoding='utf-8').read()
        b = a.replace('ß', 'ss').replace('ẞ', 'SS').replace('mit Probe-Daten', 'mit Beispieldaten')
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    return n


if __name__ == '__main__':
    print('ss statt ß in', anwenden(), 'Dateien')
