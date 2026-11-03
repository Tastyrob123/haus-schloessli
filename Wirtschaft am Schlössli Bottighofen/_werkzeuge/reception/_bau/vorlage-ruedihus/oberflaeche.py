#!/usr/bin/env python3
"""Der Gastgeber · Landgasthof Ruedihus: Umstellung auf die Werkzeug-Oberfläche «Die Bühne» (Werkbank-Chat 17.10.2026, Signal Oberchef über Chef-Chat).
Paket assets/oberflaeche (aus _Werkzeuge/stamm/oberflaeche, dort UMSTELLUNG.md), Kleid kleid/ruedihus.*. Vorbild der Ausführung: Der Gastgeber des
Berghotel Gasterntal (nur gelesen). Ersetzt nur Rahmen (Kopf, Rand, Leiste), Startbild und Übersicht; jede Funktion, jeder Weg, jede Id bleibt.
Läuft als letzter Schritt in alle.sh; bricht ab, wenn eine Stelle nicht trifft; zweiter Lauf erkennt den Stand und tut nichts."""
import os, re, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MERK = '/* Werkzeug-Oberfläche «Die Bühne» (oberflaeche.py) */'


def lies(n):
    with open(os.path.join(R, n), encoding='utf-8') as f:
        return f.read()


def schreib(n, t):
    with open(os.path.join(R, n), 'w', encoding='utf-8') as f:
        f.write(t)


def tausch(t, alt, neu, n=1, was=''):
    if t.count(alt) != n:
        sys.exit(f'oberflaeche.py: Stelle trifft nicht ({was or alt[:60]!r}, {t.count(alt)}×)')
    return t.replace(alt, neu)


def block(t, anfang, ende, neu, was):
    """ersetzt von der Zeile, die mit anfang beginnt, bis vor die Zeile, die mit ende beginnt"""
    a = t.find('\n' + anfang)
    b = t.find('\n' + ende, a + 1)
    if a < 0 or b < 0:
        sys.exit(f'oberflaeche.py: Block trifft nicht ({was})')
    return t[:a + 1] + neu.rstrip('\n') + '\n' + t[b + 1:]


# ---------- reception.js ----------
js = lies('reception.js')
if MERK in js:
    print('oberflaeche.py: Der Gastgeber ist schon umgestellt.')
