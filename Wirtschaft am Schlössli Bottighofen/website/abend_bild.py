# Fenster «Wenn es Abend wird am Hafen.» (Robert 19.10.2026: Bild 4 aus _varianten/fenster-abend-2, «noch ein bisschen mehr Schatten, dass man den Text besser lesen kann»).
# Freies Foto von Wikimedia Commons (Gottlieben am Seerhein, JoachimKohler-HB, CC BY-SA 4.0). Lokal, ohne KI: weiche Abdunklung zur Bildmitte,
# wo der Satz steht, und etwas Gesamtabdunklung. Die Schattierung liegt im Bild selbst, nichts Zusätzliches über der Fläche (Regel 55). Original bleibt unangetastet.
# Lauf: python3 abend_bild.py  →  _quelle/website/bearbeitet/abend-gottlieben.jpg  (danach bilder.py und bau.py)
import pathlib
from PIL import Image, ImageOps, ImageEnhance

HIER = pathlib.Path(__file__).resolve().parent
Q = HIER.parent / '_quelle'
QUELLE = Q / 'extern/wikipedia-commons/abend/04-gottlieben.jpg'
ZIEL = Q / 'website/bearbeitet/abend-gottlieben.jpg'

im = ImageOps.exif_transpose(Image.open(QUELLE)).convert('RGB')
im = ImageEnhance.Brightness(im).enhance(.86)
w, h = im.size
# Maske: in der Mitte am dunkelsten (52 %), weich nach aussen auslaufend
k = Image.new('L', (64, 64))
px = k.load()
for y in range(64):
    for x in range(64):
        d = (((x - 31.5) / 34) ** 2 + ((y - 31.5) / 26) ** 2) ** .5
        px[x, y] = int(255 * .52 * max(0, 1 - d) ** 1.6)
maske = k.resize((w, h), Image.BICUBIC)
im = Image.composite(Image.new('RGB', (w, h), (3, 11, 24)), im, maske)
ZIEL.parent.mkdir(parents=True, exist_ok=True)
im.save(ZIEL, quality=92)
print(ZIEL, im.size)
