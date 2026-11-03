#!/usr/bin/env python3
"""Beschreibung der Wirtschaft am Schlössli für den Schreibtisch des Stamms (Das Schaufenster · Website pflegen), Nachtbau 3.11.2026
(Aufbau aus dem Culinarium vom 28.10.2026, Inhalt aus dem Stand des Schlössli vom 19.–21.10.2026).
   python3 _werkzeuge/bureau/beschreibung.py          schreibt beide Dateien neu und legt die Probe-Kopie an, falls sie fehlt
   python3 _werkzeuge/bureau/beschreibung.py --pruef  zeigt nur, was geschrieben würde

Schreibt (Master Werkzeug-Bau 4.2 L17/L18):
  _Werkzeuge/haeuser/schloessli/haus.json                 Kennung, Name, Welt, Quelle
  _Werkzeuge/werkzeuge/website/haeuser/schloessli.json    Seiten, Bereiche, Angaben
Nichts wird abgetippt: Seiten aus website/*.html (jede gebaute Seite ausser 404), Telefon, Adresse und Instagram aus
website/inhalt/haus.json und nur, wenn sie auf der gebauten Startseite stehen; die Welt aus _kette/05-markenbauer/marke.json;
die Namen der anderen Werkzeuge aus _werkzeuge/oberflaeche/kleid/schloessli.js (eine Stelle). Die Website selbst wird nur gelesen."""
import json
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parent.parent
WEB = PROJEKT / 'website'
STAMM = PROJEKT.parent / '_Werkzeuge'
HAUS = 'schloessli'
REIHE = ['index.html', 'abend.html', 'karte.html', 'weinkarte.html', 'feiern.html', 'anlaesse.html', 'team.html', 'kontakt.html', 'gutschein.html',
         'impressum.html', 'datenschutz.html', 'agb.html']
FOTO_SEITE = {'impressum.html': 'bootshafen', 'datenschutz.html': 'morgen', 'agb.html': 'regal'}   # Seiten ohne eigenes Foto: Bild für Google-Texte und Listen (Hausfotos der Website)


def namen():
    roh = (PROJEKT / '_werkzeuge' / 'oberflaeche' / 'kleid' / 'schloessli.js').read_text(encoding='utf-8')
    m = re.search(r'namen:\s*\{([^}]*)\}', roh)
    return dict(re.findall(r"(\w+):\s*'([^']*)'", m.group(1))) if m else {}


def im_satz(n):
    return re.sub(r'^(Der|Die|Das) ', lambda m: m.group(1).lower() + ' ', n or '')


def seiten():
    da = {p.name for p in WEB.glob('*.html')} - {'404.html'}
    fremd = da - set(REIHE)
    if fremd:
        sys.exit('Neue Seite ohne Platz in der Beschreibung: ' + ', '.join(sorted(fremd)))
    return [d for d in REIHE if d in da]


def angaben():
    h = json.loads((WEB / 'inhalt' / 'haus.json').read_text(encoding='utf-8'))
    start = (WEB / 'index.html').read_text(encoding='utf-8')
    q = 'website/inhalt/haus.json (gebaut in alle Seiten von website/bau.py)'
    aus = [{'key': 'telefon', 'label': 'Telefon', 'art': 'telefon', 'wert': h['telefon'], 'link': 'tel:' + h['telefon_href'], 'quelle': q},
           {'key': 'strasse', 'label': 'Strasse', 'art': 'text', 'wert': h['strasse'], 'quelle': q},
           {'key': 'ort', 'label': 'PLZ und Ort', 'art': 'text', 'wert': h['ort'], 'quelle': q},
           {'key': 'mail', 'label': 'E-Mail', 'art': 'text', 'wert': h['mail'], 'quelle': q},
           {'key': 'instagram', 'label': 'Instagram', 'art': 'link', 'wert': h['instagram'], 'quelle': q}]
    return [a for a in aus if a['wert'] in start]


