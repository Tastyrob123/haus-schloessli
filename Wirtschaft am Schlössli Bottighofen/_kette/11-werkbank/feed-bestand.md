---
tags: [projekt, feed]
status: aktiv
---

# Feed-Bestand und Gegenprobe (Feed-Planer, 19.10.2026)

Rolle: `~/Desktop/Website-Projekte/_Kette/rollen/feed-planer.md` · Master Website-Bau 5a Regel 10 und 10a. Bestand der früheren Feeds: `Berghotel Gasterntal/_kette/11-werkbank/feed-bestand.md` (Tabelle «Bestand», Stand 17.10.2026) und die vier Abschnitte «Dieses Haus» der Maeder-Häuser.

## Dieses Haus: Wirtschaft am Schlössli · «Ein Horizont» (dritte Fassung, 19.10.2026 ~23:30)

- **Idee:** einzelne Fotos des Hauses, und genau in der Mitte des Profils (Reihe 4 von 7) ein einziges breites Bild über drei Beiträge, ohne Schrift: die blauen Stühle am Mittag vor See und Alpen, das Bild, aus dem die Farben des Markenbuchs stammen. Darüber Abend und Küche, darunter Mittag und Ufer.
- **Raster:** 21 Beiträge, 7 Reihen; 18 Einzelfotos + ein Bild über drei. Keine Schrift in den Bildern, keine Stücke über mehrere Reihen, keine Menschen im breiten Bild.
- **Erste neun:** Dessert · Abend unter der Platane · Glas vor dem See · Jonas Volpert (ganz) · Platzteller von oben · Gaststube · gefülltes Fleisch · Digestifs · grüne Suppe.
- **Farbbett:** Die hellen Teller-Bilder (weisser Grund, blauer Stuhl) liegen nur in den Ecken jedes Dreier-Blocks (dazu einmal in der Mitte unten, diagonal), nie neben- oder übereinander; dazwischen dunkle, grüne und blaue Bilder.
- **Warum dieses Haus so:** Ein Restaurant am Wasser, dessen ganze Marke aus einem Bild kommt (Stuhlblau, Seespiegel, Seehimmel aus `8cc68d`). Dieses Bild ist die Mitte, alles andere sind ruhige einzelne Fotos, wie das Haus selbst: wenig Aufwand im Raster, viel im Bild.
- **Bilder:** 19 Fotos, alle von der Website des Hauses, zwei aus dem Eintrag bei Schweiz Tourismus (Lounge, Sauce). Jedes einmal.
- **Draussen gelassen:** Porträt der Küchenchefin (Sponsor-Logo), Apéro mit Bierglas (Brauerei), Wegweiser (angeschnittene Person dahinter), Weinregal (lesbare Etiketten), Thunfisch mit Weinglas (Fast-Dublette), Team quer, Bar (900 px), alles Fremde (Schäfli, Commons, Tripadvisor, Excellence, KI-Heftbilder, Instagram-Standbilder).
- **Profil:** 46 Beiträge, 2’601 Follower, 584 gefolgt (19.10.2026).
- **Bau:** `website/_werkbank/feed_daten.py` (REGEL «bogen»), `python3 _Werkbank-Kit/feed.py "<…>/website"`, danach `python3 website/_werkbank/feed_leicht.py`. Lokal http://127.0.0.1:8982/feed/. Vorige Fassungen: `website/_sicherung/2026-10-19-2320-feed-vor-weinregal/`, `…-2330-feed-vor-ohne-hochbilder/`.

## Verlauf

- **Fassung 1 «Sitzen bleiben»** (19.10. ~22:55): drei Hochkant 1 × 3 schräg durchs Profil mit senkrechtem Satz am Rand.
- **Robert 23:18** (Bildschirmfoto Feed-Seite, mittleres hohes Bild mit Jonas Volpert, rechts angeschnitten): «Dieses Bild da mit dem abgeschnittenen Typen gefällt mir nicht.» → Fassung 2: Weinregal im mittleren hohen Bild.
- **Robert ~23:25:** «Nee, ich finde das nicht schön mit diesen beiden Bildern übereinander und den Texten da drin.» → Fassung 3 «Ein Horizont»: keine Bilder über mehrere Reihen, keine Schrift im Bild.
- **Robert ~23:40** (Bildschirmfoto: Torte über Salat, Pasta über Fisch, alle auf weissem Grund mit blauem Stuhl): «Ja, da gefällt mir das nicht, dass die Bilder so gleich übereinander sind von dem Farbbett her.» → helle Teller-Bilder nur noch in den Ecken der Dreier-Blöcke. Vorher: `website/_sicherung/2026-10-19-2340-feed-vor-farbbett/`.

## Draussen angesehen (19.10.2026, kostenlos)

