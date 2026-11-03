#!/bin/zsh
# Das Hausbuch · Schlössli: alle Läufe nacheinander (nie zwei Browser zugleich) gegen den Prüfserver der Probe-Kopie (Markenprüfung mit Probe-Antwort).
#   BASIS=http://localhost:9049/ zsh _werkzeuge/livre/pruefung/matrix.sh        (aus dem Ordner der Probe-Kopie)
cd "$(dirname $0)/.."
E=pruefung/ergebnisse; mkdir -p $E
for m in chromium webkit firefox; do
  for g in 1440x900 1366x650 390x844 320x700; do
    [ -n "$NUR" ] && [[ "$NUR" != *"$m-$g"* ]] && continue
    BASIS=${BASIS:-http://localhost:9049/} node pruefung/bedienen.js $m $g > $E/lauf-$m-$g.txt 2>&1
    echo "funktionen $m $g: $(grep -o 'Summe:.*' $E/lauf-$m-$g.txt || echo ABBRUCH)"
  done
  [ -n "$OHNE_ZUSATZ" ] && continue
  BASIS=${BASIS:-http://localhost:9049/} FEHLERLOG="$PWD/_qa/fehler.jsonl" node pruefung/zusatz.js $m > $E/zusatz-$m.txt 2>&1
  echo "zusatz $m: $(grep -o 'Summe.*' $E/zusatz-$m.txt || echo ABBRUCH)"
done
