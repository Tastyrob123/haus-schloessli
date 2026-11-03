"""Unterlagen des Landgasthofs Ruedihus, neu gesetzt im Stil der Website: die drei Karten ab 1.3.2026.

Fassung 2 (09.10.2026): von Hand gegliedert. Die erste Fassung las die Originale selbsttätig aus (satz_auto.py) und ordnete dabei
Preise falsch zu, verschluckte Überschriften und zerriss Absätze (Sicherung: _sicherung/unterlagen-fassung-1/). Jetzt steht jedes
Gericht mit seinem Preis und seinen Zeilen ausdrücklich hier. Der Wortlaut ist der des Hauses samt seinen Eigenheiten
(TAGESSSUPPE, KAFFFEE, KOFI ANAN, Carmel cream, Rundschreibenfenstern …); geprüft wird er mit satz_pruefe.py (Wörter) und
_qa/unterlagen_pruefe.py (Zeile für Zeile, Preis je Gericht).

Bewusst anders als das Original:
  · «HEUTE NACHT HIER SCHLAFEN? warum eigentlich nicht Bis zu 75 % Rabatt.» steht im Tagesteller-PDF in weisser Schrift unsichtbar
    hinter einem Foto und gehört nicht zur Karte → weggelassen.
  · «Drehort von Bauer ledig sucht» ist die Unterschrift eines Fotos, das hier fehlt → weggelassen.
  · Die Bildmarken «BIO» (Blauseeforelle) und «Swiss PrimGourmet» (Kilterschnitte) sind im Original kleine Logos → hier als Schriftmarke.
  · Tagesteller, letzter Kasten: im Original steht vor «steht für Speisen …» eine leere Stelle (das Zeichen fehlt) → hier die BIO-Marke
    der Schpis Charte, damit der Satz nicht klein und ohne Bezug beginnt. Beim Haus bestätigen lassen.
  · Schpiszettel, Desserts: Spaltenköpfe «Kleine Portion / Portion» aus der Schpis Charte (dieselben Desserts mit denselben Preisen).
Zeilen: ('d', Text) Beschreibung · ('f', Text) Übersetzung · ('h', Text) halbfett · ('k', Text, Preis) kleine Portion ·
        [[…]] im Text = Vorspann der Übersetzung · eine Liste aus (Art, Text) setzt mehrere Arten in eine Zeile."""
import html
import satz_kern as S
from kern import H

A3 = (420, 297)

# Seit 09.10.2026 (Master «Website-Bau», Abschnitt 8): eindeutige Tippfehler und Widersprüche des Originals werden in der Idee
# berichtigt. Jede Berichtigung steht hier und nirgends sonst; die Texte weiter unten sind der Wortlaut des Hauses.
# Nicht angefasst: Mundart, Preise, Namen, die sich nicht belegen lassen. (so im Original, so in der Idee, Grund)
BERICHTIGT = [
    # Egger- und Stettlerstube
    ('TAGESSSUPPE', 'TAGESSUPPE', 'Tippfehler (die beiden anderen Karten schreiben TAGESSUPPE)'),
    ('KAFFFEE FERTIG', 'KAFFEE FERTIG', 'Tippfehler'),
    ('mit Zi ebele', 'mit Ziebele', 'Leerzeichen im Wort (weiter unten «Ziebele»)'),
    ('Grosi´s', 'Grosi’s', 'Akzent statt Apostroph'),
    ('Chalsbläberli', 'Chalbsläberli', 'Buchstabendreher (Titel: CHALBSLÄBERLI)'),
    ('Emincé de der foie', 'Emincé de foie', 'Wort zu viel'),
    ('POTATOE TERRINE', 'POTATO TERRINE', 'Tippfehler'),
    ('noix et ognions', 'noix et oignons', 'Tippfehler'),
    ('à lèau', 'à l’eau', 'Tippfehler'),
    ('FISHERMANS PLATE', 'FISHERMAN’S PLATE', 'Apostroph'),
    ('ENTRECOTE DE GRATINE,', 'ENTRECÔTE GRATINÉE,', 'wie auf dem Tagesmenu und dem Tagesteller des Hauses'),
    ('SOUPE /SALADES', 'SOUPE / SALADES', 'Leerzeichen'),
    ('SOUP /SALAD', 'SOUP / SALAD', 'Leerzeichen'),
    ('oder / ou /or', 'oder / ou / or', 'Leerzeichen'),
    ('Kiltterschnitte', 'Kilterschnitte', 'Tippfehler (Karte: KILTERSCHNITTE)'),
    ('Wednsday', 'Wednesday', 'Tippfehler'),
    ('Donnerstag', 'Donnschti', 'Kopf des Tages: Mundart gross, Übersetzungen klein wie bei den anderen Tagen', 'genau'),
    ('Donnschti Jeudi, Thursday', 'Donnerstag Jeudi Thursday', 'siehe Zeile darüber', 'genau'),
    ('Forällefillet', 'Forällefilet', 'Tippfehler (am Freitag: Forällefilet)'),
    ('Pasta and végetable', 'Pasta and vegetable', 'Akzent im englischen Wort'),
    ('sauted potatoes', 'sautéed potatoes', 'Tippfehler'),
    ('liqueuer', 'liqueur', 'Tippfehler'),
    ('mit Gravesteiner', 'mit Gravensteiner', 'Apfelsorte, in der Zeile darunter richtig'),
    ('gravensteiner/', 'gravensteiner /', 'Leerzeichen'),
    ('liqueur d’Appenzelle', 'liqueur d’Appenzell', 'wie auf dem Schpiszettel'),
    # Chäs- und Wystube
    ('gekleistert oder bemalen', 'gekleistert oder bemalt', 'Tippfehler'),
    ('Die Sonst so', 'Die sonst so', 'Kleinschreibung'),
    ('Rundschreibenfenstern viel jedem', 'Rundscheibenfenstern fiel jedem', 'zwei Tippfehler'),
    ('nicht. leuchtende', 'nicht. Leuchtende', 'Satzanfang'),
    ('das Gesimmse', 'das Gesimse', 'Tippfehler'),
    ('bemalt, Darum', 'bemalt, darum', 'Kleinschreibung'),
    ('En Glück', 'Ein Glück', 'Tippfehler'),
    ('wenigsten die Fassade Grösstenteils', 'wenigstens die Fassade grösstenteils', 'Tippfehler, Kleinschreibung'),
    ('vom Ruedihaus', 'vom Ruedihus', 'Name des Hauses'),
    ('ein und ausgegangen', 'ein- und ausgegangen', 'Bindestrich'),
    ('KOFI ANAN', 'KOFI\u00a0ANNAN', 'Name des UNO-Generalsekretärs'),
    ('in unsere Liebeslaube', 'in unserer Liebeslaube', 'Tippfehler'),
    ('(7 gängiges', '(7-gängiges', 'Bindestrich'),
    ('Mail : info', 'Mail: info', 'Leerzeichen'),
    ('www. doldenhorn', 'www.doldenhorn', 'Leerzeichen in der Adresse'),
    ('Entrée –petite', 'Entrée – petite', 'Leerzeichen'),
    ('Plat principales', 'Plats principaux', 'wie in der Schpis Charte des Hauses'),
    ('Fondue aux aux truffes', 'Fondue aux truffes', 'Wort doppelt'),
    ('Reickingen', 'Reckingen', 'Ortsname (Metzgerei Eggs, Furkastrasse 6, 3998 Reckingen; geprüft 09.10.2026)'),
    ('Carmel cream', 'Caramel cream', 'Tippfehler'),
    # Tagesteller
    ('oignons, Röst', 'oignons, Rösti', 'Wort abgeschnitten'),
    ('Fresh trout from roasted', 'Fresh roasted trout', 'Wörter verstellt (Schpis Charte: «Fresh roasted trout served with potatoes and spinach»)'),
    ('Chalbsläberli Im Anke', 'Chalbsläberli im Anke', 'Kleinschreibung'),
    ('PORC ESCALOPE', 'PORK ESCALOPE', 'englische Zeile, französisches Wort'),
    ('Lamm). Die auf', 'Lamm), die auf', 'Nebensatz stand als eigener Satz'),
    ('servieren wir ihnen', 'servieren wir Ihnen', 'Anrede gross'),
    ('Salzwasserfische, und Cola', 'Salzwasserfische und Cola', 'Komma'),
    # QA-Durchgang 09.10.2026 abends (Egger- und Stettlerstube)
    ('aus Môtiers den Sonnenhängen', 'aus Môtiers, den Sonnenhängen', 'Komma vor der Beifügung'),
    ('Mashed Potatoes and vegetables', 'mashed potatoes and vegetables', 'Grossschreibung mitten in der Zeile'),
    ('Plat De Poisson', 'PLAT DE POISSON', 'Vorspann in Versalien wie bei allen anderen Gerichten (Tagesteller: PLAT DE POISSON)'),
    ('Plat de fromages', 'PLAT DE FROMAGES', 'Vorspann in Versalien wie bei allen anderen Gerichten'),
    ('served with potatoes and spinach.', 'served with potatoes and spinach', 'Schlusspunkt, den keine andere Zeile der Karte hat'),
    ('Salade aux betterave rouge', 'Salade aux betteraves rouges', 'Mehrzahl (Schpis Charte: betteraves rouges)'),
    ('Herb Soup', 'Herb soup', 'Kleinschreibung wie Celery soup, Carrot soup'),
    ('avec Nouilles', 'avec nouilles', 'Kleinschreibung'),
    ('SIE DÜRFEN GERNE EINEN 2. LÖFFEL BESTELLEN', 'Sie dürfen gerne einen 2. Löffel bestellen', 'deutsche Beschreibung, im Original in Versalien wie die englische Zeile (Schpiszettel: normale Schreibung)'),
    ('“das Ruedihus Special”', '„das Ruedihus Special“', 'deutsche Anführungszeichen wie im übrigen deutschen Text'),
    ('APPLESORBET', 'APPLE SORBET', 'Leerzeichen'),
    # Chäs- und Wystube
    ('Das “Traditionelle“', 'Das „Traditionelle“', 'Anführungszeichen (öffnend und schliessend verschieden)'),
    ('Der “Dünne“', 'Der „Dünne“', 'Anführungszeichen (öffnend und schliessend verschieden)'),
    ('FARMERS', 'FARMER’S', 'Apostroph (Schpiszettel: Cold farmer’s ham)'),
    ('HUNTERS', 'HUNTER’S', 'Apostroph'),
    ('ice-cream : plum', 'ice-cream: plum', 'im Englischen kein Leerzeichen vor dem Doppelpunkt'),
    ('Kinderteller, pour vos enfants, for your children', 'Kinderteller · pour vos enfants · for your children', 'Trennung wie bei allen anderen Rubriken'),
    # alle drei Karten
    ('auf Anfrage gerne', 'auf Anfrage gerne.', 'Schlusspunkt (Tagesteller hat ihn, die beiden anderen Karten nicht)'),
]
GENUTZT = []          # (alt, neu) jeder Ersetzung, für die Wortlaut-Prüfung (dazu/fehlt)
_ort = ['']


