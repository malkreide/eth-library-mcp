## Finding: DRIFT-002 — Fallback verengt, erweitert nie — lieber ein Fehler als ein anderer Datensatz

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** DRIFT-002
**Katalog-Referenz:** Custom (Portfolio-Fundstück meteoswiss-mcp#33, 2026-07-30)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/server.py:378 — BEFUND: `doc = data.get("docs", [{}])[0] if data.get("docs") else data`. Der else-Zweig nimmt den ANTWORT-UMSCHLAG selbst als Datensatz. Gemessen mit respx (200, Body `{"info": {"total": 0}, "warnung": "nichts gefunden"}`): `eth_get_resource` liefert `'# Kein Titel\n*Quelle: ETH-Bibliothek (Public Domain) · https://developer.library.ethz.ch*'` — kein Fehlermarker, Ueberschrift und Quellenzeile wie bei einem echten Treffer. Der Aufruf gelingt, die Antwort ist wohlgeformt, der Inhalt ist keiner
- src/eth_library_mcp/server.py:280-285, 442-444, 538-540, 640-644 — die vier Such-Werkzeuge eskalieren dagegen korrekt: `if not docs: return "Keine Ergebnisse fuer ..."` bzw. "Keine Treffer im Archiv ...". Gemessen: bei `{"docs": [], "info": {"total": 0}}` antwortet eth_search_resources mit "Keine Ergebnisse fuer 'any,contains,xyzq'." — kein substituierter Datensatz
- Keine Substitution ueber Granularitaet, Zeitbezug oder Entitaet im gesamten src/: `grep -rnE 'break$|next\(iter\(|\[0\]\s*$' src/` liefert ausser der Zeile 378 keinen Auswahl-Fallback; `_first()` (formatting.py:23-25) waehlt das erste Element EINES FELDES, nicht einen anderen Datensatz
- tests/test_tools.py:73-79 — `test_search_resources_no_hits` haelt den Nicht-Fund fuer die Suchwerkzeuge fest. Fuer `eth_get_resource` existiert kein entsprechender Test: `tests/test_tools.py:109-129` deckt nur Happy-Path und HTTP-404 ab, nicht den 200-ohne-docs-Zweig

### Expected Behavior

Die Pass-Kriterien stehen in `checks/DRIFT-002.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/server.py:378 — BEFUND: `doc = data.get("docs", [{}])[0] if data.get("docs") else data`. Der else-Zweig nimmt den ANTWORT-UMSCHLAG selbst als Datensatz. Gemessen mit respx (200, Body `{"info": {"total": 0}, "warnung": "nichts gefunden"}`): `eth_get_resource` liefert `'# Kein Titel\n*Quelle: ETH-Bibliothek (Public Domain) · https://developer.library.ethz.ch*'` — kein Fehlermarker, Ueberschrift und Quellenzeile wie bei einem echten Treffer. Der Aufruf gelingt, die Antwort ist wohlgeformt, der Inhalt ist keiner
- src/eth_library_mcp/server.py:280-285, 442-444, 538-540, 640-644 — die vier Such-Werkzeuge eskalieren dagegen korrekt: `if not docs: return "Keine Ergebnisse fuer ..."` bzw. "Keine Treffer im Archiv ...". Gemessen: bei `{"docs": [], "info": {"total": 0}}` antwortet eth_search_resources mit "Keine Ergebnisse fuer 'any,contains,xyzq'." — kein substituierter Datensatz
- Keine Substitution ueber Granularitaet, Zeitbezug oder Entitaet im gesamten src/: `grep -rnE 'break$|next\(iter\(|\[0\]\s*$' src/` liefert ausser der Zeile 378 keinen Auswahl-Fallback; `_first()` (formatting.py:23-25) waehlt das erste Element EINES FELDES, nicht einen anderen Datensatz
- tests/test_tools.py:73-79 — `test_search_resources_no_hits` haelt den Nicht-Fund fuer die Suchwerkzeuge fest. Fuer `eth_get_resource` existiert kein entsprechender Test: `tests/test_tools.py:109-129` deckt nur Happy-Path und HTTP-404 ab, nicht den 200-ohne-docs-Zweig

### Gaps

- server.py:378 eskaliert nicht, sondern substituiert: eine 200-Antwort ohne `docs` wird als Ressourcen-Detail gerendert. Wo kein semantisch gleichwertiger Kandidat existiert, gehoerte ein Fehler hin
- Die Abweichung ist in der Antwort nicht ausgewiesen — kein Feld, nicht einmal Prosa; der Konsument kann 'Kein Titel' nicht von 'nichts geliefert' unterscheiden
- Kein Test ueber den leeren Kandidatensatz von `eth_get_resource` (200 ohne `docs`)
- Keine Auswahlfunktion mit Docstring, der begruendet, was bewusst NICHT genommen wird — die Auswahl steht als Inline-Ausdruck in der Tool-Funktion

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/DRIFT-002.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.
