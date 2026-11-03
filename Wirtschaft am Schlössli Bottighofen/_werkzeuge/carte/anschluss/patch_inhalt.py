#!/usr/bin/env python3
"""Die Tafel (La Carte) · Berghotel Gasterntal · Anschluss an den Bau der Website (C11, C18, C21): ergänzt inhalt.py so, dass karte_roh()
die von der Tafel veröffentlichten Zeilen der Karte 2026 nimmt (web.py zeilen(); ohne Veröffentlichung mit Anschluss bleibt alles Byte für
Byte wie bisher, an der APFS-Kopie geprüft). Der Schreibtisch legt seine eigene Fassung der Karte weiterhin darüber (C['karte'] geht vor);
damit nicht zwei Werkzeuge dieselben Zeilen pflegen, sperrt Der Schreibtisch die Karten-Stellen mit einem Weg zur Tafel (Master 4.2 C).

    python3 _werkzeuge/carte/anschluss/patch_inhalt.py <projektordner>          zeigt den Unterschied (nichts geschrieben)
    python3 _werkzeuge/carte/anschluss/patch_inhalt.py <projektordner> --setzen  setzt ein (Sicherung inhalt.py.vor-die-tafel daneben)

Einsetzen im echten Projekt macht der Werkbank-Chat (die Tafel baut nur am eigenen Ordner). Erprobt an einer APFS-Kopie: pruef/anschluss.js."""
import difflib, os, shutil, sys

ANKER = ('def karte_roh(reihe):\n'
         '    """Die geltenden Rubriken einer Reihe (speisen · getraenke), ausgeblendete schon weg."""\n'
         '    cur = C[\'karte\'].get(reihe)\n'
         '    rub = cur if isinstance(cur, list) else KARTE_STANDARD[reihe]\n')
NEU = ('_TAFEL = []\n\n\n'
       'def _die_tafel(reihe):\n'
       '    """Die Tafel (La Carte, Werkzeug, 17.10.2026): von der Tafel veröffentlichte Zeilen der Karte 2026 (_werkzeuge/carte/web.py zeilen()).\n'
       '    Ohne Veröffentlichung mit Anschluss None: dann gilt daten.py wie bisher."""\n'
       '    try:   # nach Pfad geladen, nicht über sys.path (Falle F10: gleichnamige Module)\n'
       '        if not _TAFEL:\n'
       '            import importlib.util as _iu\n'
       '            _sp = _iu.spec_from_file_location(\'die_tafel_web\', os.path.join(ROOT, \'_werkzeuge\', \'carte\', \'web.py\'))\n'
       '            _m = _iu.module_from_spec(_sp); _sp.loader.exec_module(_m); _TAFEL.append(_m)\n'
       '        return _TAFEL[0].zeilen(reihe, None)\n'
       '    except (ImportError, OSError, AttributeError, SyntaxError):\n'
       '        return None\n\n\n'
       'def karte_roh(reihe):\n'
       '    """Die geltenden Rubriken einer Reihe (speisen · getraenke), ausgeblendete schon weg."""\n'
       '    cur = C[\'karte\'].get(reihe)\n'
       '    rub = cur if isinstance(cur, list) else (_die_tafel(reihe) or KARTE_STANDARD[reihe])\n')


def neu_text(alt):
    if 'die_tafel_web' in alt:
        return alt
    assert alt.count(ANKER) == 1, 'Stelle in inhalt.py karte_roh() nicht gefunden (def karte_roh(reihe) mit ihren ersten drei Zeilen)'
    return alt.replace(ANKER, NEU)


if __name__ == '__main__':
    proj = os.path.abspath(sys.argv[1])
    p = os.path.join(proj, 'inhalt.py')
    alt = open(p, encoding='utf-8').read()
    neu = neu_text(alt)
    sys.stdout.writelines(difflib.unified_diff(alt.splitlines(True), neu.splitlines(True), 'inhalt.py', 'inhalt.py (mit der Tafel)'))
    if '--setzen' in sys.argv and neu != alt:
        shutil.copy2(p, p + '.vor-die-tafel')
        open(p + '.neu', 'w', encoding='utf-8').write(neu)
        os.replace(p + '.neu', p)
        print('\neingesetzt; Sicherung inhalt.py.vor-die-tafel')
