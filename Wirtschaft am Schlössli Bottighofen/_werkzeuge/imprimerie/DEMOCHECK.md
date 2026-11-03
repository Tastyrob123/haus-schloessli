---
tags: [projekt, website]
status: aktiv
---

# Die Hausdruckerei (L’Imprimerie) · Wirtschaft am Schlössli · Demo-Check 21.10.2026

Unabhängiger Demo-Check-Chat (nie daran gebaut), Auftrag `_Oberchef/zeigen/schloessli/democheck/AUFTRAG.md`. Prüfserver `python3 serve.py 9053` → http://127.0.0.1:9053/_werkzeuge/imprimerie/ (so verlinkt die Werkbank), KI aus (Probe-Antwort, kostet nichts).

**Urteil: demo-bereit — ja.** 15 Funde, alle repariert und nachgeprüft (der Satz zum Schwesterhaus nach Antwort des Oberchefs). Dazu auf Auftrag des Oberchefs der Rückweg «Zur Werkbank» für alle sieben Werkzeuge (unten).

Bilder (1440 Chrome + 390 Safari je Hauptansicht, dazu Vorher/Nachher der Reparaturen): `~/Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/imprimerie/`

## Was geprüft wurde (Weg für Weg)

Chromium und WebKit (Safari-Kern), je 1440 × 900 und 390 × 844 (Handy mit Tippen). Zusätzlich 1366 × 650 für die Führung und 320 px für den Handy-Kopf.

1. **Funktionsliste des Werkzeugs** (`_qa/funktionen.js`, 106 Schritte: Laden, Übersicht, Seitenleiste, Anlässe, Abteilungen, Hinweise, Newsletter, Meine Medien und Freigabe, Arten und Vorlagen mit Galerie und Filtern, Fotos, Le Livre und Marke, Editor mit allen Aufbauten, Gründen, Tapeten, 10 Formaten, Rückseite, Elementen, Zoom, Druckprüfung, PDF/PDF mit Marken/PNG/Arbeitsdatei, Verwerfen, Sichern): Chrome 1440 106/106, Safari 1440 106/106, Chrome 390 103/105, Safari 390 103/105. Die zwei Abweichungen am Handy sind die gewollte einspaltige Anordnung (Prüfskript erwartet Laptop-Mosaik), mit dem Auge nachgesehen.
2. **Eigener Prüfgang** (`_qa/democheck_gang.js`, je Browser und Grösse): Begrüssung, Führung mit Filmen (Schritt 1 und 4), Hilfe-Menü, Demo-Video, alle 11 Bereiche der Seitenleiste (am Handy über «Bereiche», schliesst nach der Wahl), je Bereich ganz durchgescrollt: keine kaputten Bilder, kein seitliches Verrutschen, kein roher Code, kein fremdes Haus. Fünf Entwürfe aus einem Satz (Probe), Entwurf wählen, Titel auf dem Blatt ändern (Doppelklick bzw. Feld «Inhalt» am Handy), Format quer und zurück, Druckprüfung, PDF und PNG speichern und ansehen, Speichern → neu laden → noch da, Meine Medien, Instagram-Beitrag mit Handy-Vorschau und Bildtext, Newsletter-Baukasten (mail.html), Prüfseite, alle Links der Startseite per Abruf. Ergebnis zuletzt: Chrome 1440 30/31, Safari 1440 30/31, Chrome 390 47/48, Safari 390 47/48; die eine offene Zeile ist überall der Satz zum Schwesterhaus (unten).
3. **Alle 248 Vorlagen**: per Skript ohne fremde Häuser, ohne Preise, ohne erfundene Zahlen, Platzhalter nur gewollt in [Klammern] ([Datum] 30×, [Uhrzeit] 16× …). Druckprüfung über alle 505 Fälle (Vorlagen mit Rückseiten, Katalog, Newsletter-Bilder): 0 Seitenfehler, 23 Meldungen nur zur Auflösung einzelner Website-Fotos auf grossen Formaten (siehe «Nach dem Auftrag»).
4. **Ausgaben angesehen**: PDF (A5, 3 mm Beschnitt, Open Sans, Instrument Sans, DM Mono eingebettet, Logo des Schlössli, Adresse Seestrasse 50 · 8598 Bottighofen · +41 71 688 90 92), PNG gleich, Karten-PDF aus Meine Medien. Kein abgeschnittener Text, richtige Schrift.
5. **Nichts geht raus**: kein mailto/tel öffnet etwas (Klicks in der Mail-Vorschau werden abgefangen, in jedem Lauf zusätzlich abgefangen und gezählt: 0), kein Formular an das Haus, KI nur Probe-Antwort mit sichtbarem Hinweis «Beispiel: gewählt wurde die passendste fertige Vorlage … Mit eingeschalteter KI schreibt das Studio die Texte», Bildtext «Probe ohne KI». Keine Konsolenfehler, keine Antwort ≥ 400.
6. **Zur Werkbank**: mit Herkunft (`?wb=de.werkzeuge&wbo=http://localhost:8982`) erscheint der Knopf und führt auf die Werkbank (200).

