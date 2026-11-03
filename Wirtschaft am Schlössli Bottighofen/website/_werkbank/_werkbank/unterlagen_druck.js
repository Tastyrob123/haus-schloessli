// Brief und Angebot drucken (Werkbank Papier, Nachtbau 3.11.2026; nach papier_druck.js des Kits): node _werkbank/unterlagen_druck.js "<website/_werkbank>"
//   unterlagen/pdf/<kurz>-brief.pdf, <kurz>-angebot.pdf   jede Seite einzeln gedruckt, mit pdfunite zusammengefügt (feste Schnitte, kein Type 3)
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.resolve(process.argv[2]), HIER = path.join(ROOT, '_werkbank');
const P = JSON.parse(fs.readFileSync(path.join(HIER, 'plan.json'), 'utf8'));
const KURZ = 'wirtschaft-am-schloessli', EIN = path.join(HIER, 'roh', 'einzel-unterlagen');
(async () => {
  fs.mkdirSync(EIN, { recursive: true }); fs.mkdirSync(path.join(ROOT, 'unterlagen/pdf'), { recursive: true });
  const b = await chromium.launch();
  for (const id of ['brief', 'angebot']) {
    const p = await b.newPage({ viewport: { width: 1300, height: 1300 } });
    await p.goto(P.base + '_werkbank/satz/unterlagen-' + id + '.html', { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
    await p.evaluate(() => document.documentElement.className = 'einzeln'); await p.emulateMedia({ media: 'print' });
    const n = await p.evaluate(() => document.querySelectorAll('.blatt').length), teile = [];
    for (let i = 0; i < n; i++) {
      const m = await p.evaluate(i => { document.querySelectorAll('.blatt').forEach((x, k) => x.classList.toggle('dran', k === i)); const x = document.querySelectorAll('.blatt')[i]; return [x.dataset.b, x.dataset.h]; }, i);
      const t = path.join(EIN, id + '-' + i + '.pdf');
      await p.pdf({ path: t, width: m[0] + 'mm', height: m[1] + 'mm', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1' });
      teile.push(t);
    }
    const ziel = path.join(ROOT, 'unterlagen/pdf', KURZ + '-' + id + '.pdf');
    if (teile.length === 1) fs.copyFileSync(teile[0], ziel); else execFileSync('pdfunite', [...teile, ziel]);
    console.log(id, n, 'Seiten'); await p.close();
  }
  await b.close();
})();
