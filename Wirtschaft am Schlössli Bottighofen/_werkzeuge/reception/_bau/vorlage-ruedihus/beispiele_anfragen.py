#!/usr/bin/env python3
"""Schreibt gast_beispiele.json: neun erfundene Anfragen für den Eingang des Gastgebers (La Réception) im Landgasthof Ruedihus, je mit Brief als Entwurf
und (bei fremder Sprache) deutscher Lesefassung. Sechs kommen wie echt über die Formulare der Website (Tisch in der Stube, Fest-Rechner, Gutschein,
Vor Ihrer Anreise, Ihre Abreise, Bewerbung; mit Abteilung, Seite und Formular), drei über den Chat.
Gäste, Namen und Wünsche sind erfunden (example.com) und in der Oberfläche als «Beispiel» beschriftet. Jede Angabe über das Haus in den Briefen steht
so in den Seiten oder Karten des Hauses (gast/gast_wissen.txt); prufe() bricht ab, wenn eine Zahl im Brief weder dort noch in der Anfrage steht.
Nachgetragene Antworten des Teams gibt es bewusst keine (Master E10: nie erfinden, das Team habe etwas nachgetragen).
Vorbild: _bau/beispiele_anfragen.py des Waldhotel Doldenhorn (nur gelesen).
Aufruf: python3 _werkzeuge/reception/_bau/beispiele_anfragen.py"""
import json, os, re, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = 'Rezeption · Landgasthof Ruedihus'
E = 'Event-Team · Landgasthof Ruedihus'
P = 'Personal · Landgasthof Ruedihus'


def web(seite, text):
    return [['user', f'Über ein Formular der Website (Seite {seite}): {text}']]


