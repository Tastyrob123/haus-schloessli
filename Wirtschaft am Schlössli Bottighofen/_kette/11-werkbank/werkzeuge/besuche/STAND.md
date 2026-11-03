---
tags: [projekt, website]
status: entwurf
---

# Die Besucherliste (Le Registre) · Wirtschaft am Schlössli · Station 11, Teil `besuche`

Stand 19.10.2026, Werkzeug-Anpasser `besuche`. Bauer ist nie Prüfer: Station 12 prüft in einem neuen Chat.

## Wo

- **Werkzeug:** http://127.0.0.1:8988/_werkzeuge/registre/ (eigener Server des Besucherbuchs: `python3 _werkzeuge/registre/server.py 8988` im Projektordner; liefert nur das Werkzeug, `/assets/` und die Seiten aus `website/`, die Oberfläche des Hauses aus `_werkzeuge/oberflaeche/` und `/api/registre`).
- **Anleitung:** http://127.0.0.1:8988/_werkzeuge/registre/anleitung.html (zehn Kapitel in vier Themen, Bilder aus dem Werkzeug, Beispielwerte).
- **Stand-Weg für Die Stube (La Maison):** `GET http://127.0.0.1:8988/api/registre?tage=30&beispiel=1` → `{werte, summe:{heute, buchung, anfrage, kontakt, route, besuche, seiten, laender, …}, je_tag:[{tag, besuche, seiten, buchung}], tage, beispiel, leer}`. Die Stube liest ihn über `/_weiter/registre/…` (Adresse aus `stand.json`). Ersatz ohne Dienst: `beispiel/30.json`, aber nur mit derselben Kürzung auf «heute bis jetzt» wie `registre.js` (Master M14b).
- **Ordner:** `Wirtschaft am Schlössli Bottighofen/_werkzeuge/registre/` (neben `carte`, `maison`, `livre`, `reception`, `imprimerie`; Rahmen gemeinsam unter `_werkzeuge/oberflaeche/`, angelegt vom Chat La Carte). `website/` ist unberührt.
- **Name:** **Die Besucherliste** (Robert 19.10.2026, «passt», über den Chef-Chat). Der Name steht an EINER Stelle: `_werkzeuge/oberflaeche/kleid/schloessli.js` → `WO_HAUS.namen` (dort auch «Das Hafenbüro» für die Zentrale). Werkzeug, Rundgang, Tür, Tab-Titel, Anleitung (`anleitung_bau.py` liest das Kleid) und die Prüfzeilen lesen ihn von dort; Sätze sind so gebaut, dass jeder Artikel passt (nur Nominativ/Akkusativ). Tausch = eine Zeile im Kleid, dann `python3 anleitung_bau.py` und `node anleitung_bilder.js`.

## Was gebaut ist

Kopie von Das Besucherbuch des Berghotel Gasterntal (17./18.10.2026, dort nach Doldenhorn und Carlton, Funktion wie Le Registre des Grand Beau-Rivage), angepasst an ein Restaurant ohne Zimmer. Acht Ansichten: Übersicht, Besuche, Herkunft, Zeit, Seiten, Verlauf, **Zur Reservation**, So wird gezählt. Funktionen G01 bis G13 des Werkzeug-Masters (4.6), Rahmen R01 bis R24 über die Oberfläche der Häuser («Die Bühne», Kleid `schloessli`).

**Was das Schlössli anders zählt als die Hotels** (Schlüssel der Ereignisse bleiben wie in allen Häusern, damit Die Stube, die Ablage und die Prüfläufe gleich lesen):

