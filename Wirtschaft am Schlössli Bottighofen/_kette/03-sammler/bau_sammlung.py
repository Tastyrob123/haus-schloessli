#!/usr/bin/env python3
"""Sammlung des Sammlers (Station 3) für die Wirtschaft am Schlössli, Bottighofen, gebaut mit dem Werkbank-Kit.
   python3 bau_sammlung.py   → sammlung.html + werkbank/ + bilder/ in diesem Ordner.
   Inhalt aus fakten.json, sprachen.json und _quelle/ (19.10.2026). Zahlen des Vorrats werden beim Bau im Ordner gezählt."""
import json, os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
os.environ['HAUS'] = HIER
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import kern as K
from kern import H, e, kn, titel, kap, PF

PROJ = os.path.dirname(os.path.dirname(HIER))
QU = os.path.join(PROJ, '_quelle')
QA = os.path.join(HIER, 'assets', 'quelle')
FAKT = json.load(open(os.path.join(HIER, 'fakten.json'), encoding='utf-8'))
SPR = json.load(open(os.path.join(HIER, 'sprachen.json'), encoding='utf-8'))
HEUTE = 'https://www.schloessli-bottighofen.ch'
MAT = '../../_quelle/material.html'
PROMPT = '../../Prompt%20%E2%80%94%20Wirtschaft%20am%20Schl%C3%B6ssli.md'
SCHWESTER = '/haus/Taverne%20zum%20Sch%C3%A4fli%20Wigoltingen/_kette/03-sammler/sammlung.html'
O = '<span class="bf-offen">offen</span>'
BILD = ('.jpg', '.jpeg', '.png', '.webp', '.JPG')


def bild(name, ziel, breite=1600, schnitt=None, lage=(.5, .5), dunkel=None):
    quelle = os.path.join(QA, name)
    z = os.path.join(HIER, 'bilder', ziel + '.webp')
    os.makedirs(os.path.dirname(z), exist_ok=True)
    if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(quelle):
        K.webp(quelle, z, breite, q=80, schnitt=schnitt, lage=lage, dunkel=dunkel)
    return 'bilder/' + ziel + '.webp'


def zaehl(rel, endungen=BILD):
    p = os.path.join(QU, rel)
    if not os.path.isdir(p):
        return 0
    return sum(1 for f in os.listdir(p) if f.endswith(endungen))


def mb(rel):
    s = 0
    for w, _, fs in os.walk(os.path.join(QU, rel)):
        s += sum(os.path.getsize(os.path.join(w, f)) for f in fs)
    return round(s / 1e6)


def muster():
    vb, innen = H.ZEICHEN
    w, h = [float(x) for x in vb.split()[2:]]
    s = 30 / w
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="220" height="220" viewBox="0 0 220 220">'
           f'<g fill="none" stroke="#c9a97a" stroke-opacity=".07" stroke-width="1"><path d="M0 .5H220M.5 0V220"/></g>'
           f'<g fill="#c9a97a" fill-opacity=".09" transform="translate({110 - 15} {110 - h * s / 2}) scale({s})">{innen}</g></svg>')
    open(os.path.join(HIER, 'werkbank', 'muster.svg'), 'w').write(svg)


def b(t):
    return f'<span class="bf-beleg">{t}</span>'


def tab(kopf, zeilen):
    return ('<table class="bf-tab" data-a="auf"><thead><tr>' + ''.join(f'<th>{k}</th>' for k in kopf) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in z) + '</tr>' for z in zeilen) + '</tbody></table>')


def blatt(i, ident, name, zeilen, text, innen, fl):
    return f'''<section class="fl {fl} blatt" id="{ident}">
  <div class="in">
    {K.kopf(i, name, zeilen, text)}
    {innen}
  </div>
</section>'''


def fenster(img, satz, kopfzeile, alt, fl='fl--nacht'):
    return f'''<section class="fl {fl} blatt" style="padding-top:0">
  <div class="in"><div class="fen" data-a="schweb"><div class="fen__k"><i></i><i></i><i></i><span>{kopfzeile}</span></div><img src="{img}" alt="{alt}" loading="lazy"></div>
  <div class="lauf" style="margin-top:22px"><p data-a="worte">{satz}</p></div></div>
</section>'''



