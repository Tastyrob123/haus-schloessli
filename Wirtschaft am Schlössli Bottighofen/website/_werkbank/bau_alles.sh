#!/bin/bash
# Werkbank Wirtschaft am Schlössli: das ganze Paket bauen (Nachtbau 3./4.11.2026; Vorlage bau_alles.sh des Culinarium über Walk on the Wild Side).
#   bash website/_werkbank/bau_alles.sh [--ohne-aufnahmen] [--nur-kern]
# Revier: website/_werkbank/ ist der Projektordner des Kits; die Website liegt eine Ebene höher und wird nur gelesen (assets ist ein Verweis).
# Voraussetzung: Vorschau-Server läuft:  python3 website/_werkbank/serve.py 9288, Werkzeug-Server 9281–9287 (cloud/server.sh). Kit unverändert, headless, nichts geht online.
# Teile: Papier (Werkbank Papier: Unterlagen, Drucksachen, Untersetzer, Sticker, Postkarten, Beigaben), Feed/Mails/Dateien (Werkbank Feed),
#        Kern (Startseite, Befund, KI, Karte «Ein Vorschlag.», Geprüft). Haben die Reviere ein eigenes Bauskript, ruft dieses es auf, sonst die Schritte des Culinarium.
set -e
P="$(cd "$(dirname "$0")" && pwd)"; cd "$P"
K="${WERKBANK_KIT:-$(cd "$P/../../.." && pwd)/_Werkbank-Kit}"
export PYTHONPATH="$K:$P/_werkbank" WB_PORT=9288 KIT="$K"
OHNE=""; NURKERN=""
for a in "$@"; do case "$a" in --ohne-aufnahmen) OHNE=1;; --nur-kern) NURKERN=1;; esac; done
python3 "$K/kern.py" "$P" | grep -v "Schrift fehlt" || true
python3 "$K/schriften.py" "$P" > /dev/null || true
timeout 300 python3 _werkbank/druckschrift.py > /dev/null           # Open Sans als feste Druckschnitte (nach schriften.py, das die Kit-Namen anlegt)
if [ -z "$OHNE" ]; then
  timeout 900 node _werkbank/ansicht_lang.js "$P"                    # jede Seite der Website am Rechner und am Handy
  timeout 900 node _werkbank/sb_ideen.js                             # Ideen und Gäste-Funktionen
  timeout 900 node _werkbank/sb_werkzeuge.js                         # Bildschirme der sieben Werkzeuge (Adressen aus _werkbank/werkzeuge.json)
fi
python3 _werkbank/sb_heute.py                                        # heute (Website vom 19.10.2026) und neu
if [ -z "$NURKERN" ]; then
  # ---------- Papier (Werkbank Papier, 3.11.2026: eigenes Bauskript, vor den Dateien) ----------
  timeout 1800 bash _werkbank/papier_bau.sh
  # ---------- Feed, Mails, Dateien (Werkbank Feed) ----------
  timeout 1800 bash _werkbank/feed_alles.sh feed mails               # Feed und Mails (Werkbank Feed, 3.11.2026: eigenes Bauskript mit feed_kleid.py)
  node _werkbank/geraete/schirme.js feed || true                     # Feed im Handy der Werkbank (feed_buehne.py braucht geraete/schirm-feed-sb.png)
fi
node "$K/ziele.js" "$P" || true
# ---------- Kern: Startseite, Befund, KI, Karte «Ein Vorschlag.», Geprüft ----------
timeout 900 node _werkbank/sb_strom.js || true                       # Befund, Prüfbericht, Karte, Markenbuch für die Objekte
timeout 600 python3 _werkbank/objekte_bau.py "$P"
[ -z "$NURKERN" ] && timeout 900 python3 _werkbank/material_seite.py   # Dateien (Werkbank Feed): sammelt, was die Reviere liefern, letzter Schritt vor bau.py
timeout 900 python3 "$K/bau.py" "$P" | grep -v "Schrift fehlt"        # die Werkbank (ruft haus.nach_bau: Kapitel, Befund, KI-Seite, Schweizer Schreibung, Kleid)
timeout 900 node _werkbank/sb_strom.js || true
timeout 600 python3 _werkbank/objekte_bau.py "$P"
timeout 900 python3 "$K/bau.py" "$P" | grep -v "Schrift fehlt"
python3 _werkbank/ruecksprung.py "$P" || true                         # zuletzt: Rücksprung auf die alte Höhe in jeder Seite (auch nach den Bauten der Beigaben)
# letzte Kontrolle (Oberchef 3.11.2026): kein Schritt hat die Website selbst geändert (website/*.html, website/assets/ …), nur website/_werkbank/
draussen="$(git -C "$P/../.." status --short -- website | grep -v "website/_werkbank/" || true)"
if [ -n "$draussen" ]; then echo "ACHTUNG, ausserhalb von website/_werkbank/ geändert:"; echo "$draussen"; exit 1; fi
echo "fertig: http://127.0.0.1:9288/werkbank/"
