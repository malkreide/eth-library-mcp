## Finding: DRIFT-006 — Der CHANGELOG darf dem Code nicht widersprechen

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** DRIFT-006
**Katalog-Referenz:** Custom (Portfolio-Fundstück swiss-energy-mcp, 2026-08-01)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- BEFUND src/eth_library_mcp/server.py:179 — die `instructions` des Servers fuehren «Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung.» GEMESSEN an einem echten `initialize` durch build_http_app(): der Satz steht so im Handshake-Resultat. Gleichzeitig gemessen: `hasattr(eth_library_mcp.server, 'eth_search_persons')` ist False, und tests/test_server.py:254-259 verbietet das Werkzeug ausdruecklich («Eine Faehigkeit, die es nicht gibt, darf nicht angeboten werden»). Der Server bewirbt im Handshake genau die Faehigkeit, die sein eigener Test verbietet
- BEFUND src/eth_library_mcp/server.py:713 — `**Version:** 0.3.0` im Rueckgabetext von `eth_library_info`. GEMESSEN an einem tools/call durch build_http_app(): DIESELBE Antwort traegt in `_meta['io.modelcontextprotocol/serverInfo']['version']` den Wert `0.4.0`. Zwei Versionsangaben, eine Antwort, ein Widerspruch. scripts/check_version_sync.py faengt ihn nicht — CI ist gruen
- BEFUND src/eth_library_mcp/server.py:21 — der Modul-Docstring beschreibt «formatting.py — Markdown-Rendering, Persons-Parsing, Error-Mapping». Der HEAD-Commit 32ac730 heisst «refactor: toten Persons-Parser entfernen»; `grep -in person src/eth_library_mcp/formatting.py` liefert 0 Treffer (Gegenkontrolle: dasselbe Muster liefert in server.py 4 Treffer). Die Modulgrenze beschreibt eine Funktion, die es nicht mehr gibt
- BEFUND src/eth_library_mcp/server.py:580 — die Abschnittsueberschrift «TOOL 5: Personen suchen» steht ueber `SearchEducationInput` / `eth_search_education`; die naechste Ueberschrift ist «TOOL 7» (server.py:688). Die Nummerierung und der Titel beschreiben den entfernten Stand
- BEFUND tests/test_tools.py:8-9 — «Run with `pytest -m live` for the (currently absent) live suite.» GEMESSEN: `pytest -m live --collect-only` sammelt zwei Tests ein (tests/test_server.py::TestLiveGatewayRoutes), und README.md:331 datiert ihre Einfuehrung auf 2026-08-08. Zusaetzlich tests/test_tools.py:5 — «against a stubbed Discovery / Persons API response»; Persons-Tests gibt es in der Datei keine
- BEFUND docs/ARCHITECTURE.md:14 und :67, README.md:243, README.de.md:244 — «FastMCP tools, resources, prompts», «FastMCP's structured-output path», «FastMCP-Server, alle Tools». Der Server laeuft auf `mcp.server.mcpserver.MCPServer` (server.py:34); FastMCP ist in mcp 2.0.0 entfallen und `grep -rn 'FastMCP' src/ tests/` liefert 0 Treffer
- BEFUND README.md:53 / README.de.md:53 «Dual transport – stdio for Claude Desktop, Streamable HTTP/SSE for cloud deployment» und README.md:133 / README.de.md:133 «Cloud Deployment (SSE for browser access)». GEMESSEN: `build_http_app().routes` enthaelt genau eine Route, `/mcp`; GET und POST auf `/sse` antworten mit HTTP 404. Eine dokumentierte Faehigkeit, die der Code nicht hat
- Modus 1 gefuehrt, nicht nur gegrept: `[Unreleased]` in CHANGELOG.md ist leer (sed-Auszug zwischen `## [Unreleased]` und `## [0.4.0]` enthaelt keine Zeile) — von dort kommt kein Widerspruch. Modus 2 als Vorsortierung: das Absichtsvokabular findet zwei Stellen, docs/secret-management.md:43 («planned for a future sprint», trifft zu — keine gitleaks-Stufe in ci.yml) und tests/test_tools.py:9 (widerlegt, siehe oben). Gegenkontrolle: dasselbe Muster gegen eine Probedatei mit «noch nicht implementiert» liefert 1 Treffer

### Expected Behavior

