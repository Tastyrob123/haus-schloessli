---
tags: [projekt, website]
status: aktiv
---

# Das Hafenbüro (Zentrale, Arbeitsname La Maison) · Wirtschaft am Schlössli · Funktionsliste (Nachtbau 3./4.11.2026)

Aufbau und Funktionen wie die Zentrale der Häuser (Master Werkzeug-Bau 3, R01–R24, und 4.1, M01–M27), Inhalt und Kleid des Schlössli. Beleg je Zeile: Code (`bau.py`, `quelle/maison.js`) und die schnelle Prüfung (`_Werkzeuge/abnahme-tor/tor-schnell.js … --nur tresen`, Chromium, 1440/1280/1000/390).

| Nr | Stand im Schlössli |
|---|---|
| R01 Aufbau | Leiste (Insel mit den Zeigern im Ring), Empfang mit fünf Fenstern, sechs Säle, Fuss, Startfehler-Tür |
| R03 Fehlermelder | `fehler.js` vor allem anderen, Schlüssel `schloessli_werkzeuge_fehler`, höchstens 20, Netzfehler nie |
| R04 Startfehler-Tür | «Das Hafenbüro startet nicht.» mit Grund, «Prüfung öffnen» (Prüfseite des Schaufensters, nur lokal), «Neu laden» |
| R05 Kopfleiste | Insel mit Zeichen und Name, sechs Werkzeuge (nur, wenn sie ganz Platz haben), Eck-Knöpfe «Anleitungen», «Website ansehen» (Website des Schlössli auf 9281) |
| R07 Handy | Fenster als Bänder untereinander, kein seitliches Verrutschen |
| R17 Bewegung | Fenster schweben gestaffelt, Fotos zoomen ein, Titel Zeile für Zeile, Horizont zieht sich auf, Zahlen laufen hoch; nur transform/opacity; «Weniger Bewegung» beachtet |
| R18 Rundgang | fünf Schritte in Sie-Form, Schlüssel `rundgang-schloessli-maison`, `?rundgang` |
| R19 Zur Werkbank | `zur-werkbank.js`, Schlüssel `schloessli-wb` |
| R20 / M27 Beispiele | Besucherliste und Reservationsbuch mit Beispielwerten, «Besuchszahlen als Beispiel» leise in der Datumszeile |
| M03 Gruss, Datum | nach Tageszeit (`?gruss=morgen|tag|abend`), Datum ausgeschrieben |
| M04 Empfang | fünf hohe Fenster mit Fotos des Hauses (`platanen`, `anguria`, `morgen`, `jonas`, `abend` aus `website/inhalt/bilder.json`), darüber Wortmarke, «by Christian Kuchler · Seestrasse 50 · 8598 Bottighofen» (aus `haus.json`), der Name der Zentrale auf dem Horizont |
| M05 Stand je Werkzeug, live | über `/_weiter/<werkzeug>/…` von `server.py` (Wege in `stand_wege.json`); ohne Antwort der Satz aus `bau.py` |
| M06 Zahlenzeile | «Heute X Besuche · Y zur Reservation · Die Besucherliste öffnen» |
| M07 Laufband | Namen der Werkzeuge, Wirtschaft am Schlössli, Lästermeile, Adresse |
| M08 Säle mit echten Bildschirmen | aus `roh/` (aufgenommen mit `schirme.js`, Chromium oder WebKit, 1440 × 932 @2x) |
| M09 Stücke | drei Seiten der Karten (Lästermeile, Lunch, Speisekarte), Drucksache der Hausdruckerei, sechs Fotos im Saal des Markenbuchs, zwölf Hausfarben aus `livre/livre.json` |
| M10 Fuss | Zeiger und Wortmarke, das Haus (Adresse, Telefon aus `haus.json`), alle sechs Anleitungen, Fragen |
| M12 Taste 1–6 | öffnet das Werkzeug |
| M13 Zwei Fassungen | `online/` ohne localhost und ohne Platzhalter (Bau bricht sonst ab) |
| M20 Knopf-Namen | jede «…»-Angabe der Tafeln (`tafeln.json`) gegen den Code des Werkzeugs geprüft (`knoepfe()`) |
| M24 Ecke oben links | die Zeiger im Ring, Name, «Alle Werkzeuge · Wirtschaft am Schlössli» |
