#!/usr/bin/env python3
"""Antwortbuch der Rezeption im Chat · Landgasthof Ruedihus (Werkbank-Chat 19.10.2026).

Robert 19.10.2026 05:10: «Kein Guthaben jetzt. Baut in allen vier Häusern feste Demo-Antworten in den Gäste-Chat ein.»
Antwortet die KI nicht (kein Guthaben, kein Schlüssel, Fehler), antwortet der Chat aus diesem Buch: auf dem Server (api/gast.py, Hülle aus
_werkzeuge/reception/online/gast.py) und, wenn der Server gar nicht antwortet, im Browser (assets/js/gast-antworten.js). Eine Quelle, zwei Ausgaben.

Jede Angabe steht auf der Website des Hauses oder in seinen Karten (daten.py: ZEITEN, PARTERRE, ERSTER_STOCK, ZIMMER, GUT, UMGEBUNG, HALT,
GUTSCHEIN, GOURMET, ANGEBOT; Seiten anreise, abreise, essen, haus, zimmer). Was dort nicht steht (Frühstückszeiten, Check-in, Stornierung,
Barrierefreiheit), erfindet das Buch nicht, es führt zur Rezeption.

    python3 _werkzeuge/reception/online/antwortbuch.py   → _werkzeuge/reception/online/gast_antworten.json, assets/js/gast-antworten.js
"""
import json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HIER, '..', '..', '..'))
TEL, MAIL, MAIL_FESTE = '+41 33 675 81 81', 'info@doldenhorn.ch', 'event@doldenhorn.ch'
ADRESSE = 'Hinder de Büele 6, 3718 Kandersteg'