def beschreibung():
    s = seiten()
    n = namen()
    karten = im_satz(n.get('karten', ''))
    website = [
        ('start', 'Startseite', 'Der erste Eindruck am Hafen: Willkommen, Lästermeile, Küche, Keller, Besen, Feiern und der Abend unter der Platane.', ['index.html'], 'start'),
        ('abend', 'Ihr Abend', 'Der Abend am Tisch: wie er abläuft, was auf den Tisch kommt, und der Weg zur Reservation.', ['abend.html'], 'abend'),
        ('essen', 'Karte & Wein', f'Texte und Fotos rund um Speisekarte, Lunch, Lästermeile und Weinkarte. Gerichte, Preise und Weine pflegen Sie im {karten[4:] if karten.startswith("das ") else karten}.', ['karte.html', 'weinkarte.html'], 'tortelloni'),
        ('feiern', 'Feiern', f'Banketts und Gruppen: die zwei Etagen und die Anfrage. Die Bankettmenüs pflegen Sie im {karten[4:] if karten.startswith("das ") else karten}.', ['feiern.html'], 'gaststube'),
        ('anlaesse', 'Events & Termine', 'Der nächste Anlass und der Rückblick. Die Ferien des Hauses pflegen Sie unter «Termine».', ['anlaesse.html'], 'platanen'),
        ('team', 'Team', 'Die Menschen in Küche und Service, mit Name, Aufgabe und Foto.', ['team.html'], 'team'),
        ('kontakt', 'Kontakt & Gutschein', 'Adresse, Öffnungszeiten, Anfahrt, der Weg über das Wasser und der Gutschein.', ['kontakt.html', 'gutschein.html'], 'schild'),
        ('recht', 'Rechtliches', 'Impressum, Datenschutz und AGB im Wortlaut des Hauses.', [d for d in s if d in ('impressum.html', 'datenschutz.html', 'agb.html')], 'haus'),
    ]
    fehlt = set(s) - {d for w in website for d in w[3]}
    if fehlt:
        sys.exit('Seiten ohne Bereich: ' + ', '.join(sorted(fehlt)))
    return {
        '_lies_mich': 'Beschreibung des Hauses für das Werkzeug «website» (Das Schaufenster · Website pflegen). Wirtschaft am Schlössli, Bottighofen: Restaurant am Hafen, '
                      'keine Zimmer, nur Deutsch. Jeder Text, jede Zahl, jedes Foto wird aus den gebauten Seiten gelesen (website/ des Projekts). Läuft im Rahmen des Hauses: '
                      'http://127.0.0.1:9282/_werkzeuge/bureau/ (Wirtschaft am Schlössli Bottighofen/_werkzeuge/bureau/). Geschrieben von _werkzeuge/bureau/beschreibung.py, nie von Hand ändern.',
        'seiten': [dict({'datei': d}, **({'foto': FOTO_SEITE[d]} if d in FOTO_SEITE else {})) for d in s],
        'sprachen': [],
        'kopie': {'unter': 'website', 'ordner': ['assets', 'unterlagen'] if (WEB / 'unterlagen').is_dir() else ['assets']},
        'gesperrt': [   # Karten, Lunch, Lästermeile, Weine und Bankettmenüs pflegt das Kartenpult (Stand 21.10.2026, Wähler gegen die gebauten Seiten geprüft 3.11.2026)
            {'wahl': '#karte .ka14, #mittag-start, #feiern .mk-tisch', 'werkzeug': 'karten'},
            {'wahl': '#laender .ka__wechsel, #laender .karte-fuss, #wein-zum-gang .wzg4__r, #mittag .lum__m, #laestermeile .lmk__set', 'werkzeug': 'karten'},
            {'wahl': '#berater .keller, #berater .wf-raster, #weine .wl__filter, #weine .wk__gruppe, #weine .karte-fuss, #kopf .wkb__seite', 'werkzeug': 'karten'},
            {'wahl': '#etagen .bm, #menues .mk-tisch', 'werkzeug': 'karten'}],
        # Fuss: Karte der Schwester (Taverne zum Schäfli) pflegt das Schlössli nicht; Ferien-Zeile: eigene Ansicht «Termine» (Daten, nicht Text)
        'auslassen': ['.fz__h.b', '.ab__ferien'],
        'vorschau': {'ohne_skripte': [], 'zusatz_css': '.fenster{overflow:clip}@media (hover:none){[data-ws-e],img[data-ws-b]{cursor:pointer}}'},
        'bereiche': {
            **{k: {'an': False} for k in ('zimmer', 'preisstufen', 'packages', 'saele', 'unterlagen', 'stellen')},
            'anlaesse': {
                'name': 'Anlässe',
                'satz': 'Der nächste Anlass am Hafen mit Titel, Datum, Text und Fotos, so wie er auf der Seite «Events & Termine» steht.',
                'quellen': [{'seite': 'anlaesse.html', 'jedes': '#naechster', 'felder': [
                    {'key': 'titel', 'label': 'Titel', 'art': 'text', 'wo': '.tz__titel', 'titel': True},
                    {'key': 'ort', 'label': 'Ort und Datum', 'art': 'text', 'wo': 'p.mono'},
                    {'key': 'namen', 'label': 'Namen', 'art': 'text', 'wo': '.tz__namen'},
                    {'key': 'texte', 'label': 'Text', 'art': 'liste', 'wo': 'p.lauf'},
                    {'key': 'zeit', 'label': 'Zeit', 'art': 'zahl', 'wo': '.tz__zeit'},
                    {'key': 'bilder', 'label': 'Fotos', 'art': 'bilder', 'wo': '.tz__bild'}]}]},
            'team': {
                'name': 'Team',
                'satz': 'Jeder Mensch auf der Seite «Über uns» mit Name, Aufgabe und Foto.',
                'quellen': [{'seite': 'team.html', 'jedes': '#menschen .mensch', 'felder': [
                    {'key': 'name', 'label': 'Name', 'art': 'text', 'wo': 'h3', 'titel': True},
                    {'key': 'rolle', 'label': 'Aufgabe', 'art': 'text', 'wo': '.schild p'},
                    {'key': 'bild', 'label': 'Foto', 'art': 'bild', 'wo': 'img', 'kann_fehlen': True}]}]},
        },
        'kleid': {'zeichen': 'assets/svg/zeichen.svg', 'zeichen_art': 'maske', 'tapete': 'assets/svg/tapete-a-hell.svg', 'tapete_breite': 168, 'foto': 'start'},
        'website': [{'key': k, 'name': nm, 'satz': t, 'seiten': sei, 'foto': f} for k, nm, t, sei, f in website],
        'angaben': angaben(),
        'google': {'an': True},
        'hochladen': {'an': True, 'ordner': 'assets/img'},
        'funktionen': ['leiste_klar', 'team_wer'],
        'anleitung': '/_werkzeuge/bureau/anleitung.html',
    }


