"""Kleid Wirtschaft am Schlössli, zuletzt nach jedem Bau (haus.nach_bau): Reste der Vorlagen (Culinarium: Fraunces, Urbanist, /assets/schrift, /assets/bild,
/assets/zeichen; Wild Side: Prata, Hanken) werden zu den Schriften und Wegen des Hauses (Open Sans, Instrument Sans, DM Mono aus /assets/fonts, Punkt-Tapete aus
/assets/svg). Kleine Seiten laden ihre Bilder sofort (WebKit malt lazy Bilder unterhalb des Fensters in Ganzseiten-Aufnahmen nicht, Protokoll Wild Side).
Wiederholbar, ändert nur Ausgaben in werkbank/ und befund/. Bauart wie kleid_wild.py des Walk on the Wild Side (31.10.2026). Nachtbau 3.11.2026."""
import os
import re

TAUSCH = [
    ("'Fraunces'", "'Open Sans'"), ('"Fraunces"', '"Open Sans"'), ('font-family="Fraunces', 'font-family="Open Sans'), ("'Urbanist',", ''), ("'Urbanist'", "'Instrument Sans'"),
    ("'Prata'", "'Open Sans'"), ("'Hanken Grotesk'", "'Instrument Sans'"),
    ('/assets/schrift/fraunces-soft.woff2', '/assets/fonts/OpenSans-var.woff2'), ('/assets/schrift/instrument.woff2', '/assets/fonts/InstrumentSans-normal-400_600.woff2'),
    ('/assets/schrift/dmmono.woff2', '/assets/fonts/DMMono-normal-400.woff2'), ('/assets/schrift/urbanist.woff2', '/assets/fonts/InstrumentSans-normal-400_600.woff2'),
    ('fonts/fraunces-soft.woff2', 'fonts/OpenSans-var.woff2'),
    ('/assets/zeichen/tapete-dunkel.svg', '/assets/svg/tapete-a-dunkel.svg'), ('/assets/zeichen/tapete-hell.svg', '/assets/svg/tapete-a-hell.svg'),
    ('font-variation-settings:"SOFT" 100,"WONK" 0', 'font-variation-settings:normal'), ('font-variation-settings:"SOFT" 100', 'font-variation-settings:normal'),
]


def anwenden(root):
    for ordner in ('werkbank', 'befund'):
        for dp, dn, fn in os.walk(os.path.join(root, ordner)):
            for f in fn:
                if not f.endswith(('.html', '.css', '.js', '.svg')):
                    continue
                p = os.path.join(dp, f)
                try:
                    t = open(p, encoding='utf-8').read()
                except UnicodeDecodeError:
                    continue
                n = t
                for a, b in TAUSCH:
                    n = n.replace(a, b)
                n = re.sub(r'font-weight:\s*340\b', 'font-weight:400', n)
                n = re.sub(r'(font:\s*)340\b', r'\g<1>400', n)
                if f.endswith('.html') and not p.endswith(os.path.join('werkbank', 'index.html')):
                    n = n.replace(' loading="lazy"', '')
                if n != t:
                    open(p, 'w', encoding='utf-8').write(n)
    for alt in ('fraunces-soft.woff2', 'urbanist.woff2'):   # Schriften der Vorlage, die der Kit hier nicht mehr braucht
        q = os.path.join(root, 'werkbank', 'fonts', alt)
        if os.path.exists(q):
            os.remove(q)


if __name__ == '__main__':
    anwenden(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
