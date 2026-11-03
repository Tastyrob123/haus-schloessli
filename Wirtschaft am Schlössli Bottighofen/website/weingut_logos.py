# Logos der Weingüter für die Weinliste (Robert 19.10.2026: «ob man da noch irgendwie Logos findet … Logo klein, oder Wappen»).
# Quelle: die eigene Website jedes Weinguts (gefunden über die freie Suche von DuckDuckGo), dort das Logo im Kopf der Seite.
# Roh: _quelle/weingut-logos/ (seiten.json = Website je Weingut, logos.json = gefundene Datei). Jede Datei danach von Hand geprüft (Liste FALSCH).
# RECHTE: Marken der Weingüter, nur zur Anschauung in der Designstudie. Vor jeder Veröffentlichung Erlaubnis holen oder weglassen.
#   python3 weingut_logos.py suchen | holen | tafel
import json, pathlib, re, sys, time, urllib.parse, urllib.request, html as H, io, unicodedata
from concurrent.futures import ThreadPoolExecutor

HIER = pathlib.Path(__file__).resolve().parent
Q = HIER.parent / '_quelle' / 'weingut-logos'
Q.mkdir(parents=True, exist_ok=True)
ZIEL = HIER / 'assets' / 'img' / 'logo-weingut'
ZIEL.mkdir(parents=True, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15', 'Accept-Language': 'de-CH,de;q=0.9,en;q=0.8'}
WEINE = json.loads((HIER / 'assets' / 'data' / 'weine.json').read_text())
# Händler, Führer, Verzeichnisse: nie die Website des Weinguts
FREMD = re.compile(r'vivino|falstaff|martel|wine-searcher|wikipedia|wikidata|facebook|instagram|linkedin|youtube|tripadvisor|mondovino|globus|coop|gerstl|schuler|divo|amazon|decanter|cellartracker|jancisrobinson|winespectator|ebay|weinweg|kapweine|vinatis|millesima|idealwine|wine\.com|vinous|robertparker|wein\.plus|weinfreunde|hawesko|jacques|lavinia|uvinum|vinello|lobenbergs|xtrawine|tannico|callmewine|bernabei|vinum|weinhandel|caviste|vinatis|twil|mövenpick|moevenpick|smith|zweifel|baur-au-lac|bindella|delinat|ullrich|riegger|casa-del-vino|flaschenpost|weinclub|bolero|gaultmillau|guide|michelin|tasteatlas|duckduckgo|bing\.|google\.|sothebys|christies|liv-ex|winebid|klwines|totalwine|winelibrary|astorwines|winehouse|vinmonopolet|systembolaget|alko|saq\.com|lcbo|bcliquor|vinexus|weinco|wein-co|wineandco|grandcruselection|gourmondo|weinundco|belvini|superiore|weinfurore|hart-auf-hart|vinorama|vinoscout|weinkontor|vinocentral|weinbaule|wein-direkt', re.I)
LEER = set('weingut domaine domaines chateau champagne cave caves tenuta bodegas bodega maison weinbau weinkellerei kellerei castello cantina cantine familia famille family dr the de du la le les des et and von zum zur am der die das di del della y e by fils freres vinedos vignoble'.split())


def norm(s):
    s = (s or '').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('Ä', 'Ae').replace('Ö', 'Oe').replace('Ü', 'Ue')
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return [t for t in re.split(r'[^a-z0-9]+', s) if t and len(t) > 2 and t not in LEER]


def weingueter():
    d = {}
    for w in WEINE:
        if w['erzeuger']:
            d.setdefault(w['erzeuger'], {'land': w['land'], 'region': w['region']})
    return d


def lade(url, roh=False, t=15):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t)
    b = r.read()
    return (b, r.geturl(), r.headers.get('content-type', '')) if roh else b.decode('utf-8', 'ignore')


