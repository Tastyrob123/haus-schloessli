#!/usr/bin/env python3
"""werkbank/ki.html «KI und Ihre Daten» für den Landgasthof Ruedihus (Werkbank-Chat 17.10.2026, Regel 8 im Website-Bau-Master: das Kapitel «Wo die KI arbeitet»
mit «Mehr zu KI und Ihren Daten», Vorbild Grand Beau-Rivage _werkbank/ki_seite.py, über dh_ki.py des Waldhotel Doldenhorn; beide nur gelesen; Inhalt fürs
Ruedihus, ohne Preise). Verlinkt aus Gang IV «Wo die KI arbeitet» der Karte «Ein Vorschlag.» (rh_angebot.py) und aus «Ihre Daten» im Angebot.

Nur Belegtes (gelesen am 17.10.2026 im Ruedihus):
  · Rezeption im Chat: rechtliches.html, Abschnitt «KI-Assistent der Rezeption» (Fragen, Sprache, Datum; IP nur im Arbeitsspeicher; Frankfurt am Main;
    E-Mail/Telefon unkenntlich; zwölf Monate; öffentliche Angaben der Bergbahnen), assets/js/gast.js (Rückfall ohne Antwort).
  · Der Gastgeber: Antwortbrief und Einlesen von Links (_werkzeuge/reception/reception.js), ohne KI Probe-Antworten (LIEFERUNG), keine Löschfrist gebaut.
  · Die Werkstatt: «Fünf Entwürfe» (_werkzeuge/imprimerie/api/entwurf.py, Wissen des Hauses), Medien im Browser (ds-ruedihus-*), 256 Vorlagen ohne KI.
  · Das Hausbuch: _werkzeuge/livre/livre.py (Entwurf als Bild und Messung der Farben an Claude, «Gespeichert wird nichts», Probe aus der Messung).
  · Anbieter: privacy.claude.com, anthropic.com/legal/data-processing-addendum (wie beim Doldenhorn am 17.10.2026 gelesen)."""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rh_angebot import KI_PREISE, KI_FUSS   # Preise des Anbieters wie im Rivage (Robert 18.10.2026)

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
e = html.escape
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
STAND = '17. Oktober 2026'
HZ = '<svg class="ki-hz" viewBox="0 0 1044 1398" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'
CLAUDE_PFAD = open(os.path.join(W, 'ki_claude_pfad.txt'), encoding='utf-8').read().strip()
CLAUDE = f'<svg class="ki-claude" viewBox="0 0 24 24" role="img" aria-label="Claude"><path fill="currentColor" d="{CLAUDE_PFAD}"/></svg>'

AUFTAKT = ('Wo die KI mitarbeitet.', 'Und wo Ihre Daten bleiben.',
           'An vier Stellen arbeitet im Ruedihus Claude mit, das Sprachmodell von Anthropic. Hier steht zu jeder, was sie tut, was dabei zum Anbieter geht, was gespeichert wird und was ohne KI weiterläuft.')
ZAHLEN = [('4', 'Stellen arbeiten mit KI, alles andere ohne.'),
          ('0', 'Ihrer Eingaben nutzt der Anbieter fürs Training, solange niemand ausdrücklich zustimmt.'),
          ('30', 'Tage, dann löscht der Anbieter jede Eingabe.'),
          ('12', 'Monate bewahrt die Rezeption im Chat Fragen auf, danach sind sie gelöscht.')]
BLICK = ('Wie es abgerechnet wird', [
    'Die KI läuft über ein eigenes Konto Ihres Hauses beim Anbieter und wird dort nach Verbrauch abgerechnet. Ich richte das Konto ein und setze eine Obergrenze je Monat; den Rahmen bestimmen Sie.',
    'Alles andere braucht kein Guthaben: die fertigen Vorlagen, das Markenbuch und die Werkzeuge, wenn sie ohne KI arbeiten.'])
