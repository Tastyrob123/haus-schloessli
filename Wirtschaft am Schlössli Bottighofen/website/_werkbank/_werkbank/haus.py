"""Wirtschaft am Schlössli, Bottighofen: Inhalt der Werkbank («Alles auf einen Blick») und ihrer Beigaben.   Werkzeug: ~/Desktop/Website-Projekte/_Werkbank-Kit/

Werkbank-Kern, Nachtbau 3./4.11.2026 (Auftrag Oberchef, Roberts Deal: «kopieren, umkleiden, Hauswerte eintragen, nichts neu erfinden»).
Aufbau, Wege, Bausteine und Prüf-Nachbauten aus der Werkbank des Culinarium Hannover (28.10.–1.11.2026, über Walk on the Wild Side), Inhalt aus dem alten
Schlössli-Stand (Werkbank vom 21.10.2026, demo-geprüft: _werkbank.vor-nachtbau-2026-11-03/haus.py): Brief, Befund, Karten, Ideen, Gefüge, Gäste, Angebot.
Kleid «Stuhl und See» (website/assets/css/haus.css :root, _werkzeuge/oberflaeche/kleid/schloessli.css): Nacht über dem See #0B1D3D, Tief #0A234C, Stuhlblau
#113D88 als dunkle Flächen mit der Punkt-Tapete; Papier #E7ECF3, Seespiegel #D0DAE7, Blatt #F4F6F9 als Raum; Seehimmel #A2B6CF/#C5D2E1 als Linie und Zeichen
auf Dunkel, Seehimmel tief #0F3678 als Betonung auf Hell; Tinte #041023; Schirmrot #FD9964 nur als Punkt. Titel Open Sans 400 in Versalien gesperrt,
Lauf Instrument Sans, Angaben DM Mono. Zeichen sind die Zeiger, die Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» kommt aus dem Kleid (nie nachgebaut).

Eigenes Revier: website/_werkbank/ ist der Projektordner des Kits (ROOT), die Website liegt eine Ebene höher (WEB) und wird nur gelesen;
assets/ ist ein Verweis auf website/assets (nur gelesen). Serviert von website/_werkbank/serve.py auf Port 9288 (zuerst das Revier, sonst die Website).
Ton: Sie-Form, Schweizer Schreibung (ss statt ß, ss_gang.py am Ende jedes Baus), herzlich. Restaurant, keine Zimmer. Kein Betrag ausser der Betreuung."""
import json
import os
import re as _re
import sys
import glob as _glob
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # = website/_werkbank (Projektordner des Kits)
WEB = os.path.dirname(ROOT)                                          # = website/ (nur gelesen)
PROJ = os.path.dirname(WEB)
KLEID = os.path.join(PROJ, '_werkzeuge', 'oberflaeche', 'kleid')
HAUS = json.load(open(os.path.join(WEB, 'inhalt', 'haus.json'), encoding='utf-8'))


def bild(key, hoechstens=2400):
    """Grösste Fassung eines Fotos der Website bis «hoechstens» Pixel Breite (assets/img/<key>-<breite>.webp) als voller Pfad für K.hausbild."""
    b = sorted(int(m.group(1)) for p in _glob.glob(os.path.join(WEB, 'assets', 'img', key + '-*.webp')) if (m := _re.fullmatch(_re.escape(key) + r'-(\d+)\.webp', os.path.basename(p))) and int(m.group(1)) <= hoechstens)
    if not b:
        raise FileNotFoundError(f'Bild {key} fehlt in website/assets/img')
    return os.path.join(WEB, 'assets', 'img', f'{key}-{b[-1]}.webp')


NAME = 'Wirtschaft am Schlössli'
KURZ = 'wirtschaft-am-schloessli'
LEISTE = ''          # in der Leiste stehen die Zeiger; keine Ersatz-Wortmarke aus Schrift (Kriterium 14)
HAUSART = 'restaurant'
PORT = 9288
DOMAIN = 'schloessli-bottighofen.ch'
HEUTE_URL = 'https://www.schloessli-bottighofen.ch'
ANREDE = 'Grüezi Herr\u00a0Kuchler, grüezi Herr\u00a0Volpert'   # Namen nie getrennt (Handy 390: kein Einzelwort)
RECHTE = 'der Wirtschaft am Schlössli und den jeweiligen Fotografen.'
START_MS = 4200
WAHL = 'main > section'
ADRESSE = f"{NAME} · {HAUS['strasse']} · {HAUS['ort']}"

# ---------- Farben: die der Website (website/assets/css/haus.css :root), Farbwelt A «Stuhl und See», kein Gold ----------
FARBEN = dict(nacht='#0b1d3d', tief='#081631', navy='#0a234c', blau='#113d88', papier='#f3f6f9', creme='#e7ecf3', weiss='#fbfcfe',
              gold='#a2b6cf', messing='#c5d2e1', taupe='#0f3678', tinte='#041023', punkt='#fd9964', rot='#fd9964')
SCHRIFT = dict(titel=('Open Sans', 'OpenSans-var.woff2'), titel_folge="Arial,sans-serif", ersatz="local('Arial')", druckgewicht=400)
SCHRIFT_MEHR = []
DRUCKQUELLEN = []   # Open Sans setzt _werkbank/druckschrift.py fest (wght und wdth), der Kit nur Instrument Sans und DM Mono
DRUCKSCHRIFT = [('Open Sans', 400, 'OpenSans-Regular.ttf'), ('Open Sans', 500, 'OpenSans-Medium.ttf'), ('Open Sans', 700, 'OpenSans-Medium.ttf')]
# Muster der Website: das Punktraster (assets/svg/tapete-a-dunkel.svg, Ton in Ton), vom Wurzelweg aus
MUSTER = 'url(/assets/svg/tapete-a-dunkel.svg)'
MUSTER_B = '168px'
MUSTER_DRUCK = '14mm'
# Das Zeichen: die Zeiger der Wortmarke als Datei aus dem Kleid (_werkzeuge/oberflaeche/kleid/schloessli-zeichen.svg, Quelle website/assets/svg/zeichen.svg),
# unverändert übernommen, nie nachgezeichnet.
_ZC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen', 'zeichen-zeiger.svg')
os.makedirs(os.path.dirname(_ZC), exist_ok=True)
open(_ZC, 'w', encoding='utf-8').write(open(os.path.join(KLEID, 'schloessli-zeichen.svg'), encoding='utf-8').read())
ZEICHEN = K.svg_innen(_ZC)
ZEICHEN = (ZEICHEN[0], ZEICHEN[1].replace(' fill="#000"', ''))   # Farbe über currentColor, wie bei jedem Zeichen der Werkbank


def _wortmarke():
    """Die Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» aus _werkzeuge/oberflaeche/kleid/schloessli-marke.svg (Symbol «wm»), so wie Website und Werkzeuge sie zeigen."""
    s = open(os.path.join(KLEID, 'schloessli-marke.svg'), encoding='utf-8').read()
    m = _re.search(r'<symbol id="wm" viewBox="([^"]+)">(.*?)</symbol>', s, _re.S)
    vb = ' '.join(str(float(x)).rstrip('0').rstrip('.') for x in m.group(1).split())
    return vb, _re.sub(r'\s+fill="currentColor"', '', _re.sub(r'\s*\n\s*', ' ', m.group(2))).strip()


WORT = _wortmarke()
ETIKETTEN = dict(ordner='untersetzer', name='Untersetzer der Lästermeile', einzahl='Untersetzer')

