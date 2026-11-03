"""Wirtschaft am Schlössli · Station 05 Markenbauer · erster Durchgang, ohne Blender (Robert 18./19.10.2026).
Baut aus den gemessenen Werten (_bau/messung.json, _bau/messen.py): marke.json, farben.svg, Tapeten, markenbuch.html, probe.html,
logo-richtig-falsch/index.html. Jede Farbe mit Fundstelle; abgeleitete Töne sind gerechnet und so gekennzeichnet.
Machart wie das Markenbuch des Schwesterhauses (Taverne zum Schäfli, 19.10.2026), Farben, Schrift, Zeichen und Tapete eigen."""
import os, re, json, html

H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(H, 'marke')
E = html.escape
MS = json.load(open(os.path.join(H, '_bau', 'messung.json')))
SH = 'Ausgewertet ist der häufigste Ton der Fläche'


def m(n): return MS[n]['hex']


def fs(n, was):
    d = MS[n]
    b = d['box']
    return '%s · %s, Ausschnitt x %d–%d, y %d–%d' % (was, d['datei'], b[0], b[2], b[1], b[3])


# ---------------------------------------------------------------- Farben, gemessen
FARBEN = [
    dict(gruppe='hafen', name='Stuhlblau', hex=m('Stuhlblau'), rolle='flaeche-dunkel', belegt='Foto', foto='k-stuhl',
         fundstelle=fs('Stuhlblau', 'Geflecht der Terrassenstühle in der Sonne'), auch='Median ' + MS['Stuhlblau']['median'] + '; dieselben Stühle auf fast jedem Terrassenfoto der Seite'),
    dict(gruppe='hafen', name='Seespiegel', hex=m('Seespiegel'), rolle='flaeche-hell', belegt='Foto', foto='k-see',
         fundstelle=fs('Seespiegel', 'Wasser vor den Alpen am Mittag (Startbild der Seite)'), auch='Median ' + MS['Seespiegel']['median']),
    dict(gruppe='hafen', name='Seehimmel', hex=m('Seehimmel'), rolle='akzent', belegt='Foto', foto='k-himmel',
         fundstelle=fs('Seehimmel', 'Himmel über dem See, ebd.'), auch='Median ' + MS['Seehimmel']['median']),
    dict(gruppe='hafen', name='Ufersand', hex=m('Ufersand'), rolle='flaeche-hell', belegt='Foto', foto='k-ufer',
         fundstelle=fs('Ufersand', 'Sand und Steine am Ufer in der Sonne, ebd.'), auch='Median ' + MS['Ufersand']['median'] + ' mit Schatten und nassem Sand'),
    dict(gruppe='hafen', name='Kies', hex=m('Kies'), rolle='schrift', belegt='Foto', foto='k-kies',
         fundstelle=fs('Kies', 'Kies unter den Tischen, Licht durch die Platanen'), auch='Median ' + MS['Kies']['median']),
    dict(gruppe='hafen', name='Platanenlaub', hex=m('Platanenlaub'), rolle='akzent', belegt='Foto', foto='k-laub',
         fundstelle=fs('Platanenlaub', 'Laub der Platanen über der Terrasse, nur die hellen Blätter'), auch='Median ' + MS['Platanenlaub']['median'] + ' · nicht in den Farbwelten: Grün ist die Welt B des Schäfli'),
    dict(gruppe='hafen', name='Schirmrot', hex=m('Schirmrot'), rolle='akzent', belegt='Foto', foto='k-schirm',
         fundstelle=fs('Schirmrot', 'Sonnenschirme der Terrasse, Stoff im Gegenlicht'), auch='Median ' + MS['Schirmrot']['median']),
    dict(gruppe='hafen', name='Tellerblau', hex=m('Tellerblau'), rolle='akzent', belegt='Foto', foto='k-teller',
         fundstelle=fs('Tellerblau', 'Blauer Platzteller unter dem Gericht «Anguria»'), auch='Median ' + MS['Tellerblau']['median']),
    dict(gruppe='abend', name='Abendrot', hex=MS['Abendrot']['median'], rolle='akzent', belegt='Foto', foto='k-abendrot',
         fundstelle=fs('Abendrot', 'Himmel über dem Ufer nach Sonnenuntergang'), auch='Hier der Median: der Streifen ist ein Verlauf, der häufigste Ton ' + m('Abendrot') + ' ist nur sein hellster Teil'),
    dict(gruppe='abend', name='Blaue Stunde', hex=m('Blaue Stunde'), rolle='flaeche-dunkel', belegt='Foto', foto='k-blau',
         fundstelle=fs('Blaue Stunde', 'Himmel über dem See am Abend, ebd.'), auch='Median ' + MS['Blaue Stunde']['median']),
    dict(gruppe='abend', name='Lichterkette', hex=m('Lichterkette'), rolle='akzent', belegt='Foto', foto='k-licht',
         fundstelle=fs('Lichterkette', 'Lichter in der Platane über der Terrasse, ebd.'), auch='Median ' + MS['Lichterkette']['median']),
    dict(gruppe='fliese', name='Fliese Anthrazit', hex=m('Fliese Anthrazit'), rolle='flaeche-dunkel', belegt='Foto', foto='k-anthrazit',
         fundstelle=fs('Fliese Anthrazit', 'Zementfliesen an der Bar, Grund der Fliesen'), auch='Median ' + MS['Fliese Anthrazit']['median']),
    dict(gruppe='fliese', name='Fliese Kalk', hex=m('Fliese Kalk'), rolle='flaeche-hell', belegt='Foto', foto='k-kalk',
         fundstelle=fs('Fliese Kalk', 'helle Felder der Fliesen, ebd.'), auch='Median ' + MS['Fliese Kalk']['median']),
    dict(gruppe='fliese', name='Fliese Terrakotta', hex=m('Fliese Terrakotta'), rolle='akzent', belegt='Foto', foto='k-terrakotta',
         fundstelle=fs('Fliese Terrakotta', 'Ornament der zweiten Fliese, ebd.'), auch='Median ' + MS['Fliese Terrakotta']['median']),
    dict(gruppe='fliese', name='Fliese Graublau', hex=m('Fliese Graublau'), rolle='akzent', belegt='Foto', foto='k-graublau',
         fundstelle=fs('Fliese Graublau', 'Grund der vierten Fliese, ebd.'), auch='Median ' + MS['Fliese Graublau']['median']),
    dict(gruppe='logo', name='Schwarz des Logos', hex='#000000', rolle='schrift', belegt='Logo', foto=None, zeige='logo/logo-transparent-1563.png',
         fundstelle='alle deckenden Pixel des Logos · _quelle/extern/logo/schloessli-logo-transparent.png (1563 × 1563, Seite des Schäfli)', auch='Das Logo ist einfarbig. Auf dem Teilen-Bild der Seite ebenfalls Schwarz'),
    dict(gruppe='heute', name='Mint der heutigen Seite', hex='#D8FFFC', rolle='flaeche-hell', belegt='heutige Seite', foto=None, zeige='logo/logo-auf-mint-teilen-bild.jpeg',
         fundstelle='Grund der Seite, gemessen vom Späher · _kette/02-spaeher/befund.md', auch='Im Teilen-Bild des Logos ' + m('Mint der heutigen Seite') + ' (JPEG) · nicht als Hausfarbe belegt'),
    dict(gruppe='heute', name='Nachtblau der heutigen Seite', hex='#213C4F', rolle='flaeche-dunkel', belegt='heutige Seite', foto='heute-knoepfe',
         fundstelle='Knöpfe der heutigen Seite · _kette/02-spaeher/befund.md; Bild: Aufnahme des Spähers _qa/spaeher/start-rechner-voll.jpg, 18.10.2026', auch='nicht als Hausfarbe belegt'),
    dict(gruppe='heute', name='Schrift der heutigen Seite', hex='#0F3538', rolle='schrift', belegt='heutige Seite', foto='heute-text',
         fundstelle='Lauftext der heutigen Seite · _kette/02-spaeher/befund.md; Bild: ebd.', auch='nicht als Hausfarbe belegt'),
]
F = {f['name']: f['hex'] for f in FARBEN}


def rgb(h): return [int(h[i:i + 2], 16) for i in (1, 3, 5)]
def hx(c): return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)
def mix(a, b, t): return hx([x + (y - x) * t for x, y in zip(rgb(a), rgb(b))])
def toene(h): return [mix(h, '#000000', .55), mix(h, '#000000', .3), h, mix(h, '#FFFFFF', .45), mix(h, '#FFFFFF', .82)]


WELTEN = {
    'a': dict(name='Stuhl und See', kurz='Stuhlblau',
              satz='Das Blau der Terrassenstühle als dunkle Fläche, der Himmel über dem See aufgehellt als helle und als Linie und Zeichen. Schirmrot nur als Punkt.',
              nacht=mix(F['Stuhlblau'], '#000000', .64), tief=mix(F['Stuhlblau'], '#000000', .44), mittel=F['Stuhlblau'],
              kalk=mix(F['Seehimmel'], '#FFFFFF', .74), kalk2=mix(F['Seehimmel'], '#FFFFFF', .5),
              ak=F['Seehimmel'], ak_h=mix(F['Seehimmel'], '#FFFFFF', .38), ak_t=mix(F['Stuhlblau'], '#000000', .12),
              tinte=mix(F['Stuhlblau'], '#000000', .74), signal=F['Schirmrot'], titel_h=mix(F['Stuhlblau'], '#000000', .4),
              ak_text='#0B2530', ak_titel=F['Seehimmel']),
    'b': dict(name='Fliese und Lichterkette', kurz='Fliese',
              satz='Der dunkle Grund der Zementfliesen an der Bar als dunkle Fläche, ihre hellen Felder als helle, das Licht der Lichterkette in der Platane als Linie und Zeichen. Stuhlblau nur als Punkt.',
              nacht=mix(F['Fliese Anthrazit'], '#000000', .46), tief=mix(F['Fliese Anthrazit'], '#000000', .26), mittel=F['Fliese Anthrazit'],
              kalk=mix(mix(F['Fliese Kalk'], F['Fliese Terrakotta'], .16), '#FFFFFF', .55), kalk2=mix(mix(F['Fliese Kalk'], F['Fliese Terrakotta'], .2), '#FFFFFF', .22),
              ak=F['Lichterkette'], ak_h=mix(F['Lichterkette'], '#FFFFFF', .4), ak_t=mix(F['Lichterkette'], '#000000', .42),
              tinte=mix(F['Fliese Anthrazit'], '#000000', .55), signal=F['Stuhlblau'], titel_h=mix(F['Fliese Anthrazit'], '#000000', .3),
              ak_text='#2A1C00', ak_titel=mix(F['Lichterkette'], F['Fliese Kalk'], .32)),
}


