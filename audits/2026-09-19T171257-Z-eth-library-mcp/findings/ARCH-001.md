## Finding: ARCH-001 — Tool Naming Convention

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-001
**Katalog-Referenz:** Sec 2.2
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Gemessen mit `mcp.list_tools()` (PYTHONPATH=src): genau 6 Tools, alle snake_case mit einheitlichem `eth_`-Praefix — eth_search_resources, eth_get_resource, eth_search_archive, eth_search_by_type, eth_search_education, eth_library_info. Keine Spaces, Punkte, Klammern, Unicode-Sonderzeichen.
- src/eth_library_mcp/server.py:247, :359, :423, :514, :613, :690 — jeder `@mcp.tool(name="eth_...")` setzt den Namen explizit; in der gemessenen Liste existiert keine zweite Convention (kein camelCase-, kein kebab-case-Name).
- src/eth_library_mcp/server.py:248-254 u.a. — jedes Tool traegt zusaetzlich `annotations={"title": ...}` mit menschenlesbarem Titel; im gemessenen tools/list-Resultat vorhanden.
- Beschreibungslaengen, whitespace-normalisiert aus dem gemessenen tools/list: [59, 71, 71, 73, 74, 215] Zeichen. Nur eth_search_resources (215) liefert Kontext ueber die Funktion hinaus (Discovery-Endpunkt, unterstuetzte Suchformen); die uebrigen fuenf sind Ein-Satz-Funktionsbeschreibungen, z.B. 'Durchsucht ein spezifisches Archiv oder eine Sammlung der ETH-Bibliothek.'

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-001.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Gemessen mit `mcp.list_tools()` (PYTHONPATH=src): genau 6 Tools, alle snake_case mit einheitlichem `eth_`-Praefix — eth_search_resources, eth_get_resource, eth_search_archive, eth_search_by_type, eth_search_education, eth_library_info. Keine Spaces, Punkte, Klammern, Unicode-Sonderzeichen.
- src/eth_library_mcp/server.py:247, :359, :423, :514, :613, :690 — jeder `@mcp.tool(name="eth_...")` setzt den Namen explizit; in der gemessenen Liste existiert keine zweite Convention (kein camelCase-, kein kebab-case-Name).
- src/eth_library_mcp/server.py:248-254 u.a. — jedes Tool traegt zusaetzlich `annotations={"title": ...}` mit menschenlesbarem Titel; im gemessenen tools/list-Resultat vorhanden.
- Beschreibungslaengen, whitespace-normalisiert aus dem gemessenen tools/list: [59, 71, 71, 73, 74, 215] Zeichen. Nur eth_search_resources (215) liefert Kontext ueber die Funktion hinaus (Discovery-Endpunkt, unterstuetzte Suchformen); die uebrigen fuenf sind Ein-Satz-Funktionsbeschreibungen, z.B. 'Durchsucht ein spezifisches Archiv oder eine Sammlung der ETH-Bibliothek.'

### Gaps

- Pass-Kriterium 4 (Use-Case oder Kontext in der Beschreibung, nicht nur Funktion) ist nur bei 1 von 6 Tools erfuellt; 5 Beschreibungen wiederholen im Kern den Tool-Namen als Satz.
- Vier Such-Tools (eth_search_resources/_archive/_by_type/_education) rufen alle denselben Endpunkt /resources auf; die Beschreibungen sagen nicht, wann welches zu waehlen ist — die Begruendung der Aufteilung steht nur in docs/ARCHITECTURE.md:20-58, nicht in der Tool-Description (siehe ARCH-002).

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-001.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.
