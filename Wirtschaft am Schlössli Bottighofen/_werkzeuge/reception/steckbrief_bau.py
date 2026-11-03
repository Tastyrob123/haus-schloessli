#!/usr/bin/env python3
"""Steckbrief für «Das weiss der Chat» der Wirtschaft am Schlössli, Bottighofen (Kopie des Bauskripts des Ruedihus, 19.10.2026; Muster Grand Beau-Rivage).

Jede Zeile: Stichwort, Angabe, Beleg. Der Beleg ist eine Stelle, die wörtlich in `gast/gast_wissen.txt` (Seiten und Karten des Hauses) oder
`gast/gast_umgebung.txt` (Lage, Anreise, Geschichte aus der Sammlung, Station 3) steht; dieses Skript bricht ab, wenn ein Beleg dort nicht vorkommt
oder eine Zahl der Angabe nicht im Umfeld des Belegs steht (nichts abgetippt oder verschönert). Bewusst NICHT im Steckbrief, weil die Quellen es
nicht sagen: Kinderstuhl, Anreise mit dem Schiff, Rollstuhl, Namen der zwei Etagen. «Veranstaltungen» und «Fragen & Antworten» füllt das Team selbst.
Ergebnis: steckbrief.json daneben, gelesen von gedaechtnis.py. Nach jedem neuen Wissen (python3 _bau/schloessli_wissen.py) erneut laufen lassen.
Aufruf: python3 _werkzeuge/reception/steckbrief_bau.py"""
import hashlib, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WISSEN = os.path.join(HIER, 'gast')
DATEIEN = ('gast_wissen.txt', 'gast_umgebung.txt')

