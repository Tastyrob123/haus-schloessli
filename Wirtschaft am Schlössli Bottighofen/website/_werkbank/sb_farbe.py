#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli: letzter Farbgang (19.10.2026). Die Bausteine kommen aus der Werkbank des Ruedihus (Wandholz, Kerzenlicht, Gold).
Hier wird jede warme Farbe, die noch in den gebauten Seiten steht, auf die Töne der Schlössli-Seite umgerechnet (assets/css/haus.css :root):
Helligkeit bleibt, der Ton wird das Blau der Stühle und des Sees, hell wird Kalk und Papier. Das Rot der Geranien wird das Rot der Schirme.
Fotos werden nicht angefasst, nur Text in CSS und HTML. Mehrfach anwendbar (Blau bleibt Blau)."""
import colorsys, glob, os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
FEST = {'#c42e13': '#fd9964', '#a8260f': '#e8875a', '#e0a96a': '#fd9964', '#e6007e': '#e6007e', '#fd9964': '#fd9964', '#e8875a': '#e8875a', '#fec7aa': '#fec7aa'}   # Signalfarben; Magenta ist die Schnittlinie im Druckbogen


def _blau(r, g, b):
    if (r, g, b) in ((253, 153, 100), (232, 135, 90)):   # Schirmrot bleibt
        return r, g, b
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    grad = h * 360
    if s < .1 or l > .985 or l < .02 or not (8 <= grad <= 70):
        return r, g, b
    nh = 216 / 360
    if l < .3:
        ns = .66
    elif l < .62:
        ns = .55
    elif l < .86:
        ns = .3
    else:
        ns = .3
        l = min(.975, l + .01)
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
    t = re.sub(r'(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', lambda m: '%s(%d,%d,%d' % ((m.group(1),) + _blau(int(m.group(2)), int(m.group(3)), int(m.group(4)))), t)
    return t


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
    for p in glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.css'), recursive=True):
        a = open(p, encoding='utf-8').read(); b = ohne_fett(faerbe(a))
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    seiten = (glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.html'), recursive=True)
              + [os.path.join(ROOT, d, 'index.html') for d in ('unterlagen', 'drucksachen', 'untersetzer', 'feed', 'material', 'mails')])
    for p in seiten:
        if not os.path.exists(p):
            continue
        a = open(p, encoding='utf-8').read(); b = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + ohne_fett(m.group(2)) + m.group(3), nur_style(a), flags=re.S)
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    return n


if __name__ == '__main__':
    print('umgefärbt:', anwenden(), 'Dateien')
