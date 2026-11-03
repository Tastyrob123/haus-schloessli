---
tags: [projekt, website]
status: aktiv
---

# Demo-Check · Das Schaufenster (Le Bureau) · Wirtschaft am Schlössli · 21.10.2026

Unabhängiger Chat, nie daran gebaut. Auftrag: `_Oberchef/zeigen/schloessli/democheck/AUFTRAG.md`. Massstab: Website-Bau-Master «Vor dem Pitch: Demo-Check» 1–4, Werkzeug-Master 3, 4.2, 9, 10a.

**Urteil: demo-bereit, ja.**

Adresse der Demo: http://127.0.0.1:9035/_werkzeuge/bureau/ (Server neu gestartet 21.10.2026 ~03:50, echte Daten, damit die Reparaturen gelten). Prüfseite: http://127.0.0.1:9035/werkzeuge/website/pruefung.html?haus=schloessli

## Wie geprüft

- `democheck/democheck.js <chromium|webkit> <1440|390>`: eigener Server (Port 9121) mit Wegwerf-Daten und Wegwerf-Kopie der Seiten, Browser unsichtbar, mailto/tel abgefangen. Am Handy (390 × 844) Tippen statt Klicken (Chromium mit Handy-Nachbildung; Safari-Kern siehe unten). Prüfsummen der Website des Hauses (`website/*.html|css|js|json`) und der echten Daten (`_Werkzeuge/daten/schloessli`) vor und nach jedem Lauf.
- Gegenprobe mit dem festen Lauf des Stamms im Rahmen des Hauses (`pruef.js`, RAHMEN=1): `democheck/lauf-stamm-pruef.log`.
- Gedrosselt gemessen mit `fluss.js` gegen :9035: `democheck/fluss.json`.
- Bilder je Ansicht, je Motor, je Grösse: `~/Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/bureau/` (01 Übersicht … 17 Website ansehen).

| Lauf | Ergebnis |
|---|---|
| democheck.js Chromium 1440 | BESTANDEN 136/136 (`democheck/lauf-chromium-1440.log`) |
| democheck.js Chromium 390 | BESTANDEN 150/150 |
| democheck.js Safari-Kern 1440 | BESTANDEN 136/136 |
| democheck.js Safari-Kern 390 | BESTANDEN 150/150 |
| pruef.js (Stamm) Chromium 1440 / 390, Safari-Kern 1440 / 390 | je BESTANDEN 148/148 (vor der Reparatur: 3–4 rot, Anlässe und Abbruch am Handy) |

## Was geprüft ist, Weg für Weg (jeder in beiden Browsern und beiden Grössen bedient)

1. **Übersicht:** Kopf mit «Das Schaufenster», Startbild, Lage-Platte (Entwurf, Website, Kartenpult), «Häufig gebraucht» (6 Kacheln, jede öffnet ihre Ansicht, «Gericht oder Preis» führt zum Kartenpult), «Die Website, Bereich für Bereich» (7 Kacheln mit Foto, jede öffnet ihren Bereich). Kein seitliches Verrutschen.
2. **Rand:** alle 15 Einträge öffnen ihre Ansicht; am Handy Knopf «Bereiche», schliesst nach der Wahl.
3. **Sieben Bereiche der Website:** Vorschau lädt, Stellen-Liste gefüllt, jede Seite eines Bereichs über die Reiter (Karte & Wein 2, Kontakt & Gutschein 2, Rechtliches 3), Suche filtert.
4. **Text ändern:** Klick (Handy: Tippen) auf einen Text in der Vorschau öffnet das Feld, Tippen schreibt sofort in der Vorschau mit, Speichern-Knopf gelb, Quittung, Speichern → neu laden → noch da, Speichern ändert die Website noch nicht.
5. **Rückgängig** aus der Quittung nimmt die Änderung zurück.
6. **Zeiten & Preise:** Filter Alle / Preise / Zeiten / Grössen und Dauer, Suche, Wert ändern und speichern, «In der Seite» springt in den Bereich.
7. **Foto tauschen:** Fenster mit 72 Fotos des Hauses, ganze Kacheln (Fehlerbuch), Wahl und Speichern landen im Entwurf.
8. **Anlässe:** Eintrag mit Foto, aufklappen, «Ausblenden» → Entwurf, «Wieder zeigen» nimmt es zurück. **Team:** fünf Einträge mit Foto bzw. Initialen (zwei Menschen haben auf der Website kein Foto).
9. **Hinweis für Gäste:** ein-/ausschalten, Text, Ab/Bis, speichern → Entwurf.
10. **Entwurf & Vergleich:** Liste vorher/nachher, «Vorher, nachher» öffnet den Vergleich, einzelne Änderung «Zurücknehmen», «Entwurf verwerfen» mit Bestätigung.
11. **Veröffentlichen** (nur in die Wegwerf-Kopie): Fenster mit Liste und Notiz, «Ist online.», die Kopie zeigt den neuen Stand, «Website ansehen» liefert ihn.
12. **Frühere Fassungen:** mit «Ursprünglicher Stand» unten; Zurückholen legt in den Entwurf (Website bleibt), erneut veröffentlicht → alle 11 Seiten Byte für Byte wie vorher.
13. **Wege:** Kopf-Knöpfe Hafenbüro (→ :8987, 200), Prüfung, Website ansehen; Kartenpult (→ :9031, 200); kein mailto/tel im Werkzeug, keine Anfrage an fremde Server, keine Antwort 4xx/5xx, keine Konsolenfehler.
14. **Prüfseite:** alle 16 Punkte in Ordnung, Name des Hauses, «Zum Werkzeug» zurück ins Schaufenster.
15. **Kopf-Titel** «Kontakt & Gutschein» überdeckt bei 920 / 1000 / 1100 / 1240 px keinen Knopf (Fehlerbuch).
16. **Demo-Daten:** Änderungen landen nur im Speicher des Werkzeugs und in der Probe-Kopie `_Werkzeuge/werkzeuge/website/_probe/schloessli/online/`; die Website des Hauses (`website/`) wird nie geschrieben (Prüfsummen vorher/nachher gleich in allen Läufen; `ausgabe.py` schreibt nur in die Probe-Kopie). Nach dem Check: echte Daten unverändert (leer, wie gebaut), Probe-Kopie = Grundlage.

