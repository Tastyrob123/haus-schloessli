#!/usr/bin/env python3
"""Befund-Seite des Spähers (Station 2) für die Wirtschaft am Schlössli, Bottighofen, gebaut mit dem Werkbank-Kit.
   python3 bau_befund.py   → befund.html + werkbank/ + bilder/ in diesem Ordner. Inhalt aus befund.md / einordnung.json (18.10.2026).
   Vorlage: Zurbriggen Wellnesshotel, _kette/02-spaeher/bau_befund.py."""
import json, os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
os.environ['HAUS'] = HIER
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import kern as K
from kern import H, e, kn, titel, kap, PF

Q = os.path.join(HIER, '_quelle-bilder')
HEUTE = 'https://www.schloessli-bottighofen.ch/'
EIN = json.load(open(os.path.join(HIER, 'einordnung.json'), encoding='utf-8'))
B = lambda t: f'<span class="bf-beleg">{t}</span>'
OFFEN = lambda t='offen': f'<span class="bf-offen">{t}</span>'


def bild(name, breite=1600, schnitt=None, lage=(.5, .5), dunkel=None, ziel=None):
    quelle = os.path.join(Q, name + '.jpg')
    ziel_n = ziel or name
    pfad = os.path.join(HIER, 'bilder', ziel_n + '.webp')
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    if not os.path.exists(pfad) or os.path.getmtime(pfad) < os.path.getmtime(quelle):
        K.webp(quelle, pfad, breite, q=80, schnitt=schnitt, lage=lage, dunkel=dunkel)
    return 'bilder/' + ziel_n + '.webp'


def muster():
    vb, innen = H.ZEICHEN
    w, h = [float(x) for x in vb.split()[2:]]
    s = 30 / w
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">'
           f'<g fill="none" stroke="#c9a97a" stroke-opacity=".10" stroke-width="1"><path d="M0 .5H240M.5 0V240"/></g>'
           f'<g fill="#c9a97a" fill-opacity=".09" transform="translate({120 - 15} {120 - h * s / 2}) scale({s})">{innen}</g></svg>')
    open(os.path.join(HIER, 'werkbank', 'muster.svg'), 'w').write(svg)


def blatt(i, ident, name, zeilen, text, innen, fl):
    return f'''<section class="fl {fl} blatt" id="{ident}">
  <div class="in">
    {K.kopf(i, name, zeilen, text)}
    {innen}
  </div>
</section>'''


def liste(punkte):
    return '<ul class="bf-liste">' + ''.join(f'<li data-a="auf" style="--i:{min(k, 6)}"><b>{t}</b>{x}</li>' for k, (t, x) in enumerate(punkte)) + '</ul>'


def tab(kopf, zeilen):
    return ('<table class="bf-tab" data-a="auf"><thead><tr>' + ''.join(f'<th>{k}</th>' for k in kopf) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in z) + '</tr>' for z in zeilen) + '</tbody></table>')


def satz(t, oben=24):
    return f'<div class="lauf" style="margin-top:{oben}px"><p data-a="worte">{t}</p></div>'


