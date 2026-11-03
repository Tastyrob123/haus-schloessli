"""Unterlagen der Wirtschaft am Schlössli, neu gesetzt in der Machart des Hauses (Station 10, Kartenmacher, 19.10.2026).

Robert, 19.10.2026: «ich finde deren Unterlagen ehrlicherweise viel schöner als unsere.» Deshalb ist die Idee hier keine fremde Vorlage
mit Kopfband, sondern die Karte des Hauses selbst, sauber gesetzt (Master Website-Bau Abschnitt 8: «in den Farben und mit den Zeichnungen
des jeweiligen Hauses, kreativ so, wie die es gemacht haben»): Garamond wie im Original, Gerichte in blauen Kapitälchen, das Blatt-Ornament
zwischen zwei Doppellinien über jeder Rubrik, die Länderumrisse der Speisekarte (nachgezogen aus dem Original, sb_zeichnungen.py),
Lästermeile und Lunch mittig wie beim Haus. Neu sind nur Ordnung und Feinheit: feste Spalten für Kürzel und Preise, ruhige Abstände,
gleiche Gestalt für jeden Eintrag, Blau der neuen Website (Ton in Ton), scharfe Linien statt Bilder.

Nichts ist abgetippt: Jeder Name, jeder Text, jeder Preis kommt aus den Kartendaten `../_karten/stand/<karte>.json`, die `_karten/lesen.py`
aus den Original-PDFs liest und `_karten/abgleich.py` Wort für Wort gegen das Original prüft. Dieselben Daten liest La Carte.
Je Seite des Originals ein Blatt (Bankettmenü: jedes Menü ganz auf einer Seite), damit die Unterlagen-Seite Seite für Seite vergleicht.
Eindeutige Tippfehler werden in der Idee berichtigt (Liste `../_karten/berichtigt.json`, gezählt, als dazu/fehlt in satz_pruefe.py).
Bewusst anders: Fuss mit der Adresse des Hauses; Weinkarte ohne das weisse, unsichtbare «A» auf Seite 1 und ohne die Seitenzahlen
«– 2 –» … «– 27 –» des Originals; «1er» ohne Hochstellung."""
import json, os, re
import satz_kern as S
from kern import H, ROOT

KARTEN = os.path.join(ROOT, '..', '_karten')
SB = os.path.join(ROOT, '_werkbank', 'sb')
Q = '../_quelle/website/pdf/'
e = S.e

# Farben der neuen Website (Ton in Ton, website/assets/css/haus.css, gemessen 19.10.2026)
BLAU, BLAU_T, HIMMEL, TINTE, LEISE, PAPIER = '#113D88', '#0A2552', '#A2B6CF', '#041023', '#3B4A60', '#FFFFFF'

_B = json.load(open(os.path.join(KARTEN, 'berichtigt.json'), encoding='utf-8'))['stellen']
GENUTZT = {}
_karte = ['']


def r(t):
    """Wortlaut des Hauses → berichtigter Wortlaut der Idee. Merkt sich jede Ersetzung je Karte."""
    n = len(re.findall(r'\b1 er\b', t))
    if n:
        GENUTZT.setdefault(_karte[0], []).extend([('1 er', '1er')] * n)
        t = re.sub(r'\b1 er\b', '1er', t)
    for b in _B:
        if b['karte'] == _karte[0] and b['alt'] in t:
            GENUTZT.setdefault(_karte[0], []).extend([(b['alt'], b['neu'])] * t.count(b['alt']))
            t = t.replace(b['alt'], b['neu'])
    return t


def x(t):
    return e(r(t), quote=False)


def _kk(t, nur_erstes):
    """Kapitälchen wie Word sie setzt: Versalien, grosse Buchstaben voll, die übrigen kleiner. Von Hand gesetzt, weil die nachgebauten
    Kapitälchen der Schrift die Umlaute verziehen («Frühling»)."""
    aus, erstes = [], True
    for w in t.split(' '):
        if not w:
            continue
        i = next((k for k, c in enumerate(w) if c.isalpha()), None)
        if i is None or (nur_erstes and not erstes):
            aus.append(f'<span class="kl">{e(w.upper())}</span>' if i is not None else e(w))
        else:
            aus.append(e(w[:i + 1].upper()) + (f'<span class="kl">{e(w[i + 1:].upper())}</span>' if w[i + 1:] else ''))
        erstes = False
    return ' '.join(aus)


def kap1(t):
    """Gerichtname: nur der erste Buchstabe gross («Quinto quarto», «Carré di cervo»), wie im Original."""
    return _kk(r(t), True)


def kap(t):
    """Titel: erster Buchstabe jedes Worts gross («Iberische Halbinsel»)."""
    return _kk(r(t), False)


def svg(name, kl):
    s = open(os.path.join(SB, name + '.svg'), encoding='utf-8').read()
    return s.replace('<svg ', f'<svg class="{kl}" aria-hidden="true" ', 1)


def ornament():
    return f'<div class="sb-orn"><i></i>{svg("blatt", "sb-blatt")}<i></i></div>'


def mx(blatt, wert):
    return blatt.replace('<section class="blatt', f'<section data-max="{wert}" class="blatt', 1)


def karte(kid):
    return json.load(open(os.path.join(KARTEN, 'stand', kid + '.json'), encoding='utf-8'))


