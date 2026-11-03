#!/usr/bin/env python3
"""Hebt die Oberfläche von La Réception des Grand Beau-Rivage (nur gelesen) in den Landgasthof Ruedihus (17.10.2026, Auftrag Chef-Chat Ruedihus:
gleiche Funktionen, gleiche Bedienung, gleiche Technik wie das Rivage, dazu was Carlton und Doldenhorn dazugebaut haben, Kleid aus dem Haus).
Vorbild für den Weg: _bau/portiere.py des Waldhotel Doldenhorn und des Carlton-Europe (beide nur gelesen).

Kopiert reception.css/js und studio/*.css|js und setzt Farben, Schriften, Tapete und Pfade des Ruedihus ein (Werte aus assets/css/main.css und
_werkbank/marke_werkbank.py, «Stube bei Kerzenlicht», jeder Ton dort aus einem Bild des Hauses gemessen):
  Wandholz #321f10 (statt Marine #1b2033), Stube #1f1209, Tief #170d06, Balken #6d431f, Papier #efe4d3, Leinen #d8c2ad, Blatt #fbf5ea, Tinte #2a1a0e,
  Gold #b78f51, Kerze #c98543, Licht #f3cd94, Geranie #c42e13 (nur als Punkt: Fehler, Neu).
  Gelasio fett (Titel aus der Wortmarke) statt Cormorant und Cinzel; Butzenscheiben (assets/img/butzen-07.png, 56 px) statt der Rivage-Tapete.
Die Farben in zwei Schritten: feste Werte für jedes Merkmal des Rivage (HEX, RGB), danach alle übrigen Blautöne über den Farbton auf das Wandholz gedreht.
Hausspezifische Inhalte (Fotos, Namen, Adressen) stehen NICHT hier, die setzt ruedihus.py danach.
Aufruf: python3 _werkzeuge/reception/_bau/portiere.py"""
import colorsys, os, re
G = os.path.expanduser('~/Desktop/Website-Projekte/Grand Beau-Rivage/website')
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Werte des Ruedihus aus assets/css/main.css (:root) und _werkbank/marke_werkbank.py (gelesen, nicht erfunden)
HEX = {'#1b2033': '#321f10', '#12162a': '#1f1209', '#0e1222': '#170d06', '#141827': '#24150a', '#141829': '#24150a', '#151a2c': '#2a180a', '#161a2c': '#2a180a',
       '#232a45': '#3d2612', '#232a43': '#3d2612', '#2c334d': '#4a2e17', '#2a3150': '#4a2c14', '#262d48': '#432812', '#3e4870': '#6d431f', '#3b4466': '#5f3a1b',
       '#323a58': '#55361c', '#323b5e': '#55361c', '#1a1d28': '#1f1209', '#22252f': '#2a1a0e', '#2c3456': '#4a2e17', '#121626': '#1a0d05', '#191d31': '#2a180a',
       '#151929': '#1f1209', '#0c0f1a': '#120a04', '#434d74': '#6d431f', '#3a4366': '#5f3a1b', '#29304f': '#432812', '#2a2d38': '#3a2a1c', '#3a3d48': '#4a3a2a',
       '#d2bf98': '#e6cf9f', '#c9ab6c': '#c39a57', '#b8975a': '#b78f51', '#c6a96b': '#c39a57', '#e3cd98': '#f0d6a2', '#f6e8c2': '#f8e2b6', '#f7e9c6': '#f8e2b6',
       '#f0e3c2': '#f1e6d4', '#e6d2a2': '#e6cf9f', '#b7a27a': '#b78f51', '#9f896f': '#b89f7f', '#7d6a4f': '#84603c', '#b99a5c': '#b78f51',
       '#fdf9f1': '#fcf6ec', '#f7f0e3': '#efe4d3', '#efe4cf': '#e7d7c0', '#fbf4e4': '#fbf3e2', '#fdf6e6': '#fdf8ee', '#f4ead6': '#ecdcc5', '#f4efe5': '#f6ecdc',
       '#ecdcb8': '#e7d7c0', '#e2d2b5': '#d8c2ad', '#fbf7ef': '#fbf5ea', '#fffdf8': '#fffaf0', '#f7efdd': '#f7ecdc', '#f3eadb': '#f1e6d4', '#f0e6d2': '#efe3cf',
       '#9c3b34': '#a8321a', '#3d6b4f': '#46652e', '#b8892a': '#b8862a', '#7a1f2b': '#7a2412'}
