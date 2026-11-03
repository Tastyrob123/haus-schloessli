#!/usr/bin/env python3
"""Das Markenbuch · Wirtschaft am Schlössli: die Hausregeln (buch.html und buch/), gebaut von bau.py.
Grundlage ist das bestätigte Markenbuch der Station 05 (Farbwelt A «Stuhl und See», _kette/05-markenbauer/marke/markenbuch.html, nur gelesen),
im Stand der Website: seit 19.10.2026 «Ton in Ton» (Blautöne um 21° auf das Blau des Platztellers gedreht, gleiche Drehung wie website/farbwelt.py,
im Bau nachgerechnet). Aufbau wie die Hausregeln des Culinarium (Leiste mit Weg zurück, Kapitel, «Als PDF sichern», Bewegung aus dem Kleid),
Inhalt vom Schlössli. Für den Kunden weggelassen: Arbeitsstand (Messstellen, Mediane, «belegt», abgeleitete Töne), die heutige Squarespace-Seite,
die verworfene Farbwelt, Vergleiche mit anderen Häusern, Wege zu Quellen. Dazu das Kapitel «Die Hausregeln» (zehn Regeln für jeden Text und jede
Drucksache, aus den Regeln der Hausdruckerei). «Als PDF sichern» öffnet das Druckfenster (A4 quer)."""
import hashlib, html, os, re, shutil

e = html.escape
HIER = os.path.dirname(os.path.abspath(__file__))

# Zehn Regeln des Hauses (Vorlage: Regeln der Hausdruckerei im Stand vom 22.10.2026, für das Markenbuch gefasst: Sie, ss, Versalien wie die Wortmarke,
# Betonung über Farbe, kein Hotel, Schwesterhaus nur als Verweis)
REGELN = [
    ('Sie, herzlich und unkompliziert', 'Das Haus siezt seine Gäste, herzlich und ohne Umstände, so wie es auf seiner Seite schreibt: «Mehr Wirtschaft, weniger feine Pinkel». Nie werblich laut.'),
    ('Schweizer Schreibung', 'Immer ss, nie das scharfe S; Anführungszeichen «…». Zeiten wie auf der Seite des Hauses: «Donnerstag - Montag», «11:30 Uhr - 23:00 Uhr».'),
    ('Titel in Versalien', 'Titel kurz, höchstens fünf Wörter, in gesperrten Versalien wie die Wortmarke, in Open Sans 400. Keine Ausrufezeichen im Titel.'),
    ('Betonung über Farbe', 'Betont wird mit Seehimmel auf Dunkel und Seehimmel tief auf Hell, nie fett und nie kursiv.'),
    ('Gerichte wie auf der Karte', 'Gerichte stehen so, wie sie auf der Karte stehen (THON, CAVATELLI, TORTELLONI), mit der Zeile darunter; nie übersetzt, nie geglättet.'),
    ('Preise nur auf den Karten', 'Preise stehen auf den Karten des Hauses. Aushänge, Einladungen und Beiträge nennen keine Preise.'),
    ('Dunkle Flächen mit Tapete', 'Nacht, Tief und Stuhlblau tragen die dunklen Flächen, immer mit dem Punktraster der Zeiger. Seehimmel nur für Zeichen, Linien und kleine Zeilen.'),
    ('Schirmrot nur als Punkt', 'Das Rot der Sonnenschirme steht höchstens als Punkt: eine Markierung, ein Stempel, nie als Fläche und nie als Schrift.'),
    ('Bilder vom Hafen', 'Fotos zeigen, was der Gast vorfindet: Hafen, Terrasse, See, Teller, Bar, Team. Ansichtskarten nur Hafen, Terrasse oder See, Titel ist der Ort.'),
    ('Eine Wirtschaft am Hafen', 'Das Haus heisst «Wirtschaft am Schlössli» und liegt direkt im Hafen von Bottighofen am Bodensee. Kein Hotel, keine Zimmer. Die Taverne zum Schäfli in Wigoltingen steht höchstens als Verweis auf das Schwesterhaus.'),
]

