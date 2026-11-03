#!/usr/bin/env python3
"""Zweiter Schritt nach portiere.py: setzt in reception.js die Inhalte des Landgasthof Ruedihus ein (Name, Adresse, Fotos, Abteilungen, Beispielfragen, Wege).
Vorbild: _bau/doldenhorn.py des Waldhotel Doldenhorn und _bau/carlton.py des Carlton-Europe (beide nur gelesen). Jede Ersetzung muss genau so oft treffen
wie angegeben, sonst bricht das Skript ab (nichts bleibt halb übertragen).

Belege der Hauswerte (aus den Seiten und Mails des Hauses gelesen, 17.10.2026):
  Name, Adresse, Telefon, Mail: Fuss jeder Seite («Landgasthof Ruedihus · Hinder de Büele 6 · 3718 Kandersteg · (+41) 033 675 81 81 · info@doldenhorn.ch», index.html)
  Zeile: «Kandersteg · seit 1753» (Kopf der Mails mails/01-tisch, 02-anreise, 03-gutschein; Titel index.html)
  Abteilungen: info@ (Rezeption, jede Seite), event@ (Fest-Rechner essen.html «mail»), jobs@ (Stellen, haus.html). Ein eigenes Spa-Team hat das Ruedihus nicht:
  Hallenbad, Saunen und Massagen liegen im Waldhotel Doldenhorn gegenüber (haus.html «Spa im Nachbarhaus», anreise.html «Ein Termin im Spa»).
  Fotos: assets/img/<name>-s|m|l.webp, Beschreibung in assets/img/manifest.json («was»).
  Namen der Werkzeuge: Welt Landhaus (_Werkzeuge/stamm/welt.js): La Réception = Der Gastgeber, La Maison = Die Stube.
Aufruf: python3 _werkzeuge/reception/_bau/ruedihus.py"""
import os, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(C, 'reception.js')
t = open(p, encoding='utf-8').read()


def ers(alt, neu, n=1):
    global t
    if t.count(alt) != n:
        sys.exit(f'ABBRUCH: «{alt[:70]}» kommt {t.count(alt)}× vor, erwartet {n}×')
    t = t.replace(alt, neu)


def block(anfang, neu, ende='};'):
    """Ersetzt eine Konstante vom Anfang bis zum Ende (die Werte des Rivage stehen nur dort)."""
    global t
    a = t.index(anfang); b = t.index(ende, a) + len(ende)
    t = t[:a] + neu + t[b:]


ers('La Réception · Grand Beau-Rivage. Das Werkzeug', 'Der Gastgeber (La Réception) · Landgasthof Ruedihus. Das Werkzeug')
# Zeichen: das Zeichen des Hauses (assets/logo/zeichen.svg, von der Karte des Hauses nachgezeichnet) in Gold, als Bild in _werkzeuge/reception/zeichen-gold.svg
ers("const ZEICHEN = '<img src=\"../assets/logo/zeichen-gold.webp\" width=\"784\" height=\"777\" alt=\"\">';",
    "const ZEICHEN = '<img src=\"zeichen-gold.svg\" width=\"312\" height=\"418\" alt=\"\">';")
# Arten: das Ruedihus nimmt zusätzlich Gutscheine an (haus.html «Gutschein anfragen», Mail 03-gutschein); Sitzungen in der Jungestube (essen.html)
ers("const ART = { zimmer: 'Zimmer', tisch: 'Tisch', feier: 'Feier', tagung: 'Tagung', spa: 'Spa', aufenthalt: 'Aufenthalt', programm: 'Ausflug', nachricht: 'Nachricht' };",
    "const ART = { zimmer: 'Zimmer', tisch: 'Tisch', feier: 'Fest', tagung: 'Sitzung', gutschein: 'Gutschein', spa: 'Spa', aufenthalt: 'Aufenthalt', programm: 'Ausflug', nachricht: 'Nachricht' };")
ers("const ART_LANG = { zimmer: 'Zimmer & Suiten', tisch: 'Tisch im Restaurant', feier: 'Feier & Hochzeit', tagung: 'Tagung & Seminar', spa: 'Termin im Spa', aufenthalt: 'Anreise & Abreise', programm: 'Ausflüge & Programm', nachricht: 'Nachrichten' };",
    "const ART_LANG = { zimmer: 'Zimmer', tisch: 'Tisch in der Stube', feier: 'Feste im Haus', tagung: 'Sitzung in der Jungestube', gutschein: 'Geschenkgutschein', spa: 'Spa im Nachbarhaus', aufenthalt: 'Anreise & Abreise', programm: 'Rund um Kandersteg', nachricht: 'Nachrichten' };")