## Was repariert wurde

Vor jedem Schreiben Sicherung `*.vor-democheck-2026-10-21`.

| # | Fund | Datei | Nachgeprüft |
|---|---|---|---|
| 1 | Führung und Demo-Video ohne Filme (`hilfe/` leer: leere Filmrahmen, «Das Video konnte nicht geladen werden») | `hilfe/` neu: 11 Führungsfilme + Demo-Video 90 s mit Kapiteln, aufgenommen am Schlössli-Werkzeug mit Probe-Antwort (Flyer «Banketts & Gruppen», «Feiern am Hafen»); Skripte `_qa/schritt_filme.js`, `_qa/demo_film.js` (Vorlage aus `_Drucksachen-Studio`, angepasst) | jedes Bild der Filme angesehen; Video lädt in Chrome und Safari |
| 2 | Weg «Das Hafenbüro» → 404 (localhost:8982/_werkzeuge/maison/), Fund des Hafenbüro-Chats | `haeuser/schloessli/buehne.js` Z. 12 → 127.0.0.1:8987 | 200 |
| 3 | «Das Bildarchiv öffnen» → 404 (localhost:8982/_werkzeuge/livre/) | `satz.js` Z. 83 → 127.0.0.1:9049 | 200 |
| 4 | «Zur Werkbank» hätte auf :9053/werkbank/ (404) gezeigt | `index.html` Z. 300 (auf :9053 als fremde Adresse) | Ziel localhost:8982/werkbank/ 200 |
| 5 | Fotoauswahl zeigte Fremd- und KI-Fotos aus dem Hausbuch (Tripadvisor, Guide Michelin, Excellence, KI-Feuerwerk), obwohl `marke.json → raus` sie ausschliesst (Fehlerbuch Schäfli 21.10.) | `satz.js` Z. 42 | 42 Fotos, keine aus `raus`, keines mit KI |
| 6 | «im Stil des Wirtschaft am Schlössli» (Begrüssung, Entwerfen) | `fuehrung.js` Z. 44, `index.html` Z. 78 | «der Wirtschaft» |
| 7 | Seitenleiste: «Übersicht» dunkle Taste mit fast unsichtbarer dunkler Schrift, sobald ein anderer Bereich offen ist | `haeuser/schloessli/oberflaeche.css` | hell lesbar |
| 8 | Anlässe: Monat mit einem Anlass, Foto deckte Titel und Text zu | `haeuser/schloessli/oberflaeche.css` (`.ev-raster .wo--breit .wo__k`) | Bild `anlaesse-ein-anlass-repariert…` |
| 9 | Probe-Entwürfe hiessen «… Nebel», «… Talwand» (Kandertal) | `serve.py` `probe()` → Stuhlblau / Seespiegel | Antwort geprüft |
| 10 | Probe: «Flyer» im Satz ergab ein A3-Plakat | `serve.py` `probe()` (Art im Auftrag geht vor) | «Banketts & Gruppen, Flyer» A5 |
| 11 | Marke des Hauses: zwei kaputte Bilder (Farben .css, Schriften .zip als Bild) und Kacheln «zeiger», «name» klein | `start.js` Z. 625 | keine kaputten Bilder, «Zeiger», «Name» |
| 12 | Prüfseite meldete «Druckfassungen nicht erreichbar» (Haus druckt absichtlich aus dem Bildarchiv) | `pruefung.html` Z. 76 | klarer Satz |
| 13 | Editor-Kopf: Name «Banketts & Gr» mitten im Wort abgeschnitten | `haeuser/schloessli/oberflaeche.css` | «Banketts & …» |
| 14 | Handy: leerer Kreis statt Zeichen, «Neu» halb aus dem Bild, «Zurück zur Drucksache» leerer Kreis, Leiste unter dem Blatt in fünf Zeilen mit abgeschnittenem Plus, 320 px Plus abgeschnitten | `haeuser/schloessli/oberflaeche.css` (Ende der Datei, vier Blöcke) | 390 und 320 px, Chrome und Safari |

