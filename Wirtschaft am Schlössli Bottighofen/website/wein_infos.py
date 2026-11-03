# Geschmack, Speisen, Rebsorten und Weinstil je Wein (Robert 19.10.2026: «wie der schmeckt, wie der hergestellt wird, wo der herkommt, Informationen zum Weingut»).
# Quelle: die öffentliche Weinseite bei Vivino (vivino.com/w/<id>), nur für Weine, deren Erzeuger UND Wein sicher zugeordnet sind (wie in wein_bilder.py).
# Gespeichert wird roh in _quelle/wein-bilder/seiten/<vivino-id>.json, nichts wird erfunden.
#   python3 wein_infos.py holen   lädt fehlende Seiten (langsam, eine je Sekunde)
import json, pathlib, re, sys, time, urllib.request
import wein_bilder as WB

HIER = pathlib.Path(__file__).resolve().parent
SEITEN = WB.QUELLE / 'seiten'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15'


def zuordnung():
    """Wein der Karte -> Vivino-Wein, nur bei sicherem Treffer (Erzeuger passt, Name zu mindestens zwei Dritteln, nicht von Hand ausgeschlossen)."""
    z = {}
    for w in WB.WEINE:
        r = WB.ROH.get(str(w['id']), {})
        alle = [h for t in ('a', 'b', 'c') for h in r.get(t, [])]
        best, wert = None, 0
        for h in alle:
            if WB.passt_erz(w, h):
                s = WB.name_wert(w, h)
                if s > wert:
                    best, wert = h, s
        if best and wert >= .67 and w['id'] not in WB.NICHT:
            z[w['id']] = best['id']
    return z


def hole(vid):
    ziel = SEITEN / f'{vid}.json'
    if ziel.exists():
        return json.loads(ziel.read_text())
    roh = urllib.request.urlopen(urllib.request.Request(f'https://www.vivino.com/w/{vid}', headers={'User-Agent': UA, 'Accept-Language': 'de-CH,de;q=0.9'}), timeout=40).read().decode('utf-8', 'replace')
    m = re.search(r'winePageInformation\s*=\s*', roh)
    if not m:
        return None
    d, _ = json.JSONDecoder().raw_decode(roh[m.end():])
    w = d.get('wine') or {}
    st = w.get('style') or {}
    kurz = {
        'id': vid, 'name': w.get('name'), 'weingut': (w.get('winery') or {}).get('name'),
        'region': (w.get('region') or {}).get('name'), 'region_id': (w.get('region') or {}).get('id'),
        'alkohol': w.get('alcohol'), 'verschluss': w.get('closure'), 'natur': w.get('is_natural'),
        'reben': [g.get('name') for g in (w.get('grapes') or [])],
        'speisen': [f.get('name') for f in (w.get('foods') or [])],
        'struktur': ((d.get('tastes') or {}).get('structure')),
        'aromen': [{'gruppe': f.get('group'), 'n': (f.get('stats') or {}).get('mentions_count'), 'worte': [k.get('name') for k in (f.get('primary_keywords') or [])][:5]} for f in ((d.get('tastes') or {}).get('flavor') or [])],
        'stil': {k: st.get(k) for k in ('id', 'name', 'description', 'blurb', 'interesting_facts', 'body', 'body_description', 'acidity', 'acidity_description')} if st else None,
        'bewertung': (w.get('statistics') or {}).get('ratings_average'), 'bewertungen': (w.get('statistics') or {}).get('ratings_count'),
        'weingut_weine': (((w.get('winery') or {}).get('statistics')) or {}).get('wines_count'),
        'gelesen': time.strftime('%Y-%m-%d'),
    }
    ziel.write_text(json.dumps(kurz, ensure_ascii=False, indent=1))
    return kurz


if __name__ == '__main__':
    SEITEN.mkdir(parents=True, exist_ok=True)
    z = zuordnung()
    (WB.QUELLE / 'vivino_wein.json').write_text(json.dumps(z, indent=1))
    print('sicher zugeordnet', len(z), 'eindeutige Seiten', len(set(z.values())), flush=True)
    if sys.argv[1:] == ['holen']:
        for i, vid in enumerate(sorted(set(z.values()))):
            if (SEITEN / f'{vid}.json').exists():
                continue
            try:
                hole(vid)
            except Exception as ex:
                print('fehlt', vid, ex, flush=True)
            time.sleep(1.0)
            if i % 25 == 0:
                print(i, flush=True)
        print('fertig', len(list(SEITEN.glob('*.json'))), flush=True)


