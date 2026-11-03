#!/usr/bin/env python3
"""Ideen für Papier: Drucksachen und Zündholz-Etiketten des Landgasthofs Ruedihus.
   PYTHONPATH=<Kit> python3 _werkbank/papier.py "<Projekt>"

Alle Angaben stammen aus den Karten und von der Website des Hauses (siehe _recherche/Fakten-Blatt.md, daten.py).
Was von Tasty Studios ist, steht in MEINS. Keine CSS-Masken und keine weichen Schatten im Druck: Formen sind Pfade."""
import os, sys
import papier_kern as P
from papier_kern import t, lin, linv, rahmen, kasten, foto, blatt, hz, hw, tx, bogen_text, hzz, hwz, stern, strich, etikett, e
from kern import H, ROOT
sys.path.insert(0, ROOT)
import daten as D

F = H.FARBEN
RUSS, TIEF, HOLZ, PAPIER, BLATT, KERZE, MESSING, TAUPE, TINTE, LICHT, ROT, OFEN = F['nacht'], F['tief'], F['blau'], F['papier'], F['weiss'], F['gold'], F['messing'], F['taupe'], F['tinte'], H.LICHT, H.GERANIE, H.OFEN
MUSTER = f'{H.MUSTER} 50% 0/9mm auto'
# Couvert: dasselbe Muster, so kräftig gedruckt, dass man es auf dem Umschlag sieht (wie die Tapete des Carlton-Europe)
assert "stroke-opacity='.08'" in H.MUSTER
MUSTER_COUVERT = H.MUSTER.replace('"', '&quot;').replace("stroke-opacity='.08'", "stroke-opacity='.12'") + ' 50% 0/15mm auto'
ADR = 'Hinder de Büele 6 · 3718 Kandersteg'
TEL = '(+41) 033 675 81 81'
MAIL = 'info@doldenhorn.ch'

MEINS = ['Bildzeilen der Ansichtskarten', 'Alle Sätze auf der Karte zur Zimmermappe', 'Auf den Anhängern: die Wörter «Zimmer» und «Nr.»', 'Feldnamen auf Gutschein und Tischkarte, das Wort «Reserviert»', 'Auswahl und Kürzung der Sätze auf dem Blatt zur Hausgeschichte',
         'Sätze zu den Zündholz-Etiketten']


# ============================================================ Ansichtskarten (A6 quer)
ANSICHT = [   # Robert 10.10.2026: Ansichtskarten zeigen Haus und Landschaft, der Titel nennt den Ort wie auf einer echten Karte
    ('haus-sommer', 'Landgasthof Ruedihus', 'die Terrasse unter den Bäumen', '50% 50%', 'Kandersteg'),
    ('haus-wiese', 'Kandersteg', 'das Haus von 1753 über der Blumenwiese', '50% 45%', 'Berner Oberland'),
    ('haus-winter', 'Winter in Kandersteg', 'das Haus im Schnee, dahinter die Berge', '50% 50%', 'Berner Oberland'),
    ('haus-baum', 'Seit 1753', 'das Haus zwischen zwei Bäumen', '50% 50%', 'Kandersteg'),
]


def ansichtskarte(key, name, zeile, lage, ort='Kandersteg'):
    v = (foto(key, 5, 5, 138, 95, lage)
         + f'<div class="abs kerbe" style="left:5mm;bottom:5mm;background:{BLATT}"><b>{e(name)}</b><span>{e(ort)}</span></div>')
    adr = ''.join(lin(84, 55 + i * 11, 54, 'rgba(42,26,14,.42)', .2) for i in range(4))
    marke = f'<i class="abs" style="left:116mm;top:8mm;width:22mm;height:27mm;border:.25mm dashed {MESSING}"></i>' + hz(127, 12.5, 13, MESSING)
    r = (linv(74, 12, 81, MESSING, .25) + adr + marke
         + hz(10, 9, 12, HOLZ, False)
         + t(10, 28.5, e(name), 's', f'font-size:5.2mm;color:{HOLZ}') + t(10, 36, e(zeile[0].upper() + zeile[1:]), '', f'font-size:3mm;line-height:1.45;color:{TINTE}', 56)
         + t(10, 86.5, 'Landgasthof Ruedihus', 'm', f'font-size:1.9mm;letter-spacing:.16em;color:{TINTE}') + t(10, 90.6, e(ADR), 'm', f'font-size:1.9mm;letter-spacing:.16em;color:{TINTE};opacity:.75'))
    return [blatt(148, 105, v, '', f'background:{BLATT}'), blatt(148, 105, r, '', 'background:#fffaf1')]


