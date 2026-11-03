---
tags: [projekt, website]
status: entwurf
---

# Wirtschaft am Schlössli · Übergabe der Website (Station 07, 19.10.2026)

**Stand:** Website als Entwurf lokal fertig gebaut, alle Seiten der Seitenliste neu, nichts online, nichts verschickt.
**Lokal:** http://127.0.0.1:8982/ (Server: `python3 website/serve.py 8982`, auch als `schloessli-bottighofen` in `~/SecondBrain/.claude/launch.json`).
**Über die Karte:** http://127.0.0.1:8978/haus/Wirtschaft%20am%20Schl%C3%B6ssli%20Bottighofen/website/index.html

## Die Geschichte in einem Satz

Man kommt am Hafen an, setzt sich auf einen der blauen Stühle unter den Platanen und bleibt sitzen; alles, was das Schlössli ausmacht, kommt an diesen einen Tisch, am Horizont des Sees (Konzept, Station 06, bestätigt 19.10.2026).

## Was wo liegt

| Was | Wo |
|---|---|
| Bau aller Seiten | `website/bau.py` (Kopf, Leiste, Fuss, Fenster einmal) |
| Inhalte, eine Stelle | `website/inhalt/haus.json` (Zeiten, Adresse, Sätze, Team, Anlässe, Quellen je Feld) |
| Karten als Daten | `website/inhalt/karte.json`, `laestermeile.json`, `lunch.json`, `bankett.json`, `wein.json`, maschinell aus den PDF-Texten gelesen mit `website/karten_lesen.py` (495 Preiszeilen der Weinkarte = 495 im Original) |
| Bilder | `website/bilder.py` baut aus `_quelle/` die Liefergrössen nach `assets/img/` und `inhalt/bilder.json` (Horizont je Foto gemessen, Skalen in `_qa/horizont/`) |
| Gestaltung | `website/assets/css/haus.css` (ein Block je Teil, Kommentar davor) |
| Verhalten | `website/assets/js/haus.js` (Auftakt, Lader, Auftritte, Schlitz, Leiste, Menü, Fenster, Auswahl und Kalender) |
| Rechtstexte | im Wortlaut aus `_quelle/website/text/` (impressum.md, datenschutzerklarung.md, agbs.md), umgesetzt in `bau.py › md_zu_html` |
| Prüfen | `website/_qa/pruefen.js` (Abschnitt für Abschnitt, Chromium und WebKit, Aufnahmen in `_qa/bilder/`) |
| Messen | `website/_qa/messen.js` (4- und 6-fach gedrosselt, Werte in `_qa/messung-*.json`) |
| Paket der Station | `_kette/07-baumeister/abschnitte.json`, `stand.json` |

Neu bauen: `cd website && python3 karten_lesen.py && python3 bilder.py && python3 bau.py`

## Seiten

`index.html` (Startseite, zwölf Teile) · `karte.html` (Speisekarte nach Ländern, Lunch-Menü, Lästermeile, drucken) · `weinkarte.html` (alle Weine nach Gruppen) · `feiern.html` (zwei Etagen, Bankettmenüs, Anfrage im Fenster) · `anlaesse.html` (Gourmetkreuzfahrt, Rückblick) · `team.html` · `kontakt.html` · `gutschein.html` · `impressum.html` · `datenschutz.html` · `agb.html` · `404.html` · `robots.txt` (Studie gesperrt) · `sitemap.xml`

## Lästermeile (Robert 19.10.2026, 20:05)

- Karte (`karte.html#laestermeile`): Fassung 3 «Tischset aus Zementfliesen» aus `website/_varianten-laestermeile/` (15 Fassungen, Pfeiltasten). Fliesenband oben und unten, Papier-Tischset mit Innenrand, Apéro und Bar als schräge Abzüge. CSS-Block `.lmk` am Ende von `haus.css`.
- Startseite: Fliesenband schmaler (44–68 px), dazu dasselbe Band oben am Abschnitt (Robert 20:09; der Streifen hell/dunkel war nur ein Versuch). Knopf «Karte der Lästermeile» seit 20:15 im Abschnitt auf der Naht, einfarbig blau (20:18; zweifarbig war ein Versuch), Abschnitt unten länger; Bänder auf der Karte gleich schmal. Sicherung: `website/_sicherung/vor-laestermeile-tischset-*`.

## Lunch-Menü (Robert 19.10.2026, 20:10)

