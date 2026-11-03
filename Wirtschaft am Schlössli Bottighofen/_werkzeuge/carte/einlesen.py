#!/usr/bin/env python3
"""Das Kartenpult (La Carte) · Wirtschaft am Schlössli Bottighofen: liest die Karten des Hauses einmal als Daten ein (20.10.2026, C17).
Kopie von einlesen.py der Tafel des Berghotel Gasterntal (dort aus dem Ruedihus und Doldenhorn).

Nichts wird abgetippt. Station 10 hat die Karten aus den PDFs des Hauses gelesen (_karten/stand/<id>.json, Abgleich 0 Abweichungen) und mit dem
Werkbank-Kit gesetzt: website/_werkbank/satz_daten.py → website/_werkbank/satz/u-<karte>.html (Stil satz.css daneben), daraus sind die PDFs unter
website/unterlagen/pdf/ gedruckt. Die eindeutigen Tippfehler des Originals sind dort schon berichtigt und gezählt (website/_werkbank/berichtigt.json).
Dieses Skript zerlegt den Satz in einen Baum: Elemente (Tag, Merkmale, Kinder), Texte (das, was das Haus ändert) und feste Teile (Zeichen, Umrisse,
Flaggen). Aus diesem Baum setzt satz/satz.js dasselbe HTML Zeichen für Zeichen wieder (python3 _werkzeuge/carte/pruefe.py rund).

Das Lunch-Menü (Mittagsmenü der Woche, C08) wird als Woche angelegt: Titel, Gruss, drei Gänge mit ihrer Zeile und der Preis, je Feld wörtlich aus
dem Satz u-lunch.html (Reihenfolge: erster Gang = Vorspeise, zweiter = Hauptgang, dritter = Dessert); satz.js setzt daraus dasselbe Blatt.
Der 4-Hands-Lunch hat keinen Satz und keine PDF (Station 10: nur in den Daten) und ist deshalb nicht im Werkzeug.

Nur gelesen wird website/_werkbank/ (satz/, fonts/, unterlagen.json). Geschrieben wird nur in _werkzeuge/carte/ (_daten/, satz/satz.css, satz/zeichen.json, fonts/).

    python3 _werkzeuge/carte/einlesen.py            nur wo noch kein Stand liegt (ein Stand des Hauses wird nie überschrieben)
    python3 _werkzeuge/carte/einlesen.py --grund    nur den Grundstand neu (_daten/grundstand/), für den Rundlauf und «Ursprünglicher Stand»
"""
import datetime, html, json, os, re, shutil, sys

HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(HIER))
PROJ = _WURZEL if os.path.isfile(os.path.join(_WURZEL, 'bau.py')) else os.path.join(_WURZEL, 'website')   # Schlössli: Website in website/
WB = os.path.join(PROJ, '_werkbank')
DATEN = os.environ.get('CARTE_DATEN') or os.path.join(HIER, '_daten')
sys.path.insert(0, HIER)

# Karten, die La Carte pflegt: Kennung = Ziel im Werkbank-Satz (u-<kennung>.html) = Name der PDF unter unterlagen/pdf/<kennung>.pdf
_PLAN = {d['ziel']: d for d in json.load(open(os.path.join(WB, 'unterlagen.json'), encoding='utf-8'))}
_GRUPPE = {'speisekarte': 'Restaurant', 'laestermeile': 'Bar', 'weinkarte': 'Keller', 'bankett': 'Banketts'}
KARTEN = {k: dict(name=_PLAN[k]['name'], unter='', gruppe=g, quelle=_PLAN[k]['quelle']) for k, g in _GRUPPE.items()}
LEER_TAG = {'img', 'br', 'hr', 'meta', 'link', 'input', 'wbr', 'col', 'source'}
A, Z = '', ''          # Platzhalter für feste Teile (Bilder als data:, Zeichen als svg) im Baum
TOKEN = re.compile(r'<!--.*?-->|<svg\b.*?</svg>|</?([a-zA-Z][\w-]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>', re.S)


