# Wirtschaft am Schlössli, Potentialanalyse · Inhalt des ersten Entwurfs (ohne Blender), Stand 19.10.2026.
# Jede Aussage mit Beleg: Aufnahme (stellen/ → belege/), Quelltext-Zeile (roh/) oder Datei in _quelle/.
# Gelesen von bau.py. Wortlaut des Hauses steht in «», unverändert.

STAND = '19. Oktober 2026'
SEITE = 'https://www.schloessli-bottighofen.ch'

GRUSS = [
    'Guten Tag nach Bottighofen, Herr Kuchler, Frau Huber, Herr Volpert.',
    'Wir haben Ihre Seite gelesen wie ein Gast: am Telefon und am Rechner, jede der fünfzehn Seiten, die Karten als PDF, die Formulare bis zum letzten Feld, dazu den Quelltext. Was wir gefunden haben, steht hier, jeweils mit der Stelle, an der man es selbst nachsehen kann.',
    'Vorweg: Ihr Haus ist stärker als seine Seite. In anderthalb Jahren seit der Eröffnung am 3. April 2025 kamen die Entdeckung des Jahres, der 15. Punkt und 91 Punkte bei Falstaff. Auf der Seite steht davon ein kleines Siegel ganz unten.',
]

ZAHLEN = [
    ('15', 'Punkte GaultMillau', 'Guide 2027, gaultmillau.ch, 19.10.2026'),
    ('2026', 'Entdeckung des Jahres', 'GaultMillau für Monika Huber, Oktober 2025'),
    ('91', 'Punkte Falstaff', 'Falstaff Magazine Schweiz Nr. 5/2026'),
    ('4,2', 'bei Google, 85 Bewertungen', 'Google Maps, 19.10.2026'),
]

