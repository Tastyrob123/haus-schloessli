# Gäste-Funktionen der Wirtschaft am Schlössli (Station 07, Runde 3, Robert 19.10.2026 «okay alle einbaun»).
# Vorne das beste Ergebnis, hinten simuliert: nichts wird verschickt, gebucht oder bezahlt (Designstudie).
# Alle Angaben aus inhalt/ und assets/data/weine.json; was dort nicht steht, wird nicht behauptet.
import json, pathlib, html

HIER = pathlib.Path(__file__).resolve().parent
HAUS = json.loads((HIER / 'inhalt' / 'haus.json').read_text())
KARTE = json.loads((HIER / 'inhalt' / 'karte.json').read_text())
LUNCH = json.loads((HIER / 'inhalt' / 'lunch.json').read_text())
BANKETT = json.loads((HIER / 'inhalt' / 'bankett.json').read_text())
WEINE = json.loads((HIER / 'assets' / 'data' / 'weine.json').read_text())
RES = 'https://services.gastronovi.com/restaurants/118851/reservierung/widget'
ZEIGER = (HIER / 'assets' / 'svg' / 'zeiger.svg').read_text().replace('<svg ', '<svg aria-hidden="true" ', 1)
ALLERGENE = [('G', 'Gluten'), ('L', 'Laktose'), ('E', 'Eier'), ('F', 'Fische'), ('S', 'Schalen- und Weichtiere'), ('So', 'Soja'), ('En', 'Erdnüsse'), ('N', 'Nüsse'), ('Se', 'Sellerie')]
PFEIL = '<span class="kn"><svg class="pf" viewBox="0 0 16 10" aria-hidden="true"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span>'
KREUZ = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13" fill="none"/></svg>'


def e(s):
    return html.escape(str(s), quote=True)


def knopf(text, href='#', dunkel=False, klein=False, attr='', tag='a'):
    k = 'knopf' + (' knopf--dunkel' if dunkel else '') + (' knopf--klein' if klein else '')
    if tag == 'button':
        return f'<button class="{k}" type="button"{attr}>{e(text)} {PFEIL}</button>'
    return f'<a class="{k}" href="{e(href)}"{attr}>{e(text)} {PFEIL}</a>'


def chips(name, werte, mehrfach=False, erste=False):
    t = 'checkbox' if mehrfach else 'radio'
    return '<div class="chips" role="group">' + ''.join(
        f'<label class="chip"><input type="{t}" name="{e(name)}" value="{e(v)}"{" checked" if erste and i == 0 else ""}><span>{e(l)}</span></label>' for i, (v, l) in enumerate(werte)) + '</div>'


def zeiten():
    return ''.join(f'<button type="button" data-v="{h:02d}:{m:02d} Uhr">{h:02d}:{m:02d} Uhr</button>' for h in range(11, 22) for m in (0, 30) if (h, m) >= (11, 30))


def kalender_feld(name='datum', titel='Datum'):
    zu = ','.join(f'{a}/{b}' for a, b in HAUS['ferien_iso'])
    return f'<div class="feld" data-wahl="{name}" data-kal data-zu="{zu}"><span>{e(titel)}</span><button class="wahl-k" type="button" aria-expanded="false"><span>Tag wählen</span></button><div class="wahl-l"></div><input type="hidden" name="{name}"></div>'


def wahl_feld(name, titel, werte, start=None):
    l = ''.join(f'<button type="button" data-v="{e(v)}">{e(v)}</button>' for v in werte)
    return f'<div class="feld" data-wahl="{name}"><span>{e(titel)}</span><button class="wahl-k" type="button" aria-expanded="false"><span>{e(start or "Bitte wählen")}</span></button><div class="wahl-l">{l}</div><input type="hidden" name="{name}" value="{e(start or "")}"></div>'


# ---------------------------------------------------------------- 2 + 6 Reservierung: Anfrage mit Flasche, Platz, Allergien und Wünschen; Buchungsmaske des Hauses bleibt
def reservation_dialog():
    allerg = chips('allergene', [(k, f'{n}') for k, n in ALLERGENE] + [('VEG', 'vegetarisch')], mehrfach=True)
    return f'''<dialog class="fe fe--breit" id="fe-reservation" aria-label="Reservation">
  <div class="fe__kopf2"><h2>Reservation</h2><button class="fe__zu" type="button" aria-label="Schliessen">{KREUZ}</button></div>
  <div class="fe__inhalt">
    <div class="reiter" role="tablist"><button type="button" role="tab" aria-selected="true" data-reiter="anfrage">Mit Wünschen anfragen</button><button type="button" role="tab" aria-selected="false" data-reiter="direkt">Direkt buchen</button></div>
    <div class="reiter__f" data-fach="anfrage">
      <form class="fe__form" novalidate data-art="reservierung">
        <div class="felder">
          {kalender_feld()}
          <div class="feld" data-wahl="uhrzeit"><span>Uhrzeit</span><button class="wahl-k" type="button" aria-expanded="false"><span>Uhrzeit wählen</span></button><div class="wahl-l">{zeiten()}</div><input type="hidden" name="uhrzeit"></div>
          <div class="feld"><label for="r-pers">Personen</label><input id="r-pers" name="personen" inputmode="numeric" autocomplete="off" required></div>
          {wahl_feld('platz', 'Platz', ['Drinnen in der Gaststube', 'Draussen auf der Terrasse', 'An der Lästermeile'], 'Draussen auf der Terrasse')}
          <div class="feld feld--ganz flasche" data-flasche><span>Ihre Flasche</span><div class="flasche__leer">Noch keine gewählt. <a href="weinkarte.html?von=abend#berater">Im Weinberater auswählen</a></div><div class="flasche__voll" hidden><b data-f-name></b><small data-f-info></small><em>wird für Sie bereitgelegt</em><button type="button" class="leise" data-f-weg>Entfernen</button></div><input type="hidden" name="flasche"></div>
          <div class="feld feld--ganz"><span>Allergien und Unverträglichkeiten</span>{allerg}</div>
          <div class="feld feld--ganz"><label for="r-wunsch">Wünsche (Anlass, Hochstuhl, Hund …)</label><textarea id="r-wunsch" name="wunsch"></textarea></div>
          <div class="feld"><label for="r-name">Name</label><input id="r-name" name="name" autocomplete="name" required></div>
          <div class="feld"><label for="r-kontakt">Telefon oder E-Mail</label><input id="r-kontakt" name="kontakt" autocomplete="email" required></div>
        </div>
        <div class="fe__senden"><button class="knopf knopf--dunkel" type="submit">Anfrage senden {PFEIL}</button></div>
        <p class="fe__hinweis">{e(HAUS['zeiten']['tage'].replace(' - ', ' bis '))}, {e(HAUS['zeiten']['offen'].replace(' - ', ' bis '))} · {e(HAUS['zeiten']['ruhetag'])}. Designstudie: In diesem Entwurf wird nichts verschickt.</p>
      </form>
      <div class="fe__danke"><h3>Vielen Dank.</h3><p>Ihre Anfrage ist bei uns. Wir melden uns mit der Bestätigung.</p><p class="fe__hinweis">Designstudie: Diese Anfrage wurde nicht verschickt.</p></div>
    </div>
    <div class="reiter__f" data-fach="direkt" hidden>
      <div class="fe__frame"><iframe data-src="{RES}" title="Reservation der Wirtschaft am Schlössli" loading="lazy"></iframe></div>
      <p class="fe__hinweis">Telefonisch unter <a href="tel:{HAUS['telefon_href']}">{e(HAUS['telefon'])}</a> oder per Mail an <span>{e(HAUS['mail'])}</span>.</p>
    </div>
  </div>
</dialog>
'''


