#!/usr/bin/env python3
"""werkbank/ki.html «KI und Ihre Daten» und werkbank/karte.html + PDF «Ein Vorschlag.» (Wirtschaft am Schlössli, 20.10.2026).

Robert 20.10.2026: «… dass unten auch noch das Angebot ist, dieser ganzen KI-Sache, dieser KI-Seite» (Vorbild ki_seite.py des Grand Beau-Rivage,
nur gelesen; hier eigene, kürzere Fassung im Kleid des Schlössli). Verlinkt aus Gang IV der Karte «Ein Vorschlag.» (sb_angebot.py).

Nur Belegtes:
  · Vier Stellen und «ohne KI»: reception/gast/gast.py (Chat und Antwort-Entwurf, Wissen nur aus Seiten und Unterlagen), reception/reception.js
    («Hier wird nichts verschickt»), imprimerie/api/entwurf.py (ohne KI die passendste fertige Vorlage), livre/livre.py («Gespeichert wird nichts»,
    Messung ohne KI gegen die Palette).
  · Anbieter: privacy.anthropic.com, Artikel «Is my data used for model training?» (kommerzielle Produkte, API), gelesen am 20.10.2026.
  · Gästefragen aus dem Chat gehen mit der Antwort ins Reservationsbuch (gast.py → /api/fragen), damit das Team sieht, was gefragt wurde.
Läuft am Ende von haus.nach_bau(): bau()."""
import html, os, re, subprocess

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
WB = os.path.join(ROOT, 'werkbank')
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'

STAND = '20. Oktober 2026'
HZ = '<svg class="ki-hz" viewBox="256 16 1092 1324" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'
CLAUDE = '<svg class="ki-claude" viewBox="0 0 24 24" role="img" aria-label="Claude"><path fill="currentColor" d="' + open(os.path.join(W, 'ki_claude_pfad.txt'), encoding='utf-8').read().strip() + '"/></svg>'
KOSTEN_OFFEN = 'Nach Verbrauch über das Konto Ihres Hauses. Den Betrag je Aufruf messe ich beim ersten Lauf mit Ihrem Konto und trage ihn hier ein.'

# Aufbau wie ki_seite.py des Grand Beau-Rivage (Robert 20.10.2026: «das KI-Buch sieht bei weitem nicht aus wie die anderen KI-Bücher»):
# Auftakt → Zahlen + Kosten → vier Stellen (Gerät + helle Karte: was sie tut, was zum Anbieter geht, was gespeichert wird, Kosten, Ohne KI)
# → Sorge → Fenster → Daten → Ohne KI → In Ihrer Hand. Kosten stehen nur hier, nicht auf der Karte «Ein Vorschlag.» (Robert 20.10.2026).
AUFTAKT = ('Wo die KI hilft.', 'Und wo Ihre Daten bleiben.',
           'Drei Werkzeuge der Wirtschaft am Schlössli arbeiten an vier Stellen mit Claude, dem Sprachmodell von Anthropic. Hier steht für jede, was sie tut, was sie kostet, wohin Daten gehen und was ohne KI weiterläuft.')
ZAHLEN = [('4', 'Stellen nutzen KI, alles andere arbeitet ohne.'), ('0', 'Ihrer Daten gehen ins Training des Modells.'),
          ('30', 'Tage, dann löscht der Anbieter jede Eingabe.'), ('12', 'Monate bewahrt Ihr Haus Anfragen auf, dann sind sie weg.')]
BLICK = ('Was es kostet', ['Die KI läuft über ein eigenes Konto Ihres Hauses beim Anbieter. Sie zahlen dort direkt nach Verbrauch, ich richte das Konto ein und setze eine Obergrenze je Monat.',
                           'In der Betreuung ist das nicht enthalten. Die fertigen Vorlagen, das Bildarchiv und alles Übrige kosten nichts.'])
