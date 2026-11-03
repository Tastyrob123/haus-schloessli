#!/usr/bin/env python3
"""Das Schaufenster (Le Bureau) · Wirtschaft am Schlössli — eigener Server (19.10.2026). python3 _werkzeuge/bureau/serve.py [port]   (Standard 9035)

Das Werkzeug selbst ist der Schreibtisch des Stamms (~/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/, Schicht über den gebauten
Seiten, Probe-Kopie _probe/schloessli/, Speicher _Werkzeuge/daten/). Dieser Server legt den Rahmen des Hauses darum, wie bei den anderen
Werkzeugen des Schlössli:
  /_werkzeuge/bureau/…        Seite des Werkzeugs (index.html, bureau.css) aus diesem Ordner
  /assets/oberflaeche/…        gemeinsamer Werkzeug-Rahmen des Hauses (_werkzeuge/oberflaeche/, Kleid schloessli)
  /assets/…                    Schriften und Fotos der Website (website/assets/, nur gelesen)
  alles andere                 wie der Server des Stamms (unterbau/serve.py): /api/…, /stamm/…, /werkzeuge/website/…, /haeuser/…
Sicherheit (Master Werkzeug-Bau 5.2/5.3, S01–S03): hört nur auf 127.0.0.1, nur Anfragen an diese Adresse (421), schreibende Wege nur von der
eigenen Seite (403) und nur als JSON, höchstens 3 MB je Anfrage (413), Grenze je Absender und Minute für die Wege des Werkzeugs (429, Retry-After),
feste Kopfzeilen gegen Einbetten und fremde Skripte (die Vorschau der Seiten läuft als srcdoc im Rahmen und braucht deren eigene Skripte).
Daten: WERKZEUGE_DATEN (Wegwerf-Ordner für Prüfläufe), sonst die echten unter _Werkzeuge/daten/."""
import os
import sys
import threading
import time
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parent.parent
OBERFLAECHE = PROJEKT / '_werkzeuge' / 'oberflaeche'
ASSETS = PROJEKT / 'website' / 'assets'
STAMM = Path(os.path.expanduser('~/Desktop/Website-Projekte/_Werkzeuge'))
sys.path.insert(0, str(STAMM / 'unterbau'))
import serve as stamm  # noqa: E402  (Server des Stamms: Wege, Speicher, Dateien)

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('BUREAU_PORT', '9035'))
GROSS = 3_000_000
GRENZEN = {'alle': 900, 'schreiben': 60}
if os.environ.get('BUREAU_PRUEFLAUF'):   # fester Prüflauf (pruef.js) schreibt in einer Minute mehr als ein Mensch; Grenze selbst prüft der Lauf nicht
    GRENZEN = {'alle': 90000, 'schreiben': 6000}
