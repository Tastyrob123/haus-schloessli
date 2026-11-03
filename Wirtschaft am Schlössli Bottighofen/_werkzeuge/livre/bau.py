#!/usr/bin/env python3
"""Das Markenbuch · Wirtschaft am Schlössli, Bottighofen: baut die Marke zum Arbeiten aus der Website des Hauses und dem bestätigten Markenbuch
(Station 05, Farbwelt A «Stuhl und See»). Aufbau und Funktionen wie das Markenbuch des Culinarium (Übersicht, Fotos nach Gruppen, Logo & Dateien,
Farben, Schriften, Hausregeln, Markenprüfung), Inhalt vom Schlössli. Die Website wird nie angefasst: gelesen werden website/inhalt/bilder.json
(Bildregister mit Alt-Text, Stufen, Nachweis), website/assets/img/, website/assets/css/haus.css, website/assets/fonts/, website/farbwelt.py,
_kette/05-markenbauer/marke.json und marke/. Nichts aus _quelle/ (liegt nicht in GitHub Actions). Geschrieben wird nur in diesen Ordner.

   python3 _werkzeuge/livre/bau.py   → livre.json, dateien/ (Farben, Schriften, ZIP), buch.html, buch/, index.html

Fest im Revier (aus dem Stand vom 20.10.2026 übernommen, nicht neu gezeichnet): dateien/ mit Zeichen, Zeigern, Logo, Name, Tapeten (SVG/PNG),
listen/ (Schriftproben der Website), beispiel/ (Beispiel-Entwurf der Markenprüfung).
Farben = die Werte der Website heute (haus.css). Seit 19.10.2026 «Ton in Ton» (Robert): die Blautöne der Farbwelt A sind um 21° auf das Blau des
Platztellers gedreht (website/farbwelt.py). Der Bau rechnet die Drehung aus marke.json selbst nach und bricht ab, wenn sie nicht zu haus.css passt.
Fotos: nur Fotos des Hauses (Website des Hauses, Schweiz Tourismus, Instagram des Hauses) und frei lizenzierte (Wikimedia Commons, mit Namen und
Lizenz). Nicht im Markenbuch (UEBERGABE.md, Rechte): Gästefotos (tb-*, baum), Partner (kf-*, pa-teller, stier, kp-party, mi-teller), Feuerwerk,
Heft der Gemeinde (ch-*), das Schwesterhaus (schaefli)."""
import ast, colorsys, hashlib, io, json, os, re, struct, sys, time, zipfile
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))              # …/Wirtschaft am Schlössli Bottighofen
ROOT = os.path.join(PROJEKT, 'website')                        # die Website, nur gelesen; ausgeliefert unter / (server.py)
MARKE = os.path.join(PROJEKT, '_kette', '05-markenbauer')
IMG = os.path.join(ROOT, 'assets', 'img')
CSS = os.path.join(ROOT, 'assets', 'css', 'haus.css')
FONTS = os.path.join(ROOT, 'assets', 'fonts')
DAT = os.path.join(HIER, 'dateien')
HAUS = 'Wirtschaft am Schlössli'
ORT = 'Bottighofen'
STAND = time.strftime('%d.%m.%Y')
SCHLUESSEL = 'wirtschaft-am-schloessli'
MJ = json.load(open(os.path.join(MARKE, 'marke.json'), encoding='utf-8'))
BJ = json.load(open(os.path.join(ROOT, 'inhalt', 'bilder.json'), encoding='utf-8'))
KLEID = os.path.join(PROJEKT, '_werkzeuge', 'oberflaeche', 'kleid', 'schloessli.js')


def namen_aus_kleid():
    """Sichtbare Namen der Werkzeuge: eine Stelle für alle Werkzeuge, WO_HAUS.namen im gemeinsamen Kleid (_werkzeuge/oberflaeche/kleid/schloessli.js)."""
    m = re.search(r'namen:\s*\{([^}]*)\}', open(KLEID, encoding='utf-8').read())
    if not m:
        raise SystemExit('WO_HAUS.namen fehlt im Kleid: erst klären')
    return dict(re.findall(r"(\w+):\s*'([^']+)'", m.group(1)))


