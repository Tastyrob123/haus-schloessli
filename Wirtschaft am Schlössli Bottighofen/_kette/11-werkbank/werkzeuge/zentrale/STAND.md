---
tags: [projekt, website]
status: aktiv
---

# Das Hafenbüro (La Maison) · Wirtschaft am Schlössli · Station 11, Teil «zentrale»

**Adresse lokal:** http://127.0.0.1:8987/_werkzeuge/maison/ (Prüfserver der Stube, `python3 _werkzeuge/maison/server.py 8987`, launch.json «stube-schloessli»).
**Ordner:** `_werkzeuge/maison/` im Projekt. Bauen: `python3 _werkzeuge/maison/bau.py` (lokal + `online/`). Bildschirme: `node _werkzeuge/maison/schirme.js`. Prüfen: `node _werkzeuge/maison/pruefung/pruefe.js chromium|webkit`.
**Welt:** Landhaus (`marke.json → welt: land`). **Namen** nach Robert 19.10.2026 («passt», Regel-Notiz Abschnitt 9): Das Hafenbüro, Das Schaufenster, Das Kartenpult, Die Hausdruckerei, Das Reservationsbuch, Das Bildarchiv, Die Besucherliste. Sie stehen an einer Stelle (`bau.py` → `NAMEN`); fehlt dort einer, gilt der Landhaus-Name aus `welt.js`.

## Was gebaut ist und warum es nicht aus dem Stamm kommt

Der Stamm (`_Werkzeuge/werkzeuge/`) hat keine Zentrale («kommt zuletzt»), und La Maison bleibt nach Roberts Entscheid vom 17.10.2026 je Haus eigen. Gebaut deshalb im Projekt wie bei den vier Häusern davor, Technik nach dem Master Werkzeug-Bau 4.1 (Bau mit zwei Fassungen, Stand-Wege mit Ersatz, Fehlermelder, Startfehler-Tür, Rundgang, «Zur Werkbank», Fassungsnummern aus dem Inhalt).

**Empfang «Sechs Bilder am Horizont»** (Robert 19.10.2026 «a», nach «Das Interface finde ich nicht schön.» zur ersten Fassung; Fehlerbuch 10a): hell mit der Punkt-Tapete der Website, Kopf links (Zeiger, «Das Hafenbüro», Gruss, Datum). Links die Bühne: in Ruhe die Terrasse über dem See, beim Darüberfahren oder Tastatur-Fokus die echte Vorschau des Werkzeugs (M23). Rechts sechs Kacheln mit je einem Foto des Hauses (Haus, Tortelloni, Wegweiser, Gaststube, Platanen, Bootshafen), N°, Name, Linie, Rolle, Stand. Nichts hüpft: nur der Punkt am Namen und ein sehr langsames Einzoomen des Fotos. Alles im ersten Bild (1440 × 900). Die Fassungen B und C liegen zum Vergleich als `fassung-b.html`, `fassung-c.html`.

**Säle** je Werkzeug (M08): Zeiger, «N° x von 6 · Rolle», Titel, Satz, Linie, Bildschirm des Werkzeugs, Tafel «So geht’s», Stand und Knopf. Flächen im Wechsel Tapete hell, Nacht mit Tapete, Papier.

## Stand der Werkzeuge im Hafenbüro (20.10.2026)

Alle sechs Werkzeuge liegen vor und sind eingehängt. Bildschirme im Safari-Kern @2x mit `schirme.js` (nur GET, keine Anmeldung, Begrüssungen geschlossen), Stand-Wege über `server.py` → `/_weiter/<werkzeug>/…`, Knopf-Namen der Tafeln beim Bau im Code jedes Werkzeugs gefunden (`knoepfe()`, keine Meldung).

