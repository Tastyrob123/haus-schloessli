#!/usr/bin/env python3
"""Ideen für Papier: Drucksachen und Untersetzer der Wirtschaft am Schlössli (Werkbank Papier, Nachtbau 3./4.11.2026).
   PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/papier.py "<website/_werkbank>"
Bauart wie papier.py des Culinarium und des Walk on the Wild Side (Kit papier_kern, Satz in mm, Druck mit papier_druck.js), Inhalt vom Schlössli:
Stücke aus dem alten Stand des Hauses (Gutschein, Tischkarte, Menükarte für die Feier, Aushang Betriebsferien, Briefpapier, 19.10.2026) und neue
für Tisch, Theke und Post, dazu die Drucksachen der Hausdruckerei (_werkzeuge/imprimerie/haeuser/schloessli/drucksachen/liste.json, nur kopiert).
Satz nach dem Stilblatt der Drucksachen: eine Achse, Zeichen und Inhalt als Gruppe auf der optischen Mitte, Kopf und Fuss gleich weit vom Rahmen.
Alle Angaben aus website/inhalt/*.json (papier_haus), nichts abgetippt; ss statt ß; keine Preise ausser auf Karten. Was von Tasty Studios ist: MEINS."""
import json, os, re, shutil
import papier_haus as PH
PH.ein()
import papier_kern as P  # noqa: E402
import bogen_mitte  # noqa: E402,F401  Druckbögen mittig (Tor 4, 30.10.2026)
from papier_kern import blatt, etikett, tx, hzz, bogen_text, e  # noqa: E402
from papier_haus import (NACHT, TIEF, STUHL, PAPIER, SPIEGEL, BLATT, WEISS, HIMMEL, HIMMELH, HIMMELT, TINTE, LEISE, PUNKT,  # noqa: E402
                         TAPETE, TAPETE_H, HJ, LM, LU, BK, NAME, ADR, TEL, MAIL, IG, WEBSITE, BY, TAGE, RUHE, OFFEN, KUECHE, ss, ganz, vers)

ROOT = PH.ROOT
HD = os.path.join(PH.PROJ, '_werkzeuge', 'imprimerie', 'haeuser', 'schloessli', 'drucksachen')
MEINS = ['Feldnamen auf Gutschein, Tischkarte, Platzkarte und Menükarte, das Wort «Reserviert»', 'Der Satz auf dem Aushang zu den Betriebsferien',
         'Auswahl der Sätze und Gerichte auf Aufsteller, Kärtchen und Untersetzern']
OS, IN, MO = "'Open Sans',Arial,sans-serif", "'Instrument Sans',Arial,sans-serif", "'DM Mono',Menlo,monospace"

TOENE = {
    'nacht': dict(grund=f'background:{NACHT} {TAPETE}', bg=NACHT, titel=BLATT, text=HIMMELH, et=HIMMEL, linie=HIMMEL, zeichen=HIMMEL, rahmen='rgba(162,182,207,.55)'),
    'stuhl': dict(grund=f'background:{STUHL} {TAPETE}', bg=STUHL, titel=WEISS, text=PAPIER, et=HIMMELH, linie=HIMMELH, zeichen=HIMMELH, rahmen='rgba(197,210,225,.55)'),
    'blatt': dict(grund=f'background:{BLATT}', bg=BLATT, titel=STUHL, text=TINTE, et=HIMMELT, linie=HIMMEL, zeichen=STUHL, rahmen=HIMMEL),
    'papier': dict(grund=f'background:{PAPIER} {TAPETE_H}', bg=PAPIER, titel=STUHL, text=TINTE, et=HIMMELT, linie=HIMMEL, zeichen=STUHL, rahmen=HIMMEL),
}


# ---------------------------------------------------------------- Bausteine im Fluss (Masse in mm)
def zw(b, farbe):
    """die Zeiger, im Fluss (Breite b)"""
    return f'<svg viewBox="{PH.ZEICHEN[0]}" style="display:block;width:{b}mm;height:{b * PH.ZV:.2f}mm;color:{farbe};flex:none" fill="currentColor"><use href="#hz"/></svg>'


def wm(b, farbe):
    """die Wortmarke WIRTSCHAFT AM SCHLÖSSLI, im Fluss"""
    return f'<svg viewBox="{PH.WORT[0]}" style="display:block;width:{b}mm;height:{b * PH.WV:.2f}mm;color:{farbe};flex:none" fill="currentColor"><use href="#hw"/></svg>'


def et(text, gr, farbe, sp=.16):
    return f'<div style="font:400 {gr}mm/1.45 {MO};letter-spacing:{sp}em;text-transform:uppercase;color:{farbe};text-wrap:balance">{e(ss(text))}</div>'


def ti(text, gr, farbe, sp=.12, zl=1.18):
    """Titel: Open Sans 400 in Versalien gesperrt"""
    return f'<div style="font:400 {gr}mm/{zl} {OS};letter-spacing:{sp}em;text-transform:uppercase;color:{farbe};text-wrap:balance">{e(ss(text))}</div>'


def tx(text, gr, farbe, breite=None, zl=1.48, ausr='center'):
    b = f'max-width:{breite}mm;' if breite else ''
    return f'<div style="font:400 {gr}mm/{zl} {IN};color:{farbe};{b}text-align:{ausr};text-wrap:pretty">{e(ss(text))}</div>'


def li(b, farbe, d=.35):
    return f'<i style="display:block;width:{b}mm;height:{d}mm;background:{farbe};flex:none"></i>'


def nabe(b, farbe, d=.35):
    """der Horizont mit runder Nabe in der Mitte (Form des Hauses: Naben statt Rauten)"""
    return (f'<div style="display:flex;align-items:center;gap:1.6mm;flex:none"><i style="display:block;width:{b / 2}mm;height:{d}mm;background:{farbe}"></i>'
            f'<i style="display:block;width:{d * 4.4}mm;height:{d * 4.4}mm;border-radius:50%;border:{d}mm solid {farbe}"></i><i style="display:block;width:{b / 2}mm;height:{d}mm;background:{farbe}"></i></div>')


def ab(mm):
    return f'<i style="display:block;height:{mm}mm;flex:none"></i>'


def feld(name, b, farbe, linie, gr=2):
    return (f'<div style="width:{b}mm;text-align:left;flex:none">{et(name, gr, farbe, .14)}<i style="display:block;height:{gr * 3.6}mm"></i>'
            f'<i style="display:block;height:.22mm;background:{linie}"></i></div>')


def reihe(*teile, gap=6):
    return f'<div style="display:flex;gap:{gap}mm;justify-content:center;flex:none">{"".join(teile)}</div>'


def foto(key, b, h, lage='50% 50%'):
    return f'<img src="{e(PH.bild_satz(key))}" style="display:block;width:{b}mm;height:{h}mm;object-fit:cover;object-position:{lage};flex:none" alt="">'


