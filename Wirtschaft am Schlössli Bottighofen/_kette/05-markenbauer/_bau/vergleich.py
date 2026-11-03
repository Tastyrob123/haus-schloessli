"""Wortmarke gegen Open Sans 400: Sperrung so gesucht, dass das Seitenverhältnis von «WIRTSCHAFT» und «SCHL…SSLI» dem Logo entspricht; Bild für das Markenbuch."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
L = '../../../_quelle/extern/logo/schloessli-logo-transparent.png'
F = '/private/tmp/claude-501/-Users-robertreff-SecondBrain/cf9f40a9-97d1-437c-a432-a810d6055ffe/scratchpad/f/OpenSans[wdth,wght].ttf'
a = np.array(Image.open(L).convert('RGBA'))[:, :, 3]
def zeile(y0, y1, x0, x1):
    m = a[y0:y1, x0:x1] > 110; ys, xs = np.where(m)
    return Image.fromarray((255 - a[y0:y1, x0:x1]).astype(np.uint8)).crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
f = ImageFont.truetype(F, 400); f.set_variation_by_axes([400, 100])
def setz(t, tr):
    img = Image.new('L', (7000, 700), 255); d = ImageDraw.Draw(img); x = 40
    for c in t: d.text((x, 100), c, font=f, fill=0); x += f.getlength(c) + tr * 400
    m = np.array(img) < 128; ys, xs = np.where(m); return img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
wm = zeile(1005, 1065, 850, 1400)
best = min(((abs(setz('WIRTSCHAFT', tr).width / setz('WIRTSCHAFT', tr).height - wm.width / wm.height), tr) for tr in np.arange(.15, .35, .005)))
tr = best[1]; print('Sperrung WIRTSCHAFT %.3f em' % tr)
os_ = setz('WIRTSCHAFT', tr)
W = 1600; wm2 = wm.resize((W, round(wm.height * W / wm.width)), Image.LANCZOS); os2 = os_.resize((W, wm2.height), Image.LANCZOS)
iou = ((np.array(wm2) < 128) & (np.array(os2) < 128)).sum() / ((np.array(wm2) < 128) | (np.array(os2) < 128)).sum()
print('Deckung ganze Zeile %.3f' % iou)
c = Image.new('L', (W + 160, wm2.height * 2 + 200), 255); c.paste(wm2, (80, 60)); c.paste(os2, (80, wm2.height + 140))
c.convert('RGB').save('../marke/bilder/vergleich-wortmarke.png', optimize=True)

# Ausschnitt der Schrift aus dem Original (nur zugeschnitten, Alpha bleibt)
o = Image.open(L).convert('RGBA'); o.crop((300, 830, 1400, 1140)).save('../marke/bilder/wortmarke-ausschnitt.png', optimize=True)
