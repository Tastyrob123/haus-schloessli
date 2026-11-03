#!/usr/bin/env python3
"""Wirtschaft am Schlössli: Hauswerte, Kleid und Bausteine für alle Papier-Beigaben der Werkbank (Werkbank Papier, Nachtbau 3./4.11.2026).
Unterlagen, Drucksachen, Untersetzer, Sticker, Postkarten und Beigaben lesen ihre Farben, Schriften, Zeichen und Hauswerte nur von hier.

Kleid «Stuhl und See» (website/assets/css/haus.css :root, _werkzeuge/oberflaeche/kleid/schloessli.css): Nacht über dem See, Stuhlblau als dunkle
Flächen, Papier/Seespiegel/Blatt als Raum, Seehimmel nur als Linie und Zeichen, Schirmrot nur als Punkt. Titel Open Sans 400 in Versalien gesperrt,
Lauf Instrument Sans, Zahlen und Etiketten DM Mono gesperrt. Zeichen = die Zeiger, Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» (schloessli-marke.svg#wm).
Hauswerte nur aus website/inhalt/*.json (nie abgetippt). Schweizer Schreibung: ss statt ß in allem, was gedruckt wird (ss()).

ein() stellt vor dem ersten «import kern» sicher, dass der Kit ein Haus mit diesen Werten sieht: ist _werkbank/haus.py schon das Schlössli,
wird es genommen und nur um die Papier-Werte ergänzt (PAPIER, PAPIER_SEITE, UNTERLAGEN, FAECHER, ETIKETTEN); sonst ein schmales Ersatz-Haus."""
import glob, html, json, os, re, sys, types

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))            # website/_werkbank/_werkbank
ROOT = os.path.dirname(W)                                 # website/_werkbank (Projektordner des Kits)
WEB = os.path.dirname(ROOT)                               # website/ (nur gelesen)
PROJ = os.path.dirname(WEB)
KLEID = os.path.join(PROJ, '_werkzeuge', 'oberflaeche', 'kleid')
SATZ = os.path.join(W, 'satz')

# ---------------------------------------------------------------- Farben (Kleid Stuhl und See)
NACHT, TIEF, STUHL = '#0b1d3d', '#0a234c', '#113d88'
PAPIER, SPIEGEL, BLATT, WEISS = '#e7ecf3', '#d0dae7', '#f4f6f9', '#fbfcfe'
HIMMEL, HIMMELH, HIMMELT = '#a2b6cf', '#c5d2e1', '#0f3678'
TINTE, LEISE, PUNKT = '#041023', '#41506a', '#fd9964'
FARBEN = dict(nacht=NACHT, tief='#081631', navy=TIEF, blau=STUHL, papier='#f3f6f9', creme=PAPIER, weiss=WEISS,
              gold=HIMMEL, messing=HIMMELH, taupe=HIMMELT, tinte=TINTE, punkt=PUNKT)

_SV = os.path.relpath(os.path.join(ROOT, 'assets', 'svg'), SATZ)
TAPETE = f'url({_SV}/tapete-a-dunkel.svg) 50% 0/14mm auto'    # Punktraster der dunklen Flächen der Website
TAPETE_H = f'url({_SV}/tapete-a-hell.svg) 50% 0/14mm auto'

# ---------------------------------------------------------------- Hauswerte (website/inhalt)
_IN = os.path.join(WEB, 'inhalt')
HJ = json.load(open(os.path.join(_IN, 'haus.json'), encoding='utf-8'))
LM = json.load(open(os.path.join(_IN, 'laestermeile.json'), encoding='utf-8'))
LU = json.load(open(os.path.join(_IN, 'lunch.json'), encoding='utf-8'))
BK = json.load(open(os.path.join(_IN, 'bankett.json'), encoding='utf-8'))
BILDER = json.load(open(os.path.join(_IN, 'bilder.json'), encoding='utf-8'))
NAME = 'Wirtschaft am Schlössli'
KURZ = 'wirtschaft-am-schloessli'
STRASSE, ORT = HJ['strasse'], HJ['ort']
ADR = f'{STRASSE} · {ORT}'
TEL, MAIL = HJ['telefon'], HJ['mail']
IG = '@' + HJ['instagram'].rstrip('/').rsplit('/', 1)[1]
WEBSITE = 'schloessli-bottighofen.ch'
BY = HJ['by']                                             # «by Christian Kuchler»
Z = HJ['zeiten']
TAGE, RUHE, OFFEN = Z['tage'].replace(' - ', ' bis '), Z['ruhetag'].replace(' & ', ' und '), Z['offen'].replace(' - ', ' bis ')
KUECHE = [k.replace(' - ', ' bis ') for k in Z['kueche']]
RECHTE_FREI = {k for k, v in BILDER.items() if not v.get('nachweis') and not re.match(r'(tb-|baum|kf-|pa-|kp-|feuerwerk|ch-|stier|mi-|lounge|sauce|ig-)', k)}