STELLEN_KOPF = ('Vier Stellen,', 'genau beschrieben.', 'Was die KI dort tut, was dabei zum Anbieter geht, was Ihr Haus aufbewahrt, was es kostet und was ohne sie bleibt.')
REIHEN = ('Was sie tut', 'Was zum Anbieter geht', 'Was gespeichert wird', 'Kosten', 'Ohne KI')
STELLEN = [  # Name, Werkzeug, Bildschirm (ansichten/Werkzeuge), tut, an, gespeichert, ohne   (Belege: reception/gast/gast.py, reception/reception.py, imprimerie/api/entwurf.py, livre/livre.py)
    ('Der Chat für Ihre Gäste', 'Reservationsbuch', 'reception',
     'Beantwortet Fragen von Gästen zu Karte, Lunch, Terrasse und Anreise, nur aus den Seiten und Unterlagen des Hauses, auf Deutsch, Englisch oder Französisch. Im Entwurf steht er im Reservationsbuch zum Ausprobieren.',
     'Fragen und Antworten des Gesprächs. Name und Kontakt nur, wenn ein Gast selbst etwas anfragt.',
     'Fragen und Antworten im Reservationsbuch, damit Ihr Team sieht, was Gäste wissen wollen; nach zwölf Monaten gelöscht.',
     'Telefon, Reservation bei gastronovi und Gutschein stehen wie heute auf jeder Seite.'),
    ('Antwort auf eine Anfrage', 'Reservationsbuch', 'reception-2',
     'Schreibt Ihrem Team einen Antwortentwurf auf eine Anfrage zu Bankett, Anlass oder Reservation, im Ton des Hauses.',
     'Die Anfrage mit Name, Kontakt und Anliegen.',
     'Anfragen im Reservationsbuch, nach zwölf Monaten gelöscht, auf Wunsch des Gastes sofort.',
     'Eingang und Anfragen lassen sich bedienen. Die Antwort schreibt das Team dann selbst. Verschickt wird ohnehin nur, was jemand abschickt.'),
    ('Fünf Entwürfe', 'Hausdruckerei', 'imprimerie',
     'Macht aus einem Satz wie «Bankettmenü Herbst» fünf Entwürfe im Stil des Hauses.',
     'Ihr Satz, dazu Marke, Fotos und Texte der Website. Keine Angaben zu Gästen.',
     'Ihre Arbeiten und eigenen Fotos bleiben im Browser auf Ihrem Gerät.',
     'Alle fertigen Vorlagen lassen sich öffnen, ändern und als PDF speichern; ohne KI nimmt sie die passendste fertige Vorlage.'),
    ('Eine Markenprüfung', 'Bildarchiv', 'livre',
     'Prüft einen Entwurf, etwa eine Anzeige der Druckerei oder einer Agentur, gegen Farben, Zeichen und Schrift des Hauses.',
     'Die ersten zwei Seiten der Datei als Bild.',
     'Nichts.',
     'Fotos, Dateien und die Messung der Farben laufen weiter. Nur die schriftliche Beurteilung fehlt.')]
SORGE = ('Und wenn die KI Gästen etwas Falsches sagt?',
         'Diese Sorge ist berechtigt. Die KI darf nur sagen, was Ihr Haus selbst veröffentlicht hat, und sie muss offen sagen, wenn sie etwas nicht weiss, mit Telefon und Mail des Hauses. '
         'Ganz ausschliessen lässt sich ein Fehler bei einer KI trotzdem nicht. Verbindlich bleiben Reservation und Ihr Team.')
FENSTER = ('Die KI schreibt.', 'Ihr Team entscheidet.', 'Keine Mail an einen Gast geht hinaus, ohne dass jemand aus Ihrem Haus sie abschickt.')
DATEN_KOPF = ('Was mit Ihren Daten', 'geschieht.', 'Der Anbieter des Sprachmodells ist Anthropic. Was er zusagt, steht in seinen Geschäftsbedingungen; was Ihr Haus aufbewahrt, bestimmen Sie.')
ANBIETER = ('Claude', 'Sprachmodell von Anthropic PBC, San Francisco')
DATEN = [('Nicht zum Lernen', 'Anthropic nutzt, was über das Konto Ihres Hauses läuft, nicht zum Training seiner Modelle.'),
         ('Nach 30 Tagen gelöscht', 'Eingaben und Antworten löscht Anthropic innert 30 Tagen. Länger nur bei Verstössen gegen seine Nutzungsregeln oder wenn ein Gesetz es verlangt.'),
         ('Ihr eigener Speicher', 'Was Ihr Haus aufbewahrt, liegt im Reservationsbuch, nur mit Zugang lesbar, und wird nach zwölf Monaten gelöscht.'),
         ('Menschen verschicken', 'Die KI verschickt keine Mails und reserviert nichts. Jede Antwort per Mail geht von Ihrem Team hinaus.'),
         ('Reserviert wird woanders', 'Tische laufen über gastronovi, Gutscheine über zenchef. Karten- und Zahlungsdaten gehören nicht in den Chat.'),
         ('Abschaltbar', 'Jede der vier Stellen lässt sich einzeln abschalten, das Werkzeug arbeitet weiter.')]
