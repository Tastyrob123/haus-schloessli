// Film der Rezeption im Chat für die Werkbank: node _werkbank/chat_film.js
//   Startseite, der Zeiger fährt zum Zeichen unten rechts, Klick, das Fenster geht auf, das Bild fährt in das Fenster hinein (Zoom),
//   die Fondue-Frage wird getippt, die Antwort kommt (Wortlaut der Antwort vom 10.10.2026, dokumentiert auf der Seite «Rezeption im Chat»;
//   die Funktion selbst läuft nur online und kostet je Frage). Ergebnis: _werkbank/film/s-rezeption.mp4 + s-rezeption.jpg.
//   Technik wie beim Carlton (Screencast in doppelter Schärfe, 30 Bilder je Sekunde, Zoom per ffmpeg).
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = process.env.BASE || 'http://127.0.0.1:8917/';
const FILM = path.join(__dirname, 'film'), GR = { width: 1200, height: 900 }, FRAGE = 'Wir sind zu zweit und möchten am Abend Fondue essen. Geht das?';
const ANTWORT = 'Ja, sehr gerne. Das Restaurant ist am Abend geöffnet und Fondue ist eine unserer Spezialitäten.\n- Restaurant geöffnet: 11:30 bis 21:00 Uhr\n- Friburger Original Chäsfondue: CHF 29.00\n- Tisch reservieren: +41 33 675 81 81 oder info@doldenhorn.ch';
const ZEIGER = `(() => { const mk = () => { if (document.getElementById('__zeiger') || !document.body) return;
  const c = document.createElement('div'); c.id = '__zeiger';
  c.style.cssText = 'position:fixed;left:0;top:0;width:34px;height:34px;z-index:2147483647;pointer-events:none;opacity:0;transition:opacity .15s';
  c.innerHTML = '<svg viewBox="0 0 24 24" width="34" height="34" style="transition:transform .12s;transform-origin:4px 3px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))"><path d="M4 3l15 8.4-6.6 1.7L9.4 20z" fill="#fff" stroke="#2a1a0e" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  document.body.appendChild(c);
  let x = 0, y = 0;
  addEventListener('mousemove', e => { x = e.clientX; y = e.clientY; c.style.opacity = 1; c.style.transform = 'translate(' + (x - 5) + 'px,' + (y - 4) + 'px)'; }, true);
  addEventListener('mousedown', () => { c.firstChild.style.transform = 'scale(.8)';
    const r = document.createElement('div'); r.style.cssText = 'position:fixed;left:' + (x - 26) + 'px;top:' + (y - 26) + 'px;width:52px;height:52px;border-radius:50%;border:3px solid #c98543;background:rgba(201,133,67,.25);z-index:2147483646;pointer-events:none;transform:scale(.3);opacity:1;transition:transform .55s cubic-bezier(.16,1,.3,1),opacity .55s';
    document.body.appendChild(r); requestAnimationFrame(() => { r.style.transform = 'scale(1.5)'; r.style.opacity = 0; }); setTimeout(() => r.remove(), 650); }, true);
  addEventListener('mouseup', () => { c.firstChild.style.transform = ''; }, true); };
  document.readyState === 'loading' ? addEventListener('DOMContentLoaded', mk) : mk(); })();`;
