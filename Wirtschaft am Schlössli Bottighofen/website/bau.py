# Wirtschaft am Schlössli · statischer Bau der ganzen Website (Station 07, 19.10.2026).
# Inhalte liegen nur in inhalt/ (haus.json, karte.json, laestermeile.json, lunch.json, bankett.json, wein.json, bilder.json);
# Kopf, Leiste, Fuss und Fenster gibt es einmal hier. Rechtstexte kommen im Wortlaut aus _quelle/website/text/.
# Lauf: python3 karten_lesen.py && python3 bilder.py && python3 bau.py
import json, html, re, pathlib, hashlib

HIER = pathlib.Path(__file__).resolve().parent
Q = HIER.parent / '_quelle'
I = HIER / 'inhalt'
HAUS = json.loads((I / 'haus.json').read_text())
KARTE = json.loads((I / 'karte.json').read_text())
LM = json.loads((I / 'laestermeile.json').read_text())
LUNCH = json.loads((I / 'lunch.json').read_text())
BANKETT = json.loads((I / 'bankett.json').read_text())
WEIN = json.loads((I / 'wein.json').read_text())
B = json.loads((I / 'bilder.json').read_text())
RES = 'https://services.gastronovi.com/restaurants/118851/reservierung/widget'
# Gäste-Funktionen (Runde 3): Weindaten zuerst schreiben, dann die Bausteine laden
import funktionen_daten
(HIER / 'assets' / 'data').mkdir(parents=True, exist_ok=True)
(HIER / 'assets' / 'data' / 'weine.json').write_text(json.dumps(funktionen_daten.weine(), ensure_ascii=False, separators=(',', ':')))
import funktionen as F
import fuss_bau


def e(s):
    return html.escape(str(s), quote=True)


def version(datei):
    return hashlib.md5((HIER / datei).read_bytes()).hexdigest()[:8]


PFEIL = '<span class="kn"><svg class="pf" viewBox="0 0 16 10" aria-hidden="true"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span>'
KREUZ = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13" fill="none"/></svg>'


def zeichen(h=32):
    """Zeichen des Hauses (Zeiger im Kreis aus dem Logo), Farbe über currentColor."""
    s = (HIER / 'assets/svg/zeichen.svg').read_text()
    return s.replace('<svg ', f'<svg class="zeichen" aria-hidden="true" style="height:{h}px;width:auto" ', 1)


def zeiger(h=34):
    s = (HIER / 'assets/svg/zeiger.svg').read_text()
    return s.replace('<svg ', f'<svg aria-hidden="true" style="height:{h}px;width:auto" ', 1)


def knopf(text, href='#', dunkel=False, klein=False, attr=''):
    k = 'knopf' + (' knopf--dunkel' if dunkel else '') + (' knopf--klein' if klein else '')
    return f'<a class="{k}" href="{e(href)}"{attr}>{e(text)} {PFEIL}</a>'


def srcset(n):
    return ', '.join(f'assets/img/{n}-{w}.webp {w}w' for w in B[n]['breiten'])


def img(n, sizes, eager=False, alt=None, cls=''):
    b = B[n]
    a = e(alt if alt is not None else b['alt'])
    gr = b['breiten'][min(1, len(b['breiten']) - 1)]
    c = f' class="{cls}"' if cls else ''
    if eager:
        return f'<img{c} src="assets/img/{n}-{gr}.webp" srcset="{srcset(n)}" sizes="{sizes}" width="{b["w"]}" height="{b["h"]}" alt="{a}" fetchpriority="high" decoding="async">'
    return f'<img{c} data-src="assets/img/{n}-{gr}.webp" data-srcset="{srcset(n)}" sizes="{sizes}" width="{b["w"]}" height="{b["h"]}" alt="{a}" decoding="async">'


def foto(n, sizes, cls='', r=True, eager=False, alt=None, stil=''):
    rr = ' data-r="bild"' if r else ''
    st = f'background-image:url({B[n]["abbild"]});{stil}'
    return f'<figure class="foto {cls}"{rr} style="{st}">{img(n, sizes, eager, alt)}</figure>'


def nw(n, kl='', tag='p'):
    """Namensnennung für freie Bilder (Wikimedia Commons), steht klein unter dem Foto."""
    x = B[n].get('nachweis')
    if not x:
        return ''
    return f'<{tag} class="nachweis {kl}">Foto: <a href="{e(x["quelle"])}" rel="noopener" target="_blank">{e(x["urheber"])}</a>, {e(x["lizenz"])}, {e(x["jahr"])}</{tag}>'


def anl(n, sizes, cls='', hz=None):
    """Ruhender Rahmen mit der Linie auf dem Horizont des Fotos; nur das Foto darin bewegt sich (Anlegen)."""
    h = hz if hz is not None else B[n]['hz']
    rcht = 'hz--links' if 'ab__bild' in cls else 'hz--rechts'
    return f'<div class="anl {cls}" style="--hz:{h}"><span class="hz {rcht}" aria-hidden="true"></span>{foto(n, sizes)}{nw(n)}</div>'


# ---------------------------------------------------------------- Rahmen: Kopf, Leiste, Menü, Fenster, Fuss
NAV = [('karte.html', 'Karte'), ('weinkarte.html', 'Weinkarte'), ('karte.html#laestermeile', 'Lästermeile'), ('feiern.html', 'Feiern'),
       ('anlaesse.html', 'Events'), ('team.html', 'Team'), ('kontakt.html', 'Kontakt')]


def kopf(titel, beschreibung, seite, vorladen=''):
    can = 'https://www.schloessli-bottighofen.ch/' + ('' if seite == 'index.html' else seite.replace('.html', ''))
    return f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
<meta name="robots" content="noindex">
<link rel="canonical" href="{can}">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschreibung)}">
<meta property="og:image" content="assets/img/start-1200.webp">
<meta property="og:locale" content="de_CH">
<meta name="theme-color" content="#0b1d3d">
<link rel="icon" href="assets/svg/zeiger.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/OpenSans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
{vorladen}<link rel="stylesheet" href="assets/css/haus.css?v={version('assets/css/haus.css')}"><link rel="stylesheet" href="assets/css/fuss.css?v={version('assets/css/fuss.css')}">
<link rel="stylesheet" href="assets/css/funktionen.css?v={version('assets/css/funktionen.css')}">
<script>document.documentElement.classList.add('js');if('scrollRestoration' in history&&!location.hash)history.scrollRestoration='manual'</script>
</head>
<body data-seite="{seite.replace('.html', '')}">
<a class="vh" href="#inhalt">Zum Inhalt</a>
'''


# Speisefolge (Leiste Fassung 66, Robert 20.10.2026): das Menü der Website als Karte. Die Überzeilen sagen sachlich, was man dort findet,
# aus den Angaben des Hauses (Robert 20.10.2026: Gänge-Metapher «passt nicht»); Karte zuerst, Lästermeile nach dem Wein.
def _speisefolge():
    z, b = HAUS['zeiten'], HAUS['bankett']
    koch = next((t['name'] for t in HAUS['team'] if 'Küchenchef' in t['rolle']), '')
    an = next((a for a in HAUS['anlaesse'] if a.get('bevorstehend')), None)
    weine = len(json.loads((HIER / 'assets' / 'data' / 'weine.json').read_text()))
    return [('Mittag und Abend · à la carte', 'Die Karte', 'karte.html'), (f'{weine} Weine', 'Weinkarte', 'weinkarte.html'),
            ('Tapas den ganzen Tag', 'Lästermeile', 'karte.html#laestermeile'),
            (f"{b['etagen']} Etagen · je bis {b['personen']} Gäste", 'Feiern', 'feiern.html'),
            (f"Als Nächstes {an['datum'].rsplit(' ', 1)[0]}" if an else 'Anlässe am Hafen', 'Events', 'anlaesse.html'),
            (f'Küche von {koch}' if koch else 'Küche und Service', 'Das Team', 'team.html'), ('Anlass, Menü und Wein', 'Ihr Abend', 'abend.html'),
            (f"{z['tage'].replace(' - ', ' bis ')} · {z['offen'].replace(' Uhr', '').replace(' - ', ' bis ')}", 'Tisch reservieren', None),
            ('Zum Verschenken', 'Gutschein', 'gutschein.html'), ('Anfahrt und Telefon', 'Kontakt', 'kontakt.html')]


SPEISEFOLGE = _speisefolge()


def leiste(seite):
    def gang(i, g):
        was, name, h = g
        attr = f'href="{e(RES)}" data-fenster="fe-reservation" class="sf__g sf__g--tisch"' if h is None else f'href="{h}" class="sf__g"{" aria-current=\"page\"" if h == seite else ""}'
        return f'<a {attr} style="--i:{i + 4}"><span class="z"><b>{e(name)}</b></span></a>'  # ohne Überzeilen (Robert 20.10.2026: «viel zu unübersichtlich»)
    gaenge = ''.join(gang(i, g) for i, g in enumerate(SPEISEFOLGE))
    return f'''<header class="leiste leiste--sf">
  <a class="lz" href="index.html" aria-label="{e(HAUS['name'])}, Startseite">{zeiger(32)}</a>
  <button class="sf-taste" type="button" data-sf-auf aria-haspopup="dialog" aria-label="Menü öffnen"><i></i>Menü<i></i></button>
  <div class="ecke ecke--r">{knopf('Reservation', RES, dunkel=True, klein=True, attr=' data-fenster="fe-reservation"')}</div>
</header>
<div class="sf" role="dialog" aria-modal="true" aria-label="Menü" aria-hidden="true">
  <div class="sf__grund" data-sf></div>
  <div class="sf__karte"><div class="sf__blatt">
    <button class="sf__zu" type="button" data-sf aria-label="Menü schliessen">{KREUZ}</button>
    <p class="sf__haus z" style="--i:0"><span>{e(HAUS['name'])}</span></p>
    <h2 class="sf__titel z" style="--i:1"><span>Menü</span></h2>
    <div class="sf__zeichen z" style="--i:2"><span>{zeiger(24)}</span></div>
    <p class="sf__datum z" style="--i:3"><span data-heute>{e(HAUS['strasse'])} · {e(HAUS['ort'])}</span></p>
    <nav aria-label="Hauptmenü">{gaenge}</nav>
    <p class="sf__fuss z" style="--i:{len(SPEISEFOLGE) + 4}"><span>{e(HAUS['strasse'])} · {e(HAUS['ort'])} · <a href="tel:{e(HAUS['telefon_href'])}">{e(HAUS['telefon'])}</a></span></p>
  </div></div>