def geschmack(vid):
    """Struktur und Aromen über die Geschmacks-Abfrage von Vivino (die Weinseite liefert sie nicht mit), in dieselbe Datei."""
    ziel = SEITEN / f'{vid}.json'
    d = json.loads(ziel.read_text())
    if d.get('geschmack_geholt'):
        return
    t = json.load(urllib.request.urlopen(urllib.request.Request(f'https://www.vivino.com/api/wines/{vid}/tastes', headers={'User-Agent': UA, 'Accept': 'application/json'}), timeout=40)).get('tastes') or {}
    d['struktur'] = t.get('structure')
    d['aromen'] = [{'gruppe': f.get('group'), 'n': (f.get('stats') or {}).get('mentions_count'), 'worte': [k.get('name') for k in (f.get('primary_keywords') or [])][:5]} for f in (t.get('flavor') or [])]
    d['geschmack_geholt'] = True
    ziel.write_text(json.dumps(d, ensure_ascii=False, indent=1))


if __name__ == '__main__' and sys.argv[1:] == ['geschmack']:
    for i, f in enumerate(sorted(SEITEN.glob('*.json'))):
        try:
            geschmack(int(f.stem))
        except Exception as ex:
            print('fehlt', f.stem, ex, flush=True)
        time.sleep(.6)
    print('fertig geschmack', flush=True)


