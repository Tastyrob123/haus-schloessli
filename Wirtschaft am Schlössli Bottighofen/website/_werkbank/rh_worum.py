#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus, Blatt «Worum es geht» zwischen Brief und Register (Werkbank-Chat 17.10.2026; Aufbau, Rechner und Stil aus vertrieb.py
der Werkbank des Carlton-Europe über dh_worum.py des Waldhotel Doldenhorn, nur gelesen und kopiert; Worte und Annahmen des Ruedihus). Ein ruhiger Satz zum
Zweck, darunter der Rechner als ein Blatt: links was bleibt, rechts sechs Annahmen, jede beschriftet und ersetzbar. Robert 17.10.2026: der Rechner steht
nur hier, im Angebot nicht noch einmal. Keine Zahl ohne Quelle: Zimmerzahl laut Schpiszettel ab 1.3.2026 (7 Doppelzimmer, 1 Einzelzimmer, Hochzeitsstube,
Liebeslaube, 2 Himmelreich = 12; Fakten-Blatt Punkt 1, die Website des Hauses nennt andere Zahlen), Preis Landhaus ab CHF 250 von der Zimmer-Seite."""
import html

e = html.escape
ANNAHMEN = [  # Schlüssel, Zeile, Wert, Einheit, Beschriftung
    ('zimmer', 'Zimmer im Haus', 12, '', 'Annahme · so zählt es Ihr Schpiszettel'),
    ('belegung', 'Belegung übers Jahr', 60, '%', 'Annahme'),
    ('preis', 'Zimmerpreis je Nacht', 250, 'CHF', 'Annahme · Landhaus ab CHF 250 auf Ihrer Seite'),
    ('anteil', 'Buchungen über Portale', 50, '%', 'Annahme'),
    ('kommission', 'Kommission der Portale', 15, '%', 'Annahme · den genauen Satz kennt Ihr Vertrag'),
    ('wechsel', 'Buchungen, die zu Ihnen wechseln', 5, 'Punkte', 'Annahme · 5 von 100 Portalbuchungen'),
]
STUFEN = (1, 3, 5, 10)


def _chf(x):
    return f"{round(x):,}".replace(',', '’')


def blatt(k):
    v = {key: wert for key, _z, wert, _e, _q in ANNAHMEN}
    umsatz = v['zimmer'] * 365 * v['belegung'] / 100 * v['preis']
    portal = umsatz * v['anteil'] / 100 * v['kommission'] / 100
    punkt = umsatz / 100 * v['kommission'] / 100
    bleibt = punkt * v['wechsel']
    stufen = ''.join(f'<div class="vt-gegen__z{" vt-gegen__z--s" if n == v["wechsel"] else ""}"><span>{n} von 100 Buchungen</span><b><i data-vt-stufe="{n}">{_chf(punkt * n)}</i> CHF</b></div>' for n in STUFEN)
    felder = ''.join(f'<div class="vt-feld"><div class="vt-feld__l"><span>{e(z)}</span><small>{e(q)}</small></div><label class="vt-feld__w"><input type="text" inputmode="decimal" value="{wert}" data-k="{key}" aria-label="{e(z)}">'
                     + (f'<em>{e(ein)}</em>' if ein else '') + '</label></div>' for key, z, wert, ein, q in ANNAHMEN)
    gruende = [('Vom Zimmer direkt zur Buchung', 'Landhaus, Hochzeitsstube, Liebeslaube und Hymmelrich haben je ihre eigene Seite mit allen Fotos; der Knopf daneben öffnet Ihr SimpleBooking mit Tag und Personen.'),
               ('Mit wem und wann, dann das Zimmer', 'Das Buchen-Fenster fragt zuerst, wer kommt und wann, und schlägt dann das passende Zimmer samt Preis vor.'),
               ('Fragen geklärt, bevor jemand weiterklickt', 'Ob der Hund mit darf oder ob am Montag eine Stube offen ist, beantwortet die Rezeption im Chat auch am späten Abend, und die Buchung liegt gleich daneben.')]
    gr = ''.join(f'<li><b>{e(t)}</b><span>{e(x)}</span></li>' for t, x in gruende)
    return f'''
<section class="fl fl--navy tapete blatt vt" id="worum">
  <div class="in">
    {k['kopf'](0, 'Worum es geht', ['Gäste, die den Weg', 'selbst finden.'], 'Eine schöne Seite allein füllt keine Stube. Sie soll es Gästen, die das Ruedihus heute über ein Portal finden, leichter machen, direkt bei Ihnen zu buchen. Dieses Blatt ist ein Rechenbeispiel auf Grundlage der Annahmen rechts, und jede Annahme können Sie durch Ihre eigene Zahl ersetzen.')}
    <div class="ag-blatt vt-r" data-a="hoch">
      <div class="vt-r__t">
        <p class="ag-r__n">Die Rechnung</p>
        <h3>Ein Rechenbeispiel.</h3>
        <p class="vt-r__lead">Rechenbeispiel auf Grundlage dieser Annahmen: Im Jahr gehen <b data-vt="portal">{_chf(portal)}</b> Franken als Kommission an die Portale. Würden <b data-vt="wechsel">{v['wechsel']}</b> von hundert dieser Gäste über Ihre eigene Seite buchen, blieben davon <b data-vt="bleibt">{_chf(bleibt)}</b> Franken im Haus.</p>
        <div class="vt-gegen">
          <p class="ag-r__n">Ein Jahr lang gerechnet</p>
          {stufen}
          <p class="vt-gegen__satz">Wer über die eigene Seite bucht, kostet keine Kommission. Wie viele Gäste das tun, hängt nicht an der Seite allein: Buchungsweg, Preise, Suchmaschinen, Sichtbarkeit und wie oft der Direktweg genutzt wird, spielen mit. Eine Zusage, dass bestimmte Punkte zurückkommen, ist das Rechenbeispiel nicht.</p>
        </div>
        <p class="ag-r__n vt-gr__k">Drei Wege zum Ruedihus</p>
        <ul class="vt-gr">{gr}</ul>
      </div>
      <div class="vt-r__r">
        <p class="vt-r__k">Sechs Zahlen, jede lässt sich überschreiben</p>
        {felder}
        <div class="vt-ergebnis">
          <p class="vt-r__u">Daraus gerechnet, Zimmerumsatz im Jahr: <b data-vt="umsatz">{_chf(umsatz)}</b> CHF</p>
          <div class="vt-erg"><b data-vt="portal">{_chf(portal)}</b><span>CHF</span><small>Kommission im Jahr an die Portale</small></div>
          <div class="vt-erg"><b data-vt="punkt">{_chf(punkt)}</b><span>CHF</span><small>je Prozentpunkt, der direkt bucht</small></div>
          <div class="vt-erg vt-erg--gross"><b data-vt="bleibt">{_chf(bleibt)}</b><span>CHF</span><small>Rechenbeispiel, wenn <span data-vt="wechsel">{v['wechsel']}</span> Punkte direkt buchen</small></div>
        </div>
      </div>
    </div>
  </div>
</section>
{JS}'''


JS = '''<script id="vt-rechner">
window.RHV=(function(){var S={zimmer:12,belegung:60,preis:250,anteil:50,kommission:15,wechsel:5},H=[];
function umsatz(s){return s.zimmer*365*(s.belegung/100)*s.preis}
function proPunkt(u,k){return u/100*(k/100)}
return{S:S,umsatz:umsatz,portal:function(s){return umsatz(s)*(s.anteil/100)*(s.kommission/100)},proPunkt:proPunkt,ersparnis:function(u,k,p){return proPunkt(u,k)*p},
 hoerer:function(f){H.push(f)},melde:function(){for(var i=0;i<H.length;i++)H[i](S)}}})();
(function(){var S=document.getElementById('worum');if(!S)return;var C=window.RHV;
var nf=new Intl.NumberFormat(document.documentElement.lang||'de-CH',{maximumFractionDigits:0});
function w(el){var t=String(el.value).replace(/[\\u2019'\\u202f\\u00a0 ]/g,'').replace(/,/g,'.');if((t.match(/\\./g)||[]).length>1)t=t.replace(/\\./g,'');var v=parseFloat(t);return isFinite(v)?v:null}
function setze(k,t){[].forEach.call(S.querySelectorAll('[data-vt="'+k+'"]'),function(x){x.textContent=t})}
function zeig(){var ok=true,k;for(k in C.S)if(C.S[k]===null)ok=false;var D='\\u2013';
 var u=ok?C.umsatz(C.S):0,p=ok?C.proPunkt(u,C.S.kommission):0;
 setze('umsatz',ok?nf.format(Math.round(u)):D);setze('portal',ok?nf.format(Math.round(C.portal(C.S))):D);setze('punkt',ok?nf.format(Math.round(p)):D);
 setze('bleibt',ok?nf.format(Math.round(p*C.S.wechsel)):D);setze('wechsel',ok?nf.format(C.S.wechsel):D);[].forEach.call(S.querySelectorAll('[data-vt-stufe]'),function(x){x.textContent=ok?nf.format(Math.round(p*(+x.getAttribute('data-vt-stufe')))):D;x.closest('.vt-gegen__z').classList.toggle('vt-gegen__z--s',+x.getAttribute('data-vt-stufe')===C.S.wechsel)});C.melde()}
var F=S.querySelectorAll('.vt-feld input'),i;
for(i=0;i<F.length;i++)(function(f){var v=w(f);if(v!==null)f.value=nf.format(v);
 f.addEventListener('input',function(){C.S[f.getAttribute('data-k')]=w(f);zeig()});f.addEventListener('blur',function(){var v=w(f);if(v!==null)f.value=nf.format(v)})})(F[i]);
zeig();
/* Robert 18.10.2026: «dass die Zahlen … zählen, wenn ich da reinscrolle»: einmal beim ersten Erscheinen, wer tippt, hält es an */
(function(){if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
 var Z=[].slice.call(S.querySelectorAll('.vt-r__lead b[data-vt],.vt-r__u b[data-vt],.vt-erg b[data-vt],[data-vt-stufe]')),halt=false;
 [].forEach.call(F,function(f){f.addEventListener('input',function(){halt=true})});
 new IntersectionObserver(function(es,o){if(!es[0].isIntersecting)return;o.disconnect();
  var ziel=Z.map(function(x){return x.textContent}),ws=ziel.map(function(t){return parseFloat(String(t).replace(/[^0-9.]/g,''))}),t0=performance.now(),d=1400;
  function schritt(t){if(halt)return;var k=Math.min(1,(t-t0)/d),e=1-Math.pow(1-k,3);
   Z.forEach(function(x,i){if(isFinite(ws[i]))x.textContent=k<1?nf.format(Math.round(ws[i]*e)):ziel[i]});if(k<1)requestAnimationFrame(schritt)}
  requestAnimationFrame(schritt)},{threshold:.3}).observe(S.querySelector('.vt-r'))})();
})();
/* Weg bis zur Buchung: Zahlenreihe, nur das Bild wechselt, nichts springt */
(function(){var G=document.querySelector('.vt-weg');if(!G)return;var B=[].slice.call(G.querySelectorAll('.vt-schritte button')),I=[].slice.call(G.querySelectorAll('.vt-w')),T=[].slice.call(G.querySelectorAll('.vt-weg__t>div'));
function zeig(n){B.forEach(function(b,i){b.setAttribute('aria-pressed',i===n?'true':'false')});I.forEach(function(x,i){x.classList.toggle('an',i===n)});T.forEach(function(x,i){x.classList.toggle('an',i===n)})}
B.forEach(function(b,i){b.addEventListener('click',function(){zeig(i)})});
G.addEventListener('keydown',function(ev){var n=B.findIndex(function(b){return b.getAttribute('aria-pressed')==='true'});if(ev.key==='ArrowRight')zeig(Math.min(B.length-1,n+1));else if(ev.key==='ArrowLeft')zeig(Math.max(0,n-1))})})();
</script>'''


CSS = '''
/* ---------- «Worum es geht» (vertrieb.py, 16.10.2026): Blatt zwischen Brief und Register, Rechner mit richtigen Feldern ---------- */
.vt .kopfzeile{margin-bottom:clamp(30px,3.4vw,54px)}
.vt-r{display:grid;gap:clamp(26px,3.4vw,64px);align-items:start}
@media(min-width:960px){.vt-r{grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr)}}
/* Robert 18.10.2026: beide Spalten schliessen bündig ab, kein Leerraum unter der rechten Karte */
@media(min-width:960px){.vt-r{align-items:stretch}.vt-r__r{display:flex;flex-direction:column}.vt-ergebnis{flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-around}}
.vt-r__t h3{margin:0;font-family:var(--serif);font-weight:400;font-size:clamp(1.9rem,2.7vw,2.9rem);line-height:1.08;color:var(--tinte)}
.vt-r__t>p{margin:16px 0 0;max-width:46ch;font-family:var(--serif);font-size:clamp(1.06rem,1.16vw,1.22rem);line-height:1.6;color:rgba(12,21,38,.82)}
.vt-r__lead{margin:16px 0 0;max-width:40ch;font-family:var(--serif);font-size:clamp(1.24rem,1.5vw,1.6rem)!important;line-height:1.48!important;color:var(--tinte)!important}
.vt-r__lead b{font-weight:400;color:#8a6f35;font-variant-numeric:tabular-nums}
.vt-gegen{margin-top:clamp(24px,2.8vw,40px);padding:clamp(20px,2.2vw,30px);border-radius:18px;background:linear-gradient(180deg,#0f2a55,#0b1f40);color:#fbf6ea;box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 0 0 1px rgba(220,198,143,.5),0 30px 40px -30px rgba(6,20,43,.8)}
.vt-gegen .ag-r__n{color:var(--gold)}
.vt-gegen__z{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:9px 0;border-bottom:1px solid rgba(220,198,143,.2);font-family:var(--serif);font-size:clamp(1.04rem,1.14vw,1.2rem)}
.vt-gegen__z b{font-weight:400;font-variant-numeric:tabular-nums}
.vt-gegen__z--s{color:var(--gold)}
.vt-gegen__z i{font-style:normal}
.vt-gegen__z:last-of-type{border-bottom:0}
.vt-gegen__satz{margin:12px 0 0;padding-top:14px;border-top:1px solid rgba(220,198,143,.5);font-family:var(--serif);font-size:clamp(1rem,1.08vw,1.12rem);line-height:1.5;color:rgba(251,246,234,.86)}
.vt-gr__k{margin-top:clamp(24px,2.8vw,38px)!important}
.vt-gr{margin:0;padding:0;list-style:none}
.vt-gr li{position:relative;padding:12px 0 12px 30px;border-bottom:1px solid rgba(150,125,64,.22)}
.vt-gr li:last-child{border-bottom:0}
.vt-gr li::before{content:"";position:absolute;left:4px;top:1.15em;width:12px;height:6px;border-left:2px solid #8a6f35;border-bottom:2px solid #8a6f35;transform:rotate(-45deg)}
.vt-gr b{display:block;font-family:var(--serif);font-weight:400;font-size:clamp(1.1rem,1.2vw,1.26rem);color:var(--tinte)}
.vt-gr span{display:block;margin-top:3px;font-family:var(--serif);font-size:clamp(.98rem,1.04vw,1.08rem);line-height:1.5;color:rgba(12,21,38,.76)}
.vt-erg--gross b{font-size:clamp(2.8rem,3.8vw,4rem)}
.vt-erg--gross{padding-top:14px}
.vt-r__k{margin:0 0 14px;font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:#967d40}
.vt-feld{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px 18px;align-items:center;padding:12px 0;border-bottom:1px solid rgba(150,125,64,.22)}
.vt-feld:last-of-type{border-bottom:0}
.vt-feld__l span{display:block;font-family:var(--serif);font-size:clamp(1.14rem,1.24vw,1.32rem);line-height:1.3;color:var(--tinte)}
.vt-feld__l small{display:block;margin-top:4px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#967d40}
.vt-feld__w{display:flex;align-items:baseline;gap:8px;min-width:8.6em;padding:9px 16px 9px 14px;border-radius:12px;background:rgba(255,255,255,.72);box-shadow:inset 0 1px 2px rgba(60,40,10,.08),inset 0 0 0 1px rgba(150,125,64,.42);cursor:text;transition:box-shadow .3s}
.vt-feld__w:focus-within{box-shadow:inset 0 1px 2px rgba(60,40,10,.08),inset 0 0 0 1.5px #967d40}
.vt-feld__w input{flex:1 1 auto;width:6.5em;min-width:0;appearance:none;-webkit-appearance:none;background:transparent;border:0;padding:0;text-align:right;font-family:var(--serif);font-size:clamp(1.6rem,1.9vw,2rem);line-height:1.1;color:var(--tinte)}
.vt-feld__w input:focus{outline:0;color:#6d5a2c}
.vt-feld__w em{flex:none;font-family:var(--serif);font-style:italic;font-size:clamp(1rem,1.06vw,1.1rem);color:rgba(12,21,38,.62)}
.vt-ergebnis{margin-top:clamp(18px,2vw,26px);padding:clamp(18px,2vw,26px) clamp(20px,2.2vw,28px);border-radius:18px;background:linear-gradient(180deg,#fbf3e2,#f0e3c4);box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(150,125,64,.5)}
.vt-r__u{margin:0 0 12px;padding-bottom:12px;border-bottom:1px solid rgba(150,125,64,.3);font-family:var(--serif);font-style:italic;font-size:clamp(1rem,1.06vw,1.1rem);color:rgba(12,21,38,.7)}
.vt-r__u b{font-weight:400;font-style:normal;color:var(--tinte)}
.vt-erg{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;padding:8px 0}
.vt-erg+.vt-erg{border-top:1px solid rgba(150,125,64,.22)}
.vt-erg b{font-family:var(--serif);font-weight:400;font-size:clamp(2.4rem,3.2vw,3.4rem);line-height:1;color:#967d40;font-variant-numeric:tabular-nums}
.vt-erg span{font-family:var(--serif);font-style:italic;font-size:clamp(1.1rem,1.2vw,1.3rem);color:#967d40}
.vt-erg small{flex-basis:100%;font-family:var(--serif);font-size:clamp(1.02rem,1.08vw,1.14rem);color:rgba(12,21,38,.78)}
@media(max-width:600px){.vt-feld{grid-template-columns:1fr}.vt-feld__w{min-width:0}}
/* ---------- Kapitel 1, die vier Funde auf der Bühne der Befunde (vertrieb.py): Bedeutung unter dem Klartext, Fenster am Rechner ---------- */
.bfk-bed{flex-basis:100%;order:2;display:grid;gap:8px 18px;margin-top:4px}
@media(min-width:700px){.bfk-bed{grid-template-columns:1fr 1fr}}
.bfk-bed span{display:block;padding:10px 14px;border-radius:12px;color:var(--tinte);background:linear-gradient(180deg,#fbf3e2,#ecdfc0);box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(220,198,143,.7);font-family:var(--serif);font-size:clamp(.94rem,1vw,1.04rem);line-height:1.42}
.bfk-bed b{display:block;margin-bottom:2px;font-family:var(--mono);font-weight:500;font-size:.64rem;letter-spacing:.18em;text-transform:uppercase;color:#8a6f35}
.bfk .bfx--fenster .bfx-fen{width:min(100%,400px)}
.bfk .bfx-fen__s{position:relative}
.bfk .bfx--fenster .bfx-kreis{inset:0}
.bfx--handy .bfx-tel__s img{border-radius:32px}
.bfk-b__t small{white-space:normal}
.bfk-wahl{flex-wrap:wrap}
@media(max-width:600px){.bfk .bfx--handy{max-width:142px}.bfk .bfx--handy .bfx-tel{height:min(60vh,300px)}.bfk .bfx--handy figcaption{max-width:100%;margin-top:10px}.bfk .bfx--handy figcaption span{font-size:.8rem}}
@media (prefers-reduced-motion:reduce){.vt .ag-blatt[data-a]{opacity:1;transform:none}}
'''
