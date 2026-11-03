---
tags: [projekt, website]
status: aktiv
---

# Das Hafenbüro (Zentrale, Arbeitsname La Maison) · Wirtschaft am Schlössli Bottighofen · Lieferung 3.11.2026 (Nachtbau)

Agent `schloessli-maison`. Nichts online, nichts verschickt.

**Adresse:** http://127.0.0.1:9281/_werkzeuge/maison/ (Server `python3 server.py 9281` im Ordner `_werkzeuge/maison`) · Kleid-Muster: http://127.0.0.1:9281/assets/oberflaeche/muster.html?haus=schloessli

## Was steht

- **Empfang:** fünf hohe Fenster mit Fotos des Hauses (Platanen-Terrasse, Anguria auf blauem Teller, Morgen am See, Jonas Volpert, Terrasse am Abend; aus `website/inhalt/bilder.json`), darüber Wortmarke «WIRTSCHAFT AM SCHLÖSSLI», «by Christian Kuchler · Seestrasse 50 · 8598 Bottighofen», «DAS HAFENBÜRO» gross auf dem Horizont des Sees, Gruss nach Tageszeit, Datum, Zeile «Heute · Besuche · zur Reservation · Die Besucherliste öffnen» (Taste 6). Stand je Werkzeug live (über `/_weiter/…`).
- **Säle** für alle sechs Werkzeuge mit echten Bildschirmen (`roh/`, Chromium 1440 × 932 @2x, 3.11.2026 mit dem Stand der anderen Agenten aufgenommen), Tafel «So geht’s» in Sie-Form mit Knopf-Namen aus dem Code (alle gefunden), Stücke: drei Kartenseiten (Lästermeile, Lunch, Speisekarte), Bankett-Flyer, sechs Hausfotos, zwölf Hausfarben aus `livre/livre.json`; Weg zur Reservation (Besuche → «Die Karte» angesehen → Reservation oder Anfrage → am Tisch).
- **Fuss:** Zeiger und Wortmarke, Haus (Adresse, Telefon aus `haus.json`), sechs Anleitungen, Fragen. Laufband, Rundgang (5 Schritte), «Zur Werkbank» (`schloessli-wb`), Startfehler-Tür, «Website ansehen» = Website des Schlössli auf 9281.
- **Kleid:** Open Sans 400 in Versalien gesperrt für Titel, Instrument Sans im Lauf, DM Mono für Etiketten und Zahlen, alle aus `/assets/fonts/`; Farben Nacht/Stuhlblau/Papier/Seehimmel, Schirmrot nur als Punkt in der Nabe der Saal-Linie.
- **Bau:** `python3 bau.py` liest alles aus `website/inhalt/haus.json`, `website/inhalt/bilder.json`, `oberflaeche/kleid/schloessli.js` (Namen, Sätze, Bar, Kürzel) und `schloessli-zeichen.svg`/`schloessli-marke.svg`; bricht ab, wenn Culinarium-, Wild-Side- oder Fremdhaus-Angaben in die Ausgabe gelangen. Bildschirme neu: `SCHIRM_KERN=chromium node schirme.js [werkzeug]`, dann `python3 bau.py`. `server.py` holt die Stand-Wege aus `stand_wege.json` (früher aus alten Kettenadressen) ohne Proxy.
- Culinarium-Dateien gelöscht (Fotos, Fenster, Karten- und Druckbilder, `wahl-hero/`, `namen/`, `schrift/`); Suchlauf aus dem gemeinsamen Auftrag in `maison/` und `oberflaeche/`: keine sichtbaren Treffer (nur Herkunftsvermerke und die Sperrliste im Bau).

## Wie geprüft

- `tor-schnell.js … --nur tresen --browser chromium --max 40 --tiefe 2 --breiten 1440,1280,1000,390`: **5 Zustände je Breite, 0 Funde, nichts nicht erreicht** (Lauf `/tmp/aus-tresen`). Behoben auf dem Weg: zerfallende Spalten (Fenster-Stand und Weg-Stufen kürzer, Zahlenzeile in zwei Teilen), Schrift in den Eck-Knöpfen mittig, abgeschnittene Fensterleiste am Handy, Laufband-Text unter der Platte, Einzelwort im Saal-Satz, Punkt am Zeilenende in Adresse und Datum (390).
- Mit den Augen: Empfang 1440/1000/390, Rundgang 1440/390, alle sechs Säle und Fuss je 1440 und 390 (über 20 Bilder).

## Offen, mit Grund

- Bildschirme der anderen Werkzeuge zeigen deren Stand vom 3.11. abends; gegen Ende noch einmal `SCHIRM_KERN=chromium node schirme.js` und `python3 bau.py`, wenn die Agenten fertig sind.
- Tafel der Hausdruckerei (`tafeln.json`) nutzt «Fünf Entwürfe», «Arten und Vorlagen», «Druckfertig speichern»; ändert die Hausdruckerei diese Knöpfe, meldet `bau.py` es.
