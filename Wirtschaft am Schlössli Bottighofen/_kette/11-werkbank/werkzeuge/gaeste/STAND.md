---
tags: [projekt, website]
status: entwurf
---

# Das Reservationsbuch (La Réception) · Wirtschaft am Schlössli, Bottighofen · Station 11, Teil `gaeste`

Werkzeug-Anpasser, 19.10.2026. Auftrag: Chef-Chat Kuchler («komplette Werkbank», Robert 19.10.2026). Welt `land` aus `marke.json`; Name **Das Reservationsbuch** (Robert 19.10.2026 «passt»). Alle Werkzeug-Namen kommen nur aus `_werkzeuge/oberflaeche/kleid/schloessli.js` (`WO_HAUS.namen`) und werden nur über `WO.name()` gezeigt (Kopf, Titel, Startfehler, Prüfseite, Anleitung über `studio/namen.js`, Rundgang); kein Name ist fest eingetippt. Nichts online, nichts verschickt, keine KI-Aufrufe, kein Schlüssel gelesen.

## Adresse

- Werkzeug: http://127.0.0.1:9047/_werkzeuge/reception/ · Prüfseite `pruefung.html` · Anleitung `anleitung.html`
- Starten (aus dem Projektordner): `python3 _werkzeuge/reception/server.py 9047` (in `~/SecondBrain/.claude/launch.json` als «gastgeber-schloessli»). Ohne `RECEPTION_KI=1` antworten Chat, Brief, Übersetzen und Wissen-Einlesen mit Probe-Antworten (E23).
- Ordner: `Wirtschaft am Schlössli Bottighofen/_werkzeuge/reception/` (Projektebene wie La Carte und La Maison; die Website wird nur gelesen). Kleid: das gemeinsame `_werkzeuge/oberflaeche/kleid/schloessli.*` (Rahmen «Die Bühne»), unverändert übernommen.
- Stand-Weg für Die Stube: `GET /_werkzeuge/reception/api/ueberblick` → `{anfragen_neu, anfragen_offen, ohne_antwort, fragen_gesamt, …}`.

## Was gebaut ist

Grundlage ist der Gastgeber des Landgasthof Ruedihus (17.10.2026, abgenommen), nicht der Stamm in `_Werkzeuge/`: Master Werkzeug-Bau Abschnitt 2.1 und Regel 62 verlangen dieselbe Technik und dieselben Funktionen wie die bestätigten Häuser, je Haus im eigenen Projekt. Kopie per `rsync` ohne Daten; alle Hauswerte ersetzt, die Bauskripte des Ruedihus liegen nur noch als Vorlage in `_bau/vorlage-ruedihus/`.

