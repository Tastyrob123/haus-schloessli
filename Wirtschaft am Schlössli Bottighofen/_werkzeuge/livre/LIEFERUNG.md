---
tags: [projekt, website]
status: aktiv
---

# Das Markenbuch (Le Livre) · Wirtschaft am Schlössli · Lieferung (Nachtbau 3.11.2026)

**Adresse:** http://127.0.0.1:9285/_werkzeuge/livre/ · Hausregeln: http://127.0.0.1:9285/_werkzeuge/livre/buch.html · Anleitung: http://127.0.0.1:9285/_werkzeuge/livre/anleitung.html
Server: `python3 server.py 9285` im Ordner `_werkzeuge/livre` (Markenprüfung ohne KI, Probe-Antwort). Neu bauen: `python3 bau.py`, Anleitung: `BROWSER=chromium node anleitung_bilder.js && python3 anleitung_bau.py`.

## Was steht
- Aufbau und Funktionen aus dem Markenbuch des Culinarium (Übersicht, Fotos, Logo & Dateien, Markenprüfung, Hausregeln, Rundgang, Anleitung), Kleid `kleid/schloessli.*`, Name nur aus `WO_HAUS.namen`.
- **Fotos:** 47 aus dem Bildregister der Website (`website/inhalt/bilder.json`, Stufen aus `website/assets/img/`), sieben Gruppen: Hafen & Terrasse, Küche & Teller, Bar & Lästermeile, Wein, Team, Bodensee & Geschichte, Instagram. 36 des Hauses, 11 frei lizenziert (Wikimedia, mit Urheber, Lizenz, Quelle). Nicht drin (Rechte): `tb-*`, `baum`, `kf-*`, `pa-teller`, `kp-party`, `feuerwerk*`, `ch-*`, dazu `stier`, `mi-teller`, `schaefli`.
- **Dateien:** Zeichen, Zeiger, Logo (4 Farben), Name lang/kurz, Tapeten, Original-Logo, Farben (CSS/JSON/ASE), Schriften-ZIP, Marken-ZIP — alles Schlössli (aus dem Stand vom 20.10.2026). Culinarium-Dateien, -Fotos, -Beispiele gelöscht (22 MB → 11 MB).
- **Farben:** Farbwelt «Stuhl und See» aus `haus.css`, Drehung «Ton in Ton» im Bau nachgerechnet: Nacht, Tief, Stuhlblau, Papier, Seespiegel, Blatt, Seehimmel (hell/tief), Tinte, Titelblau, Schirmrot (nur Punkt).
- **Schriften:** Open Sans, Instrument Sans, DM Mono, Caveat aus `/assets/fonts/`.
- **Hausregeln** (`buch.py` aus `_kette/05-markenbauer/marke/`): Zeichen, Wortmarke, Schriften, Farben mit Fotos des Hauses, Farbwelt, Logo richtig/falsch, Ton, neu «Zehn Regeln für jeden Text» (Sie, ss, Versalien, Betonung über Farbe, kein Hotel, Schäfli nur als Verweis), eigene Welt. Ohne Arbeitsstand (Messstellen, Mediane, heutige Squarespace-Seite, «gewählt»). Bewegung über das Kleid (`schloessli.js` → `bewegung.js`).
- **Markenprüfung:** Palette aus `livre.json`, Regeln des Hauses, Probe-Antwort ohne KI; Beispiel «Abend am Hafen» neu gemessen.
- **Anleitung:** neun Kapitel, Texte in Sie-Form, Bilder neu aus dem Werkzeug (Chromium).
- Nichts aus `_quelle/` zur Laufzeit (kein `_quellen.json`; «Druck» liefert die grösste Fassung der Website).

## Wie geprüft (3.11.2026, `tor-schnell.js … --browser chromium --max 40 --tiefe 2 --breiten 1440,1280,1000,390`)
| Schlüssel | Zustände | Funde | nicht erreicht |
|---|---|---|---|
| plakatarchiv | 17 | 0 | 0 |
| plakatarchiv-buch | 7 | 0 | 0 |
| plakatarchiv-anleitung | 8 | 0 | 0 |

Vorher 235 Funde (erster Lauf), repariert: Farbkarten kompakt, kurze Kachelnamen, Wahl-Etikett, Knöpfe der Hausregeln mittig, Titel ohne Einzelwort, Leiste der Hausregeln am Handy, verzerrtes Beispiel-Logo als eigenes Bild, Kapitel der Hausregeln als `kapitel` statt `blatt` (sind Bildschirm-Kapitel, keine Druckblätter; die Prüfung las sie als Dokument und wandte das noch nicht umgestellte Stilblatt der Hausdruckerei an: «Versalien nur … Fraunces … Urbanist»).
Mit dem Auge: rund 30 Zustandsbilder (1440 und 390): Fotos ganz, Reihen auf einer Linie, keine leere Kachel, Kleid und Schriften des Hauses, nichts vom Culinarium.

## Offen
- Markenprüfung mit Claude: aus, bis Robert den Schalter freigibt (Probe-Antwort).
- Cloud-Prüfung in WebKit: stösst der Oberchef an.
