"""Instagram-Feed des Landgasthofs Ruedihus als Idee. Heute zeigt sich das Haus im gemeinsamen Profil @waldhotel.doldenhorn
(778 Follower, 43 Beiträge, abgelesen am 08.10.2026), ein eigenes Profil gibt es nicht.
Fotos: nur vom Haus selbst (Website, Schweiz Tourismus, Booking.com), keine Gästefotos, keine freien Fotos (auch nicht die Fassaden
von Wikimedia), keine erzeugten Bilder. Sätze auf den Zetteln: Wortlaut der Karten ab 1.3.2026 (Quelle im Kommentar).
Texte zu den Beiträgen: Tasty Studios.

Feed-Planer 17.10.2026 (Master 5a Regel 10a, Bestand und Gegenprobe in _kette/11-werkbank/feed-bestand.md), dritte Fassung nach
Robert ~23:45: «Ruedli: Da ein Bild vom Gebäude nehmen im Grün wie auf Startseite statt dieser Kammer» und «diese Tickets / Anhänger
gefallen mir grundsätzlich nicht … Ich möchte natürlich echte Motive im Feed nehmen und nicht so schlecht animierte Bilder. Mit
irgendeinem Text.» Frühere Fassungen: _sicherung/2026-10-17-2330-feed-vor-roberts-rueckmeldung/ (erste, mit Daten) und
_sicherung/2026-10-17-2350-feed-zweite-fassung/ (zweite, nur der gebaute Feed).
«Stube für Stube, Zimmer für Zimmer». Oben einmal das Haus im Grünen wie auf der Startseite, über sechs Beiträge
(_werkbank/feed_quellen/haus-gruen.png = Startbild ohne Abdunklung, aus varianten3.profi()). Darunter trägt in jeder Reihe ein echtes
Foto den Namen seines Raums als Schrift, weiss mit Textschatten wie im Hero: Ofestübli, Hochzeitsstube, Novembernacht (Sage aus der
Karte der Chäs- und Wystube), Liebeslaube, Hymmelrich, Landhaus. Die Schrift wandert von Reihe zu Reihe die Spalte. Nur echte Fotos,
keine Zettel, Anhänger oder Karten als Grafik. Neun Reihen, 27 Beiträge. Namen und Zeilen der Zimmer: Zimmerseiten der Website."""
import feed_bogen

PROFIL = {'name': 'landgasthof.ruedihus', 'titel': 'Landgasthof Ruedihus', 'art': 'Hotel · Restaurant',
          'bio': ['Gebaut 1753 in Kandersteg. Zu Gast – bei Freunden.', 'Fünf Stuben, Fondue, Raclette und Zimmer mit Himmelbett.'], 'link': 'doldenhorn-ruedihus.ch',
          'zahlen': {'beitraege': '27', 'follower': '–', 'gefolgt': '–'}, 'stand': '08.10.2026'}
HIGHLIGHTS = [('Stuben', 'stube-rund', .5), ('Zimmer', 'z-liebeslaube', .5), ('Karte', 'e-roesti', .35), ('Garten', 'garten-luft', .5), ('1753', 'schild', .5)]
TON = (.94, 1.03, 1.01, .98)
REGEL = 'bogen'
QUELLEN = ('../Carlton-Europe Interlaken/_quelle/doldenhorn-ruedihus',)   # Originale (Schweiz Tourismus 5616 px, Mediathek der Website)
SEITE = dict(
    titel=['Stube für Stube,', 'Zimmer für Zimmer.'],
    text1='Heute zeigt sich das Ruedihus im Profil des Waldhotels Doldenhorn. Meine Idee für ein eigenes: Oben einmal Ihr Haus im Grünen, über sechs Beiträge. Darunter trägt in jeder Reihe ein Foto den Namen seines Raums.',
    text2='Ofestübli, Hochzeitsstube, Liebeslaube, Hymmelrich, Landhaus, und einmal die Novembernacht aus Ihrer Karte. Tippen Sie einen Beitrag an, dann sehen Sie ihn gross und mit einem Text dazu.',
    aufbau='Ein Bild über sechs Beiträge, danach in jeder Reihe ein Foto mit dem Namen seines Raums',
    texte='Ideen von mir. Namen und Zeilen der Zimmer stehen so auf Ihrer Website, die Sage in Ihrer Karte ab 1.3.2026',
    bilder='von Ihrer Website und aus Ihren Einträgen bei Schweiz Tourismus und Booking.com')

BOGEN_CSS = '''
@font-face{font-family:'GB';font-weight:700;src:url('../_werkbank/fonts/Gelasio-Bold.ttf') format('truetype')}
@font-face{font-family:'DM';src:url('../_werkbank/fonts/DMMono-Regular.ttf') format('truetype')}
/* Foto mit Schrift: weiss, Textschatten wie im Hero der Website (dort 0 2px 24px / 0 0 70px, hier auf 1080 px hochgerechnet) */
.sf>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.sf .txt{position:absolute;left:110px;right:110px;color:#fff;text-shadow:0 3px 44px rgba(0,0,0,.9),0 0 130px rgba(0,0,0,.7)}
.sf .unten{bottom:130px}.sf .oben{top:130px}
.sf .gross{font-family:'GB',serif;font-weight:700;font-size:132px;line-height:1.02;letter-spacing:-.01em}
.sf .klein{margin-top:26px;font-family:'DM',monospace;font-size:28px;line-height:1.5;letter-spacing:.2em;text-transform:uppercase}
'''


