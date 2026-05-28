# Architecture

This document records the design decisions that came out of the
mcp-audit-skill audit (run id `2026-05-28T142641-Z-eth-library-mcp`).

## Module layout

```
src/eth_library_mcp/
├── __init__.py
├── logging_config.py  # OBS-003 — structlog JSON output on stderr
├── client.py          # SDK-001, SEC-021 — httpx, egress allow-list, lifespan
├── formatting.py      # CH-004 — Markdown rendering, source attribution
└── server.py          # FastMCP tools, resources, prompts (transport-agnostic)
```

`server.py` re-exports the previously module-level names from `client.py`
and `formatting.py`, so the public-API surface
`eth_library_mcp.server.<name>` stays stable for downstream consumers
and the existing test suite (audit `ARCH-004`).

## Tool inventory and the "consolidation" question

The audit's `ARCH-006` finding flagged four search tools that all wrap
the same Discovery endpoint with different facet filters:

- `eth_search_resources` — general query, all facets optional
- `eth_search_archive` — archive-keyed (closed enum)
- `eth_search_by_type` — type-keyed (closed enum)
- `eth_search_education` — topic-curated, sort=rank, school-friendly

### Why they are kept separate

The redundancy is real *at the HTTP-API level*, but the value of the
split is in **LLM tool-picking ergonomics**:

- An LLM presented with `eth_search_archive(archive=...)` picks it
  unambiguously for archive queries. The same intent passed through
  `eth_search_resources` requires synthesising the `qInclude` facet
  string — a step where LLMs reliably make mistakes.
- The closed `Literal` enums (`ArchiveKey`, `ResourceType`) act as
  schema-level guardrails for the LLM. Collapsing into a single tool
  loses that.
- `eth_search_education` is a curated entry point for the Schulamt
  audience documented in `EXAMPLES.md`. Removing it would force the
  LLM to reconstruct the school-context query each time.

### What we did instead

- Documented this decision here (this file).
- Documented the curated audience for each tool in `EXAMPLES.md`.
- Kept the module split (`ARCH-004`) so the underlying HTTP code is
  shared even when the tool surface is intentionally redundant.

The audit finding stays "acknowledged, accepted by design" in the
backlog — not because we ignored it, but because the LLM ergonomics
argument outweighs the architectural-purity argument for this profile
(read-only Public Open Data, single-user MCP server).

## Tool returns: Markdown vs. structured

The audit's `SDK-002` finding flagged that tools return Markdown strings
instead of structured Pydantic models. This is acknowledged and
**deferred to a future v1.0**:

- Changing the return shape is a breaking change for every consumer.
- FastMCP's structured-output path is still maturing; Markdown remains
  the most reliable form for LLM consumption today.
- The `Quelle:` attribution line (`CH-004`) provides provenance without
  needing a structured field.

Tracking issue: file before bumping to `0.3.x`.

## Logging architecture (OBS-003 / OBS-004)

- `structlog` is configured at import time in `logging_config.py`.
- All output goes to `stderr` (mandatory for stdio transport — stdout is
  reserved for the JSON-RPC protocol).
- Output format is JSON with ISO-8601 UTC timestamps and explicit log
  levels — ingestible by Datadog/CloudWatch/Loki without per-source
  parsers.
- Severity levels actually used in code:
  - `debug` — per-request URL + parameter dump
  - `info`  — lifespan startup/shutdown, persons-no-results
  - `warning` — Persons-API returned an unknown response structure
  - `error` — unhandled exception class in `_handle_error`
- `Context.info()` / `Context.warning()` are used in tool error paths so
  the MCP session sees the same signal that hits stderr (`SDK-003`).

## DNS-rebinding (SEC-005)

The audit flagged `SEC-005` as partial. There is no DNS-pinning in the
httpx client. The risk is structurally bounded because:

- No user-supplied URL ever reaches the HTTP client — all base URLs are
  module-level constants validated against `ALLOWED_EGRESS_HOSTS`.
- A successful DNS-rebinding attack would require either
  (a) compromising the ETH DNS authority or (b) the operator's local
  resolver — both are out of scope for this server's threat model.

If a future feature accepts URLs from tool input, this analysis must be
revisited and `httpx`-level DNS pinning added.

## Sticky sessions for HTTP (SCALE-002)

The streamable-HTTP transport stores session state in process memory.
If the server is deployed behind a load balancer with multiple replicas,
sessions will break silently — the LB does not know to pin on
`Mcp-Session-Id`.

**Recommended deployment posture** until a Redis-backed session manager
lands:

- Single-replica deployment behind a reverse proxy.
- For multi-replica deployments, configure sticky sessions on the LB:
  - HAProxy: `stick-table type string` + `stick on req.hdr(Mcp-Session-Id)`
  - Nginx: `sticky cookie` or `ip_hash` (fallback)
  - K8s Ingress: `nginx.ingress.kubernetes.io/affinity: cookie`
    with the session header
