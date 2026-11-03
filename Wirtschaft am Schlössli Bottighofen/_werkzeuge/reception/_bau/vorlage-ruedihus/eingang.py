#!/usr/bin/env python3
"""Achter Schritt (nach abnahme.py): der Eingang nach Abteilung, wie ihn das Doldenhorn aus seinem Studio-Eingang in La Réception gebracht hat
(Master Werkzeug-Bau E15/E22, Doldenhorn _bau/eingang.py, nur gelesen), im Ruedihus für die Formulare der Website:
  Abteilung je Anfrage (Rezeption, Event, Personal) aus der Adresse, an die das Formular ging, Zahl offener je Abteilung als Auswahl,
  Auswahl «Neu» neben Alle / Offen / Erledigt, Herkunft (Chat oder Formular der Website mit Seite), Probe-Einträge gekennzeichnet, Nachricht der Website.
Die Daten bringt der Weg «formular» (server_teil.py). Jede Ersetzung muss genau einmal treffen, sonst bricht das Skript ab.
Aufruf: python3 _werkzeuge/reception/_bau/eingang.py"""
import os, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(C, 'reception.js')
t = open(p, encoding='utf-8').read()


def ers(alt, neu, n=1):
    global t
    if t.count(alt) != n:
        sys.exit(f'ABBRUCH: «{alt[:80]}» kommt {t.count(alt)}× vor, erwartet {n}×')
    t = t.replace(alt, neu)


ers("const S = { ue: null, ansicht: 'start', anfragen: null, fragen: null, nachgetragen: null, wahl: '', filter: 'alle',",
    "const S = { ue: null, ansicht: 'start', anfragen: null, fragen: null, nachgetragen: null, wahl: '', filter: 'alle', abt: 'alle',")
ers("const SPRACHE = { de: 'Deutsch', en: 'Englisch', fr: 'Französisch', zh: 'Chinesisch', ko: 'Koreanisch', ar: 'Arabisch' };",
    "const SPRACHE = { de: 'Deutsch', en: 'Englisch', fr: 'Französisch', it: 'Italienisch', zh: 'Chinesisch', ko: 'Koreanisch', ar: 'Arabisch' };\n"
    "/* Abteilungen des Ruedihus (Adressen der Seiten: info@, event@ im Fest-Rechner, jobs@ bei den Stellen): an wen eine Anfrage ging; aus dem Chat nach der Art */\n"
    "const ABTEILUNGEN = [['Rezeption', 'Zimmer, Tisch, Gutschein, Anreise, Abreise'], ['Event', 'Feste und Sitzungen in den Stuben'], ['Personal', 'Bewerbungen']];\n"
    "const FORMULAR = { tisch: 'Tisch in der Stube', fest: 'Fest-Rechner', anreise: 'Vor Ihrer Anreise', abreise: 'Ihre Abreise', gutschein: 'Gutschein anfragen', stelle: 'Bewerbung', allgemein: 'Anfrage-Fenster' };\n"
    "const abt = a => a.abteilung || ({ feier: 'Event', tagung: 'Event' }[a.art] || 'Rezeption');")
# Karte: Abteilung, Herkunft, Probe
ers("<span class=\"re-a__k\">${esc(ART[a.art] || a.art)} · ${esc(uhr(a.zeit).replace(' Uhr', ''))}${a.beispiel ? ' · Beispiel' : ''}</span>",
    "<span class=\"re-a__k\">${esc(ART[a.art] || a.art)}${abt(a) !== ART[a.art] ? ' · ' + esc(abt(a)) : ''} · ${esc(uhr(a.zeit).replace(' Uhr', ''))}${a.web ? ' · Website' : ''}${a.beispiel ? ' · Beispiel' : a.probe ? ' · Probe' : ''}</span>")
# Liste: Auswahl nach Stand (mit «Neu») und nach Abteilung
ers("  const alle = S.anfragen, f = S.filter;\n  const l = f === 'offen' ? alle.filter(a => a.status !== 'erledigt') : f === 'erledigt' ? alle.filter(a => a.status === 'erledigt') : alle;",
    "  const jede = S.anfragen, f = S.filter, alle = S.abt === 'alle' ? jede : jede.filter(a => abt(a) === S.abt);\n"
    "  const l = f === 'neu' ? alle.filter(a => a.status === 'neu') : f === 'offen' ? alle.filter(a => a.status !== 'erledigt') : f === 'erledigt' ? alle.filter(a => a.status === 'erledigt') : alle;")
