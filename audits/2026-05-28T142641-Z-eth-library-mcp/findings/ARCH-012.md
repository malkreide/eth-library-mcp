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
