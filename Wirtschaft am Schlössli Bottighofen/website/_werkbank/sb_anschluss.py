#!/usr/bin/env python3
"""Station 14 (Werkbank-Bauer, 19.10.2026): Werkzeuge an die Website anschliessen, ohne die Werkzeuge selbst zu ändern.
  1. Der gemeinsame Rahmen der Schlössli-Werkzeuge (_werkzeuge/oberflaeche/, gehört «Schlössli · La Carte») liegt als Kopie unter website/assets/oberflaeche/,
     damit /assets/oberflaeche/… auch dort antwortet, wo nur die Website ausgeliefert wird (Bitte in schloessli-werkzeug-rahmen.md). Quelle bleibt _werkzeuge/.
  2. Nach jedem Bau der Website zieht Der Schreibtisch nach (nachbau.py des Stamms, Bitte in schloessli-11-website.md); nur wenn sein Server :9035 läuft.
Aufruf: python3 _werkbank/sb_anschluss.py   (website/bau.py ruft es am Ende auf)"""
import os, shutil, subprocess, urllib.request

W = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(W); PROJEKT = os.path.dirname(ROOT)
q, z = os.path.join(PROJEKT, '_werkzeuge', 'oberflaeche'), os.path.join(ROOT, 'assets', 'oberflaeche')
if os.path.isdir(q):
    shutil.copytree(q, z, dirs_exist_ok=True)
    print('Rahmen der Werkzeuge kopiert nach assets/oberflaeche/')
try:
    urllib.request.urlopen('http://127.0.0.1:9035/_werkzeuge/bureau/', timeout=3)
    r = subprocess.run(['python3', os.path.expanduser('~/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/nachbau.py'), 'schloessli', '9035'], capture_output=True, text=True)
    print('Schreibtisch nachgezogen:', (r.stdout or r.stderr).strip()[-300:])
except Exception:
    print('Schreibtisch (:9035) läuft nicht, nichts nachgezogen')
