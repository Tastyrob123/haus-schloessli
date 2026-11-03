#!/usr/bin/env python3
"""Werkbank Landgasthof Ruedihus, Abschnitt «Rezeption im Chat» (12.10.2026, Master 5b Punkt 14): das 3D-Handy schwebt herein,
der Film läuft einmal, rechts vier Punkte, darunter drei freie Stücke (Handy, Karte mit Code, eigene Seite).

Das Handy ist dasselbe wie auf der Seite rezeption/ des Ruedihus: Modell assets/3d/rezeption-phone.glb, Zeichen assets/3d/rezeption-zeichen.png,
Bildschirm-Film assets/video/rezeption-schirm.mp4 (ein Gast fragt nach Fondue am Abend, die Buchungsmaske erscheint). Die Website wird nicht angefasst:
das Start-Skript der Werkbank liegt als eigene Kopie in werkbank/eigen/rezeption3d.js (Stand Grand Beau-Rivage 12.10.2026: nimmt Film und Modell aus dem
Vorrat, meldet Fehler, damit der flache Rahmen einspringt).
Ablauf (Robert 12.10.2026: «einmal flüssig hochkommen und wirklich ganz sicher immer starten»): Film, Modell und Skript werden geholt, sobald die Seite
geladen ist; ausgepackt wird in einer Scrollpause; das Bild des Modells zeigt sich erst, wenn das Handy startet; der Text kommt einmal und bleibt;
kommt das Modell nicht (kein WebGL, Leitung, über 12 s), steht der flache Rahmen mit demselben Film. Am Handy steht immer der flache Rahmen.
Eingehängt am Ende von haus.py über H.EIGENE (key 'rezeption' ersetzt den Kit-Abschnitt mit dem Film im Fensterrahmen)."""
import os

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
FILM_V = 'rh3'   # Robert 18.10.2026 23:31: keine Frage «Wie alt ist das Haus?», die stellt kein Gast einer Rezeption; die Werkbank zeigt jetzt dasselbe Fondue-Gespräch wie die Seite rezeption/ (ohne neue KI-Abfrage)
SKRIPT_V = 'rh1'
DAUER = '15.6'      # Länge von assets/video/rezeption-schirm.mp4 (Fondue-Gespräch)
BEREIT = all(os.path.exists(os.path.join(ROOT, p)) for p in ('assets/3d/rezeption-phone.glb', 'assets/video/rezeption-schirm.mp4', 'assets/video/rezeption-schirm-m.mp4')) \
    and os.path.exists(os.path.join(W, 'eigen', 'rezeption3d.js'))
BILDER = []

# Zeichen zu den vier Punkten, in der Reihenfolge von haus.REZEPTION: Uhr, Kalender mit Haken, Sonne über dem Berg, Brief
ZEICHEN = [
    '<circle cx="12" cy="12" r="8.2"/><path d="M12 7.4V12l3 2"/>',
    '<rect x="4" y="5.4" width="16" height="14.2" rx="2.2"/><path d="M4 9.8h16M8.4 3.6v3.4M15.6 3.6v3.4M8.8 14.6l2.3 2.2 4.2-4.3"/>',
    '<circle cx="16.6" cy="7.6" r="2.6"/><path d="M3 19.4 9.2 9.8l3.6 5.4 2.4-3.2 5.8 7.4z"/>',
    '<path d="M4.4 7.2h15.2v10.6H4.4z"/><path d="m4.6 7.6 7.4 5.6 7.4-5.6"/>',
]

