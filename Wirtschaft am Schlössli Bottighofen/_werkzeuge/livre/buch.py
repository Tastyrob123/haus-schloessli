#!/usr/bin/env python3
"""Das Hausbuch (Le Livre) · Wirtschaft am Schlössli: das Markenbuch zum Arbeiten (buch.html), gebaut von bau.py aus denselben Daten wie livre.json.
Grundlage ist das bestätigte Markenbuch der Station 05 (Farbwelt A «Stuhl und See», _kette/05-markenbauer/marke.json), mit dem Stand der Website heute:
seit 19.10.2026 «Ton in Ton» (Blautöne auf das Blau des Platztellers gedreht). Fotos nur Originale des Hauses (Website des Hauses), keine erzeugten Bilder,
keine Gästefotos. Kapitel: Haus · Zeichen · Logo und Name · Farben (Herkunft im Foto gemessen, Kontraste) · Schriften · Tapete · Bilder · Ton.
«Als PDF sichern» öffnet das Druckfenster (je Kapitel eine A4-Seite quer). Nichts von Hand gemessen: Töne, Abstände und Kontraste rechnet der Bau."""
import hashlib, html, os

e = html.escape
HIER = os.path.dirname(os.path.abspath(__file__))


def lum(h):
    def k(c):
        c /= 255; return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = (int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)); return .2126 * k(r) + .7152 * k(g) + .0722 * k(b)


def kontrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)


def urteil(r):
    return 'sehr gut, auch für langen Text' if r >= 7 else 'gut für Lesetext' if r >= 4.5 else 'nur für grosse Zeilen' if r >= 3 else 'nur Schmuck, nie Schrift'


PAARE = [('tinte', 'papier', 'Lesetext auf Papier'), ('tinte', 'kalk', 'Lesetext auf Kalk'), ('titel-h', 'kalk', 'Titel auf Kalk'),
         ('himmel-t', 'kalk', 'Betonung im Titel auf Kalk'), ('stuhl', 'papier', 'Knöpfe und Linien auf Papier'), ('papier', 'nacht', 'Schrift auf Nacht'),
         ('himmel', 'nacht', 'Linie und Betonung auf Nacht'), ('punkt', 'kalk', 'Schirmrot auf Kalk')]
NAME = {'nacht': 'Nacht, für helle Flächen', 'stuhl': 'Stuhlblau, für helle Flächen', 'himmel': 'Seehimmel, für dunkle Flächen', 'weiss': 'Weiss, für dunkle Flächen',
        'schwarz': 'Schwarz wie das Original'}
TAPETE = {'dunkel': 'Auf Nacht · Seehimmel, Ton in Ton', 'hell': 'Auf Kalk · Stuhlblau, Ton in Ton'}
BILDER = ['start', 'platanen', 'tortelloni', 'bar', 'team', 'abend']


def _v(n):
    p = os.path.join(HIER, n)
    return hashlib.sha1(open(p, 'rb').read()).hexdigest()[:10] if os.path.exists(p) else '1'


