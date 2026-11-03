#!/usr/bin/env python3
"""Die Hausdruckerei · Wirtschaft am Schlössli Bottighofen: legt die Marke des Hauses für die Werkstatt an (nichts abgetippt, alles aus dem Projekt gelesen).
   python3 bau.py   → haeuser/schloessli/ (marke.json, schriften, bilder, mini, kopf, mail, motive.json, druck/, druck.json) + api/_daten/schloessli.json
Quellen (nur gelesen):
  Farben      _werkzeuge/oberflaeche/kleid/schloessli.css und website/assets/css/haus.css: Nacht über dem See, Stuhlblau, Papier, Seespiegel, Blatt,
              Seehimmel nur als Linie und Zeichen, Seehimmel tief als Betonung auf Hell, Tinte, Schirmrot nur als Punkt.
  Schriften   Open Sans 400 (Titel in Versalien gesperrt wie die Wortmarke), Instrument Sans 400/500/600 (Lauf), DM Mono 400 (Etiketten, Gerichte, Zeiten),
              feste TrueType-Schnitte aus _karten/schriften/ (dieselben Schriften wie website/assets/fonts/, dort nur als woff2), kein Type 3 im PDF.
  Zeichen     die Zeiger (kleid/schloessli-zeichen.svg, Pfade aus dem alten Stand der Werkstatt) und die Wortmarke «WIRTSCHAFT AM SCHLÖSSLI»
              (kleid/schloessli-marke.svg#wm, Umrisse in Open Sans), beide unverändert, nie als Schrift nachgebaut.
  Fotos       website/assets/img/<key>-<breite>.webp, Beschreibung aus website/inhalt/bilder.json. Gäste-, Fremd- und KI-Bilder (tb-*, baum, kf-*, pa-teller,
              kp-party, feuerwerk*, ch-*, jz-*, stier, schaefli …) stehen nicht in der Werkstatt."""
import glob, json, os, re, shutil
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
WZ = os.path.dirname(HIER)
PROJ = os.path.dirname(WZ)
WEB = os.path.join(PROJ, 'website')
Z = os.path.join(HIER, 'haeuser', 'schloessli')
KLEID = os.path.join(WZ, 'oberflaeche', 'kleid')
ALT = os.path.join(PROJ, '_werkzeuge.vor-nachtbau-2026-11-03', 'imprimerie', 'haeuser', 'schloessli')

GRUPPEN = ['Eigene Fotos', 'Hafen & Terrasse', 'Küche & Teller', 'Bar & Lästermeile', 'Wein', 'Team', 'Bodensee & Geschichte', 'Instagram des Hauses']
FOTOS = {
    'Hafen & Terrasse': ['start', 'start-hoch', 'platanen', 'abend', 'apero', 'gaststube', 'glas'],
    'Küche & Teller': ['thon', 'tortelloni', 'pasta', 'iberia', 'anguria', 'dessert', 'fisch', 'fleisch', 'salat', 'suppe', 'torte'],
    'Bar & Lästermeile': ['bar', 'fliesen', 'regal', 'schild'],
    'Wein': ['wein'],
    'Team': ['jonas', 'moni', 'lukas', 'team'],
    'Bodensee & Geschichte': ['bootshafen', 'saentis', 'morgen', 'abendschiff', 'schifflaende', 'haus', 'luft1954'],
    'Instagram des Hauses': ['ig-hafen', 'ig-luft', 'ig-terrasse', 'ig-abend', 'ig-teller', 'ig-pasta', 'ig-herd', 'ig-dessert'],
}
# Nie in der Werkstatt (Rechte, UEBERGABE.md): Gäste-, Fremd-, KI- und Schwesterhaus-Bilder
RAUS = ['abend-hafen', 'baum', 'lounge', 'mi-teller', 'sauce', 'teller', 'stier', 'schaefli', 'schaefli-strasse', 'feuerwerk', 'feuerwerk-ki', 'kp-party', 'pa-teller',
        'kf-anrichten', 'kf-deck-abend', 'kf-teller', 'tb-dunkel', 'tb-fisch', 'tb-glas', 'tb-hafen', 'tb-teller', 'jz-fruehling', 'jz-herbst', 'jz-sommer',
        'ch-anzeige', 'ch-luftkarte', 'ch-mann', 'ch-portal', 'ch-postkarte', 'ch-strandhotel', 'ch-ufer', 'ch-zeichnung']