(async () => {
  fs.mkdirSync(FILM, { recursive: true });
  const br = await chromium.launch();
  const ctx = await br.newContext({ viewport: GR, deviceScaleFactor: 2, locale: 'de-CH' });
  await ctx.addInitScript(ZEIGER);
  await ctx.route('**/api/gast*', r => r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ text: ANTWORT }) }));
  const s = await ctx.newPage();
  const cdp = await ctx.newCDPSession(s), dir = path.join(FILM, '_rezeption'), bilder = [];
  fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  cdp.on('Page.screencastFrame', f => { const n = String(bilder.length).padStart(5, '0') + '.jpg'; fs.writeFileSync(path.join(dir, n), Buffer.from(f.data, 'base64')); bilder.push([n, f.metadata.timestamp]); cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {}); });
  await s.goto(B + 'index.html?nomotion', { waitUntil: 'load' }); await s.waitForTimeout(2500);
  await s.evaluate(() => scrollTo(0, Math.round(innerHeight * 1.2))); await s.waitForTimeout(1200);
  await s.mouse.move(600, 380);
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 93, maxWidth: GR.width * 2, maxHeight: GR.height * 2, everyNthFrame: 1 });
  await s.waitForTimeout(400);
  const start = Date.now() / 1000;
  await s.waitForTimeout(1100);
  const kb = await s.locator('.gast-knopf').boundingBox();
  await s.mouse.move(kb.x + kb.width / 2, kb.y + kb.height / 2, { steps: 40 }); await s.waitForTimeout(500);
  await s.mouse.down(); await s.waitForTimeout(110); await s.mouse.up();
  await s.waitForSelector('.gast__feld input', { timeout: 10000 }); await s.waitForTimeout(900);
  const zoomAb = Date.now() / 1000;
  const fb = await s.locator('.gast').boundingBox();
  await s.waitForTimeout(1300);
  const eb = await s.locator('.gast__feld input').boundingBox();
  await s.mouse.move(eb.x + 60, eb.y + eb.height / 2, { steps: 26 }); await s.waitForTimeout(300); await s.mouse.down(); await s.waitForTimeout(90); await s.mouse.up(); await s.waitForTimeout(500);
  await s.keyboard.type(FRAGE, { delay: 42 }); await s.waitForTimeout(600); await s.keyboard.press('Enter');
  await s.waitForTimeout(4600);
  await s.mouse.move(eb.x + 120, eb.y - 90, { steps: 20 });
  await s.waitForTimeout(2200);
  const ende = Date.now() / 1000;
  await cdp.send('Page.stopScreencast').catch(() => {}); await s.close(); await br.close();
  let ab = bilder.findIndex(b => b[1] >= start); if (ab < 0) ab = 0;
  const l = bilder.slice(ab);
  const seq = path.join(dir, 'seq'); fs.mkdirSync(seq);
  const t0 = l.length ? l[0][1] : ende; let j = 0, n = 0;
  for (let t = t0; t < ende; t += 1 / 30) { while (j + 1 < l.length && l[j + 1][1] <= t) j++; fs.symlinkSync(path.join(dir, l[j][0]), path.join(seq, String(n++).padStart(5, '0') + '.jpg')); }
  // Zoom in das Fenster: ab Bild N in rund einer Sekunde auf das 1,4-Fache, Mitte des Fensters bleibt in der Mitte
  const N = Math.max(0, Math.round((zoomAb - t0) * 30)), Z = 1.4, W = GR.width * 2, H = GR.height * 2;
  const cx = Math.round((fb.x + fb.width / 2) * 2), cy = Math.round((fb.y + fb.height / 2) * 2);
  const z = `if(lt(in,${N}),1,min(1+(in-${N})*0.014,${Z}))`;
  const x = `min(max(${cx}-iw/zoom/2,0),iw-iw/zoom)`, y = `min(max(${cy}-ih/zoom/2,0),ih-ih/zoom)`;
  const ziel = path.join(FILM, 's-rezeption.mp4');
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '30', '-i', path.join(seq, '%05d.jpg'), '-vf', `zoompan=z='${z}':x='${x}':y='${y}':d=1:s=${W}x${H}:fps=30`, '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', ziel]);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(((ende - t0) * 0.78).toFixed(2)), '-i', ziel, '-frames:v', '1', '-q:v', '2', path.join(FILM, 's-rezeption.jpg')]);
  fs.rmSync(dir, { recursive: true, force: true });
  console.log('ok Film rezeption', l.length, 'Bilder', (ende - t0).toFixed(1) + ' s, Zoom ab Bild', N, 'auf', cx, cy);
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(1); });
