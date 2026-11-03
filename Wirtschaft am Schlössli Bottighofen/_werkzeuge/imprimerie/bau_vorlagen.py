#!/usr/bin/env python3
"""Die Hausdruckerei · Wirtschaft am Schlössli Bottighofen: Katalog und Vorlagen des Hauses.
   python3 bau_vorlagen.py → katalog.js, haeuser/schloessli/vorlagen/*.json + index.json, Beispielinhalte in start.js (INHALT) und vorlagen.js (DS.BEISPIEL),
   api/_daten/schloessli-wissen.txt (Wortlaut für die Probe-Antworten).
Jeder Satz, jede Zahl, jedes Gericht und jeder Termin steht so in website/inhalt/*.json (haus.json, karte.json, lunch.json, laestermeile.json, wein.json,
bankett.json) oder in den Seiten der Website. Keine Preise (Regel des Hauses: Preise nur auf den Karten des Kartenpults). Schweizer Schreibung (ss), Sie-Form.
Prüfung am Ende: jede Zahl muss in den Quellen vorkommen, kein «ß» in den Texten."""
import glob, html, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HIER, 'haeuser', 'schloessli')
PROJ = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(PROJ, 'website')
INH = os.path.join(WEB, 'inhalt')
J_ = lambda f: json.load(open(os.path.join(INH, f), encoding='utf-8'))
H, KARTE, LUNCH, LAESTER, WEIN, BANKETT = J_('haus.json'), J_('karte.json'), J_('lunch.json'), J_('laestermeile.json'), J_('wein.json'), J_('bankett.json')

ss = lambda t: str(t or '').replace('ß', 'ss')
glied = lambda t: ss(t).replace(' – ', ' · ').replace('–', ' · ').replace('  ', ' ').strip()
ADR = '%s · %s' % (H['strasse'], H['ort'])
TEL = H['telefon']
IG = H['instagram_name']
MAIL = H['mail']
ZEIT = '%s · %s' % (H['zeiten']['tage'], H['zeiten']['offen'])
KUECHE = 'Küche %s und %s' % tuple(H['zeiten']['kueche'])
RUHE = H['zeiten']['ruhetag']
ZEILE = 'Direkt im Hafen von Bottighofen'
S0 = {"ausr": "c", "rahmen": "einfach", "titel": 1, "zeichen": 1, "ecke": 2.4, "bild": 0.56}
S1 = {"ausr": "c", "rahmen": "ohne", "titel": 1.04, "zeichen": .95, "ecke": 2.4, "bild": 0.56}


def v(n, wo, fmt, vorlage, ton, inhalt, rueck=None, stil=S0):
    return {"n": n, "wo": wo, "format": fmt, "vorlage": vorlage, "ton": ton, "inhalt": inhalt, "rueck": rueck, "stil": stil}


def land(name):
    return next(l for l in KARTE['laender'] if l['land'] == name)


def gerichte(l, n=5):
    return [{"name": ss(g['name']), "detail": glied(g['text']), "preis": ""} for g in l['gerichte'][:n]]


def erzeuger(gruppe, region, n=5):
    for g in WEIN['gruppen']:
        if g['titel'] != gruppe:
            continue
        for r in g['regionen']:
            if (r['titel'] or '') == region or (region is None and r['titel'] is None):
                out = []
                for e in r['erzeuger'][:n]:
                    w = e['weine'][0] if e.get('weine') else {}
                    out.append({"name": ss(e['name']).replace(' – ', ' · ').replace(' - ', ' · '), "detail": ss(w.get('name', '')).replace('«', '').replace('»', ''), "preis": ""})
                return out
    raise SystemExit('Wein fehlt: %s %s' % (gruppe, region))


LUNCH_G = [{"gang": "", "name": ss(g['name']), "detail": glied(g['text'])} for g in LUNCH['gaenge']]
BANK = {m['name']: m for m in BANKETT['menues']}
bank_liste = lambda m, n=5: [{"name": ss(g['name']).replace('„', '«').replace('“', '»'), "detail": glied(g['text']), "preis": ""} for g in BANK[m]['gerichte'][:n]]
TAPAS = [{"name": ss(e['name']), "detail": glied(re.sub(r'\s+[A-Z]{1,2}(/[A-Z]{1,2})*$', '', e['text'])), "preis": ""} for e in LAESTER['gruppen'][0]['eintraege']]
STAERKUNG = [{"name": ss(e['name']), "detail": glied(re.sub(r'\s+[A-Z]{1,2}(/[A-Z]{1,2})*$', '', e['text'])).replace('„', '«').replace('“', '»'), "preis": ""} for e in LAESTER['gruppen'][1]['eintraege']]
KREUZ = H['anlaesse'][0]

