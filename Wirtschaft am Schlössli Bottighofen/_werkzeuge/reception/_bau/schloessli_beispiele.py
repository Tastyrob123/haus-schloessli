#!/usr/bin/env python3
"""Prüft die Beispiele des Reservationsbuchs der Wirtschaft am Schlössli (Nachtbau 3.11.2026): gast_beispiele.json (acht Anfragen mit Brief),
gast_beispiel_fragen.json (Fragen an den Chat, zwei mit Absicht ohne Antwort) und gast_beispiel_nachgetragen.json (leer: kein erfundener Nachtrag des Teams).
Die Gäste sind erfunden (example.com, Nummern +41 79 000 00 0x), die Angaben des Hauses nicht: jede Zahl einer Antwort und jedes Datum eines Briefs
muss im Wissen stehen (gast/gast_wissen.txt, gast/gast_umgebung.txt) oder aus der Anfrage des Gastes kommen. Dazu: Wochentag passt zum Datum,
Sie-Form, Schweizer Schreibung (ss statt ß), keine Spur eines anderen Hauses. Bricht mit Fehlerliste ab, sonst «alles belegt».
Aufruf: python3 _werkzeuge/reception/_bau/schloessli_beispiele.py"""
import datetime, json, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
WISSEN = open(os.path.join(C, 'gast', 'gast_wissen.txt'), encoding='utf-8').read() + open(os.path.join(C, 'gast', 'gast_umgebung.txt'), encoding='utf-8').read()
MON = {m: i for i, m in enumerate(('januar', 'februar', 'märz', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'dezember'), 1)}
TAG = {'mo': 0, 'di': 1, 'mi': 2, 'do': 3, 'fr': 4, 'sa': 5, 'so': 6, 'montag': 0, 'dienstag': 1, 'mittwoch': 2, 'donnerstag': 3, 'freitag': 4, 'samstag': 5, 'sonntag': 6}
FREMD = re.compile(r'culinarium|rudi|momo|derya|hannover|linden|wild side|warteliste|haasemann|tafel', re.I)
DU = re.compile(r'\b(du|dein\w*|dich|dir|euch|euer\w*)\b', re.I)
fehler = []


def wochentage(t, wo):
    for m in re.finditer(r'\b(Mo|Di|Mi|Do|Fr|Sa|So|Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag),? (\d{1,2})\. ([A-Za-zäöü]+)(?: (\d{4}))?', t):
        jahr = int(m[4] or (2027 if m[3].lower() in ('januar', 'februar') else 2026))
        if m[3].lower() in MON and datetime.date(jahr, MON[m[3].lower()], int(m[2])).weekday() != TAG[m[1].lower()]:
            fehler.append(f'{wo}: «{m[0]}» ist kein {m[1]}')


anfragen = json.load(open(os.path.join(C, 'gast_beispiele.json'), encoding='utf-8'))
for a in anfragen:
    wo = 'Anfrage ' + a['name']
    alles = json.dumps(a, ensure_ascii=False)
    if 'ß' in alles.replace('Süßsaures', ''):
        fehler.append(f'{wo}: ß statt ss')
    if FREMD.search(alles):
        fehler.append(f'{wo}: fremdes Haus «{FREMD.search(alles)[0]}»')
    if '@' in a['kontakt'] and not a['kontakt'].endswith('@example.com'):
        fehler.append(f'{wo}: Kontakt nicht erfunden')
    wochentage(alles, wo)
    gast = ' '.join([a.get('nachricht') or '', a.get('anliegen') or '', a.get('datum') or '', a.get('uhrzeit') or ''] + [t for _, t in a.get('verlauf') or []])
    text = (a.get('text') or '') + '\n' + (a.get('betreff') or '')
    if a.get('sprache') == 'de' and DU.search(text):
        fehler.append(f'{wo}: Du-Form im Brief «{DU.search(text)[0]}»')
    for z in re.findall(r'\d+(?:[.:]\d+)?', text):
        if z not in WISSEN and z not in gast and z not in ('2026', '2027'):
            fehler.append(f'{wo}: Zahl {z} steht weder im Wissen noch in der Anfrage')

fragen = json.load(open(os.path.join(C, 'gast_beispiel_fragen.json'), encoding='utf-8'))
for f in fragen:
    wo = 'Frage «' + f['frage'][:40] + '»'
    if 'ß' in f['antwort']:
        fehler.append(f'{wo}: ß statt ss')
    if f['sprache'] == 'de' and DU.search(f['antwort']):
        fehler.append(f'{wo}: Du-Form in der Antwort')
    wochentage(f['frage'] + ' ' + f['antwort'], wo)
    if f.get('belegt'):
        for z in re.findall(r'\d+(?:[.:]\d+)?', f['antwort']):
            if z not in WISSEN and z not in f['frage']:
                fehler.append(f'{wo}: Zahl {z} nicht im Wissen')
if json.load(open(os.path.join(C, 'gast_beispiel_nachgetragen.json'), encoding='utf-8')):
    fehler.append('gast_beispiel_nachgetragen.json: erfundene Nachträge des Teams')
if fehler:
    print('\n'.join(fehler)); sys.exit(1)
print(f'{len(anfragen)} Anfragen, {len(fragen)} Fragen: alles belegt')