ers("  if ((!S.wahl || !alle.some(a => a.id === S.wahl)) && alle.length) S.wahl = (l.find(a => a.status === 'neu') || l[0] || alle[0]).id;\n  const a = alle.find(x => x.id === S.wahl);",
    "  if ((!S.wahl || !l.some(a => a.id === S.wahl)) && l.length) S.wahl = (l.find(a => a.status === 'neu') || l[0]).id;\n  const a = alle.find(x => x.id === S.wahl);")
ers("  const zahl = k => k === 'offen' ? alle.filter(a => a.status !== 'erledigt').length : k === 'erledigt' ? alle.filter(a => a.status === 'erledigt').length : alle.length;",
    "  const zahl = k => k === 'neu' ? alle.filter(a => a.status === 'neu').length : k === 'offen' ? alle.filter(a => a.status !== 'erledigt').length : k === 'erledigt' ? alle.filter(a => a.status === 'erledigt').length : alle.length;\n"
    "  const offenIn = n => jede.filter(a => a.status !== 'erledigt' && (n === 'alle' || abt(a) === n)).length;")
ers("  return kopf('Eingang', 'Anfragen <em>aus dem Chat.</em>',\n    'Zimmer, Tische, Feiern und Tagungen, die Gäste im Chat angefragt haben. Zu jeder Anfrage schreibt der Assistent einen Brief im Ton des Hauses, auf Grundlage Ihrer Mail-Vorlagen. Sie lesen, ändern und schicken selbst.'",
    "  return kopf('Eingang', 'Anfragen <em>aus Chat und Website.</em>',\n    'Zimmer, Tische in der Stube, Feste, Gutscheine, Wünsche vor der Anreise und zur Abreise, die Gäste im Chat oder in einem Formular der Website geschickt haben, nach Abteilung. Zu jeder Anfrage schreibt der Assistent einen Brief im Ton des Hauses, auf Grundlage Ihrer Mail-Vorlagen. Sie lesen, ändern und schicken selbst.'")
ers("    (alle.length ? `<div class=\"re-eingang\"><div class=\"re-spalte\">\n        <div class=\"wahl2 re-filter\" role=\"group\" aria-label=\"Auswahl\">${[['alle', 'Alle'], ['offen', 'Offen'], ['erledigt', 'Erledigt']].map(",
    "    (jede.length ? `<div class=\"re-eingang\"><div class=\"re-spalte\">\n"
    "        <div class=\"re-abt\" role=\"group\" aria-label=\"Abteilung\">${[['alle', 'Alle', 'Jede Abteilung']].concat(ABTEILUNGEN.map(([k, s]) => [k, k, s])).map(([k, n, s]) => `<button type=\"button\" data-abt=\"${k}\" aria-pressed=\"${S.abt === k}\" title=\"${esc(s)}\"><span>${esc(n)}</span><i${offenIn(k) ? ' class=\"da\"' : ''}>${offenIn(k)}</i></button>`).join('')}</div>\n"
    "        <div class=\"wahl2 re-filter\" role=\"group\" aria-label=\"Auswahl\">${[['alle', 'Alle'], ['neu', 'Neu'], ['offen', 'Offen'], ['erledigt', 'Erledigt']].map(")
ers("      : `<div class=\"re-leer platte\">${ZEICHEN}<b>Der Eingang ist leer.</b><p>Sobald ein Gast im Chat etwas anfragt und Name und Kontakt nennt, steht die Anfrage hier.</p></div>`);",
    "      : `<div class=\"re-leer platte\">${ZEICHEN}<b>Der Eingang ist leer.</b><p>Sobald ein Gast im Chat etwas anfragt und Name und Kontakt nennt, oder ein Formular der Website abschickt, steht die Anfrage hier.</p></div>`);")