# ---------------------------------------------------------------- Zeichen
def svg_inline(name, cls=''):
    t = open(os.path.join(M, 'zeichen', name)).read().strip()
    return t.replace('<svg ', '<svg class="%s" aria-hidden="true" ' % cls, 1)


def teile(name):
    t = open(os.path.join(M, 'zeichen', name)).read()
    return re.search(r'viewBox="([^"]+)"', t).group(1), re.search(r'<svg[^>]*>(.*)</svg>', t, re.S).group(1)


# ---------------------------------------------------------------- Tapete: feines Punktraster (die Kugeln der Zeiger), die Zeiger als Medaillon
def tapete(farbe, a_punkt, a_zeiger):
    vb, innen = teile('zeiger.svg')
    x, y, w, h = [float(v) for v in vb.split()]
    zh = 40.0; zw = zh * w / h
    pk = ''.join('<circle cx="%d" cy="%d" r="1.1"/>' % (cx, cy) for cx in range(14, 168, 28) for cy in range(14, 168, 28)
                 if not (abs(cx - 84) < 30 and abs(cy - 84) < 30))
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="168" height="168" viewBox="0 0 168 168">'
            '<g fill="%s" fill-opacity="%s">%s</g>'
            '<svg x="%.2f" y="%.2f" width="%.2f" height="%.2f" viewBox="%s" fill="%s" fill-opacity="%s">%s</svg></svg>'
            % (farbe, a_punkt, pk, 84 - zw / 2, 84 - zh / 2, zw, zh, vb, farbe, a_zeiger, innen.replace('currentColor', farbe)))


for k, w in WELTEN.items():
    open(os.path.join(M, 'tapete-%s-dunkel.svg' % k), 'w').write(tapete(w['ak'], .22, .12))
    open(os.path.join(M, 'tapete-%s-hell.svg' % k), 'w').write(tapete(w['mittel'], .2, .085))


# ---------------------------------------------------------------- farben.svg (Farbkarten)
def farben_svg():
    W, rh = 1200, 132
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="DM Mono, Menlo, monospace">' % (W, rh * len(FARBEN) + 40, W, rh * len(FARBEN) + 40),
           '<rect width="100%%" height="100%%" fill="%s"/>' % WELTEN['a']['kalk']]
    for i, f in enumerate(FARBEN):
        y = 20 + i * rh
        out.append('<rect x="20" y="%d" width="220" height="%d" rx="10" fill="%s"/>' % (y, rh - 16, f['hex']))
        for j, t in enumerate(toene(f['hex'])):
            out.append('<rect x="%d" y="%d" width="110" height="%d" rx="6" fill="%s"/>' % (260 + j * 118, y, rh - 52, t))
            out.append('<text x="%d" y="%d" font-size="12" fill="#1d2326">%s</text>' % (260 + j * 118, y + rh - 30, t))
        out.append('<text x="870" y="%d" font-size="18" fill="#1d2326">%s</text>' % (y + 28, E(f['name'])))
        out.append('<text x="870" y="%d" font-size="14" fill="#1d2326">%s · %s</text>' % (y + 52, f['hex'], E(f['belegt'])))
    out.append('</svg>')
    open(os.path.join(M, 'farben.svg'), 'w').write('\n'.join(out))


farben_svg()


# ---------------------------------------------------------------- gemeinsames CSS
def css_welt(sel, w):
    return ('%s{--nacht:%s;--tief:%s;--mittel:%s;--kalk:%s;--kalk2:%s;--ak:%s;--ak-h:%s;--ak-t:%s;--tinte:%s;--signal:%s;--titel-h:%s;--ak-text:%s;--ak-titel:%s}'
            % (sel, w['nacht'], w['tief'], w['mittel'], w['kalk'], w['kalk2'], w['ak'], w['ak_h'], w['ak_t'], w['tinte'], w['signal'], w['titel_h'], w['ak_text'], w['ak_titel']))


def css(t='..'):
    return (r'''
@font-face{font-family:'Open Sans';src:url(%(t)s/schriften/OpenSans-var.woff2) format('woff2');font-weight:300 800;font-stretch:75%% 100%%;font-display:swap}
@font-face{font-family:'Open Sans Ersatz';src:local('Arial');size-adjust:105%%;ascent-override:102%%;descent-override:28%%}
@font-face{font-family:'Instrument Sans';src:url(%(t)s/schriften/InstrumentSans-normal-400_600.woff2) format('woff2');font-weight:400 600;font-display:swap}
@font-face{font-family:'DM Mono';src:url(%(t)s/schriften/DMMono-normal-400.woff2) format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:'Gilda Display';src:url(%(t)s/schriften/GildaDisplay-latin.woff2) format('woff2');font-weight:400;font-display:swap}
''' % {'t': t}) + css_welt(':root,[data-welt=a]', WELTEN['a']) + css_welt('[data-welt=b]', WELTEN['b']) + r'''
[data-welt=a]{--tap-d:url(%(t)s/tapete-a-dunkel.svg);--tap-h:url(%(t)s/tapete-a-hell.svg)}
[data-welt=b]{--tap-d:url(%(t)s/tapete-b-dunkel.svg);--tap-h:url(%(t)s/tapete-b-hell.svg)}
:root{--titel:'Open Sans','Open Sans Ersatz',Arial,sans-serif;--lauf:'Instrument Sans',system-ui,sans-serif;--mono:'DM Mono',ui-monospace,Menlo,monospace;
  --sperr:.205em;--rand:clamp(16px,5vw,64px);--e1:cubic-bezier(.16,1,.3,1);--rund:clamp(22px,2.6vw,34px)}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%}
body{margin:0;background:var(--kalk);color:var(--tinte);font:400 17px/1.62 var(--lauf);-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{display:block;max-width:100%%}
a{color:inherit}
.innen{max-width:1180px;margin:0 auto;padding:0 var(--rand)}
.dunkel{background-color:var(--nacht);background-image:var(--tap-d);background-size:168px;color:#EEF2F2}
.hell{background-color:var(--kalk);background-image:var(--tap-h);background-size:168px}
.matt{background:var(--kalk2)}
.blatt{position:relative;border-radius:var(--rund) var(--rund) 0 0;margin-top:calc(var(--rund)*-1);padding:clamp(72px,9vw,120px) 0}
.mono{font-family:var(--mono);font-size:11.5px;letter-spacing:.17em;text-transform:uppercase}
.vers{font-family:var(--titel);font-weight:400;text-transform:uppercase;letter-spacing:var(--sperr)}
.kopf{display:flex;flex-direction:column;align-items:center;text-align:center;margin-bottom:clamp(36px,5vw,64px)}
.kopf .z{width:38px;height:auto;color:var(--ak-t);margin-bottom:18px}
.dunkel .kopf .z{color:var(--ak)}
.kopf h2{font:400 clamp(1.7rem,3.4vw,2.9rem)/1.16 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:14px 0 0;color:var(--titel-h);max-width:24ch;text-wrap:balance}
.dunkel .kopf h2{color:#F2F5F5}
.kopf h2 em{font-style:normal;color:var(--ak-t)}
.dunkel .kopf h2 em{color:var(--ak-titel)}
.kopf .mono{color:var(--ak-t)}
.dunkel .kopf .mono{color:var(--ak-h)}
.kopf p{max-width:60ch;margin:18px auto 0;opacity:.86}
/* Knopf: Pille mit rundem Knauf, Tiefe und Glanz (Master 2.6) */
.knopf{position:relative;display:inline-flex;align-items:center;gap:18px;height:54px;padding:0 6px 0 26px;border-radius:27px;overflow:hidden;
  font:400 11.5px/1 var(--mono);letter-spacing:.17em;text-transform:uppercase;text-decoration:none;color:var(--ak-text);
  background:linear-gradient(180deg,color-mix(in srgb,var(--ak-titel) 55%%,#fff),var(--ak-titel) 58%%,color-mix(in srgb,var(--ak-titel) 80%%,#000));
  box-shadow:inset 0 1px 0 rgba(255,255,255,.6),inset 0 -2px 0 rgba(0,0,0,.18),0 22px 34px -20px rgba(0,0,0,.6);
  transition:transform .5s var(--e1),box-shadow .5s var(--e1)}
.knopf::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%%,rgba(255,255,255,.45) 50%%,transparent 70%%);transform:translateX(-120%%);pointer-events:none}
.knopf:hover{transform:translateY(-2px)}
.knopf:hover::after{transform:translateX(120%%);transition:transform .9s var(--e1)}
.knopf:active{transform:translateY(1px)}
.knopf .kn{width:42px;height:42px;border-radius:50%%;display:grid;place-items:center;background:linear-gradient(180deg,var(--tief),var(--nacht));color:var(--ak-h);box-shadow:inset 0 1px 0 rgba(255,255,255,.18),0 6px 12px -6px rgba(0,0,0,.6)}
.knopf .pf{width:16px;height:10px;stroke:currentColor;fill:none;stroke-width:1.3}
.knopf--dunkel{color:#F2F5F5;background:linear-gradient(180deg,var(--mittel),var(--tief) 60%%,var(--nacht));box-shadow:inset 0 1px 0 rgba(255,255,255,.2),inset 0 -2px 0 rgba(0,0,0,.35),0 22px 34px -20px rgba(0,0,0,.6)}
.knopf--dunkel .kn{background:linear-gradient(180deg,var(--ak-h),var(--ak));color:var(--ak-text)}
/* Auftritt: von unten, deckend, satt an den Platz; startet, sobald ein Fünftel im Bild ist */
.js [data-a]{opacity:0;transform:translateY(40px) scale(1.02);transition:opacity .85s var(--e1),transform 1.3s var(--e1)}
.js [data-a].da{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.js [data-a]{opacity:1;transform:none;transition:none}}
''' % {'t': t}


