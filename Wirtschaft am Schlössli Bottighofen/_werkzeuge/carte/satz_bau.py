#!/usr/bin/env python3
"""Das Kartenpult · Wirtschaft am Schlössli — setzt die fünf Karten des Hauses neu, im Kleid des Hauses (Nachtbau 3.11.2026).

Nichts ist abgetippt: jedes Gericht, jede Zeile, jeder Wein und jeder Preis kommt aus den Daten der Website (website/inhalt/karte.json,
lunch.json, laestermeile.json, wein.json, bankett.json; maschinell aus den PDFs des Hauses gelesen, Original-PDFs in _karten/pdf/).
Preise genau wie im Original (Schweizer Franken), der Wortlaut bleibt. Bewusst anders (typografisch): «ß» wird «ss» (Schweizer Schreibung),
« / » in Titeln wird « · » (Trenner des Hauses), Gerichte stehen in Versalien in DM Mono wie auf der Karte des Hauses (THON · CAVATELLI),
die Zeile darunter in Instrument Sans, Titel in Open Sans in Versalien gesperrt wie die Wortmarke. Kopf jeder Seite: das Zeichen (die Zeiger)
und die Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» als Vektor aus _werkzeuge/oberflaeche/kleid/schloessli-marke.svg (#wm, unverändert).

Die Weinkarte (468 Weine, 495 Positionen) läuft durch: jeder Teil wird einmal im echten Satz gemessen (satz_messen.js, Chromium), dann werden
die Seiten gefüllt; ein Titel steht nie allein am Seitenende, ein Weingut bleibt zusammen, wenn es auf eine halbe Seite passt.

Aus dem Satz liest einlesen.py die Karte als Baum; satz/satz.js setzt daraus Zeichen für Zeichen dasselbe HTML (Vorschau, PDF, Werkbank).
    python3 _werkzeuge/carte/satz_bau.py          setzt alle Karten nach satz/u-<karte>.html, die Zeichen nach satz/zeichen.json
"""
import html, json, os, re, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(HAUS, 'website')
INHALT = os.path.join(WEB, 'inhalt')
KLEID = os.path.join(HAUS, '_werkzeuge', 'oberflaeche', 'kleid')
SATZ = os.path.join(HIER, 'satz')


def lies(n):
    return json.load(open(os.path.join(INHALT, n + '.json'), encoding='utf-8'))


H = lies('haus')
NAME = H['name']
FUSS = f"{NAME} · {H['strasse']} · {H['ort']} · {H['telefon']}"


def t(x):
    """Wortlaut des Hauses in Schweizer Schreibung: «ß» → «ss», Trenner « / » → « · »"""
    x = str(x or '').replace('ß', 'ss').strip()
    return re.sub(r'\s+/\s+', ' · ', x)


def e(x):
    return html.escape(t(x), quote=False)


def preis(p):
    """Preis wie im Original: ganze Franken ohne Nachkommastellen («40»)"""
    if isinstance(p, float) and not p.is_integer():
        return f'{p:.2f}'
    return str(int(p)) if isinstance(p, (int, float)) else t(p)


# ---------------------------------------------------------------- Zeichen und Wortmarke (aus dem Kleid, unverändert)
def wortmarke():
    s = open(os.path.join(KLEID, 'schloessli-marke.svg'), encoding='utf-8').read()
    m = re.search(r'<symbol id="wm" viewBox="([^"]+)">(.*?)</symbol>', s, re.S)
    return f'<svg class="sb-wm" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="{m.group(1)}" fill="currentColor">{m.group(2).strip()}</svg>'


def zeichen_svg():
    s = open(os.path.join(KLEID, 'schloessli-zeichen.svg'), encoding='utf-8').read().strip()
    s = re.sub(r'<\?xml.*?\?>', '', s).strip()
    return s.replace('<svg ', '<svg class="sb-z" aria-hidden="true" ', 1)


WM, ZE = wortmarke(), zeichen_svg()
KOPF = f'<div class="sb-kopf"><span class="sb-zeichen">{ZE}</span><span class="sb-zeichen">{WM}</span></div>'


