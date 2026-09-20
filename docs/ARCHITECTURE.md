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

## Tool returns: Markdown *and* structured

The five data-serving tools return a `CallToolResult`: a Markdown text block,
plus `structuredContent` with three fields.

| Field | Meaning |
|---|---|
| `returned` | number of records **in this response** |
| `total` | total hits per the source, `null` where the source names none |
| `hint` | the next search to try — set **only** when `returned == 0` |

`eth_library_info` is the exception and stays `-> str`: it queries no source,
has no empty set and no error channel.

### Why both, and what it costs

The audit's `SDK-002` finding asked for structured returns; `FID-003` asked
for the next step on an empty result to live in a field rather than in prose.
Markdown alone could not answer the second: the hint was in the running text
and inseparable from the result, so a consumer wanting to know whether
anything came back at all had to read Markdown.

A Pydantic return model would have satisfied both — and turned the text block
into a JSON dump, which is the worse form for the reader this server exists
for. Returning `CallToolResult` keeps the Markdown and adds the fields beside
it.

The price is measured, not assumed: a `-> CallToolResult` annotation drops the
tool's `outputSchema` from `tools/list`, because the SDK derives that schema
from the return annotation and offers no way to declare one by hand. What is
lost is `{"result": {"type": "string"}}` — a schema that said the tool returns
a string and nothing more. The shape of `structuredContent` is documented in
the table above and in each tool's description, which is where the model reads
it anyway.

### What did *not* change

The audit's argument for Markdown stands: it remains the most reliable form
for LLM consumption, and the `Quelle:` attribution line (`CH-004`) still
carries provenance in the text.

## The error channel (FID-003 / OBS-001)

A failed call and an empty result answer two different questions, and the
server keeps them apart:

| Outcome | On the wire | Next step for the model |
|---|---|---|
| Hits | `isError: false`, `returned > 0`, `hint: null` | read the records |
| Empty set | `isError: false`, `returned: 0`, `hint` set | run the search named in `hint` |
| Failure | `isError: true`, no `structuredContent` | check configuration, credentials, endpoint |

Every tool ends its `except` by raising `ToolError` with the message from
`_handle_error`. The SDK turns that into `isError: true`; the message itself
is sanitised (`OBS-002`), so no upstream body and no internal exception class
reaches the caller.

Until 0.4.1 those messages were **returned** instead of raised. A connection
failure, a 401 and a 429 all arrived as ordinary, successful tool results —
measured over the real ASGI stack during the 19 September 2026 re-audit, with
a positive control showing the error channel worked and was simply never used
for upstream failures.

The same release removed a conflation in the message itself: the 404 branch of
a search read *«Keine Ergebnisse oder Endpunkt nicht gefunden»*, folding a
statement about the holdings and one about the configuration into one
sentence. `BUG-02` in this repository was exactly the second case — a route
that had vanished from the gateway — offered to the model as a possible empty
set.

## Logging architecture (OBS-003 / OBS-004)

- `structlog` is configured at import time in `logging_config.py`.
- All output goes to `stderr` (mandatory for stdio transport — stdout is
  reserved for the JSON-RPC protocol).
- Output format is JSON with ISO-8601 UTC timestamps and explicit log
  levels — ingestible by Datadog/CloudWatch/Loki without per-source
  parsers.
- Severity levels actually used in code:
  - `debug` — per-request URL + parameter dump
  - `info`  — lifespan startup/shutdown, CORS configuration notice
  - `warning` — CORS wildcard origin, DNS-rebinding protection disabled
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
