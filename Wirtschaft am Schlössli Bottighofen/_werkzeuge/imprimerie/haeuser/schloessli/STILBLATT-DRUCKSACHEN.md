---
tags: [projekt, website]
status: aktiv
---

# Stilblatt Drucksachen · Wirtschaft am Schlössli Bottighofen

Stand 3.11.2026 (Nachtbau). Gilt für jede Drucksache der Hausdruckerei: alle Vorlagen, die Muster unter «Entwerfen», die Vorschläge und jedes gespeicherte Dokument. Abgeleitet aus der gebauten Website des Hauses (`website/assets/css/haus.css`, Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» in Open Sans, die Zeiger als Zeichen) und den Karten des Hauses (`website/inhalt/*.json`, `_karten/`). Umgesetzt in `dokumente.js`, maschinenlesbar in `stilblatt.json`. Gegen diese Regeln prüft die Druckprüfung.

Masse in Teilen der **kurzen Seite u** des Formats (A4: u = 210 mm, DL: 99 mm, Story: 108 mm), damit dieselbe Regel auf A7 und A3 gilt.

## 1. Rollen und Schriften

| Rolle | Schrift, Schnitt | Schreibung | Wofür |
|---|---|---|---|
| Titel | Open Sans 400 | VERSALIEN, gesperrt .04–.10 em, nie fett, nie kursiv | Titel jeder Drucksache, wie die Wortmarke |
| Gericht | DM Mono 400 (auf der Menükarte Open Sans 400) | VERSALIEN wie auf der Karte: «THON», «CAVATELLI», «TORTELLONI» | Gerichte der Karten, Einleger, Bankettmenüs. Diese Versalien sind gewollt |
| Lesetext | Instrument Sans 400 | normal | Text, Beschreibung unter dem Gericht, Hinweise |
| Betont | Instrument Sans 500 | normal, nie kursiv | Hervorhebung über Stärke |
| Etikett | DM Mono 400 | VERSALIEN, gesperrt .04–.10 em | Kicker («WIRTSCHAFT AM SCHLÖSSLI», «DIE LÄSTERMEILE»), Datum, Uhrzeit, Instagram |
| Kopf- und Fusszeile | DM Mono 400 | VERSALIEN, gesperrt .08 em | Ort oben, Adresse unten |
| Zeile unter der Wortmarke | Open Sans 500 | VERSALIEN | nur auf der Menükarte |

Verboten: Kursiv, fremde Schriften, Sperrung über .10 em. Handschrift (Caveat) bleibt auf der Website.

## 2. Schreibung und Trennzeichen

- Schweizer Schreibung: **ss statt ß**, Anführungszeichen «…», Anrede **Sie**.
- Glieder, Ort, Adresse: « · ». Zeiten: «11:30 Uhr - 13:30 Uhr».
- Umbrochen wird nur zwischen zwei Gliedern; das Trennzeichen am Zeilenende fällt weg.
- **Keine Preise** auf Drucksachen der Hausdruckerei (Preise stehen nur auf den Karten des Kartenpults). Ein Gutscheinwert bleibt ein Feld zum Eintragen.

## 3. Eine Achse

- Jedes Dokument hat genau eine Achse, Standard mittig: Zeichen, Etikett, Titel, Linie, Text, Kopf- und Fusszeile auf der Mitte.
- Linksbündig nur ganz, als eigener Aufbau («Bild und Text geteilt»), nie gemischt.
- Querformat mit Bild links: die Achse ist die Mitte der Textspalte.
- Einladung, Rückseite, Titelblatt und Gutschein in A6, A5 und DL quer sind zweispaltig, jede Spalte mit eigener Mittelachse, beide auf derselben optischen Mitte.
- Zeitleisten (Ablauf, Programm, Reise) sind ein Block mit eigener Kante innen (Uhrzeit | Schritt), der als Ganzes auf der Mitte steht.

## 4. Komposition

- **Zeichen und Inhalt sind eine Gruppe.** Die Zeiger stehen direkt über Etikett oder Titel, nie allein am oberen Rand.
- Die Gruppe steht auf der **optischen Mitte** (4 % der freien Höhe über der geometrischen Mitte zwischen Kopf- und Fusszeile) und füllt **45 bis 78 %** der Höhe; Menükarte bis 92 %, Karten mit Gerichten bis 90 % (die Gerichte verteilen sich über die Höhe). Wenig Inhalt wird grösser gesetzt (bis 1,3-fach), nie unter die Mindestgrade.
- **Kopf und Fuss** 5,5 % u innen am Rahmen, oben der Ort («BOTTIGHOFEN AM BODENSEE» oder der Betrieb), unten die Adresse «SEESTRASSE 50 · 8598 BOTTIGHOFEN».
- **Menükarte:** oben die Wortmarke «WIRTSCHAFT AM SCHLÖSSLI», darunter «Menü», Anlass, kurze Linie, die Gänge gleichmässig über die Höhe.
- **Ablauf und Programm:** Zeitleiste, links die Uhrzeit in DM Mono (Seehimmel tief), rechts der Schritt in Instrument Sans.