# ============================================================ Gutschein (DIN lang quer)
# Wortlaut: Karte der Chäs- und Wystube, «Geschenkgutscheine»
def gutschein():
    v = (kasten(0, 0, 210, 100, f'background:{RUSS} {MUSTER}') + rahmen(5, KERZE, 2.5, .3) + hz(40, 19, 44, KERZE)
         + t(78, 26, 'Gutschein', 's', f'font-size:21mm;line-height:1;color:{PAPIER}')
         + lin(79, 55, 22, KERZE, .4)
         + t(79, 60.5, 'Zu Gast – bei Freunden', 's', f'font-size:5.4mm;color:{LICHT}')
         + t(79, 79, 'Landgasthof Ruedihus · Kandersteg · seit 1753', 'm', f'font-size:2.3mm;color:{KERZE}'))
    def feld(x, y, b, name):
        return t(x, y, name, 'm', f'font-size:2.25mm;color:{TAUPE}') + lin(x, y + 11.5, b, 'rgba(42,26,14,.45)', .2)
    r = (rahmen(5, MESSING, 2.5, .3)
         + feld(14, 13, 54, 'Für') + feld(74, 13, 54, 'Von')
         + feld(14, 31, 114, 'Gutschein für') + lin(14, 53.5, 114, 'rgba(42,26,14,.45)', .2)
         + feld(14, 62, 34, 'Wert CHF') + feld(54, 62, 34, 'Gültig bis') + feld(94, 62, 34, 'Nr.')
         + linv(138, 13, 74, MESSING, .25)
         + hz(146, 12, 13, HOLZ, False)
         + t(146, 33, 'Landgasthof Ruedihus', 's', f'font-size:4.3mm;color:{HOLZ}')
         + t(146, 42, 'Hinder de Büele 6<br>3718 Kandersteg', '', f'font-size:3.2mm;line-height:1.45;color:{TINTE}')
         + t(146, 56, TEL + '<br>' + MAIL, '', f'font-size:3.2mm;line-height:1.45;color:{TINTE}')
         + t(146, 72.5, 'Gerne stellen wir Ihnen einen Geschenkgutschein aus.', '', f'font-size:2.7mm;line-height:1.4;color:{TINTE};opacity:.8', 50))
    return [blatt(210, 100, v, '', f'background:{RUSS}'), blatt(210, 100, r, '', f'background:{BLATT}')]


# ============================================================ Tischkarte «Reserviert» (A6 quer, Vorder- und Rückseite eines Aufstellers)
def tischkarte():
    def feld(x, y, b, name):
        return t(x, y, name, 'm', f'font-size:2.3mm;color:{TAUPE}') + lin(x, y + 12, b, 'rgba(42,26,14,.45)', .2)
    v = (rahmen(5, MESSING, 2.5, .3) + hz(74, 11, 15, MESSING)
         + t(0, 35, 'Reserviert', 's c', f'font-size:15mm;line-height:1;color:{HOLZ}', 148)
         + lin(65, 54, 18, MESSING, .4)
         + feld(30, 60, 52, 'Für') + feld(90, 60, 28, 'Um')
         + t(0, 89.5, 'Chäs-u Wystube · Jungestube · Ofestübli · Egger- und Stettlerstube', 'm c', f'font-size:1.95mm;color:{TINTE};opacity:.78', 148))
    r = (kasten(0, 0, 148, 105, f'background:{RUSS} {MUSTER}') + rahmen(5, KERZE, 2.5, .3)
         + t(18, 20, '«Sie suchen vergebens Campari, Orangensaft, Salzwasserfische, Cognac oder Cola.»', 's c', f'font-size:6.6mm;line-height:1.24;color:{LICHT}', 112)
         + lin(65, 68, 18, KERZE, .4)
         + t(24, 73.5, 'Unser oberstes Prinzip ist: Nur ausgesuchte Produkte aus der Schweiz verwenden.', 'c', f'font-size:3.3mm;line-height:1.5;color:{PAPIER}', 100)
         + t(0, 91.5, 'Landgasthof Ruedihus · Kandersteg', 'm c', f'font-size:1.95mm;color:{KERZE}', 148))
    return [blatt(148, 105, v, '', f'background:{BLATT}'), blatt(148, 105, r, '', f'background:{RUSS}')]


# ============================================================ Untersetzer (rund, 100 mm)
def ring(text, r, farbe, groesse, oben=True, sperr=.2, ident='r'):
    d = f'M{50 - r} 50 A{r} {r} 0 0 1 {50 + r} 50' if oben else f'M{50 - r} 50 A{r} {r} 0 0 0 {50 + r} 50'
    return (f'<path id="{ident}" d="{d}" fill="none"/><text font-family="DM Mono" font-size="{groesse}" letter-spacing="{sperr}em" fill="{farbe}" text-anchor="middle">'
            f'<textPath href="#{ident}" startOffset="50%">{e(text.upper())}</textPath></text>')