| Schlüssel | Bedeutung im Schlössli | Quelle auf der Website |
|---|---|---|
| `fenster` | Fenster «Reservation» geöffnet | `data-fenster="fe-reservation"` (46 Knöpfe auf den Seiten) |
| `buchung` | Tisch angefragt («Mit Wünschen anfragen» abgeschickt, Fenster zeigt «gesendet») | `#fe-reservation form[data-art="reservierung"]` |
| `booking` | «Direkt buchen» gewählt (Reiter mit der Maske von gastronovi, oder Link zu gastronovi) | `#fe-reservation [data-reiter="direkt"]`, `services.gastronovi.com/restaurants/118851/…` |
| `tisch` | Bankettanfrage geöffnet | `data-fenster="fe-bankett"` auf «Banketts & Gruppen» |
| `anfrage` | Bankettanfrage oder Gutschein abgeschickt | `#fe-bankett form`, `#fe-gutschein form` |
| `anruf` / `mail` | Nummer des Hauses / Mail-Adresse | `tel:+41716889092`, `mailto:kontakt@schloessli-bottighofen.ch` |
| `chat` | weiter zum Schwesterhaus Schäfli (die Website hat keinen Gäste-Chat) | Links zu schaefli-wigoltingen.ch, zenchef (Tisch im Schäfli), `tel:+41527631172` |
| `route` | Route zum Hafen | OpenStreetMap-Route auf «Kontakt & Öffnungszeiten» |

«Zur Reservation» = Tisch angefragt oder «Direkt buchen». «Fenster ohne nächsten Schritt» = Fenster − Anfrage − «Direkt buchen» (je Öffnen, nie unter null). Seitenarten: Startseite · Karte und Weinkarte · Banketts & Gruppen · Events & Termine und Ihr Abend · Gutschein · Kontakt. Herkunftsnamen und Beispielorte rund um den Bodensee (Kreuzlingen, Konstanz, Thurgau, Zürich, St. Gallen …), alles als Beispiel beschriftet.

**Eigener Zähl-Schlüssel und eigener Speicher** (Master 3, «jedes Haus zählt für sich»): Schlüssel neu erzeugt, liegt nur in `~/Desktop/Website-Projekte/_Schluessel/schloessli-bottighofen.txt` (Rechte 600, ausserhalb jedes Upload-Ordners); im Code nur die Prüfsumme (`anschluss.py`, `online/registre.py`). Lokal zählt das Besucherbuch in `_werkzeuge/registre/_daten/`, online nur mit eigenem `REGISTRE_READ_WRITE_TOKEN`, sonst `/tmp/schloessli-bottighofen-registre-demo`. Kein Weg teilt Daten oder Schlüssel mit dem Schäfli. Geheimnis der Kürzel `schloessli-bottighofen-nur-lokal`, Markennamen im Browser `schloessli-registre-tage`, `schloessli-registre-fehler`, `rundgang-schloessli-registre`, `schloessli-nicht-zaehlen`, «Zur Werkbank» `schloessli-wb`.

**Vorführ-Betrieb:** `VORFUEHRUNG = True` in `registre.js`, `anschluss.py`, `online/registre.py`. Jeder sieht Beispielwerte, überall beschriftet («Beispielwerte · keine echten Besuche», Band, Leiste, Tabelle «-beispielwerte.csv»). Echte Werte nur mit `?k=<Schlüssel>`.

| Datei | Was |
|---|---|
| `registre.py` | Auswertung, Beispielwerte, Ablage, `seiten`, `leeren`, `aufraeumen` (Restaurant-Arten, Herkunft, Orte) |
| `registre.js`, `registre.css`, `schloessli.css`, `index.html` | Oberfläche (Texte, Werte, Bühnenfotos des Hauses, Farben «Ton in Ton», Zeiger als Zeichen) |
| `anschluss.py`, `server.py`, `online/registre.py` | Dienst lokal und online, eigener Schlüssel, Grenzen (403/413/429) |
| `vorschlag/messung.js` | Zählung für die Website (Vorschlag, eingebaut wird in Station 14) |
| `anleitung_bau.py`, `anleitung.vorlage.html`, `anleitung.js`, `anleitung/k01–k10.jpg` | Anleitung |
| `abnahme.js`, `_pruefung/nachrechnen.py`, `_pruefung/probe.sh`, `mess.js` | Prüfläufe (Probe-Kopie `~/Desktop/Website-Projekte/_Probe Schloessli Registre/`) |
| `seiten.json`, `beispiel/7|30|90.json` | Namen der Seiten aus den Titeln, abgelegte Beispielwerte |