def r(text):
    """Wortlaut des Hauses → berichtigter Wortlaut. Merkt sich jede Ersetzung."""
    for b_ in BERICHTIGT:
        alt, neu = b_[0], b_[1]
        if len(b_) > 3:
            if text == alt:
                GENUTZT.append((_ort[0], alt, neu, b_[2])); return neu
            continue
        n = text.count(alt)
        if n:
            text = text.replace(alt, neu); GENUTZT.extend([(_ort[0], alt, neu, b_[2])] * n)
    return text


def e(text, quote=True):
    return html.escape(r(text), quote=quote)


STERN = '<p class="stern">* * *</p>'
KP = 'kleine Portion · Petite portion · small portion'


# ---------------------------------------------------------------- Bausteine
def fmt(t):
    t = e(t, quote=False).replace('\n', '<br>').replace('« ', '«\u00a0').replace(' »', '\u00a0»')
    return t.replace('[[', '<span class="ld">').replace(']]', '</span>')


def preise(p, n=1):
    p = [p] if isinstance(p, str) else list(p or [])
    if not p:
        return ''
    p = [''] * (n - len(p)) + p
    return '<span class="prs">' + ''.join(f'<b>{e(x) or "&nbsp;"}</b>' for x in p) + '</span>'


def zeile(z, n=1):
    art, t = z[0], z[1]
    pr = preise(z[2], n) if len(z) > 2 else ''
    if isinstance(t, (list, tuple)):
        inn = ' '.join(f'<span class="{a}">{fmt(x)}</span>' for a, x in t)
        art = 'mix'
    else:
        inn = fmt(t)
    return f'<div class="gz"><p class="{art}">{inn}</p>{pr}</div>'


def G(name, pr=(), zusatz='', zeilen=(), n=1, marke='', kl=''):
    """Ein Gericht: Name (+ Zusatz, + Marke), Preis(e) rechts in festen Spalten, darunter seine Zeilen."""
    z = f' <small>{fmt(zusatz)}</small>' if zusatz else ''
    m = f' <span class="marke">{e(marke)}</span>' if marke else ''
    return (f'<div class="g {kl}"><div class="gz gz--n"><h4>{fmt(name)}{z}{m}</h4>{preise(pr, n)}</div>'
            + ''.join(zeile(x, n) for x in zeilen) + '</div>')


def R(titel, *fremd, preis='', kopf=()):
    """Rubrik: Titel, Übersetzungen klein daneben, optional Preis oder Spaltenköpfe rechts."""
    f = f'<small>{" · ".join(e(x) for x in fremd)}</small>' if fremd else ''
    r = f'<span class="rp">{e(preis)}</span>' if preis else ''
    if kopf:
        r = '<span class="kopfz">' + ''.join(f'<b>{e(k)}</b>' for k in kopf) + '</span>'
    return f'<h2 class="rubrik"><span>{e(titel)}{f}</span>{r}</h2>'


def tag(name, unter, *gaenge):
    """Ein Tag des Tagesmenus: Gänge als (Gericht, Französisch, Englisch)."""
    o = f'<h4 class="tag">{e(name)}</h4><p class="tagu">{e(unter)}</p>'
    for i, (g, fr, en) in enumerate(gaenge):
        o += (STERN if i else '') + f'<p class="gang">{fmt(g)}</p><p class="fr">{fmt(fr)}</p><p class="fr">{fmt(en)}</p>'
    return f'<div class="tmsp">{o}</div>'


def teller(titel, preis, zeilen, zusatz=''):
    """Ein Tagesteller: Titel in der Titelschrift mit Preis, darunter die Gänge."""
    z = f' <small>{e(zusatz)}</small>' if zusatz else ''
    o = ''
    for x in zeilen:
        o += STERN if x == '*' else zeile(x)
    return f'<div class="tt"><div class="tt__k"><h3>{e(titel)}{z}</h3><b>{e(preis)}</b></div>{o}</div>'


def mx(blatt, wert):
    """Grösstes Schriftmass einer Seite festlegen (satz_druck.js liest data-max; ohne Angabe 1.18)."""
    return blatt.replace('<section class="blatt', f'<section data-max="{wert}" class="blatt', 1)


def ab(text, kl=''):
    return f'<p class="ab {kl}">{fmt(text)}</p>'


def deckel(titel, zitat, von, adresse):
    return (f'<div class="deckel">{S.zeichen_gross("mitte")}<h1>{fmt(titel)}</h1><i></i>'
            f'<p class="deckel__z">{fmt(zitat)}</p><p class="deckel__q">{e(von)}</p><p class="deckel__a">{fmt(adresse)}</p></div>')


def ODER():
    return f'<p class="oder">{e("oder / ou /or")}</p>'


SUPPE = ('h', 'TAGESSUPPE oder Salat us der Schüssle')
SUPPE_F = ('f', 'Soupe du jour ou Salade / Soup of the day or Salad')
CHAES = ('Chäs mit und ohni Löcher', 'Fromage de la région', 'Cheese')
ALLERGIE = 'Über Zutaten in unseren Gerichten, die Allergien oder Intoleranzen auslösen können, informieren Sie unsere Mitarbeitenden auf Anfrage gerne'

# ================================================================ Egger- und Stettlerstube (6 Seiten A4)
_ort[0] = 'egger-und-stettlerstube'
k2_1 = S.blatt(S.titelblatt('SCHPIS CHARTE'), kl='deck', fuss=False).replace('<section class="blatt', '<section data-fest="1" class="blatt', 1)   # Deckblatt hat feste Grössen

k2_2 = S.blatt(
    R('UNSERE APERITIF-EMPFEHLUNG')   # Original «UNSERE APERITIF – EMPFEHLUNG»: Bindestrich statt Gedankenstrich (steht nicht in BERICHTIGT, weil die Prüfung die Zeile im Original in zwei Stücken liest)
    + G('MAULER TRADITION', '10.00', 'CÜPLI', [
        ('d', 'aus Môtiers den Sonnenhängen des Neuenburger Juras'),
        ('d', 'Ein Schaumwein, bestechend durch seine goldgelbe Farbe und die ansprechende Frische. In der Nase Noten aus Nüssen und Pfirsichen.')])
    + R('MENU')
    + G('MENU KOMPLETT', '80.00', zeilen=[('f', '[[LE MENU COMPLET]]'), ('f', 'Menu complet')])
    + R('VORSCHPIESE', 'NOS ENTRÉES', 'STARTERS')
    + G('GRÖICHTS BLAUSEEFORÄLLEFILET', '22.00', marke='BIO', zeilen=[
        ('d', 'Sanft gröichts Blauseeforällefilet mit Schnittlauchmeerrettichnydle (Geräuchertes Forellenfilet)'),
        ('f', '[[FILET DE TRUITE FUMÉ DU LAC BLEU]] garni d’une mousse de ciboulettes et de raifort'),
        ('f', '[[SMOKED BLUE LAKE TROUT]]')])
    + ODER()
    + G('HÄRDÖPFELTERRINE', '19.50', zeilen=[
        ('d', 'Gkochetä Härdöpfel mit Hamme, Nydle und Brät mit Chümischum (Warme Kartoffelterrine)'),
        ('f', '[[TERRINE DE POMMES DE TERRE]] une délicatesse de pommes de terre cuites, mélangées avec du jambon, de la crème et de la farce fine, garnie de mousse au cumin'),
        ('f', '[[POTATOE TERRINE]]')])
    + R('SUPPE / SALAT', 'SOUPE /SALADES', 'SOUP /SALAD')
    + G('TAGESSSUPPE', '10.50', zeilen=[('f', 'Soupe du jour / soup of the day')])
    + ODER()
    + G('GRÜENE SALAT', '10.50', zeilen=[
        ('d', 'Es Schüsseli Salat mit Brotwürfeli (Grüner Salat)'),
        ('f', '[[LAITUE]] un saladier de laitue avec croûtons'),
        ('f', '[[MIXED GREEN SALAD]]')])
    + ODER()
    + G('RANDESALAT', '11.50', zeilen=[
        ('d', 'Es Schüsseli mit Boumnüss und Ziebele (Rote Beete Salat)'),
        ('f', '[[SALADE DE BETTERAVES ROUGES]] un saladier de betteraves rouges garnies de noix et ognions'),
        ('f', '[[BEETROOT SALAD]]')]),
    kl='karte egger', kopf=S.leiste(), fuss=False)

