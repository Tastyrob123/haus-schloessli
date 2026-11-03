"""Hauswerte für die Kit-Schritte des Reviers Feed, Mails, Material (feed.py, material.py), unabhängig vom grossen haus.py der Werkbank.
Nachtbau 3./4.11.2026 (Agent schloessli-werkbank-feed): haus.py gehört dem Kern-Agenten und ist während des Umbaus nicht immer lauffähig;
feed_bau.py setzt dieses Modul als «haus» ein, bevor kern.py des Kits es lädt. Werte nur aus der Website des Hauses (assets, inhalt/haus.json)."""
import json, os
from hilfen import svg_innen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # website/_werkbank
WEB = os.path.dirname(ROOT)
HJ = json.load(open(os.path.join(WEB, 'inhalt', 'haus.json'), encoding='utf-8'))

NAME = HJ['name']                      # Wirtschaft am Schlössli
KURZ = 'schloessli'
LEISTE = 'WIRTSCHAFT AM SCHLÖSSLI'
HAUSART = 'restaurant'
PORT = 9288
DOMAIN = 'schloessli-bottighofen.ch'
RECHTE = 'Wirtschaft am Schlössli und den jeweiligen Fotografen.'
ADRESSE = f"{HJ['strasse']} · {HJ['ort']}"
# Farben des Hauses (website/assets/css/haus.css :root): Nacht über dem See, Stuhlblau, Seehimmel als Linie, Papier
FARBEN = dict(nacht='#0b1d3d', tief='#0A234C', navy='#113d88', blau='#0F3678', papier='#E7ECF3', creme='#D0DAE7', weiss='#F4F6F9',
              gold='#A2B6CF', messing='#0F3678', tinte='#041023', akzent='#0F3678', punkt='#FD9964')
SCHRIFT = dict(titel=('Open Sans', 'OpenSans-var.woff2'), titel_folge="'Open Sans',Arial,sans-serif", ersatz="local('Arial')", druckgewicht=400)
DRUCKSCHRIFT = [('Open Sans', 400, 'OpenSans-var.woff2')]
MUSTER = 'url(/assets/svg/tapete-a-dunkel.svg)'
MUSTER_B = '168px'
MUSTER_BILD = '/assets/svg/tapete-a-dunkel.svg'
MUSTER_DAEMPFUNG = 1
ZEICHEN = svg_innen(os.path.join(WEB, 'assets', 'svg', 'zeichen.svg'))
WORT = svg_innen(os.path.join(os.path.dirname(WEB), '_werkzeuge', 'oberflaeche', 'kleid', 'schloessli-marke.svg'))
ETIKETTEN = dict(ordner='untersetzer', name='Untersetzer', einzahl='Untersetzer')
REIHENFOLGE = ['brief', 'vergleich', 'ideen', 'gefuege', 'seiten', 'unterlagen', 'papier', 'feed', 'material', 'schluss']
SEITEN = []
STELLEN = []
