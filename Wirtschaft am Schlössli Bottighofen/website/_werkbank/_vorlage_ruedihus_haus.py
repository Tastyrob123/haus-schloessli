"""Landgasthof Ruedihus: Inhalt der Werkbank und ihrer Beigaben.   Werkzeug: ~/Desktop/Website-Projekte/_Werkbank-Kit/ (alles.sh nennt jeden Schritt)

Wortlaut des Hauses steht in «Guillemets» oder ist als solcher benannt, Quelle ist das Fakten-Blatt (`_recherche/Fakten-Blatt.md`)
und `daten.py` der Website. Was von Tasty Studios ist, steht am Ende unter MEINS. Ton: Sie-Form, Schweizer Schreibung, herzlich."""
import os
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'Landgasthof Ruedihus'
KURZ = 'landgasthof-ruedihus'
LEISTE = 'RUEDIHUS'
PORT = 8917
DOMAIN = 'doldenhorn-ruedihus.ch'
HEUTE_URL = 'https://www.doldenhorn-ruedihus.ch/ruedihus/'
ANREDE = 'Guten Tag, Familie Maeder'
RECHTE = 'der Familie Maeder und den jeweiligen Fotografen.'
UEBERSICHT = ('Alle vier Häuser', 'http://localhost:8920/')
START_MS = 5200

# ---------- Farben: Farbwelt «Stube» der Website (dunkles Wandholz, Kerzenlicht, Gold des Zeichens) ----------
FARBEN = dict(nacht='#1f1209', tief='#170d06', navy='#2a180a', blau='#321f10', papier='#efe4d3', creme='#e3d2ba', weiss='#fbf5ea',
              gold='#c98543', messing='#b78f51', taupe='#7d4f27', tinte='#2a1a0e', punkt='#c42e13')
GERANIE, OFEN, LICHT = '#a8260f', '#31380d', '#f3cd94'
SCHRIFT = dict(titel=('Gelasio', 'gelasio-700.woff2'), titel_folge="Georgia,'Times New Roman',serif", ersatz="local('Georgia Bold'),local('Georgia-Bold'),local('Georgia')", druckgewicht=700)
DRUCKQUELLEN = [('gelasio-700.woff2', 'Gelasio-Bold', None), ('gelasio-400.woff2', 'Gelasio-Regular', None)]
DRUCKSCHRIFT = [('Gelasio', 400, 'Gelasio-Bold.ttf'), ('Gelasio', 700, 'Gelasio-Bold.ttf'), ('Gelasio Text', 400, 'Gelasio-Regular.ttf'), ('Instrument Sans', '400i', 'InstrumentSans-Italic.ttf')]  # echte Kursive (09.10.2026): ohne sie zog der Browser die Übersetzungszeilen der Karten künstlich schräg
# Muster der Website: die Butzenscheiben der Fensterreihe (Klasse .butzen in assets/css/main.css)
MUSTER = '''url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='56'%3E%3Cg fill='none' stroke='%23c98543' stroke-opacity='.08' stroke-width='1.4'%3E%3Ccircle cx='28' cy='28' r='21'/%3E%3Ccircle cx='28' cy='28' r='5'/%3E%3Cpath d='M0 0h56v56H0z'/%3E%3C/g%3E%3C/svg%3E")'''
MUSTER_B = '56px'
MUSTER_DRUCK = '9mm'
ZEICHEN = K.svg_innen(os.path.join(ROOT, 'assets/logo/zeichen.svg'))      # Medaillon des Hauses, aus der Karte der Egger- und Stettlerstube nachgezeichnet
ETIKETTEN = dict(ordner='zuendholz', name='Zündholz-Etiketten', einzahl='Etikett')

SEITEN = [
    ('index.html', 'Startseite', 7, 'Das Haus zur blauen Stunde im ersten Bild, danach die Stuben, die Karte, die Zimmer und die Geschichte seit 1753.', ''),
    ('zimmer.html', 'Zimmer', 5, 'Landhaus, Hochzeitsstube, Liebeslaube und Hymmelrich, jedes mit seinen Fotos und seinem Preis.', ''),
    ('essen.html', 'Essen', 6, 'Fünf Stuben auf zwei Stockwerken, der Schpiszettel und woher die Produkte kommen.', ''),
    ('haus.html', 'Das Haus', 6, 'Die Geschichte von der Novembernacht 1753 bis heute, der Garten und Ihre Gastgeber.', ''),
    ('rechtliches.html', 'Rechtliches', 1, 'Rechtliches und Bildnachweis.', 'recht'),
]
LANG = {'Essen': 'Essen und Stuben', 'Zimmer': 'Zimmer und Preise', 'Das Haus': 'Das Haus seit 1753', 'Rechtliches': 'Rechtliches und Bildnachweis'}
KURZNAME = {}
# Wortmarke: «LANDGASTHOF RUEDIHUS» in Versalien wie auf der Website des Hauses (dort Georgia Bold, hier die freie Entsprechung Gelasio)
WORT = K.text_pfad(os.path.join(ROOT, 'assets/fonts/gelasio-700.woff2'), 'LANDGASTHOF RUEDIHUS', .06)

# ---------- Unterlagen ----------
SATZ_FUSS = 'Landgasthof Ruedihus · Hinder de Büele 6 · 3718 Kandersteg'
CSS_SATZ = '''
.a3 .inhalt{padding:11mm 13mm 9mm}
.a3 .spalten{gap:0 12mm}
.karte--aussen.a3 .spalten{grid-template-columns:1fr 1.05fr .9fr}
.karte--aussen.a3 .sp{padding:12mm 7mm 9mm 13mm}
.karte--aussen.a3 .sp:last-child{padding:0}
.karte--aussen.a3 .ab{font-size:calc(8.6pt*var(--s));line-height:1.46;margin-bottom:calc(2mm*var(--s))}
.karte--aussen.a3 .ukasten .ab{margin-bottom:calc(1mm*var(--s))}
.tagesmenu .rubrik{margin-bottom:6mm}
.dessert .po{padding:calc(1.9mm*var(--s)) 0}
.dessert .po__p--reihe .pz b{min-width:calc(15mm*var(--s))}
.dessert .rk b{width:calc(18mm*var(--s))}
.tagesteller .po{border-bottom:.2mm solid rgba(183,143,81,.4);padding:calc(2.4mm*var(--s)) 0}
.tagesteller .po h4{font-family:var(--titel);font-weight:700;font-size:calc(13pt*var(--s));color:#321f10}
.deck .udeck h1{font-size:50pt;letter-spacing:.02em}
'''
UNTERLAGEN = dict(
    text='Zu Ihrem Haus gehören drei Karten: der Schpiszettel der Chäs- und Wystube, die Schpis Charte der Egger- und Stettlerstube und die Tagesteller. Dazu kommt das Heft mit den Menuvorschlägen für Feste, Stand 2023. Alle vier habe ich als Idee im Stil der neuen Seite gesetzt. Auf einer eigenen Seite blättern Sie jede Unterlage neben Ihrer heutigen Fassung durch.',
    seite_text='Der Schpiszettel der Chäs- und Wystube, die Schpis Charte der Egger- und Stettlerstube, die Tagesteller und das Heft mit den Menuvorschlägen für Feste (Stand 2023): Alle vier habe ich als Idee im Stil der neuen Seite gesetzt. Hier blättern Sie jede Unterlage neben Ihrer heutigen Fassung durch.',
    knopf2=('Karte auf der Website', '../essen.html'))
FAECHER = [('chaes-und-wystube', 'Chäs- und Wystube'), ('egger-und-stettlerstube', 'Egger- und Stettlerstube'), ('tagesteller', 'Tagesteller'), ('nos-menus', 'Menuvorschläge 2023')]   # 13.10.2026: das Heft «Nos Menus» dazu

# ---------- Werkbank ----------
AUFTAKT = dict(
    titel=['Für Ihr Haus', 'entworfen.'],
    text='Ich bin Robert Reff, komme aus der Gastronomie und baue Websites. Für den Landgasthof Ruedihus habe ich eine neue entworfen, weil mir Ihr Haus sehr gefällt und ich gesehen habe, dass bei Ihnen vielleicht Platz für eine neue sein könnte. Ich hoffe, sie gefällt Ihnen.',
    abzuege=[('haus-wiese', 'Über der Blumenwiese'), ('stube-rund', 'In der Stube'), ('z-liebeslaube', 'Liebeslaube')])
BRIEF = dict(
    absaetze=[
        'Ich bin Robert und komme aus Hamburg. Zwölf Jahre habe ich in der Gastronomie gearbeitet, auch in Hotels, und mich dort hochgearbeitet. In dieser Zeit ist bei mir eine echte Leidenschaft für alles entstanden, was um einen Betrieb herum passiert. Inzwischen bin ich selbstständig und baue Websites für Hotels und Restaurants.',
        'Auf das Ruedihus bin ich über Ihre anderen Häuser gekommen. Ein Haus von 1753 mit bemaltem Giebel und Butzenscheiben, mit fünf Stuben, einer Sage vom Holz aus einer Novembernacht und einer Karte, auf der steht, was man bei Ihnen vergebens sucht. So etwas kann man sich nicht ausdenken. Ich hatte sofort Lust, dafür eine Website zu bauen, auf der man das alles sieht.',
        'Das Ganze ist eine Überraschung, Sie wussten bisher nichts davon. Entstanden ist ein Entwurf mit allen Seiten, dazu Ihre Karten im selben Stil und ein paar Ideen für Papier. Wenn Ihnen gefällt, was Sie sehen, freue ich mich sehr über ein Gespräch darüber, wie daraus Ihre Website werden kann.'],
    schluss='',
    bild='haus-sommer', lage=(.5, .5), bild_alt='Der Landgasthof Ruedihus in Kandersteg, davor die Terrasse', schild=('Landgasthof Ruedihus', 'Kandersteg · seit 1753'))
GABEN = dict(
    seite='{n} Seiten mit Stuben, Karte, Zimmern und der Geschichte des Hauses. Gebucht wird weiter über Ihr SimpleBooking.',
    unterlagen='Der Schpiszettel, die Schpis Charte, die Tagesteller und das Heft mit den Menuvorschlägen für Feste, als Idee im Stil der neuen Seite.',
    papier='{d} Drucksachen und {e} Etiketten für die Zündholzschachtel als Ideen, falls Sie Lust darauf haben.',
    feed='{n} Beiträge mit Ihren eigenen Bildern, dazu ein Profilbild und ein paar Zeilen für die Biografie.')
GABEN_BILDER = dict(seite=('haus-wiese', (.5, .5)), unterlagen=('e-roesti', (.3, .5)), papier=('stube-kerze', (.5, .5)), material=('z-himmelbett', (.5, .5)))
LAUFWORTE = ['Landgasthof Ruedihus', '<b>seit 1753</b>', 'Heute Abend Ihr Tisch', 'Kandersteg', '<b>Chäs-u Wystube</b>', 'Egger- und Stettlerstube']
IDEEN = [
    ('Rechner/Startseite', 'Das Haus zur blauen Stunde', 'Ihr Haus mit erleuchteten Fenstern steht im ersten Bild, darüber Ihr Satz «Zu Gast – bei Freunden» und gleich darunter die Buchung.', '50% 50%'),
    ('Rechner/Startseite 3', '«Was führt Sie zu uns?»', 'Eine Nacht, zu zweit oder ein Fest: Der Gast wählt eine Karte. Sie klappt auf und zeigt, was Ihr Haus dafür bereithält.', '50% 40%'),
    ('Rechner/Essen 3', 'Fünf Stuben, zwei Stockwerke', 'Jede Stube hat ihr eigenes Bild. Unten das Parterre mit Chäs-u Wystube, Jungestube und Ofestübli, eine Treppe höher die Egger- und Stettlerstube.', '50% 50%'),
    ('Rechner/Essen 4', 'Ihr Grundsatz, gross', 'Der Satz aus Ihrer Karte, was man bei Ihnen vergebens sucht, steht als Fenster mitten auf der Seite.', '50% 50%'),
    ('Rechner/Zimmer 2', 'Jedes Zimmer mit seinen Fotos', 'Landhaus, Hochzeitsstube, Liebeslaube und Hymmelrich stehen je mit drei Fotos, Ihrem Satz und dem Preis für sich.', '50% 40%'),
    ('Rechner/Zimmer 3', 'Am Morgen die Vorhänge auf', 'Ihr kurzer Film aus dem Zimmer mit Himmelbett hat einen eigenen Platz bekommen.', '50% 50%'),
    ('Rechner/Das Haus 3', 'Seit 1753', 'Die Geschichte aus Ihrer Karte als Zeitstrahl: 1753, 1908, 1990 und 2000, jede Zahl mit Ihren eigenen Worten.', '50% 50%'),
    ('Rechner/Essen 5', 'Metzgete, Stubete, Ruedi-Tag', 'Ihre Anlässe stehen als Karten zum Blättern auf der Seite «Essen».', '50% 50%'),
    ('Rechner/Startseite 6', 'So sehen es die Gäste', 'Ihre Noten bei Booking.com und Google stehen als zwei Karten nebeneinander.', '50% 50%'),
]


def gefuege(z):
    n = [
        ['fotos', 0, 0, 'Ihre Fotos', 'Website, Schweiz Tourismus', 'ein', 'Ihre Fotos', 'Die Aufnahmen von Ihrer Website und aus Ihren Einträgen bei Schweiz Tourismus und Booking.com. Aus ihnen besteht die Bildwelt des Entwurfs.', ['Haus und Garten', 'Stuben', 'Zimmer']],
        ['zeichen', 0, 1, 'Zeichen und Wortmarke', 'von Ihren Karten', 'ein', 'Ihr Zeichen und Ihre Wortmarke', 'Das Medaillon mit dem Haus, so wie es in Gold auf Ihren Karten steht, und Ihr Name in Versalien.', ['Medaillon', 'Wortmarke']],
        ['karten', 0, 2, 'Drei Karten', 'als PDF', 'ein', 'Ihre drei Karten', 'Schpiszettel, Schpis Charte und Tagesteller. Aus ihnen stammt jede Zeile auf der Seite «Essen».', ['Chäs- und Wystube', 'Egger- und Stettlerstube', 'Tagesteller']],
        ['texte', 0, 3, 'Ihre Texte', 'Ihre Worte', 'ein', 'Ihre Texte', 'Zimmer, Stuben und Ihr Willkommen. Die neuen Seiten erzählen das mit Ihren eigenen Worten.', ['Zimmer', 'Stuben', 'Gastgeber']],
        ['geschichte', 0, 4, 'Hausgeschichte', 'aus Ihrer Karte', 'ein', 'Ihre Hausgeschichte', 'Die Geschichte des Hauses, wie sie auf der Karte der Chäs- und Wystube steht, samt dem Bericht aus dem «Bund» von 1908.', ['1753', '1908', '1990']],
        ['film', 0, 5, 'Film', 'elf Sekunden', 'ein', 'Ihr Film', 'Der kurze Film aus einem Zimmer mit Himmelbett von Ihrer Website.', []],
        ['bildwelt', 1, 0, 'Bildwelt', 'jedes Foto mit festem Platz', '', 'Bildwelt', 'Jedes Foto hat seinen Platz und liegt in mehreren Grössen vor, für den Rechner und fürs Handy. So lädt die Seite schnell und bleibt scharf.', ['Grosse Fenster', 'Galerien', 'Zimmer-Ansichten']],
        ['muster', 1, 1, 'Zeichen und Muster', 'Gold und Butzenscheiben', '', 'Zeichen und Muster', 'Ihr Zeichen steht in Gold in der Leiste und zwischen den Abschnitten. Das Muster der Butzenscheiben liegt Ton in Ton auf den dunklen Flächen.', ['Leiste', 'Trenner', 'Flächen']],
        ['kartendaten', 1, 2, 'Karten-Daten', 'drei Karten', '', 'Karten-Daten', 'Alle Gerichte und Preise an einer Stelle. Daraus entsteht der Schpiszettel auf der Seite.', ['Gerichte', 'Preise', 'Tagesmenu']],
        ['zimmerdaten', 1, 3, 'Zimmer-Daten', 'vier Arten zu wohnen', '', 'Zimmer-Daten', 'Fotos, Satz und Preis jeder Zimmerart an einer Stelle. Daraus entstehen die Zimmer auf der Startseite und der Zimmer-Seite.', ['Fotos', 'Preise']],
        ['neugesetzt', 1, 4, 'Karten im Stil', 'als Idee', '', 'Karten im Stil der Seite', 'Die drei Karten als Idee im Stil der neuen Seite, jede neben Ihrer heutigen Fassung zum Durchblättern.', ['Schpiszettel', 'Schpis Charte', 'Tagesteller']],
        ['zeitstrahl', 1, 5, 'Zeitstrahl', 'vier Jahreszahlen', '', 'Zeitstrahl', 'Aus der Hausgeschichte sind vier Jahreszahlen geworden, jede mit Ihren eigenen Worten.', ['1753', '1908', '1990', '2000']],
        ['start', 2, 0, 'Startseite', 'das Haus zuerst', 'seite', 'Startseite', 'Vom Haus über die Stuben und die Karte zu den Zimmern und der Geschichte. Von hier führt ein Weg zu jeder anderen Seite.', ['Haus', 'Stuben', 'Zimmer']],
        ['zimmer', 2, 1, 'Zimmer', 'vier Zimmerarten', 'seite', 'Zimmer', 'Landhaus, Hochzeitsstube, Liebeslaube und Hymmelrich mit Fotos, Preis und Buchung.', ['Landhaus', 'Hochzeitsstube', 'Liebeslaube', 'Hymmelrich']],
        ['essen', 2, 2, 'Essen', 'Stuben und Karte', 'seite', 'Essen', 'Fünf Stuben, der Schpiszettel, die Herkunft der Produkte und Ihre Anlässe.', ['Stuben', 'Schpiszettel', 'Anlässe']],
        ['haus', 2, 3, 'Das Haus', 'seit 1753', 'seite', 'Das Haus', 'Geschichte, Garten, Gastgeber und Anreise.', ['Geschichte', 'Garten', 'Gastgeber']],
        ['recht', 2, 4, 'Rechtliches', 'und Bildnachweis', 'seite', 'Rechtliches', 'Angaben des Hauses und der Nachweis für die Fotos.', []],
        ['buchung', 3, 0, 'SimpleBooking', 'Buchung bleibt bei Ihnen', 'sys', 'SimpleBooking', 'Gebucht wird weiter dort, wo Sie es heute tun. Datum und Gäste gehen von der Seite direkt in Ihr Buchungssystem.', []],
        ['anfragen', 3, 1, 'Tisch und Fest', 'per E-Mail und Telefon', 'sys', 'Tisch und Fest', 'Wer einen Tisch oder ein Fest anfragen möchte, erreicht Sie per E-Mail oder Telefon.', []],
        ['pdf', 3, 2, 'Karten als PDF', 'zum Ausdrucken', 'sys', 'Karten als PDF', 'Die drei Karten liegen zusätzlich als PDF bereit.', []],
        ['studio', 3, 3, 'Studio', 'der nächste Schritt', 'sys', 'Studio', 'Das Werkzeug zur Seite. Dort ändern Sie Preise, Karte, Anlässe, Texte und Bilder selbst. Es entsteht als nächster Schritt.', ['Preise', 'Karte', 'Anlässe', 'Texte und Bilder']],
    ]
    k = [['fotos', 'bildwelt'], ['zeichen', 'muster'], ['karten', 'kartendaten'], ['texte', 'zimmerdaten'], ['karten', 'neugesetzt'], ['geschichte', 'zeitstrahl'],
         ['bildwelt', 'start'], ['bildwelt', 'zimmer'], ['muster', 'start'], ['kartendaten', 'essen'], ['zimmerdaten', 'zimmer'], ['neugesetzt', 'essen'], ['zeitstrahl', 'haus'], ['film', 'zimmer'],
         ['start', 'zimmer'], ['essen', 'haus'],
         ['start', 'buchung'], ['zimmer', 'buchung'], ['essen', 'anfragen'], ['essen', 'pdf'], ['studio', 'essen'], ['studio', 'zimmer']]
    return {'sp': ['Von Ihnen', 'Daraus gemacht', 'Die Seiten', 'Im Hintergrund'], 'fx': [0.118, 0.372, 0.628, 0.882], 'n': n, 'k': k,
            'tour': ['fotos', 'karten', 'geschichte', 'buchung', 'studio'], 'fuss': 'Jede Linie zeigt, was woraus entstanden ist',
            'start': ['Übersicht', 'Von Ihrem Material zur Seite', 'Jede Linie zeigt, was woraus entstanden ist. Fahren Sie mit der Maus über eine Kachel oder tippen Sie sie an, dann leuchtet ihr Weg auf.']}