OHNE_KOPF = ('Läuft auch', 'ohne KI.', 'Fällt die KI aus, ist das Guthaben aufgebraucht oder schalten Sie sie ab, arbeiten alle Werkzeuge weiter. Es fehlt nur, was die KI schreibt.')
HAND_KOPF = ('Sie entscheiden,', 'wie weit sie geht.')
HAND = [('Das Konto', 'läuft auf Ihr Haus, mit Ihrer Karte. Beim Anbieter sehen Sie jeden Aufruf und jeden Betrag.'),
        ('Die Obergrenze', 'setze ich je Monat. Ist sie erreicht, laufen die Werkzeuge bis zum nächsten Monat ohne KI weiter.'),
        ('Der Schalter', 'liegt bei Ihnen. Auf Ihren Wunsch schalte ich die KI ab, die Werkzeuge laufen weiter wie beschrieben.')]
OFFEN = ('Was Ihr Haus noch festlegt', 'Ihre Datenschutzerklärung bekommt vor dem Start einen Abschnitt zum Chat. Zwei Punkte entscheidet Ihr Haus: die Rechtsgrundlage für die Übermittlung in die USA und wie lange Anfragen aufbewahrt werden.')
QUELLEN = [('Anthropic: Training mit Daten', 'https://privacy.anthropic.com/en/articles/7996868-is-my-data-used-for-model-training'),
           ('Anthropic: Aufbewahrung', 'https://privacy.anthropic.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data')]
NAV = ('<nav aria-label="Kapitel"><a href="#ki-blick">KI</a><a href="#ki-zahlen">Kosten</a><a href="#ki-stellen">Vier Stellen</a><a href="#ki-daten">Ihre Daten</a>'
       '<a href="#ki-ohne">Ohne KI</a><a href="#ki-hand">In Ihrer Hand</a><a href="index.html#sag-vorschlag">Zurück zum Vorschlag</a></nav>')


def titel(z1, z2, cls='t2', tag='h2'):
    return f'<{tag} class="{cls} zt"><span class="z"><span>{e(z1)}</span></span><span class="z"><span><em>{e(z2)}</em></span></span></{tag}>'


def kopf_mitte(z1, z2, lauf):
    return f'<header class="ki-kopf"><div data-a="auf">{HZ}</div>{titel(z1, z2)}<p class="ki-lauf" data-a="worte">{e(lauf)}</p></header>'


def geraete():
    """Laptop mit dem echten Bildschirm je Stelle (Gehäuse der Werkbank, objekte_bau.laptop), nach werkbank/img/ki-geraet-<n>.webp."""
    import objekte_bau as OB
    os.makedirs(os.path.join(WB, 'img'), exist_ok=True)
    for _n, _w, b, *_x in STELLEN:
        q = os.path.join(W, 'ansichten', 'Werkzeuge', b + '.jpg')
        if os.path.exists(q):
            im = OB.laptop(q); im.thumbnail((1600, 1600)); im.save(os.path.join(WB, 'img', f'ki-geraet-{b}.webp'), quality=82)