# ---------------- Abteilungen ----------------
RESTAURANT = [
    v('Lunch-Menü', 'am Tisch, am Mittag', 'dlh', 'menue', 'hell', {"titel": "Lunch-Menü", "ueber": "Drei Gänge am Mittag", "liste": LUNCH_G, "fuss": ADR}),
    v('Aus Frankreich', 'Einleger zur Karte', 'a5h', 'karte', 'creme', {"ueber": "Die Karte · Frankreich", "titel": "Aus Frankreich", "text": "", "liste": gerichte(land('Frankreich'), 4), "fuss": ""}),
    v('Aus Italien', 'Einleger zur Karte', 'a5h', 'karte', 'dunkel', {"ueber": "Die Karte · Italien", "titel": "Aus Italien", "text": "", "liste": gerichte(land('Italien'), 4), "fuss": ""}),
    v('Iberische Halbinsel', 'Einleger zur Karte', 'a5h', 'karte', 'hell', {"ueber": "Die Karte · Spanien und Portugal", "titel": "Iberische Halbinsel", "text": "", "liste": gerichte(land('Iberische Halbinsel'), 4), "fuss": ""}),
    v('Die Klassiker', 'Einleger zur Karte', 'a5h', 'karte', 'creme', {"ueber": "Immer auf der Karte", "titel": "Die Klassiker", "text": "", "liste": gerichte(land('Klassiker'), 4), "fuss": ""}),
    v('Eine Reise ans Mittelmeer', 'Tischaufsteller', 'a6h', 'buehne', 'dunkel', {"bild": "thon", "ueber": "Die Küche von Monika Huber", "titel": "Eine Reise ans Mittelmeer",
      "text": "Frankreich, Italien, die Iberische Halbinsel: mediterrane Küche mit frischen, hochwertigen Zutaten.", "aktion": KUECHE}),
    v('Vegetarisch', 'Hinweiskarte am Tisch', 'a6h', 'aushang', 'creme', {"ueber": "Auf der Karte", "titel": "Vegetarisch",
      "text": "VEG = vegetarisch, OVEG = als vegetarische Option verfügbar. Für weitere vegetarische Optionen berät Sie gerne unser Service.", "aktion": ""}),
]
LAESTERMEILE = [
    v('Tapas durchgehend', 'an der Bar', 'a5h', 'karte', 'dunkel', {"ueber": "Die Lästermeile", "titel": "Tapas durchgehend", "text": "", "liste": TAPAS, "fuss": ""}),
    v('Zur Stärkung & Süsses', 'an der Bar', 'a5h', 'karte', 'creme', {"ueber": "Die Lästermeile", "titel": "Zur Stärkung & Süsses", "text": "", "liste": STAERKUNG[:4], "fuss": ""}),
    v('Den ganzen Tag', 'Tischaufsteller an der Bar', 'a6h', 'buehne', 'dunkel', {"bild": "bar", "ueber": "Die Lästermeile", "titel": "Den ganzen Tag",
      "text": "Den ganzen Tag durchgängig bieten wir die Karte der Lästermeile an.", "aktion": ZEIT}),
    v('Die Lästermeile', 'Instagram', 'insta', 'geteilt', 'dunkel', {"bild": "regal", "ueber": "Die Bar am Hafen", "titel": "Die Lästermeile",
      "text": "Zementfliesen, eine Reihe Stühle und der Blick auf den Bootshafen und die Seepromenade.", "aktion": IG}),
    v('Lästermeile · Aushang', 'an der Tür', 'a4h', 'aushang', 'dunkel', {"ueber": "Die Bar am Hafen", "titel": "Die Lästermeile",
      "text": "Die Küchenzeiten betreffen unsere grosse A-la-carte-Karte. Die Karte der Lästermeile gibt es den ganzen Tag.", "aktion": ZEIT}),
]
WEINE = [
    v('Bündner Herrschaft', 'Weinempfehlung am Tisch', 'dlh', 'karte', 'dunkel', {"ueber": "Jonas Volpert empfiehlt", "titel": "Bündner Herrschaft", "text": "", "liste": erzeuger('Rotwein', 'Bündner Herrschaft', 4), "fuss": ""}),
    v('Burgund', 'Weinempfehlung am Tisch', 'dlh', 'karte', 'creme', {"ueber": "Jonas Volpert empfiehlt", "titel": "Burgund", "text": "", "liste": erzeuger('Weisswein', 'Burgund', 4), "fuss": ""}),
    v('Champagne', 'Weinempfehlung am Tisch', 'dlh', 'karte', 'hell', {"ueber": "Jonas Volpert empfiehlt", "titel": "Champagne", "text": "", "liste": erzeuger('Champagner & Schaumwein', None, 4), "fuss": ""}),
    v('Thurgau und Bodensee', 'Weinempfehlung am Tisch', 'dlh', 'karte', 'creme', {"ueber": "Aus der Nachbarschaft", "titel": "Thurgau und Bodensee", "text": "",
      "liste": erzeuger('Weisswein', 'Thurgau', 2) + erzeuger('Weisswein', 'Bayrischer Bodensee', 2), "fuss": ""}),
    v('Der Weinkeller', 'Instagram', 'insta', 'fenster', 'dunkel', {"bild": "wein", "ueber": "GaultMillau, 30.03.2025", "titel": "Der Weinkeller",
      "unter": "Sommelier Jonas Volpert", "text": ss(H['zitat_gm_keller'])}),
    v('Jonas Volpert', 'Tischaufsteller', 'a6h', 'buehne', 'dunkel', {"bild": "jonas", "ueber": "Gastgeber & Sommelier", "titel": "Jonas Volpert",
      "text": ss(H['zitat_jonas']), "aktion": ""}),
]
ANLAESSE_ABT = [
    v('Four-Hands auf dem Rhein', 'Aushang an der Tür', 'a4h', 'aushang', 'dunkel', {"ueber": "13. bis 15. November 2026", "titel": "Four-Hands an Bord",
      "text": "Monika Huber und Dieter Koschina kochen auf der Excellence Countess. Unser Restaurant ist über diese drei Tage geschlossen, da unser Team mit an Bord ist.", "aktion": ""}),
    v('Excellence Gourmetkreuzfahrt', 'Einladung an Stammgäste', 'q148', 'einladung', 'dunkel', {"ueber": "Excellence Gourmetkreuzfahrt", "titel": "Four-Hands an Bord",
      "wann": "13. bis 15. November 2026", "wo": "Basel · Strassburg · Basel", "text": "Welcome-Apéro, Moderation über den ganzen Abend, Live-Musik, Gala-Dinner und DJ.", "aktion": "Buchung über excellence.ch"}),
    v('Die Reise', 'zum Mitnehmen', 'a5h', 'programm', 'dunkel', {"ueber": "Excellence Gourmetkreuzfahrt", "titel": "Die Reise",
      "termine": [{"wann": "Freitag, 13. November · 15:00", "was": "Start in Basel, über Nacht nach Strassburg", "wo": "Excellence Countess"},
                  {"wann": "Samstag, 14. November", "was": "Den selben Weg wieder zurück, Gala-Dinner mit Four-Hands", "wo": "Monika Huber · Dieter Koschina"},
                  {"wann": "Sonntag, 15. November · 14:00", "was": "Ankunft in Basel", "wo": ""}]}),
    v('Banketts & Gruppen', 'Angebot zum Mitschicken', 'a5h', 'buehne', 'dunkel', {"bild": "gaststube", "ueber": "Auf zwei Etagen · bis zu 26 Personen", "titel": "Banketts & Gruppen",
      "text": "Gerne übernehmen wir die Bewirtung Ihrer Familien- oder Firmenfeier. Sie geben den Rahmen vor, ob Tavolata oder gesetztes Menü.", "aktion": TEL}),
    v('Bankettmenü Herbst', 'Vorschlag zum Mitschicken', 'a5h', 'menue', 'creme', {"titel": "Herbst", "ueber": "Bankettmenü", "liste": [dict(gang="", name=x['name'], detail=x['detail']) for x in bank_liste('Herbst')], "fuss": ADR}),
    v('Bankettmenü Frühling', 'Vorschlag zum Mitschicken', 'a5h', 'menue', 'hell', {"titel": "Frühling", "ueber": "Bankettmenü", "liste": [dict(gang="", name=x['name'], detail=x['detail']) for x in bank_liste('Frühling')], "fuss": ADR}),
    v('Bankettmenü Sommer', 'Vorschlag zum Mitschicken', 'a5h', 'menue', 'dunkel', {"titel": "Sommer", "ueber": "Bankettmenü", "liste": [dict(gang="", name=x['name'], detail=x['detail']) for x in bank_liste('Sommer')], "fuss": ADR}),
    v('Tavolata oder Menü', 'Angebot zum Mitschicken', 'a5h', 'programm', 'creme', {"ueber": "Banketts & Gruppen", "titel": "So planen wir Ihr Fest",
      "termine": [{"wann": "Anfrage", "was": "Datum, Uhrzeit und Personenzahl", "wo": ""}, {"wann": "Speisenform", "was": "Tavolata oder gesetztes Menü", "wo": ""},
                  {"wann": "Gänge", "was": "Aus den Menüs drei bis fünf Gerichte wählen", "wo": ""}, {"wann": "Gespräch", "was": "Gerne auch vor Ort in Ruhe", "wo": TEL}]}),
]
HAFEN = [
    v('Postkarte Bottighofen', 'zum Mitnehmen, zum Verschicken', 'a6q', 'ansicht', 'dunkel', {"bild": "bootshafen", "titel": "Bottighofen", "unter": "Wirtschaft am Schlössli · Am Hafen"},
      {"vorlage": "kartengruss", "inhalt": {"titel": "Grüsse vom See", "text": "Direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen."}}),
    v('Postkarte Bodensee', 'zum Mitnehmen, zum Verschicken', 'a6q', 'ansicht', 'dunkel', {"bild": "saentis", "titel": "Bodensee", "unter": "Wirtschaft am Schlössli · Bottighofen"},
      {"vorlage": "kartengruss", "inhalt": {"titel": "Grüsse vom See", "text": "Direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen."}}),
    v('Postkarte Morgen am See', 'zum Mitnehmen, zum Verschicken', 'a6q', 'ansicht', 'hell', {"bild": "morgen", "titel": "Bottighofen", "unter": "Morgen am See"},
      {"vorlage": "kartengruss", "inhalt": {"titel": "Grüsse vom Hafen", "text": "Die schönste Terrasse am Bodensee, sagt Christian Kuchler."}}),
    v('Die schönste Terrasse', 'Plakat A3', 'a3h', 'buehne', 'dunkel', {"bild": "start", "ueber": "Christian Kuchler", "titel": "Die schönste Terrasse am Bodensee",
      "text": ss(H['satz_lage']), "aktion": ZEIT}),
    v('Unter den Platanen', 'Instagram', 'insta', 'fenster', 'creme', {"bild": "platanen", "ueber": "Die Seeterrasse", "titel": "Unter den Platanen",
      "unter": "GaultMillau", "text": "«" + ss(H['zitat_gm_terrasse']).capitalize() + "»"}),
    v('Das Abendschiff', 'Story', 'story', 'fenster', 'dunkel', {"bild": "abendschiff", "ueber": "Bodensee", "titel": "Abends am See", "unter": "Wirtschaft am Schlössli",
      "text": "Ein Kursschiff im Abendlicht, dahinter das Säntis-Massiv."}),
]
HAUS = [
    v('Flyer des Hauses', 'zum Mitnehmen', 'a6h', 'buehne', 'dunkel', {"bild": "start", "ueber": "Wirtschaft am Schlössli", "titel": ZEILE,
      "text": ss(H['satz_reise']), "aktion": ZEIT}, {"vorlage": "rueckseite", "inhalt": {"text": ZEIT}}),
    v('Öffnungszeiten', 'an der Tür', 'a4h', 'aushang', 'dunkel', {"ueber": "Wirtschaft am Schlössli", "titel": "Donnerstag bis Montag",
      "text": "%s, %s. %s. %s." % ('11:30 Uhr - 23:00 Uhr', 'durchgehend', KUECHE, RUHE), "aktion": TEL}),
    v('Auszeichnungen', 'für Medien, an der Bar', 'a5h', 'karte', 'dunkel', {"ueber": "Was die Guides schreiben", "titel": "Auszeichnungen", "text": "",
      "liste": [{"name": a['wer'], "detail": ss(a['was']) + (' · ' + ss(a['zusatz']) if a['zusatz'] else ''), "preis": ""} for a in H['auszeichnungen']], "fuss": ""}),
    v('Monika Huber', 'Instagram', 'insta', 'fenster', 'creme', {"bild": "moni", "ueber": "Küchenchefin", "titel": "Monika Huber", "unter": "GaultMillau · Entdeckung des Jahres 2026",
      "text": "Aus Südtirol, gelernt in der Vila Joya an der Algarve, seit April 2025 mit ihrer eigenen Küche am See."}),
    v('Das Team', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "team", "ueber": "Wirtschaft am Schlössli", "titel": "Das Team",
      "text": "Gastgeber und Sommelier Jonas Volpert, Küchenchefin Monika Huber, Sous-Chef Lukas Siebel, Entremetier Marco Reisinger und Ole Sass im Service.", "aktion": IG}),
    v('Pressemappe', 'für Medien', 'a4h', 'deckel', 'dunkel', {"ueber": "Pressemappe", "titel": "Wirtschaft am Schlössli", "unter": "by Christian Kuchler · Bottighofen",
      "text": "Ein Restaurant mit Seeterrasse direkt im Hafen von Bottighofen, im ehemaligen Hafenmeistergebäude."}),
    v('Statt eines Schilds ein Besen', 'Aushang zur Geschichte', 'a4h', 'aushang', 'creme', {"ueber": "Ende des 17. Jahrhunderts", "titel": "Ein Besen statt Schild",
      "text": ss(H['besen'][0]) + ' ' + ss(H['besen'][1]), "aktion": ""}),
    v('Der Weg zum Hafen', 'zum Mitnehmen', 'a6h', 'aushang', 'hell', {"ueber": ADR, "titel": "Der Weg zum Hafen",
      "text": "Am Kreisverkehr beim Restaurant Bären in die Seestrasse Richtung Hafen, über den Bahnübergang bis zu unserem Parkplatz. Der Bahnhof Bottighofen ist nah.", "aktion": TEL}),
]
GESCHENK = [
    v('Gutschein', 'zum Verschenken', 'dlq', 'gutschein', 'dunkel', {"titel": "Ein Essen am See", "unter": "Wirtschaft am Schlössli", "wert": "",
      "text": "Für einen Tisch auf der Terrasse oder in der Gaststube, direkt im Hafen von Bottighofen."},
      {"vorlage": "gutscheinrueck", "inhalt": {"text": "Einzulösen in der Wirtschaft am Schlössli. Reservation unter " + TEL + "."}}),
    v('Gutschein · hell', 'zum Verschenken', 'dlq', 'gutschein', 'hell', {"titel": "Ein Essen am See", "unter": "Wirtschaft am Schlössli", "wert": "",
      "text": "Für einen Tisch auf der Terrasse oder in der Gaststube, direkt im Hafen von Bottighofen."},
      {"vorlage": "gutscheinrueck", "inhalt": {"text": "Einzulösen in der Wirtschaft am Schlössli. Reservation unter " + TEL + "."}}),
    v('Gutschein Lästermeile', 'zum Verschenken', 'dlq', 'gutschein', 'creme', {"titel": "Ein Abend an der Bar", "unter": "Die Lästermeile", "wert": "",
      "text": "Tapas, ein Glas Wein und der Blick auf den Bootshafen."},
      {"vorlage": "gutscheinrueck", "inhalt": {"text": "Einzulösen an der Lästermeile der Wirtschaft am Schlössli, Donnerstag bis Montag."}}),
    v('Gutschein bestellen', 'Aushang an der Bar', 'a6h', 'aushang', 'creme', {"ueber": "Zum Verschenken", "titel": "Gutscheine",
      "text": "Wir senden Ihnen eine Bestätigung, sobald der Gutschein versendet wurde. Bestellung über die Website oder am Tisch.", "aktion": MAIL}),
]

