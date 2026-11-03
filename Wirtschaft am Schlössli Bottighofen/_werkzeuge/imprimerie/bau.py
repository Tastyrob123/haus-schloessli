#!/usr/bin/env python3
"""L’Imprimerie (Die Werkstatt) · Wirtschaft am Schlössli, Bottighofen: legt die Marke des Hauses für das Studio an (nichts abgetippt, alles aus dem Projekt gelesen).
   python3 bau.py   → haeuser/schloessli/ (marke.json, schriften, tapete, bilder, mini, kopf, mail) + api/_daten/schloessli.json
                      (das Wissen dazu baut _qa/wissen_bau.py → api/_daten/schloessli-wissen.txt)
Quellen (alle im Projekt des Hauses, nur gelesen):
  Farben      website/assets/css/haus.css :root: Farbwelt A «Stuhl und See» aus dem Markenbuch (Station 5, Robert 19.10.2026 «schlössli a»), wie sie die Website
              seit Roberts Wort «Ton in Ton» trägt (website/farbwelt.py: Blau- und Petroltöne um 21° auf das Blau des Platztellers gedreht). Die Drucksachen
              tragen damit dieselben Farben wie die Website und die Werkbank (_werkbank/haus.py FARBEN liest dieselbe Stelle).
  Schriften   website/_werkbank/fonts/*.ttf: Open Sans 400 (Titel in Versalien, aus der Wortmarke gemessen), Instrument Sans, DM Mono; dieselben für Bildschirm und PDF
  Zeichen     website/assets/svg/zeichen.svg: die Zeiger im Kreis aus dem Logo (Markenbuch, _kette/05-markenbauer/marke/zeichen/), Pfade unverändert,
              nur aus der potrace-Schreibweise in absolute Punkte im Nullpunkt umgerechnet
  Tapete      website/assets/svg/tapete-a-dunkel.svg und -hell.svg: Punktraster aus den Kugeln der Zeiger mit den Zeigern als Medaillon (168 px auf der Website)
  Fotos       website/assets/img/<key>-<breite>.webp, Beschreibung und Herkunft aus website/inhalt/bilder.json. In die Werkstatt kommen nur Fotos, die das Haus
              selbst zeigt (Website des Hauses, Instagram des Hauses) und freie Fotos mit Namensnennung (Wikimedia Commons, als fremd gekennzeichnet).
              Nie: KI-Bilder, Gästefotos von Tripadvisor, Fotos des Schwesterhauses, Fotos mit Bildrecht Dritter ohne Freigabe (RAUS).
Die Schlüssel der Farben (navy, papier, creme, weiss, gold, taupe, messing) sind die Rollen, die der Kern des Studios kennt;
die Werte und Namen sind die des Schlössli (navy = Stuhlblau, gold = Seehimmel, messing = Seehimmel tief, taupe = Seehimmel dunkel)."""
import json, os, re, shutil, subprocess
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HIER))          # Wirtschaft am Schlössli Bottighofen
WEB = os.path.join(PROJ, 'website')
Z = os.path.join(HIER, 'haeuser', 'schloessli')