k2_3 = S.blatt(
    R('HOUPTGÄNG', 'PLATS PRINCIPAUX', 'MAIN COURSES')
    + G('SUURE MOCKE', '38.00', zeilen=[
        ('d', 'Grosi´s Sure Mocke (Sauerbraten) mit Zi ebele, Späckwürfeli und Brotwürfeli Härdöpfelstock u Gmües'),
        ('f', '[[BŒUF BRAISÉ]] purée de pommes de terre, légumes'),
        ('f', '[[BRAISED BEEF, MASHED POTATOES AND VEGETABLES]]')])
    + ODER()
    + G('KILTERSCHNITTE', '46.00', marke='Swiss PrimGourmet', zeilen=[
        ('d', 'Zarts Rindsentrecote mit Chrütersauce überbache (Rindssteak mit Kräuterbutter) Härdöpfelstock u Gmües'),
        ('f', '[[ENTRECOTE DE GRATINE,]] beurre aux herbes, purée de pommes de terre, légumes'),
        ('f', '[[SIRLOIN STEAK GRATINATED WITH HERB BUTTER]] Mashed Potatoes and vegetables')])
    + ODER()
    + G('ZÜRI-GESCHNÄTZLÄTS', '44.00', zeilen=[
        ('d', 'Chalbfleischstreife anere feine Nydlesosse mit Champignons Rösti u Gmües (Zürich Geschnetzeltes)'),
        ('f', '[[ÉMINCÉ ZURICHOIS]] Emincé de veau, sauce à la crème et aux champignons, « rösti », légumes'),
        ('f', '[[SLICED VEAL ZÜRICH STYLE]]')])
    + ODER()
    + G('CHALBSLÄBERLI', '46.00', zeilen=[
        ('d', 'Chalsbläberli in viu bruunem Anke brate mit Röschti u Gmües'),
        ('f', '[[FOIE DE VEAU]] Emincé de der foie de veau sauté au beurre noisette, « rösti », légumes'),
        ('f', '[[VEAL LIVER SAUTÉED IN BROWN BUTTER, SERVED WITH RÖSTI AND VEGETABLES]]')])
    + R('CHÄS', 'FROMAGE', 'CHEESE')
    + G('MIT UND OHNI LÖCHER UF EM PLÄTTLI ZUM SELBER NÄH', '12.00', zeilen=[
        ('f', '[[Plat de fromages]] de la région à choix'),
        ('f', '[[CHEESE OF THE REGION]]')])
    + R('DESSERTS', 'DESSERTS', 'DESSERTS')
    + G('DESSERT ZUM USELÄSE', zeilen=[('f', 'Dessert au choix'), ('f', '[[DESSERT TO CHOOSE]]')])
    + S.kasten('', R('SPEZIELLES', 'NOS SPÉCIALITÉS', 'SPECIALS')
               + G('FISCHTÄLLER', '48.00', zeilen=[
                   ('d', 'E ganzi Forälle brate, Salzhärdöpfel und Spinat'),
                   ('f', '[[Plat De Poisson]] Truites fraîches rôti, garnie de pommes de terre à lèau et épinards'),
                   ('f', '[[FISHERMANS PLATE]] Fresh roasted trout served with potatoes and spinach.')]), kl='speziell'),
    kl='karte egger', kopf=S.leiste(), fuss=False)

_wo = [
    tag('Mäntig', 'Montag Lundi Monday',
        ('E Schnifu Burehame', 'Jambon de campagne garni', 'Cold farmer ham'),
        ('Louchsuppe', 'Potage aux poireaux', 'Leek cream soup'),
        ('Pouletbrüstli mit Pilze\nSpätzli Gmües', 'Poitrine de poulet Sauce aux champignons « Spätzli », légumes', 'Chicken breast with Spätzli and vegetable'),
        CHAES,
        ('Zuger Kirschtorte', 'Tourte zougoise au kirsch', 'Cake with cherry liqueur')),
    tag('Zyschtig', 'Dienstag Mardi Tuesday',
        ('Randensalat', 'Salade aux betterave rouge', 'Beetroot salad'),
        ('Chrütersuppe', 'Soupe aux herbes', 'Herb Soup'),
        ('Kiltterschnitte\nHörnli\nGemüse', 'ENTRECÔTE GRATINÉE, Beurre aux fines herbes, cornettes, légumes', 'SIRLOIN STEAK GRATINATED WITH HERB BUTTER\nPasta and végetable'),
        CHAES,
        ('Coupe Ruedi', 'Coupe Ruedi', 'Coupe Ruedi')),
    tag('Mittwoch', 'Mittwoch Mercredi Wednsday',
        ('Wybersalat', 'Salade aux lardons et fromage', 'Mixed green salad'),
        ('Selleriesuppe', 'Soupe au céleri', 'Celery soup'),
        ('Sure Mocke\nHärdöpfelstock G’müs\nGemüse', 'BŒUF BRAISÉ purée de pommes de terre, légumes', 'BRAISED BEEF, MASHED POTATOES AND VEGETABLE'),
        CHAES,
        ('Zwetschgenlisi', 'Sorbet aux pruneaux', 'Plum sorbet')),
    tag('Donnerstag', 'Donnschti Jeudi, Thursday',
        ('Mostbröckliteller', 'Viande séchée de bœuf', 'Dried beef'),
        ('Blattsalat', 'Laitue', 'Green salad'),
        ('Rahmschnitzel mit Nüdeli', 'Escalopes à la crème avec Nouilles', 'Escalope with cream sauce and noodles'),
        ('Chäs mit und ohni Löcher', 'Fromage de la région', 'Cheese of the region'),
        ('Apfelsorbet', 'Sorbet à la pomme', 'Apple sorbet')),
    tag('Frytig', 'Freitag Vendredi Friday',
        ('Fritierti Champignons mit Knoblouchmayonnaise', 'Champignons frits, mayonnaise à l’ail', 'Deep fried mushrooms, garlic mayonnaise'),
        ('Gmüessuppe', 'Crème de légumes', 'Vegetable cream soup'),
        ('Forällefilet gebraten\nSalzhärdöpfeli\nBlattspinät', 'Filet de truite du Lac bleu, Pommes natures, épinards', 'Broiled filet of trout with boiled potatoes and spinach'),
        CHAES,
        ('Nussglace mit Appezäller Rahmliqueur', 'Glace noisette, liqueuer appenzellois', 'Hazelnut ice cream with liqueur')),
    tag('Samschtig', 'Samstag Samedi Saturday',
        ('Forällefillet', 'Filet de truite', 'Trout fillet'),
        ('Rüeblisuppe', 'Potage carottes', 'Carrot soup'),
        ('Züri-Gschnätzletes\nKrokettli Gmües', 'Émincé de filet de porc zurichoise\nCroquettes, Légumes', 'Pork filet sliced zurich-style\nPotatoes croquettes and vegetable'),
        CHAES,
        ('Brönnti Crème', 'Crème caramel', 'Caramel cream')),
    tag('Sunntig', 'Sonntag Dimanche Sunday',
        ('Milkenpastetli', 'Vol-au-vent au ris de veau', 'Vol au vent of sweet-bread'),
        ('Spiezer Rieslingsuppe', 'Soupe au vin riesling de Spiez', 'Riesling cream soup'),
        ('Gmischte Brate\nBrathärdöpfle, Gmües', 'Les rôtis du dimanche\nPommes sautées, légumes', 'roast meat with sauted potatoes and vegetable'),
        CHAES,
        ('Meringue Glacé', 'Meringue glacée', 'Meringue with cream')),
]
k2_4 = S.blatt(
    R('TAGESMENU', 'MENU DU JOUR', preis='80.00')
    + f'<div class="tmreihe">{"".join(_wo[:4])}</div><div class="tmreihe">{"".join(_wo[4:])}</div>',
    kl='karte egger tagesmenu', kopf=S.leiste(), fuss=False)

k2_5 = S.blatt(
    R('VEGETARISCHES MENU', 'MENU VÉGÉTARIEN', preis='80.00')
    + G('FRITIERTI CHAMPIGNONS MIT KNOBLOUCHMAYONNAISE', zeilen=[('f', 'Champignons frits, mayonnaise à l’ail'), ('f', '[[DEEP FRIED MUSHROOMS]]')])
    + STERN
    + G('GRÜNE SALAT US DER SCHÜSSLE', zeilen=[('f', 'Saladier de laitue'), ('f', '[[MIXED GREEN SALAD]]')])
    + STERN
    + G('POCHIERTI EIER MIT BLATTSPINET', zusatz='u uf ere Chäsröschti', zeilen=[
        ('f', 'Oeufs pochés, épinards en branches sur un lit de « rösti » au fromage'), ('f', '[[POACHED EGG WITH SPINACH AND CHEESE RÖSTI]]')])
    + STERN
    + G('CHÄS MIT UND OHNI LÖCHER', zeilen=[('f', 'Fromage de la région'), ('f', '[[CHEESE]]')])
    + STERN
    + G('DESSERT ZUM USELÄSE', zeilen=[('f', 'Dessert au choix'), ('f', '[[DESSERT TO CHOOSE]]')])
    + R('FÜR ÜSI CHLINE', 'POUR VOS ENFANTS', 'FOR CHILDREN')
    + '<p class="unterzeile">(Für unsere Kleinen)</p>'
    + G('GEFÜLLTI RÖSTITÄTSCHLI', '9.50', zeilen=[('f', 'Pochettes de rösti farcies au fromage'), ('f', '[[POTATOES CROQUETTES FILLED WITH CHEESE]]')])
    + G('HÖRNLI MIT PILZSOSSE', '9.50', zeilen=[('f', 'Cornettes, sauce aux champignons'), ('f', '[[NOODLES WITH MUSHROOM SAUCE]]')])
    + '<i class="ulin ulin--breit"></i>'
    + G('KAFFFEE FERTIG', '8.00', zeilen=[('d', 'Ds traditionelle mit Bätzi (Obstler)'), ('f', '[[Café FERTIG]] avec de l’alcool blanc de différents fruits'), ('f', 'coffee with schnaps')])
    + G('KAFFEE LUTZ', '8.00', zeilen=[('d', 'Ds Helle us em Entlibuch'), ('f', '[[Café LUTZ]] une spécialité de l’Entlebuch'), ('f', 'a speciality with schnaps')])
    + G('RUEDIHUSKAFFEE', '13.00', zeilen=[('d', 'Mit Quitteschnaps und Nydlehübli'), ('f', '[[Café RUEDIHUS]] avec de l’alcool de coings et crème fraîche'), ('f', 'coffee with quince schnaps and whipped cream')])
    + G('ZUGERKAFFEE', '13.00', zeilen=[('d', 'Mit kräftigem Kirsch und Nydlehübli'), ('f', '[[Café ZOUGOIS]] avec du kirsch et crème fraîche'), ('f', 'coffee with cherry schnaps and whipped cream')])
    + G('WALLISERKAFFEE', '13.00', zeilen=[('d', 'Mit Williams und Nydlehübli'), ('f', '[[Café VALAISAN]] avec de la Williamine et crème fraîche'), ('f', 'coffee with williams schnaps and whipped cream')]),
    kl='karte egger dicht', kopf=S.leiste(), fuss=False)