class Teile:
    """Feste Teile einer Karte: jedes nur einmal gespeichert, im Baum steht der Platzhalter."""
    def __init__(self):
        self.liste, self.idx = [], {}

    def ref(self, s):
        if s not in self.idx:
            self.idx[s] = len(self.liste)
            self.liste.append(s)
        return f'{A}{self.idx[s]}{Z}'

    def at(self, s):   # data:-Bilder in Merkmalen
        return re.sub(r'data:[a-z]+/[\w.+-]+;base64,[A-Za-z0-9+/=]+', lambda m: self.ref(m.group(0)), s)


def text_kind(raw, T):
    """Text zwischen Tags: als Text (wenn er sich genau so wieder schreibt), sonst fest"""
    t = html.unescape(raw)
    if html.escape(t) == raw:
        return t
    return {'fn': 'roh', 'a': [T.at(raw)]}


def baum(s, T):
    """HTML → Liste von Kindern (Texte, Elemente {fn:'el', a:[tag, merkmale, *kinder]}, feste Teile {fn:'roh'})"""
    wurzel = {'fn': 'el', 'a': ['#', '']}
    stapel = [wurzel]
    pos = 0
    for m in TOKEN.finditer(s):
        if m.start() > pos:
            stapel[-1]['a'].append(text_kind(s[pos:m.start()], T))
        tok = m.group(0)
        pos = m.end()
        if tok.startswith('<!--'):
            stapel[-1]['a'].append({'fn': 'roh', 'a': [tok]})
            continue
        if tok.startswith('<svg'):
            stapel[-1]['a'].append({'fn': 'roh', 'a': [T.ref(tok) if len(tok) > 200 else tok]})
            continue
        tag, at = m.group(1), m.group(2)
        if tok.startswith('</'):
            oben = stapel.pop()
            assert oben['a'][0] == tag, ('Tag passt nicht', oben['a'][0], tag, s[max(0, m.start() - 80):m.start() + 20])
            continue
        el = {'fn': 'el', 'a': [tag, T.at(at)]}
        stapel[-1]['a'].append(el)
        if tag.lower() not in LEER_TAG and not at.rstrip().endswith('/'):
            stapel.append(el)
    if pos < len(s):
        stapel[-1]['a'].append(text_kind(s[pos:], T))
    assert len(stapel) == 1, ('offene Tags', [x['a'][0] for x in stapel])
    return wurzel['a'][2:]


def lies(kennung):
    pfad = os.path.join(WB, 'satz', 'u-' + kennung + '.html')
    h = open(pfad, encoding='utf-8').read()
    b = h.index('<body>') + len('<body>')
    e = h.rindex('</body>')
    kopf, koerper, fuss = h[:b], h[b:e], h[e:]
    T = Teile()
    seiten = []
    for x in baum(koerper, T):
        if isinstance(x, dict) and x['fn'] == 'el' and x['a'][0] == 'section':
            seiten.append({'fn': 'seite', 'a': x['a'][1:]})
        else:
            raise AssertionError(('zwischen den Seiten steht etwas', kennung, str(x)[:120]))
    fmt = re.search(r'@page\{size:(\d+)mm (\d+)mm', kopf)
    k = KARTEN[kennung]
    return dict(art='satz', ziel=kennung, name=k['name'], unter=k['unter'], gruppe=k['gruppe'], quelle=k['quelle'], schema=1,
                format=[int(fmt.group(1)), int(fmt.group(2))], kopf=kopf, fuss=fuss, seiten=seiten, teile=T.liste)


def _svg_in(h, kl):
    m = re.search(r'class="[^"]*\b' + re.escape(kl) + r'\b[^"]*"[^>]*>\s*(<svg\b.*?</svg>)', h, re.S)
    return m.group(1) if m else ''


def zeichen():
    """Feste Teile für das Blatt des Lunch-Menüs, aus dem Satz u-lunch.html: Zeichen über dem Titel, Blatt zwischen den Gängen, Fusszeile."""
    h = open(os.path.join(WB, 'satz', 'u-lunch.html'), encoding='utf-8').read()
    fuss = re.search(r'<footer class="ufuss2">(.*?)</footer>', h, re.S).group(1)
    return dict(ZEICHEN=_svg_in(h, 'sb-zeichen'), BLATT=_svg_in(h, 'sb-gang'), FUSS=html.unescape(fuss), WORTMARKE='')


