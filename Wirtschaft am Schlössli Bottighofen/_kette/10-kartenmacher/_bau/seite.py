# seite.py · baut das Paket der Station 10: karten.json, pruefung.md, bilder/ und die Seite karten.html.
# Liest nur: _karten/stand/*.json, _karten/druckbericht.json, abgleich.json (aus _karten/abgleich.py), Markenbuch (Station 5).
# Lauf: python3 _kette/10-kartenmacher/_bau/seite.py
import base64, html, json, pathlib, re, shutil, subprocess

PAKET = pathlib.Path(__file__).resolve().parent.parent
PROJ = PAKET.parent.parent
K = PROJ / '_karten'
MARKE = PROJ / '_kette' / '05-markenbauer' / 'marke'
e = lambda s: html.escape(str(s), quote=True)

FOTO = {'speisekarte': ('tortelloni', 'Tortelloni mit Tomate, Burrata und Taggiasca-Olive'),
        'weinkarte': ('wein', 'Wein im Glas auf der Terrasse'),
        'laestermeile': ('bar', 'An der Bar der Lästermeile'),
        'lunch': ('suppe', 'Eine Suppe aus der Küche des Hauses'),
        'bankett': ('anguria', 'Das Gericht «Anguria» auf dem blauen Platzteller'),
        'vier-haende': ('stier', 'Zum 4-Hands-Lunch mit Patrick Stier')}
REIHE = ['speisekarte', 'lunch', 'laestermeile', 'weinkarte', 'bankett', 'vier-haende']
WORT = {'speisekarte': ('Die', 'Speisekarte.'), 'lunch': ('Das', 'Lunch-Menü.'), 'laestermeile': ('Die', 'Lästermeile.'),
        'weinkarte': ('Die', 'Weinkarte.'), 'bankett': ('Das', 'Bankettmenü.'), 'vier-haende': ('Der', '4-Hands-Lunch.')}
ZAHLWORT = {1: 'Eine', 2: 'Zwei', 3: 'Drei', 4: 'Vier', 5: 'Fünf', 6: 'Sechs', 7: 'Sieben'}


def foto(name):
    for b in (800, 900, 1200, 480):
        p = PROJ / 'website' / 'assets' / 'img' / f'{name}-{b}.webp'
        if p.exists():
            return f'../../website/assets/img/{name}-{b}.webp'
    raise SystemExit('Foto fehlt: ' + name)


