#!/usr/bin/env python3
"""Die Stube (La Maison) der Wirtschaft am Schlössli, Bottighofen (19.10.2026, Station 11, Teil «zentrale»).
Funktion, Bedienung und Technik wie die Stube des Berghotel Gasterntal und La Maison der anderen Häuser (Master Werkzeug-Bau 4.1, M01 bis M27,
R03, R04, R18, R19); Kleid und Empfang eigen für dieses Haus.

  python3 _werkzeuge/maison/bau.py      baut beide Fassungen aus einem Lauf (M13):
      _werkzeuge/maison/index.html …       lokal, über server.py (http://127.0.0.1:8987/_werkzeuge/maison/)
      _werkzeuge/maison/online/…           online-Fassung (nichts wird hochgeladen; Wege ohne localhost)

Empfang «Am Horizont»: Der Horizont des Sees ist die Ordnung der Website des Hauses (marke.json → darstellungsidee). Links gross der Rahmen,
in Ruhe die Terrasse über dem See, beim Darüberfahren die echte Vorschau des Werkzeugs (M23); rechts die sechs Werkzeuge als ruhige Zeilen,
die Tafel sitzt mit ihrer oberen Linie auf dem Horizont des Ruhebilds. Schirmrot nur als Punkt an der gewählten Zeile.

Was ein Werkzeug liefert (Adresse, Bildschirm, Stand-Weg, Knopf-Namen), liest der Bau erst, wenn sein Teil in der Kette «liegt vor» oder
«bestätigt» meldet (_kette/11-werkbank/werkzeuge/<teil>/stand.json). Bis dahin: Satz ohne Zahl, Tafel ohne Knopf-Namen, lokal ein beschrifteter
Platzhalter, online die Ruhe-Ansicht. Kundendaten (Name, Adresse, Fotos) nur aus der Website des Hauses gelesen, nie abgetippt."""
import glob, hashlib, html, json, os, re, shutil, sys, urllib.parse

e = html.escape
HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HIER))          # Projektordner des Hauses
WEB = os.path.join(ROOT, 'website')
KETTE = os.path.join(ROOT, '_kette')
QUELLE = os.path.join(HIER, 'quelle')
ROH = os.path.join(HIER, 'roh')
PORT = 8987                                             # Prüfserver der Stube (server.py)
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


# ---------------------------------------------------------------- Hauswerte, gelesen aus website/inhalt/haus.json und den Dateien der Website
HAUS = json.load(open(os.path.join(WEB, 'inhalt', 'haus.json'), encoding='utf-8'))
NAME, STRASSE, ORT = HAUS['name'], HAUS['strasse'], HAUS['ort']
BILDER_W = json.load(open(os.path.join(WEB, 'inhalt', 'bilder.json'), encoding='utf-8'))
MARKE = json.load(open(os.path.join(KETTE, '05-markenbauer', 'marke.json'), encoding='utf-8'))
if MARKE.get('welt') != 'land':
    raise SystemExit('marke.json: Welt ist nicht «land»')


def svg_innen(pfad):
    s = open(pfad, encoding='utf-8').read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    innen = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    return vb, re.sub(r'\s+', ' ', innen).strip()


ZEIGER_VB, ZEIGER = svg_innen(os.path.join(WEB, 'assets', 'svg', 'zeiger.svg'))       # die zwei Zeiger des Logos (Zeichen des Hauses)


# ---------------------------------------------------------------- Werkzeuge des Hauses
# Reihe wie in allen Häusern (Taste 1 bis 6 gleich). Namen und Rollen aus _Werkzeuge/stamm/welt.js, Welt Landhaus.
REIHE = ['bureau', 'carte', 'imprimerie', 'reception', 'livre', 'registre']
TEIL = {'bureau': 'website', 'carte': 'karten', 'imprimerie': 'druck', 'reception': 'gaeste', 'livre': 'marke', 'registre': 'besuche'}


def welt_namen():
    t = open(os.path.expanduser('~/Desktop/Website-Projekte/_Werkzeuge/stamm/welt.js'), encoding='utf-8').read()
    aus = {}
    for teil, land, tut in re.findall(r"(\w+): \{ grand: '[^']+', land: '([^']+)', tut: '([^']+)' \}", t):
        aus[teil] = (land, tut)
    return aus


WN = welt_namen()
# Namen der Werkzeuge fürs Schlössli: EINE Stelle für alle sieben Werkzeuge ist _werkzeuge/oberflaeche/kleid/schloessli.js (WO_HAUS.namen,
# Chef-Chat Kuchler 19.10.2026, Regel-Notiz Abschnitt 9). Hier nur gelesen, beim Bau. Fehlt dort einer, gilt der Landhaus-Name aus welt.js.
def haus_namen():
    t = open(os.path.join(ROOT, '_werkzeuge', 'oberflaeche', 'kleid', 'schloessli.js'), encoding='utf-8').read()
    m = re.search(r"namen:\s*\{([^}]*)\}", t)
    return dict(re.findall(r"(\w+):\s*'([^']+)'", m.group(1))) if m else {}


NAMEN = haus_namen()
STUBE = NAMEN.get('zentrale') or WN['zentrale'][0]
W = {k: dict(name=NAMEN.get(TEIL[k]) or WN[TEIL[k]][0], rolle=WN[TEIL[k]][1]) for k in REIHE}
DIE = lambda n: n[0].lower() + n[1:]                     # «das Hafenbüro» im Satz
KURZ = {'bureau': 'Website des Hauses', 'carte': 'Karten des Hauses', 'imprimerie': 'Vorlagen, druckfertig', 'reception': 'Anfragen und Fragen',
        'livre': 'Fotos, Dateien, Markenprüfung', 'registre': 'Besuche ohne Namen'}
# Satz je Saal: was das Werkzeug für dieses Haus tut (nur, was es gibt: Karten aus website/inhalt, Zeiten und Ferien aus haus.json)
SATZ = {
    'bureau': 'Die Website des Hauses zum Anfassen: Texte, Fotos, Öffnungs- und Küchenzeiten, Ferien und Hinweise, Seite für Seite.',
    'carte': 'Die Karten des Hauses, von der grossen Karte bis zur Lästermeile und zum Wein. Ein Knopf setzt die neue PDF, die Website folgt.',
    'imprimerie': 'Tischkarten, Aushänge, Gutscheine und Beiträge im Stil des Hauses, aus fertigen Vorlagen und ohne Grafikprogramm.',
    'reception': 'Reservationen, Bankette, Anlässe und Gutscheine aus den Formularen der Website, je mit einem Brief im Ton des Hauses. Dazu ein Chat, der Gästen aus Ihren Seiten und Karten antwortet.',
    'livre': 'Die Marke des Hauses zum Arbeiten, für Sie und für jede Agentur: Fotos, Wortmarke, Zeiger, Schriften und Farben.',
    'registre': 'Wer Ihre Website besucht: woher die Gäste kommen, was sie sich ansehen und wie oft es weiter zur Reservation geht.',
}


