#!/usr/bin/env python3
"""Prüfserver des Hafenbüros · Wirtschaft am Schlössli Bottighofen (nur zum Bedienen und Prüfen; Nachtbau 3./4.11.2026).

  python3 _werkzeuge/maison/server.py [port]      Standard 9281

Liefert nur lesend (GET/HEAD):
  /_werkzeuge/…            aus _werkzeuge/ (das Hafenbüro unter /_werkzeuge/maison/)
  /assets/oberflaeche/…    aus _werkzeuge/oberflaeche/ (gemeinsames Kleid aller sieben Werkzeuge des Hauses)
  /assets/…  und Seiten    aus website/ (Fotos, Schriften, Seiten für «Website ansehen»)
Die Stand-Wege der Werkzeuge reicht er weiter: /_weiter/<werkzeug>/<weg> geht an die Adresse aus stand_wege.json (sonst an den festen Port
9282 … 9287 aus cloud/haus.json); nur 127.0.0.1, nur GET. Ein Browser liest nicht quer über Ports, deshalb dieser Umweg.
Fehlermeldungen der Seite (POST /studio/api/fehler) werden angenommen und verworfen."""
import http.server, json, os, socketserver, sys, urllib.request, urllib.error
from urllib.parse import urlparse, unquote, urljoin

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9281
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEB = os.path.join(WURZEL, 'website')
WZ = os.path.join(WURZEL, '_werkzeuge')
OF = os.path.join(WZ, 'oberflaeche')
TEIL = {'bureau': 'website', 'carte': 'karten', 'imprimerie': 'druck', 'reception': 'gaeste', 'livre': 'marke', 'registre': 'besuche'}
WERKBANK = 'http://127.0.0.1:9288'   # Server der Werkbank (Port 9288): «Zur Werkbank» führt lokal dorthin
FEST = {'bureau': 9282, 'carte': 9283, 'reception': 9284, 'livre': 9285, 'registre': 9286, 'imprimerie': 9287}   # Ports aus dem gemeinsamen Auftrag
LOKAL = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # nie über einen Proxy: nur 127.0.0.1


def adresse(k):
    try:
        a = (json.load(open(os.path.join(WZ, 'maison', 'stand_wege.json'), encoding='utf-8')).get(k) or {}).get('adresse') or ''
    except (OSError, ValueError):
        a = ''
    u = urlparse(a)
    if u.hostname in ('127.0.0.1', 'localhost') and u.port:
        return f'http://127.0.0.1:{u.port}/'
    return f'http://127.0.0.1:{FEST[k]}/' if k in FEST else ''


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=WEB, **k)

    def translate_path(self, path):
        p = unquote(urlparse(path).path)
        for vor, ordner in (('/assets/oberflaeche/', OF), ('/_werkzeuge/', WZ)):
            if p.startswith(vor):
                z = os.path.normpath(os.path.join(ordner, p[len(vor):]))
                return z if z == ordner or z.startswith(ordner + os.sep) else os.path.join(WEB, '.gesperrt')
        return super().translate_path(path)

    def do_GET(self):
        weg = urlparse(self.path)
        if weg.path.startswith('/_weiter/'):
            teile = weg.path.split('/', 3)
            k = teile[2] if len(teile) > 2 else ''
            basis = adresse(k) if k in TEIL else ''
            if not basis:
                return self._roh(404, b'{"fehler":"Werkzeug ohne Adresse"}')
            ziel = urljoin(basis, '/' + (teile[3] if len(teile) > 3 else '') + (('?' + weg.query) if weg.query else ''))
            if urlparse(ziel).hostname not in ('127.0.0.1', 'localhost'):
                return self._roh(403, b'{"fehler":"nur lokal"}')
            try:
                with LOKAL.open(ziel, timeout=6) as r:
                    return self._roh(r.status, r.read(), r.headers.get('Content-Type', 'application/json'))
            except urllib.error.HTTPError as f:
                return self._roh(f.code, f.read() or b'{}')
            except Exception:
                # Werkzeug läuft nicht (noch nicht geliefert oder Server aus): 204 ohne Inhalt, die Zentrale zeigt den Satz ohne Zahl (M05),
                # ohne roten Netzfehler in der Konsole des Betrachters. Falsche Wege (404 des Werkzeugs) bleiben sichtbar.
                self.send_response(204); self.send_header('X-Werkzeug', 'aus'); self.end_headers(); return
        if weg.path == '/werkbank' or weg.path.startswith('/werkbank/'):    # «Zur Werkbank» (R19): lokal liegt die Werkbank auf ihrem eigenen Server
            self.send_response(302); self.send_header('Location', WERKBANK + self.path); self.send_header('Content-Length', '0'); self.end_headers(); return
        if '/.' in unquote(weg.path):
            return self._roh(404, b'')
        return super().do_GET()

    def _roh(self, code, roh, art='application/json; charset=utf-8'):
        self.send_response(code); self.send_header('Content-Type', art); self.send_header('Content-Length', str(len(roh))); self.end_headers(); self.wfile.write(roh)

    def do_POST(self):
        n = min(int(self.headers.get('Content-Length') or 0), 4000); self.rfile.read(n)
        return self._roh(204 if urlparse(self.path).path == '/studio/api/fehler' else 405, b'')

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); self.send_header('X-Content-Type-Options', 'nosniff'); super().end_headers()

    def log_message(self, *a):
        pass


class S(socketserver.ThreadingTCPServer):
    allow_reuse_address = True; daemon_threads = True


if __name__ == '__main__':
    with S(('127.0.0.1', PORT), H) as httpd:
        print(f'Das Hafenbüro · Wirtschaft am Schlössli, Prüfserver auf http://127.0.0.1:{PORT}/_werkzeuge/maison/ (Wurzel {WURZEL})', flush=True)
        httpd.serve_forever()
