#!/usr/bin/env python3
"""Das Kartenpult · Wirtschaft am Schlössli: feste Schnitte aus den Schriften der Website (Nachtbau 3.11.2026, Muster der Tafel im Schäfli).
Chromium bettet variable Schriften im PDF als «Type 3» ein; die Apple-Vorschau zeigt sie dann weich. Darum setzt der Satz feste Schnitte
(TrueType je Stärke, aus der variablen Schrift der Website instanziiert, Lizenz SIL OFL wie das Original).
Quelle: website/assets/fonts/ (dieselben Dateien, die das Werkzeug unter /assets/fonts/ ausliefert): Open Sans (Titel, Versalien wie die Wortmarke),
Instrument Sans (Lauf), DM Mono (Gerichte, Zahlen, Etiketten).
    python3 _werkzeuge/carte/fonts_statisch.py      → fonts/OpenSans-<stärke>.ttf, fonts/InstrumentSans-<stärke>.ttf, fonts/DMMono-400.ttf
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HIER = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HIER, 'fonts')
Q = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website', 'assets', 'fonts')
SCHNITTE = {
    'OpenSans-var.woff2': [('OpenSans-300', {'wght': 300, 'wdth': 100}), ('OpenSans-400', {'wght': 400, 'wdth': 100})],
    'InstrumentSans-normal-400_600.woff2': [('InstrumentSans-400', {'wght': 400}), ('InstrumentSans-500', {'wght': 500}), ('InstrumentSans-600', {'wght': 600})],
}
if __name__ == '__main__':
    os.makedirs(F, exist_ok=True)
    for quelle, liste in SCHNITTE.items():
        for name, achsen in liste:
            t = TTFont(os.path.join(Q, quelle))
            da = {a.axisTag for a in t['fvar'].axes} if 'fvar' in t else set()
            s = instancer.instantiateVariableFont(t, {k: v for k, v in achsen.items() if k in da}, updateFontNames=False) if da else t
            s.flavor = None
            s.save(os.path.join(F, name + '.ttf'))
            print(name)
    t = TTFont(os.path.join(Q, 'DMMono-normal-400.woff2')); t.flavor = None; t.save(os.path.join(F, 'DMMono-400.ttf')); print('DMMono-400')
