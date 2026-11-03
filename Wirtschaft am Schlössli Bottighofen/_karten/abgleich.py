# abgleich.py · prüft die Karten-Daten (_karten/stand/*.json) gegen die Original-PDF des Hauses, in beide Richtungen.
# Zwei getrennte Wege (Regel 57):
#   A · Wörter: jedes Wort der Daten im Text der PDF (pdftotext -layout) und jedes Wort der PDF in den Daten, mit Anzahl.
#   B · Zahlen: jede Zahl (Preise, Jahrgänge, Flaschen, Prozent) aus einer zweiten Lesung der PDF (pdftotext -raw) gegen die Daten.
# Ausgenommen sind nur Seitenzahlen («– 2 –») und die Fusszeile, die das Original auf jeder Seite wiederholt (einmal in den Daten).
# Ergebnis: _kette/10-kartenmacher/pruefung.md und abgleich.json. Lauf: python3 _karten/abgleich.py
import collections, json, pathlib, re, subprocess

HIER = pathlib.Path(__file__).resolve().parent
PROJ = HIER.parent
PAKET = PROJ / '_kette' / '10-kartenmacher'
ZAHL = re.compile(r'\d+(?:[.,]\d+)?')


def pdf_text(pfad, art):
    t = subprocess.run(['pdftotext', art, str(pfad), '-'], capture_output=True, text=True, check=True).stdout
    return re.sub(r'\b1 er\b', '1er', t)          # hochgestelltes «er» in «1er Cru» (im Bild geprüft), liest pdftotext getrennt


def daten_woerter(e):
    """Alle Wörter, die auf der Karte stehen, ohne erfundenes Deckblatt."""
    w, k = [], e['karte']
    for t in k['teile']:
        if t['art'] == 'deckel':
            if t.get('aus_original'):
                w += t['titel'].split()
            continue
        for p in t['posten']:
            for f in ('titel', 'text', 'jahr', 'name', 'zusatz'):
                if isinstance(p.get(f), str):
                    w += p[f].split()
            for z in p.get('zeilen', []):
                w += z['text'].split()
            for i, pr in enumerate(p.get('preise', [])):
                w += pr.split()
                if p.get('einheiten'):
                    w += p['einheiten'][i].split()
    return w


def fusszeilen(e):
    return [f.strip() for f in e['karte'].get('fuss', '').split(' · ') if f.strip()]


def original_woerter(text, fuss):
    w, fuss_n = [], collections.Counter()
    for z in text.splitlines():
        s = re.sub(r'\s+', ' ', z).strip()
        if not s or re.match(r'^– ?\d+ ?–$', s):
            continue
        if s in fuss:
            fuss_n[s] += 1; continue
        if s == 'CHAMPAGNER/SCHAUMWEIN A':
            s = 'CHAMPAGNER/SCHAUMWEIN'          # weisses «A» ohne Sichtbarkeit (Bild geprüft), siehe pruefung.md
        w += s.split()
    return w, fuss_n


def pruefe(e):
    pdf = PROJ / e['herkunft']['original']
    fuss = fusszeilen(e)
    ow, fuss_n = original_woerter(pdf_text(pdf, '-layout'), fuss)
    dw = daten_woerter(e)
    o, d = collections.Counter(ow), collections.Counter(dw)
    fehlt = o - d          # im Original, nicht in den Daten
    dazu = d - o           # in den Daten, nicht im Original
    # Weg B: Zahlen aus der zweiten Lesung
    roh = pdf_text(pdf, '-raw')
    for f in fuss:
        roh = roh.replace(f, ' ')
    roh = re.sub(r'– ?\d+ ?–', ' ', roh)
    oz = collections.Counter(ZAHL.findall(roh))
    dz = collections.Counter(ZAHL.findall(' '.join(dw)))
    z_fehlt, z_dazu = oz - dz, dz - oz
    # Weg C: jede Preiszeile so, wie sie im Original steht (Name, Jahrgang, Kürzel, Flasche und Preis in derselben Zeile)
    zeilen = {re.sub(r'\s+', ' ', z).strip() for z in pdf_text(pdf, '-layout').splitlines()}
    zeilen |= {re.sub(r'\s+', ' ', z).strip() for z in pdf_text(pdf, '-raw').splitlines()}
    nicht_gefunden = []
    for t in e['karte']['teile']:
        for p in t.get('posten', []):
            if p['t'] != 'gericht' or not p.get('preise'):
                continue
            teile = [p.get('jahr', ''), p['name'], p.get('zusatz', '') if e['id'] != 'laestermeile' else '', (p.get('einheiten') or [''])[0], p['preise'][0]]
            soll = ' '.join(x for x in teile if x)
            if soll not in zeilen and not any(soll in z for z in zeilen):
                nicht_gefunden.append(soll)
    deckel = [t['titel'] for t in e['karte']['teile'] if t['art'] == 'deckel']
    deckel_im_original = {t: (t in ' '.join(ow)) for t in deckel}
    eintraege = sum(1 for t in e['karte']['teile'] if t['art'] == 'inhalt' for p in t['posten'] if p['t'] == 'gericht')
    preise = sum(len(p.get('preise', [])) for t in e['karte']['teile'] if t['art'] == 'inhalt' for p in t['posten'])
    return {'id': e['id'], 'name': e['karte']['name'], 'original': e['herkunft']['original'], 'eintraege': eintraege, 'preise': preise,
            'woerter_original': len(ow), 'woerter_daten': len(dw), 'fehlt': sorted(fehlt.elements()), 'dazu': sorted(dazu.elements()),
            'zahlen_original': sum(oz.values()), 'zahlen_daten': sum(dz.values()), 'zahlen_fehlt': sorted(z_fehlt.elements()), 'zahlen_dazu': sorted(z_dazu.elements()),
            'fuss': {f: fuss_n[f] for f in fuss}, 'zeilen_nicht_gefunden': nicht_gefunden, 'deckel': deckel_im_original}


if __name__ == '__main__':
    ergebnisse = []
    for f in sorted((HIER / 'stand').glob('*.json')):
        ergebnisse.append(pruefe(json.loads(f.read_text())))
    (PAKET / 'abgleich.json').write_text(json.dumps(ergebnisse, ensure_ascii=False, indent=1) + '\n')
    for r in ergebnisse:
        ab = len(r['fehlt']) + len(r['dazu']) + len(r['zahlen_fehlt']) + len(r['zahlen_dazu']) + len(r['zeilen_nicht_gefunden'])
        print(f"{r['id']:14} {r['eintraege']:4} Einträge {r['preise']:4} Preise · Wörter {r['woerter_original']}/{r['woerter_daten']} · Zahlen {r['zahlen_original']}/{r['zahlen_daten']} · Abweichungen {ab}")
        for k in ('fehlt', 'dazu', 'zahlen_fehlt', 'zahlen_dazu', 'zeilen_nicht_gefunden'):
            if r[k]:
                print('   ', k, r[k][:40])
        print('    Fuss', r['fuss'], 'Deckel im Original', r['deckel'])
