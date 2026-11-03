"""Instagram-Feed der Wirtschaft am Schlössli als Idee (Nachtbau 3./4.11.2026, Agent schloessli-werkbank-feed).
Aufbau vom Culinarium (Fassung «Fortsetzung»: die nächsten Beiträge über dem heutigen Feed, nummeriert in der Reihenfolge des Postens,
Schalter «Heute» / «Mit den nächsten …», feed_leicht.py), Inhalt vom Schlössli (alte Fassung «Ein Horizont» vom 19.10.2026 mit 21 Beiträgen,
website/_werkbank.vor-nachtbau-2026-11-03/feed_daten.py, hier erweitert auf 48).

Das Haus hat ein Profil: @schloessli_bottighofen, 2’601 Follower, 584 gefolgt, 46 Beiträge (abgelesen 19.10.2026 ohne Anmeldung,
_quelle/extern/ig/profil.txt); dort fast nur Reels vom See, aus der Küche und vom Pass.
Fotos: nur die eigenen des Hauses aus dem Bildregister der Website (website/assets/img, Register website/inhalt/bilder.json). Nicht verwendet:
Gäste- und Portalbilder (tb-*, baum, mi-teller), Bilder der Kreuzfahrt und anderer Häuser (kf-*, pa-teller, stier, kp-party, schaefli),
Feuerwerk, die Chronik (ch-*), freie Bilder von Commons, erzeugte Bilder. Die ig-* sind schon auf Instagram: sie stehen nur als «heute» unter
den neuen Beiträgen (feed_leicht.py). Texte zu den Beiträgen: Tasty Studios; Sätze auf den Tafeln aus website/inhalt/*.json (Quelle je Tafel).

Robert zur alten Fassung (19.10.2026): keine Bilder über mehrere Reihen, keine Schrift in Fotos, keine angeschnittenen Menschen, helle
Teller-Bilder nie neben- oder übereinander. Darum: einzelne Fotos, ein einziges breites Bild über drei Beiträge (die blauen Stühle am Mittag),
Schrift nur auf eigenen Tafeln; keine zwei Tafeln neben- oder untereinander (nachbarn())."""
import glob, json, os, re
import feed_bogen

_HIER = os.path.dirname(os.path.abspath(__file__))
_WEB = os.path.dirname(os.path.dirname(_HIER))
_INHALT = os.path.join(_WEB, 'inhalt')
HJ = json.load(open(os.path.join(_INHALT, 'haus.json'), encoding='utf-8'))
KARTE = json.load(open(os.path.join(_INHALT, 'karte.json'), encoding='utf-8'))
LUNCH = json.load(open(os.path.join(_INHALT, 'lunch.json'), encoding='utf-8'))
LAESTER = json.load(open(os.path.join(_INHALT, 'laestermeile.json'), encoding='utf-8'))


def quelle(key):
    """Grösste Fassung des Fotos im Bildregister der Website (website/assets/img/<key>-<breite>.webp)."""
    b = sorted(int(m.group(1)) for p in glob.glob(os.path.join(_WEB, 'assets', 'img', key + '-*.webp')) if (m := re.fullmatch(re.escape(key) + r'-(\d+)\.webp', os.path.basename(p))))
    if not b:
        raise FileNotFoundError(key)
    return os.path.join(_WEB, 'assets', 'img', f'{key}-{b[-1]}.webp')


def gericht(name):
    for land in KARTE['laender']:
        for g in land['gerichte']:
            if g['name'] == name:
                return land['land'], g
    raise KeyError(name)


def tapas(name):
    for gr in LAESTER['gruppen']:
        for x in gr['eintraege']:
            if x['name'] == name:
                return gr['titel'], x
    raise KeyError(name)


Z = HJ['zeiten']
TEL = HJ['telefon']
PROFIL = {'name': 'schloessli_bottighofen', 'titel': 'Wirtschaft am Schlössli', 'art': 'Restaurant',
          'bio': ['Direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen.', 'Mediterrane Küche, die Lästermeile mit Tapas. By Christian Kuchler.'],
          'link': 'schloessli-bottighofen.ch',
          'zahlen': {'beitraege': '46', 'follower': '2’601', 'gefolgt': '584'}, 'stand': '19.10.2026'}
