#!/usr/bin/env python3
"""Das Hausbuch (Le Livre) · Wirtschaft am Schlössli, Bottighofen: baut die Marke zum Arbeiten aus der Website des Hauses und dem bestätigten
Markenbuch (Station 05, Farbwelt A «Stuhl und See»). Nachbau von Le Livre des Grand Beau-Rivage, des Carlton-Europe, des Waldhotel Doldenhorn und
des Landgasthof Ruedihus (dort nur gelesen). Die Website wird nie angefasst: gelesen werden bilder.py, inhalt/bilder.json, assets/css/haus.css,
assets/svg/, assets/fonts/, farbwelt.py, die Seiten, _kette/05-markenbauer/marke.json und marke/, _quelle/**/herkunft.json. Geschrieben wird nur in
diesen Ordner.

   python3 _werkzeuge/livre/bau.py   → livre.json, dateien/, original/, _quellen.json (nur lokal), hero-*.webp, beispiel/, buch.html, index.html

Farben = die Werte der Website heute (haus.css). Seit 19.10.2026 «Ton in Ton» (Robert): die Blautöne der Farbwelt A sind um 21° auf das Blau des
Platztellers gedreht (website/farbwelt.py). Der Bau rechnet die Drehung aus marke.json selbst nach und bricht ab, wenn sie nicht zu haus.css passt.
Herkunft je Foto: haus (Website, Schweiz Tourismus, Instagram des Hauses), frei (Wikimedia Commons, Urheber und Lizenz aus herkunft.json),
ki (mit KI erzeugt), fremd (Rechte bei Dritten: Gästefotos, Partner, Heft der Gemeinde; auf der Website nur für die Demo)."""
import ast, colorsys, glob, hashlib, html, io, json, math, os, re, shutil, struct, subprocess, sys, time, zipfile
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFile, ImageChops

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))              # …/Wirtschaft am Schlössli Bottighofen (Werkzeuge liegen in _werkzeuge/, wie Die Stube)
ROOT = os.path.join(PROJEKT, 'website')                        # die Website, nur gelesen; ausgeliefert unter / (server.py)
PROJEKTE = os.path.dirname(PROJEKT)
QUELLE = os.path.join(PROJEKT, '_quelle')
MARKE = os.path.join(PROJEKT, '_kette', '05-markenbauer')
IMG = os.path.join(ROOT, 'assets', 'img')
CSS = os.path.join(ROOT, 'assets', 'css', 'haus.css')
FONTS = os.path.join(ROOT, 'assets', 'fonts')
SVG = os.path.join(ROOT, 'assets', 'svg')
DAT = os.path.join(HIER, 'dateien')
ORIG = os.path.join(HIER, 'original')
e = html.escape
HAUS = 'Wirtschaft am Schlössli'
STAND = time.strftime('%d.%m.%Y')
SCHLUESSEL = 'wirtschaft-am-schloessli'
MJ = json.load(open(os.path.join(MARKE, 'marke.json'), encoding='utf-8'))
def namen_aus_kleid():
    """Sichtbare Namen der Werkzeuge: eine Stelle für alle Werkzeuge, WO_HAUS.namen im gemeinsamen Kleid (_werkzeuge/oberflaeche/kleid/schloessli.js)."""
    t = open(os.path.join(PROJEKT, '_werkzeuge', 'oberflaeche', 'kleid', 'schloessli.js'), encoding='utf-8').read()
    m = re.search(r'namen:\s*\{([^}]*)\}', t)
    if not m:
        raise SystemExit('WO_HAUS.namen fehlt im Kleid: erst klären')
    return dict(re.findall(r"(\w+):\s*'([^']+)'", m.group(1)))


NAMEN = namen_aus_kleid()
NAME = NAMEN['marke']


def wert_aus(pfad, name):
    """Ein Wert aus einer Python-Datei, gelesen ohne sie auszuführen."""
    for n in ast.parse(open(pfad, encoding='utf-8').read()).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    return None


def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- Farben: Farbwelt A, gedreht «Ton in Ton», so wie haus.css sie trägt
FW = os.path.join(ROOT, 'farbwelt.py')
VON, BIS, DREH = next(ast.literal_eval(n.value) for n in ast.parse(open(FW, encoding='utf-8').read()).body
                     if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Tuple) and [t.id for t in n.targets[0].elts] == ['VON', 'BIS', 'DREH'])
FEST = wert_aus(FW, 'FEST')


def gedreht(hx):
    """Dieselbe Drehung wie website/farbwelt.py, hier unabhängig nachgerechnet (Regel 57: zweimal rechnen)."""
    t = hx.lstrip('#').lower()
    if t in FEST:
        return '#' + FEST[t]
    r, g, b = rgb(t)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if s < .06 or not (VON <= h * 360 <= BIS):
        return '#' + t
    r2, g2, b2 = colorsys.hls_to_rgb(((h * 360 + DREH) % 360) / 360, l, s)
    return '#%02x%02x%02x' % (round(r2 * 255), round(g2 * 255), round(b2 * 255))


FA = next(w for w in MJ['farbwelten'] if w['kennung'] == 'a')
# (Schlüssel in haus.css, Name, Wert in Farbwelt A oder None, Rolle, Gruppe)
FARBEN = [
    ('nacht', 'Nacht', FA['flaechen'][0], 'Grund der dunklen Flächen, immer mit der Punkt-Tapete', 'dunkel'),
    ('tief', 'Tief', FA['flaechen'][1], 'zweite dunkle Fläche, Platten auf Nacht', 'dunkel'),
    ('stuhl', 'Stuhlblau', FA['flaechen'][2], 'Knöpfe, Linien und Betonung auf Hell', 'dunkel'),
    ('kalk', 'Kalk', FA['flaechen'][3], 'Grund der hellen Flächen, mit der Punkt-Tapete', 'hell'),
    ('kalk2', 'Kalk tief', FA['flaechen'][4], 'zweite helle Fläche, Felder und Linien', 'hell'),
    ('papier', 'Papier', None, 'ruhige helle Abschnitte ohne Tapete', 'hell'),
    ('himmel', 'Seehimmel', FA['akzent'], 'Linie und Zeichen auf Dunkel, Horizont', 'himmel'),
    ('himmel-h', 'Seehimmel hell', FA['akzent_hell'], 'Betonung in Titeln auf Dunkel', 'himmel'),
    ('himmel-t', 'Seehimmel tief', FA['akzent_tief'], 'Betonung in Titeln auf Hell', 'himmel'),
    ('tinte', 'Tinte', FA['schrift'], 'Schrift auf hellen Flächen, nie reines Schwarz', 'schrift'),
    ('titel-h', 'Titelblau', None, 'Titel in Versalien auf Hell', 'schrift'),
    ('punkt', 'Schirmrot', FA['punkt'], 'nur als Punkt: Stempel, Markierung, nie als Fläche', 'punkt'),
]
GRUPPEN = [('dunkel', 'Nacht und Stuhlblau', 'Die dunklen Flächen. Aus dem Blau der Terrassenstühle, seit dem 19.10.2026 auf das Blau des Platztellers gedreht. Sie tragen immer die Punkt-Tapete.'),
           ('hell', 'Kalk und Papier', 'Die hellen Flächen, auf denen gelesen wird. Kalk mit der Punkt-Tapete, Papier ruhig.'),
           ('himmel', 'Seehimmel', 'Der Himmel über dem See, aufgehellt und vertieft: die Linie des Horizonts, das Zeichen auf Dunkel, die Betonung in Titeln. Zeichnet, schreibt nie den Lesetext.'),
           ('schrift', 'Schrift', 'Tinte für den Lesetext, Titelblau für Titel in Versalien. Nie reines Schwarz.'),
           ('punkt', 'Nur als Punkt', 'Das Rot der Sonnenschirme auf der Terrasse. Nie als Fläche.')]


