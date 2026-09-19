## Finding: ARCH-019 — Roots, Sampling und Logging: keine Neuimplementierung, Bestand mit Fristdatum

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-019
**Katalog-Referenz:** SEP-2577
**Spec-Baseline:** beide
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- BEFUND: Der Server nutzt das deprecatete Logging-Protokoll-Feature an fuenf Stellen — src/eth_library_mcp/server.py:326, :386, :476, :575, :680, jeweils `await ctx.warning(...)`. `mcp.server.mcpserver.Context.warning` traegt im SDK den Dekorator @deprecated("The logging capability is deprecated as of 2026-07-28 (SEP-2577).") und leitet auf `Context.log` -> `session.send_log_message` weiter, also auf `notifications/message`. Quelle: inspect.getsource(Context.warning) auf mcp 2.2.0.
- Zur Laufzeit BEOBACHTET, nicht geschlossen: ein Aufruf von eth_get_resource ueber einen echten `mcp.Client` mit auf Raise gepatchtem `_http_get` erzeugte drei Warnungen `MCPDeprecationWarning: The logging capability is deprecated as of 2026-07-28 (SEP-2577).` (warning -> log -> send_log_message). Der Fehlerpfad jedes der fuenf Tools loest das aus.
- Die Modus-1-Greps des Katalogs finden diese Nutzung NICHT: grep -rnE "logging/setLevel|set_level|LoggingCapability|notifications/message" ueber src/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen mcp/server/connection.py trifft (Zeilen 70, 425) — das Muster greift, es kennt nur die Convenience-Wrapper des SDK nicht.
- Roots und Sampling: keine Nutzung. grep -rnE "roots/list|RootsCapability|list_roots|ListRootsRequest" -> 0, grep -rnE "sampling/createMessage|create_message|CreateMessageRequest|samplingCapability" -> 0 (beide exit 1); Negativkontrollen gegen mcp/shared/peer.py:223 bzw. :158 treffen. Laufzeit GEMESSEN: roots/list, sampling/createMessage und logging/setLevel antworten je mit -32601 "Method not found".
- Kriterium 6 erfuellt, gemessen: die von server/discover ausgelieferten capabilities nennen ausschliesslich prompts, resources und tools — keines der drei deprecateten Features wird angekuendigt.
- Kriterium 5 erfuellt: das Anwendungs-Logging liegt unangetastet auf stderr — src/eth_library_mcp/logging_config.py:26-31 `logging.basicConfig(stream=sys.stderr)` und :46 `structlog.PrintLoggerFactory(file=sys.stderr)`, JSON-Renderer. Das ist genau die von der Spec empfohlene Migration und erfuellt weiterhin OBS-003.
- Historie zur Frage «neue Nutzung»: `git log -S"ctx.warning"` nennt genau zwei Commits — 5e37092 (2026-06-04), der die Aufrufe einfuehrte, und 3de3348 (2026-08-08), der ihre Zahl verringerte (Entfernung von eth_search_persons). Seit der Deprecation am 2026-07-28 ist also nichts Neues dazugekommen; eingefuehrt wurden sie allerdings nach dem Vorlauf-Audit vom 28.5.2026.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-019.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- BEFUND: Der Server nutzt das deprecatete Logging-Protokoll-Feature an fuenf Stellen — src/eth_library_mcp/server.py:326, :386, :476, :575, :680, jeweils `await ctx.warning(...)`. `mcp.server.mcpserver.Context.warning` traegt im SDK den Dekorator @deprecated("The logging capability is deprecated as of 2026-07-28 (SEP-2577).") und leitet auf `Context.log` -> `session.send_log_message` weiter, also auf `notifications/message`. Quelle: inspect.getsource(Context.warning) auf mcp 2.2.0.
- Zur Laufzeit BEOBACHTET, nicht geschlossen: ein Aufruf von eth_get_resource ueber einen echten `mcp.Client` mit auf Raise gepatchtem `_http_get` erzeugte drei Warnungen `MCPDeprecationWarning: The logging capability is deprecated as of 2026-07-28 (SEP-2577).` (warning -> log -> send_log_message). Der Fehlerpfad jedes der fuenf Tools loest das aus.
- Die Modus-1-Greps des Katalogs finden diese Nutzung NICHT: grep -rnE "logging/setLevel|set_level|LoggingCapability|notifications/message" ueber src/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen mcp/server/connection.py trifft (Zeilen 70, 425) — das Muster greift, es kennt nur die Convenience-Wrapper des SDK nicht.
- Roots und Sampling: keine Nutzung. grep -rnE "roots/list|RootsCapability|list_roots|ListRootsRequest" -> 0, grep -rnE "sampling/createMessage|create_message|CreateMessageRequest|samplingCapability" -> 0 (beide exit 1); Negativkontrollen gegen mcp/shared/peer.py:223 bzw. :158 treffen. Laufzeit GEMESSEN: roots/list, sampling/createMessage und logging/setLevel antworten je mit -32601 "Method not found".
- Kriterium 6 erfuellt, gemessen: die von server/discover ausgelieferten capabilities nennen ausschliesslich prompts, resources und tools — keines der drei deprecateten Features wird angekuendigt.
- Kriterium 5 erfuellt: das Anwendungs-Logging liegt unangetastet auf stderr — src/eth_library_mcp/logging_config.py:26-31 `logging.basicConfig(stream=sys.stderr)` und :46 `structlog.PrintLoggerFactory(file=sys.stderr)`, JSON-Renderer. Das ist genau die von der Spec empfohlene Migration und erfuellt weiterhin OBS-003.
- Historie zur Frage «neue Nutzung»: `git log -S"ctx.warning"` nennt genau zwei Commits — 5e37092 (2026-06-04), der die Aufrufe einfuehrte, und 3de3348 (2026-08-08), der ihre Zahl verringerte (Entfernung von eth_search_persons). Seit der Deprecation am 2026-07-28 ist also nichts Neues dazugekommen; eingefuehrt wurden sie allerdings nach dem Vorlauf-Audit vom 28.5.2026.

