---
tags: [projekt, website]
status: entwurf
---

# Das Schaufenster (Le Bureau) · Wirtschaft am Schlössli · Station 11, Teil `website`

Stand 19.10.2026, nachts, Werkzeug-Anpasser `website`. Bauer ist nie Prüfer: Station 12 prüft in einem neuen Chat.

## Wo

- **Werkzeug:** http://127.0.0.1:9035/_werkzeuge/bureau/ (eigener Server `_werkzeuge/bureau/serve.py 9035`, in diesem Chat gestartet, echte Daten unter `_Werkzeuge/daten/schloessli/website/`, erster Stand = die Website, wie sie gebaut ist). Weg in `kleid/schloessli.js`: `/_werkzeuge/bureau/` (stimmt).
- **Prüfseite:** http://127.0.0.1:9035/werkzeuge/website/pruefung.html?haus=schloessli
- **Stand-Weg für Das Hafenbüro (La Maison):** `GET /api/x/website/ueberblick/schloessli` am selben Server → `{aenderungen, zuletzt:{zeit}, bereiche, seiten}` (Form wie Le Bureau am Rivage).
- **Probe-Kopie:** `_Werkzeuge/werkzeuge/website/_probe/schloessli/` (`grundlage/` = gebaute Seiten, nie verändert; `online/` = was «online» wäre), aus `website/` des Projekts mit `probe.py schloessli --neu`. `website/` selbst wird nie beschrieben.
- **Name:** «Das Schaufenster» (Robert 19.10.: «passt»). Steht an einer Stelle: `_werkzeuge/oberflaeche/kleid/schloessli.js › namen` (eingetragen vom Chat «Schlössli · Das Kartenpult»). Kopf, Rand, Titel und Sätze nehmen ihn von dort; im Satz steht ein Werkzeug als «Das Kartenpult» in Anführung. Geprüft Chromium und Safari-Kern.

## Was gebaut ist

Das Schaufenster ist der Schreibtisch des Stamms (`_Werkzeuge/werkzeuge/website/`, Aufbau aus Le Bureau am Grand Beau-Rivage abgeleitet) **im gemeinsamen Rahmen des Schlössli** (`_werkzeuge/oberflaeche/`, Kleid `schloessli`, Rahmen «Die Bühne»): Kopf, Rand, Startbild, Leiste, Übersicht (Lage, «Häufig gebraucht», Bereiche als Fotokacheln) kommen aus `WO.*`, wie bei den anderen Werkzeugen des Hauses. Darin: Bereich mit Stellen links und Seite rechts (Klick in die Seite öffnet die Stelle, Foto tauschen gegen ein Foto der Website, Abschnitt ausblenden); Zeiten & Preise an einem Ort (dieselbe Angabe auf elf Seiten ist eine Zeile); Hinweis für Gäste; Entwurf & Vergleich; Frühere Fassungen; Leiste mit Vorher, nachher · Speichern (grau, gelb, grün) · Veröffentlichen; Quittung mit Rückgängig; Prüfseite mit Lexikon. Kein eigenes Kleid.

| Datei | Was |
|---|---|
| `_werkzeuge/bureau/serve.py` | eigener Server: Seite, `/assets/oberflaeche/` aus dem Rahmen, `/assets/` aus `website/assets/` (nur gelesen), sonst der Server des Stamms. Sicherheit: Host 421, Herkunft 403, Grösse 413, nur JSON 415, Grenze 900/60 je Minute 429 mit Retry-After, Kopfzeilen gegen Einbetten. Knöpfe zu den anderen Werkzeugen leiten zur Adresse aus der Kette (sonst Server des Hafenbüros 8987) |
| `_werkzeuge/bureau/index.html` | Seite: `kleid/schloessli.js`, Paket (grund, rahmen-buehne, kleid), dann `website.css`, `schweben.css`, `bureau.css`, Skripte `oberflaeche.js`, `website.js`, `schweben.js` |
| `_werkzeuge/bureau/bureau.css` | nur Brücke: die Werte der Arbeitsfläche (welt.css) zeigen auf die Werte des Kleids (`--wo-…`); Lage der Quittung im Rahmen |
| `_werkzeuge/bureau/schweben.js`, `schweben.css` | Kopie aus `_werkzeuge/carte/` des Hauses (R17): Blätter und Kacheln schweben nach der Uhr herein, «weniger Bewegung» steht still |
| `_Werkzeuge/werkzeuge/website/haeuser/schloessli.json` | Beschreibung: 11 Seiten, nur Deutsch, sieben Bereiche der Website mit Satz und Foto, Bereiche des Hauses «Anlässe» (5 Einträge, jede mit Foto) und «Team» (5), gesperrte Karten-Stellen |
| `_Werkzeuge/haeuser/schloessli/haus.json` | angelegt von einem anderen Anpasser (nur gelesen) |