</div>
'''


def fenster_dialoge():
    zu = ','.join(f'{a}/{b}' for a, b in HAUS['ferien_iso'])
    zeiten = ''.join(f'<button type="button" data-v="{h:02d}:{m:02d} Uhr">{h:02d}:{m:02d} Uhr</button>' for h in range(11, 22) for m in (0, 30) if (h, m) >= (11, 30))
    form = ''.join(f'<button type="button" data-v="{e(v)}">{e(v)}</button>' for v in HAUS['bankett']['speisenform'])
    return F.reservation_dialog() + f'''<dialog class="fe" id="fe-bankett" aria-label="Bankettanfrage">
  <div class="fe__kopf2"><h2>Bankettanfrage</h2><button class="fe__zu" type="button" aria-label="Schliessen">{KREUZ}</button></div>
  <div class="fe__inhalt">
    <form class="fe__form" novalidate>
      <p>{e(HAUS['bankett']['fett'])} {e(HAUS['bankett']['rahmen'])}</p>
      <div class="felder">
        <div class="feld" data-wahl="datum" data-kal data-zu="{zu}"><span>Datum</span><button class="wahl-k" type="button" aria-expanded="false"><span>Tag wählen</span></button><div class="wahl-l"></div><input type="hidden" name="datum"></div>
        <div class="feld" data-wahl="uhrzeit"><span>Uhrzeit</span><button class="wahl-k" type="button" aria-expanded="false"><span>Uhrzeit wählen</span></button><div class="wahl-l">{zeiten}</div><input type="hidden" name="uhrzeit"></div>
        <div class="feld"><label for="b-pers">Personenzahl</label><input id="b-pers" name="personen" inputmode="numeric" autocomplete="off" required></div>
        <div class="feld" data-wahl="speisenform"><span>Gewünschte Speisenform</span><button class="wahl-k" type="button" aria-expanded="false"><span>{e(HAUS['bankett']['speisenform'][0])}</span></button><div class="wahl-l">{form}</div><input type="hidden" name="speisenform" value="{e(HAUS['bankett']['speisenform'][0])}"></div>
        <div class="feld"><label for="b-gaenge">Anzahl Gänge</label><input id="b-gaenge" name="gaenge" inputmode="numeric" autocomplete="off"></div>
        <div class="feld"><label for="b-budget">Richt-Budget für Speisen bzw. insgesamt</label><input id="b-budget" name="budget" autocomplete="off"></div>
        <div class="feld"><label for="b-name">Name</label><input id="b-name" name="name" autocomplete="name" required></div>
        <div class="feld"><label for="b-kontakt">Gerne bin ich erreichbar via</label><input id="b-kontakt" name="kontakt" autocomplete="email" required></div>
        <div class="feld feld--ganz"><label for="b-text">Welches Gericht darf auf keinen Fall fehlen, welche Allergien müssen bedacht werden?</label><textarea id="b-text" name="text"></textarea></div>
      </div>
      <div class="fe__senden">{'<button class="knopf knopf--dunkel" type="submit">Anfrage senden ' + PFEIL + '</button>'}</div>
      <p class="fe__hinweis">Ihre Angaben verwenden wir nur für diese Anfrage. Designstudie: In diesem Entwurf wird nichts verschickt.</p>
    </form>
    <div class="fe__danke"><h3>Vielen Dank.</h3><p>{e(HAUS['bankett']['individuell'])}</p><p class="fe__hinweis">Designstudie: Diese Anfrage wurde nicht verschickt.</p></div>
  </div>
</dialog>
<dialog class="fe" id="fe-gutschein" aria-label="Gutschein">
  <div class="fe__kopf2"><h2>Gutschein</h2><button class="fe__zu" type="button" aria-label="Schliessen">{KREUZ}</button></div>
  <div class="fe__inhalt">
    <form class="fe__form" novalidate>
      <div class="felder">
        <div class="feld"><label for="g-name">Name Käufer</label><input id="g-name" name="name" autocomplete="name" required></div>
        <div class="feld"><label for="g-mail">E-Mail</label><input id="g-mail" name="mail" type="email" autocomplete="email" required></div>
        <div class="feld feld--ganz"><label for="g-adresse">Adresse</label><input id="g-adresse" name="adresse" autocomplete="street-address" required></div>
        <div class="feld"><label for="g-betrag">Betrag in Franken</label><input id="g-betrag" name="betrag" inputmode="numeric" autocomplete="off" required></div>
      </div>
      <div class="fe__senden"><button class="knopf knopf--dunkel" type="submit">Gutschein bestellen {PFEIL}</button></div>
      <p class="fe__hinweis">Designstudie: In diesem Entwurf wird nichts verschickt.</p>
    </form>
    <div class="fe__danke"><h3>Vielen Dank.</h3><p>{e(HAUS['gutschein']['bestaetigung'])}.</p><p class="fe__hinweis">Designstudie: Diese Bestellung wurde nicht verschickt.</p></div>
  </div>
</dialog>
'''


def fuss():
    # Fassung 5 «Hell am Mittag» (Robert 19.10.2026), Bau in fuss_bau.py, Gestaltung assets/css/fuss.css. Alter Fuss: _sicherung/bau.py.vor-fuss5-*
    return fuss_bau.fuss(HAUS, RES, knopf, e)


def ende():
    return f'''{fenster_dialoge()}{F.wein_dialog()}<script src="assets/js/haus.js?v={version('assets/js/haus.js')}" defer></script>
<script src="assets/js/fuss.js?v={version('assets/js/fuss.js')}" defer></script>
<script src="assets/js/funktionen.js?v={version('assets/js/funktionen.js')}" defer></script>
</body>
</html>
'''


# Weg zur nächsten Seite (Robert 20.10.2026: «… quasi in einem Gang durchgehen kann und nicht oben mal dieses Menü zwischendurch wieder öffnen muss»).
# Eine Quelle: dieselbe Liste wie das Menü (SPEISEFOLGE), davor die Startseite. Jede Seite endet vor dem Fuss mit «Als Nächstes».
WEG_BILD = {'index.html': 'teller', 'karte.html': 'thon', 'weinkarte.html': 'wein', 'karte.html#laestermeile': 'bar', 'feiern.html': 'gaststube',
            'anlaesse.html': 'excellence-schiff', 'team.html': 'team', 'abend.html': 'tb-glas', None: 'platanen', 'gutschein.html': 'torte', 'kontakt.html': 'haus'}


def weg(datei):
    gang = [('Startseite', 'index.html')] + [(n, h) for _, n, h in SPEISEFOLGE]
    stellen = [i for i, (_, h) in enumerate(gang) if h and h.split('#')[0] == datei]
    if not stellen:
        return ''
    def ziel(i):
        return gang[i % len(gang)]
    def block(i, art, versteckt=False):
        n, h = ziel(i + 1)
        j = i - 1
        while j > 0 and ziel(j)[1] is None:
            j -= 1
        pn, ph = ziel(j)
        attr = f'href="{e(RES)}" data-fenster="fe-reservation"' if h is None else f'href="{h}"'
        danach = ''
        if h is None:
            an, ah = ziel(i + 2)
            danach = f'<a class="leise" href="{ah}">Danach: {e(an)} →</a>'
        zurueck = f'<a class="leise" href="{ph}">← Zurück: {e(pn)}</a>' if i > 0 else '<span></span>'
        return f'''<section class="folge f-tapete" aria-label="Weiter" data-folge="{art}"{" hidden" if versteckt else ""}>
  <div class="innen folge__in">
    <a class="folge__karte" {attr} data-r="text"><span class="folge__bild"><img src="assets/img/{WEG_BILD.get(h, "haus")}-800.webp" alt="" width="800" height="600" loading="lazy" decoding="async"></span><span class="folge__t"><small>Als Nächstes</small><b>{e(n)}</b></span><span class="folge__kn" aria-hidden="true"><svg viewBox="0 0 16 10"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span></a>
    <div class="folge__unten" data-r="text" style="--i:1">{zurueck}{danach}</div>
  </div>
</section>
'''
    # karte.html trägt Karte und Lästermeile: wer über #laestermeile kommt, geht danach zum Feiern weiter
    out = block(stellen[0], 'haupt')
    for i in stellen[1:]:
        out += block(i, gang[i][1].split('#')[1], versteckt=True)
    return out


def seite(datei, titel, beschreibung, inhalt, vorladen=''):
    out = kopf(titel, beschreibung, datei, vorladen) + leiste(datei) + '<main id="inhalt">\n' + inhalt + weg(datei) + fuss() + '</main>\n' + ende()
    (HIER / datei).write_text(out)
    print('gebaut', datei, len(out) // 1024, 'KB')


# ---------------------------------------------------------------- Startseite
def preis(p):
    return f'{p}'


def gericht_li(g, ganz=False):
    haupt = f' · {g["haupt"]} Hauptgang' if g.get('haupt') else ''
    extra = ''
    if ganz:
        extra = f' <span class="vh">Allergene</span>' if False else ''
    allerg = f' · {e(g["allergene"])}' if ganz and g.get('allergene') else ''
    hinweis = f' {e(g["hinweis"])}' if g.get('hinweis') else ''
    return f'<li><b>{e(g["name"])}</b><span>{g["preis"]}{haupt}</span><small>{e(g["text"])}{hinweis}{allerg}</small></li>'


def land_titel(t):
    return {'Iberische Halbinsel': 'Iberische<br>Halbinsel'}.get(t, e(t))


MK_FOTO = {'Frühling': 'jz-fruehling', 'Sommer': 'jz-sommer', 'Herbst': 'jz-herbst'}  # Stimmung der Jahreszeit, keine Fotos, die schon auf der Seite stehen
def mk_karte(i, m):
    gerichte = ''.join(f'<li><b>{e(g["name"])}</b><span>{e(g["text"])}</span></li>' for g in m['gerichte'])
    return f'''<article class="mk" style="--i:{i}" data-mk>
    <div class="mk__karte">
      <figure class="mk__bild">{img(MK_FOTO[m["name"]], '(max-width:900px) 84vw, 32vw', alt='')}</figure>
      <span class="mk__siegel" aria-hidden="true">{zeiger(30)}</span>
      <div class="mk__blatt">
        <p class="mk__haus">Wirtschaft am Schlössli</p>
        <h3><small>Bankett</small>{e(m["name"])}</h3>
        <span class="mk__zier" aria-hidden="true"></span>
        <ol>{gerichte}</ol>
        <p class="mk__preis"><b>{m["preis"]}</b><span>Franken</span></p>
        <p class="mk__fuss">{e(HAUS['strasse'])} · Bottighofen</p>
      </div>
      <i class="mk__glanz" aria-hidden="true"></i>
    </div>
    <span class="mk__boden" aria-hidden="true"></span>
  </article>'''


def startseite():
    h = HAUS
    s = []
    # Auftakt «Am Tisch» (Robert 19.10.2026, Fassung 07.6 aus _varianten/teller-10.html): der blaue Teller von oben,
    # Name und Adresse als Prägung im Abstand um den Rand, links «Am», rechts «Tisch.». Reservieren nur oben rechts in der Leiste.
    # Der Ring hat 1000 Einheiten, der Teller füllt die inneren 735 (Radius 367,5); Schrift oben bei 421, unten bei 437 (hängt unter der Linie).
    tage = h['zeiten']['tage'].replace(' - ', ' bis ')
    offen = h['zeiten']['offen'].replace(' Uhr', '').replace(' - ', ' bis ') + ' Uhr'
    s.append(f'''<section class="auftakt auftakt--teller" id="auftakt" aria-label="{e(h['name'])}">
  <h1 class="vh">{e(h['name'])}</h1>
  <p class="tw tw--l" aria-hidden="true"><span class="z"><span>Am</span></span><span class="mono">{e(tage)}</span></p>
  <div class="tl">
    <picture>{img('teller', '(max-width:760px) 74vw, 44vw', eager=True)}</picture>
    <svg class="tl__ring" viewBox="0 0 1000 1000" aria-hidden="true"><defs>
      <path id="tl-oben" d="M79,500 A421,421 0 0,1 921,500"/>
      <path id="tl-unten" d="M63,500 A437,437 0 0,0 937,500"/></defs>
      <text><textPath href="#tl-oben" startOffset="50%" text-anchor="middle">WIRTSCHAFT AM SCHLÖSSLI</textPath></text>
      <text><textPath href="#tl-unten" startOffset="50%" text-anchor="middle">{e(h['strasse'].upper())} · BOTTIGHOFEN</textPath></text>
    </svg>
  </div>
  <p class="tw tw--r" aria-hidden="true"><span class="z"><span>Tisch.</span></span><span class="mono">{e(offen)}</span></p>
