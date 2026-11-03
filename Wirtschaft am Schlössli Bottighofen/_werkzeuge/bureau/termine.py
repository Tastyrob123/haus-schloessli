"""Termine der Wirtschaft am Schlössli im Schaufenster (Nachtbau 3.11.2026, Aufbau aus dem Culinarium vom 28.10.2026): die Ferien des Hauses als Daten, nie als Text.

Die Website trägt die Ferien an zwei Stellen: als Daten in jedem Reservationsfenster (data-zu="2026-11-13/2026-11-15,…": an diesen Tagen lässt der
Kalender keinen Tisch wählen) und als Zeile «Ferien …» unter den Öffnungszeiten der Startseite (.ab__ferien). Beides baut website/bau.py aus
website/inhalt/haus.json › ferien_iso und ferien. Diese Angaben sind der Ursprung: sie werden gelesen, nie abgetippt und nie verändert.
Hier liegen dazu Entwurf, veröffentlichter Stand und Verlauf (Master Werkzeug-Bau 2.2), in einer Datei mit Sicherung der letzten guten Fassung (.gut).
Ausgeliefert wird der Stand, indem der Server des Schaufensters die Seiten der Probe-Kopie beim Ausliefern mit ihm füllt (fuelle()); ohne Änderung
bleibt jede Seite Byte für Byte, wie die Website sie gebaut hat. Die Anlässe (haus.json › anlaesse) zeigt die Ansicht zum Nachschlagen; ihre Texte
und Fotos pflegt der Bereich «Anlässe» des Stamms.

Jede Anfrage, die den Entwurf ersetzt, trägt dessen Fingerabdruck (erwartet); passt er nicht mehr: KONFLIKT (409, L13).
Meldungen in der Form STICHWORT · Text (Master 2.6), jedes Stichwort steht im Lexikon der Prüfseite (pruefung-haus.js)."""
import datetime
import hashlib
import html
import json
import os
import re
import threading
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
QUELLE = HIER.parent.parent / 'website' / 'inhalt' / 'haus.json'
DATEN = Path(os.environ['WERKZEUGE_DATEN']) / 'bureau-termine' if os.environ.get('WERKZEUGE_DATEN') else HIER / '_daten'
DATEI = DATEN / 'termine.json'
WER = 'Team Schlössli'
HOECHSTENS = 12
LAENGSTENS = 120   # Tage je Ferienblock
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
_SCHLOSS = threading.Lock()
ZU = re.compile(r'data-zu="[^"]*"')
ZEILE = re.compile(r'(<p class="ab__ferien[^"]*"[^>]*><b>Ferien</b> )(.*?)(</p>)', re.S)


class Fehler(Exception):
    def __init__(self, status, stichwort, text):
        super().__init__(text)
        self.status, self.stichwort, self.text = status, stichwort, text


