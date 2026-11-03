#!/usr/bin/env python3
# Vorschau-Server Wirtschaft am Schlössli (mehrfädig, ohne Zwischenspeicher, eigene 404-Seite). python3 serve.py [port]
import http.server, socketserver, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8982


class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if code == 404 and os.path.exists('404.html'):
            body = open('404.html', 'rb').read()
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(body))); self.end_headers()
            self.wfile.write(body); return
        super().send_error(code, message, explain)

    def log_message(self, *a):
        pass


class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    S(('127.0.0.1', PORT), H).serve_forever()
