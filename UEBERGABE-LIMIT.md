# Übergabe (laufend) · Schlössli Nachtbau 3./4.11.2026

Ein Chat in einem anderen Profil liest zuerst diese Datei, dann `CLAUDE.md`, und setzt beim «nächsten genauen Schritt» an.

## Auftrag
`AUFTRAG-NACHT.md`: Werkbank, sieben Werkzeuge, Drucksachen, Feed, Prüfung für die Wirtschaft am Schlössli Bottighofen aus dem Stamm des Culinarium (`/tmp/culinarium`, Vorbild Wild Side `/tmp/wildside`). **Fertig 01:00 UTC am 4.11.2026** (09:00 Ortszeit Robert). Letzte Nachricht an Robert genau eine: «Fertig. <Link Werkbank> <Link Prüftafel>» oder «Nicht fertig. <Links> – es fehlt: <Liste>».

## Zweige
- Arbeit: `claude/schloessli-nachtbau-auftrag-es1vpf` (alle Commits, Pushes mit `[schnell: …]` stossen die Cloud-Prüfung an).
- `main`: Meilensteine (Fast-Forward von der Arbeit, Commit-Nachricht ohne `[schnell`).
- `ergebnis`: Prüftafeln `ergebnis/laeufe/<zweig>-schnell/tor/index.html` bzw. `<zweig>-teil/`.
- `quelle`: Kundenmaterial; in der Sitzung: `git worktree add -f /tmp/quelle origin/quelle && ln -sfn "/tmp/quelle/Wirtschaft am Schlössli Bottighofen/_quelle" "Wirtschaft am Schlössli Bottighofen/_quelle"`.

## Was fertig ist
- 17:20 UTC: Vorbilder geholt, Chromium läuft (Playwright 1.62.1 unter `/Users/robertreff/Aussen-Pruefung`, Browser verlinkt `/opt/pw-browsers/chromium-1234 → chromium-1243`; `cloud/vorbereiten.sh` kann hier nicht laden, Netz gesperrt).
- 17:35 UTC: Culinarium-Werkzeuge nach `Wirtschaft am Schlössli Bottighofen/_werkzeuge/` kopiert (ohne Prüfordner), Werkbank nach `website/_werkbank/`; alter Stand daneben in `*.vor-nachtbau-2026-11-03/` (nicht eingecheckt, nur lesen). Kleid `oberflaeche/kleid/schloessli.{js,css}` + `schloessli-zeichen.svg` + `schloessli-marke.svg`; Ports 908x→928x; Ziellisten `_Werkzeuge/abnahme-tor/ziele-schloessli.json`, `_Werkzeuge/messlauf/ziele-schloessli.json`; `cloud/haus.json` mit acht Servern (9281–9288); alle acht Server laufen (`bash cloud/server.sh`).
- 17:45 UTC: `_werkzeuge/AUFTRAG-GEMEINSAM.md` (Reviere, Kleid, Hauswerte, Regeln, Prüfung).

## Was offen ist (Reihenfolge)
1. Zehn Opus-Agenten parallel: maison, bureau, carte, reception, livre, registre, imprimerie, werkbank-kern, werkbank-papier, werkbank-feed (Reviere laut `AUFTRAG-GEMEINSAM.md`).
2. Je Werkzeug nach «fertig»: Commit, Push mit `[schnell: <k>]`, Funde aus `origin/ergebnis` zurück an den Agenten, Nachprüfung.
3. Werkbank-Ausgaben (werkbank/, befund/, unterlagen/, … in `website/_werkbank/`) erst committen, wenn sie Schlössli-Inhalt zeigen (jetzt noch Culinarium-Inhalt, absichtlich nicht eingecheckt).
4. Am Ende `[schnell]` über alles, Fundbilder und 15 Zustandsbilder je Werkzeug ansehen, `main` nachziehen, Meldung an Robert.

## Nächster genauer Schritt
Agenten starten (Agent-Werkzeug, `model: "opus"`), je Agent: «Lies `Wirtschaft am Schlössli Bottighofen/_werkzeuge/AUFTRAG-GEMEINSAM.md`, dein Revier ist …».

## Prüfstand
- 17:46–17:54 UTC Probelauf `schnell.yml` (workflow_dispatch, nur=tresen, Zweig `claude/…`): Ablauf läuft durch, Server 9281–9287 starten auf dem Runner; 9288 (Werkbank) antwortet 404, weil `website/_werkbank/werkbank/index.html` noch nicht eingecheckt ist (gewollt, bis Schlössli-Inhalt da ist). Tor darum noch 0 Zustände. Tafel: `ergebnis/laeufe/claude-schloessli-nachtbau-auftrag-es1vpf-teil/`.
- Agenten gestartet 17:46 UTC (10, Opus): maison+oberflaeche, bureau, carte, reception, livre, registre, imprimerie, werkbank-kern, werkbank-papier, werkbank-feed.

## Stolpersteine
- `rsync` fehlt im Container (Kopie mit `python3 -I <scratchpad>/kopieren.py`).
- Playwright-Download ist gesperrt; der vorinstallierte Chromium 1243 ist als 1234 verlinkt (`/opt/pw-browsers`).
- Agenten: keine Heredocs / `python3 -` in der Shell (Freigabe-Abfrage), Skripte als Datei anlegen.
- `website/assets/schrift/` und `/assets/bild/` gibt es hier nicht: Schriften unter `/assets/fonts/`, Fotos unter `/assets/img/<schlüssel>-<breite>.webp`.
- `imprimerie/haeuser/culinarium/` ist per `.gitignore` ausgeschlossen (nur Vorlage auf dem Rechner).
