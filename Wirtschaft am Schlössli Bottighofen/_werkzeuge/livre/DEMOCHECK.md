---
tags: [projekt, website]
status: aktiv
---

# Demo-Check · Das Bildarchiv (Le Livre) · Wirtschaft am Schlössli · 21.10.2026

Unabhängiger Prüf-Chat (nie daran gebaut), Auftrag `_Oberchef/zeigen/schloessli/democheck/AUFTRAG.md`. Server `python3 _werkzeuge/livre/server.py 9102`, Markenprüfung nur mit Probe-Antwort (ohne `LIVRE_KI`). Bilder: `~/Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/livre/` (Chromium und Safari-Kern, 1440 und 390).

## Urteil

**Demo-bereit: ja.** Zwei Funde, beide repariert und nachgeprüft, ein Text verbessert.

## Was geprüft wurde, Weg für Weg

Zwei Läufe je Browser und Grösse: der Bedien-Durchlauf des Werkzeugs (`pruefung/bedienen.js`, 60 bis 62 Punkte) und ein eigener Lauf mit Bildern (`schau.js` im Scratchpad, 28 Punkte).

| Weg | Chromium 1440 | Chromium 390 | Safari-Kern 1440 | Safari-Kern 390 |
|---|---|---|---|---|
| Übersicht: Gruss, Zahlen 68 Fotos · 45 Dateien, vier Kacheln, jede Kachel führt hin | ok | ok | ok | ok |
| Rand: Fotos, Logo & Dateien, Markenprüfung, Übersicht; Handy «Bereiche» schliesst nach der Wahl | ok | ok | ok | ok |
| Alle Wege in Kopf, Rand, Leiste (Hafenbüro, Website ansehen, Anleitung, Markenbuch) antworten | ok | ok | ok | ok |
| «Alle Dateien (ZIP)» lädt (1,2 MB) | ok | ok | ok | ok |
| Fotos: 48 Kacheln, Nachladen bis 68, alle Vorschaubilder laden | ok | ok | ok | ok |
| Suche («terrasse»), Sonderzeichen, 5000 Zeichen, «Filter zurücksetzen» | ok | ok | ok | ok |
| Filter Bereich (9), Saison (2), Format (2), Herkunft (4), jeder trifft | ok | ok | ok | ok |
| Foto-Fenster: Titel, Quelle mit Weg zur Quelle, vier Grössen; Downloads 1080×1350, 1080×1920, 1500×2000, 2500×3333 nachgemessen | ok | ok | ok | ok |
| Rahmen ziehen ändert den Ausschnitt (nur Maus) | ok | – | ok | – |
| Zwei Wege in die Hausdruckerei mit Foto und Ausschnitt | ok | ok | ok | ok |
| Schliessen mit Esc, Kreuz, Klick daneben | ok | ok | ok | ok |
| Fremde Rechte: Kennzeichen und Hinweis · KI-Bild: Hinweis und Dateiname · Vorher/Nachher/Schieber | ok | ok | ok | ok |
| Logo & Dateien: 47 Dateien abrufbar, 8 Blöcke, Farbgruppen mit je eigenem Foto, Farbe antippen meldet «Kopiert» | ok | ok | ok | ok |
| Markenprüfung: falscher Dateityp abgewiesen, Beispiel-Entwurf geprüft, Ergebnis sichern, Als Text kopieren, Neuen Entwurf prüfen, Beispiel ansehen, Netz weg | ok | ok | ok | ok |
| Markenprüfung mit eigenem Flyer (Bild «Sommerabend am Hafen», 63 % in den Hausfarben) und eigenem Text-PDF («Grosse Party», 84 %): Ergebnis, überall «Probe» beschriftet, «Ergebnis sichern» als Datei | ok | ok | ok | ok |
| Neuladen bleibt in der Ansicht | ok | ok | ok | ok |
| Markenbuch: acht Kapitel Seite für Seite (Zeichen, Wortmarke, Schriften, Farben, Farbwelt, Logo richtig und falsch, Ton, eigene Welt), alle 32 Bilder, 22 Links, «Als PDF sichern» | ok | ok | ok | ok (nach Reparatur 1) |
| Logo richtig und falsch: Seite, Bilder, Weg zurück | ok | ok | ok | ok |
| Anleitung: neun Kapitel, Bilder, 11 Links | ok | ok | ok | ok |
| Rundgang (`?rundgang`, Prüfbrowser sehen ihn sonst absichtlich nicht): Schritte durchgeklickt, danach weg | ok | ok | ok | ok |
| «Zur Werkbank» nur aus der Werkbank geöffnet, Ziel antwortet; ohne Werkbank kein Knopf | ok | ok | ok | ok |
| Kein seitliches Verrutschen (alle Ansichten, Fenster, Buch, Anleitung) | ok | ok | ok | ok |
| Keine Konsolenfehler, keine toten Anfragen, keine Anfrage an fremde Adressen | ok | ok | ok | ok |

Chromium 390 im eigenen Bilderlauf: drei Wiederholungen brachen jeweils an einer anderen Stelle mit Zeitüberschreitung ab (Rechnerlast 137 bis 155 durch die parallelen Prüf-Chats); kein Fehler des Werkzeugs, alle Funktionen in derselben Grösse im Bedien-Durchlauf 60 von 60 grün, Bilder bis zum Markenbuch vorhanden.

