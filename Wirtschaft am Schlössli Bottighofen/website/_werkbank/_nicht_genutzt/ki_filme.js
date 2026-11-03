// Filme für die Seite «KI und Ihre Daten» des Landgasthof Ruedihus (Robert 18.10.2026: «Ich dachte, dass da Videos sind»; Bauart aus der
// Werkbank des Carlton-Europe, dort nur gelesen). Echte Werkzeuge des Ruedihus auf dem Hausserver 8917, sichtbarer Zeiger, Bild für Bild über den
// Bildschirm-Mitschnitt (CDP). Keine KI-Kosten: Die Werkstatt bekommt die gespeicherten fünf Entwürfe (_werkzeuge/imprimerie/_qa/demo-fuenf.json),
// Der Gastgeber und Das Hausbuch zeigen ihre Beispiele. Rezeption im Chat nimmt den Handy-Film der Werkbank (eigen/rezeption-werkbank.mp4).
//   node _werkbank/ki_filme.js [imprimerie|reception|livre ...]   → _werkbank/kifilm/ki-<name>.mp4 + .webp (rh_ki.py legt sie nach werkbank/film/)
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.join(__dirname, '..'), OUT = path.join(__dirname, 'kifilm'), KOPIE = OUT;
fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(KOPIE, { recursive: true });
const W = 1440, H = 932;   // Bildschirm des Laptops in der Werkbank (ins-geraet.webp)
const warte = ms => new Promise(r => setTimeout(r, ms));

const ZEIGER_CSS = `#fz{position:fixed;left:0;top:0;width:30px;height:30px;z-index:2147483647;pointer-events:none;transition:transform .9s cubic-bezier(.45,.05,.25,1);transform:translate(720px,520px)}
#fz svg{width:30px;height:30px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.45))}
#fz i{position:absolute;left:-16px;top:-16px;width:32px;height:32px;border-radius:50%;border:2.5px solid #f3cd94;opacity:0;transform:scale(.4)}
#fz.klick i{animation:fzk .6s ease-out}
@keyframes fzk{0%{opacity:1;transform:scale(.4)}100%{opacity:0;transform:scale(1.8)}}`;
const ZEIGER = '<i></i><svg viewBox="0 0 24 24"><path d="M4 2.5l15.5 9.2-6.6 1.6 3.8 7.2-2.6 1.3-3.8-7.2-4.9 4.4z" fill="#fff" stroke="#11141f" stroke-width="1.3" stroke-linejoin="round"/></svg>';

