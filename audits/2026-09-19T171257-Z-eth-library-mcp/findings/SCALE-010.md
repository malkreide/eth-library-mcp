## Finding: SCALE-010 — subscriptions/listen statt GET-Endpunkt und resources/subscribe

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SCALE-010
**Katalog-Referenz:** SEP-2575
**Spec-Baseline:** 2026-07-28
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Kein alter Abonnementmechanismus im Code: `grep -rnE 'resources/(un)?subscribe|resource_subscribe|handle_get' src/ --include='*.py'` liefert 0 Treffer; ebenso 0 fuer die neuen Bezeichner `subscriptions/listen|subscriptionId|toolsListChanged|resourcesListChanged`. Negative Kontrolle: dasselbe Muster gegen das SDK liefert Treffer (u. a. mcp/server/connection.py) — das Muster greift
- GEMESSEN am `initialize`-Resultat durch build_http_app(): `capabilities = {"experimental": {}, "prompts": {"listChanged": false}, "resources": {"listChanged": false, "subscribe": false}, "tools": {"listChanged": false}}`. Der Server erklaert maschinenlesbar, dass er weder Aenderungsbenachrichtigungen noch Ressourcen-Abonnements fuehrt — das ist staerker als ein Satz Prosa, aber es steht nirgends auch in der Doku
- Request-bezogene Benachrichtigungen bleiben, wo sie hingehoeren: src/eth_library_mcp/server.py:289 ruft `ctx.report_progress(0, params.limit, 'Suche laeuft')`. GEMESSEN durch einen echten tools/call (limit=60): `Context.report_progress` wurde mit `(0, 60, 'Suche laeuft')` aufgerufen. Nichts davon laeuft ueber einen Abonnementstrom; `grep -rn 'subscriptions/listen' src/` ist leer
- BEFUND, gemessen: `GET /mcp` wird weiterhin bedient. Ohne Session-ID antwortet der Server HTTP 400 `{"code": -32600, "message": "Bad Request: Missing session ID"}`; MIT gueltiger `Mcp-Session-Id` (aus einem `initialize`) bleibt die Anfrage nach 5 s ohne Antwort offen — der serverinitiierte Strom ist da. Der vom Check verlangte 405 kommt in keinem der beiden Faelle
- src/eth_library_mcp/server.py:829 — `CORS_ALLOW_METHODS = ["GET", "POST", "DELETE", "OPTIONS"]`. Der GET-Pfad ist nicht bloss ein SDK-Rest, er ist am Endpunkt ausdruecklich freigegeben. Zur Gegenkontrolle mitgemessen: `DELETE /mcp` mit Session-ID -> HTTP 200, die Freigabeliste wirkt also

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SCALE-010.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Kein alter Abonnementmechanismus im Code: `grep -rnE 'resources/(un)?subscribe|resource_subscribe|handle_get' src/ --include='*.py'` liefert 0 Treffer; ebenso 0 fuer die neuen Bezeichner `subscriptions/listen|subscriptionId|toolsListChanged|resourcesListChanged`. Negative Kontrolle: dasselbe Muster gegen das SDK liefert Treffer (u. a. mcp/server/connection.py) — das Muster greift
- GEMESSEN am `initialize`-Resultat durch build_http_app(): `capabilities = {"experimental": {}, "prompts": {"listChanged": false}, "resources": {"listChanged": false, "subscribe": false}, "tools": {"listChanged": false}}`. Der Server erklaert maschinenlesbar, dass er weder Aenderungsbenachrichtigungen noch Ressourcen-Abonnements fuehrt — das ist staerker als ein Satz Prosa, aber es steht nirgends auch in der Doku
- Request-bezogene Benachrichtigungen bleiben, wo sie hingehoeren: src/eth_library_mcp/server.py:289 ruft `ctx.report_progress(0, params.limit, 'Suche laeuft')`. GEMESSEN durch einen echten tools/call (limit=60): `Context.report_progress` wurde mit `(0, 60, 'Suche laeuft')` aufgerufen. Nichts davon laeuft ueber einen Abonnementstrom; `grep -rn 'subscriptions/listen' src/` ist leer
- BEFUND, gemessen: `GET /mcp` wird weiterhin bedient. Ohne Session-ID antwortet der Server HTTP 400 `{"code": -32600, "message": "Bad Request: Missing session ID"}`; MIT gueltiger `Mcp-Session-Id` (aus einem `initialize`) bleibt die Anfrage nach 5 s ohne Antwort offen — der serverinitiierte Strom ist da. Der vom Check verlangte 405 kommt in keinem der beiden Faelle
- src/eth_library_mcp/server.py:829 — `CORS_ALLOW_METHODS = ["GET", "POST", "DELETE", "OPTIONS"]`. Der GET-Pfad ist nicht bloss ein SDK-Rest, er ist am Endpunkt ausdruecklich freigegeben. Zur Gegenkontrolle mitgemessen: `DELETE /mcp` mit Session-ID -> HTTP 200, die Freigabeliste wirkt also

### Gaps

- Ein GET auf /mcp antwortet nicht mit 405: mit gueltiger Session-ID oeffnet sich der serverinitiierte Strom, den Spec 2026-07-28 (SEP-2575) gestrichen hat. Ursache ist das SDK bzw. der bewusst weiterbediente Legacy-Handshake beider Epochen — der Befund bleibt, weil der Server auf der 2026-07-28-Baseline gefuehrt wird
- Weder README noch CONTRIBUTING sagen mit einem Satz, dass dieser Server keine Aenderungsbenachrichtigungen fuehrt. Belegt ist es nur ueber die `capabilities` im Handshake — wer die Doku liest, erfaehrt es nicht
- Kein Test, der festhaelt, dass `notifications/progress` auf dem Antwortstrom seines Requests laeuft und nicht anderswo; die Messung stammt aus diesem Audit, nicht aus der Suite
- `ctx.report_progress` wird nur ein einziges Mal mit progress=0 aufgerufen und nie fortgeschrieben — gemessen kam im Antwortstrom kein `notifications/progress` an (der Client hatte keinen progressToken gesetzt). Der Fortschrittspfad ist damit vorhanden, aber unbelegt in Betrieb

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SCALE-010.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
