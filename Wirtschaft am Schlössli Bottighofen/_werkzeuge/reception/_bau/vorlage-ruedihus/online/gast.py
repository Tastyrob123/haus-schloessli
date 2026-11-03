"""Rezeption im Chat online (Vercel-Funktion /api/gast, das Fenster unten rechts und die Zimmermappe), mit La Réception verbunden
(Abnahme 17.10.2026, Vorbild Grand Beau-Rivage api/gast.py): Das Chat-Modul ist unverändert _gast/gast.py (online api/_lib/_gast/gast.py);
jede Frage wandert in die Monats-Ablage im privaten Blob, Anfragen mit Name und Kontakt in die Ablage «reception».
Hält der Speicher nicht (Blob aus, Konflikt), antwortet der Chat trotzdem: der Gast merkt nichts, nur das Protokoll dieser einen Frage fehlt.
Schlüssel: ANTHROPIC_API_KEY, ANTHROPIC_WORKSPACE_ID."""
from http.server import BaseHTTPRequestHandler  # noqa: F401  (Vercel erkennt daran die Funktion)
import os, sys, threading

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import _speicher as SP  # noqa: E402
import _reception_online as RO  # noqa: E402
import io, json, re  # noqa: E402
try:
    import _antwortbuch as BUCH  # noqa: E402  Antwortbuch des Hauses (Robert 19.10.2026 05:10: feste Antworten, solange die KI kein Guthaben hat)
except Exception:  # noqa: BLE001
    BUCH = None
NOT = re.compile(r'keine gesicherte Auskunft|no confirmed information|pas d.information confirm', re.I)

RIEGEL = threading.RLock()
G = RO.gast()


class handler(G.handler):
    def do_GET(self):
        return G.handler.do_GET(self)

    def do_POST(self):
        with RIEGEL:
            try:
                A = RO.laden(1)
            except Exception:  # noqa: BLE001  Speicher nicht da: trotzdem antworten
                A = None
            try:
                return self._mit_buch()
            finally:
                if A:
                    try:
                        RO.sichern(A, zusammenfuehren=True)
                    except Exception:  # noqa: BLE001  die Antwort an den Gast ist schon unterwegs
                        pass

    def _mit_buch(self):
        """Die KI fragen wie bisher; antwortet sie nicht (Fehlerstatus, Guthaben, Schlüssel) oder nur mit dem Notsatz, antwortet das Antwortbuch mit 200."""
        if not BUCH:
            return G.handler.do_POST(self)
        n = int(self.headers.get('content-length') or 0)
        roh = self.rfile.read(n) if n else b''
        try:
            d = json.loads(roh or b'{}')
        except ValueError:
            d = {}
        echt, puffer = self.wfile, io.BytesIO()
        self.rfile, self.wfile = io.BytesIO(roh), puffer
        try:
            G.handler.do_POST(self)
        except Exception:  # noqa: BLE001  die KI-Seite ist ausgefallen: das Buch antwortet
            pass
        finally:
            try:
                self.wfile.flush()
            except Exception:  # noqa: BLE001
                pass
            self.wfile = echt
        aus = puffer.getvalue()
        kopf, _, rumpf = aus.partition(b'\r\n\r\n')
        ok = kopf.startswith(b'HTTP/') and b' 200 ' in kopf.split(b'\r\n', 1)[0]
        if ok:
            try:
                j = json.loads(rumpf or b'{}')
                ok = bool(j.get('text')) and not NOT.search(j.get('text', '')) and not j.get('grenze')   # Pause nach vielen Fragen: das Buch kostet nichts, es antwortet
            except ValueError:
                ok = False
        if ok:
            self.wfile.write(aus)
            return
        fragen = [m.get('content', '') for m in (d.get('messages') or []) if m.get('role') == 'user']
        a = BUCH.antwort(fragen[-1] if fragen else '', d.get('sprache') or 'de')
        a.pop('buch', None)
        b = json.dumps(a, ensure_ascii=False).encode('utf-8')
        self.close_connection = True
        self.send_response(200)
        self.send_header('content-type', 'application/json; charset=utf-8')
        self.send_header('cache-control', 'no-store')
        self.send_header('content-length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)
