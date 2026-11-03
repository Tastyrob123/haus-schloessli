---
tags: [projekt, website]
status: entwurf
---

# Formulare der Website → Der Gastgeber · Wirtschaft am Schlössli (Baustein, E12/E24)

Gebaut am 19.10.2026 vom Werkzeug-Anpasser «Der Gastgeber» (Station 11, Teil `gaeste`). Auf der Website ist **nichts** eingebaut; das macht der Werkbank-Bauer in Station 14 über `website/bau.py`. Geprüft im Prüfbrowser: die Seite der Website, dazu `baustein/anfrage.js` nur im Prüfbrowser geladen (`pruefung/schloessli.js`, Schritte «Website-Formular …», in Chromium und Safari-Kern, 1440 und 390).

## Was es tut

- Die Website hat fünf Formulare: **Reservation mit Wünschen** (`#fe-reservation`, mit Allergenen als Kürzel G, L, E, F, S, So, En, N, Se, VEG), **Bankettanfrage** (`#fe-bankett`), **Gutschein** (`#fe-gutschein`), **Plätze für einen Anlass** (`#fe-plaetze`, anlaesse.html) und **«Ihr Abend»** (`[data-abend]`, abend.html). Heute zeigen sie nur «Vielen Dank» (Designstudie), nichts geht weg.
- Mit dem Baustein geht jede Anfrage in den Eingang des Gastgebers, mit allen Angaben in Zeilen, den Allergenen, Formular und Seite. Erst wenn der Gastgeber sie angenommen hat, erscheint «Vielen Dank» (das Fenster der Website setzt es selbst, haus.js und funktionen.js bleiben unverändert). Geht etwas schief, steht im Fenster eine Meldung mit der Telefonnummer des Hauses; die Eingaben bleiben.
- «Ihr Abend»: Familienfeier, Firmenanlass oder ein Bankettmenü werden **Bankett**, sonst **Reservation**.
- Ein unsichtbares Feld `website` hält Maschinen ab (der Gastgeber legt dann nichts ab). Kein Mailprogramm, nie `mailto`.

## Einbauen (Station 14)

1. `baustein/anfrage.js` → `website/assets/js/anfrage.js`.
2. In `bau.py` je Seite **nach** `haus.js` und `funktionen.js` einhängen: `<script src="assets/js/anfrage.js?v={V}" defer></script>`. Fassungsnummer aus dem Inhalt.
3. Die Hinweise «Designstudie: In diesem Entwurf wird nichts verschickt.» in den Fenstern bleiben, solange die Seite ein Entwurf ist; sie gehören der Website, nicht dem Baustein.
4. Lokal: Die Website auf :8982 und der Gastgeber auf :9047 sind zwei Adressen; der Gastgeber nimmt Formulare nur von seiner eigenen Adresse an (Schutz gegen fremde Seiten). Entweder `POST /_werkzeuge/reception/api/formular` im Hausserver an :9047 weiterreichen, oder die Website über den Gastgeber ansehen (`http://127.0.0.1:9047/` liefert die Website mit). Ohne das zeigt das Fenster die Meldung mit der Telefonnummer, nichts geht verloren.
5. Online (Station 16): Die Online-Fassung des Gastgebers ist noch nicht angepasst (die des Ruedihus liegt nur als Vorlage in `_bau/vorlage-ruedihus/online/`). Bis dahin bleibt der Baustein draussen oder zeigt online die Meldung.
6. Datenschutz (`datenschutz.html`, über `inhalt/`): Absatz zu den Formularen ergänzen. Vorschlag: «Anfragen über die Formulare der Website (Name, E-Mail oder Telefon, Datum, Personen, Allergien, Nachricht, Seite) speichern wir, um Ihnen zu antworten, und löschen sie nach zwölf Monaten. [Vom Haus zu prüfen.]»

Anderes Ziel als `/_werkzeuge/reception/api/formular`: `<script … data-api="/pfad">` oder `window.WS_ANFRAGE_API`.
