// Nimmt kurze Filme vom Studio des Ruedihus auf, für die Werkbank. Läuft gegen eine Probe-Instanz mit eigenen Daten, nie gegen den echten Stand:
//   bash _qa/studio_probe.sh 8919 (oder nur der Server: RH_DATEN=/tmp/rh-probe/daten RH_LIVE=/tmp/rh-probe/live python3 studio.py 8919)
//   STUDIO=http://127.0.0.1:8919 MERK=/tmp/rh-probe/pw.txt node _werkbank/studio_film.js
//   Für die Werkbank seit 10.10.2026 mit eigener Instanz auf 8947: mkdir -p /tmp/rh-film/daten /tmp/rh-film/live; RH_DATEN=/tmp/rh-film/daten RH_LIVE=/tmp/rh-film/live python3 studio.py 8947
//   dann STUDIO=http://127.0.0.1:8947 MERK=/tmp/rh-film/pw.txt node _werkbank/studio_film.js
// Ergebnis: _werkbank/film/<name>.webm (das Kit macht daraus mp4 + Standbild) und _werkbank/ansichten/Studio/*.jpg
//   Standbilder für STUDIO['bilder'] in haus.py: zimmer, kontrolle (kontrolle.html), besuche und gaeste (aus der Online-Probe, lokal stünde dort nichts)
const path = require('path'), fs = require('fs'), crypto = require('crypto');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const B = process.env.STUDIO || 'http://127.0.0.1:8919';
const HIER = __dirname, ROOT = path.dirname(HIER), FILM = path.join(HIER, 'film'), BILD = path.join(HIER, 'ansichten', 'Studio');
const MERK = process.env.MERK || path.join(require('os').tmpdir(), 'rh-studio-probe.txt');
const FOTO = path.join(ROOT, 'assets', 'img', 'haus-wiese-l.webp');
const ZEIGER = `(() => { const mk = () => { if (document.getElementById('__zeiger') || !document.body) return;
  const c = document.createElement('div'); c.id = '__zeiger';
  c.style.cssText = 'position:fixed;left:0;top:0;width:34px;height:34px;z-index:2147483647;pointer-events:none;opacity:0;transition:opacity .15s';
  c.innerHTML = '<svg viewBox="0 0 24 24" width="34" height="34" style="transition:transform .12s;transform-origin:4px 3px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.45))"><path d="M4 3l15 8.4-6.6 1.7L9.4 20z" fill="#fff" stroke="#2a1a0e" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  document.body.appendChild(c);
  let x = 0, y = 0;
  addEventListener('mousemove', e => { x = e.clientX; y = e.clientY; c.style.opacity = 1; c.style.transform = 'translate(' + (x - 5) + 'px,' + (y - 4) + 'px)'; }, true);
  addEventListener('mouseover', e => { if (e.target && e.target.tagName === 'IFRAME') c.style.opacity = 0; }, true);
  document.documentElement.addEventListener('mouseleave', () => { c.style.opacity = 0; });
  addEventListener('mousedown', () => { c.firstChild.style.transform = 'scale(.8)';
    const r = document.createElement('div'); r.style.cssText = 'position:fixed;left:' + (x - 26) + 'px;top:' + (y - 26) + 'px;width:52px;height:52px;border-radius:50%;border:3px solid #c98543;background:rgba(201,133,67,.25);z-index:2147483646;pointer-events:none;transform:scale(.3);opacity:1;transition:transform .55s cubic-bezier(.16,1,.3,1),opacity .55s';
    document.body.appendChild(r); requestAnimationFrame(() => { r.style.transform = 'scale(1.5)'; r.style.opacity = 0; }); setTimeout(() => r.remove(), 650); }, true);
  addEventListener('mouseup', () => { c.firstChild.style.transform = ''; }, true); };
  document.readyState === 'loading' ? addEventListener('DOMContentLoaded', mk) : mk(); })();`;

