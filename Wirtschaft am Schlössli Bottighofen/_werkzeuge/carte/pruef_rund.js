// Das Kartenpult · Rundlauf: Satz → Baum (einlesen.py, _daten/grundstand) → Satz (satz/satz.js) muss Zeichen für Zeichen gleich sein.
// node pruef_rund.js   (Ausgabe je Karte «gleich» oder die erste abweichende Stelle; Rückgabe 1, wenn eine Karte abweicht)
const fs = require('fs'), path = require('path');
const SATZ = require('./satz/satz.js');
const H = __dirname, K = process.env.CARTE_DATEN || path.join(H, '_daten');
SATZ.zeichen(JSON.parse(fs.readFileSync(path.join(H, 'satz', 'zeichen.json'), 'utf8')));
let schlecht = 0;
for (const f of fs.readdirSync(path.join(K, 'grundstand')).filter(x => x.endsWith('.json')).sort()) {
  const d = JSON.parse(fs.readFileSync(path.join(K, 'grundstand', f), 'utf8'));
  const soll = fs.readFileSync(path.join(H, 'satz', 'u-' + d.ziel + '.html'), 'utf8'), ist = SATZ.dokument(d);
  if (soll === ist) { console.log(d.ziel + ': gleich (' + d.seiten.length + ' Seiten)'); continue; }
  schlecht++;
  let i = 0; while (i < soll.length && soll[i] === ist[i]) i++;
  console.log(d.ziel + ': ANDERS ab Zeichen ' + i + '\n  soll: ' + soll.slice(Math.max(0, i - 60), i + 80) + '\n  ist:  ' + ist.slice(Math.max(0, i - 60), i + 80));
}
process.exit(schlecht ? 1 : 0);
