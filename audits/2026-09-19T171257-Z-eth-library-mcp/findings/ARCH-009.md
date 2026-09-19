## Finding: ARCH-009 — Tool Annotations: readOnlyHint, destructiveHint, idempotentHint, openWorldHint

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-009
**Katalog-Referenz:** Anhang A5
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- ALLE 6 Tools tragen explizite Annotations, gemessen an `mcp.list_tools()` und zusaetzlich am Draht: der POST `tools/list` durch build_http_app() liefert pro Tool `{"destructiveHint":false,"idempotentHint":true,"openWorldHint":true,"readOnlyHint":true,"title":"..."}`. Kein Tool verlaesst sich auf Defaults durch Weglassen.
- Quelltext-Fundstellen: src/eth_library_mcp/server.py:246-255 (eth_search_resources), :358-366 (eth_get_resource), :422-430 (eth_search_archive), :513-521 (eth_search_by_type), :612-620 (eth_search_education), :689-697 (eth_library_info) — jeweils alle vier Hints plus `title`.
- readOnlyHint konsistent mit dem Verhalten: alle 5 netzsprechenden Tools nutzen ausschliesslich `_http_get` (server.py:291, 379, 448, 544, 646). Suche nach `\.(post|put|patch|delete)\(` ueber src/*.py → 0 Treffer; Negativkontrolle gegen eine Probe-Datei mit `client.post(url)` und `c.delete(u)` → 2 Treffer, das Muster greift. Kein Tool traegt create/update/delete/remove im Namen (gemessene Tool-Liste).
- idempotentHint=True ist korrekt: jeder Aufruf ist ein GET ohne Server-Zustandsaenderung; derselbe Aufruf liefert am gemockten Upstream dasselbe Resultat (selbst gefahren, respx).
- openWorldHint differenziert: 5 Tools True (erreichen api.library.ethz.ch), eth_library_info False — und die Zusicherung ist getestet, nicht nur behauptet (tests/test_tools.py:183-188 `test_library_info_no_network`, ohne respx-Route; ein Netzaufruf wuerde dort scheitern).
- destructiveHint ist bei allen 6 explizit auf False gesetzt statt weggelassen — der Default waere laut Spec True gewesen.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-009.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- ALLE 6 Tools tragen explizite Annotations, gemessen an `mcp.list_tools()` und zusaetzlich am Draht: der POST `tools/list` durch build_http_app() liefert pro Tool `{"destructiveHint":false,"idempotentHint":true,"openWorldHint":true,"readOnlyHint":true,"title":"..."}`. Kein Tool verlaesst sich auf Defaults durch Weglassen.
- Quelltext-Fundstellen: src/eth_library_mcp/server.py:246-255 (eth_search_resources), :358-366 (eth_get_resource), :422-430 (eth_search_archive), :513-521 (eth_search_by_type), :612-620 (eth_search_education), :689-697 (eth_library_info) — jeweils alle vier Hints plus `title`.
- readOnlyHint konsistent mit dem Verhalten: alle 5 netzsprechenden Tools nutzen ausschliesslich `_http_get` (server.py:291, 379, 448, 544, 646). Suche nach `\.(post|put|patch|delete)\(` ueber src/*.py → 0 Treffer; Negativkontrolle gegen eine Probe-Datei mit `client.post(url)` und `c.delete(u)` → 2 Treffer, das Muster greift. Kein Tool traegt create/update/delete/remove im Namen (gemessene Tool-Liste).
- idempotentHint=True ist korrekt: jeder Aufruf ist ein GET ohne Server-Zustandsaenderung; derselbe Aufruf liefert am gemockten Upstream dasselbe Resultat (selbst gefahren, respx).
- openWorldHint differenziert: 5 Tools True (erreichen api.library.ethz.ch), eth_library_info False — und die Zusicherung ist getestet, nicht nur behauptet (tests/test_tools.py:183-188 `test_library_info_no_network`, ohne respx-Route; ein Netzaufruf wuerde dort scheitern).
- destructiveHint ist bei allen 6 explizit auf False gesetzt statt weggelassen — der Default waere laut Spec True gewesen.

### Gaps

- Pass-Kriterium 6 unerfuellt: es gibt keine Annotations-Uebersicht in README.md, README.de.md oder docs/. Gemessen mit whitespace-normalisierter Suche nach readOnlyHint/destructiveHint/idempotentHint/openWorldHint/Annotation ueber README.md, README.de.md, docs/ARCHITECTURE.md, SECURITY.md, SECURITY.de.md: einziger Treffer ist SECURITY.md:29 bzw. SECURITY.de.md — eine Zeile 'Every tool sets readOnlyHint: True', keine Tabelle, und SECURITY.md ist keiner der vom Check akzeptierten Orte. Positivkontrolle: dieselbe Suche findet den Begriff dort, wo er steht (SECURITY.md), also greift sie.
- Damit ist auch nicht dokumentiert, dass destructiveHint/idempotentHint/openWorldHint gesetzt sind und nach welcher Policy — die SECURITY-Zeile nennt nur readOnlyHint.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-009.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.
