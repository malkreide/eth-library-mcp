## Finding: SCALE-002 — Stateful Load Balancing für Streamable HTTP / SSE

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `SCALE-002` |
| **PDF-Reference** | Sec 5.2 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **fail**

Evidence collected:
- Server supports streamable-http transport (server.py:1105) — SCALE-002 applies

### Gaps

- FAIL: No sticky-session config, no session-store backend (Redis/Durable Objects), no reference to Mcp-Session-Id handling
- If deployed behind a multi-replica load balancer, session affinity will break silently
- README cloud-deployment section does not warn that LB must pin on Mcp-Session-Id

### Reference

See `checks/SCALE-002.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.
