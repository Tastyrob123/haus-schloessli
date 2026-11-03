# Leinen für den Tischläufer im Auftakt «Am Tisch» (Robert 19.10.2026, Fläche 14 aus _varianten/hintergrund-15.html).
# Lokal gerechnet, kein Foto: Kett- und Schussfäden als feines, nahtlos kachelndes Gewebe auf Naturton.
# Lauf: python3 leinen.py  →  assets/img/leinen.webp (Kachel 480 px)
import pathlib, random
from PIL import Image, ImageFilter

HIER = pathlib.Path(__file__).resolve().parent
ZIEL = HIER / 'assets' / 'img' / 'leinen.webp'
N = 480
GRUND = (230, 225, 214)


def faeden(n, dicke, streu):
    """Helligkeit je Faden, zyklisch, damit die Kachel ohne Naht anschliesst."""
    random.seed(7 + dicke)
    return [random.uniform(-streu, streu) for _ in range(n // dicke)]


def main():
    im = Image.new('RGB', (N, N), GRUND)
    px = im.load()
    kette, schuss = faeden(N, 3, 9), faeden(N, 3, 7)
    random.seed(11)
    knoten = {(random.randrange(N), random.randrange(N)): random.uniform(-14, 6) for _ in range(900)}
    for y in range(N):
        for x in range(N):
            v = kette[x // 3] * (0.6 if (x + y) % 2 else 1) + schuss[y // 3] * (1 if (x + y) % 2 else 0.6)
            v += knoten.get((x, y), 0)
            px[x, y] = tuple(max(0, min(255, int(c + v))) for c in GRUND)
    im = im.filter(ImageFilter.GaussianBlur(0.35))
    im.save(ZIEL, 'WEBP', quality=88, method=6)
    print(ZIEL, ZIEL.stat().st_size // 1024, 'KB')


if __name__ == '__main__':
    main()
