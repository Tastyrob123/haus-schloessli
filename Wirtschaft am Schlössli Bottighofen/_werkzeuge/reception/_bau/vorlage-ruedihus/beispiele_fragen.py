#!/usr/bin/env python3
"""Schreibt gast_beispiel_fragen.json: zehn Beispielfragen für «Das wurde gefragt» des Landgasthof Ruedihus, zwei davon mit Absicht ohne Antwort
(Check-in, Kinderbett: dazu sagen die Seiten und Karten des Hauses nichts, genau dort trägt das Team nach). Die Fragen hat Tasty Studios gestellt, die
Antworten sind so geschrieben, wie der Chat aus dem Wissen antwortet (ohne KI-Kosten, Regel 54); jede Zahl einer Antwort steht in gast/gast_wissen.txt,
sonst bricht das Skript ab, und jede Lücke darf dort wirklich nicht stehen. In der Oberfläche steht «Beispiel» dabei.
gast_beispiel_nachgetragen.json bleibt leer: nie erfinden, das Team habe etwas nachgetragen (Master E10).
Vorbild: _bau/beispiele_fragen.py des Waldhotel Doldenhorn (nur gelesen).
Aufruf: python3 _werkzeuge/reception/_bau/beispiele_fragen.py"""
import json, os, re, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# so antwortet der Chat des Hauses, wenn nichts in seinen Unterlagen steht (gast_haeuser.py MUSTER['ruedihus'])
NICHT = {'de': 'Dazu steht nichts in meinen Unterlagen. Die Rezeption hilft Ihnen gerne weiter:\n- Telefon: +41 33 675 81 81\n- E-Mail: info@doldenhorn.ch',
         'en': 'There is nothing about this in my documents. The reception will be happy to help:\n- Phone: +41 33 675 81 81\n- E-mail: info@doldenhorn.ch'}
F = [  # Sprache, Frage, Antwort (None = ohne Antwort), Thema bei Lücke, vor [Tage, Stunde, Minute], Buchungsmaske
 ('de', 'Habt ihr Fondue?', 'Ja, in der Chäs- und Wystube im Parterre, zum Beispiel:\n- Walliser Tomatefondue: CHF 35.00\n- Morchelfondue mit feine Spitzmorchle: CHF 39.00\n- Trüffelfondue: CHF 48.00\nTisch reservieren: (+41) 033 675 81 81.', '', [0, 9, 12], False),
 ('en', 'When is the restaurant open?', 'The restaurant is open from 11:30 to 21:00. To reserve a table: (+41) 033 675 81 81.', '', [0, 11, 40], False),
 ('de', 'Ist die Liebeslaube am Wochenende frei?', 'Ob die Liebeslaube frei ist, zeigt die Buchungsmaske für Ihre Daten. Die Liebeslaube hat ein romantisches Himmelbett und ein Bad mit Badewanne und Dusche, für 1–2 Personen ab CHF 390.00 pro Nacht.', '', [1, 8, 20], True),
 ('de', 'Kann ich als Gast das Spa benutzen?', 'Hallenbad, Saunen und Massagen liegen im Waldhotel Doldenhorn, dem Schwesterhaus gleich gegenüber. Massagen buchen Sie direkt im Kalender des Spa, am einfachsten gleich vor der Anreise.', '', [1, 15, 5], False),
 ('fr', 'Avez-vous un menu végétarien ?', 'Oui. Dans la Egger- und Stettlerstube, le menu végétarien propose notamment une salade verte et des œufs pochés sur épinards avec une rösti au fromage. Dans la Chäs- und Wystube, la Bauernröschti (rösti sans lard, avec fromage à raboter) est végétarienne : CHF 24.00 la petite portion, CHF 29.00 la portion.', '', [1, 19, 30], False),
 ('de', 'Wie komme ich vom Bahnhof zu Ihnen?', 'Der Bahnhof Kandersteg liegt 950 m Luftlinie vom Haus. Der Bus hält an der Haltestelle «Ruedi Hus», 100 m vom Haus. Die nächsten Abfahrten stehen auf der Seite Abreise.', '', [2, 10, 15], False),
 ('en', 'What time is check-in?', None, 'Check-in', [2, 13, 45], False),
 ('de', 'Wir möchten mit 20 Personen einen Geburtstag feiern.', 'Dafür passt die Jungestube im Parterre mit 25 Sitzplätzen, «geeignet auch für Sitzungen und Familienfeste». Die Chäs- und Wystube hat 40 Sitzplätze. Einen ersten Richtpreis rechnet der Fest-Rechner auf der Seite Essen, die verbindliche Offerte schreibt Ihnen das Event-Team.', '', [3, 9, 2], False),
 ('de', 'Haben Sie ein Kinderbett für unsere Tochter?', None, 'Kinderbett', [3, 18, 25], False),
 ('de', 'Kann ich einen Gutschein verschenken?', 'Ja: ein Wertgutschein, ein Abend in der Stube oder der Gourmetaufenthalt. Sie bezahlen online, der Gutschein kommt als PDF. Der Gourmetaufenthalt kostet ab CHF 450.00 pro Person, mit 2 Übernachtungen im Ruedihus, einem rustikalen Nachtessen in der Biedermeierstube und einem Menu Gastronomique im Waldhotel Doldenhorn.', '', [4, 11, 5], False),
]
LUECKE = {'Check-in': r'check.?in|einchecken|zimmer ab \d', 'Kinderbett': r'kinderbett|babybett|gitterbett'}


def prufe():
    roh = open(os.path.join(C, 'gast', 'gast_wissen.txt'), encoding='utf-8').read()
    w = re.sub(r'\s+', ' ', roh).replace('’', '')
    fehler = [f'«{f}»: Zahl {z} nicht im Wissen' for sp, f, a, *_ in F if a for z in re.findall(r'\d+(?:[.,]\d+)?', a) if z not in w]
    fehler += [f'Lücke «{th}» steht doch im Wissen' for sp, f, a, th, *_ in F if a is None and re.search(LUECKE[th], roh, re.I)]
    if fehler:
        sys.exit('\n'.join(fehler))


if __name__ == '__main__':
    prufe()
    aus = [{'vor': vor, 'sprache': sp, 'belegt': a is not None, 'frage': f, 'antwort': a if a is not None else NICHT.get(sp, NICHT['en']), 'thema': th, 'buchung': bu}
           for sp, f, a, th, vor, bu in F]
    json.dump(aus, open(os.path.join(C, 'gast_beispiel_fragen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump([], open(os.path.join(C, 'gast_beispiel_nachgetragen.json'), 'w', encoding='utf-8'))
    print(len(aus), 'Fragen,', sum(1 for x in aus if not x['belegt']), 'ohne Antwort, jede Zahl belegt, jede Lücke echt')
