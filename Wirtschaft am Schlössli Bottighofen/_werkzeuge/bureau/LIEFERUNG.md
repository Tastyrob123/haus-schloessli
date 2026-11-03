---
tags: [projekt, website]
status: aktiv
---

# Das Schaufenster (Website pflegen) · Wirtschaft am Schlössli · Lieferung

Nachtbau 3.11.2026, Agent `schloessli-bureau`. Aufbau und Funktionen aus dem Schaufenster des Culinarium (28.10.2026), Inhalt aus dem Schlössli. Nichts online, nichts verschickt.

## Wo

- Werkzeug: http://127.0.0.1:9282/_werkzeuge/bureau/ · Server `python3 _werkzeuge/bureau/serve.py 9282` im Hausordner (legt die Probe-Kopie der Seiten selbst an, wenn sie fehlt)
- Termine: `?ansicht=e:termine` · Rundgang: `?rundgang` · Anleitung: `anleitung.html` · Prüfseite: `/werkzeuge/website/pruefung.html?haus=schloessli`
- «Website ansehen»: die Probe-Kopie der gebauten Website (`/werkzeuge/website/_probe/schloessli/online/`), ausgeliefert mit dem veröffentlichten Stand der Ferien

## Was steht

- **Beschreibung** (`beschreibung.py` → `_Werkzeuge/werkzeuge/website/haeuser/schloessli.json`, `_Werkzeuge/haeuser/schloessli/haus.json`, nie von Hand): alle 12 Seiten (index, abend, karte, weinkarte, feiern, anlaesse, team, kontakt, gutschein, impressum, datenschutz, agb), 8 Bereiche mit Hausfoto, Bereiche «Anlässe» und «Team», gesperrte Karten-Stellen (Kartenpult), Angaben Telefon, Strasse, PLZ/Ort, E-Mail, Instagram aus `website/inhalt/haus.json`, Google-Texte, eigenes Foto nach `assets/img`, Name des Kartenpults aus `kleid/schloessli.js`.
- **Termine** (`termine.py`, `termine-ansicht.js`): die Ferien des Hauses als Daten aus `haus.json › ferien_iso, ferien` (Entwurf, Stand, Verlauf in `_daten/termine.json` mit `.gut`). Ausgeliefert in jede Seite der Probe-Kopie: `data-zu` der Reservationsfenster (gesperrte Tage) und die Zeile «Ferien» der Startseite; ohne Änderung Byte für Byte wie gebaut. Prüfung auf dem Server (Tag gültig, Reihenfolge, höchstens 120 Tage, keine Überschneidung, Anlass ohne Klammern, 409 bei zwei Fenstern). Darunter die Anlässe aus `haus.json › anlaesse` zum Nachschlagen mit Weg in den Bereich «Anlässe».
- Rahmen: Kleid `kleid/schloessli.*`, Schriften `/assets/fonts/`, Fotos `/assets/img/`, Kennung `schloessli` (Speicher, `rundgang-schloessli-bureau`, `schloessli-wb`), Sie-Anrede, ss. Rundgang fünf Schritte mit Haustexten; Prüfseite im Kleid mit Teil «Ferien des Hauses» und Lexikon; Anleitung neun Schritte, Bilder neu aufgenommen (`pruefung/anleitung_bilder.js`, Wegwerf-Server und -Daten).

## Wie geprüft

- Schnelle Prüfung `tor-schnell.js … --nur schaufenster` und `--nur schaufenster-anleitung` (Chromium, 1440/1280/1000/390), Ergebnis siehe Schlussmeldung an den Oberchef.
- Bildschirme 1440 und 390 mit dem Auge (Übersicht, Termine, Bereich, Angaben, Google, Entwurf, Verlauf, Anlässe, Team, Prüfseite, Anleitung).
- `termine.fuelle`: ohne Änderung Seite unverändert; mit Änderung `data-zu` und Ferien-Zeile neu; falsche Eingaben abgewiesen.
- Suchlauf aus dem gemeinsamen Auftrag: Treffer nur in Herkunftsvermerken der Code-Kommentare.

## Offen

- `beschreibung.py` schreibt die Beschreibung des Hauses in den Stamm (`_Werkzeuge/werkzeuge/website/haeuser/schloessli.json`, `_Werkzeuge/haeuser/schloessli/haus.json`): ausserhalb dieses Reviers, vom Oberchef mit einzuchecken.
- Das Foto des nächsten Anlasses (Bereich «Anlässe») ist das Bild, das die Website selbst zeigt (`kf-teller`, Excellence); das Werkzeug zeigt die Seite, wie sie gebaut ist.