def root_farben():
    s = open(CSS, encoding='utf-8').read()
    blk = re.search(r':root\s*\{(.*?)\}', s, re.S).group(1)
    return {m.group(1): m.group(2).lower() for m in re.finditer(r'--([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;', blk)}


def farben_liste():
    werte = root_farben(); aus = []
    for k, n, a, r, g in FARBEN:
        h = werte.get(k)
        if not h:
            raise SystemExit(f'Farbe {n}: --{k} fehlt in haus.css, erst klären')
        if a:
            if gedreht(a) != h:
                raise SystemExit(f'Farbe {n}: Farbwelt A {a} gedreht {gedreht(a)}, haus.css {h}, erst klären')
            woher = (f'Farbwelt A {a.upper()}, um {DREH}° auf das Blau des Platztellers gedreht (Ton in Ton, 19.10.2026)' if gedreht(a) != '#' + a.lstrip('#').lower()
                     else f'Farbwelt A {a.upper()}, unverändert')
        else:
            woher = 'Wert der Website (haus.css), nicht aus dem Markenbuch'
        aus.append((k, n, h, r, g, woher))
    return aus


def lab(c):
    def f(x):
        x /= 255; return ((x + .055) / 1.055) ** 2.4 if x > .04045 else x / 12.92
    r, g, b = (f(x) for x in c)
    X = (.4124 * r + .3576 * g + .1805 * b) / .95047
    Y = .2126 * r + .7152 * g + .0722 * b
    Z = (.0193 * r + .1192 * g + .9505 * b) / 1.08883
    t = lambda v: v ** (1 / 3) if v > .008856 else 7.787 * v + 16 / 116
    return 116 * t(Y) - 16, 500 * (t(X) - t(Y)), 200 * (t(Y) - t(Z))


