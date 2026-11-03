"""Die Tafel (La Carte) · Wirtschaft am Schlössli online (19.10.2026, aus der Tafel des Gasterntal) (Vercel-Funktion, Python; 17.10.2026, Kopie aus der Tafel des Landgasthof Ruedihus, dort aus dem Waldhotel Doldenhorn und La Carte des Carlton-Europe vom 16.10.2026). Liegt online als api/carte.py, vercel.json schreibt
/_werkzeuge/carte/api/<was> auf /api/carte?__weg=/_werkzeuge/carte/api/<was> um (Andock-Datei _werkzeuge/carte/online.json).

Dieselbe Logik wie auf dem Rechner des Hauses: carte.py (api/_lib/carte/carte.py) arbeitet mit Dateien in einem Ordner unter /tmp. Diesen Ordner
hält der private Blob als EINE gepackte Ablage («carte»: Stand, Entwürfe, Verlauf, Protokoll, Einstellungen, Stand des Veröffentlichens), siehe
_speicher.py. Jede Anfrage entfaltet die Ablage, arbeitet und schreibt sie, wenn sich etwas geändert hat, mit Etag zurück (zwei Schreiber
gleichzeitig: der Zweite bekommt KONFLIKT, nichts wird still überschrieben). Die PDFs liegen einzeln im privaten Blob unter carte/pdf/<art>/<karte>.pdf
(live, probe, verlauf/<karte>/<zeit>.pdf), weil sie für die Ablage zu gross sind; ausgeliefert werden sie über /_werkzeuge/carte/api/pdf.

Unterschiede zum Rechner des Hauses:
- Druck: Chromium läuft nicht in Python. Probe und Veröffentlichen rufen die Node-Funktion api/carte_druck.js (Schlüssel aus dem Speicher-Schlüssel
  abgeleitet, damit niemand sonst drucken lässt); sie setzt blatt.html mit den Daten des Entwurfs und gibt die PDF zurück.
- «PDF = Daten»: statt pdftotext liest PyMuPDF den Text der gedruckten PDF; derselbe Vergleich wie carte.pdf_gleich_daten.
- Veröffentlichen läuft in der Anfrage selbst (kein Hintergrund-Faden, die Instanz kann danach eingefroren werden); der Fortschritt steht in bau.json
  der Ablage, La Carte fragt ihn wie lokal über «status» ab.
- Anschluss an die Website (PDF nach unterlagen/pdf/ und assets/pdf/, Zeilen auf «Ässe u trinke», Picknick, Startseite) gibt es online nicht: die Website wird lokal gebaut und hochgeladen,
  die Weiche liefert unterlagen/pdf/ nicht aus dem Speicher. Schalter bleibt aus. Ansicht «Website» zeigt online die Seite, wie sie ist.
- Keine tägliche Archiv-Sicherung: der Blob ist der Speicher, jede Veröffentlichung bleibt im Verlauf.
Sicherheit wie serve.py: schreibende Wege nur von der eigenen Seite (Origin = Host), nur JSON, höchstens 3 MB, Grenzen je Absender und Minute (je Instanz),
Rollen und Prüfung jeder Eingabe in carte.py."""
import base64, hashlib, json, os, shutil, sys, threading, time, traceback, urllib.error, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import _speicher as SP  # noqa: E402

LIB = os.path.join(HIER, '_lib', 'carte')
ORDNER = os.path.join(SP.TMP, 'carte')
os.environ['CARTE_DATEN'] = ORDNER
sys.path.insert(0, LIB)
import carte as C  # noqa: E402

WURZEL = '/_werkzeuge/carte/api/'
GROSS = 3_000_000
GRENZEN = {'alle': 900, 'schreiben': 60, 'druck': 8}
_ZAEHLER, _ZSCHLOSS, _SCHLOSS = {}, threading.Lock(), threading.Lock()
OHNE = ('grundstand', 'live', 'probe', 'sicherung')   # nicht in der Ablage: Grundstand liegt in der Funktion, PDFs einzeln im Blob
SCHLUESSEL = hashlib.sha256(('carte-druck|' + (SP.TOKEN or os.environ.get('VERCEL_DEPLOYMENT_ID', '') or 'lokal')).encode('utf-8')).hexdigest()