</section>
''')
    # Willkommen als Brief (Robert 19.10.2026, 18:18: Fassung 01 aus _varianten/willkommen.html, «einladender statt Eigenlob»,
    # links drei Bilder: der leere Stuhl am Wasser gross, darunter Platanen und Abend klein). Die Sätze stehen wörtlich auf der
    # Startseite des Hauses; unterschrieben von Pächter (Tagblatt), Küchenchefin und Gastgeber (Team-Seite). Ersetzt den Teil
    # «Terrasse und Hafen» mit den Stimmen der Führer (Sicherung: _sicherung/bau.py.vor-brief-1820).
    tm = {t['name']: t['rolle'] for t in h['team']}
    s.append(f'''<section class="teil f-tapete wb" id="willkommen" aria-label="Willkommen">
  <div class="innen wb__g">
    <div class="wb__bilder">
      {foto('start-hoch', '(max-width:900px) 92vw, 40vw', 'wb__gross', alt='Leere blaue Stühle am Wasser, dahinter die Alpen')}
      {foto('platanen', '(max-width:900px) 45vw, 19vw', 'wb__klein')}
      {foto('abend', '(max-width:900px) 45vw, 19vw', 'wb__klein')}
    </div>
    <div class="wb__brief" data-r="text">
      <h2 class="t2" data-schlitz>{e(h['satz_willkommen'])}</h2>
      <p class="lauf">{e(h['satz_lage'])}</p>
      <p class="lauf">{e(h['satz_reise'])}</p>
      <p class="lauf">{e(h['satz_anlass'])}</p>
      <div class="wb__sig">
        <span><b>{e(h['satz_terrasse_von'])}</b><i>Pächter</i></span>
        <span><b>Monika Huber</b><i>{e(tm['Monika Huber'])}</i></span>
        <span><b>Jonas Volpert</b><i>{e(tm['Jonas Volpert'])}</i></span>
      </div>
      <div class="knoepfe wb__k">{knopf('Tisch reservieren', RES, attr=' data-fenster="fe-reservation"')}<a class="leise" href="karte.html">Die Karte</a></div>
    </div>
  </div>
</section>
''')
    # Fenster am Ufer (Robert 19.10.2026, 18:28: Bild 4 aus _varianten/fenster statt der Lounge; Gästefoto, nur Demo, siehe bilder.py). Satz aus der Startseite des Hauses (satz_anlass)
    s.append(fenster('fenster-hafen', 'baum', 'Eine kleine Auszeit vom Alltag.'))
    # Lästermeile: die Schwelle von drinnen nach draussen; der Titel teilt sich genau zwischen «Läster» und «meile»
    tap = ''.join(f'<div class="tap__g"><h3>{e(g["titel"])}</h3><ul>' + ''.join(f'<li><b>{e(x["name"])}</b><span>{x["preis"]}</span>' + (f'<small>{e(x["text"])}</small>' if x['text'] else '') + '</li>' for x in g['eintraege']) + '</ul></div>' for g in LM['gruppen'])
    s.append(f'''<section class="lm" id="laestermeile" aria-label="Lästermeile">
  <div class="fliesen lm__band lm__band--oben" aria-hidden="true"></div>
  <div class="innen">
    <h2 class="lm__titel" aria-label="Lästermeile."><span class="links" aria-hidden="true" data-schlitz>Läster</span><span class="rechts" aria-hidden="true" data-schlitz>meile.</span></h2>
    <div class="lm__g">
      <div class="lm__drinnen">
        <p class="lm__zitat" data-r="text"><q>{e(h['zitat_gm_laester'])}</q><cite>GaultMillau</cite></p>
        <p class="lauf" data-r="text" style="--i:1">{e(h['zeiten']['laestermeile'])}</p>
        <div class="lm__bilder">{foto('regal', '(max-width:900px) 56vw, 27vw', 'lm__regal')}{foto('bar', '(max-width:900px) 36vw, 16vw', 'lm__bar')}</div>
      </div>
      <div class="lm__draussen">
        <div class="tapas tapas--zwei" data-r="text">{tap}</div>
        <div class="lm__bilder lm__bilder--r">{foto('ig-luft', '(max-width:900px) 1px, 10vw', 'lm__luft', alt=B['ig-luft']['alt'])}{foto('ig-terrasse', '(max-width:900px) 40vw, 14vw', 'lm__ig', alt=B['ig-terrasse']['alt'])}{foto('schild', '(max-width:900px) 52vw, 19vw', 'lm__schild')}</div>
      </div>
    </div>
  </div>
  <div class="lm__mehr"><a class="kz" href="karte.html#laestermeile"><span class="knopf kz__l" aria-hidden="true">Karte der Lästermeile {PFEIL}</span><span class="knopf knopf--dunkel kz__r">Karte der Lästermeile {PFEIL}</span></a></div>
  <div class="lm__band-w"><div class="fliesen lm__band" aria-hidden="true"></div></div>
</section>
''')
    # Fenster Morgen: der Blick, den das Haus selbst beschreibt
    s.append(fenster('fenster-alpen', 'saentis', 'Mit Blick aufs Wasser und die Alpen.'))
    # Karte (Fassung 14, Robert 19.10.2026): Klassiker mit den Tortelloni gross links, die drei Länder rechts je mit Bild
    def k14_li(g, text):
        preis = f'{g["preis"]}' + (f' / {g["haupt"]}' if g.get('haupt') else '')
        hin = e(g['hinweis'].strip('()').capitalize()) if g.get('hinweis') else ''
        unter = e(g['text']) + (f' · {hin}' if hin else '') if text else hin
        return f'<li><b>{e(g["name"])}</b><em aria-hidden="true"></em><span>{preis}</span>' + (f'<small>{unter}</small>' if unter else '') + '</li>'
    kl = next(l for l in KARTE['laender'] if l['land'] == 'Klassiker')
    rechts = [(l, b) for l, b in zip([l for l in KARTE['laender'] if l['land'] != 'Klassiker'], ['thon', 'pasta', 'salat'])]
    ka14 = (f'<div class="ka14"><div class="ka14__gr">{foto("tortelloni", "(max-width:980px) 92vw, 40vw", "ka14__bild")}'
            f'<div data-r="text"><h3 class="ka14__h">{e(kl["land"])}</h3><ul class="ka14__l">' + ''.join(k14_li(g, True) for g in kl['gerichte']) + '</ul></div></div>'
            '<div class="ka14__drei">' + ''.join(
                f'<div class="ka14__land">{foto(b, "(max-width:560px) 34vw, (max-width:980px) 28vw, 17vw", "ka14__klein")}'
                f'<div data-r="text" style="--i:{i}"><h3 class="ka14__h">{e(l["land"])}</h3><ul class="ka14__l">' + ''.join(k14_li(g, False) for g in l['gerichte']) + '</ul></div></div>'
                for i, (l, b) in enumerate(rechts)) + '</div></div>')
    gaenge = '<span class="lu__stern" aria-hidden="true">✶ ✶ ✶</span>'.join(f'<p class="lu__gang"><b>{e(g["name"])}</b><small>{e(g["text"])}</small></p>' for g in LUNCH['gaenge'])
    s.append(f'''<section class="teil f-tapete" id="karte" aria-label="Die Karte">
  <div class="innen">
    <div class="ka__kopf">
      <h2 class="t2" data-schlitz>Vier Länder auf <em>einer Karte.</em></h2>
      <p class="zitat" data-r="text"><q>{e(h['satz_reise'])}</q></p>
    </div>
    {ka14}
    <p class="karte-fuss mk__fuss" data-r="text">{e(KARTE['fuss']['mwst'])}</p>
    <div class="lu" id="mittag-start" data-r="bild">
      <figure class="lu__bild" style="background-image:url({B['suppe']['abbild']})">{img('suppe', '(max-width:900px) 92vw, 34vw')}</figure>
      <div class="lu__t">
        <p class="lu__kopf"><span>Mittags</span><b>Lunch-Menü</b><span>{e(LUNCH['preis'].replace(' – Gänge – ', ' Gänge · ').replace('.- Chf', ' Franken'))}</span></p>
        <div class="lu__gaenge">{gaenge}</div>
        <div class="knoepfe lu__k">{knopf('Tisch zum Lunch', RES, attr=' data-fenster="fe-reservation"')}<a class="leise" href="karte.html">Die ganze Karte</a></div>
      </div>
    </div>
  </div>
</section>
''')
    # Küche (Robert 19.10.2026, 18:4x: Fassung 1 «Blatt mit Briefkopf» aus _varianten/kueche-blatt-10.html): helles Blatt in der Mitte, Moni rund als Briefkopf,
    # seit 18:4x rundum von Bildern eingefasst wie die Rivage-Kacheln; die beiden Bilder über dem Blatt sind unten innen um Monis Kreis ausgespart (Robert 19.10.2026). Sicherung: _sicherung/bau.py.vor-kueche-blatt-*
    s.append(f'''<section class="teil f-dunkel" id="kueche" aria-label="Die Küche">
  <div class="innen">
    <div class="ku3">
      <div class="ku3__l">{foto('ig-teller', '(max-width:900px) 46vw, 22vw', alt=B['ig-teller']['alt'])}{foto('fisch', '(max-width:900px) 46vw, 22vw')}{foto('lukas', '(max-width:900px) 46vw, 22vw', 'ku3__lukas')}</div>
      {foto('sauce', '(max-width:900px) 46vw, 24vw', 'ku3__o1')}
      {foto('iberia', '(max-width:900px) 46vw, 24vw', 'ku3__o2')}
      <div class="ku3__blatt" data-r="text">
        <div class="ku3__rund">{foto('moni', '192px', r=False)}</div>
        <p class="mono ku2__kopf">Die Küche · Moni Huber</p>
        <h2 class="t2" data-schlitz>Entdeckung <em>des Jahres 2026.</em></h2>
        <p class="ku2__q">«{e(h['zitat_gm_kueche'])}»</p><p class="mono ku2__von">GaultMillau über Moni Huber</p>
        <p class="lauf ku2__weg">{e(h['weg_moni'])}</p>
        <div class="ku2__preise">
          <div><img class="ku2__lg" src="assets/img/ehre-gaultmillau-15.webp" width="292" height="240" alt="GaultMillau Guide Schweiz, 15 Punkte" loading="lazy"><b><span data-zahl="15">15</span></b><span>Punkte · GaultMillau · Guide 2027</span></div>
          <div><img class="ku2__lg" src="assets/img/ehre-michelin-2025.webp" width="240" height="240" alt="Michelin 2025" loading="lazy"><b class="w">Favorit der Inspektoren</b><span>Guide Michelin</span></div>
          <div><img class="ku2__lg ku2__lg--wort" src="assets/img/ehre-falstaff.svg" width="239" height="71" alt="Falstaff" loading="lazy"><b><span data-zahl="91">91</span><small>/100</small></b><span>Falstaff</span></div>
        </div>
      </div>
      {foto('torte', '(max-width:900px) 46vw, 24vw', 'ku3__u1')}
      {foto('ig-herd', '(max-width:900px) 46vw, 24vw', 'ku3__u2', alt=B['ig-herd']['alt'])}
      <div class="ku3__r">{foto('fleisch', '(max-width:900px) 46vw, 22vw')}{foto('dessert', '(max-width:900px) 46vw, 22vw', 'ku3__team')}{foto('ig-pasta', '(max-width:900px) 46vw, 22vw', alt=B['ig-pasta']['alt'])}</div>
    </div>
  </div>
