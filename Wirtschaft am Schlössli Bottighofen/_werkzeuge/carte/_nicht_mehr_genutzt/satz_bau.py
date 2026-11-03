#!/usr/bin/env python3
"""Die Tafel (La Carte) · Wirtschaft am Schlössli Bottighofen: setzt jede Karte des Hauses als Satz (19.10.2026).

Woher: die Karten als Daten aus Station 10 (Kartenmacher), `_karten/stand/<id>.json`, Format von La Carte im Stamm
(`_Werkzeuge/werkzeuge/karten/modell.py`), jeder Name, Text und Preis Zeichen für Zeichen aus dem Original gelesen (`_karten/lesen.py`,
Abgleich `_karten/abgleich.py`). Hier wird nichts abgetippt und nichts dazugeschrieben: jedes Stück der Daten kommt genau einmal in den Satz.

Wie: mit den Bausteinen des Werkbank-Kits (`_Werkbank-Kit/satz_kern.py`: blatt, band, rubrik, zwischen, posten, absatz), hier ohne `kern`
nachgebaut, damit das Werkzeug nur vom eigenen Ordner abhängt. Stil = `_Werkbank-Kit/satz.css`, Farben der Vorlage auf die Farben der
Website umgesetzt (assets/css/haus.css :root, Farbwelt A «Stuhl und See», Ton in Ton), Schriften des Hauses (Open Sans aus der Wortmarke,
Instrument Sans, DM Mono). Seiten wie im Original: jeder Posten trägt die Seite des Originals (`s`), dort beginnt ein neues Blatt.
Das Mittagsmenü (Lunch der Woche, C08) setzt nicht dieses Skript, sondern satz/satz.js aus der Woche (einlesen.py legt sie an).

    python3 _werkzeuge/carte/satz_bau.py     →  satz/u-<kennung>.html, satz/satz.css
Danach liest einlesen.py den Satz als Baum ein (C17, wie im Gasterntal, Ruedihus und Doldenhorn)."""
import html, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(HIER))
PROJ = WURZEL if os.path.isfile(os.path.join(WURZEL, 'bau.py')) else os.path.join(WURZEL, 'website')
KARTEN_DATEN = next(x for x in (os.path.join(WURZEL, '_karten', 'stand'), os.path.join(os.path.dirname(WURZEL), '_karten', 'stand')) if os.path.isdir(x))
KIT = os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit')
AUS = os.path.join(HIER, 'satz')
e = html.escape

NAME = 'Wirtschaft am Schlössli'
ORT = 'Bottighofen'
# Karten, die der Satz setzt: Kennung im Werkzeug → Datei aus Station 10. Reihenfolge = Reihenfolge im Werkzeug.
KARTEN = {
    'speisekarte': 'speisekarte',
    'laestermeile': 'laestermeile',
    'weinkarte': 'weinkarte',
    'bankett': 'bankett',
    'vier-haende': 'vier-haende',
}

# Farben der Vorlage (Werkbank-Kit, Grand Beau-Rivage) → Farben der Website des Schlössli (assets/css/haus.css :root)
FARBEN = {
    '#0b1f40': '#0b1d3d',    # Nacht der Vorlage → --nacht (Grund, Titel, Preise)
    '#a98a45': '#A2B6CF',    # Goldlinie → --himmel (Linien, Striche)
    '#dcc68f': '#C5D2E1',    # helles Gold auf Dunkel → --himmel-h
    '#8a7545': '#0F3678',    # dunkles Gold für kleine Zeilen auf Hell → --himmel-t
    '#f4ecdc': '#F3F6F9',    # helle Schrift auf Dunkel → --papier
    '#fbf6ea': '#F3F6F9',    # Blatt → --papier
    '#0c1526': '#041023',    # Tinte → --tinte
    '#8f8672': '#5b6577',    # Tisch hinter den Blättern (nur Bildschirm)
    'rgba(12,21,38': 'rgba(4,16,35',
    'rgba(169,138,69': 'rgba(162,182,207',
}


def zeichen_svg():
    s = open(os.path.join(PROJ, 'assets', 'svg', 'zeichen.svg'), encoding='utf-8').read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    innen = s[s.index('>') + 1:s.rindex('</svg>')]
    return f'<svg viewBox="{vb}" aria-hidden="true" fill="currentColor">{innen}</svg>'


