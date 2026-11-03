#!/usr/bin/env python3
"""Wirtschaft am Schlössli: zehn Mails an Gäste im Ton des Hauses, als Idee zum Entwurf (Nachtbau 3./4.11.2026, Agent schloessli-werkbank-feed).
Bauart und Übersicht vom Culinarium (mails/_src/bau.py, elf Mails, Band mit «Ganze Mail»), Wortlaut und Kleid vom Schlössli: die drei Mails vom
19.10.2026 (Reservation, Bankett, Gutschein, website/_alt.vor-nachtbau-2026-11-03/mails/_src/bau.py) und sieben neue.

  01 Reservation bestätigt     02 Tisch auf der Terrasse     03 Bankett-Anfrage      04 Gutschein          05 Winterpause
  06 Gourmetkreuzfahrt         07 Lunch                      08 Weinempfehlung       09 Danke nach dem Besuch   10 Warteliste
Im Sie wie das Haus, Schweizer Schreibung (ss), «…». Kopf mit dem Zeichen (die Zeiger) und der Wortmarke als PNG (mails/_src/aufnahme.js).
Echter Text oben, Fotos mit Beschreibung und unter 100 KB, lesbar auch mit gesperrten Bildern; Tabellen und feste Stile, Titel in Arial in
Versalien wie die Wortmarke (Mailprogramme laden Open Sans nicht). Angaben des Hauses aus website/inhalt/*.json; Namen, Daten und Nummern der
Gäste sind Beispielwerte und so beschriftet. Wortlaut von Tasty Studios, als Vorschlag. Gebaut, nie verschickt.

Aufruf:  python3 mails/_src/bau.py  → mails/NN-<fall>/index.html, mails/index.html, mails/img/;  danach WB_PORT=9288 node mails/_src/aufnahme.js"""
import glob, html, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__)); MAILS = os.path.dirname(HIER); ROOT = os.path.dirname(MAILS); WEB = os.path.dirname(ROOT)
from PIL import Image  # noqa: E402
_I = lambda n: json.load(open(os.path.join(WEB, 'inhalt', n), encoding='utf-8'))
HJ, BK, LU, WEIN, KA = _I('haus.json'), _I('bankett.json'), _I('lunch.json'), _I('wein.json'), _I('karte.json')

e = html.escape
STUHL, NACHT, TIEF, PAPIER, BLATT, TINTE, HIMMEL, HIMMEL2, SPIEGEL, BETONT = '#113d88', '#0b1d3d', '#0A234C', '#e7ecf3', '#f4f6f9', '#041023', '#a2b6cf', '#c5d2e1', '#d0dae7', '#0f3678'
TITEL = "Arial,'Helvetica Neue',Helvetica,sans-serif"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
ADRESSE = f"{HJ['strasse']} · {HJ['ort']}"
TEL = HJ['telefon'].replace(' ', ' ')   # Nummer bricht nicht um
Z = HJ['zeiten']
GRUSS = 'Monika Huber, Jonas Volpert und das Team'
STAND = '03.11.2026'
_herbst = next(m for m in BK['menues'] if m['name'] == 'Herbst')
_kf = HJ['anlaesse'][0]; assert 'Gourmetkreuzfahrt' in _kf['titel']


def _wein(region, erzeuger):
    for g in WEIN['gruppen']:
        for r in g['regionen']:
            if r['titel'] == region:
                for x in r['erzeuger']:
                    if x['name'].startswith(erzeuger):
                        w = x['weine'][0]; f = w['flaschen'][0]
                        return dict(erzeuger=x['name'], wein=f"{w['jahr'] or ''} {w['name']}".strip(), gross=f['gross'].replace('.', ','), preis=f['preis'])
    raise KeyError(erzeuger)


_W = _wein('Bündner Herrschaft', 'Weinkellerei Giani Boner')   # wein.json › Rotwein › Bündner Herrschaft
_tort = next(g for l in KA['laender'] for g in l['gerichte'] if g['name'] == 'TORTELLONI')
_LG = LU['gaenge']