ABTEILUNGEN = [
    {"k": "restaurant", "t": "Restaurant & Karte", "satz": "Lunch-Menü, die Länder der Karte, die Klassiker: Einleger und Aufsteller ohne Preise.", "foto": "tortelloni", "vorlagen": RESTAURANT},
    {"k": "laestermeile", "t": "Die Lästermeile", "satz": "Die Bar mit durchgehender Karte: Tapas, Stärkung und Süsses, Aufsteller und Aushang.", "foto": "bar", "vorlagen": LAESTERMEILE},
    {"k": "wein", "t": "Wein", "satz": "Weinempfehlungen von Jonas Volpert: Bündner Herrschaft, Burgund, Champagne und die Nachbarschaft.", "foto": "wein", "vorlagen": WEINE},
    {"k": "anlaesse", "t": "Anlässe & Banketts", "satz": "Die Gourmetkreuzfahrt, Banketts auf zwei Etagen, die Bankettmenüs der Jahreszeiten.", "foto": "gaststube", "vorlagen": ANLAESSE_ABT},
    {"k": "hafen", "t": "Hafen & Terrasse", "satz": "Postkarten vom Hafen, die Terrasse unter den Platanen, Abende am See.", "foto": "bootshafen", "vorlagen": HAFEN},
    {"k": "haus", "t": "Das Haus", "satz": "Zeiten, Weg, Team, Auszeichnungen, die Geschichte vom Besen und die Pressemappe.", "foto": "haus", "vorlagen": HAUS},
    {"k": "geschenk", "t": "Gutscheine", "satz": "Ein Essen am See oder ein Abend an der Lästermeile zum Verschenken, mit Rückseite.", "foto": "apero", "vorlagen": GESCHENK},
]