def kette_teil(k):
    """(zustand, adresse) des Werkzeugs aus der Kette."""
    p = os.path.join(KETTE, '11-werkbank', 'werkzeuge', TEIL[k], 'stand.json')
    try:
        j = json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        return '', ''
    return j.get('zustand') or '', j.get('adresse') or ''


def geliefert(k):
    return kette_teil(k)[0] in ('liegt vor', 'bestätigt')


# Stand-Weg je Werkzeug (Form fest, Master 4.1 «Stand-Wege»): relativ zur Adresse des Werkzeugs. Steht in stand_wege.json (vom Anpasser nach
# der Lieferung aus dem Werkzeug gelesen), sonst kein Weg. Lokal holt der Prüfserver der Stube sie über /_weiter/<werkzeug>/… (ein Browser liest
# nicht quer über Ports); online nur, wenn das Werkzeug online einen Weg hat.
def stand_wege():
    p = os.path.join(HIER, 'stand_wege.json')
    try:
        return json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def wege(online):
    sw = stand_wege()
    aus = {}
    for k in REIHE:
        z, adr = kette_teil(k)
        d = sw.get(k) or {}
        if online:
            auf = d.get('online') or '../werkbank/index.html#werkzeuge'
            stand = d.get('stand_online') or ''
        else:
            auf = adr if geliefert(k) and adr else ''
            stand = [f'/_weiter/{k}/' + x.lstrip('/') for x in ([d['stand']] if isinstance(d.get('stand'), str) else d.get('stand') or [])] if geliefert(k) else []
        aus[k] = dict(auf=auf, stand=stand, anl=(d.get('anleitung_online') if online else d.get('anleitung')) or '')
    return aus


# ---------------------------------------------------------------- Bilder
BILDER = {}
FEHLT = []


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


# Ruhe-Ansicht: die Terrasse über dem See am Mittag (Startbild der Website), 16 : 10 geschnitten, Horizont aus bilder.json
RUHE_Q = os.path.join(WEB, 'assets', 'img', 'start-2400.webp')
RUHE_HZ_Q = BILDER_W['start']['hz']                      # 0,305 der Höhe im Original 3 : 2


def ruhe_crop():
    from PIL import Image
    w, h = Image.open(RUHE_Q).size
    ch = round(w * 10 / 16)
    hz = RUHE_HZ_Q * h
    y0 = max(0, min(h - ch, round(hz - ch * 0.30)))      # Horizont bei 30 % der Höhe des Rahmens
    return (0, y0, w, y0 + ch), (hz - y0) / ch


# Fotos aus dem Bildarchiv für dessen Saal (nur Fotos des Hauses, art «haus» in livre.json; keine Menschen angeschnitten, nichts vom Schwesterhaus)
ARCHIV = ['glas', 'iberia', 'regal', 'anguria', 'abend', 'dessert']
SCHIRME = {'bureau': ['bureau', 'bureau-2'], 'carte': ['carte'], 'imprimerie': ['imprimerie'], 'reception': ['reception'],
           'livre': ['livre-fotos', 'livre-marke'], 'registre': ['registre']}


# Foto des Hauses je Werkzeug (Kachel im Empfang), aus den Bildern der Website, 4 : 3 geschnitten
RAUM = {'bureau': 'haus', 'carte': 'tortelloni', 'imprimerie': 'schild', 'reception': 'gaststube', 'livre': 'platanen', 'registre': 'bootshafen'}
RAUM_G = (800, 600)


def raum_quelle(rk):
    for w in (1200, 900, 800):
        q = os.path.join(WEB, 'assets', 'img', f'{rk}-{w}.webp')
        if os.path.exists(q):
            return q
    raise SystemExit('Foto fehlt: ' + rk)


def bilder(ziel):
    BILDER.clear(); FEHLT.clear()
    crop, hz = ruhe_crop()
    webp(ziel, 'ruhe', RUHE_Q, 2000, 1000, 80, crop)
    for k in REIHE:
        for n in SCHIRME[k]:
            q = next((os.path.join(ROH, n + x) for x in ('.png', '.jpg', '.webp') if os.path.exists(os.path.join(ROH, n + x))), '')
            if not geliefert(k) or not q:
                FEHLT.append(n)
                continue
            webp(ziel, 'schirm-' + n, q, 2400, 1200, 84)
    from PIL import Image
    for k, rk in RAUM.items():
        q = raum_quelle(rk)
        for name, (bw, bh) in ((f'raum-{k}', RAUM_G), (f'raum-{k}-s', (480, 360))):
            z = os.path.join(ziel, 'img', name + '.webp')
            if not os.path.exists(z) or os.path.getmtime(z) < max(os.path.getmtime(q), os.path.getmtime(__file__)):
                im = Image.open(q).convert('RGB'); sk = max(bw / im.width, bh / im.height)
                im = im.resize((round(im.width * sk), round(im.height * sk)), Image.LANCZOS)
                hz = BILDER_W[rk].get('hz') or .5
                x = (im.width - bw) // 2; y = min(max(0, round(im.height * hz - bh * .5)), im.height - bh)
                im.crop((x, y, x + bw, y + bh)).save(z, quality=80, method=6)
    # Stücke der Säle: Karten aus Station 10 (roh/karten/*.png, aus _karten/pdf gerechnet), Fotos aus dem Bildarchiv, weitere Bildschirme
    if geliefert('imprimerie'):
        for q in sorted(glob.glob(os.path.join(ROH, 'druck', '*.png'))):   # Blätter aus ihren druckfertigen PDF (_werkzeuge/imprimerie/_qa/lauf/pdf)
            webp(ziel, 'druck-' + os.path.basename(q)[:-4], q, 1000, None, 84)
    for q in sorted(glob.glob(os.path.join(ROH, 'karten', '*.png'))):
        webp(ziel, 'karte-' + os.path.basename(q)[:-4], q, 1000, None, 84)
    if geliefert('livre'):
        for k in ARCHIV:
            webp(ziel, 'archiv-' + k, raum_quelle(k), 900, None, 80)
    for n in ('reception-chat',):
        q = os.path.join(ROH, n + '.png')
        if os.path.exists(q) and geliefert('reception'):
            webp(ziel, 'schirm-' + n, q, 2400, 1200, 84)
    # Tapeten der Website als gerechnetes Bild (quelle/tapete.js, doppelte Dichte): ein SVG-Muster kostete am Handy beim ersten Scrollen ein Bild über 33 ms
    from PIL import Image
    for art in ('dunkel', 'hell'):
        q = os.path.join(QUELLE, f'tapete-{art}@2x.png')
        if os.path.getmtime(q) < os.path.getmtime(os.path.join(WEB, 'assets', 'svg', f'tapete-a-{art}.svg')):
            raise SystemExit('Tapete der Website ist neuer: node _werkzeuge/maison/quelle/tapete.js')
        Image.open(q).save(os.path.join(ziel, 'img', f'tapete-{art}.webp'), lossless=True, method=6)
    os.makedirs(os.path.join(ziel, 'schrift'), exist_ok=True)
    for f in ('OpenSans-var.woff2', 'InstrumentSans-normal-400_600.woff2', 'DMMono-normal-400.woff2'):
        shutil.copyfile(os.path.join(WEB, 'assets', 'fonts', f), os.path.join(ziel, 'schrift', f))
    return hz


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


