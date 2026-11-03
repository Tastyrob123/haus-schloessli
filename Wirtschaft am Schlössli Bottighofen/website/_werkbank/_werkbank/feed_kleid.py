#!/usr/bin/env python3
"""Feed-Seite im Kleid des Hauses (Nachtbau 3./4.11.2026, Agent schloessli-werkbank-feed). Läuft nach feed.py und feed_leicht.py, wiederholbar:
   python3 _werkbank/feed_kleid.py
- Schriften aus website/assets/fonts (die Seite des Kits sucht sie unter werkbank/fonts), Titel Open Sans 400 in Versalien gesperrt,
- Knöpfe, Ringe und Linien in Stuhlblau und Seehimmel statt der Messing-Töne der Vorlage, der Horizont als feine Linie unter dem Titel,
- Zahl im Kapitel ohne Nummer der Werkbank (die Seite steht für sich)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEITE = os.path.join(ROOT, 'feed', 'index.html')

KLEID = '''<style id="kleid-schloessli">
:root{--nacht:#0b1d3d;--tief:#0A234C;--stuhl:#113d88;--himmel:#A2B6CF;--himmel2:#C5D2E1;--blatt:#F4F6F9;--tinte:#041023}
body{background:var(--nacht) url(../assets/svg/tapete-a-dunkel.svg) 50% 0/168px auto}
.aside svg.ce{color:var(--himmel)}
.aside .kap{font-family:'DM Mono',ui-monospace,monospace;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--himmel)}
.aside .kap i{background:var(--himmel)}
.aside h1{font-family:'Open Sans',Arial,sans-serif;font-weight:400;text-transform:uppercase;letter-spacing:.08em;font-size:clamp(2.2rem,3.6vw,3.4rem);line-height:1.14;margin-bottom:0;padding-bottom:28px;position:relative}
.aside h1 em{color:var(--himmel)}
.aside h1::after{content:"";position:absolute;left:-100vw;right:-24px;bottom:0;height:0;border-top:1px solid rgba(162,182,207,.45)}
.aside h1+p{margin-top:28px}
.aside{position:relative;overflow:visible}
.aside dl{border-top-color:rgba(162,182,207,.3)}
.aside dt{color:var(--himmel)}
.kn{color:var(--blatt);background:linear-gradient(180deg,#1d4f9e,var(--stuhl) 60%,var(--tief));box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 0 0 1px rgba(162,182,207,.38),0 16px 26px -14px rgba(0,0,0,.7)}
.kn i{color:var(--tinte);background:linear-gradient(180deg,#f3f6f9,var(--himmel2) 55%,var(--himmel));box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}
.device{box-shadow:0 0 0 2px #2c2e36,0 0 0 9px #0a0c12,0 0 0 10px rgba(162,182,207,.35),0 60px 90px -30px rgba(0,0,0,.85)}
.avr{background:conic-gradient(#113d88,#C5D2E1,#0F3678,#A2B6CF,#113d88)}
.btns div.p{background:#113d88;color:#F4F6F9}
.t{background:#0b1d3d}
.post .img{background:#0b1d3d}
.zurueck{color:var(--blatt);background:linear-gradient(180deg,#1d4f9e,var(--stuhl) 60%,var(--tief));box-shadow:0 0 0 1px rgba(162,182,207,.38),0 10px 20px -8px rgba(0,0,0,.8)}
</style>
'''


def mach():
    t = open(SEITE, encoding='utf-8').read()
    t = re.sub(r"url\('\.\./werkbank/fonts/([^']+)'\)", lambda m: f"url('../assets/fonts/{m.group(1)}')", t)
    t = t.replace("font-family:'Baskerville CE'", "font-family:'Open Sans'").replace("'Baskerville CE',", "'Open Sans',")
    t = t.replace('url(/assets/svg/', 'url(../assets/svg/')
    t = re.sub(r'<p class="kap"><b style="font-weight:400">\d+</b><i></i>', '<p class="kap"><i></i>', t)
    t = re.sub(r'<style id="kleid-schloessli">.*?</style>\n', '', t, flags=re.S)
    t = t.replace('</head>', KLEID + '</head>', 1)
    open(SEITE, 'w', encoding='utf-8').write(t)


if __name__ == '__main__':
    mach()
    print('feed kleid: Schriften, Farben und Horizont gesetzt')
