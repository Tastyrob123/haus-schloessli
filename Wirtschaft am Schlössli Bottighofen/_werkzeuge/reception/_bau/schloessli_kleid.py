#!/usr/bin/env python3
"""Kleid des Gastgebers fürs Schlössli (19.10.2026): rechnet die Farben der Kopie aus dem Ruedihus (Wandholz, Gold, Kerzenlicht) in die Farbwelt A
«Stuhl und See» um (marke.json, Station 5): warme Töne bekommen den Farbton der Terrassenstühle (Stuhlblau #116788, 197°), die Helligkeit bleibt,
helle Töne werden zum Seespiegel (wenig Farbe), mittlere zum Seehimmel. Grau, Grün (gut) und Rot (Marke «Entwurf») bleiben. Gelasio → Open Sans
(Titelschrift aus der Wortmarke), Butzenscheiben-Tapete → Punktraster mit Zeiger (assets/svg/tapete-a-dunkel.svg der Website).
Einmal angewendet am 19.10.2026 auf die Dateien unten; erneut nur auf frische Kopien aus dem Ruedihus (sonst wird doppelt umgerechnet)."""
import colorsys, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATEIEN = ['studio/studio.css', 'studio/hell.css', 'studio/schweben.css', 'reception.css', 'schloessli-gastgeber.css', 'gastgeber.css', 'brief-pdf.css',
           'brief-pdf.js', 'reception.js', 'studio/rundgang.js', 'studio/zur-werkbank.js', 'pruefung.html', 'anleitung.html', 'index.html', 'studio/buehne.js']
ZIEL_H = 197 / 360


def neu_rgb(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    warm = 12 / 360 <= h <= 62 / 360 and s > 0.06
    if not warm:
        return None
    if l > 0.85:
        s2 = min(s * 0.42, 0.42)
    elif l > 0.45:
        s2 = min(s * 0.62, 0.45)
    else:
        s2 = min(max(s, 0.55), 0.82)
    r2, g2, b2 = colorsys.hls_to_rgb(ZIEL_H, l, s2)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def hexe(m):
    t = m.group(1)
    if len(t) == 3:
        t = ''.join(c * 2 for c in t)
    x = neu_rgb(int(t[0:2], 16), int(t[2:4], 16), int(t[4:6], 16))
    return m.group(0) if x is None else '#%02x%02x%02x' % x


def rgba(m):
    x = neu_rgb(int(m.group(2)), int(m.group(3)), int(m.group(4)))
    return m.group(0) if x is None else f'{m.group(1)}({x[0]},{x[1]},{x[2]}{m.group(5)}'


def um(s):
    s = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F\w])', hexe, s)
    s = re.sub(r'(rgba?)\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(\s*[,)])', rgba, s)
    s = re.sub(r'%23([0-9a-fA-F]{6})', lambda m: '%23' + hexe(re.match(r'#(\w+)', '#' + m.group(1)))[1:], s)   # Farben in eingebetteten SVG
    s = s.replace('gelasio-700.woff2', 'OpenSans-var.woff2').replace('gelasio-400.woff2', 'OpenSans-var.woff2')
    s = s.replace("'Gelasio'", "'Open Sans'").replace('"Gelasio"', '"Open Sans"').replace('Gelasio,', "'Open Sans',")
    s = re.sub(r"url\((['\"]?)((?:\.\./)+)assets/img/butzen-09\.png\1\) 0 0/56px 56px", r"url(\1\2assets/svg/tapete-a-dunkel.svg\1) 0 0/168px 168px", s)
    return s


if __name__ == '__main__':
    for d in sys.argv[1:] or DATEIEN:
        p = os.path.join(C, d)
        alt = open(p, encoding='utf-8').read()
        neu = um(alt)
        open(p, 'w', encoding='utf-8').write(neu)
        print(d, 'geändert' if neu != alt else 'gleich')