def ss(s):
    """Schweizer Schreibung: ss statt ß."""
    return s.replace('ß', 'ss').replace('ẞ', 'SS')


def ganz(s):
    """Leerzeichen der Daten sauber, «…» statt „…“."""
    return ss(re.sub(r'\s+', ' ', s).replace('„', '«').replace('“', '»').replace('´', '’')).strip()


def vers(text):
    return e(ss(text).upper())


def nachweis(key):
    n = BILDER.get(key, {}).get('nachweis')
    return f"Foto: {n['urheber']}, {n['lizenz']}, Wikimedia Commons" if n else ''


def bild(key, hoechstens=2400):
    """grösste Fassung eines Fotos der Website bis «hoechstens» Pixel (assets/img/<key>-<breite>.webp), voller Pfad"""
    b = sorted(int(m.group(1)) for p in glob.glob(os.path.join(WEB, 'assets', 'img', key + '-*.webp'))
               if (m := re.search(r'-(\d+)\.webp$', p)) and int(m.group(1)) <= hoechstens)
    if not b:
        raise FileNotFoundError(key)
    return os.path.join(ROOT, 'assets', 'img', f'{key}-{b[-1]}.webp')


def bild_satz(key, hoechstens=1800):
    """Foto für den Satz: als JPEG unter satz/bild/ (Chromium bettet WebP unkomprimiert ins PDF ein, JPEG bleibt klein; der Vorschau-Server
    liefert aus _werkbank/ nur satz/ und fonts/). Gibt die Adresse aus Sicht der Satzdateien zurück."""
    from PIL import Image
    q = bild(key, 2400)
    z = os.path.join(SATZ, 'bild', f'{key}-{hoechstens}.jpg')
    if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(q):
        os.makedirs(os.path.dirname(z), exist_ok=True)
        im = Image.open(q).convert('RGB')
        if im.width > hoechstens:
            im = im.resize((hoechstens, round(im.height * hoechstens / im.width)), Image.LANCZOS)
        im.save(z, 'JPEG', quality=84, optimize=True, progressive=False)
    return 'bild/' + os.path.basename(z)


# ---------------------------------------------------------------- Zeichen und Wortmarke aus dem Kleid (nie nachgebaut)
def _zeichen():
    s = open(os.path.join(KLEID, 'schloessli-zeichen.svg'), encoding='utf-8').read()
    vb = ' '.join(str(float(x)).rstrip('0').rstrip('.') for x in re.search(r'viewBox="([^"]+)"', s).group(1).split())
    innen = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    return vb, re.sub(r'\s+fill="(?:#000000|#000|currentColor)"', '', re.sub(r'\s*\n\s*', ' ', innen)).strip()


def _wortmarke():
    s = open(os.path.join(KLEID, 'schloessli-marke.svg'), encoding='utf-8').read()
    m = re.search(r'<symbol[^>]*viewBox="([^"]+)"[^>]*>(.*)</symbol>', s, re.S)
    return m.group(1), re.sub(r'\s+fill="currentColor"', '', m.group(2)).strip()


ZEICHEN = _zeichen()
WORT = _wortmarke()
ZB = [float(x) for x in ZEICHEN[0].split()]
WB = [float(x) for x in WORT[0].split()]
ZV, WV = ZB[3] / ZB[2], WB[3] / WB[2]                     # Höhe : Breite