def posten_von(k):
    return [p for t in k['karte']['teile'] if t['art'] == 'inhalt' for p in t['posten'] if not p.get('aus')]


def nach_seiten(k, ganz=True):
    seiten, s = {}, 1
    for p in posten_von(k):
        if not ganz or p['t'] == 'rubrik':
            s = p.get('s', 1)
        seiten.setdefault(s, []).append(p)
    return [seiten[n] for n in sorted(seiten)]


def kuerzel(z):
    """Kürzel des Hauses (VEG/G/L …). Robert 19./20.10.2026: Schrägstrich-Kette und Punkt-Kette über der Preisspalte «richtig hässlich».
    Jetzt klein und hochgestellt am Ende der Beschreibung, nur mit feinem Abstand getrennt; VEG und OVEG mit einem kleinen Blatt."""
    if not z:
        return ''
    aus = []
    for t in r(z).split('/'):
        if t == 'VEG':
            aus.append(f'<b class="sb-veg">{BLATT_VOLL}{e(t)}</b>')
        elif t == 'OVEG':
            aus.append(f'<b class="sb-veg">{BLATT_OFFEN}{e(t)}</b>')
        else:
            aus.append(e(t))
    return '<sup class="sb-kz">' + '<i class="sb-ab"> </i>'.join(aus) + '</sup>'


BLATT_VOLL = '<svg class="sb-vb" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 8.5C2 4 5 1.5 8.5 1.5 8.5 5.5 6 8.5 2 8.5Z" fill="currentColor"/><path d="M2 8.5 6.5 4" stroke="#fff" stroke-width=".7" fill="none"/></svg>'
BLATT_OFFEN = '<svg class="sb-vb" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 8.5C2 4 5 1.5 8.5 1.5 8.5 5.5 6 8.5 2 8.5Z" fill="none" stroke="currentColor" stroke-width=".8"/></svg>'

# ---------------------------------------------------------------- Flaggen (Robert 19.10.2026: «kleine Flaggen zumindest bei den Ländern»)
def _flagge(innen):
    return f'<svg class="sb-flagge" viewBox="0 0 30 20" aria-hidden="true">{innen}<rect x=".3" y=".3" width="29.4" height="19.4" rx="2" fill="none" stroke="rgba(4,16,35,.18)" stroke-width=".6"/></svg>'


_q = lambda *f: ''.join(f'<rect x="{10 * i}" width="10" height="20" fill="{c}"/>' for i, c in enumerate(f))
_w = lambda *f: ''.join(f'<rect y="{20 / len(f) * i:.3f}" width="30" height="{20 / len(f):.3f}" fill="{c}"/>' for i, c in enumerate(f))
FLAGGE = {
    'SCHWEIZ': _flagge('<rect width="30" height="20" fill="#DA291C"/><rect x="13" y="4.5" width="4" height="11" fill="#fff"/><rect x="9.5" y="8" width="11" height="4" fill="#fff"/>'),
    'DEUTSCHLAND': _flagge(_w('#000', '#DD0000', '#FFCE00')),
    'ÖSTERREICH': _flagge(_w('#C8102E', '#fff', '#C8102E')),
    'ITALIEN': _flagge(_q('#009246', '#fff', '#CE2B37')),
    'FRANKREICH': _flagge(_q('#0055A4', '#fff', '#EF4135')),
    'SPANIEN': _flagge('<rect width="30" height="20" fill="#AA151B"/><rect y="5" width="30" height="10" fill="#F1BF00"/>'),
    'PORTUGAL': _flagge('<rect width="30" height="20" fill="#DA291C"/><rect width="12" height="20" fill="#046A38"/><circle cx="12" cy="10" r="3.4" fill="#FFE900"/>'),
}


FEST = {'TAPAS DURCHGEHEND': 'Tapas durchgehend', 'IBERISCHE HALBINSEL': 'Iberische Halbinsel', 'ROSÉ WEINE': 'Rosé Weine',
        'CHAMPAGNER/SCHAUMWEIN': 'Champagner/Schaumwein'}
KLEIN = {'de', 'del', 'des', 'du', 'di', 'la', 'le', 'et', 'am', 'by'}


def normal(t):
    """Versal gesetzte Titel in normaler Schreibung («RIBERA DEL DUERO» → «Ribera del Duero»). Robert 19.10.2026: «Das muss auch nicht
    alles in Grossbuchstaben stehen». Gemischt Gesetztes bleibt, wie es ist."""
    t = r(t)
    if t in FEST:
        return FEST[t]
    if t != t.upper():
        return t
    def wort(w, erstes):
        teile = re.split(r'([-/.])', w.lower())
        return ''.join(q if q in '-/.' or not q else (q if (q in KLEIN and not erstes) else q[0].upper() + q[1:]) for q in teile)
    return ' '.join(wort(w, i == 0) for i, w in enumerate(t.split(' ')))


def land_teile(t):
    """«SPANIEN - RIOJA», «SCHWEIZ GRAUBÜNDEN», «Schweiz» → (Land wie geschrieben, Rest wie geschrieben) oder None."""
    for l in FLAGGE:
        if t.upper().startswith(l):
            rest = t[len(l):].strip(' -')
            return t[:len(l)], rest
    return None