def seite(b, h, ton, inhalt, rahmen=True, kopf='', fuss='', extra='', unten=''):
    """Eine Seite: Rahmen, Kopf- und Fusszeile gleich weit vom Rahmen, die Gruppe im Fluss auf der optischen Mitte (Kriterium 10)."""
    T, u = TOENE[ton], min(b, h)
    r = max(4.5, .045 * u); a = r + max(3.5, .05 * u); g = max(1.6, .014 * u)
    rah = (f'<i class="abs" style="left:{r}mm;top:{r}mm;width:{b - 2 * r}mm;height:{h - 2 * r}mm;border:{max(.25, .0018 * u):.2f}mm solid {T["rahmen"]};'
           f'border-radius:{max(1.2, .011 * u):.2f}mm"></i>') if rahmen else ''
    k = f'<div class="abs" style="left:0;top:{a}mm;width:{b}mm;text-align:center">{et(kopf, g, T["et"], .16)}</div>' if kopf else ''
    f = f'<div class="abs" style="left:{r + .06 * u}mm;bottom:{a}mm;width:{b - 2 * (r + .06 * u)}mm;text-align:center">{et(fuss, g, T["et"], .1)}</div>' if fuss else ''
    ob, un = (a + g * 2.6) if kopf else r, (a + g * 2.6) if fuss else r
    mitte = (f'<div class="abs" style="left:{r + .07 * u}mm;width:{b - 2 * (r + .07 * u)}mm;top:{ob + .03 * u}mm;bottom:{un + .03 * u}mm;display:flex;flex-direction:column;'
             f'align-items:center;justify-content:safe center;text-align:center;padding-bottom:{.05 * (h - ob - un):.2f}mm">{inhalt}</div>')
    return blatt(b, h, f'<i class="abs" style="inset:0;{T["grund"]}"></i>' + extra + rah + k + mitte + f + unten, '', f'background:{T["bg"]}')


