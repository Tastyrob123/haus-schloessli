#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli (Vorlage Ruedihus), Abschnitt «Handschrift» als Tafel mit Bewegung (12.10.2026, Master 5b Punkt 11).

Ersetzt den Standard-Abschnitt des Kits über H.EIGENE (key 'handschrift'). Eine helle Tafel mit vier Zeilen:
  Zeichen und Name   das Medaillon in Gold und die Wortmarke auf Wandholz mit Butzenscheiben, daneben woher sie kommen
  Drei Schriften     jede mit ihrer Rolle und einer Zeile aus dem Haus
  Farben             neun Töne und das Rot der Geranien, darunter woher jeder Ton stammt: gemessen aus den Bildern des Hauses
                     (assets/css/main.css :root und _recherche/farben.json, dort steht zu jedem Ton die Aufnahme)
  Muster und Knöpfe  die Butzenscheiben als Tapete, zwei Knöpfe zum Drücken
Alles in der Tafel kommt in Bewegung an: Bausteine fliegen herauf, Töne füllen sich von links nach rechts, Fotos landen,
danach bauen sich die kleinen Farbbalken auf. Nur translate, rotate, scale und opacity.
Kein Markenbuch als eigene Seite: das gehört zum Grand Beau-Rivage, hier steht alles in der Tafel selbst."""
import html, os, re
from PIL import Image

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
IMG = os.path.join(ROOT, 'assets', 'img')

TEXT = ('Ihre Zeiger und Ihr Name bleiben, wie man sie kennt. Dazu kommen die Schrift Ihres Logos für die grossen Zeilen, in Versalien, '
        'eine ruhige für den Lesetext und Farben von Ihrer Terrasse: das Blau der Stühle, der Himmel über dem See und das Rot der Schirme, nur als Punkt.')

SCHRIFTEN = [('Grosse Zeilen', 'a', 'Open Sans', 'Aa', 'DIREKT IM HAFEN', 'Die Schrift Ihres Logos, in Versalien und weit gesperrt.'),
             ('Lesetext', 's', 'Instrument Sans', 'Aa', 'Mit Blick aufs Wasser und die Alpen', 'Liest sich leicht, auch wenn es einmal mehr Text ist.'),
             ('Kleine Angaben', 'm', 'DM Mono', 'Aa', 'Seestrasse 50 · 8598 Bottighofen', 'Für Zeiten, Preise und Adressen.')]

GRUPPEN = [  # Gruppe, Töne (Schlüssel, Name, Wert): die Farben der neuen Seite (assets/css/haus.css), hergeleitet im Markenbuch (Farbwelt A «Stuhl und See»)
    ('Kalk und Papier', [('papier', 'Papier', '#f3f6f9'), ('kalk', 'Kalk', '#e7ecf3'), ('kalk2', 'Seespiegel', '#d0dae7')]),
    ('Stuhlblau', [('stuhl', 'Stuhlblau', '#113d88'), ('tief', 'Tiefe', '#0a234c'), ('nacht', 'Nacht', '#0b1d3d')]),
    ('Seehimmel', [('himmel', 'Seehimmel', '#a2b6cf'), ('dunst', 'Dunst', '#c5d2e1'), ('wasser', 'Tiefes Wasser', '#0f3678')]),
    ('Nur als Punkt', [('schirm', 'Schirmrot', '#fd9964')]),
]
F = {k: n for _, l in GRUPPEN for k, n, _ in l}
HERKUNFT = [  # Foto (assets/img), Titel, Töne daraus (Markenbuch: Fundstellen der Farben)
    ('start', 'Die Stühle auf der Terrasse', ['stuhl', 'tief', 'nacht']),
    ('morgen', 'Der See am Morgen', ['kalk2', 'himmel', 'dunst']),
    ('glas', 'Ein Glas vor dem See', ['papier', 'kalk']),
    ('baum', 'Ein Schirm am Ufer', ['schirm']),
]
LAGE = {'start': (.5, .7), 'baum': (.75, .4)}
import haus as _H
BILDER = [('hs-' + k, _H.bild(k, 1200), 760, dict(schnitt=4 / 5, lage=LAGE.get(k, (.5, .5)))) for k, _, _ in HERKUNFT]


def streifen(key, n=5):
    """Die Töne eines Fotos, gemessen: Median-Schnitt auf n Farben, nach Helligkeit sortiert, Breite = Anteil im Bild."""
    p = next(os.path.join(IMG, f'{key}{s}.webp') for s in ('-800', '-1200', '-480', '') if os.path.exists(os.path.join(IMG, f'{key}{s}.webp')))
    im = Image.open(p).convert('RGB'); im.thumbnail((360, 360))
    q = im.quantize(n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:n * 3]; ges = im.size[0] * im.size[1]
    t = [(c / ges, '#%02x%02x%02x' % tuple(pal[i * 3:i * 3 + 3])) for c, i in q.getcolors()]
    t.sort(key=lambda x: -sum(int(x[1][i:i + 2], 16) for i in (1, 3, 5)))
    return t


def abschnitt(h):
    """h = globals() von haus.py (ZEICHEN, WORT, NAME, HANDSCHRIFT)."""
    zvb, wvb, wort_innen, HS = h['ZEICHEN'][0], h['WORT'][0], h['WORT'][1], h['HANDSCHRIFT']
    pf = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'

    def bau(c):
        bild = c['bild']
        z = f'<svg class="hs2-zz" viewBox="{zvb}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'
        w = f'<svg class="hs2-ww" viewBox="{wvb}" fill="currentColor" role="img" aria-label="{e(h["NAME"])}">{wort_innen}</svg>'
        schriften = ''.join(f'<div class="hs2-schrift"><small>{e(r)}</small><div class="hs2-aa hs2-f-{k}" aria-hidden="true">{aa}</div><b>{e(n)}</b><span class="hs2-f-{k}">{e(p)}</span><i>{e(x)}</i></div>'
                            for r, k, n, aa, p, x in SCHRIFTEN)
        band = ''.join(f'<div class="hs2-gr" style="--n:{len(l)}"><div class="hs2-gr__t">' + ''.join(f'<span class="hs2-chip" style="--c:{hx}"><i></i><b>{e(n)}</b><small>{hx.upper()}</small></span>' for _, n, hx in l) + f'</div><p>{e(gn)}</p></div>'
                       for gn, l in GRUPPEN)
        her = ''
        for key, t, toene in HERKUNFT:
            if 'hs-' + key not in c['m']:
                continue
            st = ''.join(f'<i style="flex:{max(a, .06):.3f};background:{hx}"></i>' for a, hx in streifen(key))
            her += f'<figure><div class="hs2-bild">{bild("hs-" + key, t)}</div><div class="hs2-st">{st}</div><figcaption>{e(t)}<small>daraus: {", ".join(F[k] for k in toene)}</small></figcaption></figure>'
        kn1, kn2 = HS.get('knoepfe', ('Nur zu', 'Noch einer'))
        return f'''
<section class="fl {c['fl']} blatt hs2" id="handschrift">
  <div class="in">
    {c['kopf']()}
    <div class="hs2-bogen" data-a="heben">
      <div class="hs2-z hs2-marke">
        <div class="hs2-tafel">{z}{w}<small>Bottighofen · am Hafen</small></div>
        <div>
          <p class="hs2-etik"><span>Zeichen und Name</span></p>
          <p>{HS['marke_text']}</p>
          <dl><dt>Zeichen</dt><dd>die Zeiger aus Ihrem Logo, als Zeichnung</dd><dt>Name</dt><dd>Open Sans in Versalien, weit gesperrt</dd><dt>Auf Dunkel</dt><dd>Seehimmel auf Stuhlblau, mit dem Punktraster</dd></dl>
        </div>
      </div>
      <div class="hs2-z">
        <p class="hs2-etik"><span>Drei Schriften</span><span>jede mit ihrer Rolle</span></p>
        <div class="hs2-schriften">{schriften}</div>
      </div>
      <div class="hs2-z">
        <p class="hs2-etik"><span>Farben</span><span>neun Töne und das Rot der Schirme</span></p>
        <div class="hs2-band">{band}</div>
      </div>
      <div class="hs2-z">
        <p class="hs2-etik"><span>Woher die Farben kommen</span><span>aus Ihren Bildern gemessen</span></p>
        <div class="hs2-her">{her}</div>
      </div>
      <div class="hs2-z hs2-muster">
        <div class="hs2-butzen">{z}</div>
        <div>
          <p class="hs2-etik"><span>{e(HS['muster_etik'])}</span></p>
          <p>{HS['muster_text']}</p>
        </div>
        <div class="hs2-kn">
          <p>{HS.get('knopf_text', '')}</p>
          <div class="kn-reihe hell"><button class="kn" type="button">{e(kn1)}<i>{pf}</i></button><button class="kn kn--linie" type="button">{e(kn2)}<i>{pf}</i></button></div>
        </div>
      </div>
    </div>
  </div>
</section>'''

    return dict(key='handschrift', nach='unterlagen', name='Handschrift', zeilen=['Ihre Zeiger', 'bleiben, wie sie sind.'], text=TEXT, bau=bau)


CSS = '''
/* ---------- Handschrift als Tafel (marke_werkbank.py, 12.10.2026) ---------- */
.hs2{--hl:rgba(42,26,14,.14)}
.hs2-bogen{border-radius:34px;background:var(--weiss);color:var(--tinte);box-shadow:inset 0 1px 0 #fffdf7,0 50px 70px -50px rgba(0,0,0,.9);overflow:hidden}
/* die Tafel selbst steht still: in ihr bewegen sich die Bausteine, eine so grosse Fläche müsste sonst bei jedem Schritt neu gezeichnet werden */
.hs2 .hs2-bogen[data-a="heben"]{opacity:1;transform:none}
.hs2-z{padding:clamp(28px,3.4vw,56px) clamp(22px,3.6vw,60px);border-top:1px solid var(--hl)}
.hs2-z:first-child{border-top:0}
.hs2-etik{display:flex;justify-content:space-between;gap:20px;font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--taupe);margin:0 0 clamp(20px,2.4vw,34px)}
.hs2-etik span:last-child:not(:first-child){color:rgba(42,26,14,.5)}
.hs2-marke{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);gap:clamp(24px,3.4vw,56px);align-items:center}
.hs2-tafel{border-radius:24px;background:var(--blau) var(--muster) 50% 0/var(--musterb) auto;color:#d9ae6c;min-height:clamp(280px,26vw,390px);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:clamp(30px,3vw,48px) 24px;
  box-shadow:inset 0 1px 0 rgba(255,236,200,.14),inset 0 0 0 1px rgba(201,133,67,.24),0 30px 40px -30px rgba(31,18,9,.8)}
.hs2-tafel .hs2-zz{width:clamp(70px,6.6vw,104px);height:auto;margin-bottom:clamp(18px,2vw,28px);fill:url(#rhgold)}
.hs2-tafel .hs2-ww{width:min(470px,88%);height:auto;color:#fbf5ea}
.hs2-tafel small{margin-top:16px;font-family:var(--mono);font-size:11px;letter-spacing:.3em;text-transform:uppercase;opacity:.9}
.hs2-marke p,.hs2-muster p{margin:0;font-size:1.04rem;line-height:1.66;color:rgba(42,26,14,.84)}
.hs2-marke dl{display:grid;grid-template-columns:auto 1fr;gap:10px 18px;margin:22px 0 0;padding-top:20px;border-top:1px solid var(--hl);font-size:1rem}
.hs2-marke dt{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--taupe);line-height:2.1}
.hs2-marke dd{margin:0}
.hs2-schriften{display:grid;grid-template-columns:repeat(3,1fr);border-left:1px solid var(--hl)}
.hs2-schrift{padding:0 clamp(16px,2.2vw,36px);border-right:1px solid var(--hl);display:flex;flex-direction:column}
.hs2-schrift>small{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--taupe)}
.hs2-aa{font-size:clamp(4rem,6.4vw,6.6rem);line-height:1;margin:clamp(14px,1.6vw,24px) 0 clamp(10px,1.2vw,16px);color:var(--tinte)}
.hs2-schrift b{font-family:var(--serif);font-weight:700;font-size:1.45rem;line-height:1.15}
.hs2-schrift span{margin-top:8px;font-size:1.02rem;color:rgba(42,26,14,.84)}
.hs2-schrift i{font-style:normal;margin-top:10px;padding-top:10px;border-top:1px solid var(--hl);font-size:.95rem;line-height:1.5;color:rgba(42,26,14,.64)}
.hs2-f-a{font-family:var(--serif);font-weight:700}.hs2-f-s{font-family:var(--sans)}.hs2-f-m{font-family:var(--mono)}
.hs2-schrift span.hs2-f-a{font-size:1.16rem}.hs2-schrift span.hs2-f-m{font-size:.84rem}
.hs2-band{display:flex;gap:clamp(10px,1.2vw,18px)}
.hs2-gr{flex:var(--n);min-width:0}
.hs2-gr__t{display:flex;border-radius:16px;overflow:hidden;box-shadow:inset 0 0 0 1px var(--hl)}
.hs2-gr>p{margin:12px 0 0 2px;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:rgba(42,26,14,.55)}
.hs2-chip{flex:1;min-width:0;display:flex;flex-direction:column;background:#fffdf8}
.hs2-chip i{display:block;height:clamp(84px,8vw,124px);background:var(--c)}
.hs2-chip b{padding:12px 12px 0;font-family:var(--serif);font-weight:700;font-size:1.02rem;line-height:1.1}
.hs2-chip small{padding:3px 12px 12px;font-family:var(--mono);font-size:10px;letter-spacing:.06em;color:rgba(42,26,14,.6)}
.hs2-chip+.hs2-chip{border-left:1px solid var(--hl)}
.hs2-her{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(12px,1.4vw,22px)}
.hs2-her figure{margin:0}
.hs2-her .hs2-bild{position:relative;border-radius:18px 18px 0 0;overflow:hidden;aspect-ratio:4/5}
.hs2-her .hs2-bild img{display:block;width:100%;height:100%;object-fit:cover}
.hs2-st{display:flex;height:20px;border-radius:0 0 10px 10px;overflow:hidden}
.hs2-st i{display:block;min-width:3px}
.hs2-her figcaption{margin-top:12px;font-family:var(--serif);font-weight:700;font-size:1.12rem;line-height:1.18}
.hs2-her figcaption small{display:block;margin-top:5px;font-family:var(--mono);font-weight:400;font-size:10px;letter-spacing:.06em;color:rgba(42,26,14,.6)}
.hs2-muster{display:grid;grid-template-columns:auto minmax(0,1fr) minmax(0,1fr);gap:clamp(22px,3vw,52px);align-items:center}
.hs2-butzen{width:clamp(150px,15vw,220px);aspect-ratio:1;border-radius:22px;display:grid;place-items:center;background:var(--blau) var(--muster) 50% 50%/var(--musterb) auto;box-shadow:inset 0 0 0 1px rgba(201,133,67,.24),0 24px 30px -24px rgba(31,18,9,.8)}
.hs2-butzen svg{width:38%;height:auto;margin:0;fill:url(#rhgold);color:#d9ae6c}
.hs2-kn{padding-left:clamp(22px,3vw,52px);border-left:1px solid var(--hl)}
.hs2-kn .kn-reihe{margin-top:18px;display:flex;flex-wrap:wrap;gap:12px}
@media (max-width:1000px){
  .hs2-marke{grid-template-columns:1fr}
  .hs2-her{grid-template-columns:repeat(2,1fr)}
  .hs2-band{flex-wrap:wrap}.hs2-gr{flex:1 1 100%}
  .hs2-muster{grid-template-columns:auto minmax(0,1fr)}.hs2-kn{grid-column:1/-1;padding-left:0;border-left:0;padding-top:22px;border-top:1px solid var(--hl)}
}
@media (max-width:640px){
  .hs2-schriften{grid-template-columns:1fr;border-left:0}
  .hs2-schrift{border-right:0;padding:0 0 22px;margin-bottom:22px;border-bottom:1px solid var(--hl)}.hs2-schrift:last-child{margin-bottom:0;padding-bottom:0;border-bottom:0}
  .hs2-gr__t{flex-wrap:wrap}.hs2-chip{flex:1 1 33%}.hs2-chip b{padding:10px 8px 0;font-size:.9rem}.hs2-chip small{padding:3px 8px 10px;font-size:9px}
  .hs2-muster{grid-template-columns:1fr}.hs2-butzen{width:132px}
  .hs2-etik{flex-direction:column;gap:4px}
}
/* ---------- Auftritte in der Tafel: ganze Bausteine bewegen sich, einzeln laufen nur die Töne und die kleinen Farbbalken ---------- */
.hs2.lebt .hs2-z{--fd:cubic-bezier(.28,1.42,.42,1);--ld:cubic-bezier(.2,1.12,.3,1)}
.hs2.lebt :is(.hs2-schrift,.hs2-chip,.hs2-her figure,.hs2-st i):nth-child(1){--k:0}
.hs2.lebt :is(.hs2-schrift,.hs2-chip,.hs2-her figure,.hs2-st i):nth-child(2){--k:1}
.hs2.lebt :is(.hs2-schrift,.hs2-chip,.hs2-her figure,.hs2-st i):nth-child(3){--k:2}
.hs2.lebt :is(.hs2-her figure,.hs2-st i):nth-child(4){--k:3}
.hs2.lebt .hs2-st i:nth-child(5){--k:4}
.hs2.lebt .hs2-z>.hs2-etik{opacity:0;transition:opacity 1.1s var(--e2)}
.hs2.lebt .hs2-tafel{opacity:0;translate:0 clamp(70px,8vw,120px);scale:.94;transform-origin:50% 100%;transition:opacity .9s var(--e2),translate 2s var(--fd),scale 2s var(--fd)}
.hs2.lebt .hs2-tafel .hs2-zz{opacity:0;scale:.6;rotate:-14deg;transition:opacity 1.1s var(--e2) .45s,scale 2.1s var(--fd) .45s,rotate 2.1s var(--fd) .45s}
.hs2.lebt .hs2-ww{opacity:0;translate:0 22px;transition:opacity 1.1s var(--e2) .9s,translate 1.5s var(--e1) .9s}
.hs2.lebt .hs2-tafel small{opacity:0;transition:opacity 1.2s ease 1.35s}
.hs2.lebt .hs2-marke>div:last-child{opacity:0;translate:0 34px;transition:opacity 1.2s var(--e2) .6s,translate 1.6s var(--e1) .6s}
.hs2.lebt .hs2-schrift{opacity:0;translate:0 clamp(50px,5.4vw,84px);transition:opacity 1s var(--e2),translate 1.9s var(--fd);transition-delay:calc(.1s + var(--k,0)*.14s)}
.hs2.lebt .hs2-gr{opacity:0;translate:0 clamp(50px,6vw,90px);scale:.95;transform-origin:50% 100%;transition:opacity .8s var(--e2),translate 1.9s var(--fd),scale 1.9s var(--fd);transition-delay:calc(var(--g,0)*.12s)}
.hs2.lebt .hs2-gr:nth-child(1){--g:0;--o:0}.hs2.lebt .hs2-gr:nth-child(2){--g:1;--o:3}.hs2.lebt .hs2-gr:nth-child(3){--g:2;--o:6}.hs2.lebt .hs2-gr:nth-child(4){--g:3;--o:9}
.hs2.lebt .hs2-chip i{transform:scaleX(0);transform-origin:0 50%;transition:transform 1.15s var(--e1);transition-delay:calc(.55s + (var(--o,0) + var(--k,0))*.09s)}
.hs2.lebt .hs2-her figure{opacity:0;translate:var(--fx,0) clamp(90px,10vw,150px);rotate:var(--fw,5deg);scale:.94;
  transition:opacity .7s var(--e2),translate 1.9s var(--ld),rotate 1.9s var(--ld),scale 1.9s var(--ld);transition-delay:calc(var(--k,0)*.15s)}
.hs2.lebt .hs2-her figure:nth-child(1){--fx:-44px;--fw:-7deg;--f:0}.hs2.lebt .hs2-her figure:nth-child(2){--fx:-16px;--fw:-3deg;--f:1}
.hs2.lebt .hs2-her figure:nth-child(3){--fx:16px;--fw:3deg;--f:2}.hs2.lebt .hs2-her figure:nth-child(4){--fx:44px;--fw:7deg;--f:3}
.hs2.lebt .hs2-bild img{scale:1.14;transition:scale 2.4s var(--e1);transition-delay:calc(var(--k,0)*.15s)}
.hs2.lebt .hs2-st i{transform:scaleX(0);transform-origin:0 50%;transition:transform .9s var(--ld);transition-delay:calc(1.2s + var(--f,0)*.15s + var(--k,0)*.11s)}
.hs2.lebt .hs2-butzen{opacity:0;translate:0 60px;rotate:-6deg;scale:.9;transition:opacity .9s var(--e2),translate 1.9s var(--fd),rotate 1.9s var(--fd),scale 1.9s var(--fd)}
.hs2.lebt .hs2-muster>div:not(.hs2-butzen){opacity:0;translate:0 30px;transition:opacity 1.2s var(--e2) .25s,translate 1.6s var(--e1) .25s}
.hs2.lebt .hs2-muster>.hs2-kn{transition-delay:.45s}
.hs2.lebt .hs2-z.da :is(.hs2-etik,.hs2-tafel,.hs2-zz,.hs2-ww,.hs2-marke>div:last-child,.hs2-schrift,.hs2-gr,.hs2-her figure,.hs2-butzen,.hs2-muster>div){opacity:1;translate:none;rotate:none;scale:none}
.hs2.lebt .hs2-z.da :is(.hs2-chip i,.hs2-st i){transform:none}
.hs2.lebt .hs2-z.da .hs2-bild img{scale:none}
.hs2.lebt .hs2-z.da .hs2-tafel small{opacity:.9}
'''

JS = '''<script id="hs-auftritt">
/* Handschrift: jede Zeile der Tafel startet ihren Auftritt, sobald ein Drittel von ihr im Bild steht (nur Klassen setzen) */
(function(){
  var s=document.getElementById('handschrift');
  if(!s||!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  s.classList.add('lebt');
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);e.target.classList.add('da');}});},{rootMargin:'0px 0px -6% 0px',threshold:.3});
  [].forEach.call(s.querySelectorAll('.hs2-z'),function(z){io.observe(z);});
})();
</script>
'''


def anwenden(pfad):
    """Hängt das Start-Skript an die gebaute Seite. Mehrfach anwendbar."""
    if not os.path.exists(pfad):
        return False
    t = open(pfad, encoding='utf-8').read()
    if 'id="handschrift"' not in t:
        return False
    neu = re.sub(r'<script id="hs-auftritt">.*?</script>\n?', '', t, flags=re.S)
    neu = re.sub(r'(<script src="werkbank\.js)', lambda m: JS + m.group(1), neu, count=1)
    if neu != t:
        open(pfad, 'w', encoding='utf-8').write(neu)
    return neu != t