**Auf ein Restaurant ohne Zimmer umgestellt:**
- **Arten im Eingang:** Reservation, Bankett, Anlass, Gutschein, Nachricht (statt Zimmer, Fest, Sitzung, Spa, Anreise). Auswahl oben: Reservation, Bankett, Gutschein. Eine Adresse für alles (`kontakt@schloessli-bottighofen.ch`, Kontaktseite).
- **Hinweise je Anfrage** (neu, `reception.hinweise`): Ruhetag (Dienstag, Mittwoch), Ferien (13.–15.11.2026 Excellence Gourmetkreuzfahrt, 22.12.2026–10.02.2027), mehr Personen als eine Etage fasst («auf zwei Etagen Platz für jeweils bis zu 26 Personen», Seite Karten), Allergien. Gerechnet aus Angaben der Kontaktseite, nichts geschätzt.
- **Allergien:** die Kürzel der Karten des Hauses (G, L, E, F, S, So, En, N, Se; VEG) kommen aus dem Formular als Klartext in die Angaben, in die Liste und in den Brief («[Küche informieren]»). Der Brief sagt nie von sich aus, ein Gericht sei frei davon.
- **Brief im Ton des Hauses:** Das Schlössli hat keine eigenen Mail-Vorlagen. Grundlage sind die Fragen, die das Haus in seinen eigenen Mail-Links stellt (`vorlagen/bankett.txt` aus «Bankettanfrage», `vorlagen/anlass.txt` aus der Event-Reservation, `vorlagen/gutschein.txt` aus dem Gutschein-Formular), wörtlich ausgelesen (`_bau/schloessli_wissen.py`). Gruss «Mit freundlichen Grüssen» wie in den Mail-Links. Briefkopf «Wirtschaft am Schlössli · Direkt im Hafen von Bottighofen», Fuss mit Adresse, Telefon, Mail der Kontaktseite. PDF «Wirtschaft am Schlössli – Name – Datum.pdf».
- **Wissen des Chats** aus den Originalen (`_quelle/website/text`, `pdf-text`: 11 Seiten, Speisekarte Oktober, Lunch, Lästermeile, Bankettmenüs, Weinkarte, 4-Hands-Lunch; 83 210 Zeichen) plus `gast_umgebung.txt` (Lage, Anreise, Geschichte, Schwesterhaus, je Zeile mit Quelle aus `fakten.json`). Steckbrief «Das weiss der Chat»: 40 Zeilen in 7 Bereichen, jede wörtlich belegt (`steckbrief_bau.py` bricht sonst ab). Bewusst nicht drin, weil nirgends belegt: Kinderstuhl, Schiff, Rollstuhl, Namen der Etagen.
- **Chat:** Restaurant-Anweisung (Reservation statt Zimmerbuchung, Ruhetage, Allergien), Muster aus der Kontaktseite, kein Wetter, keine fremden Musterantworten mehr.
- **Chat ausprobieren:** Die Website hat keinen Chat. Rechts steht deshalb ein eigenes Chatfenster im Kleid des Hauses (wie auf dem Handy), das denselben Weg `/api/gast` fragt. Anfragen daraus sind «Beispiel».
- **Formulare der Website → Eingang:** `baustein/anfrage.js` mit `ANLEITUNG.md` für Station 14. Fängt die fünf Formulare (Reservation, Bankett, Gutschein, Plätze, «Ihr Abend») ab, ohne haus.js/funktionen.js zu ändern; «Vielen Dank» erst, wenn der Gastgeber angenommen hat. Auf der Website nichts eingebaut.
- **Beispiele (M27):** 7 Anfragen (Terrasse mit Nüssen, Bankett in den Ferien mit 30 Personen, Gutschein, englische Reservation am Ruhetag mit deutscher Lesefassung, Vormerken für den 4-Hands-Lunch, Chat-Anfrage mit Hund, Firmenanlass mit Herbstmenü), 10 Fragen (davon 2 Lücken), «Vom Team nachgetragen» mit drei beschrifteten Beispielkarten. Jede Angabe in den Beispielbriefen steht so in den Quellen (Preise, Zeiten, Plätze, Ferien, AGB Ziffer 3 und 7); Namen und Adressen erfunden (example.com), überall «Beispiel».
- **Kleid:** Farben des Ruedihus auf die Farbwelt A «Stuhl und See» umgerechnet (`_bau/schloessli_kleid.py`), Open Sans aus der Wortmarke, Punktraster mit Zeiger als Tapete, Zeiger als Zeichen, Fotos nur des Hauses (Terrasse, Gaststube, Bar, Wein, Hafen), kein Bild des Schäfli. Farben im Brief in einer Reihe (M25). Fassungsnummern aus dem Inhalt (`_bau/fassungen.py`, M20).

**Was der Stamm nicht konnte und warum neu:** Hinweise und Allergene (kein Hotel hatte sie), Brief ohne Hausmails (Vorlagen aus den Mail-Links), Chat ausprobieren ohne Chat auf der Website, Anschluss an Formulare, die schon eigene Fenster haben (Ruedihus öffnete ein eigenes Fenster).

## Geprüft (19.10.2026, unsichtbar, eigener Server :9048 mit Wegwerf-Daten, Probe-Antworten)

`pruefung/schloessli.js` bedient statt lädt: jede Ansicht zweimal; Hinweise bei den richtigen Anfragen; Auswahl zählt; Brief schreiben, ändern, sichern, neu laden; PDF; erledigt/offen; Deutsch lesen; Lücke nachtragen und entfernen; Wissen suchen (Treffer und «noch nicht im Wissen»); Chat ausprobieren mit Anfrage; alle fünf Website-Formulare über den Baustein bis in den Eingang (mit Allergenen und Hinweisen); Sicherheit des Wegs `formular`; Handy-Rand. Jede Spur «QA» weggeräumt.

| Lauf | Ergebnis |
|---|---|
| Chromium 1440 | 24 von 24 |
| Safari-Kern (WebKit) 1440 | 23 von 23 |
| Chromium 390 | 24 von 24 |
| Safari-Kern 390 | 24 von 24 |
| Prüfseite und Anleitung, beide Motoren, 1440 und 390 | ohne Fehler, ohne 404, ohne Überlaufen |

Flüssigkeit (Chromium, 1440, Wechsel aller Ansichten und Scrollen): 4× gedrosselt 114 Bilder/s, 1 Bild über 50 ms (91 ms) bei ruhigem Rechner; im Schlusslauf bei Last 64 und Akku 111 Bilder/s (3 über 50 ms, längstes 183 ms), 6× 107 Bilder/s (4 über 50 ms, längstes 258 ms). Die langen Bilder fallen auf den Augenblick des Ansichtswechsels.