async function film(b, name, url, ablauf, o = {}) {
  const ctx = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, locale: 'de-CH' });
  const p = await ctx.newPage();
  if (o.route) await o.route(p);
  await p.goto(url, { waitUntil: 'networkidle' });
  if (o.vorher) await o.vorher(p);
  await p.evaluate(() => document.fonts.ready);
  await warte(o.ruhe ?? 2600);
  await p.addStyleTag({ content: ZEIGER_CSS });
  await p.evaluate(z => { const d = document.createElement('div'); d.id = 'fz'; d.innerHTML = z; document.body.appendChild(d); }, ZEIGER);
  const cdp = await ctx.newCDPSession(p), bilder = [];
  cdp.on('Page.screencastFrame', async f => { bilder.push({ t: f.metadata.timestamp, d: f.data }); try { await cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }); } catch (e) { } });
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: W, maxHeight: H, everyNthFrame: 1 });
  await warte(900);
  const zu = async (x, y, ms = 900) => { await p.evaluate(([x, y]) => { document.getElementById('fz').style.transform = `translate(${x - 4}px,${y - 3}px)`; }, [x, y]); await p.mouse.move(x, y, { steps: 8 }); await warte(ms); };
  const mitte = async sel => { const r = await p.locator(sel).first().boundingBox(); if (!r) throw new Error('nicht gefunden: ' + sel); return [r.x + r.width / 2, r.y + r.height / 2]; };
  const ring = () => p.evaluate(() => { const z = document.getElementById('fz'); z.classList.remove('klick'); void z.offsetWidth; z.classList.add('klick'); });
  const klick = async (ziel, k = {}) => { const [x, y] = Array.isArray(ziel) ? ziel : await mitte(ziel); await zu(x, y, k.ms ?? 900); await ring(); await p.mouse.click(x, y); await warte(k.danach ?? 900); };
  // weiches Scrollen im Seitenfluss oder in einer Spalte (sel), Dauer ms, gleichmässig an- und auslaufend
  const scrolle = (sel, dy, ms = 2200) => p.evaluate(([sel, dy, ms]) => new Promise(res => {
    const el = sel ? document.querySelector(sel) : document.scrollingElement; const a = el.scrollTop, t0 = performance.now();
    const e = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
    (function f(t) { const k = Math.min(1, (t - t0) / ms); el.scrollTop = a + dy * e(k); if (k < 1) requestAnimationFrame(f); else res(); })(t0);
  }), [sel, dy, ms]).then(() => warte(250));
  await ablauf({ p, zu, klick, mitte, scrolle, warte });
  await warte(o.halten ?? 1600);
  await cdp.send('Page.stopScreencast');
  await ctx.close();

  const TMP = path.join(__dirname, '_kifilm-' + name); fs.rmSync(TMP, { recursive: true, force: true }); fs.mkdirSync(TMP);
  const liste = [];
  bilder.forEach((f, i) => { const n = path.join(TMP, `b${String(i).padStart(5, '0')}.jpg`); fs.writeFileSync(n, Buffer.from(f.d, 'base64'));
    liste.push(`file '${n}'`, `duration ${(i < bilder.length - 1 ? Math.max(.001, bilder[i + 1].t - f.t) : .6).toFixed(4)}`); });
  liste.push(`file '${path.join(TMP, `b${String(bilder.length - 1).padStart(5, '0')}.jpg`)}'`);
  fs.writeFileSync(path.join(TMP, 'liste.txt'), liste.join('\n'));
  const ziel = path.join(OUT, `ki-${name}.mp4`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(TMP, 'liste.txt'), '-vf', `scale=${W}:-2:flags=lanczos,fps=30,format=yuv420p`,
    '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '24', '-movflags', '+faststart', ziel]);
  const sb = path.join(TMP, 'stand.png');
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', String(o.standbild ?? 1), '-i', ziel, '-frames:v', '1', sb]);
  execFileSync('python3', ['-c', `from PIL import Image;Image.open(${JSON.stringify(sb)}).save(${JSON.stringify(path.join(OUT, `ki-${name}.webp`))},quality=78)`]);
  const dauer = bilder[bilder.length - 1].t - bilder[0].t;
  fs.rmSync(TMP, { recursive: true, force: true });
  console.log(name, dauer.toFixed(1) + ' s', bilder.length + ' Bilder', (bilder.length / dauer).toFixed(1) + ' Bilder/s', (fs.statSync(ziel).size / 1e3).toFixed(0) + ' kB');
}

