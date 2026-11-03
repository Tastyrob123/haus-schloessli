#!/usr/bin/env python3
"""Das Besucherbuch (Le Registre) · Wirtschaft am Schlössli, Bottighofen TG (Tasty Studios 19.10.2026, Werkzeug 6): das Haus sieht, wer seine Website besucht.
Je Besuch: Land und Ort, Tag und Uhrzeit, Gerät, Sprache des Browsers, woher der Gast kam, welche Seiten er in welcher Reihenfolge ansah, wie lange
jede Seite sichtbar war und ob er das Fenster «Reservation» öffnete, dort einen Tisch anfragte oder «Direkt buchen» (gastronovi) wählte, die
Bankettanfrage öffnete, eine Anfrage abschickte (Bankett, Gutschein), anrief, eine Mail-Adresse anklickte, zum Schwesterhaus Schäfli weiterging
oder die Route zum Hafen aufrief. Nie ein Name, nie eine Adresse der Verbindung, kein Cookie.

Kopie von Das Besucherbuch des Berghotel Gasterntal (_werkzeuge/registre/, Bau 17./18.10.2026, nur gelesen und kopiert), dieses nach dem Waldhotel
Doldenhorn und dem Carlton-Europe; Funktion und Bedienung wie Le Registre des Grand Beau-Rivage. Angepasst an die Wirtschaft am Schlössli
(ein Restaurant, keine Zimmer): Seiten des Hauses (Karte, Weinkarte, Banketts & Gruppen, Events & Termine, Ihr Abend, Gutschein, Kontakt),
Ereignisse des Hauses (Reservation im Fenster der Website mit zwei Wegen: «Mit Wünschen anfragen» und «Direkt buchen» über gastronovi),
Herkunftsnamen und Beispielorte rund um den Bodensee, Sprache = Sprache des Browsers (die Website gibt es nur deutsch).
Eigener Zähl-Schlüssel und eigener Speicher, getrennt vom Schäfli und von jedem anderen Haus (Werkzeug-Master 3, Robert 17.10.2026).

Der Browser schickt je Seite eine Zeile an /api/registre (assets/messung.js der Website, Quelle vorschlag/messung.js):
    r1 <seitenaufruf> <datei> <sprache> <geraet> <sekunden> <ereignisse|-> <herkunft|->
Einmal beim Öffnen (0 Sekunden), bei jedem gezählten Klick und beim Verlassen (sichtbare Sekunden und die Klicks).

Damit die Seiten eines Besuchs zusammenfinden, bildet der Server je Tag ein Kürzel aus Tag + Adresse der Verbindung + Browser-Kennung
(HMAC mit geheimem Schlüssel). Die Adresse selbst wird nie gespeichert; weil der Tag im Kürzel steckt, erkennt der nächste Tag
denselben Gast nicht wieder. Land und Ort nennt der Anbieter aus der Verbindung. Nach AUFBEWAHREN Tagen wird gelöscht.

Speicher: je Tag (Kalendertag in Bottighofen, Europe/Zurich) eine Datei, lokal _daten/<tag>.json.
Vorführ-Betrieb (Master Lernprotokoll 14.10.2026, Robert: «Da sollen Probewerte angezeigt werden. Für den Kunden»): die Abfrage antwortet
jedem mit Beispielwerten, als Beispiel beschriftet. Echte Werte nur mit Schlüssel (siehe server.py).

  python3 registre.py                  Stand der letzten 30 Tage (echt, lokal)
  python3 registre.py beispiel         dasselbe mit Beispielwerten
  python3 registre.py ablage           schreibt beispiel/7.json, 30.json, 90.json (falls das Werkzeug ohne Server-Teil läuft)
  python3 registre.py aufraeumen       löscht Tagesdateien älter als AUFBEWAHREN Tage
  python3 registre.py seiten           seiten.json und seiten-bilder.json neu aus der Website (nach neuen Seiten)
  python3 registre.py leeren           Zählung lokal leeren (alter Ordner bleibt als _daten.vor-leeren)"""
import collections, datetime, hashlib, hmac, json, os, random, re, sys, threading, time

HIER = os.path.dirname(os.path.abspath(__file__))
ORDNER = os.environ.get('REGISTRE_ORDNER') or os.path.join(HIER, '_daten')   # Prüfläufe zählen in einen eigenen Ordner
GEHEIM = (os.environ.get('REGISTRE_GEHEIM') or 'schloessli-bottighofen-nur-lokal').encode('utf-8')
# Klicks, die zählen (messung.js): Fenster «Reservation» geöffnet, Tisch angefragt, «Direkt buchen», Bankettanfrage geöffnet,
# Anfrage abgeschickt (Bankett, Gutschein), Telefonnummer, Mail-Adresse, weiter zum Schäfli, Route zum Hafen
EREIGNISSE = ('fenster', 'buchung', 'booking', 'tisch', 'anfrage', 'anruf', 'mail', 'chat', 'route')
# Bedeutung im Schlössli (Schlüssel wie in allen Häusern, damit La Maison, Prüfläufe und Ablage gleich lesen):
#   fenster = Fenster «Reservation» geöffnet · buchung = darin Tisch angefragt («Mit Wünschen anfragen» abgeschickt) · booking = «Direkt buchen» (gastronovi)
#   tisch = Fenster «Bankettanfrage» geöffnet · anfrage = Bankettanfrage oder Gutschein abgeschickt · anruf · mail
#   chat = weiter zum Schwesterhaus (Taverne zum Schäfli; die Website hat keinen Gäste-Chat) · route = Route zum Hafen (kontakt.html)
ZUR_BUCHUNG = {'buchung', 'booking'}   # «zur Reservation»: Tisch angefragt oder «Direkt buchen» (gastronovi) gewählt
SPRACHEN = ('de', 'en', 'fr', 'it', 'nl', 'es', 'pt', 'zh', 'ja', 'ko', 'ar', 'xx')   # Sprache des Browsers; xx = eine andere
GERAETE = ('handy', 'tablet', 'rechner')
PAUSE = 30 * 60        # nach einer halben Stunde ohne neue Seite beginnt ein neuer Besuch
LANG = 30 * 60         # länger als eine halbe Stunde sichtbar zählt eine Seite nicht
MAX_TAG = 4000         # Seitenaufrufe je Tag; darüber wird nichts mehr angenommen (Schutz vor Unfug)
AUFBEWAHREN = 400      # Tage; ältere Tagesdateien löscht aufraeumen() (Datenschutz: nicht länger als nötig)
AUTOMAT = re.compile(r'bot|crawl|spider|slurp|headless|lighthouse|preview|monitor|uptime|curl|wget|python|scrapy|facebookexternalhit|whatsapp|telegram|vercel', re.I)
_SCHLOSS = threading.Lock()

