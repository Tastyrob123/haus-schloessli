#!/usr/bin/env python3
"""Wirtschaft am Schlössli: fünf Beigaben als Druckvorlage (Werkbank Papier, Nachtbau 3./4.11.2026; Bauart wie beigaben.py des Culinarium).
Kleine Dinge, die ein Gast am Platz findet oder mitnimmt: das Serviettenband für die Feier, das Tischset der Lästermeile, die Fähnchen für die Tapas,
der Flaschenanhänger aus dem Keller und das Streichholzbriefchen für die Windlichter auf der Terrasse. Satz mit den Bausteinen aus papier.py
(eine Achse, Gruppe auf der optischen Mitte), Inhalte nur aus website/inhalt/*.json. Seite beigaben/ im Kleid der Drucksachen.
   PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/beigaben.py "<website/_werkbank>"          →  satz/beigabe-*.html, beigaben_plan.json
   node _werkbank/sticker_druck.js "<…>" beigaben, dann  PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/beigaben.py "<…>" --seite"""
import json, os, sys
import papier_haus as PH
H = PH.ein()
import papier_kern as P  # noqa: E402
import kern as K  # noqa: E402
from kern import kn, titel, kap, zahl  # noqa: E402
from papier_kern import e  # noqa: E402
import papier as PA  # noqa: E402
from papier import seite, zw, wm, et, ti, tx, nabe, ab, feld, TOENE  # noqa: E402
from papier_haus import (NACHT, STUHL, BLATT, HIMMEL, HIMMELH, HIMMELT, TINTE, LEISE, HJ, LM, NAME, BY, ganz)  # noqa: E402

W, ROOT = PH.W, PH.ROOT


