"""Wirtschaft am Schlössli, Bottighofen: Inhalt der Werkbank («Alles auf einen Blick») und ihrer Beigaben.   Werkzeug: ~/Desktop/Website-Projekte/_Werkbank-Kit/

Station 11 der Kette (Werkbank-Bauer, 19.10.2026, Roberts Wort: «die komplette Werkbank mit allen Dokumenten und Tools»). Aufbau in Kapiteln wie
beim Landgasthof Ruedihus (Bausteine von dort kopiert und umgeschrieben, Kit unverändert), Kleid und Worte der Wirtschaft am Schlössli.
Wortlaut des Hauses kommt aus website/inhalt/haus.json (eine Stelle, Quelle je Feld) und steht hier in «Guillemets». Was von Tasty Studios ist,
steht unter MEINS. Ton: Sie-Form, Schweizer Schreibung, herzlich. Restaurant, keine Zimmer. Schwesterhaus Taverne zum Schäfli: nichts wiederholen."""
import json
import os
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # = website/
import glob as _glob, re as _re


def bild(key, hoechstens=2400):
    """Grösste Fassung eines Fotos der Website bis «hoechstens» Pixel Breite (assets/img/<key>-<breite>.webp) als Schlüssel für K.hausbild."""
    b = sorted(int(m.group(1)) for p in _glob.glob(os.path.join(ROOT, 'assets', 'img', key + '-*.webp')) if (m := _re.search(r'-(\d+)\.webp$', p)) and int(m.group(1)) <= hoechstens)
    return os.path.join(ROOT, 'assets', 'img', f'{key}-{b[-1]}.webp') if b else key


HAUS = json.load(open(os.path.join(ROOT, 'inhalt', 'haus.json'), encoding='utf-8'))
NAME = 'Wirtschaft am Schlössli'
KURZ = 'wirtschaft-am-schloessli'
LEISTE = 'SCHLÖSSLI'
PORT = 8982
DOMAIN = 'schloessli-bottighofen.ch'
HEUTE_URL = 'https://www.schloessli-bottighofen.ch'
ANREDE = 'Grüezi, Herr Kuchler'
RECHTE = 'der Wirtschaft am Schlössli und den jeweiligen Fotografen.'
START_MS = 4200
WAHL = 'main > section'

# ---------- Farben: die der neuen Website (assets/css/haus.css :root), Farbwelt A «Stuhl und See», kein Gold ----------
FARBEN = dict(nacht='#0b1d3d', tief='#081631', navy='#0a234c', blau='#113d88', papier='#f3f6f9', creme='#e7ecf3', weiss='#fbfcfe',
              gold='#a2b6cf', messing='#c5d2e1', taupe='#0f3678', tinte='#041023', punkt='#fd9964')
SCHRIFT = dict(titel=('Open Sans', 'OpenSans-var.woff2'), titel_folge="Arial,sans-serif", ersatz="local('Arial')", druckgewicht=400)
DRUCKQUELLEN = [('OpenSans-var.woff2', 'OpenSans-Regular', 400), ('OpenSans-var.woff2', 'OpenSans-Medium', 500)]
DRUCKSCHRIFT = [('Open Sans', 400, 'OpenSans-Regular.ttf'), ('Open Sans', 500, 'OpenSans-Medium.ttf'), ('Open Sans', 700, 'OpenSans-Medium.ttf')]
# Muster der Website: Punktraster mit den Zeigern als Medaillon (marke/tapete-a-dunkel.svg, auf der Website assets/svg/)
MUSTER = 'url(../assets/svg/tapete-a-dunkel.svg)'
MUSTER_B = '168px'
MUSTER_DRUCK = '14mm'
ZEICHEN = K.svg_innen(os.path.join(ROOT, 'assets/svg/zeichen.svg'))      # Zeiger im Kreis aus dem Logo (Markenbuch, Station 05)
WORT = K.text_pfad(os.path.join(ROOT, 'assets/fonts/OpenSans-var.woff2'), 'SCHLÖSSLI', .3)   # Name in Versalien wie in der Leiste der Website
ETIKETTEN = dict(ordner='untersetzer', name='Untersetzer der Lästermeile', einzahl='Untersetzer')

