---
tags: [projekt, website]
status: aktiv
---

# Lieferung · Die Besucherliste · Wirtschaft am Schlössli (Nachtbau 3.11.2026)

**Werkzeug:** http://127.0.0.1:9286/_werkzeuge/registre/ (Server: `python3 _werkzeuge/registre/server.py 9286` im Hausordner)
**Anleitung:** http://127.0.0.1:9286/_werkzeuge/registre/anleitung.html (zehn Kapitel, Bilder neu aus dem Werkzeug)

## Was steht
- Aufbau und Funktionen aus der Besucherliste des Stamms (Culinarium, 28.10.2026: gefüllte Spalten, Seitenbild in der Besuchskarte, Weg-Rechnung über alle Seiten bis zur Reservation), Inhalt des Schlössli aus dem alten Stand (`_werkzeuge.vor-nachtbau-2026-11-03/registre/`).
- **Seiten** aus der Website (`python3 registre.py seiten`, Titel der Seiten): Startseite, Die Karte, Weinkarte, Banketts & Gruppen, Events & Termine, Über uns, Kontakt & Öffnungszeiten, Gutschein, Ihr Abend, AGB, Impressum, Datenschutzerklärung; je Seite ein eigenes Hausfoto aus `/assets/img/` (keine Fremd-, Gäste-, KI- oder Portalbilder, keins doppelt).
- **Wege des Hauses:** Fenster «Reservation» geöffnet, Tisch angefragt («Mit Wünschen anfragen»), «Direkt buchen» (gastronovi), Bankettanfrage geöffnet, Anfrage abgeschickt (Bankett, Gutschein), Anruf, Mail, weiter zum Schäfli, Route zum Hafen. Ansicht «Zur Reservation», Trichter «Der Weg zum Tisch».
- **Beispielwerte** (überall als Beispiel beschriftet, `beispiel/7|30|90.json` neu): Orte Thurgau, Kreuzlingen/Konstanz, rund um den See, Zürich, St. Gallen, Süddeutschland, wenige von weiter her; Herkunft Google, Instagram, GaultMillau, Guide Michelin, Falstaff, Schäfli, Tripadvisor, Gemeinde, Thurgau Bodensee; mehr Besuche Donnerstag/Freitag. Uhrzeit Europe/Zurich, Zahlen de-CH.
- **Kleid Schlössli:** nur `--wo-*` aus `kleid/schloessli.css`, Titel Open Sans 400 in Versalien gesperrt, Schriften aus `/assets/fonts/`, die Zeiger als Zeichen, Bühnenfotos des Hauses (Terrasse, Abend, Säntis, Apéro, Thon, Morgen am Hafen, Pasta, Gaststube). `culinarium.css` → `schloessli.css`; Speicher-Schlüssel `schloessli-*`; Sie-Anrede, ss statt ß. Namen nur aus `WO.name()`.
- Rundgang, «Zur Werkbank», Anleitung im Kleid des Hauses; `anleitung_bilder.js` läuft jetzt ohne macOS-Werkzeuge (JPEG direkt aus Playwright).

## Wie geprüft
- `tor-schnell.js … --nur besucherliste` (Chromium, 1440/1280/1000/390, max 40, Tiefe 2): 38 Zustände, **0 Funde, nichts nicht erreicht**.
- `--nur besucherliste-anleitung`: 16 Zustände, **0 Funde**.
- Mit dem Auge: Übersicht, Besuche, Herkunft, Zeit, Seiten, Verlauf, Zur Reservation, So wird gezählt bei 1440, 1000 und 390, Anleitung 390 und zwei Anleitungsbilder: Kennzahlen auf einer Grundlinie, Karten gleich hoch, kein Einzelwort, keine Culinarium-Spur.
- Suchlauf aus dem gemeinsamen Auftrag: nur Herkunftsvermerke in Code-Kommentaren.

## Offen (mit Grund)
- Die Beispielbesuche von «heute» wachsen mit der Uhrzeit: läuft eine Prüfung über eine volle Stunde hinweg, kann ein Besuch neu dazukommen und ein früher gesehener Zustand einmal «nicht erreicht» sein (gesehen in einem von vier Läufen, beim nächsten Lauf weg).
- Zählung auf der Website (`vorschlag/messung.js`) und Online-Speicher: nicht eingebaut, erst beim Online-Gehen (Revier `website/` und Roberts Wort).
