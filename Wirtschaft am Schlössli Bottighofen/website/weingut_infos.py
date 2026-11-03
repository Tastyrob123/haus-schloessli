# Angaben zu den Weingütern (Robert 19.10.2026: «Informationen zum Weingut»).
# Quelle: Wikipedia (Deutsch, sonst Englisch), Einleitung des Artikels über das Weingut. Nur Artikel, deren Titel den Namen des Erzeugers trägt
# und deren Text von Wein handelt; danach von Hand geprüft (Liste FALSCH). Roh: _quelle/wein-bilder/wikipedia.json
import json, pathlib, re, time, urllib.parse, urllib.request
import wein_bilder as WB

UA = {'User-Agent': 'TastyStudios-Designstudie/1.0 (robert@tasty-studios.de)'}
ZIEL = WB.QUELLE / 'wikipedia.json'
WEINWORT = re.compile(r'wein|weingut|winzer|champagner|champagne|wine|winery|domaine|vineyard|vigneron|cantina|bodega|cave', re.I)
# Von Hand geprüft: Artikel über etwas anderes als das Weingut der Karte
FALSCH = {'Miraval', 'Domaine des Lambrays'}


def api(sprache, p):
    u = f'https://{sprache}.wikipedia.org/w/api.php?' + urllib.parse.urlencode({**p, 'format': 'json'})
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))


def suche(erz):
    kern = WB.kern(erz)
    for sprache in ('de', 'en'):
        for q in (erz, erz + ' Wein'):
            try:
                d = api(sprache, {'action': 'query', 'list': 'search', 'srsearch': q, 'srlimit': 4})
            except Exception:
                continue
            for h in d['query']['search']:
                t = h['title']
                if not (kern and len(kern & WB.kern(t)) >= max(1, min(2, len(kern)))):
                    continue
                e = api(sprache, {'action': 'query', 'prop': 'extracts', 'exintro': 1, 'explaintext': 1, 'titles': t, 'redirects': 1})
                text = next(iter(e['query']['pages'].values())).get('extract', '')
                if text and WEINWORT.search(text[:600]):
                    return {'sprache': sprache, 'titel': t, 'text': text.strip(), 'url': f'https://{sprache}.wikipedia.org/wiki/' + urllib.parse.quote(t.replace(' ', '_'))}
            time.sleep(.3)
    return None


if __name__ == '__main__':
    roh = json.loads(ZIEL.read_text()) if ZIEL.exists() else {}
    for erz in sorted({w['erzeuger'] for w in WB.WEINE if w['erzeuger']}):
        if erz in roh:
            continue
        roh[erz] = suche(erz)
        ZIEL.write_text(json.dumps(roh, ensure_ascii=False, indent=1))
    print('gefunden', sum(1 for v in roh.values() if v), 'von', len(roh))