SEITEN = [   # alle Seiten, die ein Gast als Seite wahrnimmt, dazu das Rechtliche (Sätze nur aus dem, was auf der Seite steht)
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

# ---------- Unterlagen: die Karten des Hauses, als Idee im Stil der neuen Seite gesetzt (Station 10, Kartenmacher; PDFs in unterlagen/pdf) ----------
SATZ_FUSS = 'Wirtschaft am Schlössli · Seestrasse 50 · 8598 Bottighofen'
UNTERLAGEN = dict(
    text='Zum Schlössli gehören die Karte nach Ländern, die Karte der Lästermeile, das Lunch-Menü der Woche, die Bankettmenüvorschläge und die Weinkarte. Alle sind als Idee neu gesetzt, in Ihrer eigenen Machart, jede neben Ihrer heutigen Fassung.',
    seite_text='Die Karte nach Ländern, die Lästermeile, das Lunch-Menü, die Bankettmenüvorschläge und die Weinkarte, jede als Idee neu gesetzt, in Ihrer eigenen Machart. Links steht Ihre heutige Fassung, rechts die neue, Seite für Seite.',
    knopf2=('Karte auf der Website', '../karte.html'))
FAECHER = [('speisekarte', 'Die Karte nach Ländern'), ('laestermeile', 'Lästermeile'), ('lunch', 'Lunch-Menü'), ('bankett', 'Bankettmenüvorschläge')]   # PDFs: unterlagen/pdf (aus La Carte, Daten des Kartenmachers)

# ---------- Auftakt, Brief ----------
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
        'Auf Ihrer heutigen Seite findet man davon wenig. Die neue erzählt es: die Karte nach Ländern, die Lästermeile, den Keller von Jonas Volpert und den Besen, der Ende des 17. Jahrhunderts statt eines Wirtshausschilds am Haus am See hing. Reserviert wird weiter über Ihr Gastronovi.',
        'Dazu gehören Ihre Karten, neu gesetzt in Ihrer eigenen Machart, Werkzeuge, mit denen Ihr Team Karte, Anlässe und Anfragen selbst pflegt, und ein paar Dinge für die Tische. Jedes Werkzeug lässt sich hier gleich öffnen und ausprobieren.'],
    schluss='<q>Hospitality braucht nicht noch eine Webdesign-Agentur. Hotels brauchen jemanden, der Marke, Website, Gast, Betrieb und Technologie als ein zusammenhängendes System versteht.</q>',
    abzuege=[])
GABEN = dict(seite='{n} Seiten.', unterlagen='Ihre Karten.', papier='{d} Drucksachen und {e} Untersetzer.', feed='{n} Beiträge.', gaeste='Für Ihre Gäste.', studio='')
GABEN_BILDER = dict(seite=(bild('start'), (.5, .5)), unterlagen=(bild('tortelloni'), (.5, .5)), papier=(bild('fliesen'), (.5, .5)), material=(bild('glas'), (.5, .5)), gaeste=(bild('abend'), (.5, .5)))
LAUFWORTE = ['Wirtschaft am Schlössli', '<b>Bottighofen</b>', 'Direkt im Hafen', 'Lästermeile', '<b>Tapas durchgehend</b>', 'Mit Blick aufs Wasser und die Alpen']
REIHENFOLGE = ['brief', 'vergleich', 'ideen', 'gefuege', 'seiten', 'unterlagen', 'handschrift', 'papier', 'material', 'dazu', 'schluss']   # der Feed kommt als eigene Bühne (feed_buehne.py)

