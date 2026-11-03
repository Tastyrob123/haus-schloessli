// Prüf-Chat 17.10.2026: hält der gestaltete Brief, was die Leiste verspricht? Jeder Handgriff, der den Brief neu zeichnet (Foto einfügen,
// Foto entfernen, Linie entfernen, «Zurück auf die Vorlage»), muss nach dem Neuladen noch gelten (Server und Oberfläche).
//   node brief_halt.js <url-des-werkzeugs> [chromium|webkit|firefox] [breite] [höhe]
const path = require('path');
const pw = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const [, , B, MOTOR = 'chromium', BREITE = '1440', HOEHE] = process.argv;
const W = +BREITE, H = +(HOEHE || (W < 700 ? 844 : 900)), HANDY = W < 700;
const sleep = ms => new Promise(r => setTimeout(r, ms));
let gruen = 0, rot = 0;
(async () => {
  const br = await require('./schutz').start(pw, MOTOR); const ctx = await require('./schutz').kontext(br, { viewport: { width: W, height: H }, locale: 'de-CH', hasTouch: HANDY, isMobile: HANDY && MOTOR === 'chromium' });
  await ctx.addInitScript(() => { try { localStorage.setItem('reception-name', 'QA'); localStorage.setItem('rundgang-rh-reception', '1'); } catch (e) { /* */ } });
  const p = await ctx.newPage(); p.setDefaultTimeout(15000); const fehler = []; p.on('pageerror', e => fehler.push(String(e))); p.on('dialog', d => d.accept().catch(() => {}));
  const server = async wer => p.evaluate(async w => (await (await fetch('api/anfragen', { cache: 'no-store' })).json()).anfragen.find(a => a.name.includes(w)).entwurf, wer);
  const oeffne = async wer => { await p.goto('about:blank'); await p.goto(B + '#eingang', { waitUntil: 'load' }); await p.waitForSelector('.re-liste .re-a'); const k = p.locator('.re-liste .re-a', { hasText: wer }).first(); await k.evaluate(e => e.scrollIntoView({ block: 'center' })); await k.click();
    await p.waitForFunction(w => ((document.querySelector('#detail .re-d__n h2') || {}).textContent || '').includes(w), wer); await p.waitForSelector('#brief'); await sleep(700); };
  const klick = async sel => { const l = p.locator(sel).first(); await l.evaluate(e => e.scrollIntoView({ block: 'center' })); await l.click(); };
  const schritt = async (n, fn) => { const f0 = fehler.length; try { const i = await fn(); if (fehler.length > f0) throw new Error('Skriptfehler ' + fehler.slice(f0).join(' | ')); gruen++; console.log('ok  ', n, '·', i); } catch (e) { rot++; console.log('ROT ', n, '·', String(e.message).split('\n')[0].slice(0, 260)); } };
  const warteGesichert = async () => { await sleep(1200); await p.waitForFunction(() => !/Wird gesichert/.test(document.querySelector('#gs-stand')?.textContent || ''), null, { timeout: 10000 }).catch(() => {}); await sleep(500); };
  await schritt('H1 Foto einfügen → neu laden → Foto noch da', async () => {
    await oeffne('Huber'); const n0 = (await server('Huber')).gestalt?._bilder?.length || 0; await klick('.gs-werk [data-w="foto"]'); await p.waitForSelector('#fenster:not([hidden]) .gs-fotos [data-foto]'); await klick('#fenster .gs-fotos [data-foto]'); await warteGesichert();
    const s = await server('Huber'); await oeffne('Huber'); const dom = await p.locator('#brief [data-b^="bild"]').count(); const n1 = s.gestalt?._bilder?.length || 0;
    if (n1 !== n0 + 1 || dom !== n1) throw new Error(`Server ${n0} → ${n1} Fotos, nach Neuladen ${dom} im Brief`); return `${n0} → ${n1}, nach Neuladen ${dom}`;
  });
  await schritt('H2 Foto entfernen → neu laden → Foto weg', async () => {
    await oeffne('Huber'); const n0 = await p.locator('#brief [data-b^="bild"]').count(); if (!n0) throw new Error('kein Foto zum Entfernen (H1 rot)');
    await klick('#brief [data-b^="bild"]'); await sleep(300); await klick('.gs-werk [data-g="weg"]'); await warteGesichert();
    const s = await server('Huber'); await oeffne('Huber'); const dom = await p.locator('#brief [data-b^="bild"]').count(); const n1 = s.gestalt?._bilder?.length || 0;
    if (n1 !== n0 - 1 || dom !== n1) throw new Error(`Server ${n0} → ${n1}, nach Neuladen ${dom} im Brief`); return `${n0} → ${n1}, nach Neuladen ${dom}`;
  });
  await schritt('H3 Linie entfernen → neu laden → Linie weg', async () => {
    await oeffne('Ryser'); const n0 = await p.locator('#brief .gs--linie:visible').count(); await klick('#brief .gs--linie'); await sleep(300); await klick('.gs-werk [data-g="weg"]'); await warteGesichert();
    const g = JSON.stringify((await server('Ryser')).gestalt || {}); await oeffne('Ryser'); const n1 = await p.locator('#brief .gs--linie:visible').count();
    if (!/"aus":true/.test(g) || n1 !== n0 - 1) throw new Error(`Server ${/"aus":true/.test(g) ? 'aus' : 'ohne aus'}, Linien ${n0} → ${n1} nach Neuladen`); return `Linien ${n0} → ${n1}`;
  });
  await schritt('H4 Text ändern, dann «Zurück auf die Vorlage» → neu laden → Vorlage gilt', async () => {
    await oeffne('Wenger'); const v = (await server('Wenger')).text; const el = p.locator('#brief .gs--p').nth(1); await el.evaluate(e => e.scrollIntoView({ block: 'center' }));
    if (HANDY) await el.evaluate(e => e.dispatchEvent(new MouseEvent('dblclick', { bubbles: true }))); else await el.dblclick(); await sleep(300); await p.keyboard.press('End'); await p.keyboard.type(' QAVORLAGE'); await p.mouse.click(3, 200); await warteGesichert();
    const zw = (await server('Wenger')).text; if (!/QAVORLAGE/.test(zw)) throw new Error('Änderung nicht gesichert');
    await klick('.gs-werk [data-w="vorlage"]'); await p.waitForSelector('#fenster:not([hidden]) #f-los'); await klick('#fenster #f-los'); await warteGesichert();
    const s = (await server('Wenger')).text; await oeffne('Wenger'); const dom = (await p.locator('#brief').innerText());
    if (/QAVORLAGE/.test(s) || /QAVORLAGE/.test(dom) || s !== v) throw new Error(`Server ${/QAVORLAGE/.test(s) ? 'mit' : 'ohne'} Änderung, nach Neuladen ${/QAVORLAGE/.test(dom) ? 'mit' : 'ohne'}`); return 'Vorlage gesichert';
  });
  console.log(`brief_halt ${MOTOR} ${W}x${H}: ${gruen} grün, ${rot} rot`); await br.close();
})().catch(e => { console.log('ABBRUCH', e.message); process.exit(2); });
