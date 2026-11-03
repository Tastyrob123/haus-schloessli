#!/usr/bin/env python3
"""Baut das Konzept-Board (Station 06): bilder/*.webp, konzept.html, konzept.json.
Aufruf: python3 _bau/bau.py   (aus dem Ordner 06-konzepter oder von überall)"""
import html, json, os, sys
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
PAKET = os.path.dirname(HIER)
PROJ = os.path.abspath(os.path.join(PAKET, '..', '..'))
sys.path.insert(0, HIER)
from inhalt import B, HAEUSER, GESCHICHTE_SATZ, GESCHICHTE, IDEEN, SZENEN, UEBERLEITUNG, SEITEN, GESTRICHEN, OFFEN  # noqa: E402

E = html.escape
M = '../05-markenbauer/marke'


def rgb(h): return [int(h[i:i + 2], 16) for i in (1, 3, 5)]
def hx(c): return '#%02X%02X%02X' % tuple(max(0, min(255, round(x))) for x in c)
def mix(a, b, t): return hx([x + (y - x) * t for x, y in zip(rgb(a), rgb(b))])


STUHL, HIMMEL, SCHIRM = '#116788', '#A2C6CF', '#FD9964'
W = dict(nacht=mix(STUHL, '#000000', .64), tief=mix(STUHL, '#000000', .44), mittel=STUHL,
         kalk=mix(HIMMEL, '#FFFFFF', .74), kalk2=mix(HIMMEL, '#FFFFFF', .5), ak=HIMMEL, ak_h=mix(HIMMEL, '#FFFFFF', .38),
         ak_t=mix(STUHL, '#000000', .12), tinte=mix(STUHL, '#000000', .74), signal=SCHIRM, titel_h=mix(STUHL, '#000000', .4))


# ---------------------------------------------------------------- Bilder
def bild(k, breit=1400):
    quelle, r, f = B[k]
    ziel = os.path.join(PAKET, 'bilder', k + '.webp')
    if not os.path.exists(ziel):
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        im = Image.open(os.path.join(PROJ, quelle)).convert('RGB')
        if im.width > breit:
            im = im.resize((breit, round(im.height * breit / im.width)), Image.LANCZOS)
        im.save(ziel, 'WEBP', quality=80, method=6)
    return 'bilder/%s.webp' % k


for k in B:
    bild(k, 2000 if k in ('start', 'fliesen') else 1400)

PFEIL = '<span class="kn"><svg class="pf" viewBox="0 0 16 10"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span>'
ZEIGER = open(os.path.join(PAKET, M, 'zeichen', 'zeiger.svg'), encoding='utf-8').read().replace('<svg ', '<svg class="z" aria-hidden="true" ', 1)


