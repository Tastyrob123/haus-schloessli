"""Der Gastgeber (La Réception) und der Chat des Landgasthof Ruedihus online (Vorbild Doldenhorn und Carlton, dort nur gelesen): gemeinsamer Zugang zu den Daten (Abnahme 17.10.2026, Vorbild Grand Beau-Rivage
api/_rezeption_online.py, dort nur gelesen). Liegt online als api/_reception_online.py (online.json → lib).

Ablagen im privaten Blob (api/_speicher.py, Ablage mit Etag-Schutz): «reception» (Anfragen, Status, Nachgetragenes, Wissen des Teams) und je Monat
«reception-fragen-JJJJ-MM» (die Fragen aus dem Chat), damit der Chat je Frage nur den laufenden Monat liest und schreibt. Zwölf Monate werden
aufgehoben (reception.py räumt auf), ältere Monats-Ablagen löscht aufraeumen() hier.

Logik unverändert in api/_lib/reception/reception.py (dieselbe Datei wie am Rechner); das Chat-Modul ist api/_lib/_gast/gast.py mit seinem Wissen."""
import base64, glob, gzip, importlib.util, json, os, shutil, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import _speicher as SP  # noqa: E402

LIB = os.path.join(HIER, '_lib')
TMP = os.path.join(SP.TMP, 'reception')
DATEN = os.path.join(TMP, 'daten')
os.makedirs(DATEN, exist_ok=True)
os.environ['RECEPTION_DATEN'] = DATEN
os.environ.setdefault('RECEPTION_ONLINE', '1')
sys.path.insert(0, os.path.join(LIB, 'reception'))
import reception as R  # noqa: E402

_G = None


def gast():
    """Das Chat-Modul (_lib/_gast/gast.py) mit La Réception verbunden; einmal je Instanz. Fragen landen zusätzlich wie bisher bei /api/fragen,
    falls GAST_GEHEIM gesetzt ist (alte Ablage fürs Studio)."""
    global _G
    if _G is None:
        s = importlib.util.spec_from_file_location('gast_ruedihus', os.path.join(LIB, 'reception', 'gast', 'gast.py'))
        g = importlib.util.module_from_spec(s); s.loader.exec_module(g)
        alt_merke = g.merke
        if os.environ.get('RECEPTION_KI') == '0':   # nur in Prüfläufen: Probe-Antworten statt Claude
            import probe_ki
            g._api = probe_ki.api
        R.einbinden(g)
        neu_merke = g.merke

        def merke(host, daten):
            neu_merke(host, dict(daten))
            alt_merke(host, daten)
        g.merke = merke
        _G = g
    return _G