def land_kopf(text, rest='', klein=False):
    r_ = f'<h3 class="sb-region">{e(normal(rest))}</h3>' if rest else ''
    return (f'<h3 class="sb-land{" sb-land--klein" if klein else ""}">{FLAGGE[text.upper()]}<span>{e(normal(text))}</span></h3>' + r_)


# ---------------------------------------------------------------- à la carte: Speisekarte und Bankettmenü
LAND = {'FRANKREICH': 'frankreich', 'ITALIEN': 'italien', 'IBERISCHE HALBINSEL': 'iberien'}


def preis_html(p):
    """Preis rechts; der zweite Preis mit Angabe darunter als «Hauptgang 65» in normaler Schreibung (Robert 20.10.2026: das Versal-Etikett
    «HAUPTGANG» ist hässlich)."""
    ein = p.get('einheiten') or [''] * len(p.get('preise', []))
    return ''.join(f'<span>{f"<em>{x(b)}</em>" if b else ""}<b>{x(a)}</b></span>' for a, b in zip(p.get('preise', []), ein))


def gericht(p):
    hin = [z['text'] for z in p.get('zeilen', [])]
    warte = [t for t in hin if t.startswith('(')]            # «(20 MIN. WARTEZEIT)»: klein unter der Beschreibung
    text = [t for t in hin if not t.startswith('(')]
    kz = kuerzel(p.get('zusatz', ''))
    zeilen = [x(t) for t in text] or ['']
    zeilen[-1] = zeilen[-1] + (f' {kz}' if kz else '')
    zeilen += [f'<span class="sb-w">{x(t)}</span>' for t in warte]
    return (f'<div class="sb-g"><p class="sb-n">{kap1(p["name"])}</p><p class="sb-p">{preis_html(p)}</p>'
            + ''.join(f'<p class="sb-t">{z}</p>' for z in zeilen) + '</div>')


def a_la_carte(kid, mass):
    _karte[0] = kid
    k = karte(kid)
    seiten = nach_seiten(k)
    anzahl = [sum(1 for p in ps if p['t'] == 'gericht') for ps in seiten]
    blaetter = []
    deckel = next((t for t in k['karte']['teile'] if t['art'] == 'deckel' and t.get('aus_original')), None)
    for i, ps in enumerate(seiten):
        teile, fuss, offen = [], [], False
        if i == 0 and deckel:                        # Titel, den das Original selbst trägt (Bankettmenü)
            teile.append(f'<h1 class="sb-titel">{x(deckel["titel"])}</h1>')
        for j, p in enumerate(ps):
            if p['t'] == 'rubrik':
                karte_svg = svg(LAND[p['titel']], 'sb-umriss sb-umriss--' + LAND[p['titel']]) if p['titel'] in LAND else ''
                m = re.match(r'^(.*?)\s+\((\d+) (CHF)\)$', p['titel'])
                if m:                                # Bankett: Jahreszeit gross, der Menüpreis als eigene Marke darunter
                    titel = (f'<h2 class="sb-saison">{e(normal(m.group(1)))}</h2>'
                             f'<p class="sb-menupreis"><i></i><span>(<b>{e(m.group(2))}</b> {e(m.group(3))})</span><i></i></p>')
                else:
                    titel = f'<h2 class="sb-h">{kap(p["titel"])}</h2>'
                if offen:
                    teile.append('</section>')
                offen = True
                teile.append(f'<section class="sb-r{" sb-r--karte" if kid == "speisekarte" else ""}">{ornament()}{titel}{karte_svg}')
            elif p['t'] == 'gericht':
                teile.append(gericht(p))
            elif p['t'] == 'notiz':
                ziel = fuss if all(q['t'] == 'notiz' for q in ps[j:]) else teile
                ziel.append(f'<p class="sb-notiz">{x(p["text"])}</p>')
        if offen:
            teile.append('</section>')
        if i == len(seiten) - 1 and k['karte'].get('fuss'):
            fuss.append(f'<p class="sb-notiz">{x(k["karte"]["fuss"])}</p>')
        if fuss:
            teile.append('<div class="sb-fuss">' + ''.join(fuss) + '</div>')
        luft = ' sb-luft' if anzahl[i] < 0.7 * max(anzahl) else ''
        blaetter.append(mx(S.blatt(*teile, kl='sb-haus' + luft), mass))
    return k, blaetter


# ---------------------------------------------------------------- Lästermeile: mittig, beide Titel in derselben Form (Robert 19.10.2026)
def laestermeile(mass):
    _karte[0] = 'laestermeile'
    k = karte('laestermeile')
    teile = []
    for p in posten_von(k):
        if p['t'] == 'rubrik':
            teile.append(f'{ornament()}<h2 class="sb-band">{e(normal(p["titel"]))}</h2>')
        elif p['t'] == 'gericht':
            zeilen = [x(z['text']) for z in p.get('zeilen', [])]
            if p.get('zusatz'):                        # Kürzel am Ende der Beschreibung, wie beim Haus
                k_ = f' {kuerzel(p["zusatz"])}'
                zeilen = zeilen[:-1] + [zeilen[-1] + k_] if zeilen else [k_]
            teile.append(f'<div class="sb-m"><p class="sb-n">{kap1(p["name"])}<span class="sb-mp">{x(p["preise"][0])}</span></p>'
                         + ''.join(f'<p class="sb-t">{z}</p>' for z in zeilen) + '</div>')
        elif p['t'] == 'notiz':
            teile.append(f'<div class="sb-fuss"><p class="sb-notiz">{x(p["text"])}</p></div>')
    return k, [mx(S.blatt(*teile, kl='sb-haus sb-mittig'), mass)]