SEITEN = [   # alle Seiten, die ein Gast als Seite wahrnimmt, dazu das Rechtliche (Sätze nur aus dem, was auf der Seite steht; alter Schlössli-Stand)
    ('index.html', 'Startseite', 8, 'Die blauen Stühle unter den Platanen, der Hafen, die Lästermeile, die Karte nach Ländern, Küche und Keller, der Besen von 1699 und der Abend unter der Platane.', ''),
    ('karte.html', 'Die Karte', 5, 'Frankreich, Italien, die Iberische Halbinsel und die Klassiker, ein Glas zu jedem Gang, das Lunch-Menü und die Lästermeile.', ''),
    ('weinkarte.html', 'Weinkarte', 4, 'Der Weinberater und alle Weine der Karte als Kärtchen, nach Champagner, Weiss, Rosé, Rot und Süss.', ''),
    ('feiern.html', 'Banketts & Gruppen', 4, 'Zwei Etagen für je bis zu 26 Personen, die Bankettmenüs Gericht für Gericht und die Anfrage im Fenster.', ''),
    ('anlaesse.html', 'Events', 4, 'Das Four-Hands-Dinner auf der Excellence, das Jahr am Hafen als Band und was war.', ''),
    ('team.html', 'Über uns', 3, 'Ein Blick in die Küche, das Team und die Taverne zum Schäfli in Wigoltingen.', ''),
    ('kontakt.html', 'Kontakt', 3, 'Zeiten, Anfahrt über Land und über das Wasser und der See heute.', ''),
    ('gutschein.html', 'Gutschein', 2, 'Den Gutschein gestalten: Betrag, Haus, für wen, von wem und ein Satz dazu.', ''),
    ('abend.html', 'Ihr Abend', 2, 'Anlass, Tag, Personen, Platz und Menü wählen, der Zettel rechnet mit den Preisen der Karte.', ''),
    ('impressum.html', 'Rechtliches', 1, 'Impressum, Datenschutz, AGB und der Bildnachweis.', 'recht'),
]
LANG = {'Startseite': 'Startseite', 'Banketts & Gruppen': 'Banketts und Gruppen', 'Rechtliches': 'Rechtliches und Bildnachweis'}
KURZNAME = {'Banketts & Gruppen': 'Banketts'}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import namen_fall as _nf  # noqa: E402


def _werkzeugname(teil):
    """Name eines Werkzeugs aus der einen Stelle (_werkzeuge/oberflaeche/kleid/schloessli.js › namen, Schreiber schloessli-maison), nie fest geschrieben."""
    k = open(os.path.join(KLEID, 'schloessli.js'), encoding='utf-8').read()
    return dict(_re.findall(r"(\w+): '([^']+)'", _re.search(r'namen:\s*\{([^}]*)\}', k).group(1)))[teil]


# ---------- Unterlagen: die Karten des Hauses (Station 10, Kartenmacher; PDFs in unterlagen/pdf, sb_karten.py) ----------
SATZ_FUSS = ADRESSE
UNTERLAGEN = dict(
    pflege=('Karten selbst ändern', 'http://127.0.0.1:9283/_werkzeuge/carte/'),
    text='Zum Schlössli gehören die Karte nach Ländern, die Karte der Lästermeile, das Lunch-Menü der Woche, die Bankettmenüvorschläge und die Weinkarte. Alle sind als Idee neu gesetzt, in Ihrer eigenen Machart, jede neben Ihrer heutigen Fassung.',
    seite_text='Die Karte nach Ländern, die Lästermeile, das Lunch-Menü, die Bankettmenüvorschläge und die Weinkarte, jede als Idee neu gesetzt, in Ihrer eigenen Machart. Links steht Ihre heutige Fassung, rechts die neue. Jede Karte pflegt Ihr Team ' + _nf.in_(_werkzeugname('karten')) + '.',
    knopf2=('Karte auf der Website', '../karte.html'))
try:   # die Karten im Fächer aus dem Plan von Werkbank Papier (unterlagen.json), nur Karten mit PDF, höchstens vier
    _UP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unterlagen.json'), encoding='utf-8'))
except Exception:
    _UP = []
_KURZ_K = {'speisekarte': 'Die Karte', 'lunch': 'Lunch', 'laestermeile': 'Lästermeile', 'bankett': 'Bankett', 'weinkarte': 'Wein'}   # kurz, damit die Aufschrift am Handy ganz bleibt
FAECHER = [(_x['ziel'], next(v for k, v in _KURZ_K.items() if k in _x['ziel'])) for _x in _UP if any(w in _x['ziel'] for w in ('speisekarte', 'laestermeile', 'lunch', 'bankett', 'weinkarte'))
           and os.path.exists(os.path.join(ROOT, 'unterlagen', 'pdf', _x['ziel'] + '.pdf'))][:4]

# ---------- Auftakt, Brief (alter Schlössli-Stand, 19.10.2026) ----------
AUFTAKT = dict(
    titel=['Ein Tisch', 'am Wasser.'],
    text='Für die Wirtschaft am Schlössli liegt hier die neue Website als Entwurf, und um sie herum Ihre Karten, neu gesetzt, sieben Werkzeuge für Ihr Team und einiges für die Tische am Hafen.',
    abzuege=[(bild('platanen'), 'Unter den Platanen'), (bild('bar'), 'An der Lästermeile'), (bild('tortelloni'), 'Tortelloni')])
BRIEF = dict(
    art='kurz',
    bild=bild('bootshafen'), schnitt=2.0, lage=(.5, .55), bild_alt='Der Bootshafen von Bottighofen, dahinter die Wirtschaft am Schlössli und das Schlössli',
    schild=('Wirtschaft am Schlössli', 'Bottighofen · am Hafen'), ort='Tasty Studios',
    absaetze=[
        'Blaue Stühle auf Kies, Platanen darüber und der See bis zu den Alpen: Wer bei Ihnen draussen sitzt, bleibt gern länger als geplant. Dieses Gefühl soll man auf der neuen Seite haben, noch bevor man einen Tisch reserviert.',
        'Ich bin Robert Reff, komme selbst aus der Gastronomie und baue heute in Hamburg Websites für Restaurants und Hotels. Beim Schlössli hat mich zuerst die Küche neugierig gemacht: Monika Huber kocht seit April 2025 am See, und GaultMillau nennt sie die Entdeckung des Jahres 2026.',
        'Auf Ihrer heutigen Seite findet man davon wenig. Die neue erzählt es: die Karte nach Ländern, die Lästermeile, den Keller von Jonas Volpert und den Besen, der Ende des 17. Jahrhunderts statt eines Wirtshausschilds am Haus am See hing. Reserviert wird weiter über Ihr gastronovi.',
        'Dazu gehören Ihre Karten, neu gesetzt in Ihrer eigenen Machart, Werkzeuge, mit denen Ihr Team Karte, Anlässe und Anfragen selbst pflegt, und ein paar Dinge für die Tische. Jedes Werkzeug lässt sich hier gleich öffnen und ausprobieren.'],
    schluss=f"<q>{HAUS['satz_lage']}</q> <small>{NAME}</small>",
    abzuege=[])
GABEN = dict(seite='{n} Seiten.', unterlagen='Ihre Karten.', papier='{d} Drucksachen und {e} Untersetzer.', feed='{n} Beiträge.', gaeste='Für Ihre Gäste.', studio='')
GABEN_BILDER = dict(seite=(bild('start'), (.5, .5)), unterlagen=(bild('thon'), (.5, .5)), papier=(bild('fliesen'), (.5, .5)), material=(bild('wein'), (.5, .5)), gaeste=(bild('abend'), (.5, .5)))
LAUFWORTE = ['Wirtschaft am Schlössli', '<b>Bottighofen</b>', 'Direkt im Hafen', 'Lästermeile', '<b>Tapas durchgehend</b>', 'Mit Blick aufs Wasser und die Alpen']
REIHENFOLGE = ['brief', 'vergleich', 'ideen', 'gefuege', 'seiten', 'unterlagen', 'handschrift', 'papier', 'material', 'dazu', 'schluss']   # der Feed kommt als eigene Bühne (feed_buehne.py)

