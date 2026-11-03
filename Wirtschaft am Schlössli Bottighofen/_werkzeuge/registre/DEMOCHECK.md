---
tags: [projekt, website]
status: aktiv
---

# Demo-Check Die Besucherliste (Le Registre) · Wirtschaft am Schlössli · 21.10.2026

Unabhängiger Demo-Check-Chat (nie daran gebaut), Auftrag `_Oberchef/zeigen/schloessli/democheck/AUFTRAG.md`. Massstab: Website-Bau-Master «Vor dem Pitch: Demo-Check» Punkte 1–4. Geprüft an der Probe-Kopie `~/Desktop/Website-Projekte/_Probe Schloessli Registre/` (Prüfserver 8992 und 9103, Wegwerf-Daten unter /tmp), am echten Schlössli wurde nichts gezählt und nichts geschrieben ausser den Reparaturen unten. Browser nur headless (Playwright Chromium + WebKit), eine Instanz zugleich, mailto/tel im Prüfbrowser abgefangen.

**Urteil: demo-bereit — ja.**

## Was geprüft wurde, Weg für Weg

1. **Funktionsliste (`abnahme.js`, 91 Zeilen) in Chromium und Safari-Kern, je 1440 × 900 und 390 × 844 (Handy mit Tippen):** letzter Lauf nach allen Reparaturen (gestartet 21.10.2026, 04:17) **91 von 91 Zeilen grün in allen vier Läufen**. Das deckt jede der acht Ansichten (Übersicht, Besuche, Herkunft, Zeit, Seiten, Verlauf, Zur Reservation, So wird gezählt), Zeitraum 7/30/90 (gemerkt, alle Zahlen folgen), alle fünf Filter über der Besuchsliste, «Weitere 60 zeigen», Besuch wählen (Seite springt nicht), Kopf (Marke, Anleitung, Das Hafenbüro, Website ansehen), Rand und Rand-Klappe am Handy, Leiste, Meldungen, Rundgang (Weiter, ←/→, Esc, Überspringen, «Kurzer Rundgang» im Rand), Anleitung (zehn Kapitel, Bild gross, Esc, keine toten Links), «Als Tabelle sichern» (CSV mit «Beispiel» im Namen und je Zeile), «Zur Werkbank» nur aus der Werkbank, Startfehler-Tür, Sicherheitsregel der Online-Fassung.
   Im ersten Lauf war L03 (Rundgang, Chromium 1440) einmal rot: Zeitüberschreitung beim dritten Neuladen bei Rechnerlast 80 (acht Prüf-Chats parallel); einzeln sofort grün, in den Läufen danach grün. Kein Fehler des Werkzeugs.
