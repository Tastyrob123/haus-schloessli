# Lieferung: Der Gastgeber (La Réception) · Landgasthof Ruedihus (Bau-Chat, 17.10.2026)

Geliefert (Bau), Prüfung offen

Bauer: Bau-Chat «La Réception Ruedihus» (Auftrag Chef-Chat Ruedihus). Prüfen muss ein neuer Chat, der nie daran gebaut hat (Master Werkzeug-Bau Abschnitt 8).
Nichts hochgeladen, nichts an das Haus geschickt, an der Website nichts geändert, keine KI-Kosten, kein Schlüssel gelesen.

## Starten

- **Lokal:** aus dem Projektordner `python3 _werkzeuge/reception/server.py 9023` → http://localhost:9023/_werkzeuge/reception/
  Website mit Chat: http://localhost:9023/ · Zimmermappe: http://localhost:9023/mappe.html · Prüfseite: http://localhost:9023/_werkzeuge/reception/pruefung.html · Anleitung: http://localhost:9023/_werkzeuge/reception/anleitung.html
  **Ohne KI ist der Standard** (Regel 54): ohne `RECEPTION_KI=1` antworten Chat, Brief, Übersetzen und Wissen-Einlesen mit Probe-Antworten (sichtbar beschriftet). Mit `RECEPTION_KI=1` braucht der Server `ANTHROPIC_API_KEY` in der Umgebung; aus dem Vault liest er nie etwas. Echte KI nur in der Kostenrunde auf Roberts Wort.
  Daten: `_werkzeuge/reception/daten/` (oder `RECEPTION_DATEN=<ordner>`). Am echten Haus noch nie gestartet; alle Läufe an der Probe-Kopie.
- **Neu bauen** (nach neuen Seiten des Hauses oder einer neuen Fassung von Rivage, Carlton, Doldenhorn): `bash _werkzeuge/reception/_bau/alle.sh` — jeder Schritt bricht ab, wenn eine Ersetzung nicht genau trifft; danach `?v=` in `index.html` hochzählen.
- **Probe-Kopie:** `~/Desktop/Website-Projekte/_Probe Ruedihus Reception 1710/` (APFS-Klon, Wegwerf-Daten, `PROBE-LIESMICH.txt`; dort und nur dort ist das Anfrage-Fenster in 15 Seiten eingebunden). Prüfläufe dort: `bash _werkzeuge/reception/pruefung/alle.sh "chromium webkit" "1440x900 390x844"`, `bash _werkzeuge/reception/pruefung/sicherheit.sh`, Online nachgestellt `python3 _werkzeuge/reception/pruefung/online_probe.py 9033` + `node _werkzeuge/reception/pruefung/online_bedienen.js http://localhost:9033 webkit`, Messung `node _werkzeuge/reception/pruefung/messung.js http://localhost:9023/_werkzeuge/reception/ 6`.

## Wie gebaut

Gleiche Technik wie Doldenhorn und Carlton, Funktion wie Rivage. Skriptkette `_bau/alle.sh`: `portiere.py` (Oberfläche des Rivage, Farben auf Wandholz, Gelasio, Butzenscheiben) → `ruedihus.py` (Hauswerte, Arten, Fotos, Namen) → `brief.py` (Briefpapier und Mail im Kleid der Hausmails) → `pdf.py` (A4 vom Server, E16) → `server_teil.py` (`rezeption.py`/`gedaechtnis.py` des Rivage mit Ruedihus-Werten, `.gut`-Sicherung, Konflikt E21, Weg `formular` mit Abteilung, Seite, Formular) → `abnahme.py` (Prüfseite, R11, E17, E21, F47) → `eingang.py` (Abteilungen E15/E22) → `rahmen.py` (Rundgang, Zur Werkbank, Fehlermelder, PDF-Satz, Prüfseite, Anleitung aus dem Carlton) → `namen.py` (Namen der Welt Landhaus) → `gast_bau.py` (Chat am Rechner = dieselben Dateien wie online) → `beispiele_anfragen.py`, `beispiele_fragen.py` → `steckbrief_bau.py`.
Neu im Ruedihus: `baustein/anfrage.js`, `baustein/anfrage.css`, `baustein/ANLEITUNG.md` (Anfrage-Fenster der Website), `pruefung/formular_web.js`, `pruefung/messung.js`.

## Funktionen

