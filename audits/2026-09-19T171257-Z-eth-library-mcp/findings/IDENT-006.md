## Finding: IDENT-006 — Veröffentlichte Version ist der aktuelle Stand — kein Release-Gap

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** IDENT-006
**Katalog-Referenz:** Custom (Portfolio-Fundstück meteoswiss-mcp#31, 2026-07-30)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Der Vergleich hat stattgefunden (kein Exit-127-Aequivalent): `curl https://pypi.org/pypi/eth-library-mcp/json` -> HTTP 200. NEGATIVKONTROLLE fuer die Erreichbarkeit: `https://pypi.org/pypi/httpx/json` -> HTTP 200; ein 404 ist hier also eine Antwort der Quelle und kein gesperrter Pfad.
- Index == letzter Tag: PyPI `info.version` = 0.4.0 (hochgeladen 2026-09-19T17:05:54Z), `git tag --list --sort=-v:refname | head -1` = v0.4.0, `pyproject.toml` version = 0.4.0. Die Registry fuehrt denselben Stand: der Eintrag mit `isLatest: true` ist 0.4.0 (publishedAt 2026-09-19T17:06:04Z). Kein Release-Gap. `yanked` ist bei 0.4.0 false.
- BEFUND — ein Tag, den der Index nicht hat: `git tag` fuehrt v0.3.2 (Commit ef72ac1, 'Release 0.3.2', 2026-06-07T04:57:58Z). `curl https://pypi.org/pypi/eth-library-mcp/0.3.2/json` -> HTTP 404, und `releases` in der PyPI-Antwort listet 0.2.0, 0.3.0, 0.3.3, 0.3.4, 0.4.0 — kein 0.3.2. Die MCP-Registry kennt ebenfalls nur 0.3.3, 0.3.4, 0.4.0. NEGATIVKONTROLLE mit derselben URL-Form: `.../0.3.3/json` -> HTTP 200. Der 404 ist also eine Auskunft und kein Messfehler. (0.3.3 wurde 24 Minuten spaeter hochgeladen — dass 0.3.2 bewusst uebersprungen statt fehlgeschlagen ist, waere eine mit den Daten vertraegliche Lesart; die Ursache ist NICHT gemessen. Der Tag existiert und der Index hat ihn nicht, und genau das verbietet das Kriterium.)
- Unveroeffentlichte Commits: `git log v0.4.0..HEAD --no-merges` -> 32ac730 'refactor: toten Persons-Parser entfernen, Profil auf Spec 2026-07-28' und 07bf225 'audit: Lauf 2026-09-19 ... begonnen', beide vom 2026-09-19. `git diff --stat v0.4.0..HEAD` beruehrt an Produktivcode ausschliesslich src/eth_library_mcp/formatting.py (-27 Zeilen, toter Parser). Kein `fix`, `feat`, `perf` oder `revert` unveroeffentlicht, nichts aelter als 7 Tage.
- CHANGELOG.md:8 — `## [Unreleased]` ist leer; der naechste Abschnitt ist `## [0.4.0] - 2026-09-19`. Der Abschnitt widerspricht dem Code also nicht.
- Modus 2: .github/workflows/publish.yml:3-4 loest auf `release: types: [published]` aus — das Erstellen des GitHub-Releases bleibt ein menschlicher Schritt. Zulaessig, aber damit dokumentationspflichtig.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/IDENT-006.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Der Vergleich hat stattgefunden (kein Exit-127-Aequivalent): `curl https://pypi.org/pypi/eth-library-mcp/json` -> HTTP 200. NEGATIVKONTROLLE fuer die Erreichbarkeit: `https://pypi.org/pypi/httpx/json` -> HTTP 200; ein 404 ist hier also eine Antwort der Quelle und kein gesperrter Pfad.
- Index == letzter Tag: PyPI `info.version` = 0.4.0 (hochgeladen 2026-09-19T17:05:54Z), `git tag --list --sort=-v:refname | head -1` = v0.4.0, `pyproject.toml` version = 0.4.0. Die Registry fuehrt denselben Stand: der Eintrag mit `isLatest: true` ist 0.4.0 (publishedAt 2026-09-19T17:06:04Z). Kein Release-Gap. `yanked` ist bei 0.4.0 false.
- BEFUND — ein Tag, den der Index nicht hat: `git tag` fuehrt v0.3.2 (Commit ef72ac1, 'Release 0.3.2', 2026-06-07T04:57:58Z). `curl https://pypi.org/pypi/eth-library-mcp/0.3.2/json` -> HTTP 404, und `releases` in der PyPI-Antwort listet 0.2.0, 0.3.0, 0.3.3, 0.3.4, 0.4.0 — kein 0.3.2. Die MCP-Registry kennt ebenfalls nur 0.3.3, 0.3.4, 0.4.0. NEGATIVKONTROLLE mit derselben URL-Form: `.../0.3.3/json` -> HTTP 200. Der 404 ist also eine Auskunft und kein Messfehler. (0.3.3 wurde 24 Minuten spaeter hochgeladen — dass 0.3.2 bewusst uebersprungen statt fehlgeschlagen ist, waere eine mit den Daten vertraegliche Lesart; die Ursache ist NICHT gemessen. Der Tag existiert und der Index hat ihn nicht, und genau das verbietet das Kriterium.)
- Unveroeffentlichte Commits: `git log v0.4.0..HEAD --no-merges` -> 32ac730 'refactor: toten Persons-Parser entfernen, Profil auf Spec 2026-07-28' und 07bf225 'audit: Lauf 2026-09-19 ... begonnen', beide vom 2026-09-19. `git diff --stat v0.4.0..HEAD` beruehrt an Produktivcode ausschliesslich src/eth_library_mcp/formatting.py (-27 Zeilen, toter Parser). Kein `fix`, `feat`, `perf` oder `revert` unveroeffentlicht, nichts aelter als 7 Tage.
- CHANGELOG.md:8 — `## [Unreleased]` ist leer; der naechste Abschnitt ist `## [0.4.0] - 2026-09-19`. Der Abschnitt widerspricht dem Code also nicht.
- Modus 2: .github/workflows/publish.yml:3-4 loest auf `release: types: [published]` aus — das Erstellen des GitHub-Releases bleibt ein menschlicher Schritt. Zulaessig, aber damit dokumentationspflichtig.

### Gaps

- Der Release-Tag v0.3.2 existiert, ohne dass Index oder Registry ihn fuehren — ein geschnittenes Release, das nie angekommen ist (oder ein Tag ohne Release; beides bleibt sichtbar als Behauptung, der nichts entspricht).
- Der Release-Prozess ist nirgends beschrieben: CONTRIBUTING.md behandelt nur Fork/Branch/Tests/CHANGELOG/PR (Zeilen 66-85) und nennt weder das Bumpen, das Taggen noch das manuelle Erstellen des GitHub-Releases, das `publish.yml` ueberhaupt erst ausloest. README.md erwaehnt weder Release noch Publish. Genau der manuelle Schritt, den der Check dokumentiert sehen will, steht nirgends — und genau so bleibt ein Release liegen.
- IDENT-007 wurde separat beantwortet; aus diesem Pass wurde NICHT auf die Gesundheit des Artefakts geschlossen.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/IDENT-006.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.
