# Übergabe (Limit) · Schlössli Nachtbau · Stand 4.11.2026, 04:30 UTC

Neuer Chat: zuerst diese Datei lesen, dann `CLAUDE.md`, dann beim «Nächsten genauen Schritt» weitermachen.

## Auftrag
`AUFTRAG-NACHT.md`: Werkbank, sieben Werkzeuge, Drucksachen, Feed, Prüfung für die Wirtschaft am Schlössli Bottighofen, Stamm Culinarium (`git clone --depth 1 https://github.com/Tastyrob123/haus-culinarium-hannover /tmp/culinarium`), Vorbild Wild Side (`/tmp/wildside`). Frist war 01:00 UTC. Am Ende **eine** Meldung an Robert: «Fertig. <Link Werkbank> <Link Prüftafel>» oder «Nicht fertig. <Links> – es fehlt: <Liste>». Deutsch, kurz, keine Begründungen.

## Was fertig ist
Alle zehn Reviere sind gebaut, committet und gepusht (Zweig `claude/schloessli-nachtbau-auftrag-es1vpf`). Lokal in Chromium haben alle 0 Funde.
- **Hafenbüro** (`_werkzeuge/maison`, 9281), **Kartenpult** (`carte`, 9283), **Markenbuch** (`livre`, 9285, Hausregeln, Anleitung), **Besucherliste** (`registre`, 9286): in WebKit 0 Messfunde.
- **Schaufenster** (`bureau`, 9282), **Reservationsbuch** (`reception`, 9284): in WebKit nur noch wenige «leere Kachel»-Funde.
- **Hausdruckerei** (`imprimerie`, 9287): 89 Vorlagen, 34 fertige Drucksachen (`haeuser/schloessli/drucksachen/LISTE.md`), Stilblatt.
- **Werkbank** (`website/_werkbank/`, 9288): alle 14 Seiten mit Schlössli-Inhalt (Start, Karte, KI, Geprüft, Befund, Unterlagen, Drucksachen, Untersetzer, Sticker, Postkarten, Beigaben, Feed mit 48 Beiträgen, 10 Mails, Material).
- Kleid `_werkzeuge/oberflaeche/kleid/schloessli.{js,css}`, Ziellisten `_Werkzeuge/abnahme-tor/ziele-schloessli.json` und `_Werkzeuge/messlauf/ziele-schloessli.json`, `cloud/haus.json` mit Servern 9281–9288.
- Prüfregeln geschärft (mit Beleg in `_Werkzeuge/abnahme-tor/README.md`): Kriterium 34 misst eine Grundlinie des Rechners; «Text zerfällt» lässt Karten mit gesetztem Blatt aus. `schnell.yml`: jeder Lauf eigene Gruppe, Teilprüfungen unter `ergebnis/laeufe/<zweig>-teil-<laufnummer>/`.

## Prüfstand
Letzter Lauf über alles: Commit 4381dcf, Tafel im Zweig `ergebnis`: `ergebnis/laeufe/claude-schloessli-nachtbau-auftrag-es1vpf-schnell/tor/index.html`. 442 Zustände, nichts «nicht erreicht» ausser 1 in der Hausdruckerei.
Offene Funde (fast alle Kriterium 35, Schrift in Knöpfen in WebKit 0,6–1,3 px versetzt):
1. **Werkbank, alle Seiten:** Knöpfe (Kasten 56 px) 0,7 px zu tief; Reiter-Pillen 1,0 px zu tief und 0,8 px zu weit rechts; Ziffern 0,6 px. Ursache: Ausgleiche in `_werkbank/text_mitte.py` / `knopf_mitte.css` gelten nur für Chromium. Dazu Geprüft 6× leere Kachel.
2. **Hausdruckerei:** «Website ansehen» 1,3 px tief, Filter-Pillen 0,6 px rechts, Einzelwort «Gourmetkreuzfahrt», eine Kante, ein Loch 15 %, Mail-Seite leere Kacheln und Kriterium 37 (Bewegung) in allen Zuständen.
3. **Reservationsbuch:** Listenbilder im Eingang in WebKit leer (wohl eigener Scrollbereich oder Einblende-Klasse `sw-da`).
4. **Schaufenster:** 5 leere Kacheln (Team ohne Foto, Weinkarte). **Markenbuch-Anleitung:** 1 leere Kachel.
5. **Kriterium 34 (Scrollen flüssig):** auf dem Runner überall rot, auch mit Grundlinie. Die Grundlinie misst seit 21:37 zwölf animierte Fotos; ob das reicht, zeigt erst der nächste Lauf. Lokal in Chromium ist alles flüssig.

Um 01:40 UTC liefen drei Opus-Agenten auf die Punkte 1, 2 und 3+4. Ihr Stand ist nur, was committet ist (`git log`).

