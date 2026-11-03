#!/usr/bin/env python3
"""Sechster Schritt nach portiere.py, ruedihus.py, brief.py, pdf.py (und server_teil.py); übernommen aus dem Carlton-Europe (_bau/abnahme.py dort, nur gelesen, über das Doldenhorn): was die Abnahme vom 16.10.2026 nach dem Master
Werkzeug-Bau (Abschnitt 3) verlangt und im Rivage fehlt: Prüfseite pruefung.html (R23) mit Knopf im Kopf und Weg im Rand (R05, R06),
Fehler als Quittung mit Stichwort und «Was tun?» (R11). Jede Ersetzung muss genau einmal treffen, sonst bricht das Skript ab.
Aufruf: python3 _werkzeuge/reception/_bau/abnahme.py"""
import os, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(C, 'reception.js')
t = open(p, encoding='utf-8').read()


def ers(alt, neu, n=1):
    global t
    if t.count(alt) != n:
        sys.exit(f'ABBRUCH: «{alt[:80]}» kommt {t.count(alt)}× vor, erwartet {n}×')
    t = t.replace(alt, neu)


# R11: Fehler zeigen ihr Stichwort und führen mit «Was tun?» zum Eintrag im Lexikon der Prüfseite
ers("function fehler(e) { quit(String((e && e.message) || e).replace(/^[A-ZÄÖÜ]+ · /, ''), '', [], true); }",
    "function fehler(e) {\n"
    "  const m = String((e && e.message) || e), st = (m.match(/^([A-ZÄÖÜ-]+) · /) || [])[1] || '';\n"
    "  quit(m.replace(/^[A-ZÄÖÜ-]+ · /, ''), st ? 'Stichwort ' + st : '', [['Was tun?', () => window.open('pruefung.html#' + (st || 'SERVER'), '_blank', 'noopener')]], true, 12000);\n"
    "}")
# R05: runder Knopf «Prüfung» im Kopf
ers("  haken: '<svg viewBox=\"0 0 16 16\" aria-hidden=\"true\"><path d=\"m3.5 8.5 3 3 6-7\"/></svg>' };",
    "  haken: '<svg viewBox=\"0 0 16 16\" aria-hidden=\"true\"><path d=\"m3.5 8.5 3 3 6-7\"/></svg>',\n"
    "  pruef: '<svg viewBox=\"0 0 16 16\" aria-hidden=\"true\"><path d=\"M8 1.8 13 3.8v3.7c0 3-2.1 5.4-5 6.7-2.9-1.3-5-3.7-5-6.7V3.8z\"/><path d=\"m5.6 8 1.7 1.7 3.2-3.4\"/></svg>' };")
ers('      <a class="rund" href="anleitung.html" target="_blank" rel="noopener" data-tip="Anleitung" aria-label="Anleitung">${SYM.buch}</a>\n',
    '      <a class="rund" href="pruefung.html" target="_blank" rel="noopener" data-tip="Prüfung" aria-label="Prüfung">${SYM.pruef}</a>\n'
    '      <a class="rund" href="anleitung.html" target="_blank" rel="noopener" data-tip="Anleitung" aria-label="Anleitung">${SYM.buch}</a>\n')
# R06: Weg zur Prüfung unten im Rand
ers('      <a href="anleitung.html" target="_blank" rel="noopener">Anleitung${PF}</a>\n      <a href="${STUBE}">Die Stube${PF}</a>',
    '      <a href="anleitung.html" target="_blank" rel="noopener">Anleitung${PF}</a>\n      <a href="pruefung.html" target="_blank" rel="noopener">Prüfung${PF}</a>\n'
    '      <a href="${STUBE}">Die Stube${PF}</a>')
open(p, 'w', encoding='utf-8').write(t)
print('Abnahme eingesetzt')