ers("const ARTBILD = { zimmer: 'z-fluss-s', tisch: 'bar-teatime-s', feier: 'saal-bankett-s', tagung: 'raum-jungfrau-s', spa: 'spa-massage-s', aufenthalt: 'haus-vorfahrt-s', programm: 'aus-first-steg-s', nachricht: 'halle-s' };",
    "const ARTBILD = { zimmer: 'z-himmelbett-s', tisch: 'stube-kerze-s', feier: 'fest-tafel-s', tagung: 'stube-lang-s', gutschein: 'kaffee-s', spa: 'spa-s', aufenthalt: 'haus-fassade-s', programm: 'haus-wiese-s', nachricht: 'stube-tuer-s' };")
ers('<small>Gäste im Chat · Grand Beau-Rivage</small>', '<small>Gäste im Chat · Landgasthof Ruedihus</small>')
ers("kopf('La Réception · Grand Beau-Rivage Interlaken'", "kopf('Der Gastgeber · Landgasthof Ruedihus Kandersteg'")
# Themen von «Das wurde gefragt» (reception.py THEMEN, server_teil.py) mit Foto je Thema
block("const THEMABILD = {", """const THEMABILD = { 'Essen & Stuben': 'stube-kerze-s', 'Zimmer & Buchung': 'z-himmelbett-s', 'Feste im Haus': 'fest-tafel-s', 'Spa im Nachbarhaus': 'spa-s',
  'Gutscheine': 'kaffee-s', 'Anreise & Abreise': 'haus-fassade-s', 'Ausflüge & Region': 'haus-wiese-s', 'Hund': 'balkon-s', 'Stellen': 'stube-tuer-s' };""")
t = t.replace('src="../assets/', 'src="../../assets/')
t = t.replace('../werkbank/anleitung/rezeption/', 'anleitung.html')
ers('<a href="../index.html" target="_blank" rel="noopener">Chat auf der Website${PF}</a>', '<a href="../../index.html" target="_blank" rel="noopener">Chat auf der Website${PF}</a>\n      <a href="../../mappe.html" target="_blank" rel="noopener">Zimmermappe${PF}</a>')
ers('<a href="../rezeption/" target="_blank" rel="noopener">So arbeitet der Chat${PF}</a>', '<a href="../../rezeption/" target="_blank" rel="noopener">So arbeitet der Chat${PF}</a>')
# Die Stube (La Maison) des Ruedihus liegt als Werkzeug unter _werkzeuge/maison/ (wie Carlton und Doldenhorn); online unter /maison/ (Fall Doldenhorn): Weg nach Adresse
ers('<a class="rund" href="../maison/" data-tip="La Maison" aria-label="La Maison">${SYM.haus}</a>', '<a class="rund" href="${STUBE}" data-tip="Die Stube" aria-label="Die Stube">${SYM.haus}</a>')
ers('<a href="../maison/">La Maison${PF}</a>', '<a href="${STUBE}">Die Stube${PF}</a>')
ers("const SYM = {", "const STUBE = /\\/_werkzeuge\\//.test(location.pathname) ? '../maison/' : '/maison/';   // Die Stube: lokal _werkzeuge/maison/, online /maison/ (Falle Doldenhorn 17.10.2026)\nconst SYM = {")
# Brief: Kopf und Fuss des Hauses (Belege oben)
ers("<header class=\"brief__kopf\">${ZEICHEN}<b>Grand Beau-Rivage</b><span>Interlaken · seit 1874</span></header>", "<header class=\"brief__kopf\">${ZEICHEN}<b>Landgasthof Ruedihus</b><span>Kandersteg · seit 1753</span></header>", 2)
ers("<footer class=\"brief__fuss\">Höheweg 211 · 3800 Interlaken · Schweiz<br>+41 33 826 70 07 · info@grandbeaurivage.ch</footer>", "<footer class=\"brief__fuss\">Hinder de Büele 6 · 3718 Kandersteg<br>(+41) 033 675 81 81 · info@doldenhorn.ch</footer>")
ers("const GKOPF = { haus: 'Grand Beau-Rivage', zeile: 'Interlaken · seit 1874', fuss: 'Höheweg 211 · 3800 Interlaken · Schweiz\\n+41 33 826 70 07 · info@grandbeaurivage.ch' };",
    "const GKOPF = { haus: 'Landgasthof Ruedihus', zeile: 'Kandersteg · seit 1753', fuss: 'Hinder de Büele 6 · 3718 Kandersteg\\n(+41) 033 675 81 81 · info@doldenhorn.ch' };")
