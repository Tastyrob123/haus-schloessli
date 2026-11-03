---
tags: [projekt, website]
status: aktiv
---

# Funktionsliste Die Tafel (La Carte) · Berghotel Gasterntal

Vorlagen: die Tafel des Waldhotel Doldenhorn (`Waldhotel Doldenhorn/_werkzeuge/carte/`, Funktion, Bedienung und Technik, Karten aus dem fertigen Satz C17, Zeilen-Abgleich C18), dahinter La Carte des Carlton-Europe (Sicherheit, Rollen, Prüfseite, Export, Online-Weg) und die lokale La Carte des Grand Beau-Rivage (`website/mission-control/`); Code als Ausgangspunkt aus der Tafel des Landgasthof Ruedihus kopiert (gleiche Technik wie Doldenhorn, dazu C20–C23 und die Namen der Landhaus-Welt). Alle nur gelesen. Katalog: Master «Werkzeug-Bau», Abschnitt 3 (R01–R24) und 4.3 (C01–C23).

Name in der Landhaus-Welt: **Die Tafel** (`_Werkzeuge/stamm/welt.js`, `haeuser/gasterntal/haus.json` welt=land), Knöpfe «Die Stube» (La Maison) und «Der Schreibtisch» (Le Bureau). Dateien und Adressen bleiben `_werkzeuge/carte/`.

**Rahmen aus der Werkzeug-Oberfläche der Häuser** (`_Werkzeuge/stamm/oberflaeche/`, UMSTELLUNG.md: «Die Werkzeuge des Gasterntal … entstehen direkt mit diesem Paket», Rahmen «Die Bühne», Kleid `gasterntal`): Kopf, Rand, Startbild und Leiste kommen aus `oberflaeche.js` (`WO.kopf`, `WO.rand`, `WO.startbild`, `WO.leiste`, `WO.knopf`), der Arbeitsbereich (Liste, Vorschau, Gestalten, Fenster) bleibt der der Tafel, wie es UMSTELLUNG.md für La Carte vorsieht. Eingebunden direkt aus dem Haus (`/assets/oberflaeche/`), das Paket unverändert.

Geprüft mit: «L» = `pruef/lauf.js` (Bedienung im Browser, Wegwerf-Daten; Kennung der Zeile in Klammern) · «O» = `pruef/online_probe.js` (Online-Fassung auf dem Rechner) · «A» = `pruef/anschluss.js` (Anschluss an die Website an einer APFS-Kopie) · «P» = `pruefe.py` (Rundlauf, Wortlaut gegen das Original, Druck gegen die PDF der Website) · «G» = `pruef/gleich.js` (Vorschau = PDF) · «Bild» = `pruef/bilder.js`. Alle Läufe an der Probe-Kopie `~/Desktop/Website-Projekte/_Probe Gasterntal Carte 1710/` (APFS-Klon), Port 8971, ohne KI, ohne Hochladen.

## Die Karte

| Karte | Seiten | Liste «Einfach» | Satz | Original des Hauses | auf der Website |
|---|---|---|---|---|---|
| Karte 2026 · Ässe u trinke | 2 (A4) | 109 Zeilen: Seite 1 Getränke und Deckel (43 Getränke, 8 Rubriken, 6 Zwischentitel, 9 Texte des Deckels), Seite 2 Speisen und Jugendschutz (28 Gerichte, 9 Rubriken, 1 Titel, 1 Zwischentitel, 4 Texte) | `_werkbank/satz/u-karte-2026.html` | `_quelle/website/pdf/Neue_Karte_Gasterntal_2026.pdf` | essen.html (ganze Karte als Zettel-Tisch, Knopf «Karte als PDF» → `assets/pdf/Karte-2026.pdf`), picknick.html (Rubrik «Öpis chalts», Bildzeile Zvieri Plättli), index.html (Auszug «Grossis Küche», «Gäng guet», Bildzeilen Chäsefondue und Zvieri Plättli), Laufband mit Namen von Rubriken |

**Weitere Preislisten belegt das Haus nicht:** «Öpis chalts» (Picknick) ist eine Rubrik der Karte 2026 und wird dort gepflegt. Die Sauna hat keine Preisliste: CHF 60.00 und CHF 50.00 stehen als Text auf sauna.html (daten.py `SAUNA`, `SAUNA_PREIS`) und gehören Der Schreibtisch («Zeiten & Preise»). Der Wildabend (CHF 67.00) ist ein Anlass des Schreibtischs, keine Karte.

