# Security Policy & Posture

🌐 **English** | **[Deutsch](SECURITY.de.md)**

`eth-library-mcp` was hardened against the internal MCP best-practice audit
catalogue. This document summarises the security posture and records the
**accepted-risk** decisions for controls that are deliberately handled at the
portfolio/gateway layer rather than inside this single server.

## Reporting a vulnerability

Please open a private security advisory on the GitHub repository, or contact the
maintainer listed in `README.md`. Do not file public issues for exploitable
vulnerabilities.

## Posture summary

This is a **read-only**, **no-PII**, **public-domain-metadata** MCP server. All
7 tools only issue HTTP GET requests against a fixed allow-list of ETH Library
endpoints (Discovery & Persons API — see `README.md`). Hardening already in
place:

| Area | Control |
|---|---|
| Egress | HTTPS to a fixed allow-list (`ALLOWED_EGRESS_HOSTS`) of ETH Library hosts; every outbound call against a non-listed host raises `PermissionError`; no user-controlled URLs are constructed (SEC-004/021) |
| TLS | Certificate verification on by default (httpx default); never disabled (SEC-005) |
| Binding | stdio transport by default; the optional `--http` transport binds to `127.0.0.1` — `--host 0.0.0.0` must be passed explicitly, only behind a reverse proxy (SEC-016 / SDK-004) |
| CORS | The HTTP transport wraps the Starlette app in `CORSMiddleware`; `Mcp-Session-Id` is in `allow_headers` / `expose_headers` (SDK-004) |
| Tools | Every tool sets `readOnlyHint: True`; no write, mutate, or delete paths exist (ARCH) |
| Secrets | The single `ETH_LIBRARY_API_KEY` is read from the environment only; it is never logged or transmitted to third parties. `.gitignore` + `.env.example` prevent accidental secret commits (ARCH-005 / SEC-013) |
| Errors | Upstream error bodies and exception class names are never leaked to the LLM; the model receives a generic, non-leaking message. Details land in the structured stderr log (OBS-002) |
| Logging | Structured JSON logging via `structlog`, pinned to stderr; the stdio JSON-RPC stdout stream stays clean (OBS-003/004) |
| Sandbox | Multi-stage `Dockerfile` on a slim base, running as non-root UID 1000; recommended runtime `--read-only --tmpfs /tmp` (SEC-007) |
| Dependencies | Upper bounds pinned on all dependencies (`mcp[cli]>=1.0.0,<2.0.0`, `httpx>=0.27.0,<1.0.0`, `pydantic>=2.0.0,<3.0.0`) (ARCH-012) |
| Resilience | A 30s per-request timeout (`REQUEST_TIMEOUT`) bounds every upstream call (SCALE-002/003) |

The audit (`audits/2026-05-28T142641-Z-eth-library-mcp/`) found 20 findings
(3 Critical, 12 High, 5 Medium). The re-audit
(`audits/2026-05-28T184347-Z-eth-library-mcp/`, identical catalogue) confirms
all **36/36 applicable checks PASS, 0 findings** as of `0.3.0`. See
`CHANGELOG.md` for the hardening history.

> ℹ️ **Note (BUG-02):** The `eth_search_persons` tool currently returns HTTP 404
> because the Persons API endpoint URL needs verification. This is a
> functionality bug, not a security issue — the tool remains read-only and
> egress-gated like every other tool.

## Accepted risks (portfolio-level controls)

The following audit checks are **not** implemented inside this server by design.
They are portfolio-wide concerns best enforced at an MCP gateway / host layer,
and the residual risk here is low because the server is read-only and only
reaches a small set of trusted public-data providers.

### SEC-014 — Tool allow-listing via an MCP gateway

**Status:** accepted risk (portfolio-level).
A per-tool allow-list belongs to the MCP host/gateway that aggregates multiple
servers, not to an individual server that exposes a fixed, read-only tool set.
If/when a central gateway is introduced for the portfolio, tool allow-listing
should be configured there. Until then, the risk is bounded: every tool is
read-only and constrained to the fixed endpoints above.

### SEC-015 — Pre-flight tool-poisoning detection

**Status:** accepted risk (portfolio-level) — with a local guard in place.
Tool-poisoning (malicious tool descriptions / rug-pulls) is a supply-chain and
host-side concern. This server's tool definitions are version-controlled,
authored in-repo, and reviewed via PR; there is no dynamic or remote tool
registration. Cross-server poisoning detection remains a gateway/host
responsibility tracked at the portfolio level.

## Re-evaluation triggers

These acceptances should be revisited if the server ever:

- gains **write** capability or starts processing **PII**, or
- adds an **authentication** model beyond the upstream API key (then implement
  bound, TTL'd, server-side-invalidated session IDs and re-audit before merge),
  or
- registers tools **dynamically** / from remote sources, or
- is aggregated behind a shared MCP gateway (then enable the gateway's tool
  allow-listing and tool-poisoning detection).
