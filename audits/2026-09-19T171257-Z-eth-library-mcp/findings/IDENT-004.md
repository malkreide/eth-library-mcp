## Finding: IDENT-004 — Dokumentierte Versionen erzwingen — Badges sind sonst dauerhaft falsch

**Severity:** low
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** IDENT-004
**Katalog-Referenz:** Custom (Portfolio-Sweep 2026-07-29, 30 Server)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Beide Versions-Badges stimmen mit `pyproject.toml` (0.4.0) ueberein: README.md:5 und README.de.md:5 tragen je `https://img.shields.io/badge/version-0.4.0-blue`. Die uebrigen Badges (License, Python, MCP, Datenquelle) tragen keine Paketversion und sind vom Muster korrekt nicht erfasst.
- Beide README-Varianten werden wirklich geprueft, nicht nur die englische: scripts/check_version_sync.py:137-139 iteriert `ROOT.glob("README*.md")`, und die Erfolgsausgabe des Laufs nennt beide namentlich — 'geprueft: server.json -> version, server.json -> packages[0].version, README.de.md -> Versions-Badge, README.md -> Versions-Badge'.
- Der Check laeuft im selben Lauf wie IDENT-003: .github/workflows/ci.yml, letzter Schritt 'Versions-Sync (pyproject <-> server.json / README / src)' -> dasselbe Skript, dieselbe Ausfuehrung, auf allen drei Matrix-Feldern (3.11/3.12/3.13).
- GEGENPROBE gefahren: `sed -i 's|badge/version-0.4.0-blue|badge/version-0.1.0-blue|' README.de.md` -> `python scripts/check_version_sync.py` exitet 1 mit 'README.de.md -> Versions-Badge = 0.1.0'. Danach `git checkout README.de.md`, `git status --short` zeigt die Datei nicht mehr.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/IDENT-004.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Beide Versions-Badges stimmen mit `pyproject.toml` (0.4.0) ueberein: README.md:5 und README.de.md:5 tragen je `https://img.shields.io/badge/version-0.4.0-blue`. Die uebrigen Badges (License, Python, MCP, Datenquelle) tragen keine Paketversion und sind vom Muster korrekt nicht erfasst.
- Beide README-Varianten werden wirklich geprueft, nicht nur die englische: scripts/check_version_sync.py:137-139 iteriert `ROOT.glob("README*.md")`, und die Erfolgsausgabe des Laufs nennt beide namentlich — 'geprueft: server.json -> version, server.json -> packages[0].version, README.de.md -> Versions-Badge, README.md -> Versions-Badge'.
- Der Check laeuft im selben Lauf wie IDENT-003: .github/workflows/ci.yml, letzter Schritt 'Versions-Sync (pyproject <-> server.json / README / src)' -> dasselbe Skript, dieselbe Ausfuehrung, auf allen drei Matrix-Feldern (3.11/3.12/3.13).
- GEGENPROBE gefahren: `sed -i 's|badge/version-0.4.0-blue|badge/version-0.1.0-blue|' README.de.md` -> `python scripts/check_version_sync.py` exitet 1 mit 'README.de.md -> Versions-Badge = 0.1.0'. Danach `git checkout README.de.md`, `git status --short` zeigt die Datei nicht mehr.

### Gaps

- Der Check bricht beim ersten Befund ab — genau das Anti-Pattern aus der Common-Failures-Tabelle dieses Checks ('Badge-Drift verdeckt die schwerere src/-Pruefung'). GEMESSEN: beim zurueckgedrehten Badge druckte scripts/check_version_sync.py nur den DRIFT-Block und exitete via `sys.exit(1)` (Zeile 185), bevor `find_hardcoded()` (Zeile 188) ueberhaupt lief. Die Meldung 'keine hartkodierte Version in src/' erschien in diesem Lauf nicht. Richtig waere: alle Kategorien melden, dann erst `exit`.
- Die dokumentierte Version, die ein Nutzer als Erstes sieht, ist bei diesem Server nicht nur das README-Badge: `eth_library_info` meldet `**Version:** 0.3.0` (src/eth_library_mcp/server.py:713) — gemessen auch am publizierten 0.4.0-Artefakt. Das ist dieselbe Klasse (eine dokumentierte Zahl ohne erzwingende Stelle), liegt aber ausserhalb des Badge-Musters `img.shields.io/badge/[Vv]ersion-...` und wird vom Gate nicht erfasst. Der Befund selbst steht unter IDENT-002.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `low`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/IDENT-004.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