## Stand 04:30 UTC
- Prüfung über alles auf fb2eb3a: **12.488 → 50 Funde** (Tafel `ergebnis/laeufe/claude-schloessli-nachtbau-auftrag-es1vpf-schnell/`). Werkbank ohne Kriterium 35.
- Danach behoben (noch ungeprüft): Kriterium 37 «bleibt unsichtbar» als Regel-Lücke geschärft (waagrecht ausserhalb, geparkte Reihenglieder; Beleg README), Mail-Seiten `overflow-x:clip`, Prüftor holt Vorschau-Blätter ins Fenster vor dem Bild (WebKit lud lazy-Bilder nicht; Beleg README).
- Offen: **Kriterium 34 (Scrollen flüssig) überall rot** auf dem Runner (Grundlinie 1 Ruckler, Werkzeuge 19–56). Messprobe läuft (Commit b2a249e, `probe.on` mit tresen, plakatarchiv-buch): misst das Scrollen mit je einem abgeschalteten Effekt; Ergebnis steht im K34-Fund der Tafel. `probe.on` danach löschen.
- Agent für leere Kacheln Schaufenster/Reservationsbuch läuft noch (Reservationsbuch schon grün).

## Stand 03:10 UTC (zweiter Chat)
- Ursache der Knopfschrift-Funde (Kriterium 35, über 11.000): der Runner-WebKit unter Linux kennt `font:-apple-system-body` nicht, also galt der Chromium-Ausgleich `@supports not (font:-apple-system-body)` dort mit. Ersetzt in der ganzen Werkbank durch die Chromium-Weiche `@supports (interpolate-size:allow-keywords) and (app-region:drag)` (Commit 1ca728c, Prüfung `[schnell: werkbank]` läuft). Lokal in Chromium unverändert (0,7 px).
- Einrichtung in dieser Sitzung: `~/Desktop/Website-Projekte` -> Repo verlinken (sonst startet Schaufenster 9282 nicht), Playwright 1.62.1 unter `/Users/robertreff/Aussen-Pruefung`, Links chromium-1234 -> 1243, dann `bash cloud/server.sh`.
- Drei Opus-Agenten arbeiten (nicht committet, bis der Oberchef committet): Hausdruckerei-Funde; leere Kacheln Reservationsbuch/Schaufenster/Anleitung; Werkbank Einzelwörter und Geprüft-Kacheln.

## Nächster genauer Schritt
1. `git fetch origin && git log --oneline origin/claude/schloessli-nachtbau-auftrag-es1vpf -15` lesen: was von den drei Agenten committet ist.
2. Einrichten: `cd /Users/robertreff/Aussen-Pruefung` nötig? Nein – in der Cloud: `bash cloud/vorbereiten.sh chromium` scheitert am Download; stattdessen Playwright 1.62.1 unter `/Users/robertreff/Aussen-Pruefung` (`npm i playwright@1.62.1`) und `ln -sfn /opt/pw-browsers/chromium-1243 /opt/pw-browsers/chromium-1234` und dasselbe für `chromium_headless_shell`. Dann `bash cloud/server.sh` (Server 9281–9288). Kundenmaterial: siehe CLAUDE.md (`quelle`).
3. Die offenen Funde 1–4 reparieren (Lösungsmuster: Beschriftung in `<span>` mit `text-box: trim-both cap alphabetic`, Grundfall symmetrisch, jeder Ausgleich nur in `@supports (interpolate-size:allow-keywords)`; Bilder `loading="eager" decoding="sync"`).
4. Commit mit `[schnell]` in der Nachricht, pushen **Commit für Commit** (`git push origin <sha>:refs/heads/claude/schloessli-nachtbau-auftrag-es1vpf`, der Proxy kappt grosse Pakete), Ergebnis im Zweig `ergebnis` abwarten (rund 45 min).
5. Bei null offenen Funden: `main` vorspulen (`git push origin claude/schloessli-nachtbau-auftrag-es1vpf:main`), Meldung an Robert.

## Links
- Werkbank (Quelle): https://github.com/Tastyrob123/haus-schloessli/tree/claude/schloessli-nachtbau-auftrag-es1vpf/Wirtschaft%20am%20Schl%C3%B6ssli%20Bottighofen/website/_werkbank
- Prüftafel: https://github.com/Tastyrob123/haus-schloessli/blob/ergebnis/ergebnis/laeufe/claude-schloessli-nachtbau-auftrag-es1vpf-schnell/tor/index.html
- Lokal nach `bash cloud/server.sh`: http://127.0.0.1:9288/werkbank/index.html

## Stolpersteine
- Container-Neustarts löschen Prozesse, nicht Dateien: Server neu starten, uncommittete Agentenarbeit sichten.
- Agenten: keine Heredocs / `python3 -` in der Shell (wartet auf Freigabe); Skripte als Datei.
- Untracked Dateien in `website/_werkbank/_werkbank/` (roh, sb, Cache) sind Bau-Rohstoff, absichtlich nicht eingecheckt.
- `reception/online/schluessel.txt` (Culinarium-Token, auch im öffentlichen Culinarium-Repo) stand im Commit 2eee208; gelöscht, in der Geschichte noch drin – Robert entscheidet.
- Agenten-Commits tragen teils «Co-Authored-By: Claude Opus 5.5»; gepusht, nicht umgeschrieben.
- Kein WebKit lokal (Download gesperrt); WebKit-Prüfung nur in Actions.