HINWEISE = [
    v('Betriebsferien im Winter', 'aushängen ab Dezember', 'a4h', 'aushang', 'dunkel', {"ueber": "22. Dezember 2026 - 10. Februar 2027", "titel": "Wir machen Ferien",
      "text": "Vom 22. Dezember 2026 bis zum 10. Februar 2027 bleibt die Wirtschaft am Schlössli geschlossen. Ab dem 11. Februar sind wir wieder für Sie da.", "aktion": IG}),
    v('Geschlossen wegen Kreuzfahrt', 'aushängen im November', 'a4h', 'aushang', 'creme', {"ueber": "13. - 15. November", "titel": "Das Team ist an Bord",
      "text": "Unser Restaurant ist über diese drei Tage geschlossen, da unser Team geschlossen mit an Bord ist. Ab Montag, 16. November, sind wir wieder da.", "aktion": ""}),
    v('Ruhetag', 'an der Tür', 'a5h', 'aushang', 'dunkel', {"ueber": "Dienstag & Mittwoch", "titel": "Heute ist Ruhetag",
      "text": "Ab Donnerstag sind wir wieder für Sie da, 11:30 Uhr - 23:00 Uhr.", "aktion": TEL}),
    v('Geschlossene Gesellschaft', 'sofort aushängen', 'a4h', 'aushang', 'hell', {"ueber": "Heute", "titel": "Geschlossene Gesellschaft",
      "text": "Heute feiert bei uns eine geschlossene Gesellschaft. Die Lästermeile ist wie gewohnt für Sie da.", "aktion": ""}),
    v('Küche geschlossen', 'an der Bar', 'a6h', 'aushang', 'creme', {"ueber": "Nach 20:00 Uhr", "titel": "Die Küche ruht",
      "text": "Die grosse Karte gibt es wieder morgen ab 11:30 Uhr. Die Karte der Lästermeile gibt es weiter.", "aktion": ""}),
    v('Allergien', 'am Tisch', 'a6h', 'aushang', 'hell', {"ueber": "Bitte sagen Sie es uns", "titel": "Allergien",
      "text": "G Gluten · L Laktose · E Eier · F Fische · S Schalen- und Weichtiere · N Nüsse · Se Sellerie. Unser Service berät Sie gerne.", "aktion": ""}),
    v('Reserviert', 'auf dem Tisch', 'a7q', 'deckel', 'dunkel', {"ueber": "Wirtschaft am Schlössli", "titel": "Reserviert", "unter": "", "text": ""}),
]