# ---------------------------------------------------------------- 1 + 3 Weinberater «Der Keller» und Wein-Ansicht (Robert 19.10.2026: «richtig geil, luxuriös, edel … jeder Wein seine eigene Welt»)
# Gezeichnete Flaschen je Art (nur als Zeichen für die Art; wo es ein echtes Flaschenfoto gibt, steht das Foto), runde Flaggen je Land.
FL_FORM = {
    'rot': 'M34 6h12v9h-1v50c0 11 21 15 21 35v122c0 4-3 7-7 7H21c-4 0-7-3-7-7V100c0-20 21-24 21-35V15h-1z',
    'ros': 'M34 6h12v9h-1v38c0 27 23 37 23 61v108c0 4-3 7-7 7H19c-4 0-7-3-7-7V114c0-24 23-34 23-61V15h-1z',
    'sch': 'M33 6h14v10h-1v32c0 29 26 39 26 65v113c0 5-3 8-8 8H16c-5 0-8-3-8-8V113c0-26 26-36 26-65V16h-1z',
    'wei': 'M35 4h10v8h-1v60c0 22 15 30 15 52v104c0 4-3 6-6 6H27c-3 0-6-2-6-6V124c0-22 15-30 15-52V12h-1z',
    'sue': 'M35 4h10v8h-1v60c0 22 15 30 15 52v104c0 4-3 6-6 6H27c-3 0-6-2-6-6V124c0-22 15-30 15-52V12h-1z',
}
FL_KAPSEL = {'rot': 62, 'ros': 50, 'sch': 74, 'wei': 66, 'sue': 66}
FL_ETIKETT = {'rot': (16, 128, 48, 62), 'ros': (14, 136, 52, 58), 'sch': (10, 140, 60, 56), 'wei': (23, 142, 34, 54), 'sue': (23, 142, 34, 54)}
FL_FARBEN = {'rot': ('#1d0710', '#5e1526', '#2a0a14'), 'ros': ('#d77f6c', '#f6b9a5', '#e0907c'), 'sch': ('#0f241a', '#2c4c39', '#132b20'),
             'wei': ('#a99550', '#e8d9a0', '#bfa964'), 'sue': ('#6b330c', '#c47a2c', '#86420f')}
ART_KLASSE = {'Champagner & Schaumwein': 'sch', 'Weisswein': 'wei', 'Rosé': 'ros', 'Rotwein': 'rot', 'Süsswein': 'sue'}
LAENDER = ['Schweiz', 'Deutschland', 'Österreich', 'Frankreich', 'Italien', 'Spanien', 'Portugal']


def flaschen_defs():
    g = ''
    for k, (a, m, z) in FL_FARBEN.items():
        g += f'<linearGradient id="fl-{k}" x1="0" x2="1"><stop offset="0" stop-color="{a}"/><stop offset=".42" stop-color="{m}"/><stop offset=".62" stop-color="{z}"/><stop offset="1" stop-color="{a}"/></linearGradient>'
    g += '<linearGradient id="fl-kap" x1="0" x2="1"><stop offset="0" stop-color="#06142d"/><stop offset=".45" stop-color="#1A4D9F"/><stop offset="1" stop-color="#06142d"/></linearGradient>'
    g += '<linearGradient id="fl-gold" x1="0" x2="1"><stop offset="0" stop-color="#7d6338"/><stop offset=".45" stop-color="#e3cf9c"/><stop offset="1" stop-color="#7d6338"/></linearGradient>'
    for k, d in FL_FORM.items():
        g += f'<clipPath id="fl-c-{k}"><path d="{d}"/></clipPath>'
    for i, l in enumerate(LAENDER):
        g += f'<clipPath id="flg-c-{i}"><circle cx="20" cy="20" r="20"/></clipPath>'
    return f'<svg class="fl-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>{g}</defs></svg>'


def flasche_svg(k, cls='fl'):
    x, y, w, h = FL_ETIKETT[k]
    kap = 'url(#fl-gold)' if k == 'sch' else 'url(#fl-kap)'
    zug = ' transform="translate(12 64) scale(.7)"' if k == 'sue' else ''
    return (f'<svg class="{cls} {cls}--{k}" viewBox="0 0 80 240" aria-hidden="true" focusable="false"><g{zug}>'
            f'<path d="{FL_FORM[k]}" fill="url(#fl-{k})"/>'
            f'<g clip-path="url(#fl-c-{k})"><rect x="0" y="0" width="80" height="{FL_KAPSEL[k]}" fill="{kap}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#F3F1EA"/><rect x="{x + 6}" y="{y + 14}" width="{w - 12}" height="1.4" fill="#0A2552" opacity=".55"/>'
            f'<rect x="{x + 10}" y="{y + 22}" width="{w - 20}" height="1" fill="#0A2552" opacity=".35"/>'
            f'<rect x="{x + 8}" y="{y + h - 14}" width="{w - 16}" height="1" fill="#0A2552" opacity=".3"/>'
            f'<rect x="24" y="0" width="5" height="240" fill="#fff" opacity=".22"/><rect x="31" y="0" width="1.6" height="240" fill="#fff" opacity=".16"/></g></g></svg>')


FLAGGE = {
    'Schweiz': '<rect width="40" height="40" fill="#D52B1E"/><path d="M17 9h6v8h8v6h-8v8h-6v-8H9v-6h8z" fill="#fff"/>',
    'Deutschland': '<rect width="40" height="14" fill="#111"/><rect y="13.3" width="40" height="13.4" fill="#DD0000"/><rect y="26.7" width="40" height="13.3" fill="#FFCE00"/>',
    'Österreich': '<rect width="40" height="40" fill="#C8102E"/><rect y="13.3" width="40" height="13.4" fill="#fff"/>',
    'Frankreich': '<rect width="14" height="40" fill="#0055A4"/><rect x="13.3" width="13.4" height="40" fill="#fff"/><rect x="26.7" width="13.3" height="40" fill="#EF4135"/>',
    'Italien': '<rect width="14" height="40" fill="#009246"/><rect x="13.3" width="13.4" height="40" fill="#fff"/><rect x="26.7" width="13.3" height="40" fill="#CE2B37"/>',
    'Spanien': '<rect width="40" height="40" fill="#AA151B"/><rect y="10" width="40" height="20" fill="#F1BF00"/>',
    'Portugal': '<rect width="40" height="40" fill="#FF0000"/><rect width="16" height="40" fill="#006600"/><circle cx="16" cy="20" r="6.5" fill="#FFCC00"/><circle cx="16" cy="20" r="4" fill="#fff" stroke="#FF0000" stroke-width="1.6"/>',
}