</section>
''')
    # Keller als Abzüge vom Abend (Robert 19.10.2026, Fassung 3 aus _varianten/keller-runde2.html): links Titel, Zahl, Jonas mit seinem Satz
    # und dem GaultMillau-Zeichen; rechts sechs Abzüge, die einzeln von unten hereinfliegen (ausgelöst vom Stapel, sobald er am Rand auftaucht,
    # weil die weit versetzten Abzüge selbst erst spät in den Blick kämen); Weinberater mittig darunter
    weine = sum(len(p['weine']) for g in WEIN['gruppen'] for r in g['regionen'] for p in r['erzeuger'])
    ab = [('lounge', 'a', '45% 60%'), ('wein', 'b', '50% 40%'), ('apero', 'c', '50% 62%'), ('ig-abend', 'd', '50% 45%'), ('ig-hafen', 'e', '50% 50%'), ('glas', 'f', '50% 52%')]
    abz = ''.join(foto(n, '(max-width:900px) 50vw, 26vw', f'ke__ab ke__ab--{k}', r=False, alt=B[n]['alt'], stil=f'--pos:{p}') for n, k, p in ab)
    s.append(f'''<section class="teil f-hell" id="keller" aria-label="Der Keller">
  <div class="innen">
    <div class="ke__g">
      <div class="ke__l">
        <h2 class="t2 ke__t" data-schlitz>Jonas Volpert, <em>Gastgeber und Sommelier.</em></h2>
        <p class="ke__zahl" data-r="text"><b data-zahl="{weine}">{weine}</b><span>Weine auf der Karte, vom Thurgau bis Pauillac, Champagner bis zur 9-Liter-Flasche</span></p>
        <div class="ke__jonas">{foto('jonas', '(max-width:900px) 40vw, 16vw')}
          <div class="ke__zit" data-r="text" style="--i:1"><p class="zitat zitat--gross"><q>{e(h['zitat_jonas'])}</q></p><p class="ke__satz">Jonas sucht mit Ihnen die Flasche aus.</p><p class="ke__von"><img src="assets/img/logo-gm15.webp" width="259" height="240" alt="GaultMillau Guide Schweiz, 15 Punkte" loading="lazy"><span>Jonas Volpert im GaultMillau</span></p></div>
        </div>
      </div>
      <div class="ke__stapel" data-r="stapel">{abz}</div>
      <div class="ke__knopf" data-r="text" style="--i:2">{knopf('Weinberater', 'weinkarte.html#berater')}<a class="leise" href="weinkarte.html">Die ganze Weinkarte</a></div>
    </div>
  </div>
</section>
''')
    # Fenster Abend: die Platane mit der Lichterkette
    s.append(fenster('fenster-abend', 'abend-hafen', 'Wenn es Abend wird am Hafen.'))
    # Besen als Chronik-Wand (Robert 19.10.2026, Fassung 01 aus _varianten/besen2.html, scharf in besen-wand.html):
    # elf Stücke aus drei Jahrhunderten dicht an einer Wand, mittendrin der Titel als eigener Stein. Jedes Bild geht beim Auftritt auf (wächst und zoomt hinein, nacheinander).
    # Die alte Fassung (Luftbild, Inschrift, drei Spalten) liegt in _sicherung/bau.py.vor-chronikwand-*.
    wand = [('ch-postkarte', 'a', '1888'), ('luft1954', 'b', '1954'), ('ch-anzeige', 'c', ''), ('ch-strandhotel', 'd', 'Strandhotel'), None,
            ('ch-zeichnung', 'e', 'Zeichnung'), ('ch-mann', 'f', 'Hotel'), ('schifflaende', 'g', 'Heute'), ('ch-luftkarte', 'h', 'Strandhotel'),
            ('ch-portal', 'i', 'Haus'), ('bootshafen', 'j', 'Heute'), ('ch-ufer', 'k', 'Hotel')]
    steine = []
    for i, w in enumerate(wand):
        if w is None:
            steine.append('<div class="chw__titel"><p class="mono" data-r="text">Bottighofen · seit dem 17. Jahrhundert</p><h2 class="t2" data-schlitz>Ein Besen statt <em>eines Schilds.</em></h2></div>')
            continue
        n, k, et = w
        steine.append(f'<div class="chw__stein chw--{k}">{foto(n, "(max-width:900px) 92vw, 40vw", stil=f"--i:{i}")}' + (f'<span class="chw__et">{et}</span>' if et else '') + '</div>')
    s.append(f'''<section class="chw f-tapete" id="besen" aria-label="Geschichte des Ortes">
  <div class="innen">
    <div class="chw__wand">{''.join(steine)}</div>
    <p class="chw__nw">Heft 2 «Die Bottighofer Mühlen und das Schlössli am See», Gemeinde Bottighofen 1994, Bilder mit KI nachgeschärft, Text der Anzeige nach dem Original gesetzt · 1954: {nw('luft1954', 'nachweis--zeile', 'span')} · Schifflände und Bootshafen: {nw('schifflaende', 'nachweis--zeile', 'span')}</p>
  </div>
</section>
''')
    # Feiern (Robert 19.10.2026, Fassung 2 aus _varianten/feiern-15.html, «Karten mit 3D-Effekt und Schein wie in den Werkzeugen, richtig edel»):
    # die drei Bankettmenüs als gedruckte Karten des Hauses auf dem Leder. Jede Karte neigt sich am Rechner zur Maus, ein Lichtstreif läuft
    # auf jeder Karte einmal, nacheinander von links nach rechts (Hereinkommen oder erstes Berühren, nur transform, haus.js Teil 11). Am Handy ein Band zum Seitwärtsblättern.
    s.append(f'''<section class="teil f-dunkel" id="feiern" aria-label="Banketts und Gruppen">
  <div class="innen">
    <div class="mk-kopf">
      <span class="mk-kopf__zeichen" aria-hidden="true" data-r="text">{zeiger(46)}</span>
      <!-- Robert 19.10.2026, 20:40: auf der Startseite sah der Abschnitt aus wie die normale Karte, darum Bankett in der Überschrift -->
      <h2 class="mk-kopf__t" data-schlitz>Bankettmenüs für <em>Ihre Feier.</em></h2>
      <p class="lauf mk-kopf__satz" data-r="text">{e(HAUS['bankett']['fett'])} {e(BANKETT['hinweis'])}</p>
    </div>
    <div class="mk-tisch" data-r="bild">{''.join(mk_karte(i, m) for i, m in enumerate(BANKETT['menues']))}</div>
    <p class="mk-nachweis">{' · '.join(nw(n, tag='span') for n in MK_FOTO.values())}</p>
    <div class="fe__unten knoepfe" data-r="text">{knopf('Bankettanfrage', '#', dunkel=True, attr=' data-fenster="fe-bankett"')}<a class="leise" href="feiern.html#menues">Alle Bankettmenüs</a></div>
  </div>
</section>
''')
    # Abend: der Tag aus Bildern (Fassung 01 aus _varianten/zeiten-bilder-15.html, Robert 19.10.2026 mit Fotos, die auf der ganzen Website
    # noch nicht vorkommen). Jedes Bild so breit, wie seine Zeit dauert: 11:30–13:30, 13:30–18:00, 18:00–20:00, 20:00–23:00.
    z = h['zeiten']
    # Jedes Foto ganz, ohne Ausschnitt: der Rahmen folgt dem Seitenverhältnis des Bildes (--a = Breite/Höhe), alle gleich hoch.
    tag = [('tb-fisch', '11:30', 'Küche', 'Mittag'), ('tb-glas', '13:30', 'Lästermeile', 'den ganzen Tag'),
           ('tb-teller', '18:00', 'Küche', 'Abend'), ('tb-dunkel', '20:00', 'Unter der Platane', 'bis 23:00')]
    streif = ''.join(f'<div class="tb" style="--a:{round(B[n]["w"] / B[n]["h"], 4)};--i:{i}"><span class="tb__u">{u}</span>{foto(n, "(max-width:760px) 46vw, 30vw")}<p class="tb__t"><b>{e(t)}</b>{e(un)}</p></div>'
                     for i, (n, u, t, un) in enumerate(tag))
    # Am Handy zwei Zeilen zu je zwei Bildern: Umbruch nach dem zweiten Bild
    teile = streif.split('</div><div class="tb"')
    streif = '</div><i class="tb__bruch" aria-hidden="true"></i><div class="tb"'.join(['</div><div class="tb"'.join(teile[:2]), '</div><div class="tb"'.join(teile[2:])])
    s.append(f'''<section class="teil f-hell" id="abend" aria-label="Öffnungszeiten und Reservation">
  <div class="innen">
    <h2 class="t2 tb__titel" data-schlitz>Bis 23 Uhr <em>unter der Platane.</em></h2>
    <div class="tb__streif" aria-label="Der Tag: Küche 11:30 bis 13:30, Lästermeile den ganzen Tag, Küche 18:00 bis 20:00, offen bis 23:00">{streif}</div>
    <div class="tb__fuss" data-r="text">
      <p class="tb__woche"><span>{e(z['tage'].replace(' - ', ' bis '))}, {e(z['offen'].replace(' Uhr', '').replace(' - ', ' bis '))} Uhr</span> <i>·</i> <span>{e(z['ruhetag'].replace(' & ', ' und '))}</span></p>
      <div class="knoepfe">{knopf('Tisch reservieren', RES, dunkel=True, attr=' data-fenster="fe-reservation"')}<a class="leise" href="abend.html">Abend zusammenstellen</a><a class="leise" href="gutschein.html">Gutschein</a><a class="leise" href="kontakt.html#see">Der See heute</a></div>
    </div>
    <p class="ab__ferien tb__ferien" data-r="text"><b>Ferien</b> {' <i>·</i> '.join(f'<span>{e(f.replace(' - ', ' bis '))}</span>' for f in h['ferien'])}</p>
  </div>
</section>
''')
    seite('index.html', f'{h["name"]} · Restaurant am Hafen von Bottighofen', f'{h["satz_lage"]} Mediterrane Küche von Moni Huber, Lästermeile mit Tapas den ganzen Tag, Banketts auf zwei Etagen.', ''.join(s),
          vorladen=f'<link rel="preload" as="image" href="assets/img/start-1200.webp" imagesrcset="{srcset("start")}" imagesizes="100vw" media="(min-width:761px)">\n<link rel="preload" as="image" imagesrcset="{srcset("start-hoch")}" imagesizes="100vw" media="(max-width:760px)">\n')


def fenster(id_, n, satz):
    b = B[n]
    gr = b['breiten'][-2] if len(b['breiten']) > 1 else b['breiten'][-1]
    # Das Bild füllt den ganzen Bildschirm (cover): auf schmalen Geräten ist es breiter als 100vw, sonst lädt das Handy eine zu kleine Grösse (19.10.2026)
    gr_sizes = f"(max-aspect-ratio:{b['w']}/{b['h']}) {round(b['w'] / b['h'] * 100)}vh, 100vw"
    return f'''<section class="fenster" id="{id_}" aria-label="{e(satz)}">
  <div class="fenster__f">
    <img data-src="assets/img/{n}-{gr}.webp" data-srcset="{srcset(n)}" sizes="{gr_sizes}" width="{b['w']}" height="{b['h']}" alt="{e(b['alt'])}" decoding="async" style="background:url({b['abbild']}) center/cover">
    <div class="fenster__s"><p data-schlitz>{e(satz)}</p></div>
  </div>
  {nw(n, 'nachweis--fenster')}
</section>
'''


# ---------------------------------------------------------------- Unterseiten
def seitenkopf(n, titel_html, unter_html, hzk=.62, dunkel=False, alt=None):
    return f'''<section class="kopf {'f-dunkel' if dunkel else 'f-tapete'}" id="kopf" style="--hzk:{hzk}">
  <div class="kopf__t"><h1>{titel_html}</h1></div>
  <span class="hz hz--rechts" aria-hidden="true"></span>
  <div class="kopf__unter">{unter_html}</div>
  <figure class="kopf__bild" style="background:url({B[n]['abbild']}) center/cover">{img(n, '(max-width:860px) 100vw, 50vw', eager=True, alt=alt)}</figure>
