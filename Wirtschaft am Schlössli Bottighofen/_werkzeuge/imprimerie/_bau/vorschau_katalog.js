/* Vorschaubilder für jedes Stück des Katalogs (Abteilungen, Hinweise, Newsletter, Anlässe), ohne Klicken: gleicher Schlüssel wie start.js kvBlatt.
   NODE_PATH=/opt/node-tools/node_modules node _bau/vorschau_katalog.js */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.addInitScript(() => { try { localStorage.setItem('ds-schloessli-willkommen', '1'); } catch (e) {} });
  await p.goto('http://127.0.0.1:9287/_werkzeuge/imprimerie/', { waitUntil: 'load' });
  await p.waitForFunction(() => window.DS && DS.M && DS.VB && DS.VB.geladen && window.DSStudio, null, { timeout: 30000 });
  const n = await p.evaluate(async () => {
    const K = window.DSKATALOG, alle = [].concat(...K.ABTEILUNGEN.map(a => a.vorlagen), K.HINWEISE, K.NEWSLETTER, ...K.ANLAESSE.map(a => K.motive(a)));
    let neu = 0;
    for (const x of alle) {
      const fkey = DS.FORMATE[x.format] ? x.format : 'a5h', f = DS.FORMATE[fkey];
      const seiten = [{ vorlage: x.vorlage, ton: x.ton, inhalt: x.inhalt, stil: x.stil || null }];
      if (x.rueck) seiten.push({ vorlage: x.rueck.vorlage, ton: x.ton, inhalt: x.rueck.inhalt, stil: null });
      for (const s of seiten) {
        const vs = { vorlage: s.vorlage, ton: s.ton, inhalt: s.inhalt, stil: s.stil, foto: '' };
        const k = DS.VB.schluessel(fkey, vs);
        if (DS.VB.index[k]) continue;
        const doc = { format: { b: f.b, h: f.h }, formatKey: fkey, seiten: [DS.setze(DS.M, fkey, s.vorlage, s.ton, s.inhalt, s.stil)] };
        const blob = await DS.png(DS.M, doc, 0, DS.VB.px(f));
        const png = await new Promise(ok => { const r = new FileReader(); r.onload = () => ok(r.result); r.readAsDataURL(blob); });
        const a = await fetch('api/vorschau', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ k, k2: DS.VB.inhalt(fkey, vs), png }) });
        if (a.ok) { const d = await a.json(); DS.VB.index[k] = d.farbe || '#fff'; neu++; }
      }
    }
    return neu;
  });
  console.log('neu:', n);
  await b.close();
})();
