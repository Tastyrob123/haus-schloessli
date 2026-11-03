---
tags: [projekt, website]
status: aktiv
---

# Lieferung Die Tafel (La Carte) · Berghotel Gasterntal (17.10.2026, Bau-Chat «Die Tafel», Port 8971)

**Status:** geliefert (Bau, Selbstprüfung auf Demo-Niveau). Die unabhängige Abnahme macht ein Prüf-Chat; Sicherheit, Rollen, Firefox und alle Grössen kommen nach dem Auftrag. Nichts hochgeladen, nichts gesendet, keine KI-Aufrufe. Im Projekt nur `_werkzeuge/carte/` geschrieben; Website, `inhalt.py`, `_werkbank/`, `werkbank/`, `serve.py` und die Ordner der anderen Werkzeuge unberührt. Probe-Kopie: `~/Desktop/Website-Projekte/_Probe Gasterntal Carte 1710/` (APFS-Klon, Wegwerf-Daten).

## Start

```
python3 _werkzeuge/carte/serve.py 8971
```
→ http://localhost:8971/_werkzeuge/carte/ · Prüfseite http://localhost:8971/_werkzeuge/carte/pruefung.html · Anleitung http://localhost:8971/_werkzeuge/carte/anleitung.html. Eigener Server, hört nur auf 127.0.0.1. Website und die anderen Werkzeuge verlinkt die Tafel lokal auf den Hausserver :8918 (Die Stube unter `/_werkzeuge/maison/`, Der Schreibtisch unter `/studio/`), online auf dieselbe Adresse. Daten sind eingelesen (`_daten/stand/karte-2026.json`); erneut einlesen überschreibt nie einen Stand des Hauses (`python3 _werkzeuge/carte/einlesen.py`, `--grund` nur den Ursprung).

Name in der Landhaus-Welt: **Die Tafel** (Kopf «Die Tafel · Karte · Berghotel Gasterntal»), Knöpfe «Die Stube» und «Der Schreibtisch». Dateien und Adressen bleiben `_werkzeuge/carte/`.

## Was es ist

Eine Karte: **Karte 2026 · Ässe u trinke** (2 Seiten A4: Getränke mit dem Deckel des Hauses, Speisen mit dem Kasten zum Jugendschutz). Einmal aus dem fertigen Satz der Werkbank eingelesen (`_werkbank/satz/u-karte-2026.html`, C17), nichts abgetippt:
- Rundlauf Daten → Satz: Zeichen für Zeichen gleich (37 857 Zeichen).
- Wortlaut gegen das Original `_quelle/website/pdf/Neue_Karte_Gasterntal_2026.pdf`: 756 Wörter im Original, 756 im Druck, «Wortlaut gleich» nach der Regel der Werkbank (berichtigte Stellen nur aus `satz_daten.py BERICHTIGT`, eingetragen in `_werkbank/unterlagen.json`).
- Preise: 103 im Original, 103 im Druck, jeder gleich (gezählt).
- Druck der Tafel gegen `unterlagen/pdf/karte-2026.pdf`: Text Zeichen für Zeichen, Seitenzahl und Seitenbilder gleich.

**Weitere Preislisten belegt das Haus nicht.** «Öpis chalts» (Picknick) ist eine Rubrik der Karte 2026. Die Sauna hat keine Preisliste (CHF 60.00 / 50.00 stehen als Text auf sauna.html, Sache des Schreibtischs). **Mittagsmenü (C08): betrifft nicht**, Belege: Seite «Restaurant» des Hauses nennt nur die Speisekarte (`_quelle/website/text/pages__restaurant.md`), Willkommensschreiben «RESTAURANT · Warme Speisen bis 2030h», daten.py ohne Mittagsmenü.

