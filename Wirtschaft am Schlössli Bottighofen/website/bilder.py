# Bilder leicht ausliefern: aus den Originalen in _quelle/ werden Liefergrössen (WebP) und ein winziges echtes Abbild als Grund gebaut.
# Horizont = Höhe des Seehorizonts im Bild (Anteil von oben), am Bild gemessen 19.10.2026 (Station 07, Skala in _qa/horizont/).
# Lauf: python3 bilder.py  →  assets/img/<name>-<breite>.webp + inhalt/bilder.json
import json, base64, io, pathlib, subprocess
from PIL import Image, ImageOps

HIER = pathlib.Path(__file__).resolve().parent
Q = HIER.parent / '_quelle'
W = 'website/bilder/'
AUS = HIER / 'assets' / 'img'
BREITEN = [480, 800, 1200, 1800, 2400]

# name: (Datei, Horizont oder None, Bildbeschreibung, Ausschnitt (l, o, r, u) als Anteile oder None)
C2 = 'extern/wikipedia-commons/bilder/'
BILDER = {
    'start':      (W + '8cc68d_32_-_FHF_2573.jpg', .305, 'Blaue Stühle auf der Terrasse am Mittag, dahinter der Bodensee und die Alpen', None),
    'start-hoch': (W + '8cc68d_32_-_FHF_2573.jpg', .305, 'Blaue Stühle auf der Terrasse am Mittag, dahinter der Bodensee und die Alpen', (.16, 0, .66, 1)),
    'platanen':   (W + '178109_IMG_1967.jpeg', .433, 'Gedeckte Tische unter den Platanen, Sonnenschirme, dahinter der Hafen', None),
    'lounge':     ('extern/myswitzerland/01_922778687.jpg', .305, 'Lounge mit Champagner am Ufer, dahinter der See und die Alpen', None),
    # Gästefoto von Tripadvisor (Robert 19.10.2026, 18:28, Bild 4 aus _varianten/fenster): Rechte bei den Gästen, nur für die Demo; vor jeder Veröffentlichung durch ein Foto des Hauses ersetzen
    'baum':       ('extern/portale/tripadvisor/tripadvisor-09.jpg', None, 'Gäste am Tisch im Schatten des Baums am Ufer, roter Sonnenschirm, dahinter der See', (0, .28, 1, .83)),
    'gaststube':  (W + '50fa79__DSC5718.JPG', None, 'Die Gaststube mit grossen Fenstern zum Hafen', None),
    'mi-teller':  ('extern/portale/guide-michelin/guide-michelin_titelbild.jpeg', None, 'Ein Gericht der Küche in einer geriffelten Schale', None),
    'bar':        (W + 'b49b5b_IMG_2226.jpeg', None, 'An der Bar wird ein Bier gezapft, unter der Theke die Zementfliesen', None),
    'regal':      (W + 'de97ff_IMG_2166.jpeg', None, 'Flaschen im Regal an der Bar, durch die Scheibe der See', None),
    'schild':     (W + 'a005f3_2026-05-22_193805_Schl_C3_B6ssli_SM.jpg', None, 'Wegweiser zur A-la-carte-Restaurant-Terrasse und zur Lästermeile', None),
    'fliesen':    (W + '7c2036_IMG_2037.jpeg', None, 'Die Zementfliesen an der Bar', None),
    'thon':       (W + 'fc5b3b_Schloessli_August2025-11-5.jpg', None, 'Thunfisch in Scheiben in einer gerippten Schale', None),
    'pasta':      (W + '93b96d_Schloessli_August2025-12-6.jpeg', None, 'Schwarze Pasta mit Garnelen und Meeresfrüchten', None),
    'iberia':     (W + 'd18c6d_Schloessli_August2025-9-4.jpg', None, 'Fisch in grüner Sauce in einer gerippten Schale, daneben ein Weinglas', None),
    'tortelloni': (W + '88d916_Tortelloni.jpg', None, 'Tortelloni mit Tomate, Burrata und Taggiasca-Olive', None),
    'moni':       (W + 'c39c8a_5_-_FHF_2667.jpg', None, 'Monika Huber, Küchenchefin, auf der Terrasse', None),
    'sauce':      ('extern/myswitzerland/02_922778688.jpg', None, 'Die Sauce wird mit dem Löffel angegossen', None),
    'team':       (W + 'd51216_2_-_FHF_2646.jpg', None, 'Das Team der Wirtschaft am Schlössli vor der Holzwand', None),
    'glas':       (W + '9a3afc_Schloessli_August2025-1-1.jpg', .485, 'Ein Glas Weisswein und ein Wasserglas vor dem See', None),
    'wein':       (W + '8e85ca__DSC5833_1.JPG', None, 'Weinflaschen im Regal', None),
    'jonas':      (W + 'dfee6f_11_-_FHF_2706.jpg', None, 'Jonas Volpert, Gastgeber und Sommelier, auf der Terrasse', None),
    'lukas':      (W + '5c9a30_13_-_FHF_2729.jpg', None, 'Lukas Siebel, Sous-Chef, auf der Terrasse', None),
    'apero':      (W + '816543_2026-05-22_205034_Schl_C3_B6ssli_SM.jpg', .61, 'Ein Spritz und ein Bier auf einem blauen Tisch in der blauen Stunde', None),
    'anguria':    (W + '7f6b93_Anguria.jpg', None, 'Ein Teller von oben auf dem blauen Platzteller', None),
    'teller':     ('website/bearbeitet/teller-anguria.jpg', None, 'Ein Teller von oben auf dem blauen Platzteller', None),  # aus teller_bild.py (Auftakt)
    'dessert':    (W + '9f207d_Schloessli_August2025-18-9.jpg', None, 'Dessert mit Beeren auf einem blauen Teller, dahinter ein Wasserglas', None),
    'abend':      (W + '28f071_2026-05-22_220420_Schl_C3_B6ssli_SM_blurred.jpg', .565, 'Abend unter der Platane mit Lichterkette, Gäste am Tisch über dem See', None),
    'suppe':      (W + '05cfd1_Schloessli_August2025-5-2.jpeg', None, 'Grüne Suppe in einer blauen Schale', None),
    'fisch':      (W + '30467d_Schloessli_August2025-14-7.jpeg', None, 'Fischfilet mit Sauce in einer gerippten Schale, dahinter ein blauer Stuhl', None),
    'salat':      (W + '49a4b9_Schloessli_August2025-7-3.jpeg', None, 'Ein Salat auf einem gerippten silbernen Teller', None),
    'fleisch':    (W + '9f9d8b_Schloessli_August2025-15-8.jpeg', None, 'Gefülltes Fleisch mit Blättern und Blüten auf einem geriffelten Teller', None),
    'haus':       ('extern/wikipedia-commons/bilder/Bar_Wirtschaft_"Schlössli"_am_Bodensee_in_Bottighofen_TG_(2016).jpg', .647, 'Das ehemalige Hafenmeistergebäude mit der Wirtschaft am Hafen von Bottighofen, 2016', None),
    'bootshafen': ('extern/wikipedia-commons/bilder/Bootshafen_mit_Wirtschaft_und_Schlössli_-_MG_0679.jpg', .495, 'Der Bootshafen, dahinter die Wirtschaft und das Schlössli', None),
    'luft1954':   ('extern/wikipedia-commons/bilder/ETH-BIB-Bottighofen,_Strandhotel_Schlössli-LBS_H1-017018.jpg', None, 'Das Strandhotel Schlössli am See aus der Luft, 1954', None),
    'morgen':     ('extern/wikipedia-commons/bilder/Morgen_am_Bodensee_mit_Schifflände_Bottighofen_(2012).jpg', .64, 'Morgen am Bodensee, hinten die Alpen und die Schifflände Bottighofen', None),
    # Grössere Fassung desselben Porträts von papageno-konstanz.de/files/bilder/patrick-stier.jpg (Robert 19.10.2026, 21:14: alte Datei war nur 499 px breit)
    'stier':      ('extern/papageno/patrick-stier.jpg', None, 'Patrick Stier vom Restaurant Papageno in Konstanz', (0, 0, .8, 1)),
    # Anlass-Seite (Robert 19.10.2026, Fassung 14 «Teller zuerst» aus _varianten-kreuzfahrt): Bilder von excellence.ch, Rechte bei Excellence/Twerenbold, nur für die Demo
    'kf-teller':  ('extern/excellence/twerenbold-107002.jpg', None, 'Fisch auf Safransauce in einer gerillten Schale, an Bord der Excellence', None),
    # Plakatwand «Angeschlagen am Hafen», neue Bilder (Robert 19.10.2026, 21:3x «bessere Bilder»): Rechte bei Excellence, Schäfli, Papageno/Guide Michelin, nur Designstudie
    'kf-deck-abend': ('extern/excellence/twerenbold-64243.jpg', None, 'Das Sonnendeck der Excellence in der Abenddämmerung', None),
    'kp-party':   ('extern/schaefli-kitchenparty/kp-3651.jpg', None, 'Kitchen Party in der Gasse vor dem Schäfli am Abend, Lichter und Gäste', None),
    'pa-teller':  ('extern/papageno/papageno-1.jpg', None, 'Hauptgang von Patrick Stier im Papageno auf weissem Teller vor Schwarz', None),
    'kf-anrichten': ('extern/excellence/twerenbold-89782.jpg', None, 'Eine Hand richtet einen Teller an, an Bord der Excellence', None),
    'schaefli':   (W + '172617_IMG_0293.jpeg', None, 'Die Taverne zum Schäfli in Wigoltingen am Abend, die Fenster erleuchtet', None),
    # Bildrecht laut Dateiname bei «Keller», von der Website des Hauses übernommen: vor jeder Veröffentlichung Rechte klären
    'feuerwerk':  (W + '177117_feuerwerk-seenachtfest-konstanz-bildrecht-keller-1.jpg', None, 'Feuerwerk über dem Konstanzer Trichter beim Seenachtfest', None),
    'ig-terrasse': ('extern/ig/ig-02.jpg', None, 'Gäste auf den Stühlen an der Promenade, dahinter die Wirtschaft', None),
    'ig-herd':     ('extern/ig/ig-03.jpg', None, 'In der Küche am Herd', None),
    'ig-teller':   ('extern/ig/ig-07.jpg', None, 'Am Pass werden die Teller angerichtet', None),
    'ig-pasta':    ('extern/ig/ig-09.jpg', None, 'Tortelloni werden von Hand geformt', None),
    'schifflaende': (C2 + 'Bottighofen_TG_-_Schifflände_und_Bootstankstelle.jpg', None, 'Die Schifflände und die Bootstankstelle am Hafen von Bottighofen', None),
    'ig-luft':     ('extern/ig/ig-08.jpg', None, 'Die Terrasse am Abend von oben, davor der Hafen', None),
    'ig-dessert':  ('extern/ig/ig-11.jpg', None, 'In der Küche wird ein Dessert auf den Teller gesetzt', None),
    # Keller als Abzüge vom Abend (Robert 19.10.2026, Fassung 3 aus _varianten/keller-runde2.html): zwei Standbilder aus den Reels, klein (360/524 breit)
    'ig-abend':    ('extern/ig/ig-01.jpg', None, 'Dämmerung über dem See, am Ufer die Lichter', None),
    'ig-hafen':    ('extern/ig/ig-10.jpg', None, 'Die Wirtschaft am Hafen vom Wasser aus', None),
    # Öffnungszeiten (#abend, 19.10.2026): Bilder, die sonst nirgends auf der Website stehen. tb-fisch, tb-glas, tb-teller und tb-dunkel sind Gästefotos von Tripadvisor,
    # Rechte bei den Gästen, vor jeder Veröffentlichung durch Fotos des Hauses ersetzen (wie baum).
    'tb-fisch':    ('extern/portale/tripadvisor/tripadvisor-06.jpg', None, 'Rotbarbe auf Risotto mit grüner Sauce in der gerippten Schale', None),
    'tb-glas':     ('extern/portale/tripadvisor/tripadvisor-11.jpg', None, 'Ein Glas Weisswein auf dem Tisch der Terrasse, dahinter der See', None),
    'tb-teller':   ('extern/portale/tripadvisor/tripadvisor-08.jpg', None, 'Thunfisch mit Kaviar und Sauce in der gerippten Schale auf dem blauen Platzteller', None),
    'tb-dunkel':   ('extern/portale/tripadvisor/tripadvisor-05.jpg', None, 'Masten im Hafen vor dem Abendrot über dem See', None),
    # Freies Foto Commons (Robert 19.10.2026, Bild 4 aus _varianten/fenster-abend-2), abgedunkelt mit abend_bild.py
    'abend-hafen': ('website/bearbeitet/abend-gottlieben.jpg', None, 'Sonnenuntergang am Seerhein in Gottlieben, Laternen und Pfähle am Ufer', None),
    'torte':      (W + 'fb5117_Schloessli_August2025-19-10.jpeg', None, 'Schichttorte mit Beeren auf einem blauen Teller', None),
    # Freie Fotos Commons für die Bankettkarten (Robert 19.10.2026: «Bilder, die wir noch nicht auf der Seite verwendet haben, Moodbilder der Jahreszeiten»)
    'jz-fruehling': ('extern/wikipedia-commons/jahreszeiten/fruehling-apfelbluete.jpg', None, 'Apfelblüte am Bodensee im April', None),
    'jz-sommer':    ('extern/wikipedia-commons/jahreszeiten/sommer-johannisbeeren.jpg', None, 'Reife rote Johannisbeeren am Strauch', (0, .12, 1, .78)),
    # Chronik-Wand (#besen, Robert 19.10.2026): Bilder aus Heft 2 der Gemeinde (1994, S. 103–125), mit KI nachgeschärft (Higgsfield gpt_image_2_5, Roberts Ja),
    # Text der Anzeige nach dem Original gesetzt, Postkarte nur oben (die KI erfand unten einen Brief). Rechte: Gemeinde Bottighofen, nur zur Anschauung, vor Veröffentlichung Erlaubnis holen.
    'ch-postkarte': ('presse/heft-bilder/ki/hf-postkarte-ki-bild.png', None, 'Postkarte Hotel & Pension Schlössli Bottighofen, Gruss vom Bodensee', None),
    'ch-anzeige':   ('presse/heft-bilder/ki/hf-anzeige-ki.png', None, 'Anzeige Hotel & Restaurant Schlössli-Bottighofen, Lohnendster Ausflug, Besitzer Carl Gängel', None),
    'ch-strandhotel': ('presse/heft-bilder/ki/hf-haus-ki.png', None, 'Das Strandhotel Schlössli mit dem weissen Gitterzaun', None),
    'ch-zeichnung': ('presse/heft-bilder/ki/hf-zeichnung-titel-ki.png', None, 'Das Schlössli, gezeichnet von Günter Dittmann', None),
    'ch-mann':      ('presse/heft-bilder/ki/hf-haus-mann-ki.png', None, 'Ein Mann vor dem Schlössli', None),
    'ch-luftkarte': ('presse/heft-bilder/ki/hf-strandhotel-ki.png', None, 'Postkarte Strand Hotel Schlössli Bottighofen aus der Luft', None),
    'ch-portal':    ('presse/heft-bilder/ki/hf-portal-ki.png', None, 'Das Portal des Schlössli am See', None),
    'ch-ufer':      ('presse/heft-bilder/ki/hf-ufer-ki.png', None, 'Hotel und Restaurant Schlössli vom See aus, Segelboot und Ruderboote', None),
    'jz-herbst':    ('extern/wikipedia-commons/jahreszeiten/herbst-zwetschgen.jpg', None, 'Reife Zwetschgen am Baum', None),
    # Fenster «Mit Blick aufs Wasser und die Alpen» (Robert 19.10.2026: Bild 1 aus _varianten/fenster-bild-2.html), freies Foto Commons
    'saentis':      ('extern/wikipedia-commons/alpen/saentis-ausblick.jpg', None, 'Blick über den Bodensee bis zum Säntis', None),
    # Kopf «Events & Termine» (Robert 19.10.2026: Fassung 8 «Bild im Passepartout» aus _varianten/events-kopf-20.html, Bild 2 aus events-kopf-8-bilder.html), freies Foto Commons
    # Kopf «Events & Termine» seit 19.10.2026 (Robert: Fassung 6 «Nachtblaue Spalte» aus _varianten/events-kopf-runde4.html).
    # Robert 19.10.2026: Foto von der Website des Hauses (177117_feuerwerk-…-bildrecht-keller-1.jpg, nur 1200 breit) mit KI neu erzeugt
    # (Higgsfield gpt_image_2_5, Original als Vorlage, 2336 breit). KI-Bild, nur als Platzhalter bis zu einem echten Foto des Hauses.
    'feuerwerk-ki': ('website/bearbeitet/feuerwerk-ki.png', None, 'Feuerwerk über dem Konstanzer Trichter beim Seenachtfest', None),
    'abendschiff':  ('extern/wikipedia-commons/abend/01-abendschiff-saentis.jpg', None, 'Ein Kursschiff im Abendlicht auf dem Bodensee, dahinter das Säntis-Massiv', None),
}


