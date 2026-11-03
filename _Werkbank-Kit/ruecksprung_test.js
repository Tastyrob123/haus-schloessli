// Rücksprung-Test (Robert 1.11.2026): Seite laden, auf ~60 % scrollen, Link in eine andere Werkbank-Seite im selben Tab, Zurück;
// der Abschnitt in Fenstermitte muss ±40 px an derselben Stelle im Fenster stehen (in einer mitlaufenden Bühne der Abschnitt, der sie trägt; bewegte Teile darin zählen nicht);
// ohne Abschnitt der Text in Fenstermitte, nur wenn gar nichts zu finden ist: scrollY ±40 px. Headless, nichts im Vordergrund.
//   node ruecksprung_test.js http://127.0.0.1:<port>/ [chromium|webkit] [playwright-pfad]
const [, , BASIS, ART = 'chromium', PW = 'playwright'] = process.argv;
const pw = require(PW);
const FAELLE = [['Startseite → Feed', 'werkbank/index.html', 'feed/']].concat(
  ['feed', 'befund', 'unterlagen', 'drucksachen', 'untersetzer', 'sticker', 'postkarten', 'beigaben', 'mails', 'material', 'werkbank/geprueft']
    .map(o => ['Unterseite ' + o + ' → weiter', o + '/index.html', null]));(async () => {
  const b = await pw[ART].launch();
  let fehler = 0;
  for (const breite of [1440, 390]) {
    const ctx = await b.newContext({ viewport: { width: breite, height: breite > 500 ? 900 : 844 } });
    for (const [name, pfad, ziel] of FAELLE) {
      const p = await ctx.newPage();
      try {
        const r = await p.goto(BASIS + pfad, { waitUntil: 'load' });
        if (!r || r.status() >= 400) { await p.close(); continue; }
        await p.waitForTimeout(800);
        const h = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
        if (h < 200) { console.log(`–  ${breite} ${name}: zu kurz (${h})`); await p.close(); continue; }
        const soll = Math.round(h * 0.6);
        // in Schritten scrollen wie ein Mensch, dann einen Moment warten
        for (let y = 0; y <= soll; y += 600) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(30); }
        await p.evaluate(y => scrollTo(0, y), soll); await p.waitForTimeout(500);
        const vor = await p.evaluate(() => Math.round(scrollY));
        // Inhalt in Fenstermitte merken (Text eines Absatzes/Titels/Bildes und seine Lage)
        const MARK = () => {
          const S = 'h1,h2,h3,h4,p,li,img,figure';
          const st = document.elementsFromPoint(innerWidth / 2, innerHeight / 2);
          for (const e of st) { const c = e.closest(S) || ((e.tagName === 'IMG' || (e.children.length === 0 && e.textContent.trim().length > 3)) ? e : null); if (c) { let f = c, fx = false; while (f && f !== document.body) { const ps = getComputedStyle(f).position; if (ps === 'fixed' || ps === 'sticky') fx = true; f = f.parentElement; }
            if (!fx) return { t: (c.textContent || c.getAttribute('src') || '').replace(/\s+/g, ' ').trim().slice(0, 50), n: c.tagName, top: Math.round(c.getBoundingClientRect().top) }; } }
          return null; };
        const PFAD = () => {   // feststehendes Stück in Fenstermitte über seinen Platz im Aufbau (Rückfall, wenn kein Text da ist)
          const festAb = (e) => { let f = null; for (; e && e !== document.body; e = e.parentElement) { const ps = getComputedStyle(e).position; if (ps === 'fixed' || ps === 'sticky') f = e; } return f; };
          for (const e0 of document.elementsFromPoint(innerWidth / 2, innerHeight / 2)) {
            let e = e0, n = 0;
            while (e && e !== document.body && n++ < 30) { const f = festAb(e); if (!f) break; if (getComputedStyle(f).position === 'fixed') { e = null; break; } e = f.parentElement; }
            if (!e || e === document.body || e === document.documentElement) continue;
            const g = e.closest('section,article,header,footer,[id]');   // der Abschnitt drumherum: bewegte Teile darin (Chat, Film, Bühne) verrutschen, er nicht
            if (g && g !== document.body && g.tagName !== 'MAIN' && !festAb(g) && g.getBoundingClientRect().height <= innerHeight * 4) e = g;
            const pf = []; let x = e; while (x && x !== document.body) { pf.unshift([...x.parentElement.children].indexOf(x)); x = x.parentElement; }
            return { pf, n: e.tagName, top: Math.round(e.getBoundingClientRect().top) };
          }
          return null; };
        const inhalt = await p.evaluate(MARK);
        const platz = await p.evaluate(PFAD);
        // Link wählen: das Ziel, sonst ein Link auf eine andere Seite der Werkbank (gleiche Herkunft, kein #, kein PDF)
        const href = await p.evaluate((ziel) => {
          const alle = [...document.querySelectorAll('a[href]')].filter(a => {
            const u = new URL(a.href, location.href);
            return u.origin === location.origin && u.pathname !== location.pathname && !/\.(pdf|jpg|webp|png|zip|mp4)$/i.test(u.pathname)
              && /^\/(werkbank|feed|mails|befund|unterlagen|drucksachen|material|untersetzer|sticker|postkarten|beigaben)\//.test(u.pathname);
          });
          const a = (ziel && alle.find(a => a.getAttribute('href').includes(ziel))) || alle[0];
          if (!a) return null;
          a.removeAttribute('target');
          a.setAttribute('data-test', '1');
          return a.getAttribute('href');
        }, ziel);
        if (!href) { console.log(`–  ${breite} ${name}: kein Link`); await p.close(); continue; }
        await Promise.all([p.waitForNavigation({ waitUntil: 'load' }), p.evaluate(() => document.querySelector('a[data-test]').click())]);
        await p.waitForTimeout(700);
        const dort = p.url();
        await p.goBack({ waitUntil: 'load' });
        await p.waitForTimeout(2500);
        const nach = await p.evaluate(() => Math.round(scrollY));
        const lage = inhalt ? await p.evaluate((m) => { const k = [...document.querySelectorAll(m.n)].filter(e => (e.textContent || e.getAttribute('src') || '').replace(/\s+/g, ' ').trim().slice(0, 50) === m.t);
          if (!k.length) return null; return k.map(e => Math.round(e.getBoundingClientRect().top)).sort((a, b) => Math.abs(a - m.top) - Math.abs(b - m.top))[0]; }, inhalt) : null;
        const lage2 = platz ? await p.evaluate((m) => { let e = document.body; for (const i of m.pf) e = e && e.children[i]; return e && e.tagName === m.n ? Math.round(e.getBoundingClientRect().top) : null; }, platz) : null;
        const ok = platz ? (lage2 !== null && Math.abs(lage2 - platz.top) <= 40) : inhalt ? (lage !== null && Math.abs(lage - inhalt.top) <= 40) : Math.abs(nach - vor) <= 40;
        if (!ok) fehler++;
        console.log(`${ok ? '✓' : '✗'}  ${ART} ${breite} ${name}: vor ${vor}, nach Zurück ${nach}; Abschnitt ${platz ? '<' + platz.n + '> ' + platz.top + ' → ' + lage2 : '–'}; Text «${inhalt ? inhalt.t.slice(0, 24) : '–'}» ${inhalt ? inhalt.top + ' → ' + lage : ''} (über ${href} → ${dort.replace(BASIS, '')})`);
      } catch (e) { fehler++; console.log(`✗  ${ART} ${breite} ${name}: ${e.message.split('\n')[0]}`); }
      await p.close();
    }
    await ctx.close();
  }
  await b.close();
  console.log(fehler ? `${fehler} Fehler` : 'alles bestanden');
  process.exit(fehler ? 1 : 0);
})();