Z = None


def blatt(teile, b, h, kopf='', fuss=''):
    f = f'<footer class="ufuss2">{e(fuss)}</footer>' if fuss else f'<footer class="ufuss2">{e(NAME)} · {e(ORT)}</footer>'
    return f'<section class="blatt" data-b="{b}" data-h="{h}" style="width:{b}mm;height:{h}mm">{kopf}<div class="inhalt">{"".join(teile)}</div>{f}</section>'


def band(titel, unter=''):
    return f'<header class="uband"><span class="uband__z">{Z}</span><div><h1>{e(titel)}</h1>' + (f'<p>{e(unter)}</p>' if unter else '') + '</div></header>'


def leiste(text=''):
    return f'<header class="uleiste"><span>{Z}</span>' + (f'<b>{e(text)}</b>' if text else '') + '</header>'


def deckblatt(titel, unter, zeilen):
    z = ''.join(f'<p>{e(x)}</p>' for x in zeilen)
    return f'<div class="udeck"><span class="udeck__z">{Z}</span><h1>{e(titel)}</h1><i></i>' + (f'<p class="udeck__u">{e(unter)}</p>' if unter else '') + z + '</div>'


def posten(p):
    """Ein Gericht oder Wein. Preise mit Angabe (Hauptgang, 0.7l) als Angabe + Preis, sonst nur der Preis."""
    pr = ''
    ein = p.get('einheiten') or []
    for i, x in enumerate(p.get('preise') or []):
        a = ein[i] if i < len(ein) else ''
        pr += f'<span class="pz"><em>{e(a)}</em><b>{e(x)}</b></span>' if a else f'<span class="pz"><b>{e(x)}</b></span>'
    zs = f' <small>{e(p["zusatz"])}</small>' if p.get('zusatz') else ''
    jg = f' <small class="jg">{e(p["jahr"])}</small>' if p.get('jahr') else ''
    zl = ''.join(f'<p>{e(z["text"])}</p>' for z in p.get('zeilen') or [])
    return f'<div class="po"><div class="po__t"><h4>{e(p["name"])}{jg}{zs}</h4>{zl}</div><div class="po__p">{pr}</div></div>'


def stueck(p):
    t = p['t']
    if t == 'rubrik':
        zs = f'<small>{e(p["zusatz"])}</small>' if p.get('zusatz') else ''
        return f'<h2 class="rubrik"><span>{e(p["titel"])}{zs}</span></h2>'
    if t == 'land':
        return f'<h3 class="zw zw--land">{e(p["text"])}</h3>'
    if t == 'zw':
        return f'<h3 class="zw{" zw--gut" if p.get("weingut") else ""}">{e(p["text"])}</h3>'
    if t == 'gericht':
        return posten(p)
    if t == 'notiz':
        return f'<p class="ab klein">{e(p["text"])}</p>'
    if t == 'frei':
        aus = ''
        for z in p.get('zeilen') or []:
            aus += f'<p class="stern">{e(z["text"])}</p>' if re.fullmatch(r'[*·\s]+', z['text']) else f'<p class="ab">{e(z["text"])}</p>'
        return aus
    raise SystemExit(f'Unbekannter Posten «{t}» – der Satz kennt ihn nicht, nichts wird still weggelassen.')


def setze(kennung, datei):
    d = json.load(open(os.path.join(KARTEN_DATEN, datei + '.json'), encoding='utf-8'))
    k = d['karte']
    b, h = k['format']
    seiten, deckel = {}, None
    for teil in k['teile']:
        if teil['art'] == 'deckel':
            deckel = teil
            continue
        for p in teil['posten']:
            seiten.setdefault(p.get('s', 1), []).append(stueck(p))
    fuss = k.get('fuss') or ''
    aus = []
    if deckel and deckel.get('aus_original'):          # das Original hat ein eigenes Deckblatt (Bankettmenü)
        aus.append(blatt([deckblatt(deckel['titel'], deckel.get('unter', ''), deckel.get('zeilen') or [])], b, h, '', fuss).replace('class="blatt"', 'class="blatt deck"', 1))
        deckel = None
    for i, nr in enumerate(sorted(seiten)):
        if i == 0 and deckel:                           # Titel der Karte als Band über der ersten Seite (kein eigenes Blatt, das Original hat keins)
            kopf = band(deckel['titel'], deckel.get('unter', ''))
        else:
            kopf = leiste(k['name'] if i else '')
        aus.append(blatt(seiten[nr], b, h, kopf, fuss))
    doc = (f'<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><title>{e(k["name"])} · {e(NAME)}</title>'
           f'<link rel="stylesheet" href="satz.css"><style>@page{{size:{b}mm {h}mm;margin:0}}</style></head><body>{"".join(aus)}</body></html>')
    os.makedirs(AUS, exist_ok=True)
    with open(os.path.join(AUS, 'u-' + kennung + '.html'), 'w', encoding='utf-8') as f:
        f.write(doc)
    return len(aus)


