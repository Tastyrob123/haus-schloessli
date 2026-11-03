#!/usr/bin/env python3
"""Wirtschaft am Schlössli: vierzig Sticker (Werkbank Papier, Nachtbau 3./4.11.2026; Bauart wie sticker.py des Culinarium und des Walk on the Wild Side).
Gebaut wie die Untersetzer (papier_kern.etikett, Druckbogen A3 mit Schnittlinie in Magenta), in einen eigenen Ordner sticker/.
Formen: rund, eckig und Kapsel. Inhalte nur vom Haus: die Zeiger, die Wortmarke, die Lästermeile, die Zeilen der Website (haus.json),
die Auszeichnungen, die Gerichte der Karte, Fotos des Hauses (website/inhalt/bilder.json, nur eigene Fotos). Kein «x», kein «C».
   PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/sticker.py "<website/_werkbank>"   →  satz/sticker*.html, sticker_plan.json
   danach  node _werkbank/sticker_druck.js "<website/_werkbank>" sticker   und   PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/sticker.py "<…>" --seite"""
import json, os, sys
import papier_haus as PH
H = PH.ein()
import papier_kern as P  # noqa: E402
import bogen_mitte  # noqa: E402,F401  Druckbögen mittig (Tor 4, 30.10.2026)
from papier_kern import etikett, hzz, hwz, blatt, t, e  # noqa: E402
from papier_haus import (NACHT, TIEF, STUHL, PAPIER, BLATT, WEISS, HIMMEL, HIMMELH, HIMMELT, TINTE, PUNKT, HJ, LM, BK, NAME, BY, TAGE, OFFEN, IG, ss, ganz)  # noqa: E402

W = PH.W
ZV, WV = PH.ZV, PH.WV


# ---------------------------------------------------------------- Formen (SVG-Pfade in mm)
def kreis(d):
    r = d / 2
    return f'M{r} 0A{r} {r} 0 1 1 {r - .01} 0Z'


def eck(b, h, r=3):
    return f'M{r} 0H{b - r}A{r} {r} 0 0 1 {b} {r}V{h - r}A{r} {r} 0 0 1 {b - r} {h}H{r}A{r} {r} 0 0 1 0 {h - r}V{r}A{r} {r} 0 0 1 {r} 0Z'


def kapsel(b, h):
    return eck(b, h, h / 2)


# ---------------------------------------------------------------- Bausteine
def grund(form, farbe):
    return f'<path d="{form}" fill="{farbe}"/>'


def ring_kreis(d, farbe, ab=2.4):
    return f'<circle cx="{d / 2}" cy="{d / 2}" r="{d / 2 - ab}" fill="none" stroke="{farbe}" stroke-width=".3"/>'


def ring_eck(b, h, farbe, ab=2.2, r=1.6, d=.3):
    return f'<rect x="{ab}" y="{ab}" width="{b - 2 * ab}" height="{h - 2 * ab}" rx="{r}" fill="none" stroke="{farbe}" stroke-width="{d}"/>'


def ti(x, y, text, gr, farbe, sp=.12):
    """Titel: Open Sans in Versalien gesperrt"""
    return P.tx(x, y, e(ss(text).upper()), gr, farbe, 's', sp, 'middle')


def mo(x, y, text, gr, farbe, sp=.18):
    """Etikett: DM Mono in gesperrten Versalien"""
    return P.tx(x, y, e(ss(text).upper()), gr, farbe, 'm', sp, 'middle')


def zg(x, y, b, farbe):
    """die Zeiger, x = Mitte, y = Oberkante"""
    return hzz(x, y, b, farbe)


def wm(x, y, b, farbe):
    """die Wortmarke, x = Mitte, y = Oberkante"""
    return hwz(x, y, b, farbe)


def horizont(x, y, b, farbe, d=.3):
    """Horizont mit Nabe"""
    return (f'<rect x="{x - b / 2}" y="{y - d / 2}" width="{b / 2 - 1.6}" height="{d}" fill="{farbe}"/><rect x="{x + 1.6}" y="{y - d / 2}" width="{b / 2 - 1.6}" height="{d}" fill="{farbe}"/>'
            f'<circle cx="{x}" cy="{y}" r=".9" fill="none" stroke="{farbe}" stroke-width="{d}"/>')