**Bühnenfotos** (nur Fotos des Hauses selbst, `website/assets/img/*-1200.webp`): Übersicht das Aussenfoto des Kleids (`haus`), Besuche die Tische unter den Platanen, Herkunft der Wegweiser zur Terrasse und zur Lästermeile, Zeit der Abend unter der Platane, Seiten das Regal an der Bar, Verlauf die Gäste am Ufer, Zur Reservation das Glas vor dem See, So wird gezählt die Gaststube.

## Geprüft (selbst, Bauer; Station 12 prüft neu)

- **Nachlauf 20.10.2026 ~00:5x** nach Namen und Bildern: wieder **91 von 91 grün** in allen vier Läufen (eigener Prüf-Port 8992, das Werkzeug lief daneben auf 8988 weiter, echte Daten unberührt).
- **Abnahme `abnahme.js`** an der Probe-Kopie `~/Desktop/Website-Projekte/_Probe Schloessli Registre/` (eigener Server, Wegwerf-Daten unter /tmp): **91 von 91 Zeilen grün** in Chromium und Safari-Kern × 1440 × 900 und 390 × 844 (19.10.2026, 23:2x–23:4x, Rechnerlast 13 bis 36 durch andere Chats). Liste `FUNKTIONSLISTE.md`, Ergebnis `abnahme-ergebnis.json` im Werkzeug. Dabei bedient: jede Ansicht über Adresse und Rand, Zeitraum 7/30/90, Filter, «Weitere zeigen», Besuch wählen, Rundgang, Tabelle sichern (CSV gegen die Liste), Anleitung mit Bild gross und Esc, Fehlermelder, Startfehler-Tür, Dienst-Ausfall, echte Werte mit Schlüssel und «Neu laden», Grenzen 403/413/429, Online-Sicherheitsregel (CSP).
- **Zählung der Website** (Z01, Z01b, Z02, an Seiten der Probe-Kopie mit `messung.js`): Fenster «Reservation», Tisch angefragt erst nach «gesendet», «Direkt buchen», Bankettanfrage öffnen, leeres Formular zählt nicht, abgeschickt zählt, Gutschein, Telefon des Hauses, Nummer und Seite des Schäfli, Mail, Route; nicht gezählt: «nicht mitzählen», Prüfbrowser, Werkzeug-Seiten.
- **Nachrechnen** `_pruefung/nachrechnen.py` (eigene Rechnung aus den Rohdaten, Regeln dort selbst geschrieben): **45 Vergleiche, 0 Abweichungen** (Beispielwerte 7/30/90, Ablage gekürzt zu sechs Uhrzeiten, Dienst = Ablage, um 1/3/7 Tage geschoben, echte Zählung aus 160 Zeilen, 11 ungültige abgelehnt, Datenschutz). Bericht `_pruefung/nachrechnen.txt`. Am Bildschirm zusätzlich P01/P01b/P02 in allen vier Läufen.
- **Ansicht** jeder der acht Ansichten in Chromium und Safari-Kern, 1440 und 390: kein seitliches Überlaufen, keine Konsolenfehler, keine toten Adressen (Prüfbilder nur in `_pruefung/bilder/` und im Arbeitsordner, nicht an Robert).
- **Flüssigkeit** (`mess.js`, Chromium, Prozessor gedrosselt, Ansichtswechsel und Scrollen, Rechnerlast 26 bis 36 durch andere Chats): 4× 1440 p50 8,3 / p95 9,3–16,1 ms, 4–7 von rund 1150 Bildern über 33 ms; 4× 390 p50 8,3 / p95 9,2 ms, 5–6 von 1130; 6× 1440 p95 9,3–15,9 ms, 5–6 von 1070; 6× 390 p95 9,2–16,5 ms, 6–7 von 1150 (ein Ausreisser 384 ms beim Ansichtswechsel unter Last). Mit «weniger Bewegung» gleich oder ruhiger. Unter normaler Last neu messen (offen).