CSS_HAUS = """
/* Schlössli: Titel wie die Wortmarke (Open Sans, Versalien gesperrt), Rubriken mit der feinen Horizontlinie in Seehimmel statt der kurzen Goldlinie */
.uband h1,.udeck h1{text-transform:uppercase;letter-spacing:.16em;font-weight:400}
.uband h1{font-size:21pt}
.uband__z{width:13mm}
.rubrik{text-transform:uppercase;letter-spacing:.14em;font-weight:400;font-size:calc(15pt*var(--s))}
.rubrik::after{width:100%;height:.25mm}
.zw--land{font-size:calc(7.6pt*var(--s));color:#0b1d3d;margin-top:calc(4.6mm*var(--s))}
.zw--gut{font-family:'Instrument Sans',Arial,sans-serif;font-weight:600;font-size:calc(9.2pt*var(--s));letter-spacing:0;text-transform:none;color:#0b1d3d;margin:calc(2.8mm*var(--s)) 0 calc(.6mm*var(--s))}
.po h4 small.jg{font-family:'DM Mono',Menlo,monospace;font-size:calc(7.4pt*var(--s));letter-spacing:.06em;color:#0F3678}
.pz em{font-family:'DM Mono',Menlo,monospace;font-size:calc(6.8pt*var(--s));letter-spacing:.06em}
.udeck__n{font-family:'DM Mono',Menlo,monospace;font-size:8pt!important;letter-spacing:.24em;text-transform:uppercase;color:#C5D2E1;margin-top:auto!important;padding-top:12mm}
.blatt.deck .inhalt{padding:0}
.blatt.deck .udeck{margin:0}
.ufuss2{letter-spacing:.2em}
"""


def css():
    s = open(os.path.join(KIT, 'satz.css'), encoding='utf-8').read()
    for a, b in FARBEN.items():
        s = re.sub(re.escape(a), b, s, flags=re.I)
    kopf = ("@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;src:url('../fonts/OpenSans-var.ttf') format('truetype')}\n"
            "@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:400;src:url('../fonts/InstrumentSans-Regular.ttf') format('truetype')}\n"
            "@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:500;src:url('../fonts/InstrumentSans-Medium.ttf') format('truetype')}\n"
            "@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:600;src:url('../fonts/InstrumentSans-SemiBold.ttf') format('truetype')}\n"
            "@font-face{font-family:'DM Mono';font-style:normal;font-weight:400;src:url('../fonts/DMMono-Regular.ttf') format('truetype')}\n"
            ":root{--titel:'Open Sans',Arial,sans-serif;--tg:400;--muster:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='56'%3E%3Cg fill='%23A2B6CF' fill-opacity='.22'%3E%3Ccircle cx='14' cy='14' r='1.1'/%3E%3Ccircle cx='42' cy='14' r='1.1'/%3E%3Ccircle cx='14' cy='42' r='1.1'/%3E%3Ccircle cx='42' cy='42' r='1.1'/%3E%3C/g%3E%3Ccircle cx='28' cy='28' r='5' fill='none' stroke='%23A2B6CF' stroke-opacity='.2' stroke-width='1.2'/%3E%3C/svg%3E\");--musterb:9mm}\n")
    s = kopf + s + CSS_HAUS
    with open(os.path.join(HIER, 'satz', 'satz.css'), 'w', encoding='utf-8') as f:
        f.write(s)


if __name__ == '__main__':
    Z = zeichen_svg()
    css()
    for kennung, datei in KARTEN.items():
        print(f'{kennung}: {setze(kennung, datei)} Seiten gesetzt')
