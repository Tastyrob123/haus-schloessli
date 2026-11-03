#!/bin/zsh
# Probe-Kopie für die Prüfläufe des Besucherbuchs · Wirtschaft am Schlössli (Werkzeug-Master F25: je Chat eine eigene Kopie, Wegwerf-Daten).
# Aufbau wie das Projekt: website/ (APFS-Klon von assets/ und den Seiten) neben _werkzeuge/ (registre frisch, oberflaeche und maison nur gelesen).
# Am echten Schlössli wird nichts geschrieben; Zählungen der Prüfläufe gehen in einen eigenen Ordner unter /tmp (REGISTRE_ORDNER).
set -e
QUELLE="$HOME/Desktop/Website-Projekte/Wirtschaft am Schlössli Bottighofen"
PROBE="$HOME/Desktop/Website-Projekte/_Probe Schloessli Registre"
mkdir -p "$PROBE/website" "$PROBE/_werkzeuge"
rm -rf "$PROBE/website/assets"; cp -c -R "$QUELLE/website/assets" "$PROBE/website/assets"
for f in "$QUELLE"/website/*.html; do cp -c "$f" "$PROBE/website/" 2>/dev/null || cp "$f" "$PROBE/website/"; done
# Oberfläche des Hauses und Die Stube (andere Chats, nur gelesen)
for w in oberflaeche maison; do [ -d "$QUELLE/_werkzeuge/$w" ] && { rm -rf "$PROBE/_werkzeuge/$w"; cp -c -R "$QUELLE/_werkzeuge/$w" "$PROBE/_werkzeuge/$w"; } || true; done
rm -rf "$PROBE/_werkzeuge/registre"
cp -c -R "$QUELLE/_werkzeuge/registre" "$PROBE/_werkzeuge/registre"
rm -rf "$PROBE/_werkzeuge/registre/_daten"
# messung.js (Vorschlag) für den Zähl-Test an Seiten der Probe-Kopie: am Ende jeder Seite, nach haus.js, funktionen.js und fuss.js
cp "$QUELLE/_werkzeuge/registre/vorschlag/messung.js" "$PROBE/website/assets/js/messung.js"
for f in "$PROBE"/website/*.html; do grep -q 'assets/js/messung.js' "$f" || perl -0pi -e 's#</body>#<script src="assets/js/messung.js?v=probe" defer></script>\n</body>#' "$f"; done
echo "Probe-Kopie: $PROBE"