FAELLE = [
    dict(nr='01', wann='Wenn das Haus den Tisch bestätigt', ordner='01-reservation', name='Ihre Reservation', satz='Kommt, sobald das Haus den Tisch bestätigt: Tag, Uhrzeit, Personen, Platz und der Weg zum Hafen.',
         betreff='Ihr Tisch am Hafen ist bestätigt', titel=('Ihr Tisch', 'am Hafen.'), foto=('platanen', 'Gedeckte Tische unter den Platanen der Terrasse, dahinter der Hafen'),
         text=['Liebe Frau Keller', 'Vielen Dank für Ihre Reservation. Ihr Tisch ist bestätigt, wir freuen uns auf Sie.',
               'Die ganze Karte finden Sie schon jetzt auf unserer Seite. Haben Sie eine Allergie oder feiern Sie etwas, schreiben Sie es uns gern als Antwort auf diese Mail.',
               f'Kommt etwas dazwischen, erreichen Sie uns unter {TEL}.'],
         karte=('Ihre Reservation', [('Tag', 'Samstag, 28. November 2026'), ('Uhrzeit', '19:00 Uhr'), ('Personen', '2'), ('Platz', 'Gaststube, am Fenster')]),
         knopf=('Die Karte ansehen', 'karte.html'), dazu=HJ['anfahrt']),
    dict(nr='02', wann='Wenn ein Gast draussen sitzen möchte', ordner='02-terrasse', name='Tisch auf der Terrasse', satz='Kommt, wenn ein Gast ausdrücklich draussen sitzen möchte: der Tisch auf der Terrasse, und was das Haus macht, wenn das Wetter nicht mitspielt.',
         betreff='Ihr Tisch auf der Terrasse', titel=('Ihr Tisch', 'auf der Terrasse.'), foto=('start', 'Blaue Stühle auf der Terrasse am Mittag, dahinter der Bodensee und die Alpen'),
         text=['Lieber Herr Brunner', 'Sie möchten draussen sitzen, mit Blick aufs Wasser und die Alpen. Wir haben Ihnen einen Tisch auf der Terrasse reserviert.',
               'Spielt das Wetter nicht mit, rufen wir Sie am Vormittag an und decken für Sie in der Gaststube, mit den grossen Fenstern zum Hafen.'],
         karte=('Ihre Reservation', [('Tag', 'Freitag, 21. Mai 2027'), ('Uhrzeit', '12:00 Uhr'), ('Personen', '4'), ('Platz', 'Terrasse')]),
         knopf=('Die Karte ansehen', 'karte.html'), dazu=f"{Z['tage']}, {Z['offen']}. {Z['ruhetag']}."),
    dict(nr='03', wann='Gleich nach der Bankettanfrage', ordner='03-bankett', name='Ihr Bankett', satz='Kommt nach der Bankettanfrage: Datum, Personen, Speisenform und Menü, und der Satz, dass das Haus sich persönlich meldet.',
         betreff='Ihre Bankettanfrage ist bei uns', titel=('Ihr Fest', 'am See.'), foto=('lounge', 'Die Lounge am Ufer, dahinter der See und die Alpen'),
         text=['Lieber Herr Brunner', 'Vielen Dank für Ihre Anfrage. Wir melden uns persönlich, besprechen mit Ihnen das Menü und richten uns nach Ihnen und Ihren Wünschen.',
               HJ['bankett']['platz'],
               'Gibt es Allergien oder ein Gericht, das auf keinen Fall fehlen darf, schreiben Sie es uns gern noch dazu.'],
         karte=('Ihre Anfrage', [('Datum', 'Freitag, 11. Dezember 2026'), ('Personen', '24'), ('Speisenform', 'Gesetztes Menue'), ('Menü', f"{_herbst['name']}, CHF {_herbst['preis']} je Person")]),
         knopf=('Die Bankettmenüs ansehen', 'feiern.html'), dazu=f'Für Fragen erreichen Sie uns unter {TEL}.'),
    dict(nr='04', wann='Nach der Bestellung des Gutscheins', ordner='04-gutschein', name='Ihr Gutschein', satz='Kommt nach der Bestellung des Gutscheins. Die Karte selbst hängt als PDF an der Mail.',
         betreff='Ihr Gutschein für die Wirtschaft am Schlössli', titel=('Ihr Gutschein', 'ist da.'), foto=('glas', 'Ein Glas Weisswein und ein Wasserglas vor dem See'),
         text=['Liebe Frau Keller', 'Vielen Dank. Ihr Gutschein hängt als PDF an dieser Mail, mit Ihrem Satz darauf. Drucken Sie ihn aus oder schicken Sie ihn weiter.',
               'Eingelöst wird er bei uns am Hafen, im Restaurant und an der Lästermeile.'],
         karte=('Ihr Gutschein', [('Für', 'Anna und Luca'), ('Von', 'Mama'), ('Betrag', 'CHF 150'), ('Satz', '«Ein Abend am See»')]),
         knopf=('Einen Tisch reservieren', 'index.html'), dazu=f'Fragen dazu beantworten wir gern unter {TEL}.'),
    dict(nr='05', echt=True, wann='Vor der Winterpause, an Gäste mit Reservation', ordner='05-winterpause', name='Unsere Winterpause', satz='Geht vor den Ferien an Gäste, die schon reserviert haben oder bald kommen möchten: wann zu ist, bis wann noch offen, wann es weitergeht.',
         betreff='Unsere Winterpause', titel=('Bis bald', 'am See.'), foto=('abend', 'Abend unter der Platane mit Lichterkette, Gäste am Tisch über dem See'),
         text=['Liebe Frau Keller', f"Bald macht unser Team Ferien: Vom {HJ['ferien'][1].replace(' - ', ' bis ')} bleibt die Wirtschaft am Schlössli geschlossen.",
               'Bis Montag, 21. Dezember sind wir noch für Sie da, mittags und abends. Ab Donnerstag, 11. Februar 2027 decken wir wieder für Sie.',
               'Noch ein Geschenk gesucht? Unser Gutschein lässt sich auch in den Ferien bestellen.'],
         karte=('Ferien', [('Geschlossen', '22. Dezember 2026 bis 10. Februar 2027'), ('Letzter Tag', 'Montag, 21. Dezember'), ('Wieder offen', 'Donnerstag, 11. Februar 2027')]),
         knopf=('Gutschein bestellen', 'gutschein.html'), dazu=f"{Z['tage']}, {Z['offen']}. {Z['ruhetag']}."),
    dict(nr='06', echt=True, wann='An Gäste der Liste, vor der Gourmetkreuzfahrt', ordner='06-kreuzfahrt', name='Ein Wochenende auf dem Rhein', satz='Geht an Gäste, die gern von Anlässen hören: die Gourmetkreuzfahrt mit Dieter Koschina, wann und wo, und dass das Haus in den drei Tagen zu ist.',
         betreff='Four-Hands-Dinner auf der Excellence Countess', titel=('Four Hands', 'an Bord.'), foto=('moni', 'Monika Huber, Küchenchefin, auf der Terrasse'),
         text=['Lieber Herr Brunner', 'Gemeinsam mit einem ihrer grossen Mentoren, Dieter Koschina, bei dem unsere Küchenchefin Monika Huber in der Vila Joya an der Algarve viel gelernt hat, geht es an Bord der Excellence Countess.',
               'Start ist am Freitag in Basel, über Nacht geht es nach Strassburg, am Samstag denselben Weg zurück. Welcome-Apéro, Live-Musik, Gala-Dinner und DJ.',
               'Unser Restaurant ist über diese drei Tage geschlossen, denn das ganze Team ist mit an Bord. Die Reise buchen Sie direkt bei Excellence.'],
         karte=('Die Reise', [('Wann', _kf['zeit']), ('Schiff', 'Excellence Countess'), ('Strecke', 'Basel – Strassburg – Basel')]),
         knopf=('Zu den Anlässen', 'anlaesse.html'), dazu='Ab Montag, 16. November sind wir wieder am Hafen für Sie da.'),
    dict(nr='07', echt=True, wann='Wenn es ein neues Lunch-Menü gibt', ordner='07-lunch', name='Unser Lunch', satz='Geht an Gäste aus der Nähe, wenn es ein neues Lunch-Menü gibt: die drei Gänge, der Preis und die Zeiten der Küche am Mittag.',
         betreff='Unser Lunch, mittags am See', titel=('Mittags', 'am See.'), foto=('suppe', 'Grüne Suppe in einer blauen Schale'),
         text=['Liebe Frau Keller', f'Für die Mittagspause am Hafen gibt es bei uns ein Lunch-Menü: drei Gänge für {LU["preis_zahl"]} Franken.',
               f"Die Küche kocht mittags von {Z['kueche'][0]}. Wer wenig Zeit hat, sagt es uns beim Bestellen."],
         karte=('Lunch-Menü', [(g['name'], g['text']) for g in _LG] + [('Preis', f"CHF {LU['preis_zahl']}, drei Gänge")]),
         knopf=('Die Karte ansehen', 'karte.html#mittag'), dazu=f"{Z['tage']}, {Z['ruhetag']}."),
    dict(nr='08', wann='Wenn ein Gast nach einem Wein gefragt hat', ordner='08-wein', name='Eine Weinempfehlung', satz='Antwort von Jonas Volpert, wenn ein Gast nach einem Wein gefragt hat: Weingut, Jahrgang, Flasche und Preis aus der Weinkarte.',
         betreff='Der Wein von Ihrem Abend', titel=('Der Wein', 'von Ihrem Abend.'), foto=('wein', 'Weinflaschen im Regal'),
         text=['Lieber Herr Brunner', 'Sie haben nach dem Pinot Noir gefragt, den wir Ihnen zu den Tortelloni eingeschenkt haben. Hier ist er, so wie er auf unserer Weinkarte steht.',
               'Der Schwerpunkt unserer Karte liegt auf der Bündner Herrschaft, dem Burgund und der Champagne. Möchten Sie beim nächsten Besuch etwas anderes probieren, sagen Sie es mir einfach am Tisch.',
               'Herzlich, Jonas Volpert, Gastgeber und Sommelier'],
         karte=('Aus der Weinkarte', [('Weingut', _W['erzeuger']), ('Wein', _W['wein']), ('Flasche', f"{_W['gross']}, CHF {_W['preis']}"), ('Gericht', f"Tortelloni, {_tort['text']}")]),
         knopf=('Die Weinkarte ansehen', 'weinkarte.html'), dazu='Gericht und Gast sind Beispielwerte, Wein und Preis stehen so auf der Weinkarte.'),
    dict(nr='09', wann='Am Tag nach dem Besuch', ordner='09-danke', name='Danke für Ihren Besuch', satz='Kommt am Tag nach dem Besuch: ein Dank, die Bitte um ein Wort und der Weg zum nächsten Tisch.',
         betreff='Danke für Ihren Besuch am Hafen', titel=('Danke', 'für Ihren Besuch.'), foto=('dessert', 'Dessert mit Beeren auf einem blauen Teller, dahinter ein Wasserglas'),
         text=['Liebe Frau Keller', 'Schön, dass Sie gestern bei uns am Hafen waren. Wir hoffen, Sie haben den Abend am See genossen.',
               'Hat Ihnen etwas besonders gefallen, oder gibt es etwas, das wir besser machen können? Antworten Sie einfach auf diese Mail, wir lesen jede.'],
         karte=('Ihr Besuch', [('Tag', 'Samstag, 28. November 2026'), ('Personen', '2'), ('Platz', 'Gaststube, am Fenster')]),
         knopf=('Wieder reservieren', 'index.html'), dazu=f"Bis zum nächsten Mal, {Z['tage']} ab 11:30 Uhr."),
    dict(nr='10', wann='Wenn der Wunschtermin ausgebucht ist', ordner='10-warteliste', name='Auf der Warteliste', satz='Kommt, wenn der Wunschtermin ausgebucht ist: der Gast steht auf der Warteliste, und wird ein Tisch frei, ruft das Haus an.',
         betreff='Sie stehen auf unserer Warteliste', titel=('Sie stehen', 'auf der Liste.'), foto=('gaststube', 'Die Gaststube mit grossen Fenstern zum Hafen'),
         text=['Lieber Herr Brunner', 'Vielen Dank für Ihre Anfrage. An Ihrem Wunschtermin sind wir leider schon ausgebucht. Wir haben Sie auf unsere Warteliste gesetzt.',
               'Wird ein Tisch frei, rufen wir Sie an. An der Lästermeile gibt es die Tapas den ganzen Tag, vielleicht passt ein Glas am Nachmittag.'],
         karte=('Ihr Wunsch', [('Tag', 'Samstag, 5. Dezember 2026'), ('Uhrzeit', '19:00 Uhr'), ('Personen', '6')]),
         knopf=('Einen anderen Tag wählen', 'index.html'), dazu=f'Ändert sich etwas, erreichen Sie uns unter {TEL}.'),
]


