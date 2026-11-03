# Liest die Karten des Hauses maschinell aus den PDF-Texten in _quelle/ und legt sie als Daten in inhalt/ ab.
# Nichts wird abgetippt: Namen, Beschreibungen und Preise kommen Zeichen für Zeichen aus dem Original (Regel 60d).
# Lauf: python3 karten_lesen.py  →  inhalt/karte.json, inhalt/laestermeile.json, inhalt/lunch.json, inhalt/bankett.json, inhalt/wein.json
import json, re, pathlib

HIER = pathlib.Path(__file__).resolve().parent
Q = HIER.parent / '_quelle' / 'website' / 'pdf-text'
AUS = HIER / 'inhalt'
HAUPT = {'CHAMPAGNER': 'Champagner & Schaumwein', 'WEISSWEIN': 'Weisswein', 'ROSÉ': 'Rosé', 'ROTWEIN': 'Rotwein', 'SÜSSWEIN': 'Süsswein'}
LAENDER_W = ['SCHWEIZ', 'DEUTSCHLAND', 'ÖSTERREICH', 'ITALIEN', 'FRANKREICH', 'SPANIEN', 'PORTUGAL']
LAENDER = ['FRANKREICH', 'ITALIEN', 'IBERISCHE HALBINSEL', 'KLASSIKER']


def speisekarte():
    zeilen = (Q / 'Speisekarte-Oktober.txt').read_text().splitlines()
    karte, land, gericht = [], None, None
    for z in zeilen:
        s = z.strip()
        if not s:
            continue
        if s in LAENDER:
            land = {'land': s.title().replace('Iberische Halbinsel', 'Iberische Halbinsel'), 'gerichte': []}
            karte.append(land); gericht = None; continue
        if land is None or s.startswith(('VEG =', 'Für weitere', 'Alle Preise', 'G = Gluten')):
            continue
        m = re.match(r'^([A-ZÀ-ÜÉÈ][A-ZÀ-Ü0-9É´\' \(\)\.]+?)\s{2,}([A-Za-z/]+)\s{2,}(\d+)$', s)
        if m:
            gericht = {'name': m.group(1).strip(), 'allergene': m.group(2), 'preis': int(m.group(3)), 'text': '', 'haupt': None, 'hinweis': None}
            land['gerichte'].append(gericht); continue
        if gericht and not gericht['text']:
            m2 = re.match(r'^(.*?)(?:\s{2,}(\(.*?\)))?(?:\s{2,}(\d+) Hauptgang)?$', s)
            gericht['text'] = m2.group(1).strip()
            gericht['hinweis'] = m2.group(2)
            gericht['haupt'] = int(m2.group(3)) if m2.group(3) else None
            continue
        if gericht:
            m3 = re.match(r'^(\d+) Hauptgang$', s)
            if m3:
                gericht['haupt'] = int(m3.group(1)); continue
            raise SystemExit('Unerwartete Zeile in der Speisekarte: ' + s)
    fuss = {'mwst': 'Alle Preise verstehen sich in Schweizer Franken inkl. 8,1% MwSt.',
            'veg': 'VEG = vegetarisch, OVEG = als vegetarische Option verfügbar',
            'veg2': 'Für weitere vegetarische Optionen berät Sie gerne unser Service.',
            'allergene': 'G = Gluten, L = Laktose, E = Eier, F = Fische, S = Schalen- und Weichtiere, So = Soja, En = Erdnüsse, N = Nüsse, Se = Sellerie'}
    roh = (Q / 'Speisekarte-Oktober.txt').read_text()
    for v in fuss.values():
        assert v in roh, v
    return {'stand': 'Speisekarte Oktober, PDF vom 30.09.2026', 'quelle': '_quelle/website/pdf/Speisekarte-Oktober.pdf', 'laender': karte, 'fuss': fuss}