HK = json.loads((Q / 'extern/wikipedia-commons/bilder/herkunft.json').read_text())
HKJ = json.loads((Q / 'extern/wikipedia-commons/jahreszeiten/herkunft.json').read_text())
HKJ.update(json.loads((Q / 'extern/wikipedia-commons/alpen/herkunft.json').read_text()))
NACHWEIS_EXTRA = {**{k: {'urheber': v['urheber'], 'lizenz': v['lizenz'], 'jahr': v['datum'][:4], 'quelle': v['quelle']} for k, v in HKJ.items()}, **{f: {'urheber': 'Heft 2 der Gemeinde Bottighofen', 'lizenz': 'nur zur Anschauung, mit KI nachgeschärft', 'jahr': '1994', 'quelle': 'https://www.bottighofen.ch/_doc/87701'} for f in ('hf-postkarte-ki-bild.png', 'hf-anzeige-ki.png', 'hf-haus-ki.png', 'hf-zeichnung-titel-ki.png', 'hf-haus-mann-ki.png', 'hf-strandhotel-ki.png', 'hf-portal-ki.png', 'hf-ufer-ki.png')},'01-abendschiff-saentis.jpg': {'urheber': 'Ameichle', 'lizenz': 'CC BY-SA 3.0', 'jahr': '2010', 'quelle': 'https://commons.wikimedia.org/wiki/File:Abendschiff_vor_dem_S%C3%A4ntis-Massiv.JPG'},'abend-gottlieben.jpg': {'urheber': 'JoachimKohler-HB', 'lizenz': 'CC BY-SA 4.0', 'jahr': '2015', 'quelle': 'https://commons.wikimedia.org/wiki/File:Sonnenuntergang_am_SeeRhein_in_Gottlieben_(Thurgau,_2015).jpg'}}
NACHWEIS = {k: {'urheber': v['urheber'].split('  ')[0], 'lizenz': v['lizenz'], 'jahr': (v['datum'][:4] if v['datum'][:4].isdigit() else v['datum'].split('date')[0].strip()[-4:]), 'quelle': v['quelle']} for k, v in HK.items()}


