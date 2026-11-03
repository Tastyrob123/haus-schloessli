# Der Gastgeber (La Réception) · Landgasthof Ruedihus: Funktionsliste

Vorlage für Funktion und Bedienung: La Réception des Grand Beau-Rivage (`Grand Beau-Rivage/website/reception/`, `_gast/rezeption.py`, `_gast/gedaechtnis.py`, Stand 17.10.2026, nur gelesen).
Vorlage für Technik und Zusätze: La Réception des Carlton-Europe (E16–E21, F46–F49) und des Waldhotel Doldenhorn (E15/E22, Fallen), beide nur gelesen. Master: Werkzeug-Bau Abschnitt 3 (R01–R24) und 4.4 (E01–E22).

Jede Zeile ist an der Probe-Kopie bedient (`_Probe Ruedihus Reception 1710/`, Wegwerf-Daten, Probe-Antworten ohne KI). Beleg = Schritt der Prüfläufe:
`pruefung/gegenprobe.js` (01–98), `pruefung/abnahme.js` (R…, E…, C, U, Z, N), `pruefung/formular_web.js` (W01–W13), `pruefung/sicherheit.sh` (S1–S6, F1–F6, K1–K2), `pruefung/online_bedienen.js` (O1–O12).
Die Spalte «Ruedihus anders» nennt nur, was bewusst nicht gleich ist.

## A Rahmen (R01–R24)

| # | Funktion | Master | Beleg | Ruedihus anders |
|---|---|---|---|---|
| A1 | Kopfleiste: Zeichen des Hauses in Gold, «Der Gastgeber», Unterzeile, Titel der Ansicht, Zahl neuer Anfragen | R01, R05 | 01, R01/R05 | Name in Gelasio fett und Versalien wie auf den Karten des Hauses; Name der Welt Landhaus |
| A2 | Runde Knöpfe Prüfung, Anleitung, Die Stube (mit Hinweis beim Darüberfahren) | R05 | 07, R01/R05 | «Die Stube» statt «La Maison»; Weg nach Adresse (lokal `../maison/`, online `/maison/`) |
| A3 | «Chat ausprobieren» oben rechts | E11 | 80–82 | |
| A4 | Rand: Übersicht, Bereiche mit Zahlen, aktueller markiert | R06 | 04 | |
| A5 | Rand unten: Chat auf der Website, Zimmermappe, So arbeitet der Chat, Anleitung, Prüfung, Die Stube, Kurzer Rundgang | R06, E11 | 07 | |
| A6 | Leiste unten: ein Satz zum Stand, «Neu laden», «Zum Eingang» | R08 | 06 | ändert keine Website, deshalb kein «Veröffentlichen» (wie Rivage) |
| A7 | Quittungen, höchstens drei, ×, verschwinden von selbst; Fehler mit Stichwort und «Was tun?» | R11 | R11 | |
| A8 | Fenster: Abbrechen, Esc, Klick daneben schliesst | R01 | 14, 82, 97 | |
| A9 | Adresse mit `#bereich`, Neuladen bleibt dort; aus der Stube immer Übersicht | R15 | 98, R15 | |
| A10 | Bühne im Kopf jeder Ansicht mit eigenem Foto des Hauses | R16 | Bilder | Haus zur blauen Stunde, Stube bei Kerzenlicht, Ofestübli, Stube im Parterre, Giebel |
| A11 | Ruhiger Auftakt, Bewegung nur transform/opacity, «Weniger Bewegung» | R02, R17 | Messung | |
| A12 | Handy: «Bereiche» klappt auf und schliesst nach der Wahl | R07 | 96, R07 | |
| A13 | Kein seitliches Verrutschen (1440, 390) | R07 | 95, R07, W13 | |
| A14 | Prüfseite: Zustand, Browserfehler, Reparaturen mit zweitem Klick, Lexikon | R23, E20 | R23 | Stichwort FORMULAR statt WEBSITE; Punkt «Formulare der Website» |
| A15 | Fehlermelder vor allem anderen | R03 | R23 | |
| A16 | Startfehler-Tür «Der Gastgeber startet nicht.» | R04 | von Hand (Server aus) | |
| A17 | Rundgang beim ersten Öffnen, wieder über `?rundgang` | R18 | R18 | Texte nennen Stube, Formulare, Gutschein; Schlüssel `rundgang-rh-…` |
| A18 | «Zur Werkbank» nur aus der Werkbank | R19 | R19 | |
| A19 | Hell mit Bühne: Kopf Wandholz mit Butzenscheiben, Raum Papier, Kacheln Holz, Rand weiss | R21 | Bilder | |
| A20 | Kein Passwort bis zur Auslieferung (Prüfseite gelb ANMELDUNG) | R22 | R23 | |
| A21 | Sprache der Oberfläche Deutsch | R24 | – | |