# Thema: Stichwörter (DE/EN/FR, mit Varianten), Antwort de/en, Knöpfe (Folgefragen, die selbst ein Thema treffen), maske (Buchungsmaske öffnen)
THEMEN = [
    dict(id='essen', s=['essen', 'küche', 'kueche', 'stube', 'stuben', 'restaurant', 'zmittag', 'znacht', 'abendessen', 'mittagessen', 'hunger', 'speis',
                        'food', 'eat', 'dinner', 'lunch', 'cuisine', 'manger', 'diner', 'dîner'],
         de='Bei uns isst man in den Stuben eines Hauses von 1753:\n- Parterre: drei rustikale Stuben für Fondue, Raclette und Rösti\n- 1. Stock: zwei Biedermeierstuben für den feineren Abend\n'
            'Auf den Tisch kommen ausgesuchte Produkte aus der Schweiz, «Sie suchen vergebens Campari, Orangensaft, Salzwasserfische, Cognac oder Cola». Das Restaurant ist von 11:30 bis 21:00 Uhr geöffnet.',
         en='You dine in the Stuben of a house built in 1753:\n- Ground floor: three rustic Stuben for fondue, raclette and rösti\n- First floor: two Biedermeier Stuben for a finer evening\n'
            'The kitchen uses selected Swiss produce only. The restaurant is open from 11:30 to 21:00.',
         k=['karte', 'tisch', 'oeffnung']),
    dict(id='oeffnung', s=['offen', 'geöffnet', 'geoeffnet', 'öffnungszeit', 'oeffnungszeit', '~wann hat', '~bis wann', '~ab wann', '~uhrzeit', 'open', 'opening', 'hours', 'ouvert', 'horaire', 'restaurant offen', 'restaurant open', 'restaurant geöffnet', 'is the restaurant open', 'opening hours'],
         de='Das Restaurant ist von 11:30 bis 21:00 Uhr geöffnet. Die Tagesteller stehen in der Karte, für einen Tisch am Abend rufen Sie am besten kurz an: ' + TEL + '.',
         en='The restaurant is open from 11:30 to 21:00. For a table in the evening, a short call is best: ' + TEL + '.',
         k=['karte', 'tisch']),
    dict(id='karte', s=['karte', 'schpiszettel', 'speisekarte', 'menu', 'menü', 'gericht', 'fondue', 'raclette', 'rösti', 'roesti', 'röschti', 'vegetar', 'tagesteller', 'preis essen',
                        'menu card', 'dish', 'carte', 'plat'],
         de='Ein paar Gerichte aus dem Schpiszettel der Chäs- und Wystube:\n- Friburger Original Chäsfondue: 29.00\n- Morchelfondue: 39.00\n- Raclette à discrétion: 36.00\n'
            '- Bauernröschti mit Hobelkäse, vegetarisch: 24.00 / 29.00\nDie ganze Karte und die Tagesteller finden Sie auf unserer Seite unter Essen.',
         en='A few dishes from the menu of the Chäs- und Wystube:\n- Friburger Original cheese fondue: 29.00\n- Morel fondue: 39.00\n- Raclette as much as you like: 36.00\n'
            '- Farmer’s rösti with mountain cheese, vegetarian: 24.00 / 29.00\nThe full menu and the dishes of the day are on our website under Essen.',
         k=['tisch', 'oeffnung']),
    dict(id='tisch', s=['tisch', 'reservier', 'platz frei', 'plätze', 'table', 'reserve a table', 'book a table', 'réserver une table'],
         de='Einen Tisch in der Stube reservieren Sie am einfachsten am Telefon: ' + TEL + ', oder per Mail an ' + MAIL + '. Das Restaurant ist von 11:30 bis 21:00 Uhr geöffnet. '
            'Für ein Familienfest gibt es die Jungestube mit 25 Plätzen.',
         en='The easiest way to book a table in the Stube is by phone: ' + TEL + ', or by email to ' + MAIL + '. The restaurant is open from 11:30 to 21:00.',
         k=['karte', 'feste']),
    dict(id='zimmer', s=['zimmer', 'himmelbett', 'landhaus', 'hochzeitsstube', 'liebeslaube', 'hymmelrich', 'himmelreich', 'übernacht', 'uebernacht', 'schlafen', 'nichtraucher', 'zimmerpreis',
                         'room', 'rooms', 'bed', '~stay', 'chambre', 'nuit'],
         de='Vier Zimmerarten, alle für 1–2 Personen und Nichtraucher:\n- Landhaus: ab 250 CHF pro Nacht\n- Hochzeitsstube: ab 300 CHF\n- Liebeslaube: ab 390 CHF\n- Hymmelrich: ab 390 CHF\n'
            'Mehrere davon mit Himmelbett. Frühstück als Buffet, Parkplatz und WLAN sind inbegriffen.',
         en='Four room types, all for 1–2 people and non-smoking:\n- Landhaus: from CHF 250 per night\n- Hochzeitsstube: from CHF 300\n- Liebeslaube: from CHF 390\n- Hymmelrich: from CHF 390\n'
            'Several have a canopy bed. Buffet breakfast, parking and Wi-Fi are included.',
         k=['buchen', 'fruehstueck', 'anreise']),
    dict(id='buchen', s=['zimmer buchen', 'book a room', 'buchen', 'buchung', 'verfügbar', 'verfuegbar', 'frei am', 'noch frei', 'book', 'booking', 'availab', 'réserver', 'disponib'],
         de='Gerne. Wählen Sie Daten und Zimmer, die Buchung übernimmt den Rest. Verfügbarkeit und Tagespreis zeigt die Buchungsseite des Hauses.',
         en='With pleasure. Choose dates and room, the booking page does the rest and shows availability and the price of the day.',
         k=['zimmer'], maske=True),
    dict(id='fruehstueck', s=['frühstück', 'fruehstueck', 'fruhstuck', 'zmorge', 'buffet', 'breakfast', 'petit-déjeuner', 'petit dejeuner'],
         de='Das Frühstück steht bei uns als Buffet bereit, es ist im Zimmerpreis inbegriffen. Die genauen Zeiten nennt Ihnen die Rezeption gern: ' + TEL + '.',
         en='Breakfast is served as a buffet and is included in the room rate. Reception will gladly tell you the exact times: ' + TEL + '.',
         k=['essen', 'zimmer']),
    dict(id='spa', s=['spa', 'sauna', 'saunen', 'hallenbad', 'schwimm', 'pool', 'massage', 'wellness', 'baden', 'swim', 'piscine'],
         de='Hallenbad, Saunen und Massagen liegen im Waldhotel Doldenhorn, unserem Schwesterhaus gleich gegenüber. Massagen buchen Sie direkt im Kalender des Spa, am einfachsten schon vor der Anreise. '
            'Was für Ihren Aufenthalt gilt, sagt Ihnen die Rezeption gern.',
         en='Indoor pool, saunas and massages are at the Waldhotel Doldenhorn, our sister hotel just across the road. Massages can be booked directly in the spa’s calendar, ideally before you arrive. '
            'Reception will gladly tell you what applies to your stay.',
         k=['zimmer', 'ausfluege']),
    dict(id='anreise', s=['anreise', 'anfahrt', 'wie komme ich', 'komme ich zu', 'get to you', 'how do i get', 'how to get', 'adresse', '~wo liegt', '~wo ist', 'zug', 'bahn', 'bahnhof', 'bus', 'haltestelle', '~auto', '~weg zu',
                          'arrive', 'arrival', 'address', 'train', 'station', 'directions', 'how do i get', 'adresse', 'gare'],
         de='So finden Sie zu uns:\n- Adresse: ' + ADRESSE + '\n- Zug: Bahnhof Kandersteg, 950 m vom Haus\n- Bus: Haltestelle «Ruedi Hus» direkt beim Haus\n- Auto: Parkplatz inbegriffen\n'
            'Das Ruedihus liegt einen Kilometer vom Zentrum, gegenüber dem Waldhotel Doldenhorn.',
         en='How to find us:\n- Address: ' + ADRESSE + '\n- Train: Kandersteg station, 950 m from the house\n- Bus: stop «Ruedi Hus» right by the house\n- Car: parking included\n'
            'The Ruedihus is one kilometre from the village centre, opposite the Waldhotel Doldenhorn.',
         k=['parken', 'zimmer']),
    dict(id='parken', s=['parkplatz', 'parkieren', 'parken', 'garage', 'auto abstellen', 'parking', 'park'],
         de='Der Parkplatz ist im Zimmerpreis inbegriffen. Wer lieber mit dem Bus kommt: Die Haltestelle «Ruedi Hus» liegt direkt beim Haus.',
         en='Parking is included in the room rate. If you prefer the bus: the stop «Ruedi Hus» is right by the house.',
         k=['anreise']),
    dict(id='hund', s=['hund', 'hunde', 'haustier', 'katze', 'dog', 'pet', 'chien'],
         de='Das Ruedihus ist haustierfreundlich, Ihr Hund ist willkommen. Was dabei im Haus gilt, sagt Ihnen die Rezeption gern vorab: ' + TEL + '.',
         en='The Ruedihus is pet-friendly, your dog is welcome. Reception will gladly tell you what applies in the house: ' + TEL + '.',
         k=['zimmer', 'buchen']),
    dict(id='wlan', s=['wlan', 'wifi', 'wi-fi', 'internet', 'w-lan'],
         de='WLAN ist bei uns inklusive.', en='Wi-Fi is included.', k=['zimmer']),
    dict(id='ausfluege', s=['ausflug', 'ausflüge', 'ausfluege', 'unternehm', 'wandern', 'wanderung', 'wetter', 'regen', '~heute', 'oeschinen', 'öschinen', 'blausee', 'sunnbüel', 'sunnbuel', 'gemmi', 'gasterntal',
                            'excursion', 'hike', 'hiking', 'weather', 'rain', 'what can i do', '~today', 'randonnée'],
         de='Rund um Kandersteg:\n- Oeschinensee: mit der Gondelbahn ab Kandersteg\n- Sunnbüel: Luftseilbahn Richtung Gemmi\n- Blausee: von dort kommt die Forelle unserer Karte\n- Gasterntal: in Selden steht das Berghotel Gasterntal der Familie\n'
            'Bei Regen: Hallenbad und Saunen im Waldhotel Doldenhorn gegenüber, danach ein Fondue in der Stube. Die Betriebszeiten der Bahnen stehen auf oeschinensee.ch und sunnbuel.ch.',
         en='Around Kandersteg:\n- Oeschinensee: by gondola from Kandersteg\n- Sunnbüel: cable car towards the Gemmi\n- Blausee: where the trout on our menu comes from\n- Gasterntal: home of the family’s Berghotel Gasterntal in Selden\n'
            'When it rains: indoor pool and saunas at the Waldhotel Doldenhorn opposite, then a fondue in the Stube. Lift times are on oeschinensee.ch and sunnbuel.ch.',
         k=['spa', 'essen']),
    dict(id='gutschein', s=['gutschein', 'geschenk', 'schenken', 'voucher', 'gift', 'bon cadeau', 'cadeau'],
         de='Gerne stellen wir Ihnen einen Geschenkgutschein aus, zum Beispiel eine Übernachtung mit Frühstück für 2 Personen. Wertgutschein, Abend in der Stube oder Gourmetaufenthalt '
            '(ab CHF 450.00 pro Person) bestellen Sie gleich auf unserer Seite unter Zimmer, Geschenkgutscheine.',
         en='We gladly issue gift vouchers, for example one night with breakfast for two. Value vouchers, an evening in the Stube or the gourmet stay (from CHF 450.00 per person) can be ordered on our website.',
         k=['zimmer', 'essen']),
    dict(id='feste', s=['fest', 'feier', 'geburtstag', 'hochzeit', 'familienfest', 'bankett', 'gesellschaft', 'gruppe', 'anlass', 'apéro', 'apero',
                        'wedding', 'birthday', 'party', 'celebrat', 'group', 'mariage', 'anniversaire', 'seminar', 'sitzung', 'tagung', 'meeting', 'konferenz', 'conference', 'réunion'],
         de='Für Ihr Fest:\n- Jungestube: 25 Plätze, für Familienfeste und Sitzungen\n- Chäs- und Wystube: 40 Plätze\n- Bernerstuben im 1. Stock für den besonderen Anlass\n'
            'Hochzeiten, Bankette und Seminare richtet das Waldhotel Doldenhorn gleich gegenüber aus. Anfragen gehen an ' + MAIL_FESTE + '.',
         en='For your celebration:\n- Jungestube: 25 seats, for family parties and meetings\n- Chäs- und Wystube: 40 seats\n- Bernerstuben on the first floor for special occasions\n'
            'Weddings, banquets and seminars are hosted by the Waldhotel Doldenhorn just opposite. Please send enquiries to ' + MAIL_FESTE + '.',
         k=['tisch', 'karte']),
    dict(id='kontakt', s=['kontakt', 'telefon', 'anrufen', 'erreiche', '~nummer', '~mail', 'rezeption', 'erreichen', 'contact', 'phone', 'call', 'reception', 'téléphone'],
         de='Die Rezeption erreichen Sie am Telefon unter ' + TEL + ' oder per Mail an ' + MAIL + '. Die Adresse: ' + ADRESSE + '.',
         en='You can reach reception by phone on ' + TEL + ' or by email at ' + MAIL + '. Address: ' + ADRESSE + '.',
         k=['anreise', 'tisch']),
    dict(id='bedingungen', s=['check-in', 'checkin', 'check in', 'check-out', 'checkout', 'einchecken', 'auschecken', 'storn', 'annull', 'absagen', 'cancel', 'late arrival', 'spät ankommen', 'spaet ankommen', 'annulation'],
         de='Die Bedingungen Ihrer Buchung, auch zu Storno und Ankunftszeit, stehen in der Bestätigung der Buchungsseite. Für alles Weitere hilft Ihnen die Rezeption gern: ' + TEL + ' oder ' + MAIL + '.',
         en='The conditions of your booking, including cancellation and arrival time, are in the confirmation from the booking page. For anything else, reception will gladly help: ' + TEL + ' or ' + MAIL + '.',
         k=['kontakt', 'buchen']),
    dict(id='zugang', s=['rollstuhl', 'barrierefrei', 'lift', 'aufzug', 'treppe', 'wheelchair', 'accessib', 'elevator'],
         de='Das Ruedihus ist ein Holzhaus von 1753 mit Stuben im Parterre und im 1. Stock. Was für Sie gut passt, besprechen Sie am besten direkt mit der Rezeption: ' + TEL + '.',
         en='The Ruedihus is a wooden house from 1753 with Stuben on the ground and first floor. Please talk to reception about what suits you best: ' + TEL + '.',
         k=['kontakt', 'spa']),
    dict(id='haus', s=['geschichte', 'baujahr', 'alt ist', '1753', 'historisch', 'history', 'old is', 'histoire'],
         de='Das Ruedihus wurde 1753 durch Peter Germann erbaut und gilt als Spitzenleistung der Zimmermannskunst im 18. Jahrhundert. Es ist Mitglied der Swiss Historic Hotels. Die ganze Geschichte steht auf unserer Seite unter Das Haus.',
         en='The Ruedihus was built in 1753 by Peter Germann and is considered a masterpiece of 18th-century carpentry. It is a member of Swiss Historic Hotels. The full story is on our website under Das Haus.',
         k=['zimmer', 'essen']),
    dict(id='kinder', s=['kinder', 'kind', 'familie', 'baby', 'kinderbett', 'children', 'child', 'kids', 'family', 'enfant'],
         de='Für ein Familienfest gibt es die Jungestube mit 25 Plätzen. Was für Kinder im Zimmer möglich ist, zum Beispiel ein zusätzliches Bett, sagt Ihnen die Rezeption gern: ' + TEL + '.',
         en='For a family celebration there is the Jungestube with 25 seats. Reception will gladly tell you what is possible for children in the room: ' + TEL + '.',
         k=['zimmer', 'feste']),
]
# Knopf-Texte je Thema (die Frage, die der Knopf stellt; trifft selbst wieder dieses Thema)
KNOPF = {'essen': ('Was gibt es zu essen?', 'What is there to eat?'), 'oeffnung': ('Wann hat das Restaurant offen?', 'When is the restaurant open?'),
         'karte': ('Was steht auf dem Schpiszettel?', 'What is on the menu?'), 'tisch': ('Tisch in der Stube reservieren', 'Book a table in the Stube'),
         'zimmer': ('Welche Zimmer haben Sie?', 'Which rooms do you have?'), 'buchen': ('Zimmer buchen', 'Book a room'),
         'fruehstueck': ('Wie ist das Frühstück?', 'What about breakfast?'), 'spa': ('Kann ich das Spa im Doldenhorn benutzen?', 'Can I use the spa at the Doldenhorn?'),
         'anreise': ('Wie komme ich zu Ihnen?', 'How do I get to you?'), 'parken': ('Gibt es einen Parkplatz?', 'Is there parking?'),
         'ausfluege': ('Was kann ich heute unternehmen?', 'What can I do today?'), 'feste': ('Ein Fest bei Ihnen feiern', 'Celebrate with you'),
         'kontakt': ('Wie erreiche ich die Rezeption?', 'How do I reach reception?')}