def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    t = p + '.neu'
    with open(t, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(t, encoding='utf-8'))
    os.replace(t, p)


def beigaben():
    """Was der Satz zum Setzen braucht, als Kopie ins Werkzeug (Werkzeuge hängen nur vom eigenen Ordner ab): satz.css, Schriften."""
    os.makedirs(os.path.join(HIER, 'satz'), exist_ok=True)
    shutil.copy2(os.path.join(WB, 'satz', 'satz.css'), os.path.join(HIER, 'satz', 'satz.css'))
    os.makedirs(os.path.join(HIER, 'fonts'), exist_ok=True)
    for f in os.listdir(os.path.join(WB, 'fonts')):
        if f.endswith('.ttf'):
            shutil.copy2(os.path.join(WB, 'fonts', f), os.path.join(HIER, 'fonts', f))
    css = open(os.path.join(HIER, 'satz', 'satz.css'), encoding='utf-8').read()
    for url in sorted(set(re.findall(r"url\(['\"]?([^'\")]+)['\"]?\)", css))):   # weitere Dateien, auf die satz.css zeigt (Schrift der Idee, Tapete)
        if url.startswith('data:') or url.startswith('../fonts/'):
            continue
        quelle = os.path.normpath(os.path.join(WB, 'satz', url))
        ziel = os.path.normpath(os.path.join(HIER, 'satz', url))
        if os.path.isfile(quelle) and ziel.startswith(HIER + os.sep):
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
            shutil.copy2(quelle, ziel)


def weinbilder():
    """Flaschen aus dem Weinberater der Website (assets/data/weine.json, assets/img/wein/f-<id>.webp) für die Bilder in der Liste der Weinkarte.
    Nur Weine, deren Bild wirklich da ist (sonst 404 im Werkzeug). Schlüssel: Weingut|Name wie im Satz. Rechte der Flaschenbilder: bei der Website offen."""
    try:
        weine = json.load(open(os.path.join(PROJ, 'assets', 'data', 'weine.json'), encoding='utf-8'))
    except (OSError, ValueError):
        weine = []
    da = set(os.listdir(os.path.join(PROJ, 'assets', 'img', 'wein'))) if os.path.isdir(os.path.join(PROJ, 'assets', 'img', 'wein')) else set()
    aus = {(w.get('erzeuger') or '') + '|' + (w.get('name') or ''): w['id'] for w in weine if f"f-{w['id']}.webp" in da}   # Weine ohne Weingut (Hauswein) brechen nicht ab
    _schreib(os.path.join(HIER, 'satz', 'weinbilder.json'), aus)
    return len(aus)


