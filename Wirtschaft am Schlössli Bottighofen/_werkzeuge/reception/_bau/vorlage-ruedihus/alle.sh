#!/bin/bash
# Baut den Gastgeber (La Réception) des Landgasthof Ruedihus neu: Oberfläche und Server-Teil aus dem Grand Beau-Rivage (nur gelesen), Zusätze des Carlton-Europe
# und des Waldhotel Doldenhorn (nur gelesen), Hauswerte und Eingang des Ruedihus, Chat am Rechner, Steckbrief und Beispiele. Jeder Schritt bricht ab, wenn eine Stelle nicht trifft.
#   bash _werkzeuge/reception/_bau/alle.sh
set -e; cd "$(dirname "$0")"
for s in portiere ruedihus brief pdf server_teil abnahme eingang rahmen namen formulare formulare2 gast_bau beispiele_anfragen beispiele_fragen oberflaeche demo; do python3 "$s.py"; done
python3 ../steckbrief_bau.py
node --check ../reception.js && node --check ../baustein/anfrage.js && python3 -m py_compile ../reception.py ../gedaechtnis.py ../server.py ../probe_ki.py ../online/reception.py ../online/gast.py ../online/_reception_online.py
echo "Der Gastgeber gebaut, alles liest sich. Fassungsnummern in index.html hochzählen, wenn sich reception.js/.css oder studio/ geändert hat."
