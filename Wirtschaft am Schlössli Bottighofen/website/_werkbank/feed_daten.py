"""Instagram-Feed der Wirtschaft am Schlössli als Idee. Das Haus hat ein Profil: @schloessli_bottighofen, 2’601 Follower, 584 gefolgt,
46 Beiträge (abgelesen 19.10.2026 ohne Anmeldung, _quelle/extern/ig/profil.txt); dort fast nur Reels vom See, aus der Küche und vom Pass.
Fotos: nur vom Haus selbst (Website des Hauses, Eintrag bei Schweiz Tourismus), keine Gästefotos, keine freien Fotos von Commons,
keine Bilder des Schäfli, keine erzeugten Bilder. Texte zu den Beiträgen: Tasty Studios.

Feed-Planer 19.10.2026 (Master 5a Regel 10a, Bestand und Gegenprobe in _kette/11-werkbank/feed-bestand.md), dritte Fassung «Ein Horizont»:
Robert 19.10.2026 23:18 und ~23:25 zur Fassung «Sitzen bleiben» (drei hohe Bilder über je drei Reihen mit senkrechtem Satz):
«Dieses Bild da mit dem abgeschnittenen Typen gefällt mir nicht.» · «Nee, ich finde das nicht schön mit diesen beiden Bildern übereinander
und den Texten da drin.» Daraus: keine Bilder über mehrere Reihen, keine Schrift in den Bildern, keine angeschnittenen Menschen.
Jetzt: 21 Beiträge, 7 Reihen. Genau in der Mitte (Reihe 4) ein einziges breites Bild über drei Beiträge, ohne Schrift: die blauen Stühle
am Mittag, dahinter der See und die Alpen (das Bild, aus dem die Farben des Markenbuchs stammen). Darüber der Abend und die Küche,
darunter der Mittag und das Ufer. Alle anderen Beiträge sind einzelne Fotos."""
import feed_bogen

B = '../_quelle/website/bilder/'
M = '../_quelle/extern/myswitzerland/'
PROFIL = {'name': 'schloessli_bottighofen', 'titel': 'Wirtschaft am Schlössli', 'art': 'Restaurant',
          'bio': ['Direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen.', 'Mediterrane Küche, die Lästermeile mit Tapas. By Christian Kuchler.'],
          'link': 'schloessli-bottighofen.ch',
          'zahlen': {'beitraege': '46', 'follower': '2’601', 'gefolgt': '584'}, 'stand': '19.10.2026'}
HIGHLIGHTS = [('Terrasse', B + '8cc68d_32_-_FHF_2573.jpg', .45), ('Küche', B + 'fc5b3b_Schloessli_August2025-11-5.jpg', .5),
              ('Lästermeile', B + 'de97ff_IMG_2166.jpeg', .3), ('Team', B + 'dfee6f_11_-_FHF_2706.jpg', .5), ('Abend', B + '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', .3)]
TON = (.95, 1.03, 1.0, 1.01)
REGEL = 'bogen'
SEITE = dict(
    titel=['Ein', 'Horizont.'],
    text1='Auf Ihrem Profil zeigen Sie vor allem Filme vom See und aus der Küche. Meine Idee für das Raster: einzelne Fotos, und genau in der Mitte ein einziges breites Bild über drei Beiträge, Ihre blauen Stühle vor dem See und den Alpen.',
    text2='Darüber der Abend und die Küche, darunter der Mittag am Ufer. Tippen Sie einen Beitrag an, dann sehen Sie ihn gross und mit einem Text dazu.',
    aufbau='Einzelne Fotos, in der mittleren Reihe ein Bild über drei Beiträge',
    texte='Ideen von mir',
    bilder='von Ihrer Website und aus Ihrem Eintrag bei Schweiz Tourismus')


def foto(r, c, key, datei, text, fx=.5, fy=.5, q=B):
    return dict(id=key, r=r, c=c, bild=q + datei, fx=fx, fy=fy, texte=[text])


