---
tags: [projekt, website]
status: aktiv
---

# Das Hafenbüro (La Maison) · Demo-Check 21.10.2026

Chat «Demo-Check · Schlössli · Zentrale (La Maison)», nie daran gebaut. Massstab: gemeinsamer Auftrag `_Oberchef/zeigen/schloessli/democheck/AUFTRAG.md`, Werkzeug-Master 4.1 (M01–M27), 9, Fehlerbuch 10a.
Server: `python3 _werkzeuge/maison/server.py 8987` → http://127.0.0.1:8987/_werkzeuge/maison/

## Urteil

**Demo-bereit: ja.** Alle Wege grün, auch der Rückweg aus der Hausdruckerei (dort vom eigenen Demo-Check-Chat repariert, um 03:32 nachgeprüft: 200).

## Was geprüft wurde (bedient, nicht nur geladen)

Je Chromium und Safari-Kern (WebKit), je 1440 × 900 und 390 × 844 (Handy mit Tippen). Prüfläufe: `pruefung/pruefe.js` (72 Punkte je Browser) und neu `pruefung/democheck.js` (99 Punkte je Browser), Ergebnisse `pruefung/ergebnis-*.json`, `pruefung/democheck-*.json`.

| Weg | Ergebnis |
|---|---|
| Laden zweimal: Antwort 200, keine kaputten Bilder nach Durchscrollen, kein seitliches Verrutschen, Startfehler-Tür zu, alle Stücke aufgetreten, Konsole leer | grün, alle vier Kombinationen |
| Gruss morgen/tag/abend, Datum ausgeschrieben (de-CH, Zeitzone Zürich) | grün |
| Empfang: sechs Kacheln, Darüberfahren zeigt die Vorschau des richtigen Werkzeugs, nichts hüpft, Zeiger weg = Ruhebild, Tastatur-Fokus zeigt Vorschau; Handy: Bühne aus, Kacheln ganz im Bild | grün |
| Jede der sechs Kacheln geklickt bzw. getippt: Schaufenster 9035, Kartenpult 9031, Hausdruckerei 9053, Reservationsbuch 9047, Bildarchiv 9049, Besucherliste 8988 öffnen ohne Skriptfehler | grün |
| Taste 1 bis 6 öffnet das Werkzeug | grün |
| Stand je Werkzeug live: «Alles veröffentlicht» · «5 Karten, alle veröffentlicht» · «248 Vorlagen in 23 Arten» · «6 Anfragen offen · 1 Frage ohne Antwort · Beispiel» · «68 Fotos · 45 Dateien» · «789 Besuche in 30 Tagen · Beispiel»; Zahlenzeile «Heute 21 Besuche · 0 zur Reservation · Beispiel» | grün, gleiche Zahlen wie in den Werkzeugen |
| Werkzeuge antworten nicht: Sätze ohne Zahl, Zahlenzeile «–» | grün |
| Leiste: «Anleitungen» springt zum Fuss, Marke springt nach oben, «Website ansehen» öffnet die Website (ohne kaputte Bilder); Leiste kommt beim Hochscrollen zurück; Namen der Werkzeuge erst ab rund 1900 px Breite, sonst nur die Marke (M01, Fehlerbuch 19.10.) | grün |
| Goldband läuft nur im Bild | grün |
| Jeder Link der Seite (19 Adressen: sechs Werkzeuge, vier Anleitungen, Website, Prüfseite, Sprungziele) antwortet 200 | grün |
| Kein mailto/tel, kein Formular, nichts geht hinaus | grün |
| Rundgang: Schild «Kurzer Rundgang» erscheint, «Zeigen», fünf Schritte, Karte jedes Mal ganz im Bild, danach zu | grün |
| Weniger Bewegung: nichts verschoben | grün |
| Startfehler-Tür bei fehlendem Skript | grün |
| Aus jedem Werkzeug zurück ins Hafenbüro | Schaufenster, Kartenpult, Reservationsbuch, Bildarchiv, Besucherliste grün (nach Reparatur 1); Hausdruckerei zuerst 404 (`localhost:8982`), gemeldet, vom Chat der Hausdruckerei auf 8987 umgestellt und nachgeprüft: grün |
| Inhalt: Name, Adresse «Seestrasse 50, 8598 Bottighofen» wie `website/inhalt/haus.json`; keine Angabe eines anderen Hauses (grep über das Revier leer), kein Lorem, keine Platzhalter; Knopf-Namen der Tafeln vom Bau gegen den Code geprüft | grün |

