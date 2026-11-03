---
tags: [projekt, website]
status: aktiv
---

# Demo-Check · Das Reservationsbuch (La Réception) · Wirtschaft am Schlössli · 21.10.2026

**Urteil: demo-bereit — ja.**

Geprüft von einem Chat, der nie daran gebaut hat, nach `_Oberchef/zeigen/schloessli/democheck/AUFTRAG.md` und Werkzeug-Master Abschnitt 4.4 (E01–E34), 9 und Fehlerbuch 10a.
Server: `python3 _werkzeuge/reception/server.py 9047` (launch.json «gastgeber-schloessli»), ohne `RECEPTION_KI`, ohne Schlüssel: Probe ohne KI. Geprüft wurde an einer Kopie mit Wegwerf-Daten (eigener Server :9048, `RECEPTION_DATEN` im Scratchpad); die Daten des Demo-Servers sind unverändert und frei von Prüfspuren (`grep QA|Probe-Antwort daten/` leer).
Der Demo-Server :9047 wurde um 03:50 einmal neu gestartet (gleicher Befehl, gleicher Ordner, ohne KI), damit der neue Satz in `probe_ki.py` gilt.

Bilder (1440 und 390, Safari-Kern und Chromium, jede Hauptansicht): `~/Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/reception/` (50 Bilder).

## Ergebnis je Browser und Grösse (letzter Lauf, 04:05)

| Lauf | Chromium 1440 | Chromium 390 | WebKit 1440 | WebKit 390 |
|---|---|---|---|---|
| Prüflauf des Werkzeugs `pruefung/schloessli.js` | 24/25 | 24/25 | 23/24 | 24/25 |
| Zusatzlauf Demo-Check | 10/10 | 9/10 | 10/10 | 9/10 |

Die einzigen roten Punkte, beide geklärt:
- **Website-Formular `fe-plaetze`**: das Fenster gibt es auf der Website seit 20.10. nicht mehr (`anlaesse.html` nutzt `fe-reservation`). Kein Fehler des Werkzeugs; der Prüflauf ist angepasst (Zeile auskommentiert).
- **Chat am Handy im Zusatzlauf**: der Zusatzlauf suchte den Knopf an der falschen Stelle. Am Handy liegt «Chat ausprobieren» unter «Bereiche»; so bedient (Antippen) in Chromium und WebKit 390 mit 8 Fragen hintereinander: Eingabefeld bleibt unten sichtbar, Antworten rollen im Handy, kein seitliches Verrutschen (Bild `webkit-390-chat-nach-8-fragen.jpg`).
- Frühere Läufe hatten Zeitüberschreitungen bei Rechnerlast über 100 (andere Chats); bei Last 40–50 grün.

## Was geprüft wurde, Weg für Weg

- **Fünf Ansichten** (Übersicht, Eingang, Das wurde gefragt, Vom Team nachgetragen, Das weiss der Chat): je zweimal geladen, keine Konsolenfehler, kein 404, keine kaputten Bilder, kein seitliches Überlaufen, kein roher Code (`{`, undefined, NaN, None, null), jede Liste mit Foto.
- **Eingang**: Hinweise Ruhetag, Ferien, Etagen, Allergien bei den richtigen Anfragen; Abstand Hinweise zur Schrift 18 px, Rundgang-Schild wandert 0 px; Auswahl Reservation 3 / Bankett 3 / Gutschein 1 stimmt mit den Daten; **Filter Alle 7 / Neu / Offen 6 / Erledigt 1** stimmen mit den Daten; Erledigt ↔ Wieder offen; Auf Deutsch lesen (englische Anfrage Emma Clarke).
- **Brief**: «Brief schreiben» (Probe) nennt die Allergie, ändern, sichern, neu laden, bleibt; **«Text kopieren»** legt Betreff und Brief in die Zwischenablage, Quittung «Kopiert»; «Als PDF speichern» lädt ein A4-PDF «Wirtschaft am Schlössli – Thomas Brunner – 21.10.2026.pdf» mit Briefkopf des Schlössli.
- **Das wurde gefragt**: Lücke nachtragen → steht unter «Vom Team nachgetragen» → entfernen.
- **Das weiss der Chat**: Suche «Lunch» trifft; «Kinderstuhl» → «Noch nicht im Wissen» → **Abteilung fragen** (Küche) → steht unter «Offen bei Ihrem Team» → neu laden → noch da → «Nicht mehr nötig» → weg. **Angabe hinzufügen** → neu laden → noch da → entfernen → neu laden → weg (im Verlauf steht «neu» und «entfernt», wie gewollt). Auswahl und Kalender im Stil des Hauses.
- **Chat ausprobieren**: 13 typische Gästefragen (Ruhetag, Küchenzeiten, Reservation, Lunch, Weinkarte, Anfahrt, Parkplatz, Gutschein, Geburtstag 20 Personen, Nussallergie, vegetarisch, Ferien, Reservation mit Kontakt). Jede bekommt eine sichtbar beschriftete Probe-Antwort, keine Fehlermeldung; die Frage mit Mail-Adresse legt eine Anfrage als «Beispiel» im Eingang an (danach entfernt).
- **Website-Formulare über den Baustein**: Reservation, Bankett, Gutschein, «Ihr Abend» (Firmenanlass wird Bankett) landen im Eingang mit allen Angaben. Weg `formular`: fremde Herkunft 403, ungültiger Kontakt 422, Maschinenfeld legt nichts ab, über 12 kB 413.
- **Nichts öffnet ein Programm**: kein `mailto:`, `tel:` oder `sms:` in allen Ansichten, jeder Anfrage, jeder Frage, Prüfseite, Anleitung; kein Aufruf mitgeschrieben; kein neues Fenster mit Programm.
- **Prüfseite** `pruefung.html`: «Alles in Ordnung. Gelb heisst: bewusst so, kein Fehler.» (gelb: Probe ohne KI); «Alle Daten herunterladen» liefert eine ZIP (20 kB).
- **Anleitung**: alle sichtbaren Bilder geladen, jeder Kapitel-Sprung trifft, alle Links ohne 404, kein Überlaufen.
- **Wege aus dem Werkzeug**: Reservation und Bankettanfrage auf der Website, Das Hafenbüro, Anleitung, Prüfung, Zur Werkbank: alle 200.
- **Inhalt gegen das Original**: die zehn Beispiel-Antworten unter «Das wurde gefragt» gegen `website/inhalt/*.json`, `_quelle/website/pdf-text/` und `_kette/03-sammler/fakten.json`: Ruhetag und Zeiten, Ferien (13.–15.11., 22.12.–10.2.), Lunch 35 Franken mit drei Gängen, Tapas ohne G (Padrón, Patatine L/E, Kalamata N), Bankett zwei Etagen je 26, Menüs 175/185/175, 3–5 Gerichte, Parkplatz und Bahn, Hunde willkommen (Falstaff, Tagblatt), Kinderstuhl und Schiff ehrlich ohne Antwort. Telefon, Adresse, Mail stimmen. Eine Antwort war unvollständig (siehe Reparaturen).
- **Fremde Häuser**: `grep` nach Rivage, Carlton, Doldenhorn, Ruedihus, Schäfli usw. im Revier: nur Herkunftskommentare im Code, nichts Sichtbares, nichts in Daten, Wissen, Briefen.
- **Flüssig** (4× gedrosselt, Wechsel der Ansichten und Scrollen, Chromium 1440): 100 Bilder/s, 7 Bilder über 50 ms, längstes 216 ms.