def baue(daten, herkunft, messe, img, BJ, MJ):
    F = {f['k']: f for f in daten['farben']}
    D = {g['k']: g for g in daten['dateien']}
    S = 'wirtschaft-am-schloessli'
    v = lambda n: f'dateien/{S}-{n}'
    gr_ = lambda k: f'{k}-{max(BJ[k]["breiten"])}.webp'
    kl_ = lambda k: f'{k}-{max([b for b in BJ[k]["breiten"] if b <= 800] or [min(BJ[k]["breiten"])])}.webp'
    alt = lambda k: BJ[k]['alt']
    kap = []

    def kapitel(nr, k, titel, satz, inhalt, dunkel=False):
        d = ' bu-k--d' if dunkel else ''
        kap.append(f'<section class="bu-k{d}" id="{k}"><header class="bu-k__h"><span class="bu-k__nr">{nr:02d}</span><h2>{titel}</h2><p>{e(satz)}</p></header>{inhalt}</section>')

    def tafel(x, datei=None):
        return f'<figure class="bu-tafel bu-tafel--{x["grund"]}"><img src="dateien/{datei or x["dateien"][0]}" alt=""><figcaption>{e(NAME.get(x["k"], x["k"]))}</figcaption></figure>'

    welt = MJ['eigene_welt']['satz']
    # 1 Haus
    kapitel(1, 'haus', 'Das <em>Haus</em>', welt[0],
            f'<div class="bu-zwei"><figure class="bu-foto"><img src="../../assets/img/{kl_("start")}" alt="{e(alt("start"))}" loading="lazy"></figure>'
            f'<div class="bu-text"><p>{e(welt[2].split(" Worin")[0])}</p>'
            '<ul class="bu-liste"><li>Die Zeiger als einziges Zeichen, der Name in weit gesperrten Versalien</li>'
            '<li>Stuhlblau und Seehimmel, Ton in Ton auf das Blau des Platztellers, Schirmrot nur als Punkt</li>'
            '<li>Echte Fotos vom Hafen, von der Terrasse, den Tellern und dem Team</li></ul></div></div>')
    # 2 Zeichen
    zt = ''.join(tafel(x) for x in D['zeichen']['var'])
    zg = ''.join(tafel(x) for x in D['zeiger']['var'] if x['k'] in ('nacht', 'himmel'))
    z = v('zeichen-nacht.svg')
    kapitel(2, 'zeichen', 'Ein Kreis, zwei <em>Zeiger</em>',
            'Das Zeichen kommt aus dem Logo des Hauses: ein offener Kreis, zwei Zeiger mit Rauten, zwei Kugeln. Die Buchstaben sind weggelassen, der Rest ist nachgezeichnet und bleibt in jeder Grösse scharf. Die Zeiger allein stehen als Medaillon in der Tapete und als Zeichen in der Leiste der Website.',
            f'<div class="bu-zeichen"><div class="bu-schutz bu-tafel--dunkel"><img src="{v("zeichen-himmel.svg")}" alt="Das Zeichen in Seehimmel">'
            '<small>Auf Nacht in Seehimmel oder Weiss, auf Hell in Nacht oder Stuhlblau</small></div>'
            f'<div class="bu-tafeln">{zt}{zg}</div></div>'
            f'<div class="bu-nie"><figure><img src="{z}" alt="" style="transform:rotate(-14deg)"><figcaption>nicht drehen</figcaption></figure>'
            f'<figure><img src="{z}" alt="" style="transform:scaleX(1.5)"><figcaption>nicht verzerren</figcaption></figure>'
            f'<figure><img src="{z}" alt="" style="filter:invert(.6) sepia(1) saturate(9) hue-rotate(10deg)"><figcaption>nicht umfärben</figcaption></figure></div>')
    # 3 Logo und Name
    lg = ''.join(tafel(x) for x in D['logo']['var'])
    kapitel(3, 'logo', 'Logo und <em>Name</em>',
            'Das Logo bleibt, wie das Haus es hat: der Kreis mit den Zeigern, das Ö als Nabe, SCHLÖSSLI, WIRTSCHAFT und BY CHRISTIAN KUCHLER. Es liegt nur als Bild vor, nicht als Vektor; hier ist es Pixel für Pixel das Original, nur umgefärbt. Der Name steht in Open Sans, der Schrift der Wortmarke, in weit gesperrten Versalien.',
            '<div class="bu-logos">' + lg
            + f'<figure class="bu-tafel bu-tafel--hell bu-tafel--breit"><img src="{v("name-nacht.svg")}" alt="WIRTSCHAFT AM SCHLÖSSLI in Open Sans"><figcaption>Der Name in Versalien, 0,3 em gesperrt</figcaption></figure>'
            + f'<figure class="bu-tafel bu-tafel--dunkel"><img src="{v("name-kurz-himmel.svg")}" alt="SCHLÖSSLI"><figcaption>Kurz</figcaption></figure>'
            + f'<figure class="bu-tafel bu-tafel--hell"><img src="{v("logo-website-heute.jpg")}" alt="Logo auf der heutigen Website"><figcaption>So zeigt es die heutige Website beim Teilen</figcaption></figure></div>')
    # 4 Farben
    gr = ''
    for g in daten['gruppen']:
        fs = [f for f in daten['farben'] if f['g'] == g['k']]
        if not fs:
            continue
        zellen = ''
        for f in fs:
            woher = f'<small class="bu-woher">{e(f["woher"])}</small>' if f.get('woher') else ''
            zellen += (f'<figure class="bu-farbe"><span style="background:{f["h"]}"></span><figcaption><b>{e(f["n"])}</b><code>{f["h"]}</code>'
                       f'<small>RGB {" · ".join(map(str, f["rgb"]))}</small><small>{e(f["r"])}</small>{woher}</figcaption></figure>')
        gr += f'<div class="bu-gruppe"><h3>{e(g["n"])}</h3><p>{e(g["s"])}</p><div class="bu-farben">{zellen}</div></div>'
    her = ''
    for key, titel, satz, toene in herkunft:
        p = os.path.join(img, f'{key}-1200.webp' if os.path.exists(os.path.join(img, f'{key}-1200.webp')) else gr_(key))
        punkte = [(n, h) + messe(p, h) for n, h in toene]
        lupen = ''.join(f'<span class="bu-lupe" style="left:{x}%;top:{y}%;--c:{g}"><i>{e(n)}</i></span>' for n, h, g, d, x, y in punkte)
        zeilen = ''.join(f'<li><span style="background:{h}"></span><b>{e(n)} {h.upper()}</b><small>im Foto gemessen {g.upper()}, Abstand ΔE {str(d).replace(".", ",")}</small></li>'
                         for n, h, g, d, x, y in punkte)
        her += (f'<figure class="bu-her"><div class="bu-her__b"><img src="../../assets/img/{kl_(key)}" alt="{e(titel)}" loading="lazy">{lupen}</div>'
                f'<figcaption><b>{e(titel)}</b><p>{e(satz)}</p><ul>{zeilen}</ul></figcaption></figure>')
    paare = ''
    for a, b, t in PAARE:
        r = kontrast(F[a]['h'], F[b]['h'])
        paare += (f'<li><span class="bu-paar" style="background:{F[b]["h"]};color:{F[a]["h"]}">Aa</span><b>{e(F[a]["n"])} auf {e(F[b]["n"])}</b>'
                  f'<small>{e(t)} · {f"{r:.1f}".replace(".", ",")} : 1 · {urteil(r)}</small></li>')
    kapitel(4, 'farben', 'Stuhl, See und <em>Platzteller</em>',
            'Die Farbwelt A «Stuhl und See» aus dem Markenbuch, so wie die Website sie heute trägt: seit dem 19.10.2026 Ton in Ton, alle Blautöne um 21° auf das Blau des Platztellers gedreht. Keiner steht von Hand hier, sie kommen aus der Gestaltung der Website (assets/css/haus.css).',
            gr + '<h3 class="bu-zw">Wo die Farben herkommen</h3><p class="bu-satz">Jeder Ton des Markenbuchs ist in einem Foto des Hauses gesucht: die Stelle, deren Mittel ihm am nächsten liegt, mit dem Abstand nach CIEDE2000 (unter 5 gilt als gleich).</p>'
            + '<div class="bu-hers">' + her + '</div><h3 class="bu-zw">Was sich lesen lässt</h3><ul class="bu-paare">' + paare + '</ul>')
    # 5 Schriften
    sch = ''.join(f'<li class="bu-schrift"><span class="bu-schrift__p f-{s["k"]}">{e(s["p"])}</span><b>{e(s["n"])}</b><small>{e(s["r"])} · {e(s["e"])}</small></li>' for s in daten['schriften'])
    kapitel(5, 'schriften', 'Open Sans trägt die <em>Titel</em>', 'Open Sans in gesperrten Versalien für Titel und Namen, Instrument Sans für den Lesetext, DM Mono für kleine Angaben und Knöpfe, Caveat für einzelne Wörter in Handschrift. Die Probezeilen sind Sätze des Hauses.',
            f'<ul class="bu-schriften">{sch}</ul>')
    # 6 Tapete
    tap = ''.join(f'<figure class="bu-tapete bu-tafel--{x["grund"]}" style="background-image:url(dateien/{x["dateien"][2]})"><figcaption>{e(TAPETE[x["k"]])}</figcaption></figure>' for x in D['tapete']['var'])
    kapitel(6, 'tapete', 'Punkte und <em>Zeiger</em>',
            'Ein feines Punktraster, die Kugeln der Zeiger, im Abstand von 28 Punkten; in der Mitte jedes Felds die Zeiger als Medaillon, Ton in Ton. Es liegt auf den dunklen und hellen Flächen der Website. Nie ein freies Motiv.',
            '<div class="bu-tapeten">' + tap + f'<figure class="bu-tapete bu-tapete--foto"><img src="{v("zeiger-nacht.svg")}" alt="Die Zeiger"><figcaption>Das Vorbild: die Zeiger des Logos</figcaption></figure></div>')
    # 7 Bilder
    kapitel(7, 'bilder', 'Hafen, Platanen und ein <em>Horizont</em>', MJ['darstellungsidee'],
            '<div class="bu-bilder">' + ''.join(f'<figure><img src="../../assets/img/{kl_(k)}" alt="{e(alt(k))}" loading="lazy"></figure>' for k in BILDER) + '</div>'
            '<ul class="bu-liste bu-liste--zwei"><li>Fotos des Hauses, nichts aus Bilddatenbanken</li><li>Frei lizenzierte Fotos nur mit Namen und Lizenz</li>'
            '<li>Gästefotos und Bilder von Partnern nur mit deren Erlaubnis</li><li>Erzeugte Bilder nur als Platzhalter und beschriftet</li></ul>', dunkel=True)
    # 8 Ton
    worte = ''.join(f'<li>{e(w)}</li>' for w in MJ['ton']['eigene_worte'][:8])
    nicht = ''.join(f'<li>{e(w)}</li>' for w in MJ['ton']['nicht'][:7])
    kapitel(8, 'ton', 'Wie das Haus <em>spricht</em>', 'Herzlich, unkompliziert, konkret. Sie-Form, Schweizer Schreibung mit ss. Kurze Sätze, lieber eine Angabe als ein Adjektiv.',
            f'<div class="bu-ton"><div><h3>Worte des Hauses</h3><ul class="bu-liste">{worte}</ul></div>'
            f'<div><h3>Nicht bei uns</h3><ul class="bu-liste bu-liste--nein">{nicht}</ul></div></div>')
    inhalt = ''.join(f'<a href="#{k}">{t}</a>' for k, t in (('haus', 'Haus'), ('zeichen', 'Zeichen'), ('logo', 'Logo'), ('farben', 'Farben'), ('schriften', 'Schriften'),
                                                             ('tapete', 'Tapete'), ('bilder', 'Bilder'), ('ton', 'Ton')))
    zh = v('zeiger-himmel.svg')
    open(os.path.join(HIER, 'buch.html'), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Markenbuch · Wirtschaft am Schlössli</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['nacht']['h']}">
