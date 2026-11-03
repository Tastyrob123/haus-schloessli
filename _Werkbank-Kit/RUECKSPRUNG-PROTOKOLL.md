# Rücksprung-Rollout 1.11.2026

Robert: Zurück im Browser landet in der Werkbank auf der alten Höhe, nie ganz oben. Kit: `ruecksprung.js`, `ruecksprung.py`, `ruecksprung_test.js`, `kern.schreib`, Ende von `bau.py`.
Test je Haus: `node ruecksprung_test.js http://127.0.0.1:<port>/ chromium|webkit`, 1440 und 390 px, Abschnitt in Fenstermitte ±40 px. Sicherung je Haus: `<Projekt>/_sicherung/vor-ruecksprung-2026-11-01/`.
Ausgelassen: Grand Beau-Rivage (nie anfassen), Walk on the Wild Side, Culinarium Hannover, Tasty Grand Hotel (Website, keine Kit-Werkbank), Probe- und Sicherungskopien.

| Haus | Seiten | Chromium | WebKit | Bemerkung |
|---|---|---|---|---|
| Berghotel Gasterntal | 9 | 10/10 | 10/10 | alter Rückweg `data-wb-hoehe` (`_werkbank/zurueck.py`) macht Zurück/Vor nicht mehr selbst |
| Carlton-Europe Interlaken | 60 | 13/13 | 13/13 | Rücksprung als letzter Schritt in `_werkbank/bau.py`; `ce-wb-y` in `werkbank.js` nur noch für ?y= |
| Compleat Redesign | 6 | bestanden | bestanden | Werkbank verlinkt nur auf die Website; einzeln geprüft (Werkbank → Startseite → Zurück) |
| Familie Maeder — Landingpage | 3 | 4/4 | 4/4 | |
| Hotel Seiler au Lac | 6 | 11/11 | 11/11 | |
| Landgasthof Ruedihus | 13 | 13/13 | 13/13 | `#rh-zurueck` (haus.py) mit `data-rs`, nur noch ?y= |
| Taverne zum Schäfli | 13 | 12/12 | 12/12 | `#rh-zurueck` (sb_skripte.py) mit `data-rs`; `auslieferung/` unverändert, bekommt es beim nächsten Bau |
| Waldhotel Doldenhorn | 11 | 13/13 | 13/13 | eigener Rückweg liegt in der Website (`assets/js/zur-werkbank.js`), nicht angefasst |
| Wirtschaft am Schlössli | 14 | 14/14 | 14/14 | `#rh-zurueck` (sb_skripte.py) mit `data-rs`, nur noch ?y= |

## Linkprüfung aller Werkbänke 1.11.2026 (nach Roberts Fund «Das Hausbuch startet nicht»)

Ursache des Funds: Link über den Kette-Server 8978 (`/haus/…`); Werkzeuge brauchen den Hausserver. Werkbänke nur über den Hausserver öffnen:
Gasterntal 8918 · Carlton 8912 · Compleat 8853 · Maeder 8925 (`studio.py`, ersetzt `serve.py`, liefert den Empfang) · Seiler 8921 · Ruedihus 8917 · Schäfli 9068 · Doldenhorn 8916 · Schlössli 8982.
Jeder lokale Link jeder Werkbank-Seite in Chromium und WebKit geöffnet: 0 Fehler in allen neun Häusern. Behoben: Carlton-Werkbank war seit 26.10. die Fassung zum Hochladen (lokal neu gebaut; Livre/Registre lokal `_werkzeuge/`, Knöpfe auf Unterlagen/Drucksachen je nach Fassung), Schlössli-Unterlagen «Karten selbst ändern» auf die eigene Tafel 9031, Maeder-Empfang (Server getauscht).
