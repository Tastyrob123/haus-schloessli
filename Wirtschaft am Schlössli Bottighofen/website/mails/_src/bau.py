#!/usr/bin/env python3
"""Wirtschaft am Schlössli: drei Mail-Vorlagen im Ton des Hauses, als Idee zum Entwurf (Station 13, 19.10.2026; Bauart aus mails/_src/bau.py des Ruedihus).

Drei Fälle, die es im Entwurf wirklich gibt (Fenster der Website):
  01 Ihre Reservation   nach der Anfrage im Reservations-Fenster (Tag, Uhrzeit, Personen, Platz, bereitgelegte Flasche)
  02 Ihr Bankett        nach der Bankettanfrage (Datum, Personen, Etage, Menü aus den Bankettmenüvorschlägen)
  03 Ihr Gutschein      nach dem Gutschein, die Karte hängt als PDF an
Echter Text oben (Titel, Anrede, Sätze), Fotos nur mit Beschreibung und unter 100 KB, lesbar auch mit gesperrten Bildern (Master 5b, Pitch-Mails 14.10.2026).
Tabellen und feste Stile, Schrift Arial in Versalien wie die Titel der Seite. Angaben des Hauses aus website/inhalt/haus.json, Beispielwerte erfunden und so beschriftet.
Wortlaut von Tasty Studios, als Vorschlag. Gebaut, nie verschickt.

Aufruf:  python3 mails/_src/bau.py  → mails/NN-<fall>/index.html, mails/index.html, mails/img/;  danach node mails/_src/aufnahme.js (Server 8982)"""
import html, json, os, sys

HIER = os.path.dirname(os.path.abspath(__file__)); MAILS = os.path.dirname(HIER); ROOT = os.path.dirname(MAILS)
from PIL import Image  # noqa: E402
HJ = json.load(open(os.path.join(ROOT, 'inhalt', 'haus.json'), encoding='utf-8'))
BK = json.load(open(os.path.join(ROOT, 'inhalt', 'bankett.json'), encoding='utf-8'))

e = html.escape
HOLZ, RUSS, TIEF, PAPIER, BLATT, TINTE, KERZE, GOLD, LICHT = '#113d88', '#0b1d3d', '#081631', '#e7ecf3', '#fbfcfe', '#041023', '#a2b6cf', '#c5d2e1', '#d0dae7'
SERIF = "Arial,'Helvetica Neue',Helvetica,sans-serif"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
ADRESSE = f"{HJ['strasse']} · {HJ['ort']}"
TEL_ZEIGE = HJ['telefon'].replace(' ', '\u00a0')   # Nummer bricht nicht um
GRUSS = 'Monika Huber, Jonas Volpert und das Team'
STAND = '19.10.2026'
_herbst = next(m for m in BK['menues'] if m['name'] == 'Herbst')

