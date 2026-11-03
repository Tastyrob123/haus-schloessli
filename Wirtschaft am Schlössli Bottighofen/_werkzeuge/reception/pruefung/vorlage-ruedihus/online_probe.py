#!/usr/bin/env python3
"""Der Gastgeber (La Réception) · Landgasthof Ruedihus: die Online-Fassung auf dem Rechner nachstellen, ohne Vercel und ohne Hochladen (Vorbild Doldenhorn
und Carlton, dort nur gelesen). Baut aus online.json einen Online-Ordner im Temp-Ordner (Funktionen, lib, statik; Speicher-Schicht api/_speicher.py aus dem
Carlton _werkzeuge/online/api/, nur kopiert), «Blob» als Ordner (BLOB_LOKAL), Probe-Antworten statt KI, und stellt auf einem Port die Umleitungen aus
online.json nach: /werkzeuge/reception/… statisch, /_werkzeuge/reception/api/… und /werkzeuge/reception/api/… an api/reception.py, /api/gast an api/gast.py.
Die Website (mit dem Anfrage-Fenster der Probe-Kopie) kommt als Dateien aus dem Ordner der Probe-Kopie.
   python3 online_probe.py [port]      Standard 9033      (nur in der Probe-Kopie)
Danach läuft node online_bedienen.js http://localhost:<port>. Strg+C beendet, der Temp-Ordner bleibt zum Nachsehen."""
import importlib.util, json, os, shutil, sys, tempfile, urllib.request, urllib.error
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, quote

HIER = os.path.dirname(os.path.abspath(__file__))
REC = os.path.dirname(HIER)
PROJ = os.path.dirname(os.path.dirname(REC))
CARLTON_API = os.path.expanduser('~/Desktop/Website-Projekte/Carlton-Europe Interlaken/_werkzeuge/online/api')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9033
if not os.path.exists(os.path.join(PROJ, 'PROBE-LIESMICH.txt')):
    sys.exit('Nur in der Probe-Kopie laufen lassen.')


def kopiere(q, z):
    if os.path.isdir(q):
        shutil.copytree(q, z, dirs_exist_ok=True)
    else:
        os.makedirs(os.path.dirname(z), exist_ok=True); shutil.copy2(q, z)


Z = tempfile.mkdtemp(prefix='reception-rh-online-')
A = json.load(open(os.path.join(REC, 'online.json'), encoding='utf-8'))
for f in ('_speicher.py',):
    kopiere(os.path.join(CARLTON_API, f), os.path.join(Z, 'api', f))
for ziel, f in A['funktionen'].items():
    kopiere(os.path.join(PROJ, f['von']), os.path.join(Z, ziel))
for q, z in A['lib'].items():
    kopiere(os.path.join(PROJ, q), os.path.join(Z, z))
for q, z in A['statik'].items():
    if os.path.exists(os.path.join(PROJ, q)):
        kopiere(os.path.join(PROJ, q), os.path.join(Z, z))
os.makedirs(os.path.join(Z, 'blob'), exist_ok=True)
for k in ('BLOB_READ_WRITE_TOKEN', 'BLOB_PUBLIC_READ_WRITE_TOKEN', 'VERCEL', 'VERCEL_ENV', 'ANTHROPIC_API_KEY'):
    os.environ.pop(k, None)
os.environ.update(BLOB_LOKAL=os.path.join(Z, 'blob'), WERKZEUG_TMP=os.path.join(Z, '_tmp'), RECEPTION_KI='0')
sys.path.insert(0, os.path.join(Z, 'api'))


def lade(n):
    s = importlib.util.spec_from_file_location('fn_' + n, os.path.join(Z, 'api', n + '.py'))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m.handler


REC_H, GAST_H = lade('reception'), lade('gast')
UMLEITEN = [(u['source'].split(':')[0], u['destination']) for u in A['umleitungen']]
TYP = {'.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml',
       '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.json': 'application/json', '.woff2': 'font/woff2'}


class Vorschalt(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *a):
        pass

    def _weiter_haus(self):
        """Website der Probe-Kopie als Dateien (online liefert Vercel sie aus); Wege mit _ und Quellen bleiben zu wie online."""
        u = urlparse(self.path).path
        rel = u.strip('/') or 'index.html'
        if rel.endswith('/'):
            rel += 'index.html'
        p = os.path.normpath(os.path.join(PROJ, rel))
        if os.path.isdir(p):
            p = os.path.join(p, 'index.html')
        if not p.startswith(PROJ) or any(x.startswith('_') or x.startswith('.') for x in os.path.relpath(p, PROJ).split(os.sep)) or p.endswith(('.py', '.md')) or not os.path.isfile(p):
            d = b'Nicht gefunden'
            self.send_response(404); self.send_header('Content-Type', 'text/plain'); self.send_header('Content-Length', str(len(d))); self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(d)
            return
        d = open(p, 'rb').read()
        self.send_response(200); self.send_header('Content-Type', TYP.get(os.path.splitext(p)[1], 'application/octet-stream')); self.send_header('Content-Length', str(len(d)))
        self.send_header('Cache-Control', 'no-store'); self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(d)

    def _statisch(self, p):
        if not os.path.isfile(p):
            return self._weiter_haus()
        d = open(p, 'rb').read()
        self.send_response(200); self.send_header('Content-Type', TYP.get(os.path.splitext(p)[1], 'application/octet-stream')); self.send_header('Content-Length', str(len(d)))
        self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(d)

    def _als(self, klasse, schreibt):
        """Die Anfrage von der Funktion selbst beantworten lassen (wie Vercel): für die Dauer der Antwort ist dieser Handler die Funktion."""
        self.__class__ = klasse
        try:
            return (klasse.do_POST if schreibt else klasse.do_GET)(self)
        finally:
            self.__class__ = Vorschalt
            self.close_connection = True

    def _route(self, schreibt):
        u = urlparse(self.path)
        if u.path.startswith(('/_werkzeuge/reception/api/', '/werkzeuge/reception/api/')):   # wie vercel.json: /api/reception?__weg=…
            self.path = '/api/reception?__weg=' + quote(u.path) + ('&' + u.query if u.query else '')
            return self._als(REC_H, schreibt)
        if u.path == '/api/gast':
            return self._als(GAST_H, schreibt)
        if u.path in ('/_werkzeuge/reception', '/_werkzeuge/reception/', '/werkzeuge/reception', '/werkzeuge/reception/'):
            return self._statisch(os.path.join(Z, 'werkzeuge', 'reception', 'index.html'))
        for vor, ziel in ((u_[0], u_[1]) for u_ in UMLEITEN):
            if vor.endswith('/') and u.path.startswith(vor) and ziel.endswith(':datei*'):
                return self._statisch(os.path.join(Z, ziel.split(':')[0].lstrip('/'), u.path[len(vor):]))
        if u.path.startswith('/werkzeuge/reception/'):
            return self._statisch(os.path.join(Z, u.path.lstrip('/')))
        return self._weiter_haus()   # Website der Probe-Kopie

    def do_GET(self):
        return self._route(False)

    def do_HEAD(self):
        return self._route(False)

    def do_POST(self):
        return self._route(True)


if __name__ == '__main__':
    print(f'Online-Probe Der Gastgeber: http://localhost:{PORT}/werkzeuge/reception/  ·  Ordner {Z}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', PORT), Vorschalt).serve_forever()