Server :9053 nach den Änderungen an `serve.py` neu gestartet. Alle Regeln, die für jedes Haus gelten, stehen im Fehlerbuch 10a des Werkzeug-Masters (Zeilen 21.10.2026 «Wirtschaft am Schlössli (Demo-Check, gilt für alle Häuser mit L’Imprimerie)»).

## Messwert (CPU 4× gedrosselt, Chromium, fertiger Stand)

Start bis bereit 0,9–1,4 s. Bildwechsel (Bereich wechseln, Vorlage öffnen, Format wechseln): Median 8,3 ms, p95 9,2 ms (120 Bilder/s). Scrollen der Bereiche: Median 8,3–8,4 ms, p95 9–26 ms; einzelne Aussetzer 100–350 ms beim ersten Laden der Fotos. Der Rechner lief während der Messung mit Last 48–60 (viele Chats parallel), die Einzelaussetzer schwankten von Lauf zu Lauf. Rohwerte: `_qa/democheck_fluss.js`.

## Satz zum Schwesterhaus (Antwort Oberchef 21.10.2026)

In «Marke des Hauses → Regeln» (und im Hausbuch-Fach des Editors) stand sichtbar «Kein Hotel, keine Zimmer. Das Schwesterhaus (Taverne zum Schäfli) kommt in keiner Drucksache vor.» Der Oberchef: ganz aus der Ansicht, die Regel bleibt intern. Gebaut: `DS.regelSichtbar()` in `satz.js` nimmt den Teil ab «Kein Hotel» aus der Anzeige, `start.js` Z. 634 und `studio.js` Z. 802 zeigen nur diese Fassung; `marke.json` (und damit die KI) unverändert. Nachgeprüft: kein «Schäfli» mehr auf der Seite.

## Rückweg «Zur Werkbank» in allen sieben Werkzeugen (Auftrag Oberchef 21.10.2026)

Vorher: Aus der Werkbank geöffnet erschien in keinem Werkzeug «Zur Werkbank». Grund: die Werkbank hängt beim Öffnen `?wb=<Scrollhöhe>` an, die Werkzeuge erwarten wie beim Vorbild `?wb=de.<Kapitel>&wy=<Höhe>&wbo=<Adresse der Werkbank>`; dazu fehlte der Knopf im Schaufenster ganz, und Hafenbüro, Besucherliste und Hausdruckerei suchten die Werkbank auf ihrem eigenen Prüfserver (404).

