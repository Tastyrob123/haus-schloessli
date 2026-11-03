"""Antworten ohne KI statt Claude (Robert 16.10.2026: «lokal bis zur Kostenrunde», keine bezahlten KI-Aufrufe in Prüfläufen).

Im Schlössli ist das der Standard: python3 _werkzeuge/reception/server.py 9284 (ohne RECEPTION_KI=1). Aufbau aus dem Stamm der Werkzeuge (Nachtbau 3.11.2026).
Dann ruft kein Teil des Reservationsbuchs und vom Chat die KI auf und kein Schlüssel wird gelesen. Jede Stelle, die sonst Claude fragt, bekommt
eine Antwort in genau der Form, die Claude liefern würde:
  Chat (gast.frage)        Antwort aus den belegten Zeilen von steckbrief.json («Das weiss der Chat») und den Nachträgen des Teams, Sie-Form;
                           nennt der Gast eine E-Mail oder Telefonnummer, ruft sie das Werkzeug «anfrage» auf (so entsteht wie echt eine Anfrage im Eingang);
                           fragt er nach einem Tisch, zeigt sie den Weg zur Reservation (Werkzeug «buchungsmaske»); ohne Beleg meldet sie «nicht belegt».
  Brief (gast.anfrage)     «Betreff: …», Brief mit Anrede, offenen Stellen [in Klammern] und Gruss, darunter «---» mit Punkten fürs Team.
  Übersetzen               JSON mit betreff, text und verlauf in gleicher Länge (Wortlaut unverändert).
  Wissen einlesen          Werkzeug «eintraege» mit einem Eintrag je Material.
"""
import json, os, re

BEREICH = 'Das Haus'
HIER = os.path.dirname(os.path.abspath(__file__))
NICHTS = 'Dazu steht nichts in meinen Unterlagen. Ich gebe Ihre Frage gerne ans Team weiter; direkt erreichen Sie es unter +41 71 688 90 92.'

