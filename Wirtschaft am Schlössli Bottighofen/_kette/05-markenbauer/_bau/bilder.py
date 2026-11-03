"""Fotos für Farbkarten, Probe und Markenbuch: Ausschnitte aus den Originalen in _quelle/website/bilder, als webp. Nichts retuschiert."""
import os
from PIL import Image
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(H, '..', '..', '_quelle', 'website', 'bilder'); O = os.path.join(H, 'marke', 'bilder')
J = [  # name, datei, box (Original-Pixel) oder None, Breite
    ('terrasse-see', '8cc68d_32_-_FHF_2573.jpg', None, 2200),
    ('platanen', '178109_IMG_1967.jpeg', None, 1500),
    ('abend', '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', None, 1500),
    ('gaststube', '50fa79__DSC5718.JPG', None, 1800),
    ('bar', 'b49b5b_IMG_2226.jpeg', None, 900),
    ('tortelloni', '88d916_Tortelloni.jpg', None, 900),
    ('apero', '816543_2026-05-22_205034_Schl_C3_B6ssli_SM.jpg', None, 1300),
    ('wegweiser', 'a005f3_2026-05-22_193805_Schl_C3_B6ssli_SM.jpg', None, 1300),
    ('team', 'd51216_2_-_FHF_2646.jpg', None, 1800),
    ('fliesen', '7c2036_IMG_2037.jpeg', None, 2200),
    ('k-stuhl', '8cc68d_32_-_FHF_2573.jpg', (1262, 987, 1987, 1400), 900),
    ('k-see', '8cc68d_32_-_FHF_2573.jpg', (0, 420, 1375, 760), 1100),
    ('k-himmel', '8cc68d_32_-_FHF_2573.jpg', (0, 0, 1375, 520), 1100),
    ('k-ufer', '8cc68d_32_-_FHF_2573.jpg', (0, 900, 900, 1250), 900),
    ('k-laub', '178109_IMG_1967.jpeg', (300, 60, 1300, 900), 900),
    ('k-schirm', '178109_IMG_1967.jpeg', (1300, 1000, 2400, 1500), 900),
    ('k-kies', '178109_IMG_1967.jpeg', (1500, 2300, 2500, 3200), 900),
    ('k-abendrot', '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', (200, 1250, 2500, 1900), 1100),
    ('k-blau', '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', (1000, 800, 2400, 1400), 1000),
    ('k-licht', '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', (1500, 0, 2500, 900), 900),
    ('k-terrakotta', '7c2036_IMG_2037.jpeg', (325, 0, 800, 582), 600),
    ('k-graublau', '7c2036_IMG_2037.jpeg', (1450, 0, 1975, 582), 600),
    ('k-anthrazit', '7c2036_IMG_2037.jpeg', (2030, 0, 2500, 582), 600),
    ('k-kalk', '7c2036_IMG_2037.jpeg', (930, 0, 1420, 582), 600),
    ('k-teller', '7f6b93_Anguria.jpg', (0, 0, 2500, 1900), 900),
]
for n, f, box, w in J:
    im = Image.open(os.path.join(W, f)).convert('RGB')
    if box: im = im.crop(box)
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(O, n + '.webp'), quality=84); print(n, im.size)
