---
tags: [projekt, website]
status: aktiv
---

# Das Kartenpult (La Carte) · Wirtschaft am Schlössli Bottighofen · Station 11, Teil `karten`

Stand 20.10.2026, Werkzeug-Anpasser (Bau). Prüfung durch einen anderen Chat steht aus (Station 12). Nichts hochgeladen, nichts verschickt, keine KI-Aufrufe, keine bezahlten Werkzeuge.

## Adresse

- **Werkzeug:** http://127.0.0.1:9031/_werkzeuge/carte/ (eigener Server der Tafel: `python3 _werkzeuge/carte/serve.py 9031` im Projektordner, launch.json «tafel-schloessli»; hört nur auf 127.0.0.1)
- **Prüfseite:** http://127.0.0.1:9031/_werkzeuge/carte/pruefung.html · **Anleitung:** http://127.0.0.1:9031/_werkzeuge/carte/anleitung.html
- **Lunch-Menü direkt:** http://127.0.0.1:9031/_werkzeuge/carte/#mittag
- **Stand-Weg für Die Stube (La Maison):** `GET http://127.0.0.1:9031/_werkzeuge/carte/api/status` → `{karten:[{ziel, name, unter, gruppe, entwurf, entwurf_zeit, pdf_zeit, stand_zeit, seiten, verlauf}], bau, einstellungen, rollen, rechte}`
- Name **Das Kartenpult** (Robert 19.10.2026 «passt»: Hafenbüro, Schaufenster, Kartenpult, Reservationsbuch, Bildarchiv, Besucherliste, Hausdruckerei). Die Namen stehen an **einer** Stelle: `_werkzeuge/oberflaeche/kleid/schloessli.js` (`WO_HAUS.namen`), `oberflaeche.js name()` liest sie zuerst; das Kartenpult nimmt sie über `WO.name()`, Anleitung und Prüfseite über `namen.js`. Dateien und Wege bleiben `_werkzeuge/carte/`. Dieselben zwei Dateien liegen auch in `website/assets/oberflaeche/` (dort hatte jemand den Rahmen schon hingelegt, nachgezogen 20.10.2026, Sicherung `*.vor-namen-2026-10-20`).

## Was das Werkzeug pflegt (Satz der Werkbank, nichts abgetippt)

| Karte (Kennung) | Seiten | Satz | PDF der Website | Wer veröffentlicht |
|---|---|---|---|---|
| Die Karte nach Ländern (`speisekarte`) | 2 | `website/_werkbank/satz/u-speisekarte.html` | `website/unterlagen/pdf/speisekarte.pdf` | Direktion |
| Lunch-Menü der Woche (`mittag`, C08) | 1, A4 quer | Woche, gesetzt wie `u-lunch.html` | `lunch.pdf` (mit Anschluss dazu `mittag.pdf`) | **Küche** und Direktion |
| Lästermeile (`laestermeile`) | 1 | `u-laestermeile.html` | `laestermeile.pdf` | Direktion |
| Weinkarte (`weinkarte`) | 23 | `u-weinkarte.html` | `weinkarte.pdf` | Direktion |
| Bankettmenüvorschläge (`bankett`) | 2 | `u-bankett.html` | `bankett.pdf` | Direktion |

Kette: Original-PDF → Station 10 (`_karten/stand/*.json`, Abgleich 0 Abweichungen) → Werkbank-Kit (`website/_werkbank/satz_daten.py`, Berichtigungen gezählt in `website/_werkbank/berichtigt.json`) → `einlesen.py` liest den Satz als Baum ein (C17) → Vorschau, Probe-PDF und veröffentlichte PDF kommen aus demselben `satz/satz.js`. Der 4-Hands-Lunch hat keinen Satz und keine PDF (Station 10: nur in den Daten) und ist nicht im Werkzeug.

**Belege (20.10.2026, Satz der Werkbank von 00:04):**
- Rundlauf Daten → Satz Zeichen für Zeichen gleich: 4 von 4 Satz-Karten, dazu das Blatt der Lunch-Woche gleich `u-lunch.html` (`node pruef/rund.js`).
- Druck des Kartenpults gegen die PDFs der Website: 4 von 4 gleicher Text (`pdftotext -layout`), gleiche Seitenzahl, gleiche Seitenbilder (`python3 pruefe.py website`). Damit ist La Carte die eine Quelle der Karten-PDFs (Roberts Standard 17.10.2026).
- Wortlaut gegen die Originale des Hauses: 4 von 4 «gleich bis auf Trennung» nach der Regel von `_Werkbank-Kit/satz_pruefe.py`, bewusste Abweichungen aus `website/_werkbank/unterlagen.json` (`python3 pruefe.py wortlaut`).