## Was repariert wurde

| Fund | Datei | Änderung |
|---|---|---|
| Chat ausprobieren: nach einigen Fragen wuchs das Handy über das Fenster, die linke Spalte rutschte leer nach oben weg, das Eingabefeld lag unter dem Rand | `schloessli-gastgeber.css` (Block «Demo-Check 21.10.2026», nach Zeile 194) | `.probe__k` und `.probe__rechts` bekommen eine feste Zeile; die Antworten rollen im Handy. Nachgeprüft mit 10 Fragen (1440) und 8 Fragen (390, beide Browser) |
| Probe-Antwort des Chats sagte «Echte Antworten gibt es erst mit Schlüssel» | `probe_ki.py` Zeile 81 | «In der Demo ist der Chat noch nicht angeschlossen; im Betrieb antwortet er hier aus dem Wissen des Hauses.» |
| Telefonnummer eines Gastes war ein `tel:`-Link (öffnet beim Antippen ein Programm) | `reception.js` Zeile 262 (`kontaktLink`) | reiner Text wie die Mail-Adresse |
| Beispiel-Antwort Tortelloni nannte nur 35 Franken, die Karte hat 35 und 50 als Hauptgang | `gast_beispiel_fragen.json`, `daten/fragen/2026-10-18/13-40-00_beispiel-4.json` | «Price: CHF 35, as a main course CHF 50» |
| Fassungsnummern | `index.html`, `pruefung.html`, `anleitung.html` | `_bau/fassungen.py` gelaufen (reception.js, schloessli-gastgeber.css, kleid/schloessli.css neu) |
| Prüflauf prüfte ein Website-Fenster, das es nicht mehr gibt | `pruefung/schloessli.js` (FORM, `fe-plaetze`) | Zeile auskommentiert mit Grund |

Sicherungen: `*.vor-democheck-2026-10-21` neben jeder geänderten Datei.
Fehlerbuch 10a im Werkzeug-Master: drei neue Zeilen vom 21.10.2026 (Chat-Fenster mit fester Zeile, Demo-Wort statt Technik in Probe-Antworten, kein `tel:` im Werkzeug).

## Nach dem Auftrag (stört die Demo nicht)

- **Echte Chat-Antworten** sind in der Demo nicht prüfbar (Probe ohne KI). In der Kostenrunde die 13 Fragen oben einmal mit `RECEPTION_KI=1` stellen und jede Antwort gegen das Original legen.
- **Gutschein**: Die heutige Website des Hauses hat keine Gutschein-Seite, das Wissen des Chats deshalb keine Gutschein-Angabe; die neue Website hat `gutschein.html`. Vor dem Betrieb Gutschein-Angaben vom Haus holen und ins Wissen.
- **Text «Plätze für Anlässe»** in Übersicht und Eingang und das Beispiel Peter Huber (Seite Anlässe): stimmen noch, seit das Fenster `fe-plaetze` weg ist, aber prüfen, ob die Website Anlass-Plätze weiter über die Reservation anbietet.
- **Brief-Ansicht 1440**: beim Scrollen bis zum Brief steht links eine leere Fläche, weil der Rand nicht mitläuft (Bild `webkit-1440-brief.jpg`). Gestaltung, nicht geändert.
- **Gleicher Chat-Fenster-Fehler im Schäfli** (`Taverne zum Schäfli Wigoltingen/_werkzeuge/reception/schaefli-gastgeber.css`), dort nicht angefasst; gemeldet an den Oberchef. Der Satz «mit Schlüssel» und der `tel:`-Link stecken in allen anderen Häusern (Ruedihus, Gasterntal, Carlton, Doldenhorn, Schäfli).
