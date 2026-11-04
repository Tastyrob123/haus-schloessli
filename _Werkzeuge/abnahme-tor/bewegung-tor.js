#!/usr/bin/env node
// Abnahme-Tor · Bewegung beim Scrollen (Kriterien 34 «flüssig» und 37 «Bewegung»), WebKit.
// Je Seite: (1) mit Bewegung langsam durchscrollen, jede Bildfolge messen (Bilder über 50 ms = Ruckler), laufende Animationen und ihre Eigenschaften
// erfassen (nur transform/opacity erlaubt), nach dem Scrollen nach Stücken suchen, die unsichtbar hängen geblieben sind;
// (2) mit prefers-reduced-motion: alles sofort sichtbar, keine langen Bewegungen.
// Aufruf: node bewegung-tor.js <ziele.json> <ausgabe-ordner> [--nur k1,k2] [--groesse 1440x900]
const path = require('path'), fs = require('fs');
const pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const [ZIELE, AUS] = process.argv.slice(2);
let ziele = JSON.parse(fs.readFileSync(ZIELE, 'utf8')).ziele; if (arg('nur')) ziele = ziele.filter(z => arg('nur').split(',').includes(z.k));
const [W, H] = arg('groesse', '1440x900').split('x').map(Number);
fs.mkdirSync(path.join(AUS, 'bilder'), { recursive: true });
const warte = ms => new Promise(r => setTimeout(r, ms));

const messeScroll = async (p) => p.evaluate(async () => {
  const frames = []; let laufend = true, letzte = performance.now();
  const tick = t => { frames.push(t - letzte); letzte = t; if (laufend) requestAnimationFrame(tick); }; requestAnimationFrame(tick);
  const eigenschaften = new Set(), animiert = new Set(); let maxAnim = 0;
  const sammle = () => { const a = document.getAnimations().filter(x => { const t = x.effect && x.effect.getTiming && x.effect.getTiming(); return !t || !(+t.duration <= 50) || t.iterations === Infinity; }); maxAnim = Math.max(maxAnim, a.length);   // Übergänge ≤ 50 ms sind Sprünge, keine Bewegung
    for (const x of a) { const ef = x.effect; if (!ef || !ef.getKeyframes) continue; const tgt = ef.target; if (tgt) animiert.add(tgt.tagName + '.' + String(tgt.className.baseVal ?? tgt.className).split(' ')[0]);
      if (x.transitionProperty) eigenschaften.add(x.transitionProperty); for (const k of ef.getKeyframes()) for (const p of Object.keys(k)) if (!['offset', 'easing', 'composite', 'computedOffset'].includes(p)) eigenschaften.add(p); } };
  const hoch = document.documentElement.scrollHeight, schritt = Math.max(40, innerHeight / 18);
  for (let y = 0; y <= hoch; y += schritt) { scrollTo(0, y); sammle(); await new Promise(r => setTimeout(r, 40)); }
  await new Promise(r => setTimeout(r, 1800)); sammle(); laufend = false;
  const f = frames.slice(2).filter(x => x < 1000); const sortiert = [...f].sort((a, b) => a - b);
  // Stücke im Fenster, die nach dem Scrollen unsichtbar geblieben sind (Auftritt nicht ausgelöst)
  // Ausgenommen: natives <select> mit opacity:0 und pointer-events:none unter einem eigenen Auswahlknopf (lib/auswahl.css .hwahl-nativ, Hausdruckerei Mail-Seite, 4.11.2026) – absichtlich unsichtbar, kein Auftritt
  const unsichtbar = []; for (let y = 0; y <= hoch; y += innerHeight * .8) { scrollTo(0, y); await new Promise(r => setTimeout(r, 900));
    for (const e of document.querySelectorAll('body *')) { const r = e.getBoundingClientRect(); if (r.width < 30 || r.height < 14 || r.bottom < 0 || r.top > innerHeight) continue;
      const c = getComputedStyle(e); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity >= .1) continue; if (e.tagName === 'SELECT' && c.pointerEvents === 'none') continue; let a = e.parentElement, schon = false; while (a) { const ca = getComputedStyle(a); if (+ca.opacity < .1 || ca.visibility === 'hidden' || ca.display === 'none') { schon = true; break; } a = a.parentElement; }
      if (!schon && (e.innerText || '').trim() || (!schon && e.querySelector('img'))) unsichtbar.push({ sel: e.tagName.toLowerCase() + '.' + String(e.className.baseVal ?? e.className).trim().split(/\s+/).slice(0, 2).join('.'), text: (e.innerText || '').trim().slice(0, 40), y: Math.round(r.top + scrollY) }); } }
  const u = [...new Map(unsichtbar.map(x => [x.sel + x.text, x])).values()].slice(0, 20);
  return { bilder: f.length, ruckler: f.filter(x => x > 50).length, p95: sortiert[Math.floor(sortiert.length * .95)] || 0, mittel: f.reduce((a, b) => a + b, 0) / Math.max(1, f.length), maxAnim, animiert: [...animiert].slice(0, 30), eigenschaften: [...eigenschaften], unsichtbar: u };
});