def rund_svg(innen, grund):
    return f'<svg class="abs" style="inset:0;width:100mm;height:100mm" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="{grund}"/>{innen}</svg>'


def untersetzer():
    kreis = lambda r, f, d=.3: f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="{f}" stroke-width="{d}"/>'
    eins = rund_svg(kreis(45.5, KERZE) + kreis(44, KERZE, .15) + hzz(50, 20, 34, KERZE) + ring('Landgasthof Ruedihus · Kandersteg', 38.5, PAPIER, 3, False, .24, 'u1'), RUSS)
    zwei = rund_svg(kreis(45.5, MESSING) + kreis(44, MESSING, .15) + tx(50, 54, '1753', 24, HOLZ) + strich(18, 63, 50, MESSING)
                    + tx(50, 70.5, 'DURCH PETER GERMANN ERBAUT', 2.6, TAUPE, 'm', .2) + ring('Landgasthof Ruedihus', 38.6, TAUPE, 3, True, .26, 'u2'), BLATT)
    drei = rund_svg(kreis(45.5, LICHT) + kreis(44, LICHT, .15) + tx(50, 46, 'Zu Gast –', 11.5, PAPIER) + tx(50, 60, 'bei Freunden', 11.5, LICHT)
                    + strich(18, 66, 50, LICHT) + ring('Landgasthof Ruedihus · Kandersteg', 38.6, LICHT, 2.9, True, .24, 'u3'), ROT)
    zl = ['Sie suchen vergebens', 'Campari, Orangensaft,', 'Salzwasserfische,', 'Cognac oder Cola.']
    vier = rund_svg(kreis(45.5, HOLZ) + kreis(44, HOLZ, .15) + ''.join(tx(50, 38 + i * 8.2, z, 6.2, HOLZ) for i, z in enumerate(zl))
                    + strich(18, 68.5, 50, HOLZ) + ring('Nur ausgesuchte Produkte aus der Schweiz', 38.6, HOLZ, 2.7, True, .2, 'u4'), LICHT)
    return [blatt(100, 100, x, '', 'background:transparent', 'kreis') for x in (eins, zwei, drei, vier)]