def _bild(key):
    b = sorted(int(m.group(1)) for p in glob.glob(os.path.join(WEB, 'assets', 'img', key + '-*.webp')) if (m := re.fullmatch(re.escape(key) + r'-(\d+)\.webp', os.path.basename(p))))
    return os.path.join(WEB, 'assets', 'img', f'{key}-{[x for x in b if x <= 1800][-1]}.webp')


def bilder():
    """Fotos 1000 px, unter 100 KB (Qualität sinkt, bis es passt). Quelle: Bildregister der Website."""
    os.makedirs(os.path.join(MAILS, 'img'), exist_ok=True)
    for f in FAELLE + [dict(foto=('team', ''))]:
        key = f['foto'][0]
        im = Image.open(_bild(key)).convert('RGB'); w, h = im.size; nh = round(w * 9 / 16)
        if nh < h:
            y = round((h - nh) * (.35 if key in ('moni', 'team') else .5)); im = im.crop((0, y, w, y + nh))
        im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
        z = os.path.join(MAILS, 'img', key + '.jpg')
        for br, qu in ((1000, 80), (1000, 72), (1000, 64), (900, 66), (820, 64), (760, 62)):
            k = im.resize((br, round(im.height * br / im.width)), Image.LANCZOS) if br < im.width else im
            k.save(z, quality=qu, optimize=True, progressive=True)
            if os.path.getsize(z) < 100_000:
                break
    alt = {f['foto'][0] + '.jpg' for f in FAELLE} | {'team.jpg', 'zeichen.png', 'wortmarke.png'}
    for d in os.listdir(os.path.join(MAILS, 'img')):   # Bilder früherer Fassungen weg
        if d not in alt:
            os.remove(os.path.join(MAILS, 'img', d))