const FUENF = JSON.parse(fs.readFileSync(path.join(ROOT, '_werkzeuge', 'imprimerie', '_qa', 'demo-fuenf.json'), 'utf8'));
const FILME = {
  // Satz eintippen → «Fünf Entwürfe anlegen» → die fünf Entwürfe zeigen → einen öffnen
  imprimerie: ['http://localhost:8917/_werkzeuge/imprimerie/?demo=1', async ({ p, klick, zu, mitte, scrolle, warte }) => {
    await p.waitForFunction(() => window.__ST && window.__ST.M, null, { timeout: 30000 }).catch(() => {});
    await klick('#auftrag', { danach: 300 });
    await p.keyboard.type('Ein Plakat A3 zur Metzgete in der Stube', { delay: 60 });
    await warte(500);
    await klick('text=Fünf Entwürfe anlegen', { danach: 300 });
    await p.waitForSelector('[data-entwurf]', { timeout: 20000 });
    /* der Prüf-Hinweis der Probe-Antwort gehört nicht in den Film */
    await p.evaluate(() => { const h = [...document.querySelectorAll('*')].find(e => e.children.length < 3 && /^Bitte noch ansehen/.test((e.textContent || '').trim())); if (h) { let k = h; while (k.parentElement && k.parentElement.textContent.trim().length < 400) k = k.parentElement; k.style.display = 'none'; } });
    await warte(2000);
    const sp = await p.evaluate(() => { const s = document.querySelector('[data-entwurf]'); let e = s && s.parentElement; while (e && !(e.scrollHeight > e.clientHeight + 40 && /(auto|scroll)/.test(getComputedStyle(e).overflowY))) e = e.parentElement; if (!e) return null; e.setAttribute('data-kifilm', '1'); return '[data-kifilm]'; });
    await zu(860, 300, 500);
    for (const i of [0, 1, 2, 3, 4]) { const el = p.locator(`[data-entwurf="${i}"]`).first(); if (!(await el.count())) continue;
      await el.scrollIntoViewIfNeeded().catch(() => {}); await warte(500); const [x, y] = await mitte(`[data-entwurf="${i}"]`); await zu(x, y - 40, 900); }
    const [x, y] = await mitte('[data-entwurf="1"]'); await klick([x, y - 40], { danach: 2600 });
  }, { route: p => p.route('**/api/entwurf', async r => { await warte(2600); r.fulfill({ json: FUENF }); }), halten: 1800, ruhe: 3500 }],

  // Eingang → Anfrage von Martina Huber (Tisch, Beispiel) → der Antwortbrief nach der Vorlage des Hauses
  reception: ['http://localhost:8917/_werkzeuge/reception/', async ({ p, klick, zu, mitte, scrolle, warte }) => {
    await klick('text=Eingang >> nth=0', { danach: 1700 });
    await klick('text=Martina Huber >> nth=0', { danach: 2000 });
    await zu(1000, 640, 700);
    // der Brief steht unten in der Anfrage: bis zu ihm in seiner eigenen Spalte (oder der Seite) weich hinunter, dann den Text entlang
    const [sel, dy] = await p.evaluate(() => { const b = document.querySelector('.brief'); if (!b) return [null, 600]; let e = b.parentElement;
      while (e && !(e.scrollHeight > e.clientHeight + 40 && /(auto|scroll)/.test(getComputedStyle(e).overflowY))) e = e.parentElement;
      const oben = e ? e.getBoundingClientRect().top : 0; if (e) e.setAttribute('data-kifilm', '1');
      return [e ? '[data-kifilm]' : null, Math.max(200, b.getBoundingClientRect().top - oben - 90)]; });
    await scrolle(sel, dy, 3000);
    await warte(1800);
    await scrolle(sel, 380, 2600);
  }, { halten: 2000 }],

  // Markenprüfung → «Beispiel ansehen» → Messung der Farben und Beurteilung in Ruhe
  livre: ['http://localhost:8917/_werkzeuge/livre/', async ({ p, klick, zu, scrolle, warte }) => {
    await klick('text=Markenprüfung >> nth=0', { danach: 1600 });
    await klick('text=Beispiel ansehen >> nth=0', { danach: 2600 });
    await zu(980, 560, 700);
    const sel = await p.evaluate(() => { const s = [...document.querySelectorAll('*')].find(e => e.scrollHeight > e.clientHeight + 200 && /(auto|scroll)/.test(getComputedStyle(e).overflowY) && e.clientHeight > 400);
      if (!s) return null; s.setAttribute('data-kifilm', '1'); return '[data-kifilm]'; });
    await scrolle(sel, 420, 2600);
    await warte(1400);
    await scrolle(sel, 380, 2400);
  }, { halten: 2000 }],
};

(async () => {
  const b = await chromium.launch();
  const nur = process.argv.slice(2);
  for (const [name, [url, ablauf, o]] of Object.entries(FILME)) {
    if (nur.length && !nur.includes(name)) continue;
    await film(b, name, url, ablauf, o || {});
  }
  await b.close();
})();
