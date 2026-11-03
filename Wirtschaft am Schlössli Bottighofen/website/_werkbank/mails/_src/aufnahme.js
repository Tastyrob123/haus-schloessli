// Mails der Wirtschaft am Schlössli (Vorlage Culinarium, Nachtbau 3.11.2026): Zeichen (die Zeiger) und Wortmarke als PNG für die Mails (Mailprogramme
// zeigen kein SVG) und der obere Teil jeder Mail als Bild für die Werkbank, doppelte Dichte.
// node mails/_src/aufnahme.js   (Server 9288 läuft; vorher python3 mails/_src/bau.py)  → mails/img/zeichen.png, wortmarke.png, _werkbank/ansichten/Mails/NN.jpg
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.join(__dirname, '..', '..'), WEB = path.join(ROOT, '..'), B = 'http://127.0.0.1:' + (process.env.WB_PORT || 9288) + '/';
const liste = JSON.parse(fs.readFileSync(path.join(__dirname, 'werkbank.json'), 'utf8'));
(async () => {
  const b = await chromium.launch({ headless: true });
  const z = await b.newPage({ viewport: { width: 400, height: 540 }, deviceScaleFactor: 1 });
  // das Zeichen des Hauses: die Zeiger der Wortmarke (website/assets/svg/zeichen.svg) in Seehimmel, für den Kopf in Stuhlblau
  const x = fs.readFileSync(path.join(WEB, 'assets/svg/zeichen.svg'), 'utf8');
  await z.setContent('<body style="margin:0;background:transparent"><div id="z" style="width:200px;color:#a2b6cf">' + x.replace('<svg ', '<svg style="display:block;width:200px;height:auto" ') + '</div></body>');
  fs.mkdirSync(path.join(ROOT, 'mails/img'), { recursive: true });
  await (await z.$('#z')).screenshot({ path: path.join(ROOT, 'mails/img/zeichen.png'), omitBackground: true });
  // die Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» in Weiss, fertig aus dem Markenbuch (_werkzeuge/livre/dateien, dieselbe Zeichnung wie kleid/schloessli-marke.svg#wm)
  const wmq = path.join(WEB, '..', '_werkzeuge/livre/dateien/wirtschaft-am-schloessli-name-weiss.png');
  if (fs.existsSync(wmq)) fs.copyFileSync(wmq, path.join(ROOT, 'mails/img/wortmarke.png'));
  await z.close();
  const ziel = path.join(ROOT, '_werkbank/ansichten/Mails'); fs.mkdirSync(ziel, { recursive: true });
  for (const f of fs.readdirSync(ziel)) if (/^\d\d\.jpg$/.test(f) && !liste.some(([nr]) => nr + '.jpg' === f)) fs.unlinkSync(path.join(ziel, f));
  for (const [nr, ordner] of liste) {
    const p = await b.newPage({ viewport: { width: 640, height: 900 }, deviceScaleFactor: 2 });
    await p.goto(B + 'mails/' + ordner + '/index.html', { waitUntil: 'load' }); await p.waitForTimeout(1200);
    await p.screenshot({ path: path.join(ziel, nr + '.jpg'), quality: 88, clip: { x: 0, y: 0, width: 640, height: 940 }, fullPage: true });
    console.log('Mail', nr, ordner); await p.close();
  }
  await b.close();
})();
