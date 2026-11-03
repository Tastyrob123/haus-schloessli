# lesen.py · Station 10 (Kartenmacher) · Wirtschaft am Schlössli Bottighofen
# Liest jede Karte des Hauses aus der Textschicht ihrer PDF (_quelle/website/pdf/*.pdf, pdftotext -layout)
# und legt sie im Format von La Carte (_Werkzeuge/werkzeuge/karten/modell.py) unter _karten/stand/<id>.json ab.
# Nichts ist abgetippt: jeder Name, jeder Text, jeder Preis kommt Zeichen für Zeichen aus dem Original (Regel 60d).
# Die Regeln unten sagen nur, welches Stück in welches Feld gehört. Was nicht zuzuordnen ist, bricht den Lauf ab.
# Lauf: python3 _karten/lesen.py   →   _karten/stand/*.json, _karten/haus.json (alle Karten als ein Dokument für La Carte)
import hashlib, json, pathlib, re, subprocess, sys

HIER = pathlib.Path(__file__).resolve().parent
PROJ = HIER.parent
PDF = PROJ / '_quelle' / 'website' / 'pdf'
STAND = HIER / 'stand'
sys.path.insert(0, str(pathlib.Path.home() / 'Desktop/Website-Projekte/_Werkzeuge/werkzeuge/karten'))
import modell as M  # noqa: E402  (nur prüfen, nie schreiben)

A4, A4Q = [210, 297], [297, 210]


def text(datei):
    return subprocess.run(['pdftotext', '-layout', str(PDF / datei), '-'], capture_output=True, text=True, check=True).stdout


def seiten(datei):
    return text(datei).split('\f')


def eng(s):
    """Leerraum des Satzes (Spalten von pdftotext) zu einem Leerzeichen; die Zeichen selbst bleiben."""
    return re.sub(r'\s+', ' ', s).strip()


def hoch(s):
    """«1er» steht im Original mit hochgestelltem «er» (im Bild geprüft, Weinkarte S. 12); pdftotext liest «1 er»."""
    return re.sub(r'\b1 er\b', '1er', s)


def herkunft(datei):
    roh = (PDF / datei).read_bytes()
    return {'original': f'_quelle/website/pdf/{datei}', 'sha256': hashlib.sha256(roh).hexdigest(),
            'adresse': f'https://www.schloessli-bottighofen.ch/s/{datei}', 'abgerufen': '2026-10-19', 'gelesen_mit': '_karten/lesen.py'}


def eintrag(kid, datei, karte, offen, gilt=('', '')):
    return {'id': kid, 'gilt': {'von': gilt[0], 'bis': gilt[1]}, 'fassungen': {}, 'herkunft': herkunft(datei), 'offen': offen, 'karte': karte}


