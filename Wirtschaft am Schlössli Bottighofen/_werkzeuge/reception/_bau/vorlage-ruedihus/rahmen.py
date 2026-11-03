#!/usr/bin/env python3
"""Siebter Schritt: die Teile, die das Carlton-Europe zu La Réception dazugebaut hat (Abnahme 16./17.10.2026, Master E16–E20, R03, R05, R06, R18, R19, R23)
und die es im Rivage nicht gibt, aus dem Carlton (_werkzeuge/reception/ dort, nur gelesen) holen und ins Kleid des Ruedihus setzen (Weg wie Doldenhorn _bau/rahmen.py):
  studio/rundgang.js, studio/zur-werkbank.js, studio/fehlermelder.js, studio/anleitung.js   (Rahmen, R03/R18/R19)
  brief-pdf.html, brief-pdf.css, brief-pdf.js, brief_pdf.js                                  (Brief als A4-PDF, E16)
  pruefung.html, pruefung.js                                                                 (Prüfseite, E20/R23)
  anleitung.html                                                                             (Anleitung, R05)
Farben: jeder Farbwert des Carlton wird über seinen Ursprung im Rivage auf den Wert des Ruedihus gesetzt (portiere.py beider Häuser),
Schrift Libre Baskerville → Gelasio, Zeichen CE → Zeichen des Ruedihus, Tapete → Butzenscheiben, Texte und Adressen des Hauses.
Jede Ersetzung mit «ers» muss genau so oft treffen wie angegeben, sonst bricht das Skript ab.
Aufruf: python3 _werkzeuge/reception/_bau/rahmen.py"""
import importlib.util, os, re, sys
HIER = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HIER)
CARLTON = os.path.expanduser('~/Desktop/Website-Projekte/Carlton-Europe Interlaken/_werkzeuge/reception')
sys.path.insert(0, HIER)
import portiere  # noqa: E402


def _carlton_portiere():
    s = importlib.util.spec_from_file_location('carlton_portiere_nur_lesen', os.path.join(CARLTON, '_bau', 'portiere.py'))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


CP = _carlton_portiere()
# Carlton-Wert → Rivage-Ursprung → Ruedihus-Wert
HEX_CD, RGB_CD = {}, {}
for riv, car in CP.HEX.items():
    HEX_CD.setdefault(car, portiere.HEX.get(riv) or riv)
for riv, car in CP.RGB.items():
    RGB_CD.setdefault(car, portiere.RGB.get(riv) or riv)
# Werte, die das Carlton selbst gesetzt hat (Rundgang, Prüfseite, Anleitung, carlton.css)
HEX_CD.update({'#0b1f40': '#321f10', '#06142b': '#1f1209', '#050f22': '#170d06', '#12305e': '#4a2e17', '#1e3c72': '#55361c', '#17356a': '#4a2c14',
               '#dcc68f': '#e6cf9f', '#b89a58': '#b78f51', '#8a7545': '#84603c', '#6e5c36': '#6a4a2a', '#f4ecdc': '#efe4d3', '#fbf6ea': '#fbf5ea',
               '#fffcf4': '#fffaf0', '#1d2a42': '#2a1a0e', '#34478a': '#5f3a1b', '#0a1230': '#1a0d05', '#c9b27a': '#c39a57', '#e3d6b4': '#e7d7c0',
               '#f7f1e5': '#f6ecdc', '#fcf8ee': '#fcf6ec', '#f6eedc': '#efe4d3', '#4a4330': '#4a3a2a', '#3d6b4a': '#46652e', '#a07a1c': '#b8862a', '#8f2a2a': '#a8321a',
               '#e6d3a0': '#f0d6a2', '#e8dbbf': '#e7d7c0', '#dccdac': '#d8c2ad', '#c2a561': '#c39a57', '#f2e3bc': '#f8e2b6', '#f3e6c3': '#f8e2b6',
               '#ecdca9': '#f0d6a2', '#0c1526': '#1f1209', '#121c3c': '#24150a', '#fffdf6': '#fffaf0', '#faf4e4': '#fbf3e2', '#faf3e1': '#fbf3e2',
               '#f2e7c8': '#f1e6d4', '#f1e6d1': '#efe3cf', '#dccaa6': '#d8c2ad', '#5b584c': '#5a4532', '#4a483f': '#4a3a2a', '#3b3a33': '#3a2a1c', '#7a1f2b': '#7a2412'})