# Tafeln «So geht’s». ALLG ohne Knopf-Namen, solange das Werkzeug nicht vorliegt. HAUS (tafeln.json) mit den echten Knopf-Namen («…»), erst
# nach der Lieferung aus dem Code des Werkzeugs gelesen und beim Bau dagegen geprüft.
TAFEL_ALLG = {
    'bureau': [('stift', 'Text oder Foto ändern', 'Den Bereich wählen, in der Vorschau auf den Text oder das Foto klicken und ändern.'),
               ('uhr', 'Zeiten und Ferien', 'Öffnungs- und Küchenzeiten, Ruhetage und Ferien stehen untereinander. Einmal ändern, jede Stelle der Website folgt.'),
               ('waage', 'Erst Entwurf, dann online', 'Gespeichert ist erst ein Entwurf. Vorher und nachher nebeneinander ansehen, dann veröffentlichen.')],
    'carte': [('stift', 'Gericht oder Preis ändern', 'Die Karte wählen, das Gericht anklicken, Name, Beschreibung oder Preis überschreiben. Daneben steht sofort die Karte.'),
              ('liste', 'Neues Gericht', 'Bei der passenden Gruppe ein Gericht anfügen und an die richtige Stelle schieben.'),
              ('zurueck', 'Vorübergehend weg', 'Gibt es ein Gericht gerade nicht, nehmen Sie es heraus. Es bleibt gespeichert und kommt später zurück.'),
              ('pdf', 'Neue Karte drucken', 'Vorab eine Probe ansehen, dann veröffentlichen: die PDF wird neu gesetzt, die Karte auf der Website gleich mit.')],
    'imprimerie': [('satz', 'Sagen, was Sie brauchen', 'In einem Satz beschreiben, was gebraucht wird, oder eine fertige Vorlage mit Texten und Zeiten des Hauses nehmen.'),
                   ('fuenf', 'Einen Entwurf wählen', 'Es kommen mehrere Entwürfe im Stil des Hauses. Den passenden anklicken.'),
                   ('druck', 'Drucken', 'Druckfertig als PDF speichern, für die Druckerei oder den eigenen Drucker.')],
    'reception': [('blase', 'Gäste fragen im Chat', 'Auf jeder Seite der Website können Gäste fragen. Der Chat antwortet aus Ihren Seiten und Karten, in der Sprache des Gastes.'),
                  ('eingang', 'Anfragen beantworten', 'Ein Fest, eine Gruppe, ein Gutschein: jede Anfrage steht im Eingang, mit einem Entwurf für Ihre Antwort. Verschickt wird nur, was Sie selbst schicken.'),
                  ('liste', 'Lücken schliessen', 'Wusste der Chat etwas nicht, steht die Frage in einer eigenen Liste. Einmal nachtragen, ab dann antwortet er selbst.')],
    'livre': [('foto', 'Ein Foto holen', 'Ein Foto anklicken und die Grösse wählen: für Instagram, die Website oder den Druck.'),
              ('datei', 'Wortmarke weitergeben', 'Wortmarke, Zeiger, Farben und Schriften liegen als Dateien bereit, für Agentur oder Druckerei.'),
              ('farbe', 'Einen Entwurf prüfen', 'Plakat oder Flyer einer Agentur hineinziehen. Es sagt Punkt für Punkt, was zum Haus passt.')],
    'registre': [('karte', 'Woher die Gäste kommen', 'Länder und Orte der Besuche, ohne Cookies und nie mit Namen.'),
                 ('liste', 'Was sie sich ansehen', 'Die meistbesuchten Seiten und Karten, und wie lange die Gäste bleiben.'),
                 ('uhr', 'Weiter zur Reservation', 'Wie oft ein Besuch zum Reservieren, zum Anrufen oder zur Anfrage führt.')],
}


def tafel_zeilen(k):
    try:
        h = json.load(open(os.path.join(HIER, 'tafeln.json'), encoding='utf-8'))
    except (OSError, ValueError):
        h = {}
    return h.get(k) if geliefert(k) and h.get(k) else TAFEL_ALLG[k]


def tafel(k, i=0, extra=''):
    z = ''.join(f'<div class="m-tafel__z"><i>{I[s]}</i><p><b>{e(t)}</b>{ui(e(x, quote=False), k)}</p></div>' for s, t, x in tafel_zeilen(k))
    return f'<div class="m-tafel" data-r style="--i:{i}"><p class="m-tafel__kopf"><span>So geht’s</span></p>{z}{extra}</div>'


class Bau:
    online = False
    fassung = os.environ.get('MAISON_FASSUNG', 'a')   # Robert 19.10.2026: «a» (Sechs Bilder am Horizont)


def schirm(n, k, leiste, alt, i=0, sizes='(max-width:1000px) 92vw, 60vw'):
    name = 'schirm-' + n
    if name not in BILDER:
        if Bau.online:
            return ''
        return (f'<figure class="m-schirm m-schirm--platz" data-r="schweb" style="--i:{i}" data-platz="{e(n)}"><div class="m-schirm__leiste" aria-hidden="true"><span>{e(leiste)}</span></div>'
                f'<div class="m-platz">{zeiger("")}<b>Bildschirm folgt</b><p>{e(W[k]["name"])} wird gerade gebaut. Sobald es vorliegt, steht hier sein echter Bildschirm.</p>'
                f'<small>Platzhalter, nur lokal</small></div></figure>')
    b = BILDER[name]
    return (f'<figure class="m-schirm" data-r="schweb" style="--i:{i}"><div class="m-schirm__leiste" aria-hidden="true"><span>{e(leiste)}</span></div>'
            f'<img src="img/{name}.webp" srcset="img/{name}-s.webp 1200w, img/{name}.webp {b[0]}w" sizes="{sizes}" width="{b[0]}" height="{b[1]}" alt="{e(alt)}" loading="lazy" decoding="async"></figure>')


