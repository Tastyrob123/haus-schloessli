#!/bin/zsh
# Die Tafel (La Carte) · Berghotel Gasterntal — alle Prüfläufe nacheinander auf Port 8971 (der eigene Server von La Carte muss vorher beendet sein).
#   zsh _werkzeuge/carte/pruef/alle.sh            → Protokolle in pruef/aus/<lauf>.txt, danach python3 pruef/bericht.py
cd "$(dirname "$0")/.."
A=pruef/aus; mkdir -p $A
for b in chromium webkit firefox; do
  for m in "1440 900" "1366 650" "390 844" "320 640"; do
    set -- ${=m}
    node pruef/lauf.js $b $1 $2 > $A/lauf-$b-$1.txt 2>&1; echo "lauf $b $1: $(tail -1 $A/lauf-$b-$1.txt)"
  done
done
for b in chromium webkit; do node pruef/gleich.js $b > $A/gleich-$b.txt 2>&1; echo "gleich $b: $(tail -1 $A/gleich-$b.txt)"; done
CARTE_PY=${CARTE_PY:-python3} node pruef/online_probe.js chromium > $A/online-chromium.txt 2>&1; echo "online: $(tail -1 $A/online-chromium.txt)"
node pruef/anschluss.js > $A/anschluss.txt 2>&1; echo "anschluss: $(tail -1 $A/anschluss.txt)"
# Flüssigkeit nur unter Rechnerlast 8 (höchstens 15 Minuten warten), danach die Bildschirmbilder
for i in {1..30}; do python3 -c 'import os,sys;sys.exit(0 if os.getloadavg()[0]<8 else 1)' && break; sleep 30; done
for b in chromium webkit; do node pruef/fluessig.js $b > $A/fluessig-$b.txt 2>&1; echo "fluessig $b: $(grep -c '^ok' $A/fluessig-$b.txt) ok, $(grep -c '^FEHLER' $A/fluessig-$b.txt) rot, $(grep -m1 'Rechnerlast' $A/fluessig-$b.txt)"; done
node pruef/bilder.js > $A/bilder.txt 2>&1; echo "bilder: $(wc -l < $A/bilder.txt) Bilder"
