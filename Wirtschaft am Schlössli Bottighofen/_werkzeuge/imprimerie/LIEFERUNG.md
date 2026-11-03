---
tags: [projekt, website]
status: entwurf
---

# Die Hausdruckerei · Wirtschaft am Schlössli Bottighofen · Lieferung

**Stand:** 3.11.2026, Nachtbau (Agent schloessli-imprimerie, gemeinsamer Auftrag `_werkzeuge/AUFTRAG-GEMEINSAM.md`). Lokal, nichts verschickt, keine KI aufgerufen (nur Probe).

## Wo

- **Werkzeug:** http://127.0.0.1:9287/_werkzeuge/imprimerie/ (Server: `python3 serve.py 9287` im Ordner `_werkzeuge/imprimerie`)
- **Newsletter & E-Mail:** http://127.0.0.1:9287/_werkzeuge/imprimerie/mail.html · **Prüfseite:** `pruefung.html` · **Anleitung:** `hilfe/index.html` (Demo-Video und neun Kurzfilme, am Schlössli aufgenommen, `_bau/filme.js`)
- **Hausordner:** `haeuser/schloessli/` (marke.json, stilblatt.json, STILBLATT-DRUCKSACHEN.md, Schriften, Fotos, Vorlagen, Mails, Drucksachen)

## Was steht

- Werkzeug ganz auf `schloessli`: Kleid des Hauses (`/assets/oberflaeche/kleid/schloessli.*`), Name nur aus `WO.name('druck')` «Die Hausdruckerei», Markenbuch über `WO_HAUS.wege.marke` (:9285), localStorage `ds-schloessli-*`, Fotos aus `website/assets/img/` (Rechte laut `website/inhalt/bilder.json`, keine Gäste-/Fremd-/KI-Bilder), Schriften Open Sans / Instrument Sans / DM Mono als feste Schnitte (kein Type 3 im PDF), Zeichen = die Zeiger, Wortmarke als Grafik. Sie-Form, Schweizer Schreibung.
- **89 Vorlagen in 20 Arten** (13 Gruppen): Aushänge (Betriebsferien, Kreuzfahrt, Ruhetag, Öffnungszeiten, Besen), Plakate, Einladungen, Programm «Die Reise», Lunch-Menü, Bankettmenüs, Einleger, Weinempfehlungen (Jonas Volpert), Lästermeile, Tisch- und Hinweiskarten, Postkarten vom Hafen, Gutscheine, Pressemappe, Teamaushänge, Instagram, Story, sechs Mails in Sie-Form. Inhalte nur aus `website/inhalt/*.json` (`bau_vorlagen.py`), keine Preise.
- **34 fertige Drucksachen** (`haeuser/schloessli/drucksachen/`, Liste `LISTE.md`): je Stück PDF mit 3 mm Beschnitt und eingebetteten Schriften plus Vorschaubild; gesetzt mit `node _bau/drucksachen.js`. Vorschauen aller Vorlagen in `vorschau-dok/`, druckfertige Bilder in `druck/`.
- KI-Entwürfe: nur Probe, gewählt wird die passendste fertige Vorlage des Hauses und als Beispiel beschriftet.

## Geprüft

Schnelle Prüfung lokal (Chromium, 1440/1280/1000/390, höchstens 40 Zustände, zwei Ebenen), sieben Runden: `plakatwerkstatt` 40 + 120 Zustände, `plakatwerkstatt-mail` 40 + 145 Zustände, nichts «nicht erreicht», keine Skriptfehler. Letzte Runde: 3 Funde (je Schlüssel dieselben), alle von derselben Art: «Text zerfällt» an drei Postkarten-Karten in der Abteilung «Hafen & Terrasse», deren Knopf das ganze Blatt (Vorder- und Rückseite, live gesetzt) enthält — die Regel zählt die Zeilen des Blatts als Lesetext (in `seite.js` sind Vorlagen-Knöpfe erst ab 40 Elementen ausgenommen, die Postkarte hat 28). PDFs: alle Schriften CID TrueType eingebettet, kein Type 3. Mit dem Auge: Übersicht, Anlässe, Abteilung, Motive, Fotos, Alle Vorlagen, Studio, Newsletter-Seite in 1440/1280/1000/390 und 10 Drucksachen.

## Offen

- Einladung zum Bankett und Bestätigungsmail tragen [Datum · Uhrzeit] als Feld zum Ausfüllen; Gutscheinwert und Nummer bleiben leer zum Eintragen (keine Zahl erfunden).
