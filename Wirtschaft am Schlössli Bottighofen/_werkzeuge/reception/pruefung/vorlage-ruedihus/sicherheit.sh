#!/bin/bash
# Sicherheit des Gastgebers (La Réception) · Landgasthof Ruedihus (Master Werkzeug-Bau 5.2 und Abschnitt 8), nur in der Probe-Kopie, Wegwerf-Daten, ohne KI:
#   S1 fremder Host 421 · S2 fremde Herkunft 403 (Schreiben) · S3 Lesen von fremder Seite 403 (Sec-Fetch-Site) · S4 zu gross 413 · S5 kein JSON 415
#   S6 zu viele Änderungen 429 · F1–F6 Formular der Website: ohne Herkunft 403, mehr als 6 je Minute 429, über 12 kB 413, Maschine (Feld website) ohne Eintrag,
#   Kontakt ungültig 422, Antwort ohne Daten des Hauses · K1 ohne RECEPTION_KI=1 kein Schlüssel und Probe-Antwort
#   bash sicherheit.sh
cd "$(dirname "$0")"; W="$(cd ../../.. && pwd)"; [ -f "$W/PROBE-LIESMICH.txt" ] || { echo "Nur in der Probe-Kopie laufen lassen."; exit 1; }
T="${TMPDIR:-/tmp}/reception-rh-sicher-${PORT:-9023}"; rm -rf "$T"; mkdir -p "$T/daten"; PORT=${PORT:-9023}; B="http://localhost:$PORT/_werkzeuge/reception/api"; O="Origin: http://localhost:$PORT"
if lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null; then echo "Port $PORT belegt, nichts beendet (F67)."; exit 1; fi
gruen=0; rot=0; pr() { if [ "$2" = "$3" ]; then gruen=$((gruen+1)); echo "ok   $1 ($2)"; else rot=$((rot+1)); echo "ROT  $1: $2 statt $3"; fi; }
(cd "$W" && exec env -u ANTHROPIC_API_KEY RECEPTION_DATEN="$T/daten" python3 _werkzeuge/reception/server.py $PORT > "$T/server.log" 2>&1) & SP=$!; sleep 2
pr "S1 fremder Host" "$(curl -s -o /dev/null -w '%{http_code}' -H "Host: boese.example:$PORT" $B/ueberblick)" 421
pr "S2 Schreiben von fremder Herkunft" "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Origin: https://boese.example' -H 'Content-Type: application/json' -d '{}' $B/anfrage)" 403
pr "S3 Lesen von fremder Seite (Sec-Fetch-Site)" "$(curl -s -o /dev/null -w '%{http_code}' -H 'Sec-Fetch-Site: cross-site' $B/anfragen)" 403
head -c 3500000 /dev/zero | tr '\0' 'a' > "$T/gross.txt"
pr "S4 Anfrage über 3 MB" "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "$O" -H 'Content-Type: application/json' --data-binary @"$T/gross.txt" $B/nachtragen)" 413
pr "S5 kein JSON" "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "$O" -H 'Content-Type: text/plain' -d 'x' $B/nachtragen)" 415
letzt=200; for i in $(seq 1 125); do letzt=$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "$O" -H 'Content-Type: application/json' -d '{"id":"anfragen/2000-01-01/x.json","status":"gelesen"}' $B/anfrage); done
pr "S6 mehr als 120 Änderungen in einer Minute" "$letzt" 429
pr "F1 Formular ohne Herkunft (kein Browser der Seite)" "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{"name":"x","kontakt":"x@example.com"}' $B/formular)" 403
head -c 13000 /dev/zero | tr '\0' 'a' | sed 's/^/{"name":"/; s/$/"}/' > "$T/f.txt"
pr "F2 Formular über 12 kB" "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "$O" -H 'Content-Type: application/json' --data-binary @"$T/f.txt" $B/formular)" 413
pr "F3 Kontakt ungültig (keine E-Mail, keine Nummer)" "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "$O" -H 'Content-Type: application/json' -d '{"name":"QA","kontakt":"morgen"}' $B/formular)" 422
r=$(curl -s -X POST -H "$O" -H 'Content-Type: application/json' -d '{"name":"Robot","kontakt":"robot@example.com","website":"http://spam.example"}' $B/formular)
n=$(curl -s -H "$O" $B/anfragen | python3 -c "import json,sys; print(sum(1 for a in json.load(sys.stdin)['anfragen'] if a.get('name')=='Robot'))")
pr "F4 Maschine füllt das unsichtbare Feld: Antwort ok, kein Eintrag" "$r $n" '{"ok": true} 0'
r=$(curl -s -X POST -H "$O" -H 'Content-Type: application/json' -d '{"name":"Sicher QA","kontakt":"sicher-qa@example.com","art":"tisch","an":"event@doldenhorn.ch","anliegen":"Tisch QA"}' $B/formular)
pr "F5 Antwort an den Gast trägt nur ok und Dank, keine Daten des Hauses" "$(echo "$r" | python3 -c "import json,sys; print(sorted(json.load(sys.stdin)))")" "['danke', 'ok']"
letzt=200; for i in 1 2 3 4 5 6; do letzt=$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "$O" -H 'Content-Type: application/json' -d '{"name":"Grenze QA","kontakt":"g@example.com"}' $B/formular); done
pr "F6 mehr als 6 Formulare in einer Minute" "$letzt" 429
z=$(curl -s $B/zustand | python3 -c "import json,sys; p=[x for x in json.load(sys.stdin)['punkte'] if x['was']=='Assistent'][0]; print(p['stand'])")
a=$(curl -s -X POST -H "$O" -H 'Content-Type: application/json' -d '{"messages":[{"role":"user","content":"Habt ihr Fondue?"}],"sprache":"de"}' http://localhost:$PORT/api/gast | python3 -c "import json,sys; print('Probe' in json.load(sys.stdin).get('text',''))")
pr "K1 ohne RECEPTION_KI=1: kein Schlüssel, Chat antwortet als Probe, Prüfseite gelb" "$z $a" "gelb True"
kill $SP; wait $SP 2>/dev/null
grep -q "Schlüssel" "$T/server.log" && { rot=$((rot+1)); echo "ROT  K2 Server meldet einen Schlüssel"; } || { gruen=$((gruen+1)); echo "ok   K2 kein Schlüssel gelesen (Protokoll)"; }
echo "sicherheit: $gruen grün, $rot rot von $((gruen+rot))"