| Werkzeug | Adresse | Vorschau und Stücke im Saal | Stand-Weg | Stand im Hafenbüro |
|---|---|---|---|---|
| Das Schaufenster | :9035 `/_werkzeuge/bureau/` | Übersicht, Startseite | `/api/x/website/ueberblick/schloessli` | Entwurf/veröffentlicht, 7 Bereiche, 11 Seiten |
| Das Kartenpult | :9031 `/_werkzeuge/carte/` | Arbeitsbereich, drei gedruckte Karten (Speisekarte, Lunch, Lästermeile aus `_karten/pdf`) | `/_werkzeuge/carte/api/status` | Karten, offene Entwürfe |
| Die Hausdruckerei | :9053 `/_werkzeuge/imprimerie/` | Übersicht, Flyer, Gutschein, Einladung (aus ihren druckfertigen PDF) | `…/haeuser/schloessli/vorlagen/index.json` | 251 Vorlagen in 23 Arten |
| Das Reservationsbuch | :9047 `/_werkzeuge/reception/` | Übersicht, «Chat ausprobieren» | `/_werkzeuge/reception/api/ueberblick` | neue/offene Anfragen, Fragen ohne Antwort, beschriftet «Beispiel» |
| Das Bildarchiv | :9049 `/_werkzeuge/livre/` | Übersicht, Logo & Dateien, sechs Fotos des Hauses, Farben in einer Reihe (aus `livre.json`) | `/marke/livre.json` | Fotos · Dateien |
| Die Besucherliste | :8988 `/_werkzeuge/registre/` | Übersicht mit Beispielwerten, «Der Weg zum Tisch» (Besuche → Fenster «Reservation» → gastronovi oder Anfrage → reserviert) | `/api/registre?tage=30&beispiel=1` | Heute · zur Reservation, 30 Tage, Länder, beschriftet «Beispiel» |

Namen aus der einen Stelle `_werkzeuge/oberflaeche/kleid/schloessli.js` (`WO_HAUS.namen`), beim Bau gelesen.

## Aus den anderen Häusern übernommen (Auftrag Robert 19.10.2026, «nicht wieder bei Null alle Fehler»)

Gelesen: Master Werkzeug-Bau (M01–M27, Abschnitt 10 bis 19.10.), Tasty-Sprache (Belege und Werdegang zu La Maison), Lieferung der Stube Gasterntal, Memory zu den Werkzeugen. Je Punkt am eigenen Stand geprüft:

| Korrektur | Herkunft | Hier |
|---|---|---|
| Vorschau statt Foto, nichts hüpft, Schilder gross und ruhig (M23) | alle Häuser 18.10. | Rahmen zeigt beim Darüberfahren die Aufnahme des Werkzeugs; Prüflauf «nichts hüpft» je Zeile grün |
| Kopf mittig mit Luft, Zeichen klein, Titel gross, nie gequetscht (M22) | Carlton 18.10. | Zeiger ~36 px, Titel bis 5 rem, Linie mit Punkt, Gruss, Datum untereinander |
| Ecke oben links in allen sieben Werkzeugen gleich (M24) | 18.10. 17:36 | Zeichen 26 px, Name 17 px, «Alle Werkzeuge · Haus» in Mono wie `.wo-marke-w` im gemeinsamen Rahmen |
| Farben höchstens eine Reihe (M25) | 18.10. | Farbreihe im Saal des Bildarchivs einreihig, erst nach dessen Lieferung |
| In der Demo nie leer (M27) | 18.10. 17:43 | Stand-Zeilen: Satz statt Leere; Beispielwerte beschriftet «Beispiel» |
| Bilder sofort, links nie leer («Wieso ist da links nichts?») | 18.10. 22:11 | Ruhebild mit hoher Priorität und kleinem Abbild als Grund; Vorschauen laden 0,4 s nach dem Ruhebild |
| Versionsnummer aus dem Inhalt (M20) | Carlton 18.10. | `?v=` je Datei aus dem Inhalt |
| Startfehler-Tür und Fehlermelder (R03, R04) | Rivage 17.10. | `fehler.js`, Prüflauf grün |
| Jedes Werkzeug öffnet oben (Gasterntal 18.10. 18:30) | Gasterntal | `scrollRestoration = manual` |
| Auftritt, wenn ein Fünftel im Bild ist, nie zu früh (18.10. 18:17) | alle Häuser | `fuenftel()` wie Gasterntal |
| Werkbank-Schlüssel des Hauses gleich in allen Werkzeugen | Besucherliste 19.10. | `schloessli-wb` |

## Prüfpunkte 7a (`_Werkzeuge/STAND.md`, «Prüfpunkte für jedes Werkzeug»)