**Inhalt:** Revier nach fremden Häusern durchsucht (Rivage, Interlaken, Wigoltingen, Schäfli, Maeder, Carlton …): nur Herkunftsvermerke in Kommentaren von `schweben.*`/`serve.py`. Texte des Werkzeugs (Sätze der Bereiche) gegen die Seiten abgeglichen; der Satz zu «Events & Termine» nannte noch «alle Termine des Jahres», die es auf der Seite nicht mehr gibt (berichtigt).

## Was repariert ist

| Fund | Datei, Stelle | Sicherung |
|---|---|---|
| **Anlässe fand seine Einträge nicht mehr** (Seite am 20.10. neu gebaut, der Jahreskalender `#kalender` ist weg): Liste fast leer, Prüfseite rot («trifft nichts»). Jetzt die grosse Ankündigung (`#naechster`) als Eintrag mit Titel, Ort/Datum, Namen, Text, Zeit, Fotos; Sätze von Bereich und Kachel an die Seite angepasst. Der Rückblick taugt nicht als Liste (siehe «Nach dem Auftrag»). | `_Werkzeuge/werkzeuge/website/haeuser/schloessli.json` › `bereiche.anlaesse`, `website[anlaesse].satz` | `schloessli.json.vor-democheck-2026-10-21` |
| **Prüfseite im Look des Stamms:** Titel «Prüfung · Der Schreibtisch», Knopf «Grandhotel» (Weltwechsel des Stamms), «Zum Werkzeug» führte in den Stamm ohne Rahmen. Jetzt «Prüfung · Das Schaufenster» im Kleid des Hauses, ohne Weltknopf, zurück ins Schaufenster. Die Datei des Stamms bleibt unverändert, der Server des Hauses setzt Kopf und Stile ein. | `serve.py` › `_pruefseite()` und Weg in `_bedien`; neu `pruefung-haus.css`, `pruefung-haus.js` | `serve.py.vor-democheck-2026-10-21` |
| Bereich-Kacheln der Übersicht ohne Foto (Fehlerbuch 10a, am Schäfli gefunden «am Schlössli genauso») | `bureau.css` (Raster des Rahmens für `.wo-bk.ws-bk`) | `bureau.css.vor-democheck-2026-10-21` |
| Unter dem Startbild nur 28 px Luft (Fehlerbuch: mindestens 30) → 36 px, Handy 28 | `bureau.css` `.ws-titel--wo` | dieselbe |
| Leiste mit ausgegrauten Knöpfen «Vorher, nachher» / «Veröffentlichen» ohne Entwurf (Fehlerbuch) → Schalter `leiste_klar` des Stamms eingeschaltet | `schloessli.json` › `funktionen` | wie oben |
| Einzige Anlass-Karte stand über die volle Breite, Foto 1070 px breit und unscharf → so gross wie eine Karte der Dreierreihe, mittig; Ausschnitt des hochkant fotografierten Tellers sass auf weisser Fläche → auf dem Teller | `bureau.css` (`.ws-eintrag:only-child`, `img[src*="/kf-teller-"]`) | `bureau.css…` |
| Knopf «Veröffentlichen» im Startbild der Entwurf-Ansicht: Schrift klebte am linken Rand und war grösser als die Knöpfe daneben → Abstand 20 px, Schrift wie die Rahmen-Knöpfe | `bureau.css` `.ws-titel--wo .kn` | `bureau.css…` |
| Kacheln 4 + 2 («Häufig gebraucht») und 3 + 3 + 1 (Bereiche, eine allein) → 3 + 3 und 3 + 2 + 2 mittig, zwischen 701 und 1100 px letzte Kachel mittig (Fehlerbuch «gleichmässig verteilen») | `bureau.css` (Ende) | `bureau.css…` |
| Tippen auf Texte der Vorschau am iPhone/iPad: Safari löst bei Elementen ohne Klick-Merkmal keinen Klick aus, wenn der Hörer am Dokument sitzt. Abhilfe: auf Geräten ohne Maus tragen Texte und Fotos der Vorschau `cursor:pointer`. **Am echten iPhone ungeprüft** (der Safari-Kern auf dem Mac erzeugt aus Tippen nie einen Klick, dort mit Klick geprüft: 11 von 12 Stellen, die zwölfte liegt unter dem Foto eines Fensters und ist über die Liste erreichbar). | `schloessli.json` › `vorschau.zusatz_css` | wie oben |
| **Zeiten & Preise zeigte die Öffnungszeiten des Schäfli** (Karte der Schwester im Fuss jeder Seite) als zweites «Offen» neben denen des Schlössli (Nachtrag auf Wunsch des Oberchefs). Die Schwesterkarte `.fz__h.b` wird im Schaufenster nicht mehr als Stelle angeboten; nur Einstellung des Schlössli, Stamm unverändert, Seiten bleiben Byte für Byte gleich (Prüfseite grün). Jetzt 12 Angaben, keine des Schäfli. Nachgeprüft Chromium 1440 136/136, Safari-Kern 390 150/150. | `schloessli.json` › `auslassen` | wie oben |
| `index.html`: Stilfassung `bureau.css?v=2` | `index.html` Zeile 18 | `index.html.vor-democheck-2026-10-21` |

