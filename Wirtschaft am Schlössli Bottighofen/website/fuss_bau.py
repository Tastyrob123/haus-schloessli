# Der Fuss aller Seiten, Fassung 5 «Hell am Mittag» (Robert 19.10.2026, aus _varianten/fuss4.html).
# Terrasse mit Zeiten, alle Bereiche mit Bildern, Auszeichnungen als grosse Zahlen, die zwei Häuser der Familie Kuchler auf einer Grundlinie.
# Gestaltung: assets/css/fuss.css · Bewegung: assets/js/fuss.js · Fakten Schlössli: inhalt/haus.json
# Fakten Schäfli: ~/Desktop/Website-Projekte/Taverne zum Schäfli Wigoltingen/website/inhalt/haus.py (Adresse, Tage, Auszeichnungen, Zenchef)

SCH = {'name': 'Taverne zum Schäfli', 'strasse': 'Oberdorfstrasse 8', 'plz': '8556 Wigoltingen', 'tage': 'Mittwoch bis Samstag',
       'kurz': 'Zwei Michelin-Sterne · 18 Punkte GaultMillau',
       'zeiten': '11:30 bis 14:30 und 18:00 bis 23:00 Uhr', 'tel': '+41 52 763 11 72', 'tel_h': '+41527631172',
       'url': 'http://127.0.0.1:8953/',                      # Designstudie des Schäfli (lokal); offizielle Seite: haus.json › schwester.url
       'res': 'https://bookings.zenchef.com/results?rid=378685&pid=1001'}
PF = '<svg class="pfl" viewBox="0 0 16 10" aria-hidden="true"><path d="M0 5h14M10 1l4 4-4 4"/></svg>'