HIGHLIGHTS = [('Terrasse', quelle('platanen'), .5), ('Küche', quelle('thon'), .5), ('Lästermeile', quelle('regal'), .3),
              ('Team', quelle('team'), .5), ('Wein', quelle('wein'), .5)]
TON = (.96, 1.03, 1.0, 1.01)
REGEL = 'bogen'
ORT = 'Wirtschaft am Schlössli, Bottighofen'
SEITE = dict(
    titel=['Die nächsten', '48 Beiträge.'],
    text1='Ihr Feed bleibt, wie er ist. Darauf bauen die nächsten 48 Beiträge auf, so wie Sie sie nach und nach posten: die Gourmetkreuzfahrt im November, Lunch, Lästermeile und Banketts im Advent, die Winterpause und der Frühling am See. Dazwischen Teller von Monika Huber, die Weine von Jonas Volpert, das Team und die Terrasse.',
    text2='Kein Foto, das schon auf Ihrem Profil steht, kommt noch einmal vor. Mit dem Schalter sehen Sie Ihren Feed heute und mit den nächsten 48; die Nummern zeigen die Reihenfolge zum Posten. Tippen Sie einen Beitrag an, dann sehen Sie ihn gross und mit Text.',
    aufbau='Die nächsten 48 Beiträge über Ihrem heutigen Feed, nummeriert in der Reihenfolge des Postens',
    texte='Ideen von mir, Zeiten, Karten und Zitate aus Ihren Unterlagen',
    bilder='Ihre eigenen Fotos von der Website, die noch nie gepostet wurden')