def baue():
    K.gestaltung()
    muster()
    b_abend = bild('terrasse-abend', 2000, schnitt=16 / 10, lage=(.5, .55), dunkel=(.5, .5), ziel='terrasse-abend-dunkel')
    b_tag = bild('terrasse-tag', 2000)
    b_apero = bild('apero-see', 1100)
    b_pasta = bild('teller-pasta', 1100)
    b_wein = bild('weinregal', 1100)
    b_team = bild('team', 1600)
    b_schaefli = bild('schaefli-haus', 900, schnitt=4 / 3)
    b_fam_s = bild('terrasse-tag', 900, schnitt=4 / 3, ziel='familie-schloessli')

    streu = ''.join(f'<div class="abzug" data-a="schweb" style="left:{x}%;top:{y}%;width:{w}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}"><img src="{s}" alt=""></div>'
                    for i, (s, x, y, w, r) in enumerate([(b_apero, 6, 4, 46, -3), (b_pasta, 46, 30, 42, 2.5), (b_wein, 14, 58, 40, -1.5)]))
    auftakt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(2, 'Späher · Befund')}
      {titel(['Entdeckung des Jahres,', 'eine Seite aus der Vorlage.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte">Wirtschaft am Schlössli im Hafen von Bottighofen, 15 Punkte GaultMillau, Küche Monika Huber, Schwesterhaus der Taverne zum Schäfli. Hier steht, wie die heutige Seite dasteht, wer dahintersteht, was fehlt, was das Haus ausmacht und ob es passt. Jede Angabe mit Quelle, Stand 18. Oktober 2026.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Heutige Seite öffnen', HEUTE, neu=True)}{kn('Zur Empfehlung', '#empfehlung', 'kn--linie')}</div>
    </div>
    <div class="auslage" aria-hidden="true">{streu}</div>
  </div>
</section>'''

    haus = blatt(1, 'haus', 'Das Haus in Kürze', ['Ein Restaurant am Hafen,', 'kein Kettenhaus.'],
                 'Betreiberin ist die CK Gastro Consulting GmbH in Wigoltingen; Christian Kuchler hält 199 von 200 Stammanteilen. Seit der Neueröffnung 2025 kocht hier Monika Huber, früher seine Sous-Chefin im Schäfli.',
                 tab(['Angabe', 'Wert', 'Quelle'], [
                     ['Art', 'Restaurant, mediterrane und französische Küche, Preisklasse €€€, keine Zimmer', B('Startseite; Michelin, 18.10.2026')],
                     ['Lage', 'Seestrasse 50, 8598 Bottighofen, direkt im Hafen, Blick auf See und Alpen', B('Startseite, Kontakt')],
                     ['Küche · Gastgeber', 'Monika Huber, Küchenchefin · Jonas Volpert, Gastgeber und Sommelier', B('Startseite, Über uns')],
                     ['Betreiberin', 'CK Gastro Consulting GmbH, CHE-139.373.932, eingetragen 04.05.2021, Zweck «Beratung im Gastronomiebereich»', B('Impressum; SHAB über Zefix, 18.10.2026')],
                     ['Gesellschafter', 'Christian Kuchler (Vorsitz, 199 Anteile), Ramona Gubler (Geschäftsführerin, 1 Anteil)', B('SHAB 04.05.2021')],
                     ['Urheberrechte', 'laut Impressum bei der Taverne zum Schäfli AG', B('Impressum')],
                     ['Geöffnet', 'Donnerstag bis Montag 11:30 bis 23:00, Küche 11:30 bis 13:30 und 18:00 bis 20:00; Dienstag und Mittwoch Ruhetag', B('Kontakt, 18.10.2026')],
                     ['Eröffnet', 'Neueröffnung April 2025; davor «Strandwirtschaft Schlössli» eines anderen Teams', B('Web-Archiv 08.12.2024, 08.09.2024')],
                     ['Alter des Gebäudes', OFFEN('offen') + ' · Wanderführer nennen das 17. Jahrhundert, die Seite sagt nichts', B('Station 3')],
                 ]), 'fl--papier')

    agentur = blatt(2, 'agentur', 'Wer hinter der heutigen Seite steht', ['Keine Agentur,', 'ein Abo bei Squarespace.'],
                    'Weder Fuss noch Impressum noch Quelltext nennen eine Agentur. Die Seite läuft auf dem Baukasten Squarespace, Vorlage 7.1, wie die des Schäfli. Wer sie gebaut hat und pflegt, ist von aussen nicht zu sehen.',
                    liste([('Anbieter', f'Server-Antwort {B("server: Squarespace")}, Vorlage {B("templateId 5c5a519771c10ba3470d8101 · 7.1")}. Agentur: ' + OFFEN() + '.'),
                           ('Gebaut', 'Kennung der Seite mit Zeitstempel 12.09.2024, Instagram verknüpft am 03.10.2024, Gutschein-Formular am 06.12.2024. Im Web-Archiv am 08.12.2024 zuerst mit «Neueröffnung April 2025».'),
                           ('Zuletzt geändert', 'Events 24.09.2026 (Sitemap), Weinkarte 14.10.2026, Lunch-Menü «Lunch_261015» (Dateinamen).'),
                           ('Vorher', 'Bis Herbst 2024 die «Strandwirtschaft Schlössli» auf einer Seite von gastronovi, anderes Team.'),
                           ('Pakete und Preise', 'Abos «Basic», «Core», «Advanced», jährlich oder monatlich. Von hier aus nur in Baht zu sehen; Preis in Franken und Abo des Hauses: ' + OFFEN() + '.'),
                           ('Laufzeit', 'Squarespace-Bedingungen ab 27.03.2025: läuft, bis gekündigt wird, verlängert sich automatisch, kündbar jederzeit, Rückerstattung in der Regel nicht.'),
                           ('Nutzungsrechte', 'Inhalte bleiben beim Haus, Vorlage und Plattform gehören Squarespace, Squarespace hat eine dauerhafte Lizenz an den Inhalten. Export nur als WordPress-Datei, Bilder darin als Verweise, Events, Gestaltung und CSS gehen nicht mit.'),
                           ('Adresse', f'Namensserver {B("ns14.net")}, Mail bei Google; bei wem die Adresse registriert ist: ' + OFFEN() + '.'),
                           ('Vertrag des Hauses', OFFEN('ungeprüft, im Gespräch zu klären') + '.')])
                    + f'''<div class="bf-zwei" data-a="auf"><div><h3>Wo wir besser sind</h3><ul>
<li>Erzählung statt Vorlage: Schlössli, Hafen, Platanen, Monika Hubers Weg an den See</li>
<li>15 Punkte und «Entdeckung des Jahres» dort, wo der Gast landet</li>
<li>Karten als Seite aus einer Quelle statt sieben PDFs</li>
<li>Bankette, Events und Gutschein mit eigenem Weg statt Mail-Programm und Handversand</li>
<li>Am Handy Reservation im ersten Bildschirm</li></ul></div>
<div><h3>Was dem Haus bleibt</h3><ul>
<li>Die neue Seite gehört dem Haus ganz: Code, Bilder, Adresse, Zugänge</li>
<li>Die Reservation bei gastronovi bleibt, wie sie ist</li>
<li>Kein Vertrag mit Mindestlaufzeit im Weg, laut den öffentlichen Bedingungen jederzeit kündbar</li>
<li>Zwei Häuser als Familie, jedes mit eigener Welt</li></ul></div></div>''', 'fl--nacht')

    fenster1 = f'''<section class="fl fl--nacht blatt" style="padding-top:0">
  <div class="in"><div class="fen" data-a="schweb"><div class="fen__k"><i></i><i></i><i></i><span>Startbild der heutigen Seite · Original 2500 px</span></div><img src="{b_tag}" alt="Blaue Stühle auf der Terrasse vor See und Alpen" loading="lazy"></div>
  {satz('Das kann die heutige Seite: Ihr Startbild zeigt sofort, wo man sitzt. Darunter wird sie zur Vorlage mit Mint-Grund und kleinen Kacheln.', 22)}</div>
</section>'''

    seite = blatt(3, 'seite', 'Die heutige Seite', ['Jung und gepflegt,', 'aber ohne Geschichte.'],
                  'Fünf Seiten in der Leiste, fünfzehn in der Sitemap. Startbild über die ganze Breite, darunter Text, Bildpaare und acht Gerichte als kleine Kacheln. Im Fuss die Siegel von GaultMillau und Michelin.',
                  tab(['Punkt', 'Stand', 'Beleg'], [
                      ['Technik', 'Squarespace 7.1, Schriften Gilda Display und PT Serif, Grund Mint #d8fffc, Knöpfe Nachtblau #213c4f', B('Quelltext; Aufnahme gemessen')],
                      ['Seiten', 'Home, Karten, Events & Termine, Über uns, Kontakt; doppelte Startseite /home-1, «Impressionen» nur in der Sitemap, Adressen aus der Vorlage', B('sitemap.xml, 18.10.2026')],
                      ['Bilder', '40 eigene Bilder, Originale bis 5504 × 8256 px aus Fotoserien August 2025 und Mai 2026; Gerichte auf der Startseite als Kacheln mit 223 px, letzte Reihe halb leer', B('Quelltext, Aufnahme 1440 px')],
                      ['Handy', 'eigene Fassung, nichts läuft über; erster Bildschirm nur Foto und Name, Reservation erst nach dem Wischen', B('Aufnahme 390 px')],
                      ['Gewicht', 'Startseite rund 2,6 MB am Rechner, 1,7 MB am Handy; Ladezeiten von Thailand aus nur Arbeitswert', B('_qa/spaeher/messung.json')],
                      ['Sprachen', 'nur Deutsch; «Genießen» mit ß, Cookie-Fenster in Du-Form', B('Quelltext')],
                      ['Buchung', 'Reservation über gastronovi (Restaurant 118851) auf Startseite und Kontakt; Bankett und Event-Plätze per Mail-Link', B('Startseite, Karten, Events')],
                      ['Gutschein', 'Formular mit Name, E-Mail, Adresse, Betrag, ohne Bezahlung, Versand von Hand', B('Quelltext Startseite')],
                      ['Rechtstexte', 'Impressum ja · Datenschutz ja, nennt Google Analytics, nicht Squarespace und gastronovi · AGB ja (April 2025) · Widerruf ' + OFFEN('keiner gefunden'), B('/impressum, /datenschutzerklarung, /agbs')],
                      ['Newsletter · Social', 'kein Newsletter sichtbar (Baustein im Quelltext nicht eingerichtet) · Instagram @schloessli_bottighofen verknüpft, im Fuss nicht zu sehen', B('Quelltext /kontakt')],
                      ['Karten', 'Speisekarte Oktober, Weinkarte 14.10.2026, Lunch, Lästermeile, Bankett: alle als PDF', B('Seite Karten')],
                  ]) + satz('<b>Was sie gut macht:</b> Das Startbild trägt, die Fotos sind professionell und gross vorhanden. Karten, Lunch, Events und Ferien sind aktuell, das Team pflegt die Seite sichtbar. Reservieren geht mit einem Klick, das Cookie-Fenster lässt ablehnen. Eine junge, saubere Seite, keine alte.', 26), 'fl--papier')

    fehlt = blatt(4, 'fehlt', 'Was fehlt', ['Was der Gast', 'nicht erfährt.'],
                  'Alles davon steht schon irgendwo: bei GaultMillau, in Event-Texten, in den PDFs. Nur nicht dort, wo der Gast landet.',
                  liste([('Die Auszeichnung', '«Entdeckung des Jahres 2026» fehlt auf der ganzen Seite, der 15. Punkt steht nur als Siegel im Fuss.'),
                         ('Die Geschichte', 'Kein Satz zum Schlössli, zum Hafen, zu den Platanen, zur Neueröffnung, zum Schäfli. Monika Hubers Weg nur in Event-Texten.'),
                         ('Die Karte als Seite', 'Alle Karten nur als PDF; die Seite «Karten» trägt als einzige Überschrift «Banketts & Gruppen».'),
                         ('Wege ohne Mail-Programm', 'Bankettanfrage und Event-Reservation öffnen das Mail-Programm, der Gutschein ist ein Formular ohne Bezahlung.'),
                         ('Handy', 'Reservation nicht im ersten Bildschirm.'),
                         ('Team', 'Patissière Theresa Hermann, die GaultMillau nennt, fehlt auf «Über uns».'),
                         ('Sprachen und Ordnung', 'Kein Englisch; doppelte Startseite, versteckte «Impressionen», Adressen aus der Vorlage.'),
                         ('Datenschutz', 'Nennt die genutzten Dienste Squarespace und gastronovi nicht.')]), 'fl--nacht')

    ausmacht = blatt(5, 'ausmacht', 'Was das Haus ausmacht', ['Die schönste Terrasse', 'am Bodensee.'],
                     'So nennt Christian Kuchler sie auf der Startseite. GaultMillau beschreibt die Terrasse im Schatten prächtiger Platanen. Hier kocht Monika Huber, früher bei Dieter Koschina in der Villa Joya und Sous-Chefin im Schäfli, ihre Reise durch das Mittelmeer; GaultMillau kürte sie zur Entdeckung des Jahres 2026.',
                     liste([('Gastgeber und Keller', 'Jonas Volpert, Sommelier. GaultMillau: auf den Weinkeller «dürfte manches Fine-Dining-Restaurant neidisch sein».'),
                            ('Seine Leute', 'Ein «Ehemaligen Lunch» holte die Weggefährten aus dem Schäfli an den See; das Team fährt geschlossen auf die Gourmetkreuzfahrt mit Koschina.'),
                            ('Zimmer', 'keine.'),
                            ('Anlässe', 'Banketts und Gruppen auf zwei Etagen für je bis zu 26 Personen, Tavolata oder gesetztes Menü, Vorschläge als PDF.'),
                            ('Seeterrasse', 'ja, mit eigenem Gewicht: Startbild, Kuchler-Zitat; Michelin führt das Haus als «Favorit der Inspektoren».'),
                            ('Dazu', 'Lunch-Menü, durchgehend die Karte der «Lästermeile», 4-Hands-Lunch, Gourmetkreuzfahrt 13. bis 15.11.2026, Gutscheine.')]), 'fl--papier')

    fenster2 = f'''<section class="fl fl--papier blatt" style="padding-top:0">
  <div class="in"><div class="fen" data-a="schweb"><div class="fen__k"><i></i><i></i><i></i><span>Über uns · Das Team</span></div><img src="{b_team}" alt="Das Team der Wirtschaft am Schlössli" loading="lazy"></div>
  {satz('Auf der heutigen Seite stehen fünf Namen mit Rolle. Wer sie sind und woher sie kommen, erzählt sie nicht.', 22)}</div>
</section>'''

    fam = [('Wirtschaft am Schlössli', 'Seestrasse 50, 8598 Bottighofen', 'CK Gastro Consulting GmbH · 15 Punkte', 'Squarespace 7.1 · Reservation gastronovi · Mail Google', HEUTE, b_fam_s),
           ('Taverne zum Schäfli', 'Oberdorfstrasse 8, 8556 Wigoltingen', 'Taverne zum Schäfli AG · 18 Punkte', 'Squarespace 7.1, gleiche Vorlage · Reservation Zenchef · Mail Microsoft', 'https://www.schaefli-wigoltingen.ch/', b_schaefli)]
    karten = ''.join(f'<a href="{e(w)}" target="_blank" rel="noopener" data-a="auf"><img src="{img}" alt="{e(n)}" loading="lazy"><div><b>{e(n)}</b><small>{e(o)}<br>{e(g)}<br>{e(s)}</small></div></a>' for n, o, g, s, w, img in fam)
    familie = blatt(6, 'familie', 'Familie und weitere Häuser', ['Zwei Häuser,', 'eine Handschrift von Kuchler.'],
                    'Beide Seiten verweisen aufeinander, laufen auf demselben Baukasten und tragen denselben Wortlaut im Impressum. Sonst treten sie getrennt auf: eigene Firma, eigene Reservation, eigene Gutscheine. Gebaut hat Robert noch keines der beiden.',
                    f'<div class="bf-fam">{karten}</div>'
                    + '''<div class="bf-zwei" data-a="auf"><div><h3>Wie sie aufeinander verweisen</h3><ul>
<li>Schlössli, Kontakt: Foto des Schäfli-Hauses und Plakette «2** Michelin 18 Punkte», verlinkt</li>
<li>Schlössli, Events: «Kitchen Party im Schäfli» mit Link nach Wigoltingen, «Ehemaligen Lunch» mit den Weggefährten aus dem Schäfli</li>
<li>Logo des Schlössli: «by Christian Kuchler»</li>
<li>Schäfli, Kontakt: Logo des Schlössli, «Besuchen Sie auch unser Partner-Restaurant am Bodensee»</li></ul></div>
<div><h3>Gemeinsam und getrennt</h3><ul>
<li>Gemeinsam: Squarespace mit derselben Vorlage, gleiches Impressum, Gutschein als Formular auf der Startseite</li>
<li>Getrennt: GmbH gegen AG, gastronovi gegen Zenchef, je eigenes Gutschein-Formular, Google gegen Microsoft</li>
<li>Gemeinsamer Gutschein oder gemeinsame Reservation: nicht zu sehen</li>
<li>Urheberrechte der Schlössli-Seite laut Impressum bei der Taverne zum Schäfli AG</li></ul></div></div>''', 'fl--nacht')

    noten = blatt(7, 'noten', 'Noten', ['Die Gäste', 'und die Führer.'],
                  'Abgelesen am 18. Oktober 2026, nur abgelesen. Die Auszeichnungen an der Quelle geprüft.',
                  tab(['Quelle', 'Note', 'Anzahl'], [['Google Maps', '4,2 von 5', '85'],
                                                     ['TripAdvisor', 'Eintrag «Schlössli», Bottighofen: 3,1 von 5 · ' + OFFEN('ob heutige Wirtschaft oder frühere Strandwirtschaft'), '9'],
                                                     ['Booking.com', 'betrifft nicht (Restaurant)', '–'],
                                                     ['GaultMillau', '15 Punkte, «Entdeckung des Jahres 2026»', B('gaultmillau.ch, 18.10.2026')],
                                                     ['Michelin', 'empfohlen, kein Stern, «Favorit der Inspektoren»; Plakette im Fuss sagt 2025', B('guide.michelin.com, 18.10.2026')],
                                                     ['Falstaff', OFFEN('Seite an der Quelle nicht lesbar'), '–']]), 'fl--papier')

    empfehlung = f'''<section class="schluss" id="empfehlung">
  <img class="schluss__b" src="{b_abend}" alt="Die Terrasse am Abend über dem Bodensee" loading="lazy">
  <div class="in">
    {kap(8, 'Empfehlung')}
    <p class="bf-urteil" data-a="auf">Passt, als Studie, weil es zur Familie gehört. <em>Mit einem Vorbehalt.</em></p>
    <div class="lauf">
      <p data-a="worte">Schweizer Haus, inhabergeführt von Christian Kuchler, Schwesterhaus der Taverne zum Schäfli. Das Haus ist sichtbar stärker als seine Seite: Entdeckung des Jahres, 15 Punkte, Terrasse am Hafen, eine Küchenchefin mit Geschichte. Die Seite zeigt eine Vorlage, erzählt nichts davon und schickt Gäste für Karten in PDFs. Echtes Material ist da, kein Relaunch erkennbar.</p>
      <p data-a="worte">Der Vorbehalt: Die Seite ist jung, seit der Neueröffnung 2025, und hat starke Fotos. Technik allein trägt nicht, unsere Seite muss über Erlebnis, Geschichte und Auszeichnung hinausgehen. Hinter ihr steht keine Agentur, nur das Squarespace-Abo, jederzeit kündbar. Die Reservation bei gastronovi kann bleiben.</p>
    </div>
    <div class="kn-reihe" data-a="auf">{kn('Heutige Seite öffnen', HEUTE, neu=True)}{kn('Zur Karte der Kette', 'http://127.0.0.1:8978/?familie=Taverne%20zum%20Sch%C3%A4fli%20AG', 'kn--linie')}</div>
  </div>
</section>'''

    haupt = auftakt + haus + agentur + fenster1 + seite + fehlt + ausmacht + fenster2 + familie + noten + empfehlung
    html = K.rahmen('Befund', 'Station 2 der Kette: Befund des Spähers zur Wirtschaft am Schlössli, Bottighofen.', 'Befund', haupt,
                    'Befund von Robert Reff, Tasty Studios, für die interne Kette. Fotos, Zeichen und Texte gehören ' + H.RECHTE)
    html = html.replace('../werkbank/', 'werkbank/')
    html = html.replace(f'<a class="glanz" href="werkbank/index.html">Zur Werkbank{PF}</a>', f'<a class="glanz" href="{HEUTE}" target="_blank" rel="noopener">Heutige Seite{PF}</a>')
    html = html.replace('<a class="insel__m" href="werkbank/index.html">', '<a class="insel__m" href="#">')
    K.schreib(os.path.join(HIER, 'befund.html'), html)
    print('befund.html geschrieben,', len(html) // 1024, 'KB')


if __name__ == '__main__':
    baue()
