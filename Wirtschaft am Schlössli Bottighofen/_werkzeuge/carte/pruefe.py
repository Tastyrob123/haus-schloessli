#!/usr/bin/env python3
"""Das Kartenpult (La Carte) · Wirtschaft am Schlössli — Prüfungen der Karten (20.10.2026, Kopie aus der Tafel des Gasterntal). Für «wortlaut» und «website» muss der Server laufen
(python3 _werkzeuge/carte/serve.py, Port aus CARTE_PORT, Standard 9031).

    python3 _werkzeuge/carte/pruefe.py rund        Satz von La Carte = Satz des Projekts, Zeichen für Zeichen (pruef/rund.js, Grundstand)
    python3 _werkzeuge/carte/pruefe.py wortlaut    jede Karte aus dem veröffentlichten Stand drucken und Wort für Wort gegen das ORIGINAL des Hauses
                                                   prüfen (_quelle/website/pdf/…, Quelle je Karte in website/_werkbank/unterlagen.json), nach derselben Regel wie _Werkbank-Kit/satz_pruefe.py:
                                                   bewusste Abweichungen (berichtigte Tippfehler aus _werkbank/satz_daten.py BERICHTIGT, Kopfzeilen des
                                                   Druckprogramms) stehen je Karte in _werkbank/unterlagen.json «fehlt» / «dazu»
    python3 _werkzeuge/carte/pruefe.py website     die Drucke von La Carte gegen die PDFs, die heute auf der Website liegen (unterlagen/pdf/):
                                                   gleicher Text (pdftotext -layout, Zeichen für Zeichen), gleiche Seitenzahl, gleiche Seitenbilder
    python3 _werkzeuge/carte/pruefe.py alles
Nur gelesen wird _werkbank/, assets/pdf/ und unterlagen/pdf/; geschrieben wird nur nach pruef/aus/."""
import collections, json, os, re, subprocess, sys, unicodedata

HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(HIER))
PROJ = _WURZEL if os.path.isfile(os.path.join(_WURZEL, 'bau.py')) else os.path.join(_WURZEL, 'website')   # Schlössli: Website in website/
HAUS = os.path.dirname(PROJ) if os.path.basename(PROJ) == 'website' else PROJ   # dort liegt _quelle/
AUS = os.path.join(HIER, 'pruef', 'aus')
KARTEN = ['speisekarte', 'laestermeile', 'weinkarte', 'bankett']   # Lunch-Menü: eigene Woche (C08), Prüfung in der Bedienungsprobe