# ------------------------------------------------------------------ Speisekarte
def speisekarte():
    d = 'Speisekarte-Oktober.pdf'
    LAENDER = ('FRANKREICH', 'ITALIEN', 'IBERISCHE HALBINSEL', 'KLASSIKER')
    MWST = 'Alle Preise verstehen sich in Schweizer Franken inkl. 8,1% MwSt.'
    posten, g = [], None
    for nr, seite in enumerate(seiten(d), 1):
        for z in seite.splitlines():
            s = z.strip()
            if not s:
                continue
            if s in LAENDER:
                posten.append({'t': 'rubrik', 'titel': s, 's': nr}); g = None; continue
            if s == MWST:
                continue                                        # steht als Fusszeile der Karte
            if s.startswith(('VEG =', 'Für weitere', 'G = Gluten')):
                posten.append({'t': 'notiz', 'text': eng(s), 's': nr}); g = None; continue
            m = re.match(r'^(\S.*?)\s{2,}((?:O?VEG/)?[A-Za-z]+(?:/[A-Za-z]+)*)\s{2,}(\d+)$', s)
            if m:
                g = {'t': 'gericht', 'name': m.group(1).strip(), 'zusatz': m.group(2), 'zeilen': [], 'preise': [m.group(3)], 'einheiten': [''], 's': nr}
                posten.append(g); continue
            if g is None:
                raise SystemExit(f'Speisekarte, Seite {nr}: Zeile ohne Gericht: {s}')
            m = re.match(r'^(.*?)(?:\s{2,}(\(.*?\)))?(?:\s{2,}(\d+) (Hauptgang))?$', s)
            if m.group(1):
                g['zeilen'].append({'text': m.group(1).strip()})
            if m.group(2):
                g['zeilen'].append({'text': m.group(2)})
            if m.group(3):
                g['preise'].append(m.group(3)); g['einheiten'].append(m.group(4))
    karte = {'ziel': 'speisekarte', 'name': 'Speisekarte Oktober', 'gruppe': 'Restaurant', 'format': A4, 'kl': '', 'fuss': MWST,
             'teile': [{'art': 'deckel', 'titel': 'Speisekarte', 'unter': '', 'zeilen': []}, {'art': 'inhalt', 'posten': posten}]}
    offen = ['Zeitraum: Titel der Datei «Speisekarte-Oktober», die Karte selbst nennt keinen Monat und kein Jahr. PDF erstellt 30.09.2026.',
             'Deckblatt: das Original hat keins; «Speisekarte» ist der Name, unter dem die Seite /karten die Datei verlinkt.',
             'Allergene: das Haus schreibt Kürzel (G, L, E, F, S, So, En, N, Se) und VEG/OVEG; sie stehen wörtlich im Feld «zusatz». '
             'Nicht in die 14 Allergene von La Carte übertragen, weil «L = Laktose» und «S = Schalen- und Weichtiere» nicht deckungsgleich mit deren Feldern sind.']
    return eintrag('speisekarte', d, karte, offen)


# ------------------------------------------------------------------ Lästermeile
def laestermeile():
    d = 'Lastermeile-Homepage-2339.pdf'
    zeilen = [z.strip() for z in text(d).splitlines() if z.strip()]
    posten, g, i = [], None, 0
    while i < len(zeilen):
        s = zeilen[i]
        if s in ('TAPAS DURCHGEHEND', 'Zur Stärkung & Süsses'):
            posten.append({'t': 'rubrik', 'titel': s, 's': 1}); g = None
        elif s.startswith('G = Gluten'):
            posten.append({'t': 'notiz', 'text': eng(s + ' ' + zeilen[i + 1]), 's': 1}); i += 1; g = None
        elif re.match(r'^[A-ZÀ-ÜÉÓ´ ]+ \d+$', s):
            n, p = s.rsplit(' ', 1)
            g = {'t': 'gericht', 'name': n, 'zeilen': [], 'preise': [p], 's': 1}; posten.append(g)
        elif g is not None:
            m = re.match(r'^(.*?) ([A-Z][A-Za-z]?(?:/[A-Z][A-Za-z]?)*)$', s)
            if m and len(m.group(2)) <= 12 and m.group(2) != s:
                g['zeilen'].append({'text': m.group(1)}); g['zusatz'] = m.group(2)
            else:
                g['zeilen'].append({'text': s})
        else:
            raise SystemExit('Lästermeile: Zeile ohne Gericht: ' + s)
        i += 1
    karte = {'ziel': 'laestermeile', 'name': 'Lästermeile', 'gruppe': 'Bar', 'format': A4, 'kl': '', 'fuss': '',
             'teile': [{'art': 'deckel', 'titel': 'Lästermeile', 'unter': '', 'zeilen': []}, {'art': 'inhalt', 'posten': posten}]}
    offen = ['Zeitraum: die Karte nennt keinen; PDF erstellt 14.10.2026.',
             'Öffnungszeit «11:30 Uhr - 21:00 Uhr» steht nur auf der Seite /karten, nicht in der PDF; nicht in die Karte übernommen.',
             'Die Seite /karten verlinkt beim Titel «Lästermeile» eine zweite Datei (/s/Lastermeile-Homepage-2tbd.pdf), die nicht im Paket liegt; gelesen ist die Fassung 2339.',
             'Währung: die Karte nennt keine (Preise ohne CHF).',
             'Allergen-Kürzel stehen wörtlich im Feld «zusatz», wie in der Speisekarte.']
    return eintrag('laestermeile', d, karte, offen)


