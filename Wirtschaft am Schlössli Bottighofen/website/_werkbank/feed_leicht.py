"""Feed der Werkbank leicht (Oberchef 18.10.2026, Regel M19, Robert 14:20 «es dauert sehr lange, bis es lädt»):
das Raster und die Highlights im Feed (feed/index.html) laden 400-px-WebP aus feed/thumbs-w/, die grossen Bilder erst beim Antippen eines Beitrags.
Läuft am Ende jedes Werkbank-Baus mit (haus.py) und allein: python3 _werkbank/feed_leicht.py"""
import glob, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'feed')


def mach():
    seite = os.path.join(F, 'index.html')
    if not os.path.exists(seite):
        return 0
    os.makedirs(os.path.join(F, 'thumbs-w'), exist_ok=True)
    for q in glob.glob(os.path.join(F, 'thumbs', '*.jpg')):
        z = os.path.join(F, 'thumbs-w', os.path.basename(q)[:-4] + '.webp')
        if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(q):
            im = Image.open(q).convert('RGB')
            if im.width > 400:
                im = im.resize((400, round(im.height * 400 / im.width)), Image.LANCZOS)
            im.save(z + '.neu', 'WEBP', quality=74, method=6)
            os.replace(z + '.neu', z)
    t = open(seite, encoding='utf-8').read()
    n = 0

    def um(m):
        nonlocal n
        name = m.group(1)
        if not os.path.exists(os.path.join(F, 'thumbs-w', name + '.webp')):
            return m.group(0)
        n += 1
        return f'src="thumbs-w/{name}.webp" decoding="async"'
    t2 = re.sub(r'src="thumbs/([A-Za-z0-9_-]+)\.jpg"', um, t)
    if t2 != t:
        open(seite, 'w', encoding='utf-8').write(t2)
    return n


if __name__ == '__main__':
    print('feed leicht:', mach(), 'Vorschaubilder umgestellt')
