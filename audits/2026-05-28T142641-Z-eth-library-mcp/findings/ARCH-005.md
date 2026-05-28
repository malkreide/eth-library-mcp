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
