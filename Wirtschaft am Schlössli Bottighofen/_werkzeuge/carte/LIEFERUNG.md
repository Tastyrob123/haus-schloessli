---
tags: [projekt, website]
status: aktiv
---

# Lieferung Das Kartenpult · Wirtschaft am Schlössli Bottighofen (Nachtbau 3./4.11.2026)

Agent `schloessli-carte`. Aufbau und Funktionen der Tafel aus dem Stamm (Liste links, Karte rechts, Einfach/Fortgeschritten, Entwurf, Vorher/nachher, Probe-PDF, Veröffentlichen mit Wort-für-Wort-Prüfung, frühere Fassungen, Rundgang, Anleitung, Prüfseite), Inhalt und Kleid des Hauses. Name nur aus `kleid/schloessli.js` (`WO.name('karten')`).

**Werkzeug:** http://127.0.0.1:9283/_werkzeuge/carte/ · **Anleitung:** http://127.0.0.1:9283/_werkzeuge/carte/anleitung.html · **Prüfung:** http://127.0.0.1:9283/_werkzeuge/carte/pruefung.html

## Was steht

- **Die fünf Karten des Hauses** in der Seitenleiste (Restaurant: Karte nach Ländern, Lunch · Lästermeile · Keller: Weinkarte · Banketts: Bankett), je mit Foto des Hauses aus `/assets/img/` (anguria, suppe, bar, wein, gaststube; Register `website/inhalt/bilder.json`).
- **Nichts abgetippt:** `satz_bau.py` liest `website/inhalt/karte.json`, `lunch.json`, `laestermeile.json`, `wein.json`, `bankett.json` und setzt `satz/u-<karte>.html`; `einlesen.py` macht daraus den Baum in `_daten/`. Preise wie im Original (Franken, «35.-» beim Lunch). Schweizer Schreibung: «ß» → «ss» («Süsssaures»), Trenner « / » in Titeln → « · ».
- **Satz im Kleid des Hauses** (`satz/satz.css`): Kopf jeder Seite mit dem Zeichen (die Zeiger) und der Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» als Vektor aus `kleid/schloessli-marke.svg#wm`, Titel Open Sans in Versalien gesperrt, Horizont-Linie, Gerichte in DM Mono in Versalien (THON · CAVATELLI), Zeile in Instrument Sans, Allergene klein in DM Mono, Preise rechts (Hauptgang als zweiter Preis), Nabe zwischen den Lunch-Gängen, Preis als Marke zwischen zwei Linien. Schriften als feste Schnitte aus `/assets/fonts/` (`fonts_statisch.py` → `fonts/*.ttf`), kein Type 3. Karte 2 Seiten, Lunch A4 quer, Lästermeile 1 Seite, Weinkarte 20 Seiten (468 Weine, 495 Positionen, im echten Satz gemessen und gefüllt: `satz_messen.js`), Bankett 3 Seiten (je Menü eine).
- **Begriffe:** Karte, Lunch, Lästermeile, Weinkarte, Bankett, Eintrag; Sie-Anrede. Gestalten mit den Schriften (Open Sans, Instrument Sans, DM Mono) und Farben des Hauses (Tinte, Stuhlblau, Seehimmel tief, Nacht über dem See, Seehimmel, Blatt). Das Lunch-Menü darf die Küche selbst veröffentlichen, die übrigen Karten die Direktion.
- **Ansicht Website:** Karte, Weinkarte, Banketts, Startseite. Der Server liefert `/assets/oberflaeche/` immer aus `_werkzeuge/oberflaeche/` (vorher den alten Stand aus `website/assets/oberflaeche/`).
- **Anleitung** neu mit Hausinhalt und drei neuen Aufnahmen (`bilder/kartenpult-1440.webp`, `kartenpult-weinkarte-1440.webp`, `kartenpult-handy-390.webp`), Rundgang mit Hausinhalt.
- **Demo-Sperre:** Datei `DEMO` liegt; das Kartenpult schreibt nie in `website/`. Nach jedem Veröffentlichen `anschluss/karten.json` (je Karte die Einträge in der Form der Website, `web.py`).
- Culinarium-Abende, -Plakate, -Fotos, `karten_lesen.py` und Fraunces/Urbanist sind gelöscht.

## Starten und prüfen

- `python3 _werkzeuge/carte/serve.py 9283` (im Hausordner)
- Karten neu aus der Website: `python3 _werkzeuge/carte/satz_bau.py` → `python3 _werkzeuge/carte/einlesen.py` (ein Stand des Hauses wird nie überschrieben; `--grund` nur der Grundstand)
- `python3 _werkzeuge/carte/pruefe.py alles`: Rundlauf Satz → Baum → Satz (5/5 Zeichen für Zeichen gleich), jede Angabe der Quelle auf der Karte (Karte 92, Lunch 7, Lästermeile 28, Weinkarte 2142, Bankett 51: alle da), Druck jeder Karte: PDF = Daten Wort für Wort, nur feste Schnitte. GESAMT GRÜN.
- Schnelle Prüfung (Chromium, 1440/1280/1000/390): siehe unten.

## Prüfstand

PRUEFSTAND

## Offen, mit Grund

- **Website liest das Kartenpult noch nicht:** die Website baut ihre Karten aus `website/inhalt/*.json` (Revier `website/`, nicht das Kartenpult); bis zum Einbau von `karten.json` bleibt sie, wie sie ist.
- **Vier-Hände-Lunch** (`_karten/stand/vier-haende.json`) ist vorbei und nicht in `website/inhalt/`; nicht im Werkzeug.
- **Online** nicht gebaut und nicht hochgeladen (Auftrag).