# Kleid des Hauses: Nacht über dem See und Papier, Seehimmel als Linie und Zeichen, Open Sans in Versalien gesperrt, Instrument Sans, DM Mono.
_Z = '<i class="z"></i>'   # die Zeiger der Wortmarke (website/assets/svg/zeichen.svg als Maske), einziges Zeichen
BOGEN_CSS = (
    "@font-face{font-family:'O';src:url('../assets/fonts/OpenSans-var.woff2') format('woff2');font-weight:300 800}"
    "@font-face{font-family:'M';src:url('../assets/fonts/DMMono-normal-400.woff2') format('woff2')}"
    "@font-face{font-family:'S';src:url('../assets/fonts/InstrumentSans-normal-400_600.woff2') format('woff2');font-weight:400 600}"
    '.st{--nacht:#0b1d3d;--tief:#0A234C;--stuhl:#113d88;--papier:#E7ECF3;--spiegel:#D0DAE7;--blatt:#F4F6F9;--himmel:#A2B6CF;--himmel2:#C5D2E1;--betont:#0F3678;--tinte:#041023}'
    '.n,.w,.a{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:170px 128px}'
    '.n{background:var(--nacht) url(../assets/svg/tapete-a-dunkel.svg) 0 0/336px 336px;color:var(--blatt)}'
    '.w{background:var(--papier) url(../assets/svg/tapete-a-hell.svg) 0 0/336px 336px;color:var(--tinte)}'
    '.z{display:block;width:66px;height:80px;background:var(--himmel);-webkit-mask:url(../assets/svg/zeichen.svg) center/contain no-repeat;mask:url(../assets/svg/zeichen.svg) center/contain no-repeat}'
    '.w .z{background:var(--betont)}'
    '.kop{position:absolute;top:128px;left:0;right:0;display:flex;justify-content:center}'
    '.fu{position:absolute;bottom:124px;left:120px;right:120px;font:400 24px/1.3 M;letter-spacing:.16em;text-transform:uppercase;color:var(--himmel)}'
    '.w .fu{color:var(--betont)}'
    '.ti{font:400 84px/1.16 O;text-transform:uppercase;letter-spacing:.08em;text-wrap:balance}'
    '.ti span{display:block;white-space:nowrap}.ti b{font-weight:400;color:var(--himmel);display:block;white-space:nowrap}'
    '.w .ti b{color:var(--betont)}'
    # der Horizont des Sees: eine feine Linie über die ganze Breite unter dem Titel
    '.hz{display:block;align-self:stretch;height:0;border-top:1.5px solid rgba(162,182,207,.55);margin:58px -128px 0}'
    '.w .hz{border-top-color:rgba(15,54,120,.4)}'
    '.da{margin-top:52px;font:400 30px/1.75 M;letter-spacing:.14em;text-transform:uppercase;color:var(--himmel2)}'
    '.w .da{color:var(--betont)}'
    '.sa{margin-top:46px;max-width:780px;font:400 38px/1.45 S;text-wrap:balance;opacity:.9}'
    '.ki2{font:400 26px/1 M;letter-spacing:.16em;text-transform:uppercase;color:var(--himmel);margin-bottom:42px}'
    '.w .ki2{color:var(--betont)}'
    '.zi{font:400 60px/1.3 S;text-wrap:balance;max-width:820px}'
    '.zi::before{content:"«";color:var(--himmel)}.zi::after{content:"»";color:var(--himmel)}'
    '.w .zi::before,.w .zi::after{color:var(--betont)}'
    # Zeiten als Liste: links das Etikett, rechts die Zeit, auf einer Grundlinie
    '.li{margin-top:52px;width:100%;max-width:800px;font:400 30px/1.3 M;letter-spacing:.1em;text-transform:uppercase}'
    '.li p{display:flex;justify-content:space-between;align-items:baseline;gap:24px;padding:20px 0;border-top:1.5px solid rgba(162,182,207,.35);text-align:left}'
    '.li p:last-child{border-bottom:1.5px solid rgba(162,182,207,.35)}'
    '.li span{color:var(--himmel)}.li b{font-weight:400;text-align:right}'
    # Blatt aus der Karte: Gericht in DM Mono gesperrt wie auf der Karte des Hauses, darunter die Zeile, unten der Preis
    '.k{position:absolute;inset:0;background:var(--blatt);color:var(--tinte);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:170px 140px}'
    '.k::before{content:"";position:absolute;inset:86px 96px;border:1.5px solid rgba(15,54,120,.35);border-radius:20px}'
    '.k .z{background:var(--betont)}'
    '.k .ki2{color:var(--betont)}'
    '.k .gn{font:400 76px/1.18 M;letter-spacing:.14em;text-transform:uppercase;text-wrap:balance}'
    '.k .gz{margin-top:40px;font:400 40px/1.45 S;color:rgba(4,16,35,.82);max-width:720px;text-wrap:balance}'
    '.k .hz{border-top-color:rgba(15,54,120,.4);margin:56px -140px 0}'
    '.k .pr{margin-top:46px;font:400 34px/1 M;letter-spacing:.14em;color:var(--betont)}'
    # Blatt mit Bild: das Foto gerahmt auf der Nacht, Name darüber (für Fotos, die nicht hoch genug für einen ganzen Beitrag sind)
    '.a{background:var(--nacht) url(../assets/svg/tapete-a-dunkel.svg) 0 0/336px 336px;color:var(--blatt);justify-content:flex-start;padding-top:300px}'
    '.a .bild{width:100%;border-radius:20px;overflow:hidden;box-shadow:0 0 0 1.5px rgba(162,182,207,.45),0 40px 60px -30px rgba(0,0,0,.7)}'
    '.a .bild img{display:block;width:100%;height:520px;object-fit:cover}'
    '.a .bild.streif img{height:380px}'
    '.a .ti{margin-top:64px;font-size:72px}'
    # Karussell-Deckblatt: Foto randlos, Titel im unteren Drittel auf einem Verlauf der Nacht
    '.fo{position:absolute;inset:0}.fo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
    '.fo::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,29,61,0) 40%,rgba(11,29,61,.9) 100%)}'
    '.fo .tx{position:absolute;left:110px;right:110px;bottom:130px;z-index:2;color:var(--blatt);text-align:left}'
    '.fo .ki{font:400 25px/1 M;letter-spacing:.14em;text-transform:uppercase;color:var(--himmel2);margin-bottom:28px}'
    '.fo .ti{font-size:76px;line-height:1.14}'
    '.fo .wi{position:absolute;top:110px;right:110px;z-index:2;font:400 25px/1 M;letter-spacing:.14em;color:var(--blatt)}'
)