**Gesperrt (gehört der Tafel):** Speisekarte nach Ländern, Wein zum Gang, Lunch, Lästermeile-Karte, Weinkarte samt Berater und Kopf, Bankettmenüs, die Auszüge davon auf der Startseite. In der Vorschau gepunktet umrandet, mit Weg zur Tafel; der Server lehnt Änderungen dort ab (423).

**Bereiche nach dem, was der Betrieb pflegt (Restaurant: Karte und Zeiten):** Karte → Die Tafel · Zeiten → «Zeiten & Preise» (14 Angaben, Öffnungs- und Küchenzeiten stehen je einmal für alle elf Seiten) · Anlässe (Plakate und nächster Anlass, ausblenden statt löschen) · Team. Zimmer, Preisstufen, Packages, Säle, Unterlagen, Stellen: aus (das Haus hat sie nicht).

## Was im Stamm-Werkzeug neu ist (für jedes Haus, abwärtskompatibel)

- **Rahmen eines Hauses:** lädt eine Seite das Werkzeug-Paket des Hauses (`kleid/<haus>.js` + `oberflaeche.js`), zeichnet `website.js` Kopf, Rand, Startbild («voll» mit Aussenfoto auf der Übersicht, «buehne» mit dem Foto des Bereichs sonst), Leiste und Übersicht mit `WO.*`; Namen über `wname()` aus `WO_HAUS.namen`. Ohne Paket bleibt alles wie im Stamm.
- `kopie.unter` in der Beschreibung (Quelle = Projektordner, Seiten im Unterordner).
- Stand-Weg `ueberblick` (La Maison), Foto je Bereich gross (`foto_gross`).
- Beispiele statt Leere (R20/M27) in «Entwurf & Vergleich» (drei echte Angaben der Website als «Vorher», beschriftet «Beispiel») und «Frühere Fassungen».
- Behoben: ein Bereich mit nur einer Seite schrieb «null» unter den Titel; Prüfseite jetzt mit fester Adresse `/werkzeuge/website/pruefung.html`.
- `nachbau.py <haus> [port]` (nach jedem neuen Seitenbau), `fluss.js` (gedrosselte Messung), `pruef.js` mit `PRUEF_PORT`, `MOTOR=webkit`, `PLAYWRIGHT_PFAD`, `RAHMEN=1 SERVER_SKRIPT=…` (Lauf im Rahmen des Hauses).
- Vorschau: `vorschau.zusatz_css` der Beschreibung für das Schlössli `.fenster{overflow:clip}` (Robert 19.10.: «mit Blick aufs» wurde beim Scrollen über das vorige Bild geschoben).

## Aus den anderen Häusern übernommen (Auftrag 19.10., geprüft am Schaufenster)

- Ein Rahmen und ein Startbild für alle Werkzeuge des Hauses (Master 3, UMSTELLUNG.md): Kopf, Rand, Startbild, Leiste aus dem Paket, Kleid nur aus `kleid/schloessli.css` (kein eigenes). Geprüft: Bildschirme 1440/390, Lauf im Rahmen bestanden.
- Ecke oben links gleich wie in allen Werkzeugen (M24): Zeichen im Ring, Name, «Website · Wirtschaft am Schlössli», aus `WO.kopf`.
- Weg zur Zentrale in jedem Werkzeug (Robert 15.10.): Haus-Knopf im Kopf führt über `serve.py` zum Hafenbüro (Adresse aus der Kette, sonst :8987). Geprüft: 302 auf :8987/_werkzeuge/maison/.
- Hell mit Bühne (R21): Kopf in der dunklen Hausfarbe, Raum hell, Rand weiss. Aus dem Paket.
- Speichern-Knopf grau, gelb, grün (R09) aus `WO.knopf` (glas/wartet/fertig). Im Lauf geprüft (`data-ws-lage`).
- Schweben nach der Uhr, nicht am Scrollen (R17, Robert 16.10.): `schweben.js/.css` aus La Carte des Hauses; «weniger Bewegung» steht still.
- Beispiele statt Leere in jeder Liste (M27, Robert 18.10. «alle Häuser alle Tools Beispiele»): Entwurf, Frühere Fassungen; Anlässe und Team sind echt gefüllt.
- Demo-Hinweis verdeckt nichts (M26): es gibt keinen schwebenden Hinweis.
- Sicherheit S01–S03 wie am Carlton (Host 421, Herkunft 403, Grösse 413, Grenze 429). Geprüft mit `curl`: 421, 403, 413, 429 nach 60 Schreibvorgängen.
- Auswahl im Hausstil (feste Regel): keine Auswahl des Betriebssystems, im Lauf je Ansicht geprüft.
- Nicht übernommen, weil es dem Werkzeug des Stamms fehlt: Anleitung, Rundgang, Angaben des Hauses, Google-Texte, Hochladen (offen).