FAELLE = [
    dict(nr='01', wann='Gleich nach der Reservationsanfrage', ordner='01-reservation', name='Ihre Reservation', satz='Kommt gleich nach der Anfrage im Fenster: Tag, Uhrzeit, Personen, Platz und die bereitgelegte Flasche zum Nachlesen.',
         betreff='Ihre Reservation ist bei uns', titel=('Ihr Tisch', 'am Hafen.'), foto=('platanen', 'Gedeckte Tische unter den Platanen der Terrasse, dahinter der Hafen'),
         text=['Liebe Frau Keller', 'Vielen Dank für Ihre Anfrage. Wir schauen in unser Buch und bestätigen Ihnen den Tisch persönlich.',
               'Die Flasche, die Sie ausgesucht haben, legt Jonas Volpert für Sie bereit. Die ganze Karte finden Sie schon jetzt auf unserer Seite.',
               f'Geht etwas schneller am Telefon, erreichen Sie uns unter {TEL_ZEIGE}.'],
         karte=('Ihre Anfrage', [('Tag', 'Samstag, 6. Juni 2026'), ('Uhrzeit', '19:00 Uhr'), ('Personen', '2'), ('Platz', 'Terrasse'), ('Flasche', 'aus der Weinkarte bereitgelegt')]),
         knopf=('Die Karte ansehen', 'karte.html'), dazu=f"{HJ['zeiten']['tage']}, {HJ['zeiten']['offen']}. {HJ['zeiten']['ruhetag']}."),
    dict(nr='02', wann='Gleich nach der Bankettanfrage', ordner='02-bankett', name='Ihr Bankett', satz='Kommt nach der Bankettanfrage: Datum, Personen, Etage und Menü, und der Satz, dass wir uns melden.',
         betreff='Ihre Bankettanfrage ist bei uns', titel=('Ihr Fest', 'am See.'), foto=('lounge', 'Die Lounge am Ufer, dahinter der See und die Alpen'),
         text=['Lieber Herr Brunner', 'Vielen Dank für Ihre Anfrage. Wir melden uns persönlich, besprechen mit Ihnen das Menü und richten uns nach Ihnen und Ihren Wünschen.',
               HJ['bankett']['platz'],
               'Gibt es Allergien oder ein Gericht, das auf keinen Fall fehlen darf, schreiben Sie es uns gern noch dazu.'],
         karte=('Ihre Anfrage', [('Datum', 'Freitag, 18. September 2026'), ('Personen', '24'), ('Etage', 'eine Etage für Sie'), ('Menü', f"{_herbst['name']}, CHF {_herbst['preis']} je Person")]),
         knopf=('Die Bankettmenüs ansehen', 'feiern.html'), dazu=f"Für Fragen erreichen Sie uns unter {TEL_ZEIGE}."),
    dict(nr='03', wann='Nach der Bestellung des Gutscheins', ordner='03-gutschein', name='Ihr Gutschein', satz='Kommt nach der Bestellung des Gutscheins. Die Karte selbst hängt als PDF an der Mail.',
         betreff='Ihr Gutschein für das Schlössli', titel=('Ihr Gutschein', 'ist da.'), foto=('glas', 'Ein Glas Weisswein vor dem See'),
         text=['Liebe Frau Keller', 'Vielen Dank. Ihr Gutschein hängt als PDF an dieser Mail, mit Ihrem Satz darauf. Drucken Sie ihn aus oder schicken Sie ihn weiter.',
               'Eingelöst wird er bei uns am Hafen.'],
         karte=('Ihr Gutschein', [('Für', 'Anna und Luca'), ('Von', 'Mama'), ('Betrag', 'CHF 150'), ('Satz', '«Ein Abend am See»')]),
         knopf=('Einen Tisch reservieren', 'index.html'), dazu=f"Fragen dazu beantworten wir gern unter {TEL_ZEIGE}."),
]


def bilder():
    """Fotos 1000 px, unter 100 KB (Qualität sinkt, bis es passt)."""
    os.makedirs(os.path.join(MAILS, 'img'), exist_ok=True)
    for f in FAELLE + [dict(foto=('team', ''))]:
        key = f['foto'][0]
        q = next(os.path.join(ROOT, 'assets', 'img', f'{key}-{s}.webp') for s in (1200, 1800, 900, 800) if os.path.exists(os.path.join(ROOT, 'assets', 'img', f'{key}-{s}.webp')))
        im = Image.open(q).convert('RGB'); w, h = im.size; nh = round(w * 9 / 16)
        if nh < h:
            y = round((h - nh) * .5); im = im.crop((0, y, w, y + nh))
        im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
        z = os.path.join(MAILS, 'img', key + '.jpg')
        for br, qu in ((1000, 80), (1000, 72), (1000, 64), (900, 66), (820, 64), (760, 62)):
            k = im.resize((br, round(im.height * br / im.width)), Image.LANCZOS) if br < im.width else im
            k.save(z, quality=qu, optimize=True, progressive=True)
            if os.path.getsize(z) < 100_000:
                break