# Seiten des Schlössli nach Art (die Seiten aus bau.py der Website)
KARTE = ('karte.html', 'weinkarte.html')
ESSEN = ('feiern.html',)                    # Banketts & Gruppen: dort liegt die Bankettanfrage
ERLEBEN = ('anlaesse.html', 'abend.html')   # Events & Termine, Ihr Abend
FESTE = ('gutschein.html',)
WEG = ('kontakt.html',)
ABEND = ()                                  # keine eigene Buchungsseite: das Fenster «Reservation» öffnet sich auf jeder Seite


class Konflikt(Exception):
    pass


def jetzt():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo('Europe/Zurich'))
    except Exception:  # noqa: BLE001  ohne Zeitzonen-Daten: Uhr des Rechners
        return datetime.datetime.now()


def art_von(datei):
    if datei == 'index.html': return 'start'
    if datei in KARTE: return 'karte'
    if datei in ABEND: return 'abend'
    if datei in ESSEN: return 'essen'
    if datei in ERLEBEN: return 'erleben'
    if datei in FESTE: return 'feste'
    if datei in WEG: return 'weg'
    return 'sonst'


# ---- Speicher: lokal je Tag eine Datei. Ein Online-Teil ersetzt nur diese drei Funktionen.
def _lies(tag):
    try:
        with open(os.path.join(ORDNER, tag + '.json'), encoding='utf-8') as f:
            d = json.load(f)
        return (d if isinstance(d, dict) else {}), None
    except (OSError, ValueError):
        return {}, None


def _schreib(tag, d, marke):
    os.makedirs(ORDNER, exist_ok=True)
    p = os.path.join(ORDNER, tag + '.json')
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
    os.replace(p + '.neu', p)


def _tage_lesen(tage):
    return {t: _lies(t)[0] for t in tage}


# ---- Annehmen
def _kuerzel(tag, ip, ua):
    return hmac.new(GEHEIM, f'{tag}|{ip}|{ua}'.encode('utf-8', 'replace'), hashlib.sha256).hexdigest()[:10]


def _wort(s, n=60):
    return re.sub(r'[^\w\s\-’\'.()]', '', str(s or ''), flags=re.U).strip()[:n]


def melde(roh, ip='', ua='', land='', ort='', region=''):
    """Eine Zeile des Browsers. Angenommen wird nur, was genau dem Muster entspricht; alles andere fällt weg."""
    if not roh or len(roh) > 300 or AUTOMAT.search(ua or '') or not (ua or '').strip():
        return False
    try:
        t = roh.decode('ascii').strip().split(' ')
    except (UnicodeDecodeError, AttributeError):
        return False
    if len(t) != 8 or t[0] != 'r1':
        return False
    _, pv, datei, sp, geraet, sek, ereignisse, her = t
    if not (re.fullmatch(r'[a-z0-9]{4,8}', pv) and re.fullmatch(r'[a-z0-9-]{1,60}\.html', datei) and sp in SPRACHEN and geraet in GERAETE
            and re.fullmatch(r'\d{1,5}', sek) and (her == '-' or re.fullmatch(r'[a-z0-9.-]{3,60}', her))):
        return False
    e = [] if ereignisse == '-' else ereignisse.split(',')
    if any(x not in EREIGNISSE for x in e) or len(e) > len(EREIGNISSE):
        return False
    sek = min(int(sek), LANG)
    n = jetzt()
    tag, uhr = n.date().isoformat(), n.strftime('%H:%M:%S')
    kz = _kuerzel(tag, ip, ua)
    land = re.sub(r'[^A-Z]', '', (land or '').upper())[:2]
    for versuch in range(7):
        with _SCHLOSS:
            d, marke = _lies(tag)
            b = d.setdefault('b', {})
            if sum(len(x.get('a') or []) for x in b.values()) >= MAX_TAG:
                return False
            g = b.get(kz)
            if g is None:
                g = b[kz] = {'l': land, 'o': _wort(ort), 'r': _wort(region, 12), 'g': geraet, 'h': '' if her == '-' else her, 'a': []}
            alt = next((x for x in g['a'] if x.get('k') == pv), None)
            if alt is None:
                if len(g['a']) >= 400:
                    return False
                g['a'].append({'k': pv, 'z': uhr, 's': datei, 'sp': sp, 'sek': sek, 'e': sorted(set(e))})
            else:
                alt['sek'] = max(int(alt.get('sek') or 0), sek)
                alt['e'] = sorted(set(alt.get('e') or []) | set(e))
            try:
                _schreib(tag, d, marke)
                return True
            except Konflikt:
                pass
        time.sleep(0.05 + random.random() * 0.3 * (versuch + 1))
    return False