## B Übersicht (E01)

| # | Funktion | Beleg | Ruedihus anders |
|---|---|---|---|
| B1 | Gruss nach Tageszeit, drei Felder (Eingang, ohne Antwort, gefragt), Zahlen = Server | 02, 03, 05 | |
| B2 | Neun Arten mit Foto, Zahl der Anfragen und offenen | 02 | **Gutschein** als eigene Art (Mail «Ihr Gutschein ist da»); Fest und Sitzung statt Feier und Tagung |
| B3 | Zuletzt angefragt, zuletzt gefragt | 02 | |

## C Eingang und Brief (E02–E06, E12–E14, E16, E17, E21)

| # | Funktion | Beleg | Ruedihus anders |
|---|---|---|---|
| C1 | Auswahl Alle, Neu, Offen, Erledigt mit Zahlen | 10, W12 | |
| C2 | Abteilungen Rezeption, Event, Personal mit Zahl offener, filtern, bleibt beim Neuladen | W12 | drei Abteilungen (kein eigenes Spa-Team, Spa im Doldenhorn) |
| C3 | Tagesgruppen, Karte mit Foto, Art, Abteilung, Uhrzeit, Website/Chat, Beispiel/Probe | 10 | |
| C4 | Öffnen macht «gelesen», Zahl sinkt | 11 | |
| C5 | Detail: Datum, Personen, Sprache, Kontakt, An (Abteilung, Adresse), Über (Chat oder Formular mit Name und Seite), Anliegen, Gespräch bzw. Nachricht | 12, W12 | «Über» nennt das Formular (Tisch in der Stube, Fest-Rechner, Vor Ihrer Anreise, Ihre Abreise, Gutschein, Bewerbung) |
| C6 | Erledigt / Wieder offen, Name im Protokoll | 13 | |
| C7 | Löschen mit Rückfrage | 14, E13 | |
| C8 | Brief auf Briefpapier, offene Stellen markiert, «Vor dem Senden» | 20, 21 | Kleid der Hausmails: Wandholz, Zeichen, Gelasio, Gruss «Herzlich, Familie Maeder und ihre Crew» |
| C9 | Gestalten wie in Canva | 22–29 | |
| C10 | 14 Hausfotos einfügen, verschieben, entfernen | 30 | Fotos des Ruedihus |
| C11 | Linien, Zeichen, Hausname, «Gestalten» mit allen Reglern, zurücksetzen | 31–36 | Hausfarben Wandholz, Balken, Kerze, Licht, Gold, Geranie |
| C12 | Nur Text: Betreff und Text, sichern | 37 | |
| C13 | Brief kopieren (gestaltete Mail und Text), Im Mailprogramm öffnen | 38, 39 | Mail im Kleid der Hausmails |
| C14 | Als PDF sichern: A4 vom Server, Dateiname «Landgasthof Ruedihus – Gast – Datum.pdf»; online Druckfenster | 40, U, O7 | |
| C15 | Neu schreiben lassen mit Hinweis | 41 | |
| C16 | Auf Deutsch lesen | 42, 43 | |
| C17 | Nichts geht beim Wechseln oder Verlassen verloren, Nachsichern bis fünfmal | C, R13, N | |
| C18 | Absender und Unterschrift nach Abteilung | W12 | |
| C19 | Neues von selbst: alle zwei Minuten | E14 | |
| C20 | Zwei Fenster am selben Brief: «Anderes Fenster war schneller», nichts überschrieben | Z | wie Carlton (E21); neu: auch ein neu geschriebener Brief zählt die Fassung weiter |
| C21 | Firefox/Handy: Antippen ohne Verrutschen, gewählter Teil über dem Blatt «Gestalten» | Handy-Läufe | wie Carlton F47 und Doldenhorn F48 |

## D Formulare der Website (E12 mit Baustein, neu im Ruedihus)