ROLLEN = ['Eigene Fotos', 'Hafen & Terrasse', 'Küche & Teller', 'Bar & Lästermeile', 'Wein', 'Team', 'Bodensee & Geschichte', 'Instagram des Hauses']
GRUPPE = {
    'start': 'Hafen & Terrasse', 'start-hoch': 'Hafen & Terrasse', 'platanen': 'Hafen & Terrasse', 'glas': 'Hafen & Terrasse', 'apero': 'Hafen & Terrasse',
    'abend': 'Hafen & Terrasse', 'gaststube': 'Hafen & Terrasse', 'schild': 'Bar & Lästermeile',
    'thon': 'Küche & Teller', 'pasta': 'Küche & Teller', 'iberia': 'Küche & Teller', 'tortelloni': 'Küche & Teller', 'anguria': 'Küche & Teller',
    'dessert': 'Küche & Teller', 'suppe': 'Küche & Teller', 'fisch': 'Küche & Teller', 'salat': 'Küche & Teller', 'fleisch': 'Küche & Teller', 'torte': 'Küche & Teller',
    'bar': 'Bar & Lästermeile', 'regal': 'Bar & Lästermeile', 'fliesen': 'Bar & Lästermeile', 'wein': 'Wein',
    'moni': 'Team', 'team': 'Team', 'jonas': 'Team', 'lukas': 'Team',
    'haus': 'Bodensee & Geschichte', 'bootshafen': 'Bodensee & Geschichte', 'luft1954': 'Bodensee & Geschichte', 'morgen': 'Bodensee & Geschichte',
    'schifflaende': 'Bodensee & Geschichte', 'saentis': 'Bodensee & Geschichte', 'abendschiff': 'Bodensee & Geschichte',
}
# Fotos, die das Haus nicht zeigen darf (Grund steht dabei): nie in die Werkstatt, alte Kopien werden beim Bau entfernt
RAUS = {
    'teller': 'bearbeitete Fassung (website/bearbeitet/teller-anguria.jpg), das Original «anguria» ist da',
    'feuerwerk': 'Bildrecht laut Dateiname bei «Keller», nicht geklärt (website/bilder.py)',
    'feuerwerk-ki': 'KI-Bild, nur Platzhalter der Website', 'schaefli': 'Schwesterhaus Taverne zum Schäfli', 'kp-party': 'Kitchen Party im Schäfli (Schwesterhaus)',
    'baum': 'Gästefoto Tripadvisor', 'tb-fisch': 'Gästefoto Tripadvisor', 'tb-glas': 'Gästefoto Tripadvisor', 'tb-teller': 'Gästefoto Tripadvisor', 'tb-dunkel': 'Gästefoto Tripadvisor',
    'lounge': 'Schweiz Tourismus (myswitzerland), Rechte nicht geklärt', 'sauce': 'Schweiz Tourismus (myswitzerland), Rechte nicht geklärt',
    'mi-teller': 'Guide Michelin, Rechte beim Guide', 'stier': 'Papageno Konstanz', 'pa-teller': 'Papageno Konstanz',
    'kf-teller': 'Excellence/Twerenbold', 'kf-deck-abend': 'Excellence/Twerenbold', 'kf-anrichten': 'Excellence/Twerenbold',
    'abend-hafen': 'Gottlieben, nicht der Hafen des Hauses', 'jz-fruehling': 'Stimmungsbild, nicht das Haus', 'jz-sommer': 'Stimmungsbild, nicht das Haus', 'jz-herbst': 'Stimmungsbild, nicht das Haus',
}
# ch-* (Heft der Gemeinde 1994, mit KI nachgeschärft) fallen über die Regel «KI» weg
# Ansichten des Studios: Foto im Kopf (1200 px, haeuser/schloessli/kopf/)
KOPF = ['start', 'platanen', 'glas', 'apero', 'abend', 'gaststube', 'schild', 'bar', 'regal', 'fliesen', 'wein', 'tortelloni', 'anguria', 'thon', 'dessert',
        'team', 'moni', 'jonas', 'pasta', 'fisch', 'iberia']


