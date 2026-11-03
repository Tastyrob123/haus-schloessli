#!/usr/bin/env python3
"""Neunter Schritt nach formulare.py (Werkbank-Chat 17.10.2026, Robert: «Wir verschicken alles von allen Seiten mit Formularen»):
Antwortbrief ohne Mailprogramm. «Im Mailprogramm öffnen» ist weg, der Brief bleibt im Werkzeug: «Als PDF speichern» setzt ihn als A4-Seite,
«Text kopieren» legt Betreff und Brief als Text in die Zwischenablage. Mail-Adressen der Gäste stehen als Text, nie als mailto.
Ersetzungen wörtlich aus Waldhotel Doldenhorn/_werkzeuge/reception/_bau/formulare.py (nur gelesen), dazu die Schritte 38 und 39 der Gegenprobe.
Jede Ersetzung muss genau so oft treffen wie angegeben; schon gesetzt = übersprungen.   Aufruf: python3 _werkzeuge/reception/_bau/formulare2.py"""
import os
HIER = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HIER)


def ers(datei, paare):
    p = os.path.join(C, datei)
    t = open(p, encoding='utf-8').read()
    for alt, neu, n in paare:
        if t.count(alt) != n:
            if t.count(neu) and not t.count(alt):
                continue   # schon gesetzt (Schritt zweimal gelaufen)
            raise SystemExit(f'{datei}: «{alt[:90]}» trifft {t.count(alt)}× statt {n}×')
        t = t.replace(alt, neu)
    open(p, 'w', encoding='utf-8').write(t)


ers('reception.js', [
    # --- Brief: nichts mehr ans Mailprogramm
    ("<p>${offen ? 'Die gold markierten Felder füllt Ihr Team aus, zum Beispiel Preise, Zeiten oder ob ein Raum frei ist.' : 'Lesen Sie ihn einmal durch und schicken Sie ihn aus Ihrem Mailprogramm.'}</p>",
     "<p>${offen ? 'Die gold markierten Felder füllt Ihr Team aus, zum Beispiel Preise, Zeiten oder ob ein Raum frei ist.' : 'Lesen Sie ihn einmal durch. Danach als PDF speichern oder den Text kopieren.'}</p>", 1),
    ('<button class="kn kn--gold" type="button" data-akt="kopieren">Brief kopieren<i>${SYM.kopie}</i></button>\n'
     "            ${/@/.test(a.kontakt || '') ? `<button class=\"kn\" type=\"button\" data-akt=\"mail\">Im Mailprogramm öffnen<i>${SYM.post}</i></button>` : ''}\n",
     '<button class="kn kn--gold" type="button" data-akt="pdf">Als PDF speichern<i>${SYM.post}</i></button>\n'
     '            <button class="kn" type="button" data-akt="kopieren">Text kopieren<i>${SYM.kopie}</i></button>\n', 1),
    ('            <button class="kn kn--linie" type="button" data-akt="pdf">Als PDF sichern<i>${SYM.post}</i></button>\n', '', 1),
    ("«Brief kopieren» legt den gestalteten Brief zum Einfügen ins Mailprogramm ab, «Als PDF sichern» setzt ihn als fertige A4-Seite (bei langem Text mit sauberem Umbruch). '}Verschickt wird hier nichts. Sie kopieren den Brief oder öffnen ihn in Ihrem Mailprogramm und schicken selbst.",
     "«Als PDF speichern» setzt ihn als fertige A4-Seite (bei langem Text mit sauberem Umbruch), «Text kopieren» legt Betreff und Brief als Text in die Zwischenablage. '}Verschickt wird hier nichts, und es öffnet sich kein Mailprogramm. Der Brief bleibt hier bei der Anfrage.", 1),
    ("    if (akt === 'kopieren' || akt === 'mail' || akt === 'sichern') {", "    if (akt === 'kopieren' || akt === 'sichern') {", 1),
    ("      if (akt === 'kopieren') { try { const plain = 'Betreff: ' + betreff + '\\n\\n' + text; if (window.ClipboardItem && $('#brief')) await navigator.clipboard.write([new ClipboardItem({ 'text/html': new Blob([briefMail(a, a.entwurf)], { type: 'text/html' }), 'text/plain': new Blob([plain], { type: 'text/plain' }) })]); else await navigator.clipboard.writeText(plain); } catch (e) { return quit('Nicht kopiert', 'Der Browser hat die Zwischenablage nicht freigegeben. Markieren Sie den Text und kopieren Sie ihn von Hand.', [], true); } return quit('Kopiert', $('#brief') ? 'Der gestaltete Brief liegt in der Zwischenablage. Im Mailprogramm einfügen, er erscheint mit Briefkopf und Fotos.' : 'Betreff und Brief liegen in der Zwischenablage.', [], false, 6000); }\n"
     "      if (akt === 'mail') { location.href = `mailto:${encodeURIComponent(a.kontakt.trim())}?subject=${encodeURIComponent(betreff)}&body=${encodeURIComponent(text)}`; return quit('Im Mailprogramm geöffnet', 'Dort prüfen und selbst schicken.', [], false, 5000); }\n",
     "      if (akt === 'kopieren') { try { await navigator.clipboard.writeText('Betreff: ' + betreff + '\\n\\n' + text); } catch (e) { return quit('Nicht kopiert', 'Der Browser hat die Zwischenablage nicht freigegeben. Markieren Sie den Text und kopieren Sie ihn von Hand.', [], true); } return quit('Kopiert', 'Betreff und Brief liegen als Text in der Zwischenablage.', [], false, 5000); }\n", 1),
    # --- Mail-Adresse des Gastes als Text zum Markieren und Kopieren, kein mailto (nichts öffnet ein Mailprogramm)
    ("  if (/^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$/.test(t)) return `<a href=\"mailto:${esc(t)}\">${esc(t)}</a>`;",
     "  if (/^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$/.test(t)) return `<span class=\"re-mail\">${esc(t)}</span>`;   // kein mailto, Adresse zum Kopieren (17.10.2026)", 1),
])

