# Flaschen- und Landschaftsbilder für den Weinberater (Robert 19.10.2026: «Bilder von den Flaschen … freigestellt … Landschaft vom Weingut»).
# Quelle: öffentliche Weinsuche von Vivino (Rohdaten in _quelle/wein-bilder/vivino_roh.json, gesucht je Wein nach Erzeuger + Name).
# Flasche nur, wenn Erzeuger UND Wein eindeutig passen; sonst keine Flasche (nie das Etikett eines anderen Weins).
# Landschaft: Hintergrundbild der Region bei Vivino, sonst Region gleichen Namens aus der Karte, sonst das Land.
# RECHTE: Bilder bei Vivino bzw. den Weingütern, nur zur Anschauung in der Designstudie. Vor jeder Veröffentlichung klären oder ersetzen.
import json, pathlib, re, sys, unicodedata, urllib.request, io
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

HIER = pathlib.Path(__file__).resolve().parent
QUELLE = HIER.parent / '_quelle' / 'wein-bilder'
ROH = json.loads((QUELLE / 'vivino_roh.json').read_text())
WEINE = json.loads((HIER / 'assets' / 'data' / 'weine.json').read_text())
ZIEL = HIER / 'assets' / 'img' / 'wein'
LAND = {'Schweiz': 'ch', 'Deutschland': 'de', 'Österreich': 'at', 'Frankreich': 'fr', 'Italien': 'it', 'Spanien': 'es', 'Portugal': 'pt'}
LEER = set('weingut domaine domaines chateau château champagne cave caves tenuta bodegas bodega azienda agricola weinbau weinkellerei kellerei maison famille family estate wines vins winery de du la le les des et and & the von zum zur am im der die das di del della e y cantina fattoria cascina herrschaft schloss familie gebrüder geschwister castello dr fils pere jean marc'.split())
# Von Hand geprüft 19.10.2026: anderer Erzeuger, andere Farbe oder andere Lage als auf der Karte, deshalb ohne Flaschenfoto
# Landschaften, die Städte oder fremde Orte statt Weinberge zeigen (Lyon, Wien, Ätna für die Toskana, Venedig, Windmühlen, Barcelona): nie zeigen
SCHLECHT = {'60ZcnTj1Qi-SQNY8iYn7Sg', 'OpZClcRnTV21_UN6-L4dgg', 'RxxS1jkqQ-iGTD_KZLLgzQ', 'WCIaSSA0QMaX1Pjfe2SxEg', 'bl_qn4j1R8iFpdjt9RouEw', 'd1SrUgn0R3eXP9xtxVUIdg', 'eVKu6qi1RcyjGx_HnD-CzQ', 'z4PAmh_nQUK_VcwpoMx4EA'}
NICHT = {13, 14, 48, 123, 126, 173, 225, 235, 250, 253, 343, 344, 379, 461, 89, 127, 128, 172, 176, 226, 227, 323, 463}

# Zweite Suche 20.10.2026 (Vivino-Suche je Wein mit Erzeuger + Name, nur Flaschenfotos), jeder Treffer von Hand geprüft; Herkunft und Quelle in flaschen-zusatz.json
ZUSATZ = json.loads((QUELLE / 'flaschen-zusatz.json').read_text()) if (QUELLE / 'flaschen-zusatz.json').exists() else {}