def blatt(inhalt, b=210, h=297, kl='', mx='1.15', stil=''):
    return (f'<section data-max="{mx}" class="blatt sb-haus{(" " + kl) if kl else ""}" data-b="{b}" data-h="{h}" style="{stil}width:{b}mm;height:{h}mm">'
            f'<div class="inhalt">{inhalt}</div><footer class="ufuss2">{html.escape(FUSS, quote=False)}</footer></section>')


def doc(titel, seiten, b=210, h=297):
    return (f'<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><title>{html.escape(titel, quote=False)} · {html.escape(NAME, quote=False)}</title>\n'
            f'<link rel="stylesheet" href="satz.css"><style>@page{{size:{b}mm {h}mm;margin:0}}</style></head><body>' + ''.join(seiten) + '</body></html>')


def kopf(titel=None):
    return KOPF + (f'<h1 class="sb-titel">{e(titel)}</h1><div class="sb-horizont"></div>' if titel else '<div class="sb-horizont"></div>')


def notizen(liste):
    return '<div class="sb-fuss">' + ''.join(f'<p class="sb-notiz">{e(x)}</p>' for x in liste if t(x)) + '</div>'


# ---------------------------------------------------------------- Speisekarte nach Ländern
def gericht(g, mit_hinweis=True):
    pr = f'<span><b>{preis(g["preis"])}</b></span>'
    if g.get('haupt'):
        pr += f'<span><em>Hauptgang</em><b>{preis(g["haupt"])}</b></span>'
    aus = f'<div class="sb-g"><p class="sb-n">{e(g["name"])}</p><p class="sb-p">{pr}</p>'
    if t(g.get('text')):
        aus += f'<p class="sb-t">{e(g["text"])}</p>'
    if t(g.get('allergene')):
        aus += f'<p class="sb-al">{e(g["allergene"])}</p>'
    if mit_hinweis and t(g.get('hinweis')):
        aus += f'<p class="sb-w">{e(g["hinweis"])}</p>'
    return aus + '</div>'


def rubrik(titel, inhalt, kl=''):
    return f'<section class="sb-r"><h2 class="sb-h{(" " + kl) if kl else ""}">{e(titel)}</h2>{inhalt}</section>'


def speisekarte():
    k = lies('karte')
    L = k['laender']
    teile = [L[:2], L[2:]]   # zwei Seiten: Frankreich und Italien, dann Iberische Halbinsel und Klassiker mit den Fussnoten
    seiten = []
    for i, ls in enumerate(teile):
        inn = kopf('Speisekarte' if i == 0 else None) + ''.join(rubrik(l['land'], ''.join(gericht(g) for g in l['gerichte'])) for l in ls)
        if i == len(teile) - 1:
            f = k.get('fuss') or {}
            inn += notizen([f.get('mwst'), f.get('veg'), f.get('veg2'), f.get('allergene')])
        seiten.append(blatt(inn, mx='1.12'))
    return doc('Speisekarte', seiten)


# ---------------------------------------------------------------- Lunch-Menü (quer, mittig)
def lunch():
    d = lies('lunch')
    gaenge = []
    for i, g in enumerate(d['gaenge']):
        if i:
            gaenge.append('<div class="sb-gang"><i></i></div>')
        gaenge.append(f'<div class="sb-m sb-m--gross"><p class="sb-n">{e(g["name"])}</p>' + (f'<p class="sb-t">{e(g["text"])}</p>' if t(g.get('text')) else '') + '</div>')
    m = re.match(r'^\s*(\d+\s*–\s*Gänge)\s*–\s*(\d+\.-)\s*(\S+)\s*$', d['preis'])
    if m:
        pr = f'<div class="sb-g sb-lunchpreis"><p class="sb-p"><span><em>{e(m.group(1))}</em><b>{e(m.group(2))}</b><small>{e(m.group(3))}</small></span></p></div>'
    else:
        pr = f'<div class="sb-g sb-lunchpreis"><p class="sb-p"><span><b>{e(d["preis"])}</b></span></p></div>'
    inn = KOPF + f'<div class="sb-mitte"><h1 class="sb-titel">{e(d["titel"])}</h1><div class="sb-horizont sb-horizont--kurz"></div>{"".join(gaenge)}{pr}</div>'
    return doc('Lunch-Menü', [blatt(inn, 297, 210, kl='sb-quer', mx='1.5')], 297, 210)