`FUNKTIONEN.md`: **68 Funktionszeilen in 7 Gruppen** (A Rahmen 21 · B Übersicht 3 · C Eingang und Brief 21 · D Formulare der Website 6 · E Gefragt/Nachgetragen 4 · F Das weiss der Chat 5 · G Chat, Server, Daten 8), dazu H mit 3 beim Bau behobenen Funden; **68 von 68 bedient**, je mit Schritt-Beleg. Master-Zeilen: R01–R24, E01–E22 alle drin, dazu F35–F41, F46–F49 gelöst (F35/E17, F36, F37, F38, F39 aus dem Rivage-Stand, F41 im Rivage-Stand, F46/E21, F47, F48, F49).

## Prüfzahlen (Probe-Kopie, Wegwerf-Daten, ohne KI)

| | 1440 × 900 | 390 × 844 |
|---|---|---|
| Chromium | Gegenprobe 72/73 · Abnahme 18/18 · Formulare 13/13 (Nachlauf) | 72/73 · 18/18 · 13/13 |
| Safari-Kern (WebKit) | 72/73 · 18/18 · 13/13 | 72/73 · 18/18 · 13/13 |

- Rot in jeder Zeile genau Schritt 90: **Fund an der Website, nicht am Werkzeug** (Chat-Feld der Website einzeilig, Regel «Chat-Eingabe bricht um»; Quelle `Familie Maeder — Vier Häuser/gast_haeuser.py` / Carlton `assets/js/gast.js`, wie im Doldenhorn).
- Erste Matrix hatte zusätzlich rot: R01/R05, R18, 20, 42, 43, 50b, W01–W03, W11 — alles Prüfskript-Stellen mit Namen und Lücken des Doldenhorn bzw. Fehler im Skript (Adresse mit `#` vor `?probe=1`, verdeckter Knopf); Skripte berichtigt, danach grün.
- **Sicherheit** (`sicherheit.sh`): 14/14 (Host 421, Herkunft 403, Lesen von fremder Seite 403, 3 MB 413, kein JSON 415, 120 Änderungen 429, Formular ohne Herkunft 403, über 12 kB 413, Kontakt ungültig 422, Maschinenfeld ohne Eintrag, Antwort nur ok und Dank, 7. Formular in der Minute 429, ohne Schalter Probe und kein Schlüssel).
- **Online nachgestellt** (`online_probe.py` + `online_bedienen.js`): 12/12 in Chromium und Safari-Kern (Oberfläche unter `/werkzeuge/` und `/_werkzeuge/`, Formular der Website → Eingang, Brief, Gestaltung hält, PDF über das Druckfenster, Chat → «Das wurde gefragt», Prüfseite, ZIP, Herkunft 403). Nicht geprüft: echtes Vercel, echter Blob.
- **PDF:** Brief von Beat Ryser als A4, eine Seite, Dateiname «Landgasthof Ruedihus – Beat Ryser – 17.10.2026.pdf», angesehen.
- **Flüssigkeit gedrosselt** (Chromium, Netz 2 MB/s 150 ms, Rechnerlast 6,0–7,6): Öffnen 2,6 s (1×/4×/6×, Laptop und Handy; der ruhige Auftakt wartet auf die Bühnenfotos, höchstens 2,5 s, R02) · Wechsel zum Eingang 74 / 192 / 321 ms (Handy 4×/6×: 165 / 248 ms) · Rollen Bildzeit p95 9,6–10,3 ms · Verschieben beim Laden 0.
- **Steckbrief** 49 Zeilen, jeder Beleg wörtlich in den Seiten und Karten · **Beispiele** 9 Anfragen, 10 Fragen, jede Zahl gegen die Seiten geprüft, beide Lücken (Check-in, Kinderbett) geprüft, dass sie wirklich nirgends stehen (bricht sonst ab).
- Belege: Protokolle `pruefung/lauf/*.json`, Bildschirmfotos `pruefung/belege/` in der Probe-Kopie.
- Firefox, 1366 × 650 und 320 px **nicht** gelaufen (Auftrag: Chromium und Safari-Kern, 1440 und 390). Die Skripte können es: `alle.sh "firefox" "1366x650 320x640"`.

## Was am Haus anders ist