**Wortlaut:** Die Website trägt den Wortlaut des Hauses (daten.py, mit seinen Tippfehlern wie «Tagesssuppe», «Aperitiv»), der Druck die berichtigte Fassung (`_werkbank/satz_daten.py BERICHTIGT`). Die Tafel hält diese Trennung: eine Zeile der Website bleibt Wort für Wort, bis das Haus ihren Eintrag ändert, dann geht genau das geänderte Stück mit (A: Preis der Tagessuppe geändert, die Zeile heisst weiter «Tagesssuppe»).

## A · Rahmen jeder Oberfläche (R01–R24)

| Nr | Vorlage | Gasterntal | geprüft |
|---|---|---|---|
| R01 | Kopfleiste, Rand, Hauptfläche, Leiste, Fenster, Quittung (`aria-live`) | gleich, Rahmen der Oberfläche «Die Bühne» (`wo-kopf`, `wo-rand`, `wo-raum`, `wo-leiste`), `data-wo-haus="gasterntal"` | ✓ L (R01) |
| R02 | Auftakt: ruhig bis Daten, Schriften, Foto da (höchstens 2,5 s) | gleich (`auftakt.js`) | ✓ L (A01) |
| R03 | Fehlermelder als erstes Skript, an `api/fehler`, höchstens 20, Netzfehler nie | gleich (`fehlermelder.js` in Werkzeug, Blatt, Anleitung, Prüfseite) | ✓ L (R03) |
| R04 | Startfehler-Tür mit «Prüfung öffnen» | «Die Tafel startet nicht.» in Schiefer und Balkonholz | ✓ L (R04) |
| R05 | Kopf: Zeichen, Name, Unterzeile, Titel, Stand; runde Knöpfe La Maison, Prüfung, Anleitung; «Website ansehen» | `WO.kopf`: Raute der Laube, «Die Tafel · Karte · Berghotel Gasterntal», Titel «Karte 2026» und Stand («PDF vom …», «Entwurf wartet», «Nicht gespeichert»); runde Knöpfe Die Stube, Prüfung, Anleitung, dazu Protokoll, Zustand, wer arbeitet; «Website ansehen» → essen.html#karte. Der Schreibtisch steht im Rand unter «Wege» (Platz im Kopf) | ✓ L (R05) |
| R06 | Rand: Karten, Gruppen, Wege je in neuem Fenster | `WO.rand`: «Ihre Karte» (Kachel mit Foto), «Bearbeiten» (Einfach / Fortgeschritten mit Satz), «Wege», unten Website, Anleitung, Prüfung | ✓ L (C01, C13) |
| R07 | Handy: Rand als Knopf, schliesst nach der Wahl, kein Verrutschen | «Bereiche» im Kopf (Oberfläche), schliesst nach der Wahl; 390 px ohne seitliches Verrutschen | ✓ L 390 (R07) |
| R08 | Leiste: Text links, Vorher/nachher, Speichern, Veröffentlichen | `WO.leiste`: «Alles ist veröffentlicht» / «Entwurf: n Änderungen warten» / «Nicht gespeicherte Änderungen», Marke «Entwurf»; Verwerfen, Vorher/nachher, Probe-PDF, Speichern, Veröffentlichen | ✓ L (R08) |
| R09 | Speichern grau/gelb/grün 2,6 s, ⌘S | `wo-kn--glas` / `--wartet` / `--fertig`, ⌘S auch aus der Vorschau | ✓ L (R09) |
| R10 | Nichts speichert still; «Nichts geändert, nichts gespeichert.»; abgewiesene Eingabe bleibt gelb | gleich | ✓ L (R10, A08) |
| R11 | Quittung mit Rückgängig und Vorher/nachher, Fehler mit Stichwort und «Was tun?» | gleich, in Schiefer mit Holzkante | ✓ L (R11) |
| R12 | Veröffentlichen nur mit Entwurf, Fenster mit Änderungen, Fortschritt in Schritten | gleich | ✓ L (R12) |
| R13 | Verlassen mit offenen Eingaben: Browser fragt | gleich | ✓ L (R13) |
| R14 | Frühere Fassungen, «Ursprünglicher Stand», in den Entwurf | gleich | ✓ L (C12) |
| R15 | Letzte Ansicht gemerkt, aus La Maison die Übersicht | Modus gemerkt; aus der Stube (:8918/_werkzeuge/maison/) die Karte | ✓ L (R15, C01) |
| R16 | Bühne mit Hausfoto, Zierzeile, Titel | `WO.startbild` Art «buehne»: Foto der Gaststube (`stube-l.webp`), Zierzeile mit der Raute, «Karte 2026 Ässe u trinke», Satz, Knopf, Angaben (Seiten, Format, PDF vom) | ✓ L (R16) |
| R17 | Schweben beim Wechsel, «Weniger Bewegung» | Startbild mit eigenem Auftritt (nur `transform`), Kopf der Vorschau schwebt (`schweben.js`); «Weniger Bewegung» steht alles | Code, Bild |
| R18 | Rundgang (vier Schritte), `?rundgang` | Texte des Hauses («Die Karte, wie sie auf dem Tisch liegt»), auch im Rand «Kurzer Rundgang» | ✓ L (R18) |
| R19 | «Zur Werkbank» nur aus der Werkbank | gleich (`zur-werkbank.js`, Schlüssel `bg-wb` wie Die Stube) | ✓ L (R19) |
| R20 | Beispiele statt Leere | keine leere Liste: die Karte ist voll eingelesen | – |
| R21 | Kopf dunkel, Raum hell, Auswahl im Hausstil | Kopf in Schiefer mit Lauben-Raute, Raum hell (Papier, Raute 3 %), Rand weiss, Kacheln im Hausstil | ✓ Bild |
| R22 | Kein Passwort bis zur Auslieferung | gleich (Rollen ohne Anmeldung) | – |
| R23 | Eigene Prüfseite mit Lexikon und Reparaturen | gleich (`pruefung.html`, Lexikon `anleitung.html#was-tun`) | ✓ L (C14) |
| R24 | Deutsch | gleich | – |