def suche(name):
    q = urllib.parse.quote_plus(name + ' Wein')
    s = lade('https://html.duckduckgo.com/html/?q=' + q)
    urls = [H.unescape(u) for u in re.findall(r'class="result__url" href="([^"]+)"', s)]
    toks = norm(name)
    beste = None
    for u in urls:
        host = urllib.parse.urlparse(u).netloc.lower().removeprefix('www.')
        if FREMD.search(host):
            continue
        hn = re.sub(r'[^a-z0-9]', '', host.split('.')[0] if host.count('.') <= 1 else host.rsplit('.', 2)[-2])
        treffer = [t for t in toks if t in hn or (len(hn) > 4 and hn in ''.join(toks))]
        if treffer:
            return {'url': 'https://' + urllib.parse.urlparse(u).netloc + '/', 'treffer': treffer, 'alle': urls[:6]}
        beste = beste or u
    return {'url': None, 'erste': beste, 'alle': urls[:6]}


# Bekannte eigene Websites, wo die Suche nur Händler bringt (geprüft wird danach das Logo selbst auf der Tafel)
HAND = {'Champagne Taittinger': 'https://www.taittinger.com/', 'Weingut Emmerich Knoll': 'https://www.knoll.at/', 'Miguel Torres': 'https://www.torres.es/',
        'Tenuta San Guido': 'https://www.tenutasanguido.com/', 'Bodegas Vega Sicilia': 'https://www.vegasicilia.com/', 'Alvaro Palacios': 'https://www.alvaropalacios.com/',
        'Angelo Gaja': 'https://www.gaja.com/', 'Champagne Nicolas Maillard': 'https://www.champagne-maillart.fr/', 'Weingut Kühling-Gillot': 'https://www.kuehlingandbattenfeld.com/'}


def suchen():
    p = Q / 'seiten.json'
    alt = json.loads(p.read_text()) if p.exists() else {}
    for k, u in HAND.items():
        alt[k] = {'url': u, 'hand': True}
    for name in weingueter():
        if name in alt and alt[name].get('url'):
            continue
        try:
            alt[name] = suche(name)
        except Exception as ex:
            alt[name] = {'url': None, 'fehler': str(ex)}
        print(name, '->', alt[name].get('url'), flush=True)
        p.write_text(json.dumps(alt, ensure_ascii=False, indent=1))
        time.sleep(1.2)


def logo_url(seite, basis):
    """Logo im Kopf der Seite: erst img/svg mit «logo» in Klasse, Id, Datei oder Alt, dann Icon für Apple-Geräte."""
    kands = []
    for m in re.finditer(r'<img\b[^>]*>', seite, re.I):
        tag = m.group(0)
        if re.search(r'logo|brand|signet|wappen', tag, re.I):
            src = re.search(r'''\s(?:data-src|src)=["']([^"']+)["']''', tag)
            if src and not src.group(1).startswith('data:'):
                kands.append((m.start(), urllib.parse.urljoin(basis, H.unescape(src.group(1)))))
    # inline-SVG in einem Element mit «logo»
    m = re.search(r'<(?:a|div|span|figure)[^>]*(?:class|id)=["\'][^"\']*logo[^"\']*["\'][^>]*>\s*(?:<[^>]+>\s*)?(<svg\b.*?</svg>)', seite, re.I | re.S)
    svg = m.group(1) if m else None
    if kands:
        return kands[0][1], svg
    if svg:
        return None, svg
    ico = re.search(r'<link[^>]*rel=["\']apple-touch-icon[^>]*href=["\']([^"\']+)', seite, re.I) or re.search(r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']apple-touch-icon', seite, re.I)
    if ico:
        return 'ICON:' + urllib.parse.urljoin(basis, H.unescape(ico.group(1))), None
    return None, None


def datei(name):
    return re.sub(r'[^a-z0-9]+', '-', ' '.join(norm(name)) or 'x').strip('-')[:60]


