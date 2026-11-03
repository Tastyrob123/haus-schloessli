#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli, Kapitel VIII «Das Angebot» (Neufassung 20.10.2026 nach dem Vorbild des Grand Beau-Rivage).

Robert 20.10.2026 zum alten Platzhalter «Der Vorschlag folgt.»: «Warum ist nicht alles so wie beim Rivage? … also jetzt nicht alles genauso,
aber halt auch das Ziel angepasst … dass unten auch noch das Angebot ist, dieser ganzen KI-Sache, dieser KI-Seite. Da sagen wir meinetwegen
200 Franken im Monat Betreuung.» Vorbild: angebot_ebene.py des Rivage (nur gelesen, Aufbau übernommen, Inhalt und Kleid eigen):
Register → Zusammenfassung → Was dazugehört (steht / läuft / braucht Sie / Idee) → Wie es gebaut ist + Ihre Daten → Woche für Woche →
Karte «Ein Vorschlag.» (Eigentum, Preis, Betreuung, Wo die KI arbeitet, Link zur Seite «KI und Ihre Daten», PDF).

Nur Belegtes: Zahlen gezählt aus dem gebauten Stand (wb_kapitel.zaehle, papier_plan.json, unterlagen.json, feed.json, Bildarchiv /api/stand),
Systeme des Hauses aus der heutigen Website (gastronovi für Tische, zenchef für Gutscheine), KI-Stellen aus dem Code der Werkzeuge
(reception/gast/gast.py, imprimerie/api/entwurf.py, livre/livre.py). Betreuung CHF 200 im Monat: Robert 20.10.2026 (eingetragen in Angebot.md).
Der Bau: «Den Betrag nennen Sie» wie beim Rivage. Kosten der KI je Aufruf sind für das Schlössli nicht gemessen und stehen deshalb nicht da."""
import html, json, os, urllib.request

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)

BETREUUNG = '200'   # CHF im Monat, Robert 20.10.2026
DATUM = 'Hamburg, 20. Oktober 2026'
PDF_NAME = 'vorschlag-wirtschaft-am-schloessli.pdf'
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
ORN = '<div class="sag-orn" aria-hidden="true"><i></i><b></b><i></i></div>'


def _j(p, leer):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return leer


def _fotos():
    try:
        return json.load(urllib.request.urlopen('http://127.0.0.1:9049/_werkzeuge/livre/api/stand', timeout=4)).get('fotos')
    except Exception:
        return None


def zahlen(z):
    p = _j(os.path.join(W, 'papier_plan.json'), {'druck': [], 'etiketten': []})
    u = _j(os.path.join(W, 'unterlagen.json'), [])
    feed = len(_j(os.path.join(ROOT, 'feed', 'feed.json'), {'posts': []})['posts'])
    return dict(seiten=z['seiten'], karten=len(u), druck=len(p['druck']), unter=len(p['etiketten']), mails=z.get('mails', 0), feed=feed, fotos=_fotos())


ZAHLWORT = {3: 'drei', 4: 'vier', 5: 'fünf', 6: 'sechs', 7: 'sieben', 8: 'acht', 9: 'neun', 10: 'zehn', 11: 'elf', 12: 'zwölf'}
wort = lambda n: ZAHLWORT.get(n, str(n))


def inhalt(z):
    Z = zahlen(z)
    zus = [f'Für die Wirtschaft am Schlössli habe ich einen ganzen Auftritt gebaut: die Website mit {wort(Z["seiten"])} Seiten, sieben Werkzeuge, mit denen Ihr Team sie selbst pflegt, '
           f'{wort(Z["karten"])} Karten neu gesetzt, {wort(Z["druck"])} Drucksachen, {wort(Z["unter"])} Untersetzer für die Lästermeile, {wort(Z["mails"])} Mails und {Z["feed"]} Beiträge für Instagram. Alles davon können Sie hier anklicken.',
           'Gebaut ist es. Was fehlt, liegt bei Ihnen: die Zugänge zu Domain und Mail, der Entscheid zu den Fotos und das Gegenlesen von Karten und Preisen. Sechs Wochen nach dem Start läuft die Seite unter schloessli-bottighofen.ch.',
           f'Den Betrag für den Bau nennen Sie. Danach kümmere ich mich um Seite, Werkzeuge und KI, für CHF {BETREUUNG} im Monat, monatlich kündbar.']
    steht = [f'{wort(Z["seiten"]).capitalize()} Seiten und das Rechtliche', 'Die Karte nach Ländern, Lunch, Lästermeile, Wein und Bankett, je als PDF',
             'Reservation und Gutschein auf jeder Seite', f'{wort(Z["druck"]).capitalize()} Drucksachen, {wort(Z["unter"])} Untersetzer', f'{wort(Z["mails"]).capitalize()} Mails an Ihre Gäste',
             f'{Z["feed"]} Beiträge für Instagram'] + ([f'Das Bildarchiv mit {Z["fotos"]} Fotos'] if Z['fotos'] else [])
    import rh_werkzeuge as WK
    laeuft = [w[1] for w in WK.WERKZEUGE]
    umfang = [('Steht, zum Anklicken', steht), ('Läuft im Entwurf, zieht mit um', laeuft),
              ('Braucht etwas von Ihnen', ['Zugänge zu Domain und Mail', 'Der Entscheid zu den Fotos', 'Gegenlesen von Karten und Preisen', 'Freigabe der Rechtstexte']),
              ('Eine Idee, noch nicht gebaut', ['Der Chat direkt auf der Website', 'Englisch und Französisch für die Gäste vom See'])]
    return zus, umfang


AUFBAU = ['Fertige Seiten, kein Programm dazwischen: schnell und robust.', 'Jedes Werkzeug ein eigener Dienst mit eigenem Zugang.',
          'Tische und Gutscheine bleiben bei gastronovi und zenchef.', 'Eine Karte, ein Eintrag: Website, PDF und Tafel zugleich.', 'Jede frühere Fassung bleibt.']
DATEN = ['Keine Cookies, kein Verfolgen.', 'Der Chat antwortet nur aus Ihren Seiten und Karten.', 'Keine Karten- oder Zahlungsdaten im Chat.',
         'Ein Passwort je Person, ab dem Umzug.', 'Für Suchmaschinen gesperrt, bis zum Umzug.']

WOCHEN = [  # Titel, Ich, Ihr Haus, Dabei (Roberts Vorschlag nach dem Vorbild Rivage, auf ein Restaurant mit einem Gastgeber gekürzt)
    ('Zugänge und Gespräch', 'Gespräch mit Ihnen und Monika Huber, dazu die Liste der Zugänge.', 'Zugänge zu Domain und Mail, die Wege zu gastronovi und zenchef.', 'Christian Kuchler, Küche'),
    ('Lesen und berichtigen', 'Jede Korrektur am selben Tag.', 'Küche und Service lesen Karten, Preise und Seiten gegen.', 'Küche, Service'),
    ('Anbindungen und Fotos', 'Mailversand, Chat und jedes Werkzeug mit Passwort; freigegebene Fotos einarbeiten.', 'Der Entscheid zu den Fotos.', 'Christian Kuchler, Fotografen'),
    ('Runde im Haus', 'Gemeinsam durch jede Seite und jedes Werkzeug; die zweite Fassung bis Ende der Woche.', 'Küche und Service sehen durch.', 'Christian Kuchler, Küche, Service'),
    ('Schulung und Umzug vorbereiten', 'Eine Stunde je Werkzeug; Rechtstexte, Weiterleitungen, Google.', 'Zeit für die Runden, Freigabe der Rechtstexte.', 'Küche, Service'),
    ('Umzug', 'Die Seite geht unter schloessli-bottighofen.ch online; zwei Wochen täglich hinsehen.', 'Ihre Freigabe.', 'Christian Kuchler')]
WOCHEN_SATZ = 'So stelle ich mir die sechs Wochen vor. Das Tempo bestimmt Ihr Haus; was in einer Woche nicht fertig wird, rückt, ohne dass etwas anderes wackelt.'

EIGENTUM = ['Website, Code, Karten, Drucksachen, Beiträge und Bildarchiv gehören Ihrem Haus.', 'Domain, Server und alle Zugänge laufen auf Ihren Namen.',
            'Die Fotos bleiben bei Ihnen und Ihren Fotografen.', 'Sollten wir einmal getrennte Wege gehen, nehmen Sie alles mit.']
PREIS = [
    ('Der Bau', 'Den Betrag nennen Sie', 'Sie nennen den Betrag, bei dem Sie sich wohlfühlen.'),
    ('Betreuung', f'CHF {BETREUUNG} im Monat', ['Server, Domain, Sicherungen, Aktualisierungen, Sicherheit und Datenschutz.',
        'Die sieben Werkzeuge laufen, Fehler behebe ich ohne Rechnung, ein Ausfall hat Vorrang.',
        'Die KI kennt Ihre neuen Karten, Zeiten und Preise: ich halte ihr Wissen aktuell.',
        'Antwort spätestens am nächsten Werktag. Ihr Team pflegt die Inhalte selbst.']),
    ('Wünsche darüber hinaus', 'Angebot vorher', 'Ein weiterer Bereich oder eine neue Funktion: dafür mache ich Ihnen gern vorher ein Angebot.')]
PREIS_FUSS = 'Monatlich kündbar, Beträge netto.'
DANACH = ['Bis zum Umzug passen wir an, bis es stimmt.', 'Druckerei und Fotografen bleiben Ihre Rechnungen, ebenso die Gebühren von gastronovi und zenchef.']
KI_SATZ = 'Vier Stellen nutzen ein Sprachmodell. Es läuft über ein eigenes Konto Ihres Hauses beim Anbieter: Sie zahlen dort direkt nach Verbrauch, ich richte das Konto ein und setze eine Obergrenze je Monat. Jede Stelle läuft auch ohne KI weiter.'
KI = [  # Titel, Werkzeug, Satz (aus dem Code der Werkzeuge)
    ('Der Chat für Ihre Gäste', 'Reservationsbuch', 'Antwortet aus Ihren Seiten und Karten, auch spät am Abend. Im Entwurf steht er im Reservationsbuch zum Ausprobieren.'),
    ('Antwort auf eine Anfrage', 'Reservationsbuch', 'Aus der Mail des Gastes wird ein Entwurf im Ton des Hauses. Verschickt wird erst, wenn jemand vom Team gelesen hat.'),
    ('Fünf Entwürfe', 'Hausdruckerei', 'Ein Satz genügt für fünf Entwürfe im Stil des Hauses. Ohne KI nimmt sie die passendste fertige Vorlage.'),
    ('Eine Markenprüfung', 'Bildarchiv', 'Prüft einen fremden Entwurf gegen Farben, Zeichen und Schrift des Hauses. Gespeichert wird nichts.')]


def bilder(webp, haus):
    webp(haus('haus-2400'), 'sag-haus', 1400, 80, 1.18, (.42, .5))


def angebot(k):
    bild, kopfk = k['bild'], k['kopfk']
    zus, umfang = inhalt(k['z'])
    reg = ''.join(f'<a href="#sag-{a}"><span>{n:02d}</span>{e(t)}</a>' for n, (a, t) in enumerate(
        (('kurz', 'Zusammenfassung'), ('umfang', 'Umfang'), ('aufbau', 'Aufbau'), ('wochen', 'Woche für Woche'), ('vorschlag', 'Ein Vorschlag')), 1))
    h = lambda n, t: f'<h3 class="sag-h"><span>{n}</span>{e(t)}</h3>'
    liste = lambda pp: '<ul class="sag-l">' + ''.join(f'<li>{e(p)}</li>' for p in pp) + '</ul>'
    spalten = ''.join(f'<div class="sag-sp sag-sp--{i + 1}"><h4>{e(t)}</h4><ul>' + ''.join(f'<li>{e(p)}</li>' for p in pp) + '</ul></div>' for i, (t, pp) in enumerate(umfang))
    wochen = ''.join(f'<article class="sag-w" data-a="auf" style="--i:{i % 3}"><p class="sag-w__n"><b>{i + 1:02d}</b><small>Woche {i + 1}</small></p><h4>{e(t)}</h4>'
                     f'<div class="sag-w__r"><span>Ich</span><p>{e(ich)}</p></div><div class="sag-w__r"><span>Ihr Haus</span><p>{e(haus)}</p></div>'
                     f'<div class="sag-w__r sag-w__r--wer"><span>Dabei</span><p>{e(wer)}</p></div></article>' for i, (t, ich, haus, wer) in enumerate(WOCHEN))
    return f'''
<section class="fl fl--nacht tapete-leicht blatt sag" id="k8">
  <div class="in">
    {kopfk('k8', ['Was Sie', 'bekommen.'], 'Alles, was ein Entscheid braucht, auf einem Blatt, und am Schluss der Vorschlag.')}
    <nav class="sag-reg" data-a="auf" aria-label="Auf diesem Blatt">{reg}</nav>
    <div class="sag-blatt sag-kurz" id="sag-kurz" data-a="heben">
      <figure class="sag-bild">{bild('sag-haus', 'Die Wirtschaft am Schlössli am Bootshafen von Bottighofen')}</figure>
      <div class="sag-text">{h('01', 'Zusammenfassung')}{''.join(f'<p>{e(p)}</p>' for p in zus)}</div>
    </div>
    <div class="sag-blatt sag-umf" id="sag-umfang" data-a="heben">{h('02', 'Was dazugehört')}<div class="sag-spalten">{spalten}</div></div>
    <div class="sag-blatt sag-zwei" id="sag-aufbau" data-a="heben">
      <div>{h('03', 'Wie es gebaut ist')}{liste(AUFBAU)}</div>
      <div>{h('04', 'Ihre Daten und die Ihrer Gäste')}{liste(DATEN)}</div>
    </div>
    <div class="sag-teil" id="sag-wochen">
      <p class="sag-k">05 · Woche für Woche</p>
      <div class="sag-wochen">{wochen}</div>
      <p class="sag-satz">{e(WOCHEN_SATZ)}</p>
    </div>
    <div class="sag-buehne" id="sag-vorschlag">{karte_html()}</div>
  </div>
</section>'''


def karte_html():
    zeilen = lambda pp: '<ul class="mn-l">' + ''.join(f'<li>{e(p)}</li>' for p in pp) + '</ul>'
    gang = lambda n, t: f'<p class="mn-gang"><span>{n}</span>{e(t)}</p>'
    preis = ''
    for t, r, s in PREIS:
        unten = ('<ul class="mn-p__l">' + ''.join(f'<li>{e(x)}</li>' for x in s) + '</ul>') if isinstance(s, list) else f'<p class="mn-p__s">{e(s)}</p>'
        preis += f'<li class="mn-p"><p class="mn-p__z"><b>{e(t)}</b><i></i><span>{e(r)}</span></p>{unten}</li>'
    ki = ''.join(f'<li class="mn-p"><p class="mn-p__z"><b>{e(t)}</b><i></i><span>{e(w)}</span></p><p class="mn-p__s">{e(s)}</p></li>' for t, w, s in KI)
    return f'''<article class="mn" data-a="heben">
        <header class="mn-kopf">
          <img class="mn-zeichen" src="../assets/svg/zeichen.svg" alt="" width="72" height="72">
          <p class="mn-haus">Wirtschaft am Schlössli · Bottighofen</p>
          <h3 class="mn-titel">Ein Vorschlag.</h3>
          <p class="mn-unter">Eigentum, Preis und Betreuung, so wie ich es mir vorstelle. Über alles davon sprechen wir gern gemeinsam.</p>
        </header>
        {ORN}{gang('I', 'Was Ihnen gehört')}{zeilen(EIGENTUM)}
        {ORN}{gang('II', 'Der Preis')}<ul class="mn-l mn-preise">{preis}</ul><p class="mn-fuss">{e(PREIS_FUSS)}</p>
        {ORN}{gang('III', 'Laufende Betreuung')}{zeilen(DANACH)}
        {ORN}{gang('IV', 'Wo die KI arbeitet')}{zeilen([KI_SATZ])}<ul class="mn-l mn-preise">{ki}</ul>
        <p class="mn-ki"><a class="kn kn--klein" href="ki.html">Mehr zu KI und Ihren Daten<i>{PF}</i></a></p>
        <footer class="mn-ende"><i></i><span>{e(DATUM)}</span><i></i></footer>
        <p class="mn-pdf"><a class="kn kn--klein" href="{PDF_NAME}" download>Als PDF speichern<i>{PF}</i></a></p>
      </article>'''


CSS = '''
/* ---------- Kapitel VIII «Das Angebot» (sb_angebot.py, 20.10.2026, Aufbau nach dem Rivage, Kleid des Schlössli): helle Blätter auf der Nacht ---------- */
.sag .kopfzeile{margin-bottom:clamp(30px,3.4vw,54px)}
.sag-reg{display:flex;flex-wrap:wrap;gap:8px clamp(18px,2.6vw,44px);justify-content:center;margin:0 auto clamp(40px,4.6vw,72px);padding-bottom:18px;border-bottom:1px solid rgba(162,182,207,.28)}
.sag-reg a{display:inline-flex;align-items:baseline;gap:9px;font:400 12.5px/1.2 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:var(--creme);text-decoration:none;opacity:.82;transition:opacity .4s}
.sag-reg a span{font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--messing)}
.sag-reg a:hover{opacity:1}
.sag-blatt{position:relative;margin-top:clamp(36px,4vw,64px);padding:clamp(28px,3.8vw,64px);border-radius:clamp(22px,2.4vw,34px);background:var(--weiss);color:var(--tinte);
  box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(17,61,136,.22),0 70px 90px -56px rgba(0,0,0,.9),0 26px 40px -30px rgba(0,0,0,.6)}
.sag-blatt::before{content:"";position:absolute;pointer-events:none;inset:clamp(10px,1.1vw,16px);border:1px solid rgba(17,61,136,.2);border-radius:clamp(14px,1.6vw,24px)}
.sag-reg+.sag-blatt{margin-top:0}
.sag-h{display:flex;align-items:baseline;gap:16px;margin:0 0 clamp(18px,2vw,28px);font-family:var(--serif);font-weight:400;font-size:clamp(1.7rem,2.4vw,2.5rem);line-height:1.1;letter-spacing:.06em;text-transform:uppercase;color:var(--tinte)}
.sag-h span{font-family:var(--mono);font-size:clamp(.78rem,.9vw,.92rem);letter-spacing:.16em;color:var(--blau)}
.sag-kurz{display:grid;gap:clamp(26px,3.6vw,64px);align-items:center}
@media(min-width:900px){.sag-kurz{grid-template-columns:minmax(0,.84fr) minmax(0,1.16fr)}}
.sag-bild{margin:0;border-radius:clamp(14px,1.5vw,22px);overflow:hidden;aspect-ratio:1.18;background:var(--creme)}
.sag-bild img{display:block;width:100%;height:100%;object-fit:cover}
.sag-text p{margin:0;font-size:clamp(1.08rem,1.24vw,1.28rem);line-height:1.6;color:rgba(4,16,35,.84)}
.sag-text p+p{margin-top:1em}
.sag-text h3+p{font-size:clamp(1.24rem,1.5vw,1.5rem);line-height:1.45;color:var(--tinte)}
.sag-spalten{display:grid}
.sag-sp{padding:clamp(18px,2vw,30px) 0}
.sag-sp+.sag-sp{border-top:1px solid rgba(17,61,136,.2)}
.sag-sp h4{margin:0 0 8px;font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,1.8vw,1.9rem);line-height:1.15;color:var(--tinte)}
.sag-sp ul,.sag-l{list-style:none;margin:0;padding:0}
.sag-sp li{padding:11px 0;border-top:1px solid rgba(17,61,136,.12);font-size:clamp(1.06rem,1.2vw,1.24rem);line-height:1.4;color:rgba(4,16,35,.88)}
.sag-sp li:first-child{border-top:0}
@media(min-width:760px){
  .sag-spalten{grid-template-columns:repeat(2,minmax(0,1fr))}
  .sag-sp--1,.sag-sp--4{grid-column:1/-1}
  .sag-sp--1 ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:clamp(22px,2.6vw,44px)}
  .sag-sp--1 li:nth-child(-n+2){border-top:0}
  .sag-sp--2{padding-inline-end:clamp(22px,2.6vw,44px)}
  .sag-sp--3{padding-inline-start:clamp(22px,2.6vw,44px);border-inline-start:1px solid rgba(17,61,136,.2)}
  .sag-sp--4 ul{display:flex;flex-wrap:wrap;gap:0 clamp(18px,2vw,34px)}
  .sag-sp--4 li{border-top:0;display:flex;align-items:center;gap:clamp(18px,2vw,34px)}
  .sag-sp--4 li+li::before{content:"";width:7px;height:7px;border:1px solid var(--blau);transform:rotate(45deg);flex:none}
}
.sag-zwei{display:grid;gap:clamp(36px,4vw,64px)}
@media(min-width:900px){.sag-zwei{grid-template-columns:repeat(2,minmax(0,1fr))}}
.sag-l li{position:relative;padding:14px 0 14px 30px;border-top:1px solid rgba(17,61,136,.12);font-size:clamp(1.08rem,1.24vw,1.3rem);line-height:1.45;color:rgba(4,16,35,.88)}
.sag-l li:first-child{border-top:0;padding-top:0}
.sag-l li::before{content:"";position:absolute;left:3px;top:1.05em;width:7px;height:7px;border:1px solid var(--blau);transform:rotate(45deg)}
.sag-l li:first-child::before{top:.5em}
.sag-teil{margin-top:clamp(56px,6vw,100px)}
.sag-k{margin:0 0 clamp(18px,2vw,28px);text-align:center;font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--messing)}
.sag-wochen{display:grid;gap:clamp(16px,1.8vw,26px)}
@media(min-width:700px){.sag-wochen{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(min-width:1100px){.sag-wochen{grid-template-columns:repeat(3,minmax(0,1fr))}}
.sag-w{display:flex;flex-direction:column;padding:clamp(22px,2.2vw,32px);border-radius:24px;background:var(--weiss);color:var(--tinte);box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(17,61,136,.2),0 40px 50px -36px rgba(0,0,0,.9)}
.sag-w__n{display:flex;align-items:baseline;gap:12px;margin:0 0 8px}
.sag-w__n b{font-family:var(--serif);font-weight:400;font-size:clamp(2.2rem,2.6vw,2.8rem);line-height:.9;color:var(--blau)}
.sag-w__n small{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:rgba(4,16,35,.5)}
.sag-w h4{margin:0 0 14px;font-family:var(--serif);font-weight:400;font-size:clamp(1.3rem,1.5vw,1.6rem);line-height:1.15}
.sag-w__r{padding:10px 0;border-top:1px solid rgba(17,61,136,.18)}
.sag-w__r span{display:block;margin-bottom:3px;font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--blau)}
.sag-w__r p{margin:0;font-size:clamp(1rem,1.06vw,1.1rem);line-height:1.5;color:rgba(4,16,35,.86)}
.sag-w__r--wer{margin-top:auto}
.sag-satz{margin:clamp(22px,2.4vw,34px) auto 0;max-width:62ch;text-align:center;font-size:clamp(1.06rem,1.24vw,1.28rem);line-height:1.55;color:rgba(255,255,255,.86)}
.sag-buehne{display:flex;justify-content:center;margin-top:clamp(56px,6vw,100px)}
.mn{position:relative;width:min(100%,880px);padding:clamp(34px,5vw,80px) clamp(22px,5.4vw,92px) clamp(30px,4vw,60px);text-align:center;color:var(--tinte);background:var(--weiss);border-radius:6px;
  box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(17,61,136,.3),0 90px 110px -60px rgba(0,0,0,.95),0 30px 50px -30px rgba(0,0,0,.7)}
.mn::before,.mn::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(17,61,136,.34);inset:clamp(10px,1.2vw,18px)}
.mn::after{inset:clamp(14px,1.6vw,24px);border-color:rgba(17,61,136,.14)}
.mn-zeichen{display:block;width:clamp(56px,5.4vw,80px);height:auto;margin:0 auto clamp(14px,1.6vw,22px)}
.mn-haus{margin:0;font:400 clamp(11px,.9vw,13px)/1.3 var(--serif);letter-spacing:.3em;text-transform:uppercase;color:var(--blau)}
.mn-titel{margin:clamp(14px,1.4vw,20px) 0 0;font-family:var(--serif);font-weight:400;font-size:clamp(2.4rem,4.2vw,4.2rem);line-height:1;letter-spacing:.06em;text-transform:uppercase;color:var(--tinte)}
.mn-unter{margin:clamp(12px,1.2vw,16px) auto 0;max-width:46ch;font-size:clamp(1.04rem,1.16vw,1.2rem);line-height:1.5;color:rgba(4,16,35,.66)}
.sag-orn{display:flex;align-items:center;justify-content:center;gap:14px;margin:clamp(26px,3vw,44px) auto clamp(20px,2.2vw,32px);max-width:420px}
.sag-orn i{flex:1;height:1px;background:rgba(17,61,136,.35)}
.sag-orn b{width:8px;height:8px;transform:rotate(45deg);border:1px solid var(--blau)}
.mn-gang{margin:0 0 clamp(14px,1.6vw,22px);font-family:var(--serif);font-weight:400;font-size:clamp(1.5rem,2.1vw,2.1rem);line-height:1.1;color:var(--tinte)}
.mn-gang span{display:block;margin-bottom:8px;font:400 11px/1 var(--mono);letter-spacing:.3em;color:var(--blau)}
.mn-l{list-style:none;margin:0 auto;padding:0;max-width:62ch}
.mn-l li{padding:8px 0;font-size:clamp(1.04rem,1.16vw,1.2rem);line-height:1.55;color:rgba(4,16,35,.88)}
.mn-preise{max-width:620px;text-align:left}
.mn-p{padding:clamp(12px,1.2vw,16px) 0!important}
.mn-p+.mn-p{border-top:1px solid rgba(17,61,136,.16)}
.mn-p__z{display:flex;align-items:baseline;gap:10px;margin:0}
.mn-p__z b{flex:none;font-family:var(--serif);font-weight:500;font-size:clamp(1.1rem,1.26vw,1.3rem);color:var(--tinte)}
.mn-p__z i{flex:1;border-bottom:1px dotted rgba(17,61,136,.6);transform:translateY(-.3em)}
.mn-p__z span{flex:none;font-size:clamp(1.04rem,1.16vw,1.2rem);color:var(--blau);white-space:nowrap}
.mn-p__l{list-style:none;margin:6px 0 0;padding:0}.mn-p__l li{padding:2px 0 2px 1.1em!important;position:relative;font-size:clamp(.96rem,1.02vw,1.06rem)!important;line-height:1.5!important;color:rgba(4,16,35,.68)!important}.mn-p__l li::before{content:'–';position:absolute;left:0;color:var(--blau)}
.mn-p__s{margin:5px 0 0;font-size:clamp(.96rem,1.02vw,1.06rem);line-height:1.5;color:rgba(4,16,35,.68)}
.mn-fuss{margin:clamp(12px,1.3vw,18px) 0 0;font-size:.96rem;color:rgba(4,16,35,.58)}
.mn-ende{display:flex;align-items:center;justify-content:center;gap:16px;margin-top:clamp(30px,3.4vw,52px)}
.mn-ende i{width:clamp(30px,4vw,60px);height:1px;background:rgba(17,61,136,.4)}
.mn-ende span{font:400 10.5px/1 var(--mono);letter-spacing:.26em;text-transform:uppercase;color:var(--blau)}
.mn-ki,.mn-pdf{margin:clamp(18px,2vw,28px) 0 0}
@media(max-width:600px){.mn-p__z{flex-wrap:wrap;justify-content:center;text-align:center}.mn-p__z i{display:none}.mn-p__z span{width:100%;white-space:normal}.mn-preise{text-align:center}}
.sag [data-a="heben"]{opacity:1;transform:translate3d(0,120px,0) scale(.975);transition:transform 2.1s cubic-bezier(.16,1,.3,1)}
.sag [data-a="heben"].da{transform:none}
@media(prefers-reduced-motion:reduce){.sag [data-a="heben"]{transform:none;transition:none}}
'''