def potrace_pfade(svg):
    """potrace-SVG (transform translate/scale, Befehle m M c l z, relativ) → Liste von Pfaden als absolute Befehle in Einheiten der Seite (y nach unten).
    Die Umlaufrichtung bleibt erhalten (beide Achsen gleich gespiegelt), deshalb füllen PDF (pdf-lib, nonzero) und Bildschirm gleich."""
    tr = re.search(r'translate\(([-\d.]+),([-\d.]+)\)\s*scale\(([-\d.]+),([-\d.]+)\)', svg)
    tx, ty, sx, sy = (float(x) for x in tr.groups()) if tr else (0, 0, 1, 1)
    alle = []
    for d in re.findall(r'\sd="([^"]+)"', svg):
        tok = re.findall(r'[MmCcLlZz]|-?\d*\.?\d+', d)
        i, cmd, x, y, sx0, sy0, teile = 0, None, 0.0, 0.0, 0.0, 0.0, []
        while i < len(tok):
            t = tok[i]
            if re.match(r'[A-Za-z]', t):
                cmd = t; i += 1
                if cmd in 'Zz':
                    teile.append(('Z',)); x, y = sx0, sy0
                continue
            n = {'M': 2, 'm': 2, 'L': 2, 'l': 2, 'C': 6, 'c': 6}[cmd]
            v = [float(q) for q in tok[i:i + n]]; i += n
            rel = cmd.islower()
            if cmd in 'Mm':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1]); sx0, sy0 = x, y
                teile.append(('M', x, y)); cmd = 'l' if rel else 'L'
            elif cmd in 'Ll':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1]); teile.append(('L', x, y))
            else:
                p = [(x + v[k], y + v[k + 1]) if rel else (v[k], v[k + 1]) for k in (0, 2, 4)]
                teile.append(('C', *p[0], *p[1], *p[2])); x, y = p[2]
        neu = []
        for t in teile:
            if t[0] == 'Z':
                neu.append(t); continue
            q = []
            for k in range(1, len(t), 2):
                q += [tx + sx * t[k], ty + sy * t[k + 1]]
            neu.append((t[0], *q))
        alle.append(neu)
    return alle


def rahmen(pfade):
    pts = [(t[k], t[k + 1]) for p in pfade for t in p if t[0] != 'Z' for k in range(1, len(t), 2)]
    return min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)


def zeichen():
    """Die Zeiger im Kreis (website/assets/svg/zeichen.svg), Höhe 140 Einheiten."""
    ges = potrace_pfade(open(os.path.join(WEB, 'assets/svg/zeichen.svg'), encoding='utf-8').read())
    x0, y0, x1, y1 = rahmen(ges)
    k = 140 / (y1 - y0)
    f = lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')
    aus = []
    for p in ges:
        s = []
        for t in p:
            if t[0] == 'Z':
                s.append('Z'); continue
            q = [f((t[j] - x0) * k) if j % 2 == 1 else f((t[j] - y0) * k) for j in range(1, len(t))]
            s.append(t[0] + ' '.join(q))
        aus.append(''.join(s))
    return aus, [0, 0, round((x1 - x0) * k, 2), 140]


def tapete(quelle, farbe, deckung_punkte, deckung_zeiger, ziel, breite=336):
    """Kachel der Website-Tapete (168 px, doppelte Dichte) mit eigener Farbe und Deckkraft als WebP mit Alpha."""
    s = open(os.path.join(WEB, 'assets/svg', quelle), encoding='utf-8').read()
    s = re.sub(r'fill="#[0-9A-Fa-f]{6}" fill-opacity="[\d.]+"(?=><circle)', f'fill="{farbe}" fill-opacity="{deckung_punkte}"', s, count=1)
    s = re.sub(r'(<svg x="[\d.]+" y="[\d.]+" width="[\d.]+" height="[\d.]+" viewBox="[^"]+") fill="#[0-9A-Fa-f]{6}" fill-opacity="[\d.]+"', rf'\1 fill="{farbe}" fill-opacity="{deckung_zeiger}"', s, count=1)
    tmp_svg, tmp_png = ziel + '.svg', ziel + '.png'
    open(tmp_svg, 'w', encoding='utf-8').write(s)
    env = dict(os.environ, NODE_PATH=os.path.expanduser('~/Aussen-Pruefung/node_modules'))
    subprocess.run(['node', os.path.join(HIER, '_qa', 'svg_png.js'), tmp_svg, tmp_png, str(breite)], check=True, env=env)
    Image.open(tmp_png).save(ziel, 'WEBP', lossless=True)
    os.remove(tmp_svg); os.remove(tmp_png)