NEWSLETTER = [
    v('Wir machen Ferien', 'an alle Gäste', 'mail', 'fenster', 'dunkel', {"bild": "morgen", "ueber": "Betriebsferien", "titel": "Wir machen Ferien", "unter": "22. Dezember - 10. Februar",
      "text": "Ab dem 11. Februar 2027 sind wir wieder für Sie da, direkt im Hafen von Bottighofen."}),
    v('Four-Hands an Bord', 'an alle Gäste', 'mail', 'fenster', 'dunkel', {"bild": "moni", "ueber": "13. bis 15. November 2026", "titel": "Four-Hands an Bord", "unter": "Excellence Gourmetkreuzfahrt",
      "text": "Monika Huber kocht mit ihrem Mentor Dieter Koschina auf der Excellence Countess, von Basel nach Strassburg und zurück."}),
    v('Lunch am See', 'an Stammgäste', 'mail', 'aushang', 'creme', {"ueber": "Am Mittag", "titel": "Lunch am See",
      "text": "Drei Gänge am Mittag: Kürbissuppe, Risi e bisi und Joghurt Panna Cotta.", "aktion": TEL}),
    v('Kopfbild Hafen', 'über jeder E-Mail', 'mailkopf', 'ansicht', 'dunkel', {"bild": "bootshafen", "titel": "Bottighofen", "unter": "Wirtschaft am Schlössli"}),
    v('Kopfbild Terrasse', 'über jeder E-Mail', 'mailkopf', 'ansicht', 'dunkel', {"bild": "start", "titel": "Bodensee", "unter": "Wirtschaft am Schlössli"}),
    v('Story: Die Terrasse', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "platanen", "ueber": "Die Seeterrasse", "titel": "Unter den Platanen", "unter": ZEIT,
      "text": "Direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen."}),
]

# ---------------- Anlässe & Events (haus.json › anlaesse, ferien) ----------------
ANLAESSE = [
    {"k": "kreuzfahrt-2026", "t": "Four-Hands an Bord", "z": "13.–15. November", "von": "2026-11-13", "bis": "2026-11-15", "wo": "stadt",
     "ort": "Excellence Countess · Basel – Strassburg", "satz": "Four-Hands-Dinner mit Dieter Koschina an Bord, Start am Freitag in Basel. Das Restaurant ist über diese drei Tage geschlossen.", "fotos": ["moni", "iberia", "thon"]},
    {"k": "lunch-herbst", "t": "Lunch-Menü am Mittag", "z": "bis 21. Dezember", "von": "2026-10-19", "bis": "2026-12-21", "wo": "haus",
     "ort": "Wirtschaft am Schlössli · am Mittag", "satz": "Drei Gänge am Mittag: Kürbissuppe, Risi e bisi, Joghurt Panna Cotta.", "fotos": ["suppe", "tortelloni", "dessert"]},
    {"k": "bankett-winter", "t": "Banketts & Firmenfeiern", "z": "bis 21. Dezember", "von": "2026-11-01", "bis": "2026-12-21", "wo": "haus",
     "ort": "Wirtschaft am Schlössli · zwei Etagen", "satz": "Familien- und Firmenfeiern auf zwei Etagen für jeweils bis zu 26 Personen, Tavolata oder gesetztes Menü.", "fotos": ["gaststube", "glas", "fleisch"]},
    {"k": "ferien-winter", "t": "Betriebsferien", "z": "22. Dezember – 10. Februar", "von": "2026-12-22", "bis": "2027-02-10", "wo": "haus",
     "ort": "Wirtschaft am Schlössli · geschlossen", "satz": "Vom 22. Dezember 2026 bis zum 10. Februar 2027 macht das Haus Ferien.", "fotos": ["morgen", "saentis", "haus"]},
    {"k": "zurueck-2027", "t": "Zurück am See", "z": "ab 11. Februar", "von": "2027-02-11", "bis": "2027-03-31", "wo": "haus",
     "ort": "Wirtschaft am Schlössli · Donnerstag bis Montag", "satz": "Nach den Ferien wieder offen, Donnerstag bis Montag 11:30 Uhr - 23:00 Uhr.", "fotos": ["start", "abendschiff", "platanen"]},
]
MOTIVE = {
    "kreuzfahrt-2026": [ANLAESSE_ABT[1], ANLAESSE_ABT[0], ANLAESSE_ABT[2], NEWSLETTER[1],
                        v('Story', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "iberia", "ueber": "13. bis 15. November", "titel": "Four-Hands an Bord", "unter": "Excellence Countess", "text": "Monika Huber und Dieter Koschina kochen zusammen."})],
    "lunch-herbst": [RESTAURANT[0], NEWSLETTER[2],
                     v('Story', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "suppe", "ueber": "Am Mittag", "titel": "Lunch am See", "unter": "Drei Gänge", "text": "Kürbissuppe, Risi e bisi, Joghurt Panna Cotta."}),
                     v('Aushang an der Tür', 'an der Tür', 'a4h', 'aushang', 'creme', {"ueber": "Am Mittag", "titel": "Lunch-Menü", "text": "Drei Gänge am Mittag: Kürbissuppe, Risi e bisi, Joghurt Panna Cotta.", "aktion": KUECHE})],
    "bankett-winter": [ANLAESSE_ABT[3], ANLAESSE_ABT[4], ANLAESSE_ABT[7],
                       v('Einladung', 'an die Gäste der Feier', 'q148', 'einladung', 'creme', {"ueber": "Wirtschaft am Schlössli", "titel": "Unser Fest am See", "wann": "Datum · Uhrzeit", "wo": ADR, "text": "Auf zwei Etagen, direkt im Hafen von Bottighofen.", "aktion": "Antwort an " + TEL})],
    "ferien-winter": [HINWEISE[0], NEWSLETTER[0],
                      v('Story', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "saentis", "ueber": "Betriebsferien", "titel": "Wir machen Ferien", "unter": "22. Dezember - 10. Februar", "text": "Ab dem 11. Februar 2027 sind wir wieder für Sie da."}),
                      v('Beitrag', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "morgen", "ueber": "22. Dezember - 10. Februar", "titel": "Wir machen Ferien", "text": "Danke für dieses Jahr am See. Ab dem 11. Februar 2027 sind wir wieder für Sie da.", "aktion": IG})],
    "zurueck-2027": [
        v('Aushang', 'an der Tür', 'a4h', 'aushang', 'dunkel', {"ueber": "Ab 11. Februar 2027", "titel": "Zurück am See", "text": "Donnerstag bis Montag 11:30 Uhr - 23:00 Uhr. " + KUECHE + ".", "aktion": TEL}),
        v('Beitrag', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "start", "ueber": "Ab 11. Februar 2027", "titel": "Zurück am See", "text": "Die Ferien sind vorbei, die Terrasse wartet.", "aktion": IG}),
        v('Story', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "abendschiff", "ueber": "Ab 11. Februar", "titel": "Zurück am See", "unter": "Donnerstag bis Montag", "text": "Wir freuen uns auf Sie."}),
        HAFEN[0]],
}

