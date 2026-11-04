#!/usr/bin/env python3
"""Material der Werkbank Schlössli: alle Dateien des Pakets in Ordnern, zum Ansehen und Herunterladen (Nachtbau 3./4.11.2026, Agent schloessli-werkbank-feed).
Aufbau wie material.py des Kits und material_mehr.py des Culinarium (Kopf, je Ordner Nummer, Name, Satz und die Dateien mit Vorschau), aber für sich
allein gebaut: Die Ordner sammeln ein, was die anderen Reviere gerade liefern (Pläne papier_plan.json, unterlagen.json, beigaben_plan.json,
postkarten_plan.json, sticker_plan.json und die Dateien in unterlagen/pdf, drucksachen/pdf, untersetzer/pdf, sticker/pdf, postkarten/pdf,
beigaben/pdf), dazu Zeichen und Logo aus dem Markenbuch (_werkzeuge/livre/dateien), die Ansichten der Website, der Feed und die Mails.
Grosse PDFs werden nicht doppelt abgelegt: der Eintrag zeigt auf die Datei an ihrem Platz in der Werkbank. Kopiert nach material/ wird nur,
was sonst nicht ausgeliefert wird (Zeichen und Logo, Ansichten, Bilder der Untersetzer und Sticker, die Texte zum Feed).
   python3 _werkbank/material_seite.py        (wiederholbar; am Ende des Baus noch einmal, um alle Ordner einzusammeln)"""
import glob, hashlib, html, json, os, re, shutil, subprocess

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)                       # website/_werkbank
WEB = os.path.dirname(ROOT)
HAUS = os.path.dirname(WEB)
ZIEL = os.path.join(ROOT, 'material')
VOR = os.path.join(ZIEL, '_vorschau')
KURZ = 'wirtschaft-am-schloessli'
N = 'Wirtschaft am Schlössli'
HJ = json.load(open(os.path.join(WEB, 'inhalt', 'haus.json'), encoding='utf-8'))
e = html.escape
STAND = '03.11.2026'


