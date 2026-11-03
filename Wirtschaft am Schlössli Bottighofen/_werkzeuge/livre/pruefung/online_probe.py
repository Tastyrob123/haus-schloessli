#!/usr/bin/env python3
"""Das Hausbuch · Wirtschaft am Schlössli · Probe der Online-Fassung auf dem Rechner, ohne Vercel und ohne Hochladen (Muster Carlton _werkzeuge/carte/pruef/online_probe.js).
   python3 _werkzeuge/livre/pruefung/online_probe.py [port]       (Port 9049: vorher den eigenen Prüfserver beenden)
Baut aus online.json einen Online-Ordner im Temp-Ordner (Funktion api/livre.py, lib, statik; Speicher-Schicht api/_speicher.py als Kopie aus dem
gemeinsamen Online-Weg des Carlton, dort nur gelesen), stellt die Umleitungen aus online.json nach, liefert die Website (assets/) nur lesend aus und
setzt dieselbe Sicherheitsregel für Skripte wie online (script-src 'self', keine eingebetteten Skripte, Falle 9). Ohne Schlüssel, ohne Blob, ohne Claude.
Danach läuft der Server, bis er per PID beendet wird (Ausgabe nennt sie)."""
import http.server, importlib.util, json, mimetypes, os, re, shutil, socketserver, sys, tempfile, urllib.parse

HIER = os.path.dirname(os.path.abspath(__file__))
LIV = os.path.dirname(HIER)
PROJ = os.path.dirname(os.path.dirname(LIV))
SPEICHER = os.path.expanduser('~/Desktop/Website-Projekte/Carlton-Europe Interlaken/_werkzeuge/online/api/_speicher.py')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9049
A = json.load(open(os.path.join(LIV, 'online.json'), encoding='utf-8'))
Z = tempfile.mkdtemp(prefix='livre-online-')


def kopiere(q, z):
    if os.path.isdir(q):
        shutil.copytree(q, z, dirs_exist_ok=True)
    else:
        os.makedirs(os.path.dirname(z), exist_ok=True); shutil.copyfile(q, z)


kopiere(SPEICHER, os.path.join(Z, 'api', '_speicher.py'))
for ziel, f in A['funktionen'].items():
    kopiere(os.path.join(PROJ, f['von']), os.path.join(Z, ziel))
for q, z in A['lib'].items():
    kopiere(os.path.join(PROJ, q), os.path.join(Z, z))
for q, z in A['statik'].items():
    kopiere(os.path.join(PROJ, q), os.path.join(Z, z))
for k in ('BLOB_READ_WRITE_TOKEN', 'BLOB_PUBLIC_READ_WRITE_TOKEN', 'VERCEL', 'ANTHROPIC_API_KEY', 'LIVRE_KI', 'LIVRE_JSON'):
    os.environ.pop(k, None)
spec = importlib.util.spec_from_file_location('livre_fn', os.path.join(Z, 'api', 'livre.py'))
FN = importlib.util.module_from_spec(spec); spec.loader.exec_module(FN)
UM = []
for u in A['umleitungen']:
    rx = '^' + re.escape(u['source']).replace(r'/:pfad\*', '(?:/(?P<pfad>.*))?') + '$'
    UM.append((re.compile(rx), u['destination']))
CSP = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; frame-ancestors 'self'"


def umleiten(pfad, query):
    for rx, ziel in UM:
        m = rx.match(pfad)
        if m:
            neu = ziel.replace(':pfad*', (m.groupdict().get('pfad') or ''))
            if '?' in neu and query:
                neu += '&' + query
            elif query:
                neu += '?' + query
            return neu
    return pfad + ('?' + query if query else '')


class H(FN.handler):
    def _statisch(self, pfad):
        rel = urllib.parse.unquote(pfad).lstrip('/')
        if '..' in rel:
            return self.send_error(404)
        for basis in (Z, PROJ if rel.startswith('assets/') else None):
            if not basis:
                continue
            p = os.path.join(basis, rel)
            if os.path.isdir(p):
                p = os.path.join(p, 'index.html')
            if os.path.isfile(p):
                d = open(p, 'rb').read()
                self.send_response(200)
                self.send_header('Content-Type', mimetypes.guess_type(p)[0] or 'application/octet-stream')
                self.send_header('Content-Length', str(len(d)))
                self.send_header('Content-Security-Policy', CSP)
                self.end_headers()
                if self.command != 'HEAD':
                    self.wfile.write(d)
                return
        self.send_error(404)

    def _weiche(self):
        u = urllib.parse.urlparse(self.path)
        neu = umleiten(u.path, u.query)
        if neu.startswith('/api/livre'):
            self.path = neu
            return True
        self.path = neu
        self._statisch(urllib.parse.urlparse(neu).path)
        return False

    def do_GET(self):
        if self._weiche():
            return super().do_GET()

    def do_HEAD(self):
        return self.do_GET()

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        neu = umleiten(u.path, u.query)
        if not neu.startswith('/api/livre'):
            return self.send_error(405)
        self.path = neu
        return super().do_POST()


class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    print(f'Online-Probe Le Livre auf http://127.0.0.1:{PORT}/werkzeuge/livre/  ·  Ordner {Z}  ·  PID {os.getpid()}', flush=True)
    try:
        S(('127.0.0.1', PORT), H).serve_forever()
    finally:
        shutil.rmtree(Z, ignore_errors=True)