# ---------------------------------------------------------------- Bühne: Bilder an der Linie (alle Masse in cqw)
def buehne(st, teil):
    if not st:
        return ''
    if st.get('fenster'):
        return ('<div class="fenster" data-a><img src="%s" alt="" loading="lazy"><p class="fsatz"><span>%s</span></p></div>'
                % (bild(st['fenster']), E(st['satz'])))
    if st.get('text'):
        return ('<div class="buehne buehne--text"><div class="linie" data-l></div><p class="fussnote schlitz" data-a><span>%s</span></p></div>' % E(st['text']))
    figs, L, oben = [], 0, []
    for k, w in st['figs']:
        _, r, f = B[k]
        h = w * r
        a = (f if f is not None else 1) * h
        oben.append((k, w, r, f, h, a))
        L = max(L, a)
    L += 3
    unten = 0
    teile = []
    for i, (k, w, r, f, h, a) in enumerate(oben):
        top = L - a
        unten = max(unten, top + h)
        u = st.get('unter')
        lab = ('<figcaption class="mono">%s</figcaption>' % E(u[i])) if u else ''
        teile.append('<figure class="fig" data-a style="--w:%.2f;--top:%.2f;--r:%.4f;--f:%s"><div class="rahmen"><img src="%s" alt="" loading="lazy"></div>%s</figure>'
                     % (w, top, r, ('%.3f' % f) if f is not None else '1', bild(k), lab))
    titel, just = '', 'center'
    if st.get('titel'):
        ort = st.get('titel_ort', 'rechts')
        frei = 100 - sum(o[1] for o in oben) - 2.2 * (len(oben) - 1) - 4
        if ort == 'innen':
            frei = 70
        else:
            just = 'flex-start' if ort == 'rechts' else 'flex-end'
        titel = '<p class="btitel btitel--%s schlitz" data-a style="--frei:%.1f"><span>%s</span></p>' % (ort, frei, E(st['titel']))
    hoehe = max(unten + (6 if st.get('unter') else 3), L + 6)
    if st.get('zwei'):
        hoehe = max(hoehe, L + 16)
    cls = 'buehne' + (' buehne--geteilt' if st.get('geteilt') else '') + (' buehne--ein' if len(oben) == 1 and oben[0][1] >= 99 else '')
    boden = ''
    if st.get('boden'):
        boden = '<div class="boden" style="--L:%.2f"><img src="%s" alt="" loading="lazy"></div>' % (L, bild(st['boden']))
    linie = '' if st.get('boden') else '<div class="linie" data-l style="--L:%.2f"></div>' % L
    zwei = ''
    if st.get('zwei'):
        zwei = ('<div class="linie linie--zwei" data-l style="--L:%.2f"></div><p class="etage" style="--L:%.2f">26</p><p class="etage etage--zwei" style="--L:%.2f">26</p>'
                '<div class="wahl" style="--L:%.2f"><span class="knopf">Tavolata%s</span><span class="knopf knopf--dunkel">Gesetztes Menü%s</span></div>'
                % (L - 13, L - 13, L, L - 11, PFEIL, PFEIL))
    breit = ''
    if st.get('breit'):
        breit = '<figure class="fig fig--breit" data-a><div class="rahmen"><img src="%s" alt="" loading="lazy"></div></figure>' % bild(st['breit'])
    return ('<div class="buehne-hulle"><div class="%s" style="--L:%.2f;--H:%.2f">%s%s%s<div class="reihe" style="justify-content:%s">%s</div>%s</div>%s</div>'
            % (cls, L, hoehe, linie, boden, zwei, just, ''.join(teile), titel, breit))


def flaeche_cls(fl):
    if fl.startswith('dunkel und hell'):
        return 'geteilt', 'Dunkel und hell geteilt'
    if fl == 'tapete dunkel':
        return 'dunkel', 'Dunkel mit Tapete'
    return {'dunkel': ('dunkel', 'Dunkel, Stuhlblau'), 'hell': ('matt', 'Hell, Seehimmel'), 'tapete': ('hell', 'Hell mit Punkt-Tapete')}[fl]


def link(haus):
    u = HAEUSER.get(haus)
    return ('<a href="%s" target="_blank" rel="noopener">%s</a>' % (E(u), E(haus))) if u else E(haus)


