#!/usr/bin/env python3
"""Achter Schritt nach namen.py (Prüf-Chat 17.10.2026, Auftrag Oberchef nach Roberts Wort «keine Mails, sondern überall Formulare»):
«Abteilung fragen» unter «Das weiss der Chat» öffnete das Mailprogramm (location.href = mailto:…). Beim Doldenhorn ging so in einem Prüflauf
Apple Mail auf Roberts Bildschirm auf, beim Ruedihus ebenso (Firefox, 17.10. 15:21). Jetzt bleibt die Frage im Werkzeug: Thema, Abteilung und
Absender stehen unter «Offen bei Ihrem Team» und werden dort mit «Antwort eintragen» beantwortet. Kein Mailprogramm, nichts verschickt.
Jede Ersetzung muss genau einmal treffen, sonst bricht das Skript ab.   Aufruf: python3 _werkzeuge/reception/_bau/formulare.py"""
import os, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ers(t, alt, neu, n=1):
    if t.count(alt) != n:
        sys.exit(f'ABBRUCH: «{alt[:80]}» kommt {t.count(alt)}× vor, erwartet {n}×')
    return t.replace(alt, neu)


p = os.path.join(C, 'reception.js')
t = open(p, encoding='utf-8').read()
t = ers(t, "   Selbst eintragen, oder die zuständige Abteilung per Mail fragen (das Mailprogramm öffnet sich, verschickt wird nur, was das Team selbst schickt); das Thema steht dann oben als offen. */",
        "   Selbst eintragen, oder die zuständige Abteilung fragen: die Frage bleibt im Werkzeug unter «Offen bei Ihrem Team» (Thema, Abteilung, wer gefragt hat)\n   und wird dort beantwortet. Kein Mailprogramm (Robert 17.10.2026: keine Mails, sondern Formulare). */")
t = ers(t, "        <p>Die Frage öffnet sich als Mail in Ihrem Mailprogramm. Hier bleibt «${esc(thema)}» als offen stehen, bis die Antwort eingetragen ist.</p>",
        "        <p>«${esc(thema)}» kommt oben unter «Offen bei Ihrem Team», mit der Abteilung und Ihrem Namen. Wer die Antwort weiss, trägt sie dort ein, ab dann antwortet der Chat damit.</p>")
t = ers(t, '<button class="kn kn--linie" type="button" id="fe-frag">Mail vorbereiten<i>${SYM.post}</i></button>',
        '<button class="kn kn--linie" type="button" id="fe-frag">Bei der Abteilung als offen vermerken<i>${PF}</i></button>')
t = ers(t, "      const [an, mail] = ABTEILUNG[+$('#fe-an').value];\n", "      const [an] = ABTEILUNG[+$('#fe-an').value];\n")
t = ers(t, "      const text = `Grüezi\\n\\nGäste fragen im Chat der Website nach «${thema}». Dazu steht noch nichts im Wissen des Chats.\\n\\nKönnen Sie mir kurz schreiben, was Gäste dazu wissen sollen (Regeln, Preise, Zeiten, Ausnahmen)? Ich trage es dann im Gastgeber ein, ab dann antwortet der Chat damit.\\n\\nDanke und herzliche Grüsse\\n${von}`;\n", "")
t = ers(t, "      location.href = `mailto:${mail}?subject=${encodeURIComponent('Frage für den Chat: ' + thema)}&body=${encodeURIComponent(text)}`;\n", "")
t = ers(t, "quit('Als offen vermerkt', `«${thema}» steht oben, bis die Antwort eingetragen ist.`, [], false, 5000);",
        "quit('Als offen vermerkt', `«${thema}» steht oben unter «Offen bei Ihrem Team» (${an}), bis die Antwort eingetragen ist.`, [], false, 5000);")
open(p, 'w', encoding='utf-8').write(t)

p = os.path.join(C, 'anleitung.html')
t = open(p, encoding='utf-8').read()
t = ers(t, "bietet der Gastgeber zwei Wege an: selbst eintragen, oder die zuständige Abteilung per Mail fragen. Das Thema steht dann oben als «Offen bei Ihrem Team», bis die Antwort eingetragen ist.",
        "bietet der Gastgeber zwei Wege an: selbst eintragen, oder bei der zuständigen Abteilung als offen vermerken. Das Thema steht dann oben unter «Offen bei Ihrem Team» mit Abteilung und Namen; wer die Antwort weiss, trägt sie dort mit «Antwort eintragen» ein. Es öffnet sich kein Mailprogramm.")
open(p, 'w', encoding='utf-8').write(t)
print('Abteilung fragen ohne Mailprogramm')