</section>
'''


def klein_kopf(titel_html):
    return f'<section class="kopf kopf--klein f-tapete" id="kopf"><div class="kopf__t"><h1>{titel_html}</h1></div></section>\n'


def slug(t):
    return t.lower().replace(' ', '-')


def karte_kopf():
    # Kompass (Robert 19.10.2026, 20:40, Fassung 16 aus _varianten/karte-kopf-15.html): links der Zeiger aus der Wortmarke als Kompass,
    # an seinen Enden die vier Teile der Karte als feine Landkarten (landkarten.py) mit Stadt in Handschrift; Mitte Titel, Satz, Knopf auf einer Achse; rechts die Suppe.
    stadt = {'Frankreich': 'Paris', 'Italien': 'Roma', 'Iberische Halbinsel': 'Madrid', 'Klassiker': 'Bottighofen'}
    lage = ['n', 'o', 's', 'w']
    orte = ''.join(f'<a class="kko__ort kko__ort--{r}" href="#land-{slug(l["land"])}"><img src="assets/svg/land-{slug(l["land"])}.svg" width="140" height="140" alt=""><i></i><span>{e(l["land"])}</span><small>{stadt[l["land"]]}</small></a>' for r, l in zip(lage, KARTE['laender']))
    return f'''<section class="kko f-tapete" id="kopf">
  <nav class="kko__rose" aria-label="Die vier Teile der Karte"><span class="kko__zeiger">{zeiger(240)}</span>{orte}</nav>
  <div class="kko__m"><h1>Die <em>Karte.</em></h1><p class="lauf">{e(HAUS["satz_reise"])}</p></div>
  <div class="kko__kn">{knopf("Tisch reservieren", RES, dunkel=True, attr=' data-fenster="fe-reservation"')}</div>
  <figure class="kko__bild kopf__bild" style="background:url({B['suppe']['abbild']}) center/cover">{img('suppe', '(max-width:860px) 100vw, 28vw', eager=True)}</figure>
</section>
'''


def karte_seite():
    # Im Wechsel (Fassung 04 aus _varianten/karte-bilder-15.html, Robert 19.10.2026): je Land ein ganzes Foto, abwechselnd links und rechts
    kw_bild = {'Frankreich': 'thon', 'Italien': 'pasta', 'Iberische Halbinsel': 'iberia', 'Klassiker': 'tortelloni'}
    laender = ''.join(f'<div class="kw{' kw--r' if i % 2 else ''}" id="land-{slug(l["land"])}">' + foto(kw_bild[l['land']], '(max-width:900px) 80vw, 30vw', cls='kw__bild', stil=f"aspect-ratio:{B[kw_bild[l['land']]]['w']}/{B[kw_bild[l['land']]]['h']}") + f'<div class="land kw__t" data-r="text"><h3>{e(l["land"])}</h3><ul>' + ''.join(gericht_li(g, ganz=True) for g in l['gerichte']) + '</ul></div></div>' for i, l in enumerate(KARTE['laender']))
    f = KARTE['fuss']
    tap_g = ''.join(f'<div class="tap__g"><h3>{e(g["titel"])}</h3><ul>' + ''.join(f'<li><b>{e(x["name"])}</b><span>{x["preis"]}</span>' + (f'<small>{e(x["text"])}</small>' if x['text'] else '') + '</li>' for x in g['eintraege']) + '</ul></div>' for g in LM['gruppen'])
    tap = ''.join(f'<h3>{e(g["titel"])}</h3><ul>' + ''.join(f'<li><b>{e(x["name"])}</b><span>{x["preis"]}</span>' + (f'<small>{e(x["text"])}</small>' if x['text'] else '') + '</li>' for x in g['eintraege']) + '</ul>' for g in LM['gruppen'])
    lunch_gaenge = '<span class="lum__stern" aria-hidden="true">✶</span>'.join(f'<p><b>{e(g["name"])}</b><small>{e(g["text"])}</small></p>' for g in LUNCH['gaenge'])
    inhalt = karte_kopf()
    inhalt += f'''<section class="teil f-hell karte-ganz" id="laender" aria-label="Speisekarte">
  <div class="innen">
    <div class="ab-satz"><h2 class="t2" data-schlitz>Frankreich, Italien, <em>Iberische Halbinsel, Klassiker.</em></h2><p class="lauf" data-r="text">{e(HAUS['zeiten']['kueche_hinweis'])} Küche {e(HAUS['zeiten']['kueche'][0].replace(' - ', ' bis '))} und {e(HAUS['zeiten']['kueche'][1].replace(' - ', ' bis '))}.</p></div>
    <div class="ka__wechsel">{laender}</div>
    <div class="karte-fuss"><p>{e(f['veg'])}. {e(f['veg2'])}</p><p>{e(f['allergene'])}</p><p>{e(f['mwst'])}</p></div>
    <div class="drucken"><button class="leise" type="button" onclick="print()">Karte drucken</button><a class="leise" href="unterlagen/pdf/speisekarte.pdf" target="_blank" rel="noopener">Karte als PDF</a></div>
  </div>
</section>
{F.wein_zum_gang(foto)}<section class="teil f-hell lum" id="mittag" aria-label="Lunch-Menü">
  <div class="innen">
    <h2 class="t2" data-schlitz>Mittags am <em>Hafen.</em></h2>
    <div class="lum__m">
      {foto('platanen', '(max-width:900px) 92vw, 46vw', 'lum__a')}{foto('suppe', '(max-width:900px) 46vw, 22vw', 'lum__b')}{foto('tb-glas', '(max-width:900px) 46vw, 22vw', 'lum__c')}
      <div class="lum__karte" data-r="text"><div class="lum__rahmen">
        {zeichen(32)}
        <h3 class="lum__titel">Lunch</h3><p class="lum__wo">Diese Woche</p>
        <div class="lum__gaenge">{lunch_gaenge}</div>
        <p class="lum__p"><b>{LUNCH['preis_zahl']}</b><span>Franken · {['eins','zwei','drei','vier','fünf'][len(LUNCH['gaenge'])-1]} Gänge</span></p>
      </div></div>
      {foto('tb-fisch', '(max-width:900px) 46vw, 22vw', 'lum__d')}{foto('sauce', '(max-width:900px) 46vw, 22vw', 'lum__e')}{foto('dessert', '(max-width:900px) 92vw, 22vw', 'lum__f')}
    </div>
    <div class="lum__fuss"><p class="lauf" data-r="text">Das Menü wechselt jede Woche.</p><div class="knoepfe" data-r="text">{knopf("Tisch zum Lunch", RES, attr=" data-fenster=\"fe-reservation\"")}<a class="leise" href="#laender">Die ganze Karte</a><a class="leise" href="unterlagen/pdf/lunch.pdf" target="_blank" rel="noopener">Lunch als PDF</a></div></div>
  </div>
</section>
<section class="lmk f-dunkel" id="laestermeile" aria-label="Karte der Lästermeile">
  <div class="fliesen lmk__band" aria-hidden="true"></div>
  <div class="innen lmk__tisch">
    <div class="lmk__set" data-r="text"><h2 class="t2" data-schlitz>Die <em>Lästermeile.</em></h2><div class="tapas tapas--zwei lmk__zwei">{tap_g}</div><p class="lmk__zeit">{e(HAUS['zeiten']['laestermeile'])}</p><p class="lmk__pdf"><a class="leise" href="unterlagen/pdf/laestermeile.pdf" target="_blank" rel="noopener">Karte der Lästermeile als PDF</a></p></div>
    <div class="lmk__fotos">{foto('apero', '(max-width:900px) 70vw, 30vw', 'lmk__apero')}{foto('bar', '(max-width:900px) 46vw, 18vw', 'lmk__bar')}</div>
  </div>
  <div class="fliesen lmk__band" aria-hidden="true"></div>
