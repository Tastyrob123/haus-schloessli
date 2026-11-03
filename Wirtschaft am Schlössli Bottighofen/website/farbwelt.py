# Farbwelt «Ton in Ton» für die ganze Seite (Robert 19.10.2026: «die restliche Seite auch anpassen», nach Fassung 02 im Auftakt).
# Regel: Alle Blau- und Petroltöne der bisherigen Farbwelt «Stuhl und See» (Farbton 185–212°) werden um denselben Winkel auf den Farbton
# des Platztellers gedreht (Petrol 197° → Platzteller 218°, also +21°). Helligkeit und Sättigung bleiben, damit alle Abstufungen,
# Kontraste und Schatten zueinander stimmen. Warme Töne (Papier, Sand, Hausorange) bleiben unberührt. --nacht wird genau #0b1d3d.
# Lauf: python3 farbwelt.py [--probe]   (vorher Sicherung in _sicherung/vor-farbwelt-ton-in-ton/)
import colorsys, pathlib, re, shutil, sys, time

HIER = pathlib.Path(__file__).resolve().parent
DATEIEN = ['assets/css/haus.css', 'assets/css/funktionen.css', 'assets/svg/tapete-a-dunkel.svg', 'assets/svg/tapete-a-hell.svg', 'bau.py']
VON, BIS, DREH = 185, 212, 21
FEST = {'062531': '0b1d3d'}   # Grund der Seite = dunkles Blau des Platztellers, am Tellerbild gemessen


def drehe(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if s < .06 or not (VON <= h * 360 <= BIS):
        return None
    r2, g2, b2 = colorsys.hls_to_rgb(((h * 360 + DREH) % 360) / 360, l, s)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def hex_neu(m):
    t = m.group(1)
    if len(t) == 3:
        t = ''.join(c * 2 for c in t)
    if t.lower() in FEST:
        n = FEST[t.lower()]
    else:
        d = drehe(*(int(t[i:i + 2], 16) for i in (0, 2, 4)))
        if not d:
            return m.group(0)
        n = '%02x%02x%02x' % d
    return '#' + (n.upper() if m.group(1).isupper() else n)


def rgba_neu(m):
    r, g, b = int(m.group(2)), int(m.group(3)), int(m.group(4))
    d = drehe(r, g, b)
    if not d:
        return m.group(0)
    return f'{m.group(1)}({d[0]},{d[1]},{d[2]}{m.group(5)}'


def main():
    probe = '--probe' in sys.argv
    if not probe:
        z = HIER / '_sicherung' / f'vor-farbwelt-ton-in-ton-{time.strftime("%H%M%S")}'
        z.mkdir(parents=True, exist_ok=True)
    for f in DATEIEN:
        p = HIER / f
        alt = p.read_text()
        neu = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', hex_neu, alt)
        neu = re.sub(r'(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(\s*[,)])', rgba_neu, neu)
        n = sum(1 for a, b in zip(re.findall(r'#[0-9a-fA-F]{3,6}|rgba?\([^)]*\)', alt), re.findall(r'#[0-9a-fA-F]{3,6}|rgba?\([^)]*\)', neu)) if a != b)
        print(f, n, 'Farben gedreht')
        if not probe and neu != alt:
            shutil.copy2(p, z / p.name)
            p.write_text(neu)


if __name__ == '__main__':
    main()
