#!/usr/bin/env python3
"""Ein Kit-Schritt mit den Hauswerten des Reviers (feed_haus.py statt haus.py). Nachtbau 3./4.11.2026, Agent schloessli-werkbank-feed.
   python3 _werkbank/feed_bau.py <Kit-Skript> "<website/_werkbank>" [Argumente …]
   z. B.  python3 _werkbank/feed_bau.py feed.py "$P"   ·   python3 _werkbank/feed_bau.py material.py "$P"
Setzt das Modul «haus» auf feed_haus, bevor kern.py des Kits es lädt, und führt das Kit-Skript als __main__ aus."""
import os, runpy, sys

HIER = os.path.dirname(os.path.abspath(__file__))
KIT = os.environ.get('KIT') or next((p for p in sys.path if os.path.exists(os.path.join(p, 'kern.py'))), '/home/user/haus-schloessli/_Werkbank-Kit')
for p in (HIER, KIT):
    if p not in sys.path:
        sys.path.insert(0, p)
import feed_haus  # noqa: E402
sys.modules['haus'] = feed_haus

skript = sys.argv[1]
sys.argv = [os.path.join(KIT, skript)] + sys.argv[2:]
runpy.run_path(sys.argv[0], run_name='__main__')