block("const BRIEFBILDER = [", """const BRIEFBILDER = [['haus-fassade', 'Die Fassade mit Geranien'], ['haus-winter', 'Das Haus im Schnee'], ['haus-daemmerung', 'Zur blauen Stunde'], ['giebel', 'Der bemalte Giebel'],
  ['butzen', 'Butzenscheiben und Geranien'], ['stube-kerze', 'Stube bei Kerzenlicht'], ['stube-rund', 'Stube im Parterre'], ['ofestuebli', 'Ofestübli'],
  ['z-himmelbett', 'Himmelbett'], ['z-liebeslaube', 'Liebeslaube'], ['z-hochzeit', 'Hochzeitsstube'], ['z-hymmelrich', 'Hymmelrich'], ['fest-tafel', 'Gedeckt für ein Fest'], ['terrasse', 'Die Terrasse']];""", '];')
# Schriften: Cormorant und Cinzel → Gelasio (Titel aus der Wortmarke; «Versalien» = Gelasio fett in Versalien wie der Name auf den Karten)
t = t.replace("'Cormorant Garamond',Georgia,'Times New Roman',serif", "'Gelasio',Georgia,'Times New Roman',serif")
t = t.replace("Cinzel,Georgia,serif", "'Gelasio',Georgia,serif")
t = t.replace('Schrift Cinzel', 'Schrift Versalien').replace("['cinzel', 'Cinzel', 'var(--caps)']", "['cinzel', 'Versalien', 'var(--caps)']")
t = t.replace("['serif', 'Cormorant', 'var(--serif)']", "['serif', 'Gelasio', 'var(--serif)']")
ers("../imprimerie/haeuser/gbr/marke.json", "../imprimerie/haeuser/ruedihus/marke.json")
# Hausfarben im Brief (main.css :root des Ruedihus, marke_werkbank.py): Wandholz, Balken, Tinte, Papier, Leinen, Blatt, Kerze, Licht, Gold, Holz hell, Geranie
block("const HNAME = {", "const HNAME = { navy: 'Wandholz', blau: 'Balken', tinte: 'Tinte', papier: 'Papier', creme: 'Leinen', weiss: 'Blatt', sand: 'Kerze', gold: 'Licht', messing: 'Gold', taupe: 'Holz hell', rot: 'Geranie' };")
block("const HFARBE = {", "const HFARBE = { navy: '#321f10', blau: '#6d431f', tinte: '#2a1a0e', papier: '#efe4d3', creme: '#d8c2ad', weiss: '#fbf5ea', sand: '#c98543', gold: '#f3cd94', messing: '#b78f51', taupe: '#84603c', rot: '#c42e13' };")
block("const LFARBE = {", "const LFARBE = { taupe: 'rgba(132,96,60,.42)', gold: '#b78f51', navy: '#321f10' };")
# Wissen: Bereiche des Ruedihus (gedaechtnis.py BEREICHE, server_teil.py) mit Foto
block("const BER_BILD = {", """const BER_BILD = { 'Das Haus': 'haus-fassade-s', 'Zimmer': 'z-himmelbett-s', 'Essen & Stuben': 'stube-kerze-s', 'Feste im Haus': 'fest-tafel-s',
  'Durchs Jahr': 'stube-lang-s', 'Spa im Nachbarhaus': 'spa-s', 'Anreise & Abreise': 'haus-sommer-s', 'Kandersteg & Ausflüge': 'haus-wiese-s', 'Geschichte': 'giebel-s',
  'Veranstaltungen': 'stube-rund-s', 'Fragen & Antworten': 'stube-tuer-s' };""")