else:
    RAHMEN = MERK + r"""
/* Kopf, Rand, Leiste und Startbild aus dem Paket der Werkzeuge des Hauses (assets/oberflaeche, Rahmen «Die Bühne», kleid/ruedihus.*):
   gleich wie in den anderen Werkzeugen des Ruedihus. Ids, data-gehe und Handler bleiben (UMSTELLUNG.md). */
const WEGE = { anleitung: 'anleitung.html', pruefung: 'pruefung.html' };
const SB_FOTO = { eingang: 'stube-tuer', gefragt: 'stube-kerze', nachgetragen: 'stube-lang', wissen: 'stube-tuer' };   // Bühne je Ansicht, Fotos des Hauses
/* Knöpfe in Startbild und Bühne im Stil des Pakets (gleiche Ids und data-Attribute) */
const woKn = h => String(h || '').replace(/class="kn kn--(gold|linie)( glanz-kn)?"/g, (m, a) => `class="wo-kn wo-kn--${a === 'gold' ? 'gold' : 'hell'}"`)
  .replace(/class="kn"/g, 'class="wo-kn wo-kn--hell"').replace(/(<(?:a|button) class="wo-kn[^"]*"[^>]*>)([^<]+)<i>/g, '$1<span>$2</span><i>');
function kopfLeiste() {
  const u = S.ue;
  $('#kopf').innerHTML = WO.kopf({ werkzeug: 'gaeste', unter: 'Gäste im Chat', titel: TITEL[S.ansicht] || WO.name('gaeste'),
    stand: u.anfragen_neu ? mal(u.anfragen_neu, 'Eine neue Anfrage', 'neue Anfragen') : 'Keine neuen Anfragen',
    pruefung: WEGE.pruefung, anleitung: WEGE.anleitung, website: '../../index.html', marke: 'data-gehe="start"' });
  const r = $('#kopf .wo-kopf__r');
  if (r) r.insertAdjacentHTML('afterbegin', WO.knopf('Chat ausprobieren', 'chat', 'hell', { id: 'k-probe', klein: true }) + '<span class="wo-trenn"></span>');
  $$('#kopf [data-gehe]').forEach(x => x.onclick = e => { e.preventDefault(); gehe(x.dataset.gehe); });
  const kp = $('#k-probe'); if (kp) kp.onclick = probe;
}
function rand() {
  const u = S.ue, an = S.ansicht;
  const e = (key, text, zahl = 0) => ({ text, zahl, an: an === key, attr: `data-gehe="${key}"` });
  $('#rand').innerHTML = WO.rand([{ titel: '', eintraege: [e('start', 'Übersicht')] },
    { titel: 'Für das Team', eintraege: [e('eingang', 'Eingang', u.anfragen_neu), e('gefragt', 'Das wurde gefragt', u.ohne_antwort), e('nachgetragen', 'Vom Team nachgetragen')]
      .concat(S.wissenDa ? [e('wissen', 'Das weiss der Chat', S.wissenNeu || 0)] : []) }], WEGE);
  const w = $('#rand .wo-rand__wege'), pf = WO.ic('pfeil');
  if (w) {   // die bisherigen Wege: Chat auf der Website, Zimmermappe, So arbeitet der Chat, Anleitung, Prüfung, Die Stube; dazu «Chat ausprobieren» fürs Handy
    w.insertAdjacentHTML('afterbegin', `<a href="../../index.html" target="_blank" rel="noopener">Chat auf der Website${pf}</a><a href="../../mappe.html" target="_blank" rel="noopener">Zimmermappe${pf}</a><a href="../../rezeption/" target="_blank" rel="noopener">So arbeitet der Chat${pf}</a>`);
    w.insertAdjacentHTML('beforeend', `<a href="${STUBE}">${esc(WO.name('zentrale'))}${pf}</a><button class="wo-rand__probe" type="button" data-probe>Chat ausprobieren${WO.ic('chat')}</button>`);
  }
  $$('#rand [data-gehe]').forEach(b => b.onclick = () => gehe(b.dataset.gehe));
  $$('#rand [data-probe]').forEach(b => b.onclick = probe);
  kopfLeiste();
}
function leiste() {
  const u = S.ue;
  $('#leiste').innerHTML = WO.leiste({
    titel: u.anfragen_neu ? mal(u.anfragen_neu, 'Eine neue Anfrage', 'neue Anfragen') + ' im Eingang' : u.anfragen_offen ? mal(u.anfragen_offen, 'Eine Anfrage', 'Anfragen') + ' noch offen' : 'Der Eingang ist leer',
    satz: (u.ohne_antwort ? mal(u.ohne_antwort, 'Eine Frage', 'Fragen') + ' ohne Antwort. Einmal nachtragen, dann antwortet der Chat selbst.' : 'Jede Frage an den Chat hatte eine Antwort.') + (u.letzte_frage ? ' Letzte Frage ' + zeit(u.letzte_frage) + '.' : ''),
    knoepfe: WO.knopf('Neu laden', 'verlauf', 'glas', { id: 'l-neu', klein: true }) + WO.knopf('Zum Eingang', 'rechts', u.anfragen_neu ? 'gold' : 'hell', { id: 'l-eingang', klein: true }) });
  $('#l-neu').onclick = () => frisch(true);
  $('#l-eingang').onclick = () => gehe('eingang');
}
function kopf(mono, titel, satz, knoepfe = '', foto = '') {   // Bühne jeder Ansicht = Startbild «buehne» des Pakets mit dem Foto der Ansicht
  return WO.startbild({ werkzeug: 'gaeste', art: 'buehne', zier: esc(WO.name('gaeste') + ' · ' + mono), h1: titel, satz, knoepfe: woKn(knoepfe),
    foto: '/assets/img/' + (foto || SB_FOTO[S.ansicht] || 'haus-fassade') + '-l.webp' });
}
"""
    js = block(js, 'function kopfLeiste() {', 'function gehe(', RAHMEN, 'Rahmen')

    # Übersicht: Startbild «voll», Lage und Überschriften des Pakets
    js = tausch(js, """  const u = S.ue, h = new Date().getHours();
  const gruss = h >= 5 && h < 11 ? 'Guten Morgen.' : h >= 11 && h < 18 ? 'Guten Tag.' : 'Guten Abend.';""", "  const u = S.ue, gruss = WO.gruss();", was='Gruss')
    js = tausch(js, "  return kopf('Der Gastgeber · Landgasthof Ruedihus Kandersteg', `${gruss} <em>Wer hat geschrieben?</em>`,\n",
                "  return WO.startbild({ werkzeug: 'gaeste', art: 'voll', h1: `${gruss} <em>Wer hat geschrieben?</em>`,\n    satz: ", was='Startbild')
    js = tausch(js, "Verschickt wird nur, was Sie selbst schicken.',\n    `<a class=\"kn kn--linie\" href=\"anleitung.html\" target=\"_blank\" rel=\"noopener\">Anleitung<i>${PF}</i></a>`) +\n",
                "Verschickt wird nur, was Sie selbst schicken.',\n    knoepfe: WO.knopf('Anleitung', 'buch', 'gold', { href: 'anleitung.html', neu: true }) }) +\n", was='Startbild-Knopf')
    alt_lage = re.search(r"\n    `<div class=\"lage platte\">\n(.*?)\n    </div>\n    \$\{S\.anfragen\.length", js, re.S)
    if not alt_lage:
        sys.exit('oberflaeche.py: Lage trifft nicht')
    lage = alt_lage.group(1)
    for alt, neu in ((' <div class="lg"><span class="mono">Eingang</span>', ' <div class="wo-lg"><i class="wo-lg__z">${WO.ic(\'mail\')}</i><span class="wo-mk">Eingang</span>'),
                     (' <div class="lg"><span class="mono">Ohne Antwort</span>', ' <div class="wo-lg"><i class="wo-lg__z">${WO.ic(\'chat\')}</i><span class="wo-mk">Ohne Antwort</span>'),
                     (' <div class="lg"><span class="mono">Gefragt</span>', ' <div class="wo-lg"><i class="wo-lg__z">${WO.ic(\'suche\')}</i><span class="wo-mk">Gefragt</span>')):
        lage = tausch(lage, alt, neu, was='Lage ' + alt[30:44])
    lage = re.sub(r"</b><span>(.*?)</span><button type=\"button\"", r'</b><p>\1</p><button class="wo-lk" type="button"', lage)
    if lage.count('wo-lk') != 3:
        sys.exit('oberflaeche.py: Lage-Wege treffen nicht')
    js = js[:alt_lage.start(1)] + lage + js[alt_lage.end(1):]
    js = tausch(js, '\n    `<div class="lage platte">\n', '\n    `<div class="wo-lage">\n', was='Lage-Behälter')
    js = tausch(js, '<h2 class="zw">Zuletzt <em>angefragt</em></h2>', '<h2 class="wo-zw">Zuletzt <em>angefragt</em></h2>')
    js = tausch(js, '<h2 class="zw">Zuletzt <em>gefragt</em></h2>', '<h2 class="wo-zw">Zuletzt <em>gefragt</em></h2>')

    # Arten als Kacheln des Pakets (wo-aufg), gleiche Ziele
    ARTEN = r"""function arten() {   // die Arten als Kacheln mit Foto (wo-aufg des Pakets), wie viele Anfragen je Art im Eingang liegen
  const Z = { zimmer: 'haus', tisch: 'blatt', feier: 'siegel', tagung: 'schild', gutschein: 'karte', spa: 'uhr', aufenthalt: 'rechts', programm: 'welt', nachricht: 'mail' };
  return `<h2 class="wo-zw">Nach <em>Art</em></h2><div class="wo-aufg">${Object.keys(ART).map(k => { const l = S.anfragen.filter(a => a.art === k), o = l.filter(a => a.status !== 'erledigt').length;
    return `<button class="wo-ag" type="button" data-gehe="eingang"><span class="wo-ag__b"><img src="../../assets/img/${ARTBILD[k] || ARTBILD.zimmer}.webp" alt="" width="900" height="675" decoding="async"></span><span class="wo-ag__t"><i class="wo-ag__z">${WO.ic(Z[k] || 'mail')}</i><b>${ART_LANG[k]}</b><span>${l.length ? mal(l.length, 'eine Anfrage', 'Anfragen') + (o ? ' · ' + o + ' offen' : '') : 'noch keine'}</span></span></button>`; }).join('')}</div>`;
}
"""
    js = block(js, 'function arten() {', '/* ---------- Eingang', ARTEN + '\n', 'Arten')
    schreib('reception.js', js)
    print('oberflaeche.py: reception.js umgestellt.')