<link rel="icon" href="{v('zeiger-nacht.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="buch.css?v={_v('buch.css')}">
</head>
<body class="bu">
<header class="bu-kopf"><a class="bu-kopf__m" href="./"><img src="{zh}" alt=""><span><b>Markenbuch</b><small>Wirtschaft am Schlössli · {daten['namen']['marke']}</small></span></a>
<nav class="bu-inhalt" aria-label="Kapitel">{inhalt}</nav><button class="bu-pdf" type="button" id="bu-pdf">Als PDF sichern</button></header>
<section class="bu-titel"><img src="{zh}" alt=""><h1>Wirtschaft am <em>Schlössli</em></h1><p>Markenbuch · Bottighofen · Direkt im Hafen · Stand {e(daten['stand']['datum'])}</p></section>
<main>{''.join(kap)}</main>
<footer class="bu-fuss"><p>Gebaut aus dem bestätigten Markenbuch (Farbwelt A «Stuhl und See») und der Website des Hauses. Farben aus der Gestaltung der Seite, Töne in den Fotos gemessen, Dateien unter <a href="./#dateien">Logo &amp; Dateien</a>.</p></footer>
<script src="buch.js?v={_v('buch.js')}"></script>
</body>
</html>
''')


# ---------------------------------------------------------------- Das Markenbuch des Hauses (seit 19.10.2026, Robert: «noch ein bisschen schöner, so wie die anderen Markenbücher auch»)
# Grundlage ist das bestätigte Markenbuch der Station 05 (_kette/05-markenbauer/marke/markenbuch.html, nur gelesen), in derselben Machart wie die
# Markenbücher der anderen Häuser: Farbkarten mit dem Foto, aus dem die Farbe kommt, grosse Logo-Tafeln, «So steht das Logo, so nicht», Kapitel im Wechsel
# dunkel und hell. Angepasst an den Stand der Website: Rahmen und Farbwelt «Ton in Ton» (gleiche Drehung wie website/farbwelt.py, im Bau nachgerechnet),
# die gemessenen Töne der Fotos bleiben wie gemessen. Für das Haus weggelassen: die verworfene Wahl, der Vergleich mit den anderen Häusern, die Paletten
# des Schwesterhauses, der Hinweis auf die Probe-Seite und die Zeile zur Kette. Bilder: nur Originale des Hauses (Ausschnitte aus den Fotos der Website).
import re, shutil



def ohne_internes(s):
    """Demo-Check 21.10.2026: keine Arbeitswege im Kundenbuch (Fehlerbuch 10a: nichts zu Station und Kette). Dateipfade der Quellen werden zu Worten."""
    s = s.replace('Grund der Seite, gemessen vom Späher · _kette/02-spaeher/befund.md', 'Grund der heutigen Seite, gemessen')
    s = s.replace('_kette/02-spaeher/befund.md; Bild: Aufnahme des Spähers _qa/spaeher/start-rechner-voll.jpg, 18.10.2026', 'Aufnahme der heutigen Seite, 18.10.2026')
    s = s.replace('_kette/02-spaeher/befund.md; Bild: ebd.', 'Aufnahme der heutigen Seite, ebd.')
    s = re.sub(r'_quelle/extern/logo/[^ ,<(]+', 'Logo des Hauses', s)
    s = re.sub(r'_quelle/website/bilder/[^ ,<]+', 'Foto der Website', s)
    return s

def aus_station5(st5, web, gedreht, daten):
    """st5 = Ordner marke/ der Station 05, web = website/. Schreibt buch.html und buch/ (Bilder, Logo, Zeichen, Schriften, Tapeten, Logo richtig und falsch)."""
    ziel = os.path.join(HIER, 'buch')
    if os.path.isdir(ziel):
        shutil.rmtree(ziel)
    for d in ('bilder', 'logo', 'zeichen', 'schriften', 'logo-richtig-falsch'):
        shutil.copytree(os.path.join(st5, d), os.path.join(ziel, d))
    for n in ('tapete-a-dunkel.svg', 'tapete-a-hell.svg'):                      # die gedrehten Tapeten der Website
        shutil.copyfile(os.path.join(web, 'assets', 'svg', n), os.path.join(ziel, n))
    for n in ('tapete-b-dunkel.svg', 'tapete-b-hell.svg'):
        shutil.copyfile(os.path.join(st5, n), os.path.join(ziel, n))
    dreh = lambda m: (lambda h: h.upper() if m.group(0)[1:].isupper() else h)(gedreht(m.group(0)))
    def stil(t):
        return re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + re.sub(r'#[0-9a-fA-F]{6}\b', dreh, m.group(2)) + m.group(3), t, flags=re.S)

    s = open(os.path.join(st5, 'markenbuch.html'), encoding='utf-8').read()
    s = stil(s)
    # Farbwelt A so, wie die Website sie heute trägt
    s = re.sub(r'(<section[^>]*id="farbwelten".*?</section>)', lambda m: re.sub(r'#[0-9a-fA-F]{6}\b', dreh, m.group(1)), s, flags=re.S)
    s = re.sub(r'\s*<div class="abgrenzung" data-a>.*?</div></div></div>(?=\s*</div>\s*</section>|\s*</section>)', '', s, count=1, flags=re.S)
    s = re.sub(r'<a class="knopf" href="probe\.html">.*?</a>', '', s, flags=re.S)
    s = s.replace('Schirmrot nur als Punkt. Ohne Gold und ohne die Farben des Schäfli, damit man die zwei Häuser der Familie auf den ersten Blick auseinanderhält.',
                  'Schirmrot nur als Punkt. Ohne Gold und ohne die Farben des Schäfli, damit man die zwei Häuser der Familie auf den ersten Blick auseinanderhält. '
                  'Seit dem 19. Oktober 2026 trägt die Website die Farbwelt «Ton in Ton»: alle Blautöne um 21° auf das Blau des Platztellers gedreht, die warmen Töne bleiben.')
    # die eigene Welt ohne den Vergleich mit anderen Häusern, ohne Anhang
    s = s.replace(' Worin sie sich von den bisherigen Häusern unterscheidet, steht darunter, Haus für Haus.', '')
    s = ohne_internes(s)
    s = re.sub(r'\s*<div class="ud" data-a>.*?</div>\s*(?=</div>\s*</section>)', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<section class="blatt matt anhang" id="anhang">.*?</section>', '', s, flags=re.S)
    s = re.sub(r'<footer class="fuss dunkel">.*?</footer>',
               f'<footer class="fuss dunkel"><div class="innen"><p>Markenbuch der Wirtschaft am Schlössli · Stand {e(daten["stand"]["datum"])}</p>'
               f'<p>Fotos und Logo: Wirtschaft am Schlössli. Alle Dateien der Marke unter <a href="./#dateien">Logo &amp; Dateien</a>.</p></div></footer>', s, flags=re.S)
    # Wege der Dateien
    s = re.sub(r'(src|href)="(\./)?(bilder|logo|zeichen|logo-richtig-falsch)/', r'\1="buch/\3/', s)
    s = s.replace('url(./schriften/', 'url(buch/schriften/').replace('url(./tapete-', 'url(buch/tapete-')
    # Leiste oben: zurück ins Werkzeug, Kapitel, Als PDF sichern (im Stil des Buchs: Nacht, DM Mono, Knopf mit Knauf)
    name = daten['namen']['marke']
    kap = [(m.group(1), re.sub(r'<[^>]+>', '', m.group(2))) for m in re.finditer(r'<section class="blatt[^"]*" id="([a-z]+)">.*?<p class="mono">([^<]*)</p>', s, re.S)]
    leiste = ('<nav class="lb-leiste" aria-label="Markenbuch"><a class="lb-zur" href="./">' + e(name) + '</a><span class="lb-kap">'
              + ''.join(f'<a href="#{k}">{e(t)}</a>' for k, t in kap) + '</span><button type="button" id="bu-pdf">Als PDF sichern</button></nav>')
    s = s.replace('<body', '<body data-livre', 1)
    s = re.sub(r'(<body[^>]*>)', r'\1' + leiste.replace('\\', r'\\'), s, count=1)
    css = ('<style>.lb-leiste{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:18px;min-height:56px;padding:8px clamp(14px,2.4vw,32px);'
           'background:var(--tap-d,none) 0 0/168px,#0b1d3d;color:#e9eef3;font:400 10.5px/1 "DM Mono",ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;'
           'box-shadow:0 1px 0 rgba(162,182,207,.22)}.lb-leiste a{color:inherit;text-decoration:none}.lb-zur::before{content:"\\2190  "}'
           '.lb-kap{flex:1;display:flex;justify-content:center;gap:4px;flex-wrap:wrap}.lb-kap a{padding:6px 9px;border-radius:999px;color:rgba(233,238,243,.78)}'
           '.lb-kap a:hover{color:#fff;background:rgba(162,182,207,.14)}#bu-pdf{flex:none;height:36px;padding:0 16px;border:0;border-radius:999px;cursor:pointer;'
           'font:inherit;letter-spacing:inherit;text-transform:inherit;color:#0b1d3d;background:linear-gradient(180deg,#f3f6f9,#c5d2e1);'
           'box-shadow:inset 0 1px 0 #fff,inset 0 -2px 0 rgba(4,16,35,.18),0 8px 16px -10px #000}'
           '@media (max-width:900px){.lb-kap{display:none}.lb-leiste{justify-content:space-between}}'
           '@page{size:A4 landscape;margin:10mm}@media print{.lb-leiste{display:none}[data-a]{opacity:1!important;transform:none!important}'
           '.blatt,.auftakt,.fuss{-webkit-print-color-adjust:exact;print-color-adjust:exact}.blatt{break-before:page}.blatt{padding:34px 0 26px;margin-top:0;border-radius:0}.auftakt{min-height:0;padding:90px 0}.kopf{margin-bottom:24px}.fz,.wt,.wv,figure,.zg__gross,.zg__fass,.gruppe>p,.ton li{break-inside:avoid}.mitte:has(.knopf){display:none}.fuss{break-before:avoid;padding:24px 0}}</style>')
    s = s.replace('</head>', css + '<link rel="icon" href="dateien/wirtschaft-am-schloessli-zeiger-nacht.svg" type="image/svg+xml"></head>', 1)
    s = re.sub(r'<title>[^<]*</title>', '<title>Markenbuch · Wirtschaft am Schlössli</title>', s, count=1)
    s = s.replace('</body>', f'<script src="buch.js?v={_v("buch.js")}"></script></body>', 1)
    open(os.path.join(HIER, 'buch.html'), 'w', encoding='utf-8').write(s)

    # Beispielbilder «richtig»: Petrol auf das Blau des Platztellers gedreht wie die Website (die «falsch»-Bilder zeigen den Fehler und bleiben)
    import numpy as np
    from PIL import Image
    for n in os.listdir(os.path.join(ziel, 'logo-richtig-falsch')):
        if not (n.startswith('richtig-') and n.endswith('.png')):
            continue
        p = os.path.join(ziel, 'logo-richtig-falsch', n)
        im = Image.open(p); alpha = im.getchannel('A') if im.mode == 'RGBA' else None
        hsv = np.asarray(im.convert('RGB').convert('HSV')).astype(np.int16)
        grad = hsv[..., 0] * 360 / 255
        m = (grad >= 185) & (grad <= 212) & (hsv[..., 1] > 15)
        hsv[..., 0] = np.where(m, (hsv[..., 0] + round(21 * 255 / 360)) % 256, hsv[..., 0])
        neu = Image.fromarray(hsv.astype('uint8'), 'HSV').convert('RGB')
        if alpha is not None:
            neu.putalpha(alpha)
        neu.save(p, optimize=True)
    # Logo richtig und falsch: dieselbe Seite der Station 05, gedreht, Weg zurück ins Markenbuch des Werkzeugs
    r = open(os.path.join(st5, 'logo-richtig-falsch', 'index.html'), encoding='utf-8').read()
    r = stil(r).replace('../markenbuch.html', '../../buch.html')
    r = re.sub(r'(Station 05[^<]*|Designstudie von Tasty Studios[^<]*)', '', r)
    open(os.path.join(ziel, 'logo-richtig-falsch', 'index.html'), 'w', encoding='utf-8').write(r)
    return [k for k, t in kap]