# Schweizer Regionen: bei Vivino ohne Landschaft, deshalb Wikimedia Commons (frei, Urheber und Lizenz in _quelle/wein-bilder/herkunft-schweiz.json)
CH = {
    'Bündner Herrschaft': ('ch-flaesch', 'https://upload.wikimedia.org/wikipedia/commons/9/98/Fl%C3%A4sch_Autumn_2020_03.jpg', 'Fläsch Autumn 2020 03.jpg', 'CC BY-SA 4.0'),
    'Graubünden': ('ch-maienfeld', 'https://upload.wikimedia.org/wikipedia/commons/6/61/Wein_und_Berge_-_Rebst%C3%B6cke_in_der_B%C3%BCndner_Herrschaft_bei_Maienfeld_GR_%282021%29.jpg', 'Wein und Berge - Rebstöcke in der Bündner Herrschaft bei Maienfeld GR (2021).jpg', 'CC BY-SA 4.0'),
    'Thurgau': ('ch-ottenberg', 'https://upload.wikimedia.org/wikipedia/commons/9/99/Weinbau_am_Ottenberg_und_Restaurant_Thurberg_%28Weinfelden%2C_2015%29.jpg', 'Weinbau am Ottenberg und Restaurant Thurberg (Weinfelden, 2015).jpg', 'CC BY-SA 4.0'),
    None: ('ch-ermatingen', 'https://upload.wikimedia.org/wikipedia/commons/8/83/Weinlese_bei_Ermatingen_TG_%282009%29.jpg', 'Weinlese bei Ermatingen TG (2009).jpg', 'CC BY-SA 4.0'),
    'Zürich': ('ch-eglisau', 'https://upload.wikimedia.org/wikipedia/commons/1/1c/Eglisau-Buchberg_-_Rhinsberg_2011-09-21_13-41-52.jpg', 'Eglisau-Buchberg - Rhinsberg 2011-09-21 13-41-52.jpg', 'CC BY-SA 3.0'),
    'Neuchatel': ('ch-auvernier', 'https://upload.wikimedia.org/wikipedia/commons/f/fd/Auvernier-village.jpg', 'Auvernier-village.jpg', 'CC BY-SA 3.0'),
}
CH['Neuchâtel'] = CH['Neuchatel']


def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return [t for t in re.split(r'[^a-z0-9]+', s) if t and len(t) > 1 and not re.fullmatch(r'(19|20)\d\d', t)]


def kern(s):
    return set(t for t in norm(s) if t not in LEER)


def passt_erz(w, hit):
    a, b = kern(w['erzeuger']), kern(hit['winery'])
    return bool(a and b and (a & b))


def name_wert(w, hit):
    a = kern(w['name']) - kern(w['erzeuger']) - kern(w['region'] or '')
    b = kern(hit['name'])
    if not a:
        return 0.0
    return len(a & b) / len(a)


def flasche(hit):
    v = ((hit.get('img') or {}).get('variations') or {})
    return v.get('bottle_large') or v.get('bottle_medium')


def waehle(w):
    r = ROH.get(str(w['id']), {})
    alle = [h for t in ('a', 'b', 'c') for h in r.get(t, [])]
    erz = [h for h in alle if passt_erz(w, h)]
    best, wert = None, 0
    for h in erz:
        s = name_wert(w, h)
        if s > wert:
            best, wert = h, s
    bild = flasche(best) if best and wert >= .67 and w['id'] not in NICHT else None
    if not bild and str(w['id']) in ZUSATZ:
        bild = ZUSATZ[str(w['id'])]['flasche']
    region = None
    for h in ([best] if best else []) + erz:
        lg = ((h.get('rbg') or {}).get('variations') or {}).get('large')
        if lg and (h.get('land') or '') == LAND.get(w['land']) and not any(x in lg for x in SCHLECHT):
            region = lg
            break
    return {'flasche': bild, 'region_bild': region, 'treffer': best['name'] if best and bild else None, 'weingut': best['winery'] if best else (erz[0]['winery'] if erz else None), 'wert': round(wert, 2)}


def lade(url, ziel, groesse, art):
    if ziel.exists():
        return True
    try:
        roh = urllib.request.urlopen(urllib.request.Request('https:' + url if url.startswith('//') else url, headers={'User-Agent': 'TastyStudios-Designstudie/1.0 (robert@tasty-studios.de)'}), timeout=30).read()
        im = Image.open(io.BytesIO(roh))
        if art == 'flasche':
            im = im.convert('RGBA')
            bb = im.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
            if bb:
                im = im.crop(bb)
            if im.height > groesse:
                im = im.resize((round(im.width * groesse / im.height), groesse), Image.LANCZOS)
            im.save(ziel, 'WEBP', quality=86, method=6)
        else:
            im = im.convert('RGB')
            if im.width > groesse:
                im = im.resize((groesse, round(im.height * groesse / im.width)), Image.LANCZOS)
            im.save(ziel, 'WEBP', quality=78, method=6)
        return True
    except Exception as ex:
        print('fehlt', url, ex)
        return False


