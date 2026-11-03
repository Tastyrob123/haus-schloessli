/* Kopf, Fuss und Trenner der Mails als PNG (kein Mailprogramm zeigt SVG zuverlässig): die echte Wortmarke «WIRTSCHAFT AM SCHLÖSSLI» und die Zeiger
   in Seehimmel auf der dunklen Fläche, Trenner als feine Linie in Seehimmel.
   NODE_PATH=/opt/node-tools/node_modules node _bau/mail_marken.js */
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const Z = path.join(__dirname, '..', 'haeuser', 'schloessli', 'mail');
const K = path.join(__dirname, '..', '..', 'oberflaeche', 'kleid');
const HIMMEL = '#A2B6CF';
const wm = fs.readFileSync(path.join(K, 'schloessli-marke.svg'), 'utf8').replace(/<symbol id="wm" viewBox="[^"]*">/, '').replace('</symbol>', '').replace(/<use[^>]*\/>/g, '').replace(/fill="currentColor"/g, `fill="${HIMMEL}"`);
const ze = fs.readFileSync(path.join(K, 'schloessli-zeichen.svg'), 'utf8').replace(/fill="currentColor"/g, `fill="${HIMMEL}"`);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 });
  const shot = async (html, w, h, f) => { await p.setViewportSize({ width: w, height: h }); await p.setContent(`<style>html,body{margin:0;background:transparent}svg{display:block}</style>${html}`); await p.screenshot({ path: path.join(Z, f), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } }); };
  await shot(`<div style="width:340px;height:40px;display:grid;place-items:center">${wm.replace('<svg ', '<svg style="width:340px;height:auto" ')}</div>`, 340, 40, '_kopf.png');
  await shot(`<div style="width:44px;height:54px;display:grid;place-items:center">${ze.replace('<svg ', '<svg style="height:54px;width:auto" ')}</div>`, 44, 54, '_fuss.png');
  await shot(`<div style="width:190px;height:30px;position:relative"><i style="position:absolute;left:20px;right:20px;top:14.5px;height:1px;background:${HIMMEL}"></i><i style="position:absolute;left:91px;top:11px;width:8px;height:8px;border-radius:50%;background:${HIMMEL}"></i></div>`, 190, 30, '_trenner.png');
  await b.close();
  console.log('Kopf, Fuss, Trenner fertig');
})();