JS = r'''<script>
document.documentElement.classList.add('js');if('scrollRestoration' in history)history.scrollRestoration='manual';
(function(){
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('da');io.unobserve(e.target)}})},{threshold:.2});
document.querySelectorAll('[data-a]').forEach(function(el){io.observe(el)});
})();
</script>'''
PFEIL = '<span class="kn"><svg class="pf" viewBox="0 0 16 10"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span>'


def seite(titel, body, extra_css='', tiefe='..', beschreibung=''):
    return ('<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex"><title>%s</title><meta name="description" content="%s">'
            '<link rel="icon" href="%s/zeichen/zeiger.svg"><style>%s%s</style></head><body data-welt="a">%s%s</body></html>'
            % (E(titel), E(beschreibung), tiefe, css(tiefe), extra_css, body, JS))


# ---------------------------------------------------------------- Ton und eigene Welt
TON = dict(
    charakter=[
        'Eine junge Küche mit Sterne-Herkunft, die am Hafen eine Wirtschaft sein will: Monika Huber, früher Sous-Chefin im Schäfli und vorher bei Dieter Koschina in der Vila Joya, kocht seit April 2025 am See; GaultMillau nennt sie «Entdeckung des Jahres 2026».',
        'Das Mittelmeer auf einer Karte, geordnet nach Frankreich, Italien, Iberischer Halbinsel und Klassikern; die Tortelloni mit Tomate, Burrata und Taggiasca-Olive sind das Gericht des Hauses.',
        'Bedient wird «auf légère Art und Weise», wie das Tagblatt schreibt: «Mehr Wirtschaft, weniger feine Pinkel». An der Bar, die von drinnen nach draussen führt, der «Lästermeile», gibt es den ganzen Tag Tapas.'],
    eigene_worte=['Willkommen in der Wirtschaft am Schlössli', 'Direkt im Hafen von Bottighofen', 'mit Blick aufs Wasser und die Alpen',
                  'Die schönste Terrasse am Bodensee', 'kulinarische Reise in die Welt der mediterranen Küche', 'junges Küchenteam', 'frischer Wind',
                  'herzliche Gastfreundschaft', 'Lästermeile', 'Tapas durchgehend', 'Zur Stärkung & Süsses', 'Banketts & Gruppen', 'Tavolata oder gesetztes Menue',
                  'unkompliziert', 'in Ruhe besprechen', 'Reservation', 'klassisch wie bei der italienischen Oma'],
    nicht=['kulinarische Highlights', 'Genuss pur', 'ein Fest für die Sinne', 'Gourmet-Tempel', 'unvergesslich', 'Verwöhnprogramm', 'Geheimtipp',
           'Wir essen im Schlössli (das Restaurant liegt im ehemaligen Hafenmeistergebäude)', 'Statt zu … / ohne zu …', '«ß» (heute in «Genießen», «Weißen»)', 'Du-Ansprache (das Cookie-Fenster duzt heute)'],
    quellen=['_quelle/website/text/start.md', '_quelle/website/text/karten.md', '_quelle/website/pdf-text/Speisekarte-Oktober.txt', '_quelle/website/pdf-text/Lastermeile-Homepage-2339.txt',
             '_quelle/presse/tagblatt-zu-tisch.md', '_quelle/presse/gaultmillau-zwei-koeniginnen.md', '_quelle/extern/portale/gaultmillau.md', '_kette/02-spaeher/befund.md'])

EIGENE_WELT = dict(
    satz=['Die Wirtschaft am Schlössli ist die Welt eines Hafens am Bodensee: blaue Stühle auf Kies unter Platanen, das Wasser bis zu den Alpen, '
          'eine Bar mit alten Zementfliesen, die von drinnen nach draussen führt, und ein Logo mit zwei Zeigern, dessen Nabe das Ö im Namen ist.',
          'Der Ort hat ein langes Gedächtnis mit Augenzwinkern: Ende des 17. Jahrhunderts setzte Hans Conrad Hafen im «Haus am See» einen Wirt als Pächter ein, der die Schiffsleute bewirtete, '
          'und hängte statt eines Wirtshausschilds einen Besen heraus; 1699 musste er sich der Tagsatzung fügen. Heute ist die Taverne der Familie die Schwester in Wigoltingen.',
          'Die Seite nimmt den Horizont des Sees als Ordnung, eine feine Linie, die über die ganze Breite läuft und an der Bild und Titel sitzen, '
          'und die Zeiger als einziges Zeichen. Worin sie sich von den bisherigen Häusern unterscheidet, steht darunter, Haus für Haus.'],
    unterschied_zu={
        'Taverne zum Schäfli (Schwesterhaus)': 'Riegelhaus im Dorf, Ochsenblut oder Ladengrün auf Kalk, Schildgold, Lamm als Wappen, Titel in Petrona; hier See und Hafen, Stuhlblau und Seehimmel, kein Gold, Zeiger statt Wappentier, Titel in den Versalien der Wortmarke.',
        'Carlton-Europe': 'Vintage-Hotel in Interlaken, Dachterrasse, Kissen, Weinkeller, Nachtblau und Gold; hier kein Hotel, ein Restaurant am Wasser, Petrolblau aus den Stühlen statt Nachtblau, keine Goldlinie.',
        'Grand Beau-Rivage': 'Belle Époque, Portier und Ballsaal, Marine und Beige, Medaillon-Tapete; hier Kies und Platanen, die Tapete ein Punktraster aus den Kugeln der Zeiger.',
        'Hotel Seiler au Lac': 'Seehotel in Braun, Creme und Gold mit Serifen; hier dasselbe Element Wasser, aber kühl, ohne Gold, in einer Grotesk.',
        'Waldhotel Doldenhorn': 'Wald und Berge im Kandertal; hier Mittelland, Hafen und Mittelmeer auf dem Teller.',
        'Landgasthof Ruedihus': 'Holzhaus mit Zimmern im Kandertal; hier keine Zimmer, eine Bar mit Fliesen und eine Terrasse.',
        'Berghotel Gasterntal': 'Tal, Weg und Picknick mit Polaroids, Graphit und kühles Papier mit dem Rot der Läden; hier kein Weg, sondern ein Platz, an dem man sitzen bleibt, Petrol mit hellblauem Papier und Schirmrot als Punkt.',
        'Zurbriggen (vier Häuser)': 'Berg, Schnee und Lärche; Zermatt in Anthrazit mit Pinsel-Rot, Monte-Moro in Bergnacht-Blau; hier Wasser und Hafen im Mittelland, Petrol der Stühle und Himmelblau, Rot nur als kleiner Punkt.',
        'Salt & Silver': 'Hamburger Taco-Bar mit Reise-Erzählung, Antonio in Versalien; hier ruhige, weit gesperrte Versalien aus der eigenen Wortmarke.'})

# ---------------------------------------------------------------- Markenbuch
GRUPPEN = [('hafen', 'Der Hafen am Tag', 'Gemessen am Startbild der Seite, an der Terrasse unter den Platanen und an einem Teller.'),
           ('abend', 'Der Abend am Wasser', 'Gemessen an der Terrasse nach Sonnenuntergang.'),
           ('fliese', 'Die Fliesen der Bar', 'Gemessen an den Zementfliesen, die auf der Seite neben der Bar stehen.'),
           ('logo', 'Das Logo', 'Das Logo ist einfarbig Schwarz und bleibt es.'),
           ('heute', 'Die heutige Seite', 'Aus der Squarespace-Seite von 2024. Am Haus nicht belegt, darum nicht in den Farbwelten.')]


def farbzeile(f):
    if f.get('zeige'):
        bild = '<div class="fz__wap"><img src="%s" alt="" loading="lazy"></div>' % f['zeige']
    elif f['foto']:
        bild = '<img src="bilder/%s.webp" alt="" loading="lazy">' % f['foto']
    else:
        bild = '<div class="fz__heute">heutige Seite</div>'
    stufen = ''.join('<span style="background:%s" title="%s"><i>%s</i></span>' % (c, c, c) for c in toene(f['hex']))
    if f['hex'] == '#000000':
        stufen = ''
    return ('<article class="fz" data-a>'
            '<div class="fz__b">%s</div>'
            '<div class="fz__t"><div class="fz__f" style="background:%s"></div>'
            '<div class="fz__n"><h3>%s</h3><p class="mono">%s · %s</p></div>'
            '<p class="fz__q">%s</p>%s'
            '%s</div></article>'
            % (bild, f['hex'], E(f['name']), f['hex'], E('belegt: ' + f['belegt']), E(f['fundstelle']),
               ('<p class="fz__q fz__auch">%s</p>' % E(f['auch'])) if f['auch'] else '',
               ('<div class="fz__s" aria-label="abgeleitete Töne">%s</div><p class="fz__ab mono">abgeleitete Töne, gerechnet</p>' % stufen) if stufen else ''))


def welt_tafel(k, w):
    sw = ''.join('<div><span style="background:%s"></span><b>%s</b><i class="mono">%s</i></div>' % (c, n, c) for n, c in
                 [('Nacht', w['nacht']), ('Tief', w['tief']), ('Fläche', w['mittel']), ('Hell', w['kalk']), ('Hell 2', w['kalk2']), ('Linie', w['ak']), ('Schrift', w['tinte']), ('Punkt', w['signal'])])
    return ('<article class="wt" data-welt="%s" data-a>'
            '<div class="wt__d dunkel"><p class="mono">Farbwelt · %s</p>%s<h3>%s</h3><p>%s</p>'
            '%s</div>'
            '<div class="wt__h hell"><h4>Willkommen in der <em>Wirtschaft am Schlössli.</em></h4>'
            '<span class="knopf knopf--dunkel" aria-hidden="true">Tisch reservieren %s</span></div>'
            '<div class="wt__s">%s</div></article>'
            % (k, 'gewählt' if k == 'a' else 'B · verworfen', svg_inline('zeiger.svg', 'wt__z'), E(w['name']), E(w['satz']),
               ('<a class="knopf" href="probe.html">Probe ansehen %s</a>' % PFEIL) if k == 'a' else '<p class="mono">am 19.10.2026 nicht gewählt</p>', PFEIL, sw))