def hole_eins(item):
    name, info = item
    if not info.get('url'):
        return name, {'status': 'keine Website'}
    try:
        seite, end, _ = lade(info['url'], roh=True)
        seite = seite.decode('utf-8', 'ignore')
        u, svg = logo_url(seite, end)
        art = 'logo'
        if u and u.startswith('ICON:'):
            u, art = u[5:], 'icon'
        f = datei(name)
        if u:
            b, _, ct = lade(u, roh=True)
            if 'svg' in ct or u.lower().split('?')[0].endswith('.svg') or b.lstrip()[:5] in (b'<?xml', b'<svg '):
                (ZIEL / (f + '.svg')).write_bytes(b)
                return name, {'status': art, 'datei': f + '.svg', 'quelle': u, 'seite': end}
            from PIL import Image
            im = Image.open(io.BytesIO(b))
            im.load()
            im = im.convert('RGBA')
            if im.width > 600:
                im = im.resize((600, round(im.height * 600 / im.width)))
            im.save(ZIEL / (f + '.webp'), quality=92)
            return name, {'status': art, 'datei': f + '.webp', 'quelle': u, 'seite': end, 'gross': [im.width, im.height]}
        if svg:
            if 'xmlns' not in svg[:200]:
                svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
            (ZIEL / (f + '.svg')).write_text(svg)
            return name, {'status': 'svg im Kopf', 'datei': f + '.svg', 'seite': end}
        return name, {'status': 'kein Logo gefunden', 'seite': end}
    except Exception as ex:
        return name, {'status': 'Fehler', 'fehler': str(ex)[:160]}


def holen():
    S = json.loads((Q / 'seiten.json').read_text())
    with ThreadPoolExecutor(8) as ex:
        L = dict(ex.map(hole_eins, S.items()))
    (Q / 'logos.json').write_text(json.dumps(L, ensure_ascii=False, indent=1))
    from collections import Counter
    print(Counter(v['status'] for v in L.values()))


# Von Hand geprüft 19.10.2026 auf der Tafel: fremdes Zeichen (Bio-Suisse, VDP, Facebook, Hoster, Restaurant, Kampagne), anderes Haus oder Foto statt Logo
FALSCH = {'Champagne Ulysse Collin', 'Champagne Agrapart et fils', 'Champagne Bollinger', 'Champagne Nicolas Maillard', 'Hansruedi Adank', 'Weingut Wegelin - Scadenagut',
          'Weingut Jonas Kurek', 'Weingut Achim Molitor', 'Weingut Wittmann', 'Weingut Battenfeld-Spanier', 'Weingut Kühling-Gillot', 'Weingut Veyder-Malberg',
          'Weingut Hansruedi Adank', 'Weingut Thomas Studach', 'Weingut Schmidt am Bodensee', 'Tenuta Guado al Tasso', 'R. López de Heredia – Viña Tondonia',
          'Domaine Guiberteau', 'Guilbert Gillet',
          'Benjamin Leroux', 'Weingut Walter Polz'}  # Leroux: zu fein; Polz: Schrift ausgespart in voller Fläche
BLAU = (10, 37, 82)   # --titel-h, Ton in Ton mit der Seite


def farbig(im):
    from PIL import Image, ImageChops
    im = im.convert('RGBA')
    a = im.getchannel('A')
    frei = a.getextrema()[0] < 250 and sum(a.histogram()[:20]) > im.width * im.height * .08
    if not frei:
        w, h = im.size
        ecken = [im.getpixel(p)[:3] for p in ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2))]
        if all(min(c) > 225 for c in ecken):
            # Abstand zu Weiss als Deckkraft, Farbe aus dem Original zurückgerechnet
            rgb = im.convert('RGB')
            d = ImageChops.invert(rgb.convert('L'))
            mx = ImageChops.lighter(ImageChops.lighter(*[ImageChops.invert(c) for c in rgb.split()[:2]]), ImageChops.invert(rgb.split()[2]))
            alpha = mx.point(lambda x: 0 if x < 14 else min(255, int((x - 14) * 1.12)))
            im = rgb.convert('RGBA')
            im.putalpha(ImageChops.multiply(alpha, a))
        a = im.getchannel('A')
    # Helligkeit der sichtbaren Teile: weisses Logo -> keine Farbfassung
    L, S = im.convert('L'), im.convert('HSV').getchannel('S')
    px = [(l, sa) for l, sa, al in zip(L.get_flattened_data(), S.get_flattened_data(), a.get_flattened_data()) if al > 128]
    if not px:
        return None
    hell = sum(l for l, _ in px) / len(px)
    satt = sum(sa for _, sa in px) / len(px)
    if hell > 205 or (hell > 150 and satt < 60):     # weiss oder blasses Grau: auf der hellen Platte nicht lesbar
        return None
    box = a.point(lambda x: 255 if x > 10 else 0).getbbox()
    im = im.crop(box)
    if im.height > 96:
        im = im.resize((max(1, round(im.width * 96 / im.height)), 96), Image.LANCZOS)
    return im


