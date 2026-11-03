"""Probe-Antworten statt Claude (Robert 16.10.2026: «lokal bis zur Kostenrunde», keine bezahlten KI-Aufrufe in Prüfläufen).

Im Schlössli ist das der Standard: python3 _werkzeuge/reception/server.py 9047 (ohne RECEPTION_KI=1). Kopie aus dem Ruedihus, dort aus Carlton und Doldenhorn.
Dann ruft kein Teil des Reservationsbuchs und vom Chat die KI auf und kein Schlüssel wird gelesen. Jede Stelle, die sonst Claude fragt, bekommt
eine Antwort in genau der Form, die Claude liefern würde, sichtbar als Probe beschriftet:
  Chat (gast.frage)        Text «Probe-Antwort ohne KI …»; nennt der Gast eine E-Mail oder Telefonnummer, ruft die Probe das Werkzeug «anfrage» auf
                           (so entsteht wie echt eine Anfrage im Eingang); enthält die Frage «lücke», meldet sie «nicht belegt».
  Brief (gast.anfrage)     «Betreff: …», Brief mit Anrede, offenen Stellen [in Klammern] und Gruss, darunter «---» mit Punkten fürs Team.
  Übersetzen               JSON mit betreff, text und verlauf in gleicher Länge.
  Wissen einlesen          Werkzeug «eintraege» mit einem Eintrag je Material.
"""
import json, re, time

BEREICH = 'Das Haus'


def _text(koerper):
    """Alles, was der Aufruf an Text mitschickt (System und Nachrichten), für die Erkennung der Stelle."""
    s = koerper.get('system')
    sys_t = s if isinstance(s, str) else ' '.join(b.get('text', '') for b in (s or []) if isinstance(b, dict))
    msg = []
    for m in koerper.get('messages') or []:
        c = m.get('content')
        if isinstance(c, str):
            msg.append(c)
        else:
            msg += [b.get('text', '') for b in c or [] if isinstance(b, dict) and b.get('type') == 'text']
    return sys_t, msg


def _antwort(text='', werkzeug=None):
    inhalt = [{'type': 'text', 'text': text}] if text else []
    if werkzeug:
        inhalt.append({'type': 'tool_use', 'id': 'toolu_probe', 'name': werkzeug[0], 'input': werkzeug[1]})
    return {'content': inhalt, 'stop_reason': 'tool_use' if werkzeug else 'end_turn', 'usage': {'input_tokens': 0, 'output_tokens': 0}}


def api(koerper):
    sys_t, msg = _text(koerper)
    werkzeuge = [w.get('name') for w in koerper.get('tools') or []]
    letzte = msg[-1] if msg else ''
    if 'eintraege' in werkzeuge:                                    # Wissen einlesen (gedaechtnis._auszug)
        m = re.search(r'BEREICH DES TEAMS: (.+)', letzte)
        bereich = (m.group(1).strip() if m else '') or BEREICH
        roh = ' '.join(msg)
        stueck = re.sub(r'\s+', ' ', roh.split('TEXT DES TEAMS:', 1)[-1] if 'TEXT DES TEAMS:' in roh else roh)[-220:].strip()
        return _antwort(werkzeug=('eintraege', {'grund': 'Probe ohne KI', 'eintraege': [
            {'bereich': bereich, 'titel': 'Probe-Eintrag', 'text': 'Probe ohne KI: ' + stueck, 'gueltig_bis': None}]}))
    if sys_t.startswith('Du übersetzt'):                             # reception.uebersetzen
        try:
            d = json.loads(letzte)
        except ValueError:
            d = {}
        return _antwort(json.dumps({'betreff': '[Probe] ' + str(d.get('betreff', '')), 'text': '[Probe-Übersetzung ohne KI]\n\n' + str(d.get('text', '')),
                                    'verlauf': ['[Probe] ' + str(v) for v in d.get('verlauf') or []]}, ensure_ascii=False))
    if 'ANFRAGE:' in letzte:                                         # gast.anfrage (Brief)
        name = (re.search(r'Name:\s*(.+)', letzte) or re.search(r'"name":\s*"([^"]+)"', letzte))
        wer = name.group(1).strip() if name else 'Gast'
        allerg = (re.search(r'Allergien \(Formular\):\s*(.+)', letzte) or [None, ''])[1].strip()
        satz_al = f'Ihre Angaben zu Allergien ({allerg}) geben wir an die Küche weiter [Küche informieren].\n\n' if allerg and allerg != 'keine angegeben' else ''
        return _antwort(f'Betreff: Ihre Anfrage in der Wirtschaft am Schlössli (Probe)\n\nGuten Tag {wer}\n\n'
                        'Vielen Dank für Ihre Anfrage. Dies ist ein Probe-Brief ohne KI, damit sich Gestalten, PDF und Text prüfen lassen.\n\n'
                        f'Für Ihr Datum [Verfügbarkeit prüfen] und [Tisch bestätigen].\n\n{satz_al}'
                        'Damit wir alles in Ruhe vorbereiten können:\n- Uhrzeit\n- Anzahl Personen\n\n'
                        'Mit freundlichen Grüssen\n\n[Name]\nWirtschaft am Schlössli'
                        '\n---\nGrundlage: Probe ohne KI\nOffen: Verfügbarkeit, Bestätigung')
    # Chat (gast.frage, auch der zweite Schritt nach der Buchungsmaske)
    if any(isinstance(m.get('content'), list) and any(b.get('type') == 'tool_result' for b in m['content']) for m in koerper.get('messages') or []):
        return _antwort('OK')
    frage = letzte.strip()
    kontakt = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+|(?:\+|00)\d[\d\s]{7,}\d', frage)
    if kontakt and 'anfrage' in werkzeuge:
        name = re.search(r'(?:ich bin|mein name ist|name:|my name is|je suis)\s+([A-ZÄÖÜ][\w-]+(?:\s+[A-ZÄÖÜ][\w-]+)?)', frage, re.I)
        pers = re.search(r'(\d{1,3})\s*(?:personen|gäste|persons|people|personnes)', frage, re.I)
        art = 'bankett' if re.search(r'bankett|feier|fest\b|geburtstag|hochzeit|party|birthday|wedding|firmen', frage, re.I) else ('gutschein' if re.search(r'gutschein|voucher', frage, re.I) else 'tisch')
        return _antwort('Probe-Antwort ohne KI: Dies ist ein Entwurf, Ihre Anfrage geht nicht an das Haus. Für eine echte Anfrage hilft das Team am Telefon.',
                        ('anfrage', {'art': art, 'name': name.group(1) if name else 'Probe Gast', 'kontakt': kontakt.group(0), 'datum': None,
                                     'personen': int(pers.group(1)) if pers else None, 'anliegen': 'Probe ohne KI: ' + frage[:300]}))
    if 'lücke' in frage.lower() or 'luecke' in frage.lower():
        return _antwort('Probe-Antwort ohne KI: Dazu steht nichts in meinen Unterlagen.', ('nicht_belegt', {'thema': frage[:80]}))
    return _antwort('Probe-Antwort ohne KI auf «' + frage[:160] + '» (' + time.strftime('%H:%M') + ' Uhr). In der Demo ist der Chat noch nicht angeschlossen; im Betrieb antwortet er hier aus dem Wissen des Hauses.')   # Uhrzeit: Prüfläufe erkennen daran, dass eine Antwort kam