def stueck_bild(name, alt, cls='', i=0):
    if name not in BILDER:
        return ''
    w, h = BILDER[name]
    return (f'<figure class="m-stueck {cls}" data-r="schweb" style="--i:{i}"><img src="img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}" loading="lazy" decoding="async"></figure>')


def stuecke(k):
    """Weitere echte Bilder je Saal (Robert 19.10.2026 23:55: «die anderen Tools hatten … ein paar mehr Bilder … Das sah schöner aus»)."""
    t = ''
    if k == 'bureau':
        t = schirm('bureau-2', 'bureau', f'{STUBE} · {W["bureau"]["name"]} · Startseite', 'Eine Seite offen: links die Stellen, rechts die Startseite der Website', 1, '(max-width:1000px) 92vw, 40vw')
        return f'<div class="m-stuecke m-stuecke--eins">{t}</div>' if t and 'schirm-bureau-2' in BILDER else ''
    if k == 'carte':
        teile = [('karte-speisekarte-2', 'Speisekarte, Seite mit Frankreich und Italien', 'm-stueck--blatt'),
                 ('karte-lunch-1', 'Lunch-Menü, drei Gänge', 'm-stueck--quer'),
                 ('karte-laestermeile-2', 'Lästermeile, Tapas durchgehend und zur Stärkung', 'm-stueck--blatt')]
        t = ''.join(stueck_bild(n, a, c, i + 1) for i, (n, a, c) in enumerate(teile))
        return f'<div class="m-stuecke m-stuecke--karten">{t}</div>' if t else ''
    if k == 'imprimerie':
        teile = [('druck-flyer-001-1', 'Flyer aus der Hausdruckerei: Ihre Feier am Hafen', 'm-stueck--blatt'),
                 ('druck-gutschein-001-1', 'Gutschein aus der Hausdruckerei', 'm-stueck--quer'),
                 ('druck-einladung-001-1', 'Einladung aus der Hausdruckerei: Wir feiern', 'm-stueck--blatt')]
        t = ''.join(stueck_bild(n, a, c, i + 1) for i, (n, a, c) in enumerate(teile))
        return f'<div class="m-stuecke m-stuecke--karten">{t}</div>' if t else ''
    if k == 'reception':
        t = schirm('reception-chat', 'reception', f'{STUBE} · {W["reception"]["name"]} · Chat ausprobieren', 'Chat ausprobieren: so fragt ein Gast, mit Beispielfragen', 1, '(max-width:1000px) 92vw, 40vw')
        return f'<div class="m-stuecke m-stuecke--eins">{t}</div>' if 'schirm-reception-chat' in BILDER else ''
    if k == 'livre':
        t = ''.join(stueck_bild('archiv-' + n, BILDER_W[n]['alt'], 'm-stueck--foto', i + 1) for i, n in enumerate(ARCHIV))
        return f'<div class="m-stuecke m-stuecke--fotos">{t}</div>' if t else ''
    return ''


def zeiger(c):
    return f'<svg class="{c}" viewBox="{ZEIGER_VB}" fill="currentColor" aria-hidden="true">{ZEIGER}</svg>'


def knopf(t, href, cls='', neu=False):
    if not href:
        return f'<span class="m-hinweis">{e(t.replace("öffnen", "folgt"))}, sobald es vorliegt.</span>'
    z = ' target="_blank" rel="noopener"' if neu else ''
    return f'<a class="knopf {cls}" href="{e(href)}"{z}>{e(t)}<i>{PF}</i></a>'


def saal_kopf(k, nr):
    artikel, wort = W[k]['name'].split(' ', 1)
    return (f'<header class="m-saal__kopf">{zeiger("m-saal__z")}<p class="m-saal__nr" data-r style="--i:0">N° {nr + 1} von 6 · {e(W[k]["rolle"])}</p>'
            f'<h2 class="m-saal__titel" data-r style="--i:1"><em>{e(artikel)}</em> {e(wort)}</h2><p class="m-saal__satz" data-r style="--i:2">{e(SATZ[k])}</p></header>'
            f'<div class="m-saal__linie" aria-hidden="true"></div>')


def farben():
    """Farben des Hauses für den Saal des Hausbuchs: aus dessen livre.json (nur nach der Lieferung), sonst keine (nichts erfunden)."""
    if not geliefert('livre'):
        return []
    sw = stand_wege().get('livre') or {}
    p = sw.get('livre_json')
    if not p:
        return []
    try:
        f = json.load(open(os.path.join(ROOT, p), encoding='utf-8')).get('farben') or []
        return [(x['n'], x['h'].lower()) for x in f if re.fullmatch(r'#[0-9a-fA-F]{6}', x.get('h', '')) and x.get('n') and x.get('g') != 'heute'][:10]
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return []


# ---------------------------------------------------------------- Seite
# Demo-Check 21.10.2026: Die Werkzeuge verlinken «Das Hafenbüro» über ihren eigenen Server (9047/_werkzeuge/maison/ …). Dort fehlen die
# Stand-Wege (/_weiter/…), die Stube stand ohne Zahlen und mit Konsolenfehlern da. Lokal geht die Stube deshalb immer auf ihren Server.
ZUR_STUBE = (f'<script>if(/^(127\\.0\\.0\\.1|localhost)$/.test(location.hostname)&&location.port!=="{PORT}")'
             f'location.replace("http://127.0.0.1:{PORT}"+location.pathname+location.search+location.hash)</script>\n')