# ---------------------------------------------------------------- Lunch: quer, der Gruss links, das Menü mittig (wie beim Haus)
def menupreis(t):
    """«(3 – Gänge – 35.- Chf)» als Preis-Marke (Robert 19.10.2026: «das kann man auch viel geiler darstellen»). Wortlaut bleibt."""
    m = re.match(r'^\((\d+)\s*–\s*(Gänge)\s*–\s*(\d+)(\.-)\s*(\w+)\)$', r(t))
    if not m:
        return f'<p class="sb-preis">{x(t)}</p>'
    return (f'<div class="sb-lunchpreis"><span class="g">{e(m.group(1))} {e(m.group(2))}</span><i></i>'
            f'<span class="z">{e(m.group(3))}<small>{e(m.group(4))}</small></span><span class="w">{e(m.group(5))}</span></div>')


def lunch(mass):
    _karte[0] = 'lunch'
    k = karte('lunch')
    gruss, mitte = '', []
    for p in posten_von(k):
        if p['t'] == 'rubrik':
            mitte.append(S.zeichen_gross('sb-zeichen'))            # Robert 18.10.2026: Mittagsmenü mittig, «logo drüber das es edel aussieht»
            mitte.append(f'<h2 class="sb-band">{x(p["titel"])}</h2>')
        elif p['t'] == 'frei' and p['zeilen'][0]['text'] != '***':
            gruss = f'<p class="sb-gruss">{x(p["zeilen"][0]["text"])}</p>'
        elif p['t'] == 'frei':
            mitte.append(f'<div class="sb-gang">{svg("blatt", "sb-blatt")}</div>')     # «***» des Originals als Blatt-Ornament
        elif p['t'] == 'gericht':
            mitte.append(f'<div class="sb-m"><p class="sb-n sb-n--gross">{x(p["name"])}</p>'
                         + ''.join(f'<p class="sb-t">{x(z["text"])}</p>' for z in p.get('zeilen', [])) + '</div>')
        elif p['t'] == 'notiz':
            mitte.append(menupreis(p['text']))
    inhalt = f'<div class="sb-quer"><div class="sb-links">{gruss}</div><div class="sb-menue">{"".join(mitte)}</div><div></div></div>'
    return k, [mx(S.blatt(inhalt, kl='sb-haus', quer=True), mass)]


# ---------------------------------------------------------------- Weinkarte: durchlaufend, jede Seite gefüllt (Robert 20.10.2026)
# «diese ganzen leeren, halbleeren Seiten finde ich echt scheisse … ob man das dann auch irgendwie zusammenzieht»: die Weine laufen durch,
# statt an den Seitenumbrüchen des Originals zu kleben. Jeder Eintrag wird einmal im echten Satz gemessen (wein_messen), dann werden die
# Seiten gefüllt: ein Titel steht nie allein am Seitenende, ein Weingut bleibt zusammen, wenn es auf eine Seite passt, eine neue Weinart
# beginnt oben, wenn auf der Seite weniger als ein Drittel frei ist. Neben jeder Seite zeigt die Unterlagen-Seite die Seite des Originals,
# aus der ihr erster Wein stammt (alt_seiten).
def wein_teile(k):
    """Die Weinkarte als Folge von Teilen: (art, html, s). art: rubrik, land, region-ober, region, weingut, wein."""
    ps = posten_von(k)
    teile = []
    for i, p in enumerate(ps):
        t, s_ = p['t'], p.get('s', 1)
        if t == 'rubrik':
            art, _, land = p['titel'].partition(' - ')
            teile.append(('rubrik', f'{ornament()}<h2 class="sb-wart">{e(normal(art))}</h2>', s_))
            if land and land_teile(land):
                teile.append(('land', land_kopf(*land_teile(land)), s_))
        elif t == 'land' or (t == 'zw' and not p.get('weingut') and land_teile(p['text'])):
            lt = land_teile(p['text'])
            teile.append(('land', land_kopf(*lt, klein=(t == 'zw')) if lt else f'<h3 class="sb-land"><span>{e(normal(p["text"]))}</span></h3>', s_))
        elif t == 'zw' and p.get('weingut'):
            teile.append(('weingut', f'<h4 class="sb-gut">{x(p["text"])}</h4>', s_))
        elif t == 'zw':
            naechster = ps[i + 1] if i + 1 < len(ps) else {}
            ober = naechster.get('t') == 'zw' and not naechster.get('weingut') and not land_teile(naechster.get('text', ''))
            kl = 'sb-region sb-region--ober' if ober else 'sb-region'
            teile.append(('region-ober' if ober else 'region', f'<h3 class="{kl}">{e(normal(p["text"]))}</h3>', s_))
        elif t == 'gericht':
            rows = ''
            for j, (pr, ei) in enumerate(zip(p['preise'], p['einheiten'])):
                if j == 0:
                    rows += (f'<span class="j">{e(p.get("jahr", ""))}</span><span class="n">{x(p["name"])}'
                             + (f' <small>{x(p["zusatz"])}</small>' if p.get('zusatz') else '') + '</span>'
                             + f'<span class="f">{x(ei)}</span><span class="p">{x(pr)}</span>')
                    rows += ''.join(f'<span></span><span class="d">{x(z["text"])}</span><span></span><span></span>' for z in p.get('zeilen', []))
                else:
                    rows += f'<span></span><span></span><span class="f">{x(ei)}</span><span class="p">{x(pr)}</span>'
            teile.append(('wein', f'<div class="sb-wein">{rows}</div>', s_))
    return teile


