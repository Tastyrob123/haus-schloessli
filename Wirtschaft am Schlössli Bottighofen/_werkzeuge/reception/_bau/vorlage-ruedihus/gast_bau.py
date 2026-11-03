#!/usr/bin/env python3
"""Legt den Gäste-Chat des Ruedihus für La Réception am Rechner an: _werkzeuge/reception/gast/ mit denselben Dateien, die online als api/ liegen
(Familie Maeder — Vier Häuser/gast_haeuser.py online(), nur gelesen und aufgerufen, nichts dort geändert):
  gast.py           die Chat-Funktion des Carlton-Europe (_gast/gast.py, unverändert kopiert; online api/gast.py)
  gast_wissen.txt   die Seiten des Hauses + die PDF-Unterlagen (assets/pdf/), gebaut mit gast_haeuser.wissen() wie beim Hochladen
  gast_tal.txt      Talwissen Kandersteg (Familie Maeder — Vier Häuser/_gast_tal/kandersteg.txt)
  gast_haus.json    Name, Ort, Telefon, Mail, Adresse, Muster und Modell des Ruedihus (HAEUSER['ruedihus'], MUSTER, MODELL)
Seiten: alle *.html im Projekt ausser Entwürfen (…varianten…, konzept), so wie sie online liegen (14 Seiten am 17.10.2026).
Aufruf: python3 _werkzeuge/reception/_bau/gast_bau.py   (nach jeder Änderung an den Seiten des Hauses erneut)"""
import glob, importlib.util, json, os, re, shutil, sys, tempfile
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.dirname(os.path.dirname(C))
WP = os.path.dirname(WEB)
FM = os.path.join(WP, 'Familie Maeder — Vier Häuser')
CARLTON_GAST = os.path.join(WP, 'Carlton-Europe Interlaken', '_gast', 'gast.py')
ZIEL = os.path.join(C, 'gast')
ENTWURF = re.compile(r'varianten|^konzept|^bildauswahl')


def gh():
    s = importlib.util.spec_from_file_location('gast_haeuser_nur_lesen', os.path.join(FM, 'gast_haeuser.py'))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def bau():
    g = gh(); h = g.HAEUSER['ruedihus']
    os.makedirs(ZIEL, exist_ok=True)
    shutil.copy2(CARLTON_GAST, os.path.join(ZIEL, 'gast.py'))
    # Wissen aus den Seiten wie beim Hochladen: wissen(z, h) liest z/*.html. Entwürfe bleiben draussen (online gibt es sie nicht).
    with tempfile.TemporaryDirectory() as z:
        n = 0
        for f in sorted(glob.glob(os.path.join(WEB, '*.html'))):
            if not ENTWURF.search(os.path.basename(f)):
                os.symlink(f, os.path.join(z, os.path.basename(f))); n += 1
        w, seiten = g.wissen(z, h)
    open(os.path.join(ZIEL, 'gast_wissen.txt'), 'w', encoding='utf-8').write(w)
    shutil.copy2(g.TAL_DATEI, os.path.join(ZIEL, 'gast_tal.txt'))
    k = 'ruedihus'
    json.dump({'name': h['name'], 'ort': h['ort'], 'tel': h['tel'], 'mail': h['mail'], 'adresse': h['adresse'], 'zeiten': h['zeiten'], 'fahrplan': g.FAHRPLAN,
               'kategorien': [], 'orte': g.ORTE_KANDERSTEG, 'muster': g.MUSTER[k], **({'modell': g.MODELL[k]} if k in g.MODELL else {})},
              open(os.path.join(ZIEL, 'gast_haus.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'gast/: {seiten} Seiten + Unterlagen im Wissen ({len(w):,} Zeichen), Talwissen {os.path.getsize(os.path.join(ZIEL, "gast_tal.txt")):,} Bytes')


if __name__ == '__main__':
    bau()
