// Mails der Wirtschaft am Schlössli: die Zeiger als PNG für die Mails (einmal) und der obere Teil jeder Mail als Bild für die Werkbank, doppelte Dichte.
// node mails/_src/aufnahme.js   (Server 8917 läuft; vorher python3 mails/_src/bau.py)  → mails/img/zeichen.png, _werkbank/ansichten/Mails/NN.jpg
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
const ROOT = path.join(__dirname, '..', '..'), B = 'http://127.0.0.1:' + (process.env.WB_PORT || 8982) + '/';
const liste = JSON.parse(fs.readFileSync(path.join(__dirname, 'werkbank.json'), 'utf8'));
(async () => {
  const b = await chromium.launch({ headless: true });
  const z = await b.newPage({ viewport: { width: 400, height: 540 }, deviceScaleFactor: 1 });
  const svg = fs.readFileSync(path.join(ROOT, 'assets/svg/zeichen.svg'), 'utf8').replace('fill="currentColor"', 'fill="url(#g)"').replace(/<(path|g) /, '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e7ecf3"/><stop offset=".5" stop-color="#c5d2e1"/><stop offset="1" stop-color="#a2b6cf"/></linearGradient></defs><g ');
  await z.setContent('<body style="margin:0;background:transparent"><div id="z" style="width:348px">' + svg.replace('<svg ', '<svg style="display:block;width:348px;height:auto" ') + '</div></body>');
  fs.mkdirSync(path.join(ROOT, 'mails/img'), { recursive: true });
  await (await z.$('#z')).screenshot({ path: path.join(ROOT, 'mails/img/zeichen.png'), omitBackground: true });
  await z.close();
  const ziel = path.join(ROOT, '_werkbank/ansichten/Mails'); fs.mkdirSync(ziel, { recursive: true });
  for (const [nr, ordner] of liste) {
    const p = await b.newPage({ viewport: { width: 640, height: 900 }, deviceScaleFactor: 2 });
    await p.goto(B + 'mails/' + ordner + '/index.html', { waitUntil: 'load' }); await p.waitForTimeout(1200);
    await p.screenshot({ path: path.join(ziel, nr + '.jpg'), quality: 88, clip: { x: 0, y: 0, width: 640, height: 940 }, fullPage: true });
    console.log('Mail', nr, ordner); await p.close();
  }
  await b.close();
})();
