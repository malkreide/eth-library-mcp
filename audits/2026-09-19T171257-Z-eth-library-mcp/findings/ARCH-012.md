## Finding: ARCH-012 — protocolVersion-Pinning + CHANGELOG + SDK-Update-Disziplin

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-012
**Katalog-Referenz:** Anhang A9
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Verhalten der modernen Baseline gemessen, nicht geschlossen: ein POST durch build_http_app() mit `_meta["io.modelcontextprotocol/protocolVersion"] = "2026-07-28"` liefert HTTP 200 und ein tools/list-Resultat; derselbe Request mit "2099-01-01" liefert HTTP 400 und `{"code":-32022,"message":"Unsupported protocol version","data":{"supported":["2026-07-28"],"requested":"2099-01-01"}}`. Die Pruefung findet also pro Request statt.
- `server/discover` nennt dieselbe Liste: gemessen `"supportedVersions":["2026-07-28"]` im selben Lauf — deckungsgleich mit dem `data.supported` des -32022 (Kriterium zu ARCH-016 erfuellt).
- Kein Pin im Server-Code: `grep -rnE 'protocolVersion|protocol_version|PROTOCOL_VERSION|SUPPORTED_PROTOCOL' src/` → 0 Treffer; Positivkontrolle: derselbe Ausdruck findet die Konstanten in tests/ (test_protocol_version.py:47, :86-96). Der Pin ist stattdessen CI-seitig: tests/test_protocol_version.py:58-59 `DOCUMENTED_HANDSHAKE_VERSION = "2025-11-25"` / `DOCUMENTED_MODERN_VERSION = "2026-07-28"`, abgesichert gegen LATEST_HANDSHAKE_VERSION / LATEST_MODERN_VERSION des SDK und gegen eine echte `initialize`-Aushandlung durch den ASGI-Stack (test_protocol_version.py:175-183). Der Docstring begruendet die Bauart: das SDK nimmt gar keinen setzbaren Pin entgegen.
- CHANGELOG.md vorhanden im Keep-a-Changelog-Format (CHANGELOG.md:1-8: Titel, Verweis auf keepachangelog.com, `## [Unreleased]`, `## [0.4.0] – 2026-09-19` mit Rubriken '⚠️ Brechende Aenderungen' / 'Geaendert' / 'Behoben').
- CHANGELOG nennt Spec-Revisionen explizit: Zeilen 14, 54, 169, 184, 191-192, 200 fuehren `2026-07-28` und `2025-11-25` samt der Aera-Aufteilung.
- README-Sektion vorhanden: README.md:260-286 '## MCP Protocol Version' mit Tabelle beider Aeren und Absatz '**Update policy.**' (README.md:281-285: Spec-Changelog lesen, Verhalten pruefen, dann Konstante, README.de.md und CHANGELOG.md zusammen bewegen). Deutsche Entsprechung README.de.md:261 '## MCP-Protokollversion'. Ein Test haelt beide Fassungen zusammen (test_protocol_version.py:115-129).
- Dependabot aktiv: .github/dependabot.yml mit drei Oekosystemen (pip, github-actions, docker), je `interval: "monthly"` und `open-pull-requests-limit: 5`. Der SDK-Bump von `mcp[cli]` faellt damit in die pip-Gruppe `python-dependencies: patterns: ["*"]`.
- 128 Unit-Tests gruen (`PYTHONPATH=src pytest tests/ -m "not live" -q` → 128 passed, 2 deselected), darunter die 11 Protokoll-Tests.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-012.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Verhalten der modernen Baseline gemessen, nicht geschlossen: ein POST durch build_http_app() mit `_meta["io.modelcontextprotocol/protocolVersion"] = "2026-07-28"` liefert HTTP 200 und ein tools/list-Resultat; derselbe Request mit "2099-01-01" liefert HTTP 400 und `{"code":-32022,"message":"Unsupported protocol version","data":{"supported":["2026-07-28"],"requested":"2099-01-01"}}`. Die Pruefung findet also pro Request statt.
- `server/discover` nennt dieselbe Liste: gemessen `"supportedVersions":["2026-07-28"]` im selben Lauf — deckungsgleich mit dem `data.supported` des -32022 (Kriterium zu ARCH-016 erfuellt).
- Kein Pin im Server-Code: `grep -rnE 'protocolVersion|protocol_version|PROTOCOL_VERSION|SUPPORTED_PROTOCOL' src/` → 0 Treffer; Positivkontrolle: derselbe Ausdruck findet die Konstanten in tests/ (test_protocol_version.py:47, :86-96). Der Pin ist stattdessen CI-seitig: tests/test_protocol_version.py:58-59 `DOCUMENTED_HANDSHAKE_VERSION = "2025-11-25"` / `DOCUMENTED_MODERN_VERSION = "2026-07-28"`, abgesichert gegen LATEST_HANDSHAKE_VERSION / LATEST_MODERN_VERSION des SDK und gegen eine echte `initialize`-Aushandlung durch den ASGI-Stack (test_protocol_version.py:175-183). Der Docstring begruendet die Bauart: das SDK nimmt gar keinen setzbaren Pin entgegen.
- CHANGELOG.md vorhanden im Keep-a-Changelog-Format (CHANGELOG.md:1-8: Titel, Verweis auf keepachangelog.com, `## [Unreleased]`, `## [0.4.0] – 2026-09-19` mit Rubriken '⚠️ Brechende Aenderungen' / 'Geaendert' / 'Behoben').
- CHANGELOG nennt Spec-Revisionen explizit: Zeilen 14, 54, 169, 184, 191-192, 200 fuehren `2026-07-28` und `2025-11-25` samt der Aera-Aufteilung.
- README-Sektion vorhanden: README.md:260-286 '## MCP Protocol Version' mit Tabelle beider Aeren und Absatz '**Update policy.**' (README.md:281-285: Spec-Changelog lesen, Verhalten pruefen, dann Konstante, README.de.md und CHANGELOG.md zusammen bewegen). Deutsche Entsprechung README.de.md:261 '## MCP-Protokollversion'. Ein Test haelt beide Fassungen zusammen (test_protocol_version.py:115-129).
- Dependabot aktiv: .github/dependabot.yml mit drei Oekosystemen (pip, github-actions, docker), je `interval: "monthly"` und `open-pull-requests-limit: 5`. Der SDK-Bump von `mcp[cli]` faellt damit in die pip-Gruppe `python-dependencies: patterns: ["*"]`.
- 128 Unit-Tests gruen (`PYTHONPATH=src pytest tests/ -m "not live" -q` → 128 passed, 2 deselected), darunter die 11 Protokoll-Tests.

