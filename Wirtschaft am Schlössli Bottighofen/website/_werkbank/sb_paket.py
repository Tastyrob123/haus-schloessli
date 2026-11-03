#!/usr/bin/env python3
"""Pakete der Stationen 11 (werkbank.json) und 13 (beigaben.json) für die Kette, aus dem gebauten Stand gezählt (19.10.2026).
   python3 _werkbank/sb_paket.py"""
import json, os, urllib.parse, urllib.request

W = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(W); PROJEKT = os.path.dirname(ROOT)
K = os.path.join(PROJEKT, '_kette')
KARTE = 'http://127.0.0.1:8978/haus/' + urllib.parse.quote('Wirtschaft am Schlössli Bottighofen') + '/website/'
TEIL = [('zentrale', 'La Maison / Die Stube'), ('website', 'Le Bureau / Der Schreibtisch'), ('karten', 'La Carte / Die Tafel'), ('gaeste', 'La Réception / Der Gastgeber'),
        ('marke', 'Le Livre / Das Hausbuch'), ('besuche', 'Le Registre / Das Besucherbuch'), ('druck', 'L’Imprimerie / Die Werkstatt')]


def da(weg):
    try:
        return urllib.request.urlopen(weg if weg.startswith('http') else 'http://127.0.0.1:8982/' + weg, timeout=8).status == 200
    except Exception:
        return False


def main():
    st = {t: json.load(open(os.path.join(K, '11-werkbank', 'werkzeuge', t, 'stand.json'), encoding='utf-8')) for t, _ in TEIL}
    stuecke = [dict(name='Potentialanalyse', da=da('potenzialanalyse/index.html'), ziel=KARTE + 'potenzialanalyse/index.html', werkbank='#k1'),
               dict(name='Angebot (Angebots-Ebene, Vorschlag folgt nach 15c)', da=True, ziel=KARTE + 'werkbank/#k8', werkbank='#k8'),
               dict(name='Markenbuch und Designidentität', da=True, ziel=KARTE + 'werkbank/#k2', werkbank='#k2'),
               dict(name='Website (Seiten zum Durchklicken)', da=da('werkbank/index.html'), ziel=KARTE + 'werkbank/#seiten', werkbank='#seiten')]
    for t, n in TEIL:
        stuecke.append(dict(name=n, da=st[t].get('zustand') in ('liegt vor', 'bestätigt') and bool(st[t].get('adresse')), ziel=st[t].get('adresse'), werkbank='#k5', zustand=st[t].get('zustand')))
    stuecke.append(dict(name='Beigaben', da=True, ziel=KARTE + 'werkbank/#k6', werkbank='#k6'))
    fehlt = [s['name'] for s in stuecke if not s['da']]
    json.dump(dict(stuecke=stuecke, port=8982, adresse=KARTE + 'werkbank/', fehlt=fehlt), open(os.path.join(K, '11-werkbank', 'werkbank.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    pp = json.load(open(os.path.join(W, 'papier_plan.json'), encoding='utf-8'))
    bg = [dict(name='Karten, neu gesetzt (Unterlagen)', datei='unterlagen/index.html', knopf='#k4 «Unterlagen durchblättern»', ziel=KARTE + 'unterlagen/', geprueft=da('unterlagen/index.html')),
          dict(name=f'Drucksachen ({len(pp["druck"])}: ' + ', '.join(d['name'] for d in pp['druck']) + ')', datei='drucksachen/index.html', knopf='#k6 Papier', ziel=KARTE + 'drucksachen/', geprueft=da('drucksachen/index.html')),
          dict(name=f'Untersetzer der Lästermeile ({len(pp["etiketten"])}, Gegenstück zum Sticker)', datei='untersetzer/index.html', knopf='#k6 Papier', ziel=KARTE + 'untersetzer/', geprueft=da('untersetzer/index.html')),
          dict(name='Mailvorlagen (3, nur Text, nicht verschickt)', datei='mails/index.html', knopf='#k6 Papier, dritte Karte', ziel=KARTE + 'mails/', geprueft=da('mails/index.html')),
          dict(name='Instagram-Feed als Handy-Vorschau (Feed-Planer-Chat)', datei='feed/index.html', knopf='#k6 Feed', ziel=KARTE + 'feed/', geprueft=da('feed/index.html')),
          dict(name='Dateien (Material-Ordner, lokal; Drive erst auf Roberts Wort)', datei='material/index.html', knopf='#k6 Dateien', ziel=KARTE + 'material/', geprueft=da('material/index.html')),
          dict(name='Potentialanalyse als Kopie neben der Website', datei='potenzialanalyse/index.html', knopf='#k1 «Die ganze Analyse ansehen»', ziel=KARTE + 'potenzialanalyse/', geprueft=da('potenzialanalyse/index.html')),
          dict(name='Prüfbericht in Alltagssprache', datei='werkbank/geprueft/index.html', knopf='#k7', ziel=KARTE + 'werkbank/geprueft/', geprueft=da('werkbank/geprueft/index.html')),
          dict(name='Studio und Anleitung', datei=None, knopf='als nächster Schritt (Werkzeuge im Laptop)', ziel=None, geprueft=False)]
    os.makedirs(os.path.join(K, '13-beigaben'), exist_ok=True)
    json.dump(bg, open(os.path.join(K, '13-beigaben', 'beigaben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('fehlt in der Werkbank:', fehlt)
    print('Beigaben:', [(b['name'][:30], b['geprueft']) for b in bg])


if __name__ == '__main__':
    main()