### Gaps

- Kein dokumentiertes Fristdatum und kein Zielzustand: normalisierte Suche (Zeilenumbrueche geglaettet) nach `deprecat|abkuendig|abkuendig|rueckbau|2027-07-28|SEP-2577` ueber README.md, README.de.md und CHANGELOG.md -> 0 Treffer in allen drei Dateien. Negativkontrolle gegen eine Probedatei mit «Logging deprecated, Rueckbau bis 2027-07-28.» trifft. Damit sind die Kriterien 2 (Nutzung benannt mit Zielzustand und Datum), 3 (Datum nicht nach 2027-07-28) und 4 (Zielzustand entspricht der Spec-Empfehlung) unerfuellt — vorhandene Nutzung ohne Datum ist nach dem Check ein Vorsatz, kein Plan.
- Behebung waere klein und ist benannt: die fuenf `ctx.warning`-Aufrufe geben dieselbe Information bereits doppelt aus — `_handle_error` (formatting.py:161) loggt die Ausnahme auf stderr. Der Rueckbau ist damit ein Loeschen, kein Ersetzen; er braucht nur die Entscheidung und ein Datum im CHANGELOG.
- KATALOG-BEFUND: Die Verifikationsgreps dieses Checks koennen die haeufigste Form der Nutzung im Python-SDK nicht sehen. `Context.warning`, `Context.info`, `Context.debug`, `Context.error` und `Context.log` sind das deprecatete Feature, enthalten aber keinen der gesuchten Namen. Ein Server kann das Feature auf fuenf Zeilen nutzen und Modus 1 mit 0 Treffern bestehen — genau der «Grep meldet 0 Treffer, weil das Muster nie greift»-Fall, den der Check selbst in seiner Failure-Tabelle fuehrt.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-019.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
