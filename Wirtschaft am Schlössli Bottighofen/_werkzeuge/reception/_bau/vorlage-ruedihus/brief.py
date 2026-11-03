#!/usr/bin/env python3
"""Dritter Schritt nach portiere.py und ruedihus.py: Briefpapier des Landgasthof Ruedihus statt Formular (Vorbild Doldenhorn und Carlton _bau/brief.py,
dort «Brief viel luxuriöser und edler», Robert 16.10.2026). Markup und Mail in reception.js; das Aussehen am Bildschirm steht in ruedihus.css («Der Brief»).

Das Kleid kommt aus den Mails des Hauses (mails/01-tisch, 02-anreise, 03-gutschein): Kopf in Wandholz mit dem Zeichen in Gold, Name in Gelasio fett
in Versalien, Ort in Versalien in Kerzenlicht, Anrede und Gruss in Gelasio fett, Text in Instrument Sans, Fuss in Stube-Braun mit Adresse, Telefon und Mail.
Jede Ersetzung muss genau einmal treffen, sonst bricht das Skript ab."""
import os, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(C, 'reception.js')
t = open(p, encoding='utf-8').read()


def ers(alt, neu, n=1):
    global t
    if t.count(alt) != n:
        sys.exit(f'ABBRUCH: «{alt[:80]}» kommt {t.count(alt)}× vor, erwartet {n}×')
    t = t.replace(alt, neu)


# Siegel (die Tannen, klein) vor der Fusszeile
ers('<footer class="brief__fuss">Hinder de Büele 6 · 3718 Kandersteg<br>(+41) 033 675 81 81 · info@doldenhorn.ch</footer>',
    '<div class="brief__siegel" aria-hidden="true">${ZEICHEN}</div>\n          <footer class="brief__fuss">Hinder de Büele 6 · 3718 Kandersteg<br>(+41) 033 675 81 81 · info@doldenhorn.ch</footer>')
ers("          ${linie('linie3')}\n          ${bk('fuss'", "          <div class=\"brief__siegel\" aria-hidden=\"true\">${ZEICHEN}</div>\n          ${linie('linie3')}\n          ${bk('fuss'")
# Von: keine Vorlagen-Zeile im Brief (Werkzeug-Technik, nicht Briefpapier); die Vorlage steht als Hinweis am Absender
ers("<dd>${esc(e.absender)}<small>Vorlage ${esc(e.vorlage)}</small></dd>", "<dd title=\"Mail-Vorlage: ${esc(e.vorlage)}\">${esc(e.absender)}</dd>", 2)
# Schlussabsatz (Gruss, Name, Abteilung) als Unterschrift
ers("ab.map((x, n) => bk('p' + n, 'gs--p', feldHTML(x), true, ' dir=\"auto\"') + fotos('p' + n)).join('')",
    "ab.map((x, n) => bk('p' + n, 'gs--p' + (ab.length > 2 && n === ab.length - 1 ? ' gs--sign' : ''), feldHTML(x), true, ' dir=\"auto\"') + fotos('p' + n)).join('')")
# Offene Stellen: keine Etiketten, nur die Markierung
ers("'<mark class=\"offen-feld\"><i>offen</i>$1</mark>'", "'<mark class=\"offen-feld\">$1</mark>'")
# Druck: Hintergründe und Farben mitdrucken
ers(".brief::before{inset:10px}.gs{cursor:default!important;box-shadow:none!important}", "*{-webkit-print-color-adjust:exact;print-color-adjust:exact}.gs{cursor:default!important;box-shadow:none!important}")

# ---- Mail im Kleid der Hausmails des Ruedihus (nur Tabellen und Inline-Stile, wie es Mailprogramme verlangen; Werte aus mails/01-tisch/index.html)
SANS = "font-family:'Instrument Sans','Helvetica Neue',Helvetica,Arial,sans-serif"
ers('<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:100%;background:#fffcf5;border:1px solid #e4d9c3">\n<tr><td style="padding:44px 48px 36px">',
    '<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:100%;background:#fbf5ea;border-radius:22px;overflow:hidden">\n<tr><td style="padding:0">')
