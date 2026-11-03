#!/usr/bin/env python3
"""Impressum und Datenschutz für die eigenen Seiten von Tasty Studios zur Wirtschaft am Schlössli («Alles auf einen Blick», Prüfbericht, KI-Seite).
Vorlage: dh_impressum.py des Waldhotel Doldenhorn (dort aus impressum.py des Carlton-Europe), nur gelesen und kopiert; Wortlaut wie
Familie Maeder — Vier Häuser/impressum.html; keine Mail- und Telefon-Links (Robert 17.10.2026: nichts öffnet ein Mailprogramm), die Adressen stehen als Text.
Kleid des Schlössli über das Kleid der Werkbank (Nachtbau 3.11.2026, Vorlage Culinarium)."""

# Impressum und Datenschutz für die eigenen Seiten (17.10.2026): Wortlaut wie Familie Maeder — Vier Häuser/impressum.html (dort wie legal.html der Seite
# von Tasty Studios), Punkt 2, 6 und 7 für das, was diese Seiten zusätzlich tun (Werkzeuge zum Ausprobieren, Rezeption im Chat). Verlinkt aus dem Fuss
# der Werkbank, des Prüfberichts, der Beigaben-Seiten (papier_seiten.py, unterlagen.py, feed.py, mails_bau.py, material.py) und der Potenzialanalyse (eigene Kopie).
import rh_werkzeuge as _WK
_NAMEN = [w[1] for w in _WK.WERKZEUGE]
IMPRESSUM = [
    ('Impressum', [
        ('Angaben gemäß § 5 DDG', 'Robert Reff<br>TastyRob Commerce (Einzelunternehmen)<br>Barmbeker Straße 26c<br>22303 Hamburg<br>Deutschland'),
        ('Kontakt', 'Telefon: +49 173 7230530<br>E-Mail: robert@tasty-studios.de'),
        ('Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV', 'Robert Reff, Anschrift wie oben.'),
        ('EU-Streitschlichtung', 'Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener">https://ec.europa.eu/consumers/odr/</a>. Die E-Mail-Adresse steht oben im Impressum.'),
        ('Verbraucherstreitbeilegung', 'Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.'),
        ('Hinweis zum gezeigten Entwurf', 'Die hier gezeigte Website, die Werkzeuge, Unterlagen und Ideen sind Entwürfe von Tasty Studios und nicht die offizielle Website der Wirtschaft am Schlössli. Fotos, Zeichen und Texte gehören der Wirtschaft am Schlössli und den jeweiligen Fotografen.')]),
    ('Datenschutz', [
        ('1. Verantwortlicher', 'Robert Reff, TastyRob Commerce, Barmbeker Straße 26c, 22303 Hamburg, Deutschland. E-Mail: robert@tasty-studios.de'),
        ('2. Das Wichtigste in Kürze', 'Diese Seiten zeigen einen Entwurf für die Wirtschaft am Schlössli. Sie enthalten keine Werbung. Schriften und Bilder liegen auf dem eigenen Server; es werden keine Schriftarten von Google oder anderen Drittanbietern nachgeladen. Keine dieser Seiten verschickt etwas in Ihrem Namen.'),
        ('3. Hosting und Server-Logfiles', 'Die Seiten werden bei Vercel Inc., 340 S Lemon Ave #4133, Walnut, CA 91789, USA, gehostet. Beim Aufruf verarbeitet der Hoster technisch notwendige Daten, die Ihr Browser übermittelt (IP-Adresse, Datum und Uhrzeit des Zugriffs, aufgerufene Datei, Browsertyp und Betriebssystem). Diese Daten sind für die Auslieferung der Seiten technisch erforderlich und werden nicht mit anderen Datenquellen zusammengeführt. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der technisch fehlerfreien Bereitstellung der Seiten). Vercel verarbeitet Daten teils in den USA; die Übermittlung stützt sich auf die EU-Standardvertragsklauseln sowie das EU-US Data Privacy Framework, unter dem Vercel zertifiziert ist.'),
        ('4. Zählung der Aufrufe', 'Bei jedem Seitenaufruf meldet Ihr Browser den Pfad der Seite und die Geräteart (Handy, Tablet oder Rechner) an einen eigenen Dienst, der ebenfalls bei Vercel liegt. Gespeichert werden der Zeitpunkt, Land und Ort, wie sie sich aus der Verbindung ergeben, die Seite, die Geräteart und eine Kurzkennung, die täglich wechselt. Die IP-Adresse selbst wird nicht gespeichert, es gibt kein Cookie und keine Kennung über den Tag hinaus. Zweck ist zu sehen, ob und welche Teile des Entwurfs angesehen werden. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO.'),
        ('5. Kontakt per E-Mail oder Telefon', 'Wenn Sie mir schreiben oder mich anrufen, verarbeite ich die von Ihnen übermittelten Daten (Name, E-Mail-Adresse oder Telefonnummer, Inhalt der Nachricht), um Ihre Anfrage zu beantworten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, soweit Ihre Anfrage auf einen Vertrag zielt, im Übrigen Art. 6 Abs. 1 lit. f DSGVO. Die Daten bleiben gespeichert, solange es für die Bearbeitung und mögliche Anschlussfragen nötig ist; gesetzliche Aufbewahrungspflichten bleiben unberührt.'),
        ('6. Werkzeuge zum Ausprobieren', 'Die Werkzeuge des Entwurfs (' + ', '.join(_NAMEN) + ') lassen sich hier ohne Anmeldung bedienen. ' + _WK.NAMEN['bureau'] + ' legt dafür ein technisch notwendiges Cookie für Ihren eigenen Probe-Entwurf ab; die echte Website ändert sich dabei nicht. Was Sie in den Werkzeugen eintragen, wird nur zur Vorführung verarbeitet und bei Vercel gespeichert, ' + _WK.NAMEN['imprimerie'] + ' speichert in Ihrem eigenen Browser. ' + _WK.NAMEN['registre'] + ' zeigt Beispielwerte. Bitte tragen Sie dort keine personenbezogenen Daten ein. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO.'),
        ('7. Der Chat für Ihre Gäste', 'Das Werkzeug für die Gäste enthält einen Chat zum Ausprobieren. Ihre Frage wird zur Beantwortung an den Anbieter des Sprachmodells (Anthropic PBC, USA) übermittelt; die Fragen werden ohne E-Mail-Adressen und Telefonnummern gespeichert, damit das Team sieht, was gefragt wurde. Bitte geben Sie im Chat keine Karten-, Pass- oder Gesundheitsdaten ein. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO.'),
        ('8. Ihre Rechte', 'Sie haben nach der DSGVO das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen Verarbeitungen auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO (Art. 21). Dazu reicht eine formlose E-Mail an die oben genannte Adresse. Außerdem haben Sie das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren; zuständig für Hamburg ist der Hamburgische Beauftragte für Datenschutz und Informationsfreiheit.'),
        ('Stand', 'Oktober 2026')]),
]