MB_CSS = r'''
.auftakt{min-height:min(92svh,900px);display:flex;align-items:center;padding:clamp(110px,14vh,160px) 0 clamp(90px,12vh,140px);text-align:center}
.auftakt .innen{display:flex;flex-direction:column;align-items:center}
.auftakt .wap{width:clamp(120px,13vw,168px);height:auto;color:var(--ak)}
.auftakt h1{font:400 clamp(1.9rem,5.4vw,4.6rem)/1.12 var(--titel);margin:30px 0 0;letter-spacing:.3em;text-transform:uppercase;padding-left:.3em}
.auftakt .ort{display:flex;align-items:center;gap:16px;margin-top:18px;color:var(--ak-h)}
.auftakt .ort i{width:clamp(26px,4vw,60px);height:1px;background:currentColor;opacity:.7}
.auftakt .unter{max-width:54ch;margin-top:24px;opacity:.9}
.wahl{display:inline-flex;flex-wrap:wrap;justify-content:center;gap:6px;margin-top:34px;padding:6px;border-radius:30px;background:rgba(0,0,0,.25);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--ak) 35%,transparent)}
.wahl button{all:unset;cursor:pointer;padding:13px 20px;border-radius:24px;font:400 11.5px/1 var(--mono);letter-spacing:.17em;text-transform:uppercase;color:rgba(255,255,255,.82)}
.wahl button[aria-pressed=true]{color:var(--ak-text);background:linear-gradient(180deg,var(--ak-h),var(--ak))}
.wahl button:focus-visible{outline:2px solid var(--ak-h);outline-offset:2px}
.zg{display:grid;gap:clamp(28px,4vw,56px);grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);align-items:center}
.zg__gross{background:#fff;border-radius:var(--rund);padding:clamp(28px,4vw,56px);box-shadow:0 40px 60px -40px rgba(0,0,0,.35)}
.zg__gross svg{width:min(100%,400px);height:auto;margin:0 auto;display:block}
.zg__fass{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.zg__fass figure{margin:0;border-radius:18px;padding:22px;display:flex;flex-direction:column;align-items:center;gap:12px;box-shadow:0 26px 40px -30px rgba(0,0,0,.4)}
.zg__fass svg{height:120px;width:auto}
.zg__fass figcaption{font:400 11px/1.4 var(--mono);letter-spacing:.12em;text-transform:uppercase;text-align:center}
.f1{background:#fff;color:#000}.f2{background:var(--kalk2);color:var(--tinte)}.f3{background:var(--nacht);color:var(--ak)}.f4{background:var(--tief);color:var(--kalk)}
.zg__dl{margin-top:22px;display:flex;flex-wrap:wrap;gap:12px 22px}
.zg__dl a{font:400 11.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ak-t);text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:4px}
.herkunft{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:clamp(36px,5vw,60px)}
.herkunft figure{margin:0;position:relative;border-radius:var(--rund);overflow:hidden;box-shadow:0 40px 60px -40px rgba(0,0,0,.45);background:#fff}
.herkunft img{width:100%;object-fit:contain;aspect-ratio:4/3;padding:clamp(16px,3vw,36px)}
.herkunft figcaption{padding:16px 22px 20px;font-size:14.5px;line-height:1.45;color:var(--tinte);border-top:1px solid rgba(0,0,0,.06)}
.wm{display:grid;gap:16px;grid-template-columns:1fr 1fr}
.wm figure{margin:0;border-radius:var(--rund);overflow:hidden;background:#fff;color:var(--tinte);box-shadow:0 30px 50px -36px rgba(0,0,0,.4)}
.wm figure .alt{padding:clamp(20px,3vw,40px);display:flex;justify-content:center;background:#fff}
.wm figure .alt{min-height:280px;align-items:center}
.wm figure .alt img{width:min(100%,460px)}
.wm figure .bild img{width:100%;aspect-ratio:4/3;object-fit:cover}
.wm figcaption{padding:18px 22px 22px;font-size:15px;line-height:1.5}
.wm figcaption b{display:block;font:400 11.5px/1.3 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--ak-t);margin-bottom:6px}
.vgl{margin-top:clamp(36px,5vw,64px);border-radius:var(--rund);background:#fff;color:var(--tinte);padding:clamp(24px,4vw,52px);box-shadow:0 30px 50px -36px rgba(0,0,0,.35)}
.vgl img{width:100%;max-width:900px;margin:0 auto}
.vgl .satz{font:400 clamp(1.1rem,3.4vw,2.6rem)/1.15 var(--titel);letter-spacing:.3em;text-transform:uppercase;text-align:center;margin:26px 0 0;color:#000;padding-left:.3em}
.vgl p.mono{text-align:center;color:var(--ak-t);margin:18px auto 0;max-width:70ch;line-height:1.6}
.muster{display:grid;gap:clamp(24px,4vw,56px);grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);margin-top:0;align-items:start}
.muster h3{font:400 clamp(1.8rem,3.6vw,3.1rem)/1.16 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:12px 0 20px;color:var(--titel-h)}
.muster h3 em{font-style:normal;color:var(--ak-t)}
.muster .lauf{max-width:58ch}
.muster dl{margin:0;display:grid;gap:18px}
.muster dt{font:400 11.5px/1 var(--mono);letter-spacing:.17em;text-transform:uppercase;color:var(--ak-t)}
.muster dd{margin:6px 0 0;font-size:15.5px;line-height:1.5}
.gew{display:flex;flex-wrap:wrap;gap:10px 30px;margin-top:24px;font-family:var(--titel);font-size:1.25rem;text-transform:uppercase;letter-spacing:.2em}
.heute-schrift{margin-top:clamp(36px,5vw,60px);display:grid;grid-template-columns:1fr 1fr;gap:16px}
.heute-schrift div{background:#fff;border-radius:18px;padding:22px 24px;box-shadow:0 26px 40px -32px rgba(0,0,0,.35)}
.heute-schrift b{display:block;font:400 11px/1.3 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:#7b8486;margin-bottom:10px}
.heute-schrift p{margin:0}
.gruppe{margin-top:clamp(50px,7vw,90px)}
.gruppe:first-of-type{margin-top:0}
.gruppe>h3{font:400 clamp(1.3rem,2.4vw,1.9rem)/1.2 var(--titel);text-transform:uppercase;letter-spacing:.18em;margin:0;text-align:center;color:var(--titel-h)}
.gruppe>p{text-align:center;margin:10px auto 28px;max-width:60ch;opacity:.8}
.fz{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);border-radius:var(--rund);overflow:hidden;background:#fff;box-shadow:0 34px 60px -40px rgba(0,0,0,.42);margin-bottom:22px}
.fz__b{min-height:300px;position:relative;background:var(--kalk2)}
.fz__b>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.fz__b>img[src*="heute-"]{object-fit:cover;background:#D8FFFC}
.fz__wap{position:absolute;inset:0;display:grid;place-items:center;background:#fff}
.fz__wap img{width:72%;height:auto;max-height:86%;object-fit:contain}
.fz__heute{position:absolute;inset:0;display:grid;place-items:center;font:400 11.5px/1 var(--mono);letter-spacing:.17em;text-transform:uppercase;color:#7b8486;background:repeating-linear-gradient(135deg,#eef1f1 0 14px,#e5e9e9 14px 28px)}
.fz__t{min-width:0;padding:clamp(20px,2.6vw,32px);display:grid;grid-template-columns:110px 1fr;gap:6px 22px;align-content:start}
.fz__f{grid-row:span 3;width:110px;height:140px;border-radius:12px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08),0 18px 28px -18px rgba(0,0,0,.45)}
.fz__n h3{font:400 1.25rem/1.25 var(--titel);text-transform:uppercase;letter-spacing:.14em;margin:0}
.fz__n .mono{margin:8px 0 0;color:var(--ak-t)}
.fz__q{margin:0;overflow-wrap:anywhere;font-size:14.5px;line-height:1.5;color:#4b5456;grid-column:2}
.fz__auch{color:#6f787a}
.fz__s{grid-column:1/-1;display:grid;grid-template-columns:repeat(5,1fr);margin-top:18px;border-radius:10px;overflow:hidden}
.fz__s span{height:62px;position:relative}
.fz__s i{position:absolute;left:8px;bottom:6px;font:400 10px/1 var(--mono);letter-spacing:.06em;font-style:normal;color:#fff;mix-blend-mode:difference}
.fz__ab{grid-column:1/-1;margin:8px 0 0;color:#7b8486;font-size:10.5px}
.welten{display:grid;grid-template-columns:1fr 1fr;gap:clamp(16px,2.4vw,28px)}
.welten--eins{grid-template-columns:minmax(0,760px);justify-content:center}
.verworfen{max-width:560px;margin:0 auto;opacity:.82;filter:saturate(.7)}
.anhang .kopf h2{font-size:clamp(1.4rem,2.6vw,2.2rem)}
.wt{border-radius:var(--rund);overflow:hidden;box-shadow:0 44px 70px -44px rgba(0,0,0,.6),0 0 0 1px color-mix(in srgb,var(--ak) 30%,transparent);background:var(--kalk);color:var(--tinte)}
.wt__d{padding:clamp(26px,3.4vw,44px);text-align:center;display:flex;flex-direction:column;align-items:center;color:#EEF2F2}
.wt__d .mono{color:var(--ak-h)}
.wt__z{width:40px;height:auto;color:var(--ak);margin:18px 0 6px}
.wt__d h3{font:400 clamp(1.3rem,2.2vw,1.8rem)/1.2 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:8px 0 12px;color:#F2F5F5}
.wt__d p{max-width:42ch;margin:0 0 24px;opacity:.88}
.wt__h{padding:clamp(26px,3.4vw,44px);text-align:center}
.wt__h h4{font:400 clamp(1.05rem,1.7vw,1.4rem)/1.3 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:0 0 22px;color:var(--titel-h)}
.wt__h h4 em{font-style:normal;color:var(--ak-t)}
.wt__s{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(0,0,0,.06)}
.wt__s div{background:#fff;padding:12px 12px 14px;display:flex;flex-direction:column;gap:4px;min-width:0}
.wt__s span{height:40px;border-radius:6px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.wt__s b{font-weight:500;font-size:14px}
.wt__s i{font-style:normal;font-size:10.5px;color:#6f787a}
.abgrenzung{margin-top:clamp(28px,4vw,48px);display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.abgrenzung div{border-radius:18px;padding:18px 20px;background:rgba(255,255,255,.06);box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}
.abgrenzung div:last-child:nth-child(odd){grid-column:1/-1;width:min(100%,calc(50% - 7px));justify-self:center}
.abgrenzung .pk span{min-width:0}
.abgrenzung b{display:block;font:400 11px/1.3 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--ak-h);margin-bottom:10px}
.abgrenzung .pk{display:flex;gap:6px}
.abgrenzung .pk span{flex:1;height:30px;border-radius:6px}
.abgrenzung p{margin:10px 0 0;font-size:14.5px;opacity:.85}
.rf{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.rf a{display:block;text-decoration:none;border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 26px 44px -32px rgba(0,0,0,.45)}
.rf img{width:100%;aspect-ratio:4/3;object-fit:cover}
.rf span{display:block;padding:12px 14px 14px;font-size:14px;line-height:1.35}
.rf b{display:block;font:400 10.5px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;margin-bottom:5px}
.rf .ja b{color:#2f6b55}.rf .nein b{color:#a23a2c}
.mitte{text-align:center;margin-top:30px}
.ton{display:grid;gap:clamp(28px,4vw,60px);grid-template-columns:minmax(0,1.2fr) minmax(0,1fr)}
.ton ol{list-style:none;margin:0;padding:0;display:grid;gap:24px}
.ton li{font-size:clamp(1.05rem,1.5vw,1.25rem);line-height:1.55;padding-left:22px;border-left:1px solid color-mix(in srgb,var(--ak) 60%,transparent)}
.worte h3{font:400 11.5px/1 var(--mono);letter-spacing:.17em;text-transform:uppercase;color:var(--ak-h);margin:0 0 12px}
.worte p{margin:0 0 28px;font-size:16px;line-height:1.75}
.worte .nein{opacity:.72;text-decoration:line-through;text-decoration-color:color-mix(in srgb,var(--signal) 80%,transparent)}
.welt p.gross{font-size:clamp(1.1rem,1.7vw,1.35rem);line-height:1.6;margin:0 auto 22px;max-width:62ch;color:var(--titel-h)}
.ud{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:rgba(0,0,0,.08);border-radius:var(--rund);overflow:hidden;margin-top:clamp(36px,5vw,60px);box-shadow:0 30px 50px -36px rgba(0,0,0,.4)}
.ud div{background:#fff;padding:22px 24px}
.ud div:last-child:nth-child(odd){grid-column:1/-1}
.ud b{display:block;font:400 11.5px/1.3 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--ak-t);margin-bottom:6px}
.ud p{margin:0;font-size:15px;line-height:1.5}
.fuss{padding:56px 0 64px;text-align:center;font-size:14px}
.fuss p{opacity:.75;margin:6px 0}
@media(max-width:900px){.zg,.wm,.muster,.ton,.welten,.herkunft,.ud,.heute-schrift,.abgrenzung{grid-template-columns:1fr}.rf{grid-template-columns:1fr 1fr}.fz{grid-template-columns:1fr}.fz__b{min-height:220px}}
@media(max-width:520px){.fz__t{grid-template-columns:76px 1fr}.fz__f{width:76px;height:96px}.wt__s{grid-template-columns:repeat(2,1fr)}.zg__fass svg{height:84px}.auftakt h1{letter-spacing:.22em;padding-left:.22em}}
'''