## Was neu gebaut wurde (und warum die Vorlage es nicht konnte)

Vorlage: die Tafel des Berghotel Gasterntal (`_werkzeuge/carte/`, neueste Fassung mit dem Rahmen «Die Bühne»), dort aus Ruedihus, Doldenhorn, Carlton und Rivage. Stamm-Werkzeug `_Werkzeuge/werkzeuge/karten/` nicht benutzt: es hat kein Mittagsmenü, keine Prüfseite, keinen Export und nicht den gemeinsamen Rahmen der sechs Werkzeuge (Master 3, UMSTELLUNG.md).

1. **Satz der Werkbank lesen (C25):** Die Werkbank setzt Namen in Kapitälchen (erster Buchstabe als Text, Rest in `span.kl`) und die Allergene als kleine hochgestellte Marke mit Blatt-Zeichen für VEG/OVEG. Das Kartenpult bearbeitet beides als **ein** Feld («Name», «Allergene» mit «/» wie auf der Karte des Hauses) und setzt es beim Speichern genau so zurück wie `satz_daten.py` (`_kk`, `kuerzel`), Trennzeichen und Blatt aus dem Satz selbst. Geschützte Leerzeichen vor «–» bleiben. Eine Rubrik als Block verschiebt ihren ganzen Abschnitt (`section.sb-r`). Die Vorlage (Gasterntal) kannte nur die Bausteine `po`/`re`/`rubrik`.
2. **Lunch-Menü der Woche (C08) in der Form des Hauses:** Das Haus hat kein Tagesmenü (Salat, Vegi, Fleisch, Fisch je Tag), sondern ein Lunch-Menü mit drei Gängen, das wechselt. `satz/satz.js` Teil MITTAG, `carte.js wocheHTML()`, `carte.py` (GAENGE_FELDER, Prüfung genau ein Menü je Woche): je Woche Vorspeise, Hauptgang, Dessert mit Zeile darunter, Titel, Gruss, Preis; Pfeile statt Kalender; «Nächste Woche anlegen»; «Diese Woche kein Lunch-Menü»; dasselbe Blatt wie der Satz der Werkbank (`u-lunch.html`: Gruss links, Menü mittig mit Zeichen, Blatt-Ornament zwischen den Gängen, Preis als Marke «3 Gänge — 35.- Chf», Wortlaut des Hauses im Feld). Die Küche veröffentlicht es selbst (`KUECHE_LIVE`).
3. **Website-Pfad:** Im Schlössli liegt die Website in `website/` neben `_werkzeuge/` (bei den Kandertal-Häusern ist das Projekt selbst die Website). Server, Satz, Einlesen und Prüfung finden die Website über `PROJ` (beide Lagen); zieht das Werkzeug in Station 14 nach `website/_werkzeuge/`, geht es ohne Änderung.
4. **Gemeinsamer Rahmen und Namen:** `_werkzeuge/oberflaeche/` (Paket aus `_Werkzeuge/stamm/oberflaeche/` + `kleid/schloessli.js/.css`) für alle sechs Werkzeuge des Hauses; der Server liefert ihn unter `/assets/oberflaeche/`, bis Station 14 ihn nach `website/assets/oberflaeche/` legt. Kleid: Farben der Website (Ton in Ton), Open Sans in Versalien wie die Wortmarke, Zeiger als Zeichen, die Horizontlinie unter dem Titel der Bühne (zieht sich beim Öffnen auf), Naben statt Rauten, keine Einkerbungen.
5. **Bilder in allen Listen (Robert 19.10.2026 «in allen Tools Bilder dazu», Fehlerbuch 10a):** umgebaut sind (a) die Liste der Einträge (Bild 64 px je Zeile: eigenes Gericht wie THON, TORTELLONI, sonst das Foto, das die Website der Rubrik gibt, `bau.py kw_bild`, sonst das der Karte; Weine mit der Flasche aus dem Weinberater, 172 von 468, Rechte dort offen), (b) die Rubrik-Wahl bei «Neuer Eintrag» (Foto der Rubrik), (c) «Vorher und nachher» (Bild je Stelle), (d) «Frühere Fassungen» (Foto der Karte je Fassung); (e) die Karten im Rand hatten schon Fotos. Alle Bilder aus `website/assets/img` als 112-px-Vorschauen (`bilder/z/`), geladen, wenn die Zeile ins Bild kommt. Doppelte Einträge: keine (geprüft in allen vier Satz-Karten, Name + alle Felder + Weingut).
6. **Anschluss an die Website: noch nicht.** `web.py` ist ein Platzhalter (Bauplan als `web.py.vorlage-gasterntal`). Die Seiten der Website zeigen die Karten aus `website/inhalt/*.json`; die fasst nur Station 14 an. Mit eingeschaltetem Anschluss legt «Veröffentlichen» die geprüfte PDF nach `website/unterlagen/pdf/<karte>.pdf` (Lunch: `lunch.pdf` und `mittag.pdf`), vorige gesichert.