## Aus den anderen Häusern übernommen und am Stand geprüft (Auftrag Oberchef, 19./20.10.2026)

- **Namen des Schlössli** (Robert 19.10.: «passt»): nur über `WO.name()` aus `kleid/schloessli.js`; Prüfseite und Anleitung laden dafür das Kleid und `studio/namen.js`.
- **Bilder in jeder Liste** (Robert 19.10.: «in allen Tools Bilder dazu»): Eingang (je Art), Das wurde gefragt (je Thema), Vom Team nachgetragen (Karten mit Foto oben, auch die Beispiele), Das weiss der Chat (jede Angabe mit eigenem Foto, Personen mit Porträt, Bereiche mit Foto), Offen bei Ihrem Team, Links, Zuletzt geändert. Neuer Prüfschritt: jeder Eintrag hat ein geladenes Foto. Doppelte Einträge: keine gefunden.
- **Gemeinsames Kleid** `_werkzeuge/oberflaeche/kleid/schloessli.*` unverändert, kein eigenes.
- **Fehlerbuch 10a «roher Code im Bild»:** neuer Prüfschritt sucht `{…}`, `undefined`, `NaN`, `None`, `null` in allen Ansichten und jeder Anfrage: nichts gefunden.
- **Jede Auswahl im Hausstil** (Robert 11./12.10.): Die Vorlage öffnete im Wissen noch drei Systemlisten und einen Systemkalender. Jetzt eigene Auswahl und eigener Kalender (`studio/auswahl.js`), bedient im Prüflauf (Bereich und «Gilt bis»), auch am Handy.
- **Beispiele statt Leere (M27):** Eingang 7, Fragen 10, «Vom Team nachgetragen» drei beschriftete Karten.
- **Deutsch lesen** (Werdegang La Réception): bedient, Lesefassung erscheint (Schritt im Prüflauf).
- **Farbfelder in einer Reihe (M25), Fassungsnummern aus dem Inhalt (M20), Weg zum Hafenbüro im Kopf, Briefe als Brief auf Papier, kein Mailprogramm (E28):** am Stand nachgesehen.

## Roberts Beanstandungen

- **20.10.2026, Eingang:** Abstand Bühne zu den Kacheln zu klein; unten eine andere Farbe als oben (Petrol statt Blau, nachdem die Website auf «Ton in Ton» gedreht war). Behoben: alle Arbeitsflächen auf die Töne des Kleids (`_bau/schloessli_blau.py`, Variablen `--wo-nacht/-nacht2/-tief`), 34 px Luft unter der Bühne (Handy 24 px), langer Name im Kopf am Handy gekürzt. Vier Läufe grün, Anleitungsbilder neu. Im Fehlerbuch (Master 10a).
- **20.10.2026, zweite Runde:** Schilder zu nah an der Schrift, Angaben unübersichtlich, Sammeltitel als Zitat, Leerraum in der Karte, Nachricht als Rohtext, Antworten des Chats roh, Nachtrag-Karten eng, Rundgang-Schild wanderte beim Scrollen. Behoben: Angaben in Gruppen (Wann · Gast · Woher), Zitat nur aus den Worten des Gastes, Formular als Liste Feld · Wert, Gespräch zugeklappt statt Karte gestreckt, Antworten als gesetzte Antwort mit Liste, Luft in den Karten, Schild fest über der Leiste. Neuer Prüfschritt misst Abstand, Leerraum und Schild. Sechs Zeilen im Fehlerbuch (Master 10a), Schild-Regel gilt für alle Häuser.
- **20.10.2026, Namensabfrage (Regel Robert über das Kartenpult):** «Wer trägt ein?» ist raus. Einträge laufen fest unter «Team Schlössli», eine Anmeldung kommt erst mit der Auslieferung. Vier Läufe grün.

## Prüfpunkte (Liste aus `_Werkzeuge/STAND.md`, Master 7a)

