---
tags: [projekt, website]
status: aktiv
---

# Demo-Check Das Kartenpult (La Carte) · Wirtschaft am Schlössli Bottighofen · 21.10.2026

Prüfer: Demo-Check-Chat «Karten», nie daran gebaut. Auftrag: `_Oberchef/zeigen/schloessli/democheck/AUFTRAG.md`. Massstab: Demo-Check (Website-Master «Vor dem Pitch»), Werkzeug-Master 4.3, Fehlerbuch 10a. Nichts online, nichts verschickt, keine KI.

**Urteil: demo-bereit — ja.**

Werkzeug: http://127.0.0.1:9031/_werkzeuge/carte/ (launch.json «tafel-schloessli») · Bilder: `~/Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/carte/`

## Was geprüft wurde (Weg für Weg)

| Weg | Wie geprüft | Ergebnis |
|---|---|---|
| Bedienungsprobe aller Funktionen (R01–R19, C01–C15, C08 Lunch, Rollen, Sicherheit, zwei Fenster, Netz weg, Rundgang, Prüfseite, Export, Anleitung) | `node pruef/lauf.js` auf Wegwerf-Daten, nach den Reparaturen | Chromium 1440: 153/153 · Chromium 390: 151/151 · Safari-Kern 1440: 153/153 · Safari-Kern 390: 151/151 |
| Jede Karte öffnen, Preis bzw. Gericht ändern, speichern, neu laden → noch da, Probe-PDF, verwerfen → Ausgangsstand | eigener Lauf über die Wege des Werkzeugs, Wegwerf-Server :9034 | alle fünf Karten grün (Speisekarte, Lunch-Menü, Lästermeile, Weinkarte, Bankettmenüs); Stand danach Zeichen für Zeichen wie vorher |
| Echte Daten des Hauses | `_daten/entwurf/` leer, kein offener Entwurf, nichts verändert | sauber |
| Jede PDF ansehen | alle Seiten gerendert und angesehen (2 + 1 + 1 + 23 + 2) | kein abgeschnittener Text, kein leeres Feld |
| Mittagsmenü vorhanden | Lunch-Menü der Woche 19.–25.10.2026, Blatt A4 quer, mittig | vorhanden, Wortlaut = `_quelle/website/pdf/Lunch_261019.pdf` (Kürbissuppe, Risi e bisi, Joghurt Panna Cotta, 3 Gänge 35.- Chf) |
| Wortlaut jedes Gerichts, jeder Preis gegen das Original | `python3 pruefe.py wortlaut` | 4 von 4 «gleich bis auf Trennung», GRÜN |
| Druck = PDF der Website | `python3 pruefe.py website` | 4 von 4 Text und Seitenbilder gleich |
| Rundlauf Daten → Satz | `node pruef/rund.js` | 5 von 5 gleich |
| Jeder Link im Kopf und Rand (19) | aufgerufen, Status | 0 tot (vorher 2, s. u.) |
| Hauptansichten je Browser und Grösse | Bilder: Speisekarte, Lunch, Lästermeile, Weinkarte, Bankett, Fortgeschritten, Website, Anleitung, Prüfung | kein seitliches Verrutschen (0 px), keine Konsolenfehler |
| Fremde Häuser | grep im Revier | nur in Kommentaren (Herkunft der Vorlage), nirgends sichtbar |
| mailto/tel, Versand, KI | grep, Bedienungsprobe fängt mailto/tel ab | keiner vorhanden, keine KI im Werkzeug, Anschluss an die Website aus |
| Listen-Zeilen auf rohen Code | alle 797 Zeilen der vier Satz-Karten | kein `undefined`/`NaN`/`{`, nach Reparatur keine Klammer-Zeile |

## Was repariert wurde

