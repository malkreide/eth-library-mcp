# Network egress

The server makes outbound HTTPS calls only to the hosts in
`ALLOWED_EGRESS_HOSTS` (defined in `src/eth_library_mcp/client.py`; re-exported
from `server.py` for a stable import path):

| Host | Used by | Purpose |
|---|---|---|
| `api.library.ethz.ch` | all 6 tools | Bibliographic lookups via the Discovery API |

Every call goes through `_http_get()`, which calls `_check_egress_allowed()`
before reaching the HTTP client. Any attempt to reach a host outside the
allow-list raises `EgressPolicyViolation` — the call never leaves the process.

## The refusal says which kind it is (SEC-028)

`EgressPolicyViolation` is a subclass of `EgressError`, which in turn subclasses
`PermissionError` so an existing `except PermissionError` around the guard keeps
working. What it adds is a **discriminator the code reads**: `retryable = False`.

That flag is not decoration. The refusal is deterministic — the allow-list is a
configuration decision of this server, and the answer is the same on every
attempt. The message the caller gets therefore names the blocked host and the
allow-list, and it says *«Ein erneuter Versuch ändert daran nichts.»* Until
0.4.1 the same refusal arrived as *«Unbekannter Fehler. Bitte später erneut
versuchen.»* — character-identical with the message for a `ValueError`, and
with retry advice for a decision that never changes. A model reading it saw an
outage where a configuration decision was.

There is deliberately **no** `EgressResolutionError` for the transient half of
SEC-028: this guard resolves nothing. It compares the hostname from the URL
against a `frozenset`. A DNS hiccup reaches the caller as `httpx.ConnectError`
or `httpx.TimeoutException`, both of which have had their own branch in
`_handle_error` all along — and neither names the egress policy, so nobody is
sent looking for an allow-list entry for a host that is already on it.

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