# Namen der Farbkarten im Markenbuch der Station 05 → Namen der Palette (Kleid): die Quelle «Seespiegel» der Station heisst hier nach dem Foto
UMBENENNEN_KARTE = {'Seespiegel': 'Wasser am Mittag'}
WELT_NAMEN = {'Fläche': 'Stuhlblau', 'Hell': 'Papier', 'Hell 2': 'Seespiegel', 'Linie': 'Seehimmel', 'Schrift': 'Tinte', 'Punkt': 'Schirmrot'}


def kw(t):
    """Beschriftung der Knöpfe in eigenem span (Tor WebKit 3.11.2026: text-box statt festem Versatz)."""
    return re.sub(r'(<(?:a|span) class="knopf[^"]*"[^>]*>)\s*([^<]+?)\s*(<span class="kn">)', r'\1<span class="kw">\2</span>\3', t)


def _v(n):
    p = os.path.join(HIER, n)
    return hashlib.sha1(open(p, 'rb').read()).hexdigest()[:10] if os.path.exists(p) else '1'


def ohne_internes(s):
    """Keine Arbeitswege im Kundenbuch. Dateipfade der Quellen werden zu Worten."""
    s = s.replace('Grund der Seite, gemessen vom Späher · _kette/02-spaeher/befund.md', 'Grund der heutigen Seite, gemessen')
    s = s.replace('_kette/02-spaeher/befund.md; Bild: Aufnahme des Spähers _qa/spaeher/start-rechner-voll.jpg, 18.10.2026', 'Aufnahme der heutigen Seite, 18.10.2026')
    s = s.replace('_kette/02-spaeher/befund.md; Bild: ebd.', 'Aufnahme der heutigen Seite, ebd.')
    s = re.sub(r'_quelle/extern/logo/[^ ,<(]+', 'Logo des Hauses', s)
    s = re.sub(r'_quelle/website/bilder/[^ ,<]+', 'Foto der Website', s)
    return s


def weg(s, muster, n=1):
    s2, k = re.subn(muster, '', s, flags=re.S)
    if k != n and not (n == 0 and k >= 1):
        raise SystemExit(f'Hausregeln: Muster «{muster[:60]}» {k}× statt {n}×, erst klären')
    return s2


def ersetze(s, alt, neu, n=1):
    k = s.count(alt)
    if k != n:
        raise SystemExit(f'Hausregeln: «{alt[:70]}» {k}× statt {n}×, erst klären')
    return s.replace(alt, neu)