def beigaben():
    B = []

    def d(ident, name, format_, blaetter, karton, titel_, satz):
        namen = [n for n, _, _ in karton]
        B.append(dict(id=ident, name=name, format=format_, blaetter=blaetter, vorschau=[(n, i + 1) for i, n in enumerate(namen)], satz=satz, karton=karton, titel=titel_))

    # 1 Serviettenband für die Feier: die Serviette gerollt, das Band mit den Zeigern hält sie
    d('serviettenband', 'Serviettenband für die Feier', 'Band 210 × 40 mm, um die gerollte Serviette',
      [seite(210, 40, 'nacht', f'<div style="display:flex;align-items:center;gap:7mm">{zw(7, HIMMEL)}{wm(78, BLATT)}</div>' + ab(2.4) + et(HJ['bankett']['titel'], 1.8, HIMMEL, .22), rahmen=False),
       seite(210, 40, 'blatt', f'<div style="display:flex;align-items:center;gap:7mm">{zw(7, STUHL)}{ti("Schön, dass Sie da sind.", 5, STUHL, .1)}</div>', rahmen=False)],
      [('band', 90, 'Aussen'), ('band-r', 90, 'Innen')], ['Ein Band', 'um die Serviette.'],
      'Bei Banketts liegt auf jedem Teller die Serviette gerollt, ein Band mit den Zeigern und der Wortmarke hält sie zusammen. Innen ein Satz zur Begrüssung.')
    # 2 Tischset der Lästermeile (A3 quer): die Tapas ohne Preise und die Geschichte vom Besen
    tap = ''.join(ti(ganz(x['name']), 6.6, STUHL, .1, 1.2) + ab(2) + tx(ganz(x['text']), 4.4, LEISE, 150) + ab(7) if x['text'] else ti(ganz(x['name']), 6.6, STUHL, .1, 1.2) + ab(7)
                  for x in LM['gruppen'][0]['eintraege'])
    links = (f'<div style="width:160mm;display:flex;flex-direction:column;align-items:center">{et("Lästermeile", 3, HIMMELT, .24)}{ab(3.4)}{ti(LM["gruppen"][0]["titel"], 11, STUHL, .14)}{ab(6)}{nabe(34, HIMMEL)}{ab(11)}{tap}</div>')
    rechts = (f'<div style="width:160mm;display:flex;flex-direction:column;align-items:center">{zw(15, STUHL)}{ab(6)}{et("Seit dem 17. Jahrhundert", 3, HIMMELT, .2)}{ab(3.4)}'
              f'{ti("Ein Besen statt eines Schilds", 8.6, STUHL, .12)}{ab(6)}{nabe(34, HIMMEL)}{ab(9)}' + ''.join(tx(ganz(s), 4.6, TINTE, 156) + ab(4.6) for s in HJ['besen']) + '</div>')
    mitte = f'<div style="display:flex;gap:22mm;align-items:center;justify-content:center"><div>{links}</div><i style="display:block;width:.3mm;height:200mm;background:{HIMMEL}"></i><div>{rechts}</div></div>'
    d('tischset', 'Tischset der Lästermeile', 'A3 quer, 420 × 297 mm', [seite(420, 297, 'blatt', mitte, kopf=f'{NAME} · {BY}', fuss=f'{PH.ADR} · {PH.TEL} · {PH.IG}')],
      [('tischset', 92, '')], ['Ein Tischset', 'für die Bar.'],
      'Auf den Tischen der Lästermeile liegt ein Blatt aus Papier: links die Tapas, die es den ganzen Tag gibt, rechts die Geschichte vom Besen, der Ende des 17. Jahrhunderts statt eines Schilds heraushing.')
    # 3 Tapas-Fähnchen: am Spiess in der Schale, je Gericht eines
    fa = ''.join(f'<div style="width:46mm;height:26mm;display:flex;flex-direction:column;align-items:center;justify-content:center;border:.25mm solid {HIMMEL};border-radius:1.2mm;margin:0 2mm">'
                 f'{zw(4, STUHL)}{ab(1.6)}{ti(ganz(x["name"]), 2.9 if len(x["name"]) < 14 else 2.4, STUHL, .08, 1.2)}</div>' for x in LM['gruppen'][0]['eintraege'])
    d('faehnchen', 'Fähnchen für die Tapas', 'Fähnchen 46 × 26 mm, gefalzt am Spiess', [seite(210, 40, 'blatt', f'<div style="display:flex;justify-content:center">{fa}</div>', rahmen=False)],
      [('faehnchen', 90, '')], ['Ein Fähnchen', 'in jeder Schale.'],
      'Am Spiess in der Schale: welche der Tapas auf dem Tisch steht. Vier Fähnchen für die vier Tapas der Lästermeile, Namen wie auf der Karte.')
    # 4 Flaschenanhänger aus dem Keller
    t2 = TOENE['blatt']
    loch = f'<i class="abs" style="left:24mm;top:9mm;width:7mm;height:7mm;border-radius:50%;background:#8f8672"></i>'
    vorn = seite(55, 120, 'nacht', ab(10) + zw(8, HIMMEL) + ab(4) + et('Aus dem Keller', 1.7, HIMMEL, .2) + ab(2.4) + ti('Jonas Volpert', 4.2, BLATT, .1) + ab(1.6) + et('empfiehlt', 1.7, HIMMEL, .2) + ab(4) + nabe(14, HIMMEL),
                 fuss=NAME, extra=loch.replace('#8f8672', '#fbfcfe'))
    hinten = seite(55, 120, 'blatt', ab(10) + feld('Der Wein', 38, t2['et'], 'rgba(4,16,35,.4)', 1.6) + ab(4) + feld('Jahrgang', 38, t2['et'], 'rgba(4,16,35,.4)', 1.6) + ab(4)
                   + feld('Dazu passt', 38, t2['et'], 'rgba(4,16,35,.4)', 1.6), fuss='Bündner Herrschaft · Burgund · Champagne', extra=loch.replace('#8f8672', '#0b1d3d'))
    d('flaschenanhaenger', 'Flaschenanhänger aus dem Keller', '55 × 120 mm, zwei Seiten, gelocht', [vorn, hinten],
      [('anhaenger', 30, 'Vorderseite'), ('anhaenger-r', 30, 'Rückseite')], ['Ein Anhänger', 'für die Flasche.'],
      'Für die Flasche, die ein Gast mit nach Hause nimmt: vorne die Empfehlung von Jonas Volpert, hinten Wein, Jahrgang und was dazu passt, von Hand eingetragen.')
    # 5 Streichholzbriefchen für die Windlichter auf der Terrasse
    d('streichholz', 'Streichholzbriefchen', 'Briefchen 50 × 110 mm (gefalzt 50 × 40)',
      [seite(50, 110, 'nacht', zw(12, HIMMEL) + ab(5) + et('Wirtschaft am Schlössli', 1.5, HIMMELH, .14) + ab(14) + et('Für das Windlicht am Tisch', 1.5, HIMMEL, .12), fuss=PH.HJ['strasse'], rahmen=False)],
      [('streichholz', 30, '')], ['Streichhölzer', 'für die Windlichter.'],
      'Für die Windlichter auf der Terrasse, zum Mitnehmen nach dem Abend unter der Platane. Aussen die Zeiger auf der Nacht über dem See.')
    return B


