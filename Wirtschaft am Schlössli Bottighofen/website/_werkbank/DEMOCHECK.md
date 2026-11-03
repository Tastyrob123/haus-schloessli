---
tags: [projekt, website]
status: aktiv
---

# Wirtschaft am Schlössli · Demo-Check der Werkbank (21.10.2026, ~02:55–04:15)

**Urteil: demo-bereit — ja.** Jeder sichtbare Weg der Werkbank und ihrer Beigaben ist in Chromium und WebKit, bei 1440 × 900 und 390 × 844 (Handy mit Tippen) bedient und grün. 7 Funde, alle repariert und nachgeprüft.

Ansehen: http://127.0.0.1:8982/werkbank/index.html (Server `python3 website/serve.py 8982`, launch.json «schloessli-bottighofen»).
Bilder: `~/Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/werkbank/` (je Browser und Grösse ein Ordner mit jedem Abschnitt, Tafeln, Vorher/Nachher der Reparaturen).
Massstab: Website-Master «Vor dem Pitch: Demo-Check» 1–4 und Werkbank-Regeln 1–17, gemeinsamer Auftrag `_Oberchef/zeigen/schloessli/democheck/AUFTRAG.md`. Prüfskripte (Playwright, headless, eine Instanz zugleich) liegen im Scratchpad der Sitzung; mailto/tel/window.open und Formular-Absenden waren in jedem Lauf abgefangen.

## Was geprüft wurde, Weg für Weg

| Weg | Chromium 1440 | Chromium 390 | WebKit 1440 | WebKit 390 |
|---|---|---|---|---|
| Werkbank `werkbank/index.html`, alle 22 Abschnitte von oben bis unten, je Abschnitt ein Bild | grün | grün | grün | grün |
| Jeder Knopf der Werkbank angeklickt bzw. angetippt (82 am Rechner, 75 am Handy; nur die zwei «Zurück» am Bandanfang sind absichtlich gesperrt) | grün | grün | grün | grün |
| Bänder: seitlich wischen, Pfeile; Mausrad über jedem Band läuft an die Seite weiter (Regel 1), keine Kachel mit eigenem senkrechtem Scrollen | grün | grün | grün | grün |
| Jedes Band bei Anfang und Ende ganz erreichbar | grün | grün nach Reparatur 5/6 | grün | grün nach Reparatur 5/6 |
| Seiten-Kapitel: alle 10 Reiter, je Reiter «Öffnen» auf die echte Seite (index, karte, weinkarte, feiern, anlaesse, team, kontakt, gutschein, abend, impressum) | grün | – | grün | – |
| Werkzeug-Kapitel: alle 7 Reiter, je Werkzeug «… öffnen» → neues Fenster mit dem laufenden Werkzeug (8987, 9035, 9031, 9047, 9049, 8988, 9053), Titel richtig | grün | grün | grün | grün |
| Bildschirme der Werkzeuge in der Werkbank gegen die laufenden Werkzeuge gelegt (`werkzeug-bildschirme-werkbank-gegen-live.jpg`): alle sieben zeigen den heutigen Stand | grün | | | |
| `werkbank/ki.html`, `karte.html` («Ein Vorschlag.»), `impressum.html`, `geprueft/index.html` | grün | grün | grün | grün |
| Vorschlag als PDF (2 Seiten), neu gedruckt und angesehen | grün | | | |
| Potenzialanalyse (13 Knöpfe), Unterlagen (7/9 Knöpfe), Drucksachen, Untersetzer, Feed (21 Beiträge, Mausrad über dem Telefon läuft an die Seite weiter), Mails (Übersicht + 3 Mails), Material | grün | grün | grün | grün |
| Alle 391 Verweise und Bilder der 15 Seiten (Server-Antwort 200), alle 25 PDFs geöffnet und gelesen | grün | | | |
| Konsolenfehler, seitliches Überlaufen, kaputte Bilder, POST-Anfragen, mailto/tel | 0 | 0 | 0 | 0 |

