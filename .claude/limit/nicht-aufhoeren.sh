#!/bin/bash
# Stop-Hook: Die Sitzung darf erst aufhören, wenn UEBERGABE-LIMIT.md mit «Fertig.» oder «Nicht fertig.» beginnt.
# Gegen Endlosschleifen: nach 6 Sperren innerhalb von 15 Minuten darf sie aufhören (die Wache am Mac startet dann eine Folgesitzung).
D="$(cd "$(dirname "$0")" && pwd)"; R="$(cd "$D/../.." && pwd)"; Z="$D/sperren"
head -5 "$R/UEBERGABE-LIMIT.md" 2>/dev/null | grep -qE '^(«)?(Fertig\.|Nicht fertig\.)' && exit 0
JETZT=$(date +%s); touch "$Z"; awk -v j="$JETZT" '$1 > j-900' "$Z" > "$Z.n"; mv "$Z.n" "$Z"
[ $(wc -l < "$Z") -ge 6 ] && exit 0
echo "$JETZT" >> "$Z"
echo '{"decision":"block","reason":"Nicht aufhören: Der Auftrag ist offen (UEBERGABE-LIMIT.md beginnt nicht mit «Fertig.» oder «Nicht fertig.»). Laufende Unteragenten abwarten und prüfen, den nächsten offenen Schritt aus UEBERGABE-LIMIT.md weiterbauen, committen, pushen. Erst wenn alles fertig und geprüft ist: UEBERGABE-LIMIT.md mit «Fertig. …» beginnen lassen (oder «Nicht fertig. …» mit Grund, wenn es wirklich nicht weitergeht), pushen, dann aufhören."}'
