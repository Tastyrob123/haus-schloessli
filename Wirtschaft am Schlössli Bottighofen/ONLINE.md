---
tags: [projekt, website]
status: aktiv
---

# Wirtschaft am Schlössli · online als Demo (22.10.2026)

## Adressen

- Website: https://schloessli.tastystudios.ch/
- Werkbank: https://schloessli.tastystudios.ch/werkbank/
- Werkzeuge (aus der Werkbank, Kapitel Werkzeuge, oder direkt):
  - Das Hafenbüro (La Maison): https://schloessli.tastystudios.ch/_werkzeuge/maison/
  - Das Schaufenster (Le Bureau): https://schloessli.tastystudios.ch/_werkzeuge/bureau/
  - Das Kartenpult (La Carte): https://schloessli.tastystudios.ch/_werkzeuge/carte/
  - Das Reservationsbuch (La Réception): https://schloessli.tastystudios.ch/_werkzeuge/reception/
  - Das Bildarchiv (Le Livre): https://schloessli.tastystudios.ch/_werkzeuge/livre/
  - Die Besucherliste (Le Registre): https://schloessli.tastystudios.ch/_werkzeuge/registre/
  - Die Hausdruckerei (L’Imprimerie): https://schloessli.tastystudios.ch/_werkzeuge/imprimerie/
- Beigaben: /unterlagen/ · /drucksachen/ · /feed/ · /untersetzer/ · /material/ · /potenzialanalyse/ · /mails/ · /werkbank/geprueft/

Nichts davon ist verschickt. Keine Mail, kein Link an den Kunden.

## Wie es online läuft (Demo)

- Hochladen nur über `~/Desktop/Website-Projekte/_Kuchler-Online/online.py stell|hoch schloessli` (Vorbild: online.py der Maeder-Häuser, als Modul benutzt). Online-Ordner `~/kuchler-online/schloessli-bottighofen-entwurf` (+ `-2`, `-3`, `-4` für Bilder und Beigaben, `schloessli-bottighofen-werkstatt` für die grossen Fotos der Hausdruckerei).
- Im Projekt wird nichts verändert: lokale Ports (8982, 8987, 9031, 9035, 9047, 9049, 8988, 9053) und der Schäfli-Link (8953) werden nur in der Online-Kopie auf die öffentlichen Adressen umgeschrieben.
- Werkzeuge als Demo: kein Speicher am Projekt (alles nur in der laufenden Instanz, nichts hält), keine KI (Probe-Antworten, keine Schlüssel), «Veröffentlichen» in jedem Werkzeug aus, kleines Schild «Demo» unten rechts. Le Bureau läuft zum ersten Mal online (Schreibtisch des Stamms als Vercel-Funktion, nur ansehen und Vorschau, Fotos hochladen aus).
- Wächter und Übersicht kennen das Haus: `~/Versand-Schutz/projekte.py`, Schlüssel `wirtschaft-am-schloessli`.

## Was geprüft ist

1. Am Rechner gegen die Online-Kopie (probe.py), dann online: `pruefen.js` (Chromium und WebKit, 1440 und 390): Startseite und alle Unterseiten, Werkbank mit jedem Kapitel, jedes der sieben Werkzeuge aus der Werkbank geöffnet, Knopf «Zur Werkbank» führt zurück, Schild «Demo», alle Beigaben, 109 Links und 27 PDFs ganz abgerufen. Ergebnis online: 0 Funde. Keine Verweise auf localhost/127.0.0.1, keine Konsolenfehler, mailto/tel nie ausgeführt.
2. Prüfung von aussen `~/Aussen-Pruefung/aussen wirtschaft-am-schloessli` (Chrome, Safari, Firefox, Handy, Firmennetz …, Klick-Probe aller Werkzeuge): zweiter Lauf 22.10.2026 02:45: rot 0, Klick-Probe 687 Knöpfe in 8 Werkzeugen, 0 Fehler. Danach behoben und einzeln nachgeprüft (alle 200): die vier PDFs im Kartenpult (Speisekarte, Lästermeile, Weinkarte, Bankett) und das Lunch-Menü. Gefundenes und behoben, nur online aufgetreten: Bilder im Bildarchiv («Logo & Dateien»), PDFs im Kartenpult, Knopf «Zur Werkbank» (die Werkbank gab bei gleicher Adresse keine Herkunft mit), Stand-Zahlen im Hafenbüro.

## Offen, mit Grund

- Werkbank lädt 8,5 bis 10 MB, bevor die Seite steht (Aussen-Prüfung gelb). Die meisten Bilder laden schon erst beim Hinscrollen; weniger geht nur mit einem Umbau der Werkbank, nicht beim Hochladen.
- Besuche werden nicht gezählt, solange die Adresse nicht im Dienst tasty-besuche (api/b.py, SEITEN) steht; für die Demo nicht nötig.
