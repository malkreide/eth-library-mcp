## Finding: SCALE-009 — Legacy HTTP+SSE abgeschaltet — mit Datum, nicht mit Vorsatz

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SCALE-009
**Katalog-Referenz:** SEP-2596
**Spec-Baseline:** beide
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Kein Legacy-Pfad im Code: `grep -rnE 'sse_app|SseServerTransport|/sse|text/event-stream|EventSourceResponse' src/ --include='*.py'` liefert 0 Treffer. Negative Kontrolle: dasselbe Muster gegen das installierte SDK findet mcp/server/sse.py und mcp/server/mcpserver/server.py — es greift also
- GEMESSEN an der zusammengebauten App: `build_http_app().routes` enthaelt genau eine Route, `('/mcp', [])`. Kein zweiter Transportpfad
- GEMESSEN am laufenden Stack: `GET /sse` mit `Accept: text/event-stream` -> HTTP 404; `POST /sse` mit vollstaendigem modernen Envelope -> HTTP 404
- GEGENPROBE gefuehrt (vom Check ausdruecklich verlangt): derselbe Aufruf gegen einen Server MIT offenem SSE-Pfad — `MCPServer('probe').sse_app()` hat die Routen `['/sse', '/messages']`, und `GET /sse` bleibt dort als langlebiger text/event-stream-Strom offen statt 404 zu liefern. Die 404 oben ist damit eine Messung und kein Tippfehler in der URL
- Deployment-Konfiguration ohne Legacy-Route: Dockerfile ENTRYPOINT/CMD ist `python -m eth_library_mcp.server --http --host 0.0.0.0 --port 8000`, server.json:15-18 deklariert `"transport": {"type": "stdio"}`, claude_desktop_config.json startet stdio. Es gibt keine Ingress-/Compose-Datei mit einer /sse-Route (`find . -name 'docker-compose*' -o -name 'ingress*'` leer)
- BEFUND README.md:53 und README.de.md:53 — «Dual transport – stdio for Claude Desktop, Streamable HTTP/SSE for cloud deployment». Dazu README.md:133 und README.de.md:133 als eigener Abschnitt «Cloud Deployment (SSE for browser access)» bzw. «Cloud-Deployment (SSE fuer Browser-Zugriff)». Das README fuehrt SSE als gleichwertigen ausgelieferten Transport, obwohl gemessen keiner existiert

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SCALE-009.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Kein Legacy-Pfad im Code: `grep -rnE 'sse_app|SseServerTransport|/sse|text/event-stream|EventSourceResponse' src/ --include='*.py'` liefert 0 Treffer. Negative Kontrolle: dasselbe Muster gegen das installierte SDK findet mcp/server/sse.py und mcp/server/mcpserver/server.py — es greift also
- GEMESSEN an der zusammengebauten App: `build_http_app().routes` enthaelt genau eine Route, `('/mcp', [])`. Kein zweiter Transportpfad
- GEMESSEN am laufenden Stack: `GET /sse` mit `Accept: text/event-stream` -> HTTP 404; `POST /sse` mit vollstaendigem modernen Envelope -> HTTP 404
- GEGENPROBE gefuehrt (vom Check ausdruecklich verlangt): derselbe Aufruf gegen einen Server MIT offenem SSE-Pfad — `MCPServer('probe').sse_app()` hat die Routen `['/sse', '/messages']`, und `GET /sse` bleibt dort als langlebiger text/event-stream-Strom offen statt 404 zu liefern. Die 404 oben ist damit eine Messung und kein Tippfehler in der URL
- Deployment-Konfiguration ohne Legacy-Route: Dockerfile ENTRYPOINT/CMD ist `python -m eth_library_mcp.server --http --host 0.0.0.0 --port 8000`, server.json:15-18 deklariert `"transport": {"type": "stdio"}`, claude_desktop_config.json startet stdio. Es gibt keine Ingress-/Compose-Datei mit einer /sse-Route (`find . -name 'docker-compose*' -o -name 'ingress*'` leer)
- BEFUND README.md:53 und README.de.md:53 — «Dual transport – stdio for Claude Desktop, Streamable HTTP/SSE for cloud deployment». Dazu README.md:133 und README.de.md:133 als eigener Abschnitt «Cloud Deployment (SSE for browser access)» bzw. «Cloud-Deployment (SSE fuer Browser-Zugriff)». Das README fuehrt SSE als gleichwertigen ausgelieferten Transport, obwohl gemessen keiner existiert

### Gaps

- Das README nennt SSE als unterstuetzten Transport (4 Stellen in beiden Sprachfassungen). Wer danach deployt, sucht einen Endpunkt, den es nicht gibt — und wer den Check spaeter wiederholt, liest die Doku als Beleg fuer einen offenen Legacy-Pfad, den der Code nicht hat. Der Abschnittstitel «Cloud Deployment (SSE …)» beschreibt tatsaechlich Streamable HTTP
- Kein Abschaltdatum im CHANGELOG — hier folgerichtig, weil nichts offen ist, aber damit auch kein Nachweis, wann der Pfad geschlossen wurde
- Gemessen wurde am lokal zusammengebauten ASGI-Stack; eine ausgelieferte HTTP-Instanz existiert nicht (Deployment local-stdio), der Punkt «an der ausgelieferten Instanz geprueft» ist damit so weit erfuellt, wie er hier erfuellbar ist

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SCALE-009.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.
