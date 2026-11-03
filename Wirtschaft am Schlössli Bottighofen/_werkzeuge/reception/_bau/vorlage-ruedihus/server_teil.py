#!/usr/bin/env python3
"""Hebt den Server-Teil von La Réception (rezeption.py und gedaechtnis.py des Grand Beau-Rivage, nur gelesen) nach _werkzeuge/reception/ und setzt den
Landgasthof Ruedihus ein. Vorbild: _bau/server_teil.py des Waldhotel Doldenhorn und des Carlton-Europe (beide nur gelesen), deren Zusätze hier mitkommen
(Sicherung .gut, Probe des Teams ausserhalb der Gästegrenzen, PDF vom Server, Konflikt statt Überschreiben am Brief, Abteilungen).
Anders als im Doldenhorn hat die Website des Ruedihus kein eigenes Anfrage-Fenster mit Ablage (/api/anfragen): die Formulare der Website schicken über
den Baustein baustein/anfrage.js direkt an den Weg «formular» von La Réception, mit Abteilung, Seite und Formular.
Aufruf: python3 _werkzeuge/reception/_bau/server_teil.py"""
import os, sys
G = os.path.expanduser('~/Desktop/Website-Projekte/Grand Beau-Rivage/website/_gast')
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lade(n):
    return open(os.path.join(G, n), encoding='utf-8').read()


def ers(t, alt, neu, n=1):
    if t.count(alt) != n:
        sys.exit(f'ABBRUCH: «{alt[:80]}» kommt {t.count(alt)}× vor, erwartet {n}×')
    return t.replace(alt, neu)


# ------------------------------------------------------------------ reception.py
t = lade('rezeption.py')
t = ers(t, '"""La Réception · Grand Beau-Rivage. Das Arbeitswerkzeug', '"""Der Gastgeber (La Réception) · Landgasthof Ruedihus. Das Arbeitswerkzeug')
t = ers(t, "(website/mails/)", "(mails/01-tisch, 02-anreise, 03-gutschein)")
t = ers(t, "HIER = os.path.dirname(os.path.abspath(__file__))\nWEB = os.path.dirname(HIER)\nDATEN = os.environ.get('REZEPTION_DATEN') or os.path.join(HIER, 'daten')",
        "HIER = os.path.dirname(os.path.abspath(__file__))\nWEB = os.path.dirname(os.path.dirname(HIER))   # der Ordner des Ruedihus (Website, mails/)\n"
        "DATEN = os.environ.get('RECEPTION_DATEN') or os.environ.get('REZEPTION_DATEN') or os.path.join(HIER, 'daten')")
t = ers(t, "ARTEN = {'zimmer': 'Zimmer', 'tisch': 'Tisch', 'feier': 'Feier', 'tagung': 'Tagung', 'spa': 'Spa', 'aufenthalt': 'Aufenthalt', 'programm': 'Ausflug', 'nachricht': 'Nachricht'}",
        "ARTEN = {'zimmer': 'Zimmer', 'tisch': 'Tisch', 'feier': 'Fest', 'tagung': 'Sitzung', 'gutschein': 'Gutschein', 'spa': 'Spa', 'aufenthalt': 'Aufenthalt', 'programm': 'Ausflug', 'nachricht': 'Nachricht'}")