- Karte (`karte.html#mittag`): Fassung 14 «Mosaik» aus `website/_varianten/lunch-15.html` (15 Fassungen, Pfeiltasten), Menükarte auf Roberts Wort edler: Papier `#F6F3EC` mit Doppelrahmen, Zeichen des Hauses (`zeichen()` in `bau.py`), «Lunch» gesperrt, Gänge mittig mit ✶. Gänge und Preis aus `inhalt/lunch.json`. Die sieben Fotos sind Stimmung, keines zeigt die Gerichte der Woche; `tb-fisch` und `tb-glas` sind Gästefotos (Rechte, siehe Öffnungszeiten). CSS-Block `.lum` am Ende von `haus.css`. Sicherung: `website/_sicherung/vor-lunch-mosaik-2010/`.

- Karte nach Ländern seit 19.10.2026, 20:25: Fassung 1 «Mittelachse» aus `website/_varianten-laender/` (eine Spalte mittig, Name, Beschreibung, Preis untereinander, Stern unter dem Land; Bild wechselt links und rechts). Sicherung `website/_sicherung/vor-laender-mittelachse-*`.

## Wein zum Gang (Robert 19.10.2026, 20:4x)

- Karte (`karte.html#wein-zum-gang`): Fassung 4 «Jonas schenkt ein» aus `website/_varianten/wein-gang-luxus.html` (Runde 3; Runde 1 `wein-gang-15.html` und Runde 2 `wein-gang-klar.html` abgelehnt). Dunkel, links Jonas und das Glas als Abzüge mit weissem Rand, rechts die Wahl der Küche, drei gedruckte Kärtchen fliegen von unten herein (beim Hereinkommen und bei jedem Wechsel). Ein Kärtchen öffnet das Wein-Fenster.
- Quelle: `website/funktionen.py › wein_zum_gang(foto)` (Weinauswahl je Küche wie vorher, jetzt fertig im HTML), CSS-Block `.wzg4` in `assets/css/funktionen.css`, Verhalten Teil 4 in `assets/js/funktionen.js`. Sicherung davor: `website/_sicherung/vor-wein-zum-gang-4-*`.
- Gemessen 6-fach gedrosselt: 120 Bilder/s, nichts über 50 ms, CLS 0.

## Anlass-Seite «Teller zuerst» (Robert 19.10.2026, 20:5x)

- `anlaesse.html#naechster`: Fassung 14 aus `website/_varianten-kreuzfahrt/` (15 Fassungen, Pfeiltasten). Links Teller gross (`kf-teller`) mit Abzug (`kf-anrichten`), rechts «Four Hands.», Namen, alle Sätze aus der Quelle (Satz «Welcome-Apéro …» in `haus.json` nachgetragen), Zeit, Knopf.
- `#rueckblick` «Was war.» in derselben Handschrift: je Termin ein ganzes Foto (Rahmen folgt dem Bild), Seiten im Wechsel. Fotos über `bild` in `haus.json › anlaesse` (platanen, feuerwerk, schaefli, stier).
- **Rechte:** `kf-*` von excellence.ch (Twerenbold, Herkunft `_quelle/extern/excellence/herkunft.json`), `feuerwerk` laut Dateiname «Bildrecht Keller»: vor jeder Veröffentlichung klären.
- Quelle `bau.py › anlaesse_seite`, CSS-Block `.tz`/`.tzr` am Ende von `haus.css`. Gemessen 6-fach gedrosselt 120 Bilder/s, nichts über 50 ms, CLS 0. Sicherung `website/_sicherung/vor-anlaesse-teller-1910/`.

## Kopf «Events & Termine» (Robert 19.10.2026, 21:1x)

- `anlaesse.html`: Fassung 6 «Nachtblaue Spalte» aus `website/_varianten/events-kopf-runde4.html` (vorher kurz Passepartout mit Abendschiff, abgelöst; Runden: `events-kopf-15`, `-20`, `-8-bilder`, `-runde3`, `-runde4`). Links nachtblaue Spalte mit Titel, Satz und nächstem Anlass aus `haus.json`, rechts das Feuerwerk über zwei Drittel.
- Bild `feuerwerk-ki` in `bilder.py` (nur im Kopf; `feuerwerk` bleibt das Originalfoto im Rückblick): auf Roberts Wort (19.10.2026) mit KI neu erzeugt aus dem Foto der Website des Hauses (Higgsfield gpt_image_2_5, 2,75 Credits, 2336 px), Quelle `_quelle/website/bearbeitet/feuerwerk-ki.png`, Kopie in `~/Downloads/Design & Bildserien/Schlössli Feuerwerk/`. KI-Bild = Platzhalter bis zu einem echten Foto des Hauses. CSS-Block `.esp` am Ende von `haus.css` (`.epp` darüber ungenutzt), Auftakt wartet auf `.esp__bild img`. Sicherungen: `website/_sicherung/vor-events-kopf-passepartout-2102/`, `vor-events-kopf-feuerwerk-2118/`.

## Plakatwand «Angeschlagen am Hafen»: Band, Tausch, Karte (Robert 19.10.2026, 21:1x–21:2x)