def laestermeile():
    zeilen = [z.strip() for z in (Q / 'Lastermeile-Homepage-2339.txt').read_text().splitlines() if z.strip()]
    gruppen, g, eintrag = [], None, None
    for s in zeilen:
        if s == 'TAPAS DURCHGEHEND' or s == 'Zur Stärkung & Süsses':
            g = {'titel': 'Tapas durchgehend' if s.startswith('TAPAS') else s, 'eintraege': []}; gruppen.append(g); continue
        if s.startswith(('G = Gluten', 'Weichtiere')):
            continue
        m = re.match(r'^([A-ZÀ-ÜÉÓ´ ]+?) (\d+)$', s)
        if m:
            eintrag = {'name': m.group(1).strip(), 'preis': int(m.group(2)), 'text': []}; g['eintraege'].append(eintrag); continue
        eintrag['text'].append(s)
    for g in gruppen:
        for e in g['eintraege']:
            e['text'] = ' '.join(e['text'])
    return {'stand': 'Karte der Lästermeile, PDF vom 14.10.2026', 'quelle': '_quelle/website/pdf/Lastermeile-Homepage-2339.pdf', 'gruppen': gruppen,
            'allergene': 'G = Gluten, L = Laktose, E = Eier, F = Fische, S = Schalen- und Weichtiere, So = Soja, En = Erdnüsse, N = Nüsse, Se = Sellerie'}


def lunch():
    roh = (Q / 'Lunch_261019.txt').read_text()
    gaenge = []
    for name, text in [('Kürbissuppe', 'Wachtelei – Serrano Schinken'), ('Risi e bisi', 'Reis – Miesmuschel – Erbsen – Spinat'), ('Joghurt Panna Cotta', 'Apfelcrumble')]:
        assert name in roh and text in roh, name
        gaenge.append({'name': name, 'text': text})
    assert '(3 – Gänge – 35.- Chf)' in roh
    return {'stand': 'Lunch-Menü, PDF «Lunch_261019» vom 18.10.2026', 'quelle': '_quelle/website/pdf/Lunch_261019.pdf', 'titel': 'Lunch – Menü',
            'gaenge': gaenge, 'preis': '3 – Gänge – 35.- Chf', 'preis_zahl': 35}


def bankett():
    zeilen = [z.strip() for z in (Q / 'Bankettmenuvorschlage.txt').read_text().splitlines() if z.strip()]
    menues, m, g = [], None, None
    for s in zeilen:
        k = re.match(r'^(FRÜHLING|SOMMER|HERBST)\s*\((\d+) CHF\)$', s)
        if k:
            m = {'name': k.group(1).title(), 'preis': int(k.group(2)), 'gerichte': []}; menues.append(m); continue
        if m is None:
            continue
        if s.startswith('Aus den Menüs'):
            break
        p = re.match(r'^(.+?)\s+(\d+)$', s)
        if p and p.group(1).upper() == p.group(1):
            g = {'name': p.group(1).strip(), 'preis': int(p.group(2)), 'text': ''}; m['gerichte'].append(g); continue
        g['text'] = (g['text'] + ' ' + s).strip()
    hinweis = 'Aus den Menüs können 3-5 Gerichte ausgewählt werden. Nach Belieben können die Menüs auch gemischt werden (soweit es saisonal möglich ist) oder auch einzelne Gerichte ausgetauscht oder individuell angepasst werden.'
    roh = ' '.join((Q / 'Bankettmenuvorschlage.txt').read_text().split())
    assert hinweis in roh
    return {'stand': 'Bankettmenüvorschläge, PDF vom 29.04.2025', 'quelle': '_quelle/website/pdf/Bankettmenuvorschlage.pdf', 'menues': menues, 'hinweis': hinweis}