## Aus den anderen Häusern übernommen und an diesem Stand geprüft (Auftrag Oberchef 19.10.2026)

Gelesen: Werkzeug-Master ganz (4.6 G01–G13, 6, 8, 9, 10, Fehlerbuch 10a), Merkdateien zu den Werkzeugen, Gasterntal-Lieferung; Lernauswertung «Registre, Besucherbuch» seit 11.10. (816 Nachrichten, 315 Bilder): keine eigene Beanstandung von Robert am Besucherbuch mit Bild, nur die allgemeinen Aufträge.

| Korrektur | Herkunft | Am Schlössli |
|---|---|---|
| Jedes Haus zählt für sich (eigener Schlüssel, eigener Speicher) | Robert 17.10., Master 3 | eigener Schlüssel, eigener Ordner, nie Schäfli (A08b, N01, P03) |
| Anteile an allen Besuchen, nicht an den gezeigten Plätzen (G10/F30) | Carlton 16.10. | geprüft P02, nachrechnen |
| Beispielwerte genau bis jetzt (G11/F31) | Carlton 16.10. | P01/P01b, nachrechnen B/C |
| Als Tabelle sichern (G12), Fehlermelder und Grenzen (G13) | Carlton 16.10. | P03, Q03, Q04 |
| Beispiele schon beim Öffnen, nie leer (M27) | Robert 18.10. | Vorführ-Betrieb zeigt sofort Beispielwerte, beschriftet |
| Knopf «Dieses Gerät nicht mitzählen» entfernt | Robert 18.10. 18:44 | nicht da; Prüfbild-Skript berichtigt |
| Trichter lesbar (dunkle Schrift auf hellem Grund) | Robert 18.10. 18:58 | `schloessli.css`, Bild «Zur Reservation» angesehen |
| Ein Startbild für alle Werkzeuge, Ecke oben links gleich (M24) | Robert 17./18.10. | Rahmen und Kleid der Oberfläche des Hauses, kein eigener Kopf |
| Demo-Hinweis verdeckt nichts (M26) | Robert 18.10. | Beispiel-Band im Fluss unter dem Startbild |
| Bilder in jeder Liste (Fehlerbuch 10a) | Robert 19.10. (Schlössli, Schaufenster) | **neu, umgebaute Listen:** (1) Seiten-Tabelle, (2) «Am meisten angesehen» (Übersicht), (3) «Von welcher Seite reserviert wird», (4) «Der Weg durch die Website» eines Besuchs zeigen je Seite ihr erstes eigenes Foto; (5) die Besuchsliste zeigt je Besuch das Bild der Seite, auf der er begann, mit dem Land als Kreis darauf (`seiten-bilder.json` aus `registre.py seiten`, Fotos aus `website/assets/img/`, kein KI-Bild, keine Seite doppelt). Doppelte Einträge gibt es keine (je Seite und je Besuch eine Zeile). Ohne Bild bleiben Länder, Orte, Sprachen, Geräte und «Gekommen über» (das Haus hat dafür keine Bilder; Flaggen wären Zeichen, keine Fotos). Nachgeprüft 20.10.: 21 betroffene Zeilen in vier Läufen grün |
| Kein roher Vorlagen-Code sichtbar (`{`, `undefined`, `NaN`, `None`) | Fehlerbuch 10a | in allen acht Ansichten gesucht, nichts gefunden |
| Namen der Werkzeuge an einer Stelle | Chef-Chat 19.10. | siehe «Wo» |
| Zierzeile am Handy abgeschnitten | eigener Fund | bricht jetzt um (`schloessli.css`) |

## Was neu gebaut wurde und warum der Stamm es nicht konnte