def tafel(zeilen, satz='', fuss='', ton='n', da='', kicker='', liste=None):
    """Schrift-Beitrag auf der Nacht (n) oder dem Papier (w): Zeichen oben, Titel in Versalien (letzte Zeile in Seehimmel), Horizont, Angaben."""
    ti = ''.join(f'<b>{z}</b>' if i == len(zeilen) - 1 else f'<span>{z}</span>' for i, z in enumerate(zeilen))
    li = ('<div class="li">' + ''.join(f'<p><span>{a}</span><b>{b}</b></p>' for a, b in liste) + '</div>') if liste else ''
    return (f'<div class="{ton}"><div class="kop">{_Z}</div>' + (f'<p class="ki2">{kicker}</p>' if kicker else '') + f'<p class="ti">{ti}</p><i class="hz"></i>'
            + (f'<p class="da">{da}</p>' if da else '') + li + (f'<p class="sa">{satz}</p>' if satz else '') + (f'<p class="fu">{fuss}</p>' if fuss else '') + '</div>')


def zitat(satz, wer, ton='w'):
    return f'<div class="{ton}"><div class="kop">{_Z}</div><p class="zi">{satz}</p><p class="fu">{wer}</p></div>'


def karte(kicker, name, zeile, preis):
    return f'<div class="k"><div class="kop">{_Z}</div><p class="ki2">{kicker}</p><p class="gn">{name}</p><p class="gz">{zeile}</p><i class="hz"></i><p class="pr">{preis}</p></div>'


def blatt(key, name, streif=False):
    return f'<div class="a"><div class="kop">{_Z}</div><div class="bild{" streif" if streif else ""}"><img src="{{bild:{quelle(key)}}}" alt=""></div><p class="ti">{name}</p></div>'


def deckblatt(key, kicker, titel, wink):
    return '<div class="fo"><img src="{bild:' + quelle(key) + '}" alt=""><span class="wi">' + wink + '</span><div class="tx"><p class="ki">' + kicker + '</p><p class="ti">' + titel + '</p></div></div>'


F = lambda key, art, fx=.5, fy=.5: dict(art='foto', bild=quelle(key), fx=fx, fy=fy, _art=art)
H = lambda html, art: dict(art='html', html=html, _art=art)
BREIT = 'breit'   # Platzhalter: die drei Beiträge des breiten Bilds (unten zusammen gebaut)

_tort = gericht('TORTELLONI')[1]
_cav_land, _cav = gericht('CAVATELLI')
_kro_gr, _kro = tapas('CROQUETAS')
_lunch = LUNCH['gaenge']
_ferien_kf, _ferien_winter = HJ['ferien']
_kf = HJ['anlaesse'][0]   # Excellence Gourmetkreuzfahrt, 13. bis 15. November 2026 (bevorstehend)
assert _kf['bevorstehend'] and 'Gourmetkreuzfahrt' in _kf['titel']


def chf(g):
    return f"CHF {g['preis']}" + (f" · als Hauptgang {g['haupt']}" if g.get('haupt') else '')