## Geprüft (selbst, Bauer, 19.10.2026 nachts)

- **Im Rahmen des Hauses** (`RAHMEN=1 SERVER_SKRIPT=…/_werkzeuge/bureau/serve.py pruef.js schloessli land …`, Wegwerf-Daten, eigener Port 9042): Chromium 1440/390 **240 bestanden**, 320 **148 bestanden**; Safari-Kern 1440 bestanden, 390 **148 bestanden** (ein Lauf davor brach unter Rechnerlast 24 bei 390 einmal mit Zeitüberschreitung ab, Wiederholung grün). Öffnen, Text und Zeit ändern, speichern, neu laden, Konflikt zweier Fenster, Vorher/nachher, veröffentlichen, Kopie zeigt den neuen Stand, Verlauf, zurückholen, Seite wieder Byte für Byte alt, gesperrte Karte mit Weg zur Tafel, Prüfseite ohne Werkzeug, Startfehler-Tür, kein Überlauf, keine Auswahl des Betriebssystems, keine Konsolenfehler.
- **Gegenprobe Stamm** (alter Weg ohne Rahmen): schloessli und gasterntal 1440 **304 bestanden**.
- **Flüssigkeit** (`fluss.js`, Chromium, Rechnerlast 20,4, Werte in `fluss.json`): Öffnen bis die Übersicht steht 102 / 220 / 334 ms (1× / 4× / 6×) · Scrollen Bildabstand p95 9,1 / 9,2 / 8,9 ms, längster 9,4 ms · Bereich öffnen, Liste 54 / 132 / 208 ms, Seite in der Vorschau 119 / 240 / 316 ms · Zeiten & Preise 133 / 327 / 549 ms.
- Vorschau-Fehler aus Roberts Bildschirmfoto: in Chromium und Safari-Kern beim Scrollen über #fenster-hafen nachgestellt, nach der Abhilfe kein fremder Satz mehr.
- `unterbau/pruefe.py`: BESTANDEN.

## Prüfpunkte (Liste aus `_Werkzeuge/STAND.md`)

