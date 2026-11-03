---
tags: [projekt, website]
status: aktiv
---

# Lieferung Die Tafel (La Carte) · Wirtschaft am Schlössli Bottighofen (19.10.2026, Werkzeug-Anpasser Station 11)

Geliefert (Bau), Prüfung durch Station 12 offen. Alles Weitere, Prüfpunkte und offene Punkte: `_kette/11-werkbank/werkzeuge/karten/STAND.md`.

- Start: `python3 _werkzeuge/carte/serve.py 9031` (launch.json «tafel-schloessli») → http://127.0.0.1:9031/_werkzeuge/carte/
- Karten neu aus Station 10: `python3 _werkzeuge/carte/einlesen.py` (setzt den Satz mit `satz_bau.py`; ein Stand des Hauses wird nie überschrieben, `--grund` nur den Ursprung)
- Prüfen: `node pruef/rund.js` · `python3 pruefe.py wortlaut` (Server muss laufen) · `node pruef/lauf.js <chromium|webkit|firefox> <breite> <höhe>` (Prüfport 9033) · `node pruef/bilder.js` (Bilder für Stube und Werkbank nach `bilder/`) · `node pruef/fluessig.js` (erst unter Rechnerlast 8)
- Bilder: `bilder/la-carte-1440.webp` (Hauptbild), `-liste-`, `-lunch-`, `-fortgeschritten-`, `-website-1440.webp`, `la-carte-handy-390.webp`
- Vorlage: Tafel des Berghotel Gasterntal; deren Lieferung und Funktionsliste liegen als `*.vorlage-gasterntal.md` daneben.
