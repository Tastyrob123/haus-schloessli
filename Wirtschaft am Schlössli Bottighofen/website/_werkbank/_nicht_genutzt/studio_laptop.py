#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus, Abschnitt «Studio» (12.10.2026, Master 5b Punkt 13): ein Laptop, in dessen Bildschirm das echte Studio liegt.

Bauart wie beim Grand Beau-Rivage (Regel «Gerät mit echtem Bildschirm»): das Gehäuse ist so gerendert, dass der Bildschirm ein exaktes Rechteck ist.
Der Inhalt liegt als schlichtes Rechteck UNTER dem Gehäuse, das Gehäuse hat dort ein Loch und lässt den Zeiger durch. Erst steht ein Standbild
derselben Seite, ein Klick auf den Bildschirm lädt das echte Studio (../studio/), das Standbild bleibt, bis es geladen ist. Solange das Studio läuft,
ruhen die Animationen der anderen Abschnitte. Verlässt der Abschnitt das Bild, wird das Studio wieder entladen.
Das Gehäuse (geraete/laptop-geraet.png, laptop.json) ist vom Grand Beau-Rivage übernommen, der Bildschirminhalt ist das Studio des Ruedihus
(node _werkbank/geraete/schirme.js studio → geraete/schirm-studio.jpg).
Eigen fürs Ruedihus: darunter bleiben die fünf kurzen Filme zu den wichtigsten Handgriffen und die dreizehn Bereiche (das hat das Grand Beau-Rivage nicht).
Eingehängt am Ende von haus.py über H.EIGENE (key 'studio' ersetzt den Kit-Abschnitt)."""
import json, os

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
G = os.path.join(W, 'geraete')
_LJ = os.path.join(G, 'laptop.json')
L = json.load(open(_LJ)) if os.path.exists(_LJ) else None
BEREIT = bool(L) and all(os.path.exists(os.path.join(G, f)) for f in ('laptop-geraet.png', 'schirm-studio.jpg'))
BILDER = [('lap-geraet', os.path.join(G, 'laptop-geraet.png'), 2000, dict(q=88)), ('lap-schirm', os.path.join(G, 'schirm-studio.jpg'), 1800, dict(q=84))] if BEREIT else []

PROBE = dict(
    titel='Im Bildschirm läuft das Studio selbst.',
    text='Was Sie hier sehen, ist das Werkzeug, mit dem Sie später arbeiten. Klicken Sie hinein und ändern Sie, was Sie möchten. Es ist eine Probe, auf Ihrer Seite ändert sich dabei nichts.',
    punkte=['Zimmerpreis ändern, und er stimmt auf jeder Seite', 'Ein Gericht anlegen, mit kleiner Portion und Preis', 'Einen Text direkt in der Seite neu schreiben', 'Jede Änderung wartet als Entwurf, bis Sie sie veröffentlichen'],
    knopf='Studio im eigenen Fenster öffnen', hin='Einmal auf den Bildschirm klicken, dann lässt sich das Studio direkt bedienen.',
    alt='Das Studio des Landgasthof Ruedihus: die Übersicht mit der Frage «Was möchten Sie tun?»')

JS = '''<script>(function(){var h=document.querySelector('#studio .stl-lap');if(!h||!matchMedia('(hover:hover) and (pointer:fine)').matches||innerWidth<760)return;
var e=h.querySelector('.stl-lap__s'),f=null,warte=0,FB=%(fb)d,FH=%(fh)d;
function mass(){if(f){var k=e.clientWidth/FB;f.style.transform='scale('+k.toFixed(5)+')'}}
function weg(){clearTimeout(warte);if(f){f.remove();f=null}e.classList.remove('live','laedt');document.documentElement.classList.remove('lap-ruhe')}
function zeig(x){if(x!==f||x.classList.contains('da'))return;clearTimeout(warte);x.classList.add('da');e.classList.remove('laedt');e.classList.add('live')}
/* Klick irgendwo auf den Bildschirm lädt das echte Studio; das Standbild bleibt, bis es geladen ist */
function live(){if(f)return;var x=document.createElement('iframe');x.title='Studio des Landgasthof Ruedihus';x.width=FB;x.height=FH;
x.onload=function(){setTimeout(function(){zeig(x)},350)};
f=x;e.classList.add('laedt');document.documentElement.classList.add('lap-ruhe');x.src=e.getAttribute('data-ziel');e.appendChild(x);mass();warte=setTimeout(function(){zeig(x)},9000)}
e.addEventListener('click',function(){if(!f)live()});addEventListener('resize',mass);
new IntersectionObserver(function(E){if(!E[0].isIntersecting)weg()},{threshold:0}).observe(h)})();</script>'''


def abschnitt(g):
    """EIGENE-Eintrag für haus.py. g = globals() von haus.py (STUDIO)."""
    ST = g['STUDIO']
    pf = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'

    def bau(k):
        bild, kn, e, m = k['bild'], k['kn'], k['e'], k['m']
        gw, gh = m['lap-geraet']; sw, sh = m['lap-schirm']
        x, y, b, h_ = L['schirm']
        laptop = (f'<div class="stl-lap" data-a="heben"><div class="stl-lap__b" style="aspect-ratio:{gw}/{gh}">'
                  f'<div class="stl-lap__s" data-ziel="{ST.get("link", "../studio/")}" style="left:{x * 100:.3f}%;top:{y * 100:.3f}%;width:{b * 100:.3f}%;height:{h_ * 100:.3f}%">'
                  f'<img class="ld stl-lap__bild" src="img/lap-schirm.webp" width="{sw}" height="{sh}" alt="{e(PROBE["alt"])}" loading="lazy" decoding="async">'
                  '<span class="stl-lap__k"><span class="a">Zum Bedienen klicken</span><span class="b">Wird geöffnet …</span><i><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 3.5v14.2l3.9-3.2 2.7 6 2.3-1-2.7-5.9 5.3-.4z"/></svg></i></span></div>'
                  f'<img class="ld frei stl-lap__g" src="img/lap-geraet.webp" width="{gw}" height="{gh}" alt="" loading="lazy" decoding="async"></div>'
                  f'<p class="stl-hin">{e(PROBE["hin"])}</p></div>')
        haken = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7"/></svg>'
        punkte = ''.join(f'<li style="--i:{i}">{haken}<span>{e(p)}</span></li>' for i, p in enumerate(PROBE['punkte']))
        schritte = ''.join(f'<button class="schritt" type="button" aria-pressed="{"true" if i == 0 else "false"}" data-film="film/{n}.mp4" data-bild="img/f-{n}.webp" data-adr="{e(a)}"><i>{i + 1:02d}</i><b>{e(t)}</b><span>{x_}</span><u></u></button>'
                           for i, (n, t, x_, a) in enumerate(ST['schritte']) if 'f-' + n in m)
        bereiche = ''.join(f'<li data-a="auf" style="--i:{i % 4}"><b>{e(b_)}</b><span>{x_}</span></li>' for i, (b_, x_) in enumerate(ST['bereiche']))
        filme = f'''<h3 class="stl-zw" data-a="auf">{e(ST.get('filme_titel', 'Fünf Handgriffe im Film'))}</h3>
    <div class="studio" data-a="auf">
      <div class="schritte">{schritte}</div>
      <div class="kino"><div class="fen__k"><i></i><i></i><i></i><span></span></div><div class="kino__s"><video muted playsinline preload="none"></video><span class="kino__play" data-wort="Gross ansehen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3.5v17l14-8.5z"/></svg></span><span class="kino__hin">Klick oder Esc zum Anhalten</span><div class="kino__k"><button type="button" data-nochmal>Nochmal</button></div></div></div>
    </div>''' if schritte else ''
        return f'''
<section class="fl {k['fl']} blatt stl" id="studio">
  <div class="in">
    {k['kopf']()}
    <div class="stl-b">
      {laptop}
      <div class="stl-t" data-a="auf" style="--i:2">
        <h3>{e(PROBE['titel'])}</h3>
        <i class="stl-linie"></i>
        <p>{PROBE['text']}</p>
        <ul class="stl-p">{punkte}</ul>
        {kn(PROBE['knopf'], ST.get('link', '../studio/'), neu=True)}
      </div>
    </div>
    {filme}
    <h3 class="stl-zw" data-a="auf">{e(ST.get('bereiche_titel', 'Was Sie selbst pflegen'))}</h3>
    <ul class="bereiche">{bereiche}</ul>
    <p class="hinweis hinweis--dunkel stl-hinweis" data-a="auf">{ST['hinweis']}</p>
  </div>
  {JS % dict(fb=L['fenster'][0], fh=L['fenster'][1])}
</section>'''
    return dict(key='studio', nach='handschrift', name=ST.get('name', 'Studio'), zeilen=['Sie pflegen die Seite', 'ganz einfach selbst.'], text=ST.get('text', ''), bau=bau)


CSS = '''
/* ---------- Studio: Laptop mit dem echten Studio im Bildschirm (studio_laptop.py, 12.10.2026) ---------- */
.stl-b{display:grid;grid-template-columns:minmax(0,1fr);gap:clamp(30px,4vw,72px);align-items:center}
.stl-b>*{min-width:0}
@media(max-width:700px){.stl-t .kn{max-width:100%;white-space:normal;line-height:1.35;text-align:left}.stl-t .kn i{flex:none}}
@media(min-width:1040px){.stl-b{grid-template-columns:minmax(0,1.5fr) minmax(0,.78fr)}}
.stl-lap{position:relative}
.stl-lap__b{position:relative;width:100%}
.stl-lap__b img{display:block;max-width:none}
.stl-lap__g{position:absolute;left:0;top:0;width:100%;height:auto;z-index:2;pointer-events:none}
.stl-lap__s{position:absolute;z-index:1;overflow:hidden;background:#1f1209}
.stl-lap__bild{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;object-position:50% 0}
.stl-lap__s iframe{position:absolute;left:0;top:0;max-width:none;border:0;background:#1f1209;transform-origin:0 0;opacity:0;pointer-events:none;z-index:3;transition:opacity .3s linear}
.stl-lap__s iframe.da{opacity:1;pointer-events:auto}
.stl-lap__k{display:none}
.stl-hin{display:none;margin:clamp(6px,1vw,14px) 0 0;text-align:center;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
html.lap-ruhe :is(.stapel .tel,.runter i,.zeile__z,.namenzug div,.haengt.da img,.glanz,.lb__z){animation-play-state:paused!important}
@media(hover:hover) and (pointer:fine) and (min-width:760px){
  .stl-hin{display:block}
  .stl-lap__s{cursor:pointer}.stl-lap__s.laedt{cursor:progress}.stl-lap__s.live{cursor:auto}
  .stl-lap__k{position:absolute;right:3%;bottom:5%;z-index:2;display:flex;align-items:center;gap:10px;padding:5px 5px 5px 16px;border-radius:999px;pointer-events:none;
    font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;line-height:1;white-space:nowrap;color:var(--tinte);
    background:linear-gradient(180deg,#fdf6e8 0%,#e9d3ad 100%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.9),inset 0 -1px 0 rgba(110,72,34,.35),0 0 0 1px rgba(201,133,67,.8),0 12px 22px -8px rgba(0,0,0,.8),0 3px 8px rgba(0,0,0,.4);transition:opacity .3s}
  .stl-lap__k i{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,#4b2f19 0%,#1f1209 100%);box-shadow:inset 0 1px 0 rgba(255,236,200,.2)}
  .stl-lap__k svg{width:14px;height:14px;fill:none;stroke:#f3cd94;stroke-width:1.7;stroke-linejoin:round}
  .stl-lap__k .b{display:none}.stl-lap__s.laedt .stl-lap__k .a{display:none}.stl-lap__s.laedt .stl-lap__k .b{display:inline}
  .stl-lap__s.live .stl-lap__k{opacity:0}
}
.stl [data-a="heben"]{opacity:0;transform:translateY(130px) scale(.965);transition:opacity 1.3s cubic-bezier(.16,1,.3,1),transform 2.1s cubic-bezier(.16,1,.3,1)}
.stl [data-a="heben"].da{opacity:1;transform:none}
.stl-t h3{margin:0;font-family:var(--serif);font-weight:700;font-size:clamp(1.7rem,2.5vw,2.6rem);line-height:1.1;color:#fbf5ea}
.stl-linie{display:block;width:64px;height:2px;margin:clamp(18px,2vw,28px) 0;background:linear-gradient(90deg,#c98543,rgba(201,133,67,0))}
.stl-t p{margin:0;max-width:44ch;font-size:clamp(1.02rem,1.1vw,1.12rem);line-height:1.64;color:rgba(251,245,234,.86)}
.stl-p{list-style:none;margin:clamp(18px,2vw,28px) 0 clamp(22px,2.4vw,34px);padding:0}
.stl-p li{display:grid;grid-template-columns:26px minmax(0,1fr);gap:12px;align-items:start;padding:13px 0;border-top:1px solid rgba(201,133,67,.24);font-size:clamp(1rem,1.06vw,1.08rem);line-height:1.45;color:#fbf5ea}
.stl-p li:last-child{border-bottom:1px solid rgba(201,133,67,.24)}
.stl-p svg{width:22px;height:22px;margin-top:1px;fill:none;stroke:var(--gold);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.stl-zw{margin:clamp(64px,7.4vw,120px) 0 clamp(24px,2.8vw,44px);text-align:center;font-family:var(--serif);font-weight:700;font-size:clamp(1.7rem,2.9vw,3rem);line-height:1.1;color:#fbf5ea}
.stl-zw::after{content:'';display:block;width:64px;height:2px;margin:clamp(14px,1.6vw,22px) auto 0;background:var(--gold);opacity:.8}
.stl .bereiche{margin-top:0}
.stl .schritt[aria-pressed="true"]{background:#4b2f19;box-shadow:inset 0 1px 0 rgba(255,236,200,.22),inset 0 0 0 1px rgba(201,133,67,.5),0 26px 30px -24px rgba(0,0,0,.9)}
.stl .kino{box-shadow:0 0 0 1px rgba(201,133,67,.3),0 50px 60px -40px rgba(0,0,0,.9)}
#studio .stl-hinweis{margin-inline:auto;text-align:center;max-width:none}
@media (prefers-reduced-motion:reduce){.stl [data-a="heben"]{opacity:1;transform:none;transition:none}}
'''