# ---------------- Beispielinhalte je Aufbau (DS.BEISPIEL) und je Art (INHALT) ----------------
BEISPIEL = {
    "deckel": {"ueber": "Wirtschaft am Schlössli", "titel": ZEILE, "unter": ADR, "text": ss(H['satz_lage'])},
    "buehne": {"bild": "start", "ueber": "Die Seeterrasse", "titel": "Die schönste Terrasse am Bodensee", "text": ss(H['satz_lage']), "aktion": ADR},
    "ansicht": {"bild": "bootshafen", "titel": "Bottighofen", "unter": "Wirtschaft am Schlössli · Am Hafen"},
    "karte": RESTAURANT[4]["inhalt"],
    "einladung": {"ueber": "Banketts & Gruppen", "titel": "Unser Fest am See", "wann": "Datum · Uhrzeit", "wo": ADR, "text": "Auf zwei Etagen für jeweils bis zu 26 Personen, Tavolata oder gesetztes Menü.", "aktion": TEL},
    "programm": ANLAESSE_ABT[2]["inhalt"],
    "fenster": {"bild": "platanen", "ueber": "Die Seeterrasse", "titel": "Unter den Platanen", "unter": "Bottighofen", "text": ss(H['satz_lage'])},
    "geteilt": {"bild": "regal", "ueber": "Die Bar am Hafen", "titel": "Die Lästermeile", "text": "Zementfliesen, eine Reihe Stühle und der Blick auf den Bootshafen.", "aktion": "Wirtschaft am Schlössli"},
    "gutschein": GESCHENK[0]["inhalt"],
    "gutscheinrueck": GESCHENK[0]["rueck"]["inhalt"],
    "aushang": HINWEISE[0]["inhalt"],
    "rueckseite": {"text": ZEIT},
    "kartengruss": {"titel": "Grüsse vom See", "text": "Direkt im Hafen von Bottighofen, mit Blick aufs Wasser und die Alpen."},
    "menue": {"titel": "Lunch-Menü", "ueber": "Drei Gänge am Mittag", "liste": LUNCH_G, "fuss": ADR},
}
INHALT = {
    "menuekarte": {"menue": BEISPIEL["menue"], "karte": RESTAURANT[1]["inhalt"]},
    "flyer": {"buehne": HAUS[0]["inhalt"], "fenster": BEISPIEL["fenster"]},
    "plakat": {"buehne": HAFEN[3]["inhalt"], "aushang": HINWEISE[0]["inhalt"], "deckel": {"ueber": "13. bis 15. November 2026", "titel": "Four-Hands an Bord", "unter": "Excellence Gourmetkreuzfahrt", "text": "Monika Huber und Dieter Koschina kochen auf der Excellence Countess."}},
    "speisekarte": {"karte": RESTAURANT[2]["inhalt"]},
    "weinempfehlung": {"karte": WEINE[0]["inhalt"], "fenster": WEINE[4]["inhalt"]},
    "einladung": {"einladung": ANLAESSE_ABT[1]["inhalt"]},
    "aushang": {"aushang": HAUS[1]["inhalt"]},
    "programm": {"programm": ANLAESSE_ABT[2]["inhalt"]},
    "tisch": {"buehne": LAESTERMEILE[2]["inhalt"], "aushang": RESTAURANT[6]["inhalt"]},
    "instagram": {"geteilt": LAESTERMEILE[3]["inhalt"], "buehne": HAUS[4]["inhalt"], "fenster": HAUS[3]["inhalt"]},
    "postkarte": {"ansicht": HAFEN[0]["inhalt"]},
    "tischkarte": {"deckel": HINWEISE[6]["inhalt"]},
    "hinweiskarte": {"aushang": HINWEISE[5]["inhalt"]},
    "stoerung": {"aushang": HINWEISE[3]["inhalt"]},
    "menueeinleger": {"karte": RESTAURANT[3]["inhalt"]},
    "teamaushang": {"aushang": {"ueber": "Für das Team", "titel": "Küchenzeiten", "text": "Bestellungen für die grosse Karte 11:30 Uhr - 13:30 Uhr und 18:00 Uhr - 20:00 Uhr. Die Lästermeile läuft durchgehend.", "aktion": ""}},
    "pressemappe": {"deckel": HAUS[5]["inhalt"]},
    "story": {"fenster": NEWSLETTER[5]["inhalt"]},
    "newsletter": {"fenster": NEWSLETTER[0]["inhalt"]},
    "gutschein": {"gutschein": GESCHENK[0]["inhalt"]},
}

# ---------------- Bibliothek je Art (vorlagen/<art>.json) ----------------
ART_FORMAT = {"menuekarte": "dlh", "flyer": "a6h", "plakat": "a3h", "speisekarte": "a5h", "weinempfehlung": "dlh", "einladung": "q148", "aushang": "a4h", "programm": "a5h",
              "tisch": "a6h", "instagram": "insta", "postkarte": "a6q", "tischkarte": "a7q", "hinweiskarte": "a6h", "stoerung": "a4h", "menueeinleger": "a5h",
              "teamaushang": "a4h", "pressemappe": "a4h", "story": "story", "newsletter": "mail", "gutschein": "dlq"}
GRUPPE_NAME = {"menuekarte": "Menükarte", "flyer": "Flyer und Programm", "programm": "Flyer und Programm", "plakat": "Plakat und Presse", "pressemappe": "Plakat und Presse",
               "speisekarte": "Karte und Einleger", "menueeinleger": "Karte und Einleger", "weinempfehlung": "Weinempfehlung", "einladung": "Einladung und Gutschein",
               "gutschein": "Einladung und Gutschein", "aushang": "Aushang und Hinweise", "stoerung": "Aushang und Hinweise", "teamaushang": "Aushang und Hinweise",
               "tisch": "Tischaufsteller", "instagram": "Instagram und Newsletter", "newsletter": "Instagram und Newsletter", "postkarte": "Postkarte", "tischkarte": "Tischkarte",
               "hinweiskarte": "Hinweiskarte", "story": "Story"}
BIB = {k: [] for k in ART_FORMAT}


def neu(art, titel, bereich, x, fmt=None, anlass=None):
    BIB[art].append({"id": "%s-%03d" % (art, len(BIB[art]) + 1), "titel": titel, "bereich": bereich, "vorlage": x["vorlage"], "ton": x["ton"], "stil": x["stil"],
                     "inhalt": x["inhalt"], "rueck": x["rueck"], **({"format": fmt} if fmt else {}), **({"anlass": anlass} if anlass else {})})