def fest(t):
    """Titelzeile: die letzten zwei Wörter fest verbunden, damit nie ein Wort allein in der letzten Zeile steht (Kriterium 7)."""
    w = e(t).rsplit(' ', 1)
    return '&nbsp;'.join(w)


def mail(f, basis):
    """basis: Adresse der Website, relativ aus dem Ordner der Mail (Vorschau) oder voll (Versand)."""
    zeilen = ''.join(f'<tr><td style="padding:11px 12px 11px 0;border-top:1px solid #2a4f8f;font:400 11px/1.3 {SANS};letter-spacing:.14em;text-transform:uppercase;color:{HIMMEL};width:34%;vertical-align:top">{e(k)}</td>'
                     f'<td style="padding:11px 0;border-top:1px solid #2a4f8f;font:400 16px/1.35 {SANS};color:{BLATT}">{e(v)}</td></tr>' for k, v in f['karte'][1])
    absaetze = f'<p style="margin:0 0 14px;font:400 20px/1.3 {SANS};color:{TINTE}">{e(f["text"][0])}</p>' + ''.join(
        f'<p style="margin:0 0 14px;font:400 16px/1.62 {SANS};color:#22324d">{e(t)}</p>' for t in f['text'][1:])
    return f'''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>{e(f['betreff'])} · Wirtschaft am Schlössli</title></head>
<body style="margin:0;padding:0;background:{PAPIER}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{PAPIER}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:{BLATT};border-radius:22px;overflow:hidden">
  <tr><td align="center" style="background:{STUHL};padding:34px 30px 30px">
    <img src="../img/zeichen.png" width="54" alt="" style="display:block;border:0;width:54px;height:auto;margin:0 auto 18px">
    <img src="../img/wortmarke.png" width="300" alt="Wirtschaft am Schlössli" style="display:block;border:0;width:300px;max-width:78%;height:auto;margin:0 auto">
    <div style="margin:10px 0 0;font:400 10.5px/1.2 {SANS};letter-spacing:.24em;text-transform:uppercase;color:{HIMMEL}">Bottighofen · am Bodensee</div>
    <div style="height:0;border-top:1px solid rgba(162,182,207,.45);margin:26px -30px 0"></div>
    <h1 style="margin:26px 0 0;font:400 clamp(24px,7vw,32px)/1.2 {TITEL};letter-spacing:.12em;text-transform:uppercase;color:{BLATT}">{fest(f['titel'][0])}<br><span style="color:{HIMMEL2}">{fest(f['titel'][1])}</span></h1>
  </td></tr>
  <tr><td style="padding:34px clamp(22px,6vw,40px) 8px">{absaetze}</td></tr>
  <tr><td style="padding:6px 28px 6px"><img src="../img/{f['foto'][0]}.jpg" width="544" alt="{e(f['foto'][1])}" style="display:block;border:0;width:100%;height:auto;border-radius:16px"></td></tr>
  <tr><td style="padding:10px 28px 6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{NACHT};border-radius:16px">
    <tr><td style="padding:22px 26px 12px"><div style="font:400 10.5px/1.2 {SANS};letter-spacing:.2em;text-transform:uppercase;color:{HIMMEL};padding-bottom:12px">{e(f['karte'][0])}{'' if f.get('echt') else ' · Beispielwerte'}</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{zeilen}</table></td></tr></table></td></tr>
  <tr><td align="center" style="padding:26px 40px 8px"><a href="{basis}{f['knopf'][1]}" style="display:inline-block;padding:16px 30px;border-radius:999px;background:{STUHL};font:400 12px/1 {SANS};letter-spacing:.16em;text-transform:uppercase;color:{BLATT};text-decoration:none">{e(f['knopf'][0])} &nbsp;↗</a></td></tr>
  <tr><td style="padding:14px 40px 30px"><p style="margin:0;font:400 15px/1.6 {SANS};color:#3a4c69;text-align:center">{e(f['dazu'])}</p>
    <img src="../img/team.jpg" width="520" alt="Das Team der Wirtschaft am Schlössli vor der Holzwand" style="display:block;border:0;width:100%;max-width:520px;height:auto;margin:26px auto 0;border-radius:16px">
    <p style="margin:16px 0 0;font:400 17px/1.4 {SANS};color:{TINTE};text-align:center">Herzlich, {e(GRUSS)}</p></td></tr>
  <tr><td align="center" style="background:{TIEF};padding:26px 30px"><div style="font:400 12px/1.4 {TITEL};letter-spacing:.24em;color:{BLATT}">WIRTSCHAFT AM SCHLÖSSLI</div>
    <div style="margin-top:8px;font:400 13px/1.6 {SANS};color:{HIMMEL2}">{e(ADRESSE)}<br>{e(TEL)} · {e(HJ['mail'])}</div></td></tr>
</table>
</td></tr></table>
</body></html>
'''