# Befunde: Reihenfolge = was ein Inhaber zuerst versteht. belege: Liste von Aufnahmen (id aus belege.json) oder Quelltext-Blöcken.
BEFUNDE = [
 dict(nr='01', kurz='Auszeichnungen', foto='monika',
  titel='Die Entdeckung des Jahres steht nirgends auf Ihrer Seite',
  wo='Startseite, ganz unten im Fuss. Am Telefon nach fast sechs Bildschirmhöhen (Siegel bei 4868 von 5466 Pixeln).',
  was='Zwei Siegel im Fuss: GaultMillau mit 15 und eine Michelin-Plakette mit der Jahreszahl «2025». Die «Entdeckung des Jahres 2026» steht auf keiner der fünfzehn Seiten, Falstaff mit 91 Punkten auch nicht.',
  warum='Ein Paar aus Konstanz liest in der Zeitung, dass Monika Huber die Entdeckung des Jahres ist. Es öffnet Ihre Seite, sieht blaue Stühle am See und «Willkommen». Warum gerade jetzt ein Tisch bei Ihnen besonders ist, erfährt es nicht.',
  gaeste='Der Grund, der sie neugierig gemacht hat, fehlt genau dort, wo sie nachsehen.',
  haus='Drei Auszeichnungen in einem Jahr arbeiten auf der eigenen Seite nicht mit.',
  tun='Auszeichnungen mit Satz und Quelle oben auf die Startseite und zu Monika Huber, die Plakette mit dem richtigen Jahr.',
  belege=['fuss-handy'],
  quellen=['https://www.gaultmillau.ch/restaurants/wirtschaft-am-schlossli-844948', '_quelle/presse/tz-14-punkte.md (08.10.2025)', '_quelle/extern/portale/falstaff-restaurant.md', 'Suche in allen 15 Seitentexten nach «Entdeckung» und «Falstaff»: kein Treffer (19.10.2026)']),

 dict(nr='02', kurz='Reservieren', foto='stuehle',
  titel='«Reservation» sieht nicht aus wie ein Knopf und kommt erst nach dem Wischen',
  wo='Startseite, unter dem grossen Foto. Am Telefon und am Rechner liegt sie unterhalb des ersten Bildschirms.',
  was='Der erste Bildschirm zeigt nur das Foto und den Namen. Darunter steht «Reservation» als gesperrte Schrift ohne Rahmen. Den einzigen Rahmen hat das «Lunch-Menü» daneben. Im Quelltext ist die Reservation als kleiner Knopf der dritten Stufe eingestellt, das Lunch-Menü als grosser Knopf der zweiten.',
  warum='Jemand will für Samstag einen Tisch auf der Terrasse. Am Telefon sieht er Stühle und Wasser, wischt, und das Auffälligste ist das Lunch-Menü. Wer nicht sucht, tippt dort hin und landet in einer PDF-Datei.',
  gaeste='Der kürzeste Weg zum Tisch ist der unauffälligste auf der Seite.',
  haus='Reservierungen hängen an einem Wort, das wie eine Überschrift aussieht.',
  tun='Reservieren im ersten Bildschirm, als klarer Knopf, am Telefon immer erreichbar. Reserviert wird weiter über gastronovi.',
  belege=['start-handy-1', 'start-handy-2', 'start-rechner',
          dict(code='roh/start.html', datei='Quelltext der Startseite', zeilen=[(2544, 'data-button-type="tertiary"'), (2548, 'href="https://services.gastronovi.com/restaurants/118851/reservation/widget"'), (2549, 'class="sqs-block-button-element--small sqs-button-element--tertiary …"'), (2608, 'data-button-type="secondary"'), (2612, 'href="/s/Lunch_261019.pdf"'), (2613, 'class="sqs-block-button-element--large sqs-button-element--secondary …"')], mark=[2549, 2613])],
  quellen=['Aufnahmen iPhone 390 × 844 und Rechner 1440 × 900, Chromium, 19.10.2026', 'In Safari-Technik (WebKit) gemessen: Reservation ohne Rahmen («0px none»), Lunch-Menü «2px solid»']),

 dict(nr='03', kurz='Karten', foto='wein',
  titel='Ihre Karten sind aktuell, aber nur als PDF zu lesen',
  wo='Menü «Karten», dann «Speisekarte», «Weinkarte» oder «Lästermeile». Dazu «Lunch-Menü» auf der Startseite.',
  was='Jede Karte öffnet eine PDF-Datei im Format A4: die Speisekarte vom 30. September auf zwei Seiten, die Weinkarte vom 14. Oktober auf 26 Seiten, das Lunch-Menü vom 18. Oktober. Am Telefon steht eine A4-Seite so klein da wie rechts, man muss sie erst gross ziehen.',
  warum='Ein Gast sitzt im Zug nach Bottighofen und möchte wissen, was es heute gibt. Er tippt auf «Speisekarte», bekommt ein Blatt in Briefmarken-Schrift, zieht es auf, verliert die Zeile, zieht wieder.',
  gaeste='Die Küche, für die man kommt, macht am Telefon weniger Lust, als sie sollte.',
  haus='Thon, Quinto Quarto, Parmigiana: die Gerichte stehen nirgends als Text auf der Seite, auch nicht für Google.',
  tun='Jede Karte als eigene Seite, am Telefon lesbar, das PDF zum Ausdrucken bleibt; beides aus einer Liste, die Sie selbst pflegen.',
  belege=['karten-handy', 'speisekarte-pdf'],
  quellen=['https://www.schloessli-bottighofen.ch/karten', 'https://www.schloessli-bottighofen.ch/s/Speisekarte-Oktober.pdf (erstellt 30.09.2026, 2 Seiten A4)', 'https://www.schloessli-bottighofen.ch/s/20261014_Weinkarte.pdf (26 Seiten A4)', 'https://www.schloessli-bottighofen.ch/s/Lunch_261019.pdf']),

 dict(nr='04', kurz='Bankette', foto='stube',
  titel='Eine Bankettanfrage öffnet das Mail-Programm, die zwei Etagen sieht man nicht',
  wo='Menü «Karten», Abschnitt «Banketts & Gruppen», Knopf «Bankettanfrage».',
  was='Der Knopf öffnet ein leeres Mail mit vorbereiteten Zeilen: Datum, Uhrzeit, Personenzahl, Speisenform, Anzahl Gänge, Richt-Budget. Von den zwei Etagen für je bis zu 26 Personen gibt es kein Foto und keinen Namen.',
  warum='Eine Firma plant ein Essen für 20 Personen. Beim Tippen öffnet sich ein Mail-Programm, das am Rechner im Büro oft gar nicht eingerichtet ist. Wie der Raum aussieht, in dem gefeiert würde, kann sie niemandem zeigen.',
  gaeste='Wer feiern will, plant mit Bildern und einem Formular, nicht mit einem leeren Mail.',
  haus='Anlässe sind die grossen Tische. Heute hängt jede Anfrage am Mail-Programm des Gastes.',
  tun='Beide Etagen mit Bildern und Plätzen, dazu eine Anfrage mit Datum und Personenzahl direkt auf der Seite.',
  belege=['bankett-handy',
          dict(code='_quelle/website/text/karten.md', datei='Ziel des Knopfs «Bankettanfrage»', zeilen=[(0, 'mailto:kontakt@schloessli-bottighofen.ch?subject=Bankettanfrage'), (0, '&body=Guten Tag, Gerne erhalte ich weitere Informationen für eine geplante Feier.'), (0, 'Datum: · Uhrzeit: · Personenzahl: · Gewünschte Speisenform: (Tavolata oder Gesetztes Menue)'), (0, 'Anzahl Gänge: · Richt-Budget für Speisen bzw. insgesamt:')], mark=[])],
  quellen=['https://www.schloessli-bottighofen.ch/karten', '_quelle/website/text/karten.md («auf zwei Etagen Platz für jeweils bis zu 26 Personen»)']),

 dict(nr='05', kurz='Gutschein', foto='digestif',
  titel='Einen Gutschein bestellt man mit einem Formular und wartet auf Post',
  wo='Startseite, «Gutschein» unter dem grossen Foto.',
  was='Es öffnet sich ein Formular: Name, E-Mail, Adresse, «Betrag» als freies Textfeld. Ganz unten ein Pflicht-Häkchen «vor dem Senden ankreuzen», ohne zu sagen, wozu. Bezahlt wird nicht. Nach dem Senden steht da: «Wir senden Ihnen eine Bestätigung, sobald der Gutschein versendet wurde.»',
  warum='Am Abend vor einem Geburtstag sucht jemand ein Geschenk. Er füllt alles aus, kreuzt ein Kästchen an, dessen Sinn er nicht kennt, und hat danach nichts in der Hand.',
  gaeste='Ein Geschenk, das man sofort haben möchte, bleibt offen.',
  haus='Jede Bestellung kommt als Formular an und wird von Hand bearbeitet, das Geld kommt später.',
  tun='Gutscheine mit Betrag zum Auswählen, gleich bezahlt und sofort als schönes PDF da.',
  belege=['gutschein-handy'],
  quellen=['Formular «Gutschein» im Quelltext der Startseite (formFields, «vor dem Senden ankreuzen», formSubmissionMessage), 19.10.2026']),

 dict(nr='06', kurz='Newsletter', foto='apero',
  titel='Das Feld «Abonnieren» hat keinen Ort, an dem Anmeldungen ankommen',
  wo='Menü «Kontakt & Öffnungszeiten», nach der Anfahrt.',
  was='Gäste sehen «Abonnieren» mit Feld und Knopf «Registrieren». Im Quelltext ist für das Feld kein Speicherort eingetragen, und Squarespace hat in den Baustein selbst geschrieben: «Dieser Newsletter-Block benötigt eine Speichermöglichkeit.»',
  warum='Eine Stammgästin möchte von der nächsten Gourmetkreuzfahrt rechtzeitig erfahren und trägt ihre Adresse ein. Ob sie je etwas bekommt, ist offen.',
  gaeste='Wer Ihnen folgen will, bekommt womöglich nie Post.',
  haus='Ob Anmeldungen ankommen, lässt sich nur von innen prüfen. Sichtbar ist: eingerichtet ist der Baustein nicht.',
  tun='Ein Newsletter, der ankommt, oder das Feld weg, bis es einen gibt.',
  belege=['newsletter-handy',
          dict(code='roh/kontakt.html', datei='Quelltext der Kontaktseite', zeilen=[(3227, 'Dieser Newsletter-Block benötigt eine Speichermöglichkeit. Bearbeite den Block und gib über den Tab Speicher ein, wo er gespeichert werden soll.'), (3245, 'data-collection-id=""')], mark=[3227, 3245])],
  quellen=['https://www.schloessli-bottighofen.ch/kontakt', 'Nachtrag zum Befund vom 18.10.2026: dort als «für Gäste unsichtbar» notiert; am 19.10.2026 am Telefon sichtbar (Aufnahme)']),

 dict(nr='07', kurz='Küche und Team', foto='team',
  titel='Monika Hubers Weg steht im Text einer Kreuzfahrt, nicht bei ihr',
  wo='Menü «Über uns». Der Weg steht unter «Events & Termine», Excellence Gourmetkreuzfahrt.',
  was='«Über uns» zeigt fünf Fotos mit Name und Aufgabe, keinen Satz dazu. Dass Monika Huber bei Dieter Koschina in der Vila Joya gelernt hat, steht nur in der Beschreibung der Kreuzfahrt. Die Patissière Theresa Hermann, die GaultMillau nennt, fehlt.',
  warum='Wer nach dem Artikel über die Entdeckung des Jahres wissen möchte, wer da kocht, findet ein Foto und das Wort «Küchenchefin».',
  gaeste='Die Menschen, für die man kommt, bleiben ohne Geschichte.',
  haus='Ein Weg von der Algarve über das Schäfli an den See ist erzählt, nur an der falschen Stelle, und nach dem 15. November ist die Kreuzfahrt vorbei.',
  tun='Eine Seite über Küche und Gastgeber mit ihren Wegen, dazu die Patisserie.',
  belege=['team-handy', 'kreuzfahrt-handy'],
  quellen=['https://www.schloessli-bottighofen.ch/uber-uns', 'https://www.schloessli-bottighofen.ch/events-2-1/excellence-g-ourmetkreuzfahrt', '_quelle/presse/gaultmillau-zwei-koeniginnen.md (30.03.2025, Theresa Hermann)']),

 dict(nr='08', kurz='Geschichte', foto='postkarte',
  titel='Der Ort hat 350 Jahre Gastgeber-Geschichte, die Seite keinen Satz davon',
  wo='Startseite und «Über uns»: kein Wort zum Schlössli, zum Hafen oder zum Haus.',
  was='Das Schlössli nebenan wurde 1676 als «Haus am See» gebaut, mit der Auflage, dass darin nicht gewirtet wird. Um 1690 setzte der Besitzer trotzdem einen Wirt als Pächter ein, der die Schiffsleute bewirtete. 1888 wurde es «Hotel und Pension Schlössli», später Strandhotel. Ihre Wirtschaft liegt heute im ehemaligen Hafenmeistergebäude daneben.',
  warum='Gäste fragen, warum ein Restaurant am Hafen «Schlössli» heisst. Die Seite kann es ihnen nicht sagen.',
  gaeste='Man sitzt an einem Ort mit Geschichte und erfährt nichts davon.',
  haus='Ein Pächter, der am See Gäste bewirtet, wie schon um 1690: diese Geschichte gehört nur Ihnen.',
  tun='Ein kurzes Kapitel zum Ort, mit den Postkarten des alten Hotels, wenn die Gemeinde zustimmt.',
  belege=[dict(bild='bilder/postkarte-720.webp', text='Gemeindeschrift «Die Bottighofer Mühlen und das Schlössli am See», Gemeinde Bottighofen 1994, Seite 124: Postkarten «Hotel und Pension Schlössli» und «Strand Hotel Schlössli»')],
  quellen=['_quelle/presse/pdf-text/Bottighofen_Heft_2_Schloessli_S103-128_OCR.txt (S. 104–124)', '_quelle/presse/gemeinde-bottighofen-geschichte.md («im ehemaligen Hafenmeistergebäude»)', 'Suche in allen 15 Seitentexten nach «Geschichte», «1676», «1888», «Hafenmeister»: kein Treffer']),

 dict(nr='09', kurz='Anlässe', foto='bar',
  titel='Nach dem Datum verschwinden Ihre Anlässe von der Seite',
  wo='Menü «Events & Termine».',
  was='Unter «Bevorstehende Events & Termine» steht heute ein Anlass, die Gourmetkreuzfahrt. Der Ehemaligen Lunch vom 6. September, das Seenachtfest, die Kitchen Party und der 4-Hands-Lunch mit Patrick Stier sind noch unter ihren Adressen da, aber keine Seite führt mehr hin. Drei Adressen tragen noch Namen aus der Vorlage: «event-two-yf5k9», «event-three-6jzsc» und «zqff5xzr7qhnfnil32eokk5dy6gi5q».',
  warum='Wer im Frühling wissen will, was das Schlössli so macht, sieht nach dem 15. November eine leere Seite.',
  gaeste='Ein lebendiges Haus wirkt zwischen zwei Anlässen still.',
  haus='Der Ehemaligen Lunch mit Weggefährten aus London, Gonten und Weinfelden ist eine Geschichte, die bleiben dürfte.',
  tun='Anlässe mit Datum, die danach von selbst in einen Rückblick wandern.',
  belege=['events-handy', 'ehemalige-handy'],
  quellen=['https://www.schloessli-bottighofen.ch/events-2-1', 'https://www.schloessli-bottighofen.ch/events-2-1/zqff5xzr7qhnfnil32eokk5dy6gi5q', 'sitemap.xml (Befund 18.10.2026)']),

 dict(nr='10', kurz='Bildbeschreibungen', foto='thon',
  titel='Google liest bei Ihren Bildern «Bierkrug» und «deutsches Fachwerkhaus»',
  wo='Kontaktseite (Plakette und Foto des Schäfli) und Startseite (die acht Teller).',
  was='Jedes Bild hat eine Beschreibung, die Google liest. Bei Ihnen klingen sie wie automatisch erzeugt: die Plakette mit zwei Sternen und 18 Punkten heisst «ein Getränk mit der Zahl 18 auf dem Etikett, ein Bierkrug», das Schäfli «ein traditionelles deutsches Fachwerkhaus», der Thunfisch «Gedünsteter Thunfischfilet mit grünen, roten und weißen Beilagen». Der Name eines Gerichts aus Ihrer Karte steht bei keinem Teller.',
  warum='Wer bei Google Bilder nach «Thunfisch Bottighofen» sucht, findet Ihren Teller nicht unter seinem Namen.',
  gaeste='Die Teller auf der Startseite bleiben namenlos, man weiss nicht, was man da sieht.',
  haus='Die Auszeichnung des Schwesterhauses steht für Suchmaschinen als Bierkrug da.',
  tun='Jedes Bild mit dem, was es zeigt: Gericht, Ort, Person.',
  belege=['plakette-handy',
          dict(code='roh/kontakt.html', datei='Quelltext der Kontaktseite', zeilen=[(3820, 'alt="Ein traditionelles deutsches Fachwerkhaus mit grünen Fensterläden und roten Details, im Ort in einer ruhigen Straße."'), (4140, 'alt="Zwei Blumenmotive, ein Getränk mit der Zahl 18 auf dem Etikett, ein Bierkrug."')], mark=[3820, 4140]),
          dict(code='roh/start.html', datei='Quelltext der Startseite', zeilen=[(3790, 'alt="Zwei Männer feiern im Café, einer schenkt dem anderen ein Bier vom Zapfhahn, …"'), (4370, 'alt="Gedünsteter Thunfischfilet mit grünen, roten und weißen Beilagen auf einem weißen Teller"')], mark=[4370])],
  quellen=['https://www.schloessli-bottighofen.ch/kontakt', 'https://www.schloessli-bottighofen.ch/']),

 dict(nr='11', kurz='Versteckte Seiten', foto='glas',
  titel='Ihre schönste Bilderseite ist im Menü nicht zu finden',
  wo='Leiste oben: fünf Punkte. Die Seite «Impressionen» liegt unter /impressionen-1, eine zweite Startseite unter /home-1.',
  was='«Impressionen» zeigt die Fotoserie vom August 2025 gross: das Weinglas vor dem See, die Teller auf Blau. Kein Menüpunkt und kein Knopf führt dorthin. Die zweite Startseite /home-1 ist eine Kopie, ebenfalls ohne Weg dorthin.',
  warum='Wer Bilder sehen will, bevor er reserviert, scrollt die Startseite und findet acht kleine Kacheln. Die grossen Bilder bleiben ungesehen.',
  gaeste='Die stärksten Bilder des Hauses sieht kaum jemand.',
  haus='Professionelle Fotografie bleibt ungenutzt.',
  tun='Die Bilder dort zeigen, wo man über Küche und Terrasse liest; doppelte Seiten weg.',
  belege=['leiste-rechner'],
  quellen=['https://www.schloessli-bottighofen.ch/impressionen-1', 'https://www.schloessli-bottighofen.ch/home-1', 'sitemap.xml (Befund 18.10.2026)']),

 dict(nr='12', kurz='Datenschutz', foto='schild',
  titel='Die Datenschutzerklärung beschreibt Dienste, die Ihre Seite nicht lädt',
  wo='Fuss jeder Seite, «Datenschutz».',
  was='Die Erklärung nennt Google Analytics, Google Ads, Google AdSense, den Tag Manager, einen Online-Shop mit Kundenkonto und die Zahlungsdienste Visa, PayPal und Stripe, dazu das «Privacy Shield». Beim Besuch von Startseite, Karten, Events und Kontakt lädt die Seite am 19. Oktober nur Inhalte von Squarespace und, auf der Kontaktseite, die Karte von Google. Squarespace, auf dem die Seite läuft, und gastronovi, über das reserviert wird, nennt die Erklärung nicht.',
  warum='Ein Gast, der wissen will, was mit seinen Daten bei der Reservation geschieht, liest von Werbung und einem Shop, die es nicht gibt, und von gastronovi nichts.',
  gaeste='Die Erklärung beantwortet nicht, was ein Gast über Ihre Seite wissen möchte.',
  haus='Das «Privacy Shield» hat der Europäische Gerichtshof im Juli 2020 für ungültig erklärt. Ob die Erklärung rechtlich genügt, beurteilt eine Juristin; sichtbar ist, dass sie nicht zu Ihrer Seite passt.',
  tun='Eine Erklärung, die genau die Dienste nennt, die die Seite lädt, und mit jedem neuen mitwächst.',
  belege=['datenschutz-handy', 'shop-handy',
          dict(code='messung', datei='Gemessen am 19.10.2026: Adressen, von denen die Seite beim Besuch lädt', zeilen=[(0, 'Startseite, Karten, Events:  www.schloessli-bottighofen.ch · assets.squarespace.com · definitions.sqspcdn.com · static1.squarespace.com · images.squarespace-cdn.com · file.squarespace-cdn.com'), (0, 'Kontakt, zusätzlich:  www.google.com · maps.googleapis.com · maps.gstatic.com · www.gstatic.com · fonts.googleapis.com · fonts.gstatic.com'), (0, 'Nicht geladen:  google-analytics · googletagmanager · googlesyndication (AdSense) · googleadservices · paypal · stripe')], mark=[])],
  quellen=['https://www.schloessli-bottighofen.ch/datenschutzerklarung', '_quelle/website/text/datenschutzerklarung.md', 'Messung mit Playwright, Cookie-Fenster abgelehnt, 19.10.2026']),

 dict(nr='13', kurz='Sprachen', foto='abend',
  titel='Ihre Seite spricht nur Deutsch, der Guide Michelin auch Englisch',
  wo='Alle Seiten, alle Karten.',
  was='Seite, Karten und Formulare gibt es nur auf Deutsch, eine Sprachwahl fehlt. Der Guide Michelin stellt Ihr Haus auch auf Englisch vor.',
  warum='Ein Gast aus Zürich bringt Geschäftspartner aus London mit. Er schickt den Link, sie verstehen die Karte nicht.',
  gaeste='Wer kein Deutsch liest, findet sich nur mit Mühe zurecht.',
  haus='Welche Sprachen Ihre Gäste sprechen, war auf keinem Portal abzulesen; Englisch ist der naheliegende Anfang.',
  tun='Die Seite auch auf Englisch, umschaltbar an derselben Stelle, auf Wunsch Französisch.',
  belege=['michelin-en'],
  quellen=['Quelltext lang="de-CH", keine weitere Sprache (Befund 18.10.2026)', '_quelle/extern/portale/guide-michelin-en.md', '_kette/03-sammler/sprachen.json']),
]

