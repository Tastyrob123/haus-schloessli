#!/usr/bin/env python3
"""Nach den Seitenbauten (Kit papier_seiten.py, sticker.py, postkarten.py, beigaben.py, unterlagen_bau.py): die sechs Papier-Seiten in den Worten des Hauses
(Werkbank Papier, Nachtbau 3.11.2026; Vorlage papier_nach.py des Culinarium). Gleich grosse Stücke heissen «je 94 mm» statt «94 bis 94 mm»,
Schweizer Schreibung (ss statt ß), «der Wirtschaft am Schlössli» statt «des Wirtschaft am Schlössli», Sie-Form wie in den Werkzeugen.
Aufruf: python3 _werkbank/papier_nach.py (im Ordner website/_werkbank)."""
import os, re
HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDNER = ('unterlagen', 'drucksachen', 'untersetzer', 'sticker', 'postkarten', 'beigaben')


def text_teile(t, f):
    """f nur auf sichtbaren Text anwenden (nicht in Tags, Skripten, Stilen)."""
    aus, pos = [], 0
    for m in re.finditer(r'<script\b.*?</script>|<style\b.*?</style>|<[^>]+>', t, re.S):
        aus.append(f(t[pos:m.start()])); aus.append(m.group(0)); pos = m.end()
    aus.append(f(t[pos:]))
    return ''.join(aus)


def worte(s):
    s = re.sub(r'(\d+) bis \1 mm', r'je \1 mm', s)
    s = s.replace('ß', 'ss').replace('des Wirtschaft am Schlössli', 'der Wirtschaft am Schlössli')
    s = s.replace('und eure Unterlagen', 'und Ihre Unterlagen').replace('lasst ihr', 'lassen Sie').replace('für euch', 'für Sie')
    return s


# Titel in Versalien (Open Sans gesperrt) sind breiter als die des Kits: unter 1040 px eine Spalte, die nie breiter wird als der Bildschirm,
# am Handy der Seitentitel kleiner, damit «LÄSTERMEILE.» oder «POSTKARTEN» nie über den Rand laufen (Tor werkbank-untersetzer, 390 px)
SCHMAL = ('<style id="papier-schmal">@media(max-width:1039px){.sk .in,.stueck .in{grid-template-columns:minmax(0,1fr)}.sk .in>*,.stueck .in>*,.kopfzeile>*{min-width:0}}'
          '@media(max-width:560px){.sk h1.t1{font-size:clamp(1.7rem,8vw,2.5rem)!important;letter-spacing:.06em!important}.kopfzeile h2.t2,.stueck__t h2.t2{font-size:clamp(1.4rem,6.6vw,2.1rem)!important;letter-spacing:.06em!important}}</style>')

try:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from text_mitte import BLOCK as TM
except Exception:
    TM = ''

for o in ORDNER:
    p = os.path.join(HIER, o, 'index.html')
    if not os.path.exists(p):
        continue
    alt = t = open(p, encoding='utf-8').read()
    t = re.sub(r'<style id="papier-schmal">.*?</style>', '', t, flags=re.S).replace('</head>', SCHMAL + '\n</head>', 1)
    n = text_teile(t, worte)
    n = re.sub(r'(<meta name="description" content=")([^"]*)', lambda m: m.group(1) + worte(m.group(2)), n)
    n = re.sub(r'(<title>)([^<]*)', lambda m: m.group(1) + worte(m.group(2)), n)
    # Titel: die letzten zwei Wörter jeder Zeile fest verbunden (kein Einzelwort allein unten, Kriterium 7)
    n = re.sub(r'(<h[1-4][^>]*>)(.*?)(</h[1-4]>)', lambda m: m.group(1) + re.sub(r'(>|^)([^<>]*\S) (\S+)(?=<|$)', lambda k: k.group(1) + k.group(2) + '\u00a0' + k.group(3), m.group(2)) + m.group(3), n, flags=re.S)
    if o == 'unterlagen':   # «LUNCH» sitzt mit der Chromium-Verschiebung der Knöpfe 0,5 px rechts (Tor 3.11.2026)
        n = n.replace('</head>', '<style id="papier-lunch">@supports not (font:-apple-system-body){.uwahl button[data-id$="-lunch"]>.tm{left:.02em}}</style></head>', 1) if 'papier-lunch' not in n else n
    if TM and '</body>' in n:   # Schrift mittig in den Knöpfen wie auf allen Seiten der Werkbank (Baustein des Kerns, text_mitte.py, nur gelesen)
        n = re.sub(r'<style id="text-mitte">.*?</style><script id="text-mitte-js">.*?</script>', '', n, flags=re.S)
        i = n.rfind('</body>'); n = n[:i] + TM + n[i:]
    if n != alt:
        open(p, 'w', encoding='utf-8').write(n)
        print('papier-nach:', o)