def mail(f, basis):
    """basis: Adresse der Website, relativ aus dem Ordner der Mail (Vorschau) oder voll (Versand)."""
    zeilen = ''.join(f'<tr><td style="padding:11px 0;border-top:1px solid #2a4f8f;font:400 11px/1.3 {SANS};letter-spacing:.14em;text-transform:uppercase;color:{LICHT};width:38%">{e(k)}</td>'
                     f'<td style="padding:11px 0;border-top:1px solid #2a4f8f;font:400 16px/1.35 {SANS};color:{BLATT}">{e(v)}</td></tr>' for k, v in f['karte'][1])
    absaetze = f'<p style="margin:0 0 14px;font:400 20px/1.3 {SANS};color:{TINTE}">{e(f["text"][0])}</p>' + ''.join(
        f'<p style="margin:0 0 14px;font:400 16px/1.62 {SANS};color:#22324d">{e(t)}</p>' for t in f['text'][1:])
    return f'''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>{e(f['betreff'])} · Wirtschaft am Schlössli</title></head>
<body style="margin:0;padding:0;background:{PAPIER}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{PAPIER}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:{BLATT};border-radius:22px;overflow:hidden">
  <tr><td align="center" style="background:{HOLZ};padding:34px 30px 30px">
    <img src="../img/zeichen.png" width="58" alt="" style="display:block;border:0;width:58px;height:auto;margin:0 auto 14px">
    <div style="font:400 15px/1.2 {SERIF};letter-spacing:.3em;color:{BLATT}">SCHLÖSSLI</div>
    <div style="margin-top:7px;font:400 10.5px/1.2 {SANS};letter-spacing:.24em;text-transform:uppercase;color:{KERZE}">Wirtschaft am Schlössli · Bottighofen</div>
    <h1 style="margin:28px 0 0;font:400 clamp(26px,7.4vw,34px)/1.18 {SERIF};letter-spacing:.12em;text-transform:uppercase;color:{BLATT}">{e(f['titel'][0])}<br><span style="color:{KERZE}">{e(f['titel'][1])}</span></h1>
  </td></tr>
  <tr><td style="padding:34px clamp(22px,6vw,40px) 8px">{absaetze}</td></tr>
  <tr><td style="padding:6px 28px 6px"><img src="../img/{f['foto'][0]}.jpg" width="544" alt="{e(f['foto'][1])}" style="display:block;border:0;width:100%;height:auto;border-radius:16px"></td></tr>
  <tr><td style="padding:10px 28px 6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{HOLZ};border-radius:16px">
    <tr><td style="padding:22px 26px 12px"><div style="font:400 10.5px/1.2 {SANS};letter-spacing:.2em;text-transform:uppercase;color:{KERZE};padding-bottom:12px">{e(f['karte'][0])} · Beispielwerte</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{zeilen}</table></td></tr></table></td></tr>
  <tr><td align="center" style="padding:26px 40px 8px"><a href="{basis}{f['knopf'][1]}" style="display:inline-block;padding:16px 30px;border-radius:999px;background:{HOLZ};font:400 12px/1 {SANS};letter-spacing:.16em;text-transform:uppercase;color:{BLATT};text-decoration:none">{e(f['knopf'][0])} &nbsp;↗</a></td></tr>
  <tr><td style="padding:14px 40px 30px"><p style="margin:0;font:400 15px/1.6 {SANS};color:#3a4c69;text-align:center">{e(f['dazu'])}</p>
    <img src="../img/team.jpg" width="520" alt="Das Team der Wirtschaft am Schlössli" style="display:block;border:0;width:100%;max-width:520px;height:auto;margin:26px auto 0;border-radius:16px">
    <p style="margin:16px 0 0;font:400 17px/1.4 {SANS};color:{TINTE};text-align:center">Herzlich, {e(GRUSS)}</p></td></tr>
  <tr><td align="center" style="background:{RUSS};padding:26px 30px"><div style="font:400 13px/1.4 {SERIF};letter-spacing:.24em;color:{BLATT}">WIRTSCHAFT AM SCHLÖSSLI</div>
    <div style="margin-top:8px;font:400 13px/1.6 {SANS};color:#c5d2e1">{e(ADRESSE)}<br><span style="color:#c5d2e1">{e(TEL_ZEIGE)}</span> · <span style="color:#c5d2e1">{e(HJ['mail'])}</span></div></td></tr>
</table>
</td></tr></table>
</body></html>
'''


def eingebettet(f):
    """Robert 18.10.2026 23:35 «die E-Mails laden zu lange … bis die offen sind»: die Mail steht direkt in der Seite (kein eingebettetes Fenster,
    das Safari beim Aufklappen erst nachzeichnet). Dieselbe Mail wie im Ordner, nur die Bildwege von hier aus."""
    t = mail(f, '../')
    t = t[t.index('<body'):]; t = t[t.index('>') + 1:t.rindex('</body>')]
    return t.replace('src="../img/', 'src="img/')