def abbild(im):
    k = im.copy(); k.thumbnail((24, 24))
    b = io.BytesIO(); k.save(b, 'WEBP', quality=40)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def main():
    AUS.mkdir(parents=True, exist_ok=True)
    liste = {}
    for name, (datei, hz, alt, aus) in BILDER.items():
        im = ImageOps.exif_transpose(Image.open(Q / datei)).convert('RGB')
        if aus:
            w, h = im.size; im = im.crop((int(aus[0] * w), int(aus[1] * h), int(aus[2] * w), int(aus[3] * h)))
        w, h = im.size
        breiten = [b for b in BREITEN if b < w] + [min(w, 2400)]
        breiten = sorted(set(breiten))
        for b in breiten:
            ziel = AUS / f'{name}-{b}.webp'
            if not ziel.exists() or ziel.stat().st_mtime < (Q / datei).stat().st_mtime:
                k = im.resize((b, round(h * b / w)), Image.LANCZOS) if b < w else im
                k.save(ziel, 'WEBP', quality=82, method=6)
        nw = NACHWEIS.get(datei.split('/')[-1]) or NACHWEIS_EXTRA.get(datei.split('/')[-1])
        liste[name] = {'nachweis': nw, 'datei': datei, 'w': w, 'h': h, 'verh': round(h / w, 5), 'hz': hz, 'alt': alt, 'breiten': breiten, 'abbild': abbild(im)}
        print(name, w, h, breiten)
    (HIER / 'inhalt' / 'bilder.json').write_text(json.dumps(liste, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
