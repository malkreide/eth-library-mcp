## Finding: ARCH-006 — Tool-Budget: High-Level-Use-Cases statt API-Mapping 1:1

| Feld | Wert |
|---|---|
| **Severity** | high |
| **Status** | open |
| **Server** | `eth-library-mcp` |
| **Check-Reference** | `ARCH-006` |
| **PDF-Reference** | Sec 2.3 |
| **Audit-Datum** | 2026-05-28 |
| **Auditor** | Claude (mcp-audit-skill v0.5.0) |

### Observed Behavior

Verification-Status: **partial**

Evidence collected:
- 7 tools total — under the typical budget of 10–15
- Tools organized around use cases (search_education for school context, library_info as entry point)

### Gaps

- eth_search_resources, eth_search_archive, eth_search_by_type and eth_search_education all wrap the same Discovery API endpoint with different facet filters — they could be a single tool with optional facet parameters
- eth_search_education is essentially eth_search_resources with sort=rank and a fixed query template — boundary between them is fuzzy

### Reference

See `checks/ARCH-006.md` in mcp-audit-skill for full pass criteria, remediation steps, and references.
