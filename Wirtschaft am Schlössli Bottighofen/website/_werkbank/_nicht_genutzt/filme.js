// Prüft, ob jeder Film der Werkbank wirklich läuft: node _werkbank/filme.js [Adresse]   (Standard http://127.0.0.1:8917/werkbank/)
//   Öffnet die Werkbank in Chrome- und Safari-Technik, sammelt jede Filmdatei (Studio-Schritte, Rezeption), lädt sie, spielt sie an
//   und meldet Dauer, Bildgrösse und ob die Zeit nach 1,5 s weiterläuft. Dazu der Zwei-Byte-Abruf (Range), den Safari braucht.
const path = require('path'), http = require('http'), https = require('https');
const PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const URL_ = process.argv[2] || 'http://127.0.0.1:8917/werkbank/';
const range = u => new Promise(r => { const m = u.startsWith('https') ? https : http; const q = m.request(u, { method: 'GET', headers: { Range: 'bytes=0-1' } }, a => { r({ status: a.statusCode, typ: a.headers['content-type'], laenge: a.headers['content-range'] || a.headers['content-length'] }); a.resume(); }); q.on('error', e => r({ status: 'FEHLER ' + e.message })); q.end(); });
(async () => {
  let schlecht = 0;
  for (const art of ['chromium', 'webkit']) {
    const b = await PW[art].launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
    await p.goto(URL_, { waitUntil: 'load' }); await p.waitForTimeout(1500);
    const filme = await p.evaluate(() => { const s = new Set(); document.querySelectorAll('video[src]').forEach(v => s.add(v.getAttribute('src'))); document.querySelectorAll('[data-film]').forEach(k => s.add(k.getAttribute('data-film'))); return [...s]; });
    for (const f of filme) {
      const u = new URL(f, URL_).href;
      const r = await p.evaluate(async src => {
        const v = document.createElement('video'); v.muted = true; v.playsInline = true; v.preload = 'auto'; v.src = src; document.body.appendChild(v);
        const warte = ms => new Promise(x => setTimeout(x, ms));
        try { await v.play(); } catch (e) { return { fehler: 'play: ' + e.message }; }
        await warte(1500);
        const aus = { dauer: +v.duration.toFixed(1), b: v.videoWidth, h: v.videoHeight, zeit: +v.currentTime.toFixed(2), bereit: v.readyState, fehler: v.error ? v.error.code : null };
        v.pause(); v.remove(); return aus;
      }, u);
      const rg = art === 'chromium' ? await range(u) : null;
      const ok = !r.fehler && r.zeit > 0.5 && r.b > 0;
      if (!ok) schlecht++;
      console.log((ok ? 'ok   ' : 'FEHL ') + art.padEnd(9), f.padEnd(26), JSON.stringify(r), rg ? ` range ${rg.status} ${rg.typ} ${rg.laenge}` : '');
    }
    await b.close();
  }
  console.log(schlecht ? schlecht + ' Filme laufen nicht' : 'alle Filme laufen');
  process.exit(schlecht ? 1 : 0);
})();