block("const ABTEILUNG = [", """const ABTEILUNG = [['Rezeption', 'info@doldenhorn.ch'], ['Event-Team (Feste im Haus)', 'event@doldenhorn.ch'], ['Personal (Stellen)', 'jobs@doldenhorn.ch']];""", '];')
# Probefragen aus dem Chat des Hauses (gast_haeuser.py HAEUSER['ruedihus'] karten, MUSTER)
block("const PROBEFRAGEN = [", """const PROBEFRAGEN = ['Was gibt es bei Ihnen zu essen?', 'Welche Zimmer haben Sie?', 'Kann ich als Gast das Spa benutzen?', 'Habt ihr Fondue?'];""", '];')
ers("location.pathname.replace(/reception\\/.*$/, '')", "location.pathname.replace(/_?werkzeuge\\/reception\\/.*$/, '')")   # online liegt die Oberfläche unter /werkzeuge/reception/
ers('src="../kontakt.html?probe=1"', 'src="../../index.html?probe=1"')
t = t.replace("'halle-2')", "'stube-tuer')")
ers("THEMABILD[f.gruppe] || 'halle-s'}", "THEMABILD[f.gruppe] || 'stube-tuer-s'}")   # Foto für Fragen ohne Thema
# «Chat ausprobieren»: der Chat der Maeder-Häuser (gast_haeuser.py, Fassung des Carlton) hat ein einzeiliges Feld (input), der des Rivage ein textarea (Fund Doldenhorn)
n = t.count("d.querySelector('.gast__feld textarea')")
if n != 2:
    sys.exit(f'ABBRUCH: Feld des Chats {n}× statt 2×')
t = t.replace("d.querySelector('.gast__feld textarea')", "d.querySelector('.gast__feld textarea, .gast__feld input')")
ers("Zum Beispiel: Ballsaal ist an dem Tag frei, Angebot mit Apéro auf der Terrasse", "Zum Beispiel: Jungestube ist an dem Tag frei, Cüpli zum Empfang anbieten")
ers("Zum Beispiel: Ab 1. November öffnet das Schwimmbad dienstags erst um 10 Uhr. Oder einfach einen Link einfügen.", "Zum Beispiel: Ab [Datum] ist die Terrasse geschlossen. Oder einfach einen Link einfügen.")
ers("Suchen, zum Beispiel Frühstück, Spa, Hund", "Suchen, zum Beispiel Frühstück, Fondue, Hund")
ers("Zum Beispiel: kürzer, mit Preis der Hochzeitspauschale", "Zum Beispiel: kürzer, mit dem Richtpreis des Menüs")
open(p, 'w', encoding='utf-8').write(t)
print('Ruedihus eingesetzt')

# studio/buehne.js: Fotos des Ruedihus, je Ansicht ein eigenes; Pfad zu assets/img des Projekts
b = os.path.join(C, 'studio', 'buehne.js')
u = open(b, encoding='utf-8').read()


def ers_b(alt, neu):
    global u
    if u.count(alt) != 1:
        sys.exit(f'ABBRUCH buehne.js: «{alt[:70]}»')
    u = u.replace(alt, neu)


ers_b("var FOTO = { bu: 'haus-vorfahrt', rg: 'halle-gepaeck', re: 'halle-sessel', li: 'fassade-detail' };", "var FOTO = { bu: 'haus-fassade', rg: 'stube-kerze', re: 'stube-tuer', li: 'giebel' };")
ers_b("replace(/studio\\/buehne\\.js.*$/, '') + 'assets/img/';", "replace(/_?werkzeuge\\/reception\\/studio\\/buehne\\.js.*$/, '') + 'assets/img/';")
ers_b("im.src = basis + k + '.webp'; }", "im.src = basis + k + '-s.webp'; }")
ers_b("var k = h.getAttribute('data-kb') || FOTO[art];",
      "var ANSICHT = { uebersicht: 'haus-daemmerung', eingang: 'stube-kerze', gefragt: 'ofestuebli', nachgetragen: 'stube-rund', wissen: 'giebel' };   // je Ansicht ein Foto des Hauses (Ruedihus)\n"
      "    var k = h.getAttribute('data-kb') || ANSICHT[location.hash.slice(1)] || FOTO[art];")
open(b, 'w', encoding='utf-8').write(u)
print('buehne.js angepasst')