/* Grundlinie des Rechners (Oberchef 3.11.2026, Nachtbau Schlössli): Auf den GitHub-Rechnern (2 Kerne, WebKit ohne GPU) ruckelte das Scrollen in allen sieben
   Werkzeugen, auch im nahezu stillen Hafenbüro (78 Bilder über 50 ms), während dieselben Seiten in Chromium mit 12-fach gedrosselter Rechenleistung glatt liefen
   (höchstens 1 Bild über 50 ms). Darum misst das Tor zuerst eine stille Vergleichsseite (langer Text, Verläufe, keine Skripte) auf demselben Rechner und
   hebt die Schwellen um das, was der Rechner selbst nicht schafft. Die Grundlinie steht im Ergebnis und in jedem Fund. */
const GRUNDSEITE = 'data:text/html;charset=utf-8,' + encodeURIComponent('<!doctype html><meta name=viewport content="width=device-width"><style>body{margin:0;font:18px/1.6 system-ui;background:#f4f6f9}section{min-height:100vh;padding:40px;display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:center}h1{font-size:64px;grid-column:1/-1}'
  + '.f{overflow:hidden;border-radius:16px;aspect-ratio:3/2;box-shadow:0 18px 40px -26px rgba(4,16,35,.45)}.f img{width:100%;height:112%;display:block;object-fit:cover;animation:z 2.6s cubic-bezier(.19,1,.22,1) both}@keyframes z{from{scale:1.12}}'
  + '@supports (animation-timeline:view()){@keyframes p{from{translate:0 -6%}to{translate:0 0}}.f img{animation:z 2.6s cubic-bezier(.19,1,.22,1) both,p linear both;animation-timeline:auto,view();animation-range:normal,exit 0% exit 100%}}</style>'
  + Array.from({ length: 12 }, (_, i) => `<section><h1>Abschnitt ${i + 1}</h1><p>${'Ein ruhiger Satz zum Scrollen. '.repeat(30)}</p><div class=f><img id=b${i}></div></section>`).join('')
  + '<script>(function(){var c=document.createElement("canvas");c.width=1600;c.height=1067;var x=c.getContext("2d");var g=x.createLinearGradient(0,0,1600,1067);g.addColorStop(0,"#0b1d3d");g.addColorStop(.5,"#a2b6cf");g.addColorStop(1,"#e7ecf3");x.fillStyle=g;x.fillRect(0,0,1600,1067);'
  + 'var d=x.getImageData(0,0,1600,1067),q=d.data;for(var i=0;i<q.length;i+=4){var n=(Math.random()-.5)*40;q[i]+=n;q[i+1]+=n;q[i+2]+=n}x.putImageData(d,0,0);var u=c.toDataURL("image/jpeg",.85);document.querySelectorAll("img").forEach(function(im){im.src=u})})()</script>');