- Kleine Plakate gerade in einer Reihe (Robert «nicht so schräg»), mit demselben blauen Band wie das grosse. Jede Karte trägt dieselben Angaben (`funktionen.py › kalender › karte`), damit sie tauschen können.
- Tausch: ein Tipp auf ein kleines Plakat legt es gross, das grosse fliegt an seinen Platz (nur transform, Feder 0,7 s, `funktionen.js › tauschen`, Ziel wird nach dem neuen Text gemessen).
- Die Karte des Termins steht neben dem grossen Plakat unter den kleinen (`.ap__r`; Robert «man sieht gar nicht, was unten passiert»): Papier mit Doppelrahmen, Zeichen, Tag gross, Titel, Zeit, Text, Knöpfe (`#kalender .ktd` in `funktionen.css`).
- Seit 21:3x (Robert «die Bildgrösse richtet sich nach der Textmenge»): das grosse Plakat hat festes Format 3:4 und gibt allein die Höhe vor (`.ap__r` mit Höhe 0 und Mindesthöhe 100 %); alle Termine liegen als Karten übereinander im selben Feld, gezeigt wird einer (Tag, Titel, Zeit, erster Satz, Knöpfe); der ganze Text steht im Fenster «Alles lesen» (`#fe-termin`). Geprüft bei 1440, 1000 und 390 px. Sicherung `website/_sicherung/vor-plakat-feste-groesse-2125/`.
- Gemessen: 0 px Scrollversatz beim Tausch (Rechner und Handy), 6-fach gedrosselt 120 Bilder/s, CLS 0. Sicherungen `website/_sicherung/vor-plakat-tausch-2115/`, `vor-plakat-nebeneinander-2120/`.

- Bilder der Plakate seit 21:3x (Robert «bessere Bilder», Feuerwerk bleibt): Kreuzfahrt `kf-deck-abend` (Sonnendeck in der Dämmerung, Excellence), Ehemaligen Lunch `platanen` (Bild des Hauses zum Anlass), Kitchen Party `kp-party` (Schäfli-Seite der Kitchen Party), 4-Hands-Lunch `pa-teller` (Papageno, aus dem Guide Michelin, Herkunft `_quelle/extern/papageno/`). Rechte jeweils beim Anbieter, nur Designstudie.

## Weinkarte Kopf «Das Kellerbuch» (Robert 19.10.2026, 21:4x)

- Fassung 9 aus `website/_varianten-weinkopf/` (20 Fassungen, Pfeiltasten): aufgeschlagenes Buch, links das Glas am See, rechts die Inhaltsseite, je Art Zeile mit Punktlinie und Zahl, darunter Weine · Weingüter · Länder (gezählt aus der Karte). Quelle `bau.py › weinkarte_seite`, CSS-Block `.wkb` am Ende von `haus.css`, `haus.js` Teil 1 kennt `.wkb__bild`. Gemessen 6-fach gedrosselt 116 Bilder/s, CLS 0; geprüft bei 1440, 1000 und 390 px. Sicherung `website/_sicherung/vor-weinkopf-kellerbuch-2145/`. Die alten `.wkopf`-Regeln sind nur noch Reste.

## Farbwelt

Seit 19.10.2026 (Robert) «Ton in Ton»: alle Blautöne auf den Farbton des Platztellers gedreht, Grund `--nacht` #0b1d3d. Werkzeug `website/farbwelt.py` (Drehung +21°, warme Töne bleiben), Sicherung davor in `website/_sicherung/vor-farbwelt-ton-in-ton-*`. Neue Farben nur noch in diesem Farbton wählen.

## Kontakt-Kopf «Briefkopf» (Robert 19.10.2026, 21:1x)

- `kontakt.html#kopf`: Fassung 03 «Der Briefkopf» aus `website/_varianten/kontakt-links.html` (Runde 4; Runde 1 `kontakt-kopf-15.html`, Runde 2 `kontakt-kopf-runde2.html` und Runde 3 `kontakt-fein.html` abgelehnt). Links alles mittig wie auf dem Briefpapier: Zeichen, Wortmarke, «by Christian Kuchler», Linie, Titel, Satz, Linie, Adresse, Tage und Zeiten, Knöpfe. Rechts das Schild wie bisher, Bild 38 % breit.
- Quelle: `bau.py › kontakt_seite` (eigener Kopf statt `seitenkopf`), CSS-Block `.kopf--brief` / `.kb` am Ende von `haus.css`. Sicherung: `website/_sicherung/vor-kontakt-briefkopf-2110/`.
- Gemessen 6-fach gedrosselt: Kopf 117 Bilder/s, nichts über 50 ms, CLS 0. Geprüft 1440, 1024, 390, 320 px in WebKit und Chromium, keine Fehler, nichts läuft seitlich über.

