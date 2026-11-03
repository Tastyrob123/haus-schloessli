# Kleine freigestellte Bilder für «Im Duft und am Gaumen» und «Passt zu» (Robert 19.10.2026: «Bilder statt farbiger Kreise»).
# Quelle: die Aroma- und Speisenbilder von Vivino (images.vivino.com/flavors/…, …/backgrounds/foods/…), freigestellt geliefert.
# Kein generiertes Bild, keine Kosten. RECHTE bei Vivino, nur zur Anschauung in der Designstudie.
import io, json, pathlib, re, time, urllib.request
from PIL import Image
import wein_infos as WI, wein_bilder as WB

HIER = pathlib.Path(__file__).resolve().parent
ZIEL = HIER / 'assets' / 'img' / 'wein' / 'klein'
UA = {'User-Agent': WI.UA, 'Accept-Language': 'de-CH,de;q=0.9'}
GRUPPE_DATEI = {'tropical_fruit': 'fallback_tropical', 'non_oak': 'fallback_nonOak'}


def lade(url, ziel, kante=260):
    if ziel.exists():
        return True
    try:
        roh = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
    except Exception:
        return False
    im = Image.open(io.BytesIO(roh)).convert('RGBA')
    bb = im.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
    if bb:
        im = im.crop(bb)
    im.thumbnail((kante, kante), Image.LANCZOS)
    im.save(ziel, 'WEBP', quality=84, method=6)
    return True


def slug(s):
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')


if __name__ == '__main__':
    ZIEL.mkdir(parents=True, exist_ok=True)
    karte = {'gruppe': {}, 'aroma': {}, 'speise': {}}
    import wein_texte as T
    for g in T.GRUPPE:
        if lade(f'https://images.vivino.com/flavors/{GRUPPE_DATEI.get(g, "fallback_" + g)}.png', ZIEL / f'g-{g}.webp'):
            karte['gruppe'][g] = f'assets/img/wein/klein/g-{g}.webp'
    # Aromawörter der Karte (die drei ersten je Gruppe); nur wo Vivino ein Bild hat
    worte = set()
    for f in WI.SEITEN.glob('*.json'):
        for a in json.loads(f.read_text()).get('aromen') or []:
            worte.update(a['worte'][:3])
    for w in sorted(worte):
        if lade(f'https://images.vivino.com/flavors/{slug(w)}.png', ZIEL / f'a-{slug(w)}.webp'):
            karte['aroma'][T.AROMA.get(w, w)] = f'assets/img/wein/klein/a-{slug(w)}.webp'
        time.sleep(.05)
    # Speisen: Bild aus einer Weinseite, die die Speise nennt (die Weinseite trägt die Bildadresse)
    offen = {}
    for f in sorted(WI.SEITEN.glob('*.json')):
        for s in json.loads(f.read_text()).get('speisen') or []:
            offen.setdefault(s, int(f.stem))
    for name, vid in offen.items():
        if (ZIEL / f's-{slug(name)}.webp').exists():
            karte['speise'][name] = f'assets/img/wein/klein/s-{slug(name)}.webp'
            continue
        roh = urllib.request.urlopen(urllib.request.Request(f'https://www.vivino.com/w/{vid}', headers=UA), timeout=40).read().decode('utf-8', 'replace')
        m = re.search(r'"name":"' + re.escape(name) + r'","weight":[0-9.]+,"background_image":\{"location":"([^"]+)"', roh)
        # die Kachel (…/thumbs/…_932x810.png) ist freigestellt, das breite Bild nur ein Ausschnitt (Robert 19.10.: «abgeschnitten oben und unten»)
        if m and lade('https:' + m.group(1).replace('/backgrounds/foods/', '/backgrounds/foods/thumbs/').replace('.png', '_932x810.png'), ZIEL / f's-{slug(name)}.webp', 300):
            karte['speise'][name] = f'assets/img/wein/klein/s-{slug(name)}.webp'
        time.sleep(1)
    (HIER / 'assets' / 'data' / 'wein-bildchen.json').write_text(json.dumps(karte, ensure_ascii=False, separators=(',', ':')))
    print('Gruppen', len(karte['gruppe']), 'Aromen', len(karte['aroma']), 'von', len(worte), 'Speisen', len(karte['speise']), 'von', len(offen))
