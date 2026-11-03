/* Vorschaubilder der Galerien vorab rechnen (haeuser/schloessli/vorschau-dok/, über api/vorschau des Servers): alle Ansichten öffnen, ganz durchscrollen,
   warten, bis die Schlange der Werkstatt leer ist. Nach jeder Änderung an Satz, Vorlagen, Druck oder dokumente.js neu laufen lassen.
   NODE_PATH=/opt/node-tools/node_modules node _bau/vorschaubilder.js */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.addInitScript(() => { try { localStorage.setItem('ds-schloessli-willkommen', '1'); } catch (e) {} });
  await p.goto('http://127.0.0.1:9287/_werkzeuge/imprimerie/', { waitUntil: 'load' });
  await p.waitForFunction(() => window.DS && DS.M && window.DSStudio && DS.VB, null, { timeout: 30000 }); await p.waitForTimeout(1500);
  const leer = async () => { for (let n = 0; n < 600; n++) { const o = await p.evaluate(() => DS.VB.offen || 0); if (!o) { await p.waitForTimeout(1500); if (!(await p.evaluate(() => DS.VB.offen || 0))) return; } await p.waitForTimeout(700); } };
  const runter = async () => { for (let i = 0; i < 40; i++) { await p.evaluate(() => { const h = document.querySelector('#start .ms-haupt') || document.scrollingElement; h.scrollBy(0, 700); }); await p.waitForTimeout(250); } await p.waitForTimeout(800); };
  const ansicht = async a => { await p.click(`[data-ansicht="${a}"]`).catch(() => {}); await p.waitForTimeout(1500); await runter(); await leer(); };
  for (const a of ['start', 'events', 'abteilungen', 'hinweise', 'newsletter', 'meine', 'neu']) await ansicht(a);
  await p.click('#vbAlle button, [data-st="alle"]').catch(() => {}); await p.waitForTimeout(2000); await runter(); await leer();
  const zahl = async sel => p.evaluate(s => document.querySelectorAll(s).length, sel);
  for (const typ of ['event', 'abteilung']) {
    await p.click(`[data-ansicht="${typ === 'event' ? 'events' : 'abteilungen'}"]`).catch(() => {}); await p.waitForTimeout(1200);
    const n = await zahl(`[data-${typ}]`);
    for (let i = 0; i < n; i++) { await p.click(`[data-ansicht="${typ === 'event' ? 'events' : 'abteilungen'}"]`).catch(() => {}); await p.waitForTimeout(900); const l = await p.$$(`#start [data-${typ}]`); const sichtbar = []; for (const e of l) if (await e.isVisible()) sichtbar.push(e); if (!sichtbar[i]) break; await sichtbar[i].click(); await p.waitForTimeout(1500); await runter(); await leer(); }
  }
  await p.click('[data-ansicht="neu"]').catch(() => {}); await p.waitForTimeout(1200);
  const arten = await p.$$eval('#arten [data-art]', l => l.map(e => e.dataset.art));
  for (const a of arten) { await p.click('[data-ansicht="neu"]').catch(() => {}); await p.waitForTimeout(800); await p.click(`#arten [data-art="${a}"]`).catch(() => {}); await p.waitForTimeout(1500); await runter(); await leer(); }
  console.log('Vorschaubilder:', await p.evaluate(() => Object.keys(DS.VB.index).length));
  await b.close();
})();
