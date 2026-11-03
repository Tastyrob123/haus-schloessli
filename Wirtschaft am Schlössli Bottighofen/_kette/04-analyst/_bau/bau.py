# Wirtschaft am Schlössli, Potentialanalyse: erster Entwurf ohne Blender (Robert 19.10.2026).
# Eigenes Kleid: Hafen-Tafel (Register wie eine Abfahrtstafel am Steg), Gilda Display wie die Seite des Hauses, Nachtblau und Stuhlblau aus Seite und Fotos.
#   python3 bau.py → ../potential/index.html + ../potential.json
import json, os, html
from inhalt import *
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(os.path.dirname(H), 'potential')
B = json.load(open(H + '/belege.json')); e = html.escape

def quelltext(c):
    zeilen = ''.join(f'<li{" class=hl" if n in c["mark"] else ""}><span class=n>{n or ""}</span><code>{e(t)}</code></li>' for n, t in c['zeilen'])
    ziel = SEITE + '/' if 'start' in c['code'] else SEITE + '/kontakt' if 'kontakt' in c['code'] else ''
    hinweis = f' · <a href="view-source:{ziel}">Quelltext öffnen</a>' if ziel and c['code'].startswith('roh/') else ''
    return f'<figure class="qt"><figcaption>{e(c["datei"])}{hinweis}</figcaption><ol>{zeilen}</ol></figure>'

def aufnahme(id):
    b = B[id]; geraet = 'Rechner' if b['desk'] else 'Telefon'
    url = b['url']; kurz = url.replace('https://www.', '').replace('https://', '')
    nah = f'<a class="nah" href="belege/{id}-nah.webp" target="_blank"><img src="belege/{id}-nah.webp" width="{b["nah"][0]}" height="{b["nah"][1]}" loading="lazy" alt="Die Stelle vergrössert"></a>' if 'nah' in b else ''
    solo = '' if 'nah' in b else ' solo'
    stand = 'Seite 1 der PDF-Karte in Telefonbreite (390 Punkte), aus der Datei gerendert' if id == 'speisekarte-pdf' else f'{geraet} · {e(kurz)} · 19.10.2026'
    return (f'<figure class="auf {"desk" if b["desk"] else "tel"}{solo}"><div class="paar">'
            f'<a class="ganz" href="belege/{id}-ganz.webp" target="_blank"><img src="belege/{id}-ganz.webp" width="{b["ganz"][0]}" height="{b["ganz"][1]}" loading="lazy" alt="Aufnahme {e(geraet)}: {e(kurz)}"></a>{nah}</div>'
            f'<figcaption><span>{stand}</span><a class="hin" href="{e(url)}" target="_blank" rel="noopener">{"Auf Ihrer Seite ansehen" if "schloessli-bottighofen" in url else "Beim Guide Michelin ansehen"} ↗</a></figcaption></figure>')

def beleg(x):
    if isinstance(x, str): return aufnahme(x)
    if 'code' in x: return quelltext(x)
    if 'bild' in x: return f'<figure class="auf frei"><img src="{x["bild"]}" loading="lazy" alt=""><figcaption><span>{e(x["text"])}</span></figcaption></figure>'
    if 'link' in x: return f'<p class="nurlink"><a href="{e(x["link"])}" target="_blank" rel="noopener">{e(x["text"])} ↗</a></p>'

def quelle(q):
    return f'<a href="{e(q)}" target="_blank" rel="noopener">{e(q)}</a>' if q.startswith('http') else e(q)

reg = ''.join(f'<a class="zeile" href="#p{b["nr"]}"><span class="nr">{b["nr"]}</span><img src="bilder/{b["foto"]}-720.webp" alt="" loading="lazy"><span class="ziel">{e(b["titel"])}</span><span class="steg">{e(b["kurz"])}</span></a>' for b in BEFUNDE)

punkte = ''
for b in BEFUNDE:
    punkte += f'''
<section class="punkt" id="p{b["nr"]}">
 <header><span class="gross">{b["nr"]}</span><div><p class="steg">{e(b["kurz"])}</p><h2>{e(b["titel"])}</h2></div></header>
 <div class="spalten">
  <div class="text">
   <h3>Wo</h3><p>{e(b["wo"])}</p>
   <h3>Was genau</h3><p>{e(b["was"])}</p>
   <h3>Warum es stört</h3><p>{e(b["warum"])}</p>
   <div class="bedeutet"><p><b>Für Ihre Gäste</b>{e(b["gaeste"])}</p><p><b>Für Ihr Haus</b>{e(b["haus"])}</p></div>
   <p class="tun"><b>Was wir tun würden</b> {e(b["tun"])}</p>
   <details><summary>Quellen</summary><ul>{"".join(f"<li>{quelle(q)}</li>" for q in b["quellen"])}</ul></details>
  </div>
  <div class="belege">{"".join(beleg(x) for x in b["belege"])}</div>
 </div>
</section>'''

