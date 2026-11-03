---
tags: [projekt, website]
status: entwurf
---

# Die Hausdruckerei (L’Imprimerie) · Wirtschaft am Schlössli · Station 11, Teil `druck`

Stand 19.10.2026, Werkzeug-Anpasser `druck`. Bauer ist nie Prüfer: Station 12 prüft in einem neuen Chat.

## Wo

- **Werkzeug:** http://127.0.0.1:9053/_werkzeuge/imprimerie/ (eigener Prüfserver der Hausdruckerei: `python3 _werkzeuge/imprimerie/serve.py 9053` im Projektordner, launch.json «werkstatt-schloessli»). Prüfseite: http://127.0.0.1:9053/_werkzeuge/imprimerie/pruefung.html · Newsletter: http://127.0.0.1:9053/_werkzeuge/imprimerie/mail.html
- **Ordner:** `Wirtschaft am Schlössli Bottighofen/_werkzeuge/imprimerie/` (neben `carte`, `maison`, `livre`, `reception`, `registre`; Oberfläche gemeinsam unter `_werkzeuge/oberflaeche/`, Kleid `kleid/schloessli.*` vom Chat «Besucherbuch», nicht geändert). `website/` ist unberührt.
- **Der Server bildet die Wege des Hauses nach** und liefert nur lesend: `/assets/img/` und `/assets/fonts/` aus `website/assets/`, `/assets/oberflaeche/` aus `website/assets/oberflaeche/` oder, solange es das nicht gibt, aus `_werkzeuge/oberflaeche/`, `/_werkzeuge/livre/` (livre.json, dateien, fotos) aus dem Hausbuch. Markenprüfung geht an den Server des Hausbuchs (`LIVRE_SERVER`, Standard http://127.0.0.1:9049).
- **Name:** **Die Hausdruckerei** (Robert 19.10.2026 «passt», über den Chef-Chat Kuchler), Wege «Das Hafenbüro», «Das Bildarchiv». Die Namen stehen an einer Stelle: `_werkzeuge/oberflaeche/kleid/schloessli.js` (`WO_HAUS.namen`). Der Kopf liest sie über `WO.name()`, die übrigen sichtbaren Sätze setzt `_qa/schloessli_anpassen.py` aus derselben Zeile mit Grammatik («in der Hausdruckerei», «zum Hafenbüro»); Tausch = Zeile im Kleid ändern und den Lauf wiederholen.
- **Stand für Das Hafenbüro (M17):** `GET /_werkzeuge/imprimerie/haeuser/schloessli/vorlagen/index.json` → `[{art, format, zahl}]`, Summe **248 Vorlagen in 23 Arten**.

## Was gebaut ist

Kopie der Werkstatt (L’Imprimerie) des Berghotel Gasterntal (17./18.10.2026, Kern Carlton → Rivage, alle Korrekturen I01–I16, F45, F79, KI-FREIGABE), angepasst an ein **Restaurant am Hafen ohne Zimmer**. Alles wiederholbar, nichts von Hand in den Kerndateien:

```
python3 bau.py                      Marke: Farben, Schriften, Zeichen, Tapete, 42 Fotos des Hauses → haeuser/schloessli/
python3 _qa/wissen_bau.py           Wissen des Hauses → api/_daten/schloessli-wissen.txt
python3 _qa/vorlagen_schloessli.py  248 Vorlagen, katalog.js, Beispiele, sechs Mails (bricht ab bei jedem nicht belegten Satz, jeder Zahl, jedem Preis)
node _qa/mail_marken.js             Kopf, Fuss, Trenner der Mails als Bild
python3 _qa/schloessli_anpassen.py  Kern aus _qa/carlton-vorlage/ ins Kleid des Schlössli; schreibt _qa/reste.txt
zsh _qa/kette_demo.sh               Prüfkette (PDF aller Vorlagen, Funktionen, Rahmen, Sonderfälle, KI-Probe, Markenprüfung-Probe, Zahlen, echte Maus, Mails)
```

**Marke (aus dem Projekt gelesen):**
- Farben aus `website/assets/css/haus.css :root`: Farbwelt A «Stuhl und See» aus dem Markenbuch, wie die Website sie seit Roberts Wort «Ton in Ton» trägt (`website/farbwelt.py`, Petrol um 21° auf das Blau des Platztellers gedreht). Stuhlblau `#0a234c` als dunkler Grund, Seehimmel `#a2b6cf` für Linien, Zeichen und kleine Zeilen, Papier `#e7ecf3`, Seespiegel `#d0dae7`, Blatt `#f3f6f9`, Tinte `#041023`, Schirmrot `#fd9964` nur als Marke «Entwurf». Dieselben Werte wie das Kleid der Werkzeuge und die Werkbank.
- Schriften `website/_werkbank/fonts/`: Open Sans 400 (Titel, aus der Wortmarke gemessen), Instrument Sans, DM Mono, alle eingebettet.
- Zeichen: die Zeiger im Kreis aus dem Logo (`website/assets/svg/zeichen.svg`), Pfade unverändert.
- Tapete: das Punktraster mit den Zeigern als Medaillon (`website/assets/svg/tapete-a-*.svg`), 14 mm Rapport im Druck.
- Fotos: 42 Fotos, davon 27 vom Haus selbst in Vorlagen. **Nicht übernommen** (30, Grund je Foto in `bau.py RAUS`): KI-Bilder (Feuerwerk, Heft der Gemeinde), Gästefotos Tripadvisor, Fotos des Schäfli, Excellence, Papageno, Guide Michelin, Schweiz Tourismus, Stimmungsbilder, das Feuerwerk mit ungeklärtem Bildrecht. Commons-Fotos (Hafen, Luftbild 1954, Säntis …) liegen im Bildarchiv mit Namensnennung, nie in Vorlagen. Instagram-Bilder des Hauses (360 px) nur im Archiv.

**Vorlagen: 248 in 23 Arten, jeder Satz belegt, keine Preise** (Master: «rund 250 Vorlagen», Robert 15.10.2026)
- **186 in 11 Abteilungen:** Empfang & Reservation 13 · Karte & Küche 37 · Lunch-Menü 7 · Lästermeile 18 · Wein & Keller 11 · Banketts & Gruppen 30 · Events & Termine 13 · Gutscheine 8 · Zeiten & Ferien 10 · Hafen & Ansichtskarten 14 · Team & Marketing 25.
- **12 Anlässe × 4 Motive = 48:** mit Datum Excellence Gourmetkreuzfahrt (13.–15.11.2026) und Winterferien (22.12.2026–10.02.2027); ohne Datum Lunch-Menü, Lästermeile, Banketts & Gruppen, Gutschein, Die schönste Terrasse am Bodensee, Die Karte, Weinkarte, Das Team; Seenachtfest und 4-Hands-Lunch mit «[Datum]» (die belegten von 2026 sind vorbei).
- **14 Hinweise im Haus:** Geschlossene Gesellschaft, alle Tische vergeben, Terrasse geschlossen, Küche geschlossen (Lästermeile hat offen), Ruhetag, Ferien, An Bord, ausgebucht, bitte warten, Reinigung, nasser Boden, ausser Betrieb, Parkplatz, Fundsachen.
- **9 Newsletter-Bilder und 6 versendbare Mails** (Ferien, Lunch, Banketts, Einladung 4-Hands-Lunch, Bestätigung der Reservation, Nach dem Besuch). Kein `mailto`-Knopf; Anfrage-Knöpfe führen auf die Website.
- **Für ein Restaurant:** Reserviert-Karten (Restaurant, Terrasse, Lästermeile), Tischnummern, Tischpläne, Platz-, Menü- und Tischkarten fürs Bankett, Bankettmenüs Frühling, Sommer, Herbst mit Deckblatt, Bankettmappe (Deckblatt, «Was wir wissen möchten», «Gut zu wissen» aus den AGB), Einladungen (Familie, Firma, Geburtstag, 4-Hands-Lunch), jedes Gericht der Karte und jede Tapa der Lästermeile als Empfehlung am Tisch, Weinkarte (Champagner, Thurgau, Rosé, Wein des Monats), Gutscheine mit Umschlagkarte, Öffnungs- und Küchenzeiten, Ferien, Ansichtskarten vom Hafen, Namensschilder des Teams, Pressemappe, Auszeichnungen, «Ein Besen statt Schild» aus der Geschichte.
- **Bewusst nicht drin:** Preise jeder Art (stehen nur auf den Karten der Tafel); Kofferetiketten, Türhänger, Zimmer- und Housekeeping-Karten (keine Zimmer; die Art «Türhänger» ist aus «Neu erstellen» entfernt, «Tagungsmappe» heisst «Bankettmappe»); das Schwesterhaus Schäfli in jeder Form; Blätter zum Ausfüllen (Robert hat Felder zum Ausfüllen abgelehnt, Master 8); Visitenkarten; Ansichtskarten bei Nacht oder von innen.
- **Quellen:** Seiten der heutigen Website des Hauses (`_quelle/website/text/`), PDF-Unterlagen (Speisekarte Oktober, Lunch-Menü, Lästermeile, Bankettmenü, 4-Hands-Lunch, Weinkarte 14.10.2026), `website/inhalt/haus.json`, Texte der neuen Website. Sätze wörtlich (`Q`), Gerichte ohne Gross/Klein (`QI`), «ß» der Bankettkarte als «ss» (`QS`, Markenbuch «nicht: ß»), jede Zahl über `zahlen_pruefen()`.

**Kleid:** gleiche Bedienung und Anordnung wie Carlton, Doldenhorn, Ruedihus, Gasterntal; Kopf, Rand und Startbilder aus dem gemeinsamen Paket «Die Bühne» mit dem Kleid des Schlössli; Hausschicht `haeuser/schloessli/oberflaeche.*` (Quelle `_qa/haus/`). Fotos je Ansicht aus dem Haus (Terrasse, Moni, Gaststube, Wegweiser, Abend, Platanen, Fliesen, Regal, Bar, Glas, Tortelloni). Kanten rund wie die Naben der Zeiger, der Horizont als feine Linie unter dem Kopf, nie kursiv, keine Einkerbungen. Gründe heissen Stuhlblau, Papier, Seespiegel.

## Was neu gebaut wurde und warum der Stamm es nicht konnte

- Der Stamm `_Werkzeuge/` hat keine Hausdruckerei (nur `website`, `karten`, `gaeste`). Gebaut ist sie deshalb wie in den Maeder-Häusern als Werkzeug im Projekt mit eigenem Server, Vorlage Gasterntal.
- Restaurant statt Hotel: Abteilungen, Anlässe, Hinweise, Mails, Beispiele, Arten, Suchwörter, «sechs Beispiele» der Übersicht neu aus dem Betrieb des Schlössli.
- `serve.py`: die Website liegt in `website/` neben `_werkzeuge/` (bei den Kandertal-Häusern ist das Projekt die Website).
- `_qa/svg_png.js`: die Tapete des Hauses ist SVG, die Hausdruckerei braucht sie als Kachel mit Alpha (PDF).

## Selbst geprüft (20.10.2026, unsichtbar, eigener Server :9053, ohne KI)

Logs: `_werkzeuge/imprimerie/_qa/lauf/`.

| Lauf | Chromium | Safari-Kern |
|---|---|---|
| PDF jeder Vorlage über «Druckfertig speichern» (`pruefung_250.js/.py`) | 251 von 251 ohne Befund, 0 Konsolen- oder Seitenfehler, 12 Formate, Schriften eingebettet, 0 Masken, 0 Verläufe, 0 Angaben ausserhalb des Wissens; PDF gegen Bildschirm Median 2,02, höchstens 4,19 von 255 | – |
| Funktionsliste 1440 × 900 | 106 / 106 | 106 / 106 |
| Funktionsliste 390 × 844 | 103 / 105 | 103 / 105 |
| Rahmen (R03, R04, R07, R09, R15, R17, R19, R23) | 8 / 8 | 8 / 8 |
| Sonderfälle (zwei Fenster, 5'000 Zeichen, `<script>`, Emoji, Foto 30 MB / 400 px, kaputte Arbeitsdatei, Netz weg, leeres Guthaben) | 22 / 22 | 22 / 22 |
| KI-Probe (ohne KI) | 8 / 8 | 8 / 8 |
| Markenprüfung-Probe | 5 / 5 | 5 / 5 |
| Zahlen und Reste anderer Häuser | 44 grün, 0 rot | 44 grün, 0 rot |
| Echte Maus 1440 / 390 | 37 / 37 · 37 / 37 | 37 / 37 · 37 / 37 |
| Werkzeug-Oberfläche «Die Bühne» (1440, 390, 320) | 22 / 22 (beide Kerne) | |
| Mails (sechs, Bilder da, keine Reste, kein `mailto`) | 7 / 7 | – |

Die zwei offenen Zeilen am Handy sind in allen Häusern dieselben und gewollt: «eine grosse, drei Querkarten» und «Mosaik mit zwei grossen Kacheln» stehen am Handy untereinander.

**Nachgezogen 20.10.2026 (Vorgaben über den Chef-Chat und das Oberchef-Fehlerbuch):**
- Namen des Hauses aus dem Kleid (siehe oben), Prüfskripte auf «Die Hausdruckerei» und «Das Hafenbüro» umgestellt.
- **Bilder in jeder Liste:** Anlässe & Events, Anlässe der nächsten Wochen, Abteilungen, Newsletter zeigen das Foto des Eintrags; die Listen der Vorlagen, Hinweise im Haus, Arten, Meine Medien und Freigegeben zeigen das gesetzte Blatt als Bild. Geprüft in allen Ansichten.
- **Doppelte zusammengeführt:** «Bitte warten», «Ruhetag», «Küche geschlossen» standen in einer Abteilung und unter den Hinweisen im Haus, jetzt nur noch unter den Hinweisen (251 → 248).
- Hotel-Wörter in der Oberfläche ersetzt: Filter «Zimmer & Empfang» → «Tisch & Empfang», Beispiel «Namensschild für die Rezeption» → «für das Team», Satz der Hinweise ohne «Bauarbeiten, Stromunterbruch».
- Fehlerbuch 10a «blaue Schrift auf Dunkel»: alle Titel und Sätze auf dunklen Flächen in allen Ansichten gemessen, keiner unter 3:1 (`_qa/kontrast.js`).
- Für die Werkbank (Fehlerbuch 10a «Abfrage vor dem Bild»): vor jeder Aufnahme der Hausdruckerei `localStorage['ds-schloessli-willkommen']='1'` setzen, sonst liegt die Begrüssung über dem Bild.

**Behoben beim Prüfen:** Kopf im Editor am Handy 44 px (390) und 42 px (320) zu breit → engere Knöpfe bis 430 px, «Speichern» bis 360 px nur als Knauf (Wort bleibt für Vorleser); Fotos, die die Hausdruckerei nicht zeigen darf, kamen über das Hausbuch herein (ein Gästefoto Tripadvisor als Ersatzfoto) → `marke.json raus`, `satz.js` filtert; Blatt «Bankettanfrage» zum Ausfüllen herausgenommen.

**Sicherheit** (curl gegen :9053): fremde Herkunft 403, kein JSON 415, 70 KB 413, Haus `../gbr` 400; `serve.py`, `bau.py`, `_qa/…`, `api/_daten/…`, `api/entwurf.py`, `.env.local`, Ausbruch über `/assets/img/..%2f..` je 404. «Fünf Entwürfe» antwortet mit Probe aus den Vorlagen.

**Flüssigkeit (Regel 55)**, Chromium unsichtbar, Last beim Lauf 7 bis 12:

| | 1440 px, 6× | 1440 px, 4× | 390 px, 6× |
|---|---|---|---|
| Galerie aller 251 Vorlagen, Scrollen schnell bis sehr schnell | Median 8,3 ms, längstes 50 ms, über 50 ms: 0 | längstes 34 ms, über 50 ms: 0 | längstes 91 ms, über 50 ms: 2 von 4'395 Bildern (ohne Skript und ohne Layout, nur Zeichnen) |
| Editor, neun Ansichten nacheinander | längstes 159 ms beim Wechsel der Ansicht (Gasterntal 157, Ruedihus 183, Carlton 142: Kern) | | längstes 133 ms |
| Titel ziehen mit Einrasten · Rückgängig | längstes 92 ms beim Greifen · 25 ms | | 59 ms · 17 ms |

Nicht geprüft (nach Auftrag, wie in allen Werkstätten): Firefox, echte Geräte, Druck auf Papier, Schnittmarken je Format, Grenze 40 Entwürfe je Stunde am Haus, echte KI.

## Wünsche an den Stamm / Funde

- **Tapete als SVG:** der Kern nimmt nur Rasterkacheln (`tapete-*.webp`). Vorläufig rendert `bau.py` das SVG der Website unsichtbar zu WebP.
- **Ports:** 9049 ist vom Hausbuch belegt (`_werkzeuge/livre/server.py 9049`), die Hausdruckerei läuft auf 9053.
- **Titel auf den Blättern in normaler Schreibung:** das Markenbuch setzt Titel in Versalien (Open Sans 0,16 em), der Kern der Hausdruckerei setzt Titel gemischt. Nicht umgebaut (Kern aller Häuser); Roberts Urteil offen.
- **Hausbuch führt Gästefotos (Tripadvisor) und KI-Bilder:** die Hausdruckerei filtert sie (`raus`), das Fach «Das Hausbuch» im Editor zeigt das Archiv des Hausbuchs aber so, wie das Hausbuch es führt. Sache des Hausbuch-Chats.
- **Kern:** «Übersicht» steht im Rand immer als dunkle Pille, auch wenn eine andere Ansicht gewählt ist (`hell.css .ms-nav>button[data-ansicht=start]`), in allen Werkstätten so. Nicht angefasst.

## Prüfpunkte (Liste aus `_Werkzeuge/STAND.md`)

| Prüfpunkt | Stand | Beleg, Lücke |
|---|---|---|
| Backend | **offen** | Nur `serve.py` auf diesem Rechner (Port 9053). Online-Fassung `online.json` liegt bereit (Form wie Gasterntal), nicht angeschlossen |
| Datenbank | **betrifft dieses Werkzeug nur im Browser** | Drucksachen liegen im Browser (localStorage, eigene Fotos IndexedDB); zwei Fenster überschreiben sich nicht (I01, Sonderfälle). Keine Ablage auf dem Server |
| Authentication und Rollen | **offen** | Keine Anmeldung (Robert 15.10.: kein Passwort bis zur Auslieferung). Die Hausdruckerei ändert nichts auf der Website |
| Rechteverwaltung | **offen** | fehlt |
| API-Sicherheit | **erfüllt lokal** | Server nur 127.0.0.1; Wache vor der KI (I02): fremde Herkunft 403, nur JSON 415, Grösse 413, 40 Entwürfe je Stunde 429, Hausname geprüft; keine Quellen (`.py`, `.md`, `_qa`, `api`) ausgeliefert (I06). Belege unten |
| Rate Limits | **erfüllt** | 40 Entwürfe je Stunde und Absender (`api/entwurf.py wache`) |
| Logging | **teils** | Fehlermelder schreibt Skriptfehler nach localStorage `sb-imprimerie-fehler`, die Prüfseite zeigt sie. Kein Änderungsprotokoll nötig, die Hausdruckerei ändert nichts am Haus |
| Backups | **teils** | «Alle Drucksachen als Datei sichern» und «Arbeitsdatei öffnen» (Prüfseite, I04, I07). Keine Kopie ausserhalb des Browsers |
| Deployment | **offen** | `online.json` bereit; andocken und hochladen macht Station 14/16. Online-Adresse des Hauses gibt es noch nicht (`ONLINE` vorläufig `schloessli-bottighofen-entwurf.vercel.app`). Nichts hochgeladen |
| CMS-Datenmodell | **erfüllt** | Sechste Hausdruckerei nach Carlton, Doldenhorn, Ruedihus, Gasterntal mit demselben Kern; ein Restaurant passt ohne neue Felder |
| Übersetzungsworkflow | **betrifft noch nicht** | Vorlagen nur Deutsch wie die Website; Bildtext der KI in sechs Sprachen (Kern) |
| KI-Kosten | **erfüllt (aus)** | Kein KI-Aufruf: ohne `IMPRIMERIE_KI=1` antworten «Fünf Entwürfe» und Bildtext mit Probe-Antworten aus den Vorlagen; online ohne Schlüssel `KI-FREIGABE · …`. Kein Schlüssel gelesen (Regel 54). Obergrenze 40 Entwürfe je Stunde |
| Prompt-Injection-Schutz | **erfüllt im Kern** | Auftrag und Wissen getrennt, Fakten nur aus dem Wissen, Unbekanntes als [Klammer]; Antwort wird als Daten geprüft. Echter Lauf ungeprüft (keine KI) |
| DSGVO und Schweizer Datenschutz | **betrifft kaum** | Keine Gästedaten; Drucksachen bleiben im Browser des Hauses |
| Datenlöschung | **erfüllt im Browser** | Meine Medien: löschen je Drucksache; Prüfseite: Fehler leeren |
| Verfügbarkeit | **erfüllt lokal** | Startfehler-Tür nach 15 s mit Grund (I05); ohne Hausbuch nimmt die Hausdruckerei ihre eigene Kopie der Fotos |
| Monitoring | **offen** | fehlt |
| Booking-Integration | **betrifft nicht** | Reservation bleibt bei gastronovi |
| Druck und Dateien | **erfüllt** | PDF im Browser (pdf-lib), Schriften eingebettet, 3 mm Beschnitt; Prüfung aller Vorlagen unten |

Kein Passwort vorerst (Robert 15.10.2026). In der Werkbank steht der Satz zur Auslieferung: alle Werkzeuge bekommen dann Anmeldung und Passwort.

## Für den Werkbank-Bauer (Station 14)

1. **Link in der Werkbank:** http://127.0.0.1:9053/_werkzeuge/imprimerie/ (lokal; Server muss laufen). Online nach dem Anschluss unter `/werkzeuge/imprimerie/`.
2. **Hausserver :8982** (`website/serve.py`) kennt `/_werkzeuge/…` heute nicht; die Hausdruckerei bleibt bis Station 14 auf ihrem eigenen Server.
3. **Hausbuch:** «In der Werkstatt gestalten» (Hausbuch-Knopf, heisst dort nach dem Namen des Hauses) zielt auf `../imprimerie/?foto=<k>&art=insta|story`; die Hausdruckerei liest es.
4. **Website:** nichts. Die Hausdruckerei ändert die Website nicht.