- Zusätzlich zum Stand vom 17.10.: Werkzeuge zum Teilen von Bildern bieten Panoramen von 3 × 1 bis 3 × 6 an, alle quer über die Reihe; ein hohes Bild über drei Reihen in nur einer Spalte kommt dort nicht vor. Profil-Raster zeigt 3:4 (Quellen uneinig, seit 2025 oder Januar 2026), deckt sich mit der Rechnung des Kits (1012,5 von 1080). Gelesen wird oben: die erste Reihe muss allein tragen, deshalb steht der Abend oben rechts. Quellen: postplanify.com/blog/instagram-grid-layout-guide · mergeimages.net/blog/restaurant-instagram-grid-food-photo-aesthetic (Anbieterseiten, Zahlen dort ungeprüft).

## Gegenprobe (dritte Fassung)

| Feed | Leitform | Schrift | Erste Reihe | Unterschied zum Schlössli |
|---|---|---|---|---|
| Carlton-Europe | Paar 1 + 2, Hochkant 1 × 2 | Sätze auf Fotos | Abzug + Häuser heute | keine Paare, kein Hochkant, keine Schrift |
| Waldhotel Doldenhorn | Titelseite 2 × 2, Zahl darunter | Titel und Zahlen | Titelseite «Das Haus» | keine Blöcke, keine Zahlen |
| Landgasthof Ruedihus | Bild über sechs 3 × 2 oben, Raumnamen | Namen auf Fotos | Haus im Grünen (6) | kein Bild über zwei Reihen, keine Namen |
| Berghotel Gasterntal | drei Wortplakate 3 × 1 | Satz gross im Plakat | Plakat Fest | ein einziges breites Bild, ohne Schrift, in der Mitte statt oben |
| Grand Beau-Rivage | Plakat jede vierte Reihe, ohne Schrift, oben beginnend | Tafeln | Plakat Haus | nur eines, genau in der Mitte, keine Tafeln |
| Tasty Hub | Banner oben | – | Banner | Breitbild nicht oben, sondern Mitte |
| Taverne zum Schäfli | noch kein Feed | | | für den Schäfli-Feed gesperrt: ein einziges Breitbild genau in der Mitte |

Ergebnis: Kein bisheriger Feed hat ein einzelnes Breitbild in der Mitte und sonst nur Einzelfotos ohne Schrift.

## Nachgeprüft 19.10.2026 nachts: was aus den anderen Häusern übernommen ist (Auftrag Oberchef)

Gelesen: Feed-Regeln (Memory feedback-feed-qualitaetsregeln, feedback-feed-bildauswahl-ablehnungen), Tasty-Sprache Teil C «Feeds», Belege #1939 und #2513/2514/2519, Werdegang «Werkbank in Kapiteln» (Ruedihus) und Gasterntal Phase 1, Nachträge 17.10. in den Feed-Beständen der Maeder-Häuser. Jede Korrektur am Stand geprüft:

| Korrektur aus den anderen Häusern | Am Schlössli |
|---|---|
| Nur echte Motive, keine Tickets, Anhänger, Postkarten, Zettel, Abzüge, keine «schlecht animierten Bilder mit Text» (17.10. ~23:45) | 27 von 27 Beiträgen sind Fotos des Hauses, keine Tafel |
| Schriftzüge in den grossen Bildern, weiss mit Hero-Schatten; oben rechts, wo unten links unlesbar ist (Doldenhorn) | Schrift in allen drei hohen Bildern, Schatten von `.ha2__t`; an jedem Bild einzeln angesehen, Schrift liegt auf Laub, Abendhimmel oder dunklen Flaschen, nicht über Gesichtern, Körpern oder Etiketten |
| Keine blauen Farbbilder / nachtblauen Flächen (Carlton, Doldenhorn) | keine Farbfläche im Feed; Blau nur, wo es im Foto ist (Stühle, Platzteller) |
| Grosse Bilder nur einmal je Haus anders; Banner insgesamt drei (Ruedihus, Gasterntal) | eine Form (Hochkant 1 × 3), drei Stück, in keinem anderen Feed |
| Keine Dreierreihe zum Schluss (#1939) | unterste Reihe: hohes Bild + zwei Fotos |
| Fremdmarken wegschneiden (02.10.) | Apéro mit Bierglas raus, Porträt der Küchenchefin mit Sponsor-Logo raus, Weinregal mit Etiketten raus |
| Kein Motiv doppelt, auch keine Fast-Dubletten, Familien ≥ 4 Beiträge auseinander (02.10.) | Thunfisch mit Weinglas ersetzt (sah aus wie der Thunfisch in Scheiben); Dessert/Torte 6 Beiträge auseinander |
| Bildschärfe: nichts über 1,6-fach hochgerechnet (17.10.) | grösster Faktor 1,21 (hohe Bilder), Tortelloni 1,2 |
| Echte Profilzahlen, wenn es ein Profil gibt (Doldenhorn) | 46 · 2’601 · 584, Stand 19.10.2026 |
| Prüfung Chromium und WebKit, 1440 und 390 (Gasterntal) | 32 Vorschaubilder geladen, kein Überlauf, keine Fehler, Beitrag öffnet mit Bild 1080 px und Text, in beiden Kernen und beiden Breiten |

Die Bühne des Feeds in der Werkbank (Handy mit Polaroids, Hinweis darunter) gehört dem Werkbank-Chat.

## Roberts Rückmeldung 19.10.2026 23:18

Bild: Feed-Seite in Safari, hohes Bild in der Mitte mit Jonas Volpert, rechts angeschnitten. Robert: «Dieses Bild da mit dem abgeschnittenen Typen gefällt mir nicht.»
- Umgesetzt: Das mittlere hohe Bild ist jetzt das Weinregal (`8e85ca`, Ausschnitt links, Etiketten unscharf), Satz «Jonas Volpert, Sommelier.» höher gesetzt über den dunklen Flaschen. Jonas Volpert steht ganz im einzelnen Beitrag 18, die Sauce ist dafür raus. Regel daraus: Menschen nie im hohen oder breiten Bild, wo sie angeschnitten werden, nur ganz im einzelnen Beitrag. Vorher: `website/_sicherung/2026-10-19-2320-feed-vor-weinregal/`.
- Geprüft: Chromium und WebKit, 1440 und 390, alle Vorschaubilder geladen, kein Überlauf, keine Fehler, Beitrag öffnet mit Bild und Text.

## Abgleich 19.10.2026 ~23:50 (Chef-Chat: Regel-Notiz Abschnitt 11, Fehlerbuch 10a)

Fehlerbuch-Zeilen am Feed geprüft: Schatten/Kasten hinter freigestellten Bildern (keine Freisteller im Feed) · Glanz nur einmal (keine Bewegung im Feed) · roher Code (`{`, `undefined`, `NaN`, `None` auf feed/index.html und in feed.json: keiner) · Fakten nur aus diesem Haus (Namen, Zeiten, Zitat aus der Schlössli-Seite, nichts vom Schäfli) · Gesichter nie angeschnitten (Jonas Volpert, Lukas Siebel und das Abendbild ganz) · Schrift auf Bildern lesbar (keine Schrift mehr im Feed). Drei neue Zeilen eingetragen (angeschnittener Mensch, hohe Stücke mit Schrift, gleiches Farbbett).
Ausserdem geprüft: Tasty-Sprache Teil C «Restaurant-Website» (oben links ein Teller, nicht das Gebäude) und Werdegang Schlössli (Bilder scharf: grösster Faktor 1,24 beim breiten Bild).

## Abgleich mit dem Instagram-Profil (19.10.2026, nachts)

Auftrag Robert über den Chef-Chat: Bilder, die auf @schloessli_bottighofen schon gepostet sind, im Feed-Vorschlag ersetzen. Claude in Chrome war nicht verbunden; angesehen im eingebauten Browser ohne Anmeldung (nichts eingegeben, nichts angeklickt).
- **Angesehen: 12 von 46 Beiträgen** (mehr lädt Instagram ohne Anmeldung nicht, danach Anmeldesperre): Reels Ddt4mM3oBnu, Dcp83R_oajm, DcYmDKJos2U, DcOn011o50o, DcGBoENoTuO, DcA8_sGM-7k (Gemeinschaftsbeitrag @christiankuchler85), Db8FPgtoIYx, DbxwnZlo42p; Bildbeiträge Da7srxfiFJU (18.07., «PastaLiebe»), DaLOIDjiFXn (29.06., «Einfach wohlfühlen»), DaCnJVLCLfG (26.06., Theresa Hermann), DZ7azbJCNXZ (23.06., Kräutergarten). Je das Titelbild (`_quelle/extern/ig/ig-01…12.jpg`).
- **Abgleich:** jedes der 19 Feed-Fotos mit eigenen Augen und mit Bild-Abgleich (Differenz-Hash, ganzes Bild und neun Ausschnitte) gegen die 12 Titelbilder. Kleinste Abweichung 66 von 256 (gleiche Fotos lägen unter 20): kein Treffer.
- **Ersetzt: 0 Bilder.**
- **Nicht prüfbar ohne Anmeldung:** die übrigen 34 Beiträge und die weiteren Bilder in den vier Bildbeiträgen (falls es Karussells sind; ohne Anmeldung zeigt Instagram nur das erste Bild). Sobald Robert sich im eingebauten Browser oder in Chrome anmeldet, wird der Rest abgeglichen.

## Abgenommen 19.10.2026

Robert: «passt». Gültig ist die dritte Fassung «Ein Horizont» mit Farbbett-Ordnung (21 Beiträge). Instagram-Abgleich auf Roberts Wort beendet («egal vergiss es»), 12 von 46 geprüft.
