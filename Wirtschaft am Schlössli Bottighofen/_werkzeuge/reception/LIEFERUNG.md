---
tags: [projekt, website]
status: aktiv
---

# Lieferung Das Reservationsbuch · Wirtschaft am Schlössli Bottighofen (Nachtbau 3.11.2026)

Aufbau, Wege und Funktionen aus dem Gästebuch des Stamms (sieben Werkzeuge), Inhalt aus dem Schlössli: Hauswerte aus `website/inhalt/*.json`,
Fragen und Briefe des Hauses aus dem Reservationsbuch vom 19.10.2026. Nichts online, nichts verschickt, keine KI aufgerufen (Antworten ohne KI aus
`probe_ki.py`), kein Schlüssel gelesen. Name nur aus `WO.name('gaeste')` bzw. `kleid/schloessli.js › namen` (Python liest ihn per Regex).

**Adresse:** http://127.0.0.1:9284/_werkzeuge/reception/ · Anleitung `anleitung.html` · Prüfung `pruefung.html`
Start aus dem Hausordner: `python3 _werkzeuge/reception/server.py 9284`.

## Was steht

- **Kleid des Hauses:** Farben der Kopie mit `_bau/schloessli_kleid.py` in Nacht über dem See, Stuhlblau, Papier und Seehimmel gerechnet; Open Sans
  (Titel), Instrument Sans, DM Mono aus `/assets/fonts/`; Zeichen = die Zeiger (`zeichen-haus.svg/png`), Briefkopf = Wortmarke «WIRTSCHAFT AM SCHLÖSSLI»
  (`marke-haus.svg`, `marke-haus-weiss.png` für den Mail-Satz); Fotos nur aus `/assets/img/` (eigene Fotos des Hauses, keine Gäste-, Fremd- oder KI-Bilder).
- **Eingang:** Reservation, Bankett, Anlass, Gutschein, Nachricht; Hinweise je Anfrage aus den Angaben des Hauses: Ruhetag (Di/Mi), Ferien
  (13.–15.11.2026 Gourmetkreuzfahrt, 22.12.2026–10.2.2027), mehr Personen als eine Etage fasst (26), Allergien.
- **Brief** in Sie-Form, Schweizer Schreibung, Fuss mit Seestrasse 50, Telefon und kontakt@; Vorlagen aus den Fragen des Hauses
  (`vorlagen/bankett.txt`, `gutschein.txt`, `anlass.txt`); PDF A4 «Wirtschaft am Schlössli – Name – Datum.pdf» (Open Sans + Instrument Sans eingebettet).
- **Wissen des Chats:** `_bau/schloessli_wissen.py` baut `gast/gast_wissen.txt` aus `haus.json`, `karte.json`, `lunch.json`, `laestermeile.json`,
  `wein.json` (Überblick), `bankett.json` und dem Wortlaut der Seiten (Kontakt, Gutschein, AGB; `_bau/website_text.js`), dazu `gast_umgebung.txt`
  (Lage, Anreise, Hunde, Zahlung, Geschichte). Steckbrief «Das weiss der Chat»: 61 belegte Zeilen in elf Bereichen (`steckbrief_bau.py`, bricht ab, wenn ein Beleg fehlt).
- **Beispiele:** acht Anfragen mit fertigem Brief (Terrasse und Nussallergie, Bankett 30 Personen am Kreuzfahrt-Wochenende, Gutschein, Dienstag =
  Ruhetag auf Englisch, Plätze für die Gourmetkreuzfahrt, acht Personen mit Hund, Firmenanlass, Silvester in den Ferien), zwölf Fragen (zwei mit Absicht
  ohne Antwort: Kinderstuhl, Kursschiff). Gäste erfunden (example.com), Angaben des Hauses geprüft (`_bau/schloessli_beispiele.py`).
- **Chat ausprobieren:** antwortet ohne KI aus den belegten Zeilen des Steckbriefs, zeigt bei Tischfragen den Weg zur Reservation (gastronovi).
- **Baustein** für die Formulare der Website (`baustein/anfrage.js`, Reservation, Bankett, Gutschein, «Ihr Abend»), auf der Website nicht eingebaut.
- Gelöscht: Culinarium-Beispiele, -Daten, -Prüfprotokolle, `online/` (Abholen von einer fremden Online-Adresse, jetzt aus).

## Wie geprüft

`node _Werkzeuge/abnahme-tor/tor-schnell.js … --nur gaestebuch` und `--nur gaestebuch-anleitung`, Chromium, 1440/1280/1000/390, max. 40 Zustände,
Tiefe 2; Zustandsbilder 1440 und 390 mit dem Auge; Suchlauf aus dem gemeinsamen Auftrag. Ergebnis unten (Prüfstand).

## Offen, mit Grund

- Die Website hat noch keinen Chat und keinen Online-Eingang: Formulare und Chat landen erst im Eingang, wenn der Baustein eingebaut ist (Revier Website).
- Ob in Bottighofen ein Kursschiff anlegt und ob es Kinderstühle gibt, sagt keine Quelle: steht als Frage ohne Antwort zum Nachtragen.