# ---------- index.html ----------
h = lies('index.html')
if 'wo-app' in h:
    print('oberflaeche.py: index.html ist schon umgestellt.')
else:
    h = tausch(h, '<script src="studio/fehlermelder.js?v=2"></script>\n',
               '<script src="studio/fehlermelder.js?v=2"></script>\n<script src="/assets/oberflaeche/kleid/ruedihus.js?v=2"></script>\n')
    h = tausch(h, '<link rel="stylesheet" href="ruedihus.css?v=4">\n',
               '<link rel="stylesheet" href="ruedihus.css?v=4">\n<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v=1">\n'
               '<link rel="stylesheet" href="/assets/oberflaeche/rahmen-buehne.css?v=1">\n<link rel="stylesheet" href="/assets/oberflaeche/kleid/ruedihus.css?v=1">\n'
               '<link rel="stylesheet" href="gastgeber.css?v=3">\n')
    h = tausch(h, '<body class="bu re">', '<body class="bu re wo-app">')
    h = tausch(h, '<header class="kopf" id="kopf"></header>', '<header class="wo-kopf" id="kopf"></header>')
    h = tausch(h, '<aside class="rand" id="rand"', '<aside class="wo-rand" id="rand"')
    h = tausch(h, '<main class="haupt" id="haupt">', '<main class="gg-raum" id="haupt">')
    h = tausch(h, '<footer class="leiste" id="leiste"', '<footer class="wo-leiste" id="leiste"')
    h = tausch(h, '<script src="reception.js?v=10"></script>', '<script src="/assets/oberflaeche/oberflaeche.js?v=1"></script>\n<script src="reception.js?v=11"></script>')
    h = tausch(h, 'data-blaetter="#ansicht h2.zw, #ansicht .lage, #ansicht .re-zahlen, #ansicht .re-leer" data-kacheln="#ansicht .re-gr"',
               'data-blaetter="#ansicht h2.wo-zw, #ansicht .wo-lage, #ansicht .re-zahlen, #ansicht .re-leer" data-kacheln="#ansicht .re-gr, #ansicht .wo-ag"')
    h = tausch(h, '<script src="studio/buehne.js?v=4" defer></script>\n', '')
    h = tausch(h, '<script src="studio/rundgang.js?v=3" defer', '<script src="studio/rundgang.js?v=5" defer')
    schreib('index.html', h)
    print('oberflaeche.py: index.html umgestellt.')