### Gaps

- Pass-Kriterium 1 ('protocolVersion ist im Server-Code explizit gepinnt') ist woertlich unerfuellt — in src/ steht keine Versionskonstante. Das ist begruendet (das SDK bietet keinen Parameter) und durch einen CI-Gate ersetzt; wer nur src/ liest, sieht den Pin aber nicht, und der gemessene -32022-Pfad stammt vollstaendig aus dem SDK, nicht aus diesem Repo.
- Der abgeloeste Persons-Stand ist in SECURITY.md:34 nicht nachgezogen: dort steht 'Upper bounds pinned on all dependencies (`mcp[cli]>=1.0.0,<2.0.0`, ...)', pyproject.toml:29 fuehrt aber `mcp[cli]>=2.0.0,<3`. Die Sicherheitsnotiz beschreibt die Dependency-Disziplin einer Major-Version, die dieses Release verlassen hat (gleiches in SECURITY.de.md).
- Hartkodierte Version im Auslieferungspfad, die das Versionsgate nicht sieht: src/eth_library_mcp/server.py:713 gibt `**Version:** 0.3.0` aus; gemessen liefert `eth_library_info()` diese Zeile, waehrend `eth_library_mcp.__version__` 0.4.0 ist. `python scripts/check_version_sync.py` meldet trotzdem 'Versions-Sync OK (0.4.0; ... keine hartkodierte Version in src/)' — der Detektor (scripts/check_version_sync.py:102-128) sucht nur die User-Agent-Form und `__version__ = "..."`, nicht Versionsangaben in Tool-Ausgaben.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-012.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
