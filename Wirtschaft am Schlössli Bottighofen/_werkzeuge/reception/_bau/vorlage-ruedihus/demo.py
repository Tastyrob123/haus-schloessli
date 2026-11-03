#!/usr/bin/env python3
"""Der Gastgeber · Landgasthof Ruedihus: vor dem Auftrag ist alles ein Entwurf (Werkbank-Regel 12, Robert 17.10.2026: «Die Formulare schicken Mails an die
echte Adresse des Hauses, und der Chat speichert Daten im Namen des Hauses … ein Detail, das sich abstellen oder als Demo kennzeichnen lässt»).
Nichts geht an eine Adresse des Hauses (es gab nie einen Versand, die Anfragen liegen nur im Eingang); jetzt sagt es jede Stelle auch so:
der Chat beim Aufnehmen einer Anfrage, die Probe-Antwort, der Dank nach einem Formular und das Startbild des Gastgebers.
Läuft in alle.sh nach oberflaeche.py; bricht ab, wenn eine Stelle nicht trifft; zweiter Lauf erkennt den Stand."""
import os, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ersetze(datei, paare):
    p = os.path.join(R, datei)
    t = open(p, encoding='utf-8').read()
    neu = t
    for alt, ers in paare:
        if ers in neu:
            continue
        if neu.count(alt) != 1:
            sys.exit(f'demo.py: {datei}: Stelle trifft nicht ({alt[:70]!r}, {neu.count(alt)}×)')
        neu = neu.replace(alt, ers)
    if neu != t:
        open(p, 'w', encoding='utf-8').write(neu)
        print('demo.py:', datei, 'gekennzeichnet')
    else:
        print('demo.py:', datei, 'schon gekennzeichnet')


ersetze('reception.py', [
    ("- Deine Antwort dazu: ein Satz, dass die Anfrage beim Team liegt und sich das Haus persönlich meldet. Sag nie, dass etwas reserviert oder bestätigt ist.",
     "- Deine Antwort dazu: ein Satz, dass dies ein Entwurf von Tasty Studios ist und die Anfrage deshalb nicht an das Haus geht; für eine echte Anfrage hilft die Rezeption am Telefon (Nummer wie oben). Sag nie, dass etwas reserviert, bestätigt oder weitergegeben ist."),
    ("DANKE = {'de': 'Danke, Ihre Anfrage liegt beim Team des Landgasthof Ruedihus. Wir melden uns persönlich bei Ihnen.',",
     "DANKE = {'de': 'Danke. Dies ist ein Entwurf von Tasty Studios: Die Anfrage geht nicht an das Haus, sie liegt nur zur Ansicht im Gastgeber.',"),
    ("         'en': 'Thank you, your request is with the team of the Landgasthof Ruedihus. We will get back to you personally.',",
     "         'en': 'Thank you. This is a draft by Tasty Studios: your request does not go to the hotel, it is only kept for viewing in the host tool.',"),
    ("         'fr': 'Merci, votre demande est transmise à l’équipe du Landgasthof Ruedihus. Nous reviendrons vers vous personnellement.'}",
     "         'fr': 'Merci. Ceci est une ébauche de Tasty Studios : votre demande n’est pas transmise à l’hôtel, elle est seulement conservée pour être consultée.'}"),
])
ersetze('probe_ki.py', [
    ("'Probe-Antwort ohne KI: Ich gebe Ihre Anfrage an das Team weiter.'",
     "'Probe-Antwort ohne KI: Dies ist ein Entwurf, Ihre Anfrage geht nicht an das Haus. Für eine echte Anfrage hilft die Rezeption am Telefon.'"),
])
ersetze('reception.js', [
    ("liegt die Anfrage im Eingang, nach Abteilung, mit einem Brief als Entwurf für Ihre Antwort. Verschickt wird nur, was Sie selbst schicken.'",
     "liegt die Anfrage im Eingang, nach Abteilung, mit einem Brief als Entwurf für Ihre Antwort. Verschickt wird nur, was Sie selbst schicken. Solange dies ein Entwurf ist, kommt nichts davon von echten Gästen und nichts geht an das Haus: Die Anfragen hier sind Beispiele und Proben.'"),
])