# ============================================================ Die Geschichte des Hauses (A5 hoch, zwei Seiten)
# Wortlaut: Karte der Chäs- und Wystube («GESCHICHTE · Das RUEDIHUS») über daten.py der Website
def geschichte():
    v = (foto('haus-wiese', 0, 0, 148, 96, '50% 40%') + kasten(0, 96, 148, .7, f'background:{MESSING}')
         + hz(74, 104, 17, MESSING)
         + t(0, 128, 'Das Ruedihus', 's c', f'font-size:13mm;line-height:1.05;color:{HOLZ}', 148)
         + lin(65, 146.5, 18, MESSING, .4)
         + t(20, 152, 'wurde 1753 durch Peter Germann erbaut. Es gilt als Spitzenleistung der Zimmermannskunst im 18. Jahrhundert.', 'c', f'font-size:3.9mm;line-height:1.5;color:{TINTE}', 108)
         + t(20, 176, e(D.GESCHICHTE[1]), 'c', f'font-size:3mm;line-height:1.5;color:{TINTE};opacity:.86', 108)
         + t(0, 200.5, 'Landgasthof Ruedihus · Kandersteg', 'm c', f'font-size:2mm;color:{TAUPE}', 148))
    y0 = 32
    jahre = [('1753', D.SAGE), ('1908', D.BRAND + ' ' + D.SCHWELLE), ('1990', 'Am 21. Dezember 1990 konnten wir das Haus erwerben. Im Februar 1991 haben wir den Betrieb wiedereröffnet.'),
             ('2000', 'Kontinuierlich haben wir das Haus restauriert, was mit der besonderen Auszeichnung, historisches Hotel Restaurant des Jahres 2000, gewürdigt wurde.')]
    y, zl = 32, ''
    for jahr, text in jahre:
        hoehe = (len(text) // 44 + 1) * 5.5
        zl += t(16, y - 1.5, jahr, 's', f'font-size:11.5mm;line-height:1;color:{KERZE}') + t(52, y, e(text), '', f'font-size:3.55mm;line-height:1.5;color:{PAPIER}', 80)
        y += max(hoehe, 13) + 8
        zl += lin(16, y - 4, 116, 'rgba(201,133,67,.4)', .2)
    r = (kasten(0, 0, 148, 210, f'background:{RUSS} {MUSTER}') + rahmen(5, KERZE, 2.5, .25)
         + t(16, 13, 'Geschichte', 's', f'font-size:8mm;color:{LICHT}') + zl
         + t(16, 180, e(D.WICHTIG), 's', f'font-size:4.6mm;line-height:1.3;color:{LICHT}', 116)
         + t(0, 199.5, 'Familie Maeder und ihre Crew', 'm c', f'font-size:2mm;color:{KERZE}', 148))
    return [blatt(148, 210, v, '', f'background:{BLATT}'), blatt(148, 210, r, '', f'background:{RUSS}')]


# ============================================================ Briefpapier
def briefpapier():
    bogen = (hz(105, 12, 15, MESSING) + hw(105, 35, 70, HOLZ) + lin(25, 47, 160, MESSING, .25)
             + t(25, 53, f'Landgasthof Ruedihus · {ADR}', 'm', f'font-size:1.85mm;color:{TINTE};opacity:.7')
             + lin(4, 105, 5, 'rgba(42,26,14,.5)', .15) + lin(4, 210, 5, 'rgba(42,26,14,.5)', .15)
             + lin(25, 273, 160, MESSING, .25) + t(0, 277, f'Landgasthof Ruedihus · {e(ADR)}', 'm c', f'font-size:1.95mm;color:{TINTE}', 210)
             + t(0, 281.6, f'{TEL} · {MAIL} · doldenhorn-ruedihus.ch', 'm c', f'font-size:1.95mm;color:{TINTE};opacity:.78', 210))
    couvert = (kasten(0, 0, 229, 114, f'background:{RUSS} {MUSTER_COUVERT}') + hz(15, 11, 11, KERZE, False) + hw(31, 14.5, 58, PAPIER, False) + t(31, 22.5, e(ADR), 'm', f'font-size:2.05mm;color:{KERZE}')
               + rahmen(4.5, KERZE, 2, .25)
               + f'<i class="abs" style="left:122mm;top:50mm;width:92mm;height:42mm;background:#fffaf1;border-radius:1.6mm"></i>')
    karte_v = kasten(0, 0, 85, 55, f'background:{RUSS} {MUSTER}') + rahmen(3.2, KERZE, 1.6, .22) + hz(42.5, 8, 19, KERZE) + hw(42.5, 37.5, 50, PAPIER) + t(0, 44.6, 'Kandersteg · seit 1753', 'm c', f'font-size:1.9mm;color:{KERZE}', 85)
    karte_r = (hz(8, 7, 9, HOLZ, False) + t(8, 21.5, 'Familie Maeder', 's', f'font-size:5mm;color:{HOLZ}') + t(8, 28.6, 'Ihre Gastgeber', 'm', f'font-size:2mm;color:{TAUPE}')
               + lin(8, 34, 14, MESSING, .3)
               + t(8, 37.5, f'Landgasthof Ruedihus<br>{e(ADR)}', '', f'font-size:2.55mm;line-height:1.5;color:{TINTE}')
               + t(8, 46.2, f'{TEL} · {MAIL}', '', f'font-size:2.55mm;color:{TINTE}'))
    return [blatt(210, 297, bogen, '', 'background:#fffdf8'), blatt(229, 114, couvert, '', f'background:{RUSS}'),
            blatt(85, 55, karte_v, '', f'background:{RUSS}'), blatt(85, 55, karte_r, '', f'background:{BLATT}')]


# ============================================================ Zündholz-Etiketten (56 × 38 mm quer, 38 × 56 mm hoch)
def form(b, h, r=2.2, a=1):
    return f'M{a + r} {a}H{b - a - r}A{r} {r} 0 0 1 {b - a} {a + r}V{h - a - r}A{r} {r} 0 0 1 {b - a - r} {h - a}H{a + r}A{r} {r} 0 0 1 {a} {h - a - r}V{a + r}A{r} {r} 0 0 1 {a + r} {a}Z'


def zh(ident, quer, grund, rand, innen, name, satz):
    b, h = (56, 38) if quer else (38, 56)
    f = form(b, h)
    return etikett(ident, b, h, f, f'<path d="{f}" fill="{grund}"/><path d="{form(b, h, 1.2, 3)}" fill="none" stroke="{rand}" stroke-width=".3"/>' + innen, name, satz)


def etiketten():
    E = []
    E.append(zh('e01', True, RUSS, KERZE, hzz(12, 9.5, 12.5, KERZE) + tx(36.5, 18.5, 'RUEDIHUS', 4.5, PAPIER, 's', .08) + strich(12, 21.6, 36.5, KERZE, .3) + tx(36.5, 27, 'KANDERSTEG · 1753', 1.8, KERZE, 'm', .2),
                'Das Zeichen', 'Ihr Zeichen in Kerzengold auf dunklem Holz.'))
    E.append(zh('e02', False, BLATT, MESSING, tx(19, 27, '1753', 12.5, HOLZ) + strich(12, 32.6, 19, MESSING, .3) + tx(19, 38.6, 'ERBAUT DURCH', 1.75, TAUPE, 'm', .2) + tx(19, 42.4, 'PETER GERMANN', 1.75, TAUPE, 'm', .2) + hzz(19, 8, 7, MESSING),
                '1753', 'Das Baujahr, gross.'))
    E.append(zh('e03', True, ROT, LICHT, tx(28, 17.5, 'Zu Gast –', 6.6, PAPIER) + tx(28, 26, 'bei Freunden', 6.6, LICHT) + tx(28, 32, 'LANDGASTHOF RUEDIHUS', 1.6, PAPIER, 'm', .22),
                'Zu Gast – bei Freunden', 'Ihr Satz im Rot der Geranien.'))
    E.append(zh('e04', True, BLATT, HOLZ, tx(28, 18.5, 'Chäs-u Wystube', 5.2, HOLZ) + strich(12, 22, 28, MESSING, .3) + tx(28, 28, 'FONDUE · RACLETTE · RÖSTI', 1.8, TAUPE, 'm', .2),
                'Chäs-u Wystube', 'Für die Stube im Parterre.'))
    kacheln = ''.join(f'<rect x="{11 + (i % 4) * 4.2}" y="{9 + (i // 4) * 4.2}" width="3.6" height="3.6" rx=".5" fill="none" stroke="{LICHT}" stroke-width=".25"/>' for i in range(12))
    E.append(zh('e05', False, OFEN, LICHT, kacheln + tx(19, 33.5, 'Ofestübli', 6.2, PAPIER) + strich(12, 37, 19, LICHT, .3) + tx(19, 43, 'MIT GRÜNEM', 1.7, LICHT, 'm', .2) + tx(19, 46.6, 'KACHELOFEN', 1.7, LICHT, 'm', .2),
                'Ofestübli', 'Das Grün Ihres Kachelofens.'))
    sterne = ''.join(stern(x, y, r, LICHT) for x, y, r in [(10, 10, 1), (17, 7, .6), (28, 8.5, 1.2), (39, 7, .7), (46, 11, .9), (22, 12.5, .5), (34, 12, .5)])
    E.append(zh('e06', True, TIEF, KERZE, sterne + tx(28, 24, 'Hymmelrich', 7.2, PAPIER) + tx(28, 30.5, 'UNTER DEM OFFENEN DACHSTUHL', 1.6, KERZE, 'm', .2),
                'Hymmelrich', 'Für die Zimmer unter dem Dach.'))
    herz = f'<path d="M19 17.5c-3.2-2.6-6-4.800-6-7.800 0-2 1.500-3.400 3.300-3.400 1.100 0 2.100.6 2.700 1.500.6-.9 1.600-1.500 2.700-1.500 1.800 0 3.300 1.400 3.300 3.400 0 3-2.800 5.200-6 7.800Z" fill="none" stroke="{ROT}" stroke-width=".45"/>'
    E.append(zh('e07', False, LICHT, HOLZ, herz + tx(19, 30, 'Liebes-', 6.4, HOLZ) + tx(19, 37.6, 'laube', 6.4, HOLZ) + strich(12, 41, 19, ROT, .3) + tx(19, 47, 'MIT HIMMELBETT', 1.7, TAUPE, 'm', .2),
                'Liebeslaube', 'Mit dem Herz aus Ihren Stuhllehnen.'))
    E.append(zh('e08', True, BLATT, MESSING, tx(28, 16.5, 'Novembernacht', 5.6, HOLZ) + strich(12, 20, 28, MESSING, .3) + tx(28, 25.4, 'ALLES HOLZ IN EINER EINZIGEN', 1.6, TAUPE, 'm', .18) + tx(28, 29, 'BESTIMMTEN NOVEMBERNACHT', 1.6, TAUPE, 'm', .18),
                'Novembernacht', 'Die Sage vom Holz, aus Ihrer Karte.'))
    E.append(zh('e09', False, RUSS, KERZE, hzz(19, 8, 8, KERZE) + tx(19, 28, 'ds rich', 6.4, PAPIER) + tx(19, 36, 'Ruedi', 7.4, LICHT) + strich(12, 39.6, 19, KERZE, .3) + tx(19, 45.4, 'RUDOLF REICHEN', 1.7, KERZE, 'm', .2) + tx(19, 49, 'CA. 1850', 1.7, KERZE, 'm', .2),
                'Ds rich Ruedi', 'Woher Ihr Haus seinen Namen hat.'))
    E.append(zh('e10', True, KERZE, HOLZ, tx(28, 18.5, 'Suure Mocke', 6.6, RUSS) + strich(12, 22, 28, RUSS, .3) + tx(28, 28, 'WIE ZU GROSSMUTTERS ZEITEN', 1.7, RUSS, 'm', .2),
                'Suure Mocke', 'Ein Gericht aus der Egger- und Stettlerstube.'))
    butzen = ''.join(f'<circle cx="{11.5 + (i % 4) * 5}" cy="{11 + (i // 4) * 5}" r="2.1" fill="none" stroke="{HOLZ}" stroke-width=".3"/><circle cx="{11.5 + (i % 4) * 5}" cy="{11 + (i // 4) * 5}" r=".5" fill="{HOLZ}"/>' for i in range(12))
    E.append(zh('e11', False, BLATT, HOLZ, butzen + tx(19, 33, 'Butzen-', 5.6, HOLZ) + tx(19, 39.6, 'scheiben', 5.6, HOLZ) + strich(12, 43, 19, MESSING, .3) + tx(19, 48.6, 'REIHENFENSTER', 1.7, TAUPE, 'm', .2),
                'Butzenscheiben', 'Das Muster Ihrer Fensterreihe.'))
    E.append(zh('e12', True, RUSS, KERZE, tx(28, 17.5, 'Schpiszettel', 6.6, LICHT) + strich(12, 21, 28, KERZE, .3) + tx(28, 26.4, 'NUR AUSGESUCHTE PRODUKTE', 1.6, PAPIER, 'm', .18) + tx(28, 30, 'AUS DER SCHWEIZ', 1.6, PAPIER, 'm', .18),
                'Schpiszettel', 'Ihr Grundsatz für die Küche.'))
    return E


# ============================================================ Banderole für die Serviette (210 × 50), hell und dunkel
# Wortlaut: Karte «Tagesteller», Zitat von Jeremias Gotthelf, so wie es das Haus abdruckt
def banderole():
    def b(grund, schrift, akzent, muster):
        v = ((kasten(0, 0, 210, 50, f'background:{grund} {MUSTER}') if muster else '') + rahmen(3, akzent, 1.5, .25)
             + hz(105, 5.4, 9.5, akzent)
             + t(20, 21.5, '«' + e(D.GOTTHELF) + '»', 's c', f'font-size:4.1mm;line-height:1.32;color:{schrift}', 170)
             + t(0, 41.2, 'Jeremias Gotthelf', 'm c', f'font-size:1.8mm;color:{akzent}', 210))
        return blatt(210, 50, v, '', f'background:{grund}')
    return [b(RUSS, LICHT, KERZE, True), b(BLATT, HOLZ, MESSING, False)]


# ============================================================ Anhänger für die Zimmerschlüssel (60 × 120, gelocht), je Zimmerart einer
# Namen der Zimmerarten: Zimmer-Seite der Website (daten.py: ZIMMER). Satz der Rückseite: Leitsatz des Hauses
def anhaenger():
    def kontur(farbe):
        return (f'<svg class="abs" style="inset:0;width:60mm;height:120mm" viewBox="0 0 60 120" fill="none"><path d="M17.5 3.2H42.5L56.8 17.5V112a4.8 4.8 0 0 1-4.8 4.8H8A4.8 4.8 0 0 1 3.2 112V17.5Z" stroke="{farbe}" stroke-width=".3"/>'
                f'<circle class="oese" cx="30" cy="14" r="3.4" fill="#fff" stroke="rgba(0,0,0,.3)" stroke-width=".2"/><circle cx="30" cy="14" r="5.4" stroke="{farbe}" stroke-width=".3"/></svg>')
    aus = []
    for z in D.ZIMMER:
        name = z['name']
        aus.append(blatt(60, 120, kontur(MESSING) + hz(30, 27, 15, MESSING)
                         + t(0, 51, e(name), 's c', f'font-size:{6.2 if len(name) > 11 else 7.6}mm;line-height:1;color:{HOLZ}', 60) + lin(22, 63.5, 16, MESSING, .4)
                         + t(0, 68, 'Zimmer', 'm c', f'font-size:2.1mm;color:{TINTE}', 60)
                         + f'<i class="abs" style="left:13mm;top:76mm;width:34mm;height:22mm;border:.3mm solid {HOLZ};border-radius:2mm"></i>' + t(15.5, 77.6, 'Nr.', 'm', f'font-size:2.1mm;color:{TAUPE}')
                         + t(0, 105, 'Landgasthof Ruedihus', 's c', f'font-size:3.3mm;color:{HOLZ}', 60) + t(0, 110.6, 'Kandersteg', 'm c', f'font-size:1.95mm;color:{TINTE}', 60),
                         '', f'background:{BLATT}', 'gepaeck'))
    aus.append(blatt(60, 120, kasten(0, 0, 60, 120, f'background:{RUSS} {MUSTER}') + kontur(KERZE) + hz(30, 30, 17, KERZE)
                     + t(0, 58, 'Zu Gast –', 's c', f'font-size:7mm;line-height:1.1;color:{LICHT}', 60) + t(0, 67, 'bei Freunden.', 's c', f'font-size:7mm;line-height:1.1;color:{KERZE}', 60)
                     + lin(22, 82, 16, KERZE, .4)
                     + t(0, 100, 'Landgasthof Ruedihus', 'm c', f'font-size:1.9mm;color:{LICHT}', 60) + t(0, 105, e(TEL), 's c', f'font-size:3.6mm;color:{LICHT}', 60),
                     '', f'background:{RUSS}', 'gepaeck'))
    return aus


# ============================================================ Karte zur Zimmermappe: Aufsteller mit QR-Code (A6 hoch), Tasty Studios 10.10.2026
# Der Code führt auf die Zimmermappe (mappe.html), die Rezeption im Chat ganzseitig am Handy. Sätze von mir (MEINS), Nummer und Adresse vom Haus.
MAPPE_ADRESSE = 'https://ruedihus.tastystudios.ch/mappe.html'


def qr_pfad(adresse):
    import qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0); q.add_data(adresse); q.make(fit=True)
    m = q.get_matrix()
    return len(m), ''.join(f'M{x} {y}h1v1h-1z' for y, z in enumerate(m) for x, an in enumerate(z) if an)