# ---------- Website: Ideen (Aufnahmen _werkbank/sb_ideen.js → ansichten/Ideen), Vergleich (vorher.js → ansichten/Vorher) ----------
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
        ['muster', 1, 1, 'Zeiger und Raster', 'auf den dunklen Flächen', '', 'Zeichen und Muster', 'Die Zeiger stehen in der Leiste und zwischen den Abschnitten, das Punktraster mit den Zeigern liegt Ton in Ton auf den dunklen Flächen.', ['Leiste', 'Flächen']],
        ['kartendaten', 1, 2, 'Karten-Daten', 'eine Stelle', '', 'Karten-Daten', 'Alle Gerichte und Preise an einer Stelle. Daraus entstehen die Karte auf der Seite und die PDFs.', ['Gerichte', 'Preise', 'Allergene']],
        ['weindaten', 1, 3, 'Wein-Kärtchen', 'jeder Wein der Karte', '', 'Wein-Kärtchen', 'Jeder Wein der Weinkarte als Kärtchen mit Herkunft, Rebsorte und Preis. Daraus entstehen der Weinberater und «Ein Glas zu jedem Gang».', ['Herkunft', 'Rebsorte']],
        ['neugesetzt', 1, 4, 'Karten neu gesetzt', 'als Idee', '', 'Karten neu gesetzt', 'Die Karten als Idee neu gesetzt, in Ihrer eigenen Machart, jede neben Ihrer heutigen Fassung zum Durchblättern.', []],
        ['zeitstrahl', 1, 5, 'Besen und Luftbild', 'Ende 17. Jh. und 1954', '', 'Geschichte', 'Der Besen, der statt eines Schilds hing, und das Strandhotel Schlössli aus der Luft, 1954.', []],
        ['start', 2, 0, 'Startseite', 'der Tisch zuerst', 'seite', 'Startseite', 'Vom Tisch über die Terrasse und den Hafen zur Lästermeile, zur Karte, zu Küche und Keller. Von hier führt ein Weg zu jeder Seite.', ['Terrasse', 'Lästermeile', 'Küche']],
        ['karte', 2, 1, 'Die Karte', 'nach Ländern', 'seite', 'Die Karte', 'Die Karte nach Ländern, ein Glas zu jedem Gang, das Lunch-Menü und die Lästermeile; dazu die Weinkarte.', ['Länder', 'Lunch', 'Wein']],
        ['feiern', 2, 2, 'Banketts', 'zwei Etagen', 'seite', 'Banketts & Gruppen', 'Zwei Etagen für je bis zu 26 Personen, die Bankettmenüs und die Anfrage im Fenster.', []],
        ['anlaesse', 2, 3, 'Events', 'was kommt, was war', 'seite', 'Events', 'Four Hands auf der Excellence, das Jahr am Hafen und was war.', []],
        ['haus', 2, 4, 'Über uns', 'und Kontakt', 'seite', 'Über uns und Kontakt', 'Das Team, die Küche, das Schäfli, Zeiten, Anfahrt und der See heute.', []],
        ['reservation', 3, 0, 'Reservation', 'Gastronovi bleibt', 'sys', 'Reservation', 'Reserviert wird weiter über Ihr Gastronovi; die Anfrage im Fenster nimmt zusätzlich Platz, Flasche und Allergien mit.', []],
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
    ('reservation', 'Reservieren mit Wünschen', 'Im Fenster wählt der Gast Tag, Uhrzeit, Personen und Platz, legt eine Flasche bereit und nennt Allergien aus Ihrer Karte. Direkt buchen geht weiter über Gastronovi.', '50% 50%'),
    ('berater', 'Der Weinberater', 'Art, Herkunft, Rebsorte und Preis antippen, dann stehen die passenden Weine Ihrer Karte als Kärtchen da und lassen sich zur Reservierung bereitlegen.', '50% 50%'),
    ('wein-gang', 'Ein Glas zu jedem Gang', 'Ein Gericht antippen, drei Flaschen aus derselben Gegend erscheinen als Kärtchen, alle aus Ihrer Weinkarte.', '50% 50%'),
    ('abend', 'Den Abend zusammenstellen', 'Anlass, Tag, Personen, Platz und Menü wählen, der Zettel rechnet mit den Preisen Ihrer Karte mit und geht als Anfrage an Ihr Team.', '50% 0'),
    ('bankett', 'Bankettmenüs für Ihre Feier', 'Frühling, Sommer und Herbst, jedes Menü mit seinen Gängen aus Ihren Bankettmenüvorschlägen; die Anfrage geht gleich daneben im Fenster an Ihr Team.', '50% 50%'),
    ('gutschein', 'Gutschein gestalten', 'Betrag, Haus, für wen, von wem und ein Satz: Die Karte entsteht im Kleid des Hauses, für das Schlössli, das Schäfli oder beide.', '50% 30%'),
    ('kalender', 'Plätze für einen Abend', 'Das Jahr am Hafen als Band, jeder Termin mit seinen Angaben. Plätze fragt man im Fenster an.', '50% 50%'),
    ('see', 'Der See heute', 'Der Sonnenuntergang des Tages, aus dem Sonnenstand gerechnet, und ob die Terrasse offen ist, nach Ihren Zeiten und Ferien.', '50% 50%'),
]
GAESTE_TEL = []
GAESTE_KNOEPFE = [('Weinberater ausprobieren', '../weinkarte.html#berater'), ('Abend zusammenstellen', '../abend.html'), ('Gutschein gestalten', '../gutschein.html')]
GAESTE_LINK = '../abend.html'
GABEN['gaeste'] = 'Reservieren mit Wünschen, Weinberater, Bankettmenüs, Gutschein und der See heute.'