# Kopf der Ansichten (buehne.js / oberflaeche.js): je Ansicht ein Raum des Hauses
KOPF = ['start', 'moni', 'gaststube', 'schild', 'abend', 'platanen', 'fliesen', 'regal', 'bar', 'glas', 'tortelloni', 'apero', 'anguria', 'bootshafen', 'saentis',
        'thon', 'wein', 'jonas', 'team', 'iberia', 'dessert', 'pasta', 'morgen', 'abendschiff']
ERSATZ = 'start'
# Motive vom See: Hafen, Terrasse und See für Ansichtskarten und Aushänge (Regel des Hauses: Ansichtskarten zeigen nur Hafen, Terrasse oder See)
MOTIVE = [('bootshafen', 'Der Bootshafen', 'Bottighofen'), ('start', 'Terrasse am Mittag', 'Bodensee'), ('saentis', 'Bis zum Säntis', 'Bodensee'),
          ('morgen', 'Morgen am See', 'Bottighofen'), ('abendschiff', 'Das Abendschiff', 'Bodensee'), ('platanen', 'Unter den Platanen', 'Bottighofen'),
          ('abend', 'Abend unter der Platane', 'Bottighofen'), ('schifflaende', 'Die Schifflände', 'Bottighofen'), ('ig-hafen', 'Vom Wasser aus', 'Bottighofen'),
          ('ig-luft', 'Die Terrasse von oben', 'Bottighofen'), ('haus', 'Am Hafen', 'Bottighofen'), ('luft1954', 'Das Schlössli 1954', 'Bottighofen')]
DRUCK = ['start', 'platanen', 'abend', 'bootshafen', 'saentis', 'morgen', 'apero', 'glas', 'thon', 'moni', 'jonas', 'team', 'gaststube', 'schifflaende', 'abendschiff', 'haus']


def bilder_register():
    return json.load(open(os.path.join(WEB, 'inhalt', 'bilder.json'), encoding='utf-8'))


def stufen(key):
    l = glob.glob(os.path.join(WEB, 'assets', 'img', key + '-*.webp'))
    l = [p for p in l if re.search(r'-(\d+)\.webp$', p) and os.path.basename(p)[:-5].rsplit('-', 1)[0] == key]
    return sorted(l, key=lambda p: int(re.search(r'-(\d+)\.webp$', p).group(1)))


def wortmarke():
    """kleid/schloessli-marke.svg#wm (absolute M L H V Q Z in Schrifteinheiten, y nach unten, viewBox 0 -463 40448 1925) → ein Pfad, Höhe 140."""
    svg = open(os.path.join(KLEID, 'schloessli-marke.svg'), encoding='utf-8').read()
    vb = [float(x) for x in re.search(r'<symbol[^>]*viewBox="([^"]+)"', svg).group(1).split()]
    d = re.search(r'<path[^>]*\sd="([^"]+)"', svg).group(1)
    k = 140 / vb[3]
    f = lambda v: ('%.2f' % v).rstrip('0').rstrip('.')
    tok = re.findall(r'[MLHVQZmlhvqz]|-?\d*\.?\d+(?:e-?\d+)?', d)
    aus, i, cmd, x, y = [], 0, None, 0.0, 0.0
    P = lambda px, py: f((px - vb[0]) * k) + ' ' + f((py - vb[1]) * k)
    while i < len(tok):
        t = tok[i]
        if re.match(r'[A-Za-z]', t):
            cmd = t; i += 1
            if cmd in 'Zz':
                aus.append('Z')
            continue
        if cmd == 'M' or cmd == 'L':
            x, y = float(tok[i]), float(tok[i + 1]); i += 2
            aus.append(('M' if cmd == 'M' else 'L') + P(x, y))
            if cmd == 'M':
                cmd = 'L'
        elif cmd == 'H':
            x = float(tok[i]); i += 1; aus.append('L' + P(x, y))
        elif cmd == 'V':
            y = float(tok[i]); i += 1; aus.append('L' + P(x, y))
        elif cmd == 'Q':
            x1, y1, x, y = (float(q) for q in tok[i:i + 4]); i += 4
            aus.append('Q' + P(x1, y1) + ' ' + P(x, y))
        else:
            raise SystemExit('Wortmarke: Befehl %s nicht erwartet' % cmd)
    return dict(vb=[0, 0, round(vb[2] * k, 2), 140], pfade=[''.join(aus)], verh=round(vb[3] / vb[2], 5),
                name='Die Wortmarke WIRTSCHAFT AM SCHLÖSSLI (Umrisse in Open Sans, kleid/schloessli-marke.svg)')