| Prüfpunkt | Stand | Beleg, Lücke |
|---|---|---|
| Backend | **offen** | Nur `_werkzeuge/bureau/serve.py` auf diesem Rechner (Port 9035). Stürzt er ab, startet ihn niemand neu; verloren geht nichts, das Werkzeug hält keinen Stand im Prozess |
| Datenbank | **erfüllt im Rahmen des Stamms, sonst offen** | Schicht je Haus im Speicher, Konflikt 409 statt Überschreiben (im Lauf geprüft). Keine Datenbank, keine Grenze für Verlauf und Protokoll |
| Authentication und Rollen | **offen** | Keine Anmeldung (Robert 15.10.: kein Passwort bis zur Auslieferung). `wer` ist ein frei eingetragener Name |
| Rechteverwaltung | **offen** | fehlt |
| API-Sicherheit | **erfüllt lokal, Rollen offen** | Jede Eingabe geprüft (Seite, Stelle, gesperrte Stellen 423, Text gesäubert, im Lauf geprüft). Server nur auf 127.0.0.1, fremder Host 421, fremde Herkunft 403, über 3 MB 413, nur JSON 415, Kopfzeilen gegen Einbetten (mit curl geprüft). Offen: Rollen, Anmeldung |
| Rate Limits | **erfüllt lokal** | 900 Abfragen / 60 Schreibvorgänge je Absender und Minute, danach 429 mit Retry-After (`_werkzeuge/bureau/serve.py`, mit curl geprüft) |
| Logging | **erfüllt lokal** | Protokoll des Speichers (wer, wann, was), sichtbar unter «Frühere Fassungen»; Fehler im Browser, die Prüfseite liest sie |
| Backups | **teils** | Jeder veröffentlichte Stand im Verlauf, zurückholbar (im Lauf: danach Byte für Byte wie gebaut). Keine Kopie ausserhalb des Rechners |
| Deployment | **für die Kopie erfüllt, für die echte Website offen** | Veröffentlichen schreibt nach `_probe/schloessli/online/` (prüft vorher jede Stelle, 422 sonst). Kein Weg zur echten Website des Hauses (Station 16) |
| CMS-Datenmodell | **erfüllt** | Drittes Haus ohne Umbau, nur Beschreibung; Restaurant statt Hotel, eigene Bereiche (Anlässe, Team) mit freien Schlüsseln. Grenze: nur fertig gebaute Seiten, keine neuen Einträge |
| Übersetzungsworkflow | **betrifft dieses Haus noch nicht** | Website nur Deutsch. Sprachen kommen mit Station 15a; das Werkzeug kann sie (am Beau-Rivage geprüft), dann `sprachen` in der Beschreibung setzen |
| KI-Kosten | **betrifft dieses Werkzeug nicht** | Keine KI |
| Prompt-Injection-Schutz | **betrifft dieses Werkzeug nicht** | Keine KI; Eingaben werden gesäubert |
| DSGVO und Schweizer Datenschutz | **offen, kleiner Umfang** | Keine Gästedaten. Es entstehen: der Name im Protokoll und im Browser, die gewählte Welt, Fehlerliste im Browser |
| Datenlöschung | **offen** | Verlauf und Protokoll wachsen ohne Grenze; löschen lässt sich nur der Entwurf |
| Verfügbarkeit | **teils** | Die Website hängt nicht am Werkzeug. Steht der Server: «antwortet nicht» mit Tür zur Prüfung (im Lauf geprüft) |
| Monitoring | **offen** | Die Prüfseite prüft nur, wenn jemand sie öffnet |
| Booking-Integration | **betrifft dieses Werkzeug nicht** | Reservation bleibt bei Gastronovi (Adresse ist ein Link der Seite) |
| Quelle in Bewegung | **teils** | `nachbau.py schloessli` holt neue Seiten und legt den veröffentlichten Stand wieder darüber; die Prüfseite nennt Änderungen ohne Platz. Läuft nicht selbsttätig (Anschluss-Zeile unten) |

Kein Passwort vorerst (Robert 15.10.2026). In der Werkbank steht der Satz zur Auslieferung: alle Werkzeuge bekommen dann Anmeldung und Passwort.

## Für den Werkbank-Bauer (Station 14)

1. **Link in der Werkbank:** `http://127.0.0.1:9035/_werkzeuge/bureau/` (lokal; Server `python3 _werkzeuge/bureau/serve.py 9035` im Projektordner). Online gibt es das Werkzeug noch nicht; in der Demo «Veröffentlichen» aus, nur ansehen (Robert 17.10.).
2. **Anschluss-Zeile im Seitenbau** (nicht eingesetzt, `website/` gehört Station 14): am Ende von `website/bau.py`, damit ein neuer Bau die Änderungen des Hauses nicht verliert:
   `subprocess.run(['python3', os.path.expanduser('~/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/nachbau.py'), 'schloessli', '9035'])`
3. **Stand-Weg für das Hafenbüro:** `/api/x/website/ueberblick/schloessli` am Server 9035 (Hafenbüro ist benachrichtigt).
4. **Rahmen:** legt Station 14 `_werkzeuge/oberflaeche/` nach `website/assets/oberflaeche/`, bleibt die Seite gleich (sie lädt `/assets/oberflaeche/…`); `serve.py` liefert dann weiter aus `_werkzeuge/oberflaeche/` und muss auf `website/assets/oberflaeche/` umgestellt werden (eine Zeile `OBERFLAECHE`).
5. **Website-Fund** `.fenster{overflow:clip}`: vom Website-Chat am 19.10. in `website/assets/css/haus.css` eingesetzt und geprüft; Kopie im Schaufenster mit `nachbau.py` erneuert.

## Offen