STIMMT = [
 ('Ihre Fotos', 'Die Terrasse, die blauen Stühle vor See und Alpen, die Teller auf Blau: eigene, starke Bilder aus zwei Serien (August 2025, Mai 2026).', 'stuehle'),
 ('Aktuelle Karten', 'Speisekarte vom 30. September, Weinkarte vom 14. Oktober, Lunch-Menü vom 18. Oktober. Man sieht, dass hier jemand pflegt.', 'wein'),
 ('Klare Zeiten', 'Öffnungs- und Küchenzeiten, Ruhetage und Ferien bis Februar 2027 stehen auf der Kontaktseite.', 'schild'),
 ('Freie Wahl beim Cookie-Fenster', '«ablehnen» steht gleich gross neben «annehmen», nichts liegt darüber.', None),
 ('Für Google vorbereitet', 'Jede Seite hat Titel und Beschreibung, am Telefon läuft nichts seitlich über.', None),
]

SELBST = [
 ('Michelin-Plakette', 'Im Fuss steht «2025». Die Selektion 2026 erscheint am 2. November; danach die Jahreszahl prüfen.', 'https://guide.michelin.com/ch/de/thurgau/bottighofen_1149146/restaurant/wirtschaft-am-schlossli'),
 ('Schweiz Tourismus', 'Der Eintrag auf myswitzerland.com nennt noch «14 Punkte».', '_quelle/extern/myswitzerland/seite-text.md'),
 ('Du und Sie', 'Cookie-Fenster («erklärst du dich»), Newsletter («Melde dich») und das Häkchen in den Formularen («Registriere dich») sprechen per Du, die Seite sonst per Sie.', 'cookie-handy'),
 ('Schweizer Schreibung', '«Genießen» in der Beschreibung, die Google anzeigt, «Straße und Hausnummer» im Gutschein-Formular, «Menue» bei den Banketten.', SEITE + '/karten'),
 ('Instagram', '2’601 Menschen folgen @schloessli_bottighofen. Das Konto ist im Quelltext hinterlegt, im Fuss fehlt das Zeichen.', 'fuss-rechner'),
 ('Pflicht-Häkchen', '«vor dem Senden ankreuzen» im Gutschein- und im Kontaktformular sagt nicht, wozu.', SEITE + '/kontakt'),
]

