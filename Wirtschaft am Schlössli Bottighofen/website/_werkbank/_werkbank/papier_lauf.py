#!/usr/bin/env python3
"""Ruft ein Skript des Kits (oder ein eigenes) mit dem Haus aus papier_haus.ein() auf (Werkbank Papier, Nachtbau 3.11.2026).
   PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/papier_lauf.py <skript.py> "<website/_werkbank>" [weitere]
Beispiel: python3 _werkbank/papier_lauf.py "$K/papier_seiten.py" "$P"   (Kit unverändert, nur das Haus kommt von papier_haus)"""
import os, runpy, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import papier_haus  # noqa: E402

papier_haus.ein()
skript = sys.argv[1]
sys.argv = [skript] + sys.argv[2:]
sys.path.insert(0, os.path.dirname(os.path.abspath(skript)))
runpy.run_path(skript, run_name='__main__')
