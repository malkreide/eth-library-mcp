## Finding: ARCH-021 — Extensions deklariert und versioniert — Tasks sind kein Kern-Feature mehr

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-021
**Katalog-Referenz:** SEP-2663
**Spec-Baseline:** 2026-07-28
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Keine Extension im Code: grep -rnE "io\.modelcontextprotocol/|extensions" ueber src/ trifft genau zwei Kommentarzeilen — src/eth_library_mcp/__init__.py:55 und src/eth_library_mcp/server.py:148 —, und beide nennen `_meta.io.modelcontextprotocol/serverInfo`, also einen Meta-Schluessel der Kernspec, keine Extension-Deklaration. Negativkontrolle: dasselbe Muster gegen mcp_types/_types.py trifft (Zeilen 53, 59, 62).
- Keine Tasks in keiner Fassung: grep -rnE "tasks/(get|update|result|list)|TaskHandle|task_id" ueber src/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen mcp/server/extension.py:59 trifft. Laufzeit GEMESSEN: `tasks/list` durch build_http_app() -> -32601 "Method not found"; weder die alte noch die Extension-Fassung wird bedient.
- Deklaration deckt sich in BEIDE Richtungen mit dem Code, gemessen an server/discover: die ausgelieferten capabilities bestehen aus prompts, resources und tools — ein `extensions`-Feld fehlt, und es gibt nichts zu deklarieren. Weder «deklariert, nicht implementiert» noch «implementiert, nicht deklariert».
- Kein eigener Namensraum missbraucht: es gibt ueberhaupt keine eigene Erweiterung, also auch keine unter `io.modelcontextprotocol/*` (gedeckt vom ersten Punkt).

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-021.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Keine Extension im Code: grep -rnE "io\.modelcontextprotocol/|extensions" ueber src/ trifft genau zwei Kommentarzeilen — src/eth_library_mcp/__init__.py:55 und src/eth_library_mcp/server.py:148 —, und beide nennen `_meta.io.modelcontextprotocol/serverInfo`, also einen Meta-Schluessel der Kernspec, keine Extension-Deklaration. Negativkontrolle: dasselbe Muster gegen mcp_types/_types.py trifft (Zeilen 53, 59, 62).
- Keine Tasks in keiner Fassung: grep -rnE "tasks/(get|update|result|list)|TaskHandle|task_id" ueber src/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen mcp/server/extension.py:59 trifft. Laufzeit GEMESSEN: `tasks/list` durch build_http_app() -> -32601 "Method not found"; weder die alte noch die Extension-Fassung wird bedient.
- Deklaration deckt sich in BEIDE Richtungen mit dem Code, gemessen an server/discover: die ausgelieferten capabilities bestehen aus prompts, resources und tools — ein `extensions`-Feld fehlt, und es gibt nichts zu deklarieren. Weder «deklariert, nicht implementiert» noch «implementiert, nicht deklariert».
- Kein eigener Namensraum missbraucht: es gibt ueberhaupt keine eigene Erweiterung, also auch keine unter `io.modelcontextprotocol/*` (gedeckt vom ersten Punkt).

### Gaps

- Kriterium 1 unerfuellt: Weder README.md noch README.de.md noch CHANGELOG.md sagt in einem Satz, dass dieser Server keine Extension fuehrt. Normalisierte Suche (Zeilenumbrueche geglaettet) nach `extension|erweiterung|tasks` ueber alle drei Dateien -> 0 Treffer; Negativkontrolle gegen eine Probedatei mit «Dieser Server fuehrt keine Extensions.» trifft. Damit bleiben «keine» und «nicht dokumentiert» fuer einen Leser ununterscheidbar — genau die Failure-Zeile «README schweigt zu Extensions» des Checks.
- Behebung ist ein Satz je README, neben dem bestehenden Abschnitt «MCP Protocol Version» / «MCP-Protokollversion» (tests/test_protocol_version.py:62-65 nennt beide Anker). Ein Test, der ihn haelt, liesse sich nach demselben Muster wie test_beide_readmes_nennen_dieselben_beiden_revisionen schreiben.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-021.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