B = [
 # 1 · Website, Tisch in der Stube, Rezeption, Deutsch, neu
 {'vor': [0, 8, 14], 'art': 'tisch', 'status': 'neu', 'an': 'info@doldenhorn.ch', 'abteilung': 'Rezeption', 'seite': '/essen.html', 'seite_name': 'Essen', 'formular': 'tisch', 'web': True,
  'name': 'Martina Huber', 'kontakt': 'martina.huber@example.com', 'datum': 'Samstag, 24. Oktober 2026, 19:00 Uhr', 'personen': 4, 'sprache': 'de',
  'anliegen': 'Tisch in der Chäs- und Wystube',
  'nachricht': 'Stube: Chäs- und Wystube\nTag: Samstag, 24.10.2026\nUhrzeit: 19:00\nPersonen: 4\nMenü: Fondue oder Raclette Menu\nWünsche: Unsere Tochter isst lieber Rösti als Fondue.',
  'betreff': 'Ihr Tisch in der Chäs- und Wystube, Samstag, 24. Oktober',
  'text': 'Liebe Frau Huber\n\nvielen Dank für Ihre Anfrage. Wir schauen in unser Buch und halten Ihnen gern einen Tisch für vier Personen um 19:00 Uhr in der Chäs- und Wystube frei: [Tisch bestätigen].\n\n'
          'Für Ihre Tochter steht die Bauernröschti mit Hobelchäs auf dem Schpiszettel, als kleine Portion für CHF 24.00.\n\n'
          'Geht etwas schneller am Telefon, erreichen Sie uns unter (+41) 033 675 81 81.\n\n'
          'Herzlich, Familie Maeder und ihre Crew\n\n[Name]\n' + R,
  'team': 'Grundlage: essen.html (Schpiszettel Chäs- und Wystube ab 1.3.2026: Bauernröschti 24.00 / 29.00), Mail «Ihr Tisch in der Stube».\nOffen: Tisch 24.10. 19:00 für vier.'},
 # 2 · Website, Fest-Rechner, Event, Deutsch, neu
 {'vor': [0, 5, 2], 'art': 'feier', 'status': 'neu', 'an': 'event@doldenhorn.ch', 'abteilung': 'Event', 'seite': '/essen.html', 'seite_name': 'Essen', 'formular': 'fest', 'web': True,
  'name': 'Beat Ryser', 'kontakt': '+41 79 000 00 00', 'datum': 'Samstag, 14. November 2026', 'personen': 22, 'sprache': 'de',
  'anliegen': 'Geburtstag mit 22 Gästen',
  'nachricht': 'Anlass: Geburtstag\nDatum: 2026-11-14\nGäste: 22\nStube: Jungestube\nFondue oder Raclette Menu, 18 Erwachsene\nFür di Chline, 4 Kinder\nCüpli zum Empfang\nWünsche: Meine Mutter wird 70. Wir möchten gern um 18 Uhr beginnen.',
  'betreff': 'Der 70. Geburtstag Ihrer Mutter, Samstag, 14. November',
  'text': 'Lieber Herr Ryser\n\nvielen Dank für Ihre Anfrage und schon jetzt alles Gute zum 70. Geburtstag Ihrer Mutter. Es freut uns, dass Sie dieses Fest bei uns feiern möchten.\n\n'
          'Für 22 Gäste passt die Jungestube im Parterre mit 25 Sitzplätzen, «geeignet auch für Sitzungen und Familienfeste». Für Ihr Datum [Verfügbarkeit prüfen].\n\n'
          'Ihr Richtpreis aus dem Fest-Rechner ist ein erster Entwurf. Die verbindliche Offerte mit Menü, Cüpli zum Empfang und Getränken schicken wir Ihnen gern: [Offerte freigeben].\n\n'
          'Damit wir alles vorbereiten können:\n- Gibt es Allergien oder Wünsche zum Menü?\n- Möchten Sie eine Torte zum Dessert?\n\n'
          'Herzlich, Familie Maeder und ihre Crew\n\n[Name]\n' + E,
  'team': 'Grundlage: essen.html (Feste im Ruedihus: Jungestube 25 Sitzplätze, Fest-Rechner mit den Karten ab 1.3.2026).\nOffen: Jungestube am 14.11. ab 18 Uhr; Offerte; Torte.'},
 # 3 · Website, Gutschein, Rezeption, Deutsch, gelesen
 {'vor': [1, 9, 33], 'art': 'gutschein', 'status': 'gelesen', 'an': 'info@doldenhorn.ch', 'abteilung': 'Rezeption', 'seite': '/zimmer.html', 'seite_name': 'Zimmer', 'formular': 'gutschein', 'web': True,
  'name': 'Sandra Wenger', 'kontakt': 'sandra.wenger@example.com', 'datum': 'zum Hochzeitstag im Dezember', 'personen': 2, 'sprache': 'de',
  'anliegen': 'Gutschein für die Liebeslaube',
  'nachricht': 'Guten Tag, ich möchte meinen Eltern zum Hochzeitstag eine Nacht in der Liebeslaube schenken, mit Frühstück. Können Sie mir dafür einen Gutschein ausstellen?',
  'betreff': 'Ihr Gutschein für die Liebeslaube',
  'text': 'Liebe Frau Wenger\n\nvielen Dank für Ihre Anfrage. Was für ein schönes Geschenk zum Hochzeitstag Ihrer Eltern.\n\n'
          'Einen Gutschein für ein bestimmtes Zimmer stellen wir Ihnen gern aus, für eine Nacht in der Liebeslaube mit Frühstück: [Preis nennen]. Er kommt als PDF, mit Ihrer Widmung, zum Ausdrucken oder Weiterschicken.\n\n'
          'Fragen dazu beantworten wir gern unter (+41) 033 675 81 81.\n\n'
          'Herzlich, Familie Maeder und ihre Crew\n\n[Name]\n' + R,
  'team': 'Grundlage: zimmer.html (Geschenkgutscheine: «Für ein bestimmtes Zimmer nennt Ihnen die Familie am Telefon den Preis»), Mail «Ihr Gutschein ist da».\nOffen: Preis Liebeslaube mit Frühstück; Widmung erfragen; Zahlung.'},
 # 4 · Website, Vor Ihrer Anreise, Rezeption, Englisch, gelesen
 {'vor': [1, 17, 48], 'art': 'aufenthalt', 'status': 'gelesen', 'an': 'info@doldenhorn.ch', 'abteilung': 'Rezeption', 'seite': '/anreise.html', 'seite_name': 'Vor Ihrer Anreise', 'formular': 'anreise', 'web': True,
  'name': 'James Whitaker', 'kontakt': 'j.whitaker@example.com', 'datum': '11 to 13 December 2026', 'personen': 2, 'sprache': 'en',
  'anliegen': 'Arrival on 11 December and a table on the first evening',
  'nachricht': 'Name: James Whitaker\nBooking number: -\nArrival: 2026-12-11\nDeparture: 2026-12-13\nArriving: 18 to 20 h\nTable: Egger- und Stettlerstube, Fri 11 Dec, 19:30, 2 persons, Menu komplett',
  'betreff': 'Your arrival on 11 December and your table',
  'text': 'Dear Mr Whitaker\n\nThank you very much for letting us know. In a few weeks we will welcome you to the Ruedihus.\n\n'
          'On your first evening we will gladly keep a table for two in the Egger- und Stettlerstube at 19:30: [confirm table]. The Menu komplett costs CHF 80.00 per person.\n\n'
          'Parking is included, and breakfast is served as a buffet. When you arrive between 18 and 20 h, everything will be ready.\n\n'
          'Warm regards, the Maeder family and their crew\n\n[Name]\nReception · Landgasthof Ruedihus',
  'team': 'Grundlage: anreise.html (Formular «Vor Ihrer Anreise»), essen.html (Schpis Charte: Menu komplett 80.00), zimmer.html (Parkplatz inbegriffen, Frühstück als Buffet).\nOffen: Buchung zum Namen suchen (keine Buchungsnummer); Tisch 11.12. 19:30.',
  'deutsch': {'betreff': 'Ihre Anreise am 11. Dezember und Ihr Tisch',
              'text': 'Lieber Herr Whitaker\n\nvielen Dank für Ihre Nachricht. In ein paar Wochen dürfen wir Sie im Ruedihus begrüssen.\n\n'
                      'Am ersten Abend halten wir Ihnen gern einen Tisch für zwei in der Egger- und Stettlerstube um 19:30 frei: [Tisch bestätigen]. Das Menu komplett kostet CHF 80.00 pro Person.\n\n'
                      'Der Parkplatz ist inbegriffen, das Frühstück steht als Buffet bereit. Wenn Sie zwischen 18 und 20 Uhr ankommen, steht alles bereit.\n\n'
                      'Herzlich, Familie Maeder und ihre Crew\n\n[Name]\nRezeption · Landgasthof Ruedihus'},
  'verlauf_de': ['Über ein Formular der Website (Seite Vor Ihrer Anreise): Name: James Whitaker · Buchungsnummer: - · Anreise: 11.12.2026 · Abreise: 13.12.2026 · Ankunft: 18 bis 20 Uhr · Tisch: Egger- und Stettlerstube, Fr 11. Dez., 19:30, 2 Personen, Menu komplett']},
 # 5 · Website, Ihre Abreise, Rezeption, Deutsch, neu
 {'vor': [1, 7, 10], 'art': 'aufenthalt', 'status': 'neu', 'an': 'info@doldenhorn.ch', 'abteilung': 'Rezeption', 'seite': '/abreise.html', 'seite_name': 'Ihre Abreise', 'formular': 'abreise', 'web': True,
  'name': 'Ursula Bieri', 'kontakt': 'ursula.bieri@example.com', 'datum': 'Sonntag, 25. Oktober 2026, 14:00 Uhr', 'personen': 2, 'sprache': 'de',
  'anliegen': 'Abreise am Sonntag und Zmittag in der Stube',
  'nachricht': 'Name: Ursula Bieri\nZimmer oder Buchungsnummer: Hochzeitsstube\nAbreise: So., 25. Okt. 2026, 14:00 Uhr\nZmittag: Chäs- und Wystube, 12:00 Uhr, 2 Personen\nNachricht: Dürfen wir das Gepäck nach dem Auschecken bis zur Abfahrt stehen lassen?',
  'betreff': 'Ihr Zmittag vor der Abreise am Sonntag',
  'text': 'Liebe Frau Bieri\n\nvielen Dank für Ihre Nachricht. Vor Ihrer Fahrt decken wir Ihnen gern einen Tisch für zwei in der Chäs- und Wystube um 12:00 Uhr: [Tisch bestätigen].\n\n'
          'Zu Ihrem Gepäck: [Aufbewahren bis zur Abfahrt bestätigen].\n\n'
          'Der Bus hält an der Haltestelle «Ruedi Hus» gleich beim Haus. Wir wünschen Ihnen schon jetzt eine gute Heimreise.\n\n'
          'Herzlich, Familie Maeder und ihre Crew\n\n[Name]\n' + R,
  'team': 'Grundlage: abreise.html (Formular «Ihre Abreise», Haltestelle «Ruedi Hus»), essen.html (Restaurant 11:30 – 21:00 Uhr).\nOffen: Tisch 25.10. 12:00; Gepäck aufbewahren (steht nicht auf den Seiten).'},
 # 6 · Website, Bewerbung, Personal, Deutsch, neu
 {'vor': [2, 16, 42], 'art': 'nachricht', 'status': 'neu', 'an': 'jobs@doldenhorn.ch', 'abteilung': 'Personal', 'seite': '/haus.html', 'seite_name': 'Das Haus', 'formular': 'stelle', 'web': True,
  'name': 'Lena Zurbuchen', 'kontakt': 'lena.zurbuchen@example.com', 'datum': 'ab der Wintersaison', 'personen': None, 'sprache': 'de',
  'anliegen': 'Bewerbung im Service',
  'nachricht': 'Guten Tag, ich arbeite seit drei Jahren im Service und würde gern ab der Wintersaison in Ihren Stuben arbeiten. Meinen Lebenslauf schicke ich Ihnen gern.',
  'betreff': 'Ihre Bewerbung im Service',
  'text': 'Liebe Frau Zurbuchen\n\nvielen Dank für Ihr Interesse an einer Stelle bei uns. Zurzeit suchen wir für das Ruedihus und das Waldhotel Doldenhorn unter anderem im Service (m/w/d).\n\n'
          'Schicken Sie uns Ihren Lebenslauf gern per E-Mail an jobs@doldenhorn.ch, ein paar Zeilen zu Ihnen reichen für den Anfang. Danach melden wir uns für ein Gespräch: [Termin vorschlagen].\n\n'
          'Herzlich, Familie Maeder und ihre Crew\n\n[Name]\n' + P,
  'team': 'Grundlage: haus.html (Offene Stellen: Sous-Chef, Rezeptionist, Service, Koch; «Bewerbung per E-Mail an jobs@doldenhorn.ch»).\nOffen: Gespräch; Beginn Wintersaison; Wohnen, Dienste und Verpflegung stehen nicht auf der Website.'},
 # 7 · Chat, Tisch, Französisch, erledigt
 {'vor': [2, 12, 5], 'art': 'tisch', 'status': 'erledigt', 'name': 'Élise Dubois', 'kontakt': 'elise.dubois@example.com', 'datum': 'vendredi 30 octobre 2026, 19 h', 'personen': 2, 'sprache': 'fr',
  'anliegen': 'Raclette à discrétion pour deux, vendredi soir.',
  'verlauf': [['user', 'Bonsoir, est-ce que vous servez de la raclette ? Nous serions deux vendredi soir.'],
              ['assistant', 'Oui, dans la Chäs- und Wystube au rez-de-chaussée : raclette à discrétion pour CHF 36.00. Souhaitez-vous que l’équipe vous réserve une table ? Il me faut votre nom et une adresse e-mail ou un numéro de téléphone.'],
              ['user', 'Élise Dubois, elise.dubois@example.com, vendredi 30 octobre vers 19 h.'],
              ['assistant', 'Merci, Madame Dubois. Votre demande est transmise à l’équipe, la maison vous répondra personnellement.']],
  'betreff': 'Votre table pour la raclette, vendredi 30 octobre',
  'text': 'Chère Madame Dubois\n\nMerci beaucoup pour votre demande. Nous vous réservons volontiers une table pour deux dans la Chäs- und Wystube, vendredi 30 octobre à 19 h : [confirmer la table].\n\n'
          'La raclette à discrétion coûte CHF 36.00 par personne.\n\n'
          'Chaleureusement, la famille Maeder et son équipe\n\n[Name]\nRéception · Landgasthof Ruedihus',
  'team': 'Grundlage: essen.html (Schpiszettel: Raclette so viel dr möget 36.00).\nOffen: Tisch 30.10. 19 Uhr.',
  'deutsch': {'betreff': 'Ihr Tisch für das Raclette, Freitag, 30. Oktober',
              'text': 'Liebe Frau Dubois\n\nvielen Dank für Ihre Anfrage. Gern reservieren wir Ihnen einen Tisch für zwei in der Chäs- und Wystube, Freitag, 30. Oktober um 19 Uhr: [Tisch bestätigen].\n\n'
                      'Das Raclette à discrétion kostet CHF 36.00 pro Person.\n\n'
                      'Herzlich, Familie Maeder und ihre Crew\n\n[Name]\nRezeption · Landgasthof Ruedihus'},
  'verlauf_de': ['Guten Abend, servieren Sie Raclette? Wir wären am Freitagabend zu zweit.',
                 'Ja, in der Chäs- und Wystube im Parterre: Raclette à discrétion für CHF 36.00. Soll das Team Ihnen einen Tisch reservieren? Dann brauche ich Ihren Namen und eine E-Mail-Adresse oder Telefonnummer.',
                 'Élise Dubois, elise.dubois@example.com, Freitag, 30. Oktober gegen 19 Uhr.',
                 'Danke, Frau Dubois. Ihre Anfrage liegt beim Team, das Haus meldet sich persönlich bei Ihnen.']},
 # 8 · Chat, Zimmer, Deutsch, erledigt
 {'vor': [3, 20, 11], 'art': 'zimmer', 'status': 'erledigt', 'name': 'Reto und Anna Lüthi', 'kontakt': 'reto.luethi@example.com', 'datum': '5. bis 7. Februar 2027', 'personen': 2, 'sprache': 'de',
  'anliegen': 'Zwei Nächte im Himmelbett zum Hochzeitstag.',
  'verlauf': [['user', 'Wir feiern im Februar unseren Hochzeitstag und suchen ein Zimmer mit Himmelbett für zwei Nächte.'],
              ['assistant', 'Wie schön. Die Hochzeitsstube ist ein Salonzimmer mit Himmelbett, Bad, Dusche und WC, ab CHF 300.00 pro Nacht für 1–2 Personen. Möchten Sie ein persönliches Angebot? Dann brauche ich Ihren Namen und eine E-Mail-Adresse oder Telefonnummer.'],
              ['user', 'Reto Lüthi, reto.luethi@example.com, vom 5. bis 7. Februar.'],
              ['assistant', 'Danke, Herr Lüthi. Ihre Anfrage liegt beim Team, das Haus meldet sich persönlich bei Ihnen.']],
  'betreff': 'Ihr Hochzeitstag in der Hochzeitsstube, 5. bis 7. Februar 2027',
  'text': 'Lieber Herr Lüthi, liebe Frau Lüthi\n\nvielen Dank für Ihre Anfrage und herzliche Gratulation zum Hochzeitstag.\n\n'
          'Die Hochzeitsstube ist ein Salonzimmer mit Himmelbett, Bad, Dusche und WC, ab CHF 300.00 pro Nacht. Für Ihre Daten [Verfügbarkeit prüfen].\n\n'
          'Am Abend deckt Ihnen die Küche gern einen Tisch in einer der beiden Biedermeierstuben im 1. Stock: [Tisch anbieten].\n\n'
          'Herzlich, Familie Maeder und ihre Crew\n\n[Name]\n' + R,
  'team': 'Grundlage: zimmer.html (Hochzeitsstube ab 300.00, Salonzimmer mit Himmelbett), essen.html (Biedermeierstuben im 1. Stock).\nOffen: Hochzeitsstube 5.–7.2.; Tisch am Abend.'},
 # 9 · Chat, Sitzung, Event, Deutsch, neu
 {'vor': [4, 10, 51], 'art': 'tagung', 'status': 'neu', 'name': 'Daniel Ogi', 'kontakt': 'daniel.ogi@example.com', 'datum': 'Donnerstag, 19. November 2026, 18 Uhr', 'personen': 14, 'sprache': 'de',
  'anliegen': 'Vereinssitzung mit 14 Personen, danach ein Znacht in der Stube.',
  'verlauf': [['user', 'Unser Verein möchte im November eine Sitzung bei Ihnen halten, 14 Personen, und danach zusammen essen. Geht das?'],
              ['assistant', 'Die Jungestube im Parterre hat 25 Sitzplätze und ist «geeignet auch für Sitzungen und Familienfeste». Soll das Event-Team Ihnen ein Angebot schicken? Dann brauche ich Ihren Namen und eine E-Mail-Adresse oder Telefonnummer.'],
              ['user', 'Daniel Ogi, daniel.ogi@example.com, Donnerstag, 19. November ab 18 Uhr.'],
              ['assistant', 'Danke, Herr Ogi. Ihre Anfrage liegt beim Team, das Haus meldet sich persönlich bei Ihnen.']],
  'betreff': 'Ihre Vereinssitzung am Donnerstag, 19. November',
  'text': 'Lieber Herr Ogi\n\nvielen Dank für Ihre Anfrage. Ihr Verein ist bei uns herzlich willkommen.\n\n'
          'Für 14 Personen passt die Jungestube im Parterre mit 25 Sitzplätzen. Für Ihr Datum [Verfügbarkeit prüfen].\n\n'
          'Zum Znacht danach empfehlen wir aus unseren Stuben ein Fondue, ein Raclette oder eine Röstispezialität: [Menü vorschlagen].\n\n'
          'Herzlich, Familie Maeder und ihre Crew\n\n[Name]\n' + E,
  'team': 'Grundlage: essen.html (Jungestube 25 Sitzplätze, «geeignet auch für Sitzungen und Familienfeste»; Stuben im Parterre: Fondue, Raclette, Rösti).\nOffen: Jungestube 19.11. ab 18 Uhr; Menü und Getränke.'},
]