k2_6 = S.blatt(
    R('ZUM DESSERT', kopf=('Kleine Portion', 'Portion'))
    + G('BRÖNNTI CREME', ('7.50', '9.50'), n=2, zeilen=[('f', 'Crème caramel / [[CARAMEL CREAM]]')])
    + G('ÖPFELCHÜCHLI', ('14.00', '16.00'), 'mit Vanillesosse', n=2, zeilen=[('f', 'Beignets de pommes, sauce vanille / [[APPLE FRITTERS, VANILLA SAUCE]]')])
    + G('Coupe Ruedi', ('10.50', '14.00'), n=2, kl='vers', zeilen=[('d', 'Vanilleglacé mit warmen Waldbeeren'), ('f', 'Glace vanille et fruits chauds / [[VANILLA ICE CREAM WITH HOT BERRIES]]')])
    + G('Zwetschgenlisi', ('10.50', '14.00'), n=2, kl='vers', zeilen=[
        ('d', 'Zwetschgensorbet mit eingelegten Grappazwetschgen und Zwetschgenschnaps'),
        ('f', 'Sorbet aux pruneaux avec de la grappa de pruneaux et du schnaps de pruneaux'),
        ('f', '[[PRUNE SORBET WITH PRUNE GRAPPA AND PRUNE SCHNAPS]]')])
    + G('MERINGUE mit Greyerzer Nydle', ('12.50', '16.00'), n=2, zeilen=[('f', 'Meringue avec crème de Gruyère / [[MERINGUE WITH GREYERZER CREAM]]')])
    + G('VACHERIN GLACE “das Ruedihus Special”', ('18.00',), n=2, zeilen=[('d', 'SIE DÜRFEN GERNE EINEN 2. LÖFFEL BESTELLEN'), ('f', '[[TYPICAL SWISS DESSERT]]')])
    + G('COUPE APRICOTINE', ('10.50', '14.00'), n=2, zeilen=[
        ('d', 'Vanille Glace und Aprikosensorbet mit eingelegten Aprikosen und Apricotine'),
        ('f', 'Glace à la vanille, sorbet d’abricot, abricots marinés et Apricotine'),
        ('f', '[[VANILLA ICE CREAM, APRICOT SORBET, MARINATED APRICOTS AND APRICOTINE]]')])
    + G('ÖPFUSORBET', ('10.50', '14.00'), 'mit Gravesteiner', n=2, zeilen=[('f', 'Sorbet pomme avec gravensteiner/ [[APPLESORBET WITH GRAVENSTEINER]]')])
    + G('COUPE ROMANTIC', ('10.50', '14.00'), n=2, zeilen=[
        ('d', 'Haselnussglacé mit Appenzellerrahmliqueur'),
        ('f', 'Glace vanille et noisette avec liqueur d’Appenzelle'),
        ('f', '[[VANILLA AND HAZELNUT ICE CREAM WITH APPENZELLER LIQUEUR]]')])
    + G('ZUGER KIRSCHTURTE', ('8.00',), 'Eine Kirschtorte die es in sich hat', n=2, zeilen=[('f', 'Tourte au Kirsch / [[CHERRY CAKE]]')])
    + G('AARGAUER RÜEBLITURTE', ('7.00',), n=2, zeilen=[
        ('d', 'Eine echte Schweizer Spezialität aus Haselnüssen und Karotten'), ('f', 'Gâteau aux carottes / [[CARROT CAKE]]')])
    + G('Sorbet und Glacé pro Kugel', ('3.50',), n=2, zeilen=[
        ('d', 'Zwetschgensorbet, Apfelsorbet, Aprikosensorbet, Haselnussglacé, Vanilleglacé, Schoggiglacé, Erdbeerglacé'),
        ('f', 'Sorbet et glaces : Prune, Pomme, Abricot, Noisette, Vanille, Chocolat et Fraise'),
        ('f', '[[SORBET AND ICE-CREAM: PLUM, APPLE, APRICOT, HAZELNUT, VANILLA, CHOCOLATE AND STRAWBERRIES]]')])
    + f'<p class="hinweis">{e(ALLERGIE)}</p>',
    kl='karte egger dessert', kopf=S.leiste(), fuss=False)

# Alle Karten-Seiten in einer Schriftgrösse (die volle Seite 5 gibt das Mass vor); das Tagesmenu ist eine Tabelle und bleibt für sich.
k2_2, k2_3, k2_5, k2_6 = (mx(x, 1.05) for x in (k2_2, k2_3, k2_5, k2_6))

# ================================================================ Chäs- und Wystube (2 Seiten A3 quer)
_ort[0] = 'chaes-und-wystube'
_geschichte = (
    '<p class="vorzeile">GESCHICHTE</p><h2 class="ut">Das RUEDIHUS</h2>'
    + ab('wurde 1753 durch Peter Germann erbaut. Es gilt als Spitzenleistung der Zimmermannskunst im 18. Jahrhundert. Ganz ausserordentlich ist auch die '
         'Ausstattung der Innenräume die zum grossen Teil noch vorhanden ist. Die Türen sind gekleistert oder bemalen, alle Türstürze haben ein barockes Profil, '
         'ferner stehen da bemalte Buffets und Truhen. Doch was den Innenräumen die unvergleichliche Atmosphäre verleiht, sind die Reihenfenster mit den '
         'Butzenscheiben. (aus dem Frutigbuch)')
    + ab('Es diente als Wohnung für den Landsvenner Peter Germann und als Maultier-Wechselstation für Reisende über die Gemmi, sowie später als Gaststätte. '
         'Der Name des Hauses muss wohl von jenem Rudolf Reichen stammen (ca. 1850) der den ganzen Besitz erwerben konnte und somit im Volksmund „ds '
         'rich Ruedi“ genannt wurde. Im Jahre 1908 brach im hinteren Teil des Gebäudes Feuer aus. In der Tageszeitung „der Bund“ steht (auszugsweise):')
    + ab('Ein seltenes Schauspiel in der hinteren Kandersteger Ebene. Kerzengerade steht eine Riesenrauchsäule im Tal. Die Sonst so gemächlichen Älpler rennen das Tal '
         'hinein ein Schlitten fährt im Galopp vorbei. Es ist keine Frage, es handelt sich um eine Feuersbrunst. Richtig, da hört man schon das Ruedihus brennt. In der Tat '
         'das Ruedihus, neben dem alten Teil des Hotels Viktoria und einem zweiten, 1556 erbauten Bauernhaus, das älteste, daneben aber bei weitem das originellste Haus '
         'des ganzen Kandertals, ist zum Teil ein Raub der Flammen geworden. Das Ruedihus war eine bauliche Sehenswürdigkeit des Tales. Seine reich verzierte '
         'Fassade mit den Reihen von Rundschreibenfenstern viel jedem Beobachter sofort auf. Peter Germann, einem alten Volksglauben nachlebend, liess in einer einzigen '
         'bestimmten Novembernacht alles Holz zu seinem künftigen Heim schlagen. Nur dann würde der Segen auf demselben ruhen und die Stürme darüber '
         'hinwegbrausen. Unter solchem Glauben entstand 1753 das Ruedihus. Auch seine Einrichtung ging in manchem Stücke, nach des Landes guter, alter Sitte. Tür und '
         'Fenster liess man sich schenken. Die Fenstergaben waren ohnehin noch allenthalben im Bernerlande im Schwung. Auch die Giebelseite musste '
         'offenbaren, dass ein Mann hier sitze, der etwas sei und etwas wolle. Und so genügten denn auch die hölzernen Zierarten nicht. leuchtende Farben mussten '
         'hinein.', 'zitat')
    + ab('Die gekröpften Leisten, die Stäbe, das Gesimmse alles wurde bemalt, Darum war auch der Schreck unter der Bevölkerung gross, als es hiess, das Ruedihus steht '
         'in Flammen. En Glück, dass der Schnee dem Dach einen Rückhalt gab. So haben wenigsten die Fassade Grösstenteils und die Fensterreihe, sowie die originellen '
         'Türen keinen Schaden genommen. Materiell ist das Haus aber so gut wie eine Ruine. In der Scheune vom Ruedihaus, das seit Jahren an fremde Sommergäste '
         'vermietet wurde, ist neuerdings eine Schule für Italiener Kinder eingebaut worden. Das Haus selbst dient als Wohnung für den katholischen Geistlichen und '
         'für Beamte der Lötschbergunternehmung. Der Schaden ist durch die Versicherung teilweise gedeckt.', 'zitat')
    + '<p class="quelle">Der BUND 12.1.1908</p>'
    + ab('Dass der vordere Teil erhalten blieb schrieben die Einwohner des Dorfes der vermuteten Tatsache zu, dass beim Hausbau unter die Schwelle der '
         'Eingangstüre das Kraut Allermannsharnisch gelegt worden sei. Die Pflanze, welche unter dem Panzer getragen wurde, um sich vor tödlicher Verletzung '
         'zu schützen.'))