def seite(online, hz, v):
    Bau.online = online
    UI.clear()
    A = wege(online)
    auf = {k: A[k]['auf'] for k in REIHE}
    web = '/index.html' if online else '../../website/index.html'

    zeilen = ''.join(
        f'<li class="hz-z"><a href="{e(auf[k] or "#" + k)}" data-taste="{i + 1}">'
        f'<span class="hz-nr">N° {i + 1}</span><b class="hz-name">{e(W[k]["name"])}</b>'
        f'<span class="hz-was">{e(W[k]["rolle"])} · <span class="hz-stand" data-stand="{k}-kurz">{e(KURZ[k])}</span></span>'
        f'<span class="hz-ring" aria-hidden="true">{PF}</span></a></li>'
        for i, k in enumerate(REIHE))
    rb = BILDER['ruhe']
    vorschau = (f'<img class="hz-bild hz-bild--ruhe an" data-vorschau="ruhe" src="img/ruhe.webp" srcset="img/ruhe-s.webp 1000w, img/ruhe.webp {rb[0]}w" '
                f'sizes="(max-width:1000px) 100vw, 54vw" width="{rb[0]}" height="{rb[1]}" alt="{e(BILDER_W["start"]["alt"])}" decoding="async" fetchpriority="high">')
    unter = f'<span data-vorschau="ruhe" class="an">{e(NAME)} · {e(STUBE)}</span>'
    for i, k in enumerate(REIHE):
        n = 'schirm-' + SCHIRME[k][0]
        if n in BILDER:
            vorschau += (f'<img class="hz-bild hz-bild--schirm" data-vorschau="{i}" src="img/{n}.webp" srcset="img/{n}-s.webp 1200w, img/{n}.webp {BILDER[n][0]}w" '
                         f'sizes="(max-width:1000px) 100vw, 54vw" width="{BILDER[n][0]}" height="{BILDER[n][1]}" alt="Vorschau: {e(W[k]["name"])}" decoding="async" loading="lazy">')
            unter += f'<span data-vorschau="{i}">Vorschau · {e(W[k]["name"])}</span>'
        elif not online:
            vorschau += (f'<div class="hz-platz" data-vorschau="{i}" data-platz="{e(k)}"><div>{zeiger("m-saal__z")}<b>{e(W[k]["name"])}</b>'
                         f'Die Vorschau folgt, sobald das Werkzeug vorliegt.<small>Platzhalter, nur lokal</small></div></div>')
            unter += f'<span data-vorschau="{i}">{e(W[k]["name"])} · Vorschau folgt</span>'
    insel = ''.join(f'<a class="m-insel__p" href="#{k}"><span class="rl">{e(W[k]["name"])}</span></a>' for k in REIHE)
    band = ''.join(f'<li>{e(t)}</li><li class="p" aria-hidden="true"></li>' for t in [W[k]['name'] for k in REIHE] + [NAME, STRASSE, ORT])

    fb = farben()
    farbreihe = (f'<ul class="m-farben" aria-label="Die Farben des Hauses" style="--n:{len(fb)}">' +
                 ''.join(f'<li data-r style="--i:{min(i, 4)};--c:{hx}"><i></i><b>{e(nm)}</b><span>{hx.upper()}</span></li>' for i, (nm, hx) in enumerate(fb)) + '</ul>') if fb else ''

    def zwei(k, a, b):
        return f'<div class="m-schirme{" m-schirme--zwei" if b else ""}">{a}{b}</div>'

    saele = f'''
<section class="m-saal tapete" id="bureau">
  <div class="innen">
  {saal_kopf('bureau', 0)}
  <div class="m-saal__feld">
    <div class="m-saal__links">{zwei('bureau', schirm('bureau', 'bureau', f'{STUBE} · {W["bureau"]["name"]} · Übersicht', W['bureau']['name'] + ': ' + 'die Übersicht mit allen Bereichen der Website', 0), '')}{stuecke('bureau')}</div>
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
    <div class="m-saal__links">{zwei('carte', schirm('carte', 'carte', f'{STUBE} · {W["carte"]["name"]}', W['carte']['name'] + ': ' + 'links die Gerichte, rechts die Karte, wie sie gedruckt wird', 0), '')}{stuecke('carte')}</div>
    <div>
      {tafel('carte', 1)}
      <div data-r style="--i:2;margin-top:22px">
        <div class="m-zahlen"><div class="m-zahl"><b data-zahl="karten" style="color:#F2F5F8">–</b><span style="color:var(--himmel-h)">Karten</span></div><div class="m-zahl"><b data-zahl="entwurf" style="color:#F2F5F8">–</b><span style="color:var(--himmel-h)">Offene Entwürfe</span></div></div>
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
    <div class="m-saal__links">{zwei('imprimerie', schirm('imprimerie', 'imprimerie', f'{STUBE} · {W["imprimerie"]["name"]}', W['imprimerie']['name'] + ': ' + 'die Übersicht mit den Vorlagen des Hauses', 0), '')}{stuecke('imprimerie')}</div>
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
    <div class="m-saal__links">{zwei('reception', schirm('reception', 'reception', f'{STUBE} · {W["reception"]["name"]} · Eingang', W['reception']['name'] + ': ' + 'Eingang mit den Anfragen und was Gäste gefragt haben', 0), '')}{stuecke('reception')}</div>
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
    <div class="m-saal__links">{zwei('livre', schirm('livre-fotos', 'livre', f'{STUBE} · {W["livre"]["name"]} · Bildarchiv', W['livre']['name'] + ': ' + 'das Bildarchiv mit den Fotos des Hauses', 0), schirm('livre-marke', 'livre', f'{STUBE} · {W["livre"]["name"]} · Dateien', W['livre']['name'] + ': ' + 'Wortmarke, Zeiger und Farben als Dateien', 1, '(max-width:1000px) 92vw, 30vw') if 'schirm-livre-marke' in BILDER else '')}{stuecke('livre')}</div>
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
    {zwei('registre', schirm('registre', 'registre', f'{STUBE} · {W["registre"]["name"]} · Beispielwerte', W['registre']['name'] + ' mit Beispielwerten: Besuche je Tag, Herkunft und die meistbesuchten Seiten', 0), '')}
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
  <ol class="m-weg" style="--n:4;margin-top:clamp(36px,4vw,56px)">
          <li><b data-wg="besuche">–</b><span>Besuche</span><small data-wg="besuche-satz">auf der Website</small></li>
          <li><b data-wg="fenster">–</b><span>Fenster «Reservation» geöffnet</span><small data-wg="fenster-satz">&nbsp;</small></li>
          <li><b data-wg="weiter">–</b><span>weiter zu gastronovi oder als Anfrage ans Haus</span><small data-wg="weiter-satz">&nbsp;</small></li>
          <li><b aria-hidden="true">·</b><span>reserviert</span><small>zählen gastronovi und das Haus, nicht die Website</small></li>
        </ol>
  </div>
</section>'''

    anl = [(W[k]['name'], A[k]['anl']) for k in REIHE if A[k]['anl']]
    anleitungen = ''.join(f'<a href="{e(h)}" target="_blank" rel="noopener">{e(n)}, Schritt für Schritt</a>' for n, h in anl) or \
        '<span class="m-fuss__leer">Die Anleitungen kommen mit den Werkzeugen.</span>'
    wm_vb, wm = svg_innen(os.path.join(WEB, 'assets', 'svg', 'zeichen.svg'))
    reg_auf = auf['registre']
    pw = '' if online or not geliefert('bureau') else ((stand_wege().get('bureau') or {}).get('pruefung') or '')
    pruef = knopf('Prüfung öffnen', pw, 'knopf--klein') + ' ' if pw else ''   # R04: Prüfung des Schreibtischs, nur lokal (online nur «Neu laden»)

    zeile_heute = (f'<p class="m-zeile"><span>Heute</span><span><b data-stand="registre-heute">–</b>Besuche</span><i></i><span><b data-stand="registre-buchung">–</b>zur Reservation</span>'
                   f'<span class="m-zeile__bsp bsp" hidden>Beispiel</span><i></i>' + (f'<a href="{e(reg_auf)}">{e(W["registre"]["name"])} öffnen</a>' if reg_auf else f'<span>{e(W["registre"]["name"])} folgt</span>') + '</p>')
    hilfe = '<p class="m-hilfe">Ein Klick oder die Taste <kbd>1</kbd> bis <kbd>6</kbd> öffnet das Werkzeug. Darunter stellt sich jedes einzeln vor.</p>'
    rahmen = f'<figure class="hz-rahmen" style="--abbild:url({BILDER_W["start"].get("abbild", "")})">{vorschau}<figcaption class="hz-unter" aria-live="polite">{unter}</figcaption></figure>'
    kopf_links = (f'<div class="fk-kopf">{zeiger("fk-kopf__z")}<div><h1 class="fk-titel">{e(STUBE.split(" ", 1)[0])} <em>{e(STUBE.split(" ", 1)[1])}</em></h1>'
                  f'<p class="fk-gruss"><span id="gruss">Guten Tag.</span> Womit fangen wir heute an? <small id="datum">&nbsp;</small></p></div></div>')
    def kachel(i, k, cls):
        rk = RAUM[k]
        return (f'<li class="hz-z {cls}" style="--i:{i}"><a href="{e(auf[k] or "#" + k)}" data-taste="{i + 1}">'
                f'<span class="fk-b"><img src="img/raum-{k}.webp" width="{RAUM_G[0]}" height="{RAUM_G[1]}" alt="{e(BILDER_W[rk]["alt"])}" decoding="async"></span>'
                f'<small class="fk-nr">N° {i + 1}</small><b class="fk-name">{e(W[k]["name"])}</b><i class="fk-linie" aria-hidden="true"></i>'
                f'<span class="fk-was">{e(W[k]["rolle"])}</span><span class="fk-stand" data-stand="{k}-kurz">{e(KURZ[k])}</span></a></li>')
    def reihe(i, k):
        rk = RAUM[k]
        return (f'<li class="hz-z fb-z"><a href="{e(auf[k] or "#" + k)}" data-taste="{i + 1}">'
                f'<span class="fb-b"><img src="img/raum-{k}-s.webp" width="240" height="180" alt="{e(BILDER_W[rk]["alt"])}" decoding="async"></span>'
                f'<span class="fb-t"><small>N° {i + 1} · {e(W[k]["rolle"])}</small><b>{e(W[k]["name"])}</b><span class="fb-stand" data-stand="{k}-kurz">{e(KURZ[k])}</span></span>'
                f'<span class="hz-ring" aria-hidden="true">{PF}</span></a></li>')
    def schirmkachel(i, k):
        n = 'schirm-' + SCHIRME[k][0]
        if n in BILDER:
            b = f'<img src="img/{n}-s.webp" width="1200" height="750" alt="Vorschau: {e(W[k]["name"])}" decoding="async">'
        else:
            b = (f'<img src="img/raum-{k}.webp" width="{RAUM_G[0]}" height="{RAUM_G[1]}" alt="{e(BILDER_W[RAUM[k]]["alt"])}" decoding="async">'
                 + ('' if online else '<em class="fc-folgt">Vorschau folgt</em>'))
        return (f'<li class="hz-z fc-z"><a href="{e(auf[k] or "#" + k)}" data-taste="{i + 1}"><span class="fc-b">{b}</span>'
                f'<span class="fc-t"><small>N° {i + 1} · {e(W[k]["rolle"])}</small><b>{e(W[k]["name"])}</b>'
                f'<span class="fc-stand" data-stand="{k}-kurz">{e(KURZ[k])}</span></span><span class="hz-ring" aria-hidden="true">{PF}</span></a></li>')
    F = Bau.fassung
    if F == 'a':   # Sechs Bilder am Horizont: hell, links die Bühne (Ruhe = Terrasse, Zeiger = Vorschau), rechts sechs Fotokacheln des Hauses
        empfang = (f'<section class="m-empfang fa tapete" id="oben"><div class="innen">{kopf_links}'
                   f'<div class="fa-feld"><div class="hz-buehne">{rahmen}</div>'
                   f'<nav aria-label="Alle Werkzeuge"><ol class="hz-tafel fa-kacheln">{"".join(kachel(i, k, "fa-k") for i, k in enumerate(REIHE))}</ol></nav></div>'
                   f'{zeile_heute}{hilfe}</div></section>')
    elif F == 'b':   # Die Tafel am Steg: Nacht, links das grosse Bild, rechts eine helle Tafel mit sechs Zeilen und Foto
        empfang = (f'<section class="m-empfang fb dunkel" id="oben"><div class="innen">{kopf_links}'
                   f'<div class="fb-feld"><div class="hz-buehne">{rahmen}</div>'
                   f'<nav class="fb-tafel" aria-label="Alle Werkzeuge"><p class="fb-kopf">{zeiger("")}<span><b>{e(NAME)}</b>{e(STRASSE)} · {e(ORT)}</span></p>'
                   f'<ol class="hz-tafel">{"".join(reihe(i, k) for i, k in enumerate(REIHE))}</ol></nav></div>'
                   f'{zeile_heute}{hilfe}</div></section>')
    elif F == 'c':   # Sechs Bildschirme: hell, Kopf mittig (M22), die Werkzeuge selbst als grosse Vorschauen
        empfang = (f'<section class="m-empfang fc tapete" id="oben"><div class="innen"><div class="m-kopf0">{zeiger("m-kopf0__z")}'
                   f'<h1 class="m-kopf0__titel">{e(STUBE.split(" ", 1)[0])} <em>{e(STUBE.split(" ", 1)[1])}</em></h1><div class="m-kopf0__linie" aria-hidden="true"></div>'
                   f'<p class="m-kopf0__gruss"><span id="gruss">Guten Tag.</span> Womit fangen wir heute an?</p><small class="m-kopf0__datum" id="datum">&nbsp;</small></div>'
                   f'{zeile_heute}<nav aria-label="Alle Werkzeuge"><ol class="hz-tafel fc-kacheln">{"".join(schirmkachel(i, k) for i, k in enumerate(REIHE))}</ol></nav>'
                   f'{hilfe}</div></section>')
    else:
        empfang = f'''<section class="m-empfang dunkel" id="oben">
  <div class="innen">
    <div class="m-kopf0">
      {zeiger("m-kopf0__z")}
      <h1 class="m-kopf0__titel">{e(STUBE.split(' ', 1)[0])} <em>{e(STUBE.split(' ', 1)[1])}</em></h1>
      <div class="m-kopf0__linie" aria-hidden="true"></div>
      <p class="m-kopf0__gruss"><span id="gruss">Guten Tag.</span> Womit fangen wir heute an?</p>
      <small class="m-kopf0__datum" id="datum">&nbsp;</small>
    </div>
    <div class="hz-feld" data-hz="{hz:.4f}">
      <div class="hz-linie" aria-hidden="true"></div>
      <div class="hz-buehne">
        <figure class="hz-rahmen" style="--abbild:url({BILDER_W["start"].get("abbild", "")})">{vorschau}<figcaption class="hz-unter" aria-live="polite">{unter}</figcaption></figure>
      </div>
      <nav aria-label="Alle Werkzeuge"><ol class="hz-tafel">{zeilen}</ol></nav>
    </div>
    <p class="m-zeile"><span>Heute</span><span><b data-stand="registre-heute">–</b>Besuche</span><i></i><span><b data-stand="registre-buchung">–</b>zur Reservation</span><span class="m-zeile__bsp bsp" hidden>Beispiel</span><i></i>{f'<a href="{e(reg_auf)}">{e(W["registre"]["name"])} öffnen</a>' if reg_auf else f'<span>{e(W["registre"]["name"])} folgt</span>'}</p>
    <p class="m-hilfe">Ein Klick oder die Taste <kbd>1</kbd> bis <kbd>6</kbd> öffnet das Werkzeug. Darunter stellt sich jedes einzeln vor.</p>
  </div>
</section>'''

    return f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
{'' if online else ZUR_STUBE}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(STUBE)} · {e(NAME)}</title>
<meta name="description" content="Alle Werkzeuge der {e(NAME)} an einem Ort: {', '.join(W[k]['name'] for k in REIHE)}.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0b1d3d">
<link rel="preload" href="schrift/OpenSans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="maison.css?v={v['maison.css']}">
<script src="fehler.js?v={v['fehler.js']}"></script>
</head>
<body class="ma">
<div class="m-tuer" id="tuer" role="alert" hidden><p class="m-tuer__t">{e(STUBE)} startet nicht.</p><p id="tuer-t">&nbsp;</p>{pruef}<a class="knopf knopf--klein" href="">Neu laden<i>{PF}</i></a></div>