# Die nächsten 48 Beiträge in der Reihenfolge des Postens (1 = zuerst). Im Profil steht der zuletzt gepostete oben links: das Raster ist
# die Liste umgekehrt, Reihe für Reihe zu drei. Termine nur aus haus.json (Kreuzfahrt 13.–15.11., Winterpause 22.12.2026–10.2.2027);
# 16.11.2026 und 21.12.2026 sind Montage, 11.2.2027 ein Donnerstag (Öffnungstage laut haus.json › zeiten).
# Arten für den Nachbar-Abgleich: text (Tafeln, Karte), blatt, teller, mensch, ort, glas.
JAHR = [
    # ---- November 2026: Gourmetkreuzfahrt mit Dieter Koschina, das Haus ist geschlossen
    (H(tafel(['Four Hands', 'an Bord.'], da='13.–15. November 2026', fuss='Excellence Countess · Basel – Strassburg', kicker='Gourmetkreuzfahrt'), 'text'),   # haus.json › anlaesse[0]
     'Four-Hands-Dinner auf der Excellence Countess: Vom 13. bis 15. November geht unsere Küchenchefin Monika Huber mit Dieter Koschina an Bord. Start ist am Freitag in Basel, über Nacht geht es nach Strassburg und am Samstag denselben Weg zurück. Alles zur Reise finden Sie auf excellence.ch.'),
    (F('thon', 'teller', .5, .5), 'Thunfisch in Scheiben, in der gerippten Schale. Mediterran und klar, so kocht das junge Team um Moni Huber.'),
    (F('moni', 'mensch', .5, .3), 'Monika Huber, unsere Küchenchefin. Bei Dieter Koschina hat sie in der Vila Joya an der Algarve viel gelernt, im November kochen die beiden gemeinsam auf dem Schiff.'),
    (F('apero', 'glas', .5, .55), 'Ein Spritz und ein Bier in der blauen Stunde. An der Lästermeile gibt es die Karte den ganzen Tag.'),
    (F('jonas', 'mensch', .5, .3), 'Jonas Volpert, Gastgeber und Sommelier. Der Schwerpunkt seiner Weinkarte liegt auf der Bündner Herrschaft, dem Burgund und der Champagne. Fragen Sie ihn ruhig, was zu Ihrem Teller passt.'),
    (H(tafel(['Wir sind', 'an Bord.'], da='13.–15. November geschlossen', fuss='Ab Montag, 16. November wieder für Sie da', ton='w'), 'text'),   # haus.json › ferien[0], anlaesse[0] text[4]
     'Vom 13. bis 15. November bleibt unsere Wirtschaft geschlossen, denn das ganze Team ist mit an Bord der Excellence Countess. Ab Montag, 16. November sind wir wieder für Sie da.'),
    (F('tortelloni', 'teller', .5, .5), 'Die Tortelloni mit Tomate, Burrata und Taggiasca-Olive. Das Gericht des Hauses, als Vorspeise oder als Hauptgang.'),
    (H(karte('Klassiker', 'Tortelloni', _tort['text'], chf(_tort)), 'text'),   # karte.json › Klassiker › TORTELLONI
     f"Von der Karte: TORTELLONI, {_tort['text'].replace(' – ', ', ')}. {_tort['preis']} Franken als Vorspeise, {_tort['haupt']} Franken als Hauptgang."),
    (F('platanen', 'ort', .5, .6), 'Gedeckt unter den Platanen, dahinter der Hafen. Im Herbst wird es ruhiger auf der Terrasse, der Blick bleibt.'),
    (H(zitat('beeindruckt mit exzellentem Handwerk und klarer kulinarischer Sprache', 'GaultMillau · 15 Punkte', ton='n'), 'text'),   # haus.json › zitat_gm_kueche, auszeichnungen
     '15 Punkte im GaultMillau und «Entdeckung des Jahres 2026» für Moni Huber. Danke an alle, die jeden Tag mit in der Küche und am Pass stehen.'),
    (F('team', 'mensch', .5, .45), '«Mehr Wirtschaft, weniger feine Pinkel», hat das Tagblatt über uns geschrieben. Wir nehmen das als Kompliment. Das ist unser Team.'),
    (H(tafel(['Lunch.', 'Drei Gänge.'], da=f"CHF {LUNCH['preis_zahl']}", satz=' · '.join(g['name'] for g in _lunch), fuss=f"Mittags · Küche {Z['kueche'][0]}", ton='w'), 'text'),   # lunch.json, haus.json › zeiten
     f"Unser Lunch-Menü: {_lunch[0]['name']} mit {_lunch[0]['text'].replace(' – ', ' und ')}, {_lunch[1]['name']} mit {_lunch[1]['text'].replace(' – ', ', ')}, zum Schluss {_lunch[2]['name']} mit {_lunch[2]['text']}. Drei Gänge für {LUNCH['preis_zahl']} Franken."),
    (F('suppe', 'teller', .5, .6), 'Grüne Suppe in der blauen Schale. Für einen kühlen Mittag am See.'),
    (H(tafel(['Die', 'Lästermeile.'], satz='Ein Glas, ein paar Tapas und der Blick auf den Bootshafen.', fuss='Tapas durchgehend'), 'text'),   # laestermeile.json, haus.json › zitat_gm_laester
     'An der Lästermeile sitzen Sie in der Reihe, schauen auf den Bootshafen und die Promenade und lästern ein wenig. Pimientos de Padrón, Croquetas, Kalamata Oliven: Die Tapas gibt es den ganzen Tag.'),
    (F('regal', 'ort', .32, .5), 'Die Flaschen stehen an der Scheibe, dahinter liegt der See. An der Lästermeile.'),
    (H(karte(_cav_land, 'Cavatelli', _cav['text'], chf(_cav)), 'text'),   # karte.json › Italien › CAVATELLI (Speisekarte Oktober)
     f"Von der Karte im Oktober: CAVATELLI, {_cav['text'].replace(' – ', ', ')}. Als Vorspeise oder als Hauptgang, auf Wunsch auch vegetarisch."),
    (F('glas', 'glas', .45, .5), 'Ein Glas Weisswein, dahinter nur noch der See.'),
    (F('fisch', 'teller', .5, .5), 'Ein Fischfilet mit Sauce in der gerippten Schale, dahinter ein blauer Stuhl der Terrasse.'),
    (H(blatt('fliesen', 'Zementfliesen', streif=True), 'blatt'),
     'Die Zementfliesen an der Bar. Wer an der Lästermeile steht, hat sie unter den Füssen.'),
    (F('gaststube', 'ort', .42, .5), 'Die Gaststube mit den grossen Fenstern zum Hafen. Wenn es draussen kühler wird, sitzen Sie hier mit demselben Blick.'),
    # ---- Advent: Banketts, Gutschein, die Terrasse, dann die Winterpause
    (H(tafel(['Ihre Feier', 'am See.'], da=f"Zwei Etagen · je bis zu {HJ['bankett']['personen']} Personen", fuss='Tavolata oder gesetztes Menue'), 'text'),   # haus.json › bankett
     f"Das Weihnachtsessen mit der Firma, ein runder Geburtstag, die Familie am Tisch: Wir haben auf zwei Etagen Platz für jeweils bis zu {HJ['bankett']['personen']} Personen. Sie geben den Rahmen vor, ob Tavolata oder gesetztes Menue. Schreiben Sie uns, dann besprechen wir alles in Ruhe."),
    (F('lounge', 'ort', .4, .5), 'Die Lounge am Ufer, dahinter der See und die Alpen.'),
    (H(tafel(['Ein Abend', 'am See.'], satz='Zum Verschenken: unser Gutschein, den Betrag wählen Sie.', fuss='schloessli-bottighofen.ch', ton='w', kicker='Gutschein'), 'text'),   # haus.json › gutschein
     'Noch ein Geschenk gesucht? Mit unserem Gutschein verschenken Sie einen Abend am Hafen von Bottighofen. Den Betrag wählen Sie selbst, bestellen können Sie ihn auf unserer Website.'),
    (F('dessert', 'teller', .5, .55), 'Zum Schluss etwas Süsses mit Beeren, auf dem blauen Teller.'),
    BREIT, BREIT, BREIT,   # 25–27: das breite Bild der Terrasse, rechts zuerst gepostet, damit es im Profil von links nach rechts steht
    (H(tafel(['Winterpause.'], da='22.12.2026 – 10.2.2027', satz='Bis Montag, 21. Dezember sind wir für Sie da.', fuss='Danke für dieses Jahr am See'), 'text'),   # haus.json › ferien[1]
     'Bis Montag, 21. Dezember sind wir noch für Sie da, dann macht das Team Ferien. Vom 22. Dezember 2026 bis 10. Februar 2027 bleibt die Wirtschaft geschlossen. Danke für dieses Jahr am See.'),
    (F('abend', 'ort', .3, .5), 'Ein Abend unter der Platane, die Lichterkette brennt. Danke, dass Sie da waren.'),
    # ---- Winterpause: Geschichte, Menschen, Teller
    (H(tafel(['Statt eines Schilds', 'ein Besen.'], fuss='Am Hafen · Ende 17. Jahrhundert', ton='w', kicker='Aus der Geschichte'), 'text'),   # haus.json › besen (Quelle: Munz-Schaufelberger 1994)
     'Aus der Geschichte am Hafen: Gleich nebenan, im Haus am See, das heute Schlössli heisst, setzte Hans Conrad Hafen Ende des 17. Jahrhunderts einen Wirt ein, der die Schiffsleute mit Speis und Trank bewirtete. Statt eines Wirtshausschilds hing nur ein Besen heraus.'),
    (F('pasta', 'teller', .5, .5), 'Schwarze Pasta mit Garnelen und Meeresfrüchten.'),
    (H(tafel(['Aus Südtirol', 'an den See.'], satz='Vila Joya an der Algarve, Taverne zum Schäfli, seit April 2025 die eigene Küche am Hafen.', fuss='Monika Huber · Küchenchefin'), 'text'),   # haus.json › weg_moni
     HJ['weg_moni']),
    (F('lukas', 'mensch', .5, .3), 'Lukas Siebel, Sous-Chef, an der Seite von Moni Huber.'),
    (H(karte(_kro_gr, 'Croquetas', _kro['text'].replace(' G/L/E', ''), f"CHF {_kro['preis']}"), 'text'),   # laestermeile.json › Tapas durchgehend › CROQUETAS
     f"Von der Karte der Lästermeile: CROQUETAS, Pata-Negra-Kroketten für {_kro['preis']} Franken. Dazu ein Glas, und der Nachmittag am Hafen gehört Ihnen."),
    (F('schild', 'ort', .5, .5), 'Unser Schild zeigt den Weg: zur Restaurant-Terrasse und zur Lästermeile.'),
    (F('anguria', 'teller', .5, .5), 'Von oben gesehen, auf dem blauen Platzteller.'),
    (H(blatt('bar', 'An der Bar'), 'blatt'), 'An der Bar wird ein Bier gezapft, unter der Theke die Zementfliesen.'),
    (F('fleisch', 'teller', .5, .5), 'Gefülltes Fleisch mit Blättern und Blüten auf dem geriffelten Teller.'),
    # ---- Februar 2027: wieder offen, der Frühling am See
    (H(tafel(['Ab 11. Februar', 'wieder da.'], da=f"Do – Mo · {Z['offen'].replace(' Uhr', '')}", fuss=Z['ruhetag']), 'text'),   # haus.json › ferien[1], zeiten
     'Die Ferien sind vorbei: Ab Donnerstag, 11. Februar 2027 sind wir wieder für Sie da. Donnerstag bis Montag von 11:30 bis 23:00 Uhr, Dienstag und Mittwoch ist Ruhetag. Wir freuen uns auf Sie.'),
    (F('iberia', 'teller', .5, .5), 'Fisch in grüner Sauce in der gerippten Schale, daneben ein Glas Wein.'),
    (H(zitat('mit der Terrasse im Schatten prächtiger Platanen und Blick auf den Bodensee', 'GaultMillau'), 'text'),   # haus.json › zitat_gm_terrasse
     f'Bald wieder draussen: GaultMillau schreibt von unserer «Terrasse im Schatten prächtiger Platanen und Blick auf den Bodensee». Reservieren Sie Ihren Tisch auf unserer Website oder unter {TEL}.'),
    (F('torte', 'teller', .5, .5), 'Schichttorte mit Beeren auf dem blauen Teller.'),
    (H(tafel(['Unsere', 'Zeiten.'], liste=[('Do – Mo', Z['offen'].replace(' Uhr', '')), ('Küche', Z['kueche'][0].replace(' Uhr', '')), ('', Z['kueche'][1].replace(' Uhr', '')), ('Lästermeile', 'durchgehend')], fuss=Z['ruhetag']), 'text'),   # haus.json › zeiten
     'Damit Sie planen können: Donnerstag bis Montag ab 11:30 Uhr offen, die Küche kocht von 11:30 bis 13:30 und von 18:00 bis 20:00 Uhr. Die Karte der Lästermeile gibt es den ganzen Tag. Dienstag und Mittwoch ist Ruhetag.'),
    (F('sauce', 'teller', .5, .5), 'Die Sauce wird mit dem Löffel angegossen. Am Pass zählt jeder Handgriff.'),
    (H(tafel(['Ihr Tisch', 'am Hafen.'], da=TEL, fuss='Reservation auf schloessli-bottighofen.ch', ton='w'), 'text'),   # haus.json › telefon, reservation
     f'Ihr Tisch am Hafen: Reservieren Sie auf unserer Website oder rufen Sie uns an, {TEL}. Wir freuen uns auf Sie.'),
    (F('wein', 'glas', .5, .5), 'Die Weinkarte von Jonas Volpert hat 26 Seiten. GaultMillau schreibt: «Der Weinkeller, bei vielen neuen Lokalen das Sorgenkind, ist im ‹Schlössli› bestens bestückt.»'),
    (H(tafel(['Favorit der', 'Inspektoren.'], fuss='Guide Michelin · Falstaff 91 von 100'), 'text'),   # haus.json › auszeichnungen
     'Der Guide Michelin nennt uns «Favorit der Inspektoren», Falstaff gibt 91 von 100 Punkten. Am meisten freut uns trotzdem, wenn Sie wiederkommen.'),
    (F('salat', 'teller', .5, .5), 'Ein Salat auf dem gerippten silbernen Teller. Der Frühling kommt auch auf die Karte.'),
]
assert len(JAHR) == 48, len(JAHR)

