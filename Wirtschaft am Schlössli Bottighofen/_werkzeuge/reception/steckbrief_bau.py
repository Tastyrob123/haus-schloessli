#!/usr/bin/env python3
"""Steckbrief für «Das weiss der Chat» der Wirtschaft am Schlössli, Bottighofen (Nachtbau 3.11.2026; Bauskript aus dem Stamm, Zeilen des Hauses).

Jede Zeile: Stichwort, Angabe, Beleg. Der Beleg ist eine Stelle, die wörtlich in `gast/gast_wissen.txt` (Website und Karten des Hauses, aus
website/inhalt/*.json) oder `gast/gast_umgebung.txt` (Lage, Anreise, Geschichte aus der Sammlung, Station 3) steht; dieses Skript bricht ab, wenn ein
Beleg dort nicht vorkommt oder eine Zahl der Angabe nicht im Umfeld des Belegs steht (nichts abgetippt oder verschönert).
Bewusst NICHT im Steckbrief, weil die Quellen es nicht sagen: Kinderstuhl, Rollstuhl, Namen der zwei Etagen, ob ein Kursschiff anlegt.
«Veranstaltungen» und «Fragen & Antworten» füllt das Team selbst.
Ergebnis: steckbrief.json daneben, gelesen von gedaechtnis.py. Nach jedem neuen Wissen (python3 _bau/schloessli_wissen.py) erneut laufen lassen.
Aufruf: python3 _werkzeuge/reception/steckbrief_bau.py"""
import hashlib, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WISSEN = os.path.join(HIER, 'gast')
DATEIEN = ('gast_wissen.txt', 'gast_umgebung.txt')