7. **Robert 20.10.2026 (Beanstandung 01:00 und 01:18, Fehlerbuch 10a):** keine Abfrage «Wer arbeitet hier?» mehr, das Protokoll schreibt fest «Team Schlössli» mit vollen Rechten (das Reservationsbuch hatte dieselbe Abfrage, dessen Chat ist benachrichtigt); Plus-Knöpfe («Eintrag hinzufügen», «Eintrag am Ende», «Neue Rubrik», «Nächste Woche anlegen») als Knöpfe des Rahmens mit Tiefe und rundem Knauf; die Knöpfe einer gewählten Zeile stehen als eigene Zeile darunter, nie über Bild oder Text, ohne Fläche und Schatten hinter den Kreisen; Fortgeschritten: «Gestalten» rollt in sich, nichts abgeschnitten, die untere Leiste zeigt dann nur Zeichen; untere Leiste neu: derselbe Zustand wie der Kopf (eine Quelle, auch beim Lunch), kurzer ganzer Satz, nur Knöpfe, die gerade etwas tun, Speichern mit Haken; im Modus Fortgeschritten schliesst das Fenster (Karte und Website) unten bündig mit der linken Kachel ab. Um 01:24 dazu: ein Name oder eine Rubrik in Kapitälchen ist auch in der Karte (Fortgeschritten) ein Text, gewählt, in «Gestalten» benannt und geschrieben als ganzer Wortlaut und gesetzt wie die Werkbank (Probe `pruef/kapitaelchen.js`, Chromium und WebKit, 1000 und 1440); der Titel der Leiste überdeckt nie einen Knopf (Knöpfe dann nur mit Zeichen), «Veröffentlichen» steht erst nach dem Speichern da, nie blass.

## Selbst geprüft (bedient, nicht nur geladen)

Bedienungsprobe `node pruef/lauf.js <browser> <breite> <höhe>` (eigener Prüfserver :9033, Wegwerf-Daten, unsichtbar), drückt jede Zeile der Funktionsliste, dazu Lunch-Menü, Rollen, Sicherheit, zwei Fenster, Netz weg, ungewöhnliche Eingaben:

| (20.10.2026, nach Roberts Beanstandung) | 1440 × 900 | 390 × 844 |
|---|---|---|
| Chromium | 153 von 153 | 151 von 151 |
| Safari-Kern (WebKit) | 153 von 153 | 151 von 151 |
| Firefox (Stand vor der Beanstandung) | 149 von 149 | nicht gelaufen |

Je Lauf: jede Seite zweimal geladen, R01–R19, C01–C15 bedient (u. a. Eintrag ändern, Preis in der Schreibweise der Karte, neuer Eintrag, kopieren, ausblenden, entfernen, verschieben, Rubrik als Block, Seite ausblenden und verschieben, Vorher/nachher, Probe-PDF, Veröffentlichen mit PDF = Daten, Frühere Fassungen, Verwerfen, Fortgeschritten: wählen, ziehen, ⌘Z, Pfeile, Gestalten, direkt schreiben, Daten als Text), C08 Lunch-Menü (Felder wörtlich aus Station 10, Blatt A4 quer, mittig, Eintrag geht sofort in die Karte, Woche vor, «Nächste Woche anlegen», Woche ohne Menü, Küche veröffentlicht, PDF = Woche), Rollen und Sicherheit (403/413/415/421/429-Wege, Programmcode, fremdes HTML), Prüfseite, Export aller Daten, Fehlermelder, Startfehler-Tür, Rundgang, «Zur Werkbank», zwei Fenster (Konflikt), Netz weg, 5'000 Zeichen, Emoji und Umlaute, Verlassen mit ungespeicherten Eingaben; keine Skriptfehler, keine toten Adressen, kein seitliches Verrutschen. Belege: `_werkzeuge/carte/pruef/aus/lauf-<browser>-<breite>/` (ergebnis.json, PDFs, Prüfbilder). Wegwerf-Daten, die echten Daten der Tafel bleiben unberührt.