# ---------- Handschrift (marke_werkbank.py) ----------
HANDSCHRIFT = dict(
    text='Ihre Zeiger und Ihr Name bleiben, wie man sie kennt. Dazu kommen die Schrift Ihres Logos für die grossen Zeilen, in Versalien, eine ruhige für den Lesetext und die Farben von Ihrer Terrasse: das Blau der Stühle, der Himmel über dem See und das Rot der Schirme als einziger Punkt.',
    marke_etik='Zeiger und Name', marke_text='Die Zeiger aus Ihrem Logo sind nachgezeichnet und bleiben in jeder Grösse scharf. Die Nabe der Zeiger ist das Ö in Ihrem Namen.',
    schriften=[], farben=[], farben_etik='von Ihrer Terrasse',
    muster_etik='Das Punktraster mit den Zeigern',
    muster_text='Auf den dunklen Flächen liegt ein feines Punktraster, in jedem Feld die Zeiger als kleines Medaillon, Ton in Ton. Man findet es auf der Seite, auf den Karten und auf jeder Drucksache.',
    knopf_text='Diese Knöpfe darf man drücken.', knoepfe=('Ausprobieren', 'Noch einmal'))

# ---------- Feed, Papier, Dateien ----------
FEED = dict(art='bogen', bogen=[1, 2, 3, 4, 5, 6, 7, 8, 9], bogen_zeile='Die ersten drei Reihen',
            text1='Einundzwanzig Beiträge aus Ihren eigenen Fotos, Reihe für Reihe am Horizont ausgerichtet, in der Mitte einmal ein Bild über drei Beiträge.',
            text2='Keine Grafiken, keine Schrift auf den Bildern. Tippen Sie auf den Bildschirm, dann scrollen Sie durch den Feed wie am Handy.',
            kacheln=[])
PAPIER = dict(
    etik_text='An der Lästermeile gehen den ganzen Tag Gläser über die Theke. Dazu passen Untersetzer: zwölf Ideen mit Ihren Fliesen, den Zeigern und den Tapas der Karte.',
    druck_text='Ansichtskarten vom Hafen, ein Gutschein, die Tischkarte für reservierte Tische, eine Menükarte für jede Feier, ein Aushang für die Betriebsferien und Briefpapier.',
    orte_e=[(3, 6, 27, -8), (33, 0, 18, 6), (54, 8, 25, -4), (80, 2, 17, 8), (8, 50, 17, 7), (29, 54, 27, -6), (62, 52, 26, 4)],
    orte_d=[('ansichtskarte-1', 3, 3, 42, -3, 0), ('gutschein', 47, 5, 50, 3, 0), ('menuekarte', 6, 42, 24, -4, 0), ('tischkarte', 36, 44, 36, 3, 0), ('aushang', 76, 40, 19, 6, 0),
            ('ansichtskarte-3', 40, 74, 30, -5, 0), ('gutschein-r', 66, 78, 28, 3, 0)])
PAPIER_SEITE = dict(
    breit={'ansichtskarte-1', 'ansichtskarte-2', 'ansichtskarte-3', 'ansichtskarte-4', 'ansichtskarte-r', 'gutschein', 'gutschein-r', 'tischkarte', 'tischkarte-r', 'couvert', 'briefbogen', 'menuekarte', 'menuekarte-r', 'aushang'},
    formen=set(),
    auslage=[('ansichtskarte-1', 28, 0, 44, 3), ('menuekarte', 0, 2, 24, -6), ('gutschein', 36, 40, 52, -3), ('tischkarte', 2, 58, 32, -4), ('aushang', 80, 4, 19, 7), ('ansichtskarte-3', 64, 62, 30, 5)],
    karton={'ansichtskarten': ('', [('ansichtskarte-1', 46, ''), ('ansichtskarte-2', 46, ''), ('ansichtskarte-3', 46, ''), ('ansichtskarte-4', 46, ''), ('ansichtskarte-r', 46, 'Rückseite')]),
            'gutschein': ('', [('gutschein', 88, 'Vorderseite'), ('gutschein-r', 88, 'Rückseite')]),
            'tischkarte': ('', [('tischkarte', 47, 'Vorderseite'), ('tischkarte-r', 47, 'Rückseite')]),
            'menuekarte': ('', [('menuekarte', 44, 'Vorderseite'), ('menuekarte-r', 44, 'Rückseite')]),
            'aushang': ('', [('aushang', 46, '')]),
            'briefpapier': ('', [('couvert', 92, 'Couvert'), ('briefbogen', 38, 'Briefbogen')])},
    titel={'ansichtskarten': ['Grüsse', 'vom Hafen.'], 'gutschein': ['Ein Gutschein', 'zum Verschenken.'], 'tischkarte': ['Dieser Tisch', 'ist reserviert.'], 'menuekarte': ['Ein Menü', 'für Ihre Feier.'],
           'aushang': ['Wenn das Schlössli', 'Pause macht.'], 'briefpapier': ['Briefbogen', 'und Couvert.']},
    schatten={'ansichtskarten', 'gutschein', 'tischkarte', 'menuekarte', 'aushang', 'briefpapier'},
    etik_titel=('Untersetzer', 'für die Lästermeile.'),
    etik_text='An der Lästermeile gehen den ganzen Tag Gläser über die Theke. Hier sind {n} Untersetzer als Idee, rund und quadratisch, mit Ihren Zementfliesen, den Zeigern und den Tapas der Karte.',
    etik_kap='Die Untersetzer', etik_kopf=['Zwölf', 'Untersetzer.'],
    etik_kopftext='Das Blau der Stühle, der Himmel über dem See und das Rot der Schirme kommen von Ihrer Terrasse, die Fliese von Ihrer Bar, die Worte von Ihrer Karte.',
    druck_text='Dinge, die bei Ihnen auf dem Tisch, an der Tür oder in der Post liegen könnten. Nehmen Sie davon, was Ihnen gefällt.',
    etik_auslage=[(0, 4, 26, -7), (30, 0, 22, 5), (56, 6, 26, -4), (66, 42, 24, 6), (6, 40, 22, 6), (30, 38, 26, -5), (88, 2, 0, 0), (0, 76, 0, 0), (62, 72, 22, 4), (36, 74, 0, 0), (6, 76, 0, 0), (26, 72, 26, 3)])
