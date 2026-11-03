#!/usr/bin/env python3
"""Das Kartenpult · Wirtschaft am Schlössli — Prüfungen der Karten (Nachtbau 3.11.2026, Muster: pruefe.py der Tafel im Schäfli).

    python3 _werkzeuge/carte/pruefe.py rund        Satz → Baum → Satz Zeichen für Zeichen gleich (pruef_rund.js, Grundstand)
    python3 _werkzeuge/carte/pruefe.py quelle      jede Karte gegen die Daten der Website (website/inhalt/*.json): jeder Name, jede Zeile, jeder Preis
                                                   steht im Grundstand, genau so oft wie in der Quelle (Schweizer Schreibung: «ß» als «ss»)
    python3 _werkzeuge/carte/pruefe.py druck       jede Karte aus dem Stand drucken (Server muss laufen, CARTE_PORT, Standard 9283), PDF = Daten
                                                   (Wort für Wort) und nur feste Schnitte (pdffonts, kein Type 3)
    python3 _werkzeuge/carte/pruefe.py alles
Nur gelesen wird website/; geschrieben wird nur nach pruef/aus/."""
import collections, json, os, re, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
AUS = os.path.join(HIER, 'pruef', 'aus')
INHALT = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website', 'inhalt')
import carte  # noqa: E402
import satz_bau  # noqa: E402


def rund():
    r = subprocess.run(['node', os.path.join(HIER, 'pruef_rund.js')], capture_output=True, text=True)
    print(r.stdout.strip())
    return r.returncode == 0


def soll(z):
    """Was aus der Quelle auf der Karte stehen muss (Texte in Schweizer Schreibung, Preise als Zahl)."""
    T, P = satz_bau.t, satz_bau.preis
    j = lambda n: json.load(open(os.path.join(INHALT, n + '.json'), encoding='utf-8'))
    aus = []
    if z == 'speisekarte':
        for l in j('karte')['laender']:
            aus.append(T(l['land']))
            for g in l['gerichte']:
                aus += [T(g['name']), T(g['text']), T(g['allergene']), P(g['preis'])] + ([P(g['haupt'])] if g.get('haupt') else []) + ([T(g['hinweis'])] if g.get('hinweis') else [])
    elif z == 'lunch':
        d = j('lunch')
        aus += [T(d['titel'])] + [T(x) for g in d['gaenge'] for x in (g['name'], g['text'])]
    elif z == 'laestermeile':
        for g in j('laestermeile')['gruppen']:
            aus.append(T(g['titel']))
            for x in g['eintraege']:
                aus += [T(x['name']), P(x['preis'])] + ([T(x['text'])] if x.get('text') else [])
    elif z == 'weinkarte':
        for g in j('wein')['gruppen']:
            aus.append(T(g['titel']))
            for r in g['regionen']:
                if r['titel']:
                    aus.append(T(r['titel']))
                for e in r['erzeuger']:
                    aus.append(T(e['name']))
                    for w in e['weine']:
                        aus += [T(w['name'])] + ([T(w['jahr'])] if w.get('jahr') else []) + ([T(w['notiz'])] if w.get('notiz') else [])
                        aus += [x for f in w['flaschen'] for x in (T(f['gross']), P(f['preis']))]
    elif z == 'bankett':
        for m in j('bankett')['menues']:
            aus += [T(m['name']), P(m['preis'])]
            for g in m['gerichte']:
                aus += [T(g['name']), T(g['text']), P(g['preis'])]
    return [x for x in aus if x]


def quelle():
    ok = True
    for z in carte.ZIELE:
        g = carte._lies(carte._p('grundstand', z))
        ist = collections.Counter(x.strip() for x in carte.texte(g))
        s = collections.Counter(soll(z))
        fehlt = s - ist
        print(f'{z}: {sum(s.values())} Angaben aus der Quelle, ' + ('alle auf der Karte' if not fehlt else f'FEHLEN {dict(list(fehlt.items())[:6])}'))
        ok = ok and not fehlt
    return ok


def druck():
    ok = True
    os.makedirs(AUS, exist_ok=True)
    for z in carte.ZIELE:
        p = os.path.join(AUS, z + '.pdf')
        b = carte.drucke(z, 'stand', p)
        v = carte.pdf_gleich_daten(carte._lies(carte._p('stand', z)), p)
        f = subprocess.run(['pdffonts', p], capture_output=True, text=True).stdout
        typ3 = 'Type 3' in f
        print(f'{z}: {b.get("seiten")} Seiten, Schriftmass {b.get("mass")}, {v["woerter"]} Wörter, ' + ('PDF = Daten' if not v['fehlt'] else f'FEHLT {list(v["fehlt"])[:4]}') + (', TYPE 3' if typ3 else ', feste Schnitte') + (f', passt nicht: {b["fehler"][:2]}' if b.get('fehler') else ''))
        ok = ok and not v['fehlt'] and not typ3 and not b.get('fehler')
    return ok


if __name__ == '__main__':
    was = (sys.argv[1:] or ['alles'])[0]
    teile = {'rund': [rund], 'quelle': [quelle], 'druck': [druck], 'alles': [rund, quelle, druck]}[was]
    gut = all([f() for f in teile])
    print('GESAMT', 'GRÜN' if gut else 'ROT')
    sys.exit(0 if gut else 1)