def schriften(S):
    from fontTools.ttLib import TTFont
    from fontTools import subset
    os.makedirs(S, exist_ok=True)
    K = os.path.join(PROJ, '_karten', 'schriften')
    paare = [('OpenSans-Regular.ttf', 'OpenSans-400.ttf'), ('OpenSans-Medium.ttf', 'OpenSans-500.ttf'), ('OpenSans-Light.ttf', 'OpenSans-300.ttf'),
             ('InstrumentSans-Regular.ttf', 'InstrumentSans-400.ttf'), ('InstrumentSans-SemiBold.ttf', 'InstrumentSans-600.ttf'), ('DMMono-Regular.ttf', 'DMMono-400.ttf')]
    for q, z in paare:
        p = os.path.join(K, q)
        if os.path.exists(p):
            shutil.copyfile(p, os.path.join(S, z))
    for q, z in [('InstrumentSans-Medium.ttf', 'InstrumentSans-500.ttf')]:
        for p in (os.path.join(ALT, 'schriften', q), os.path.join(S, q)):
            if os.path.exists(p) and not os.path.exists(os.path.join(S, z)):
                shutil.copyfile(p, os.path.join(S, z))
    for f in glob.glob(os.path.join(S, '*')):   # alte Namen ohne Stärke entfernen
        if not re.search(r'-\d00\.(ttf|woff2)$', f) and not f.endswith('.txt'):
            os.remove(f)
    for f in ('OFL-OpenSans.txt',):
        p = os.path.join(WEB, 'assets', 'fonts', f)
        if os.path.exists(p):
            shutil.copyfile(p, os.path.join(S, f))
    U = list(range(0x20, 0x7f)) + list(range(0xa0, 0x250)) + list(range(0x2000, 0x2070)) + [0x20ac, 0x2122, 0x2190, 0x2192, 0x2212]
    for f in sorted(glob.glob(os.path.join(S, '*.ttf'))):
        o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['*']; o.name_IDs = ['*']; o.notdef_outline = True; o.legacy_kern = True
        ft = TTFont(f); u = subset.Subsetter(o); u.populate(unicodes=U); u.subset(ft); ft.flavor = 'woff2'; ft.save(f[:-4] + '.woff2')


