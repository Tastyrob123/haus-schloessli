# Weingut-Texte aus eigener Recherche im Netz (19.10.2026), für Erzeuger ohne Wikipedia-Artikel. Nur belegte Fakten, Quelle je Eintrag.
# ALIAS: andere Schreibweisen desselben Erzeugers auf der Karte.
import json, pathlib
DATEI = pathlib.Path(__file__).resolve().parent / 'inhalt' / 'weingut-recherche.json'


def lies():
    return json.loads(DATEI.read_text()) if DATEI.exists() else {}


def dazu(eintraege):
    d = lies()
    d.update(eintraege)
    DATEI.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    return len(d)