| Prüfpunkt | Stand | Beleg oder was fehlt |
|---|---|---|
| Backend | offen | Läuft nur, solange `server.py` auf diesem Rechner läuft. Ohne Server: Startfehler-Tür mit «Prüfung öffnen». Nichts startet ihn neu. |
| Datenbank | erfüllt am Rechner | Dateien unter `daten/`, `.gut`-Sicherung vor jedem Schreiben, beschädigte Datei → Sicherung; Konflikt am Brief mit Fassungsnummer (E21). Online-Speicher fehlt (Station 16). |
| Authentication und Rollen | offen | Kein Passwort bis zur Auslieferung (Robert 15.10.2026). Name je Gerät für das Protokoll. |
| Rechteverwaltung | offen | fehlt wie in allen Häusern (`_wache.py`, Master 5.3). |
| API-Sicherheit | teils erfüllt | Nur 127.0.0.1, Host 421, fremde Herkunft 403, nur JSON 415, 3 MB 413, Formular: Kontakt geprüft 422, über 12 kB 413, Maschinenfeld; Lesen nur von der eigenen Seite. Einbetten nur auf der eigenen Seite und in der Karte der Kette (`frame-ancestors`). Beleg Schritt «Sicherheit» in allen vier Läufen. |
| Rate Limits | teils erfüllt | 900 Aufrufe, 120 Änderungen, 8 PDF, 6 Formulare je Absender und Minute; Chat 20 in 10 min, 80 am Tag, 2000 gesamt. Nicht für ein Restaurant bemessen. |
| Logging | teils erfüllt | Protokoll des Wissens («Zuletzt geändert» mit Namen), Browserfehler nach `daten/fehler.jsonl`, sichtbar auf der Prüfseite. |
| Backups | offen | `.gut` je Datei, «Alle Daten herunterladen» als ZIP (E19). Keine Kopie ausserhalb des Rechners. |
| Deployment | offen | Nichts hochgeladen. Online-Fassung noch die des Ruedihus (`_bau/vorlage-ruedihus/online/`), vor Station 16 anzupassen. |
| CMS-Datenmodell | erfüllt | Wissen, Steckbrief, Vorlagen und Haus-Werte aus Skripten neu baubar (`_bau/schloessli_wissen.py`, `steckbrief_bau.py`); Beispiele in `gast_beispiele.json`. |
| Übersetzungsworkflow | teils erfüllt | Brief in der Sprache des Gastes, deutsche Lesefassung (Beispiel Emma Clarke). Echte Übersetzung erst mit KI; Oberfläche nur Deutsch (R24). |
| KI-Kosten | offen | Standard ohne KI (E23). Mit `RECEPTION_KI=1` nur Schlüssel aus der Umgebung; Monatsgrenze für dieses Haus nicht gesetzt, Kosten je Frage am Schlössli nicht gemessen (Kostenrunde). |
| Prompt-Injection-Schutz | teils erfüllt | Bauart wie Ruedihus (Text der Gäste nur im Gespräch, Werkzeuge mit festem Schema, Anfrage nur mit Kontakt im Text). Am Schlössli nur mit Probe-Antworten geprüft. |
| DSGVO und Schweizer Datenschutz | offen | Datenschutzerklärung nennt die Formulare und den Chat nicht; Vorschlag in `baustein/ANLEITUNG.md` Punkt 6, vom Haus zu prüfen. |
| Datenlöschung | erfüllt am Rechner | Nach zwölf Monaten von selbst; einzeln je Anfrage und Frage mit Rückfrage (Schritt «Chat ausprobieren» und Formulare löschen ihre Spur). |
| Verfügbarkeit | teils erfüllt | Ohne KI Probe-Antworten, ohne Server Tür; Baustein meldet Ausfall mit Telefonnummer, Eingaben bleiben. |
| Monitoring | offen | Niemand wird gerufen; Stand-Weg `ueberblick` für Die Stube. |
| Booking-Integration | betrifft nicht | Reserviert nichts im gastronovi; zeigt nur den Weg zur Reservation online. |

## Offen

1. Station 14: Baustein einbauen (`baustein/ANLEITUNG.md`) und den Weg `formular` lokal vom Hausserver :8982 an :9047 reichen; Datenschutz-Absatz.
2. Echte KI (Brief, Übersetzen, Chat, Wissen einlesen) nicht geprüft: erst in der Kostenrunde auf Roberts Wort.
3. Online-Fassung (online.json, Funktionen) fürs Schlössli bauen, vor Station 16.
4. Firefox und 320 px nicht gelaufen; Station 12 prüft.
5. Ob «Hunde willkommen» auch für die Terrasse gilt, steht nur in Falstaff und Tagblatt, nicht auf der Seite des Hauses.

**Nachgeprüft 20.10.2026 (Chat «Schlössli · Werkbank und Beigaben»):** Brief in «Nur Text» sieht aus wie «Gestalten» (Beanstandung 01:08): Betreff in derselben Schrift und Stärke, bricht um, Enter macht keine neue Zeile; Linie unter dem Kopf; Schreibfelder ohne Rahmen und Füllung. Geprüft nebeneinander in Chromium und WebKit, 1440 und 390; Speichern → neu laden → zurück geprüft. Fehlerbuch 10a nachgetragen.
