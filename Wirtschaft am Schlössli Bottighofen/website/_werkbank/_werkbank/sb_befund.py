#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli, Kapitel I «Was wir gefunden haben» (Nachtbau 3.11.2026; Bauart sb_befund.py des Culinarium, Inhalt wie im alten Schlössli-Stand).

Inhalt nur aus der Potentialanalyse der Station 04 (_kette/04-analyst/potential.json, bestätigt 19.10.2026), bei jedem Bau frisch gelesen: die vier ersten
der dreizehn Befunde (Robert 20.10.2026: in der Werkbank nur die vier stärksten, Reihenfolge der Analyse), im Wortlaut der Analyse, mit ihren Aufnahmen
(potential/belege/*-ganz.webp im Handy, *-nah.webp mit dem roten Kreis der Analyse als Ausschnitt daneben): die Belegbilder zeigen genau die Stelle,
von der der Befund spricht. Eine Bühne, ein Befund im Blick: Pfeile, Ziffern, Wischen, Tasten. Kein Preis, kein Vorwurf.
Der Knopf führt zum ganzen Befund als eigene Seite unter befund/ (kopiere_analyse): was gut ist, die vier von vorn, die übrigen neun, was möglich ist."""
import html, json, os, re, shutil
from PIL import Image, ImageDraw

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PROJ = os.path.dirname(os.path.dirname(ROOT))
AN = os.path.join(PROJ, '_kette', '04-analyst')
P = json.load(open(os.path.join(AN, 'potential.json'), encoding='utf-8'))
G = os.path.join(W, 'geraete')
LI = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>'
RE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>'
ZAHL = 4   # Robert 20.10.2026, gilt für alle Häuser: in der Werkbank nur die vier stärksten Funde, alle übrigen stehen im ganzen Befund
ALLE = len(P['befunde'])


def _sinn(b):
    teile = re.split(r'\s*(Gäste:|Haus:|Was wir tun würden:)\s*', b['nutzen'])
    return {teile[i].rstrip(':'): teile[i + 1].strip() for i in range(1, len(teile) - 1, 2)}


def befunde(alle=False):
    aus = []
    for b in P['befunde']:
        m = re.match(r'(potential/belege/[a-z0-9-]+)-ganz\.webp', b['beleg'])
        ganz = os.path.join(AN, m.group(1) + '-ganz.webp') if m else None
        nah = os.path.join(AN, m.group(1) + '-nah.webp') if m else None
        if not m:   # Befund mit Bild statt Aufnahme (Postkarte aus der Gemeindeschrift)
            q = os.path.join(AN, 'potential', b['beleg'].split(',')[0].strip())
            nah = q if os.path.exists(q) else None
        sinn = _sinn(b)
        if len(aus) == ZAHL and not alle:
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


def _ist_handy(p):
    """Aufnahmen vom Handy kommen ins Handy, Aufnahmen vom Rechner und PDFs stehen gerade als Ausschnitt."""
    return '-handy' in os.path.basename(p)


def bilder(webp):
    for b in befunde():
        if b['ganz'] and _ist_handy(b['ganz']):
            webp(_handy(b['ganz']), f'bf-h-{b["nr"]}', 700, 84)
        if b['nah']:
            webp(Image.open(b['nah']).convert('RGB'), f'bf-n-{b["nr"]}', 1100, 84)


STARK = [  # «Was gut ist» aus der Potentialanalyse (potential/index.html, Abschnitt «stimmt»), wörtlich
    ('Ihre Fotos.', 'Die Terrasse, die blauen Stühle vor See und Alpen, die Teller auf Blau: eigene, starke Bilder aus zwei Serien (August 2025, Mai 2026).'),
    ('Aktuelle Karten.', 'Speisekarte vom 30. September, Weinkarte vom 14. Oktober, Lunch-Menü vom 18. Oktober. Man sieht, dass hier jemand pflegt.'),
    ('Klare Zeiten.', 'Öffnungs- und Küchenzeiten, Ruhetage und Ferien bis Februar 2027 stehen auf der Kontaktseite.'),
    ('Für Google vorbereitet.', 'Jede Seite hat Titel und Beschreibung, am Telefon läuft nichts seitlich über.'),
]


def _chancen():
    aus = []
    for c in P.get('chancen', []):
        t, _, s = c['was'].partition(': ')
        aus.append((t.strip() + '.', s.strip() or t.strip()))
    return aus


def kopiere_analyse():
    """Der ganze Befund als eigene Seite neben der Werkbank (befund/index.html), für das Haus geschrieben: was gut ist, die vier Befunde von vorn mit Bild,
    die übrigen neun und was möglich ist. Quelle: Potentialanalyse der Station 04, nichts dazuerfunden; die interne Seite der Kette wird nicht kopiert."""
    import kern as K
    z = os.path.join(ROOT, 'befund'); os.makedirs(os.path.join(z, 'img'), exist_ok=True)
    for f in os.listdir(os.path.join(z, 'img')):
        os.remove(os.path.join(z, 'img', f))
    bilder_ = {}
    for b in befunde():
        for art, q in (('h', b['ganz'] if b['ganz'] and _ist_handy(b['ganz']) else None), ('n', b['nah'])):
            if not q:
                continue
            im = _handy(q) if art == 'h' else Image.open(q).convert('RGB')
            im.thumbnail((900, 900)); n = f'{art}-{b["nr"]}.webp'
            (im if im.mode == 'RGBA' else im.convert('RGB')).save(os.path.join(z, 'img', n), 'WEBP', quality=84); bilder_.setdefault(b['nr'], []).append((n, im.size, art))
    stark = ''.join(f'<li data-a="auf" style="--i:{i % 4}"><b>{e(t)}</b><span>{e(s)}</span></li>' for i, (t, s) in enumerate(STARK))
    funde = ''
    for b in befunde():
        bi = ''.join(f'<img src="img/{n}" width="{w}" height="{h}" alt="Aufnahme Ihrer heutigen Seite zum Befund {b["nr"]}" decoding="async" class="bfs-{art}">' for n, (w, h), art in bilder_.get(b['nr'], []))
        funde += (f'<article class="bfs-f"><div class="bfs-b" data-a="heben">{bi}</div><div data-a="auf"><p class="bfs-nr">{b["nr"]}</p><h2>{e(b["was"])}</h2><p class="bfs-wo"><b>Wo</b>{e(b["wo"])}</p>'
                  f'<dl><dt>Für Ihre Gäste</dt><dd>{e(b["gaeste"])}</dd><dt>Für Ihr Haus</dt><dd>{e(b["haus"])}</dd><dt>Was wir tun würden</dt><dd>{e(b["tun"])}</dd></dl></div></article>')
    weitere = ''.join(f'<li data-a="auf" style="--i:{i % 3}"><b>{e(b["nr"])} · {e(b["was"])}</b><span>{e(b["tun"] or b["voll"])}</span></li>' for i, b in enumerate(befunde(alle=True)[ZAHL:]))
    moeglich = ''.join(f'<li data-a="auf" style="--i:{i % 3}"><b>{e(t)}</b><span>{e(s)}</span></li>' for i, (t, s) in enumerate(_chancen()))
    haupt = f'''<section class="fl fl--nacht tapete-leicht bfs"><div class="in">
  <p class="kap kap--z">Der Befund</p>
  <h1 class="t1 zt"><span class="z"><span>Wie Ihre Seite</span></span><span class="z"><span><em>heute dasteht.</em></span></span></h1>
  <p class="bfs-lauf" data-a="worte">Angesehen am {e(P["stand"])}, am Handy und am Rechner: schloessli-bottighofen.ch, dazu Google, die Führer und Ihre Karten.
  Hier steht zuerst, was schon gut ist, dann, wo ein Gast auf dem Weg an Ihren Tisch stockt, und am Schluss, was Ihr Haus schon hat und die Seite noch nicht erzählt.</p>
</div></section>
<section class="fl fl--papier tapete-hell bfs"><div class="in"><h2 class="bfs-h" data-a="auf">Was schon gut ist</h2><ul class="bfs-l">{stark}</ul></div></section>
<section class="fl fl--nacht tapete-leicht bfs"><div class="in"><h2 class="bfs-h" data-a="auf">Vier Punkte von vorn</h2>{funde}</div></section>
<section class="fl fl--papier tapete-hell bfs"><div class="in"><h2 class="bfs-h" data-a="auf">Was sonst noch auffällt</h2><ul class="bfs-l">{weitere}</ul></div></section>
<section class="fl fl--creme tapete-hell bfs"><div class="in"><h2 class="bfs-h" data-a="auf">Was möglich ist</h2><ul class="bfs-l">{moeglich}</ul></div></section>'''
    css = ('<style>.bfs .in{max-width:1180px}.bfs-lauf{max-width:62ch;margin:18px auto 0;text-align:center;font-size:clamp(1.05rem,1.3vw,1.25rem);line-height:1.6;color:rgba(233,238,243,.88)}'
           '.bfs-h{font-family:var(--serif);font-weight:400;text-transform:uppercase;letter-spacing:.12em;font-size:clamp(1.5rem,2.6vw,2.4rem);margin:0 0 clamp(24px,3vw,44px);text-wrap:balance}'
           '.bfs-l{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:clamp(18px,2vw,30px)}'
           '.bfs-l li{display:flex;flex-direction:column;gap:8px;padding-top:16px;border-top:1px solid rgba(4,16,35,.16)}.bfs-l b{font-family:var(--sans);font-weight:500;font-size:1.18rem;line-height:1.35}.bfs-l span{line-height:1.6}'
           '.bfs-f{display:grid;gap:clamp(24px,4vw,64px);align-items:center;padding:clamp(28px,4vw,56px) 0;border-top:1px solid rgba(162,182,207,.22)}'
           '@media(min-width:900px){.bfs-f{grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)}}'
           '.bfs-b{display:flex;gap:16px;align-items:center;justify-content:center}.bfs-b img{max-width:100%;height:auto;min-width:0}'
           '.bfs-b img.bfs-h{width:min(260px,46%)}.bfs-b img.bfs-n{width:min(480px,100%);border-radius:12px}'
           '.bfs-b:has(img+img) img.bfs-h{width:32%;flex:none}.bfs-b:has(img+img) img.bfs-n{width:auto;flex:1 1 0}'
           '.bfs-nr{margin:0;font-family:var(--serif);font-size:clamp(3rem,6vw,5.6rem);line-height:.9;color:var(--gold)}.bfs-f h2{font-family:var(--sans);font-weight:500;font-size:clamp(1.3rem,2vw,1.9rem);line-height:1.3;margin:12px 0 0;text-wrap:balance}'
           '.bfs-wo{display:flex;gap:14px;margin:16px 0 0;line-height:1.55;color:rgba(233,238,243,.8)}.bfs-wo b{font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);padding-top:3px}'
           '.bfs-f dl{margin:18px 0 0}.bfs-f dt{margin-top:14px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}.bfs-f dd{margin:6px 0 0;line-height:1.6;color:rgba(233,238,243,.92)}</style>')
    s = K.rahmen('Der Befund', f'Wie die Seite der Wirtschaft am Schlössli heute dasteht, angesehen am {P["stand"]}.', 'Befund', haupt,
                 f'Ein Befund von Robert Reff, Tasty Studios, nach dem Stand vom {P["stand"]}. Aufnahmen Ihrer heutigen Seite nur zur Anschauung.')
    s = s.replace('</head>', css + '</head>', 1)
    open(os.path.join(z, 'index.html'), 'w', encoding='utf-8').write(s)


def abschnitt(k, kopfk):
    M, bild = k['m'], k['bild']
    B = befunde()
    platten = ''
    for i, b in enumerate(B):
        handy = (f'<div class="sbf-handy">{bild("bf-h-" + b["nr"], "Aufnahme Ihrer heutigen Seite zum Befund " + b["nr"], lazy=i > 1)}</div>' if 'bf-h-' + b['nr'] in M else '')
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
    {kopfk('k1', ['Vier Stellen,', 'an denen Gäste stocken.'], f'Die vier, die am meisten ausmachen, jede mit einer Aufnahme Ihrer heutigen Seite als Beleg. Alle {ALLE} Funde stehen im ganzen Befund.')}
    <div class="sbf-b" tabindex="0" aria-roledescription="Karussell" aria-label="Die Befunde">
      <div class="sbf-platten">{platten}</div>
      <div class="sbf-fuss"><button type="button" class="wf__pf" data-f="-1" aria-label="Voriger Befund">{LI}</button><div class="sbf-ziffern">{ziffern}</div><button type="button" class="wf__pf" data-f="1" aria-label="Nächster Befund">{RE}</button></div>
    </div>
    <div class="kn-reihe" data-a="auf" style="justify-content:center;margin-top:clamp(28px,3vw,48px)">{k['kn']('Den ganzen Befund ansehen', '../befund/index.html')}</div>
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
