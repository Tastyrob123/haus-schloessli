---
tags: [projekt, website]
status: aktiv
---

# Wirtschaft am Schlössli · Demo-Check der Website (21.10.2026)

**Urteil: demo-bereit, ja.** Geprüft von einem Chat, der nie an der Website gebaut hat, nach dem gemeinsamen Auftrag `_Oberchef/zeigen/schloessli/democheck/AUFTRAG.md`. Nur lokal (http://127.0.0.1:8982/), nichts online gestellt, nichts verschickt.
Bilder: `~/Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/website/` (je Seite 1440 und 390, dazu jedes Fenster vor und nach dem Absenden, Menü, Buchungsmaske, Weinberater; Übersicht `_tafel-1440.jpg`, `_tafel-390.jpg`).

## Was geprüft wurde

| Weg | Chromium 1440 | Chromium 390 | WebKit 1440 | WebKit 390 |
|---|---|---|---|---|
| 13 Seiten ganz durchgescrollt wie ein Gast (Startseite, Ihr Abend, Events, Feiern, Karte, Weinkarte, Gutschein, Kontakt, Team, Impressum, Datenschutz, AGB, 404), `_qa/pruefen.js` | grün | grün | grün | grün |
| Seitliches Überlaufen | 0 px überall | 0 px | 0 px | 0 px |
| Konsolenfehler, fehlgeschlagene Abrufe | keine | keine | keine | keine |
| Auftritte: jedes Stück am Ende sichtbar | ja | ja | ja | ja |
| Reservation (Fenster): öffnen, ausfüllen, absenden, Dank mit «Designstudie: Diese Anfrage wurde nicht verschickt», schliessen | grün | grün (Tippen) | grün | grün (Tippen) |
| Reservation, Reiter «Direkt buchen»: Buchungsmaske von gastronovi lädt im Fenster (nach 2 bis 4 s, Personen, Kalender) | grün | – | – | grün |
| Bankettanfrage (feiern.html), Gutschein-Fenster: öffnen, absenden, Dank, schliessen | grün | grün | grün | grün |
| Menü «Speisefolge» öffnen, schliessen (Escape und Knopf), 11 Wege, Link folgt (auch «Tisch» öffnet das Reservations-Fenster) | grün | grün | grün | grün |
| Events: vier Rückblick-Knöpfe und Weiter-Pfeil wechseln den Anlass | grün | grün | grün | grün |
| Weinkarte: Wein-Fenster, «Zur Reservierung bereitlegen» trägt die Flasche ins Reservations-Fenster; Weinberater «Nach Geschmack» mit 13 Aromabildern | grün | – | – | grün |
| Interne Links und Sprungmarken (alle Seiten, alle `#…`) | alle vorhanden | | | |
| Fünf Karten-PDFs (Speisekarte, Lunch, Lästermeile, Bankett, Weinkarte): laden, Inhalt = heutige Karte, Schriften ohne «Type 3» | grün | | | |
| Nichts geht raus: kein `mailto` auf der ganzen Website; im Test ging kein POST an fremde Adressen, kein Fenster/Programm öffnete sich | grün | grün | grün | grün |

**Inhalt gegen das Original** (`_quelle/website/text/kontakt.md`, `uber-uns.md`, `impressum.md`, Karten-JSON): Name, Seestrasse 50, 8598 Bottighofen, +41 71 688 90 92, kontakt@schloessli-bottighofen.ch, Donnerstag bis Montag 11:30 bis 23:00 Uhr, Küche 11:30 bis 13:30 und 18:00 bis 20:00 Uhr, Dienstag und Mittwoch Ruhetag, Ferien 13. bis 15. November und 22. Dezember 2026 bis 10. Februar 2027, Team (Jonas Volpert, Monika Huber, Lukas Siebel, Marco Reisinger, Ole Sass), Gerichte und Preise der Karte, Lunch 35 Franken: stimmen. Schwesterhaus im Fuss (Oberdorfstrasse 8, 8556 Wigoltingen, +41 52 763 11 72, Mittwoch bis Samstag) stimmt mit `Taverne zum Schäfli Wigoltingen/website/inhalt/haus.py`.
**Fremde Häuser (grep):** Treffer nur gewollt: Schäfli/Wigoltingen im Fuss «Zwei Häuser der Familie Kuchler», auf team.html (#schaefli), im Gutschein («In beiden Häusern»), auf anlaesse.html (Kitchen Party im Schäfli) und im Impressum/Datenschutz (Firmensitz CK Gastro Consulting GmbH, Oberdorfstrasse 8, Wigoltingen, wörtlich aus dem Original). «GBR» nur zufällig in eingebetteten Bilddaten. Kein Rivage, Maeder, Carlton, Koh Phangan, kein Lorem, keine Platzhalter, keine Beispielpreise.

## Messwert (Regel 55, CPU 4× gedrosselt, Leitung gedrosselt)

| Seite | Breite | schwächster Abschnitt | CLS |
|---|---|---|---|
| Startseite | 1440 | 97 Bilder/s (Feiern) | 0 |
| Startseite | 390 | 99 Bilder/s (Feiern) | 0 |
| Events | 1440 | 116 Bilder/s | 0 |
| Weinkarte | 390 | 99 Bilder/s (Weinliste) | 0 |

Ein erster Lauf zeigte im Abschnitt Feiern der Startseite einmal 74 Bilder/s mit zwei langen Bildern; zwei weitere Läufe 97 und 99, also ein Ausreisser.

## Was repariert wurde

1. **Ferien auf der Startseite** standen als «13. - 15. November … · 22. Dezember 2026 - 10. Februar 2027» (Bindestrich aus dem Original), überall sonst «bis». Jetzt «13. bis 15. November (Excellence Gourmetkreuzfahrt) · 22. Dezember 2026 bis 10. Februar 2027». `website/bau.py` Zeile 528 (`f.replace(' - ', ' bis ')`), `index.html` neu gebaut.
2. **Kontakt-Kopf** stand als «Donnerstag - Montag · 11:30 Uhr - 23:00 Uhr». Jetzt «Donnerstag bis Montag · 11:30 bis 23:00 Uhr» wie im Rest der Seite. `website/bau.py` Zeile 928, `kontakt.html` neu gebaut.

Vorher geprüft: ein Neubau mit `python3 bau.py` ergibt vor der Änderung exakt die heutigen Seiten; nach der Änderung unterscheiden sich nur `index.html` und `kontakt.html`, je nur an dieser Stelle. Sicherungen: `bau.py.vor-democheck-2026-10-21`, `index.html.vor-democheck-2026-10-21`, `kontakt.html.vor-democheck-2026-10-21`. Nachgeprüft: Startseite WebKit 390 und Kontakt Chromium 1440 / WebKit 390 ohne Fehler, kein Überlauf.

## Für das Hochladen (Chat demo-kuchler-online)

- Die beiden Knöpfe «Zum Haus» und das Hausbild im Fuss beim Schäfli zeigen auf `http://127.0.0.1:8953/` (die lokale Schäfli-Studie, `fuss_bau.py` Zeile 9). Online muss dort die Adresse der hochgeladenen Schäfli-Studie stehen, sonst führt der Weg ins Leere. Danach `python3 bau.py`.
- «Direkt buchen» ist die echte Buchungsmaske des Hauses (gastronovi). Wer dort bucht, bucht wirklich; so steht es auch auf der heutigen Seite des Hauses und war so gewollt (Buchungsmasken bleiben).

## Nach dem Auftrag

- Rechte vor jeder echten Veröffentlichung: Gästefotos (Tripadvisor), Excellence-Bilder, Feuerwerk «Bildrecht Keller», Heft-Bilder der Gemeinde, Gemeindewappen, Vivino-Bilder und -Daten, Weingut-Logos (Liste in `UEBERGABE.md`).
- Ferien «13. bis 15. November» ohne Jahr, wie im Original; bei der nächsten Pflege Jahr ergänzen.
- Abschnitt Feiern auf der Startseite im Auge behalten (einmal 74 Bilder/s, sonst 97 bis 99).
- `_qa/funktionen.js` prüft noch den alten Kalender und den alten Menü-Knopf (`data-menue`), die es nicht mehr gibt; Prüfskript auf Speisefolge (`data-sf-auf`) und Rückblick (`data-kbg`) umstellen.
- Die Buchungsmaske ist zwei bis vier Sekunden weiss, bis gastronovi lädt; ein ruhiger Ladehinweis im Rahmen wäre schöner.