NAMEN = namen_aus_kleid()
NAME = NAMEN['marke']


def wert_aus(pfad, name):
    for n in ast.parse(open(pfad, encoding='utf-8').read()).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    return None


def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- Farben: Farbwelt A «Stuhl und See», gedreht «Ton in Ton», so wie haus.css sie trägt
FW = os.path.join(ROOT, 'farbwelt.py')
VON, BIS, DREH = next(ast.literal_eval(n.value) for n in ast.parse(open(FW, encoding='utf-8').read()).body
                     if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Tuple) and [t.id for t in n.targets[0].elts] == ['VON', 'BIS', 'DREH'])
FEST = wert_aus(FW, 'FEST')


def gedreht(hx):
    """Dieselbe Drehung wie website/farbwelt.py, hier unabhängig nachgerechnet."""
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
# (Schlüssel, Name, Variable in haus.css, Wert in Farbwelt A oder None, Rolle, Gruppe); Namen wie im Kleid der Werkzeuge
FARBEN = [
    ('nacht', 'Nacht', 'nacht', FA['flaechen'][0], 'Nacht über dem See: Grund der dunklen Flächen, immer mit der Punkt-Tapete', 'dunkel'),
    ('tief', 'Tief', 'tief', FA['flaechen'][1], 'zweite dunkle Fläche, Platten auf Nacht', 'dunkel'),
    ('stuhl', 'Stuhlblau', 'stuhl', FA['flaechen'][2], 'das Blau der Terrassenstühle: Knöpfe, Linien und Flächen', 'dunkel'),
    ('papier', 'Papier', 'kalk', FA['flaechen'][3], 'Grund der hellen Flächen, mit der Punkt-Tapete', 'hell'),
    ('seespiegel', 'Seespiegel', 'kalk2', FA['flaechen'][4], 'zweite helle Fläche, Felder und Linien', 'hell'),
    ('blatt', 'Blatt', 'papier', None, 'ruhige helle Abschnitte ohne Tapete', 'hell'),
    ('himmel', 'Seehimmel', 'himmel', FA['akzent'], 'Linie, Zeichen und Knauf auf Dunkel, der Horizont', 'himmel'),
    ('himmel-h', 'Seehimmel hell', 'himmel-h', FA['akzent_hell'], 'Betonung in Titeln auf Dunkel', 'himmel'),
    ('himmel-t', 'Seehimmel tief', 'himmel-t', FA['akzent_tief'], 'Betonung in Titeln auf Hell', 'himmel'),
    ('tinte', 'Tinte', 'tinte', FA['schrift'], 'Schrift auf hellen Flächen, nie reines Schwarz', 'schrift'),
    ('titel', 'Titelblau', 'titel-h', None, 'Titel in Versalien auf Hell', 'schrift'),
    ('punkt', 'Schirmrot', 'punkt', FA['punkt'], 'nur als Punkt: Stempel, Markierung, Nabe der Zeiger, nie als Fläche', 'punkt'),
]
GRUPPEN = [('dunkel', 'Nacht und Stuhlblau', 'Die dunklen Flächen, aus dem Blau der Terrassenstühle, Ton in Ton auf das Blau des Platztellers gestimmt. Sie tragen immer die Punkt-Tapete.'),
           ('hell', 'Papier und Seespiegel', 'Die hellen Flächen, auf denen gelesen wird: der helle Himmel über dem See. Papier mit der Punkt-Tapete, Blatt ruhig.'),
           ('himmel', 'Seehimmel', 'Der Himmel über dem See, aufgehellt und vertieft: die Linie des Horizonts, das Zeichen auf Dunkel, die Betonung in Titeln. Zeichnet, schreibt nie den Lesetext.'),
           ('schrift', 'Schrift', 'Tinte für den Lesetext, Titelblau für Titel in Versalien. Nie reines Schwarz.'),
           ('punkt', 'Nur als Punkt', 'Das Rot der Sonnenschirme auf der Terrasse. Nie als Fläche, nie als Schrift.')]
