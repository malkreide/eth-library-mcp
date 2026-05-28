# Network egress

The server makes outbound HTTPS calls only to the hosts in
`ALLOWED_EGRESS_HOSTS` (defined in `src/eth_library_mcp/server.py`):

| Host | Used by | Purpose |
|---|---|---|
| `api.library.ethz.ch` | Discovery + Persons tools | All bibliographic and personal-record lookups |

Every call goes through `_http_get()`, which calls `_check_egress_allowed()`
before reaching the HTTP client. Any attempt to reach a host outside the
allow-list raises `PermissionError` — the call never leaves the process.

## Why this matters (SEC-021)

A code-layer allow-list is defence-in-depth. It catches:

- a typosquatted dependency that tries to phone home,
- a future feature added without scrutiny of its outbound host,
- a malicious commit that redirects an existing endpoint to an attacker.

The `frozenset` is immutable at runtime, so a compromised tool cannot mutate
the allow-list before issuing a request.

## Adding a new host

1. Confirm the host is genuinely needed and documented in this file.
2. Add the hostname (not the full URL) to `ALLOWED_EGRESS_HOSTS`.
3. Update this table.
4. Land the change in a PR — reviewers should treat allow-list growth as a
   security-relevant diff.

## Network-layer controls (recommended for production)

The code-layer check is intentionally cheap and the first line of defence.
For a deployment that handles non-public data or runs in a multi-tenant
environment, also configure one of:

- Kubernetes `NetworkPolicy` allowing egress only to `api.library.ethz.ch`
  on TCP/443.
- Cloud-provider security group / VPC firewall rule with the same allow-list.
- Cloudflare WARP / Tailscale ACL.

This server's current profile (Public Open Data, local-stdio default) does
not require network-layer egress controls, but the option is documented so
the path is short when scope changes.