def haus():
    try:
        welt = json.loads((PROJEKT / '_kette/05-markenbauer/marke.json').read_text(encoding='utf-8')).get('welt') or 'land'
    except (OSError, ValueError):
        welt = 'land'
    return {'kennung': HAUS, 'name': 'Wirtschaft am Schlössli', 'welt': welt, 'quelle': '~/Desktop/Website-Projekte/Wirtschaft am Schlössli Bottighofen',
            'hinweis': 'Restaurant am Hafen von Bottighofen, keine Zimmer, nur Deutsch. Welt aus _kette/05-markenbauer/marke.json. '
                       'Geschrieben von _werkzeuge/bureau/beschreibung.py (Nachtbau 3.11.2026). Die Quelle wird nur gelesen, nie beschrieben.'}


def schreib(p, d):
    neu = json.dumps(d, ensure_ascii=False, indent=1) + '\n'
    if p.is_file() and p.read_text(encoding='utf-8') == neu:
        return f'{p.name}: unverändert'
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix('.tmp')
    tmp.write_text(neu, encoding='utf-8')
    tmp.replace(p)
    return f'{p.name}: geschrieben'


if __name__ == '__main__':
    b, h = beschreibung(), haus()
    if '--pruef' in sys.argv:
        print(json.dumps({'haus': h, 'beschreibung': b}, ensure_ascii=False, indent=1))
        sys.exit()
    print(schreib(STAMM / 'haeuser' / HAUS / 'haus.json', h))
    print(schreib(STAMM / 'werkzeuge/website/haeuser' / f'{HAUS}.json', b))
    print(subprocess.run([sys.executable, str(STAMM / 'werkzeuge/website/probe.py'), HAUS], capture_output=True, text=True).stdout.strip())