## B · Laden, Karte, Wege (C01, C13)

| Vorlagen | Gasterntal | geprüft |
|---|---|---|
| Kacheln je Karte mit Foto, Gruppe, Seitenzahl, Marke «Entwurf» | eine Karte (Karte 2026), Kachel mit Foto der Gaststube, Marke «Entwurf» im Rot der Fensterläden | ✓ L (C01) |
| Wechsel mit offenen Eingaben fragt «Verwerfen und wechseln» | gleich (bei einer Karte nur beim Moduswechsel) | Code |
| Einfach / Fortgeschritten mit Satz, gemerkt | gleich, als Segment-Wahl der Oberfläche | ✓ L (C01) |
| Wege: Frühere Fassungen, Veröffentlichte PDF, Unterlagen, Zur Werkbank, Seite der Website, Anschluss | gleich, dazu Der Schreibtisch und Kurzer Rundgang | ✓ L (C13) |

## C · Einfach (C02, C03, C04)

| Vorlagen | Gasterntal | geprüft |
|---|---|---|
| Liste je Seite: Rubrik, Zwischentitel, Titel, Text, Eintrag mit Preis | Einträge sind Getränke (`re`) und Gerichte (`po`), Zwischentitel Weisse, Rote, Rosé und «Zum Schutz unserer Jugend», Texte des Deckels und des Kastens | ✓ L (C02) |
| Marken Neu, Geändert, Verschoben, Ausgeblendet | gleich | ✓ L (C02, C09) |
| Zeilenknöpfe Bearbeiten, Kopieren, Hoch, Runter, Auge, Papierkorb; «Eintrag hinzufügen» an der Rubrik | gleich | ✓ L (C02) |
| «Eintrag am Ende», «Neue Rubrik», «Neuer Eintrag» mit Wahl der Rubrik | gleich (17 Rubriken zur Wahl) | ✓ L (C02) |
| Doppelklick öffnet das Fenster | gleich | ✓ L (C02) |
| Fenster je Eintrag mit seinen Feldern, Vorschau «So steht es auf der Karte» | Felder mit den Namen des Gasterntal-Satzes: Gericht = Name, Zusatz, Beschreibung (deutsche Zeile), Übersetzung (englische Zeile), Angabe (Portion, Chlini Portion, pro Person, Kinder) und Preis; Getränk = Name, Zusatz (mit und ohne, A. Mathier, 17 %), Angabe (33cl, Cüpli, Flasche) und Preise; Rubrik = Rubrik, Zusatz, Spaltenkopf (3dl, 5dl, 1,5 Liter). Ein Feld leer = die Zeile fällt weg | ✓ L (C02) |
| Zeichen am Gericht | betrifft nicht: die Karte des Gasterntal hat keine Bildzeichen | – |
| Name Pflicht | gleich | ✓ L (C02) |
| Preis in der Schreibweise der Karte («12,5» → «12.50») | gleich | ✓ L (C03) |
| Rubrik verschieben als Block, Rubrik entfernen nennt die Zahl der Einträge | gleich («Gäng guet» mit dem Chäsefondue vor «Grossis Küche» und zurück) | ✓ L (C02) |
| Seite ausblenden, verschieben | gleich | ✓ L (C02) |
| Klick links ↔ rechts auf derselben Höhe, Blinken; Doppelklick in der Vorschau öffnet | gleich | ✓ L (C04) |

