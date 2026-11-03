#!/usr/bin/env python3
"""Vierter Schritt nach portiere.py, carlton.py und brief.py (Robert 16.10.2026: «Als PDF sichern soll ein fertiges, edles PDF erzeugen, nicht das Druckfenster»):
der Server setzt den Brief mit Chromium (brief_pdf.js, Seite brief-pdf.html) und schickt die Datei zum Laden. Jede Ersetzung muss genau einmal treffen."""
import os, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(C, 'reception.js')
t = open(p, encoding='utf-8').read()

def ers(alt, neu, n=1):
    global t
    if t.count(alt) != n:
        sys.exit(f'ABBRUCH: «{alt[:80]}» kommt {t.count(alt)}× vor, erwartet {n}×')
    t = t.replace(alt, neu)

a = t.index('function briefPDF() {'); b = t.index('function verbindeBrief(a) {')
t = t[:a] + '''async function briefPDF(a) {   // Der Server setzt den Brief als A4-PDF (Chromium); die Datei wird direkt geladen
  if (!a) return;
  quit('Das PDF wird gesetzt', 'Das dauert einen Moment.', [], false, 15000);
  let r;
  try { r = await fetch('api/brief_pdf', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: a.id }) }); }
  catch (e) { return fehler(new Error('VERBINDUNG · Der Server-Teil antwortet nicht.')); }
  if (!r.ok) { let d = {}; try { d = await r.json(); } catch (e) { /* */ } return fehler(new Error(d.fehler || ('SERVER · Fehler ' + r.status))); }
  const m = /filename\\*=UTF-8''([^;]+)/.exec(r.headers.get('Content-Disposition') || ''), name = m ? decodeURIComponent(m[1]) : 'Brief.pdf';
  const url = URL.createObjectURL(await r.blob()), l = document.createElement('a'); l.href = url; l.download = name; document.body.appendChild(l); l.click(); l.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
  quit('PDF gesichert', name, [], false, 6000);
}
''' + t[b:]
ers("    if (akt === 'pdf') return briefPDF();",
    "    if (akt === 'pdf') {\n      if ($('#e-text')) { const b = $('#e-betreff').value, x = $('#e-text').value; if (b !== a.entwurf.betreff || x !== a.entwurf.text) { await api('anfrage', { id: a.id, betreff: b, entwurf_text: x }); a.entwurf.betreff = b; a.entwurf.text = x; } }\n      return briefPDF(a);\n    }")
ers("${bearb ? `<button class=\"kn kn--linie\" type=\"button\" data-akt=\"sichern\">Änderung sichern<i>${SYM.haken}</i></button>` : `<button class=\"kn kn--linie\" type=\"button\" data-akt=\"pdf\">Als PDF sichern<i>${SYM.post}</i></button>`}",
    "${bearb ? `<button class=\"kn kn--linie\" type=\"button\" data-akt=\"sichern\">Änderung sichern<i>${SYM.haken}</i></button>` : ''}\n            <button class=\"kn kn--linie\" type=\"button\" data-akt=\"pdf\">Als PDF sichern<i>${SYM.post}</i></button>")
ers("«Als PDF sichern» genau so, wie er hier steht.", "«Als PDF sichern» setzt ihn als fertige A4-Seite (bei langem Text mit sauberem Umbruch).")
open(p, 'w', encoding='utf-8').write(t)
print('PDF eingesetzt')