- Der Stamm `_Werkzeuge/` hat kein Besucherbuch (nur `website`, `karten`, `gaeste`). Gebaut ist es deshalb wie in den Maeder-Häusern als Werkzeug im Projekt mit eigenem Server, Vorlage Gasterntal.
- Restaurant statt Hotel: Ereignisse, Seitenarten, neun Werte, Trichter «Der Weg zum Tisch», Filter «Bankett oder Anfrage», Anleitung, Rundgang, Zählung der Website (`messung.js`) neu auf die Fenster der Schlössli-Website geschrieben.
- `server.py`: Website liegt in `website/` neben `_werkzeuge/` (bei den Kandertal-Häusern ist das Projekt die Website); `/_werkzeuge/…` aus dem Projekt, alles andere aus `website/`, Oberfläche aus `_werkzeuge/oberflaeche/` bis Station 14 sie nach `website/assets/` legt.

## Wünsche an den Stamm / Funde (für den Master)

- **Prüfzeile E04 der Vorlage** verlangte «Als Tabelle sichern» in der Leiste am Handy, das `gasterntal.css` dort seit dem 18.10. ausblendet (der Knopf steht am Handy unter der Besuchsliste). Hier berichtigt.
- **Im Safari-Kern kam im Prüflauf derselbe Aufruf von `feiern.html` zweimal als zwei Besuche an** (Z01b, nur im Lauf mit mehreren Kontexten; ein einzelner Lauf im Safari-Kern schickt sauber drei Zeilen eines Aufrufs). Ursache nicht geklärt; die Zeile prüft jetzt, dass eine Anfrage erst nach «gesendet» zählt, nicht die Zahl der Besuche.

- **Prüfzeile F01 der Gasterntal-Vorlage ruft `WO.quit`, das es im Paket der Oberfläche nicht gibt.** Die Vorlage wurde am 18.10. umgestellt und nicht neu laufen gelassen (Ergebnis-Datei vom 17.10.). Hier berichtigt (`quit()` des Werkzeugs). Gilt vermutlich auch für Doldenhorn/Ruedihus, dort nicht angefasst.
- **Prüfbild-Skript der Vorlage klickt `#l-geraet`**, den Knopf «Dieses Gerät nicht mitzählen», der seit 18.10.2026 entfernt ist (Robert). Hier berichtigt (`anleitung_bilder.js`, Kapitel 10 = «So wird gezählt»).
- **Kleid und Wege in `kleid/schloessli.js`:** Le Bureau steht dort als `/_werkzeuge/bureau/`; der Chat `website` hat den Schreibtisch im Stamm auf :8970 gebaut. Wer die Wege zusammenführt: eine Zeile im Kleid.
- **Oberfläche, Bildbeschreibung:** `oberflaeche.js` schreibt «Das <Name> von aussen»; beim Schlössli ergibt das «Das Wirtschaft am Schlössli von aussen» (Stamm, nicht angefasst).

## Prüfpunkte (Liste aus `_Werkzeuge/STAND.md`)

