# MCP-Server Audit-Report — `eth-library-mcp`

**Audit-Datum:** 
**Skill-Version:** 0.5.0
**Catalog-Version:** ?

---

## 1. Executive Summary

Server `eth-library-mcp` wurde gegen 36 anwendbare Best-Practice-Checks geprüft. 16 bestanden, 20 Findings dokumentiert (3 critical, 12 high, 5 medium, 0 low). Production-Readiness: NICHT erreicht — blockierend: OBS-002, SCALE-002, SDK-001, SDK-004, SEC-007, SEC-016, SEC-021.

**Production-Readiness:** NO

---

## 2. Profil-Snapshot

| Feld | Wert |
|---|---|
| Server-Name | `eth-library-mcp` |
| Audit-Datum | ? |
| Skill-Version | 0.5.0 |
| Catalog-Version | ? |
| transport | `dual` |
| auth_model | `API-Key` |
| data_class | `Public Open Data` |
| write_capable | `False` |
| deployment | `['local-stdio']` |
| uses_sampling | `False` |
| tools_make_external_requests | `True` |
| stadt_zuerich_context | `False` |
| schulamt_context | `False` |
| data_source.is_swiss_open_data | `True` |

---

## 3. Applicability

### Status pro Kategorie

| Kategorie | Pass | Fail | Partial | Todo | N/A |
|---|---|---|---|---|---|
| ARCH | 7 | 0 | 4 | 0 | 0 |
| CH | 0 | 0 | 1 | 0 | 0 |
| OBS | 1 | 2 | 1 | 0 | 0 |
| OPS | 2 | 0 | 1 | 0 | 0 |
| SCALE | 0 | 1 | 0 | 0 | 0 |
| SDK | 0 | 3 | 1 | 0 | 0 |
| SEC | 6 | 3 | 3 | 0 | 2 |
| **Total** | **16** | **9** | **11** | **0** | **2** |

---

## 4. Findings-Übersicht

_Policy: `fail-or-partial`_

| ID | Category | Severity | Status |
|---|---|---|---|
| ARCH-005 | ARCH | critical | partial |
| OBS-004 | OBS | critical | partial |
| SEC-016 | SEC | critical | fail |
| ARCH-004 | ARCH | high | partial |
| ARCH-006 | ARCH | high | partial |
| OBS-002 | OBS | high | fail |
| OPS-001 | OPS | high | partial |
| SCALE-002 | SCALE | high | fail |
| SDK-001 | SDK | high | fail |
| SDK-004 | SDK | high | fail |
| SEC-003 | SEC | high | partial |
| SEC-005 | SEC | high | partial |
| SEC-007 | SEC | high | fail |
| SEC-013 | SEC | high | partial |
| SEC-021 | SEC | high | fail |
| ARCH-012 | ARCH | medium | partial |
| CH-004 | CH | medium | partial |
| OBS-003 | OBS | medium | fail |
| SDK-002 | SDK | medium | partial |
| SDK-003 | SDK | medium | fail |

**Gesamt:** 20 Findings

---

## 5. Detail-Findings

### ARCH-004

## Finding: ARCH-004 — Inversion of Control: Transport-agnostische Server-Logik

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `ARCH-004` |
| **PDF-Reference** | Sec 2.1 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- Tools are decorated at module level; FastMCP separates transport from tool logic (FastMCP framework choice satisfies IoC partially)
- Transport choice handled via CLI flag --http in __main__ (server.py:1100-1107)

### Gaps

- All tool functions live in a single 1107-line server.py — no separation of tool-layer / api-client / formatting layers
- HTTP client (_http_get) is module-private and not injectable for testing — couples transport-agnostic logic to httpx instantiation

### Reference

See `checks/ARCH-004.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### ARCH-005

## Finding: ARCH-005 — Keine Hardcoded Secrets: Env-Vars / Secret Manager only

| Feld | Wert |
|---|---|
| **Severity** | critical |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `ARCH-005` |
| **PDF-Reference** | Sec 2.1 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- No hardcoded API keys, passwords, or tokens in src/ (grep for secret patterns returns 0 hits)
- API key loaded from environment via os.environ.get('ETH_LIBRARY_API_KEY') (server.py:101, server.py:982)
- No default fallback secret in os.environ.get(..., default=...) calls
- No api_key value is logged anywhere

### Gaps

- CRITICAL: .gitignore is MISSING from the repository — a developer who creates .env locally risks committing it
- No .env.example file with placeholders
- No CI secret-scanning workflow (gitleaks/trufflehog) — CI runs only ruff + pytest
- No Pydantic-Settings / SecretStr wrapper around the api key — it lives as a plain str in memory
- No pre-commit hook configuration

### Reference

See `checks/ARCH-005.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### ARCH-006

