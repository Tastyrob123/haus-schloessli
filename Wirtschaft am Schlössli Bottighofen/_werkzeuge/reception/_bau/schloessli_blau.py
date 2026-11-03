#!/usr/bin/env python3
"""Zweiter Farbschritt (20.10.2026): Die Website des Schlössli wurde am 19.10. abends auf «Ton in Ton» gedreht (Blau des Platztellers,
website/assets/css/haus.css, gemeinsames Kleid _werkzeuge/oberflaeche/kleid/schloessli.css: #0b1d3d · #0A234C · #113d88 · #A2B6CF · #E7ECF3).
Robert 20.10.: «warum ist unten … eine andere Farbe als oben?» Alle Petrol-Töne (Farbton 180–208°) bekommen den Farbton des Kleids, Helligkeit und Sättigung bleiben."""
import colorsys, os, re, sys
C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATEIEN = ['studio/studio.css', 'studio/hell.css', 'studio/schweben.css', 'reception.css', 'schloessli-gastgeber.css', 'gastgeber.css', 'brief-pdf.css', 'brief-pdf.js',
           'reception.js', 'studio/rundgang.js', 'studio/zur-werkbank.js', 'studio/auswahl.js', 'pruefung.html', 'anleitung.html', 'index.html', 'zeichen-haus.svg']
r_, g_, b_ = 0x11 / 255, 0x3d / 255, 0x88 / 255
ZIEL = colorsys.rgb_to_hls(r_, g_, b_)[0]
def neu(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if not (180 / 360 <= h <= 208 / 360 and s > 0.06):
        return None
    x = colorsys.hls_to_rgb(ZIEL, l, s); return tuple(round(v * 255) for v in x)
def hx(m):
    t = m.group(1); t = ''.join(c * 2 for c in t) if len(t) == 3 else t
    x = neu(int(t[:2], 16), int(t[2:4], 16), int(t[4:], 16)); return m.group(0) if x is None else '#%02x%02x%02x' % x
def rgba(m):
    x = neu(int(m.group(2)), int(m.group(3)), int(m.group(4))); return m.group(0) if x is None else f'{m.group(1)}({x[0]},{x[1]},{x[2]}{m.group(5)}'
for d in sys.argv[1:] or DATEIEN:
    p = os.path.join(C, d); s = open(p, encoding='utf-8').read()
    s2 = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F\w])', hx, s)
    s2 = re.sub(r'(rgba?)\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(\s*[,)])', rgba, s2)
    s2 = re.sub(r'%23([0-9a-fA-F]{6})', lambda m: '%23' + hx(re.match(r'#(\w+)', '#' + m.group(1)))[1:], s2)
    open(p, 'w', encoding='utf-8').write(s2); print(d, 'geändert' if s2 != s else 'gleich')
