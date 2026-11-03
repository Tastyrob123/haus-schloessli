#!/usr/bin/env python3
"""Wissen des Chats für das Reservationsbuch der Wirtschaft am Schlössli (Nachtbau 3.11.2026; Aufbau wie im Stamm, Inhalt des Hauses).
Liest nur, aus dem Hausordner:
  website/inhalt/haus.json          Adresse, Telefon, Mail, Zeiten, Ferien, Reservation, Anfahrt, Team, Auszeichnungen, Bankett, Gutschein, Anlässe, Geschichte
  website/inhalt/karte.json         Speisekarte nach Ländern (Speisekarte Oktober)
  website/inhalt/lunch.json         Lunch-Menü
  website/inhalt/laestermeile.json  Karte der Lästermeile
  website/inhalt/wein.json          Weinkarte (nur Überblick: Gruppen, Regionen, Erzeuger, Zahl der Weine)
  website/inhalt/bankett.json       Bankettmenüs Frühling, Sommer, Herbst
  _werkzeuge/reception/_bau/website-text/*.txt   Wortlaut der Website, wie ein Gast ihn sieht (node _bau/website_text.js), für Team, Kontakt, AGB
  _werkzeuge/reception/_bau/umgebung.txt         Lage, Anreise, Geschichte, Schwesterhaus (Sammlung Station 3, Stand des Reservationsbuchs vom 19.10.2026)
Schreibt: gast/gast_wissen.txt, gast/gast_umgebung.txt, gast/gast_haus.json und vorlagen/*.txt.
Nichts wird erfunden; jede Angabe kommt aus einer der Dateien oben. Fehlt etwas, fehlt es auch im Chat und der Chat verweist ans Team.
Aufruf: python3 _werkzeuge/reception/_bau/schloessli_wissen.py   (danach python3 _werkzeuge/reception/steckbrief_bau.py)"""
import datetime, json, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))     # _werkzeuge/reception
HAUS_DIR = os.path.dirname(os.path.dirname(C))
INHALT = os.path.join(HAUS_DIR, 'website', 'inhalt')
WT = os.path.join(C, '_bau', 'website-text')
ZIEL = os.path.join(C, 'gast')
HEUTE = datetime.date.today().isoformat()
NAV = {'Zum Inhalt', 'Menü', 'Reservation', 'Schlössli Wirtschaft', 'by Christian Kuchler'}


def lies(n):
    return json.load(open(os.path.join(INHALT, n), encoding='utf-8'))


def chf(p):
    return f'CHF {p}' if p is not None else ''


def seite_text(n, bis=None):
    """Wortlaut einer Seite ohne Leiste oben und ohne Fuss (der Fuss steht einmal als eigener Teil); Bildnachweise und Bedienwörter fallen weg."""
    roh = open(os.path.join(WT, n + '.txt'), encoding='utf-8').read()
    zeilen = roh.partition('\n\n')[2].splitlines()
    while zeilen and zeilen[0] in NAV:
        zeilen.pop(0)
    aus = []
    for i, z in enumerate(zeilen):
        if z == 'Als Nächstes' or (z == 'Willkommen' and i + 1 < len(zeilen) and zeilen[i + 1] == 'am Hafen.'):
            break
        if bis and z == bis:
            break
        if z.startswith('Foto:') or re.fullmatch(r"[\d'’.,/ –-]+|[−+·←→]|.{0,2}", z):
            continue
        aus.append(z.replace('**', ''))
    return '\n'.join(aus)


def kopf(titel, datei, quelle):
    return f'=== Seite: {titel} · Wirtschaft am Schlössli (Website: {datei}; {quelle}, abgerufen {HEUTE}) ==='


