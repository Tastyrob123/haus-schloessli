# Wirtschaft am Schlössli, Potentialanalyse, Entwurf ohne Blender (Robert 19.10.2026): schlichte Aufnahmen der heutigen Seite,
# jede gemeinte Stelle mit rotem Kreis. Je Stelle zwei Bilder: «ganz» (ganzer Bildschirm, zeigt wo) und «nah» (Ausschnitt, zeigt was).
#   python3 belege.py → ../potential/belege/<id>-ganz.webp, <id>-nah.webp + belege.json
import json, os, subprocess
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); ST = H + '/stellen/'
OUT = os.path.join(os.path.dirname(H), 'potential', 'belege'); os.makedirs(OUT, exist_ok=True)
S = json.load(open(ST + 'stellen.json')); ROT = (196, 30, 36); INFO = {}

def zusammen(marks, luft=10):
    """Stellen, die sich berühren (Name und Rolle untereinander), bekommen einen gemeinsamen Kreis."""
    bx = [[m['x'], m['y'], m['x'] + m['w'], m['y'] + m['h']] for m in marks]
    fertig = False
    while not fertig:
        fertig = True
        for i in range(len(bx)):
            for j in range(i + 1, len(bx)):
                a, b = bx[i], bx[j]
                if a[0] - luft < b[2] and b[0] - luft < a[2] and a[1] - luft < b[3] and b[1] - luft < a[3]:
                    bx[i] = [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]; bx.pop(j); fertig = False; break
            if not fertig: break
    return bx

def kreise(im, marks, f, y0=0):
    """Roter Ring als Kapsel eng um die Stelle: schneidet keine Nachbarzeile, Schrift bleibt frei."""
    d = ImageDraw.Draw(im)
    for x0, y0_, x1, y1 in zusammen(marks):
        p = 7; r = min((y1 - y0_) / 2 + p, 22)
        d.rounded_rectangle(((x0 - p - 4) * f, (y0_ - p) * f, (x1 + p + 4) * f, (y1 + p) * f), radius=r * f, outline=ROT, width=round(3 * f))
    return im

def sichern(im, name, breite):
    if im.width > breite: im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{name}.webp', 'WEBP', quality=84, method=6); return im.size

def stelle(id, nah=None, ohne_kreis=()):
    s = S[id]; f = s['f']; im = Image.open(ST + id + '.png').convert('RGB')
    marks = [m for i, m in enumerate(s['marks']) if not m.get('fehlt') and i not in ohne_kreis]
    kreise(im, marks, f, s.get('y0', 0) if False else 0)
    gw, gh = sichern(im.copy(), id + '-ganz', 900 if not s['desk'] else 1600)
    info = {'url': s['url'], 'desk': s['desk'], 'ganz': [gw, gh], 'zeit': s['zeit'][:10]}
    if marks or nah:
        if nah: x0, y0, x1, y1 = nah
        else:
            y0 = min(m['y'] for m in marks) - 60; y1 = max(m['y'] + m['h'] for m in marks) + 60
            if s['desk']:
                x0 = min(m['x'] for m in marks) - 80; x1 = max(m['x'] + m['w'] for m in marks) + 80
                if x1 - x0 < 640: c = (x0 + x1) / 2; x0, x1 = c - 320, c + 320
            else: x0, x1 = 0, s['W']
        x0 = max(0, x0); y0 = max(0, y0); x1 = min(s['W'], x1); y1 = min(s['H'], y1)
        c = im.crop((round(x0 * f), round(y0 * f), round(x1 * f), round(y1 * f)))
        info['nah'] = list(sichern(c, id + '-nah', 1200))
    INFO[id] = info

AKTUELL = [x['id'] for x in json.load(open(H + '/stellen.json'))]
for id in AKTUELL + ['michelin-en']:
    if id in ('start-handy-1',): stelle(id); continue
    if id == 'plakette-handy': stelle(id, ohne_kreis=(1,)); continue
    if id == 'events-handy': stelle(id, nah=(0, 60, 390, 760)); continue
    if id == 'cookie-handy': stelle(id, nah=(0, 630, 390, 844)); continue
    stelle(id)

# Speisekarte am Telefon: Seite 1 so breit wie das Telefon (390 pt Breite), Zeile «Thon» eingekreist
pdf = H + '/pdf/Speisekarte-Oktober.pdf'
subprocess.run(['pdftoppm', '-r', '200', '-f', '1', '-l', '1', '-png', '-singlefile', pdf, H + '/_tmp'], check=True)
pg = Image.open(H + '/_tmp.png').convert('RGB'); os.remove(H + '/_tmp.png')
f = 3; s = 390 / 594.96
pg = pg.resize((390 * f, round(pg.height * 390 * f / pg.width)), Image.LANCZOS)
tel = Image.new('RGB', (390 * f, 844 * f), (82, 86, 89)); top = round(844 * f / 2 - pg.height / 2); tel.paste(pg, (0, top))
m = {'x': 46.2 * s, 'y': 133.2 * s + top / f, 'w': (380.6 - 46.2) * s, 'h': (160.2 - 133.2) * s}
kreise(tel, [m], f)
INFO['speisekarte-pdf'] = {'url': 'https://www.schloessli-bottighofen.ch/s/Speisekarte-Oktober.pdf', 'desk': False, 'ganz': list(sichern(tel.copy(), 'speisekarte-pdf-ganz', 900)), 'zeit': '2026-10-19'}
c = tel.crop((0, round((m['y'] - 40) * f), 390 * f, round((m['y'] + m['h'] + 60) * f)))
INFO['speisekarte-pdf']['nah'] = list(sichern(c, 'speisekarte-pdf-nah', 1200))
json.dump(INFO, open(H + '/belege.json', 'w'), indent=1)
print(len(INFO), 'Stellen:', ', '.join(INFO))
