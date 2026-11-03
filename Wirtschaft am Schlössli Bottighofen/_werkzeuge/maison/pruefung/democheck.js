#!/usr/bin/env node
/* Demo-Check der Stube (21.10.2026): jeder Link, jede Kachel, Sprungmarken, Rundgang, Stand-Zeilen, Website, Weg aus der Werkbank. node pruefung/democheck.js chromium|webkit */
const path = require('path'), os = require('os'), fs = require('fs');
module.paths.push(path.join(os.homedir(), 'Aussen-Pruefung', 'node_modules'));
const pw = require('playwright');
const MOTOR = process.argv[2] || 'chromium', BASIS = 'http://127.0.0.1:8987/_werkzeuge/maison/';
const BILD = path.join(os.homedir(), 'Desktop/Website-Projekte/_Oberchef/zeigen/schloessli/democheck/maison');
const erg = []; const ok = (w, n, g, i) => erg.push({ w, n, gut: !!g, info: i === undefined ? '' : String(i).slice(0, 400) });
(async () => {
  const browser = await pw[MOTOR].launch({ headless: true });
  for (const [B, H] of [[1440, 900], [390, 844]]) {
    const w = `${MOTOR} ${B}`, hand = B < 1000;
    const neu = async (q = '') => {
      const ctx = await browser.newContext({ viewport: { width: B, height: H }, locale: 'de-CH', timezoneId: 'Europe/Zurich', hasTouch: hand, isMobile: hand && MOTOR === 'chromium' });
      const page = await ctx.newPage(); const f = [];
      page.on('console', m => { if (m.type() === 'error') f.push(page.url() + ' ' + m.text()); });
      page.on('pageerror', e => f.push(page.url() + ' ' + e));
      await ctx.route(/^(mailto|tel):/, r => { f.push('mailto/tel ' + r.request().url()); r.abort(); });
      return { ctx, page, f };
    };
    // A Laden, Bilder, Stand-Zeilen, alle Links
    {
      const { ctx, page, f } = await neu();
      await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(2500);
      await page.screenshot({ path: path.join(BILD, `${MOTOR}-${B}-1-empfang.png`) });
      const hoch = await page.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < hoch; y += 400) { await page.evaluate(v => scrollTo(0, v), y); await page.waitForTimeout(120); }
      await page.waitForTimeout(1500);
      if (MOTOR === 'webkit' || B === 1440) await page.screenshot({ path: path.join(BILD, `${MOTOR}-${B}-0-ganz.png`), fullPage: true });
      const stand = await page.evaluate(() => [...document.querySelectorAll('[data-stand]')].map(x => x.getAttribute('data-stand') + ': ' + x.textContent.trim()));
      ok(w, 'Stand-Zeilen gefüllt', stand.every(s => !/: $/.test(s) && !/undefined|NaN|null/.test(s)), stand.join(' | '));
      const links = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => ({ h: a.href, t: (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0, 50), sicht: !!(a.offsetWidth || a.offsetHeight) })));
      const gesehen = new Set();
      for (const l of links) {
        if (/#/.test(l.h) && l.h.split('#')[0] === BASIS) { const id = l.h.split('#')[1]; ok(w, `Sprungziel #${id} da`, !id || await page.$('#' + id), l.t); continue; }
        if (/^(mailto|tel):/.test(l.h)) { ok(w, 'kein mailto/tel', false, l.h); continue; }
        if (gesehen.has(l.h)) continue; gesehen.add(l.h);
        const r = await ctx.request.get(l.h).catch(e => ({ status: () => String(e) }));
        ok(w, `Link «${l.t}» antwortet`, r.status() === 200, r.status() + ' ' + l.h);
      }
      ok(w, 'Konsole leer beim Laden', !f.length, f.join(' | '));
      await ctx.close();
    }
    // B Jede Kachel des Empfangs öffnen (Klick bzw. Tippen), Ziel lädt ohne Fehler
    for (let i = 0; i < 6; i++) {
      const { ctx, page, f } = await neu();
      await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(1600);
      const a = (await page.$$('.hz-z a'))[i];
      const href = await a.evaluate(x => x.href); const tgt = await a.evaluate(x => x.target);
      const pop = tgt === '_blank' ? ctx.waitForEvent('page', { timeout: 8000 }) : null;
      if (hand) await a.tap(); else await a.click();
      let ziel = page; if (pop) { ziel = await pop.catch(() => null); }
      if (ziel) { ziel.on('pageerror', e => f.push('ZIEL ' + e)); await ziel.waitForLoadState('load').catch(() => { }); await ziel.waitForTimeout(1500); }
      const titel = ziel ? await ziel.title().catch(() => '') : '';
      ok(w, `Kachel ${i + 1} öffnet ${href}`, ziel && ziel.url().split(/[?#]/)[0] === href.split(/[?#]/)[0], (ziel && ziel.url()) + ' · ' + titel + ' · ' + tgt);
      if (ziel && i === 0) await ziel.screenshot({ path: path.join(BILD, `${MOTOR}-${B}-kachel-ziel-${i + 1}.png`) }).catch(() => { });
      ok(w, `Kachel ${i + 1}: keine Skriptfehler`, !f.filter(x => / ZIEL |pageerror|Error/.test(x)).length, f.join(' | '));
      await ctx.close();
    }
    // C Leiste: Sprungmarken (nur breit) und Eck-Knöpfe
    {
      const { ctx, page, f } = await neu();
      await page.goto(BASIS, { waitUntil: 'load' }); await page.waitForTimeout(1500);
      const marken = await page.$$eval('.m-oben a[href^="#"]', xs => xs.filter(x => x.offsetWidth).map(x => x.getAttribute('href')));
      ok(w, 'Leiste: sichtbare Sprungmarken', true, marken.join(' '));
      for (const m of marken) {
        await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(500);
        await page.click(`.m-oben a[href="${m}"]`); await page.waitForTimeout(1300);
        const lage = await page.evaluate(id => { const e = document.querySelector(id); return e ? Math.round(e.getBoundingClientRect().top) : null; }, m);
        ok(w, `Leiste ${m} springt hin`, lage !== null && (m === '#fuss' ? lage < H : lage > -60 && lage < H * 0.6), lage);
      }
      ok(w, 'Leiste ohne Fehler', !f.length, f.join(' | '));
      await ctx.close();
    }
    // D Rundgang erzwungen: fünf Schritte durchklicken
    {
      const { ctx, page, f } = await neu();
      await page.addInitScript(() => Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false }));
      await page.goto(BASIS, { waitUntil: 'load' });
      const schild = await page.waitForSelector('.rdg-schild .rdg-los', { timeout: 12000 }).catch(() => null);
      ok(w, 'Schild «Kurzer Rundgang» erscheint', !!schild);
      if (schild) { await page.screenshot({ path: path.join(BILD, `${MOTOR}-${B}-rundgang-0-schild.png`) }); if (hand) await schild.tap(); else await schild.click(); }
      await page.waitForSelector('.rdg-karte', { timeout: 6000 }).catch(() => null); await page.waitForTimeout(900);
      let n = 0;
      for (; n < 7; n++) {
        const k = await page.$('.rdg-karte'); if (!k) break;
        if (n < 5) await page.screenshot({ path: path.join(BILD, `${MOTOR}-${B}-rundgang-${n + 1}.png`) });
        const im = await k.evaluate(x => { const r = x.getBoundingClientRect(); return r.left >= -1 && r.right <= innerWidth + 1 && r.top >= -1 && r.bottom <= innerHeight + 1; });
        ok(w, `Rundgang Schritt ${n + 1}: Karte ganz im Bild`, im);
        const los = await page.$('.rdg-los'); if (hand) await los.tap(); else await los.click(); await page.waitForTimeout(900);
      }
      ok(w, 'Rundgang: fünf Schritte, dann zu', n === 5 && !(await page.$('.rdg-karte')), n);
      ok(w, 'Rundgang ohne Fehler', !f.length, f.join(' | '));
      await ctx.close();
    }
    // E Weg aus der Werkbank: Link zur Stube, «Zur Werkbank» zurück
    {
      const { ctx, page, f } = await neu();
      await page.goto('http://127.0.0.1:8982/werkbank/index.html', { waitUntil: 'load' }); await page.waitForTimeout(1500);
      const l = await page.$('a[href*="8987/_werkzeuge/maison"]');
      ok(w, 'Werkbank hat Weg zur Stube', !!l);
      if (l) {
        await l.scrollIntoViewIfNeeded().catch(() => { });
        const tgt = await l.evaluate(x => x.target);
        const pop = tgt === '_blank' ? ctx.waitForEvent('page', { timeout: 8000 }) : null;
        await l.evaluate(x => x.click());
        let z = page; if (pop) z = await pop.catch(() => null);
        if (z) { await z.waitForLoadState('load').catch(() => { }); await z.waitForTimeout(2000); }
        ok(w, 'Werkbank → Stube öffnet', z && z.url().startsWith(BASIS), z && z.url());
        const zw = z ? await z.$('#zur-werkbank') : null;
        ok(w, 'Stube zeigt «Zur Werkbank»', !!zw);
        if (zw) {
          const zh = await zw.evaluate(x => (x.querySelector('a') || x).href || '');
          const r = zh ? await ctx.request.get(zh) : null;
          ok(w, '«Zur Werkbank» führt auf die Werkbank', r && r.status() === 200, zh);
          await z.screenshot({ path: path.join(BILD, `${MOTOR}-${B}-aus-werkbank.png`) });
        }
      }
      await ctx.close();
    }
  }
  await browser.close();
  const rot = erg.filter(x => !x.gut);
  fs.writeFileSync(path.join(__dirname, `democheck-${MOTOR}.json`), JSON.stringify({ zeit: new Date().toISOString(), gruen: erg.length - rot.length, rot: rot.length, ergebnis: erg }, null, 1));
  console.log(`${MOTOR}: ${erg.length - rot.length} grün, ${rot.length} rot`); rot.forEach(x => console.log('  ROT', x.w, x.n, x.info));
})().catch(e => { console.error(e); process.exit(1); });