OHNE = dict(
    de='Das beantwortet Ihnen unsere Rezeption am liebsten selbst: ' + TEL + ' oder ' + MAIL + '. Gern helfe ich Ihnen hier mit diesen Themen weiter:',
    en='Our reception will gladly answer that personally: ' + TEL + ' or ' + MAIL + '. I can help you right here with these topics:',
    k=['essen', 'zimmer', 'anreise'])
EN_WOERTER = ['the', 'is', 'are', 'do', 'does', 'can', 'could', 'you', 'what', 'where', 'how', 'when', 'which', 'have', 'there', 'room', 'breakfast', 'please', 'i ', 'my', 'is there', 'open']
DE_WOERTER = ['der', 'die', 'das', 'ist', 'sind', 'kann', 'können', 'ich', 'sie', 'wie', 'wo', 'wann', 'gibt', 'es', 'haben', 'ein', 'eine', 'bitte', 'zimmer', 'mit', 'und', 'bei', 'für']


def norm(t):
    t = ' ' + str(t or '').lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    t = re.sub(r'[éèê]', 'e', t); t = re.sub(r'[àâ]', 'a', t); t = re.sub(r'[^a-z0-9\-\s]', ' ', t)
    return re.sub(r'\s+', ' ', t) + ' '


def sprache(f, sp='de'):
    n = norm(f)
    e = sum(1 for w in EN_WOERTER if ' ' + norm(w).strip() + ' ' in n); d = sum(1 for w in DE_WOERTER if ' ' + norm(w).strip() + ' ' in n)
    return 'en' if e > d else 'de' if d > e else ('en' if sp in ('en', 'fr') else 'de')


