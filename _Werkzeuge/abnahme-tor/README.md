# Abnahme-Tor (seit 29.10.2026)

Pflicht laut `OBERCHEF-PAKET.md`, Abschnitt «Abnahme-Tor vor Robert». Gemessen wird gegen jeden Satz in `ROBERTS-KRITERIEN.md`. Ohne Grün des Tors sieht Robert nichts.

## Was es tut
1. **Inventar aus dem Werkzeug selbst** (`tor.js`): Das Tor öffnet jedes Ziel aus der Zielliste und klickt jede bedienbare Stelle an, die nichts verändert.
   - Jeder neue Zustand kommt ins Inventar: Navigation, Reiter, Fenster, «Neu erstellen», Vorlage, Dokument, Unterseite, Editor mit offener Leiste (Klick auf die grösste Schrift im Dokument, je hohes und queres Dokument).
   - Zustände werden an ihrer Kennung erkannt: Weg, aktive Navigation, offene Fenster, Titel, Dokumente.
   - Gleichartige Stücke im Inhalt (z. B. 231 Fotos) werden zu dritt bedient. Führt eins davon zu einem Dokument, werden alle bedient, denn jede Vorlage zählt einzeln. Navigationen werden immer vollständig bedient.
   - Bekommt ein Werkzeug neue Zustände, stehen sie beim nächsten Lauf im Inventar, ohne dass jemand eine Liste pflegt.
2. **Messung jedes Zustands**: WebKit 1440×900 mit Bild. Es laufen der Messlauf (`../messlauf/messen.js`) und die Ergänzungen in `seite.js`:
   - **K1** Rundknopf ohne eigene Fläche
   - **K2** Platzhalter abgeschnitten; Beschriftung ohne Luft im Knopf
   - **K4** leere Kachel und Hintergrund-Flächen (Bildprüfung)
   - **K6** gemeinsame linke Kante
   - **K7** Einzelwort in der letzten Zeile
   - **K8** blasser Platzhalter
   - **K10** Löcher und Mitte der Dokumente (Bildprüfung)
   - **K12** Stil: Versalien und Trennzeichen laut `stil` in der Zielliste; liegt ein `stilblatt.json` vor, sind dessen Werte einzutragen
   - **K14** doppelte Marke
   - **K15** zwei Wege zum selben Ziel
   - **K18** zu wenige Vorlagen

   Danach folgen Stichproben bei 1280×800, 1000×650 (Roberts Safari) und 390×844.
3. **Messlauf** (Pflicht vor jeder Übergabe, `../messlauf/messlauf.sh <haus>`, Anleitung `../messlauf/ANLEITUNG.md`): `lauf.js` startet ihn am Ende des Oberflächen-Laufs selbst (Chromium + WebKit, 1440/1280/390, Tafel unter `<ausgabe>/messlauf/`). Seine Messfunktion `messen.js` läuft ausserdem in jedem Zustand des Tors (Kriterien 1, 2, 3, 5, 7 «einzelwort», 13 «beschnitten»).
4. **Auswertung** (`auswertung.py`): Abdeckungstafel Zustand × Kriterium mit grün, rot, Auge (Kriterium A, Urteil mit dem Auge in `augen.json`), nicht prüfbar oder entfällt. Dazu kommen eine Fundliste mit Bild und, falls angegeben, die Gegenprobe gegen Roberts Funde.

## Aufruf
```
node lauf.js ziele-<haus>.json <haus>/_qa/abnahme-tor/<lauf> --parallel 4
python3 auswertung.py <haus>/_qa/abnahme-tor/<lauf> _Oberchef/zeigen/<haus>/abnahme-tor --titel "…" [--gegenprobe gegenprobe-<haus>.json] [--augen augen.json]
```
Die Zielliste `ziele-<haus>.json` kommt aus `../messlauf/ziele-<haus>.json`. Dazu kommen der Bereich (`bereich`), das Vorwissen im Browser (`localStorage`) und die Hausregeln (`stil`).

Gesperrt ist alles, was etwas verändert oder verschickt (`gefahr`). POST-Anfragen beantwortet das Tor selbst, damit kein Server schreibt; mailto und tel werden abgefangen.