## Heikle Stellen (beim Weiterbauen nicht kaputt machen)

- **Die Linie:** Jedes Foto mit Horizont sitzt in einem ruhenden Rahmen `.anl` (Linie bei `--hz`), nur die `figure` darin bewegt sich. Grids rechnen die Zeilenhöhe in `cqw` aus Breite × Verhältnis × Horizont; `.innen` ist der Container. Neue Fotos: Horizont in `bilder.py` messen, nie schätzen.
- **Auftakt (seit 19.10.2026 «Am Tisch», Fassung 07.6 aus `website/_varianten/teller-10.html`):** Teller von oben (`anguria`), Name und Adresse als Prägung im Abstand um den Rand (SVG-Ring, 1000 Einheiten, Teller füllt 735), links «Am», rechts «Tisch.». Reservieren nur oben rechts in der Leiste (Robert). Einziger bewegter Teil: der Ring dreht beim Scrollen mit (`haus.js` Teil 9). Gemessen 6-fach gedrosselt 120 Bilder/s, CLS 0. Teller seit 19.10. per KI nachgeschärft (`website/teller_bild.py`, Quelle `_quelle/website/bearbeitet/`). Darunter ein Tischläufer aus Leinen quer durchs Bild (Fläche 14 aus `_varianten/hintergrund-15.html`, Kachel aus `website/leinen.py`, CSS `.auftakt--teller::before`); «Am» und «Tisch.» stehen am Rechner in Tinte auf dem Leinen, am Handy weiss auf Dunkel. Die Fläche drumherum ist das Leder des Platztellers im Nachtblau der Seite (`website/leder.py` → `leder-nacht.webp` + `leder-narbe.webp`, Massstab = Narbung im Tellerfoto). Seit 19.10.2026 Farbwelt «Ton in Ton» (Fassung 02 aus `_varianten/farben-12.html`): Grund, Leder (`leder-ton.webp`) und «Am»/«Tisch.» im dunklen Blau des Platztellers `#0b1d3d`, Block am Ende von `haus.css`. Der alte Foto-Auftakt liegt in `website/_sicherung/vor-teller-auftakt-*`.
- **Willkommen (seit 19.10.2026, 18:20):** Der erste Teil nach dem Auftakt ist der Brief des Hauses (`#willkommen`, Fassung 01 aus `website/_varianten/willkommen.html`, Robert «einladender»), links Stuhl gross, Platanen und Abend klein. Er ersetzt «Terrasse und Hafen» mit den Stimmen der Führer und dem Wappen; die alten Stellen in `haus.css` (`.thb__*`) sind nur noch Reste. Sicherung: `website/_sicherung/*.vor-brief-1820`. Gemessen 6-fach gedrosselt 117 Bilder/s, CLS 0.
- **Erstes Fenster (seit 19.10.2026, 18:28):** Gäste unter dem Baum am Ufer (Gästefoto von Tripadvisor, `baum` in `bilder.py`, **Rechte bei den Gästen, vor jeder Veröffentlichung durch ein Foto des Hauses ersetzen**), Satz «Eine kleine Auszeit vom Alltag.» (aus dem Anlass-Satz der Startseite des Hauses). Zehn Bildideen in `website/_varianten/fenster/`.
- **Kopf der Karte «Kompass» (seit 19.10.2026, 20:45):** Fassung 16 aus `website/_varianten/karte-kopf-15.html`. Links der Zeiger der Wortmarke, an seinen Enden die vier Teile der Karte als feine Landkarten (`website/landkarten.py` → `assets/svg/land-*.svg`, Umrisse Natural Earth gemeinfrei, `_quelle/extern/geo/`), Stadt in Handschrift (Caveat, OFL, `assets/fonts/Caveat-500.woff`); jede Karte springt zum Land (`#land-…`). Mitte Titel, Satz, Knopf auf einer Achse, rechts die Suppe. `bau.py › karte_kopf`, CSS-Block `.kko` am Ende von `haus.css`. Gemessen 6-fach gedrosselt 112 Bilder/s im Kopf, CLS 0. Sicherung: `website/_sicherung/vor-kompass-kopf-2042/`. Abgelehnt auf dem Weg: Kartenmedaillons mit Gradnetz, kräftige Farbwolken, Wellen-Kritzel.
- **Zwei Häuser (team.html #schaefli, seit 19.10.2026, 21:15):** Zwei weisse Karten nebeneinander (Handy untereinander), je mit feinem Innenrahmen, Hausfoto oben (`haus`, `schaefli`), Titel, Auszeichnungen in Originalfarben auf Weiss, kurzer Text, Knopf zum Haus. Links das Schlössli: GaultMillau 15, Michelin 2025 «Favorit», Falstaff 91 (dieselben Logos wie auf der Startseite). Rechts das Schäfli: Michelin-Abzeichen rot ohne Jahreszahl (`ehre-schaefli-michelin.webp`), GaultMillau mit den vier Mützen «18» aus der Plakette des Schäfli in GM-Rot plus Schriftzug aus dem GM-Logo (`ehre-schaefli-gaultmillau.webp`), Falstaff 98 (belegt in `Taverne zum Schäfli Wigoltingen/_quelle/extern/portale/`), Knopf «Zum Schäfli» auf schaefli-wigoltingen.ch. Abgelehnt (Robert): Tafel auf Leder im Nachtblau; nur das Schäfli allein. Code `funktionen.py` `schwester()` + Block am Ende von `funktionen.css`; Sicherungen `website/_sicherung/2026-10-19-vor-auszeichnung-schaefli/`.
- **Öffnungszeiten (#abend, seit 19.10.2026, 19:40):** «Der Tag aus Bildern», Fassung 01 aus `website/_varianten/zeiten-bilder-15.html`. Vier Fotos, die auf der ganzen Website sonst nicht vorkommen, **ganz gezeigt, ohne Ausschnitt** (Robert: kein Hineinzoomen, der Rahmen folgt dem Bild): Rotbarbe 11:30 (`tb-fisch`), Glas Weisswein 13:30 (`tb-glas`), Thunfisch mit Kaviar 18:00 (`tb-teller`), Masten im Abendrot 20:00 bis 23:00 (`tb-dunkel`). Alle gleich hoch, Breite nach Seitenverhältnis (`--a`), am Handy zwei Zeilen (`.tb__bruch`). **Alle vier sind Gästefotos von Tripadvisor, Rechte bei den Gästen, vor jeder Veröffentlichung durch Fotos des Hauses ersetzen** (neue Fotos gleich ins Seitenverhältnis gedacht liefern, dann passt der Streifen von selbst). Abgelehnt: 15 Linien-Fassungen, Bilder als Ausschnitt in Zeit-breiten Kacheln. Sicherungen: `website/_sicherung/vor-zeiten-bilder-1909/`, `vor-zeiten-ganz-*`.
- **Speisekarte im Wechsel (karte.html #laender, seit 19.10.2026, 20:10):** Fassung 04 aus `website/_varianten/karte-bilder-15.html` (Robert). Je Land ein ganzes Foto aus der Küche, abwechselnd links und rechts, die Gerichte in zwei Spalten daneben (`bau.py › karte_seite`, Zuordnung `kw_bild`; CSS-Block `.kw` in `haus.css`). Die Fotos stehen fürs Land, nicht für ein Gericht, ausser den Tortelloni bei den Klassikern; ändert sich die Karte, nur die Zuordnung prüfen. Am Handy Bild über Liste, im Druck ohne Bilder. Gemessen 6-fach gedrosselt 119 Bilder/s, CLS 0. Sicherung: `website/_sicherung/vor-karte-wechsel-2010/`.
- **Geschichte als Chronik-Wand (seit 19.10.2026, 19:30):** `#besen` ist eine Wand aus elf Bildern auf 12 Spalten (Zeilen in `cqw`), mittendrin der Titel als blaue Kachel, Text mittig (Fassung 01 aus `website/_varianten/besen2.html`, scharf in `besen-wand.html`). Acht Bilder aus Heft 2 der Gemeinde (1994) sind mit KI neu gezeichnet (`_quelle/presse/heft-bilder/ki/`, Higgsfield gpt_image_2_5, 24,75 Credits, Roberts Ja). Bei der Anzeige steht der Text nach dem Original, die Fassung mit erfundenem KI-Text liegt daneben als `*-text-falsch.png`. Die Postkarte ist nur oben gezeigt, weil die KI unten einen Brief erfunden hat. **Rechte beim Heft der Gemeinde, nur zur Anschauung: vor jeder Veröffentlichung Erlaubnis der Gemeinde Bottighofen holen.** Auftritt: jedes Bild wächst aus 86 % und zoomt von 124 % hinein, nacheinander (`.chw` am Ende von `haus.css`). Gemessen 6-fach gedrosselt 121 Bilder/s, CLS 0. Sicherung: `website/_sicherung/*.vor-chronikwand-1923`.
- **Anfahrt auf kontakt.html (seit 19.10.2026, 21:35):** Fassung 06 «Nachtblaue Seekarte» aus `website/_varianten/anfahrt-20.html` (Runde 2; Runde 1 `anfahrt-15.html`, davor `kontakt-15.html` mit Zeiten abgelehnt). Robert: der Abschnitt zeigt nur die Anfahrt, Zeiten und Kontakt stehen im Fuss. Nachtblau mit feinen Wellenlinien, links die Koordinaten aus `haus.json`, rechts Satz und Bahnsatz, Links zu Karte und Route (OpenStreetMap). Die alte Tafel mit Zeiten, **Ferien** und Kontakt ist weg; die Ferien stehen damit auf der Kontaktseite nicht mehr. `bau.py › kontakt_seite`, CSS-Block `.ank` am Ende von `haus.css`. Gemessen 6-fach gedrosselt 119 Bilder/s, CLS 0.003. Sicherung: `website/_sicherung/vor-anfahrt-seekarte-2130/`.
- **Leiste «Speisefolge» (seit 20.10.2026, Fassung 66 aus `website/_varianten/wege-30.html`, von Robert gewählt und verfeinert):** links das Zeichen, in der Mitte «Menü» wie ein Kartenkopf, rechts die Reservation. Das Menü ist eine Speisefolge auf Papier (`bau.py › SPEISEFOLGE`, Karte zuerst, Lästermeile nach dem Wein), CSS-Block «Leiste Speisefolge» am Ende von `haus.css`, Verhalten `haus.js` Teil 11. Die Karte steigt von unten herein, die Gänge kommen aus dem Schlitz; gemessen 4- und 6-fach gedrosselt 120 Bilder/s. Sicherung des Stands davor: `website/_sicherung/vor-speisefolge-2026-10-20/`.
- **Fenster:** Bauart ohne Beschneiden (Bild und Satz `sticky`, z-index −1, die Nachbarn decken). Kein Vorfahr der Abschnitte darf einen Stapelkontext bilden (kein transform/opacity/z-index auf `main`).
- **Lästermeile:** Titel liegt zweimal übereinander, links weiss, rechts Tinte, je mit `clip-path` an der Bildschirmmitte geteilt.
- **Wappen Bottighofen (nur Demo):** Die Gemeinde-Stimme im Hafen (`thb__stimme` in `bau.py`) zeigt seit 19.10.2026 auf Roberts Wort das Gemeindewappen (`assets/img/wappen-bottighofen.svg`, Herkunft `_quelle/extern/wappen/herkunft.json`). Nach Wappenschutzgesetz Art. 8 darf es nur die Gemeinde selbst verwenden: **vor jeder Veröffentlichung entfernen oder schriftliche Erlaubnis der Gemeinde Bottighofen einholen.** Ein Kommentar in `bau.py` sagt dasselbe.
- **Formulare:** schicken in der Studie nichts ab (zeigen nur den Dank mit Hinweis «Designstudie»). Reservation = Buchungsmaske von gastronovi im Fenster (Rahmen erlaubt, `x-frame-options: ALLOWALL`, geprüft 19.10.2026).

## Sicherungen

Neuer Ordner, nichts Bestehendes überschrieben. `~/SecondBrain/.claude/launch.json` vor dem Eintrag gesichert unter `website/_sicherung/launch.json.vor-schloessli-2026-10-19`.

## Gäste-Funktionen (Runde 3, 19.10.2026, Robert «okay alle einbaun»)

- `website/funktionen_daten.py` schreibt `assets/data/weine.json` (468 Weine, Land aus den Überschriften der Karte, Rebsorte nur wörtlich aus dem Namen).
- `website/funktionen.py` baut die Teile: Reservation mit zwei Reitern (Anfrage mit Flasche, Platz, Allergenen, Wünschen · Buchungsmaske gastronovi), Weinberater, Wein-Ansicht, Wein zum Gang, Abend zusammenstellen (`abend.html`), Gutschein als Karte, Kalender mit Plätze-Anfrage, Blick in die Küche, Schwesterhaus, Der See heute.
- «Ihr Abend» (`abend.html`, seit 20.10.2026): Anlass, Platz und Menü als Bildkarten (`funktionen.py › bildwahl`), Personen mit Plus und Minus, die gewählten Bilder oben auf dem Zettel; CSS-Block «Ihr Abend mit Bildkarten» am Ende von `funktionen.css`, Verhalten `funktionen.js` Teil 5b. Der Platz läuft über das versteckte Feld `platz`, das der Zettel liest. Zweite Runde (20.10.): Überschrift «Ihr Abend am Tisch.», Karte als Liste zum Ankreuzen, Zettel als Papier mit allen Angaben (auch Wünsche, Name, Kontakt). Der Weinberater führt mit `?von=abend` zurück nach `abend.html#az-wein`; alle Eingaben bleiben in sessionStorage `schloessli-abend` stehen. Sicherung davor: `website/_sicherung/vor-abend-bilder-2026-10-20/`.
- `assets/css/funktionen.css` und `assets/js/funktionen.js` (Sonnenuntergang aus dem Sonnenstand gerechnet, keine fremde Abfrage; Flasche in sessionStorage; nichts wird verschickt).
- Prüfung der Bedienung: `node website/_qa/funktionen.js webkit 1440`.

## Weinberater «Der Keller» und Weinwelt (19.10.2026, 20:50)

- Auswahl neu: Arten als echte Flaschen in Kacheln, Länder als runde Flaggen, Rebsorte/Preis/Flasche als Auswahl im Hausstil; jede Möglichkeit zeigt, wie viele Weine danach noch passen. Code in `funktionen.py › weinberater()`, `assets/js/funktionen.js`, `assets/css/funktionen.css`. Sicherung davor: `website/_sicherung/vor-weinwelt-2026-10-19/`.
- Kärtchen und Wein-Ansicht: Landschaft der Herkunft, freigestellte Flasche, Flagge, Angaben mit Zeichen, Weine desselben Weinguts.
- Bilder: `website/wein_bilder.py` → `assets/img/wein/`, Zuordnung `assets/data/wein-bilder.json`. 212 von 468 Weinen mit echtem Flaschenfoto (Erzeuger und Wein müssen passen, 14 Fehltreffer von Hand ausgeschlossen, Liste `NICHT`), alle 468 mit Landschaft. Rohdaten und Zuordnung in `_quelle/wein-bilder/`.
- **Rechte:** Flaschenfotos und Landschaften ausserhalb der Schweiz stammen von Vivino (Bilder der Weingüter bzw. Vivinos), nur zur Anschauung in der Designstudie. Schweizer Landschaften von Wikimedia Commons (CC BY-SA, Urheber in `_quelle/wein-bilder/herkunft-schweiz.json`, Namensnennung nötig). **Vor jeder Veröffentlichung klären oder durch Bilder der Weingüter mit Erlaubnis ersetzen.**
- Gemessen 6-fach gedrosselt: Weinberater 120 Bilder/s, Weinliste 119 Bilder/s, CLS 0.

## Weinliste als Platten je Weingut (19.10.2026, 21:05)

- Fassung 01 aus `website/_varianten/weinliste-3d.html` (vier Fassungen, Robert: «jede Kachel so wie bei Erstens», Logo klein oben, Weingut gross mittig). Je Land ein Kapitel mit Flagge, je Weingut eine erhabene Platte, die Weine in der Kuhle; jede Zeile öffnet die Wein-Ansicht. Code: `bau.py › weinkarte_seite`, CSS-Block `.wl__*` am Ende von `haus.css`. Sicherung: `website/_sicherung/vor-weinliste-platten-2055/`.
- Logos: `website/weingut_logos.py` (suchen → holen → tafel → aufbereiten), eigene Website je Weingut, in Originalfarben (`f-*.webp`, weisser Grund durchsichtig), weisse oder blasse Logos einfarbig im Blau der Seite (`m-*.webp`), Zuordnung `assets/data/weingut-logos.json`. 84 Weingüter mit Logo, von Hand geprüft (Liste `FALSCH`); ohne Logo ein Monogramm, ohne Weingut (Bordeaux, Schweizer Schaumwein) die Flagge.
- **Rechte:** Logos sind Marken der Weingüter, nur zur Anschauung in der Designstudie. Vor jeder Veröffentlichung Erlaubnis holen oder weglassen.
- Gemessen 6-fach gedrosselt: Rechner 114 Bilder/s, Handy 96 Bilder/s, nichts über 50 ms, CLS 0.

### Geschmack, Weinstil, Weingut und Suche nach Geschmack (19.10.2026, 21:30)

- Wein-Ansicht zeigt zusätzlich: Alkohol und Verschluss, «Im Glas» (Körper, Säure, Süsse, Tannin, Perlage), «Im Duft und am Gaumen» (Aromen), «Passt zu», «Der Weinstil», «Das Weingut».
- Weinberater mit Umschalter «Klassisch» / «Nach Geschmack» (Körper, Säure, Süsse, Tannin als Stufen, Aromen als Farbtafel, «Passt zu»); beide Auswahlen gelten zusammen.
- Daten: `website/wein_infos.py` (holen · geschmack · bauen) → `assets/data/wein-infos.json`. Quelle Vivino (Weinseite und Geschmacks-Abfrage) nur bei sicherer Zuordnung, 9 weitere Fehltreffer in `NICHT`. Abdeckung: Geschmack 251, Aromen 235, Speisen 236, Weinstil 236, Weingut 104 von 468 Weinen. Roh in `_quelle/wein-bilder/seiten/`.
- Deutsche Texte in `website/wein_texte.py`: Aromawörter übersetzt, Weinstile aus Vivino übersetzt und gekürzt, Weingüter aus der Einleitung der Wikipedia-Artikel (`weingut_infos.py`, Roh `_quelle/wein-bilder/wikipedia.json`, Quelle verlinkt).
- **Rechte:** Vivino-Daten nur zur Anschauung in der Designstudie, vor Veröffentlichung klären; Wikipedia-Texte stehen unter CC BY-SA (Quelle ist je Weingut verlinkt).
- Gemessen 6-fach gedrosselt: Weinberater 117 Bilder/s, Weinliste 114 Bilder/s, CLS 0.
- 21:25: Arten (Schaumwein, Weiss …) als ruhiger Trenner mittig zwischen Linien (`.wl__art`), Länder mittig; Länder mit nur einer Platte teilen sich ein Kapitel, Rosé und Süsswein ein Block ohne Ländertitel. Filter über der Liste (Art, Land, Suche, Trefferzahl), Verhalten am Ende von `haus.js`. Schaumwein-Länder in `karten_lesen.py` korrigiert (Länder-Zwischenzeilen waren als Anmerkung gelesen). Gemessen 6-fach gedrosselt: 117 Bilder/s, CLS 0.

### Weinwelt: Bilder, Erzählung, Weingüter (19.10.2026, 22:05)

- **Robert 21:22:** Platte des Weinberaters ohne Tapete (`.keller.f-dunkel{background-image:none}`); Reiter «Klassisch / Nach Geschmack» gestaltet. **Achtung:** `assets/css/funktionen.css` stand um 21:24 plötzlich auf einem Stand ohne den Geschmacks-Block (401 Zeilen, fremder Schreibzugriff); der Block wurde neu geschrieben und steht jetzt am Ende der Datei. Zwei Chats nie an funktionen.* gleichzeitig.
- **Bilder statt Farbkreise:** `website/wein_bildchen.py` → `assets/img/wein/klein/` (13 Aromagruppen, 80 Aromawörter, 21 Speisen), Zuordnung `assets/data/wein-bildchen.json`. Quelle: die freigestellten Aroma- und Speisenbilder von Vivino (Speisen: `…/thumbs/…_932x810.png`, das breite Bild ist nur ein Ausschnitt). Nichts generiert, keine Kosten. Rechte bei Vivino, nur Designstudie.
- **Weingüter:** `website/weingut_recherche.py` + `website/inhalt/weingut-recherche.json`: 110 Erzeuger aus eigener Netz-Recherche (Weingut-Seiten, Fachpresse, Händlerprofile), je Eintrag die Quelle; dazu 36 aus Wikipedia (`wein_texte.py`). Jetzt 401 von 468 Weinen mit Weingut-Text. Ohne belegte Angaben: Arnaud Baillot (als Domaine vorhanden), Champagne Valentin Leflaive, Joel Nänni, Maison Meyer, San Barnaba, Ses Talaioles.
- **Erzählung je Wein (Robert «mehr Geschichte»):** `website/wein_regionen.py` mit Herkunftstexten für alle 50 Regionen der Karte (Landschaft, Klima, Boden, Trauben; allgemeines Weinwissen, bewusst ohne Zahlen) und einem Glossar der Begriffe im Weinnamen (Grand Cru, GG, Smaragd, Auslese, pas dosé …). `wein_infos.py bauen` setzt daraus je Wein «Woher er kommt» und «Was ihn ausmacht» zusammen (Art, Rebsorte, Jahrgang, Begriff, Struktur, Aromen, Alkohol, Flaschen; nur belegte Angaben). Reihenfolge im Fenster: Angaben → Woher er kommt → Das Weingut → Was ihn ausmacht → Im Glas (farbige Bahnen) → Aromen (bis drei Bildchen) → Passt zu (Teller) → Weinstil → Vom selben Weingut (Flaschen im Regal, ohne Foto die gezeichnete Flasche).
- Gemessen 6-fach gedrosselt: Weinberater 116 Bilder/s, Weinliste 114 Bilder/s, CLS 0.
- **Robert 21:4x «Schatten hinter den Bildern»:** Safari wirft bei `filter:drop-shadow` auf einem `<img>` mit `object-fit:contain` den Schatten des ganzen Kastens, nicht der Kontur. Behoben in `funktionen.css`: unter einem drop-shadow nie object-fit, Bilder mit `width:auto;height:auto;max-width/max-height` (Aromen im Berater und im Fenster, Speisen, Mini-Flaschen, Flaschen der Arten). Geprüft in WebKit (Playwright, `_qa`-Umgebung).
- 22:40 Events (`anlaesse.html`): Four-Hands-Teller rechts gerundet, kleiner Abzug ohne Rahmen gerundet; «Angeschlagen am Hafen» Plakate und Zettel als gerundete 3D-Kacheln (Block am Ende von `haus.css`, `#kalender`-Regeln dort statt in `funktionen.css`); Rückblick wechselt sanft in Pfeilrichtung (`haus.js` Kontaktbogen `zeig(n, dir)`). Sicherung: `website/_sicherung/vor-events-kacheln-2235/`.