def thema(f):
    n, best, pb = norm(f), None, 0
    for t in THEMEN:
        p = 0
        for s_ in t['s']:
            g = s_.startswith('~'); k = norm(s_[1:] if g else s_).strip()
            if k and ' ' + k in n:
                p += 1 if g else (2 if len(k) > 4 else 1)
        if p > pb:
            pb, best = p, t
    return best


def antwort(f, sp='de'):
    """{text, knoepfe, maske?, buch}: dieselbe Zuordnung wie im Browser (MATCH_JS)"""
    l = sprache(f, sp); t = thema(f); i = 1 if l == 'en' else 0
    if not t:
        return dict(text=OHNE[l], knoepfe=[KNOPF[k][i] for k in OHNE['k']], buch='ohne')
    a = dict(text=t[l], knoepfe=[KNOPF[k][i] for k in t['k']], buch=t['id'])
    if t.get('maske'):
        a['maske'] = {}
    return a


def buch():
    for t in THEMEN:
        assert t['de'] and t['en'], t['id']
        for x in t['k']:
            assert x in KNOPF, (t['id'], x)
    for k, (de, en) in KNOPF.items():   # jeder Knopf trifft sein eigenes Thema, auf Deutsch und Englisch
        assert thema(de) and thema(de)['id'] == k, ('Knopf de', k, de, thema(de) and thema(de)['id'])
        assert thema(en) and thema(en)['id'] == k, ('Knopf en', k, en, thema(en) and thema(en)['id'])
    return dict(themen=THEMEN, knopf=KNOPF, ohne=OHNE, en=EN_WOERTER, de=DE_WOERTER, tel=TEL, mail=MAIL)


