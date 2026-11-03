"""Der Gastgeber (La Réception) online, Landgasthof Ruedihus (Vercel-Funktion, Vorbild Doldenhorn und Carlton online/reception.py, Grand Beau-Rivage api/reception.py): /_werkzeuge/reception/api/<was> und
/werkzeuge/reception/api/<was>, in vercel.json auf /api/reception?__weg=… umgeschrieben (online.json). Logik in api/_lib/reception/reception.py
(dieselbe Datei wie am Rechner), Daten im privaten Blob (_reception_online.py). Brief schreiben und Übersetzen nutzen den Chat-Assistenten
(Claude), Schlüssel ANTHROPIC_API_KEY und ANTHROPIC_WORKSPACE_ID beim Vercel-Projekt.

Sicherheit wie am Rechner (server.py): nur Aufrufe von der eigenen Seite (Herkunft), höchstens 3 MB je Anfrage, Grenze je Absender und Minute
(je Instanz). «Das weiss der Chat» fragt die Oberfläche online nicht ab (wie im Rivage); das PDF setzt online das Druckfenster des Browsers."""
from http.server import BaseHTTPRequestHandler
import os, random, re, sys, threading, time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import _speicher as SP  # noqa: E402
import _reception_online as RO  # noqa: E402

RIEGEL = threading.RLock()
MONATE_ANSICHT = 3   # so viele Monate Fragen zeigt La Réception
WEG = re.compile(r'^/_?werkzeuge/reception/api/([a-z_]+)$')
GRENZEN = {'alle': 900, 'schreiben': 120, 'formular': 6}   # formular: Gäste der Website, öffentlich
_ZAEHLER = {}


def zu_viel(wer, art):
    jetzt = time.time()
    l = [t for t in _ZAEHLER.get((wer, art), []) if jetzt - t < 60]
    if len(l) >= GRENZEN[art]:
        _ZAEHLER[(wer, art)] = l
        return True
    l.append(jetzt); _ZAEHLER[(wer, art)] = l
    return False


class handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _lauf(self, schreibt):
        pfad, q = SP.weg_von(self.path)
        m = WEG.match(pfad)
        if not m:
            return SP.sende(self, 404, {'fehler': 'WEG · Unbekannter Weg.'})
        was = m.group(1)
        host = (self.headers.get('x-forwarded-host') or self.headers.get('Host') or '').split(',')[0].strip()
        herkunft = self.headers.get('Origin') or ''
        if herkunft and herkunft not in ('https://' + host, 'http://' + host if re.match(r'(localhost|127\.0\.0\.1)(:\d+)?$', host) else ''):   # http nur für vercel dev am Rechner
            return SP.sende(self, 403, {'fehler': 'HERKUNFT · Nicht erlaubt.'})
        if schreibt and not herkunft:
            return SP.sende(self, 403, {'fehler': 'HERKUNFT · Nur von der eigenen Seite.'})
        if not schreibt and (self.headers.get('Sec-Fetch-Site') or 'same-origin') not in ('same-origin', 'none'):   # Lesen nur von der eigenen Seite, wie am Rechner (E15; Prüfung 17.10.2026: online fehlte es)
            return SP.sende(self, 403, {'fehler': 'HERKUNFT · Nur von der eigenen Seite.'})
        wer = (self.headers.get('x-forwarded-for') or '').split(',')[0].strip() or self.client_address[0]
        with RIEGEL:
            if zu_viel(wer, 'alle') or (schreibt and zu_viel(wer, 'formular' if was == 'formular' else 'schreiben')):
                return SP.sende(self, 429, {'fehler': 'GRENZE · Zu viele Anfragen in kurzer Zeit. Bitte eine Minute warten.'}, kopf={'Retry-After': '60'})
            if was == 'zustand' and not schreibt:
                return SP.antwort(self, RO.zustand)
            if was == 'export' and not schreibt:   # alle Daten als eine Datei: Anfragen, zwölf Monate Fragen, Nachträge
                try:
                    RO.laden(13)
                    import datetime, io, zipfile
                    b = io.BytesIO()
                    with zipfile.ZipFile(b, 'w', zipfile.ZIP_DEFLATED) as z:
                        for w, _, fs in os.walk(RO.DATEN):
                            for f in sorted(fs):
                                if not f.endswith(('.gut', '.neu')) and not f.startswith('.'):
                                    z.write(os.path.join(w, f), os.path.join('la-reception', os.path.relpath(os.path.join(w, f), RO.DATEN)))
                    return SP.sende(self, 200, b.getvalue(), 'application/zip', {'Content-Disposition': f'attachment; filename="Der-Gastgeber-Landgasthof-Ruedihus-{datetime.date.today().isoformat()}.zip"'})
                except SP.Fehler as e:
                    return SP.sende(self, 500, {'fehler': str(e)})
            if schreibt and was == 'brief_pdf':   # kein Chromium in der Funktion: die Oberfläche öffnet das Druckfenster (ruedihus.css «Drucken»)
                return SP.sende(self, 501, {'fehler': 'DRUCK · Online setzt der Browser das PDF.'})
            if schreibt and was in ('fehler', 'fehler_leeren'):
                d = SP.koerper(self, 20000) if was == 'fehler' else {}
                if was == 'fehler':
                    print('Browserfehler La Réception:', str(d.get('text', ''))[:600], flush=True)
                return SP.sende(self, 200, {'ok': True})

            def tun():
                if schreibt:
                    d = SP.koerper(self, 12000 if was == 'formular' else 3 * 1024 * 1024)
                    if not isinstance(d, dict):
                        raise ValueError('EINGABE · Kein Objekt.')
                    if was == 'formular':   # Gäste der Website: Probe nur aus einer Seite mit ?probe=1, die Antwort trägt keine Daten des Hauses
                        d['probe'] = 'probe=1' in (self.headers.get('Referer') or '')
                    zusatz = [RO.monat_von(d['id'])] if was in ('frage', 'weg') and isinstance(d.get('id'), str) and d['id'].startswith('fragen/') else []
                    zusatz += [RO.monat_von(d['quelle'])] if was == 'nachtragen' and isinstance(d.get('quelle'), str) and d['quelle'].startswith('fragen/') else []
                    A = RO.laden(MONATE_ANSICHT, zusatz)
                    if was in ('entwurf', 'uebersetzen'):
                        RO.gast()
                    aus = RO.R.post(was, d)
                    RO.sichern(A)
                    return aus
                A = RO.laden(MONATE_ANSICHT)
                aus = RO.R.get(was, q)
                try:   # get() legt beim ersten Aufruf die Beispiele an; ohne Sichern lebten sie nur in dieser Instanz
                    RO.sichern(A, zusammenfuehren=True)
                except SP.Fehler:
                    pass
                if was == 'ueberblick':
                    aus['speicher'] = 'Blob' if SP.TOKEN else 'Vorführung'
                if random.random() < 0.02:
                    try:
                        RO.aufraeumen()
                    except SP.Fehler:
                        pass
                return aus
            return SP.antwort(self, tun)

    def do_GET(self):
        return self._lauf(False)

    def do_POST(self):
        return self._lauf(True)
