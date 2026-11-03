#!/usr/bin/env python3
"""Wirtschaft am Schlössli: fünfzehn Postkarten vom Hafen, von der Terrasse und vom See (Werkbank Papier, Nachtbau 3./4.11.2026;
Bauart wie postkarten.py des Culinarium und des Walk on the Wild Side). Titel = der Ort («Bottighofen», «Bodensee», «Am Hafen», «Lästermeile»).
Fotos nur aus website/assets/img mit den Rechten aus website/inhalt/bilder.json: eigene Fotos des Hauses, dazu freie Fotos von Wikimedia Commons
mit Nennung von Urheber und Lizenz auf der Rückseite. Keine Gäste-, Fremd- oder KI-Bilder.
Vorn A6 im Format des Fotos (quer 148 × 105, hoch 105 × 148), das Foto randlos, unten der Ort in Open Sans; hinten A6 quer auf Papier:
links Ort, Bildzeile und Nachweis, rechts Platz zum Schreiben, Adresslinien und ein Markenfeld mit den Zeigern.
Druck-PDF mit 3 mm Beschnitt, Sammelbogen SRA3, Fächer und Kartenständer als Bild (postkarten_druck.js).
   PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/postkarten.py "<website/_werkbank>"            → satz/postkarten*.html, postkarten_plan.json
   node _werkbank/postkarten_druck.js "<…>"   dann   PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/postkarten.py "<…>" --seite"""
import json, os, shutil, sys
from PIL import Image
import papier_haus as PH
H = PH.ein()
import papier_kern as P  # noqa: E402
from papier_kern import blatt, e, t  # noqa: E402
import kern as K  # noqa: E402
from kern import kn, titel, kap, zahl  # noqa: E402
from papier_haus import (NACHT, STUHL, PAPIER, BLATT, WEISS, HIMMEL, HIMMELH, HIMMELT, TINTE, LEISE, NAME, ADR, IG, WEBSITE, ss)  # noqa: E402

W, ROOT = PH.W, PH.ROOT
B = 3   # Beschnitt
OS, IN, MO = "'Open Sans',Arial,sans-serif", "'Instrument Sans',Arial,sans-serif", "'DM Mono',Menlo,monospace"
# Foto, Ort (Titel), Bildzeile, Lage
KARTEN = [('start', 'Bottighofen', 'Die blauen Stühle auf der Terrasse am Mittag, dahinter der See und die Alpen.', '50% 55%'),
          ('bootshafen', 'Bottighofen', 'Der Bootshafen, dahinter die Wirtschaft und das Schlössli.', '50% 55%'),
          ('platanen', 'Am Hafen', 'Gedeckte Tische unter den Platanen, dahinter der Hafen.', '50% 50%'),
          ('morgen', 'Bodensee', 'Morgen am See, hinten die Alpen und die Schifflände.', '50% 55%'),
          ('abend', 'Bottighofen', 'Abend unter der Platane, die Lichterkette über dem See.', '50% 60%'),
          ('haus', 'Am Hafen', 'Das ehemalige Hafenmeistergebäude mit der Wirtschaft.', '50% 55%'),
          ('saentis', 'Bodensee', 'Der Blick über den See bis zum Säntis.', '50% 50%'),
          ('apero', 'Bodensee', 'Ein Spritz und ein Bier in der blauen Stunde.', '50% 55%'),
          ('schifflaende', 'Bottighofen', 'Die Schifflände am Hafen.', '50% 55%'),
          ('gaststube', 'Am Hafen', 'Die Gaststube mit den grossen Fenstern zum Hafen.', '50% 50%'),
          ('abendschiff', 'Bodensee', 'Ein Kursschiff im Abendlicht, dahinter das Säntis-Massiv.', '50% 50%'),
          ('regal', 'Lästermeile', 'An der Bar: durch die Scheibe der See.', '50% 50%'),
          ('glas', 'Bodensee', 'Ein Glas Weisswein vor dem See.', '50% 45%'),
          ('luft1954', 'Bottighofen, 1954', 'Das Strandhotel Schlössli am See aus der Luft.', '50% 50%'),
          ('bar', 'Lästermeile', 'An der Bar wird gezapft, unter der Theke die Zementfliesen.', '50% 50%')]


