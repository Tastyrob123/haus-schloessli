# schriften.py · feste Schriftschnitte für den Druck der Karten: python3 _karten/schriften.py  →  _karten/schriften/*.ttf
# Grund (Master Website-Bau Abschnitt 8, Carlton 08.10.2026): Chromium schreibt variable Schriften als «Type 3» in die PDF,
# die Apple-Vorschau zeichnet sie weich. Feste Schnitte landen als TrueType. Prüfen: pdffonts <datei.pdf>, kein «Type 3».
# Quelle: die Schriften des Markenbuchs (Station 5), dieselben wie auf der Website.
import pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HIER = pathlib.Path(__file__).resolve().parent
Q = HIER.parent / '_kette' / '05-markenbauer' / 'marke' / 'schriften'
Z = HIER / 'schriften'
Z.mkdir(exist_ok=True)
NAME = {300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold'}


def fest(quelle, familie, achsen, g):
    f = TTFont(Q / quelle)
    f = instancer.instantiateVariableFont(f, dict(achsen, wght=g), inplace=False)
    f.flavor = None
    for rec in f['name'].names:          # eigener Name je Schnitt, sonst hält die PDF sie für dieselbe Schrift
        if rec.nameID in (1, 16): rec.string = familie + ' Druck'
        if rec.nameID in (2, 17): rec.string = NAME[g]
        if rec.nameID == 4: rec.string = f'{familie} Druck {NAME[g]}'
        if rec.nameID == 6: rec.string = f'{familie}Druck-{NAME[g]}'
    f['OS/2'].usWeightClass = g
    ziel = Z / f'{familie}-{NAME[g]}.ttf'
    f.save(ziel)
    print(ziel.name, ziel.stat().st_size // 1024, 'KB')


for g in (300, 400, 500):
    fest('OpenSans-var.ttf', 'OpenSans', {'wdth': 100}, g)
for g in (400, 600):
    fest('InstrumentSans-normal-400_600.woff2', 'InstrumentSans', {}, g)
f = TTFont(Q / 'DMMono-normal-400.woff2'); f.flavor = None; f.save(Z / 'DMMono-Regular.ttf'); print('DMMono-Regular.ttf')