HANDSCHRIFT = dict(
    text='Ihr Zeichen und Ihr Name bleiben, wie man sie kennt. Dazu kommen eine Schrift für die Titel, die Ihrer Wortmarke entspricht, eine ruhige für den Lesetext und die Farben Ihrer Stuben: dunkles Wandholz, Kerzenlicht und das Gold Ihres Zeichens.',
    marke_etik='Zeichen und Wortmarke',
    marke_text='Ihr Medaillon ist aus Ihrer Karte nachgezeichnet und bleibt deshalb in jeder Grösse scharf. Ihr Name steht in Versalien daneben, so wie auf Ihrer heutigen Seite.',
    schriften=[('Grosse Zeilen', 'a', 'Gelasio', 'Entspricht der Georgia, in der Ihre Wortmarke und Ihre Karten gesetzt sind.', 'Heute Abend Ihr Tisch, heute Nacht Ihr Bett.'),
               ('Lesetext', 's', 'Instrument Sans', 'Ruhig und gut lesbar, auch bei längeren Texten.', 'Gemütliche Zimmer zum Teil mit Himmelbett'),
               ('Kleine Angaben', 'm', 'DM Mono', 'Für Zeiten, Preise und Adressen.', 'Hinder de Büele 6 · 3718 Kandersteg')],
    farben=[('#1f1209', 'Stube', 'Grundfläche'), ('#321f10', 'Wandholz', 'dunkle Flächen'), ('#efe4d3', 'Papier', 'helle Fläche'), ('#c98543', 'Kerzenlicht', 'Betonung'), ('#b78f51', 'Gold', 'Zeichen, Linien'), ('#c42e13', 'Geranie', 'nur als Punkt')],
    farben_etik='aus Ihren Stuben',
    muster_etik='Ihre Butzenscheiben als Muster',
    muster_text='Das Muster auf den dunklen Flächen sind die Butzenscheiben Ihrer Fensterreihe, Ton in Ton. Es liegt auf der neuen Seite und in den Karten.')
FEED = dict(
    text1='Heute zeigt sich das Ruedihus im Instagram-Profil des Waldhotels Doldenhorn. So könnte ein eigenes aussehen: dreissig Beiträge mit Ihren eigenen Bildern, Ihr Zeichen als Profilbild und ein paar Zeilen für die Biografie.',
    text2='Zwischen den Fotos stehen Sätze aus Ihrer Karte auf dem Muster der Butzenscheiben. Zu jedem Beitrag gibt es einen Text.',
    kacheln=[(1, 'Blaue Stunde', -6, '-0.06'), (9, 'Ofestübli', 4, '0.05'), (4, 'Röschti', 5, '0.07'), (5, 'Liebeslaube', -4, '-0.04'),
             (3, 'In der Stube', 5, '0.06'), (14, 'Das Haus', -5, '-0.07'), (19, 'Terrasse', 6, '-0.05'), (13, 'Am Morgen', -4, '0.05')])
PAPIER = dict(
    etik_text='In Ihren Stuben brennen Kerzen und das Rechaud unter dem Fondue. Dazu passen Zündhölzer mit eigenem Etikett: zwölf Ideen mit Ihrem Zeichen, den Namen Ihrer Stuben und Sätzen aus Ihrer Karte.',
    druck_text='Ansichtskarten, ein Gutschein, eine Tischkarte für reservierte Tische, die Geschichte des Hauses als Blatt fürs Zimmer und einiges mehr.',
    orte_e=[(3, 6, 27, -8), (33, 0, 15, 6), (52, 8, 25, -4), (81, 2, 15, 8), (8, 50, 15, 7), (29, 54, 27, -6), (62, 52, 26, 4)],
    orte_d=[('ansichtskarte-1', 3, 3, 42, -3, 0), ('gutschein', 47, 5, 50, 3, 0), ('geschichte', 6, 42, 24, -4, 0), ('tischkarte', 36, 44, 36, 3, 0), ('untersetzer-3', 76, 40, 19, 6, 0),
            ('untersetzer-2', 40, 74, 17, -5, 0), ('gutschein-r', 62, 76, 26, 3, 0)])
MATERIAL = dict(
    text='Was für den Entwurf neu entstanden ist, liegt sortiert in einem Ordner: die Karten als PDF, die Drucksachen, die Zündholz-Etiketten, die siebenundzwanzig Beiträge für Instagram und Ihr Zeichen als Datei.',
    streu=[('haus-sommer', 'Die Terrasse', -4, '-0.05'), ('ofestuebli', 'Ofestübli', 3, '0.04'), ('z-hochzeit', 'Hochzeitsstube', -2, '-0.07'), ('garten-luft', 'Der Garten', 4, '0.05'), ('e-roesti', 'Röschti', -3, '-0.04')],
    druck_satz='Ansichtskarten, Gutschein, Tischkarte und die weiteren Ideen für Papier.',
    zeichen=[('Ihr Zeichen', 'assets/logo/zeichen.svg', 'Landgasthof Ruedihus Zeichen.svg')],
    zeichen_satz='Ihr Zeichen als Zeichnung, die in jeder Grösse scharf bleibt.',
    auslage=[('blattbild', '../unterlagen/img/n-egger-und-stettlerstube-02.webp', 2, 4, 30, -6), ('blattbild', '../drucksachen/img/ansichtskarte-1.webp', 30, 0, 44, 3), ('blattbild', '../drucksachen/img/gutschein.webp', 34, 44, 52, -3),
             ('blattbild', '../unterlagen/img/n-tagesteller-01.webp', 72, 8, 28, 6), ('form', '../zuendholz/img/e03.webp', 4, 62, 24, -5), ('form', '../drucksachen/img/untersetzer-2.webp', 84, 52, 15, 5)])
AUSBLICK = dict(
    text='Drei Dinge sind noch offen. Über jedes davon spreche ich gern mit Ihnen.',
    studio='Zur Website gehört ein Studio. Dort ändern Sie Preise, Karte, Anlässe, Texte und Bilder selbst, ohne dass jemand programmieren muss. Es entsteht als Nächstes, zusammen mit einer Anleitung für jeden Handgriff.',
    punkte=[('Ihre Fotos', 'Der Entwurf zeigt Ihre Aufnahmen von der Website und aus Ihren Einträgen bei Schweiz Tourismus und Booking.com, dazu wenige freie Fotos mit Namensnennung. Welche davon auf der fertigen Seite stehen, entscheiden Sie.'),
            ('Rechtliches', 'Impressum und Datenschutz sind angelegt. Die Angaben dazu kommen von Ihnen.')])
SCHLUSS = dict(bild='haus-wiese')

PAPIER_SEITE = dict(
    breit={'ansichtskarte-1', 'ansichtskarte-2', 'ansichtskarte-3', 'ansichtskarte-4', 'ansichtskarte-r', 'gutschein', 'gutschein-r', 'tischkarte', 'tischkarte-r', 'geschichte', 'geschichte-r', 'couvert', 'briefbogen'},
    formen={'untersetzer-1', 'untersetzer-2', 'untersetzer-3', 'untersetzer-4'},
    auslage=[('ansichtskarte-1', 28, 0, 44, 3), ('geschichte', 0, 2, 24, -6), ('gutschein', 36, 40, 52, -3), ('tischkarte', 2, 58, 32, -4), ('untersetzer-3', 80, 4, 19, 7), ('untersetzer-2', 84, 62, 16, 6), ('gutschein-r', 46, 78, 27, 3)],
    karton={'ansichtskarten': ('', [('ansichtskarte-1', 46, ''), ('ansichtskarte-2', 46, ''), ('ansichtskarte-3', 46, ''), ('ansichtskarte-4', 46, ''), ('ansichtskarte-r', 46, 'Rückseite')]),
            'gutschein': ('', [('gutschein', 88, 'Vorderseite'), ('gutschein-r', 88, 'Rückseite')]),
            'tischkarte': ('', [('tischkarte', 47, 'Vorderseite'), ('tischkarte-r', 47, 'Rückseite')]),
            'untersetzer': ('', [('untersetzer-1', 44, ''), ('untersetzer-2', 44, ''), ('untersetzer-3', 44, ''), ('untersetzer-4', 44, '')]),
            'geschichte': ('', [('geschichte', 44, 'Vorderseite'), ('geschichte-r', 44, 'Rückseite')]),
            'briefpapier': ('', [('couvert', 92, 'Couvert'), ('briefbogen', 38, 'Briefbogen')])},
    titel={'ansichtskarten': ['Grüsse aus', 'Kandersteg.'], 'gutschein': ['Ein Gutschein', 'zum Verschenken.'], 'tischkarte': ['Dieser Tisch', 'ist reserviert.'], 'untersetzer': ['Vier', 'Untersetzer.'],
           'geschichte': ['Die Geschichte', 'des Hauses.'], 'briefpapier': ['Briefbogen', 'und Couvert.']},
    schatten={'ansichtskarten', 'gutschein', 'tischkarte', 'geschichte', 'briefpapier'},
    etik_titel=('Etiketten', 'für die Zündhölzer.'),
    etik_text='In Ihren Stuben brennen Kerzen und das Rechaud unter dem Fondue. Dazu passen Zündhölzer mit eigenem Etikett. Hier sind {n} Ideen dafür, mit Ihrem Zeichen, den Namen Ihrer Stuben und Zimmer und Sätzen aus Ihrer Karte.',
    etik_kap='Die Etiketten', etik_kopf=['Zwölf kleine', 'Geschichten.'],
    etik_kopftext='Dunkles Wandholz, Kerzenlicht und das Rot der Geranien kommen von Ihrer neuen Seite, die Worte aus Ihrer Karte und von Ihrer Website.',
    etik_auslage=[(0, 4, 31, -7), (35, 0, 19, 5), (58, 6, 30, -4), (66, 42, 30, 6), (6, 40, 19, 6), (30, 38, 30, -5), (90, 2, 0, 0), (0, 76, 0, 0), (62, 72, 19, 4), (36, 74, 0, 0), (6, 76, 0, 0), (26, 72, 30, 3)])

CSS = '''
.t1,.t2,.t3{font-weight:700;letter-spacing:-.005em}
.insel__m svg{height:30px}
.tapetenband svg{height:clamp(96px,11vw,150px)}
.dazu__gross svg{height:clamp(56px,6vw,80px)}
.marke__w{color:var(--blau);max-width:560px}
.zeile__z svg{height:1.1em}
'''
MEINS = ['Der Brief und alle Sätze der Werkbank', 'Titel und Sätze zu den neun Ideen, zum Gefüge und zu den Drucksachen', 'Bildzeilen der Ansichtskarten, Feldnamen, das Wort «Reserviert»',
         'Auswahl der Sätze auf dem Blatt zur Hausgeschichte', 'Sätze zu den Zündholz-Etiketten', 'Texte zu den Beiträgen des Feeds']

# ================================================================ Eigene Werkbank dieses Hauses (09.10.2026)
# Aufbau, Reihenfolge, Auftakt und alle Überschriften sind wie beim Carlton-Europe (Robert 09.10.2026). Die Vorstellung von Robert steht
# auf der Übersicht der vier Häuser und fehlt hier bewusst. Was dieses Haus unterscheidet, steht im Inhalt: eigene Sätze (kein Satz soll
# klingen wie in den anderen Werkbänken; was nur wiederholt, fällt weg), Aufbau des Feeds, eigene Drucksachen.
AUFTAKT.update(text='Für den Landgasthof Ruedihus liegt hier eine neue Website als Entwurf auf dem Tisch. Daneben Ihre drei Karten, neu gesetzt, und ein paar Dinge für die Stuben. Nehmen Sie Platz und schauen Sie in Ruhe.')
BRIEF.update(
    art='kurz',
    absaetze=[
        'Auf das Ruedihus bin ich über Ihre anderen Häuser gekommen und dann lange geblieben. Ein Haus von 1753 mit bemaltem Giebel und Butzenscheiben, mit fünf Stuben, einer Sage vom Holz aus einer Novembernacht und einer Karte, auf der steht, was man bei Ihnen vergebens sucht. Erfinden könnte man das nicht.',
        'Am längsten habe ich über Ihren Karten gesessen. Der Schpiszettel, die Schpis Charte und die Tagesteller sind neu gesetzt, mit Ihren Gerichten und Ihren Preisen. Dazu kommen die Website, ein paar Dinge für den Tisch und ein Feed, in dem Bild und Blatt wechseln.'],
    schluss='Schauen Sie sich in Ruhe um.',
    abzuege=[('ofestuebli', 'Ofestübli', 5, '0.06'), ('schild', 'Über der Tür', -6, '-0.05')])
GABEN.update(
    papier='Anhänger mit den Namen Ihrer Zimmer, eine Banderole für die Serviette und mehr: {d} Drucksachen und {e} Etiketten für die Zündholzschachtel.',
    feed='{n} Beiträge, in denen Foto und Blatt wechseln: neben jedem Bild ein Gericht aus Ihrer Karte oder ein Satz von Ihnen.')
KAPITEL = {
    'mitgebracht': dict(text=''),
    'vergleich': dict(text='Schieben Sie den Griff nach links und nach rechts: einmal Ihre Startseite von heute, einmal die neue.'),
    'ideen': dict(text='Zu jeder Stelle der Seite gibt es einen Grund. {n} davon stehen hier.'),
    'gefuege': dict(text='Aus Ihren Fotos, Ihren Karten und Ihren Worten ist die Seite entstanden. Das Brett zeigt, was wohin gewandert ist. Tippen Sie eine Kachel an oder starten Sie den Rundgang.'),
    'seiten': dict(text='Eine Seite aussuchen, mit den Pfeilen weiterblättern. Rechts sehen Sie, wie dieselbe Stelle am Handy aussieht, und mit «Öffnen» sind Sie auf der echten Seite.'),
    'unterlagen': dict(text='Der Schpiszettel der Chäs- und Wystube, die Schpis Charte der Egger- und Stettlerstube und die Tagesteller: alle drei neu gesetzt, mit Ihren Gerichten und Ihren Preisen. Legen Sie jede neben Ihre heutige Fassung und blättern Sie durch.'),
    'papier': dict(text='Zu Ihren Stuben sind mir ein paar Dinge eingefallen: Anhänger für die Zimmerschlüssel, eine Banderole für die Serviette, Etiketten für die Zündhölzer. Nehmen Sie, was Ihnen gefällt.'),
    'material': dict(text='Die Karten als PDF, die Drucksachen, die Zündholz-Etiketten, die siebenundzwanzig Beiträge für Instagram und Ihr Zeichen als Datei: alles Neue liegt in einem Ordner beisammen.'),
    'dazu': dict(text='Ein paar Dinge fehlen noch. Über jedes rede ich gern mit Ihnen.'),
    'schluss': dict(text='Sagen Sie mir ruhig offen, was Ihnen gefällt und was nicht. Ändern lässt sich alles.'),
}
HANDSCHRIFT.update(knopf_text='Diese Knöpfe darf man drücken. Sie geben ein wenig nach.', knoepfe=('Nur zu', 'Noch einer'))
AUSBLICK.update(
    studio='Was noch fehlt, ist das Studio. Damit ändern Sie Preise, Karte, Anlässe, Texte und Bilder selbst, so einfach wie eine Tafel neu zu beschriften. Es kommt als Nächstes, mit einer Anleitung dazu.',
    punkte=[('Ihre Fotos', 'Im Entwurf sind Ihre Aufnahmen von der Website und aus Ihren Einträgen bei Schweiz Tourismus und Booking.com, dazu wenige freie Fotos mit Namensnennung. Was bleibt und was geht, sagen Sie.'),
            ('Rechtliches', 'Impressum und Datenschutz sind da. Es fehlen nur noch Ihre Angaben.')])
FEED = dict(
    art='bogen', bogen=[1, 2, 3, 4, 5, 6, 7, 8, 9], bogen_zeile='Die ersten drei Reihen',
    text1='Oben steht einmal das Haus im Grünen, ein Bild über sechs Beiträge. Darunter trägt in jeder Reihe ein Foto den Namen seines Raums.',
    text2='Nur Fotos aus dem Haus, keine Grafiken. Heute zeigt sich das Ruedihus im Profil des Waldhotels Doldenhorn, so könnte ein eigenes aussehen.')
PAPIER.update(
    druck_text='Anhänger für die Zimmerschlüssel mit den Namen Ihrer Zimmer, eine Banderole für die Serviette, eine Tischkarte, die Geschichte des Hauses als Blatt fürs Zimmer und einiges mehr.',
    orte_d=[('anhaenger-3', 3, 2, 15, -6, 1), ('anhaenger-1', 20, 5, 15, 4, 1), ('gutschein', 41, 4, 55, 3, 0), ('banderole-1', 3, 49, 58, -3, 0), ('tischkarte', 60, 38, 37, 3, 0),
            ('untersetzer-3', 10, 70, 19, 6, 0), ('untersetzer-2', 35, 73, 17, -5, 0), ('gutschein-r', 62, 78, 26, 3, 0)])
PAPIER_SEITE['druck_text'] = 'Dinge, die in Ihren Stuben und Zimmern liegen könnten: vom Anhänger am Schlüssel bis zur Banderole um die Serviette. Nehmen Sie davon, was Ihnen gefällt, den Rest lassen Sie liegen.'
PAPIER_SEITE['breit'] |= {'banderole-1', 'banderole-2'}
PAPIER_SEITE['formen'] |= {'anhaenger-1', 'anhaenger-2', 'anhaenger-3', 'anhaenger-4', 'anhaenger-r'}
PAPIER_SEITE['karton'].update({'banderole': ('', [('banderole-1', 92, 'Dunkel'), ('banderole-2', 92, 'Hell')]),
                               'anhaenger': ('', [('anhaenger-1', 22, ''), ('anhaenger-2', 22, ''), ('anhaenger-3', 22, ''), ('anhaenger-4', 22, ''), ('anhaenger-r', 22, 'Rückseite')])})
PAPIER_SEITE['titel'].update({'banderole': ['Um die', 'Serviette.'], 'anhaenger': ['Jedes Zimmer', 'hat seinen Namen.']})
PAPIER_SEITE['schatten'] |= {'banderole'}
PAPIER_SEITE['auslage'] = [('ansichtskarte-1', 30, 0, 44, 3), ('anhaenger-3', 2, 0, 15, -6), ('anhaenger-2', 16, 6, 15, 4), ('gutschein', 36, 40, 52, -3), ('tischkarte', 2, 60, 32, -4), ('untersetzer-3', 80, 4, 19, 7),
                           ('untersetzer-2', 84, 62, 16, 6), ('banderole-1', 38, 82, 46, 2)]
GABEN['seite'] = GABEN['seite'].replace('Gebucht wird weiter über Ihr SimpleBooking.', 'Ihr SimpleBooking bleibt, wie es ist.')

_gefuege = gefuege
def gefuege(z):   # dieselbe Tafel, die Sätze dazu in der Stimme dieses Hauses
    d = _gefuege(z)
    d['fuss'] = 'Folgen Sie einer Linie: Sie führt vom Material zur Seite'
    d['start'] = [d['start'][0], d['start'][1], 'Jede Kachel hat ihren Weg. Tippen Sie eine an und er leuchtet.']
    return d