## Was repariert wurde

1. **Hafenbüro aus einem anderen Werkzeug geöffnet stand ohne Zahlen.** Die Werkzeuge verlinken «Das Hafenbüro» über ihren eigenen Server (`127.0.0.1:9047/_werkzeuge/maison/` usw.); dort fehlen die Stand-Wege, also standen alle sechs Stand-Zeilen ohne Zahl, «– Besuche» und fünf Konsolenfehler. Jetzt leitet sich die lokale Stube auf 8987 um. `bau.py` (Konstante `ZUR_STUBE` vor `seite()`, eine Zeile im `<head>` nur der lokalen Fassung), neu gebaut; Online-Fassung unverändert. Nachgeprüft aus 9035, 9047, 9049, 8988: überall dieselben Zahlen, keine Fehler.
2. **Rundgang beschrieb eine andere Seite.** «Jede Zeile ist ein Werkzeug … Daneben steht …», «Fahren Sie über eine Zeile», «Diese Leiste führt in jedes Werkzeug» passte nicht zum Gebauten (Kacheln, Stand darunter, Leiste zeigt unter 1900 px nur die Marke). Wortlaut angepasst: «Jede Kachel ist ein Werkzeug … Darunter steht …», «Am Rechner zeigt das grosse Bild links, wie das Werkzeug aussieht, sobald Sie über eine Kachel fahren.», «Ein Klick auf diese Leiste bringt Sie von überall zurück zu den Werkzeugen. Aus jedem Werkzeug kommen Sie hierher zurück.» `bau.py` › `rundgang()`, neu gebaut.

Sicherungen: `bau.py`, `index.html`, `fassung-a/b/c.html`, `rundgang.js` je `*.vor-democheck-2026-10-21`. `bau.py` vorher in einer Kopie laufen lassen: baut Byte für Byte dieselbe Seite, die Neubauten ändern nur die zwei Stellen.

## Gemeldet an andere Reviere

- Demo-Check Hausdruckerei: alle Wege «Das Hafenbüro» zeigen auf `http://localhost:8982/_werkzeuge/maison/` (404). Richtig: `http://127.0.0.1:8987/_werkzeuge/maison/`. Erledigt, nachgeprüft.

## Messwert (Regel 55)

`pruefung/fluss.js`, Chromium, fertige Seite: CPU 4× · 1440: Bildabstand Mitte 8,3 ms, 95 % unter 9,3 ms, längstes 17,6 ms, kein Bild über 33 ms, Verschiebung 0,037, Gewicht 3,76 MB. CPU 4× · 390: Mitte 8,3 ms, 95 % 9,2 ms, ein Bild 50,6 ms, 2,73 MB. CPU 6× · 1440: ein Ausreisser 367 ms beim ersten Bildwechsel, sonst 95 % unter 16,7 ms.

## Bilder

`~/Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/maison/`: je Browser und Grösse Empfang (`*-1-empfang.png`), ganze Seite (`*-0-ganz.png`), Rundgang Schild + fünf Schritte, erstes geöffnetes Werkzeug.

## Nach dem Auftrag (stört die Demo nicht)

- «Zur Werkbank» erscheint im Hafenbüro nicht, wenn man aus der Werkbank kommt: Die Werkbank (8982) öffnet das Hafenbüro (8987) im neuen Reiter, gibt aber keine Herkunft mit (`zur-werkbank.js` hängt `wb=` nur an Links auf dieselbe Adresse). Die Werkbank bleibt im ersten Reiter offen, so wie bei den abgenommenen Häusern; der Fuss hat dort auch keinen Weg «Zur Werkbank» (M10). Für den Betrieb online klären.
- Zahlenzeile «0 zur Reservation» am Abend: richtig gerechnet (Tageswert der Beispielwerte, M14), wirkt in der Vorführung aber mager.
- Kachel «reserviert» im Saal der Besucherliste zeigt als Wert nur «·» (gewollt: zählen gastronovi und das Haus). Ein Wort statt Punkt wäre klarer.
- Bei CPU 6× ein langes Bild beim ersten Vorschauwechsel (367 ms).
- Rundgang Schritt 3 am Handy: zeigt auf die Kacheln, der Satz spricht vom Rechner.