neu('menuekarte', 'Lunch-Menü', 'Restaurant', RESTAURANT[0])
neu('menuekarte', 'Lunch-Menü · Stuhlblau', 'Restaurant', v('Lunch-Menü', '', 'dlh', 'menue', 'dunkel', BEISPIEL['menue']))
for x in ANLAESSE_ABT[4:7]:
    neu('menuekarte', x["n"], 'Banketts', x, 'dlh', 'bankett-winter')
for x in RESTAURANT[1:5]:
    neu('speisekarte', x["n"], 'Restaurant', x)
for x in LAESTERMEILE[:2]:
    neu('speisekarte', x["n"], 'Lästermeile', x)
for x in WEINE[:4]:
    neu('weinempfehlung', x["n"], 'Wein', x)
neu('weinempfehlung', 'Der Weinkeller', 'Wein', WEINE[4], 'dlh')
for x in [HAUS[0], ANLAESSE_ABT[3], LAESTERMEILE[2]]:
    neu('flyer', x["n"], 'Haus', x, 'a6h')
neu('flyer', 'Flyer Lästermeile', 'Lästermeile', v('Flyer Lästermeile', '', 'a6h', 'fenster', 'creme', {"bild": "regal", "ueber": "Die Lästermeile", "titel": "Die Bar am Hafen", "unter": ZEIT, "text": "Tapas durchgehend, Stärkung und Süsses, mit Blick auf den See."}))
for x in [ANLAESSE_ABT[2], ANLAESSE_ABT[7]]:
    neu('programm', x["n"], 'Anlässe', x)
neu('programm', 'Das Haus in Zahlen', 'Haus', v('Das Haus', '', 'a5h', 'programm', 'hell', {"ueber": "Wirtschaft am Schlössli", "titel": "Das Haus",
    "termine": [{"wann": "Seit April 2025", "was": "Monika Huber führt ihre eigene Küche am See", "wo": ""}, {"wann": "Zwei Etagen", "was": "Banketts für jeweils bis zu 26 Personen", "wo": ""},
                {"wann": "Donnerstag bis Montag", "was": "11:30 Uhr - 23:00 Uhr, die Lästermeile durchgehend", "wo": ""}]}))
for x in [HAFEN[3], ANLAESSE_ABT[0], HINWEISE[0]]:
    neu('plakat', x["n"], 'Aushang', x, 'a3h')
neu('plakat', 'Four-Hands an Bord', 'Anlässe', v('Four-Hands an Bord', '', 'a3h', 'deckel', 'dunkel', INHALT['plakat']['deckel']), 'a3h', 'kreuzfahrt-2026')
neu('plakat', 'Banketts & Gruppen', 'Anlässe', ANLAESSE_ABT[3], 'a3h', 'bankett-winter')
neu('pressemappe', HAUS[5]["n"], 'Haus', HAUS[5])
neu('pressemappe', 'Pressemappe · Auszeichnungen', 'Haus', v('Pressemappe', '', 'a4h', 'deckel', 'creme', {"ueber": "GaultMillau · Guide 2027", "titel": "15 Punkte", "unter": "Entdeckung des Jahres 2026", "text": "Moni Huber, Küchenchefin der Wirtschaft am Schlössli."}))
neu('pressemappe', 'Pressemappe · Küche', 'Haus', v('Pressemappe', '', 'a4h', 'fenster', 'creme', {"bild": "moni", "ueber": "Pressemappe", "titel": "Monika Huber", "unter": "Küchenchefin", "text": ss(H['weg_moni'])}))
for x in [ANLAESSE_ABT[1]] + [MOTIVE['bankett-winter'][3]]:
    neu('einladung', x["n"], 'Anlässe', x)
neu('einladung', 'Einladung · hell', 'Anlässe', v('Einladung', '', 'q148', 'einladung', 'hell', BEISPIEL['einladung']))
for x in GESCHENK[:3]:
    neu('gutschein', x["n"], 'Gutschein', x)
for x in [HAUS[1], HAUS[6], LAESTERMEILE[4], MOTIVE['lunch-herbst'][3], MOTIVE['zurueck-2027'][0], HINWEISE[0]]:
    neu('aushang', x["n"], 'Hinweise', x)
for x in [HINWEISE[1], HINWEISE[2], HINWEISE[3], HINWEISE[4]]:
    neu('stoerung', x["n"], 'Hinweise', x)
neu('teamaushang', 'Küchenzeiten', 'Team', v('Küchenzeiten', '', 'a4h', 'aushang', 'hell', INHALT['teamaushang']['aushang']))
neu('teamaushang', 'Ablauf Bankett', 'Team', v('Ablauf Bankett', '', 'a4h', 'programm', 'hell', {"ueber": "Für das Team", "titel": "Ablauf Bankett",
    "termine": [{"wann": "Vorher", "was": "Personenzahl, Speisenform und Allergien prüfen", "wo": ""}, {"wann": "Empfang", "was": "Gäste in Empfang nehmen, Apéro", "wo": ""},
                {"wann": "Menü", "was": "Gänge nach Absprache mit der Küche", "wo": ""}, {"wann": "Danach", "was": "Tische abräumen, Etage für den nächsten Tag", "wo": ""}]}))
for x in [LAESTERMEILE[2], RESTAURANT[5], RESTAURANT[6], WEINE[5], GESCHENK[3]]:
    neu('tisch', x["n"], 'Am Tisch', x)
for x in [LAESTERMEILE[3], HAUS[3], HAUS[4], WEINE[4], HAFEN[4]] + [MOTIVE['ferien-winter'][3], MOTIVE['zurueck-2027'][1]]:
    neu('instagram', x["n"], 'Instagram', x, 'insta')
for x in HAFEN[:3]:
    neu('postkarte', x["n"], 'Hafen', x)
neu('postkarte', 'Postkarte Schifflände', 'Hafen', v('Postkarte Schifflände', '', 'a6q', 'ansicht', 'dunkel', {"bild": "schifflaende", "titel": "Bottighofen", "unter": "Die Schifflände"},
    {"vorlage": "kartengruss", "inhalt": BEISPIEL['kartengruss']}))
for t, u, ton in [('Reserviert', 'Wirtschaft am Schlössli', 'dunkel'), ('Reserviert', 'Die Seeterrasse', 'creme'), ('Reserviert', 'Die Lästermeile', 'hell'), ('Willkommen', 'Banketts & Gruppen', 'dunkel')]:
    neu('tischkarte', t + ' · ' + u, 'Am Tisch', v(t, '', 'a7q', 'deckel', ton, {"ueber": u, "titel": t, "unter": "", "text": ""}))