</section>
'''
    seite('karte.html', f'Die Karte · {HAUS["name"]}', 'Die Speisekarte nach Frankreich, Italien, Iberischer Halbinsel und Klassikern, das Lunch-Menü der Woche und die Karte der Lästermeile.', inhalt)


def weinkarte_seite():
    def anker(t):
        return re.sub(r'[^a-z]+', '-', t.lower().replace('é', 'e').replace('ü', 'ue').replace('&', ''))
    reiter = ''.join(f'<a href="#{anker(g["titel"])}">{e(g["titel"])}</a>' for g in WEIN['gruppen'])
    # Liste als Platten je Weingut (Robert 19.10.2026, Fassung 01 aus _varianten/weinliste-3d.html): Land mit Flagge als Kapitel,
    # je Weingut eine erhabene Platte, oben klein das Logo (weingut_logos.py, einfarbig im Blau der Seite), mittig der Name, darunter die Region,
    # die Weine in der eingelassenen Kuhle (Logos seit 21:10 in Originalfarben, nur weisse oder blasse in Blau); jede Zeile öffnet die Wein-Ansicht. Ohne belegtes Logo: Monogramm bzw. Flagge.
    LOGO = json.loads((HIER / 'assets' / 'data' / 'weingut-logos.json').read_text())
    DAT = {w['id']: w for w in funktionen_daten.weine()}

    def monogramm(n):
        kern = re.split(r'\s[–-]\s', n)[0]
        t = [x for x in re.findall(r"[A-Za-zÀ-ÿ’']+", kern) if x.lower() not in {'champagne', 'weingut', 'domaine', 'maison', 'tenuta', 'bodegas', 'castello', 'cantina', 'cantine', 'weinkellerei', 'weinbau', 'de', 'du', 'des', 'la', 'le', 'les', 'et', 'y', 'by', 'von', 'zum', 'zur', 'dell', 'della', 'di', 'dr', 'château', 'vignoble'}]
        return ''.join(x[0].upper() for x in t[:2]) or n[:1].upper()

    def zeile(x, nr):
        preis = ' · '.join(f'{fl["gross"].replace("l", " l").replace(".", ",")} <b>{fl["preis"]}</b>' for fl in x['flaschen'])
        q = ' '.join(str(v) for v in (x['jahr'], x['name'], x.get('notiz'), DAT[nr]['erzeuger'], DAT[nr]['region'], DAT[nr]['land']) if v)
        return (f'<button type="button" class="wl__z" data-wein="{nr}" data-q="{e(q)}"><i>{e(str(x["jahr"] or ""))}</i><span>{e(x["name"])}'
                + (f'<small>{e(x["notiz"])}</small>' if x.get('notiz') else '') + f'</span><em>{preis}</em></button>')

    def platte(q, gemischt):
        """Eine Platte; gemischt = Kapitel mit mehreren Ländern oder ohne Länder-Titel, dann trägt die Platte ihre Flagge klein in der Unterzeile."""
        land, region, erz = q['land'], q['region'], q['erz']
        flg = f'<span class="wl__kflg">{F.flagge_svg(land)}</span>' if gemischt else ''
        if erz:
            lg = LOGO.get(erz)
            zeichen = (f'<img class="wl__logo" src="{lg.get("farbe") or lg["logo"]}" width="{lg.get("fb") or lg["b"]}" height="{lg.get("fh") or lg["h"]}" alt="" loading="lazy" decoding="async">' if lg
                       else f'<span class="wl__mono" aria-hidden="true">{e(monogramm(erz))}</span>')
            titel, unter = erz, ' · '.join(x for x in (region, land) if x)
        elif region:                                     # Bordeaux: Appellation als Titel
            zeichen, titel, unter, flg = f'<span class="wl__flg">{F.flagge_svg(land)}</span>', region, land, ''
        else:                                            # «Diverse Schaumweine» der Karte: je Land eine Platte
            zeichen, titel, unter, flg = f'<span class="wl__flg">{F.flagge_svg(land)}</span>', (land if gemischt else 'Diverse Schaumweine'), ('Schaumwein' if gemischt else land), ''
        return (f'<article class="wl__p" data-land="{e(land)}"><header class="wl__kopf">{zeichen}<h4>{e(titel)}</h4><small>{flg}{e(unter)}</small></header>'
                f'<div class="wl__kuhle">{q["zeilen"]}</div></article>')

    teile, nr = [], 0
    for g in WEIN['gruppen']:
        pl = []                                         # Platten der Gruppe in der Reihenfolge der Karte
        for r in g['regionen']:
            for p in r['erzeuger']:
                if not p['weine']:
                    continue
                zeilen = ''
                for x in p['weine']:
                    nr += 1
                    zeilen += zeile(x, nr)
                d = DAT[nr]
                pl.append({'land': d['land'], 'region': d['region'], 'erz': d['erzeuger'], 'zeilen': zeilen, 'n': len(p['weine'])})
        # Kapitel (Robert 19.10.2026, 21:15: «nicht so viele einzelne untereinander, zu Blöcken links, rechts zusammenfassen»):
        # kleine Gruppen (bis 8 Platten) ohne Länder-Titel in einem Block; Länder mit nur einer Platte gehen mit dem nächsten Land
        # (am Ende mit dem vorigen) in ein gemeinsames Kapitel, Reihen solcher Länder in eines.
        laeufe = []
        for q in pl:
            if not laeufe or laeufe[-1][0] != q['land']:
                laeufe.append((q['land'], []))
            laeufe[-1][1].append(q)
        if len(pl) <= 8:
            kapitel = [(None, pl)]
        else:
            kapitel, offen = [], []
            for i, (land, qs) in enumerate(laeufe):
                offen.append((land, qs))
                einzeln = len(qs) == 1
                naechster_einzeln = i + 1 < len(laeufe) and len(laeufe[i + 1][1]) == 1
                if einzeln and i + 1 < len(laeufe):
                    continue                            # wartet auf das nächste Land
                if not einzeln and naechster_einzeln and i + 2 >= len(laeufe):
                    continue                            # letztes Einzel-Land kommt noch dazu
                kapitel.append(([l for l, _ in offen], [q for _, x in offen for q in x]))
                offen = []
            if offen:
                if kapitel and len(offen) == 1 and len(offen[0][1]) == 1:
                    kapitel[-1][0].append(offen[0][0]); kapitel[-1][1].extend(offen[0][1])
                else:
                    kapitel.append(([l for l, _ in offen], [q for _, x in offen for q in x]))
        kap = ''
        for laender, qs in kapitel:
            gemischt = laender is None or len(laender) > 1
            raster = f'<div class="wl__raster">{"".join(platte(q, gemischt) for q in qs)}</div>'
            if laender is None:
                kap += f'<section class="wl__kap">{raster}</section>'
                continue
            n = sum(q['n'] for q in qs)
            schaum = all(not q['erz'] and not q['region'] for q in qs) and len(laender) > 1
            name = 'Diverse Schaumweine' if schaum else ' · '.join(laender)
            kap += (f'<section class="wl__kap"><div class="wl__land"><span class="wl__lflgs">{"".join(f"<span class={chr(34)}wl__lflg{chr(34)}>{F.flagge_svg(l)}</span>" for l in laender)}</span>'
                    f'<h3>{e(name)}</h3><small>{n} {"Wein" if n == 1 else "Weine"}</small></div>{raster}</section>')
        teile.append(f'<div class="wk__gruppe" id="{anker(g["titel"])}" data-art="{e(g["titel"])}"><h2 class="wl__art"><span>{e(g["titel"])}</span></h2>{kap}</div>')
    # Kopf «Glas am See» mit der Leiste der fünf Arten (Fassungen 04 + 01 aus _varianten/weinkarte-kopf-15.html, Robert 19.10.2026)
    zahl = [(g['titel'], sum(len(p['weine']) for r in g['regionen'] for p in r['erzeuger'])) for g in WEIN['gruppen']]
    summe = sum(n for _, n in zahl)
    leiste = ''.join(f'<a href="#{anker(t)}" style="--w:{n / summe:.3f}"><b>{e({"Champagner & Schaumwein": "Schaumwein"}.get(t, t))}</b><small>{n}</small></a>' for t, n in zahl)
    # Kopf «Das Kellerbuch» (Robert 19.10.2026, 21:4x: Fassung 9 aus _varianten-weinkopf): aufgeschlagenes Buch, links das Glas am See,
    # rechts die Seite mit dem Inhalt, je Art eine Zeile mit Punktlinie und Zahl; Zahlen aus der Karte gezählt
    erz_n = len({w['erzeuger'] for w in DAT.values()})
    land_n = len({w['land'] for w in DAT.values()})
    inhalt_buch = ''.join(f'<li><a href="#{anker(t)}">{e({"Champagner & Schaumwein": "Schaumwein"}.get(t, t))}<span>{n}</span></a></li>' for t, n in zahl)
    inhalt = f'''<section class="wkb" id="kopf">
  <div class="wkb__buch">
    <figure class="wkb__bild" style="background:url({B['glas']['abbild']}) center/cover">{img('glas', '(max-width:900px) 92vw, 46vw', eager=True)}</figure>
    <div class="wkb__seite">
      <p class="wkb__haus">{e(HAUS['name'])}</p>
      <h1>Die <em>Weinkarte.</em></h1>
      <nav aria-label="Arten der Weinkarte"><ol>{inhalt_buch}</ol></nav>
      <p class="wkb__fuss">{summe} Weine · {erz_n} Weingüter · {land_n} Länder</p>
    </div>
  </div>
</section>
'''
    # Filter über der Liste (Robert 19.10.2026, 21:18: «oben eine kleine Möglichkeit zum Filtern»): Art, Land, Suche; haus.js Teil «Weinliste filtern»
    kurz = {'Champagner & Schaumwein': 'Schaumwein', 'Weisswein': 'Weiss', 'Rotwein': 'Rot', 'Süsswein': 'Süss'}
    laender_da = [l for l in F.LAENDER if any(w['land'] == l for w in DAT.values())]
    lupe = '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12.6 12.6 17 17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
    wl_filter = (f'<header class="wl__titel"><h2 class="t2" data-schlitz>Die ganze <em>Karte.</em></h2><p>Alle {summe} Weine des Hauses, nach Art, Land oder Namen.</p></header>'
                 f'<div class="wl__filter" role="search" aria-label="Weinkarte filtern">'
                 f'<div class="wl__wahl" role="group" aria-label="Art"><button type="button" data-f-art="" aria-pressed="true">Alle<small>{summe}</small></button>'
                 + ''.join(f'<button type="button" data-f-art="{e(t)}" aria-pressed="false">{e(kurz.get(t, t))}<small>{n}</small></button>' for t, n in zahl) + '</div>'
                 f'<div class="wl__wahl wl__wahl--land" role="group" aria-label="Land"><button type="button" data-f-land="" aria-pressed="true">Alle Länder</button>'
                 + ''.join(f'<button type="button" data-f-land="{e(l)}" aria-pressed="false"><span class="wl__kflg">{F.flagge_svg(l)}</span>{e(l)}</button>' for l in laender_da) + '</div>'
                 f'<label class="wl__suche">{lupe}<span class="vh">Suchen</span><input type="search" placeholder="Weingut, Wein oder Jahrgang" autocomplete="off" data-f-q></label>'
                 f'<p class="wl__stand" aria-live="polite" data-f-stand>{summe} Weine</p></div>'
                 f'<p class="wl__leer" data-f-leer hidden>Kein Wein passt zu dieser Auswahl.</p>')
    inhalt += f'''<section class="teil f-hell" id="weine" aria-label="Weinkarte">
  <div class="innen">
    {wl_filter}
    {''.join(teile)}
    <div class="karte-fuss">{''.join(f'<p>{e(x)}</p>' for x in WEIN['fuss'])}</div>
    <div class="drucken"><button class="leise" type="button" onclick="print()">Weinkarte drucken</button><a class="leise" href="unterlagen/pdf/weinkarte.pdf" target="_blank" rel="noopener">Weinkarte als PDF</a></div>
  </div>
</section>
'''
    inhalt = inhalt.replace('<section class="teil f-hell" id="weine"', F.weinberater() + '<section class="teil f-hell" id="weine"', 1)
    seite('weinkarte.html', f'Weinkarte · {HAUS["name"]}', 'Die Weinkarte der Wirtschaft am Schlössli: Champagner und Schaumwein, Weiss-, Rosé-, Rot- und Süsswein, Stand 14. Oktober 2026.', inhalt)



def bankett_rechner(b):
    """Teil «Ihr Menü» der Seite Feiern (Robert 19.10.2026, Fassung 3 aus _varianten/etagen-neu.html): aus den Bankettmenüs drei bis fünf
    Gerichte wählen, Gäste einstellen, Richtwert für die Speisen; die Anfrage nimmt die Auswahl mit (haus.js Teil «Bankett-Rechner»).
    Alle Jahreszeiten liegen übereinander, damit die Karte beim Wechseln nicht springt."""
    zeichen = f'<span class="bm__zeichen" aria-hidden="true">{zeiger(34)}</span>'
    tabs = ''.join(f'<button type="button" data-bm-s="{i}" aria-pressed="{str(i == 0).lower()}">{e(m["name"])}</button>' for i, m in enumerate(BANKETT['menues']))
    felder = ''.join(f'<fieldset class="bm__liste" data-bm-feld="{i}"{"" if i == 0 else " hidden"}><legend class="vh">Bankett {e(m["name"])}</legend>' + ''.join(
        f'<label class="bm__g"><input type="checkbox" value="{g["preis"]}" data-name="{e(g["name"])}"{" checked" if j != 1 else ""}><span class="bm__box" aria-hidden="true"></span>'
        f'<span class="bm__n"><b>{e(g["name"])}</b><small>{e(g["text"])}</small></span><span class="bm__p">{g["preis"]}</span></label>' for j, g in enumerate(m['gerichte'])) + '</fieldset>'
        for i, m in enumerate(BANKETT['menues']))
    n = b['personen']
    return f'''<section class="teil f-hell bm-blau" id="etagen" aria-label="Ihr Menü">
  <div class="innen">
    <div class="bm">
      <div class="bm__l">
        {foto('mi-teller', '(max-width:900px) 92vw, 36vw', 'bm__f')}
        <div class="bm__text"><h2 class="t2" data-schlitz>Ihr Menü, <em>Gericht für Gericht.</em></h2>
          <p class="lauf" data-r="text">Aus unseren Bankettmenüs wählen Sie drei bis fünf Gerichte, gemischt über die Jahreszeiten, soweit es die Saison erlaubt.</p>
          <p class="lauf" data-r="text">{e(b['platz'])}</p></div>
      </div>
      <div class="bm__karte" data-r="text">
        <div class="bm__kopf">{zeichen}<p class="bm__haus">Wirtschaft am Schlössli</p><p class="bm__titel">Bankett</p>
          <div class="bm__saison" role="tablist" aria-label="Jahreszeit">{tabs}</div></div>
        <div class="bm__stapel">{felder}</div>
        <label class="bm__gaeste"><span>Gäste</span><input type="range" min="6" max="{n}" value="18" aria-label="Anzahl Gäste"><output>18</output></label>
        <div class="bm__summe" aria-live="polite"><p><b data-bm-n>4</b><span>Gänge</span></p><p><b data-bm-p>145</b><span>Franken je Gast</span></p><p class="bm__total"><b data-bm-t>2610</b><span>Franken für <i data-bm-g>18</i> Gäste</span></p></div>
        <p class="bm__warn" data-bm-w hidden>Bitte drei bis fünf Gerichte wählen.</p>
        <div class="bm__an">{knopf('Mit dieser Auswahl anfragen', '#', dunkel=False, attr=' data-fenster="fe-bankett" data-bm-anfrage')}<small>Richtwert für die Speisen, nach den Preisen der Bankettmenüs.</small></div>
      </div>
    </div>
  </div>
