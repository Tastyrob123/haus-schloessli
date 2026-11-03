// Das Hausbuch · Wirtschaft am Schlössli · die Online-Fassung in der Probe bedienen (online_probe.py muss laufen): Laden aller Ansichten unter /werkzeuge/livre/
// mit der Sicherheitsregel für Skripte (keine eingebetteten Skripte), Stand-Weg /marke/livre.json, Downloads in Website-Grösse, Prüfung mit Probe-Antwort,
// Umleitungen /_werkzeuge/livre/ und /marke/api/.   BASIS=http://127.0.0.1:9049/ node _werkzeuge/livre/pruefung/online_pruef.js [chromium|webkit|firefox]
const path = require('path'), fs = require('fs');
const pw = require(path.join(process.env.HOME, 'Aussen-Pruefung/node_modules/playwright'));
const BASIS = process.env.BASIS || 'http://127.0.0.1:9049/', motor = process.argv[2] || 'chromium';
const erg = []; const Z = (t, ok, m = '') => { erg.push({ t, ok: !!ok, m: String(m) }); console.log((ok ? '✓' : '✗') + ' ' + t + (m !== '' ? ' · ' + String(m).slice(0, 180) : '')); };
(async () => {
  const b = await pw[motor].launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, acceptDownloads: true });
  await ctx.addInitScript(() => { try { localStorage.setItem('rundgang-sl-livre', '1'); } catch (e) {} });
  const p = await ctx.newPage(); const fehler = [];
  p.on('pageerror', e => fehler.push('JS ' + e.message)); p.on('console', m => { if (m.type() === "error" && !/status of 400/.test(m.text())) fehler.push("K " + m.text()); });
  p.on('response', r => { if (r.status() >= 400 && !/maison|imprimerie|favicon|marke\/api\/pruefen/.test(r.url())) fehler.push(r.status() + ' ' + r.url()); });
  const st = async u => p.evaluate(async u => { const r = await fetch(u, { cache: 'no-store' }); const bl = await r.blob(); return [r.status, bl.size, r.headers.get('content-disposition') || '', r.headers.get('content-type') || '']; }, u);
  for (const a of ['start', 'bilder', 'dateien', 'pruefung']) {
    await p.goto('about:blank'); await p.goto(BASIS + 'werkzeuge/livre/#' + a, { waitUntil: 'load' }); await p.waitForSelector('#ansicht .li-hero', { timeout: 20000 }); await p.waitForTimeout(1200);
  }
  Z('Vier Ansichten laden online (Sicherheitsregel script-src self), keine Skript- oder Konsolenfehler', fehler.length === 0, fehler.slice(0, 3).join(' | '));
  const s = await st(BASIS + 'werkzeuge/livre/api/stand'); const sj = await p.evaluate(async u => (await fetch(u)).json(), BASIS + 'werkzeuge/livre/api/stand');
  Z('api/stand online: Zahlen, nur Website-Grösse, Prüfung ohne Claude', s[0] === 200 && sj.fotos === 62 && sj.nur_website && sj.pruefung_ki === false && sj.ohne_original.length === 62, JSON.stringify({ fotos: sj.fotos, ki: sj.ki, dateien: sj.dateien }));
  const m = await p.evaluate(async u => (await fetch(u)).json(), BASIS + 'marke/livre.json');
  Z('Stand-Weg für Die Stube /marke/livre.json → stand:{fotos, ki, dateien}', m.stand && m.stand.fotos === 62 && m.stand.ki === 0 && m.stand.dateien > 30, JSON.stringify(m.stand));
  const um = await st(BASIS + '_werkzeuge/livre/buch.html');
  Z('Umleitung /_werkzeuge/livre/ → /werkzeuge/livre/', um[0] === 200);
  const dl = {}; for (const [k, f] of [['platanen', 'web'], ['platanen', 'druck'], ['gast-annan', 'instagram'], ['haus-doldenhorn', 'story'], ['film-zimmer', 'druck']]) dl[k + ' ' + f] = await st(BASIS + 'werkzeuge/livre/api/bild?k=' + encodeURIComponent(k) + '&f=' + f);
  const okDl = Object.values(dl).every(x => x[0] === 200 && /jpeg/.test(x[3])) && /websitegroesse-druck/.test(dl['platanen druck'][2]) && /film-zimmer-websitegroesse-druck-1920x1080/.test(dl['film-zimmer druck'][2]) && /1080x1350/.test(dl['gast-annan instagram'][2]);
  Z('Downloads online aus der Website (auch Gäste, Schwesterhäuser, Film), Druck heisst «websitegroesse»', okDl, Object.entries(dl).map(([k, v]) => k + ' ' + v[0] + ' ' + (v[2].match(/filename="([^"]+)"/) || [])[1]).join(' | '));
  await p.goto(BASIS + 'werkzeuge/livre/#bilder'); await p.waitForSelector('#li-raster .li-f'); await p.waitForTimeout(800);
  const k = p.locator('#li-raster .li-f[data-k="platanen"]'); await k.evaluate(e => e.scrollIntoView({ block: 'center' })); await k.click(); await p.waitForSelector('#fenster .li-det'); await p.waitForTimeout(600);
  Z('Fenster sagt online beim Druck «in Website-Grösse»', /Website-Grösse/.test(await p.locator('.li-gr[data-g="druck"]').innerText()));
  await p.keyboard.press('Escape');
  await p.goto(BASIS + 'werkzeuge/livre/#pruefung'); await p.waitForSelector('#li-waehle'); await p.waitForTimeout(800);
  await p.locator('#li-datei').setInputFiles({ name: 'online.png', mimeType: 'image/png', buffer: Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAAFUlEQVR4nGPklndgwA2Y8MgxjFxpAIylAH608qaWAAAAAElFTkSuQmCC', 'base64') }); await p.waitForTimeout(600);
  await p.locator('#li-los').click(); await p.waitForFunction(() => !document.querySelector('#li-pr .li-lauf'), null, { timeout: 60000 }); await p.waitForTimeout(800);
  Z('Prüfung online mit Probe-Antwort, beschriftet', (await p.locator('#li-pr .li-hinweis--probe').count()) === 1 && (await p.locator('#li-pr .li-pk').count()) >= 4);
  const mp = await p.evaluate(async u => { const r = await fetch(u, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' }); return [r.status, (await r.json()).fehler]; }, BASIS + 'marke/api/pruefen');
  Z('Umleitung /marke/api/pruefen (für Die Werkstatt) erreicht die Funktion', mp[0] === 400 && /DATEI/.test(mp[1]), mp.join(' '));
  Z('Am Ende keine Fehler', fehler.length === 0, fehler.slice(0, 3).join(' | '));
  await b.close();
  fs.mkdirSync(path.join(__dirname, 'ergebnisse'), { recursive: true });
  fs.writeFileSync(path.join(__dirname, 'ergebnisse', `online-${motor}.json`), JSON.stringify(erg, null, 1));
  console.log(`Summe online ${motor}: ${erg.filter(x => x.ok).length}/${erg.length}`);
})().catch(e => { console.log('ABBRUCH', String(e.stack || e).slice(0, 500)); process.exit(2); });