RF = [  # (datei, ja/nein, titel, satz)
    ('richtig-schwarz-auf-hell', 'ja', 'Schwarz auf Hell', 'Das Logo in seinem Schwarz auf Weiss oder auf der hellen Fläche.'),
    ('richtig-zeichen-auf-dunkel', 'ja', 'Zeichen einfarbig hell', 'Auf der dunklen Fläche steht das Zeichen einfarbig in der Linienfarbe.'),
    ('richtig-schutzraum', 'ja', 'Schutzraum', 'Rundum frei, so breit wie eine der beiden Kugeln an den Zeigern (63 von 1120 Pixeln).'),
    ('richtig-klein', 'ja', 'Klein: das Zeichen allein', 'Unter 240 Pixeln Logobreite steht das Zeichen ohne Schrift; die Zeile «by Christian Kuchler» wäre sonst niedriger als 4,5 Pixel (gerechnet: 21 von 1120 Pixeln).'),
    ('falsch-verzerrt', 'nein', 'Nicht verzerren', 'Der Kreis bleibt rund, das Logo in seinem Verhältnis.'),
    ('falsch-umgefaerbt', 'nein', 'Nicht einfärben', 'Keine farbigen Zeiger, kein zweifarbiges Logo.'),
    ('falsch-unruhig', 'nein', 'Nicht auf Unruhe', 'Nicht frei auf einem Foto ohne ruhige Fläche dahinter.'),
    ('falsch-verstellt', 'nein', 'Zeiger nicht verstellen', 'Die Zeiger stehen, wie das Haus sie gesetzt hat: nicht drehen, nicht bewegen, kein Schatten.'),
]