## D · Fortgeschritten (C05, C06)

| Vorlagen | Gasterntal | geprüft |
|---|---|---|
| Klick wählt, Rahmen mit Griffen, Seitenleiste «Gestalten» | gleich | ✓ L (C05) |
| Ziehen mit Mass, Einrasten, Alt ohne | gleich | ✓ L (C05) |
| Ecken 40–300 %, Linien mit Endgriffen, Pfeile 0,5/5 mm, Entf, Esc | gleich | ✓ L (C05) |
| ⌘Z / ⌘⇧Z / ⌘Y | gleich | ✓ L (C05) |
| Doppelklick schreibt, Enter beendet | gleich, jeder Text der Karte | ✓ L (C05) |
| Gestalten: Schrift, pt, Textart, Farbe, Ausrichtung, Zeilenabstand, Abstand davor/danach; zweiter Klick schaltet ab; «Teil zurücksetzen», «Anordnung zurücksetzen» | Schriften des Hauses (Barlow Semi, Instrument Sans, DM Mono), elf Farben des Hauses aus `assets/css/main.css` (Tinte, Talwand im Regen, Talwand, Nacht, Tannen am Hang, Balkonholz, Kander, Papier, Blatt, Fensterläden, Weiss) | ✓ L (C05), G |
| Kopfleiste und Fusszeile als eigene Elemente | Band über den Speisen (`header.uband`), Deckel | ✓ G |
| Daten der Karte als Text, Ungültiges abgewiesen | gleich; der Server weist fremde Tags, Merkmale, feste Teile und eine falsche Art der Karte ab | ✓ L (C06, S01) |

## E · Vorschau (C07)

| Vorlagen | Gasterntal | geprüft |
|---|---|---|
| Vorschau wie die PDF (derselbe Satz), «n Seiten», «Seite x von y» | gleich | ✓ L (C07), G, P |
| Zoom ±0,1, je Modus gemerkt, per transform | gleich (in der Ansicht Website ausgeblendet) | ✓ L (C07) |
| Karte / Website | drei Seiten zur Wahl: «Ässe u trinke», «Picknick», «Startseite»; mit Patch im Bau mit dem Entwurf, sonst wie heute, die Karte blinkt | ✓ L (C07), A |

## F · Mittagsmenü (C08): betrifft nicht

Das Gasterntal hat kein Mittagsmenü der Woche. Belege: die Seite «Restaurant» des Hauses (`_quelle/website/text/pages__restaurant.md`) nennt nur die «Speisekarte» und den Wildabend; das Willkommensschreiben (`_quelle/website/pdf/Willkommensschreiben.pdf`) sagt «RESTAURANT · Warme Speisen bis 2030h»; daten.py kennt kein Mittagsmenü. Keine Karte «mittag»; der Teil MITTAG in `satz.js` und die Mittag-Wege in `carte.js` stammen aus der Vorlage und werden nicht benutzt.

| Prüfung | geprüft |
|---|---|
| Keine Karte «mittag», `api/karte?z=mittag` 404 | ✓ L (C08) |

## G · Speichern bis Zurückholen (C09–C12)

