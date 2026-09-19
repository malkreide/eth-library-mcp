## Finding: ARCH-011 — Standardisierte Repo-Struktur (src-Layout, tests, README.de.md)

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-011
**Katalog-Referenz:** Anhang A8
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Alle fuenf Pflicht-Top-Level-Files vorhanden (test -f je Datei): README.md, README.de.md, CHANGELOG.md, LICENSE, pyproject.toml. Negativkontrolle derselben Schleife gegen NOPE.md → 'MISSING', die Pruefung greift also.
- Alle drei Pflicht-Verzeichnisse vorhanden: src/, tests/, .github/workflows/ — letzteres mit drei Workflows: ci.yml, live-tests.yml, publish.yml. Die Rolle 'test.yml' erfuellt ci.yml (Push/PR auf main, `pytest tests/ -m "not live"` in ci.yml:29-30), publish.yml existiert separat.
- src-Layout korrekt: `ls src/` liefert genau ein Verzeichnis `eth_library_mcp` (kein flaches Paket, keine .py-Dateien direkt unter src/), und pyproject.toml:55-56 deklariert `[tool.hatch.build.targets.wheel] packages = ["src/eth_library_mcp"]`.
- Zusaetzliche Standard-Dateien vorhanden: CONTRIBUTING.md + CONTRIBUTING.de.md, SECURITY.md + SECURITY.de.md, .env.example, Dockerfile, .dockerignore, server.json, docs/ mit fuenf Notizen.
- ABWEICHUNG 1 — kein tools/-Verzeichnis bei 6 Tools: `ls src/eth_library_mcp/tools` → 'No such file or directory'. Alle sechs Tool-Bodies liegen in src/eth_library_mcp/server.py, die mit `wc -l` 973 Zeilen misst — gegen die Vorgabe des Checks (<200 Zeilen, nur Registry + Lifecycle). Das Modul ist mit client.py/formatting.py/logging_config.py bereits geteilt, aber nicht entlang der Tool-Gruppen.
- ABWEICHUNG 2 — README-Paritaet verletzt: Section-Inventar `grep -E '^## '` ergibt EN 17 / DE 16 Ueberschriften. Die 16 decken sich semantisch paarweise; ueberzaehlig ist in README.md:399-412 ein zweiter, generierter Abschnitt `<!-- BEGIN GENERATED: install -->` / `## Installation` mit der uvx-Konfiguration. `grep -n 'BEGIN GENERATED|uvx'` findet ihn in README.md (Zeilen 399, 402, 408) und in README.de.md gar nicht; Positivkontrolle desselben Musters gegen eine Probe-Datei → Treffer. Deutschsprachige Leser bekommen die uvx-Installationsanleitung also nicht.
- ABWEICHUNG 3 — README.md:236-256 / README.de.md:237-257 ('Project Structure') beschreibt einen Baum, den es nicht mehr gibt: gelistet sind nur `__init__.py` und `server.py` ('FastMCP server, all tools') sowie `tests/test_server.py`. Tatsaechlich enthaelt src/eth_library_mcp/ vier Module (zusaetzlich client.py, formatting.py, logging_config.py) und tests/ elf Testdateien; 'FastMCP' existiert im SDK mcp 2.x gar nicht mehr (der Server nutzt `mcp.server.mcpserver.MCPServer`, server.py:34). docs/ wird im Baum nicht erwaehnt.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-011.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Alle fuenf Pflicht-Top-Level-Files vorhanden (test -f je Datei): README.md, README.de.md, CHANGELOG.md, LICENSE, pyproject.toml. Negativkontrolle derselben Schleife gegen NOPE.md → 'MISSING', die Pruefung greift also.
- Alle drei Pflicht-Verzeichnisse vorhanden: src/, tests/, .github/workflows/ — letzteres mit drei Workflows: ci.yml, live-tests.yml, publish.yml. Die Rolle 'test.yml' erfuellt ci.yml (Push/PR auf main, `pytest tests/ -m "not live"` in ci.yml:29-30), publish.yml existiert separat.
- src-Layout korrekt: `ls src/` liefert genau ein Verzeichnis `eth_library_mcp` (kein flaches Paket, keine .py-Dateien direkt unter src/), und pyproject.toml:55-56 deklariert `[tool.hatch.build.targets.wheel] packages = ["src/eth_library_mcp"]`.
- Zusaetzliche Standard-Dateien vorhanden: CONTRIBUTING.md + CONTRIBUTING.de.md, SECURITY.md + SECURITY.de.md, .env.example, Dockerfile, .dockerignore, server.json, docs/ mit fuenf Notizen.
- ABWEICHUNG 1 — kein tools/-Verzeichnis bei 6 Tools: `ls src/eth_library_mcp/tools` → 'No such file or directory'. Alle sechs Tool-Bodies liegen in src/eth_library_mcp/server.py, die mit `wc -l` 973 Zeilen misst — gegen die Vorgabe des Checks (<200 Zeilen, nur Registry + Lifecycle). Das Modul ist mit client.py/formatting.py/logging_config.py bereits geteilt, aber nicht entlang der Tool-Gruppen.
- ABWEICHUNG 2 — README-Paritaet verletzt: Section-Inventar `grep -E '^## '` ergibt EN 17 / DE 16 Ueberschriften. Die 16 decken sich semantisch paarweise; ueberzaehlig ist in README.md:399-412 ein zweiter, generierter Abschnitt `<!-- BEGIN GENERATED: install -->` / `## Installation` mit der uvx-Konfiguration. `grep -n 'BEGIN GENERATED|uvx'` findet ihn in README.md (Zeilen 399, 402, 408) und in README.de.md gar nicht; Positivkontrolle desselben Musters gegen eine Probe-Datei → Treffer. Deutschsprachige Leser bekommen die uvx-Installationsanleitung also nicht.
- ABWEICHUNG 3 — README.md:236-256 / README.de.md:237-257 ('Project Structure') beschreibt einen Baum, den es nicht mehr gibt: gelistet sind nur `__init__.py` und `server.py` ('FastMCP server, all tools') sowie `tests/test_server.py`. Tatsaechlich enthaelt src/eth_library_mcp/ vier Module (zusaetzlich client.py, formatting.py, logging_config.py) und tests/ elf Testdateien; 'FastMCP' existiert im SDK mcp 2.x gar nicht mehr (der Server nutzt `mcp.server.mcpserver.MCPServer`, server.py:34). docs/ wird im Baum nicht erwaehnt.

### Gaps

- Pass-Kriterium 'Bei > 5 Tools: tools/-Verzeichnis mit File-pro-Gruppe-Aufteilung' unerfuellt (6 Tools, server.py mit 973 Zeilen).
- Pass-Kriterium 'README.de.md ist parallel zu README.md' unerfuellt: der generierte uvx-Installationsabschnitt fehlt in der deutschen Fassung.
- Pass-Kriterium 'Abweichungen sind in README.md oder README.de.md begruendet' unerfuellt: die einzige Begruendung zur Tool-Organisation steht in docs/ARCHITECTURE.md:20-58 — der Check schliesst docs/ ausdruecklich aus. Und auch dort geht es um die Anzahl der Such-Tools, nicht um die fehlende tools/-Aufteilung.
- Die 'Project Structure'-Sektion beider READMEs ist seit dem Modul-Split (0.3.0) und der SDK-2.x-Migration nicht nachgezogen worden; sie nennt ein Framework (FastMCP), das dieser Server nicht mehr verwendet.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-011.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