# Bereich → Gruppen → Zeilen (Stichwort, Angabe, Beleg)
S = [
 ('Das Haus', [
  ('Auf einen Blick', [
   ('Adresse', 'Seestrasse 50, 8598 Bottighofen', 'Wirtschaft am Schlössli Seestrasse 50 8598 Bottighofen'),
   ('Telefon und E-Mail', '+41 71 688 90 92, kontakt@schloessli-bottighofen.ch', 'Tel.: +41 71 688 90 92', 'kontakt@schloessli-bottighofen.ch'),
   ('Lage', 'direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen', 'Direkt im Hafen von Bottighofen gelegen mit Blick aufs Wasser und die Alpen.'),
   ('Küche', 'mediterran, mit frischen, hochwertigen Zutaten', 'Hier erwartet Sie eine kulinarische Reise in die Welt der mediterranen Küche, die mit frischen, hochwertigen Zutaten und kreativen Rezepten zubereitet wird.'),
   ('Terrasse', '«Die schönste Terrasse am Bodensee», sagt Christian Kuchler', '„Die schönste Terrasse am Bodensee“ — Christian Kuchler'),
   ('Hunde', 'willkommen (Falstaff, Tagblatt)', 'Hunde willkommen (Falstaff «Dogs allowed»'),
   ('Zahlung', 'bar, Debit, Kredit, NFC', 'Zahlung bar, Debit, Kredit, NFC'),
  ]),
  ('Das Team', [
   ('Gastgeber und Sommelier', 'Jonas Volpert', '## Jonas Volpert Gastgeber & Sommelier'),
   ('Küchenchefin', 'Monika Huber', '## Monika Huber Küchenchefin'),
   ('Sous-Chef', 'Lukas Siebel', '## Lukas Siebel Sous-Chef'),
   ('Entremetier', 'Marco Reisinger', '## Marco Reisinger Entremetier'),
   ('Service', 'Ole Sass', '## Ole Sass Service'),
  ]),
 ]),
 ('Öffnungszeiten & Reservation', [
  ('Wann offen ist', [
   ('Restaurant', 'Donnerstag bis Montag, 11:30 bis 23:00 Uhr', 'Donnerstag - Montag Dienstag & Mittwoch Ruhetag 11:30 Uhr - 23:00 Uhr'),
   ('Ruhetage', 'Dienstag und Mittwoch', 'Dienstag & Mittwoch Ruhetag'),
   ('Küche à la carte', '11:30 bis 13:30 und 18:00 bis 20:00 Uhr', 'Die Küchenzeiten betreffen unsere grosse A-la-carte-Karte und die Bestellungsannahme. 11:30 Uhr - 13:30 Uhr 18:00 Uhr - 20:00 Uhr'),
   ('Lästermeile', 'die Karte der Lästermeile den ganzen Tag', 'Den ganzen Tag durchgängig bieten wir die Karte der Lästermeile an.'),
   ('Ferien', '13. bis 15. November (Excellence Gourmetkreuzfahrt) und 22. Dezember 2026 bis 10. Februar 2027', '- 13. - 15. November (Excellence Gourmetkreuzfahrt) - 22. Dezember 2026 - 10. Februar 2027'),
  ]),
  ('Reservieren', [
   ('Online', 'über gastronovi, Restaurant 118851', 'Reservation online: https://services.gastronovi.com/restaurants/118851/reservation/widget (System gastronovi)'),
   ('Gruppen', 'ab 6 gebuchten Personen gilt eine Reservation als Gruppe (AGB)', 'Gruppen im Sinne dieser AGB sind Gruppen mit einer Mindestzahl von 6 gebuchten Personen.'),
  ]),
 ]),
 ('Karte & Lunch', [
  ('Die Karte', [
   ('Aufbau', 'Frankreich, Italien, Iberische Halbinsel und Klassiker', 'FRANKREICH', 'ITALIEN', 'IBERISCHE HALBINSEL'),
   ('Vegetarisch', 'VEG = vegetarisch, OVEG = als vegetarische Option verfügbar; weitere vegetarische Optionen berät der Service', 'VEG = vegetarisch, OVEG = als vegetarische Option verfügbar Für weitere vegetarische Optionen berät Sie gerne unser Service.'),
   ('Tortelloni', 'vegetarisch, CHF 35', 'TORTELLONI VEG/G/L/E/SE 35'),
  ]),
  ('Lunch', [
   ('Lunch-Menü', '3 Gänge, CHF 35', '(3 – Gänge – 35.- Chf)'),
  ]),
 ]),
 ('Lästermeile', [
  ('Tapas und mehr', [
   ('Tapas', 'durchgehend', 'TAPAS DURCHGEHEND'),
   ('Prato', 'Aufschnitt, Käse, Pickels und Focaccia, CHF 30', 'PRATO 30 Aufschnitt, Käse, Pickels und Focaccia'),
   ('Tarte flambée', 'vegetarisch oder mit Speck, CHF 20', 'TARTE FLAMBÉE 20 Vegetarisch oder mit Speck'),
   ('Allergene', 'G Gluten, L Laktose, E Eier, F Fische, S Schalen- und Weichtiere, So Soja, En Erdnüsse, N Nüsse, Se Sellerie', 'G = Gluten, L = Laktose, E = Eier, F = Fische, S = Schalen- und Weichtiere, So = Soja, En = Erdnüsse, N = Nüsse, Se = Sellerie'),
  ]),
 ]),
 ('Bankette & Gruppen', [
  ('Platz und Form', [
   ('Plätze', 'zwei Etagen für jeweils bis zu 26 Personen', 'Wir haben auf zwei Etagen Platz für jeweils bis zu 26 Personen'),
   ('Speisenform', 'Tavolata oder gesetztes Menue', 'Sie geben den Rahmen vor - ob Tavolata oder gesetztes Menue!'),
   ('Besprechen', 'unkompliziert, gerne auch vor Ort in Ruhe', 'wir können das sehr gerne auch vor Ort in Ruhe besprechen.'),
  ]),
  ('Bankettmenüs', [
   ('Frühling', 'CHF 175', 'FRÜHLING (175 CHF)'),
   ('Sommer', 'CHF 185', 'SOMMER (185 CHF)'),
   ('Herbst', 'CHF 175', 'HERBST (175 CHF)'),
   ('Auswahl', '3 bis 5 Gerichte aus den Menüs, mischen und anpassen möglich', 'Aus den Menüs können 3-5 Gerichte ausgewählt werden. Nach Belieben können die Menüs auch gemischt werden'),
  ]),
 ]),
 ('Hausregeln (AGB)', [
  ('Veranstaltungen', [
   ('Teilnehmerzahl', 'verbindlich spätestens 2 Werktage vorher', 'die verbindliche Teilnehmerzahl für eine Veranstaltung spätestens 2 Werktage vor dem Veranstaltungstermin mitzuteilen'),
   ('Anzahlung', 'ab CHF 1000 Reservationsbetrag kann das Restaurant 50 % Anzahlung verlangen', 'ab einem Reservationsbetrag von CHF 1000.- kann das Restaurant eine Anzahlung von 50% des gesamten Buchungsbetrags verlangen'),
  ]),
 ]),
 ('Lage, Anreise & Geschichte', [
  ('Anreise', [
   ('Mit dem Auto', 'am Kreisverkehr beim Restaurant Bären in die Seestrasse Richtung Hafen, über den Bahnübergang zum Parkplatz', 'Am Kreisverkehr beim Restaurant Bären Abfahrt in die Seestrasse in Richtung Hafen, über den Bahnübergang hinweg gelangen Sie der Strasse immer weiter folgend direkt zu unserem Parkplatz.'),
   ('Parkplatz und Zug', 'ausreichend Parkplätze, Bahnhof Bottighofen in der Nähe', 'ausreichend Parkplätze und eine nahe Anbindung zum Zugverkehr mit dem Bahnhof Bottighofen'),
  ]),
  ('Geschichte', [
   ('1676', 'Erlaubnis für ein «Haus am See», das spätere Schlössli, unter der Bedingung, dass darin nicht gewirtet wird', '1676: Untermüller Hans Conrad Hafen-Schedler erhält vom Kloster Münsterlingen die Erlaubnis'),
   ('Heute', 'das Schlössli ist ein Wohnhaus, die Wirtschaft liegt im ehemaligen Hafenmeistergebäude', 'Heute: das Schlössli ist ein Wohnhaus, die Wirtschaft am Schlössli liegt im ehemaligen Hafenmeistergebäude'),
  ]),
 ]),
]