2. **Zahlen passen zusammen:** P01/P01b/P02 rechnen jede Zahl in 7, 30 und 90 Tagen aus den Rohdaten der Beispielwerte nach (heute und drei Tage später). Von Hand gegengelesen: 27 von 538 = 5 %, 59 von 542 = 10.9 %, 38 + 59 = 97 Schritte zur Reservation, Länder 6 im Startbild = 6 in der Herkunft, Zahl im Rand (21) = «heute» im Startbild.
3. **Demo als Demo gekennzeichnet:** in jeder Ansicht, beiden Browsern, beiden Grössen steht «Beispielwerte. Diese Zahlen sind erfunden …» und die Leiste «Sie sehen Beispielwerte»; Kopf «Beispielwerte · keine echten Besuche»; kein Knopf zu echten Besuchen; der Dienst gibt ohne Schlüssel nur Beispielwerte heraus (M02, A08b).
4. **Eigener Rundgang mit Messung (`gang.js`):** jede Ansicht geladen, ganz durchgescrollt, gemessen: keine Konsolenfehler, keine Antwort 4xx/5xx, kein leeres Bild, kein roher Vorlagen-Code (undefined, NaN, null, {…}, Lorem), kein mailto- oder tel-Link im Werkzeug, nichts ragt seitlich hinaus (in WebKit 390 meldet nur das unsichtbare Zeichen-Depot `#zeichen` eine Lage, kein sichtbares Element; Seite 390 px breit).
5. **Zwischenbreiten (Fehlerbuch 10a, Schäfli 21.10.):** 920, 1000, 1100, 1180, 1240, 1280 px in Chromium und WebKit, jede Ansicht durchgescrollt, dazu die lange Besuchskarte bei 1440 × 900, 1366 × 650, 1280 × 720 und das Zusammenstossen im Vergleich «Neben dem Zeitraum davor» bei 901–1440 px. Drei Funde, alle repariert (unten).
6. **Inhalt:** Seitennamen = Titel der Website (12 Seiten, `seiten.json` gegen die `<title>` von `website/*.html` vom 20.10. 23:43), alle 12 Seitenfotos (`seiten-bilder.json`) vorhanden. Reservation über gastronovi stimmt mit der Website (`gastronovi.com/restaurants/118851/reservierung/widget`), «Route planen» steht auf der Kontaktseite, Schäfli-Verweis gewollt (Schwesterhaus, Ereignis «weiter zum Schäfli»). Herkunftsnamen (GaultMillau, Guide Michelin, Tripadvisor, Thurgau Bodensee Tourismus) passen zum Haus (`website/inhalt/haus.json`, `_quelle/extern/portale/`). Suche nach fremden Häusern im Revier: Treffer nur in Code-Kommentaren (Herkunft der Kopie) und der gewollte Schäfli-Verweis, nichts Sichtbares. Alle sichtbaren Texte aller Ansichten gelesen (aus `innerText` beider Browser): keine Platzhalter, keine Rechtschreibfehler gefunden.
7. **Nichts geht raus:** das Werkzeug hat keinen Weg, der ein Mailprogramm oder Telefon öffnet; es verschickt nichts; keine KI. Die Zählung der Website ist nur ein Vorschlag (`vorschlag/messung.js`), auf der echten Website nicht eingebaut.
8. **Bildschirmfotos:** `~/Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/registre/` — je Ansicht `<ansicht>-<browser>-<1440|390>.png` (32 Bilder), dazu `nachher-…` für die Reparaturen und `seiten-gescrollt-…`.

## Messwert (Regel 55, CPU 4× gedrosselt, Chromium, fertiger Stand)

Gleichmässiges Scrollen 4 s je Ansicht, Bilder je Sekunde / 95 %-Wert des Bildabstands:

| Ansicht | 1440 × 900 | 390 × 844 |
|---|---|---|
| Übersicht | 120 / 9 ms | 120 / 9 ms |
| Besuche | 115–117 / 9 ms (1–2 Bilder über 50 ms) | 117 / 9 ms |
| Verlauf | 120 / 9 ms | 119 / 9 ms |
| Zur Reservation | 120 / 9 ms | 87–119 / 9 ms |

Besuch wählen → Karte steht: 260–330 ms gedrosselt (1440), 295–347 ms (390). Gemessen bei Rechnerlast 66–80 (acht Prüf-Chats parallel); der eine Ausreisser (24 Bilder/s in Besuche, erster Lauf) liess sich in zwei Wiederholungen nicht nachstellen.

## Was repariert wurde

Sicherungen: `schloessli.css.vor-democheck-2026-10-21`, `registre.js.vor-democheck-2026-10-21`, `index.html.vor-democheck-2026-10-21`.