CSS = '''
/* ---------- Rezeption im Chat: helle Fläche, links das Handy in 3D (wie auf rezeption/), rechts vier Punkte, darunter drei freie Stücke (rezeption_handy.py, 12.10.2026) ---------- */
#rezeption.rzh{background-color:var(--weiss)}
.rzh-b{position:relative;max-width:1560px;margin:0 auto;height:clamp(620px,90svh,880px)}
.rzh-b .tel-pin{position:absolute;inset:0;z-index:0}
.rzh-sch{position:absolute;z-index:-1;left:29.5%;top:91%;width:min(340px,27%);height:44px;transform:translate(-50%,-50%);border-radius:50%;pointer-events:none;
  background:radial-gradient(closest-side,rgba(42,26,14,.36),rgba(42,26,14,.13) 56%,rgba(42,26,14,0));opacity:0;transition:opacity 1.6s .15s}
.rzh-b.laeuft .rzh-sch{opacity:1;transition:opacity 1.6s 1.5s}
#rezeption .kopfzeile{margin-bottom:clamp(6px,1.6vw,26px)}
.rzh-b canvas{position:absolute;inset:0;width:100%;height:100%;display:block;opacity:0}
.rzh-b.laeuft canvas{opacity:1}
#rezeption #telefon3d-text{position:absolute;z-index:3;top:50%;left:53%;right:max(var(--rand),calc((100% - var(--max))/2));transform:translateY(-50%);max-width:620px}
.rzh-p{list-style:none;margin:0;padding:0}
.rzh-p li{display:grid;grid-template-columns:54px minmax(0,1fr);gap:clamp(14px,1.5vw,22px);align-items:start;padding:clamp(14px,1.5vw,22px) 0;border-top:1px solid rgba(125,79,39,.3)}
.rzh-p li:last-child{border-bottom:1px solid rgba(125,79,39,.3)}
.rzh-z{width:54px;height:54px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,#5a3a20 0%,#321f10 52%,#170d06 100%);
  box-shadow:inset 0 1px 0 rgba(255,236,200,.3),inset 0 -3px 0 rgba(0,0,0,.5),0 14px 20px -12px rgba(42,26,14,.6)}
.rzh-z svg{width:25px;height:25px;fill:none;stroke:#f3cd94;stroke-width:1.35;stroke-linecap:round;stroke-linejoin:round}
.rzh-p b{display:block;font-family:var(--serif);font-weight:700;font-size:clamp(1.24rem,1.56vw,1.6rem);line-height:1.14;color:var(--tinte);margin:2px 0 7px}
.rzh-p p{margin:0;font-size:clamp(.98rem,1.04vw,1.06rem);line-height:1.5;color:rgba(42,26,14,.8);max-width:48ch}
.rzh-kn{display:flex;flex-wrap:wrap;gap:12px 14px;margin-top:clamp(20px,2.2vw,32px)}
@media (max-width:700px){.rzh-kn .kn{max-width:100%;white-space:normal;line-height:1.35;text-align:left}.rzh-kn .kn i{flex:none}}
.js #telefon3d-text .rzh-p li,.js #telefon3d-text .rzh-kn{opacity:0;transform:translateX(34px);transition:opacity .9s cubic-bezier(.16,1,.3,1),transform 1.2s cubic-bezier(.16,1,.3,1);transition-delay:calc(var(--i,0)*120ms)}
.js #telefon3d-text.steht .rzh-p li,.js #telefon3d-text.steht .rzh-kn{opacity:1;transform:none}
.rzh-b .m-telefon{display:none;margin:0}
.rzh-b.rzh--flach canvas,.rzh-b.rzh--flach .rzh-sch{display:none}
.rzh-b.rzh--flach .m-telefon{display:block;position:absolute;left:30%;top:50%;width:min(270px,22vw);transform:translate(-50%,-50%);animation:rzh-flach 1.2s cubic-bezier(.16,1,.3,1) both}
@keyframes rzh-flach{from{transform:translate(-50%,-38%)}to{transform:translate(-50%,-50%)}}
.rzh-b .m-tel-rahmen{padding:10px;border-radius:44px;background:linear-gradient(160deg,#2b2d33,#0d0e11 45%,#1b1c20);box-shadow:0 0 0 1.5px #3a3c42,0 40px 60px -34px rgba(42,26,14,.6)}
.rzh-b .m-tel-film{display:block;width:100%;height:auto;border-radius:34px;background:#1f1209}
@media (max-width:900px) and (orientation:portrait),(max-width:700px){
  .rzh-b{height:auto;display:block;padding:0 var(--rand)}
  .rzh-b .tel-pin{position:static;display:flex;flex-direction:column;gap:clamp(30px,7vw,44px)}
  .rzh-b canvas,.rzh-sch{display:none}
  #rezeption .kopfzeile{margin-bottom:clamp(34px,8vw,56px)}
  #rezeption #telefon3d-text{position:static;transform:none;max-width:none;order:2}
  .rzh-b .m-telefon{display:block;order:1;margin:0 auto;width:min(292px,74vw)}
  .rzh-p li{grid-template-columns:46px minmax(0,1fr)}.rzh-z{width:46px;height:46px}.rzh-z svg{width:21px;height:21px}
}
/* drei freie Stücke: Handy, Karte und Seite liegen ohne Fläche auf dem Grund, jedes leicht gedreht, darunter der Text ohne Rahmen. Unter der Maus bleibt alles liegen. */
.rzh-st{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(30px,4.6vw,90px);margin-top:clamp(64px,8vw,136px);align-items:start}
.rzh-s{display:flex;flex-direction:column;align-items:center;text-align:center;color:var(--tinte);text-decoration:none}
.rzh-s__o{width:100%;height:clamp(300px,31vw,480px);display:flex;align-items:center;justify-content:center;margin-bottom:clamp(34px,3.8vw,60px)}
.rzh-s__k{height:86%;border-radius:clamp(14px,1.6vw,26px);overflow:hidden;box-shadow:0 1px 1px rgba(42,26,14,.1),0 34px 46px -24px rgba(42,26,14,.5),0 12px 18px -12px rgba(42,26,14,.24)}
.rzh-s__k--tel{aspect-ratio:440/952;padding:6px;background:linear-gradient(160deg,#2b2d33,#0d0e11 45%,#1b1c20)}
.rzh-s__k--tel img{border-radius:clamp(9px,1.2vw,20px)}
.rzh-s__k--karte{aspect-ratio:var(--f,640/902);border-radius:4px}
.rzh-s__b{width:min(100%,540px);aspect-ratio:1280/800;border-radius:clamp(10px,1vw,16px);overflow:hidden;box-shadow:0 1px 1px rgba(42,26,14,.1),0 40px 54px -26px rgba(42,26,14,.5),0 14px 20px -14px rgba(42,26,14,.24)}
.rzh-s__k img,.rzh-s__b img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 0}
.rzh-s small{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--taupe)}
.rzh-s h3{font-family:var(--serif);font-weight:700;font-size:clamp(1.4rem,1.9vw,1.96rem);line-height:1.12;margin:12px 0 12px}
.rzh-s p{margin:0;max-width:36ch;font-size:clamp(.98rem,1.04vw,1.06rem);line-height:1.55;color:rgba(42,26,14,.8)}
.rzh-s .pfeil{margin-top:18px;color:var(--tinte)}
@media (max-width:899px){
  .rzh-st{grid-template-columns:1fr;gap:clamp(64px,14vw,96px)}
  .rzh-s__o{height:clamp(280px,84vw,420px);margin-bottom:30px}
  .rzh-s__b{width:min(100%,440px)}
}
.rzh-hin{margin:clamp(34px,4.2vw,60px) auto 0;padding-top:20px;border-top:1px solid rgba(125,79,39,.3);max-width:68ch;text-align:center;font-size:1rem;line-height:1.55;color:rgba(42,26,14,.76)}
@media (prefers-reduced-motion:reduce){.js #telefon3d-text .rzh-p li,.js #telefon3d-text .rzh-kn{opacity:1;transform:none;transition:none}.rzh-b.rzh--flach .m-telefon{animation:none}}
'''