def wein():
    zeilen = (Q / '20261014_Weinkarte.txt').read_text().splitlines()
    gruppen, g, region, prod, wein = [], None, None, None, None
    haupt, land, reg = None, None, None
    for z in zeilen:
        s = z.strip()
        if not s or s.startswith(('Alle Preise', 'Alle Weine')) or re.match(r'^–\s*\d+\s*–$', s):
            continue
        lead = len(z) - len(z.lstrip(' '))
        # Überschrift: nur Grossbuchstaben, ohne Preis
        if re.match(r'^[A-ZÄÖÜÉÈÔÂÊ/ \-–&\.]+(\s+A)?$', s) and not re.search(r'\d', s):
            titel = re.sub(r'\s+A$', '', s).strip()
            for teil in [t.strip() for t in re.split(r'\s[-–]\s|\s{3,}', titel) if t.strip()]:
                if any(k in teil for k in HAUPT):
                    haupt = HAUPT[[k for k in HAUPT if k in teil][0]]; land = None; reg = None
                elif teil in LAENDER_W:
                    land = teil.title(); reg = None
                else:
                    reg = teil.title()
            rest = [t.strip() for t in re.split(r'\s[-–]\s|\s{3,}', titel) if t.strip() and not any(k in t for k in HAUPT)]
            label = ' · '.join(_titel(t) for t in rest) or None
            if not gruppen or gruppen[-1]['titel'] != haupt:
                g = {'titel': haupt, 'regionen': []}; gruppen.append(g)
            region = {'titel': label, 'erzeuger': []}; g['regionen'].append(region)
            prod = None; continue
        mw = re.match(r'^(?:(\d{4}|NV)\s+)?(.+?)\s{2,}(\d+[.,]\d+l)\s+(\d+)$', s) if lead < 5 else re.match(r'^(.+?)\s{2,}(\d+[.,]\d+l)\s+(\d+)$', s)
        nur = re.match(r'^(\d+[.,]\d+l)\s+(\d+)$', s)
        if nur and wein:
            wein['flaschen'].append({'gross': nur.group(1), 'preis': int(nur.group(2))}); continue
        if lead >= 5 and not nur:
            # eingerückte Zeile: Wein ohne Jahrgang, Land-Unterzeile oder Anmerkung
            m = re.match(r'^(.+?)\s{2,}(\d+[.,]\d+l)\s+(\d+)$', s)
            if m:
                wein = {'jahr': None, 'name': ' '.join(m.group(1).split()), 'flaschen': [{'gross': m.group(2), 'preis': int(m.group(3))}], 'notiz': None}
                if prod is None:
                    prod = {'name': None, 'weine': []}; (region or _reg(g))['erzeuger'].append(prod)
                prod['weine'].append(wein); continue
            # Länder-Zwischenzeile unter «Diverse Schaumweine» (Deutschland, Italien …) ist keine Anmerkung zum Wein davor (19.10.2026)
            if s.upper() in LAENDER_W:
                prod = {'name': s, 'weine': []}; (region or _reg(g))['erzeuger'].append(prod); wein = None; continue
            if wein and prod and prod['weine'] and wein is prod['weine'][-1] and wein['notiz'] is None and prod['name'] is not None:
                wein['notiz'] = s; continue
            # Unter-Überschrift innerhalb einer Erzeugerzeile (z. B. «Schweiz» unter «Diverse Schaumweine»)
            prod = {'name': (prod['name'] + ' · ' if prod and prod['name'] and not prod['weine'] else '') + s if False else s, 'weine': []}
            (region or _reg(g))['erzeuger'].append(prod); wein = None; continue
        m = re.match(r'^(\d{4})\s+(.+?)\s+(\d+[.,]\d+l)\s+(\d+)$', s)
        if m:
            wein = {'jahr': m.group(1), 'name': ' '.join(m.group(2).split()), 'flaschen': [{'gross': m.group(3), 'preis': int(m.group(4))}], 'notiz': None}
            if prod is None:
                prod = {'name': None, 'weine': []}; (region or _reg(g))['erzeuger'].append(prod)
            prod['weine'].append(wein); continue
        # Erzeuger
        prod = {'name': s, 'weine': []}; (region or _reg(g))['erzeuger'].append(prod); wein = None
    # leere Erzeuger, die nur als Überschrift dienten (Diverse Schaumweine), bleiben als Zwischenzeile stehen
    return {'stand': 'Weinkarte, Stand 14.10.2026 (26 Seiten)', 'quelle': '_quelle/website/pdf/20261014_Weinkarte.pdf', 'gruppen': gruppen,
            'fuss': ['Alle Preise in Schweizer Franken inkl. 8,1% MwSt.', 'Alle Weine enthalten Sulfite']}


def _titel(t):
    klein = {'De', 'Del', 'Du', 'La', 'Le', 'Des'}
    return ' '.join(w.lower() if w in klein and i else w for i, w in enumerate(t.title().split()))


def _reg(g):
    if not g['regionen'] or g['regionen'][-1]['titel'] is not None:
        if not g['regionen']:
            g['regionen'].append({'titel': None, 'erzeuger': []})
    return g['regionen'][-1]


if __name__ == '__main__':
    AUS.mkdir(exist_ok=True)
    for name, f in [('karte', speisekarte), ('laestermeile', laestermeile), ('lunch', lunch), ('bankett', bankett), ('wein', wein)]:
        d = f()
        (AUS / (name + '.json')).write_text(json.dumps(d, ensure_ascii=False, indent=1))
        print(name, 'ok')
