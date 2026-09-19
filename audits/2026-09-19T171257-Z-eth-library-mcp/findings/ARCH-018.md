## Finding: ARCH-018 — resultType auf allen Results — «complete» ist kein Default, den man weglässt

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-018
**Katalog-Referenz:** SEP-2322
**Spec-Baseline:** 2026-07-28
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Am Draht GEMESSEN durch build_http_app(), moderne Aera: `resultType: "complete"` liegt auf tools/list, resources/list, resources/templates/list, prompts/list, server/discover, resources/read, prompts/get und tools/call an. Beispiel tools/list, vollstaendige Schluesselmenge des result: ['_meta','cacheScope','resultType','tools','ttlMs'].
- Fehlerpfad GEMESSEN, getrennt vom Erfolgspfad: tools/call auf ein unbekanntes Werkzeug -> {"content":[{"text":"Unknown tool: does_not_exist",...}],"isError":true,"resultType":"complete",...}; tools/call auf eth_get_resource mit einem Argument, das die Pydantic-Validierung verletzt (mmsid="") -> ebenfalls isError true UND resultType "complete". Beide Ergebniswege tragen das Feld.
- Das Feld stammt aus dem SDK, nicht aus diesem Repo: grep -rnE "resultType|result_type" ueber src/ UND tests/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Wort steht in /usr/local/lib/python3.11/dist-packages/mcp_types/_types.py:167/171/221 und in mcp/server/{connection,runner,session}.py — das Muster greift. Installierte und gemessene SDK-Version: mcp 2.2.0.
- SDK-Untergrenze im Manifest gepinnt: pyproject.toml:29 `"mcp[cli]>=2.0.0,<3"`. Der Server fuehrt kein MRTR (kein tasks/*, gemessen: tasks/list -> -32601), `"input_required"` kommt folglich nirgends vor.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-018.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Am Draht GEMESSEN durch build_http_app(), moderne Aera: `resultType: "complete"` liegt auf tools/list, resources/list, resources/templates/list, prompts/list, server/discover, resources/read, prompts/get und tools/call an. Beispiel tools/list, vollstaendige Schluesselmenge des result: ['_meta','cacheScope','resultType','tools','ttlMs'].
- Fehlerpfad GEMESSEN, getrennt vom Erfolgspfad: tools/call auf ein unbekanntes Werkzeug -> {"content":[{"text":"Unknown tool: does_not_exist",...}],"isError":true,"resultType":"complete",...}; tools/call auf eth_get_resource mit einem Argument, das die Pydantic-Validierung verletzt (mmsid="") -> ebenfalls isError true UND resultType "complete". Beide Ergebniswege tragen das Feld.
- Das Feld stammt aus dem SDK, nicht aus diesem Repo: grep -rnE "resultType|result_type" ueber src/ UND tests/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Wort steht in /usr/local/lib/python3.11/dist-packages/mcp_types/_types.py:167/171/221 und in mcp/server/{connection,runner,session}.py — das Muster greift. Installierte und gemessene SDK-Version: mcp 2.2.0.
- SDK-Untergrenze im Manifest gepinnt: pyproject.toml:29 `"mcp[cli]>=2.0.0,<3"`. Der Server fuehrt kein MRTR (kein tasks/*, gemessen: tasks/list -> -32601), `"input_required"` kommt folglich nirgends vor.

### Gaps

- Kein Test prueft `resultType` am tatsaechlichen Wire-Format — grep ueber tests/ findet das Feld gar nicht. Das im Check benannte Kriterium («nicht am Rueckgabewert der Python-Funktion, sondern am Draht») ist unerfuellt; die Konformitaet ruht vollstaendig darauf, dass das SDK das Feld weiterhin setzt, und nichts im Repo meldet den Tag, an dem es das nicht mehr tut. Die vorhandenen Draht-Tests (tests/test_server_identity.py:86-105, tests/test_cache_hints.py) fahren bereits genau den Stack, in dem die Zusicherung stehen muesste.
- Die gepinnte Untergrenze `>=2.0.0` ist nicht nachgemessen: beobachtet ist nur, dass 2.2.0 das Feld setzt.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-018.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