def bauen():
    """assets/data/wein-infos.json: je Wein der Karte die belegten Angaben, dazu Stile und Weingüter (deutsche Texte aus wein_texte.py)."""
    import wein_texte as T, weingut_recherche
    RECHERCHE = weingut_recherche.lies()
    z = {int(k): v for k, v in json.loads((WB.QUELLE / 'vivino_wein.json').read_text()).items()}
    VS = {'cork': 'Naturkorken', 'screw': 'Schraubverschluss', 'screwcap': 'Schraubverschluss', 'glass': 'Glasverschluss', 'synthetic': 'Kunststoffkorken'}
    weine, stile = {}, {}
    for w in WB.WEINE:
        x = {}
        if w['id'] in z:
            p = SEITEN / f'{z[w["id"]]}.json'
            d = json.loads(p.read_text()) if p.exists() else {}
            s = d.get('struktur') or {}
            st = {k: round(s[v], 1) for k, v in (('k', 'intensity'), ('sa', 'acidity'), ('su', 'sweetness'), ('t', 'tannin'), ('p', 'fizziness')) if s.get(v)}
            if st:
                x['s'] = st
                x['sn'] = (s.get('user_structure_count') or 0) + (s.get('calculated_structure_count') or 0)
            ar = sorted([a for a in d.get('aromen') or [] if a.get('n') and a.get('gruppe') in T.GRUPPE], key=lambda a: -a['n'])[:4]
            if ar:
                x['a'] = [[a['gruppe'], a['n'], [T.AROMA.get(k, k) for k in a['worte'][:3]]] for a in ar]
            if d.get('speisen'):
                x['sp'] = d['speisen'][:5]
            if d.get('reben'):
                x['rb'] = d['reben']
            if d.get('alkohol'):
                x['al'] = d['alkohol']
            if d.get('verschluss') in VS:
                x['vs'] = VS[d['verschluss']]
            sti = (d.get('stil') or {})
            if sti.get('id') in T.STILE:
                x['st'] = sti['id']
                stile[sti['id']] = {**T.STILE[sti['id']], 'koerper': T.KOERPER.get(sti.get('body')), 'saeure': sti.get('acidity_description')}
        if w['erzeuger'] in T.WEINGUT or w['erzeuger'] in RECHERCHE:
            x['wg'] = w['erzeuger']
        if x:
            weine[w['id']] = x
    # Die Erzählung je Wein (Robert 19.10.2026): woher er kommt ('hk'), was ihn ausmacht ('bes'), aus Region, Namen und belegten Angaben
    import wein_regionen as RG
    ART = {'Champagner & Schaumwein': 'Schaumwein', 'Weisswein': 'Weisswein', 'Rosé': 'Rosé', 'Rotwein': 'Rotwein', 'Süsswein': 'Süsswein'}
    for w in WB.WEINE:
        x = weine.setdefault(w['id'], {})
        hk = RG.REGION.get(w['region']) or RG.LAND.get(w['land'])
        if hk:
            x['hk'] = hk
        saetze = []
        name = (w['name'] or '')
        for wort, erkl in RG.BEGRIFF:
            if wort.lower() in name.lower() or wort.lower() in (w['notiz'] or '').lower():
                saetze.append(erkl)
                break
        reben = x.get('rb') or w['reben']
        st = stile.get(x.get('st')) if x.get('st') else None
        teil = []
        if reben:
            teil.append('aus ' + (', '.join(reben[:-1]) + ' und ' + reben[-1] if len(reben) > 1 else reben[0]))
        if w['jahr']:
            teil.append(f"vom Jahrgang {w['jahr']}")
        wo = RG.WO.get(w['region']) or ('in ' + w['region'] if w['region'] else RG.WO_LAND.get(w['land'], ''))
        saetze.insert(0, f"Ein {ART[w['art']]} " + (', '.join(teil) + ', gewachsen ' if teil else 'aus dem Keller eines Hauses ') + wo + '.')
        saetze[0] = saetze[0].replace('nennt grüner Apfel', 'nennt grünen Apfel')
        s_ = x.get('s') or {}
        glas = []
        if s_.get('k'): glas.append('leicht' if s_['k'] < 2.8 else 'mittelkräftig' if s_['k'] <= 3.8 else 'voll und dicht')
        if s_.get('sa'): glas.append('mit milder Säure' if s_['sa'] < 2.8 else 'mit ausgewogener Säure' if s_['sa'] <= 3.8 else 'mit frischer, lebendiger Säure')
        if s_.get('t'): glas.append('weichem Tannin' if s_['t'] < 2.5 else 'spürbarem Tannin' if s_['t'] <= 3.5 else 'kräftigem Tannin')
        if s_.get('su') and s_['su'] >= 3: glas.append('deutlich süss')
        if glas:
            saetze.append('Im Glas zeigt er sich ' + glas[0] + (', ' + ', '.join(glas[1:]) if glas[1:] else '') + '.')
        ar = x.get('a') or []
        worte = [k for a in ar[:3] for k in a[2][:2]]
        if worte:
            worte = list(dict.fromkeys(worte))[:5]
            saetze.append('Wer ihn trinkt, nennt ' + ', '.join(worte[:-1]) + (' und ' + worte[-1] if len(worte) > 1 else worte[0]) + '.')
            saetze[-1] = saetze[-1].replace('grüner Apfel', 'grünen Apfel').replace('gelber Apfel', 'gelben Apfel').replace('reifer Apfel', 'reifen Apfel').replace('weisser Pfirsich', 'weissen Pfirsich').replace('weisser Pfeffer', 'weissen Pfeffer').replace('schwarzer Trüffel', 'schwarzen Trüffel').replace('frischer Erdbeere', 'frische Erdbeere')
        if x.get('al'):
            saetze.append(f"{str(x['al']).replace('.', ',')} Prozent Alkohol" + (f", verschlossen mit {x['vs']}" if x.get('vs') else '') + '.')
        if st and st.get('koerper') and not glas:
            saetze.append(f"Weine dieses Stils haben meist {st['koerper'].lower()}" + (f" und {st['saeure'].lower()}e Säure" if st.get('saeure') else '') + '.')
        if len(w['flaschen']) > 1:
            saetze.append('Wir führen ihn in ' + ', '.join(f['gross'].replace('.', ',').replace('l', ' l') for f in w['flaschen'][:-1]) + ' und ' + w['flaschen'][-1]['gross'].replace('.', ',').replace('l', ' l') + '.')
        elif w['flaschen'] and w['flaschen'][0]['gross'] != '0.7l':
            g = w['flaschen'][0]['gross']
            saetze.append('Wir führen ihn als ' + ('halbe Flasche' if g == '0.375l' else 'Magnum' if g == '1.5l' else 'grosse Flasche mit ' + g.replace('.', ',').replace('l', ' Litern')) + '.')
        if saetze:
            x['bes'] = ' '.join(saetze)
    aus = {'weine': weine, 'stile': stile, 'weingut': {**RECHERCHE, **T.WEINGUT}, 'gruppen': T.GRUPPE}
    (HIER / 'assets' / 'data' / 'wein-infos.json').write_text(json.dumps(aus, ensure_ascii=False, separators=(',', ':')))
    print('Weine mit Angaben', len(weine), '· Geschmack', sum('s' in v for v in weine.values()), '· Aromen', sum('a' in v for v in weine.values()),
          '· Speisen', sum('sp' in v for v in weine.values()), '· Stil', sum('st' in v for v in weine.values()), '· Weingut', sum('wg' in v for v in weine.values()))


if __name__ == '__main__' and sys.argv[1:] == ['bauen']:
    bauen()