def setzen():
    B = beigaben()
    for d in B:
        P.seite('beigabe-' + d['id'], d['blaetter'], d['name'])
    json.dump({'druck': [{k: d[k] for k in ('id', 'name', 'format', 'vorschau', 'satz', 'karton', 'titel')} | {'seiten': len(d['blaetter'])} for d in B]},
              open(os.path.join(W, 'beigaben_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Beigaben gesetzt:', len(B))


def seite_():
    from PIL import Image
    import shutil
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'beigaben_plan.json')))
    roh, ziel = os.path.join(W, 'roh', 'beigaben'), os.path.join(ROOT, 'beigaben', 'img')
    if os.path.isdir(ziel):
        shutil.rmtree(ziel)
    os.makedirs(ziel, exist_ok=True)
    M = {}
    for d in plan['druck']:
        for name, _ in d['vorschau']:
            im = Image.open(os.path.join(roh, name + '.png')).convert('RGBA')
            if im.width > 1000:
                im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
            im.save(os.path.join(ziel, name + '.webp'), 'WEBP', quality=88, method=5); M[name] = im.size
    FL = ['fl--papier', 'fl--nacht tapete-leicht', 'fl--creme', 'fl--papier', 'fl--creme']
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([zahl(len(plan['druck'])) + ' Beigaben', 'für den Tisch.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Kleine Dinge, die ein Gast am Platz findet oder mitnimmt. Alle im Stil der neuen Seite, jede als Druckvorlage. Was nicht passt, lassen Sie einfach weg.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn('Drucksachen', '../drucksachen/index.html', 'kn--linie')}</div>
    </div>
  </div>
</section>
'''
    for i, d in enumerate(plan['druck']):
        figs = ''.join(f'<figure class="sch" data-a="schweb" style="width:{w}%;--i:{k % 4}"><img src="img/{nm}.webp" width="{M[nm][0]}" height="{M[nm][1]}" alt="{e(d["name"])}" decoding="async">'
                       f'{f"<figcaption>{e(u)}</figcaption>" if u else ""}</figure>' for k, (nm, w, u) in enumerate(d['karton']))
        haupt += f'''<section class="fl {FL[i % len(FL)]} blatt stueck{" stueck--r" if i % 2 else ""}" id="{d['id']}">
  <div class="in">
    <div class="stueck__t">
      {kap(i + 1, e(d['name']))}
      {titel(d['titel'])}
      <div class="lauf"><p data-a="worte">{e(d['satz'])}</p></div>
      <p class="stueck__f" data-a="auf">{e(d['format'])}</p>
      <div class="kn-reihe" data-a="auf">{kn('Als PDF ansehen', f"pdf/{PH.KURZ}-{d['id']}.pdf", neu=True)}</div>
    </div>
    <div class="karton">{figs}</div>
  </div>
</section>
'''
    haupt += f'''<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Drucksachen, Untersetzer, Sticker und Postkarten im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Sticker', '../sticker/index.html', 'kn--linie')}{kn('Postkarten', '../postkarten/index.html', 'kn--linie')}</div></div></section>'''
    K.schreib(os.path.join(ROOT, 'beigaben', 'index.html'), K.rahmen('Beigaben', f'{zahl(len(plan["druck"]))} Beigaben für die Tische der {NAME}.', 'Beigaben', haupt))
    print('Seite gebaut: beigaben/ ·', len(plan['druck']), 'Beigaben')


if __name__ == '__main__':
    seite_() if '--seite' in sys.argv else setzen()