</section>
'''

def feiern_seite():
    b = HAUS['bankett']
    # Kopf: Robert 19.10.2026, 21:05, Fassung 41 aus _varianten/feiern-kopf-20.html, 21:15 doch wie im Vorschlag:
    # ein Bild der blauen Stühle am See, schräg geschnitten, links im Original, rechts in Nachtblau; Platte rechts unten.
    inhalt = f'''<section class="kopf-schnitt" id="kopf" aria-label="Banketts und Gruppen">
  <figure class="ks__s ks__s--nacht" aria-hidden="true">{img('start', '100vw', eager=True, alt='')}</figure>
  <figure class="ks__s ks__s--tag">{img('start', '100vw', eager=True)}</figure>
  <div class="ks__p" data-r="text"><h1>Banketts &amp; <em>Gruppen.</em></h1><p class="lauf">{e(b["fett"])}</p>
    <div class="knoepfe">{knopf("Bankettanfrage", "#", attr=' data-fenster="fe-bankett"')}<a class="leise" href="#menues">Bankettmenüs</a></div></div>
</section>
'''
    inhalt += bankett_rechner(b) + f'''
<section class="teil f-dunkel" id="menues" aria-label="Bankettmenüs">
  <div class="innen">
    <div class="mk-kopf">
      <span class="mk-kopf__zeichen" aria-hidden="true" data-r="text">{zeiger(46)}</span>
      <h2 class="mk-kopf__t" data-schlitz>Frühling, Sommer, <em>Herbst.</em></h2>
      <p class="lauf mk-kopf__satz" data-r="text">{e(BANKETT['hinweis'])}</p>
    </div>
    <div class="mk-tisch" data-r="bild">{''.join(mk_karte(i, m) for i, m in enumerate(BANKETT['menues']))}</div>
    <p class="mk-nachweis">{' · '.join(nw(n, tag='span') for n in MK_FOTO.values())}</p>
    <div class="ka__weiter">{knopf('Bankettanfrage', '#', dunkel=True, attr=' data-fenster="fe-bankett"')}<a class="leise" href="unterlagen/pdf/bankett.pdf" target="_blank" rel="noopener">Bankettmenüs als PDF</a></div>
  </div>
</section>
'''
    seite('feiern.html', f'Banketts & Gruppen · {HAUS["name"]}', 'Familien- und Firmenfeiern auf zwei Etagen für jeweils bis zu 26 Personen, Tavolata oder gesetztes Menü, Bankettmenüs für Frühling, Sommer und Herbst.', inhalt)


def anlaesse_seite():
    # «Angeschlagen am Hafen» (F.kalender) gestrichen, Robert 20.10.2026: zeigte dieselben Anlässe wie «Der nächste Termin» und «Was war»
    a = HAUS['anlaesse']
    n = a[0]
    # Anlass-Seite «Teller zuerst» (Robert 19.10.2026, Fassung 14 aus _varianten-kreuzfahrt): der nächste Termin gross mit Teller und Abzug,
    # die vergangenen in derselben Handschrift darunter, Foto ganz gezeigt (Rahmen folgt dem Bild), Seiten im Wechsel
    # Rückblick «Kontaktbogen» (Robert 19.10.2026, Fassung 1 aus _varianten/was-war-15.html): ein Filmstreifen von Rand zu Rand läuft
    # ohne Halt durch, auch unter der Maus; ein Tipp auf ein Bild legt es als grosse Kachel darunter, Text rechts, Pfeile darunter.
    vorbei = a[1:]
    def tag_monat(d):
        t = re.findall(r'(\d+)\.', d)
        m = re.search(r'(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember) (\d{4})', d)
        return ('–'.join(x.zfill(2) for x in t[:2]), m.group(1), m.group(2), d.split(',')[0] if ',' in d else '')
    bild_nr = [f'{(j % len(vorbei)) + 1 + (j // len(vorbei)) * len(vorbei)}A' for j in range(len(vorbei) * 3)]
    def oben(x):  # Hochformat (Porträts) oben anschneiden, damit das Gesicht im Bild bleibt
        return '50% 12%' if B[x['bild']]['h'] * 1.45 > B[x['bild']]['w'] else '50% 50%'
    def film_bild(j):
        x = vorbei[j % len(vorbei)]
        return f'<button type="button" class="kbg__k" data-kbg="{j % len(vorbei)}" aria-label="{e(x["titel"])} zeigen"><span class="kbg__nr">{bild_nr[j]}</span>{img(x["bild"], "(max-width:900px) 40vw, 250px", alt="").replace(" data-src=", f" style=\"object-position:{oben(x)}\" src=").replace(" data-srcset=", " srcset=")}<small>{e(x["titel"])}</small></button>'
    satz = ''.join(film_bild(j) for j in range(len(vorbei) * 3))
    film = f'<div class="kbg__band" aria-hidden="false"><div class="kbg__lauf">{satz}<span class="kbg__kopie" aria-hidden="true">{satz}</span></div></div>'
    def buehne(i, x):
        tg, mo, jr, wt = tag_monat(x['datum'])
        zeit, _, ort = x['zeit'].partition(' · ')
        link = f'<p class="kbg__mehr"><a class="leise" href="{x["link"]}" rel="noopener" target="_blank">{e(x["link_text"])}</a></p>' if x.get('link') else ''
        zeilen = f'<div class="kbg__info"><p><span class="mono">Wann</span><span>{e(zeit)}</span></p>' + (f'<p><span class="mono">Wo</span><span>{e(ort)}</span></p>' if ort else '') + '</div>'
        return (f'<div class="kbg__s" data-kbg-s="{i}"{"" if i == 0 else " aria-hidden=\"true\""}>'
                f'<figure class="foto kbg__bild" style="background-image:url({B[x["bild"]]["abbild"]})">{img(x["bild"], "(max-width:900px) 92vw, 52vw").replace("<img ", f"<img style=\"object-position:{oben(x)}\" ", 1)}</figure>'
                f'<div class="kbg__t"><div class="kbg__datum"><b>{tg}</b><span>{e(mo)} {jr}{"<br>" + e(wt) if wt else ""}</span></div>'
                f'<h3>{e(x["titel"])}</h3>{"".join(f"<p class=\"lauf\">{e(t)}</p>" for t in x["text"])}{zeilen}{link}</div></div>')
    pfeil_l = '<span class="kn"><svg class="pf" viewBox="0 0 16 10" aria-hidden="true" style="transform:scaleX(-1)"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span>'
    rueck = (f'{film}<div class="innen"><div class="kbg__buehne" aria-live="polite">{"".join(buehne(i, x) for i, x in enumerate(vorbei))}</div>'
             f'<div class="kbg__pfeile"><button type="button" class="kbg__p" data-kbg-p="-1" aria-label="Anlass davor">{pfeil_l}</button>'
             f'<p class="mono kbg__stand" data-kbg-stand>{e(vorbei[0]["titel"])}</p>'
             f'<button type="button" class="kbg__p" data-kbg-p="1" aria-label="Nächster Anlass">{PFEIL}</button></div></div>')
    # Kopf: Robert 19.10.2026, Fassung 6 «Nachtblaue Spalte» aus _varianten/events-kopf-runde4.html (ersetzt das Passepartout mit dem Abendschiff):
    # links eine nachtblaue Spalte mit hellem Titel, Satz und dem nächsten Anlass, rechts das Feuerwerk vom Seenachtfest über zwei Drittel.
    kommt = next(a for a in HAUS['anlaesse'] if a['bevorstehend'])
    inhalt = f'''<section class="esp f-dunkel" id="kopf">
  <div class="esp__t"><h1>Events &amp; <em>Termine.</em></h1><p class="lauf">Gemeinsam mit Gastköchen, an Bord und am Hafen.</p><p class="mono esp__nx">Als Nächstes · {e(kommt['datum'])} · {e(kommt['titel'])}</p></div>
  <figure class="esp__bild" style="background:url({B['feuerwerk-ki']['abbild']}) center/cover">{img('feuerwerk-ki', '(max-width:860px) 100vw, 67vw', eager=True)}</figure>
</section>
'''
    inhalt += f'''<section class="teil f-hell tz" id="naechster" aria-label="Der nächste Termin">
  <div class="tz__bild">{foto(n['bild'], '(max-width:900px) 100vw, 50vw', 'tz__teller')}{foto(n['bild_klein'], '240px', 'tz__klein')}</div>
  <div class="tz__t">
    <p class="mono" data-r="text">Excellence Countess · 13.–15. November</p>
    <h2 class="tz__vier" data-r="text">Four<br>Hands.</h2>
    <p class="tz__namen mono" data-r="text">Dieter Koschina<i></i>Monika Huber</p>
    <h3 class="tz__titel" data-r="text">{e(n['titel'])}</h3>
    {''.join(f'<p class="lauf" data-r="text">{e(t)}</p>' for t in n['text'][1:])}
    <p class="mono tz__zeit" data-r="text">{e(n['zeit'])}</p>
    <p class="knoepfe" style="margin-top:28px">{knopf('Zum Gourmetfestival', n['link'], dunkel=True, attr=' rel="noopener" target="_blank"')}</p>
  </div>
</section>
<script type="application/json" id="anlaesse-daten">{json.dumps(a, ensure_ascii=False)}</script>
<section class="teil f-hell kbg" id="rueckblick" aria-label="Rückblick" data-kbg-root>
  <div class="innen">
    <h2 class="t2" data-schlitz style="margin-bottom:clamp(30px,3vw,48px)">Was <em>war.</em></h2>
  </div>
  {rueck}
</section>
'''
    seite('anlaesse.html', f'Events & Termine · {HAUS["name"]}', 'Die Excellence Gourmetkreuzfahrt mit Dieter Koschina und Monika Huber vom 13. bis 15. November 2026 und die Anlässe der Wirtschaft am Schlössli.', inhalt)


def team_seite():
    leute = [t for t in HAUS['team'] if t['bild']]
    ohne = [t for t in HAUS['team'] if not t['bild']]
    menschen = ''.join(f'<div class="mensch">{foto(t["bild"], "(max-width:520px) 92vw, (max-width:820px) 46vw, 30vw")}<div class="schild" data-r="text"><h3>{e(t["name"])}</h3><p>{e(t["rolle"])}</p></div></div>' for t in leute)
    weitere = ''.join(f'<div class="mensch"><div class="schild" data-r="text"><h3>{e(t["name"])}</h3><p>{e(t["rolle"])}</p></div></div>' for t in ohne)
    # Kopf als Bühne (Robert 19.10.2026, Fassung 2 aus _varianten/team-15.html): Gruppenbild breit oben, Titel und Satz mittig darunter
    inhalt = f'''<section class="kopf kopf--buehne f-tapete" id="kopf">
  <figure class="kopf__bild" style="background:url({B['team']['abbild']}) center/cover">{img('team', '(max-width:860px) 100vw, 92vw', eager=True)}</figure>
  <div class="kopf__t"><h1>Das <em>Team.</em></h1></div>
  <div class="kopf__unter"><p class="lauf">{e(HAUS["satz_team"])}</p></div>