# ---------- Rundgang: Wähler auf die neuen Klassen ----------
rg = lies('studio/rundgang.js')
if "ziel: ['#ansicht .wo-sb'], titel: 'Das ist der Gastgeber'" in rg:
    print('oberflaeche.py: Rundgang ist schon umgestellt.')
else:
    rg = tausch(rg, "ziel: ['#ansicht .titel'], titel: 'Das ist der Gastgeber'", "ziel: ['#ansicht .wo-sb'], titel: 'Das ist der Gastgeber'")
    rg = tausch(rg, "ziel: ['#rand .nav', '#rand'], titel: 'Was Gäste wissen wollen'", "ziel: ['#rand .wo-rand__g', '#rand'], titel: 'Was Gäste wissen wollen'")
    rg = tausch(rg, "ziel: ['#kopf .kopf__werk .kn', '#kopf .kopf__werk'], oben: true, titel: 'Probieren Sie es selbst'", "ziel: ['#k-probe', '#kopf .wo-kopf__r', '#rand [data-probe]'], oben: true, titel: 'Probieren Sie es selbst'")
    rg = tausch(rg, "ziel: ['#ansicht .titel'], titel: 'Das Gedächtnis des Chats'", "ziel: ['#ansicht .wo-sb'], titel: 'Das Gedächtnis des Chats'")
    schreib('studio/rundgang.js', rg)
    print('oberflaeche.py: Rundgang umgestellt.')