def hauptteil():
    zahlen = ''.join(f'<div class="ki-zahl" data-a="auf" style="--i:{i}"><p class="ki-zahl__n"><span class="odo" data-z="{z}">{z}</span></p><p class="ki-zahl__t">{e(t)}</p></div>' for i, (z, t) in enumerate(ZAHLEN))
    kosten = ''.join(f'<li class="mn-p"><p class="mn-p__z"><b>{e(n)}</b><i></i><span>{e(w)}</span></p><p class="mn-p__s">{e(KOSTEN_OFFEN)}</p></li>' for n, w, *_x in STELLEN)
    stellen = ''
    for i, (n, w, b, tut, an, sp, ohne) in enumerate(STELLEN):
        reihen = ''.join(f'<div class="ki-k__r"><dt>{e(REIHEN[j])}</dt><dd>{e(x)}</dd></div>' for j, x in enumerate((tut, an, sp, KOSTEN_OFFEN)))
        stellen += (f'<article class="ki-st{" ki-st--um" if i % 2 else ""}"><figure class="ki-geraet" data-a="kipp"><img src="img/ki-geraet-{b}.webp" alt="{e(w)} am Laptop: {e(n)}" loading="lazy" decoding="async"></figure>'
                    f'<div class="ag-blatt ki-k" data-a="heben"><h3 class="ki-k__t">{e(n)}</h3><p class="ki-k__preis">{e(w)}</p><dl>{reihen}</dl>'
                    f'<div class="ki-k__ohne"><p class="ki-k__ohne-t">{e(REIHEN[4])}</p><p>{e(ohne)}</p></div></div></article>')
    daten = ''.join(f'<div class="ki-d" data-a="heben"><span class="ki-siegel" aria-hidden="true"><i></i></span><h3>{e(t)}</h3><p>{e(s)}</p></div>' for t, s in DATEN)
    ohne = ''.join(f'<div class="ki-o" data-a="kipp" style="--i:{i}"><h3>{e(s[0])}</h3><p>{e(s[6])}</p></div>' for i, s in enumerate(STELLEN))
    hand = ''.join(f'<p class="ki-h" data-a="auf" style="--i:{i}"><b>{e(t)}</b>{e(s)}</p>' for i, (t, s) in enumerate(HAND))
    quellen = ''.join(f'<li><a href="{q}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, q in QUELLEN)
    f1, f2, fs = FENSTER
    return f'''
<section class="fl fl--nacht tapete-leicht ki ki-auftakt" id="ki-blick">
  <div class="in"><div data-a="auf">{HZ}</div>{titel(AUFTAKT[0], AUFTAKT[1], 't1', 'h1')}<p class="ki-lauf" data-a="worte">{e(AUFTAKT[2])}</p></div>
</section>
<section class="fl fl--navy tapete blatt ki" id="ki-zahlen">
  <div class="in">
    <div class="ki-zahlen">{zahlen}</div>
    <div class="ag-blatt ki-blick" data-a="heben">
      <div class="ki-blick__text"><div class="ki-marke">{CLAUDE}<span>{e(ANBIETER[0])}</span></div><h3 class="ki-k__t">{e(BLICK[0])}</h3>{''.join(f'<p>{e(p)}</p>' for p in BLICK[1])}</div>
      <div><ul class="mn-l mn-preise ki-preise">{kosten}</ul></div>
    </div>
  </div>
</section>
<section class="fl fl--navy tapete blatt ki" id="ki-stellen">
  <div class="in">{kopf_mitte(*STELLEN_KOPF)}<div class="ki-stellen">{stellen}</div>
    <div class="ag-blatt ki-offen ki-sorge" data-a="heben"><h3 class="ki-k__t">{e(SORGE[0])}</h3><p>{e(SORGE[1])}</p></div></div>
</section>
<section class="wfen" id="ki-fenster" aria-label="{e(f1)} {e(f2)}">
  <div class="wfen__f">
    <img src="eigen/fen-fenster-tisch-1800.webp" srcset="eigen/fen-fenster-tisch-1200.webp 1200w, eigen/fen-fenster-tisch-1800.webp 1800w, eigen/fen-fenster-tisch-2400.webp 2400w" sizes="100vw" alt="Ein gedeckter Tisch in der Wirtschaft am Schlössli" loading="lazy" decoding="async">
    <div class="wfen__in"><svg class="wfen__z" viewBox="256 16 1092 1324" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg><h2 class="wfen__t"><span>{e(f1)}</span><span><em>{e(f2)}</em></span></h2><p class="wfen__k">{e(fs)}</p></div>
  </div>
</section>
<section class="fl fl--papier tapete-hell blatt ki" id="ki-daten">
  <div class="in">{kopf_mitte(*DATEN_KOPF)}
    <div class="ki-anbieter" data-a="auf">{CLAUDE}<p><b>{e(ANBIETER[0])}</b><span>{e(ANBIETER[1])}</span></p></div>
    <div class="ki-daten">{daten}</div></div>
</section>
<section class="fl fl--creme tapete-hell blatt ki" id="ki-ohne">
  <div class="in">{kopf_mitte(*OHNE_KOPF)}<div class="ki-ohne">{ohne}</div></div>
</section>
<section class="fl fl--nacht tapete-leicht blatt ki" id="ki-hand">
  <div class="in">
    <div class="ki-hand">
      <figure class="ki-hand__b" data-a="kipp"><img src="img/ki-team.webp" alt="Das Team der Wirtschaft am Schlössli" loading="lazy" decoding="async"></figure>
      <div class="ki-hand__t"><div data-a="auf">{HZ}</div>{titel(*HAND_KOPF)}{hand}</div>
    </div>
    <div class="ag-blatt ki-offen" data-a="heben"><h3 class="ki-k__t">{e(OFFEN[0])}</h3><p>{e(OFFEN[1])}</p>
      <p class="ki-knoepfe"><a class="kn kn--klein" href="../datenschutz.html" target="_blank" rel="noopener">Ihre Datenschutzerklärung heute<i>{PF}</i></a>
      <a class="kn kn--klein" href="index.html#sag-vorschlag">Zurück zum Vorschlag<i>{PF}</i></a></p>
      <p class="ki-quellen">Angaben des Anbieters, gelesen am {STAND}:</p><ul class="ki-quellen__l">{quellen}</ul></div>
  </div>
</section>
<script>
(function () {{ var f = document.getElementById('ki-fenster'); if (!f) return; if (!('IntersectionObserver' in window)) {{ f.classList.add('da'); return; }}
  f.classList.add('weg'); new IntersectionObserver(function (es) {{ f.classList.toggle('weg', !es[0].isIntersecting); }}).observe(f);
  new IntersectionObserver(function (es, o) {{ if (es[0].isIntersecting) {{ o.disconnect(); f.classList.add('da'); }} }}, {{ threshold: 0.35 }}).observe(f); }})();
</script>
'''


def ki_seite(t):
    geraete()
    from PIL import Image
    q = os.path.join(ROOT, 'assets', 'img', 'team-1200.webp')
    if os.path.exists(q):
        Image.open(q).convert('RGB').save(os.path.join(WB, 'img', 'ki-team.webp'), quality=82)
    m0, m1 = t.find('<main id="oben">'), t.find('</main>')
    kopf = t[:m0]
    kopf = re.sub(r'<title>.*?</title>', '<title>KI und Ihre Daten · Wirtschaft am Schlössli</title>', kopf, count=1, flags=re.S)
    kopf = re.sub(r'<nav aria-label="Kapitel">.*?</nav>', NAV, kopf, count=1, flags=re.S)
    import sb_farbe as SF
    kopf = kopf.replace('</head>', SF.ohne_fett(SF.faerbe(open(os.path.join(W, 'sb_ki.css'), encoding='utf-8').read())) + '\n<style>.ki-claude{color:#d97757!important}</style>\n</head>', 1)
    return kopf + '<main id="oben">' + hauptteil() + t[m1:]


def _kopf(t, titel):
    css = ''.join(re.findall(r'<link rel="stylesheet" href="[^"]*(?:werkbank|kapitel)\.css[^"]*">', t))
    fonts = ''.join(re.findall(r'<link rel="preload"[^>]*font[^>]*>', t))
    return f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)} · Wirtschaft am Schlössli</title>