MATERIAL = dict(
    text='Was für den Entwurf neu entstanden ist, liegt sortiert in einem Ordner: die Karten als PDF, die Drucksachen, die Untersetzer, die Beiträge für Instagram und Ihr Zeichen als Datei.',
    streu=[(bild('lounge'), 'Am Ufer', -4, '-0.05'), (bild('regal'), 'An der Bar', 3, '0.04'), (bild('suppe'), 'Aus der Küche', -2, '-0.07'), (bild('dessert'), 'Zum Schluss', 4, '0.05'), (bild('apero'), 'Blaue Stunde', -3, '-0.04')],
    druck_satz='Ansichtskarten, Gutschein, Tischkarte, Menükarte, Aushang und Briefpapier.',
    zeichen=[('Die Zeiger', 'assets/svg/zeichen.svg', 'Wirtschaft am Schlössli Zeichen.svg')],
    zeichen_satz='Die Zeiger als Zeichnung, die in jeder Grösse scharf bleibt.',
    auslage=[('blattbild', '../drucksachen/img/ansichtskarte-1.webp', 30, 0, 44, 3), ('blattbild', '../drucksachen/img/gutschein.webp', 34, 44, 52, -3),
             ('blattbild', '../drucksachen/img/menuekarte.webp', 2, 6, 26, -6), ('form', '../untersetzer/img/u01.webp', 4, 62, 22, -5), ('form', '../untersetzer/img/u05.webp', 82, 54, 16, 5)])
AUSBLICK = dict(text='Ein paar Dinge fehlen noch.', gross=('', '', ''), punkte=[], studio='')
SCHLUSS = dict(bild=bild('abend'))
KAPITEL = {
    'vergleich': dict(text=VERGLEICH_TEXT),
    'ideen': dict(text='Zu jeder Stelle der Seite gibt es einen Grund. Zwölf davon stehen hier, aufgenommen auf der Seite, wie sie heute aussieht.'),
    'gefuege': dict(text='Ein Blick hinter die Seiten: links, was von Ihnen kommt, in der Mitte, was daraus geworden ist, rechts die Seiten und was im Hintergrund mitläuft.'),
    'seiten': dict(text='Eine Seite aussuchen, mit den Pfeilen weiterblättern. Rechts dieselbe Stelle am Handy, mit «Öffnen» sind Sie auf der echten Seite.'),
    'unterlagen': dict(text=UNTERLAGEN['text']),
    'gaeste': dict(text='Was ein Gast auf der Seite selbst erledigt, bevor er anruft: reservieren, einen Wein aussuchen, den Abend planen, einen Gutschein gestalten. Alles rechnet mit Ihren Zahlen und lässt sich ausprobieren.'),
    'papier': dict(text='Zum Hafen sind mir ein paar Dinge eingefallen: Untersetzer für die Lästermeile, eine Menükarte für jede Feier, Ansichtskarten und einiges mehr. Nehmen Sie, was Ihnen gefällt.'),
    'material': dict(text='Die Karten als PDF, die Drucksachen, die Untersetzer und Ihr Zeichen als Datei: alles Neue liegt in einem Ordner beisammen.'),
    'geprueft': dict(text='Bevor Sie etwas davon sehen, ist jedes Teil durchgegangen worden: die Website auf jedem Gerät, die Karten Wort für Wort, jedes Werkzeug Knopf für Knopf. Auf dem Blatt steht das Wichtigste, der Rest auf einer eigenen Seite.'),
    'schluss': dict(text='Sagen Sie mir offen, was Ihnen am Schlössli gefällt und was nicht. Ändern lässt sich alles.'),
}
MEINS = ['Der Brief und alle Sätze der Werkbank', 'Titel und Sätze zu den Ideen, zum Gefüge, zu den Drucksachen und Untersetzern', 'Bildzeilen der Ansichtskarten, Feldnamen, das Wort «Reserviert»', 'Texte zu den Beiträgen des Feeds']