def _haus():
    try:
        return json.loads(QUELLE.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        raise Fehler(503, 'termine-quelle', 'TERMINE · website/inhalt/haus.json ist nicht lesbar.')


def ursprung():
    """Die Ferien, wie die Website sie gebaut hat: haus.json › ferien_iso (von, bis), der Anlass in Klammern aus haus.json › ferien."""
    h = _haus()
    iso, text = h.get('ferien_iso'), h.get('ferien') or []
    if not isinstance(iso, list):
        raise Fehler(503, 'termine-quelle', 'TERMINE · In haus.json stehen keine Ferien («ferien_iso») mehr. Die Website wurde umgebaut; die Ferien lassen sich erst wieder pflegen, wenn die Angabe da ist.')
    aus = []
    for i, paar in enumerate(iso):
        m = re.search(r'\(([^)]*)\)', text[i]) if i < len(text) else None
        try:
            aus.append(pruefe_einen({'id': f'f{i + 1}', 'von': paar[0], 'bis': paar[1], 'grund': m.group(1) if m else ''}, i))
        except (Fehler, IndexError, TypeError) as e:
            raise Fehler(503, 'termine-quelle', f'TERMINE · Die Ferien in haus.json sind nicht lesbar ({getattr(e, "text", e)}).')
    return aus


def anlaesse():
    """Die Anlässe des Hauses zum Nachschlagen (Titel, Datum, Zeit, ob bevorstehend), nur gelesen."""
    return [{'titel': a.get('titel', ''), 'datum': a.get('datum', ''), 'zeit': a.get('zeit', ''), 'bevorstehend': bool(a.get('bevorstehend'))}
            for a in _haus().get('anlaesse') or []]


def fingerabdruck(liste):
    return hashlib.sha1(json.dumps(liste, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()[:12]


def _tag(s, nr, was):
    try:
        return datetime.date.fromisoformat(str(s or ''))
    except ValueError:
        raise Fehler(400, 'termin-datum', 'DATUM · ' + nr + f'Der Tag «{was}» fehlt oder gibt es nicht.')


def pruefe_einen(t, i=0):
    """Ein Ferienblock: erster und letzter Tag, Anlass (frei, kurz). Alles andere wird abgelehnt (keine fremden Felder auf die Website)."""
    if not isinstance(t, dict):
        raise Fehler(400, 'termin-falsch', 'FERIEN · Ein Eintrag ist kein Ferienblock.')
    nr = f'Ferien {i + 1}: '
    tid = str(t.get('id') or '')
    if not re.fullmatch(r'[a-z0-9-]{1,24}', tid):
        raise Fehler(400, 'termin-falsch', 'FERIEN · ' + nr + 'Kennung fehlt.')
    von, bis = _tag(t.get('von'), nr, 'von'), _tag(t.get('bis'), nr, 'bis')
    if bis < von:
        raise Fehler(400, 'termin-reihe', 'REIHENFOLGE · ' + nr + 'Der letzte Tag liegt vor dem ersten.')
    if (bis - von).days + 1 > LAENGSTENS:
        raise Fehler(400, 'termin-lang', f'DAUER · {nr}Ein Ferienblock dauert höchstens {LAENGSTENS} Tage.')
    grund = re.sub(r'\s+', ' ', str(t.get('grund') or '')).strip()
    if len(grund) > 60:
        raise Fehler(400, 'termin-grund', 'ANLASS · ' + nr + 'Der Anlass ist länger als 60 Zeichen.')
    if re.search(r'[<>{}()\[\]]', grund):
        raise Fehler(400, 'termin-grund', 'ANLASS · ' + nr + 'Im Anlass stehen Zeichen, die auf der Website nicht stehen dürfen (Klammern, < >).')
    return {'id': tid, 'von': von.isoformat(), 'bis': bis.isoformat(), 'grund': grund}


def pruefe(liste):
    if not isinstance(liste, list):
        raise Fehler(400, 'termin-falsch', 'FERIEN · Die Anfrage enthält keine Liste.')
    if len(liste) > HOECHSTENS:
        raise Fehler(400, 'termin-viele', f'FERIEN · Höchstens {HOECHSTENS} Ferienblöcke stehen gleichzeitig auf der Website.')
    aus = sorted((pruefe_einen(t, i) for i, t in enumerate(liste)), key=lambda t: (t['von'], t['bis']))
    if len({t['id'] for t in aus}) != len(aus):
        raise Fehler(400, 'termin-falsch', 'FERIEN · Zwei Einträge tragen dieselbe Kennung.')
    for a, b in zip(aus, aus[1:]):
        if b['von'] <= a['bis']:
            raise Fehler(400, 'termin-doppelt', 'ÜBERSCHNEIDUNG · Zwei Ferienblöcke überschneiden sich. Bitte zu einem zusammenlegen.')
    return aus


def text(t):
    """Wie die Website einen Block schreibt: «22. Dezember 2026 bis 10. Februar 2027», im selben Monat «13. bis 15. November 2026», Anlass in Klammern."""
    a, b = datetime.date.fromisoformat(t['von']), datetime.date.fromisoformat(t['bis'])
    if a == b:
        s = f'{a.day}. {MONATE[a.month - 1]} {a.year}'
    elif (a.year, a.month) == (b.year, b.month):
        s = f'{a.day}. bis {b.day}. {MONATE[b.month - 1]} {b.year}'
    elif a.year == b.year:
        s = f'{a.day}. {MONATE[a.month - 1]} bis {b.day}. {MONATE[b.month - 1]} {b.year}'
    else:
        s = f'{a.day}. {MONATE[a.month - 1]} {a.year} bis {b.day}. {MONATE[b.month - 1]} {b.year}'
    return s + (f' ({t["grund"]})' if t.get('grund') else '')


def _leer():
    return {'entwurf': None, 'stand': None, 'verlauf': [], 'protokoll': []}


def lade():
    """Datei lesen; ist sie beschädigt, die letzte gute Fassung, nie still leer (Master 5.1)."""
    for p in (DATEI, DATEI.with_suffix('.json.gut')):
        if p.is_file():
            try:
                d = json.loads(p.read_text(encoding='utf-8'))
                if isinstance(d, dict) and 'verlauf' in d:
                    return d
            except ValueError:
                continue
    if DATEI.is_file():
        raise Fehler(500, 'termine-speicher', 'SPEICHER · Die Datei der Ferien und ihre Sicherung sind beide unlesbar. Prüfung öffnen.')
    return _leer()


def schreib(d):
    DATEN.mkdir(parents=True, exist_ok=True)
    if DATEI.is_file():
        try:
            json.loads(DATEI.read_text(encoding='utf-8'))
            DATEI.replace(DATEI.with_suffix('.json.gut'))
        except ValueError:
            pass
    tmp = DATEI.with_suffix('.tmp')
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    tmp.replace(DATEI)


def jetzt():
    return time.strftime('%Y-%m-%dT%H:%M:%S')


def lage(d=None):
    """Was die Ansicht braucht: Ursprung, Stand (veröffentlicht), Entwurf (falls einer wartet), Verlauf, Fingerabdruck des Entwurfs, Anlässe."""
    d = d or lade()
    u = ursprung()
    stand = d['stand'] if d['stand'] is not None else u
    entwurf = d['entwurf']
    return {'ursprung': u, 'stand': stand, 'entwurf': entwurf, 'wartet': entwurf is not None and entwurf != stand,
            'kennung': fingerabdruck(entwurf if entwurf is not None else stand),
            'zuletzt': next((v for v in reversed(d['verlauf']) if v.get('art') == 'veroeffentlicht'), None),
            'verlauf': [{'nr': i, 'zeit': v['zeit'], 'art': v['art'], 'notiz': v.get('notiz', ''), 'zahl': len(v['termine'])} for i, v in enumerate(d['verlauf'])][::-1],
            'anlaesse': anlaesse(), 'heute': datetime.date.today().isoformat(),
            'quelle': 'website/inhalt/haus.json › ferien_iso, ferien'}


def wartend(l):
    """Wie viele Ferienblöcke sich zwischen Stand und Entwurf unterscheiden (neu, geändert, entfällt), wie die Ansicht sie zählt."""
    if not l['wartet']:
        return 0
    alt, neu = {t['id']: t for t in l['stand']}, {t['id']: t for t in l['entwurf']}
    return sum(1 for k, t in neu.items() if alt.get(k) != t) + sum(1 for k in alt if k not in neu)


def _bewache(d, erwartet):
    l = lage(d)
    if erwartet != l['kennung']:
        raise Fehler(409, 'konflikt', 'KONFLIKT · In einem anderen Fenster wurden die Ferien inzwischen geändert. Die Liste lädt neu, Ihre Eingaben bleiben stehen.')
    return l


def _protokoll(d, was):
    d['protokoll'] = (d['protokoll'] + [{'zeit': jetzt(), 'wer': WER, 'was': was}])[-400:]


def speichern(liste, erwartet):
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        neu = pruefe(liste)
        alt = l['entwurf'] if l['entwurf'] is not None else l['stand']
        if neu == alt:
            return {'nichts': True, 'meldung': 'Nichts geändert, nichts gespeichert.', **lage(d)}
        d['entwurf'] = None if neu == l['stand'] else neu
        _protokoll(d, 'Ferien im Entwurf gespeichert')
        schreib(d)
        return {'vorher': alt, **lage(d)}


def veroeffentlichen(erwartet, notiz=''):
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        if not l['wartet']:
            return {'nichts': True, 'meldung': 'Nichts geändert, nichts veröffentlicht.', **l}
        d['stand'] = l['entwurf']
        d['entwurf'] = None
        d['verlauf'] = (d['verlauf'] + [{'zeit': jetzt(), 'art': 'veroeffentlicht', 'notiz': str(notiz or '')[:200], 'termine': d['stand']}])[-60:]
        _protokoll(d, 'Ferien veröffentlicht')
        schreib(d)
        return lage(d)


def verwerfen(erwartet):
    with _SCHLOSS:
        d = lade()
        _bewache(d, erwartet)
        vorher = d['entwurf']
        d['entwurf'] = None
        _protokoll(d, 'Entwurf der Ferien verworfen')
        schreib(d)
        return {'vorher': vorher, **lage(d)}


def zurueckholen(nr, erwartet):
    """Eine frühere Fassung (nr im Verlauf) oder den Ursprung («ursprung») in den Entwurf holen, nie direkt auf die Website (R14)."""
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        if nr == 'ursprung':
            t = l['ursprung']
        else:
            try:
                t = d['verlauf'][int(nr)]['termine']
            except (ValueError, IndexError, TypeError):
                raise Fehler(404, 'fassung-unbekannt', 'FASSUNG · Diese frühere Fassung gibt es nicht.')
        d['entwurf'] = None if t == l['stand'] else t
        _protokoll(d, 'Frühere Fassung der Ferien in den Entwurf geholt')
        schreib(d)
        return lage(d)


def fuelle(roh, liste, u):
    """Eine Seite der Website mit einer Liste füllen: data-zu der Reservationsfenster und die Zeile «Ferien» der Startseite.
    Gleich wie der Ursprung: unverändert zurück (Byte für Byte, wie gebaut)."""
    if liste == u:
        return roh
    zu = ','.join(f'{t["von"]}/{t["bis"]}' for t in liste)
    roh = ZU.sub(f'data-zu="{zu}"', roh)
    zeile = ' <i>·</i> '.join(f'<span>{html.escape(text(t), quote=False)}</span>' for t in liste) or '<span>Zurzeit sind keine Betriebsferien geplant</span>'
    return ZEILE.sub(lambda m: m.group(1) + zeile + m.group(3), roh)


def ausliefern(roh, welche='stand'):
    l = lage()
    liste = l['entwurf'] if welche == 'entwurf' and l['entwurf'] is not None else l['stand']
    return fuelle(roh, liste, l['ursprung'])


def pruefung():
    """Punkte für die Prüfseite: Quelle lesbar, Speicher lesbar, Sicherung da, Stand gültig."""
    p = []
    try:
        u = ursprung()
        p.append({'gut': True, 'titel': 'Ferien der Website', 'text': f'{len(u)} Ferienblöcke in website/inhalt/haus.json gelesen.'})
    except Fehler as e:
        return [{'gut': False, 'titel': 'Ferien der Website', 'text': e.text, 'stichwort': e.stichwort}]
    try:
        d = lade()
        for k in ('stand', 'entwurf'):
            if d[k] is not None:
                pruefe(d[k])
        p.append({'gut': True, 'titel': 'Speicher der Ferien', 'text': 'lesbar' + (', Sicherung der letzten guten Fassung liegt daneben' if DATEI.with_suffix('.json.gut').is_file() else ', noch nichts gespeichert') + '.'})
    except Fehler as e:
        p.append({'gut': False, 'titel': 'Speicher der Ferien', 'text': e.text, 'stichwort': e.stichwort})
    return p
