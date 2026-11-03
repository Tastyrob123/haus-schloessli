#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli, Blatt «Worum es geht» zwischen Brief und Register (Station 11, 19.10.2026; Aufbau und Kleid wie rh_worum.py
des Ruedihus, Rechnung eigen fürs Restaurant). Im Vordergrund steht die Rechnung für das Haus (Tasty-Sprache C, Werkbank): Feste und Mittagstische,
die über die neue Seite angefragt werden. Robert 17.10.2026: der Rechner steht nur hier. Keine Zahl ohne Quelle: Plätze je Etage aus «Banketts & Gruppen»
(haus.json › bankett.platz), Menüpreis aus den Bankettmenüvorschlägen vom 29.04.2025 (bankett.json, Herbst CHF 175), Lunch CHF 35 aus dem Lunch-Menü
(lunch.json). Alles andere ist als Annahme beschriftet und lässt sich überschreiben. Kein Agenturpreis, keine Zusage."""
import html, json, os

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
BK = json.load(open(os.path.join(ROOT, 'inhalt', 'bankett.json'), encoding='utf-8'))
LU = json.load(open(os.path.join(ROOT, 'inhalt', 'lunch.json'), encoding='utf-8'))
_menue = min(m['preis'] for m in BK['menues'])
ANNAHMEN = [  # Schlüssel, Zeile, Wert, Einheit, Beschriftung
    ('feste', 'Feste mehr im Jahr, über die Seite angefragt', 6, '', 'Annahme'),
    ('personen', 'Gäste je Fest', 26, '', 'Annahme · bis zu 26 je Etage laut Ihrer Seite'),
    ('menue', 'Menüpreis je Gast', _menue, 'CHF', f'laut Bankettmenüvorschlägen 2025 (ab CHF {_menue})'),
    ('lunch', 'Mittagsgäste mehr je Woche', 10, '', 'Annahme'),
    ('lunchpreis', 'Lunch-Menü', LU['preis_zahl'], 'CHF', 'laut Ihrem Lunch-Menü, drei Gänge'),
    ('wochen', 'Wochen mit Lunch im Jahr', 44, '', 'Annahme · ohne Betriebsferien'),
]


def _chf(x):
    return f"{round(x):,}".replace(',', '’')


def blatt(k):
    v = {key: wert for key, _z, wert, _e, _q in ANNAHMEN}
    fest = v['feste'] * v['personen'] * v['menue']
    lunch = v['lunch'] * v['lunchpreis'] * v['wochen']
    felder = ''.join(f'<div class="vt-feld"><div class="vt-feld__l"><span>{e(z)}</span><small>{e(q)}</small></div><label class="vt-feld__w"><input type="text" inputmode="decimal" value="{wert}" data-k="{key}" aria-label="{e(z)}">'
                     + (f'<em>{e(ein)}</em>' if ein else '') + '</label></div>' for key, z, wert, ein, q in ANNAHMEN)
    gruende = [('Das Fest beginnt auf der Seite', 'Die Bankettmenüs stehen Gang für Gang auf der Seite, die zwei Etagen mit ihren Plätzen gleich dabei; die Anfrage geht im Fenster an Ihr Team, mit Datum, Allergien und Wünschen.'),
               ('Der Mittag steht vorne', 'Das Lunch-Menü der Woche steht mit Gängen und Preis auf der Seite, nicht nur als PDF, und Ihr Team ändert es jede Woche selbst im Werkzeug für die Karten.'),
               ('Der Abend ist geplant, bevor jemand anruft', 'Auf dem Zettel «Ihr Abend» wählt der Gast Anlass, Personen, Platz und Menü; er rechnet mit den Preisen Ihrer Karte.')]
    fotos = ['vt-g-1', 'vt-g-2', 'vt-g-3']
    gr = ''.join(f'<li>' + (f'<span class="vt-gb">{k["bild"](f, t)}</span>' if f in k['m'] else '') + f'<b>{e(t)}</b><span>{e(x)}</span></li>' for (t, x), f in zip(gruende, fotos))
    return f'''
<section class="fl fl--navy tapete blatt vt" id="worum">
  <div class="in">
    {k['kopf'](0, 'Worum es geht', ['Mehr Feste,', 'mehr Mittage.'], 'Eine schöne Seite allein füllt keinen Tisch. Sie soll es leichter machen, bei Ihnen ein Fest anzufragen oder mittags vorbeizukommen. Dieses Blatt ist ein Rechenbeispiel auf Grundlage der Annahmen rechts, und jede Annahme können Sie durch Ihre eigene Zahl ersetzen.')}
    <div class="ag-blatt vt-r" data-a="hoch">
      <div class="vt-r__t">
        <p class="ag-r__n">Die Rechnung</p>
        <h3>Ein Rechenbeispiel.</h3>
        <p class="vt-r__lead">Rechenbeispiel auf Grundlage dieser Annahmen: <b data-vt="feste">{v['feste']}</b> Feste mehr im Jahr ergeben <b data-vt="fest">{_chf(fest)}</b> Franken für die Menüs, ohne Getränke. Kommen jede Woche <b data-vt="lunch">{v['lunch']}</b> Gäste mehr zum Lunch, sind es <b data-vt="lunchsumme">{_chf(lunch)}</b> Franken im Jahr.</p>
        <p class="ag-r__n vt-gr__k">Drei Wege ins Schlössli</p>
        <ul class="vt-gr">{gr}</ul>
        <p class="vt-gegen__satz">Wie viele Gäste so kommen, hängt nicht an der Seite allein: Lage, Wetter, Preise, Empfehlungen und Suchmaschinen spielen mit. Eine Zusage ist das Rechenbeispiel nicht.</p>
      </div>
      <div class="vt-r__r">
        <p class="vt-r__k">Sechs Zahlen, jede lässt sich überschreiben</p>
        {felder}
        <div class="vt-ergebnis">
          <div class="vt-erg"><b data-vt="fest">{_chf(fest)}</b><span>CHF</span><small>Menüs der Feste im Jahr</small></div>
          <div class="vt-erg"><b data-vt="lunchsumme">{_chf(lunch)}</b><span>CHF</span><small>Lunch im Jahr</small></div>
          <div class="vt-erg vt-erg--gross"><b data-vt="summe">{_chf(fest + lunch)}</b><span>CHF</span><small>Rechenbeispiel zusammen, ohne Getränke</small></div>
        </div>
      </div>
    </div>
  </div>
</section>
{JS}'''



def bilder(webp, haus):
    for n, key, lage in (('vt-g-1', 'lounge', (.5, .5)), ('vt-g-2', 'suppe', (.5, .5)), ('vt-g-3', 'abend', (.5, .6))):
        webp(haus(key), n, 520, 80, 3 / 2, lage)


JS = '''<script id="vt-rechner">
(function(){var S=document.getElementById('worum');if(!S)return;
var nf=new Intl.NumberFormat('de-CH',{maximumFractionDigits:0});
function w(el){var t=String(el.value).replace(/[\\u2019'\\u202f\\u00a0 ]/g,'').replace(/,/g,'.');var v=parseFloat(t);return isFinite(v)&&v>=0?v:null}
function setze(k,t){[].forEach.call(S.querySelectorAll('[data-vt="'+k+'"]'),function(x){x.textContent=t})}
function rechne(){var v={};[].forEach.call(S.querySelectorAll('input[data-k]'),function(i){var x=w(i);i.classList.toggle('falsch',x===null);v[i.getAttribute('data-k')]=x===null?0:x});
var fest=v.feste*v.personen*v.menue,lunch=v.lunch*v.lunchpreis*v.wochen;
setze('feste',nf.format(v.feste));setze('lunch',nf.format(v.lunch));setze('fest',nf.format(fest));setze('lunchsumme',nf.format(lunch));setze('summe',nf.format(fest+lunch))}
[].forEach.call(S.querySelectorAll('input[data-k]'),function(i){i.addEventListener('input',rechne)});rechne()})();
</script>'''


CSS = '''
/* Blatt des Rechenbeispiels (Bauart des Blatts aus rh_angebot.py des Ruedihus) */
.ag-blatt{position:relative;padding:clamp(28px,3.8vw,64px);border-radius:clamp(22px,2.4vw,34px);background:linear-gradient(rgba(251,252,254,.94),rgba(251,252,254,.94)),var(--weiss) url(../assets/svg/tapete-a-hell.svg) 50% 0/168px auto;color:var(--tinte);box-shadow:inset 0 1px 0 #fff,0 50px 70px -46px rgba(0,0,0,.95)}
.ag-blatt::before,.ag-blatt::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(15,54,120,.4);border-radius:clamp(14px,1.6vw,24px);inset:clamp(10px,1.1vw,16px)}
.ag-blatt::after{inset:clamp(15px,1.5vw,22px);border-color:rgba(15,54,120,.18);border-radius:clamp(11px,1.3vw,19px)}
.ag-r__n{margin:0 0 12px;font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--taupe)}
.vt-r{color:var(--tinte)}
.vt-gr li{display:grid;grid-template-columns:clamp(92px,9vw,128px) 1fr;column-gap:16px;align-items:start}
.vt-gr li>.vt-gb{grid-row:1/span 2;display:block;border-radius:12px;overflow:hidden;aspect-ratio:3/2}.vt-gr li>.vt-gb img{display:block;width:100%;height:100%;object-fit:cover}
.vt-gr li>b,.vt-gr li>span:not(.vt-gb){grid-column:2}
'''