ers('anleitung.html', [
    ('<p class="s">Hier wird nichts verschickt. Die Mail schicken Sie selbst, aus Ihrem Mailprogramm.</p>\n'
     '<ol><li><b>Brief kopieren</b> legt den gestalteten Brief (mit Anordnung, Linien und Fotos) und den reinen Text in die Zwischenablage. Im Mailprogramm einfügen: der Brief erscheint, wie Sie ihn gestaltet haben.</li>\n'
     '<li><b>Im Mailprogramm öffnen</b> (nur wenn der Gast eine E-Mail-Adresse genannt hat) legt eine neue Mail an den Gast mit Betreff und Text an.</li>\n'
     '<li><b>Als PDF sichern</b> setzt',
     '<p class="s">Hier wird nichts verschickt, und es öffnet sich kein Mailprogramm. Der Brief bleibt bei der Anfrage.</p>\n'
     '<ol><li><b>Text kopieren</b> legt Betreff und Brief als reinen Text in die Zwischenablage.</li>\n'
     '<li><b>Als PDF speichern</b> setzt', 1),
])

gp = os.path.join(C, 'pruefung', 'gegenprobe.js')
if os.path.exists(gp):   # Schritte 38 und 39 der Gegenprobe: ganze Zeile tauschen (Wortlaut im Ruedihus anders als im Doldenhorn)
    import re
    g = open(gp, encoding='utf-8').read()
    S38 = "  await schritt('38 Text kopieren: Betreff und Brief als Text in der Zwischenablage', async () => { await erstesBrief(); await p.click('#detail [data-akt=\"kopieren\"]'); const m = await quit(/Kopiert|Nicht kopiert/); ok(/Kopiert/.test(m), m); if (MOTOR === 'chromium') { const r = await p.evaluate(async () => (await navigator.clipboard.readText()).length); ok(r > 100, 'Text ' + r); return 'Text ' + r + ' Zeichen'; } return m; });"
    S39 = "  await schritt('39 Kein Mailprogramm: Brief bleibt im Werkzeug, «Als PDF speichern» und «Text kopieren» da', async () => { await erstesBrief(); ok(await n('#detail [data-akt=\"mail\"]') === 0, 'Knopf zum Mailprogramm steht noch'); ok(await n('#detail a[href^=\"mailto:\"]') === 0, 'mailto im Brief'); ok(await n('#detail [data-akt=\"pdf\"]') === 1 && await n('#detail [data-akt=\"kopieren\"]') === 1, 'PDF oder Kopieren fehlt'); return 'PDF + Text kopieren'; });"
    for nr, zeile in (('38', S38), ('39', S39)):
        g, k = re.subn(r"^  await schritt\('" + nr + r" [^\n]*$", lambda m: zeile, g, count=1, flags=re.M)
        if k != 1: raise SystemExit(f'gegenprobe.js: Schritt {nr} nicht gefunden')
    open(gp, 'w', encoding='utf-8').write(g)
print('formulare2.py: Antwortbrief ohne Mailprogramm (PDF und Text kopieren), Mail-Adressen als Text.')