def wein_messen(teile, mass, fuss):
    """Höhe jedes Teils und die freie Höhe einer Seite im echten Satz (Chromium, Druckmodus, Mass der Karte)."""
    import subprocess, kern as K
    css = K.druckschrift_css() + f":root{{--titel:'{H.SCHRIFT['titel'][0]}',{H.SCHRIFT.get('titel_folge', 'Georgia,serif')};--tg:{H.SCHRIFT.get('druckgewicht', 400)};--muster:{H.MUSTER};--musterb:{getattr(H, 'MUSTER_DRUCK', '40mm')}}}\n"
    css += K.faerbe(open(os.path.join(K.KIT, 'satz.css'), encoding='utf-8').read()) + H.CSS_SATZ
    probe = S.blatt('<div id="mess">' + ''.join(f'<div class="mi" style="display:flow-root">{h}</div>' for _, h, _ in teile) + '</div>', kl='sb-haus sb-wk', fuss=fuss)
    leer = S.blatt('<i></i>', kl='sb-haus sb-wk', fuss=fuss).replace('class="blatt', 'id="leer" class="blatt', 1)
    html_ = (f'<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><style>{css}.blatt{{--s:{mass}}}#mess{{display:block}}'
             f'.blatt:first-child{{height:auto!important}}</style></head><body>{probe}{leer}</body></html>')
    pfad = os.path.join(ROOT, '_werkbank', 'satz', '_mess-wein.html')
    open(pfad, 'w', encoding='utf-8').write(html_)
    js = r"""const { chromium } = require(require('path').join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1300, height: 1400 } });
  await p.emulateMedia({ media: 'print' }); await p.goto('file://' + process.argv[1]); await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => { const h = [...document.querySelectorAll('.mi')].map(x => x.getBoundingClientRect().height);
    const i = document.querySelector('#leer .inhalt'), c = getComputedStyle(i); return { h, frei: i.clientHeight - parseFloat(c.paddingTop) - parseFloat(c.paddingBottom) }; });
  process.stdout.write(JSON.stringify(r)); await b.close(); })();"""
    r = subprocess.run(['node', '-e', js, pfad], capture_output=True, text=True, timeout=120)
    os.remove(pfad)
    if r.returncode:
        raise SystemExit('Weinkarte messen: ' + r.stderr[-600:])
    m = json.loads(r.stdout)
    return m['h'], m['frei']


def wein_seiten(teile, hoehe, frei):
    """Füllt die Seiten. Rückgabe: Liste von Listen mit Indizes der Teile."""
    platz = frei * 0.985
    seiten, akt, voll = [], [], 0.0
    KOPF = ('rubrik', 'land', 'region-ober', 'region', 'weingut')
    n = len(teile)

    def kette(i):
        """Titel ab i bis einschliesslich des ersten Weins (bleibt zusammen)."""
        j = i
        while j < n and teile[j][0] in KOPF:
            j += 1
        return list(range(i, min(j + 1, n)))

    def weingut_block(i):
        j = i + 1
        while j < n and teile[j][0] == 'wein':
            j += 1
        return list(range(i, j))

    def neu():
        nonlocal akt, voll
        if akt:
            seiten.append(akt)
        akt, voll = [], 0.0

    i = 0
    while i < n:
        art = teile[i][0]
        if art == 'rubrik' and akt and (platz - voll) < platz / 3:
            neu()
        if art in KOPF:
            # Titelkette plus, wenn sie mit einem Weingut endet, das ganze Weingut, solange es eine halbe Seite nicht übersteigt
            k = kette(i)
            letzter_kopf = max(q for q in k if teile[q][0] in KOPF)
            if teile[letzter_kopf][0] == 'weingut':
                block = weingut_block(letzter_kopf)
                hb = sum(hoehe[q] for q in range(i, block[-1] + 1))
                if hb <= platz / 2:
                    k = list(range(i, block[-1] + 1))
            hk = sum(hoehe[q] for q in k)
            if voll + hk > platz and akt:
                neu()
            for q in k:
                akt.append(q); voll += hoehe[q]
            i = k[-1] + 1
            continue
        if voll + hoehe[i] > platz and akt:
            neu()
        akt.append(i); voll += hoehe[i]
        i += 1
    neu()
    return seiten


