"""Das Kartenpult · Wirtschaft am Schlössli — die Karten als Daten für die Website (Nachtbau 3.11.2026, C27 in der Form des Hauses).

Die Website zeigt die Karten aus ihren eigenen Daten (website/inhalt/karte.json, lunch.json, laestermeile.json, wein.json, bankett.json). Dieses Modul
liest aus jeder veröffentlichten Karte die Einträge (Rubrik, Name, Zeile, Preise; ausgeblendete zählen nicht) und schreibt alle Karten nach karten.json:
  _werkzeuge/carte/anschluss/karten.json          immer nach dem Veröffentlichen (im Revier des Werkzeugs, ändert die Website nicht)
Die Website liest die Datei erst, wenn ihr Bau sie vor website/inhalt/*.json nimmt (Einbau in website/, nicht Revier des Kartenpults; bis dahin
bleibt jede Seite der Website, wie sie ist)."""
import datetime, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(os.path.dirname(HIER))
WEIN = {'j': 'jahr', 'n': 'name', 'f': 'flasche', 'p': 'preis', 'd': 'notiz'}


def _klasse(n):
    m = re.search(r'\sclass="([^"]*)"', n['a'][1] or '')
    return m.group(1).split() if m else []


def _text(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict) and x.get('fn') == 'el' and not x.get('aus'):
        return ''.join(_text(y) for y in x['a'][2:])
    return ''


def zeilen(d):
    """Einträge der Karte: [{rubrik, name, zeile, preise, …}] in der Reihenfolge der Karte; ausgeblendete Einträge zählen nicht."""
    aus, rub = [], ['']

    def eintrag(x):
        e = {'rubrik': rub[0], 'name': '', 'zeile': '', 'preise': []}
        if 'sb-wein' in _klasse(x):
            fl = []
            for y in x['a'][2:]:
                if isinstance(y, dict) and y.get('fn') == 'el':
                    k = next((WEIN[c] for c in _klasse(y) if c in WEIN), '')
                    t = _text(y).strip()
                    if k == 'flasche':
                        fl.append({'gross': t, 'preis': ''})
                    elif k == 'preis' and fl:
                        fl[-1]['preis'] = t
                    elif k and t:
                        e[k] = t
            e['preise'] = fl
            return e

        def geh(y):
            if not isinstance(y, dict) or y.get('fn') != 'el' or y.get('aus'):
                return
            kl = _klasse(y)
            if 'sb-n' in kl:
                e['name'] = ''.join(z for z in y['a'][2:] if isinstance(z, str)).strip()
            elif 'sb-t' in kl:
                e['zeile'] = _text(y).strip()
            elif 'sb-al' in kl:
                e['allergene'] = _text(y).strip()
            elif 'sb-w' in kl:
                e['hinweis'] = _text(y).strip()
            if 'sb-mp' in kl:
                e['preise'].append(_text(y).strip())
            elif y['a'][0] == 'b':
                e['preise'].append(_text(y).strip())
            for z in y['a'][2:]:
                geh(z)
        for y in x['a'][2:]:
            geh(y)
        return e

    def geh(x):
        if not isinstance(x, dict) or x.get('aus'):
            return
        if x.get('fn') == 'seite':
            for y in x['a'][1:]:
                geh(y)
            return
        if x.get('fn') != 'el':
            return
        kl = _klasse(x)
        if 'sb-h' in kl or 'sb-land' in kl or 'sb-region' in kl or 'sb-gut' in kl:
            rub[0] = _text(x).strip()
            return
        if 'sb-g' in kl or 'sb-m' in kl:
            aus.append(eintrag(x))
            return
        for y in x['a'][2:]:
            geh(y)
    for s in d.get('seiten', []):
        geh(s)
    return aus


def karten_json(K, ziele, lies):
    """Alle veröffentlichten Karten (Stand) in der Form der Website."""
    aus = {'stand': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'quelle': 'Das Kartenpult (_werkzeuge/carte/_daten/stand/)', 'karten': {}}
    for z in ziele:
        s = lies(os.path.join(K, 'stand', z + '.json'))
        if s:
            aus['karten'][z] = dict(name=s.get('name', ''), eintraege=zeilen(s))
    return aus


def schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(p + '.neu', encoding='utf-8'))
    os.replace(p + '.neu', p)


def anschliessen(K, ziele, lies):
    """Nach jedem Veröffentlichen: karten.json im Revier des Werkzeugs (nie in website/)."""
    eigen = os.path.realpath(K) == os.path.realpath(os.path.join(HIER, '_daten'))   # Prüfläufe mit Wegwerf-Daten schreiben neben ihre Daten, nie über die Datei des Hauses
    schreib(os.path.join(HIER if eigen else K, 'anschluss', 'karten.json'), karten_json(K, ziele, lies))
    return 'anschluss/karten.json'


if __name__ == '__main__':
    sys.path.insert(0, HIER)
    import carte
    d = karten_json(carte.K, carte.ZIELE, carte._lies)
    schreib(os.path.join(HIER, 'anschluss', 'karten.json'), d)
    print('anschluss/karten.json:', {k: len(v['eintraege']) for k, v in d['karten'].items()})