/* Die Vergleichsseite trägt dieselbe Arbeit wie die Startbilder der Werkzeuge: zwölf grosse Fotos (1600 px, Rauschen wie ein Foto), die beim Erscheinen zoomen und
   beim Scrollen mitziehen (Scroll-Zeitachse wie im Kleid). Was der Rechner damit nicht schafft, wird keinem Werkzeug angelastet. */
const messeGrund = async (b) => {
  const ctx = await b.newContext({ viewport: { width: W, height: H }, locale: 'de-DE' }); const p = await ctx.newPage();
  await p.goto(GRUNDSEITE, { waitUntil: 'load', timeout: 30000 }).catch(() => { }); await warte(800);
  const m = await messeScroll(p).catch(() => ({ ruckler: 0, p95: 0, bilder: 0 })); await ctx.close();
  return { ruckler: m.ruckler || 0, p95: m.p95 || 0, bilder: m.bilder || 0 };
};
(async () => {
  const b = await pw.webkit.launch(); const erg = [];
  const grund = await messeGrund(b); const rucklerMax = Math.max(2, grund.ruckler + 2), p95Max = Math.max(34, grund.p95 * 1.5);
  const grundText = `Grundlinie dieses Rechners: ${grund.ruckler} Bilder über 50 ms, 95 % unter ${Math.round(grund.p95)} ms (${grund.bilder} Bilder); Schwellen ${rucklerMax} Ruckler / ${Math.round(p95Max)} ms`;
  console.log(grundText);
  for (const z of ziele) for (const url of [z.url, ...(z.startExtra || [])]) {
    const r = { k: z.k, name: z.name, url, funde: [] };
    for (const reduce of [false, true]) {
      const ctx = await b.newContext({ viewport: { width: W, height: H }, reducedMotion: reduce ? 'reduce' : 'no-preference', locale: 'de-DE' });
      await ctx.route('**/*', q => q.request().method() === 'GET' || q.request().method() === 'HEAD' ? q.continue() : q.fulfill({ status: 200, body: '{}' }));
      await ctx.addInitScript(v => { try { for (const [k, w] of Object.entries(v || {})) localStorage.setItem(k, w); } catch (e) { } }, z.localStorage || {});
      const p = await ctx.newPage(); const t0 = Date.now();
      await p.goto(url, { waitUntil: 'load', timeout: 30000 }).catch(() => { }); const lade = Date.now() - t0; await warte(1200);
      const m = await messeScroll(p).catch(e => ({ fehler: String(e).slice(0, 120) }));
      await p.evaluate(() => scrollTo(0, 0)); await warte(400);
      const bild = `${z.k}-${(url.split('?')[1] || 'start').replace(/\W+/g, '')}-${reduce ? 'ruhig' : 'bewegt'}.jpg`;
      await p.screenshot({ path: path.join(AUS, 'bilder', bild), type: 'jpeg', quality: 70 }).catch(() => { });
      r[reduce ? 'ruhig' : 'bewegt'] = { ...m, ladezeit: lade, bild };
      if (m.fehler) r.funde.push({ k: 34, info: 'Messung fehlgeschlagen: ' + m.fehler });
      else if (!reduce) {
        let probeText = '';
        // Messprobe (4.11.2026, Nachtbau Schlössli): liegt probe.on neben diesem Skript, misst das Tor bei den Zielen aus probe.on dasselbe Scrollen noch einmal mit je einem abgeschalteten Effekt, um zu finden, was der Rechner nicht schafft
        const probeDatei = path.join(__dirname, 'probe.on');
        if (fs.existsSync(probeDatei) && fs.readFileSync(probeDatei, 'utf8').split(/[\s,]+/).includes(z.k) && url === z.url) {
          const AUS_ = { 'ohne Unschärfe': '*,*::before,*::after{backdrop-filter:none!important;-webkit-backdrop-filter:none!important}', 'ohne Schatten': '*,*::before,*::after{box-shadow:none!important;text-shadow:none!important}',
            'ohne Filter': '*,*::before,*::after{filter:none!important}', 'ohne Animation': '*,*::before,*::after{animation:none!important;transition:none!important}', 'ohne Hintergrundbilder': '*,*::before,*::after{background-image:none!important}',
            'ohne Bilder': 'img,video,canvas,svg{visibility:hidden!important}', 'ohne fest/klebend': '*{position:static!important}', 'ohne Mischmodus': '*,*::before,*::after{mix-blend-mode:normal!important;isolation:auto!important}',
            'ohne alles': '*,*::before,*::after{backdrop-filter:none!important;-webkit-backdrop-filter:none!important;box-shadow:none!important;text-shadow:none!important;filter:none!important;animation:none!important;transition:none!important;background-image:none!important;mix-blend-mode:normal!important}' };
          const teile = [];
          for (const [name, css] of Object.entries(AUS_)) {
            const p2 = await ctx.newPage(); await p2.goto(url, { waitUntil: 'load', timeout: 30000 }).catch(() => { }); await p2.addStyleTag({ content: css }).catch(() => { }); await warte(1200);
            const m2 = await messeScroll(p2).catch(() => null); await p2.close(); teile.push(`${name}: ${m2 ? m2.ruckler + '/' + Math.round(m2.p95) + ' ms' : '–'}`);
          }
          probeText = ' · Probe (Ruckler/p95): ' + teile.join('; '); r.probe = teile; console.log('Probe', z.k, teile.join(' | '));
        }
        if (m.ruckler > rucklerMax || m.p95 > p95Max || probeText) r.funde.push({ k: 34, info: `Scrollen ruckelt: ${m.ruckler} Bilder über 50 ms, 95 % der Bilder unter ${Math.round(m.p95)} ms (${m.bilder} Bilder) · ${grundText}${probeText}` });
        if (!m.maxAnim) r.funde.push({ k: 37, info: 'Keine Bewegung beim Scrollen (keine Animation lief)' });
        const fremd = m.eigenschaften.filter(x => !/^(transform|opacity|translate|scale|rotate|filter|clip-path|all)$/.test(x));
        if (fremd.length) r.funde.push({ k: 37, info: `Animiert auch ${fremd.slice(0, 6).join(', ')} (erlaubt nur transform/opacity)` });
        if (m.unsichtbar.length) r.funde.push({ k: 37, info: `${m.unsichtbar.length} Stücke bleiben nach dem Scrollen unsichtbar: ${m.unsichtbar.slice(0, 3).map(x => '«' + (x.text || x.sel) + '»').join(', ')}` });
      } else {
        if (m.unsichtbar.length) r.funde.push({ k: 37, info: `reduced-motion: ${m.unsichtbar.length} Stücke bleiben unsichtbar: ${m.unsichtbar.slice(0, 3).map(x => '«' + (x.text || x.sel) + '»').join(', ')}` });
        if (m.maxAnim > 6) r.funde.push({ k: 37, info: `reduced-motion: trotzdem ${m.maxAnim} Animationen gleichzeitig` });
      }
      await ctx.close();
    }
    erg.push(r); console.log(z.k, url.split('/').pop(), r.funde.length ? r.funde.map(f => 'K' + f.k + ' ' + f.info).join(' | ') : 'ok', `· ${r.bewegt && r.bewegt.bilder} Bilder, ${r.bewegt && r.bewegt.maxAnim} Animationen`);
    fs.writeFileSync(path.join(AUS, 'bewegung.json'), JSON.stringify({ zeit: new Date().toISOString(), groesse: [W, H], grundlinie: { ...grund, rucklerMax, p95Max }, seiten: erg }, null, 1));
  }
  await b.close();
})();