GRUPPE_BILD = {'dunkel': ('buch/bilder/k-stuhl.webp', 'Das Geflecht der Terrassenstühle. Daraus kommt Stuhlblau.'),
               'hell': ('../../assets/img/start-800.webp', 'Der Hafen am Mittag. Der helle Himmel über dem See gibt Papier und Seespiegel.'),
               'himmel': ('buch/bilder/k-himmel.webp', 'Der Himmel über dem See. Daraus kommt Seehimmel, hell und tief.'),
               'schrift': ('listen/schrift-t.webp', 'So stehen Tinte und Titelblau auf der Website.'),
               'punkt': ('buch/bilder/k-schirm.webp', 'Die Sonnenschirme der Terrasse. Daraus kommt Schirmrot.')}


def root_farben():
    s = open(CSS, encoding='utf-8').read()
    blk = re.search(r':root\s*\{(.*?)\}', s, re.S).group(1)
    return {m.group(1): m.group(2).lower() for m in re.finditer(r'--([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;', blk)}


def farben_liste():
    werte = root_farben(); aus = []
    for k, n, var, a, r, g in FARBEN:
        h = werte.get(var)
        if not h:
            raise SystemExit(f'Farbe {n}: --{var} fehlt in haus.css, erst klären')
        if a:
            if gedreht(a) != h:
                raise SystemExit(f'Farbe {n}: Farbwelt A {a} gedreht {gedreht(a)}, haus.css {h}, erst klären')
            woher = ('Farbwelt «Stuhl und See», Ton in Ton auf das Blau des Platztellers gestimmt' if gedreht(a) != '#' + a.lstrip('#').lower()
                     else 'Farbwelt «Stuhl und See», unverändert')
        else:
            woher = 'Wert der Website des Hauses'
        aus.append((k, n, h, r, g, woher))
    return aus


# ---------------------------------------------------------------- Fotos: Bildregister der Website, in sieben Gruppen
GRUPPE_FOTOS = {
    'hafen': ['start', 'platanen', 'abend', 'lounge', 'haus', 'bootshafen', 'schifflaende'],
    'kueche': ['tortelloni', 'thon', 'iberia', 'pasta', 'anguria', 'fisch', 'fleisch', 'salat', 'suppe', 'sauce', 'dessert', 'torte'],
    'bar': ['gaststube', 'bar', 'fliesen', 'schild', 'apero'],
    'wein': ['wein', 'glas', 'regal'],
    'team': ['team', 'moni', 'jonas', 'lukas'],
    'see': ['morgen', 'saentis', 'abendschiff', 'abend-hafen', 'jz-fruehling', 'jz-sommer', 'jz-herbst', 'luft1954'],
    'instagram': ['ig-terrasse', 'ig-luft', 'ig-hafen', 'ig-abend', 'ig-herd', 'ig-teller', 'ig-pasta', 'ig-dessert'],
}
BEREICHE = list(GRUPPE_FOTOS)
SOMMER = {'start', 'platanen', 'lounge', 'glas', 'apero', 'abend', 'ig-terrasse', 'ig-luft', 'jz-sommer'}
NICHT = re.compile(r'^(tb-|kf-|ch-|feuerwerk)|^(baum|pa-teller|kp-party|stier|mi-teller|schaefli|start-hoch|teller)$')
INSTAGRAM = 'https://www.instagram.com/schloessli_bottighofen/'
WEBSITE = 'https://www.schloessli-bottighofen.ch'


def herkunft(k, b):
    """(art, Quelle als Satz, Adresse)."""
    n = b.get('nachweis')
    d = b.get('datei') or ''
    if n:
        q = f"{n['urheber']}, {n['lizenz']}, Wikimedia Commons, {n['jahr']}"
        if k == 'abend-hafen':
            q += '. Sonnenuntergang am Seerhein bei Gottlieben, ein paar Kilometer unterhalb von Bottighofen'
        return 'frei', q, n.get('quelle', '')
    if d.startswith('extern/ig/'):
        return 'haus', 'Instagram des Hauses (@schloessli_bottighofen), Standbild aus einem Beitrag', INSTAGRAM
    if d.startswith('extern/myswitzerland/'):
        return 'haus', 'Schweiz Tourismus (myswitzerland.com), Bild aus dem Eintrag des Hauses', ''
    if d.startswith('website/'):
        return 'haus', 'Website des Hauses (schloessli-bottighofen.ch); Rechte beim Haus und den genannten Fotografen', WEBSITE
    raise SystemExit(f'Foto {k}: Herkunft unklar ({d}), erst klären')


