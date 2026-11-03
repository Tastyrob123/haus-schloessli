# Leder für die Fläche des Auftakts «Am Tisch» (Robert 19.10.2026: «den Hintergrund genauso ledrig wie auf dem Tellerbild, und in der Farbe»).
# Aus dem echten Platzteller im nachgeschärften Tellerfoto geschnitten (Ecke oben links, ausserhalb des Tellers), Licht geglättet,
# nahtlos gemacht. Zweite Kachel = dieselbe Narbung gedreht, als Struktur darüber in anderer Grösse, damit sich nichts sichtbar wiederholt.
# Lauf: python3 leder.py  →  assets/img/leder.webp, leder-narbe.webp, leder-nacht.webp (in Gebrauch)
import pathlib
import numpy as np
from PIL import Image, ImageFilter

HIER = pathlib.Path(__file__).resolve().parent
QUELLE = HIER.parent / '_quelle/website/bearbeitet/teller-anguria-ki.png'
AUS = HIER / 'assets' / 'img'
X, Y, N, B = 120, 120, 600, 100   # Ausschnitt im 4096er Bild: N Kachel + B Überlappung (am Bild geprüft 19.10.2026: reines Leder)


def nahtlos(p):
    w = np.linspace(0, 1, B)[None, :, None]
    t = p[:, :N].copy(); t[:, :B] = p[:, N:N + B] * (1 - w) + p[:, :B] * w
    w = np.linspace(0, 1, B)[:, None, None]
    u = t[:N].copy(); u[:B] = t[N:N + B] * (1 - w) + t[:B] * w
    return u


def main():
    im = Image.open(QUELLE).convert('RGB').crop((X, Y, X + N + B, Y + N + B))
    a = np.asarray(im).astype(float)
    licht = np.asarray(im.filter(ImageFilter.GaussianBlur(40))).astype(float)
    farbe = a.reshape(-1, 3).mean(0)                      # Ton des Platztellers an dieser Stelle
    flach = a / np.maximum(licht, 1) * farbe               # Narbung bleibt, Lichtverlauf geht
    t = nahtlos(flach)
    Image.fromarray(np.clip(t, 0, 255).astype('uint8')).save(AUS / 'leder.webp', 'WEBP', quality=86, method=6)
    g = t.mean(2); g = (g - g.mean()) * 1.0 + 128           # reine Narbung um Mittelgrau, für «soft-light»
    Image.fromarray(np.clip(np.rot90(g), 0, 255).astype('uint8')).save(AUS / 'leder-narbe.webp', 'WEBP', quality=86, method=6)
    # Robert 19.10.2026 «Farbe wieder wie vorher»: dieselbe Narbung im Nachtblau der Seite (--nacht #062531)
    nacht = np.array([6, 37, 49], float)
    d = t / farbe * nacht + (t - farbe) * 0.12            # Ton auf Nachtblau, Narbung etwas kräftiger, damit sie im Dunkeln sichtbar bleibt
    Image.fromarray(np.clip(d, 0, 255).astype('uint8')).save(AUS / 'leder-nacht.webp', 'WEBP', quality=86, method=6)
    # Robert 19.10.2026 «02 Ton in Ton»: Grund im dunklen Blau des Platztellers (#0b1d3d, Farbton 218°, am Tellerbild gemessen)
    ton = np.array([11, 29, 61], float)
    d = t / farbe * ton + (t - farbe) * 0.12
    Image.fromarray(np.clip(d, 0, 255).astype('uint8')).save(AUS / 'leder-ton.webp', 'WEBP', quality=86, method=6)
    print('Ton', farbe.round(1), 'Kachel', N)


if __name__ == '__main__':
    main()