Geändert (je Sicherung `*.vor-democheck-2026-10-21`, Änderungsdatum vorher geprüft):
- Werkbank: nur die zwei Stellen, die Werkzeug-Links mit der Herkunft versehen. `website/_werkbank/sb_skripte.py` (`merk`, Klick auf einen Link) und `website/_werkbank/rh_werkzeuge.py` (`live`, Klick auf den Laptop) und dieselben zwei Stellen im fertigen `website/werkbank/index.html` (kein Neubau). Links in die Werkzeuge (andere Adresse, Pfad `_werkzeuge/`) bekommen `wb=de.<Kapitel>&wy=<Höhe>&wbo=<Werkbank>`; alle übrigen Links (z. B. `ki.html`) behalten `wb=<Höhe>` wie bisher.
- Hafenbüro `_werkzeuge/maison/zur-werkbank.js`, Besucherliste `_werkzeuge/registre/zur-werkbank.js`: nehmen auf dem eigenen Prüfserver die Werkbank-Adresse aus `wbo` (online unverändert: dort gleiche Adresse). Versionszähler im Skript-Tag erhöht (`maison/index.html`, `registre/index.html`).
- Schaufenster `_werkzeuge/bureau/`: neue `zur-werkbank.js` (Kopie der Hausdruckerei, eingebunden mit `data-fremd`) und eine Skript-Zeile in `index.html`.
- Hausdruckerei `zur-werkbank.js`: auf :9053 ohne `wbo` gilt 127.0.0.1:8982.

Nachgeprüft (echter Weg, `_qa/democheck_rueckweg.js`): Werkbank http://127.0.0.1:8982/werkbank/ öffnen, im Kapitel V jeden Reiter wählen, «… öffnen» antippen, im neuen Reiter «Zur Werkbank» antippen. Chromium 1440: 7 von 7, WebKit 390: 7 von 7 führen zurück. Hafenbüro, Schaufenster, Kartenpult, Besucherliste und Hausdruckerei schliessen den Werkzeug-Reiter, die Werkbank steht noch an derselben Stelle; Reservationsbuch und Bildarchiv öffnen die Werkbank auf ihrem eigenen Server im selben Reiter (Kapitel V, 200), so gebaut in deren Skript. Klick auf den Laptop-Bildschirm: ebenso. Werkbank lädt in Chromium und WebKit ohne Skriptfehler. Bilder: `_Oberchef/zeigen/schloessli/democheck/imprimerie/rueckweg/`.

## Nach dem Auftrag

- **Druckauflösung einzelner Fotos:** 23 Meldungen der Druckprüfung (z. B. «Lästermeile, Plakat» A3 mit «bar» 66 dpi, «Die Karte · Plakat» mit «tortelloni» 75 dpi). Die Website-Fotos reichen für A5/A6, nicht für A3. Originale in Druckauflösung beim Haus holen. Die Druckprüfung sagt es dem Haus ehrlich, das ist kein Fehler des Werkzeugs.
- **Reservationsbuch und Bildarchiv** führen auf die Werkbank ihres eigenen Servers statt in den ersten Reiter zurück (funktioniert, ist aber ein zweiter Reiter mit der Werkbank). Bei Gelegenheit wie die anderen fünf über `wbo`.
- **Handy-Suchfeld:** Platzhalter «In Ihren 6 Medien suchen …» ist bei 390 px abgeschnitten («In Ihren»). Kürzerer Text am Handy.
- **Druckprüfung am Handy:** der Knopf ist am Handy aus dem Kopf genommen (so gebaut, Platz). Klären, ob es dort einen Weg zur Druckprüfung braucht.
- **Filme anderer Häuser:** `hilfe/` ist auch in Carlton, Doldenhorn, Ruedihus, Gasterntal und Schäfli leer (Führung ohne Film, Demo-Video mit Fehlersatz). Gleiche Skripte je Haus anpassen.
- **Anlässe-Karte und Handy-Kopf** stecken im gemeinsamen Kern (`studio.css`); vermutlich in den anderen Hausdruckereien gleich. Nicht angefasst (fremde Reviere).
- «Fotos des Hauses» nennt «0 mit KI erzeugt» und bietet den Filter «Mit KI erzeugt» an, der leer bleibt.