JS = '''<script>(function(){var b=document.getElementById('s-telefon3d');if(!b)return;document.documentElement.classList.add('js');
var t=document.getElementById('telefon3d-text'),film=document.getElementById('m-tel-film');
var mobil=matchMedia('(max-width:900px) and (orientation:portrait),(max-width:700px)').matches,drei=false,los=false,gesehen=false,wartet=false,vorrat=false,flach=false,steht=false,gZeit=0,tStart=0;
/* Ruhe-Planer: Skript auswerten und Modell auspacken laufen erst, wenn seit 700 ms nicht gescrollt wurde, spätestens nach 8 s; steht der Abschnitt schon im Bild, sofort */
var ruheJobs=[],letzt=0,ruheUhr=0;function jz(){return performance.now()}
function nah(){var r=b.getBoundingClientRect();return r.top<innerHeight*2.5&&r.bottom>-innerHeight}
function imBild(){var r=b.getBoundingClientRect();return r.top<innerHeight*.85&&r.bottom>innerHeight*.15}
function ruheTick(){ruheUhr=0;if(!ruheJobs.length)return;var z=jz(),da=imBild();if(da||z-letzt>700||(z-ruheJobs[0][1]>8000&&nah())){var j=ruheJobs.shift();try{j[0]()}catch(x){}}if(ruheJobs.length)ruheUhr=setTimeout(ruheTick,da?0:150)}
window.__tsWennRuhig=window.__tsWennRuhig||function(fn){ruheJobs.push([fn,jz()]);if(!ruheUhr)ruheUhr=setTimeout(ruheTick,0)};
window.__tsWennLeitungFrei=window.__tsWennLeitungFrei||function(fn,spaet){var ab=jz();(function pr(){var h=innerHeight,offen=0;[].forEach.call(document.images,function(i){if(i.complete||!(i.currentSrc||i.getAttribute('src')))return;var r=i.getBoundingClientRect();if(r.top<h*4&&r.bottom>-h)offen++});if(!offen||jz()-ab>(spaet||6000))fn();else setTimeout(pr,300)})()};
addEventListener('scroll',function(){letzt=jz()},{passive:true});addEventListener('wheel',function(){letzt=jz()},{passive:true});addEventListener('touchmove',function(){letzt=jz()},{passive:true});
function laden(){if(drei)return;drei=true;window.__tsWennRuhig(function(){var s=document.createElement('script');s.src=b.getAttribute('data-src');s.onerror=function(){window.__telefonFehler()};document.body.appendChild(s)});
/* Bodenschatten des Modells aus (auf hellem Grund kästchenförmig), sobald das Modell da ist */
var n=0,w=setInterval(function(){var z=window.__telefonSzene&&window.__telefonSzene(),g=false;if(z)z.szene.traverse(function(o){if(o.isMesh&&o.material&&o.material.type==='ShadowMaterial'){o.visible=false;g=true}});if(g||++n>600)clearInterval(w)},100)}
function hole(){if(vorrat||mobil)return;vorrat=true;
var l=document.createElement('link');l.rel='preload';l.as='script';l.href=b.getAttribute('data-src');document.head.appendChild(l);
function ab(u,art){return fetch(u).then(function(r){if(!r.ok)throw new Error(r.status);return r[art]()})}
var v={film:ab(b.getAttribute('data-film'),'blob'),modell:ab(b.getAttribute('data-modell'),'arrayBuffer')};v.film.catch(function(){});v.modell.catch(function(){});window.__telefonVorrat=v;laden()}
function filmStart(){if(los||!film)return;los=true;film.preload='auto';film.load();film.addEventListener('canplay',function(){var p=film.play();if(p&&p.catch)p.catch(function(){})},{once:true})}
function filmNah(){if(!film||los)return;var h=innerHeight,f=film.getBoundingClientRect();if(f.top<h*.6&&f.bottom>h*.3)filmStart()}
function stell(){if(steht)return;steht=true;t.classList.add('steht')}
window.__telefonFehler=function(){if(flach||mobil)return;var k=window.__telefonTakte&&window.__telefonTakte();if(k&&k.geladen)return;flach=true;b.classList.add('rzh--flach');filmNah();bald()};
function textUhr(){if(steht)return;if(mobil||flach){stell();return}var k=window.__telefonTakte&&window.__telefonTakte(),z=jz();if(k&&k.laeuftSchleife&&!tStart)tStart=z;if((tStart&&z-tStart>1500)||z-gZeit>3200){stell();return}setTimeout(textUhr,100)}
function fertig(){return gesehen&&(mobil||flach?los:drei)}
function pruefe(){wartet=false;var h=innerHeight,r=b.getBoundingClientRect();
if(!mobil&&!vorrat&&r.top<h*3&&r.bottom>-h)hole();
if(mobil||flach)filmNah();
if(!gesehen){var o=mobil?t.getBoundingClientRect():r,s=(Math.min(o.bottom,h)-Math.max(o.top,0))/Math.min(o.height||1,h);if(s>=(mobil?.2:.45)){gesehen=true;gZeit=jz();textUhr();if(!mobil)setTimeout(function(){window.__telefonFehler()},12000)}}
if(fertig()){removeEventListener('scroll',bald);removeEventListener('resize',bald)}}
function bald(){if(!wartet){wartet=true;requestAnimationFrame(pruefe)}}
addEventListener('scroll',bald,{passive:true});addEventListener('resize',bald);addEventListener('load',bald);pruefe();
function nachLaden(){if(mobil||vorrat)return;window.__tsWennLeitungFrei(hole,3000)}
if(document.readyState==='complete')nachLaden();else addEventListener('load',nachLaden);
if(film)film.addEventListener('click',function(){filmStart();var p=film.play();if(p&&p.catch)p.catch(function(){})})})();</script>'''