# ---------- Website: Ideen (Aufnahmen _werkbank/sb_ideen.js → ansichten/Ideen), Vergleich (sb_heute.py → ansichten/Vorher) ----------
IDEEN = [   # (Aufnahme, Titel, Satz, Ausschnitt): jeder Satz nur aus dem, was auf der Aufnahme zu sehen ist
    ('Ideen/start', 'Am Tisch, von oben', 'Ein Teller auf dem blauen Platzteller in der Mitte, links «Am», rechts «Tisch.», darunter die Tage und die Zeiten. Reserviert wird oben rechts.', '50% 50%'),
    ('Ideen/willkommen', 'Ihr Willkommen', 'Ihr Satz «Willkommen in der Wirtschaft am Schlössli!» neben den blauen Stühlen, darunter Christian Kuchler, Monika Huber und Jonas Volpert mit Namen.', '50% 50%'),
    ('Ideen/laestermeile', 'Die Lästermeile hat ihr Band', 'Das Band aus Ihren Zementfliesen läuft über die Seite, darunter die Tapas, die es den ganzen Tag gibt.', '50% 50%'),
    ('Ideen/karte', 'Vier Länder auf einer Karte', 'Frankreich, Italien, die Iberische Halbinsel und die Klassiker, jedes mit seinem eigenen Zeichen.', '50% 50%'),
    ('Ideen/kueche', 'Die Entdeckung des Jahres', 'Monika Huber und ihr Weg an den See, daneben die Auszeichnungen mit ihrer Quelle.', '50% 50%'),
    ('Ideen/keller', 'Der Keller von Jonas Volpert', 'Ihr Gastgeber und Sommelier und die Weine der Karte, vom Thurgau bis Pauillac, daneben der Weg zum Weinberater.', '50% 50%'),
    ('Ideen/besen', 'Ein Besen statt eines Schilds', 'Die Geschichte vom Haus am See seit dem 17. Jahrhundert, mit der Zeichnung, der alten Anzeige und dem Luftbild von 1954.', '50% 50%'),
    ('Ideen/laender', 'Die Karte, Gericht für Gericht', 'Auf der Seite «Die Karte» stehen Name, Beschreibung und Preis untereinander, das Bild wechselt die Seite.', '50% 50%'),
    ('Ideen/mittag', 'Das Lunch-Menü der Woche', 'Die drei Gänge und der Preis als kleine Menükarte, dazu Bilder vom Mittag am Hafen.', '50% 50%'),
    ('Ideen/etagen', 'Ihr Menü, Gericht für Gericht', 'Auf «Banketts & Gruppen» steht jedes Bankettmenü mit seinen Gängen und Preisen, die Anfrage gleich daneben.', '50% 50%'),
    ('Ideen/naechster', 'Four Hands auf dem Schiff', 'Das Dinner mit Dieter Koschina an Bord der Excellence, Teller zuerst, dann Zeit und Anfrage.', '50% 50%'),
    ('Ideen/schaefli', 'Die Taverne zum Schäfli', 'Das Schwesterhaus in Wigoltingen mit Sternen und Punkten und dem Gutschein für beide Häuser.', '50% 50%'),
]
VORHER = [
    ('startseite', 'Startseite', 'Der Tisch zuerst, die Auszeichnungen gleich darunter.',
     ['Heute steht oben ein Foto mit der Leiste darüber. Neu öffnet die Seite mit einem Teller am Tisch, den Tagen und den Zeiten.',
      'Die Entdeckung des Jahres 2026 und die 15 Punkte stehen jetzt auf der Startseite, nicht erst im Fuss.',
      'Danach Terrasse, Hafen, Lästermeile, die Karte nach Ländern, Küche, Keller und der Besen.'], 'index.html'),
    ('karte', 'Die Karte', 'Die Karte auf der Seite, nicht nur als PDF.',
     ['Heute öffnet sich die Karte als PDF. Neu steht jedes Gericht mit Preis auf der Seite, nach Ländern.',
      'Zu jedem Gericht schlägt «Ein Glas zu jedem Gang» drei Weine aus Ihrer Karte vor.',
      'Das Lunch-Menü und die Lästermeile haben eigene Abschnitte, die PDFs gibt es weiter.'], 'karte.html'),
    ('events', 'Events', 'Was kommt, was war.',
     ['Das Four-Hands-Dinner auf der Excellence steht gross oben, mit Teller, Zeit und Anfrage.',
      'Das Jahr am Hafen als Band: jeder Termin als Platte, die Plätze fragt man im Fenster an.',
      'Unter «Was war» bleiben die vergangenen Abende mit ihren Fotos.'], 'anlaesse.html'),
    ('team', 'Über uns', 'Ein Blick in die Küche.',
     ['Ein Blick in die Küche mit vier Bildern, dazu Ihr Team mit Namen und Rollen.',
      'Die Taverne zum Schäfli steht als Schwesterhaus da, mit dem Gutschein für beide Häuser.',
      'Monika Huber, Jonas Volpert und Lukas Siebel mit Foto, dazu Marco Reisinger und Ole Sass.'], 'team.html'),
    ('kontakt', 'Kontakt', 'Anreise über Land und über das Wasser.',
     ['Zeiten, Ruhetage und Betriebsferien stehen oben, so wie Sie sie angeben.',
      'Anfahrt mit Parkplatz und Bahnhof, dazu die Schifflände für Gäste, die mit dem Boot kommen.',
      '«Der See heute» rechnet den Sonnenuntergang des Tages aus und sagt, ob die Terrasse offen ist.'], 'kontakt.html'),
]
VERGLEICH_TEXT = 'Links Ihre Seite von heute, rechts die neue. Den Griff schieben Sie hin und her, und daneben steht, was sich geändert hat.'