def bau():
    h = lies('haus.json')
    z = h['zeiten']
    teile = []

    # Das Haus
    aw = [f"{a['wer']}: {a['was']}" + (f" ({a['zusatz']})" if a.get('zusatz') else '') for a in h['auszeichnungen']]
    teile.append('\n'.join([
        kopf('Willkommen', 'index.html', 'inhalt/haus.json'),
        f"## {h['name']}",
        h['satz_willkommen'], h['satz_lage'], h['satz_reise'], h['satz_anlass'], h['satz_wein'],
        f"„{h['satz_terrasse']}“ — {h['satz_terrasse_von']}",
        f"GaultMillau: «{h['zitat_gm_terrasse']}»",
        f"Pächter: Christian Kuchler, «{h['by']}». Schwesterhaus: {h['schwester']['name']} in {h['schwester']['ort']} ({h['schwester']['url']}).",
        '## Auszeichnungen',
        *aw,
        f"GaultMillau über die Küche: «{h['zitat_gm_kueche']}»",
        '## Geschichte des Ortes',
        *h['besen'],
    ]))
    tm = [f"{t['name']}, {t['rolle']}" for t in h['team']]
    teile.append('\n'.join([kopf('Das Team', 'team.html', 'inhalt/haus.json'), '## Das Team', h['satz_team'], *tm,
                            '## Ein Blick in die Küche', h['weg_moni'], '## Der Weinkeller', h['zitat_jonas']]))

    # Öffnungszeiten, Ferien, Reservation, Anfahrt
    fe = [f'- {x}' for x in h['ferien']]
    kontakt = seite_text('kontakt')
    wasser = next((l for l in kontakt.splitlines() if l.startswith('Die Wirtschaft liegt direkt im Hafen')), '')
    teile.append('\n'.join([
        kopf('Öffnungszeiten, Kontakt und Anfahrt', 'kontakt.html', 'inhalt/haus.json'),
        '## Öffnungszeiten',
        f"{z['tage']}: {z['offen']}", z['ruhetag'],
        f"Küche: {z['kueche'][0]} und {z['kueche'][1]}. {z['kueche_hinweis']}",
        f"Lästermeile: {z['laestermeile']}",
        '## Ferien',
        'Ferien des Restaurants:', *fe,
        '## Reservation',
        f"Reservation online: {h['reservation']} (System gastronovi).",
        f"Telefon: {h['telefon']} · E-Mail: {h['mail']} · Instagram: {h['instagram_name']}",
        f"Adresse: {h['name']}, {h['strasse']}, {h['ort']} {h['kanton']}",
        '## Anfahrt',
        h['anfahrt'],
        f"Wir haben {h['bahn']}.",
        *( [wasser] if wasser else [] ),
    ]))

    # Karten
    k = lies('karte.json')
    zl = [kopf('Speisekarte', 'karte.html', 'inhalt/karte.json, ' + k['stand'])]
    for l in k['laender']:
        zl.append(f"## {l['land']}")
        for g in l['gerichte']:
            preis = chf(g['preis']) + (f" / {g['haupt']} (als Hauptgang)" if g.get('haupt') else '')
            zl.append(f"{g['name']} ({g['allergene']}): {g['text']} – {preis}" + (f" {g['hinweis']}" if g.get('hinweis') else ''))
    f = k['fuss']
    zl += ['## Hinweise zur Karte', f['mwst'], f['veg'], f['veg2'], 'Allergene: ' + f['allergene']]
    teile.append('\n'.join(zl))

    lu = lies('lunch.json')
    teile.append('\n'.join([kopf('Lunch-Menü', 'karte.html', 'inhalt/lunch.json, ' + lu['stand']), '## ' + lu['titel'],
                            *[f"{g['name']}: {g['text']}" for g in lu['gaenge']], f"({lu['preis']})"]))

    lm = lies('laestermeile.json')
    zl = [kopf('Lästermeile', 'index.html', 'inhalt/laestermeile.json, ' + lm['stand']), '## Lästermeile', z['laestermeile']]
    for g in lm['gruppen']:
        zl.append(f"## {g['titel']}")
        zl += [f"{e['name']}: {e['text'] + ' – ' if e['text'] else ''}{chf(e['preis'])}" for e in g['eintraege']]
    zl.append('Allergene: ' + lm['allergene'])
    teile.append('\n'.join(zl))

    w = lies('wein.json')
    zl = [kopf('Weinkarte', 'weinkarte.html', 'inhalt/wein.json, ' + w['stand']), '## Die Weinkarte', h['satz_wein'], h['zitat_jonas']]
    alle = 0
    for g in w['gruppen']:
        n = sum(len(e['weine']) for r in g['regionen'] for e in r['erzeuger'])
        alle += n
        reg = [r['titel'] for r in g['regionen'] if r['titel']]
        erz = [e['name'] for r in g['regionen'] for e in r['erzeuger']]
        zl.append(f"## {g['titel']}")
        zl.append(f"{g['titel']}: {n} Weine" + (f" aus {', '.join(reg)}" if reg else '') + '.')
        zl.append('Erzeuger: ' + ', '.join(erz[:40]) + (' und weitere.' if len(erz) > 40 else '.'))
    zl.insert(4, f'Die Weinkarte hat {alle} Weine. Einzelne Flaschen und Preise stehen auf der Weinkarte der Website.')
    zl += [x for x in w['fuss']]
    teile.append('\n'.join(zl))

    # Banketts
    b = h['bankett']; bm = lies('bankett.json')
    zl = [kopf('Banketts & Gruppen', 'feiern.html', 'inhalt/haus.json und inhalt/bankett.json, ' + bm['stand']), '## ' + b['titel'],
          b['fett'], b['rahmen'], b['individuell'], b['platz'],
          'Für die Bankettanfrage fragt das Haus: ' + ', '.join(b['felder']) + '.']
    for m in bm['menues']:
        zl.append(f"## Bankettmenü {m['name']} ({m['preis']} CHF)")
        zl += [f"{g['name']}: {g['text']} – {chf(g['preis'])}" for g in m['gerichte']]
    zl += ['## Auswahl', bm['hinweis']]
    teile.append('\n'.join(zl))

    # Gutschein
    gu = h['gutschein']
    gt = seite_text('gutschein', bis='Gutschein bestellen')
    zl = [kopf('Gutschein', 'gutschein.html', 'inhalt/haus.json und Wortlaut der Seite'), '## Gutschein']
    zl += [l for l in gt.splitlines() if not l.startswith('## ')]
    zl += ['Für den Gutschein fragt das Haus: ' + ', '.join(gu['felder']) + '.', gu['bestaetigung'] + '.']
    teile.append('\n'.join(zl))

    # Anlässe
    zl = [kopf('Events & Termine', 'anlaesse.html', 'inhalt/haus.json')]
    for a in h['anlaesse']:
        zl.append(f"## {a['titel']}")
        zl.append(('Steht bevor: ' if a.get('bevorstehend') else 'War: ') + f"{a['datum']} ({a['zeit']})")
        zl += a['text']
        if a.get('link'):
            zl.append(f"{a.get('link_text') or 'Mehr'}: {a['link']}")
    teile.append('\n'.join(zl))

    # AGB (Wortlaut der Seite)
    teile.append(kopf('Allgemeine Geschäftsbedingungen', 'agb.html', 'Wortlaut der Seite') + '\n' + seite_text('agb'))

    # Fuss jeder Seite
    teile.append('\n'.join(['=== Fuss jeder Seite (Adresse, Zeiten, Kontakt) ===',
                            f"{h['name']} · {h['by']} · {h['strasse']}, {h['ort']}",
                            f"{z['tage']} · {z['offen']} · Küche {z['kueche'][0]} und {z['kueche'][1]} · Lästermeile den ganzen Tag · {z['ruhetag']}",
                            f"{h['telefon']} · {h['mail']} · Instagram {h['instagram_name']}"]))
    wissen = '\n\n'.join(teile) + '\n'
    if re.search(r'ß', wissen.replace('Süßsaures', '')):
        print('Hinweis: ß im Wissen (Wortlaut der Karten bleibt, wie er ist)')

    # Umgebung: aus dem Reservationsbuch vom 19.10.2026 (Sammlung Station 3), Reservationsweg aus haus.json
    umg = open(os.path.join(C, '_bau', 'umgebung.txt'), encoding='utf-8').read()
    umg = re.sub(r'https://services\.gastronovi\.com/\S+', h['reservation'], umg)

    haus = {
        'name': h['name'], 'ort': 'Bottighofen', 'tel': h['telefon'], 'mail': h['mail'],
        'adresse': f"{h['strasse']}, {h['ort']}",
        'zeiten': f"{z['tage'].replace(' - ', ' bis ')} {z['offen'].replace(' Uhr - ', ' bis ')}, Dienstag und Mittwoch Ruhetag",
        'fahrplan': 'sbb.ch', 'kategorien': [], 'orte': [], 'reservation': h['reservation'],
        'muster': ('Frage: Haben Sie am Dienstag offen?\nAntwort: Dienstag und Mittwoch ist Ruhetag. Geöffnet ist Donnerstag bis Montag:\n'
                   f"- Restaurant: {z['offen'].replace(' Uhr - ', ' bis ')}\n- Küche à la carte: {z['kueche'][0].replace(' Uhr - ', ' bis ')} und {z['kueche'][1].replace(' Uhr - ', ' bis ')}\n"
                   '- Lästermeile: die Karte den ganzen Tag\n\n'
                   'Frage: Haben Sie einen Kinderspielplatz?\nAntwort: Dazu steht nichts in meinen Unterlagen. Das Team hilft Ihnen gerne weiter:\n'
                   f"- Telefon: {h['telefon']}\n- E-Mail: {h['mail']}"),
    }

    # Vorlagen der Briefe: die Fragen, die das Haus selbst stellt (Bankettanfrage, Gutschein) und die Reservation eines Anlasses (Mail-Link des Hauses)
    vorlagen = {
        'bankett': ['Quelle: Seite «Banketts & Gruppen», Bankettanfrage (website/inhalt/haus.json › bankett)', f"An: {h['mail']}", 'Betreff: Bankettanfrage', '',
                    'Guten Tag,', '', 'Gerne erhalte ich weitere Informationen für eine geplante Feier.', ''] +
                   [f'{x}:' + (' (Tavolata oder Gesetztes Menue)' if x == 'Gewünschte Speisenform' else '') for x in b['felder']] + ['', 'Gerne bin ich erreichbar via ...', '', 'Mit freundlichen Grüssen,'],
        'gutschein': ['Quelle: Seite «Gutschein», Formular (website/inhalt/haus.json › gutschein)', f"An: {h['mail']}", 'Betreff: Gutschein', '',
                      'Felder des Formulars: ' + ', '.join(gu['felder']) + '.', gu['bestaetigung'] + '.'],
        'anlass': open(os.path.join(C, '_bau', 'vorlage-anlass.txt'), encoding='utf-8').read().strip().splitlines(),
    }
    open(os.path.join(ZIEL, 'gast_wissen.txt'), 'w', encoding='utf-8').write(wissen)
    open(os.path.join(ZIEL, 'gast_umgebung.txt'), 'w', encoding='utf-8').write(umg)
    json.dump(haus, open(os.path.join(ZIEL, 'gast_haus.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.makedirs(os.path.join(C, 'vorlagen'), exist_ok=True)
    for alt in os.listdir(os.path.join(C, 'vorlagen')):
        if alt.endswith('.txt') and alt[:-4] not in vorlagen:
            os.remove(os.path.join(C, 'vorlagen', alt))
    for n, zeilen in vorlagen.items():
        open(os.path.join(C, 'vorlagen', n + '.txt'), 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')
    print(f'gast_wissen.txt {len(wissen) // 1024} kB · gast_umgebung.txt {len(umg)} Zeichen · gast_haus.json · vorlagen: {", ".join(vorlagen)}')


if __name__ == '__main__':
    bau()
