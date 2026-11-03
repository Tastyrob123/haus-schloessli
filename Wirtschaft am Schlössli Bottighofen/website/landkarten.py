#!/usr/bin/env python3
"""Vier kleine Landkarten für den Kopf der Karte-Seite (Robert 19.10.2026, Fassung 16 aus _varianten/karte-kopf-15.html).
Feine Federlinie mit leichter Handunruhe, ein Hauch Blau dahinter, ein Punkt für die Stadt.
Umrisse: Natural Earth 1:110 Mio., gemeinfrei (_quelle/extern/geo/). Schreibt assets/svg/land-*.svg.
Aufruf: python3 landkarten.py"""
import json, math
from pathlib import Path
HIER = Path(__file__).parent
TOPO = json.loads((HIER.parent / '_quelle/extern/geo/countries-110m.json').read_text())
TINTE, HIMMEL = '#0A2552', '#A2B6CF'   # --titel-h und --himmel aus haus.css

KARTEN = [  # Datei, Ländercodes, Ausschnitt (Länge/Breite), Stadt, eigenes Haus
    ('frankreich', {'250'}, (-5.2, 42.2, 8.3, 51.2), (2.35, 48.86), False),
    ('italien', {'380'}, (6.6, 36.6, 18.6, 47.1), (12.50, 41.90), False),
    ('iberische-halbinsel', {'724', '620'}, (-9.6, 35.9, 3.4, 43.9), (-3.70, 40.42), False),
    ('klassiker', {'756'}, (5.9, 45.8, 10.5, 47.85), (9.21, 47.64), True),
]


def bogen(i):
    a = TOPO['arcs'][i if i >= 0 else ~i]
    sx, sy = TOPO['transform']['scale']; tx, ty = TOPO['transform']['translate']
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
    return pts if i >= 0 else pts[::-1]


def ringe(g):
    for poly in (g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]):
        for ring in poly:
            pts = []
            for i in ring:
                pts += bogen(i)
            yield pts


def karte(ids, box, stadt, heim, gr=140):
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; k = math.cos(math.radians(cy))
    f = gr * .78 / max((x1 - x0) * k, y1 - y0)
    P = lambda lo, la: (gr / 2 + (lo - cx) * k * f, gr / 2 - (la - cy) * f)
    d = ''.join('M' + 'L'.join('%.1f %.1f' % P(*q) for q in r) + 'Z'
                for g in TOPO['objects']['countries']['geometries'] if g.get('id') in ids for r in ringe(g))
    px, py = P(*stadt)
    ring = f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="none" stroke="{TINTE}" stroke-width=".6" stroke-opacity=".45"/>' if heim else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {gr} {gr}" width="{gr}" height="{gr}">
<filter id="w" x="-40%" y="-40%" width="180%" height="180%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="2" result="n"/><feMorphology in="SourceGraphic" operator="dilate" radius="12" result="d"/><feDisplacementMap in="d" in2="n" scale="34" result="v"/><feGaussianBlur in="v" stdDeviation="11"/></filter>
<filter id="h"><feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="3" seed="4"/><feDisplacementMap in="SourceGraphic" scale="2.2"/></filter>
<path d="{d}" fill="{HIMMEL}" fill-opacity=".1" filter="url(#w)" transform="translate(6 7)"/>
<path d="{d}" fill="none" stroke="{TINTE}" stroke-width=".8" stroke-opacity=".55" stroke-linejoin="round" filter="url(#h)"/>
<circle cx="{px:.1f}" cy="{py:.1f}" r="{1.8 if heim else 1.6}" fill="{TINTE}" fill-opacity=".6"/>{ring}
</svg>
'''


if __name__ == '__main__':
    for name, ids, box, stadt, heim in KARTEN:
        (HIER / f'assets/svg/land-{name}.svg').write_text(karte(ids, box, stadt, heim))
    print('ok', len(KARTEN))