MATCH_JS = r"""
/* Zuordnung (gleich wie in api/gast.py): Text vereinfachen, Stichwörter zählen (längere zählen doppelt), bestes Thema; Sprache aus der Frage. */
function rhNorm(s) { return (' ' + String(s || '').toLowerCase().replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue').replace(/ß/g, 'ss').replace(/[éèê]/g, 'e').replace(/[àâ]/g, 'a').replace(/[^a-z0-9\-\s]/g, ' ').replace(/\s+/g, ' ') + ' '); }
function rhSprache(f, sp) { var n = rhNorm(f), e = 0, d = 0; B.en.forEach(function (w) { if (n.indexOf(' ' + rhNorm(w).trim() + ' ') > -1) e++; }); B.de.forEach(function (w) { if (n.indexOf(' ' + rhNorm(w).trim() + ' ') > -1) d++; });
  if (e > d) return 'en'; if (d > e) return 'de'; return sp === 'en' || sp === 'fr' ? 'en' : 'de'; }
function rhThema(f) { var n = rhNorm(f), best = null, pb = 0;
  B.themen.forEach(function (t) { var p = 0; t.s.forEach(function (s) { var g = s.charAt(0) === '~', k = rhNorm(g ? s.slice(1) : s).trim(); if (k && n.indexOf(' ' + k) > -1) p += g ? 1 : k.length > 4 ? 2 : 1; }); if (p > pb) { pb = p; best = t; } });
  return best; }
function rhAntwort(f, sp) { var l = rhSprache(f, sp), t = rhThema(f), i = l === 'en' ? 1 : 0;
  if (!t) return { text: B.ohne[l], knoepfe: B.ohne.k.map(function (k) { return B.knopf[k][i]; }), buch: 'ohne' };
  return { text: t[l], knoepfe: t.k.map(function (k) { return B.knopf[k][i]; }), maske: t.maske ? {} : undefined, buch: t.id }; }
"""

