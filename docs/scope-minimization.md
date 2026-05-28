# Scope minimization

Audit check `SEC-003` (Progressive Scope-Minimierung) requires explicit
documentation of how the upstream credential is scoped.

## Current credential

A single `ETH_LIBRARY_API_KEY` is used for every outbound request.

## Scope analysis

| API | Operation | Privilege |
|---|---|---|
| `discovery/v1/resources` | search + read bibliographic records | read-only |
| `discovery/v1/resources/{mmsid}` | read single record | read-only |
| `persons/v1/persons` | search person records | read-only |

The upstream API is **read-only against Public Domain data**. The
operator's quota is the only thing tied to the key, so further scoping
would not change the security boundary.

## Future split

If a future iteration adds write capability or non-public data:

1. Request scoped keys (one per data-class or per write/read split) from
   the developer portal at https://developer.library.ethz.ch.
2. Move all credentials to a secret manager (Stage 3 per
   [docs/secret-management.md](secret-management.md)).
3. Re-audit `SEC-003` and `SEC-013` against the new profile.

This server's current state is **acceptable for the Public Open Data
profile** — no further scope split is warranted today.