def weinkarte(mass):
    _karte[0] = 'weinkarte'
    k = karte('weinkarte')
    fuss_roh = k['karte']['fuss']
    vorlaeufig = e(fuss_roh)
    teile = wein_teile(k)
    hoehe, frei = wein_messen(teile, mass, vorlaeufig)
    seiten = wein_seiten(teile, hoehe, frei)
    blaetter, alt = [], []
    mm = 96 / 25.4
    for nr, seite in enumerate(seiten):
        fuss = x(fuss_roh)                            # Fusszeile je Seite; Berichtigungen darin zählen je Seite
        rest = frei * 0.985 - sum(hoehe[q] for q in seite)
        luecken = sum(1 for q in seite[1:] if teile[q][0] in ('weingut', 'land', 'region-ober', 'region', 'rubrik'))
        luft = 0 if nr == len(seiten) - 1 or not luecken else min(rest / luecken, 6 * mm * mass) * 0.95
        b_ = S.blatt(*[teile[q][1] for q in seite], kl='sb-haus sb-wk', fuss=fuss)
        b_ = b_.replace('style="width:', f'style="--luft:{max(luft, 0):.1f}px;width:', 1)
        blaetter.append(mx(b_, mass))
        alt.append(next((teile[q][2] for q in seite if teile[q][0] == 'wein'), teile[seite[0]][2]))
    return k, blaetter, alt