BROWSER = r"""/* Rezeption im Chat · Antwortbuch des Landgasthof Ruedihus (gebaut von _werkzeuge/reception/online/antwortbuch.py, nicht von Hand ändern).
   Robert 19.10.2026 05:10: feste Antworten, solange die KI kein Guthaben hat. Liegt vor assets/js/gast.js: Antwortet /api/gast nicht, mit Fehler oder nur mit
   dem Notsatz, antwortet der Chat sofort aus diesem Buch. Unter der Antwort stehen Knöpfe mit passenden Folgefragen. Ändert gast.js (Vorlage der Familie) nicht. */
(function () {
  var B = /*BUCH*/;
%MATCH%
  window.rhAntwort = rhAntwort;
  var NOT = /keine gesicherte Auskunft|no confirmed information|pas d.information confirm/i;
  var roh = window.fetch && window.fetch.bind(window);
  if (!roh) return;
  function antwortAus(body) {
    var d = {}; try { d = JSON.parse(body || '{}'); } catch (e) {}
    var m = (d.messages || []).filter(function (x) { return x.role === 'user'; }), f = m.length ? m[m.length - 1].content : '';
    var a = rhAntwort(f, d.sprache || 'de'); merke(a.knoepfe); return a;
  }
  function json(a) { return new Response(JSON.stringify(a), { status: 200, headers: { 'content-type': 'application/json' } }); }
  window.fetch = function (u, o) {
    var url = typeof u === 'string' ? u : (u && u.url) || '';
    if (!/\/api\/gast(\?|$)/.test(url) || !o || String(o.method || '').toUpperCase() !== 'POST') return roh(u, o);
    var body = o.body, ersatz = function () { return json(antwortAus(body)); };
    return roh(u, o).then(function (r) {
      if (!r.ok) return ersatz();
      return r.clone().json().then(function (a) { if (!a || !a.text || a.grenze || NOT.test(a.text)) return ersatz(); if (a.knoepfe) merke(a.knoepfe); return r; }, ersatz);
    }, ersatz);
  };
  /* Knöpfe unter der Antwort: erst wenn sie fertig getippt ist */
  var offen = null;
  function merke(k) { offen = (k || []).slice(0, 3); setTimeout(warte, 60); }
  function warte() {
    var lauf = document.querySelector('.gast__lauf'); if (!lauf || !offen) return;
    var letzte = lauf.lastElementChild, t0 = 0, alt = '';
    (function blick() {
      var b = lauf.lastElementChild; if (!b) return;
      if (b.classList.contains('gast__b--denkt')) return setTimeout(blick, 120);
      var jetzt = b.textContent; if (jetzt !== alt) { alt = jetzt; t0 = Date.now(); return setTimeout(blick, 120); }
      if (Date.now() - t0 < 350) return setTimeout(blick, 120);
      if (!offen || document.documentElement.classList.contains('gast-bucht')) { offen = null; return; }
      zeige(lauf, offen); offen = null;
    })();
  }
  var PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>';
  function zeige(lauf, liste) {
    if (!liste.length) return; var alt = lauf.querySelector('.gast__vor'); if (alt) alt.remove();
    var v = document.createElement('div'); v.className = 'gast__vor';
    liste.forEach(function (f) {
      var k = document.createElement('button'); k.type = 'button'; k.innerHTML = '<span></span>' + PF; k.firstChild.textContent = f;
      k.addEventListener('click', function () {
        var fen = lauf.closest('.gast') || document, feld = fen.querySelector('.gast__feld textarea, .gast__feld input'), form = fen.querySelector('form');
        if (!feld || !form) return; v.remove(); feld.value = f; feld.dispatchEvent(new Event('input', { bubbles: true }));
        if (form.requestSubmit) form.requestSubmit(); else form.dispatchEvent(new Event('submit', { cancelable: true }));
      });
      v.appendChild(k);
    });
    lauf.appendChild(v); try { lauf.scrollTop = lauf.scrollHeight; } catch (e) {}
  }
})();
"""


def main():
    b = buch()
    open(os.path.join(HIER, 'gast_antworten.json'), 'w', encoding='utf-8').write(json.dumps(b, ensure_ascii=False, indent=1))
    js = BROWSER.replace('/*BUCH*/', json.dumps(b, ensure_ascii=False)).replace('%MATCH%', MATCH_JS)
    open(os.path.join(ROOT, 'assets', 'js', 'gast-antworten.js'), 'w', encoding='utf-8').write(js)
    print('Antwortbuch:', len(b['themen']), 'Themen, DE/EN →', 'gast_antworten.json, assets/js/gast-antworten.js')


if __name__ == '__main__':
    main()
