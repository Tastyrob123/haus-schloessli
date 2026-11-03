#!/usr/bin/env python3
"""Ideen für Papier: Drucksachen und Untersetzer der Lästermeile, Wirtschaft am Schlössli (Station 13, 19.10.2026).
   PYTHONPATH=<Kit> python3 _werkbank/papier.py "<website>"

Alle Angaben kommen aus website/inhalt/haus.json, bankett.json und laestermeile.json (eine Stelle, Quelle je Feld), nichts ist abgetippt.
Was nur im Betrieb vorkommt, wird gedruckt: Gutscheine (Gutschein-Seite), reservierte Tische (Reservation), Bankettmenüs (Banketts & Gruppen),
die Betriebsferien (Kontakt), Briefe. Das Gegenstück zum Sticker ist der Untersetzer, weil an der Lästermeile den ganzen Tag Getränke
über die Theke gehen (Foto «bar»: «An der Bar wird ein Bier gezapft»). Ansichtskarten zeigen nur Haus und Landschaft (Master 5a).
Keine Einkerbungen, keine Visitenkarte, keine Kreise als Schmuck (Tasty-Sprache E). Was von Tasty Studios ist, steht in MEINS."""
import json, os, re
import papier_kern as P
from papier_kern import t, lin, linv, rahmen, kasten, foto, blatt, hz, hw, tx, hzz, hwz, strich, etikett, e
from kern import H, ROOT

F = H.FARBEN
NACHT, TIEF, STUHL, PAPIER, KALK, WEISS, HIMMEL, DUNST, TINTE, PUNKT, WASSER = (F['nacht'], F['navy'], F['blau'], F['papier'], F['creme'], F['weiss'],
                                                                                F['gold'], F['messing'], F['tinte'], F['punkt'], F['taupe'])
HJ = H.HAUS
LM = json.load(open(os.path.join(ROOT, 'inhalt', 'laestermeile.json'), encoding='utf-8'))
BK = json.load(open(os.path.join(ROOT, 'inhalt', 'bankett.json'), encoding='utf-8'))
_SVG = os.path.relpath(os.path.join(ROOT, 'assets', 'svg'), os.path.join(ROOT, '_werkbank', 'satz'))
TAPETE = f'url({_SVG}/tapete-a-dunkel.svg) 50% 0/14mm auto'      # Punktraster mit den Zeigern, wie auf den dunklen Flächen der Seite
TAPETE_H = f'url({_SVG}/tapete-a-hell.svg) 50% 0/14mm auto'
ADR = f"{HJ['strasse']} · {HJ['ort']}"
TEL, MAIL = HJ['telefon'], HJ['mail']

MEINS = ['Bildzeilen der Ansichtskarten', 'Feldnamen auf Gutschein, Tischkarte und Menükarte, das Wort «Reserviert»', 'Der Satz auf dem Aushang zu den Betriebsferien',
         'Auswahl der Sätze und Gerichte auf den Untersetzern', 'Zeichnung der Zementfliesen auf den Untersetzern (nach dem Foto «fliesen»)']


def gross(text):
    """Titel wie auf der Website: Open Sans in Versalien, gesperrt."""
    return e(text.upper())


# ============================================================ Ansichtskarten (A6 quer): Haus und Landschaft, der Ort im Titel
ANSICHT = [   # Bild (website/assets/img), Titel, Bildzeile, Lage, Nachweis (bei freien Fotos Pflicht)
    ('start-2400', 'Bottighofen', 'die Terrasse am Mittag, dahinter der See und die Alpen', '50% 55%', ''),
    ('platanen-2400', 'Am Hafen', 'gedeckte Tische unter den Platanen', '50% 46%', ''),
    ('haus-2400', 'Wirtschaft am Schlössli', 'das ehemalige Hafenmeistergebäude am Bootshafen', '50% 60%', 'Foto: JoachimKohler-HB, CC BY-SA 4.0'),
    ('morgen-2400', 'Bodensee', 'Morgen am See, hinten die Alpen und die Schifflände', '50% 55%', 'Foto: JoachimKohler-HB, CC BY-SA 4.0'),
]


