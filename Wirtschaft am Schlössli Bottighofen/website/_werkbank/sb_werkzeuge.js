// Bildschirme der sieben Werkzeuge für die Werkbank der Wirtschaft am Schlössli (19.10.2026). Adresse aus dem Paket jedes Werkzeug-Chats
// (_kette/11-werkbank/werkzeuge/<teil>/stand.json, nur «liegt vor» oder «bestätigt»).   node _werkbank/sb_werkzeuge.js [schlüssel …] [--alle]
//   → ansichten/Werkzeuge/<schlüssel>.jpg (Rechner 1440 × 900, doppelte Dichte), <schlüssel>-2.jpg (eine Bildschirmhöhe weiter), ansichten/Werkzeuge-Handy/<schlüssel>.jpg (390 × 844)
// Nur ansehen: nichts wird gespeichert, nichts abgeschickt. --alle nimmt auch Werkzeuge, die noch «läuft» melden (Probebild, nie für die Meldung).
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const HIER = __dirname, PROJEKT = path.join(HIER, '..', '..');
const TEIL = { maison: 'zentrale', bureau: 'website', carte: 'karten', reception: 'gaeste', livre: 'marke', registre: 'besuche', imprimerie: 'druck' };
const arg = process.argv.slice(2), alle = arg.includes('--alle'), nur = arg.filter(a => !a.startsWith('--'));
(async () => {
  for (const d of ['Werkzeuge', 'Werkzeuge-Handy']) fs.mkdirSync(path.join(HIER, 'ansichten', d), { recursive: true });
  const b = await chromium.launch({ headless: true });
  for (const [k, t] of Object.entries(TEIL)) {
    if (nur.length && !nur.includes(k)) continue;
    const p0 = path.join(PROJEKT, '_kette/11-werkbank/werkzeuge', t, 'stand.json');
    const st = fs.existsSync(p0) ? JSON.parse(fs.readFileSync(p0, 'utf8')) : {};
    // Robert 20.10.2026 «Da fehlt ein Tool»: alle sieben stehen immer in der Werkbank; ohne gemeldete Adresse der Stand vom Prüfserver des Werkzeug-Chats (nur ansehen)
    const PRUEF = { druck: 'http://127.0.0.1:9053/_werkzeuge/imprimerie/' };
    if (!st.adresse && PRUEF[t]) { st.adresse = PRUEF[t]; st.zustand = st.zustand || 'läuft'; }
    if (!st.adresse || (!alle && !['liegt vor', 'bestätigt'].includes(st.zustand))) { console.log('wartet', k, st.zustand || ''); continue; }
    for (const [art, vp, dsf] of [['Werkzeuge', { width: 1440, height: 900 }, 2], ['Werkzeuge-Handy', { width: 390, height: 844 }, 2]]) {
      const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: dsf, ...(vp.width < 700 ? { isMobile: true, hasTouch: true } : {}) });
      const p = await ctx.newPage();
      await p.addInitScript(() => { try { for (const h of ['schloessli']) localStorage.setItem('ds-' + h + '-willkommen', '1'); if (!localStorage.getItem('lc-wer')) { localStorage.setItem('lc-wer', 'Christian Kuchler'); localStorage.setItem('lc-rolle', 'direktion'); } } catch (e) {} });
      try {
        await p.goto(st.adresse, { waitUntil: 'load', timeout: 30000 }); await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(3500);
        await p.screenshot({ path: path.join(HIER, 'ansichten', art, k + '.jpg'), quality: 88 });
        if (art === 'Werkzeuge') { await p.evaluate(() => scrollTo(0, innerHeight * .9)); await p.waitForTimeout(1500); await p.screenshot({ path: path.join(HIER, 'ansichten', art, k + '-2.jpg'), quality: 88 }); }
        console.log('aufgenommen', k, art, st.adresse);
      } catch (e) { console.log('fehlgeschlagen', k, art, String(e).slice(0, 120)); }
      await ctx.close();
    }
  }
  await b.close();
})();