## 5. Grössen nach Zweck

| Zweck | Formate | Titel | Text | Etikett | Zeichen (Breite) |
|---|---|---|---|---|---|
| Aushang, aus 2–3 m | A3, A4, A5 hoch | 0,105 u | 0,038 u | 0,0165 u | 0,13 u |
| Karte, aus Armlänge | A6, DL hoch | 0,118 u | 0,047 u | 0,02 u | 0,15 u |
| Tisch- und Platzkarte quer | A7, A6 quer | 0,14 u | 0,055 u | 0,022 u | 0,13 u |
| Handy | Story, Instagram, Newsletter | 0,115 u | 0,046 u | 0,02 u | 0,15 u |

Verhältnisse: Titel zu Text 2,5 bis 3,2; Etikett zu Text 0,4 bis 0,5; Zeichen 1,2 bis 1,4 mal so breit wie der Titelgrad.

## 6. Mindestgrade (mm)

| Format | Titel | Text | Etikett, Fuss |
|---|---|---|---|
| A3, A4 Aushang | 15 | 6 | 2,6 |
| A5 | 11 | 4,2 | 2,0 |
| A6, DL | 6 | 2,1 | 1,5 |
| A7 quer | 5 | 2,0 | 1,5 |
| Story, Instagram | 7 | 3,6 | 1,6 |

## 7. Farben je Ton (nur diese)

| Ton | Grund | Titel | Text | Etikett | Linie, Zeichen |
|---|---|---|---|---|---|
| hell | Blatt #F4F6F9 | Tief #0A234C | Tinte #041023 | Seehimmel tief #0F3678 | Seehimmel tief (Zeichen Stuhlblau #113D88) |
| creme | Papier #E7ECF3, helle Tapete | Tief #0A234C | Tinte #041023 | Seehimmel tief #0F3678 | Seehimmel tief (Zeichen Stuhlblau) |
| dunkel | Stuhlblau #113D88 oder Nacht über dem See #0B1D3D, Punkt-Tapete | Blatt #F4F6F9 | Papier #E7ECF3 | Seehimmel #A2B6CF | Seehimmel |

Schirmrot #FD9964 höchstens als Punkt. Keine Verläufe, keine Schatten im Dokument.

## 8. Linien und Ränder

- Rahmen 4,5 % u vom Rand (mindestens 4,5 mm), Stärke 0,0018 u (mindestens 0,25 mm), Ecke 1,1 % u.
- Unter dem Titel eine kurze Linie: 0,08 bis 0,1 u lang, 0,0024 u stark — der Horizont des Sees.
- Zwischen Posten keine groben Linien, nur Luft oder ein kurzer feiner Strich (6–8 mm, 0,25 mm).
- Satzbreite 8 bis 9 % u innen vom Rahmen, Lesetext höchstens 0,74 u breit.

## 9. Marke und Schmuck

- Ein Zeichen: **die Zeiger** aus der Wortmarke. Keine Ersatz- oder Zierzeichen (kein «x», Stern, Raute, Punkt als Schmuck), das Zeichen dient nie als Trenner.
- Die Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» steht als Grafik (nie als Schrift nachgebaut), höchstens einmal je Seite, nicht zusammen mit dem Zeichen.
- Nie zwei grosse Elemente in voller Akzentfarbe nebeneinander.

## 10. Bilder

- Nur Fotos des Hauses aus `website/assets/img/` (Register `website/inhalt/bilder.json`); keine Gäste-, Fremd- oder KI-Bilder (`tb-*`, `baum`, `kf-*`, `pa-teller`, `kp-party`, `feuerwerk*`, `ch-*`).
- Nie verzerren; Fotos dürfen beschnitten werden, Schrift im Bild nie.

## 11. Umbruch und Texte

- Nie ein Wort allein in der letzten Zeile, ausser bei einem Titel aus einem Wort.
- Jeder Satz wertet auf: Sorgfalt, der einzelne Gast, der See. Herzlich und unkompliziert, nie werblich laut. Fakten nur aus `website/inhalt/haus.json`.