# ================================================================ Studio (Kontrollpanel), seit 09.10.2026 gebaut: ../studio/ (lokal das echte, online die Probe-Fassung)
STUDIO = dict(
    ansicht='02 Übersicht',
    text='Zur Website gehört ein Studio. Dort ändern Sie Zimmerpreise, Karten, Öffnungszeit, Anlässe, Texte und Bilder selbst, so einfach wie eine Tafel neu zu beschriften. Jede Änderung wartet zuerst als Entwurf: Sie sehen sie vorher und nachher und stellen sie mit einem Knopf auf die Website. Die fünf kurzen Filme zeigen die wichtigsten Handgriffe.',
    schritte=[('1-zimmer', 'Zimmerpreis ändern', 'Zimmer öffnen, Preis eintragen, speichern. Danach stimmt er auf der Startseite und auf der Zimmer-Seite.', 'studio / zimmer & preise'),
              ('2-gericht', 'Gericht anlegen', 'Karte und Rubrik wählen, Name, Zusatz und Preis dazu, auch für kleine Portion und Portion. Rechts sehen Sie gleich, wie es auf der Karte steht.', 'studio / karten'),
              ('3-seite', 'Text in der Seite', 'Sie sehen die Seite wie Ihre Gäste. Tippen Sie auf einen Text und schreiben Sie ihn neu.', 'studio / seiten & texte'),
              ('4-bild', 'Bild tauschen', 'Foto wählen, neues hochladen, bisher und neu nebeneinander bestätigen. Es ändert sich überall, wo es zu sehen ist.', 'studio / bilder'),
              ('5-raus', 'Veröffentlichen', 'Alles wartet erst als Entwurf. Sie sehen die Liste, was live geht, und stellen es mit einem Knopf auf die Website.', 'studio / entwurf')],
    bereiche=[('Zimmer & Preise', 'Name, Satz des Hauses, Preis, Belegung und Fotos je Zimmer. Neue Zimmer kommen dazu.'),
              ('Die drei Karten', 'Jedes Gericht mit Zusatz und Preis, eigene Rubriken, das Tagesmenu, die Karte als PDF.'),
              ('Haus & Angaben', 'Öffnungszeit, Adresse, Telefon, E-Mail-Adressen, Buchungslink und die Noten der Gäste, jede nur einmal.'),
              ('Anlässe', 'Metzgete, Stubete, Ruedi-Tag mit Datum, Text, Menü und Foto, auf dem Jahreslineal.'),
              ('Stellen & Team', 'Offene Stellen und die Zahlen zum Team auf der Seite «Das Haus».'),
              ('Seiten & Texte', 'Jede Überschrift, jeder Absatz, jeder Knopf, direkt in der Seite, auch wie am Handy.'),
              ('Bilder', 'Jedes Foto tauschen, aus dem Vorrat oder neu hochgeladen, auch Startbild, Seitenköpfe und Fenster.'),
              ('Hinweis für Gäste', 'Betriebsferien oder Feiertage, zeitlich begrenzt, unten auf jeder Seite.'),
              ('Google & Co.', 'Was Google über jede Seite zeigt, und die Beschreibung jedes Bildes.'),
              ('Änderungen & Verlauf', 'Vorher und nachher ansehen, veröffentlichen, jeden früheren Stand zurückholen.')],
    hinweis='Hinter «Studio ausprobieren» liegt eine Probe-Fassung, in der Sie alles selbst ausprobieren können. Was Sie dort ändern, sehen nur Sie, auf der Seite ändert sich nichts. Nur eigene Fotos lassen sich dort noch nicht hochladen, «Aus dem Vorrat» geht. Das echte Studio mit Ihrem eigenen Passwort zieht mit um, sobald die Seite zu Ihnen kommt.',
    knopf='Studio ausprobieren')
GABEN['studio'] = '{n} Bereiche, die Sie selbst pflegen: Zimmerpreise, Karten, Zeiten, Anlässe, Texte und Bilder. Jede Änderung wartet als Entwurf, bis Sie sie veröffentlichen.'
GABEN_BILDER['studio'] = ('stube-kerze', (.5, .5))
KAPITEL['mitgebracht'] = dict(text='Fünf Dinge sind es geworden.')
KAPITEL['studio'] = dict(text='Das Studio ist das Werkzeug zur Seite. Zimmerpreise, Karten, Öffnungszeit, Anlässe, Texte und Bilder ändern Sie dort selbst, so einfach wie eine Tafel neu zu beschriften. Jede Änderung wartet erst als Entwurf, Sie sehen sie vorher und nachher und stellen sie mit einem Knopf auf die Website. Die fünf Filme zeigen die wichtigsten Handgriffe, unten stehen alle Bereiche.')
KAPITEL['dazu'] = dict(text='Drei Dinge fehlen noch. Über jedes rede ich gern mit Ihnen.')
AUSBLICK.update(studio='', gross=('Seit heute dabei', 'Das Studio', 'Zimmerpreise, Karten, Öffnungszeit, Anlässe, Texte und Bilder ändern Sie selbst. Wie das geht, zeigt der Abschnitt «Studio» weiter oben mit fünf kurzen Filmen.'))
BRIEF['absaetze'][1] = ('Am längsten habe ich über Ihren Karten gesessen. Der Schpiszettel, die Schpis Charte und die Tagesteller sind neu gesetzt, mit Ihren Gerichten und Ihren Preisen. '
                       'Dazu kommen die Website, ein Studio, mit dem Sie Preise, Karten und Bilder selbst ändern, ein paar Dinge für den Tisch und ein Feed, in dem Bild und Blatt wechseln.')
MEINS.append('Die Sätze zum Studio, zu seinen Schritten und Bereichen')

_gefuege2 = gefuege
def gefuege(z):   # das Studio ist gebaut: die Kachel sagt es, und es hängt an den Seiten, die es pflegt
    d = _gefuege2(z)
    for n in d['n']:
        if n[0] == 'studio':
            n[4] = 'Sie pflegen selbst'
            n[7] = 'Das Werkzeug zur Seite. Dort ändern Sie Zimmerpreise, Karten, Öffnungszeit, Anlässe, Texte und Bilder selbst. Jede Änderung wartet als Entwurf, bis Sie sie veröffentlichen.'
            n[8] = ['Zimmerpreise', 'Karten', 'Anlässe', 'Texte und Bilder', 'Verlauf']
    d['k'] = [k for k in d['k'] if k[0] != 'studio'] + [['studio', 'start'], ['studio', 'zimmer'], ['studio', 'essen'], ['studio', 'haus']]
    return d


# ================================================================ Werkbank final (10.10.2026, Roberts Auftrag: «komplett auf den Stand bringen, fertiges Pitch-Objekt»)
# Neu: «Für Ihre Gäste» (Gäste-Funktionen seit 10.10.2026 im Haus), «Rezeption im Chat» mit Film, Zimmermappe und Karte mit QR-Code, «Geprüft» mit eigener Seite,
# Studio mit Besuchen, Gästen und Kontrolle, Ideen neu aufgenommen (geöffnete Zustände), kein Tor, keine «Zu Gast – bei Freunden»-Zeile mehr (steht beim Doldenhorn).
ONLINE = 'https://ruedihus.tastystudios.ch/'
AUFTAKT.update(text='Für den Landgasthof Ruedihus liegt hier eine neue Website als Entwurf auf dem Tisch. Daneben Ihre drei Karten, neu gesetzt, ein paar Dinge für Ihre Gäste, eine Rezeption im Chat, ein Studio zum Selberpflegen und ein paar Dinge für die Stuben. Nehmen Sie Platz und schauen Sie in Ruhe.')
BRIEF['absaetze'][1] = ('Am längsten habe ich über Ihren Karten gesessen. Der Schpiszettel, die Schpis Charte und die Tagesteller sind neu gesetzt, mit Ihren Gerichten und Ihren Preisen. '
                       'Dazu kommen die Website, ein paar Dinge, die Ihren Gästen das Buchen und den Abend leichter machen, eine Rezeption im Chat, ein Studio, mit dem Sie Preise, Karten und Bilder selbst ändern, '
                       'ein paar Dinge für den Tisch und ein Feed, in dem Bild und Blatt wechseln.')
KAPITEL['mitgebracht'] = dict(text='Sechs Dinge sind es geworden.')
IDEEN[:] = [
    ('Rechner/Startseite', 'Das Haus im ersten Bild', 'Ihr Haus unter den Bäumen steht gross im ersten Bild, daneben der Satz «1753 gebaut. Heute Abend Ihr Tisch, heute Nacht Ihr Bett.» und gleich darunter die Buchung.', '50% 50%'),
    ('Ideen/frage', '«Was führt Sie zu uns?»', 'Eine Nacht, ein Znacht, zu zweit oder ein Fest: Der Gast tippt eine Karte an, und die Galerie zeigt, was Ihr Haus dafür bereithält.', '50% 50%'),
    ('Ideen/stuben', 'Fünf Stuben, zwei Stockwerke', 'Unten das Parterre mit Chäs-u Wystube, Jungestube und Ofestübli, eine Treppe höher die Egger- und Stettlerstube. Jede Stube mit ihrem Bild.', '50% 50%'),
    ('Ideen/grundsatz', 'Ihr Grundsatz, gross', 'Der Satz aus Ihrer Karte, was man bei Ihnen vergebens sucht, steht als Fenster mitten auf der Seite «Essen».', '50% 50%'),
    ('Ideen/zimmer', 'Jedes Zimmer mit seinen Fotos', 'Landhaus, Hochzeitsstube, Liebeslaube und Hymmelrich stehen je mit drei Fotos, Ihrem Satz und dem Preis für sich.', '50% 40%'),
    ('Ideen/buehne', 'Alle Fotos auf einen Klick', 'Ein Klick auf «Alle Fotos» öffnet die Bühne: jedes Bild gross, Pfeile zum Blättern, die kleinen Bilder darunter zum Springen.', '50% 50%'),
    ('Ideen/film', 'Am Morgen die Vorhänge auf', 'Ihr kurzer Film aus dem Zimmer mit Himmelbett hat einen eigenen Platz bekommen. Er startet erst, wenn man ihn antippt.', '50% 50%'),
    ('Ideen/zahlen', 'Seit 1753', 'Vier Jahreszahlen aus Ihrer Karte, jede mit Ihren eigenen Worten: 1753, 1908, 1990 und 2000. Sie zählen hoch, wenn man bei ihnen ankommt.', '50% 50%'),
    ('Ideen/anlaesse', 'Metzgete, Stubete, Ruedi-Tag', 'Ihre Anlässe liegen auf einem Jahreslineal auf der Seite «Essen», jeder mit Datum, Menü und Foto.', '50% 50%'),
    ('Ideen/noten', 'So sehen es die Gäste', 'Ihre Noten bei Booking.com und Google stehen als zwei Karten nebeneinander, die Zahlen zählen hoch.', '50% 50%'),
]

# ---------- Für Ihre Gäste (Gäste-Funktionen, im Haus seit 10.10.2026: Block «Gäste-Funktionen» in bau.py, assets/js/dienste.js) ----------
GAESTE = [   # Bild (_werkbank/ansichten/Gaeste/<n>.jpg, node _werkbank/gaeste.js), Titel, Satz, Ausschnitt
    ('finder', 'Zimmer mit Tagespreis', 'Mit wem und wann? Zwei Fragen im Buchen-Fenster, dann steht das passende Zimmer da, mit dem Preis des Tages aus Ihrem Buchungssystem. Gibt es das System den Preis gerade nicht her, stehen Ihre Ab-Preise.', '50% 50%'),
    ('tisch', 'Tisch in der Stube', 'Im selben Fenster der Reiter «Tisch»: Stube wählen, Tag, Uhrzeit, Personen und Menü. Die Anfrage kommt bei Ihnen an.', '50% 50%'),
    ('gutschein', 'Gutschein online', 'Ein Wert, ein Abend in der Stube oder der Gourmetaufenthalt: antippen, Widmung schreiben, bezahlen. Der Gutschein kommt als PDF. Die Zahlung ist im Entwurf eine Probe und steht auch so da.', '50% 30%'),
    ('rechner', 'Welche Stube für Ihr Fest?', 'Gäste und Menü wählen: Die passende Stube und ein erster Richtpreis aus Ihren Karten stehen sofort da, als erster Entwurf gekennzeichnet, als PDF zum Mitnehmen.', '50% 0'),
    ('anreise', 'Vor Ihrer Anreise', 'Eine Seite für Gäste, die schon gebucht haben: Ankunftszeit, Tisch in der Stube und Termin im Spa. Alles kommt gesammelt bei Ihnen an.', '50% 0'),
    ('besuche', 'Besuche & Anfragen im Studio', 'Was auf der Seite passiert: Besuche, Klicks auf «Buchen», gefragte Zimmer, Tischanfragen und Gutscheine der letzten 30 Tage. Ohne Kekse, ohne Namen.', '50% 0'),
]
GAESTE_TEL = [('finder-h', 'Zimmer-Finder am Handy'), ('anreise-lang', 'Vor Ihrer Anreise'), ('tisch-h', 'Tisch in der Stube')]
GAESTE_KNOEPFE = [('Zimmer-Finder ausprobieren', '../zimmer.html'), ('Vor Ihrer Anreise', '../anreise.html'), ('Welche Stube für Ihr Fest?', '../essen.html#rechner')]
GAESTE_LINK = '../zimmer.html'
GABEN['gaeste'] = '{n} Dinge für Ihre Gäste: das Zimmer mit Tagespreis, der Tisch in der Stube, der Gutschein online und der Fest-Rechner.'
GABEN_BILDER['gaeste'] = ('stube-rund', (.5, .5))
KAPITEL['gaeste'] = dict(text='{n} Dinge, die Ihren Gästen das Buchen und den Abend leichter machen. Alles ist im Entwurf gebaut und lässt sich ausprobieren, alles rechnet mit Ihren Zahlen: aus dem Buchungssystem und aus Ihren Karten. Geschätzt ist nichts.')

# ---------- Rezeption im Chat (seit 10.10.2026 auf allen Seiten, assets/js/gast.js; Seite rezeption/, Zimmermappe mappe.html aus mappe.py) ----------
REZEPTION = [
    ('Antwortet sofort, auch spätabends', 'Unten rechts auf jeder Seite. Gäste fragen nach dem Fondue, dem Himmelbett oder dem Alter des Hauses und bekommen die Antwort aus Ihren Seiten und Karten, in Deutsch, Englisch und Französisch.'),
    ('Bucht, ohne die Seite zu verlassen', 'Fragt ein Gast nach Daten, legt sie die Buchungsmaske ins Gespräch. «Zur Buchung» öffnet Ihr Buchungssystem in einem grossen Fenster, mit den Daten des Gastes. Bezahlt wird dort wie bisher.'),
    ('Kennt das Wetter und den Weg hinauf', 'Die Vorhersage der nächsten Tage für Kandersteg, den Oeschinensee und den Gemmipass, dazu die Seiten der Bahnen. Bei Regen schlägt sie die Stube vor, bei klarem Himmel die Höhe.'),
    ('Schreibt Entwürfe für Anfragen', 'Verein, Familienfest, Gruppe: Die Mail des Gastes kommt hinein, ein Entwurf im Ton des Hauses kommt heraus, mit Stuben, Sitzplätzen und Preisen aus Ihren Karten. Verschickt wird erst, wenn jemand von Ihnen gelesen hat.'),
]
REZEPTION_HINWEIS = 'Noch ist die Rezeption im Chat zum Ausprobieren da. Freie Zimmer kann sie erst nachsehen, wenn Ihr Buchungssystem ihr den Zugang gibt; bis dahin übergibt sie an die Buchung. Die Kosten je Frage richten sich nach dem Sprachmodell, das Ihr Haus wählt.'
MAPPE_ADRESSE = ONLINE + 'mappe.html'
QR_KARTE = 'drucksachen/img/mappekarte.webp'
CHAT_FRAGE = 'Wir sind zu zweit und möchten am Abend Fondue essen. Geht das?'
CHAT_FRAGE_H = 'Wir sind zu zweit und möchten am Abend Fondue essen. Geht das?'   # Robert 18.10.2026 23:31: keine Frage nach dem Alter des Hauses
REZEPTION_KARTEN = dict(
    mappe=('Am Handy', 'Die Zimmermappe.', 'Der Gast scannt die Karte im Zimmer und fragt in der Sprache seines Handys nach der Stube, der Karte oder dem Weg zum Oeschinensee. Was sich im Haus ändert, steht noch am selben Tag in der Mappe.'),
    karte=('Auf dem Nachttisch', 'Die Karte mit dem Code.', 'Eine Karte im Stil Ihrer Drucksachen, A6 zum Aufstellen, mit dem QR-Code zur Mappe. Hinten steht, was man alles fragen kann.'),
    seite=('Eigene Seite', 'Rezeption im Chat.', 'Ein Gespräch am Handy Schritt für Schritt, vier Antworten vom 10. Oktober im Wortlaut, die Buchung im Gespräch, das Wetter und was die Rezeption nicht tut.'))
KAPITEL['rezeption'] = dict(text='Unten rechts auf jeder Seite sitzt die Rezeption des Ruedihus als Gespräch. Ein Gast tippt seine Frage, die Antwort kommt sofort, aus Ihren Seiten und Karten, in seiner Sprache, auch wenn im Haus längst Ruhe ist. Der Film zeigt, wie sich das anfühlt. Alles, was die Rezeption kann, steht auf einer eigenen Seite.')