def mappekarte():
    n, weg = qr_pfad(MAPPE_ADRESSE)
    qr = f'<svg class="abs" style="left:24.5mm;top:58mm;width:56mm;height:56mm" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><path fill="{RUSS}" d="{weg}"/></svg>'
    v = (f'<i class="abs" style="left:0;top:0;width:105mm;height:44mm;background:{RUSS} {MUSTER};border-bottom:.5mm solid {MESSING}"></i>'
         + hz(52.5, 7, 16, KERZE)
         + t(0, 25.5, 'Ihre Zimmermappe', 's c', f'font-size:6.4mm;color:{PAPIER}', 105)
         + t(0, 35.2, 'Your room folder · Votre dossier de chambre', 'm c', f'font-size:2mm;letter-spacing:.12em;color:{KERZE}', 105)
         + f'<i class="abs" style="left:20.5mm;top:54mm;width:64mm;height:64mm;background:#fff;border-radius:3mm;box-shadow:inset 0 0 0 .25mm {MESSING}"></i>' + qr
         + t(12, 122.5, 'Kamera öffnen, Code scannen, fragen.', 's c', f'font-size:3.9mm;white-space:nowrap;color:{RUSS}', 81)   # Robert 18.10.2026: Titel bricht in Safari nicht mehr um
         + t(12, 130, 'Open your camera, scan, ask. · Ouvrez l’appareil photo, scannez, demandez.', 'c', f'font-size:2.45mm;line-height:1.4;color:{TINTE};opacity:.8', 81)
         + lin(12, 139.5, 81, MESSING, .2)
         + t(0, 141.5, 'Landgasthof Ruedihus · ' + TEL, 'm c', f'font-size:1.95mm;color:{TINTE};opacity:.75', 105))
    punkte = [('Stuben', 'Welche Stube offen ist, einen Tisch anfragen'), ('Karte', 'Schpiszettel, Tagesteller und die Preise der Fondues'), ('Zimmer', 'Himmelbett, Liebeslaube, Hymmelrich, Preise'),
              ('Ausflüge', 'Oeschinensee, Sunnbüel, Gemmi, je nach Wetter'), ('Geschichte', 'Das Haus von 1753 und seine Stuben'), ('Buchen', 'Daten nennen, das Buchungssystem öffnet sich')]
    y, z = 37, ''
    for name, text in punkte:
        z += t(14, y, e(name), 's', f'font-size:4.1mm;color:{RUSS}', 30) + t(44, y + .5, e(text), '', f'font-size:2.8mm;line-height:1.45;color:{TINTE}', 48)
        y += 13.4
        z += lin(14, y - 3.6, 77, 'rgba(183,143,81,.5)', .2)
    r = (hz(20.5, 11, 13, RUSS) + t(31, 12.6, 'Was Sie fragen können', 's', f'font-size:5.6mm;color:{RUSS}', 62) + lin(14, 28, 77, MESSING, .3) + z
         + t(14, 122, 'Die Antworten kommen von einer KI aus den Angaben des Hauses. Verbindlich sind Buchung und Rezeption.', '', f'font-size:2.35mm;line-height:1.45;color:{TINTE};opacity:.75', 77)
         + t(0, 141.5, 'Landgasthof Ruedihus · ' + e(ADR), 'm c', f'font-size:1.95mm;color:{TINTE};opacity:.75', 105))
    return [blatt(105, 148, v, '', 'background:' + PAPIER), blatt(105, 148, r, '', 'background:' + PAPIER)]


