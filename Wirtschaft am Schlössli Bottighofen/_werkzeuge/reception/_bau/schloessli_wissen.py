#!/usr/bin/env python3
"""Wissen des Chats für den Gastgeber der Wirtschaft am Schlössli (19.10.2026). Ersetzt für dieses Haus _bau/gast_bau.py des Ruedihus.
Liest nur, aus dem Projektordner:
  _quelle/website/text/*.md        die Seiten der heutigen Website des Hauses (abgerufen 19.10.2026), Wortlaut ohne Bilder und Links
  _quelle/website/pdf-text/*.txt   die Unterlagen der Website (Speisekarte, Lunch, Lästermeile, Bankettmenüs, Weinkarte, 4-Hands-Lunch)
  _kette/03-sammler/fakten.json    Lage, Anreise, Geschichte, Schwesterhaus (jede Zeile mit ihrer Quelle)
Schreibt: gast/gast_wissen.txt, gast/gast_umgebung.txt, gast/gast_haus.json und vorlagen/*.txt (Fragen des Hauses aus seinen eigenen Mail-Links).
Nichts wird abgetippt oder umformuliert; fehlt etwas, fehlt es auch im Chat und der Chat verweist ans Haus.
Aufruf: python3 _werkzeuge/reception/_bau/schloessli_wissen.py   (nach neuen Quellen erneut)"""
import glob, json, os, re, urllib.parse

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))     # _werkzeuge/reception
PROJ = os.path.dirname(os.path.dirname(C))
Q = os.path.join(PROJ, '_quelle', 'website')
ZIEL = os.path.join(C, 'gast')
# Seiten, die Gäste betreffen (Impressum, Datenschutz und die Bildergalerie nicht; home-1 ist eine ältere Fassung von start)
SEITEN = [('start', 'Willkommen', 'index.html'), ('uber-uns', 'Über uns', 'team.html'), ('karten', 'Karten, Banketts & Gruppen', 'karte.html'),
          ('kontakt', 'Öffnungszeiten, Kontakt und Anfahrt', 'kontakt.html'), ('events-2-1', 'Events', 'anlaesse.html'),
          ('events-2-1__excellence-g-ourmetkreuzfahrt', 'Excellence Gourmetkreuzfahrt', 'anlaesse.html'), ('events-2-1__fantastical-seenachtfest', 'Seenachtfest', 'anlaesse.html'),
          ('events-2-1__event-two-yf5k9', 'Event', 'anlaesse.html'), ('events-2-1__event-three-6jzsc', 'Event', 'anlaesse.html'),
          ('events-2-1__zqff5xzr7qhnfnil32eokk5dy6gi5q', 'Ehemaligen Lunch', 'anlaesse.html'), ('agbs', 'Allgemeine Geschäftsbedingungen', 'agb.html')]
UNTERLAGEN = [('Speisekarte-Oktober', 'Speisekarte Oktober'), ('Lunch_261019', 'Lunch-Menü'), ('Lastermeile-Homepage-2339', 'Karte der Lästermeile'),
              ('Bankettmenuvorschlage', 'Bankettmenüvorschläge'), ('4_Hands-_Stier', '4-Hands-Lunch mit Patrick Stier'), ('20261014_Weinkarte', 'Weinkarte')]


def text_aus_md(s):
    s = re.sub(r'^Quelle: .*\nAbgerufen: .*\n', '', s)
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', s)                                   # Bilder
    s = re.sub(r'\[([^\]]*)\]\((?:\\\)|\\\(|[^)])*\)', r'\1', s)                  # Links: nur der Text (Mail-Links enthalten \( und \))
    s = s.replace('\\-', '-').replace('\\.', '.').replace('**', '')
    s = re.sub(r'^Newsletter-Block\n.*?(?=\n#|\Z)', '', s, flags=re.S | re.M)       # Hinweis des Seitenbaukastens, kein Inhalt
    s = re.sub(r'[ \t]+\n', '\n', s); s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()


def fakt(d, *weg):
    for k in weg:
        d = (d or {}).get(k) if isinstance(d, dict) else None
    return d