# ---------- Geprüft (nur Belegtes: _qa/Messprotokoll.md, _qa/rand.js, _qa/klick.js, _qa/studio.js, _qa/kontrolle_test.py, studio.py LEXIKON, satz_pruefe, sicherheit.py, Stand 10.10.2026) ----------
GEPRUEFT = [
    ('Die Website', 'seite', ['Am Handy und am Rechner, von 320 bis 1728 Pixeln Breite, in Safari- und Chrome-Technik: nichts läuft seitlich über, kein Skriptfehler.',
                              'Auf gebremster Rechenleistung geprüft, wie auf einem schwachen Gerät: Alle Seiten laufen beim Scrollen ohne Ruckeln.',
                              'Buchung, Frage-Karten, Lupe, Galerie, Zahlen, Lauftexte, Bühne je Zimmer, Karten, Film und Menü am Handy durchgeklickt.',
                              'Jedes Foto kommt in der Reihenfolge, in der man es sieht; das Kopfbild zuerst leicht, dann scharf, hinter jedem Bild seine Farbe statt Schwarz.']),
    ('Die drei Karten', 'karte', ['Schpiszettel, Schpis Charte und Tagesteller Zeile für Zeile gegen Ihre PDFs gelesen, Wort für Wort geprüft.',
                                  '70 Tippfehler aus den Originalen berichtigt, jeder einzeln festgehalten, damit Sie nachsehen können.',
                                  'Satz auf jeder Seite geprüft: nichts abgeschnitten, nichts überdeckt, Schriften fest eingebettet, echte Kursive.',
                                  'Was das Haus klären muss, steht gesondert: zwei Gutschein-Preise, die sich widersprechen, ein fehlender vierter Tagesteller, zwei Telefonnummern.']),
    ('Das Studio', 'schloss', ['55 Prüfpunkte durch jeden Bereich bis zum Veröffentlichen und zurück, in einer eigenen Probe mit eigenen Daten, zuletzt am 10. Oktober: alle grün.',
                               'Die Kontrolle prüft das Werkzeug selbst: 20 Punkte, ein Lexikon mit 20 Fehlerquellen, acht Reparaturen und eine Prüfseite, die auch ohne das Studio läuft.',
                               'Jede Änderung wartet als Entwurf, mit Vorher und Nachher. Jeder veröffentlichte Stand bleibt im Verlauf und lässt sich zurückholen.',
                               'Das echte Studio antwortet nur am Rechner des Hauses und lehnt Anfragen von fremden Seiten ab. Online steht eine Probe ohne Hochladen.']),
]
GEPRUEFT_OFFEN = 'Dazu, was ehrlich offen bleibt: die Namen von vier Stuben-Fotos, das Königspaar und das Jahr des Bundesratsfotos, die Preise aus dem Buchungssystem und Ihr Blick auf die Fotos.'
GEPRUEFT_BILD = 'stube-kerze'
GEPRUEFT_NAV = ['Website', 'Karten', 'Studio', 'Daten', 'Offen']
GEPRUEFT_EIN = 'Bevor Sie etwas zu sehen bekommen, ist es durchgegangen worden: die Website auf jedem Gerät, die drei Karten Wort für Wort, das Studio bis zum letzten Knopf, der Umgang mit Ihren Daten. Hier steht, was genau, ohne Fachwörter. Und was ehrlich offen bleibt, steht auch da.'
GEPRUEFT_MEHR = [
    ('Die Website', 'seite', 'Fünf Seiten und die Seite «Vor Ihrer Anreise», dazu das Rechtliche mit Bildnachweis.', [
        'Am Handy und am Rechner in elf Breiten von 320 bis 1728 Pixeln, in Safari- und Chrome-Technik: nichts läuft seitlich über, kein Skriptfehler.',
        'Auf gebremster Rechenleistung geprüft, wie auf einem schwachen Gerät: Startseite, Zimmer, Essen und Das Haus laufen beim Scrollen ohne Ruckeln. Der Film im Zimmer startet erst auf Tastendruck, weil ein Film, der von selbst anläuft, gebremst einen Hänger machte.',
        'Buchung, Frage-Karten, Lupe, Galerie, Zahlen, Lauftexte, Bühne je Zimmer, Karten, Film und Menü am Handy in einer Klickprüfung durchgeklickt, ohne Fehler.',
        'Bilder: Das Kopfbild jeder Seite kommt zuerst leicht und dann scharf, alle anderen Fotos warten, bis es da ist; jedes Foto hat seinen Platz in mehreren Grössen für Rechner und Handy; hinter jedem Bild liegt seine mittlere Farbe statt Schwarz.',
        'Jede Angabe auf der Seite wurde wörtlich gegen Ihre Karten, Ihre Website und Ihre Einträge geprüft; was abgeleitet ist, steht so im Faktenblatt.',
        'Vor jedem Hochladen wird jede Seite am Rechner und am Handy geöffnet und bis unten gefahren; jede fehlende Datei würde gemeldet.']),
    ('Die drei Karten', 'karte', 'Schpiszettel, Schpis Charte und Tagesteller, neu gesetzt im Stil der Seite.', [
        'Alle drei Karten Zeile für Zeile gegen Ihre PDFs gelesen; ein Prüflauf vergleicht nach jedem Bau Wort für Wort.',
        '70 Tippfehler aus den Originalen berichtigt, jeder einzeln in einer Liste festgehalten.',
        'Am 13. Oktober dazugekommen: das Heft mit den Menuvorschlägen für Feste von 2023, zwanzig Seiten. Wort für Wort und Preis für Preis gegen Ihr PDF gelesen, 48 Stellen berichtigt (Tippfehler und Satzzeichen), jede in einer Liste. An den Preisen von 2023 ist nichts geändert, das Jahr steht auf jeder Seite.',
        'Satz auf jeder Seite geprüft, in beiden Browser-Techniken: nichts abgeschnitten, nichts überdeckt. Die Schriften sind fest in die PDF eingebettet, die Übersetzungszeilen stehen in echter Kursive.',
        'Weggelassen: der im Original unsichtbare Satz zu einem Rabatt und die Fotounterschrift zu einer Fernsehsendung.',
        'Was das Haus klären muss, steht gesondert: Gutschein-Preise, die sich zwischen Schpiszettel und Tagesteller widersprechen, der fehlende vierte Tagesteller im Original, zwei Schreibweisen des Walliser Kaffees, zwei Telefonnummern. Im Heft von 2023 stehen für die Eggerstube 24 und 26 Plätze, für die Stettlerstube 18 und 24.']),
    ('Das Studio', 'schloss', 'Das Werkzeug, mit dem Sie die Seite selbst pflegen.', [
        '55 Prüfpunkte durch jeden Bereich: Gericht anlegen, ändern, ausblenden, zurückholen, falscher Preis, eigene Rubrik, Zeit speichern, Weggehen ohne Speichern, falsche E-Mail, Zimmerpreis, neues Zimmer, Anlass, Bild und festes Bild tauschen, Text in der Seite, Hinweis, Veröffentlichen, Verlauf, Zurückholen. Danach werden die gebauten Seiten gelesen.',
        'Die Kontrolle prüft das Werkzeug selbst: 20 Punkte auf dem Server, ein Lexikon mit 20 Fehlerquellen, jede mit Prüfung und Behebung, acht Reparaturen. Die Prüfseite läuft auch, wenn der Rest nicht mehr lädt.',
        'Absichtlich kaputte Zustände wurden hergestellt; die Kontrolle musste jeden melden und nach der Reparatur wieder grün sein: 59 Schritte, alle grün, zuletzt am 10. Oktober.',
        'Das echte Studio antwortet nur am Rechner des Hauses und lehnt Anfragen von fremden Seiten ab. Fehlermeldungen geben keine Innereien preis.',
        'Online steht eine Probe-Fassung: jeder Besucher arbeitet in seiner eigenen Kopie, Hochladen ist dort ausgeschaltet, auf der Seite ändert sich nichts.',
        'Jede Änderung wartet als Entwurf, mit Vorher und Nachher an jeder Stelle. Jeder veröffentlichte Stand bleibt im Verlauf und lässt sich zurückholen.']),
    ('Ihre Daten und die Ihrer Gäste', 'schild', 'Was die Seite speichert und was nicht.', [
        'Die Website setzt für Gäste keine Kekse. «Besuche & Anfragen» im Studio zählt Klicks ohne Namen und ohne Adressen; Prüfläufe zählen nicht mit.',
        'Jede Antwort der Online-Fassung trägt Sicherheits-Kopfzeilen: keine fremde Seite darf den Entwurf einbetten, kein Dateityp wird geraten, Kamera, Mikrofon und Standort bleiben aus.',
        'Die Rezeption im Chat nimmt keine Karten- oder Passdaten entgegen, speichert Fragen ohne Mail-Adressen und Nummern und löscht sie nach zwölf Monaten. Wer in kurzer Zeit sehr viel fragt, landet bei der Telefonnummer.',
        'Online läuft alles über eine verschlüsselte Verbindung. Der Entwurf ist für Suchmaschinen gesperrt, bis Sie ihn freigeben.']),
    ('Was ehrlich offen bleibt', 'auge', 'Diese Dinge liegen nicht in meiner Hand.', [
        'Vier Stuben-Fotos tragen noch keinen sicheren Namen; nur das Ofestübli ist belegt. Welche Stube auf welchem Bild zu sehen ist, sagen Sie mir am besten selbst.',
        'In der Gäste-Galerie auf «Das Haus» sind das Königspaar und das Jahr des Bundesratsfotos aus freien Quellen abgeleitet und vom Haus nicht bestätigt.',
        'Echte Preise und freie Zimmer online: Das Buchungssystem bricht Anfragen aus Rechenzentren ab. Dafür braucht der Entwurf einen offiziellen Zugang des Hauses; bis dahin zeigt der Finder Ihre Ab-Preise und führt zur Buchung.',
        'Ihre Fotos: Die Aufnahmen stammen von Ihrer Website, aus Ihren Einträgen bei Schweiz Tourismus und Booking.com und wenigen freien Quellen mit Namensnennung. Welche auf der fertigen Seite stehen, entscheiden Sie.',
        'Rechtliches: Impressum und Datenschutz sind angelegt, die Angaben dazu kommen von Ihnen. Die Seite spricht bisher Deutsch; die Rezeption im Chat antwortet auch auf Englisch und Französisch.']),
]
KAPITEL['geprueft'] = dict(text='Bevor diese Werkbank zu Ihnen kommt, ist jedes Teil durchgegangen worden: die Website auf jedem Gerät, die drei Karten Wort für Wort, das Studio bis zum letzten Knopf, der Umgang mit Ihren Daten. Was genau, steht auf einer eigenen Seite, in Alltagssprache.')

# ---------- Studio: mit Besuchen & Anfragen, Gästen & Anfragen (online) und der Kontrolle ----------
STUDIO['text'] = ('Zur Website gehört ein Studio. Dort ändern Sie Zimmerpreise, Karten, Öffnungszeit, Anlässe, Texte und Bilder selbst, so einfach wie eine Tafel neu zu beschriften. '
                  'Jede Änderung wartet zuerst als Entwurf: Sie sehen sie vorher und nachher und stellen sie mit einem Knopf auf die Website. Dazu sehen Sie, was auf der Seite passiert, '
                  'was Ihre Gäste die Rezeption im Chat fragen, und eine Kontrolle prüft das Werkzeug selbst. Die fünf kurzen Filme zeigen die wichtigsten Handgriffe.')
KAPITEL['studio'] = dict(text=STUDIO['text'])
STUDIO['bereiche'] += [('Besuche & Anfragen', 'Besuche, Klicks auf «Buchen», gefragte Zimmer, Tischanfragen und Gutscheine der letzten 30 Tage, ohne Kekse.'),
                       ('Gäste & Anfragen', 'Was die Rezeption im Chat gefragt wurde, und Entwürfe für Antworten auf Anfragen von Vereinen und Familien.'),
                       ('Kontrolle', 'Das Studio prüft sich selbst: 20 Punkte, ein Lexikon mit 20 Fehlerquellen, acht Reparaturen, auch wenn der Rest nicht mehr lädt.')]
STUDIO['bilder'] = [('zimmer', 'Zimmer & Preise: Name, Satz, Preis, Fotos'), ('besuche', 'Besuche & Anfragen: was auf der Seite passiert'), ('gaeste', 'Gäste & Anfragen: die Fragen an die Rezeption'), ('kontrolle', 'Kontrolle: das Studio prüft sich selbst')]
GABEN['studio'] = '{n} Bereiche, die Sie selbst pflegen: Zimmerpreise, Karten, Zeiten, Anlässe, Texte und Bilder, dazu die Besuche der Seite, die Fragen Ihrer Gäste und eine Kontrolle, die das Werkzeug selbst prüft.'

_gefuege3 = gefuege
def gefuege(z):   # die Gäste-Funktionen und die Rezeption im Chat laufen im Hintergrund mit
    d = _gefuege3(z)
    d['n'].append(['dienste', 3, 4, 'Für Ihre Gäste', 'Preis, Stube, Chat', 'sys', 'Gäste-Funktionen',
                   'Zimmer mit Tagespreis, Tisch in der Stube, Gutschein online, Fest-Rechner, «Vor Ihrer Anreise» und die Rezeption im Chat. Alles mit Ihren Zahlen, nichts geschätzt.', []])
    d['k'] += [['zimmer', 'dienste'], ['essen', 'dienste'], ['studio', 'dienste']]
    d['tour'] = ['fotos', 'karten', 'geschichte', 'buchung', 'dienste', 'studio']
    return d

# ---------- Ausblick ----------
KAPITEL['dazu'] = dict(text='Drei Dinge fehlen noch. Über jedes rede ich gern mit Ihnen.')
AUSBLICK.update(
    gross=('Der nächste Schritt', 'Die Anleitung', 'Zum Studio gehört eine Anleitung, die jeden Handgriff Schritt für Schritt zeigt, mit Filmen und Bildern. Sie entsteht als Nächstes. Dazu zieht das Studio auf einen eigenen kleinen Server zu Ihnen um, damit Ihre Änderungen dauerhaft bleiben; bis dahin probieren Sie alles in der Probe aus.'),
    punkte=[('Ihre Fotos', 'Im Entwurf sind Ihre Aufnahmen von der Website und aus Ihren Einträgen bei Schweiz Tourismus und Booking.com, dazu wenige freie Fotos mit Namensnennung. Was bleibt und was geht, sagen Sie.'),
            ('Preise aus dem Buchungssystem', 'Der Zimmer-Finder und die Rezeption im Chat zeigen online echte Preise und freie Zimmer, sobald das Buchungssystem dem Entwurf einen Zugang gibt. Den Preisvergleich mit den Portalen schalten Sie dort ein; bis dahin steht ein beschriftetes Beispiel.'),
            ('Rechtliches', 'Impressum und Datenschutz sind da. Es fehlen nur noch Ihre Angaben.')])

# ---------- Papier: die Karte zur Zimmermappe ----------
PAPIER_SEITE['karton']['mappekarte'] = ('', [('mappekarte', 44, 'Vorderseite'), ('mappekarte-r', 44, 'Rückseite')])
PAPIER_SEITE['titel']['mappekarte'] = ['Die Karte', 'zur Zimmermappe.']
PAPIER_SEITE['schatten'] |= {'mappekarte'}
PAPIER['druck_text'] = 'Anhänger für die Zimmerschlüssel mit den Namen Ihrer Zimmer, eine Banderole für die Serviette, eine Tischkarte, die Karte zur Zimmermappe mit dem QR-Code, die Geschichte des Hauses als Blatt fürs Zimmer und einiges mehr.'
MEINS += ['Die Sätze zu den Gäste-Funktionen, zur Rezeption im Chat und zum Prüfbericht', 'Alle Sätze auf der Karte zur Zimmermappe']


# ================================================================ Auf dem Stand der Werkbank des Grand Beau-Rivage (12.10.2026, Roberts Auftrag; Master «Website-Bau», Abschnitt 5b)
# Aufbau, Reihenfolge und Überschriften wie bei den Schwesterhäusern, Oberfläche und Stimme vom Ruedihus: Wandholz, Kerzenlicht, Butzenscheiben, Gelasio fett.
# Jeder Baustein liegt als eigenes Modul in _werkbank/ und hängt hier über die Haken des Kits (EIGENE, brief_abschnitt, gabe_html, geprueft_abschnitt,
# wege_abschnitt, nach_bau). Das Kit selbst bleibt unverändert. Sicherung davor: _sicherung/2026-10-12-werkbank-vor-ueberarbeitung/.
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
EIGENE, EIGENE_BILDER, FLAECHE = [], [], {}
SCHRIFT_MEHR = ['gelasio-500.woff2']          # der grosse erste Absatz im Brief steht in Gelasio 500
_WB = os.path.join(ROOT, 'werkbank')

# ---------- Auftakt: kein Wort zur Person, kein «in Ruhe» (Master 5, Regel 7) ----------
AUFTAKT.update(text='Für den Landgasthof Ruedihus liegt hier eine neue Website als Entwurf auf dem Tisch. Daneben Ihre drei Karten als Idee im selben Stil, ein paar Dinge für Ihre Gäste, '
                    'eine Rezeption im Chat, ein Studio zum Selberpflegen und einiges für die Stuben. Nehmen Sie Platz.')

# ---------- Brief: das Haus über die ganze Breite, der Brief als Blatt darüber (brief_blatt.py) ----------
BRIEF.update(
    bild='haus-sommer', schnitt=2.0, lage=(.5, .56), bild_alt='Der Landgasthof Ruedihus in Kandersteg hinter Laub, davor die Terrasse mit den Schirmen',
    schild=('Landgasthof Ruedihus', 'Kandersteg · seit 1753'), ort='Tasty Studios',
    absaetze=[
        'Auf das Ruedihus bin ich über Ihre anderen Häuser gekommen und dann lange geblieben. Ein Haus von 1753 mit bemaltem Giebel und Butzenscheiben, mit fünf Stuben und einer Karte, auf der steht, was man bei Ihnen vergebens sucht. Erfinden könnte man das nicht.',
        'Für dieses Haus liegt hier eine neue Website als Entwurf auf dem Tisch. Sie erzählt von den Stuben und vom Schpiszettel, von den Zimmern unter den alten Balken und von der Novembernacht, in der das Holz für das Haus geschlagen wurde. Gebucht wird weiter in Ihrem SimpleBooking.',
        'Am längsten habe ich über Ihren Karten gesessen. Den Schpiszettel, die Schpis Charte und die Tagesteller habe ich als Idee im Stil der neuen Seite gesetzt, mit Ihren Gerichten und Ihren Preisen.',
        'Dazu kommen ein paar Dinge, die Ihren Gästen das Buchen und den Abend leichter machen, eine Rezeption im Chat, die auch dann antwortet, wenn im Haus längst Ruhe ist, und ein Studio, in dem Sie Preise, Karten und Bilder selbst ändern, so einfach wie eine Tafel neu zu beschriften.',
        'Für die Stuben sind Anhänger mit den Namen Ihrer Zimmer entstanden, eine Banderole für die Serviette und Etiketten für die Zündhölzer. Und für Instagram ein Feed, in dem Foto und Blatt wechseln.'],
    schluss='Gefällt Ihnen, was hier liegt, setze ich mich gern mit Ihnen an einen Tisch, und wir reden darüber, wie daraus Ihre Website wird.')
import brief_blatt as _bb  # noqa: E402
brief_abschnitt = _bb.abschnitt(globals())
EIGENE_BILDER += _bb.bilder(BRIEF)
CSS += _bb.CSS

# ---------- Mitgebracht: Kacheln mit Kuhle (gaben_kuhle.py). Jedes Foto steht auf der Seite nur einmal. ----------
import gaben_kuhle as _gk  # noqa: E402
gabe_html, GABEN_KLASSE, GABEN_BILD = _gk.gabe, _gk.KLASSE, _gk.GABEN_BILD
GABEN_BILDER.update(seite=('haus-fassade', (.5, .56)), gaeste=('terrasse', (.5, .6)), unterlagen=('e-roesti', (.36, .5)), papier=('schild', (.5, .42)), material=('e-plaettli', (.5, .5)))
GABEN_BILDER['studio'] = ('stube-lang', (.5, .6))
KAPITEL['mitgebracht'] = dict(text='')
MATERIAL['streu'] = [('balkon', 'Die Laube', -4, '-0.05'), ('ofestuebli', 'Ofestübli', 3, '0.04'), ('z-hochzeit', 'Hochzeitsstube', -2, '-0.07'), ('garten-luft', 'Der Garten', 4, '0.05'), ('e-terrine', 'Aus der Küche', -3, '-0.04')]
CSS += _gk.CSS

# ---------- Abschnittsköpfe mittig mit dem Medaillon in Gold, Kacheln im Auftakt ----------
import kopf_mitte as _km  # noqa: E402
import auftakt_kacheln as _ak  # noqa: E402
CSS += _km.CSS + _ak.CSS

# ---------- Leichte Tapete: die Butzenscheiben auch auf den ruhigen Flächen, mit der Flächenfarbe darüber zurückgenommen ----------
FLAECHE.update(brief='fl--papier tapete-hell', mitgebracht='fl--navy tapete', vergleich='fl--nacht tapete-leicht', ideen='fl--blau tapete-leicht', gefuege='fl--nacht tapete-leicht',
               seiten='fl--papier tapete-hell', gaeste='fl--navy tapete', unterlagen='fl--tief tapete-leicht')
CSS += '''
/* ---------- Leichte Tapete (12.10.2026): keine Fläche ganz ohne Muster neben einer mit ---------- */
.tapete-leicht{background-image:linear-gradient(var(--tl),var(--tl)),var(--muster);background-size:auto,var(--musterb) auto;background-position:0 0,50% 0}
.fl--nacht.tapete-leicht{--tl:rgba(31,18,9,.42)}
.fl--blau.tapete-leicht{--tl:rgba(52,30,12,.4)}
.fl--tief.tapete-leicht{--tl:rgba(23,13,6,.42)}
.tapete-hell{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='56'%3E%3Cg fill='none' stroke='%237d4f27' stroke-opacity='.075' stroke-width='1.4'%3E%3Ccircle cx='28' cy='28' r='21'/%3E%3Ccircle cx='28' cy='28' r='5'/%3E%3Cpath d='M0 0h56v56H0z'/%3E%3C/g%3E%3C/svg%3E");background-size:56px auto;background-position:50% 0}
'''