| Fund | Wo sichtbar | Reparatur | Nachgeprüft |
|---|---|---|---|
| Verlauf «Woche für Woche»: jede Wochenzeile ragte bis 59 px aus dem Fenster | 920–1000 px (kleines Laptopfenster) | `schloessli.css:66–72`, Lösung aus dem Schäfli: «n zur Reservation» rückt unter den Balken | 920–1280 px beide Browser: nichts ragt hinaus; Bild `nachher-verlauf-wochen-chromium-1000.png` |
| Karte eines langen Besuchs (8 Seiten, 846 px hoch) klebte oben, ihr Weg und der Hinweis lagen unter der Leiste, erreichbar erst am Ende der ganzen Liste | auch bei 1440 × 900, stärker bei 1366 × 650 und 1280 × 720 | `registre.js:669–684`, Block «Lange Besuche» aus dem Schäfli (Master G15): die Karte klebt mit dem Ende über der Leiste | Ende der Karte nach dem Scrollen bei 804 px (Leiste 822) bzw. 554 (Leiste 572); Bild `nachher-besuche-lange-karte-webkit-1440.png`; I08 grün |
| Verlauf «Neben dem Zeitraum davor»: «Angesehene Seiten», «Zur Reservation» liefen bis 70 px in die Zahl «2'218» | 901–1240 px (Tablet quer, kleines Fenster) | `schloessli.css:82–86`: in diesem Bereich stehen die zwei Blätter untereinander | Name gegen Zahl gemessen bei 901–1440 px, beide Browser: kein Zusammenstoss mehr |
| Handy: die fünf Filter über der Besuchsliste brachen als runder Klumpen um (2 + 2 + 1 in einer Pille) | 390 px, beide Browser | `schloessli.css:74–80`, Lösung aus dem Schäfli mit den Ecken des Schlössli: «Alle» über die ganze Breite, darunter 2 × 2 | Bilder `nachher-besuche-filter-*-390.png`; I01, I01b, I03, I06, I07, I09, E04, E05 am Handy grün |
| Neue Fassung wird sicher geladen | — | `index.html:20` `schloessli.css?v=3`, `index.html:37` `registre.js?v=5` | — |

Regel fürs Fehlerbuch: Werkzeug-Master 10a, neue Zeile «Wirtschaft am Schlössli · Verlauf «Neben dem Zeitraum davor»» (Felder auch auf Zusammenstossen messen, nicht nur auf Überragen; G15 in jede Kopie); die beiden Schäfli-Zeilen tragen jetzt «im Schlössli behoben».

## Nach dem Auftrag (stört die Demo nicht)

- **Listenbilder** stehen auf 56 × 42 (Master «Bilder in jeder Liste»: 104 × 78, Handy 72 × 54; das Schäfli ist schon umgestellt). Gestaltung, deshalb nicht im Demo-Check geändert. Mit grösseren Bildern muss am Handy das Bild über dem Seitennamen stehen (Schäfli-Block «Bilder in jeder Liste»).
- **Seiten:** die Balken der ersten Zeilen wachsen erst, wenn das Blatt zur Hälfte im Bild ist (Zeile K03, Rezeptur Rivage); beim ersten Blick auf die Ansicht stehen sie kurz leer. So gewollt, nur notiert.
- **Seiten:** der Spaltenkopf «Zur Reservation» reicht bei 1440 px wenige Pixel über die Trennlinien der Zeilen hinaus (bleibt im Blatt).
- **Anleitung:** die zehn Bilder stammen vom 20.10. 00:00, vor der Kopfänderung im Kleid (20.10. 14:25); sichtbar gleich, beim nächsten Bau neu aufnehmen (`anleitung_bilder.js`).
- **«Zur Werkbank» lokal** (Fund des Werkbank-Demo-Checks, 21.10.): erscheint nur mit `?wb=…` von Hand angehängt, nicht über den echten Weg aus der Werkbank (neuer Reiter). Mit `?wb=de.k5` zeigt der Knopf lokal auf `http://127.0.0.1:8988/werkbank/index.html#k5` → 404, weil der Server des Besucherbuchs die Werkbank nicht ausliefert (sie liegt auf 8982); online gleiche Adresse, dort richtig. Prüfzeile Q02 prüft nur die Form des Ziels, nicht dass es antwortet. Beim Auftrag: lokal auf die Werkbank des Hauses zeigen oder `werkbank/` im Server freigeben, Q02 das Ziel abrufen lassen.
- **Prüfreihe:** L03 lädt dreimal neu und wartet je 9 s; unter hoher Rechnerlast einmal zu knapp. Beim nächsten Bau die Wartezeit auf 15 s.

## Ansicht

Lokal: `python3 _werkzeuge/registre/server.py 8988` aus dem Projektordner → http://localhost:8988/_werkzeuge/registre/ (Prüfstand dieses Checks lief auf http://localhost:9103/_werkzeuge/registre/ aus der Probe-Kopie).