RGB = {'159,137,111': '184,159,127', '210,191,152': '230,207,159', '27,32,51': '50,31,16', '26,29,40': '31,18,9', '183,162,122': '183,143,81', '240,227,194': '241,230,212',
       '20,24,39': '31,18,9', '190,206,255': '243,205,148', '150,166,214': '201,133,67', '184,151,90': '183,143,81', '152,115,60': '132,96,60', '17,20,31': '23,13,6',
       '120,100,70': '132,96,60', '253,249,241': '252,246,236', '247,240,227': '239,228,211', '20,26,46': '31,18,9', '9,17,39': '23,13,6', '10,12,22': '23,13,6',
       '16,19,32': '23,13,6', '6,18,42': '23,13,6', '222,232,255': '248,226,182', '156,59,52': '168,50,26', '61,107,79': '70,101,46', '184,137,42': '184,134,42'}


def _drehen(r, g, b):
    """Übrige Blautöne des Rivage (Farbton 205–255°) auf den Farbton des Wandholzes (26°) drehen; Sättigung leicht gedämpft (Holz, nicht Orange)."""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if s < 0.08 or not (205 / 360 <= h <= 255 / 360):
        return None
    h = 26 / 360
    s = min(0.62, s * 1.05) if l < 0.5 else min(0.5, s * 0.8)
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def _hex(m):
    x = m.group(0).lower()
    if x in HEX:
        return HEX[x]
    d = _drehen(int(x[1:3], 16), int(x[3:5], 16), int(x[5:7], 16))
    return '#%02x%02x%02x' % d if d else m.group(0)


def _rgb(m):
    k = m.group(1)
    if k in RGB:
        return 'rgba(' + RGB[k]
    r, g, b = (int(v) for v in k.split(','))
    d = _drehen(r, g, b)
    return 'rgba(' + (','.join(map(str, d)) if d else k)


def farben(t):
    t = re.sub(r'#[0-9a-fA-F]{6}\b', _hex, t)
    t = re.sub(r'rgba\((\d+,\d+,\d+)', _rgb, t)
    return t


SERIF = "'Gelasio',Georgia,'Times New Roman',serif"


def schrift(t, js=False):
    """Cormorant und Cinzel → Gelasio. In JS stehen die Schriftangaben in Zeichenketten mit ' oder ": dort ohne Anführungszeichen (gültiges CSS),
    sonst bricht die Zeichenkette (Falle aus dem Doldenhorn)."""
    if js:
        for alt in ("'Cormorant Garamond',Georgia,'Times New Roman',serif", "'Cormorant Garamond',Georgia,serif", '"Cormorant Garamond",Georgia,serif', "'Cinzel',Georgia,serif", 'Cinzel,Georgia,serif'):
            t = t.replace(alt, 'Gelasio,Georgia,serif')
        return t
    t = t.replace("'Cormorant Garamond',Georgia,'Times New Roman',serif", SERIF)
    t = t.replace("'Cormorant Garamond',Georgia,serif", SERIF).replace("'Cinzel',Georgia,serif", SERIF)
    t = t.replace('"Cormorant Garamond",Georgia,serif', SERIF).replace('Cinzel,Georgia,serif', "'Gelasio',Georgia,serif")
    t = re.sub(r"@font-face\{font-family:'Cormorant Garamond'[^}]*\}\n?", '', t)
    t = re.sub(r"@font-face\{font-family:'Cinzel'[^}]*\}\n?", '', t)
    return t