# ---------- Seiten: die Startseite beginnt seit Fassung 4 mit dem Sommerbild ----------
SEITEN[0] = ('index.html', 'Startseite', 7, 'Das Haus unter den Bäumen im ersten Bild, danach die Stuben, die Karte, die Zimmer und die Geschichte seit 1753.', '')

# ---------- Vergleich für drei Seiten, daneben «Was neu ist» (Aufnahmen: node _werkbank/vorher.js → ansichten/Vorher/) ----------
VORHER = [
    ('startseite', 'Startseite', 'Das Haus zuerst, die Buchung gleich darunter.',
     ['Ihr Haus unter den Bäumen steht gross im ersten Bild, daneben der Satz «1753 gebaut. Heute Abend Ihr Tisch, heute Nacht Ihr Bett.»',
      'Anreise, Abreise und Gäste wählt man gleich unter dem Bild. Gebucht wird wie bisher in Ihrem SimpleBooking.',
      'Danach kommen die Stuben, die Karte, die Zimmer und die Geschichte seit 1753, jede mit eigenen Fotos.'], 'index.html'),
    ('zimmer', 'Zimmer', 'Vier Arten zu wohnen, jede für sich.',
     ['Landhaus, Hochzeitsstube, Liebeslaube und Hymmelrich stehen je mit drei Fotos, Ihrem Satz und dem Preis da.',
      'Ein Klick auf «Alle Fotos» öffnet die Bühne mit jedem Bild in gross.',
      'Ihr kurzer Film aus dem Zimmer mit Himmelbett hat einen eigenen Platz und startet erst, wenn man ihn antippt.'], 'zimmer.html'),
    ('essen', 'Essen', 'Fünf Stuben und drei Karten auf einer Seite.',
     ['Unten das Parterre mit Chäs-u Wystube, Jungestube und Ofestübli, eine Treppe höher die Egger- und Stettlerstube. Jede Stube mit ihrem Bild.',
      'Ihre drei Karten stehen mit jedem Gericht und Preis auf der Seite und liegen zusätzlich als PDF bereit.',
      'Metzgete, Stubete und Ruedi-Tag liegen auf einem Jahreslineal, und der Fest-Rechner nennt die passende Stube.'], 'essen.html'),
]
VERGLEICH_TEXT = 'Links Ihre Seite von heute, rechts die neue. Den Griff schieben Sie hin und her, und daneben lesen Sie, was sich geändert hat.'

# ---------- Für Ihre Gäste: fünf Karten. «Vor Ihrer Anreise» steht jetzt bei «Rund um den Aufenthalt». ----------
GAESTE[:] = [g_ for g_ in GAESTE if g_[0] != 'anreise']
GAESTE_TEL = []
GAESTE_KNOEPFE = [('Zimmer-Finder ausprobieren', '../zimmer.html'), ('Welche Stube für Ihr Fest?', '../essen.html#rechner'), ('Gutschein ansehen', '../zimmer.html#gutschein')]
GABEN['gaeste'] = 'Das Zimmer mit dem Preis des Tages, der Tisch in der Stube, der Gutschein online und der Fest-Rechner. Was davon genutzt wird, sehen Sie im Studio.'
KAPITEL['gaeste'] = dict(text='{n} Dinge, die Ihren Gästen das Buchen und den Abend leichter machen. Alles ist im Entwurf gebaut und lässt sich ausprobieren, und alles rechnet mit Ihren Zahlen: aus dem Buchungssystem und aus Ihren Karten. Geschätzt ist nichts.')

# ---------- Rund um den Aufenthalt (rundum.py) ----------
import rundum as _ru  # noqa: E402
if _ru.RUNDUM:
    EIGENE.append(_ru.EINTRAG); EIGENE_BILDER += _ru.BILDER; CSS += _ru.CSS
    FLAECHE['rundum'] = 'fl--papier tapete-hell'

# ---------- Handschrift als Tafel mit Bewegung (marke_werkbank.py) ----------
HANDSCHRIFT.update(marke_text='Ihr Medaillon ist von Ihrer Karte nachgezeichnet und bleibt deshalb in jeder Grösse scharf. Ihr Name steht in Versalien daneben, so wie auf Ihrer heutigen Seite.',
                   muster_etik='Ihre Butzenscheiben als Muster',
                   muster_text='Das Muster auf den dunklen Flächen sind die Butzenscheiben Ihrer Fensterreihe, Ton in Ton. Man findet es auf der neuen Seite wieder, in den Karten und auf jeder Drucksache.')
import marke_werkbank as _mw  # noqa: E402
EIGENE.append(_mw.abschnitt(globals())); EIGENE_BILDER += _mw.BILDER; CSS += _mw.CSS
FLAECHE['handschrift'] = 'fl--navy tapete'

# ---------- Studio: das echte Studio im Laptop zum Bedienen, darunter die fünf Filme und die Bereiche (studio_laptop.py) ----------
STUDIO.pop('bilder', None)    # die vier Standbilder fallen weg: im Laptop lässt sich jeder Bereich selbst öffnen
STUDIO.update(text='Zur Website gehört ein Studio. Dort ändern Sie Zimmerpreise, Karten, Öffnungszeit, Anlässe, Texte und Bilder selbst, so einfach wie eine Tafel neu zu beschriften.',
              filme_titel='Fünf Handgriffe im Film', bereiche_titel='Was Sie selbst pflegen',
              hinweis='Im Laptop und hinter «Studio im eigenen Fenster öffnen» liegt eine Probe-Fassung. Was Sie dort ändern, sehen nur Sie, auf der Seite ändert sich nichts. Nur eigene Fotos lassen sich dort noch nicht hochladen, «Aus dem Vorrat» geht. Zieht die Seite zu Ihnen, kommt das echte Studio mit, mit Ihrem eigenen Passwort.')
KAPITEL['studio'] = dict(text=STUDIO['text'])
import studio_laptop as _sl  # noqa: E402
if _sl.BEREIT:
    EIGENE.append(_sl.abschnitt(globals())); EIGENE_BILDER += _sl.BILDER; CSS += _sl.CSS
    FLAECHE['studio'] = 'fl--navy tapete'

# ---------- Rezeption im Chat: das 3D-Handy der Seite rezeption/ schwebt herein (rezeption_handy.py) ----------
REZEPTION[:] = [
    ('Antwortet sofort, auch spätabends', 'Unten rechts auf jeder Seite. Gäste fragen nach dem Fondue, dem Himmelbett oder dem Alter des Hauses, die Antwort kommt aus Ihren Seiten und Karten, auf Deutsch, Englisch und Französisch.'),
    ('Die Buchung liegt gleich im Gespräch', 'Sagt ein Gast, wann er kommen möchte, legt sie die Buchungsmaske ins Gespräch. «Zur Buchung» öffnet Ihr Buchungssystem mit seinen Daten, bezahlt wird dort wie bisher.'),
    ('Kennt das Wetter und den Weg hinauf', 'Die Vorhersage für Kandersteg, den Oeschinensee und den Gemmipass. Bei Regen schlägt sie die Stube vor, bei klarem Himmel den Weg in die Höhe.'),
    ('Schreibt Entwürfe für Anfragen', 'Aus der Mail eines Vereins oder einer Familie wird ein Entwurf im Ton des Hauses, mit Stuben und Preisen aus Ihren Karten. Verschickt wird erst, wenn jemand von Ihnen gelesen hat.'),
]
REZEPTION_TEXT = 'Unten rechts auf jeder Seite sitzt die Rezeption des Ruedihus als Gespräch. Am Handy sehen Sie, wie ein Gast nach dem Fondue fragt und die Buchung für zwei Nächte gleich im Gespräch liegt.'
KAPITEL['rezeption'] = dict(text=REZEPTION_TEXT)
import rezeption_handy as _rh  # noqa: E402
if _rh.BEREIT:
    EIGENE.append(_rh.abschnitt(globals())); CSS += _rh.CSS
    FLAECHE['rezeption'] = 'fl--papier tapete-hell'

# ---------- Mails: drei Fälle im Ton des Hauses (mails_reihe.py, Quelle mails/_src/bau.py) ----------
import mails_reihe as _mr  # noqa: E402
if _mr.BEREIT:
    EIGENE.append(_mr.EINTRAG); EIGENE_BILDER += _mr.BILDER; CSS += _mr.CSS
    FLAECHE['mails'] = 'fl--blau tapete-leicht'
    MEINS.append('Der Wortlaut der drei Mails (Vorschlag im Ton des Hauses, mit Beispielwerten)')

# ---------- Feed: Handy in der Mitte, Foto und Blatt ringsum (feed_buehne.py) ----------
FEED.update(text1='Oben steht einmal das Haus im Grünen, ein Bild über sechs Beiträge. Darunter trägt in jeder Reihe ein Foto den Namen seines Raums.',
            text2='Nur Fotos aus dem Haus, keine Grafiken. Heute zeigt sich das Ruedihus im Profil des Waldhotels Doldenhorn, so könnte ein eigenes aussehen.')
import feed_buehne as _fb  # noqa: E402
if _fb.BEREIT:
    EIGENE.append(_fb.abschnitt(globals())); EIGENE_BILDER += _fb.BILDER; CSS += _fb.CSS
    FLAECHE['feed'] = 'fl--nacht tapete-leicht'
FLAECHE.update(papier='fl--navy tapete', material='fl--papier tapete-hell')

# ---------- Fenster vor Studio und vor Ausblick, «Was noch dazukommt» als Tafel (fenster_ausblick.py) ----------
AUSBLICK['bild_alt'] = 'Türknauf und Butzenscheiben im Ruedihus'
import fenster_ausblick as _fa  # noqa: E402
EIGENE.append(_fa.ausblick_abschnitt(globals())); EIGENE_BILDER += _fa.BILDER; CSS += _fa.CSS
FLAECHE['dazu'] = 'fl--creme tapete-hell'

# ---------- Geprüft als Blatt wie ein Schpiszettel, daneben drei Fotos (geprueft_blatt.py) ----------
import datetime as _dt  # noqa: E402
GEPRUEFT_TRIO = [('z-himmelbett', 1.6, (.5, .42), 'Unter dem Himmelbett'), ('e-zopf', 1.6, (.5, .5), 'Am Morgen'), ('haus-winter', 1.6, (.5, .6), 'Im Winter')]
GEPRUEFT_PUNKTE = [
    ('Die Website', 'Am Handy und am Rechner geöffnet, in Safari- und Chrome-Technik, von der schmalsten bis zur breitesten Ansicht. Nichts läuft über, und auch auf einem schwachen Gerät bleibt das Scrollen flüssig.'),
    ('Die drei Karten', 'Schpiszettel, Schpis Charte und Tagesteller Zeile für Zeile gegen Ihre PDFs gelesen. 70 Tippfehler aus den Originalen sind berichtigt, jeder einzeln festgehalten.'),
    ('Das Studio', 'Durch jeden Bereich geklickt, vom Gericht anlegen bis zum Veröffentlichen und wieder zurück. Jede Änderung wartet als Entwurf, jeder Stand lässt sich zurückholen.'),
    ('Ihre Daten', 'Die Website setzt für Gäste keine Kekse. Die Rezeption im Chat nimmt weder Karten- noch Passdaten entgegen.'),
]
PRUEFDATUM = _dt.date(2026, 10, 12)   # Tag der Prüfung, fest: ein späterer Bau zieht ihn nicht mit (Stand der Werkbank im Auftakt und Fuss ist der Bautag)
STEMPEL_TEXT = f'GEPRÜFT · LANDGASTHOF RUEDIHUS · {PRUEFDATUM:%d.%m.%Y} ·'
KAPITEL['geprueft'] = dict(text='Bevor diese Werkbank zu Ihnen kommt, ist jedes Teil durchgegangen worden. Auf dem Blatt steht das Wichtigste, der Rest ohne Fachwörter auf einer eigenen Seite.')
GEPRUEFT_OFFEN = 'Offen bleibt, was nur Sie wissen: die Namen von vier Stuben-Fotos, das Königspaar und das Jahr des Bundesratsfotos, dazu die Preise aus dem Buchungssystem und Ihr Blick auf die Fotos.'
FLAECHE['geprueft'] = 'fl--navy tapete'
import geprueft_blatt as _gb  # noqa: E402
geprueft_abschnitt = _gb.abschnitt(globals())
CSS += _gb.CSS

# ---------- Vier Häuser, eine Startseite: das Gegenstück zur Vision (vision_familie.py) ----------
import vision_familie as _vf  # noqa: E402
if _vf.BEREIT:
    EIGENE.append(_vf.EINTRAG); EIGENE_BILDER += _vf.BILDER; CSS += _vf.CSS
    FLAECHE['vier'] = 'fl--blau tapete-leicht'

# ---------- Schluss in der Dämmerung, Laufband davor (schlussband.py) ----------
SCHLUSS.update(bild='haus-daemmerung')
KAPITEL['schluss'] = dict(text='Sagen Sie mir ruhig offen, was Ihnen gefällt und was nicht. Ändern lässt sich alles, und über jede Rückmeldung freue ich mich.')
import schlussband as _sb  # noqa: E402
CSS += _sb.CSS

# ---------- Fuss «Alles auf einen Blick» als Fächer mit den eigenen Stücken des Hauses (fuss_faecher.py, objekte_bau.py) ----------
import fuss_faecher as _ff  # noqa: E402
if _ff.BEREIT:
    wege_abschnitt = _ff.abschnitt
    CSS += _ff.CSS

# ---------- Kleinigkeiten: Wahl-Knöpfe mittig unter den mittigen Köpfen, dreizehn Bereiche ohne halb leere Reihe, Farbnamen ganz ----------
CSS += '''
@media(min-width:760px){.vh-wahl,#seiten .wahl{justify-content:center}}
.vh-wahl{justify-content:center}
@media(max-width:700px){.schluss__b{object-position:10% 50%}}
/* lange Knöpfe brechen am Handy um, statt den Pfeil-Knauf aus dem Bild zu schieben */
@media(max-width:480px){.kn{max-width:100%;height:auto;min-height:54px;padding-top:9px;padding-bottom:9px;white-space:normal;line-height:1.35;text-align:left}.kn i{flex:none}.kn-reihe{max-width:100%}}
@media(min-width:1100px){
  .stl .bereiche{grid-template-columns:repeat(20,minmax(0,1fr))}
  .stl .bereiche li{grid-column:span 4}
  .stl .bereiche li:nth-child(n+6){grid-column:span 5}
}
@media(min-width:560px) and (max-width:1099px){.stl .bereiche{grid-template-columns:repeat(2,minmax(0,1fr))}.stl .bereiche li:last-child{grid-column:1/-1}}
'''

# ---------- Brett «Wie alles zusammenhängt» Kachel für Kachel, Bilder in den Bändern gleiten unter der Maus ----------
CSS += '''
@media (hover:hover){
  .gf .idee .idee__b img,#ideen .idee .idee__b img{transform-origin:50% 22%;transition:transform 2.2s cubic-bezier(.16,1,.3,1)}
  .gf .idee.da:hover .idee__b img,#ideen .idee.da:hover .idee__b img{transform:scale(1.06);transition-duration:2.8s}
}
@media (prefers-reduced-motion:reduce){.idee .idee__b img{transition:none;transform:none!important}}
.brett.warm .bn,.brett.warm .bs{will-change:transform,opacity}
#gefuege .bn{transition:opacity .9s cubic-bezier(.16,1,.3,1),transform 1.25s cubic-bezier(.16,1,.3,1)}
#gefuege .brett.vor .bn{opacity:0;transform:translate(-50%,30px)}
#gefuege .bs{transition:opacity .9s cubic-bezier(.16,1,.3,1)}
'''


# Brett «Wie alles zusammenhängt» am Handy (Fund des Gasterntal-Chats, 12.10.2026, hier nachgemessen: bei 320 bis 390 px blieben 0 von 22 Kacheln sichtbar):
# das Kit baut das Brett erst auf, wenn 30 % von ihm im Bild sind; am Handy ist es breiter als der Bildschirm und kommt nie so weit.
# Ein eigener Beobachter stösst den Aufbau an, sobald das Brett ins Bild kommt und noch wartet. Das Kit bleibt unverändert.
BRETT_HILFE = """<script id="brett-hilfe">(function(){var b=document.getElementById('brett'),k=document.getElementById('brett-noch');if(!b||!k||!('IntersectionObserver' in window))return;
new IntersectionObserver(function(E,o){if(!E[0].isIntersecting)return;o.disconnect();setTimeout(function(){if(/\\bvor\\b/.test(b.className))k.click()},700)},{rootMargin:'0px 0px -35% 0px'}).observe(b)})();</script>
"""
CSS += '''
/* Schluss: das Haus leuchtet in der Dämmerung, ein weicher Schatten nur hinter den Buchstaben hält die Schrift lesbar */
.schluss .zt,.schluss .lauf p,.schluss .gruss-u,.schluss .kap span{text-shadow:0 1px 2px rgba(15,8,3,.9),0 2px 16px rgba(15,8,3,.8),0 0 42px rgba(15,8,3,.55)}
/* Hinweis unter dem Studio: der Abschnitt ist hier dunkel, die Kit-Regel setzt dunkle Schrift */
#studio.stl .hinweis{color:rgba(251,245,234,.8);border-top-color:rgba(201,133,67,.24)}
'''


def nach_bau():
    """Nach jedem Bau der Werkbank: Eigenes nach werkbank/eigen (der Bau räumt nur img/ auf), dann die gebaute Seite nacharbeiten."""
    import re as _re, shutil as _sh
    from PIL import Image as _I
    q, z = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen'), os.path.join(_WB, 'eigen')
    os.makedirs(z, exist_ok=True)
    sig = _I.open(os.path.join(q, 'unterschrift-robert.webp')).convert('RGBA')   # Roberts Unterschrift, in der Tinte dieses Hauses
    r, g, b = (int(FARBEN['tinte'][i:i + 2], 16) for i in (1, 3, 5))
    _I.merge('RGBA', (*_I.new('RGB', sig.size, (r, g, b)).split(), sig.getchannel('A'))).save(os.path.join(z, 'unterschrift.webp'), 'WEBP', quality=90)
    _sh.copy2(os.path.join(q, 'rezeption3d.js'), os.path.join(z, 'rezeption3d.js'))   # Start-Skript des 3D-Handys, eigene Kopie der Werkbank
    _fb.bilder()                                                                       # acht Beiträge für die Polaroids
    _ff.bilder()                                                                       # Objekte für den Fuss
    seite = os.path.join(_WB, 'index.html')
    t = open(seite, encoding='utf-8').read()
    t = t.replace('Links Ihre Seite, wie sie heute ist, rechts der Entwurf. Schieben Sie den Griff hin und her, daneben steht, was neu ist.', VERGLEICH_TEXT)
    if 'id="brett-hilfe"' not in t:
        t = t.replace('</body>', BRETT_HILFE + '</body>', 1)
    open(seite, 'w', encoding='utf-8').write(t)
    _ak.anwenden(seite)   # Auftakt: Kacheln statt Polaroids
    _mw.anwenden(seite)   # Handschrift: Auftritte in der Tafel
    _fa.anwenden(seite)   # Fenster vor Studio und vor Ausblick
    _sb.anwenden(seite)   # Laufband zwischen Schluss und Fuss
    _km.anwenden(seite)   # Abschnittsköpfe: Medaillon statt Zahl, mittig (zuletzt, damit es jeden Kopf trifft)
    import fluss_werkbank as _fw
    _fw.anwenden(seite)   # Flüssigkeit: kleinere Bildstufen, Vorher/Nachher lazy

