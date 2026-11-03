---
tags: [projekt, website]
status: aktiv
---

# Werkzeug-Oberfläche · Wirtschaft am Schlössli Bottighofen

Einziger Schreiber dieses Ordners: der Agent **schloessli-maison** (Zentrale «Das Hafenbüro»), im Nachtbau 3./4.11.2026. Paket = Stamm der Häuser (`grund.css`, `rahmen-buehne.css`, `rahmen-inseln.css`, `oberflaeche.js`, `bewegung.js`, `muster.html`, unverändert aus dem Stamm), Kleid eigen: `kleid/schloessli.js` + `kleid/schloessli.css` + `kleid/schloessli-zeichen.svg` (die Zeiger der Wortmarke, aus `website/assets/svg/zeichen.svg`) + `kleid/schloessli-marke.svg` (die ganze Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» in Open Sans, Symbol `#wm`). Rahmen «Die Bühne»: Kopf dunkel wie die Nacht über dem See, Raum hell wie das Papier im Seespiegel.

## Einbinden (jedes Werkzeug gleich)

Der Server des Werkzeugs liefert `/assets/oberflaeche/…` aus **diesem Ordner** und `/assets/…` sonst aus `website/assets/` (Fotos `/assets/img/<schlüssel>-<breite>.webp`, Register `website/inhalt/bilder.json`; Schriften `/assets/fonts/`; Tapeten `/assets/svg/tapete-a-dunkel.svg`, `-hell.svg`). `/assets/bild/`, `/assets/schrift/` und `/assets/zeichen/` gibt es hier **nicht**. Muster: `_werkzeuge/maison/server.py` (`translate_path`, Port 9281).

```html
<script src="/assets/oberflaeche/kleid/schloessli.js?v=1"></script>          <!-- vor allem anderen, ohne defer -->
<link rel="preload" href="/assets/fonts/OpenSans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v=1">
<link rel="stylesheet" href="/assets/oberflaeche/rahmen-buehne.css?v=1">
<link rel="stylesheet" href="/assets/oberflaeche/kleid/schloessli.css?v=1">
<!-- eigenes CSS des Werkzeugs danach -->
<script src="/assets/oberflaeche/oberflaeche.js?v=1"></script>            <!-- vor dem Skript des Werkzeugs -->
```

`?v=` beim Bau aus dem Inhalt bilden (M20), nie von Hand. Musterseite mit jedem Baustein: http://127.0.0.1:9281/assets/oberflaeche/muster.html?haus=schloessli (ohne `?haus` gilt jetzt auch `schloessli`).

## Werte des Hauses (nur lesen, nie abtippen)

