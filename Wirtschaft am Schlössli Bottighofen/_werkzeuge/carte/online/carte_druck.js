// Die Tafel (La Carte) · Wirtschaft am Schlössli online (19.10.2026, aus der Tafel des Gasterntal), der Teil mit Chromium (Vercel-Funktion, Node; 17.10.2026, Kopie aus der Tafel des Ruedihus, dort aus dem Doldenhorn und La Carte des Carlton-Europe). Liegt online als api/carte_druck.js.
// Nur api/carte.py ruft sie (Kopfzeile x-carte-druck = Schlüssel, abgeleitet aus dem Speicher-Schlüssel; ohne ihn 403). Druckt eine Karte wie
// _werkzeuge/carte/drucke.js auf dem Rechner des Hauses: satz/blatt.html der eigenen Website in Chromium, die Daten der Karte kommen aus der Anfrage
// (abgefangen statt /_werkzeuge/carte/api/druckdaten), PDF mit Seitengrösse aus @page. Antwort {ok, pdf (base64), bericht}.
// Chromium online: @sparticuz/chromium-min (Paket beim ersten Lauf von GitHub, ~2 s) + playwright-core; auf dem Rechner (Probe) das Playwright
// des Tasty Website Builder (PLAYWRIGHT_LOKAL). Vor jedem Druck wird /tmp aufgeräumt (Rivage 15.10.2026: ab dem fünften Druck sonst voll).
const path = require('path'), fs = require('fs'), crypto = require('crypto');

const ZIELE = ['speisekarte', 'mittag', 'laestermeile', 'weinkarte', 'bankett'];
const PACK = process.env.CHROMIUM_PACK || 'https://github.com/Sparticuz/chromium/releases/download/v153.0.0/chromium-v153.0.0-pack.x64.tar';
const SCHLUESSEL = crypto.createHash('sha256').update('carte-druck|' + (process.env.BLOB_READ_WRITE_TOKEN || process.env.VERCEL_DEPLOYMENT_ID || 'lokal')).digest('hex');

async function browser() {
  if (['production', 'preview'].includes(process.env.VERCEL_ENV || '')) {
    const m = await import('@sparticuz/chromium-min');   // ES-Modul seit Fassung 138
    const chromium = m.default || m;
    const { chromium: pw } = require('playwright-core');
    return pw.launch({ args: chromium.args.concat(['--disk-cache-size=1', '--media-cache-size=1', '--disable-dev-shm-usage']), executablePath: await chromium.executablePath(PACK), headless: true });
  }
  const pw = require(process.env.PLAYWRIGHT_LOKAL || path.join(process.env.HOME || '', 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright'));
  return pw.chromium.launch();
}
function tmpAufraeumen() {
  try {
    for (const n of fs.readdirSync('/tmp')) {
      if (/^(playwright|puppeteer|\.org\.chromium|core|chrome|\.com\.google)/i.test(n) && !/^chromium$/.test(n)) {
        try { fs.rmSync(path.join('/tmp', n), { recursive: true, force: true }); } catch (e) { /* weiter */ }
      }
    }
  } catch (e) { /* kein /tmp */ }
}
function tmpFrei() { try { const st = fs.statfsSync('/tmp'); return Math.round(st.bavail * st.bsize / 1048576) + ' MB frei in /tmp'; } catch (e) { return ''; } }

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') return res.status(405).json({ fehler: 'Nur POST.', stichwort: 'WEG' });
  if (req.headers['x-carte-druck'] !== SCHLUESSEL) return res.status(403).json({ fehler: 'Nur La Carte selbst lässt drucken.', stichwort: 'RECHT' });
  const body = typeof req.body === 'object' && req.body ? req.body : (() => { try { return JSON.parse(req.body || '{}'); } catch (e) { return {}; } })();
  const z = String(body.z || ''), daten = body.daten;
  if (!ZIELE.includes(z)) return res.status(400).json({ fehler: 'Diese Karte gibt es nicht.', stichwort: 'ZIEL' });
  if (!daten || typeof daten !== 'object' || JSON.stringify(daten).length > 3000000) return res.status(400).json({ fehler: 'Die Daten der Karte fehlen.', stichwort: 'FORM' });
  const basis = `${req.headers['x-forwarded-proto'] || 'https'}://${req.headers.host}`;
  if (process.env.VERCEL) tmpAufraeumen();
  let b;
  try { b = await browser(); } catch (e) { return res.status(500).json({ fehler: 'Der Druck startet nicht: ' + String(e.message || e).slice(0, 160) + ' (' + tmpFrei() + ')', stichwort: 'DRUCK' }); }
  try {
    const p = await b.newPage({ viewport: { width: 1300, height: 1400 }, deviceScaleFactor: 1.5 });   // wie drucke.js und _werkbank/satz_druck_datei.js
    await p.route('**/_werkzeuge/carte/api/druckdaten**', route => route.fulfill({ status: 200, contentType: 'application/json; charset=utf-8', body: JSON.stringify(daten) }));
    await p.goto(`${basis}/_werkzeuge/carte/satz/blatt.html?druck=1&z=${encodeURIComponent(z)}&q=entwurf&t=${Date.now()}`, { waitUntil: 'load', timeout: 60000 });
    await p.waitForFunction(() => window.CARTE_FERTIG || window.CARTE_FEHLER, null, { timeout: 120000 });
    const f = await p.evaluate(() => window.CARTE_FEHLER || null);
    if (f) return res.status(500).json({ fehler: 'Die Karte liess sich nicht setzen: ' + String(f).slice(0, 200), stichwort: 'DRUCK' });
    const bericht = await p.evaluate(() => window.CARTE_FERTIG);
    await p.emulateMedia({ media: 'print' });
    const pdf = await p.pdf({ preferCSSPageSize: true, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    return res.status(200).json({ ok: true, pdf: Buffer.from(pdf).toString('base64'), bericht });
  } catch (e) {
    return res.status(500).json({ fehler: 'Die PDF liess sich nicht drucken: ' + String(e.message || e).slice(0, 200) + ' (' + tmpFrei() + ')', stichwort: 'DRUCK' });
  } finally { await b.close().catch(() => {}); }
};
