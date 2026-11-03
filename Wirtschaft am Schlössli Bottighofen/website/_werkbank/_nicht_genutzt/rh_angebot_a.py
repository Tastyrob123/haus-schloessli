#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus, Kapitel 8 «Was zum Ruedihus gehört», Teil «Was dazugehört» in Fassung A (Robert 18.10.2026 «vorschlag a»,
Vorbild Doldenhorn dh_angebot_a.py, hier auf dem hellen Blatt des Ruedihus): ein System für die vier Häuser, Zahlen, die Sprachen, die sieben
Werkzeuge als Gegenstände im Wechsel (Stube am Laptop, Schreibtisch am Handy, Karten der Tafel gedruckt, Gastgeber am Handy, Markenbuch
aufgeschlagen, Besucherbuch am Handy, Drucksachen der Werkstatt als Stapel), gleiche Höhe, leicht geneigt; darunter die Checkliste mit Symbolen.
Das Gerüst (03) und die Daten (04) als Symbole statt Textlisten.
  Quellen: ansichten/Angebot/maison.jpg und markenbuch.pdf (node _werkbank/angebot_schirm.js, Server 8917), ansichten/Werkzeuge-Handy/*.jpg,
  unterlagen/img, drucksachen/img. Schreibt werkbank/img/ag-wz-<werkzeug>.webp, nur wenn eine Quelle neuer ist."""
import os, subprocess, sys, tempfile
from PIL import Image, ImageFilter

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
sys.path.insert(0, W)
import objekte_bau as OB  # noqa: E402
import schatten  # noqa: E402  (Kit, über objekte_bau im Pfad)

IMG = os.path.join(ROOT, 'werkbank', 'img')
AN = os.path.join(W, 'ansichten')
HOEHE = 560
WZ = [('maison', 'Die Stube', 'am Laptop'), ('bureau', 'Der Schreibtisch', 'am Handy'), ('carte', 'Die Tafel', 'gedruckte Karten'),
      ('reception', 'Der Gastgeber', 'am Handy'), ('livre', 'Das Hausbuch', 'das Markenbuch'), ('registre', 'Das Besucherbuch', 'am Handy'),
      ('imprimerie', 'Die Werkstatt', 'Drucksachen')]


def _sch(im, st=.55):
    return schatten.backe(im, rand=.08, tiefe=.025, weich=.03, staerke=st, farbe=OB.DUNKEL)


def _handy(n, grad):
    im = OB.offen(os.path.join(AN, 'Werkzeuge-Handy', n + '.jpg')); o = round(im.height * .056)
    neu = Image.new('RGBA', im.size, im.getpixel((4, 4))); neu.paste(im.crop((0, 0, im.width, im.height - o)), (0, o))
    pf = os.path.join(AN, 'Werkzeuge-Handy', '_' + n + '.png'); neu.save(pf)
    h = OB.handy(pf).rotate(grad, expand=True, resample=Image.BICUBIC)
    return h   # das Gehäuse bringt seinen Schatten mit


def _blatt(p, breite, grad):
    im = OB.blatt(p); im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    return _sch(im.rotate(grad, expand=True, resample=Image.BICUBIC), .5)


def _stapel(teile, groesse):
    c = Image.new('RGBA', groesse, (0, 0, 0, 0))
    for im, x, y in teile:
        c.alpha_composite(im, (x, y))
    return c


def _buch(pdf, seiten=(2, 4)):
    """Aufgeschlagenes Markenbuch: zwei echte Seiten aus dem Hausbuch (Das Haus, Das Medaillon), Falz in der Mitte."""
    with tempfile.TemporaryDirectory() as d:
        ims = []
        for n, s in enumerate(seiten):
            subprocess.run(['pdftoppm', '-r', '90', '-png', '-f', str(s), '-l', str(s), pdf, os.path.join(d, f'p{n}')], check=True)
            f = sorted(x for x in os.listdir(d) if x.startswith(f'p{n}'))[0]
            ims.append(Image.open(os.path.join(d, f)).convert('RGB'))
    a, b = ims; h = 620
    a = a.resize((round(a.width * h / a.height), h), Image.LANCZOS); b = b.resize((round(b.width * h / b.height), h), Image.LANCZOS)
    buch = Image.new('RGBA', (a.width + b.width, h), (0, 0, 0, 0)); buch.paste(a, (0, 0)); buch.paste(b, (a.width, 0))
    falz = Image.new('L', (140, h), 0)
    for x in range(140):
        falz.paste(round(80 * (1 - abs(x - 70) / 70) ** 2.2), (x, 0, x + 1, h))
    dunkel = Image.new('RGBA', (140, h), (30, 18, 8, 255)); dunkel.putalpha(falz)
    buch.alpha_composite(dunkel, (a.width - 70, 0))
    return _sch(buch.rotate(-2, expand=True, resample=Image.BICUBIC))


def gegenstaende():
    A, U, D = os.path.join(AN, 'Angebot'), os.path.join(ROOT, 'unterlagen', 'img'), os.path.join(ROOT, 'drucksachen', 'img')
    H = lambda n: os.path.join(AN, 'Werkzeuge-Handy', n + '.jpg')
    quellen = {'maison': [os.path.join(A, 'maison.jpg')], 'bureau': [H('bureau')],
               'carte': [os.path.join(U, 'n-chaes-und-wystube-01.webp'), os.path.join(U, 'n-tagesteller-01.webp')],
               'reception': [H('reception')], 'livre': [os.path.join(A, 'markenbuch.pdf')], 'registre': [H('registre')],
               'imprimerie': [os.path.join(D, n + '.webp') for n in ('geschichte', 'ansichtskarte-1', 'gutschein', 'tischkarte')]}
    aus = {}
    os.makedirs(IMG, exist_ok=True)
    for key, *_ in WZ:
        ziel = os.path.join(IMG, f'ag-wz-{key}.webp'); aus[key] = 'img/' + os.path.basename(ziel)
        q = quellen[key]
        if not all(os.path.exists(p) for p in q):
            print('Angebot A: Quelle fehlt für', key, [p for p in q if not os.path.exists(p)])
            continue
        if os.path.exists(ziel) and os.path.getmtime(ziel) >= max(os.path.getmtime(p) for p in q + [__file__]):
            continue
        if key == 'maison':
            im = _sch(OB.laptop(q[0]))
        elif key in ('bureau', 'reception', 'registre'):
            im = _handy(key, {'bureau': -5, 'reception': 5, 'registre': -5}[key])
        elif key == 'carte':
            a = _blatt(q[0], 520, -6); b = _blatt(q[1], 480, 5)
            im = _stapel([(a, 0, 0), (b, 300, 70)], (300 + b.width, max(a.height, 70 + b.height)))
        elif key == 'livre':
            im = _buch(q[0])
        else:
            s1 = _blatt(q[0], 420, -6); s2 = _blatt(q[1], 460, 4); s3 = _blatt(q[2], 440, -3); s4 = _blatt(q[3], 300, 8)
            im = _stapel([(s1, 0, 0), (s2, 260, 120), (s3, 60, 360), (s4, 470, 430)], (900, 900))
        bb = im.getbbox()
        if bb:
            im = im.crop(bb)
        im = im.resize((round(im.width * HOEHE / im.height), HOEHE), Image.LANCZOS)
        im.save(ziel + '.neu.webp', 'WEBP', quality=86, method=6); os.replace(ziel + '.neu.webp', ziel)
    return aus


SYM = open(os.path.join(W, 'eigen', 'angebot-a-symbole.svg'), encoding='utf-8').read()
SYSTEM = ('Ein System für vier Häuser', 'Landgasthof Ruedihus, Waldhotel Doldenhorn, Berghotel Gasterntal und Carlton-Europe: vier Websites, '
          'eine gemeinsame Startseite der Familie und dieselben sieben Werkzeuge für alle vier Häuser. Die Zahlen hier zeigen, was im Ruedihus steht.')
BRAUCHT = [('schluessel', 'Domain, SimpleBooking und Mail: die Zugänge'), ('foto', 'Ein Wort zu den Fotos'), ('recht', 'Impressum und Datenschutz: Ihre Angaben'),
           ('tel', 'Die Telefonnummer fürs Papier'), ('lesen', 'Jemand, der Seiten und Karten gegenliest'), ('preis', 'Für Preise auf der Seite: SimpleBooking freischalten')]
IDEE = 'Gedacht, noch nicht gebaut: einen Tisch mit freier Uhrzeit reservieren · die Tagesteller der Woche gleich auf der Startseite.'
GERUEST = [('blitz', 'Jede Seite liegt fertig da und lädt ohne Umweg'), ('tuer', 'Sieben Werkzeuge, sieben eigene Zugänge'), ('bett', 'Gebucht wird weiter in Ihrem SimpleBooking'),
           ('chat', 'Der Chat antwortet nur aus Ihren Seiten und Karten'), ('eins', 'Einmal eingetragen, stimmt es überall'), ('zurueck', 'Ein älterer Stand ist mit einem Klick wieder da')]
DATEN = [('keks', 'Kein Cookie, niemand verfolgt Gäste'), ('karte', 'Der Chat fragt nie nach Karte oder Pass'), ('falle', 'Eine Falle hält Maschinen draussen'),
         ('zaehlen', 'Das Besucherbuch kennt keine Namen'), ('schloss', 'Ab dem Einzug ein Passwort je Person'), ('suche', 'Bis dahin sieht keine Suchmaschine die Seite')]
PF = '<i><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg></i>'


def ico(n, kl='ico'):
    return f'<svg class="{kl}" aria-hidden="true"><use href="#i-{n}"/></svg>'


def symbole(e, pp):
    return '<div class="aga-symbole">' + ''.join(f'<div class="aga-sym" data-a="auf" style="--i:{i % 3}">{ico(n)}<span>{e(t)}</span></div>' for i, (n, t) in enumerate(pp)) + '</div>'


def teil(e, z, livre_fotos, h, sprachen_html):
    bilder = gegenstaende()
    zahlen = [(z['seiten'], 'Seiten', 'Jede der vier Zimmerarten mit eigener Seite'), (7, 'Werkzeuge', 'Damit Ihr Team die Seite selbst führt'),
              (z['unterlagen'], 'Unterlagen', 'Vom Schpiszettel bis zum Heft mit den Menuvorschlägen'), (z['druck'], 'Drucksachen', f'Dazu {z["etiketten"]} Zündholz-Etiketten'),
              (z['mails'], 'Mails', 'An Ihre Gäste'), (z['feed'], 'Beiträge', 'Für Instagram'), (livre_fotos, 'Fotos', 'Des Hauses, im Hausbuch')]
    zz = ''.join(f'<div class="aga-zahl" data-a="auf" style="--i:{i % 4}"><b>{n}</b><p class="aga-kl">{e(t)}</p><span>{e(s)}</span></div>' for i, (n, t, s) in enumerate(zahlen))
    zz += f'<div class="aga-zahl" data-a="auf" style="--i:3"><b>{ico("chat", "ico aga-gross")}</b><p class="aga-kl">Rezeption im Chat</p><span>Dazu Zimmer-Finder, Gutschein, Fest-Rechner und Anfrage-Fenster</span></div>'

    def mass(key):
        try:
            with Image.open(os.path.join(ROOT, 'werkbank', bilder[key])) as im:
                return im.size
        except OSError:
            return (16, 10)
    wz = ''.join(f'<figure class="aga-wz" style="--a:{mass(k)[0] / mass(k)[1]:.3f}"><span class="aga-wz__b"><img src="{bilder[k]}" width="{mass(k)[0]}" height="{mass(k)[1]}" alt="{e(n)}, {e(w)}" loading="lazy" decoding="async"></span>'
                 f'<figcaption>{e(n)}</figcaption></figure>' + ('<i class="aga-bruch" aria-hidden="true"></i>' if i == 3 else '') for i, (k, n, w) in enumerate(WZ))
    liste = ''.join(f'<li data-a="auf" style="--i:{i % 3}">{ico(n)}<span>{e(t)}</span></li>' for i, (n, t) in enumerate(BRAUCHT))   # Robert 18.10.2026: als Kacheln nebeneinander
    return f'''
    {SYM}
    <div class="ag-teil" id="ag-umfang">
      <div class="ag-blatt ag-umf aga" data-a="mkhoch">
        {h(e, '02', 'Was dazugehört')}
        <div class="aga-system"><p class="aga-kl">{e(SYSTEM[0])}</p><p>{e(SYSTEM[1])}</p></div>
        <div class="aga-zahlen">{zz}</div>
        {sprachen_html}
        <div class="aga-block"><p class="aga-kl">Im Entwurf in Betrieb, zieht mit ein</p><div class="aga-reihe">{wz}</div></div>
        <div class="aga-braucht"><h4>Kommt aus Ihrem Haus</h4><ul class="aga-kacheln">{liste}</ul><p class="aga-idee">{e(IDEE)}</p></div>
      </div>
    </div>
    <div class="ag-teil">
      <div class="ag-blatt ag-zwei aga" data-a="mkhoch">
        <div id="ag-aufbau">{h(e, '03', 'Das Gerüst')}{symbole(e, GERUEST)}</div>
        <div id="ag-daten">{h(e, '04', 'Was mit Daten geschieht')}{symbole(e, DATEN)}<p class="aga-mehr"><a class="kn kn--klein" href="ki.html">Mehr zu KI und Ihren Daten{PF}</a></p></div>
      </div>
    </div>'''


CSS = '''
/* ---------- Angebot, Fassung A (Robert 18.10.2026 «vorschlag a», Vorbild Doldenhorn, auf dem hellen Blatt des Ruedihus) ---------- */
.aga-kl{margin:0;font:11.5px/1.4 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:#967d40}
.aga-system{max-width:70ch;margin:0 0 clamp(26px,3vw,40px)}
.aga-system p:last-child{margin:10px 0 0;font-size:1.04rem;line-height:1.6;color:rgba(42,26,14,.82)}
.aga-zahlen{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid rgba(150,125,64,.3)}
.aga-zahl{display:grid;gap:10px;align-content:start;padding:clamp(20px,2.2vw,32px) clamp(14px,1.6vw,24px);border-bottom:1px solid rgba(150,125,64,.3)}
.aga-zahl:not(:nth-child(4n+1)){border-left:1px solid rgba(150,125,64,.3)}
.aga-zahl b{font-family:var(--serif);font-weight:700;font-size:clamp(2.6rem,4.4vw,4rem);line-height:.9;color:var(--tinte)}
.aga-zahl span{font-size:.98rem;line-height:1.45;color:rgba(42,26,14,.72)}
.aga .ico{width:26px;height:26px;fill:none;stroke:currentColor;stroke-width:1.4;stroke-linecap:round;stroke-linejoin:round;flex:none;color:#967d40}
.aga .ico.aga-gross{width:54px;height:54px;color:var(--tinte)}
.aga .sp-zeile{margin-top:clamp(26px,3vw,40px)}
.aga-block{margin-top:clamp(50px,5.4vw,84px)}
.aga-reihe{display:flex;flex-wrap:wrap;justify-content:center;gap:clamp(30px,3vw,48px) clamp(28px,3.4vw,56px);align-items:flex-end;margin-top:30px}
.aga-wz{margin:0;display:grid;gap:16px;justify-items:center;text-align:center}
.aga-wz__b{display:block}
.aga-wz__b img{display:block;width:auto;height:clamp(170px,16vw,236px)}
.aga-bruch{flex-basis:100%;height:0}
/* Robert 18.10.2026 23:35: «diese acht Sachen bitte nebeneinander … nicht zwei Zeilen»: am Laptop alle Geräte in einer Reihe, jedes so breit wie sein Bild bei gleicher Höhe */
@media(min-width:701px){.aga-reihe{flex-wrap:nowrap;gap:clamp(14px,1.8vw,30px)}.aga-bruch{display:none}.aga-wz{flex:var(--a) 1 0;min-width:0;grid-template-columns:minmax(0,1fr);justify-items:stretch}
  .aga-wz__b{width:100%;min-width:0}.aga-wz__b img{width:100%;height:auto}.aga-wz figcaption{white-space:normal!important;text-wrap:balance;font-size:clamp(.82rem,.95vw,1.02rem)!important;line-height:1.25}}
.aga-wz figcaption{font-family:var(--serif);font-weight:700;font-size:1.02rem;color:var(--tinte);white-space:nowrap}
.aga-braucht{margin-top:clamp(50px,5.4vw,84px)}
.aga-kacheln{list-style:none;padding:0;margin:22px 0 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(12px,1.4vw,20px)}
.aga-kacheln li{display:flex;flex-direction:column;gap:14px;min-height:clamp(132px,10vw,156px);padding:clamp(18px,1.8vw,26px);border-radius:20px;background:linear-gradient(180deg,rgba(255,255,255,.72),rgba(255,251,242,.4));box-shadow:inset 0 0 0 1px rgba(150,125,64,.32),inset 0 1px 0 #fff;font-family:var(--serif);font-size:clamp(1.06rem,1.2vw,1.22rem);line-height:1.35;color:rgba(42,26,14,.92)}
.aga-kacheln .ico{width:30px;height:30px}
@media(max-width:900px){.aga-kacheln{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.aga-kacheln{grid-template-columns:1fr}.aga-kacheln li{min-height:0;flex-direction:row;align-items:center}}
.aga h4{margin:0;font-family:var(--serif);font-weight:700;font-size:clamp(1.6rem,2vw,2.1rem);line-height:1.12;color:var(--tinte)}
.aga-liste{list-style:none;padding:0;margin:20px 0 0}
.aga-liste li{display:flex;align-items:center;gap:16px;padding:14px 0;border-bottom:1px solid rgba(150,125,64,.22);font-family:var(--serif);font-size:clamp(1.1rem,1.25vw,1.3rem);line-height:1.35;color:rgba(42,26,14,.92)}
.aga-kast{width:20px;height:20px;border:1.4px solid #967d40;border-radius:5px;flex:none}
.aga-idee{margin:18px 0 0;font-size:.95rem;line-height:1.5;color:rgba(42,26,14,.62)}
.aga-symbole{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px 22px;margin:8px 0 0}
.aga-sym{display:grid;gap:12px;align-content:start}
.aga-sym .ico{width:32px;height:32px}
.aga-sym span{font-family:var(--serif);font-size:1.08rem;line-height:1.38;color:rgba(42,26,14,.9)}
.aga-mehr{margin:30px 0 0}
@media(max-width:700px){.aga-bruch{display:none}.aga-reihe{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;scroll-snap-type:x mandatory;gap:22px;padding:6px 4px 18px;scrollbar-width:none}.aga-reihe::-webkit-scrollbar{display:none}.aga-wz{flex:0 0 auto!important;scroll-snap-align:start}.aga-wz__b img{width:auto;height:170px}}
@media(max-width:900px){.aga-zahlen{grid-template-columns:repeat(2,minmax(0,1fr))}.aga-zahl:not(:nth-child(4n+1)){border-left:0}.aga-zahl:nth-child(even){border-left:1px solid rgba(150,125,64,.3)}}
@media(max-width:520px){.aga-symbole{grid-template-columns:repeat(2,minmax(0,1fr))}}
'''