RGB_CD.update({'11,31,64': '50,31,16', '6,20,43': '31,18,9', '5,15,34': '23,13,6', '184,154,88': '183,143,81', '220,198,143': '230,207,159',
               '138,117,69': '132,96,60', '160,128,70': '160,110,60', '120,95,50': '106,74,42', '96,68,18': '90,58,26', '230,211,160': '240,214,162', '244,236,220': '239,228,211',
               '130,108,53': '132,96,60', '12,21,38': '31,18,9', '251,246,234': '251,245,234', '232,219,191': '231,215,192'})


def kleid(t):
    t = re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: HEX_CD.get(m.group(0).lower(), m.group(0)), t)
    t = re.sub(r'rgba?\((\d+,\s*\d+,\s*\d+)', lambda m: m.group(0).replace(m.group(1), RGB_CD.get(m.group(1).replace(' ', ''), m.group(1))), t)
    t = t.replace("'Baskerville CE'", "'Gelasio'").replace('"Baskerville CE"', '"Gelasio"').replace('Baskerville CE', 'Gelasio')
    t = t.replace('libre-baskerville-400-italic.woff2', 'gelasio-400.woff2').replace('libre-baskerville-400.woff2', 'gelasio-400.woff2').replace('libre-baskerville-700.woff2', 'gelasio-700.woff2')
    t = t.replace('assets/img/tapete-navy.webp', 'assets/img/butzen-09.png').replace('tapete-navy.webp', 'butzen-09.png').replace('/700px auto', '/56px 56px')
    t = t.replace('../../assets/img/ce-gold-320.webp', 'zeichen-gold.svg').replace('ce-gold-320.webp', 'zeichen-gold.svg')
    t = t.replace('../../assets/logo/favicon.ico', '../../assets/logo/zeichen.svg')
    # helle Flächen (Prüfseite, Anleitung): Butzenscheiben Ton in Ton statt der Creme-Tapete des Carlton; Foto der Anleitung: Stube bei Kerzenlicht
    t = re.sub(r"url\('\.\./\.\./assets/img/tapete(?:-creme)?\.webp'\) 50% 0/(?:1000px auto|56px 56px)", "url('../../assets/img/butzen-07.png') 50% 0/56px 56px", t)
    t = t.replace('rgba(239,228,211,.5),rgba(239,228,211,.5)', 'rgba(239,228,211,.86),rgba(239,228,211,.86)')
    t = t.replace('assets/img/reception-l.webp', 'assets/img/stube-kerze-l.webp')
    return t

def lies(n):
    return open(os.path.join(CARLTON, n), encoding='utf-8').read()


def schreib(n, t):
    os.makedirs(os.path.dirname(os.path.join(C, n)), exist_ok=True)
    open(os.path.join(C, n), 'w', encoding='utf-8').write(t)


def ers(t, alt, neu, n=1, wo=''):
    if t.count(alt) != n:
        sys.exit(f'ABBRUCH {wo}: «{alt[:80]}» kommt {t.count(alt)}× vor, erwartet {n}×')
    return t.replace(alt, neu)


HAUS = [('Carlton-Europe Vintage Adults Hotel', 'Landgasthof Ruedihus'), ('Carlton-Europe Interlaken', 'Landgasthof Ruedihus Kandersteg'),
        ('des Carlton-Europe', 'des Landgasthof Ruedihus'), ('vom Carlton-Europe', 'vom Landgasthof Ruedihus'), ('im Carlton-Europe', 'im Landgasthof Ruedihus'),
        ('Carlton-Europe', 'Landgasthof Ruedihus'), ('Wellnessdörfli', 'Spa im Nachbarhaus'), ('8976', '9023'), ('8993', '9023')]


def texte(t):
    for a, b in HAUS:
        t = t.replace(a, b)
    return t


