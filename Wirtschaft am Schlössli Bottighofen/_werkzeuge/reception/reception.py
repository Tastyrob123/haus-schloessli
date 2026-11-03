"""Das Reservationsbuch (La Réception) · Wirtschaft am Schlössli, Bottighofen (Nachtbau 3.11.2026: Aufbau aus dem Gästebuch des Culinarium Hannover,
Inhalt aus dem Reservationsbuch des Schlössli vom 19.10.2026). Ein Restaurant direkt im Hafen am Bodensee, ohne Zimmer.
Zwei Dinge kommen herein:
  Eingang      Die Formulare der Website (Reservation mit Wünschen und Allergien, Bankettanfrage, Gutschein, Plätze für einen Anlass, «Ihr Abend»)
               und Anfragen aus dem Chat, sobald ein Gast Name und Kontakt nennt. Das Team bekommt dazu einen Antwortentwurf im Ton des Hauses,
               auf Grundlage der Fragen, die das Haus in seinen eigenen Mail-Links stellt (vorlagen/), ändert ihn und schickt ihn selbst.
               Hier wird nichts verschickt. Zu jeder Anfrage stehen Hinweise dabei: Ruhetag, Ferien, mehr Personen als eine Etage fasst, Allergien.
  Gefragt      Jede Frage mit Antwort. Wo der Chat keine Antwort hatte (Werkzeug «nicht_belegt»), trägt das Team sie einmal nach;
               ab dann antwortet der Chat damit (Block «NACHGETRAGEN VOM TEAM» in der Anweisung).

Speicher: Dateien unter daten/ (oder RECEPTION_DATEN), im selben Aufbau wie der Online-Speicher beim Carlton (Vercel Blob, _gast/fragen.js):
  fragen/JJJJ-MM-TT/<zeit>-<zufall>.json · anfragen/JJJJ-MM-TT/<zeit>-<zufall>.json · nachgetragen.json · status.json
Einträge älter als zwölf Monate werden gelöscht (Datenschutzerklärung).

Eingebunden von server.py: reception.einbinden(gast_modul) hängt sich an gast/gast.py, ohne die Datei zu ändern."""
import datetime, glob, hashlib, html, json, os, random, re, shutil, threading, time
try:   # «Das weiss der Chat» (16.10.2026, nur lokal): Berichtigungen und Ergänzungen des Teams am Wissen. Online fehlt die Datei: dann wie bisher.
    import gedaechtnis
except ImportError:
    gedaechtnis = None

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website')   # die Website des Schlössli (nur gelesen)
DATEN = os.environ.get('RECEPTION_DATEN') or os.environ.get('REZEPTION_DATEN') or os.path.join(HIER, 'daten')
def _name(teil='gaeste', standard='Das Reservationsbuch'):
    """Name eines Werkzeugs aus der einen Stelle (_werkzeuge/oberflaeche/kleid/schloessli.js › namen), nie fest im Code (Robert wählt, das Hafenbüro trägt ein)."""
    try:
        s = open(os.path.join(os.path.dirname(HIER), 'oberflaeche', 'kleid', 'schloessli.js'), encoding='utf-8').read()
        m = re.search(r"namen:\s*\{([^}]*)\}", s)
        n = re.search(teil + r":\s*'([^']+)'", m.group(1)) if m else None
        return n.group(1) if n else standard
    except OSError:
        return standard


NAME = _name()
NAME_IM = ('im ' + NAME[4:]) if NAME.startswith('Das ') else ('in der ' + NAME[4:]) if NAME.startswith('Die ') else ('im ' + NAME[4:]) if NAME.startswith('Der ') else ('in ' + NAME)   # «im Reservationsbuch»

SCHLOSS = threading.Lock()
LOKAL = threading.local()
ARTEN = {'tisch': 'Reservation', 'bankett': 'Bankett', 'anlass': 'Anlass', 'gutschein': 'Gutschein', 'nachricht': 'Nachricht'}   # Restaurant ohne Zimmer (19.10.2026)
# Das Schlössli hat eine Adresse für alles (kontakt@, jede Seite, auch Bankett- und Event-Links) und keine eigenen Mail-Vorlagen. Grundlage für den Brief
# sind die Fragen, die das Haus in seinen Mail-Links selbst stellt (vorlagen/bankett.txt aus «Bankettanfrage», vorlagen/anlass.txt aus «Reservation» eines
# Events, vorlagen/gutschein.txt aus dem Gutschein-Formular); für Reservation und Nachricht gibt es keine, dann gilt nur der Ton des Markenbuchs.
MAIL = 'kontakt@schloessli-bottighofen.ch'
VORLAGE = {'tisch': ('', MAIL), 'bankett': ('bankett', MAIL), 'anlass': ('anlass', MAIL), 'gutschein': ('gutschein', MAIL), 'nachricht': ('', MAIL)}
VORLAGEN_DATEIEN = ('bankett.txt', 'anlass.txt', 'gutschein.txt')
# Eine Anfrage von der Website antwortet von der Adresse, an die sie ging (Feld «an»); erlaubt ist nur die Adresse des Hauses.
# Die «Abteilung» ist im Schlössli die Art der Arbeit (wer sich darum kümmert), nicht eine Mail-Adresse.
ABTEILUNG_VON = {MAIL: 'Restaurant'}
ART_ABTEILUNG = {'tisch': 'Reservation', 'nachricht': 'Reservation', 'bankett': 'Bankett', 'anlass': 'Bankett', 'gutschein': 'Gutschein'}
FORMULARE = ('reservation', 'bankett', 'gutschein', 'plaetze', 'abend', 'allgemein')
# Allergene: Kürzel der Karten des Hauses (Lästermeile, Speisekarte Oktober: G, L, E, F, S, So, En, N, Se; VEG), so auch im Reservationsfenster der Website
ALLERGENE = {'G': 'Gluten', 'L': 'Laktose', 'E': 'Eier', 'F': 'Fische', 'S': 'Schalen- und Weichtiere', 'So': 'Soja', 'En': 'Erdnüsse', 'N': 'Nüsse', 'Se': 'Sellerie', 'VEG': 'vegetarisch'}
# Öffnungstage und Ferien (Kontaktseite des Hauses, abgerufen 19.10.2026) und Plätze (Seite «Karten»: «auf zwei Etagen Platz für jeweils bis zu 26 Personen»)
RUHETAGE = (1, 2)   # Dienstag, Mittwoch (Montag = 0)
FERIEN = (('2026-11-13', '2026-11-15', 'Ferien: Excellence Gourmetkreuzfahrt, das Team ist an Bord'), ('2026-12-22', '2027-02-10', 'Ferien bis 10. Februar 2027'))
ETAGE = 26
SPRACHEN = ('de', 'en', 'fr')
# Themen für «Das wurde gefragt»: Wortlisten in den Sprachen der Gäste, erste passende gewinnt
THEMEN = [('Allergien & Unverträglichkeiten', r'allerg|gluten|laktose|lactose|zöliak|unverträg|nuss|nüss|erdnuss|sellerie|soja|vegan|vegetar|végétar|intoler|nut\b|nuts|dairy|celiac|sans gluten'),
          ('Bankette & Gruppen', r'bankett|feier|fest\b|geburtstag|hochzeit|jubil|firmen|gruppe|etage|tavolata|gesetzt|apéro|apero|party|birthday|wedding|group|anniversaire|mariage|fête|groupe'),
          ('Anlässe & Events', r'anlass|event|4.hands|four.hands|stier|kreuzfahrt|excellence|seenacht|feuerwerk|ehemalig|kitchen party|lunch mit|veranstalt'),
          ('Gutscheine', r'gutschein|geschenk|schenken|voucher|gift|cadeau|bon\b'),
          ('Hund', r'hund|dog|chien|haustier'),
          ('Reservation & Zeiten', r'reserv|tisch|platz frei|frei\b|ruhetag|offen|geöffnet|öffnung|ferien|dienstag|mittwoch|uhr\b|küche|book|table|open|closed|réserv|ouvert|fermé|storn|annul|cancel'),
          ('Lästermeile', r'läster|laester|bar\b|tapas|lästerschirm|drink|cocktail|aperitif'),
          ('Karte & Wein', r'karte|menü|menu|lunch|mittag|abend|gericht|tortelloni|fisch|fleisch|dessert|wein|wine|vin\b|sommelier|flasche|korkgeld|essen|dinner|plat|carte'),
          ('Terrasse & Hafen', r'terrasse|draussen|aussen|see\b|hafen|blick|sonne|schirm|terrace|lake|harbour|harbor|lac\b|port\b'),
          ('Anreise & Parkplatz', r'park|anreise|anfahrt|bahnhof|zug|bus\b|auto|schiff|velo|parking|train|station|arriv|venir|gare'),
          ('Stellen', r'job|stelle|arbeit|lehre|bewerb|emploi|career|work')]