# ---------------------------------------------------------------- Werte, die der Kit für die Seiten braucht (Inhalt von hier, Revier Papier)
ETIKETTEN = dict(ordner='untersetzer', name='Untersetzer', einzahl='Untersetzer')
SCHRIFT = dict(titel=('Open Sans', 'OpenSans-var.woff2'), titel_folge='Arial,sans-serif', ersatz="local('Arial')", druckgewicht=400)
DRUCKQUELLEN = []
DRUCKSCHRIFT = [('Open Sans', 300, 'OpenSans-Light.ttf'), ('Open Sans', 400, 'OpenSans-Regular.ttf'), ('Open Sans', 500, 'OpenSans-Medium.ttf'), ('Open Sans', 700, 'OpenSans-Medium.ttf')]
UNTERLAGEN = dict(
    text='Zum Schlössli gehören die Karte nach Ländern, das Lunch-Menü, die Karte der Lästermeile, die Weinkarte und die Bankettmenüs. Alle sind als Idee neu gesetzt, mit Ihren Preisen, jede neben Ihrer heutigen Fassung. Dazu liegen der Brief und das Angebot bei.',
    seite_text='Die Karte nach Ländern, das Lunch-Menü, die Lästermeile, die Weinkarte und die Bankettmenüs, jede als Idee neu gesetzt, mit Ihren Preisen. Links steht Ihre heutige Fassung, rechts die neue, Seite für Seite. Dazu der Brief und das Angebot.',
    knopf2=('Karte auf der Website', '../karte.html'))
FAECHER = [('speisekarte', 'Die Karte nach Ländern'), ('lunch', 'Lunch-Menü'), ('laestermeile', 'Lästermeile'), ('bankett', 'Bankettmenüs')]
PAPIER_W = dict(   # haus.PAPIER (Kit)
    etik_text='An der Lästermeile gehen den ganzen Tag Gläser über die Theke. Dazu passen zwölf Untersetzer in den Tönen des Sees, mit den Zeigern und den Zeilen der Lästermeile.',
    druck_text='Vom Gutschein bis zur Menükarte für die Feier, dazu <a href="../sticker/index.html" target="_blank" rel="noopener">Sticker</a>, <a href="../postkarten/index.html" target="_blank" rel="noopener">Postkarten</a> und <a href="../beigaben/index.html" target="_blank" rel="noopener">Beigaben</a>.')
PAPIER_SEITE = dict(breit=set(), formen=set(), auslage=[], karton={}, titel={}, schatten=set(),
                    flaeche=['fl--papier', 'fl--creme', 'fl--nacht tapete-leicht', 'fl--papier', 'fl--creme', 'fl--navy tapete'],
                    etik_titel=('Untersetzer', 'für die Lästermeile.'),
                    etik_text='An der Lästermeile gehen den ganzen Tag Gläser über die Theke. Hier sind {n} Untersetzer als Idee, rund, je 94 mm, in den Tönen des Sees: Stuhlblau, Seehimmel und Papier.',
                    etik_kap='Die Untersetzer', etik_kopf=['Zwölf', 'Untersetzer.'],
                    etik_kopftext='Das Blau der Stühle, der Himmel über dem See und das helle Papier der Karte, in der Mitte die Zeiger oder eine Zeile der Lästermeile.',
                    druck_text='Dinge, die bei Ihnen auf dem Tisch, an der Tür oder in der Post liegen könnten: von Ihnen gesetzt, in der Hausdruckerei gedruckt. Nehmen Sie davon, was Ihnen gefällt.',
                    etik_auslage=[(4, 0, 22, -6), (38, 2, 22, 4), (72, 0, 22, -3), (6, 35, 22, 5), (40, 36, 22, -4), (74, 34, 22, 6), (4, 70, 22, 3), (38, 70, 22, -5), (72, 68, 22, 4), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)])
_PS = os.path.join(W, 'papier_neu_seite.json')