def szene(s, nr):
    cls, fl_name = flaeche_cls(s['flaeche'])
    bisher = ''.join('<li><span class="haus">%s</span><span>%s</span></li>' % (link(h), E(t)) for h, t in s['bisher'].items())
    bilder = ''.join('<li>%s</li>' % E(B[k][0].split('/')[-1]) for k in s['bilder']) or '<li>keine Bilder</li>'
    skizze = ('<div class="skizze"><h4>Skizze</h4><p>%s</p></div>' % E(s['skizze'])) if s.get('skizze') else ''
    ueber = UEBERLEITUNG.get(s['teil'])
    ueber_html = ('<div class="ueber"><div class="ulinie"></div><p>%s</p></div>' % E(ueber)) if ueber else ''
    return '''
<section class="szene %(cls)s" id="%(teil)s">
 <div class="innen">
  <header class="skopf">
   <h2 class="schlitz" data-a><span>%(titel)s</span></h2>
   <p class="ssatz">%(satz)s</p>
  </header>
  %(buehne)s
  <div class="drei">
   <div class="frage" data-a><h4>Einfall aus dem Haus</h4><p>%(einfall)s</p></div>
   <div class="frage" data-a><h4>Komposition</h4><p>%(komposition)s</p></div>
   <div class="frage" data-a><h4>Moment</h4><p>%(moment)s</p></div>
  </div>
  %(skizze)s
  <div class="steck">
   <div><h4>Baustein</h4><p><b class="bs">%(baustein)s</b> <span class="quelle q-%(quelle)s">%(qname)s</span></p></div>
   <div><h4>Bewegung</h4><p>%(bewegung)s</p></div>
   <div><h4>Fläche</h4><p class="fl"><i class="chip chip--%(cls)s"></i>%(fl)s</p></div>
   <div><h4>Teil</h4><p class="mono">%(teil)s</p></div>
   <div class="bilder"><h4>Bilder aus _quelle</h4><ul>%(bilder)s</ul></div>
  </div>
  <div class="vergleich">
   <div class="dieses"><h4>Dieses Haus</h4><p>%(unterschied)s</p></div>
   <div class="bisher"><h4>Bisherige Häuser an dieser Stelle</h4><ul>%(bisher)s</ul></div>
  </div>
 </div>
 %(ueber)s
</section>''' % dict(cls=cls, teil=s['teil'], titel=E(s['titel']), satz=E(s['satz']), buehne=buehne(s.get('stage'), s['teil']),
                     einfall=E(s['einfall']), komposition=E(s['komposition']), moment=E(s['moment']), skizze=skizze,
                     baustein=E(s['baustein']), quelle=s['quelle'], qname='aus dem Fundus' if s['quelle'] == 'fundus' else 'neu',
                     bewegung=E(s['bewegung']), fl=E(fl_name), bilder=bilder, unterschied=E(s['unterschied']), bisher=bisher, ueber=ueber_html)


def kopf():
    demo = [('start', 24), ('platanen', 15), ('glas', 13), ('abend', 15)]
    st = buehne(dict(figs=demo, titel=None), 'demo')
    ideen = ''.join('<div class="idee" data-a><p class="mono">%s</p><h3>%s</h3><p>%s</p></div>' % (E(a), E(b), E(c)) for a, b, c in IDEEN)
    inhalt = ''.join('<a href="#%s">%s</a>' % (s['teil'], E(s['titel'])) for s in SZENEN)
    return '''
<header class="kopf-board dunkel">
 <div class="innen">
  %s
  <p class="mono kz">Konzept-Board · Station 06 · intern · 19. Oktober 2026</p>
  <h1 class="schlitz" data-a><span>Wirtschaft am Schlössli</span></h1>
  <p class="geschichte">%s</p>
  <p class="geschichte2">%s</p>
 </div>
</header>
<section class="szene hell ideen-teil">
 <div class="innen">
  <header class="skopf"><h2 class="schlitz" data-a><span>Ein Horizont für alle Bilder.</span></h2>
  <p class="ssatz">Vier Fotos des Hauses, jedes mit seinem eigenen Horizont auf derselben Linie: so ordnet sich die ganze Seite. Beim Hereinkommen legen sie an.</p></header>
  %s
  <div class="ideen">%s</div>
  <nav class="inhalt"><p class="mono">Das Drehbuch der Startseite</p>%s</nav>
 </div>
</section>''' % (ZEIGER, E(GESCHICHTE_SATZ), E(GESCHICHTE), st, ideen, inhalt)


def unterseiten():
    rows = []
    for s in SEITEN:
        sz = ''.join('<li><span class="mono">%s</span><span>%s</span>%s</li>' % (
            E(t), E(x), ''.join('<img src="%s" alt="" loading="lazy">' % bild(b) for b in bs)) for t, x, bs in s['szenen'])
        rows.append('<div class="useite" data-a><h3>%s</h3><p class="mono">%s</p><ul>%s</ul></div>' % (E(s['titel']), E(s['seite']), sz))
    return '''
<section class="szene matt" id="unterseiten"><div class="innen">
 <header class="skopf"><h2 class="schlitz" data-a><span>Unterseiten, kürzer erzählt.</span></h2>
 <p class="ssatz">Alles, was das Haus heute hat (Seitenliste des Spähers), neu gedacht; Karten als Seiten statt PDF, Anfragen im Fenster statt im Mailprogramm, Reservation über gastronovi bleibt. Kein Klick führt ins alte Design. Jede Unterseite beginnt mit einem Seitenkopf auf der Linie.</p></header>
 <div class="useiten">%s</div>
</div></section>''' % ''.join(rows)


