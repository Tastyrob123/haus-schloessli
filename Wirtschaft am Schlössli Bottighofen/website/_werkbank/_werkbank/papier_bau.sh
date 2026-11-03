#!/bin/bash
# Werkbank Wirtschaft am Schlössli, Papier: Unterlagen, Drucksachen, Untersetzer, Sticker, Postkarten, Beigaben (Werkbank Papier, Nachtbau 3.11.2026).
#   bash website/_werkbank/_werkbank/papier_bau.sh            (von bau_alles.sh an der Stelle «Papier» aufzurufen)
# Voraussetzung: Vorschau-Server 9288 läuft (serve.py), feste Druckschnitte liegen in _werkbank/fonts (aus _karten/schriften). Kit unverändert, headless, nichts geht online.
set -e
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
K="${WERKBANK_KIT:-$(cd "$P/../../.." && pwd)/_Werkbank-Kit}"
export PYTHONPATH="$K:$P/_werkbank"
cp ../../_karten/schriften/*.ttf _werkbank/fonts/                          # Open Sans, Instrument Sans, DM Mono als feste Schnitte (kein Type 3)
# Drucksachen und Untersetzer
rm -rf drucksachen/img drucksachen/pdf untersetzer/img untersetzer/pdf _werkbank/roh/papier
timeout 300 python3 _werkbank/papier.py "$P"
timeout 900 node "$K/papier_druck.js" "$P" > /dev/null
timeout 300 python3 _werkbank/papier_lauf.py "$K/papier_seiten.py" "$P" | grep -v "Schrift fehlt" || true
# Sticker und Beigaben
rm -rf _werkbank/roh/sticker _werkbank/roh/einzel-sticker _werkbank/roh/beigaben sticker/img sticker/pdf beigaben/img beigaben/pdf
timeout 120 python3 _werkbank/sticker.py "$P"
timeout 120 python3 _werkbank/beigaben.py "$P"
timeout 900 node _werkbank/sticker_druck.js "$P" > /dev/null
timeout 300 python3 _werkbank/sticker.py "$P" --seite
timeout 300 python3 _werkbank/beigaben.py "$P" --seite
# Postkarten
rm -rf _werkbank/roh/postkarten _werkbank/roh/einzel-postkarten postkarten/pdf
timeout 120 python3 _werkbank/postkarten.py "$P"
timeout 900 node _werkbank/postkarten_druck.js "$P" > /dev/null
timeout 300 python3 _werkbank/postkarten.py "$P" --seite
# Unterlagen (zuletzt: das Angebot zählt Drucksachen, Sticker, Postkarten und Beigaben)
timeout 300 python3 _werkbank/unterlagen_bau.py "$P"
timeout 300 node _werkbank/unterlagen_druck.js "$P" > /dev/null
rm -f _werkbank/roh/unterlagen/n-wirtschaft-am-schloessli-angebot.json _werkbank/roh/unterlagen/n-wirtschaft-am-schloessli-brief.json
timeout 600 python3 _werkbank/unterlagen_bau.py "$P" --seite
python3 _werkbank/papier_nach.py
echo "Papier fertig: http://127.0.0.1:9288/unterlagen/ · /drucksachen/ · /untersetzer/ · /sticker/ · /postkarten/ · /beigaben/"