a = t.index('# Welche Mail-Vorlage des Hauses'); b = t.index("SPRACHEN = (")
t = t[:a] + """# Mail-Vorlagen des Ruedihus: die drei Mails des Hauses (mails/01-tisch, 02-anreise, 03-gutschein, je eine Datei), je Art die passende als Grundlage.
# Absender je Abteilung: Rezeption info@ (jede Seite), Event-Team event@ (Fest-Rechner essen.html), Personal jobs@ (Stellen haus.html). Ein Spa-Team
# hat das Ruedihus nicht (Spa im Waldhotel Doldenhorn gegenüber): Wünsche zum Spa gehen an die Rezeption, wie in der Mail «Vor der Anreise».
VORLAGE = {'zimmer': ('02-anreise', 'info@doldenhorn.ch'), 'aufenthalt': ('02-anreise', 'info@doldenhorn.ch'), 'programm': ('02-anreise', 'info@doldenhorn.ch'),
           'spa': ('02-anreise', 'info@doldenhorn.ch'), 'tisch': ('01-tisch', 'info@doldenhorn.ch'), 'feier': ('01-tisch', 'event@doldenhorn.ch'),
           'tagung': ('01-tisch', 'event@doldenhorn.ch'), 'gutschein': ('03-gutschein', 'info@doldenhorn.ch'), 'nachricht': ('01-tisch', 'info@doldenhorn.ch')}
# Eine Anfrage von der Website antwortet von der Adresse, an die sie ging (Feld «an»); erlaubt sind nur diese drei Adressen des Hauses
ABTEILUNG_VON = {'info@doldenhorn.ch': 'Rezeption', 'event@doldenhorn.ch': 'Event', 'jobs@doldenhorn.ch': 'Personal'}
FORMULARE = ('tisch', 'fest', 'anreise', 'abreise', 'gutschein', 'stelle', 'allgemein')
""" + t[b:]
t = ers(t, "SPRACHEN = ('de', 'en', 'fr', 'zh', 'ko', 'ar')", "SPRACHEN = ('de', 'en', 'fr')")
a = t.index('THEMEN = ['); b = t.index('ABDECKEN = ')
t = t[:a] + """THEMEN = [('Feste im Haus', r'\\bfest\\b|feste|feier|geburtstag|hochzeit|heirat|jubil|verein|sitzung|jungestube|jungenstube|bankett|cüpli|party|birthday|wedding|anniversaire|mariage|fête'),
          ('Hund', r'hund|dog|chien|haustier'),
          ('Gutscheine', r'gutschein|geschenk|schenken|voucher|gift|cadeau'),
          ('Spa im Nachbarhaus', r'spa\\b|sauna|hallenbad|schwimm|pool|massage|wellness|bademantel|piscine|swim|treatment'),
          ('Essen & Stuben', r'restaurant|stube|stübli|fondue|raclette|rösti|röschti|essen|tisch|frühstück|fruehstueck|zmittag|znacht|mittag|abend|menü|menu|karte|schpis|tagesteller|wein|kaffee|vegan|vegetar|végétar|allerg|gluten|laktose|breakfast|dinner|lunch|wine|table|petit.déjeuner|dîner|déjeuner|vin'),
          ('Zimmer & Buchung', r'zimmer|himmelbett|liebeslaube|hochzeitsstube|hymmelrich|landhaus|buch|übernacht|nacht|room|book|stay|night|chambre|réserv|frei\\b|verfügbar|available|check.?in|check.?out|einchecken|storn|annul|cancel'),
          ('Anreise & Abreise', r'park|anreise|abreise|bahnhof|bus\\b|haltestelle|taxi|zug|auto|ladestation|flughafen|gepäck|koffer|arrive|arrival|departure|station|train|airport|parking|luggage|venir|gare|bagage|départ'),
          ('Ausflüge & Region', r'ausflug|oeschinen|kandersteg|gemmi|sunnbüel|sunnbuel|blausee|gastern|wetter|wander|berg|see\\b|schnee|ski|langlauf|schlitt|bike|velo|weather|hike|excursion|lake|mountain|météo|randonn|région|region'),
          ('Stellen', r'job|stelle|arbeit|lehre|schnupper|bewerb|emploi|career|work')]
""" + t[b:]

t = ers(t, "DANKE = {'de': 'Danke, Ihre Anfrage liegt beim Team des Grand Beau-Rivage. Wir melden uns persönlich bei Ihnen.',",
        "DANKE = {'de': 'Danke, Ihre Anfrage liegt beim Team des Landgasthof Ruedihus. Wir melden uns persönlich bei Ihnen.',")
