#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli: letzter Farbgang (Nachtbau 3.11.2026; Bauart wie sb_farbe.py des Culinarium und des alten Schlössli-Stands vom 19.10.).
Die Bausteine kommen aus den Werkbänken des Culinarium (Nacht-Violett, Kerze, Warmweiss), des Schäfli und des Ruedihus (Gold, Holz). Jede dieser Farben,
die noch in den gebauten Seiten steht, wird auf die Töne der Schlössli-Seite umgerechnet (website/assets/css/haus.css :root, «Stuhl und See»):
dunkel wird Nacht über dem See und Stuhlblau, die Mitte Seehimmel, hell wird Papier und Seespiegel. Das Schirmrot (#FD9964) bleibt, nur als Punkt.
Fotos werden nicht angefasst, nur Text in CSS und HTML. Mehrfach anwendbar (Blau bleibt Blau)."""
import colorsys, glob, os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
FEST = {   # Akzente der Vorlagen in die Rolle, die sie dort hatten (Kerze = was leuchtet → Seehimmel auf Dunkel, Seehimmel tief auf Hell)
    '#ef7649': '#a2b6cf', '#f5a689': '#c5d2e1', '#b15736': '#0f3678', '#c98543': '#a2b6cf', '#dcc68f': '#c5d2e1', '#b78f51': '#a2b6cf', '#c9a05c': '#a2b6cf',
    '#16151a': '#0b1d3d', '#0f0e13': '#081631', '#1c1b21': '#0a234c', '#222028': '#0a234c', '#26252e': '#0f2a57', '#3a3845': '#113d88', '#5b5763': '#5e6f86',
    '#26242d': '#041023', '#faf4f4': '#f4f6f9', '#f2eaea': '#e7ecf3', '#fffbfa': '#fbfcfe', '#fbf5ea': '#f4f6f9', '#8953a9': '#0f3678',
    '#c42e13': '#fd9964', '#a8260f': '#fd9964', '#e0a96a': '#a2b6cf', '#e8875a': '#fd9964', '#fec7aa': '#c5d2e1', '#7d433a': '#113d88',
    '#e6007e': '#e6007e', '#fd9964': '#fd9964'}   # Magenta ist die Schnittlinie im Druckbogen
BLEIBT = {(0xfd, 0x99, 0x64), (0xe6, 0x00, 0x7e)}


def _blau(r, g, b):
    if (r, g, b) in BLEIBT:
        return r, g, b
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    grad = h * 360
    if s < .06 or l > .985 or l < .02 or 196 <= grad <= 234:   # Grau, fast Weiss, fast Schwarz und Blau bleiben
        return r, g, b
    nh = 218 / 360
    if l < .3:
        ns = .66
    elif l < .62:
        ns = .55
    elif l < .86:
        ns = .3
    else:
        ns = .3
    nr, ng, nb = colorsys.hls_to_rgb(nh, l, ns)
    return round(nr * 255), round(ng * 255), round(nb * 255)


def faerbe(t):
    def hexf(m):
        x = m.group(1)
        if len(x) == 3:
            x = ''.join(c * 2 for c in x)
        if len(x) != 6:
            return m.group(0)
        k = '#' + x.lower()
        if k in FEST:
            return FEST[k]
        return '#%02x%02x%02x' % _blau(*(int(x[i:i + 2], 16) for i in (0, 2, 4)))
    t = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![0-9a-fA-F-])', hexf, t)
    t = re.sub(r'(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', lambda m: '%s(%d,%d,%d' % ((m.group(1),) + _ersetze_rgb(int(m.group(2)), int(m.group(3)), int(m.group(4)))), t)
    return t


def _ersetze_rgb(r, g, b):
    k = '#%02x%02x%02x' % (r, g, b)
    if k in FEST:
        v = FEST[k]
        return int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16)
    return _blau(r, g, b)


def nur_style(t):
    """In HTML nur <style>-Blöcke und style=""-Werte umrechnen, nie Text, Adressen oder eingebettete Bilder."""
    t = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + faerbe(m.group(2)) + m.group(3), t, flags=re.S)
    t = re.sub(r'(style=")([^"]*)(")', lambda m: m.group(1) + faerbe(m.group(2)) + m.group(3), t)
    t = re.sub(r'(<meta name="theme-color" content=")(#[0-9a-fA-F]{6})', lambda m: m.group(1) + faerbe(m.group(2)), t)
    t = re.sub(r'(<svg\b.*?</svg>)', lambda m: faerbe(m.group(1)) if 'data:image' not in m.group(1) else m.group(1), t, flags=re.S)
    return t


def ohne_fett(t):
    """Nie fett (Tasty-Sprache Stufe 2 Nr. 8): kräftige Schnitte werden Medium, Titel bleiben Regular."""
    t = re.sub(r'font-weight:\s*(?:600|700|800|900|bold)\b', 'font-weight:500', t)
    return re.sub(r'(font:\s*)(?:600|700|800|900|bold)\b', r'\g<1>500', t)


def anwenden():
    n = 0
    for p in glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.css'), recursive=True) + glob.glob(os.path.join(ROOT, 'befund', '**', '*.css'), recursive=True):
        a = open(p, encoding='utf-8').read(); b = ohne_fett(faerbe(a))
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    seiten = (glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.html'), recursive=True) + [os.path.join(ROOT, 'befund', 'index.html')])   # nur das eigene Revier (Kern)
    for p in seiten:
        if not os.path.exists(p):
            continue
        a = open(p, encoding='utf-8').read(); b = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + ohne_fett(m.group(2)) + m.group(3), nur_style(a), flags=re.S)
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    return n


if __name__ == '__main__':
    print('umgefärbt:', anwenden(), 'Dateien')