def ansichtskarte(key, name, zeile, lage, nachweis):
    v = (foto(key, 0, 0, 148, 105, lage)
         + kasten(0, 82, 148, 23, f'background:linear-gradient(transparent,rgba(4,16,35,.55))')
         + t(8, 88, gross(name), 's', f'font-size:5.4mm;letter-spacing:.16em;color:{WEISS}')
         + t(8, 96.6, 'Wirtschaft am Schlössli', 'm', f'font-size:1.9mm;color:{DUNST}'))
    adr = ''.join(lin(84, 55 + i * 11, 54, 'rgba(4,16,35,.4)', .2) for i in range(4))
    marke = f'<i class="abs" style="left:116mm;top:8mm;width:22mm;height:27mm;border:.25mm dashed {HIMMEL}"></i>' + hz(127, 12, 12, HIMMEL)
    r = (linv(74, 12, 81, HIMMEL, .25) + adr + marke
         + hz(10, 9, 11, STUHL, False)
         + t(10, 27, gross(name), 's', f'font-size:{4.2 if len(name) < 14 else 3.1}mm;letter-spacing:.14em;color:{STUHL};white-space:nowrap', 60)
         + t(10, 36, e(zeile[0].upper() + zeile[1:]), '', f'font-size:3mm;line-height:1.45;color:{TINTE}', 56)
         + (t(10, 78, e(nachweis), '', f'font-size:1.9mm;line-height:1.4;color:{TINTE};opacity:.6', 56) if nachweis else '')
         + t(10, 86.5, 'Wirtschaft am Schlössli', 'm', f'font-size:1.9mm;color:{TINTE}') + t(10, 90.6, e(ADR), 'm', f'font-size:1.9mm;color:{TINTE};opacity:.75'))
    return [blatt(148, 105, v, '', f'background:{NACHT}'), blatt(148, 105, r, '', f'background:{WEISS}')]


# ============================================================ Gutschein (DIN lang quer). Felder wie auf der Gutschein-Seite der Website
def gutschein():
    v = (kasten(0, 0, 210, 100, f'background:{NACHT} {TAPETE}') + rahmen(5, HIMMEL, 2.5, .3) + hz(40, 22, 36, HIMMEL)
         + t(76, 27, gross('Gutschein'), 's', f'font-size:15mm;line-height:1;letter-spacing:.14em;color:{WEISS}')
         + lin(77, 50, 22, HIMMEL, .4)
         + t(77, 55, gross('Ein Tisch am Hafen'), 's', f'font-size:4.4mm;letter-spacing:.16em;color:{DUNST}')
         + t(77, 79, 'Wirtschaft am Schlössli · Bottighofen', 'm', f'font-size:2.3mm;color:{HIMMEL}'))

    def feld(x, y, b, name):
        return t(x, y, name, 'm', f'font-size:2.25mm;color:{WASSER}') + lin(x, y + 11.5, b, 'rgba(4,16,35,.42)', .2)
    r = (rahmen(5, HIMMEL, 2.5, .3)
         + feld(14, 13, 54, 'Für') + feld(74, 13, 54, 'Von')
         + feld(14, 31, 114, 'Ein Satz dazu') + lin(14, 53.5, 114, 'rgba(4,16,35,.42)', .2)
         + feld(14, 62, 34, 'Betrag CHF') + feld(54, 62, 34, 'Gültig bis') + feld(94, 62, 34, 'Nr.')
         + linv(138, 13, 74, HIMMEL, .25)
         + hz(146, 12, 12, STUHL, False)
         + t(146, 30, gross('Wirtschaft am Schlössli'), 's', f'font-size:3mm;letter-spacing:.14em;line-height:1.3;color:{STUHL}', 54)
         + t(146, 42, f"{e(HJ['strasse'])}<br>{e(HJ['ort'])}", '', f'font-size:3.2mm;line-height:1.45;color:{TINTE}')
         + t(146, 56, f'{e(TEL)}<br>{e(MAIL)}', '', f'font-size:2.9mm;line-height:1.5;color:{TINTE}')
         + t(146, 73, e(HJ['zeiten']['tage']) + '<br>' + e(HJ['zeiten']['offen']), 'm', f'font-size:1.95mm;line-height:1.6;color:{TINTE};opacity:.8', 54))
    return [blatt(210, 100, v, '', f'background:{NACHT}'), blatt(210, 100, r, '', f'background:{WEISS}')]