# ---------------------------------------------------------------- Lästermeile (mittig, Name und Preis auf einer Zeile)
def laestermeile():
    d = lies('laestermeile')
    inn = ''
    for gr in d['gruppen']:
        inn += f'<h2 class="sb-h">{e(gr["titel"])}</h2>'
        for x in gr['eintraege']:
            inn += f'<div class="sb-m"><p class="sb-n">{e(x["name"])}<span class="sb-mp">{preis(x["preis"])}</span></p>' + (f'<p class="sb-t">{e(x["text"])}</p>' if t(x.get('text')) else '') + '</div>'
    inn = kopf('Lästermeile') + f'<div class="sb-mitte">{inn}</div>' + notizen([d.get('allergene')])
    return doc('Lästermeile', [blatt(inn, mx='1.2')])


# ---------------------------------------------------------------- Bankettmenüs (je Menü eine Seite)
def bankett():
    d = lies('bankett')
    seiten = []
    for i, m in enumerate(d['menues']):
        gs = ''.join(gericht(g) for g in m['gerichte'])
        mp = f'<div class="sb-g sb-menupreis"><p class="sb-p"><span><em>Menü</em><b>{preis(m["preis"])}</b><small>CHF</small></span></p></div>'
        inn = kopf('Bankettmenüs') + f'<div class="sb-mitte"><h2 class="sb-h sb-saison">{e(m["name"])}</h2>{mp}{gs}</div>'
        if i == len(d['menues']) - 1 and t(d.get('hinweis')):
            inn += notizen([d['hinweis']])
        seiten.append(blatt(inn, mx='1.18'))
    return doc('Bankettmenüs', seiten)


# ---------------------------------------------------------------- Weinkarte (durchlaufend, jede Seite gefüllt)
def wein_teile():
    w = lies('wein')
    teile = []
    for g in w['gruppen']:
        teile.append(('wart', f'<h2 class="sb-h sb-wart">{e(g["titel"])}</h2>'))
        for r in g['regionen']:
            if r['titel']:
                land = not r['erzeuger']            # ein Land ohne eigene Weingüter ist die Überschrift der Regionen darunter
                teile.append(('land' if land else 'region', f'<h3 class="{"sb-land" if land else "sb-region"}">{e(r["titel"])}</h3>'))
            for erz in r['erzeuger']:
                if t(erz.get('name')):
                    teile.append(('gut', f'<h4 class="sb-gut">{e(erz["name"])}</h4>'))
                for x in erz['weine']:
                    fl = x['flaschen'] or [{'gross': '', 'preis': ''}]
                    z = (f'<span class="j">{e(x.get("jahr") or "")}</span><span class="n">{e(x["name"])}</span>'
                         f'<span class="f">{e(fl[0]["gross"])}</span><span class="p">{preis(fl[0]["preis"])}</span>')
                    for f in fl[1:]:
                        z += f'<span></span><span></span><span class="f">{e(f["gross"])}</span><span class="p">{preis(f["preis"])}</span>'
                    if t(x.get('notiz')):
                        z += f'<span></span><span class="d">{e(x["notiz"])}</span><span></span><span></span>'
                    teile.append(('wein', f'<div class="sb-g sb-wein">{z}</div>'))
    return w, teile


NODE_PW = ['/Users/robertreff/Aussen-Pruefung/node_modules/playwright', os.path.join(os.path.expanduser('~'), 'Aussen-Pruefung/node_modules/playwright')]


def wein_messen(teile):
    """Höhe jedes Teils und die freie Höhe der ersten und der folgenden Seiten im echten Satz (Chromium, Druckmodus)."""
    probe = blatt('<div id="mess">' + ''.join(f'<div class="mi" style="display:flow-root">{h}</div>' for _, h in teile) + '</div>', kl='sb-wk', mx='1')
    leer1 = blatt(kopf('Weinkarte') + '<div class="fr" style="flex:1"></div>', kl='sb-wk', mx='1')
    leer2 = blatt(kopf(None) + '<div class="fr" style="flex:1"></div>', kl='sb-wk', mx='1')
    seite = (f'<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><link rel="stylesheet" href="satz.css">'
             f'<style>.blatt:first-child{{height:auto!important}}</style></head><body>{probe}{leer1}{leer2}</body></html>')
    pfad = os.path.join(SATZ, '_mess-wein.html')
    open(pfad, 'w', encoding='utf-8').write(seite)
    try:
        r = subprocess.run(['node', os.path.join(HIER, 'satz_messen.js'), pfad], capture_output=True, text=True, timeout=180)
    finally:
        os.remove(pfad)
    if r.returncode:
        raise SystemExit('Weinkarte messen: ' + r.stderr[-800:])
    m = json.loads(r.stdout)
    return m['h'], m['frei']