_heute = (
    ab('Der brandgeschädigte Teil wurde wiederaufgebaut und im November 1908 wurde eine Schule für Kinder, der am Bahnbau beteiligten Italiener eröffnet. '
       'Nach der Bauzeit wurde das Ruedihus auch als Pension betrieben. Am 21. Dezember 1990 konnten wir das Haus erwerben. Mit einer umsichtigen, '
       'sanften Renovation haben wir das Haus wiederum in einen Zustand gebracht, der es uns ermöglicht, einen zweckmässigen Landgasthof zu '
       'führen, unter Berücksichtigung seiner wertvollen, historischen Bedeutung. Im Februar 1991 haben wir den Betrieb wiedereröffnet.')
    + ab('Kontinuierlich haben wir das Haus restauriert, was mit der besonderen Auszeichnung, historisches Hotel Restaurant des Jahres 2000, gewürdigt '
         'wurde. Tausende von Gästen sind hier ein und ausgegangen, besonders gefreut hat uns, dass wir in den vergangenen Jahren den GESAMT-BUNDESRAT '
         'dreimal bei uns begrüssen durften. Herr KOFI ANAN, Generalsekretär der UNO und seine Frau, PRINZ CHARLES von Wales, und '
         'das BELGISCHE KÖNIGSPAAR waren ebenfalls unsere Gäste.')
    + ab('Wichtig jedoch sind SIE und wir freuen uns, wenn es Ihnen bei uns gefällt.', 'stark')
    + '<p class="gruss">Wir danken Ihnen für Ihren Besuch<br>Familie Maeder und ihre Crew</p>'
    + '<p class="gruss gruss--2">Nellija Rakovska <span>Gastgeberin</span></p>'
    + S.kasten('DAS KONZEPT', ab('Unser oberstes Prinzip ist: Nur ausgesuchte Produkte aus der Schweiz verwenden. Zurück zu einer Küche ohne Firlefanz, natürlich passend zum '
                                 'Haus. Sie suchen deshalb vergebens nach ausländischen Produkten, mit ganz wenigen Ausnahmen.'))
    + S.kasten('UNSER ANGEBOT', S.liste([r(x) for x in [
        'CHÄS- UND WYSTUBE mit 40 Sitzplätzen.',
        'JUNGENSTUBE mit 25 Sitzplätzen, geeignet auch für Sitzungen und Familienfeste.',
        '2 Biedermeierstuben im 1. Stock EGGER- und STETTLERSTUBE, Die vornehmen Bernerstuben für den besonderen Anlass.',
        '7 DOPPELZIMMER, wovon 3 mit Himmelbetten',
        '1 EINZELZIMMER, 1 HOCHZEITSSTUBE,',
        '1 LIEBESLAUBE, 2 HIMMELREICH']]))
    + S.kasten('GESCHENKGUTSCHEINE',
               ab('Gerne stellen wir Ihnen einen Geschenkgutschein aus, zum Beispiel eine Übernachtung mit Frühstück für 2 Personen')
               + '<p class="gzeile">im Doppelzimmer <b>CHF 250.00</b></p><p class="gzeile">in der Hochzeitsstube <b>CHF 300.00</b></p>'
                 '<p class="gzeile">' + r('in unsere Liebeslaube') + ' <b>CHF 390.00</b></p><p class="gzeile">und den zwei Juniorsuiten HIMMELREICH</p>'
                 '<p class="gzeile"><b>für CHF 390.00 für zwei Personen.</b></p>'
               + '<h3 class="gz2">oder einen GOURMETAUFENTHALT</h3>'
               + '<p class="gzeile">2 Übernachtungen im RUEDIHUS</p><p class="gzeile">1 Rustikales Nachtessen in der Biedermeierstube</p>'
                 '<p class="gzeile">' + r('1 Menu Gastronomique (7 gängiges Feinschmeckermenu) im WALDHOTEL DOLDENHORN') + '</p>'
                 '<p class="gzeile"><b>ab CHF 450.00 pro Person</b></p>', kl='dunkel mitte'))
k1_1 = S.blatt(S.spalten(
    _geschichte, _heute,
    deckel('Schpiszettel',
           'Die feinste Reisekunst besteht darin, zu einigen besonders schönen Plätzen immer wieder einmal zurückzukehren, bis sich in uns eine Art Heimatgefühl entwickelt, das sie doppelt kostbar macht.',
           'Graff', 'LANDGASTHOF RUEDIHUS\n3718 KANDERSTEG\nTel 033 675 81 82 · Fax 033 675 81 85\nMail : info@doldenhorn.ch\nwww. doldenhorn-ruedihus.ch'),
    kl='aussen'), kl='karte karte--aussen a3', fuss=False, format=A3)

_sp1 = (
    R('SUPPE', 'Potages', 'Soups')
    + G('TAGESSUPPE', '10.50', zeilen=[('f', 'Soupe du jour, soup of the day')])
    + G('GÄRSCHTESUPPE', '14.00', zeilen=[('x', [('d', 'Gerstensuppe,'), ('f', 'Crème d’orges des Grisons, Barley – soup')])])
    + R('PLÄTTLI', 'Hors d’oeuvre', 'Starters')
    + G('MOSTBRÖCKLI', '28.00', zeilen=[
        ('x', [('d', 'Chline Täller'), ('f', 'Entrée –petite portion as starter, small portion')], '22.00'),
        ('f', 'Viande séchée de bœuf, air dried beef')])
    + G('TROCHEWURSCHT MIT HOBELCHÄS', '27.00', zeilen=[('f', 'Saucisse séchée avec fromage raboté, air-dried sausage and mountain cheese')])
    + G('E SCHNIFU BUREHAMME', '24.00', zeilen=[('x', [('d', 'Kalter Bauernschinken,'), ('f', 'Jambon de campagne froid')]), ('f', 'Cold farmer’s ham')])
    + G('HOBELCHÄS', '22.00', zeilen=[('x', [('d', 'Einheimischer Hobelkäse,'), ('f', 'Fromage de montagne raboté,')]), ('f', 'A portion of shaved mountain cheese')])
    + R('SALAT', 'Salades', 'Salad')
    + G('GRÜNER SALAT', '10.50', 'im Schüsseli', [('f', 'Salade verte, green salad')])
    + G('RANDESALAT', '11.50', 'mit Boumnüss u Zwibele', [('f', 'Salade de betteraves rouges, Beetroot salad')])
    + R('ÖPIS URCHIGS', 'Plat principales', 'Main Plates')
    + G('BAUERNRÖSCHTI', '29.00', 'Rösti mit Hobelchäs', [
        ('k', KP, '24.00'),
        ('d', 'Rösti (ohne Speck) mit Hobelkäse (vegetarisch)'),
        ('f', 'Rösti (sans lard) avec fromage de montagne (végétarien)'),
        ('f', 'FARMERS RÖSTI with local shaved mountain cheese')])
    + G('CHÄSRÖSCHTI', '29.00', 'Speckrösti mit Raclette überbacken', [
        ('k', KP, '24.00'),
        ('f', 'Rösti au lard gratiné avec Raclette'),
        ('f', 'CHEESE RÖSTI, Raclette cheese melted on a bacon Rösti')])
    + G('JÄGERRÖSCHTI', '30.00', 'Speckrösti are feine Sosse mit vielne Waldpilze', [
        ('k', KP, '26.00'),
        ('f', 'Rösti chasseur, rösti au lard avec une bonne sauce aux champignons'),
        ('f', 'HUNTERS RÖSTI, bacon rösti with a fine sauce with lots of forest mushrooms')])
    + G('ANKERÖSCHTI', '32.50', 'Speckrösti mit amnä bitz kalte Burehamme', [
        ('k', KP, '29.00'),
        ('d', 'Speckrösti mit kaltem Bauernschinken'),
        ('f', 'Rösti au lard avec jambon de campagne froid'),
        ('f', 'Bacon rösti with cold farmer’s ham')])
    + G('SENNEHÖRNLI', '26.00', zeilen=[
        ('d', 'Hörnli mit Schinkenstreifen an Rahmsauce'),
        ('f', 'Cornettes à la crème, Jambon et fromage'),
        ('f', 'Pasta with stripes of ham, in a cream sauce, topped with melted cheese')])
    + G('CHÄSSCHNITTE', '26.00', 'mit Ei und Schinken', [
        ('k', KP, '22.00'),
        ('f', 'Croûte au fromage garnie d’un oeuf au plat et jambon'),
        ('f', 'Melted cheese on wine soaked toast with a fried egg and ham “Swiss speciality”')])
    + R('FÜR DI CHLINE', 'Kinderteller, pour vos enfants, for your children')
    + G('GFÜLLTI RÖSCHTITÄSCHLI', '9.50', zeilen=[('f', 'Pochette de rösti farcie au fromage'), ('f', 'Rösti-pocket filled with cheese')])
    + G('HÖRNLI MIT PILZSOSSE', '9.50', zeilen=[('f', 'Cornettes avec sauce aux champignons'), ('f', 'Pasta with mushroom sauce')]))
