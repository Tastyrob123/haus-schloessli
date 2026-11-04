#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli: Brief und Schluss wie bei Wild Side, Culinarium und Schäfli (Robert 01.11.2026, nachgezogen 04.11.2026).
  Brief oben: nur die drei Orte mit dem gestrichelten Verlauf, kein Ticket (eigen/tg/brief.html).
  Schluss unten: Gruss wie in der Mail, Foto, Name, Kanäle, darunter das Billett von Tasty Studios (eigen/tg/schluss.html).
  Kapitel I als eigener heller Abschnitt ohne Tapete (sbf--weiss).
Markup, Schriften und Bilder unverändert aus der Schäfli-Werkbank (dort aus der Wild-Side-Demo); im Stilblatt nur die Tinte des Hauses (#041023) statt der des Schäfli.
Bilder im Gruss nie mit verzögertem Laden (Fehlerbuch 01.11.2026).
Laufband der Karten: der Trenner ist schon das Zeichen des Hauses (zeichen-c.svg in kapitel.css), darum hier keine eigene Regel."""
import os
import re
import shutil

Q = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen', 'tg')


def brief():
    return open(os.path.join(Q, 'brief.html'), encoding='utf-8').read()


def schluss():
    return open(os.path.join(Q, 'schluss.html'), encoding='utf-8').read()


ABGLEICH = ('<style id="abgleich-0411">'
            # Seiten-Reiter: nur umbrechen, wo sie am Rand angeschnitten wären (das Skript darunter setzt «gekappt»), zwei gleiche Reihen zu fünf
            '@media(min-width:900px){#seiten .wahl.gekappt{flex-wrap:wrap;justify-content:center;overflow:visible!important;max-width:640px;margin-left:auto;margin-right:auto;padding-left:0;padding-right:0}'
            '#seiten .wahl.gekappt>:first-child,#seiten .wahl.gekappt>:last-child{margin-left:0;margin-right:0}}'
            '</style>'
            # misst ohne Umbruch und setzt «gekappt» nur, wenn die Reihe breiter ist als ihr Platz (1440: alle zehn passen, 1280 und 1000: angeschnitten)
            '<script id="abgleich-0411-js">(function(){var r=document.querySelector("#seiten .wahl");if(!r)return;'
            'function m(){r.classList.remove("gekappt");if(innerWidth>=900&&r.scrollWidth>r.clientWidth+1)r.classList.add("gekappt")}'
            'm();addEventListener("resize",m);addEventListener("load",m);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(m)})();</script>')


def anwenden(root):
    """Nach dem Bau: Stilblatt, Schriften und Bilder in werkbank/, Stilblatt einhängen, Kapitel I hell. Zweimal bauen = einmal bauen."""
    wb = os.path.join(root, 'werkbank')
    os.makedirs(os.path.join(wb, 'img'), exist_ok=True)
    os.makedirs(os.path.join(wb, 'fonts', 'tg'), exist_ok=True)
    shutil.copy2(os.path.join(Q, 'gruss.css'), os.path.join(wb, 'gruss.css'))
    for f in ('tg-robert.webp', 'tg-tasty.png', 'tg-palmen.png'):
        shutil.copy2(os.path.join(Q, f), os.path.join(wb, 'img', f))
    for f in os.listdir(os.path.join(Q, 'fonts')):
        shutil.copy2(os.path.join(Q, 'fonts', f), os.path.join(wb, 'fonts', 'tg', f))
    seite = os.path.join(wb, 'index.html')
    t = open(seite, encoding='utf-8').read()
    if 'gruss.css' not in t:
        t = t.replace('</head>', '<link rel="stylesheet" href="gruss.css?v=04112026">\n</head>', 1)
    if 'id="abgleich-0411"' not in t:
        css, js = ABGLEICH.split('<script', 1)
        t = t.replace('</head>', css + '\n</head>', 1)
        t = t.replace('</body>', '<script' + js + '\n</body>', 1)
    t = re.sub(r'<section class="fl fl--nacht tapete-leicht blatt sbf" id="k1">', '<section class="fl fl--papier blatt sbf sbf--weiss" id="k1">', t, count=1)
    open(seite, 'w', encoding='utf-8').write(t)
