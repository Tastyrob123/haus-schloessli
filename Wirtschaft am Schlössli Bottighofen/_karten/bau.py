# bau.py · druckt jede Karte aus ihren Daten (_karten/stand/<id>.json) als PDF im Stil des Hauses.
# Farben: wie die fertige Website, Farbwelt «Ton in Ton» aus dem Platzteller (Robert 19.10.2026, UEBERGABE.md des Projekts;
#   Werte gemessen am 19.10.2026 mit getComputedStyle auf website/weinkarte.html). Schrift wie Website und Markenbuch:
#   Titel Open Sans in Versalien, Lauftext Instrument Sans, Kürzel DM Mono, als feste Schnitte (schriften.py, kein «Type 3»).
# Lehren aus den anderen Häusern (Master Website-Bau Abschnitt 8 und Lernprotokoll 11./12./14.10.2026):
#   Lesetext nicht unter 11 pt · Titel gut doppelt so gross wie der Lesetext · gleiche Seitenzahl wie das Original, Seiten gefüllt,
#   freie Höhe je Zwischenraum höchstens 6 mm, der Rest an den Fuss · kein Gericht allein, keine Rubrik ohne ihr erstes Gericht ·
#   Menüs ohne Preise je Gericht ganz mittig, senkrecht und waagrecht · ein Format für jeden Eintrag · keine weichen Schatten,
#   keine CSS-Masken, Zeichen als Pfad, dunkle Fläche als SVG · kein «1 von 2».
# Ein Satz für alles: satz/<id>.html ist die Seite, die gedruckt wird. Danach liest pruefe_pdf() die PDF wieder aus und vergleicht
# Wort für Wort mit den Daten; dazu die Regeln je Seite und die Schriftart.
# Lauf: python3 _karten/bau.py [id …]   →   _karten/pdf/<id>.pdf, _karten/satz/*.html, _karten/bilder/<id>.png, druckbericht.json
import base64, collections, html, json, pathlib, re, subprocess, sys

HIER = pathlib.Path(__file__).resolve().parent
PROJ = HIER.parent
MARKE = PROJ / '_kette' / '05-markenbauer' / 'marke'
SATZ, PDF, BILD, SCHRIFT = HIER / 'satz', HIER / 'pdf', HIER / 'bilder', HIER / 'schriften'
HAUS, ORT = 'Wirtschaft am Schlössli', 'Bottighofen'
NODE_PATH = str(pathlib.Path.home() / 'Aussen-Pruefung' / 'node_modules')

# Farbwelt der Website (Ton in Ton)
NACHT, TIEF, STUHL = '#0B1D3D', '#0A234C', '#113D88'
HIMMEL, HIMMEL_T, HIMMEL_H = '#A2B6CF', '#0F3678', '#C5D2E1'
TINTE, TITEL_H, LEISE = '#041023', '#0A2552', '#3B4A60'     # LEISE: --fg2 aus website/assets/css/fuss.css

SEITE_INNEN = {'hoch': 251, 'quer': 180}                    # nutzbare Höhe in mm (A4 minus Ränder, 4 mm Luft gegen Rundung beim Umbruch)
RAND = {'hoch': {'top': '22mm', 'bottom': '20mm', 'left': '22mm', 'right': '22mm'},
        'quer': {'top': '15mm', 'bottom': '12mm', 'left': '22mm', 'right': '22mm'}}


def b64(p):
    return base64.b64encode(p.read_bytes()).decode('ascii')


def zeichen_svg(farbe):
    return (MARKE / 'zeichen' / 'zeichen.svg').read_text().replace('fill="currentColor"', f'fill="{farbe}"', 1)


def schrift(fam, datei, g):
    return f"@font-face{{font-family:'{fam}';src:url(data:font/ttf;base64,{b64(SCHRIFT / datei)}) format('truetype');font-weight:{g}}}"


SCHRIFTEN = ''.join([schrift('Titel', 'OpenSans-Light.ttf', 300), schrift('Titel', 'OpenSans-Regular.ttf', 400),
                     schrift('Lauf', 'InstrumentSans-Regular.ttf', 400), schrift('Lauf', 'InstrumentSans-SemiBold.ttf', 600),
                     schrift('Mono', 'DMMono-Regular.ttf', 400)])
