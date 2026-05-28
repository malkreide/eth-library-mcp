# Secret Management

## Current posture: Stage 1 (environment variable)

The single secret this server handles is `ETH_LIBRARY_API_KEY`, a free API
key obtained from [developer.library.ethz.ch](https://developer.library.ethz.ch).
It is loaded from the process environment at request time (`os.environ.get`
in `src/eth_library_mcp/server.py`) and never persisted, logged, or
transmitted anywhere other than the upstream API.

The mcp-audit-skill `SEC-013` check defines four maturity stages for secret
storage. This server runs at **Stage 1 (plain environment variable)** by
design.

| Stage | Mechanism | Used here? |
|---|---|---|
| 1 | Environment variable | yes |
| 2 | `.env` file outside repo | optional (gitignored) |
| 3 | Secret manager (Vault, AWS SM, GCP SM) | not used |
| 4 | Workload identity (no secret on the host) | not applicable |

### Why Stage 1 is acceptable here

The audit profile classifies this server as **Public Open Data**:

- The upstream API returns Public Domain bibliographic metadata.
- The API key is rate-limited but otherwise low-value — its compromise
  does not expose user data, only the operator's quota.
- A leaked key can be revoked and reissued in minutes from the developer
  portal.

For deployments that handle `Verwaltungsdaten` or `PII`, this server's
profile would change and Stage 3 (secret manager) would be required.

## Operational checklist

- [x] `.gitignore` excludes `.env`, `.env.*` (except `.env.example`).
- [x] `.env.example` is committed with placeholder only.
- [x] `_get_api_key()` reads from `os.environ` at call time — no module-
      level caching that could leak via repr.
- [x] The key is never included in tool returns, log messages, or error
      strings (see OBS-002 fix).
- [ ] CI gitleaks / trufflehog scan (planned for a future sprint).

## Rotation procedure

1. Visit https://developer.library.ethz.ch and generate a new key.
2. Update the operator's `ETH_LIBRARY_API_KEY` env var (e.g. in Claude
   Desktop config, Docker secret, or shell profile).
3. Restart the server process so the new value is picked up.
4. Revoke the old key in the developer portal.

No code changes are needed for rotation.
