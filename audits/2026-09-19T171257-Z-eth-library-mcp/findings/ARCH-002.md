## Finding: ARCH-002 — Tool-Beschreibung mit Use-Case-Tags

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-002
**Katalog-Referenz:** Sec 2.2
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- Gemessen mit `mcp.list_tools()` und `re.sub(r'\s+',' ',desc)`: Laengen [59, 71, 71, 73, 74, 215], Median 72 Zeichen. Pass-Kriterium verlangt Median >= 100 — verfehlt. Minimum 59 liegt ueber der 50-Zeichen-Untergrenze.
- Suche nach `<use_case>|<important_notes>|<example>` ueber alle 5 Dateien in src/, jeweils NACH Whitespace-Normalisierung des ganzen Datei-Texts: 0 Treffer in client.py, __init__.py, formatting.py, logging_config.py, server.py. Positivkontrolle im selben Lauf: derselbe Regex auf 'desc <use_case>x</use_case>' → Treffer; Negativkontrolle 'nothing here' → kein Treffer. Das Muster greift also.
- src/eth_library_mcp/server.py:423-437 — die Description von eth_search_archive ist der Docstring 'Durchsucht ein spezifisches Archiv oder eine Sammlung der ETH-Bibliothek.' (73 Zeichen), ohne Caveat, Limit-Hinweis oder Abgrenzung zu eth_search_resources.
- Mildernd, aber nicht kriteriumserfuellend: die Feld-Beschreibungen im inputSchema sind reichhaltig — gemessen im tools/list-Schema traegt `query` 301 Zeichen mit Syntaxerklaerung und zwei Beispielen (src/eth_library_mcp/server.py:200-207). Die Kriterien von ARCH-002 beziehen sich auf die Tool-Description, nicht auf Parameterfelder.
- src/eth_library_mcp/server.py:175-186 — die Server-`instructions` (Zeile 179: 'Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung') bewerben ein Werkzeug, das 0.4.0 entfernt hat. Gemessen im `server/discover`-Resultat durch den zusammengebauten ASGI-Stack: der Satz geht live an jeden Client raus.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-002.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Gemessen mit `mcp.list_tools()` und `re.sub(r'\s+',' ',desc)`: Laengen [59, 71, 71, 73, 74, 215], Median 72 Zeichen. Pass-Kriterium verlangt Median >= 100 — verfehlt. Minimum 59 liegt ueber der 50-Zeichen-Untergrenze.
- Suche nach `<use_case>|<important_notes>|<example>` ueber alle 5 Dateien in src/, jeweils NACH Whitespace-Normalisierung des ganzen Datei-Texts: 0 Treffer in client.py, __init__.py, formatting.py, logging_config.py, server.py. Positivkontrolle im selben Lauf: derselbe Regex auf 'desc <use_case>x</use_case>' → Treffer; Negativkontrolle 'nothing here' → kein Treffer. Das Muster greift also.
- src/eth_library_mcp/server.py:423-437 — die Description von eth_search_archive ist der Docstring 'Durchsucht ein spezifisches Archiv oder eine Sammlung der ETH-Bibliothek.' (73 Zeichen), ohne Caveat, Limit-Hinweis oder Abgrenzung zu eth_search_resources.
- Mildernd, aber nicht kriteriumserfuellend: die Feld-Beschreibungen im inputSchema sind reichhaltig — gemessen im tools/list-Schema traegt `query` 301 Zeichen mit Syntaxerklaerung und zwei Beispielen (src/eth_library_mcp/server.py:200-207). Die Kriterien von ARCH-002 beziehen sich auf die Tool-Description, nicht auf Parameterfelder.
- src/eth_library_mcp/server.py:175-186 — die Server-`instructions` (Zeile 179: 'Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung') bewerben ein Werkzeug, das 0.4.0 entfernt hat. Gemessen im `server/discover`-Resultat durch den zusammengebauten ASGI-Stack: der Satz geht live an jeden Client raus.

### Gaps

- Kein Tool nennt Use-Case-Tags oder ein Aequivalent (0% statt geforderter 80%).
- Keine Important-Notes/Caveats in den Descriptions: weder das 100er-Limit, noch dass ein API-Key noetig ist, noch dass eth_get_resource eine MMS-ID aus einer vorherigen Suche braucht.
- Bei vier stark aehnlichen Such-Tools macht keine Description die Differenzierung explizit — genau der Common-Failure-Fall 'LLM raet, welches richtig ist'.
- Die Server-instructions bewerben ein entferntes Werkzeug (Personen-Suche). Der CHANGELOG 0.4.0 beschreibt, dass pyproject.toml, server.json, READMEs, EXAMPLES.md und docs/ dafuer nachgezogen wurden — server.py:179 wurde dabei uebersehen.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-002.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