def markenbuch():
    gr = ''
    for g, t, s in GRUPPEN:
        gr += '<div class="gruppe"><h3 data-a>%s</h3><p data-a>%s</p>%s</div>' % (E(t), E(s), ''.join(farbzeile(f) for f in FARBEN if f['gruppe'] == g))
    rf = ''.join('<a class="%s" href="logo-richtig-falsch/index.html#%s" data-mitwelt><img src="logo-richtig-falsch/%s.png" alt="" loading="lazy"><span><b>%s</b>%s</span></a>'
                 % (j, d, d, 'Richtig' if j == 'ja' else 'Falsch', E(t)) for d, j, t, s in RF)
    ud = ''.join('<div><b>%s</b><p>%s</p></div>' % (E(k), E(v)) for k, v in EIGENE_WELT['unterschied_zu'].items())
    SM = json.load(open(os.path.join(H, '..', '..', '..', 'Taverne zum Schäfli Wigoltingen', '_kette', '05-markenbauer', 'marke.json')))['farbwelten']
    schaefli = [('Taverne zum Schäfli · Welt %s «%s»' % (w['kennung'].upper(), w['name']), [w['flaechen'][0], w['flaechen'][2], w['flaechen'][3], w['akzent'], w['punkt']]) for w in SM] + [
                ('Schlössli · gewählt: «Stuhl und See»', [WELTEN['a'][x] for x in ('nacht', 'mittel', 'kalk', 'ak', 'signal')]),
            ]
    abgr = ''.join('<div><b>%s</b><div class="pk">%s</div></div>' % (E(n), ''.join('<span style="background:%s" title="%s"></span>' % (c, c) for c in cs)) for n, cs in schaefli)
    body = '''
<header class="auftakt dunkel"><div class="innen">
  <div data-a>%(zeichen_a)s</div>
  <h1 data-a>Wirtschaft am Schlössli</h1>
  <p class="ort mono" data-a><i></i>Markenbuch · Bottighofen am Bodensee<i></i></p>
  <p class="unter" data-a>Das Zeichen mit den zwei Zeigern, die Versalien der Wortmarke und die Farben des Hafens: alles hier ist am Haus gemessen. Die Farbwelt ist «Stuhl und See», das Blau der Terrassenstühle und der Himmel über dem See.</p>
</div></header>

<section class="blatt hell" id="zeichen"><div class="innen">
  <div class="kopf" data-a>%(zeiger_k)s<p class="mono">Das Zeichen</p><h2>Ein Kreis, zwei Zeiger, <em>zwei Kugeln.</em></h2>
  <p>Das Logo des Hauses ist ein gebrochener Kreis mit zwei Zeigern und zwei Kugeln; die Nabe der Zeiger ist zugleich das Ö im Namen. Was die Zeiger meinen, sagt das Haus nirgends, deshalb wird hier nichts hineingelesen. Die Schrift ist weggelassen, der Rest aus dem Original als Vektor gezogen.</p></div>
  <div class="zg">
    <div class="zg__gross" data-a style="color:#000">%(zeichen_g)s</div>
    <div data-a>
      <div class="zg__fass">
        <figure class="f1">%(zeichen1)s<figcaption>Zeichen · Schwarz</figcaption></figure>
        <figure class="f2">%(zeichen2)s<figcaption>Auf heller Fläche</figcaption></figure>
        <figure class="f3">%(zeichen3)s<figcaption>Hell auf Dunkel</figcaption></figure>
        <figure class="f4">%(zeiger2)s<figcaption>Die Zeiger allein</figcaption></figure>
      </div>
      <div class="zg__dl"><a href="zeichen/zeichen.svg" download>Zeichen · SVG</a><a href="zeichen/zeiger.svg" download>Zeiger · SVG</a><a href="logo/logo-transparent-1563.png" download>Logo · PNG 1563 px</a></div>
    </div>
  </div>
  <div class="herkunft">
    <figure data-a><img src="logo/logo-transparent-1563.png" alt="" loading="lazy"><figcaption>Grösste Fassung: transparent, 1563 × 1563 Pixel. Sie liegt nur auf der Seite des Schäfli, unter «Partner-Restaurant am Bodensee». Eine Vektordatei ist nicht öffentlich.</figcaption></figure>
    <figure data-a><img src="logo/logo-auf-mint-teilen-bild.jpeg" alt="" loading="lazy" style="background:#E0FEFB"><figcaption>Auf der eigenen Seite: das Teilen-Bild auf Mint, 1144 × 1258 Pixel.</figcaption></figure>
  </div>
</div></section>

<section class="blatt dunkel" id="wortmarke"><div class="innen">
  <div class="kopf" data-a>%(zeiger_k)s<p class="mono">Wortmarke und Titelschrift</p><h2>Der Name in weit <em>gesperrten Versalien.</em></h2>
  <p>Die Wortmarke ist in Open Sans gesetzt. Neben sie gelegt wurden zehn freie Schriften, Buchstabe für Buchstabe: Open Sans 400 deckt sich zu 95 Prozent, die nächste andere Schrift zu 88. Die Sperrung ist am Wort «WIRTSCHAFT» gemessen.</p></div>
  <div class="wm">
    <figure data-a><div class="alt"><img src="bilder/wortmarke-ausschnitt.png" alt="Ausschnitt aus dem Logo: SCHLÖSSLI, WIRTSCHAFT, BY CHRISTIAN KUCHLER" loading="lazy"></div><figcaption><b>Logo · Ausschnitt aus dem Original</b>SCHLÖSSLI gross, darunter WIRTSCHAFT, darunter klein BY CHRISTIAN KUCHLER, alles in Versalien einer Grotesk.</figcaption></figure>
    <figure data-a><div class="bild"><img src="bilder/wegweiser.webp" alt="Wegweiser auf der Terrasse: A-la-carte-Restaurant-Terrasse und Lästermeile" loading="lazy"></div><figcaption><b>Am Ort · Wegweiser</b>Auf der Terrasse stehen die Wege auf hellblauen Schildern, in gesperrten Versalien einer Serifenschrift: A-LA-CARTE-RESTAURANT-TERRASSE, LÄSTERMEILE.</figcaption></figure>
  </div>
  <div class="vgl" data-a><img src="bilder/vergleich-wortmarke.png" alt="Oben WIRTSCHAFT aus dem Logo, unten Open Sans 400 mit derselben Sperrung"><p class="satz">Wirtschaft am Schlössli</p><p class="mono">Oben das Wort aus dem Logo, darunter Open Sans 400 mit 0,205 em Sperrung · Zeile ganz unten: Open Sans 400, 0,3 em, als Name</p></div>
</div></section>

<section class="blatt hell" id="schrift"><div class="innen">
  <div class="kopf" data-a>%(zeiger_k)s<p class="mono">Schriften</p><h2>Open Sans trägt <em>die Titel.</em></h2>
  <p>Titel stehen in den Versalien der Wortmarke, weit gesperrt, nie fett, nie kursiv. Betont wird über die Farbe. Gelesen wird in einer ruhigen Grotesk, Etiketten und Knöpfe stehen in einer Mono.</p></div>
  <div class="muster">
    <div data-a><p class="mono" style="color:var(--ak-t)">Titel · Open Sans 400, Versalien, 0,16 em</p><h3>Direkt im Hafen, <em>mit Blick aufs Wasser.</em></h3>
      <p class="lauf">Hier erwartet Sie eine kulinarische Reise in die Welt der mediterranen Küche, die mit frischen, hochwertigen Zutaten und kreativen Rezepten zubereitet wird.</p>
      <p class="mono" style="color:var(--ak-t);margin-top:6px">Startseite heute</p>
      <div class="gew"><span>Frankreich</span><span>Italien</span><span>Iberische Halbinsel</span><span>Klassiker</span></div>
    </div>
    <dl data-a>
      <div><dt>Titel</dt><dd>Open Sans, variabel, 400. Name 0,3 em gesperrt, Titel 0,16 em, kleine Zeilen 0,2 em. Datei: marke/schriften/OpenSans-var.woff2 · Google Fonts, SIL Open Font License.</dd></div>
      <div><dt>Lauftext</dt><dd>Instrument Sans 400, 17 px, Zeilenabstand 1,62. Datei: marke/schriften/InstrumentSans-normal-400_600.woff2 · OFL.</dd></div>
      <div><dt>Etiketten und Knöpfe</dt><dd>DM Mono 400 in Versalien, 11,5 px, gesperrt 0,17 em. Datei: marke/schriften/DMMono-normal-400.woff2 · OFL.</dd></div>
      <div><dt>Ersatz beim Laden</dt><dd>Arial mit angeglichener Grösse, damit beim Wechsel nichts springt.</dd></div>
    </dl>
  </div>
  <div class="heute-schrift" data-a>
    <div><b>Heute auf der Seite · Titel</b><p style="font:400 2rem/1.15 'Gilda Display',serif;color:var(--titel-h)">Willkommen in der Wirtschaft am Schlössli!</p><p style="margin-top:10px;font-size:14.5px;color:#4b5456">Gilda Display, frei (OFL), gewählt in der Squarespace-Vorlage 2024. Steht nicht im Logo.</p></div>
    <div><b>Heute auf der Seite · Text</b><p style="font:400 1.05rem/1.6 'PT Serif',Georgia,serif;color:var(--tinte)">Direkt im Hafen von Bottighofen gelegen mit Blick aufs Wasser und die Alpen.</p><p style="margin-top:10px;font-size:14.5px;color:#4b5456">PT Serif, frei (OFL), ebenfalls aus der Vorlage; hier in der Ersatzschrift gezeigt, die Datei ist nicht im Paket.</p></div>
  </div>
</div></section>

<section class="blatt matt" id="farben"><div class="innen">
  <div class="kopf" data-a>%(zeiger_k)s<p class="mono">Farben</p><h2>Jede Farbe mit dem Foto, <em>aus dem sie kommt.</em></h2>
  <p>Gemessen ist der häufigste Ton einer Fläche, nicht ein einzelner Pixel; daneben steht der Median derselben Fläche als zweite Rechnung. Die abgeleiteten Töne darunter sind gerechnet, nicht am Haus gemessen.</p></div>
  %(gruppen)s
</div></section>

<section class="blatt dunkel" id="farbwelten"><div class="innen">
  <div class="kopf" data-a>%(zeiger_k)s<p class="mono">Die Farbwelt</p><h2>Stuhl <em>und See.</em></h2>
  <p>Der Mittag am Wasser: das Blau der Terrassenstühle als dunkle Fläche, der Himmel über dem See aufgehellt als helle Fläche und als Linie, Schirmrot nur als Punkt. Ohne Gold und ohne die Farben des Schäfli, damit man die zwei Häuser der Familie auf den ersten Blick auseinanderhält.</p></div>
  <div class="welten welten--eins">%(welt_a)s</div>
  <div class="abgrenzung" data-a>%(abgr)s</div>
</div></section>

<section class="blatt hell" id="logo"><div class="innen">
  <div class="kopf" data-a>%(zeiger_k)s<p class="mono">Logo richtig und falsch</p><h2>So steht das Logo, <em>so nicht.</em></h2></div>
  <div class="rf" data-a>%(rf)s</div>
  <p class="mitte" data-a><a class="knopf knopf--dunkel" href="logo-richtig-falsch/index.html" data-mitwelt>Alle Regeln ansehen %(pfeil)s</a></p>
</div></section>

<section class="blatt dunkel" id="ton"><div class="innen">
  <div class="kopf" data-a>%(zeiger_k)s<p class="mono">Der Ton</p><h2>Wie das Haus <em>spricht.</em></h2></div>
  <div class="ton">
    <ol data-a>%(charakter)s</ol>
    <div class="worte" data-a><h3>Worte des Hauses</h3><p>%(eigene)s</p><h3>Nicht bei uns</h3><p>%(nicht)s</p></div>
  </div>
</div></section>

<section class="blatt hell welt" id="welt"><div class="innen">
  <div class="kopf" data-a>%(zeiger_k)s<p class="mono">Die eigene Welt</p><h2>Hafen, Platanen <em>und ein Horizont.</em></h2></div>
  %(welt_saetze)s
  <div class="ud" data-a>%(ud)s</div>
  <p class="mitte" data-a><a class="knopf knopf--dunkel" href="probe.html" data-mitwelt>Die Probe ansehen %(pfeil)s</a></p>
</div></section>

<section class="blatt matt anhang" id="anhang"><div class="innen">
  <div class="kopf" data-a>%(zeiger_k)s<p class="mono">Anhang</p><h2>Die verworfene <em>Wahl.</em></h2>
  <p>Zur Wahl stand auch «Fliese und Lichterkette»: der Grund der Zementfliesen an der Bar, ihre hellen Felder und das Gelb der Lichterkette. Robert hat am 19. Oktober 2026 «Stuhl und See» gewählt. Diese Welt bleibt nur hier als Beleg stehen.</p></div>
  <div class="verworfen" data-a>%(welt_b)s</div>
</div></section>

<footer class="fuss dunkel"><div class="innen"><p>Markenbuch der Wirtschaft am Schlössli · Station 05 · erster Durchgang, Stand 19. Oktober 2026</p><p>Designstudie von Tasty Studios, nicht die offizielle Website. Fotos und Logo: Wirtschaft am Schlössli.</p></div></footer>
''' % dict(
        zeichen_a=svg_inline('zeichen.svg', 'wap'), zeiger_k=svg_inline('zeiger.svg', 'z'),
        zeichen_g=svg_inline('zeichen.svg'), zeichen1=svg_inline('zeichen.svg'), zeichen2=svg_inline('zeichen.svg'), zeichen3=svg_inline('zeichen.svg'), zeiger2=svg_inline('zeiger.svg'),
        gruppen=gr, welt_a=welt_tafel('a', WELTEN['a']), welt_b=welt_tafel('b', WELTEN['b']), abgr=abgr, rf=rf, pfeil=PFEIL,
        charakter=''.join('<li>%s</li>' % E(s) for s in TON['charakter']),
        eigene=' · '.join(E(w) for w in TON['eigene_worte']), nicht=' · '.join('<span class="nein">%s</span>' % E(w) for w in TON['nicht']),
        welt_saetze=''.join('<p class="gross" data-a>%s</p>' % E(s) for s in EIGENE_WELT['satz']), ud=ud)
    open(os.path.join(M, 'markenbuch.html'), 'w').write(seite('Markenbuch · Wirtschaft am Schlössli', body, MB_CSS, '.',
         'Markenbuch der Wirtschaft am Schlössli, Bottighofen: Zeichen, Wortmarke, Schrift, Farben, zwei Farbwelten, Ton und eigene Welt.'))