Beim Bauen gefunden und behoben (Firefox meldete einmal einen abgebrochenen Schrift-Download beim Neuaufbau des Rahmens, im zweiten Lauf nicht mehr): (1) Unter Rechnerlast blieb die Vorschau grau, weil der Rahmen sein «bereit» schickte, bevor das Werkzeug zuhörte; jetzt Handschlag (`carte.js halloVorschau`, `blatt.js` «hallo»). Gilt auch für die Tafeln der anderen Häuser (Master Abschnitt 9). (2) Der Server lieferte keine `.woff`-Schriften der Website (Ansicht «Website» in Firefox). (3) Anleitung und Prüfseite luden Dateien der Gasterntal-Werkbank.

Flüssigkeit (`node pruef/fluessig.js chromium`, Rechnerlast 5,5 bis 7, 20.10.2026): ungebremst steht jede Karte nach 0,1 bis 0,9 s; gedrosselt (Prozessor 4× und 6×, Slow 4G) Speisekarte 4,5 s, Lunch 3,8 s, Weinkarte 4,7 s / 5,9 s (Grenze 6 s); Tippen → Vorschau 43 bis 71 ms; Scrollen von Liste und Vorschau 120 Bilder/s, schlechtestes Bild 9 ms; lange Aufgaben 0 bis 2 (längste 74 ms). Dafür beim Bauen: Kartendaten gepackt (140 → 39 kB), Zeilenbilder als 112-px-Vorschauen (`bilder/z/`, je rund 4 kB) und erst geladen, wenn die Zeile ins Bild kommt. Erste Seite der Speisekarte: 1019 → 608 kB.

## Übernommen aus den anderen Häusern (Auftrag Oberchef 20.10.2026, je am Stand geprüft)

| Korrektur / Standard | Herkunft | Am Kartenpult geprüft |
|---|---|---|
| La Carte ist die eine Quelle der Karten-PDFs | Robert 17.10.2026 (Werkzeug-Master vor 4) | Druck = PDF der Website, 4 von 4 Seite für Seite (`pruefe.py website`) |
| Mittagsmenü immer, wenn das Haus eins hat; schön und mittig | Robert 17./18.10.2026 (C08) | Lunch-Menü der Woche, Blatt gleich `u-lunch.html`, Bedienungsprobe «mittig ± 3 %» |
| Bilder in jeder Liste | Fehlerbuch 10a (Schaufenster, 19.10.2026) | jede Zeile mit Foto des Hauses oder Flasche, Prüfbild `bilder/la-carte-liste-1440.webp` |
| Namen der Werkzeuge an einer Stelle | Chef-Chat 19.10.2026, Robert «passt» | `WO_HAUS.namen`, Kopf «Das Kartenpult», Wege «Das Schaufenster» (Bedienungsprobe R05, C13) |
| Startfehler-Tür, Fehlermelder, Prüfseite, Export | R03, R04, C14, C15 (Rivage 17.10., Carlton 16.10.) | Bedienungsprobe R03, R04, C14, C15 grün |
| Sicherheit: Host, Herkunft, Grösse, Grenze, Rollen | 5.2 (Carlton) | Bedienungsprobe S01, S02 grün |
| Veröffentlichen online in der Demo aus | Robert 17.10.2026 «in allen» | betrifft lokal nicht; Online-Fassung nicht gebaut (offen) |
| Auswahl, Kalender, Schalter im Hausstil, keine Systemauswahl | feedback-werkzeuge-regeln | Bedienungsprobe C08 «kein Kalender», Pfeile; Schalter der Vorlage |
| Hell mit Bühne, Auftritt der abgenommenen Häuser (40 px, Zoom) | feedback-werkzeuge-hell-buehne, Fehlerbuch 10a (Hafenbüro) | Kleid `schloessli.css` (Auftritt 40 px / 1,06, Horizontlinie) |
| Vor der Fertig-Meldung nach `{`, `undefined`, `NaN`, `None` suchen | Fehlerbuch 10a (Anlässe) | keine Fundstelle in Werkzeug, Anleitung, Prüfseite (Bedienungsprobe A99 und Durchsicht) |
| Keine Einkerbungen | Robert 18.10.2026 | keine im Kleid und in der Tafel |
| Vorschau bleibt grau unter Last (Handschlag) | eigener Fund 19.10. (Master 9) | Bilder für Hafenbüro und Werkbank entstehen auch unter Last |

