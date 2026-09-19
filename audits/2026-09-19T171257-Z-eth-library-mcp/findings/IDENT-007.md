## Finding: IDENT-007 — Das veröffentlichte Artefakt startet in einer leeren Umgebung

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** IDENT-007
**Katalog-Referenz:** Custom (Portfolio-Fundstücke zurich-opendata-mcp 0.5.1, 2026-07-31; swiss-energy-mcp, 2026-08-01)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Leere Umgebung, aus dem INDEX installiert: `python -m venv /tmp/verify7` und `/tmp/verify7/bin/pip install --no-cache-dir "eth-library-mcp==0.4.0"` -> exit 0. Kein Checkout, kein Lockfile, kein Constraint aus dem Repo, kein Cache.
- IMPORT: `/tmp/verify7/bin/python -c "import eth_library_mcp; print(eth_library_mcp.__version__)"` -> 'import ok 0.4.0', exit 0.
- AUFGELOESTE KERN-ABHAENGIGKEITEN protokolliert (`pip freeze` im venv, 2026-09-19): mcp==2.2.0, mcp-types==2.2.0, httpx==0.28.1, httpx2==2.13.0, pydantic==2.13.5, pydantic_core==2.46.5, structlog==26.1.0, starlette==1.6.0, uvicorn==0.53.0. Die Deckelung `mcp[cli]>=2.0.0,<3` steht auch in den Index-Metadaten (`requires_dist`), der Resolver bleibt also in 2.x.
- ENTRY POINT startet und beantwortet `initialize`: `/tmp/verify7/bin/eth-library-mcp` ueber stdio -> serverInfo {name: eth_library_mcp, title: 'ETH-Bibliothek Zuerich', version: '0.4.0', description: 'MCP Server for ETH Library Zurich - ...', websiteUrl: 'https://github.com/malkreide/eth-library-mcp'}. `tools/list` -> 6 Werkzeuge (eth_search_resources, eth_get_resource, eth_search_archive, eth_search_by_type, eth_search_education, eth_library_info).
- ECHTER tools/call gegen das installierte Artefakt, stdin bis zur Antwort offen gehalten (der erste Versuch mit einer geschlossenen Pipe bekam keine Antwort — der Prozess fuhr nach 76 ms herunter; das ist die im Check benannte Falle, nicht ein Defekt des Pakets): `tools/call name=eth_library_info` -> `isError: false`, 1722 Zeichen Antworttext. Nicht leer, kein Fehler.
- RELEASE NICHT ZURUECKGEZOGEN: PyPI-Metadaten zu 0.4.0 melden `yanked: false`, `yanked_reason: null`; auch keine der 2 Dateien des Releases ist yanked.
- `TOOL_ERROR` war nicht einschlaegig und musste deshalb nicht gegen eine Egress-Allow-List geprueft werden: der gefahrene Aufruf ist das einzige Werkzeug mit `openWorldHint: False`, das keinen Upstream anspricht.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/IDENT-007.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Leere Umgebung, aus dem INDEX installiert: `python -m venv /tmp/verify7` und `/tmp/verify7/bin/pip install --no-cache-dir "eth-library-mcp==0.4.0"` -> exit 0. Kein Checkout, kein Lockfile, kein Constraint aus dem Repo, kein Cache.
- IMPORT: `/tmp/verify7/bin/python -c "import eth_library_mcp; print(eth_library_mcp.__version__)"` -> 'import ok 0.4.0', exit 0.
- AUFGELOESTE KERN-ABHAENGIGKEITEN protokolliert (`pip freeze` im venv, 2026-09-19): mcp==2.2.0, mcp-types==2.2.0, httpx==0.28.1, httpx2==2.13.0, pydantic==2.13.5, pydantic_core==2.46.5, structlog==26.1.0, starlette==1.6.0, uvicorn==0.53.0. Die Deckelung `mcp[cli]>=2.0.0,<3` steht auch in den Index-Metadaten (`requires_dist`), der Resolver bleibt also in 2.x.
- ENTRY POINT startet und beantwortet `initialize`: `/tmp/verify7/bin/eth-library-mcp` ueber stdio -> serverInfo {name: eth_library_mcp, title: 'ETH-Bibliothek Zuerich', version: '0.4.0', description: 'MCP Server for ETH Library Zurich - ...', websiteUrl: 'https://github.com/malkreide/eth-library-mcp'}. `tools/list` -> 6 Werkzeuge (eth_search_resources, eth_get_resource, eth_search_archive, eth_search_by_type, eth_search_education, eth_library_info).
- ECHTER tools/call gegen das installierte Artefakt, stdin bis zur Antwort offen gehalten (der erste Versuch mit einer geschlossenen Pipe bekam keine Antwort — der Prozess fuhr nach 76 ms herunter; das ist die im Check benannte Falle, nicht ein Defekt des Pakets): `tools/call name=eth_library_info` -> `isError: false`, 1722 Zeichen Antworttext. Nicht leer, kein Fehler.
- RELEASE NICHT ZURUECKGEZOGEN: PyPI-Metadaten zu 0.4.0 melden `yanked: false`, `yanked_reason: null`; auch keine der 2 Dateien des Releases ist yanked.
- `TOOL_ERROR` war nicht einschlaegig und musste deshalb nicht gegen eine Egress-Allow-List geprueft werden: der gefahrene Aufruf ist das einzige Werkzeug mit `openWorldHint: False`, das keinen Upstream anspricht.

### Gaps

- Kein wiederkehrender Lauf prueft das PUBLIZIERTE Paket. Der einzige `schedule:`-Workflow ist .github/workflows/live-tests.yml (taeglich 06:17 UTC), und dessen Install-Schritt lautet `pip install -e ".[dev]"` (Zeile 42) — er prueft den Checkout, also genau das, was die CI schon prueft. Damit ist die Antwort auf diesen Check ein Zeitpunkt (2026-09-19) und kein Zustand: der Vorfall, gegen den er existiert, entsteht ohne Commit.
- Von den 6 Werkzeugen wurde genau eines per `tools/call` gefahren — das einzige ohne Upstream-Aufruf. Die fuenf Discovery-Werkzeuge wurden am Artefakt NICHT ausgeloest, weil Netzzugriffe auf die ETH-API fuer diesen Lauf ausgeschlossen waren und die API ohnehin einen Schluessel verlangt. Der `meteoswiss-mcp`-Fall (Werkzeuge, die listen und nichts liefern) waere damit an diesem Artefakt nicht aufgefallen.
- Am selben, aus dem Index installierten Artefakt gemessen und hier festgehalten, weil es der einzige Ort ist, an dem es sichtbar wird: die Antwort von `eth_library_info` traegt '**Version:** 0.3.0' (Befund unter IDENT-002), und die `instructions` im `initialize` bewerben weiterhin 'Personen-Suche mit Wikidata-Verlinkung' fuer ein Werkzeug, das 0.4.0 entfernt hat. Beides macht das Artefakt nicht funktionsunfaehig und ist deshalb kein Verstoss gegen die Kriterien dieses Checks.
- Geprueft wurde die Wheel-Variante; ein sdist-Build wurde nicht gesondert installiert und gestartet.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/IDENT-007.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.