# ---- Auswerten
# Herkunftsnamen des Schlössli (Master G08). Website des Hauses: schloessli-bottighofen.ch; Reservation über gastronovi; Schwesterhaus Taverne zum Schäfli
# (schaefli-wigoltingen.ch, Tisch dort über zenchef); Gemeinde Bottighofen; Bodensee- und Thurgau-Tourismus; Führer, in denen das Haus steht (GaultMillau,
# Guide Michelin, Falstaff). Reihenfolge zählt: «schloessli-bottighofen.» vor «bottighofen.ch» (sonst wird die Website des Hauses zur Gemeinde),
# «thurgau-bodensee.» vor «bodensee.».
HERKUNFT = (('google.', 'Google'), ('bing.', 'Bing'), ('duckduckgo.', 'DuckDuckGo'), ('ecosia.', 'Ecosia'), ('yahoo.', 'Yahoo'),
            ('instagram.', 'Instagram'), ('facebook.', 'Facebook'), ('linkedin.', 'LinkedIn'), ('tripadvisor.', 'Tripadvisor'),
            ('schloessli-bottighofen.', 'Website des Hauses'), ('gastronovi.', 'gastronovi (Reservation)'),
            ('schaefli-wigoltingen.', 'Taverne zum Schäfli'), ('zenchef.', 'Taverne zum Schäfli'),
            ('bottighofen.ch', 'Gemeinde Bottighofen'), ('thurgau-bodensee.', 'Thurgau Bodensee Tourismus'), ('bodensee.', 'Bodensee Tourismus'),
            ('gaultmillau.', 'GaultMillau'), ('guide.michelin.', 'Guide Michelin'), ('michelin.', 'Guide Michelin'), ('falstaff.', 'Falstaff'),
            ('excellence.ch', 'Excellence (Gourmetkreuzfahrt)'), ('myswitzerland.', 'Schweiz Tourismus'), ('sbb.ch', 'SBB'),
            ('chatgpt.', 'ChatGPT'), ('perplexity.', 'Perplexity'))


def herkunft(h):
    if not h:
        return 'Direkt aufgerufen'
    for stueck, name in HERKUNFT:
        if stueck in h:
            return name
    return h[4:] if h.startswith('www.') else h


def _sek(z):
    h, m, s = (int(x) for x in z.split(':'))
    return h * 3600 + m * 60 + s


def besuche_aus(tage_inhalt):
    """Alle Besuche aus den Tagesdateien: je Gast und Tag die Seiten nach Uhrzeit, getrennt, wo eine halbe Stunde Pause lag."""
    aus = []
    for tag in sorted(tage_inhalt):
        for g in ((tage_inhalt[tag] or {}).get('b') or {}).values():
            a = sorted((x for x in (g.get('a') or []) if isinstance(x, dict) and x.get('z') and x.get('s')), key=lambda x: x['z'])
            teil = []
            for x in a:
                if teil and _sek(x['z']) - (_sek(teil[-1]['z']) + int(teil[-1].get('sek') or 0)) > PAUSE:
                    aus.append(_besuch(tag, g, teil)); teil = []
                teil.append(x)
            if teil:
                aus.append(_besuch(tag, g, teil))
    return aus


def _besuch(tag, g, a):
    e = set(y for x in a for y in (x.get('e') or []))
    return {'tag': tag, 'z': a[0]['z'][:5], 'zs': a[0]['z'][:8], 'l': g.get('l') or '', 'o': g.get('o') or '', 'r': g.get('r') or '', 'g': g.get('g') or 'rechner',
            'sp': a[0].get('sp') or 'de', 'h': herkunft(g.get('h') or ''), 'dauer': sum(int(x.get('sek') or 0) for x in a), 'seiten': len(a),
            'buchung': bool(e & ZUR_BUCHUNG), 'anfrage': bool(e & {'tisch', 'anfrage'}), 'kontakt': bool(e & {'anruf', 'mail'}), 'chat': 'chat' in e,
            'route': 'route' in e,
            'weg': [{'z': x['z'][:5], 's': x['s'], 'sp': x.get('sp') or 'de', 'sek': int(x.get('sek') or 0), 'e': x.get('e') or []} for x in a]}


def _anteil(z, n):
    return round(min(100.0, 100.0 * z / n), 1) if n else None


def _rang(zaehler, n=12):
    return [{'k': k, 'n': v} for k, v in sorted(zaehler.items(), key=lambda x: (-x[1], str(x[0])))[:n]]


def _kurz(B):
    mit_zeit = [b['dauer'] for b in B if b['dauer'] > 0]
    seiten = sum(b['seiten'] for b in B)
    return {'besuche': len(B), 'seiten': seiten, 'buchung': sum(1 for b in B if b['buchung']), 'anfrage': sum(1 for b in B if b['anfrage']),
            'kontakt': sum(1 for b in B if b['kontakt']), 'route': sum(1 for b in B if b['route']),
            'dauer_mittel': round(sum(mit_zeit) / len(mit_zeit)) if mit_zeit else None,
            'seiten_je_besuch': round(seiten / len(B), 1) if B else None,
            'laender': len({b['l'] for b in B if b['l'] and b['l'] != '??'})}


def platz_bis(weg):
    """Stelle der Seite im Weg eines Besuchs, auf der er zur Reservation kam (Tisch angefragt oder «Direkt buchen»), sonst -1. Damit «Von der Startseite
    zur Reservation» und «Von welcher Seite reserviert wird» die ganze Vorgeschichte zeigen, zählt jede Seite, die der Besuch bis dahin ansah (Pseudo-Ereignis «platz»)."""
    return next((i for i, x in enumerate(weg) if ZUR_BUCHUNG & set(x.get('e') or [])), -1)