# ============================================================ Tischkarte «Reserviert» (A6 quer, Aufsteller)
def tischkarte():
    def feld(x, y, b, name):
        return t(x, y, name, 'm', f'font-size:2.3mm;color:{WASSER}') + lin(x, y + 12, b, 'rgba(4,16,35,.42)', .2)
    v = (rahmen(5, HIMMEL, 2.5, .3) + hz(74, 11, 13, STUHL)
         + t(0, 36, gross('Reserviert'), 's c', f'font-size:11mm;line-height:1;letter-spacing:.18em;color:{STUHL}', 148)
         + lin(65, 52, 18, HIMMEL, .4)
         + feld(30, 58, 52, 'Für') + feld(90, 58, 28, 'Um')
         + t(0, 89.5, 'Terrasse · Gaststube · Lästermeile', 'm c', f'font-size:1.95mm;color:{TINTE};opacity:.78', 148))
    r = (kasten(0, 0, 148, 105, f'background:{NACHT} {TAPETE}') + rahmen(5, HIMMEL, 2.5, .3)
         + t(14, 28, gross(HJ['satz_terrasse']), 's c', f'font-size:6.2mm;line-height:1.35;letter-spacing:.14em;color:{WEISS}', 120)
         + lin(65, 56, 18, HIMMEL, .4)
         + t(0, 61, e(HJ['satz_terrasse_von']), 'm c', f'font-size:2.2mm;color:{HIMMEL}', 148)
         + t(14, 74, e(HJ['satz_lage']), 'c', f'font-size:3.2mm;line-height:1.5;color:{DUNST}', 120))
    return [blatt(148, 105, v, '', f'background:{WEISS}'), blatt(148, 105, r, '', f'background:{NACHT}')]


# ============================================================ Menükarte für eine Feier (A5 hoch). Gänge und Preise aus den Bankettmenüvorschlägen
def menuekarte():
    m = next(x for x in BK['menues'] if x['name'] == 'Herbst')
    y, gaenge = 70, ''
    for g in m['gerichte']:
        name = re.sub(r'\s+', ' ', g['name']).strip()
        gaenge += (t(14, y, gross(name), 's c', f'font-size:{3.4 if len(name) < 28 else 2.8}mm;letter-spacing:.12em;line-height:1.3;color:{STUHL}', 120)
                   + t(18, y + (6.4 if len(name) < 40 else 10.4), e(g['text']), 'c', f'font-size:3.1mm;line-height:1.45;color:{TINTE}', 112))
        y += 23
    v = (rahmen(6, HIMMEL, 2.5, .3) + hz(74, 15, 15, STUHL)
         + t(0, 36, gross('Ihr Menü'), 's c', f'font-size:8mm;letter-spacing:.2em;color:{STUHL}', 148)
         + lin(65, 50, 18, HIMMEL, .4)
         + feld_zeile(30, 55, 'Anlass') + feld_zeile(84, 55, 'Datum', 34)
         + gaenge
         + t(0, 196, 'Wirtschaft am Schlössli · ' + e(ADR), 'm c', f'font-size:1.95mm;color:{TINTE};opacity:.75', 148))
    r = (kasten(0, 0, 148, 210, f'background:{NACHT} {TAPETE}') + rahmen(6, HIMMEL, 2.5, .3)
         + hz(74, 40, 22, HIMMEL)
         + t(14, 80, gross(HJ['bankett']['titel']), 's c', f'font-size:6mm;letter-spacing:.16em;color:{WEISS}', 120)
         + t(18, 96, e(HJ['bankett']['platz']), 'c', f'font-size:3.3mm;line-height:1.55;color:{DUNST}', 112)
         + t(0, 186, e(TEL) + ' · ' + e(MAIL), 'm c', f'font-size:2mm;color:{HIMMEL}', 148))
    return [blatt(148, 210, v, '', f'background:{WEISS}'), blatt(148, 210, r, '', f'background:{NACHT}')]


def feld_zeile(x, y, name, b=48):
    return t(x, y, name, 'm', f'font-size:2.1mm;color:{WASSER}') + lin(x, y + 8.6, b, 'rgba(4,16,35,.42)', .2)