**Inhalt:** Farben im Werkzeug gegen `website/assets/css/haus.css`: alle 12 Werte gleich (Nacht #0B1D3D … Schirmrot #FD9964). Schriften gleich (Open Sans, Instrument Sans, DM Mono, Caveat). Fremde Häuser: nur gewollte Treffer (Schäfli als Schwesterhaus, Fotos mit fremden Rechten Papageno, Excellence, Kitchen Party mit Quelle; Kommentare im Code). Kein mailto, kein tel. Markenprüfung antwortet ohne Schalter nur mit Probe, sichtbar beschriftet. Online: Claude nur, wenn am Vercel-Projekt ein Schlüssel gesetzt ist (`online/livre_online.py:22`), sonst Probe.

## Was repariert wurde

1. **«Als PDF sichern» im Markenbuch öffnete manchmal keinen Druck** (Safari-Kern 390 im Bedien-Durchlauf; nachgemessen 1 von 10 Mal, wenn man kurz nach dem Öffnen tippt). `buch.js` Zeile 5: das Warten auf die Fotos über `addEventListener(…, {once:true})` statt `i.onload = i.onerror = r`, das ein zweiter Aufruf überschrieb. Danach 35 von 35 Mal Druck (Safari-Kern 390, Chromium 1440, auch direkt beim Öffnen mit 31 offenen Bildern). Cache-Zusatz in `buch.html` auf `buch.js?v=8893785e0a` nachgezogen.
2. **Interne Dateipfade im Markenbuch, Kapitel Farben** («gemessen vom Späher · _kette/02-spaeher/befund.md», bei jeder Farbe «_quelle/website/bilder/…jpg»). Jetzt in Worten: «Foto der Website, Ausschnitt …», «Logo des Hauses», «Aufnahme der heutigen Seite», «Grund der heutigen Seite, gemessen». `buch.py` neue Funktion `ohne_internes()` (im Bau aufgerufen nach den anderen Weglassungen), dieselbe Ersetzung in `buch.html`. Prüflauf `pruefung/bedienen.js` Zeile 182 sucht jetzt auch `_quelle/`, `_kette/`, `_qa/`, «Späher».
3. **Anleitung, Kapitel 03:** «Zwei Wege führen direkt in der Hausdruckerei» → «Zwei Wege öffnen das Foto direkt in der Hausdruckerei». `anleitung_bau.py` Zeile 24 und `anleitung.html`.

Sicherungen: `*.vor-democheck-2026-10-21` neben `buch.js`, `buch.html`, `buch.py`, `anleitung.html`, `anleitung_bau.py`, `pruefung/bedienen.js`.

Fehlerbuch 10a (Werkzeug-Master): zwei Zeilen «Selbst gefunden im Demo-Check» (PDF-Knopf, Interna im Markenbuch).

## Messwert

Chromium 1440, Prozessor 4× gedrosselt, headless, gemessen bei Rechnerlast 131–149 (also eher zu schlecht als zu gut):

| Weg | Bilder/s im Mittel | langsamstes Bild | Bilder über 50 ms |
|---|---|---|---|
| Übersicht scrollen | 117 | 18 ms | 0 von 602 |
| Fotos scrollen (mit Nachladen) | 120 | 25 ms | 0 von 1505 |
| Logo & Dateien scrollen | 117 | 250 ms | 3 von 3541 |
| Foto öffnen und schliessen (3×) | 99 | 566 ms | 3 von 631 |
| Rand: vier Ansichten wechseln | 111 | 99 ms | 4 von 503 |
| Markenbuch scrollen | 93 | 292 ms | 4 von 477 |

Einzelne lange Bilder fallen auf das Öffnen grosser Fotos und das erste Bild einer Ansicht; Scrollen selbst läuft durchgehend flüssig.

## Nach dem Auftrag

- Gleicher Druck-Fehler steht noch in `buch.js` des Schäfli und des Ruedihus (nicht angefasst, an den Oberchef gemeldet).
- Markenbuch, Kapitel Schriften: Lauftext steht mit 17 px, Zeilenabstand 1,62, Etiketten 11,5 px / 0,17 em; die Website und «Logo & Dateien» sagen 18 px, 1,64 und 0,16 em. Auf den Stand der Website angleichen.
- Probe-Antwort: «63 % der Fläche» bricht am Handy zwischen Zahl und %, geschütztes Leerzeichen setzen (`livre.py` `_probe`, `livre.js` `p_rahmen`).
- Probe-Antwort beurteilt nur Farben: ein knalliger Party-Flyer auf weissem Grund bekommt «84 %, passt». In der Vorführung besser «Beispiel ansehen» zeigen oder die echte Prüfung einschalten (nur auf Roberts Wort).
- Markenbuch, Kapitel Farben, Platanenlaub: «Grün ist die Welt B des Schäfli» ist Arbeitssprache; in Worten des Hauses sagen.
- Nur Deutsch freigeschaltet (R24, Übersetzung erst Schritt 15a), Absicht.