## Prüfpunkte (Master 7a, `_Werkzeuge/STAND.md`)

| Prüfpunkt | Stand | Beleg oder was fehlt |
|---|---|---|
| Backend | **offen** | Läuft nur auf diesem Rechner (`serve.py`, 9031). Für die PDF braucht der Server node, Playwright mit Chromium und poppler. Online-Fassung (`online.json`, `online/`) aus der Vorlage übernommen, Namen angepasst, nicht gebaut und nicht hochgeladen. |
| Datenbank | **offen**, Teil erfüllt | Dateien in `_daten/` über `carte.py` (`_schreib` mit Sicherung `.vorher`, beschädigte Datei nie still leer). Zwei Schreiber: Konflikt statt Überschreiben (Bedienungsprobe A08 «Zwei Fenster»). Keine Obergrenze für Verlauf und PDF. |
| Authentication und Rollen | **offen** | Kein Passwort (Robert 15.10.2026). Rollen Küche, Service, Direktion mit Rechten je Weg (403), geprüft S01. `wer` ist eingetippt, nicht geprüft. |
| Rechteverwaltung | **offen** | Das Haus kann keine Zugänge anlegen oder sperren. |
| API-Sicherheit | **offen**, Teil erfüllt | Host 421, fremde Herkunft 403, nur JSON 415, über 3 MB 413, Programmcode 400, fremdes HTML 400, gesperrte Pfade 404, CSP (Bedienungsprobe S02). Nach aussen nicht gebaut. |
| Rate Limits | **erfüllt** (lokal) | 900 Anfragen / 60 Änderungen / 8 Drucke je Absender und Minute (`serve.py GRENZEN`), nur auf den Wegen des Werkzeugs. |
| Logging | **erfüllt** (lokal) | `_daten/protokoll.jsonl` (wer, Rolle, was, Karte), `_daten/fehler.log`, Browserfehler über den Fehlermelder (R03). |
| Backups | **offen**, Teil erfüllt | Verlauf jeder Veröffentlichung, «Ursprünglicher Stand», tägliche Sicherung `_daten/sicherung/` (14 Tage). Keine Kopie ausserhalb des Rechners. |
| Deployment | **offen** | Nichts online. Git nur über den Hausordner (auto-sync des Vaults betrifft ihn nicht). |
| CMS-Datenmodell | **erfüllt** | Fünf Karten mit verschiedenen Formen (A4 hoch/quer, Kapitälchen, Kürzel-Marken, Weingüter, Jahrgänge, Flaggen, zweiter Preis mit Angabe, Woche) laufen ohne Hauswerte im Bedien-Code; Hauswerte stehen in `einlesen.py KARTEN`, `carte.py ZIELE/WEBSITE_PDF`, `carte.js FOTO/SEITE_DER_KARTE/FOTO_RUBRIK`, Namen in `kleid/schloessli.js`. |
| Übersetzungsworkflow | **betrifft dieses Werkzeug vorerst nicht** | Die Karten des Hauses sind nur deutsch (Station 10: keine Sprache, die das Original nicht hat). Übersetzung ist Station 15a. |
| KI-Kosten | **betrifft dieses Werkzeug nicht** | Keine KI. |
| Prompt-Injection-Schutz | **betrifft dieses Werkzeug nicht** | Keine KI liest die Texte. |
| DSGVO und Schweizer Datenschutz | **offen**, klein | Keine Gästedaten. Personenbezogen ist nur der eingetragene Name im Protokoll. |
| Datenlöschung | **offen** | Verlauf, Protokoll und abgelöste PDF werden nie gelöscht. |
| Verfügbarkeit | **offen** | Gäste berührt das Werkzeug nicht; fällt es aus, bleibt Veröffentlichtes. |
| Monitoring | **offen** | `GET /_werkzeuge/carte/api/gesund` liefert den Zustand, niemand fragt ihn ab. |
| Booking-Integration | **betrifft dieses Werkzeug nicht** | Karten haben mit Reservationen nichts zu tun. |
| Druck und Dateien | **erfüllt** (lokal) | node, Playwright/Chromium (`Tasty Website Builder/node_modules`), poppler vorhanden; fehlt etwas: Stichwort DRUCK, nichts veröffentlicht. |