def fuer_den_kunden(s, gedreht, daten):
    """Arbeitsstand raus, Farben im Stand der Website, Ton ohne Interna, Kapitel «Die Hausregeln» dazu."""
    dreh = lambda m: gedreht(m.group(0)).upper()
    # Farben: nur, was eine Farbe des Hauses erklärt; Töne im Stand der Website (Ton in Ton), ohne Messstellen und Mediane
    i = s.index('id="farben"'); j = s.index('</section>', i)
    f = s[i:j]
    f = re.sub(r'<div class="gruppe"><h3 data-a>Das Logo</h3>.*?</article></div>', '', f, count=1, flags=re.S)
    f = re.sub(r'<div class="gruppe"><h3 data-a>Die heutige Seite</h3>.*?</article></div>(?=\s*</div>\s*$|<div class="gruppe">|\s*$)', '', f, count=1, flags=re.S)
    f = re.sub(r'<article class="fz" data-a>(?:(?!</article>).)*<h3>Platanenlaub</h3>.*?</article>', '', f, count=1, flags=re.S)
    f = re.sub(r'<p class="fz__q fz__auch">.*?</p>', '', f, flags=re.S)
    f = re.sub(r'<div class="fz__s"[^>]*>.*?</div>', '', f, flags=re.S)
    f = re.sub(r'<p class="fz__ab mono">.*?</p>', '', f, flags=re.S)
    f = re.sub(r' · belegt: [^<]*', '', f)
    f = re.sub(r'(<p class="fz__q">[^<]*?) · (?:Foto der Website|Logo des Hauses)[^<]*', r'\1', f)
    f = re.sub(r'#[0-9A-Fa-f]{6}\b', dreh, f)
    for a, b in UMBENENNEN_KARTE.items():
        f = f.replace(f'<h3>{a}</h3>', f'<h3>{b}</h3>')
    f = re.sub(r'(<h2>Jede Farbe mit dem Foto, <em>aus dem sie kommt\.</em></h2>\s*<p>).*?(</p>)',
               r'\1Jede Farbe des Hauses ist in einem Foto des Hauses gefunden: an den Stühlen der Terrasse, am See, an den Sonnenschirmen, am Teller, '
               r'an den Fliesen der Bar. Die Blautöne stehen so, wie die Website sie trägt: Ton in Ton auf das Blau des Platztellers gestimmt.\2', f, count=1, flags=re.S)
    s = s[:i] + f + s[j:]
    if 'Die heutige Seite' in s[i:i + len(f)]:
        raise SystemExit('Hausregeln: Gruppe «Die heutige Seite» steht noch drin')
    # Schrift: ohne die Schriften der heutigen Seite, ohne Dateiwege
    s = weg(s, r'\s*<div class="heute-schrift" data-a>.*?</div>\s*</div>(?=\s*</div></section>)')
    s = re.sub(r' Datei: marke/schriften/[^ ]+ · ', ' ', s)
    s = ersetze(s, '<p class="mono" style="color:var(--ak-t);margin-top:6px">Startseite heute</p>', '<p class="mono" style="color:var(--ak-t);margin-top:6px">Die Karte</p>')
    # Zeichen: ohne die Herkunft der Logo-Dateien (Seite des Schwesterhauses, Teilen-Bild der heutigen Seite)
    s = weg(s, r'\s*<div class="herkunft">.*?</div>(?=\s*</div></section>)')
    # Farbwelt: ohne Wahl, Namen der Palette
    s = ersetze(s, '<p class="mono">Farbwelt · gewählt</p>', '<p class="mono">Die Farbwelt des Hauses</p>')
    s = ersetze(s, 'Ohne Gold und ohne die Farben des Schäfli, damit man die zwei Häuser der Familie auf den ersten Blick auseinanderhält. ', 'Ohne Gold und ohne Grün. ')
    for a, b in WELT_NAMEN.items():
        s = ersetze(s, f'<b>{a}</b>', f'<b>{b}</b>')
    s = s.replace('zwei Farbwelten, ', 'Farbwelt, ')
    # Ton: «Nicht bei uns» ohne Vermerke zur heutigen Seite
    nein = ' · '.join(f'<span class="nein">{e(x)}</span>' for x in daten['ton']['nicht'])
    s, n_ = re.subn(r'(<h3>Nicht bei uns</h3><p>).*?(</p>)', lambda m: m.group(1) + nein + m.group(2), s, count=1, flags=re.S)
    if not n_:
        raise SystemExit('Hausregeln: «Nicht bei uns» nicht gefunden')
    # Kapitel «Die Hausregeln»
    z = re.search(r'<svg class="z".*?</svg>', s, re.S).group(0)
    regeln = ''.join(f'<li data-a><span class="hr__n mono">{n:02d}</span><h3>{e(t).rsplit(" ", 1)[0] + "&nbsp;" + e(t).rsplit(" ", 1)[1] if " " in t else e(t)}</h3><p>{e(x)}</p></li>' for n, (t, x) in enumerate(REGELN, 1))
    kap = (f'<section class="blatt matt" id="regeln"><div class="innen">\n  <div class="kopf" data-a>{z}<p class="mono">Die Hausregeln</p>'
           f'<h2>Zehn Regeln für <em>jeden Text.</em></h2>\n  <p>Für jeden Aushang, jede Karte, jeden Beitrag und jede Mail des Hauses, ob aus dem Team oder von einer Agentur.</p></div>\n'
           f'  <ol class="hr">{regeln}</ol>\n</div></section>\n\n')
    s = ersetze(s, '<section class="blatt hell welt" id="welt">', kap + '<section class="blatt hell welt" id="welt">')
    css = ('<style>.hr{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}'
           '.hr li{position:relative;background:#fff;border-radius:var(--rund);padding:clamp(22px,2.6vw,32px) clamp(22px,2.6vw,34px) clamp(22px,2.6vw,30px) clamp(64px,6vw,84px);box-shadow:0 30px 50px -40px rgba(0,0,0,.4)}'
           '.hr li::before{content:"";position:absolute;left:0;right:0;top:0;height:3px;border-radius:var(--rund) var(--rund) 0 0;background:var(--ak)}'
           '.hr__n{position:absolute;left:clamp(22px,2.6vw,34px);top:clamp(26px,2.9vw,36px);color:var(--ak-t)}'
           '.hr h3{font:400 clamp(.98rem,1.25vw,1.12rem)/1.3 var(--titel);text-transform:uppercase;letter-spacing:.14em;color:var(--titel-h);margin:0 0 10px;text-wrap:balance}'
           '.hr p{margin:0;font-size:16px;line-height:1.62;color:var(--tinte)}'
           '@media(max-width:760px){.hr{grid-template-columns:1fr}}</style>')
    s = s.replace('</head>', css + '</head>', 1)
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
    # nicht gebraucht: das Teilen-Bild der heutigen Seite, Schriften der heutigen Seite
    for n in ('logo-auf-mint-teilen-bild.jpeg',):
        p = os.path.join(ziel, 'logo', n)
        if os.path.exists(p):
            os.remove(p)
    for n in os.listdir(os.path.join(ziel, 'schriften')):
        if n.startswith(('Gilda', 'PT')):
            os.remove(os.path.join(ziel, 'schriften', n))
    for n in ('heute-knoepfe.webp', 'heute-text.webp'):
        p = os.path.join(ziel, 'bilder', n)
        if os.path.exists(p):
            os.remove(p)
    dreh = lambda m: (lambda h: h.upper() if m.group(0)[1:].isupper() else h)(gedreht(m.group(0)))

    def stil(t):
        return re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + re.sub(r'#[0-9a-fA-F]{6}\b', dreh, m.group(2)) + m.group(3), t, flags=re.S)

    s = open(os.path.join(st5, 'markenbuch.html'), encoding='utf-8').read()
    s = stil(s)
    s = re.sub(r'(<section[^>]*id="farbwelten".*?</section>)', lambda m: re.sub(r'#[0-9a-fA-F]{6}\b', dreh, m.group(1)), s, flags=re.S)
    s = re.sub(r'\s*<div class="abgrenzung" data-a>.*?</div></div></div>(?=\s*</div>\s*</section>|\s*</section>)', '', s, count=1, flags=re.S)
    s = re.sub(r'<a class="knopf" href="probe\.html">.*?</a>', '', s, flags=re.S)
    s = s.replace('Schirmrot nur als Punkt. Ohne Gold und ohne die Farben des Schäfli, damit man die zwei Häuser der Familie auf den ersten Blick auseinanderhält.',
                  'Schirmrot nur als Punkt. Ohne Gold und ohne die Farben des Schäfli, damit man die zwei Häuser der Familie auf den ersten Blick auseinanderhält. '
                  'Seit dem 19. Oktober 2026 trägt die Website die Farbwelt «Ton in Ton»: alle Blautöne um 21° auf das Blau des Platztellers gedreht, die warmen Töne bleiben.')
    s = s.replace(' Worin sie sich von den bisherigen Häusern unterscheidet, steht darunter, Haus für Haus.', '')
    s = ohne_internes(s)
    s = re.sub(r'\s*<div class="ud" data-a>.*?</div>\s*(?=</div>\s*</section>)', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<section class="blatt matt anhang" id="anhang">.*?</section>', '', s, flags=re.S)
    s = fuer_den_kunden(s, gedreht, daten)
    name = daten['namen']['marke']
    s = re.sub(r'<footer class="fuss dunkel">.*?</footer>',
               f'<footer class="fuss dunkel"><div class="innen"><p>Die Hausregeln der Wirtschaft am Schlössli · Stand {e(daten["stand"]["datum"])}</p>'
               f'<p>Fotos und Logo: Wirtschaft am Schlössli. Alle Dateien der Marke unter <a href="./#dateien">Logo &amp; Dateien</a>.</p></div></footer>', s, flags=re.S)
    s = ersetze(s, 'Markenbuch · Bottighofen am Bodensee', 'Die Hausregeln · Bottighofen am Bodensee')
    s = ersetze(s, 'alles hier ist am Haus gemessen.', 'alles hier kommt vom Haus.')
    # Wege der Dateien
    s = re.sub(r'(src|href)="(\./)?(bilder|logo|zeichen|logo-richtig-falsch)/', r'\1="buch/\3/', s)
    s = s.replace('url(./schriften/', 'url(buch/schriften/').replace('url(./tapete-', 'url(buch/tapete-')
    # Leiste oben: zurück ins Werkzeug, Kapitel, Als PDF sichern (Knopf des Hauses: Nacht, DM Mono, heller Knauf)
    kap = [(m.group(1), re.sub(r'<[^>]+>', '', m.group(2))) for m in re.finditer(r'<section class="(?:blatt|kapitel)[^"]*" id="([a-z]+)">.*?<p class="mono">([^<]*)</p>', s, re.S)]
    zu = re.sub(r'^Das ', 'zum ', name) if name.startswith('Das ') else 'zu ' + name
    pfeil = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v10M3.5 7.5 8 12l4.5-4.5M3 14h10"/></svg>'
    leiste = ('<nav class="lb-leiste" aria-label="Die Hausregeln"><a class="lb-zur" href="./" title="Zurück ' + e(zu) + '"><img src="dateien/wirtschaft-am-schloessli-zeiger-himmel.svg" alt="" width="26" height="26"><span><b>' + e(name) + '</b><small>Die Hausregeln</small></span></a><span class="lb-kap">'
              + ''.join(f'<a href="#{k}">{e(t)}</a>' for k, t in kap) + '</span><button type="button" id="bu-pdf"><span>Als PDF sichern</span><i>' + pfeil + '</i></button></nav>')
    s = re.sub(r'(<section class=")blatt\b', r'\1kapitel', s)
    s = re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + re.sub(r'\.blatt\b', '.kapitel', m.group(2)) + m.group(3), s, flags=re.S)
    s = s.replace('<body', '<body data-livre', 1)
    s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + leiste, s, count=1)
    css = ('<style>.lb-leiste{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:18px;min-height:64px;padding:8px clamp(14px,2.4vw,32px);'
           'background:var(--tap-d,none) 0 0/168px,#0b1d3d;color:#e9eef3;font:400 10.5px/1 "DM Mono",ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;'
           'box-shadow:0 1px 0 rgba(162,182,207,.22)}.lb-leiste a{color:inherit;text-decoration:none}'
           '.lb-zur{display:flex;align-items:center;gap:12px;flex:none}.lb-zur img{width:26px;height:26px}.lb-zur span{display:flex;flex-direction:column;gap:5px}'
           '.lb-zur b{font:400 12px/1 "Open Sans",Arial,sans-serif;letter-spacing:.2em}.lb-zur small{font-size:9.5px;color:#A2B6CF}'
           '.lb-kap{flex:1;display:flex;justify-content:center;gap:2px;flex-wrap:wrap}.lb-kap a{padding:7px 9px;border-radius:999px;color:rgba(233,238,243,.78)}'
           '.lb-kap a:hover{color:#fff;background:rgba(162,182,207,.14)}'
           '#bu-pdf{flex:none;display:inline-flex;align-items:center;gap:12px;height:44px;padding:0 5px 0 20px;border:0;border-radius:999px;cursor:pointer;'
           'font:inherit;letter-spacing:inherit;text-transform:inherit;color:#fff;background:#113d88;box-shadow:inset 0 0 0 1px rgba(162,182,207,.35)}'
           '#bu-pdf span{text-box:trim-both cap alphabetic}#bu-pdf i{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#E7ECF3;color:#0b1d3d}'
           '#bu-pdf svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}'
           '@media (max-width:620px){.lb-zur small{display:none}.lb-zur b{font-size:11px}#bu-pdf{width:44px;padding:0;justify-content:center}#bu-pdf span{display:none}#bu-pdf i{width:34px;height:34px}}@media (max-width:1679px){.lb-kap{display:none}.lb-leiste{justify-content:space-between}}.lb-kap{flex-wrap:nowrap}'
           'h1,h2,h3,h4,figcaption{text-wrap:balance}'
           '@page{size:A4 landscape;margin:10mm}@media print{.lb-leiste{display:none}[data-a]{opacity:1!important;transform:none!important}'
           '.kapitel,.auftakt,.fuss{-webkit-print-color-adjust:exact;print-color-adjust:exact}.kapitel{break-before:page}.kapitel{padding:34px 0 26px;margin-top:0;border-radius:0}.auftakt{min-height:0;padding:90px 0}.kopf{margin-bottom:24px}.fz,.wt,.wv,figure,.zg__gross,.zg__fass,.gruppe>p,.ton li,.hr li{break-inside:avoid}.mitte:has(.knopf){display:none}.fuss{break-before:avoid;padding:24px 0}}</style>')
    s = re.sub(r'<link rel="icon"[^>]*>', '', s)
    s = s.replace('</head>', css + '<link rel="icon" href="/assets/oberflaeche/kleid/schloessli-zeichen.svg" type="image/svg+xml"></head>', 1)
    # Tor 3.11.2026: Schrift im Knopf optisch mittig (1,3 px tiefer), Pfeil im Knauf mittig; Titel nie mit einem Wort allein in der letzten Zeile
    s = s.replace('</head>', '<style>.knopf>.kw{text-box:trim-both cap alphabetic}.knopf .pf{translate:1px 0}@supports (interpolate-size:allow-keywords){.knopf>.kw{translate:0 0px}}</style>' + '</head>', 1)
    s = kw(s)
    s = re.sub(r'(<figcaption>)([^<]*)(</figcaption>)', lambda m: m.group(1) + re.sub(r' (?=\S+\s*$)', '&nbsp;', m.group(2), count=1) + m.group(3), s)
    s = ersetze(s, '<h2>Der Name in weit <em>gesperrten Versalien.</em></h2>', '<h2>Der Name, <em>weit gesperrt.</em></h2>')
    def zus(t):   # letzte zwei Wörter zusammen, wenn sie zusammen kurz genug für eine Handyzeile sind
        m = re.search(r'(\S+) ([^ <>]+(?:</em>)?\s*)$', t)
        if not m:
            m2 = re.search(r'(\S+) (<em>[^ <]+</em>\s*)$', t)
            return t[:m2.start()] + m2.group(1) + '&nbsp;' + m2.group(2) if m2 and len(re.sub(r'<[^>]+>', '', m2.group(1) + m2.group(2))) <= 15 else t
        return t[:m.start()] + m.group(1) + '&nbsp;' + m.group(2) if m and len(re.sub(r'<[^>]+>', '', m.group(1) + m.group(2))) <= 15 else t
    s = re.sub(r'(<(h2|h3)\b[^>]*>)(.*?)(</\2>)', lambda m: m.group(1) + zus(m.group(3)) + m.group(4), s, flags=re.S)
    s = re.sub(r'<title>[^<]*</title>', '<title>Die Hausregeln · Wirtschaft am Schlössli</title>', s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Die Hausregeln der Wirtschaft am Schlössli, Bottighofen: Zeichen, Wortmarke, Schrift, Farben, Farbwelt, Logo richtig und falsch, Ton, zehn Regeln für jeden Text.">', s, count=1)
    # Bewegung des Kleids (Robert 1.11.2026: auch auf den Hausregeln): das Kleid lädt bewegung.js nach
    s = s.replace('</body>', f'<script src="/assets/oberflaeche/kleid/schloessli.js?v={_v("../oberflaeche/kleid/schloessli.js")}"></script><script src="buch.js?v={_v("buch.js")}"></script></body>', 1)
    sichtbar = re.sub(r'<(style|script)[^>]*>.*?</\1>|<[^>]+>', ' ', s, flags=re.S)
    for w in ('Platzhalter', 'Station 0', 'Tasty', 'probe.html', 'Welt B', 'belegt', 'Median', 'Ausschnitt x', 'Squarespace', 'gewählt', 'abgeleitete Töne',
              'Bildarchiv', 'Hausbuch', 'ß', 'Hotel ', 'Culinarium', '_quelle/', '_kette/', 'Späher', 'heutige Seite', 'heutigen Seite'):
        if w in sichtbar:
            i_ = sichtbar.index(w); raise SystemExit(f'Hausregeln: «{w}» steht noch drin: …{sichtbar[max(0, i_ - 90):i_ + 60]}…')
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
    # Logo richtig und falsch: dieselbe Seite der Station 05, gedreht, Weg zurück in die Hausregeln
    r = open(os.path.join(st5, 'logo-richtig-falsch', 'index.html'), encoding='utf-8').read()
    r = stil(r).replace('../markenbuch.html', '../../buch.html')
    r = re.sub(r'(Station 05[^<]*|Designstudie von Tasty Studios[^<]*)', '', r)
    r = r.replace('Zurück zum Markenbuch', 'Zurück zu den Hausregeln').replace('Markenbuch', 'Die Hausregeln').replace('MARKENBUCH', 'DIE HAUSREGELN')
    r = re.sub(r'<title>[^<]*</title>', '<title>Logo richtig und falsch · Wirtschaft am Schlössli</title>', r, count=1)
    r = re.sub(r'<link rel="icon"[^>]*>', '<link rel="icon" href="/assets/oberflaeche/kleid/schloessli-zeichen.svg" type="image/svg+xml">', r, count=1)
    r = re.sub(r'(<h2>)([^<]*)(</h2>)', lambda m: m.group(1) + re.sub(r' (?=\S+$)', '&nbsp;', m.group(2), count=1) + m.group(3), r)
    r = r.replace('</head>', '<style>.knopf>.kw{text-box:trim-both cap alphabetic}.knopf .pf{translate:1px 0}@supports (interpolate-size:allow-keywords){.knopf>.kw{translate:0 0px}}</style>' + '<style>.mass{left:16px}</style></head>', 1)
    r = kw(r)
    lg = Image.open(os.path.join(ziel, 'logo', 'logo-transparent-1563.png'))
    lg.resize((1563, round(1563 / 1.786)), Image.LANCZOS).save(os.path.join(ziel, 'logo-richtig-falsch', 'falsch-verzerrt-logo.png'), optimize=True)
    alt_ = '<img src="../logo/logo-transparent-1563.png" alt="" style="width:86%;height:56%">'
    if r.count(alt_) != 1:
        raise SystemExit('Logo richtig und falsch: verzerrtes Logo nicht gefunden')
    r = r.replace(alt_, '<img src="falsch-verzerrt-logo.png" alt="" style="width:86%;height:auto;aspect-ratio:1.786">')
    open(os.path.join(ziel, 'logo-richtig-falsch', 'index.html'), 'w', encoding='utf-8').write(r)
    return [k for k, t in kap]