# Kopf: Wandholz mit dem Zeichen in Gold, Name in Versalien, Ort in Kerzenlicht (wie die Hausmails)
ers('<tr><td style="text-align:center;padding-bottom:8px"><img src="${basis}assets/logo/zeichen-gold.webp" width="${Math.round(46 * ((G.zeichen || {}).s || 1))}" alt="" style="height:auto;border:0"></td></tr>',
    '<tr><td style="background:#321f10;text-align:center;padding:34px 20px 4px"><img src="${wz}zeichen-gold.png" width="${Math.round(46 * ((G.zeichen || {}).s || 1))}" alt="" style="height:auto;border:0"></td></tr>')
ers("""<tr><td style="${st('haus', 20, "text-align:center;letter-spacing:.3em;text-transform:uppercase;font-family:Gelasio,Georgia,serif;color:#321f10")}">${kt('haus')}</td></tr>""",
    """<tr><td style="background:#321f10;${st('haus', 15, "text-align:center;letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-family:Gelasio,Georgia,'Times New Roman',serif;color:#fbf5ea;padding-top:12px")}">${kt('haus')}</td></tr>""")
ers("""<tr><td style="${st('zeile', 9, 'text-align:center;letter-spacing:.32em;text-transform:uppercase;font-family:Menlo,monospace;color:#84603c;padding-top:6px')}">${kt('zeile')}</td></tr>""",
    """<tr><td style="background:#321f10;${st('zeile', 10.5, "text-align:center;letter-spacing:.24em;text-transform:uppercase;%s;color:#c98543;padding:8px 20px 30px")}">${kt('zeile')}</td></tr>
<tr><td style="padding:34px 40px 30px">
<table role="presentation" width="100%%" cellpadding="0" cellspacing="0">""" % SANS)
ers('<tr><td style="font-family:Menlo,monospace;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:#84603c">Betreff</td></tr>',
    '<tr><td style="%s;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:#84603c">Betreff</td></tr>' % SANS)
ers("""${st('betreff', 23, serif + ';font-weight:500;color:#321f10;padding:4px 0 28px;line-height:1.25')}""",
    """${st('betreff', 22, serif + ';font-weight:700;color:#2a1a0e;padding:6px 0 22px;line-height:1.2')}""")
ers("""${st('p' + n, 18, serif + ';line-height:1.6;padding-bottom:' + (16 + Math.max(0, (G['p' + n] || {}).mb || 0)) + 'px')}""",
    """${st('p' + n, 16, "%s;color:#3d2a1a;line-height:1.62;padding-bottom:" + (14 + Math.max(0, (G['p' + n] || {}).mb || 0)) + 'px' + (ab.length > 2 && n === ab.length - 1 ? ';padding-top:8px' : ''))}""" % SANS)
ers("${mLinie('linie3', '30px 0 0')}", """<tr><td style="text-align:center;padding:22px 0 0"><img src="${wz}zeichen-gold.png" width="22" alt="" style="height:auto;border:0"></td></tr>
${mLinie('linie3', '16px 0 0')}""")
ers("""${st('fuss', 9.5, 'text-align:center;letter-spacing:.14em;text-transform:uppercase;font-family:Menlo,monospace;color:#84603c;line-height:1.9;padding-top:14px')}""",
    """${st('fuss', 13, "text-align:center;%s;color:#5a4532;line-height:1.6;padding-top:14px")}""" % SANS)
ers("</table></td></tr></table></td></tr></table>`;\n}", "</table></td></tr></table></td></tr></table></td></tr></table>`;\n}")
# Ordner des Werkzeugs (für das Zeichen in der Mail): lokal /_werkzeuge/reception/, online /werkzeuge/reception/
ers("const G = e.gestalt || {}, bilder = G._bilder || [], basis = location.origin + location.pathname.replace(/_?werkzeuge\\/reception\\/.*$/, '');",
    "const G = e.gestalt || {}, bilder = G._bilder || [], basis = location.origin + location.pathname.replace(/_?werkzeuge\\/reception\\/.*$/, ''), wz = location.origin + location.pathname.replace(/[^/]*$/, '');")
open(p, 'w', encoding='utf-8').write(t)
print('Brief eingesetzt')