def flagge_svg(land, cls='flg'):
    if land not in FLAGGE:
        return ''
    return f'<svg class="{cls}" viewBox="0 0 40 40" aria-hidden="true" focusable="false"><g clip-path="url(#flg-c-{LAENDER.index(land)})">{FLAGGE[land]}</g></svg>'


ZEICHEN_K = (HIER / 'assets' / 'svg' / 'zeichen.svg').read_text().replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1)


def weinberater():
    from collections import Counter
    n_art = Counter(w['art'] for w in WEINE)
    n_land = Counter(w['land'] for w in WEINE)
    arten = [(a, a.replace('Champagner & Schaumwein', 'Schaumwein'), ART_KLASSE[a]) for a in ['Champagner & Schaumwein', 'Weisswein', 'Rosé', 'Rotwein', 'Süsswein']]
    # Je Art eine echte Flasche von der Karte (Foto aus wein_bilder.py); fehlt das Foto, steht die gezeichnete Flasche
    bilder = json.loads((HIER / 'assets' / 'data' / 'wein-bilder.json').read_text()) if (HIER / 'assets' / 'data' / 'wein-bilder.json').exists() else {}
    vertreter = {'sch': 37, 'wei': 196, 'ros': 255, 'rot': 351, 'sue': 465}

    def echte(k):
        b = bilder.get(str(vertreter[k]), {})
        return f'<img class="fl fl--foto" src="{b["f"]}" alt="" decoding="async" fetchpriority="low">' if b.get('f') else flasche_svg(k)
    alle_fl = '<span class="kf__alle">' + echte('wei') + echte('rot') + echte('sch') + '</span>'
    art_html = (f'<label class="kf kf--alle"><input type="radio" name="art" value="" checked><span class="kf__b">{alle_fl}</span><span class="kf__n">Alle Weine</span><span class="kf__z" data-z>{len(WEINE)}</span></label>'
                + ''.join(f'<label class="kf kf--{k}"><input type="radio" name="art" value="{e(a)}"><span class="kf__b">{echte(k)}</span><span class="kf__n">{e(l)}</span><span class="kf__z" data-z>{n_art[a]}</span></label>' for a, l, k in arten))
    land_html = (f'<label class="kl"><input type="radio" name="land" value="" checked><span class="kl__m kl__m--alle">{ZEICHEN_K}</span><span class="kl__n">Alle Länder</span><span class="kl__z" data-z>{len(WEINE)}</span></label>'
                 + ''.join(f'<label class="kl"><input type="radio" name="land" value="{e(l)}"><span class="kl__m">{flagge_svg(l)}</span><span class="kl__n">{e(l)}</span><span class="kl__z" data-z>{n_land[l]}</span></label>' for l in LAENDER))
    rb = [r for r, n in Counter(r for w in WEINE for r in w['reben']).most_common() if n >= 2]

    def wahl(name, titel, werte):
        l = ''.join(f'<button type="button" data-v="{e(v)}" data-l="{e(t)}"><span>{e(t)}</span><i data-z></i></button>' for v, t in werte)
        return f'<div class="keller__wahl" data-kw="{name}"><span class="mono">{e(titel)}</span><button class="keller__k" type="button" aria-expanded="false"><span>{e(werte[0][1])}</span></button><div class="keller__l" role="listbox">{l}</div><input type="hidden" name="{name}" value=""></div>'
    zeile = (wahl('rebe', 'Rebsorte', [('', 'Alle Rebsorten')] + [(r, r) for r in sorted(rb)])
             + wahl('preis', 'Preis der Flasche', [('', 'Jeder Preis'), ('0-80', 'bis 80 Franken'), ('81-120', '81 bis 120 Franken'), ('121-200', '121 bis 200 Franken'), ('201-99999', 'über 200 Franken')])
             + wahl('gross', 'Flasche', [('', 'Jede Grösse'), ('0.375l', 'Halbe Flasche, 0,375 l'), ('0.7l', 'Flasche, 0,7 l'), ('1.5l', 'Magnum, 1,5 l'), ('gross', 'Grösser als Magnum')]))
    # Nach Geschmack (Robert 19.10.2026 «klassisch oder individuell … Geschmacksnuancen»): nur belegte Angaben aus wein-infos.json (wein_infos.py)
    infos = json.loads((HIER / 'assets' / 'data' / 'wein-infos.json').read_text()) if (HIER / 'assets' / 'data' / 'wein-infos.json').exists() else {'weine': {}, 'gruppen': {}}
    n_g = sum(1 for v in infos['weine'].values() if 's' in v or 'a' in v)
    skalen = [('g_k', 'Körper', ['leicht', 'mittel', 'voll']), ('g_sa', 'Säure', ['mild', 'ausgewogen', 'frisch']),
              ('g_su', 'Süsse', ['trocken', 'halbtrocken', 'süss']), ('g_t', 'Tannin', ['weich', 'mittel', 'kräftig'])]
    skala_html = ''.join(f'<div class="skala" role="radiogroup" aria-label="{t}"><span class="mono">{t}</span><div class="skala__bahn"><input type="radio" name="{n}" value="" checked hidden>'
                         + ''.join(f'<label class="skala__p"><input type="radio" name="{n}" value="{i + 1}"><i></i><span>{e(x)}</span><b data-z></b></label>' for i, x in enumerate(st)) + '</div></div>' for n, t, st in skalen)
    FARBE = {'red_fruit': '#B23A48', 'black_fruit': '#3D1E3F', 'citrus_fruit': '#E8C547', 'tree_fruit': '#A7C957', 'tropical_fruit': '#F2A541', 'dried_fruit': '#8C5E3C',
             'floral': '#D9A5C0', 'vegetal': '#5E8C61', 'spices': '#A0522D', 'oak': '#7A5230', 'earth': '#6B6B6B', 'microbio': '#E3D5B8', 'non_oak': '#4A3B2A'}
    bildchen = json.loads((HIER / 'assets' / 'data' / 'wein-bildchen.json').read_text()) if (HIER / 'assets' / 'data' / 'wein-bildchen.json').exists() else {'gruppe': {}}
    aroma_html = ''.join(f'<label class="ka"><input type="checkbox" name="aroma" value="{g}"><span class="ka__m">' + (f'<img src="{bildchen["gruppe"][g]}" alt="" loading="lazy" decoding="async">' if g in bildchen['gruppe'] else '') + f'</span><span class="ka__n">{e(t)}</span><span class="ka__z" data-z></span></label>' for g, t in infos['gruppen'].items())
    speisen = [x for x, n in Counter(f for v in infos['weine'].values() for f in v.get('sp', [])).most_common() if n >= 3]
    speise_html = wahl('speise', 'Passt zu', [('', 'Jedem Gericht')] + [(x, x) for x in speisen])
    zeichen = ''.join(f'<i data-art="{k}">{flasche_svg(k, "wf__zf")}</i>' for k in FL_FORM) + ''.join(f'<i data-land="{e(l)}">{flagge_svg(l, "wf__flg")}</i>' for l in LAENDER)
    return f'''<section class="teil f-tapete" id="berater" aria-label="Weinberater">
  {flaschen_defs()}
  <div class="innen">
    <div class="ab-satz"><h2 class="t2" data-schlitz>Welcher Wein <em>darf es sein?</em></h2><p class="lauf" data-r="text">Wählen Sie, was Ihnen schmeckt: Art, Herkunft, Rebsorte, Preis und Flasche. Jede Flasche stammt aus der Weinkarte vom 14. Oktober 2026. Was im Glas wartet, erzählt Ihnen Jonas Volpert am Tisch.</p></div>
    <form class="keller f-dunkel" data-berater onsubmit="return false">
      <div class="keller__modus" role="tablist" aria-label="Art der Suche"><button type="button" role="tab" aria-selected="true" data-modus="klassisch">Klassisch</button><button type="button" role="tab" aria-selected="false" data-modus="geschmack">Nach Geschmack</button></div>
      <div class="keller__fach" data-fach-k="klassisch">
        <div class="keller__arten" role="radiogroup" aria-label="Art des Weins">{art_html}</div>
        <div class="keller__laender" role="radiogroup" aria-label="Herkunft">{land_html}</div>
        <div class="keller__zeile">{zeile}</div>
      </div>
      <div class="keller__fach" data-fach-k="geschmack" hidden>
        <div class="keller__skalen">{skala_html}</div>
        <div class="keller__aromen" aria-label="Aromen"><span class="mono">Im Duft und am Gaumen</span><div class="keller__ar">{aroma_html}</div></div>
        <div class="keller__zeile keller__zeile--g">{speise_html}<p class="keller__quelle">Geschmack, Aromen und Speisen sind für {n_g} unserer {len(WEINE)} Weine beschrieben, so wie Weintrinker bei Vivino sie erleben. Die übrigen erklärt Ihnen Jonas Volpert am Tisch.</p></div>
      </div>
      <button type="button" class="leise keller__neu" data-neu hidden>Auswahl zurücksetzen</button>
    </form>
    <p class="berater__zahl" aria-live="polite"><b data-treffer>{len(WEINE)}</b> <span data-treffer-t>Weine passen</span></p>
    <div class="wf-raster" data-weine></div>
    <div class="ka__weiter"><button type="button" class="knopf" data-mehr hidden>Mehr Weine zeigen {PFEIL}</button></div>
  </div>
  <template id="wf-zeichen">{zeichen}</template>
</section>
'''