def zu_viel(wer, art):
    jetzt = time.time()
    with _ZSCHLOSS:
        liste = [t for t in _ZAEHLER.get((wer, art), []) if jetzt - t < 60]
        voll = len(liste) >= GRENZEN[art]
        if not voll:
            liste.append(jetzt)
        _ZAEHLER[(wer, art)] = liste
        return voll


def _pdf_blob(rel):
    return 'carte/pdf/' + rel.replace(os.sep, '/')


def _ablage():
    """Ablage entfalten; beim allerersten Mal mit dem ausgelieferten Stand füllen. Grundstand immer aus der Funktion."""
    os.makedirs(ORDNER, exist_ok=True)
    a = SP.Ablage('carte', ORDNER, ohne=OHNE)
    daten = a.laden()
    if not any(k.startswith('stand/') for k in daten):
        for teil in ('stand', 'einstellungen.json'):
            q = os.path.join(LIB, '_daten', teil)
            if os.path.isdir(q):
                shutil.copytree(q, os.path.join(ORDNER, teil), dirs_exist_ok=True)
            elif os.path.isfile(q):
                shutil.copy2(q, os.path.join(ORDNER, teil))
    g = os.path.join(ORDNER, 'grundstand')
    shutil.rmtree(g, ignore_errors=True)
    shutil.copytree(os.path.join(LIB, '_daten', 'grundstand'), g)
    for t in ('live', 'probe'):
        shutil.rmtree(os.path.join(ORDNER, t), ignore_errors=True)
    try:
        C.BAU.clear()
        C.BAU.update(json.load(open(os.path.join(ORDNER, 'bau.json'), encoding='utf-8')))
    except (OSError, ValueError):
        C.BAU.clear()
        C.BAU.update(laeuft=False, ziel='', schritt='', schritte=[], fehler='', fertig='', start=0, ende=0, bericht={})
    if C.BAU.get('laeuft') and time.time() - (C.BAU.get('start') or 0) > 330:   # hängengebliebene Veröffentlichung (Funktion abgebrochen)
        C.BAU.update(laeuft=False, schritt='', fehler='Das Veröffentlichen wurde unterbrochen. Es wurde nichts geändert.', ende=time.time())
    return a


def _bau_merken():
    with open(os.path.join(ORDNER, 'bau.json'), 'w', encoding='utf-8') as f:
        json.dump(C.BAU, f, ensure_ascii=False)


def _pdfs_hoch():
    """Jede PDF, die carte.py in den Ordner gelegt hat (live, probe, verlauf), einzeln in den privaten Blob; danach aus dem Ordner."""
    for w, _, fs in os.walk(ORDNER):
        for f in fs:
            if f.endswith('.pdf'):
                p = os.path.join(w, f)
                SP.put(_pdf_blob(os.path.relpath(p, ORDNER)), open(p, 'rb').read(), 'application/pdf', 'private')
                os.remove(p)


def _pdfzeit(z):
    try:
        return json.load(open(os.path.join(ORDNER, 'pdfzeit.json'), encoding='utf-8')).get(z, '')
    except (OSError, ValueError):
        return ''


# ---------------------------------------------------------------- carte.py für online: Druck, PDF-Prüfung, Anschluss, Status
_BASIS = threading.local()