# ---------------------------------------------------------------- Probe: drei Stücke der künftigen Seite, getragen vom Horizont
PROBE_CSS = r'''
.hz{position:absolute;left:0;right:0;height:1px;background:var(--ak);opacity:.75;transform:scaleX(0);transform-origin:0 50%;transition:transform 1.6s var(--e1) .35s}
.da .hz,.hz.da{transform:scaleX(1)}
.pr{position:relative;padding:clamp(90px,10vw,140px) 0 clamp(110px,12vw,160px);overflow:hidden}
.pr .innen{max-width:1400px;position:relative}
.pr__g{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:clamp(28px,4.6vw,72px);align-items:start;position:relative}
.pr__bild{position:relative;margin:0;border-radius:var(--rund);overflow:hidden;box-shadow:0 60px 90px -50px rgba(0,0,0,.8)}
.pr__bild img{width:100%;aspect-ratio:3/2;object-fit:cover;transform:scale(1.06);transition:transform 2.4s var(--e1)}
.pr__bild.da img{transform:none}
.pr .hz{top:calc(var(--h-oben) + var(--h-bild) * .287)}
.pr__t{padding-top:calc(var(--h-bild) * .287 - 4.2em)}
.pr__t .z{width:44px;height:auto;color:var(--ak);margin-bottom:20px}
.pr__t .mono{color:var(--ak-h)}
.pr__t h1{font:400 clamp(1.7rem,3.1vw,2.9rem)/1.18 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:16px 0 34px;color:#F2F5F5;text-wrap:balance}
.pr__t h1 em{font-style:normal;color:var(--ak-titel)}
.pr__t p.l{margin:0 0 26px;color:rgba(238,242,242,.9);max-width:44ch}
.pr__u{display:flex;flex-direction:column;align-items:flex-end;margin:0 0 30px;max-width:44ch}
.pr__u q{font:400 1rem/1.4 var(--titel);text-transform:uppercase;letter-spacing:.14em;color:#F2F5F5;quotes:"«" "»";text-align:right}
.pr__u small{color:var(--ak-h);margin-top:8px}
.pr__k{display:flex;flex-wrap:wrap;gap:16px 26px;align-items:center}
.leise{font:400 11.5px/1 var(--mono);letter-spacing:.17em;text-transform:uppercase;text-decoration:none;border-bottom:1px solid var(--ak);padding-bottom:5px}
.dunkel .leise{color:#F2F5F5}
.mm{position:relative;padding:clamp(90px,10vw,140px) 0;overflow:hidden}
.mm__g{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(28px,5vw,80px);align-items:center;position:relative}
.mm .hz{background:var(--mittel);top:auto;bottom:clamp(150px,16vw,210px);opacity:.5}
.mm h2{font:400 clamp(1.6rem,3vw,2.6rem)/1.2 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:14px 0 22px;color:var(--titel-h)}
.mm h2 em{font-style:normal;color:var(--ak-t)}
.mm .mono{color:var(--ak-t)}
.mm .laender{display:flex;flex-wrap:wrap;gap:12px 28px;margin:30px 0 0;padding:0;list-style:none;font:400 .95rem/1.2 var(--titel);text-transform:uppercase;letter-spacing:.22em;color:var(--titel-h)}
.mm .laender li:nth-child(2){color:var(--ak-t)}
.mm figure{margin:0;position:relative;border-radius:var(--rund);overflow:hidden;box-shadow:0 50px 80px -50px rgba(0,0,0,.5)}
.mm figure img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 60%}
.mm figcaption{position:absolute;left:0;right:0;bottom:0;padding:70px 26px 22px;color:#fff;background:linear-gradient(transparent,rgba(0,0,0,.55))}
.mm figcaption b{display:block;font:400 1rem/1.2 var(--titel);text-transform:uppercase;letter-spacing:.2em}
.mm figcaption span{font-size:15px;opacity:.92}
.lm{position:relative;padding:clamp(90px,10vw,140px) 0 clamp(110px,12vw,150px);overflow:hidden}
.lm__g{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.3fr);gap:clamp(28px,5vw,80px);align-items:center}
.lm h2{font:400 clamp(1.6rem,3vw,2.6rem)/1.2 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:14px 0 22px;color:#F2F5F5}
.lm h2 em{font-style:normal;color:var(--ak-titel)}
.lm .mono{color:var(--ak-h)}
.lm .tapas{margin:26px 0 30px;padding:0;list-style:none;display:grid;gap:10px}
.lm .tapas li{display:flex;justify-content:space-between;gap:20px;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,.12)}
.lm .tapas b{font:400 .95rem/1.3 var(--titel);text-transform:uppercase;letter-spacing:.14em;font-weight:400}
.lm .tapas span{font-family:var(--mono);font-size:13px;color:var(--ak-h)}
.lm__b{display:grid;grid-template-columns:1.25fr 1fr;gap:14px;align-items:end}
.lm__b figure{margin:0;border-radius:var(--rund);overflow:hidden;box-shadow:0 50px 80px -50px rgba(0,0,0,.8)}
.lm__b img{width:100%;object-fit:cover}
.lm__b figure:first-child img{aspect-ratio:3/4}
.lm__b figure:last-child img{aspect-ratio:1/1}
.probe-wahl{position:fixed;right:16px;top:16px;z-index:9;display:flex;gap:6px;padding:6px;border-radius:30px;background:var(--nacht);box-shadow:0 14px 30px -14px rgba(0,0,0,.6),inset 0 0 0 1px color-mix(in srgb,var(--ak) 40%,transparent)}
.probe-wahl button{all:unset;cursor:pointer;padding:11px 16px;border-radius:24px;font:400 11px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:rgba(255,255,255,.82)}
.probe-wahl button[aria-pressed=true]{color:var(--ak-text);background:linear-gradient(180deg,var(--ak-h),var(--ak))}
.pfuss{padding:40px 0 110px;text-align:center;font-size:13.5px}
.pfuss p{opacity:.75;margin:0}
@media(max-width:900px){.pr__g,.mm__g,.lm__g{grid-template-columns:1fr}.pr__t{padding-top:0}.pr .hz{top:auto;bottom:clamp(60px,8vw,90px)}.pr__u{align-items:flex-start}.pr__u q{text-align:left}.mm .hz{bottom:60px}}
@media(max-width:520px){.probe-wahl{left:16px;right:16px;justify-content:center}.probe-wahl button{padding:11px 12px}}
'''

PROBE_JS = r'''<script>(function(){var g=document.querySelector('.pr__g'),b=document.querySelector('.pr__bild'),s=document.querySelector('.pr');
function setz(){var r=b.getBoundingClientRect(),q=s.getBoundingClientRect();s.style.setProperty('--h-bild',r.height+'px');s.style.setProperty('--h-oben',(r.top-q.top)+'px')}
setz();addEventListener('resize',setz);if(document.fonts)document.fonts.ready.then(setz);
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('da');io.unobserve(e.target)}})},{threshold:.2});
document.querySelectorAll('.hz').forEach(function(h){io.observe(h)})})()</script>'''


def probe():
    body = '''
<section class="pr dunkel" aria-label="Probe: Willkommen am Hafen"><span class="hz" aria-hidden="true"></span><div class="innen pr__g">
  <figure class="pr__bild" data-a><img src="bilder/terrasse-see.webp" alt="Blaue Stühle auf der Terrasse, dahinter der Bodensee und die Alpen"></figure>
  <div class="pr__t" data-a>
    %(zeiger)s
    <p class="mono">Seestrasse 50 · Bottighofen</p>
    <h1>Willkommen in der <em>Wirtschaft am Schlössli.</em></h1>
    <p class="l">Direkt im Hafen von Bottighofen gelegen mit Blick aufs Wasser und die Alpen.</p>
    <div class="pr__u"><q>Die schönste Terrasse am Bodensee</q><small class="mono">Christian Kuchler</small></div>
    <div class="pr__k"><a class="knopf" href="https://services.gastronovi.com/restaurants/118851/reservation/widget" target="_blank" rel="noopener">Tisch reservieren %(pfeil)s</a><a class="leise" href="markenbuch.html" data-mitwelt>Zum Markenbuch</a></div>
  </div>
</div></section>
<section class="mm blatt hell" aria-label="Probe: Die Karte"><span class="hz" aria-hidden="true"></span><div class="innen mm__g">
  <div data-a><p class="mono">Monika Huber · Küchenchefin</p><h2>Eine Reise in die Welt der <em>mediterranen Küche.</em></h2>
    <p>Die Speisekarte des Oktobers ist nach Ländern geordnet. Gekocht wird von einem jungen Küchenteam unter der Leitung von Monika Huber, ehemals Sous-Chefin von Christian Kuchler.</p>
    <ul class="laender"><li>Frankreich</li><li>Italien</li><li>Iberische Halbinsel</li><li>Klassiker</li></ul>
  </div>
  <figure data-a><img src="bilder/tortelloni.webp" alt="Tortelloni mit Tomate, Burrata und Taggiasca-Olive in einer gerippten Schale" loading="lazy"><figcaption><b>Tortelloni</b><span>Tomate – Burrata – Taggiasca Olive</span></figcaption></figure>
</div></section>
<section class="lm blatt dunkel" aria-label="Probe: Lästermeile"><div class="innen lm__g">
  <div data-a><p class="mono">An der Bar · den ganzen Tag</p><h2>Die <em>Lästermeile.</em></h2>
    <ul class="tapas"><li><b>Pimientos de Padrón</b><span>8</span></li><li><b>Croquetas</b><span>9</span></li><li><b>Kalamata Oliven</b><span>8</span></li><li><b>Prato</b><span>30</span></li></ul>
    <a class="knopf knopf--dunkel" href="https://www.schloessli-bottighofen.ch/s/Lastermeile-Homepage-2339.pdf" target="_blank" rel="noopener">Karte der Lästermeile %(pfeil)s</a>
  </div>
  <div class="lm__b" data-a><figure><img src="bilder/apero.webp" alt="Ein Spritz und ein Bier auf einem blauen Tisch am Abend über dem See" loading="lazy"></figure><figure><img src="bilder/bar.webp" alt="An der Bar wird ein Bier gezapft, unter der Theke die Zementfliesen" loading="lazy"></figure></div>
</div></section>
<footer class="pfuss dunkel"><p>Probe der Designidentität, Station 05 · Designstudie von Tasty Studios, nicht die offizielle Website · Fotos: Wirtschaft am Schlössli · Preise aus der Karte der Lästermeile, in Franken</p></footer>
''' % dict(zeiger=svg_inline('zeiger.svg', 'z'), pfeil=PFEIL)
    open(os.path.join(M, 'probe.html'), 'w').write(seite('Probe · Wirtschaft am Schlössli', body + PROBE_JS, PROBE_CSS, '.',
         'Drei Stücke der künftigen Seite in Titelschrift, Farbwelt, Knopf, Tapete und echten Fotos, getragen vom Horizont des Sees.'))