def gefuege(z):
    n = [
        ['fotos', 0, 0, 'Ihre Fotos', 'Website, Instagram, Portale', 'ein', 'Ihre Fotos', 'Die Aufnahmen von Ihrer Website, aus Instagram und von MySwitzerland, dazu wenige freie Fotos mit Namensnennung.', ['Terrasse', 'Küche', 'Hafen']],
        ['zeichen', 0, 1, 'Logo und Zeiger', 'von Ihrem Logo', 'ein', 'Ihr Logo', 'Die Zeiger aus Ihrem Logo, nachgezeichnet, und Ihr Name in Versalien.', ['Zeiger', 'Name']],
        ['karten', 0, 2, 'Ihre Karten', 'als PDF', 'ein', 'Ihre Karten', 'Speisekarte, Lästermeile, Lunch-Menü, Bankettmenüvorschläge und Weinkarte. Aus ihnen stammt jede Zeile auf der Seite «Die Karte».', ['Speisekarte', 'Lästermeile', 'Wein']],
        ['texte', 0, 3, 'Ihre Texte', 'Ihre Worte', 'ein', 'Ihre Texte', 'Willkommen, Küche, Terrasse, Banketts: Die neue Seite sagt es mit Ihren eigenen Sätzen.', ['Willkommen', 'Banketts']],
        ['presse', 0, 4, 'Auszeichnungen', 'mit Quelle', 'ein', 'Auszeichnungen', 'GaultMillau, Falstaff und Guide Michelin, jede Auszeichnung mit Quelle und Datum.', ['15 Punkte', 'Entdeckung 2026']],
        ['geschichte', 0, 5, 'Der Besen', 'Gemeindebuch 1994', 'ein', 'Die Geschichte vom Besen', 'Aus «Die Bottighofer Mühlen und das Schlössli am See» der Gemeinde Bottighofen, 1994.', []],
        ['bildwelt', 1, 0, 'Bildwelt', 'jedes Foto mit festem Platz', '', 'Bildwelt', 'Jedes Foto liegt in mehreren Grössen vor, für den Rechner und fürs Handy, und sitzt mit seinem Horizont auf der Linie der Seite.', ['Horizont', 'Grössen']],
        ['muster', 1, 1, 'Zeiger und Raster', 'auf den dunklen Flächen', '', 'Zeichen und Muster', 'Die Zeiger stehen in der Leiste und zwischen den Abschnitten, das Punktraster liegt Ton in Ton auf den dunklen Flächen.', ['Leiste', 'Flächen']],
        ['kartendaten', 1, 2, 'Karten-Daten', 'eine Stelle', '', 'Karten-Daten', 'Alle Gerichte und Preise an einer Stelle. Daraus entstehen die Karte auf der Seite und die PDFs.', ['Gerichte', 'Preise', 'Allergene']],
        ['weindaten', 1, 3, 'Wein-Kärtchen', 'jeder Wein der Karte', '', 'Wein-Kärtchen', 'Jeder Wein der Weinkarte als Kärtchen mit Herkunft, Rebsorte und Preis. Daraus entstehen der Weinberater und «Ein Glas zu jedem Gang».', ['Herkunft', 'Rebsorte']],
        ['neugesetzt', 1, 4, 'Karten neu gesetzt', 'als Idee', '', 'Karten neu gesetzt', 'Die Karten als Idee neu gesetzt, in Ihrer eigenen Machart, jede neben Ihrer heutigen Fassung zum Durchblättern.', []],
        ['zeitstrahl', 1, 5, 'Besen und Luftbild', 'Ende 17. Jh. und 1954', '', 'Geschichte', 'Der Besen, der statt eines Schilds hing, und das Strandhotel Schlössli aus der Luft, 1954.', []],
        ['start', 2, 0, 'Startseite', 'der Tisch zuerst', 'seite', 'Startseite', 'Vom Tisch über die Terrasse und den Hafen zur Lästermeile, zur Karte, zu Küche und Keller. Von hier führt ein Weg zu jeder Seite.', ['Terrasse', 'Lästermeile', 'Küche']],
        ['karte', 2, 1, 'Die Karte', 'nach Ländern', 'seite', 'Die Karte', 'Die Karte nach Ländern, ein Glas zu jedem Gang, das Lunch-Menü und die Lästermeile; dazu die Weinkarte.', ['Länder', 'Lunch', 'Wein']],
        ['feiern', 2, 2, 'Banketts', 'zwei Etagen', 'seite', 'Banketts & Gruppen', 'Zwei Etagen für je bis zu 26 Personen, die Bankettmenüs und die Anfrage im Fenster.', []],
        ['anlaesse', 2, 3, 'Events', 'was kommt, was war', 'seite', 'Events', 'Four Hands auf der Excellence, das Jahr am Hafen und was war.', []],
        ['haus', 2, 4, 'Über uns', 'und Kontakt', 'seite', 'Über uns und Kontakt', 'Das Team, die Küche, das Schäfli, Zeiten, Anfahrt und der See heute.', []],
        ['reservation', 3, 0, 'Reservation', 'gastronovi bleibt', 'sys', 'Reservation', 'Reserviert wird weiter über Ihr gastronovi; die Anfrage im Fenster nimmt zusätzlich Platz, Flasche und Allergien mit.', []],
        ['anfragen', 3, 1, 'Anfragen', 'ins Werkzeug', 'sys', 'Anfragen', 'Bankett, Plätze für einen Abend und Gutschein fragt der Gast über ein Fenster an. Die Anfrage kommt im Werkzeug für die Anfragen an, nie als Mail.', []],
        ['pdf', 3, 2, 'Karten als PDF', 'zum Ausdrucken', 'sys', 'Karten als PDF', 'Jede Karte liegt zusätzlich als PDF bereit.', []],
        ['studio', 3, 3, 'Sieben Werkzeuge', 'für Ihr Team', 'sys', 'Sieben Werkzeuge', 'Mit ihnen ändert Ihr Team Zeiten, Anlässe, Texte, Bilder und Karten selbst; jede Änderung wartet als Entwurf.', ['Zeiten', 'Anlässe', 'Texte und Bilder']],
    ]
    k = [['fotos', 'bildwelt'], ['zeichen', 'muster'], ['karten', 'kartendaten'], ['karten', 'weindaten'], ['karten', 'neugesetzt'], ['presse', 'start'], ['texte', 'start'], ['geschichte', 'zeitstrahl'],
         ['bildwelt', 'start'], ['bildwelt', 'anlaesse'], ['muster', 'start'], ['kartendaten', 'karte'], ['weindaten', 'karte'], ['kartendaten', 'feiern'], ['zeitstrahl', 'start'], ['neugesetzt', 'karte'],
         ['start', 'reservation'], ['karte', 'pdf'], ['feiern', 'anfragen'], ['anlaesse', 'anfragen'], ['studio', 'start'], ['studio', 'anlaesse'], ['studio', 'haus']]
    return {'sp': ['Von Ihnen', 'Daraus gemacht', 'Die Seiten', 'Im Hintergrund'], 'fx': [0.118, 0.372, 0.628, 0.882], 'n': n, 'k': k,
            'tour': ['fotos', 'karten', 'presse', 'reservation', 'anfragen', 'studio'], 'fuss': 'Folgen Sie einer Linie: Sie führt von dem, was von Ihnen kommt, zur Seite',
            'start': ['Übersicht', 'Von Ihnen zur Seite', 'Tippen Sie eine Kachel an, dann leuchtet ihr Weg. Oder starten Sie den Rundgang.']}


# ---------- Für Ihre Gäste (Gäste-Funktionen der Website, Aufnahmen sb_ideen.js → ansichten/Gaeste) ----------
GAESTE = [
    ('reservation', 'Reservieren mit Wünschen', 'Im Fenster wählt der Gast Tag, Uhrzeit, Personen und Platz, legt eine Flasche bereit und nennt Allergien aus Ihrer Karte. Direkt reservieren geht weiter über gastronovi.', '50% 50%'),
    ('berater', 'Der Weinberater', 'Art, Herkunft, Rebsorte und Preis antippen, dann stehen die passenden Weine Ihrer Karte als Kärtchen da und lassen sich zur Reservation bereitlegen.', '50% 50%'),
    ('wein-gang', 'Ein Glas zu jedem Gang', 'Ein Gericht antippen, drei Flaschen aus derselben Gegend erscheinen als Kärtchen, alle aus Ihrer Weinkarte.', '50% 50%'),
    ('abend', 'Den Abend zusammenstellen', 'Anlass, Tag, Personen, Platz und Menü wählen, der Zettel rechnet mit den Preisen Ihrer Karte mit und geht als Anfrage an Ihr Team.', '50% 0'),
    ('bankett', 'Bankettmenüs für Ihre Feier', 'Frühling, Sommer und Herbst, jedes Menü mit seinen Gängen aus Ihren Bankettmenüvorschlägen; die Anfrage geht gleich daneben im Fenster an Ihr Team.', '50% 50%'),
    ('gutschein', 'Gutschein gestalten', 'Betrag, Haus, für wen, von wem und ein Satz: Die Karte entsteht im Kleid des Hauses, für das Schlössli, das Schäfli oder beide.', '50% 30%'),
    ('kalender', 'Plätze für einen Abend', 'Das Jahr am Hafen als Band, jeder Termin mit seinen Angaben. Plätze fragt man im Fenster an.', '50% 50%'),
    ('see', 'Der See heute', 'Der Sonnenuntergang des Tages, aus dem Sonnenstand gerechnet, und ob die Terrasse offen ist, nach Ihren Zeiten und Ferien.', '50% 50%'),
]
GAESTE_TEL = []
GAESTE_KNOEPFE = [('Weinberater', '../weinkarte.html#berater'), ('Ihr Abend', '../abend.html'), ('Gutschein gestalten', '../gutschein.html')]
GAESTE_LINK = '../abend.html'
GABEN['gaeste'] = 'Reservieren mit Wünschen, Weinberater, Bankettmenüs, Gutschein und der See heute.'

# ---------- Handschrift (marke_werkbank.py) ----------
HANDSCHRIFT = dict(
    text='Ihre Zeiger und Ihr Name bleiben, wie man sie kennt. Dazu kommen die Schrift Ihres Logos für die grossen Zeilen, in Versalien, eine ruhige für den Lesetext und die Farben von Ihrer Terrasse: das Blau der Stühle, der Himmel über dem See und das Rot der Schirme als einziger Punkt.',
    marke_etik='Zeiger und Name', marke_text='Die Zeiger aus Ihrem Logo sind nachgezeichnet und bleiben in jeder Grösse scharf. Die Nabe der Zeiger ist das Ö in Ihrem Namen.',
    schriften=[], farben=[], farben_etik='von Ihrer Terrasse',
    muster_etik='Das Punktraster',
    muster_text='Auf den dunklen Flächen liegt ein feines Punktraster, Ton in Ton. Man findet es auf der Seite, auf den Karten und auf jeder Drucksache.',
    knopf_text='Diese Knöpfe darf man drücken.', knoepfe=('Ausprobieren', 'Noch einmal'))

# ---------- Feed, Papier, Dateien (Inhalte der Beigaben: Werkbank Papier und Werkbank Feed; hier nur, was der Kit für die Werkbank selbst braucht) ----------
FEED = dict(art='bogen', bogen=[1, 2, 3, 4, 5, 6, 7, 8, 9], bogen_zeile='Die ersten drei Reihen',
            text1='', text2='Tippen Sie auf den Bildschirm, dann scrollen Sie durch den Feed wie am Handy.', kacheln=[])