def foto(r, c, bild, texte, w=1, h=1, fx=.5, fy=.5, id=None):
    return dict(id=id or bild, r=r, c=c, w=w, h=h, bild=bild, fx=fx, fy=fy, texte=texte if isinstance(texte, list) else [texte])


def mit_schrift(r, c, bild, gross, klein, text, op='50% 50%', lage='unten'):
    return dict(id='schrift-' + bild, r=r, c=c, art='html', klasse='sf', texte=[text],
                html=f'<img src="{{bild:{bild}}}" style="object-position:{op}"><div class="txt {lage}"><p class="gross">{gross}</p><p class="klein">{klein}</p></div>')


BOGEN = [
    # Reihen 1–2 (oben, das Neueste): das Haus im Grünen wie auf der Startseite, das einzige Bild über mehrere Beiträge
    foto(0, 0, '_werkbank/feed_quellen/haus-gruen.png', ['Der Landgasthof Ruedihus in Kandersteg, gebaut 1753. Ein Bild über sechs Beiträge.', 'Die bemalte Fassade mit ihren Butzenscheiben.', 'Der grosse Baum vor dem Haus.',
                               'Fünf Stuben hat das Ruedihus.', 'Die Terrasse unter den Schirmen.', 'Ein Sommertag in Kandersteg.'], w=3, h=2, fx=.5, fy=.5, id='haus-gruen'),
    # Reihe 3
    mit_schrift(2, 0, 'ofestuebli', 'Ofestübli.', 'Am grünen Kachelofen', 'Das Ofestübli mit dem grünen Kachelofen.', op='40% 50%'),
    foto(2, 1, 'e-roesti', 'Chalbsläberli mit Röschti, in viu bruunem Anke brate.', fx=.3),   # Karte Egger- und Stettlerstube
    foto(2, 2, 'garten-gitter', 'Der Ziergarten, durch das Fenstergitter gesehen.'),
    # Reihe 4
    foto(3, 0, 'hz-detail', 'Ein altes Telefon und eine Lampe mit Glasschirm.', fx=.5),
    foto(3, 1, 'lh-fenster', 'Aus dem Fenster, draussen liegt Schnee.', fx=.5),
    mit_schrift(3, 2, 'z-hochzeit', 'Hochzeits&shy;stube.', 'Salonzimmer mit Himmelbett', 'Die Hochzeitsstube. Ein Salonzimmer mit Himmelbett, Bad, Dusche und WC.', op='55% 50%', lage='oben'),   # zimmer-hochzeitsstube.html
    # Reihe 5
    foto(4, 0, 'stube-rund', 'Der runde Tisch in der Stube, darüber die Petrollampen.', fx=.45),
    mit_schrift(4, 1, 'haus-daemmerung', 'November&shy;nacht.', 'Unter solchem Glauben entstand 1753 das Ruedihus',   # Karte Chäs- und Wystube ab 1.3.2026
                'Peter Germann liess in einer einzigen bestimmten Novembernacht alles Holz zu seinem künftigen Heim schlagen. So steht es in unserer Karte.', op='42% 50%', lage='oben'),
    foto(4, 2, 'e-terrine', 'Härdöpfelterrine, eine Vorschpiese aus der Egger- und Stettlerstube.', fx=.55),
    # Reihe 6
    mit_schrift(5, 0, 'z-liebeslaube', 'Liebeslaube.', 'Mit einem romantischen Himmelbett', 'Die Liebeslaube mit ihrem Himmelbett, Badewanne und Dusche.', op='55% 50%'),   # zimmer-liebeslaube.html
    foto(5, 1, 'll-detail', 'Ein Bord an der Holzwand: Ähren im Krug, ein Bild, eine Lampe.', fx=.4),
    foto(5, 2, 'stube-lang', 'Eine lange Stube unter alten Balken.', fx=.5),
    # Reihe 7
    foto(6, 0, 'hymmelrich-haus', 'Das Hymmelrich von aussen, im Schnee.', fx=.5),
    mit_schrift(6, 1, 'hy-bett', 'Hymmelrich.', 'Mit einem romantischen Bett', 'Das Hymmelrich: ein romantisches Bett, Badewanne und Dusche.', op='45% 50%'),   # zimmer-hymmelrich.html
    foto(6, 2, 'e-zopf', 'Zopf, Butter und Konfitüre.', fx=.4),
    # Reihe 8
    foto(7, 0, 'd-bilder', 'Alte Fotografien an der Holzwand.', fx=.5),
    foto(7, 1, 'stube-kerze', 'Weiss gedeckt, bei Kerzenlicht.', fx=.5),
    mit_schrift(7, 2, 'z-landhaus', 'Landhaus.', 'Zum Teil mit Himmelbett', 'Die Zimmer im Landhaus: gemütlich, zum Teil mit Himmelbett.', op='50% 50%', lage='oben'),   # zimmer-landhaus.html
    # Reihe 9 (unten, der erste Beitrag)
    foto(8, 0, 'terrasse', 'Die Terrasse im Sommer.', fx=.5),
    foto(8, 1, 'kaffee', 'Kaffee und Dessert in der Stube.', fx=.5),
    foto(8, 2, 'balkon', 'Vom Balkon: Geranien und die Berge.', fx=.5),
]
P = feed_bogen.p_liste(BOGEN)