def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def main():
    quelle = {n: open(os.path.join(WISSEN, n), encoding='utf-8').read() for n in DATEIEN}
    roh = {n: norm(t) for n, t in quelle.items()}
    fehler, aus = [], []
    for bereich, gruppen in S:
        gl = []
        for gruppe, zeilen in gruppen:
            zl = []
            for was, angabe, beleg, *mehr in zeilen:
                datei = next((n for n, t in roh.items() if norm(beleg) in t), None)
                if not datei or any(not any(norm(m) in t for t in roh.values()) for m in mehr):
                    fehler.append(f'Beleg fehlt: {bereich} / {was}: «{beleg}»')
                    continue
                # jede Zahl der Angabe steht im Umfeld eines Belegs (±1500 Zeichen), nicht nur irgendwo im Wissen
                fen = ''
                for bl in [beleg] + mehr:
                    for t in roh.values():
                        i = t.find(norm(bl))
                        if i >= 0:
                            fen += t[max(0, i - 1500):i + 1500].replace('’', '')
                for zahl in re.findall(r'\d+(?:[.,]\d+)?', (gruppe + ' ' + angabe).replace('’', '')):
                    if zahl not in fen:
                        fehler.append(f'Zahl {zahl} nicht beim Beleg: {bereich} / {was}')
                fid = hashlib.sha1(f'{bereich}|{gruppe}|{was}'.encode('utf-8')).hexdigest()[:10]
                zl.append({'fid': fid, 'was': was, 'angabe': angabe, 'beleg': norm(beleg), 'datei': datei, 'mehr': [norm(m) for m in mehr]})
            gl.append({'gruppe': gruppe, 'zeilen': zl})
        aus.append({'bereich': bereich, 'gruppen': gl})
    if fehler:
        print('\n'.join(fehler)); sys.exit(1)
    json.dump({'stand': max(os.path.getmtime(os.path.join(WISSEN, n)) for n in DATEIEN), 'bereiche': aus},
              open(os.path.join(HIER, 'steckbrief.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(sum(len(g['zeilen']) for b in aus for g in b['gruppen']), 'Zeilen, alle belegt')


if __name__ == '__main__':
    main()
