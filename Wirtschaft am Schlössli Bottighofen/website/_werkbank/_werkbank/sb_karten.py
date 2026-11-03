#!/usr/bin/env python3
"""Werkbank Wirtschaft am Schlössli, Kapitel IV «Karten und Unterlagen» (Nachtbau 3.11.2026; Bauart sb_karten.py des Culinarium, Inhalt wie im alten Schlössli-Stand).
Die fünf Karten des Hauses, neu gesetzt vom Kartenmacher (Station 10, _karten/pdf/: feste Schriften, kein Type 3), neben der heutigen Fassung (die PDFs
der heutigen Website, beim Bau aus _quelle/website/pdf/ nach _werkbank/heute/ kopiert; zur Laufzeit lädt nichts aus _quelle/).
   python3 _werkbank/sb_karten.py  → unterlagen/pdf/<ziel>.pdf, _werkbank/heute/<ziel>.pdf; _werkbank/unterlagen.json nur, solange dort noch kein Schlössli-Plan steht
   (den Plan führt Werkbank Papier, danach baut der Kit unterlagen.py die Seite)."""
import json, os, shutil

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PROJ = os.path.dirname(os.path.dirname(ROOT))
NEU = os.path.join(PROJ, '_karten', 'pdf')
QUELLE = os.path.join(PROJ, '_quelle', 'website', 'pdf')
KARTEN = [  # Ziel, heutige Fassung (Website des Hauses), Name, Gruppe, Seiten, Breite, Höhe   (aus dem alten Schlössli-Stand, unterlagen.json vom 21.10.2026)
    ('speisekarte', 'Speisekarte-Oktober.pdf', 'Die Karte nach Ländern', 'Restaurant', 2, 210, 297),
    ('lunch', 'Lunch_261019.pdf', 'Lunch-Menü', 'Restaurant', 1, 297, 210),
    ('laestermeile', 'Lastermeile-Homepage-2339.pdf', 'Lästermeile', 'Bar', 1, 210, 297),
    ('bankett', 'Bankettmenuvorschlage.pdf', 'Bankettmenüvorschläge', 'Banketts & Gruppen', 2, 210, 297),
    ('weinkarte', None, 'Weinkarte', 'Keller', 0, 210, 297),
]


def bau():
    try:   # führt Werkbank Papier den Plan (unterlagen.json, unterlagen_bau.py), bleibt alles bei ihr
        _p = json.load(open(os.path.join(W, 'unterlagen.json'), encoding='utf-8'))
        if _p and not any(str(x.get('ziel', '')).startswith('abend-') for x in _p):
            print('Karten: Plan von Werkbank Papier,', ', '.join(x['ziel'] for x in _p)); return
    except Exception:
        pass
    os.makedirs(os.path.join(ROOT, 'unterlagen', 'pdf'), exist_ok=True); os.makedirs(os.path.join(W, 'heute'), exist_ok=True)
    for d in (os.path.join(ROOT, 'unterlagen', 'pdf'), os.path.join(W, 'heute')):   # Karten des Culinarium (Abende) entfernen
        for f in os.listdir(d):
            if f.startswith('abend-') and f.endswith('.pdf'):
                os.remove(os.path.join(d, f))
    plan = []
    for ziel, alt, name, gruppe, seiten, b, h in KARTEN:
        q = os.path.join(NEU, ziel + '.pdf')
        if not os.path.exists(q):
            print('fehlt', q); continue
        shutil.copy2(q, os.path.join(ROOT, 'unterlagen', 'pdf', ziel + '.pdf'))
        heute = ''
        if alt:
            a = os.path.join(QUELLE, alt)
            if os.path.exists(a):
                shutil.copy2(a, os.path.join(W, 'heute', ziel + '.pdf'))
            if os.path.exists(os.path.join(W, 'heute', ziel + '.pdf')):
                heute = os.path.relpath(os.path.join(W, 'heute', ziel + '.pdf'), ROOT)
        plan.append(dict(ziel=ziel, quelle=heute, name=name, gruppe=gruppe, seiten=seiten, b=b, h=h, dazu='', fehlt=''))
    p = os.path.join(W, 'unterlagen.json')
    try:
        alt_plan = json.load(open(p, encoding='utf-8'))
    except Exception:
        alt_plan = []
    if not alt_plan or any(str(x.get('ziel', '')).startswith('abend-') for x in alt_plan):
        json.dump(plan, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Karten:', ', '.join(x['ziel'] for x in plan))


if __name__ == '__main__':
    bau()