| Fund | Datei, Stelle | Nachgeprüft |
|---|---|---|
| Knopf «Das Hafenbüro» (Kopf) und «Das Schaufenster» (Rand) führten ins Leere (404, Server der Website liefert keine Werkzeuge) | `carte.js` Z. 45–48 (WERKZEUGE → :8987); Probe `pruef/lauf.js` Z. 71, 96 angepasst | 19 Links, 0 tot, alle vier Browser-Läufe |
| Ansicht «Website» zeigte bei Bankettmenüs und Weinkarte die Seite «Karte» statt «Banketts» bzw. «Weinkarte» | `carte.js lade()` Z. 948 | Bild `4-website-*`: «Banketts & Gruppen» mit den Menüs |
| Am Handy wurde «Bankettmenüvorschläge» im Kopfbild abgeschnitten | `carte.js kopf()` Z. 231 (Trennstellen) | Safari-Kern und Chromium 390: Titel 314 von 314 px, zwei Zeilen |
| Anleitung beschrieb die entfernte Abfrage «Wer sind Sie?», einen Namensknopf oben rechts, den 4-Hands-Lunch (nicht im Werkzeug) und «Im Grandhotel heisst dieses Werkzeug La Carte» | `anleitung.html` Z. 34, 37, RECHT, ROLLE | Bild `5-anleitung-*` |
| Liste der Bankettmenüs zeigte den Menüpreis als Zeile «( Text 175» | `carte.js titelVon()` Z. 117 | Zeile heisst jetzt «(175 CHF)» |
| Prüfseite zeigte zwei Skriptfehler vom Bau (20.10., längst behoben) | über die Reparatur der Prüfseite «Fehlerlisten leeren», alte Listen liegen daneben (`_daten/*.alt`) | Prüfseite: keine Fehler |
| Schwebender Knopf «Zur Werkbank» (erscheint, wenn das Kartenpult aus der Werkbank geöffnet wird, `?wb=de.k5`) zeigte auf `:9031/werkbank/` → 404 (Fund des Werkbank-Demo-Checks; im echten Weg aus der Werkbank erscheint der Knopf nicht, nur mit `?wb=` von Hand, trotzdem behoben) | `zur-werkbank.js` nach `if (!basis) return;` (lokal → :8982); `index.html`, `anleitung.html` `zur-werkbank.js?v=3` | Chromium 1440 und Safari-Kern 390, Werkzeug und Anleitung: `:8982/werkbank/index.html#k5` → 200; Bedienungsprobe Chromium 1440 153/153; Bild `6-zur-werkbank-chromium-1440.png` |
| Cache: Browser mit alter `carte.js` | `index.html` `carte.js?v=18` | — |

Sicherungen: `carte.js.vor-democheck-2026-10-21`, `index.html.vor-democheck-2026-10-21`, `anleitung.html.vor-democheck-2026-10-21`, `pruef/lauf.js.vor-democheck-2026-10-21`, `zur-werkbank.js.vor-democheck-2026-10-21`.

Beim Reparieren selbst kurz verursacht und sofort behoben: ein Kommentar hinter dem Titel nahm für einige Minuten den Erklärsatz im Kopfbild weg (an den Bildern gesehen, nicht an der Probe; die Probe prüft den Satz nicht).

Fehlerbuch 10a (Werkzeug-Master): sechs Zeilen vom 21.10.2026 als Regeln für alle Häuser.

## Messwert (gedrosselt)

Chromium, Prozessor 4× gebremst, 1440 × 900, gemessen 21.10.2026 03:52 unter Rechnerlast 67 (viele Chats parallel; `pruef/fluessig.js` misst erst unter Last 8 und lief deshalb nicht, dies ist der ungünstigere Fall): Speisekarte steht nach 1,2 s, Lunch 0,1 s, Weinkarte 1,3 s, Bankett 0,8 s (Grenze 6 s). Scrollen 120 Bilder/s, schlechtestes Bild 9 ms; nach Weinkarte und Bankett 116 Bilder/s, schlechtestes Bild 58 ms (Grenze 30/s und 120 ms). Bau-Messung 20.10. unter Last 5,5–7 (Slow 4G dazu): Karten 3,8–5,9 s, 120 Bilder/s.

## Nach dem Auftrag (stört die Demo nicht)

- Bankettmenüs Seite 2 (Herbst) und Weinkarte Seite 23 sind unten halb leer; es sind jeweils die letzten Seiten. Roberts Regel «keine halbleeren Seiten» (Fehlerbuch 19./20.10.) prüfen, ob Herbst auf Seite 1 nachrücken oder die Seite anders gefüllt werden soll.
- Am Desktop läuft «Bankettmenüvorschläge» jetzt zweizeilig (Bankettmenü- / vorschläge); vorher stand es einzeilig und lief bis ins Foto. Gestaltung: Robert entscheidet, ob der Name der Karte kürzer werden soll («Bankettmenüs»).
- Anschluss an die Website fehlt: die Seiten zeigen die Karten aus `website/inhalt/*.json`; «Veröffentlichen» legt die PDF erst mit Anschluss ab (Station 14).
- Online-Fassung nicht gebaut; kein Passwort, Rollen ohne Anmeldung, keine Kopie ausserhalb des Rechners.
- Lunch-Menü: Wochentage und Uhrzeit stehen nicht in der PDF des Hauses (Feld leer).
- 172 Flaschenbilder der Weinkarte aus dem Weinberater (Vivino), Rechte offen.
- Die Bedienungsprobe prüft den Erklärsatz im Kopfbild und die Erreichbarkeit der Links nicht; beides ist bei der nächsten Überarbeitung von `pruef/lauf.js` nachzutragen.
- Die Wege zu den anderen Werkzeugen hängen fest an Port 8987; zieht das Werkzeug in Station 14 nach `website/_werkzeuge/`, gelten wieder relative Wege (online ohnehin `/`).