# Detail: Abteilung, Herkunft, Nachricht der Website
ers("  const angaben = [['Datum', esc(a.datum || 'nicht genannt')], ['Personen', esc(a.personen || 'nicht genannt')], ['Sprache', esc(SPRACHE[a.sprache] || a.sprache)], ['Kontakt', kontaktLink(a.kontakt)]];",
    "  const angaben = [['Datum', esc(a.datum || 'nicht genannt')], ['Personen', esc(a.personen || 'nicht genannt')], ['Sprache', esc(SPRACHE[a.sprache] || a.sprache)], ['Kontakt', kontaktLink(a.kontakt)],\n"
        "    ['An', esc(abt(a)) + (a.an ? ` <small>${esc(a.an)}</small>` : '')], ['Über', a.web ? 'Website, ' + esc(FORMULAR[a.formular] || 'Formular') + (a.seite_name ? `, Seite ${esc(a.seite_name)}` : '') : 'Chat der Website']];")
ers("<span class=\"re-d__k\">${esc(ART_LANG[a.art] || a.art)} · ${esc(zeit(a.zeit))}${a.beispiel ? ' · Beispiel' : ''}</span>",
    "<span class=\"re-d__k\">${esc(ART_LANG[a.art] || a.art)}${abt(a) !== ART[a.art] ? ' · ' + esc(abt(a)) : ''} · ${esc(zeit(a.zeit))}${a.beispiel ? ' · Beispiel' : a.probe ? ' · Probe' : ''}</span>")
ers("<summary><span>Das Gespräch im Chat</span>", "<summary><span>${a.web ? 'Die Nachricht über die Website' : 'Das Gespräch im Chat'}</span>")
ers("${(a.verlauf || []).map(v => `<p class=\"${v.rolle === 'user' ? 'gast' : 'haus'}\" dir=\"auto\"><small>${v.rolle === 'user' ? 'Gast' : 'Rezeption im Chat'}</small>${esc(v.text)}</p>`).join('')}",
    "${(a.verlauf || []).map(v => `<p class=\"${v.rolle === 'user' ? 'gast' : 'haus'}\" dir=\"auto\"><small>${v.rolle === 'user' ? 'Gast' : 'Rezeption im Chat'}</small>${esc(v.text).replace(/\\n/g, '<br>')}</p>`).join('')}")
ers("  $$('.re-filter [data-filter]').forEach(b => b.onclick = () => { S.filter = b.dataset.filter; zeichne(); });",
    "  $$('.re-filter [data-filter]').forEach(b => b.onclick = () => { S.filter = b.dataset.filter; zeichne(); });\n"
    "  $$('.re-abt [data-abt]').forEach(b => b.onclick = () => { S.abt = b.dataset.abt; try { sessionStorage.setItem('re-rh-abt', S.abt); } catch (e) { /* */ } zeichne(); });")
# Abteilung und Auswahl bleiben beim Neuladen (wie die Ansicht, R15)
ers("const S = { ue: null,", "const S0 = (() => { try { return sessionStorage.getItem('re-rh-abt') || 'alle'; } catch (e) { return 'alle'; } })();\nconst S = { ue: null,")
ers("wahl: '', filter: 'alle', abt: 'alle',", "wahl: '', filter: 'alle', abt: S0,")
# R20 ohne Erfundenes (Master E10): leere Liste «Vom Team nachgetragen» zeigt auf Wunsch, wie eine Karte aussieht, ohne zu behaupten, das Team habe etwas
# nachgetragen. Die Frage ist eine echte Lücke des Chats (Hund steht nirgends auf den Seiten), die Antwort ist nur ein Platzhalter.
ers("      : `<div class=\"re-leer platte\">${ZEICHEN}<b>Noch nichts nachgetragen.</b><p>Hatte der Chat auf eine Frage keine Antwort, steht sie unter «Das wurde gefragt» mit dem Knopf «Antwort nachtragen».</p></div>`);",
    "      : `<div class=\"re-leer platte\">${ZEICHEN}<b>Noch nichts nachgetragen.</b><p>Hatte der Chat auf eine Frage keine Antwort, steht sie unter «Das wurde gefragt» mit dem Knopf «Antwort nachtragen».</p><button class=\"kn kn--linie\" type=\"button\" id=\"n-beispiel\">Beispiel ansehen<i>${PF}</i></button></div>`);")
