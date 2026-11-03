#!/usr/bin/env python3
"""Das Kartenpult · Wirtschaft am Schlössli: liest die fünf Karten des Hauses einmal als Daten ein (Nachtbau 3.11.2026, C17).
Kopie von einlesen.py der Tafel im Schäfli, Inhalt aus diesem Haus.

Nichts wird abgetippt. satz_bau.py setzt die Karten aus den Daten der Website (website/inhalt/karte.json, lunch.json, laestermeile.json,
wein.json, bankett.json) im Kleid des Hauses nach satz/u-<karte>.html. Dieses Skript zerlegt den Satz in einen Baum: Elemente (Tag, Merkmale,
Kinder), Texte (das, was das Haus ändert) und feste Teile (Zeichen und Wortmarke). Aus diesem Baum setzt satz/satz.js dasselbe HTML Zeichen
für Zeichen wieder (python3 _werkzeuge/carte/pruefe.py rund).

Geschrieben wird nur in _werkzeuge/carte/ (_daten/, bilder/z/, bilder/fotos.json).

    python3 _werkzeuge/carte/einlesen.py            nur wo noch kein Stand liegt (ein Stand des Hauses wird nie überschrieben)
    python3 _werkzeuge/carte/einlesen.py --grund    nur den Grundstand neu (_daten/grundstand/), für den Rundlauf und «Ursprünglicher Stand»
"""
import datetime, html, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(HIER))
PROJ = os.path.join(_WURZEL, 'website')
DATEN = os.environ.get('CARTE_DATEN') or os.path.join(HIER, '_daten')
sys.path.insert(0, HIER)

_STAND = {n: json.load(open(os.path.join(PROJ, 'inhalt', n + '.json'), encoding='utf-8')).get('stand', '') for n in ('karte', 'lunch', 'laestermeile', 'wein', 'bankett')}
# Karten, die das Kartenpult pflegt: Kennung = Satz satz/u-<kennung>.html = Name der PDF. Reihenfolge = Reihenfolge in der Seitenleiste.
KARTEN = {
    'speisekarte': dict(name='Karte', unter='nach Ländern', gruppe='Restaurant', quelle='website/inhalt/karte.json · ' + _STAND['karte']),
    'lunch': dict(name='Lunch', unter='am Mittag', gruppe='Restaurant', quelle='website/inhalt/lunch.json · ' + _STAND['lunch']),
    'laestermeile': dict(name='Lästermeile', unter='an der Bar', gruppe='Lästermeile', quelle='website/inhalt/laestermeile.json · ' + _STAND['laestermeile']),
    'weinkarte': dict(name='Weinkarte', unter='aus dem Keller', gruppe='Keller', quelle='website/inhalt/wein.json · ' + _STAND['wein']),
    'bankett': dict(name='Bankett', unter='für Gruppen', gruppe='Banketts', quelle='website/inhalt/bankett.json · ' + _STAND['bankett']),
}
LEER_TAG = {'img', 'br', 'hr', 'meta', 'link', 'input', 'wbr', 'col', 'source'}
A, Z = '', ''          # Platzhalter für feste Teile (Zeichen als svg) im Baum
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
    pfad = os.path.join(HIER, 'satz', 'u-' + kennung + '.html')
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


def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    t = p + '.neu'
    with open(t, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(t, encoding='utf-8'))
    os.replace(t, p)


# Fotos des Hauses für Liste und Kacheln (Register website/inhalt/bilder.json, ausgeliefert unter /assets/img/<schlüssel>-<breite>.webp):
# je Karte ein Foto, das zu ihr gehört (Teller von oben, Suppe am Mittag, die Bar, das Weinregal, die Gaststube für Banketts)
FOTOS = {'speisekarte': 'anguria', 'lunch': 'suppe', 'laestermeile': 'bar', 'weinkarte': 'wein', 'bankett': 'gaststube'}


def vorschaubilder():
    """Kleine Bilder für die Liste und die Kacheln (112 × 112 px aus der kleinsten Liefergrösse der Website); fotos.json: Karte → Schlüssel."""
    from PIL import Image
    reg = json.load(open(os.path.join(PROJ, 'inhalt', 'bilder.json'), encoding='utf-8'))
    ziel = os.path.join(HIER, 'bilder', 'z')
    os.makedirs(ziel, exist_ok=True)
    for f in os.listdir(ziel):
        if f.endswith('.webp') and f[:-5] not in FOTOS.values():
            os.remove(os.path.join(ziel, f))
    for nm in sorted(set(FOTOS.values())):
        assert nm in reg, ('Bild nicht im Register', nm)
        q = os.path.join(PROJ, 'assets', 'img', nm + '-480.webp')
        if not os.path.isfile(q):
            raise SystemExit(f'Bild fehlt: {q}')
        im = Image.open(q).convert('RGB'); w, h = im.size; k = min(w, h)
        im.crop(((w - k) // 2, (h - k) // 2, (w - k) // 2 + k, (h - k) // 2 + k)).resize((112, 112), Image.LANCZOS).save(os.path.join(ziel, nm + '.webp'), 'WEBP', quality=80)
    gross = {}
    for z, nm in FOTOS.items():   # grösste Liefergrösse bis 1200 px für das Startbild
        br = sorted(b for b in reg[nm].get('breiten', []) if b <= 1200 and os.path.isfile(os.path.join(PROJ, 'assets', 'img', f'{nm}-{b}.webp')))
        gross[z] = [nm, br[-1] if br else 800, reg[nm].get('alt', '')]
    _schreib(os.path.join(HIER, 'bilder', 'fotos.json'), gross)
    return len(set(FOTOS.values()))


def alle():
    return {k: lies(k) for k in KARTEN}


if __name__ == '__main__':
    grund_nur = '--grund' in sys.argv
    karten = alle()
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
