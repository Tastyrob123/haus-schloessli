#!/usr/bin/env python3
"""Baut anleitung.html (Anleitung Das Besucherbuch · Wirtschaft am Schlössli) aus den Texten unten. Vorlage: die Anleitung des Besucherbuchs im Berghotel Gasterntal
(dort nach Doldenhorn und Carlton: elf Kapitel in vier Themen), Bild gross mit Klick und Esc, «Gut zu wissen» je Kapitel, im Kleid des Schlössli.
Bilder: node anleitung_bilder.js (anleitung/k01.jpg …). python3 anleitung_bau.py"""
import html, os, re
HIER = os.path.dirname(os.path.abspath(__file__))
# Namen der Werkzeuge nur aus dem Kleid des Hauses (_werkzeuge/oberflaeche/kleid/schloessli.js, WO_HAUS.namen, Robert 19.10.2026), nie abgetippt.
_KLEID = open(os.path.join(os.path.dirname(HIER), 'oberflaeche', 'kleid', 'schloessli.js'), encoding='utf-8').read()
def _name(k):
    m = re.search(k + r":\s*'([^']+)'", re.search(r'namen:\s*\{([^}]*)\}', _KLEID).group(1))
    return m.group(1)
NAME, STUBE = _name('besuche'), _name('zentrale')
KLEIN = re.sub(r'^(Die|Das|Der) ', lambda m: m.group(0).lower(), NAME)
THEMEN = [
 ('Grundlagen', 'So geht ' + KLEIN, [
  ('k01', 'Übersicht', 'So ist ' + KLEIN + ' aufgebaut.', NAME + ' zeigt, wer Ihre Website besucht: woher die Gäste kommen, was sie sich ansehen, wie lange sie bleiben und wie oft daraus eine Reservation wird. Sie ändern hier nichts, Sie lesen.',
   ['Links die Bereiche: «Übersicht», darunter «Besuche», «Herkunft» und «Zeit» für die Gäste, «Seiten», «Verlauf» und «Zur Reservation» für die Website, zuletzt «So wird gezählt».',
    'Unter dem Titel jeder Ansicht wählen Sie den Zeitraum: 7, 30 oder 90 Tage. Alle Zahlen der Ansicht gelten für diesen Zeitraum.',
    'Oben im Kopf stehen Titel und Stand der Ansicht, rechts der Weg zu allen Werkzeugen (' + STUBE + '), die Anleitung und «Website ansehen». Unten nennt die Leiste die Besuche von heute.',
    'Beim ersten Mal zeigt ein kleines Schild unten rechts «Kurzer Rundgang». Er lässt sich jederzeit über den Rand wieder öffnen.'],
   'Die Bilder dieser Anleitung zeigen Beispielwerte. Sie sind erfunden und im Bild so beschriftet. Ihre echten Besuche erscheinen, sobald die Website zählt.'),
  ('k02', 'Übersicht', 'Die Übersicht lesen.', 'Oben vier Zahlen: Besuche (mit dem Vergleich zum Zeitraum davor), angesehene Seiten, Minuten je Besuch und wie viele zur Reservation gingen, also im Fenster «Reservation» einen Tisch anfragten oder «Direkt buchen» wählten. Darunter die Besuche je Tag als Säulen.',
   ['Mit der Maus über eine Säule fahren: Tag und Zahl der Besuche erscheinen.',
    '«Woher die Gäste kommen» und «Am meisten angesehen» zeigen je die sechs ersten Plätze. Der Link daneben führt zur ganzen Liste.',
    'Ganz unten stehen die letzten fünf Besuche. Ein Klick öffnet den Besuch.'],
   'Ein Besuch ist ein Gast an einem Tag. Kommt derselbe Gast nach mehr als einer halben Stunde Pause wieder, zählt das als neuer Besuch.')]),
 ('Die Gäste', 'Besuche, Herkunft und Zeit', [
  ('k03', 'Besuche', 'Einen Besuch lesen.', 'Unter «Besuche» steht jeder einzelne Besuch: links die Liste nach Tagen, rechts der gewählte Besuch.',
   ['Links einen Besuch anklicken. Im Kreis steht das Land, daneben Ort, Uhrzeit, Zahl der Seiten und Dauer. Die Seite bleibt, wo sie ist, nur die Karte rechts wechselt.',
    'Rechts oben sechs Angaben: wann der Gast kam, wie lange er blieb, wie viele Seiten, mit welchem Gerät, in welcher Sprache und über welche Website er zu Ihnen fand.',
    'Darunter «Der Weg durch die Website»: Seite für Seite in der Reihenfolge des Besuchs, mit der Zeit je Seite. Unter einer Seite steht, was der Gast dort getan hat, etwa «Fenster «Reservation» geöffnet» oder «Route zum Hafen geöffnet».'],
   'Ein Name steht nie da. ' + NAME + ' kennt Ort, Uhrzeit und Weg, aber nicht, wer der Gast ist.'),
  ('k04', 'Besuche', 'Wer einen Tisch reservieren wollte.', 'Über der Liste grenzen Sie ein: alle Besuche, nur die zur Reservation, nur die mit Bankettanfrage oder einer anderen Anfrage, nur die mit Anruf oder Mail, oder nur die am Handy.',
   ['Auf «Zur Reservation» klicken. Die Liste zeigt nur noch Besuche, bei denen der Gast einen Tisch anfragte oder «Direkt buchen» wählte. Ihr Kreis ist im hellen Seeblau.',
    'Einen dieser Besuche öffnen und den Weg lesen: Welche Seiten hat der Gast vorher angesehen, wie lange, und von welcher Seite aus hat er reserviert?',
    '«Bankett oder Anfrage» zeigt, wer die Bankettanfrage geöffnet oder eine Anfrage abgeschickt hat, etwa für eine Feier oder einen Gutschein. «Anruf oder Mail» zeigt, wer die Nummer des Hauses gewählt oder die Mail-Adresse angeklickt hat, «Am Handy» die Besuche vom Telefon.'],
   'So sehen Sie, welche Seiten Gäste an den Tisch bringen. Lesen viele vor der Reservation die Karte oder die Weinkarte, lohnt es sich, gerade diese Seiten aktuell zu halten.'),
  ('k05', 'Herkunft', 'Woher die Gäste kommen.', 'Unter «Herkunft» stehen Länder und Orte, wie viele aus der Schweiz kommen, die Sprache des Browsers und das Gerät.',
   ['«Länder» und «Orte» nennt die Verbindung des Gastes. Der Ort ist der seines Anschlusses und kann einige Kilometer danebenliegen.',
    '«Gekommen über» zeigt, von welcher Website der Gast zu Ihnen fand: Google, Instagram, GaultMillau, der Guide Michelin, Tripadvisor, die Gemeinde Bottighofen oder das Schäfli. «Direkt aufgerufen» heisst: Adresse eingetippt, Lesezeichen oder Link aus einer Mail.',
    '«Sprache des Browsers» ist die Sprache, in der der Gast seinen Browser eingestellt hat (die Website selbst ist deutsch), «Gerät» unterscheidet Handy, Tablet und Rechner.'],
   'Kommen viele Besuche von der anderen Seite des Sees oder aus einem Land, dessen Sprache die Website noch nicht spricht, sehen Sie es hier zuerst.'),
  ('k06', 'Zeit', 'Wann Gäste vorbeischauen.', 'Unter «Zeit» steht, zu welcher Stunde und an welchem Wochentag die Besuche beginnen. Uhrzeit in Bottighofen.',
   ['Oben vier Spitzen: wann die meisten kommen, welcher Tag am stärksten ist, wie viele ab 18 Uhr und wie viele am Wochenende.',
    '«Zu welcher Uhrzeit» zeigt 24 Säulen, eine je Stunde. Mit der Maus darüber erscheint die Zahl.',
    '«Wochentag und Stunde» legt beides übereinander: Je dunkler ein Feld, desto mehr Besuche.'],
   'So sehen Sie, wann sich ein Beitrag, ein Hinweis auf den Lunch oder einen Anlass am ehesten lohnt: Dann sind die Gäste ohnehin auf der Seite.')]),
 ('Die Website', 'Seiten, Verlauf und Reservation', [
  ('k07', 'Seiten', 'Was am meisten angesehen wird.', 'Unter «Seiten» steht jede Seite der Website mit ihren Aufrufen, der Zeit, die Gäste im Schnitt darauf bleiben, und wie oft von dort ein Tisch angefragt oder «Direkt buchen» gewählt wurde.',
   ['Die Liste ist nach Aufrufen geordnet, die meistbesuchte Seite steht oben.',
    '«Zeit im Schnitt» zählt nur, solange die Seite im Vordergrund war. Liegt sie in einem Reiter im Hintergrund, läuft die Zeit nicht.',
    '«Zur Reservation» nennt, wie oft Gäste von dieser Seite einen Tisch anfragten oder «Direkt buchen» wählten.'],
   'Eine Seite mit vielen Aufrufen und wenig Zeit wird oft nur überflogen. Eine Seite mit wenigen Aufrufen und viel Zeit wird gelesen, aber selten gefunden.'),
  ('k08', 'Verlauf', 'Wie sich die Besuche entwickeln.', 'Unter «Verlauf» steht der gewählte Zeitraum neben dem Zeitraum davor: Geht es aufwärts oder abwärts?',
   ['Die Säulen zeigen die Besuche je Tag, dahinter hell derselbe Tag im Zeitraum davor.',
    '«Neben dem Zeitraum davor» vergleicht Besuche, Seiten, Zeit, Schritte zur Reservation, Bankett und Anfragen, Anrufe und Mails sowie die Route zum Hafen, mit dem Unterschied in Prozent.',
    '«Woche für Woche» fasst von Montag bis Sonntag zusammen, darunter die wichtigsten Länder als kleine Verlaufslinien.'],
   'Ein einzelner Tag sagt wenig. Achten Sie auf Wochen und auf die Richtung der Linien, besonders zum Start der Terrasse im Frühling und vor den Betriebsferien.'),
  ('k09', 'Zur Reservation', 'Wie oft die Website an den Tisch führt.', 'Reserviert wird im Fenster «Reservation» der Website, mit Wünschen als Anfrage ans Haus oder über «Direkt buchen» bei gastronovi. Neun Werte zeigen, wie oft ein Aufruf dahin führt: von der Startseite, von Karte und Weinkarte, über «Direkt buchen», aus dem Fenster ohne nächsten Schritt, zur Bankettanfrage, zu einer Anfrage, zu Anruf oder Mail, weiter zum Schäfli und zur Route zum Hafen.',
   ['Jeder Wert steht als Anteil in Prozent, darunter die gezählten Zahlen, also wie viele von allen Aufrufen der Karte und der Weinkarte zu einer Tisch-Anfrage oder zu «Direkt buchen» führten.',
    '«Fenster ohne nächsten Schritt» zählt, wie oft jemand das Fenster «Reservation» öffnet und weder einen Tisch anfragt noch «Direkt buchen» wählt.',
    'Darunter «Von welcher Seite reserviert wird» und «Der Weg zum Tisch» vom Besuch bis zur Anfrage oder «Direkt buchen».'],
   'Gezählt wird, dass eine Anfrage abgeschickt oder «Direkt buchen» gewählt wurde, nie ihr Inhalt. Ob danach ein Tisch reserviert wurde, sehen Sie im Eingang Ihrer Anfragen und bei gastronovi.')]),
 ('Gut zu wissen', 'Die Zählung', [
  ('k10', 'Gut zu wissen', 'Was gezählt wird und was nicht.', NAME + ' zählt so wenig wie möglich und so viel wie nötig. «So wird gezählt» im Rand sagt es in einem Blick.',
   ['Gezählt werden Seite, Zeit, Land und Ort, Gerät, Sprache des Browsers, die Herkunft (nur der Name der Website) und die Schritte zu Reservation, «Direkt buchen», Bankettanfrage, Anfrage, Telefon, Mail, Schäfli und Route.',
    'Nie gezählt werden Namen, Mailadressen, Eingaben, die Adresse der Verbindung und Cookies. Am nächsten Tag erkennt ' + KLEIN + ' denselben Gast nicht wieder.',
    'Die Daten liegen nur in Ihrem Speicher, getrennt von jedem anderen Haus, auch vom Schäfli, und werden nach 400 Tagen gelöscht.'],
   'Sobald die Zählung auf der Website läuft, steht sie auch in der Datenschutzerklärung.')])]

def e(s): return html.escape(s, quote=False)
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
  <figure class="kap__b"><button type="button" class="bild" aria-label="Bild gross ansehen: {e(titel)}"><img src="anleitung/{bild}.jpg" width="1200" height="750" decoding="async" alt="{e(NAME)}, {e(bereich)}: {e(titel)} (Beispielwerte)"></button>
    <figcaption><span>{e(NAME.lower())} / {e(bereich.lower())}</span><span>Beispielwerte · Grösser ansehen</span></figcaption></figure>
</article>''')
    inhalt.append(f'<section class="thema"><h3><small>{e(kz)}</small>{e(tz)}<em>{len(ks)} Kapitel</em></h3><ol>{"".join(zeilen)}</ol></section>')
seite = open(os.path.join(HIER, 'anleitung.vorlage.html'), encoding='utf-8').read()
seite = seite.replace('%%NAME%%', e(NAME)).replace('%%ANZAHL%%', str(n)).replace('%%INHALT%%', ''.join(inhalt)).replace('%%KAPITEL%%', '\n'.join(kapitel))
open(os.path.join(HIER, 'anleitung.html'), 'w', encoding='utf-8').write(seite)
print('anleitung.html:', n, 'Kapitel')