CHANCEN = [
 ('Die Geschichte des Ortes', '1676 das «Haus am See», um 1690 der erste Wirt als Pächter, 1888 «Hotel und Pension Schlössli», die Fischenz im Konstanzer Trichter; dazu die Postkarten aus der Gemeindeschrift.', '_quelle/presse/pdf-text/Bottighofen_Heft_2_Schloessli_S103-128_OCR.txt'),
 ('Monika Hubers Weg', 'Vila Joya an der Algarve, Sous-Chefin im Schäfli, Entdeckung des Jahres, 15. Punkt. Daneben Theresa Hermann (Patisserie) und Jonas Volpert, dessen Weinkeller laut GaultMillau «manches Fine-Dining-Restaurant» neidisch machen dürfte.', '_quelle/extern/portale/gaultmillau.md'),
 ('Terrasse und Lästermeile', 'Die Terrasse «im Schatten prächtiger Platanen» (GaultMillau), die Lästermeile als eigene Terrasse an der Hafenpromenade mit Tapas den ganzen Tag (Michelin).', '_quelle/extern/portale/guide-michelin-de.md'),
 ('Die Familie mit dem Schäfli', 'Beide Seiten verweisen schon aufeinander; der Ehemaligen Lunch hat die Weggefährten aus Wigoltingen an den See geholt.', SEITE + '/kontakt'),
 ('Anlässe mit Rückblick', 'Gourmetkreuzfahrt, Seenachtfest mit «beste Sicht» auf das Feuerwerk, 4-Hands-Lunch: ein Jahr voller Anlässe, das sichtbar bleiben kann.', SEITE + '/events-2-1'),
 ('Hunde willkommen', 'Falstaff nennt es, das Tagblatt erzählt vom Napf, der aus der Champagnerflasche gefüllt wird. Auf der Seite steht es nicht.', '_quelle/presse/tagblatt-zu-tisch.md'),
]

