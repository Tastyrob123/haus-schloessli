#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli, Unterlagen (Werkbank Papier, Nachtbau 3./4.11.2026; Bauart wie sb_karten.py des Culinarium und unterlagen.py des Kits).
Die fünf Karten des Hauses als Idee neben der heutigen Fassung: Speisekarte nach Ländern, Lunch, Lästermeile, Weinkarte, Bankettmenüs.
«Idee» = der Satz des Hauses in _karten/pdf/ (Open Sans, Instrument Sans, DM Mono, feste Schnitte, kein Type 3, Preise wie im Original),
«Heute» = die Original-PDFs des Hauses (einmal aus _quelle/website/pdf/ nach _werkbank/unterlagen_heute/ kopiert und eingecheckt: zur Laufzeit lädt
nichts aus _quelle/). Je Seite der Idee die Seite des Originals mit den meisten gleichen Wörtern (altmap, pdftotext).
Dazu zwei Unterlagen ohne heutige Fassung: der Brief an Christian Kuchler und das Angebot (Betreuung CHF 200 im Monat, Robert 20.10.2026; der Bau ohne Betrag).
   PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/unterlagen_bau.py "<website/_werkbank>"            → unterlagen/pdf, satz/unterlagen-*.html, unterlagen.json
   node _werkbank/unterlagen_druck.js "<website/_werkbank>"                                            → unterlagen/pdf/<kurz>-brief.pdf, -angebot.pdf
   PYTHONPATH=<Kit>:<_werkbank> python3 _werkbank/unterlagen_bau.py "<website/_werkbank>" --seite     → unterlagen/index.html, unterlagen/img"""
import datetime, glob, json, os, re, shutil, subprocess, sys
import papier_haus as PH
H = PH.ein()
import kern as K  # noqa: E402
import papier_kern as P  # noqa: E402
from papier_kern import blatt, e  # noqa: E402
from papier_haus import (NACHT, STUHL, BLATT, WEISS, HIMMEL, HIMMELH, HIMMELT, TINTE, LEISE, HJ, NAME, ADR, TEL, MAIL, WEBSITE, KURZ, ss)  # noqa: E402

ROOT, W = PH.ROOT, PH.W
KARTEN = os.path.join(PH.PROJ, '_karten', 'pdf')
QUELLE = os.path.join(PH.PROJ, '_quelle', 'website', 'pdf')
HEUTE = os.path.join(W, 'unterlagen_heute')
ZIEL = os.path.join(ROOT, 'unterlagen'); IMG = os.path.join(ZIEL, 'img'); PDF = os.path.join(ZIEL, 'pdf')
ROH = os.path.join(W, 'roh', 'unterlagen')
# Ziel, Name, Gruppe, Idee (_karten/pdf), Heute (Original des Hauses)
LISTE = [('speisekarte', 'Die Karte nach Ländern', 'Restaurant', 'speisekarte.pdf', 'Speisekarte-Oktober.pdf'),
         ('lunch', 'Lunch', 'Restaurant', 'lunch.pdf', 'Lunch_261019.pdf'),
         ('laestermeile', 'Lästermeile', 'Bar', 'laestermeile.pdf', 'Lastermeile-Homepage-2339.pdf'),
         ('weinkarte', 'Weinkarte', 'Restaurant', 'weinkarte.pdf', '20261014_Weinkarte.pdf'),
         ('bankett', 'Bankettmenüs', 'Banketts & Gruppen', 'bankett.pdf', 'Bankettmenuvorschlage.pdf')]
OS, IN, MO = "'Open Sans',Arial,sans-serif", "'Instrument Sans',Arial,sans-serif", "'DM Mono',Menlo,monospace"
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
HEUTE_D = datetime.date.today()
DATUM = f'{HEUTE_D.day}. {MONATE[HEUTE_D.month - 1]} {HEUTE_D.year}'
BETREUUNG = 200   # CHF im Monat, Robert 20.10.2026


def woerter(pdf):
    """Wörter je Seite (pdftotext), klein geschrieben, ab vier Buchstaben"""
    t = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    return [set(w for w in re.findall(r'[a-zäöüéèàçñ]{4,}', s.lower())) for s in t.split('\f')]


def altmap(neu, alt):
    a, n = woerter(alt), woerter(neu)
    n = n[:int(subprocess.run(['pdfinfo', neu], capture_output=True, text=True).stdout.split('Pages:')[1].split()[0])]
    m, letzte = [], 1
    for s in n:
        if len(s) < 6:   # Umschlag oder fast leere Seite: dieselbe wie die vorige (Umschlag zeigt das erste Blatt)
            m.append(letzte); continue
        best = max(range(len(a)), key=lambda i: len(s & a[i]))
        letzte = best + 1; m.append(letzte)
    return m


# ---------------------------------------------------------------- Brief und Angebot (Satz in mm wie die Drucksachen)
def _abs():
    """Brief: die Absätze des Briefs der Werkbank (haus.BRIEF), solange der fehlt, die Fassung vom 19.10.2026."""
    b = getattr(H, 'BRIEF', None)
    if b and b.get('absaetze') and not getattr(H, '_ersatz', False):
        return [re.sub(r'<[^>]+>', '', x) for x in b['absaetze']], getattr(H, 'ANREDE', 'Grüezi Herr Kuchler')
    return ['Blaue Stühle auf Kies, Platanen darüber und der See bis zu den Alpen: Wer bei Ihnen draussen sitzt, bleibt gern länger als geplant. Dieses Gefühl soll man auf der neuen Seite haben, noch bevor man einen Tisch reserviert.',
            'Ich bin Robert Reff, komme selbst aus der Gastronomie und baue heute Websites für Restaurants und Hotels. Beim Schlössli hat mich zuerst die Küche neugierig gemacht: Monika Huber kocht seit April 2025 am See, und GaultMillau nennt sie die Entdeckung des Jahres 2026.',
            'Auf Ihrer heutigen Seite findet man davon wenig. Die neue erzählt es: die Karte nach Ländern, die Lästermeile, den Keller von Jonas Volpert und den Besen, der Ende des 17. Jahrhunderts statt eines Wirtshausschilds am Haus am See hing. Reserviert wird weiter über Ihr Gastronovi.',
            'Dazu gehören Ihre Karten, neu gesetzt mit Ihren Preisen, Werkzeuge, mit denen Ihr Team Karte, Anlässe und Anfragen selbst pflegt, und ein paar Dinge für die Tische. Jedes Werkzeug lässt sich in der Werkbank gleich öffnen und ausprobieren.'], 'Grüezi Herr Kuchler'


def _p(text, gr=3.6, farbe=TINTE, zl=1.55, mehr=''):
    return f'<p style="margin:0 0 {gr * 1.05}mm;font:400 {gr}mm/{zl} {IN};color:{farbe};{mehr}">{text}</p>'


def _et(text, gr=1.9, farbe=HIMMELT, sp=.16):
    return f'<div style="font:400 {gr}mm/1.45 {MO};letter-spacing:{sp}em;text-transform:uppercase;color:{farbe}">{e(ss(text))}</div>'


def _ti(text, gr, farbe=STUHL, sp=.14):
    return f'<div style="font:400 {gr}mm/1.2 {OS};letter-spacing:{sp}em;text-transform:uppercase;color:{farbe}">{e(ss(text))}</div>'


def kopf_brief(b=210):
    return (f'<div class="abs" style="left:25mm;top:18mm;width:160mm;display:flex;justify-content:space-between;align-items:flex-end">'
            f'<div>{_ti("Tasty Studios", 4.4, STUHL, .22)}<div style="height:1.4mm"></div>{_et("Robert Reff · robert@tasty-studios.de", 1.8, LEISE, .1)}</div>'
            f'<div style="text-align:right">{_et(f"Für {NAME}", 1.8, HIMMELT, .12)}</div></div>'
            f'<i class="abs" style="left:25mm;top:32mm;width:160mm;height:.25mm;background:{HIMMEL}"></i>')


def fuss_brief(nr, von):
    return (f'<i class="abs" style="left:25mm;top:276mm;width:160mm;height:.25mm;background:{HIMMEL}"></i>'
            f'<div class="abs" style="left:25mm;top:279mm;width:160mm;display:flex;justify-content:space-between">{_et("Tasty Studios · Robert Reff · robert@tasty-studios.de", 1.7, LEISE, .08)}'
            f'{_et(f"Seite {nr} von {von}", 1.7, LEISE, .08)}</div>')


def brief():
    abs_, anrede = _abs()
    os.makedirs(os.path.join(P.SATZ, 'bild'), exist_ok=True)   # der Vorschau-Server liefert aus _werkbank/ nur satz/ und fonts/
    shutil.copy2(os.path.join(W, 'eigen', 'unterschrift-robert.webp'), os.path.join(P.SATZ, 'bild', 'unterschrift-robert.webp'))
    unterschrift = 'bild/unterschrift-robert.webp'
    an = ''.join(f'<div style="font:400 3.4mm/1.45 {IN};color:{TINTE}">{e(z)}</div>' for z in (NAME, 'Herr Christian Kuchler', HJ['strasse'], HJ['ort']))
    text = ''.join(_p(e(ss(a))) for a in abs_)
    inn = (f'<i class="abs" style="inset:0;background:{WEISS}"></i>' + kopf_brief()
           + f'<div class="abs" style="left:25mm;top:48mm;width:90mm">{an}</div>'
           + f'<div class="abs" style="left:125mm;top:48mm;width:60mm;text-align:right;font:400 3.2mm/1.45 {IN};color:{LEISE}">{e(DATUM)}</div>'
           + f'<div class="abs" style="left:25mm;top:88mm;width:160mm">{_ti("Ihre neue Website, als Entwurf", 4.6, STUHL, .12)}<div style="height:8mm"></div>'
           + _p(e(ss(anrede.rstrip(',') + ','))) + text
           + _p('Herzliche Grüsse', mehr='margin-top:6mm')
           + f'<img src="{e(unterschrift)}" style="display:block;height:16mm;width:auto;margin:1mm 0 1mm -2mm" alt="">'
           + _p('Robert Reff, Tasty Studios', 3.3, LEISE) + '</div>'
           + fuss_brief(1, 1))
    return [blatt(210, 297, inn, '', f'background:{WEISS}')]


def werkzeugnamen():
    s = open(os.path.join(PH.KLEID, 'schloessli.js'), encoding='utf-8').read()
    return re.findall(r"\w+: '([^']+)'", re.search(r'namen:\s*\{([^}]*)\}', s).group(1))


def zahlen():
    lies = lambda n, l: json.load(open(os.path.join(W, n), encoding='utf-8')) if os.path.exists(os.path.join(W, n)) else l
    p = lies('papier_plan.json', {'druck': []}); m = lies('papier_mehr.json', {'druck': []})
    return dict(karten=len(LISTE), druck=len(p['druck']) + len(m['druck']), unter=len(p.get('etiketten', [])),
                sticker=len(lies('sticker_plan.json', {'etiketten': []})['etiketten']), post=len(lies('postkarten_plan.json', {'karten': []})['karten']),
                gaben=len(lies('beigaben_plan.json', {'druck': []})['druck']))


def liste(punkte, gr=3.2):
    return ''.join(f'<div style="display:flex;gap:2.4mm;margin:0 0 1.6mm;font:400 {gr}mm/1.45 {IN};color:{TINTE}"><i style="flex:none;width:1.6mm;height:1.6mm;margin-top:{gr * .45}mm;border-radius:50%;border:.3mm solid {HIMMELT}"></i><span>{e(ss(x))}</span></div>' for x in punkte)


def angebot():
    Z = zahlen(); wz = werkzeugnamen()
    zw = lambda n: {40: 'Vierzig', 30: 'Dreissig'}.get(n) or K.zahl(n)
    zus = [f'Für die Wirtschaft am Schlössli habe ich einen ganzen Auftritt gebaut: die Website, sieben Werkzeuge, mit denen Ihr Team sie selbst pflegt, '
           f'{zw(Z["karten"]).lower()} Karten neu gesetzt, {zw(Z["druck"]).lower()} Drucksachen, {zw(Z["unter"]).lower()} Untersetzer für die Lästermeile, '
           f'{zw(Z["sticker"]).lower()} Sticker, {zw(Z["post"]).lower()} Postkarten und {zw(Z["gaben"]).lower()} Beigaben. Alles davon können Sie in der Werkbank anklicken.',
           'Gebaut ist es. Was fehlt, liegt bei Ihnen: die Zugänge zu Domain und Mail, der Entscheid zu den Fotos und das Gegenlesen von Karten und Preisen.',
           f'Den Betrag für den Bau nennen Sie. Danach kümmere ich mich um Website, Werkzeuge und KI, für CHF {BETREUUNG} im Monat, monatlich kündbar.']
    steht = ['Die Website mit allen Seiten und dem Rechtlichen', 'Die Karte nach Ländern, Lunch, Lästermeile, Weinkarte und Bankett, je als PDF',
             'Reservation über gastronovi und der Gutschein auf jeder Seite', f'{zw(Z["druck"])} Drucksachen, {zw(Z["unter"]).lower()} Untersetzer, {zw(Z["sticker"]).lower()} Sticker',
             f'{zw(Z["post"])} Postkarten und {zw(Z["gaben"]).lower()} Beigaben']
    braucht = ['Zugänge zu Domain und Mail', 'Der Entscheid zu den Fotos', 'Gegenlesen von Karten und Preisen', 'Freigabe der Rechtstexte']
    eigentum = ['Website, Code, Karten, Drucksachen und Beiträge gehören Ihrem Haus.', 'Domain, Server und alle Zugänge laufen auf Ihren Namen.',
                'Die Fotos bleiben bei Ihnen und Ihren Fotografen.', 'Sollten wir einmal getrennte Wege gehen, nehmen Sie alles mit.']
    betreuung = ['Server, Domain, Sicherungen, Aktualisierungen, Sicherheit und Datenschutz.', 'Die sieben Werkzeuge laufen, Fehler behebe ich ohne Rechnung, ein Ausfall hat Vorrang.',
                 'Die KI kennt Ihre neuen Karten, Zeiten und Preise: ich halte ihr Wissen aktuell.', 'Antwort spätestens am nächsten Werktag. Ihr Team pflegt die Inhalte selbst.']
    wochen = [('Zugänge und Gespräch', 'Gespräch mit Ihnen und Monika Huber, dazu die Liste der Zugänge.'), ('Lesen und berichtigen', 'Küche und Service lesen Karten, Preise und Seiten gegen; jede Korrektur am selben Tag.'),
              ('Anbindungen und Fotos', 'Mailversand, Chat und jedes Werkzeug mit Passwort; freigegebene Fotos einarbeiten.'), ('Runde im Haus', 'Gemeinsam durch jede Seite und jedes Werkzeug.'),
              ('Schulung', 'Eine Stunde je Werkzeug; Rechtstexte, Weiterleitungen, Google.'), ('Umzug', f'Die Seite geht unter {WEBSITE} online; zwei Wochen täglich hinsehen.')]

    def block(titel, innen, b=160):
        return f'<div style="width:{b}mm;margin:0 0 7mm">{_et(titel, 2, HIMMELT, .18)}<i style="display:block;height:.25mm;background:{HIMMEL};margin:1.6mm 0 3mm"></i>{innen}</div>'

    s1 = (f'<i class="abs" style="inset:0;background:{WEISS}"></i>' + kopf_brief()
          + f'<div class="abs" style="left:25mm;top:44mm;width:160mm">{_ti("Ein Vorschlag.", 9, STUHL, .12)}<div style="height:2.4mm"></div>{_et(f"Für {NAME} · {DATUM}", 2, LEISE, .12)}<div style="height:9mm"></div>'
          + block('Zusammenfassung', ''.join(_p(e(ss(x)), 3.4) for x in zus))
          + f'<div style="display:flex;gap:10mm">{block("Steht, zum Anklicken", liste(steht, 3), 75)}{block("Läuft im Entwurf, zieht mit um", liste(wz, 3), 75)}</div>'
          + block('Braucht etwas von Ihnen', f'<div style="display:grid;grid-template-columns:1fr 1fr;column-gap:10mm">{liste(braucht, 3)}</div>')
          + block('Wo die KI arbeitet', _p('Vier Stellen nutzen ein Sprachmodell: der Chat für Ihre Gäste, die Antwort auf eine Anfrage, Entwürfe in der Hausdruckerei und die Markenprüfung im Markenbuch. Es läuft über ein eigenes Konto Ihres Hauses beim Anbieter: Sie zahlen dort direkt nach Verbrauch, ich richte das Konto ein und setze eine Obergrenze je Monat. Jede Stelle läuft auch ohne KI weiter.', 3.1))
          + '</div>' + fuss_brief(1, 2))
    zeile = lambda a, b_, c: (f'<div style="display:grid;grid-template-columns:40mm 50mm 1fr;gap:4mm;padding:3.4mm 0;border-bottom:.25mm solid {HIMMELH};align-items:baseline">'
                              f'<div style="font:400 3.6mm/1.3 {OS};letter-spacing:.1em;text-transform:uppercase;color:{STUHL}">{e(a)}</div>'
                              f'<div style="font:400 3.3mm/1.3 {MO};letter-spacing:.04em;color:{TINTE}">{e(b_)}</div><div>{c}</div></div>')
    preis = (zeile('Der Bau', 'Den Betrag nennen Sie', _p('Sie nennen den Betrag, bei dem Sie sich wohlfühlen.', 3.1, mehr='margin:0'))
             + zeile('Betreuung', f'CHF {BETREUUNG} im Monat', liste(betreuung, 3.1))
             + zeile('Wünsche darüber hinaus', 'Angebot vorher', _p('Ein weiterer Bereich oder eine neue Funktion: dafür mache ich Ihnen gern vorher ein Angebot.', 3.1, mehr='margin:0')))
    woche = ''.join(f'<div style="display:grid;grid-template-columns:16mm 1fr;gap:3mm;margin:0 0 2.2mm;align-items:baseline"><div style="font:400 2.2mm/1.4 {MO};letter-spacing:.12em;color:{HIMMELT}">WOCHE {i + 1}</div>'
                    f'<div style="font:400 3.1mm/1.45 {IN};color:{TINTE}"><b style="font-weight:600">{e(t)}.</b> {e(ss(s))}</div></div>' for i, (t, s) in enumerate(wochen))
    s2 = (f'<i class="abs" style="inset:0;background:{WEISS}"></i>' + kopf_brief()
          + f'<div class="abs" style="left:25mm;top:44mm;width:160mm">'
          + block('Der Preis', preis + _p('Monatlich kündbar, Beträge netto.', 2.9, LEISE, mehr='margin-top:3mm'))
          + block('Eigentum', liste(eigentum, 3.1))
          + block('So geht es weiter', woche)
          + '</div>' + fuss_brief(2, 2))
    return [blatt(210, 297, s1, '', f'background:{WEISS}'), blatt(210, 297, s2, '', f'background:{WEISS}')]


def bau():
    for d in (PDF, HEUTE):
        os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(PDF, '*.pdf')):
        if not os.path.basename(f).startswith(KURZ + '-'):
            os.remove(f)   # Karten des Culinarium
    plan = []
    for ziel, name, gruppe, idee, heute in LISTE:
        q = os.path.join(KARTEN, idee)
        if not os.path.exists(q):
            print('fehlt', q); continue
        shutil.copy2(q, os.path.join(PDF, f'{KURZ}-{ziel}.pdf'))
        h = os.path.join(HEUTE, ziel + '.pdf')
        if os.path.exists(os.path.join(QUELLE, heute)):
            shutil.copy2(os.path.join(QUELLE, heute), h)
        plan.append(dict(ziel=f'{KURZ}-{ziel}', quelle=os.path.relpath(h, ROOT), name=name, gruppe=gruppe, seiten=0, b=210, h=297, dazu='', fehlt='',
                         alt_seiten=altmap(os.path.join(PDF, f'{KURZ}-{ziel}.pdf'), h)))
    P.seite('unterlagen-brief', brief(), 'Brief')
    P.seite('unterlagen-angebot', angebot(), 'Angebot')
    plan.append(dict(ziel=f'{KURZ}-brief', quelle='', name='Brief', gruppe='Tasty Studios', seiten=1, b=210, h=297, dazu='', fehlt=''))
    plan.append(dict(ziel=f'{KURZ}-angebot', quelle='', name='Angebot', gruppe='Tasty Studios', seiten=2, b=210, h=297, dazu='', fehlt=''))
    json.dump(plan, open(os.path.join(W, 'unterlagen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Unterlagen:', ', '.join(p['ziel'] for p in plan))


# ---------------------------------------------------------------- die Seite (wie Kit unterlagen.py, dazu Unterlagen ohne heutige Fassung)
def seiten(pdf, kennung):
    os.makedirs(ROH, exist_ok=True); os.makedirs(IMG, exist_ok=True)
    marke = os.path.join(ROH, kennung + '.json')
    if os.path.exists(marke) and os.path.getmtime(marke) > os.path.getmtime(pdf) and all(os.path.exists(os.path.join(IMG, x[0])) for x in json.load(open(marke))):
        return json.load(open(marke))
    for alt in glob.glob(os.path.join(ROH, kennung + '-*.png')):
        os.remove(alt)
    subprocess.run(['pdftoppm', '-r', '170', '-png', pdf, os.path.join(ROH, kennung)], check=True)
    from PIL import Image
    aus = []
    for i, f in enumerate(sorted(glob.glob(os.path.join(ROH, kennung + '-*.png')))):
        im = Image.open(f).convert('RGB')
        if im.width > 1500:
            im = im.resize((1500, round(im.height * 1500 / im.width)), Image.LANCZOS)
        name = f'{kennung}-{i + 1:02d}.webp'
        im.save(os.path.join(IMG, name), 'WEBP', quality=84, method=5)
        aus.append([name, im.width, im.height]); os.remove(f)
    json.dump(aus, open(marke, 'w'))
    return aus


JS_OHNE = r'''/* Unterlagen ohne heutige Fassung (Brief, Angebot): nur die Idee, mittig (Werkbank Papier 3.11.2026) */
(function () {
  var U = window.UNTERLAGEN, s = document.querySelector('.uschau'); if (!U || !s) return;
  var wahl = [].slice.call(document.querySelectorAll('.uwahl button'));
  function pruef() { var i = wahl.findIndex(function (w) { return w.getAttribute('aria-pressed') === 'true'; }); var x = U[i < 0 ? 0 : i]; s.classList.toggle('ohne-alt', !!x && !x.alt.length); }
  new MutationObserver(pruef).observe(document.querySelector('.uwahl'), { attributes: true, subtree: true, attributeFilter: ['aria-pressed'] }); pruef();
})();
'''
CSS_OHNE = ('<style>.uschau.ohne-alt .ublatt--alt{display:none}.uschau.ohne-alt .upaar{grid-template-columns:minmax(0,560px);justify-content:center}'
            '.uschau.ohne-alt .uschalter{visibility:hidden}.uschau.ohne-alt .ublatt--neu{display:block!important}</style>')


def seite():
    K.gestaltung()
    from kern import kn, titel, kap, zahl, PF, LI, RE
    plan = json.load(open(os.path.join(W, 'unterlagen.json')))
    for f in glob.glob(os.path.join(IMG, '*.webp')):
        if not os.path.basename(f)[2:].startswith(KURZ + '-'):
            os.remove(f)   # Bilder des Culinarium
    D = []
    for d in plan:
        neu = seiten(os.path.join(PDF, d['ziel'] + '.pdf'), 'n-' + d['ziel'])
        alt = seiten(os.path.join(ROOT, d['quelle']), 'h-' + d['ziel']) if d['quelle'] else []
        x = {'id': d['ziel'], 'name': d['name'], 'gruppe': d['gruppe'], 'neu': neu, 'alt': alt}
        if d.get('alt_seiten'):
            x['altmap'] = d['alt_seiten']
        D.append(x)
    n = sum(1 for d in D if d['alt'])
    U = H.UNTERLAGEN
    wahl = ''.join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-id="{d["id"]}">{e(d["name"])}</button>' for i, d in enumerate(D))
    orte = [(0, 10, 36, -8), (21, 4, 36, -3), (42, 0, 36, 3), (63, 7, 36, 8)]
    faecher = ''.join(f'<div class="blattbild" data-a="schweb" style="left:{x}%;top:{y}%;width:{b}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}"><img src="img/n-{KURZ}-{k}-{"02" if k in ("speisekarte", "laestermeile", "bankett") else "01"}.webp" alt=""></div>'
                      for i, ((k, _), (x, y, b, r)) in enumerate(zip(H.FAECHER[:4], orte)))
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('unterlagen'), 'Unterlagen')}
      {titel(['Ihre Karten,', 'neu gesetzt.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">{e(U['seite_text'])}</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Durchblättern', '#blaettern')}{kn('Zur Werkbank', '../werkbank/index.html#unterlagen', 'kn--linie')}</div>
    </div>
    <div class="auslage auslage--pdf" aria-hidden="true">{faecher}</div>
  </div>
</section>
<section class="fl fl--papier blatt" id="blaettern">
  <div class="in">
    <div class="kopfzeile"><div>{kap(1, 'Durchblättern')}{titel(['Heute und', 'als Idee.'])}</div><div class="lauf"><p data-a="worte">Wählen Sie eine Unterlage und blättern Sie mit den Pfeilen. Links steht Ihre heutige Fassung, rechts die Idee im Stil der neuen Seite. Brief und Angebot gibt es nur neu.</p></div></div>
    <div class="uwahl" data-a="auf" role="group" aria-label="Unterlage wählen">{wahl}</div>
    <div class="uschau" data-a="auf" tabindex="0">
      <div class="uschalter" role="group" aria-label="Fassung"><button type="button" aria-pressed="false" data-s="alt">Heute</button><button type="button" aria-pressed="true" data-s="neu">Idee</button></div>
      <div class="upaar">
        <figure class="ublatt ublatt--alt"><div class="ublatt__b"></div><figcaption>Heute</figcaption></figure>
        <figure class="ublatt ublatt--neu"><div class="ublatt__b"></div><figcaption>Idee</figcaption></figure>
        <button class="rund schau__p schau__p--l" type="button" data-zur aria-label="Vorige Seite">{LI}</button>
        <button class="rund schau__p schau__p--r" type="button" data-vor aria-label="Nächste Seite">{RE}</button>
      </div>
      <div class="ufuss">
        <div><h3></h3><p class="mono"></p></div>
        <div class="kn-reihe"><a class="kn kn--klein" href="#" target="_blank" rel="noopener" data-pdf>Als PDF<i>{PF}</i></a></div>
      </div>
    </div>
  </div>
</section>
<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Ideen für Papier: Drucksachen, Untersetzer, Sticker, Postkarten und Beigaben.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Untersetzer', '../untersetzer/index.html', 'kn--linie')}{kn('Zur Werkbank', '../werkbank/index.html#unterlagen', 'kn--linie')}</div></div></section>
{CSS_OHNE}
<script>window.UNTERLAGEN={json.dumps(D, ensure_ascii=False)};</script>
<script src="unterlagen.js?v={int(os.path.getmtime(os.path.join(K.KIT, 'unterlagen.js')))}" defer></script>
<script src="unterlagen-ohne.js" defer></script>'''
    s = K.rahmen('Unterlagen', f'{zahl(n)} Karten der {NAME} als Idee im Stil der neuen Website, jede neben der heutigen Fassung, dazu Brief und Angebot.', 'Unterlagen', haupt,
                 f'Die neuen Fassungen sind Ideen von Robert Reff, Tasty Studios, und keine offiziellen Unterlagen des Hauses. Fotos, Zeichen und Texte gehören {H.RECHTE}')
    K.schreib(os.path.join(ZIEL, 'index.html'), s)
    js = open(os.path.join(K.KIT, 'unterlagen.js'), encoding='utf-8').read()
    # ohne heutige Fassung: kein Bild links, die Idee allein
    js = js.replace("setz(alt, x.alt[ai], r); setz(neu, x.neu[si], r);", "if (x.alt.length) setz(alt, x.alt[ai], r); setz(neu, x.neu[si], r);")
    js = js.replace("var na = x.alt[", "var na = x.alt.length && x.alt[")
    K.schreib(os.path.join(ZIEL, 'unterlagen.js'), js)
    open(os.path.join(ZIEL, 'unterlagen-ohne.js'), 'w', encoding='utf-8').write(JS_OHNE)
    print('Unterlagen:', len(D), 'mit', sum(len(d['neu']) for d in D), 'Seiten')


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else bau()