ABDECKEN = [(re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'), '[E-Mail]'), (re.compile(r'(?:\+|00)?\d[\d\s/().-]{7,}\d'), '[Nummer]')]


# ---------------------------------------------------------------- Dateien
def _pfad(*t):
    return os.path.join(DATEN, *t)

def _lies(p, standard):
    try:
        return json.load(open(p, encoding='utf-8'))
    except OSError:
        return standard
    except ValueError:              # beschädigt: die letzte gute Fassung nehmen
        try:
            return json.load(open(p + '.gut', encoding='utf-8'))
        except (OSError, ValueError):
            return standard

def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.neu'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    try:
        json.load(open(p, encoding='utf-8')); shutil.copy2(p, p + '.gut')   # nur eine lesbare Fassung wird zur Sicherung
    except (OSError, ValueError):
        pass
    os.replace(tmp, p)

def _neue_id(art):
    jetzt = datetime.datetime.now().astimezone()
    zeit = jetzt.isoformat(timespec='seconds')
    return zeit, f'{art}/{zeit[:10]}/{zeit.replace(":", "-").replace("+", "_")}-{random.randrange(36**6):06x}.json'

def _gueltig(id_, art):
    return bool(re.fullmatch(art + r'/\d{4}-\d{2}-\d{2}/[\w.-]+\.json', id_ or '')) and os.path.exists(_pfad(id_))

def _alle(art):
    l = []
    for f in sorted(glob.glob(_pfad(art, '*', '*.json')), reverse=True):
        d = _lies(f, None)
        if d:
            d['id'] = os.path.relpath(f, DATEN)
            l.append(d)
    return l

def aufraeumen():
    """Einträge älter als zwölf Monate löschen (ganze Tagesordner)."""
    grenze = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    n = 0
    for art in ('fragen', 'anfragen'):
        for o in glob.glob(_pfad(art, '*')):
            if os.path.basename(o) < grenze:
                shutil.rmtree(o, ignore_errors=True); n += 1
    return n


# ---------------------------------------------------------------- Ablegen (aus dem Chat)
def thema_von(text):
    t = (text or '').lower()
    for name, muster in THEMEN:
        if re.search(muster, t):
            return name
    return 'Weitere Fragen'

def lege_frage(daten):
    for muster, ersatz in ABDECKEN:
        daten['frage'] = muster.sub(ersatz, daten.get('frage', ''))
    zeit, id_ = _neue_id('fragen')
    e = {'zeit': zeit, 'frage': str(daten.get('frage', ''))[:600], 'antwort': str(daten.get('antwort', ''))[:2000], 'belegt': daten.get('belegt') is not False,
         'thema': str(daten.get('thema', ''))[:80], 'gruppe': thema_von(daten.get('frage', '')), 'sprache': str(daten.get('sprache', 'de'))[:2],
         'buchung': bool(daten.get('buchung')), 'mappe': bool(daten.get('mappe')), 'anfrage': daten.get('anfrage') or ''}
    if daten.get('beispiel'):
        e['beispiel'] = True; e['probe'] = True
    with SCHLOSS:
        _schreib(_pfad(id_), e)
    if random.random() < 0.05:
        aufraeumen()
    return id_

def lege_anfrage(eingabe, gespraech, sprache, verlauf):
    """Legt eine Anfrage ab. Kommt im selben Gespräch dieselbe Art noch einmal (Gast ergänzt Datum oder Personen), wird sie ergänzt, nicht verdoppelt."""
    art = eingabe.get('art') if eingabe.get('art') in ARTEN else 'nachricht'
    with SCHLOSS:
        for a in _alle('anfragen')[:80]:
            if a.get('gespraech') == gespraech and a.get('art') == art and a.get('status') != 'erledigt':
                for k in ('name', 'kontakt', 'datum', 'personen', 'anliegen'):
                    if eingabe.get(k) not in (None, ''):
                        a[k] = eingabe[k]
                a['verlauf'] = verlauf; a['entwurf'] = None; a['geaendert'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
                id_ = a.pop('id'); _schreib(_pfad(id_), a)
                return id_
        zeit, id_ = _neue_id('anfragen')
        _schreib(_pfad(id_), {'zeit': zeit, 'art': art, 'name': str(eingabe.get('name') or '')[:120], 'kontakt': str(eingabe.get('kontakt') or '')[:160],
                              'datum': str(eingabe.get('datum') or '')[:120], 'personen': eingabe.get('personen'), 'anliegen': str(eingabe.get('anliegen') or '')[:1200],
                              'sprache': sprache, 'gespraech': gespraech, 'verlauf': verlauf, 'status': 'neu', 'entwurf': None})
        return id_


# ---------------------------------------------------------------- Beispiele im Eingang
BEISPIEL_STAND = 4   # Schlössli Nachtbau 3.11.2026: eigene Beispiele des Restaurants ab Stand 4   # 3: deutsche Lesefassungen der fremdsprachigen Briefe (16.10.2026) · 1: fünf Anfragen und neun Fragen (13./14.10.2026) · 2: zwölf Anfragen, 24 Fragen, drei Antworten des Teams, Entwürfe neu geschrieben (15.10.2026)


def _jetzt():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo('Europe/Zurich'))
    except Exception:
        return datetime.datetime.now().astimezone()


def _zeit_vor(jetzt, vor):
    tage, h, m = vor
    z = (jetzt - datetime.timedelta(days=tage)).replace(hour=h, minute=m, second=0, microsecond=0)
    if z > jetzt:
        z -= datetime.timedelta(days=1)
    return z.isoformat(timespec='seconds')


def _stand(marke):
    """Welcher Beispiel-Stand liegt in diesem Datenordner: 0 = noch keiner, 1 = alte Marke ohne Stand."""
    if not os.path.exists(marke):
        return 0
    return int(_lies(marke, {}).get('stand') or 1)


def _quelle(e):
    """Kennung des Textstands, aus dem eine Lesefassung stammt: ändert das Team den Brief, ist die Übersetzung veraltet."""
    return hashlib.sha1(((e.get('betreff') or '') + '\n' + (e.get('text') or '')).encode('utf-8')).hexdigest()[:12]


UEBERSETZEN = """Du übersetzt für das Team eines Restaurants einen Antwortbrief an einen Gast und das Gespräch, das der Gast im Chat geführt hat, ins Deutsche.
Die Übersetzung ist nur zum Mitlesen für das Team und wird nie verschickt. Übersetze genau und vollständig, nichts weglassen, nichts hinzufügen,
Schweizer Schreibung (ss statt ß). Stellen in eckigen Klammern bleiben in eckigen Klammern, übersetzt. Namen, Adressen, Zahlen und Preise bleiben, wie sie sind.
Antworte ausschliesslich mit JSON: {"betreff": "…", "text": "…", "verlauf": ["…", …]} – «verlauf» hat genau so viele Einträge wie im Eingang, in derselben Reihenfolge."""

def uebersetzen(id_):
    """Deutsche Lesefassung eines fremdsprachigen Briefs und seines Chat-Gesprächs (Robert 16.10.2026: «der Mitarbeiter … muss das auch nochmal kurz
    übersetzen können … sehen, wie das übersetzt aussieht, bevor er es abschickt»). Wird gespeichert und gilt, bis der Brief geändert wird."""
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    a = _lies(_pfad(id_), {})
    e = a.get('entwurf') or {}
    if not e.get('text'):
        raise ValueError('ÜBERSETZEN · Es gibt noch keinen Brief.')
    q = _quelle(e)
    if (e.get('deutsch') or {}).get('quelle') == q and a.get('verlauf_de'):
        return {'deutsch': e['deutsch'], 'verlauf_de': a['verlauf_de']}
    if _G is None:
        raise ValueError('CHAT · Der Assistent ist noch nicht geladen.')
    verlauf = [v.get('text', '') for v in a.get('verlauf') or []]
    eingabe = json.dumps({'betreff': e.get('betreff', ''), 'text': e['text'], 'verlauf': verlauf}, ensure_ascii=False)
    antwort = _G._api({'model': _G.MODELL, 'max_tokens': 6000, 'system': UEBERSETZEN, 'messages': [{'role': 'user', 'content': eingabe}]})
    roh = ''.join(b.get('text', '') for b in antwort.get('content', []) if b.get('type') == 'text').strip()
    roh = re.sub(r'^```(?:json)?\s*|\s*```$', '', roh)
    try:
        d = json.loads(roh[roh.index('{'):roh.rindex('}') + 1])
    except (ValueError, json.JSONDecodeError):
        raise ValueError('ÜBERSETZEN · Die Übersetzung kam unvollständig zurück. Bitte noch einmal versuchen.')
    with SCHLOSS:
        a = _lies(_pfad(id_), {})
        a['entwurf']['deutsch'] = {'betreff': str(d.get('betreff') or ''), 'text': str(d.get('text') or ''), 'quelle': q}
        vd = d.get('verlauf') if isinstance(d.get('verlauf'), list) else []
        a['verlauf_de'] = [str(x) for x in vd][:len(verlauf)] if len(vd) == len(verlauf) else a.get('verlauf_de') or []
        _schreib(_pfad(id_), a)
    return {'deutsch': a['entwurf']['deutsch'], 'verlauf_de': a['verlauf_de']}


def beispiele():
    """Beispiel-Anfragen mit fertigem Entwurf (gast_beispiele.json), damit das Haus sieht, wie der Eingang arbeitet (Robert 13.10.2026, erweitert 15.10.2026).
    Je Datenordner merkt sich beispiele.json den Stand. Ein neuer Stand legt nur die neu hinzugekommenen Beispiele an und schreibt die Entwürfe der
    noch vorhandenen neu; gelöschte Beispiele kommen nicht wieder. Liegt beim ersten Mal schon eine echte Anfrage da, bleibt der Eingang wie er ist.
    Namen und Adressen sind erfunden (example.com), in der Oberfläche steht «Beispiel» dabei."""
    marke = _pfad('beispiele.json')
    if _stand(marke) >= BEISPIEL_STAND:
        return 0
    with SCHLOSS:
        stand = _stand(marke)
        if stand >= BEISPIEL_STAND:
            return 0
        alt = _lies(marke, {}).get('anzahl', 0) if stand else 0
        da = {a.get('gespraech'): a for a in _alle('anfragen') if a.get('beispiel')}
        if not stand and any(not a.get('beispiel') for a in _alle('anfragen')):
            _schreib(marke, {'angelegt': '', 'anzahl': 0, 'stand': BEISPIEL_STAND})
            return 0
        liste = _lies(os.path.join(HIER, 'gast_beispiele.json'), [])
        jetzt = _jetzt(); n_neu = 0
        for n, b in enumerate(liste, 1):
            nr, absender = VORLAGE.get(b['art'], VORLAGE['nachricht'])
            absender = b.get('an') or absender
            g = f'beispiel-{n}'
            if g in da and stand >= 2:   # schon auf Stand 2: nur die deutsche Lesefassung dazu, Text, Gestaltung und Status bleiben
                a = da[g]; id_ = a.pop('id')
                if b.get('deutsch') and a.get('entwurf'):
                    a['entwurf']['deutsch'] = dict(b['deutsch'], quelle=_quelle(a['entwurf']))
                if b.get('verlauf_de'):
                    a['verlauf_de'] = b['verlauf_de']
                _schreib(_pfad(id_), a)
                continue
            if g in da:   # noch vorhanden: Entwurf und Angaben auf den neuen Stand, Status des Teams bleibt
                a = da[g]; id_ = a.pop('id')
                a.update({'name': b['name'], 'kontakt': b['kontakt'], 'datum': b['datum'], 'personen': b['personen'], 'anliegen': b['anliegen'],
                          'verlauf': [{'rolle': r, 'text': t} for r, t in b['verlauf']]})
                a['entwurf'] = {'betreff': b['betreff'], 'text': b['text'], 'team': b['team'], 'vorlage': nr, 'absender': absender, 'zeit': a.get('zeit')}
                if b.get('deutsch'):
                    a['entwurf']['deutsch'] = dict(b['deutsch'], quelle=_quelle(a['entwurf']))
                if b.get('verlauf_de'):
                    a['verlauf_de'] = b['verlauf_de']
                _schreib(_pfad(id_), a)
                continue
            if n <= alt:  # gab es schon und wurde gelöscht
                continue
            zeit = _zeit_vor(jetzt, b['vor'])
            _schreib(_pfad('anfragen', zeit[:10], f"{zeit[11:19].replace(':', '-')}_{g}.json"),
                     {'zeit': zeit, 'art': b['art'], 'name': b['name'], 'kontakt': b['kontakt'], 'datum': b['datum'], 'personen': b['personen'], 'anliegen': b['anliegen'],
                      'sprache': b['sprache'], 'gespraech': g, 'verlauf': [{'rolle': r, 'text': t} for r, t in b['verlauf']], 'status': b['status'], 'beispiel': True, **{k: b[k] for k in ('an', 'abteilung', 'seite', 'seite_name', 'web', 'nachricht', 'formular', 'allergene', 'uhrzeit', 'platz') if b.get(k)},
                      'entwurf': (dict({'betreff': b['betreff'], 'text': b['text'], 'team': b['team'], 'vorlage': nr, 'absender': absender, 'zeit': zeit},
                                       **({'deutsch': dict(b['deutsch'], quelle=_quelle(b))} if b.get('deutsch') else {})) if b.get('text') else None),   # Anfragen ohne Brief: den schreibt der Assistent auf Knopfdruck (Probe ohne KI: probe_ki.py)
                      **({'verlauf_de': b['verlauf_de']} if b.get('verlauf_de') else {})})
            n_neu += 1
        _schreib(marke, {'angelegt': jetzt.isoformat(timespec='seconds'), 'anzahl': len(liste), 'stand': BEISPIEL_STAND})
        return n_neu


def beispiel_fragen():
    """Beispiel-Fragen für «Das wurde gefragt» (gast_beispiel_fragen.json, Robert 14.10.2026: «Beispielfragen einsetzen in der Rezeption», erweitert 15.10.2026)
    und Beispiel-Antworten des Teams (gast_beispiel_nachgetragen.json). Stand wie bei beispiele(): ein neuer Stand legt nur Neues an.
    Die Antworten der Fragen stehen so im Wissen des Chats (Website und Unterlagen des Hauses); einige Fragen haben mit Absicht keine Antwort
    (Lücken zum Nachtragen). Die nachgetragenen Beispiele gehen nicht ins Wissen des Chats. In der Oberfläche steht «Beispiel» dabei."""
    marke = _pfad('beispiele_fragen.json')
    if _stand(marke) >= BEISPIEL_STAND:
        return 0
    with SCHLOSS:
        stand = _stand(marke)
        if stand >= BEISPIEL_STAND:
            return 0
        alt = _lies(marke, {}).get('anzahl', 0) if stand else 0
        jetzt = _jetzt()
        if not stand and glob.glob(_pfad('fragen', '*', '*.json')):
            _schreib(marke, {'angelegt': '', 'anzahl': 0, 'stand': BEISPIEL_STAND})
            return 0
        if stand and not alt:   # damals lag schon eine echte Frage da: auch jetzt keine Beispiele dazwischen
            _schreib(marke, {'angelegt': '', 'anzahl': 0, 'stand': BEISPIEL_STAND})
            return 0
        liste = _lies(os.path.join(HIER, 'gast_beispiel_fragen.json'), [])
        n_neu = 0
        for n, b in enumerate(liste, 1):
            if n <= alt:
                continue
            zeit = _zeit_vor(jetzt, b['vor'])
            _schreib(_pfad('fragen', zeit[:10], f"{zeit[11:19].replace(':', '-')}_beispiel-{n}.json"),
                     {'zeit': zeit, 'frage': b['frage'], 'antwort': b['antwort'], 'belegt': bool(b.get('belegt', True)), 'thema': b.get('thema', ''),
                      'gruppe': thema_von(b['frage']), 'sprache': b['sprache'], 'buchung': bool(b.get('buchung')), 'mappe': False, 'anfrage': '', 'beispiel': True})
            n_neu += 1
        ng = nachgetragen()
        if not any(str(x.get('nid', '')).startswith('beispiel-') for x in ng):
            for n, b in enumerate(_lies(os.path.join(HIER, 'gast_beispiel_nachgetragen.json'), []), 1):
                ng.append({'nid': f'beispiel-{n}', 'frage': b['frage'], 'antwort': b['antwort'], 'zeit': _zeit_vor(jetzt, b['vor']), 'quelle': '', 'beispiel': True})
            _schreib(_pfad('nachgetragen.json'), ng)
        _schreib(marke, {'angelegt': jetzt.isoformat(timespec='seconds'), 'anzahl': len(liste), 'stand': BEISPIEL_STAND})
        return n_neu


# ---------------------------------------------------------------- Nachgetragen vom Team
def nachgetragen():
    return _lies(_pfad('nachgetragen.json'), [])

def wissen_block():
    l = [x for x in nachgetragen() if (x.get('antwort') or '').strip() and not x.get('beispiel')]   # Beispiele sind erfunden, der Chat sagt sie nicht
    if not l:
        return ''
    return ('\n\nNACHGETRAGEN VOM TEAM (gilt wie WISSEN; das Team des Hauses hat diese Antworten selbst geschrieben, nachdem Gäste danach gefragt hatten):\n'
            + '\n'.join(f'Frage: {x["frage"]}\nAntwort des Hauses: {x["antwort"]}' for x in l))


# ---------------------------------------------------------------- Anbindung an _gast/gast.py
ZUSATZ = """

Anfragen an das Team (Werkzeug anfrage):
- Möchte ein Gast einen Tisch mit Wünschen reservieren (Allergien, Anlass, Platz auf der Terrasse oder an der Lästermeile), ein Bankett oder eine Feier anfragen (zwei Etagen für jeweils bis zu 26 Personen), Plätze für einen Anlass des Hauses oder einen Gutschein, bietest du an, die Anfrage an das Team weiterzugeben. Dafür brauchst du den Namen und eine E-Mail-Adresse oder Telefonnummer; frag in einem Satz danach.
- Sobald Name und Kontakt genannt sind, rufst du das Werkzeug anfrage auf, mit allem, was der Gast gesagt hat (Datum, Personen, Wünsche). Ohne Kontakt rufst du es nicht auf.
- Deine Antwort dazu: ein Satz, dass dies ein Entwurf von Tasty Studios ist und die Anfrage deshalb nicht an das Haus geht; für eine echte Anfrage hilft das Team am Telefon (Nummer wie oben). Sag nie, dass etwas reserviert, bestätigt oder weitergegeben ist.
- Für einen Tisch ohne besondere Wünsche bleibt die Reservation online der schnellste Weg; die Anfrage ist ein Angebot zusätzlich, wenn der Gast Wünsche hat oder lieber persönlich bedient wird.
- Allergien und Unverträglichkeiten nimmst du immer in die Anfrage auf. Ob ein Gericht frei davon ist, sagst du nur, wenn die Karte es mit ihren Kürzeln so ausweist; sonst sagst du, dass die Küche es mit dem Gast abstimmt."""

WERKZEUG = {
    'name': 'anfrage',
    'description': 'Gibt eine Anfrage des Gastes an das Team des Restaurants weiter (Reservation mit Wünschen, Bankett oder Feier, Plätze für einen Anlass, Gutschein, Nachricht). Nur aufrufen, wenn Name und E-Mail oder Telefon genannt sind.',
    'strict': True,
    'input_schema': {'type': 'object', 'additionalProperties': False, 'required': ['art', 'name', 'kontakt', 'datum', 'personen', 'anliegen'],
                     'properties': {'art': {'type': 'string', 'enum': list(ARTEN)},
                                    'name': {'type': 'string', 'description': 'Name, wie der Gast ihn nennt'},
                                    'kontakt': {'type': 'string', 'description': 'E-Mail-Adresse oder Telefonnummer, wörtlich'},
                                    'datum': {'type': ['string', 'null'], 'description': 'Datum oder Zeitraum, wie der Gast ihn nennt, oder null'},
                                    'personen': {'type': ['integer', 'null'], 'description': 'Anzahl Personen oder null'},
                                    'anliegen': {'type': 'string', 'description': 'Worum es geht, in ein bis drei Sätzen auf Deutsch, mit allen Wünschen des Gastes; Allergien und Unverträglichkeiten immer ausdrücklich'}}}}

DANKE = {'de': f'Danke. Dies ist ein Entwurf von Tasty Studios: Die Anfrage geht nicht an das Haus, sie liegt nur zur Ansicht {NAME_IM}.',
         'en': 'Thank you. This is a draft by Tasty Studios: your request does not go to the restaurant, it is only kept for viewing in the host tool.',
         'fr': 'Merci. Ceci est une ébauche de Tasty Studios : votre demande n’est pas transmise au restaurant, elle est seulement conservée pour être consultée.'}

ANFRAGE_GBR = """Du schreibst im Namen des Teams der Wirtschaft am Schlössli in Bottighofen (Restaurant direkt im Hafen am Bodensee, mediterrane Küche von Monika Huber, Gastgeber und Sommelier Jonas Volpert, Pächter Christian Kuchler; keine Zimmer) den Entwurf einer Antwort-Mail auf eine Anfrage, die ein Gast über ein Formular der Website oder im Chat gestellt hat (Reservation mit Wünschen, Bankett oder Feier, Plätze für einen Anlass, Gutschein, Nachricht).

Regeln:
- Grundlage ist, wo vorhanden, die VORLAGE: die Fragen, die das Haus in seinem eigenen Mail-Link stellt (Bankettanfrage: Datum, Uhrzeit, Personenzahl, Speisenform Tavolata oder gesetztes Menue, Anzahl Gänge, Richt-Budget; Anlass: Personen, Name, Telefon, Anschrift). Was davon in der Anfrage fehlt, erfragst du freundlich am Ende, in einer kurzen Liste. Gibt es keine Vorlage, gilt nur der Ton.
- Alles, was du an Preisen, Menüs, Gerichten, Zeiten, Plätzen und Leistungen nennst, steht wörtlich in WISSEN (Seiten und Karten des Hauses). Erfinde nichts, rechne keine Gesamtpreise, die nicht eindeutig aus den Angaben folgen. Die Bankettmenüs (Frühling, Sommer, Herbst) nennst du nur mit dem Preis, der dort steht.
- Freie Tische und Etagen kannst du nicht prüfen: setz dafür [Verfügbarkeit prüfen] an die Stelle. Fällt das Datum auf einen Dienstag oder Mittwoch (Ruhetag) oder in die Ferien des Hauses (13. bis 15. November 2026, 22. Dezember 2026 bis 10. Februar 2027), sag das freundlich und frag nach einem anderen Tag. Mehr Personen, als eine Etage fasst (26), sind [Etagen klären]. Was das Haus entscheiden muss, steht in eckigen Klammern, kurz und in normaler Schreibung, zum Beispiel [Tisch bestätigen] oder [Offerte freigeben]. Das Werkzeug zeigt diese Stellen als offene Felder im Brief.
- Allergien und Unverträglichkeiten: Nenne jede, die der Gast angibt, ausdrücklich und schreib, dass die Küche sie berücksichtigt [Küche informieren]. Sag nie von dir aus, ein Gericht sei frei davon.
- Ton des Hauses (Markenbuch): herzlich und unkompliziert, «mehr Wirtschaft», Sie-Form, Schweizer Schreibung (ss statt ß), keine Werbesprache (nicht «kulinarisches Highlight», «Genuss pur», «unvergesslich»), keine Emojis, kein Fettdruck. Kurze Absätze. Wendungen des Hauses, wo sie passen: «gerne», «in Ruhe besprechen», «Tavolata oder gesetztes Menue».
- Greif auf, was der Gast erzählt (Anlass, Wunsch, Platz), und nenne, wo es wirklich passt, höchstens einen Ort oder ein Gericht des Hauses aus WISSEN (zum Beispiel die Terrasse, die Lästermeile, die Tortelloni).
- Anrede «Guten Tag Frau …», «Guten Tag Herr …» bzw. in der Sprache des Gastes, Gruss «Mit freundlichen Grüssen» bzw. in der Sprache des Gastes (so in den Mail-Links des Hauses).
- Sprache: die Sprache des Gastes (steht bei der Anfrage).
- Form: Zeile 1 «Betreff: …» (persönlich, mit Anlass und Datum), dann Leerzeile, dann die Mail mit Anrede und Gruss, darunter zwei Zeilen: «[Name]» und «Wirtschaft am Schlössli». Adresse und Telefon stehen schon im Briefkopf, nicht wiederholen.
- Nach der Mail eine Zeile «---» und darunter für das Team, nicht für den Gast: «Grundlage:» mit den Seiten und Karten, aus denen die Angaben stammen, und «Offen:» mit dem, was das Team vor dem Senden klären muss.

WISSEN:
"""

_G = None

def einbinden(g):
    """Hängt La Réception an das geladene Modul _gast/gast.py: Werkzeug «anfrage», Wissen des Teams, Ablage statt Online-Speicher."""
    global _G
    _G = g
    os.makedirs(DATEN, exist_ok=True)
    g.WERKZEUGE = [w for w in g.WERKZEUGE if w.get('name') != 'anfrage'] + [WERKZEUG]
    if gedaechtnis:
        gedaechtnis._G = g
    basis = g.ANWEISUNG
    g.ANFRAGE = ANFRAGE_GBR + g.WISSEN
    roh_api, roh_frage, roh_ip = g._api, g.frage, g.handler._ip

    def api(koerper):
        a = roh_api(koerper)
        for b in a.get('content', []):
            if b.get('type') == 'tool_use' and b.get('name') == 'anfrage':
                LOKAL.anfrage = b.get('input') or {}
        return a

    def ip(self):
        LOKAL.ip = roh_ip(self)
        # «Chat ausprobieren» in La Réception lädt die Website mit ?probe=1: Fragen und Anfragen daraus gelten als Beispiel (Robert 16.10.2026)
        LOKAL.probe = 'probe=1' in (self.headers.get('referer') or self.headers.get('Referer') or '') or self.headers.get('X-Reception-Probe') == '1'
        return LOKAL.ip

    def frage(messages, mappe=False, heute='', sprache='de'):
        LOKAL.anfrage = None
        g.ANWEISUNG = (gedaechtnis.anweisung(basis) if gedaechtnis else basis) + ZUSATZ + wissen_block()   # vom Team Berichtigtes, Ergänztes und Nachgetragenes gilt ab der nächsten Frage
        a = roh_frage(messages, mappe=mappe, heute=heute, sprache=sprache)
        e = getattr(LOKAL, 'anfrage', None)
        LOKAL.anfrage = None
        if e and (e.get('kontakt') or '').strip():
            erste = next((str(m.get('content', '')) for m in messages if m.get('role') == 'user'), '')
            gespraech = hashlib.sha1((getattr(LOKAL, 'ip', '') + '|' + erste[:300]).encode('utf-8')).hexdigest()[:16]
            sp = sprache if sprache in SPRACHEN else 'de'
            if re.search(r"\b(the|is|are|could|would|we|our|table|room|please)\b", (messages[-1].get('content') or '').lower()) and sp == 'de':
                sp = 'en'
            if a.get('text') in g.NICHTS.values() or not a.get('text'):   # Text endete am Werkzeug: kurzer Dank statt «dazu kann ich nichts sagen»
                a['text'] = DANKE.get(sp, DANKE['en'])
            verlauf = [{'rolle': m.get('role'), 'text': str(m.get('content', ''))[:600]} for m in messages[-8:]] + [{'rolle': 'assistant', 'text': a.get('text', '')[:1200]}]
            LOKAL.letzte = lege_anfrage(e, gespraech, sp, verlauf)
            if getattr(LOKAL, 'probe', False) and LOKAL.letzte:
                with SCHLOSS:
                    x = _lies(_pfad(LOKAL.letzte), {})
                    if x:
                        x['beispiel'] = True; x['probe'] = True; _schreib(_pfad(LOKAL.letzte), x)
        return a

    def merke(host, daten):
        if getattr(LOKAL, 'probe', False):   # Tor 3 G1 (30.10.2026): Proben des Teams («Chat ausprobieren», ?probe=1) kommen nicht unter die Gästefragen
            return
        try:
            lege_frage(dict(daten, anfrage=getattr(LOKAL, 'letzte', None) or '', beispiel=bool(getattr(LOKAL, 'probe', False))))
        except Exception:  # noqa: BLE001  die Antwort an den Gast bleibt davon unberührt
            pass

    roh_erlaubt = g.erlaubt
    PROBEN = {'tag': '', 'n': 0}

    def erlaubt(ip_, art='gast'):
        """Proben des Teams («Chat ausprobieren», Prüfläufe) zählen nicht gegen die Grenzen der Gäste, haben aber eine eigene: 400 am Tag (Carlton 17.10.2026)."""
        if getattr(LOKAL, 'probe', False) and art == 'gast':
            heute = time.strftime('%Y-%m-%d')
            with SCHLOSS:
                if PROBEN['tag'] != heute:
                    PROBEN.update(tag=heute, n=0)
                PROBEN['n'] += 1
                return PROBEN['n'] <= 400
        return roh_erlaubt(ip_, art)

    g._api, g.frage, g.merke, g.handler._ip, g.erlaubt = api, frage, merke, ip, erlaubt
    # Die Frage im Protokoll soll wissen, ob daraus eine Anfrage wurde: do_POST ruft frage(), dann merke(); dazwischen merkt sich LOKAL.letzte die Kennung.
    roh_post = g.handler.do_POST

    def do_post(self):
        LOKAL.letzte = None; LOKAL.probe = False
        return roh_post(self)
    g.handler.do_POST = do_post
    return g


# ---------------------------------------------------------------- Entwurf
def vorlage_text(art, sprache):
    """Die Fragen des Hauses aus seinem eigenen Mail-Link (vorlagen/<nr>.txt, Deutsch); ohne Vorlage leer. Der Assistent schreibt in der Sprache des Gastes."""
    nr, absender = VORLAGE.get(art, VORLAGE['nachricht'])
    if not nr:
        return '', absender, 'de', ''
    try:
        t = open(os.path.join(HIER, 'vorlagen', nr + '.txt'), encoding='utf-8').read().strip()
    except OSError:
        return nr, absender, 'de', ''
    return nr, absender, 'de', t


def _datum_aus(text):
    """Datum aus den Angaben der Formulare («Do, 22. Oktober 2026», «22.10.2026», «2026-10-22»); sonst None."""
    t = str(text or '')
    mon = {m: i for i, m in enumerate(('januar', 'februar', 'märz', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'dezember'), 1)}
    try:
        m = re.search(r'(\d{4})-(\d{2})-(\d{2})', t)
        if m:
            return datetime.date(int(m[1]), int(m[2]), int(m[3]))
        m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', t)
        if m:
            return datetime.date(int(m[3]), int(m[2]), int(m[1]))
        m = re.search(r'(\d{1,2})\.\s*([A-Za-zÄÖÜäöü]+)\s+(\d{4})', t)
        if m and m[2].lower() in mon:
            return datetime.date(int(m[3]), mon[m[2].lower()], int(m[1]))
    except ValueError:
        return None
    return None


def hinweise(a):
    """Hinweise fürs Team zu einer Anfrage, nur aus Angaben des Hauses gerechnet (nicht gespeichert, bei jedem Lesen neu):
    Ruhetag (Dienstag, Mittwoch), Ferien, mehr Personen als eine Etage fasst (26, nur bei Bankett und Anlass), Allergien und Unverträglichkeiten."""
    h = []
    d = _datum_aus(a.get('datum'))
    if d:
        if d.weekday() in RUHETAGE:
            h.append({'art': 'ruhetag', 'text': ('Dienstag' if d.weekday() == 1 else 'Mittwoch') + ' ist Ruhetag'})
        for von, bis, satz in FERIEN:
            if von <= d.isoformat() <= bis:
                h.append({'art': 'ferien', 'text': satz})
    try:
        p = int(a.get('personen') or 0)
    except (TypeError, ValueError):
        p = 0
    if p > ETAGE and a.get('art') in ('bankett', 'anlass', 'tisch'):
        h.append({'art': 'etage', 'text': f'{p} Personen: mehr als eine Etage fasst (je bis zu {ETAGE})'})
    al = [ALLERGENE.get(x, x) for x in (a.get('allergene') or []) if isinstance(x, str)]
    text = ' '.join(str(a.get(k) or '') for k in ('anliegen', 'nachricht'))
    text = re.sub(r'(?:Wünsche, Allergien|Gericht, Allergien|Allergien)\s*:|keine angegeben', ' ', text)   # Feldnamen der Formulare zählen nicht, nur was der Gast schreibt
    frei = re.findall(r'allerg\w*|unverträglich\w*|verträgt keine?\b|zöliak\w*|gluten\w*|laktose\w*|nuss\w*|nüsse|vegan\w*|vegetar\w*', text, re.I)
    if al:
        h.append({'art': 'allergie', 'text': 'Allergien: ' + ', '.join(al)})
    elif frei:
        h.append({'art': 'allergie', 'text': 'Allergien oder Wünsche zur Küche im Text'})
    return h

def entwurf(id_, hinweis=''):
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    if _G is None:
        raise ValueError('CHAT · Der Assistent ist noch nicht geladen. Einmal eine Frage im Chat stellen oder server.py neu starten.')
    a = _lies(_pfad(id_), {})
    nr, absender, sp_v, vorlage = vorlage_text(a.get('art'), a.get('sprache', 'de'))
    absender = MAIL   # das Schlössli antwortet immer von kontakt@
    gast = '\n'.join(f"{'Gast' if v.get('rolle') == 'user' else 'Chat des Hauses'}: {v.get('text', '')}" for v in a.get('verlauf') or [])
    mail = (f"Art: {ARTEN.get(a.get('art'), a.get('art'))}\nAbteilung: {a.get('abteilung') or ART_ABTEILUNG.get(a.get('art'), 'Reservation')}\nName: {a.get('name')}\nKontakt: {a.get('kontakt')}\nDatum: {a.get('datum') or 'nicht genannt'}\n"
            f"Personen: {a.get('personen') or 'nicht genannt'}\nAnliegen: {a.get('anliegen')}\nSprache des Gastes: {a.get('sprache')}\n\nGESPRÄCH IM CHAT:\n{gast}\n\n"
            f"Allergien (Formular): {', '.join(ALLERGENE.get(x, x) for x in a.get('allergene') or []) or 'keine angegeben'}\nHinweise: {'; '.join(x['text'] for x in hinweise(a)) or 'keine'}\n\n"
            f"VORLAGE DES HAUSES ({nr or 'keine'}, Sprache {sp_v}):\n{vorlage or '(keine: nur der Ton des Hauses)'}")
    _G.ANFRAGE = ANFRAGE_GBR + (gedaechtnis.wissen_text(_G.WISSEN) if gedaechtnis else _G.WISSEN) + wissen_block()   # derselbe Stand wie im Chat
    r = _G.anfrage(mail, hinweis)
    if r.get('fehler'):
        raise ValueError('ENTWURF · ' + r['fehler'])
    entwurf_neu = {'betreff': r.get('betreff', ''), 'text': r.get('text', ''), 'team': r.get('team', ''), 'vorlage': nr, 'absender': absender,
                   'zeit': datetime.datetime.now().astimezone().isoformat(timespec='seconds')}
    with SCHLOSS:
        # frisch lesen: während der Assistent schrieb (Sekunden), kann das Team die Anfrage geändert haben (Status, Notiz, Betreff);
        # vorher überschrieb der alte Stand von oben diese Änderungen (17.10.2026)
        a = _lies(_pfad(id_), a)
        entwurf_neu['fassung'] = ((a.get('entwurf') or {}).get('fassung', 0) or 0) + 1
        a['entwurf'] = entwurf_neu
        if a.get('status') == 'neu':
            a['status'] = 'gelesen'
        _schreib(_pfad(id_), a)
    return a['entwurf']


# ---------------------------------------------------------------- Schnittstelle für La Réception (/reception/api/<was>)
def ueberblick():
    an = _alle('anfragen'); fr = _alle('fragen'); ng = nachgetragen()
    erledigt = set(_lies(_pfad('status.json'), {}).get('fragen_erledigt', []))
    luecken = [f for f in fr if not f.get('belegt') and f['id'] not in erledigt]
    return {'anfragen_neu': sum(1 for a in an if a.get('status') == 'neu'), 'anfragen_offen': sum(1 for a in an if a.get('status') != 'erledigt'),
            'anfragen_gesamt': len(an), 'fragen_gesamt': len(fr), 'ohne_antwort': len(luecken), 'nachgetragen_gesamt': len(ng),
            'letzte_frage': fr[0]['zeit'] if fr else '', 'speicher': os.path.relpath(DATEN, WEB)}

# ---------------------------------------------------------------- Online-Eingang der Website (29.10.2026)
# Die Website läuft auf Vercel, das Gästebuch auf Roberts Rechner. Was Gäste dort eintragen (assets/anfrage.js), liegt in der Funktion /api/anfrage
# (privater Speicher in Frankfurt). Das Gästebuch holt es mit dem Schlüssel aus online/schluessel.txt ab, legt es wie ein Formular in den Eingang
# und löscht es danach online. RECEPTION_ONLINE=aus schaltet das Abholen ab (Prüfläufe mit Wegwerf-Daten), eine andere Adresse geht ebenso.
# Nur das echte Gästebuch (Datenordner daten/) holt von selbst ab. Probe-Kopien mit RECEPTION_DATEN holen nur mit ausdrücklichem RECEPTION_ONLINE,
# sonst nähmen Prüfläufe echte Einträge der Gäste in ihre Wegwerf-Daten mit (29.10.2026: zwei Proben so verschwunden).
ONLINE_API = os.environ.get('RECEPTION_ONLINE') or 'aus'   # Schlössli (3.11.2026): die Website hat noch keinen Online-Eingang, nichts wird abgeholt
ONLINE_SCHLUESSEL = os.path.join(HIER, 'online', 'schluessel.txt')
ONLINE_STAND = {'zeit': '', 'neu': 0, 'fehler': ''}
_ONLINE_SCHLOSS = threading.Lock()


def online_abholen():
    """Holt die Anfragen der Website ab; jede kommt genau einmal in den Eingang (online_id), erst danach wird sie online gelöscht."""
    import urllib.parse, urllib.request
    if ONLINE_API == 'aus' or not _ONLINE_SCHLOSS.acquire(blocking=False):
        return 0
    try:
        k = open(ONLINE_SCHLUESSEL, encoding='utf-8').read().strip()
        with urllib.request.urlopen(ONLINE_API + '?' + urllib.parse.urlencode({'k': k}), timeout=20) as r:
            roh = json.load(r)
        liste, fragen = roh.get('anfragen') or [], roh.get('fragen') or []
        schon = {a.get('online_id') for a in _alle('anfragen') + _alle('fragen') if a.get('online_id')}
        neu = 0
        for f in fragen:   # der Gäste-Chat der Website: jede Frage mit Antwort, ohne Antwort als Lücke unter «Das wurde gefragt»
            oid = str(f.get('id') or '')
            if not re.fullmatch(r'fragen/\d{4}-\d{2}-\d{2}/[\w-]+\.json', oid):
                continue
            if f.get('probe'):   # Tor 3 (30.10.2026): Probe-Fragen der Website (?probe=1, Prüfläufe) kommen nicht unter die Gästefragen; online wird sie trotzdem gelöscht
                pass
            elif oid not in schon:
                fid = lege_frage({'frage': f.get('frage', ''), 'antwort': f.get('antwort', ''), 'belegt': f.get('belegt') is not False, 'thema': f.get('thema', ''), 'sprache': f.get('sprache', 'de')})
                with SCHLOSS:
                    x = _lies(_pfad(fid), {})
                    x.update({'online_id': oid, 'web': True, **({'probe': True} if f.get('probe') else {})})
                    try:
                        x['zeit'] = datetime.datetime.fromisoformat(str(f.get('zeit'))).astimezone().isoformat(timespec='seconds')
                    except ValueError:
                        pass
                    _schreib(_pfad(fid), x)
                neu += 1
            weg = urllib.request.Request(ONLINE_API + '?' + urllib.parse.urlencode({'k': k, 'weg': oid}), data=b'', method='POST')
            urllib.request.urlopen(weg, timeout=20).read()
        for a in liste:
            oid = str(a.get('id') or '')
            if not re.fullmatch(r'anfragen/\d{4}-\d{2}-\d{2}/[\w-]+\.json', oid):
                continue
            if oid not in schon:
                try:
                    post('formular', {**{k_: v for k_, v in a.items() if k_ != 'id'}, 'website': '', 'online_id': oid})
                except ValueError as e:   # nimmt das Gästebuch nicht an: online liegen lassen, Stand zeigt es
                    ONLINE_STAND['fehler'] = f'{oid}: {e}'
                    continue
                neu += 1
            weg = urllib.request.Request(ONLINE_API + '?' + urllib.parse.urlencode({'k': k, 'weg': oid}), data=b'', method='POST')
            urllib.request.urlopen(weg, timeout=20).read()
        ONLINE_STAND.update(zeit=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), neu=neu)
        if not any(str(a.get('id')) in ONLINE_STAND['fehler'] for a in liste):
            ONLINE_STAND['fehler'] = ''
        return neu
    except Exception as e:  # noqa: BLE001 (kein Netz, Schlüssel fehlt, Speicher besetzt): beim nächsten Mal wieder
        ONLINE_STAND['fehler'] = type(e).__name__ + ': ' + str(e)[:160]
        return 0
    finally:
        _ONLINE_SCHLOSS.release()


def get(was, q=None):
    if was.startswith('wissen') and gedaechtnis:
        return {**gedaechtnis.get(was, q), 'nachgetragen': nachgetragen()} if was == 'wissen' else gedaechtnis.get(was, q)
    beispiele(); beispiel_fragen()
    if was == 'ueberblick':
        return ueberblick()
    if was == 'anfragen':
        an = _alle('anfragen')
        for a in an:
            a['hinweise'] = hinweise(a)
            a['allergene_lang'] = [ALLERGENE.get(x, x) for x in a.get('allergene') or [] if isinstance(x, str)]
        return {'anfragen': an, **ueberblick()}
    if was == 'fragen':
        erledigt = set(_lies(_pfad('status.json'), {}).get('fragen_erledigt', []))
        fr = _alle('fragen')
        for f in fr:
            f['erledigt'] = f['id'] in erledigt
            f['gruppe'] = thema_von(f.get('frage'))
        return {'fragen': fr, 'nachgetragen': nachgetragen(), **ueberblick()}
    if was == 'vorlage':
        nr, absender, sp, t = vorlage_text((q or {}).get('art', ['nachricht'])[0], (q or {}).get('sprache', ['de'])[0])
        return {'vorlage': nr, 'absender': absender, 'sprache': sp, 'text': t}
    raise ValueError('ANFRAGE · Unbekannte Ansicht.')

def brief_pdf(id_, port):
    """Der Brief einer Anfrage als A4-PDF: Chromium setzt brief-pdf.html (brief_pdf.js, Playwright wie in La Carte). Gibt (Bytes, Dateiname) zurück."""
    import subprocess, tempfile
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    a = _lies(_pfad(id_), {}); e = a.get('entwurf') or {}
    if not e.get('text'):
        raise ValueError('BRIEF · Zu dieser Anfrage gibt es noch keinen Brief.')
    daten = {'name': a.get('name') or '', 'kontakt': a.get('kontakt') or '', 'absender': e.get('absender') or MAIL,
             'betreff': e.get('betreff') or '', 'text': e.get('text') or '', 'gestalt': e.get('gestalt') or {}}
    node = shutil.which('node') or next((x for x in ('/opt/homebrew/bin/node', '/usr/local/bin/node') if os.path.exists(x)), None)
    if not node:
        raise ValueError('PDF · node ist nicht installiert (wird für das PDF gebraucht).')
    with tempfile.TemporaryDirectory() as t:
        quelle, ziel = os.path.join(t, 'brief.json'), os.path.join(t, 'brief.pdf')
        with open(quelle, 'w', encoding='utf-8') as f:
            json.dump(daten, f, ensure_ascii=False)
        try:
            r = subprocess.run([node, os.path.join(HIER, 'brief_pdf.js'), str(port), quelle, ziel], capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            raise ValueError('PDF · Das PDF liess sich nicht setzen (Zeitüberschreitung).')
        if r.returncode != 0 or not os.path.exists(ziel):
            raise ValueError('PDF · Das PDF liess sich nicht setzen. Ist Playwright installiert? ' + (r.stderr or '')[-160:])
        roh = open(ziel, 'rb').read()
    wer = re.sub(r'[\\/:*?"<>|\n\r]+', ' ', a.get('name') or 'Gast').strip()[:60] or 'Gast'
    return roh, f'Wirtschaft am Schlössli – {wer} – {datetime.date.today().strftime("%d.%m.%Y")}.pdf'


def post(was, d):
    if was.startswith('wissen') and gedaechtnis:
        return gedaechtnis.post(was, d)
    beispiele(); beispiel_fragen()
    if was == 'uebersetzen':
        return {**uebersetzen(d.get('id')), **ueberblick()}
    if was == 'entwurf':
        return {'entwurf': entwurf(d.get('id'), str(d.get('hinweis') or '')[:2000]), **ueberblick()}
    if was == 'anfrage':            # Status, Notiz oder geänderter Entwurf des Teams
        id_ = d.get('id')
        if not _gueltig(id_, 'anfragen'):
            raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
        with SCHLOSS:
            a = _lies(_pfad(id_), {})
            aendert = a.get('entwurf') and (isinstance(d.get('entwurf_text'), str) or isinstance(d.get('gestalt'), dict))
            if aendert and isinstance(d.get('fassung'), int) and d['fassung'] != a['entwurf'].get('fassung', 0):
                raise ValueError('KONFLIKT · Dieser Brief wurde inzwischen in einem anderen Fenster geändert. Ihre Eingabe ist noch hier; bitte kopieren, neu laden und wieder einsetzen.')
            if aendert:
                a['entwurf']['fassung'] = a['entwurf'].get('fassung', 0) + 1
            if d.get('status') in ('neu', 'gelesen', 'erledigt'):
                a['status'] = d['status']
            if isinstance(d.get('entwurf_text'), str) and a.get('entwurf'):
                if 'original' not in a['entwurf']:
                    a['entwurf']['original'] = {'text': a['entwurf'].get('text') or '', 'betreff': a['entwurf'].get('betreff') or ''}
                a['entwurf']['text'] = d['entwurf_text'][:12000]
                if isinstance(d.get('betreff'), str):
                    a['entwurf']['betreff'] = d['betreff'][:300]
                a['entwurf']['geaendert'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
            if isinstance(d.get('gestalt'), dict) and a.get('entwurf') and len(json.dumps(d['gestalt'])) < 20000:   # Anordnung des Briefs (verschoben, Grösse, Bündigkeit, Kopftexte)
                a['entwurf']['gestalt'] = d['gestalt']
            _schreib(_pfad(id_), a)
        return {'ok': True, 'fassung': (a.get('entwurf') or {}).get('fassung', 0), **ueberblick()}
    if was == 'formular':           # Formular der Website (baustein/anfrage.js): landet im Eingang, nicht in einem Mailfach (Rivage E12, Ruedihus 17.10.2026, Schlössli 19.10.2026, Schäfli 21.10.2026, Schlössli Nachtbau 3.11.2026)
        if d.get('website'):        # Feld, das Menschen nicht sehen: nur Maschinen füllen es aus
            return {'ok': True}
        name, kontakt = str(d.get('name') or '').strip()[:120], str(d.get('kontakt') or '').strip()[:160]
        if not kontakt:
            raise ValueError('FORMULAR · Bitte E-Mail oder Telefon angeben, damit das Haus antworten kann.')
        if not re.fullmatch(r'[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]{2,}|\+?[\d\s/().-]{7,24}', kontakt):
            raise ValueError('FORMULAR · Bitte eine gültige E-Mail-Adresse oder Telefonnummer angeben.')
        art = d.get('art') if d.get('art') in ARTEN else 'nachricht'
        sp = d.get('sprache') if d.get('sprache') in SPRACHEN else 'de'
        try:
            pers = max(1, min(60, int(d.get('personen'))))
        except (TypeError, ValueError):
            pers = None
        anliegen = str(d.get('anliegen') or '').strip()[:300]
        nachricht = str(d.get('nachricht') or '').strip()[:6000]   # Angaben des Formulars + Nachricht des Gastes (bis 1'200) + Wünsche ohne Grenze: 1'200 schnitt still ab (Prüfung 17.10.2026); die Anfrage selbst bleibt unter 12 kB
        an = MAIL
        allergene = [x for x in (d.get('allergene') or []) if x in ALLERGENE][:len(ALLERGENE)] if isinstance(d.get('allergene'), list) else []
        seite = str(d.get('seite') or '')[:160]
        seite = re.sub(r'[^\w./?#=&%-]', '', seite) if seite.startswith('/') else ''   # Weg der Seite (mit ? und #), nur harmlose Zeichen
        seite_name = re.sub(r'[<>]', '', str(d.get('seite_name') or ''))[:80]
        formular = d.get('formular') if d.get('formular') in FORMULARE else 'allgemein'
        text = nachricht or anliegen
        id_ = lege_anfrage({'art': art, 'name': name, 'kontakt': kontakt, 'datum': str(d.get('datum') or '')[:120], 'personen': pers, 'anliegen': anliegen or text[:200]},
                           'formular-' + hashlib.sha1(f'{time.time()}{random.random()}'.encode()).hexdigest()[:12], sp,
                           [{'rolle': 'user', 'text': f'Über ein Formular der Website (Seite {seite_name or seite or "unbekannt"}): ' + text}])
        with SCHLOSS:
            x = _lies(_pfad(id_), {})
            x.update({'web': True, 'an': an, 'abteilung': ART_ABTEILUNG.get(art, 'Reservation'), 'seite': seite, 'seite_name': seite_name, 'formular': formular,
                      'nachricht': nachricht, 'allergene': allergene, 'uhrzeit': str(d.get('uhrzeit') or '')[:20], 'platz': str(d.get('platz') or '')[:60], 'hund': d.get('hund') is True})
            if d.get('probe') is True:
                x['probe'] = True
            if d.get('online_id'):   # von der Website über /api/anfrage (online_abholen): Zeit des Gastes und Kennung im Online-Speicher
                x['online_id'] = str(d['online_id'])[:120]
                try:
                    x['zeit'] = datetime.datetime.fromisoformat(str(d.get('zeit'))).astimezone().isoformat(timespec='seconds')
                except ValueError:
                    pass
            _schreib(_pfad(id_), x)
        return {'ok': True, 'danke': DANKE.get(sp, DANKE['de'])}
    if was == 'weg':                # Anfrage oder Frage löschen (Wunsch des Gastes, Test)
        id_ = d.get('id', '')
        art = id_.split('/')[0]
        if art not in ('anfragen', 'fragen') or not _gueltig(id_, art):
            raise ValueError('ANFRAGE · Dieser Eintrag existiert nicht.')
        with SCHLOSS:
            os.remove(_pfad(id_))
            for rest in ('.gut', '.neu'):
                try:
                    os.remove(_pfad(id_) + rest)
                except OSError:
                    pass
        return {'ok': True, **ueberblick()}
    if was == 'frage':              # Frage erledigt / wieder offen
        id_ = d.get('id')
        if not _gueltig(id_, 'fragen'):
            raise ValueError('FRAGE · Diese Frage gibt es nicht mehr.')
        with SCHLOSS:
            s = _lies(_pfad('status.json'), {}); l = [x for x in s.get('fragen_erledigt', []) if x != id_]
            if d.get('erledigt'):
                l.append(id_)
            s['fragen_erledigt'] = l[-5000:]
            _schreib(_pfad('status.json'), s)
        return {'ok': True, **ueberblick()}
    if was == 'nachtragen':         # Antwort des Teams auf eine Frage ohne Antwort
        frage_ = str(d.get('frage') or '').strip()[:400]; antwort = str(d.get('antwort') or '').strip()[:2000]
        if len(frage_) < 3 or len(antwort) < 3:
            raise ValueError('EINGABE · Bitte Frage und Antwort ausfüllen.')
        with SCHLOSS:
            l = nachgetragen()
            nid = d.get('nid') or ('n' + str(int(time.time() * 1000)))
            alt = next((x for x in l if x.get('nid') == nid), None)
            eintrag = {'nid': nid, 'frage': frage_, 'antwort': antwort, 'zeit': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                       'quelle': d.get('quelle') or (alt or {}).get('quelle') or ''}
            l = [x for x in l if x.get('nid') != nid] + [eintrag]
            _schreib(_pfad('nachgetragen.json'), l)
            if d.get('quelle') and _gueltig(d['quelle'], 'fragen'):
                s = _lies(_pfad('status.json'), {}); fe = set(s.get('fragen_erledigt', [])); fe.add(d['quelle'])
                s['fragen_erledigt'] = sorted(fe)[-5000:]; _schreib(_pfad('status.json'), s)
        return {'ok': True, 'eintrag': eintrag, **ueberblick()}
    if was == 'nachtragen_weg':
        with SCHLOSS:
            _schreib(_pfad('nachgetragen.json'), [x for x in nachgetragen() if x.get('nid') != d.get('nid')])
        return {'ok': True, **ueberblick()}
    raise ValueError('ANFRAGE · Unbekannter Auftrag.')