# ------------------------------------------------------------------ Lunch
def lunch():
    d = 'Lunch_261019.pdf'
    posten = []
    gruss = []
    gang = None
    for z in text(d).splitlines():
        if not z.strip():
            continue
        # links steht der Gruss in einer eigenen Spalte, rechts das Menü
        links = z[:30].strip() if len(z) - len(z.lstrip()) < 20 else ''
        rest = z[len(z) - len(z.lstrip()) + len(links):].strip() if links else z.strip()
        if links:
            gruss.append(links)
        if not rest:
            continue
        if rest == 'Lunch – Menü':
            posten.append({'t': 'rubrik', 'titel': rest, 's': 1}); continue
        if rest == '***':
            posten.append({'t': 'frei', 'zeilen': [{'text': '***'}], 's': 1}); gang = None; continue
        if rest.startswith('('):
            posten.append({'t': 'notiz', 'text': rest, 's': 1}); continue
        if gang is None:
            gang = {'t': 'gericht', 'name': rest, 'zeilen': [], 's': 1}; posten.append(gang)
        else:
            gang['zeilen'].append({'text': rest})
    posten.insert(1, {'t': 'frei', 'zeilen': [{'text': eng(' '.join(gruss))}], 's': 1})
    karte = {'ziel': 'lunch', 'name': 'Lunch-Menü', 'gruppe': 'Restaurant', 'format': A4Q, 'kl': 'mittag', 'fuss': '',
             'teile': [{'art': 'inhalt', 'posten': posten}]}
    offen = ['Zeitraum: die Karte nennt keinen Tag. Datei «Lunch_261019» (PDF erstellt 18.10.2026, 23:44); ob 261019 der 19.10.2026 ist, sagt das Haus nicht.',
             'Wochentage und Uhrzeit des Lunchs nennt die PDF nicht.',
             'Die Karte wechselt (Startseite verlinkt jeweils die aktuelle Datei); diese Daten sind der Stand vom 19.10.2026.']
    return eintrag('lunch', d, karte, offen)


# ------------------------------------------------------------------ Bankett
def bankett():
    d = 'Bankettmenuvorschlage.pdf'
    zeilen = [(nr, z.strip()) for nr, seite in enumerate(seiten(d), 1) for z in seite.splitlines() if z.strip()]
    posten, g, schluss = [], None, []
    for nr, s in zeilen:
        if s == 'Bankettmenü':
            continue                                            # Titel der Karte (Deckblatt)
        if re.match(r'^(FRÜHLING|SOMMER|HERBST|WINTER)\s+\(\d+ CHF\)$', s):
            posten.append({'t': 'rubrik', 'titel': eng(s), 's': nr}); g = None; continue
        if s.startswith('Aus den Menüs') or schluss:
            schluss.append(s); continue
        m = re.match(r'^(\S.*?)\s*(?<=\s)(\d+)$', s)
        if m and m.group(1).upper() == m.group(1):
            g = {'t': 'gericht', 'name': eng(m.group(1)), 'zeilen': [], 'preise': [m.group(2)], 's': nr}; posten.append(g); continue
        if g is None:
            raise SystemExit('Bankett: Zeile ohne Gericht: ' + s)
        g['zeilen'].append({'text': s})
    posten.append({'t': 'notiz', 'text': eng(' '.join(schluss)), 's': 2})
    karte = {'ziel': 'bankett', 'name': 'Bankettmenü', 'gruppe': 'Banketts & Gruppen', 'format': A4, 'kl': '', 'fuss': '',
             'teile': [{'art': 'deckel', 'titel': 'Bankettmenü', 'unter': '', 'zeilen': [], 'aus_original': True}, {'art': 'inhalt', 'posten': posten}]}
    offen = ['Stand: PDF erstellt 29.04.2025; ob Gerichte und Preise noch gelten, sagt das Haus nicht (auch beim Baumeister offen).',
             'Ein Wintermenü hat das Original nicht.',
             'Die Preise der Gerichte nennen keine Währung; die Menüpreise stehen als «(175 CHF)» im Titel.']
    return eintrag('bankett', d, karte, offen)