if __name__ == '__main__':
    ZIEL.mkdir(parents=True, exist_ok=True)
    wahl = {w['id']: waehle(w) for w in WEINE}
    # Region ohne eigenes Bild: dasselbe Bild wie ein anderer Wein derselben Region der Karte, sonst desselben Landes
    nach_region, nach_land = {}, {}
    for w in WEINE:
        u = wahl[w['id']]['region_bild']
        if u:
            nach_region.setdefault((w['land'], w['region']), u)
            nach_land.setdefault(w['land'], u)
    for w in WEINE:
        x = wahl[w['id']]
        if w['land'] == 'Schweiz' and w['region'] in CH:
            x['region_bild'] = CH[w['region']][1]
        if not x['region_bild']:
            x['region_bild'] = nach_region.get((w['land'], w['region'])) or nach_land.get(w['land'])
    aufgaben = []
    for w in WEINE:
        x = wahl[w['id']]
        if x['flasche']:
            aufgaben.append((x['flasche'], ZIEL / f'f-{w["id"]}.webp', 720, 'flasche', w['id'], 'f'))
        if x['region_bild']:
            ch = [v[0] for v in CH.values() if v[1] == x['region_bild']]
            n = ch[0] if ch else re.search(r'/([^/]+?)(_\d+x\d+)?\.jpe?g$', x['region_bild']).group(1)
            aufgaben.append((x['region_bild'], ZIEL / f'r-{n}.webp', 1280, 'region', w['id'], 'r'))
    erg, einmal = {}, {}
    for a in aufgaben:
        einmal.setdefault(a[1], a)
    fremd = [a for a in einmal.values() if 'wikimedia' not in a[0]]
    with ThreadPoolExecutor(8) as ex:
        ok = dict(zip([a[1] for a in fremd], ex.map(lambda a: lade(*a[:4]), fremd)))
    for a in einmal.values():
        if 'wikimedia' in a[0]:
            ok[a[1]] = lade(*a[:4])
    for a in aufgaben:
        if ok.get(a[1]):
            erg.setdefault(a[4], {})[a[5]] = a[1].name
    karte = {}
    for w in WEINE:
        e = erg.get(w['id'], {})
        k = {}
        if e.get('f'):
            with Image.open(ZIEL / e['f']) as im:
                k['f'] = 'assets/img/wein/' + e['f']
                k['v'] = round(im.width / im.height, 4)
        if e.get('r'):
            k['r'] = 'assets/img/wein/' + e['r']
            # kleine Fassung für die Kärtchen (640 px), die grosse nur in der Wein-Ansicht
            klein = ZIEL / e['r'].replace('.webp', '-640.webp')
            if not klein.exists():
                with Image.open(ZIEL / e['r']) as im:
                    im.convert('RGB').resize((640, round(im.height * 640 / im.width)), Image.LANCZOS).save(klein, 'WEBP', quality=74, method=6)
            k['rk'] = 'assets/img/wein/' + klein.name
        if k:
            karte[w['id']] = k
    (QUELLE / 'herkunft-schweiz.json').write_text(json.dumps({v[0]: {'datei': 'https://commons.wikimedia.org/wiki/File:' + v[2].replace(' ', '_'), 'lizenz': v[3]} for v in CH.values()}, ensure_ascii=False, indent=1))
    (QUELLE / 'zuordnung.json').write_text(json.dumps({w['id']: {**wahl[w['id']], 'karte': f"{w['erzeuger']} · {w['name']}"} for w in WEINE}, ensure_ascii=False, indent=1))
    # eigene Datei, damit funktionen_daten.py die Weine neu lesen kann, ohne die Bilder zu verlieren
    (HIER / 'assets' / 'data' / 'wein-bilder.json').write_text(json.dumps(karte, separators=(',', ':')))
    print('Flaschen', sum(1 for k in karte.values() if 'f' in k), 'Landschaften', sum(1 for k in karte.values() if 'r' in k), 'von', len(WEINE))
