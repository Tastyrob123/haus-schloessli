#!/usr/bin/env python3
"""Das Hausbuch · Wirtschaft am Schlössli · Prüfung der Dateien und Downloads ohne Browser (FUNKTIONEN.md Zeilen 85, 86, 90). Nur lesen, schreibt nur ergebnisse/.
85  jede Datei gegen ihre Quelle: Farben (livre.json, CSS, JSON, ASE) gegen assets/css/main.css und die Handschrift der Werkbank (_werkbank/marke_werkbank.py),
    Schriften Byte für Byte die der Website, Tapete = Website (butzen-07/-09.png, Muster aus main.css) und Werkbank (.tapete-hell), Logo der heutigen Website =
    Mediathek, Zeichen-SVG = Pfade aus assets/logo/zeichen.svg, Logo in Lage und Grösse wie das Original vermessen, Farben aller Varianten, ZIP = Einzeldateien.
86  jedes Foto in allen vier Grössen (wie «Laden», ohne Server): Masse, JPEG, «-mit-ki-erzeugt» genau bei KI, ohne Original «websitegroesse», Ausschnitt wirkt.
90  Probe-Antwort ohne Claude: Prüfung läuft durch, kein Schlüssel wird gelesen, keine Anfrage nach aussen.
   python3 _werkzeuge/livre/pruefung/dateien_pruef.py"""
import builtins, hashlib, io, json, os, re, struct, sys, time, urllib.request, zipfile
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__))
LIV = os.path.dirname(HIER)
ROOT = os.path.dirname(os.path.dirname(LIV))
sys.path.insert(0, LIV)
os.environ.pop('LIVRE_KI', None); os.environ.pop('ANTHROPIC_API_KEY', None)
import livre as LV  # noqa: E402
L = json.load(open(os.path.join(LIV, 'livre.json'), encoding='utf-8'))
DAT = os.path.join(LIV, 'dateien')
erg = []
def z(nr, t, ok, m=''): erg.append(dict(nr=nr, t=t, ok=bool(ok), m=str(m)[:300])); print(('✓' if ok else '✗'), nr, t, '·', str(m)[:200])
sha = lambda b: hashlib.sha1(b).hexdigest()

# ---------------------------------------------------------------- 85 Dateien gegen ihre Quelle
import ast, urllib.parse
S_ = 'wirtschaft-am-schloessli-'
p85 = []
css = open(os.path.join(ROOT, 'assets', 'css', 'main.css'), encoding='utf-8').read()
root = {}
for blk in re.findall(r':root\s*\{(.*?)\}', css, re.S):
    for k, v in re.findall(r'--([a-z0-9]+)\s*:\s*(#[0-9a-fA-F]{6})', blk):
        root.setdefault(k, v)
wb = next(ast.literal_eval(n.value) for n in ast.parse(open(os.path.join(ROOT, '_werkbank', 'marke_werkbank.py'), encoding='utf-8').read()).body
          if isinstance(n, ast.Assign) and any(getattr(t, 'id', '') == 'GRUPPEN' for t in n.targets))
wb_werte = [hx.upper() for _, l in wb for _, _, hx in l]
for f in L['farben']:
    if root.get(f['k'], '').upper() != f['h']: p85.append('Website ' + f['k'] + ' ' + f['h'] + ' ≠ ' + root.get(f['k'], '?'))
    if tuple(f['rgb']) != tuple(int(f['h'][i:i + 2], 16) for i in (1, 3, 5)): p85.append('RGB ' + f['k'])
if [f['h'] for f in L['farben'] if f['g'] != 'weitere'] != wb_werte: p85.append('Neun Töne und Geranie ≠ Handschrift der Werkbank')
cssd = open(os.path.join(DAT, S_ + 'farben.css'), encoding='utf-8').read()
jsond = json.load(open(os.path.join(DAT, S_ + 'farben.json'), encoding='utf-8'))
ase = open(os.path.join(DAT, S_ + 'farben.ase'), 'rb').read()
for f in L['farben']:
    if f['h'].lower() not in cssd.lower(): p85.append('CSS ohne ' + f['k'])