def werte_aus(summe):
    """Die neun Werte der Ansicht «Zur Reservation» aus den gezählten Aufrufen und Klicks (summe(ereignis, art, geraet)). Eine Rechnung für Dienst und Ablage.
    Schlössli: «zur Reservation» = im Fenster «Reservation» einen Tisch angefragt oder «Direkt buchen» (gastronovi) gewählt.
    Ohne nächsten Schritt = Fenster geöffnet, weder angefragt noch «Direkt buchen» (je Öffnen gezählt, nie unter null)."""
    def wert(z, n, **mehr):
        return dict(zahl=z, von=n, anteil=_anteil(z, n), **mehr)
    auf = summe('seite')
    return {
        'start': wert(summe('platz', 'start'), summe('seite', 'start')),   # Aufrufe der Startseite in Besuchen, die danach zur Reservation kamen
        'karte': wert(summe('platz', 'karte'), summe('seite', 'karte')),   # dasselbe für Karte und Weinkarte
        'booking': wert(summe('booking'), summe('buchung') + summe('booking'), anfrage=summe('buchung')),
        'abbruch': wert(max(0, summe('fenster') - summe('buchung') - summe('booking')), summe('fenster')),
        'tisch': wert(summe('tisch'), auf, essen=summe('tisch', 'essen')),
        'anfrage': wert(summe('anfrage'), auf, essen=summe('anfrage', 'essen'), feste=summe('anfrage', 'feste')),
        'kontakt': wert(summe('anruf') + summe('mail'), auf, anruf=summe('anruf'), mail=summe('mail')),
        'chat': wert(summe('chat'), auf),
        'route': wert(summe('route'), auf, weg=summe('route', 'weg')),
    }


def stand(tage=30, beispiel=False, ablage=False):
    """Alles, was das Besucherbuch zeigt, für die letzten Tage (heute eingeschlossen) und zum Vergleich den gleich langen Zeitraum davor.
    Nichts geschätzt: wo nichts gemessen ist, steht None."""
    try:
        tage = max(1, min(366, int(tage)))
    except (TypeError, ValueError):
        tage = 30
    bis = jetzt().date()
    von = bis - datetime.timedelta(days=tage - 1)
    liste = [(von + datetime.timedelta(days=i)).isoformat() for i in range(tage)]
    vorher_liste = [(von - datetime.timedelta(days=tage - i)).isoformat() for i in range(tage)]
    inhalt = _beispiel(vorher_liste + liste, voll=ablage) if beispiel else _tage_lesen(vorher_liste + liste)
    alle = besuche_aus(inhalt)
    hier = set(liste)
    B = [b for b in alle if b['tag'] in hier]
    V = [b for b in alle if b['tag'] not in hier]

    je_tag = {t: {'tag': t, 'besuche': 0, 'seiten': 0, 'buchung': 0} for t in liste}
    vor_tag = {t: 0 for t in vorher_liste}
    laender, orte, sprachen, geraete, her, stunden = (collections.Counter() for _ in range(6))
    raster = [[0] * 24 for _ in range(7)]
    land_tag = collections.defaultdict(collections.Counter)
    seiten = {}
    S = collections.Counter()
    for b in V:
        vor_tag[b['tag']] += 1
    for b in B:
        je_tag[b['tag']]['besuche'] += 1
        je_tag[b['tag']]['seiten'] += b['seiten']
        je_tag[b['tag']]['buchung'] += 1 if b['buchung'] else 0
        laender[b['l'] or '??'] += 1
        land_tag[b['l'] or '??'][b['tag']] += 1
        if b['o']:
            orte[(b['o'], b['l'])] += 1
        sprachen[b['sp']] += 1
        geraete[b['g']] += 1
        her[b['h']] += 1
        h = int(b['z'][:2])
        stunden[h] += 1
        raster[datetime.date.fromisoformat(b['tag']).weekday()][h] += 1
        pb = platz_bis(b['weg'])
        for i, x in enumerate(b['weg']):
            s = seiten.setdefault(x['s'], {'s': x['s'], 'n': 0, 'sek': 0, 'gemessen': 0, 'buchung': 0})
            s['n'] += 1
            if x['sek'] > 0:
                s['sek'] += x['sek']; s['gemessen'] += 1
            a = art_von(x['s'])
            S[('seite', a, b['g'])] += 1
            if i <= pb:   # diese Seite lag auf dem Weg zur Reservation
                s['buchung'] += 1
                S[('platz', a, b['g'])] += 1
            for e in x['e']:
                S[(e, a, b['g'])] += 1

    def summe(ereignis, art=None, geraet=None):
        return sum(n for (e, a, g), n in S.items() if e == ereignis and art in (None, a) and geraet in (None, g))

    heute = bis.isoformat()
    mit_daten = [t for t in liste if je_tag[t]['besuche']]
    k, kv = _kurz(B), _kurz(V)
    # Woche für Woche (Montag bis Sonntag), damit der Verlauf auch bei 90 Tagen lesbar bleibt
    wochen = collections.OrderedDict()
    for t in liste:
        d = datetime.date.fromisoformat(t)
        mo = (d - datetime.timedelta(days=d.weekday())).isoformat()
        w = wochen.setdefault(mo, {'von': t, 'bis': t, 'tage': 0, 'besuche': 0, 'buchung': 0})
        w['bis'] = t; w['tage'] += 1; w['besuche'] += je_tag[t]['besuche']; w['buchung'] += je_tag[t]['buchung']
    top = [x['k'] for x in _rang(laender, 5) if x['k'] != '??'][:4]
    aus = {
        'tage': tage, 'von': von.isoformat(), 'bis': heute, 'seit': mit_daten[0] if mit_daten else None, 'leer': not B, 'beispiel': bool(beispiel),
        'summe': dict(k, heute=je_tag[heute]['besuche']),
        'vorher': dict(kv, von=vorher_liste[0], bis=vorher_liste[-1]),
        'je_tag': [je_tag[t] for t in liste],
        'vor_tag': [vor_tag[t] for t in vorher_liste],
        'wochen': list(wochen.values()),
        'land_verlauf': [{'k': l, 'n': [land_tag[l].get(t, 0) for t in liste]} for l in top],
        'stunden': [stunden.get(h, 0) for h in range(24)],
        'raster': raster,
        'laender': _rang(laender, 20),
        'orte': [{'k': o[0], 'l': o[1], 'n': n} for o, n in sorted(orte.items(), key=lambda x: (-x[1], x[0]))[:20]],
        'sprachen': _rang(sprachen), 'geraete': _rang(geraete), 'herkunft': _rang(her, 14),
        'seiten': sorted(({'s': s['s'], 'n': s['n'], 'sek': round(s['sek'] / s['gemessen']) if s['gemessen'] else None, 'buchung': s['buchung']} for s in seiten.values()),
                         key=lambda x: (-x['n'], x['s'])),
        'werte': werte_aus(summe),
        'besuche': sorted(B, key=lambda b: (b['tag'], b['zs']), reverse=True)[:400 + (je_tag[heute]['besuche'] if ablage else 0)],   # Ablage: heute ganz dazu, registre.js kürzt
    }
    if ablage:   # was registre.js braucht, um abgelegte Beispielwerte genau auf «heute bis jetzt» zu kürzen (Carlton, Prüfung 16.10.2026)
        mz = [b['dauer'] for b in B if b['dauer'] > 0]
        aus['roh'] = {'dauer': [sum(mz), len(mz)], 'seiten_sek': {s['s']: [s['sek'], s['gemessen']] for s in seiten.values()},
                      'S': [[e, a, g, n] for (e, a, g), n in sorted(S.items())], 'laender': _rang(laender, 999), 'herkunft': _rang(her, 999),
                      'orte': [{'k': o[0], 'l': o[1], 'n': n} for o, n in sorted(orte.items(), key=lambda x: (-x[1], x[0]))],
                      'land_tag': {l: [land_tag[l].get(t, 0) for t in liste] for l in land_tag}, 'heute_voll': True}
    return aus