# ---------- Geprüft (nur Belegtes: Station 07 Baumeister, abschnitte.json Messwerte; Karten: Station 10; Werkzeuge: ihre Pakete; Stand des Baus) ----------
import datetime as _dt
GEPRUEFT = [
    ('Die Website', 'seite', ['Alle Seiten in der Technik von Safari und von Chrome, von 320 bis 1440 Pixeln Breite: nichts läuft seitlich über, kein Skriptfehler, kein kaputtes Bild.',
                              'Auf vier- und sechsfach gebremster Rechenleistung gemessen, wie auf einem schwachen Gerät: Das Scrollen bleibt flüssig.',
                              'Jede Angabe kommt aus einer Stelle mit Quelle: Zeiten, Adresse, Sätze, Team und Auszeichnungen.']),
    ('Die Karten', 'karte', ['Jede Karte aus Ihren PDFs gelesen, nicht abgetippt; die Weinkarte Zeile für Zeile gegen das Original gezählt.',
                             'Was Sie klären müssen, steht gesondert in der Liste der offenen Punkte.']),
    ('Die Werkzeuge', 'schloss', ['Jedes der sieben Werkzeuge in einem eigenen Durchgang gebaut und Knopf für Knopf bedient, nur mit erfundenen Daten.',
                                  'Kein Werkzeug verschickt etwas von selbst, keines öffnet ein Mailprogramm.']),
]
GEPRUEFT_PUNKTE = [
    ('Die Website', 'Alle Seiten am Handy und am Rechner geöffnet, in der Technik von Safari und von Chrome. Nichts läuft über, und auch auf einem schwachen Gerät bleibt das Scrollen flüssig.'),
    ('Die Karten', 'Jede Zeile kommt aus Ihren PDFs, nicht abgetippt. Die Weinkarte ist Zeile für Zeile gegen das Original gezählt.'),
    ('Die Werkzeuge', 'Alle sieben Werkzeuge einzeln gebaut und ausprobiert, nur mit erfundenen Daten. Von sich aus verschickt keines etwas.'),
    ('Ihre Daten', 'Die Website setzt für Gäste keine Kekse. Anfragen gehen über Fenster auf der Seite an Ihr Team, im Entwurf nie an das echte Haus.'),
]
GEPRUEFT_TRIO = [(bild('glas'), 1.6, (.5, .5), 'Am Wasser'), (bild('sauce'), 1.6, (.5, .5), 'In der Küche'), (bild('ig-luft'), 1.6, (.5, .5), 'Von oben')]
GEPRUEFT_OFFEN = 'Offen bleibt, was nur Sie wissen: die Rechte an einigen Fotos von Gästen und Partnern, Ihr Blick auf die Auswahl der Bilder und die Passwörter für die Werkzeuge.'
GEPRUEFT_EIN = 'Bevor Sie etwas davon sehen, ist es durchgegangen worden: die Website auf jedem Gerät, die Karten Zeile für Zeile, jedes Werkzeug Knopf für Knopf. Hier steht, was genau, ohne Fachwörter. Was offen bleibt, steht auch da.'
GEPRUEFT_NAV = ['Website', 'Karten', 'Werkzeuge', 'Daten', 'Offen']
GEPRUEFT_MEHR = [
    ('Die Website', 'seite', 'Neun Seiten von der Startseite bis zu «Ihr Abend», dazu das Rechtliche mit Bildnachweis.', [
        'Am Handy und am Rechner, von 320 bis 1440 Pixeln Breite, in Safari- und Chrome-Technik: nichts läuft seitlich über, kein Skriptfehler, kein kaputtes Bild.',
        'Auf vier- und sechsfach gebremster Rechenleistung gemessen: Die Seiten laufen beim Scrollen ohne Ruckeln, nichts springt beim Laden.',
        'Jede Angabe steht an einer einzigen Stelle mit ihrer Quelle; jede Seite liest von dort. Freie Fotos tragen ihre Namensnennung, gesammelt im Bildnachweis.']),
    ('Die Karten', 'karte', 'Die Karte nach Ländern, die Lästermeile, der Lunch, die Bankettmenüs und die Weinkarte.', [
        'Jede Karte aus Ihren PDFs gelesen, nicht abgetippt. Die Weinkarte ist Zeile für Zeile gegen das Original gezählt.',
        'Neu gesetzt in Ihrer eigenen Machart, mit fest eingebetteten Schriften.']),
    ('Die sieben Werkzeuge', 'schloss', 'Sieben Werkzeuge, mit denen Ihr Team die Seite selbst führt.', [
        'Jedes Werkzeug in einem eigenen Durchgang gebaut und Knopf für Knopf bedient, mit Probe-Daten, nie mit Ihren echten.',
        'Kein Werkzeug verschickt etwas von selbst und keines öffnet ein Mailprogramm: Antworten an Gäste bleiben als Brief im Werkzeug.']),
    ('Ihre Daten und die Ihrer Gäste', 'schild', 'Was die Seite speichert und was nicht.', [
        'Die Website setzt für Gäste keine Kekse. Im Entwurf zählt die Seite keine Besuche; das Werkzeug für die Besuche zeigt Beispielwerte.',
        'Reservation, Bankett, Plätze und Gutschein schickt der Gast über ein Fenster auf der Seite; im Entwurf geht nichts an das echte Haus.',
        'Der Entwurf ist für Suchmaschinen gesperrt, bis Sie ihn freigeben.']),
    ('Was offen bleibt', 'auge', 'Diese Dinge liegen nicht in meiner Hand.', [
        'Einige Fotos stammen von Gästen und Partnern (Tripadvisor, Excellence, Papageno). Ob sie bleiben dürfen, klären wir mit Ihnen; freie Fotos tragen ihre Namensnennung.',
        'Die Werkzeuge stehen im Entwurf ohne Anmeldung. Bei der Auslieferung bekommt jedes eine Anmeldung und jede Person ihr eigenes Passwort.',
        'Die Seite spricht bisher Deutsch; weitere Sprachen folgen.'])]