def prufe():
    """Jede Zahl im Brief (und in der Lesefassung) steht in den Seiten des Hauses oder in der Anfrage selbst. Nichts erfunden über das Haus."""
    w = re.sub(r'\s+', ' ', open(os.path.join(C, 'gast', 'gast_wissen.txt'), encoding='utf-8').read()).replace('’', '')
    fehler = []
    for n, b in enumerate(B, 1):
        anfrage = ' '.join(str(b.get(k) or '') for k in ('datum', 'personen', 'anliegen', 'nachricht', 'kontakt')) + ' '.join(t for _, t in b.get('verlauf') or [])
        for text in [b['text'], (b.get('deutsch') or {}).get('text', '')]:
            for z in re.findall(r'\d+(?:[.,]\d+)?', text.replace('’', '')):
                if z not in w and z not in anfrage:
                    fehler.append(f'Beispiel {n}: Zahl {z} weder im Wissen noch in der Anfrage')
    if fehler:
        sys.exit('\n'.join(fehler))


if __name__ == '__main__':
    prufe()
    for b in B:
        if b.get('web'):
            b['verlauf'] = web(b['seite_name'], b['nachricht'])
    json.dump(B, open(os.path.join(C, 'gast_beispiele.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(B), 'Anfragen geschrieben, jede Zahl belegt')