zahlen = ''.join(f'<div><b>{z}</b><span>{e(t)}</span><small>{e(q)}</small></div>' for z, t, q in ZAHLEN)
stimmt = ''.join(f'<li>{f"<img src=bilder/{f}-720.webp alt=>" if f else ""}<div><b>{e(t)}</b><p>{e(s)}</p></div></li>' for t, s, f in STIMMT)
def selbst_ziel(z):
    if z in B: return f'<a href="belege/{z}-nah.webp" target="_blank">Aufnahme</a> · <a href="{e(B[z]["url"])}" target="_blank" rel="noopener">auf Ihrer Seite ↗</a>'
    return f'<a href="{e(z)}" target="_blank" rel="noopener">ansehen ↗</a>' if z.startswith('http') else f'<span class="q">{e(z)}</span>'
selbst = ''.join(f'<li><b>{e(t)}</b><p>{e(s)}</p><p class="wo">{selbst_ziel(z)}</p></li>' for t, s, z in SELBST)
chancen = ''.join(f'<li><b>{e(t)}</b><p>{e(s)}</p><p class="wo">{quelle(q) if q.startswith("http") else f"<span class=q>{e(q)}</span>"}</p></li>' for t, s, q in CHANCEN)
heute = ''.join(f'<div class="hz"><b>{e(t)}</b><p>{e(s)}</p><small>{e(q)}</small></div>' for t, s, q in HEUTE['fakten'])
offen = ''.join(f'<li>{e(o)}</li>' for o in HEUTE['offen'])
gruss = ''.join(f'<p>{e(s)}</p>' for s in GRUSS)

seite = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Potentialanalyse · Wirtschaft am Schlössli, Bottighofen</title>
<meta name="description" content="Die Website der Wirtschaft am Schlössli, gelesen am Telefon und am Rechner: {len(BEFUNDE)} Stellen mit Beleg. Stand {STAND}.">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#1f3a4c">
<link rel="icon" href="bilder/zeichen.png">
<link rel="preload" href="schrift/GildaDisplay.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="schloessli.css">
</head>
<body>
<header class="auftakt">
 <img class="foto" src="bilder/terrasse-1920.webp" srcset="bilder/terrasse-960.webp 960w, bilder/terrasse-1920.webp 1920w" sizes="100vw" alt="Die Terrasse der Wirtschaft am Schlössli unter Platanen am Hafen von Bottighofen">
 <div class="schild">
  <img class="zeichen" src="bilder/zeichen.png" alt="">
  <p class="vor">Potentialanalyse der Website</p>
  <h1>Wirtschaft am Schlössli</h1>
  <p class="ort">Seestrasse 50 · Bottighofen · am Hafen</p>
  <p class="satz">Was Ihre Seite heute zeigt, und was Ihr Haus mehr zu erzählen hat.</p>
  <p class="zeile">15 Seiten gelesen · 1 Sprache · {len(BEFUNDE)} Stellen · {STAND}</p>
 </div>
</header>

<main>
<section class="gruss">
 <div class="brief">{gruss}</div>
 <div class="zahlen">{zahlen}</div>
</section>

<section class="tafel" id="tafel">
 <h2>Was zuerst zählt</h2>
 <p class="unter">Von oben nach unten: was ein Gast am ehesten merkt.</p>
 <nav class="register">{reg}</nav>
 <p class="blaetter"><a href="#stimmt">Was gut ist</a> · <a href="#selbst">Selbst beheben</a> · <a href="#heute">Ihre Seite heute</a> · <a href="#chancen">Was möglich ist</a></p>
</section>

{punkte}

<section class="blatt" id="stimmt"><h2>Was gut ist</h2><ul class="stimmt">{stimmt}</ul></section>

<section class="blatt hell" id="selbst"><h2>Selbst beheben</h2><p class="unter">Kleinigkeiten, die Sie oder Ihr Team in wenigen Minuten ändern können.</p><ul class="liste">{selbst}</ul></section>

<section class="blatt dunkel" id="heute">
 <h2>Ihre Seite heute: wer dahinter steht und was wem gehört</h2>
 <div class="heute">{heute}</div>
 <p class="beiuns">{e(HEUTE["bei_uns"])}</p>
 <h3>Noch offen</h3><ul class="offen">{offen}</ul>
</section>

<section class="blatt" id="chancen"><h2>Was möglich ist</h2><p class="unter">Was Ihr Haus schon hat und die Seite noch nicht erzählt.</p><ul class="liste">{chancen}</ul></section>
</main>

