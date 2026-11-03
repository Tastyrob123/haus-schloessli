---
tags: [projekt, website]
status: aktiv
---

# Lieferung Werkbank-Kern · Wirtschaft am Schlössli (Nachtbau 3./4.11.2026)

Kopiert, umgekleidet, Hauswerte eingetragen: Aufbau, Wege und Prüf-Nachbauten der Werkbank des Culinarium (über Walk on the Wild Side), Inhalt aus dem alten Schlössli-Stand (`../_werkbank.vor-nachtbau-2026-11-03/`, demo-geprüft 21.10.2026). Nur lokal, nichts verschickt, keine KI aufgerufen.

## Wo

- Werkbank: http://127.0.0.1:9288/werkbank/index.html (Server `python3 website/_werkbank/serve.py 9288`; reicht `/_werkzeuge/`, `/assets/oberflaeche/`, `/stamm/`, `/werkzeuge/`, `/api/` an 9281–9287 weiter)
- KI: `/werkbank/ki.html` · Karte «Ein Vorschlag.»: `/werkbank/karte.html` + `/werkbank/vorschlag-wirtschaft-am-schloessli.pdf` · Geprüft: `/werkbank/geprueft/index.html` · Befund: `/befund/index.html` · Impressum: `/werkbank/impressum.html`
- Bau: `bash website/_werkbank/bau_alles.sh` (alles), `--ohne-aufnahmen`, `--nur-kern` (ohne die Schritte von Papier und Feed). Kit: `_Werkbank-Kit/` im Repo-Stamm.

## Was steht

- Kleid «Stuhl und See»: Nacht #0B1D3D, Tief, Stuhlblau mit Punkt-Tapete (`/assets/svg/tapete-a-*.svg`), Papier/Seespiegel/Blatt, Seehimmel als Linie und Zeichen, Schirmrot nur als Punkt; Titel Open Sans 400 in Versalien gesperrt, Instrument Sans, DM Mono (`/assets/fonts/`); Zeichen = die Zeiger, Wortmarke aus `schloessli-marke.svg#wm`. Reste der Vorlagen fängt `sb_farbe.py` (Farben) und `kleid_schloessli.py` (Schriften, Wege).
- Brief an Christian Kuchler und Jonas Volpert im Sie, ss statt ß (`ss_gang.py` nach jedem Bau), «Meine drei Orte» als Ticket; «Worum es geht» gestrichen.
- I Befund: vier erste Befunde der Potentialanalyse (Station 04) mit ihren Belegbildern (Handy + roter Kreis); eigene Seite `befund/` mit «Was schon gut ist», vier von vorn, den übrigen neun, «Was möglich ist».
- II Marke (Zeiger, Wortmarke, drei Schriften, neun Töne + Schirmrot, Herkunft aus Fotos der Website), III Website heute/neu (fünf Paare), zwölf Ideen, Gefüge, alle Seiten, Gäste-Funktionen (Aufnahmen neu vom 3.11.), IV Karten (Plan und PDFs von Werkbank Papier), V sieben Werkzeuge im Laptop mit Namen aus `kleid/schloessli.js`, «Einmal ändern», VI Für draussen (Untersetzer, Drucksachen, Mails, Postkarten, Feed, Dateien), VII Geprüft, VIII Angebot: Zusammenfassung, Umfang, Aufbau/Daten, «So geht's weiter», Karte «Ein Vorschlag.» mit Bau «Den Betrag nennen Sie» und Betreuung CHF 200 im Monat; Schluss, Fuss «Das Wichtigste».
- KI-Seite: vier Stellen, ohne Modellnamen, ohne Kosten.

## Wie geprüft

- `tor-schnell.js` (Chromium, 1440/1280/1000/390, max. 40 Zustände, Tiefe 2) für `werkbank`, `werkbank-ki`, `werkbank-karte`, `werkbank-geprueft`, `werkbank-befund`; Funde behoben (Versalien am Handy, Kanten im Auftakt-Fuss, Ziffern mittig, Nummern der Angebotsblätter, Zahlen der KI-Seite, Aufschriften im Kartenfächer). Stand der Läufe: siehe Meldung an den Oberchef.
- PDF «Ein Vorschlag.»: nur feste TrueType-Schnitte (kein Type 3), kein ß.
- Suchlauf aus dem gemeinsamen Auftrag über `werkbank/`, `befund/`: keine sichtbaren Treffer (nur Herkunftsvermerke in Kommentaren).

## Offen, mit Grund

- Bildschirme der Werkzeuge: Stand vom 3.11. abends; neu aufnehmen, sobald alle Werkzeug-Agenten fertig melden (`node _werkbank/sb_werkzeuge.js`, dann `bash bau_alles.sh --ohne-aufnahmen --nur-kern`).
