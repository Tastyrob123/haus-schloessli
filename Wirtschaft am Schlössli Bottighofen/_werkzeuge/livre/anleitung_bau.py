#!/usr/bin/env python3
"""Baut anleitung.html (Anleitung Das Hausbuch · Wirtschaft am Schlössli) aus den Texten unten und anleitung.vorlage.html (Aufbau wie die Anleitung des Le Livre im
Carlton: Bild gross mit Klick und Esc, «Gut zu wissen» je Kapitel; Inhalt nach der Anleitung des Rivage, neun Kapitel in fünf Themen), angepasst an das
Schlössli: Zeichen und Zeiger, Punkt-Tapete, Herkunft Haus/frei/KI/fremde Rechte, Vorher/Nachher, Probe-Antwort der Prüfung, Markenbuch im Werkzeug.
Bilder: node anleitung_bilder.js (anleitung/k01.jpg …, aus dem echten Werkzeug).   python3 anleitung_bau.py"""
import html, os
HIER = os.path.dirname(os.path.abspath(__file__))
THEMEN = [
 ('Grundlagen', 'So geht {N_es}', [
  ('k01', 'Übersicht', 'So ist {N_es} aufgebaut.', '{N} ist die Marke des Hauses zum Arbeiten. Drei Teile für den Alltag, dazu das Markenbuch zum Nachschlagen.',
   ['Links die Teile: «Fotos», «Logo & Dateien» und «Markenprüfung». Darunter das Markenbuch.',
    'Oben rechts stehen «Anleitung», «{zentrale}» und «Website ansehen». Unten steht immer der Hinweis zu den Bildrechten, daneben laden Sie alle Dateien der Marke auf einmal.',
    'Auf dem Handy öffnet der Knopf «Bereiche» die Teile als Menü und schliesst sich nach der Wahl.'],
   '{N} speichert nichts. Was Sie laden, landet auf Ihrem Rechner, was Sie prüfen, ist nach der Prüfung wieder weg.')]),
 ('Fotos', 'Finden, laden, Herkunft', [
  ('k02', 'Fotos', 'Ein Foto finden.', 'Alle Fotos der Website liegen unter «Fotos», jedes mit Bereich, Saison, Format und Herkunft.',
   ['Oben ins Suchfeld schreiben, zum Beispiel «Terrasse», «Tortelloni» oder «Bar».',
    'Darunter eingrenzen: Bereich, Saison, Hoch- oder Querformat und Herkunft (Fotos des Hauses, frei lizenziert, mit KI erzeugt oder mit fremden Rechten).',
    'Über der Liste steht, wie viele Fotos passen. «Filter zurücksetzen» zeigt wieder alle. Beim Scrollen kommen weitere Fotos nach.'],
   'Für einen Instagram-Beitrag eignen sich Hochformate am besten: «Hochformat» wählen, dann wird am wenigsten weggeschnitten.'),
  ('k03', 'Fotos', 'In der richtigen Grösse laden.', 'Ein Klick auf ein Foto öffnet es gross. Rechts stehen vier fertige Grössen.',
   ['«Instagram-Beitrag» (1080 × 1350) oder «Story» (1080 × 1920) mit der Maus berühren. Im Bild erscheint der Ausschnitt.',
    'Den Rahmen im Bild an die Stelle ziehen, die zu sehen sein soll. Der Knopf «Laden» nimmt genau diesen Ausschnitt.',
    '«Website» lädt das Foto mit 2000 Pixel an der längsten Seite, «Druck» in voller Auflösung. Zwei Wege öffnen das Foto direkt in {druck_in}, mit demselben Ausschnitt.',
    'Bei den nachgeschärften Fotos zeigen «Vorher», «Nachher» und «Schieber», wie das Foto geliefert wurde und wie es heute auf der Website steht.'],
   'Ist das Foto für eine Story etwas zu klein, steht im Dateinamen «hochgerechnet». Steht dort «websitegroesse», liegt kein grösseres Original vor.'),
  ('k04', 'Fotos', 'Woher ein Foto kommt.', 'Die meisten Fotos stammen vom Haus: von seiner Website, von Schweiz Tourismus und aus seinem Instagram. Einige sind frei lizenziert, etwa der Hafen und das Haus auf Wikimedia Commons. Andere gehören nicht dem Haus und stehen auf der Website nur für die Demo.',
   ['Unter «Quelle» steht, woher das Foto kommt, und ein Weg zur Quelle. Frei lizenzierte Fotos nennen den Fotografen und die Lizenz. So müssen sie auch genannt werden.',
    'Unter «Herkunft» lassen sich Fotos des Hauses, frei lizenzierte, mit KI erzeugte und solche mit fremden Rechten ein- oder ausblenden.',
    'Das eine mit KI erzeugte Bild (das Feuerwerk) trägt «KI» und einen Hinweis. Fotos mit fremden Rechten (Gäste auf Tripadvisor, Partner, das Heft der Gemeinde) tragen «Rechte»: für Werbung nur mit Erlaubnis.'],
   'Die alten Bilder aus dem Heft der Gemeinde sind mit KI nachgeschärft, das Feuerwerk mit KI neu erzeugt. «Vorher» zeigt die Vorlage.')]),
 ('Logo & Dateien', 'Dateien und Farben', [
  ('k05', 'Logo & Dateien', 'Zeichen und Logo für die Agentur.', 'Unter «Logo & Dateien» liegt alles, was eine Agentur oder eine Druckerei vom Haus braucht.',
   ['Das Zeichen und die Zeiger gibt es in Nacht, Stuhlblau, Seehimmel und Weiss, das Logo des Hauses in Nacht, Schwarz, Weiss und Seehimmel, den Namen allein in Open Sans, lang und kurz.',
    '«SVG» bleibt in jeder Grösse scharf. «PNG» hat einen durchsichtigen Grund, für Präsentationen und Office. Das Logo selbst gibt es nur als PNG, weil das Haus keinen Vektor hat.',
    'Die Punkt-Tapete liegt als Kachel bei. «Alle Dateien (ZIP)» lädt alles auf einmal, mit den Schriften.'],
   'Was mit dem Zeichen nie geschieht (drehen, verzerren, umfärben), steht im Markenbuch unter «Zeichen».'),
  ('k06', 'Logo & Dateien', 'Farbwerte kopieren.', 'Die Farben des Hauses stehen mit Namen und Rolle da: Nacht und Stuhlblau, Kalk und Papier, Seehimmel, die Schrift und Schirmrot. Ein Klick genügt.',
   ['Auf eine Farbe klicken: der Wert (zum Beispiel #0B1D3D für Nacht) liegt in der Zwischenablage.',
    'Ein Klick auf die RGB-Zeile kopiert die RGB-Werte.',
    'Darunter laden Sie die Farben als CSS, JSON oder ASE (für InDesign und Illustrator) und die Schriften als WOFF2 oder als Paket mit TTF.'],
   'Seehimmel zeichnet und schreibt nie den Lesetext. Schirmrot steht nur als Punkt, nie als Fläche.')]),
 ('Markenprüfung', 'Prüfen und lesen', [
  ('k07', 'Markenprüfung', 'Einen Entwurf prüfen.', 'Schickt eine Agentur ein Plakat, einen Flyer oder einen Beitrag, prüfen Sie hier, ob er zum Haus passt.',
   ['Den Entwurf in das Feld ziehen oder «Datei wählen». Bild (JPG, PNG, WebP) oder PDF, bis 30 MB.',
    '«Prüfen» drücken. {N} misst zuerst die Farben, dann sieht Claude sich den Entwurf an.',
    'Nach etwa einer halben Minute steht die Rückmeldung da. Unter dem leeren Feld steht schon ein Beispiel.'],
   'Solange die Prüfung durch Claude nicht eingeschaltet ist, antwortet eine Probe: die Farben sind gemessen, der Rest ist als Probe beschriftet.'),
  ('k08', 'Markenprüfung', 'Die Rückmeldung lesen.', 'Oben ein Satz, wie nah der Entwurf am Haus ist. Darunter Punkt für Punkt: Farben, Schrift, Zeichen, Abstand, Bild und Ton.',
   ['Jeder Punkt hat ein Urteil: «passt», «achten» oder «passt nicht». Was nicht passt, steht oben.',
    'Links die gemessenen Farben: wie viel der Fläche in den Farben des Hauses liegt, und welche Töne fremd sind. Diese Messung macht keine KI.',
    '«Als Text kopieren» gibt Ihnen die Rückmeldung für die Mail an die Agentur. «Ergebnis sichern» legt sie als Datei auf Ihren Rechner, nur wenn Sie es wollen.'],
   'Das Beispiel ist eigens gezeichnet. Die Farben darin sind wirklich gemessen; die Urteile zu Schrift, Zeichen, Bild und Ton sind ein Beispiel, so wie die Prüfung antwortet.')]),
 ('Nachschlagen', 'Das Markenbuch', [
  ('k09', 'Markenbuch', 'Im Markenbuch nachschlagen.', 'Das Markenbuch erklärt in acht Kapiteln, wie das Haus aussieht: Haus, Zeichen, Logo, Farben und ihre Herkunft im Foto, Schriften, Tapete, Bilder und Ton.',
   ['Links «Markenbuch» oder auf der Übersicht «Lesen» drücken.', 'Oben im Markenbuch springen Sie zu jedem Kapitel. «Als PDF sichern» legt es als PDF ab, je Kapitel eine Seite.'],
   'Die Markenprüfung prüft nach denselben Regeln. Ändert sich etwas an der Marke, wird beides zusammen neu gebaut.')])]