# Wörter der Gäste → Stichwörter der Zeilen (erste passende Gruppe zählt doppelt)
THEMEN = [
    (r'ferien|geschlossen|silvester|neujahr|november|dezember|januar|februar|weihnacht|kreuzfahrt|excellence|closed|holiday', ('Ferien', 'Excellence Gourmetkreuzfahrt', 'Restaurant geschlossen')),
    (r'dienstag|mittwoch|ruhetag|offen|geöffnet|öffnung|uhr|zeiten|open', ('Restaurant', 'Ruhetage', 'Küche à la carte', 'Lästermeile')),
    (r'küche|essen bis|warm', ('Küche à la carte',)),
    (r'lunch|mittag', ('Lunch-Menü', 'Die Gänge')),
    (r'läster|bar\b|tapas|apéro|apero', ('Lästermeile', 'Tapas', 'Prato', 'Tarte flambée')),
    (r'wein|wine|sommelier|champagner|flasche', ('Weinkarte', 'Sommelier', 'Gruppen')),
    (r'bankett|feier|geburtstag|hochzeit|firmen|gruppe|etage|personen|tavolata|party|birthday|wedding|group', ('Plätze', 'Speisenform', 'Besprechen', 'Auswahl')),
    (r'bankettmen|menü|menu|frühling|sommer|herbst', ('Frühling', 'Sommer', 'Herbst', 'Auswahl')),
    (r'gutschein|geschenk|schenken|voucher|gift', ('Wofür', 'Angaben', 'Bestätigung')),
    (r'hund|dog|chien', ('Hunde',)),
    (r'park|auto|anfahrt|anreise|zug|bahn|parking|train', ('Mit dem Auto', 'Parkplatz und Zug')),
    (r'schiff|boot|hafen|see\b|wasser|boat', ('Am Hafen', 'Lage')),
    (r'terrasse|draussen|platane|terrace|outside', ('Terrasse', 'Lage')),
    (r'vegetar|vegan|allerg|gluten|laktose|nuss|nüss|unverträg', ('Vegetarisch', 'Allergene')),
    (r'karte|gericht|speise|tortelloni', ('Aufbau', 'Tortelloni', 'Preise')),
    (r'adresse|wo\b|telefon|mail|kontakt|instagram|address|phone', ('Adresse', 'Telefon und E-Mail', 'Instagram')),
    (r'zahl|karte zahlen|twint|bar zahlen|kredit|debit|pay', ('Zahlung',)),
    (r'team|koch|köchin|chef|gastgeber|wer\b|moni|jonas', ('Küchenchefin', 'Gastgeber und Sommelier', 'Sous-Chef', 'Pächter')),
    (r'punkte|gault|michelin|falstaff|auszeichn', ('GaultMillau', 'Entdeckung des Jahres', 'Falstaff', 'Guide Michelin')),
    (r'geschichte|früher|alt\b|schlössli heisst|besen|history', ('1676', 'Der Besen', 'Heute')),
    (r'anzahlung|storn|agb|teilnehmer', ('Teilnehmerzahl', 'Anzahlung', 'Gruppen')),
]
EINSTIEG = {'Restaurant': 'Geöffnet ist Donnerstag bis Montag, Dienstag und Mittwoch ist Ruhetag.', 'Ferien': 'Das Restaurant macht zweimal Ferien.',
            'Lunch-Menü': 'Mittags gibt es das Lunch-Menü mit drei Gängen.', 'Plätze': 'Für Banketts hat das Haus zwei Etagen, jede für bis zu 26 Personen.',
            'Wofür': 'Gutscheine gibt es über die Seite «Gutschein» der Website.', 'Hunde': 'Hunde sind willkommen.',
            'Mit dem Auto': 'Das Haus hat einen eigenen Parkplatz, der Bahnhof Bottighofen liegt in der Nähe.', 'Weinkarte': 'Die Weinkarte stellt Jonas Volpert zusammen.',
            'Vegetarisch': 'Die Karte weist Vegetarisches und die Allergene mit Kürzeln aus; die Küche stimmt alles Weitere mit Ihnen ab.',
            'Lästermeile': 'An der Lästermeile gibt es die Karte den ganzen Tag.', 'Adresse': 'Sie finden uns direkt im Hafen von Bottighofen.'}