_RASTER = list(reversed(JAHR))
FEED = [_RASTER[i:i + 3] for i in range(0, 48, 3)]
_BREIT_TEXTE = [   # im Raster von links nach rechts (gepostet: rechts zuerst)
    'Direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen. Das ganze Bild sehen Sie in unserem Profil, über drei Beiträge.',
    'Die blauen Stühle der Terrasse am Mittag. Aus diesem Bild stammen die Farben unseres Hauses: das Blau der Stühle, der See, der Himmel.',
    '«Die schönste Terrasse am Bodensee», sagt Christian Kuchler.',
]


def _art(x):
    return 'breit' if x == BREIT else x[0]['_art']


def nachbarn():
    """Tafeln und Blätter nie nebeneinander oder untereinander; gleiche Art nie nebeneinander oder untereinander."""
    art = [[_art(x) for x in r] for r in FEED]
    schrift = {'text'}   # ein Blatt (Foto gerahmt auf der Nacht) darf neben einer hellen Tafel stehen, nie neben einem zweiten Blatt
    fehler = []
    for r in range(len(art)):
        for c in range(3):
            a = art[r][c]
            for rr, cc in ((r, c + 1), (r + 1, c)):
                if rr < len(art) and cc < 3:
                    b = art[rr][cc]
                    if a == 'breit' and b == 'breit':
                        continue
                    if a == b or (a in schrift and b in schrift):
                        fehler.append((r + 1, c + 1, a, rr + 1, cc + 1, b))
    return fehler