## Messwert (gedrosselt, Chromium, `fluss.json`, Rechnerlast 75 durch andere Chats)

| Drosselung | Öffnen | Scrollen Übersicht (Bildabstand p95 / längster) | Bereich: Liste / Seite in der Vorschau | Zeiten & Preise |
|---|---|---|---|---|
| 1× | 568 ms | 9,1 / 9,3 ms | 125 / 363 ms | 465 ms |
| 4× | 530 ms | 9,2 / 9,3 ms | 227 / 850 ms | 1186 ms |
| 6× | 891 ms | 9,1 / 16,8 ms | 334 / 599 ms | 1566 ms |

Scrollen bei 4× rund 110 Bilder pro Sekunde, flüssig.

## Nach dem Auftrag (stört die Demo nicht)

- **Rückblick auf «Events & Termine»** (Ehemaligen Lunch, Seenachtfest, Kitchen Party, 4-Hands-Lunch): ausser dem ersten Blatt tragen alle Blätter `aria-hidden`, die Schicht des Stamms liest dort keinen Text. Diese Termine sind im Schaufenster nicht änderbar (nur das erste Blatt über den Bereich). Entweder Website ohne `aria-hidden` im Quelltext (Skript setzt es erst im Browser) oder Stamm liest auch verborgene Blätter.
- Prüfseite: Texte des Stamms erwähnen noch «die gewählte Welt» / «die zwei Welten» (Stamm-Wortlaut).
- Funktionen aus L18 (Schäfli), am Schlössli nicht eingeschaltet: Angaben des Hauses, Google-Texte, eigenes Foto hochladen, Anleitung, Rundgang, Fehlermelder an den Server. Für die Demo nicht nötig, kein toter Weg.
- Team: Marco Reisinger und Ole Sass ohne Foto (die Website hat keins), stehen mit Initialen.
- Knopf «Zur Werkbank» fehlt im Schaufenster (kein `zur-werkbank.js`), Meldung des Werkbank-Checks; stört die Demo nicht, weil jedes Werkzeug aus der Werkbank im neuen Reiter öffnet. Ziel wäre http://127.0.0.1:8982/werkbank/index.html#k5.
- Schaufenster online gibt es nicht (nur lokal :9035); Demo-Regel «online nur ansehen» unberührt.
- Tippen am echten iPhone einmal von Hand nachsehen (siehe Reparatur oben).

## Dateien dieses Checks

`democheck/democheck.js` (Hauptlauf), `erkunden.js`, `blick.js`, `blick2.js`, `tippen.js`, `tippen2.js` (Fehlersuche), Logs `democheck/lauf-*.log`, `fluss.json`.