def punkt(x, y, r=.9):
    """Schirmrot nur als Punkt"""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PUNKT}"/>'


def foto(key, b, h, ident, form_innen):
    return (f'<clipPath id="{ident}c"><path d="{form_innen}" transform="translate(2.2 2.2)"/></clipPath>'
            f'<image href="{e(PH.bild_satz(key, 1200))}" x="2.2" y="2.2" width="{b - 4.4}" height="{h - 4.4}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{ident}c)"/>')


# ---------------------------------------------------------------- die vierzig (gemischt: Form, Grösse und Farbe wechseln)
def alle():
    S, n = [], [0]
    G = {a['wer'] + a['was']: a for a in HJ['auszeichnungen']}

    def s(b, h, form, innen, name, satz):
        n[0] += 1
        S.append(etikett(f's{n[0]:02d}', b, h, form, innen, name, satz))

    def nid():
        return f's{n[0] + 1:02d}'

    def kr(d, farbe, innen, name, satz, linie=None):
        s(d, d, kreis(d), grund(kreis(d), farbe) + (ring_kreis(d, linie) if linie else '') + innen, name, satz)

    def ek(b, h, farbe, innen, name, satz, linie=None):
        s(b, h, eck(b, h, 2.6), grund(eck(b, h, 2.6), farbe) + (ring_eck(b, h, linie) if linie else '') + innen, name, satz)

    def ka(b, h, farbe, innen, name, satz):
        s(b, h, kapsel(b, h), grund(kapsel(b, h), farbe) + innen, name, satz)

    def fo(b, h, key, name, satz, rund=False):
        f = kreis(b) if rund else eck(b, h, 2.6)
        fi = kreis(b - 4.4) if rund else eck(b - 4.4, h - 4.4, 1.6)
        s(b, h, f, grund(f, BLATT) + foto(key, b, h, nid(), fi), name, satz)

    zh = lambda b: b * ZV
    # 1–5 die Zeiger und die Wortmarke
    kr(46, STUHL, zg(23, 23 - zh(18) / 2, 18, HIMMELH), 'Die Zeiger', 'Rund, 46 mm. Das Zeichen des Hauses im Stuhlblau.')
    kr(40, BLATT, zg(20, 20 - zh(15) / 2, 15, STUHL), 'Die Zeiger auf Papier', 'Rund, 40 mm.', HIMMEL)
    kr(40, HIMMEL, zg(20, 20 - zh(15) / 2, 15, NACHT), 'Die Zeiger im Seehimmel', 'Rund, 40 mm.')
    ka(110, 20, NACHT, wm(55, 10 - 76 * WV / 2, 76, BLATT), 'Die Wortmarke', 'Kapsel, 110 mm. WIRTSCHAFT AM SCHLÖSSLI auf der Nacht über dem See.')
    ka(110, 20, BLATT, wm(55, 10 - 76 * WV / 2, 76, STUHL), 'Die Wortmarke auf Papier', 'Kapsel, 110 mm.')
    # 6–11 die Lästermeile
    kr(56, NACHT, ti(28, 26, 'Läster', 6.6, BLATT, .16) + ti(28, 34, 'meile', 6.6, HIMMEL, .16) + horizont(28, 39, 18, HIMMEL), 'Lästermeile', 'Rund, 56 mm. Der Name der Bar, geteilt wie auf der Startseite.', HIMMEL)
    ka(96, 24, STUHL, ti(48, 13.6, LM['gruppen'][0]['titel'], 4.6, WEISS, .14) + mo(48, 19.4, 'Lästermeile', 2, HIMMELH, .24), 'Tapas durchgehend', 'Kapsel, 96 mm. Die erste Spalte der Karte der Lästermeile.')
    kr(50, BLATT, ti(25, 23, 'Zur Stärkung', 3.4, STUHL, .1) + ti(25, 30.4, '& Süsses', 5.2, HIMMELT, .12) + horizont(25, 35, 16, HIMMEL), 'Zur Stärkung & Süsses', 'Rund, 50 mm. Die zweite Spalte der Karte.', HIMMEL)
    ek(54, 54, NACHT, zg(27, 9, 7, HIMMEL) + mo(27, 25, 'Den ganzen Tag', 2.6, HIMMELH, .16) + ti(27, 33, 'die Karte der', 3.6, BLATT, .08) + ti(27, 39, 'Lästermeile', 3.6, BLATT, .12),
       'Den ganzen Tag', 'Eckig, 54 mm. Aus dem Satz zu den Zeiten.', HIMMEL)
    tapas = [ganz(x['name']) for x in LM['gruppen'][0]['eintraege']]
    for k, nm in enumerate(tapas[:4]):
        farbe, schrift, linie = [(BLATT, STUHL, HIMMEL), (STUHL, WEISS, HIMMELH), (HIMMEL, NACHT, NACHT), (NACHT, BLATT, HIMMEL)][k]
        teile = nm.split(' ')
        zl = [' '.join(teile[:(len(teile) + 1) // 2]), ' '.join(teile[(len(teile) + 1) // 2:])] if len(nm) > 10 and len(teile) > 1 else [nm]
        g = 4.2 if max(len(z) for z in zl) < 10 else 3.4
        innen = ''.join(ti(25, 25 + j * (g + 1.4) - (len(zl) - 1) * (g + 1.4) / 2 + g / 2.6, z, g, schrift, .1) for j, z in enumerate(zl)) + horizont(25, 33 + (len(zl) - 1) * 2, 14, linie)
        innen += mo(25, 13, 'Tapas', 1.8, linie, .24)
        kr(50, farbe, innen, nm.title(), 'Rund, 50 mm. Ein Gericht der Lästermeile, Name wie auf der Karte.', linie)
    # 15–20 die Zeilen der Website
    kr(52, STUHL, ti(26, 25, 'Direkt', 5.6, WEISS, .16) + ti(26, 32, 'im Hafen', 5.6, HIMMELH, .16) + horizont(26, 37, 16, HIMMELH), 'Direkt im Hafen', 'Rund, 52 mm. Aus Ihrem Satz zur Lage.')
    ka(112, 22, BLATT, mo(56, 12.6, HJ['satz_lage'].split(' gelegen ')[1].rstrip('.'), 3.2, STUHL, .08), 'Mit Blick aufs Wasser und die Alpen', 'Kapsel, 112 mm. Der zweite Teil Ihres Satzes zur Lage.')
    ek(62, 46, BLATT, ti(31, 18.5, 'Die schönste', 4.6, STUHL, .1) + ti(31, 25, 'Terrasse', 4.6, STUHL, .12) + ti(31, 31.5, 'am Bodensee', 4.6, STUHL, .1) + mo(31, 38.5, HJ['satz_terrasse_von'], 1.8, HIMMELT, .2),
       'Die schönste Terrasse', 'Eckig, 62 × 46 mm. Der Satz von Christian Kuchler.', HIMMEL)
    kr(44, HIMMEL, mo(22, 17, 'Am See', 1.9, NACHT, .24) + ti(22, 25.4, 'Bottighofen', 4, NACHT, .1) + horizont(22, 30, 12, NACHT), 'Bottighofen', 'Rund, 44 mm. Der Ort am See.')
    ka(90, 20, NACHT, mo(45, 12, BY, 3.4, HIMMEL, .16), 'By Christian Kuchler', 'Kapsel, 90 mm. Die Zeile des Logos.')
    ek(54, 54, STUHL, zg(27, 9, 7, HIMMELH) + mo(27, 24, 'Willkommen', 2.4, HIMMELH, .24) + ti(27, 31.5, 'in der Wirtschaft', 3.2, WEISS, .08) + ti(27, 37, 'am Schlössli', 3.2, WEISS, .1),
       'Willkommen', 'Eckig, 54 mm. Ihr Satz zur Begrüssung auf der Startseite.', HIMMELH)
    # 21–28 Fotos des Hauses (nur eigene Fotos, website/inhalt/bilder.json)
    fo(60, 60, 'start', 'Foto: die Terrasse am Mittag', 'Eckig, 60 mm. Die blauen Stühle, dahinter der See und die Alpen.')
    fo(60, 60, 'platanen', 'Foto: unter den Platanen', 'Eckig, 60 mm. Gedeckte Tische unter den Platanen.')
    fo(50, 50, 'tortelloni', 'Foto: Tortelloni', 'Rund, 50 mm. Tortelloni mit Tomate, Burrata und Taggiasca-Olive.', True)
    fo(60, 60, 'apero', 'Foto: blaue Stunde', 'Eckig, 60 mm. Ein Spritz und ein Bier auf dem blauen Tisch.')
    fo(50, 50, 'dessert', 'Foto: Dessert', 'Rund, 50 mm. Dessert mit Beeren auf dem blauen Teller.', True)
    fo(60, 60, 'bar', 'Foto: an der Bar', 'Eckig, 60 mm. An der Bar wird ein Bier gezapft.')
    fo(50, 50, 'anguria', 'Foto: von oben', 'Rund, 50 mm. Ein Teller auf dem blauen Platzteller.', True)
    fo(60, 60, 'glas', 'Foto: ein Glas am See', 'Eckig, 60 mm. Ein Glas Weisswein vor dem See.')
    # 29–32 die Auszeichnungen (haus.json › auszeichnungen)
    gm = next(a for a in HJ['auszeichnungen'] if a['wer'] == 'GaultMillau' and 'Punkte' in a['was'])
    kr(50, NACHT, mo(25, 15, 'GaultMillau', 2, HIMMEL, .22) + ti(25, 30, gm['was'].split()[0], 13, BLATT, .02) + mo(25, 37, 'Punkte · ' + gm['zusatz'], 1.8, HIMMEL, .14), '15 Punkte', 'Rund, 50 mm. GaultMillau, Guide 2027.', HIMMEL)
    kr(56, BLATT, mo(28, 18, 'GaultMillau', 2, HIMMELT, .22) + ti(28, 27, 'Entdeckung', 4.2, STUHL, .1) + ti(28, 33, 'des Jahres', 4.2, STUHL, .1) + ti(28, 39, '2026', 4.2, STUHL, .1) + mo(28, 45, 'Moni Huber', 1.7, HIMMELT, .2),
       'Entdeckung des Jahres 2026', 'Rund, 56 mm. GaultMillau über Monika Huber.', HIMMEL)
    fa = next(a for a in HJ['auszeichnungen'] if a['wer'] == 'Falstaff')
    kr(44, STUHL, mo(22, 13.5, 'Falstaff', 1.9, HIMMELH, .24) + ti(22, 27, fa['was'].split()[0], 11, WEISS, .02) + mo(22, 33, 'von 100', 1.8, HIMMELH, .2), '91 von 100', 'Rund, 44 mm. Falstaff.')
    ek(64, 34, NACHT, mo(32, 11, 'Guide Michelin', 2, HIMMEL, .2) + ti(32, 19.5, 'Favorit der', 4, BLATT, .1) + ti(32, 25.6, 'Inspektoren', 4, BLATT, .12), 'Favorit der Inspektoren', 'Eckig, 64 × 34 mm. Guide Michelin, Selektion 2025.', HIMMEL)
    # 33–40 Haus, Karte, Wein, Feiern, Zeiten, Ort
    ek(56, 56, BLATT, zg(28, 9, 6, STUHL) + ti(28, 25, 'Ein Besen', 4.4, STUHL, .12) + ti(28, 31, 'statt eines', 4.4, STUHL, .1) + ti(28, 37, 'Schilds', 4.4, STUHL, .12) + mo(28, 44, 'Seit dem 17. Jahrhundert', 1.7, HIMMELT, .14),
       'Ein Besen statt eines Schilds', 'Eckig, 56 mm. Die Geschichte vom Haus am See.', HIMMEL)
    ka(108, 22, STUHL, mo(54, 13, 'Frankreich · Italien · Iberische Halbinsel', 3, WEISS, .06), 'Die Karte nach Ländern', 'Kapsel, 108 mm. Die Länder der Karte.')
    kr(50, NACHT, mo(25, 16, 'Der Keller', 1.9, HIMMEL, .24) + ti(25, 24, 'Bündner', 3.6, BLATT, .1) + ti(25, 29.4, 'Herrschaft', 3.6, BLATT, .1) + ti(25, 34.8, 'Burgund', 3.6, BLATT, .1) + ti(25, 40.2, 'Champagne', 3.6, BLATT, .1),
       'Der Keller', 'Rund, 50 mm. Der Schwerpunkt der Weinkarte von Jonas Volpert.', HIMMEL)
    ek(64, 44, STUHL, mo(32, 12, 'Banketts & Gruppen', 2.1, HIMMELH, .18) + ti(32, 22, 'Zwei Etagen', 4.4, WEISS, .1) + ti(32, 28.5, f'je bis zu {BK and HJ["bankett"]["personen"]}', 4.4, WEISS, .1) + mo(32, 35, 'Personen', 2, HIMMELH, .2),
       'Zwei Etagen', 'Eckig, 64 × 44 mm. Platz für Ihre Feier.', HIMMELH)
    kr(46, HIMMEL, mo(23, 16, 'Mittags', 2, NACHT, .24) + ti(23, 25, 'Lunch', 6, NACHT, .2) + horizont(23, 29, 12, NACHT) + mo(23, 34, '3 Gänge', 1.9, NACHT, .2), 'Lunch', 'Rund, 46 mm. Das Lunch-Menü der Woche.')
    ek(60, 42, NACHT, mo(30, 12, TAGE, 2, HIMMEL, .14) + ti(30, 21.5, OFFEN.replace(' Uhr', '').replace(' bis ', ' – '), 5, BLATT, .04) + mo(30, 29, 'Dienstag und Mittwoch Ruhetag', 1.6, HIMMEL, .1) + punkt(30, 34.5),
       'Die Zeiten', 'Eckig, 60 × 42 mm. Offen Donnerstag bis Montag.', HIMMEL)
    ka(108, 22, NACHT, mo(54, 13, 'Four Hands · Excellence Countess', 3.1, HIMMEL, .08), 'Four Hands an Bord', 'Kapsel, 108 mm. Das Dinner mit Dieter Koschina auf dem Schiff.')
    ka(100, 20, BLATT, mo(50, 12, IG, 3.4, STUHL, .06), 'Instagram', 'Kapsel, 100 mm. Wo das Haus seine Abende zeigt.')
    kr(52, STUHL, zg(26, 9, 6, HIMMELH) + ti(26, 27, HJ['strasse'], 4.4, WEISS, .1) + mo(26, 33, HJ['ort'], 2.1, HIMMELH, .14) + horizont(26, 38, 16, HIMMELH), 'Seestrasse 50', 'Rund, 52 mm. Die Adresse am Hafen.')
    return S


def fertig(S):
    """Satzdateien und Druckbögen wie papier_kern.fertig, aber für den Ordner sticker/."""
    alle_ = ''
    for x in S:
        svg = f'<svg class="abs" style="inset:0;width:{x["b"]}mm;height:{x["h"]}mm" viewBox="0 0 {x["b"]} {x["h"]}">{x["innen"]}</svg>'
        alle_ += blatt(x['b'], x['h'], svg, 'etikett', 'background:transparent')
    P.seite('sticker', [alle_], 'Sticker')
    boegen, akt, x0, y0, zh = [], [], 14, 16, 0
    for x in S:
        if x0 + x['b'] > 420 - 14:
            x0, y0, zh = 14, y0 + zh + 9, 0
        if y0 + x['h'] > 297 - 12:
            boegen.append(akt); akt, x0, y0, zh = [], 14, 16, 0
        akt.append((x, x0, y0)); x0 += x['b'] + 9; zh = max(zh, x['h'])
    boegen.append(akt)
    seiten = []
    for nr, akt in enumerate(boegen):
        inn = ''.join(f'<svg class="abs" style="left:{ox}mm;top:{oy}mm;width:{x["b"]}mm;height:{x["h"]}mm;overflow:visible" viewBox="0 0 {x["b"]} {x["h"]}">'
                      f'{x["innen"].replace("id=\"", "id=\"b" + x["id"]).replace("url(#", "url(#b" + x["id"]).replace("href=\"#", "href=\"#b" + x["id"]).replace("#b" + x["id"] + "hz", "#hz").replace("#b" + x["id"] + "hw", "#hw")}'
                      f'<path d="{x["form"]}" fill="none" stroke="#e6007e" stroke-width=".15"/></svg>' for x, ox, oy in akt)
        inn += t(14, 6.5, f'{e(NAME)} · Sticker · Druckbogen {nr + 1} von {len(boegen)} · A3 quer · Originalgrösse · Schnittlinie in Magenta', 'm', f'font-size:2.1mm;color:{TINTE}')
        seiten.append(blatt(420, 297, inn, '', 'background:#fff'))
    P.seite('sticker-bogen', seiten, 'Sticker, Druckbogen')
    plan = {'etiketten': [{k: x[k] for k in ('id', 'b', 'h', 'name', 'satz', 'form')} for x in S], 'boegen': len(boegen),
            'masse': [min(min(x['b'], x['h']) for x in S), max(max(x['b'], x['h']) for x in S)]}
    json.dump(plan, open(os.path.join(W, 'sticker_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Sticker gesetzt:', len(S), 'Stück,', len(boegen), 'Druckbögen')


def seite():
    """sticker/index.html mit der Seite der Untersetzer (papier_seiten.etiketten), umgestellt auf den Ordner sticker/."""
    import papier_seiten as PS
    plan = json.load(open(os.path.join(W, 'sticker_plan.json')))
    PS.plan = dict(PS.plan, etiketten=plan['etiketten'], boegen=plan['boegen'], masse=plan['masse'])
    PS.ROH = os.path.join(W, 'roh', 'sticker')
    PS.ET = dict(ordner='sticker', name='Sticker', einzahl='Sticker')
    PS.S = dict(PS.S, etik_titel=('Sticker', 'vom Hafen.'),
                etik_text='Für die Tür, das Glas, den Laptop und die Tüte zum Mitnehmen: {n} Ideen, rund, eckig und als Kapsel, in den Tönen des Sees.',
                etik_kap='Die Sticker', etik_kopf=['Vierzig', 'Sticker.'],
                etik_kopftext='Die Zeiger, die Wortmarke, die Lästermeile, Ihre Sätze zur Lage und zur Terrasse, die Auszeichnungen und Fotos von Terrasse, Bar und Küche.',
                etik_auslage=[(2, 2, 24, -5), (38, 0, 22, 4), (70, 4, 22, -3), (0, 0, 0, 0), (2, 74, 34, 3), (0, 0, 0, 0), (42, 44, 30, -4), (6, 38, 22, 5), (72, 60, 24, 4)]
                + [(0, 0, 0, 0)] * 40, etik_haufen=None)
    PS.etiketten()
    from PIL import Image
    p = os.path.join(PH.ROOT, 'sticker', 'index.html')
    t_ = open(p, encoding='utf-8').read().replace(' loading="lazy"', '')
    open(p, 'w', encoding='utf-8').write(t_)
    im = Image.open(os.path.join(PH.ROOT, 'sticker', 'img', 's06.webp')); im.save(os.path.join(PH.ROOT, 'sticker', 'img', 'vorschau.webp'), 'WEBP', quality=86)
    print('Seite gebaut: sticker/ ·', len(plan['etiketten']), 'Sticker')


if __name__ == '__main__':
    if '--seite' in sys.argv:
        import kern as K
        K.gestaltung(); seite()
    else:
        fertig(alle())