STELLEN_KOPF = ('Vier Stellen,', 'genau beschrieben.', 'Was die KI dort tut, was dabei zum Anbieter geht, was Ihr Haus aufbewahrt und was ohne sie bleibt.')
STELLEN = [  # Name, Gerät, Bildschirm, Beschreibung, was sie tut, was zum Anbieter geht, was gespeichert wird, ohne KI
    ('Rezeption im Chat', 'handy', 'ansichten/Chat/chat-h.jpg', 'Der Chat der Rezeption am Handy',
     'Beantwortet Fragen von Gästen auf jeder Seite, aus Ihren Seiten, Ihren Unterlagen und den öffentlichen Angaben der Bergbahnen, und legt die Buchung ins Gespräch.',
     'Fragen und Antworten des Gesprächs, die Sprache der Seite und das Datum. Namen oder E-Mail-Adresse braucht der Chat nicht.',
     'Jede Frage mit ihrer Antwort, E-Mail-Adressen und Telefonnummern vorher unkenntlich, gespeichert in Frankfurt am Main und nach zwölf Monaten gelöscht. Die IP-Adresse nur im Arbeitsspeicher, gegen zu viele Anfragen.',
     'Statt einer Antwort zeigt der Chat die passende Stelle aus «Gut zu wissen» und die Nummer der Rezeption. Die Buchung auf der Website läuft davon unabhängig.'),
    ('Der Gastgeber', 'laptop', '../_werkzeuge/maison/roh/reception.jpg', 'Der Gastgeber am Laptop',
     'Schreibt Ihrem Team zu jeder Anfrage einen Antwortbrief im Ton Ihrer Hausmails und liest Links ein, damit der Chat Neues kennt.',
     'Die Anfrage mit Name, Kontakt und Anliegen; beim Einlesen der Inhalt der verlinkten Seite.',
     'Anfragen liegen im Speicher Ihrer Website, bis Ihr Team sie löscht. Eine feste Frist legt Ihr Haus noch fest.',
     'Eingang, Anfragen und das Wissen des Chats lassen sich weiter bedienen. Den Brief schreibt Ihr Team dann selbst.'),
    ('Die Werkstatt', 'laptop', '../_werkzeuge/maison/roh/imprimerie.jpg', 'Die Werkstatt am Laptop',
     'Macht aus einem Satz wie «Plakat zur Metzgete» fünf Entwürfe im Stil des Hauses.',
     'Ihr Satz, dazu Marke, Fotokatalog und Texte der Website. Keine Angaben zu Gästen.',
     'Ihre Arbeiten und eigenen Fotos bleiben im Browser auf Ihrem Gerät.',
     'Alle fertigen Vorlagen lassen sich öffnen, ändern und als PDF speichern. Nur das Entwerfen aus einem Satz braucht die KI.'),
    ('Das Hausbuch', 'laptop', '../_werkzeuge/maison/roh/livre-pruefung.jpg', 'Das Hausbuch am Laptop mit der Markenprüfung',
     'Prüft einen Entwurf, etwa eine Anzeige oder einen Flyer der Druckerei, gegen die Marke des Hauses.',
     'Die ersten drei Seiten der Datei als Bild, dazu die Messung der Farben.',
     'Nichts. Der Entwurf liegt nur für die Prüfung im Arbeitsspeicher und wird danach gelöscht.',
     'Markenbuch, Fotos, Dateien und die Messung der Farben laufen weiter. Nur die schriftliche Beurteilung fehlt.')]
REIHEN = ('Was sie tut', 'Was zum Anbieter geht', 'Was gespeichert wird', 'Ohne KI')
FENSTER = ('Die KI schreibt.', 'Ihr Team entscheidet.', 'Keine Antwort geht an einen Gast, ohne dass jemand aus Ihrem Haus sie liest und selbst weitergibt.', 'gedeck', 'Eine festlich gedeckte Tafel im Landgasthof Ruedihus')
DATEN_KOPF = ('Was mit Ihren Daten', 'geschieht.', 'Der Anbieter des Sprachmodells ist Anthropic. Was er zusagt, steht in seinen Bedingungen; was Ihr Haus aufbewahrt, bestimmen Sie.')
ANBIETER = ('Claude', 'Sprachmodell von Anthropic PBC, San Francisco')
DATEN = [
    ('Nicht zum Lernen', 'Was über das Konto Ihres Hauses läuft, nutzt Anthropic nicht zum Training seiner Modelle, solange niemand ausdrücklich zustimmt.'),
    ('Nach 30 Tagen gelöscht', 'Eingaben und Antworten löscht Anthropic innert 30 Tagen. Länger nur bei Verstössen gegen seine Nutzungsregeln oder wenn ein Gesetz es verlangt.'),
    ('Mit Vertrag', 'Ein Vertrag zur Auftragsbearbeitung mit Standardvertragsklauseln ist Teil der Geschäftsbedingungen und gilt mit dem Konto Ihres Hauses.'),
    ('Ihr eigener Speicher', 'Was Ihr Haus aufbewahrt, liegt im Speicher Ihrer Website und ist nur über die Werkzeuge lesbar.'),
    ('Menschen geben weiter', 'Die KI verschickt nichts und bucht nichts. Jede Antwort an einen Gast geht über Ihr Team hinaus.'),
    ('Gebucht wird woanders', 'Gebucht und bezahlt wird in Ihrem SimpleBooking. Karten- und Ausweisdaten gehören nicht in den Chat.')]
OHNE_KOPF = ('Läuft auch', 'ohne KI.', 'Fällt die KI aus, ist das Guthaben aufgebraucht oder schalten Sie sie ab, arbeiten alle vier Stellen weiter. Es fehlt nur, was die KI schreibt.')
HAND_KOPF = ('Sie entscheiden,', 'wie weit sie geht.')
HAND = [('Das Konto', 'läuft auf Ihr Haus. Beim Anbieter sehen Sie jeden Aufruf und jeden Betrag.'),
        ('Die Obergrenze', 'setze ich je Monat. Ist sie erreicht, arbeiten die Werkzeuge bis zum nächsten Monat ohne KI.'),
        ('Der Schalter', 'liegt bei Ihnen. Auf Ihren Wunsch schalte ich die KI ab, die Werkzeuge laufen weiter wie beschrieben.')]
OFFEN = ('Was Ihr Haus noch festlegt',
         'Die Datenschutzerklärung der Website hat einen Abschnitt zur Rezeption im Chat, als Entwurf. Ihr Haus legt noch fest: die Rechtsgrundlage für die Übermittlung in die USA und wie lange Anfragen aufbewahrt werden.')