a = t.index("         'en': 'Thank you, your request is with the team of the Grand"); b = t.index("ANFRAGE_GBR = ")
t = t[:a] + """         'en': 'Thank you, your request is with the team of the Landgasthof Ruedihus. We will get back to you personally.',
         'fr': 'Merci, votre demande est transmise à l’équipe du Landgasthof Ruedihus. Nous reviendrons vers vous personnellement.'}

""" + t[b:]
a = t.index("ANFRAGE_GBR = ")
b = t.index('WISSEN:\n"""', a) + len('WISSEN:\n"""')
t = t[:a] + '''ANFRAGE_GBR = """Du schreibst im Namen des Teams des Landgasthof Ruedihus in Kandersteg (Familie Maeder, ein Haus von 1753, gegenüber dem Waldhotel Doldenhorn) den Entwurf einer Antwort-Mail auf eine Anfrage, die ein Gast im Chat oder über ein Formular der Website gestellt hat (Zimmer, Tisch in der Stube, Fest, Sitzung, Gutschein, Wünsche vor der Anreise oder zur Abreise, Bewerbung).

Regeln:
- Grundlage ist die VORLAGE des Hauses (eine seiner Mails): Übernimm Ton, Wendungen und den Gruss des Hauses («Herzlich, Familie Maeder und ihre Crew»). Die Vorlage ist eine Eingangsbestätigung; du bestätigst nichts, du antwortest auf eine Anfrage.
- Alles, was du an Preisen, Menüs, Stuben, Zimmern, Zeiten und Leistungen nennst, steht wörtlich in WISSEN (Website und Karten des Hauses). Erfinde nichts, rechne keine Gesamtpreise, die nicht eindeutig aus den Angaben folgen.
- Freie Zimmer, Tische und Stuben kannst du nicht prüfen: setz dafür [Verfügbarkeit prüfen] an die Stelle. Was das Haus entscheiden muss, steht in eckigen Klammern, kurz und in normaler Schreibung, zum Beispiel [Tisch bestätigen] oder [Offerte freigeben]. Der Gastgeber zeigt diese Stellen als offene Felder im Brief.
- Was für eine Antwort fehlt (Datum, Personen, Wünsche), erfragst du freundlich am Ende, in einer kurzen Liste.
- Ton des Hauses: herzlich, persönlich und bodenständig, ein Landgasthof mit Stuben und Geschichte, Sie-Form, Schweizer Schreibung (ss statt ß), keine Werbesprache, keine Emojis, kein Fettdruck. Kurze Absätze.
- Greif auf, was der Gast erzählt (Anlass, Wunsch, Begleitung), und nenne, wo es wirklich passt, eine Stube, ein Zimmer oder ein Gericht des Hauses aus WISSEN, das dazu gehört (zum Beispiel Chäs- und Wystube, Jungestube, Liebeslaube, Rösti). Höchstens ein solcher Vorschlag. Hallenbad, Saunen und Massagen liegen im Waldhotel Doldenhorn gegenüber; Hochzeiten, Bankette und Seminare richtet die Familie dort aus.
- Anrede wie in den Mails des Hauses («Liebe Frau …», «Lieber Herr …» bzw. in der Sprache des Gastes), Gruss «Herzlich» bzw. in der Sprache des Gastes.
- Sprache: die Sprache des Gastes (steht bei der Anfrage).
- Form: Zeile 1 «Betreff: …» (persönlich, mit Anlass und Datum), dann Leerzeile, dann die Mail mit Anrede und Gruss, darunter zwei Zeilen: «[Name]» und «<Abteilung> · Landgasthof Ruedihus» (Rezeption, Event-Team oder Personal, je nachdem, an wen die Anfrage ging, in der Sprache des Gastes). Adresse und Telefon stehen schon im Briefkopf, nicht wiederholen.
- Nach der Mail eine Zeile «---» und darunter für das Team, nicht für den Gast: «Grundlage:» mit den Seiten und Karten, aus denen die Angaben stammen, und «Offen:» mit dem, was das Team vor dem Senden klären muss.

WISSEN:
"""''' + t[b:]