| Vorlagen | Gasterntal | geprüft |
|---|---|---|
| Entwurf, neu laden, noch da; Vorher/nachher; Verwerfen in den Verlauf | gleich | ✓ L (C09) |
| Probe-PDF | gleich | ✓ L (C10) |
| Veröffentlichen: drucken, Wort für Wort gegen die Daten, dann umschalten; vorige Fassung in den Verlauf | gleich | ✓ L (C11) |
| Restaurant-Seiten setzen | **mit Anschluss:** PDF nach `unterlagen/pdf/karte-2026.pdf` und an die Adresse der Website (`assets/pdf/Karte-2026.pdf` oder was Der Schreibtisch unter `link.pdf` führt), Zeilen neu; der Bau des Hauses setzt die Seiten zweimal und übernimmt genau die Seiten, die sich ändern (essen.html, index.html, picknick.html), nur wenn die Seite heute dem Bau gleicht, sonst nur ihren Abschnitt id="karte" und eine Meldung; vorige Seiten und PDFs gesichert, Nachprüfung Byte für Byte | ✓ A |
| Frühere Fassungen, Ursprünglicher Stand | gleich | ✓ L (C12), A |

## H · Prüfseite, Export, Online (C14–C16)

| Vorlagen | Gasterntal | geprüft |
|---|---|---|
| Prüfseite (Browser, Server, Karten, Druck, Sicherungen, Fehler, Reparaturen nur Direktion mit zwei Klicks) | gleich | ✓ L (C14) |
| Alle Daten herunterladen (`api/export`) | gleich | ✓ L (C15) |
| Online ohne Werkbank-Kette (`online/carte.py`, `online/carte_druck.js`, `online.json`) | gleich; Satz, Schriften und Kachel im Werkzeug, die Oberfläche aus `assets/oberflaeche` des Hauses | ✓ O |

## J · Aus Doldenhorn und Ruedihus (C17–C23)

| Nr | Vorlage | Gasterntal | geprüft |
|---|---|---|---|
| C17 | Karten aus dem fertigen Satz | gleich: Rundlauf Zeichen für Zeichen, Druck = PDF der Website (Text, Seitenzahl, Seitenbilder), Wortlaut = Original nach den Regeln von BERICHTIGT, 103 Preise im Druck = 103 im Original | ✓ P |
| C18 | Anschluss mit Zeilen-Abgleich | Abgleich in der Reihenfolge der Karte, jede Zuordnung an den Preisen geprüft (71 Zeilen, 17 Rubriken); Zwischentitel nach Wortlaut («Rosé» unter «Weine offen» steht nur in der Karte und bleibt der Website fern); geändert wird nur das Stück, das sich ändert (Name, Zusatz, Beschreibung, Übersetzung, Preise); Kennungen der Rubriken bleiben (die Startseite und das Picknick suchen ihre Rubriken danach). Zeilen aus dem Grundstand = `inhalt.KARTE_STANDARD` | ✓ A |
| C19 | Rolle Spa | betrifft nicht (keine Spa-Karte); Rolle «spa» bekommt 403 ROLLE | ✓ L (S01) |
| C20 | PDF an alle Adressen der Website | gleich (zwei Adressen); Sicherung der vorigen PDFs mit Ordner im Namen, weil `karte-2026.pdf` und `Karte-2026.pdf` auf dem Mac derselbe Name sind | ✓ A |
| C21 | Seiten über zwei Bauten übernehmen | gleich; weicht eine Seite ab, bekommt jede Seite mit Abschnitt id="karte" (essen, picknick, index) nur diesen Abschnitt | ✓ A |
| C22 | Zeilen-Abgleich mit Teilpreisen und Gruppen | im Gasterntal ein Eintrag je Zeile; Getränke mit Angabe und Preis («Cüpli 10.00 · Flasche 54.00») folgen Stück für Stück | ✓ A |
| C23 | Leere Zeile fällt weg | gleich (leere englische Zeile eines neuen Gerichts) | ✓ L (C02) |

## I · Rollen und Sicherheit (Master 5.2)

| Carlton / Doldenhorn / Ruedihus | Gasterntal | geprüft |
|---|---|---|
| Küche, Service, Direktion | Küche und Service ändern die Karte und drucken Proben, veröffentlichen darf die Direktion (eine Karte, kein Tagesteller, kein Mittagsmenü) | ✓ L (S01) |
| Herkunft 403, Host 421, nur JSON 415, 3 MB 413, Grenzen 429 nur auf `/api/`-Wegen, gesperrte Pfade, CSP | gleich | ✓ L (S02) |
| Jede Eingabe geprüft | gleich (Bausteine nur aus dem Grundstand, Art passt zur Karte) | ✓ L (C06, S01, S02) |
| Tägliche Sicherung 14 Tage, Konflikt 409 zweier Fenster | gleich | ✓ L (A08), O |