if [x['hex'].upper() for x in jsond] != [f['h'] for f in L['farben']]: p85.append('JSON-Farben weichen ab')
if ase[:4] != b'ASEF' or struct.unpack('>I', ase[8:12])[0] != len(L['farben']): p85.append('ASE-Kopf')
else:
    i, gelesen = 12, []
    while i < len(ase):
        typ, laenge = struct.unpack('>HI', ase[i:i + 6]); body = ase[i + 6:i + 6 + laenge]; i += 6 + laenge
        nl = struct.unpack('>H', body[:2])[0]; r, g, b = struct.unpack('>fff', body[2 + nl * 2 + 4:2 + nl * 2 + 16])
        gelesen.append('#%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255)))
    if gelesen != [f['h'] for f in L['farben']]: p85.append('ASE-Werte ' + ','.join(gelesen[:3]))
for s in L['schriften']:
    if not os.path.exists(os.path.join(ROOT, 'assets', 'fonts', s['d'])): p85.append('Schrift fehlt ' + s['d'])
    if s['d'] not in css: p85.append('Schrift nicht in main.css ' + s['d'])
with zipfile.ZipFile(os.path.join(DAT, S_ + 'schriften.zip')) as zf:
    for s in L['schriften']:
        if sha(zf.read('web/' + s['d'])) != sha(open(os.path.join(ROOT, 'assets', 'fonts', s['d']), 'rb').read()): p85.append('Schrift im ZIP ≠ Website ' + s['d'])
        from fontTools.ttLib import TTFont
        t = TTFont(io.BytesIO(zf.read('programme/' + s['d'].replace('.woff2', '.ttf'))))
        if 'glyf' not in t and 'CFF ' not in t: p85.append('TTF ohne Umrisse ' + s['d'])
werkbank = open(os.path.join(ROOT, '_werkbank', 'haus.py'), encoding='utf-8').read()
for v in next(g for g in L['dateien'] if g['k'] == 'tapete')['var']:
    q = {'holz': 'butzen-07.png', 'fuss': 'butzen-09.png'}.get(v['k'])
    if q:
        if sha(open(os.path.join(DAT, v['dateien'][0]), 'rb').read()) != sha(open(os.path.join(ROOT, 'assets', 'img', q), 'rb').read()): p85.append('Tapete ≠ Website ' + v['k'])
        if q not in css: p85.append('Tapete nicht auf der Website ' + q)
    svg = open(os.path.join(DAT, v['dateien'][1]), encoding='utf-8').read()
    st = re.search(r"stroke='(#[0-9a-f]{6})' stroke-opacity='([.\d]+)'", svg).groups()
    quelle = css if q else werkbank
    if urllib.parse.quote(st[0]).replace('%23', '%23') not in quelle.replace('%23', '#').replace('#', '%23') or f"stroke-opacity='{st[1]}'" not in quelle.replace(f"stroke-opacity='{st[1].lstrip('0')}'", f"stroke-opacity='{st[1]}'"):
        p85.append('Muster ' + v['k'] + ' nicht in der Quelle ' + str(st))
    im = Image.open(os.path.join(DAT, v['dateien'][0])).convert('RGBA')
    if im.size != (112, 112) or im.getchannel('A').getextrema()[0] != 0: p85.append('Tapete-PNG ' + v['k'] + ' ' + str(im.size))
F = {f['k']: f['h'] for f in L['farben']}
FARBE = {'gold': F['gold'], 'hellgold': F['gold2'], 'holz': F['holz'], 'weiss': F['blatt']}
def farbe_von(pfad):
    im = Image.open(pfad).convert('RGBA')
    return next(('#%02X%02X%02X' % px[:3] for px in im.get_flattened_data() if px[3] == 255), None), im
zsvg = open(os.path.join(ROOT, 'assets', 'logo', 'zeichen.svg'), encoding='utf-8').read()
d0 = re.findall(r'\sd="([^"]+)"', zsvg)
for v in next(g for g in L['dateien'] if g['k'] == 'zeichen')['var']:
    s = open(os.path.join(DAT, v['dateien'][0]), encoding='utf-8').read()
    if re.findall(r'\sd="([^"]+)"', s) != d0: p85.append('Zeichen-Pfad verändert ' + v['k'])
    if f'fill="{FARBE[v["k"]].lower()}"' not in s.lower(): p85.append('Zeichen-SVG-Farbe ' + v['k'])
    c, im = farbe_von(os.path.join(DAT, v['dateien'][1]))
    if c != FARBE[v['k']] or im.getpixel((0, 0))[3] != 0: p85.append('Zeichen-PNG ' + v['k'] + ' ' + str(c))
orig = Image.open(os.path.join(ROOT, 'assets', 'logo', 'wortmarke-original.png')).convert('RGBA').getchannel('A').point(lambda x: 255 if x > 40 else 0)
lg = next(g for g in L['dateien'] if g['k'] == 'logo')
for v in lg['var']:
    c, im = farbe_von(os.path.join(DAT, v['dateien'][1]))
    if c != FARBE[v['k']]: p85.append('Logo-Farbe ' + v['k'] + ' ' + str(c))
    a = im.getchannel('A').point(lambda x: 255 if x > 40 else 0).resize((323, 116), Image.LANCZOS)
    o = orig.crop((27, 8, 350, 124))
    import numpy as np
    A, O = np.asarray(a) > 127, np.asarray(o) > 127
    # Zeichen links: Fläche gleich (dieselbe Zeichnung), Text rechts: Ober- und Unterkanten der zwei Zeilen wie im Original (±2 Punkte)
    def kasten(M):
        y = np.where(M.any(1))[0]; x = np.where(M.any(0))[0]; return (int(x.min()), int(y.min()), int(x.max()), int(y.max()))
    za, zo = kasten(A[:, :90]), kasten(O[:, :90])     # Zeichen: gleicher Platz (die Zeichnung selbst ist die der Karte, das alte Logo ist dichter gefüllt)
    def zeilen(M):
        r = np.where(M[:, 102:].any(1))[0]; t = []; s0 = r[0]; pr = r[0]
        for y in r[1:]:
            if y != pr + 1: t.append((int(s0), int(pr))); s0 = y
            pr = y
        t.append((int(s0), int(pr))); return t
    ta, to = zeilen(A), zeilen(O)
    breite_a = [int(np.where(A[y0:y1 + 1, 102:].any(0))[0].max() + 102) for y0, y1 in ta]
    if any(abs(p_ - q_) > 3 for p_, q_ in zip(za, zo)) or len(ta) != 2 or abs(ta[0][1] - to[0][1]) > 2 or abs(ta[1][1] - to[1][1]) > 2 or any(b_ > 323 for b_ in breite_a):
        p85.append(f'Logo-Lage {v["k"]}: Zeichen {za}/{zo}, Zeilen {ta}/{to}, rechts {breite_a}')
    lage = f'Zeichen {za}/{zo}, Zeilen {ta}/{to}'
web = lambda n: sha(open(n, 'rb').read())
mediathek = os.path.expanduser('~/Desktop/Website-Projekte/Carlton-Europe Interlaken/_quelle/doldenhorn-ruedihus/website/mediathek/225012_Ruedihus_logo.png')
if web(os.path.join(DAT, S_ + 'logo-website-heute.png')) != web(os.path.join(ROOT, 'assets', 'logo', 'wortmarke-original.png')) or (os.path.exists(mediathek) and web(mediathek) != web(os.path.join(DAT, S_ + 'logo-website-heute.png'))):
    p85.append('Logo der heutigen Website ≠ Mediathek')
for v in next(g for g in L['dateien'] if g['k'] == 'name')['var']:
    k = v['k'].replace('kurz-', '')
    s = open(os.path.join(DAT, v['dateien'][0]), encoding='utf-8').read()
    c, im = farbe_von(os.path.join(DAT, v['dateien'][1]))
    if f'fill="{FARBE[k].lower()}"' not in s.lower() or c != FARBE[k] or im.getpixel((0, 0))[3] != 0: p85.append('Name ' + v['k'] + ' ' + str(c))
with zipfile.ZipFile(os.path.join(DAT, S_ + 'marke.zip')) as zf:
    namen = set(zf.namelist())
    alle = {n for n in os.listdir(DAT) if n != S_ + 'marke.zip'}
    if namen != alle: p85.append('ZIP ≠ Einzeldateien: ' + str(sorted(alle ^ namen))[:120])
    for nm in namen:
        if sha(zf.read(nm)) != sha(open(os.path.join(DAT, nm), 'rb').read()): p85.append('ZIP-Inhalt ≠ ' + nm)
if set(L['groessen']) != set(os.listdir(DAT)) or any(os.path.getsize(os.path.join(DAT, k)) != v for k, v in L['groessen'].items()): p85.append('Grössen in livre.json veraltet')
z(85, 'Jede Datei gegen ihre Quelle (Farben, Schriften, Tapete, Zeichen, Logo, Name, ZIP)', not p85, ' | '.join(p85) or f'{len(L["farben"])} Farben, {len(L["schriften"])} Schriften, {len(alle)} Dateien, ZIP gleich, Logo {lage}')

# ---------------------------------------------------------------- 86 jedes Foto in allen vier Grössen
fehl, ws, n, t0 = [], [], 0, time.time()
ohne = set(LV.ohne_original())
for f in L['fotos']:
    for g in ('instagram', 'story', 'web', 'druck'):
        try:
            d, typ, name = LV.bild(f['k'], g, .5, .5)
            im = Image.open(io.BytesIO(d)); im.load(); n += 1
            w, h = im.size
            soll = {'instagram': (1080, 1350), 'story': (1080, 1920)}.get(g)
            if soll and (w, h) != soll: fehl.append(f"{f['k']} {g} {w}x{h}")
            if g == 'web' and (max(w, h) > 2000 or (max(f['w'], f['h']) >= 2000 and max(w, h) != 2000)): fehl.append(f"{f['k']} web {w}x{h}")
            if g == 'druck':
                if 'websitegroesse' in name:
                    ws.append(f['k'])
                    if f['k'] not in ohne: fehl.append(f"{f['k']} Druck in Website-Grösse, obwohl Original da")
                elif abs(w - f['w']) > 2 or abs(h - f['h']) > 2: fehl.append(f"{f['k']} druck {w}x{h} ≠ {f['w']}x{f['h']}")
                if f['k'] in ohne and 'websitegroesse' not in name: fehl.append(f"{f['k']} ohne Original, Name sagt es nicht")
            if ('-mit-ki-erzeugt' in name) != (f['art'] == 'ki'): fehl.append(f"{f['k']} {g} Name {name}")
            if not name.startswith('wirtschaft-am-schloessli-') or im.format != 'JPEG' or typ != 'image/jpeg': fehl.append(f"{f['k']} {g} {im.format} {name}")
        except Exception as e:  # noqa: BLE001
            fehl.append(f"{f['k']} {g} FEHLER {e}")
a, _, _ = LV.bild('platanen', 'instagram', 0, 0); b, _, _ = LV.bild('platanen', 'instagram', 1, 1)
if a == b: fehl.append('Ausschnitt x/y wirkt nicht')
z(86, f'Alle {len(L["fotos"])} Fotos in allen vier Grössen ({n} Dateien)', not fehl, (' | '.join(fehl[:4]) or f'0 Abweichungen, {len(ws)} ohne Original in Website-Grösse benannt') + f', {time.time() - t0:.0f} s')

# ---------------------------------------------------------------- 91 Herkunft je Foto mit Datum und Weg zur Quelle
ohne_q = [f['k'] for f in L['fotos'] if not f.get('q') or 'offen' in f['q']]
ohne_u = [f['k'] for f in L['fotos'] if not f.get('u') and not f['k'].startswith('haus-') ]
schlecht_u = [f['k'] for f in L['fotos'] if f.get('u') and not re.match(r'^https://(doldenhorn-ruedihus\.ch|www\.myswitzerland\.com|www\.booking\.com|commons\.wikimedia\.org)/', f['u'])]
mit_datum = sum(1 for f in L['fotos'] if re.search(r'\d{2}\.\d{2}\.\d{4}', f.get('q', '')))
z(91, 'Herkunft je Foto aus den Unterlagen, mit Weg zur Quelle (ausser den drei Schwesterhäusern)', not ohne_q and not ohne_u and not schlecht_u,
  f"{len(L['fotos'])} Fotos, {sum(1 for f in L['fotos'] if f.get('u'))} mit Weg, {mit_datum} mit Datum · ohne Herkunft {ohne_q} · ohne Weg {ohne_u} · fremder Weg {schlecht_u}")

# ---------------------------------------------------------------- 90 Probe-Antwort ohne Claude
gelesen, aussen = [], []
_open, _url = builtins.open, urllib.request.urlopen
def open_wache(p, *a, **k):
    if 'API Key' in str(p): gelesen.append(str(p))
    return _open(p, *a, **k)
def url_wache(*a, **k):
    aussen.append(str(a[0])[:80]); raise OSError('keine Anfrage nach aussen in der Probe')
builtins.open, urllib.request.urlopen = open_wache, url_wache
try:
    import base64
    png = io.BytesIO(); Image.new('RGB', (600, 400), (50, 31, 16)).save(png, 'PNG')
    r = LV.pruefen({'name': 'probe.png', 'daten': 'data:image/png;base64,' + base64.b64encode(png.getvalue()).decode(), 'sprache': 'de'})
finally:
    builtins.open, urllib.request.urlopen = _open, _url
z(90, 'Probe-Antwort ohne Claude: kein Schlüssel gelesen, keine Anfrage nach aussen, Antwort in derselben Form', r.get('probe') and r['ki'].get('punkte') and not gelesen and not aussen and r['messung']['im_rahmen'] > .9,
  f"{len(r['ki']['punkte'])} Punkte, {round(r['messung']['im_rahmen'] * 100)} % im Rahmen, Schlüssel {len(gelesen)}, aussen {len(aussen)}")

os.makedirs(os.path.join(HIER, 'ergebnisse'), exist_ok=True)
json.dump(erg, open(os.path.join(HIER, 'ergebnisse', 'dateien.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"Summe: {sum(e['ok'] for e in erg)}/{len(erg)}")
sys.exit(0 if all(e['ok'] for e in erg) else 1)