# R10/R13 (Fund der Abnahme 17.10.2026, steckt auch im Rivage): Wechsel zu einer anderen Anfrage verwarf ungesicherte Eingaben in «Nur Text»
# und die letzten 0,7 s Tippen im gestalteten Brief; Verlassen der Seite fragte nie nach. Jetzt: vor jedem Wechsel sichern, beim Verlassen nachfragen.
t = open(p, encoding='utf-8').read()
ers("function gehe(ziel, wahl = '') {\n  const gs = $('#gs-seite');", "function gehe(ziel, wahl = '') {\n  wartendesSichern();   // was im Brief noch wartet, vor dem Wechsel sichern (Abnahme 17.10.2026)\n  const gs = $('#gs-seite');")
t += """
/* Abnahme 17.10.2026 (_bau/abnahme.py): nichts geht beim Wechseln oder Verlassen still verloren. */
function nurTextOffen() {
  const tx = $('#e-text'), be = $('#e-betreff'), a = S.anfragen && S.anfragen.find(x => x.id === S.wahl);
  return tx && be && a && a.entwurf && (tx.value !== a.entwurf.text || be.value !== a.entwurf.betreff) ? { a, betreff: be.value, text: tx.value } : null;
}
function wartendesSichern() {
  if ($('#brief') && S.briefSichern) Promise.resolve(S.briefSichern()).catch(() => {});
  const o = nurTextOffen();
  if (o) { o.a.entwurf.betreff = o.betreff; o.a.entwurf.text = o.text; api('anfrage', { id: o.a.id, betreff: o.betreff, entwurf_text: o.text }).then(() => quit('Gesichert', 'Ihre Änderung am Brief ist gespeichert.', [], false, 3000)).catch(fehler); }
}
addEventListener('beforeunload', ev => {
  const offen = nurTextOffen() || $('#gs-stand.laeuft') || $$('#fenster:not([hidden]) textarea, #fenster:not([hidden]) input[type=text], #w-text').some(x => x.value.trim() && x.value !== x.defaultValue);
  if (offen) { ev.preventDefault(); ev.returnValue = ''; }
});
"""
open(p, 'w', encoding='utf-8').write(t)
print('Wechseln und Verlassen gesichert')

# Rundgang, Zur-Werkbank, Fehlermelder und Anleitung-Knopf: _bau/rahmen.py (aus dem Carlton, im Kleid des Ruedihus)

# «Als PDF sichern» online: dort gibt es kein node mit Chromium; der Server antwortet «DRUCK · …», dann öffnet das Druckfenster mit demselben A4-Satz
t = open(p, encoding='utf-8').read()
ers("  if (!r.ok) { let d = {}; try { d = await r.json(); } catch (e) { /* */ } return fehler(new Error(d.fehler || ('SERVER · Fehler ' + r.status))); }",
    "  if (!r.ok) { let d = {}; try { d = await r.json(); } catch (e) { /* */ }\n"
    "    if (/^DRUCK · /.test(d.fehler || '')) { quit('Druckfenster', 'Dort «Als PDF sichern» wählen. Der Brief steht auf A4 wie im Werkzeug.', [], false, 8000); setTimeout(() => window.print(), 300); return; }\n"
    "    return fehler(new Error(d.fehler || ('SERVER · Fehler ' + r.status))); }")
open(p, 'w', encoding='utf-8').write(t)
print('PDF online über Druckfenster')

# Netz weg (Abnahme 17.10.2026): Meldung in Alltagssprache, ohne Dateinamen, und mit dem Hinweis, dass die Eingabe noch da ist
t = open(p, encoding='utf-8').read()
ers("throw new Error('VERBINDUNG · Der Server-Teil antwortet nicht. Läuft serve.py?');", "throw new Error('VERBINDUNG · Keine Verbindung. Ihre Eingabe ist noch da, bitte gleich noch einmal versuchen.');")
ers("return fehler(new Error('VERBINDUNG · Der Server-Teil antwortet nicht.'));", "return fehler(new Error('VERBINDUNG · Keine Verbindung. Bitte gleich noch einmal versuchen.'));")
open(p, 'w', encoding='utf-8').write(t)
print('Meldung ohne Netz')

# Abnahme 17.10.2026: Wer die Seite verliess, während der Brief gerade sicherte, brach das Sichern ab (der Browser kappt laufende Anfragen);
# blieb man auf der Nachfrage hin auf der Seite, stand der Brief für immer auf «Nicht gesichert». Jetzt: bis fünfmal von selbst nachsichern,
# die Meldung nur beim ersten Fehlschlag; beim Verlassen wird sofort gesichert, statt die 0,7 s abzuwarten.
t = open(p, encoding='utf-8').read()
ers("      try { await api('anfrage', { id: a.id, betreff: e.betreff, entwurf_text: e.text, gestalt: G }); S.gesichert[a.id] = jetzt; if (stand) { stand.textContent = 'Gesichert'; stand.classList.remove('laeuft'); } }\n      catch (x) { if (stand) stand.textContent = 'Nicht gesichert'; fehler(x); }",
    "      try { await api('anfrage', { id: a.id, betreff: e.betreff, entwurf_text: e.text, gestalt: G }); S.gesichert[a.id] = jetzt; S.nachSichern = 0; if (stand) { stand.textContent = 'Gesichert'; stand.classList.remove('laeuft'); } }\n"
    "      catch (x) { if (stand) stand.textContent = 'Nicht gesichert'; S.nachSichern = (S.nachSichern || 0) + 1; if (S.nachSichern === 1) fehler(x); if (S.nachSichern <= 5) setTimeout(() => { if (br.isConnected) sichern(true); }, 1500 * S.nachSichern); }")