- **Name und Welt:** sichtbar «Der Gastgeber» (Welt Landhaus, `_Werkzeuge/stamm/welt.js`), Weg zurück «Die Stube» (lokal `../maison/`, online `/maison/`), Rundgang nennt Schreibtisch, Tafel, Werkstatt, Hausbuch, Besucherbuch. Dateien und Wege bleiben `reception`, `maison`. Schlüssel im Browser `rundgang-rh-…`, «Zur Werkbank» `rh-wb` (wie die Geschwister-Chats).
- **Kleid:** Kopf Wandholz `#321f10` mit Butzenscheiben (`assets/img/butzen-09.png`, 56 px), Raum Papier, Kacheln Holz, Gold `#b78f51`, Kerze `#c98543`, Licht `#f3cd94`, Geranie `#c42e13` nur als Punkt; Gelasio fett (Name in Versalien wie auf den Karten), Instrument Sans, DM Mono; Zeichen des Hauses in Gold (`zeichen-gold.svg/.png` aus `assets/logo/zeichen.svg`). Bühnen: Haus zur blauen Stunde, Stube bei Kerzenlicht, Ofestübli, Stube im Parterre, Giebel. Werte aus `assets/css/main.css` und `_werkbank/marke_werkbank.py`.
- **Brief:** Kleid der Hausmails (`mails/01-tisch` …): Kopf «LANDGASTHOF RUEDIHUS · Kandersteg · seit 1753», Fuss «Hinder de Büele 6 · 3718 Kandersteg · (+41) 033 675 81 81 · info@doldenhorn.ch» (Fuss der Seiten und Mails), Gruss «Herzlich, Familie Maeder und ihre Crew», Unterschrift «<Abteilung> · Landgasthof Ruedihus».
- **Mail-Vorlagen** je Art: Tisch, Fest, Sitzung, Nachricht → `mails/01-tisch`; Zimmer, Aufenthalt, Ausflug, Spa → `mails/02-anreise`; **Gutschein** (neue Art) → `mails/03-gutschein`.
- **Abteilungen:** Rezeption `info@`, Event `event@` (Fest-Rechner essen.html), Personal `jobs@` (Stellen haus.html). Kein Spa-Team: Spa liegt im Waldhotel Doldenhorn, Spa-Wünsche gehen an die Rezeption wie in der Hausmail.
- **Anfragen der Website:** Das Ruedihus hat kein `/api/anfragen` wie das Doldenhorn. Die Formulare der Website gehen über den Baustein direkt an den Weg `formular` des Gastgebers (E12 erweitert), mit Abteilung, Formular, Seite, Probe-Kennzeichen; eigene Grenze 6 je Minute, höchstens 12 kB, Kontakt geprüft, Antwort ohne Daten des Hauses.
- **KI:** Probe ist Standard, Schlüssel nur aus der Umgebung (Carlton/Doldenhorn lasen ihn aus dem Vault).
- **Beispiele:** 9 erfundene Anfragen (6 über Formulare der Website: Tisch, Fest-Rechner, Gutschein, Vor Ihrer Anreise, Ihre Abreise, Bewerbung; 3 aus dem Chat; Deutsch, Englisch, Französisch), 10 Fragen, alles als Beispiel beschriftet, Gäste mit example.com. «Vom Team nachgetragen» leer, «Beispiel ansehen» zeigt die echte Lücke «Ab wann kann ich am Anreisetag ins Zimmer?» mit Platzhalter (E10).

## Für den Werkbank-Chat (Übernahme)