<meta name="robots" content="noindex, nofollow">
{fonts}
{css}'''


def karte_seite(t):
    m = re.search(r'<article class="mn".*?</article>', t, re.S)
    if not m:
        return None
    karte = m.group(0).replace('<article class="mn" data-a="heben">', '<article class="mn da">')
    return _kopf(t, 'Ein Vorschlag') + '''
<style>
html,body{margin:0;background:var(--nacht,#0b1d3d)}
body{min-height:100vh;display:flex;justify-content:center;align-items:flex-start;padding:clamp(20px,4vw,64px) 16px}
.mn{opacity:1!important;transform:none!important;transition:none!important}
.mn-pdf{display:none!important}
@page{margin:0}
@media print{html,body{background:#fbfcfe;padding:0;display:block}.mn{width:100%;max-width:none;border-radius:0;box-shadow:none;padding:14mm 18mm;zoom:.86}.mn-ki{display:none!important}.mn-gang,.mn-l li,.mn-p{break-inside:avoid}}
</style>
</head>
<body>
''' + karte + '\n</body>\n</html>\n'


PDF_JS = r'''
const path = require('path');
const { chromium } = require(process.env.HOME + '/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('http://127.0.0.1:8982/werkbank/karte.html', { waitUntil: 'load' }); await p.evaluate(() => document.fonts && document.fonts.ready);
  await p.pdf({ path: process.argv[2], format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); console.log('PDF', process.argv[2]); })();
'''


def bau():
    idx = os.path.join(WB, 'index.html')
    if not os.path.exists(idx):
        return
    t = open(idx, encoding='utf-8').read()
    open(os.path.join(WB, 'ki.html'), 'w', encoding='utf-8').write(ki_seite(t))
    k = karte_seite(t)
    if k:
        open(os.path.join(WB, 'karte.html'), 'w', encoding='utf-8').write(k)
        js = os.path.join(W, '_karte_pdf.js'); open(js, 'w', encoding='utf-8').write(PDF_JS)
        import sb_angebot as SA
        r = subprocess.run(['node', js, os.path.join(WB, SA.PDF_NAME)], capture_output=True, text=True, timeout=120)
        print(r.stdout.strip() or ('PDF nicht gebaut: ' + r.stderr[-300:]))


if __name__ == '__main__':
    bau()