ers("  if (offen) { ev.preventDefault(); ev.returnValue = ''; }", "  if ($('#gs-stand.laeuft') && S.briefSichern) S.briefSichern();   // sofort sichern; bleibt man auf der Seite, ist es danach gesichert\n  if (offen) { ev.preventDefault(); ev.returnValue = ''; }")
open(p, 'w', encoding='utf-8').write(t)
print('Nachsichern')

# Zwei Fenster am selben Brief (Carlton E21, Abnahme 17.10.2026; im Doldenhorn noch nicht): jede Änderung am Entwurf schickt die Fassungsnummer mit,
# Änderungen einer Anfrage laufen nacheinander (sonst träfen sich zwei eigene Anfragen mit derselben Nummer), bei «KONFLIKT» kein Nachsichern,
# sondern Meldung mit «Neu laden». Übernommen aus Carlton _bau/abnahme.py (nur gelesen).
t = open(p, encoding='utf-8').read()
ers("async function api(was, daten) {\n  let r;", "async function api(was, daten) {\n"
    "  if (was === 'anfrage' && daten && (typeof daten.entwurf_text === 'string' || daten.gestalt) && !daten.__kette) {   // Fassung mitschicken, nacheinander (Carlton E21)\n"
    "    const a = (S.anfragen || []).find(x => x.id === daten.id);\n"
    "    const lauf = async () => { const d = await api(was, { ...daten, __kette: 1, fassung: a && a.entwurf ? (a.entwurf.fassung || 0) : undefined }); if (a && a.entwurf && typeof d.fassung === 'number') a.entwurf.fassung = d.fassung; return d; };\n"
    "    const k = (S.kette || Promise.resolve()).catch(() => {}).then(lauf); S.kette = k; return k;\n"
    "  }\n"
    "  if (daten && daten.__kette) { daten = { ...daten }; delete daten.__kette; }\n"
    "  let r;")
ers("if (S.nachSichern === 1) fehler(x); if (S.nachSichern <= 5)", "if (/^KONFLIKT/.test(x.message)) { S.nachSichern = 0; return quit('Anderes Fenster war schneller', 'Dieser Brief wurde inzwischen in einem anderen Fenster geändert. Ihre Eingabe ist noch hier.', [['Neu laden', () => frisch(true)]], true, 0); } if (S.nachSichern === 1) fehler(x); if (S.nachSichern <= 5)")
open(p, 'w', encoding='utf-8').write(t)
print('Konflikt statt Überschreiben')

# Firefox am Handy (Carlton F47, steckt im Rivage): Antippen ausserhalb des Briefs wählte ab und zeichnete die Leiste «Gestalten» neu, auch ohne Auswahl;
# die Seite rückte dabei um rund 84 px, der Tipp auf Knöpfe unter dem Brief kam nicht an. Jetzt nur abwählen, wenn etwas gewählt ist oder geschrieben wird.
t = open(p, encoding='utf-8').read()
ers("if (!br.isConnected) return; if (!br.contains(ev.target) && !ev.target.closest('#fenster')",
    "if (!br.isConnected) return; if (!wahl && !br.querySelector('[contenteditable=\"true\"]')) return; if (!br.contains(ev.target) && !ev.target.closest('#fenster')")
open(p, 'w', encoding='utf-8').write(t)
print('Antippen ohne Verrutschen')

# «Zurück auf die Vorlage» (Prüfung 17.10.2026, steckt so im Rivage): die Vorlage wurde beim ersten Öffnen des gestalteten Briefs aus dem gerade
# gespeicherten Text genommen. Hatte das Team vorher in «Nur Text» geändert, holte der Knopf diese Änderung zurück statt des Briefs des Assistenten.
# Jetzt merkt sich der Server die Fassung des Assistenten beim ersten Ändern (entwurf.original, _bau/server_teil.py), die Oberfläche nimmt sie.
t = open(p, encoding='utf-8').read()
ers("  if (!G._orig) G._orig = { text: e.text, betreff: e.betreff };",
    "  G._orig = e.original ? { text: e.original.text, betreff: e.original.betreff } : (G._orig || { text: e.text, betreff: e.betreff });")
open(p, 'w', encoding='utf-8').write(t)
print('Vorlage = Fassung des Assistenten')