(async () => {
  fs.mkdirSync(FILM, { recursive: true }); fs.mkdirSync(BILD, { recursive: true });
  for (const f of fs.readdirSync(BILD)) fs.unlinkSync(path.join(BILD, f));
  const br = await chromium.launch();
  const c0 = await br.newContext({ viewport: { width: 1440, height: 900 } });
  const p0 = await c0.newPage();
  await p0.goto(B + '/studio/'); await p0.waitForSelector('.tor__k');
  const neu = await p0.locator('.tor input[name=p2]').count();
  let pw = fs.existsSync(MERK) ? fs.readFileSync(MERK, 'utf8').trim() : '';
  if (neu) { pw = pw || crypto.randomBytes(12).toString('hex'); fs.writeFileSync(MERK, pw); }
  await p0.waitForTimeout(900);
  await p0.screenshot({ path: path.join(BILD, '01 Anmeldung.jpg'), quality: 90 });
  await p0.fill('.tor input[name=p]', pw); if (neu) await p0.fill('.tor input[name=p2]', pw);
  await p0.click('.tor button[type=submit]'); await p0.waitForSelector('.tuer'); await p0.waitForTimeout(1200);
  await p0.screenshot({ path: path.join(BILD, '02 Übersicht.jpg'), quality: 90 });
  for (const [h, n, warte] of [['#/karte/k1', '03 Karten', '.gz'], ['#/zimmer', '04 Zimmer und Preise', '[data-l="zimmer"] .gz'], ['#/haus', '05 Haus und Angaben', '[data-p="haus.zeiten"] input'], ['#/anlaesse', '06 Anlässe', '[data-l="anlaesse"] .gz'], ['#/bilder', '07 Bilder', '.bk'], ['#/seiten', '08 Seiten und Texte', '.sk']]) {
    await p0.goto(B + '/studio/' + h); await p0.waitForSelector(warte); await p0.waitForTimeout(1300);
    await p0.screenshot({ path: path.join(BILD, n + '.jpg'), quality: 90 });
  }
  // Standbilder für die Werkbank (STUDIO['bilder']): Zimmer mit geöffnetem Zimmer, Kontrolle, Besuche & Anfragen und Gäste & Anfragen aus der Online-Probe
  await p0.goto(B + '/studio/#/zimmer'); await p0.waitForSelector('[data-l="zimmer"] .gz'); await p0.waitForTimeout(900);
  await p0.locator('[data-l="zimmer"] .gz').nth(2).locator('.kn[data-akt="edit"]').click().catch(() => {}); await p0.waitForSelector('#lf-ok', { timeout: 8000 }).catch(() => {}); await p0.waitForTimeout(900);
  await p0.screenshot({ path: path.join(BILD, 'zimmer.jpg'), quality: 90 });
  await p0.goto((process.env.REAL || 'http://127.0.0.1:8917') + '/studio/kontrolle.html'); await p0.waitForTimeout(5500);   // Kontrolle vom echten Studio (die Probe meldet ihre fehlenden Teile)
  await p0.screenshot({ path: path.join(BILD, 'kontrolle.jpg'), quality: 90 });
  const ON = process.env.ONLINE || 'https://ruedihus.tastystudios.ch';
  for (const [h, n, warte] of [['/studio/#/besuche', 'besuche', '.in h2'], ['/studio/gaeste.html', 'gaeste', 'h1, h2']]) {
    try { await p0.goto(ON + h, { waitUntil: 'load', timeout: 60000 }); await p0.waitForSelector(warte, { timeout: 30000 }).catch(() => {}); await p0.waitForTimeout(3500); await p0.screenshot({ path: path.join(BILD, n + '.jpg'), quality: 90 }); console.log('ok   Bild', n); }
    catch (e) { console.log('FEHL Bild', n, String(e).split('\n')[0].slice(0, 160)); }
  }
  const zustand = await c0.storageState(); await c0.close();

  const ctx = await br.newContext({ viewport: { width: 1440, height: 900 }, storageState: zustand, recordVideo: { dir: FILM, size: { width: 1440, height: 900 } } });
  await ctx.addInitScript(ZEIGER);
  let maus = { x: 720, y: 450 };
  const NUR = process.env.NUR || '';
  const clip = async (name, tun) => {
    if (NUR && NUR !== name) return;
    const s = await ctx.newPage();
    const zu = async (x, y) => { await s.mouse.move(x, y, { steps: 28 }); maus = { x, y }; await s.waitForTimeout(260); };
    const auf = async (sel, o = {}) => { const l = typeof sel === 'string' ? s.locator(sel).first() : sel; await l.evaluate(el => el.scrollIntoView({ block: 'center', inline: 'nearest' })); await s.waitForTimeout(350); const b = await l.boundingBox(); await zu(b.x + (o.x != null ? o.x : b.width / 2), b.y + b.height / 2); };
    const klick = async (sel, o) => { await auf(sel, o); await s.mouse.down(); await s.waitForTimeout(90); await s.mouse.up(); await s.waitForTimeout(o && o.nach != null ? o.nach : 500); };
    const tipp = async t => { await s.keyboard.type(t, { delay: 48 }); await s.waitForTimeout(350); };
    const quitt = async t => { await s.waitForFunction(x => [...document.querySelectorAll('.quitt b, .quitt')].some(d => d.textContent.includes(x)) || !document.querySelector('#fenster:not([hidden]) #g-ok, #fenster:not([hidden]) #lf-ok, #w-schreib'), t, { timeout: 25000 }).catch(() => {}); };
    await s.mouse.move(maus.x, maus.y);
    try { await tun(s, { zu, auf, klick, tipp, quitt }); console.log('ok  ', name); } catch (e) { console.log('FEHL', name, String(e).split('\n')[0].slice(0, 200)); await s.screenshot({ path: path.join(FILM, name + '-fehler.png') }); }
    await s.waitForTimeout(1500);
    const v = s.video(); await s.close();
    const ziel = path.join(FILM, name + '.webm'); if (fs.existsSync(ziel)) fs.unlinkSync(ziel);
    fs.renameSync(await v.path(), ziel);
  };

  await clip('1-zimmer', async (s, w) => {
    await s.goto(B + '/studio/#/zimmer'); await s.waitForSelector('[data-l="zimmer"] .gz'); await s.waitForTimeout(1400);
    await w.klick(s.locator('[data-l="zimmer"] .gz').first().locator('.kn[data-akt="edit"]')); await s.waitForSelector('#lf-2'); await s.waitForTimeout(600);
    await w.klick('#lf-2'); await s.keyboard.press('Meta+A'); await w.tipp('Ab: 260.00 CHF / Nacht');
    await w.klick('#lf-ok'); await w.quitt('Zimmer gespeichert'); await s.waitForTimeout(2400);
  });
  await clip('2-gericht', async (s, w) => {
    await s.goto(B + '/studio/#/uebersicht'); await s.waitForSelector('.tuer'); await s.waitForTimeout(1200);
    await w.klick('.tuer[data-los="gericht"]'); await s.waitForSelector('#g-n'); await s.waitForTimeout(500);
    await w.klick('[data-chips="gruppe"] button:has-text("ÖPIS URCHIGS")');
    await w.klick('#g-n'); await w.tipp('CHÄSSCHNITTE');
    await w.klick('#g-z'); await w.tipp('Mit Spiegelei und Speck');
    await w.klick('[data-chips="art"] button:has-text("Kleine Portion")');
    await w.klick('#g-p'); await w.tipp('19.00');
    await w.klick('#g-p2'); await w.tipp('24.00');
    await s.waitForTimeout(800);
    await w.klick('#g-ok'); await w.quitt('Gericht hinzugefügt'); await s.waitForTimeout(2400);
  });
  await clip('3-seite', async (s, w) => {
    await s.goto(B + '/studio/#/seite/index.html');
    const f = s.frameLocator('#w-rahmen'); await f.locator('.auftakt__satz[data-e]').first().waitFor(); await s.waitForTimeout(1800);
    const hb = await f.locator('.auftakt__satz[data-e]').first().boundingBox();
    await w.zu(hb.x + 60, hb.y + hb.height / 2); await s.mouse.down(); await s.waitForTimeout(90); await s.mouse.up();
    await s.waitForSelector('#w-schreib'); await s.waitForTimeout(700);
    await w.klick('#w-schreib'); await s.keyboard.press('Meta+A');
    await w.tipp('Landgasthof Ruedihus in Kandersteg. Fünf Stuben, vier Zimmer, ein Haus von 1753.');
    await w.klick('#w-ok'); await w.quitt('Text gespeichert'); await s.waitForTimeout(2400);
  });
  await clip('4-bild', async (s, w) => {
    await s.goto(B + '/studio/#/bilder'); await s.waitForSelector('.bk[data-key="familie"]'); await s.waitForTimeout(1300);
    await w.klick('.bk[data-key="familie"]'); await s.waitForSelector('#f-ablage'); await s.waitForTimeout(700);
    await w.auf('#f-ablage');
    const [fc] = await Promise.all([s.waitForEvent('filechooser'), s.mouse.click(maus.x, maus.y)]); await fc.setFiles(FOTO);
    await s.waitForSelector('#f-ok'); await s.waitForTimeout(1600);
    await w.klick('#f-ok'); await w.quitt('Bild getauscht'); await s.waitForTimeout(2400);
  });
  await clip('5-raus', async (s, w) => {
    await s.goto(B + '/studio/#/uebersicht'); await s.waitForSelector('.leiste'); await s.waitForTimeout(1300);
    await s.waitForSelector('.leiste [data-akt="lade"]', { timeout: 20000 });
    await w.klick(s.locator('.leiste [data-akt="lade"]').first()); await s.waitForSelector('.lade__l li'); await s.waitForTimeout(1600);
    await w.klick(s.locator('.lade__l li [data-akt="sehen"]').first());
    await s.waitForFunction(() => { const d = document.querySelector('#v-entwurf') && document.querySelector('#v-entwurf').contentDocument; const b = d && d.querySelector('.studio-an'); return b && b.style.display === 'block'; }, null, { timeout: 20000 });
    await s.waitForTimeout(2800);
    await w.klick('.vgl [data-akt="zu"]'); await s.waitForTimeout(500);
    await w.klick('.leiste [data-akt="raus"]'); await s.waitForSelector('#f-ok'); await s.waitForTimeout(900);
    await w.klick('#f-notiz'); await w.tipp('Neue Zimmerpreise');
    await w.klick('#f-ok'); await s.waitForSelector('#fenster button:has-text("Fertig")', { timeout: 30000 }); await s.waitForTimeout(2600);
    await w.klick('#fenster button:has-text("Fertig")'); await s.waitForTimeout(600);
    await w.klick('a[href="#/verlauf"]'); await s.waitForTimeout(2800);
  });
  await ctx.close(); await br.close();
})();