H.CSS_SATZ = getattr(H, 'CSS_SATZ', '') + f"""
/* Schlössli, Station 10: in der Machart des Hauses (Garamond, blaue Kapitälchen, Blatt-Ornament, Länderumrisse), verfeinert */
@font-face{{font-family:'Garamond Haus';src:url(../sb/EBGaramond-400.ttf) format('truetype');font-weight:400}}
@font-face{{font-family:'Garamond Haus';src:url(../sb/EBGaramond-700.ttf) format('truetype');font-weight:700}}
.blatt.sb-haus{{font-feature-settings:'locl' 0;background:{PAPIER};color:{TINTE};font-family:'Garamond Haus',Garamond,serif;font-size:calc(11pt*var(--s));line-height:1.3}}
.sb-haus .inhalt{{padding:12mm 18mm 4mm}}
.sb-haus .ufuss2{{font-family:'Garamond Haus',serif;font-size:8pt;letter-spacing:.02em;color:{HIMMEL};border-top:0;padding-top:2mm}}
.sb-haus .kl{{font-size:.8em;letter-spacing:.03em}}
.sb-orn{{display:flex;align-items:center;gap:3mm;margin:0 0 calc(3mm*var(--s))}}
.sb-orn i{{flex:1;height:1.1mm;border-top:.3mm solid {HIMMEL};border-bottom:.3mm solid {HIMMEL}}}
.sb-blatt{{flex:none;width:calc(6.5mm*var(--s));height:auto;color:{HIMMEL}}}
.sb-r{{position:relative;margin-bottom:calc(6mm*var(--s))}}
.sb-r:last-of-type{{margin-bottom:0}}
.sb-h{{text-align:center;font-weight:700;font-size:calc(17pt*var(--s));letter-spacing:.04em;color:{BLAU_T};margin:calc(2mm*var(--s)) 0 calc(6mm*var(--s))!important}}
.sb-titel{{text-align:center;font-weight:400;font-size:calc(26pt*var(--s));letter-spacing:.02em;color:{BLAU_T};margin:0 0 calc(5mm*var(--s))!important}}
/* Länderumriss rechts neben der Liste, nie unter den Preisen (Robert 19.10.2026, Bild: Iberien unter «45 / 65 Hauptgang») */
.sb-umriss{{position:absolute;right:-13mm;top:calc(9mm*var(--s));width:calc(42mm*var(--s));height:auto;color:{HIMMEL}}}
.sb-umriss--iberien{{width:calc(36mm*var(--s))!important;top:calc(10mm*var(--s))!important;right:-14mm!important}}
.sb-r--karte .sb-g{{margin-right:calc(30mm*var(--s))}}
.sb-g{{display:grid;grid-template-columns:1fr calc(23mm*var(--s));column-gap:4mm;align-items:baseline;margin-bottom:calc(4.4mm*var(--s));break-inside:avoid;position:relative;z-index:1}}
.sb-n{{color:{BLAU};font-size:calc(12pt*var(--s));letter-spacing:.03em}}
/* Kürzel: Punkte statt Schrägstriche, VEG mit Blatt (Robert 19.10.2026, Bild «VEG/G/L/E/N/SE») */
.sb-k{{font-size:calc(7.4pt*var(--s));letter-spacing:.08em;color:#7F93B0;white-space:nowrap;text-align:right}}
.sb-m .sb-k{{text-align:center}}
.sb-kz{{font-size:calc(6.6pt*var(--s));letter-spacing:.06em;color:#8FA3BE;vertical-align:.55em;line-height:0;white-space:nowrap;margin-left:.3em}}
.sb-ab{{display:inline-block;width:.45em}}
.sb-kz .sb-veg{{color:#3E7A4F;font-weight:700}}
.sb-veg{{color:{BLAU};font-weight:700;display:inline-flex;align-items:center;gap:.25em}}
.sb-vb{{width:1.1em;height:1.1em;color:#3E7A4F;vertical-align:-.1em;margin-right:.1em}}
.sb-w{{font-size:calc(6.8pt*var(--s));letter-spacing:.06em}}
.sb-p{{grid-row:1 / span 4;grid-column:2;font-variant-numeric:lining-nums;text-align:right}}
.sb-p span{{display:flex;justify-content:flex-end;align-items:baseline;gap:2mm}}
.sb-p b{{font-weight:400;font-size:calc(12.5pt*var(--s));color:{BLAU_T}}}
.sb-p em{{font-style:normal;font-size:calc(9.6pt*var(--s));letter-spacing:0;color:{LEISE}}}
.sb-g .sb-t{{grid-column:1}}
.sb-t{{font-size:calc(11pt*var(--s))}}
.sb-fuss{{margin-top:auto;padding-top:calc(4mm*var(--s));text-align:center}}
.sb-notiz{{text-align:center;font-size:calc(9pt*var(--s));color:{LEISE};margin-top:calc(1mm*var(--s))!important}}
.sb-luft .sb-g{{margin-bottom:calc(10.4mm*var(--s))}}   /* je Zwischenraum höchstens 6 mm mehr, der Rest an den Fuss (GBR 11.10.2026) */
.sb-zeichen{{width:calc(11mm*var(--s))!important;margin:0 auto calc(4mm*var(--s));color:{BLAU}!important}}
/* Bankett: Jahreszeit gross, Menüpreis als Marke zwischen zwei Linien */
.sb-saison{{text-align:center;font-weight:400;font-size:calc(24pt*var(--s));letter-spacing:.02em;color:{BLAU_T};margin:calc(1mm*var(--s)) 0 0!important}}
.sb-menupreis{{display:flex;align-items:center;justify-content:center;gap:4mm;margin:calc(1.5mm*var(--s)) 0 calc(6mm*var(--s))!important;color:{BLAU};font-size:calc(10pt*var(--s));letter-spacing:.12em}}
.sb-menupreis i{{width:14mm;border-top:.3mm solid {HIMMEL}}}
.sb-menupreis b{{font-weight:400;font-size:calc(15pt*var(--s));letter-spacing:.02em;color:{BLAU_T}}}
/* Lästermeile: beide Titel in derselben Form, normale Schreibung (Robert 19.10.2026) */
.sb-band{{text-align:center;font-weight:400;font-size:calc(19pt*var(--s));letter-spacing:.02em;color:{BLAU_T};margin:0 0 calc(6mm*var(--s))!important}}
.sb-mittig .sb-orn{{margin-top:calc(5mm*var(--s))}}
.sb-mittig .sb-orn:first-child{{margin-top:0}}
.sb-m{{text-align:center;margin-bottom:calc(4.6mm*var(--s));break-inside:avoid}}
.sb-mp{{color:{BLAU_T};font-size:calc(12.5pt*var(--s));margin-left:3mm}}
.sb-k--m{{margin-top:calc(.8mm*var(--s))!important}}
/* Lunch */
.sb-quer{{flex:1;display:grid;grid-template-columns:62mm 1fr 62mm;align-items:center}}
.sb-gruss{{text-align:center;font-weight:400;font-style:normal;font-size:calc(15pt*var(--s));line-height:1.45;color:{BLAU}}}
.sb-menue .sb-band{{border-top:.3mm solid {HIMMEL};border-bottom:.3mm solid {HIMMEL};padding:calc(2mm*var(--s)) 0;margin-bottom:calc(7mm*var(--s))!important}}
.sb-n--gross{{font-size:calc(16pt*var(--s));font-weight:700;letter-spacing:0}}
.sb-gang{{display:flex;justify-content:center;margin:calc(3.5mm*var(--s)) 0;position:relative}}
.sb-gang .sb-blatt{{width:calc(5mm*var(--s))}}
.sb-lunchpreis{{display:flex;align-items:baseline;justify-content:center;gap:3mm;margin-top:calc(8mm*var(--s));color:{BLAU}}}
.sb-lunchpreis .g{{font-size:calc(9pt*var(--s));letter-spacing:.16em;text-transform:uppercase}}
.sb-lunchpreis i{{width:10mm;border-top:.3mm solid {HIMMEL};align-self:center}}
.sb-lunchpreis .z{{font-size:calc(24pt*var(--s));color:{BLAU_T};line-height:1}}
.sb-lunchpreis .z small{{font-size:.6em}}
.sb-lunchpreis .w{{font-size:calc(9pt*var(--s));letter-spacing:.16em;text-transform:uppercase}}
/* Weinkarte: Art gross, Land mit Flagge, Region grösser in normaler Schreibung (Robert 19.10.2026) */
.sb-wk .inhalt{{padding-top:10mm}}
.sb-wart{{text-align:center;font-weight:400;font-size:calc(24pt*var(--s));letter-spacing:.02em;color:{BLAU_T};margin:calc(1mm*var(--s)) 0 calc(4mm*var(--s))!important}}
.sb-land{{display:flex;align-items:center;justify-content:center;gap:3mm;font-weight:400;font-size:calc(17pt*var(--s));color:{BLAU_T};margin:calc(4.5mm*var(--s)) 0 calc(1mm*var(--s))!important;break-after:avoid}}
.sb-land--klein{{font-size:calc(14pt*var(--s));margin-top:calc(6mm*var(--s))!important;margin-bottom:calc(1.6mm*var(--s))!important}}
.sb-flagge{{width:calc(7mm*var(--s));height:auto;flex:none;border-radius:1mm}}
.sb-land--klein .sb-flagge{{width:calc(5.5mm*var(--s))}}
.sb-lr,.sb-region{{display:block;text-align:center;font-style:normal;font-size:calc(13pt*var(--s));color:{BLAU};letter-spacing:.02em;margin:calc(2.4mm*var(--s)) 0 calc(1.2mm*var(--s))!important;break-after:avoid}}
.sb-region--ober{{font-size:calc(15pt*var(--s));color:{BLAU_T};margin-top:calc(4mm*var(--s))!important;margin-bottom:0!important}}
.sb-region--ober + .sb-region{{font-size:calc(11.5pt*var(--s));margin-top:calc(.8mm*var(--s))!important}}
.sb-region::before,.sb-region::after{{content:'';display:inline-block;width:8mm;border-top:.3mm solid {HIMMEL};vertical-align:middle;margin:0 3mm}}
.sb-wk .sb-gut,.sb-wk .sb-land,.sb-wk .sb-region--ober,.sb-wk .sb-orn{{padding-top:var(--luft,0px)}}
.sb-wk .sb-region:not(.sb-region--ober + .sb-region):not(.sb-land + .sb-region){{padding-top:var(--luft,0px)}}
.sb-gut{{font-weight:700;font-size:calc(11.5pt*var(--s));color:{TINTE};margin:calc(2.8mm*var(--s)) 0 calc(.8mm*var(--s))!important;padding-bottom:calc(.6mm*var(--s));border-bottom:.2mm solid #DCE4EE;break-after:avoid}}
.sb-wein{{display:grid;grid-template-columns:calc(11mm*var(--s)) 1fr calc(13mm*var(--s)) calc(12mm*var(--s));column-gap:2mm;font-size:calc(10.6pt*var(--s));line-height:1.36;font-variant-numeric:lining-nums tabular-nums;break-inside:avoid}}
.sb-wein .j{{color:#7F93B0;font-size:.92em}}
.sb-wein .n small{{font-size:.86em;color:{LEISE}}}
.sb-wein .f{{text-align:right;color:#7F93B0;font-size:.86em}}
.sb-wein .p{{text-align:right;color:{BLAU_T}}}
.sb-wein .d{{font-size:.84em;color:{LEISE};font-style:normal}}
"""

