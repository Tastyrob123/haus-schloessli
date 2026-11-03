# Teller für den Auftakt «Am Tisch» (Robert 19.10.2026: «so bearbeiten, dass es aussieht wie professionelle Fotografie, es wirkt unscharf»).
# Lokal, ohne KI: quadratischer Ausschnitt mit dem Teller genau in der Mitte (damit Teller, Platzteller und Schriftring dieselbe Mitte haben),
# Klarheit (grobe Unschärfemaske), Feinzeichnung (feine Unschärfemaske), etwas Kontrast. Original bleibt unangetastet.
# Seit 19.10.2026 (Roberts Ja, 2 Credits): liegt die KI-Fassung vor (teller-anguria-ki.png, Higgsfield «bytedance_image_upscale» 4K
# aus teller-anguria-roh.jpg = derselbe Ausschnitt ohne Bearbeitung), wird sie genommen und nur leicht im Kontrast angehoben.
# Lauf: python3 teller_bild.py  →  _quelle/website/bearbeitet/teller-anguria.jpg  (danach bilder.py und bau.py)
import pathlib
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

HIER = pathlib.Path(__file__).resolve().parent
Q = HIER.parent / '_quelle'
QUELLE = Q / 'website/bilder/7f6b93_Anguria.jpg'
ZIEL = Q / 'website/bearbeitet/teller-anguria.jpg'
MITTE = (1236, 1706)   # Tellermitte im Original (2500 × 3333), am Bild gemessen 19.10.2026
HALB = 1236            # grösster Ausschnitt um diese Mitte, der noch ins Bild passt


KI = Q / 'website/bearbeitet/teller-anguria-ki.png'


def main():
    if KI.exists():
        im = ImageEnhance.Contrast(Image.open(KI).convert('RGB')).enhance(1.03)
        ZIEL.parent.mkdir(parents=True, exist_ok=True)
        im.save(ZIEL, 'JPEG', quality=95, subsampling=0)
        print(ZIEL, im.size, 'aus KI-Fassung')
        return
    im = ImageOps.exif_transpose(Image.open(QUELLE)).convert('RGB')
    x, y = MITTE
    im = im.crop((x - HALB, y - HALB, x + HALB, y + HALB))
    im = im.filter(ImageFilter.UnsharpMask(radius=14, percent=22, threshold=2))   # Klarheit
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=95, threshold=3))  # Feinzeichnung
    im = ImageEnhance.Contrast(im).enhance(1.05)
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    im.save(ZIEL, 'JPEG', quality=95, subsampling=0)
    print(ZIEL, im.size)


if __name__ == '__main__':
    main()