def katalog():
    aus = []
    for g, ks in GRUPPE_FOTOS.items():
        for k in ks:
            if NICHT.search(k):
                raise SystemExit(f'Foto {k} gehört nicht ins Markenbuch')
            b = BJ.get(k)
            if not b:
                raise SystemExit(f'Foto {k} fehlt im Bildregister der Website')
            st = sorted(b['breiten'])
            for x in st:
                if not os.path.exists(os.path.join(IMG, f'{k}-{x}.webp')):
                    raise SystemExit(f'Foto {k}: {k}-{x}.webp fehlt in website/assets/img')
            gr, kl = st[-1], st[0]
            mi = max([x for x in st if x <= 1200] or [kl])
            with Image.open(os.path.join(IMG, f'{k}-{gr}.webp')) as im:
                w, h = im.size
            f = 'hoch' if h > w * 1.04 else 'quer' if w > h * 1.04 else 'quadrat'
            art, q, u = herkunft(k, b)
            aus.append(dict(k=k, t={'de': b['alt']}, b=g, s='sommer' if k in SOMMER else 'jahr', f=f, w=w, h=h, art=art, q=q, u=u, ue=False, alt=False, vn=False,
                            fl=f'../../assets/img/{k}-{gr}.webp', fm=f'../../assets/img/{k}-{mi}.webp', fs=f'../../assets/img/{k}-{kl}.webp'))
    return aus


# ---------------------------------------------------------------- Dateien
def ase(farben):
    def block(name, r, g, b):
        n = (name + '\0').encode('utf-16-be')
        body = struct.pack('>H', len(name) + 1) + n + b'RGB ' + struct.pack('>fff', r / 255, g / 255, b / 255) + struct.pack('>H', 2)
        return struct.pack('>HI', 1, len(body)) + body
    bl = b''.join(block(n, *rgb(h)) for n, h in farben)
    return b'ASEF' + struct.pack('>HHI', 1, 0, len(farben)) + bl


SCHRIFTEN = [
    ('t', 'Open Sans', 'OpenSans-var.woff2', 'Titel und Name, die Schrift der Wortmarke', '400, Versalien, Titel 0,14 em gesperrt, Name 0,3 em; nie fett, nie kursiv', 'Direkt im Hafen von Bottighofen', 400),
    ('s', 'Instrument Sans', 'InstrumentSans-normal-400_600.woff2', 'Lesetext', '400 bis 600, 18 px, Zeilenabstand 1,64', 'Den ganzen Tag durchgängig bieten wir die Karte der Lästermeile an.', 400),
    ('m', 'DM Mono', 'DMMono-normal-400.woff2', 'Zahlen, Etiketten und Gerichte wie auf der Karte', '400, Versalien, 0,16 em gesperrt', 'Seestrasse 50 · 8598 Bottighofen', 400),
    ('h', 'Caveat', 'Caveat-500.woff', 'Handschrift, nur einzelne Wörter auf der Website', '500, nie für Sätze', 'Lästermeile', 500),
]
LIZENZ = {'OpenSans-var.woff2': 'OFL-OpenSans.txt', 'Caveat-500.woff': 'OFL-Caveat.txt'}
VAR = {   # Fassungen der festen Dateien: (Gruppe, Schlüssel, Grund, Dateien ohne Vorsilbe)
    'zeichen': [('nacht', 'hell'), ('stuhl', 'hell'), ('himmel', 'dunkel'), ('weiss', 'dunkel')],
    'zeiger': [('nacht', 'hell'), ('stuhl', 'hell'), ('himmel', 'dunkel'), ('weiss', 'dunkel')],
    'logo': [('nacht', 'hell'), ('schwarz', 'hell'), ('weiss', 'dunkel'), ('himmel', 'dunkel')],
    'name': [('nacht', 'hell'), ('weiss', 'dunkel'), ('himmel', 'dunkel'), ('kurz-nacht', 'hell'), ('kurz-weiss', 'dunkel'), ('kurz-himmel', 'dunkel')],
}