KNOEPFE = ('Entwurf der Datenschutzerklärung', 'Zurück zum Angebot')
QUELLEN_SATZ = f'Angaben des Anbieters, gelesen am {STAND}:'
QUELLEN = [('Anthropic: Training mit Daten', 'https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training'),
           ('Anthropic: Aufbewahrung', 'https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data'),
           ('Anthropic: Vertrag zur Auftragsbearbeitung', 'https://www.anthropic.com/legal/data-processing-addendum')]


# Robert 18.10.2026 (Safari, online): «Ich dachte, dass da Videos sind»: an jeder der vier Stellen ein Film aus dem echten Werkzeug, mit Probe-Daten,
# ohne KI-Aufruf (Rezeption im Chat: der Handy-Film der Werkbank; die übrigen: node _werkbank/ki_filme.js → _werkbank/kifilm/)
FILME = {0: ('../assets/video/rezeption-schirm-m.mp4', 'eigen/rezeption-fondue-start.webp'),   # Robert 18.10.2026 23:31: das Fondue-Gespräch statt «Wie alt ist das Haus?»
         1: ('kifilm/ki-reception.mp4', 'kifilm/ki-reception.webp'),
         2: ('kifilm/ki-imprimerie.mp4', 'kifilm/ki-imprimerie.webp'), 3: ('kifilm/ki-livre.mp4', 'kifilm/ki-livre.webp')}
FILM_JS = """<script>(function(){var v=[].slice.call(document.querySelectorAll('video.ki-film'));if(!v.length)return;
var ruhig=matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!('IntersectionObserver' in window)||ruhig)return;
var io=new IntersectionObserver(function(es){es.forEach(function(x){var f=x.target;if(x.isIntersecting){if(f.preload!=='auto')f.preload='auto';var p=f.play();if(p&&p.catch)p.catch(function(){})}else f.pause()})},{threshold:.35});
v.forEach(function(f){io.observe(f)})})();</script>"""


def schirm(art, quelle, alt):
    img = f'<img src="img/ki-s-{quelle[0]}.webp" alt="{e(alt)}" loading="lazy" decoding="async">'
    fi = FILME.get(quelle[0])
    if fi and os.path.exists(os.path.join(ROOT, 'werkbank', fi[0])):
        img = f'<video class="ki-film" src="{fi[0]}" poster="{fi[1]}" muted loop playsinline preload="none" aria-label="{e(alt)}"></video>'
    if art == 'laptop':
        return (f'<figure class="ki-geraet ki-geraet--laptop" data-a="kipp"><div class="ki-laptop"><div class="ki-laptop__s">{img}</div>'
                f'<img class="ki-laptop__g" src="img/ins-geraet.webp" width="2000" height="1673" alt="" decoding="async"></div></figure>')
    return f'<figure class="ki-geraet ki-geraet--handy" data-a="kipp"><div class="ki-handy"><div class="ki-handy__s">{img}</div></div></figure>'


def titel(z1, z2, cls='t2', tag='h2'):
    return f'<{tag} class="{cls} zt"><span class="z"><span>{e(z1)}</span></span><span class="z"><span><em>{e(z2)}</em></span></span></{tag}>'


def kopf_mitte(z1, z2, lauf):
    return f'<header class="ki-kopf"><div data-a="auf">{HZ}</div>{titel(z1, z2)}<p class="ki-lauf" data-a="worte">{e(lauf)}</p></header>'


def bilder():
    from PIL import Image
    import shutil
    img = os.path.join(ROOT, 'werkbank', 'img')
    kf, kz = os.path.join(W, 'kifilm'), os.path.join(ROOT, 'werkbank', 'kifilm')
    if os.path.isdir(kf):
        os.makedirs(kz, exist_ok=True)
        for n in os.listdir(kf):
            if n.startswith('ki-'):
                shutil.copy2(os.path.join(kf, n), os.path.join(kz, n))
    for i, s in enumerate(STELLEN):
        q = os.path.join(W, s[2]) if not s[2].startswith('..') else os.path.join(W, s[2])
        im = Image.open(os.path.normpath(q)).convert('RGB')
        im.thumbnail((1200, 1600) if s[1] == 'handy' else (1440, 1440))
        im.save(os.path.join(img, f'ki-s-{i}.webp'), 'WEBP', quality=82, method=5)
    for k, quelle, breite in (('gedeck', 'fest-tafel', 2400), ('familie', 'familie', 1100)):   # Ruedihus: die festliche Tafel und die Familie Maeder
        a = os.path.join(ROOT, 'assets', 'img')
        q = next(os.path.join(a, quelle + s) for s in ('-g.webp', '-l.webp', '.webp') if os.path.exists(os.path.join(a, quelle + s)))
        im = Image.open(q).convert('RGB'); im.thumbnail((breite, breite))
        im.save(os.path.join(img, f'ki-{k}.webp'), 'WEBP', quality=80, method=5)
        yield k, im.size


