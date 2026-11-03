"""Zeichen der Wirtschaft am Schlössli als Vektor: aus dem transparenten Logo (1563 × 1563, Seite des Schäfli) die Schrift-Teile
weggelassen (zusammenhängende Flächen der Buchstaben), Rest mit potrace gezogen. Nichts nachgezeichnet, nichts verschoben."""
import os, re, subprocess, numpy as np, cv2
from PIL import Image
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(H, '..', '..', '_quelle', 'extern', 'logo', 'schloessli-logo-transparent.png')
OUT = os.path.join(H, 'marke', 'zeichen'); T = os.path.join(H, '_bau', 'tmp'); os.makedirs(T, exist_ok=True)
a = np.array(Image.open(Q).convert('RGBA'))[:, :, 3]
m = (a > 128).astype(np.uint8)
n, cc, st, _ = cv2.connectedComponentsWithStats(m, 8)
def ist_schrift(i):
    x, y, w, h, ar = st[i]
    if 860 <= y <= 870 and h < 110: return True              # SCHL SSLI
    if 840 <= y <= 850 and h < 20: return True               # Umlaut-Punkte
    if 1008 <= y <= 1013 and h < 55: return True             # WIRTSCHAFT
    if 1100 <= y <= 1104 and h < 25: return True             # BY CHRISTIAN KUCHLER
    return False
schrift = np.zeros_like(m, bool); zeichen = np.zeros_like(m, bool)
for i in range(1, n):
    (schrift if ist_schrift(i) else zeichen)[cc == i] = True
# Zeiger allein: die grösste Fläche (Nabe, Schäfte, zwei Rauten, Kugeln)
zeiger = cc == (1 + int(np.argmax(st[1:, 4])))
print('Schrift-Flächen', int(sum(ist_schrift(i) for i in range(1, n))), 'Pixel Zeichen', int(zeichen.sum()))
def trace(mask, name):
    p = os.path.join(T, name + '.pbm'); Image.fromarray(((~mask) * 255).astype(np.uint8)).convert('1').save(p)
    s = os.path.join(T, name + '.svg'); subprocess.run(['potrace', p, '-s', '-o', s, '-t', '4', '-a', '1.0', '--flat'], check=True)
    t = open(s).read(); g = re.search(r'<g transform="([^"]+)"[^>]*>(.*?)</g>', t, re.S)
    return g.group(1), re.sub(r'\s+', ' ', g.group(2)).strip()
def schreib(mask, name, pad=14):
    tr, pf = trace(mask, name); ys, xs = np.where(mask)
    vb = '%d %d %d %d' % (xs.min() - pad, ys.min() - pad, xs.max() - xs.min() + 2 * pad, ys.max() - ys.min() + 2 * pad)
    open(os.path.join(OUT, name + '.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" fill="currentColor"><g transform="%s">%s</g></svg>\n' % (vb, tr, pf))
    print(name, vb)
schreib(zeichen, 'zeichen')
schreib(zeiger, 'zeiger')
# Prüfbild: Zeichen + Schrift = Original?
chk = np.zeros(m.shape + (3,), np.uint8) + 255; chk[zeichen] = (20, 20, 20); chk[schrift] = (200, 60, 40)
Image.fromarray(chk).resize((780, 780)).save(os.path.join(T, 'pruef-trennung.png'))