## Gegenprobe
Jeder Fund Roberts kommt als Zeile in `gegenprobe-<haus>.json`: Kriterium und Suchmuster. Das Tor muss ihn am Stand vor der Reparatur finden. Findet es ihn nicht, wird erst das Tor erweitert, dann die Reparatur gemeldet.
Culinarium 29.10.: Der alte Stand der Plakatwerkstatt wurde aus den Sicherungen `*.vor-*-2026-10-29` unter `Culinarium Hannover/_qa/abnahme-tor/alt/` zusammengesetzt (Port 9187).

## Schnelle Fassung (seit 31.10.2026): `lauf-schnell.sh`, `tor-schnell.js`

**Warum.** Gemessen am Culinarium-Bestand (31.10.): Das alte Tor brauchte je Zustand rund 13 s, davon **0,3 s Messen** und 12 s Warten:
frischer Browser und Nachspielen des ganzen Klickwegs für jeden Zustand (4,2 s Laden + 7–9 s Weg), dazu bei jedem Schritt bis 2,5 s Warten auf
Einblend-Animationen. Die Plakatwerkstatt (464 Zustände) brauchte so 305 min allein für 1440 px, die Stichproben in anderen Breiten noch einmal 14–16 s je Zustand.
Ein Volllauf aller Werkzeuge waren Tage; in der Cloud 5.538 Rechner-Minuten.

**Was anders ist** (gleiche Messfunktionen `messen.js` und `seite.js`, gleiche Kriterien, gleiche Ausgabe für `auswertung.py`):
1. Ein Browser bleibt offen. Jeder Zustand wird an Ort und Stelle erkundet und wieder zurückgenommen (Escape bei Fenstern, Zurück bei Adresswechsel,
   Reiter erneut anklicken). Zum nächsten Zustand geht es über den gemeinsamen Vorfahren, nicht von vorn. Nur wenn der Rückweg nicht ankommt,
   wird der Weg einmal frisch nachgespielt (steht als `zaehler.nachgespielt` im Inventar).
2. Während der Messung sind Einblend-Animationen aus (`reducedMotion` + Stil mit 1-ms-Dauer). Gewartet wird auf Netz und DOM (150 ms Ruhe), nicht auf feste Fristen.
   Bewegung (Kriterien 34, 37) misst wie bisher `bewegung-tor.js` mit Bewegung.
3. **Jeder Zustand in jeder Breite**: 1440, 1280, 1000 (Roberts Safari) und 390 im selben Fenster durch Grössenwechsel, nicht mehr nur Stichproben.
   Am Handy zusätzlich «Menü offen» in Start- und Navigationszuständen. Ausgabe: `inventar.json` + `bilder/` (1440), `stich-<W>.json` + `stich-<W>/` je weitere Breite.
4. Gleiche Layouts werden erkannt (`skelett`: Gerüst der sichtbaren Elemente ohne Text; `gleichWie`, wenn Gerüst und Fundmenge gleich sind). Gemessen wird trotzdem
   jeder Zustand, denn gleiches Gerüst heisst nicht gleiche Funde (Fotos derselben Sammlung haben verschiedene Seitenverhältnisse). Die Tafel zeigt es in der Zeile.
5. Gleichartige Stücke ohne Dokument: die ersten drei und dazu das mit dem längsten und dem kürzesten Text.

**Aufruf**
```
./lauf-schnell.sh <haus> <lauf-name> [P=3] [k1 k2 …]       # alles: Tore je Werkzeug (P gleichzeitig), Bewegung, Dokumente, Auswertung, Messwerte
./lauf-schnell.sh culinarium 0111-werkbank 1 werkbank      # ein Werkzeug gleich nach dem Bau
node tor-schnell.js ziele-<haus>.json <ausgabe> --nur <k> [--breiten 1440,1280,1000,390] [--max 700] [--tiefe 4]
python3 vergleich.py <lauf-alt> <lauf-neu> [k …]            # findet der neue Lauf jede Fundstelle des alten? (Art + Stelle + Meldung, alle Breiten)
python3 zeiten.py <lauf>                                    # Zustände, Minuten, Sekunden je Zustand, Rückwege je Werkzeug
```
Tafel: `http://localhost:8978/haus/_Oberchef/zeigen/<haus>/abnahme-tor/<lauf-name>/index.html`. Speicher: ein WebKit 400–800 MB, P=3 ist auf dem 24-GB-Mac sicher.
`TOR_BEWEGUNG=1` lässt die Animationen an (nur zum Vergleich). `TOR_HAENGER_MIN`, `TOR_KLICK_MIN` wie beim alten Tor.