# vorlage_text: die passende Mail aus mails/index.html (drei Mails als Blöcke .mb mit Überschrift .mb-art)
a = t.index("def vorlage_text(art, sprache):"); b = t.index("def entwurf(id_, hinweis=''):")
t = t[:a] + '''def vorlage_text(art, sprache):
    nr, absender = VORLAGE.get(art, VORLAGE['zimmer'])
    p = os.path.join(WEB, 'mails', nr, 'index.html')   # die Mail des Hauses (Deutsch), online api/mails/<nr>/index.html (online.json, F76); der Assistent schreibt in der Sprache des Gastes
    try:
        s = open(p, encoding='utf-8').read()
    except OSError:
        return nr, absender, 'de', ''
    s = re.sub(r'<(script|style|head)[^>]*>.*?</\\1>', '', s, flags=re.S | re.I)
    s = re.sub(r'<br\\s*/?>', '\\n', s); s = re.sub(r'</(p|tr|h\\d|div|td|li|dd|dt)>', '\\n', s)
    t = html.unescape(re.sub(r'<[^>]+>', '', s))
    t = re.sub(r'[\u034f\ufeff\u200b]', '', t); t = re.sub(r'[ \\t\u00a0]+', ' ', t); t = re.sub(r'\\n\\s*\\n+', '\\n', t).strip()
    return nr, absender, 'de', t

''' + t[b:]

t = ers(t, "    nr, absender, sp_v, vorlage = vorlage_text(a.get('art'), a.get('sprache', 'de'))\n",
        "    nr, absender, sp_v, vorlage = vorlage_text(a.get('art'), a.get('sprache', 'de'))\n"
        "    absender = a.get('an') if a.get('an') in ABTEILUNG_VON else absender   # Anfrage von der Website: Antwort von der Adresse, an die sie ging (Abteilung)\n")
t = ers(t, "    mail = (f\"Art: {ARTEN.get(a.get('art'), a.get('art'))}\\nName:",
        "    mail = (f\"Art: {ARTEN.get(a.get('art'), a.get('art'))}\\nAbteilung: {a.get('abteilung') or 'Rezeption'}\\nName:")
t = ers(t, "Einmal eine Frage im Chat stellen oder serve.py neu starten.", "Einmal eine Frage im Chat stellen oder server.py neu starten.")
t = ers(t, "        LOKAL.probe = 'probe=1' in (self.headers.get('referer') or self.headers.get('Referer') or '')",
        "        LOKAL.probe = 'probe=1' in (self.headers.get('referer') or self.headers.get('Referer') or '') or self.headers.get('X-Reception-Probe') == '1'")
