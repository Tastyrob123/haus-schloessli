#!/usr/bin/env python3
"""Prüfserver der Stube · Wirtschaft am Schlössli (nur zum Bedienen und Prüfen).

  python3 _werkzeuge/maison/server.py [port]      Standard 8987, Wurzel = Projektordner des Hauses

Liefert die Dateien des Projekts nur lesend (GET/HEAD) und reicht die Stand-Wege der Werkzeuge weiter: /_weiter/<werkzeug>/<weg> geht an
die Adresse, die das Werkzeug in der Kette angibt (_kette/11-werkbank/werkzeuge/<teil>/stand.json → adresse), nur an 127.0.0.1/localhost,
nur GET. Ein Browser liest nicht quer über Ports, deshalb dieser Umweg. Fehlermeldungen der Seite (POST /studio/api/fehler) werden angenommen
und verworfen."""
import http.server, json, os, socketserver, sys, urllib.request, urllib.error
from urllib.parse import urlparse, unquote, urljoin

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8987
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEIL = {'bureau': 'website', 'carte': 'karten', 'imprimerie': 'druck', 'reception': 'gaeste', 'livre': 'marke', 'registre': 'besuche'}


def adresse(k):
    try:
        j = json.load(open(os.path.join(WURZEL, '_kette', '11-werkbank', 'werkzeuge', TEIL[k], 'stand.json'), encoding='utf-8'))
    except (OSError, ValueError, KeyError):
        return ''
    a = j.get('adresse') or ''
    return a if urlparse(a).hostname in ('127.0.0.1', 'localhost') else ''


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=WURZEL, **k)

    def do_GET(self):
        weg = urlparse(self.path)
        if weg.path.startswith('/_weiter/'):
            teile = weg.path.split('/', 3)
            k = teile[2] if len(teile) > 2 else ''
            basis = adresse(k) if k in TEIL else ''
            if not basis:
                return self._roh(404, b'{"fehler":"Werkzeug ohne Adresse"}')
            ziel = urljoin(basis, '/' + (teile[3] if len(teile) > 3 else '') + (('?' + weg.query) if weg.query else ''))   # Weg ab der Wurzel des Werkzeug-Servers
            if urlparse(ziel).hostname not in ('127.0.0.1', 'localhost'):
                return self._roh(403, b'{"fehler":"nur lokal"}')
            try:
                with urllib.request.urlopen(ziel, timeout=6) as r:
                    return self._roh(r.status, r.read(), r.headers.get('Content-Type', 'application/json'))
            except urllib.error.HTTPError as f:
                return self._roh(f.code, f.read() or b'{}')
            except Exception:
                return self._roh(502, b'{"fehler":"Werkzeug antwortet nicht"}')
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
        print(f'Die Stube, Prüfserver auf http://127.0.0.1:{PORT}/_werkzeuge/maison/ (Wurzel {WURZEL})', flush=True)
        httpd.serve_forever()