_sp2 = (
    R('RACLETTE')
    + G('RACLETTE', '36.00', 'SO VIEL DR MÖGET', [('f', 'Raclette à discrétion'), ('f', 'Raclette (melted cheese) served with potatoes')])
    + G('RACLETTE', '12.00', 'PORTION')
    + R('FONDUES')
    + G('FRIBURGER ORIGINAL CHÄSFONDUE', '29.00', zeilen=[
        ('d', 'DR RAHMIG VACHERIN GIT IHM E BSUNDERE GOUT'), ('f', 'Fondue Fribourgeoise au Vacherin'),
        ('f', 'The creamy “Vacherin” cheese gives this fondue a special taste')])
    + G('WALLISER TOMATEFONDUE', '35.00', zeilen=[
        ('d', 'FRÜSCHI TOMATEWÜRFELI UND TOMATEMARK MIT GSCHWELTI'), ('d', 'Käsefondue mit Tomaten und Pellkartoffeln'),
        ('f', 'Fondue aux tomates'), ('f', 'Cheese Fondue with tomato and potatoes boiled in their skin')])
    + G('SPÄCKFONDUE', '35.00', zeilen=[
        ('d', 'SPÄCKWÜRFELI UND ZIEBELE, DIE WÜRZIGI FONDUEÜBERRASCHIG'), ('d', 'Käsefondue mit Speck und Zwiebeln'),
        ('f', 'Fondue avec lard et oignons'), ('f', 'Cheese Fondue with bacon and onions')])
    + G('MORCHELFONDUE', '39.00', 'MIT FEINE SPITZMORCHLE', [
        ('d', 'Käsefondue mit Morcheln'), ('f', 'Fondue aux morilles'), ('f', 'Morel Fondue, the king of the mushrooms')])
    + G('TRÜFFELFONDUE', '48.00', zeilen=[('d', 'Käsefondue mit Trüffel'), ('f', 'Fondue aux aux truffes'), ('f', 'Fondue with truffles')])
    + S.kasten('FONDUE ODER RACLETTE MENU',
               '<p class="mg">MOSTBRÖCKLITÄLLER</p><p class="mf">VIANDE SÉCHÉE Cured (air dried) beef marinated in cider</p>' + STERN
               + '<p class="mg">FRIBURGER FONDUE oder Raclette à discrétion</p><p class="mf">FONDUE FRIBOURGEOIS OU RACLETTE Fondue or Raclette</p>' + STERN
               + '<p class="mg">EN CHLINE KIRSCH</p><p class="mf">UN PETIT KIRSCH a small cherry schnapps</p>' + STERN
               + '<p class="mg">ÖPFUSORBET</p><p class="mf">SORBET DE POMMES apple sorbet</p>'
               + '<p class="mpreis">48.00</p>', kl='dunkel mitte menu')
    + G('ZVIERI PLÄTTLI', '28.00', zeilen=[
        ('d', 'Walliser Trockenfleisch, Coppa und Rohessspeck aus der Fleischtrocknerei Eggs in Reickingen, Kandersteger Hobelkäse aus dem Ueschinental von Hans Rösti und Kandersteger Dauerwurst'),
        ('f', 'Viande séchée du Valais, lard crû, coppa et fromage raboté'),
        ('f', 'Dry meat from the Valais, coppa, raw meat and mountain cheese')], kl='zvieri')
    + S.kasten('', ab('Im ganzen Haus gilt als oberstes Gebot (mit ganz wenigen Ausnahmen), Schweizer Produkte zu verwenden, möglichst direkt vom Produzenten. '
                      'Sie suchen vergebens Campari, Orangensaft, Salzwasserfische, Cognac oder Cola.', 'klein mitte'), kl='gebot')
    + f'<p class="hinweis">{e(ALLERGIE)}</p>')
_sp3 = (
    R('ZUM DESSERT', kopf=('Kleine Portion', 'Portion'))
    + G('CRÈME CARAMEL', ('7.50', '9.50'), n=2, zeilen=[('f', 'Crème caramel, Carmel cream')])
    + G('ÖPFELCHÜCHLI', ('14.00', '16.00'), 'mit Vanillesosse', n=2, zeilen=[('f', 'Beignets aux pommes avec sauce vanille, Apple fritters with vanilla sauce')])
    + G('COUPE RUEDI', ('10.50', '14.00'), n=2, zeilen=[('d', 'Vanilleglacé mit warmen Waldbeeren'), ('f', 'Glace vanille et fruits chauds, Vanilla ice cream with hot berries')])
    + G('ZWETSCHGENLISI', ('10.50', '14.00'), n=2, zeilen=[
        ('d', 'Zwetschgensorbet mit eingelegten Grappazwetschgen und Zwetschgenschnaps'),
        ('f', 'Sorbet de prunes avec prunes marinées à la grappa avec eau de vie de prune'),
        ('f', 'Prune sorbet with prune marinated in Grappa and a prune schnapps')])
    + G('MERINGUE mit Greyerzer Nydle', ('12.50', '16.00'), n=2, zeilen=[('f', 'Meringue avec crème de Gruyère'), ('f', 'Meringue with Greyerzer cream')])
    + G('VACHERIN GLACE', ('18.00',), 'das Ruedihus Special', n=2, zeilen=[('d', 'Sie dürfen gerne einen 2. Löffel bestellen'), ('f', 'Typical Swiss Dessert')], kl='g--stark')
    + G('COUPE APRICOTINE', ('10.50', '14.00'), n=2, zeilen=[
        ('d', 'Vanille Glace und Aprikosensorbet mit eingelegten Aprikosen und Apricotine'),
        ('f', 'Glace vanille, sorbet d’abricot, abricots marinés et Apricotine'),
        ('f', 'Vanilla ice cream, apricot sorbet, marinated apricots and Apricotine')])
    + G('ÖPFUSORBET', ('10.50', '14.00'), 'mit Gravensteiner', n=2, zeilen=[('f', 'Sorbet de pomme avec Gravensteiner, Apple sorbet with Gravensteiner')])
    + G('COUPE ROMANTIC', ('10.50', '14.00'), n=2, zeilen=[
        ('d', 'Vanille und Haselnussglacé mit Appenzellerrahmliqueur'),
        ('f', 'Glace vanille et noisette et liqueur d’Appenzell'),
        ('f', 'Vanilla and hazelnut ice cream with Appenzeller liqueur')])
    + G('ZUGER KIRSCHTURTE', ('8.00',), n=2, zeilen=[('d', 'Eine Kirschtorte die es in sich hat'), ('f', 'Tourte au Kirsch / Cherry schnapps cake')])
    + G('AARGAUER RÜEBLITURTE', ('7.00',), n=2, zeilen=[
        ('d', 'Eine echte Schweizer Spezialität aus Haselnüssen und Karotten'), ('f', 'Gâteau aux carottes et aux noisettes / Carrot cake with hazel nuts')])
    + G('Sorbet und Glacé pro Kugel', ('3.50',), n=2, zeilen=[
        ('d', 'Zwetschgensorbet, Apfelsorbet, Aprikosensorbet, Haselnussglacé, Vanilleglacé, Schoggiglacé und Erdbeerglacé'),
        ('f', 'Sorbet aux prunes, aux pommes, à l’abricot, glace noisette, vanille, chocolat et fraise / sorbet and ice-cream : plum, apple, apricot, hazelnut, vanilla, chocolate and strawberries')])
    + R('KAFFEE', 'Café', 'Coffee')
    + G('KAFFEE FERTIG', ('8.00',), n=2, zeilen=[
        ('x', [('d', 'Das “Traditionelle“ mit Obstler,'), ('f', 'le café traditionnel avec du schnaps et du sucre / the traditional Swiss coffee with schnapps, sugar')])])
    + G('KAFFEE LUTZ', ('8.00',), n=2, zeilen=[
        ('d', 'Der “Dünne“ aus dem Entlebuch + Obstler oder Zwetschge'), ('f', 'Kaffee Lutz, speciality of county Entlebuch, without cream')])
    + G('RUEDIHUSKAFFEE', ('13.00',), n=2, zeilen=[
        ('d', 'Mit Quittenschnaps und Rahm'), ('f', 'café avec eau de vie de coing et chantilly'), ('f', 'coffee with Quince schnapps and whipped cream')])
    + G('ZUGERKAFFEE', ('13.00',), n=2, zeilen=[
        ('x', [('d', 'Mit kräftigem Kirsch und Rahm /'), ('f', 'avec eau de vie de Kirsch, chantilly')]),
        ('f', 'Zuger coffee, from the canton of Zug, with a strong cherry schnapps')])
    + G('WALLISER KAFFEE', ('13.00',), n=2, zeilen=[
        ('d', 'Mit Williams und Rahm'), ('f', 'avec de la williamine et chantilly'), ('f', 'Walliser coffee, with pear schnapps and cream')]))
k1_1 = k1_1.replace('(aus dem Frutigbuch)', '<span class="nb">(aus dem Frutigbuch)</span>')   # Quellangabe nicht über zwei Zeilen
k1_2 = S.blatt(S.spalten(_sp1, _sp2, _sp3), kl='karte a3 innen', fuss=False, format=A3)

# ================================================================ Tagesteller (2 Seiten A4)
_ort[0] = 'tagesteller'
_gut = (f'<div class="gutschein">{S.zeichen_gross("mitte")}<h2 class="ut mitte">Einen Geschenkgutschein vom Landgasthof Ruedihus?</h2>{S.linie()}'
        '<p class="ab mitte">Gerne stellen wir Ihnen einen Gutschein<br>mit dem gewünschten Frankenbetrag aus,<br>oder für</p>'
        '<p class="ab mitte">eine Übernachtung für 2 Personen<br>mit Frühstück zum Preis <b>ab CHF 265.00</b></p>'
        '<p class="ab mitte">oder ganz speziell im Hochzeitszimmer<br><b>ab CHF 315.00</b></p>'
        '<p class="ab mitte">oder Liebeslaube und Himmelreich<br><b>ab CHF 390.00</b><br>für 2 Personen inklusive Frühstücks</p></div>')
k3_1 = S.blatt(S.spalten(
    _gut,
    deckel('Mir empfähle Euch',
           'Die Welt wäre eigentlich\nvoller Freuden\nman könnte deren auflesen\nbei jedem Schritt und Tritt,\naber man muss\n„die eigete Ouge ha“,\num sie zu sehen.',
           'Jeremias Gotthelf', 'LANDGASTHOF RUEDIHUS\n3718 KANDERSTEG\nTel 033 675 81 82 · Fax 033 675 81 85\nMail : info@doldenhorn.ch'),
    kl='aussen'), kl='karte karte--aussen', fuss=False)
k3_1 = mx(k3_1, 1)