Kein Passwort vorerst; bei der Auslieferung ans Haus kommt die Anmeldung vor das Werkzeug (Satz für die Werkbank).

## Offen (auch in `stand.json`)

- Anschluss an die Website fehlt: die Seiten zeigen die Karten aus website/inhalt/*.json, keine Seite verlinkt eine PDF. Die Tafel schreibt nicht in website/ (Station 14 verbindet) (_werkzeuge/carte/web.py, carte.py _anschluss)
- Lunch-Menü: Wochentage und Uhrzeit nennt die PDF des Hauses nicht (Feld Zeiten leer); Gänge nach Reihenfolge als Vorspeise, Hauptgang, Dessert benannt (die Namen stehen nicht auf der Karte) (_karten/stand/lunch.json, Lunch_261019.pdf)
- Online-Fassung nicht gebaut und nicht hochgeladen (online.json aus der Vorlage, Speicher-Schicht api/_speicher.py fehlt im Haus); Veröffentlichen online in der Demo ohnehin aus (_werkzeuge/carte/online.json)
- Kein Passwort, Rollen ohne Anmeldung, keine Kopie ausserhalb des Rechners, keine Überwachung (Prüfpunkte 7a, bei Auslieferung) (_kette/11-werkbank/werkzeuge/karten/STAND.md)
- Die 9 Berichtigungen von Station 10 (Tippfehler des Originals, z. B. «Pickels» → «Pickles», «M wSt.» → «MwSt.») stehen im Satz der Werkbank schon im Grundstand; beim Gasterntal lagen sie als Entwurf zur Freigabe im Werkzeug. Roberts Wort, ob so oder als Entwurf (website/_werkbank/berichtigt.json, _karten/berichtigt.json)
- Der gemeinsame Rahmen liegt zweimal: _werkzeuge/oberflaeche/ und website/assets/oberflaeche/ (beide am 20.10. gleich nachgezogen). Station 14 entscheidet, welcher bleibt (_werkzeuge/oberflaeche/kleid/schloessli.js, website/assets/oberflaeche/kleid/schloessli.js)
- Flaschenbilder der Weinkarte (172) kommen aus dem Weinberater der Website (Vivino); Rechte dort offen, nur zur Anschauung (website/wein_bilder.py, _werkzeuge/carte/satz/weinbilder.json)

## Wünsche an den Stamm

- Der gemeinsame Rahmen (`oberflaeche/`) gehört je Haus an eine Stelle in `website/assets/oberflaeche/`; vorläufig `_werkzeuge/oberflaeche/`, ausgeliefert von jedem Werkzeug-Server.
- Die Bausteine des Werkbank-Satzes (Kapitälchen `span.kl`, Kürzel-Marke `sup.sb-kz`, `section.sb-r`) kennt jetzt `satz/satz.js` des Schlössli; gehört in eine gemeinsame Fassung von satz.js, damit jedes Haus mit dem Werkbank-Kit sie hat.

**Nachgeprüft 20.10.2026 (Chat «Schlössli · Werkbank und Beigaben»):** die fünf Punkte von 01:00 (Plus-Knöpfe, Knöpfe nie über Bild, keine Fläche hinter den Kreisen, Fortgeschritten nichts abgeschnitten, untere Leiste) sitzen in WebKit und Chromium, 1440 und 1000. Dazu behoben: Knopfzeile einer gewählten Rubrik bricht fest um (Knopf oben, sechs Kreise darunter), Kopf-Titel überdeckt bei 920 bis 1240 px nie die Knöpfe («Website ansehen» dann nur als runder Knopf, Kleid für alle Werkzeuge), `einlesen.py` brach an Hausweinen ohne Weingut ab. Fehlerbuch 10a und Abschnitt 9 nachgetragen.