**Inhalt gegen die Quelle:**
- Befund (Kapitel I): die vier Funde = die ersten vier der heutigen Potenzialanalyse, «Alle 13 Funde» stimmt (13 in der Analyse).
- Zahlen: 9 Seiten (Website hat 9 + Rechtliches), 7 Werkzeuge, 5 Karten, 6 Drucksachen (6 PDFs), 12 Untersetzer (12 Seiten im PDF), 3 Mails, 21 Beiträge (feed.json), 68 Fotos im Bildarchiv (livre.json) — überall gleich.
- Karten-PDFs der Unterlagen gegen die Original-PDFs des Hauses (`_quelle/website/pdf/`): alle Preise gleich (Weinkarte 495 = 495, Speisekarte, Bankett, Lunch, Lästermeile; einziger Mehr-Wert ist die Hausnummer 50 der Adresse).
- Fremde Häuser: nur das Schäfli als gewolltes Schwesterhaus (Ideen-Kapitel, Über uns, Gutschein für beide Häuser, Analyse). Kein Koh Phangan, kein Lorem, kein mailto-Link.
- Preise: nur die Betreuung CHF 200 im Monat (Roberts Entscheid 20.10.2026, `Angebot.md`), der Bau ohne Betrag mit Satz «Den Betrag nennen Sie». KI-Kosten nur auf `ki.html`, ohne Beträge. Kein Drängen zum Gespräch, kein Angebot vorbeizukommen.

**Flüssig (Chromium, CPU 4× gebremst, zweiter Durchgang, Rechner mit Last 61 durch die parallelen Chats):** Werkbank 1440: 68 Bilder/s im Mittel, 95 % der Bilder unter 25 ms, Springen 0. Handy 390: 68 Bilder/s, 95 % unter 17 ms, Springen 0. Einzelne längere Stockungen wanderten von Lauf zu Lauf an andere Stellen (Last des Rechners, nicht der Seite).

## Was repariert wurde

Sicherungen je Datei als `*.vor-democheck-2026-10-21`, Bilder in `_werkbank/_sicherung-vor-democheck-2026-10-21/`.

1. **Prüfbericht-Blatt (Kapitel VII):** am Handy lagen die Bildchen über dem Text, am Rechner rutschte der Haken unter das Bild. `werkbank/werkbank.css:1275` und Quelle `_werkbank/geprueft_blatt.py:52`: `.gb-blatt .gb-l li{display:flex…}` (vorher von einer späteren allgemeinen Regel überschrieben). Bild: `fix-pruefbericht-blatt-1440-390.jpg`.
2. **Ort auf «Ein Vorschlag.»:** «Bottighofen, 20. Oktober 2026» → «Hamburg, 20. Oktober 2026» (Werkbank-Regel 10). `werkbank/index.html:500`, `werkbank/karte.html:32`, Quelle `_werkbank/sb_angebot.py:21`; PDF `werkbank/vorschlag-wirtschaft-am-schloessli.pdf` mit `_werkbank/_karte_pdf.js` neu gedruckt. Bild: `fix-vorschlag-pdf-vorher-nachher.png`.
3. **Seiten-Kapitel «Über uns»** zeigte noch Monika links, Jonas in der Mitte (Website seit 20.10. 23:40 umgekehrt). Seite neu aufgenommen (`_Werkbank-Kit/ansicht.js … team.html`), `werkbank/img/ueber-uns-1..3.webp`, `ueber-uns-h, -h2, -h3.webp` neu, ebenso `material/05 Ansichten der neuen Website/{Rechner,Handy}/Über uns*.jpg`. Bild: `fix-seiten-ueber-uns-1440-webkit.jpg`.
4. **Impressum der Werkbank** nannte die Werkzeug-Namen einer Vorlage (Die Stube, Der Schreibtisch, Die Tafel …) und einen Chat «auf der Website». Jetzt die Namen des Hauses (Hafenbüro, Schaufenster, Kartenpult, Reservationsbuch, Bildarchiv, Besucherliste, Hausdruckerei) und «Das Reservationsbuch des Entwurfs enthält einen Chat zum Ausprobieren». `werkbank/impressum.html`, Quelle `_werkbank/rh_impressum.py:24–25`.
5. **Werkzeug-Kapitel am Handy:** die Reiter «Das Hafenbüro» und «Das Schaufenster» lagen links ausserhalb der Leiste und waren weder sichtbar noch erreichbar. `werkbank/kapitel.css:238` und Quelle `_werkbank/rh_werkzeuge.py`: `justify-content:flex-start` in der Handy-Regel. Bild: `fix-werkzeug-reiter-390-chromium.jpg`.
6. **«Heute und neu» am Handy:** Reiter «Startseite» links abgeschnitten. `werkbank/werkbank.css:1366` und Quelle `_werkbank/haus.py:354`: Mittig nur noch ab 760 px.
7. **Prüfbericht-Seite `werkbank/geprueft/index.html`:** Hintergrundmuster 404 (Variable mit relativem Pfad), dazu im Text «Ihre Zimmer» und «Booking» bei einem Restaurant. Muster-Pfad im eigenen `<style>` der Seite gesetzt; Sätze jetzt «Ihre Karten, Anlässe und Angebote», «Adresse, Telefon, Reservation, Karten und Öffnungszeiten», «Tripadvisor, im Guide Michelin, bei GaultMillau und den anderen Portalen». Der Text kommt aus `_Werkbank-Kit/bau.py:225–227` (geteilt, nicht angefasst, siehe unten).