KAPITEL['unterlagen'] = dict(text='Der Schpiszettel der Chäs- und Wystube, die Schpis Charte der Egger- und Stettlerstube, die Tagesteller und das Heft mit den Menuvorschlägen für Feste: alle vier als Idee im Stil der neuen Seite, mit Ihren Gerichten und Ihren Preisen. Das Heft ist von 2023, an seinen Preisen habe ich nichts geändert. Legen Sie jede Unterlage neben Ihre heutige Fassung und blättern Sie durch.')


# ================================================================ Ein Empfänger (Robert 12.10.2026 abends): die Familie bekommt die Übersicht und alle vier Werkbänke zusammen.
# Vorstellung, Anlass, Angebot und die Bitte um ein Gespräch stehen einmal auf der Übersicht («Familie Maeder — Vier Häuser»). Hier nur noch, was dieses Haus betrifft.
BRIEF['absaetze'][-1] = ('Für die Stuben sind Anhänger mit den Namen Ihrer Zimmer entstanden, eine Banderole für die Serviette und Etiketten für die Zündhölzer. '
                         'Und für Instagram ein Feed, in dem Foto und Blatt wechseln. Ich hoffe, Sie erkennen Ihr Haus in allem wieder.')
BRIEF['schluss'] = ''
KAPITEL['schluss'] = dict(text='Sagen Sie mir ruhig offen, was Ihnen am Ruedihus gefällt und was nicht. Ändern lässt sich alles.')
AUSBLICK.update(
    gross=('Der nächste Schritt', 'Die Anleitung', 'Wie jeder Handgriff im Studio geht, steht bald in einer Anleitung: jeder Schritt mit Bild, die wichtigsten als kurzer Film. Sie kommt als Nächstes. Dann bekommt das Studio auch seinen festen Platz bei Ihnen, und was Sie ändern, bleibt. Bis dahin ist die Probe zum Ausprobieren da.'),
    punkte=[AUSBLICK['punkte'][0],
            ('Preise aus dem Buchungssystem', 'Den Preis des Tages und die freien Zimmer holt die Seite aus Ihrem SimpleBooking. Online lässt SimpleBooking solche Abfragen erst zu, wenn das Haus dort einen Zugang bestellt. Bis dahin stehen im Zimmer-Finder Ihre Ab-Preise, die Rezeption im Chat führt zur Buchung, und der Preisvergleich mit den Portalen zeigt ein beschriftetes Beispiel.'),
            ] + AUSBLICK['punkte'][2:])


# ================================================================ Werkbank-Chat 17.10.2026: acht Kapitel wie die Werkbank des Carlton-Europe (wb_kapitel.py)
# Weg über das Waldhotel Doldenhorn (Kit-Haus, dort wb_kapitel.py, nur gelesen und kopiert), Kleid und Worte des Ruedihus. Kundentexte vom 17.10.2026
# (Familie Maeder — Vier Häuser/bau.py): Robert genau einmal vorgestellt, Warum vor dem Was, Leitsatz wörtlich, Absender nur «Robert Reff, Hamburg»,
# kein Koh Phangan, kein Siargao, keine Kurslinie, kein Portfolio-Satz, kein Instagram; für das Haus heisst es «Alles auf einen Blick» und «Dateien».
# Das Studio heisst jetzt «Der Schreibtisch» und ist eines der sieben Werkzeuge (Welt Landhaus, _Werkzeuge/stamm/welt.js).
SEITEN[:] = [   # alle 13 Seiten und das Rechtliche, die ein Gast als Seite wahrnimmt (Abgleich 17.10.2026; Sätze nur aus dem, was auf der Seite steht)
    ('index.html', 'Startseite', 7, 'Das Haus im ersten Bild, die Dependance mit ihren Fotos, «Was führt Sie zu uns?», die Zimmer, die Stuben, die Novembernacht und was die Gäste sagen.', ''),
    ('zimmer.html', 'Zimmer', 5, 'Landhaus, Hochzeitsstube, Liebeslaube und Hymmelrich, was zu jedem Zimmer gehört und die Geschenkgutscheine.', ''),
    ('zimmer-landhaus.html', 'Landhaus', 3, 'Das Zimmer Landhaus mit allen Fotos, dem Blick auf Tal und Berge und den anderen Zimmern zum Vergleich.', ''),
    ('zimmer-hochzeitsstube.html', 'Hochzeitsstube', 3, 'Die Hochzeitsstube mit Himmelbett, allen Fotos und der Buchung.', ''),
    ('zimmer-liebeslaube.html', 'Liebeslaube', 3, 'Die Liebeslaube mit Himmelbett, allen Fotos und der Buchung.', ''),
    ('zimmer-hymmelrich.html', 'Hymmelrich', 3, 'Das Hymmelrich, ein eigenes kleines Holzhaus, mit allen Fotos und der Buchung.', ''),
    ('zu-zweit.html', 'Zu zweit', 4, 'Zwei Zimmer mit Himmelbett, ein Haus für sich, ein Abend in der Stube und der Nachmittag im Wasser.', ''),
    ('essen.html', 'Essen', 6, 'Fünf Stuben auf zwei Stockwerken, drei Karten ab 1.3.2026, woher es kommt, und welche Stube für Ihr Fest.', ''),
    ('veranstaltungen.html', 'Durchs Jahr', 4, 'Der Jahreslauf von der Kuttel-Woche bis Sylvester, jeder Anlass mit seinem Menu, und Ihr eigenes Fest.', ''),
    ('geschichte.html', 'Geschichte', 4, 'Seit 1753: die Maultiere über die Gemmi, «Ds rich Ruedi», der Brand von 1908 und wer hier schon zu Gast war.', ''),
    ('haus.html', 'Das Haus', 6, 'Ihre Gastgeber, der Garten, das Spa im Nachbarhaus, Kandersteg, Anreise und Kontakt und die offenen Stellen.', ''),
    ('anreise.html', 'Vor Ihrer Anreise', 3, 'Die Seite für gebuchte Gäste: Ihr Aufenthalt, ein Tisch in der Stube und ein Termin im Spa.', ''),
    ('abreise.html', 'Abreise', 3, 'Zug und Bus ab Kandersteg, der letzte Morgen und ein Wort an die Rezeption.', ''),
    ('rechtliches.html', 'Rechtliches', 1, 'Angaben des Hauses, Bildnachweis, Daten und der KI-Assistent der Rezeption.', 'recht'),
]
LANG.update({'Durchs Jahr': 'Durchs Jahr im Ruedihus', 'Geschichte': 'Geschichte seit 1753', 'Zu zweit': 'Zu zweit im Ruedihus'})
KURZNAME.update({'Vor Ihrer Anreise': 'Anreise', 'Hochzeitsstube': 'Hochzeit', 'Durchs Jahr': 'Jahr'})

AUFTAKT.update(text='Für den Landgasthof Ruedihus liegt hier eine neue Website als Entwurf auf dem Tisch. Daneben Ihre Karten im selben Stil, sieben Werkzeuge für Ihr Team, '
                    'eine Rezeption im Chat und einiges für die Stuben. Nehmen Sie Platz.')

BRIEF.update(
    absaetze=[
        'Ein Holzhaus von 1753 mit bemaltem Giebel und Butzenscheiben, fünf Stuben auf zwei Stockwerken und eine Karte, auf der steht, was man bei Ihnen vergebens sucht. Erfinden könnte man das nicht. Genau das soll man auf der neuen Seite spüren.',
        'Das Ruedihus ist das kleinere der beiden Häuser in Kandersteg, mit zwölf Zimmern. Wer hier schläft, bucht kein Zimmer, sondern ein bestimmtes: die Hochzeitsstube, die Liebeslaube oder das Hymmelrich.',   # Robert 18.10.2026 23:31 «text passt» (Wortlaut über Oberchef)
        'Genau dorthin soll die neue Seite führen. Wer das Ruedihus auf einem Portal findet, sieht hier die Stuben, wie sie sind, und bucht direkt bei Ihnen, weiter über Ihr SimpleBooking.',
        'Unten folgt alles der Reihe nach: was mir auf Ihrer heutigen Seite aufgefallen ist, der Entwurf, Ihre Karten und Werkzeuge und am Schluss mein Vorschlag. Die Werkzeuge lassen sich gleich hier ausprobieren.'],
    schluss='<q>Hospitality braucht nicht noch eine Webdesign-Agentur. Hotels brauchen jemanden, der Marke, Website, Gast, Betrieb und Technologie als ein zusammenhängendes System versteht.</q>',
    ort='Tasty Studios')

GEPRUEFT_PUNKTE[:] = [
    ('Die Website', 'Alle dreizehn Seiten und das Rechtliche am Handy und am Rechner geöffnet, in der Technik von Safari und von Chrome, bis unten gefahren. Nichts läuft über, und auch auf einem schwachen Gerät bleibt das Scrollen flüssig.'),
    ('Die Karten', 'Schpiszettel, Schpis Charte, Tagesteller und das Heft mit den Menuvorschlägen Zeile für Zeile gegen Ihre PDFs gelesen. Jeder berichtigte Tippfehler ist einzeln festgehalten.'),
    ('Die Werkzeuge', 'Alle sieben Werkzeuge wurden einzeln gebaut und Knopf für Knopf ausprobiert, nur mit erfundenen Daten. Von sich aus verschickt keines etwas.'),
    ('Ihre Daten', 'Die Website setzt für Gäste keine Kekse. Anfragen kommen über Fenster auf der Seite bei Ihrem Team an, nichts öffnet ein Mailprogramm. Die Rezeption im Chat nimmt weder Karten- noch Passdaten entgegen.'),
]
GEPRUEFT[:] = [
    ('Die Website', 'seite', ['Alle dreizehn Seiten und das Rechtliche am Handy und am Rechner, in Safari- und Chrome-Technik: nichts läuft seitlich über, kein Skriptfehler.',
                              'Flüssigkeit gebremst gemessen, wie auf einem schwachen Gerät.',
                              'Buchung, Frage-Karten, Galerie, Bühne je Zimmer, Karten, Film, Anfrage-Fenster und Menü am Handy durchgeklickt.',
                              'Jedes Foto kommt in der Reihenfolge, in der man es sieht; hinter jedem Bild seine Farbe statt Schwarz.']),
    ('Die Karten', 'karte', ['Schpiszettel, Schpis Charte und Tagesteller Zeile für Zeile gegen Ihre PDFs gelesen, Wort für Wort geprüft.',
                             'Das Heft mit den Menuvorschlägen von 2023 Wort für Wort und Preis für Preis gegen Ihr PDF gelesen.',
                             'Jeder berichtigte Tippfehler aus den Originalen ist einzeln festgehalten, damit Sie nachsehen können.',
                             'Was das Haus klären muss, steht gesondert: zwei Gutschein-Preise, die sich widersprechen, ein fehlender vierter Tagesteller, zwei Telefonnummern.']),
    ('Die Werkzeuge', 'schloss', ['Die Stube und sechs Werkzeuge, jedes in einem eigenen Durchgang gebaut und Knopf für Knopf bedient, mit Probe-Daten.',
                                  'Die Tafel: 134 von 134 Schritten in drei Browsern und vier Grössen; Die Werkstatt: alle 256 Vorlagen als druckfertige PDF, ohne Befund.',
                                  'Der Gastgeber: 68 von 68 Funktionen bedient, der Chat nur mit Probe-Antworten, ohne Kosten; Antworten an Gäste bleiben als Brief im Werkzeug.',
                                  'Kein Werkzeug verschickt etwas von selbst, keines öffnet ein Mailprogramm.']),
]
GEPRUEFT_OFFEN = 'Und was ehrlich offen bleibt: die Namen von vier Stuben-Fotos, das Königspaar und das Jahr des Bundesratsfotos, die Preise aus dem Buchungssystem online, Ihr Blick auf die Fotos, Ihre Angaben für Impressum und Datenschutz und die Passwörter für die Werkzeuge.'
GEPRUEFT_EIN = 'Bevor Sie etwas zu sehen bekommen, ist es durchgegangen worden: die Website auf jedem Gerät, die Karten Wort für Wort, jedes Werkzeug Knopf für Knopf, der Umgang mit den Daten Ihrer Gäste. Hier steht, was genau, ohne Fachwörter. Was offen bleibt, steht auch da.'
GEPRUEFT_NAV = ['Website', 'Karten', 'Werkzeuge', 'Daten', 'Diese Seite', 'Offen']
_GM = {g[0]: i for i, g in enumerate(GEPRUEFT_MEHR)}
_w = GEPRUEFT_MEHR[_GM['Die Website']]
GEPRUEFT_MEHR[_GM['Die Website']] = (_w[0], _w[1], 'Dreizehn Seiten von der Startseite bis zur Abreise, dazu das Rechtliche mit Bildnachweis.', [
    'Am Handy und am Rechner, von der schmalsten bis zur breitesten Ansicht, in Safari- und Chrome-Technik: nichts läuft seitlich über, kein Skriptfehler.',
    'Flüssigkeit gebremst gemessen, wie auf einem schwachen Gerät. Der Film im Zimmer startet erst auf Tastendruck, damit nichts anderes ins Stocken kommt.',
    'Buchung, Frage-Karten, Galerie, Bühne je Zimmer, Karten, Film, Anfrage-Fenster und Menü am Handy durchgeklickt, ohne Fehler.'] + _w[3][3:])
_k = GEPRUEFT_MEHR[_GM['Die drei Karten']]
GEPRUEFT_MEHR[_GM['Die drei Karten']] = ('Die Karten', _k[1], 'Schpiszettel, Schpis Charte, Tagesteller und das Heft mit den Menuvorschlägen, neu gesetzt im Stil der Seite.', _k[3])
GEPRUEFT_MEHR[_GM['Das Studio']] = ('Die sieben Werkzeuge', 'schloss', 'Die Stube und sechs Werkzeuge, mit denen Ihr Team die Seite selbst führt. Jedes wurde in einem eigenen Durchgang gebaut und Knopf für Knopf bedient, mit Probe-Daten, nie mit Ihren echten.', [
    'Die Stube: 38 Zeilen der Funktionsliste bedient, in Chrome, Safari-Technik und Firefox bei vier Grössen vom Handy bis zum Rechner.',
    'Der Schreibtisch: Speichern, Veröffentlichen und Zurückholen an einer Probe-Kopie der Seite; die Probe-Fassung online in 20 von 20 Schritten nachgestellt.',
    'Die Tafel: vier Karten aus dem Satz Ihrer Unterlagen eingelesen und Wort für Wort gegen die Website geprüft; 134 von 134 Schritten in drei Browsern und vier Grössen.',
    'Der Gastgeber: 68 von 68 Funktionen bedient, in Chrome und Safari-Technik, am Rechner und am Handy. Der Chat lief nur mit Probe-Antworten, ohne Kosten.',
    'Das Hausbuch: 92 von 92 Zeilen bedient; alle 62 Fotos in vier Grössen gegen ihre Quelle geprüft, ohne Abweichung.',
    'Das Besucherbuch: in drei Browsern und vier Grössen bedient, jede Zahl im Werkzeug nachgerechnet. Gezeigt werden Beispielwerte.',
    'Die Werkstatt: alle 256 Vorlagen über den echten Knopf als druckfertige PDF ausgegeben, ohne Befund.',
    'Kein Werkzeug verschickt etwas von selbst und keines öffnet ein Mailprogramm: Antworten an Gäste bleiben als Brief im Werkzeug, zum Speichern als PDF oder zum Kopieren.'])
_d = GEPRUEFT_MEHR[_GM['Ihre Daten und die Ihrer Gäste']]
GEPRUEFT_MEHR[_GM['Ihre Daten und die Ihrer Gäste']] = (_d[0], _d[1], _d[2], [
    'Die Website setzt für Gäste keine Kekse. Im Entwurf zählt die Seite keine Besuche; Das Besucherbuch zeigt Beispielwerte.',
    'Anfragen für Tisch, Fest, Gutschein, Anreise und Abreise schickt der Gast über ein Fenster auf der Seite; sie kommen im Gastgeber bei der zuständigen Abteilung an. Nichts öffnet ein Mailprogramm.'] + _d[3][1:])
_o = GEPRUEFT_MEHR[_GM['Was ehrlich offen bleibt']]
GEPRUEFT_MEHR[_GM['Was ehrlich offen bleibt']] = (_o[0], _o[1], _o[2], _o[3] + [
    'Die Werkzeuge stehen im Entwurf ohne Passwort. Vor der Übergabe bekommt jede Person ihr eigenes.'])
GEPRUEFT_MEHR.insert(len(GEPRUEFT_MEHR) - 1, ('Diese Seite', 'seite', 'Die Seite «Alles auf einen Blick» mit allem, was dazugehört.', [
    'Am 17. Oktober 2026 nach dem Umbau in Kapitel in der Technik von Safari und von Chrome geöffnet, am Rechner und am Handy, und bis unten gefahren: nichts läuft seitlich über, kein Bild fehlt.',
    'Jeder Verweis und jeder Knopf führt an sein Ziel; im Laptop lässt sich jedes der sieben Werkzeuge öffnen.',
    'Die Mails nennen nur, was in Ihren Unterlagen steht; die Gäste, Daten und Beträge darin sind erfunden.']))
PRUEFDATUM = _dt.date(2026, 10, 17)
STEMPEL_TEXT = f'GEPRÜFT · LANDGASTHOF RUEDIHUS · {PRUEFDATUM:%d.%m.%Y} ·'
KAPITEL['geprueft'] = dict(text='Bevor Sie etwas davon sehen, ist jedes Teil durchgegangen worden: die Website auf jedem Gerät, die Karten Wort für Wort, jedes Werkzeug Knopf für Knopf, der Umgang mit den Daten Ihrer Gäste. Auf dem Blatt steht das Wichtigste, der Rest auf einer eigenen Seite.')
KAPITEL['gefuege'] = dict(text='Ein Blick hinter die Seiten: links, was von Ihnen kommt, in der Mitte, was daraus geworden ist, rechts die Seiten und was im Hintergrund mitläuft. Eine Kachel antippen oder den Rundgang starten, beides zeigt den Weg.')
REZEPTION_TEXT = ('Wer abends noch wissen will, ob es in der Stube Fondue gibt oder wie alt das Haus ist, fragt einfach unten rechts auf der Seite. Am Handy sehen Sie so ein Gespräch; '
                  'die Antwort kommt aus Ihren Seiten und Karten, auch wenn im Haus längst Ruhe ist. Was Gäste fragen, liest Ihr Team im Gastgeber nach.')
KAPITEL['rezeption'] = dict(text=REZEPTION_TEXT)
GAESTE = [(g[0], g[1], g[2].replace('Die Anfrage kommt bei Ihnen an.', 'Die Anfrage kommt bei Ihrem Team im Gastgeber an, ohne Mailprogramm.'), *g[3:]) for g in GAESTE]

_gefuege4 = gefuege


def gefuege(z):   # noqa: F811  Abgleich 17.10.2026: Anfragen gehen ins Werkzeug, das Studio heisst Der Schreibtisch, «Material» heisst für das Haus nicht so
    d = _gefuege4(z)
    d['fuss'] = 'Folgen Sie einer Linie: Sie führt von dem, was von Ihnen kommt, zur Seite'
    if 'start' in d and isinstance(d['start'], list) and len(d['start']) > 2:
        d['start'] = [d['start'][0], 'Von Ihnen zur Seite', d['start'][2].replace('vom Material', 'von dem, was von Ihnen kommt,').replace('von Ihrem Material', 'von dem, was von Ihnen kommt,')]
    for n in d['n']:
        if n[0] == 'anfragen':
            n[3], n[4], n[6] = 'Anfragen', 'in den Gastgeber', 'Anfragen'
            n[7] = 'Tisch, Fest, Gutschein, Anreise und Abreise fragt der Gast über ein Fenster auf der Seite an. Die Anfrage kommt im Gastgeber bei der zuständigen Abteilung an, nie als Mail.'
        if n[0] == 'studio':
            n[3], n[4], n[6] = 'Der Schreibtisch', 'und sechs Werkzeuge', 'Der Schreibtisch'
            n[7] = 'Das Werkzeug zur Seite, eines von sieben. Dort ändert Ihr Team Zimmer, Zeiten, Anlässe, Texte und Bilder selbst; die Karten pflegt es in der Tafel. Jede Änderung wartet als Entwurf, bis Sie sie veröffentlichen.'
            if len(n) > 8:
                n[8] = ['Zimmer', 'Zeiten', 'Anlässe', 'Texte und Bilder']
        if n[0] == 'zimmer':
            n[7] = 'Landhaus, Hochzeitsstube, Liebeslaube und Hymmelrich, jedes mit eigener Seite, mit Fotos, Preis und Buchung; dazu die Seite «Zu zweit».'
        if n[0] == 'essen':
            n[7] = 'Fünf Stuben, drei Karten, die Herkunft der Produkte; dazu die Seite «Durchs Jahr» mit allen Anlässen.'
        if n[0] == 'haus':
            n[7] = 'Gastgeber, Garten, Spa im Nachbarhaus, Anreise und Stellen; dazu die Geschichte seit 1753, «Vor Ihrer Anreise» und die Abreise.'
    return d


