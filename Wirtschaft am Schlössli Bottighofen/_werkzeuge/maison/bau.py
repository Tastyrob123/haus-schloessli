#!/usr/bin/env python3
"""Das Hafenbüro (Zentrale, Arbeitsname La Maison) der Wirtschaft am Schlössli Bottighofen (Nachtbau 3./4.11.2026, Agent «schloessli-maison»).
Funktion, Bedienung und Technik wie die Zentrale der anderen Häuser (Master Werkzeug-Bau 4.1, M01 bis M27, R03, R04, R18, R19);
Stamm: die Zentrale der Häuser (Empfang mit fünf hohen Fenstern), Kleid und Inhalt aus diesem Haus.

  python3 _werkzeuge/maison/bau.py      baut beide Fassungen aus einem Lauf (M13):
      _werkzeuge/maison/index.html …       lokal, über server.py (http://127.0.0.1:9281/_werkzeuge/maison/)
      _werkzeuge/maison/online/…           online-Fassung (nichts wird hochgeladen; Wege ohne localhost)

Alles Hausbezogene kommt aus Hauswerten, nichts ist abgetippt:
  website/inhalt/haus.json      Name, Strasse, Ort (Adresse des Hauses)
  website/inhalt/bilder.json    Fotos (Schlüssel, Alt-Text, Horizont «hz»), Dateien unter website/assets/img/<schlüssel>-<breite>.webp
  oberflaeche/kleid/schloessli.js  WO_HAUS: Namen und Sätze der sieben Werkzeuge, Bar (Lästermeile), Ort
  oberflaeche/kleid/schloessli-zeichen.svg / schloessli-marke.svg  Zeichen (die Zeiger) und Wortmarke
Was ein Werkzeug liefert (Bildschirm, Knopf-Namen), nimmt der Bau erst, wenn es im Revier des Werkzeugs liegt (_werkzeuge/<werkzeug>/index.html)
und sein Bildschirm unter roh/ liegt (aufgenommen mit schirme.js)."""
import glob, hashlib, html, json, os, re, shutil, sys

e = html.escape
HIER = os.path.dirname(os.path.abspath(__file__))
WZ = os.path.dirname(HIER)                             # _werkzeuge/
ROOT = os.path.dirname(WZ)                             # Projektordner des Hauses
WEB = os.path.join(ROOT, 'website')
KLEID = os.path.join(WZ, 'oberflaeche', 'kleid')
QUELLE = os.path.join(HIER, 'quelle')
ROH = os.path.join(HIER, 'roh')
PORT = 9281                                             # Prüfserver des Hafenbüros (server.py, cloud/haus.json)
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


# ---------------------------------------------------------------- Hauswerte (website/inhalt/haus.json, kleid/schloessli.js)
HAUS = json.load(open(os.path.join(WEB, 'inhalt', 'haus.json'), encoding='utf-8'))
NAME = HAUS['name']                                       # «Wirtschaft am Schlössli»
STRASSE = HAUS['strasse']                                 # «Seestrasse 50»
PLZ_ORT = HAUS['ort']                                     # «8598 Bottighofen»
_ot = re.fullmatch(r'(\d{4,5}) (.+)', PLZ_ORT)
if not _ot:
    raise SystemExit('haus.json: Ort nicht lesbar')
ORT = _ot.group(2)
KLEID_JS = open(os.path.join(KLEID, 'schloessli.js'), encoding='utf-8').read()


def wo_feld(n):
    m = re.search(n + r":\s*'([^']+)'", KLEID_JS)
    if not m:
        raise SystemExit('kleid/schloessli.js: ' + n + ' fehlt')
    return m.group(1)


def wo_gruppe(n):
    """namen: {…} oder saetze: {…} aus WO_HAUS (die eine Stelle für alle sieben Werkzeuge)."""
    m = re.search(n + r":\s*\{(.*?)\}", KLEID_JS, re.S)
    return dict(re.findall(r"(\w+):\s*'([^']+)'", m.group(1))) if m else {}


BAR = wo_feld('bar')                                      # «Lästermeile»
KURZNAME = wo_feld('kurz')                                # «schloessli» (Speicher-Schlüssel)
BILDER_W = json.load(open(os.path.join(WEB, 'inhalt', 'bilder.json'), encoding='utf-8'))


def svg_innen(pfad):
    s = open(pfad, encoding='utf-8').read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    innen = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    innen = re.sub(r'<!--.*?-->', '', innen, flags=re.S).replace('fill="#000"', '')
    return vb, re.sub(r'\s+', ' ', innen).strip()


ZEICHEN_VB, ZEICHEN = svg_innen(os.path.join(KLEID, 'schloessli-zeichen.svg'))       # die Zeiger der Wortmarke (Zeichen des Hauses)


# ---------------------------------------------------------------- Werkzeuge des Hauses
# Reihe wie in allen Häusern (Taste 1 bis 6 gleich).
REIHE = ['bureau', 'carte', 'imprimerie', 'reception', 'livre', 'registre']
TEIL = {'bureau': 'website', 'carte': 'karten', 'imprimerie': 'druck', 'reception': 'gaeste', 'livre': 'marke', 'registre': 'besuche'}
PORTS = {'bureau': 9282, 'carte': 9283, 'reception': 9284, 'livre': 9285, 'registre': 9286, 'imprimerie': 9287}   # AUFTRAG-GEMEINSAM.md

# Namen und Sätze der Werkzeuge: EINE Stelle für alle sieben Werkzeuge ist kleid/schloessli.js (WO_HAUS.namen, WO_HAUS.saetze). Hier nur gelesen.
NAMEN = wo_gruppe('namen')
SAETZE = wo_gruppe('saetze')
for _t in ['zentrale'] + list(TEIL.values()):
    if not NAMEN.get(_t) or not SAETZE.get(_t):
        raise SystemExit('kleid/schloessli.js: Name oder Satz fehlt: ' + _t)
ZENTRALE = NAMEN['zentrale']
ROLLE = {'bureau': 'Website pflegen', 'carte': 'Karten des Hauses', 'imprimerie': 'Aushänge und Drucksachen', 'reception': 'Anfragen und Gäste-Chat',
         'livre': 'Marke zum Arbeiten', 'registre': 'Besuche der Website'}
W = {k: dict(name=NAMEN[TEIL[k]], rolle=ROLLE[k]) for k in REIHE}
ROLLE_K = {'bureau': 'Website', 'carte': 'Karten', 'imprimerie': 'Drucksachen', 'reception': 'Gäste', 'livre': 'Marke', 'registre': 'Besuche'}   # kurze Zeile im Fenster
# Stand-Zeile im Fenster, solange das Werkzeug keinen Stand liefert (maison.js setzt sie zurück, wenn ein Werkzeug nicht antwortet)
KURZ = {'bureau': 'Texte, Zeiten, Ferien, Anlässe', 'carte': 'Karte, Lunch, Lästermeile, Wein', 'imprimerie': 'Aushänge, druckfertig', 'reception': 'Anfragen und Fragen',
        'livre': 'Fotos, Wortmarke, Farben', 'registre': 'Besuche ohne Namen'}
SATZ = {k: SAETZE[TEIL[k]] for k in REIHE}                 # Satz je Saal: nur aus WO_HAUS.saetze


def geliefert(k):
    """Ein Werkzeug gilt als da, wenn sein Revier eine Oberfläche hat (_werkzeuge/<werkzeug>/index.html)."""
    return os.path.exists(os.path.join(WZ, k, 'index.html'))