def baue():
    K.gestaltung()
    muster()
    b_terr = bild('terrasse.jpg', 'terrasse', 1800)
    b_abend = bild('abend.jpg', 'abend', 1400)
    b_plat = bild('platanen.jpg', 'platanen', 1400)
    b_tort = bild('tortelloni.jpg', 'tortelloni', 900)
    b_team = bild('team.jpg', 'team', 1800)
    b_bar = bild('bar.jpg', 'bar', 900, schnitt=4 / 5)
    b_heft = bild('heft125.jpg', 'heft125', 1100)
    b_titel = bild('heft001.jpg', 'heft001', 900, schnitt=4 / 5)
    b_nacht = bild('abend.jpg', 'abend-dunkel', 1600, dunkel=(.45, .6))

    # ------------------------------------------------------------ Auftakt
    streu = ''.join(f'<div class="abzug" data-a="schweb" style="left:{x}%;top:{y}%;width:{w}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}"><img src="{s}" alt=""></div>'
                    for i, (s, x, y, w, r) in enumerate([(b_terr, 2, 4, 66, -2.5), (b_heft, 46, 34, 42, 2.5), (b_tort, 8, 56, 30, -1.5)]))
    n_web = zaehl('website/bilder'); n_heft = zaehl('presse/heft-bilder')
    n_pdf = zaehl('website/pdf', ('.pdf',)) + zaehl('presse/pdf', ('.pdf',))
    n_txt = zaehl('website/text', ('.md',)) + zaehl('web-archiv/text', ('.md',)) + zaehl('presse', ('.md',)) + zaehl('extern/portale', ('.md',))
    auftakt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(3, 'Sammler · Recherche')}
      {titel(['Alles, was es', 'über das Schlössli gibt.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Wirtschaft am Schlössli in Bottighofen: die Seite des Hauses ganz, die Vorgängerin aus dem Web-Archiv, Portale, Instagram, Presse, das Handelsregister und die Gemeindeschrift von 1994 über das Schlössli am See. Jede Angabe mit Quelle, jede Lücke rot. Stand 19. Oktober 2026.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Material ansehen', MAT)}{kn('Zu den Lücken', '#luecken', 'kn--linie')}</div>
    </div>
    <div class="auslage" aria-hidden="true">{streu}</div>
  </div>
</section>'''

    # ------------------------------------------------------------ 1 Vorrat je Quelle
    zeilen = [
        ['Website heute', f'{n_web} Bilder · {zaehl("website/text", (".md",))} Seiten · {zaehl("website/pdf", (".pdf",))} PDFs', 'schloessli-bottighofen.ch, Squarespace, bis 2500 px; Karten vom Oktober 2026', 'Haus; laut Impressum Taverne zum Schäfli AG; kein Fotograf in den Dateien'],
        ['Web-Archiv', f'{zaehl("web-archiv/text", (".md",))} Seiten', 'archive.org 2023–2025: Strandwirtschaft Schlössli, «Neueröffnung April 2025»', 'Vorgängerin: anderer Betrieb; heutige Fassung: Haus'],
        ['Gemeindeschrift 1994', f'1 PDF, 152 Seiten · {n_heft} Seitenbilder', '«Die Bottighofer Mühlen und das Schlössli am See», Kapitel per Texterkennung', 'Gemeinde Bottighofen, nur Anschauung'],
        ['GaultMillau · Michelin', f'{zaehl("extern/portale/gaultmillau") + zaehl("extern/portale/guide-michelin")} Bilder · Texte · Belege', '15 Punkte an der Quelle, Michelin «plate», Titelbilder 1770 und 1000 px', 'Verlage / Haus, nur Anschauung'],
        ['Falstaff · Feinschmecker', 'Texte', '91 von 100 mit Teilnoten; 2,5 von 5', 'Verlage, nur zum Nachlesen'],
        ['Schweiz Tourismus', f'{zaehl("extern/myswitzerland")} Bilder · Text', 'Eintrag wie Startseite, nennt noch 14 Punkte', 'vom Haus geliefert'],
        ['Instagram', f'{zaehl("extern/ig")} Beiträge', '@schloessli_bottighofen, 640 px, ohne Anmeldung', 'Haus; ein Gemeinschaftsbeitrag @christiankuchler85'],
        ['Logo', f'{zaehl("extern/logo")} Datei', 'transparent 1563 px, gefunden auf der Schäfli-Seite', 'Haus'],
        ['Presse', f'{zaehl("presse", (".md",))} Texte', 'GaultMillau 2025, Tagblatt 2025, Thurgauer Zeitung, Südkurier, Handelsregister, Gemeinde', 'Verlage, nur zum Nachlesen'],
        ['Aussortiert', f'{zaehl("website/fremd-schaefli/bilder")} Bilder', 'Haus und Plakette der Taverne zum Schäfli auf «Kontakt»', 'Schwesterhaus, nie für diese Seite'],
        ['Filme · Booking · TripAdvisor', '–', 'keine Filme gefunden · kein Hotel · Chrome-Erweiterung nicht verbunden', O],
    ]
    vorrat = blatt(1, 'vorrat', 'Der Vorrat je Quelle', ['Was da ist,', 'und wem es gehört.'],
                   'Gezählt im Ordner _quelle/ beim Bau dieser Seite. Zu jedem Bildordner gibt es eine herkunft.json mit der Adresse jedes Bildes.',
                   tab(['Quelle', 'Anzahl', 'Herkunft', 'Rechte'], zeilen) +
                   f'<div class="kn-reihe" data-a="auf">{kn("Material-Übersicht öffnen", MAT)}</div>', 'fl--papier')

    # ------------------------------------------------------------ 2 Die Bögen
    boegen = [('website_bilder', 'Website heute', 'Gerichte auf blauen Tellern, Terrasse am Tag und im Abendlicht, Team, Bar mit Zementfliesen, Weinregal, das Logo auf Mint, die Siegel im Fuss.'),
              ('presse_heft-bilder', 'Gemeindeschrift 1994', 'Titelblatt, Kapitelseite, Postkarten «Hotel und Pension Schlössli» und «Strand Hotel Schlössli», Zeichnung von Günter Dittmann.'),
              ('extern_ig', 'Instagram', 'Zwölf sichtbare Beiträge: Hafen, Schwäne, Küche, Tortelloni. Einer ist ein Beitrag von Christian Kuchler und zeigt das Schäfli.'),
              ('extern_myswitzerland', 'Schweiz Tourismus', 'Zwei Bilder des Eintrags, 1761 und 1270 px.'),
              ('website_fremd-schaefli_bilder', 'Aussortiert', 'Haus der Taverne zum Schäfli bei Tag und Nacht, Plakette «2** Michelin 18 Punkte»: hängen auf der Schlössli-Seite als Verweis, gehören zum Schwesterhaus.')]
    fig = ''.join(f'<figure data-a="auf"><img src="{bild("bogen_" + k + ".jpg", "bogen-" + k, 1800)}" alt="Bilderbogen {e(t)}" loading="lazy"><figcaption><b>{e(t)}</b>{e(s)}</figcaption></figure>' for k, t, s in boegen)
    bogen = blatt(2, 'boegen', 'Die Bögen', ['Jedes Bild', 'gegen das Haus geprüft.'],
                  'Je Quelle ein Bogen. Was nicht zum Schlössli gehört, liegt in eigenen Ordnern.',
                  f'<div class="sa-boegen">{fig}</div>', 'fl--nacht')

    f1 = fenster(b_heft, 'Das Schlössli auf einer alten Postkarte: «Strand Hotel Schlössli, Bottighofen b/Kreuzlingen». Heute ist es ein Wohnhaus; die Wirtschaft liegt daneben, im ehemaligen Hafenmeistergebäude.',
                 'Gemeindeschrift Bottighofen 1994, Seite 125 · nur zur Anschauung', 'Postkarte Strand Hotel Schlössli aus der Luft')

    # ------------------------------------------------------------ 3 Noten
    noten = blatt(3, 'noten', 'Noten', ['Was andere', 'darüber sagen.'],
                  'Abgelesen am 19. Oktober 2026, jede an ihrer Quelle. Die GaultMillau-Punkte stehen dort nur als Zeichen einer Symbolschrift; das Zeichen heisst «Points15».',
                  tab(['Portal', 'Note', 'Anzahl', 'Beleg'], [
                      ['Google Maps', '4,2 von 5 (62 · 5 · 4 · 1 · 13)', '85 Rezensionen, 138 Fotos', b('eingebauter Browser')],
                      ['GaultMillau', '15 Punkte (Guide 2027); 14 und «Entdeckung des Jahres 2026» im Guide 2026', '–', b('gaultmillau-punkte-beleg.md · TZ 08.10.2025, 06.10.2026')],
                      ['Guide Michelin', 'empfohlen, «Favorit der Inspektoren», Selektion 2025', '–', b('Selektion 2026 am 02.11.2026')],
                      ['Falstaff', '91 von 100 (44 · 19 · 19 · 9)', '–', b('Magazine Switzerland 5/2026')],
                      ['Der Feinschmecker', '2,5 von 5', '–', b('feinschmecker.de')],
                      ['TripAdvisor', O, O, b('Chrome-Erweiterung nicht verbunden')],
                      ['Booking.com', 'betrifft nicht', '–', b('kein Hotel')]]), 'fl--papier')

    # ------------------------------------------------------------ 4 Fakten mit Quelle
    F = FAKT
    def w(x):
        return e(str(x['wert'])) if x.get('wert') is not None else O
    def qq(x):
        return b(e(x['quelle'])[:170])
    P = F['preise_ab']
    fz = [['Name', w(F['name']), qq(F['name'])], ['Adresse', w(F['adresse']), qq(F['adresse'])], ['Lage', w(F['lage']), qq(F['lage'])],
          ['Telefon · Mail', e(F['telefon']['wert'] + ' · ' + F['mail']['wert']), qq(F['mail'])],
          ['Betreiberin', w(F['rechtstraeger']), qq(F['rechtstraeger'])], ['Pacht', w(F['pacht']) + '<br><span class="bf-offen">Eigentümer der Liegenschaft: offen</span>', qq(F['pacht'])],
          ['Urheberrechte', w(F['urheberrechte']), qq(F['urheberrechte'])], ['Zimmer', 'keine', qq(F['zimmer']['anzahl'])],
          ['Öffnungszeiten', w(F['oeffnungszeiten']), qq(F['oeffnungszeiten'])], ['Ferien', w(F['saison']), qq(F['saison'])]]
    fz += [[k, w(P[s]), qq(P[s])] for k, s in [('À la carte', 'a_la_carte'), ('Lunch', 'lunch'), ('Lästermeile', 'laestermeile'), ('Bankettmenüs', 'bankettmenues'), ('Wein', 'wein'), ('Anlässe', 'anlaesse')]]
    fz += [['Räume', w(F['raeume']) + '<br><span class="bf-offen">Namen der Etagen: offen</span>', qq(F['raeume'])],
           ['Lästermeile', e(F['restaurants'][1]['wert']['art']), qq(F['restaurants'][1])],
           ['Reservieren', 'gastronovi, Restaurant 118851; Bankett und Anlässe per Mail-Link', qq(F['buchungsweg'])],
           ['Gutschein', w(F['gutschein']), qq(F['gutschein'])], ['Anreise', w(F['anreise']), qq(F['anreise'])],
           ['Hausregeln', w(F['hausregeln']), qq(F['hausregeln'])],
           ['Team', ' · '.join(e(p['wert']['name'] + ' (' + p['wert']['rolle'].split(',')[0].split(' (')[0] + ')') for p in F['personen'][1:7]), b('_quelle/website/text/uber-uns.md; Presse')],
           ['Sprachen der Seite', 'Deutsch; keine Karte in anderer Sprache', qq(F['sprachen_website'])],
           ['Rechtstexte', 'Impressum, Datenschutz, AGB als Text; Widerruf: keine eigene Seite, Annullation in den AGB', b('_quelle/website/text/')],
           ['Zeichen', w(F['zeichen']), qq(F['zeichen'])], ['Fotografen', O + ' (kein Name in den Dateien)', b('_quelle/fotografen-aus-metadaten.json')],
           ['Social', 'Instagram @schloessli_bottighofen (2’601 Follower, 46 Beiträge); kein Facebook verlinkt, kein YouTube', b('_quelle/extern/ig/')]]
    fakten = blatt(4, 'fakten', 'Fakten mit Quelle', ['Jede Angabe', 'mit ihrer Datei.'],
                   'Auszug aus fakten.json. Preise und Namen stehen dort, wie sie in den Karten des Hauses stehen; die Karten selbst liegen als PDF und als Text bei.',
                   tab(['Angabe', 'Wert', 'Quelle'], fz), 'fl--nacht')

    # ------------------------------------------------------------ 5 Geschichte
    zeit = [('1676', 'Das Kloster Münsterlingen erlaubt dem Untermüller Hafen ein «Haus am See» für seinen Sohn, zuerst «Seeburg» genannt. Erste Bedingung: darin darf nicht gewirtet werden.', 'Gemeindeschrift 1994, S. 104–108'),
            ('um 1690', 'Der Sohn setzt trotzdem einen Wirt als Pächter ein, der die Schiffsleute bewirtet; statt eines Wirtshausschilds hängt ein Besen heraus. 1699 verliert er vor der Tagsatzung.', 'Gemeindeschrift 1994, S. 110–111'),
            ('1869', 'Die Fischenz im Konstanzer Trichter wird «einziges privates Fischereirecht am Bodensee» des Schlössli-Besitzers.', 'Gemeindeschrift 1994, S. 122'),
            ('1888', '«Hotel und Pension Schlössli, Bottighofen, b. Constanz» eröffnet im Juni; später «Strandhotel Schlössli», 1937 renoviert, bis nach 1988.', 'Gemeindeschrift 1994, S. 123–124'),
            ('heute', 'Das Schlössli ist ein Wohnhaus. Die Wirtschaft am Schlössli liegt im ehemaligen Hafenmeistergebäude.', 'Gemeinde Bottighofen; Wikipedia'),
            ('2023/24', '«Strandwirtschaft Schlössli» der GASTRO GROUP 5 AG am Hafen, mit «Läschtermeile Charte».', 'Web-Archiv'),
            ('2021', 'CK Gastro Consulting GmbH eingetragen (29.04.2021), Christian Kuchler 199 von 200 Anteilen.', 'Handelsregister Thurgau'),
            ('2025', 'Eröffnung am 3. April, Christian Kuchler als Pächter, Küchenchefin Monika Huber, Patissière Theresa Hermann, Gastgeber Jonas Volpert. Im Oktober 14 GaultMillau-Punkte und «Entdeckung des Jahres 2026».', 'GaultMillau 30.03.2025; Thurgauer Zeitung 08.10.2025'),
            ('2026', '15. GaultMillau-Punkt (06.10.2026), Falstaff 91.', 'Thurgauer Zeitung; gaultmillau.ch; falstaff.com')]
    zl = '<ul class="sa-zeit">' + ''.join(f'<li data-a="auf"><b>{j}</b><div>{e(t)}<small>{e(s)}</small></div></li>' for j, t, s in zeit) + '</ul>'
    geschichte = blatt(5, 'geschichte', 'Geschichte mit Beleg', ['Ein Pächter am See,', 'schon um 1690.'],
                       'Nur Jahreszahlen, die eine Quelle hat. Das Kapitel «Das Schlössli am See» liegt als PDF und als Text (Texterkennung) bei; Zitate vor Gebrauch am PDF prüfen. Das Baujahr des Hafenmeistergebäudes steht nirgends.',
                       zl, 'fl--papier')
    f2 = fenster(b_plat, 'Die Terrasse unter den Platanen, direkt am Wasser: «Die schönste Terrasse am Bodensee», sagt Christian Kuchler. Ein Foto der heutigen Seite, 2500 px.',
                 'Terrasse · schloessli-bottighofen.ch', 'Terrasse der Wirtschaft am Schlössli unter Platanen')

    # ------------------------------------------------------------ 6 Lücken
    stand = json.load(open(os.path.join(HIER, 'stand.json'), encoding='utf-8'))
    lk = ''.join(f'<li data-a="auf">{e(p["punkt"])}<small>{e(p["wo"])}</small></li>' for p in stand.get('offen', []))
    luecken = blatt(6, 'luecken', 'Lücken', ['Was offen ist,', 'in Rot.'],
                    'Jeder Punkt steht auch in stand.json und auf der Karte. Was nicht öffentlich ist, bleibt offen; nichts davon ist geschätzt.',
                    f'<ul class="sa-luecken">{lk}</ul>', 'fl--nacht')

    # ------------------------------------------------------------ 7 Nicht bekommen, Rechte, Sprachen
    nb = [('TripAdvisor', 'Chrome mit der Claude-Erweiterung war nicht verbunden; nach Auftrag nicht anders versucht.'),
          ('Google Maps', 'Ohne Anmeldung nur Note, Verteilung, Anzahl und Zahl der Fotos; drei Rezensionen sichtbar, Sprachen der übrigen nicht.'),
          ('Instagram', 'Nur die zwölf sichtbaren Beiträge in 640 px, Reels nur als Standbild. Facebook ist nicht verlinkt.'),
          ('Grosse Originale', 'Squarespace liefert höchstens 2500 px. Grösser nur beim Haus oder den Fotografen.'),
          ('Filme', 'Kein eigener Kanal, keine Filme Dritter gefunden.'),
          ('Presse', 'Thurgauer Zeitung und Südkurier nur bis zur Bezahlschranke.')]
    sp = SPR
    nicht = blatt(7, 'nicht', 'Nicht bekommen, Rechte, Sprachen', ['Ehrlich,', 'was fehlt.'],
                  'Inhalte und Bilder der Seite gehören laut Impressum der Taverne zum Schäfli AG «oder den speziell genannten Rechtsinhabern»; in den Dateien steht kein Fotograf. Ob das Haus die Rechte für eine neue Seite hat, ist offen. Feuerwerk, Gastkoch-Porträt und Festival-Logo gehören Dritten; Portal-, Presse- und Heftbilder nur zur Anschauung.',
                  '<ul class="bf-liste">' + ''.join(f'<li data-a="auf" style="--i:{min(k, 6)}"><b>{t}</b>{x}</li>' for k, (t, x) in enumerate(nb)) + '</ul>' +
                  tab(['Sprachen', 'Was', 'Quelle'], [
                      ['Gäste', O + ' (keine Zahlen je Sprache ablesbar)', b('sprachen.json')],
                      ['Seite heute', ', '.join(sp['website_heute']), b(e(sp['website_heute_quelle']))],
                      ['Ort', ', '.join(sp['ort']), b(e(sp['ort_quelle']))],
                      ['Schweiz Tourismus', ', '.join(sp['schweiz_tourismus']), b('myswitzerland.com, hreflang')],
                      ['Reihenfolge', ' → '.join(sp['reihenfolge']), b(e(sp['reihenfolge_grund'])[:170])]]), 'fl--papier')

    paar = f'''<div class="bf-paar">
  <figure data-a="auf"><img src="{b_bar}" alt="Bar der Wirtschaft am Schlössli mit Zementfliesen" loading="lazy"><figcaption>Die Bar mit den Zementfliesen, von drinnen nach draussen: die «Lästermeile».</figcaption></figure>
  <figure data-a="auf" style="--i:1"><img src="{b_titel}" alt="Titelblatt der Gemeindeschrift Bottighofen Heft 2" loading="lazy"><figcaption>«Die Bottighofer Mühlen und das Schlössli am See», Gemeinde Bottighofen 1994: die Quelle für die Geschichte.</figcaption></figure>
</div>'''

    schluss = f'''<section class="schluss" id="schluss">
  <img class="schluss__b" src="{b_nacht}" alt="Die Terrasse der Wirtschaft am Schlössli am Abend" loading="lazy">
  <div class="in">
    {kap(8, 'Weiter')}
    <p class="bf-urteil" data-a="auf">Das Material liegt. <em>Station 4 kann lesen.</em></p>
    <div class="lauf"><p data-a="worte">Alles liegt in _quelle/ im Projektordner, die Übersicht als Seite, die Fakten in fakten.json, die Gäste-Sprachen in sprachen.json, der Bau-Prompt neben dem Material. Die Lücken oben bleiben offen, bis eine Quelle sie hergibt. Das Schwesterhaus Taverne zum Schäfli ist eigens gesammelt.</p></div>
    {paar}
    <div class="kn-reihe" data-a="auf">{kn('Material-Übersicht', MAT)}{kn('Bau-Prompt', PROMPT, 'kn--linie')}{kn('Sammlung Schäfli', SCHWESTER, 'kn--linie')}{kn('Heutige Seite', HEUTE, 'kn--linie', neu=True)}</div>
  </div>
</section>'''

    haupt = auftakt + vorrat + bogen + f1 + noten + fakten + geschichte + f2 + luecken + nicht + schluss
    html = K.rahmen('Sammlung', 'Station 3 der Kette: Sammlung des Materials zur Wirtschaft am Schlössli, Bottighofen.', 'Sammlung', haupt,
                    'Sammlung von Robert Reff, Tasty Studios, für die interne Kette. Fotos, Zeichen und Texte gehören ' + H.RECHTE)
    html = html.replace('../werkbank/', 'werkbank/')
    import re as _re
    html = _re.sub(r'<a [^>]*href="mailto:[^"]*"[^>]*>(.*?)</a>', r'\1', html)
    html = html.replace(f'<a class="glanz" href="werkbank/index.html">Zur Werkbank{PF}</a>', f'<a class="glanz" href="{MAT}">Material{PF}</a>')
    html = html.replace('<a class="insel__m" href="werkbank/index.html">', '<a class="insel__m" href="#">')
    K.schreib(os.path.join(HIER, 'sammlung.html'), html)
    print('sammlung.html geschrieben,', len(html) // 1024, 'KB')


if __name__ == '__main__':
    baue()
