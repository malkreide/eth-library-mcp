## Finding: ARCH-016 — server/discover ist implementiert — der RPC ist MUSS, nicht Kür

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-016
**Katalog-Referenz:** SEP-2575
**Spec-Baseline:** 2026-07-28
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Streamable HTTP GEMESSEN durch build_http_app(): `server/discover` antwortet mit allen DREI Bestandteilen — supportedVersions: ["2026-07-28"] (Liste, kein String), capabilities: {prompts:{listChanged},resources:{listChanged,subscribe},tools:{listChanged}}, und Identitaet in _meta["io.modelcontextprotocol/serverInfo"] = {name: "eth_library_mcp", title: "ETH-Bibliothek Zuerich", version: "0.4.0", description, websiteUrl}.
- stdio GEMESSEN (ARCH-013-Kriterium «ueber jeden bedienten Transportpfad»): derselbe JSON-RPC-Request ueber `mcp.run()` als Subprozess (PYTHONPATH=src, stdin/stdout) lieferte ein inhaltlich identisches Resultat, inklusive supportedVersions, capabilities und serverInfo-Stempel. Beide Pfade bedienen den RPC.
- Die Version im Stempel stammt aus den Paket-Metadaten, nicht aus einem Literal: src/eth_library_mcp/__init__.py:15 `__version__ = _distribution_version("eth-library-mcp")`, server.py:172 `version=__version__`; gemessener Wert 0.4.0 == importlib.metadata.version('eth-library-mcp'). tests/test_server_identity.py:157 vergleicht genau dagegen statt gegen eine Zahl.
- Der RPC stammt aus dem SDK, nicht aus diesem Repo: grep -rnE "server/discover|server_discover|def discover|DiscoverResult" ueber src/ trifft nur server.py:144, und das ist ein Cache-Hint-Schluessel, kein Handler. SDK-Untergrenze gepinnt in pyproject.toml:29 `mcp[cli]>=2.0.0,<3`; installiert und gemessen: mcp 2.2.0.
- Negativkontrolle der Laufzeitsonde: `server/discoverX` durch denselben Stack -> HTTP 404 mit {"code": -32601, "message": "Method not found"}. Die Sonde unterscheidet also einen bedienten von einem unbekannten RPC; das gemessene 200 auf server/discover ist ein positiver Beleg und kein Artefakt.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-016.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Streamable HTTP GEMESSEN durch build_http_app(): `server/discover` antwortet mit allen DREI Bestandteilen — supportedVersions: ["2026-07-28"] (Liste, kein String), capabilities: {prompts:{listChanged},resources:{listChanged,subscribe},tools:{listChanged}}, und Identitaet in _meta["io.modelcontextprotocol/serverInfo"] = {name: "eth_library_mcp", title: "ETH-Bibliothek Zuerich", version: "0.4.0", description, websiteUrl}.
- stdio GEMESSEN (ARCH-013-Kriterium «ueber jeden bedienten Transportpfad»): derselbe JSON-RPC-Request ueber `mcp.run()` als Subprozess (PYTHONPATH=src, stdin/stdout) lieferte ein inhaltlich identisches Resultat, inklusive supportedVersions, capabilities und serverInfo-Stempel. Beide Pfade bedienen den RPC.
- Die Version im Stempel stammt aus den Paket-Metadaten, nicht aus einem Literal: src/eth_library_mcp/__init__.py:15 `__version__ = _distribution_version("eth-library-mcp")`, server.py:172 `version=__version__`; gemessener Wert 0.4.0 == importlib.metadata.version('eth-library-mcp'). tests/test_server_identity.py:157 vergleicht genau dagegen statt gegen eine Zahl.
- Der RPC stammt aus dem SDK, nicht aus diesem Repo: grep -rnE "server/discover|server_discover|def discover|DiscoverResult" ueber src/ trifft nur server.py:144, und das ist ein Cache-Hint-Schluessel, kein Handler. SDK-Untergrenze gepinnt in pyproject.toml:29 `mcp[cli]>=2.0.0,<3`; installiert und gemessen: mcp 2.2.0.
- Negativkontrolle der Laufzeitsonde: `server/discoverX` durch denselben Stack -> HTTP 404 mit {"code": -32601, "message": "Method not found"}. Die Sonde unterscheidet also einen bedienten von einem unbekannten RPC; das gemessene 200 auf server/discover ist ein positiver Beleg und kein Artefakt.

### Gaps

- Kein Test prueft die drei Bestandteile einzeln. Die einzige Zusicherung auf server/discover ist tests/test_server_identity.py:152-157 und prueft ausschliesslich `info.get("version")`; supportedVersions und capabilities sind von keinem Test beruehrt (grep "server/discover" ueber tests/ findet nur diese Stelle plus zwei Docstring-Zeilen). Kriterium «Ein Test ... prueft alle drei Bestandteile einzeln» unerfuellt.
- Keine Gegenprobe gegen einen Server OHNE den Handler. tests/test_server_identity.py:203-234 ist eine Gegenprobe fuer den Versionsstempel (MCPServer ohne `version=`), nicht fuer die Existenz des RPC. Kriterium 7 unerfuellt.
- Die gepinnte Untergrenze ist nicht nachgemessen: beobachtet ist nur, dass mcp 2.2.0 den RPC fuehrt. Ob `>=2.0.0` ihn bereits enthaelt, wurde nicht geprueft (kein Netzzugriff auf den Index); die Konformitaet haengt insoweit an der zufaellig installierten Version.
- Nebenbefund ausserhalb dieses Checks, weil von diesem RPC ausgeliefert: die gemessenen `instructions` (server.py:180) werben weiterhin mit «Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung» — ein Werkzeug, das in 0.4.0 entfernt wurde. Gehoert zu IDENT/FID.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-016.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.