def wein_dialog():
    return f'''<dialog class="fe ww" id="fe-wein" aria-label="Wein">
  <div class="ww__buehne">
    <div class="ww__land" data-w-land></div>
    <button class="fe__zu ww__zu" type="button" aria-label="Schliessen">{KREUZ}</button>
    <div class="ww__flasche" data-w-flasche></div>
    <div class="ww__flagge" data-w-flagge></div>
  </div>
  <div class="ww__inhalt">
    <div class="ww__kopf">
      <p class="ww__herkunft mono" data-w-herkunft></p>
      <h2 class="ww__name" data-w-titel>Wein</h2>
      <p class="ww__erz" data-w-erz></p>
    </div>
    <dl class="ww__angaben" data-w-angaben></dl>
    <div class="ww__teil ww__text" data-w-hk-t hidden><p class="mono">Woher er kommt</p><p data-w-hk></p></div>
    <div class="ww__teil ww__gut" data-w-gut-t hidden><p class="mono">Das Weingut</p><div data-w-gut></div></div>
    <div class="ww__teil ww__text" data-w-bes-t hidden><p class="mono">Was ihn ausmacht</p><p data-w-bes></p></div>
    <div class="ww__teil" data-w-glas-t hidden><p class="mono">Im Glas</p><div class="wg" data-w-glas></div></div>
    <div class="ww__teil" data-w-aromen-t hidden><p class="mono">Im Duft und am Gaumen</p><div class="ww__aromen" data-w-aromen></div></div>
    <div class="ww__teil" data-w-speisen-t hidden><p class="mono">Passt zu</p><ul class="ww__speisen" data-w-speisen></ul></div>
    <div class="ww__teil ww__stil" data-w-stil-t hidden><p class="mono">Der Weinstil</p><div data-w-stil></div></div>
    <p class="ww__nachweis" data-w-herkunftsnachweis hidden>Geschmack, Aromen und Speisen so, wie Weintrinker bei Vivino diesen Wein beschreiben; Weinstil nach Vivino.</p>
    <div class="ww__haus" data-w-haus hidden><p class="mono">Vom selben Weingut auf unserer Karte</p><div class="ww__liste" data-w-liste></div></div>
    <p class="fe__hinweis ww__hinweis">Geschmack und die passenden Gerichte stehen nicht in der Karte; Jonas Volpert, Gastgeber und Sommelier, berät Sie dazu am Tisch.</p>
    <div class="fe__senden">{knopf('Zur Reservierung bereitlegen', tag='button', dunkel=True, attr=' data-bereitlegen')}</div>
  </div>
</dialog>
'''


# ---------------------------------------------------------------- 4 Wein zum Gang
# Robert 19.10.2026: Fassung 4 «Jonas schenkt ein» aus _varianten/wein-gang-luxus.html (Runde 3, nach zwei abgelehnten Runden).
# Links Jonas und das Glas als Abzüge mit weissem Rand, rechts wählt der Gast die Küche seines Gerichts, und drei Flaschen fliegen als
# gedruckte Kärtchen von unten herein. Die Weine hängen an der Küche, nicht am einzelnen Gericht: je Gegend Weiss, Rot, Schaumwein
# (sonst Rosé), jeweils die Flasche am Ende des unteren Drittels der Preise; Fotos sonst nirgends auf karte.html.
WZG_LAND = {'Frankreich': ['Frankreich'], 'Italien': ['Italien'], 'Iberische Halbinsel': ['Spanien', 'Portugal'], 'Klassiker': ['Schweiz']}