def main():
    for u in ('schriften', 'bilder', 'mini', 'kopf', 'mail', 'druck'):
        os.makedirs(os.path.join(Z, u), exist_ok=True)
    F = dict(navy='#113d88', nacht='#0b1d3d', blau='#0a234c', tinte='#041023', papier='#e7ecf3', creme='#d0dae7', weiss='#f4f6f9', gold='#a2b6cf',
             taupe='#0f3678', messing='#0f3678', tanne='#0a234c', kander='#c5d2e1', laden='#0a234c', punkt='#fd9964', leise='#3d4a5e')
    N = dict(navy='Stuhlblau', nacht='Nacht über dem See', blau='Tief', tinte='Tinte', papier='Papier', creme='Seespiegel', weiss='Blatt', gold='Seehimmel',
             taupe='Seehimmel tief', messing='Seehimmel tief', tanne='Tief', kander='Seehimmel hell', laden='Tief', punkt='Schirmrot (nur als Punkt)', leise='Tinte leise')

    zeichen = json.load(open(os.path.join(ALT, 'marke.json'), encoding='utf-8'))['zeichen'] if os.path.exists(os.path.join(ALT, 'marke.json')) else \
        json.load(open(os.path.join(Z, 'marke.json'), encoding='utf-8'))['zeichen']
    zeichen['name'] = 'Die Zeiger (Zeichen der Wortmarke, kleid/schloessli-zeichen.svg)'
    wm = wortmarke()
    wm['farben'] = dict(grund=F['weiss'], zeichen=F['blau'], text=F['tinte'], hell=F['gold'])

    S = os.path.join(Z, 'schriften')
    schriften(S)
    SCHRIFTEN = {
        'titel': ('Open Sans', 'OpenSans-400.ttf', 'Titel in Versalien gesperrt, Open Sans 400 wie die Wortmarke: nie fett, nie kursiv'),
        'kapitale': ('DM Mono', 'DMMono-400.ttf', 'Gerichte wie auf der Karte in Versalien (THON, CAVATELLI, TORTELLONI), gesperrt'),
        'text': ('Instrument Sans', 'InstrumentSans-400.ttf', 'Lesetext wie die Website'),
        'kursiv': ('Instrument Sans 500', 'InstrumentSans-500.ttf', 'Betont (das Haus setzt nie kursiv, Betonung über Stärke)'),
        'mono': ('DM Mono', 'DMMono-400.ttf', 'Etiketten, Zeiten, Daten, Kopf- und Fusszeile in Versalien gesperrt'),
        'plakat': ('Open Sans 500', 'OpenSans-500.ttf', 'Zeile unter der Wortmarke («DIREKT IM HAFEN VON BOTTIGHOFEN») in Versalien'),
        'plakatfett': ('Instrument Sans 600', 'InstrumentSans-600.ttf', 'Zahlen und Daten gross (Aushang, Ferien)'),
        'kopf': ('Open Sans', 'OpenSans-400.ttf', 'Kopfzeile in Versalien wie die Wortmarke'),
        'detail': ('Instrument Sans', 'InstrumentSans-400.ttf', 'Zeile unter dem Gericht'),
    }

    t = Image.open(os.path.join(Z, 'tapete-dunkel.webp')).convert('RGBA'); g = Image.new('RGBA', t.size, F['navy']); g.alpha_composite(t)
    g.convert('RGB').save(os.path.join(Z, 'mail', '_tapete.jpg'), 'JPEG', quality=86)

    B = bilder_register()
    bilder = []

    def ablegen(key, alt, gr, quelle):
        st = stufen(key)
        if not st:
            print('fehlt:', key); return
        gut = [p for p in st if int(re.search(r'-(\d+)\.webp$', p).group(1)) <= 1800]
        im = ImageOps.exif_transpose(Image.open((gut or st)[-1])).convert('RGB')
        w, h = im.size
        im.save(os.path.join(Z, 'bilder', key + '.webp'), 'WEBP', quality=84, method=5)
        k = im.copy(); k.thumbnail((520, 520), Image.LANCZOS); k.save(os.path.join(Z, 'mini', key + '.webp'), 'WEBP', quality=74, method=5)
        k = im.copy(); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(os.path.join(Z, 'mail', key + '.jpg'), 'JPEG', quality=76, optimize=True, progressive=True)
        if key in KOPF:
            k = im.copy(); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(os.path.join(Z, 'kopf', key + '.webp'), 'WEBP', quality=78, method=5)
            k = im.copy(); k.thumbnail((800, 800), Image.LANCZOS); k.save(os.path.join(Z, 'kopf', key + '-800.webp'), 'WEBP', quality=76, method=5)
        b = dict(key=key, alt=alt, w=w, h=h, gruppe=gr, quelle=quelle)
        n = (B.get(key) or {}).get('nachweis')
        if isinstance(n, dict) and n.get('urheber'):
            b['nachweis'] = '%s, %s' % (n.get('urheber'), n.get('lizenz', ''))
        bilder.append(b)

    for gr in GRUPPEN[1:]:
        for key in FOTOS.get(gr, []):
            if key in RAUS:
                continue
            alt = (B.get(key) or {}).get('alt') or key
            ablegen(key, alt.rstrip('.'), gr, 'website/assets/img')

    da = {b['key'] for b in bilder}
    for u, ext in (('bilder', '.webp'), ('mini', '.webp'), ('mail', '.jpg')):
        for f in os.listdir(os.path.join(Z, u)):
            if f.endswith(ext) and not f.startswith('_') and f[:-len(ext)] not in da:
                os.remove(os.path.join(Z, u, f))
    for f in os.listdir(os.path.join(Z, 'kopf')):
        if f.replace('-800', '')[:-5] not in KOPF:
            os.remove(os.path.join(Z, 'kopf', f))

    # Druckfassungen (satz.js liest druck.json): die grösste Stufe der Website für A3 und A4
    D = os.path.join(Z, 'druck')
    for f in os.listdir(D):
        os.remove(os.path.join(D, f))
    dj = {}
    for k in DRUCK:
        st = stufen(k)
        if not st:
            continue
        im = ImageOps.exif_transpose(Image.open(st[-1])).convert('RGB')
        if max(im.size) <= 1800:
            continue
        im.save(os.path.join(D, k + '.jpg'), 'JPEG', quality=86); dj[k] = list(im.size)
    json.dump(dj, open(os.path.join(Z, 'druck.json'), 'w'))

    idx = {b['key']: b for b in bilder}
    motive = [dict(key=k, titel=t, ort=o, quelle='foto', schrift=False, alt=idx[k]['alt'], w=idx[k]['w'], h=idx[k]['h']) for k, t, o in MOTIVE if k in idx]
    json.dump(motive, open(os.path.join(Z, 'motive.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    H = json.load(open(os.path.join(WEB, 'inhalt', 'haus.json'), encoding='utf-8'))
    z = H['zeiten']
    marke = dict(
        key='schloessli', name='Wirtschaft am Schlössli', voll='Wirtschaft am Schlössli Bottighofen', ort='Bottighofen', artikel='die',
        zeile='Direkt im Hafen von Bottighofen',
        satz=H['satz_lage'],
        adr='%s · %s' % (H['strasse'], H['ort']), tel=H['telefon'], mail=H['mail'], web=H['instagram_name'],
        zeiten='%s · %s' % (z['tage'], z['offen']), kueche=' und '.join(z['kueche']), ruhetag=z['ruhetag'], ferien=H['ferien'],
        farben=F, farbnamen=N,
        toene=dict(
            dunkel=dict(grund='navy', tapete='dunkel', titel='weiss', text='papier', mono='gold', linie='gold', zeichen='gold', schild='papier', schild_text='navy'),
            hell=dict(grund='weiss', tapete=None, titel='blau', text='tinte', mono='taupe', linie='taupe', zeichen='navy', schild='navy', schild_text='weiss'),
            creme=dict(grund='papier', tapete='hell', titel='blau', text='tinte', mono='taupe', linie='taupe', zeichen='navy', schild='navy', schild_text='weiss'),
        ),
        schriften={k: dict(familie=f, datei=d, wofuer=w) for k, (f, d, w) in SCHRIFTEN.items()},
        tapete=dict(dunkel='tapete-dunkel.webp', hell='tapete-hell.webp', rapport_mm=14),
        zeichen=zeichen, zeichen2=wm,
        abende=[],
        betriebe=[('Das Restaurant', 'mediterrane Küche à la carte, Küche %s' % ' und '.join(k.replace(' Uhr', '') for k in z['kueche'])),
                  ('Die Lästermeile', 'die Bar mit durchgehender Karte, Zementfliesen und Blick auf den See'),
                  ('Die Seeterrasse', 'direkt im Hafen von Bottighofen, unter den Platanen'),
                  ('Banketts & Gruppen', 'auf zwei Etagen für jeweils bis zu 26 Personen'),
                  ('Anlässe', 'Four-Hands-Dinner, Excellence Gourmetkreuzfahrt')],
        regeln=['Anrede «Sie», herzlich und unkompliziert, wie das Haus auf seiner Seite schreibt («Mehr Wirtschaft, weniger feine Pinkel»). Nie werblich laut, keine Ausrufezeichen im Titel.',
                'Schweizer Schreibung: ss statt ß, Anführungszeichen «…».',
                'Titel in Open Sans 400, Versalien gesperrt wie die Wortmarke, nie fett, nie kursiv. Gerichte wie auf der Karte in Versalien (THON, CAVATELLI, TORTELLONI) in DM Mono, die Zeile darunter in Instrument Sans.',
                'Keine Preise auf Drucksachen der Werkstatt: Preise stehen nur auf den Karten des Hauses (Das Kartenpult).',
                'Zeiten wie auf der Seite des Hauses: «Donnerstag - Montag», «11:30 Uhr - 23:00 Uhr», Küche «11:30 Uhr - 13:30 Uhr» und «18:00 Uhr - 20:00 Uhr», Dienstag & Mittwoch Ruhetag.',
                'Trenner «·», eine Achse mittig. Dunkle Flächen in Stuhlblau oder Nacht mit dem Punktraster; Seehimmel nur für Zeichen, Linien und kleine Zeilen; Schirmrot höchstens als Punkt.',
                'Ansichtskarten zeigen nur den Hafen, die Terrasse am See oder den See, Titel = Ort («Bottighofen», «Bodensee»).',
                'Das Haus heisst «Wirtschaft am Schlössli», es liegt direkt im Hafen von Bottighofen am Bodensee. Kein Hotel, keine Zimmer.'],
        bilder=bilder, raus=RAUS, ersatz=ERSATZ, doppelt={},
    )
    json.dump(marke, open(os.path.join(Z, 'marke.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    api = dict(marke)
    api['bilder'] = ['%s | %s | %s' % (b['key'], 'quer' if b['w'] > b['h'] * 1.1 else 'hoch' if b['h'] > b['w'] * 1.1 else 'quadrat', b['alt']) for b in bilder]
    for k in ('zeichen', 'zeichen2'):
        api.pop(k, None)
    os.makedirs(os.path.join(HIER, 'api', '_daten'), exist_ok=True)
    json.dump(api, open(os.path.join(HIER, 'api', '_daten', 'schloessli.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Marke:', len(bilder), 'Fotos,', len(motive), 'Motive vom See,', len(dj), 'Druckfassungen')


if __name__ == '__main__':
    main()