## Finding: ARCH-006 — Tool-Budget: High-Level-Use-Cases statt API-Mapping 1:1

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `ARCH-006` |
| **PDF-Reference** | Sec 2.3 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- 7 tools total — under the typical budget of 10–15
- Tools organized around use cases (search_education for school context, library_info as entry point)

### Gaps

- eth_search_resources, eth_search_archive, eth_search_by_type and eth_search_education all wrap the same Discovery API endpoint with different facet filters — they could be a single tool with optional facet parameters
- eth_search_education is essentially eth_search_resources with sort=rank and a fixed query template — boundary between them is fuzzy

### Reference

See `checks/ARCH-006.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### ARCH-012

## Finding: ARCH-012 — protocolVersion-Pinning + CHANGELOG + SDK-Update-Disziplin

| Feld | Wert |
|---|---|
| **Severity** | medium |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `ARCH-012` |
| **PDF-Reference** | Anhang A9 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- CHANGELOG.md exists in Keep-a-Changelog format with versioned entries (0.1.0, 0.2.0)
- Version bumps documented
- MCP SDK dependency declared: mcp[cli]>=1.0.0

### Gaps

- MCP SDK pinned only with lower bound (>=1.0.0) — no upper bound or explicit protocolVersion pin against the 2025-06-18 spec
- No documentation in README/CHANGELOG of which MCP protocol version this server targets
- httpx/pydantic dependencies use lower-bound only, exposing CI to silent breakage on major bumps

### Reference

See `checks/ARCH-012.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### CH-004

## Finding: CH-004 — OGD-CH Lizenz-Compliance: CC BY 4.0 Attribution

| Feld | Wert |
|---|---|
| **Severity** | medium |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `CH-004` |
| **PDF-Reference** | Custom (OGD-CH-Richtlinien) |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- README documents the data source ('ETH Library Zurich, Discovery + Persons APIs', README.md:259)
- README documents license: bibliographic metadata as Public Domain (README.md:280)
- Safety & Limits section names data source and ToS link (README.md:259)

### Gaps

- Tool responses do NOT include a per-result 'source' field with provenance (e.g. 'Source: ETH Library, Public Domain')
- Aggregated formatting (_format_resource_summary, _format_resource_detail) drops the canonical source attribution from the API response
- No docs/data-sources.md inventory listing the four linked-data sources (Wikidata, Metagrid, DNB, beacon.findbuch) cited in code

### Reference

See `checks/CH-004.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### OBS-002

## Finding: OBS-002 — Mask Error Details: keine Stacktraces / SQL ans LLM

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `OBS-002` |
| **PDF-Reference** | Sec 6.2 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- FastMCP server constructed without mask_error_details (server.py:290-303)

### Gaps

- FAIL: _handle_error leaks upstream response body to the LLM: 'HTTP-Fehler {status}: {e.response.text[:200]}' (server.py:280) — bug pages / proxy errors / stack traces could surface
- FAIL: Generic Exception branch returns 'type(e).__name__: {e}' (server.py:285), exposing internal exception class names and Python error strings to the LLM
- No mask_error_details=True on FastMCP init

### Reference

See `checks/OBS-002.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### OBS-003

## Finding: OBS-003 — Structured Logging mit RFC 5424 Severity-Stufen

| Feld | Wert |
|---|---|
| **Severity** | medium |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `OBS-003` |
| **PDF-Reference** | Sec 6.3 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- logging.getLogger(__name__) used (server.py:30) — stdlib logging, not structlog/loguru
- Only one logger.warning() call in the entire server (server.py:233)

### Gaps

- No structured logger (structlog/loguru) in dependencies
- No JSON/logfmt output configuration
- Only WARNING severity is actually used — DEBUG/INFO/ERROR are absent
- No log fields for request_id, tool_name, user_session — impossible to correlate across an MCP session

### Reference

See `checks/OBS-003.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### OBS-004

## Finding: OBS-004 — stderr für stdio-Server: stdout reserviert für Protocol

| Feld | Wert |
|---|---|
| **Severity** | critical |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `OBS-004` |
| **PDF-Reference** | Sec 6.3 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- FastMCP framework handles stdio protocol routing — by default it sends logs to stderr, not stdout
- Only one explicit log statement in code (logger.warning) — low risk of stdout pollution
- No print() statements found in src/eth_library_mcp/

### Gaps

- No explicit logging.basicConfig(stream=sys.stderr) call — relies on FastMCP defaults and Python's root-logger default (which is stderr)
- If a downstream consumer adds a handler to logger without specifying stream, accidental stdout writes could corrupt the JSON-RPC protocol
- Not documented in README that stdio transport requires stderr-only logging

### Reference

See `checks/OBS-004.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### OPS-001