# ============================================================ Aushang an der Tür: Betriebsferien (A4 hoch). Zeiten aus haus.json
def aushang():
    ferien = HJ['ferien']
    zeilen = ''.join(t(20, 164 + i * 12, e(f), 's c', f'font-size:5mm;letter-spacing:.06em;line-height:1.3;color:{WEISS}', 170) for i, f in enumerate(ferien))
    v = (foto('abend-2400', 0, 0, 210, 118, '50% 62%') + kasten(0, 118, 210, 179, f'background:{NACHT} {TAPETE}')
         + kasten(0, 117.4, 210, .7, f'background:{HIMMEL}')
         + hz(105, 127, 12, HIMMEL)
         + t(0, 147, gross('Betriebsferien'), 's c', f'font-size:7.4mm;letter-spacing:.2em;color:{WEISS}', 210)
         + zeilen
         + lin(96, 196, 18, HIMMEL, .4)
         + t(20, 204, e(HJ['zeiten']['tage'] + ', ' + HJ['zeiten']['offen'] + '. ' + HJ['zeiten']['ruhetag'] + '.'), 'c', f'font-size:3.6mm;line-height:1.5;color:{DUNST}', 170)
         + t(20, 222, e(HJ['zeiten']['laestermeile']), 'c', f'font-size:3.6mm;line-height:1.5;color:{DUNST}', 170)
         + hw(105, 256, 62, WEISS)
         + t(0, 270, e(ADR) + ' · ' + e(TEL), 'm c', f'font-size:2.2mm;color:{HIMMEL}', 210))
    return [blatt(210, 297, v, '', f'background:{NACHT}')]


# ============================================================ Briefpapier (ohne Visitenkarte)
def briefpapier():
    bogen = (hz(105, 12, 13, STUHL) + hw(105, 33, 58, STUHL) + lin(25, 44, 160, HIMMEL, .25)
             + t(25, 50, 'Wirtschaft am Schlössli · ' + e(ADR), 'm', f'font-size:1.85mm;color:{TINTE};opacity:.7')
             + lin(4, 105, 5, 'rgba(4,16,35,.5)', .15) + lin(4, 210, 5, 'rgba(4,16,35,.5)', .15)
             + lin(25, 273, 160, HIMMEL, .25) + t(0, 277, 'Wirtschaft am Schlössli · ' + e(ADR), 'm c', f'font-size:1.95mm;color:{TINTE}', 210)
             + t(0, 281.6, f'{e(TEL)} · {e(MAIL)} · schloessli-bottighofen.ch', 'm c', f'font-size:1.95mm;color:{TINTE};opacity:.78', 210))
    couvert = (kasten(0, 0, 229, 114, f'background:{NACHT} {TAPETE}') + hz(15, 11, 10, HIMMEL, False) + hw(30, 14, 44, WEISS, False) + t(30, 21, e(ADR), 'm', f'font-size:2.05mm;color:{HIMMEL}')
               + rahmen(4.5, HIMMEL, 2, .25)
               + f'<i class="abs" style="left:122mm;top:50mm;width:92mm;height:42mm;background:{WEISS};border-radius:1.6mm"></i>')
    return [blatt(210, 297, bogen, '', f'background:{WEISS}'), blatt(229, 114, couvert, '', f'background:{NACHT}')]


# ============================================================ Untersetzer der Lästermeile (rund 100 mm und quadratisch 94 mm), zwölf Motive
# Die Fliese: aus dem Foto der Zementfliesen an der Bar nachgezeichnet (Rauten und Stern im Quadrat), Ton in Ton im Stuhlblau
def fliese(x, y, s, farbe, d=.3):
    h = s / 2
    return (f'<g transform="translate({x},{y})" fill="none" stroke="{farbe}" stroke-width="{d}">'
            f'<rect x="{-h}" y="{-h}" width="{s}" height="{s}"/><path d="M0 {-h}L{h} 0 0 {h}{-h} 0Z"/>'
            f'<path d="M0 {-h * .52}L{h * .16} {-h * .16} {h * .52} 0 {h * .16} {h * .16} 0 {h * .52}{-h * .16} {h * .16}{-h * .52} 0{-h * .16} {-h * .16}Z"/>'
            f'<path d="M{-h} {-h}L{-h * .52} {-h * .52}M{h} {-h}L{h * .52} {-h * .52}M{h} {h}L{h * .52} {h * .52}M{-h} {h}L{-h * .52} {h * .52}"/></g>')


def kreisform(r=49):
    return f'M50 {50 - r}A{r} {r} 0 1 1 50 {50 + r}A{r} {r} 0 1 1 50 {50 - r}Z'


def eckform(s=94, r=5):
    return f'M{r} 0H{s - r}A{r} {r} 0 0 1 {s} {r}V{s - r}A{r} {r} 0 0 1 {s - r} {s}H{r}A{r} {r} 0 0 1 0 {s - r}V{r}A{r} {r} 0 0 1 {r} 0Z'