PFAD_STUDIO = [("url('../assets/", "url('../../../assets/"), ("url(\"../assets/", "url(\"../../../assets/")]
PFAD_REC = [("url('../assets/", "url('../../assets/"), ("url(\"../assets/", "url(\"../../assets/")]
GELASIO = ("@font-face{font-family:'Gelasio';font-style:normal;font-weight:700;font-display:swap;src:url('%sassets/fonts/gelasio-700.woff2') format('woff2')}\n"
           "@font-face{font-family:'Gelasio';font-style:normal;font-weight:400;font-display:swap;src:url('%sassets/fonts/gelasio-400.woff2') format('woff2')}\n")


def gelasio_masse(t):
    """Gelasio läuft wie Georgia, deutlich grösser als Cormorant: Titel in Gelasio fett auf 86 % (Haus: «Gelasio fett», Betonung über Farbe,
    nie kursiv), Fliesstext und Kursives des Rivage (Cormorant 300/400, italic) in Instrument Sans auf 90 %, wie auf der Website des Ruedihus."""
    def masse(s, f):
        return re.sub(r'(\d+(?:\.\d+)?)px', lambda m: ('%g' % round(float(m.group(1)) * f, 1)) + 'px', s)

    def ein(m):
        vor = m.group(1)
        if re.search(r'\b(italic|300|400)\b', vor):
            return 'font:' + masse(re.sub(r'\bitalic\s+', '', vor), 0.9) + 'var(--sans)'
        vor = re.sub(r'\b(500|600)\b', '700', vor)
        if not re.search(r'\b700\b', vor):
            vor = '700 ' + vor
        return 'font:' + masse(vor, 0.86) + 'var(--serif)'
    t = re.sub(r'font:([^;}]*?)var\(--serif\)', ein, t)
    # Versalien des Rivage (Cinzel 400) → Gelasio fett in Versalien, wie der Name auf den Karten des Hauses
    return re.sub(r'font:(\d00) ([^;}]*?)var\(--caps\)', lambda m: 'font:700 ' + m.group(2) + 'var(--caps)', t)


def tapete(t):
    """Rivage-Tapete → Butzenscheiben des Ruedihus (assets/img/butzen-07.png, 112 px Datei, doppelt scharf: 56 × 56 px), wie in main.css .butzen."""
    t = t.replace('tapete-dunkel.webp', 'butzen-09.png').replace('tapete-hell.webp', 'butzen-07.png')
    for alt in ('/340px auto', '/300px auto', '/180px auto'):
        t = t.replace(alt, '/56px 56px')
    return t


def kopiere(quelle, ziel, pfade, tiefe):
    t = open(os.path.join(G, quelle), encoding='utf-8').read()
    t = tapete(schrift(farben(t), quelle.endswith('.js')))
    if quelle.endswith('.css'):
        t = gelasio_masse(t)
    for a, b in pfade:
        t = t.replace(a, b)
    if quelle == 'studio/studio.css':
        i = t.index('@font-face')
        t = t[:i] + GELASIO % (tiefe, tiefe) + t[i:]
    os.makedirs(os.path.dirname(os.path.join(C, ziel)), exist_ok=True)
    open(os.path.join(C, ziel), 'w', encoding='utf-8').write(t)


if __name__ == '__main__':
    for f in ('studio.css', 'hell.css', 'schweben.css'):
        kopiere('studio/' + f, 'studio/' + f, PFAD_STUDIO, '../../../')
    for f in ('schweben.js', 'buehne.js', 'auftakt.js'):
        kopiere('studio/' + f, 'studio/' + f, [], '')
    kopiere('reception/reception.css', 'reception.css', PFAD_REC, '../../')
    c = os.path.join(C, 'reception.css'); x = open(c, encoding='utf-8').read().replace('/* La Réception · Grand Beau-Rivage.', '/* La Réception · Landgasthof Ruedihus (aus dem Werkzeug des Grand Beau-Rivage).', 1); open(c, 'w', encoding='utf-8').write(x)
    kopiere('reception/reception.js', 'reception.js', [], '')
    print('kopiert')