def impressum_html(css, zurueck, zurueck_text='Zurück zur Übersicht'):
    """Impressum und Datenschutz als eigene Seite; css und zurueck relativ zum Ort der Seite."""
    teile = ''.join(f'<section class="ip-a" aria-label="{t}"><h2>{t}</h2>' + ''.join(f'<p class="ip-k">{k}</p><p>{x}</p>' for k, x in z) + '</section>' for t, z in IMPRESSUM)
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Impressum und Datenschutz · Tasty Studios</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0b1d3d">
<style>
:root{{--nacht:#0b1d3d;--papier:#e7ecf3;--tinte:#041023;--taupe:#0f3678;--gold:#a2b6cf}}
@font-face{{font-family:'Titel OS';src:url({css}assets/fonts/OpenSans-var.woff2) format('woff2');font-weight:300 800;font-display:swap}}
@font-face{{font-family:'Instrument CE';src:url({css}assets/fonts/InstrumentSans-normal-400_600.woff2) format('woff2');font-weight:400 600;font-display:swap}}
html{{background:var(--papier)}}body{{margin:0;color:var(--tinte);font:400 17px/1.62 'Instrument CE',system-ui,sans-serif}}
.ip-s{{max-width:760px;margin:0 auto;padding:clamp(40px,7vw,96px) 16px clamp(60px,9vw,120px)}}
.ip-z{{display:inline-flex;gap:8px;color:var(--taupe);text-decoration:none;font-size:15px}}.ip-z:hover{{color:var(--tinte)}}
h1{{font:400 clamp(1.7rem,3.6vw,2.8rem)/1.15 'Titel OS',Arial,sans-serif;text-transform:uppercase;letter-spacing:.12em;margin:28px 0 8px;text-wrap:balance}}
h2{{font:400 clamp(1.1rem,2vw,1.45rem)/1.25 'Titel OS',Arial,sans-serif;text-transform:uppercase;letter-spacing:.12em;margin:44px 0 6px;padding-top:28px;border-top:1px solid rgba(4,16,35,.16)}}
.ip-k{{margin:22px 0 2px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--taupe)}}
p{{margin:0}}a{{color:var(--tinte)}}
</style>
</head>
<body>
<main class="ip-s">
  <a class="ip-z" href="{zurueck}"><span aria-hidden="true">←</span> {zurueck_text}</a>
  <h1>Impressum und Datenschutz</h1>
  {teile}
</main>
</body>
</html>
'''