def _zeilen():
    try:
        sb = json.load(open(os.path.join(HIER, 'steckbrief.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return []
    return [{'was': z['was'], 'angabe': z['angabe'], 'bereich': b['bereich']} for b in sb['bereiche'] for g in b['gruppen'] for z in g['zeilen']]


def _nachgetragen(frage):
    try:
        import reception
        l = [x for x in reception.nachgetragen() if (x.get('antwort') or '').strip() and not x.get('beispiel')]
    except Exception:  # noqa: BLE001
        return None
    w = set(re.findall(r'\w{4,}', frage.lower()))
    best = max(l, key=lambda x: len(w & set(re.findall(r'\w{4,}', x['frage'].lower()))), default=None)
    if best and len(w & set(re.findall(r'\w{4,}', best['frage'].lower()))) >= 2:
        return best['antwort']
    return None


def _beleg(frage):
    """Antwort aus den belegten Zeilen: ein Satz, darunter höchstens vier Punkte «Stichwort: Angabe». None, wenn nichts passt."""
    nt = _nachgetragen(frage)
    if nt:
        return {'text': nt, 'belegt': True}
    zl = {z['was']: z for z in _zeilen()}
    wahl = []
    treffer = 0
    for muster, was in THEMEN:   # höchstens die zwei ersten passenden Themen: nichts Ungefragtes
        if treffer < 2 and re.search(muster, frage, re.I):
            treffer += 1
            wahl += [w for w in was if w in zl and w not in wahl]
    if not wahl:
        return None
    satz = next((EINSTIEG[w] for w in wahl if w in EINSTIEG), 'Das steht in unseren Unterlagen:')
    punkte = '\n'.join(f"- {zl[w]['was']}: {zl[w]['angabe']}" for w in wahl[:4])
    return {'text': satz + '\n' + punkte, 'belegt': True}


def _text(koerper):
    """Alles, was der Aufruf an Text mitschickt (System und Nachrichten), für die Erkennung der Stelle."""
    s = koerper.get('system')
    sys_t = s if isinstance(s, str) else ' '.join(b.get('text', '') for b in (s or []) if isinstance(b, dict))
    msg = []
    for m in koerper.get('messages') or []:
        c = m.get('content')
        if isinstance(c, str):
            msg.append(c)
        else:
            msg += [b.get('text', '') for b in c or [] if isinstance(b, dict) and b.get('type') == 'text']
    return sys_t, msg


def _antwort(text='', werkzeug=None):
    inhalt = [{'type': 'text', 'text': text}] if text else []
    if werkzeug:
        inhalt.append({'type': 'tool_use', 'id': 'toolu_probe', 'name': werkzeug[0], 'input': werkzeug[1]})
    return {'content': inhalt, 'stop_reason': 'tool_use' if werkzeug else 'end_turn', 'usage': {'input_tokens': 0, 'output_tokens': 0}}


def _brief(letzte):
    name = (re.search(r'Name:\s*(.+)', letzte) or re.search(r'"name":\s*"([^"]+)"', letzte))
    wer = name.group(1).strip() if name else ''
    art = (re.search(r'Art:\s*(.+)', letzte) or [None, ''])[1].strip()
    datum = (re.search(r'Datum:\s*(.+)', letzte) or [None, ''])[1].strip()
    pers = (re.search(r'Personen:\s*(.+)', letzte) or [None, ''])[1].strip()
    hinw = (re.search(r'Hinweise:\s*(.+)', letzte) or [None, ''])[1].strip()
    allerg = (re.search(r'Allergien \(Formular\):\s*(.+)', letzte) or [None, ''])[1].strip()
    anl = (re.search(r'Anliegen:\s*(.+)', letzte) or [None, ''])[1].strip()
    if not allerg or allerg == 'keine angegeben':
        gast = letzte.split('VORLAGE DES HAUSES', 1)[0].split('GESPRÄCH IM CHAT:', 1)[-1] + ' ' + anl
        gast = re.sub(r'Wünsche, Allergien\s*:|Gericht, Allergien\s*:|Allergien \(Formular\):[^\n]*|Allergien\s*:', ' ', gast)
        m = re.findall(r'(\w*allergi\w*|\w*unverträglich\w*|gluten\w*|laktose\w*|nüsse|nuss\w*|vegan\w*|vegetar\w*|kein\w* fleisch)', gast, re.I)
        allerg = ', '.join(dict.fromkeys(m)) if m else ''
    nachname = wer.split()[-1] if wer else ''
    anrede = f'Guten Tag {wer}' if wer else 'Guten Tag'
    wann = datum if datum and datum != 'nicht genannt' else ''
    teil_al = (f'Ihre Angaben für die Küche ({allerg}) geben wir an Monika Huber und ihr Team weiter, damit sie bei jedem Gang berücksichtigt werden [Küche informieren].\n\n'
               if allerg else '')
    teil_ruhe = ''
    if 'Ruhetag' in hinw:
        teil_ruhe = 'Am gewünschten Tag haben wir Ruhetag; Donnerstag bis Montag sind wir gerne für Sie da. Passt Ihnen ein anderer Tag?\n\n'
    elif 'Ferien' in hinw:
        teil_ruhe = 'In dieser Zeit sind wir in den Ferien. Gerne finden wir mit Ihnen einen anderen Tag.\n\n'
    if art == 'Anlass' and re.search(r'kreuzfahrt|excellence', anl + ' ' + letzte, re.I):
        betreff = 'Ihre Plätze für die Excellence Gourmetkreuzfahrt'
        kern = ('herzlichen Dank für Ihr Interesse. Wir freuen uns, dass Sie mit uns an Bord gehen möchten.\n\n'
                'Vom 13. bis 15. November 2026 kocht Monika Huber gemeinsam mit Dieter Koschina auf der Excellence Countess, mit Start am Freitag in Basel und über Nacht nach Strassburg. '
                'Die Plätze und Kabinen bucht man direkt bei Excellence, beim Gourmetfestival Dieter Koschina & Monika Huber auf excellence.ch [Link mitschicken].\n\n'
                + teil_al +
                'Unser Restaurant ist über diese drei Tage geschlossen, da das ganze Team mit an Bord ist. Ab Donnerstag, 19. November sind wir wieder am Hafen für Sie da.')
        grundlage = 'Events & Termine (Website), Excellence Gourmetkreuzfahrt'
        offen = 'Link zur Buchung mitschicken'
    elif art in ('Bankett', 'Anlass'):
        betreff = 'Ihre Feier in der Wirtschaft am Schlössli' + (f', {wann}' if wann else '')
        kern = ('herzlichen Dank für Ihre Anfrage. Wir freuen uns, dass Sie Ihre Feier bei uns am Hafen planen.\n\n'
                + teil_ruhe +
                'Für Banketts haben wir zwei Etagen mit Platz für jeweils bis zu 26 Personen. Sie geben den Rahmen vor, ob Tavolata oder gesetztes Menue; '
                'aus unseren Bankettmenüs Frühling, Sommer und Herbst stellen Sie drei bis fünf Gerichte zusammen [Verfügbarkeit prüfen].' + (' [Etagen klären]' if 'Etage' in hinw else '') + '\n\n'
                + teil_al +
                'Damit wir alles in Ruhe vorbereiten können, bräuchten wir noch:\n- Uhrzeit\n- gewünschte Speisenform (Tavolata oder gesetztes Menue)\n- Anzahl Gänge\n- Richt-Budget für Speisen bzw. insgesamt\n\n'
                'Gerne besprechen wir alles auch vor Ort in Ruhe.')
        grundlage = 'Banketts & Gruppen, Bankettmenüs (Website), Bankettanfrage des Hauses'
        offen = 'Verfügbarkeit der Etage, Speisenform, Budget'
    elif art == 'Gutschein':
        betreff = 'Ihr Gutschein der Wirtschaft am Schlössli'
        kern = ('herzlichen Dank für Ihre Bestellung. Wir freuen uns, dass Sie jemandem einen Besuch bei uns am Hafen schenken.\n\n'
                'Den Gutschein stellen wir über den gewünschten Betrag aus [Betrag bestätigen]. Wir senden Ihnen eine Bestätigung, sobald der Gutschein versendet wurde.')
        grundlage = 'Gutschein (Website)'
        offen = 'Betrag, Versand'
    else:
        betreff = 'Ihre Reservation in der Wirtschaft am Schlössli' + (f', {wann}' if wann else '')
        kern = ('herzlichen Dank für Ihre Anfrage. Wir freuen uns auf Ihren Besuch bei uns direkt im Hafen.\n\n'
                + teil_ruhe +
                (f'Für {pers} Personen ' if pers and pers != 'nicht genannt' else 'Für Sie ') + 'halten wir gerne einen Tisch bereit [Tisch bestätigen].'
                + (' Den Wunsch nach einem Platz auf der Terrasse nehmen wir gerne auf; draussen sitzen Sie im Schatten der Platanen mit Blick auf den See [Terrasse je nach Wetter].' if re.search(r'terrasse|draussen|see', anl, re.I) else '')
                + (' Ihr Hund ist bei uns willkommen.' if re.search(r'hund', anl, re.I) else '') + '\n\n'
                + teil_al +
                'Die Küche ist von 11:30 bis 13:30 und von 18:00 bis 20:00 Uhr für Sie da, die Karte der Lästermeile den ganzen Tag.')
        grundlage = 'Öffnungszeiten, Speisekarte (Website)'
        offen = 'Tisch bestätigen'
    gruss = f'Guten Tag {wer}' if wer else 'Guten Tag'
    del anrede, nachname
    return (f'Betreff: {betreff}\n\n{gruss}\n\n{kern}\n\nMit freundlichen Grüssen\n\n[Name]\nWirtschaft am Schlössli'
            f'\n---\nGrundlage: {grundlage}\nOffen: {offen}')


def api(koerper):
    sys_t, msg = _text(koerper)
    werkzeuge = [w.get('name') for w in koerper.get('tools') or []]
    letzte = msg[-1] if msg else ''
    if 'eintraege' in werkzeuge:                                    # Wissen einlesen (gedaechtnis._auszug)
        m = re.search(r'BEREICH DES TEAMS: (.+)', letzte)
        bereich = (m.group(1).strip() if m else '') or BEREICH
        roh = ' '.join(msg)
        stueck = re.sub(r'\s+', ' ', roh.split('TEXT DES TEAMS:', 1)[-1] if 'TEXT DES TEAMS:' in roh else roh)[-220:].strip()
        return _antwort(werkzeug=('eintraege', {'grund': 'Aus dem Dokument übernommen', 'eintraege': [
            {'bereich': bereich, 'titel': (' '.join(stueck.split()[:6]) or 'Neuer Eintrag'), 'text': stueck, 'gueltig_bis': None}]}))
    if sys_t.startswith('Du übersetzt'):                             # reception.uebersetzen
        try:
            d = json.loads(letzte)
        except ValueError:
            d = {}
        return _antwort(json.dumps({'betreff': str(d.get('betreff', '')), 'text': str(d.get('text', '')),
                                    'verlauf': [str(v) for v in d.get('verlauf') or []]}, ensure_ascii=False))
    if 'ANFRAGE:' in letzte:                                         # gast.anfrage (Brief)
        return _antwort(_brief(letzte))
    # Chat (gast.frage, auch der zweite Schritt nach der Buchungsmaske)
    if any(isinstance(m.get('content'), list) and any(b.get('type') == 'tool_result' for b in m['content']) for m in koerper.get('messages') or []):
        return _antwort('OK')
    frage = letzte.strip()
    kontakt = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+|(?:\+|00)\d[\d\s]{7,}\d', frage)
    if kontakt and 'anfrage' in werkzeuge:
        name = re.search(r'(?:ich bin|mein name ist|name:|my name is|je suis)\s+([A-ZÄÖÜ][\w-]+(?:\s+[A-ZÄÖÜ][\w-]+)?)', frage, re.I)
        pers = re.search(r'(\d{1,3})\s*(?:personen|gäste|persons|people|personnes)', frage, re.I)
        art = ('bankett' if re.search(r'bankett|feier|fest\b|geburtstag|hochzeit|party|birthday|wedding|firmen|gruppe', frage, re.I)
               else 'gutschein' if re.search(r'gutschein|voucher', frage, re.I) else 'tisch')
        return _antwort('Danke, Ihre Anfrage liegt jetzt beim Team. Es meldet sich persönlich bei Ihnen.',
                        ('anfrage', {'art': art, 'name': name.group(1) if name else 'Gast', 'kontakt': kontakt.group(0), 'datum': None,
                                     'personen': int(pers.group(1)) if pers else None, 'anliegen': frage[:300]}))
    if 'buchungsmaske' in werkzeuge and re.search(r'reserv|tisch\b|platz (frei|für)|freie tische|book|table', frage, re.I):   # wie echt: der Weg zur Reservation unter der Antwort
        b = _beleg(frage)
        return _antwort('Gerne. Die Reservation online zeigt die freien Tische.' + ('\n' + b['text'].split('\n', 1)[1] if b and '\n' in b['text'] else ''),
                        ('buchungsmaske', {'datum': None, 'uhrzeit': None, 'personen': None}))
    b = _beleg(frage)
    if b and b.get('belegt'):
        return _antwort(b['text'])
    return _antwort(NICHTS, ('nicht_belegt', {'thema': frage[:80]}))