<header class="m-oben">
  <a class="knopf knopf--klein m-oben__ecke m-oben__ecke--l" href="#fuss">Anleitungen<i>{PF}</i></a>
  <nav class="m-insel" aria-label="Werkzeuge">
    <a class="m-ecke" href="#oben">{zeiger("m-ecke__z")}<span class="m-ecke__t"><b>{e(STUBE)}</b><small>Alle Werkzeuge · {e(NAME)}</small></span></a>
    <span class="m-insel__wege">{insel}</span>
  </nav>
  <a class="knopf knopf--klein m-oben__ecke" href="{web}" target="_blank" rel="noopener">Website ansehen<i>{PF}</i></a>
</header>

<main>
{empfang}

<div class="m-band" data-laufband aria-hidden="true"><ul>{band}{band}</ul></div>
{saele}
</main>

<footer class="m-fuss tapete" id="fuss">
  <div class="m-fuss__platte" data-r>
    <svg class="m-fuss__wm" viewBox="{wm_vb}" fill="currentColor" role="img" aria-label="{e(NAME)}">{wm}</svg>
    <div class="m-fuss__spalte"><p class="m-fuss__k">Das Haus</p><p>{e(NAME)}</p><p>{e(STRASSE)}, {e(ORT)}</p><a href="{web}" target="_blank" rel="noopener">Website ansehen</a></div>
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
    """Jeder «Knopf-Name» aus den Tafeln muss im Code des Werkzeugs vorkommen (M20). Ordner aus stand_wege.json → code."""
    fehlt = []
    sw = stand_wege()
    for k, n in sorted(set(UI)):
        code = (sw.get(k) or {}).get('code') or []
        n = html.unescape(n)
        gefunden = False
        for o in code:
            for wurzel, _, dateien in os.walk(os.path.expanduser(o)):
                if any(t in wurzel for t in ('/online', '/pruefung', '/node_modules', '/_qa')):
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
/* Fehlermelder (R03), vor allem anderen: Skriptfehler in den Browser (sb_werkzeuge_fehler) und an den Server-Teil (studio/api/fehler, wenn es ihn gibt).
   Netzfehler nie melden, höchstens 20 je Seite, eigener Fehlschlag wird nicht erneut gemeldet. */