def aufbereiten():
    """Jedes geprüfte Logo einfarbig im Blau der Seite, freigestellt, auf den Inhalt beschnitten (SVG vorher von WebKit gerastert)."""
    from PIL import Image, ImageOps
    L = json.loads((Q / 'logos.json').read_text())
    raster = Q / 'raster'
    aus = {}
    for n, v in L.items():
        if n in FALSCH or not v.get('datei'):
            continue
        f = ZIEL / v['datei']
        if f.suffix == '.svg':
            f = raster / (f.stem + '.png')
            if not f.exists():
                continue
        im = Image.open(f).convert('RGBA')
        a = im.getchannel('A')
        if a.getextrema()[0] < 250 and sum(a.histogram()[:20]) > im.width * im.height * .08:
            maske = a                                   # freigestelltes Logo: die Form ist die Deckkraft
        else:
            maske = ImageOps.invert(im.convert('L'))    # Logo auf hellem Grund: dunkel = Farbe
            maske = maske.point(lambda x: 0 if x < 28 else min(255, int((x - 28) * 1.25)))
        box = maske.getbbox()
        if not box:
            continue
        maske = maske.crop(box)
        h = 96                                          # doppelte Anzeigehöhe (44 px)
        maske = maske.resize((max(1, round(maske.width * h / maske.height)), h), Image.LANCZOS) if maske.height > h else maske
        out = Image.new('RGBA', maske.size, BLAU + (0,))
        out.putalpha(maske)
        name = 'm-' + f.stem + '.webp'
        out.save(ZIEL / name, quality=90, method=6)
        aus[n] = {'logo': 'assets/img/logo-weingut/' + name, 'b': out.width, 'h': out.height, 'quelle': v.get('quelle') or v.get('seite')}
        # Originalfarben (Robert 19.10.2026, 21:10): weisser Grund wird durchsichtig, farbige Fläche bleibt; ein weisses Logo bliebe
        # auf der hellen Platte unsichtbar, dort gilt weiter die blaue Fassung
        fa = farbig(im)
        if fa:
            fa.save(ZIEL / ('f-' + f.stem + '.webp'), quality=90, method=6)
            aus[n].update(farbe='assets/img/logo-weingut/f-' + f.stem + '.webp', fb=fa.width, fh=fa.height)
    (HIER / 'assets' / 'data' / 'weingut-logos.json').write_text(json.dumps(aus, ensure_ascii=False, indent=1))
    print(len(aus), 'Logos')


def tafel():
    """Prüftafel: jedes Logo mit Namen auf Papier und auf Kalk, zum Ansehen von Hand."""
    L = json.loads((Q / 'logos.json').read_text())
    S = json.loads((Q / 'seiten.json').read_text())
    k = ''.join(f'<div class="k"><div class="b">' + (f'<img src="../../website/assets/img/logo-weingut/{v["datei"]}">' if v.get('datei') else '<i>–</i>') +
                f'</div><b>{i:03d} {H.escape(n)}</b><small>{H.escape(v["status"])} · {H.escape(S[n].get("url") or "")}</small></div>' for i, (n, v) in enumerate(L.items()))
    (Q / 'tafel.html').write_text('<!doctype html><meta charset=utf-8><style>body{font:12px system-ui;margin:20px;display:grid;grid-template-columns:repeat(6,1fr);gap:10px;background:#fff}'
                                  '.k{border:1px solid #ddd;padding:8px}.b{height:90px;display:grid;place-items:center;background:#E7ECF3}.b img{max-height:70px;max-width:90%}small{display:block;color:#777;word-break:break-all}</style>' + k)
    print(Q / 'tafel.html')


if __name__ == '__main__':
    {'suchen': suchen, 'holen': holen, 'tafel': tafel, 'aufbereiten': aufbereiten}[sys.argv[1]]()