_tl = (
    teller('Tageställer 1', '32.00', [
        SUPPE, SUPPE_F, '*',
        ('h', '2 POCHIERTI EIER'), ('d', 'uf Blattspinet, Ankesauce, Salzhärdöpfel'),
        ('f', '[[2 ŒUFS POCHÉS]] Sur épinards, sauce au beurre, pommes de terre'),
        ('f', '[[2 POACHED EGGS]] Spinach, butter sauce, potatoes')], zusatz='vegetarisch')
    + teller('Tageställer 2', '34.00', [
        SUPPE, SUPPE_F, '*',
        ('h', 'POULETBRÜSCHTLI aus Schweizer Zucht'), ('d', 'Pilzsosse, Spätzli, Gmües vom Pflanzblätz'),
        ('f', '[[POITRINE DE POULET]] Sauce aux champignons, Spätzli, légumes du potager'),
        ('f', '[[CHICKEN BREAST]] Mushroom sauce, Spätzli, vegetables')])
    + teller('Tageställer 3', '44.00', [
        SUPPE, SUPPE_F, '*',
        ('h', 'KILTERSCHNITTE Lyoner Härdöpfel Späck und Zibele'), ('d', 'Entrecôte überbacken mit Lyoner Kartoffeln, Speck, Zwiebel'),
        ('f', '[[ENTRECÔTE GRATINÉE,]] Avec pommes de terre lyonnaises, lardons, oignons'),
        ('f', '[[SIRLOIN STEAK GRATINATED]] With Lyon potatoes, bacon, onion')])
    + teller('Tageställer 5', '34.00', [
        SUPPE, ('f', 'Salade / Salad'), '*',
        ('h', 'CHUTTLE MIT TOMATESOSSE'), ('d', 'Gschwelti'),
        ('f', '[[TRIPES SAUCE TOMATE]] Pommes de terre en robe du champ'),
        ('f', '[[TRIPES]] Tomato sauce, potatoes in their skin')])
    + teller('Tageställer 6', '36.00', [
        SUPPE, SUPPE_F, '*',
        ('x', [('h', 'RAHMSCHNITZEL'), ('d', '(Schwynigs) wie früecher,\nNüdeli & Pilzsosse')]),
        ('f', '[[ESCALOPE À LA CRÈME]] (porc), Nouilles, Sauce aux champignons'),
        ('f', '[[PORC ESCALOPE]] Cream sauce, pasta, Mushroom sauce')]))
_tr = (
    teller('BURETÄLLER', '32.00', [
        SUPPE, SUPPE_F, '*',
        ('d', 'Burebratwurscht, Zibelesosse, Rösti'),
        ('f', '[[ASSIETTE PAYSANNE]] Saucisse à rôtir, sauce aux oignons, Röst'),
        ('f', '[[FARMERS PLATE]] Sausage, onion sauce, Rösti')])
    + teller('FISCHTÄLLER', '48.00', [
        ('d', 'E ganzi Forälle brate, Salzhärdöpfel und Spinat'),
        ('f', '[[PLAT DE POISSON]] Truites fraîches rôti, garnie de pommes de terre à lèau et épinards'),
        ('f', '[[FISHERMANS PLATE]] Fresh trout from roasted with potatoes and spinach')])
    + teller('CHALBSLÄBERLI', '46.00', [
        ('d', 'Chalbsläberli Im Anke brate mit Röschti u Gmües'),
        ('f', '[[FOIE DE VEAU]] Emincé de der foie de veau sauté au beurre « rösti », légumes'),
        ('f', 'Sliced veal liver with Rösti')])
    + f'<p class="hinweis hinweis--frei">{e(ALLERGIE)}</p>'
    + S.kasten('', ab('Wir verwenden mit Ausnahme der Kilterschnitte ausschliesslich Schweizer Fleisch (Rind, Kalb, Schwein, Lamm). Die auf Schweizer '
                      'Bauernhöfen aufgezogen werden. Eine artgerechte Haltung und natürliche Fütterung wird nicht nur garantiert. Bei der Kilterschnitte müssen wir unser '
                      'Prinzip leider verlassen, da nicht genügend gutgelagertes Schweizer Fleisch zur Verfügung steht, deshalb servieren wir ihnen erstklassige argentinische '
                      'Stücke.', 'klein'), kl='gebot')
    + S.kasten('', ab('Im ganzen Haus gilt als oberstes Gebot (mit ganz wenigen Ausnahmen) Schweizer Produkte zu verwenden, möglichst direkt vom Produzenten. '
                      'Sie suchen vergeblich Campari, Cognac, Orangensaft, Salzwasserfische, und Cola.', 'klein'), kl='gebot')
    + S.kasten('', '<p class="ab klein"><span class="marke marke--satz">BIO</span> '
               + fmt('steht für Speisen und Gerichte, für die wir ausschliesslich natur- und tiergerechte Zutaten in Bio-Qualität verwenden.').replace('Bio-Qualität', '<span class="nb">Bio-Qualität</span>') + '</p>', kl='gebot'))
k3_2 = S.blatt(S.spalten(_tl, _tr), kl='karte tagesteller', kopf=S.leiste(), fuss=False)

