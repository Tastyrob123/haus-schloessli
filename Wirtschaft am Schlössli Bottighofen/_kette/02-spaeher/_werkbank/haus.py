"""Wirtschaft am Schlössli, Bottighofen: Haken für das Werkbank-Kit, nur für die Befund-Seite des Spähers (Station 2, 18.10.2026).
Farben aus der heutigen Seite und dem Startbild gemessen (Knopf #213c4f, Text #0f3538, Stuhl #307998, Kies und Sand #b89668 aus
`_quelle-bilder/terrasse-tag.jpg`), Zeichen aus dem Logo (Zeiger und Kreis ohne Schrift) mit potrace. Titelschrift Gilda Display wie auf der
heutigen Seite; Marke, Schrift und Farbwelten legt erst Station 5 fest."""
import os, sys
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'Wirtschaft am Schlössli'
KURZ = 'schloessli-bottighofen'
LEISTE = 'Schlössli'
PORT = 8978
RECHTE = 'der Wirtschaft am Schlössli, der Taverne zum Schäfli AG und den jeweiligen Fotografen.'
SEITEN = []
ETIKETTEN = dict(ordner='etiketten', name='Etiketten', einzahl='Etikett')

# Seeblau der Knöpfe als Nacht, Sand vom Ufer als Gold, Stuhlblau als Punkt, Papier mit einem Hauch Mint wie der Grund der heutigen Seite
FARBEN = dict(nacht='#10222e', tief='#0a1720', navy='#213c4f', blau='#2b4c62', papier='#f3f8f6', creme='#e3efeb', weiss='#fbfdfc',
              gold='#c9a97a', messing='#b89668', taupe='#8a7358', tinte='#0f2a33', punkt='#307998', rot='#b3412e')
SCHRIFT = dict(titel=('Gilda Display', 'GildaDisplay-latin.woff2'), titel_folge="Georgia,'Times New Roman',serif", ersatz="local('Georgia');size-adjust:100%")
DRUCKSCHRIFT = []
ZEICHEN = K.svg_innen(os.path.join(ROOT, 'assets/logo/zeichen.svg'))
WORT = K.text_pfad(os.path.join(ROOT, 'assets/fonts/GildaDisplay-latin.woff2'), 'Wirtschaft am Schlössli', .04)
MUSTER = 'url("muster.svg")'
MUSTER_B = '240px'
CSS = '''
/* Befund: Tabellen und Belege */
.bf-tab{width:100%;border-collapse:collapse;margin-top:clamp(18px,2vw,28px);font-size:15px}
.bf-tab th,.bf-tab td{text-align:left;padding:12px 14px;border-bottom:1px solid color-mix(in srgb,currentColor 14%,transparent);vertical-align:top}
.bf-tab th{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.7;font-weight:400}
.bf-beleg{font-family:var(--mono);font-size:12px;opacity:.72;word-break:break-word}
.bf-offen{color:var(--rot)}
.fl--nacht .bf-offen{color:#e98a72}
.bf-liste{list-style:none;padding:0;margin:clamp(18px,2vw,28px) 0 0;display:grid;gap:14px}
.bf-liste li{padding:18px 20px;border-radius:22px;background:color-mix(in srgb,currentColor 5%,transparent);box-shadow:inset 0 2px 6px rgba(0,0,0,.08)}
.bf-liste b{display:block;font-family:var(--serif);font-weight:400;font-size:20px;margin-bottom:4px}
.bf-fam{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin-top:clamp(22px,2.4vw,34px)}
.bf-fam a{display:block;border-radius:26px;overflow:hidden;color:inherit;text-decoration:none;background:color-mix(in srgb,currentColor 6%,transparent)}
.bf-fam img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.bf-fam div{padding:16px 18px 20px}
.bf-fam b{display:block;font-family:var(--serif);font-weight:400;font-size:21px}
.bf-fam small{display:block;font-family:var(--mono);font-size:11.5px;opacity:.72;margin-top:6px;line-height:1.5}
.bf-zwei{display:grid;grid-template-columns:1fr 1fr;gap:clamp(16px,2vw,28px);margin-top:clamp(22px,2.4vw,34px)}
.bf-zwei>div{padding:22px 24px;border-radius:26px;background:color-mix(in srgb,currentColor 5%,transparent);box-shadow:inset 0 2px 6px rgba(0,0,0,.08)}
.bf-zwei h3{font-family:var(--serif);font-weight:400;font-size:24px;margin:0 0 10px}
.bf-zwei ul{margin:0;padding:0;list-style:none;line-height:1.55}
.bf-zwei li{padding:9px 0;border-top:1px solid color-mix(in srgb,currentColor 14%,transparent)}
.bf-zwei li:first-child{border-top:0;padding-top:0}
.bf-urteil{font-family:var(--serif);font-size:clamp(30px,3.6vw,52px);line-height:1.12;margin:0}
.bf-urteil em{font-style:normal;color:var(--gold)}
@media (max-width:760px){.bf-zwei{grid-template-columns:1fr}}
@media (max-width:640px){.bf-tab,.bf-tab tbody,.bf-tab tr,.bf-tab td{display:block;width:100%}.bf-tab thead{display:none}.bf-tab tr{padding:12px 0;border-bottom:1px solid color-mix(in srgb,currentColor 14%,transparent)}.bf-tab td{border:0;padding:2px 0;font-size:15px}.bf-tab td:first-child{font-family:var(--serif);font-size:19px;margin-bottom:4px}}
'''
