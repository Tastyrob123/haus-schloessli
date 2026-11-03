#!/usr/bin/env python3
"""Letzter Schritt der Oberfläche (nach rahmen.py): die Namen der Welt Landhaus (_Werkzeuge/stamm/welt.js, Welt «land») in allem, was das Team sieht.
La Réception heisst im Ruedihus «Der Gastgeber», La Maison «Die Stube», Le Bureau «Der Schreibtisch», La Carte «Die Tafel», L’Imprimerie «Die Werkstatt»,
Le Livre «Das Hausbuch», Le Registre «Das Besucherbuch». Dateinamen, Wege (reception/, maison/ …) und Kommentare im Code bleiben (Master 1: «Name je Haus
legt Robert fest; Dateinamen und Adressen bleiben»). Jede Ersetzung ist ein ganzer Satzteil mit Artikel, damit die Grammatik stimmt; jede muss treffen.
Danach darf in keiner sichtbaren Zeichenkette mehr «La Réception» stehen (rest() bricht sonst ab).
Aufruf: python3 _werkzeuge/reception/_bau/namen.py"""
import os, re, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ERS = {
 'reception.js': [
  ('<b>La Réception</b><small>', '<b>Der Gastgeber</b><small>'),
  ("|| 'La Réception')", "|| 'Der Gastgeber')"),
  ('Ich trage es dann in La Réception ein', 'Ich trage es dann im Gastgeber ein'),
 ],
 'pruefung.html': [
  ('<title>Prüfung · La Réception · Landgasthof Ruedihus</title>', '<title>Prüfung · Der Gastgeber · Landgasthof Ruedihus</title>'),
  ('<small>La Réception · Landgasthof Ruedihus</small>', '<small>Der Gastgeber · Landgasthof Ruedihus</small>'),
  ('>Zu La Réception<', '>Zum Gastgeber<'),
  ('Sie läuft auch, wenn La Réception selbst nicht startet.', 'Sie läuft auch, wenn der Gastgeber selbst nicht startet.'),
  ('Jede Meldung von La Réception beginnt', 'Jede Meldung des Gastgebers beginnt'),
 ],
 'pruefung.js': [
  ("'La Réception wurde über einen fremden Namen", "'Der Gastgeber wurde über einen fremden Namen"),
  ('Die Anfrage kam nicht von La Réception selbst', 'Die Anfrage kam nicht vom Gastgeber selbst'),
  ("'La Réception direkt öffnen", "'Den Gastgeber direkt öffnen"),
  ('Keine Anmeldung vor La Réception.', 'Keine Anmeldung vor dem Gastgeber.'),
  ('Browser kann La Réception', 'Browser kann den Gastgeber'),
 ],
 'anleitung.html': [
  ('<title>Anleitung La Réception · Landgasthof Ruedihus Kandersteg</title>', '<title>Anleitung · Der Gastgeber · Landgasthof Ruedihus Kandersteg</title>'),
  ('Schritt für Schritt durch La Réception, das Werkzeug', 'Schritt für Schritt durch den Gastgeber, das Werkzeug'),
  ('<b>Anleitung · La Réception</b>', '<b>Anleitung · Der Gastgeber</b>'),
  ('>La Réception öffnen<', '>Den Gastgeber öffnen<'),
  ('So ist <em>La Réception</em> aufgebaut.', 'So ist <em>der Gastgeber</em> aufgebaut.'),
  ('<p class="s">La Réception ist das Werkzeug', '<p class="s">Der Gastgeber ist das Werkzeug'),
  (' La Réception sieht auch von selbst nach', ' Der Gastgeber sieht auch von selbst nach'),
  ('alt="Übersicht von La Réception"', 'alt="Übersicht des Gastgebers"'),
  ('bietet La Réception zwei Wege an', 'bietet der Gastgeber zwei Wege an'),
  ('fragt La Réception einmal', 'fragt der Gastgeber einmal'),
  ('<figcaption>La Réception · ', '<figcaption>Der Gastgeber · '),
 ],
 'studio/rundgang.js': [
  ("maison: { name: 'La Maison'", "maison: { name: 'Die Stube'"), ("titel: 'Das ist La Maison'", "titel: 'Das ist die Stube'"),
  ("'Le Bureau, La Carte, L’Imprimerie, La Réception, Le Livre.", "'Der Schreibtisch, die Tafel, die Werkstatt, der Gastgeber, das Hausbuch."),
  ("bureau: { name: 'Le Bureau'", "bureau: { name: 'Der Schreibtisch'"), ("titel: 'Das ist Le Bureau'", "titel: 'Das ist der Schreibtisch'"),
  ("carte: { name: 'La Carte'", "carte: { name: 'Die Tafel'"), ("titel: 'Das ist La Carte'", "titel: 'Das ist die Tafel'"),
  ("reception: { name: 'La Réception'", "reception: { name: 'Der Gastgeber'"), ("titel: 'Das ist La Réception'", "titel: 'Das ist der Gastgeber'"),
  ("livre: { name: 'Le Livre'", "livre: { name: 'Das Hausbuch'"), ("titel: 'Das ist Le Livre'", "titel: 'Das ist das Hausbuch'"),
  ("registre: { name: 'Le Registre'", "registre: { name: 'Das Besucherbuch'"), ("titel: 'Das ist Le Registre'", "titel: 'Das ist das Besucherbuch'"),
  ('übernommen aus La Réception des Landgasthof Ruedihus', 'übernommen aus La Réception des Carlton-Europe'),
 ],
 'studio/zur-werkbank.js': [
  ('übernommen aus La Réception des Landgasthof Ruedihus', 'übernommen aus La Réception des Carlton-Europe'),
 ],
}


def rest(t, html=False):
    """Sichtbare Zeichenketten (in '…', "…", `…` oder zwischen > und <) ohne Kommentare, in denen noch ein Name der Welt Grandhotel steht."""
    ohne = re.sub(r'/\*.*?\*/|<!--.*?-->|^\s*//.*$', '', t, flags=re.S | re.M)
    return [m.group(0)[:90] for m in re.finditer(r"'[^'\n]*(La Réception|La Maison)[^'\n]*'|\"[^\"\n]*(La Réception|La Maison)[^\"\n]*\"" + (r"|>[^<]*(La Réception|La Maison)[^<]*<" if html else ''), ohne)]


if __name__ == '__main__':
    fehler = []
    for f, paare in ERS.items():
        p = os.path.join(C, f); t = open(p, encoding='utf-8').read()
        for a, b in paare:
            if t.count(a) < 1:
                sys.exit(f'ABBRUCH {f}: «{a[:70]}» nicht gefunden')
            t = t.replace(a, b)
        open(p, 'w', encoding='utf-8').write(t)
        fehler += [f'{f}: {x}' for x in rest(t, f.endswith('.html'))]
    if fehler:
        sys.exit('Noch Namen der Welt Grandhotel sichtbar:\n' + '\n'.join(fehler))
    print('Namen der Welt Landhaus gesetzt (Der Gastgeber, Die Stube …)')
