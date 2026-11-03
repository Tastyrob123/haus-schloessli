# Auftrag Nachtbau · Wirtschaft am Schlössli Bottighofen (04.11.2026)

Du bist Oberchef dieses Hauses. Lies zuerst `CLAUDE.md` (vor allem «Der Deal mit Robert», «Was fertig heisst» und «Limit und Übergabe»), dann `_Werkzeuge/OBERCHEF-PAKET.md`, `_Werkzeuge/ROBERTS-KRITERIEN.md`, `vorgaben/` falls vorhanden, `Wirtschaft am Schlössli Bottighofen/UEBERGABE.md`, `Wirtschaft am Schlössli Bottighofen/CHARAKTER.md` falls vorhanden und `_kette/`.
Vorbilder holen (öffentlich, ohne Schlüssel):
- `git clone --depth 1 https://github.com/Tastyrob123/haus-culinarium-hannover /tmp/culinarium` (Stamm der sieben Werkzeuge und der Werkbank)
- `git clone --depth 1 https://github.com/Tastyrob123/haus-wildside /tmp/wildside` (zuletzt fertig gebautes Haus nach demselben Weg, Regelwerke in `/tmp/wildside/vorgaben/`)
Kundenmaterial: Zweig `quelle` (siehe CLAUDE.md).

**Fertig um 09:00 Uhr Ortszeit Robert (UTC+8) am 04.11.2026, also 01:00 UTC.** Keine Ausrede, keine neue Zeitangabe, keine Begründung; hängt ein Teil, wird der Weg gewechselt, nicht die Zeit.

**Was schon da ist:** die Website (`Wirtschaft am Schlössli Bottighofen/website/`, Stand 19.10.), eine Werkbank in acht Kapiteln (`website/werkbank/`, `website/_werkbank/`) und ältere Werkzeug-Anfänge in `Wirtschaft am Schlössli Bottighofen/_werkzeuge/` (bureau, carte, imprimerie, livre, maison, reception, registre). Massstab ist trotzdem der Stand von Culinarium und Wild Side: was dort besser ist, wird übernommen.

1. **Werkbank** auf den Stand von `/tmp/culinarium/Culinarium Hannover/website/_werkbank/` bringen (mit `_Werkbank-Kit/`): alle Seiten (Start, Karte, KI, Geprüft, Befund, Unterlagen, Drucksachen, Untersetzer/Sticker, Feed, Mails, Material) mit Inhalt des Schlössli (Website, `website/inhalt/haus.json`, Karten-Daten, `quelle`), ohne Platzhalter.
2. **Die sieben Werkzeuge** aus `/tmp/culinarium/Culinarium Hannover/_werkzeuge/` (bzw. wie bei Wild Side) nach `Wirtschaft am Schlössli Bottighofen/_werkzeuge/` übernehmen und umkleiden: Name, Zeichen, Farben, Schriften aus Marke/Website des Schlössli; Hauswerte eintragen (Adresse, Zeiten, Karten inkl. Weinkarte und Lästermeile, Anlässe, Fotos aus `quelle`); aus der Werkbank verlinkt; Server wie in `cloud/haus.json`. Je Werkzeug ein Unteragent (Agent-Werkzeug, `model: "opus"`, nie Fable), parallel, jeder mit klarem Revier. Nichts neu erfinden.
3. **Drucksachen** der Plakatwerkstatt und der **Feed** für das Haus.
4. **Prüfen:** Ziellisten `_Werkzeuge/abnahme-tor/ziele-schloessli.json` und `_Werkzeuge/messlauf/ziele-schloessli.json` aus den Culinarium-Listen anlegen (Ports und Namen des Hauses, Stilblatt-Pfad des Hauses). Jedes Werkzeug gleich nach dem Bau mit `[schnell: <werkzeug>]` prüfen, Funde reparieren, noch einmal prüfen; am Ende `[schnell]` über alles. Fundbilder und je Werkzeug 15 Zustandsbilder mit dem Auge ansehen (Kriterien A).
5. **Übergabe laufend:** `UEBERGABE-LIMIT.md` nach jedem fertigen Schritt nachführen und pushen (siehe CLAUDE.md «Limit und Übergabe»). Commits auf `main` mit kurzer Nachricht, was fertig ist.

**Letzte Nachricht, genau eine:** «Fertig. <Link Werkbank> <Link Prüftafel>» – oder nur, wenn trotz Wegwechsel etwas fehlt: «Nicht fertig. <Links> – es fehlt: <Liste>». Keine Zwischenmeldungen, keine Begründungen, keine Technik, keine neue Uhrzeit. Deutsch, kurz, Alltagssprache.
Nichts verschicken, nichts veröffentlichen, nichts bezahlen, keine Schlüssel einchecken; nichts an anderen Häusern ändern; Grand Beau-Rivage nie anfassen.