for x in [HINWEISE[5], HINWEISE[4], RESTAURANT[6], HAUS[7]]:
    neu('hinweiskarte', x["n"], 'Am Tisch', x, 'a6h')
for x in [RESTAURANT[1], RESTAURANT[2], RESTAURANT[3], RESTAURANT[4]]:
    neu('menueeinleger', x["n"], 'Restaurant', x)
for x in [NEWSLETTER[5], HAFEN[5]] + [m for k in MOTIVE for m in MOTIVE[k] if m["n"] == 'Story']:
    neu('story', x["n"], 'Story', x, 'story')
for x in NEWSLETTER:
    neu('newsletter', x["n"], 'Newsletter', x, x["format"])


def wissen():
    """Wortlaut für die Probe-Antworten und das Wissen der KI: Seiten der Website ohne Markup, dazu die Inhaltsdaten (ohne Preise)."""
    t = []
    for f in sorted(glob.glob(os.path.join(WEB, '*.html'))):
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'(?s)<(script|style|svg)[^>]*>.*?</\1>', ' ', s)
        s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
        s = re.sub(r'\s+', ' ', s).strip()
        t.append('## ' + os.path.basename(f) + '\n' + s[:6000])
    t.append('## Karte\n' + '\n'.join('%s: %s' % (l['land'], '; '.join('%s (%s)' % (g['name'], glied(g['text'])) for g in l['gerichte'])) for l in KARTE['laender']))
    t.append('## Lunch\n' + '; '.join('%s (%s)' % (g['name'], g['text']) for g in LUNCH['gaenge']))
    t.append('## Lästermeile\n' + '; '.join(e['name'] for g in LAESTER['gruppen'] for e in g['eintraege']))
    return ss('\n\n'.join(t))


def schreiben():
    vd = os.path.join(Z, 'vorlagen'); os.makedirs(vd, exist_ok=True)
    for f in os.listdir(vd):
        if f.endswith('.json'):
            os.remove(os.path.join(vd, f))
    index = []
    for art, l in BIB.items():
        if not l:
            continue
        json.dump({"art": art, "format": ART_FORMAT[art], "vorlagen": l}, open(os.path.join(vd, art + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        index.append({"art": art, "format": ART_FORMAT[art], "zahl": len(l), "gruppe": GRUPPE_NAME[art]})
    json.dump(index, open(os.path.join(vd, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
    kat = ("/* Die Hausdruckerei · Wirtschaft am Schlössli Bottighofen · Katalog des Hauses. GESCHRIEBEN VON bau_vorlagen.py, nicht von Hand ändern.\n"
           "   Fertig gesetzte Vorlagen nur aus dem, was das Haus selbst sagt (website/inhalt/*.json); jede öffnet ohne KI und ohne Kosten. Keine Preise. */\n(function () {\n"
           f"  const ABTEILUNGEN = {J(ABTEILUNGEN)};\n  const HINWEISE = {J(HINWEISE)};\n  const NEWSLETTER = {J(NEWSLETTER)};\n  const ANLAESSE = {J(ANLAESSE)};\n"
           f"  const MOTIVE = {J(MOTIVE)};\n  const motive = a => MOTIVE[a.k] || [];\n  window.DSKATALOG = {{ ABTEILUNGEN, HINWEISE, ANLAESSE, motive, NEWSLETTER }};\n}})();\n")
    open(os.path.join(HIER, 'katalog.js'), 'w', encoding='utf-8').write(kat)
    s = open(os.path.join(HIER, 'start.js'), encoding='utf-8').read()
    s = re.sub(r'  const INHALT = \{.*?\};\n', lambda m: '  const INHALT = ' + json.dumps(INHALT, ensure_ascii=False) + ';\n', s, count=1, flags=re.S)
    open(os.path.join(HIER, 'start.js'), 'w', encoding='utf-8').write(s)
    s = open(os.path.join(HIER, 'vorlagen.js'), encoding='utf-8').read()
    s = re.sub(r'  /\* Beispielinhalte im Wortlaut [^\n]*\n', '  /* Beispielinhalte im Wortlaut des Hauses (geschrieben und geprüft von bau_vorlagen.py) */\n', s, count=1)
    s = re.sub(r'  DS\.BEISPIEL = \{.*?\};\n', lambda m: '  DS.BEISPIEL = ' + json.dumps(BEISPIEL, ensure_ascii=False) + ';\n', s, count=1, flags=re.S)
    open(os.path.join(HIER, 'vorlagen.js'), 'w', encoding='utf-8').write(s)
    os.makedirs(os.path.join(HIER, 'api', '_daten'), exist_ok=True)
    open(os.path.join(HIER, 'api', '_daten', 'schloessli-wissen.txt'), 'w', encoding='utf-8').write(wissen())
    n = sum(len(l) for l in BIB.values())
    print('Vorlagen:', n, 'in', len(index), 'Arten', {k: len(l) for k, l in BIB.items()}, '·', sum(len(a["vorlagen"]) for a in ABTEILUNGEN), 'in Abteilungen ·', len(ANLAESSE), 'Anlässe')


def pruefen():
    """Jede Zahl der Texte muss in den Quellen stehen; kein ß; keine Preise (CHF, Fr., .-)."""
    q = json.dumps([H, KARTE, LUNCH, LAESTER, WEIN, BANKETT], ensure_ascii=False)
    for f in glob.glob(os.path.join(WEB, '*.html')):
        q += open(f, encoding='utf-8').read()
    texte = json.dumps([ABTEILUNGEN, HINWEISE, NEWSLETTER, ANLAESSE, MOTIVE, BEISPIEL, INHALT], ensure_ascii=False)
    erlaubt = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27',
               '28', '29', '30', '31', '00', '03', '2025', '2026', '2027', '50', '41', '71', '688', '90', '92', '8598', '001', '002', '003', '004', '005', '006', '007', '008'}
    fehl = sorted({z for z in re.findall(r'\d+', texte) if z not in erlaubt and z not in q})
    if fehl:
        print('NICHT BELEGT:', fehl)
    if 'ß' in texte:
        print('ß IM TEXT')
    if re.search(r'CHF|Chf|SFr|\d\.-', texte):
        print('PREIS IM TEXT')


if __name__ == '__main__':
    pruefen()
    schreiben()