t = ers(t, "    g._api, g.frage, g.merke, g.handler._ip = api, frage, merke, ip\n",
        '''    roh_erlaubt = g.erlaubt
    PROBEN = {'tag': '', 'n': 0}

    def erlaubt(ip_, art='gast'):
        """Proben des Teams («Chat ausprobieren», Prüfläufe) zählen nicht gegen die Grenzen der Gäste, haben aber eine eigene: 400 am Tag (Carlton 17.10.2026)."""
        if getattr(LOKAL, 'probe', False) and art == 'gast':
            heute = time.strftime('%Y-%m-%d')
            with SCHLOSS:
                if PROBEN['tag'] != heute:
                    PROBEN.update(tag=heute, n=0)
                PROBEN['n'] += 1
                return PROBEN['n'] <= 400
        return roh_erlaubt(ip_, art)

    g._api, g.frage, g.merke, g.handler._ip, g.erlaubt = api, frage, merke, ip, erlaubt
''')
# Beschädigte Datei nie still leer lesen (Master Werkzeug-Bau 5.1, F36): vor jedem Schreiben die letzte gute Fassung als .gut, beim Lesen die .gut nehmen
t = ers(t, """def _lies(p, standard):
    try:
        return json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        return standard
""", """def _lies(p, standard):
    try:
        return json.load(open(p, encoding='utf-8'))
    except OSError:
        return standard
    except ValueError:              # beschädigt: die letzte gute Fassung nehmen
        try:
            return json.load(open(p + '.gut', encoding='utf-8'))
        except (OSError, ValueError):
            return standard
""")
t = ers(t, """    tmp = p + '.neu'
    json.dump(d, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, p)
""", """    tmp = p + '.neu'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    try:
        json.load(open(p, encoding='utf-8')); shutil.copy2(p, p + '.gut')   # nur eine lesbare Fassung wird zur Sicherung
    except (OSError, ValueError):
        pass
    os.replace(tmp, p)
""")
# «Als PDF sichern» setzt der Server (Carlton E16): brief_pdf() vor post()
BRIEF_PDF = '''def brief_pdf(id_, port):
    """Der Brief einer Anfrage als A4-PDF: Chromium setzt brief-pdf.html (brief_pdf.js, Playwright wie in La Carte). Gibt (Bytes, Dateiname) zurück."""
    import subprocess, tempfile
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    a = _lies(_pfad(id_), {}); e = a.get('entwurf') or {}
    if not e.get('text'):
        raise ValueError('BRIEF · Zu dieser Anfrage gibt es noch keinen Brief.')
    daten = {'name': a.get('name') or '', 'kontakt': a.get('kontakt') or '', 'absender': e.get('absender') or 'info@doldenhorn.ch',
             'betreff': e.get('betreff') or '', 'text': e.get('text') or '', 'gestalt': e.get('gestalt') or {}}
    node = shutil.which('node') or next((x for x in ('/opt/homebrew/bin/node', '/usr/local/bin/node') if os.path.exists(x)), None)
    if not node:
        raise ValueError('PDF · node ist nicht installiert (wird für das PDF gebraucht).')
    with tempfile.TemporaryDirectory() as t:
        quelle, ziel = os.path.join(t, 'brief.json'), os.path.join(t, 'brief.pdf')
        with open(quelle, 'w', encoding='utf-8') as f:
            json.dump(daten, f, ensure_ascii=False)
        try:
            r = subprocess.run([node, os.path.join(HIER, 'brief_pdf.js'), str(port), quelle, ziel], capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            raise ValueError('PDF · Das PDF liess sich nicht setzen (Zeitüberschreitung).')
        if r.returncode != 0 or not os.path.exists(ziel):
            raise ValueError('PDF · Das PDF liess sich nicht setzen. Ist Playwright installiert? ' + (r.stderr or '')[-160:])
        roh = open(ziel, 'rb').read()
    wer = re.sub(r'[\\\\/:*?"<>|\\n\\r]+', ' ', a.get('name') or 'Gast').strip()[:60] or 'Gast'
    return roh, f'Landgasthof Ruedihus – {wer} – {datetime.date.today().strftime("%d.%m.%Y")}.pdf'

'''
t = ers(t, '\ndef post(was, d):', '\n' + BRIEF_PDF + '\ndef post(was, d):')

# ---- Zwei Fenster am selben Brief (Carlton E21, F46; im Rivage gewinnt still das spätere Speichern): der Entwurf trägt eine Fassungsnummer;
# wer mit einer veralteten Nummer speichert, bekommt «KONFLIKT · …» und behält seine Eingabe, nichts wird überschrieben (Vorbild Carlton _bau/server_teil.py).
t = ers(t, """        with SCHLOSS:
            a = _lies(_pfad(id_), {})
            if d.get('status') in ('neu', 'gelesen', 'erledigt'):
                a['status'] = d['status']
            if isinstance(d.get('entwurf_text'), str) and a.get('entwurf'):""", """        with SCHLOSS:
            a = _lies(_pfad(id_), {})
            aendert = a.get('entwurf') and (isinstance(d.get('entwurf_text'), str) or isinstance(d.get('gestalt'), dict))
            if aendert and isinstance(d.get('fassung'), int) and d['fassung'] != a['entwurf'].get('fassung', 0):
                raise ValueError('KONFLIKT · Dieser Brief wurde inzwischen in einem anderen Fenster geändert. Ihre Eingabe ist noch hier; bitte kopieren, neu laden und wieder einsetzen.')
            if aendert:
                a['entwurf']['fassung'] = a['entwurf'].get('fassung', 0) + 1
            if d.get('status') in ('neu', 'gelesen', 'erledigt'):
                a['status'] = d['status']
            if isinstance(d.get('entwurf_text'), str) and a.get('entwurf'):""")
t = ers(t, """            _schreib(_pfad(id_), a)
        return {'ok': True, **ueberblick()}
    if was == 'formular':""", """            _schreib(_pfad(id_), a)
        return {'ok': True, 'fassung': (a.get('entwurf') or {}).get('fassung', 0), **ueberblick()}
    if was == 'formular':""")