def e(s): return html.escape(s, quote=False)


import json
import re as _re
_kleid = open(os.path.join(os.path.dirname(HIER), 'oberflaeche', 'kleid', 'schloessli.js'), encoding='utf-8').read()
NAMEN = dict(_re.findall(r"(\w+):\s*'([^']+)'", _re.search(r'namen:\s*\{([^}]*)\}', _kleid).group(1)))   # eine Stelle: WO_HAUS.namen im Kleid
def n(s):
    """{N} Name des Werkzeugs, {N_es} klein am Satzanfang nach «So geht», {<schlüssel>} und {<schlüssel>_in} (Dativ) der Nachbarn."""
    d = lambda x: x.replace('Das ', 'dem ', 1).replace('Die ', 'der ', 1).replace('Der ', 'dem ', 1)
    s = s.replace('{N_es}', NAMEN['marke'][0].lower() + NAMEN['marke'][1:]).replace('{N}', NAMEN['marke'])
    for k, v in NAMEN.items():
        s = s.replace('{' + k + '_in}', d(v)).replace('{' + k + '}', v)
    return s
THEMEN = json.loads(n(json.dumps(THEMEN, ensure_ascii=False)))


n = 0
inhalt, kapitel = [], []
for kz, tz, ks in THEMEN:
    zeilen = []
    for (bild, bereich, titel, einl, schritte, wissen) in ks:
        n += 1; nr = '%02d' % n
        zeilen.append(f'<li><a href="#k{nr}"><b>{nr}</b><span>{e(titel)}</span><i>{e(bereich)}</i></a></li>')
        li = ''.join(f'<li><span>{i}</span><p>{e(s)}</p></li>' for i, s in enumerate(schritte, 1))
        kapitel.append(f'''<article class="kap" id="k{nr}">
  <div class="kap__t"><span class="mono">{nr} · {e(bereich)}</span><h2>{e(titel)}</h2><p class="einl">{e(einl)}</p>
    <ol class="schritte">{li}</ol>
    <p class="wissen"><b>Gut zu wissen</b>{e(wissen)}</p></div>
  <figure class="kap__b"><button type="button" class="bild" aria-label="Bild gross ansehen: {e(titel)}"><img src="anleitung/{bild}.jpg" width="1200" height="714" loading="lazy" decoding="async" alt="{e(NAMEN['marke'])}, {e(bereich)}: {e(titel)}"></button>
    <figcaption><span>{e(NAMEN['marke'].split(' ', 1)[1].lower())} / {e(bereich.lower())}</span><span>Grösser ansehen</span></figcaption></figure>
</article>''')
    inhalt.append(f'<section class="thema"><h3><small>{e(kz)}</small>{e(tz)}<em>{len(ks)} Kapitel</em></h3><ol>{"".join(zeilen)}</ol></section>')
seite = open(os.path.join(HIER, 'anleitung.vorlage.html'), encoding='utf-8').read()
seite = seite.replace('%%ANZAHL%%', str(n)).replace('%%NAME%%', NAMEN['marke']).replace('%%NAME_IN%%', 'wie ' + NAMEN['marke'][0].lower() + NAMEN['marke'][1:]).replace('%%INHALT%%', ''.join(inhalt)).replace('%%KAPITEL%%', '\n'.join(kapitel))
open(os.path.join(HIER, 'anleitung.html'), 'w', encoding='utf-8').write(seite)
print('anleitung.html:', n, 'Kapitel')