BOGEN = [
    # Reihen 1–3 (oben, das Neueste). Robert 19.10.2026 ~23:40 zu zwei hellen Tellern übereinander: «… gefällt mir das nicht, dass die Bilder
    # so gleich übereinander sind von dem Farbbett her.» Darum: die hellen Teller-Bilder (weisser Grund, blauer Stuhl) nur in den Ecken
    # jedes Dreier-Blocks, nie neben- oder übereinander; dazwischen dunkle, grüne und blaue Bilder.
    foto(0, 0, 'dessert', '9f207d_Schloessli_August2025-18-9.jpg', 'Zum Schluss etwas Süsses mit Beeren, auf dem blauen Teller.', fy=.55),
    foto(0, 1, 'abend', '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', '«Die schönste Terrasse am Bodensee», sagt Christian Kuchler. Offen bis 23 Uhr.', fx=.3),
    foto(0, 2, 'glas', '9a3afc_Schloessli_August2025-1-1.jpg', 'Ein Glas Weisswein, dahinter nur noch Wasser.', fx=.45),
    foto(1, 0, 'jonas', 'dfee6f_11_-_FHF_2706.jpg', 'Jonas Volpert, Gastgeber und Sommelier. Die Weinauswahl ist seine.', fy=.45),
    foto(1, 1, 'anguria', '7f6b93_Anguria.jpg', 'Von oben gesehen, auf dem blauen Platzteller.'),
    foto(1, 2, 'gaststube', '50fa79__DSC5718.JPG', 'Die Gaststube. Durch die grossen Fenster sieht man den Hafen.', fx=.42),
    foto(2, 0, 'fleisch', '9f9d8b_Schloessli_August2025-15-8.jpeg', 'Gefülltes Fleisch mit Blättern und Blüten.'),
    foto(2, 1, 'regal', 'de97ff_IMG_2166.jpeg', 'Die Digestifs stehen an der Scheibe, dahinter liegt der See.', fx=.32),
    foto(2, 2, 'suppe', '05cfd1_Schloessli_August2025-5-2.jpeg', 'Grüne Suppe in der blauen Schale.', fy=.6),
    # Reihe 4, die Mitte: ein Bild über drei Beiträge, ohne Schrift
    dict(id='horizont', r=3, c=0, w=3, bild=B + '8cc68d_32_-_FHF_2573.jpg', fx=.5, fy=.42,
         texte=['Direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen. Ein Bild über drei Beiträge.', 'Die blauen Stühle der Terrasse am Mittag.', 'Aus diesem Bild stammen die Farben: das Blau der Stühle, der See, der Himmel.']),
    # Reihen 5–7 (unten, der erste Beitrag)
    foto(4, 0, 'torte', 'fb5117_Schloessli_August2025-19-10.jpeg', 'Schichttorte mit Beeren.'),
    foto(4, 1, 'lukas', '5c9a30_13_-_FHF_2729.jpg', 'Lukas Siebel, Sous-Chef.', fy=.4),
    foto(4, 2, 'pasta', '93b96d_Schloessli_August2025-12-6.jpeg', 'Schwarze Pasta mit Garnelen.'),
    foto(5, 0, 'lounge', '01_922778687.jpg', 'Die Lounge am Ufer.', fx=.4, q=M),
    foto(5, 1, 'thon', 'fc5b3b_Schloessli_August2025-11-5.jpg', 'Thunfisch in Scheiben, in der gerippten Schale. Die Küche führt Monika Huber.'),
    foto(5, 2, 'sauce', '02_922778688.jpg', 'Die Sauce wird mit dem Löffel angegossen.', q=M),
    foto(6, 0, 'salat', '49a4b9_Schloessli_August2025-7-3.jpeg', 'Ein Salat auf dem gerippten Teller.'),
    foto(6, 1, 'platanen', '178109_IMG_1967.jpeg', 'Gedeckt unter den Platanen, die Schirme stehen schon. Donnerstag bis Montag ab 11.30 Uhr.', fy=.6),
    foto(6, 2, 'fisch', '30467d_Schloessli_August2025-14-7.jpeg', 'Ein Fischfilet mit Sauce, dahinter ein blauer Stuhl der Terrasse.'),
]
P = feed_bogen.p_liste(BOGEN)
