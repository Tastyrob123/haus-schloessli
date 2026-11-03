#!/usr/bin/env python3
"""Schlössli (Nachtbau 3./4.11.2026): der Ordner «Material» entsteht ganz in material_seite.py (alle Ordner, auch Sticker, Beigaben und Postkarten,
die beim Culinarium dieses Skript nach material.py des Kits dazulegte). Bleibt als Name für den Aufruf in bau_alles.sh:
   python3 _werkbank/material_mehr.py ["<website/_werkbank>"]   (wiederholbar)"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import material_seite  # noqa: E402

if __name__ == '__main__':
    material_seite.main()