def baue():
    Dr = []
    def d(ident, name, format_, blaetter, vorschau, satz, quelle):
        Dr.append(dict(id=ident, name=name, format=format_, blaetter=blaetter, vorschau=vorschau, satz=satz, quelle=quelle))
    d('banderole', 'Banderole für die Serviette', '210 × 50 mm, hell und dunkel', banderole(), [('banderole-1', 1), ('banderole-2', 2)],
      'Ein Streifen Papier, der die Serviette zusammenhält. Darauf steht das Zitat von Jeremias Gotthelf, das Sie auf Ihrer Karte abdrucken.', 'Karte «Tagesteller»')
    d('anhaenger', 'Anhänger für die Zimmerschlüssel', '60 × 120 mm, gelocht, vier Motive', anhaenger(), [(f'anhaenger-{i + 1}', i + 1) for i in range(len(D.ZIMMER))] + [('anhaenger-r', len(D.ZIMMER) + 1)],
      'Ihre Zimmer haben Namen, die man nicht vergisst. Jede Zimmerart bekommt ihren eigenen Anhänger, auf der Rückseite steht Ihr Satz.', 'Zimmer-Seite Ihrer Website')
    ak = []
    for x in ANSICHT:
        ak += ansichtskarte(*x)
    d('ansichtskarten', 'Ansichtskarten', 'A6 quer, vier Motive', ak, [(f'ansichtskarte-{i + 1}', i * 2 + 1) for i in range(4)] + [('ansichtskarte-r', 2)],
      'Vier Karten mit Ihren eigenen Aufnahmen, das Schild in der Bildecke nennt das Motiv.', 'Fotos von Ihrer Website und aus Ihrem Eintrag bei Schweiz Tourismus')
    d('gutschein', 'Gutschein', 'DIN lang quer, 210 × 100 mm', gutschein(), [('gutschein', 1), ('gutschein-r', 2)],
      'Für die Geschenkgutscheine, die Sie laut Ihrer Karte gerne ausstellen: vorn Ihr Zeichen und Ihr Satz, hinten Platz für Namen, Leistung und Wert.', 'Karte der Chäs- und Wystube, «Geschenkgutscheine»')
    d('tischkarte', 'Tischkarte', 'A6 quer, zum Aufstellen', tischkarte(), [('tischkarte', 1), ('tischkarte-r', 2)],
      'Eine Karte für reservierte Tische in Ihren Stuben. Auf der Rückseite steht Ihr Grundsatz für die Küche, so wie er auf Ihrer Karte steht.', 'Karte der Chäs- und Wystube, «Das Konzept»; Restaurant-Seite Ihrer Website')
    d('untersetzer', 'Untersetzer', 'rund, 100 mm, vier Motive', untersetzer(), [(f'untersetzer-{i + 1}', i + 1) for i in range(4)],
      'Vier Untersetzer für die Stuben: Ihr Zeichen, das Baujahr, Ihr Satz und was man bei Ihnen vergebens sucht.', 'Karten des Hauses und Startseite Ihrer Website')
    d('geschichte', 'Die Geschichte des Hauses', 'A5 hoch, zwei Seiten', geschichte(), [('geschichte', 1), ('geschichte-r', 2)],
      'Die Geschichte Ihres Hauses steht heute klein auf der Rückseite der Karte. Hier ist sie als eigenes Blatt fürs Zimmer, mit vier Jahreszahlen und Ihren eigenen Worten.', 'Karte der Chäs- und Wystube, «Geschichte»')
    d('briefpapier', 'Briefpapier', 'Briefbogen A4, Couvert C6/5', briefpapier()[:2], [('briefbogen', 1), ('couvert', 2)],   # ohne Visitenkarte (Robert 10.10.2026)
      'Briefbogen und Couvert mit Ihrem Zeichen und Ihrer Wortmarke.', 'Kontaktangaben Ihrer Website')
    d('mappekarte', 'Karte zur Zimmermappe', 'A6 hoch, zum Aufstellen', mappekarte(), [('mappekarte', 1), ('mappekarte-r', 2)],
      'Eine Karte fürs Zimmer mit dem QR-Code zur Zimmermappe: Der Gast scannt und fragt die Rezeption im Chat in seiner Sprache. Hinten steht, was man alles fragen kann.', 'Rezeption im Chat des Entwurfs; Adresse und Telefon von Ihrer Website')
    P.fertig(Dr, etiketten(), MEINS)


if __name__ == '__main__':
    baue()
