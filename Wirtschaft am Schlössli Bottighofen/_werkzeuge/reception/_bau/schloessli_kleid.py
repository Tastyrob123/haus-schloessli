#!/usr/bin/env python3
"""Kleid des Reservationsbuchs fürs Schlössli (Nachtbau 3.11.2026): rechnet die Farben der Kopie aus dem Stamm (Nacht/Schiefer, Kerze, Warmweiss)
in die Farbwelt des Schlössli um (Werte wie _werkzeuge/oberflaeche/kleid/schloessli.css und website/assets/css/haus.css):
  Nacht/Schiefer (Farbton 235–265°, wenig Sättigung)        → Nacht über dem See / Stuhlblau (Farbton 218°), Helligkeit bleibt
  Kerze kräftig (Farbton 0–32°, Sättigung ab 0,35), mittel   → Seehimmel tief / Stuhlblau (Farbton 218°, Sättigung 0,5), Helligkeit bleibt
  Kerze hell (Helligkeit über 0,66)                           → Seehimmel (#A2B6CF, Farbton 214°), Linien und Zeichen auf Dunkel
  Warmweiss und Rosé (Farbton 0–32°, wenig Sättigung)         → Papier, Seespiegel, Blatt (Farbton 215°), Helligkeit bleibt
Grau, Grün (gespeichert) und Rot der Warnungen bleiben; die Farben des Schlössli selbst (Schirmrot #FD9964 nur als Punkt) werden nie angefasst.
Schriften: Fraunces → Open Sans (Titel in Versalien gesperrt, nie fett, nie kursiv), Instrument Sans und DM Mono aus /assets/fonts/ der Website.
Einmal angewendet am 3.11.2026 auf die frische Kopie; erneut nur auf frische Kopien (sonst wird doppelt umgerechnet)."""
import colorsys, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATEIEN = ['studio/studio.css', 'studio/hell.css', 'studio/schweben.css', 'reception.css', 'schloessli-reception.css', 'gastgeber.css', 'brief-pdf.css',
           'brief-pdf.js', 'reception.js', 'studio/rundgang.js', 'studio/zur-werkbank.js', 'studio/auswahl.js', 'pruefung.html', 'anleitung.html',
           'index.html', 'brief-pdf.html', 'studio/anleitung.js', 'pruefung.js', 'studio/auftakt.js', 'studio/schweben.js']
HAUS = {'fd9964', 'ad8a5a', 'a2b6cf', 'c5d2e1', '0f3678', '113d88', '0a234c', '0b1d3d', 'e7ecf3', 'd0dae7', 'f4f6f9', '041023', 'fbfdfd', '747b7b', '515656', 'eef2f6', '718091'}


def neu_rgb(r, g, b):
    if '%02x%02x%02x' % (r, g, b) in HAUS:
        return None
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hg = h * 360
    if s <= 0.05:
        return None
    if 230 <= hg <= 270 and s <= 0.35:                       # Nacht, Schiefer
        h2, s2 = 218 / 360, (0.55 if l <= 0.4 else 0.35 if l <= 0.75 else 0.3)
    elif hg <= 34 or hg >= 345:
        if s >= 0.35 and l <= 0.66:                           # Kerze kräftig, Kerze tief, Rot-Orange
            if s > 0.75 and l < 0.5 and hg < 8:               # Rot der Warnungen bleibt
                return None
            h2, s2 = 218 / 360, 0.5 if l < 0.45 else 0.42
        elif s >= 0.35:                                       # Kerze hell → Seehimmel
            h2, s2 = 214 / 360, 0.32
        else:                                                 # Warmweiss, Rosé, gedeckte Töne
            h2, s2 = 215 / 360, min(max(s, 0.18), 0.32)
    else:
        return None
    r2, g2, b2 = colorsys.hls_to_rgb(h2, l, s2)
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
    # Schriften des Hauses aus /assets/fonts/ (es gibt hier kein /assets/schrift/)
    for alt, neu in (('../../../assets/schrift/fraunces-soft.woff2', '/assets/fonts/OpenSans-var.woff2'), ('../../assets/schrift/fraunces-soft.woff2', '/assets/fonts/OpenSans-var.woff2'),
                     ('../../../assets/schrift/instrument.woff2', '/assets/fonts/InstrumentSans-normal-400_600.woff2'), ('../../assets/schrift/instrument.woff2', '/assets/fonts/InstrumentSans-normal-400_600.woff2'),
                     ('../../../assets/schrift/dmmono.woff2', '/assets/fonts/DMMono-normal-400.woff2'), ('../../assets/schrift/dmmono.woff2', '/assets/fonts/DMMono-normal-400.woff2'),
                     ('assets/schrift/fraunces-soft.woff2', 'assets/fonts/OpenSans-var.woff2'), ('assets/schrift/instrument.woff2', 'assets/fonts/InstrumentSans-normal-400_600.woff2'),
                     ('assets/schrift/dmmono.woff2', 'assets/fonts/DMMono-normal-400.woff2')):
        s = s.replace(alt, neu)
    s = re.sub(r"@font-face\{font-family:'Fraunces';font-style:italic;[^}]*\}\n?", '', s)
    s = s.replace("font-family:'Fraunces';font-style:normal;font-weight:100 900;", "font-family:'Open Sans';font-style:normal;font-weight:300 800;")
    s = s.replace("'Fraunces'", "'Open Sans'").replace('"Fraunces"', '"Open Sans"').replace('font-family:Fraunces,', "font-family:'Open Sans',")
    return s


if __name__ == '__main__':
    for d in sys.argv[1:] or DATEIEN:
        p = os.path.join(C, d)
        if not os.path.exists(p):
            continue
        alt = open(p, encoding='utf-8').read()
        neu = um(alt)
        open(p, 'w', encoding='utf-8').write(neu)
        print(d, 'geändert' if neu != alt else 'gleich')
