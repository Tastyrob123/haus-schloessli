/* Kurzfilme der Führung (hilfe/schritt-1…9.mp4 + .jpg) und Demo-Video (hilfe/demo.mp4, demo-poster.jpg, kapitel.json), aufgenommen an der Hausdruckerei
   der Wirtschaft am Schlössli (Server :9287, Probe ohne KI). Playwright nimmt WebM auf, ffmpeg schneidet um das Ziel und wandelt in H.264.
   NODE_PATH=/opt/node-tools/node_modules node _bau/filme.js */
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const H = path.join(__dirname, '..', 'hilfe'), TMP = fs.mkdtempSync('/tmp/sl-filme-');
const URL = 'http://127.0.0.1:9287/_werkzeuge/imprimerie/';
const W = 1440, HH = 900;
async function seite(b, video) {
  const ctx = await b.newContext({ viewport: { width: W, height: HH }, recordVideo: video ? { dir: TMP, size: { width: W, height: HH } } : undefined });
  await ctx.addInitScript(() => { try { localStorage.setItem('ds-schloessli-willkommen', '1'); } catch (e) {} });
  const p = await ctx.newPage(); await p.goto(URL, { waitUntil: 'load' });
  await p.waitForFunction(() => window.DS && DS.M && window.DSStudio, null, { timeout: 30000 }); await p.waitForTimeout(1200);
  return { ctx, p };
}
const oeffne = p => p.evaluate(() => { const x = DSKATALOG.ABTEILUNGEN.find(a => a.k === 'haus').vorlagen[0]; const d = DS.dokument(DS.M, { name: x.n, format: x.format, seiten: [{ vorlage: x.vorlage, ton: x.ton, inhalt: x.inhalt, stil: x.stil }] }); DSStudio.oeffne(d); if (window.DSStart && DSStart.offen()) DSStart.zu(); });
const ffm = (a) => execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...a]);
async function film(b, name, ziel, tun, vorher) {
  const { ctx, p } = await seite(b, true);
  await oeffne(p); await p.waitForTimeout(1500); if (vorher) await vorher(p);
  const t0 = Date.now(); const r = await p.locator(ziel).first().boundingBox();
  await tun(p); await p.waitForTimeout(800);
  const v = p.video(); await ctx.close(); const roh = await v.path();
  const cw = 880, ch = 550; let x = Math.round((r ? r.x + r.width / 2 : W / 2) - cw / 2), y = Math.round((r ? r.y + r.height / 2 : HH / 2) - ch / 2);
  x = Math.max(0, Math.min(W - cw, x)); y = Math.max(0, Math.min(HH - ch, y));
  const vor = ((Date.now() - t0) / 1000);
  ffm(['-i', roh, '-ss', '1.6', '-vf', `crop=${cw}:${ch}:${x}:${y},fps=25`, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '28', '-movflags', '+faststart', '-an', path.join(H, name + '.mp4')]);
  ffm(['-i', path.join(H, name + '.mp4'), '-ss', String(Math.max(0, vor - 1.2)), '-frames:v', '1', '-q:v', '4', path.join(H, name + '.jpg')]);
  console.log(name, 'fertig');
}
(async () => {
  const b = await chromium.launch();
  const tippe = async (p, sel, t) => { await p.click(sel); for (const ch of t) { await p.keyboard.type(ch); await p.waitForTimeout(45); } };
  await film(b, 'schritt-1', '#auftrag', async p => { await tippe(p, '#auftrag', 'Ein Aushang zu den Betriebsferien im Winter'); await p.waitForTimeout(900); }, p => p.click('.reiter [data-tab="entwerfen"]'));
  await film(b, 'schritt-2', '#btnEntwerfen', async p => { await p.fill('#auftrag', 'Ein Aushang zu den Betriebsferien im Winter'); await p.click('#btnEntwerfen'); await p.waitForTimeout(5000); }, p => p.click('.reiter [data-tab="entwerfen"]'));
  await film(b, 'schritt-3', '#wirt', async p => { const t = p.locator('#wirt .el').filter({ hasText: 'Direkt im Hafen' }).first(); const r = await t.boundingBox(); if (r) { await p.mouse.move(r.x + r.width / 2, r.y + r.height / 2, { steps: 12 }); await p.mouse.down(); await p.mouse.move(r.x + r.width / 2 - 30, r.y + r.height / 2 + 24, { steps: 20 }); await p.mouse.up(); await p.waitForTimeout(600); await p.mouse.move(r.x + r.width / 2 + 30, r.y + r.height / 2 - 24, { steps: 20 }); } await p.waitForTimeout(1200); });
  await film(b, 'schritt-4', '#rechts', async p => { const t = p.locator('#wirt .el').filter({ hasText: 'Donnerstag' }).first(); await t.click().catch(() => {}); await p.waitForTimeout(1500); await p.mouse.wheel(0, 300); await p.waitForTimeout(1500); });
  await film(b, 'schritt-5', '#werkzeug', async p => { await p.click('[data-neu="titel"]'); await p.waitForTimeout(1500); await p.click('[data-neu="zeichen"]'); await p.waitForTimeout(1500); });
  await film(b, 'schritt-6', '.reiter', async p => { await p.click('.reiter [data-tab="fotos"]'); await p.waitForTimeout(1600); await p.click('.reiter [data-tab="vorlagen"]'); await p.waitForTimeout(1600); await p.click('.reiter [data-tab="ablage"]'); await p.waitForTimeout(1400); });
  await film(b, 'schritt-7', '#btnZurueck', async p => { await p.click('[data-neu="titel"]'); await p.waitForTimeout(1200); await p.click('#btnZurueck'); await p.waitForTimeout(1500); });
  await film(b, 'schritt-8', '#btnPruefen', async p => { await p.click('#btnPruefen'); await p.waitForTimeout(2500); await p.keyboard.press('Escape'); await p.waitForTimeout(500); });
  await film(b, 'schritt-9', '#btnSpeichern', async p => { await p.hover('#btnSpeichern'); await p.waitForTimeout(800); await p.click('#btnSpeichern'); await p.waitForTimeout(2500); await p.keyboard.press('Escape'); });
  /* Demo: Sagen, Anpassen, Format, Drucken */
  const { ctx, p } = await seite(b, true); const k = []; const t0 = Date.now(); const mark = t => k.push({ titel: t, t: +((Date.now() - t0) / 1000).toFixed(1) });
  await p.waitForTimeout(2500);
  await p.click('[data-ansicht="abteilungen"]').catch(() => {}); await p.waitForTimeout(2500);
  mark('Sagen'); await oeffne(p); await p.waitForTimeout(1500);
  await p.click('.reiter [data-tab="entwerfen"]').catch(() => {}); await tippe(p, '#auftrag', 'Ein Aushang zu den Betriebsferien'); await p.waitForTimeout(800); await p.click('#btnEntwerfen').catch(() => {}); await p.waitForTimeout(5500);
  await oeffne(p); await p.waitForTimeout(1500);
  mark('Anpassen'); const t = p.locator('#wirt .el').filter({ hasText: 'Direkt im Hafen' }).first(); await t.dblclick().catch(() => {}); await p.waitForTimeout(600); await p.keyboard.press('Control+A'); await p.keyboard.type('Lunch am See', { delay: 90 }); await p.mouse.click(1300, 860); await p.waitForTimeout(1500);
  await p.click('.reiter [data-tab="fotos"]').catch(() => {}); await p.waitForTimeout(2500);
  mark('Format'); await p.click('.reiter [data-tab="vorlagen"]').catch(() => {}); await p.waitForTimeout(3000);
  mark('Drucken'); await p.click('#btnPruefen').catch(() => {}); await p.waitForTimeout(2500); await p.keyboard.press('Escape'); await p.click('#btnSpeichern').catch(() => {}); await p.waitForTimeout(3000);
  const v = p.video(); await ctx.close(); const roh = await v.path();
  ffm(['-i', roh, '-vf', 'scale=1280:800,fps=25', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '26', '-movflags', '+faststart', '-an', path.join(H, 'demo.mp4')]);
  ffm(['-i', path.join(H, 'demo.mp4'), '-ss', String(k[1] ? k[1].t + 2 : 6), '-frames:v', '1', '-q:v', '3', path.join(H, 'demo-poster.jpg')]);
  fs.writeFileSync(path.join(H, 'kapitel.json'), JSON.stringify(k));
  console.log('demo fertig', JSON.stringify(k));
  await b.close(); fs.rmSync(TMP, { recursive: true, force: true });
})();
