"""Die Tafel (La Carte) · Wirtschaft am Schlössli Bottighofen — Anschluss an die Website (19.10.2026): noch nicht gebaut.

Die Website des Schlössli zeigt ihre Karten als Zeilen aus website/inhalt/*.json (gelesen von website/karten_lesen.py aus den PDFs des Hauses),
nicht aus der Tafel. Die Website-Seiten gehören in dieser Station dem Werkbank-Bauer (Station 14 verbindet), deshalb schreibt die Tafel dort nichts:
- seite_mit() liefert None → die Ansicht «Website» zeigt die Seite, wie sie heute ist (serve.py leitet weiter), mit dem Hinweis im Werkzeug.
- anschliessen() setzt keine Seiten; mit eingeschaltetem Anschluss geht nur die PDF nach website/unterlagen/pdf/<karte>.pdf (carte.py _anschluss).
Der Bauplan für den echten Anschluss (Zeilen-Abgleich, zwei Bauten, C18/C21/C22) liegt als web.py.vorlage-gasterntal daneben."""

KARTEN = {}


def ids(d, vorsatz='k'):
    return d


def abgleich(karten, D=None):
    return {}


def anschluss_im_bau():
    return False


def anschliessen(z, d, K=None):
    return []


def seite_mit(z, d, seite, K=None):
    return None
