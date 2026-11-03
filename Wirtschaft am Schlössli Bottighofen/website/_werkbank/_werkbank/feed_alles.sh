#!/bin/bash
# Revier Feed, Mails, Material der Werkbank Schlössli bauen (Nachtbau 3./4.11.2026, Agent schloessli-werkbank-feed).
#   bash website/_werkbank/_werkbank/feed_alles.sh [feed|mails|material …]   (ohne Angabe: alles; Server 9288 muss laufen)
# Die Kit-Schritte laufen über feed_bau.py mit den Hauswerten aus feed_haus.py (unabhängig vom grossen haus.py der Werkbank).
set -e
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
K="${KIT:-$(cd "$P/../../.." && pwd)/_Werkbank-Kit}"
export PYTHONPATH="$K:$P/_werkbank" WB_PORT=9288 KIT="$K"
teile="${*:-feed mails material}"
for t in $teile; do
  case "$t" in
    feed)
      python3 _werkbank/feed_bau.py feed.py "$P"
      node "$K/feed_druck.js" "$P"
      python3 _werkbank/feed_bau.py feed.py "$P"
      python3 _werkbank/feed_leicht.py "$P"
      python3 _werkbank/feed_kleid.py
      node "$K/feed_druck.js" "$P" --handy ;;
    mails)
      python3 mails/_src/bau.py
      node mails/_src/aufnahme.js ;;
    material)
      python3 _werkbank/material_seite.py ;;
  esac
done
echo "fertig: http://127.0.0.1:9288/feed/ · /mails/ · /material/"