Die Pass-Kriterien stehen in `checks/DRIFT-006.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- BEFUND src/eth_library_mcp/server.py:179 — die `instructions` des Servers fuehren «Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung.» GEMESSEN an einem echten `initialize` durch build_http_app(): der Satz steht so im Handshake-Resultat. Gleichzeitig gemessen: `hasattr(eth_library_mcp.server, 'eth_search_persons')` ist False, und tests/test_server.py:254-259 verbietet das Werkzeug ausdruecklich («Eine Faehigkeit, die es nicht gibt, darf nicht angeboten werden»). Der Server bewirbt im Handshake genau die Faehigkeit, die sein eigener Test verbietet
- BEFUND src/eth_library_mcp/server.py:713 — `**Version:** 0.3.0` im Rueckgabetext von `eth_library_info`. GEMESSEN an einem tools/call durch build_http_app(): DIESELBE Antwort traegt in `_meta['io.modelcontextprotocol/serverInfo']['version']` den Wert `0.4.0`. Zwei Versionsangaben, eine Antwort, ein Widerspruch. scripts/check_version_sync.py faengt ihn nicht — CI ist gruen
- BEFUND src/eth_library_mcp/server.py:21 — der Modul-Docstring beschreibt «formatting.py — Markdown-Rendering, Persons-Parsing, Error-Mapping». Der HEAD-Commit 32ac730 heisst «refactor: toten Persons-Parser entfernen»; `grep -in person src/eth_library_mcp/formatting.py` liefert 0 Treffer (Gegenkontrolle: dasselbe Muster liefert in server.py 4 Treffer). Die Modulgrenze beschreibt eine Funktion, die es nicht mehr gibt
- BEFUND src/eth_library_mcp/server.py:580 — die Abschnittsueberschrift «TOOL 5: Personen suchen» steht ueber `SearchEducationInput` / `eth_search_education`; die naechste Ueberschrift ist «TOOL 7» (server.py:688). Die Nummerierung und der Titel beschreiben den entfernten Stand
- BEFUND tests/test_tools.py:8-9 — «Run with `pytest -m live` for the (currently absent) live suite.» GEMESSEN: `pytest -m live --collect-only` sammelt zwei Tests ein (tests/test_server.py::TestLiveGatewayRoutes), und README.md:331 datiert ihre Einfuehrung auf 2026-08-08. Zusaetzlich tests/test_tools.py:5 — «against a stubbed Discovery / Persons API response»; Persons-Tests gibt es in der Datei keine
- BEFUND docs/ARCHITECTURE.md:14 und :67, README.md:243, README.de.md:244 — «FastMCP tools, resources, prompts», «FastMCP's structured-output path», «FastMCP-Server, alle Tools». Der Server laeuft auf `mcp.server.mcpserver.MCPServer` (server.py:34); FastMCP ist in mcp 2.0.0 entfallen und `grep -rn 'FastMCP' src/ tests/` liefert 0 Treffer
- BEFUND README.md:53 / README.de.md:53 «Dual transport – stdio for Claude Desktop, Streamable HTTP/SSE for cloud deployment» und README.md:133 / README.de.md:133 «Cloud Deployment (SSE for browser access)». GEMESSEN: `build_http_app().routes` enthaelt genau eine Route, `/mcp`; GET und POST auf `/sse` antworten mit HTTP 404. Eine dokumentierte Faehigkeit, die der Code nicht hat
- Modus 1 gefuehrt, nicht nur gegrept: `[Unreleased]` in CHANGELOG.md ist leer (sed-Auszug zwischen `## [Unreleased]` und `## [0.4.0]` enthaelt keine Zeile) — von dort kommt kein Widerspruch. Modus 2 als Vorsortierung: das Absichtsvokabular findet zwei Stellen, docs/secret-management.md:43 («planned for a future sprint», trifft zu — keine gitleaks-Stufe in ci.yml) und tests/test_tools.py:9 (widerlegt, siehe oben). Gegenkontrolle: dasselbe Muster gegen eine Probedatei mit «noch nicht implementiert» liefert 1 Treffer

### Gaps

- Der Server bewirbt im `initialize`-Handshake eine entfernte Faehigkeit (Personen-Suche). Das ist der teuerste der Befunde: er erreicht jedes Modell bei jeder Verbindung und widerspricht einem Test desselben Repos
- `eth_library_info` meldet Version 0.3.0, waehrend dieselbe Antwort 0.4.0 stempelt; scripts/check_version_sync.py sieht Literale in server.py nicht an
- Vier Doku-Stellen fuehren FastMCP, obwohl die SDK-2.x-Migration abgeschlossen ist — der PR, der die Absicht ausgefuehrt hat, hat die Saetze nicht im selben Diff korrigiert
- README fuehrt SSE als ausgelieferten Transport; gemessen existiert kein SSE-Pfad (siehe SCALE-009)
- Kein Release-Schritt, der `[Unreleased]` liest statt verschiebt — heute folgenlos, weil der Abschnitt leer ist

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/DRIFT-006.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