def uebersicht():
    # Robert 18.10.2026 (Website-Master Punkt 15): Mails nebeneinander im Band, obere Hälfte mit weichem Auslauf, «Ganze Mail» auf und zu,
    # Nummer, Titel, Absender und Wann darüber; Pfeile am Laptop, am Handy eine nach der anderen
    pf = lambda d: f'<svg viewBox="0 0 16 16" aria-hidden="true"><path d="{d}"/></svg>'
    karten = ''.join(f'''<article class="mb">
  <header class="mb-ueber"><span class="mb-nr">{f['nr']}</span><span class="mb-ueber__t"><b>{e(f['name'])}</b><small><span>Von</span> Wirtschaft am Schlössli · {e(HJ['mail'])}</small><small><span>Wann</span> {e(f['wann'])}</small><small><span>Betreff</span> {e(f['betreff'])}</small></span></header>
  <div class="mb-blatt"><div class="mb-in">{eingebettet(f)}</div></div>
  <p class="mb-ganz"><button type="button" class="mb-kn" aria-expanded="false"><span class="a">Ganze Mail</span><span class="z">Weniger zeigen</span><i>{pf('M4 6l4 4 4-4')}</i></button></p>
</article>''' for f in FAELLE)
    return f'''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>Drei Mails · Wirtschaft am Schlössli</title>
<link rel="icon" href="../assets/svg/zeichen.svg">
<style>
@font-face{{font-family:'Open Sans';font-weight:300 700;font-display:swap;src:url('../assets/fonts/OpenSans-var.woff2') format('woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:400 600;font-display:swap;src:url('../assets/fonts/InstrumentSans-normal-400_600.woff2') format('woff2')}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:{RUSS};color:{BLATT};font:400 17px/1.6 'Instrument Sans',system-ui,sans-serif;--rand:clamp(20px,4.6vw,76px)}}
header.kopf{{padding:clamp(56px,8vw,120px) var(--rand) clamp(30px,4vw,60px);text-align:center}}
header.kopf img{{width:clamp(50px,5.9vw,92px);height:auto}}
h1{{margin:clamp(14px,1.6vw,24px) 0 0;font:400 clamp(1.9rem,4.6vw,4.4rem)/1.12 'Open Sans',Arial,sans-serif;text-transform:uppercase;letter-spacing:.12em}}h1 em{{font-style:normal;color:{KERZE}}}
header.kopf p{{max-width:60ch;margin:clamp(18px,2.1vw,32px) auto 0;color:rgba(243,246,249,.86)}}
main{{padding:0 0 clamp(60px,8vw,120px)}}
.band{{display:flex;gap:clamp(20px,2.4vw,40px);align-items:flex-start;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scroll-padding-inline:var(--rand);padding:4px var(--rand) 34px;scrollbar-width:none;-webkit-overflow-scrolling:touch}}
.band::-webkit-scrollbar{{display:none}}
.band:focus-visible{{outline:2px solid {KERZE};outline-offset:-2px}}
.mb{{flex:0 0 clamp(300px,34vw,520px);scroll-snap-align:start}}
.mb:last-child{{margin-inline-end:var(--rand)}}
.mb-ueber{{display:flex;gap:16px;align-items:flex-start;margin:0 4px 18px}}
.mb-nr{{font:400 2.3rem/.9 'Open Sans',Arial,sans-serif;color:{KERZE}}}
.mb-ueber__t{{display:flex;flex-direction:column;gap:5px;min-width:0}}
.mb-ueber__t b{{font:400 1.2rem/1.2 'Open Sans',Arial,sans-serif}}
.mb-ueber__t small{{font-size:.86rem;line-height:1.4;color:rgba(243,246,249,.74)}}
.mb-ueber__t small span{{display:inline-block;min-width:5.4em;font:400 10px/1.4 ui-monospace,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;color:{KERZE}}}
.mb-blatt{{position:relative;height:640px;border-radius:20px;overflow:hidden;background:{PAPIER};box-shadow:0 0 0 1px rgba(162,182,207,.3),0 40px 50px -30px rgba(0,0,0,.9);-webkit-mask-image:linear-gradient(#000 68%,transparent);mask-image:linear-gradient(#000 68%,transparent)}}
.mb.auf .mb-blatt{{-webkit-mask-image:none;mask-image:none}}
.mb-in{{position:relative}}.mb-in table{{max-width:100%}}
.mb-ganz{{position:relative;margin:-30px 0 0;text-align:center}}
.mb.auf .mb-ganz{{margin-top:22px}}
.mb-kn{{display:inline-flex;align-items:center;gap:12px;padding:8px 8px 8px 22px;border:0;border-radius:999px;cursor:pointer;font:400 11.5px/1 ui-monospace,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;color:{BLATT};
  background:linear-gradient(180deg,#1d4f9e,{HOLZ} 60%,{TIEF});box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 0 0 1px rgba(162,182,207,.38),0 14px 22px -12px rgba(0,0,0,.8)}}
.mb-kn i{{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;color:{TINTE};background:linear-gradient(180deg,#f3f6f9,{LICHT} 55%,{KERZE});box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}}
.mb-kn svg{{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}}
.mb-kn .z,.mb.auf .mb-kn .a{{display:none}}.mb.auf .mb-kn .z{{display:inline}}.mb.auf .mb-kn svg{{transform:rotate(180deg)}}
.mb-kn:focus-visible{{outline:2px solid {LICHT};outline-offset:3px}}
.pfeile{{display:flex;justify-content:center;gap:14px;margin-top:4px}}
.pf{{width:52px;height:52px;border:0;border-radius:50%;cursor:pointer;display:grid;place-items:center;color:{TINTE};background:linear-gradient(180deg,#f3f6f9,{LICHT} 55%,{KERZE});box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 12px 20px -10px rgba(0,0,0,.7)}}
.pf svg{{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.pf:disabled{{opacity:.35;cursor:default}}
footer{{padding:26px var(--rand) 40px;text-align:center;font-size:.92rem;color:rgba(243,246,249,.6);border-top:1px solid rgba(162,182,207,.2)}}
footer a{{color:{LICHT}}}
@media (max-width:760px){{.mb{{flex-basis:calc(100vw - 2 * var(--rand))}}.pfeile{{display:none}}}}
@media (hover:none){{.pfeile{{display:none}}}}
</style></head>
<body>
<header class="kopf"><img src="img/zeichen.png" alt="" width="92"><h1>Drei Mails,<br><em>im Ton Ihres Hauses.</em></h1>
<p>Was ein Gast nach einer Anfrage von Ihnen bekommt, sieht aus wie die neue Seite. Drei Fälle als Idee. Namen, Daten und Beträge in den Mails sind Beispielwerte, Telefon, Adresse und Zeiten sind Ihre.</p></header>
<main><div class="band" id="mband" tabindex="0" aria-label="Die drei Mails, zum Blättern">{karten}</div>
<div class="pfeile"><button type="button" class="pf" data-r="-1" aria-label="Vorige Mail">{pf('M10 3 5 8l5 5')}</button><button type="button" class="pf" data-r="1" aria-label="Nächste Mail">{pf('m6 3 5 5-5 5')}</button></div></main>
<footer>Entwurf von Robert Reff, Tasty Studios. Stand {STAND}. <a href="../werkbank/index.html#papier">Zurück zu «Alles auf einen Blick»</a></footer>
<script>
(function () {{
  /* die Mail steht in der Seite; zu sieht man den oberen Teil, auf die ganze Mail, sofort */
  var ms = [].slice.call(document.querySelectorAll('.mb'));
  function lage(m) {{ var bl = m.querySelector('.mb-blatt'), i = bl.querySelector('.mb-in'); bl.style.height = (m.classList.contains('auf') ? i.scrollHeight : Math.min(640, i.scrollHeight)) + 'px'; }}
  ms.forEach(function (m) {{
    var k = m.querySelector('.mb-kn');
    [].forEach.call(m.querySelectorAll('img'), function (im) {{ if (!im.complete) im.addEventListener('load', function () {{ lage(m); }}, {{ once: true }}); }});
    lage(m);
    k.addEventListener('click', function () {{ var auf = m.classList.toggle('auf'); k.setAttribute('aria-expanded', auf); lage(m); if (!auf) m.scrollIntoView({{ block: 'nearest' }}); }});
  }});
  var rt = 0; addEventListener('resize', function () {{ clearTimeout(rt); rt = setTimeout(function () {{ ms.forEach(lage); kl(); }}, 120); }});
  /* Pfeile am Laptop blättern das Band um eine Mail */
  var b = document.getElementById('mband'), p = document.querySelectorAll('.pf');
  function schritt() {{ return ms[0].getBoundingClientRect().width + parseFloat(getComputedStyle(b).columnGap || 0); }}
  function kl() {{ p[0].disabled = b.scrollLeft < 4; p[1].disabled = b.scrollLeft > b.scrollWidth - b.clientWidth - 4; }}
  [].forEach.call(p, function (x) {{ x.addEventListener('click', function () {{ b.scrollBy({{ left: +x.dataset.r * schritt(), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }}); }}); }});
  b.addEventListener('scroll', kl, {{ passive: true }}); kl();
}})();
</script>
</body></html>
'''


def main():
    bilder()
    for f in FAELLE:
        z = os.path.join(MAILS, f['ordner']); os.makedirs(z, exist_ok=True)
        open(os.path.join(z, 'index.html'), 'w', encoding='utf-8').write(mail(f, '../../'))
    open(os.path.join(MAILS, 'index.html'), 'w', encoding='utf-8').write(uebersicht())
    json.dump([[f['nr'], f['ordner'], f['name'], f['satz']] for f in FAELLE], open(os.path.join(HIER, 'werkbank.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(FAELLE), 'Mails gebaut:', ', '.join(f['ordner'] for f in FAELLE))


if __name__ == '__main__':
    main()