# Neu geschriebener Brief zählt die Fassung weiter (sonst träfe ein altes Fenster mit Fassung 0 auf einen neuen Brief mit 0 und überschriebe ihn still)
t = ers(t, "        a = _lies(_pfad(id_), a)\n        a['entwurf'] = entwurf_neu\n",
        "        a = _lies(_pfad(id_), a)\n        entwurf_neu['fassung'] = ((a.get('entwurf') or {}).get('fassung', 0) or 0) + 1\n        a['entwurf'] = entwurf_neu\n")

# ---- Formulare der Website (E12, Rivage `formular`, erweitert): Abteilung, Seite und Formular; Kontakt geprüft; Probe gekennzeichnet; Dank in der Sprache
a = t.index("    if was == 'formular':"); b = t.index("    if was == 'weg':")
t = t[:a] + '''    if was == 'formular':           # Formular der Website (baustein/anfrage.js): landet im Eingang, nicht in einem Mailfach (Rivage E12, Ruedihus 17.10.2026)
        if d.get('website'):        # Feld, das Menschen nicht sehen: nur Maschinen füllen es aus
            return {'ok': True}
        name, kontakt = str(d.get('name') or '').strip()[:120], str(d.get('kontakt') or '').strip()[:160]
        if not kontakt:
            raise ValueError('FORMULAR · Bitte E-Mail oder Telefon angeben, damit das Haus antworten kann.')
        if not re.fullmatch(r'[^\\s@<>"]+@[^\\s@<>"]+\\.[^\\s@<>"]{2,}|\\+?[\\d\\s/().-]{7,24}', kontakt):
            raise ValueError('FORMULAR · Bitte eine gültige E-Mail-Adresse oder Telefonnummer angeben.')
        art = d.get('art') if d.get('art') in ARTEN else 'nachricht'
        sp = d.get('sprache') if d.get('sprache') in SPRACHEN else 'de'
        try:
            pers = max(1, min(60, int(d.get('personen'))))
        except (TypeError, ValueError):
            pers = None
        anliegen = str(d.get('anliegen') or '').strip()[:300]
        nachricht = str(d.get('nachricht') or '').strip()[:6000]   # Angaben des Formulars + Nachricht des Gastes (bis 1'200) + Wünsche ohne Grenze: 1'200 schnitt still ab (Prüfung 17.10.2026); die Anfrage selbst bleibt unter 12 kB
        an = d.get('an') if d.get('an') in ABTEILUNG_VON else VORLAGE.get(art, VORLAGE['nachricht'])[1]
        seite = str(d.get('seite') or '')[:160]
        seite = re.sub(r'[^\\w./?#=&%-]', '', seite) if seite.startswith('/') else ''   # Weg der Seite (mit ? und #), nur harmlose Zeichen
        seite_name = re.sub(r'[<>]', '', str(d.get('seite_name') or ''))[:80]
        formular = d.get('formular') if d.get('formular') in FORMULARE else 'allgemein'
        text = nachricht or anliegen
        id_ = lege_anfrage({'art': art, 'name': name, 'kontakt': kontakt, 'datum': str(d.get('datum') or '')[:120], 'personen': pers, 'anliegen': anliegen or text[:200]},
                           'formular-' + hashlib.sha1(f'{time.time()}{random.random()}'.encode()).hexdigest()[:12], sp,
                           [{'rolle': 'user', 'text': f'Über ein Formular der Website (Seite {seite_name or seite or "unbekannt"}): ' + text}])
        with SCHLOSS:
            x = _lies(_pfad(id_), {})
            x.update({'web': True, 'an': an, 'abteilung': ABTEILUNG_VON[an], 'seite': seite, 'seite_name': seite_name, 'formular': formular, 'nachricht': nachricht})
            if d.get('probe') is True:
                x['probe'] = True
            _schreib(_pfad(id_), x)
        return {'ok': True, 'danke': DANKE.get(sp, DANKE['de'])}
''' + t[b:]