def plan(name):
    try:
        return json.load(open(os.path.join(HIER, name), encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def groesse(p):
    b = os.path.getsize(p)
    return f'{b / 1e6:.1f} MB'.replace('.', ',') if b >= 1e6 else f'{max(1, round(b / 1e3))} KB'


def vorschau(p):
    """Kleines Bild der Datei (PDF: erste Seite, Bild: verkleinert) in material/_vorschau, nach Inhalt benannt."""
    os.makedirs(VOR, exist_ok=True)
    h = hashlib.sha1(f'{os.path.relpath(p, ROOT)}:{int(os.path.getmtime(p))}'.encode()).hexdigest()[:12]
    z = os.path.join(VOR, h + '.webp')
    if not os.path.exists(z):
        from PIL import Image
        try:
            if p.lower().endswith('.pdf'):
                t = os.path.join(VOR, h)
                subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-scale-to', '220', '-png', '-singlefile', p, t], check=True, capture_output=True, timeout=120)
                im = Image.open(t + '.png'); os.remove(t + '.png')
            elif p.endswith('index.html') and os.path.exists(os.path.join(HIER, 'ansichten', 'Mails', os.path.basename(os.path.dirname(p))[:2] + '.jpg')):
                im = Image.open(os.path.join(HIER, 'ansichten', 'Mails', os.path.basename(os.path.dirname(p))[:2] + '.jpg'))   # Mail: ihr oberer Teil (mails/_src/aufnahme.js)
            elif p.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                im = Image.open(p)
            else:
                return None
            im = im.convert('RGBA'); im.thumbnail((220, 220))
            bg = Image.new('RGB', im.size, '#F4F6F9'); bg.paste(im, (0, 0), im)
            bg.save(z, 'WEBP', quality=80)
        except Exception:
            return None
    return '_vorschau/' + os.path.basename(z)


def kopie(ordner, quelle, name=None):
    d = os.path.join(ZIEL, ordner); os.makedirs(d, exist_ok=True)
    z = os.path.join(d, name or os.path.basename(quelle))
    if not os.path.exists(z) or os.path.getmtime(z) < os.path.getmtime(quelle):
        shutil.copy2(quelle, z)
    return z


def eintrag(name, pfad):
    """(Name, Weg von material/ aus, Pfad auf der Platte) – nur wenn die Datei da ist."""
    if not pfad or not os.path.exists(pfad):
        return None
    return (name, os.path.relpath(pfad, ZIEL).replace(os.sep, '/'), pfad)


def rest_name(stamm):
    s = stamm.replace(KURZ + '-', '').replace('-', ' ')
    return s[:1].upper() + s[1:]


def pdfs(ordner, liste):
    """Einträge aus einem Plan (id/ziel, name) und alle übrigen PDFs des Ordners."""
    d = os.path.join(ROOT, ordner, 'pdf')
    aus, genannt = [], set()
    for stamm, name in liste:
        p = os.path.join(d, stamm + '.pdf')
        if os.path.exists(p):
            aus.append(eintrag(name, p)); genannt.add(p)
    for p in sorted(glob.glob(os.path.join(d, '*.pdf'))):
        if p not in genannt:
            aus.append(eintrag(rest_name(os.path.basename(p)[:-4]), p))
    return [x for x in aus if x]


def ordner_liste():
    O = []
    U = plan('unterlagen.json') or []
    O.append(('Unterlagen', 'Ihre Karten im Satz der neuen Seite und die Unterlagen zum Entwurf, jede als PDF.',
              pdfs('unterlagen', [(u['ziel'], u['name']) for u in U if isinstance(u, dict) and 'ziel' in u])))
    pp = plan('papier_plan.json')
    O.append(('Drucksachen', 'Aushang, Karten, Einladung, Gutschein, Briefpapier und mehr, druckfertig mit Beschnitt.',
              pdfs('drucksachen', [(f"{KURZ}-{x['id']}", x['name']) for x in pp.get('druck', [])])))
    d = pdfs('untersetzer', [(f'{KURZ}-untersetzer-druckbogen-a3', 'Untersetzer, Druckbogen A3'), (f'{KURZ}-untersetzer-einzeln', 'Untersetzer, alle einzeln')])
    for x in pp.get('etiketten', []):
        q = os.path.join(HIER, 'roh', 'papier', x['id'] + '.png')
        if os.path.exists(q):
            d.append(eintrag(x['name'], kopie('03 Untersetzer', q, f"Untersetzer {x['id'][1:]} {re.sub(r'[/:’«»]', ' ', x['name']).strip()}.png")))
    O.append(('Untersetzer', 'Der Druckbogen mit Schnittlinien, jeder Untersetzer einzeln und alle als Bild.', [x for x in d if x]))
    sp = plan('sticker_plan.json')
    d = pdfs('sticker', [(f'{KURZ}-sticker-druckbogen-a3', 'Sticker, Druckbogen A3'), (f'{KURZ}-sticker-einzeln', 'Sticker, alle einzeln')])
    for x in sp.get('etiketten', []):
        q = os.path.join(HIER, 'roh', 'sticker', x['id'] + '.png')
        if os.path.exists(q):
            d.append(eintrag(x['name'], kopie('04 Sticker', q, f"Sticker {x['id'][1:]} {re.sub(r'[/:’«»]', ' ', x['name']).strip()}.png")))
    O.append(('Sticker', f"{len(sp.get('etiketten', [])) or 'Die'} Sticker: der Druckbogen mit Schnittlinien, jeder einzeln und alle als Bild.".replace('40 Sticker', 'Vierzig Sticker'), [x for x in d if x]))
    pk = plan('postkarten_plan.json')
    O.append(('Postkarten', f"{len(pk.get('karten', [])) or 'Die'} Postkarten vom Hafen: mit Beschnitt für die Druckerei und als Sammelbogen.",
              pdfs('postkarten', [(f'{KURZ}-postkarten-druck', 'Postkarten mit Beschnitt'), (f'{KURZ}-postkarten-sammelbogen-a3', 'Postkarten, Sammelbogen A3')])))
    bp = plan('beigaben_plan.json')
    O.append(('Beigaben', 'Was auf dem Tisch und an der Flasche liegt, jede Beigabe als PDF.', pdfs('beigaben', [(f"{KURZ}-{x['id']}", x['name']) for x in bp.get('druck', [])])))
    # Zeichen und Logo aus dem Markenbuch (dort fertig gezeichnet); die Website heute und die Werkstatt-Zips der Schriften bleiben weg
    LD = os.path.join(HAUS, '_werkzeuge', 'livre', 'dateien')
    namen = {'zeichen': 'Zeichen', 'zeiger': 'Die Zeiger', 'name-kurz': 'Name kurz', 'name': 'Name', 'logo': 'Logo', 'tapete': 'Tapete', 'farben': 'Farben', 'marke': 'Alles zur Marke'}
    farbe = {'himmel': 'Seehimmel', 'nacht': 'Nacht', 'stuhl': 'Stuhlblau', 'weiss': 'Weiss', 'schwarz': 'Schwarz', 'original': 'Original', 'dunkel': 'dunkel', 'hell': 'hell'}
    d = []
    for p in sorted(glob.glob(os.path.join(LD, KURZ + '-*'))):
        st, endung = os.path.splitext(os.path.basename(p)[len(KURZ) + 1:])
        if 'website-heute' in st or st.startswith('schriften'):
            continue
        art = next((k for k in sorted(namen, key=len, reverse=True) if st == k or st.startswith(k + '-')), None)
        if not art:
            continue
        zusatz = st[len(art):].strip('-')
        name = namen[art] + (' ' + farbe.get(zusatz, zusatz) if zusatz else '') + ' · ' + endung[1:].upper()
        d.append(eintrag(name, kopie('07 Zeichen und Logo', p)))
    O.append(('Zeichen und Logo', 'Die Zeiger, der Name und das Logo in allen Farben des Hauses, als SVG für den Druck und als PNG, dazu die Farben und die Tapete.', [x for x in d if x]))
    # Ansichten der neuen Website: jede Seite am Rechner und am Handy
    d = []
    for art, wort in (('Rechner', 'am Rechner'), ('Handy', 'am Handy')):
        for f in sorted(glob.glob(os.path.join(HIER, 'ansichten', art, '*.jpg'))):
            z = kopie(f'08 Ansichten der Website/{art}', f)
            if not re.search(r' \d+\.jpg$', f):
                d.append(eintrag(os.path.basename(f)[:-4] + ', ' + wort, z))
    O.append(('Ansichten der Website', 'Jede Seite des Entwurfs als Bild, am Rechner und am Handy; im Ordner liegen dazu die weiteren Abschnitte jeder Seite.', [x for x in d if x]))
    # Instagram: Profilbild, Texte, Beiträge (an ihrem Platz im Feed)
    d = []
    fj = os.path.join(ROOT, 'feed', 'feed.json')
    if os.path.exists(fj):
        fd = json.load(open(fj, encoding='utf-8'))
        t = os.path.join(ZIEL, '09 Instagram', 'Texte zu den Beiträgen.txt'); os.makedirs(os.path.dirname(t), exist_ok=True)
        open(t, 'w', encoding='utf-8').write('Profil @' + fd['profil']['name'] + '\n' + fd['profil']['titel'] + '\n' + '\n'.join(fd['profil']['bio']) + '\n' + fd['profil']['link'] + '\n\n'
                                             + 'Die Beiträge in der Reihenfolge des Rasters (01 = oben links, zuletzt gepostet).\n\n' + '\n\n'.join(f"Beitrag {p['n']}\n{p['cap']}" for p in fd['posts']) + '\n')
        d.append(eintrag('Profilbild', kopie('09 Instagram', os.path.join(ROOT, 'feed', 'avatar.jpg'), 'Profilbild.jpg')))
        d.append(eintrag('Texte zu den Beiträgen', t))
        for p in fd['posts']:
            d.append(eintrag(f"Beitrag {p['n']}", os.path.join(ROOT, 'feed', 'posts', p['n'] + '.jpg')))
    O.append(('Instagram', f"Das Profilbild, die Texte und die {len(d) - 2 if d else ''} Beiträge in voller Grösse, 1080 × 1350.", [x for x in d if x]))
    # Mails: jede Vorlage als Seite
    d = []
    mj = os.path.join(ROOT, 'mails', '_src', 'werkbank.json')
    if os.path.exists(mj):
        for nr, ordner, name, _ in json.load(open(mj, encoding='utf-8')):
            d.append(eintrag(f'{nr} {name}', os.path.join(ROOT, 'mails', ordner, 'index.html')))
    O.append(('Mails', 'Die zehn Mails an Gäste als Vorlage zum Öffnen, im Ton und Kleid des Hauses.', [x for x in d if x]))
    return [(n, s, [x for x in fs if x]) for n, s, fs in O if [x for x in fs if x]]


PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 11.5 11.5 4.5M5.5 4.5h6v6"/></svg>'


def zeile(i, name, weg, pfad):
    v = vorschau(pfad)
    endung = os.path.splitext(pfad)[1][1:].upper()
    art = 'Seite' if endung == 'HTML' else endung
    bild = f'<img src="{e(v)}" alt="" loading="lazy" decoding="async">' if v else f'<b>{e(art)}</b>'
    return (f'<li class="hr" style="--i:{min(i, 6)}"><a href="{e(weg)}" target="_blank" rel="noopener"><span class="vs{" vs--m" if art == "Seite" else ""}">{bild}</span>'
            f'<span class="nm">{e(name)}<small>{e(art)} · {groesse(pfad)}</small></span><i>{PF}</i></a></li>')


def seite(O):
    teile = ''
    for i, (name, satz, dateien) in enumerate(O, 1):
        beitraege = [x for x in dateien if x[0].startswith('Beitrag ')]
        andere = [x for x in dateien if x not in beitraege]
        liste = ''.join(zeile(k, *x) for k, x in enumerate(andere))
        raster = ''
        if beitraege:
            raster = '<div class="raster">' + ''.join(f'<a href="{e(w)}" target="_blank" rel="noopener" aria-label="{e(n)} öffnen"><img src="{e(vorschau(p) or w)}" alt="" loading="lazy" decoding="async"></a>' for n, w, p in beitraege) + '</div>'
        teile += f'''<section class="or {"or--b" if i % 2 else "or--p"}" id="o{i}">
  <div class="in">
    <div class="kopf hr"><p class="nr"><span>{i:02d}</span><i></i></p><h2>{e(name)}</h2><p class="satz">{e(satz)}</p><p class="zahl">{len(dateien)} {"Datei" if len(dateien) == 1 else "Dateien"}</p></div>
    <div class="inh"><ul class="dateien{" dateien--2" if len(andere) > 8 else ""}">{liste}</ul>{raster}</div>
  </div>
</section>
'''
    zahl = sum(len(fs) for _, _, fs in O)
    ordner_wort = {9: 'neun', 10: 'zehn', 8: 'acht', 7: 'sieben', 11: 'elf'}.get(len(O), str(len(O)))
    return f'''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>Material · {N}</title>
<meta name="description" content="Alles, was für den Entwurf der neuen Website der {N} entstanden ist, sortiert zum Ansehen und Herunterladen.">
<link rel="icon" href="../assets/svg/zeichen.svg">
<style>
@font-face{{font-family:'Open Sans';font-weight:300 800;font-display:swap;src:url('../assets/fonts/OpenSans-var.woff2') format('woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:400 600;font-display:swap;src:url('../assets/fonts/InstrumentSans-normal-400_600.woff2') format('woff2')}}
@font-face{{font-family:'DM Mono';font-weight:400;font-display:swap;src:url('../assets/fonts/DMMono-normal-400.woff2') format('woff2')}}
:root{{--nacht:#0b1d3d;--tief:#0A234C;--stuhl:#113d88;--papier:#E7ECF3;--spiegel:#D0DAE7;--blatt:#F4F6F9;--himmel:#A2B6CF;--himmel2:#C5D2E1;--betont:#0F3678;--tinte:#041023;--leise:#515656;
  --rand:clamp(20px,5vw,84px);--e1:cubic-bezier(.16,1,.3,1)}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--papier);color:var(--tinte);font:400 17px/1.6 'Instrument Sans',system-ui,sans-serif}}
a{{color:inherit}}
.leiste{{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px var(--rand);background:rgba(11,29,61,.94);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid rgba(162,182,207,.25)}}
.leiste .mk{{display:flex;align-items:center;gap:14px;text-decoration:none;color:var(--blatt);min-width:0}}
.leiste .mk img{{width:26px;height:auto;display:block}}
.leiste .mk span{{font:400 13px/1.2 'Open Sans',Arial,sans-serif;letter-spacing:.2em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.leiste .mk small{{font:400 11px/1 'DM Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--himmel);padding-left:14px;border-left:1px solid rgba(162,182,207,.4)}}
.zu{{flex:none;display:inline-flex;align-items:center;gap:10px;height:40px;padding:0 6px 0 18px;border-radius:999px;text-decoration:none;font:400 11px/1 'DM Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--blatt);
  background:linear-gradient(180deg,#1d4f9e,var(--stuhl) 60%,var(--tief));box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 0 0 1px rgba(162,182,207,.38)}}
.zu i,.kn i,.dateien a i{{flex:none;display:grid;place-items:center;border-radius:50%;color:var(--tinte);background:linear-gradient(180deg,#f3f6f9,var(--himmel2) 55%,var(--himmel));box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}}
.zu i{{width:28px;height:28px}}
svg{{fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.zu svg{{width:12px;height:12px}}
.held{{background:var(--nacht) url(../assets/svg/tapete-a-dunkel.svg) 50% 0/168px auto;color:var(--blatt);padding:clamp(70px,10vw,150px) 0 clamp(70px,9vw,130px);overflow:hidden}}
.held .in{{padding:0 var(--rand);max-width:1500px;margin:0 auto}}
.held .zz{{width:clamp(48px,4.4vw,66px);height:auto;display:block;margin-bottom:clamp(26px,3vw,40px)}}
.held .kap{{display:flex;align-items:center;gap:16px;margin:0 0 22px;font:400 12.5px/1 'DM Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--himmel)}}
.held .kap i{{width:64px;height:1px;background:var(--himmel)}}
h1{{margin:0;font:400 clamp(2.3rem,5.4vw,5rem)/1.12 'Open Sans',Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;text-wrap:balance}}
h1 em{{font-style:normal;color:var(--himmel)}}
.hz{{height:0;border-top:1px solid rgba(162,182,207,.45);margin:clamp(30px,3.4vw,48px) calc(-1 * var(--rand)) 0}}
.held p.lead{{max-width:56ch;margin:clamp(26px,3vw,40px) 0 0;color:rgba(244,246,249,.86);font-size:clamp(1rem,1.25vw,1.18rem)}}
.held dl{{display:flex;flex-wrap:wrap;gap:12px 48px;margin:clamp(28px,3vw,44px) 0 0;padding:0}}
.held dl div{{display:flex;flex-direction:column;gap:6px}}
.held dt{{font:400 11px/1 'DM Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--himmel)}}
.held dd{{margin:0;font:400 clamp(1.6rem,2.4vw,2.2rem)/1 'DM Mono',monospace;color:var(--blatt)}}
.or{{position:relative;margin-top:-22px;border-radius:22px 22px 0 0;padding:clamp(56px,6.4vw,96px) 0 clamp(70px,7vw,110px);box-shadow:inset 0 1px 0 rgba(162,182,207,.55)}}
.or--b{{background:var(--blatt)}}.or--p{{background:var(--papier)}}
.or .in{{display:grid;grid-template-columns:minmax(260px,.8fr) 1.6fr;gap:clamp(30px,5vw,90px);padding:0 var(--rand);max-width:1500px;margin:0 auto;align-items:start}}
.kopf{{position:sticky;top:96px}}
.nr{{display:flex;align-items:center;gap:16px;margin:0 0 18px;font:400 13px/1 'DM Mono',monospace;letter-spacing:.14em;color:var(--betont)}}
.nr i{{width:56px;height:1px;background:var(--betont);opacity:.6}}
h2{{margin:0;font:400 clamp(1.5rem,2.4vw,2.2rem)/1.2 'Open Sans',Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;text-wrap:balance}}
.satz{{margin:16px 0 0;color:#2c3b52;max-width:40ch;text-wrap:pretty}}
.zahl{{margin:18px 0 0;font:400 11px/1 'DM Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--betont)}}
.dateien{{list-style:none;margin:0;padding:0;border-top:1px solid rgba(4,16,35,.12)}}
.dateien--2{{display:grid;grid-template-columns:1fr 1fr;column-gap:clamp(20px,2.4vw,40px)}}
.dateien li{{border-bottom:1px solid rgba(4,16,35,.12)}}
.dateien a{{display:flex;align-items:center;gap:18px;padding:12px 0;text-decoration:none}}
.vs{{flex:none;width:58px;height:58px;border-radius:10px;overflow:hidden;display:grid;place-items:center;background:var(--spiegel);box-shadow:0 0 0 1px rgba(15,54,120,.14)}}
.vs img{{width:100%;height:100%;object-fit:contain;display:block}}
.vs--m img{{object-fit:cover;object-position:50% 0}}
.vs b{{font:400 10.5px/1 'DM Mono',monospace;letter-spacing:.1em;color:var(--betont)}}
.nm{{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px;font-size:1rem;line-height:1.35}}
.nm small{{font:400 10.5px/1.3 'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--leise)}}
.dateien a i{{width:40px;height:40px;transition:transform .5s var(--e1)}}
.dateien a i svg{{width:14px;height:14px}}
.dateien a:hover i{{transform:translate(2px,-2px)}}
.dateien a:focus-visible,.raster a:focus-visible,.zu:focus-visible,.kn:focus-visible{{outline:2px solid var(--betont);outline-offset:3px;border-radius:12px}}
.raster{{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin-top:26px}}
.raster a{{display:block;aspect-ratio:4/5;border-radius:10px;overflow:hidden;background:var(--nacht);box-shadow:0 0 0 1px rgba(15,54,120,.14)}}
.raster img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .9s var(--e1)}}
.raster a:hover img{{transform:scale(1.04)}}
.ausklang{{background:var(--nacht) url(../assets/svg/tapete-a-dunkel.svg) 50% 0/168px auto;color:var(--blatt);text-align:center;padding:clamp(70px,8vw,120px) var(--rand);margin-top:-22px;border-radius:22px 22px 0 0;position:relative}}
.ausklang p{{max-width:52ch;margin:0 auto;font-size:clamp(1.02rem,1.3vw,1.2rem);color:rgba(244,246,249,.88)}}
.kn{{display:inline-flex;align-items:center;gap:14px;height:54px;padding:0 8px 0 26px;border-radius:999px;margin-top:32px;text-decoration:none;font:400 12px/1 'DM Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--blatt);
  background:linear-gradient(180deg,#1d4f9e,var(--stuhl) 60%,var(--tief));box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 0 0 1px rgba(162,182,207,.38),0 16px 26px -14px rgba(0,0,0,.7)}}
.kn i{{width:40px;height:40px}}.kn svg{{width:14px;height:14px}}
.zu>span,.kn>span{{position:relative}}
@supports (interpolate-size:allow-keywords) and (app-region:drag){{.zu>span,.kn>span{{top:.5px}}}}
footer{{background:var(--tief);color:rgba(244,246,249,.66);text-align:center;font-size:.9rem;padding:26px var(--rand) 34px}}
footer a{{color:var(--himmel2)}}
html.js .hr{{opacity:0;transform:translate3d(0,26px,0)}}
html.js .hr.da{{opacity:1;transform:none;transition:opacity .8s cubic-bezier(.2,.7,.2,1) calc(var(--i,0) * 60ms),transform 1.1s var(--e1) calc(var(--i,0) * 60ms)}}
@media (prefers-reduced-motion:reduce){{html.js .hr{{opacity:1;transform:none;transition:none}}}}
@media (max-width:1000px){{.or .in{{grid-template-columns:1fr}}.kopf{{position:static}}.dateien--2{{grid-template-columns:1fr}}.raster{{grid-template-columns:repeat(4,1fr)}}}}
@media (max-width:560px){{.leiste .mk small,.leiste .mk span{{display:none}}.raster{{grid-template-columns:repeat(3,1fr)}}.vs{{width:50px;height:50px}}.dateien a{{gap:12px}}.dateien a i{{width:32px;height:32px}}.nm{{font-size:.95rem}}}}
</style></head>
<body>
<script>if (!matchMedia('(prefers-reduced-motion:reduce)').matches && 'IntersectionObserver' in window) document.documentElement.classList.add('js');</script>
<header class="leiste"><a class="mk" href="../werkbank/index.html"><img src="../mails/img/zeichen.png" alt="" width="26"><span>{N}</span><small>Material</small></a>
  <a class="zu" href="../werkbank/index.html#material"><span>Alles auf einen Blick</span><i>{PF}</i></a></header>
<main>
<section class="held"><div class="in">
  <img class="zz" src="../mails/img/zeichen.png" alt="" width="66">
  <p class="kap"><i></i><span>Material</span></p>
  <h1>Alles liegt für<br><em>Sie bereit.</em></h1>
  <div class="hz"></div>
  <p class="lead">Was für den Entwurf neu entstanden ist, liegt hier sortiert in {ordner_wort} Ordnern: Unterlagen, Drucksachen, Untersetzer, Sticker, Postkarten, Beigaben, Zeichen und Logo, die Ansichten der Website, der Feed und die Mails. Sie können jede Datei ansehen und herunterladen.</p>
  <dl><div><dt>Ordner</dt><dd>{len(O)}</dd></div><div><dt>Dateien</dt><dd>{zahl}</dd></div><div><dt>Stand</dt><dd>{STAND.replace('.2026', '.26')}</dd></div></dl>
</div></section>
{teile}<section class="ausklang"><p class="hr">Fehlt Ihnen eine Datei oder ein Format, sagen Sie es mir; ich lege es dazu.</p>
  <a class="kn hr" href="../werkbank/index.html#material"><span>Zur Werkbank</span><i>{PF}</i></a></section>
</main>
<footer>Die Dateien gehören zum Entwurf von Robert Reff, Tasty Studios, und sind keine offiziellen Unterlagen des Hauses. Fotos, Zeichen und Texte gehören der {N} und den jeweiligen Fotografen. Stand {STAND}.</footer>
<script>
(function () {{
  if (!document.documentElement.classList.contains('js')) return;
  var io = new IntersectionObserver(function (es) {{ es.forEach(function (x) {{ if (x.isIntersecting) {{ x.target.classList.add('da'); io.unobserve(x.target); }} }}); }}, {{ rootMargin: '0px 0px -6% 0px' }});
  [].forEach.call(document.querySelectorAll('.hr'), function (x) {{ io.observe(x); }});
}})();
</script>
</body></html>
'''


def aufraeumen(O):
    """Dateien in material/, die keinem Eintrag mehr gehören (frühere Fassungen, Culinarium), und alte Vorschauen weg."""
    behalten = {os.path.realpath(p) for _, _, fs in O for _, _, p in fs}
    for wurzel, _, dateien in os.walk(ZIEL):
        if wurzel.startswith(VOR):
            continue
        for d in dateien:
            p = os.path.join(wurzel, d)
            if d == 'index.html' and wurzel == ZIEL:
                continue
            if os.path.realpath(p) not in behalten and not ('08 Ansichten der Website' in p):
                os.remove(p)
    # Ansichten: nur, was es in den Quellen noch gibt
    for art in ('Rechner', 'Handy'):
        q = {os.path.basename(f) for f in glob.glob(os.path.join(HIER, 'ansichten', art, '*.jpg'))}
        for f in glob.glob(os.path.join(ZIEL, '08 Ansichten der Website', art, '*')):
            if os.path.basename(f) not in q:
                os.remove(f)
    for wurzel, ordner, dateien in sorted(os.walk(ZIEL), key=lambda x: -len(x[0])):
        if wurzel != ZIEL and not os.listdir(wurzel):
            os.rmdir(wurzel)


def main():
    O = ordner_liste()
    s = seite(O)
    benutzt = set(re.findall(r'_vorschau/([0-9a-f]{12}\.webp)', s))
    aufraeumen(O)
    for f in glob.glob(os.path.join(VOR, '*.webp')):
        if os.path.basename(f) not in benutzt:
            os.remove(f)
    open(os.path.join(ZIEL, 'index.html'), 'w', encoding='utf-8').write(s)
    print('Material:', len(O), 'Ordner,', sum(len(fs) for _, _, fs in O), 'Dateien:', ', '.join(f'{n} {len(fs)}' for n, _, fs in O))


if __name__ == '__main__':
    main()