TAPETE = 'data:image/svg+xml;base64,' + base64.b64encode((MARKE / 'tapete-a-dunkel.svg').read_text().replace('#A2C6CF', HIMMEL).encode()).decode()

STIL = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font:400 11pt/1.4 Lauf,sans-serif;color:{TINTE};background:#fff}}
.vers{{font-family:Titel,sans-serif;font-weight:400;text-transform:uppercase}}
/* Umschlag: dunkle Fläche als SVG, erscheint auch ohne «Hintergrund drucken» */
.umschlag{{position:relative;color:#F2F5F9;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;overflow:hidden}}
.umschlag>svg.grund{{position:absolute;inset:0;width:100%;height:100%}}
.umschlag>*:not(.grund){{position:relative}}
.umschlag .z{{width:32mm}}
.umschlag .z svg{{width:100%;height:auto;display:block}}
.umschlag .haus{{font-size:10pt;letter-spacing:.3em;color:{HIMMEL_H};margin-top:12mm}}
.umschlag .linie{{width:100%;height:.6pt;background:{HIMMEL};margin:10mm 0}}
.umschlag h1{{font-size:32pt;letter-spacing:.16em;font-weight:300}}
.umschlag .ort{{position:absolute;bottom:20mm;left:0;right:0;font-size:8.5pt;letter-spacing:.3em;color:{HIMMEL_H}}}
/* Seiten mit festem Umbruch (wie das Original) */
.seite{{display:flex;flex-direction:column;break-after:page;overflow:hidden}}
.seite:last-child{{break-after:auto}}
.block{{break-inside:avoid}}
.rubrik{{text-align:center;margin:0 0 7mm}}
.rubrik h2{{font-size:23pt;line-height:1.15;letter-spacing:.16em;color:{TITEL_H};font-weight:300}}
.rubrik .linie{{height:.6pt;background:{HIMMEL};margin-top:4mm}}
.g{{display:grid;grid-template-columns:1fr auto;column-gap:10mm;margin:0 0 5.2mm;break-inside:avoid}}
.g .n{{font-size:12.5pt;line-height:1.3;letter-spacing:.09em}}
.g .k{{font-family:Mono,monospace;font-size:7.6pt;letter-spacing:.08em;color:{HIMMEL_T};margin-left:3mm;text-transform:none}}
.g .t{{grid-column:1;font-size:11pt;line-height:1.38}}
.g .p{{grid-column:2;grid-row:1 / span 4;text-align:right;white-space:nowrap;font-family:Titel,sans-serif;font-size:13pt;line-height:1.3;color:{TITEL_H}}}
.g .p span{{display:block}}
.g .p i{{font-style:normal;font-family:Lauf,sans-serif;font-size:8.6pt;color:{LEISE};margin-left:2mm;letter-spacing:.02em}}
.notiz{{text-align:center;font-size:9.6pt;line-height:1.45;color:{LEISE};margin:3mm auto 0;max-width:150mm}}
.fuss-notiz{{margin-top:auto;padding-top:4mm}}
/* Weinkarte: drei Ebenen (Farbe als Rubrik, Land in der Titelschrift, Region als Mono-Etikett), darunter das Weingut */
.wk .rubrik{{break-before:page}}
.wk .rubrik:first-child{{break-before:auto}}
.land{{font-size:15pt;letter-spacing:.16em;color:{TITEL_H};text-align:center;margin:7mm 0 3.6mm;break-after:avoid;font-weight:300}}
.zw{{font-family:Mono,monospace;font-size:8.6pt;letter-spacing:.2em;text-transform:uppercase;color:{HIMMEL_T};text-align:center;margin:5.4mm 0 2.6mm;break-after:avoid}}
.gut{{font-weight:600;font-size:11.5pt;margin:4.4mm 0 1.4mm;break-after:avoid}}
.w{{display:grid;grid-template-columns:12mm 1fr auto 14mm 13mm;column-gap:2.6mm;font-size:11pt;line-height:1.42;break-inside:avoid;font-variant-numeric:tabular-nums lining-nums}}
.w .j{{color:{HIMMEL_T}}}
.w .e{{font-size:9.4pt;color:{LEISE};text-align:right}}
.w .p{{font-family:Titel,sans-serif;text-align:right;color:{TITEL_H}}}
.w .x{{grid-column:2 / span 2;font-size:9.6pt;color:{LEISE};line-height:1.35}}
/* Menüs ohne Preis je Gericht: ganz mittig */
.quer{{display:grid;grid-template-columns:58mm 1fr 58mm;align-items:center}}
.menue{{text-align:center;display:flex;flex-direction:column;align-items:center}}
.menue .rubrik{{width:100%;margin-bottom:5mm}}
.menue .rubrik .linie{{margin-top:3mm}}
.menue .rubrik h2{{font-size:22pt}}
.menue .g{{display:block;margin:0}}
.menue .g .n{{font-family:Titel,sans-serif;font-size:13pt;line-height:1.25;letter-spacing:.04em;text-transform:none}}
.menue .g .t{{font-size:11pt;line-height:1.3}}
.menue .stern{{font-family:Mono,monospace;font-size:9pt;letter-spacing:.06em;color:{HIMMEL};margin:var(--stern,1.4mm) 0;line-height:1}}
.menue .notiz{{margin-top:5mm;font-size:10.5pt;color:{TITEL_H}}}
.menue.gross .rubrik h2{{font-size:26pt}}
.menue.gross .g .n{{font-size:17pt}}
.menue.gross .g .t{{font-size:12.5pt}}
.menue.gross .notiz{{font-size:12pt}}
.gross-gruss .gruss{{font-size:12pt}}
.gruss{{font-family:Titel,sans-serif;text-transform:uppercase;letter-spacing:.18em;font-size:10.5pt;line-height:1.8;color:{HIMMEL_T};text-align:center;font-weight:300}}
"""

# Freie Höhe verteilen, je Zwischenraum höchstens 6 mm, Rest an den Fuss (GBR packe(), 11.10.2026); Überlauf ist ein Fehler
VERTEILEN = """
<script>
(function(){
  var mm = 96 / 25.4, fehler = [];
  document.querySelectorAll('.seite').forEach(function(s, i){
    var voll = s.scrollHeight - s.clientHeight;
    if (voll > 1) { fehler.push('Seite ' + (i + 1) + ' läuft über (' + Math.round(voll / mm) + ' mm)'); return; }
    var oben = s.getBoundingClientRect().top, unten = 0;
    [].forEach.call(s.querySelectorAll('.block'), function(k){ unten = Math.max(unten, k.getBoundingClientRect().bottom - oben); });
    var fuss = s.querySelector('.fuss-notiz'), fh = fuss ? fuss.offsetHeight : 0;
    var frei = s.clientHeight - unten - fh, luecken = s.querySelectorAll('.g').length + s.querySelectorAll('.block').length;
    if (frei > 0 && luecken > 1) { s.style.setProperty('--plus', Math.min(frei / luecken, 6 * mm) + 'px'); s.classList.add('verteilt'); }
    if (s.scrollHeight - s.clientHeight > 1) { s.classList.remove('verteilt'); }
  });
  document.querySelectorAll('.menue').forEach(function(m){
    var h = m.parentNode.clientHeight, i = m.scrollHeight, n = m.querySelectorAll('.stern').length;
    if (i > h + 1) fehler.push('Menü läuft über');
    else if (n) m.style.setProperty('--stern', Math.min(1.4 * mm + (h - i) * 0.5 / (2 * n), 7 * mm) + 'px');
  });
  window.SATZ_FEHLER = fehler;
})();
</script>
<style>.verteilt .g{margin-bottom:calc(5.2mm + var(--plus))}.verteilt .block{margin-bottom:var(--plus)}</style>
"""


def esc(s):
    return html.escape(s, quote=False)


def posten_von(karte):
    return [p for t in karte['teile'] if t['art'] == 'inhalt' for p in t['posten'] if not p.get('aus')]


def gericht(p, menue=False):
    k = f'<span class="k">{esc(p["zusatz"])}</span>' if p.get('zusatz') else ''
    zeilen = ''.join(f'<p class="t">{esc(z["text"])}</p>' for z in p.get('zeilen', []))
    preise = ''
    if p.get('preise'):
        ein = p.get('einheiten') or [''] * len(p['preise'])
        preise = '<p class="p">' + ''.join(f'<span>{esc(pr)}{f"<i>{esc(e)}</i>" if e else ""}</span>' for pr, e in zip(p['preise'], ein)) + '</p>'
    return f'<div class="g"><p class="n{"" if menue else " vers"}">{esc(p["name"])}{k}</p>{preise}{zeilen}</div>'


def wein(p):
    erste = (f'<span class="j">{esc(p.get("jahr", ""))}</span><span>{esc(p["name"])}</span>'
             f'<span class="e">{esc(p.get("zusatz", ""))}</span><span class="e">{esc(p["einheiten"][0])}</span><span class="p">{esc(p["preise"][0])}</span>')
    x = ''.join(f'<span></span><span class="x">{esc(z["text"])}</span><span></span><span></span>' for z in p.get('zeilen', []))
    weitere = ''.join(f'<span></span><span></span><span></span><span class="e">{esc(e)}</span><span class="p">{esc(pr)}</span>' for pr, e in zip(p['preise'][1:], p['einheiten'][1:]))
    return f'<div class="w">{erste}{x}{weitere}</div>'


def rubrik(titel):
    return f'<div class="rubrik"><h2 class="vers">{esc(titel)}</h2><div class="linie"></div></div>'


def seiten_fest(karte):
    """À-la-carte-Karten: dieselben Seiten wie das Original (Feld «s»), jede Rubrik mit ihren Gerichten als ein Block,
    Erläuterungen am Ende einer Seite stehen am Fuss."""
    seiten, akt_s = collections.OrderedDict(), 1
    for p in posten_von(karte):
        if p['t'] == 'rubrik':
            akt_s = p.get('s', 1)                     # eine Rubrik bleibt ganz auf der Seite, auf der sie im Original beginnt
        seiten.setdefault(akt_s, []).append(p)
    out = []
    for ps in seiten.values():
        n_fuss = 0
        while n_fuss < len(ps) and ps[len(ps) - 1 - n_fuss]['t'] == 'notiz':
            n_fuss += 1
        haupt, fuss = ps[:len(ps) - n_fuss], ps[len(ps) - n_fuss:]
        bloecke, akt = [], []
        for p in haupt:
            if p['t'] == 'rubrik':
                if akt: bloecke.append(akt)
                akt = [rubrik(p['titel'])]
            elif p['t'] == 'gericht':
                akt.append(gericht(p))
            elif p['t'] == 'notiz':
                akt.append(f'<p class="notiz">{esc(p["text"])}</p>')
        if akt: bloecke.append(akt)
        innen_ = ''.join('<section class="block">' + ''.join(b) + '</section>' for b in bloecke)
        if fuss:
            innen_ += '<div class="fuss-notiz">' + ''.join(f'<p class="notiz">{esc(p["text"])}</p>' for p in fuss) + '</div>'
        out.append(f'<div class="seite" style="height:{SEITE_INNEN["hoch"]}mm">{innen_}</div>')
    return ''.join(out)


def weinkarte(karte):
    teile, block = [], []

    def zu():
        if block:
            teile.append('<div class="block">' + ''.join(block) + '</div>'); block.clear()
    for p in posten_von(karte):
        t = p['t']
        if t == 'rubrik':
            zu(); teile.append(rubrik(p['titel']))
        elif t == 'land':
            zu(); teile.append(f'<p class="land vers">{esc(p["text"])}</p>')
        elif t == 'zw' and p.get('weingut'):
            zu(); block.append(f'<p class="gut">{esc(p["text"])}</p>')
        elif t == 'zw':
            zu(); teile.append(f'<p class="zw">{esc(p["text"])}</p>')
        elif t == 'gericht':
            if block and len(block) < 7:
                block.append(wein(p))                       # Weingut mit seinen ersten Weinen bleibt zusammen
            else:
                zu(); teile.append(wein(p))
        elif t == 'notiz':
            zu(); teile.append(f'<p class="notiz">{esc(p["text"])}</p>')
    zu()
    return '<div class="wk">' + ''.join(teile) + '</div>'


def menue(karte):
    """Eine Seite quer: Lunch und Anlass-Menü, ganz mittig wie im Original, der Gruss des Hauses links."""
    gruss, mitte = '', []
    for p in posten_von(karte):
        if p['t'] == 'rubrik':
            mitte.append(rubrik(p['titel']))
        elif p['t'] == 'frei' and p['zeilen'][0]['text'] != '***':
            gruss = '<p class="gruss">' + esc(p['zeilen'][0]['text']) + '</p>'
        elif p['t'] == 'frei':
            mitte.append('<p class="stern">***</p>')
        elif p['t'] == 'gericht':
            mitte.append(gericht(p, menue=True))
        elif p['t'] == 'notiz':
            mitte.append(f'<p class="notiz">{esc(p["text"])}</p>')
    gross = sum(1 for p in posten_von(karte) if p['t'] == 'gericht') <= 5        # kurzes Menü: grösser, damit die Seite gefüllt ist
    return (f'<div class="quer{" gross-gruss" if gross else ""}" style="height:{SEITE_INNEN["quer"]}mm"><div>{gruss}</div>'
            f'<div class="menue{" gross" if gross else ""}">{"".join(mitte)}</div><div></div></div>')


def dokument(karte, koerper, rand=''):
    return (f'<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><title>{esc(karte["name"])} · {esc(HAUS)}</title>'
            f'<style>{rand}{SCHRIFTEN}{STIL}</style></head><body>{koerper}</body></html>')


def umschlag(karte):
    b, h = karte['format']
    d = next(t for t in karte['teile'] if t['art'] == 'deckel')
    grund = (f'<svg class="grund" viewBox="0 0 {b} {h}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">'
             f'<defs><pattern id="tp" width="22.2" height="22.2" patternUnits="userSpaceOnUse"><image href="{TAPETE}" width="22.2" height="22.2"/></pattern></defs>'
             f'<rect width="{b}" height="{h}" fill="{NACHT}"/><rect width="{b}" height="{h}" fill="url(#tp)"/></svg>')
    k = (f'<section class="umschlag" style="width:{b}mm;height:{h}mm">{grund}<div class="z">{zeichen_svg(HIMMEL)}</div>'
         f'<p class="haus vers">{esc(HAUS)}</p><div class="linie"></div><h1 class="vers">{esc(d["titel"])}</h1><p class="ort vers">{esc(ORT)}</p></section>')
    return dokument(karte, k, '@page{size:%smm %smm;margin:0}' % (b, h))


def innen(karte):
    if karte['format'][0] > karte['format'][1]:
        k = menue(karte)
    elif karte.get('kl') == 'wein':
        k = weinkarte(karte)
    else:
        k = seiten_fest(karte)
    return dokument(karte, '<main>' + k + '</main>' + VERTEILEN)


def kopf_fuss(karte):
    z = 'data:image/svg+xml;base64,' + base64.b64encode(zeichen_svg(HIMMEL_T).encode()).decode()
    fs = schrift('Lauf', 'InstrumentSans-Regular.ttf', 400)
    kopf = (f'<div style="width:100%;padding:0 22mm;display:flex;align-items:center;justify-content:center;gap:2.6mm;'
            f'font:7.2pt Lauf,sans-serif;letter-spacing:.3em;text-transform:uppercase;color:{HIMMEL_T}"><style>{fs}</style>'
            f'<img src="{z}" style="height:4.6mm"><span>{esc(HAUS)}</span></div>')
    fuss_text = ' · '.join(esc(f) for f in karte.get('fuss', '').split(' · ') if f)
    nummer = '<span class="pageNumber"></span>' if karte.get('kl') == 'wein' else ''
    fuss = (f'<div style="width:100%;padding:0 22mm;display:flex;justify-content:space-between;gap:8mm;font:7.4pt Lauf,sans-serif;color:{LEISE}">'
            f'<style>{fs}</style><span>{fuss_text}</span><span>{nummer}</span></div>')
    return kopf, fuss


DRUCK_JS = r"""
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const auftraege = JSON.parse(fs.readFileSync(0, 'utf8'));
  const b = await chromium.launch({ headless: true });
  const fehler = [];
  for (const a of auftraege) {
    // der Satz misst in der Breite der bedruckten Fläche, im Druckmodus
    const p = await b.newPage({ viewport: { width: Math.round(a.breite_mm * 96 / 25.4), height: 1200 } });
    p.on('pageerror', e => fehler.push(a.html + ': ' + e));
    await p.emulateMedia({ media: 'print' });
    await p.goto('file://' + a.html, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const satz = await p.evaluate(() => window.SATZ_FEHLER || []);
    satz.forEach(f => fehler.push(a.html.split('/').pop() + ': ' + f));
    const o = { path: a.pdf, width: a.b + 'mm', height: a.h + 'mm', printBackground: true };
    if (a.kopf) Object.assign(o, { displayHeaderFooter: true, headerTemplate: a.kopf, footerTemplate: a.fuss, margin: a.rand });
    else Object.assign(o, { preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    await p.pdf(o);
    await p.close();
  }
  await b.close();
  process.stdout.write(JSON.stringify({ fehler }));
})();
"""


def drucke(auftraege):
    js = HIER / '.druck.js'
    js.write_text(DRUCK_JS)
    r = subprocess.run(['node', str(js)], input=json.dumps(auftraege), capture_output=True, text=True,
                       env={'NODE_PATH': NODE_PATH, 'PATH': '/opt/homebrew/bin:/usr/bin:/bin'}, timeout=600)
    if r.returncode:
        raise SystemExit('Druck: ' + r.stderr[-1500:])
    aus = json.loads(r.stdout)
    if aus['fehler']:
        raise SystemExit('Satz: ' + ' · '.join(aus['fehler']))


def pruefe_pdf(e, pdf):
    """Die fertige PDF Wort für Wort gegen die Daten, dazu die Umbruchregeln je Seite und die Schriftart."""
    k = e['karte']
    roh = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True, text=True, check=True).stdout
    seiten = roh.split('\f')
    weg = {f for f in k.get('fuss', '').split(' · ') if f}
    ow = []
    for s in seiten:
        for z in s.splitlines():
            z = re.sub(r'\s+', ' ', z).strip()
            if z.replace(' ', '') in (HAUS.upper().replace(' ', ''), ORT.upper().replace(' ', '')):
                continue                                         # Kopf jeder Seite und Ort auf dem Umschlag, gesperrt gesetzt
            for w in weg:
                z = z.replace(w, ' ')
            z = z.replace(' · ', ' ').strip()
            if z and z != '·':
                ow += z.split()
    dw = []
    for t in k['teile']:
        if t['art'] == 'deckel':
            dw += t['titel'].split(); continue
        for p in t['posten']:
            if p.get('aus'):
                continue
            for f in ('jahr', 'name', 'zusatz', 'titel', 'text'):
                if isinstance(p.get(f), str):
                    dw += p[f].split()
            for z in p.get('zeilen', []):
                dw += z['text'].split()
            for i, pr in enumerate(p.get('preise', [])):
                dw.append(pr)
                if p.get('einheiten') and p['einheiten'][i]:
                    dw += p['einheiten'][i].split()
    o, d = collections.Counter(w.upper() for w in ow), collections.Counter(w.upper() for w in dw)   # Versalien sind Satz, nicht Text
    fehlt, dazu = sorted((d - o).elements()), sorted((o - d).elements())
    if k.get('kl') == 'wein':                                    # Seitenzahlen im Fuss der Weinkarte
        nummern = collections.Counter(str(i) for i in range(1, len(seiten) + 1))
        rest = collections.Counter(dazu) - nummern
        dazu = sorted(rest.elements())
    namen = {p['name'].upper() for p in posten_von(k) if p['t'] == 'gericht'}
    kopf = {(p.get('text') or p.get('titel')).upper() for p in posten_von(k) if p['t'] in ('rubrik', 'land', 'zw')}
    regeln = []
    for nr, s in enumerate(seiten, 1):
        if not s.strip():
            continue
        t = re.sub(r'\s+', ' ', s).upper()
        if sum(1 for n in namen if n in t) == 1 and len(namen) > 1:
            regeln.append(f'Seite {nr}: nur ein Eintrag auf der Seite')
        z = [re.sub(r'\s+', ' ', x).strip() for x in s.splitlines() if x.strip()]
        z = [x for x in z if not re.fullmatch(r'\d{1,2}', x) and x not in weg and not x.startswith('Alle ')]
        if z and z[-1].upper() in kopf:
            regeln.append(f'Seite {nr}: endet mit dem Titel «{z[-1]}»')
    if k['format'][0] < k['format'][1] and k.get('kl') != 'wein':   # Seiten wie im Original: jeder Eintrag auf «seiner» Seite
        versatz = 1 if any(t['art'] == 'deckel' for t in k['teile']) else 0
        seite_von, akt_s = {}, 1
        for p in posten_von(k):
            if p['t'] == 'rubrik':
                akt_s = p.get('s', 1)
            seite_von[id(p)] = akt_s
        for p in posten_von(k):
            if p['t'] == 'gericht':
                nr = seite_von[id(p)] + versatz
                if nr > len(seiten) or not all(w in seiten[nr - 1].upper().split() for w in p['name'].upper().split()):
                    regeln.append(f'«{p["name"]}» steht nicht auf Seite {nr} wie im Original')
    if 'Type 3' in subprocess.run(['pdffonts', str(pdf)], capture_output=True, text=True).stdout:
        regeln.append('Schrift als «Type 3» in der PDF')
    return {'seiten': len([s for s in seiten if s.strip()]), 'fehlt_in_pdf': fehlt, 'dazu_in_pdf': dazu, 'regeln': regeln}


def bild(pdf, ziel):
    subprocess.run(['pdftoppm', '-r', '60', '-png', '-f', '1', '-l', '1', '-singlefile', str(pdf), str(ziel.with_suffix(''))], check=True)


if __name__ == '__main__':
    for d in (SATZ, PDF, BILD):
        d.mkdir(exist_ok=True)
    ids = sys.argv[1:] or [p.stem for p in sorted((HIER / 'stand').glob('*.json'))]
    auftraege, plan = [], []
    for kid in ids:
        e = json.loads((HIER / 'stand' / f'{kid}.json').read_text())
        k = e['karte']
        b, h = k['format']
        art = 'quer' if b > h else 'hoch'
        (SATZ / f'{kid}.html').write_text(innen(k))
        kopf, fuss = kopf_fuss(k)
        auftraege.append({'html': str(SATZ / f'{kid}.html'), 'pdf': str(SATZ / f'{kid}-innen.pdf'), 'b': b, 'h': h, 'kopf': kopf, 'fuss': fuss,
                          'rand': RAND[art], 'breite_mm': b - 44})
        teile = []
        if any(t['art'] == 'deckel' for t in k['teile']):
            (SATZ / f'{kid}-umschlag.html').write_text(umschlag(k))
            auftraege.append({'html': str(SATZ / f'{kid}-umschlag.html'), 'pdf': str(SATZ / f'{kid}-umschlag.pdf'), 'b': b, 'h': h, 'breite_mm': b})
            teile.append(SATZ / f'{kid}-umschlag.pdf')
        teile.append(SATZ / f'{kid}-innen.pdf')
        plan.append((e, teile))
    drucke(auftraege)
    bericht = {}
    for e, teile in plan:
        ziel = PDF / f'{e["id"]}.pdf'
        if len(teile) > 1:
            subprocess.run(['pdfunite', *map(str, teile), str(ziel)], check=True)
        else:
            ziel.write_bytes(teile[0].read_bytes())
        for t in teile:
            t.unlink()
        r = pruefe_pdf(e, ziel)
        bild(ziel, BILD / f'{e["id"]}.png')
        bericht[e['id']] = r
        ok = not (r['fehlt_in_pdf'] or r['dazu_in_pdf'] or r['regeln'])
        print(f'{e["id"]:14} {r["seiten"]:3} Seiten · PDF gleich Daten: {"ja" if ok else "NEIN"}', '' if ok else json.dumps(r, ensure_ascii=False)[:700])
    alt = json.loads((HIER / 'druckbericht.json').read_text()) if (HIER / 'druckbericht.json').exists() else {}
    alt.update(bericht)
    (HIER / 'druckbericht.json').write_text(json.dumps(alt, ensure_ascii=False, indent=1) + '\n')