## Finding: OPS-001 — Test-Strategie: Unit-Tests mocked + Live-Tests gemarkert

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `OPS-001` |
| **PDF-Reference** | Anhang C1 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- tests/test_server.py contains 25 test functions
- pytest markers include 'live' for live-API tests (pyproject.toml)
- CI runs 'pytest -m "not live"' so live tests are gated (workflows/ci.yml)
- Matrix tested on Python 3.11/3.12/3.13

### Gaps

- respx is declared in [dev] dependencies BUT not actually used anywhere in tests/ — no HTTP mocking of httpx calls
- Tests cover only pure-Python helpers (_first, _format_resource_summary, _parse_persons_response, _handle_error, input validation) — none of the 7 actual @mcp.tool functions are exercised
- No tests with @pytest.mark.live markers found in test_server.py — the marker is declared but never used
- Coverage of the tool layer is effectively 0%

### Reference

See `checks/OPS-001.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SCALE-002

## Finding: SCALE-002 — Stateful Load Balancing für Streamable HTTP / SSE

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SCALE-002` |
| **PDF-Reference** | Sec 5.2 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- Server supports streamable-http transport (server.py:1105) — SCALE-002 applies

### Gaps

- FAIL: No sticky-session config, no session-store backend (Redis/Durable Objects), no reference to Mcp-Session-Id handling
- If deployed behind a multi-replica load balancer, session affinity will break silently
- README cloud-deployment section does not warn that LB must pin on Mcp-Session-Id

### Reference

See `checks/SCALE-002.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SDK-001

## Finding: SDK-001 — FastMCP Lifespan via @asynccontextmanager + AsyncExitStack

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SDK-001` |
| **PDF-Reference** | Sec 3.1 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- FastMCP instance created at module level without lifespan parameter (server.py:290-303)

### Gaps

- FAIL: No @asynccontextmanager lifespan defined — httpx.AsyncClient is constructed and torn down on EVERY tool call (server.py:121)
- Per-call client construction defeats httpx connection pooling and forces a fresh TCP+TLS handshake per request → measurable latency penalty, especially on slow networks
- No AsyncExitStack pattern — if future external clients are added, there's no cleanup path

### Reference

See `checks/SDK-001.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SDK-002

## Finding: SDK-002 — Pydantic v2 / TypedDict / Dataclass als Tool-Returns

| Feld | Wert |
|---|---|
| **Severity** | medium |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SDK-002` |
| **PDF-Reference** | Sec 3.1 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- All 6 input models inherit from pydantic BaseModel with model_config = ConfigDict(str_strip_whitespace=True, extra='forbid') (server.py:314,463,535,642,755,851)
- Literal types used for sort/resource_type/archive parameters (server.py:43-64)

### Gaps

- Tool RETURN type is plain str (Markdown) for all 7 tools — no structured dataclass or TypedDict on the output side
- Downstream LLMs cannot parse structured fields out of formatted Markdown without re-parsing — defeats the FastMCP structured-output capability

### Reference

See `checks/SDK-002.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SDK-003

## Finding: SDK-003 — Context Injection für Progress Reports und Logging

| Feld | Wert |
|---|---|
| **Severity** | medium |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SDK-003` |
| **PDF-Reference** | Sec 3.1 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- No mcp.server.fastmcp.Context type imported, no Context parameter in any tool signature

### Gaps

- FAIL: No Context injection — long-running searches (e.g. limit=100) have no progress reports
- FAIL: Errors are silently masked into return-strings rather than emitted via ctx.warning() / ctx.error() — observability blind spot
- Persons-API unknown-structure warning uses stdlib logger only, not Context

### Reference

See `checks/SDK-003.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SDK-004

## Finding: SDK-004 — CORS Mcp-Session-Id Exposure bei HTTP/SSE

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SDK-004` |
| **PDF-Reference** | Sec 3.1 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- Server supports HTTP transport (server.py:1105) — SDK-004 applies

### Gaps

- FAIL: No CORS middleware is installed or configured
- FAIL: Mcp-Session-Id is neither in expose_headers nor allow_headers — browser-based MCP clients cannot read the session id from the response
- Cloud-deployment section in README does not document the CORS requirement

### Reference

See `checks/SDK-004.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SEC-003

## Finding: SEC-003 — Progressive Scope-Minimierung: Least-Privilege-Modell

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SEC-003` |
| **PDF-Reference** | Sec 4.3 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- Server uses a single ETH_LIBRARY_API_KEY for all upstream calls — operator-controlled credential, not user-delegated
- All tools are read-only against Public Open Data — the surface that 'privilege' could be reduced over is small

### Gaps

- The same key is used for every endpoint (Discovery + Persons). ETH Library may offer scoped keys per API — not investigated or documented
- No documentation in docs/ on how to request a minimum-scope key from developer.library.ethz.ch

### Reference