def liste(titel, satz, items, cls, id_):
    li = ''.join('<li><b>%s</b><span>%s</span></li>' % (E(a), E(b)) for a, b in items)
    return '''<section class="szene %s" id="%s"><div class="innen">
 <header class="skopf"><h2 class="schlitz" data-a><span>%s</span></h2><p class="ssatz">%s</p></header>
 <ul class="zliste">%s</ul></div></section>''' % (cls, id_, E(titel), E(satz), li)


CSS = r'''
@font-face{font-family:'Open Sans';src:url(%(m)s/schriften/OpenSans-var.woff2) format('woff2');font-weight:300 800;font-display:swap}
@font-face{font-family:'Instrument Sans';src:url(%(m)s/schriften/InstrumentSans-normal-400_600.woff2) format('woff2');font-weight:400 600;font-display:swap}
@font-face{font-family:'DM Mono';src:url(%(m)s/schriften/DMMono-normal-400.woff2) format('woff2');font-weight:400;font-display:swap}
:root{--nacht:%(nacht)s;--tief:%(tief)s;--mittel:%(mittel)s;--kalk:%(kalk)s;--kalk2:%(kalk2)s;--ak:%(ak)s;--ak-h:%(ak_h)s;--ak-t:%(ak_t)s;--tinte:%(tinte)s;--signal:%(signal)s;--titel-h:%(titel_h)s;
 --titel:'Open Sans',Arial,sans-serif;--lauf:'Instrument Sans',system-ui,sans-serif;--mono:'DM Mono',ui-monospace,Menlo,monospace;--rand:clamp(16px,5vw,64px);--e1:cubic-bezier(.16,1,.3,1);--rund:clamp(22px,2.6vw,34px)}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%%}
body{margin:0;background:var(--kalk);color:var(--tinte);font:400 16.5px/1.62 var(--lauf);-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{display:block;max-width:100%%}a{color:inherit}
.innen{max-width:1240px;margin:0 auto;padding:0 var(--rand)}
.mono{font-family:var(--mono);font-size:11.5px;letter-spacing:.17em;text-transform:uppercase}
.dunkel{background-color:var(--nacht);background-image:url(%(m)s/tapete-a-dunkel.svg);background-size:168px;color:#E9F0F2}
.hell{background-color:var(--kalk);background-image:url(%(m)s/tapete-a-hell.svg);background-size:168px}
.matt{background:var(--kalk2)}
.geteilt{background:linear-gradient(90deg,var(--nacht) 0 50%%,var(--kalk) 50%% 100%%)}
.szene{position:relative;border-radius:var(--rund) var(--rund) 0 0;margin-top:calc(var(--rund)*-1);padding:clamp(64px,8vw,112px) 0 clamp(72px,8vw,112px)}
.geteilt .skopf,.geteilt .drei,.geteilt .steck,.geteilt .vergleich,.geteilt .skizze{background:var(--kalk);color:var(--tinte);border-radius:20px;padding:22px 24px}
.geteilt .skopf{background:transparent;color:inherit;padding:0}
.geteilt .skopf h2,.geteilt .skopf p{color:#E9F0F2;max-width:46%%}
/* Kopf */
.kopf-board{padding:clamp(80px,11vw,150px) 0 clamp(110px,12vw,170px);text-align:center}
.kopf-board .z{width:46px;height:auto;color:var(--ak);margin:0 auto 22px;display:block}
.kopf-board .kz{color:var(--ak-h)}
.kopf-board h1{font:400 clamp(2.1rem,6vw,5rem)/1.08 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:18px 0 28px;color:#F4F8F9}
.geschichte{font:300 clamp(1.25rem,2.4vw,1.9rem)/1.4 var(--titel);max-width:34ch;margin:0 auto;color:#F4F8F9;text-wrap:balance}
.geschichte2{max-width:64ch;margin:26px auto 0;opacity:.82}
/* Szenen-Kopf */
.skopf{margin-bottom:clamp(28px,4vw,48px)}
.skopf h2{font:400 clamp(1.5rem,3.2vw,2.6rem)/1.16 var(--titel);text-transform:uppercase;letter-spacing:.14em;margin:0;color:var(--titel-h);max-width:26ch}
.dunkel .skopf h2{color:#F4F8F9}
.ssatz{max-width:70ch;margin:14px 0 0;opacity:.86}
.schlitz{overflow:hidden}.schlitz>span{display:inline-block}
.js .schlitz[data-a]>span{transform:translateY(108%%);transition:transform 1.3s var(--e1)}
.js .schlitz[data-a].da>span{transform:none}
/* Bühne */
.buehne-hulle{container-type:inline-size;margin:0 0 clamp(30px,4vw,52px)}
.buehne{position:relative;height:calc(var(--H)*1cqw)}
.reihe{position:absolute;inset:0;display:flex;gap:2.2cqw;justify-content:center}
.buehne--ein .reihe{justify-content:stretch}
.fig{margin:0;width:calc(var(--w)*1cqw);flex:none;position:relative;top:calc(var(--top)*1cqw)}
.fig .rahmen{overflow:hidden;border-radius:14px;aspect-ratio:1/var(--r);box-shadow:0 30px 50px -34px rgba(4,27,35,.55)}
.fig img{width:100%%;height:100%%;object-fit:cover;transform:scale(1.06);transition:transform 2.6s var(--e1)}
.fig.da img{transform:none}
.fig figcaption{margin-top:12px;text-align:center}
.js .fig[data-a]{transform:translateY(64px);transition:transform 1.5s var(--e1)}
.js .fig[data-a].da{transform:none}
.linie{position:absolute;left:0;right:0;top:calc(var(--L)*1cqw);height:1.5px;background:var(--ak-t);z-index:2;transform-origin:0 50%%;transition:transform 1.6s var(--e1)}
.dunkel .linie{background:var(--ak)}
.js .linie[data-l]{transform:scaleX(0)}.js .linie[data-l].da{transform:none}
.boden{position:absolute;left:0;right:0;top:calc(var(--L)*1cqw);height:5cqw;z-index:2;overflow:hidden}
.boden img{width:100%%;height:100%%;object-fit:cover}
.btitel{position:absolute;bottom:calc((var(--H) - var(--L))*1cqw + 10px);margin:0;z-index:3;font:400 clamp(1rem,2.6cqw,2.4rem)/1.15 var(--titel);letter-spacing:.16em;color:var(--titel-h);max-width:calc(var(--frei)*1cqw)}
.dunkel .btitel{color:#F4F8F9}
.btitel--rechts{right:0;text-align:right}.btitel--links{left:0}
.btitel--innen{left:4cqw;color:#fff;max-width:70cqw;font-size:clamp(1.2rem,4.4cqw,4rem);text-shadow:0 2px 30px rgba(4,27,35,.55)}
.geteilt .btitel{color:var(--titel-h)}
.buehne--text{height:auto;padding-top:60px}
.buehne--text .linie{top:40px}
.fussnote{font:300 clamp(1.3rem,3vw,2.4rem)/1.3 var(--titel);max-width:30ch;margin:0;color:var(--titel-h)}
.dunkel .fussnote{color:#F4F8F9}
.etage{position:absolute;right:0;top:calc(var(--L)*1cqw - 5.2cqw);margin:0;font:300 4.6cqw/1 var(--titel);color:var(--ak-t);z-index:3}
.dunkel .etage{color:var(--ak)}
.linie--zwei{opacity:1}
.wahl{position:absolute;left:0;top:calc(var(--L)*1cqw);display:flex;gap:12px;flex-wrap:wrap;z-index:3}
/* Fenster */
.fenster{position:relative;border-radius:22px;overflow:hidden;margin:0 0 clamp(30px,4vw,52px);aspect-ratio:21/9}
.fenster img{width:100%%;height:100%%;object-fit:cover}
.fsatz{position:absolute;inset:auto 0 0 0;margin:0;padding:60px 6%% 7%%;text-align:center;font:400 clamp(1.1rem,2.8vw,2.3rem)/1.2 var(--titel);letter-spacing:.12em;text-transform:uppercase;color:#fff;
 background:radial-gradient(ellipse at 50%% 90%%,rgba(4,27,35,.55),rgba(4,27,35,0) 70%%)}
.js .fenster[data-a]{transform:translateY(60px);transition:transform 1.5s var(--e1)}.js .fenster[data-a].da{transform:none}
/* Drei Fragen, Steckbrief, Vergleich */
.drei{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2.4vw,32px);margin-bottom:28px}
.frage{background:rgba(255,255,255,.55);border-radius:20px;padding:22px 24px;box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 24px 40px -34px rgba(4,27,35,.5)}
.dunkel .frage{background:rgba(255,255,255,.06);box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
.js .frage[data-a]{transform:translateY(34px);transition:transform 1.4s var(--e1)}.js .frage[data-a].da{transform:none}
h4{font:400 11px/1.3 var(--mono);letter-spacing:.17em;text-transform:uppercase;margin:0 0 8px;color:var(--ak-t)}
.dunkel h4{color:var(--ak)}
.frage p,.steck p,.vergleich p{margin:0}
.skizze{margin:0 0 28px;max-width:86ch}
.steck{display:grid;grid-template-columns:2fr 2fr 1.3fr 1fr 2fr;gap:22px;padding:22px 0;border-top:1px solid color-mix(in srgb,currentColor 18%%,transparent);border-bottom:1px solid color-mix(in srgb,currentColor 18%%,transparent);margin-bottom:28px}
.bs{font-weight:500}
.quelle{display:inline-block;font:400 10.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;padding:6px 10px;border-radius:12px;margin-left:6px;vertical-align:2px}
.q-neu{background:var(--signal);color:#2B1206}.q-fundus{background:var(--ak);color:#0B2530}
.chip{display:inline-block;width:18px;height:18px;border-radius:6px;vertical-align:-4px;margin-right:8px;border:1px solid rgba(0,0,0,.15)}
.chip--dunkel{background:var(--nacht)}.chip--hell{background:var(--kalk)}.chip--matt{background:var(--kalk2)}.chip--geteilt{background:linear-gradient(90deg,var(--nacht) 50%%,var(--kalk) 50%%)}
.bilder ul{margin:0;padding:0;list-style:none;font:400 11.5px/1.6 var(--mono);word-break:break-all;opacity:.8}
.vergleich{display:grid;grid-template-columns:1fr 1.6fr;gap:clamp(18px,3vw,40px)}
.dieses p{font:300 1.2rem/1.45 var(--titel)}
.bisher ul{margin:0;padding:0;list-style:none}
.bisher li{display:grid;grid-template-columns:minmax(150px,200px) 1fr;gap:14px;padding:9px 0;border-bottom:1px solid color-mix(in srgb,currentColor 12%%,transparent)}
.bisher .haus a{text-decoration:none;border-bottom:1px solid var(--ak);font-weight:500}
/* Überleitung */
.ueber{max-width:1240px;margin:clamp(40px,5vw,70px) auto 0;padding:0 var(--rand);position:relative}
.ulinie{height:1.5px;background:var(--signal);width:42px;margin-bottom:12px}
.ueber p{margin:0;font:300 1.15rem/1.4 var(--titel);max-width:52ch}
/* Ideen und Inhalt */
.ideen{display:grid;grid-template-columns:1fr 1fr;gap:clamp(16px,2.4vw,32px);margin-top:10px}
.idee{background:var(--nacht);color:#E9F0F2;border-radius:22px;padding:28px 30px;box-shadow:0 30px 50px -34px rgba(4,27,35,.6)}
.idee .mono{color:var(--ak)}
.idee h3{font:400 1.5rem/1.2 var(--titel);text-transform:uppercase;letter-spacing:.12em;margin:8px 0 12px}
.idee p{margin:0}
.js .idee[data-a]{transform:translateY(40px);transition:transform 1.4s var(--e1)}.js .idee[data-a].da{transform:none}
.inhalt{margin-top:clamp(36px,5vw,60px);display:flex;flex-wrap:wrap;gap:10px 22px;align-items:baseline}
.inhalt .mono{width:100%%;color:var(--ak-t);margin:0 0 6px}
.inhalt a{text-decoration:none;border-bottom:1px solid var(--ak-t);padding-bottom:2px}
/* Unterseiten */
.useiten{display:grid;grid-template-columns:repeat(2,1fr);gap:clamp(16px,2.4vw,30px)}
.useite{background:var(--kalk);border-radius:20px;padding:24px 26px;box-shadow:0 26px 44px -34px rgba(4,27,35,.5)}
.useite h3{font:400 1.25rem/1.2 var(--titel);text-transform:uppercase;letter-spacing:.12em;margin:0 0 4px;color:var(--titel-h)}
.useite>.mono{color:var(--ak-t);margin:0 0 14px}
.useite ul{list-style:none;margin:0;padding:0}
.useite li{display:grid;grid-template-columns:96px 1fr;gap:6px 14px;padding:10px 0;border-top:1px solid rgba(4,27,35,.1)}
.useite li img{grid-column:2;width:120px;height:80px;object-fit:cover;border-radius:10px;display:inline-block;margin:4px 8px 0 0}
.useite li .mono{font-size:10.5px;color:var(--ak-t)}
.js .useite[data-a]{transform:translateY(40px);transition:transform 1.4s var(--e1)}.js .useite[data-a].da{transform:none}
.zliste{list-style:none;margin:0;padding:0;columns:2;column-gap:clamp(20px,4vw,56px)}
.zliste li{break-inside:avoid;padding:12px 0;border-top:1px solid color-mix(in srgb,currentColor 16%%,transparent)}
.zliste b{display:block;font-weight:500;margin-bottom:2px}
.knopf{position:relative;display:inline-flex;align-items:center;gap:16px;height:50px;padding:0 5px 0 22px;border-radius:25px;overflow:hidden;
 font:400 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:#0B2530;
 background:linear-gradient(180deg,color-mix(in srgb,var(--ak) 55%%,#fff),var(--ak) 58%%,color-mix(in srgb,var(--ak) 80%%,#000));
 box-shadow:inset 0 1px 0 rgba(255,255,255,.6),inset 0 -2px 0 rgba(0,0,0,.18),0 20px 30px -20px rgba(0,0,0,.6)}
.knopf .kn{width:40px;height:40px;border-radius:50%%;display:grid;place-items:center;background:linear-gradient(180deg,var(--tief),var(--nacht));color:var(--ak-h)}
.knopf .pf{width:15px;height:10px;stroke:currentColor;fill:none;stroke-width:1.3}
.knopf--dunkel{color:#F2F5F5;background:linear-gradient(180deg,var(--mittel),var(--tief) 60%%,var(--nacht))}
.knopf--dunkel .kn{background:linear-gradient(180deg,var(--ak-h),var(--ak));color:#0B2530}
.fuss{background:var(--nacht);color:#C9D6DA;padding:60px 0 70px;text-align:center;border-radius:var(--rund) var(--rund) 0 0;margin-top:calc(var(--rund)*-1);position:relative}
.fuss .z{width:30px;color:var(--ak);margin:0 auto 14px;display:block;height:auto}
/* Handy */
@media (max-width:760px){
 .drei,.vergleich,.ideen,.useiten{grid-template-columns:1fr}
 .steck{grid-template-columns:1fr 1fr}
 .bisher li{grid-template-columns:1fr;gap:2px}
 .zliste{columns:1}
 .geteilt{background:var(--nacht)}
 .geteilt .skopf h2,.geteilt .skopf p{max-width:none}
 .buehne{height:auto}
 .reihe{position:static;flex-direction:column;gap:22px}
 .fig{width:100%%;top:0}
 .fig .rahmen{max-height:70vh}
 .linie{display:none}
 .boden{position:static;height:44px;border-radius:8px;margin-top:22px}
 .btitel,.btitel--innen{position:static;max-width:none;font-size:1.3rem;margin:18px 0 0;text-shadow:none;color:inherit;text-align:left}
 .etage,.linie--zwei{display:none}
 .wahl{position:static;margin-top:16px}
 .buehne--text .linie{display:block;top:20px}
 .buehne--text{padding-top:40px}
 .fenster{aspect-ratio:4/5}
 .useite li{grid-template-columns:1fr}
 .useite li img{grid-column:1}
}
@media (prefers-reduced-motion:reduce){.js [data-a],.js [data-a]>span,.js .linie[data-l],.fig img{transform:none!important;transition:none!important}}
'''