# Beispiele des Ruedihus kommen auch aus den Formularen der Website: Abteilung, Adresse und Seite mitnehmen, Absender = Adresse der Abteilung
t = ers(t, "            nr, absender = VORLAGE.get(b['art'], VORLAGE['zimmer'])\n", "            nr, absender = VORLAGE.get(b['art'], VORLAGE['zimmer'])\n            absender = b.get('an') or absender\n")
t = ers(t, "'status': b['status'], 'beispiel': True,", "'status': b['status'], 'beispiel': True, **{k: b[k] for k in ('an', 'abteilung', 'seite', 'seite_name', 'web', 'nachricht', 'formular') if b.get(k)},")
# «Zurück auf die Vorlage» braucht die Fassung des Assistenten: beim ersten Ändern des Texts merkt sich der Entwurf sie als «original» (Prüfung 17.10.2026)
t = ers(t, "                a['entwurf']['text'] = d['entwurf_text'][:12000]\n", "                if 'original' not in a['entwurf']:\n                    a['entwurf']['original'] = {'text': a['entwurf'].get('text') or '', 'betreff': a['entwurf'].get('betreff') or ''}\n                a['entwurf']['text'] = d['entwurf_text'][:12000]\n")
# Löschen auf Wunsch des Gastes nimmt auch die Sicherung mit (Prüfung 17.10.2026: nach «Löschen» lag die Anfrage samt Name und Kontakt noch als .gut im Datenordner)
t = ers(t, "            os.remove(_pfad(id_))\n", "            os.remove(_pfad(id_))\n            for rest in ('.gut', '.neu'):\n                try:\n                    os.remove(_pfad(id_) + rest)\n                except OSError:\n                    pass\n")
open(os.path.join(C, 'reception.py'), 'w', encoding='utf-8').write(t)

# ------------------------------------------------------------------ gedaechtnis.py
g = lade('gedaechtnis.py')
g = ers(g, 'Das weiss der Chat · La Réception, Grand Beau-Rivage', 'Das weiss der Chat · La Réception (Der Gastgeber), Landgasthof Ruedihus')
g = ers(g, "HIER = os.path.dirname(os.path.abspath(__file__))\nDATEN = os.path.join(os.environ.get('REZEPTION_DATEN') or os.path.join(HIER, 'daten'), 'gedaechtnis')",
        "HIER = os.path.dirname(os.path.abspath(__file__))\nWEB = os.path.dirname(os.path.dirname(HIER))   # der Ordner des Ruedihus\n"
        "WISSEN_DIR = os.path.join(HIER, 'gast')    # gast_wissen.txt und gast_tal.txt wie online in api/ (_bau/gast_bau.py)\n"
        "DATEN = os.path.join(os.environ.get('RECEPTION_DATEN') or os.environ.get('REZEPTION_DATEN') or os.path.join(HIER, 'daten'), 'gedaechtnis')")
g = ers(g, "os.path.join(HIER, n)) if os.path.exists(os.path.join(HIER, n)) else 0)", "os.path.join(WISSEN_DIR, n)) if os.path.exists(os.path.join(WISSEN_DIR, n)) else 0)")
g = ers(g, "        p = os.path.join(HIER, datei)\n", "        p = os.path.join(WISSEN_DIR, datei)\n", 2)
g = ers(g, "    web = os.path.dirname(HIER)\n", "    web = WEB\n")
g = ers(g, "gast_wissen.txt (Seiten der Website + Unterlagen des Hauses) und gast_tal.txt (Bergbahnen, Interlaken Tourismus)",
        "gast_wissen.txt (Seiten der Website + Unterlagen des Hauses, _bau/gast_bau.py) und gast_tal.txt (Bergbahnen und BLS rund um Kandersteg)")
