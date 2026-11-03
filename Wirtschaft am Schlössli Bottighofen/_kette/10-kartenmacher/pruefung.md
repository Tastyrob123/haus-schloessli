---
tags: [projekt, website]
status: aktiv
---

# Prüfung der Karten · Wirtschaft am Schlössli · Station 10

Stand 19.10.2026. Geprüft mit `_karten/abgleich.py` (Daten gegen Original) und `_karten/bau.py` (neue PDF gegen Daten).

## Wie geprüft wurde

- **Weg A, Wörter:** jedes Wort der Daten im Text der Original-PDF (pdftotext -layout) und jedes Wort des Originals in den Daten, mit Anzahl.
- **Weg B, Zahlen:** jede Zahl aus einer zweiten, getrennten Lesung der Original-PDF (pdftotext -raw) gegen die Zahlen der Daten.
- **Weg C, Zeilen:** jede Preiszeile (Name, Jahrgang, Kürzel, Flasche, Preis) muss als eine Zeile im Original stehen. Gegenprobe: zwei vertauschte Preise und ein Tippfehler werden gefunden.
- **Neue PDF gegen Daten:** die gedruckte PDF wird wieder ausgelesen und Wort für Wort mit den Daten verglichen; dazu je Seite: kein Eintrag allein, keine Seite endet mit einem Titel. Alle Schriften eingebettet (pdffonts).
- Ausgenommen vom Wortvergleich: Seitenzahlen des Originals und die Fusszeile, die es auf jeder Seite wiederholt (in den Daten einmal als «fuss»).
- **Selbst gelesen, Zeile für Zeile neben dem Original:** Speisekarte (alle 20 Gerichte, 27 Preise), Lästermeile (9), Bankettmenü (15); dazu Weinkarte Seite 12 im Bild (dabei «1er» mit hochgestelltem «er» gefunden, das pdftotext als «1 er» liest; jetzt richtig, 41 Stellen).

## Übernommen aus den anderen Häusern (Stand 19.10.2026)

- Farbe wie die fertige Website («Ton in Ton» aus dem Platzteller), nicht die Farbwelt A des Markenbuchs (Website `haus.css`, `UEBERGABE.md`).
- Feste Schriftschnitte statt variabler Schrift, keine «Type 3» in der PDF (Carlton 08.10., `_karten/schriften.py`, Prüfung im Druck).
- Lesetext 11 pt, Titel gut doppelt so gross, Preise in der Titelschrift (GBR 11.10., Carlton 08.10.).
- Gleiche Seiten wie das Original, jede Rubrik ganz auf ihrer Seite, freie Höhe je Zwischenraum höchstens 6 mm, Erläuterungen am Fuss (GBR 11.10.). Prüfregel im Druck: jeder Eintrag auf der Seite seiner Rubrik.
- Kein Eintrag allein auf einer Seite, keine Seite endet mit einem Titel (GBR 12.10.).
- Ein Format für jeden Eintrag, Wein mit mehreren Flaschen = ein Eintrag mit mehreren Preisen (GBR 12.10.).
- Weinkarte in drei Ebenen: Farbe als Rubrik, Land in der Titelschrift, Region als Mono-Etikett (GBR 11.10.).
- Menüs ohne Preis je Gericht (Lunch, 4-Hands) ganz mittig, senkrecht und waagrecht, kurzes Menü grösser gesetzt, keine leere untere Hälfte (La Carte C08, Robert 18.10.).
- Dunkle Umschlagfläche als SVG (erscheint ohne «Hintergrund drucken»), Zeichen als Pfad, keine weichen Schatten (GBR 12.10., Abschnitt 8).
- Kein «1 von 2»: Seitenzahl nur in der Weinkarte, ohne Gesamtzahl (Tasty-Sprache, Unterlagen und PDF).
- Unsichtbarer Text des Originals nicht mitgesetzt («A» hinter «CHAMPAGNER/SCHAUMWEIN», Ruedihus 09.10.).
- Eindeutige Tippfehler als Liste, nicht angewendet (`_karten/berichtigt.json`, wie Gasterntal in La Carte).

## Ergebnis

| Karte | Einträge | Preise | Wörter Original / Daten | Zahlen Original / Daten | Abweichungen | Neue PDF = Daten |
|---|---|---|---|---|---|---|
| Speisekarte Oktober | 20 | 27 | 281 / 281 | 29 / 29 | 0 | ja (3 S.) |
| Lunch-Menü | 3 | 0 | 37 / 37 | 2 / 2 | 0 | ja (1 S.) |
| Lästermeile | 9 | 9 | 103 / 103 | 9 / 9 | 0 | ja (2 S.) |
| Weinkarte | 468 | 495 | 3568 / 3568 | 1502 / 1502 | 0 | ja (25 S.) |
| Bankettmenü | 15 | 15 | 187 / 187 | 21 / 21 | 0 | ja (3 S.) |
| 4-Hands-Lunch mit Patrick Stier | 11 | 0 | 85 / 85 | 3 / 3 | 0 | ja (1 S.) |

## Abweichungen mit Fundstelle

Keine. Jedes Wort und jede Zahl der Daten steht im Original, und jedes Wort und jede Zahl des Originals steht in den Daten.

## Was am Original auffällt (nicht berichtigt, so übernommen)