def monate(n):
    import datetime
    heute = datetime.date.today().replace(day=1)
    aus = []
    for i in range(n):
        m = (heute.month - 1 - i) % 12 + 1
        j = heute.year - ((i + 12 - heute.month) // 12)
        aus.append(f'{j:04d}-{m:02d}')
    return aus


def monat_von(id_):
    try:
        return id_.split('/')[1][:7]
    except (IndexError, AttributeError):
        return monate(1)[0]


class MonatsAblage(SP.Ablage):
    """Die Fragen eines Monats liegen in Tagesordnern (fragen/JJJJ-MM-TT/…); die Ablage heisst nach dem Monat. Jede Datei gehört dazu,
    deren Pfad mit dem Monat beginnt (Fund im Rivage 16.10.2026: mit teil='fragen/JJJJ-MM' blieb die Ablage leer)."""

    def _gehoert(self, rel):
        return rel.startswith(self.teil) and rel[len(self.teil):len(self.teil) + 1] in ('/', '-') and not rel.endswith('.gut')

    def _eltern(self):
        return os.path.join(self.ordner, os.path.dirname(self.teil)), os.path.basename(self.teil)

    def laden(self):
        roh, self.etag = SP.get(self.pfad, mit_etag=True)
        daten = json.loads(gzip.decompress(roh).decode('utf-8')) if roh else {}
        eltern, basis = self._eltern()
        if os.path.isdir(eltern):
            for e in os.listdir(eltern):
                if e == basis or e.startswith(basis + '-'):
                    shutil.rmtree(os.path.join(eltern, e), ignore_errors=True)
        os.makedirs(eltern, exist_ok=True)
        for rel, inhalt in daten.items():
            if self._gehoert(rel):
                self._schreib_datei(rel, inhalt)
        self.vorher = {k: v for k, v in daten.items() if self._gehoert(k)}
        return self.vorher

    def _lesen(self):
        daten = {}
        eltern, _ = self._eltern()
        for w, _, fs in os.walk(eltern):
            for f in fs:
                if f.endswith(('.neu', '.gut')) or f.startswith('.'):
                    continue
                p = os.path.join(w, f)
                rel = os.path.relpath(p, self.ordner).replace(os.sep, '/')
                if self._gehoert(rel):
                    roh = open(p, 'rb').read()
                    try:
                        daten[rel] = roh.decode('utf-8')
                    except UnicodeDecodeError:
                        daten[rel] = 'b64:' + base64.b64encode(roh).decode('ascii')
        return daten


class HausAblage(SP.Ablage):
    """«reception» ohne die Monatsfragen und ohne die .gut-Sicherungen der Ablage am Rechner (im Blob schützt der Etag)."""

    def _gehoert(self, rel):
        return super()._gehoert(rel) and not rel.endswith('.gut')


def laden(n_monate=1, zusatz=()):
    """Ablagen laden: Anfragen und Status immer, dazu die letzten n Monate Fragen (und die Monate in zusatz)."""
    A = [HausAblage('reception', DATEN, ohne=('fragen',))]
    for m in dict.fromkeys(list(monate(n_monate)) + list(zusatz)):
        A.append(MonatsAblage(f'reception-fragen-{m}', DATEN, teil=f'fragen/{m}'))
    for a in A:
        a.laden()
    return A


def sichern(A, zusammenfuehren=False):
    for a in A:
        a.sichern(zusammenfuehren=zusammenfuehren)


def aufraeumen():
    """Monats-Ablagen älter als zwölf Monate löschen (Datenschutz: Gästefragen zwölf Monate)."""
    grenze = monate(13)[-1]
    alt = [b['url'] for b in SP.liste('ablage/reception-fragen-') if b['pathname'][len('ablage/reception-fragen-'):][:7] < grenze]
    if alt:
        SP.loeschen(alt)
    return len(alt)


def zustand():
    """Für pruefung.html online: liest nur."""
    p = []
    def punkt(gruppe, was, stand, text, stichwort=''):
        p.append({'gruppe': gruppe, 'was': was, 'stand': stand, 'text': text, 'stichwort': stichwort})
    punkt('Server', 'Server-Teil läuft', 'gut', 'online (Vercel-Funktion)')
    punkt('Server', 'Speicher', 'gut' if SP.TOKEN else 'rot', 'Vercel Blob, privat' if SP.TOKEN else 'Vorführung: nichts hält (Schlüssel BLOB_READ_WRITE_TOKEN fehlt)', '' if SP.TOKEN else 'SERVER')
    punkt('Server', 'Assistent', 'gut' if os.environ.get('ANTHROPIC_API_KEY') else 'rot', 'Schlüssel beim Projekt' if os.environ.get('ANTHROPIC_API_KEY') else 'Schlüssel ANTHROPIC_API_KEY fehlt: Chat und Brief schreiben gehen nicht', '' if os.environ.get('ANTHROPIC_API_KEY') else 'KI')
    n = {art: len(glob.glob(os.path.join(DATEN, art, '*', '*.json'))) for art in ('anfragen', 'fragen')}
    punkt('Daten', 'Anfragen und Fragen', 'gut', f"{n['anfragen']} Anfragen, {n['fragen']} Fragen der letzten drei Monate")
    for q in ('gast_wissen.txt', 'gast_tal.txt'):
        f = os.path.join(LIB, 'reception', 'gast', q)
        punkt('Wissen', q, 'gut' if os.path.exists(f) and os.path.getsize(f) > 1000 else 'rot', f'{os.path.getsize(f) // 1024} kB' if os.path.exists(f) else 'fehlt', '' if os.path.exists(f) else 'WISSEN')
    punkt('Brief', 'PDF', 'gelb', 'online öffnet das Druckfenster des Browsers mit demselben A4-Satz (kein Chromium in der Funktion)', 'PDF')
    punkt('Wissen', '«Das weiss der Chat»', 'gelb', 'nur am Rechner des Hauses (wie im Rivage)', '')
    web = sum(1 for f in glob.glob(os.path.join(DATEN, 'anfragen', '*', '*.json')) if (lambda s: '"web": true' in s and '"beispiel": true' not in s)(open(f, encoding='utf-8', errors='replace').read()))
    punkt('Website', 'Formulare der Website', 'gut', f'{web} Anfragen über die Formulare der Website (Weg formular)')
    punkt('Sicherheit', 'Herkunft und Grösse', 'gut', 'nur Aufrufe von der eigenen Seite, höchstens 3 MB je Anfrage, Formulare 6 je Minute und Absender')
    punkt('Sicherheit', 'Anmeldung', 'gelb', 'noch keine (Roberts Wort 15.10.2026), kommt vor der Auslieferung', 'ANMELDUNG')
    return {'punkte': p, 'fehler': []}