PAPIER = dict(
    etik_text='An der Lästermeile gehen den ganzen Tag Gläser über die Theke. Dazu passen Untersetzer: zwölf Ideen mit Ihren Fliesen, den Zeigern und den Tapas der Karte.',
    druck_text='Von der Tischkarte bis zum Aushang für die Betriebsferien, dazu <a href="../sticker/index.html" target="_blank" rel="noopener">Sticker</a> und <a href="../beigaben/index.html" target="_blank" rel="noopener">Beigaben</a>.',
    orte_e=[(3, 6, 28, -3), (36, 6, 28, 2), (69, 6, 28, -2), (3, 54, 28, 2), (36, 54, 28, -3), (69, 54, 28, 3)],   # drei mal zwei mit Abstand, nichts überdeckt (Robert 29.10.2026)
    orte_d=[('menuekarte', 3, 16, 29, -3, 0), ('tischkarte', 35.5, 16, 29, 2, 0), ('einladung', 68, 16, 29, -2, 0)])   # drei Blätter nebeneinander (Robert 29.10.2026)
PAPIER_SEITE = dict(
    breit={'gutschein', 'gutschein-r', 'tischkarte', 'tischkarte-r', 'couvert', 'briefbogen', 'menuekarte', 'menuekarte-r', 'aushang'},
    formen=set(),
    auslage=[('menuekarte', 0, 2, 24, -6), ('gutschein', 36, 40, 52, -3), ('tischkarte', 2, 58, 32, -4), ('aushang', 80, 4, 19, 7)],
    karton={}, titel={}, schatten=set(),
    flaeche=['fl--papier', 'fl--nacht tapete-leicht', 'fl--papier', 'fl--creme'],
    etik_titel=('Untersetzer', 'für die Lästermeile.'),
    etik_text='An der Lästermeile gehen den ganzen Tag Gläser über die Theke. Hier sind {n} Untersetzer als Idee, rund und quadratisch, mit Ihren Zementfliesen, den Zeigern und den Tapas der Karte.',
    etik_kap='Die Untersetzer', etik_kopf=['Zwölf', 'Untersetzer.'],
    etik_kopftext='Das Blau der Stühle, der Himmel über dem See und das Rot der Schirme kommen von Ihrer Terrasse, die Fliese von Ihrer Bar, die Worte von Ihrer Karte.',
    druck_text='Dinge, die bei Ihnen auf dem Tisch, an der Tür oder in der Post liegen könnten. Nehmen Sie davon, was Ihnen gefällt.',
    etik_auslage=[(0, 4, 26, -7), (30, 0, 22, 5), (56, 6, 26, -4), (66, 42, 24, 6), (6, 40, 22, 6), (30, 38, 26, -5), (0, 0, 0, 0), (0, 0, 0, 0), (62, 72, 22, 4), (0, 0, 0, 0), (0, 0, 0, 0), (26, 72, 26, 3)])
# Weitere Drucksachen: Karton, Titel und Breite je Stück aus papier_neu_seite.json (geschrieben von Werkbank Papier)
try:
    for _k, _v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'papier_neu_seite.json'), encoding='utf-8')).items():
        PAPIER_SEITE['karton'][_k] = (_v['karton'][0], [tuple(x) for x in _v['karton'][1]]); PAPIER_SEITE['titel'][_k] = _v['titel']
        PAPIER_SEITE['breit'].update(_v['breit']); PAPIER_SEITE['schatten'].add(_k)
except (FileNotFoundError, KeyError, ValueError, TypeError):
    pass
MATERIAL = dict(
    text='Was für den Entwurf neu entstanden ist, liegt sortiert in einem Ordner: die Karten als PDF, die Drucksachen, die Untersetzer, die Sticker, die Beigaben, die Postkarten, die Beiträge für Instagram und Ihr Zeichen als Datei.',
    streu=[(bild('lounge'), 'Am Ufer', -4, '-0.05'), (bild('regal'), 'An der Bar', 3, '0.04'), (bild('suppe'), 'Aus der Küche', -2, '-0.07'), (bild('dessert'), 'Zum Schluss', 4, '0.05'), (bild('apero'), 'Blaue Stunde', -3, '-0.04')],
    druck_satz='Tischkarte, Menükarte, Gutschein, Aushang, Einladung und Briefpapier.',
    zeichen=[('Die Zeiger', '../../_werkzeuge/oberflaeche/kleid/schloessli-zeichen.svg', 'Wirtschaft am Schlössli Zeichen.svg')],
    zeichen_satz='Die Zeiger als Zeichnung, die in jeder Grösse scharf bleibt.',
    auslage=[])
AUSBLICK = dict(text='Ein paar Dinge fehlen noch.', gross=('', '', ''), punkte=[], studio='')
SCHLUSS = dict(bild=bild('abend'))
KAPITEL = {
    'vergleich': dict(text=VERGLEICH_TEXT),
    'ideen': dict(text='Zu jeder Stelle der Seite gibt es einen Grund. Zwölf davon stehen hier, aufgenommen auf der Seite, wie sie heute aussieht.'),
    'gefuege': dict(text='Ein Blick hinter die Seiten: links, was von Ihnen kommt, in der Mitte, was daraus geworden ist, rechts die Seiten und was im Hintergrund mitläuft.'),
    'seiten': dict(text='Eine Seite aussuchen, mit den Pfeilen weiterblättern. Rechts dieselbe Stelle am Handy, mit «Öffnen» sind Sie auf der echten Seite.'),
    'unterlagen': dict(text=UNTERLAGEN['text']),
    'gaeste': dict(text='Was ein Gast auf der Seite selbst erledigt, bevor er anruft: reservieren, einen Wein aussuchen, den Abend planen, einen Gutschein gestalten. Alles rechnet mit Ihren Zahlen und lässt sich ausprobieren.'),
    'papier': dict(text='Zum Hafen sind mir ein paar Dinge eingefallen: Untersetzer für die Lästermeile, Drucksachen von der Tischkarte bis zum Aushang, Mails an Ihre Gäste und Postkarten vom Hafen. Nehmen Sie, was Ihnen gefällt.'),
    'material': dict(text='Die Karten als PDF, die Drucksachen, die Untersetzer und Ihr Zeichen als Datei: alles Neue liegt in einem Ordner beisammen.'),
    'geprueft': dict(text='Bevor Sie etwas davon sehen, ist jedes Teil durchgegangen worden: die Website auf jedem Gerät, die Karten Wort für Wort, jedes Werkzeug Knopf für Knopf. Auf dem Blatt steht das Wichtigste, der Rest auf einer eigenen Seite.'),
    'schluss': dict(text='Sagen Sie mir offen, was Ihnen am Entwurf gefällt und was nicht. Ändern lässt sich alles.'),
}
MEINS = ['Der Brief und alle Sätze der Werkbank', 'Titel und Sätze zu den Ideen, zum Gefüge, zu den Drucksachen und Untersetzern', 'Bildzeilen der Postkarten, Feldnamen, das Wort «Reserviert»', 'Texte zu den Beiträgen des Feeds']