def bild_oben(b, h, ton, key, anteil, inhalt, lage='50% 50%', fuss=''):
    """Foto randlos oben, die Zeiger in einer Nabe auf der Naht, darunter die Gruppe."""
    T, u = TOENE[ton], min(b, h)
    ph = h * anteil; d = .15 * u
    oben = (f'<img class="abs" src="{e(PH.bild_satz(key))}" style="left:0;top:0;width:{b}mm;height:{ph}mm;object-fit:cover;object-position:{lage}">'
            f'<i class="abs" style="left:0;top:{ph - .2}mm;width:{b}mm;height:.4mm;background:{T["linie"]}"></i>'
            f'<i class="abs" style="left:{(b - d) / 2}mm;top:{ph - d / 2}mm;width:{d}mm;height:{d}mm;border-radius:50%;background:{T["bg"]};border:.35mm solid {T["linie"]}"></i>'
            f'<div class="abs" style="left:{(b - d * .34) / 2}mm;top:{ph - d * .34 * PH.ZV / 2}mm">{zw(d * .34, T["zeichen"])}</div>')
    r = max(4.5, .045 * u); a = r + max(3.5, .05 * u); g = max(1.6, .014 * u)
    f = f'<div class="abs" style="left:{r}mm;bottom:{a}mm;width:{b - 2 * r}mm;text-align:center">{et(fuss, g, T["et"], .1)}</div>' if fuss else ''
    mitte = (f'<div class="abs" style="left:{r + .06 * u}mm;width:{b - 2 * (r + .06 * u)}mm;top:{ph + d / 2 + .04 * u}mm;bottom:{(a + g * 2.6 if fuss else r) + .03 * u}mm;'
             f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">{inhalt}</div>')
    return blatt(b, h, f'<i class="abs" style="inset:0;{T["grund"]}"></i>' + oben + mitte + f, '', f'background:{T["bg"]}')


def zeile_zeit(paare, gr, ton, breite):
    """Tage und Zeiten als Liste: Tag in DM Mono, Zeit daneben, als Block mittig."""
    T = TOENE[ton]
    z = ''.join(f'<div style="display:flex;justify-content:space-between;gap:{gr * 1.4}mm;align-items:baseline;margin:{gr * .5}mm 0;border-bottom:.2mm solid {T["rahmen"]};padding-bottom:{gr * .5}mm">'
                f'<span style="font:400 {gr * .78}mm/1.2 {MO};letter-spacing:.12em;text-transform:uppercase;color:{T["et"]};text-align:left">{e(ss(a))}</span>'
                f'<span style="font:400 {gr}mm/1.25 {IN};color:{T["text"]};text-align:right">{e(ss(b))}</span></div>' for a, b in paare)
    return f'<div style="width:{breite}mm;flex:none">{z}</div>'


FUSS = f'{NAME} · {ADR}'
FUSS_KURZ = f'{ss(HJ["strasse"])} · Bottighofen'
ZEITEN = [(TAGE, OFFEN), ('Küche', ' und '.join(KUECHE)), ('Lästermeile', 'den ganzen Tag'), (RUHE.replace(' Ruhetag', ''), 'Ruhetag')]


# ============================================================ die eigenen Stücke
def gutschein():
    """DIN lang quer, 210 × 100: vorn Nacht mit den Zeigern, hinten Felder wie auf der Gutschein-Seite."""
    T = TOENE['nacht']
    v = seite(210, 100, 'nacht', zw(11, HIMMEL) + ab(4.6) + ti('Gutschein', 13, BLATT, .2, 1) + ab(4.2) + nabe(26, HIMMEL) + ab(4.2)
              + et('Ein Tisch am Hafen', 2.6, HIMMELH, .2), kopf=NAME, fuss=FUSS_KURZ)
    t2 = TOENE['blatt']
    r = seite(210, 100, 'blatt', reihe(feld('Für', 58, t2['et'], 'rgba(4,16,35,.4)'), feld('Von', 58, t2['et'], 'rgba(4,16,35,.4)'), gap=10) + ab(7)
              + reihe(feld('Ein Satz dazu', 126, t2['et'], 'rgba(4,16,35,.4)')) + ab(7)
              + reihe(feld('Betrag CHF', 36, t2['et'], 'rgba(4,16,35,.4)'), feld('Gültig bis', 36, t2['et'], 'rgba(4,16,35,.4)'), feld('Nr.', 36, t2['et'], 'rgba(4,16,35,.4)'), gap=9),
              kopf=f'{NAME} · {BY}', fuss=f'{ADR} · {TEL} · {WEBSITE}')
    return [v, r]


def tischkarte():
    """A6 quer zum Aufstellen: vorn «Reserviert», hinten der Satz zur Terrasse."""
    t2 = TOENE['blatt']
    v = seite(148, 105, 'blatt', zw(9, STUHL) + ab(4) + ti('Reserviert', 10.4, STUHL, .2, 1) + ab(4) + nabe(22, HIMMEL) + ab(5.5)
              + reihe(feld('Für', 50, t2['et'], 'rgba(4,16,35,.4)', 1.9), feld('Um', 26, t2['et'], 'rgba(4,16,35,.4)', 1.9), gap=8), kopf=NAME, fuss='Terrasse · Gaststube · Lästermeile')
    r = seite(148, 105, 'nacht', ti(HJ['satz_terrasse'], 6, BLATT, .12, 1.3) + ab(3.4) + et(HJ['satz_terrasse_von'], 1.9, HIMMEL) + ab(4.4) + nabe(20, HIMMEL) + ab(4.4)
              + tx(HJ['satz_lage'], 3.2, HIMMELH, 104), kopf=NAME, fuss=FUSS_KURZ)
    return [v, r]


def menuekarte():
    """A5 hoch: Menükarte für eine Feier, Gänge aus den Bankettmenüvorschlägen (Herbst), ohne Preise; hinten Banketts & Gruppen."""
    m = next(x for x in BK['menues'] if x['name'] == 'Herbst')
    g = ''
    for x in m['gerichte']:
        g += ti(ganz(x['name']), 3.5 if len(x['name']) < 30 else 3, STUHL, .12, 1.3) + ab(1.6) + tx(ganz(x['text']), 2.9, TINTE, 100) + ab(6.2)
    t2 = TOENE['blatt']
    v = seite(148, 210, 'blatt', zw(10, STUHL) + ab(4.5) + ti('Ihr Menü', 8, STUHL, .2, 1) + ab(4) + nabe(24, HIMMEL) + ab(5)
              + reihe(feld('Anlass', 46, t2['et'], 'rgba(4,16,35,.4)', 1.9), feld('Datum', 30, t2['et'], 'rgba(4,16,35,.4)', 1.9), gap=8) + ab(10) + g,
              kopf=NAME, fuss=FUSS)
    r = seite(148, 210, 'nacht', zw(14, HIMMEL) + ab(8) + ti(HJ['bankett']['titel'], 6.4, BLATT, .16) + ab(5) + nabe(24, HIMMEL) + ab(6)
              + tx(ganz(HJ['bankett']['platz']), 3.3, HIMMELH, 104) + ab(5) + tx(ganz(HJ['bankett']['individuell']), 3.3, HIMMELH, 104),
              kopf=NAME, fuss=f'{TEL} · {MAIL}')
    return [v, r]


def aushang():
    """A4 hoch: Betriebsferien, Foto oben (Abend unter der Platane), Zeiten aus haus.json."""
    fer = ''.join(ti(ganz(f).replace(' - ', ' bis '), 5, BLATT, .06, 1.3) + ab(3) for f in HJ['ferien'])
    inn = (ti('Betriebsferien', 8.2, BLATT, .2, 1) + ab(6) + fer + ab(3) + nabe(26, HIMMEL) + ab(6)
           + tx(f'{TAGE}, {OFFEN}. {RUHE}.', 3.7, HIMMELH, 160) + ab(2.4) + tx(ganz(HJ['zeiten']['laestermeile']), 3.7, HIMMELH, 160) + ab(9) + wm(110, BLATT))
    return [bild_oben(210, 297, 'nacht', 'abend', .40, inn, '50% 62%', fuss=f'{ADR} · {TEL}')]


def briefpapier():
    """Briefbogen A4 und Couvert C5/6 (229 × 114)."""
    bogen = (f'<i class="abs" style="inset:0;background:{WEISS}"></i>'
             f'<div class="abs" style="left:0;top:14mm;width:210mm;display:flex;flex-direction:column;align-items:center">{zw(10, STUHL)}{ab(4)}{wm(96, STUHL)}{ab(2.6)}{et(BY, 1.9, HIMMELT, .2)}</div>'
             f'<i class="abs" style="left:25mm;top:46mm;width:160mm;height:.25mm;background:{HIMMEL}"></i>'
             f'<i class="abs" style="left:4mm;top:105mm;width:5mm;height:.15mm;background:rgba(4,16,35,.5)"></i><i class="abs" style="left:4mm;top:210mm;width:5mm;height:.15mm;background:rgba(4,16,35,.5)"></i>'
             f'<i class="abs" style="left:25mm;top:271mm;width:160mm;height:.25mm;background:{HIMMEL}"></i>'
             f'<div class="abs" style="left:0;top:275mm;width:210mm;text-align:center">{et(FUSS, 1.9, TINTE, .1)}{et(f"{TEL} · {MAIL} · {WEBSITE}", 1.9, LEISE, .06)}</div>')
    couvert = (f'<i class="abs" style="inset:0;background:{NACHT} {TAPETE}"></i>'
               f'<i class="abs" style="left:5mm;top:5mm;width:219mm;height:104mm;border:.25mm solid rgba(162,182,207,.55);border-radius:2mm"></i>'
               f'<div class="abs" style="left:14mm;top:14mm;display:flex;align-items:center;gap:4mm">{zw(7, HIMMEL)}<div>{wm(62, BLATT)}{ab(1.6)}{et(ADR, 1.8, HIMMEL, .1)}</div></div>'
               f'<i class="abs" style="left:122mm;top:52mm;width:92mm;height:44mm;background:{WEISS};border-radius:1.6mm"></i>')
    return [blatt(210, 297, bogen, '', f'background:{WEISS}'), blatt(229, 114, couvert, '', f'background:{NACHT}')]


def lunch():
    """A5 hoch: das Lunch-Menü der Woche als Tafel (eine Karte: Preis wie im Original)."""
    g = ''.join(ti(ganz(x['name']), 5, STUHL, .1, 1.2) + ab(1.6) + tx(ganz(x['text']).replace(' – ', ' · '), 3.1, TINTE, 100) + ab(7.5) for x in LU['gaenge'])
    preis = f"3 Gänge · CHF {LU['preis_zahl']}"
    v = seite(148, 210, 'blatt', zw(10, STUHL) + ab(4.5) + et('Mittags am Hafen', 2.2, HIMMELT, .2) + ab(2.4) + ti('Lunch', 12, STUHL, .24, 1) + ab(4) + nabe(24, HIMMEL) + ab(10)
              + g + ab(1) + et(preis, 2.6, HIMMELT, .16) + ab(2) + tx('Küche ' + KUECHE[0], 2.8, LEISE),
              kopf=NAME, fuss=FUSS)
    return [v]


def tapas():
    """A6 hoch, Aufsteller für die Lästermeile: vorn Tapas durchgehend, hinten die Zeiten."""
    namen = [ganz(x['name']) for x in LM['gruppen'][0]['eintraege']]
    v = seite(105, 148, 'stuhl', zw(10, HIMMELH) + ab(4.5) + et('Lästermeile', 2.1, HIMMELH, .24) + ab(2.6) + ti(LM['gruppen'][0]['titel'], 7, WEISS, .14, 1.2) + ab(4) + nabe(20, HIMMELH) + ab(5)
              + ''.join(et(n, 2.3, PAPIER, .14) + ab(1.8) for n in namen), kopf=NAME, fuss=FUSS_KURZ)
    r = seite(105, 148, 'blatt', ti('Den ganzen Tag', 6.2, STUHL, .12, 1.2) + ab(3.4) + tx(ganz(HJ['zeiten']['laestermeile']), 3, TINTE, 78) + ab(5) + nabe(20, HIMMEL) + ab(5)
              + zeile_zeit(ZEITEN, 2.9, 'blatt', 76), kopf=NAME, fuss=FUSS_KURZ)
    return [v, r]


def wein():
    """A7 hoch, Kärtchen zum Glas: der Satz von Jonas Volpert, Platz für den Wein des Abends."""
    t2 = TOENE['blatt']
    v = seite(74, 105, 'nacht', zw(8, HIMMEL) + ab(3.6) + et('Jonas Volpert empfiehlt', 1.7, HIMMEL, .16) + ab(2.4) + ti('Ein Glas dazu', 4.6, BLATT, .12, 1.2) + ab(3) + nabe(14, HIMMEL) + ab(3.4)
              + tx(ganz(HJ['zitat_jonas']), 2.5, HIMMELH, 56), kopf='', fuss='Gastgeber und Sommelier')
    r = seite(74, 105, 'blatt', feld('Der Wein', 54, t2['et'], 'rgba(4,16,35,.4)', 1.7) + ab(5) + feld('Herkunft', 54, t2['et'], 'rgba(4,16,35,.4)', 1.7) + ab(5)
              + feld('Zum Gang', 54, t2['et'], 'rgba(4,16,35,.4)', 1.7), kopf=NAME, fuss=FUSS_KURZ)
    return [v, r]


def allergien():
    """A7 quer, Kärtchen am Platz: die Allergene der Karte, wie auf der Karte der Lästermeile."""
    teile = [x.strip() for x in LM['allergene'].split(',')]
    liste = ''.join(f'<div style="display:flex;gap:1.6mm;align-items:baseline;text-align:left"><span style="flex:none;width:5.4mm;font:400 2.1mm/1.3 {MO};letter-spacing:.06em;color:{HIMMELT}">{e(a.split(" = ")[0])}</span>'
                    f'<span style="font:400 2.4mm/1.3 {IN};color:{TINTE}">{e(ss(a.split(" = ")[1]))}</span></div>' for a in teile)
    v = seite(105, 74, 'blatt', ti('Was dürfen wir weglassen?', 4.4, STUHL, .1, 1.25) + ab(2.6) + nabe(16, HIMMEL) + ab(3)
              + f'<div style="display:grid;grid-template-columns:repeat(3,auto);gap:1.2mm 5mm;flex:none">{liste}</div>', kopf=NAME, fuss='Sagen Sie es uns bei der Bestellung')
    return [v]


def platzkarte():
    """A7 quer, gefalzt: Platzkarte für eine Feier, Name zum Eintragen."""
    t2 = TOENE['blatt']
    v = seite(105, 74, 'blatt', zw(7, STUHL) + ab(3.4) + feld('Ihr Platz', 64, t2['et'], 'rgba(4,16,35,.4)', 1.8) + ab(3.4) + et(HJ['bankett']['titel'], 1.7, HIMMELT, .16), kopf='', fuss='')
    r = seite(105, 74, 'nacht', wm(66, BLATT) + ab(3) + et(BY, 1.8, HIMMEL, .2), kopf='', fuss='')
    return [v, r]


def visitenkarte():
    """85 × 55 mm, zwei Seiten: vorn die Wortmarke auf der Nacht, hinten Adresse, Telefon, Instagram und Zeiten."""
    v = seite(85, 55, 'nacht', zw(7, HIMMEL) + ab(3) + wm(62, BLATT) + ab(2.2) + et(BY, 1.6, HIMMEL, .2), rahmen=False)
    r = seite(85, 55, 'blatt', et(NAME, 1.9, STUHL, .14) + ab(1.6) + tx(f'{HJ["strasse"]}, {HJ["ort"]}', 2.3, TINTE) + ab(.6) + tx(f'{TEL} · {MAIL}', 2.1, TINTE) + ab(.6)
              + tx(f'{IG} · {WEBSITE}', 2.1, LEISE) + ab(2) + li(10, HIMMEL) + ab(2) + et(f'{TAGE} · {OFFEN}', 1.5, HIMMELT, .1), rahmen=False)
    return [v, r]


def einladung():
    """Quadrat 148 × 148, zwei Seiten: das Four-Hands-Dinner auf der Excellence (haus.json › anlaesse)."""
    a = next(x for x in HJ['anlaesse'] if x.get('bevorstehend'))
    v = bild_oben(148, 148, 'nacht', 'anguria', .46,
                  et('Wir laden ein', 2, HIMMEL, .2) + ab(2.4) + ti('Four Hands', 8, BLATT, .2, 1) + ab(2.4) + tx(ganz(a['text'][0]).rstrip('!') + '.', 3.2, HIMMELH, 110) + ab(3) + et(a['datum'], 2.2, HIMMEL, .16),
                  '50% 62%', fuss=NAME)
    r = seite(148, 148, 'blatt', ti(a['titel'], 5.4, STUHL, .14, 1.25) + ab(3.4) + nabe(22, HIMMEL) + ab(4.4)
              + tx(ganz(a['text'][1]), 3.1, TINTE, 112) + ab(2.6) + tx(ganz(a['text'][2]).replace(' - ', ', '), 3.1, TINTE, 112) + ab(4)
              + et(ganz(a['zeit']), 2, HIMMELT, .1) + ab(2.4) + tx(ganz(a['text'][4]).replace('an Board', 'an Bord'), 2.7, LEISE, 112),
              kopf=NAME, fuss=f'{TEL} · {MAIL}')
    return [v, r]


def besen():
    """A5 hoch, zum Lesen am Tisch: die Geschichte vom Besen (haus.json › besen)."""
    s = HJ['besen']
    v = seite(148, 210, 'nacht', zw(12, HIMMEL) + ab(6) + et('Seit dem 17. Jahrhundert', 2.2, HIMMEL, .2) + ab(3) + ti('Ein Besen statt eines Schilds', 7.4, BLATT, .12, 1.25) + ab(5) + nabe(24, HIMMEL) + ab(6)
              + tx(ganz(s[0]), 3.3, HIMMELH, 104) + ab(3) + tx(ganz(s[1]), 3.3, HIMMELH, 104) + ab(3) + tx(ganz(s[2]), 3.3, HIMMELH, 104),
              kopf=NAME, fuss=FUSS_KURZ)
    return [v]


def anfahrt():
    """DL hoch, 99 × 210: der Weg ans Wasser, über Land und mit dem Zug (haus.json › anfahrt, bahn)."""
    v = bild_oben(99, 210, 'blatt', 'bootshafen', .36,
                  et('Der Weg', 2, HIMMELT, .2) + ab(2.2) + ti('Direkt im Hafen', 5.6, STUHL, .12, 1.2) + ab(3.6)
                  + tx(ganz(HJ['anfahrt']), 2.8, TINTE, 78) + ab(3) + tx('Mit dem Zug bis Bahnhof Bottighofen, von dort wenige Schritte zum Hafen.', 2.8, TINTE, 78) + ab(4)
                  + et(f'{HJ["strasse"]} · Bottighofen', 1.8, HIMMELT, .12) + ab(1.4) + et(f'{PH.HJ["koordinaten"][0]:.4f} N · {PH.HJ["koordinaten"][1]:.4f} O', 1.6, LEISE, .08),
                  '50% 50%', fuss=PH.nachweis('bootshafen'))
    return [v]


# ============================================================ Untersetzer der Lästermeile (rund, je 94 mm): zwölf in den Tönen des Sees
D = 94
R_ = D / 2


def kreis():
    return f'M{R_} 0A{R_} {R_} 0 1 1 {R_ - .01} 0Z'


def ring(ident, text, farbe, rr=38, g=2.5):
    return bogen_text(ident + 'r', f'M{R_ - rr} {R_}A{rr} {rr} 0 1 1 {R_ + rr} {R_}A{rr} {rr} 0 1 1 {R_ - rr} {R_}', (e(ss(text).upper()) + ' · ') * 2, g, farbe, 'm', .18)


def us(ident, grund, linie, innen, name, satz):
    z = f'<path d="{kreis()}" fill="{grund}"/><circle cx="{R_}" cy="{R_}" r="{R_ - 3}" fill="none" stroke="{linie}" stroke-width=".35"/>' + innen
    return etikett(ident, D, D, kreis(), z, name, satz)


def ts(x, y, text, gr, farbe, sp=.12):
    """Titel in Open Sans, Versalien gesperrt"""
    return tx_svg(x, y, vers(text), gr, farbe, 's', sp)


def ms(x, y, text, gr, farbe, sp=.18):
    return tx_svg(x, y, vers(text), gr, farbe, 'm', sp)


def tx_svg(x, y, text, gr, farbe, art, sp):
    return P.tx(x, y, text, gr, farbe, art, sp)


def horizont(y, b, farbe):
    """Horizont mit Nabe, im SVG"""
    return (f'<rect x="{R_ - b / 2}" y="{y - .17}" width="{b / 2 - 2}" height=".35" fill="{farbe}"/><rect x="{R_ + 2}" y="{y - .17}" width="{b / 2 - 2}" height=".35" fill="{farbe}"/>'
            f'<circle cx="{R_}" cy="{y}" r="1.1" fill="none" stroke="{farbe}" stroke-width=".35"/>')


def untersetzer_alle():
    T = [ganz(x['name']) for g in LM['gruppen'] for x in g['eintraege']]
    zh = 22 * PH.ZV
    U = []
    # vier mit den Zeigern
    U.append(us('u01', STUHL, HIMMELH, hzz(R_, R_ - 15, 14, HIMMELH) + ms(R_, R_ + 16, 'Lästermeile', 3.2, WEISS, .24) + horizont(R_ + 21, 22, HIMMELH) + ring('u01', f'{NAME} · Bottighofen', HIMMELH),
                'Die Zeiger', 'Stuhlblau, in der Mitte die Zeiger, ringsum der Name des Hauses.'))
    U.append(us('u02', BLATT, STUHL, hzz(R_, R_ - 15, 14, STUHL) + ms(R_, R_ + 16, 'Lästermeile', 3.2, STUHL, .24) + horizont(R_ + 21, 22, HIMMEL) + ring('u02', HJ['satz_lage'].split(' gelegen')[0], HIMMELT, g=2.3),
                'Direkt im Hafen', 'Papier, die Zeiger in Stuhlblau, ringsum der Satz zur Lage.'))
    U.append(us('u03', HIMMEL, STUHL, hzz(R_, R_ - 15, 14, NACHT) + ms(R_, R_ + 16, 'Bottighofen', 3.2, NACHT, .24) + horizont(R_ + 21, 22, NACHT) + ring('u03', 'Mit Blick aufs Wasser und die Alpen', NACHT, g=2.3),
                'Seehimmel', 'Im Seehimmel, die Zeiger in der Nacht über dem See.'))
    U.append(us('u04', NACHT, HIMMEL, hzz(R_, R_ - 15, 14, HIMMEL) + ms(R_, R_ + 16, BY, 2.6, BLATT, .18) + horizont(R_ + 21, 22, HIMMEL) + ring('u04', NAME, HIMMEL),
                'By Christian Kuchler', 'Nacht über dem See, die Zeiger und die Zeile des Logos.'))
    # zwei mit dem Namen der Bar und der Spalte der Karte
    U.append(us('u05', BLATT, STUHL, ts(R_, R_ - 1, 'Läster', 9, STUHL, .16) + ts(R_, R_ + 10, 'meile', 9, HIMMELT, .16) + horizont(R_ + 16, 22, HIMMEL) + ring('u05', f'{NAME} · {BY}', HIMMELT, g=2.3),
                'Lästermeile', 'Der Name der Bar, geteilt wie auf der Startseite.'))
    U.append(us('u06', STUHL, HIMMELH, ts(R_, R_ - 2, 'Tapas', 8.6, WEISS, .2) + ms(R_, R_ + 7, 'durchgehend', 3.6, HIMMELH, .24) + horizont(R_ + 13, 22, HIMMELH) + ring('u06', f'{TAGE} · {OFFEN}', HIMMELH, g=2.3),
                'Tapas durchgehend', 'Die erste Spalte der Karte der Lästermeile, ringsum die Zeiten.'))
    # vier Gerichte der Lästermeile, Namen wie auf der Karte
    toene = [(BLATT, STUHL, HIMMELT), (NACHT, BLATT, HIMMEL), (HIMMEL, NACHT, NACHT), (STUHL, WEISS, HIMMELH)]
    for i, n in enumerate([x for x in T if len(x) <= 19][:4]):
        grund, schrift, linie = toene[i]
        w = n.split(' ')
        zl = [' '.join(w[:(len(w) + 1) // 2]), ' '.join(w[(len(w) + 1) // 2:])] if len(n) > 11 and len(w) > 1 else [n]
        gr = 6.2 if max(len(z) for z in zl) < 9 else (5 if max(len(z) for z in zl) < 12 else 4.2)
        innen = hzz(R_, R_ - 22, 8, linie) + ''.join(ts(R_, R_ + 2 + j * (gr + 1.6) - (len(zl) - 1) * (gr + 1.6) / 2, z, gr, schrift, .12) for j, z in enumerate(zl))
        innen += horizont(R_ + 10 + (len(zl) - 1) * 3, 22, linie) + ms(R_, R_ + 19 + (len(zl) - 1) * 3, 'Lästermeile', 2.4, linie, .26)
        U.append(us(f'u{7 + i:02d}', grund, linie, innen, n.title() if n.isupper() else n, 'Ein Gericht der Lästermeile, Name wie auf der Karte.'))
    U.append(us('u11', NACHT, HIMMEL, ms(R_, R_ - 9, 'Zur Stärkung', 4, BLATT, .16) + ts(R_, R_ + 1.5, '& Süsses', 6.4, HIMMEL, .14) + horizont(R_ + 8, 22, HIMMEL) + ring('u11', 'Lästermeile · Bottighofen', HIMMEL),
                'Zur Stärkung & Süsses', 'Die zweite Spalte der Karte der Lästermeile.'))
    U.append(us('u12', BLATT, STUHL, ts(R_, R_ - 3, 'Die schönste', 4.8, STUHL, .12) + ts(R_, R_ + 4.4, 'Terrasse', 4.8, STUHL, .12) + ts(R_, R_ + 11.8, 'am Bodensee', 4.8, STUHL, .12)
                + horizont(R_ + 17, 22, HIMMEL) + ring('u12', HJ['satz_terrasse_von'], HIMMELT) + hzz(R_, R_ - 24, 8, STUHL),
                'Die schönste Terrasse', f'Der Satz von {HJ["satz_terrasse_von"]}, auf dem Papier der Karte.'))
    return U


# ============================================================ die Drucksachen der Hausdruckerei (nur kopiert)
HD_TEXT = {   # Titel und Satz je Drucksache der Hausdruckerei (Inhalt aus ihrer liste.json, in den Worten der Werkbank)
    'aushang-betriebsferien': (['Wenn das Schlössli', 'Pause macht.'], 'Der Aushang für Tür und Bar zu den Betriebsferien im Winter, vom 22. Dezember bis zum 10. Februar.'),
    'aushang-kreuzfahrt-geschlossen': (['Geschlossen,', 'das Team ist an Bord.'], 'Vom 13. bis 15. November ist das Haus zu, weil das ganze Team auf der Excellence kocht. Das Blatt sagt es an der Tür.'),
    'aushang-oeffnungszeiten': (['Die', 'Öffnungszeiten.'], 'Donnerstag bis Montag, die Zeiten der Küche und der Ruhetag auf einem Blatt A4 für die Tür.'),
    'aushang-ruhetag': (['Heute', 'ist Ruhetag.'], 'Ein kleines Blatt A5 für die Tür an den Ruhetagen Dienstag und Mittwoch.'),
    'aushang-besen': (['Statt eines Schilds', 'ein Besen.'], 'Die Geschichte vom Haus am See als Aushang A4, zum Lesen im Eingang.'),
    'plakat-terrasse': (['Die schönste', 'Terrasse.'], 'Ein Plakat A3 mit der Terrasse am Mittag, für das Fenster oder den Steg.'),
    'einladung-gourmetkreuzfahrt': (['Four Hands', 'an Bord.'], 'Die Einladung zum Four-Hands-Dinner mit Dieter Koschina auf der Excellence, quadratisch zum Verschicken.'),
    'programm-die-reise': (['Die', 'Reise.'], 'Das Programm der Gourmetkreuzfahrt auf A5: von Basel nach Strassburg und zurück.'),
    'flyer-banketts': (['Banketts', 'und Gruppen.'], 'Das Angebotsblatt A5 für Feiern auf zwei Etagen mit je bis zu 26 Personen.'),
    'menuekarte-lunch': (['Das Lunch-Menü', 'der Woche.'], 'Die drei Gänge am Mittag als schmale Menükarte für den Tisch.'),
    'menuekarte-bankett-herbst': (['Ein Menü', 'im Herbst.'], 'Das Bankettmenü des Herbsts auf A5, fünf Gerichte für den Tisch der Feier.'),
    'menuekarte-bankett-sommer': (['Ein Menü', 'im Sommer.'], 'Das Bankettmenü des Sommers auf A5, fünf Gerichte für den Tisch der Feier.'),
    'einleger-italien': (['Aus', 'Italien.'], 'Ein Einleger A5 für die Karte mit den Gerichten aus Italien, ohne Preise.'),
    'einleger-klassiker': (['Die', 'Klassiker.'], 'Ein Einleger A5 mit den Klassikern der Karte, ohne Preise.'),
    'wein-buendner-herrschaft': (['Ein Glas aus der', 'Bündner Herrschaft.'], 'Die Weinempfehlung als schmale Karte: ein Pinot Noir aus der Bündner Herrschaft.'),
    'wein-burgund': (['Ein Glas', 'aus dem Burgund.'], 'Die Weinempfehlung als schmale Karte: ein Weisswein aus dem Burgund.'),
    'wein-champagne': (['Ein Glas', 'Champagne.'], 'Die Weinempfehlung als schmale Karte für den Champagner zum Apéro.'),
    'laestermeile-tapas': (['Die Karte', 'der Lästermeile.'], 'Die Karte der Lästermeile auf A5, für die Tische an der Promenade.'),
    'hinweiskarte-laestermeile': (['Den ganzen', 'Tag geöffnet.'], 'Ein Aufsteller A6: die Karte der Lästermeile gibt es den ganzen Tag.'),
    'hinweiskarte-allergien': (['Was dürfen wir', 'weglassen?'], 'Eine Hinweiskarte A6 am Tisch mit den Allergenen, wie sie auf Ihren Karten stehen.'),
    'tischkarte-reserviert': (['Dieser Tisch', 'ist reserviert.'], 'Die Tischkarte A7 für reservierte Tische in der Gaststube und an der Lästermeile.'),
    'tischkarte-terrasse': (['Reserviert', 'auf der Terrasse.'], 'Dieselbe Tischkarte für die Tische auf der Seeterrasse.'),
    'gutschein': (['Ein Gutschein', 'zum Verschenken.'], 'Der Gutschein in DL quer, vorne die Zeiger, hinten für wen, von wem und der Betrag.'),
    'flyer-des-hauses': (['Der Flyer', 'des Hauses.'], 'Ein Flyer A6: vorne die Terrasse, hinten die Zeiten und der Weg.'),
    'pressemappe': (['Die', 'Pressemappe.'], 'Das Deckblatt A4 der Pressemappe, für Anfragen von Zeitungen und Guides.'),
    'teamaushang-ablauf-bankett': (['Ablauf', 'eines Banketts.'], 'Ein Aushang A4 für das Team: wie ein Bankett abläuft, Schritt für Schritt.'),
    'teamaushang-kuechenzeiten': (['Die', 'Küchenzeiten.'], 'Ein Aushang A4 für das Team mit den Zeiten der Küche und der Lästermeile.'),
    'instagram-laestermeile': (['Die Lästermeile', 'auf Instagram.'], 'Ein Beitrag 4:5 für Instagram: die Bar am Hafen.'),
    'instagram-monika-huber': (['Monika Huber', 'auf Instagram.'], 'Ein Beitrag 4:5 für Instagram über die Küchenchefin.'),
    'instagram-weinkeller': (['Der Weinkeller', 'auf Instagram.'], 'Ein Beitrag 4:5 für Instagram mit dem Satz von GaultMillau über den Keller.'),
    'story-four-hands': (['Four Hands', 'als Story.'], 'Eine Story 9:16 für Instagram zum Four-Hands-Dinner an Bord.'),
    'story-terrasse': (['Die Terrasse', 'als Story.'], 'Eine Story 9:16 für Instagram: unter den Platanen.'),
}


def hausdruckerei(eigene):
    """liste.json der Hausdruckerei → drucksachen/img/hd-*.webp, drucksachen/pdf/*.pdf, _werkbank/papier_mehr.json (vom Kit als weitere Stücke gezeigt).
    Fehlt die Liste noch, bleibt papier_mehr.json leer."""
    from PIL import Image
    img = os.path.join(ROOT, 'drucksachen', 'img'); pdf = os.path.join(ROOT, 'drucksachen', 'pdf')
    os.makedirs(img, exist_ok=True); os.makedirs(pdf, exist_ok=True)
    mehr = []
    lp = os.path.join(HD, 'liste.json')
    if os.path.exists(lp):
        for d in json.load(open(lp, encoding='utf-8')):
            k = d['k']
            if k in eigene or k.startswith('postkarte-'):   # gleiche Idee als eigenes Stück schon da; Postkarten auf ihrer eigenen Seite
                continue
            namen = []
            for j, v in enumerate(d['vorschau'][:2]):
                nm = 'hd-' + k + ('' if j == 0 else '-r')
                im = Image.open(os.path.join(HD, v)).convert('RGB')
                if im.width > 1000:
                    im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
                im.save(os.path.join(img, nm + '.webp'), 'WEBP', quality=86, method=5)
                namen.append((nm, im.size))
            ziel = f'{PH.KURZ}-{k}.pdf'
            shutil.copy2(os.path.join(HD, d['pdf']), os.path.join(pdf, ziel))
            hoch = namen[0][1][1] > namen[0][1][0]
            if len(namen) == 2:
                w = 44 if hoch else 84
                karton = [(namen[0][0], w, 'Vorderseite'), (namen[1][0], w, 'Rückseite')]
            else:
                r = namen[0][1][1] / namen[0][1][0]
                w = 40 if r > 1.6 else (54 if r > 1.3 else (64 if r > 1.05 else 86))
                karton = [(namen[0][0], w, '')]
            t = ss(d['n'])
            w2 = t.split(' ')
            titel, satz = HD_TEXT.get(k, ([' '.join(w2[:max(1, len(w2) // 2)]), ' '.join(w2[max(1, len(w2) // 2):]) + '.'] if len(w2) > 1 else ['Die', t + '.'], ss(d.get('was', ''))))
            mehr.append(dict(id='hd-' + k, name=ss(d['n']), format=ss(d['format']) + (' · ' + str(d['seiten']) + ' Seiten' if d.get('seiten', 1) > 1 else '') + ' · aus der Hausdruckerei',
                             satz=ss(satz), titel=titel, pdf=ziel, karton=karton, masse={n: list(s) for n, s in namen}, schatten=True, haengt=False, seiten=d.get('seiten', 1)))
    json.dump({'druck': mehr}, open(os.path.join(PH.W, 'papier_mehr.json'), 'w'), ensure_ascii=False, indent=1)
    return mehr


def baue():
    Dr, SEITE = [], {}

    def d(ident, name, format_, blaetter, karton, titel, satz, quelle, breit=True, folge=None):
        namen = [n for n, _, _ in karton]
        folge = folge or namen   # Reihenfolge der Blätter im Satz (Vorschaubild je Blatt)
        Dr.append(dict(id=ident, name=name, format=format_, blaetter=blaetter, vorschau=[(n, i + 1) for i, n in enumerate(folge)], satz=satz, quelle=quelle))
        SEITE[ident] = dict(karton=['', [list(x) for x in karton]], titel=titel, breit=sorted(namen) if breit else [])

    d('gutschein', 'Gutschein', 'DIN lang quer, 210 × 100 mm, zwei Seiten', gutschein(), [('gutschein', 88, 'Vorderseite'), ('gutschein-r', 88, 'Rückseite')],
      ['Ein Gutschein', 'zum Verschenken.'], 'Der Gutschein zum Verschenken, mit denselben Feldern wie auf der Gutschein-Seite: für wen, von wem, ein Satz dazu und der Betrag.',
      'Gutschein-Seite und Kontakt Ihrer Website')
    d('tischkarte', 'Tischkarte «Reserviert»', 'A6 quer, zum Aufstellen', tischkarte(), [('tischkarte', 47, 'Vorderseite'), ('tischkarte-r', 47, 'Rückseite')],
      ['Dieser Tisch', 'ist reserviert.'], 'Für reservierte Tische auf der Terrasse, in der Gaststube und an der Lästermeile. Hinten steht Ihr Satz zur Terrasse.', 'Startseite Ihrer Website')
    d('menuekarte', 'Menükarte für Ihre Feier', 'A5 hoch, zwei Seiten', menuekarte(), [('menuekarte', 44, 'Vorderseite'), ('menuekarte-r', 44, 'Rückseite')],
      ['Ein Menü', 'für Ihre Feier.'], 'Für jedes Bankett eine eigene Karte auf dem Tisch, hier mit dem Herbstmenü aus Ihren Bankettmenüvorschlägen. Anlass und Datum tragen Sie ein.',
      'Bankettmenüvorschläge, PDF vom 29.04.2025')
    d('lunch', 'Lunch-Tafel', 'A5 hoch', lunch(), [('lunch', 46, '')], ['Mittags', 'am Hafen.'],
      'Das Lunch-Menü der Woche als kleine Tafel für die Theke und den Eingang: drei Gänge und der Preis, wie auf Ihrer Lunch-Karte.', 'Lunch-Menü, PDF vom 18.10.2026')
    d('tapas', 'Aufsteller der Lästermeile', 'A6 hoch, zwei Seiten', tapas(), [('tapas', 40, 'Vorderseite'), ('tapas-r', 40, 'Rückseite')],
      ['Tapas', 'den ganzen Tag.'], 'Vorne die Tapas, die es an der Lästermeile durchgehend gibt, hinten die Zeiten der Woche. Steht auf den Tischen an der Promenade.',
      'Karte der Lästermeile, PDF vom 14.10.2026')
    d('aushang', 'Aushang Betriebsferien', 'A4 hoch', aushang(), [('aushang', 46, '')], ['Wenn das Schlössli', 'Pause macht.'],
      'Ein Blatt für die Tür und die Bar, wenn das Schlössli Pause macht, mit Ihren Ferien und Zeiten.', 'Kontakt-Seite Ihrer Website')
    d('einladung', 'Einladung Four Hands', 'Quadrat 148 × 148 mm, zwei Seiten', einladung(), [('einladung', 46, 'Vorderseite'), ('einladung-r', 46, 'Rückseite')],
      ['Four Hands', 'auf dem Schiff.'], 'Die Einladung zum Four-Hands-Dinner mit Dieter Koschina an Bord der Excellence, vorne der Abend am See, hinten der Ablauf aus Ihrer Seite «Events».',
      'Seite «Events» Ihrer Website')
    d('wein', 'Kärtchen zum Glas', 'A7 hoch, zwei Seiten', wein(), [('wein', 38, 'Vorderseite'), ('wein-r', 38, 'Rückseite')], ['Ein Glas', 'dazu.'],
      'Ein kleines Kärtchen, das zum Wein des Abends an den Tisch kommt: vorne der Satz von Jonas Volpert, hinten Platz für Wein, Herkunft und Gang.', 'Seite «Weinkarte» Ihrer Website')
    d('allergien', 'Allergien am Platz', 'A7 quer, 105 × 74 mm', allergien(), [('allergien', 60, '')], ['Was dürfen wir', 'weglassen?'],
      'Ein Kärtchen am Platz mit den Zeichen der Allergene, wie sie auf Ihren Karten stehen. Die Gäste sagen es bei der Bestellung.', 'Karte der Lästermeile')
    d('platzkarte', 'Platzkarte für Banketts', 'A7 quer, gefalzt, zwei Seiten', platzkarte(), [('platzkarte', 46, 'Vorderseite'), ('platzkarte-r', 46, 'Rückseite')],
      ['Ihr Platz', 'an der Tafel.'], 'Für die Feiern auf den zwei Etagen: vorne der Name des Gastes, hinten die Wortmarke.', 'Seite «Banketts & Gruppen»')
    d('besen', 'Ein Besen statt eines Schilds', 'A5 hoch', besen(), [('besen', 44, '')], ['Ein Besen', 'statt eines Schilds.'],
      'Die Geschichte vom Haus am See zum Lesen am Tisch: wie Ende des 17. Jahrhunderts statt eines Wirtshausschilds ein Besen heraushing.', 'Startseite Ihrer Website, «Der Besen»')
    d('anfahrt', 'Der Weg ans Wasser', 'DL hoch, 99 × 210 mm', anfahrt(), [('anfahrt', 36, '')], ['Direkt', 'im Hafen.'],
      'Ein schmales Blatt für die Post und den Tresen: der Weg über die Seestrasse zum Parkplatz und mit dem Zug zum Bahnhof Bottighofen.', 'Kontakt-Seite Ihrer Website')
    d('visitenkarte', 'Visitenkarte', '85 × 55 mm, zwei Seiten', visitenkarte(), [('visitenkarte', 60, 'Vorderseite'), ('visitenkarte-r', 60, 'Rückseite')],
      ['Die', 'Visitenkarte.'], 'Vorne die Wortmarke auf der Nacht über dem See, hinten Adresse, Telefon, Instagram und die Zeiten.', 'Fuss Ihrer Website')
    d('briefpapier', 'Briefpapier', 'Briefbogen A4, Couvert C5/6', briefpapier(), [('couvert', 92, 'Couvert'), ('briefbogen', 38, 'Briefbogen')],
      ['Briefbogen', 'und Couvert.'], 'Briefbogen und Couvert mit den Zeigern, der Wortmarke und Ihrer Adresse.', 'Kontakt Ihrer Website', folge=['briefbogen', 'couvert'])
    # Abgleich mit der Hausdruckerei: was sie schon setzt, kommt von dort (ein Weg je Ziel, Kriterium 15); Postkarten stehen auf der eigenen Seite
    lp = os.path.join(HD, 'liste.json')
    hd = {d['k'] for d in json.load(open(lp, encoding='utf-8'))} if os.path.exists(lp) else set()
    abdeckt = {'gutschein': 'gutschein', 'tischkarte': 'tischkarte-reserviert', 'menuekarte': 'menuekarte-bankett-herbst', 'lunch': 'menuekarte-lunch',
               'tapas': 'hinweiskarte-laestermeile', 'aushang': 'aushang-betriebsferien', 'einladung': 'einladung-gourmetkreuzfahrt', 'wein': 'wein-burgund',
               'allergien': 'hinweiskarte-allergien', 'besen': 'aushang-besen'}
    Dr = [x for x in Dr if abdeckt.get(x['id']) not in hd]
    SEITE = {k: v for k, v in SEITE.items() if k in {x['id'] for x in Dr}}
    mehr = hausdruckerei({x['id'] for x in Dr})
    json.dump(SEITE, open(os.path.join(PH.W, 'papier_neu_seite.json'), 'w'), ensure_ascii=False, indent=1)
    da = {n for x in Dr for n, _ in x['vorschau']} | {n for m in mehr for n, _, _ in m['karton']}
    wahl = [n for n in ('hd-plakat-terrasse', 'hd-gutschein', 'hd-einladung-gourmetkreuzfahrt', 'hd-aushang-oeffnungszeiten', 'visitenkarte', 'hd-tischkarte-reserviert',
                        'gutschein', 'menuekarte', 'einladung', 'tischkarte', 'aushang', 'lunch') if n in da][:6]
    orte = [(38, 0, 22, -3), (0, 8, 34, -5), (68, 4, 26, 5), (6, 50, 20, -4), (66, 58, 30, 5), (32, 60, 28, -3)]
    json.dump([(n,) + o for n, o in zip(wahl, orte)], open(os.path.join(PH.W, 'papier_auslage.json'), 'w'))
    P.fertig(Dr, untersetzer_alle(), MEINS)
    print('Hausdruckerei:', len(mehr), 'Drucksachen kopiert ·', len(Dr), 'eigene')


if __name__ == '__main__':
    baue()