# Bereich → Gruppen → Zeilen (Stichwort, Angabe, Beleg, weitere Belege …)
S = [
 ('Das Haus', [
  ('Auf einen Blick', [
   ('Adresse', 'Seestrasse 50, 8598 Bottighofen', 'Adresse: Wirtschaft am Schlössli, Seestrasse 50, 8598 Bottighofen TG'),
   ('Telefon und E-Mail', '+41 71 688 90 92, kontakt@schloessli-bottighofen.ch', 'Telefon: +41 71 688 90 92 · E-Mail: kontakt@schloessli-bottighofen.ch'),
   ('Instagram', '@schloessli_bottighofen', 'Instagram: @schloessli_bottighofen'),
   ('Lage', 'direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen', 'Direkt im Hafen von Bottighofen gelegen mit Blick aufs Wasser und die Alpen.'),
   ('Küche', 'mediterran, mit frischen, hochwertigen Zutaten', 'Hier erwartet Sie eine kulinarische Reise in die Welt der mediterranen Küche, die mit frischen, hochwertigen Zutaten und kreativen Rezepten zubereitet wird.'),
   ('Terrasse', '«Die schönste Terrasse am Bodensee», sagt Christian Kuchler', '„Die schönste Terrasse am Bodensee“ — Christian Kuchler'),
   ('Hunde', 'willkommen (Falstaff, Tagblatt)', 'Hunde willkommen (Falstaff «Dogs allowed»'),
   ('Zahlung', 'bar, Debit, Kredit, NFC', 'Zahlung bar, Debit, Kredit, NFC'),
  ]),
  ('Auszeichnungen', [
   ('GaultMillau', '15 Punkte (Guide 2027)', 'GaultMillau: 15 Punkte (Guide 2027)'),
   ('Entdeckung des Jahres', 'Moni Huber, GaultMillau «Entdeckung des Jahres 2026»', 'GaultMillau: «Entdeckung des Jahres 2026» (Moni Huber)'),
   ('Falstaff', '91 von 100 Punkten', 'Falstaff: 91 von 100'),
   ('Guide Michelin', '«Favorit der Inspektoren»', 'Guide Michelin: «Favorit der Inspektoren»'),
  ]),
  ('Das Team', [
   ('Pächter', 'Christian Kuchler', 'Pächter: Christian Kuchler'),
   ('Gastgeber und Sommelier', 'Jonas Volpert', 'Jonas Volpert, Gastgeber & Sommelier'),
   ('Küchenchefin', 'Monika Huber', 'Monika Huber, Küchenchefin'),
   ('Sous-Chef', 'Lukas Siebel', 'Lukas Siebel, Sous-Chef'),
   ('Entremetier', 'Marco Reisinger', 'Marco Reisinger, Entremetier'),
   ('Service', 'Ole Sass', 'Ole Sass, Service'),
  ]),
 ]),
 ('Öffnungszeiten & Reservation', [
  ('Wann offen ist', [
   ('Restaurant', 'Donnerstag bis Montag, 11:30 bis 23:00 Uhr', 'Donnerstag - Montag: 11:30 Uhr - 23:00 Uhr'),
   ('Ruhetage', 'Dienstag und Mittwoch', 'Dienstag & Mittwoch Ruhetag'),
   ('Küche à la carte', '11:30 bis 13:30 und 18:00 bis 20:00 Uhr', 'Küche: 11:30 Uhr - 13:30 Uhr und 18:00 Uhr - 20:00 Uhr.'),
   ('Lästermeile', 'die Karte der Lästermeile den ganzen Tag', 'Den ganzen Tag durchgängig bieten wir die Karte der Lästermeile an.'),
   ('Ferien', '13. bis 15. November 2026 (Excellence Gourmetkreuzfahrt) und 22. Dezember 2026 bis 10. Februar 2027', '- 13. - 15. November (Excellence Gourmetkreuzfahrt)', '- 22. Dezember 2026 - 10. Februar 2027'),
  ]),
  ('Reservieren', [
   ('Online', 'über gastronovi, der Link steht auf der Website', 'Reservation online: https://services.gastronovi.com/restaurants/118851/reservation/widget (System gastronovi).'),
   ('Gruppen', 'ab 6 gebuchten Personen gilt eine Reservation als Gruppe (AGB)', 'Gruppen im Sinne dieser AGB sind Gruppen mit einer Mindestzahl von 6 gebuchten Personen.'),
  ]),
 ]),
 ('Karte & Lunch', [
  ('Die Karte', [
   ('Aufbau', 'Frankreich, Italien, Iberische Halbinsel und Klassiker', '## Frankreich', '## Italien', '## Iberische Halbinsel', '## Klassiker'),
   ('Vegetarisch', 'VEG = vegetarisch, OVEG = als vegetarische Option verfügbar; weitere vegetarische Optionen berät der Service', 'VEG = vegetarisch, OVEG = als vegetarische Option verfügbar', 'Für weitere vegetarische Optionen berät Sie gerne unser Service.'),
   ('Tortelloni', 'Tomate, Burrata, Taggiasca-Olive; vegetarisch, CHF 35, als Hauptgang 50', 'TORTELLONI (VEG/G/L/E/SE): Tomate – Burrata – Taggiasca Olive – CHF 35 / 50 (als Hauptgang)'),
   ('Allergene', 'G Gluten, L Laktose, E Eier, F Fische, S Schalen- und Weichtiere, So Soja, En Erdnüsse, N Nüsse, Se Sellerie', 'G = Gluten, L = Laktose, E = Eier, F = Fische, S = Schalen- und Weichtiere, So = Soja, En = Erdnüsse, N = Nüsse, Se = Sellerie'),
   ('Preise', 'in Schweizer Franken inkl. 8,1% MwSt.', 'Alle Preise verstehen sich in Schweizer Franken inkl. 8,1% MwSt.'),
  ]),
  ('Lunch', [
   ('Lunch-Menü', '3 Gänge, CHF 35', '(3 – Gänge – 35.- Chf)'),
   ('Die Gänge', 'Kürbissuppe, Risi e bisi, Joghurt Panna Cotta', 'Kürbissuppe: Wachtelei – Serrano Schinken', 'Risi e bisi: Reis – Miesmuschel – Erbsen – Spinat', 'Joghurt Panna Cotta: Apfelcrumble'),
  ]),
 ]),
 ('Lästermeile', [
  ('Tapas und mehr', [
   ('Tapas', 'durchgehend: Pimientos de Padrón, Patatine fritte, Croquetas, Kalamata-Oliven', '## Tapas durchgehend'),
   ('Prato', 'Aufschnitt, Käse, Pickels und Focaccia, CHF 30', 'PRATO: Aufschnitt, Käse, Pickels und Focaccia G/L – CHF 30'),
   ('Tarte flambée', 'vegetarisch oder mit Speck, CHF 20', 'TARTE FLAMBÉE: Vegetarisch oder mit Speck G/L – CHF 20'),
   ('Süsses', 'Kuchen vom Blech CHF 7, Löffeldessert im Glas CHF 9', 'TARTA: hausgemachter Kuchen vom Blech G/L/N – CHF 7', 'DOLCE AL CUCCHIAIO: Geschichtetes Löffeldessert im Glas G/L/N – CHF 9'),
  ]),
 ]),
 ('Wein', [
  ('Der Keller', [
   ('Weinkarte', '468 Weine, Schwerpunkt Bündner Herrschaft, Burgund und Champagne', 'Die Weinkarte hat 468 Weine.', 'Der Schwerpunkt liegt auf der Bündner Herrschaft, dem Burgund und der Champagne.'),
   ('Sommelier', 'Jonas Volpert, Sommelier und Gastgeber', 'Weinauswahl von Sommelier und Gastgeber Jonas Volpert'),
   ('Gruppen', 'Champagner & Schaumwein, Weisswein, Rosé, Rotwein, Süsswein', '## Champagner & Schaumwein', '## Weisswein', '## Rosé', '## Rotwein', '## Süsswein'),
  ]),
 ]),
 ('Bankette & Gruppen', [
  ('Platz und Form', [
   ('Plätze', 'zwei Etagen für jeweils bis zu 26 Personen', 'Wir haben auf zwei Etagen Platz für jeweils bis zu 26 Personen'),
   ('Speisenform', 'Tavolata oder gesetztes Menue', 'Sie geben den Rahmen vor - ob Tavolata oder gesetztes Menue!'),
   ('Besprechen', 'unkompliziert, gerne auch vor Ort in Ruhe', 'wir können das sehr gerne auch vor Ort in Ruhe besprechen.'),
  ]),
  ('Bankettmenüs', [
   ('Frühling', 'CHF 175', '## Bankettmenü Frühling (175 CHF)'),
   ('Sommer', 'CHF 185', '## Bankettmenü Sommer (185 CHF)'),
   ('Herbst', 'CHF 175', '## Bankettmenü Herbst (175 CHF)'),
   ('Auswahl', '3 bis 5 Gerichte aus den Menüs, mischen und anpassen möglich', 'Aus den Menüs können 3-5 Gerichte ausgewählt werden. Nach Belieben können die Menüs auch gemischt werden'),
  ]),
 ]),
 ('Gutschein', [
  ('Bestellen', [
   ('Wofür', 'einen Abend unter der Platane, einen Lunch am Hafen oder die Lästermeile', 'Für einen Abend unter der Platane, einen Lunch am Hafen oder die Lästermeile.'),
   ('Angaben', 'Name, E-Mail, Adresse und Betrag', 'Für den Gutschein fragt das Haus: Name Käufer, E-Mail, Adresse, Betrag.'),
   ('Bestätigung', 'sobald der Gutschein versendet wurde', 'Wir senden Ihnen eine Bestätigung, sobald der Gutschein versendet wurde.'),
  ]),
 ]),
 ('Anlässe & Events', [
  ('Als Nächstes', [
   ('Excellence Gourmetkreuzfahrt', '13. bis 15. November 2026, Four-Hands-Dinner mit Dieter Koschina an Bord der Excellence Countess', 'Steht bevor: 13. bis 15. November 2026', 'Four-Hands-Dinner auf der Excellence Countess!'),
   ('Restaurant geschlossen', 'während der Gourmetkreuzfahrt, das Team ist an Bord', 'Unser Restaurant ist über diese drei Tage geschlossen, da unser Team geschlossen mit an Board ist.'),
  ]),
  ('Was war', [
   ('Seenachtfest', '7. bis 8. August 2026, Feuerwerk mit Sicht von der Terrasse', 'War: 7. bis 8. August 2026', 'wir haben beste Sicht von unserer Terrasse auf dieses Spektakel!'),
   ('Ehemaligen Lunch', 'Sonntag, 6. September 2026', 'War: Sonntag, 6. September 2026'),
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
   ('Am Hafen', 'Schifflände, Bootshafen und Bootstankstelle; ob ein Kursschiff anlegt, beim Haus fragen', 'am Hafen liegen die Schifflände, der Bootshafen und die Bootstankstelle.'),
  ]),
  ('Geschichte', [
   ('1676', 'Erlaubnis für ein «Haus am See», das spätere Schlössli, unter der Bedingung, dass darin nicht gewirtet wird', '1676: Untermüller Hans Conrad Hafen-Schedler erhält vom Kloster Münsterlingen die Erlaubnis'),
   ('Der Besen', 'statt eines Wirtshausschilds hing nur ein Besen heraus', 'Statt eines Wirtshausschilds hing nur ein Besen heraus.'),
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
