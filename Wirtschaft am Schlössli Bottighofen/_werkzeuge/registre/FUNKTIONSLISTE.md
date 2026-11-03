---
tags: [projekt, website]
status: aktiv
---

# Funktionsliste Das Besucherbuch (Le Registre) · Wirtschaft am Schlössli

Vorlage: Das Besucherbuch des Berghotel Gasterntal (17./18.10.2026), dahinter Doldenhorn, Carlton-Europe (G10–G13) und Grand Beau-Rivage (Stand 16.10.2026); Rahmen aus der Oberfläche der Häuser (Kleid schloessli, «Die Bühne»). Jede Zeile ist zugleich eine Prüfung in `abnahme.js`. Letzter Lauf 21.10.2026, 04:17:36: **91 von 91 Zeilen grün** in 4 Läufen (chromium 1440, chromium 390, webkit 1440, webkit 390).

`✓` = in allen Läufen grün, in denen die Zeile gilt. «Rechner»/«Handy»: die Zeile gilt nur dort.

## Laden

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| A01 | Auftakt: beim Öffnen bleibt die Seite ruhig (alles verborgen), bis Daten, Schriften und Fotos im ersten Bild da sind (höchstens 2,5 s), dann erscheint alles auf einmal | alle | ✓ 4/4 |
| A02 | Beim Erscheinen stehen Rand, Kopf, Bühne mit Titel und Leiste schon da (nichts halb weiss, nichts leer) | alle | ✓ 4/4 |
| A03 | Jede der acht Ansichten öffnet über die Adresse (#start … #zaehlung) und zeigt ihren Titel | alle | ✓ 4/4 |
| A04 | Eine unbekannte Adresse (#gibtsnicht) öffnet die Übersicht | alle | ✓ 4/4 |
| A05 | Der Tab-Titel nennt die Ansicht («Besuche · <Name aus dem Kleid> · Wirtschaft am Schlössli») | alle | ✓ 4/4 |
| A06 | Seiten stehen mit ihrem Namen da (Startseite, Die Karte, Weinkarte, Banketts & Gruppen …, gelesen aus den Titeln der Website), nie als Dateiname | alle | ✓ 4/4 |
| A07 | ?gruss=tag hält den Gruss fest («Guten Tag.») für die Bildschirmfotos der Werkbank | alle | ✓ 4/4 |
| A08 | Ohne Schlüssel zeigt die Adresse immer Beispielwerte (auch mit ?beispiel=1 gleich), überall beschriftet | alle | ✓ 4/4 |
| A08b | Mit falschem Schlüssel antwortet auch der Dienst nur mit Beispielwerten (Beispiel-Band da, kein Knopf zu den echten) | Dienst | ✓ 4/4 |
| A09 | Fällt das Laden aus, steht «<Name> startet nicht» mit dem Grund und den Knöpfen «Neu laden» und dem Weg zur Zentrale, kein leeres Fenster | alle | ✓ 4/4 |
| A10 | Der gewählte Zeitraum wird im Browser gemerkt und beim nächsten Öffnen wieder gewählt | alle | ✓ 4/4 |
| A11 | Keine Konsolenfehler, keine toten Adressen beim Öffnen jeder Ansicht | alle | ✓ 4/4 |

## Kopf

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| B01 | Der Kopf nennt oben den Titel der Ansicht und darunter den Stand («Beispielwerte · keine echten Besuche») | Rechner | ✓ 2/2 |
| B02 | Anleitung: runder Knopf mit Hinweis, öffnet anleitung.html in neuem Tab | alle | ✓ 4/4 |
| B03 | Die Stube: runder Knopf mit Hinweis, führt zur Stube (lokal ../maison/ = _werkzeuge/maison/, online ../../maison/ = /maison/; die Adresse antwortet) | alle | ✓ 4/4 |
| B04 | «Website ansehen» öffnet die Website in neuem Tab | alle | ✓ 4/4 |
| B05 | Die Marke «Das Besucherbuch» (Zeichen des Hauses, oben links) führt zurück zur Übersicht | alle | ✓ 4/4 |
| B06 | Am Handy (Oberfläche der Häuser): im Kopf Marke und «Bereiche», Kopf-Titel und runde Knöpfe weichen; Website, Anleitung und Die Stube stehen im aufgeklappten Rand | Handy | ✓ 2/2 |

## Rand

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| C01 | Der Rand führt in die acht Ansichten (Übersicht; Die Gäste: Besuche, Herkunft, Zeit; Die Website: Seiten, Verlauf, Zur Reservation; Gut zu wissen: So wird gezählt), die aktuelle ist markiert | alle | ✓ 4/4 |
| C02 | Die Zahl hinter «Besuche» ist die Zahl der Besuche von heute (ohne Besuch heute keine Zahl; geprüft jetzt und um 16 Uhr) | Rechner | ✓ 2/2 |
| C03 | Unten im Rand stehen die Wege: Was gezählt wird, Die Stube, Kurzer Rundgang, Website ansehen, Anleitung | alle | ✓ 4/4 |
| C04 | «Was gezählt wird» öffnet «So wird gezählt» | alle | ✓ 4/4 |
| C05 | Am Handy klappt «Bereiche» den Rand auf und zu, nach der Wahl einer Ansicht schliesst er | Handy | ✓ 2/2 |

## Zeitraum

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| D01 | Unter jedem Titel wählt man 7, 30 oder 90 Tage; die gewählte ist markiert (aria-pressed), in allen sieben Ansichten mit Zahlen | alle | ✓ 4/4 |
| D02 | Der Zeitraum gilt für alle Zahlen: 7 Tage haben weniger Besuche als 30, 30 weniger als 90; die Leiste und der Satz folgen | alle | ✓ 4/4 |
| D03 | Ein neuer Zeitraum setzt die Besuchsliste zurück (erste Karte gewählt, wieder 40 Zeilen) | alle | ✓ 4/4 |
| D04 | Die Besuchstage in der Übersicht tragen Beschriftung im richtigen Abstand (7 Tage: jeder, 30: alle fünf, 90: alle fünfzehn) | alle | ✓ 4/4 |

## Leiste

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| E01 | Die Leiste unten nennt «Sie sehen Beispielwerte» und dazu den Satz «Erfunden, damit Sie sehen …» | alle | ✓ 4/4 |
| E03 | In der Vorführung gibt es keinen Knopf zu den echten Besuchen und kein «Neu laden» | alle | ✓ 4/4 |
| E04 | Am Handy ist die Leiste umgebrochen, nichts läuft aus dem Bild; «Als Tabelle sichern» steht dort unter der Besuchsliste (schloessli.css blendet ihn in der Leiste aus, wie Carlton und Doldenhorn) und ist erreichbar | Handy | ✓ 2/2 |
| E05 | Schmale Handys (390 und 320 px): keine Ansicht verrutscht seitlich, kein Knopftext abgeschnitten, Rand-Klappe und Zeitraum erreichbar | Handy | ✓ 2/2 |

## Meldungen

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| F01 | Meldungen stehen als Karte mit Kreuz, höchstens drei, und verschwinden nach fünf Sekunden von selbst; das Kreuz schliesst sofort | alle | ✓ 4/4 |

## Bühne

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| G01 | Jede Ansicht beginnt mit dem Startbild der Oberfläche: Übersicht «voll» mit dem Aussenfoto des Hauses, jede andere Ansicht «Bühne» mit eigenem Bild; Foto geladen, Titel, Satz, mindestens 240 px hoch | alle | ✓ 4/4 |
| G02 | Die Übersicht zeigt im Startbild vier Kennzahlen (Besuche, Länder, heute, zur Reservation) in der Form der Tafel des Hauses | alle | ✓ 4/4 |
| G03 | In jeder Ansicht mit Zahlen steht über dem Inhalt das Band «Beispielwerte. Diese Zahlen sind erfunden …» | alle | ✓ 4/4 |
| G04 | Der Zeitraum sitzt im Startbild jeder Ansicht (Segment-Wahl der Oberfläche) | alle | ✓ 4/4 |

## Übersicht

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| H01 | Vier Zahlen: Besuche (mit Vergleich zum Zeitraum davor), angesehene Seiten (je Besuch), Minuten je Besuch, zur Reservation (Tisch angefragt oder «Direkt buchen», Prozent der Besuche) | alle | ✓ 4/4 |
| H02 | Besuche je Tag als Säulen, eine je Tag, mit Tag und Zahl beim Darüberfahren und Datum darunter | Rechner | ✓ 2/2 |
| H03 | Zwei Blöcke: «Woher die Gäste kommen» (sechs Länder) und «Am meisten angesehen» (sechs Seiten mit Zeit im Schnitt), je mit Link zur ganzen Liste | alle | ✓ 4/4 |
| H04 | «Zuletzt zu Besuch»: die letzten fünf Besuche als Karten; ein Klick öffnet genau diesen Besuch unter «Besuche» | alle | ✓ 4/4 |
| H05 | «Alle Besuche» führt in die Besuchsliste | alle | ✓ 4/4 |

## Besuche

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| I01 | Über der Liste grenzt man ein: Alle, Zur Reservation, Bankett oder Anfrage, Anruf oder Mail, Am Handy (je mit Zahl); die Wahl ist markiert und Zur Reservation zeigt nur Besuche mit hellem Kreis | alle | ✓ 4/4 |
| I01b | Beim Wählen eines Filters oder bei «Weitere zeigen» bleibt die Seite ruhig: die Filterleiste und die Liste schweben nicht neu herein (und lassen sich sofort anklicken) | alle | ✓ 4/4 |
| I02 | Die Liste ist nach Tagen gegliedert («Heute», «Gestern», Wochentag, Datum; geprüft jetzt und um 16 Uhr Schweizer Zeit) | alle | ✓ 4/4 |
| I03 | Einen Besuch wählen wechselt nur die Karte; die Liste bleibt, wo sie ist (Seite springt nicht nach oben), genau ein Besuch ist gewählt | alle | ✓ 4/4 |
| I04 | Die Karte nennt Ort (Land), Tag, Siegel («Tisch angefragt» / ««Direkt buchen» gewählt» / «Bankett oder Anfrage» / «Anruf oder Mail» wo es zutrifft), sechs Angaben (Gekommen, Geblieben, Seiten, Gerät, Sprache, Gekommen über) und den Weg durch die Website mit Zeit je Seite | alle | ✓ 4/4 |
| I05 | Unter einer Seite im Weg stehen die Klicks dort («Fenster «Reservation» geöffnet», «Tisch angefragt», ««Direkt buchen» gewählt», «Bankettanfrage geöffnet», «Anfrage abgeschickt», «Route zum Hafen geöffnet» …) | alle | ✓ 4/4 |
| I06 | «Weitere zeigen» bringt jeweils 60 Besuche mehr; ganz unten steht, wie viele gezeigt werden («die neuesten 400») | alle | ✓ 4/4 |
| I07 | Ist eine Auswahl leer, steht «Kein Besuch in dieser Auswahl» statt einer leeren Liste | alle | ✓ 4/4 |
| I08 | Rechner (ab 1181 px): die Karte rechts reicht vom Kopf bis über die Leiste, der Hinweis sitzt unten; sie bleibt beim Scrollen unter dem Kopf stehen; ohne eigene Scrollfläche (Oberfläche der Häuser: ein langer Weg verlängert die Karte) | Rechner | ✓ 2/2 |
| I09 | Schmal (bis 1180 px) steht die Karte über der Liste; wählt man weiter unten einen Besuch, rückt die Seite zur Karte | Handy | ✓ 2/2 |

## Herkunft

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| J01 | Länder (zehn), Gekommen über (acht, «Direkt aufgerufen» für Adresse eingetippt), Orte (mit Land), Sprache, Gerät; Anteile in Prozent, Länder auf Deutsch | alle | ✓ 4/4 |

## Zeit

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| J02 | Zeit: Besuche nach Uhrzeit (24 Säulen), nach Wochentag und Stunde (Raster 7 × 24) und nach Wochentag; oben die Spitzen (meiste Besuche, stärkster Tag, ab 18 Uhr, am Wochenende) | alle | ✓ 4/4 |

## Seiten

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| J03 | Seiten: jede Seite mit Aufrufen (absteigend sortiert), Balken, Zeit im Schnitt und Klicks zur Buchung; Fusszeile «Nicht aufgeführte Seiten …» | alle | ✓ 4/4 |

## Verlauf

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| J04 | Verlauf: Besuche je Tag neben dem Zeitraum davor, Vergleichstabelle (Jetzt/Davor/Veränderung), Woche für Woche, die wichtigsten Länder im Verlauf | alle | ✓ 4/4 |

## Zur Reservation

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| J05 | Zur Reservation: neun Werte mit Prozent und gezählten Zahlen (Startseite und Karte/Weinkarte zur Reservation; «Direkt buchen»; Fenster ohne nächsten Schritt; Bankettanfrage; Anfrage abgeschickt; Anruf oder Mail; weiter zum Schäfli; Route zum Hafen), «Von welcher Seite reserviert wird», der Weg zum Tisch | alle | ✓ 4/4 |

## Schweben

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| K01 | Blätter liegen beim Öffnen tief und klein (unter dem Bild), schweben beim Auftauchen nach der Uhr (2,7 s, Feder) auf ihren Platz; nicht am Scrollen geführt | Rechner | ✓ 2/2 |
| K02 | Die grossen Zahlen zoomen aus einer Vergrösserung herein (nur Zoom, keine Verschiebung seitlich: kein Überlauf) | alle | ✓ 4/4 |
| K03 | Balken und Säulen wachsen erst, wenn ihr Blatt gut zur Hälfte im Bild ist (nicht schon beim Laden, wenn es unten liegt) | Rechner | ✓ 2/2 |
| K04 | Besuchs-Kacheln (viele gleiche Zeilen) blenden nur sanft ein: kein Weg, keine Feder | alle | ✓ 4/4 |
| K05 | Am Seitenende steht alles still an seinem Platz und nichts überdeckt etwas (jede Ansicht ganz durchgescrollt) | alle | ✓ 4/4 |
| K06 | Bei «Bewegung reduzieren» steht sofort alles da, nichts schwebt | alle | ✓ 4/4 |

## Rundgang

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| L01 | Auf jeder Seite erscheint unten rechts (über der Leiste) ein Schild «Kurzer Rundgang», fünf Sekunden lang; die Maus darauf hält es; das Kreuz schliesst; automatische Prüfungen sehen es nicht | alle | ✓ 4/4 |
| L02 | «Zeigen» (oder ?rundgang) startet den Rundgang: Lichtkegel auf dem echten Bedienelement, Karte mit «1 von 5» und Titel, Text | alle | ✓ 4/4 |
| L03 | Der Rundgang geht Schritt für Schritt (Weiter, Enter, →), zurück (←), überspringt (Überspringen, Esc), endet mit «Los geht’s»; die Karte steht neben dem Ziel, nie darauf | alle | ✓ 4/4 |
| L04 | «Kurzer Rundgang» im Rand startet ihn jederzeit, auch nach einem Ansichtswechsel (der Weg bleibt im Rand) | alle | ✓ 4/4 |
| L05 | Am Handy steht die Karte unten über dem Bild; in eingebetteten Ansichten (Werkbank, Laptop) erscheint nichts | Handy | ✓ 2/2 |

## Zählung

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| M01 | «So wird gezählt» sagt, was gezählt wird, was nie gezählt wird (kein Name, keine Adresse, kein Cookie), Aufbewahrung, eigene Geräte, Grenzen, Zugang | alle | ✓ 4/4 |
| M02 | Der Dienst gibt in der Vorführung nie echte Werte heraus (ohne Schlüssel, mit falschem Schlüssel, mit ?beispiel): immer «beispiel: true» | Dienst | ✓ 4/4 |
| Z01 | Zählung auf der Website (messung.js als Vorschlag, an der Startseite der Probe-Kopie): Öffnen zählt die Seite (Sprache des Browsers, Gerät, Sekunden); Fenster «Reservation», Tisch angefragt (erst wenn das Fenster «gesendet» zeigt), «Direkt buchen», Telefon des Hauses, Mail-Adresse, weiter zum Schäfli (Nummer des Schäfli) und Route kommen als Klicks an; das Besucherbuch zeigt den Besuch mit diesem Weg | Dienst | ✓ 2/2 |
| Z01b | Auf «Banketts & Gruppen»: die Bankettanfrage öffnen zählt; ein leeres Formular (kein «gesendet») zählt nicht als Anfrage, abgeschickt zählt es; auf «Gutschein» zählt die Bestellung als Anfrage; der Link zum Schäfli zählt | Dienst | ✓ 2/2 |
| Z02 | Nicht gezählt: Geräte mit «nicht mitzählen», automatische Browser (webdriver), Seiten der Werkzeuge | Dienst | ✓ 2/2 |

## Server

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| N01 | Mit dem Schlüssel liefert der Dienst die echten Besuche (leer, solange nichts gezählt wurde: «leer») | Dienst | ✓ 4/4 |
| N02 | Eine gültige Zeile der Website wird angenommen (204), Beginn und Ende desselben Seitenaufrufs fassen zu einem Eintrag zusammen, Klicks und Sekunden zählen | Dienst | ✓ 4/4 |
| N03 | Ungültiges wird verworfen: falsche Sprache, fremde Ereignisse, zu lange Zeilen, Fremdzeichen, Automaten (Bots, Prüfskripte) | Dienst | ✓ 4/4 |
| N04 | Datenschutz: in der Tagesdatei steht keine Adresse der Verbindung und kein Browser-Text, nur ein Kürzel, Ort und Zeiten | Dienst | ✓ 4/4 |
| N05 | Echte Werte im Werkzeug (mit ?k=): Leiste «Ein Besuch heute», Kopf-Stand, Knopf «Neu laden» (Meldung «Neu geladen»), kein Beispiel-Band, Zahlen stimmen mit dem Dienst | Dienst | ✓ 4/4 |
| N06 | Fällt der Dienst aus (mit Schlüssel), steht «<Name> ist gerade nicht abrufbar» mit Grund und bleibt stehen | Dienst | ✓ 4/4 |
| N07 | Leerer Zeitraum: «Noch kein Besuch gezählt» mit «Beispiel ansehen» (wechselt zu Beispielwerten); wenige Besuche: «Noch wenig zu sehen? Beispiel ansehen» | Dienst | ✓ 4/4 |
| N08 | Der Test-Server antwortet nur dem eigenen Rechner und gibt keine Quelltexte (.py) und keine Tagesdateien heraus | Dienst | ✓ 4/4 |

## Anleitung

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| O01 | Die Anleitung öffnet (zweimal geladen), hat zehn Kapitel (wie das Gasterntal: das Rivage neun, dazu Zeit und Verlauf, ohne den Knopf «nicht mitzählen») in vier Themen mit Bildern aus dem Werkzeug, Bild gross mit Klick und Esc, keine toten Links | alle | ✓ 4/4 |

## Nachrechnen

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| P01 | Jede Zahl im Werkzeug (7, 30 und 90 Tage) ist genau die Rechnung aus den Rohdaten der Beispielwerte, heute zur jetzigen Uhrzeit | alle | ✓ 4/4 |
| P01b | Jede Zahl im Werkzeug (7, 30 und 90 Tage) ist genau die Rechnung aus den Rohdaten der Beispielwerte, drei Tage nach der Ablage, 9:15 Uhr (Wochentage, Wochen und Vergleichszeitraum rücken mit) | alle | ✓ 4/4 |
| P02 | Was auf dem Bildschirm steht, ist richtig aus den Zahlen gerechnet: Kennzahlen, Anteile der Ranglisten an allen Besuchen (nicht an den gezeigten Plätzen), Bänder, Sätze | alle | ✓ 4/4 |
| P03 | «Als Tabelle sichern»: lädt eine CSV mit genau den Besuchen des Zeitraums (Beispielwerte im Dateinamen und je Zeile gekennzeichnet); mit Schlüssel alle echten Besuche, nicht nur 400; ohne Schlüssel gibt der Dienst nichts heraus | Dienst | ✓ 4/4 |

## Rahmen

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| Q01 | Jeder Weg im Kopf und im Rand antwortet (Website, Anleitung, Die Stube), keine tote Adresse | alle | ✓ 4/4 |
| Q02 | «Zur Werkbank» erscheint nur, wenn aus der Werkbank geöffnet (?wb=de.k5), und führt zur Werkbank; ohne Herkunft und eingebettet nie | alle | ✓ 4/4 |
| Q03 | Fehlermelder: ein Skriptfehler landet im Browser («schloessli-registre-fehler») und beim Dienst, Ladefehler nicht, höchstens 20 | Dienst | ✓ 4/4 |
| Q05 | Die Stube bekommt vom Dienst dieselben Beispielzahlen, die das Besucherbuch zur selben Zeit zeigt | Dienst | ✓ 4/4 |
| Q06 | Unter der Sicherheitsregel der Online-Fassung (CSP wie vercel.json, eingebettete Skripte gesperrt) läuft alles: Laden, Fehlermelder, Rundgang, Anleitung mit Bild gross, Tabelle sichern; keine Regelverletzung | alle | ✓ 4/4 |

## Sicherheit

| Nr. | Was das Rivage tut, im Schlössli genauso bedient | gilt | Stand |
|---|---|---|---|
| Q04 | Dienst: fremde Herkunft 403, zu grosse Zeile 413, zu viele Anfragen 429, Quelltexte und Tagesdateien nie | Dienst | ✓ 1/1 |