- Weinkarte, jede Seite: «8,1% M wSt.» mit Leerzeichen, im Bild der PDF geprüft (`_quelle/website/pdf/20261014_Weinkarte.pdf`, Fuss jeder Seite).
- Weinkarte, Seite 1: hinter «CHAMPAGNER/SCHAUMWEIN» steht in der Textschicht ein «A», im Bild unsichtbar (weiss); nicht in die Daten genommen.
- Weinkarte: Seitenzahlen beginnen mit «– 2 –»; die PDF hat kein Deckblatt.
- Weinkarte, Rotwein Franken: «0,7l» mit Komma (Weingut Rudolf Fürst, Spätburgunder Hundsrück GG), sonst überall «0.7l».
- Weinkarte: «BAYRISCHER BODENSEE» (Weisswein) und «BAYERISCHER BODENSEE» (Rosé, Rotwein); «NEUCHATEL» und «NEUCHÂTEL».
- Bankettmenü: «Süßsaures» mit ß, «knusprigen Knoblauchbrot», «KALBSHOHRÜCKEN», «OSSOBUCCHI», «MOSCARDINI ALL´ ARRABIATA».
- Lästermeile: «Pickels», «Parmesan–Piment d´espelette-Pommes,» (Gedankenstrich und Bindestrich gemischt).
- Speisekarte: «Fourme d´Ambert» mit Akut statt Apostroph.
- 4-Hands-Lunch: die Seite des Anlasses nennt ein «6-Gang-Menü», die PDF trennt neun Gänge durch ***; «Opera schnitte».
- Lunch: «(3 – Gänge – 35.- Chf)».

## Offen je Karte

### Speisekarte Oktober

- Zeitraum: Titel der Datei «Speisekarte-Oktober», die Karte selbst nennt keinen Monat und kein Jahr. PDF erstellt 30.09.2026.
- Deckblatt: das Original hat keins; «Speisekarte» ist der Name, unter dem die Seite /karten die Datei verlinkt.
- Allergene: das Haus schreibt Kürzel (G, L, E, F, S, So, En, N, Se) und VEG/OVEG; sie stehen wörtlich im Feld «zusatz». Nicht in die 14 Allergene von La Carte übertragen, weil «L = Laktose» und «S = Schalen- und Weichtiere» nicht deckungsgleich mit deren Feldern sind.

### Lunch-Menü

- Zeitraum: die Karte nennt keinen Tag. Datei «Lunch_261019» (PDF erstellt 18.10.2026, 23:44); ob 261019 der 19.10.2026 ist, sagt das Haus nicht.
- Wochentage und Uhrzeit des Lunchs nennt die PDF nicht.
- Die Karte wechselt (Startseite verlinkt jeweils die aktuelle Datei); diese Daten sind der Stand vom 19.10.2026.

### Lästermeile

- Zeitraum: die Karte nennt keinen; PDF erstellt 14.10.2026.
- Öffnungszeit «11:30 Uhr - 21:00 Uhr» steht nur auf der Seite /karten, nicht in der PDF; nicht in die Karte übernommen.
- Die Seite /karten verlinkt beim Titel «Lästermeile» eine zweite Datei (/s/Lastermeile-Homepage-2tbd.pdf), die nicht im Paket liegt; gelesen ist die Fassung 2339.
- Währung: die Karte nennt keine (Preise ohne CHF).
- Allergen-Kürzel stehen wörtlich im Feld «zusatz», wie in der Speisekarte.

### Weinkarte

- Stand: Datei «20261014_Weinkarte» (PDF erstellt 14.10.2026); die Karte nennt kein Datum.
- Offenausschank (Weine im Glas) hat die Weinkarte nicht; eine Getränke- oder Barkarte mit Bier, Aperitifs, Spirituosen und Kaffee ist online nicht zu finden.
- «M wSt.» schreibt das Haus so in jeder Fusszeile (im Bild geprüft); nicht berichtigt.
- Seitenzahlen des Originals beginnen mit «– 2 –» auf Seite 1; ein Deckblatt fehlt in der PDF.
- Weingut-Zeilen tragen das Feld «weingut»: true (Zwischentitel der Art «zw»), das Datenmodell von La Carte kennt keine eigene Art für den Erzeuger.
- Jahrgang steht im eigenen Feld «jahr», die Flaschengrösse in «einheiten» neben dem Preis.

### Bankettmenü

- Stand: PDF erstellt 29.04.2025; ob Gerichte und Preise noch gelten, sagt das Haus nicht (auch beim Baumeister offen).
- Ein Wintermenü hat das Original nicht.
- Die Preise der Gerichte nennen keine Währung; die Menüpreise stehen als «(175 CHF)» im Titel.

### 4-Hands-Lunch mit Patrick Stier

- Vorbei: Anlass am 22.02.2026, 12 Uhr (Seite /events-2-1/event-two-yf5k9). Die Karte steht nur noch als Beleg; ob sie auf La Carte gehört, entscheidet das Haus.
- Die Seite des Anlasses nennt ein «6-Gang-Menü», die PDF zählt neun durch *** getrennte Gänge; so übernommen, wie es die PDF schreibt.

## Nicht gefunden

- Keine Getränke- oder Barkarte (Bier, Aperitif, Spirituosen, Kaffee, Wein im Glas) auf der heutigen Seite. Im Web-Archiv liegt eine «Aperitif Karte» von 2024 (`_quelle/web-archiv/text/2024_speisekarten__aperitif-karte.md`), Stand und Gültigkeit unklar, nicht übernommen.
- Ältere Aktionskarten 2024 (Sommerkarte, Nachmittagskarte, «s’hät solang’s hät», Läschtermeile-Charte) nur im Web-Archiv, nicht übernommen.
- Karten in anderen Sprachen: keine.