# ================================================================ Gestaltung (hängt satz.py hinter den Stil der Vorlage)
H.CSS_SATZ = getattr(H, 'CSS_SATZ', '') + '''
/* ===== Unterlagen Fassung 2 (09.10.2026) ===== */
.blatt .rubrik{align-items:baseline;margin:calc(6mm*var(--s)) 0 calc(1.5mm*var(--s));padding-bottom:calc(2.3mm*var(--s));font-size:calc(17pt*var(--s))}
.blatt .sp>.rubrik:first-child,.blatt .inhalt>.rubrik:first-child,.blatt .ukasten>.rubrik:first-child{margin-top:0}
.blatt .rubrik small{font-size:calc(7.6pt*var(--s));letter-spacing:.08em;text-transform:uppercase;color:#674c31;margin-left:3mm}
.blatt .rubrik .rp{font-size:calc(15pt*var(--s))}
.kopfz{display:flex;flex:none}
.kopfz b{width:calc(var(--pb,13.5mm)*var(--s));text-align:right;font-family:'Instrument Sans',Arial,sans-serif;font-weight:500;font-size:calc(6.6pt*var(--s));color:#674c31;white-space:nowrap}
.g{padding:calc(1.5mm*var(--s)) 0;break-inside:avoid}
.gz{display:flex;justify-content:space-between;align-items:baseline;gap:4mm}
.gz>h4,.gz>p{flex:1;min-width:0;text-wrap:pretty}
.g .gz>p:only-child{padding-right:calc(var(--pb,13.5mm)*var(--s))}
.blatt .ab,.blatt .ul li,.blatt p.hinweis,.blatt .tmsp p{text-wrap:pretty}
.blatt p.hinweis{text-wrap:balance}
.blatt .g h4{font-family:'Instrument Sans',Arial,sans-serif;font-weight:600;font-size:calc(10pt*var(--s));line-height:1.3;color:#1c130d}
.blatt .g h4 small{font-weight:400;font-size:calc(8.4pt*var(--s));color:rgba(28,19,13,.76);margin-left:.5mm}
.marke{display:inline-block;vertical-align:.12em;margin-left:1.6mm;padding:.1mm 1.5mm;border:.25mm solid #7f5731;border-radius:1mm;font-family:'DM Mono',Menlo,monospace;font-weight:400;font-size:calc(5.6pt*var(--s));letter-spacing:.14em;text-transform:uppercase;color:#674c31;white-space:nowrap}
.blatt .g p,.blatt .tt p{font-size:calc(8.7pt*var(--s));line-height:1.4;color:rgba(28,19,13,.9)}
.blatt .g p.f,.blatt .tt p.f,.gz span.f{font-style:italic;font-size:calc(8pt*var(--s));color:rgba(28,19,13,.64)}
.gz span.f{font-size:.92em}
.blatt .g p.h,.blatt .tt p.h,.gz span.h{font-weight:600;color:#1c130d}
.blatt .g p.k{font-size:calc(7.6pt*var(--s));color:#674c31}
.ld{font-style:normal;font-weight:500;font-size:.9em;letter-spacing:.05em;color:rgba(28,19,13,.78)}
.prs{flex:none;display:flex}
.prs b{width:calc(var(--pb,13.5mm)*var(--s));text-align:right;font-family:var(--titel);font-weight:var(--tg);font-size:calc(11pt*var(--s));line-height:1;color:#2a180a;white-space:nowrap}
.gz:not(.gz--n) .prs b{font-size:calc(9.4pt*var(--s))}
.blatt p.stern{font-size:calc(6pt*var(--s));letter-spacing:.3em;color:#7f5731;margin:calc(.9mm*var(--s)) 0;line-height:1}
.blatt p.oder{margin:calc(.9mm*var(--s)) 0!important}
.blatt p.unterzeile{font-style:italic;font-size:calc(8pt*var(--s));color:rgba(28,19,13,.64);margin:0 0 calc(1mm*var(--s))}
.blatt p.hinweis{margin-top:auto;padding-top:calc(3mm*var(--s));border-top:.25mm solid rgba(127,87,49,.5);font-size:calc(7.6pt*var(--s));line-height:1.45;color:rgba(28,19,13,.8)}
.blatt p.hinweis--frei{margin-top:calc(5mm*var(--s));border-top:0;padding-top:0;font-size:calc(8pt*var(--s))}
.dicht .g{padding:calc(1.05mm*var(--s)) 0}
.dicht p.stern{margin:calc(.3mm*var(--s)) 0!important}
.dicht .rubrik{margin-top:calc(4.6mm*var(--s))!important}
.dicht .inhalt>.rubrik:first-child{margin-top:0!important}
.dicht .ulin--breit{margin:calc(2.6mm*var(--s)) 0 calc(1.4mm*var(--s))!important}
.ulin--breit{width:100%!important;height:.25mm!important;background:rgba(127,87,49,.5)!important;margin:calc(4mm*var(--s)) 0 calc(2.5mm*var(--s))!important}
.blatt .ab{margin-bottom:calc(2.4mm*var(--s))}
.blatt .ab.stark{font-weight:600;color:#1c130d}
.blatt .ut{margin:0 0 calc(3mm*var(--s))}
.blatt .ukasten .ab:last-child{margin-bottom:0}
.blatt .ukasten h3{margin-bottom:calc(1.8mm*var(--s))}
.ukasten.mitte{text-align:center}
.ukasten.gebot{background:rgba(127,87,49,.07);border-color:rgba(127,87,49,.55)}
.blatt .ul li{font-size:calc(8.6pt*var(--s));line-height:1.42;margin-bottom:calc(.9mm*var(--s))}
/* Egger- und Stettlerstube */
.egger .inhalt{padding:9mm 17mm 11mm}
.ukasten.speziell{margin-top:calc(6mm*var(--s));padding:calc(4.5mm*var(--s)) calc(5mm*var(--s)) calc(3mm*var(--s))}
.dessert{--pb:17mm}
.dessert .g{padding:calc(1.7mm*var(--s)) 0}
.tagesmenu .rubrik{margin-bottom:calc(6mm*var(--s))}
.tmreihe{grid-template-columns:repeat(4,1fr);gap:0 6mm;margin-bottom:calc(8mm*var(--s))}
.tmreihe:last-child{margin-bottom:0}
.blatt .tmsp h4.tag{font-size:calc(14pt*var(--s));line-height:1.1;margin-bottom:0}
.blatt .tmsp p.tagu{font-family:'DM Mono',Menlo,monospace;font-size:calc(6.4pt*var(--s));letter-spacing:.06em;text-transform:uppercase;color:#674c31;margin:calc(1.2mm*var(--s)) 0 calc(3mm*var(--s))}
.blatt .tmsp p.gang{font-weight:600;font-size:calc(9.2pt*var(--s));line-height:1.28;margin:0 0 calc(.5mm*var(--s))}
.blatt .tmsp p.fr{font-style:italic;font-size:calc(7.4pt*var(--s));line-height:1.34;color:rgba(28,19,13,.64)}
.blatt .tmsp p.stern{margin:calc(1.7mm*var(--s)) 0}
/* Chäs- und Wystube */
.karte--aussen.a3 .inhalt{padding:0}
.karte--aussen.a3 .spalten{grid-template-columns:1fr 1.02fr .86fr}
.karte--aussen.a3 .sp{padding:13mm 8mm 11mm 14mm}
.karte--aussen.a3 .sp+.sp:not(:last-child){padding-left:8mm;padding-right:10mm}
.karte--aussen.a3 .sp:last-child{padding:0}
.karte--aussen.a3 .ab{font-size:calc(8.6pt*var(--s));line-height:1.5;margin-bottom:calc(2.4mm*var(--s))}
.karte--aussen.a3 .ab.zitat{font-style:italic;color:rgba(28,19,13,.82);padding-left:4mm;border-left:.4mm solid #7f5731}
.blatt p.vorzeile{font-family:'DM Mono',Menlo,monospace;font-size:calc(6.8pt*var(--s));letter-spacing:.24em;color:#674c31;margin-bottom:calc(1.6mm*var(--s))}
.blatt p.quelle{font-family:'DM Mono',Menlo,monospace;font-size:calc(6.2pt*var(--s));letter-spacing:.16em;text-transform:uppercase;color:#674c31;padding-left:4mm;margin:calc(-.6mm*var(--s)) 0 calc(3mm*var(--s))}
.blatt p.gruss{font-size:calc(8.6pt*var(--s));line-height:1.5;margin:calc(3mm*var(--s)) 0 0}
.blatt p.gruss--2{font-family:var(--titel);font-weight:var(--tg);font-size:calc(10.5pt*var(--s));color:#2a180a;margin:calc(1.6mm*var(--s)) 0 calc(4mm*var(--s))}
.gruss--2 span{font-family:'DM Mono',Menlo,monospace;font-weight:400;font-size:calc(6.2pt*var(--s));letter-spacing:.18em;text-transform:uppercase;color:#674c31;margin-left:2mm}
.blatt p.gzeile{font-size:calc(8.6pt*var(--s));line-height:1.55}
.gzeile b{font-weight:600;color:#f3cd94}
.blatt .ukasten h3.gz2{margin:calc(3mm*var(--s)) 0 calc(1.4mm*var(--s));font-size:calc(11pt*var(--s))}
.ukasten.dunkel .ab,.ukasten.dunkel p{color:#efe4d3}
.ukasten.dunkel .ab{margin-bottom:calc(1.6mm*var(--s))}
.a3.innen .inhalt{padding:13mm 14mm 11mm}
.a3.innen .g{padding:calc(1.15mm*var(--s)) 0}
.a3.innen .rubrik{margin-top:calc(4.6mm*var(--s));margin-bottom:calc(1mm*var(--s));font-size:calc(16pt*var(--s))}
.a3.innen .g p{line-height:1.34}
.a3.innen .spalten{gap:0 14mm}
.a3.innen .spalten--3 .sp+.sp{padding-left:14mm;margin-left:-7mm}
.a3.innen .sp{display:flex;flex-direction:column}
.blatt .ukasten.menu{margin:calc(5mm*var(--s)) 0 calc(4mm*var(--s));padding:calc(5mm*var(--s)) calc(5mm*var(--s))}
.blatt .ukasten.menu h3{font-size:calc(13pt*var(--s));margin-bottom:calc(3mm*var(--s))}
.blatt .menu p.mg{font-weight:600;font-size:calc(9.4pt*var(--s));line-height:1.3;color:#efe4d3}
.blatt .menu p.mf{font-style:italic;font-size:calc(7.8pt*var(--s));color:rgba(239,228,211,.78)}
.blatt .menu p.stern{color:#c98543;margin:calc(1.5mm*var(--s)) 0}
.blatt .menu p.mpreis{font-family:var(--titel);font-weight:var(--tg);font-size:calc(15pt*var(--s));color:#c98543;margin-top:calc(3mm*var(--s));line-height:1}
.blatt .ukasten.gebot{margin:calc(4mm*var(--s)) 0}
.g--stark h4 small{font-weight:600!important;color:#1c130d!important}
/* Tagesteller */
.tagesteller .inhalt{padding:7mm 13mm 11mm}
.tagesteller .sp{display:flex;flex-direction:column}
.tt{padding:calc(3.2mm*var(--s)) 0;border-bottom:.2mm solid rgba(127,87,49,.45)}
.sp>.tt:first-child{padding-top:0}
.tt__k{display:flex;justify-content:space-between;align-items:baseline;gap:4mm;margin-bottom:calc(1.2mm*var(--s))}
.blatt .tt__k h3{font-family:var(--titel);font-weight:var(--tg);font-size:calc(13.5pt*var(--s));line-height:1.15;color:#2a180a}
.tt__k h3 small{font-family:'DM Mono',Menlo,monospace;font-weight:400;font-size:calc(5.8pt*var(--s));letter-spacing:.08em;text-transform:uppercase;color:#674c31;margin-left:2mm}
.tt__k>b{font-family:var(--titel);font-weight:var(--tg);font-size:calc(13.5pt*var(--s));color:#2a180a}
.blatt .tt p.h{font-size:calc(9.2pt*var(--s))}
.tt .gz+.gz .h{margin-top:0}
.tagesteller .ukasten.gebot{margin:calc(3.5mm*var(--s)) 0 0;padding:calc(3.6mm*var(--s)) calc(4.5mm*var(--s))}
.gutschein .ab b{font-family:var(--titel);font-weight:var(--tg);font-size:1.12em;color:#2a180a;white-space:nowrap}
.blatt .gutschein{padding:0 2mm}
.blatt .gutschein .ab{font-size:calc(9.6pt*var(--s));line-height:1.65;margin-bottom:calc(3.2mm*var(--s))}
.blatt .gutschein .ut{margin-bottom:0}
/* ===== QA-Durchgang 09.10.2026 abends ===== */
/* Linien in ganzen Bildpunkten: 0,5 mm (1,89 px) rundete beim Drucken je nach Lage auf 1 oder 2 px, die Linie unter CHÄS war dünner als die anderen */
.blatt .rubrik::after,.blatt .ulin,.deckel>i{height:2px}
.blatt .tmsp{border-top-width:2px}
.ulin--breit{height:1px!important}
/* Spaltenlinie mitten im Zwischenraum, Spalten gleich breit (vorher 7 mm links und 14 mm rechts der Linie, die erste Spalte 7 mm breiter) */
.a3.innen .spalten--3 .sp+.sp{padding-left:7mm;margin-left:-7mm}
.tagesteller .spalten--2 .sp+.sp{padding-left:5.5mm;margin-left:-5.5mm}
/* Dessertnamen der Schpis Charte einheitlich in Versalien (Coupe Ruedi, Zwetschgenlisi standen klein) */
.g.vers h4{text-transform:uppercase}
.a3.innen .sp:last-child{--pb:15.5mm}
.nb{white-space:nowrap}
.marke--satz{margin:0 .6mm 0 0;vertical-align:.1em}
'''

def _w(i, wo):
    return ' '.join(x[i] for x in GENUTZT if x[0] == wo)


# Jede Berichtigung muss gegriffen haben, sonst stimmt die Liste nicht mit dem Wortlaut überein.
_offen = [b_[0] for b_ in BERICHTIGT if not any(g[1] == b_[0] for g in GENUTZT)]
assert not _offen, 'Berichtigung ohne Fundstelle: ' + repr(_offen)
assert all(g[0] in ('egger-und-stettlerstube', 'chaes-und-wystube', 'tagesteller') for g in GENUTZT), 'Berichtigung ohne Unterlage'

DOKS = [
    S.dok('chaes-und-wystube', 'assets/pdf/RH-Chaes-und-Wystube-ab-1.3.2026.pdf', 'Chäs- und Wystube', 'Schpiszettel', [k1_1, k1_2], format=A3,
          dazu='Kleine Portion Portion ' + _w(2, 'chaes-und-wystube'), fehlt=_w(1, 'chaes-und-wystube')),
    S.dok('egger-und-stettlerstube', 'assets/pdf/Egger-und-Stettlerstube-Landgasthof-1.3.2026.pdf', 'Egger- und Stettlerstube', 'Schpis Charte', [k2_1, k2_2, k2_3, k2_4, k2_5, k2_6],
          dazu='BIO Swiss PrimGourmet ' + _w(2, 'egger-und-stettlerstube'), fehlt=_w(1, 'egger-und-stettlerstube')),
    S.dok('tagesteller', 'assets/pdf/Tagesteller-ab-01.03.2026.pdf', 'Tagesteller', 'Mir empfähle Euch', [k3_1, k3_2],
          dazu='BIO ' + _w(2, 'tagesteller'), fehlt='HEUTE NACHT HIER SCHLAFEN warum eigentlich nicht Bis zu 75 Rabatt Drehort von Bauer ledig sucht ' + _w(1, 'tagesteller')),
]

# «Nos Menus», Menuvorschläge 2023 (13.10.2026): Inhalt in nos_menus_daten.py, Gestalt in nos_menus_satz.py
import nos_menus_satz as _NM
DOKS.append(_NM.DOK)
H.CSS_SATZ += _NM.CSS
