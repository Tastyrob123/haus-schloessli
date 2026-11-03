#!/bin/bash
# Alle Läufe der Abnahme des Gastgebers (La Réception) · Landgasthof Ruedihus nacheinander (nie zwei Browser zugleich), je Lauf frische Wegwerf-Daten, ohne KI.
# Läuft NUR in der Probe-Kopie (Ordner mit PROBE-LIESMICH.txt): der Gastgeber auf :9023 oder PORT=<port> (liefert auch die Website der Kopie mit dem Anfrage-Fenster aus).
#   bash alle.sh [motoren] [groessen]     z. B. bash alle.sh "chromium webkit" "1440x900 390x844"
cd "$(dirname "$0")"; W="$(cd ../../.. && pwd)"; [ -f "$W/PROBE-LIESMICH.txt" ] || { echo "Nur in der Probe-Kopie laufen lassen."; exit 1; }
T="${TMPDIR:-/tmp}/reception-rh-abnahme-${PORT:-9023}"; mkdir -p "$T"
MOT="${1:-chromium webkit}"; GR="${2:-1440x900 390x844}"; PORT=${PORT:-9023}
if lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null; then echo "Port $PORT belegt, nichts beendet (F67)."; exit 1; fi
for m in $MOT; do for g in $GR; do
  b=${g%x*}; h=${g#*x}; rm -rf "$T/daten"; mkdir -p "$T/daten"
  (cd "$W" && exec env -u ANTHROPIC_API_KEY RECEPTION_DATEN="$T/daten" RECEPTION_FORMULAR_GRENZE=60 python3 _werkzeuge/reception/server.py $PORT > "$T/server.log" 2>&1) & SP=$!
  sleep 2; curl -s -o /dev/null "http://localhost:$PORT/_werkzeuge/reception/api/zustand" || { echo "Server startet nicht: $(tail -1 "$T/server.log")"; kill $SP; exit 1; }
  HOEHE=$h node gegenprobe.js ruedihus http://localhost:$PORT/_werkzeuge/reception/ $m $b 1 > "$T/gegenprobe-$m-$g.txt" 2>&1
  node abnahme.js http://localhost:$PORT/_werkzeuge/reception/ $m $b $h > "$T/abnahme-$m-$g.txt" 2>&1
  node formular_web.js http://localhost:$PORT $m $b $h > "$T/formular-$m-$g.txt" 2>&1
  kill $SP; wait $SP 2>/dev/null
  echo "$m $g: $(grep -h "grün," "$T/gegenprobe-$m-$g.txt" "$T/abnahme-$m-$g.txt" "$T/formular-$m-$g.txt" | tr '\n' ' ')"
done; done