# ---------- Geprüft (nur Belegtes: Prüfung der Werkzeuge im Nachtbau, Station 07/10 der Kette; Werkzeuge aus ihren Lieferungen) ----------
import datetime as _dt
GEPRUEFT = [
    ('Die Website', 'seite', ['Alle Seiten in der Technik von Safari und von Chrome, vom Handy bis zum grossen Bildschirm: nichts läuft seitlich über, kein Skriptfehler, kein kaputtes Bild.',
                              'In vier Breiten angesehen, von 390 bis 1440 Pixeln.',
                              'Jede Angabe kommt aus einer Stelle mit Quelle: Zeiten, Adresse, Sätze, Team und Auszeichnungen.']),
    ('Die Karten', 'karte', ['Jede Karte aus Ihren PDFs gelesen, nicht abgetippt; die Weinkarte Zeile für Zeile gegen das Original gezählt.',
                             'Was Sie klären müssen, steht gesondert in der Liste der offenen Punkte.']),
    ('Die Werkzeuge', 'schloss', ['Jedes der sieben Werkzeuge in einem eigenen Durchgang gebaut und Knopf für Knopf bedient, nur mit erfundenen Daten.',
                                  'Kein Werkzeug verschickt etwas von selbst, keines öffnet ein Mailprogramm.']),
]
GEPRUEFT_PUNKTE = [
    ('Die Website', 'Alle Seiten am Handy und am Rechner geöffnet, in der Technik von Safari und von Chrome, in vier Breiten. Nichts läuft über, kein Bild fehlt.'),
    ('Die Karten', 'Jede Zeile kommt aus Ihren PDFs, nicht abgetippt. Die Weinkarte ist Zeile für Zeile gegen das Original gezählt.'),
    ('Die Werkzeuge', 'Alle sieben Werkzeuge einzeln gebaut und ausprobiert, nur mit erfundenen Daten. Von sich aus verschickt keines etwas.'),
    ('Ihre Daten', 'Die Website setzt für Gäste keine Kekse. Anfragen gehen über Fenster auf der Seite an Ihr Team, im Entwurf nie an das echte Haus.'),
]
GEPRUEFT_TRIO = [(bild('glas'), 1.6, (.5, .5), 'Am Wasser'), (bild('sauce'), 1.6, (.5, .5), 'In der Küche'), (bild('ig-luft'), 1.6, (.5, .5), 'Von oben')]
GEPRUEFT_OFFEN = 'Offen bleibt, was nur Sie wissen: die Rechte an einigen Fotos von Gästen und Partnern, Ihr Blick auf die Auswahl der Bilder und wer welches Werkzeug bekommt.'
GEPRUEFT_EIN = 'Bevor Sie etwas davon sehen, ist es durchgegangen worden: die Website auf jedem Gerät, die Karten Zeile für Zeile, jedes Werkzeug Knopf für Knopf. Hier steht, was genau, ohne Fachwörter. Was offen bleibt, steht auch da.'
GEPRUEFT_NAV = ['Website', 'Karten', 'Werkzeuge', 'Daten', 'Offen']
GEPRUEFT_MEHR = [
    ('Die Website', 'seite', 'Neun Seiten von der Startseite bis zu «Ihr Abend», dazu das Rechtliche mit Bildnachweis.', [
        'Am Handy und am Rechner, in Safari- und Chrome-Technik: nichts läuft seitlich über, kein Skriptfehler, kein kaputtes Bild.',
        'In vier Breiten angesehen, von 390 bis 1440 Pixeln. Beim Laden springt nichts, beim Scrollen ruckelt nichts.',
        'Jede Angabe steht an einer einzigen Stelle mit ihrer Quelle; jede Seite liest von dort. Freie Fotos tragen ihre Namensnennung, gesammelt im Bildnachweis.']),
    ('Die Karten', 'karte', 'Die Karte nach Ländern, die Lästermeile, der Lunch, die Bankettmenüs und die Weinkarte.', [
        'Jede Karte aus Ihren PDFs gelesen, nicht abgetippt. Die Weinkarte ist Zeile für Zeile gegen das Original gezählt.',
        'Neu gesetzt in Ihrer eigenen Machart, mit fest eingebetteten Schriften.']),
    ('Die sieben Werkzeuge', 'schloss', 'Sieben Werkzeuge, mit denen Ihr Team die Seite selbst führt.', [
        'Jedes Werkzeug in einem eigenen Durchgang gebaut und Knopf für Knopf bedient, mit Probe-Daten, nie mit Ihren echten.',
        'Jedes Werkzeug ging durch die Prüfung in vier Breiten (1440, 1280, 1000 und 390 Pixel): Start, jeder Reiter, jedes Fenster, mit dem Auge an den Bildern.',
        'Kein Werkzeug verschickt etwas von selbst und keines öffnet ein Mailprogramm: Antworten an Gäste bleiben als Brief im Werkzeug.']),
    ('Ihre Daten und die Ihrer Gäste', 'schild', 'Was die Seite speichert und was nicht.', [
        'Die Website setzt für Gäste keine Kekse. Im Entwurf zählt die Seite keine Besuche; ' + _nf.klein(_werkzeugname('besuche')) + ' zeigt Beispielwerte.',
        'Reservation, Bankett, Plätze und Gutschein schickt der Gast über ein Fenster auf der Seite; im Entwurf geht nichts an das echte Haus.',
        'Der Entwurf ist für Suchmaschinen gesperrt, bis Sie ihn freigeben.']),
    ('Was offen bleibt', 'auge', 'Diese Dinge liegen nicht in meiner Hand.', [
        'Einige Fotos stammen von Gästen und Partnern. Ob sie bleiben dürfen, klären wir mit Ihnen; freie Fotos tragen ihre Namensnennung.',
        'Die Werkzeuge stehen im Entwurf ohne Anmeldung. Bei der Auslieferung bekommt jedes eine Anmeldung und jede Person ihr eigenes Passwort.',
        'Die Seite spricht bisher Deutsch; weitere Sprachen folgen.'])]
PRUEFDATUM = _dt.date(2026, 11, 4)
STEMPEL_TEXT = f'GEPRÜFT · WIRTSCHAFT AM SCHLÖSSLI · {PRUEFDATUM:%d.%m.%Y} ·'
GEPRUEFT_BILD = bild('glas')

# ================================================================ Bausteine (Vorlage Culinarium über das Schäfli, kopiert und umgeschrieben; Kit unverändert)
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
EIGENE, EIGENE_BILDER, FLAECHE = [], [], {}
CSS = ''
_WB = os.path.join(ROOT, 'werkbank')

import brief_blatt as _bb  # noqa: E402
brief_abschnitt = _bb.abschnitt(globals())
EIGENE_BILDER += _bb.bilder(BRIEF)
CSS += _bb.CSS
import kopf_mitte as _km  # noqa: E402
import auftakt_kacheln as _ak  # noqa: E402
CSS += _km.CSS + _ak.CSS
FLAECHE.update(brief='fl--papier tapete-hell', vergleich='fl--nacht tapete-leicht', ideen='fl--blau tapete-leicht', gefuege='fl--nacht tapete-leicht',
               seiten='fl--papier tapete-hell', gaeste='fl--navy tapete', unterlagen='fl--tief tapete-leicht', papier='fl--navy tapete', material='fl--papier tapete-hell',
               feed='fl--nacht tapete-leicht', geprueft='fl--navy tapete')
CSS += '''
/* ---------- Leichte Tapete: das Punktraster der Website auf jeder dunklen Fläche ---------- */
.tapete-leicht{background-image:linear-gradient(var(--tl),var(--tl)),var(--muster);background-size:auto,var(--musterb) auto;background-position:0 0,50% 0}
.fl--nacht.tapete-leicht{--tl:rgba(11,29,61,.42)}
.fl--blau.tapete-leicht{--tl:rgba(17,61,136,.36)}
.fl--tief.tapete-leicht{--tl:rgba(8,22,49,.42)}
.tapete-hell{background-image:url(/assets/svg/tapete-a-hell.svg);background-size:168px auto;background-position:50% 0}
/* ---------- Titel wie auf der Website: Open Sans 400 in Versalien, gesperrt wie die Wortmarke, nie fett, nie kursiv; Betonung nur über die Farbe ---------- */
.zt,.t1,.t2,.t3,.wfen__t,.ins-t h3,.rgw .wfa__texte h3,.sbf-text h3,.hs2-ww+small{font-weight:400!important}
.zt{text-transform:uppercase;letter-spacing:.12em}
.zt em,em{font-style:normal}
.kap--k .kap__geist{display:none}.kap--z span,.kap--k>span{font-family:var(--mono)!important;font-weight:400!important;font-size:12px!important;letter-spacing:.2em;text-transform:uppercase}
.wfen__t{text-transform:uppercase;letter-spacing:.12em}
h2,h3,.wege__t,.gb-blatt header h3,.rgw .wfa__texte h3,.fbz__n{font-weight:400!important}
b,strong{font-weight:500}
.wf .wege__t,.gb-blatt header h3{font-family:var(--serif);text-transform:uppercase;letter-spacing:.14em}
/* Gerichte wie auf der Karte (THON, CAVATELLI): DM Mono gesperrt */
.rz{font-family:var(--mono);font-weight:400;letter-spacing:.12em;text-transform:uppercase}
/* Schirmrot nur als Punkt: die Nabe der Zeiger in der Leiste */
.insel__m .hz{color:var(--gold)}
/* Abnahme-Tor 3.11.2026 (lokal, Chromium): gesperrte Versalien am Handy ohne Anschnitt («NEBENEINANDER.»), alle Zeilen des Auftakt-Fusses auf einer Kante,
   Nummer und Titel der Angebots-Blätter als eine Zeile, Ziffern im Register optisch mittig (Open Sans: I und V mit ungleichen Seitenrändern) */
@media(max-width:480px){.t2.zt,h2.zt{font-size:min(1.85rem,7.2vw)!important;letter-spacing:.07em!important}.t1.zt,h1.zt{font-size:min(2.3rem,8.6vw)!important;letter-spacing:.07em!important}}
@media(max-width:600px){.auftakt__fuss .runter i{display:none}.auftakt__fuss .runter{gap:0}}
.sag-h{display:block!important}.sag-h span{display:inline-block;margin-right:16px}
.rgc-p{letter-spacing:0!important}.rgc-p[data-i="3"]{padding-left:9.1px!important;padding-right:10.9px!important}.rgc-p[data-i="7"]{padding-left:10.6px!important;padding-right:9.4px!important}
@media(max-width:640px){#handschrift .hs2-her{grid-template-columns:minmax(0,1fr)!important}}
.sag-h::before{content:attr(data-n);display:inline-block;margin-right:16px;font-family:var(--mono);font-size:clamp(.78rem,.9vw,.92rem);letter-spacing:.16em;color:var(--blau);vertical-align:.3em}
@media(max-width:480px){.faecher .blattk span{flex-direction:column;gap:3px;font-size:9.5px;letter-spacing:.08em;white-space:nowrap}}
@supports (interpolate-size:allow-keywords){.ki-knoepfe .kn--klein>.tm{top:.5px!important}}   /* nur Chromium (Wild Side 1.11.: WebKit unter Linux kennt -apple-system-body nicht) */
/* «Läuft im Entwurf»: sieben Werkzeuge als Raster mit dem Zeichen vor jedem Namen, kein Trenner am Zeilenanfang */
@media(min-width:760px){#k8 .sag-sp--2 ul{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 clamp(18px,2vw,34px)}
  #k8 .sag-sp--2 li{display:flex;align-items:center;gap:12px}#k8 .sag-sp--2 li::before,#k8 .sag-sp--2 li+li::before{content:"";flex:none;width:.7em;height:.74em;background:var(--blau);-webkit-mask:url(eigen/zeichen-c.svg) center/contain no-repeat;mask:url(eigen/zeichen-c.svg) center/contain no-repeat}}
'''