# ------------------------------------------------------------------ 4-Hands-Lunch
def vier_haende():
    d = '4_Hands-_Stier.pdf'
    zeilen = [z.strip() for z in text(d).splitlines() if z.strip()]
    posten, block = [{'t': 'rubrik', 'titel': zeilen[0], 's': 1}], []

    def ab():
        if not block:
            return
        if len(block) > 1 and any(' – ' in b for b in block[1:]):
            posten.append({'t': 'gericht', 'name': block[0], 'zeilen': [{'text': b} for b in block[1:]], 's': 1})
        else:
            posten.extend({'t': 'gericht', 'name': b, 's': 1} for b in block)
        block.clear()
    for s in zeilen[1:]:
        if s == '***':
            ab(); posten.append({'t': 'frei', 'zeilen': [{'text': '***'}], 's': 1}); continue
        if s.startswith('170.-'):
            ab(); posten.append({'t': 'notiz', 'text': s, 's': 1}); continue
        block.append(s)
    ab()
    karte = {'ziel': 'vier-haende', 'name': '4-Hands-Lunch mit Patrick Stier', 'gruppe': 'Events', 'format': A4Q, 'kl': '', 'fuss': '',
             'teile': [{'art': 'inhalt', 'posten': posten}]}
    offen = ['Vorbei: Anlass am 22.02.2026, 12 Uhr (Seite /events-2-1/event-two-yf5k9). Die Karte steht nur noch als Beleg; ob sie auf La Carte gehört, entscheidet das Haus.',
             'Die Seite des Anlasses nennt ein «6-Gang-Menü», die PDF zählt neun durch *** getrennte Gänge; so übernommen, wie es die PDF schreibt.']
    return eintrag('vier-haende', d, karte, offen, ('2026-02-22', '2026-02-22'))


# ------------------------------------------------------------------ Weinkarte
HAUPT = ('CHAMPAGNER/SCHAUMWEIN', 'WEISSWEIN', 'ROSÉ WEINE', 'ROTWEIN', 'SÜSSWEINE')
LAND = ('SCHWEIZ', 'DEUTSCHLAND', 'ÖSTERREICH', 'ITALIEN', 'SPANIEN', 'PORTUGAL', 'FRANKREICH')
FLASCHE = r'\d[.,]\d{1,3}l'