_ZAEHLER, _SCHLOSS = {}, threading.Lock()
ENDUNG_OK = {'.html', '.css', '.js', '.json', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.woff2', '.ttf', '.ico', '.avif', '.gif', '.txt'}
KOPF = {'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer', 'X-Frame-Options': 'SAMEORIGIN',
        'Permissions-Policy': 'camera=(), microphone=(), geolocation=()', 'Cross-Origin-Opener-Policy': 'same-origin'}
# Ohne script-src: die Vorschau setzt die Seite als srcdoc in den Rahmen, srcdoc erbt die Regel der Werkzeug-Seite, und die Seite samt Klick-Skript
# der Vorschau braucht eingebettete Skripte (Fund Ruedihus 2: Vorschau von der Regel ausnehmen). Einbetten, Formulare und base bleiben gesperrt.
CSP = "frame-ancestors 'self'; base-uri 'self'; form-action 'self'; object-src 'none'"


TEIL = {'maison': 'zentrale', 'carte': 'karten', 'imprimerie': 'druck', 'reception': 'gaeste', 'livre': 'marke', 'registre': 'besuche'}


def nachbar(k):
    """Adresse eines anderen Werkzeugs des Hauses: was es in der Kette angibt (_kette/11-werkbank/werkzeuge/<teil>/stand.json › adresse),
    sonst der Server der Stube (8987, liefert den Projektordner). Jedes Werkzeug läuft bis Station 14 auf eigenem Port; ein Kopf-Knopf
    «/_werkzeuge/maison/» führt sonst hier ins Leere."""
    import json
    try:
        a = json.loads((PROJEKT / '_kette' / '11-werkbank' / 'werkzeuge' / TEIL[k] / 'stand.json').read_text(encoding='utf-8')).get('adresse') or ''
    except (OSError, ValueError, KeyError):
        a = ''
    return a if urlparse(a).hostname in ('127.0.0.1', 'localhost') else f'http://127.0.0.1:8987/_werkzeuge/{k}/'


def zu_viele(wer, art):
    jetzt = time.time()
    with _SCHLOSS:
        z = [t for t in _ZAEHLER.get((wer, art), []) if jetzt - t < 60]
        z.append(jetzt)
        _ZAEHLER[(wer, art)] = z
        return len(z) > GRENZEN[art]


class Antwort(stamm.Antwort):
    server_version = 'Schaufenster/1'

    def end_headers(self):
        for k, v in KOPF.items():
            self.send_header(k, v)
        self.send_header('Content-Security-Policy', CSP)
        super().end_headers()

    def _datei(self, wurzel, rest):
        ziel = (wurzel / rest).resolve()
        if wurzel.resolve() not in ziel.parents or not ziel.is_file() or ziel.suffix.lower() not in ENDUNG_OK or any(t.startswith('.') or t in ('_daten', '__pycache__') for t in Path(rest).parts):
            return self._json(404, {'fehler': 'Nicht gefunden', 'stichwort': 'nicht-gefunden'})
        roh = ziel.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', stamm.mimetypes.guess_type(ziel.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(len(roh)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(roh)

    def _pruefseite(self):
        """Prüfseite des Stamms im Kleid des Hauses (Demo-Check 21.10.2026): ohne den Weltknopf «Grandhotel/Landhaus» des Stamms, mit dem Namen
        des Werkzeugs im Haus (WO_HAUS.namen.website) und «Zum Werkzeug» zurück ins Schaufenster statt in den Stamm ohne Rahmen. Die Datei des Stamms
        bleibt unverändert; hier werden nur Kopf und Stile eingesetzt."""
        roh = (STAMM / 'werkzeuge' / 'website' / 'pruefung.html').read_text(encoding='utf-8')
        roh = roh.replace('<title>Prüfung · Website pflegen</title>', '<title>Prüfung · Das Schaufenster · Wirtschaft am Schlössli</title>')
        roh = roh.replace('<link rel="stylesheet" href="/stamm/welt.css">', '<script src="/assets/oberflaeche/kleid/schloessli.js?v=2"></script>\n<link rel="stylesheet" href="/stamm/welt.css">')
        roh = roh.replace('<script src="/stamm/welt.js"></script>', '<script src="/stamm/welt.js" data-haus="schloessli"></script>')
        roh = roh.replace('<link rel="stylesheet" href="pruefung.css?v=2026-10-12.1">', '<link rel="stylesheet" href="pruefung.css?v=2026-10-12.1">\n<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v=2"><link rel="stylesheet" href="/assets/oberflaeche/kleid/schloessli.css?v=2">\n<link rel="stylesheet" href="/_werkzeuge/bureau/bureau.css?v=2"><link rel="stylesheet" href="/_werkzeuge/bureau/pruefung-haus.css?v=1">')
        roh = roh.replace('<span data-werkzeug="website"></span>', 'Das Schaufenster').replace('<button data-welt-knopf></button>', '')
        roh = roh.replace('<script src="pruefung.js?v=2026-10-12.1"></script>', '<script src="pruefung.js?v=2026-10-12.1"></script>\n<script src="/_werkzeuge/bureau/pruefung-haus.js?v=1"></script>')
        daten = roh.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(daten)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(daten)

    def _bedien(self, methode):
        if self.headers.get('Host', '') not in (f'127.0.0.1:{PORT}', f'localhost:{PORT}'):
            return self._json(421, {'fehler': 'Falsche Adresse', 'stichwort': 'fremder-host'})
        pfad = unquote(urlparse(self.path).path)
        werkzeug = pfad.startswith('/api/')
        schreibt = methode in ('POST', 'PUT', 'DELETE')
        if werkzeug and zu_viele(self.client_address[0], 'schreiben' if schreibt else 'alle'):
            self.send_response(429)
            self.send_header('Retry-After', '60')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        if schreibt:
            herkunft = self.headers.get('Origin')
            if herkunft not in (f'http://127.0.0.1:{PORT}', f'http://localhost:{PORT}'):
                return self._json(403, {'fehler': 'Nur von der eigenen Seite', 'stichwort': 'fremde-herkunft'})
            if int(self.headers.get('Content-Length') or 0) > GROSS:
                return self._json(413, {'fehler': 'Zu gross', 'stichwort': 'zu-gross'})
            if not (self.headers.get('Content-Type') or '').startswith('application/json') and int(self.headers.get('Content-Length') or 0):
                return self._json(415, {'fehler': 'Nur JSON', 'stichwort': 'anfrage-unlesbar'})
        if methode == 'GET':
            if pfad in ('/', '/_werkzeuge/bureau'):
                self.send_response(301)
                self.send_header('Location', '/_werkzeuge/bureau/' + ('?' + urlparse(self.path).query if urlparse(self.path).query else ''))
                self.end_headers()
                return
            if pfad.startswith('/_werkzeuge/bureau/'):
                rest = pfad[len('/_werkzeuge/bureau/'):] or 'index.html'
                if rest.endswith('.py') or rest.endswith('.sh'):
                    return self._json(404, {'fehler': 'Nicht gefunden', 'stichwort': 'nicht-gefunden'})
                return self._datei(HIER, rest)
            teile = pfad.strip('/').split('/')
            if len(teile) >= 2 and teile[0] == '_werkzeuge' and teile[1] in TEIL:
                self.send_response(302)
                self.send_header('Location', nachbar(teile[1]))
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
            if pfad == '/werkzeuge/website/pruefung.html':
                return self._pruefseite()
            if pfad.startswith('/assets/oberflaeche/'):
                return self._datei(OBERFLAECHE, pfad[len('/assets/oberflaeche/'):])
            if pfad.startswith('/assets/'):
                return self._datei(ASSETS, pfad[len('/assets/'):])
        return super()._bedien(methode)


if __name__ == '__main__':
    os.chdir(STAMM)
    print(f'Das Schaufenster auf http://127.0.0.1:{PORT}/_werkzeuge/bureau/')
    ThreadingHTTPServer(('127.0.0.1', PORT), Antwort).serve_forever()