_nach_bau_alt = nach_bau


def nach_bau():   # noqa: F811
    """Kit-Bau → bisherige Nacharbeit → Kapitel (wb_kapitel). wb_kapitel erst hier laden (Kreis mit kern beim Import)."""
    _nach_bau_alt()
    import shutil as _sh2
    for _n in ('rezeption-werkbank.mp4', 'rezeption-werkbank-m.mp4', 'rezeption-werkbank-start.webp', 'rezeption-fondue-start.webp'):   # eigener Handy-Film der Werkbank (rh_film.js), nicht der der Seite rezeption/
        _sh2.copy2(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen', _n), os.path.join(_WB, 'eigen', _n))
    import wb_kapitel as _kp
    _kp.anwenden(os.path.join(_WB, 'index.html'))
    # Die Filme des früheren Studios (werkbank/film, 18 MB) zeigt die Werkbank in Kapiteln nicht mehr; ohne Verweis gehen sie nicht mit online
    import glob as _gl
    _fd = os.path.join(_WB, 'film')
    if os.path.isdir(_fd) and not any('film/' in open(_p, encoding='utf-8').read() for _p in _gl.glob(os.path.join(_WB, '**', '*.html'), recursive=True) + _gl.glob(os.path.join(_WB, '*.js')) + _gl.glob(os.path.join(_WB, '*.css'))):
        _sh2.rmtree(_fd)

# ---------- Abgleich mit den heutigen Seiten (Regel 8, Werkbank-Chat 17.10.2026): Ideen und Vergleich nach dem Stand der Website von heute ----------
# Aufnahmen: node _werkbank/rh_ideen.js (ersetzt ideen.js), node _werkbank/vorher.js. Jeder Satz nur aus dem, was auf der Aufnahme zu sehen ist.
IDEEN[:] = [
    ('Rechner/Startseite', 'Das Haus im ersten Bild', 'Ihr Haus unter den Bäumen steht gross im ersten Bild, daneben der Satz «1753 gebaut. Heute Abend Ihr Tisch, heute Nacht Ihr Bett.» und gleich darunter die Buchung.', '50% 50%'),
    ('Ideen/frage', '«Was führt Sie zu uns?»', 'Ein grosses Bild, unten links in der Kerbe die Antwort mit Satz und Preis; darunter wählt der Gast zwischen einer Nacht, einem Znacht, zu zweit oder einem Fest.', '50% 50%'),
    ('Ideen/zimmer', 'Vier Zimmer, zwei Spalten', 'Liebeslaube, Landhaus, Hochzeitsstube und Hymmelrich stehen auf der Startseite in zwei Spalten, jedes Foto im Goldrahmen, mit Name, Belegung und Preis.', '50% 40%'),
    ('Ideen/sockel', 'Jedes Zimmer mit eigener Seite', 'Das Zimmer gross, daneben Ihr Satz, darunter Preis, Belegung und Frühstück und der Knopf zur Buchung.', '50% 50%'),
    ('Ideen/stuben', 'Fünf Stuben, zwei Stockwerke', 'Unten im Parterre Chäs-u Wystube, Jungestube und Ofestübli, eine Treppe höher Egger- und Stettlerstube, jede mit ihren Plätzen.', '50% 50%'),
    ('Ideen/grundsatz', 'Ihr Grundsatz, gross', 'Der Satz aus Ihrer Karte, was man bei Ihnen vergebens sucht, steht als Fenster mitten auf der Seite «Essen».', '50% 50%'),
    ('Ideen/jahr', 'Der Jahreslauf', 'Auf «Durchs Jahr» steht die lange Stube gross, in der Kerbe Ihr Satz zu den Daten, darunter die sechs Anlässe von der Kuttel-Woche bis Sylvester.', '50% 50%'),
    ('Ideen/menu', 'Das Menu als kleine Karte', 'Weihnachten und Sylvester mit ihrer Menukarte im Goldrahmen, daneben drei Bilder des Hauses.', '50% 50%'),
    ('Ideen/noten', 'So sehen es die Gäste', 'Ihre Noten bei Booking.com und Google stehen als zwei Karten nebeneinander, mit Lage, Personal, Sauberkeit und Komfort.', '50% 50%'),
    ('Ideen/stellen', 'Offene Stellen im Fenster', 'Eine Stelle antippen, die Ausschreibung öffnet sich mittig im Fenster, mit Aufgaben, Anforderungen und dem, was die Bewerber erwartet.', '50% 50%'),
    ('Ideen/bewerben', 'Bewerben in einem kleinen Fenster', '«Jetzt bewerben» öffnet ein kleines Fenster, die Stelle steht schon drin. Name, E-Mail oder Telefon und ein paar Zeilen, dann geht die Bewerbung direkt ab, ohne Mailprogramm.', '50% 50%'),
    ('Ideen/warum', 'Was Bewerber über das Ruedihus wissen wollen', 'Als Idee: Bevor sich jemand bewirbt, will er wissen, wie es sich hier arbeitet und lebt. Vor den Stellen stehen deshalb das Haus von 1753, das Team der drei Häuser und Kandersteg vor der Tür, dazu drei Felder für Wohnen, Dienste und freie Tage, die die Familie Maeder füllt.', '50% 50%'),
]
KAPITEL['ideen'] = dict(text='Zu jeder Stelle der Seite gibt es einen Grund. Zwölf davon stehen hier, aufgenommen auf der Seite, wie sie heute aussieht.')
VORHER[:] = [
    ('startseite', 'Startseite', 'Das Haus zuerst, die Buchung gleich darunter.',
     ['Ihr Haus unter den Bäumen steht gross im ersten Bild, daneben der Satz «1753 gebaut. Heute Abend Ihr Tisch, heute Nacht Ihr Bett.»',
      'Anreise, Abreise und Gäste wählt man gleich unter dem Bild. Gebucht wird wie bisher in Ihrem SimpleBooking.',
      'Danach die Dependance mit ihren Fotos, «Was führt Sie zu uns?», die Zimmer, die Stuben und die Novembernacht, jede mit eigenen Fotos.'], 'index.html'),
    ('zimmer', 'Zimmer', 'Vier Arten zu wohnen, jede für sich.',
     ['Landhaus, Hochzeitsstube, Liebeslaube und Hymmelrich stehen mit Foto, Ihrem Satz und dem Preis da.',
      'Jedes Zimmer hat seine eigene Seite mit seinen Fotos, dem Preis und der Buchung.',
      'Was zum Zimmer gehört und die Geschenkgutscheine stehen gleich auf derselben Seite.'], 'zimmer.html'),
    ('essen', 'Essen', 'Fünf Stuben und drei Karten auf einer Seite.',
     ['Unten das Parterre mit Chäs-u Wystube, Jungestube und Ofestübli, eine Treppe höher die Egger- und Stettlerstube.',
      'Ihre drei Karten stehen mit jedem Gericht und Preis auf der Seite, ab 1.3.2026.',
      'Der Fest-Rechner «Welche Stube für Ihr Fest?» nennt zu Gästen und Menu die passende Stube und einen ersten Richtpreis.'], 'essen.html'),
    # Robert 18.10.2026 18:39: «warum haben Durchs Jahr und Das Haus kein Fenster dort?»
    ('jahr', 'Durchs Jahr', 'Was in den Stuben gekocht, gespielt und gefeiert wird.',
     ['Heute meldet die Events-Seite, dass es keine bevorstehenden Veranstaltungen gibt. Neu steht der Jahreslauf des Hauses da.',
      'Kuttel-Woche, Metzgete, Ruedi-Tag, Weihnachten, die Altjahr-Ländler-Stubete und Sylvester, jeder Anlass mit seinem Menu.',
      'Zu jedem Anlass fragt ein Knopf direkt einen Tisch an, darunter «Ihr eigenes Fest.»'], 'veranstaltungen.html'),
    ('haus', 'Das Haus', 'Ein Haus von 1753, auf einer eigenen Seite.',
     ['Heute steht das Haus in einem Absatz auf der Seite «Ruedihus». Neu hat es eine eigene Seite, mit Adresse und Swiss Historic Hotels gleich im ersten Bild.',
      'Ihre Gastgeber, der Garten, das Spa im Nachbarhaus und die Ausflüge rund um Kandersteg.',
      'Anreise und Kontakt, die Stimmen der Gäste und die offenen Stellen.'], 'haus.html'),
]
GAESTE = [g for g in GAESTE if g[0] != 'besuche']   # die Besuche zeigt jetzt Das Besucherbuch im Kapitel Werkzeuge, nicht mehr das Studio


# ---------- Eigene Ansprache (Werkbank-Regel 14, Robert 17.10.2026 ~20:00 und ~20:50; vier Werkbänke gehen an dieselbe Familie) ----------
# Anrede, Auftakt, Brief (oben, ohne Roberts Vorstellung: die steht im Brief der Einstiegsseite und beim Carlton), Überschriften und Schluss
# eigen fürs Ruedihus, gegen Carlton, Doldenhorn und Gasterntal gelegt (Prüfung in UEBERGABE.md). Leitsatz, Unterschrift und Bedienwörter bleiben.
ANREDE = 'Grüessech, Familie Maeder'
AUFTAKT['titel'] = ['Butzenscheiben,', 'frisch geputzt.']
AUFTAKT.update(text='Fünf Stuben, vier Zimmerarten und ein Giebel von 1753: Für den Landgasthof Ruedihus liegt hier die neue Website als Entwurf, '
                    'und um sie herum die Karten, sieben Werkzeuge für Ihr Team und einiges für die Stuben.')
TITEL_NEU = {   # alte Zeilen → neue Zeilen (wb_kapitel.eigene_titel setzt sie nach dem Bau ein)
    ('Schön, dass Sie', 'hereinschauen.'): ('Die Tür', 'steht offen.'),
    ('Was Sie hier', 'finden.'): ('Von Stube', 'zu Stube.'),
    ('Ihr Haus bleibt', 'Ihr Haus.'): ('Das Medaillon', 'bleibt, wie es ist.'),
    ('Ihre Website,', 'Seite für Seite.'): ('Gestern und heute,', 'nebeneinander.'),
    ('Die Ideen', 'hinter der Seite.'): ('Zwölf Gedanken', 'zur Seite.'),
    ('Wie alles', 'zusammenhängt.'): ('Woraus die Seite', 'gezimmert ist.'),
    ('Alle Seiten zum', 'Durchblättern.'): ('Von der Startseite', 'bis zur Abreise.'),
    ('Vorschläge für', 'Ihre Gäste.'): ('Was Gäste', 'selbst erledigen.'),
    ('Rund um', 'den Aufenthalt.'): ('Vor der Reise', 'und danach.'),
    ('Ihre Unterlagen,', 'im selben Stil.'): ('Schpiszettel', 'und Schpis Charte.'),
    ('Ein paar Ideen', 'für Papier.'): ('Für die Stuben', 'und die Zimmer.'),
    ('Ein Feed', 'für Instagram.'): ('Stube für Stube,', 'Zimmer für Zimmer.'),   # Feed vom 17.10.2026, 27 Beiträge
    ('Alles liegt für', 'Sie bereit.'): ('Der ganze Ordner,', 'in einem Stück.'),
    ('Alles geprüft,', 'bevor Sie es sehen.'): ('Zweimal hingeschaut,', 'dann gezeigt.'),
}
KAP_NAME_NEU = {'Guten Tag': 'Ein Brief', 'Register': 'Wegweiser', 'Zum Schluss': 'Bis bald'}


# ---------- Nichts läuft mit dem Scrollen mit (Werkbank-Chat 18.10.2026, Regel 55) ----------
# Robert zum Doldenhorn (17.10.2026, Safari): «die ganze Seite … fackelt. Und oben springt auch das Bild im Text immer hoch und runter» und
# «Wenn man scrollt, dann zittert der Bildschirm so … Auf jeder Höhe, mit jeder Bewegung.» Im Ruedihus gemessen (_qa/zittern.js, Safari-Kern 1440):
# 43 Elemente liefen mit. Im Konflikt fällt der Effekt; Einschweben beim ersten Erscheinen bleibt.
#  · data-drift / data-zug aus dem HTML (Auftakt-Stapel, Feed-Polaroids, Abzüge im Ordner, Fenster im Brief)
#  · Brief-Blatt und Geisterwort hinter den Kapiteln ohne Scroll-Zeitachse (stehen still wie gebaut)
#  · Fenster bleiben wie gebaut (Robert 18.10.2026 ~11:49)
#  · Aufleuchten unter dem ruhenden Zeiger beim Scrollen (unterZeiger) abgemeldet; Überfahren mit der Maus bleibt
_nach_bau_vor_ruhe = nach_bau


def nach_bau():   # noqa: F811
    _nach_bau_vor_ruhe()
    import re as _re
    p = os.path.join(_WB, 'index.html')
    t = open(p, encoding='utf-8').read()
    t = _re.sub(r'\sdata-(?:drift|zug)="[^"]*"', '', t)
    css = ('<style id="rh-ruhe">'
           '.bf .bf-blatt[data-a="heben"],.bf .bf-blatt[data-a="heben"].da{animation:none!important}'
           '.kap__geist{animation:none!important}'
           # Fenster wie gebaut (Robert 18.10.2026 ~11:49: «Die Texte müssen genauso wie die Bilder verlaufen in den Fenstern und nicht mit dem Bildschirm
           # mitgehen»): Foto und Schrift stehen, die Seite scrollt darüber; das Zittern beim Doldenhorn kam vom zweispaltigen Brief, nicht von den Fenstern
           # Robert 18.10.2026 ~01:02 (alle Häuser): «wenn ich klicke auf Buttons und dann springen die Buttons hoch und runter» und «wenn ich die
           # Buttons berühre, dann gehen sie so leicht nach oben und sind abgeschnitten»: Knöpfe, Reiter und Pfeile stehen fest (Liste wie Gasterntal)
           '.kn:hover,.kn:active,.fb__w:hover,.fb__w:active,.fb__pf button:hover,.fb__pf button:active,.rund:hover,.rund:active,.wahl button:active,.vh-wahl button:active,'
           '.bn button:hover,.bn button:active,.glanz:active,.lu-pf:hover,.lu-pf:active,.ins-r:hover,.ins-r:active,.ins-zu:active,.ins-vor:active,.wf__pf:hover,.wf__pf:active,'
           '.rgc-p:hover,.rgc-p:active,.ins-m:hover,.ins-m:active,.bn.gewaehlt button{transform:none!important;translate:none!important;scale:none!important;animation:none!important}'
           '.kn:hover i,.kn:hover svg{transform:none!important}'
           # Sprachen-Zeile (Robert 18.10.2026 ~14:40), im Kapitel Website und im Angebot «Was dazugehört»
           '.sp-zeile{margin:22px auto 0;max-width:62ch;text-align:center}.sp-zeile p{margin:0;font-size:.98rem;line-height:1.6;opacity:.86}'
           '.sp-marken{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:12px!important;opacity:1!important}'
           '.sp{display:inline-flex;align-items:baseline;gap:6px;padding:6px 12px;border-radius:999px;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;background:rgba(150,105,55,.14);box-shadow:inset 0 0 0 1px rgba(150,105,55,.35)}'
           '.sp--folgt{background:none;box-shadow:inset 0 0 0 1px rgba(150,105,55,.35);opacity:.72}.sp small{font-size:9px;letter-spacing:.1em;opacity:.8}'
           # Robert 18.10.2026 ~14:20: «Die Button sind jetzt bei allen Häusern unten abgeschnitten.» Die Ruhe-Regel overflow-y:hidden der Leisten schnitt
           # Rundung und Schatten ab; Luft innen, derselbe Wert aussen zurück (Lösung des Waldhotel Doldenhorn)
           '.ins-reiter,.fb__reiter{padding-top:10px!important;padding-bottom:26px!important;margin-top:-10px!important;margin-bottom:-26px!important}'
           '.wahl,.vh-wahl{padding-top:8px!important;padding-bottom:26px!important;margin-top:-8px!important;margin-bottom:-12px!important}'
           '.kn{overflow:hidden}'   # Robert 18.10.2026 23:32: der Glanz beim Überfahren bleibt in der Knopf-Form, kein Balken links und rechts
           '.lu-mehr .lu-pf__t{display:inline!important}'   # Ruedihus 18.10.2026: «Ganze Analyse ansehen» bleibt am Handy lesbar, nicht nur ein Pfeil
           # Robert 18.10.2026 23:30 «Warum sind die Buttons nicht in meinem Button-Stil?»: Zurück, Weiter und «Ganze Analyse ansehen» im Befund als Pille wie jeder
           # Knopf der Werkbank (dunkles Holz, Schrift gesperrt, runder heller Knauf mit Pfeil, gleicher Schatten); am Handy Zurück/Weiter nur der Knauf im Kreis
           '.lu--ruedihus .lu-pf{width:auto!important;height:46px!important;padding:0 7px 0 20px!important;gap:12px!important;justify-content:center!important;border-radius:999px!important;'
           'background:linear-gradient(180deg,#4f3119,#2a180a 55%,#160d06)!important;color:#fff!important;font-family:var(--mono)!important;font-size:11px!important;letter-spacing:.14em!important;text-transform:uppercase!important;'
           'box-shadow:inset 0 1px 0 rgba(255,255,255,.26),inset 0 -3px 0 rgba(0,0,0,.55),inset 0 0 0 1px rgba(255,255,255,.08),0 2px 2px rgba(0,0,0,.25),0 16px 26px -14px rgba(31,19,9,.6)!important}'
           '.lu--ruedihus .lu-pf--l{padding:0 20px 0 7px!important}.lu--ruedihus .lu-pf__t{display:inline!important;color:#fff!important}'
           '.lu--ruedihus .lu-pf__k{width:32px;height:32px;border-radius:50%;background:linear-gradient(180deg,#f8eddb,#dccbae 46%,#b48455);color:#2a1a0e!important;'
           'box-shadow:inset 0 1px 0 rgba(255,255,255,.9),inset 0 -2px 0 rgba(83,56,31,.38),0 3px 6px rgba(0,0,0,.35)}'
           '.lu--ruedihus .lu-pf__k svg{width:14px!important;height:14px!important}'
           '@media(max-width:600px){.lu--ruedihus .lu-fuss .lu-pf{padding:0 7px!important}.lu--ruedihus .lu-fuss .lu-pf__t{display:none!important}}'
                      '/* Robert 18.10.2026 (M21, an der Stube des Carlton): Kacheln reagieren sanft und edel. Kein Kippen, kein Sprung: die Kachel hebt sich langsam wenige Pixel, die Grundneigung bleibt, dazu eine feine Goldlinie */'
           '.blattk{transition:transform 1.1s cubic-bezier(.22,1,.36,1),opacity 1s var(--e1)!important}'
           '.da .blattk--1:hover{transform:rotate(-9deg) translateY(-4px)!important}.da .blattk--2:hover{transform:rotate(-3.5deg) translateY(-4px)!important}'
           '.da .blattk--3:hover{transform:rotate(2.5deg) translateY(-4px)!important}.da .blattk--4:hover{transform:rotate(8deg) translateY(-4px)!important}'
           '.da .faecher--2 .blattk--1:hover,.faecher--2.da .blattk--1:hover{transform:rotate(-6deg) translateY(-4px)!important}'
           '.da .faecher--2 .blattk--2:hover,.faecher--2.da .blattk--2:hover{transform:rotate(4deg) translateY(-4px)!important}'
           '.da .faecher--3 .blattk--1:hover,.faecher--3.da .blattk--1:hover{transform:rotate(-8deg) translateY(-4px)!important}'
           '.da .faecher--3 .blattk--2:hover,.faecher--3.da .blattk--2:hover{transform:rotate(-1deg) translateY(-4px)!important}'
           '.da .faecher--3 .blattk--3:hover,.faecher--3.da .blattk--3:hover{transform:rotate(7deg) translateY(-4px)!important}'
           '.kleb img,.bogenb img,.gabe__b,.zielk__b,.etk li img{transition:transform 1.1s cubic-bezier(.22,1,.36,1)!important}'
           '.kleb:hover img{transform:translateY(-3px)!important}'
           '.bogenb:hover img{transform:translateY(-4px)!important}'
           '.gabe:hover .gabe__b{transform:scale(1.06)!important}'
           '.bn button{transition:transform .9s cubic-bezier(.22,1,.36,1),box-shadow .9s cubic-bezier(.22,1,.36,1)!important}'
           '.bn button:hover{transform:translateY(-2px)!important}'
           '.zielk:hover .zielk__b{transform:translateY(-3px)!important;box-shadow:inset 0 0 0 1px rgba(201,133,67,.22),0 0 0 1px rgba(201,133,67,.55)!important}'
           '.etk li:hover img{transform:translateY(-3px)!important}'
           '#papier img.frei{filter:none!important;box-shadow:none!important}'
           '.wfen .wfen__t{font-size:clamp(26px,4.3vw,62px)!important;line-height:1.08!important}.wfen .wfen__k{font-size:clamp(15px,1.36vw,19px)!important}.wfen .wfen__in{padding-left:max(var(--rand),8vw)!important;padding-right:max(var(--rand),8vw)!important}'   # Robert 18.10.2026 18:40: Schrift in den Fenstern rund ein Fünftel kleiner, mehr Luft zum Rand
           '@media(max-width:900px){.hs2-band{flex-wrap:nowrap!important;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}.hs2-band::-webkit-scrollbar{display:none}.hs2-chip{flex:0 0 112px!important;scroll-snap-align:start}}'   # Robert 18.10.2026 17:36 (M25): Farben nie in zwei Reihen   # Robert 18.10.2026 (Safari): keine Schatten hinter den Drucksachen
'</style>')
    if 'id="rh-ruhe"' not in t:
        t = t.replace('</head>', css + '</head>', 1)
    # Robert 18.10.2026 ~14:55: Werkzeug-Knöpfe nicht auf der Startseite der Werkbank, sondern am Ende der Unterseiten (wb_kapitel.py unterseiten);
    # je Abschnitt höchstens zwei Knöpfe nebeneinander: bei den Unterlagen fällt «Karten in der Tafel pflegen» weg
    if 'class="sp-zeile"' not in t.split('id="seiten"')[1][:4000]:
        import rh_angebot as _ra
        t = t.replace('mit «Öffnen» sind Sie auf der echten Seite.</p></div></div>', 'mit «Öffnen» sind Sie auf der echten Seite.</p></div></div>' + _ra.SPRACHEN_HTML, 1)
    t = t.replace('<a class="kn kn--linie" href="#k5">Karten in der Tafel pflegen<i><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg></i></a>', '', 1)
    open(p, 'w', encoding='utf-8').write(t)
    j = os.path.join(_WB, 'werkbank.js')
    s = open(j, encoding='utf-8').read()
    alt = "addEventListener('scroll', function () { if (!zt && zx >= 0) zt = requestAnimationFrame(unterZeiger); }, { passive: true });"
    if alt in s:
        open(j, 'w', encoding='utf-8').write(s.replace(alt, '/* Ruedihus 18.10.2026: beim Scrollen leuchtet nichts unter dem Zeiger auf (Zittern in Safari) */'))
    # Robert 18.10.2026: Gerüst baut sich Kachel für Kachel auf, Spalte für Spalte, gleicher Abstand; jede Linie kommt mit ihrer Zielkachel
    s = open(j, encoding='utf-8').read()
    if 'Ruedihus Reihe' not in s:
        a1 = "B.n.forEach(function (n) { nach[n[0]].el.style.transitionDelay = (n[1] * TK.sp + n[2] * TK.z).toFixed(2) + 's'; });\n      lagen.forEach(function (s, i) { s.style.transitionDelay = (i * TK.sp + TK.linie).toFixed(2) + 's'; });"
        b1 = ("/* Ruedihus Reihe 18.10.2026 */ var rf = B.n.slice().sort(function (a, b) { return a[1] - b[1] || a[2] - b[2]; }), dl = {};\n"
              "      rf.forEach(function (n, i) { dl[n[0]] = i * 0.09; nach[n[0]].el.style.transitionDelay = dl[n[0]].toFixed(2) + 's'; });\n"
              "      lagen.forEach(function (s) { s.style.transitionDelay = '0s'; });\n"
              "      kanten.forEach(function (k) { [k.p, k.kopf].forEach(function (e) { e.style.transition = 'none'; e.style.opacity = '0'; }); });")
        a2 = "requestAnimationFrame(function () { requestAnimationFrame(function () { brett.classList.remove('vor'); }); });"
        b2 = ("requestAnimationFrame(function () { requestAnimationFrame(function () { brett.classList.remove('vor');"
              " kanten.forEach(function (k) { var t = (Math.max(dl[k.von], dl[k.nach]) + 0.25).toFixed(2) + 's'; [k.p, k.kopf].forEach(function (e) { e.style.transition = 'opacity .6s cubic-bezier(.16,1,.3,1) ' + t; e.style.opacity = ''; }); }); }); });")
        a3 = "lagen.forEach(function (s) { s.style.transitionDelay = ''; });"
        b3 = a3 + " kanten.forEach(function (k) { k.p.style.transition = ''; k.kopf.style.transition = ''; });"
        a4 = "}, TK.ende);"
        b4 = "}, Math.max(TK.ende, 3400));"
        for a, b in ((a1, b1), (a2, b2), (a3, b3), (a4, b4)):
            assert s.count(a) == 1, a[:40]
            s = s.replace(a, b)
        open(j, 'w', encoding='utf-8').write(s)


# Robert 18.10.2026 «Feed dauert sehr lange»: Raster und Highlights im Feed mit 400-px-WebP (feed_leicht.py, wie Doldenhorn), nach jedem Bau
_nach_bau_vor_feed_leicht = nach_bau


def nach_bau():   # noqa: F811
    _nach_bau_vor_feed_leicht()
    import feed_leicht
    feed_leicht.mach()


# Robert 18.10.2026 (M21): auch auf den Unterseiten heben sich die Etiketten nur leicht, ohne Kippen und Vergrössern
_nach_bau_vor_kacheln = nach_bau


def nach_bau():   # noqa: F811
    _nach_bau_vor_kacheln()
    p = os.path.join(_WB, 'seiten.css')
    if os.path.exists(p):
        t = open(p, encoding='utf-8').read()
        if 'Ruedihus Kacheln ruhig' not in t:
            t += ('\n/* Ruedihus Kacheln ruhig (Robert 18.10.2026, M21) */\n.etk li img{transition:transform 1.1s cubic-bezier(.22,1,.36,1)!important}'
                  '\n.etk li:hover img{transform:translateY(-3px)!important}\n')
            open(p, 'w', encoding='utf-8').write(t)


# Robert 18.10.2026 (Safari, online): hinter Etiketten und Drucksachen keine dunklen Ränder. Die Vorschaubilder werden aus den gesetzten Seiten
# ohne den durchsichtigen Rand neu geschrieben (dort lagen beim Drehen dunkle Säume), Breite wie bisher.
_nach_bau_vor_saeume = nach_bau


def nach_bau():   # noqa: F811
    _nach_bau_vor_saeume()
    import glob as _g
    from PIL import Image as _I
    roh, img = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roh', 'papier'), os.path.join(_WB, 'img')
    for z in _g.glob(os.path.join(img, 'k-*.webp')) + _g.glob(os.path.join(img, 'b-*.webp')):
        q = os.path.join(roh, os.path.basename(z)[2:-5] + '.png')
        if not os.path.exists(q):
            continue
        with _I.open(z) as alt:
            breite = alt.width
        im = _I.open(q).convert('RGBA')
        bb = im.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox()
        if bb:
            im = im.crop(bb)
        im = im.resize((breite, round(im.height * breite / im.width)), _I.LANCZOS)
        im.save(z, 'WEBP', quality=86, alpha_quality=100, method=6)


# Prüfung 18.10.2026 (Bänder laden erst beim Blättern): Bilder in Bändern mit seitlichem Überlauf gelten für den Browser nie als sichtbar.
# Kommt ein Band in die Nähe (120 % über und unter dem Bildschirm), werden alle seine Bilder sofort geladen (wie Carlton, werkbank.js).
VORLADEN_JS = ('<script id="rh-vorladen">(function(){if(!("IntersectionObserver" in window))return;(window.requestIdleCallback||function(f){setTimeout(f,700)})(function(){'
               'var kand=[].slice.call(document.querySelectorAll(".band,.aga-reihe,.vh-felder,.ins-dev,.lu-seiten,[class*=reihe],[class*=zug],[class*=leiste]"));'
               '[].forEach.call(document.querySelectorAll("main *"),function(e){var c=getComputedStyle(e).overflowX;if((c==="auto"||c==="scroll")&&e.scrollWidth>e.clientWidth+4&&kand.indexOf(e)<0)kand.push(e)});'
               'var io=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;io.unobserve(x.target);'
               '[].forEach.call(x.target.querySelectorAll("img[loading=lazy]"),function(i){i.loading="eager"})})},{rootMargin:"120% 0px 120% 0px"});'
               'kand.forEach(function(e){if(e.querySelector("img[loading=lazy]"))io.observe(e)})})})();</script>')
_nach_bau_vor_vorladen = nach_bau


def nach_bau():   # noqa: F811
    _nach_bau_vor_vorladen()
    p = os.path.join(_WB, 'index.html')
    t = open(p, encoding='utf-8').read()
    if 'id="rh-vorladen"' not in t:
        open(p, 'w', encoding='utf-8').write(t.replace('</body>', VORLADEN_JS + '\n</body>', 1))


# Robert 18.10.2026 22:09 «überall die Ladezeiten der Bilder prüfen»: gemessen (Safari-Kern, leerer Speicher) lud die Werkbank beim Öffnen
# das grosse Auftaktbild doppelt (vorgeladen 574 kB, angezeigt die 1920er mit 364 kB), und Bilder weiter unten kamen erst, wenn man schon davor stand.
# Jetzt: kein Vorladen der grossen Datei, das Bild sagt seine wahre Breite (die Seite nimmt die passende kleinere Stufe) und hat Vorrang;
# Bilder, die man in eineinhalb Bildschirmhöhen erreicht, laden schon vorher.
FRUEH_JS = ('<script id="rh-frueh">(function(){if(!("IntersectionObserver" in window))return;'
            'var io=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;io.unobserve(x.target);x.target.loading="eager"})},{rootMargin:"0px 0px 150% 0px"});'
            '[].forEach.call(document.querySelectorAll("main img[loading=lazy],body>section img[loading=lazy],section img[loading=lazy]"),function(i){io.observe(i)})})();</script>')
_nach_bau_vor_frueh = nach_bau


def nach_bau():   # noqa: F811
    _nach_bau_vor_frueh()
    p = os.path.join(_WB, 'index.html')
    t = open(p, encoding='utf-8').read(); t0 = t
    t = t.replace('<link rel="preload" href="img/auftakt.webp" as="image">\n', '').replace('<link rel="preload" href="img/auftakt.webp" as="image">', '')
    t = t.replace('<img src="img/auftakt.webp" width="2880" height="1800" alt="" class="ld"',
                  '<img src="img/auftakt.webp" width="2880" height="1800" alt="" class="ld" sizes="(min-width:900px) 46vw, 92vw" fetchpriority="high"', 1)
    if 'id="rh-frueh"' not in t:
        t = t.replace('</body>', FRUEH_JS + '\n</body>', 1)
    if t != t0:
        open(p, 'w', encoding='utf-8').write(t)


# Robert 18.10.2026 ~23:00, alle vier Häuser: «Zurück zur Werkbank» an genau die Stelle. Beim Verlassen der Werkbank (Analyse, Drucksachen, Unterlagen,
# Werkzeuge, Anleitungen, Rezeption, Feed, Mappe, Material, Mails, KI, Karte, Geprüft; nicht die Website) bekommt der Link ?wb=<Höhe>; die Zielseite
# zeigt damit den Knopf (assets/js/zur-werkbank.js). Kommt die Werkbank mit ?y= (oder per Browser-Zurück) wieder, öffnet sie auf dieser Höhe:
# alles darüber steht schon fertig da, alles darunter kommt beim Weiterscrollen wie gewohnt. Bauanleitung: side-session-notes …/zurueck-zur-werkbank-alle-haeuser.md
WB_JS = r'''<script id="rh-zurueck">(function(){
var WEB=/^\/(?:(?:index|anreise|abreise|essen|haus|geschichte|veranstaltungen|zu-zweit|rechtliches|zimmer(?:-[a-z]+)?)\.html)?$/;
function ziel(a){try{var u=new URL(a.getAttribute('href'),location.href);if(!/^https?:$/.test(u.protocol))return null;
 if(/\.pdf$/i.test(u.pathname))return null;
 if(u.origin===location.origin){if(u.pathname===location.pathname)return null;if(WEB.test(u.pathname))return null;return u}
 if(/-analyse\.tastystudios\.ch$/.test(u.hostname)||/potenzialanalyse/.test(u.hostname))return u;return null}catch(e){return null}}
function merk(ev){var a=ev.target.closest&&ev.target.closest('a[href]');if(!a)return;var u=ziel(a);if(!u)return;var y=Math.round(scrollY);
 u.searchParams.set('wb',y);a.href=u.toString();try{sessionStorage.setItem('wb-y',String(y))}catch(e){}
 if(ev.type!=='click'||ev.defaultPrevented||ev.metaKey||ev.ctrlKey||ev.shiftKey)return;
 /* Robert 19.10.2026 01:18 / Endprüfung: nur die sieben Werkzeuge (mit Anleitungen) öffnen einen neuen Tab, den «Zurück zur Werkbank» wieder schliesst;
    Analyse, Drucksachen, Unterlagen, Mappe und die übrigen Beigaben im selben Tab, Safari-Zurück und der Knopf landen an der Stelle */
 var werkzeug=u.origin===location.origin&&/^\/(?:maison|studio|_?werkzeuge)\//.test(u.pathname);
 ev.preventDefault();if(werkzeug)window.open(a.href,'_blank');else location.href=a.href}
document.addEventListener('click',merk,true);document.addEventListener('auxclick',merk,true);
var q=new URLSearchParams(location.search),y=q.get('y'),zur=false;
try{var nav=performance.getEntriesByType('navigation')[0];if(y===null&&nav&&nav.type==='back_forward'){y=sessionStorage.getItem('wb-y');zur=true}}catch(e){}
if(y===null||!/^\d+$/.test(y))return;y=+y;
try{history.scrollRestoration='manual'}catch(e){}
var st=document.createElement('style');st.textContent='html.wb-sofort,html.wb-sofort *{transition:none!important;animation-duration:0s!important;animation-delay:0s!important;scroll-behavior:auto!important}';document.head.appendChild(st);
document.documentElement.classList.add('wb-sofort');
function fertigOben(){var grenze=y+innerHeight*.15;[].forEach.call(document.querySelectorAll('[data-a],.odo,.zt,.roll,img.ld'),function(e){var r=e.getBoundingClientRect();if(r.top+scrollY<grenze&&!e.classList.contains('da')){e.classList.add('da')}})}
function geh(){window.scrollTo(0,y);fertigOben()}
function los(){geh();requestAnimationFrame(function(){geh();requestAnimationFrame(function(){document.documentElement.classList.remove('wb-sofort')})});
 var n=0,t=setInterval(function(){n++;if(Math.abs(scrollY-y)>40&&n<12&&!wegd)geh();if(n>=12)clearInterval(t)},150);
 if(!zur){q.delete('y');history.replaceState(history.state,'',location.pathname+(q.toString()?'?'+q:'')+location.hash)}}
var wegd=false;['wheel','touchstart','keydown'].forEach(function(k){addEventListener(k,function(){wegd=true},{once:true,passive:true})});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',los);else los();
addEventListener('load',function(){if(!wegd&&Math.abs(scrollY-y)>40)geh()});
})();</script>'''
_nach_bau_vor_zurueck = nach_bau


def nach_bau():   # noqa: F811
    _nach_bau_vor_zurueck()
    p = os.path.join(_WB, 'index.html')
    t = open(p, encoding='utf-8').read()
    if 'id="rh-zurueck"' not in t:
        open(p, 'w', encoding='utf-8').write(t.replace('</body>', WB_JS + '\n</body>', 1))


# Robert 19.10.2026 00:30 (Kapitel-Karussell): «Wieso ist da links nichts? Das lädt zu lange.» Die Nachbarn links lagen ausserhalb des Bildes und luden
# erst beim Blättern. Jetzt: jedes Bild beider Karusselle (Register und «Das Wichtigste») gibt es zusätzlich in 600 px; sobald ein Karussell
# eineinhalb Bildschirme entfernt ist, laden und entpacken alle seine Bilder, vorwärts wie rückwärts sofort da.
KARUSSELL_JS = ('<script id="rh-karussell">(function(){var K=[].slice.call(document.querySelectorAll("#register .rgw,[data-wfa],[data-rgw]"));if(!K.length)return;'
                'function hol(k){[].forEach.call(k.querySelectorAll("img"),function(i){try{i.fetchPriority="high"}catch(e){}i.loading="eager";if(i.decode)i.decode().catch(function(){})})}'
                'if(!("IntersectionObserver" in window)){K.forEach(hol);return}'
                'var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){io.unobserve(x.target);hol(x.target)}})},{rootMargin:"300% 0px 300% 0px"});'
                'K.forEach(function(k){io.observe(k)})})();</script>')
_nach_bau_vor_karussell = nach_bau


def nach_bau():   # noqa: F811
    _nach_bau_vor_karussell()
    import re as _re
    from PIL import Image as _Im
    p = os.path.join(_WB, 'index.html')
    t = open(p, encoding='utf-8').read(); t0 = t
    for name in sorted(set(_re.findall(r'<img src="eigen/(fo-[a-z-]+)\.webp" width="1000" height="1000"', t))):
        q = os.path.join(_WB, 'eigen', name + '.webp'); z = os.path.join(_WB, 'eigen', name + '-600.webp')
        if os.path.exists(q):
            with _Im.open(q) as im:
                im.resize((600, round(im.height * 600 / im.width)), _Im.LANCZOS).save(z, 'WEBP', quality=82, method=6)
            t = t.replace(f'<img src="eigen/{name}.webp" width="1000" height="1000"',
                          f'<img src="eigen/{name}-600.webp" srcset="eigen/{name}-600.webp 600w, eigen/{name}.webp 1000w" sizes="(max-width:700px) 80vw, 34vw" width="1000" height="1000"')
    if 'id="rh-karussell"' not in t:
        t = t.replace('</body>', KARUSSELL_JS + '\n</body>', 1)
    if t != t0:
        open(p, 'w', encoding='utf-8').write(t)