def karten():
    K_ = []
    for key, ort, satz, lage in KARTEN:
        v = PH.BILDER[key]
        K_.append(dict(id=f'pk{len(K_) + 1:02d}', key=key, name=ort, satz=satz, lage=lage, hoch=v['h'] > v['w'], nachweis=PH.nachweis(key)))
    return K_


def et(text, gr, farbe, sp=.18):
    return f'<span style="font:400 {gr}mm/1.4 {MO};letter-spacing:{sp}em;text-transform:uppercase;color:{farbe}">{e(ss(text))}</span>'


def zw(b, farbe):
    return f'<svg viewBox="{PH.ZEICHEN[0]}" style="display:block;width:{b}mm;height:{b * PH.ZV:.2f}mm;color:{farbe}" fill="currentColor"><use href="#hz"/></svg>'


def vorn(k, rand=0):
    """A6 im Format des Fotos; rand = Beschnitt ringsum (Druck)."""
    b, h = (105, 148) if k['hoch'] else (148, 105)
    bb, hh = b + 2 * rand, h + 2 * rand
    band = 30 if k['hoch'] else 26
    inn = (f'<img class="abs" src="{e(PH.bild_satz(k["key"]))}" style="inset:0;width:{bb}mm;height:{hh}mm;object-fit:cover;object-position:{k["lage"]}" alt="">'
           f'<i class="abs" style="left:0;top:{hh - rand - band - 14}mm;width:{bb}mm;height:{band + 14 + rand}mm;background:linear-gradient(rgba(11,29,61,0),rgba(11,29,61,.78))"></i>'
           f'<div class="abs" style="left:{rand + 9}mm;bottom:{rand + 9}mm;width:{b - 18}mm;display:flex;align-items:flex-end;justify-content:space-between;gap:4mm">'
           f'<div><div style="font:400 {6.2 if len(k["name"]) < 14 else 5}mm/1.1 {OS};letter-spacing:.16em;text-transform:uppercase;color:{BLATT}">{e(k["name"])}</div>'
           f'<div style="height:1.8mm"></div>{et(NAME, 1.8, HIMMELH, .16)}</div>{zw(5.4, HIMMELH)}</div>')
    return blatt(bb, hh, inn, '', f'background:{NACHT}')


def hinten(k, rand=0):
    """A6 quer, 148 × 105: links Ort, Bildzeile und Nachweis, rechts Adresslinien und Markenfeld mit den Zeigern."""
    b, h = 148 + 2 * rand, 105 + 2 * rand
    r = rand
    links = (f'<div class="abs" style="left:{r + 10}mm;top:{r + 12}mm;width:54mm;bottom:{r + 12}mm;display:flex;flex-direction:column;justify-content:space-between">'
             f'<div>{et("Grüsse vom Hafen", 1.8, HIMMELT, .16)}<div style="height:3mm"></div>'
             f'<div style="font:400 5.6mm/1.15 {OS};letter-spacing:.12em;text-transform:uppercase;color:{STUHL}">{e(k["name"])}</div><div style="height:2.6mm"></div>'
             f'<i style="display:block;width:8mm;height:.35mm;background:{HIMMEL}"></i><div style="height:2.6mm"></div>'
             f'<div style="font:400 3mm/1.45 {IN};color:{TINTE}">{e(ss(k["satz"]))}</div>'
             + (f'<div style="height:2mm"></div><div style="font:400 2.2mm/1.4 {IN};color:{LEISE}">{e(k["nachweis"])}</div>' if k['nachweis'] else '')
             + f'</div><div>{et(NAME, 1.5, HIMMELT, .1)}<div style="height:.8mm"></div>{et(ADR, 1.5, HIMMELT, .06)}<div style="height:.8mm"></div>{et(IG, 1.5, HIMMELT, .06)}</div></div>')
    trenn = f'<i class="abs" style="left:{r + 72}mm;top:{r + 12}mm;width:.25mm;height:81mm;background:{HIMMEL}"></i>'
    marke = (f'<div class="abs" style="left:{r + 148 - 10 - 20}mm;top:{r + 10}mm;width:20mm;height:24mm;border:.3mm dashed rgba(4,16,35,.4);border-radius:.8mm;'
             f'display:flex;align-items:center;justify-content:center">{zw(7, STUHL)}</div>')
    linien = ''.join(f'<i class="abs" style="left:{r + 80}mm;top:{r + 50 + n * 11}mm;width:58mm;height:.25mm;background:rgba(4,16,35,.34)"></i>' for n in range(4))
    return blatt(b, h, f'<i class="abs" style="inset:0;background:{BLATT}"></i>' + links + trenn + marke + linien, '', f'background:{BLATT}')