PRUEFDATUM = _dt.date(2026, 10, 19)
STEMPEL_TEXT = f'GEPRÜFT · WIRTSCHAFT AM SCHLÖSSLI · {PRUEFDATUM:%d.%m.%Y} ·'
GEPRUEFT_BILD = bild('glas')

# ================================================================ Bausteine (Vorlage Ruedihus, kopiert und umgeschrieben; Kit unverändert)
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
/* ---------- Leichte Tapete: keine Fläche ganz ohne Muster neben einer mit (Schlössli: Punktraster mit Zeigern) ---------- */
.tapete-leicht{background-image:linear-gradient(var(--tl),var(--tl)),var(--muster);background-size:auto,var(--musterb) auto;background-position:0 0,50% 0}
.fl--nacht.tapete-leicht{--tl:rgba(11,29,61,.42)}
.fl--blau.tapete-leicht{--tl:rgba(17,61,136,.36)}
.fl--tief.tapete-leicht{--tl:rgba(8,22,49,.42)}
.tapete-hell{background-image:url(../assets/svg/tapete-a-hell.svg);background-size:168px auto;background-position:50% 0}
/* ---------- Titel wie auf der Website: Open Sans in Versalien, gesperrt, nie fett ---------- */
.zt,.t1,.t2,.t3,.wfen__t,.ins-t h3,.rgw .wfa__texte h3,.sbf-text h3,.hs2-ww+small{font-weight:400!important}
.zt{text-transform:uppercase;letter-spacing:.12em}
.zt em{font-style:normal}
.kap--z span,.kap--k>span{font-family:var(--mono)!important;font-weight:400!important;font-size:12px!important;letter-spacing:.2em;text-transform:uppercase}
.wfen__t{text-transform:uppercase;letter-spacing:.12em}
h2,h3,.wege__t,.gb-blatt header h3,.rgw .wfa__texte h3,.fbz__n{font-weight:400!important}
b,strong{font-weight:500}
.wf .wege__t,.gb-blatt header h3{font-family:var(--serif);text-transform:uppercase;letter-spacing:.14em}
'''

import rundum as _ru  # noqa: E402,F401   (nicht eingehängt: das Schlössli hat keine Seiten rund um einen Aufenthalt)
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
for _i, _q in enumerate([os.path.join(_AN, 'Rechner', 'Startseite.jpg'), os.path.join(ROOT, 'unterlagen', 'img', 'n-speisekarte-01.webp'),
                         os.path.join(_AN, 'Werkzeuge', 'bureau.jpg'), os.path.join(_AN, 'Gaeste', 'reservation.jpg')]):
    if os.path.exists(_q):
        EIGENE_BILDER.append((f'gp-{_i}', _q, 320, dict(q=80, schnitt=4 / 3, lage=(.5, 0))))
CSS += _gb.CSS

import fuss_faecher as _ff  # noqa: E402
if _ff.BEREIT:
    wege_abschnitt = _ff.abschnitt
    CSS += _ff.CSS
CSS += '''
/* Dateien: Fotos ohne Polaroid-Rand und ohne Bildzeile (Polaroids nur, wo sie zur Welt gehören; Tasty-Sprache Stufe 4), ungleich gross, ohne Drehung */
#material .streu .abzug{padding:0!important;background:none!important;border-radius:clamp(14px,1.4vw,20px);overflow:hidden;--r:0deg!important;--r0:0deg!important;box-shadow:0 30px 40px -26px rgba(4,16,35,.55),0 10px 16px -10px rgba(4,16,35,.3)!important}
#material .streu .abzug span{display:none!important}
#material .streu .abzug img{display:block;width:100%;height:100%;object-fit:cover;border-radius:0!important}
@media(min-width:760px){#material .streu{align-items:center}#material .streu .abzug:nth-child(3){transform:scale(1.18);z-index:2}#material .streu .abzug:nth-child(2),#material .streu .abzug:nth-child(4){transform:scale(1.04);z-index:1}}
@media(min-width:760px){.vh-wahl,#seiten .wahl{justify-content:center}}
@media(min-width:760px){.vh-wahl{justify-content:center}}
@media(max-width:480px){.kn{max-width:100%;height:auto;min-height:54px;padding-top:9px;padding-bottom:9px;white-space:normal;line-height:1.35;text-align:left}.kn i{flex:none}.kn-reihe{max-width:100%}}
.schluss .zt,.schluss .lauf p,.schluss .kap span{text-shadow:0 1px 2px rgba(4,16,35,.9),0 2px 16px rgba(4,16,35,.8),0 0 42px rgba(4,16,35,.55)}
'''


BRETT_HILFE = ("<script id=\"brett-hilfe\">(function(){var b=document.getElementById('brett'),k=document.getElementById('brett-noch');if(!b||!k||!('IntersectionObserver' in window))return;"
               "new IntersectionObserver(function(E,o){if(!E[0].isIntersecting)return;o.disconnect();setTimeout(function(){if(/\\bvor\\b/.test(b.className))k.click()},700)},{rootMargin:'0px 0px -35% 0px'}).observe(b)})();</script>")


def nach_bau():
    """Nach jedem Bau des Kits: Eigenes nach werkbank/eigen, Nacharbeit der Bausteine, Kapitel, Ruhe, Farben."""
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
    # Nichts läuft mit dem Scrollen mit (Regel 55, Vorlage Ruedihus 18.10.2026)
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
    # Brett «Woraus die Seite gemacht ist» am Handy: Aufbau anstossen, sobald es ins Bild kommt (Fund des Gasterntal-Chats, aus der Werkbank des Ruedihus)
    if 'id="brett-hilfe"' not in t:
        t = t.replace('</body>', BRETT_HILFE + '</body>', 1)
    import sb_skripte as _sk
    for _id, _js in (('rh-vorladen', _sk.VORLADEN_JS), ('rh-frueh', _sk.FRUEH_JS), ('rh-zurueck', _sk.WB_JS), ('rh-karussell', _sk.KARUSSELL_JS)):
        if f'id="{_id}"' not in t:
            t = t.replace('</body>', _js + '\n</body>', 1)
    open(seite, 'w', encoding='utf-8').write(t)
    import feed_leicht as _fl
    if _fb.BEREIT and _FEED_DA:
        _fl.mach()
    import sb_farbe
    sb_farbe.anwenden()
    import sb_ki   # Seite «KI und Ihre Daten», Karte «Ein Vorschlag.» allein und als PDF (Robert 20.10.2026)
    sb_ki.bau()


TITEL_NEU = {
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
KAP_NAME_NEU = {'Guten Tag': 'Ein Brief', 'Register': 'Wegweiser', 'Zum Schluss': 'Bis bald'}


# Farben und Schnitte schon in H.CSS setzen (Schlössli 20.10.2026): baut ein anderer Chat mit dem Kit (K.gestaltung), steht so trotzdem das Blau des Hauses
# und kein fetter Schnitt in werkbank.css, nicht erst nach meinem Farbgang.
import sb_farbe as _sf  # noqa: E402
CSS = _sf.ohne_fett(_sf.faerbe(CSS))