1. **Anfrage-Fenster auf der Website** nach `baustein/ANLEITUNG.md`: `anfrage.js`/`anfrage.css` nach `assets/`, über `bau.py` in jede Seite (nach `dienste.js`/`seiten.js`), V hochzählen; Satz «Die Anfrage öffnet Ihr Mailprogramm.» in der Quelle ändern; lokal `POST /_werkzeuge/reception/api/formular` vom Hausserver :8917 an :9023 weiterreichen (oder Website über :9023 ansehen); `data-anfrage="gutschein"` an «Gutschein für ein bestimmtes Zimmer» und `data-anfrage="stelle"` an «Bewerben» (heute mailto). Datenschutz-Absatz zu den Formularen in `rechtliches.html` (Vorschlag in der Anleitung).
2. **Wege:** La Réception lokal `_werkzeuge/reception/` (Server :9023), online `/werkzeuge/reception/` (Umleitungen in `online.json`, auch `/_werkzeuge/reception/…`). Stand-Weg für die Stube: `GET /_werkzeuge/reception/api/ueberblick` (online `/werkzeuge/reception/api/ueberblick`) → `{anfragen_neu, anfragen_offen, ohne_antwort, fragen_gesamt, …}`. Anleitung `anleitung.html`, Prüfung `pruefung.html`. Bildschirme für Stube und Laptop: `bilder/schirm-uebersicht-1440x900.jpg`, `schirm-eingang-1440x900.jpg`, `schirm-uebersicht-390x844.jpg` (Safari-Kern, Beispieldaten).
3. **online.json** (`_werkzeuge/reception/online.json`): Funktionen `api/reception.py` (120 s) und `api/gast.py` (60 s, ersetzt den Chat von `gast_haeuser.py online`, Fragen und Chat-Anfragen in den Blob «reception», alte Ablage `/api/fragen` daneben, wenn `GAST_GEHEIM` gesetzt ist); lib mit Server-Teil, Beispielen, Steckbrief, Chat mit Wissen; statik ohne `daten/`. Voraussetzungen: `_werkzeuge/online/` des Ruedihus mit hausneutralem `api/_speicher.py` (F29: `/tmp/ruedihus-…`), `werkzeuge_online.py stell` im Hochladen, Blob-Speicher am Projekt, `vercel.json` für `api/gast.py` mit `includeFiles: api/_lib/**`, `ANTHROPIC_API_KEY` am Projekt erst in der Kostenrunde (sonst `RECEPTION_KI=0` am Projekt setzen, dann Probe-Antworten online).
4. **Mail-Vorlage am richtigen Ort (F76):** `online.json` legt `mails/01-tisch/index.html`, `02-anreise`, `03-gutschein` nach `api/mails/<nr>/index.html`; `reception.py` liest online `WEB = api/` → `api/mails/<nr>/index.html`. Passt (nachgestellt geprüft: O3/O4).
5. Nach dem Hochladen: `/werkzeuge/reception/` live bedienen (Formular auf essen.html → Eingang), Versand-Schutz und Hochlade-Sperre wie immer.

## Offene Fragen

1. **Name:** `welt.js` legt die Namen der Welt Landhaus fest («Der Gastgeber»), aber das Ruedihus ist dort nicht als Haus eingetragen (`_Werkzeuge/haeuser/` kennt nur gasterntal und beau-rivage). Gilt für das Ruedihus die Welt Landhaus? Die Geschwister-Chats (Stube, Tafel, Besucherbuch, Werkstatt) haben dieselbe Wahl getroffen.
2. **Gutschein als eigene Art** im Eingang (Mail «Ihr Gutschein ist da» als Vorlage): so lassen oder unter «Nachricht» führen?
3. Soll der Weg `formular` lokal am Hausserver :8917 hängen (Weiterleitung in `studio.py`), oder sieht das Haus die Website lokal künftig über :9023?

## Funde für andere (nicht hier behoben)

- **Website Ruedihus:** Chat-Feld einzeilig (Schritt 90, wie Doldenhorn). Datenschutz nennt die Formulare nicht. Vier Formulare öffneten das Mailprogramm (gegen [[feedback-anfragen-ins-fenster-nie-mailto]]); der Baustein löst es, sobald er eingebunden ist.
- **Zahl «speicher» in `ueberblick` lokal** zeigt einen Ordnerweg (aus dem Rivage-Code); harmlos am eigenen Rechner, online steht dort «Blob»/«Vorführung».

## Offen

1. Unabhängige Abnahme durch einen neuen Chat (Master 8), dazu Firefox, 1366 × 650, 320 px und die Prüfpunkte aus `_Werkzeuge/STAND.md`.
2. Echte KI nicht geprüft (Brief schreiben, Übersetzen, Wissen einlesen, Chat): erst in der Kostenrunde.
3. Online echt (Werkbank-Chat): Blob, `werkzeuge_online.py stell`, Hochladen, live bedienen.
4. Sicherheitsschicht `_wache.py` (Rollen, Anmeldung) fehlt wie überall; «Rolle ohne Recht 403» ist offen. Kein Passwort bis zur Auslieferung (Robert 15.10.).
5. Probe-Kopie `_Probe Ruedihus Reception 1710/` darf nach der Abnahme weg (nur auf Roberts Wort).
