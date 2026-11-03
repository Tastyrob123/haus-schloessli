"""Farben der Wirtschaft am Schlössli: häufigster Ton einer Fläche (Mode nach Quantisierung, dann Mittel der Pixel im Mode-Fach).
Zwei unabhängige Rechnungen je Farbe: Mode (Fach 6) und Median der gefilterten Pixel. Ausgabe: messung.json."""
import os, json, colorsys, numpy as np
from PIL import Image
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(H, '..', '..', '_quelle', 'website', 'bilder')
def hsv(p):
    a = p / 255.0; mx = a.max(1); mn = a.min(1); s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r, g, b = a[:, 0], a[:, 1], a[:, 2]; d = np.maximum(mx - mn, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, s, mx
FILTER = {
    'blau': lambda h, s, v: (h > 190) & (h < 225) & (s > .35) & (v > .5),
    'licht': lambda h, s, v: (v > .45),
    'rinde': lambda h, s, v: (v > .35) & (s < .45),
    'gruen': lambda h, s, v: (h > 65) & (h < 140) & (s > .3) & (v > .45),
    'kalk': lambda h, s, v: (v > .78) & (s < .14),
    'mint': lambda h, s, v: (v > .9) & (s > .05) & (h > 160) & (h < 190),
    'terra2': lambda h, s, v: (h > 5) & (h < 35) & (s > .35) & (v > .55),
    'orange': lambda h, s, v: ((h < 25) | (h > 345)) & (s > .55) & (v > .45),
    'braun': lambda h, s, v: (h > 15) & (h < 50) & (s > .15) & (v > .2),
    'hell': lambda h, s, v: (v > .55) & (s < .35),
    'alle': lambda h, s, v: np.ones_like(h, bool),
    'gold': lambda h, s, v: (h > 30) & (h < 55) & (s > .5) & (v > .8),
    'abendrot': lambda h, s, v: (h > 15) & (h < 45) & (s > .35) & (v > .5),
    'nachtblau': lambda h, s, v: (h > 200) & (h < 235) & (s > .4),
    'graublau': lambda h, s, v: (h > 180) & (h < 230) & (s > .08) & (s < .4) & (v > .5),
    'terrakotta': lambda h, s, v: (h > 5) & (h < 35) & (s > .35) & (v > .35) & (v < .85),
    'dunkel': lambda h, s, v: (v < .3),
}
M = [  # name, datei, box (Original-Pixel), filter
    ('Stuhlblau', '8cc68d_32_-_FHF_2573.jpg', (1262, 987, 1987, 1400), 'blau'),
    ('Seespiegel', '8cc68d_32_-_FHF_2573.jpg', (0, 525, 1375, 675), 'alle'),
    ('Seehimmel', '8cc68d_32_-_FHF_2573.jpg', (0, 50, 1375, 400), 'alle'),
    ('Ufersand', '8cc68d_32_-_FHF_2573.jpg', (0, 950, 850, 1175), 'alle'),
    ('Platanenlaub', '178109_IMG_1967.jpeg', (333, 100, 1266, 866), 'gruen'),
    ('Schirmrot', '178109_IMG_1967.jpeg', (1466, 1166, 2333, 1283), 'orange'),
    ('Kies', '178109_IMG_1967.jpeg', (1600, 2333, 2500, 3333), 'licht'),
    ('Abendrot', '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', (333, 1560, 2333, 1640), 'abendrot'),
    ('Blaue Stunde', '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', (1266, 1000, 2333, 1266), 'nachtblau'),
    ('Lichterkette', '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', (1800, 0, 2500, 830), 'gold'),
    ('Fliese Terrakotta', '7c2036_IMG_2037.jpeg', (325, 0, 800, 582), 'terra2'),
    ('Fliese Graublau', '7c2036_IMG_2037.jpeg', (1450, 0, 1975, 582), 'graublau'),
    ('Fliese Anthrazit', '7c2036_IMG_2037.jpeg', (0, 0, 2500, 582), 'dunkel'),
    ('Fliese Kalk', '7c2036_IMG_2037.jpeg', (0, 0, 2500, 582), 'kalk'),
    ('Mint der heutigen Seite', 'afd0fc_2b500a48-0faf-4743-ad9a-ccd5e7c54e6d.jpeg', (0, 0, 1144, 120), 'alle'),
    ('Tellerblau', '7f6b93_Anguria.jpg', (0, 0, 2500, 600), 'alle'),
]
out = {}
for n, f, box, flt in M:
    im = Image.open(os.path.join(Q, f)).convert('RGB').crop(box)
    p = np.array(im).reshape(-1, 3).astype(float)
    h, s, v = hsv(p); p = p[FILTER[flt](h, s, v)]
    q = (p // 12).astype(int); key = q[:, 0] * 10000 + q[:, 1] * 100 + q[:, 2]
    u, c = np.unique(key, return_counts=True); m = u[np.argmax(c)]
    mode = p[key == m].mean(0); med = np.median(p, 0)
    hx = lambda c: '#%02X%02X%02X' % tuple(int(round(x)) for x in c)
    dist = np.abs(mode - med).max()
    out[n] = dict(hex=hx(mode), median=hx(med), abstand=int(dist), pixel=int(len(p)), datei='_quelle/website/bilder/' + f, box=box, filter=flt)
    print('%-18s mode %s  median %s  d=%3d  n=%d' % (n, hx(mode), hx(med), dist, len(p)))
json.dump(out, open(os.path.join(H, '_bau', 'messung.json'), 'w'), ensure_ascii=False, indent=1)

# Sichtprobe: Ausschnitt neben gemessenem Ton
from PIL import ImageDraw
tiles=[]
for n,f,box,flt in M:
    im=Image.open(os.path.join(Q,f)).convert('RGB').crop(box);im.thumbnail((260,160))
    t=Image.new('RGB',(560,180),'white');t.paste(im,(0,0));d=ImageDraw.Draw(t)
    d.rectangle([270,0,400,160],fill=out[n]['hex']);d.rectangle([410,0,540,160],fill=out[n]['median']);d.text((270,164),n+' '+out[n]['hex'],fill='black');tiles.append(t)
sheet=Image.new('RGB',(1120,180*((len(tiles)+1)//2)),'white')
for i,t in enumerate(tiles): sheet.paste(t,((i%2)*560,(i//2)*180))
sheet.save('/private/tmp/claude-501/-Users-robertreff-SecondBrain/cf9f40a9-97d1-437c-a432-a810d6055ffe/scratchpad/v/mess.jpg',quality=80)