BESTAND_AUSNAHMEN = ()
BESTAND_KANDIDATEN = []
BOGEN = []
for _r, _reihe in enumerate(FEED):
    if _reihe[0] == BREIT:
        assert _reihe == [BREIT] * 3
        BOGEN.append(dict(id=f'{_r + 1:02d}1-start', r=_r, c=0, w=3, art='foto', bild=quelle('start'), fx=.5, fy=.42, texte=list(_BREIT_TEXTE)))
        continue
    for _c, (st, text) in enumerate(_reihe):
        st = {k: v for k, v in st.items() if k != '_art'}
        kurz = (os.path.basename(st['bild']).rsplit('-', 1)[0] if st['art'] == 'foto' else re.sub(r'\W+', '', re.sub(r'<[^>]+>', ' ', st['html']))[:14] or 'tafel')
        BOGEN.append(dict(id=f'{_r + 1:02d}{_c + 1}-{kurz}', r=_r, c=_c, texte=[text], **st))
P = feed_bogen.p_liste(BOGEN)
BISHER = 46   # Beiträge auf @schloessli_bottighofen heute (Profil, 19.10.2026); im Profil der Werkbank stehen die erreichbaren darunter
PROFIL['zahlen']['beitraege'] = str(len(P) + BISHER)
BESTAND_KANDIDATEN = sorted(k for k in json.load(open(os.path.join(_INHALT, 'bilder.json'), encoding='utf-8')) if not k.startswith('ig-') and glob.glob(os.path.join(_WEB, 'assets', 'img', k + '-*.webp')))
# Instagram-Bestand des Hauses für den Abgleich (_quelle/extern/ig/ig-NN.jpg, nur beim Bau, nie zur Laufzeit)
IG_BESTAND = ['../../_quelle/extern/ig/*.jpg']

if __name__ == '__main__':
    print(len(P), 'Beiträge,', len(FEED), 'Reihen; Nachbarn:', nachbarn() or 'in Ordnung')