# ---- Beispielwerte: erfunden, damit das Haus sieht, wie das Besucherbuch mit Besuchen aussieht. Immer als Beispiel gekennzeichnet.
# Orte und Herkunft passend zu einem Restaurant am Hafen von Bottighofen (Gäste aus dem Thurgau, aus Kreuzlingen/Konstanz und von beiden Seiten des Sees,
# dazu Zürich und St. Gallen); keine echten Zahlen des Hauses. Besuche vor allem am Vormittag und am Nachmittag vor dem Essen, Karte und Reservation
# werden oft gelesen, am Wochenende mehr.
def _beispiel(liste, voll=False):
    jt = jetzt()
    heute, jetzt_sek = jt.date(), jt.hour * 3600 + jt.minute * 60 + jt.second
    orte = [('CH', 'Kreuzlingen', 'TG', 'de', 14), ('CH', 'Bottighofen', 'TG', 'de', 4), ('CH', 'Münsterlingen', 'TG', 'de', 3), ('CH', 'Romanshorn', 'TG', 'de', 4),
            ('CH', 'Frauenfeld', 'TG', 'de', 5), ('CH', 'Weinfelden', 'TG', 'de', 4), ('CH', 'Amriswil', 'TG', 'de', 3), ('CH', 'Arbon', 'TG', 'de', 2),
            ('CH', 'St. Gallen', 'SG', 'de', 7), ('CH', 'Zürich', 'ZH', 'de', 12), ('CH', 'Winterthur', 'ZH', 'de', 5), ('CH', 'Schaffhausen', 'SH', 'de', 2),
            ('CH', 'Basel', 'BS', 'de', 2), ('CH', 'Bern', 'BE', 'de', 2), ('CH', 'Lausanne', 'VD', 'fr', 1), ('DE', 'Konstanz', 'BW', 'de', 9),
            ('DE', 'Friedrichshafen', 'BW', 'de', 2), ('DE', 'Stuttgart', 'BW', 'de', 2), ('DE', 'München', 'BY', 'de', 2), ('DE', 'Lindau', 'BY', 'de', 1),
            ('AT', 'Bregenz', '8', 'de', 2), ('AT', 'Wien', '9', 'de', 1), ('IT', 'Milano', '25', 'it', 1), ('GB', 'London', 'ENG', 'en', 1), ('FR', 'Paris', 'IDF', 'fr', 1)]
    her = [('', 28), ('www.google.ch', 32), ('www.google.com', 4), ('www.google.de', 4), ('www.instagram.com', 6), ('www.gaultmillau.ch', 4),
           ('guide.michelin.com', 3), ('www.schaefli-wigoltingen.ch', 3), ('www.tripadvisor.ch', 3), ('www.bottighofen.ch', 2),
           ('www.thurgau-bodensee.ch', 2), ('www.facebook.com', 2), ('www.falstaff.com', 1), ('www.bing.com', 1), ('chatgpt.com', 1)]
    karte = ['karte.html', 'weinkarte.html']
    rest = ['kontakt.html', 'feiern.html', 'anlaesse.html', 'team.html', 'abend.html', 'gutschein.html', 'impressum.html', 'datenschutz.html']
    gew = lambda l: z.choices(l, weights=[x[-1] for x in l])[0]   # z ist der Zufall des jeweiligen Tages
    aus = {}
    for tag in liste:
        d = datetime.date.fromisoformat(tag)
        z = random.Random('schloessli-bottighofen-' + tag)   # je Tag fest: derselbe Tag zeigt in 7, 30 und 90 Tagen dieselben Besuche
        wt, alter = d.weekday(), (heute - d).days
        n = int(26 * (1 - alter / 300) * (1.4 if wt in (3, 4) else 1.25 if wt == 5 else 0.85 if wt in (0, 1) else 1.0) * z.uniform(0.75, 1.25))
        b = {}
        for j in range(n):
            land, ort, region, sp, _ = gew(orte)
            geraet = z.choices(GERAETE, weights=(64, 6, 30))[0]
            t = beginn = int(z.triangular(7.0, 23.0, 16.5) * 3600)
            weg = ['index.html'] if z.random() < 0.68 else [z.choice(karte + rest[:4])]
            for _ in range(z.choices(range(0, 8), weights=(20, 22, 20, 14, 10, 7, 4, 3))[0]):
                w = z.random()
                neu = z.choice(karte) if w < 0.34 else z.choice(rest[:6]) if w < 0.92 else z.choice(rest)
                if neu != weg[-1]:   # dieselbe Seite nie zweimal hintereinander
                    weg.append(neu)
            a = []
            for s in weg:
                art = art_von(s)
                sek = int(z.triangular(6, 170, 30)) + (int(z.uniform(30, 150)) if art == 'karte' else 0)
                e = []
                if art in ('karte', 'start', 'weg') and z.random() < (0.15 if art == 'karte' else 0.09):
                    e = ['fenster']
                    r = z.random()
                    if r < 0.38:
                        e += ['buchung']
                    elif r < 0.62:
                        e += ['booking']
                elif art == 'essen' and z.random() < 0.16:
                    e = ['tisch'] + (['anfrage'] if z.random() < 0.45 else [])
                elif art == 'feste' and z.random() < 0.14:
                    e = ['anfrage']
                elif s == 'kontakt.html' and z.random() < 0.3:
                    e = [z.choice(['route', 'route', 'anruf', 'anruf', 'mail'])]
                elif art == 'erleben' and z.random() < 0.06:
                    e = [z.choice(['anruf', 'mail'])]
                elif s == 'team.html' and z.random() < 0.12:
                    e = ['chat']
                a.append({'k': 'b%03d%02d' % (j, len(a)), 'z': '%02d:%02d:%02d' % (t // 3600 % 24, t // 60 % 60, t % 60), 's': s, 'sp': sp, 'sek': sek, 'e': sorted(set(e))})
                t += sek + z.randint(1, 4)
                if t >= 24 * 3600 - 5 or ZUR_BUCHUNG & set(e):
                    break
            h = gew(her)[0]
            # heute nur bis jetzt; erst nach dem ganzen Besuch weggelassen, damit der Zufall der folgenden Besuche gleich bleibt
            # (die Ablage nimmt den ganzen Tag, registre.js kürzt beim Anzeigen genau gleich, Carlton-Prüfung 16.10.2026)
            if alter == 0 and beginn > jetzt_sek and not voll:
                continue
            b['bsp%04d' % j] = {'l': land, 'o': ort, 'r': region, 'g': geraet, 'h': h, 'a': a}
        aus[tag] = {'b': b}
    return aus


def ausfuhr(tage=30):
    """Alle Besuche der letzten Tage (heute eingeschlossen), neueste zuerst, ohne Obergrenze: für «Als Tabelle sichern» (Datenexport, Master 9d Punkt 21).
    Dieselben Angaben wie im Werkzeug, kein Kürzel, keine Adresse."""
    try:
        tage = max(1, min(AUFBEWAHREN, int(tage)))
    except (TypeError, ValueError):
        tage = 30
    bis = jetzt().date()
    liste = [(bis - datetime.timedelta(days=tage - 1 - i)).isoformat() for i in range(tage)]
    B = besuche_aus(_tage_lesen(liste))
    return {'tage': tage, 'von': liste[0], 'bis': liste[-1], 'besuche': sorted(B, key=lambda b: (b['tag'], b['zs']), reverse=True)}


def ablage_heute(tage=30, heute=None, uhr=None):
    """Die abgelegten Beispielwerte (beispiel/<tage>.json), auf heute geschoben und auf die jetzige Uhrzeit in Bottighofen (Europe/Zurich) gekürzt.
    Dieselbe Rechnung wie registre.js (ablageLaden, kuerzen), damit das Besucherbuch und die Stube dieselben Beispielzahlen zeigen.
    Fehlt die Datei: Beispielwerte frisch gerechnet (stand)."""
    try:
        tage = int(tage)
    except (TypeError, ValueError):
        tage = 30
    p = os.path.join(HIER, 'beispiel', f'{tage}.json')
    if tage not in (7, 30, 90) or not os.path.exists(p):
        return stand(tage, beispiel=True)
    d = json.load(open(p, encoding='utf-8'))
    n = jetzt()
    heute = heute or n.date().isoformat()
    uhr = uhr or n.strftime('%H:%M:%S')
    um = (datetime.date.fromisoformat(heute) - datetime.date.fromisoformat(d['bis'])).days
    sch = lambda t: (datetime.date.fromisoformat(t) + datetime.timedelta(days=um)).isoformat()
    if um:
        for k in ('von', 'bis', 'seit'):
            if d.get(k):
                d[k] = sch(d[k])
        d['vorher']['von'], d['vorher']['bis'] = sch(d['vorher']['von']), sch(d['vorher']['bis'])
        for t in d['je_tag']:
            t['tag'] = sch(t['tag'])
        for b in d['besuche']:
            b['tag'] = sch(b['tag'])
        r7 = list(d['raster'])
        d['raster'] = [r7[(w - um) % 7] for w in range(7)]
    R = d.pop('roh', None)
    if R and R.get('heute_voll'):
        _kuerzen(d, R, uhr)
    wochen = collections.OrderedDict()
    for t in d['je_tag']:
        dd = datetime.date.fromisoformat(t['tag'])
        mo = (dd - datetime.timedelta(days=dd.weekday())).isoformat()
        w = wochen.setdefault(mo, {'von': t['tag'], 'bis': t['tag'], 'tage': 0, 'besuche': 0, 'buchung': 0})
        w['bis'] = t['tag']; w['tage'] += 1; w['besuche'] += t['besuche']; w['buchung'] += t['buchung']
    d['wochen'] = list(wochen.values())
    return d


def _kuerzen(d, R, uhr):
    u, L, heute = d['summe'], len(d['je_tag']) - 1, d['bis']
    weg = [b for b in d['besuche'] if b['tag'] == heute and (b.get('zs') or b['z'] + ':00') > uhr]
    if not weg:
        d['besuche'] = d['besuche'][:400]
        return

    def minus(liste, k, l=None):
        for x in liste:
            if x['k'] == k and (l is None or x.get('l') == l):
                x['n'] -= 1
                return
    SS = collections.Counter({(e, a, g): z for e, a, g, z in R['S']})
    wtag = datetime.date.fromisoformat(heute).weekday()
    for b in weg:
        u['besuche'] -= 1; u['seiten'] -= b['seiten']; u['heute'] -= 1
        u['buchung'] -= 1 if b['buchung'] else 0; u['anfrage'] -= 1 if b['anfrage'] else 0; u['kontakt'] -= 1 if b['kontakt'] else 0; u['route'] -= 1 if b.get('route') else 0
        if b['dauer'] > 0:
            R['dauer'][0] -= b['dauer']; R['dauer'][1] -= 1
        t = d['je_tag'][L]; t['besuche'] -= 1; t['seiten'] -= b['seiten']; t['buchung'] -= 1 if b['buchung'] else 0
        l = b['l'] or '??'
        minus(R['laender'], l)
        if l in R['land_tag']:
            R['land_tag'][l][L] -= 1
        if b['o']:
            minus(R['orte'], b['o'], b['l'])
        minus(d['sprachen'], b['sp']); minus(d['geraete'], b['g']); minus(R['herkunft'], b['h'])
        h = int(b['z'][:2]); d['stunden'][h] -= 1; d['raster'][wtag][h] -= 1
        pb = platz_bis(b['weg'])
        for i, x in enumerate(b['weg']):
            for s in d['seiten']:
                if s['s'] == x['s']:
                    s['n'] -= 1; s['buchung'] -= 1 if i <= pb else 0
                    break
            if x['sek'] > 0 and x['s'] in R['seiten_sek']:
                R['seiten_sek'][x['s']][0] -= x['sek']; R['seiten_sek'][x['s']][1] -= 1
            a = art_von(x['s'])
            for e in ['seite'] + list(x['e']) + (['platz'] if i <= pb else []):
                SS[(e, a, b['g'])] -= 1
    ids = {id(b) for b in weg}
    d['besuche'] = [b for b in d['besuche'] if id(b) not in ids][:400]
    u['dauer_mittel'] = round(R['dauer'][0] / R['dauer'][1]) if R['dauer'][1] else None
    u['seiten_je_besuch'] = round(u['seiten'] / u['besuche'], 1) if u['besuche'] else None
    u['laender'] = len([x for x in R['laender'] if x['n'] > 0 and x['k'] not in ('??', '')])
    rang = lambda l, n: sorted((x for x in l if x['n'] > 0), key=lambda x: (-x['n'], str(x['k'])))[:n]
    d['laender'], d['herkunft'] = rang(R['laender'], 20), rang(R['herkunft'], 14)
    d['sprachen'], d['geraete'] = rang(d['sprachen'], 12), rang(d['geraete'], 12)
    d['orte'] = sorted((x for x in R['orte'] if x['n'] > 0), key=lambda x: (-x['n'], x['k'], x['l']))[:20]
    for s in d['seiten']:
        q = R['seiten_sek'].get(s['s'])
        s['sek'] = round(q[0] / q[1]) if q and q[1] else None
    d['seiten'] = sorted((s for s in d['seiten'] if s['n'] > 0), key=lambda x: (-x['n'], x['s']))
    top = [x['k'] for x in rang(R['laender'], 5) if x['k'] != '??'][:4]
    d['land_verlauf'] = [{'k': k, 'n': R['land_tag'].get(k) or [0] * (L + 1)} for k in top]

    def summe(e, a=None, g=None):
        return sum(z for (e2, a2, g2), z in SS.items() if e2 == e and a in (None, a2) and g in (None, g2))
    d['werte'] = werte_aus(summe)
    mit = [t['tag'] for t in d['je_tag'] if t['besuche']]
    d['seit'], d['leer'] = (mit[0] if mit else None), not u['besuche']


def ablage():
    """beispiel/<tage>.json: dieselben Beispielwerte als Dateien, für ein Werkzeug ohne Server-Teil (registre.js verschiebt die Tage auf heute)."""
    p = os.path.join(HIER, 'beispiel')
    os.makedirs(p, exist_ok=True)
    for t in (7, 30, 90):
        json.dump(stand(t, beispiel=True, ablage=True), open(os.path.join(p, f'{t}.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return p


# Gäste-, Fremd- oder KI-Bilder (UEBERGABE.md, Rechte): nie als Hausbild einer Seite; dazu das allgemeine Startfoto der Terrasse
FREMD = ('start', 'tb-', 'kf-', 'feuerwerk', 'ch-', 'ig-')


def seiten_namen():
    """seiten.json: Datei → Name der Seite, aus den Titeln der Seiten, die die Startseite des Schlössli verlinkt (Leiste, Menü, Fuss).
    «Banketts &amp; Gruppen · Wirtschaft am Schlössli» → «Banketts & Gruppen»; die Startseite heisst «Startseite». Nichts abgetippt."""
    import html
    wurzel = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website')   # Schlössli: die Website liegt in website/ neben _werkzeuge/
    start = open(os.path.join(wurzel, 'index.html'), encoding='utf-8').read()
    dateien = ['index.html'] + sorted(set(re.findall(r'href="([a-z0-9-]+\.html)"', start)) - {'index.html'})
    namen = {}
    for n in dateien:
        try:
            m = re.search(r'<title>(.*?)</title>', open(os.path.join(wurzel, n), encoding='utf-8').read(), re.S)
        except OSError:
            continue
        teile = [x.strip() for x in re.split(r' [·|–—] ', html.unescape(m.group(1)))] if m else [n]
        namen[n] = ' · '.join(teile[:-1]) if len(teile) > 1 else teile[0]
    namen['index.html'] = 'Startseite'
    p = os.path.join(HIER, 'seiten.json')
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        json.dump(namen, f, ensure_ascii=False, indent=1)
    os.replace(p + '.neu', p)
    # Bild je Seite (Fehlerbuch 10a, Robert 19.10.2026: jede Liste in jedem Werkzeug zeigt zu jedem Eintrag sein Bild): das erste Foto im Inhalt der Seite,
    # das ein eigenes Foto des Hauses ist (inhalt/bilder.json ohne fremden Nachweis, kein KI-Platzhalter, kein Logo), nicht das allgemeine Startfoto der Terrasse
    # und nicht schon bei einer anderen Seite (sonst sehen vier Seiten gleich aus); sonst das Haus von aussen. Kleine Fassung (480).
    try:
        bj = json.load(open(os.path.join(wurzel, 'inhalt', 'bilder.json'), encoding='utf-8'))
    except (OSError, ValueError):
        bj = {}
    bilder = {}
    for n in namen:
        try:
            h = open(os.path.join(wurzel, n), encoding='utf-8').read()
        except OSError:
            continue
        m = re.search(r'<main.*', h, re.S)
        # ohne eigenes Foto im Inhalt: das nächste freie Foto des Hauses (Bar, Regal, Wein, Apéro …), nie eins doppelt
        wahl = next((x for x in ('regal', 'bar', 'wein', 'apero', 'fliesen', 'abend', 'haus') if 'assets/img/' + x + '-480.webp' not in bilder.values()), 'haus')
        for b in re.findall(r'assets/img/([a-z0-9-]+?)-\d+\.webp', m.group(0) if m else h):
            e = bj.get(b)
            if e and e.get('nachweis') is None and not str(e.get('datei') or '').startswith('extern/') and not b.endswith('-ki') and not b.startswith(FREMD) and b not in ('baum', 'pa-teller', 'kp-party') and 'assets/img/' + b + '-480.webp' not in bilder.values() and os.path.exists(os.path.join(wurzel, 'assets', 'img', b + '-480.webp')):
                wahl = b
                break
        bilder[n] = 'assets/img/' + wahl + '-480.webp'
    with open(os.path.join(HIER, 'seiten-bilder.json'), 'w', encoding='utf-8') as f:
        json.dump(bilder, f, ensure_ascii=False, indent=1)
    return namen


def leeren():
    """Zählung lokal leeren: der bisherige Ordner bleibt als <ordner>.vor-leeren liegen (eine Fassung zurück)."""
    import shutil
    with _SCHLOSS:
        if os.path.isdir(ORDNER):
            ziel = ORDNER + '.vor-leeren'
            shutil.rmtree(ziel, ignore_errors=True)
            os.replace(ORDNER, ziel)
        os.makedirs(ORDNER, exist_ok=True)


def aufraeumen():
    grenze = (jetzt().date() - datetime.timedelta(days=AUFBEWAHREN)).isoformat()
    weg = 0
    if os.path.isdir(ORDNER):
        for f in os.listdir(ORDNER):
            if re.fullmatch(r'\d{4}-\d\d-\d\d\.json', f) and f[:10] < grenze:
                os.remove(os.path.join(ORDNER, f)); weg += 1
    return weg


if __name__ == '__main__':
    was = sys.argv[1] if len(sys.argv) > 1 else ''
    if was == 'ablage':
        print('Beispielwerte abgelegt:', ablage())
    elif was == 'seiten':
        print(len(seiten_namen()), 'Seiten →', os.path.join(HIER, 'seiten.json'))
    elif was == 'leeren':
        leeren(); print('Zählung geleert:', ORDNER)
    elif was == 'aufraeumen':
        print(aufraeumen(), 'Tagesdateien gelöscht (älter als', AUFBEWAHREN, 'Tage)')
    else:
        d = stand(30, beispiel=(was == 'beispiel'))
        d['besuche'] = d['besuche'][:3]
        print(json.dumps({k: d[k] for k in ('tage', 'von', 'bis', 'beispiel', 'summe', 'vorher', 'besuche')}, ensure_ascii=False, indent=1))