import marke_werkbank as _mw  # noqa: E402
EIGENE.append(_mw.abschnitt(globals())); EIGENE_BILDER += _mw.BILDER; CSS += _mw.CSS
FLAECHE['handschrift'] = 'fl--navy tapete'
import mails_reihe as _mr  # noqa: E402
CSS += _mr.CSS
EIGENE_BILDER += _mr.BILDER   # die drei Mails als dritte Karte im Papier (wb_kapitel.papier_mails)
import feed_buehne as _fb  # noqa: E402
_FEED_DA = os.path.exists(os.path.join(ROOT, 'feed', 'feed.json'))
if _fb.BEREIT and _FEED_DA:
    EIGENE.append(_fb.abschnitt(globals())); EIGENE_BILDER += _fb.BILDER; CSS += _fb.CSS
import fenster_ausblick as _fa  # noqa: E402
CSS += _fa.CSS
import geprueft_blatt as _gb  # noqa: E402
geprueft_abschnitt = _gb.abschnitt(globals())
_AN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ansichten')
for _i, _q in enumerate([os.path.join(_AN, 'Rechner', 'Startseite.jpg'), (sorted(_glob.glob(os.path.join(ROOT, 'unterlagen', 'img', 'n-*speisekarte-01.webp'))) or [''])[0],
                         os.path.join(_AN, 'Werkzeuge', 'bureau.jpg'), os.path.join(_AN, 'Gaeste', 'reservation.jpg')]):
    if os.path.exists(_q):
        EIGENE_BILDER.append((f'gp-{_i}', _q, 320, dict(q=80, schnitt=4 / 3, lage=(.5, 0))))
CSS += _gb.CSS

import fuss_faecher as _ff  # noqa: E402
if _ff.BEREIT:
    wege_abschnitt = _ff.abschnitt
    CSS += _ff.CSS
CSS += '''
/* Dateien: Fotos ohne Polaroid-Rand und ohne Bildzeile, ungleich gross, ohne Drehung */
#material .streu .abzug{padding:0!important;background:none!important;border-radius:clamp(10px,1vw,14px);overflow:hidden;--r:0deg!important;--r0:0deg!important;box-shadow:0 30px 40px -26px rgba(4,16,35,.55),0 10px 16px -10px rgba(4,16,35,.3)!important}
#material .streu .abzug span{display:none!important}
#material .streu .abzug img{display:block;width:100%;height:100%;object-fit:cover;border-radius:0!important}
@media(min-width:760px){#material .streu{align-items:center}#material .streu .abzug:nth-child(3){transform:scale(1.18);z-index:2}#material .streu .abzug:nth-child(2),#material .streu .abzug:nth-child(4){transform:scale(1.04);z-index:1}}
/* Flüssigkeit (Regel 55): Abschnitte ausserhalb des Blicks werden nicht gezeichnet. Ausgenommen der Brief (überstehendes Blatt). */
@supports (content-visibility:auto){main>section.fl:not(#brief){content-visibility:auto;contain-intrinsic-size:auto 1400px}}
html.cv-alle main>section.fl:not(#brief){content-visibility:visible}
@media(min-width:760px){.vh-wahl>:first-child,#seiten .wahl>:first-child{margin-left:auto}.vh-wahl>:last-child,#seiten .wahl>:last-child{margin-right:auto}}
@media(max-width:480px){.kn{max-width:100%;height:auto;min-height:54px;padding-top:9px;padding-bottom:9px;white-space:normal;line-height:1.35;text-align:left}.kn i{flex:none}.kn-reihe{max-width:100%}}
.schluss .zt,.schluss .lauf p,.schluss .kap span{text-shadow:0 1px 2px rgba(4,16,35,.9),0 2px 16px rgba(4,16,35,.8),0 0 42px rgba(4,16,35,.55)}
'''


CV_JS = ("<script id=\"cv-hoehen\">(function(){var d=document.documentElement;function alle(){d.classList.add('cv-alle');requestAnimationFrame(function(){requestAnimationFrame(function(){d.classList.remove('cv-alle')})})}"
         "/* einmal alles zeichnen, damit jede Fläche ihre echte Höhe kennt: Sprungmarken landen genau (content-visibility) */"
         "if(document.readyState==='complete')setTimeout(alle,300);else addEventListener('load',function(){setTimeout(alle,300)});"
         "addEventListener('resize',function(){clearTimeout(alle.t);alle.t=setTimeout(alle,400)})})();</script>")
BRETT_HILFE = ("<script id=\"brett-hilfe\">(function(){var b=document.getElementById('brett'),k=document.getElementById('brett-noch');if(!b||!k||!('IntersectionObserver' in window))return;"
               "new IntersectionObserver(function(E,o){if(!E[0].isIntersecting)return;o.disconnect();setTimeout(function(){if(/\\bvor\\b/.test(b.className))k.click()},700)},{rootMargin:'0px 0px -35% 0px'}).observe(b)})();</script>")