def hauptteil(gr):
    zahlen = ''.join(f'<div class="ki-zahl" data-a="auf" style="--i:{i}"><p class="ki-zahl__n"><span class="odo" data-z="{z}">{z}</span></p><p class="ki-zahl__t">{e(t)}</p></div>' for i, (z, t) in enumerate(ZAHLEN))
    stellen = ''
    for i, (n, art, _q, alt, tut, an, sp, ohne) in enumerate(STELLEN):
        reihen = ''.join(f'<div class="ki-k__r"><dt>{e(REIHEN[j])}</dt><dd>{e(x)}</dd></div>' for j, x in enumerate((tut, an, sp)))
        stellen += (f'<article class="ki-st{" ki-st--um" if i % 2 else ""}" id="ki-st-{i + 1}">{schirm(art, (i,), alt)}'
                    f'<div class="ag-blatt ki-k" data-a="mkhoch" style="--vz:120ms"><h3 class="ki-k__t">{e(n)}</h3><p class="ki-k__preis">{e(KI_PREISE[n][0])}</p><dl>{reihen}</dl>'
                    f'<div class="ki-k__ohne"><p class="ki-k__ohne-t">{e(REIHEN[3])}</p><p>{e(ohne)}</p></div></div></article>')
    daten = ''.join(f'<div class="ki-d" data-a="mkhoch" style="--vz:{(i % 3) * 110}ms"><span class="ki-siegel" aria-hidden="true"><i></i></span><h3>{e(t)}</h3><p>{e(s)}</p></div>' for i, (t, s) in enumerate(DATEN))
    ohne = ''.join(f'<div class="ki-o" data-a="kipp" style="--i:{i}"><h3>{e(s[0])}</h3><p>{e(s[7])}</p></div>' for i, s in enumerate(STELLEN))
    hand = ''.join(f'<p class="ki-h" data-a="auf" style="--i:{i}"><b>{e(t)}</b>{e(s)}</p>' for i, (t, s) in enumerate(HAND))
    quellen = ''.join(f'<li><a href="{q}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, q in QUELLEN)
    stellen_liste = ''.join(f'<li class="mn-p"><p class="mn-p__z"><b>{e(s[0])}</b><i></i><span>{e(KI_PREISE[s[0]][0])}</span></p><p class="mn-p__s">{e(KI_PREISE[s[0]][1])}</p></li>' for s in STELLEN)
    fz1, fz2, fsatz, fk, falt = FENSTER
    fw, fh = gr['gedeck']
    return f'''
<section class="fl fl--nacht tapete-leicht ki ki-auftakt" id="ki-blick">
  <div class="in">
    <div data-a="auf">{HZ.replace('ki-hz', 'ki-hz ki-paar__hz')}</div>
    {titel(AUFTAKT[0], AUFTAKT[1], 't1', 'h1')}
    <p class="ki-lauf" data-a="worte">{e(AUFTAKT[2])}</p>
  </div>
</section>
<section class="fl fl--navy tapete blatt ki" id="ki-zahlen">
  <div class="in">
    <div class="ki-zahlen">{zahlen}</div>
    <div class="ag-blatt ki-blick" data-a="mkhoch">
      <div class="ki-blick__text"><div class="ki-marke">{CLAUDE}<span>{e(ANBIETER[0])}</span></div><h3 class="ki-k__t">{e(BLICK[0])}</h3>{''.join(f'<p>{e(p)}</p>' for p in BLICK[1])}</div>
      <div><ul class="mn-l mn-preise ki-preise">{stellen_liste}</ul><p class="mn-fuss">{e(KI_FUSS)}</p></div>
    </div>
  </div>
</section>
<section class="fl fl--navy tapete blatt ki" id="ki-stellen">
  <div class="in">
    {kopf_mitte(*STELLEN_KOPF)}
    <div class="ki-stellen">{stellen}</div>
  </div>
</section>
<section class="wfen" id="ki-fenster" aria-label="{e(fz1)} {e(fz2)}">
  <div class="wfen__f">
    <img src="img/ki-{fk}.webp" sizes="100vw" width="{fw}" height="{fh}" alt="{e(falt)}" loading="lazy" decoding="async">
    <div class="wfen__in"><svg class="wfen__z" viewBox="0 0 1044 1398" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg><h2 class="wfen__t"><span>{e(fz1)}</span><span><em>{e(fz2)}</em></span></h2><p class="wfen__k">{e(fsatz)}</p></div>
  </div>
</section>
<script>
(function () {{ var f = document.getElementById('ki-fenster'); if (!f) return; if (!('IntersectionObserver' in window)) {{ f.classList.add('da'); return; }}
  f.classList.add('weg'); new IntersectionObserver(function (es) {{ f.classList.toggle('weg', !es[0].isIntersecting); }}).observe(f);
  new IntersectionObserver(function (es, o) {{ if (es[0].isIntersecting) {{ o.disconnect(); f.classList.add('da'); }} }}, {{ threshold: 0.35 }}).observe(f); }})();
</script>
<section class="fl fl--papier tapete-hell blatt ki" id="ki-daten">
  <div class="in">
    {kopf_mitte(*DATEN_KOPF)}
    <div class="ki-anbieter" data-a="auf">{CLAUDE}<p><b>{e(ANBIETER[0])}</b><span>{e(ANBIETER[1])}</span></p></div>
    <div class="ki-daten">{daten}</div>
  </div>
</section>
<section class="fl fl--creme tapete-hell blatt ki" id="ki-ohne">
  <div class="in">
    {kopf_mitte(*OHNE_KOPF)}
    <div class="ki-ohne">{ohne}</div>
  </div>
</section>
<section class="fl fl--nacht tapete-leicht blatt ki" id="ki-hand">
  <div class="in">
    <div class="ki-hand ki-hand--ohne-bild">
      <header class="ki-hand__t"><div data-a="auf">{HZ}</div>{titel(*HAND_KOPF)}</header>
      <div class="ki-hand__k">{hand}</div>
    </div>
    <div class="ag-blatt ki-offen" data-a="mkhoch">
      <h3 class="ki-k__t">{e(OFFEN[0])}</h3><p>{e(OFFEN[1])}</p>
      <p class="ki-knoepfe"><a class="kn kn--klein" href="../rechtliches.html#ki-assistent" target="_blank" rel="noopener">{e(KNOEPFE[0])}<i>{PF}</i></a>
      <a class="kn kn--klein" href="index.html#k8">{e(KNOEPFE[1])}<i>{PF}</i></a></p>
      <p class="ki-quellen">{e(QUELLEN_SATZ)}</p><ul class="ki-quellen__l">{quellen}</ul>
    </div>
  </div>
</section>
'''


CSS = '''
/* Ruedihus: die festliche Tafel ist hell, die Schrift darüber braucht ein gedämpftes Foto (kein Verlauf) */
img[src*="ki-gedeck"]{filter:brightness(.58) saturate(.95)}
<style id="ki-stil">
/* «KI und Ihre Daten» (ki_seite.py, 16.10.2026, zweite Fassung): Bausteine der Werkbank (ag-blatt, mn-preise, zt, odo, wfen, data-a),
   eigene Teile nur für Raster, Auftakt, Karten und Zahlen. Bewegung nur über die data-a der Werkbank, nichts Eigenes animiert.
   Das Claude-Zeichen in seinem Ton (#d97757) ist der eine Farbpunkt der Seite. */
.ki{--claude:#d97757}
.ki-hz{display:block;width:clamp(56px,5.4vw,84px);height:auto;margin:0 auto;color:var(--gold)}
.ki-claude{display:block;width:clamp(44px,4.2vw,64px);height:auto;color:var(--claude)}
.ki-kopf{text-align:center;max-width:900px;margin:0 auto clamp(48px,5.6vw,96px)}
.ki-kopf .t2{margin-top:clamp(18px,2vw,28px)}
.ki-lauf{max-width:56ch;margin:clamp(18px,2vw,28px) auto 0;font-size:clamp(1.06rem,1.22vw,1.2rem);line-height:1.64;opacity:.86}
/* Auftakt */
.ki-auftakt{padding-top:clamp(130px,13vw,190px);padding-bottom:var(--abschnitt);text-align:center}
.ki-auftakt .in{display:block}
.ki-paar{display:flex;align-items:center;justify-content:center;gap:clamp(18px,2.2vw,34px)}
.ki-paar__hz{width:clamp(72px,7vw,108px)}   /* Robert 16.10.: nur das Zeichen des Hauses, mittig in Gold, ohne Claude-Zeichen */
.ki-paar__x{position:relative;display:block;width:clamp(20px,1.8vw,28px);height:clamp(20px,1.8vw,28px)}
.ki-paar__x::before,.ki-paar__x::after{content:"";position:absolute;left:50%;top:0;bottom:0;width:1px;background:rgba(236,220,180,.6);transform:rotate(45deg)}
.ki-paar__x::after{transform:rotate(-45deg)}
.ki-paar__n{display:flex;justify-content:center;gap:clamp(40px,5vw,80px);margin:18px 0 0;font:400 11px/1.3 var(--mono,'DM Mono',monospace);letter-spacing:.24em;text-transform:uppercase;color:rgba(236,220,180,.8)}
.ki-auftakt .t1{margin:clamp(34px,4vw,60px) 0 0;text-align:center}
.ki-auftakt .t1 .z,.ki-kopf .t2 .z,.ki-auftakt .t1 .z>span,.ki-kopf .t2 .z>span{margin-left:auto;margin-right:auto}
.ki-kopf .t2,.ki-auftakt .t1{text-align:center;margin-left:auto!important;margin-right:auto!important}
.ki-buehne{margin:clamp(48px,5.6vw,96px) auto 0;max-width:1240px;border-radius:clamp(22px,2.4vw,32px);overflow:hidden;box-shadow:0 60px 90px -50px rgba(0,0,0,.85),0 22px 40px -28px rgba(0,0,0,.6)}
.ki-buehne img{display:block;width:100%;height:auto;aspect-ratio:1620/1080;object-fit:cover}
/* Zahlen + Kosten */
.ki-zahlen{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:3px double rgba(210,191,152,.55);border-bottom:3px double rgba(210,191,152,.55);margin-bottom:clamp(56px,6vw,104px)}
.ki-zahl{padding:clamp(28px,3vw,48px) clamp(14px,1.6vw,26px);text-align:center}
.ki-zahl+.ki-zahl{border-left:1px solid rgba(210,191,152,.22)}
.ki-zahl__n{margin:0;font-family:var(--serif);font-weight:500;font-size:clamp(3.6rem,7vw,7.6rem);line-height:1.16;color:#ecdcb4}
.ki-zahl__t{margin:12px auto 0;max-width:22ch;line-height:1.55;color:rgba(255,255,255,.82)}
.ki-blick{display:grid;gap:clamp(28px,3.4vw,56px);grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);align-items:center}
.ki-blick__text p{font-family:var(--serif);font-size:clamp(1.1rem,1.3vw,1.3rem);line-height:1.55;margin:.7em 0 0;color:var(--tinte)}
/* Claude gross und mittig im freien Raum der linken Spalte (Robert 16.10.2026) */
.ki-blick{align-items:stretch!important}
.ki-blick__text{display:flex;flex-direction:column}
.ki-marke{flex:1;display:flex;align-items:center;justify-content:center;gap:clamp(14px,1.4vw,22px);min-height:clamp(120px,12vw,190px);margin-bottom:clamp(16px,1.8vw,24px)}
.ki-marke .ki-claude{width:clamp(56px,5vw,80px)}
.ki-marke span{font-family:var(--serif);font-weight:500;font-size:clamp(2.4rem,3.4vw,3.6rem);line-height:1;color:var(--tinte)}
.ki-preise{max-width:none;margin:0}
.ki-k__t{margin:0;font-family:var(--serif);font-weight:500;font-size:clamp(1.7rem,2.3vw,2.4rem);line-height:1.1;color:var(--tinte)}
/* Vier Stellen: Foto + Karte, abwechselnd; das Foto ist so hoch wie die Karte */
.ki-stellen{display:grid;gap:clamp(56px,6.4vw,112px)}
.ki-st{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);gap:clamp(24px,3vw,52px);align-items:stretch}
.ki-st--um .ki-st__b{order:2}
.ki-st__b{position:relative;margin:0;border-radius:clamp(22px,2.4vw,30px);overflow:hidden;box-shadow:0 50px 80px -48px rgba(0,0,0,.9),0 18px 34px -26px rgba(0,0,0,.6);min-height:420px}
.ki-st__b img{display:block;position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ki-kerbe{position:absolute;left:0;bottom:0;padding:18px 26px 2px 24px;background:var(--navy,#1b2033);border-top-right-radius:24px;font:400 14px/1 var(--mono,'DM Mono',monospace);letter-spacing:.18em;text-transform:uppercase;color:#ecdcb4}
.ki-kerbe::before,.ki-kerbe::after{content:"";position:absolute;width:24px;height:24px;background:radial-gradient(circle at 100% 0,transparent 23.5px,var(--navy,#1b2033) 24px)}
.ki-kerbe::before{left:0;top:-24px}
.ki-kerbe::after{right:-24px;bottom:0}
.ki-k{display:flex;flex-direction:column}
.ki-k dl{margin:clamp(14px,1.6vw,22px) 0 clamp(18px,2vw,26px)}
.ki-k__r{padding:14px 0;border-top:1px solid rgba(150,125,64,.22)}
.ki-k__r dt{font:400 11px/1.3 var(--caps,'Cinzel',Georgia,serif);letter-spacing:.22em;text-transform:uppercase;color:#967d40}
.ki-k__r dd{margin:6px 0 0;font-size:1rem;line-height:1.6;color:rgba(12,21,38,.86)}
.ki-k__ohne{margin-top:auto;padding:clamp(18px,2vw,26px);border-radius:18px;background:var(--navy,#1b2033);color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.12)}
.ki-k__ohne-t{margin:0;font:400 11px/1.3 var(--caps,'Cinzel',Georgia,serif);letter-spacing:.22em;text-transform:uppercase;color:#ecdcb4}
.ki-k__ohne p+p{margin:8px 0 0;font-family:var(--serif);font-size:clamp(1.08rem,1.25vw,1.24rem);line-height:1.5;color:rgba(255,255,255,.92)}
/* Fenster: Satz mit kräftigem Schatten, damit er auf jedem Foto lesbar bleibt (Robert 16.10.2026) */
#ki-fenster .wfen__t,#ki-fenster .wfen__k{text-shadow:0 1px 2px rgba(3,10,16,.95),0 3px 14px rgba(3,10,16,.85),0 10px 46px rgba(3,10,16,.75)}
/* Robert 18.10.2026: sanfte Abdunklung hinter dem Textblock, ohne Kante; Fenster bleibt */
#ki-fenster .wfen__in::before{content:"";position:absolute;left:50%;top:50%;width:min(1100px,130%);height:170%;transform:translate(-50%,-50%);z-index:-1;pointer-events:none;background:radial-gradient(closest-side,rgba(3,10,16,.6),rgba(3,10,16,.4) 52%,rgba(3,10,16,.12) 80%,rgba(3,10,16,0))}
/* Geräte mit Film (Robert 16.10.2026): ein Gerät je Abschnitt, frei auf dem Grund, mittig zur Karte */
.ki-k__preis{margin:8px 0 0;font:400 13px/1.3 var(--mono,'DM Mono',monospace);letter-spacing:.16em;text-transform:uppercase;color:#967d40}
.ki-geraet{margin:0;display:flex;align-items:center;justify-content:center}
.ki-st--um .ki-geraet{order:2}
.ki-film{display:block;width:100%;height:100%;object-fit:cover;background:#0c0e16}
.ki-laptop{position:relative;width:100%;aspect-ratio:2000/1673;filter:drop-shadow(0 46px 50px rgba(0,0,0,.55))}
.ki-laptop__s{position:absolute;left:9.7242%;top:2.0296%;width:80.5516%;height:62.3256%;overflow:hidden;background:#0c0e16}
.ki-laptop__g{position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none}
.ki-handy{position:relative;width:min(300px,62%);aspect-ratio:540/1168;padding:11px;border-radius:52px;background:linear-gradient(160deg,#3a4262,#11141f 55%,#1b2033);
  box-shadow:inset 0 0 0 1.5px rgba(236,220,180,.28),inset 0 0 0 5px #0a0c13,0 50px 70px -36px rgba(0,0,0,.85)}
.ki-handy__s{width:100%;height:100%;border-radius:42px;overflow:hidden;background:#0c0e16}
.ki-ipad{position:relative;width:100%;aspect-ratio:1180/820;padding:clamp(12px,1.4vw,20px);border-radius:clamp(26px,2.6vw,38px);background:linear-gradient(160deg,#3a4262,#11141f 55%,#1b2033);
  box-shadow:inset 0 0 0 1.5px rgba(236,220,180,.28),inset 0 0 0 6px #0a0c13,0 50px 70px -40px rgba(0,0,0,.85)}
.ki-ipad__s{width:100%;height:100%;border-radius:clamp(12px,1.2vw,18px);overflow:hidden;background:#0c0e16}
/* Daten */
/* Daten, edler (Robert 16.10.2026: «noch geiler und edler»): Anbieter als Platte, sechs Zusagen als helle Blätter mit Doppelrand und Siegel */
.ki-anbieter{display:flex;align-items:center;justify-content:center;gap:clamp(16px,1.6vw,24px);width:max-content;max-width:100%;margin:0 auto clamp(44px,5vw,80px);padding:clamp(16px,1.6vw,22px) clamp(26px,2.6vw,40px);
  border-radius:999px;background:#fbf6ea;box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(150,125,64,.45),0 0 0 6px rgba(251,246,234,.7),0 0 0 7px rgba(150,125,64,.25),0 30px 50px -36px rgba(60,44,20,.6)}
.ki-anbieter .ki-claude{width:clamp(46px,4vw,60px)}
.ki-anbieter p{margin:0;display:flex;flex-direction:column;text-align:left}
.ki-anbieter b{font-family:var(--serif);font-weight:500;font-size:1.5rem;color:var(--tinte)}
.ki-anbieter span{font-size:.9rem;opacity:.72}
.ki-daten{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(18px,2vw,30px)}
.ki-d{position:relative;text-align:center;padding:clamp(34px,3.4vw,52px) clamp(24px,2.4vw,38px) clamp(30px,3vw,44px);border-radius:clamp(22px,2.2vw,30px);
  background:#fbf6ea;box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(150,125,64,.5),0 50px 70px -52px rgba(60,44,20,.7),0 18px 30px -26px rgba(60,44,20,.45)}
.ki-d::before,.ki-d::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(150,125,64,.45);border-radius:clamp(15px,1.5vw,22px);inset:10px}
.ki-d::after{inset:14px;border-color:rgba(150,125,64,.2);border-radius:clamp(12px,1.2vw,19px)}
.ki-siegel{display:grid;place-items:center;width:58px;height:58px;margin:0 auto;border-radius:50%;background:radial-gradient(circle at 35% 30%,#f3e6c4,#d2bf98 55%,#a8894c);box-shadow:inset 0 0 0 1px rgba(255,255,255,.55),inset 0 0 0 5px rgba(150,125,64,.35),0 10px 18px -10px rgba(60,44,20,.7)}
.ki-siegel i{width:12px;height:12px;transform:rotate(45deg);background:#1b2033}
.ki-d h3{margin:20px 0 0;font-family:var(--serif);font-weight:500;font-size:clamp(1.5rem,1.95vw,2rem);line-height:1.15;color:var(--tinte)}
.ki-d p{margin:12px auto 0;line-height:1.62;max-width:34ch;color:rgba(12,21,38,.84)}
.ki-raute{display:block;width:10px;height:10px;transform:rotate(45deg);background:var(--gold)}
/* Ohne KI */
.ki-ohne{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(18px,2vw,30px)}
.ki-o{padding:clamp(22px,2.4vw,32px);border-radius:clamp(20px,2vw,26px);background:#fbf6ea;box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(150,125,64,.35),0 34px 50px -40px rgba(60,44,20,.55)}
.ki-o h3{margin:0;font-family:var(--serif);font-weight:500;font-size:clamp(1.4rem,1.7vw,1.75rem);color:var(--tinte)}
.ki-o p{margin:12px 0 0;line-height:1.62;color:rgba(12,21,38,.86)}
/* In Ihrer Hand */
.ki-hand{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(28px,3.6vw,64px);align-items:center;margin-bottom:clamp(56px,6vw,104px)}
.ki-hand__b{margin:0;border-radius:clamp(22px,2.4vw,30px);overflow:hidden;box-shadow:0 50px 80px -48px rgba(0,0,0,.9)}
.ki-hand__b img{display:block;width:100%;height:auto}
.ki-hand__t .ki-hz{margin:0}
.ki-hand__t .t2{margin:clamp(16px,1.8vw,24px) 0 clamp(20px,2.4vw,34px)}
.ki-h{margin:0;padding:16px 0;border-top:1px solid rgba(210,191,152,.25);font-size:1.05rem;line-height:1.6;color:rgba(255,255,255,.82)}
.ki-h b{display:block;font-family:var(--serif);font-weight:500;font-size:1.45rem;color:#ecdcb4;margin-bottom:4px}
/* Robert 18.10.2026: «Sie entscheiden» ohne das Foto der Familie; die Punkte als ruhige Kacheln nebeneinander unter dem Titel */
.ki-hand--ohne-bild{display:block}
.ki-hand--ohne-bild .ki-hand__t{text-align:center;max-width:760px;margin:0 auto}
.ki-hand--ohne-bild .ki-hand__t .ki-hz{display:inline-block}
.ki-hand--ohne-bild .ki-hand__t .t2,.ki-hand--ohne-bild .ki-hand__t .t2 .z{text-align:center;justify-content:center;margin-left:auto;margin-right:auto}
.ki-hand__k{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:clamp(14px,1.6vw,22px);margin-top:clamp(8px,1vw,14px)}
.ki-hand--ohne-bild .ki-h{padding:clamp(20px,2vw,28px);border:0;border-radius:20px;background:rgba(255,255,255,.04);box-shadow:inset 0 0 0 1px rgba(210,191,152,.28),inset 0 1px 0 rgba(255,255,255,.06)}
.ki-hand--ohne-bild .ki-h b{margin-bottom:10px;padding-bottom:12px;border-bottom:1px solid rgba(210,191,152,.25)}
.ki-offen{max-width:880px;margin:0 auto;text-align:center}
.ki-offen>p{font-family:var(--serif);font-size:clamp(1.08rem,1.25vw,1.25rem);line-height:1.55;max-width:58ch;margin:14px auto 0;color:var(--tinte)}
.ki-knoepfe{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;margin-top:clamp(22px,2.4vw,34px)!important}
.ki-quellen{font-size:.82rem!important;font-family:inherit!important;opacity:.72;margin-top:clamp(24px,2.6vw,36px)!important}
.ki-quellen__l{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px 18px;justify-content:center;font-size:.82rem}
.ki-quellen__l a{color:#7d6630}
@media(max-width:1000px){.ki-blick,.ki-st,.ki-hand{grid-template-columns:1fr}.ki-st--um .ki-st__b,.ki-st--um .ki-geraet{order:0}.ki-st__b{min-height:0;aspect-ratio:4/3}
  .ki-zahlen{grid-template-columns:repeat(2,minmax(0,1fr))}.ki-zahl:nth-child(3){border-left:0}.ki-zahl:nth-child(n+3){border-top:1px solid rgba(210,191,152,.22)}
  .ki-daten{grid-template-columns:repeat(2,minmax(0,1fr))}.ki-ohne{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:600px){.ki-daten,.ki-ohne{grid-template-columns:1fr}.ki-paar__n{flex-direction:column;gap:6px}.ki-zahl__n{font-size:3.4rem}}
</style>'''


NAV = ('<nav aria-label="Abschnitte"><a href="#ki-blick">KI</a><a href="#ki-zahlen">Abrechnung</a><a href="#ki-stellen">Vier Stellen</a><a href="#ki-daten">Ihre Daten</a>'
       '<a href="#ki-ohne">Ohne KI</a><a href="#ki-hand">In Ihrer Hand</a><a href="index.html#k8">Zurück zum Angebot</a></nav>')


def bau(faerbe):
    """Rahmen (Kopf, Leiste, Laufband, Fuss, Skripte) aus der gebauten werkbank/index.html, Inhalt von hier. faerbe = K.faerbe (Farben der Vorlage aufs Haus)."""
    idx = os.path.join(ROOT, 'werkbank', 'index.html')
    t = open(idx, encoding='utf-8').read()
    m0, m1 = t.find('<main id="oben">'), t.find('</main>')
    if m0 < 0 or m1 < 0:
        raise SystemExit('ki.html: <main> der Werkbank nicht gefunden')
    gr = dict(bilder())
    kopf = t[:m0]
    kopf = re.sub(r'<title>.*?</title>', '<title>KI und Ihre Daten · Landgasthof Ruedihus</title>', kopf, count=1, flags=re.S)
    kopf = re.sub(r'<nav aria-label="Kapitel">.*?</nav>', NAV, kopf, count=1, flags=re.S)
    kopf = kopf.replace('href="#oben">', 'href="index.html">', 1)
    kopf = kopf.replace('</head>', faerbe(CSS) + '\n</head>', 1)
    seite = kopf + '<main id="oben">' + hauptteil(gr) + FILM_JS + t[m1:]
    ziel = os.path.join(ROOT, 'werkbank', 'ki.html')
    tmp = ziel + f'.{os.getpid()}.tmp'
    open(tmp, 'w', encoding='utf-8').write(seite)
    os.replace(tmp, ziel)
    return ziel