JS = r'''<script>
document.documentElement.classList.add('js');
(function(){
 var els=document.querySelectorAll('[data-a],[data-l]');
 if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('da')});return}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('da');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
 var vh=window.innerHeight||800;
 els.forEach(function(e){var r=e.getBoundingClientRect();if(r.top<vh&&r.bottom>0){e.classList.add('da')}else{io.observe(e)}});
})();
</script>'''


def main():
    body = kopf()
    for i, s in enumerate(SZENEN):
        if s['teil'] == 'fuss':
            body += szene(s, i)
            continue
        body += szene(s, i)
    body += unterseiten()
    body += liste('Gestrichen.', 'Überlegt und verworfen, damit es kein anderer Chat wieder aufmacht.', GESTRICHEN, 'hell', 'gestrichen')
    body += liste('Offen.', 'Was nicht belegt ist oder fehlt; steht auch auf der Karte unter Station 06.', OFFEN, 'matt', 'offen')
    body += '<footer class="fuss">%s<p class="mono">Wirtschaft am Schlössli · Konzept-Board · nur intern, geht nie an den Kunden</p></footer>' % ZEIGER
    css = CSS % dict(m=M, **W)
    doc = ('<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<meta name="robots" content="noindex"><title>Konzept · Wirtschaft am Schlössli</title>'
           '<meta name="description" content="Konzept-Board Station 06: Geschichte, Drehbuch und Szenen der neuen Startseite.">'
           '<link rel="icon" href="%s/zeichen/zeiger.svg"><style>%s</style></head><body>%s%s</body></html>' % (M, css, body, JS))
    open(os.path.join(PAKET, 'konzept.html'), 'w', encoding='utf-8').write(doc)

    # konzept.json im Format der Kette
    szenen = []
    for s in SZENEN:
        d = dict(teil=s['teil'], titel=s['titel'], satz=s['satz'], bilder=[B[k][0] for k in s['bilder']], baustein=s['baustein'], quelle=s['quelle'])
        if s['quelle'] == 'neu':
            d['skizze'] = s.get('skizze', '')
        elif s.get('skizze'):
            d['skizze'] = s['skizze']
        d.update(bewegung=s['bewegung'], flaeche=s['flaeche'], einfall=s['einfall'], komposition=s['komposition'], moment=s['moment'],
                 unterschied=s['unterschied'], bisher=s['bisher'], ueberleitung=UEBERLEITUNG.get(s['teil']))
        szenen.append(d)
    seiten = [dict(seite='index.html', titel='Startseite', szenen=szenen)]
    for s in SEITEN:
        seiten.append(dict(seite=s['seite'], titel=s['titel'], szenen=[dict(teil=t, satz=x, bilder=[B[b][0] for b in bs]) for t, x, bs in s['szenen']]))
    k = dict(geschichte=GESCHICHTE, geschichte_satz=GESCHICHTE_SATZ,
             ideen=[dict(art=a, name=b, satz=c) for a, b, c in IDEEN],
             seiten=seiten, gestrichen=[dict(was=a, grund=b) for a, b in GESTRICHEN],
             offen=[dict(punkt=a, wo=b) for a, b in OFFEN],
             familie_machart=None,
             familie_hinweis='Taverne zum Schäfli Wigoltingen gehört zur Familie, hat aber noch keine abgenommenen Seiten; nichts übernommen, nichts wiederholt.',
             bisherige_haeuser=HAEUSER, stand='19.10.2026, erster Durchgang ohne Blender')
    json.dump(k, open(os.path.join(PAKET, 'konzept.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ok', os.path.getsize(os.path.join(PAKET, 'konzept.html')), 'Bytes')


main()