def vorschaubilder():
    """Kleine Bilder für die Liste und die Kacheln (52 px, doppelt dicht): Fotos des Hauses und Flaschen des Weinberaters, je 112 × 112 px.
    Die Website hat als kleinste Grösse 480 px; 30 Zeilen mit je 35 kB wären am Handy auf langsamer Leitung zu schwer (gedrosselt gemessen 20.10.2026)."""
    from PIL import Image
    ziel = os.path.join(HIER, 'bilder', 'z')
    os.makedirs(ziel, exist_ok=True)
    namen = ['tortelloni', 'suppe', 'bar', 'wein', 'gaststube', 'stier', 'thon', 'pasta', 'iberia', 'anguria', 'salat', 'dessert', 'torte']
    n = 0
    for nm in namen:
        q = os.path.join(PROJ, 'assets', 'img', nm + '-480.webp')
        if not os.path.isfile(q):
            continue
        im = Image.open(q).convert('RGB'); w, h = im.size; k = min(w, h)
        im.crop(((w - k) // 2, (h - k) // 2, (w - k) // 2 + k, (h - k) // 2 + k)).resize((112, 112), Image.LANCZOS).save(os.path.join(ziel, nm + '.webp'), 'WEBP', quality=78)
        n += 1
    try:
        wb = json.load(open(os.path.join(HIER, 'satz', 'weinbilder.json'), encoding='utf-8'))
    except (OSError, ValueError):
        wb = {}
    for i in sorted(set(wb.values())):
        q = os.path.join(PROJ, 'assets', 'img', 'wein', f'f-{i}.webp')
        im = Image.open(q).convert('RGBA'); im.thumbnail((100, 100), Image.LANCZOS)
        grund = Image.new('RGBA', (112, 112), (231, 236, 243, 255)); grund.alpha_composite(im, ((112 - im.width) // 2, (112 - im.height) // 2))
        grund.convert('RGB').save(os.path.join(ziel, f'f-{i}.webp'), 'WEBP', quality=78)
        n += 1
    return n


def montag():
    d = datetime.date.today()
    return (d - datetime.timedelta(days=d.weekday())).isoformat()


def mittag():
    """Lunch-Menü als Woche (C08 in der Form des Hauses). Jedes Feld wörtlich aus dem Satz u-lunch.html; passt die Form nicht, bricht es ab."""
    h = open(os.path.join(WB, 'satz', 'u-lunch.html'), encoding='utf-8').read()
    t = lambda m: html.unescape(re.sub(r'<[^>]+>', '', m)).strip()
    gruss = re.findall(r'<p class="sb-gruss">(.*?)</p>', h, re.S)
    titel = re.findall(r'<h2 class="sb-band">(.*?)</h2>', h, re.S)
    gaenge = re.findall(r'<div class="sb-m"><p class="sb-n sb-n--gross">(.*?)</p>((?:<p class="sb-t">.*?</p>)*)</div>', h, re.S)
    pr = re.search(r'<div class="sb-lunchpreis"><span class="g">(\d+) (\S+)</span><i></i><span class="z">(\d+)<small>(.*?)</small></span><span class="w">(.*?)</span></div>', h)
    assert len(gruss) == 1 and len(titel) == 1 and len(gaenge) == 3 and pr, ('Lunch-Menü hat eine andere Form als erwartet', gruss, titel, len(gaenge), bool(pr))
    tag = dict(zu=False, hinweis='')
    for g, (name, zeilen) in zip(('vorspeise', 'haupt', 'dessert'), gaenge):
        z = re.findall(r'<p class="sb-t">(.*?)</p>', zeilen, re.S)
        assert len(z) <= 1, ('Gang mit mehr als einer Zeile', name)
        tag[g], tag[g + '_z'] = t(name), t(z[0]) if z else ''
    preis = f'({pr.group(1)} – {pr.group(2)} – {pr.group(3)}{t(pr.group(4))} {t(pr.group(5))})'   # Wortlaut des Hauses, wie satz_daten.py menupreis() ihn zerlegt
    w = dict(ab=montag(), titel=t(titel[0]), gruss=t(gruss[0]), zeiten='', preis=preis, zusatz='', spruch='', fuss='', tage=[tag], beispiel=False)
    return dict(art='mittag', ziel='mittag', name=_PLAN['lunch']['name'], unter='der Woche', gruppe='Restaurant', quelle=_PLAN['lunch']['quelle'],
                schema=1, format=[297, 210], woche=w, seiten=[], teile=[])


def alle():
    aus = {k: lies(k) for k in KARTEN}
    aus['mittag'] = mittag()
    return aus


if __name__ == '__main__':
    grund_nur = '--grund' in sys.argv
    beigaben()
    karten = alle()
    _schreib(os.path.join(HIER, 'satz', 'zeichen.json'), zeichen())
    print('Flaschenbilder für die Weinkarte:', weinbilder())
    print('Vorschaubilder:', vorschaubilder())
    for kennung, d in karten.items():
        _schreib(os.path.join(DATEN, 'grundstand', kennung + '.json'), d)
        ziel = os.path.join(DATEN, 'stand', kennung + '.json')
        if grund_nur:
            continue
        if os.path.exists(ziel):
            print(f'{kennung}: Stand liegt schon, bleibt (Grundstand erneuert)')
            continue
        _schreib(ziel, dict(d, veroeffentlicht=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wer='Einlesen'))
        print(f'{kennung}: {len(d["seiten"]) or 1} Seiten eingelesen, {len(d["teile"])} feste Teile')