# Stand-Weg je Werkzeug (Form fest, Master 4.1 «Stand-Wege»): steht in stand_wege.json (aus dem Werkzeug gelesen). Lokal holt der Prüfserver
# des Hafenbüros sie über /_weiter/<werkzeug>/… (ein Browser liest nicht quer über Ports); online nur, wenn das Werkzeug online einen Weg hat.
def stand_wege():
    try:
        return json.load(open(os.path.join(HIER, 'stand_wege.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def wege(online):
    sw = stand_wege()
    aus = {}
    for k in REIHE:
        d = sw.get(k) or {}
        if online:
            auf = d.get('online') or '../werkbank/index.html#werkzeuge'
            stand = d.get('stand_online') or ''
        else:
            auf = (d.get('adresse') or f'http://127.0.0.1:{PORTS[k]}/_werkzeuge/{k}/') if geliefert(k) else ''
            stand = [f'/_weiter/{k}/' + x.lstrip('/') for x in ([d['stand']] if isinstance(d.get('stand'), str) else d.get('stand') or [])] if geliefert(k) else []
        aus[k] = dict(auf=auf, stand=stand, anl=(d.get('anleitung_online') if online else d.get('anleitung')) or '')
    return aus


# ---------------------------------------------------------------- Bilder
BILDER = {}
FEHLT = []


def alt(k):
    return BILDER_W[k]['alt']


def webp(ziel, name, quelle, breit, klein=None, qual=82, crop=None):
    """Bild nach img/<name>.webp (und -s.webp), nur neu, wenn die Quelle neuer ist."""
    from PIL import Image
    os.makedirs(os.path.join(ziel, 'img'), exist_ok=True)
    z = os.path.join(ziel, 'img', name + '.webp')
    im = Image.open(quelle).convert('RGB')
    if crop:
        im = im.crop(crop)
    w = min(breit, im.width); h = round(im.height * w / im.width)
    if not os.path.exists(z) or os.path.getmtime(z) < max(os.path.getmtime(quelle), os.path.getmtime(__file__)):
        (im.resize((w, h), Image.LANCZOS) if w != im.width else im).save(z, quality=qual, method=6)
        if klein:
            kw = min(klein, w)
            im.resize((kw, round(im.height * kw / im.width)), Image.LANCZOS).save(os.path.join(ziel, 'img', name + '-s.webp'), quality=78, method=6)
    BILDER[name] = (w, h)


def web_bild(k):
    """Grösste Stufe eines Fotos der Website (website/assets/img/<schlüssel>-<breite>.webp, Register bilder.json)."""
    if k not in BILDER_W:
        raise SystemExit('Foto nicht im Register der Website: ' + k)
    m = sorted(glob.glob(os.path.join(WEB, 'assets', 'img', f'{k}-[0-9]*.webp')), key=lambda p: -int(re.search(r'-(\d+)\.webp$', p).group(1)))
    if not m:
        raise SystemExit('Foto fehlt in der Website: ' + k)
    return m[0]


# Fotos aus dem Markenbuch für dessen Saal (nur Fotos des Hauses; keine Gäste-, Fremd- oder KI-Bilder, UEBERGABE.md)
ARCHIV = ['gaststube', 'bar', 'thon', 'wein', 'abend', 'bootshafen']
SCHIRME = {'bureau': ['bureau', 'bureau-2'], 'carte': ['carte'], 'imprimerie': ['imprimerie'], 'reception': ['reception'],
           'livre': ['livre-fotos', 'livre-marke'], 'registre': ['registre', 'registre-herkunft']}


# Empfang: fünf hohe Fenster, je Werkzeug ein Foto des Hauses über die ganze Höhe, Die Besucherliste als Zahlenzeile unter dem Titel.
# Je Foto: Lage am Desktop (hohe Säule) und am Handy (flaches Band), so gewählt, dass das Motiv steht
# (Terrasse unter den Platanen, ein Teller auf blauem Grund, der Morgen am See unter dem Titel, der Gastgeber, die Terrasse am Abend).
FENSTER = {'bureau': ('platanen', '50% 50%', '50% 62%'), 'carte': ('anguria', '50% 50%', '50% 50%'), 'imprimerie': ('morgen', '62% 50%', '50% 55%'),
           'reception': ('jonas', '50% 50%', '50% 38%'), 'livre': ('abend', '50% 50%', '50% 52%')}
FARBE = {}   # Platzhalter in der Motivfarbe statt Schwarz


def bilder(ziel):
    BILDER.clear(); FEHLT.clear()
    from PIL import Image
    for k, (f, pos, pos_h) in FENSTER.items():
        q = web_bild(f); w, h = Image.open(q).size
        px = float(pos.split()[0].rstrip('%')) / 100; hy = float(pos_h.split()[1].rstrip('%')) / 100
        # Fenster am Desktop: nur der sichtbare Streifen (Breite : Höhe = 0,36 wie ein Fenster bei 1440 × 900 bis 1920 × 1080), 600 und 900 px breit
        cw = min(w, round(h * .36)); x0 = round((w - cw) * px)
        for b in (600, 900):
            webp(ziel, f'fenster-{k}-{b}', q, b, None, 72, (x0, 0, x0 + cw, h))
        # am Handy ein flaches Band (2,6 : 1) an der Stelle, wo das Motiv steht
        bh = min(h, round(w / 2.6)); y0 = round((h - bh) * hy)
        webp(ziel, f'fenster-{k}-band', q, 800, None, 74, (0, y0, w, y0 + bh))
        FARBE[k] = '#%02x%02x%02x' % Image.open(q).convert('RGB').resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    for k in REIHE:
        for n in SCHIRME[k]:
            q = next((os.path.join(ROH, n + x) for x in ('.png', '.jpg', '.webp') if os.path.exists(os.path.join(ROH, n + x))), '')
            if not geliefert(k) or not q:
                FEHLT.append(n)
                continue
            webp(ziel, 'schirm-' + n, q, 2400, 1200, 84)
    # Stücke der Säle: Karten (roh/karten/*.png, Seiten aus den PDF der Karten), Drucksachen (roh/druck/*.png), Fotos aus dem Markenbuch
    if geliefert('imprimerie'):
        for q in sorted(glob.glob(os.path.join(ROH, 'druck', '*.png'))):
            webp(ziel, 'druck-' + os.path.basename(q)[:-4], q, 1000, None, 84)
    if geliefert('carte'):
        for q in sorted(glob.glob(os.path.join(ROH, 'karten', '*.png'))):
            webp(ziel, 'karte-' + os.path.basename(q)[:-4], q, 1000, None, 84)
    if geliefert('livre'):
        for k in ARCHIV:
            webp(ziel, 'archiv-' + k, web_bild(k), 900, None, 80)
    for n in ('reception-chat',):
        q = os.path.join(ROH, n + '.png')
        if os.path.exists(q) and geliefert('reception'):
            webp(ziel, 'schirm-' + n, q, 2400, 1200, 84)
    # Tapeten der Website als gerechnetes Bild (quelle/tapete.js, doppelte Dichte): ein SVG-Muster kostete am Handy beim ersten Scrollen ein Bild über 33 ms
    for art in ('dunkel', 'hell'):
        q = os.path.join(QUELLE, f'tapete-{art}@2x.png')
        if not os.path.exists(q) or os.path.getmtime(q) < os.path.getmtime(os.path.join(WEB, 'assets', 'svg', f'tapete-a-{art}.svg')):
            raise SystemExit('Tapete der Website ist neuer: node _werkzeuge/maison/quelle/tapete.js')
        Image.open(q).save(os.path.join(ziel, 'img', f'tapete-{art}.webp'), lossless=True, method=6)
    # Schriften: aus /assets/fonts/ der Website (maison.css), keine Kopie im Revier


# ---------------------------------------------------------------- Bausteine
I = {
    'stift': '<svg viewBox="0 0 24 24"><path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/></svg>',
    'uhr': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3 2"/></svg>',
    'waage': '<svg viewBox="0 0 24 24"><path d="M12 4v16M7 20h10M5 8h14"/><path d="m5 8-2.5 6a2.5 2.5 0 0 0 5 0zM19 8l-2.5 6a2.5 2.5 0 0 0 5 0z"/></svg>',
    'liste': '<svg viewBox="0 0 24 24"><path d="M9 7h11M9 12h11M9 17h11"/><path d="M4.5 7h.5M4.5 12h.5M4.5 17h.5"/></svg>',
    'pdf': '<svg viewBox="0 0 24 24"><path d="M6 3.5h8l4 4v13H6z"/><path d="M14 3.5v4h4M9 13h6M9 16.5h4"/></svg>',
    'zurueck': '<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 1 0 2.4-5.7"/><path d="M4 4v4.5h4.5"/></svg>',
    'satz': '<svg viewBox="0 0 24 24"><path d="M4 6h16M4 11h16M4 16h9"/><path d="m17 15 3 3-3 3"/></svg>',
    'fuenf': '<svg viewBox="0 0 24 24"><rect x="3.5" y="5" width="7" height="9" rx="1"/><rect x="13.5" y="5" width="7" height="9" rx="1"/><path d="M6 18h12"/></svg>',
    'druck': '<svg viewBox="0 0 24 24"><path d="M7 8V3.5h10V8"/><rect x="3.5" y="8" width="17" height="8" rx="1.5"/><path d="M7 13.5h10v7H7z"/></svg>',
    'blase': '<svg viewBox="0 0 24 24"><path d="M4 5.5h16v11H10l-4 3.5v-3.5H4z"/></svg>',
    'eingang': '<svg viewBox="0 0 24 24"><path d="M4 13.5 6.5 5h11l2.5 8.5V19H4z"/><path d="M4 13.5h5a3 3 0 0 0 6 0h5"/></svg>',
    'foto': '<svg viewBox="0 0 24 24"><rect x="3.5" y="5.5" width="17" height="13" rx="1.5"/><path d="m3.5 16 5-5 4 4 3-3 5 5"/><circle cx="15.5" cy="9.5" r="1.5"/></svg>',
    'datei': '<svg viewBox="0 0 24 24"><path d="M3.5 7.5h6l2 2h9v9h-17z"/></svg>',
    'farbe': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="9" cy="9.5" r="1.3"/><circle cx="14.5" cy="8.5" r="1.3"/><circle cx="16" cy="13.5" r="1.3"/><path d="M11 20a2.5 2.5 0 0 1 0-5"/></svg>',
    'karte': '<svg viewBox="0 0 24 24"><path d="M4 20V6l5-2 6 2 5-2v14l-5 2-6-2z"/><path d="M9 4v14M15 6v14"/></svg>',
}

UI = []   # Knopf-Namen aus den Tafeln: (werkzeug, name), gegen den Code des Werkzeugs geprüft (knoepfe())


def ui(t, k=''):
    def merk(m):
        UI.append((k, m.group(1)))
        return f'<span class="m-ui">{m.group(1)}</span>'
    return re.sub(r'«([^»]+)»', merk, t)


# Tafeln «So geht’s». ALLG ohne Knopf-Namen, solange das Werkzeug nicht vorliegt. HAUS (tafeln.json) mit den echten Knopf-Namen («…»),
# erst nach der Lieferung aus dem Code des Werkzeugs gelesen und beim Bau dagegen geprüft.
TAFEL_ALLG = {
    'bureau': [('stift', 'Text oder Foto ändern', 'Den Bereich wählen, in der Vorschau auf den Text oder das Foto klicken und ändern.'),
               ('uhr', 'Zeiten und Ferien', 'Öffnungs- und Küchenzeiten, Ruhetage, Ferien und Anlässe stehen an einer Stelle. Einmal ändern, jede Seite der Website folgt.'),
               ('waage', 'Erst Entwurf, dann online', 'Gespeichert ist erst ein Entwurf. Vorher und nachher nebeneinander ansehen, dann veröffentlichen.')],
    'carte': [('stift', 'Gericht oder Preis ändern', 'Die Karte wählen, das Gericht anklicken, Name, Beschreibung oder Preis überschreiben. Daneben steht sofort die Karte.'),
              ('liste', 'Neues Gericht', 'Bei der passenden Rubrik ein Gericht anfügen und an die richtige Stelle schieben.'),
              ('pdf', 'Neue Karte drucken', 'Vorab eine Probe ansehen, dann veröffentlichen: die PDF wird neu gesetzt, die Karte auf der Website gleich mit.')],
    'imprimerie': [('satz', 'Sagen, was Sie brauchen', 'In einem Satz beschreiben, was gebraucht wird, oder eine fertige Vorlage mit Texten und Zeiten des Hauses nehmen.'),
                   ('fuenf', 'Einen Entwurf wählen', 'Es kommen mehrere Entwürfe im Stil des Hauses. Den passenden anklicken und anpassen.'),
                   ('druck', 'Drucken', 'Druckfertig als PDF speichern, für die Druckerei oder den eigenen Drucker.')],
    'reception': [('blase', 'Gäste fragen im Chat', 'Auf jeder Seite der Website können Gäste fragen. Der Chat antwortet aus Ihren Seiten und Karten, in der Sprache des Gastes.'),
                  ('eingang', 'Anfragen beantworten', 'Ein Tisch, ein Bankett, ein Gutschein: jede Anfrage steht im Eingang, mit einem Entwurf für Ihre Antwort. Verschickt wird nur, was Sie selbst schicken.'),
                  ('liste', 'Lücken schliessen', 'Wusste der Chat etwas nicht, steht die Frage in einer eigenen Liste. Einmal nachtragen, ab dann antwortet er selbst.')],
    'livre': [('foto', 'Ein Foto holen', 'Ein Foto anklicken und die Grösse wählen: für Instagram, die Website oder den Druck.'),
              ('datei', 'Wortmarke weitergeben', 'Wortmarke, Zeiger, Farben und Schriften liegen als Dateien bereit, für Agentur oder Druckerei.'),
              ('farbe', 'Einen Entwurf prüfen', 'Aushang oder Flyer einer Agentur hineinziehen. Es sagt Punkt für Punkt, was zum Haus passt.')],
    'registre': [('karte', 'Woher die Gäste kommen', 'Länder und Orte der Besuche, ohne Cookies und nie mit Namen.'),
                 ('liste', 'Was sie sich ansehen', 'Die meistbesuchten Seiten und Karten, und wie lange die Gäste bleiben.'),
                 ('uhr', 'Weiter zur Reservation', 'Wie oft ein Besuch zum Reservieren, zum Anrufen oder zu einer Anfrage führt.')],
}


def tafel_zeilen(k):
    try:
        h = json.load(open(os.path.join(HIER, 'tafeln.json'), encoding='utf-8'))
    except (OSError, ValueError):
        h = {}
    z = h.get(k) if geliefert(k) and h.get(k) else TAFEL_ALLG[k]
    nm = {TEIL[x]: W[x]['name'] for x in REIHE}      # Namen anderer Werkzeuge nur aus der einen Stelle ({karten} → «die Tafel» im Satz)
    return [(s, t, re.sub(r'\{(\w+)\}', lambda m: (nm[m.group(1)][0].lower() + nm[m.group(1)][1:]) if m.group(1) in nm else m.group(0), x)) for s, t, x in z]


def tafel(k, i=0, extra=''):
    z = ''.join(f'<div class="m-tafel__z"><i>{I[s]}</i><p><b>{e(t)}</b>{ui(e(x, quote=False), k)}</p></div>' for s, t, x in tafel_zeilen(k))
    return f'<div class="m-tafel" data-r style="--i:{i}"><p class="m-tafel__kopf"><span>So geht’s</span></p>{z}{extra}</div>'


class Bau:
    online = False


_MARKE = open(os.path.join(KLEID, 'schloessli-marke.svg'), encoding='utf-8').read()
WM_VB = re.search(r'<symbol id="wm" viewBox="([^"]+)"', _MARKE).group(1)
WM = re.search(r'<symbol id="wm"[^>]*>(.*?)</symbol>', _MARKE, re.S).group(1)
# Stufen des Wegs zur Reservation im Saal der Besucherliste: Namen wie in der Besucherliste, sobald sie sie liefert (registre/stufen.json → maison);
# bis dahin die Wege der Website (Karte ansehen → Reservation, Anruf oder Anfrage → am Tisch). STUFE_SEITE: die Seite der zweiten Stufe.
try:
    _st = json.load(open(os.path.join(WZ, 'registre', 'stufen.json'), encoding='utf-8'))
    STUFE, STUFE_SEITE = _st['maison'], _st.get('seite', 'karte.html')
except (OSError, ValueError, KeyError):
    STUFE, STUFE_SEITE = ['«Die Karte» angesehen', 'Reservation oder Anfrage', 'am Tisch', 'zählt das Team im Haus'], 'karte.html'


def wortmarke(c):
    return f'<svg class="{c}" viewBox="{WM_VB}" fill="currentColor" aria-label="{e(NAME)}" role="img">{WM}</svg>'


def zeichen(c):
    return f'<svg class="{c}" viewBox="{ZEICHEN_VB}" fill="currentColor" aria-hidden="true">{ZEICHEN}</svg>'


def schirm(n, k, leiste, alt, i=0, sizes='(max-width:1000px) 92vw, 60vw'):
    leiste = leiste.removeprefix(f'{ZENTRALE} · ')   # Abnahme-Tor 30.10.2026 (K2): man steht schon in der Zentrale; Werkzeug · Bereich passt bei jeder Breite ganz in die Leiste
    name = 'schirm-' + n
    if name not in BILDER:
        if Bau.online:
            return ''
        return (f'<figure class="m-schirm m-schirm--platz" data-r="schweb" style="--i:{i}" data-platz="{e(n)}"><div class="m-schirm__leiste" aria-hidden="true"><span>{e(leiste)}</span></div>'
                f'<div class="m-platz">{zeichen("")}<b>Bildschirm folgt</b><p>{e(W[k]["name"])} wird gerade gebaut. Sobald es vorliegt, steht hier sein echter Bildschirm.</p>'
                f'<small>Platzhalter, nur lokal</small></div></figure>')
    b = BILDER[name]
    return (f'<figure class="m-schirm" data-r="schweb" style="--i:{i}"><div class="m-schirm__leiste" aria-hidden="true"><span>{e(leiste)}</span></div>'
            f'<img src="img/{name}.webp" srcset="img/{name}-s.webp 1200w, img/{name}.webp {b[0]}w" sizes="{sizes}" width="{b[0]}" height="{b[1]}" alt="{e(alt)}" loading="eager" decoding="sync"></figure>')


def stueck_bild(name, alt, cls='', i=0):
    if name not in BILDER:
        return ''
    w, h = BILDER[name]
    return f'<figure class="m-stueck {cls}" data-r="schweb" style="--i:{i}"><img src="img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}" loading="eager" decoding="sync"></figure>'


def stuecke(k):
    """Weitere echte Bilder je Saal (Fehlerbuch 10a: die Säle der anderen Häuser haben mehr Bilder als nur einen Bildschirm)."""
    if k == 'bureau':
        t = schirm('bureau-2', 'bureau', f'{ZENTRALE} · {W["bureau"]["name"]} · Startseite', 'Eine Seite offen: links die Stellen, rechts die Startseite der Website', 1, '(max-width:1000px) 92vw, 40vw')
        return f'<div class="m-stuecke m-stuecke--eins">{t}</div>' if 'schirm-bureau-2' in BILDER else ''
    if k in ('carte', 'imprimerie'):
        vor = 'karte-' if k == 'carte' else 'druck-'
        n = sorted(b for b in BILDER if b.startswith(vor))[:3]
        art = ['m-stueck--blatt', 'm-stueck--quer', 'm-stueck--blatt']
        try:   # Namen der Stücke aus der Lieferung des Werkzeugs (roh/karten/namen.json aus /api/status von La Carte, roh/druck/namen.json), nichts erfunden
            alt = json.load(open(os.path.join(ROH, 'karten' if k == 'carte' else 'druck', 'namen.json'), encoding='utf-8'))
        except (OSError, ValueError):
            alt = {}
        t = ''.join(stueck_bild(b, W[k]['name'] + ': ' + alt.get(b[len(vor):], b[len(vor):].replace('-', ' ')), 'm-stueck--quer' if BILDER[b][0] > BILDER[b][1] else 'm-stueck--blatt', i + 1) for i, b in enumerate(n))
        return f'<div class="m-stuecke m-stuecke--karten">{t}</div>' if t else ''
    if k == 'registre':   # Abnahme-Tor 30.10.2026 (K4): sonst steht links nur ein Bildschirm neben der langen rechten Spalte
        t = schirm('registre-herkunft', 'registre', f'{W["registre"]["name"]} · Herkunft', W['registre']['name'] + ' mit Beispielwerten: woher die Gäste kommen', 1, '(max-width:1000px) 92vw, 40vw')
        return f'<div class="m-stuecke m-stuecke--eins">{t}</div>' if 'schirm-registre-herkunft' in BILDER else ''
    if k == 'reception':
        t = schirm('reception-chat', 'reception', f'{ZENTRALE} · {W["reception"]["name"]} · Chat ausprobieren', 'Chat ausprobieren: so fragt ein Gast, mit Beispielfragen', 1, '(max-width:1000px) 92vw, 40vw')
        return f'<div class="m-stuecke m-stuecke--eins">{t}</div>' if 'schirm-reception-chat' in BILDER else ''
    if k == 'livre':
        t = ''.join(stueck_bild('archiv-' + n, BILDER_W[n]['alt'], 'm-stueck--foto', i + 1) for i, n in enumerate(ARCHIV))
        return f'<div class="m-stuecke m-stuecke--fotos">{t}</div>' if t else ''
    return ''


def knopf(t, href, cls='', neu=False):
    if not href:
        return f'<span class="m-hinweis">{e(t.replace("öffnen", "folgt"))}, sobald es vorliegt.</span>'
    z = ' target="_blank" rel="noopener"' if neu else ''
    return f'<a class="knopf {cls}" href="{e(href)}"{z}><span class="knopf__t">{e(t)}</span><i>{PF}</i></a>'


def saal_kopf(k, nr):
    teile = W[k]['name'].split(' ', 1)
    titel = f'<em>{e(teile[0])}</em> {e(teile[1])}' if len(teile) == 2 else e(teile[0])
    return (f'<header class="m-saal__kopf">{zeichen("m-saal__z")}<p class="m-saal__nr" data-r style="--i:0">N° {nr + 1} von 6 · {e(W[k]["rolle"])}</p>'
            f'<h2 class="m-saal__titel" data-r style="--i:1">{titel}</h2><p class="m-saal__satz" data-r style="--i:2">{e(SATZ[k])}</p></header>'
            f'<div class="m-saal__linie" aria-hidden="true"><i></i></div>')


def farben():
    """Farben des Hauses für den Saal der Marke: aus livre.json des Werkzeugs (nur nach der Lieferung), sonst keine (nichts erfunden)."""
    if not geliefert('livre'):
        return []
    try:
        f = json.load(open(os.path.join(WZ, 'livre', 'livre.json'), encoding='utf-8')).get('farben') or []
        return [(x['n'], x['h'].lower()) for x in f if re.fullmatch(r'#[0-9a-fA-F]{6}', x.get('h', '')) and x.get('n') and x.get('g') not in ('heute', 'abende', 'dc')][:12]   # Hausfarben ohne Plakatfarben und Dirty-Chicken-Violett (Le Livre 28.10.2026)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return []


# ---------------------------------------------------------------- Seite
# Demo-Check 21.10.2026 (wie am Schlössli): Gastgeber, Hausbuch und Besucherbuch verlinken «Die Stube» über ihren eigenen Server
# (9064/9065/9066 …/_werkzeuge/maison/). Dort fehlen die Stand-Wege (/_weiter/…), die Stube stand ohne Zahlen. Lokal geht sie deshalb immer auf ihren Server,
# und zwar unter 127.0.0.1 (die Werkstatt verlinkt localhost:9061, sonst wäre der Merker «Zur Werkbank» in einem anderen Speicher).
ZUR_STUBE = (f'<script>if(/^(127\\.0\\.0\\.1|localhost)$/.test(location.hostname)&&(location.port!=="{PORT}"||location.hostname!=="127.0.0.1"))'
             f'location.replace("http://127.0.0.1:{PORT}"+location.pathname+location.search+location.hash)</script>\n')


def seite(online, v):
    Bau.online = online
    UI.clear()
    A = wege(online)
    auf = {k: A[k]['auf'] for k in REIHE}
    web = '/index.html'      # lokal liefert server.py die Website des Hauses in der Wurzel aus, online liegt sie in derselben Wurzel

    insel = ''.join(f'<a class="m-insel__p" href="#{k}"><span class="rl">{e(W[k]["name"])}</span></a>' for k in REIHE)
    band = ''.join(f'<li>{e(t)}</li><li class="p" aria-hidden="true"></li>' for t in [W[k]['name'] for k in REIHE] + [NAME, BAR, STRASSE, PLZ_ORT])

    fb = farben()
    farbreihe = (f'<ul class="m-farben" aria-label="Die Farben des Hauses" style="--n:{len(fb)}">' +
                 ''.join(f'<li data-r style="--i:{min(i, 4)};--c:{hx}"><i></i><b>{e(nm)}</b><span>{hx.upper()}</span></li>' for i, (nm, hx) in enumerate(fb)) + '</ul>') if fb else ''

    def zwei(a, b):
        return f'<div class="m-schirme{" m-schirme--zwei" if b else ""}">{a}{b}</div>'

    saele = f'''
<section class="m-saal tapete" id="bureau">
  <div class="innen">
  {saal_kopf('bureau', 0)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('bureau', 'bureau', f'{ZENTRALE} · {W["bureau"]["name"]} · Übersicht', W['bureau']['name'] + ': die Übersicht mit allen Bereichen der Website', 0), '')}{stuecke('bureau')}</div>
    <div>
      {tafel('bureau', 1)}
      <div class="m-tafel m-tafel--stand" data-r style="--i:2;margin-top:18px">
        <div class="m-zahlen"><div class="m-zahl"><b data-zahl="bereiche">–</b><span>Bereiche</span></div><div class="m-zahl"><b data-zahl="seiten">–</b><span>Seiten</span></div></div>
        <p class="m-tafel__stand" data-stand="bureau">&nbsp;</p>
        {knopf(W['bureau']['name'] + ' öffnen', auf['bureau'], 'knopf--dunkel')}
      </div>
    </div>
  </div>
  </div>
</section>

<section class="m-saal dunkel" id="carte">
  <div class="innen">
  {saal_kopf('carte', 1)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('carte', 'carte', f'{ZENTRALE} · {W["carte"]["name"]}', W['carte']['name'] + ': links die Gerichte, rechts die Karte, wie sie gedruckt wird', 0), '')}{stuecke('carte')}</div>
    <div>
      {tafel('carte', 1)}
      <div data-r style="--i:2;margin-top:22px">
        <div class="m-zahlen"><div class="m-zahl"><b data-zahl="karten">–</b><span>Karten</span></div><div class="m-zahl"><b data-zahl="entwurf">–</b><span>Offene Entwürfe</span></div></div>
        <p style="margin-top:22px">{knopf(W['carte']['name'] + ' öffnen', auf['carte'])}</p>
      </div>
    </div>
  </div>
  </div>
</section>

<section class="m-saal papier" id="imprimerie">
  <div class="innen">
  {saal_kopf('imprimerie', 2)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('imprimerie', 'imprimerie', f'{ZENTRALE} · {W["imprimerie"]["name"]}', W['imprimerie']['name'] + ': die Übersicht mit den Vorlagen des Hauses', 0), '')}{stuecke('imprimerie')}</div>
    <div>
      {tafel('imprimerie', 1)}
      <div data-r style="--i:2;margin-top:22px">{knopf(W['imprimerie']['name'] + ' öffnen', auf['imprimerie'], 'knopf--dunkel', neu=True)}<p class="m-hinweis" data-stand="imprimerie-kurz">&nbsp;</p></div>
    </div>
  </div>
  </div>
</section>

<section class="m-saal dunkel" id="reception">
  <div class="innen">
  {saal_kopf('reception', 3)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('reception', 'reception', f'{ZENTRALE} · {W["reception"]["name"]} · Eingang', W['reception']['name'] + ': Eingang mit den Anfragen und was Gäste gefragt haben', 0), '')}{stuecke('reception')}</div>
    <div>
      {tafel('reception', 1, '<p class="m-tafel__stand" data-stand="reception">&nbsp;</p>')}
      <p data-r style="--i:2;margin-top:22px">{knopf(W['reception']['name'] + ' öffnen', auf['reception'])}</p>
    </div>
  </div>
  </div>
</section>

<section class="m-saal tapete" id="livre">
  <div class="innen">
  {saal_kopf('livre', 4)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('livre-fotos', 'livre', f'{ZENTRALE} · {W["livre"]["name"]} · Fotos', W['livre']['name'] + ': die Fotos des Hauses', 0), schirm('livre-marke', 'livre', f'{ZENTRALE} · {W["livre"]["name"]} · Logo & Dateien', W['livre']['name'] + ': Wortmarke und Farben als Dateien', 1, '(max-width:1000px) 92vw, 30vw') if 'schirm-livre-marke' in BILDER else '')}{stuecke('livre')}</div>
    <div>
      {tafel('livre', 1)}
      <div data-r style="--i:2;margin-top:22px">{knopf(W['livre']['name'] + ' öffnen', auf['livre'], 'knopf--dunkel')}<p class="m-hinweis" data-stand="livre">&nbsp;</p></div>
    </div>
  </div>
  {farbreihe}
  </div>
</section>

<section class="m-saal papier" id="registre">
  <div class="innen">
  {saal_kopf('registre', 5)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei(schirm('registre', 'registre', f'{ZENTRALE} · {W["registre"]["name"]} · Beispielwerte', W['registre']['name'] + ' mit Beispielwerten: Besuche je Tag, Herkunft und die meistbesuchten Seiten', 0), '')}{stuecke('registre')}</div>
    <div>
      {tafel('registre', 1)}
      <div class="m-tafel" data-r style="--i:2;margin-top:18px">
        <div class="m-zahlen"><div class="m-zahl"><b data-zahl="reg-besuche">–</b><span>Besuche</span></div><div class="m-zahl"><b data-zahl="reg-seiten">–</b><span>Seiten angesehen</span></div><div class="m-zahl"><b data-zahl="reg-laender">–</b><span>Länder</span></div></div>
        <p class="m-hinweis" data-stand="besuche">&nbsp;</p>
        {knopf(W['registre']['name'] + ' öffnen', auf['registre'], 'knopf--dunkel')}
        <p class="m-hinweis">Gezählt ohne Cookies, nie mit Namen.</p>
      </div>
    </div>
  </div>
  <ol class="m-weg" data-r data-seite="{e(STUFE_SEITE)}" style="--n:4;margin-top:clamp(36px,4vw,56px)">
    <li style="--i:0"><b data-wg="besuche">–</b><span>Besuche</span><small data-wg="besuche-satz">letzte 30 Tage</small></li>
    <li style="--i:1"><b data-wg="fenster">–</b><span>{e(STUFE[0])}</span><small data-wg="fenster-satz">&nbsp;</small></li>
    <li style="--i:2"><b data-wg="weiter">–</b><span>{e(STUFE[1])}</span><small data-wg="weiter-satz">&nbsp;</small></li>
    <li style="--i:3"><b aria-hidden="true">{zeichen("m-weg__z")}</b><span>{e(STUFE[2])}</span><small>{e(STUFE[3])}</small></li>
  </ol>
  </div>
</section>'''

    anl = [(W[k]['name'], A[k]['anl']) for k in REIHE if A[k]['anl']]
    anleitungen = ''.join(f'<a href="{e(h)}" target="_blank" rel="noopener">{e(n)}, Schritt für Schritt</a>' for n, h in anl) or \
        '<span class="m-fuss__leer">Die Anleitungen kommen mit den Werkzeugen.</span>'
    pw = '' if online or not geliefert('bureau') else ((stand_wege().get('bureau') or {}).get('pruefung') or '')
    pruef = knopf('Prüfung öffnen', pw, 'knopf--klein') + ' ' if pw else ''   # R04: Prüfung des Schaufensters, nur lokal (online nur «Neu laden»)
    pkt = '<span class="rw-pkt" aria-hidden="true">·</span>'

    def fenster(i, k):
        f, pos, pos_h = FENSTER[k]; b = BILDER['fenster-' + k + '-900']
        art, rest = (W[k]['name'].split(' ', 1) + [''])[:2]     # «Das» · «Schaufenster»: der Artikel steht in einer eigenen Zeile, die Namen stehen auf einer Grundlinie
        return (f'<li class="hz-z"><a class="m-f5__k" style="--i:{i};--pos:{pos};--pos-h:{pos_h};--farbe:{FARBE[k]}" href="{e(auf[k] or "#" + k)}" data-taste="{i + 1}">'
                f'<picture><source media="(max-width:800px)" srcset="img/fenster-{k}-band.webp {BILDER["fenster-" + k + "-band"][0]}w" sizes="100vw">'
                f'<img src="img/fenster-{k}-900.webp" srcset="img/fenster-{k}-600.webp 600w, img/fenster-{k}-900.webp 900w" sizes="20vw" '
                f'width="{b[0]}" height="{b[1]}" alt="{e(alt(f))}" decoding="async" fetchpriority="high" onload="this.classList.add(\'da\')"></picture>'
                f'<span class="m-f5__t"><span class="m-f5__w">{e(ROLLE_K[k])}</span><b><span class="m-f5__art">{e(art)}</span> {e(rest)}</b><small data-stand="{k}-kurz">{e(KURZ[k])}</small>'
                f'<i class="m-f5__p" aria-hidden="true">{PF}</i></span></a></li>')

    # Empfang: die Fenster, darüber in der Mitte der Kopf (Wortmarke, Adresse, Name der Zentrale gross auf dem Horizont, Gruss, Datum) und die
    # Zahlenzeile der Besucherliste (Taste 6): heute Besuche auf der Website und wie viele davon weiter zur Reservation gingen. Getrennt mit «·»;
    # «Beispiel» leise in der Datumszeile.
    reg = auf['registre']
    # Zeile in zwei Teilen (Zahlen, Weg): am Handy steht der Weg in einer eigenen Zeile
    zeile = (f'<div class="m-f5__zeile"><p class="m-f5__heute"><span>Heute</span><b data-stand="registre-heute">–</b>Besuche{pkt}<b data-stand="registre-buchung">–</b>zur Reservation</p>{pkt}'
             + (f'<div class="hz-z"><a href="{e(reg)}" data-taste="6">{e(W["registre"]["name"])} öffnen{PF}</a></div>' if reg else f'<div class="hz-z"><a href="#registre" data-taste="6">{e(W["registre"]["name"])}{PF}</a></div>') + '</div>')
    by = HAUS.get('by') or ''
    empfang = (f'<section class="m-empfang m-f5" id="oben">'
               f'<nav class="m-f5__reihe" aria-label="Alle Werkzeuge"><ol class="hz-tafel">{"".join(fenster(i, k) for i, k in enumerate(REIHE[:5]))}</ol></nav>'
               f'<div class="m-f5__oben">{wortmarke("m-f5__wm")}<p class="m-f5__ort">' + (f'<span class="m-f5__by">{e(by)}</span><span class="m-f5__pkt">{pkt}</span>' if by else '') +
               f'<span>{e(STRASSE)}</span>{pkt}<span>{e(PLZ_ORT)}</span></p>'
               f'<h1 class="m-f5__titel">{e(ZENTRALE)}</h1>'
               f'<p class="m-f5__gruss"><span id="gruss">Guten Tag.</span> Womit fangen wir heute an?</p>'
               f'<p class="m-f5__datum"><span id="datum">&nbsp;</span><span class="rw-kopf__bsp" hidden>{pkt}Besuchszahlen als Beispiel</span></p>'
               f'{zeile}</div></section>')

    vorladen = '\n'.join(f'<link rel="preload" as="image" href="img/fenster-{k}-900.webp" imagesrcset="img/fenster-{k}-600.webp 600w, img/fenster-{k}-900.webp 900w" '
                         f'imagesizes="20vw" media="(min-width:801px)" fetchpriority="high">\n'
                         f'<link rel="preload" as="image" href="img/fenster-{k}-band.webp" media="(max-width:800px)" fetchpriority="high">' for k in REIHE[:5])
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
{'' if online else ZUR_STUBE}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(ZENTRALE)} · {e(NAME)}</title>
<meta name="description" content="Alle Werkzeuge der {e(NAME)} an einem Ort: {', '.join(W[k]['name'] for k in REIHE)}.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0b1d3d">
<link rel="icon" href="img/zeichen.svg" type="image/svg+xml">
<link rel="stylesheet" href="maison.css?v={v['maison.css']}">
{vorladen}
<script src="fehler.js?v={v['fehler.js']}"></script>
</head>
<body class="ma">
<div class="m-tuer" id="tuer" role="alert" hidden><p class="m-tuer__t">{e(ZENTRALE)} startet nicht.</p><p id="tuer-t">&nbsp;</p>{pruef}<a class="knopf knopf--klein" href=""><span class="knopf__t">Neu laden</span><i>{PF}</i></a></div>

<header class="m-oben">
  <a class="knopf knopf--klein m-oben__ecke m-oben__ecke--l" href="#fuss"><span class="knopf__t">Anleitungen</span><i>{PF}</i></a>
  <nav class="m-insel" aria-label="Werkzeuge">
    <a class="m-ecke" href="#oben"><span class="m-ecke__ring">{zeichen("m-ecke__z")}</span><span class="m-ecke__t"><b>{e(ZENTRALE)}</b><small>Alle Werkzeuge · {e(NAME)}</small></span></a>
    <span class="m-insel__wege">{insel}</span>
  </nav>
  <a class="knopf knopf--klein m-oben__ecke" href="{web}" target="_blank" rel="noopener"><span class="knopf__t">Website ansehen</span><i>{PF}</i></a>
</header>

<main>
{empfang}

<div class="m-band" data-laufband aria-hidden="true"><ul>{band}{band}</ul></div>
{saele}
</main>

<footer class="m-fuss tapete" id="fuss">
  <div class="m-fuss__platte" data-r>
    <div class="m-fuss__marke">{zeichen("m-fuss__z")}{wortmarke("m-fuss__wm")}</div>
    <div class="m-fuss__spalte"><p class="m-fuss__k">Das Haus</p><p>{e(NAME)} <span class="m-nb">mit der {e(BAR)}</span></p><p>{e(STRASSE)}, <span class="m-nb">{e(PLZ_ORT)}</span></p><p class="m-nb">{e(HAUS.get('telefon') or '')}</p><a href="{web}" target="_blank" rel="noopener">Website ansehen</a></div>
    <div class="m-fuss__spalte"><p class="m-fuss__k">Anleitungen</p>{anleitungen}</div>
    <div class="m-fuss__spalte"><p class="m-fuss__k">Fragen</p><p>Robert Reff · Tasty Studios</p><p>robert@tasty-studios.de</p></div>
  </div>
</footer>

<script type="application/json" id="maison-wege">{json.dumps({k: A[k]['stand'] for k in REIHE})}</script>
<script type="application/json" id="maison-beispiel">{json.dumps([k for k in REIHE if (stand_wege().get(k) or {}).get('beispiel')])}</script>
<script src="maison.js?v={v['maison.js']}"></script>
<script src="zur-werkbank.js?v={v['zur-werkbank.js']}" defer data-zw></script>
<script src="rundgang.js?v={v['rundgang.js']}" defer data-werkzeug="maison"></script>
</body>
</html>
'''


def knoepfe():
    """Jeder «Knopf-Name» aus den Tafeln muss im Code des Werkzeugs vorkommen (M20). Ordner aus stand_wege.json → code, sonst _werkzeuge/<werkzeug>."""
    fehlt = []
    sw = stand_wege()
    for k, n in sorted(set(UI)):
        code = (sw.get(k) or {}).get('code') or [os.path.join(WZ, k)]
        n = html.unescape(n)
        gefunden = False
        for o in code:
            for wurzel, _, dateien in os.walk(os.path.expanduser(o)):
                if any(t in wurzel for t in ('/online', '/pruefung', '/node_modules', '/_qa', '/_sicherung')):
                    continue
                for d in dateien:
                    if d.endswith(('.js', '.html', '.py')):
                        try:
                            if n.lower() in open(os.path.join(wurzel, d), encoding='utf-8', errors='ignore').read().lower():
                                gefunden = True; break
                        except OSError:
                            pass
                if gefunden:
                    break
            if gefunden:
                break
        if not gefunden:
            fehlt.append(f'{W[k]["name"]}: «{n}»')
    return fehlt


FEHLER_JS = r'''document.documentElement.classList.add('js');   /* Bewegung nur mit Skript; als Datei statt eingebettet (Sicherheitsregel online) */
/* Fehlermelder (R03), vor allem anderen: Skriptfehler in den Browser (KURZ_werkzeuge_fehler) und an den Server-Teil (studio/api/fehler, wenn es ihn gibt).
   Netzfehler nie melden, höchstens 20 je Seite, eigener Fehlschlag wird nicht erneut gemeldet. */
(function(){var zahl=0;function merk(t){t=String(t);window.MAISON_FEHLER=t;if(++zahl>20||/Load failed|access control|abort|NetworkError|Failed to fetch/i.test(t))return;
try{var a=JSON.parse(localStorage.getItem('KURZ_werkzeuge_fehler')||'[]');a.unshift({zeit:new Date().toISOString(),art:'maison',text:('Zentrale: '+t).slice(0,400),ort:location.pathname});localStorage.setItem('KURZ_werkzeuge_fehler',JSON.stringify(a.slice(0,30)))}catch(e){}
try{fetch('/studio/api/fehler',{method:'POST',headers:{'Content-Type':'application/json','X-Studio':'1'},body:JSON.stringify({text:('Zentrale · '+t).slice(0,600)}),keepalive:true}).catch(function(){})}catch(e){}}
window.addEventListener('error',function(e){if(e.target&&e.target.tagName==='SCRIPT'){window.MAISON_FEHLER='Die Datei '+e.target.getAttribute('src').split('?')[0]+' liess sich nicht laden.';return}merk((e.message||'Fehler')+' · '+(e.filename||'').split('/').pop()+':'+(e.lineno||''))},true);
window.addEventListener('unhandledrejection',function(e){merk('Versprechen: '+((e.reason&&e.reason.message)||e.reason))});
/* Startfehler-Tür (R04): ist maison.js beim Laden nicht durchgelaufen, sagt die Seite es und zeigt alles ohne Bewegung. Wache nach 12 s. */
function tuer(){if(window.MAISON_BEREIT)return;var t=document.getElementById('tuer');if(!t||!t.hidden)return;
document.documentElement.classList.remove('js');document.getElementById('tuer-t').textContent=window.MAISON_FEHLER||'Das Programm der Seite ist nicht durchgelaufen.';t.hidden=false}
window.addEventListener('load',tuer);setTimeout(tuer,12000);})();
'''.replace('KURZ_', KURZNAME + '_')


def rundgang():
    s = open(os.path.join(QUELLE, 'rundgang-vorlage.js'), encoding='utf-8').read()
    a = s.index('  var GAENGE = {'); b = s.index('\n  };', a) + 4
    namen = ', '.join(W[k]['name'] for k in REIHE[:5])
    die = ZENTRALE[0].lower() + ZENTRALE[1:]
    gang = f'''  var GAENGE = {{
    maison: {{ name: '{ZENTRALE}', schritte: [
      {{ ziel: ['.m-f5__titel', '#oben'], oben: true, titel: 'Das ist {die}',
        text: 'Der Eingang zu allen Werkzeugen des Hauses. Von hier aus pflegen Sie Website, Karten, Drucksachen, den Chat und die Marke selbst.' }},
      {{ ziel: ['.hz-z:first-child a', '.hz-tafel'], titel: 'Ein Fenster je Werkzeug',
        text: '{namen}. Darunter steht, was dort gerade ansteht. Ein Klick oder die Taste 1 bis 6 öffnet es.' }},
      {{ ziel: ['.m-f5__zeile'], titel: 'Heute auf der Website',
        text: 'Wer heute auf der Website war und wer von dort weiter zur Reservation ging. Ein Klick öffnet {W["registre"]["name"][0].lower() + W["registre"]["name"][1:]}.' }},
      {{ ziel: ['.m-insel', '.m-oben'], oben: true, titel: 'Immer erreichbar',
        text: 'Ein Klick auf diese Leiste bringt Sie von überall zurück zu den Werkzeugen. Aus jedem Werkzeug kommen Sie hierher zurück.' }},
      {{ ziel: ['#bureau .m-saal__kopf', '#bureau'], titel: 'Jedes Werkzeug stellt sich vor',
        text: 'Weiter unten zeigt jedes Werkzeug, was es für das Haus tut, mit Bildern aus dem Werkzeug selbst.' }}
    ] }}
  }};'''
    s = s[:a] + gang + s[b:]
    s = s.replace("'rundgang-bg-'", f"'rundgang-{KURZNAME}-'")
    # Titel der Karte wie die Titel des Hauses: Open Sans 400 in Versalien gesperrt (die Vorlage setzt danach letter-spacing:0 / text-transform:none)
    s = s.replace('.rdg-karte h3{margin:12px 0 6px;font:600 26px/1.1 "Barlow Semi","Arial Narrow",sans-serif;color:#2c3136;letter-spacing:0}',
                  '.rdg-karte h3{margin:12px 0 6px;font:400 19px/1.25 "Open Sans",Arial,sans-serif;color:#2c3136;letter-spacing:.08em;text-transform:uppercase}')
    s = s.replace('.rdg-karte h3{font:600 26px/1.1 "Barlow Semi","Arial Narrow",sans-serif!important;letter-spacing:0!important;text-transform:none!important}',
                  '.rdg-karte h3{font:400 19px/1.25 "Open Sans",Arial,sans-serif!important;letter-spacing:.08em!important;text-transform:uppercase!important}')
    s = s.replace('font:600 26px/1.1 "Barlow Semi","Arial Narrow",sans-serif','font:400 21px/1.2 "Open Sans",Arial,sans-serif;letter-spacing:.1em;text-transform:uppercase')
    s = s.replace('font:600 18px/1 "Barlow Semi","Arial Narrow",sans-serif', 'font:400 15px/1.1 "Open Sans",Arial,sans-serif;letter-spacing:.1em;text-transform:uppercase')
    s = s.replace('"Barlow Semi","Arial Narrow",sans-serif', '"Open Sans",Arial,sans-serif')
    for alt_, neu in (('#2c3136', '#0A2552'), ('#485056', '#113d88'), ('#1d2224', '#0b1d3d'), ('#7c8386', '#0F3678'), ('#e9ecec', '#F3F6F9'),
                      ('#d6bb96', '#C5D2E1'), ('#b7a27a', '#A2B6CF'), ('#e3cd98', '#C5D2E1'), ('227,205,152', '197,210,225'), ('#f7e9c6', '#EAEFF5'),
                      ('#b99a5c', '#A9BAD0'), ('#fffdf9', '#ffffff'), ('#f7f1e5', '#F3F6F9'), ('#f4ecdc', '#EEF2F6'), ('210,191,152', '162,182,207'),
                      ('130,108,53', '15,54,120'), ('10,12,22', '4,16,35'), ('10,13,26', '4,16,35'), ('26,29,40', '4,16,35'), ('27,32,51', '4,16,35')):
        s = s.replace(alt_, neu)
    s = re.sub(r'^/\*[^\n]*\*/\n', '', s, count=1)
    if re.search(r'Barlow|Cormorant|Cinzel|Gasterntal|Fenster ist|#2c3136|#485056', s):
        raise SystemExit('rundgang.js: Angabe der Vorlage übrig')
    return f'/* Rundgang (R18, M11): Kopie des Werkzeugs der Häuser, Gang für {ZENTRALE} der {NAME}; gebaut von _werkzeuge/maison/bau.py */\n' + s


def zur_werkbank():
    s = open(os.path.join(QUELLE, 'zur-werkbank-vorlage.js'), encoding='utf-8').read()
    s = re.sub(r'^/\*[^\n]*Gasterntal[^\n]*\*/\n', '', s)
    if "var SCHL = 'bg-wb';" not in s:
        raise SystemExit('zur-werkbank.js: Schlüssel nicht gefunden')
    s = s.replace("var SCHL = 'bg-wb';", f"var SCHL = '{KURZNAME}-wb';").replace('«bg-wb»', f'«{KURZNAME}-wb»')
    s = s.replace('linear-gradient(180deg,#485056,#1d2224)', 'linear-gradient(180deg,#113d88,#0b1d3d)')
    s = s.replace("'assets/schrift/DMMono-normal-400.woff2'", "'assets/fonts/DMMono-normal-400.woff2'")   # Schriften der Website liegen unter /assets/fonts/
    if 'assets/schrift' in s:
        raise SystemExit('zur-werkbank.js: Weg assets/schrift übrig')
    return f'/* «Zur Werkbank» (R19) · {ZENTRALE} der {NAME}: Kopie des Bausteins der Häuser, Schlüssel des Hauses «{KURZNAME}-wb». Gebaut von bau.py. */\n' + s


def ohne_fremde(t):
    """Angaben anderer Häuser gehen nicht in die Ausgabe (F29)."""
    m = re.search(r'.{0,40}(?:Rivage|\bgbr\b|Carlton|Interlaken|Doldenhorn|Ruedihus|Gasterntal|Kandersteg|Selden|Culinarium|Hannover|Linden|Momo|Rudi\b|Derya|Wild Side|wildside|'
                  r'Fraunces|Urbanist|Prata|Hanken|assets/schrift|assets/bild|assets/zeichen|EF7649|F5A689|B15736|16141B|16151A|3A3845|8953A9|Barlow|Cormorant|Cinzel|\bbg-wb\b|Tresen|Pairing|Plakatwerkstatt|Plakatarchiv|Gästebuch).{0,40}', t, re.I | re.S)
    if m:
        raise SystemExit('Angabe eines anderen Hauses in der Ausgabe: ' + m.group(0))
    return t


def baue():
    teile = {
        'maison.css': open(os.path.join(QUELLE, 'maison.css'), encoding='utf-8').read(),
        'maison.js': open(os.path.join(QUELLE, 'maison.js'), encoding='utf-8').read(),
        'rundgang.js': rundgang(),
        'fehler.js': FEHLER_JS,
        'zur-werkbank.js': zur_werkbank(),
    }
    v = {n: hashlib.sha1(t.encode()).hexdigest()[:10] for n, t in teile.items()}   # M20: Fassung aus dem Inhalt
    for online in (False, True):
        ziel = os.path.join(HIER, 'online') if online else HIER
        os.makedirs(ziel, exist_ok=True)
        bilder(ziel)
        open(os.path.join(ziel, 'img', 'zeichen.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#0b1d3d"/>'
                                                                                  f'<svg x="17" y="7" width="30" height="50" viewBox="{ZEICHEN_VB}" fill="#C5D2E1">{ZEICHEN}</svg></svg>')   # die Zeiger auf Nacht über dem See
        for n, t in teile.items():
            open(os.path.join(ziel, n), 'w', encoding='utf-8').write(ohne_fremde(t) if n != 'zur-werkbank.js' else t)
        s = ohne_fremde(seite(online, v))
        if online and re.search(r'localhost|127\.0\.0\.1|data-platz|/_weiter/', s):
            raise SystemExit('Online-Fassung enthält localhost oder Platzhalter')
        open(os.path.join(ziel, 'index.html'), 'w', encoding='utf-8').write(s)
    fk = knoepfe()
    os.makedirs(os.path.join(HIER, 'pruefung'), exist_ok=True)
    json.dump({k: dict(teil=TEIL[k], da=geliefert(k), adresse=wege(False)[k]['auf']) for k in REIHE},
              open(os.path.join(HIER, 'pruefung', 'adressen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{ZENTRALE} gebaut: _werkzeuge/maison/index.html + online/index.html · {len([b for b in BILDER if b.startswith("schirm")])} Bildschirme')
    print('  vorliegend:', ', '.join(f'{W[k]["name"]} {"ja" if geliefert(k) else "–"}' for k in REIHE))
    if FEHLT:
        print('  noch ohne Bildschirm:', ', '.join(FEHLT))
    if fk:
        print('  Knopf-Namen nicht im Code gefunden:', '; '.join(fk))


if __name__ == '__main__':
    baue()