# ---------- gastgeber.css: Anschluss der Arbeitsflächen an das Paket ----------
schreib('gastgeber.css', r"""/* Der Gastgeber · Landgasthof Ruedihus: Anschluss der Arbeitsflächen (Eingang, Brief, Wissen) an das Paket der Werkzeuge des Hauses
   (assets/oberflaeche, Rahmen «Die Bühne», kleid/ruedihus.css); gebaut von _bau/oberflaeche.py, Vorbild Der Gastgeber Gasterntal. Lädt als letztes Stylesheet. */
.wo-rand__wege button{display:flex;align-items:center;gap:8px;width:100%;padding:7px 14px;border:0;background:none;font:inherit;font-size:13.5px;color:var(--wo-leise);text-align:left;cursor:pointer}
.wo-rand__wege button:hover,.wo-rand__wege a:hover{color:var(--wo-tinte)}
@media (min-width:901px){.wo-rand__probe{display:none!important}}
/* Knöpfe des Pakets: studio.css setzt «.bu button{font:inherit}» und überstimmt sonst die Schrift von .wo-kn */
.wo-app button.wo-kn{font:400 11px/1 var(--wo-mono);letter-spacing:.16em;text-transform:uppercase}
.wo-app button.wo-kn--klein{font-size:10.5px}
/* Raum: Lage wie .wo-raum des Rahmens «Die Bühne», aber ohne Klasse «wo-» (sonst setzt grund.css die Knöpfe der Arbeitsflächen zurück) */
.wo-app>.gg-raum{grid-area:raum;min-width:0;margin-left:28px}
@media (max-width:900px){.wo-app>.gg-raum{margin:0 16px}}
/* Kacheln als Knopf: «.bu button{color:inherit}» aus studio.css überstimmt sonst die helle Schrift auf der dunklen Kachel */
.wo-app button.wo-ag{color:var(--wo-weiss);text-align:left;padding:0;border:0;font:inherit}
.wo-app button.wo-kopf__ber{font:400 10.5px/1 var(--wo-mono);letter-spacing:.16em;text-transform:uppercase}
.wo-app button.wo-kn--hell{color:var(--wo-tinte)}
.wo-app button.wo-kn--gold{color:var(--wo-tief)}
.wo-app button.wo-kn--dunkel,.wo-app button.wo-kn--glas{color:var(--wo-weiss)}
.wo-app button.wo-kn--rund{color:var(--wo-gold)}
""")
print('oberflaeche.py: gastgeber.css geschrieben.')