MASS = {'speisekarte': 1.0, 'bankett': 1.0, 'laestermeile': 1.0, 'lunch': 1.0, 'weinkarte': 1.0}
_mass = os.path.join(SB, 'mass.json')      # von sb_unterlagen.py gemessen: je Karte das kleinste Mass, das auf jeder Seite passt
if os.path.exists(_mass):
    MASS.update(json.load(open(_mass)))

_sk, SK = a_la_carte('speisekarte', MASS['speisekarte'])
_bk, BK = a_la_carte('bankett', MASS['bankett'])
_lm, LM = laestermeile(MASS['laestermeile'])
_lu, LU = lunch(MASS['lunch'])
_wk, WK, WK_ALT = weinkarte(MASS['weinkarte'])


def dok(kid, quelle, name, gruppe, seiten, quer=False, fuss_adresse=True, mehr_fehlt=''):
    dazu = [H.SATZ_FUSS] * len(seiten) if fuss_adresse else []
    fehlt = []
    for alt, neu in GENUTZT.get(kid, []):
        fehlt.append(alt); dazu.append(neu)
    seiten = [s.replace(' – ', ' – ') for s in seiten]          # Gedankenstrich bleibt am Wort davor (QA Doldenhorn 09.10.2026)
    return S.dok(kid, Q + quelle, name, gruppe, seiten, quer=quer, dazu=' '.join(dazu), fehlt=(' '.join(fehlt) + ' ' + mehr_fehlt).strip())


DOKS = [
    dok('speisekarte', 'Speisekarte-Oktober.pdf', 'Die Karte nach Ländern', 'Restaurant', SK),
    dok('laestermeile', 'Lastermeile-Homepage-2339.pdf', 'Lästermeile', 'Bar', LM),
    dok('lunch', 'Lunch_261019.pdf', 'Lunch-Menü', 'Restaurant', LU, quer=True),
    dok('bankett', 'Bankettmenuvorschlage.pdf', 'Bankettmenüvorschläge', 'Banketts & Gruppen', BK),
    dok('weinkarte', '20261014_Weinkarte.pdf', 'Weinkarte', 'Restaurant', WK, fuss_adresse=False,
        mehr_fehlt='A ' + ' '.join(str(n) for n in range(2, 28)) + (' ' + _wk['karte']['fuss'].replace(' · ', ' ')) * max(0, 26 - len(WK))),
]
DOKS[-1]['alt_seiten'] = WK_ALT          # neben jeder Seite der Idee die Seite des Originals, aus der ihr erster Wein stammt
# Der 4-Hands-Lunch vom 22.02.2026 ist vorbei: er bleibt in den Kartendaten (La Carte), aber nicht unter den Unterlagen des Hauses.

json.dump({d['name']: [[a, n, sum(1 for g in GENUTZT.get(d['ziel'], []) if g == (a, n))] for a, n in sorted(set(GENUTZT.get(d['ziel'], [])))] for d in DOKS},
          open(os.path.join(ROOT, '_werkbank', 'berichtigt.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