# ---------------------------------------------------------------- Logo richtig und falsch (Seite; Bilder macht aufnahme.js)
RF_CSS = r'''
.rfk{padding:clamp(60px,8vw,110px) 0}
.rfk .kopf h1{font:400 clamp(1.7rem,3.4vw,2.9rem)/1.16 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:14px 0 0;color:var(--titel-h)}
.rfk .kopf h1 em{font-style:normal;color:var(--ak-t)}
.rfg{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.karte{border-radius:20px;overflow:hidden;background:#fff;box-shadow:0 30px 50px -36px rgba(0,0,0,.45)}
.feld{aspect-ratio:4/3;display:grid;place-items:center;position:relative;overflow:hidden}
.feld img.logo{height:84%;width:auto}
.feld svg{height:62%;width:auto}
.text{padding:14px 16px 18px}
.text b{display:block;font:400 10.5px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;margin-bottom:6px}
.ja .text b{color:#2f6b55}.nein .text b{color:#a23a2c}
.text h2{font:400 1rem/1.3 var(--titel);text-transform:uppercase;letter-spacing:.14em;margin:0 0 6px}
.text p{margin:0;font-size:14.5px;line-height:1.45;color:#4b5456}
.schutz{width:44%;padding:2.46%;border:1px dashed color-mix(in srgb,var(--signal) 90%,#000)}
.schutz img{width:100%;height:auto;outline:1px solid rgba(0,0,0,.08)}
.mass{position:absolute;left:12px;bottom:10px;font:400 10px/1 var(--mono);letter-spacing:.1em;color:#57605f}
.klein{display:flex;align-items:flex-end;gap:26px;color:var(--tief)}
.kreuz::after{content:"";position:absolute;inset:14px;background:linear-gradient(to top right,transparent calc(50% - 1px),rgba(162,58,44,.55) calc(50% - 1px) calc(50% + 1px),transparent calc(50% + 1px))}
@media(max-width:900px){.rfg{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.rfg{grid-template-columns:1fr}}
'''


def logo_rf():
    z = svg_inline('zeichen.svg')
    L = '<img class="logo" src="../logo/logo-transparent-1563.png" alt="">'
    um = z.replace('fill="currentColor"', 'fill="#C2403A"', 1)
    felder = {
        'richtig-schwarz-auf-hell': '<div class="feld" style="background:#fff">%s</div>' % L,
        'richtig-zeichen-auf-dunkel': '<div class="feld dunkel" style="color:var(--ak)">%s</div>' % z,
        'richtig-schutzraum': '<div class="feld" style="background:var(--kalk)"><div class="schutz"><img src="../logo/logo-eng-zugeschnitten.png" alt=""></div><span class="mass">Abstand = eine Kugel</span></div>',
        'richtig-klein': '<div class="feld" style="background:var(--kalk)"><div class="klein"><span style="width:64px;display:block">%s</span><span style="width:36px;display:block">%s</span><span style="width:20px;display:block">%s</span></div><span class="mass">64 · 36 · 20 px</span></div>'
                         % (z.replace('<svg ', '<svg style="width:64px;height:auto" ', 1), z.replace('<svg ', '<svg style="width:36px;height:auto" ', 1), z.replace('<svg ', '<svg style="width:20px;height:auto" ', 1)),
        'falsch-verzerrt': '<div class="feld kreuz" style="background:#fff"><img src="../logo/logo-transparent-1563.png" alt="" style="width:86%;height:56%"></div>',
        'falsch-umgefaerbt': '<div class="feld kreuz" style="background:#fff;color:#1f6fb2">%s</div>' % um.replace('<svg ', '<svg style="filter:hue-rotate(160deg)" ', 1),
        'falsch-unruhig': '<div class="feld kreuz" style="background:url(../bilder/platanen.webp) center 30%/cover"><img class="logo" src="../logo/logo-eng-zugeschnitten.png" alt="" style="height:72%"></div>',
        'falsch-verstellt': '<div class="feld kreuz" style="background:var(--kalk)"><div style="height:62%;transform:rotate(-38deg);filter:drop-shadow(12px 16px 0 rgba(0,0,0,.4))">' + z.replace('<svg ', '<svg style="height:100%;width:auto" ', 1) + '</div></div>',
    }
    karten = ''.join('<article class="karte %s" id="%s" data-a>%s<div class="text"><b>%s</b><h2>%s</h2><p>%s</p></div></article>'
                     % (j, d, felder[d], 'Richtig' if j == 'ja' else 'Falsch', E(t), E(s)) for d, j, t, s in RF)
    body = '''<main class="rfk hell"><div class="innen">
<div class="kopf" data-a>%s<p class="mono">Logo richtig und falsch</p><h1>So steht das Logo, <em>so nicht.</em></h1>
<p>Das Logo wird nie nachgezeichnet, eingefärbt oder verzogen. Grundlage sind das Original in 1563 Pixeln und das daraus gezogene Zeichen ohne Schrift.</p></div>
<div class="rfg">%s</div>
<p class="mitte" style="text-align:center;margin-top:36px"><a class="knopf knopf--dunkel" href="../markenbuch.html#logo" data-mitwelt>Zurück zum Markenbuch %s</a></p>
</div></main>''' % (svg_inline('zeiger.svg', 'z'), karten, PFEIL)
    open(os.path.join(M, 'logo-richtig-falsch', 'index.html'), 'w').write(
        seite('Logo richtig und falsch · Wirtschaft am Schlössli', body, RF_CSS, '..', 'Regeln für das Logo der Wirtschaft am Schlössli.'))


# ---------------------------------------------------------------- marke.json
def marke_json():
    d = dict(
        farben=[dict(name=f['name'], hex=f['hex'], rolle=f['rolle'], belegt=f['belegt'], fundstelle=f['fundstelle'], auch=f['auch'],
                     foto=('marke/bilder/%s.webp' % f['foto']) if f['foto'] else (('marke/' + f['zeige']) if f.get('zeige') else None),
                     abgeleitet=toene(f['hex'])) for f in FARBEN],
        farbwelten=[dict(kennung=k, name=w['name'], satz=w['satz'], flaechen=[w['nacht'], w['tief'], w['mittel'], w['kalk'], w['kalk2']],
                         akzent=w['ak'], akzent_hell=w['ak_h'], akzent_tief=w['ak_t'], schrift=w['tinte'], punkt=w['signal'],
                         tapete=['marke/tapete-%s-dunkel.svg' % k, 'marke/tapete-%s-hell.svg' % k], probe='marke/probe.html' if k == 'a' else None,
                         gueltig=(k == 'a')) for k, w in WELTEN.items()],
        farbwelt_gewaehlt=dict(k='a', name=WELTEN['a']['name'], wort='Robert 19.10.2026: «schlössli a» (über den Chef-Chat Familie Kuchler)'),
        farbwelt_verworfen=dict(k='b', name=WELTEN['b']['name'], wo='marke/markenbuch.html#anhang'),
        schriften=[
            dict(rolle='titel', name='Open Sans', gewicht='400 · Name Versalien 0,3 em · Titel Versalien 0,16 em · Wortmarke gemessen 0,205 em', datei='marke/schriften/OpenSans-var.woff2',
                 quelle='Google Fonts (github.com/google/fonts, ofl/opensans), 19.10.2026', lizenz='SIL Open Font License 1.1 (marke/schriften/OFL-OpenSans.txt)',
                 abgeleitet_aus='Wortmarke: Deckung Buchstabe für Buchstabe 0,954 mit Open Sans 400, nächste andere von zehn freien Schriften (Source Sans 3) 0,878 (_bau/match.py)'),
            dict(rolle='lauf', name='Instrument Sans', datei='marke/schriften/InstrumentSans-normal-400_600.woff2', quelle='Werkbank-Kit (Google Fonts), über Späher 02', lizenz='SIL Open Font License 1.1'),
            dict(rolle='mono', name='DM Mono', datei='marke/schriften/DMMono-normal-400.woff2', quelle='Werkbank-Kit (Google Fonts), über Späher 02', lizenz='SIL Open Font License 1.1'),
            dict(rolle='heute-titel', name='Gilda Display', datei='marke/schriften/GildaDisplay-latin.woff2', quelle='Quelltext der heutigen Seite (Squarespace 2024), Späher 02', lizenz='SIL Open Font License 1.1'),
            dict(rolle='heute-lauf', name='PT Serif', datei=None, quelle='Quelltext der heutigen Seite (Squarespace 2024)', lizenz='SIL Open Font License 1.1, Datei nicht im Paket')],
        wortmarke=dict(datei='marke/logo/logo-transparent-1563.png', weitere=['marke/logo/logo-auf-mint-teilen-bild.jpeg'], art='png',
                       groesse='1563 × 1563 px, transparent (grösste gefundene Fassung, Seite des Schäfli /kontakt)', vektor=None,
                       abgeleitete_titelschrift='Open Sans 400 in Versalien',
                       schrift_der_wortmarke='Open Sans (Messung, nicht vom Haus bestätigt)'),
        zeichen=['marke/zeichen/zeichen.svg', 'marke/zeichen/zeiger.svg'],
        zeichen_quelle='_quelle/extern/logo/schloessli-logo-transparent.png: Buchstaben als eigene Flächen weggelassen, Rest mit potrace (_bau/zeichen.py)',
        tapete=dict(was='Feines Punktraster (die Kugeln der Zeiger) im Abstand 28 px, in der Mitte jedes Felds die Zeiger als Medaillon, Ton in Ton',
                    dateien=['marke/tapete-a-dunkel.svg', 'marke/tapete-a-hell.svg', 'marke/tapete-b-dunkel.svg', 'marke/tapete-b-hell.svg']),
        knopf=dict(form='Pille 54 px, DM-Mono-Versalien, rechts runder Knauf mit Pfeil in der Gegenfarbe (Master 2.6)',
                   tiefe='Verlauf in drei Stufen, Lichtkante oben, dunkle Kante unten, weicher Schatten; Glanzstreif beim Überfahren, hebt sich 2 px'),
        darstellungsidee='Der Horizont: eine feine Linie in der Linienfarbe läuft über die ganze Breite, genau auf der Höhe des Horizonts im Foto; Titel und Bild sitzen an ihr. Auf hellen Blättern läuft sie als Tischkante weiter.',
        bewegungsidee='Die Horizontlinie zieht sich beim Eintreten einmal von links nach rechts auf (nur transform), während das Foto von unten hereinschwebt und im Rahmen von 1,06 auf 1 zoomt.',
        ton=TON, welt='land', eigene_welt=EIGENE_WELT, familie_machart='Taverne zum Schäfli Wigoltingen (Markenbuch 19.10.2026, gleiche Machart, eigene Farben, Schrift und Zeichen)',
        seiten=dict(markenbuch='marke/markenbuch.html', probe='marke/probe.html', logo_richtig_falsch='marke/logo-richtig-falsch/index.html'),
        stand='19.10.2026, erster Durchgang ohne Blender, auf Farbwelt A veredelt')
    json.dump(d, open(os.path.join(H, 'marke.json'), 'w'), ensure_ascii=False, indent=1)


markenbuch(); probe(); logo_rf(); marke_json()
print('gebaut')