def wzg_wahl(land):
    t = [w for w in WEINE if w['land'] in WZG_LAND[land] and any(f['gross'] == '0.7l' for f in w['flaschen']) and w['art'] != 'Süsswein']
    wahl = []
    for a in ['Weisswein', 'Rotwein', 'Champagner & Schaumwein', 'Rosé']:
        x = sorted([w for w in t if w['art'] == a], key=lambda w: w['flaschen'][0]['preis'])
        if x:
            wahl.append(x[len(x) // 3])
    return wahl[:3]


def wzg_art(w):
    if w['art'] == 'Champagner & Schaumwein':
        return 'Champagner' if w['region'] == 'Champagne' else 'Schaumwein'
    return w['art']


def wzg_karte(w, i):
    fl = ' · '.join(f'{f["gross"].replace(".", ",").replace("l", " l")} für {f["preis"]} Franken' for f in w['flaschen'])
    jahr = e(w['jahr']) if w['jahr'] else 'ohne Jahrgang'
    return (f'<button type="button" class="wzg4__k" data-wein="{w["id"]}" style="--i:{i}"><i>{e(wzg_art(w))} · {e(w["region"] or w["land"])}</i>'
            f'<strong>{jahr}</strong><b>{e(w["name"])}</b><span>{e(w["erzeuger"] or "")}</span><em>{fl}</em></button>')


def wein_zum_gang(foto):
    laender = [l['land'] for l in KARTE['laender']]
    wahl = ''.join(f'<button type="button" data-kue="{e(l)}" aria-pressed="{"true" if i == 0 else "false"}">{e(l)}</button>' for i, l in enumerate(laender))
    drei = ''.join(f'<div class="wzg4__drei" data-fuer="{e(l)}"{"" if i == 0 else " hidden"}>' + ''.join(wzg_karte(w, j) for j, w in enumerate(wzg_wahl(l))) + '</div>' for i, l in enumerate(laender))
    return f'''<section class="teil f-dunkel" id="wein-zum-gang" aria-label="Wein zum Gang">
  <div class="innen wzg4" data-wzg>
    <div class="wzg4__abz" data-r="bild">
      <div class="wzg4__a wzg4__a1">{foto('jonas', '(max-width:900px) 70vw, 28vw', r=False)}</div>
      <div class="wzg4__a wzg4__a2">{foto('glas', '(max-width:900px) 44vw, 16vw', r=False)}</div>
      <p class="wzg4__name">Jonas Volpert<small>Gastgeber und Sommelier</small></p>
    </div>
    <div class="wzg4__r">
      <h2 class="t2" data-schlitz>Ein Glas <em>zu jedem Gang.</em></h2>
      <p class="lauf" data-r="text">Wählen Sie, woher Ihr Gericht kommt. Wir legen Ihnen drei Flaschen aus derselben Gegend hin, aus unserer Weinkarte. Welche am besten passt, sagt Ihnen Jonas Volpert am Tisch.</p>
      <div class="wzg4__wahl" data-r="text"><p>Ihr Gericht kommt aus</p><div role="group" aria-label="Ihr Gericht kommt aus">{wahl}</div></div>
      {drei}
    </div>
  </div>
</section>
'''


# ---------------------------------------------------------------- 5 Abend zusammenstellen
def bildwahl(name, werte, start=None):
    """Auswahl als kleine Bildkarten (Robert 20.10.2026: «mit so kleinen Miniaturbildern … dass es richtig Spass macht»).
    werte: (wert, titel, bild, zusatz). Nach dem input steht der Text, den der Zettel liest («Titel · Zusatz»)."""
    def karte(w, t, n, z):
        zs = f'<i><span class="vh"> · </span>{e(z)}</i>' if z else ''
        return (f'<label class="bw"><input type="radio" name="{e(name)}" value="{e(w)}"{" checked" if w == start else ""}>'
                f'<span class="bw__k"><img src="assets/img/{n}-480.webp" alt="" width="480" height="360" decoding="async"><b>{e(t)}</b>{zs}</span></label>')
    return f'<div class="bws" role="radiogroup" style="--n:{len(werte)}">' + ''.join(karte(*x) for x in werte) + '</div>'


def abend_inhalt():
    alacarte = ''.join(f'<div class="ab-land"><h4 class="ab-land__t">{e(l["land"])}</h4><div class="grs">' + ''.join(f'<label class="gr"><input type="checkbox" name="gerichte" value="{e(g["name"])}" data-preis="{g["preis"]}"><span class="gr__k"><i aria-hidden="true"></i><b>{e(g["name"])}</b><em>{g["preis"]}</em></span></label>' for g in l['gerichte']) + '</div></div>' for l in KARTE['laender'])
    JZ = {'Frühling': 'jz-fruehling', 'Sommer': 'jz-sommer', 'Herbst': 'jz-herbst'}
    menues = [('alacarte', 'À la carte', 'tb-teller', 'nach Wahl'), ('lunch', 'Lunch-Menü', 'suppe', f'{LUNCH["preis_zahl"]} Franken')] + [(f'bankett-{m["name"].lower()}', f'Bankettmenü {m["name"]}', JZ.get(m['name'], 'gaststube'), f'{m["preis"]} Franken') for m in BANKETT['menues']]
    anlass = [('Essen zu zweit', 'Essen zu zweit', 'tb-glas', ''), ('Mit Freunden', 'Mit Freunden', 'lounge', ''), ('Familienfeier', 'Familienfeier', 'torte', ''), ('Firmenanlass', 'Firmenanlass', 'regal', ''), ('Lunch', 'Lunch', 'suppe', '')]
    plaetze = [('Drinnen in der Gaststube', 'Gaststube', 'gaststube', 'drinnen'), ('Draussen auf der Terrasse', 'Terrasse', 'platanen', 'draussen'), ('An der Lästermeile', 'Lästermeile', 'bar', 'an der Bar'), ('Eine der zwei Etagen', 'Eine Etage', 'haus', 'für Gruppen')]
    allerg = chips('allergene', [(k, n) for k, n in ALLERGENE] + [('VEG', 'vegetarisch')], mehrfach=True)
    return f'''<section class="teil f-hell" id="zusammenstellen" aria-label="Abend zusammenstellen">
  <div class="innen az">
    <form class="az__form fe__form" data-abend novalidate>
      <fieldset class="az__schritt"><legend>Der Anlass</legend>{bildwahl('anlass', anlass, 'Essen zu zweit')}</fieldset>
      <fieldset class="az__schritt"><legend>Wann und wie viele</legend><div class="felder">{kalender_feld()}<div class="feld" data-wahl="uhrzeit"><span>Uhrzeit</span><button class="wahl-k" type="button" aria-expanded="false"><span>Uhrzeit wählen</span></button><div class="wahl-l">{zeiten()}</div><input type="hidden" name="uhrzeit"></div><div class="feld az__pers"><label for="a-pers">Personen</label><div class="zaehler"><button type="button" data-pers="-1" aria-label="Eine Person weniger">−</button><input id="a-pers" name="personen" inputmode="numeric" value="2" autocomplete="off"><button type="button" data-pers="1" aria-label="Eine Person mehr">+</button></div></div></div></fieldset>
      <fieldset class="az__schritt"><legend>Der Platz</legend>{bildwahl('platz_wahl', plaetze, 'Draussen auf der Terrasse')}<input type="hidden" name="platz" value="Draussen auf der Terrasse"></fieldset>
      <fieldset class="az__schritt"><legend>Das Menü</legend>{bildwahl('menue', menues, 'alacarte').replace('class="bws"', 'class="bws bws--menue"', 1)}</fieldset>
      <fieldset class="az__schritt az__gerichte" data-alacarte><legend>Ihre Gerichte</legend><p class="az__lead">Alle Gerichte unserer Karte, geordnet wie auf der Karte: {e(', '.join(l['land'] for l in KARTE['laender'][:-1]) + ' und ' + KARTE['laender'][-1]['land'])}. Kreuzen Sie an, was Sie essen möchten, der Zettel rechts rechnet mit.</p><div class="az__alacarte">{alacarte}</div></fieldset>
      <fieldset class="az__schritt" id="az-wein"><legend>Der Wein</legend><div class="flasche" data-flasche><img class="flasche__bild" src="assets/img/wein-480.webp" alt="" width="480" height="360" loading="lazy" decoding="async"><div class="flasche__leer">Noch keine Flasche gewählt. <a href="weinkarte.html?von=abend#berater">Im Weinberater auswählen</a></div><div class="flasche__voll" hidden><b data-f-name></b><small data-f-info></small><em>wird für Sie bereitgelegt</em><button type="button" class="leise" data-f-weg>Entfernen</button></div><input type="hidden" name="flasche"></div></fieldset>
      <fieldset class="az__schritt"><legend>Allergien und Wünsche</legend>{allerg}<div class="feld" style="margin-top:16px"><label for="a-wunsch">Wünsche</label><textarea id="a-wunsch" name="wunsch"></textarea></div></fieldset>
      <fieldset class="az__schritt"><legend>Wie erreichen wir Sie</legend><div class="felder"><div class="feld"><label for="a-name">Name</label><input id="a-name" name="name" autocomplete="name" required></div><div class="feld"><label for="a-kontakt">Telefon oder E-Mail</label><input id="a-kontakt" name="kontakt" autocomplete="email" required></div></div></fieldset>
    </form>
    <aside class="az__zettel" aria-label="Ihr Abend">
      <div class="zettel"><div class="zettel__blatt">
        <p class="zettel__haus">{e(HAUS['name'])}</p>
        <p class="zettel__titel">Ihr Abend</p>
        <div class="zettel__bilder" data-zettel-bilder aria-hidden="true"></div>
        <dl data-zettel></dl>
        <div class="zb" data-zettel-schoen></div>
        <p class="zettel__summe" data-summe hidden></p>
        <button class="knopf knopf--dunkel" type="button" data-abend-senden>Anfrage senden {PFEIL}</button>
        <p class="fe__hinweis">Designstudie: In diesem Entwurf wird nichts verschickt.</p>
        <div class="zettel__danke" hidden><h3>Vielen Dank.</h3><p>Ihr Abend liegt bei uns. Wir melden uns, um alles in Ruhe zu besprechen.</p></div>
      </div></div>
    </aside>
  </div>
</section>
'''


# ---------------------------------------------------------------- 7 + 11 Gutschein als gestaltete Karte, für das Schlössli, das Schäfli oder beide
def gutschein_inhalt():
    betraege = [('50', '50'), ('100', '100'), ('150', '150'), ('200', '200'), ('300', '300')]
    return f'''<section class="teil f-hell" id="gestalten" aria-label="Gutschein gestalten">
  <div class="innen gs">
    <form class="gs__form" data-gutschein onsubmit="return false">
      <div class="gs__kopf"><p class="gs__haus">{e(HAUS['name'])}</p><h2 class="gs__titel">Ihr Gutschein</h2><span class="gs__strich" aria-hidden="true"></span></div>
      <div class="berater__z"><span class="mono">Betrag in Franken</span><div class="gs__betrag">{chips('betrag', betraege).replace('value="100">', 'value="100" checked>', 1)}<div class="feld gs__frei"><label class="vh" for="gs-frei">Eigener Betrag</label><input id="gs-frei" name="frei" inputmode="numeric" autocomplete="off" placeholder="anderer"></div></div></div>
      <div class="berater__z"><span class="mono">Einzulösen</span>{chips('haus', [('schloessli', 'Im Schlössli'), ('schaefli', 'In der Taverne zum Schäfli'), ('beide', 'In beiden Häusern')], erste=True)}</div>
      <div class="felder">
        <div class="feld"><label for="gs-fuer">Für</label><input id="gs-fuer" name="fuer" autocomplete="off" maxlength="40"></div>
        <div class="feld"><label for="gs-von">Von</label><input id="gs-von" name="von" autocomplete="off" maxlength="40"></div>
        <div class="feld feld--ganz"><label for="gs-satz">Ein paar Worte</label><textarea id="gs-satz" name="satz" maxlength="160"></textarea></div>
      </div>
      <div class="knoepfe gs__knoepfe">{knopf('Gutschein bestellen', tag='button', dunkel=True, attr=' data-fenster="fe-gutschein"')}<button class="leise" type="button" data-drucken>Drucken</button></div>
    </form>
    <div class="gs__buehne">
      <div class="gkarte" data-gkarte>
        <div class="gkarte__kopf"><span class="gkarte__zeichen" aria-hidden="true">{ZEIGER}</span><span class="mono" data-g-haus>Wirtschaft am Schlössli · Bottighofen</span></div>
        <p class="gkarte__titel">Gutschein</p>
        <p class="gkarte__betrag"><b data-g-betrag>100</b><span>Franken</span></p>
        <p class="gkarte__satz" data-g-satz>Für einen Abend unter der Platane.</p>
        <div class="gkarte__fuss"><span>Für <b data-g-fuer>…</b></span><span>Von <b data-g-von>…</b></span></div>
        <span class="gkarte__linie" aria-hidden="true"></span>
      </div>
      <p class="fe__hinweis gs__hinweis">Ob ein Gutschein in beiden Häusern gilt, klären wir mit dem Haus (Idee). Designstudie: nichts wird bezahlt oder verschickt.</p>
    </div>
  </div>
</section>
'''


# ---------------------------------------------------------------- 8 Veranstaltungskalender mit Plätze-Anfrage
def kalender():
    # Plakatwand (Robert 19.10.2026, 21:1x: Fassung 5 aus _varianten/anlaesse-15-runde1.html, «rechts noch viel zu viel Raum unten»):
    # der kommende Anlass als grosses Plakat, die vergangenen als vier kleine Plakate daneben, die zusammen genau so hoch sind wie das grosse.
    # Fotos der Kreuzfahrt: excellence.ch (Twerenbold Reisen), nur Designstudie, Herkunft _quelle/extern/excellence/herkunft.json.
    mon = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    termine = {'Excellence Gourmetkreuzfahrt': (11, '13.–15.'), 'Ehemaligen Lunch': (9, '6.'), 'Fantastical / Seenachtfest': (8, '7.–8.'), 'Kitchen Party im Schäfli': (4, '30.'), '4-Hands-Lunch mit Patrick Stier': (2, '22.')}
    bild = {'Excellence Gourmetkreuzfahrt': ('kf-deck-abend', [800, 1200, 1800], 'Das Sonnendeck der Excellence in der Abenddämmerung', '50% 50%'),
            'Ehemaligen Lunch': ('platanen', [800, 1200, 1800], 'Gedeckte Tische unter den Platanen am Hafen', '50% 60%'),
            'Fantastical / Seenachtfest': ('vf-feuerwerk', [800, 1200], 'Feuerwerk über dem Konstanzer Trichter', '58% 40%'),
            'Kitchen Party im Schäfli': ('kp-party', [800, 1179], 'Kitchen Party in der Gasse vor dem Schäfli am Abend', '50% 50%'),
            '4-Hands-Lunch mit Patrick Stier': ('pa-teller', [800, 1080], 'Hauptgang von Patrick Stier im Papageno', '50% 50%')}

    def img(a, sizes):
        n, br, alt, pos = bild[a['titel']]
        return f'<img src="assets/img/{n}-{br[0]}.webp" srcset="{", ".join(f"assets/img/{n}-{w}.webp {w}w" for w in br)}" sizes="{sizes}" alt="{e(alt)}" style="object-position:{pos}" loading="lazy" decoding="async">'

    kommt = next(a for a in HAUS['anlaesse'] if a['bevorstehend'])
    vorbei = sorted((a for a in HAUS['anlaesse'] if a is not kommt), key=lambda a: -termine[a['titel']][0])
    # Jede Karte trägt dieselben Angaben, damit gross und klein tauschen können (Robert 19.10.2026, 21:1x: blaues Band auch auf den kleinen, Tausch beim Antippen)
    unter = {'Excellence Gourmetkreuzfahrt': 'Four-Hands-Dinner mit Dieter Koschina &amp; Monika Huber'}
    def karte(a, sizes):
        kurz = f'{termine[a["titel"]][1]} {mon[termine[a["titel"]][0] - 1]}'
        u = unter.get(a['titel']) or e(a['text'][0])
        return (f'{img(a, sizes)}<span class="ap__schrift"><span class="mono"><span class="ap__lang">{e(a["datum"])}</span><span class="ap__kurz">{e(kurz)}</span></span>'
                f'<span class="ap__titel">{e(a["titel"])}</span>' + (f'<span class="ap__unter">{u}</span>' if u else '') + '</span>')
    klein = ''.join(f'<button type="button" class="ap__p" style="--r:{r}deg" data-termin="{e(a["titel"])}">{karte(a, "(max-width:900px) 46vw, 300px")}</button>'
                    for a, r in zip(vorbei, [-2, 1.5, -1, 2]))
    return f'''<section class="teil f-tapete" id="kalender" aria-label="Kalender 2026">
  <div class="innen">
    <div class="ab-satz"><h2 class="t2" data-schlitz>Angeschlagen <em>am Hafen.</em></h2><p class="lauf" data-r="text">Alle Anlässe 2026 auf einen Blick. Tippen Sie einen an, und fragen Sie Plätze an.</p></div>
    <div class="ap">
      <button type="button" class="ap__gross" data-termin="{e(kommt["titel"])}" data-r="bild">{karte(kommt, "(max-width:900px) 92vw, 640px")}</button>
      <div class="ap__r"><div class="ap__klein" data-r="bild">{klein}</div>
      <div class="kt-detail" data-termin-detail aria-live="polite"></div></div>
    </div>
  </div>
</section>
<dialog class="fe" id="fe-termin" aria-label="Der Anlass">
  <div class="fe__kopf2"><h2 data-t-titel></h2><button class="fe__zu" type="button" aria-label="Schliessen">{KREUZ}</button></div>
  <div class="fe__inhalt"><p class="mono" data-t-zeit style="color:var(--himmel-t);margin:0 0 18px"></p><div data-t-text></div><div class="knoepfe" data-t-knoepfe style="margin-top:22px"></div></div>
</dialog>
<dialog class="fe" id="fe-plaetze" aria-label="Plätze anfragen">
  <div class="fe__kopf2"><h2>Plätze anfragen</h2><button class="fe__zu" type="button" aria-label="Schliessen">{KREUZ}</button></div>
  <div class="fe__inhalt">
    <form class="fe__form" novalidate>
      <p data-p-titel></p>
      <div class="felder">
        <div class="feld"><label for="p-pers">Personen</label><input id="p-pers" name="personen" inputmode="numeric" autocomplete="off" required></div>
        <div class="feld"><label for="p-name">Name</label><input id="p-name" name="name" autocomplete="name" required></div>
        <div class="feld feld--ganz"><label for="p-kontakt">Telefon oder E-Mail</label><input id="p-kontakt" name="kontakt" autocomplete="email" required></div>
        <div class="feld feld--ganz"><label for="p-wunsch">Wünsche, Allergien</label><textarea id="p-wunsch" name="wunsch"></textarea></div>
        <input type="hidden" name="anlass">
      </div>
      <div class="fe__senden"><button class="knopf knopf--dunkel" type="submit">Plätze anfragen {PFEIL}</button></div>
      <p class="fe__hinweis">Designstudie: In diesem Entwurf wird nichts verschickt.</p>
    </form>
    <div class="fe__danke"><h3>Vielen Dank.</h3><p>Wir melden uns, sobald wir Ihre Plätze bestätigen können.</p><p class="fe__hinweis">Designstudie: Diese Anfrage wurde nicht verschickt.</p></div>
  </div>
</dialog>
'''


# ---------------------------------------------------------------- 9 Blick in die Küche und 11 das Schwesterhaus
def kueche_blick(foto):
    return f'''<section class="teil f-dunkel" id="kueche" aria-label="Blick in die Küche">
  <div class="innen bk">
    <div class="bk__t">
      <h2 class="t2" data-schlitz>Ein Blick <em>in die Küche.</em></h2>
      <p class="lauf" data-r="text">{e(HAUS['satz_team'])}</p>
      <p class="lauf" data-r="text" style="--i:1">{e(HAUS['weg_moni'])}</p>
      <blockquote class="bk__ck" data-r="text" style="--i:2"><p>«Wegbereiter, Ratgeber, Inspirateur, Motivator in der Küche und im Ausgang.»</p><cite class="mono">So steht Christian Kuchler, Pächter des Schlössli, in der Einladung zum Ehemaligen Lunch</cite></blockquote>
    </div>
    <div class="bk__bilder"><div class="bk__sp bk__sp--l" data-gegen="-.45">{foto('ig-dessert', '(max-width:900px) 46vw, 18vw', 'bk__x bk__c', r=False)}{foto('ig-herd', '(max-width:900px) 46vw, 18vw', 'bk__a', alt='In der Küche am Herd')}{foto('ig-pasta', '(max-width:900px) 46vw, 18vw', 'bk__c', alt='Tortelloni werden von Hand geformt')}{foto('fleisch', '(max-width:900px) 46vw, 18vw', 'bk__x bk__a', r=False)}</div><div class="bk__sp bk__sp--r" data-gegen=".45">{foto('thon', '(max-width:900px) 46vw, 18vw', 'bk__x bk__d', r=False)}{foto('ig-teller', '(max-width:900px) 46vw, 18vw', 'bk__b', alt='Am Pass werden die Teller angerichtet')}{foto('sauce', '(max-width:900px) 46vw, 18vw', 'bk__d')}{foto('fisch', '(max-width:900px) 46vw, 18vw', 'bk__x bk__b', r=False)}</div></div>
  </div>
</section>
'''


def schwester():
    s = HAUS['schwester']
    def ehre(lg, w, h, alt, wert, i, cls=''):
        return f'<div class="sw__ehre" style="--i:{i}"><span class="sw__lg{cls}"><img src="assets/img/{lg}" width="{w}" height="{h}" alt="{alt}" loading="lazy"></span><b>{wert}</b></div>'
    return f'''<section class="teil f-tapete" id="schaefli" aria-label="Zwei Häuser">
  <div class="innen sw">
    <article class="sw__karte" data-r="text">
      <figure class="sw__bild"><img src="assets/img/haus-1200.webp" srcset="assets/img/haus-800.webp 800w, assets/img/haus-1200.webp 1200w, assets/img/haus-1800.webp 1800w" sizes="(max-width:900px) 92vw, 600px" width="1200" height="800" alt="Die Wirtschaft am Schlössli im ehemaligen Hafenmeistergebäude" loading="lazy" decoding="async"></figure>
      <p class="mono">Hier am See · Bottighofen</p>
      <h2 class="t2" data-schlitz>Wirtschaft<br><em>am Schlössli.</em></h2>
      <div class="sw__tafel">
        {ehre('ehre-gaultmillau-15.webp', 292, 240, 'GaultMillau Guide Schweiz, 15 Punkte', '<span data-zahl="15">15</span> Punkte', 0)}
        {ehre('ehre-michelin-2025.webp', 240, 240, 'Michelin 2025', 'Favorit', 1, ' sw__lg--rund')}
        {ehre('ehre-falstaff.svg', 239, 71, 'Falstaff', '<span data-zahl="91">91</span> Punkte', 2, ' sw__lg--falstaff')}
      </div>
      <p class="lauf">Mediterrane Küche von Monika Huber, direkt im Hafen. Jonas Volpert ist Sommelier und Gastgeber.</p>
      <div class="knoepfe">{knopf('Tisch am See', HAUS['reservation'], dunkel=True, attr=' rel="noopener" target="_blank"')}<a class="leise" href="karte.html">Zur Karte</a></div>
    </article>
    <article class="sw__karte" data-r="text" style="--i:1">
      <figure class="sw__bild"><img src="assets/img/schaefli-1200.webp" srcset="assets/img/schaefli-800.webp 800w, assets/img/schaefli-1200.webp 1200w, assets/img/schaefli-1800.webp 1800w" sizes="(max-width:900px) 92vw, 600px" width="1200" height="800" alt="Die Taverne zum Schäfli in Wigoltingen am Abend, die Fenster erleuchtet" loading="lazy" decoding="async"></figure>
      <p class="mono">Die Schwester · {e(s['ort'])}</p>
      <h2 class="t2" data-schlitz>Taverne<br><em>zum Schäfli.</em></h2>
      <div class="sw__tafel">
        {ehre('ehre-schaefli-michelin.webp', 900, 255, 'Michelin Guide, zwei Sterne', 'Zwei Sterne', 0)}
        {ehre('ehre-schaefli-gaultmillau.webp', 700, 643, 'GaultMillau Guide Schweiz, 18 Punkte', '<span data-zahl="18">18</span> Punkte', 1)}
        {ehre('ehre-falstaff.svg', 239, 71, 'Falstaff', '<span data-zahl="98">98</span> Punkte', 2, ' sw__lg--falstaff')}
      </div>
      <p class="lauf">Im Schäfli in Wigoltingen kocht Christian Kuchler. Von dort kamen Monika Huber, früher seine Sous-Chefin, und Jonas Volpert, Sommelier und Restaurantleiter, an den See.</p>
      <div class="knoepfe">{knopf('Zum Schäfli', s['url'], dunkel=True, attr=' rel="noopener" target="_blank"')}<a class="leise" href="gutschein.html">Gutschein für beide Häuser</a></div>
    </article>
  </div>
</section>
'''


# ---------------------------------------------------------------- 10 Der See: Terrasse heute, Platz draussen, Anreise über das Wasser
def see(foto, nw):
    lat, lon = HAUS['koordinaten']
    zu = ','.join(f'{a}/{b}' for a, b in HAUS['ferien_iso'])
    return f'''<section class="teil f-dunkel" id="see" aria-label="Der See heute">
  <div class="innen see" data-see data-lat="{lat}" data-lon="{lon}" data-zu="{zu}">
    <div class="see__wasser">
      {foto('ig-hafen', '(max-width:900px) 92vw, 34vw', 'see__hoch')}{nw('ig-hafen')}
      <p class="see__von">Vom Wasser</p>
      <h3>Über das Wasser</h3>
      <p class="lauf">Die Wirtschaft liegt direkt im Hafen von Bottighofen; am Hafen liegen die Schifflände, der Bootshafen und die Bootstankstelle. Ob ein Kursschiff anlegt und wo Gäste mit dem eigenen Boot festmachen dürfen, fragen Sie uns gerne vorab.</p>
    </div>
    <div class="see__land">
      <h2 class="t2" data-schlitz>Der See <em>heute.</em></h2>
      {foto('start', '(max-width:900px) 92vw, 56vw', 'see__breit')}{nw('start')}
      <p class="see__von">Vom Land</p>
      <div class="see__zahlen" data-r="text">
        <p><b data-see-sonne>–</b><span>Sonnenuntergang in Bottighofen</span></p>
        <p><b data-see-offen>–</b><span data-see-offen-text>Terrasse</span></p>
      </div>
      <div class="knoepfe" data-r="text" style="--i:1">{knopf('Platz draussen wünschen', tag='button', dunkel=True, attr=' data-fenster="fe-reservation" data-vorwahl="platz=Draussen auf der Terrasse"')}</div>
    </div>
  </div>
</section>
'''