def setzen():
    KK = karten()
    os.makedirs(os.path.join(P.SATZ, 'bild'), exist_ok=True)
    Image.open(PH.bild('abend', 1800)).convert('RGB').save(os.path.join(P.SATZ, 'bild', 'hafen-abend.webp'), 'WEBP', quality=80)   # Hintergrund für den Kartenständer
    vor = [vorn(k) for k in KK]; hin = [hinten(k) for k in KK]
    P.seite('postkarten', [x for p in zip(vor, hin) for x in p], 'Postkarten')
    P.seite('postkarten-druck', [x for k in KK for x in (vorn(k, B), hinten(k, B))], 'Postkarten, Druck mit Beschnitt')
    BW, BH, LUFT = 450, 320, 3
    boegen = []
    # Sammelbogen SRA3: die Karten in ihrem Format, Reihe für Reihe, so viele Bögen wie nötig
    teile, akt, x, y, zh = [], [], 12, 14, 0
    for k in KK:
        b, h = (105, 148) if k['hoch'] else (148, 105)
        if x + b > BW - 12:
            x, y, zh = 12, y + zh + LUFT, 0
        if y + h > BH - 8:
            teile.append(akt); akt, x, y, zh = [], 12, 14, 0
        akt.append((k, x, y, b, h)); x += b + LUFT; zh = max(zh, h)
    teile.append(akt)
    for nr, akt in enumerate(teile):
        inn = ''
        for k, x, y, b, h in akt:
            inn += f'<div class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{h}mm;overflow:hidden">{vorn(k).replace("style=\"width:", "style=\"margin:0;width:", 1)}</div>'
            inn += f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{h}mm;outline:.15mm solid #e6007e"></i>'
        inn += t(14, 4, f'{e(NAME)} · Postkarten · Sammelbogen {nr + 1} von {len(teile)} · SRA3 quer · Originalgrösse · Schnittlinie in Magenta', 'm', f'font-size:2.1mm;color:{TINTE}')
        boegen.append(blatt(BW, BH, inn, '', 'background:#fff'))
    P.seite('postkarten-bogen', boegen, 'Postkarten, Sammelbogen')
    json.dump({'karten': [{k2: k[k2] for k2 in ('id', 'key', 'name', 'satz', 'hoch', 'nachweis')} for k in KK], 'boegen': len(boegen)},
              open(os.path.join(W, 'postkarten_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Postkarten gesetzt:', len(KK), 'Karten,', len(boegen), 'Sammelbögen')


def seite():
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'postkarten_plan.json')))
    KK = plan['karten']
    roh, ziel = os.path.join(W, 'roh', 'postkarten'), os.path.join(ROOT, 'postkarten', 'img')
    if os.path.isdir(ziel):
        shutil.rmtree(ziel)
    os.makedirs(ziel)
    M = {}
    for f in os.listdir(roh):
        if not f.endswith('.png'):
            continue
        im = Image.open(os.path.join(roh, f)).convert('RGBA')
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(os.path.join(ziel, f[:-4] + '.webp'), 'WEBP', quality=86, method=5); M[f[:-4]] = im.size
    img = lambda n, alt='': f'<img src="img/{n}.webp" width="{M[n][0]}" height="{M[n][1]}" alt="{e(alt)}" decoding="async">'
    unter = lambda k: 'Foto: Wikimedia Commons' if k['nachweis'] else 'Foto des Hauses'
    liste = ''.join(f'<li data-a="kipp" style="--i:{n % 4}"><span class="b pk-paar{" pk-hoch" if k["hoch"] else ""}">{img(k["id"] + "-v", k["name"])}{img(k["id"] + "-h", "Rückseite")}</span>'
                    f'<h3>{e(k["name"])}</h3><p>{e(ss(k["satz"]))}</p><small>A6 · {"vorn hoch" if k["hoch"] else "vorn quer"}, hinten quer · {unter(k)}</small></li>' for n, k in enumerate(KK))
    nf = sum(1 for k in KK if k['nachweis'])
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([zahl(len(KK)), 'Postkarten', 'vom Hafen.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Grüsse von der Terrasse, vom Hafen und vom See: {zahl(len(KK) - nf).lower()} Karten mit Ihren eigenen Fotos, {zahl(nf).lower()} mit freien Fotos von Wikimedia Commons, deren Urheber auf der Rückseite steht. Vorn der Ort, hinten Platz zum Schreiben und die Zeiger im Markenfeld. Zum Auslegen an der Bar und zum Mitnehmen.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn('Druck-PDF', f'pdf/{PH.KURZ}-postkarten-druck.pdf', 'kn--linie', neu=True)}</div>
    </div>
    <div class="auslage" aria-hidden="true"><div data-a="schweb" style="left:0;top:0;width:100%;--r:0deg;--r0:0deg;--i:2">{img("faecher", "")}</div></div>
  </div>
</section>
<section class="fl fl--nacht tapete-leicht blatt stueck" id="staender">
  <div class="in">
    <div class="stueck__t">{kap(1, 'An der Bar')}{titel(['Im Ständer', 'an der Lästermeile.'])}<div class="lauf"><p data-a="worte">So könnten die Karten an der Bar stehen: zum Mitnehmen nach dem letzten Glas, mit dem Hafen im Rücken.</p></div></div>
    <div class="karton"><figure class="sch" data-a="schweb" style="width:96%">{img("staender", "Kartenständer an der Bar")}</figure></div>
  </div>
</section>
<section class="fl fl--papier blatt" id="karten">
  <div class="in">
    <div class="kopfzeile"><div>{kap(2, 'Die Karten')}{titel([zahl(len(KK)), 'Postkarten.'])}</div><div class="lauf"><p data-a="worte">Jedes Foto randlos, vorn der Ort in der Schrift der Wortmarke. Hinten die Bildzeile und bei freien Fotos der Nachweis.</p></div></div>
    <ul class="etk">{liste}</ul>
  </div>
</section>
<section class="fl fl--creme blatt stueck" id="druck">
  <div class="in">
    <div class="stueck__t">{kap(3, 'Für die Druckerei')}{titel(['Der', 'Sammelbogen.'])}
      <div class="lauf"><p data-a="worte">Alle Karten mit 3 mm Beschnitt als ein PDF, dazu {zahl(plan["boegen"]).lower()} Sammelbögen SRA3 mit Schnittlinien.</p></div>
      <div class="kn-reihe" data-a="auf">{kn('Druck-PDF', f'pdf/{PH.KURZ}-postkarten-druck.pdf', neu=True)}{kn('Sammelbogen SRA3', f'pdf/{PH.KURZ}-postkarten-sammelbogen-a3.pdf', 'kn--linie', neu=True)}</div></div>
    <div class="bogenblick" data-a="gross">{img("bogen", "Sammelbogen SRA3")}</div>
  </div>
</section>
<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Drucksachen, Sticker und Beigaben im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Sticker', '../sticker/index.html', 'kn--linie')}{kn('Beigaben', '../beigaben/index.html', 'kn--linie')}</div></div></section>'''
    css = ('<style>.etk .b.pk-paar{display:flex!important;flex-direction:row!important;gap:4%;align-items:center;justify-content:center;height:auto!important;aspect-ratio:auto!important}'
           '.etk .b.pk-paar img{position:static!important;width:48%!important;height:auto!important;max-height:none!important}'
           '.etk .b.pk-paar.pk-hoch img{width:36%!important}.etk .b.pk-paar.pk-hoch img+img{width:56%!important}</style>')
    K.schreib(os.path.join(ROOT, 'postkarten', 'index.html'), K.rahmen('Postkarten', f'{zahl(len(KK))} Postkarten der {NAME}.', 'Postkarten', css + haupt))
    Image.open(os.path.join(ziel, 'faecher.webp')).save(os.path.join(ziel, 'vorschau.webp'), 'WEBP', quality=86)
    print('Seite gebaut: postkarten/ ·', len(KK), 'Karten')


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else setzen()
