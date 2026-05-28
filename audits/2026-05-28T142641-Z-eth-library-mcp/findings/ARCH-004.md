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