(function(){var zahl=0;function merk(t){t=String(t);window.MAISON_FEHLER=t;if(++zahl>20||/Load failed|access control|abort|NetworkError|Failed to fetch/i.test(t))return;
try{var a=JSON.parse(localStorage.getItem('sb_werkzeuge_fehler')||'[]');a.unshift({zeit:new Date().toISOString(),art:'stube',text:('Die Stube: '+t).slice(0,400),ort:location.pathname});localStorage.setItem('sb_werkzeuge_fehler',JSON.stringify(a.slice(0,30)))}catch(e){}
try{fetch('/studio/api/fehler',{method:'POST',headers:{'Content-Type':'application/json','X-Studio':'1'},body:JSON.stringify({text:('Die Stube · '+t).slice(0,600)}),keepalive:true}).catch(function(){})}catch(e){}}
window.addEventListener('error',function(e){if(e.target&&e.target.tagName==='SCRIPT'){window.MAISON_FEHLER='Die Datei '+e.target.getAttribute('src').split('?')[0]+' liess sich nicht laden.';return}merk((e.message||'Fehler')+' · '+(e.filename||'').split('/').pop()+':'+(e.lineno||''))},true);
window.addEventListener('unhandledrejection',function(e){merk('Versprechen: '+((e.reason&&e.reason.message)||e.reason))});
/* Startfehler-Tür (R04): ist maison.js beim Laden nicht durchgelaufen, sagt die Seite es und zeigt alles ohne Bewegung. Wache nach 12 s. */
function tuer(){if(window.MAISON_BEREIT)return;var t=document.getElementById('tuer');if(!t||!t.hidden)return;
document.documentElement.classList.remove('js');document.getElementById('tuer-t').textContent=window.MAISON_FEHLER||'Das Programm der Seite ist nicht durchgelaufen.';t.hidden=false}
window.addEventListener('load',tuer);setTimeout(tuer,12000);})();
'''


# Demo-Check 21.10.2026: Gang an das Gebaute angepasst (Kacheln statt Zeilen, Status darunter; Namen stehen erst ab rund 1900 px in der Leiste)
def rundgang():
    s = open(os.path.join(QUELLE, 'rundgang-vorlage.js'), encoding='utf-8').read()
    a = s.index('  var GAENGE = {'); b = s.index('\n  };', a) + 4
    namen = ', '.join(W[k]['name'] for k in REIHE)
    gang = f'''  var GAENGE = {{
    maison: {{ name: '{STUBE}', schritte: [
      {{ ziel: ['.m-kopf0', '#oben'], oben: true, titel: 'Das ist {DIE(STUBE)}',
        text: 'Der Eingang zu allen Werkzeugen des Hauses. Von hier aus pflegen Sie Website, Karten, Drucksachen, den Chat und die Marke selbst.' }},
      {{ ziel: ['.hz-z:first-child a', '.hz-tafel'], titel: 'Jede Kachel ist ein Werkzeug',
        text: '{namen}. Darunter steht, was dort gerade ansteht. Ein Klick oder die Taste 1 bis 6 öffnet es.' }},
      {{ ziel: ['.hz-rahmen', '.hz-tafel'], titel: 'Erst ansehen, dann öffnen',
        text: 'Am Rechner zeigt das grosse Bild links, wie das Werkzeug aussieht, sobald Sie über eine Kachel fahren.' }},
      {{ ziel: ['.m-insel', '.m-oben'], oben: true, titel: 'Immer erreichbar',
        text: 'Ein Klick auf diese Leiste bringt Sie von überall zurück zu den Werkzeugen. Aus jedem Werkzeug kommen Sie hierher zurück.' }},
      {{ ziel: ['#bureau .m-saal__kopf', '#bureau'], titel: 'Jedes Werkzeug stellt sich vor',
        text: 'Weiter unten zeigt jedes Werkzeug, was es für das Haus tut, mit Bildern aus dem Werkzeug selbst.' }}
    ] }}
  }};'''
    s = s[:a] + gang + s[b:]
    s = s.replace("'rundgang-bg-'", "'rundgang-sb-'")
    s = s.replace('font:600 26px/1.1 "Barlow Semi","Arial Narrow",sans-serif', 'font:400 21px/1.2 "Open Sans",Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase')
    s = s.replace('"Barlow Semi","Arial Narrow",sans-serif', '"Open Sans",Arial,sans-serif')
    for alt, neu in (('#2c3136', '#0A2552'), ('#485056', '#113d88'), ('#1d2224', '#0b1d3d'), ('#7c8386', '#0F3678'), ('#e9ecec', '#F3F6F9'),
                     ('#d6bb96', '#C5D2E1'), ('#b7a27a', '#A2B6CF'), ('#e3cd98', '#C5D2E1'), ('227,205,152', '197,210,225'), ('#f7e9c6', '#EAEFF5'),
                     ('#b99a5c', '#A9BAD0'), ('#fffdf9', '#ffffff'), ('#f7f1e5', '#F3F6F9'), ('210,191,152', '162,182,207'), ('130,108,53', '15,54,120'),
                     ('10,12,22', '4,16,35'), ('10,13,26', '4,16,35'), ('26,29,40', '4,16,35'), ('27,32,51', '4,16,35')):
        s = s.replace(alt, neu)
    s = re.sub(r'^/\*[^\n]*\*/\n', '', s, count=1)
    if re.search(r'Barlow|Cormorant|Cinzel|Gasterntal|Fenster ist', s):
        raise SystemExit('rundgang.js: Angabe der Vorlage übrig')
    return f'/* Rundgang (R18, M11): Kopie des Werkzeugs der Häuser, Gang für {STUBE} der {NAME}; gebaut von _werkzeuge/maison/bau.py */\n' + s


def zur_werkbank():
    s = open(os.path.join(QUELLE, 'zur-werkbank-vorlage.js'), encoding='utf-8').read()
    s = re.sub(r'^/\*[^\n]*Gasterntal[^\n]*\*/\n', '', s)
    if "var SCHL = 'bg-wb';" not in s:
        raise SystemExit('zur-werkbank.js: Schlüssel nicht gefunden')
    s = s.replace("var SCHL = 'bg-wb';", "var SCHL = 'schloessli-wb';").replace('«bg-wb»', '«schloessli-wb»')
    s = s.replace('linear-gradient(180deg,#485056,#1d2224)', 'linear-gradient(180deg,#113d88,#0b1d3d)')
    return f'/* «Zur Werkbank» (R19) · {STUBE} der {NAME}: Kopie des Bausteins der Häuser, Schlüssel des Hauses «schloessli-wb». Gebaut von bau.py. */\n' + s


def ohne_fremde(t):
    """Angaben anderer Häuser gehen nicht in die Ausgabe (F29)."""
    m = re.search(r'.{0,40}(?:Rivage|\bgbr\b|Carlton|Interlaken|Doldenhorn|Ruedihus|Gasterntal|Kandersteg|Selden|Schäfli|Wigoltingen|Barlow|Cormorant|Cinzel|\bbg-wb\b).{0,40}', t, re.I | re.S)
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
        hz = bilder(ziel)
        for n, t in teile.items():
            open(os.path.join(ziel, n), 'w', encoding='utf-8').write(ohne_fremde(t) if n not in ('zur-werkbank.js',) else t)
        s = ohne_fremde(seite(online, hz, v))
        if online and re.search(r'localhost|127\.0\.0\.1|data-platz|/_weiter/', s):
            raise SystemExit('Online-Fassung enthält localhost oder Platzhalter')
        open(os.path.join(ziel, 'index.html'), 'w', encoding='utf-8').write(s)
        if not online:   # Fassungen des Empfangs zur Wahl (nur lokal): fassung-a.html …
            alt_f = Bau.fassung
            for f in ('a', 'b', 'c'):
                Bau.fassung = f
                open(os.path.join(ziel, f'fassung-{f}.html'), 'w', encoding='utf-8').write(ohne_fremde(seite(False, hz, v)))
            Bau.fassung = alt_f
    fk = knoepfe()
    json.dump({k: dict(teil=TEIL[k], zustand=kette_teil(k)[0], adresse=kette_teil(k)[1]) for k in REIHE},
              open(os.path.join(HIER, 'pruefung', 'adressen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{STUBE} gebaut: _werkzeuge/maison/index.html + online/index.html · {len([b for b in BILDER if b.startswith("schirm")])} Bildschirme')
    print('  vorliegend:', ', '.join(f'{W[k]["name"]} {kette_teil(k)[0] or "–"}' for k in REIHE))
    if FEHLT:
        print('  noch ohne Bildschirm:', ', '.join(FEHLT))
    if fk:
        print('  Knopf-Namen nicht im Code gefunden:', '; '.join(fk))


if __name__ == '__main__':
    os.makedirs(os.path.join(HIER, 'pruefung'), exist_ok=True)
    baue()
