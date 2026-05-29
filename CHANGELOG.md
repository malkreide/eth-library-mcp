# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier dokumentiert.
Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

---

## [0.3.0] – 2026-05-29

Audit-Härtungs-Release. Über drei Remediation-Sprints wurden alle 20 Findings aus dem [mcp-audit-skill](https://github.com/malkreide/mcp-audit-skill)-Audit (run-id `2026-05-28T142641-Z-eth-library-mcp`, 38/68 Checks anwendbar) behoben. Ein Re-Audit (run-id `2026-05-28T184347-Z-eth-library-mcp`, identischer Catalog-Hash `091f446b…`) bestätigt: 36/36 anwendbare Checks PASS, 0 Findings, Production-Readiness erreicht.

### ⚠️ Breaking Changes

- **HTTP-Default-Bind** (`SEC-016`): `python -m eth_library_mcp.server --http` bindet jetzt auf `127.0.0.1` statt `0.0.0.0`. Für Public-Exposure muss `--host 0.0.0.0` explizit übergeben werden — und nur hinter Reverse-Proxy/Firewall. Migration: bestehende Deploy-Skripte um `--host 0.0.0.0` ergänzen oder hinter den Proxy verlagern.

### Hinzugefügt

- **Container-Sandbox** (`SEC-007`): `Dockerfile` (multi-stage, slim-base, non-root UID 1000) + `.dockerignore`. Empfohlene Laufzeit: `--read-only --tmpfs /tmp`.
- **Egress-Allow-List** (`SEC-021`): `ALLOWED_EGRESS_HOSTS` als `frozenset` mit Runtime-Gate in `_http_get`. Jeder Outbound-Call gegen einen nicht gelisteten Host wirft `PermissionError`. Doku: `docs/network-egress.md`.
- **CORS-Middleware** (`SDK-004`): HTTP-Transport wrappt die Starlette-App in `CORSMiddleware`. `Mcp-Session-Id` ist in `allow_headers` und `expose_headers` — Browser-MCP-Clients können den Header lesen.
- **Strukturiertes Logging** (`OBS-003`): `structlog` mit JSON-Output auf stderr. Vier Severity-Stufen aktiv genutzt (debug/info/warning/error). Ingestion via Datadog/CloudWatch/Loki ohne Custom-Parser möglich.
- **FastMCP Lifespan + Connection Pool** (`SDK-001`): `@asynccontextmanager`-Lifespan verwaltet einen geteilten `httpx.AsyncClient`. Spart TLS-Handshake pro Tool-Call.
- **Context-Injection** (`SDK-003`): Alle 6 Such-/Get-Tools akzeptieren `ctx: Context`. `ctx.warning()` auf Error-Pfaden, `ctx.report_progress()` für `limit > 50`, `ctx.info()` für Persons-No-Results.
- **Source-Attribution** (`CH-004`): Jede formatierte Ressource trägt eine `Quelle: ETH-Bibliothek (Public Domain) · …`-Zeile.
- **Tool-Layer-Tests** (`OPS-001`): `tests/test_tools.py` mit `respx`-Mocks deckt alle 7 Tools ab (13 neue Tests, 38 total). Regression-Tests für OBS-002 (kein Body-Leak) und SEC-021 (Egress-Block).
- **Stderr-Logging explizit** (`OBS-004`): `logging.basicConfig(stream=sys.stderr)` + `structlog.PrintLoggerFactory(file=sys.stderr)`. stdio JSON-RPC-stdout bleibt sauber.
- **Doku**: `docs/ARCHITECTURE.md`, `docs/data-sources.md`, `docs/network-egress.md`, `docs/scope-minimization.md`, `docs/secret-management.md`.
- **`.gitignore`** und **`.env.example`** (`ARCH-005`): Verhindert versehentliche Secret-Commits.
- **Audit-Artefakte** unter `audits/`: Profil, Verification-Results, Summary, Findings, Reports beider Audit-Läufe.

### Geändert

- **Modul-Split** (`ARCH-004`): `server.py` (1107 LOC) aufgeteilt in `client.py` (httpx + Lifespan + Egress), `formatting.py` (Markdown-Rendering, Error-Mapping), `logging_config.py` (structlog) und `server.py` (898 LOC — nur noch FastMCP-Tools). `server.py` re-exportiert die alten Namen — Import-Pfade bleiben kompatibel.
- **Error-Handling** (`OBS-002`): `_handle_error` leakt keinen Upstream-Response-Body (`e.response.text`) und keinen Exception-Klassennamen mehr an den LLM. Details landen im strukturierten stderr-Log.
- **Versionspinning** (`ARCH-012`): Upper Bounds auf alle Dependencies (`mcp[cli]>=1.0.0,<2.0.0`, `httpx>=0.27.0,<1.0.0`, `pydantic>=2.0.0,<3.0.0`).
- **README**: MCP Protocol Version 2025-06-18 deklariert; Cloud-Deployment-Sektion mit `--host`-Warnung erweitert.

### Sicherheit

| Audit-Check | Vorher | Jetzt |
|---|---|---|
| critical findings | 3 | 0 |
| high findings | 12 | 0 |
| medium findings | 5 | 0 |
| Production-readiness | nein | **ja** |

Vollständige Reports unter `audits/2026-05-28T184347-Z-eth-library-mcp/audit-report.md`.

### Dependencies

- **+** `structlog>=24.0.0,<26.0.0`

---

## [0.2.0] – 2026-03-04

### Behoben
- **BUG-01** `pyproject.toml`: Falscher Package-Pfad `src/eth_library_mcp` → `eth_library_mcp` (Installation via `pip install -e .` schlug fehl)
- **BUG-03** `sort`-Parameter: Beliebige Strings akzeptiert → `Literal["rank","title","author","date"]` (verhindert ungültige API-Anfragen)
- **BUG-04** `resource_type`-Parameter: Beliebige Strings akzeptiert → vollständiger `Literal`-Typ mit allen 10 gültigen Werten (verhindert stille Leerantworten)
- **BUG-06** Persons-Response-Parsing: Nur `persons`/`results`-Keys unterstützt → robustes Parsing mit `data`, `items`, `hits` + Logging bei unbekannter Struktur
- **BUG-07** HTTP-404-Fehlermeldung: Generische "ID prüfen"-Meldung auch bei Suchen → kontext-spezifische Meldungen (`is_search`-Parameter in `handle_api_error`)

### Entfernt
- **BUG-05** Ungenutzte Konstanten `RESEARCH_BASE_URL` und `ETHORAMA_BASE_URL` aus `api_client.py` entfernt

### Bekannte Probleme
- **BUG-02** Persons-API-Endpunkt (`/persons/v1/persons`) gibt HTTP 404 zurück. Die korrekte URL muss via [developer.library.ethz.ch](https://developer.library.ethz.ch) verifiziert werden. Das Tool `eth_search_persons` ist strukturell korrekt implementiert, aber erst nach URL-Verifikation funktionsfähig.

---

## [0.1.0] – 2026-03-01

### Hinzugefügt
- Initiale Implementierung mit 7 Tools, 3 APIs, 2 Resources, 2 Prompts
- Discovery API: `eth_search_resources`, `eth_get_resource`, `eth_search_archive`, `eth_search_by_type`, `eth_search_education`
- Persons API: `eth_search_persons`
- Dual Transport: stdio (lokal) + SSE (Cloud/Render.com)
- Graceful Degradation ohne API-Key (hilfreiche Fehlermeldung mit Registrierungslink)
- Schulamt-spezifisches Tool `eth_search_education` für Bildungsthemen