<footer class="fuss"><img src="bilder/zeichen.png" alt=""><p>Gelesen am {STAND}, iPhone 390 × 844 und Rechner 1440 × 900. Alle Aufnahmen zeigen Ihre Seite, wie sie an diesem Tag war.</p><p>Tasty Studios, Hamburg · eine Studie, nicht die offizielle Website des Hauses</p></footer>
</body>
</html>
'''
open(P + '/index.html', 'w').write(seite)

# Paket: potential.json (Befunde mit Beleg)
def belegtext(x):
    if isinstance(x, str): return f'potential/belege/{x}-ganz.webp (+ -nah.webp), {B[x]["url"]}'
    if 'code' in x: return f'_bau/{x["code"]} Zeilen {", ".join(str(n) for n, _ in x["zeilen"] if n)}' if x['code'].startswith('roh/') else x['code']
    return x.get('bild') or x.get('link')
pj = {'stand': STAND, 'entwurf': 'erster Entwurf ohne Blender (Robert 19.10.2026); Aufnahmen in _bau/stellen/, Belege in potential/belege/',
      'befunde': [{'nr': b['nr'], 'was': b['titel'], 'wo': b['wo'], 'nutzen': f'Gäste: {b["gaeste"]} Haus: {b["haus"]} Was wir tun würden: {b["tun"]}',
                   'beleg': '; '.join(belegtext(x) for x in b['belege']), 'quellen': b['quellen']} for b in BEFUNDE],
      'chancen': [{'was': f'{t}: {s}', 'beleg': q} for t, s, q in CHANCEN],
      'zahlen': [{'wert': z, 'einheit': t, 'quelle': q} for z, t, q in ZAHLEN] + [
          {'wert': 26, 'einheit': 'Personen je Etage (zwei Etagen)', 'quelle': 'https://www.schloessli-bottighofen.ch/karten, 19.10.2026'},
          {'wert': 26, 'einheit': 'Seiten Weinkarte vom 14.10.2026', 'quelle': 'pdfinfo _bau/pdf/20261014_Weinkarte.pdf'},
          {'wert': 2601, 'einheit': 'Follower @schloessli_bottighofen', 'quelle': '_quelle/extern/ig/profil.txt (19.10.2026)'},
          {'wert': '12.09.2024', 'einheit': 'Anlage der Squarespace-Seite', 'quelle': 'Späher-Befund 18.10.2026'},
          {'wert': '03.04.2025', 'einheit': 'Eröffnung', 'quelle': '_quelle/presse/gaultmillau-zwei-koeniginnen.md'},
          {'wert': '27.03.2025', 'einheit': 'gültig ab: Terms of Service Squarespace', 'quelle': 'https://www.squarespace.com/terms-of-service, 19.10.2026'}],
      'selbst_beheben': [{'was': t, 'text': s, 'beleg': z} for t, s, z in SELBST],
      'nachtraege_zum_befund_02': [
          {'datum': '19.10.2026', 'punkt': 'Seite «Karten» trägt jetzt die Überschrift «Karten» mit Speisekarte, Weinkarte, Lästermeile und Zeiten; am 18.10. nur «Banketts & Gruppen»', 'beleg': 'stellen/karten-handy.png'},
          {'datum': '19.10.2026', 'punkt': 'Newsletter-Baustein «Abonnieren» auf /kontakt ist für Gäste sichtbar (Befund 18.10.: unsichtbar); Speicherort weiter leer', 'beleg': 'stellen/newsletter-handy.png, roh/kontakt.html Z. 3227, 3245'},
          {'datum': '19.10.2026', 'punkt': 'Kontaktseite hat einen Knopf «Kontaktformular» (Formular mit Pflicht-Häkchen «vor dem Senden ankreuzen»)', 'beleg': 'probe/m-kontaktform.png'}],
      'geprueft_wie_schaefli': [
          {'punkt': 'Reservieren-Knopf auf dem Cookie-Hinweis (Schäfli 01)', 'ergebnis': 'gilt beim Schlössli nicht: kein fester Knopf, «ablehnen» frei', 'beleg': '_bau/probe/m-erst.png, potential/belege/cookie-handy-ganz.webp'},
          {'punkt': 'Karten nur als PDF (Schäfli 02)', 'ergebnis': 'gilt auch hier, Befund 03', 'beleg': 'karten-handy, speisekarte-pdf'},
          {'punkt': 'Datenschutz passt nicht zur Seite (Schäfli 10)', 'ergebnis': 'gilt auch hier, Befund 12, mit eigener Messung', 'beleg': 'datenschutz-handy, shop-handy'},
          {'punkt': 'Gutschein als Formular (Schäfli 07)', 'ergebnis': 'gilt auch hier, Befund 05, dazu Pflicht-Häkchen ohne Text', 'beleg': 'gutschein-handy'}]}
json.dump(pj, open(os.path.dirname(H) + '/potential.json', 'w'), ensure_ascii=False, indent=1)
print('index.html', len(seite), 'Zeichen ·', len(BEFUNDE), 'Befunde')