def wein_seiten(teile, hoehe, frei):
    seiten, akt, voll = [], [], 0.0
    KOPF_ = ('wart', 'land', 'region', 'gut')
    n = len(teile)
    platz = lambda: (frei[0] if not seiten else frei[1]) * 0.985

    def kette(i):
        j = i
        while j < n and teile[j][0] in KOPF_:
            j += 1
        return list(range(i, min(j + 1, n)))

    def gut_block(i):
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
        if art == 'wart' and akt and (platz() - voll) < platz() / 3:
            neu()
        if art in KOPF_:
            k = kette(i)
            letzter = max(q for q in k if teile[q][0] in KOPF_)
            if teile[letzter][0] == 'gut':
                block = gut_block(letzter)
                if sum(hoehe[q] for q in range(i, block[-1] + 1)) <= platz() / 2:
                    k = list(range(i, block[-1] + 1))
            hk = sum(hoehe[q] for q in k)
            if voll + hk > platz() and akt:
                neu()
            for q in k:
                akt.append(q); voll += hoehe[q]
            i = k[-1] + 1
            continue
        if voll + hoehe[i] > platz() and akt:
            neu()
        akt.append(i); voll += hoehe[i]
        i += 1
    neu()
    return seiten


def weinkarte():
    w, teile = wein_teile()
    hoehe, frei = wein_messen(teile)
    seiten = wein_seiten(teile, hoehe, frei)
    blaetter, mm = [], 96 / 25.4
    for nr, s in enumerate(seiten):
        f = frei[0] if nr == 0 else frei[1]
        rest = f * 0.985 - sum(hoehe[q] for q in s)
        luecken = sum(1 for q in s[1:] if teile[q][0] in ('wart', 'land', 'region', 'gut'))
        luft = 0 if nr == len(seiten) - 1 or not luecken else min(rest / luecken, 5 * mm) * 0.9
        inn = kopf('Weinkarte' if nr == 0 else None) + ''.join(teile[q][1] for q in s)
        if nr == len(seiten) - 1:
            inn += notizen(w.get('fuss') or [])
        blaetter.append(blatt(inn, kl='sb-wk', mx='1', stil=f'--luft:{max(luft, 0):.1f}px;'))
    return doc('Weinkarte', blaetter), len(teile), len(seiten)


def zeichen():
    """Feste Teile für Werkzeug und Werkbank: das Zeichen (die Zeiger), die Wortmarke, die Fusszeile, der Name des Hauses."""
    return dict(ZEICHEN=ZE, WORTMARKE=WM, FUSS=FUSS, HAUS=NAME)


def _schreib(p, x):
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        f.write(x)
    os.replace(p + '.neu', p)


KARTEN = ['speisekarte', 'lunch', 'laestermeile', 'weinkarte', 'bankett']

if __name__ == '__main__':
    os.makedirs(SATZ, exist_ok=True)
    nur = sys.argv[1:] or KARTEN
    for kid in nur:
        if kid == 'weinkarte':
            h, n, s = weinkarte()
            print(f'gesetzt: satz/u-weinkarte.html ({n} Teile auf {s} Seiten)')
        else:
            h = {'speisekarte': speisekarte, 'lunch': lunch, 'laestermeile': laestermeile, 'bankett': bankett}[kid]()
            print(f'gesetzt: satz/u-{kid}.html')
        _schreib(os.path.join(SATZ, f'u-{kid}.html'), h)
    with open(os.path.join(SATZ, 'zeichen.json'), 'w', encoding='utf-8') as f:
        json.dump(zeichen(), f, ensure_ascii=False)
    print('Zeichen: satz/zeichen.json')