Danach ganzer Durchgang wiederholt: alles grün.

## An andere Chats gemeldet

- Kartenpult, Besucherliste, Hausdruckerei, Schaufenster: «Zur Werkbank» in den Werkzeugen zeigt auf den eigenen Port (`…:9031/werkbank/…` usw., 404), im Schaufenster fehlt der Knopf. Nachgeprüft: Über den echten Weg (Klick in der Werkbank, neues Fenster) erscheint der Knopf in keinem Werkzeug, die Werkbank bleibt im ersten Fenster offen. Stört die Demo nicht; als «Nach dem Auftrag» gemeldet. Kartenpult inzwischen behoben (Knopf zeigt auf `http://127.0.0.1:8982/werkbank/index.html#k5`, von hier aus nachgeprüft 21.10.2026). Das Hafenbüro-Chat war schon abgeschlossen (Nachricht nicht zugestellt), es hat denselben Punkt selbst in seinem DEMOCHECK.md (Zeile 59).

## Nach dem Auftrag

- `_Werkbank-Kit/bau.py:225–227` schreibt in jeden Prüfbericht «Ihre Zimmer» und «Booking»; für Restaurants je Haus anpassbar machen (hier nur im Ergebnis geändert, ein Neubau mit dem Kit holt die alten Sätze zurück).
- Die Reparaturen 1–6 stehen auch in den Quellen; 3 (Aufnahmen) und 7 (Prüfbericht-Seite) nur im Ergebnis bzw. in den Ansichten. Vor einem Neubau der Werkbank diese Liste lesen.
- Kommentare im Code der Werkbank nennen Vorlagen («Werkbank Carlton-Europe», «Grand Beau-Rivage», «Ruedihus», «Doldenhorn» in `werkbank.js`, `werkbank.css`, `kapitel.css`, `index.html`). Unsichtbar auf der Seite, aber im Quelltext lesbar, sobald die Werkbank online liegt; vor dem Hochladen herausnehmen.
- «Zur Werkbank» aus den Werkzeugen (siehe oben), wenn die Werkbank online mit den Werkzeugen unter einer Adresse läuft, nachprüfen.
- Die Schäfli-Werkbank trägt auf «Ein Vorschlag.» «Wigoltingen, 21. Oktober 2026» (gleicher Fehler wie hier Nummer 2, nicht mein Revier, an den Oberchef).
- Bildrate auf einem ruhigen Rechner noch einmal messen (heute Last 61).
- Im Text heisst die Küchenchefin «Monika Huber», auf der Seite «Über uns» im Fliesstext «Moni Huber»; beides kommt aus den Quellen, nur angleichen, wenn das Haus es so will.

## Lernprotokoll

Regeln für alle Häuser eingetragen im Website-Master, Abschnitt 11, Eintrag «21.10.2026 ~04:00 · Wirtschaft am Schlössli, Demo-Check der Werkbank».