Siehe `stand.json` (über `kette.py offen`). Kurz: Funktionen des Katalogs, die das Werkzeug des Stamms nicht hat (Angaben des Hauses, Google-Texte, eigenes Foto hochladen, Anleitung, Rundgang, Fehlermelder an den Server, S01–S03), Sicherheit nach aussen, Anschluss-Zeile, Widerspruch Markenbuch/Website bei den Farben, Fuss mit Öffnungszeiten des Schäfli unter «Zeiten & Preise» ohne Hausnamen.

## Verlauf

- **20.10.2026, 00:3x** · Robert (Bild: Foto tauschen, Streifen übereinander): «Was ist das für eine unübersichtliche Weise …». Auswahl als Raster ganzer Kacheln 4:3 (150 px, am Handy zwei Spalten) mit Beschreibung darunter, Fenster bis 1060 px breit; gemessen: keine Überlappung, 75 Fotos, Chromium und Safari-Kern, 1440 und 390. Lauf im Rahmen Chromium 240 bestanden, Safari-Kern 240 bestanden (390 bricht unter Rechnerlast über 20 etwa jedes zweite Mal beim Wechsel aus der Übersicht ab; Wiederholung grün; Knopf «Bereiche» behält jetzt seinen Zustand nach dem Neuzeichnen), Gasterntal 158 bestanden.

- **20.10.2026, 00:1x** · Robert: «wenn das nur so paar sind, dann mach 3 oben und 2 unten». Bildkarten gleichmässig auf Reihen verteilt (höchstens vier je Reihe, letzte Reihe mittig): Anlässe und Team 3 + 2, Handy eine Spalte. Lauf im Rahmen Chromium 1440/390 bestanden, Safari-Kern 1440 und 390 bestanden (390 einmal unter Rechnerlast 22 mit Zeitüberschreitung, Wiederholung 148 bestanden), Gasterntal 158 bestanden.

- **20.10.2026** · Robert (Bild: Fusszeile der Website): Listen als freistehende Bildkarten, Text darunter. Anlässe und Team stehen im Raster (4 je Reihe am Rechner, 2 am Handy), Foto 4:3 frei, darunter Datum bzw. Aufgabe in Versalien, Name, «Ändern»; geöffnet über die ganze Breite. Lauf im Rahmen Chromium 1440/390/320 332 bestanden, Safari-Kern 1440/390 240 bestanden, Gasterntal 158 bestanden.

- **20.10.2026, früh** · Robert (Bildschirmfoto Anlässe, sechs Zeilen ohne Bild, Kreuzfahrt doppelt): «in allen Tools Bilder dazu». Jeder Eintrag der Listen (Anlässe, Team) zeigt sein Foto von der Website (Ausschnitt eher oben, damit Gesichter ganz bleiben), ohne Foto ruhige Anfangsbuchstaben (Marco Reisinger, Ole Sass: auf der Website ohne Foto), dazu die zweite Angabe (Datum, Aufgabe). Die grosse Ankündigung der Kreuzfahrt ist mit ihrem Plakat ein Eintrag (Felder «Grosse Ankündigung · …», `quelle.dazu`). Website-Bereiche hatten schon Fotokacheln. Geprüft Chromium und Safari-Kern, 1440 und 390; Lauf im Rahmen 240 bestanden, Gasterntal 158 bestanden.

- **19.10.2026, 23:3x** · Robert (Bildschirmfoto): «wenn ich was anklicke zum Verändern, dass es links ein bisschen besser angezeigt wird und ein bisschen kurz aufleuchtet … und ein bisschen höher sitzt». Die geöffnete Stelle rückt in der Liste unter die Suche (Handy: unter den Kopf), Zeile und Feld leuchten 1,5 s auf (nur opacity), beide tragen eine Leiste in der Akzentfarbe. Geprüft Chromium und Safari-Kern, 1440 und 390, Lauf im Rahmen 240 bestanden.

- **19.10.2026, nachts** · Auf den gemeinsamen Rahmen des Schlössli umgestellt (eigener Ordner `_werkzeuge/bureau/` mit Server und Sicherheitsschicht, Paket statt eigenem Kleid; das eigene Kleid in `_Werkzeuge/haeuser/schloessli/` ist entfernt), Name «Das Schaufenster», Schweben, Korrekturen aus den anderen Häusern, Fenster-Fehler der Vorschau behoben. Prüfläufe oben.

- **19.10.2026, abends** · Schlössli als drittes Haus angeschlossen, Kleid des Hauses, Stand-Weg, Beispiele statt Leere, Fehler «null» behoben. Prüfläufe siehe oben.