| Prüfpunkt | Antwort |
|---|---|
| Backend | erfüllt für die Stube: sie ist statisch; lokal liefert `server.py` nur GET/HEAD und reicht Stand-Wege an die Werkzeuge weiter (nur 127.0.0.1). Fällt ein Werkzeug aus, steht sein Satz ohne Zahl (Prüflauf «Ohne Antwort», grün). |
| Datenbank | betrifft nicht: die Stube speichert nichts. |
| Authentication und Rollen | offen bis zur Auslieferung (Robert 15.10.2026: vorerst kein Passwort). Bei der Auslieferung Anmeldung vor jedem Werkzeug. |
| Rechteverwaltung | offen, wie oben. |
| API-Sicherheit | erfüllt lokal: `server.py` hört nur auf 127.0.0.1, nimmt nur GET/HEAD (POST nur Fehlermeldungen, verworfen), reicht nur an lokale Adressen aus der Kette weiter, Pfade mit Punkt-Ordnern gesperrt. Werte aus den Werkzeugen gehen nur als Zahl in die Seite (`ganz()`), Text wird maskiert. |
| Rate Limits | betrifft nicht die Stube (keine eigene Schnittstelle online). |
| Logging | erfüllt: Skriptfehler nach `localStorage sb_werkzeuge_fehler` und an `/studio/api/fehler` (R03), höchstens 20 je Seite, Netzfehler nie. |
| Backups | betrifft nicht: keine Daten; Quelle in `quelle/`, Bau wiederholbar. |
| Deployment | offen: Online-Fassung liegt in `online/`, nichts hochgeladen (Regel 61, Station 16). |
| CMS-Datenmodell | erfüllt: Werkzeuge, Adressen und Stand kommen aus der Kette und `stand_wege.json`; ein anderes Haus braucht nur neue Quelle und Kleid. |
| Übersetzungsworkflow | betrifft nicht: Oberfläche nur Deutsch (R24). |
| KI-Kosten | betrifft nicht: die Stube ruft keine KI; `schirme.js` weist KI-Wege ab. |
| Prompt-Injection-Schutz | betrifft nicht: keine KI. Werte aus den Werkzeugen werden nur als Zahl gesetzt. |
| DSGVO und Schweizer Datenschutz | betrifft nicht die Stube: keine Gästedaten, keine Cookies; Besuchszahlen nur als Summe. |
| Datenlöschung | betrifft nicht: nichts gespeichert. |
| Verfügbarkeit | erfüllt: ohne Werkzeug Satz ohne Zahl, ohne Skript Startfehler-Tür (R04, Prüflauf grün). |
| Monitoring | offen: kommt mit dem Cockpit (Station 17). |
| Booking-Integration | betrifft nicht: Reservation läuft über gastronovi auf der Website. |

## Prüfzahlen

| Lauf | Chromium | Safari-Kern |
|---|---|---|
| Gerüst, 1440 × 900 und 390 × 844 (19.10.2026) | 72 grün, 0 rot | 72 grün, 0 rot |
| Schluss, alle sechs eingehängt, 1440 × 900 (20.10.2026) | 46 grün, 0 rot | 46 grün, 0 rot |
| Schluss, Handy 320 × 640, 360 × 740, 390 × 844 (20.10.2026) | 78 grün, 0 rot | 52 grün, 0 rot (320, 390) |

Bedient je Browser und Grösse: zweimal laden (Antwort, keine kaputten Bilder, kein Überlaufen, Tür zu, alle Stücke aufgetreten, Konsole leer), drei Grussformen, Vorschau je Werkzeug beim Darüberfahren, Ruhe-Ansicht zurück, Tastatur-Fokus, nichts hüpft, Taste 1 bis 6, Laufzeile im Bild und ausserhalb, Ecke nach oben, Eck-Knöpfe ganz im Bild, «Weniger Bewegung», Startfehler-Tür, Ausfall aller Stand-Wege (Sätze ohne Zahl). Titel auf dunklem Grund weiss (gemessen). Kein `{`, `undefined`, `NaN`, `None` in den Seiten.

**Flüssigkeit** (Chromium, fertige Seite, Last 5,8 bis 6,0, 20.10.2026): 1440 × 900 4×/6× längstes Bild beim Scrollen 16,8/17,1 ms, unter dem Zeiger 33,3/32,6 ms, 0 über 33; 390 × 844 4×/6× 33,4/32,4 ms (ein Bild an der Grenze bei 4×); Layoutverschiebung 0,002 (Rechner) und 0,023 (Handy); Gewicht 3,76 MB (Rechner), 2,73 MB (Handy), 45 Anfragen.

## Offen

1. Online-Fassung liegt in `online/` (Wege aus den Andock-Dateien der Werkzeuge fehlen noch: ohne Andock führt jede Kachel online ins Kapitel Werkzeuge der Werkbank). Anschluss und Hochladen: Station 14/16.
2. Bildschirme neu aufnehmen, sobald ein Werkzeug sichtbar etwas ändert (`node _werkzeuge/maison/schirme.js`, dann `python3 _werkzeuge/maison/bau.py`).
3. Unabhängige Prüfung (Station 12).

## Wünsche an den Stamm

- Zentrale im Stamm: eine Stube, die die Adressen und Stand-Wege der Werkzeuge aus `haeuser/<kennung>/` liest, statt aus der Kette. Vorläufig im Projekt (`_werkzeuge/maison/bau.py`, `stand_wege.json`).