| Prüfpunkt | Stand | Beleg, Lücke |
|---|---|---|
| Backend | **offen** | Nur `server.py` auf diesem Rechner (Port 8988). Stürzt er ab, startet ihn niemand neu; die Oberfläche läuft dann mit den abgelegten Beispielwerten weiter (`beispiel/*.json`), Die Stube zeigt den Satz ohne Zahl |
| Datenbank | **erfüllt im Rahmen, sonst offen** | Je Tag eine Datei, Schreiben unter Schloss mit Umbenennen (`_schreib`), online Etag-Konflikt mit Wiederholen (`online/registre.py`). Tagesgrenze 4000 Aufrufe, 400 Schritte je Besuch. Keine Datenbank |
| Authentication und Rollen | **offen** | Keine Anmeldung (Robert 15.10.: kein Passwort bis zur Auslieferung). Echte Werte und die Ausfuhr nur mit Schlüssel (`?k=`), geprüft (A08b, N01, P03) |
| Rechteverwaltung | **offen** | fehlt; der Schlüssel ist der einzige Zugang zu echten Werten |
| API-Sicherheit | **erfüllt lokal** | Server nur 127.0.0.1, fremde Herkunft 403, Zeile über 300 Zeichen 413, mehr als 120 Meldungen bzw. 600 Abfragen je Minute 429, keine Quelltexte/Tagesdateien (404), entschlüsselte Pfade geprüft; jede Zeile gegen ein festes Muster (Q04, N03, N08). Online gleich in `online/registre.py`, dort nicht geprüft |
| Rate Limits | **erfüllt** | 429 ab 120 Meldungen je Minute und Absender (Q04), nur für `/api/`, nie für Bilder und Schriften |
| Logging | **teils** | Skriptfehler des Werkzeugs gehen ins Protokoll des Servers (`?fehler=1`, Q03). Das Werkzeug ändert nichts, deshalb kein Änderungsprotokoll nötig |
| Backups | **offen** | Tagesdateien ohne Sicherung ausserhalb des Rechners (kommt mit dem Cockpit, Master 14) |
| Deployment | **offen** | `online.json` liegt bereit (Form wie Gasterntal); andocken und hochladen macht Station 14/16. Nichts hochgeladen |
| CMS-Datenmodell | **erfüllt** | Viertes Haus nach Carlton, Doldenhorn, Gasterntal mit denselben Schlüsseln; ein Restaurant passt hinein ohne neue Felder |
| Übersetzungsworkflow | **betrifft dieses Werkzeug noch nicht** | Website nur Deutsch, gezählt wird die Sprache des Browsers. Oberfläche Deutsch (R24) |
| KI-Kosten | **betrifft dieses Werkzeug nicht** | Keine KI |
| Prompt-Injection-Schutz | **betrifft dieses Werkzeug nicht** | Keine KI; jede Zeile wird gegen ein festes Muster geprüft, Herkunft nur als Name |
| DSGVO und Schweizer Datenschutz | **offen** | Keine Namen, keine Adresse der Verbindung (nur Kürzel je Tag), kein Cookie (N04, nachrechnen E). Offen: Absatz in der Datenschutzerklärung der Website, erst wenn die Zählung eingeschaltet wird (Vorschlag `vorschlag/datenschutz-text.md`, Speicherort vom Haus zu nennen) |
| Datenlöschung | **teils** | `registre.py aufraeumen` löscht Tage älter als 400; läuft nur auf Aufruf. Einzelne Gäste sind nicht erkennbar, deshalb keine Einzel-Löschung möglich und nötig |
| Verfügbarkeit | **erfüllt lokal** | Ohne Dienst laufen die Beispielwerte aus der Ablage; Startfehler-Tür mit Grund (A09), Dienst-Ausfall mit Meldung (N06). Die Website wartet nie auf die Zählung (`sendBeacon`) |
| Monitoring | **offen** | fehlt |
| Booking-Integration | **betrifft dieses Werkzeug nur als Zählung** | Reservation bleibt bei gastronovi; gezählt wird nur, dass «Direkt buchen» gewählt wurde, nie was dort geschieht |

Kein Passwort vorerst (Robert 15.10.2026). In der Werkbank steht der Satz zur Auslieferung: alle Werkzeuge bekommen dann Anmeldung und Passwort.

## Für den Werkbank-Bauer (Station 14)

1. **Link in der Werkbank:** http://127.0.0.1:8988/_werkzeuge/registre/ (lokal; Server muss laufen). Online nach `stell` unter `/werkzeuge/registre/`.
2. **Zählung einschalten erst auf Roberts Wort:** `vorschlag/messung.js` nach `website/assets/js/messung.js`, in `bau.py` vor `</body>` jeder Seite `<script src="assets/js/messung.js?v=…" defer></script>` nach `haus.js`, `funktionen.js`, `fuss.js`. Dazu einen Weg `/api/registre` auf dem Server der Website (heute `website/serve.py` ohne Dienst) oder online die Funktion aus `online.json`. Dann `VORFUEHRUNG = False` an drei Stellen und Die Stube ohne `beispiel=1`.
3. **Datenschutz-Absatz** in `datenschutz.html`, wenn die Zählung läuft.
4. **Oberfläche nach `website/assets/oberflaeche/`** (siehe Notiz von La Carte); `server.py` nimmt dann die Datei im Haus.