See `checks/SEC-003.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SEC-005

## Finding: SEC-005 — DNS-Rebinding-Prevention: DNS-Pinning gegen TOCTOU

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SEC-005` |
| **PDF-Reference** | Sec 4.4 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- Server-controlled hostnames (api.library.ethz.ch) — DNS-rebinding attack would require compromising the ETH DNS or user network

### Gaps

- No DNS-pinning / IP-pinning configured in the httpx.AsyncClient (server.py:121)
- If a future feature adds tool-supplied URLs (currently none), DNS-rebinding becomes immediately exploitable
- Risk is low today because no user-supplied URL ever reaches the HTTP client — but the defensive layer is absent

### Reference

See `checks/SEC-005.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SEC-007

## Finding: SEC-007 — Container-Sandboxing: Docker / chroot mit minimalen Privilegien

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SEC-007` |
| **PDF-Reference** | Sec 4.5 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- No Dockerfile present in the repository
- No docker-compose.yml present

### Gaps

- FAIL: No container image — operators running the HTTP transport must install Python locally and run as a regular user, with no sandbox boundary
- FAIL: No documented sandboxing pattern (chroot, systemd-nspawn, firejail, WASM)
- Streamable-HTTP deployment path therefore inherits whatever privileges the host process has

### Reference

See `checks/SEC-007.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SEC-013

## Finding: SEC-013 — API-Key-Storage: Secret Manager statt Plain-Text Env-Vars

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SEC-013` |
| **PDF-Reference** | Sec 4 (Empirie 2025) |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- Data class is Public Open Data — SEC-013 explicitly allows Stage 1 (plain env-var) for this class
- API key is loaded from env, not hardcoded (server.py:101)

### Gaps

- No docs/secret-management.md documenting the Stage-1 choice and the migration path to Stage 3 if scope changes
- No 'docker history' equivalent check (because no Dockerfile exists — see SEC-007)

### Reference

See `checks/SEC-013.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SEC-016

## Finding: SEC-016 — 0.0.0.0-Binding-Prevention (NeighborJack)

| Feld | Wert |
|---|---|
| **Severity** | critical |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SEC-016` |
| **PDF-Reference** | Sec 4 (Empirie 2025) |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- server.py:1105 binds streamable-http transport to host='0.0.0.0' unconditionally when --http is passed

### Gaps

- FAIL: 0.0.0.0 binding means every interface on the host accepts incoming MCP requests — on a developer laptop or unhardened VM, this exposes the server to LAN neighbors (NeighborJack)
- FAIL: No --host CLI argument to override; no environment-variable opt-in for non-localhost binding
- FAIL: README's Cloud Deployment section does not warn operators that a reverse-proxy or firewall is mandatory in front of this server
- Default should be 127.0.0.1, with explicit opt-in for 0.0.0.0 only when behind a documented proxy

### Reference

See `checks/SEC-016.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


### SEC-021

## Finding: SEC-021 — Egress-Allow-List: Code-Layer und Network-Layer

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SEC-021` |
| **PDF-Reference** | Anhang B5 + B12 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- Two base URLs (api.library.ethz.ch/discovery, api.library.ethz.ch/persons) used as constants

### Gaps

- FAIL: No code-layer ALLOWED_HOSTS frozenset that wraps every outbound httpx call
- FAIL: No network-layer egress control documented (no NetworkPolicy, no Cloudflare WARP, no Security Group reference)
- FAIL: No docs/network-egress.md — a future tool added with a different host would be silently allowed
- Compromise of the codebase (typosquatted dependency, malicious commit) could redirect outbound traffic to an attacker-controlled host with no defence-in-depth

### Reference

See `checks/SEC-021.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.


---

## 6. Remediation-Plan

### Empfohlene Reihenfolge

1. **ARCH-005** (critical, partial)
2. **OBS-004** (critical, partial)
3. **SEC-016** (critical, fail)
4. **ARCH-004** (high, partial)
5. **ARCH-006** (high, partial)
6. **OBS-002** (high, fail)
7. **OPS-001** (high, partial)
8. **SCALE-002** (high, fail)
9. **SDK-001** (high, fail)
10. **SDK-004** (high, fail)
11. **SEC-003** (high, partial)
12. **SEC-005** (high, partial)
13. **SEC-007** (high, fail)
14. **SEC-013** (high, partial)
15. **SEC-021** (high, fail)
16. **ARCH-012** (medium, partial)
17. **CH-004** (medium, partial)
18. **OBS-003** (medium, fail)
19. **SDK-002** (medium, partial)
20. **SDK-003** (medium, fail)

---

## 7. Audit-Metadata

| Feld | Wert |
|---|---|
| skill_version | `0.5.0` |
| policy | `fail-or-partial` |


_Generated by tools/build_report.py — do not edit by hand._
