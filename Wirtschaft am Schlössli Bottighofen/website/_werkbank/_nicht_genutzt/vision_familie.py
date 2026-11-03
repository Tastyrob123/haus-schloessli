#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus, «Vier Häuser, eine Startseite.» (12.10.2026): das Gegenstück zur Vision des Grand Beau-Rivage (Master 5b Punkt 22).

Die vier Häuser der Familie Maeder und ihre gemeinsame Startseite, als Idee und nur mit Bildern: oben die Startseite, von ihr führt eine feine Linie
zu den vier Häusern darunter. Das Ruedihus leuchtet («In dieser Werkbank»), die drei anderen liegen leiser daneben («Auch als Entwurf da») und führen zu ihren Werkbänken,
die Startseite zu sich selbst (seit 12.10.2026 abends: alles geht an einen Empfänger, der alle vier Entwürfe und die Startseite in der Hand hat).
Kapitelwort und Titel sind mit den drei anderen Maeder-Werkbänken abgestimmt (Doldenhorn-Chat, 12.10.2026), der Fliesstext ist vom Ruedihus.
Aufnahmen: node _werkbank/vision_aufnahme.js → ansichten/Vision/<name>.jpg. Fehlen sie, fällt der Abschnitt weg.
Eingehängt am Ende von haus.py über H.EIGENE (key 'vier', nach 'geprueft')."""
import os

W = os.path.dirname(os.path.abspath(__file__))
_V = os.path.join(W, 'ansichten', 'Vision')
# Adressen wie BASIS und STARTSEITE in «Familie Maeder — Vier Häuser/bau.py» (lokal die Vorschau-Server; online.py setzt beim Hochladen die Online-Adressen ein)
STARTSEITE = 'http://localhost:8925/'
HAEUSER = [  # Bild, Name, Ort, Werkbank des Hauses ('' = dieses Haus)
    ('carlton', 'Carlton-Europe', 'Interlaken', 'http://localhost:8912/werkbank/'),
    ('doldenhorn', 'Waldhotel Doldenhorn', 'Kandersteg', 'http://localhost:8916/werkbank/'),
    ('ruedihus', 'Landgasthof Ruedihus', 'Kandersteg', ''),
    ('gasterntal', 'Berghotel Gasterntal', 'Selden', 'http://localhost:8918/werkbank/'),
]
BEREIT = all(os.path.exists(os.path.join(_V, n + '.jpg')) for n in ['familie'] + [h[0] for h in HAEUSER])
BILDER = ([('vi-familie', os.path.join(_V, 'familie.jpg'), 1500, dict(q=80, schnitt=16 / 10, lage=(.5, 0)))]
          + [('vi-' + n, os.path.join(_V, n + '.jpg'), 900, dict(q=78, schnitt=16 / 10, lage=(.5, 0))) for n, *_ in HAEUSER]) if BEREIT else []

# Alles geht an einen Empfänger (Robert 12.10.2026 abends): der Familie wird nicht aufgezählt, welche Häuser sie hat; die Startseite ist gebaut,
# die drei anderen Entwürfe liegen ihr ebenfalls vor. Zwei kurze Sätze, die Bilder führen zu den Werkbänken und zur Startseite.
TEXT = 'Das Ruedihus ist eines von vier Häusern, und für jedes liegt ein Entwurf da. Davor steht eine Startseite, auf der ein Gast sein Haus wählt. Ein Klick auf ein Bild öffnet es.'

def bau(k):
    e, bild = k['e'], k['bild']
    def haus(i, n, name, ort, ziel):
        innen = (f'<div class="vi-h__b">{bild("vi-" + n, "Die Startseite: " + name)}</div>'
                 f'<figcaption><b>{e(name)}</b><span>{e(ort)}</span><small>{"Auch als Entwurf da" if ziel else "In dieser Werkbank"}</small></figcaption>')
        if ziel:
            return f'<a class="vi-h" href="{ziel}" target="_blank" rel="noopener" data-a="auf" style="--i:{i}"><figure>{innen}</figure></a>'
        return f'<div class="vi-h vi-h--hier" data-a="auf" style="--i:{i}"><figure>{innen}</figure></div>'
    haeuser = ''.join(haus(i, *h_) for i, h_ in enumerate(HAEUSER))
    return f'''
<section class="fl {k['fl']} blatt vi" id="vier">
  <div class="in">
    {k['kopf']()}
    <div class="vi-b">
      <a class="vi-oben" href="{STARTSEITE}" target="_blank" rel="noopener" data-a="heben"><figure><div class="vi-oben__b">{bild('vi-familie', 'Die gemeinsame Startseite für die vier Häuser der Familie Maeder')}</div>
        <figcaption><b>Eine Startseite für alle vier</b><small>Als Entwurf gebaut</small></figcaption></figure></a>
      <svg class="vi-ast" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="M500 0V26M125 60V40Q125 26 139 26H861Q875 26 875 40V60M375 26V60M625 26V60"/></svg>
      <div class="vi-reihe">{haeuser}</div>
    </div>
  </div>
</section>'''


EINTRAG = dict(key='vier', nach='geprueft', nav='', name='Die Familie', zeilen=['Vier Häuser,', 'eine Startseite.'], text=TEXT, bau=bau)

CSS = '''
/* ---------- «Vier Häuser, eine Startseite.»: oben die gemeinsame Startseite, darunter die vier Häuser, nur Bilder (vision_familie.py, 12.10.2026) ---------- */
.vi-b{max-width:1280px;margin:0 auto}
.vi-oben{display:block;margin:0 auto;width:min(100%,640px);text-align:center;color:inherit;text-decoration:none}
.vi figure{margin:0}
a.vi-h{display:block;color:inherit;text-decoration:none}
.vi-oben__b img,.vi-h__b img{transition:transform 2.2s cubic-bezier(.16,1,.3,1),opacity .6s}
@media(hover:hover){a.vi-oben:hover img,a.vi-h:hover img{transform:scale(1.05);transition-duration:2.8s,.6s}a.vi-h:hover .vi-h__b img{opacity:.85}}
.vi-oben__b,.vi-h__b{border-radius:clamp(14px,1.4vw,22px);overflow:hidden;aspect-ratio:16/10;background:var(--tief);box-shadow:0 0 0 1px rgba(201,133,67,.3),0 34px 44px -26px rgba(0,0,0,.9),0 12px 18px -12px rgba(0,0,0,.6)}
.vi-oben__b img,.vi-h__b img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 0}
.vi-oben figcaption,.vi-h figcaption{margin-top:clamp(12px,1.3vw,18px);text-align:center}
.vi figcaption b{display:block;font-family:var(--serif);font-weight:700;font-size:clamp(1.14rem,1.36vw,1.4rem);line-height:1.15;color:#fbf5ea}
.vi figcaption span{display:block;margin-top:4px;font-size:1rem;color:rgba(251,245,234,.78)}
.vi figcaption small{display:inline-block;margin-top:9px;font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold)}
.vi-ast{display:block;width:100%;height:clamp(34px,4.4vw,60px);margin:clamp(10px,1.2vw,18px) 0 clamp(6px,.8vw,12px);fill:none;stroke:rgba(201,133,67,.6);stroke-width:1.2;vector-effect:non-scaling-stroke;overflow:visible}
.vi-ast path{vector-effect:non-scaling-stroke}
.vi-reihe{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(12px,1.6vw,26px)}
.vi-h{margin:0}
.vi-h:not(.vi-h--hier) .vi-h__b img{opacity:.62}
.vi-h:not(.vi-h--hier) figcaption b{color:rgba(251,245,234,.8)}
.vi-h:not(.vi-h--hier) figcaption small{color:rgba(243,205,148,.62)}
.vi-h--hier .vi-h__b{box-shadow:0 0 0 2px #c98543,0 0 0 7px rgba(42,24,10,.9),0 0 0 8px rgba(201,133,67,.4),0 40px 50px -26px rgba(0,0,0,.95)}
.vi [data-a="heben"]{opacity:0;transform:translateY(120px) scale(.965);transition:opacity 1.3s cubic-bezier(.16,1,.3,1),transform 2.1s cubic-bezier(.16,1,.3,1)}
.vi [data-a="heben"].da{opacity:1;transform:none}
.vi-t{display:grid;gap:clamp(16px,3vw,56px);max-width:1000px;margin:clamp(44px,5vw,80px) auto 0}
.vi-t p{margin:0;font-size:clamp(1.04rem,1.14vw,1.16rem);line-height:1.66;color:rgba(251,245,234,.86)}
@media(min-width:860px){.vi-t{grid-template-columns:1fr 1fr}}
@media(max-width:860px){.vi-ast{display:none}.vi-oben{margin-bottom:clamp(26px,5vw,40px)}.vi-reihe{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:clamp(24px,5vw,36px)}}
@media (prefers-reduced-motion:reduce){.vi [data-a="heben"]{opacity:1;transform:none;transition:none}}
'''
