#!/usr/bin/env python3
"""Rücksprung (Robert 1.11.2026): Zurück im Browser landet auf der alten Höhe, nie ganz oben.
Setzt ruecksprung.js als <script id="ruecksprung"> vor </body> in jede HTML-Seite der Werkbank-Ordner; wiederholbar (ersetzt den alten Block).
    python3 ruecksprung.py <Projektordner>        (der Ordner mit werkbank/, feed/, mails/ … – bei Häusern mit website/_werkbank/ dieser)
Seiten mit eigenem Rückweg (#rh-zurueck) bekommen nichts, ausser der Rückweg trägt data-rs (überlässt Zurück/Vor dem Rücksprung). Meldet Seiten, die selbst nach oben springen (scrollTo(0,0) oder scrollRestoration)."""
import os, re, sys

ORDNER = ('werkbank', 'befund', 'unterlagen', 'drucksachen', 'untersetzer', 'sticker', 'postkarten', 'beigaben', 'feed', 'mails', 'material')
HIER = os.path.dirname(os.path.abspath(__file__))
EIGEN = re.compile(r'<script id="rh-zurueck"(?![^>]*\bdata-rs\b)[^>]*>')   # eigener Rückweg, der Zurück/Vor selbst macht
BLOCK = re.compile(r'<script id="ruecksprung">.*?</script>\n?', re.S)
OBEN = re.compile(r'(?:window\.|(?<![\w.]))scrollTo\(\s*(?:0\s*,\s*0|\{\s*top\s*:\s*0)|scrollRestoration|(?:documentElement|body|scrollingElement)\.scrollTop\s*=\s*0\b')


def skript():
    js = open(os.path.join(HIER, 'ruecksprung.js'), encoding='utf-8').read().strip()
    return '<script id="ruecksprung">' + js + '</script>\n'


def seite(t, s=None):
    """Eine Seite: alten Block weg, neuen vor das letzte </body> (nicht bei eigenem Rückweg #rh-zurueck)."""
    if '</body>' not in t:
        return t
    t = BLOCK.sub('', t)
    if EIGEN.search(t):
        return t
    i = t.rfind('</body>')
    return t[:i] + (s or skript()) + t[i:]


def gehoert_dazu(projekt, pfad):
    """Liegt pfad als Seite in einem Werkbank-Ordner (keine _-Dateien, keine _-Ordner)?"""
    r = os.path.relpath(os.path.abspath(pfad), os.path.abspath(projekt)).split(os.sep)
    return (len(r) >= 2 and r[0] in ORDNER and r[-1].endswith('.html')
            and not any(x.startswith(('_', '.')) for x in r) and not r[-1].startswith('_'))


def einsetzen(projekt, still=False):
    if 'beau-rivage' in os.path.abspath(projekt).lower():   # Grand Beau-Rivage nie anfassen
        print('Rücksprung: Grand Beau-Rivage wird nicht angefasst'); return 0
    s, n, frei, hinweis = skript(), 0, 0, []
    for o in ORDNER:
        for wurzel, dirs, dateien in os.walk(os.path.join(projekt, o)):
            dirs[:] = [d for d in dirs if not d.startswith(('_', '.')) and d not in ('img', 'bilder', 'fonts', 'assets')]
            for f in dateien:
                if not f.endswith('.html') or f.startswith('_'):
                    continue
                p = os.path.join(wurzel, f)
                t = open(p, encoding='utf-8').read()
                if '</body>' not in t:
                    continue
                alt = t
                t = seite(t, s)
                if EIGEN.search(t):
                    frei += 1
                elif OBEN.search(BLOCK.sub('', t)):
                    hinweis.append(os.path.relpath(p, projekt))
                if t != alt:
                    open(p, 'w', encoding='utf-8').write(t)
                    n += 1
    if not still:
        print(f'Rücksprung: {n} Seiten geändert, {frei} mit eigenem Rückweg ausgelassen')
        for h in hinweis:
            print('  prüfen (springt die Seite selbst nach oben?):', h)
    return n


if __name__ == '__main__':
    einsetzen(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.'))