def nach_bau():
    """Nach jedem Bau des Kits: Eigenes nach werkbank/eigen, Nacharbeit der Bausteine, Kapitel, Ruhe, Farben, Schweizer Schreibung."""
    import re as _re, shutil as _sh
    from PIL import Image as _I
    q, z = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen'), os.path.join(_WB, 'eigen')
    os.makedirs(z, exist_ok=True)
    sig = _I.open(os.path.join(q, 'unterschrift-robert.webp')).convert('RGBA')
    r, g, b = (int(FARBEN['tinte'][i:i + 2], 16) for i in (1, 3, 5))
    _I.merge('RGBA', (*_I.new('RGB', sig.size, (r, g, b)).split(), sig.getchannel('A'))).save(os.path.join(z, 'unterschrift.webp'), 'WEBP', quality=90)
    _fa.fenster_bilder()
    for f in os.listdir(q):
        if f.startswith('fen-'):
            _sh.copy2(os.path.join(q, f), os.path.join(z, f))
    if _fb.BEREIT and _FEED_DA:
        _fb.bilder()
    if _ff.BEREIT:
        _ff.bilder()
    seite = os.path.join(_WB, 'index.html')
    _ak.anwenden(seite)
    _mw.anwenden(seite)
    _fa.anwenden(seite)
    _km.anwenden(seite)
    import fluss_werkbank as _fw
    _fw.anwenden(seite)
    import wb_kapitel as _kp
    _kp.anwenden(seite)
    # Nichts läuft mit dem Scrollen mit (Regel 55)
    t = open(seite, encoding='utf-8').read()
    t = _re.sub(r'\sdata-(?:drift|zug)="[^"]*"', '', t)
    ruhe = ('<style id="sb-ruhe">.bf .bf-blatt[data-a="heben"],.bf .bf-blatt[data-a="heben"].da{animation:none!important}.kap__geist{animation:none!important}'
            '.kn:hover,.kn:active,.rund:hover,.rund:active,.wahl button:active,.vh-wahl button:active,.bn button:hover,.bn button:active,.glanz:active,.ins-r:hover,.ins-r:active,.wf__pf:hover,.wf__pf:active,.rgc-p:hover,.rgc-p:active,.sbf-z:hover{transform:none!important;translate:none!important;scale:none!important}'
            '.kn{overflow:hidden}.ins-reiter,.fb__reiter{padding-top:10px!important;padding-bottom:26px!important;margin-top:-10px!important;margin-bottom:-26px!important}'
            '.wahl,.vh-wahl{padding-top:8px!important;padding-bottom:26px!important;margin-top:-8px!important;margin-bottom:-12px!important}'
            '.wfen .wfen__t{font-size:clamp(24px,3.6vw,54px)!important;line-height:1.14!important}.wfen .wfen__k{font-size:clamp(15px,1.36vw,19px)!important}'
            '#papier img.frei{filter:none!important;box-shadow:none!important}</style>')
    if 'id="sb-ruhe"' not in t:
        t = t.replace('</head>', ruhe + '</head>', 1)
    if 'id="brett-hilfe"' not in t:
        t = t.replace('</body>', BRETT_HILFE + '</body>', 1)
    if 'id="cv-hoehen"' not in t:
        t = t.replace('</body>', CV_JS + '</body>', 1)
    import sb_skripte as _sk
    for _id, _js in (('rh-vorladen', _sk.VORLADEN_JS), ('rh-frueh', _sk.FRUEH_JS), ('rh-zurueck', _sk.WB_JS), ('rh-karussell', _sk.KARUSSELL_JS)):
        if f'id="{_id}"' not in t:
            t = t.replace('</body>', _js + '\n</body>', 1)
    open(seite, 'w', encoding='utf-8').write(t)
    # feed_leicht.py läuft nicht mehr hier: der Feed baut sich in feed_alles.sh selbst (mit feed_kleid.py danach; Werkbank Feed 3.11.2026)
    import sb_farbe
    sb_farbe.anwenden()
    # Die Zeiger in Seehimmel tief als Datei für die Karte «Ein Vorschlag.» (als <img> wäre currentColor schwarz)
    vb, innen = ZEICHEN
    open(os.path.join(_WB, 'eigen', 'zeichen-kerze.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="{FARBEN["taupe"]}">{innen}</svg>')
    open(os.path.join(_WB, 'eigen', 'zeichen-c.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="#000">{innen}</svg>')   # Maske für Schmuck im CSS (Listen, Namenszug)
    _ft = os.path.join(ROOT, 'feed', '_tafeln.html')
    if os.path.exists(_ft):
        _s = open(_ft, encoding='utf-8').read()
        if 'noindex' not in _s:
            _s = _s.replace('<head>', '<head><meta name="robots" content="noindex, nofollow">', 1) if '<head>' in _s else '<meta name="robots" content="noindex, nofollow">' + _s
            open(_ft, 'w', encoding='utf-8').write(_s)
    import ss_gang   # Schweizer Schreibung: ss statt ß in allem, was der Kit und die Vorlagen schreiben (vor der Karte, damit das PDF stimmt)
    ss_gang.anwenden(ROOT)
    import sb_ki   # Seite «KI und Ihre Daten», Karte «Ein Vorschlag.» allein und als PDF (Robert 20.10.2026)
    sb_ki.bau()
    ss_gang.anwenden(ROOT)
    import nur_bewegung   # bewegt nur transform/opacity, Glanzkante dreht statt neu zu malen, Karte kommt herein (Abnahme-Tor 30.10.2026)
    nur_bewegung.anwenden(ROOT)
    import zeile_ganz   # kein Einzelwort allein in der letzten Titelzeile, Aufschrift im Fensterstapel frei (Abnahme-Tor 30.10.2026)
    zeile_ganz.anwenden(ROOT)
    import text_mitte   # Schrift optisch mittig in den Knöpfen aller Werkbank-Seiten (Messlauf «text-mitte», 29.10.2026)
    text_mitte.anwenden(ROOT)
    import bild_mass   # Bilder in der gezeigten Grösse, damit der Tab in WebKit nicht am Speicher scheitert (Abnahme-Tor 4, 30.10.2026)
    bild_mass.anwenden(ROOT)
    import kleid_schloessli   # zuletzt: Reste der Vorlagen im Kleid des Hauses (Nachtbau 3.11.2026)
    kleid_schloessli.anwenden(ROOT)
    import importlib.util as _iu   # ruecksprung.py des Reviers, nicht das gleichnamige Skript des Kits (Robert 1.11.2026: Zurück landet auf der alten Höhe)
    _sp = _iu.spec_from_file_location('ruecksprung_wb', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ruecksprung.py'))
    _rs = _iu.module_from_spec(_sp); _sp.loader.exec_module(_rs)
    _rs.anwenden(ROOT)


TITEL_NEU = {   # eigene Überschriften des Schlössli (Werkbank-Regel 14; alter Schlössli-Stand vom 21.10.2026)
    ('Schön, dass Sie', 'hereinschauen.'): ('Willkommen', 'am Hafen.'),
    ('Ihre Website,', 'Seite für Seite.'): ('Heute und neu,', 'nebeneinander.'),
    ('Die Ideen', 'hinter der Seite.'): ('Zwölf Gedanken', 'zur Seite.'),
    ('Wie alles', 'zusammenhängt.'): ('Woraus die Seite', 'gemacht ist.'),
    ('Alle Seiten zum', 'Durchblättern.'): ('Vom Tisch', 'bis zum Gutschein.'),
    ('Vorschläge für', 'Ihre Gäste.'): ('Was Gäste', 'selbst erledigen.'),
    ('Ihre Unterlagen,', 'im selben Stil.'): ('Ihre Karten,', 'neu gesetzt.'),
    ('Ein paar Ideen', 'für Papier.'): ('Für die Tische', 'und die Bar.'),
    ('Ein Feed', 'für Instagram.'): ('Ein Feed', 'vom Hafen.'),
    ('Alles liegt für', 'Sie bereit.'): ('Der ganze Ordner,', 'in einem Stück.'),
    ('Alles geprüft,', 'bevor Sie es sehen.'): ('Angesehen,', 'bevor Sie es sehen.'),
}
TEXT_NEU = [   # Sätze des Kits, die fürs Haus nicht stimmen (wb_kapitel.eigene_titel ersetzt sie wörtlich)
    ('Links Ihre Seite, wie sie heute ist, rechts der Entwurf. Schieben Sie den Griff hin und her, daneben steht, was neu ist.', VERGLEICH_TEXT),
]
KAP_NAME_NEU = {'Guten Tag': 'Ein Brief', 'Register': 'Wegweiser', 'Zum Schluss': 'Bis bald'}


# Farben und Schnitte schon in H.CSS setzen: baut ein anderer Schritt mit dem Kit (K.gestaltung), stehen so trotzdem die Töne des Hauses
# und kein fetter Schnitt in werkbank.css, nicht erst nach dem Farbgang.
import sb_farbe as _sf  # noqa: E402
CSS = _sf.ohne_fett(_sf.faerbe(CSS))

# Gestaltung 28.10.2026 (Prüfchat Gestaltung): Unterlagen «Heute und als Idee»: das Foto der Karte vom Tisch hat das Format des Blatts daneben (A-Format),
# beide Seiten gleich hoch, nicht ein langes Foto neben einem kürzeren Blatt (Regel «Spalten gleich hoch»).
CSS_SEITEN = '''
.upaar{align-items:center}
.ublatt--alt .ublatt__b{aspect-ratio:1/1.414!important}
.ublatt--alt .ublatt__b img{width:100%;height:100%;object-fit:cover}
'''