g = ers(g, "Du hilfst dem Team des Grand Beau-Rivage in Interlaken", "Du hilfst dem Team des Landgasthof Ruedihus in Kandersteg")
a = g.index("BEREICHE = ["); b = g.index("PREISZEILE = ")
g = g[:a] + r'''BEREICHE = ['Das Haus', 'Zimmer', 'Essen & Stuben', 'Feste im Haus', 'Durchs Jahr', 'Geschichte', 'Anreise & Abreise', 'Kandersteg & Ausflüge',
            'Veranstaltungen', 'Fragen & Antworten']
# Seite der Website bzw. Unterlage → Bereich (Kopfzeile im Wissen: «=== Seite: … (Entwurf: x.html) ===» bzw. «=== Unterlage des Hauses: name (PDF auf der Website) ===»)
SEITE_BEREICH = [(r'Entwurf: (zimmer[\w-]*|zu-zweit)\.html', 'Zimmer'), (r'Entwurf: mappe\.html', 'Fragen & Antworten'),
                 (r'Entwurf: essen\.html', 'Essen & Stuben'), (r'Entwurf: veranstaltungen\.html', 'Durchs Jahr'), (r'Entwurf: geschichte\.html', 'Geschichte'),
                 (r'Entwurf: (anreise|abreise)\.html', 'Anreise & Abreise'), (r'Entwurf: (index|haus|rechtliches)\.html', 'Das Haus'),
                 (r'Unterlage des Hauses: [\w.-]*menuvorschlaege', 'Feste im Haus'),
                 (r'Unterlage des Hauses: [\w.-]*(Stettlerstube|stettlerstube|Wystube|wystube|Tagesteller|tagesteller)', 'Essen & Stuben'),
                 (r'^Talwissen', 'Kandersteg & Ausflüge')]
UNTERLAGE_NAME = {'Egger-und-Stettlerstube-Landgasthof-1.3.2026': 'Schpis Charte, Egger- und Stettlerstube, ab 1.3.2026', 'RH-Chaes-und-Wystube-ab-1.3.2026': 'Schpiszettel, Chäs- und Wystube, ab 1.3.2026',
                  'Tagesteller-ab-01.03.2026': 'Tagesteller, ab 1.3.2026', 'landgasthof-ruedihus-chaes-und-wystube': 'Karte der Chäs- und Wystube',
                  'landgasthof-ruedihus-egger-und-stettlerstube': 'Karte der Egger- und Stettlerstube', 'landgasthof-ruedihus-menuvorschlaege-2023': 'Menuvorschläge 2023',
                  'landgasthof-ruedihus-tagesteller': 'Karte der Tagesteller'}
''' + g[b:]
g = ers(g, "r'Unterlage des Hauses: (.+?) \\(PDF\\)'", "r'Unterlage des Hauses: (.+?) \\(PDF'")
g = ers(g, "re.search(r'\\(Entwurf: ([^)]+)\\)', kopf).group(1) if '(Entwurf:' in kopf else ''", "(re.search(r'Entwurf: ([\\w.-]+)', kopf) or [None, ''])[1]")
g = ers(g, """def _lies(n, standard):
    try:
        return json.load(open(_pfad(n), encoding='utf-8'))
    except (OSError, ValueError):
        return standard
""", """def _lies(n, standard):
    try:
        return json.load(open(_pfad(n), encoding='utf-8'))
    except OSError:
        return standard
    except ValueError:              # beschädigt: letzte gute Fassung, sonst laut melden statt still leer (das nächste Schreiben würde alles löschen)
        try:
            return json.load(open(_pfad(n) + '.gut', encoding='utf-8'))
        except (OSError, ValueError):
            raise ValueError(f'DATEI · Die Ablage «{n}» ist beschädigt und hat keine gute Sicherung. Bitte die Prüfung öffnen.')
""")
g = ers(g, """    tmp = _pfad(n) + '.neu'
    json.dump(d, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, _pfad(n))
""", """    tmp = _pfad(n) + '.neu'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    try:
        json.load(open(_pfad(n), encoding='utf-8')); shutil.copy2(_pfad(n), _pfad(n) + '.gut')
    except (OSError, ValueError):
        pass
    os.replace(tmp, _pfad(n))
""")
g = ers(g, "import base64, datetime, hashlib, html, ipaddress, json, os, re, socket, threading,", "import base64, datetime, hashlib, html, ipaddress, json, os, re, shutil, socket, threading,")
open(os.path.join(C, 'gedaechtnis.py'), 'w', encoding='utf-8').write(g)
print('Server-Teil kopiert (Ruedihus)')
