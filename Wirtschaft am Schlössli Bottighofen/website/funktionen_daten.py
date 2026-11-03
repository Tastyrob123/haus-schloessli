# Daten für die Gäste-Funktionen (Station 07, Runde 3, Robert 19.10.2026 «okay alle einbaun»).
# Weine: jede Flasche aus inhalt/wein.json (maschinell aus der Weinkarte vom 14.10.2026), dazu Land und Rebsorte.
# Land kommt aus den Überschriften der Karte (Gruppe, Land, Region); die Rebsorte nur, wenn sie wörtlich im Namen steht.
# Geschmack und passende Gerichte stehen nicht in der Karte und werden deshalb nicht gezeigt (offen).
import json, re, pathlib

HIER = pathlib.Path(__file__).resolve().parent
WEIN = json.loads((HIER / 'inhalt' / 'wein.json').read_text())
LAENDER = ['Schweiz', 'Deutschland', 'Österreich', 'Italien', 'Frankreich', 'Spanien', 'Portugal']
# Regionen ohne Landzeile davor (so steht es in der Karte), Zuordnung über das Weinland
REGION_LAND = {'Bündner Herrschaft': 'Schweiz', 'Neuchatel': 'Schweiz', 'Thurgau': 'Schweiz', 'Zürich': 'Schweiz', 'Graubünden': 'Schweiz',
               'Bayerischer Bodensee': 'Deutschland', 'Bayrischer Bodensee': 'Deutschland', 'Franken': 'Deutschland', 'Baden': 'Deutschland', 'Rheinhessen': 'Deutschland',
               'Mosel': 'Deutschland', 'Pfalz': 'Deutschland', 'Nahe': 'Deutschland', 'Rheingau': 'Deutschland',
               'Wachau': 'Österreich', 'Kremstal': 'Österreich', 'Südsteiermark': 'Österreich', 'Burgenland': 'Österreich',
               'Südtirol': 'Italien', 'Piemont': 'Italien', 'Toskana': 'Italien', 'Umbrien': 'Italien', 'Lombardei': 'Italien', 'Calabria': 'Italien',
               'Rioja': 'Spanien', 'Rias Baixas': 'Spanien', 'Catalunya': 'Spanien', 'Calatayud': 'Spanien', 'Jumilla': 'Spanien', 'Penedes': 'Spanien',
               'Ribera del Duero': 'Spanien', 'Priorat': 'Spanien', 'Mallorca': 'Spanien', 'Douro': 'Portugal',
               'Chablis': 'Frankreich', 'Burgund': 'Frankreich', 'Loire': 'Frankreich', 'Rhone': 'Frankreich', 'Bordeaux': 'Frankreich', 'Provence': 'Frankreich'}
REBEN = ['Chardonnay', 'Pinot Gris', 'Pinot Noir', 'Pinot Blanc', 'Riesling-Sylvaner', 'Riesling Sylvaner', 'Welschriesling', 'Riesling', 'Sauvignon Blanc', 'Sauvignac', 'Solaris',
         'Müller-Thurgau', 'Gewürztraminer', 'Completer', 'Sylvaner', 'Grüner Veltliner', 'Weissburgunder', 'Weisser Burgunder', 'Grauburgunder', 'Spätburgunder', 'Blauburgunder',
         'Merlot', 'Cabernet Sauvignon', 'Cabernet Franc', 'Neuburger', 'Aligoté', 'Gamay', 'Syrah', 'Nebbiolo', 'Sangiovese', 'Tempranillo', 'Garnacha', 'Zweigelt', 'Blaufränkisch']
EINHEIT = {'Weisser Burgunder': 'Weissburgunder', 'Riesling Sylvaner': 'Riesling-Sylvaner'}
# Bordeaux-Lagen stehen in der Karte als eigene Zeilen
for lage in ['St. Julien', 'St.-Emillion/Fronsac', 'St.-Estephe', 'Pessac-Leognan', 'Margaux', 'Moulis', 'Haut-Medoc', 'Pauillac', 'Côtes de Bordeaux / Bordeaux Superieur']:
    REGION_LAND[lage] = 'Frankreich'


def land_und_region(titel, land_vorher):
    if not titel:
        return land_vorher, None
    teile = [t.strip() for t in re.split(r' · ', titel)]
    w = titel.split()
    if teile[0] in LAENDER:
        return teile[0], (' · '.join(teile[1:]) or None)
    if w[0] in LAENDER:
        return w[0], ' '.join(w[1:]) or None
    for t in teile:
        if t in REGION_LAND:
            return REGION_LAND[t], titel
    return land_vorher, titel


def reben(text):
    gef = []
    for r in REBEN:
        if re.search(r'(?<![\w-])' + re.escape(r) + r'(?![\w])', text):
            r2 = EINHEIT.get(r, r)
            if r2 not in gef and not any(r2 in g for g in gef):
                gef.append(r2)
    return gef


def weine():
    out, nr = [], 0
    for g in WEIN['gruppen']:
        land = None
        for reg in g['regionen']:
            land, region = land_und_region(reg['titel'], land if reg['titel'] is None or reg['titel'] not in LAENDER else None)
            if reg['titel'] in LAENDER:
                land, region = reg['titel'], None
            for p in reg['erzeuger']:
                erz = p['name']
                l2 = land
                if erz in LAENDER:          # «Diverse Schaumweine»: Länder stehen dort wie Erzeuger
                    l2, erz = erz, None
                r2 = region
                if g['titel'].startswith('Champagner') and erz and erz.startswith('Champagne'):
                    l2, r2 = 'Frankreich', 'Champagne'
                for w in p['weine']:
                    nr += 1
                    name = w['name']
                    out.append({'id': nr, 'art': g['titel'], 'land': l2, 'region': r2, 'erzeuger': erz, 'name': name, 'jahr': w['jahr'],
                                'flaschen': w['flaschen'], 'notiz': w.get('notiz'), 'reben': reben(name + ' ' + (w.get('notiz') or ''))})
                    if p['name'] in LAENDER:
                        erz = None
    return out


if __name__ == '__main__':
    W = weine()
    (HIER / 'assets' / 'data').mkdir(parents=True, exist_ok=True)
    (HIER / 'assets' / 'data' / 'weine.json').write_text(json.dumps(W, ensure_ascii=False, separators=(',', ':')))
    from collections import Counter
    print(len(W), Counter(w['art'] for w in W), Counter(w['land'] for w in W))
    print(Counter(r for w in W for r in w['reben']).most_common(40))
    print([w for w in W if not w['land']][:5])
