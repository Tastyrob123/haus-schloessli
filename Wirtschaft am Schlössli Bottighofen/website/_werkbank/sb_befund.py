#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli, Kapitel I «Was wir gefunden haben» (Station 11, 19.10.2026).

Inhalt nur aus der Potentialanalyse der Station 04 (_kette/04-analyst/potential.json, bestätigt), bei jedem Bau frisch gelesen: die dreizehn Befunde
im Wortlaut der Analyse, ihre Aufnahmen (potential/belege/*-ganz.webp im 3D-Handy, *-nah.webp mit dem roten Kreis der Analyse als Ausschnitt daneben).
Eine Bühne, ein Befund im Blick: Pfeile, Ziffern, Wischen, Tasten. Das Schlimmste kommt zuerst (Reihenfolge der Analyse). Kein Preis.
Die ganze Analyse liegt als Kopie unter website/potenzialanalyse/ (wb_kapitel kopiert sie), der Knopf führt dorthin."""
import html, json, os, re, shutil
from PIL import Image, ImageDraw

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
AN = os.path.join(os.path.dirname(ROOT), '_kette', '04-analyst')
P = json.load(open(os.path.join(AN, 'potential.json'), encoding='utf-8'))
G = os.path.join(W, 'geraete')
ZAHL = 4   # Robert 20.10.2026, gilt für alle Häuser: in der Werkbank nur die vier stärksten Funde, alle übrigen stehen in der ganzen Analyse
LI = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>'
RE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>'


def befunde():
    aus = []
    for b in P['befunde']:
        m = re.match(r'(potential/belege/[a-z0-9-]+)-ganz\.webp', b['beleg'])
        ganz = os.path.join(AN, m.group(1) + '-ganz.webp') if m else None
        nah = os.path.join(AN, m.group(1) + '-nah.webp') if m else None
        if not m:   # Befund 08: Bild statt Aufnahme (Postkarte aus der Sammlung)
            q = os.path.join(AN, 'potential', b['beleg'].split(',')[0].strip())
            nah = q if os.path.exists(q) else None
        teile = re.split(r'\s*(Gäste:|Haus:|Was wir tun würden:)\s*', b['nutzen'])
        sinn = {teile[i].rstrip(':'): teile[i + 1].strip() for i in range(1, len(teile) - 1, 2)}
        if len(aus) == ZAHL:
            break
        aus.append(dict(nr=b['nr'], was=b['was'], wo=b['wo'], gaeste=sinn.get('Gäste', ''), haus=sinn.get('Haus', ''), tun=sinn.get('Was wir tun würden', ''),
                        voll=b['nutzen'] if not sinn else '', ganz=ganz if ganz and os.path.exists(ganz) else None, nah=nah if nah and os.path.exists(nah) else None))
    return aus


def _handy(schirm):
    L = json.load(open(os.path.join(G, 'handy.json')))
    g = Image.open(os.path.join(G, 'handy-geraet.png')).convert('RGBA')
    x, y, b, h = (round(v * (g.width if i % 2 == 0 else g.height)) for i, v in enumerate(L['schirm']))
    s = Image.open(schirm).convert('RGB')
    f = max(b / s.width, h / s.height)
    s = s.resize((max(b, round(s.width * f)), max(h, round(s.height * f))), Image.LANCZOS).crop((0, 0, b, h))
    m = Image.new('L', (b, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, b - 1, h - 1], radius=round(b * .1), fill=255)
    grund = Image.new('RGBA', g.size, (0, 0, 0, 0)); grund.paste(s, (x, y), m); grund.alpha_composite(g)
    gx, gy, gb, gh = L['gehaeuse']
    return grund.crop((round(gx * g.width) - 6, round(gy * g.height) - 6, round((gx + gb) * g.width) + 6, round((gy + gh) * g.height) + 6))


def bilder(webp):
    for b in befunde():
        if b['ganz']:
            webp(_handy(b['ganz']), f'bf-h-{b["nr"]}', 700, 84)
        if b['nah']:
            webp(b['nah'], f'bf-n-{b["nr"]}', 1100, 84)


def kopiere_analyse():
    """Die Analyse als Kopie neben die Website (Beigabe), damit der Knopf auf jedem Server führt. Quelle bleibt Station 04."""
    q, z = os.path.join(AN, 'potential'), os.path.join(ROOT, 'potenzialanalyse')
    if os.path.isdir(z):
        shutil.rmtree(z)
    shutil.copytree(q, z)


def abschnitt(k, kopfk):
    M, bild = k['m'], k['bild']
    B = befunde()
    platten = ''
    for i, b in enumerate(B):
        handy = (f'<div class="sbf-handy">{bild("bf-h-" + b["nr"], "Aufnahme der heutigen Seite zum Befund " + b["nr"], lazy=i > 1)}</div>' if 'bf-h-' + b['nr'] in M else '')
        nah = (f'<figure class="sbf-nah">{bild("bf-n-" + b["nr"], "Ausschnitt mit der Stelle", lazy=i > 1)}</figure>' if 'bf-n-' + b['nr'] in M else '')
        sinn = ''.join(f'<div class="sbf-sinn__z"><dt>{e(t)}</dt><dd>{e(x)}</dd></div>' for t, x in (('Für Ihre Gäste', b['gaeste']), ('Für Ihr Haus', b['haus']), ('Was wir tun würden', b['tun'])) if x) \
            or f'<div class="sbf-sinn__z"><dd>{e(b["voll"])}</dd></div>'
        platten += (f'<article class="sbf-p{" an" if i == 0 else ""}" data-i="{i}" aria-label="Befund {b["nr"]}">'
                    f'<div class="sbf-bild">{handy}{nah}</div>'
                    f'<div class="sbf-text"><p class="sbf-nr">{b["nr"]}</p><h3>{e(b["was"])}</h3><p class="sbf-wo"><b>Wo</b>{e(b["wo"])}</p><dl class="sbf-sinn">{sinn}</dl></div></article>')
    ziffern = ''.join(f'<button type="button" class="sbf-z" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}">{b["nr"]}</button>' for i, b in enumerate(B))
    return f'''
<section class="fl fl--nacht tapete-leicht blatt sbf" id="k1">
  <div class="in">
    {kopfk('k1', ['Vier Stellen,', 'an denen Gäste stocken.'], f'Die vier, die am meisten kosten, jede mit einer Aufnahme Ihrer heutigen Seite. Alle {len(P["befunde"])} Funde stehen in der ganzen Analyse.')}
    <div class="sbf-b" tabindex="0" aria-roledescription="Karussell" aria-label="Die Befunde">
      <div class="sbf-platten">{platten}</div>
      <div class="sbf-fuss"><button type="button" class="wf__pf" data-f="-1" aria-label="Voriger Befund">{LI}</button><div class="sbf-ziffern">{ziffern}</div><button type="button" class="wf__pf" data-f="1" aria-label="Nächster Befund">{RE}</button></div>
    </div>
    <div class="kn-reihe" data-a="auf" style="justify-content:center;margin-top:clamp(28px,3vw,48px)">{k['kn']('Die ganze Analyse ansehen', '../potenzialanalyse/index.html')}</div>
  </div>
</section>
<script>(function(){{var s=document.querySelector('.sbf-b');if(!s)return;var P=[].slice.call(s.querySelectorAll('.sbf-p')),Z=[].slice.call(s.querySelectorAll('.sbf-z')),ist=0,n=P.length;
function zeig(k){{ist=(k%n+n)%n;P.forEach(function(p,i){{p.classList.toggle('an',i===ist);if(i===ist||i===(ist+1)%n)[].forEach.call(p.querySelectorAll('img[loading=lazy]'),function(x){{x.loading='eager'}})}});Z.forEach(function(z,i){{z.setAttribute('aria-pressed',i===ist?'true':'false')}})}}
[].forEach.call(s.querySelectorAll('[data-f]'),function(b){{b.addEventListener('click',function(){{zeig(ist+(+b.getAttribute('data-f')))}})}});
Z.forEach(function(z,i){{z.addEventListener('click',function(){{zeig(i)}})}});
s.addEventListener('keydown',function(ev){{if(ev.key==='ArrowRight')zeig(ist+1);else if(ev.key==='ArrowLeft')zeig(ist-1)}});
var x0=null;s.addEventListener('touchstart',function(ev){{x0=ev.touches[0].clientX}},{{passive:true}});s.addEventListener('touchend',function(ev){{if(x0===null)return;var d=ev.changedTouches[0].clientX-x0;x0=null;if(Math.abs(d)>50)zeig(ist+(d<0?1:-1))}},{{passive:true}})}})();</script>'''


CSS = '''
/* ---------- Kapitel I «Was wir gefunden haben» (sb_befund.py, 19.10.2026): ein Befund im Blick, Handy mit der heutigen Seite, daneben der Ausschnitt ---------- */
.sbf-b{outline:0;margin-top:clamp(16px,2vw,32px)}
.sbf-platten{display:grid}
.sbf-p{grid-area:1/1;display:grid;gap:clamp(26px,4vw,72px);align-items:center;opacity:0;visibility:hidden;transition:opacity .25s linear,visibility 0s .25s}
.sbf-p.an{opacity:1;visibility:visible;transition:opacity .45s linear .1s,visibility 0s}
@media(min-width:960px){.sbf-p{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.sbf-bild{position:relative;display:flex;align-items:center;justify-content:center;min-height:clamp(320px,40vw,620px)}
.sbf-handy{width:clamp(200px,20vw,300px);transform:rotate(-4deg);filter:drop-shadow(0 34px 34px rgba(0,0,0,.55))}
.sbf-handy img{display:block;width:100%;height:auto}
.sbf-nah{position:absolute;right:0;bottom:4%;width:clamp(200px,24vw,360px);margin:0;border-radius:16px;overflow:hidden;transform:rotate(3deg);
  box-shadow:0 0 0 6px var(--weiss),0 0 0 7px rgba(162,182,207,.6),0 34px 44px -24px rgba(0,0,0,.85)}
.sbf-handy+.sbf-nah{right:2%}
.sbf-bild>.sbf-nah:only-child{position:static;width:min(100%,520px);transform:rotate(-2deg)}
.sbf-nah img{display:block;width:100%;height:auto}
.sbf-p.an .sbf-handy{animation:sbfHoch 1.1s cubic-bezier(.16,1,.3,1) both}.sbf-p.an .sbf-nah{animation:sbfHoch 1.3s cubic-bezier(.16,1,.3,1) .12s both}
@keyframes sbfHoch{from{translate:0 60px}to{translate:0 0}}
.sbf-nr{margin:0;font-family:var(--serif);font-size:clamp(3.6rem,7vw,7rem);line-height:.9;letter-spacing:.06em;color:var(--gold)}
.sbf-text h3{margin:clamp(12px,1.4vw,20px) 0 0;font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,2.1vw,2.2rem);line-height:1.25;color:var(--weiss);text-wrap:balance}
.sbf-wo{display:flex;gap:14px;margin:clamp(14px,1.6vw,22px) 0 0;font-size:clamp(.96rem,1.04vw,1.06rem);line-height:1.55;color:rgba(243,246,249,.78)}
.sbf-wo b{flex:none;font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);padding-top:3px}
.sbf-sinn{margin:clamp(18px,2vw,28px) 0 0;border-top:1px solid rgba(162,182,207,.3)}
.sbf-sinn__z{padding:12px 0;border-bottom:1px solid rgba(162,182,207,.22)}
.sbf-sinn dt{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.sbf-sinn dd{margin:6px 0 0;font-size:clamp(1rem,1.08vw,1.1rem);line-height:1.6;color:rgba(243,246,249,.9)}
.sbf-fuss{display:flex;align-items:center;justify-content:center;gap:clamp(12px,2vw,28px);margin-top:clamp(26px,3vw,44px)}
.sbf-ziffern{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;max-width:640px}
.sbf-z{min-width:40px;padding:7px 9px;border-radius:999px;font-family:var(--mono);font-size:.78rem;color:rgba(243,246,249,.62);box-shadow:inset 0 0 0 1px rgba(162,182,207,.3);transition:color .4s,background .4s}
.sbf-z[aria-pressed="true"]{color:var(--tinte);background:var(--gold)}
@media(max-width:700px){.sbf-bild{min-height:0;padding:10px 0 30px}.sbf-handy{width:56vw}.sbf-nah{width:58vw;bottom:0}.sbf-ziffern{display:none}}
@media(prefers-reduced-motion:reduce){.sbf-p,.sbf-p.an .sbf-handy,.sbf-p.an .sbf-nah{transition:none;animation:none}}
'''