- **Namen der Werkzeuge:** nur `WO.name('<teil>')` bzw. `WO_HAUS.namen` (Teile: zentrale, website, karten, gaeste, marke, besuche, druck): Das Hafenbüro · Das Schaufenster · Das Kartenpult · Das Reservationsbuch · Das Markenbuch · Die Besucherliste · Die Hausdruckerei (Robert 19.10.2026 «passt», «Markenbuch» seit 29.10.); je Werkzeug ein Satz in `WO_HAUS.saetze`. Python-Seiten lesen beides aus `kleid/schloessli.js` (Regex auf `namen:` / `saetze:`, so `maison/bau.py`).
- **Haus:** `WO_HAUS.kurz` = `schloessli` (Speicher-Schlüssel `schloessli_*`, `ds-schloessli-*`), `name`, `voll`, `ort` (Bottighofen), `bar` (Lästermeile), `anrede: 'sie'` (das Haus siezt), Schreibung ss statt ß.
- **Wege und Ports:** `WO_HAUS.wege` (`/_werkzeuge/<werkzeug>/`), `WO_HAUS.ports` (9281 Zentrale, 9282 Schaufenster, 9283 Kartenpult, 9284 Reservationsbuch, 9285 Markenbuch, 9286 Besucherliste, 9287 Hausdruckerei, 9288 Werkbank). Lokal schreibt das Kleid Wege zu anderen Werkzeugen auf `http://127.0.0.1:<port>/…` um (nie `localhost`), online bleiben sie relativ.
- **Farben:** nur die Variablen aus `kleid/schloessli.css`. Dunkle Flächen `--wo-tief` (#0b1d3d Nacht über dem See), `--wo-nacht` (#0A234C Tief), `--wo-nacht2` (#113d88 Stuhlblau); Raum `--wo-papier` (#E7ECF3), `--wo-papier2` (#D0DAE7 Seespiegel), `--wo-blatt` (#F4F6F9), `--wo-weiss`; Linie, Zeichen, Knauf auf Dunkel `--wo-gold` = `--wo-kerze` (#A2B6CF Seehimmel, hell #C5D2E1); Betonung auf Hell `--wo-akzent` (#0F3678 Seehimmel tief); Schrift `--wo-tinte` (#041023), `--wo-leise`; **Schirmrot `--wo-rot` / `--wo-punkt` (#FD9964) nur als Punkt** (Marke «Entwurf», Nabe der Zeiger). Dunkle Flächen tragen die Punkt-Tapete `--wo-tapete`. `.wo-dc`/`.wo-dj` setzen hier nur Seehimmel tief (kein Violett).
- **Schrift:** Titel `var(--wo-titel)` = **Open Sans 400 in Versalien gesperrt** (wie die Wortmarke; `.wo-sb__h`, `.wo-zw` schon gesetzt), nie fett, nie kursiv, Betonung `em` über Farbe; Lauf `var(--wo-sans)` = Instrument Sans 400–600; Etiketten, Zahlen, Gerichte wie auf der Karte `var(--wo-mono)` / `var(--wo-etikett)` = DM Mono gesperrt (`.wo-zahl`, `.wo-rudi` = Menüzeile in Versalien, Name der Klasse aus dem Stamm). Fraunces, Urbanist, Prata, Hanken gibt es hier nicht.
- **Form:** der Horizont des Sees als feine Linie über die ganze Breite unter dem Titel der Bühne; Platten 20 px Radius mit Seehimmel-Linie oben, Kacheln 14 px; über Zwischentiteln die Linie mit der Nabe der Zeiger (Kreis, Punkt in Schirmrot); Zeichen = die Zeiger im Ring (`.wo-marke-w`). Knöpfe: `.wo-kn--gold` Hauptweg Stuhlblau mit hellem Knauf, `.wo-kn--dunkel` Nebenweg Nacht mit Seehimmel-Linie, `.wo-kn--hell` heller Knopf auf Papier. Keine Einkerbungen, keine Punkt-Etiketten, keine Pillen-Reihen, keine Plakat-, Ticket- oder Leuchtschrift-Optik.
- **Ganze Wortmarke:** `<svg viewBox="0 -463 40448 1925"><use href="/assets/oberflaeche/kleid/schloessli-marke.svg#wm"/></svg>`, Farbe über `color` (Seitenverhältnis 21 : 1: in der Breite planen, nicht in der Höhe). Nie als Schrift nachbauen, nie neu zeichnen.
- **Startbild-Foto:** `WO_HAUS.foto` = `/assets/img/start-1200.webp` (Schlüssel `start`, «Blaue Stühle auf der Terrasse am Mittag …»), Stufen 480/800/1200. Weitere Fotos nur aus `website/inhalt/bilder.json`; keine Gäste-, Fremd- oder KI-Bilder (`tb-*`, `baum`, `kf-*`, `pa-teller`, `kp-party`, `feuerwerk*`, `ch-*`).

## Änderungen

Nur `schloessli-maison` schreibt hier. Wer etwas am Kleid braucht, löst es im eigenen CSS und meldet es dem Oberchef.

| Datum | Was | Für wen |
|---|---|---|
| 03.11.2026 | Kleid Schlössli statt Culinarium: `kleid/schloessli.{js,css}`, `schloessli-zeichen.svg`, `schloessli-marke.svg` (Oberchef, aus dem Stamm und den Schlössli-Werten vom 19.10.2026) | alle sieben |
| 03.11.2026 | Geprüft in `muster.html?haus=schloessli` (1440): Farben, Open Sans in Versalien, Knöpfe, Tapete, Brief, Felder im Haus-Stil. `muster.html`: Vorgabe-Haus `schloessli`, Beispiele Sie-Form und «Tisch» statt «Zimmer» | alle sieben |
| 03.11.2026 | Herkunftsvermerke in `bewegung.js`, `kleid/schloessli.js`, `kleid/schloessli.css` auf das Haus gestellt (nur Kommentare, keine Wirkung) | – |