**Gemessen am Culinarium (31.10.2026, gleicher Stand, altes gegen neues Tor):** siehe unten «Messwerte».

## Grundlinie für Kriterium 34 (Oberchef 3.11.2026, Nachtbau Schlössli)
`bewegung-tor.js` misst zuerst eine Vergleichsseite mit derselben Arbeit wie die Startbilder der Werkzeuge (zwölf grosse Fotos mit Rauschen, Zoom beim Erscheinen, Scroll-Zeitachse wie im Kleid) auf demselben Rechner und hebt die Schwellen um das, was der Rechner selbst nicht schafft (Ruckler: Grundlinie + 2, mindestens 2; p95: 1,5 × Grundlinie, mindestens 34 ms). Beleg: Auf den GitHub-Rechnern (2 Kerne, WebKit ohne GPU) war Kriterium 34 in allen sieben Werkzeugen des Schlössli rot, auch im nahezu stillen Hafenbüro (78 Bilder über 50 ms von 259), während dieselben Seiten in Chromium mit 12-fach gedrosselter Rechenleistung glatt liefen (höchstens 1 Bild über 50 ms). Die Grundlinie steht in `bewegung.json` (`grundlinie`) und in jedem Fund.

`bewegung-tor.js`, Kriterium 37 «bleibt unsichtbar» (4.11.2026): ein natives `<select>` mit `opacity:0` und `pointer-events:none` zählt nicht. Beleg: Hausdruckerei Mail-Seite, `lib/auswahl.css` Zeile 4 `.hwahl-nativ` – das echte Auswahlfeld liegt absichtlich unsichtbar unter dem eigenen Auswahlknopf («Mailchimp / Brevo / Anderes Programm»), rot in allen 40 Zuständen, obwohl der sichtbare Knopf da ist.

`bewegung-tor.js`, Kriterium 37 «bleibt unsichtbar», zweite Schärfung (4.11.2026): (a) nur Stücke, die auch waagrecht im Fenster liegen – die Regel prüfte nur oben/unten. Beleg: Werkbank, Band «Ideen» (`article.idee` 04–12 bei x = 1879–6703 px in einem 1440 px breiten Fenster, waagrechtes Band, erscheint beim seitlichen Blättern), rot in allen 82 Zuständen von Werkbank und KI. (b) Stücke mit `pointer-events:none` zählen nicht, wenn sie ein `<select>` sind oder ein gleichartiges Geschwister sichtbar ist (geparktes Glied einer Reihe; ein nicht ausgelöster Auftritt lässt die ganze Reihe unsichtbar und bleibt rot). Beleg: Feed-Fächer der Werkbank, `a.fblatt[data-p="3"|"-3"|"-4"]` sind geparkte Blätter ausserhalb des Fächers, absichtlich `opacity:0` und ohne Klick.

`tor-schnell.js` (4.11.2026): vor jedem Kachel- und Blattbild wird die Stelle ins Fenster gescrollt und bis 2,5 s auf ihre Bilder gewartet. Beleg: Hausdruckerei «Arten und Vorlagen» / «Neu erstellen», WebKit 1440: die Vorschau-Blätter unterhalb des Fensters (`span.stueck__satz`, Bilder mit `loading="lazy"`) wurden per Ganzseitenbild aufgenommen, ohne dass WebKit sie nachlud – 6× «Kachel wirkt leer», 15× Loch, 8× Mitte, im Zustandsbild sind dieselben Blätter am Fensterrand angeschnitten und noch leer.

`bewegung-tor.js`, Kriterium 34, Messung gegen die Last im selben Augenblick (4.11.2026): Grundlinie direkt vor jeder Seite neu, bei Rot ein zweiter Lauf, der bessere zählt. Beleg: Hafenbüro mit unverändertem Code 70–75 Ruckler im Volllauf (Commit fb2eb3a, drei Tore gleichzeitig auf 2 Kernen) und 2 Ruckler im Teillauf (b2a249e); Markenbuch-Hausregeln 8 und 38 Ruckler in denselben zwei Läufen. Die Messung zeigte die Auslastung des Rechners, nicht die Seite. Echtes Ruckeln wiederholt sich im zweiten Lauf, eine Lastspitze nicht.