def schloessli():
    for u in ('schriften', 'bilder', 'mini', 'kopf', 'mail'):
        os.makedirs(os.path.join(Z, u), exist_ok=True)

    css = open(os.path.join(WEB, 'assets/css/haus.css'), encoding='utf-8').read()
    V = {k: v.lower() for k, v in re.findall(r'--([a-z0-9-]+):(#[0-9a-fA-F]{6})', css[css.index(':root{'):css.index('}', css.index(':root{'))])}
    F = dict(navy=V['tief'], nacht=V['nacht'], blau=V['stuhl'], tinte=V['tinte'], papier=V['kalk'], creme=V['kalk2'], weiss=V['papier'],
             gold=V['himmel'], taupe=V['himmel-t'], messing=V['titel-h'], tanne=V['stuhl'], kander=V['himmel-h'], laden=V['punkt'])
    N = dict(navy='Stuhlblau', nacht='Nacht über dem See', blau='Stuhlblau hell', tinte='Tinte', papier='Papier', creme='Seespiegel', weiss='Blatt', gold='Seehimmel',
             taupe='Seehimmel tief', messing='Hafenblau', tanne='Stuhlblau hell', kander='Seehimmel hell', laden='Schirmrot')

    pfade, vb = zeichen()

    FD = os.path.join(WEB, '_werkbank/fonts')
    SCHRIFTEN = {
        'titel': ('Open Sans', 'OpenSans-Regular.ttf', 'Titel und Namen in Versalien, Open Sans 400 wie die Wortmarke (gemessen, Markenbuch)'),
        'kapitale': ('Open Sans', 'OpenSans-Regular.ttf', 'Namen in Versalien'),
        'text': ('Instrument Sans', 'InstrumentSans-Regular.ttf', 'Fliesstext'),
        'kursiv': ('Instrument Sans Medium', 'InstrumentSans-Medium.ttf', 'Einleitung; die Website setzt nicht kursiv, Betonung über Farbe'),
        'mono': ('DM Mono', 'DMMono-Regular.ttf', 'Zeilen in gesperrten Versalien, Zeiten'),
    }
    for _, (_, datei, _) in SCHRIFTEN.items():
        shutil.copy2(os.path.join(FD, datei), os.path.join(Z, 'schriften', datei))

    # Tapete: Punktraster mit den Zeigern. Auf der Website 22 % (Punkte) und 12 % (Zeiger) Seehimmel auf Stuhlblau; im Druck kräftiger
    # (auf Papier verschwinden feine Punkte), für helle Flächen dieselbe Kachel in Stuhlblau hell wie auf der Website. In der Oberfläche leiser.
    tapete('tapete-a-dunkel.svg', F['gold'], .3, .18, os.path.join(Z, 'tapete-dunkel.webp'))
    tapete('tapete-a-hell.svg', F['blau'], .26, .14, os.path.join(Z, 'tapete-hell.webp'))
    tapete('tapete-a-dunkel.svg', F['gold'], .16, .09, os.path.join(Z, 'tapete-ui-dunkel.webp'))
    tapete('tapete-a-hell.svg', F['blau'], .12, .07, os.path.join(Z, 'tapete-ui-hell.webp'))

    # Grund der Newsletter-Mails: Stuhlblau mit dem Punktraster, als JPG (Mailprogramme zeigen keine durchsichtigen Kacheln zuverlässig)
    t = Image.open(os.path.join(Z, 'tapete-dunkel.webp')).convert('RGBA'); g = Image.new('RGBA', t.size, F['navy']); g.alpha_composite(t)
    g.convert('RGB').save(os.path.join(Z, 'mail', '_tapete.jpg'), 'JPEG', quality=86)

    # Fotos
    BJ = json.load(open(os.path.join(WEB, 'inhalt/bilder.json'), encoding='utf-8'))
    LIVRE = os.path.join(PROJ, '_werkzeuge', 'livre')
    LJ = os.path.join(LIVRE, 'livre.json')
    LV = {f['k']: f for f in json.load(open(LJ, encoding='utf-8')).get('fotos', [])} if os.path.exists(LJ) else {}
    bilder, neu, raus = [], 0, []
    for key in list(RAUS) + [k for k in BJ if k.startswith('ch-')]:
        for u, e in (('bilder', '.webp'), ('mini', '.webp'), ('mail', '.jpg'), ('kopf', '.webp')):
            if os.path.exists(os.path.join(Z, u, key + e)): os.remove(os.path.join(Z, u, key + e))
    for key, m in BJ.items():
        nw = m.get('nachweis') or {}
        if key in RAUS or 'KI' in (nw.get('lizenz') or '') or '/ki/' in m['datei'] or key not in GRUPPE and not key.startswith('ig-'):
            raus.append(key); continue
        q = os.path.join(WEB, 'assets/img', f"{key}-{max(m['breiten'])}.webp")
        if key in LV and LV[key].get('fl') and os.path.exists(os.path.normpath(os.path.join(LIVRE, LV[key]['fl']))):
            q = os.path.normpath(os.path.join(LIVRE, LV[key]['fl']))   # kennt das Hausbuch das Foto, gilt dessen Datei (Master F80)
        if not os.path.exists(q) or not m.get('alt'):
            raus.append(key); continue
        ziel, mini = os.path.join(Z, 'bilder', key + '.webp'), os.path.join(Z, 'mini', key + '.webp')
        im = Image.open(q); w, h = im.size
        if not os.path.exists(ziel) or os.path.getmtime(ziel) < os.path.getmtime(q) or Image.open(ziel).size != (w, h):
            shutil.copy2(q, ziel); neu += 1
            for alt in (mini, os.path.join(Z, 'mail', key + '.jpg'), os.path.join(Z, 'kopf', key + '.webp')):
                if os.path.exists(alt): os.remove(alt)
        if not os.path.exists(mini) or os.path.getmtime(mini) < os.path.getmtime(q):
            k = im.convert('RGB'); k.thumbnail((520, 520), Image.LANCZOS); k.save(mini, 'WEBP', quality=74, method=5)
        mail = os.path.join(Z, 'mail', key + '.jpg')
        if not os.path.exists(mail) or os.path.getmtime(mail) < os.path.getmtime(q):
            k = im.convert('RGB'); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(mail, 'JPEG', quality=76, optimize=True, progressive=True)
        if key in KOPF:
            k = im.convert('RGB'); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(os.path.join(Z, 'kopf', key + '.webp'), 'WEBP', quality=78, method=5)
        b = dict(key=key, alt=m['alt'], w=w, h=h, gruppe=GRUPPE.get(key, 'Instagram des Hauses'))
        if nw.get('lizenz'):
            b['quelle'] = f"Wikimedia Commons · {nw.get('urheber')} · {nw.get('lizenz')} · {nw.get('quelle')}"
        bilder.append(b)
    bilder.sort(key=lambda b: (ROLLEN.index(b['gruppe']), b['key']))

    H = json.load(open(os.path.join(WEB, 'inhalt/haus.json'), encoding='utf-8'))
    tel = H['telefon']
    marke = dict(
        key='schloessli', name='Wirtschaft am Schlössli', voll='Wirtschaft am Schlössli', ort='Bottighofen',
        zeile='Direkt im Hafen von Bottighofen', satz=H['satz_terrasse'],
        adr=H['strasse'] + ' · ' + H['ort'], tel=tel, mail=H['mail'], web='www.schloessli-bottighofen.ch',
        farben=F, farbnamen=N,
        toene=dict(
            dunkel=dict(grund='navy', tapete='dunkel', titel='weiss', text='papier', mono='gold', linie='gold', zeichen='gold', schild='papier', schild_text='navy'),
            hell=dict(grund='papier', tapete=None, titel='navy', text='tinte', mono='taupe', linie='messing', zeichen='navy', schild='navy', schild_text='papier'),
            creme=dict(grund='creme', tapete='hell', titel='navy', text='tinte', mono='taupe', linie='messing', zeichen='navy', schild='navy', schild_text='papier'),
        ),
        schriften={k: dict(familie=f, datei=d, wofuer=w) for k, (f, d, w) in SCHRIFTEN.items()},
        tapete=dict(dunkel='tapete-dunkel.webp', hell='tapete-hell.webp', rapport_mm=14),
        zeichen=dict(vb=vb, pfade=pfade, verh=vb[3] / vb[2], name='Die Zeiger'),
        betriebe=[('Das Restaurant', 'mediterrane Küche à la carte, Küche 11:30–13:30 und 18:00–20:00'), ('Die Lästermeile', 'die Bar, Tapas durchgehend'),
                  ('Die Seeterrasse', 'direkt im Hafen von Bottighofen'), ('Banketts & Gruppen', 'auf zwei Etagen für jeweils bis zu 26 Personen'),
                  ('Lunch-Menü', 'drei Gänge'), ('Events & Termine', 'Four-Hands, Kreuzfahrt, Seenachtfest')],
        regeln=['Anrede «Sie», herzlich und unkompliziert, wie das Haus auf seiner Seite schreibt («Mehr Wirtschaft, weniger feine Pinkel»). Nie werblich laut.',
                'Schweizer Schreibung: ss statt ß, Anführungszeichen «…».',
                'Gerichte so schreiben, wie sie auf der Karte stehen (THON, CAVATELLI, TORTELLONI …), mit der Zeile darunter; nie übersetzen oder glätten.',
                'Keine Preise auf Drucksachen der Werkstatt: Preise stehen nur auf den Karten des Hauses (Die Tafel).',
                'Zeiten wie auf der Seite des Hauses: «Donnerstag - Montag», «11:30 Uhr - 23:00 Uhr», Küche «11:30 Uhr - 13:30 Uhr» und «18:00 Uhr - 20:00 Uhr».',
                'Titel kurz, höchstens fünf Wörter, in Versalien gesetzt wie die Wortmarke. Keine Ausrufezeichen im Titel.',
                'Dunkle Flächen in Stuhlblau, immer mit dem Punktraster der Zeiger. Seehimmel nur für Zeichen, Linien und kleine Zeilen; Schirmrot höchstens als Punkt.',
                'Betonung über Farbe, nie kursiv.', 'Ansichtskarten zeigen nur den Hafen, die Terrasse am See oder den See, Titel = Ort («Bottighofen», «Bodensee»).',
                'Das Haus heisst «Wirtschaft am Schlössli», es liegt direkt im Hafen von Bottighofen am Bodensee. Kein Hotel, keine Zimmer. Das Schwesterhaus (Taverne zum Schäfli) kommt in keiner Drucksache vor.'],
        bilder=bilder,
        raus=sorted(set(raus)),   # nie in der Werkstatt, auch nicht über das Hausbuch (satz.js filtert die Fotos des Hausbuchs damit)
    )
    json.dump(marke, open(os.path.join(Z, 'marke.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump({}, open(os.path.join(Z, 'druck.json'), 'w'))   # gedruckt wird die grösste Fassung der Website (I03), Originale liegen in _quelle/

    D = os.path.join(HIER, 'api', '_daten')
    os.makedirs(D, exist_ok=True)
    ki = {k: v for k, v in marke.items() if k not in ('zeichen', 'bilder')}
    ki['bilder'] = [f"{b['key']} | {'quer' if b['w'] > b['h'] * 1.1 else 'hoch' if b['h'] > b['w'] * 1.1 else 'quadratisch'} | {b['alt']}" for b in bilder]
    json.dump(ki, open(os.path.join(D, 'schloessli.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('schloessli:', len(bilder), 'Fotos,', neu, 'neu kopiert,', len(raus), 'nicht übernommen,', len(pfade), 'Pfade im Zeichen', vb, ',',
          len(os.listdir(os.path.join(Z, 'kopf'))), 'Köpfe', '· Hausbuch', 'gelesen' if LV else 'noch ohne livre.json')


if __name__ == '__main__':
    schloessli()