def abschnitt(g):
    """EIGENE-Eintrag für haus.py. g = globals() von haus.py (REZEPTION, REZEPTION_KARTEN, REZEPTION_HINWEIS, KAPITEL)."""
    RZ, RK, HIN = g['REZEPTION'], g.get('REZEPTION_KARTEN', {}), g.get('REZEPTION_HINWEIS', '')
    rez_link = g.get('REZEPTION_LINK', '../rezeption/')

    def bau(k):
        bild, kn, e, m = k['bild'], k['kn'], k['e'], k['m']
        punkte = ''.join(f'<li style="--i:{i}"><span class="rzh-z"><svg viewBox="0 0 24 24" aria-hidden="true">{ZEICHEN[i % len(ZEICHEN)]}</svg></span><div><b>{e(ti)}</b><p>{e(x)}</p></div></li>'
                         for i, (ti, x) in enumerate(RZ))
        km, kq, ks = RK['mappe'], RK['karte'], RK['seite']
        pf = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
        alt = 'Ein Gast fragt die Rezeption des Landgasthof Ruedihus nach Fondue am Abend, die Buchungsmaske erscheint'
        hat_mappe = os.path.exists(os.path.join(ROOT, 'mappe.html'))

        def stueck(i, ding, klein, titel_, satz, link='', wort=''):
            innen = (f'<div class="rzh-s__o">{ding}</div><div data-a="auf" style="--i:{i + 1}"><small>{e(klein)}</small><h3>{e(titel_)}</h3><p>{satz}</p>'
                     + (f'<span class="pfeil">{wort}{pf}</span>' if link else '') + '</div>')
            return (f'<a class="rzh-s" href="{link}" target="_blank" rel="noopener">{innen}</a>' if link else f'<div class="rzh-s">{innen}</div>')

        handy = f'<div class="rzh-s__k rzh-s__k--tel" data-a="schweb" style="--i:0;--r:-4deg;--r0:-11deg">{bild("ch-chat-h", "Die Rezeption im Chat am Handy")}</div>' if 'ch-chat-h' in m else ''
        qw, qh = m.get('qr-karte', (640, 902))
        karte = f'<div class="rzh-s__k rzh-s__k--karte" data-a="schweb" style="--i:1;--r:3deg;--r0:9deg;--f:{qw}/{qh}">{bild("qr-karte", "Die Karte zur Zimmermappe mit QR-Code")}</div>' if 'qr-karte' in m else ''
        seite = f'<div class="rzh-s__b" data-a="schweb" style="--i:2;--r:-2deg;--r0:-7deg">{bild("ch-rezeption", "Die Seite «Rezeption im Chat»")}</div>' if 'ch-rezeption' in m else ''
        kacheln = ((stueck(0, handy, km[0], km[1], km[2], g.get('MAPPE_LINK', '../mappe.html') if hat_mappe else '', 'Zimmermappe öffnen') if handy else '')
                   + (stueck(1, karte, kq[0], kq[1], kq[2], '../drucksachen/index.html', 'Karte ansehen') if karte else '')
                   + (stueck(2, seite, ks[0], ks[1], ks[2], rez_link, 'Seite ansehen') if seite else ''))
        return f'''
<section class="fl {k['fl']} blatt rzh" id="rezeption">
  <div class="in">
    {k['kopf']()}
  </div>
  <div class="rzh-b" id="s-telefon3d" data-basis="../" data-src="eigen/rezeption3d.js?v={SKRIPT_V}" data-film="../assets/video/rezeption-schirm.mp4?v={FILM_V}" data-zeichen="../assets/3d/rezeption-zeichen.png?v={FILM_V}" data-modell="../assets/3d/rezeption-phone.glb?v=1" data-dauer="{DAUER}">
    <div class="tel-pin">
      <canvas id="cv-telefon3d" aria-label="{e(alt)}" role="img"></canvas>
      <div id="telefon3d-text">
        <ul class="rzh-p">{punkte}</ul>
        <div class="rzh-kn" style="--i:{len(RZ)}">{kn('Alles, was sie kann: die Seite dazu', rez_link, neu=True)}{kn('Rezeption auf der Website öffnen', '../index.html', 'kn--linie', neu=True)}</div>
      </div>
      <figure class="m-telefon" id="m-telefon"><div class="m-tel-rahmen"><video class="m-tel-film" id="m-tel-film" muted playsinline preload="none" width="360" height="778" poster="eigen/rezeption-fondue-start.webp?v={FILM_V}" aria-label="{e(alt)}">
        <source src="../assets/video/rezeption-schirm-m.mp4?v={FILM_V}" type="video/mp4"></video></div></figure>
      <div class="rzh-sch" aria-hidden="true"></div>
    </div>
  </div>
  <div class="in">
    <div class="rzh-st">{kacheln}</div>
    {f'<p class="rzh-hin" data-a="auf">{HIN}</p>' if HIN else ''}
  </div>
  {JS}
</section>'''
    return dict(key='rezeption', nach='studio', name='Rezeption im Chat', zeilen=['Eine Rezeption,', 'die nie schläft.'],
                text=g.get('REZEPTION_TEXT', ''), bau=bau)