| # | Funktion | Beleg |
|---|---|---|
| D1 | Baustein `baustein/anfrage.js` fängt die vier Formulare ab, die bisher das Mailprogramm öffneten (Tisch, Fest-Rechner, Vor Ihrer Anreise, Ihre Abreise) | W01, W02, W13 |
| D2 | Anfrage-Fenster zeigt die Angaben des Formulars, verlangt E-Mail oder Telefon, Dank in der Sprache der Seite | W02–W06 |
| D3 | Freie Anfrage über `data-anfrage` (Zimmer, Tisch, Fest, Gutschein, Bewerbung, Nachricht) | W07 |
| D4 | Esc/Klick daneben schliesst, Eingaben bleiben; Netz weg: Meldung, Eingaben bleiben | W08, W09 |
| D5 | Im Eingang mit Abteilung (Fest → Event `event@`), Formular, Seite, Probe-Kennzeichen | W11, W12 |
| D6 | Weg `formular`: Kontakt geprüft (422), Maschinenfeld, eigene Grenze 6 je Minute (429), höchstens 12 kB (413), nur von der eigenen Seite (403), Antwort ohne Daten des Hauses | F1–F6, E12 |

## E Das wurde gefragt, Vom Team nachgetragen (E07, E08, E10)

| # | Funktion | Beleg | Ruedihus anders |
|---|---|---|---|
| E1 | Zahlen, «Ohne Antwort», Themengruppen | 50, 51 | Themen: Feste im Haus, Hund, Gutscheine, Spa im Nachbarhaus, Essen & Stuben, Zimmer & Buchung, Anreise & Abreise, Ausflüge & Region, Stellen |
| E2 | Lücke nachtragen, abhaken | 52, 53 | |
| E3 | Vom Team nachgetragen: leer, «Beispiel ansehen» mit echter Lücke und Platzhalter | 50b, 54–56 | Lücke «Ab wann kann ich am Anreisetag ins Zimmer?» |
| E4 | Zehn Beispielfragen, zwei ohne Antwort (Check-in, Kinderbett), jede Zahl und jede Lücke geprüft | 50 | |

## F Das weiss der Chat (E09)

| # | Funktion | Beleg |
|---|---|---|
| F1 | Bereiche links, Steckbrief rechts (49 Zeilen, jede wörtlich belegt) | 60, 61 |
| F2 | Suchen, nichts gefunden: selbst eintragen oder Abteilung fragen | 62–65 |
| F3 | Zeile ändern, wie auf der Website, nicht mehr nennen | 66, 67 |
| F4 | Angabe hinzufügen mit «gilt bis», neues Wissen aus Text, Dokument, Foto, Link | 68–73 |
| F5 | Chat prüfen, Zuletzt geändert | 74, 75 |

## G Chat, Server und Daten

| # | Funktion | Beleg | Ruedihus anders |
|---|---|---|---|
| G1 | Chat ausprobieren | 80–82 | |
| G2 | Chat auf der Website: Antwort, Frage in «Das wurde gefragt», Anfrage im Eingang | 91, 92 | Schritt 90 (Feld bricht um) rot: Fund an der Website, nicht am Werkzeug |
| G3 | **KI nur auf ausdrücklichen Schalter**: ohne `RECEPTION_KI=1` Probe-Antworten, Schlüssel nur aus der Umgebung, der Vault wird nie gelesen | K1, K2 | neu (Carlton/Doldenhorn lasen den Schlüssel aus dem Vault beim ersten KI-Aufruf) |
| G4 | Alle Daten herunterladen (ZIP) | R23, O11 | |
| G5 | Sicherheit: Host 421, Herkunft 403, Lesen nur eigene Seite 403, 413, 415, 429 | S1–S6 | |
| G6 | Beschädigte Datei: `.gut`, Rückfall, laute Meldung im Wissen | Code | |
| G7 | Fragen und Anfragen zwölf Monate, E-Mail und Nummern in Fragen abgedeckt | Code | |
| G8 | Online: `online.json`, `api/reception.py`, `api/gast.py`, Mail-Vorlagen unter `api/mails/<nr>/index.html` (F76) | O1–O12 | |

## H Beim Bau gefunden und behoben

| # | Fund | Wo behoben |
|---|---|---|
| H1 | Gelasio trägt die Punkte von Ä/Ö/Ü höher: im einzeiligen Kopf (Zeilenhöhe 1,15, abgeschnitten) stand «Ubersicht» | `ruedihus.css` (Zeilenhöhe 1,4) |
| H2 | Ein neu geschriebener Brief setzte die Fassung auf 0; ein altes Fenster mit Fassung 0 hätte ihn still überschrieben (Lücke in E21) | `_bau/server_teil.py` (Fassung zählt weiter) |
| H3 | Zeilen des Fest-Rechners (`<span>` und `<b>` ohne Trenner) kamen als «… Menu, 20 × CHF 48.00960.00» an | `baustein/anfrage.js` |