# Handgriffe, die den Brief neu zeichnen, gingen verloren (Prüfung 17.10.2026, brief_halt.js H1–H4; steckt so im Rivage, Carlton und Doldenhorn):
# Foto einfügen, Foto entfernen, Linie entfernen und «Zurück auf die Vorlage» zeichneten den Brief neu, und das Neuzeichnen merkte den neuen Stand als
# «schon gesichert»; das Sichern danach fand «nichts Neues» und schickte nichts. Nach dem Neuladen war alles wie vorher.
# Jetzt zeichnet neu(true) neu, ohne den Stand als gesichert zu merken, und sichert sofort über den neuen Brief (mit Anzeige und Nachsichern).
t = open(p, encoding='utf-8').read()
ers("  const neu = () => { e.gestalt = G; neuDetail(a); };",
    "  const neu = offen => { e.gestalt = G; if (offen) S.offenNach = a.id; neuDetail(a); if (offen && S.briefSichern) S.briefSichern(); };")
ers("  S.gesichert[a.id] = JSON.stringify([e.betreff, e.text, G]);   // so wie geladen",
    "  if (S.offenNach === a.id) delete S.offenNach; else S.gesichert[a.id] = JSON.stringify([e.betreff, e.text, G]);   // so wie geladen")
ers("g.aus = true; merke(alt); sichern(); return neu(); }", "g.aus = true; merke(alt); return neu(true); }")
ers("delete G[k]; merke(alt); sichern(); return neu(); }", "delete G[k]; merke(alt); return neu(true); }")
ers("G = e.gestalt = { _orig: o }; merke(alt); neu(); sichern(true);", "G = e.gestalt = { _orig: o }; merke(alt); neu(true);")
ers("fensterZu(); merke(alt); neu(); sichern(true);\n", "fensterZu(); merke(alt); neu(true);\n")
open(p, 'w', encoding='utf-8').write(t)
print('Neu gezeichnete Handgriffe werden gesichert')

# Öffnen macht eine Anfrage «gelesen»: Kopf, Rand und Leiste zählten neu, die Auswahl «Neu» über der Liste blieb bis zum nächsten Neuzeichnen
# auf der alten Zahl (Prüfung 17.10.2026: Kopf «4 neue Anfragen», Auswahl «Neu 5»; steckt so im Rivage).
t = open(p, encoding='utf-8').read()
ers("a.status = 'gelesen'; S.ue = { ...S.ue, ...d }; rand(); leiste(); const k = ",
    "a.status = 'gelesen'; S.ue = { ...S.ue, ...d }; rand(); leiste(); const zn = $('.re-filter [data-filter=\"neu\"] i'); if (zn) zn.textContent = (S.abt === 'alle' ? S.anfragen : S.anfragen.filter(x => abt(x) === S.abt)).filter(x => x.status === 'neu').length; const k = ")
open(p, 'w', encoding='utf-8').write(t)
print('Auswahl «Neu» zählt beim Öffnen mit')

# R04 Startfehler-Tür (Prüfung 17.10.2026): hing der Server, ohne zu antworten, blieb die Seite leer und die Tür kam nie. Jetzt Wache nach 12 s.
# Die Knöpfe «Prüfung öffnen» und «Neu laden» stehen in index.html (Rivage seit 17.10.2026 gleich).
t = open(p, encoding='utf-8').read()
ers("  try { S.ue = await api('ueberblick'); }",
    "  try { S.ue = await Promise.race([api('ueberblick'), new Promise((_, nein) => setTimeout(() => nein(new Error('SERVER · Der Server-Teil antwortet nicht.')), 12000))]); }")
open(p, 'w', encoding='utf-8').write(t)
print('Startfehler-Tür mit Wache')

# Startfehler-Tür ohne Netz zeigte «Keine Verbindung. Ihre Eingabe ist noch da …» (Meldung fürs Speichern); beim Start gibt es noch keine Eingabe.
t = open(p, encoding='utf-8').read()
ers("catch (e) { $('#tuer').hidden = false; $('#tuer-t').textContent = String(e.message || e).replace(/^[A-ZÄÖÜ]+ · /, ''); return; }",
    "catch (e) { $('#tuer').hidden = false; $('#tuer-t').textContent = /^VERBINDUNG · /.test(e.message || '') ? 'Keine Verbindung zum Server-Teil. Bitte gleich neu laden.' : String(e.message || e).replace(/^[A-ZÄÖÜ]+ · /, ''); return; }")
open(p, 'w', encoding='utf-8').write(t)
print('Startfehler-Tür ohne Netz in eigenen Worten')