def rund(ident, grund, rand, innen, name, satz):
    f = kreisform()
    return etikett(ident, 100, 100, f, f'<path d="{f}" fill="{grund}"/><circle cx="50" cy="50" r="45" fill="none" stroke="{rand}" stroke-width=".3"/>' + innen, name, satz)


def eckig(ident, grund, rand, innen, name, satz):
    f = eckform()
    return etikett(ident, 94, 94, f, f'<path d="{f}" fill="{grund}"/><path d="{eckform(86, 3)}" transform="translate(4 4)" fill="none" stroke="{rand}" stroke-width=".3"/>' + innen, name, satz)


def ring(text, r, farbe, groesse, oben=True, sperr=.2, ident='r'):
    d = f'M{50 - r} 50 A{r} {r} 0 0 1 {50 + r} 50' if oben else f'M{50 - r} 50 A{r} {r} 0 0 0 {50 + r} 50'
    return (f'<path id="{ident}" d="{d}" fill="none"/><text font-family="DM Mono" font-size="{groesse}" letter-spacing="{sperr}em" fill="{farbe}" text-anchor="middle">'
            f'<textPath href="#{ident}" startOffset="50%">{e(text.upper())}</textPath></text>')


def tapas_namen():
    """Gerichte der Karte der Lästermeile, Namen im Wortlaut."""
    namen = []
    for r in LM['gruppen']:
        for g in r['eintraege']:
            n = g.get('name') if isinstance(g, dict) else None
            if n:
                namen.append(re.sub(r'\s+', ' ', n).strip())
    return namen