# Teil «Ihre Seite heute»: wer dahinter steht, was wem gehört (Befund 02 «Wer hinter der heutigen Seite steht», selbst nachgeprüft 19.10.2026)
HEUTE = dict(
 fakten=[
  ('Gebaut mit', 'Squarespace, Baukasten mit Abo, Vorlage 7.1. Angelegt am 12. September 2024. Eine Agentur nennt die Seite nirgends, weder im Fuss noch im Impressum noch im Quelltext.', 'Quelltext Zeile 198: «templateId":"5c5a519771c10ba3470d8101","templateVersion":"7.1"»; Server-Antwort «server: Squarespace» (19.10.2026)'),
  ('Laufzeit', 'Der Vertrag läuft, bis eine Seite kündigt; bezahlte Abos verlängern sich von selbst und lassen sich jederzeit im Konto abschalten. Eine Rückzahlung gibt es nur nach Ermessen von Squarespace oder wenn das Gesetz es verlangt.', 'Squarespace Terms of Service, gültig ab 27.03.2025, Ziffer 9, 9.4 und 11 (gelesen 19.10.2026)'),
  ('Ihre Inhalte', 'Texte und Bilder bleiben Ihre. Squarespace erhält aber eine weltweite, unbefristete und unwiderrufliche Lizenz daran. Vorlage und Gestaltung gehören Squarespace.', 'Terms of Service Ziffer 2.1, 2.2 und 5.4 («Squarespace owns the Templates»)'),
  ('Mitnehmen', 'Exportieren lassen sich Seiten mit Text und Bildern als WordPress-Datei. Stil-Einstellungen, eigenes CSS, Kopf- und Fussbereiche sowie Video- und Produktbausteine kommen nicht mit.', 'Squarespace-Hilfe «Export your site content», Stand 09.10.2026'),
  ('Rechte an Bildern', 'Laut Impressum gehören die Rechte an Inhalten und Bildern der Taverne zum Schäfli AG; betrieben wird die Wirtschaft von der CK Gastro Consulting GmbH. Die Fotografen sind in den Dateien nicht genannt.', 'https://www.schloessli-bottighofen.ch/impressum; _quelle/fotografen-aus-metadaten.json'),
 ],
 bei_uns='Bei uns gehören Seite, Adresse und Zugänge dem Haus, der Server läuft auf Ihren Namen, und die Reservation bei gastronovi bleibt, wie sie ist.',
 offen=['Welches Squarespace-Abo Sie haben und was es kostet', 'Wer die Seite gebaut hat und pflegt', 'Bei wem die Adresse schloessli-bottighofen.ch registriert ist', 'Was Ihr unterschriebener Vertrag vorsieht: eine Frage fürs Gespräch'],
)