def _seite_neu():
    """Karton, Titel und Breite je Drucksache (papier.py schreibt papier_neu_seite.json)."""
    if not os.path.exists(_PS):
        return
    for k, v in json.load(open(_PS, encoding='utf-8')).items():
        PAPIER_SEITE['karton'][k] = (v['karton'][0], [tuple(x) for x in v['karton'][1]]); PAPIER_SEITE['titel'][k] = v['titel']
        PAPIER_SEITE['breit'].update(v['breit']); PAPIER_SEITE['schatten'].add(k)
    if os.path.exists(os.path.join(W, 'papier_auslage.json')):
        PAPIER_SEITE['auslage'] = [tuple(x) for x in json.load(open(os.path.join(W, 'papier_auslage.json'), encoding='utf-8'))]


_seite_neu()
PAPIERWERTE = dict(ETIKETTEN=ETIKETTEN, UNTERLAGEN=UNTERLAGEN, FAECHER=FAECHER, PAPIER=PAPIER_W, PAPIER_SEITE=PAPIER_SEITE,
                   DRUCKSCHRIFT=DRUCKSCHRIFT, SCHRIFT=SCHRIFT, ZEICHEN=ZEICHEN, WORT=WORT)

# schmales Ersatz-Haus, solange _werkbank/haus.py noch nicht das Schlössli ist
ERSATZ = dict(NAME=NAME, KURZ=KURZ, LEISTE='SCHLÖSSLI', HAUSART='restaurant', PORT=9288, DOMAIN=WEBSITE, HEUTE_URL='https://www.' + WEBSITE,
              RECHTE='der Wirtschaft am Schlössli und den jeweiligen Fotografen.', FARBEN=FARBEN, MUSTER='url(../assets/svg/tapete-a-dunkel.svg)',
              MUSTER_B='168px', MUSTER_DRUCK='14mm', DRUCKQUELLEN=DRUCKQUELLEN, SATZ_FUSS=f'{NAME} · {ADR}', HAUS=HJ,
              REIHENFOLGE=['brief', 'vergleich', 'ideen', 'gefuege', 'seiten', 'unterlagen', 'handschrift', 'papier', 'material', 'dazu', 'schluss'],
              SEITEN=[('index.html', 'Startseite', 8, '', '')], STELLEN=[], ANREDE='Grüezi, Herr Kuchler', START_MS=4200, WAHL='main > section')


def ein():
    """Vor dem ersten «import kern» aufrufen. Gibt das Haus-Modul zurück."""
    if 'haus' in sys.modules and getattr(sys.modules['haus'], '_papier', False):
        return sys.modules['haus']
    H = None
    if W not in sys.path:
        sys.path.insert(0, W)
    try:
        import haus as H  # noqa: F811
        if getattr(H, 'NAME', '') != NAME:
            H = None
    except Exception:
        H = None
    if H is None:
        for m in ('haus', 'kern', 'hilfen_haus'):
            sys.modules.pop(m, None)
        H = types.ModuleType('haus'); H.__file__ = os.path.join(W, 'papier_haus.py')
        for k, v in ERSATZ.items():
            setattr(H, k, v)
        H._ersatz = True
        sys.modules['haus'] = H
    for k, v in PAPIERWERTE.items():
        setattr(H, k, v)
    H.FARBEN = dict(FARBEN, **{k: v for k, v in getattr(H, 'FARBEN', {}).items() if k not in FARBEN})
    H.KURZ = KURZ
    H._papier = True
    # werkbank/werkbank.css und seiten.css gehören dem Kern: nur schreiben, wenn sie fehlen
    import kern as K
    E_ = ['', 'ein', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun']
    for z in range(21, 50):
        K.ZAHL.setdefault(z, ((E_[z % 10] + 'und') if z % 10 else '') .capitalize() + ('zwanzig' if z < 30 else 'dreissig' if z < 40 else 'vierzig') if z % 10 else {20: 'Zwanzig', 30: 'Dreissig', 40: 'Vierzig'}[z])
    _g = K.gestaltung

    def gestaltung():
        p = os.path.join(ROOT, 'werkbank', 'werkbank.css')
        if not os.path.exists(p):
            _g()
    K.gestaltung = gestaltung
    return H


if __name__ == '__main__':
    H = ein()
    print('Haus:', H.NAME, '· Ersatz' if getattr(H, '_ersatz', False) else '· haus.py', '· Zeichen', ZEICHEN[0], '· Wortmarke', WORT[0], '·', ADR, TEL, MAIL, IG)