def weinkarte():
    d = '20261014_Weinkarte.pdf'
    posten, wein, offen_zeilen = [], None, []
    FUSS = ('Alle Preise in Schweizer Franken inkl. 8,1% M wSt.', 'Alle Weine enthalten Sulfite')
    for nr, seite in enumerate(seiten(d), 1):
        for z in seite.splitlines():
            z = hoch(z)
            s = z.strip()
            if not s or s in FUSS or re.match(r'^– ?\d+ ?–$', s):
                continue
            if nr == 1 and s.startswith('CHAMPAGNER/SCHAUMWEIN'):
                s = 'CHAMPAGNER/SCHAUMWEIN'                     # dahinter ein unsichtbares «A» in Weiss (im Bild geprüft), nicht Teil der Karte
            e = eng(s)
            # 1 · Wein: [Jahr] Name [Zusatz] Flasche Preis
            m = re.match(rf'^(?:(\d{{4}})\s+)?(\S.*?)\s{{2,}}(?:(\S+)\s+)?({FLASCHE})\s+(\d+)$', s)
            if m and not m.group(2).isupper():
                name = m.group(2).strip()
                zusatz = m.group(3)
                wein = {'t': 'gericht', 'name': name, 'preise': [m.group(5)], 'einheiten': [m.group(4)], 's': nr}
                if m.group(1):
                    wein['jahr'] = m.group(1)
                if zusatz:
                    wein['zusatz'] = zusatz
                posten.append(wein); continue
            m = re.match(rf'^(?:(\d{{4}})\s+)?(\S.*?)\s+({FLASCHE})\s+(\d+)$', s)   # enger Satz (eine Lücke)
            if m and len(z) - len(z.lstrip()) < 40:
                wein = {'t': 'gericht', 'name': m.group(2).strip(), 'preise': [m.group(4)], 'einheiten': [m.group(3)], 's': nr}
                if m.group(1):
                    wein['jahr'] = m.group(1)
                posten.append(wein); continue
            # 2 · weitere Flasche desselben Weins: nur Flasche Preis
            m = re.match(rf'^({FLASCHE})\s+(\d+)$', s)
            if m:
                if wein is None:
                    raise SystemExit(f'Weinkarte S. {nr}: Flasche ohne Wein: {s}')
                wein['einheiten'].append(m.group(1)); wein['preise'].append(m.group(2)); continue
            # 3 · Überschriften in Versalien
            if e.upper() == e and re.search(r'[A-ZÄÖÜ]{3}', e):
                if any(e.startswith(h) for h in HAUPT):
                    posten.append({'t': 'rubrik', 'titel': e, 's': nr})
                elif any(e.startswith(l) for l in LAND):
                    posten.append({'t': 'land', 'text': e, 's': nr})
                else:
                    posten.append({'t': 'zw', 'text': e, 's': nr})
                wein = None; continue
            einzug = len(z) - len(z.lstrip())
            # 4 · Erläuterung unter einem Wein (eingerückt, ohne Preis)
            if einzug >= 5 and wein is not None and not re.match(r'^[A-ZÄÖÜ][a-zäöü]+$', e):
                wein.setdefault('zeilen', []).append({'text': e}); continue
            # 5 · Land in gemischter Schreibweise (Diverse Schaumweine: «Schweiz», «Deutschland» …)
            if einzug >= 5:
                posten.append({'t': 'zw', 'text': e, 's': nr}); wein = None; continue
            # 6 · Weingut / Erzeuger am linken Rand
            if einzug == 0:
                posten.append({'t': 'zw', 'text': e, 'weingut': True, 's': nr}); wein = None; continue
            offen_zeilen.append(f'S. {nr}: {s}')
    if offen_zeilen:
        raise SystemExit('Weinkarte: nicht zuzuordnen:\n' + '\n'.join(offen_zeilen))
    karte = {'ziel': 'weinkarte', 'name': 'Weinkarte', 'gruppe': 'Restaurant', 'format': A4, 'kl': 'wein',
             'fuss': 'Alle Preise in Schweizer Franken inkl. 8,1% M wSt. · Alle Weine enthalten Sulfite',
             'teile': [{'art': 'deckel', 'titel': 'Weinkarte', 'unter': '', 'zeilen': []}, {'art': 'inhalt', 'posten': posten}]}
    offen = ['Stand: Datei «20261014_Weinkarte» (PDF erstellt 14.10.2026); die Karte nennt kein Datum.',
             'Offenausschank (Weine im Glas) hat die Weinkarte nicht; eine Getränke- oder Barkarte mit Bier, Aperitifs, Spirituosen und Kaffee ist online nicht zu finden.',
             '«M wSt.» schreibt das Haus so in jeder Fusszeile (im Bild geprüft); nicht berichtigt.',
             'Seitenzahlen des Originals beginnen mit «– 2 –» auf Seite 1; ein Deckblatt fehlt in der PDF.',
             'Weingut-Zeilen tragen das Feld «weingut»: true (Zwischentitel der Art «zw»), das Datenmodell von La Carte kennt keine eigene Art für den Erzeuger.',
             'Jahrgang steht im eigenen Feld «jahr», die Flaschengrösse in «einheiten» neben dem Preis.']
    return eintrag('weinkarte', d, karte, offen)


KARTEN = [speisekarte, lunch, laestermeile, weinkarte, bankett, vier_haende]

if __name__ == '__main__':
    STAND.mkdir(exist_ok=True)
    alle = []
    for f in KARTEN:
        e = f()
        fehler = M.pruefe_karte(e['karte'])
        if fehler:
            raise SystemExit(f'{e["id"]}: {fehler}')
        (STAND / f'{e["id"]}.json').write_text(json.dumps(e, ensure_ascii=False, indent=1) + '\n')
        n = sum(1 for t in e['karte']['teile'] if t['art'] == 'inhalt' for p in t['posten'] if p['t'] == 'gericht')
        print(f'{e["id"]:14} {n:4} Einträge')
        alle.append(e)
    doc = {'schema': M.SCHEMA, 'haus': 'schloessli', 'karten': alle}
    f = M.pruefe(doc, 'schloessli')
    if f:
        raise SystemExit('Dokument: ' + f)
    (HIER / 'haus.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n')
    print('haus.json geprüft mit modell.pruefe: in Ordnung')