def dateien(fa):
    liste = []
    for g, vs in VAR.items():
        var = []
        for k, grund in vs:
            ds = [f'{SCHLUESSEL}-{g}-{k}.{x}' for x in ('svg', 'png') if os.path.exists(os.path.join(DAT, f'{SCHLUESSEL}-{g}-{k}.{x}'))]
            if not ds:
                raise SystemExit(f'Datei fehlt: {g}-{k}')
            png = next((x for x in ds if x.endswith('.png')), None)
            var.append(dict(k=k, grund=grund, dateien=ds, px=list(Image.open(os.path.join(DAT, png)).size) if png else None))
        liste.append(dict(k=g, var=var))
    var = []
    for k, grund in (('dunkel', 'dunkel'), ('hell', 'hell')):
        ds = [f'{SCHLUESSEL}-tapete-{k}.{x}' for x in ('png', 'svg', 'webp')]
        var.append(dict(k=k, grund=grund, dateien=ds, px=list(Image.open(os.path.join(DAT, ds[0])).size)))
    liste.append(dict(k='tapete', var=var))
    liste.append(dict(k='website', var=[dict(k='original', grund='hell', dateien=[f'{SCHLUESSEL}-logo-original.png'], px=list(Image.open(os.path.join(DAT, f'{SCHLUESSEL}-logo-original.png')).size))]))
    css = ':root{\n' + ''.join(f'  --{k}:{h}; /* {n}: {r} */\n' for k, n, h, r, g, w in fa) + '}\n'
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.css'), 'w', encoding='utf-8').write(f'/* {HAUS} · Farben der Marke ({STAND}), Werte der Website, Farbwelt «Stuhl und See» */\n' + css)
    json.dump([dict(name=n, hex=h.upper(), rgb=list(rgb(h)), rolle=r, gruppe=g, woher=w) for k, n, h, r, g, w in fa],
              open(os.path.join(DAT, f'{SCHLUESSEL}-farben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.ase'), 'wb').write(ase([(n, h) for k, n, h, r, g, w in fa]))
    liste.append(dict(k='farben', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-farben.css', f'{SCHLUESSEL}-farben.json', f'{SCHLUESSEL}-farben.ase'])]))
    from fontTools.ttLib import TTFont
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-schriften.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for d_ in sorted({s[2] for s in SCHRIFTEN}):
            z.write(os.path.join(FONTS, d_), 'web/' + d_)
            f = TTFont(os.path.join(FONTS, d_)); f.flavor = None
            b = io.BytesIO(); f.save(b); z.writestr('programme/' + re.sub(r'\.woff2?$', '.ttf', d_), b.getvalue())
        for l in sorted(set(LIZENZ.values())):
            z.write(os.path.join(FONTS, l), 'lizenz/' + l)
        z.writestr('LIESMICH.txt', f'''{HAUS} · Schriften der Marke ({STAND})

Open Sans 400: Titel und Name, in Versalien gesperrt, die Schrift der Wortmarke. Nie fett, nie kursiv; betont wird über die Farbe.
Instrument Sans 400 bis 600: Lesetext.
DM Mono 400: Zahlen, Zeiten, Etiketten und Gerichte wie auf der Karte, in Versalien gesperrt.
Caveat 500: Handschrift, nur einzelne Wörter auf der Website, nie Sätze.

Alle stehen unter der SIL Open Font License 1.1 (frei für Druck, Website und Programme, auch gewerblich; nicht als Schrift allein verkaufen).
web/        die Dateien der Website
programme/  dieselben Schriften als TTF zum Installieren
lizenz/     Lizenztexte
''')
    liste.append(dict(k='schriften', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-schriften.zip'])]))
    alle = sorted(n_ for n_ in os.listdir(DAT) if not n_.endswith('-marke.zip'))   # erst die Liste, dann das ZIP (sonst packt es sich selbst ein)
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-marke.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for n_ in alle:
            z.write(os.path.join(DAT, n_), n_)
    return liste


def v_von(*namen):
    h = hashlib.sha1()
    for n in namen:
        p = os.path.join(HIER, n)
        h.update(open(p, 'rb').read() if os.path.exists(p) else b'-')
    return h.hexdigest()[:10]


def seite(F):
    v = v_von('livre.json'); vc = v_von('livre.css'); vj = v_von('livre.js')
    open(os.path.join(HIER, 'index.html'), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{NAME} · {HAUS}</title>
<meta name="description" content="{NAME}, die Marke der Wirtschaft am Schlössli zum Arbeiten: Fotos in fertigen Grössen, Zeichen, Logo, Name, Tapete und Farben als Dateien, Markenprüfung für Entwürfe, Hausregeln.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['nacht']}">
<link rel="icon" href="/assets/oberflaeche/kleid/schloessli-zeichen.svg" type="image/svg+xml">
<script src="/assets/oberflaeche/kleid/schloessli.js?v={v_von('../oberflaeche/kleid/schloessli.js')}"></script>
<link rel="preload" href="/assets/fonts/OpenSans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/DMMono-normal-400.woff2" as="font" type="font/woff2" crossorigin>
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


def main():
    t0 = time.time()
    fa = farben_liste()
    F = {k: h for k, n, h, r, g, w in fa}
    aus = katalog()
    liste = dateien(fa)
    groessen = {f: os.path.getsize(os.path.join(DAT, f)) for f in sorted(os.listdir(DAT))}
    gruppen = [dict(k=k, n=n, s=s, bild=GRUPPE_BILD[k][0], bild_t=GRUPPE_BILD[k][1]) for k, n, s in GRUPPEN]
    schriften = [dict(k=k, n=fam, d=d, r=r, e=ein, p=p, w=w, bild=f'listen/schrift-{k}.webp') for k, fam, d, r, ein, p, w in SCHRIFTEN]
    nicht = [re.sub(r'\s*\([^)]*\)', '', x) for x in MJ['ton']['nicht'] if not x.startswith(('Wir essen im', 'Statt zu'))]   # ohne Vermerke zur heutigen Seite
    nicht = ['das scharfe S statt ss' if 'ß' in x else x for x in nicht] + ['Superlative', 'Ausrufezeichen']
    daten = dict(haus=HAUS, ort=ORT, fotos=aus, dateien=liste,
                 farben=[dict(k=k, n=n, h=h.upper(), rgb=list(rgb(h)), r=r, g=g, woher=w) for k, n, h, r, g, w in fa],
                 gruppen=gruppen, glanz=[], groessen=groessen, bereiche=[b for b in BEREICHE if any(f['b'] == b for f in aus)],
                 schriften=schriften, namen=NAMEN, zusammen={},
                 ton=dict(eigene_worte=MJ['ton']['eigene_worte'], nicht=nicht),
                 stand=dict(fotos=len(aus), haus=sum(1 for x in aus if x['art'] == 'haus'), frei=sum(1 for x in aus if x['art'] == 'frei'),
                            ki=0, fremd=0, partner=0, ue=0, vn=0, original=0, dateien=len(groessen), datum=STAND))
    for f_ in [g['bild'] for g in gruppen if not g['bild'].startswith('../')] + [s['bild'] for s in schriften]:
        if not os.path.exists(os.path.join(HIER, f_)):
            raise SystemExit('Bild fehlt: ' + f_)
    import buch
    buch.aus_station5(os.path.join(MARKE, 'marke'), ROOT, gedreht, daten)
    for f_ in [g['bild'] for g in gruppen if g['bild'].startswith('buch/')]:
        if not os.path.exists(os.path.join(HIER, f_)):
            raise SystemExit('Bild fehlt: ' + f_)
    json.dump(daten, open(os.path.join(HIER, 'livre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    seite(F)
    st = daten['stand']
    print(f'livre.json: {len(aus)} Fotos ({st["haus"]} des Hauses, {st["frei"]} frei lizenziert) in {len(daten["bereiche"])} Gruppen · {len(groessen)} Dateien · {time.time() - t0:.0f} s')


if __name__ == '__main__':
    main()