ers("function verbindeNachgetragen() {\n  $('#n-neu').onclick = () => nachtragenFenster({ frage: '', antwort: '' });",
    "function verbindeNachgetragen() {\n  $('#n-neu').onclick = () => nachtragenFenster({ frage: '', antwort: '' });\n"
    "  if ($('#n-beispiel')) $('#n-beispiel').onclick = () => fenster(`<span class=\"mono\">Beispiel · so sähe ein Nachtrag aus</span><h2>Eine <em>Karteikarte.</em></h2>\n"
    "    <article class=\"re-n re-n--beispiel\"><header class=\"re-n__kopf\"><span>Nachgetragen am …</span><em>Beispiel</em></header><span class=\"re-n__l\">Frage der Gäste</span><h3 class=\"re-n__q\">Ab wann kann ich am Anreisetag ins Zimmer?</h3>\n"
    "    <div class=\"re-n__zier\" aria-hidden=\"true\"><i></i>${ZEICHEN}<i></i></div><span class=\"re-n__l\">Antwort des Hauses</span><p class=\"re-n__a\">[Hier steht die Antwort Ihres Teams, so wie Sie sie einem Gast am Telefon sagen würden.]</p></article>\n"
    "    <p class=\"leise\">So eine Frage stellen Gäste, und die Seiten des Hauses sagen dazu nichts (eine Zeit zum Einchecken steht nirgends). Tragen Sie eine Antwort ein, steht sie hier als Karte, und der Chat antwortet ab der nächsten Frage damit. Erfunden ist hier nur die Leerstelle, nicht die Antwort.</p>\n"
    "    <div class=\"fenster__kn\"><button class=\"link\" type=\"button\" data-zu>Schliessen</button><button class=\"kn kn--gold\" type=\"button\" id=\"f-los\">Jetzt eine Antwort anlegen<i>${PF}</i></button></div>`, false, () => { fensterZu(); nachtragenFenster({ frage: 'Ab wann kann ich am Anreisetag ins Zimmer?', antwort: '' }); });")
# Übersicht: Anfragen kommen aus Chat UND Anfrage-Fenster der Website
ers("'Hier sehen Sie, was Gäste die Rezeption im Chat fragen. Möchte jemand ein Zimmer, einen Tisch, eine Feier oder eine Tagung, liegt die Anfrage im Eingang, mit einem Brief als Entwurf für Ihre Antwort. Verschickt wird nur, was Sie selbst schicken.'",
    "'Hier sehen Sie, was Gäste die Rezeption im Chat fragen. Möchte jemand ein Zimmer, einen Tisch in der Stube, ein Fest oder einen Gutschein, im Chat oder in einem Formular der Website, liegt die Anfrage im Eingang, nach Abteilung, mit einem Brief als Entwurf für Ihre Antwort. Verschickt wird nur, was Sie selbst schicken.'")
t = t.replace(" aus dem Chat bisher", " aus Chat und Website bisher")
# Handy und Tablet (≤ 1100 px): «Gestalten» öffnet als Blatt unten (46 % der Höhe) und lag über dem gewählten Teil, die unteren Ecken liessen sich nicht
# greifen (Fund Bau-Prüfung 17.10.2026, steckt auch im Rivage). Jetzt rollt der gewählte Teil über das Blatt.
ers("    p.hidden = false; document.body.classList.add('gs-seite-offen');",
    "    p.hidden = false; document.body.classList.add('gs-seite-offen');\n"
    "    const el = wahl; if (innerWidth <= 1100) requestAnimationFrame(() => {   // zwischen die Werkzeugleiste oben (klebt) und das Blatt unten; ist der Teil höher als die Lücke, zählt sein oberer Rand\n"
    "      if (!el || !el.isConnected || p.hidden) return;\n"
    "      const r = el.getBoundingClientRect(), oben = p.getBoundingClientRect().top - 14, w = $('.gs-werk'), u = Math.max(w ? w.getBoundingClientRect().bottom : 0, 70) + 14;\n"
    "      let d = r.bottom > oben ? r.bottom - oben : 0; if (r.top - d < u) d = r.top - u; if (Math.abs(d) > 2) scrollBy({ top: d, behavior: 'instant' }); });")
open(p, 'w', encoding='utf-8').write(t)
print('Eingang nach Abteilung eingesetzt')