def de2000(a, b):
    L1, a1, b1 = a; L2, a2, b2 = b
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2); Cm = (C1 + C2) / 2
    G = .5 * (1 - math.sqrt(Cm ** 7 / (Cm ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360; h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dL, dC = L2 - L1, C2p - C1p
    dh = 0 if C1p * C2p == 0 else (h2p - h1p if abs(h2p - h1p) <= 180 else h2p - h1p - 360 if h2p > h1p else h2p - h1p + 360)
    dH = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh / 2))
    Lm, Cmp = (L1 + L2) / 2, (C1p + C2p) / 2
    hm = h1p + h2p if C1p * C2p == 0 else ((h1p + h2p) / 2 if abs(h1p - h2p) <= 180 else (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2)
    T = 1 - .17 * math.cos(math.radians(hm - 30)) + .24 * math.cos(math.radians(2 * hm)) + .32 * math.cos(math.radians(3 * hm + 6)) - .2 * math.cos(math.radians(4 * hm - 63))
    SL = 1 + .015 * (Lm - 50) ** 2 / math.sqrt(20 + (Lm - 50) ** 2); SC = 1 + .045 * Cmp; SH = 1 + .015 * Cmp * T
    RT = -2 * math.sqrt(Cmp ** 7 / (Cmp ** 7 + 25 ** 7)) * math.sin(math.radians(60 * math.exp(-((hm - 275) / 25) ** 2)))
    return math.sqrt((dL / SL) ** 2 + (dC / SC) ** 2 + (dH / SH) ** 2 + RT * (dC / SC) * (dH / SH))


def messe(pfad, hexwert, n=160, fenster=3, rand=.04):
    """Wo im Foto liegt der Ton? Mittel über fenster × fenster Bildpunkte, die Stelle mit dem kleinsten ΔE 2000. (gemessen, ΔE, x %, y %)"""
    im = Image.open(pfad).convert('RGB'); im.thumbnail((n, n), Image.LANCZOS)
    a = np.asarray(im, np.float32); h, w = a.shape[:2]; ziel = lab(rgb(hexwert)); best = None
    for y in range(round(h * rand), round(h * (1 - rand)) - fenster + 1):
        for x in range(round(w * rand), round(w * (1 - rand)) - fenster + 1):
            m = a[y:y + fenster, x:x + fenster].reshape(-1, 3).mean(0)
            d = de2000(lab(m), ziel)
            if best is None or d < best[0]:
                best = (d, m, x, y)
    d, m, x, y = best
    return '#%02x%02x%02x' % tuple(int(round(v)) for v in m), round(d, 1), round((x + 1.5) / w * 100, 1), round((y + 1.5) / h * 100, 1)


# Wo die Farben im Haus vorkommen (Markenbuch Station 05, fundstelle in marke.json): Foto der Website, Töne aus marke.json, gemessen beim Bau
HERKUNFT_FOTOS = [('start', 'Der Hafen am Tag', 'Blaue Stühle auf der Terrasse am Mittag, dahinter der See und die Alpen. Daraus kommen Stuhlblau, Seespiegel, Seehimmel und Ufersand.',
                   ['Stuhlblau', 'Seespiegel', 'Seehimmel', 'Ufersand']),
                  ('platanen', 'Unter den Platanen', 'Gedeckte Tische auf Kies, Sonnenschirme. Daraus kommen Kies, Platanenlaub und Schirmrot.', ['Kies', 'Platanenlaub', 'Schirmrot']),
                  ('anguria', 'Der Platzteller', 'Ein Teller von oben auf dem blauen Platzteller. Auf sein Blau sind die Blautöne seit dem 19.10.2026 gedreht.', ['Tellerblau']),
                  ('abend', 'Der Abend am Wasser', 'Unter der Platane mit Lichterkette. Daraus kommen Abendrot, Blaue Stunde und Lichterkette.', ['Abendrot', 'Blaue Stunde', 'Lichterkette']),
                  ('fliesen', 'Die Fliesen der Bar', 'Die Zementfliesen unter der Theke. Daraus kommen die vier Töne der Fliesen.', ['Fliese Anthrazit', 'Fliese Kalk', 'Fliese Terrakotta', 'Fliese Graublau'])]


def herkunft_buch():
    MF = {f['name']: f for f in MJ['farben']}
    return [(k, t, s, [(n, MF[n]['hex']) for n in ns]) for k, t, s, ns in HERKUNFT_FOTOS]


# ---------------------------------------------------------------- Bildarchiv
def bilder_liste():
    """BILDER aus website/bilder.py, ohne die Datei auszuführen: nur die einfachen Textwerte davor (W, C2) werden eingesetzt."""
    baum = ast.parse(open(os.path.join(ROOT, 'bilder.py'), encoding='utf-8').read())
    werte = {}
    for n in baum.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            if isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
                werte[n.targets[0].id] = n.value.value
            elif n.targets[0].id == 'BILDER':
                class Ein(ast.NodeTransformer):
                    def visit_Name(self, x):
                        return ast.copy_location(ast.Constant(werte[x.id]), x)
                v = Ein().visit(n.value)
                ast.fix_missing_locations(v)
                v = ast.literal_eval(ast.unparse(v).replace("' + '", ''))
                return v
    raise SystemExit('BILDER fehlt in bilder.py')


BILDER = bilder_liste()
BJ = json.load(open(os.path.join(ROOT, 'inhalt', 'bilder.json'), encoding='utf-8'))
BEREICH = {
    'terrasse': ['start', 'platanen', 'lounge', 'baum', 'apero', 'abend', 'glas', 'ig-terrasse', 'ig-luft', 'tb-glas'],
    'bar': ['gaststube', 'bar', 'regal', 'schild', 'fliesen', 'wein'],
    'essen': ['mi-teller', 'thon', 'pasta', 'iberia', 'tortelloni', 'sauce', 'anguria', 'teller', 'dessert', 'suppe', 'fisch', 'salat', 'fleisch', 'torte',
              'ig-herd', 'ig-teller', 'ig-pasta', 'ig-dessert', 'tb-fisch', 'tb-teller'],
    'team': ['moni', 'team', 'jonas', 'lukas'],
    'hafen': ['haus', 'bootshafen', 'schifflaende', 'ig-hafen'],
    'see': ['morgen', 'saentis', 'abendschiff', 'abend-hafen', 'jz-fruehling', 'jz-sommer', 'jz-herbst', 'tb-dunkel', 'ig-abend'],
    'geschichte': ['luft1954', 'ch-postkarte', 'ch-anzeige', 'ch-strandhotel', 'ch-zeichnung', 'ch-mann', 'ch-luftkarte', 'ch-portal', 'ch-ufer'],
    'anlaesse': ['stier', 'kf-teller', 'kf-deck-abend', 'kp-party', 'pa-teller', 'kf-anrichten', 'feuerwerk', 'feuerwerk-ki'],
    'familie': ['schaefli'],
}
BEREICHE = ['terrasse', 'essen', 'bar', 'team', 'hafen', 'see', 'geschichte', 'anlaesse', 'familie']
B_VON = {k: b for b, ks in BEREICH.items() for k in ks}
SOMMER = {'start', 'platanen', 'lounge', 'baum', 'apero', 'abend', 'glas', 'ig-terrasse', 'ig-luft', 'tb-glas', 'jz-sommer', 'kf-deck-abend', 'kp-party', 'feuerwerk', 'feuerwerk-ki'}
# Nur Ausschnitte eines anderen Fotos im Archiv: das Foto selbst steht dort unter eigenem Namen
NICHT = {'start-hoch'}
# Doppelte Fotos (Robert 20.10.2026: «… ein Eintrag stand doppelt drin»; Bildvergleich beim Bau, Abstand der Signaturen unter 0,4): ein Eintrag, der andere
# Fundort steht in der Quelle. Schlüssel = weggelassener Eintrag, Wert = (bleibt, Satz für die Quelle)
ZUSAMMEN = {'teller': ('anguria', 'Auf der Startseite als quadratischer Ausschnitt, Licht und Schärfe mit KI nachgeschärft'),
            'kf-teller': ('fisch', 'Dasselbe Foto zeigt Excellence / Twerenbold auf excellence.ch (Gourmetfestival mit Monika Huber)'),
            'feuerwerk': ('feuerwerk-ki', 'Vorlage war das Foto der Website des Hauses, Bildrecht laut Dateiname bei «Keller»; «Vorher» zeigt es')}
# Vorher bei nachgeschärften Bildern: das unveränderte Ausgangsbild in _quelle/
VORHER = {'feuerwerk-ki': BILDER['feuerwerk'][0]}
for _k, (_d, *_r) in BILDER.items():
    if _d.startswith('presse/heft-bilder/ki/'):
        _roh = re.sub(r'-ki(-bild)?\.png$', '-roh.png', _d)
        if os.path.exists(os.path.join(QUELLE, _roh)):
            VORHER[_k] = _roh
# Druck in voller Auflösung: das Original vor der Bearbeitung, wo die Website eine abgedunkelte Fassung zeigt
DRUCK_STATT = {'abend-hafen': 'extern/wikipedia-commons/abend/04-gottlieben.jpg'}
SAETZE_FREMD = {
    'tripadvisor': 'Foto von Gästen auf Tripadvisor, Rechte bei den Gästen. Auf der Website nur für die Demo; vor jeder Veröffentlichung durch ein Foto des Hauses ersetzen',
    'excellence': 'Excellence / Twerenbold Reisen, nur Designstudie',
    'papageno': 'Restaurant Papageno / Guide Michelin, nur Designstudie',
    'schaefli-kitchenparty': 'Taverne zum Schäfli (Schwesterhaus), nur Designstudie',
    'guide-michelin': 'Titelbild der Seite des Guide Michelin; ob das Haus es geliefert hat, ist nicht belegt',
    'heft': 'Heft 2 der Gemeinde Bottighofen (1994), mit KI nachgeschärft; nur zur Anschauung, vor Veröffentlichung Erlaubnis der Gemeinde holen',
    'feuerwerk': 'Website des Hauses; Bildrecht laut Dateiname bei «Keller», vor jeder Veröffentlichung klären',
}


def hk(rel):
    """Eintrag aus der herkunft.json im Ordner der Quelle (Schlüssel = Weg ab _quelle/ oder Dateiname, Listen mit «datei»)."""
    d = os.path.dirname(os.path.join(QUELLE, rel))
    while d.startswith(QUELLE):
        p = os.path.join(d, 'herkunft.json')
        if os.path.exists(p):
            try:
                j = json.load(open(p, encoding='utf-8'))
            except ValueError:
                return {}
            if isinstance(j, list):
                return next((x for x in j if x.get('datei') == os.path.basename(rel)), {})
            if rel in j:
                return j[rel]
            if os.path.basename(rel) in j:
                return j[os.path.basename(rel)]
            return j if 'quelle' in j else {}
        d = os.path.dirname(d)
    return {}


def herkunft(k, rel):
    """(art, Quelle als Satz, Adresse)"""
    nw = BJ.get(k, {}).get('nachweis') or {}
    h = hk(rel)
    if rel.startswith('website/bearbeitet/feuerwerk-ki'):
        return 'ki', 'Mit KI erzeugt (Higgsfield, Vorlage: Foto der Website des Hauses), nur Platzhalter bis zu einem echten Foto des Hauses', ''
    if k == 'feuerwerk':
        return 'fremd', SAETZE_FREMD['feuerwerk'], hk(rel).get('quelle', '')
    if '/wikipedia-commons/' in rel or k in DRUCK_STATT:
        q = f"{nw.get('urheber', '?')}, {nw.get('lizenz', '?')}, Wikimedia Commons, {nw.get('jahr', '')}".rstrip(', ')
        if k in DRUCK_STATT:
            q += '. Auf der Website zur Bildmitte abgedunkelt, «Druck» liefert das Original'
        return 'frei', q, nw.get('quelle') or h.get('seite') or h.get('quelle', '')
    if rel.startswith('website/bilder/'):
        return 'haus', 'Website des Hauses (schloessli-bottighofen.ch); Rechte laut Impressum beim Haus oder den genannten Rechtsinhabern', h.get('quelle', '')
    if rel.startswith('website/bearbeitet/teller'):
        return 'haus', 'Foto der Website des Hauses («Anguria»), Licht und Schärfe mit KI nachgeschärft', ''
    if '/myswitzerland/' in rel:
        return 'haus', 'Schweiz Tourismus (myswitzerland.com), Bild des Eintrags des Hauses', h.get('seite', '')
    if '/ig/' in rel:
        return 'haus', 'Instagram des Hauses (@schloessli_bottighofen), Standbild aus einem Beitrag, klein', h.get('quelle', '')
    if rel.startswith('presse/heft-bilder/'):
        return 'fremd', SAETZE_FREMD['heft'], (nw or {}).get('quelle', '')
    for s, satz in SAETZE_FREMD.items():
        if f'/{s}/' in rel:
            return 'fremd', satz, h.get('seite') or h.get('quelle', '')
    return 'fremd', 'offen: Herkunft nicht in den Unterlagen', ''


def datei(k):
    """(gross, klein) in assets/img, als Weg von der Seite des Werkzeugs aus: die grösste Breite, klein höchstens 480."""
    br = BJ[k]['breiten']
    gr = max(br); kl = max([b for b in br if b <= 480] or [min(br)])        # Kachel im Raster höchstens 480 breit (am Handy leichter zu entpacken)
    g, s = f'{k}-{gr}.webp', f'{k}-{kl}.webp'
    if not os.path.exists(os.path.join(IMG, g)):
        return None, None
    return '../../assets/img/' + g, '../../assets/img/' + s


def katalog():
    aus, quellen = [], {}
    for k, (rel, hz, alt, aus_) in BILDER.items():
        if k in NICHT or k in ZUSAMMEN or k not in BJ:
            continue
        fl, fs = datei(k)
        p = os.path.join(QUELLE, rel)
        if not fl or not os.path.exists(p):
            print('nicht im Archiv:', k); continue
        art, q, u = herkunft(k, rel)
        for weg, (bleibt, satz) in ZUSAMMEN.items():
            if bleibt == k:
                q += '. ' + satz
        druck = os.path.join(QUELLE, DRUCK_STATT[k]) if k in DRUCK_STATT else p
        with Image.open(druck) as im0:
            w, h = ImageOps.exif_transpose(im0).size
        if aus_:                                                 # die Website zeigt einen Ausschnitt: Druck liefert denselben Ausschnitt in voller Grösse
            w, h = round(w * (aus_[2] - aus_[0])), round(h * (aus_[3] - aus_[1]))
        f = 'hoch' if h > w * 1.04 else 'quer' if w > h * 1.04 else 'quadrat'
        vor = VORHER.get(k)
        mb = [x for x in BJ[k]['breiten'] if x <= 1200]                     # Bühne der Ansichten: 1200 breit, lädt sofort
        fm = f'../../assets/img/{k}-{max(mb)}.webp' if mb else fl
        aus.append(dict(k=k, t={'de': alt}, b=B_VON.get(k, 'hafen'), s='sommer' if k in SOMMER else 'jahr', f=f, w=w, h=h, art=art, q=q, u=u,
                        ue=bool(vor), alt=False, vn=False, fl=fl, fm=fm, fs=fs))
        quellen[k] = dict(druck=druck, ausschnitt=aus_, original=os.path.join(QUELLE, vor) if vor else None)
        if B_VON.get(k) is None:
            print('ohne Bereich:', k)
    return aus, quellen


def originale(aus, quellen):
    """Das unveränderte Ausgangsbild der nachgeschärften Bilder, auf die Grösse der Website gerechnet (original/<k>.webp), gleicher Ausschnitt."""
    if os.path.isdir(ORIG):
        shutil.rmtree(ORIG)
    os.makedirs(ORIG)
    n = 0
    for d in aus:
        o = quellen[d['k']]['original']
        if not (d['ue'] and o and os.path.exists(o)):
            continue
        with Image.open(os.path.join(ROOT, d['fl'][6:])) as nach:          # fl = ../../assets/… vom Werkzeug aus, ausgeliefert aus website/
            groesse = nach.size
        im = ImageOps.exif_transpose(Image.open(o)).convert('RGB')
        w, h = im.size; z = groesse[0] / groesse[1]
        if abs(w / h - z) > .005:
            if w / h > z:
                nw = round(h * z); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
            else:
                nh = round(w / z); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im.resize(groesse, Image.LANCZOS).save(os.path.join(ORIG, d['k'] + '.webp'), 'WEBP', quality=80, method=5)
        d['vn'] = True
        n += 1
    return n


# ---------------------------------------------------------------- Köpfe der Ansichten (Vorladen im Auftakt, livre.js)
HEROS = {'start': ('start', .45), 'bilder': ('platanen', .45), 'dateien': ('fliesen', .5), 'pruefung': ('apero', .55)}


def heros(F):
    for ansicht, (key, y) in HEROS.items():
        im = Image.open(os.path.join(IMG, f'{key}-{max(BJ[key]["breiten"])}.webp')).convert('RGB')
        W_, H_ = 1800, 560
        sk = max(W_ / im.width, H_ / im.height)
        im = im.resize((round(im.width * sk), round(im.height * sk)), Image.LANCZOS)
        y0 = int(max(0, min(im.height - H_, im.height * y - H_ / 2))); x0 = (im.width - W_) // 2
        a = np.asarray(im.crop((x0, y0, x0 + W_, y0 + H_)), dtype=np.float32)
        xs = np.linspace(0, 1, W_)[None, :, None]; ys = np.linspace(0, 1, H_)[:, None, None]
        dunkel = np.clip(np.clip(1 - xs / .7, 0, 1) ** 1.5 * .94 + np.clip((ys - .7) / .3, 0, 1) * .32, 0, .96)
        a = a * (1 - dunkel) + np.array(rgb(F['nacht']), np.float32) * dunkel
        Image.fromarray(a.astype('uint8')).save(os.path.join(HIER, f'hero-{ansicht}.webp'), 'WEBP', quality=82, method=5)


# ---------------------------------------------------------------- Zeichen (potrace) als Polygone, Schrift als Pfad
def svg_pfad_ganz(svg):
    s = open(svg, encoding='utf-8').read()
    vb = tuple(float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split())
    tr = re.search(r'transform="translate\(([-\d.]+),([-\d.]+)\)\s*scale\(([-\d.]+),([-\d.]+)\)"', s)
    t = tuple(float(x) for x in tr.groups()) if tr else (0, 0, 1, 1)
    return vb, re.findall(r'\sd="([^"]+)"', s), t


def flach(d, schritte=8):
    tok = re.findall(r'[MmLlHhVvCcZz]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?', d)
    polys, cur, i, cmd, x, y, sx, sy = [], [], 0, None, 0.0, 0.0, 0.0, 0.0
    while i < len(tok):
        if re.match(r'[A-Za-z]', tok[i]):
            cmd = tok[i]; i += 1
            if cmd in 'Zz':
                if cur: polys.append(cur)
                cur = []; x, y = sx, sy
                continue
        if cmd in 'Mm':
            nx, ny = float(tok[i]), float(tok[i + 1]); i += 2
            if cmd == 'm' and (cur or polys or x or y): nx += x; ny += y
            if cur: polys.append(cur)
            x, y = nx, ny; sx, sy = x, y; cur = [(x, y)]
            cmd = 'l' if cmd == 'm' else 'L'
        elif cmd in 'Ll':
            nx, ny = float(tok[i]), float(tok[i + 1]); i += 2
            if cmd == 'l': nx += x; ny += y
            x, y = nx, ny; cur.append((x, y))
        elif cmd in 'Hh':
            nx = float(tok[i]); i += 1; x = nx + (x if cmd == 'h' else 0); cur.append((x, y))
        elif cmd in 'Vv':
            ny = float(tok[i]); i += 1; y = ny + (y if cmd == 'v' else 0); cur.append((x, y))
        elif cmd in 'Cc':
            v = [float(t) for t in tok[i:i + 6]]; i += 6
            if cmd == 'c': v = [v[0] + x, v[1] + y, v[2] + x, v[3] + y, v[4] + x, v[5] + y]
            x0, y0 = x, y
            for k in range(1, schritte + 1):
                t = k / schritte; u = 1 - t
                cur.append((u ** 3 * x0 + 3 * u * u * t * v[0] + 3 * u * t * t * v[2] + t ** 3 * v[4], u ** 3 * y0 + 3 * u * u * t * v[1] + 3 * u * t * t * v[3] + t ** 3 * v[5]))
            x, y = v[4], v[5]
        else:
            i += 1
    if cur: polys.append(cur)
    return polys


def zeichen_polys(name):
    vb, ds, (tx, ty, sx, sy) = svg_pfad_ganz(os.path.join(SVG, name))
    return vb, [[(tx + px * sx, ty + py * sy) for px, py in p] for d in ds for p in flach(d)]


def png_xor(polys, vb, farbe, breite, ziel):
    """Polygone als PNG, gerade/ungerade gefüllt (potrace: Löcher bleiben frei), auf durchsichtigem Grund."""
    vx, vy, vw, vh = vb
    sk = 4; W = breite; H = round(breite * vh / vw); f = W / vw
    acc = np.zeros((H * sk, W * sk), bool)
    for p in polys:
        if len(p) < 3:
            continue
        im = Image.new('1', (W * sk, H * sk), 0)
        ImageDraw.Draw(im).polygon([((x - vx) * f * sk, (y - vy) * f * sk) for x, y in p], fill=1)
        acc ^= np.asarray(im, bool)
    a = Image.fromarray((acc * 255).astype('uint8')).resize((W, H), Image.LANCZOS)
    rgba = Image.new('RGBA', a.size, rgb(farbe) + (0,)); rgba.putalpha(a); rgba.save(ziel, format='PNG', optimize=True)


def _ttf(datei):
    from fontTools.ttLib import TTFont
    f = TTFont(os.path.join(FONTS, datei)); f.flavor = None
    b = io.BytesIO(); f.save(b); b.seek(0); return b


def text_pfad(text, sperr, datei='OpenSans-var.woff2'):
    """Ein Wort als SVG-Pfad (Standardschnitt der Schrift, Open Sans 400). (d, Breite, Versalhöhe) in Einheiten der Schrift."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    f = TTFont(os.path.join(FONTS, datei))
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm; cap = f['OS/2'].sCapHeight
    pen = SVGPathPen(gs); x = 0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            raise SystemExit(f'Zeichen {ch!r} fehlt in {datei}')
        gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, cap)))
        x += gs[g].width + sperr * upm
    x -= sperr * upm
    asc = max(cap, round(upm * .94))              # Ö trägt Punkte über der Versalhöhe
    return pen.getCommands(), x, cap, asc - cap


def text_png(text, sperr, breite, farbe, ziel, datei='OpenSans-var.woff2'):
    """Dasselbe Wort mit der Schrift selbst gezeichnet (nie gerade/ungerade füllen), Breite in Bildpunkten."""
    from fontTools.ttLib import TTFont
    from PIL import ImageFont
    d, w, cap, ueber = text_pfad(text, sperr, datei)
    f = TTFont(os.path.join(FONTS, datei)); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    k = breite * 4 / w
    font = ImageFont.truetype(_ttf(datei), size=max(1, round(upm * k)))
    W, H = round(w * k) + 8, round((cap + ueber) * k) + 8
    im = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(im); x = 0
    for c in text:
        dr.text((x * k, (cap + ueber) * k), c, font=font, fill=255, anchor='ls')
        x += gs[cmap[ord(c)]].width + sperr * upm
    a = im.resize((max(1, round(W / 4)), max(1, round(H / 4))), Image.LANCZOS)
    rgba = Image.new('RGBA', a.size, rgb(farbe) + (0,)); rgba.putalpha(a); rgba.save(ziel, optimize=True)
    return a.size


def ase(farben):
    def block(name, r, g, b):
        n = (name + '\0').encode('utf-16-be')
        body = struct.pack('>H', len(name) + 1) + n + b'RGB ' + struct.pack('>fff', r / 255, g / 255, b / 255) + struct.pack('>H', 2)
        return struct.pack('>HI', 1, len(body)) + body
    bl = b''.join(block(n, *rgb(h)) for n, h in farben)
    return b'ASEF' + struct.pack('>HHI', 1, 0, len(farben)) + bl


def logo_farbig(farbe, ziel, breite=None):
    """Das Logo des Hauses (PNG 1563 px, durchsichtig, Station 05) in einer Farbe: nur die Deckung wird übernommen, die Form bleibt Pixel für Pixel."""
    src = Image.open(os.path.join(MARKE, 'marke', 'logo', 'logo-eng-zugeschnitten.png')).convert('RGBA')
    a = src.getchannel('A')
    if breite:
        a = a.resize((breite, round(a.height * breite / a.width)), Image.LANCZOS)
    rgba = Image.new('RGBA', a.size, rgb(farbe) + (0,)); rgba.putalpha(a); rgba.save(ziel, optimize=True)
    return list(a.size)


def tapete_png(svgs):
    """Die Tapeten der Website als PNG in doppelter Dichte, gerendert von Chromium (unsichtbar, ein Lauf, eigener Prozess)."""
    js = os.path.join(HIER, '_tapete_png.js')
    open(js, 'w').write('''const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2, viewport: { width: 168, height: 168 } });
  for (const [svg, png] of JSON.parse(process.argv[2])) { await p.goto('file://' + svg); await p.screenshot({ path: png, omitBackground: true, clip: { x: 0, y: 0, width: 168, height: 168 } }); }
  await b.close(); })();''')
    env = dict(os.environ, NODE_PATH=os.path.expanduser('~/Aussen-Pruefung/node_modules'))
    subprocess.run(['node', js, json.dumps(svgs)], check=True, env=env, timeout=120)
    os.remove(js)


SCHRIFTEN = [
    ('t', 'Open Sans', 'OpenSans-var.woff2', 'Titel und Name, die Schrift der Wortmarke', '400, Versalien, Titel 0,14 em gesperrt, Name 0,3 em', 'Direkt im Hafen von Bottighofen', 400),
    ('s', 'Instrument Sans', 'InstrumentSans-normal-400_600.woff2', 'Lesetext', '400 bis 600, 18 px, Zeilenabstand 1,64', 'Den ganzen Tag durchgängig bieten wir die Karte der Lästermeile an.', 400),
    ('m', 'DM Mono', 'DMMono-normal-400.woff2', 'Kleine Angaben und Knöpfe', '400, Versalien, 0,16 em gesperrt', 'Seestrasse 50 · 8598 Bottighofen', 400),
    ('h', 'Caveat', 'Caveat-500.woff', 'Handschrift, nur einzelne Wörter (Städte auf den Landkarten der Karte)', '500, nie für Sätze', 'Lästermeile', 500),
]
LIZENZ = {'OpenSans-var.woff2': 'OFL-OpenSans.txt', 'Caveat-500.woff': 'OFL-Caveat.txt'}


def dateien(fa):
    if os.path.isdir(DAT):
        shutil.rmtree(DAT)
    os.makedirs(DAT)
    F = {k: h for k, n, h, r, g, w in fa}
    liste = []
    # Zeichen: Kreis, zwei Zeiger, zwei Kugeln (assets/svg/zeichen.svg) und die Zeiger allein (zeiger.svg), aus dem Logo des Hauses nachgezeichnet
    for gruppe, svgname, breite in (('zeichen', 'zeichen.svg', 900), ('zeiger', 'zeiger.svg', 600)):
        src = open(os.path.join(SVG, svgname), encoding='utf-8').read()
        vb, polys = zeichen_polys(svgname)
        var = []
        for k, farbe, grund in (('nacht', F['nacht'], 'hell'), ('stuhl', F['stuhl'], 'hell'), ('himmel', F['himmel'], 'dunkel'), ('weiss', '#ffffff', 'dunkel')):
            s = f'{SCHLUESSEL}-{gruppe}-{k}.svg'; p = f'{SCHLUESSEL}-{gruppe}-{k}.png'
            inhalt = src.replace('fill="currentColor"', f'fill="{farbe}"', 1).replace('<g ', f'<title>{"Zeichen" if gruppe == "zeichen" else "Zeiger"} · {HAUS}</title><g ', 1)
            open(os.path.join(DAT, s), 'w', encoding='utf-8').write(inhalt)
            png_xor(polys, vb, farbe, breite, os.path.join(DAT, p))
            var.append(dict(k=k, grund=grund, dateien=[s, p], px=list(Image.open(os.path.join(DAT, p)).size)))
        liste.append(dict(k=gruppe, var=var))
    # Logo: das Original des Hauses (PNG, kein Vektor vorhanden), umgefärbt nur in den Farben der Marke
    var = []
    for k, farbe, grund in (('nacht', F['nacht'], 'hell'), ('schwarz', '#000000', 'hell'), ('weiss', '#ffffff', 'dunkel'), ('himmel', F['himmel'], 'dunkel')):
        p = f'{SCHLUESSEL}-logo-{k}.png'
        var.append(dict(k=k, grund=grund, dateien=[p], px=logo_farbig(farbe, os.path.join(DAT, p))))
    liste.append(dict(k='logo', var=var))
    # Name in Versalien, Open Sans 400, gesperrt 0,3 em (Markenbuch): lang und kurz
    var = []
    for kurz, wort in (('', 'WIRTSCHAFT AM SCHLÖSSLI'), ('kurz-', 'SCHLÖSSLI')):
        d, w, cap, ueber = text_pfad(wort, .3)
        for k, farbe, grund in (('nacht', F['nacht'], 'hell'), ('weiss', '#ffffff', 'dunkel'), ('himmel', F['himmel'], 'dunkel')):
            s = f'{SCHLUESSEL}-name-{kurz}{k}.svg'; p = f'{SCHLUESSEL}-name-{kurz}{k}.png'
            open(os.path.join(DAT, s), 'w', encoding='utf-8').write(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-ueber} {round(w)} {cap + ueber}"><title>{wort} in Open Sans</title><path fill="{farbe}" d="{d}"/></svg>\n')
            px = text_png(wort, .3, 1800 if not kurz else 1000, farbe, os.path.join(DAT, p))
            var.append(dict(k=kurz + k, grund=grund, dateien=[s, p], px=list(px)))
    liste.append(dict(k='name', var=var))
    # Logo der heutigen Website (Teilen-Bild auf Mint) und das Original in Schwarz, unverändert
    n1 = f'{SCHLUESSEL}-logo-original.png'; n2 = f'{SCHLUESSEL}-logo-website-heute.jpg'
    shutil.copyfile(os.path.join(MARKE, 'marke', 'logo', 'logo-transparent-1563.png'), os.path.join(DAT, n1))
    shutil.copyfile(os.path.join(MARKE, 'marke', 'logo', 'logo-auf-mint-teilen-bild.jpeg'), os.path.join(DAT, n2))
    liste.append(dict(k='website', var=[dict(k='original', grund='hell', dateien=[n1], px=list(Image.open(os.path.join(DAT, n1)).size)),
                                         dict(k='heute', grund='hell', dateien=[n2], px=list(Image.open(os.path.join(DAT, n2)).size))]))
    # Tapete: Punktraster mit den Zeigern als Medaillon, wie die Website (assets/svg/tapete-a-*.svg)
    var, paare = [], []
    for k, grund, quelle in (('dunkel', 'dunkel', 'tapete-a-dunkel.svg'), ('hell', 'hell', 'tapete-a-hell.svg')):
        s = f'{SCHLUESSEL}-tapete-{k}.svg'; p = f'{SCHLUESSEL}-tapete-{k}.png'; w = f'{SCHLUESSEL}-tapete-{k}.webp'
        shutil.copyfile(os.path.join(SVG, quelle), os.path.join(DAT, s))
        paare.append((os.path.join(DAT, s), os.path.join(DAT, p)))
        var.append(dict(k=k, grund=grund, dateien=[p, s, w], px=[168, 168], farbe=F['nacht'] if k == 'dunkel' else F['kalk']))
    tapete_png(paare)
    for v in var:
        Image.open(os.path.join(DAT, v['dateien'][0])).save(os.path.join(DAT, v['dateien'][2]), 'WEBP', lossless=True)
    liste.append(dict(k='tapete', var=var))
    # Farben als Datei: CSS, JSON und ASE
    css = ':root{\n' + ''.join(f'  --{k}:{h}; /* {n}: {r} */\n' for k, n, h, r, g, w in fa) + '}\n'
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.css'), 'w', encoding='utf-8').write(f'/* {HAUS} · Farben der Marke ({NAME}, {STAND}), Werte der Website (assets/css/haus.css) */\n' + css)
    json.dump([dict(name=n, hex=h, rgb=list(rgb(h)), rolle=r, gruppe=g, woher=w) for k, n, h, r, g, w in fa], open(os.path.join(DAT, f'{SCHLUESSEL}-farben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.ase'), 'wb').write(ase([(n, h) for k, n, h, r, g, w in fa]))
    liste.append(dict(k='farben', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-farben.css', f'{SCHLUESSEL}-farben.json', f'{SCHLUESSEL}-farben.ase'])]))
    # Schriften: die Dateien der Website, dazu als ZIP mit TTF und Lizenz
    from fontTools.ttLib import TTFont
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-schriften.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for d_ in sorted({s[2] for s in SCHRIFTEN}):
            z.write(os.path.join(FONTS, d_), 'web/' + d_)
            f = TTFont(os.path.join(FONTS, d_)); f.flavor = None
            b = io.BytesIO(); f.save(b); z.writestr('programme/' + re.sub(r'\.woff2?$', '.ttf', d_), b.getvalue())
        for l in sorted(set(LIZENZ.values())):
            z.write(os.path.join(FONTS, l), 'lizenz/' + l)
        z.writestr('LIESMICH.txt', f'''{HAUS} · Schriften der Marke ({NAME}, {STAND})

Open Sans 400: Titel und Name, in Versalien gesperrt. Die Schrift der Wortmarke (Messung im Markenbuch, nicht vom Haus bestätigt).
Instrument Sans (400 bis 600): Lesetext.
DM Mono 400: kleine Angaben in Versalien, Zeiten, Adressen, Knöpfe.
Caveat 500: Handschrift, nur einzelne Wörter.

Alle stehen unter der SIL Open Font License 1.1 (frei für Druck, Website und Programme, auch gewerblich; nicht als Schrift allein verkaufen).
web/        die Dateien der Website
programme/  dieselben Schriften als TTF zum Installieren
''')
    liste.append(dict(k='schriften', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-schriften.zip'])]))
    alle = sorted(os.listdir(DAT))
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-marke.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for n_ in alle:
            z.write(os.path.join(DAT, n_), n_)
    return liste


# ---------------------------------------------------------------- Beispiel für die Markenprüfung
def beispiel(F):
    """Ein eigens gezeichneter Entwurf, wie ihn eine Agentur heute schicken würde: ein guter Beitrag, gebaut noch nach der heutigen Website des Hauses
    (Gilda Display, Nachtblau #213C4F, Mint #D8FFFC, beide gemessen von Station 02), mit Foto und Logo des Hauses (Robert 15.10.2026 am Rivage:
    «irgendein schönes Beispiel … Kein doofes … Kein zu krass erfundenes»). Geprüft mit der Prüfung selbst ohne Claude (LIVRE_KI=0); die Farben bleiben
    gemessen, Schrift, Zeichen, Bild und Ton bekommen Beispiel-Urteile zu genau diesem Entwurf (Robert 18.10.2026 18:52), beschriftet als Beispiel."""
    os.environ['LIVRE_KI'] = '0'
    sys.path.insert(0, HIER)
    import livre as LV
    LV._livre.cache_clear()
    from PIL import ImageFont
    from fontTools.ttLib import TTFont
    zb = os.path.join(HIER, 'beispiel'); os.makedirs(zb, exist_ok=True)
    W, H = 1080, 1350
    NB, MINT = (0x21, 0x3C, 0x4F), (0xD8, 0xFF, 0xFC)                      # Nachtblau und Mint der heutigen Website (marke.json, Station 02)
    im = Image.new('RGB', (W, H), NB)
    foto = Image.open(os.path.join(IMG, f'apero-{max(BJ["apero"]["breiten"])}.webp')).convert('RGB')
    sk = max(W / foto.width, 900 / foto.height); foto = foto.resize((round(foto.width * sk), round(foto.height * sk)), Image.LANCZOS)
    y0 = round((foto.height - 900) * .55)
    im.paste(foto.crop(((foto.width - W) // 2, y0, (foto.width - W) // 2 + W, y0 + 900)), (0, 0))
    dr = ImageDraw.Draw(im)
    g = TTFont(os.path.join(MARKE, 'marke', 'schriften', 'GildaDisplay-latin.woff2')); g.flavor = None; gb = io.BytesIO(); g.save(gb); gb.seek(0)
    titel = ImageFont.truetype(gb, 84)
    try:
        lese = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 34); knopf = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 26)
    except OSError:
        lese = knopf = ImageFont.load_default()
    dr.text((72, 960), 'Abend am Hafen', font=titel, fill=(255, 255, 255))
    dr.text((72, 1080), 'Die Karte der Lästermeile gibt es den ganzen Tag.', font=lese, fill=(230, 238, 240))
    dr.text((72, 1126), 'Seestrasse 50 · 8598 Bottighofen', font=lese, fill=(230, 238, 240))
    dr.rounded_rectangle((72, 1206, 412, 1278), 36, fill=MINT)
    dr.text((112, 1228), 'RESERVATION', font=knopf, fill=NB)
    logo = Image.open(os.path.join(DAT, f'{SCHLUESSEL}-logo-weiss.png')).convert('RGBA'); logo.thumbnail((190, 190), Image.LANCZOS)
    dunkel = Image.new('RGBA', (W, 260), (0, 0, 0, 0)); dd = ImageDraw.Draw(dunkel)
    for i in range(260):
        dd.line((0, i, W, i), fill=(0, 0, 0, int(110 * (1 - i / 260))))
    im.paste(dunkel, (0, 0), dunkel); im.paste(logo, (W - 60 - logo.width, 50), logo)
    im.save(os.path.join(zb, 'entwurf.png'), optimize=True)
    import base64
    b = io.BytesIO(); im.save(b, 'PNG')
    j = LV.pruefen(dict(name='Beispiel-Entwurf «Abend am Hafen», Instagram-Beitrag', typ='image/png', daten='data:image/png;base64,' + base64.b64encode(b.getvalue()).decode(), sprache='de'))
    j['beispiel'] = True
    k = j.setdefault('ki', {})
    farb = [x for x in k.get('punkte', []) if x.get('bereich') == 'farben']
    for x in farb:
        x['text'] = x['text'].replace('Gemessen ohne KI: ', 'Gemessen: ')
    k['punkte'] = farb + [
        dict(bereich='farben', urteil='achten', titel='Farben der heutigen Website', text='Das Nachtblau #213C4F der Fläche und das Mint #D8FFFC des Knopfs kommen von der heutigen Website. In der neuen Marke trägt Nacht #0B1D3D die Fläche, Knöpfe sind Kalk mit Knauf in Nacht.'),
        dict(bereich='schrift', urteil='achten', titel='Titel in Gilda Display', text='Der Titel steht in einer zarten Antiqua wie Gilda Display, der Schrift der heutigen Website. Das Schlössli setzt Titel jetzt in Open Sans in gesperrten Versalien, den Text in Instrument Sans.'),
        dict(bereich='zeichen', urteil='passt', titel='Das Logo steht richtig', text='Das Logo steht ungedreht in Weiss auf dunklem Grund, mit Luft rundherum und gut lesbar.'),
        dict(bereich='bild', urteil='passt', titel='Das Foto zeigt das Haus', text='Spritz und Bier auf dem blauen Tisch in der blauen Stunde: ein Foto des Hauses aus dem Bildarchiv, wie Gäste den Abend vorfinden.'),
        dict(bereich='ton', urteil='passt', titel='Kurz und mit echter Angabe', text='Eine Einladung ohne Ausrufezeichen, dazu die Adresse. So schreibt das Haus.'),
    ]
    k['gesamt'] = ('Ein guter Entwurf: Foto, Logo und Ton passen. Schrift und Farben stammen noch von der heutigen Website; '
                   'mit Open Sans in Versalien und Nacht statt Nachtblau wird daraus ein Beitrag der neuen Marke.')
    k['ton'] = []
    j['probe'] = False
    json.dump(j, open(os.path.join(zb, 'pruefung.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    return j


# Bilder zu jedem Eintrag der Listen «Farben» und «Schriften» (Robert 20.10.2026: «in allen Tools Bilder dazu»): das Foto, aus dem der Ton kommt
# (Ausschnitte des Markenbuchs, Station 05), sonst ein Ausschnitt der Website, wie er dort steht (listen_bilder.js)
FARB_BILD = {'dunkel': ('buch/bilder/k-stuhl.webp', 'Das Geflecht der Terrassenstühle, daraus Stuhlblau'),
             'hell': ('buch/bilder/k-himmel.webp', 'Der Himmel über dem See, aufgehellt'),
             'himmel': ('buch/bilder/k-himmel.webp', 'Der Himmel über dem See'),
             'punkt': ('buch/bilder/k-schirm.webp', 'Die Sonnenschirme der Terrasse')}
GRUPPE_BILD = {'dunkel': ('buch/bilder/k-stuhl.webp', 'Das Geflecht der Terrassenstühle. Daraus kommt Stuhlblau, seit dem 19.10.2026 auf das Blau des Platztellers gedreht.'),
               'hell': ('../../assets/img/start-800.webp', 'Der Hafen am Mittag, das Startbild der Website. Der helle Himmel über dem See, aufgehellt, gibt Kalk und Papier.'),
               'himmel': ('buch/bilder/k-himmel.webp', 'Der Himmel über dem See. Daraus kommt Seehimmel, hell und tief.'),
               'schrift': ('listen/schrift-t.webp', 'So stehen Tinte und Titelblau auf der Website.'),
               'punkt': ('buch/bilder/k-schirm.webp', 'Die Sonnenschirme der Terrasse. Daraus kommt Schirmrot.')}
FARB_BILD_K = {'papier': ('listen/farbe-papier.webp', 'So steht Papier auf der Website'), 'tinte': ('listen/farbe-tinte.webp', 'So steht Tinte auf der Website'),
               'titel-h': ('listen/schrift-t.webp', 'So steht Titelblau auf der Website')}


def listen_bilder():
    z = os.path.join(HIER, 'listen')
    if os.path.isdir(z):
        shutil.rmtree(z)
    os.makedirs(z)
    seiten = [os.path.join(ROOT, n) for n in ('index.html', 'karte.html', 'kontakt.html', 'team.html', 'anlaesse.html') if os.path.exists(os.path.join(ROOT, n))]
    env = dict(os.environ, NODE_PATH=os.path.expanduser('~/Aussen-Pruefung/node_modules'))
    subprocess.run(['node', os.path.join(HIER, 'listen_bilder.js'), z] + seiten, check=True, env=env, timeout=240, capture_output=True)
    for n in os.listdir(z):
        im = Image.open(os.path.join(z, n)).convert('RGB'); im.thumbnail((1200, 800), Image.LANCZOS)
        im.save(os.path.join(z, n[:-4] + '.webp'), 'WEBP', quality=84, method=5); os.remove(os.path.join(z, n))


def main():
    t0 = time.time()
    fa = farben_liste()
    F = {k: h for k, n, h, r, g, w in fa}
    aus, quellen = katalog()
    n_orig = originale(aus, quellen)
    heros(F)
    liste = dateien(fa)
    groessen = {f: os.path.getsize(os.path.join(DAT, f)) for f in sorted(os.listdir(DAT))}
    daten = dict(haus=HAUS, ort='Bottighofen', fotos=aus, dateien=liste,
                 farben=[dict(k=k, n=n, h=h.upper(), rgb=list(rgb(h)), r=r, g=g, woher=w) for k, n, h, r, g, w in fa],
                 gruppen=[dict(k=k, n=n, s=s) for k, n, s in GRUPPEN], glanz=[], groessen=groessen,
                 bereiche=[b for b in BEREICHE if any(f['b'] == b for f in aus)],
                 schriften=[dict(k=k, n=fam, d=d, r=r, e=ein, p=p, w=w) for k, fam, d, r, ein, p, w in SCHRIFTEN],
                 namen=NAMEN,
                 ton=dict(eigene_worte=MJ['ton']['eigene_worte'], nicht=MJ['ton']['nicht']),
                 stand=dict(fotos=len(aus), haus=sum(1 for x in aus if x['art'] == 'haus'), frei=sum(1 for x in aus if x['art'] == 'frei'),
                            ki=sum(1 for x in aus if x['art'] == 'ki'), fremd=sum(1 for x in aus if x['art'] == 'fremd'), partner=0,
                            ue=sum(1 for x in aus if x['ue']), vn=n_orig, original=sum(1 for v in quellen.values() if v['druck'] and os.path.exists(v['druck'])),
                            dateien=len(groessen), datum=STAND))
    json.dump(daten, open(os.path.join(HIER, 'livre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({k: dict(druck=v['druck'] and os.path.relpath(v['druck'], PROJEKTE), ausschnitt=v['ausschnitt'],
                       original=v['original'] and os.path.relpath(v['original'], PROJEKTE)) for k, v in quellen.items()},
              open(os.path.join(HIER, '_quellen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    beispiel(F)
    import buch
    buch.aus_station5(os.path.join(MARKE, 'marke'), ROOT, gedreht, daten)
    listen_bilder()
    # Robert 20.10.2026 (Bild: dreimal dasselbe Stuhlfoto über dünnen Farbstreifen): «Nee, das finde ich dumm.» Darum ein Foto je Gruppe, nicht je Farbe
    for g in daten['gruppen']:
        g['bild'], g['bild_t'] = GRUPPE_BILD[g['k']]
    for s_ in daten['schriften']:
        s_['bild'] = f'listen/schrift-{s_["k"]}.webp'
    for f_ in [*GRUPPE_BILD.values()] + [(x['bild'], '') for x in daten['schriften']]:
        if not os.path.exists(os.path.join(ROOT, f_[0][6:]) if f_[0].startswith('../../') else os.path.join(HIER, f_[0])):
            raise SystemExit('Bild fehlt: ' + f_[0])
    json.dump(daten, open(os.path.join(HIER, 'livre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)     # Markenbuch des Hauses (Station 05, Ton in Ton); buch.baue() bleibt als frühere Fassung
    seite(F)
    st = daten['stand']
    print(f'livre.json: {len(aus)} Fotos ({st["haus"]} Haus, {st["frei"]} frei, {st["ki"]} KI, {st["fremd"]} fremde Rechte, {st["ue"]} nachgeschärft, '
          f'{n_orig} mit Vorher, {st["original"]} mit Original) · {len(groessen)} Dateien · {time.time() - t0:.0f} s')


def v_von(*namen):
    h = hashlib.sha1()
    for n in namen:
        h.update(open(os.path.join(HIER, n), 'rb').read())
    return h.hexdigest()[:10]


def seite(F):
    v = v_von('livre.json'); vc = v_von('livre.css'); vj = v_von('livre.js')
    open(os.path.join(HIER, 'index.html'), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{NAME} · Wirtschaft am Schlössli</title>
<meta name="description" content="{NAME}, die Marke der Wirtschaft am Schlössli in Bottighofen zum Arbeiten: Bildarchiv mit fertigen Grössen, Zeichen, Logo, Name, Tapete und Farben als Dateien, Markenprüfung für Entwürfe, Markenbuch.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['nacht']}">
<link rel="icon" href="dateien/{SCHLUESSEL}-zeiger-nacht.svg" type="image/svg+xml">
<script src="/assets/oberflaeche/kleid/schloessli.js?v={v_von('../oberflaeche/kleid/schloessli.js')}"></script>
<link rel="preload" href="../../assets/fonts/OpenSans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/fonts/DMMono-normal-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="livre.json?v={v}" as="fetch" crossorigin>
<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v={v_von('../oberflaeche/grund.css')}">
<link rel="stylesheet" href="/assets/oberflaeche/rahmen-buehne.css?v={v_von('../oberflaeche/rahmen-buehne.css')}">
<link rel="stylesheet" href="/assets/oberflaeche/kleid/schloessli.css?v={v_von('../oberflaeche/kleid/schloessli.css')}">
<link rel="stylesheet" href="livre.css?v={vc}">
</head>
<body class="li wo-app">
<header class="wo-kopf" id="kopf"></header>
<aside class="wo-rand" id="rand" aria-label="{NAME}"></aside>
<main class="wo-raum" id="haupt"><div id="ansicht"></div></main>
<footer class="wo-leiste" id="leiste" aria-live="polite"></footer>
<div class="fenster" id="fenster" hidden></div>
<div class="meldung" id="meldung" aria-live="polite"></div>
<noscript><p class="li-noscript">{NAME} braucht JavaScript.</p></noscript>
<script src="start.js?v={v_von('start.js')}" data-v="{vj}"></script>
<script src="/assets/oberflaeche/oberflaeche.js?v={v_von('../oberflaeche/oberflaeche.js')}"></script>
<script src="livre.js?v={vj}"></script>
</body>
</html>
''')


if __name__ == '__main__':
    main()