`seite.js` + `tor-schnell.js`, Kriterium 4 «leer-bild», **K4 feste Ebenen** (4.11.2026): (a) Kacheln in einer festen Ebene (`position:fixed`, z. B. die Fussleiste) werden im Fensterbild ausgeschnitten, nicht im Ganzseitenbild. Beleg: Kartenpult 024 «Website → Weinkarte», WebKit 1440: `footer#leiste > div.wo-leiste__kn` «fast einfarbig (Streuung 1.03)» – der Ausschnitt `pairing-karte-024-f0.jpg` zeigt hellen Seitenhintergrund, im Zustandsbild stehen an derselben Stelle fünf Glasknöpfe mit deutlichen Symbolen (Ganzseitenbild: die feste Leiste steht dort nicht an ihrer Fensterstelle). Lokal (Chromium, Fensterbild) haben dieselben Knöpfe Streuung 19–25. (b) Kacheln, deren Mitte unter einer fremden festen Ebene liegt (offener Dialog mit Schleier), werden nicht ins Bild geprüft – der Gast sieht sie dort nicht als Kachel, sondern hinter dem Schleier. Beleg: Kartenpult 014/015/016/020/026 (Fenster «Neue Rubrik», «Neuer Eintrag», «Vorher und nachher» offen): `button.wo-kn--glas` und `button#l-sp` der Fussleiste unter `.fenster` (`position:fixed; inset:0; backdrop-filter:blur(7px)`) – Streuung 0.0, weil verschwommen.

`seite.js`, alle Kriterien, **K4 geschlossene details** (4.11.2026): Inhalt eines geschlossenen `<details>` (ausser der `<summary>`) gilt als unsichtbar. Beleg: Schaufenster 018/019 «Team», WebKit 1440: `details.platte.ws-eintrag > div.ws-eintrag__innen > div.ws-fotos > button.ws-foto` «Kachel wirkt leer» – die Ausschnitte (`schaufenster-018-f0.jpg`) zeigen nur Seitenhintergrund; die Einträge sind zu, die Fotoknöpfe liegen im zugeklappten Teil. Neuere Engines blenden den Inhalt über `::details-content` mit `content-visibility:hidden` aus, `getBoundingClientRect()` meldet trotzdem volle Masse (lokal Chromium 153: drei `button.ws-foto` je 93×70 px bei y = 952 in geschlossenen Einträgen, `display:block`).

`tor-schnell.js`, Kriterien 10 und 4, **K10/K4 Rollkasten** (4.11.2026): liegt ein Blatt oder eine Kachel in einem eigenen Rollkasten (`overflow: auto/scroll`, die Seite selbst rollt nicht), wird dieser Kasten gerollt, bis die Stelle ganz darin steht, und danach zurückgerollt; was auch dann vom Kasten- oder Seitenrand abgeschnitten bleibt, wird nicht ins Bild geprüft (ein halbes Blatt hat weder Loch noch Mitte). Beleg: Hausdruckerei, die Hauptfläche `.start__in.ms-haupt` rollt (828 von 3424 px sichtbar), das Dokument ist nur 900 px hoch, `scrollTo` der Seite bewegt nichts. Die Vorschau-Blätter der Galerien am unteren Fensterrand wurden halb aufgenommen: «Zurück am See» Blatt 261×363 px als 261×117 px, «Plakat und Presse» nur die oberen 173 px eines 294 px breiten Blatts – daraus 15 «Loch», 8 «Mitte» und «Kachel wirkt leer» am «Leeren Blatt» (nur der obere Rand des gestrichelten Rahmens im Ausschnitt, das Plus darunter abgeschnitten); dieselben Blätter sind beim Hineinrollen ganz gefüllt (gleiche Funde in Chromium, Rechnung `auswertung.py` unverändert).

`seite.js` + `auswertung.py`, Kriterium 10, **K10 randloses Foto** (4.11.2026): deckt ein Bild (nicht ein fertiges Vorschaubild `.vbild` eines ganzen Blatts) mindestens 90 % eines Blatts, gelten Loch und Mitte nicht; die Bildprüfung nimmt den Rand des Blatts als Papierfarbe, bei einem randlosen Foto ist das Himmel oder Dunst. Beleg: Hausdruckerei «Motive vom See», Ansichtskarte «Bis zum Säntis» (`div.blatt.pk-vorn`, `el-bild` 230×166 px über einem Blatt 221×157 px): «oben 15 %, unten 1 % frei» – die oberen 15 % sind der dunstige Himmel über dem Säntis (Grauwert 188 gegen gemessene «Papierfarbe» 168 aus Himmel und See), keine leere Fläche; die Karten «Bottighofen» und «Bodensee» derselben Reihe mit dichtem Bildrand bleiben unauffällig.