if __name__ == '__main__':
    # ---- Rahmen (studio/)
    t = kleid(lies('studio/rundgang.js'))
    t = ers(t, "/* La Réception · Carlton-Europe: übernommen aus control/rundgang.js (Le Bureau), dort aus dem Grand Beau-Rivage (assets/js/rundgang.js dort, 16.10.2026), Schlüssel des Hauses «rundgang-ce-…». */",
            "/* Der Gastgeber (La Réception) · Landgasthof Ruedihus: übernommen aus La Réception des Carlton-Europe (studio/rundgang.js dort, nur gelesen), dort aus dem Grand Beau-Rivage; Schlüssel des Hauses «rundgang-rh-…». */", wo='rundgang')
    t = t.replace('rundgang-ce-', 'rundgang-rh-')
    t = ers(t, 'Eine neue Karte, ein Konzert am Wochenende, geänderte Zeiten im Wellnessdörfli: hineinschreiben', 'Eine neue Karte, eine Metzgete im Herbst, geänderte Zeiten in der Stube: hineinschreiben', wo='rundgang')
    t = ers(t, 'Zimmer, Restaurant, Wellnessdörfli, Anreise, Ausflüge: alles auf einen Blick', 'Zimmer, Stuben, Karten, Anreise, Kandersteg: alles auf einen Blick', wo='rundgang')
    t = ers(t, 'Wer im Chat einen Tisch, ein Zimmer oder eine Feier anfragt, steht hier mit allen Angaben.', 'Wer im Chat oder in einem Formular der Website einen Tisch in der Stube, ein Zimmer, ein Fest oder einen Gutschein anfragt, steht hier mit allen Angaben und der Abteilung.', wo='rundgang')
    schreib('studio/rundgang.js', texte(t))

    t = kleid(lies('studio/zur-werkbank.js'))
    t = t.replace("'ce-wb'", "'rh-wb'").replace('«ce-wb»', '«rh-wb»').replace('«ce-wb', '«rh-wb')
    t = ers(t, "/* La Réception · Carlton-Europe: übernommen aus control/zur-werkbank.js (Le Bureau)", "/* Der Gastgeber (La Réception) · Landgasthof Ruedihus: übernommen aus La Réception des Carlton-Europe (dort aus control/zur-werkbank.js, Le Bureau)", wo='zur-werkbank')
    schreib('studio/zur-werkbank.js', texte(t))
    for n in ('studio/fehlermelder.js', 'studio/anleitung.js'):
        schreib(n, texte(kleid(lies(n))))

    # ---- Brief als A4-PDF (E16): Briefpapier des Ruedihus (wie ruedihus.css «Der Brief»)
    t = kleid(lies('brief-pdf.js'))
    a = t.index('  const GKOPF = {'); b = t.index('\n', a)
    t = t[:a] + "  const GKOPF = { haus: 'Landgasthof Ruedihus', zeile: 'Kandersteg · seit 1753', fuss: 'Hinder de Büele 6 · 3718 Kandersteg\\n(+41) 033 675 81 81 · info@doldenhorn.ch' };" + t[b:]
    a = t.index('  const HFARBE = {'); b = t.index('\n', a)
    t = t[:a] + "  const HFARBE = { navy: '#321f10', blau: '#6d431f', tinte: '#2a1a0e', papier: '#efe4d3', creme: '#d8c2ad', weiss: '#fbf5ea', sand: '#c98543', gold: '#f3cd94', messing: '#b78f51', taupe: '#84603c', rot: '#c42e13' };" + t[b:]
    a = t.index('  const LFARBE = {'); b = t.index('\n', a)
    t = t[:a] + "  const LFARBE = { taupe: 'rgba(132,96,60,.42)', gold: '#b78f51', navy: '#321f10' };" + t[b:]
    t = ers(t, "const SERIF = \"'Gelasio',Georgia,serif\"", "const SERIF = \"'Gelasio',Georgia,'Times New Roman',serif\"", wo='brief-pdf.js')
    t = t.replace("'Landgasthof Ruedihus')}</dd></div>", "'info@doldenhorn.ch')}</dd></div>")
    t = re.sub(r'\[("10pt \'Gelasio\'", )"italic 10pt \'Gelasio\'", "700 10pt \'Gelasio\'"\]', r'["700 10pt \'Gelasio\'", "10pt \'Instrument Sans\'", "10pt \'DM Mono\'"]', t)
    schreib('brief-pdf.js', texte(t))
    schreib('brief-pdf.html', texte(kleid(lies('brief-pdf.html'))))
    schreib('brief_pdf.js', texte(kleid(lies('brief_pdf.js'))))
    t = kleid(lies('brief-pdf.css'))
    t = re.sub(r"@font-face\{font-family:'Gelasio';font-style:italic;[^}]*\}\n?", '', t)
    t = t.replace('Briefpapier des Carlton: Papierton, Doppelrahmen mit Ecken, Kopf, Fusszeile auf jeder Seite.', 'Briefpapier des Landgasthof Ruedihus (wie ruedihus.css «Der Brief»): Blatt, feiner Goldrahmen, Kopf mit dem Zeichen, Fusszeile auf jeder Seite.')
    t += """
/* ===== Ruedihus (rahmen.py): Kleid der Hausmails (mails/01-tisch …) statt Jugendstil-Rahmen des Carlton ===== */
@font-face{font-family:'Gelasio';font-style:normal;font-weight:700;src:url('../../assets/fonts/gelasio-700.woff2') format('woff2')}
@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:400 600;src:url('../../assets/fonts/InstrumentSans-normal-400_600.woff2') format('woff2')}
@font-face{font-family:'DM Mono';font-style:normal;font-weight:400;src:url('../../assets/fonts/DMMono-normal-400.woff2') format('woff2')}
body{font-family:'Instrument Sans',system-ui,sans-serif;color:#3d2a1a}
.haus{font-family:'Gelasio',Georgia,serif;font-weight:700;text-transform:uppercase;letter-spacing:.2em;font-size:13pt;color:#321f10;padding-left:.2em}
.zeile{font-family:'Instrument Sans',system-ui,sans-serif;font-style:normal;letter-spacing:.24em;text-transform:uppercase;color:#c98543}
.betreff{font-family:'Gelasio',Georgia,serif;font-weight:700;text-transform:none;letter-spacing:0;font-size:15pt;line-height:1.2;color:#2a1a0e}
.absatz.sign::first-line{font-style:normal;color:#2a1a0e}
.kleinkopf b{font-family:'Gelasio',Georgia,serif;font-weight:700;text-transform:uppercase;letter-spacing:.16em;font-size:8.5pt}
.fuss,.seitenzahl{font-family:'Instrument Sans',system-ui,sans-serif}
"""
    schreib('brief-pdf.css', texte(t))

    # ---- Prüfseite (E20) und Anleitung (R05)
    t = kleid(lies('pruefung.html'))
    t = t.replace('src="zeichen-gold.svg" width="320" height="206"', 'src="zeichen-gold.svg" width="312" height="418"')
    schreib('pruefung.html', texte(t))
    t = kleid(lies('pruefung.js'))
    t = ers(t, "Fehlt die Vorlage: mails/anfrage.html im Projekt prüfen.", "Fehlt die Vorlage: mails/01-tisch, 02-anreise, 03-gutschein im Projekt prüfen.", wo='pruefung.js')
    t = ers(t, "    ANMELDUNG: [", "    FORMULAR: ['Ein Gast kann ein Formular der Website nicht abschicken.', 'Es fehlt eine E-Mail-Adresse oder Telefonnummer, oder sie hat eine Form, die keine sein kann. Der Gast sieht die Meldung direkt am Formular.', 'Nichts zu tun: der Gast ergänzt seine Angabe. Kommen viele solche Meldungen, das Formular auf der Website ansehen (Feld E-Mail oder Telefon).'],\n    ANMELDUNG: [", wo='pruefung.js')
    schreib('pruefung.js', texte(t))
    t = texte(kleid(lies('anleitung.html'))).replace('Antiqua (Baskerville)', 'Antiqua (Gelasio)')
    for a, b in (('Der Chat steht auf der Website unten rechts, in der Zimmermappe auf dem Handy der Gäste und hinter dem QR-Code im Zimmer. Hier landet, was Gäste anfragen, und hier sehen Sie jede Frage, die gestellt wurde.',
                  'Der Chat steht auf der Website unten rechts und in der Zimmermappe auf dem Handy der Gäste. Hier landet, was Gäste im Chat anfragen, dazu jede Anfrage aus den Formularen der Website (Tisch in der Stube, Fest-Rechner, Vor Ihrer Anreise, Ihre Abreise, Gutschein), und hier sehen Sie jede Frage, die gestellt wurde.'),
                 ('Darunter vier Arten (Zimmer, Tisch, Feier, Tagung) mit der Zahl der Anfragen', 'Darunter die Arten (Zimmer, Tisch, Fest, Sitzung, Gutschein und weitere) mit der Zahl der Anfragen'),
                 ('Möchte ein Gast einen Tisch, eine Feier, eine Tagung oder ein Zimmer mit persönlichem Angebot und nennt Name und Kontakt, legt der Chat die Anfrage in den Eingang.',
                  'Möchte ein Gast einen Tisch, ein Fest, eine Sitzung oder ein Zimmer mit persönlichem Angebot und nennt Name und Kontakt, legt der Chat die Anfrage in den Eingang. Ebenso landet hier jede Anfrage aus einem Formular der Website, mit der Abteilung, an die sie ging (Rezeption, Event, Personal), und der Seite, von der sie kam.'),
                 ('«Eingang» öffnen. Oben die Auswahl «Alle», «Offen», «Erledigt» mit der Zahl.',
                  '«Eingang» öffnen. Oben die Abteilungen mit der Zahl offener Anfragen, darunter die Auswahl «Alle», «Neu», «Offen», «Erledigt».'),
                 ('Er folgt der Mail «Ihre Anfrage ist bei uns» und schreibt in der Sprache des Gastes (Deutsch, Englisch oder Französisch).',
                  'Er folgt den Mails des Hauses («Ihr Tisch in der Stube», «Bald sind Sie bei uns», «Ihr Gutschein ist da»), schreibt in der Sprache des Gastes (Deutsch, Englisch oder Französisch) und unterschreibt mit der Abteilung, an die die Anfrage ging.'),
                 ('Ist alles beantwortet, «Erledigt» drücken. Die Anfrage bleibt in der Liste, blasser, und lässt sich mit «Wieder offen» zurückholen.',
                  'Ist alles beantwortet, «Erledigt» drücken. Die Anfrage bleibt in der Liste, blasser, und lässt sich mit «Wieder offen» zurückholen.'),
                 ('(Haus, Halle, Zimmer, Dachterrasse, Kaminbar, Festsaal …)', '(Fassade, Giebel, Stuben, Ofestübli, Himmelbett, Liebeslaube, Festtafel …)'),
                 ('zum Beispiel dass der Festsaal an dem Tag frei ist', 'zum Beispiel dass die Jungestube an dem Tag frei ist'),
                 ('nach Themen: Essen &amp; Trinken, Zimmer &amp; Buchung, Hund, Wellness &amp; Haus, Anreise &amp; Abreise, Ausflüge &amp; Region, Feiern &amp; Tagen, Jobs.',
                  'nach Themen: Essen &amp; Stuben, Zimmer &amp; Buchung, Feste im Haus, Gutscheine, Spa im Nachbarhaus, Anreise &amp; Abreise, Ausflüge &amp; Region, Hund, Stellen.'),
                 ('(Karten, Hundeinformationen, Bankett, Seminar)', '(Schpiszettel, Schpis Charte, Tagesteller, Menuvorschläge)'),
                 ('Anfragen mit Namen bleiben zwölf Monate gespeichert; so steht es im Datenschutz der Website, Abschnitt «KI-Assistent der Rezeption».',
                  'Anfragen mit Namen bleiben zwölf Monate gespeichert; für den Chat steht es so im Datenschutz der Website, Abschnitt «KI-Assistent der Rezeption».')):
        t = ers(t, a, b, wo='anleitung')
    schreib('anleitung.html', t)
    print('Rahmen, PDF-Satz, Prüfseite und Anleitung im Kleid des Ruedihus')