**Website und Druck bleiben getrennt:** die Website trägt den Wortlaut des Hauses (daten.py), der Druck die berichtigte Fassung. Die Tafel führt die Zeilen der Website nach, statt sie neu zu schreiben: eine Zeile bleibt Wort für Wort, bis ihr Eintrag geändert wird, dann geht nur das geänderte Stück mit (geprüft: Preis der Tagessuppe geändert, die Website-Zeile heisst weiter «Tagesssuppe»).

## Funktionsliste

`FUNKTIONSLISTE.md`: R01–R24 und C01–C23 mit den Zeilen der Vorlagen. **Bedient und grün:** jede Zeile mit Haken (✓) in einem Bedienlauf, der Online-Probe, der Anschluss-Probe, `pruefe.py` oder «Vorschau = PDF». **Ohne Bedienung:** R20 (keine leere Liste), R22 (kein Passwort, Robert 15.10.2026), R24 (Deutsch). **Betrifft nicht:** C08 Mittagsmenü, C19 Rolle Spa, Bildzeichen am Gericht (die Karte hat keine), je mit Prüfzeile oder Beleg.

## Kleid und was bewusst anders ist

- **Rahmen aus der Werkzeug-Oberfläche der Häuser** (`_Werkzeuge/stamm/oberflaeche/UMSTELLUNG.md`: «Die Werkzeuge des Gasterntal … entstehen direkt mit diesem Paket», Rahmen «Die Bühne», Kleid `gasterntal`): Kopf, Rand, Startbild und Leiste aus `oberflaeche.js`, gleiche Form wie die anderen Gasterntal-Werkzeuge sie bekommen; Arbeitsbereich (Liste, Vorschau, Gestalten) der der Tafel, wie UMSTELLUNG.md es für La Carte erlaubt. Eingebunden direkt aus dem Haus (`/assets/oberflaeche/…`, Zeilen laut UMSTELLUNG.md), keine eigene Kopie, das Paket unverändert; online unter statik `"assets/oberflaeche": "assets/oberflaeche"`.
- **Kleid des Gasterntal** (Werte aus `assets/css/main.css`): Kopf und Bühne in Schiefer der Talwand (#1d2224, #2c3136) mit der Lauben-Raute als Tapete, helles Balkonholz (#d6bb96) als Linie, Knauf und Akzent auf Dunkel, Tannengrün (#3b4423) als Akzent auf Hell, Raum in Papier (#e9ecec) mit der Raute bei 3 %, Rand weiss, das Rot der Fensterläden (#c5000f) nur als Marke «Entwurf». Titel in Barlow Semi Condensed, dazu Instrument Sans und DM Mono. Startbild mit dem Foto der Gaststube, Kachel aus demselben Foto. Gestalten mit den drei Schriften und elf Farben des Hauses. Nicht verwechselbar mit Doldenhorn (Nachtblau, Tannen, Caslon), Ruedihus (Wandholz, Butzen, Gelasio), Carlton (Navy, Baskerville) oder Rivage.
- **Rollen:** Küche und Service ändern die Karte und drucken Proben, veröffentlichen darf die Direktion (eine Karte, kein Tagesteller wie im Ruedihus, keine Spa-Karte wie im Doldenhorn). Kein Passwort.
- **Ansicht «Website»** mit drei Seiten zur Wahl: Ässe u trinke, Picknick, Startseite (die Karte steht auf allen dreien).
- **Anschluss** über zwei Bauten (C21) mit Zeilen-Abgleich in der Reihenfolge der Karte, jede Zuordnung an den Preisen geprüft (71 Zeilen, 17 Rubriken, Kennungen der Rubriken bleiben). Weicht eine Seite vom Bau ab, bekommt jede Seite mit Abschnitt id="karte" nur diesen Abschnitt (essen, picknick und index haben einen).
- **Verwerfen** steht in der Leiste als Knopf (in der Vorlage ein Textlink, der am Handy fehlte).
- **Handy, Fortgeschritten:** solange «Gestalten» unten als Platte offen ist, bekommt die Seite unten Luft, damit sich jedes Element über die Platte schieben lässt (ohne lag z. B. der Tomatesalat unter der Platte und liess sich nicht ziehen).

## Stand-Weg für Die Stube (Master 4.1)

`GET /_werkzeuge/carte/api/status` → `{karten:[{ziel:'karte-2026', name:'Karte 2026', unter, gruppe, entwurf, entwurf_zeit, pdf_zeit, stand_zeit, seiten, verlauf}], bau, einstellungen, rollen, rechte}` (lokal :8971, online dieselbe Adresse über `online.json` «stand»). `pdf_zeit` liest bis zur ersten Veröffentlichung die PDF unter `unterlagen/pdf/karte-2026.pdf` («10.10.2026 07:18»), danach die veröffentlichte. Antwort heute: eine Karte, `entwurf: false`.

## Bildschirmbilder

Safari-Kern, 1440 × 900 bei Pixeldichte 2, Wegwerf-Daten (`pruef/bilder.js`):
- `bilder/la-carte-1440.webp` — **Hauptbild 1440 × 900** für den Laptop der Werkbank und den Saal der Stube (Einfach: Startbild, Liste, Vorschau)
- `bilder/la-carte-liste-1440.webp` (Liste der Speisen), `bilder/la-carte-fortgeschritten-1440.webp` (Fortgeschritten), `bilder/la-carte-website-1440.webp` (Ansicht Website, Ässe u trinke), `bilder/la-carte-handy-390.webp` (Handy 390 × 844)
- Kachel der Karte: `kachel/stube.webp`.

## online.json

`_werkzeuge/carte/online.json`: Funktionen `api/carte.py` (aus `online/carte.py`, Ablage «carte» im privaten Blob, PDFs einzeln unter `carte/pdf/…`) und `api/carte_druck.js` (Chromium, nur mit Schlüssel aus dem Speicher-Schlüssel), lib (`carte.py`, `_daten/stand`, `_daten/grundstand`), statik (Oberfläche nach `werkzeuge/carte/`, `satz/`, `fonts/`, `kachel/`, `tafel.css`, dazu `assets/oberflaeche` → `assets/oberflaeche`), Umleitungen `/_werkzeuge/carte/api/*` → `/api/carte`, Stand-Weg, Prüfweg. Braucht die gemeinsame Speicher-Schicht `api/_speicher.py` und `_speicher.cjs` (im Gasterntal noch nicht da; die Probe nimmt die des Carlton, nur gelesen), PyMuPDF, `@sparticuz/chromium-min`, `playwright-core`, zwei Blob-Speicher. Online ist der Anschluss an die Website aus (Meldung ONLINE).

**Online-Fassung lokal nachgestellt** (`CARTE_PY=/usr/bin/python3 node _werkzeuge/carte/pruef/online_probe.js`, Blob als Ordner, ohne Vercel): **23 von 23** (Oberfläche über die Umleitung mit dem Rahmen aus `/assets/oberflaeche/`, Speichern in die Ablage, Probe-PDF über die Druck-Funktion, Veröffentlichen mit «PDF = Daten» über PyMuPDF, PDF aus dem Speicher, Status für die Stube, Verlauf, Zurückholen, Konflikt zweier Fenster 409, Herkunft 403, nur JSON 415, Grösse 413, Rollen 403, Programmcode 400, Anschluss online gesperrt, Druck ohne Schlüssel 403, Prüfseite).

## Anschluss an die Website (Patch für den Werkbank-Chat)

**Was die Tafel beim Veröffentlichen mit Anschluss tut** («Anschluss an die Website» im Rand unter «Wege», nur Direktion, Standard aus):
1. Die PDF geht an `unterlagen/pdf/karte-2026.pdf` und an die Adresse, auf die die Website verweist (`assets/pdf/Karte-2026.pdf`, oder was Der Schreibtisch unter `link.pdf` führt); die vorigen werden im Verlauf gesichert. **Hinweis:** heute liegt unter `assets/pdf/Karte-2026.pdf` die PDF des Hauses selbst; mit Anschluss wird sie beim ersten Veröffentlichen durch den Druck der Tafel ersetzt (berichtigte Fassung, gleicher Wortlaut wie `unterlagen/pdf/`).
2. Die Zeilen der Karte gehen nach `_daten/web/karte.json` (Format von `inhalt.py KARTE_STANDARD`), der Bau des Hauses setzt die Seiten in Wegwerf-Ordnern zweimal (`BG_ZIEL`), übernommen werden die Seiten, die sich ändern (essen.html, picknick.html, index.html), Nachprüfung Byte für Byte.

**Patch (einsetzen macht der Werkbank-Chat, nur auf Roberts Wort):** ein Block vor `inhalt.py karte_roh()` und eine geänderte Zeile darin, damit der Bau die veröffentlichten Zeilen nimmt (ohne Veröffentlichung bleibt alles, wie es ist; Modul nach Pfad geladen, Falle F10):
```
python3 _werkzeuge/carte/anschluss/patch_inhalt.py .            # zeigt den Unterschied
python3 _werkzeuge/carte/anschluss/patch_inhalt.py . --setzen   # setzt ein, Sicherung inhalt.py.vor-die-tafel
```
Der Unterschied steht in `anschluss/inhalt.diff`. Ohne Patch meldet die Tafel «Seiten: Anschluss im Bau fehlt», die PDF geht trotzdem.

**Für Der Schreibtisch:** die Karten-Stellen (Liste «karte», Stellen `k:speisen:…`, `k:getraenke:…`, `kr:…`) sperren mit Weg zur Tafel (Master 4.2 C). Ein eigener Stand des Schreibtischs in `inhalt/stand.json → karte` geht im Bau vor und würde die Tafel überdecken (heute leer). Notiz im gemeinsamen Ordner: `tafel-an-schreibtisch-und-werkbank.md`.

**Erprobt an einer APFS-Kopie** (`node _werkzeuge/carte/pruef/anschluss.js`, Projekt der Probe unberührt, Prüfsummen vor/nach gleich): **31 von 31**. Ausgangslage: der Bau ergibt heute dieselben 11 Seiten wie im Projekt; Bau mit Patch ohne Veröffentlichung Byte für Byte gleich; Chäsefondue 31.00, neues Gericht «Prüffondue Tal» in «Gäng guet», Tagessuppe 11.00 → PDF an beiden Adressen, essen.html mit allem, die Tagessuppe im Wortlaut des Hauses mit neuem Preis, index.html (Bildzeile und Auszug) folgt, nur essen.html und index.html neu, späterer Bau gleich; «Beleits Chäsbrot» ausgeblendet → fehlt auf essen.html und picknick.html; Ansicht «Website» zeigt essen.html und Startseite mit dem Entwurf, ohne die Seite zu ändern; Seite weicht ab → nur der Abschnitt «karte», Hand-Änderung bleibt, gemeldet; Ursprung zurückgeholt und veröffentlicht → alle Seiten Byte für Byte wie vorher, PDF-Text wie `unterlagen/pdf/`; ohne Patch: Meldung, PDF trotzdem.

## Prüfzahlen

Alles an der Probe-Kopie, Port 8971, Wegwerf-Daten, ohne KI, `mailto:`/`tel:` im Prüfbrowser abgefangen, nur headless. Vor dem Pitch: Chromium und Safari-Kern bei 1440 und 390 px (`pruef/demo.sh`).

| Prüfung | Ergebnis |
|---|---|
| Bedienlauf `pruef/lauf.js` Chromium 1440 × 900 | **128 von 128** |
| Bedienlauf Safari-Kern 1440 × 900 | **128 von 128** |
| Bedienlauf Chromium 390 × 844 | **126 von 126** |
| Bedienlauf Safari-Kern 390 × 844 | **126 von 126** |
| `pruefe.py alles` (Rundlauf, Wortlaut, Druck = PDF der Website) | GRÜN |
| Prüfbericht je Zeile und Lauf | `PRUEFUNG-2026-10-17.md` (aus `pruef/aus/`, `pruef/bericht.py`) |
| Vorschau = PDF (`gleich.js`) | Chromium grün (Seite 1 ohne, Seite 2 mit Gestaltung: mittlere Abweichung 2,9 / 2,7, starke 0,02 %); Safari-Kern grün mit einem Hinweis (bricht auf dem Deckel einzelne Zeilen anders um; die PDF druckt Chromium) |
| Online-Fassung auf dem Rechner (`online_probe.js`) | 23 von 23 |
| Anschluss an der APFS-Kopie (`anschluss.js`) | 31 von 31, Projekt unberührt |
| Zeilen aus dem Grundstand = `inhalt.KARTE_STANDARD` der Website | gleich |
| Flüssigkeit (`fluessig.js`) | **nicht gemessen:** Rechnerlast lag während des ganzen Baus zwischen 14 und 45 (andere Chats), gemessen wird nur unter 8 |

## Neue Funde (für den Master, überträgt der Chef-Chat)

- **Fund für Abschnitt 6 (Oberfläche, gilt für jedes Werkzeug mit `schweben.js`):** Knöpfe im Startbild der Oberfläche (`.wo-sb__kn > *`) dürfen nicht als «Kacheln» an `schweben.js` gehen. Das Startbild schneidet ab (`overflow:hidden`), `schweben.js` schiebt noch nicht sichtbare Stücke 80–140 px nach unten, dadurch liegen sie ausserhalb, der Beobachter meldet sie nie als sichtbar und sie bleiben für immer unsichtbar (im Chromium-Lauf zufällig, je nach Takt). Startbild selbst auftreten lassen, Knöpfe darin nicht an `schweben.js` geben.
- **Falle für Abschnitt 9:** zwei Website-Adressen, die sich nur in Gross/Klein unterscheiden (`unterlagen/pdf/karte-2026.pdf`, `assets/pdf/Karte-2026.pdf`), überschreiben sich beim Sichern mit `basename()` auf dem Mac (eine Sicherung statt zwei). Gasterntal: Sicherungsname mit Ordner (`carte.py _anschluss()`).
- **Falle Prüfskript:** in La Carte öffnet «Gestalten» beim Wählen und macht die Vorschau schmaler; vor dem Ziehen die Lage neu messen (sonst zieht der Lauf ein anderes Element, F21 sinngemäss). In `pruef/lauf.js` behoben.
- **Rahmen der Oberfläche am Handy:** «Entwurf verwerfen» als Textlink in der Leiste fehlt am Handy (die Leiste zeigt dort nur runde Knöpfe); als `WO.knopf` geführt.

## Offen

- **Unabhängige Abnahme** (Master 8) durch einen Prüf-Chat, der nie gebaut hat; vor dem Pitch der Demo-Check des Hauses.
- **Nach dem Auftrag:** Sicherheit und Rollen mit Anmeldung (Master 5.3, `_wache.py`), Firefox, 1366 × 650 und 320 px, Flüssigkeit gedrosselt (4×/6×) unter Rechnerlast 8 messen, echtes iPhone/iPad, Betrieb über Wochen.
- **Patch einsetzen und Anschluss einschalten** nur auf Roberts Wort (dann Schreibtisch-Sperre der Karten-Stellen).
- **Online:** gebaut, nicht hochgeladen; braucht die gemeinsame Speicher-Schicht im Gasterntal (`api/_speicher.py`, `_speicher.cjs`), zwei Blob-Speicher und PyMuPDF.
- **Die Stube:** Kachel der Tafel mit Stand-Weg `/_werkzeuge/carte/api/status` und dem Bild `bilder/la-carte-1440.webp`.