</section>
'''
    inhalt += f'''<section class="teil f-hell" id="menschen" aria-label="Menschen">
  <div class="innen">
    <div class="leute">{menschen}</div>
    <div class="leute2">{weitere}</div>
  </div>
</section>
''' + F.kueche_blick(foto) + F.schwester()
    seite('team.html', f'Über uns · {HAUS["name"]}', 'Das Team der Wirtschaft am Schlössli: Küchenchefin Monika Huber, Gastgeber und Sommelier Jonas Volpert, Sous-Chef Lukas Siebel, Marco Reisinger und Ole Sass.', inhalt)


def kontakt_seite():
    h = HAUS; z = h['zeiten']
    lat, lon = h['koordinaten']
    osm = f'https://www.openstreetmap.org/export/embed.html?bbox={lon - .006}%2C{lat - .003}%2C{lon + .006}%2C{lat + .003}&amp;layer=mapnik&amp;marker={lat}%2C{lon}'
    # Kopf «Briefkopf» (Robert 19.10.2026, 21:1x, Fassung 03 aus _varianten/kontakt-links.html): links alles mittig wie auf dem
    # Briefpapier des Hauses, Zeichen, Wortmarke, Titel, Satz, Adresse, Tage und Zeiten; rechts das Schild wie bisher.
    inhalt = f'''<section class="kopf kopf--brief f-tapete" id="kopf">
  <div class="kopf__t kb">
    {zeichen(58)}<p class="kb__wm">{e(h["wortmarke"])}</p><p class="kb__by">{e(h["by"])}</p><i class="kb__li" aria-hidden="true"></i>
    <h1>Kontakt &amp; <em>Öffnungszeiten.</em></h1><p class="lauf">{e(h["satz_lage"])}</p><i class="kb__li" aria-hidden="true"></i>
    <p class="kb__adr">{e(h["strasse"])}<br>{e(h["ort"])}</p><p class="kb__zeit">{e(z["tage"].replace(' - ', ' bis '))} · {e(z["offen"].replace(' Uhr', '').replace(' - ', ' bis '))} Uhr</p>
    <div class="knoepfe">{knopf("Tisch reservieren", RES, dunkel=True, attr=" data-fenster=\"fe-reservation\"")}<a class="leise" href="tel:{h["telefon_href"]}">{e(h["telefon"])}</a></div>
  </div>
  <figure class="kopf__bild" style="background:url({B['schild']['abbild']}) center/cover">{img('schild', '(max-width:860px) 100vw, 40vw', eager=True)}</figure>
</section>
'''
    # Anfahrt «Nachtblaue Seekarte» (Fassung 06 aus _varianten/anfahrt-20.html, Robert 19.10.2026). Zeiten und Kontakt stehen im Fuss.
    def grad(v, p, n):
        a = abs(v); return f"{int(a)}°{round(a % 1 * 60):02d}′ {p if v >= 0 else n}"
    wellen = ''.join(f'<path d="M-20 {120 + i * 46} C 240 {90 + i * 46 + (i % 3) * 18}, 520 {150 + i * 46}, 760 {116 + i * 46} S 1200 {80 + i * 46 + (i % 2) * 30}, 1460 {130 + i * 46}"/>' for i in range(16))
    inhalt += f'''<section class="teil ank" id="anreise" aria-label="Anfahrt">
  <svg class="ank__wl" viewBox="0 0 1440 900" preserveAspectRatio="none" aria-hidden="true">{wellen}</svg>
  <div class="innen ank__g">
    <div class="ank__pos" data-r="text"><i aria-hidden="true"></i><p class="ank__gr">{grad(lat, 'N', 'S')}<br>{grad(lon, 'E', 'W')}</p><p class="mono">{e(h['strasse'])} · {e(h['ort'])}</p></div>
    <div class="ank__tx">
      <h2 class="t2" data-schlitz style="margin-bottom:22px">Anfahrt.</h2>
      <p class="lauf" data-r="text">{e(h['anfahrt'])}</p>
      <p class="lauf" data-r="text" style="--i:1">Der Bahnhof Bottighofen liegt in der Nähe, Parkplätze gibt es ausreichend.</p>
      <p class="ank__l" data-r="text" style="--i:2"><a class="leise" href="https://www.openstreetmap.org/?mlat={lat}&amp;mlon={lon}#map=17/{lat}/{lon}" rel="noopener" target="_blank">Auf der Karte ansehen</a><a class="leise" href="https://www.openstreetmap.org/directions?to={lat}%2C{lon}" rel="noopener" target="_blank">Route planen</a></p>
    </div>
  </div>
</section>
''' + F.see(foto, nw)
    seite('kontakt.html', f'Kontakt & Öffnungszeiten · {HAUS["name"]}', 'Öffnungszeiten, Küchenzeiten, Ferien, Anfahrt und Reservation der Wirtschaft am Schlössli, Seestrasse 50, 8598 Bottighofen.', inhalt)


def gutschein_seite():
    inhalt = seitenkopf('torte', 'Ein <em>Gutschein.</em>', f'<p class="lauf">Für einen Abend unter der Platane, einen Lunch am Hafen oder die Lästermeile. {e(HAUS["gutschein"]["bestaetigung"])}.</p><div class="knoepfe">{knopf("Gutschein bestellen", "#", dunkel=True, attr=" data-fenster=\"fe-gutschein\"")}</div>', hzk=.6)
    inhalt += F.gutschein_inhalt()
    seite('gutschein.html', f'Gutschein · {HAUS["name"]}', 'Einen Gutschein der Wirtschaft am Schlössli bestellen.', inhalt)


def abend_seite():
    inhalt = seitenkopf('lounge', 'Ihr Abend <em>am Tisch.</em>', f'<p class="lauf">Stellen Sie Ihren Besuch zusammen: Anlass, Tag, Menü aus unserer Karte, die Flasche aus dem Keller, Allergien und Wünsche. Daraus wird eine fertige Anfrage.</p><div class="knoepfe"><a class="leise" href="#zusammenstellen">Zusammenstellen</a><a class="leise" href="weinkarte.html?von=abend#berater">Zum Weinberater</a></div>', hzk=.6)
    inhalt += F.abend_inhalt()
    seite('abend.html', f'Ihr Abend · {HAUS["name"]}', 'Einen Abend in der Wirtschaft am Schlössli zusammenstellen: Anlass, Menü, Wein, Allergien und Wünsche als fertige Anfrage.', inhalt)


def md_zu_html(t):
    """Kleiner Umsetzer für die Rechtstexte des Hauses: Überschriften, Absätze, Listen, Fett, Zeilenumbruch. Der Wortlaut bleibt."""
    zeilen = t.splitlines()
    # Kopfzeilen der Sammlung (Quelle, Abgerufen) gehören nicht zum Text
    while zeilen and (zeilen[0].startswith(('Quelle:', 'Abgerufen:')) or not zeilen[0].strip()):
        zeilen.pop(0)
    out, para, liste = [], [], None

    def inline(s):
        s = e(s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
        s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" rel="noopener" target="_blank">\1</a>', s)
        s = s.replace('\\', '')
        return s

    def flush():
        nonlocal para
        if para:
            txt = '<br>'.join(inline(p.rstrip()) for p in para)
            out.append(f'<p>{txt}</p>'); para = []

    def lzu():
        nonlocal liste
        if liste:
            tag = liste[0]
            out.append(f'<{tag}>' + ''.join(f'<li>{x}</li>' for x in liste[1]) + f'</{tag}>'); liste = None

    for z in zeilen:
        s = z.rstrip('\n')
        if not s.strip():
            flush(); lzu(); continue
        m = re.match(r'^(#{2,4})\s+(.*)$', s)
        if m:
            flush(); lzu()
            out.append(f'<h{"2" if len(m.group(1)) <= 3 else "3"}>{inline(m.group(2))}</h{"2" if len(m.group(1)) <= 3 else "3"}>'); continue
        lm = re.match(r'^(\d+)\.\s+(.*)$', s) or re.match(r'^[-*]\s+(.*)$', s)
        if lm and not s.startswith('\t'):
            flush()
            tag = 'ol' if s[0].isdigit() else 'ul'
            if not liste or liste[0] != tag:
                lzu(); liste = [tag, []]
            liste[1].append(inline(lm.group(lm.lastindex))); continue
        if s.startswith('\t') and liste:
            liste[1][-1] += '<br>' + inline(s.strip()); continue
        lzu(); para.append(s.strip() if not s.endswith('  ') else s.strip())
    flush(); lzu()
    return '\n'.join(out)


def recht_seite(datei, quelle, titel):
    t = (Q / 'website' / 'text' / quelle).read_text()
    zusatz = ''
    if datei == 'impressum.html':
        frei = [n for n in B if B[n].get('nachweis')]
        zusatz = '<h2>Bildnachweis</h2><p>Fotos des Hauses: Wirtschaft am Schlössli. Freie Bilder von Wikimedia Commons:</p><ul>' + ''.join(f'<li>{e(B[n]["alt"])}: <a href="{e(B[n]["nachweis"]["quelle"])}" rel="noopener" target="_blank">{e(B[n]["nachweis"]["urheber"])}</a>, {e(B[n]["nachweis"]["lizenz"])}, {e(B[n]["nachweis"]["jahr"])}</li>' for n in frei) + '</ul>'
    inhalt = klein_kopf(f'{e(titel)}<em>.</em>') + f'<section class="teil f-hell" id="wortlaut" aria-label="{e(titel)}" style="padding-top:clamp(40px,4vw,70px)"><div class="innen"><div class="recht">{md_zu_html(t)}{zusatz}</div></div></section>\n'
    seite(datei, f'{titel} · {HAUS["name"]}', f'{titel} der Wirtschaft am Schlössli im Wortlaut des Hauses.', inhalt)


def nicht_gefunden():
    inhalt = f'<section class="nicht f-tapete" id="kopf"><div><h1>Diese Seite gibt es <em style="font-style:normal;color:var(--himmel-t)">nicht.</em></h1><p class="lauf" style="margin:0 auto 28px">{e(HAUS["satz_lage"])}</p>{knopf("Zur Startseite", "index.html", dunkel=True)}</div></section>\n'
    seite('404.html', f'Seite nicht gefunden · {HAUS["name"]}', 'Diese Seite gibt es nicht.', inhalt)


def nebendateien():
    seiten = ['', 'abend', 'karte', 'weinkarte', 'feiern', 'anlaesse', 'team', 'kontakt', 'gutschein', 'impressum', 'datenschutz', 'agb']
    (HIER / 'robots.txt').write_text('User-agent: *\nDisallow: /\n# Designstudie: bleibt bis zur Freigabe ausserhalb der Suchmaschinen.\nSitemap: https://www.schloessli-bottighofen.ch/sitemap.xml\n')
    (HIER / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>https://www.schloessli-bottighofen.ch/{s}</loc></url>\n' for s in seiten) + '</urlset>\n')


if __name__ == '__main__':
    startseite()
    karte_seite()
    weinkarte_seite()
    feiern_seite()
    anlaesse_seite()
    team_seite()
    kontakt_seite()
    gutschein_seite()
    abend_seite()
    recht_seite('impressum.html', 'impressum.md', 'Impressum')
    recht_seite('datenschutz.html', 'datenschutzerklarung.md', 'Datenschutzerklärung')
    recht_seite('agb.html', 'agbs.md', 'AGB')
    nicht_gefunden()
    nebendateien()

    # Station 14 (Werkbank-Bauer, 19.10.2026): Werkzeuge anschliessen (Rahmen der Werkzeuge kopieren, Schreibtisch nachziehen)
    import subprocess as _sp
    _sp.run(["python3", str(HIER / "_werkbank" / "sb_anschluss.py")])