def bau():
    os.makedirs(ZIEL, exist_ok=True)
    teile = []
    for name, titel, seite in SEITEN:
        p = os.path.join(Q, 'text', name + '.md')
        roh = open(p, encoding='utf-8').read()
        abgerufen = (re.search(r'^Abgerufen: (.+)$', roh, re.M) or [None, ''])[1]
        teile.append(f'=== Seite: {titel} · Wirtschaft am Schlössli (Entwurf: {seite}; Quelle: schloessli-bottighofen.ch, abgerufen {abgerufen}) ===\n{text_aus_md(roh)}')
    for name, titel in UNTERLAGEN:
        t = open(os.path.join(Q, 'pdf-text', name + '.txt'), encoding='utf-8').read().strip()
        t = re.sub(r'\n{3,}', '\n\n', t)
        teile.append(f'=== Unterlage des Hauses: {name} (PDF auf der Website: {titel}) ===\n{t}')
    w = '\n\n'.join(teile) + '\n'
    open(os.path.join(ZIEL, 'gast_wissen.txt'), 'w', encoding='utf-8').write(w)

    f = json.load(open(os.path.join(PROJ, '_kette', '03-sammler', 'fakten.json'), encoding='utf-8'))
    u = ['=== Talwissen: Lage und Anreise · Quelle _kette/03-sammler/fakten.json · gelesen 19.10.2026 ===',
         'Lage: ' + f['lage']['wert'] + ' (' + f['lage']['quelle'] + ')',
         'Adresse: ' + f['adresse']['wert'],
         'Anfahrt mit dem Auto und Parkplatz: ' + f['anreise']['wert'] + ' (' + f['anreise']['quelle'] + ')',
         'Hunde, Zahlung, Gruppen: ' + f['hausregeln']['wert'] + ' (' + f['hausregeln']['quelle'] + ')',
         'Reservation online: ' + f['buchungsweg']['wert']['link'] + ' (System gastronovi); Bankette und Anlässe über ' + f['mail']['wert'],
         'Ferien: ' + f['saison']['wert'] + ' (' + f['saison']['quelle'] + ')',
         '', '=== Talwissen: Geschichte des Ortes · Quelle _quelle/presse (Heft Bottighofen 1994, Gemeinde Bottighofen) · gelesen 19.10.2026 ===']
    u += ['- ' + g['wert'] + ' (' + g['quelle'] + ')' for g in f['geschichte'] if g.get('wert')]
    s = f['weitere_haeuser'][0]['wert']
    u += ['', '=== Talwissen: Das Schwesterhaus · Quelle _kette/03-sammler/fakten.json · gelesen 19.10.2026 ===',
          f"{s['name']}, {s['ort']}, {s['website']} · {s['noten']} · Patron Christian Kuchler (Pächter der Wirtschaft am Schlössli)"]
    open(os.path.join(ZIEL, 'gast_umgebung.txt'), 'w', encoding='utf-8').write('\n'.join(u) + '\n')

    haus = {'name': 'Wirtschaft am Schlössli', 'ort': 'Bottighofen', 'tel': f['telefon']['wert'], 'mail': f['mail']['wert'], 'adresse': f['adresse']['wert'],
            'zeiten': 'Donnerstag bis Montag 11:30 bis 23:00 Uhr, Dienstag und Mittwoch Ruhetag', 'fahrplan': 'sbb.ch',
            'kategorien': [], 'orte': [],   # ohne Orte kein Wetter (am Rechner nichts aus dem Netz)
            'reservation': f['buchungsweg']['wert']['link'],
            'muster': ('Frage: Habt ihr am Dienstag offen?\nAntwort: Dienstag und Mittwoch ist Ruhetag. Geöffnet ist Donnerstag bis Montag:\n'
                       '- Restaurant: 11:30 bis 23:00 Uhr\n- Küche à la carte: 11:30 bis 13:30 und 18:00 bis 20:00 Uhr\n- Lästermeile: die Tapas-Karte den ganzen Tag\n\n'
                       'Frage: Habt ihr einen Kinderspielplatz?\nAntwort: Dazu steht nichts in meinen Unterlagen. Das Team hilft Ihnen gerne weiter:\n'
                       f"- Telefon: {f['telefon']['wert']}\n- E-Mail: {f['mail']['wert']}")}
    json.dump(haus, open(os.path.join(ZIEL, 'gast_haus.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # Fragen des Hauses aus seinen eigenen Mail-Links (Wortlaut, ohne Änderung): Grundlage für den Ton der Briefe
    os.makedirs(os.path.join(C, 'vorlagen'), exist_ok=True)
    for datei, nr in (('karten', 'bankett'), ('events-2-1', 'anlass')):
        roh = open(os.path.join(Q, 'text', datei + '.md'), encoding='utf-8').read()
        m = re.search(r'\((mailto:(?:\\\)|\\\(|[^)\s])+)\)', roh)
        q = urllib.parse.urlparse(m.group(1).replace('\\(', '(').replace('\\)', ')'))
        a = urllib.parse.parse_qs(q.query)
        open(os.path.join(C, 'vorlagen', nr + '.txt'), 'w', encoding='utf-8').write(
            f"Quelle: schloessli-bottighofen.ch/{datei.split('__')[0]}, Mail-Link «{(re.search(r'\[([^\]]+)\]\(mailto', roh) or [None, ''])[1]}», abgerufen 19.10.2026\n"
            f"An: {q.path}\nBetreff: {a.get('subject', [''])[0]}\n\n{a.get('body', [''])[0].strip()}\n")
    print(f'gast/: {len(SEITEN)} Seiten + {len(UNTERLAGEN)} Unterlagen ({len(w):,} Zeichen), Umgebung {len(chr(10).join(u)):,} Zeichen, vorlagen/: bankett, anlass')


if __name__ == '__main__':
    bau()