def untersetzer():
    T = tapas_namen()
    U = []
    raster = ''.join(fliese(26 + (i % 3) * 21, 26 + (i // 3) * 21, 21, HIMMEL, .28) for i in range(9))
    U.append(rund('u01', NACHT, HIMMEL, raster + f'<circle cx="50" cy="50" r="17" fill="{NACHT}"/>' + hzz(50, 39, 18, WEISS), 'Die Fliese', 'Die Zementfliesen der Bar, Ton in Ton, in der Mitte die Zeiger.'))
    U.append(rund('u02', WEISS, STUHL, tx(50, 45, 'LÄSTER', 9.4, STUHL, 's', .16) + tx(50, 58, 'MEILE', 9.4, HIMMEL, 's', .16) + strich(16, 64, 50, STUHL, .3)
                  + ring('Wirtschaft am Schlössli · Bottighofen', 38, STUHL, 2.8, True, .22, 'r02'), 'Lästermeile', 'Der Name der Bar, geteilt wie auf der Startseite.'))
    U.append(rund('u03', STUHL, WEISS, tx(50, 47, 'TAPAS', 8.6, WEISS, 's', .2) + tx(50, 58, 'DURCHGEHEND', 4.4, DUNST, 's', .2) + strich(14, 63, 50, WEISS, .3)
                  + ring(HJ['zeiten']['offen'], 38, DUNST, 2.9, False, .2, 'r03'), 'Tapas durchgehend', 'Ihr Satz, im Blau der Stühle.'))
    U.append(eckig('u04', KALK, STUHL, ''.join(fliese(13 + (i % 4) * 22.6, 13 + (i // 4) * 22.6, 22.6, STUHL, .22) for i in range(16))
                   + f'<rect x="22" y="36" width="50" height="22" rx="2" fill="{KALK}"/>' + tx(47, 50.4, 'SCHLÖSSLI', 5.2, STUHL, 's', .3), 'Fliesenboden', 'Die Fliesen als ganzer Boden, quadratisch.'))
    U.append(rund('u05', PUNKT, WEISS, tx(50, 46, 'ZUR STÄRKUNG', 5.6, WEISS, 's', .14) + tx(50, 55.5, '& SÜSSES', 5.6, NACHT, 's', .14) + strich(14, 61, 50, WEISS, .3)
                  + ring('Lästermeile · Bottighofen', 38, WEISS, 2.9, True, .24, 'r05'), 'Zur Stärkung & Süsses', 'Die zweite Spalte der Karte, im Rot der Schirme.'))
    for i, n in enumerate(T[:5]):
        teile = n.upper().split(' ')
        zl = [' '.join(teile[:len(teile) // 2 + len(teile) % 2]), ' '.join(teile[len(teile) // 2 + len(teile) % 2:])] if len(n) > 12 else [n.upper()]
        innen = ''.join(tx(47, 46 + j * 8 - (len(zl) - 1) * 4, e(z), 5.4 if len(n) < 16 else 4.6, STUHL if i % 2 == 0 else WEISS, 's', .14) for j, z in enumerate(zl))
        U.append(eckig(f'u{6 + i:02d}', WEISS if i % 2 == 0 else NACHT, HIMMEL, fliese(47, 18, 12, HIMMEL, .25) + innen + strich(14, 60, 47, HIMMEL, .3)
                       + tx(47, 76, 'LÄSTERMEILE', 2.4, HIMMEL, 'm', .24), n, 'Ein Gericht der Lästermeile, Name wie auf der Karte.'))
    U.append(rund('u11', NACHT, HIMMEL, tx(50, 42, 'DIREKT', 6.4, WEISS, 's', .2) + tx(50, 51, 'IM HAFEN', 6.4, HIMMEL, 's', .2) + tx(50, 60, 'VON BOTTIGHOFEN', 3.4, DUNST, 's', .2)
                  + strich(14, 65, 50, HIMMEL, .3) + ring('Mit Blick aufs Wasser und die Alpen', 38, DUNST, 2.7, False, .2, 'r11'), 'Direkt im Hafen', 'Ihr Satz zur Lage, wörtlich.'))
    U.append(rund('u12', KALK, STUHL, hzz(50, 26, 22, STUHL) + tx(50, 63, 'BY CHRISTIAN KUCHLER', 2.8, STUHL, 'm', .2) + ring('Wirtschaft am Schlössli', 38, STUHL, 3, True, .24, 'r12'),
                  'Die Zeiger', 'Das Zeichen des Hauses, darunter die Zeile Ihres Logos.'))
    return U


def baue():
    Dr = []

    def d(ident, name, format_, blaetter, vorschau, satz, quelle):
        Dr.append(dict(id=ident, name=name, format=format_, blaetter=blaetter, vorschau=vorschau, satz=satz, quelle=quelle))
    ak = []
    for x in ANSICHT:
        ak += ansichtskarte(*x)
    d('ansichtskarten', 'Ansichtskarten', 'A6 quer, vier Motive', ak, [(f'ansichtskarte-{i + 1}', i * 2 + 1) for i in range(len(ANSICHT))] + [('ansichtskarte-r', 2)],
      'Vier Karten mit dem Haus und dem See, der Ort steht im Bild. Zwei Aufnahmen sind freie Fotos, ihr Nachweis steht auf der Rückseite.', 'Fotos Ihrer Website; zwei Fotos von Wikimedia Commons (JoachimKohler-HB, CC BY-SA 4.0)')
    d('gutschein', 'Gutschein', 'DIN lang quer, 210 × 100 mm', gutschein(), [('gutschein', 1), ('gutschein-r', 2)],
      'Der Gutschein zum Verschenken, mit denselben Feldern wie auf der Gutschein-Seite: für wen, von wem, ein Satz und der Betrag.', 'Gutschein-Seite und Kontakt Ihrer Website')
    d('tischkarte', 'Tischkarte', 'A6 quer, zum Aufstellen', tischkarte(), [('tischkarte', 1), ('tischkarte-r', 2)],
      'Für reservierte Tische auf der Terrasse und in der Gaststube. Hinten steht Ihr Satz zur Terrasse.', 'Startseite Ihrer Website')
    d('menuekarte', 'Menükarte für Ihre Feier', 'A5 hoch, zwei Seiten', menuekarte(), [('menuekarte', 1), ('menuekarte-r', 2)],
      'Für jedes Bankett eine eigene Karte auf dem Tisch, hier mit dem Herbstmenü aus Ihren Bankettmenüvorschlägen. Anlass und Datum tragen Sie ein.', 'Bankettmenüvorschläge, PDF vom 29.04.2025')
    d('aushang', 'Aushang Betriebsferien', 'A4 hoch', aushang(), [('aushang', 1)],
      'Ein Blatt für die Tür und die Bar, wenn das Schlössli Pause macht, mit Ihren Ferien und Zeiten.', 'Kontakt-Seite Ihrer Website')
    d('briefpapier', 'Briefpapier', 'Briefbogen A4, Couvert C6/5', briefpapier(), [('briefbogen', 1), ('couvert', 2)],
      'Briefbogen und Couvert mit den Zeigern und Ihrem Namen.', 'Kontakt Ihrer Website')
    P.fertig(Dr, untersetzer(), MEINS)


if __name__ == '__main__':
    baue()