def main():
    stand = {p.stem: json.loads(p.read_text()) for p in (K / 'stand').glob('*.json')}
    druck = json.loads((K / 'druckbericht.json').read_text())
    abgl = {r['id']: r for r in json.loads((PAKET / 'abgleich.json').read_text())}
    (PAKET / 'bilder').mkdir(exist_ok=True)

    # ---------------------------------------------------------- karten.json
    karten = []
    for kid in REIHE:
        s, a, d = stand[kid], abgl[kid], druck[kid]
        ab = sum(len(a[x]) for x in ('fehlt', 'dazu', 'zahlen_fehlt', 'zahlen_dazu', 'zeilen_nicht_gefunden'))
        pdf_ab = len(d['fehlt_in_pdf']) + len(d['dazu_in_pdf']) + len(d['regeln'])
        subprocess.run(['pdftoppm', '-r', '110', '-png', '-f', '1', '-l', '1', '-singlefile', str(K / 'pdf' / f'{kid}.pdf'), str(PAKET / 'bilder' / kid)], check=True)
        if any(t['art'] == 'deckel' for t in s['karte']['teile']):
            subprocess.run(['pdftoppm', '-r', '110', '-png', '-f', '2', '-l', '2', '-singlefile', str(K / 'pdf' / f'{kid}.pdf'), str(PAKET / 'bilder' / f'{kid}-innen')], check=True)
        karten.append({'name': s['karte']['name'], 'id': kid, 'daten': f'_karten/stand/{kid}.json', 'pdf': f'_karten/pdf/{kid}.pdf',
                       'original': s['herkunft']['original'], 'adresse_original': s['herkunft']['adresse'], 'sprache': 'de',
                       'eintraege': a['eintraege'], 'preise': a['preise'], 'seiten_pdf': d['seiten'],
                       'geprueft': True, 'abweichungen': ab, 'pdf_gleich_daten': pdf_ab == 0, 'gilt': s['gilt'], 'offen': s['offen']})
    (PAKET / 'karten.json').write_text(json.dumps(karten, ensure_ascii=False, indent=1) + '\n')

    # ---------------------------------------------------------- pruefung.md
    z = ['---', 'tags: [projekt, website]', 'status: aktiv', '---', '', '# Prüfung der Karten · Wirtschaft am Schlössli · Station 10', '',
         'Stand 19.10.2026. Geprüft mit `_karten/abgleich.py` (Daten gegen Original) und `_karten/bau.py` (neue PDF gegen Daten).', '',
         '## Wie geprüft wurde', '',
         '- **Weg A, Wörter:** jedes Wort der Daten im Text der Original-PDF (pdftotext -layout) und jedes Wort des Originals in den Daten, mit Anzahl.',
         '- **Weg B, Zahlen:** jede Zahl aus einer zweiten, getrennten Lesung der Original-PDF (pdftotext -raw) gegen die Zahlen der Daten.',
         '- **Weg C, Zeilen:** jede Preiszeile (Name, Jahrgang, Kürzel, Flasche, Preis) muss als eine Zeile im Original stehen. Gegenprobe: zwei vertauschte Preise und ein Tippfehler werden gefunden.',
         '- **Neue PDF gegen Daten:** die gedruckte PDF wird wieder ausgelesen und Wort für Wort mit den Daten verglichen; dazu je Seite: kein Eintrag allein, keine Seite endet mit einem Titel. Alle Schriften eingebettet (pdffonts).',
         '- Ausgenommen vom Wortvergleich: Seitenzahlen des Originals und die Fusszeile, die es auf jeder Seite wiederholt (in den Daten einmal als «fuss»).',
         '- **Selbst gelesen, Zeile für Zeile neben dem Original:** Speisekarte (alle 20 Gerichte, 27 Preise), Lästermeile (9), Bankettmenü (15); dazu Weinkarte Seite 12 im Bild (dabei «1er» mit hochgestelltem «er» gefunden, das pdftotext als «1 er» liest; jetzt richtig, 41 Stellen).', '',
         '## Übernommen aus den anderen Häusern (Stand 19.10.2026)', '',
         '- Farbe wie die fertige Website («Ton in Ton» aus dem Platzteller), nicht die Farbwelt A des Markenbuchs (Website `haus.css`, `UEBERGABE.md`).',
         '- Feste Schriftschnitte statt variabler Schrift, keine «Type 3» in der PDF (Carlton 08.10., `_karten/schriften.py`, Prüfung im Druck).',
         '- Lesetext 11 pt, Titel gut doppelt so gross, Preise in der Titelschrift (GBR 11.10., Carlton 08.10.).',
         '- Gleiche Seiten wie das Original, jede Rubrik ganz auf ihrer Seite, freie Höhe je Zwischenraum höchstens 6 mm, Erläuterungen am Fuss (GBR 11.10.). Prüfregel im Druck: jeder Eintrag auf der Seite seiner Rubrik.',
         '- Kein Eintrag allein auf einer Seite, keine Seite endet mit einem Titel (GBR 12.10.).',
         '- Ein Format für jeden Eintrag, Wein mit mehreren Flaschen = ein Eintrag mit mehreren Preisen (GBR 12.10.).',
         '- Weinkarte in drei Ebenen: Farbe als Rubrik, Land in der Titelschrift, Region als Mono-Etikett (GBR 11.10.).',
         '- Menüs ohne Preis je Gericht (Lunch, 4-Hands) ganz mittig, senkrecht und waagrecht, kurzes Menü grösser gesetzt, keine leere untere Hälfte (La Carte C08, Robert 18.10.).',
         '- Dunkle Umschlagfläche als SVG (erscheint ohne «Hintergrund drucken»), Zeichen als Pfad, keine weichen Schatten (GBR 12.10., Abschnitt 8).',
         '- Kein «1 von 2»: Seitenzahl nur in der Weinkarte, ohne Gesamtzahl (Tasty-Sprache, Unterlagen und PDF).',
         '- Unsichtbarer Text des Originals nicht mitgesetzt («A» hinter «CHAMPAGNER/SCHAUMWEIN», Ruedihus 09.10.).',
         '- Eindeutige Tippfehler als Liste, nicht angewendet (`_karten/berichtigt.json`, wie Gasterntal in La Carte).', '',
         '## Ergebnis', '', '| Karte | Einträge | Preise | Wörter Original / Daten | Zahlen Original / Daten | Abweichungen | Neue PDF = Daten |', '|---|---|---|---|---|---|---|']
    for k in karten:
        a = abgl[k['id']]
        z.append(f"| {k['name']} | {k['eintraege']} | {k['preise']} | {a['woerter_original']} / {a['woerter_daten']} | {a['zahlen_original']} / {a['zahlen_daten']} | {k['abweichungen']} | {'ja' if k['pdf_gleich_daten'] else 'NEIN'} ({k['seiten_pdf']} S.) |")
    z += ['', '## Abweichungen mit Fundstelle', '']
    abw = [(k, abgl[k['id']]) for k in karten if k['abweichungen']]
    z += ['Keine. Jedes Wort und jede Zahl der Daten steht im Original, und jedes Wort und jede Zahl des Originals steht in den Daten.'] if not abw else \
         [f"- {k['name']}: {json.dumps({x: a[x] for x in ('fehlt', 'dazu', 'zahlen_fehlt', 'zahlen_dazu', 'zeilen_nicht_gefunden') if a[x]}, ensure_ascii=False)} ({k['original']})" for k, a in abw]
    z += ['', '## Was am Original auffällt (nicht berichtigt, so übernommen)', '',
          '- Weinkarte, jede Seite: «8,1% M wSt.» mit Leerzeichen, im Bild der PDF geprüft (`_quelle/website/pdf/20261014_Weinkarte.pdf`, Fuss jeder Seite).',
          '- Weinkarte, Seite 1: hinter «CHAMPAGNER/SCHAUMWEIN» steht in der Textschicht ein «A», im Bild unsichtbar (weiss); nicht in die Daten genommen.',
          '- Weinkarte: Seitenzahlen beginnen mit «– 2 –»; die PDF hat kein Deckblatt.',
          '- Weinkarte, Rotwein Franken: «0,7l» mit Komma (Weingut Rudolf Fürst, Spätburgunder Hundsrück GG), sonst überall «0.7l».',
          '- Weinkarte: «BAYRISCHER BODENSEE» (Weisswein) und «BAYERISCHER BODENSEE» (Rosé, Rotwein); «NEUCHATEL» und «NEUCHÂTEL».',
          '- Bankettmenü: «Süßsaures» mit ß, «knusprigen Knoblauchbrot», «KALBSHOHRÜCKEN», «OSSOBUCCHI», «MOSCARDINI ALL´ ARRABIATA».',
          '- Lästermeile: «Pickels», «Parmesan–Piment d´espelette-Pommes,» (Gedankenstrich und Bindestrich gemischt).',
          '- Speisekarte: «Fourme d´Ambert» mit Akut statt Apostroph.',
          '- 4-Hands-Lunch: die Seite des Anlasses nennt ein «6-Gang-Menü», die PDF trennt neun Gänge durch ***; «Opera schnitte».',
          '- Lunch: «(3 – Gänge – 35.- Chf)».', '',
          '## Offen je Karte', '']
    for k in karten:
        z.append(f"### {k['name']}"); z.append('')
        z += [f'- {o}' for o in k['offen']] + ['']
    z += ['## Nicht gefunden', '',
          '- Keine Getränke- oder Barkarte (Bier, Aperitif, Spirituosen, Kaffee, Wein im Glas) auf der heutigen Seite. Im Web-Archiv liegt eine «Aperitif Karte» von 2024 (`_quelle/web-archiv/text/2024_speisekarten__aperitif-karte.md`), Stand und Gültigkeit unklar, nicht übernommen.',
          '- Ältere Aktionskarten 2024 (Sommerkarte, Nachmittagskarte, «s’hät solang’s hät», Läschtermeile-Charte) nur im Web-Archiv, nicht übernommen.',
          '- Karten in anderen Sprachen: keine.', '']
    (PAKET / 'pruefung.md').write_text('\n'.join(z))

    # ---------------------------------------------------------- karten.html
    probe = (MARKE / 'probe.html').read_text()
    stil = probe[probe.index('<style>') + 7:probe.index('</style>')]
    stil = stil.replace('url(./', 'url(../05-markenbauer/marke/')
    tap = lambda n: 'data:image/svg+xml;base64,' + base64.b64encode((MARKE / n).read_text().replace('#A2C6CF', '#A2B6CF').encode()).decode()
    # Farbwelt «Ton in Ton» der fertigen Website (Robert 19.10.2026), gemessen auf website/weinkarte.html
    stil += ('[data-welt=a]{--nacht:#0B1D3D;--tief:#0A234C;--mittel:#113D88;--kalk:#E7ECF3;--kalk2:#D0DAE7;--ak:#A2B6CF;--ak-h:#C5D2E1;'
             '--ak-t:#0F3678;--tinte:#041023;--titel-h:#0A2552;--ak-text:#0A2552;--ak-titel:#A2B6CF;'
             f'--tap-d:url({tap("tapete-a-dunkel.svg")});--tap-h:url({tap("tapete-a-hell.svg")})}}')
    zeichen = re.search(r'<svg class="z".*?</svg>', probe, re.S).group(0)
    pf = '<span class="kn"><svg class="pf" viewBox="0 0 16 10"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span>'
    gesamt_e = sum(k['eintraege'] for k in karten)
    gesamt_p = sum(k['preise'] for k in karten)
    gesamt_ab = sum(k['abweichungen'] for k in karten)
    offen_n = sum(len(k['offen']) for k in karten)

    blaetter = []
    for i, k in enumerate(karten):
        kid, a = k['id'], abgl[k['id']]
        hell = i % 2 == 0
        w1, w2 = WORT[kid]
        fname, falt = FOTO[kid]
        innen = (PAKET / 'bilder' / f'{kid}-innen.png').exists()
        quer = stand[kid]['karte']['format'][0] > stand[kid]['karte']['format'][1]
        ab_kl = ' rot' if k['abweichungen'] else ''
        offen = ''.join(f'<li>{e(o)}</li>' for o in k['offen'])
        blaetter.append(f'''
<section class="kb blatt {'hell' if hell else 'dunkel'}" id="{kid}" aria-label="{e(k['name'])}"><span class="hz" aria-hidden="true"></span><div class="innen kb__g">
  <div class="kb__t" data-a>
    <p class="mono">{e(stand[kid]['karte']['gruppe'])} · {k['seiten_pdf']} {'Seite' if k['seiten_pdf'] == 1 else 'Seiten'} A4{' quer' if quer else ''}</p>
    <h2>{e(w1)} <em>{e(w2)}</em></h2>
    <dl class="zahlen">
      <div><dt>Einträge</dt><dd>{k['eintraege']}</dd></div>
      <div><dt>Preise</dt><dd>{k['preise']}</dd></div>
      <div><dt>Wörter Original · Daten</dt><dd>{a['woerter_original']} · {a['woerter_daten']}</dd></div>
      <div class="{ab_kl}"><dt>Abweichungen</dt><dd>{k['abweichungen']}</dd></div>
    </dl>
    <p class="beleg">{'Neue PDF Wort für Wort gleich den Daten.' if k['pdf_gleich_daten'] else 'Neue PDF weicht von den Daten ab.'} Gelesen aus <a href="../../{e(k['original'])}" target="_blank" rel="noopener">{e(pathlib.Path(k['original']).name)}</a>.</p>
    <div class="pr__k"><a class="knopf{'' if hell else ' knopf--dunkel'}" href="../../_karten/pdf/{kid}.pdf" target="_blank" rel="noopener">Neue PDF {pf}</a>
      <a class="leise" href="../../{e(k['original'])}" target="_blank" rel="noopener">Original</a>
      <a class="leise" href="../../_karten/stand/{kid}.json" target="_blank" rel="noopener">Daten</a></div>
    <details class="offen"><summary class="mono">{ZAHLWORT.get(len(k['offen']), len(k['offen']))} {'Punkt' if len(k['offen']) == 1 else 'Punkte'} offen</summary><ul>{offen}</ul></details>
  </div>
  <div class="kb__b{' quer' if quer else ''}" data-a>
    <figure class="seite"><a href="../../_karten/pdf/{kid}.pdf" target="_blank" rel="noopener"><img src="bilder/{kid}.png" alt="Erste Seite der neuen PDF «{e(k['name'])}»" loading="lazy"></a></figure>
    {f'<figure class="seite zwei"><img src="bilder/{kid}-innen.png" alt="Zweite Seite der neuen PDF «{e(k["name"])}»" loading="lazy"></figure>' if innen else ''}
    <figure class="foto"><img src="{foto(fname)}" alt="{e(falt)}" loading="lazy"></figure>
  </div>
</div></section>''')

    code = e("<div id=\"karte\"></div>\n<script src=\"../_karten/karte.js\"></script>\n<script>SchloessliKarte.lade('#karte', '../_karten/stand/speisekarte.json')</script>")
    seite = f'''<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Karten · Wirtschaft am Schlössli</title><meta name="description" content="Station 10, Kartenmacher: alle Karten des Hauses als Daten mit PDF, gegen das Original geprüft.">
<link rel="icon" href="../05-markenbauer/marke/zeichen/zeiger.svg"><style>{stil}
.kb{{position:relative;padding:clamp(90px,10vw,140px) 0;overflow:hidden}}
.kb .hz{{top:clamp(150px,15vw,210px)}}
.kb__g{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:clamp(28px,5vw,80px);align-items:start;position:relative}}
.kb h2{{font:400 clamp(1.6rem,3vw,2.6rem)/1.2 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:14px 0 26px;color:var(--titel-h)}}
.kb h2 em{{font-style:normal;color:var(--ak-t)}}
.kb .mono{{color:var(--ak-t)}}
.dunkel.kb h2{{color:#F2F5F5}}.dunkel.kb h2 em{{color:var(--ak-titel)}}.dunkel.kb .mono{{color:var(--ak-h)}}
.zahlen{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:0 0 22px}}
.zahlen div{{padding:16px 18px;border-radius:18px;background:var(--kalk2);box-shadow:inset 0 2px 6px rgba(4,27,35,.14),inset 0 -1px 0 rgba(255,255,255,.7)}}
.dunkel .zahlen div{{background:var(--tief);box-shadow:inset 0 2px 8px rgba(0,0,0,.45),inset 0 -1px 0 rgba(255,255,255,.06)}}
.zahlen dt{{font:400 10.5px/1.3 var(--mono);letter-spacing:.15em;text-transform:uppercase;opacity:.8}}
.zahlen dd{{margin:6px 0 0;font:400 clamp(1.25rem,2vw,1.75rem)/1 var(--titel);letter-spacing:.04em;white-space:nowrap}}
.zahlen .rot dd{{color:var(--signal)}}
.beleg{{font-size:15px;opacity:.86;margin:0 0 26px}}
.offen{{margin-top:28px}}
.offen summary{{cursor:pointer;list-style:none;display:inline-flex;align-items:center;gap:10px}}
.offen summary::before{{content:"";width:8px;height:8px;border-radius:50%;background:var(--signal)}}
.offen ul{{margin:14px 0 0;padding-left:18px;font-size:15px;line-height:1.5}}
.offen li{{margin-bottom:8px}}
.kb__b{{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}}
.kb__b figure{{margin:0;border-radius:var(--rund);overflow:hidden}}
.kb__b .seite{{background:#fff;box-shadow:0 40px 70px -40px rgba(0,0,0,.55),0 0 0 1px rgba(4,27,35,.08)}}
.kb__b .seite img{{width:100%;height:auto}}
.dunkel .kb__b .seite{{box-shadow:0 40px 70px -40px rgba(0,0,0,.8),0 0 0 1px color-mix(in srgb,var(--ak) 55%,transparent)}}
.kb__b .zwei{{margin-top:48px}}
.kb__b .foto{{grid-column:1 / -1;box-shadow:0 50px 80px -50px rgba(0,0,0,.6)}}
.kb__b .foto img{{width:100%;aspect-ratio:16/7;object-fit:cover}}
.kb__b.quer .seite{{grid-column:1 / -1}}
.web{{position:relative;padding:clamp(90px,10vw,140px) 0}}
.web__g{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(28px,5vw,80px);align-items:start}}
.web h2{{font:400 clamp(1.6rem,3vw,2.6rem)/1.2 var(--titel);text-transform:uppercase;letter-spacing:.16em;margin:14px 0 22px;color:var(--titel-h)}}
.web h2 em{{font-style:normal;color:var(--ak-t)}}
.web .mono{{color:var(--ak-t)}}
.web pre{{margin:0;padding:24px;border-radius:22px;background:var(--nacht);box-shadow:inset 0 2px 10px rgba(0,0,0,.5);font:400 13px/1.6 var(--mono);color:#DCE8EA;white-space:pre-wrap;word-break:break-word}}
.web ul{{margin:22px 0 0;padding-left:18px}}
.web code{{font-family:var(--mono);font-size:13px}}
.inhalt{{display:flex;flex-wrap:wrap;gap:10px 24px;margin:34px 0 0;padding:0;list-style:none}}
.inhalt a{{font:400 .9rem/1.2 var(--titel);text-transform:uppercase;letter-spacing:.2em;text-decoration:none;color:#F2F5F5;border-bottom:1px solid var(--ak);padding-bottom:4px}}
@media(max-width:900px){{.kb__g,.web__g{{grid-template-columns:1fr}}.kb .hz{{display:none}}}}
@media(max-width:520px){{.zahlen{{grid-template-columns:1fr 1fr}}.zahlen div{{padding:12px 14px}}.kb__b .zwei{{margin-top:24px}}}}
</style></head><body data-welt="a">
<section class="pr dunkel" aria-label="Karten des Hauses"><span class="hz" aria-hidden="true"></span><div class="innen pr__g">
  <figure class="pr__bild" data-a><img src="{foto('tortelloni')}" alt="Tortelloni mit Tomate, Burrata und Taggiasca-Olive"></figure>
  <div class="pr__t" data-a>
    {zeichen}
    <p class="mono">Station 10 · Kartenmacher · 19.10.2026</p>
    <h1>Die Karten <em>des Hauses.</em></h1>
    <p class="l">{ZAHLWORT[len(karten)]} Karten aus den PDF der heutigen Website, Wort für Wort und Zahl für Zahl gegen das Original gelesen: {gesamt_e} Einträge, {gesamt_p} Preise, {gesamt_ab} Abweichungen. Aus diesen Daten lesen La Carte, die Website und die neuen PDF.</p>
    <div class="pr__k"><a class="knopf" href="#speisekarte">Zu den Karten {pf}</a><a class="leise" href="pruefung.md" target="_blank" rel="noopener">Prüfbericht</a><a class="leise" href="../../_karten/haus.json" target="_blank" rel="noopener">Alle Daten</a></div>
    <ul class="inhalt">{''.join(f'<li><a href="#{k["id"]}">{e(k["name"])}</a></li>' for k in karten)}</ul>
  </div>
</div></section>
{''.join(blaetter)}
<section class="web blatt hell" id="website" aria-label="Für die Website"><div class="innen web__g">
  <div data-a><p class="mono">Für Station 14 · eine Quelle</p><h2>Die Website liest <em>dieselben Daten.</em></h2>
    <p>Jede Karte liegt als eigene Datei unter <code>_karten/stand/</code>. Ein Satz zeichnet sie in eine Seite, Schrift und Farbe kommen aus der Seite selbst. Ändert sich eine Karte, wird nur die Datei getauscht; PDF und Website stimmen danach überein.</p>
    <ul>{''.join(f'<li><code>_karten/stand/{k["id"]}.json</code></li>' for k in karten)}</ul></div>
  <div data-a><pre>{code}</pre><p class="beleg" style="margin-top:18px">La Carte liest alle Karten als ein Dokument: <code>_karten/haus.json</code> (Haus «schloessli», geprüft mit dem Datenmodell von La Carte).</p></div>
</div></section>
<footer class="pfuss dunkel"><p>Station 10 der Kette · Designstudie von Tasty Studios, nicht die offizielle Website · Karten und Fotos: Wirtschaft am Schlössli · {offen_n} Punkte offen</p></footer>
<script>document.documentElement.classList.add('js');(function(){{var g=document.querySelector('.pr__bild'),s=document.querySelector('.pr');
function setz(){{var r=g.getBoundingClientRect(),q=s.getBoundingClientRect();s.style.setProperty('--h-bild',r.height+'px');s.style.setProperty('--h-oben',(r.top-q.top)+'px')}}
setz();addEventListener('resize',setz);if(document.fonts)document.fonts.ready.then(setz);
var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('da');io.unobserve(x.target)}}}})}},{{threshold:.2}});
document.querySelectorAll('[data-a],.hz').forEach(function(h){{io.observe(h)}})}})()</script>
</body></html>'''
    (PAKET / 'karten.html').write_text(seite)
    print('karten.json, pruefung.md, bilder/, karten.html geschrieben ·', len(karten), 'Karten ·', gesamt_e, 'Einträge ·', gesamt_ab, 'Abweichungen')


if __name__ == '__main__':
    main()