def druck(z, art='stand'):
    os.makedirs(AUS, exist_ok=True)
    p = os.path.join(AUS, z + '.pdf')
    r = subprocess.run(['node', os.path.join(HIER, 'drucke.js'), z, art, p], capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise SystemExit(f'Druck {z} gescheitert: {r.stderr[-400:]}')
    return p


def rund():
    r = subprocess.run(['node', os.path.join(HIER, 'pruef', 'rund.js')], capture_output=True, text=True)
    print(r.stdout.strip())
    return r.returncode == 0


MUSTER = r'[0-9a-zäöüéèêëàâîïôùûçœß]+'


def _text(pfad):
    """Text einer PDF wie _Werkbank-Kit/satz_pruefe.py (die Prüfung, mit der die Werkbank die Unterlagen gegen die Originale gelesen hat)"""
    t = subprocess.run(['pdftotext', pfad, '-'], capture_output=True, text=True).stdout
    t = unicodedata.normalize('NFC', t).replace('\xa0', ' ').replace('\xad', '')
    for a, b in (('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬀ', 'ff'), ('ﬃ', 'ffi'), ('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'), ('«', '"'), ('»', '"'), ('➢', ' ')):
        t = t.replace(a, b)
    t = re.sub(r'[\ue000-\uf8ff]', ' ', t)
    return re.sub(r'_{3,}', ' ', t)


def _w(t):
    return collections.Counter(re.findall(MUSTER, unicodedata.normalize('NFC', t).lower()))


def wortlaut():
    """Wie _Werkbank-Kit/satz_pruefe.py, aber mit dem Druck von La Carte statt der PDF der Website: gezählt werden Buchstaben und Ziffern je Wort,
    Gross und Klein gleich; bewusste Abweichungen stehen je Karte in _werkbank/unterlagen.json (fehlt/dazu); zweiter Blick ohne Leerzeichen,
    weil Originale Wörter über Stücke verteilen («nur anders getrennt»)."""
    plan = {d['ziel']: d for d in json.load(open(os.path.join(PROJ, '_werkbank', 'unterlagen.json'), encoding='utf-8'))}
    ok = True
    for z in KARTEN:
        d = plan[z]
        p = druck(z)
        alt, neu = _w(_text(os.path.normpath(os.path.join(PROJ, d['quelle'])))) - _w(d['fehlt']), _w(_text(p)) - _w(d['dazu'])
        fehlt, dazu = alt - neu, neu - alt
        za = collections.Counter(''.join(sorted((alt - neu).elements())))
        zn = collections.Counter(''.join(sorted((neu - alt).elements())))
        gleich = not fehlt and not dazu
        trennung = not gleich and za == zn
        ok = ok and (gleich or trennung)
        print(f'{z}: {sum(alt.values())} Wörter im Original, {sum(neu.values())} im Druck · '
              + ('Wortlaut gleich' if gleich else 'gleich bis auf Trennung' if trennung else 'ABWEICHUNG'))
        if not (gleich or trennung):
            print('   fehlt im Druck:', ' '.join(sorted(fehlt))[:400])
            print('   kommt dazu:    ', ' '.join(sorted(dazu))[:400])
    print('\nWortlaut gegen die Originale des Hauses:', 'alle Karten stimmen' if ok else 'ABWEICHUNGEN')
    return ok


def _bild(pdf, seite, tmp):
    from PIL import Image
    subprocess.run(['pdftoppm', '-r', '36', '-f', str(seite), '-l', str(seite), '-png', pdf, tmp], check=True)
    f = next(x for x in sorted(os.listdir(os.path.dirname(tmp))) if x.startswith(os.path.basename(tmp)))
    p = os.path.join(os.path.dirname(tmp), f)
    im = Image.open(p).convert('L')
    os.remove(p)
    return im


def website():
    from PIL import ImageChops, ImageStat
    ok = True
    for z in KARTEN:
        p = druck(z)
        w = os.path.join(PROJ, 'unterlagen', 'pdf', z + '.pdf')
        t = [subprocess.run(['pdftotext', '-layout', x, '-'], capture_output=True, text=True).stdout for x in (p, w)]
        n = [int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', x], capture_output=True, text=True).stdout).group(1)) for x in (p, w)]
        abw = []
        if n[0] == n[1]:
            for s in range(1, n[0] + 1):
                a, b = _bild(p, s, os.path.join(AUS, 'b-ist')), _bild(w, s, os.path.join(AUS, 'b-soll'))
                if a.size != b.size:
                    abw.append(f'S. {s}: Grösse')
                    continue
                d = ImageStat.Stat(ImageChops.difference(a, b)).mean[0]
                if d > 1.0:
                    abw.append(f'S. {s}: Bild weicht ab ({d:.2f})')
        gleich = t[0] == t[1] and n[0] == n[1] and not abw
        ok = ok and gleich
        print(f'{z}: {"wie die PDF der Website" if gleich else "ANDERS"} ({n[0]} Seiten{", Text gleich" if t[0] == t[1] else ", TEXT ANDERS"}{", " + "; ".join(abw) if abw else ", Seitenbilder gleich"})')
    print('\nDrucke gegen die PDFs der Website:', 'gleich' if ok else 'ABWEICHUNGEN')
    return ok


if __name__ == '__main__':
    was = sys.argv[1] if len(sys.argv) > 1 else 'alles'
    r = {'rund': rund, 'wortlaut': wortlaut, 'website': website}
    ergebnis = [r[x]() for x in (r if was == 'alles' else [was])]
    print('\nGESAMT:', 'GRÜN' if all(ergebnis) else 'ROT')
    sys.exit(0 if all(ergebnis) else 1)