def fuss(H, RES, knopf, e):
    z = H['zeiten']
    tage = z['tage'].replace(' - ', ' bis ')
    offen = z['offen'].replace(' Uhr', '').replace(' - ', ' bis ')
    k1, k2 = (k.replace(' Uhr', '').replace(' - ', ' bis ') for k in z['kueche'])
    res = ' data-fenster="fe-reservation"'
    nav = [
        ('Essen & Trinken', 'tortelloni-800', [('karte.html', 'Speisekarte'), ('karte.html#mittag', 'Lunch-Menü'), ('karte.html#laestermeile', 'Lästermeile'), ('weinkarte.html', 'Weinkarte')]),
        ('Feiern & Anlässe', 'gaststube-800', [('feiern.html', 'Banketts & Gruppen'), ('feiern.html#etagen', 'Zwei Etagen'), ('feiern.html#menues', 'Bankettmenüs'), ('anlaesse.html', 'Events & Termine'), ('gutschein.html', 'Gutschein')]),
        ('Das Haus', 'haus-800', [('index.html#willkommen', 'Am Hafen'), ('index.html#kueche', 'Die Küche'), ('index.html#keller', 'Der Weinkeller'), ('index.html#besen', 'Geschichte'), ('team.html', 'Das Team')]),
        ('Ihr Besuch', 'bootshafen-800', [('abend.html', 'Ihr Abend'), ('kontakt.html', 'Kontakt & Anfahrt'), ('kontakt.html', 'Öffnungszeiten'), (H['instagram'], 'Instagram')]),
    ]
    ausz = [('GaultMillau', '15', 'Punkte', 'Guide 2027'), ('GaultMillau', '2026', 'Entdeckung des Jahres', 'Monika Huber'),
            ('Falstaff', '91', 'von 100 Punkten', ''), ('Guide Michelin', 'Favorit', 'der Inspektoren', 'empfohlen, Selektion 2025')]
    # haus.json › auszeichnungen (Quelle: _kette/03-sammler/fakten.json)

    def a(h, t):
        x = ' target="_blank" rel="noopener"' if h.startswith('http') else ''
        return f'<a href="{e(h)}"{x}>{e(t)}</a>'

    spalten = ''.join(
        f'<div data-a="auf" style="--i:{i}"><span class="fz__nb" data-a="zoom"><img src="assets/img/{b}.webp" alt="" loading="lazy" decoding="async"></span>'
        f'<h3>{e(k)}</h3><ul>' + ''.join(f'<li>{a(h, t)}</li>' for h, t in ls) + '</ul></div>' for i, (k, b, ls) in enumerate(nav))
    zahlen = ''.join(
        f'<div data-a="auf" style="--i:{i}"><span class="fz__aw">{e(w)}</span><b>{e(zz)}</b><span class="fz__ae">{e(ei)}</span><small>{e(zu)}</small></div>'
        for i, (w, zz, ei, zu) in enumerate(ausz))
    recht = ''.join(a(h, t) for h, t in [('impressum.html', 'Impressum'), ('datenschutz.html', 'Datenschutz'), ('agb.html', 'AGB')])

    return f'''<footer class="fz">
  <div class="fz__kopf">
    <div class="fz__bild" data-a="zoom"><img src="assets/img/start-1800.webp" srcset="assets/img/start-1200.webp 1200w, assets/img/start-1800.webp 1800w, assets/img/start-2400.webp 2400w" sizes="(max-width:900px) 100vw, 55vw" alt="Blaue Stühle auf der Terrasse am Mittag, dahinter der Bodensee und die Alpen" loading="lazy" decoding="async"></div>
    <div class="fz__kt">
      <img class="fz__lg" src="assets/img/logo-520.webp" width="520" height="603" alt="Schlössli Wirtschaft by Christian Kuchler" loading="lazy" data-a="feder">
      <p class="fz__claim slit"><span class="sz"><span class="si" style="--i:0">Willkommen</span></span><span class="sz"><span class="si" style="--i:1">am Hafen.</span></span></p>
      <p class="fz__lauf" data-a="auf">{e(H['satz_lage'])}</p>
      <dl class="fz__zt" data-a="auf"><div><dt>{e(tage)}</dt><dd>{e(offen)} Uhr</dd></div><div><dt>Küche</dt><dd>{e(k1)} · {e(k2)} Uhr</dd></div><div><dt>Lästermeile</dt><dd>den ganzen Tag</dd></div><div><dt>Ruhetag</dt><dd>Dienstag und Mittwoch</dd></div></dl>
      <p class="fz__kz" data-a="auf">{e(H['strasse'])}, {e(H['ort'])}<br><a href="tel:{H['telefon_href']}">{e(H['telefon'])}</a> · <span>{e(H['mail'])}</span></p>
      <div data-a="auf">{knopf('Tisch reservieren', RES, dunkel=True, attr=res)}</div>
    </div>
  </div>
  <div class="innen">
    <nav class="fz__nav" aria-label="Alle Bereiche">{spalten}</nav>
    <div class="fz__az">{zahlen}</div>
    <div class="fz__fam">
      <div class="fz__fk"><i data-a="linie"></i><p data-a="auf">Zwei Häuser der Familie Kuchler</p><i data-a="linie"></i></div>
      <div class="fz__zwei">
        <span class="fz__fb a" data-a="zoom"><img src="assets/img/haus-1800.webp" srcset="assets/img/haus-1200.webp 1200w, assets/img/haus-1800.webp 1800w" sizes="(max-width:900px) 50vw, 700px" alt="Die Wirtschaft am Schlössli im ehemaligen Hafenmeistergebäude" loading="lazy" decoding="async"></span>
        <a class="fz__fb b" data-a="zoom" href="{SCH['url']}" target="_blank" rel="noopener"><img src="assets/img/schaefli-strasse-1600.webp" srcset="assets/img/schaefli-strasse-800.webp 800w, assets/img/schaefli-strasse-1600.webp 1600w" sizes="(max-width:900px) 50vw, 700px" alt="Die Taverne zum Schäfli an der Oberdorfstrasse in Wigoltingen" loading="lazy" decoding="async"></a>
        <i class="fz__boden" data-a="linie"></i>
        <span class="fz__ck" data-a="feder">{e(H['by'][3:])}</span>
      </div>
      <div class="fz__hg">
        <div class="fz__h a" data-a="auf">
          <div class="fz__hkopf"><span class="fz__hier">Sie sind hier</span><span class="fz__ho">Bottighofen · am See</span></div>
          <p class="fz__hn">Wirtschaft am Schlössli</p>
          <p class="fz__hl">Mediterrane Küche von Monika Huber, direkt im Hafen.</p>
          <dl class="fz__hd"><div><dt>Adresse</dt><dd>{e(H['strasse'])}, {e(H['ort'])}</dd></div><div><dt>Offen</dt><dd>{e(tage)}, {e(offen)} Uhr</dd></div><div><dt>Telefon</dt><dd><a href="tel:{H['telefon_href']}">{e(H['telefon'])}</a></dd></div><div><dt>GaultMillau</dt><dd>15 Punkte</dd></div></dl>
          <div class="fz__hk">{knopf('Tisch am See', RES, dunkel=True, klein=True, attr=res)}<a class="fz__zu" href="kontakt.html">Anfahrt {PF}</a></div>
        </div>
        <div class="fz__h b" data-a="auf" style="--i:1">
          <div class="fz__hkopf"><span class="fz__hier b">Die Schwester</span><span class="fz__ho">Wigoltingen · im Dorf</span></div>
          <p class="fz__hn">{e(SCH['name'])}</p>
          <p class="fz__hl">Küche von Christian Kuchler im Riegelhaus an der Oberdorfstrasse.</p>
          <dl class="fz__hd"><div><dt>Adresse</dt><dd>{e(SCH['strasse'])}, {e(SCH['plz'])}</dd></div><div><dt>Offen</dt><dd>{e(SCH['tage'])}, {e(SCH['zeiten'])}</dd></div><div><dt>Telefon</dt><dd><a href="tel:{SCH['tel_h']}">{e(SCH['tel'])}</a></dd></div><div><dt>Guide Michelin</dt><dd>Zwei Sterne · 18 Punkte GaultMillau</dd></div></dl>
          <div class="fz__hk"><a class="knopf knopf--dunkel knopf--klein k-sch" href="{SCH['res']}" target="_blank" rel="noopener">Tisch im Schäfli <span class="kn"><svg class="pf" viewBox="0 0 16 10" aria-hidden="true"><path d="M0 5h14M10 1l4 4-4 4"/></svg></span></a><a class="fz__zu b" href="{SCH['url']}" target="_blank" rel="noopener">Zum Haus {PF}</a></div>
        </div>
      </div>
    </div>
  </div>
  <div class="fz__un"><div class="innen"><div class="fz__ug"><img class="fz__ul" src="assets/img/logo-520.webp" alt="" loading="lazy">
    <span>© {e(H['name'])} · {e(H['by'])} · {e(H['strasse'])}, {e(H['ort'])}</span><nav>{recht}</nav>
    <span class="fz__st">Designstudie von Tasty Studios, nicht die offizielle Website</span>
    <a class="fz__hoch" href="#" aria-label="Nach oben"><svg viewBox="0 0 10 16" aria-hidden="true"><path d="M5 15V1M1 5l4-4 4 4"/></svg></a></div></div></div>
</footer>
'''