## K34 in Chromium (Oberchef 4.11.2026, Nachtbau Schlössli)
`bewegung-tor.js` misst das Scrollen für Kriterium 34 jetzt in Chromium (Grundlinie ebenfalls in Chromium); WebKit bleibt für Kriterium 37 und reduced-motion, sein Ruckler-Wert steht weiter im Fund («WebKit ohne Beschleunigung»). Beleg: WebKit unter Linux läuft in Playwright ohne beschleunigtes Zusammensetzen und malt jedes Scrollbild auf dem Hauptfaden neu; so arbeitet kein Browser eines Gastes (Safari auf Mac/iPhone setzt auf der Grafikkarte zusammen). Lauf d62a6ef: Hafenbüro in WebKit 79 Ruckler im besseren von zwei Läufen bei Grundlinie 0, dieselbe Seite in Chromium mit 2-fach gedrosselter Rechenleistung 1 Ruckler (Scratchpad `k34.js`, gleiche Scrollweise wie das Tor). Auch das fertig abgegebene Wild Side war in WebKit auf dem Runner in allen Werkzeugen rot (375 Felder). Chromium trennt die Seite vom Rechner: echte Kosten der Seite (Skripte, Stil, Layout, Malen, Dekodieren) bleiben sichtbar – Werkbank-Start 96–140, Markenbuch-Anleitung 56, Material 26 Ruckler in Chromium waren echte Funde und wurden an den Seiten repariert. `schnell.yml` richtet dafür WebKit und Chromium ein.

`seite.js`, Kriterium 10, **K10 zugedeckt** (4.11.2026): ein Blatt, das ein festes Fenster (Willkommensfenster, Dialog; mindestens 30 % der Fensterhöhe, waagrecht mindestens ein Drittel des Blatts überdeckend, nicht die Ebene des Blatts selbst) zudeckt, wird nicht ins Bild geprüft. Beleg: Hausdruckerei «Erster Besuch» und die Ansichten, die die Mail-Seite ohne gespeichertes «Willkommen» öffnet (Willkommensfenster rechts unten offen), `span.papier.papier--vorn` der Galerie darunter wurde ausgeschnitten und zeigte zur Hälfte das Fenster («Willkommen in der Hausdruckerei», Knopf «Wählen») – daraus «Komposition nicht in der Mitte: oben 28 %, unten 0 %», in WebKit und Chromium, auch in der Mail-Seite (Zustände 002, 037, 038).

`seite.js` + `tor-schnell.js`, Kriterium 10, **K10 schräg** (4.11.2026): ein Blatt, das selbst oder über einen Vorfahren gedreht liegt (Galerie-Stücke der Hausdruckerei mit `--r` ±0,8–1,8°), wird fürs Bild gerade gelegt (Drehung der fünf nächsten Vorfahren aus, Ausschnitt nach der neuen Lage, danach zurück). Beleg: Hausdruckerei «Hinweise im Haus», «Alle 89 Vorlagen», «Karten & Menüs»: Querformate «Reserviert» und «Ein Essen am See» (Blatt 300 px breit, 1,6° gedreht = 8 px Höhenversatz an den Kanten) – die schräge Unterkante des Rahmens ragte in die Bildprüfung und galt als Inhalt bei 91 %, daraus «Loch 19 % (72–91 %)»; dasselbe Blatt als fertiges Vorschaubild (`vorschau-dok/*.webp`, gerade) mit derselben Rechnung ohne Fund.

`auswertung.py`, Kriterium 10, **K10 Rahmen am Rand** (4.11.2026): eine dünne, fast durchgehende Zeile (höchstens 1,5 % der Höhe, über 60 % der Breite) ganz am oberen oder unteren Rand des Prüfausschnitts ist die Rahmenlinie des Blatts, kein Inhalt. Beleg: Hausdruckerei «Hinweise im Haus», Tischschild «Reserviert» (A7 quer, 224×156 px): der Rahmen liegt 4,5 mm = 6,1 % vom Rand und damit genau in der ersten Zeile des Ausschnitts (ab 7 %), die untere Rahmenlinie ausserhalb; gezählt als Inhalt ergab das «Loch 17 % (6–24 %)» und «oben 0 %, unten 20 %», ohne die Linie: oben 17 %, unten 20 %, grösstes Loch 8 % – die Gruppe steht in der Mitte.