def eingebettet(f):
    """Die Mail steht direkt in der Seite (Robert 18.10.2026: kein eingebettetes Fenster). Dieselbe Mail wie im Ordner, nur die Bildwege von hier aus."""
    t = mail(f, '../')
    t = t[t.index('<body'):]; t = t[t.index('>') + 1:t.rindex('</body>')]
    return t.replace('src="../img/', 'src="img/')


def uebersicht():
    # Robert 18.10.2026 (Website-Master Punkt 15): Mails nebeneinander im Band, obere Hälfte mit weichem Auslauf, «Ganze Mail» auf und zu,
    # Nummer, Titel, Absender und Wann darüber; Pfeile am Laptop, am Handy eine nach der anderen
    pf = lambda d: f'<svg viewBox="0 0 16 16" aria-hidden="true"><path d="{d}"/></svg>'
    karten = ''.join(f'''<article class="mb hr" style="--i:{min(i, 4)}">
  <header class="mb-ueber"><span class="mb-nr">{f['nr']}</span><span class="mb-ueber__t"><b>{e(f['name'])}</b><small><span>Von</span> Wirtschaft am Schlössli</small><small><span>Wann</span> {e(f['wann'])}</small><small><span>Betreff</span> {e(f['betreff'])}</small></span></header>
  <div class="mb-blatt"><div class="mb-in">{eingebettet(f)}</div></div>
  <p class="mb-ganz"><button type="button" class="mb-kn" aria-expanded="false"><span class="a">Ganze Mail</span><span class="z">Weniger zeigen</span><i>{pf('M4 6l4 4 4-4')}</i></button></p>
</article>''' for i, f in enumerate(FAELLE))
    return f'''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>Zehn Mails · Wirtschaft am Schlössli</title>
<link rel="icon" href="../assets/svg/zeichen.svg">
<style>
@font-face{{font-family:'Open Sans';font-weight:300 800;font-display:swap;src:url('../assets/fonts/OpenSans-var.woff2') format('woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:400 600;font-display:swap;src:url('../assets/fonts/InstrumentSans-normal-400_600.woff2') format('woff2')}}
@font-face{{font-family:'DM Mono';font-weight:400;font-display:swap;src:url('../assets/fonts/DMMono-normal-400.woff2') format('woff2')}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:{NACHT} url(../assets/svg/tapete-a-dunkel.svg) 50% 0/168px auto;color:{BLATT};font:400 17px/1.6 'Instrument Sans',system-ui,sans-serif;--rand:clamp(20px,4.6vw,76px)}}
header.kopf{{padding:clamp(56px,8vw,120px) var(--rand) clamp(30px,4vw,60px);text-align:center}}
header.kopf .zz{{display:block;width:clamp(46px,4.6vw,68px);height:auto;margin:0 auto;color:{HIMMEL}}}
h1{{margin:clamp(18px,2vw,28px) 0 0;font:400 clamp(1.9rem,4.4vw,4.1rem)/1.14 'Open Sans',Arial,sans-serif;text-transform:uppercase;letter-spacing:.1em;text-wrap:balance}}h1 em{{font-style:normal;color:{HIMMEL}}}
.hz{{height:0;border-top:1px solid rgba(162,182,207,.4);margin:clamp(26px,3vw,44px) calc(-1 * var(--rand)) 0}}
header.kopf p{{max-width:60ch;margin:clamp(22px,2.4vw,34px) auto 0;color:rgba(244,246,249,.86);text-wrap:pretty}}
main{{padding:0 0 clamp(60px,8vw,120px)}}
.band{{display:flex;gap:clamp(20px,2.4vw,40px);align-items:flex-start;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scroll-padding-inline:var(--rand);padding:4px var(--rand) 34px;scrollbar-width:none;-webkit-overflow-scrolling:touch}}
.band::-webkit-scrollbar{{display:none}}
.band:focus-visible{{outline:2px solid {HIMMEL};outline-offset:-2px}}
.mb{{flex:0 0 clamp(300px,34vw,520px);scroll-snap-align:start}}
.mb:last-child{{margin-inline-end:var(--rand)}}
.mb-ueber{{display:flex;gap:16px;align-items:flex-start;margin:0 4px 18px;min-height:8.6em}}
.mb-nr{{font:400 2.2rem/.9 'DM Mono',ui-monospace,monospace;color:{HIMMEL}}}
.mb-ueber__t{{display:flex;flex-direction:column;gap:5px;min-width:0}}
.mb-ueber__t b{{font:400 1.08rem/1.25 'Open Sans',Arial,sans-serif;text-transform:uppercase;letter-spacing:.08em}}
.mb-ueber__t small{{font-size:.86rem;line-height:1.4;text-wrap:balance;color:rgba(244,246,249,.76)}}
.mb-ueber__t small span{{display:inline-block;min-width:5.4em;font:400 10px/1.4 'DM Mono',ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;color:{HIMMEL}}}
.mb-blatt{{position:relative;height:640px;border-radius:20px;overflow:hidden;background:{PAPIER};box-shadow:0 0 0 1px rgba(162,182,207,.3),0 40px 50px -30px rgba(0,0,0,.9);-webkit-mask-image:linear-gradient(#000 68%,transparent);mask-image:linear-gradient(#000 68%,transparent)}}
.mb.auf .mb-blatt{{-webkit-mask-image:none;mask-image:none}}
.mb-in{{position:relative}}.mb-in table{{max-width:100%}}
.mb-ganz{{position:relative;margin:18px 0 0;text-align:center}}
.mb.auf .mb-ganz{{margin-top:22px}}
.mb-kn{{display:inline-flex;align-items:center;gap:12px;padding:8px 8px 8px 22px;border:0;border-radius:999px;cursor:pointer;font:400 11.5px/1 'DM Mono',ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;color:{BLATT};
  background:linear-gradient(180deg,#1d4f9e,{STUHL} 60%,{TIEF});box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 0 0 1px rgba(162,182,207,.38),0 14px 22px -12px rgba(0,0,0,.8)}}
.mb-kn i{{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;color:{TINTE};background:linear-gradient(180deg,#f3f6f9,{HIMMEL2} 55%,{HIMMEL});box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}}
.mb-kn svg{{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}}
.mb-kn .z,.mb.auf .mb-kn .a{{display:none}}.mb.auf .mb-kn .z{{display:inline}}.mb.auf .mb-kn svg{{transform:rotate(180deg)}}
.mb-kn .a,.mb-kn .z{{position:relative}}
@supports not (font:-apple-system-body){{.mb-kn .a,.mb-kn .z{{top:1.3px}}}}   /* Schrift optisch mittig (Messlauf text-mitte), nur Chromium wie text_mitte.py der Werkbank */
.mb-kn:focus-visible{{outline:2px solid {HIMMEL2};outline-offset:3px}}
.pfeile{{display:flex;justify-content:center;gap:14px;margin-top:4px}}
.pf{{width:52px;height:52px;border:0;border-radius:50%;cursor:pointer;display:grid;place-items:center;color:{TINTE};background:linear-gradient(180deg,#f3f6f9,{HIMMEL2} 55%,{HIMMEL});box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 12px 20px -10px rgba(0,0,0,.7)}}
.pf svg{{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.pf:disabled{{opacity:.35;cursor:default}}
footer{{padding:26px var(--rand) 40px;text-align:center;font-size:.92rem;color:rgba(244,246,249,.62);border-top:1px solid rgba(162,182,207,.22)}}
footer a{{color:{HIMMEL2}}}
/* Hereinkommen wie auf den anderen Werkbank-Seiten: heben, nur transform und opacity, bei reduced-motion sofort da */
html.js .hr{{opacity:0;transform:translate3d(0,34px,0) scale(.985)}}
html.js .hr.da{{opacity:1;transform:none;transition:opacity .9s cubic-bezier(.2,.7,.2,1) calc(var(--i,0) * 110ms),transform 1.2s cubic-bezier(.16,1,.3,1) calc(var(--i,0) * 110ms)}}
@media (prefers-reduced-motion:reduce){{html.js .hr{{opacity:1;transform:none;transition:none}}}}
@media (max-width:760px){{.mb{{flex-basis:calc(100vw - 2 * var(--rand))}}.pfeile{{display:none}}}}
@media (hover:none){{.pfeile{{display:none}}}}
</style></head>
<body>
<script>if (!matchMedia('(prefers-reduced-motion:reduce)').matches && 'IntersectionObserver' in window) document.documentElement.classList.add('js');</script>
<header class="kopf"><img class="zz hr" style="--i:0" src="img/zeichen.png" alt="" width="68"><h1 class="hr" style="--i:1">Zehn Mails,<br><em>im Ton Ihres&nbsp;Hauses.</em></h1>
<div class="hz hr" style="--i:1"></div>
<p class="hr" style="--i:2">Was ein Gast nach einer Reservation, einer Anfrage oder einem Besuch von Ihnen bekommt, kommt im Kleid der neuen Seite. Zehn Fälle als Idee, von der Bestätigung bis zum Dank am Tag danach. Namen, Daten und Beträge der Gäste sind Beispielwerte; Zeiten, Karten, Ferien und Adresse sind Ihre.</p></header>
<main><div class="band" id="mband" tabindex="0" aria-label="Die zehn Mails, zum Blättern">{karten}</div>
<div class="pfeile hr" style="--i:2"><button type="button" class="pf" data-r="-1" aria-label="Vorige Mail">{pf('M10.5 3 5.5 8l5 5')}</button><button type="button" class="pf" data-r="1" aria-label="Nächste Mail">{pf('m5.5 3 5 5-5 5')}</button></div></main>
<footer class="hr">Entwurf von Robert Reff, Tasty Studios. Stand {STAND}. <a href="../werkbank/index.html#papier">Zurück zu «Alles auf einen Blick»</a></footer>
<script>
(function () {{
  if (document.documentElement.classList.contains('js')) {{
    var io = new IntersectionObserver(function (es) {{ es.forEach(function (e) {{ if (!e.isIntersecting) return; io.unobserve(e.target);
      (e.target.id === 'mband' ? [].slice.call(e.target.querySelectorAll('.hr')) : [e.target]).forEach(function (x) {{ x.classList.add('da'); }}); }}); }}, {{ rootMargin: '0px 0px -8% 0px', threshold: 0 }});
    [].forEach.call(document.querySelectorAll('header.kopf .hr,.pfeile,footer'), function (x) {{ io.observe(x); }}); io.observe(document.getElementById('mband'));
  }}
}})();
(function () {{
  var ms = [].slice.call(document.querySelectorAll('.mb'));
  function lage(m) {{ var bl = m.querySelector('.mb-blatt'), i = bl.querySelector('.mb-in'); bl.style.height = (m.classList.contains('auf') ? i.scrollHeight : Math.min(640, i.scrollHeight)) + 'px'; }}
  ms.forEach(function (m) {{
    var k = m.querySelector('.mb-kn');
    [].forEach.call(m.querySelectorAll('img'), function (im) {{ if (!im.complete) im.addEventListener('load', function () {{ lage(m); }}, {{ once: true }}); }});
    lage(m);
    k.addEventListener('click', function () {{ var auf = m.classList.toggle('auf'); k.setAttribute('aria-expanded', auf); lage(m); if (!auf) m.scrollIntoView({{ block: 'nearest' }}); }});
  }});
  var rt = 0; addEventListener('resize', function () {{ clearTimeout(rt); rt = setTimeout(function () {{ ms.forEach(lage); kl(); }}, 120); }});
  var b = document.getElementById('mband'), p = document.querySelectorAll('.pf');
  function schritt() {{ return ms[0].getBoundingClientRect().width + parseFloat(getComputedStyle(b).columnGap || 0); }}
  function kl() {{ p[0].disabled = b.scrollLeft < 4; p[1].disabled = b.scrollLeft > b.scrollWidth - b.clientWidth - 4; }}
  [].forEach.call(p, function (x) {{ x.addEventListener('click', function () {{ b.scrollBy({{ left: +x.dataset.r * schritt(), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }}); }}); }});
  b.addEventListener('scroll', kl, {{ passive: true }}); kl();
}})();
</script>
</body></html>
'''


def main():
    import shutil
    for d in glob.glob(os.path.join(MAILS, '[0-9][0-9]-*')):   # Ordner früherer Fassungen weg
        if os.path.basename(d) not in {f['ordner'] for f in FAELLE}:
            shutil.rmtree(d)
    bilder()
    for f in FAELLE:
        z = os.path.join(MAILS, f['ordner']); os.makedirs(z, exist_ok=True)
        open(os.path.join(z, 'index.html'), 'w', encoding='utf-8').write(mail(f, '../../'))
    open(os.path.join(MAILS, 'index.html'), 'w', encoding='utf-8').write(uebersicht())
    json.dump([[f['nr'], f['ordner'], f['name'], f['satz']] for f in FAELLE], open(os.path.join(HIER, 'werkbank.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(FAELLE), 'Mails gebaut:', ', '.join(f['ordner'] for f in FAELLE))


if __name__ == '__main__':
    main()