def drucke(z, art, aus):
    """Wie carte.drucke, aber über die Node-Funktion api/carte_druck.js (Chromium). art: 'stand' | 'entwurf'."""
    if art == 'entwurf':
        k = C.karte(z)
        d = k['entwurf'] or k['stand']
    else:
        d = C.karte(z)['stand']
    roh = json.dumps({'z': z, 'daten': d}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(_BASIS.wert + '/api/carte_druck', data=roh, method='POST',
                                 headers={'content-type': 'application/json', 'x-carte-druck': SCHLUESSEL})
    try:
        with urllib.request.urlopen(req, timeout=200) as r:
            antwort = json.load(r)
    except urllib.error.HTTPError as e:
        text = e.read().decode('utf-8', 'replace')[:300]
        C.fehler_log(f'Druck {z} online gescheitert: {e.code} {text}')
        raise C.Fehler('DRUCK', 'Die PDF liess sich nicht drucken. ' + (json.loads(text).get('fehler', '') if text.startswith('{') else ''), 500)
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        C.fehler_log(f'Druck {z} online gescheitert: {e!r}')
        raise C.Fehler('DRUCK', 'Die PDF liess sich nicht drucken (keine Antwort vom Druck).', 500)
    os.makedirs(os.path.dirname(aus), exist_ok=True)
    with open(aus, 'wb') as f:
        f.write(base64.b64decode(antwort['pdf']))
    return antwort.get('bericht') or {}


def pdf_gleich_daten(d, pdf):
    """Wie carte.pdf_gleich_daten, Text der PDF mit PyMuPDF statt pdftotext (derselbe Vergleich, carte.pdf_gleich_text)."""
    try:
        import pymupdf as fitz
    except ImportError:
        raise C.Fehler('PRUEFWERK', 'Das Prüfprogramm für die PDF fehlt. Ohne die Prüfung wird nichts veröffentlicht.', 500)
    with fitz.open(pdf) as doc:
        return C.pdf_gleich_text(d, '\n'.join(s.get_text() for s in doc))


def _anschluss(z, live):
    return 'aus'


def setze_einstellungen(d, wer, rolle):
    C._recht(rolle, 'einstellungen')
    if d.get('anschluss_pdf'):
        raise C.Fehler('ONLINE', 'Der Anschluss an die Website lässt sich nur auf dem Rechner des Hauses einschalten.')
    return C.einstellungen()


def gesund():
    pruef = {}
    for z in C.ZIELE:
        try:
            pruef[z] = bool(C._lies(C._p('stand', z)))
        except C.Fehler:
            pruef[z] = False
    try:
        import pymupdf  # noqa: F401
        pdfpruef = True
    except ImportError:
        pdfpruef = False
    groesse = sum(os.path.getsize(os.path.join(w, f)) for w, _, fs in os.walk(ORDNER) for f in fs)
    try:
        with open(os.path.join(ORDNER, 'fehler.log'), encoding='utf-8') as f:
            fehler = [x.rstrip() for x in f.readlines()[-5:]]
    except OSError:
        fehler = []
    werkzeug = {'speicher': SP.bereit() and not SP.DEMO, 'druck': True, 'pdfpruefung': pdfpruef}
    return dict(ok=all(pruef.values()) and all(werkzeug.values()), karten=pruef, werkzeug=werkzeug, speicher_mb=round(groesse / 1e6, 2),
                seit=int(time.time() - C.START), fehler=fehler, browserfehler=C.browserfehler_lesen(), online=True, vorfuehrung=SP.DEMO)


_reparatur_lokal = C.reparatur


def reparatur(d, wer, rolle):
    """Online: keine Archiv-Sicherung (der Blob ist der Speicher), Probe-PDFs liegen im Blob und werden beim nächsten Druck ersetzt."""
    C._recht(rolle, 'reparatur')
    if d.get('art') in ('sicherung', 'probe'):
        raise C.Fehler('ONLINE', 'Das gibt es nur auf dem Rechner des Hauses. Online ist der Speicher selbst die Sicherung; jede Veröffentlichung bleibt unter «Frühere Fassungen».')
    return _reparatur_lokal(d, wer, rolle)


C.drucke, C.pdf_gleich_daten, C._anschluss, C.setze_einstellungen, C.gesund, C.reparatur = drucke, pdf_gleich_daten, _anschluss, setze_einstellungen, gesund, reparatur
_status_lokal = C.status


def status():
    s = _status_lokal()
    for k in s['karten']:
        k['pdf_zeit'] = _pdfzeit(k['ziel'])
    s['online'] = True
    return s


C.status = status


def veroeffentlichen(z, wer, rolle):
    """Wie carte.veroeffentlichen, aber in der Anfrage selbst; Fortschritt in bau.json der Ablage."""
    C._ziel(z)
    C._recht(rolle, 'veroeffentlichen', z)
    if C.BAU.get('laeuft'):
        raise C.Fehler('BAU', 'Gerade wird schon eine Karte veröffentlicht. Bitte kurz warten.', 409)
    e, s = C._lies(C._p('entwurf', z)), C._lies(C._p('stand', z))
    if not e or C._inhalt(e) == C._inhalt(s):
        return dict(ok=True, geaendert=False)
    f = C.pruefe(e, z)
    if f:
        raise C.Fehler('PRUEF', f)
    C.BAU.update(laeuft=True, ziel=z, schritt=C.SCHRITTE[0], schritte=C.SCHRITTE, fehler='', fertig='', start=time.time(), ende=0, bericht={})
    _bau_merken()
    _AKTUELL.a.sichern()   # die anderen Instanzen sehen: es läuft
    live = SP.get(_pdf_blob(f'live/{z}.pdf'))   # die bisherige PDF kommt so in den Verlauf (carte.py kopiert live → verlauf)
    if live:
        os.makedirs(os.path.join(ORDNER, 'live'), exist_ok=True)
        open(os.path.join(ORDNER, 'live', z + '.pdf'), 'wb').write(live)
    C._veroeffentlichen(z, e, s, wer, rolle)   # fängt jeden Fehler selbst ab und trägt ihn in BAU ein (nichts ausgetauscht)
    if not C.BAU.get('fehler'):
        zeiten = {}
        try:
            zeiten = json.load(open(os.path.join(ORDNER, 'pdfzeit.json'), encoding='utf-8'))
        except (OSError, ValueError):
            pass
        zeiten[z] = time.strftime('%d.%m.%Y %H:%M')
        with open(os.path.join(ORDNER, 'pdfzeit.json'), 'w', encoding='utf-8') as fh:
            json.dump(zeiten, fh)
    _pdfs_hoch()
    _bau_merken()
    return dict(ok=True, gestartet=True, fertig=not C.BAU.get('fehler'), fehler=C.BAU.get('fehler', ''))


_AKTUELL = threading.local()


class handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _sende(self, status, daten, typ='application/json; charset=utf-8', mehr=None):
        roh = daten if isinstance(daten, bytes) else json.dumps(daten, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', typ)
        self.send_header('Content-Length', str(len(roh)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        for k, v in (mehr or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(roh)

    def _fehler(self, status, stichwort, text):
        return self._sende(status, {'fehler': text, 'stichwort': stichwort})

    def _ip(self):
        return (self.headers.get('x-forwarded-for') or self.client_address[0] or '').split(',')[0].strip()

    def _wer(self):
        return urllib.parse.unquote(self.headers.get('X-Carte-Wer') or '').strip()[:60], (self.headers.get('X-Carte-Rolle') or '').strip()[:20]

    def _was(self):
        pfad, q = SP.weg_von(self.path)
        return (pfad[len(WURZEL):] if pfad.startswith(WURZEL) else ''), q

    def _lauf(self, fn, schreiben):
        """fn() gibt (status, daten[, typ, mehr]) zurück; geantwortet wird erst, wenn die Ablage zurückgeschrieben ist."""
        with _SCHLOSS:   # eine Anfrage je Instanz zugleich: alle teilen sich den Ordner unter /tmp
            try:
                if not SP.bereit():
                    return self._fehler(500, 'SPEICHER', 'Kein Speicher eingerichtet (BLOB_READ_WRITE_TOKEN fehlt beim Vercel-Projekt).')
                _BASIS.wert = (self.headers.get('x-forwarded-proto') or 'https') + '://' + (self.headers.get('host') or '')
                _AKTUELL.a = _ablage()
                r = fn()
                if schreiben:
                    _AKTUELL.a.sichern(zusammenfuehren=False)
            except SP.Konflikt:
                return self._fehler(409, 'KONFLIKT', 'Inzwischen hat jemand anderes La Carte geändert. Bitte neu laden; Ihre Eingabe ist nicht verloren, sie steht noch im Fenster.')
            except C.Fehler as e:
                try:
                    if schreiben:
                        _AKTUELL.a.sichern(zusammenfuehren=True)   # Protokoll und Fehlerprotokoll bleiben
                except Exception:  # noqa: BLE001
                    pass
                return self._fehler(e.status, e.stichwort, e.text)
            except SP.Fehler as e:
                return self._fehler(500, 'SPEICHER', str(e).replace('SPEICHER · ', ''))
            except Exception as e:  # noqa: BLE001
                try:
                    C.fehler_log(f'online {self.command} {self.path}: {e!r} {traceback.format_exc()[-500:]}')
                except Exception:  # noqa: BLE001
                    pass
                return self._fehler(500, 'SERVER', 'Im Server ist etwas schiefgegangen. Es steht im Fehlerprotokoll.')
        if r[0] == 302:
            self.send_response(302)
            self.send_header('Location', r[1])
            self.send_header('Content-Length', '0')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            return None
        return self._sende(*r)

    def do_GET(self):
        was, q = self._was()
        if zu_viel(self._ip(), 'alle'):
            return self._fehler(429, 'GRENZE', 'Zu viele Anfragen in kurzer Zeit. Bitte eine Minute warten.')
        wer, rolle = self._wer()

        def tun():
            if was == 'pdf':
                return self._pdf(q)
            if was == 'druckdaten':
                z, art = (q.get('z') or [''])[0], (q.get('q') or ['stand'])[0]
                C._ziel(z)
                if art == 'entwurf':
                    k = C.karte(z)
                    d = k['entwurf'] or k['stand']
                elif art == 'grundstand':
                    d = C.grundstand(z)
                elif art.startswith('verlauf:'):
                    d = C.version(z, art[8:])
                else:
                    d = C.karte(z)['stand']
                return (200, d)
            if was == 'webseite':   # online ohne Bau des Hauses: die Seite, wie sie ist
                seite = (q.get('seite') or [''])[0]
                return (302, '/' + (seite if seite.replace('-', '').replace('.html', '').isalnum() else ''))
            if was == 'export':
                return (200, json.dumps(C.export(), ensure_ascii=False, indent=1).encode('utf-8'), 'application/json; charset=utf-8',
                        {'Content-Disposition': time.strftime('attachment; filename="die-tafel-wirtschaft-am-schloessli-%Y-%m-%d.json"')})
            return (200, C.get(was, q, wer, rolle))
        return self._lauf(tun, False)

    def _pdf(self, q):
        z, art = (q.get('z') or [''])[0], (q.get('q') or ['live'])[0]
        C._ziel(z)
        if art not in ('live', 'probe'):
            raise C.Fehler('DATEI', 'Diese PDF gibt es nicht.', 404)
        b = SP.get(_pdf_blob(f'{art}/{z}.pdf'))
        if b is None:
            if art == 'live' and z != 'mittag':   # noch nichts veröffentlicht: die PDF, die heute auf der Website liegt
                return (302, f'/unterlagen/pdf/{z}.pdf')
            raise C.Fehler('DATEI', 'Diese PDF gibt es noch nicht. Sie entsteht beim ersten Veröffentlichen.' if art == 'live' else 'Noch keine Probe gedruckt.', 404)
        name = urllib.parse.quote(f'{z}{"-probe" if art == "probe" else ""}.pdf')
        return (200, b, 'application/pdf', {'Content-Disposition': f"inline; filename*=UTF-8''{name}"})

    def do_POST(self):
        host = (self.headers.get('host') or '').lower()
        o = (self.headers.get('Origin') or '').lower()
        if o and urllib.parse.urlparse(o).netloc != host:
            return self._fehler(403, 'HERKUNFT', 'Anfragen nur von La Carte selbst.')
        if not (self.headers.get('Content-Type') or '').startswith('application/json'):
            return self._fehler(415, 'FORM', 'Nur JSON.')
        n = int(self.headers.get('Content-Length') or 0)
        if n > GROSS:
            if n <= 6_000_000:   # Anfrage ganz lesen, sonst bricht die Verbindung ab, bevor die Meldung ankommt
                self.rfile.read(n)
            return self._fehler(413, 'GROSS', 'Die Daten sind zu gross.')
        was, _ = self._was()
        ip = self._ip()
        if zu_viel(ip, 'alle') or zu_viel(ip, 'schreiben') or (was in ('probe', 'veroeffentlichen') and zu_viel(ip, 'druck')):
            return self._fehler(429, 'GRENZE', 'Zu viele Änderungen in kurzer Zeit. Bitte eine Minute warten.')
        try:
            d = json.loads(self.rfile.read(n) or b'{}')
            if not isinstance(d, dict):
                raise ValueError
        except ValueError:
            return self._fehler(400, 'FORM', 'Die Anfrage ist kein gültiges JSON.')
        wer, rolle = self._wer()

        def tun():
            if was == 'veroeffentlichen':
                return (200, veroeffentlichen(d.get('z', ''), wer, rolle))
            r = C.post(was, d, wer, rolle)
            if was == 'probe':
                _pdfs_hoch()
            return (200, r)
        return self._lauf(tun, True)
