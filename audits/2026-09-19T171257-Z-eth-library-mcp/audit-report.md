# MCP-Server Audit-Report — `eth-library-mcp`

**Audit-Datum:** 
**Skill-Version:** 2.3.0
**Catalog-Version:** ?

---

## 1. Executive Summary

Server `eth-library-mcp` wurde gegen 85 anwendbare Best-Practice-Checks geprüft. 24 bestanden, 60 Findings dokumentiert (4 critical, 30 high, 25 medium, 1 low). Production-Readiness: NICHT erreicht — blockierend: DRIFT-003, FID-001, FID-002, FID-003, SEC-028. Zusätzlich 3 advisory-Finding(s) auf blockierender Severity: FID-006, FID-007, OPS-010. 1 Check(s) konnten nicht verifiziert werden und zählen weder als bestanden noch als fehlgeschlagen: SEC-026. Sie gehören unter «Offen».

**Production-Readiness:** NO (über 1 nicht verifizierte Checks)

---

## 2. Profil-Snapshot

| Feld | Wert |
|---|---|
| Server-Name | `eth-library-mcp` |
| Audit-Datum | ? |
| Skill-Version | 2.3.0 |
| Catalog-Version | ? |

---

## 3. Applicability

### Status pro Kategorie

| Kategorie | Pass | Fail | Partial | Not verified | Todo | N/A |
|---|---|---|---|---|---|---|
| ARCH | 5 | 2 | 14 | 0 | 0 | 0 |
| CH | 1 | 0 | 0 | 0 | 0 | 0 |
| DEP | 1 | 0 | 0 | 0 | 0 | 0 |
| DRIFT | 1 | 2 | 4 | 0 | 0 | 0 |
| FID | 0 | 5 | 2 | 0 | 0 | 0 |
| HITL | 1 | 0 | 0 | 0 | 0 | 0 |
| IDENT | 2 | 1 | 4 | 0 | 0 | 0 |
| OBS | 1 | 0 | 5 | 0 | 0 | 0 |
| OPS | 2 | 1 | 7 | 0 | 0 | 0 |
| SCALE | 1 | 0 | 2 | 0 | 0 | 0 |
| SDK | 2 | 0 | 2 | 0 | 0 | 0 |
| SEC | 7 | 1 | 8 | 1 | 0 | 0 |
| **Total** | **24** | **12** | **48** | **1** | **0** | **0** |

### Vergleich zum Vorlauf

**Trendlinie gebrochen — kein Vergleich mit `2026-05-28T184347-Z-eth-library-mcp`.**

catalog_hash is missing for the previous run, so it cannot be shown that both audits used the same catalogue. Trend comparison refused — unknown is not the same as unchanged.

| | Vorlauf | Dieser Lauf |
|---|---|---|
| Katalog-Hash | `?` | `2bbded9079fd` |
| Geprüfte Checks | 38 | 85 |

Die Status-Zahlen beider Läufe stehen in den jeweiligen Reports. Sie werden hier **bewusst nicht** gegenübergestellt: über zwei verschiedene Katalog-Stände ist eine Differenz keine Veränderung am Server, sondern eine am Massstab. Für eine echte Trendlinie den Vorlauf gegen denselben Katalog-Stand neu auswerten.

---

## 4. Findings-Übersicht

_Policy: `fail-or-partial`_

| ID | Category | Severity | Status |
|---|---|---|---|
| ARCH-005 | ARCH | critical | partial |
| FID-001 | FID | critical | fail |
| SEC-004 | SEC | critical | partial |
| SEC-019 | SEC | critical | partial |
| ARCH-004 | ARCH | high | partial |
| ARCH-009 | ARCH | high | partial |
| ARCH-013 | ARCH | high | partial |
| ARCH-016 | ARCH | high | partial |
| DRIFT-002 | DRIFT | high | partial |
| DRIFT-003 | DRIFT | high | fail |
| DRIFT-004 | DRIFT | high | partial |
| DRIFT-008 | DRIFT | high | partial |
| FID-002 | FID | high | fail |
| FID-003 | FID | high | fail |
| FID-006 | FID | high | fail |
| FID-007 | FID | high | fail |
| IDENT-006 | IDENT | high | partial |
| IDENT-007 | IDENT | high | partial |
| OBS-001 | OBS | high | partial |
| OBS-002 | OBS | high | partial |
| OPS-001 | OPS | high | partial |
| OPS-003 | OPS | high | partial |
| OPS-004 | OPS | high | partial |
| OPS-005 | OPS | high | partial |
| OPS-009 | OPS | high | partial |
| OPS-010 | OPS | high | fail |
| SCALE-009 | SCALE | high | partial |
| SEC-003 | SEC | high | partial |
| SEC-005 | SEC | high | partial |
| SEC-007 | SEC | high | partial |
| SEC-018 | SEC | high | partial |
| SEC-021 | SEC | high | partial |
| SEC-024 | SEC | high | partial |
| SEC-028 | SEC | high | fail |
| ARCH-001 | ARCH | medium | partial |
| ARCH-002 | ARCH | medium | fail |
| ARCH-003 | ARCH | medium | fail |
| ARCH-007 | ARCH | medium | partial |
| ARCH-011 | ARCH | medium | partial |
| ARCH-012 | ARCH | medium | partial |
| ARCH-018 | ARCH | medium | partial |
| ARCH-019 | ARCH | medium | partial |
| ARCH-020 | ARCH | medium | partial |
| ARCH-021 | ARCH | medium | partial |
| ARCH-022 | ARCH | medium | partial |
| DRIFT-001 | DRIFT | medium | partial |
| DRIFT-006 | DRIFT | medium | fail |
| FID-004 | FID | medium | partial |
| FID-005 | FID | medium | partial |
| IDENT-002 | IDENT | medium | fail |
| IDENT-003 | IDENT | medium | partial |
| OBS-003 | OBS | medium | partial |
| OBS-007 | OBS | medium | partial |
| OBS-008 | OBS | medium | partial |
| OPS-002 | OPS | medium | partial |
| OPS-007 | OPS | medium | partial |
| SCALE-010 | SCALE | medium | partial |
| SDK-002 | SDK | medium | partial |
| SDK-003 | SDK | medium | partial |
| IDENT-004 | IDENT | low | partial |

**Gesamt:** 60 Findings

---

## 5. Detail-Findings

### ARCH-001

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


### ARCH-002

## Finding: ARCH-002 — Tool-Beschreibung mit Use-Case-Tags

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-002
**Katalog-Referenz:** Sec 2.2
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- Gemessen mit `mcp.list_tools()` und `re.sub(r'\s+',' ',desc)`: Laengen [59, 71, 71, 73, 74, 215], Median 72 Zeichen. Pass-Kriterium verlangt Median >= 100 — verfehlt. Minimum 59 liegt ueber der 50-Zeichen-Untergrenze.
- Suche nach `<use_case>|<important_notes>|<example>` ueber alle 5 Dateien in src/, jeweils NACH Whitespace-Normalisierung des ganzen Datei-Texts: 0 Treffer in client.py, __init__.py, formatting.py, logging_config.py, server.py. Positivkontrolle im selben Lauf: derselbe Regex auf 'desc <use_case>x</use_case>' → Treffer; Negativkontrolle 'nothing here' → kein Treffer. Das Muster greift also.
- src/eth_library_mcp/server.py:423-437 — die Description von eth_search_archive ist der Docstring 'Durchsucht ein spezifisches Archiv oder eine Sammlung der ETH-Bibliothek.' (73 Zeichen), ohne Caveat, Limit-Hinweis oder Abgrenzung zu eth_search_resources.
- Mildernd, aber nicht kriteriumserfuellend: die Feld-Beschreibungen im inputSchema sind reichhaltig — gemessen im tools/list-Schema traegt `query` 301 Zeichen mit Syntaxerklaerung und zwei Beispielen (src/eth_library_mcp/server.py:200-207). Die Kriterien von ARCH-002 beziehen sich auf die Tool-Description, nicht auf Parameterfelder.
- src/eth_library_mcp/server.py:175-186 — die Server-`instructions` (Zeile 179: 'Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung') bewerben ein Werkzeug, das 0.4.0 entfernt hat. Gemessen im `server/discover`-Resultat durch den zusammengebauten ASGI-Stack: der Satz geht live an jeden Client raus.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-002.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Gemessen mit `mcp.list_tools()` und `re.sub(r'\s+',' ',desc)`: Laengen [59, 71, 71, 73, 74, 215], Median 72 Zeichen. Pass-Kriterium verlangt Median >= 100 — verfehlt. Minimum 59 liegt ueber der 50-Zeichen-Untergrenze.
- Suche nach `<use_case>|<important_notes>|<example>` ueber alle 5 Dateien in src/, jeweils NACH Whitespace-Normalisierung des ganzen Datei-Texts: 0 Treffer in client.py, __init__.py, formatting.py, logging_config.py, server.py. Positivkontrolle im selben Lauf: derselbe Regex auf 'desc <use_case>x</use_case>' → Treffer; Negativkontrolle 'nothing here' → kein Treffer. Das Muster greift also.
- src/eth_library_mcp/server.py:423-437 — die Description von eth_search_archive ist der Docstring 'Durchsucht ein spezifisches Archiv oder eine Sammlung der ETH-Bibliothek.' (73 Zeichen), ohne Caveat, Limit-Hinweis oder Abgrenzung zu eth_search_resources.
- Mildernd, aber nicht kriteriumserfuellend: die Feld-Beschreibungen im inputSchema sind reichhaltig — gemessen im tools/list-Schema traegt `query` 301 Zeichen mit Syntaxerklaerung und zwei Beispielen (src/eth_library_mcp/server.py:200-207). Die Kriterien von ARCH-002 beziehen sich auf die Tool-Description, nicht auf Parameterfelder.
- src/eth_library_mcp/server.py:175-186 — die Server-`instructions` (Zeile 179: 'Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung') bewerben ein Werkzeug, das 0.4.0 entfernt hat. Gemessen im `server/discover`-Resultat durch den zusammengebauten ASGI-Stack: der Satz geht live an jeden Client raus.

### Gaps

- Kein Tool nennt Use-Case-Tags oder ein Aequivalent (0% statt geforderter 80%).
- Keine Important-Notes/Caveats in den Descriptions: weder das 100er-Limit, noch dass ein API-Key noetig ist, noch dass eth_get_resource eine MMS-ID aus einer vorherigen Suche braucht.
- Bei vier stark aehnlichen Such-Tools macht keine Description die Differenzierung explizit — genau der Common-Failure-Fall 'LLM raet, welches richtig ist'.
- Die Server-instructions bewerben ein entferntes Werkzeug (Personen-Suche). Der CHANGELOG 0.4.0 beschreibt, dass pyproject.toml, server.json, READMEs, EXAMPLES.md und docs/ dafuer nachgezogen wurden — server.py:179 wurde dabei uebersehen.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-002.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-003

## Finding: ARCH-003 — «Not Found» Anti-Pattern: Heuristiken statt leerer Antworten

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-003
**Katalog-Referenz:** Sec 2.2
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- Runtime gemessen (respx-Mock auf DISCOVERY_BASE_URL/resources, Antwort {"docs": [], "info": {"total": 0}}): alle vier Such-Tools geben einen nackten String zurueck, kein Objekt. eth_search_resources → "Keine Ergebnisse fuer 'any,contains,Quellensteuerverordnung'. Tipp: Breitere Suche mit 'any,contains,Begriff' versuchen."; eth_search_archive → "Keine Treffer im Archiv 'Hochschularchiv ETH Zuerich' fuer Suche '...'."; eth_search_by_type → "Keine Karten / Maps gefunden fuer Suche: '...'."; eth_search_education → "... Tipp: Englischen Begriff oder breiteres Schlagwort versuchen."
- Kein `match_type`-Feld und kein Aequivalent: Suche nach `match_type` und `suggestion` ueber src/ und tests/ → je 0 Treffer. Negativkontrolle im selben Lauf gegen eine Probe-Datei mit den Zeilen `result.match_type` / `result.suggestions` → je 1 Treffer, das Muster greift also.
- src/eth_library_mcp/server.py:296-300, :452-454, :548-550, :650-654 — die vier Leermengen-Zweige. Zwei davon (resources, education) tragen einen generischen Tipp, zwei (archive, by_type) geben gar keinen naechsten Schritt an.
- Modus-3-Testpaar fehlt vollstaendig: Suche nach `call_count` ueber tests/ und src/ → 0 Treffer; Negativkontrolle gegen eine Probe-Datei mit `assert route.call_count == 1` → 1 Treffer. tests/test_tools.py:72-79 (`test_search_resources_no_hits`) prueft ausschliesslich den Rueckgabewert (`assert "Keine Ergebnisse" in out`), zaehlt keine Route und gibt es nur fuer eines der vier Such-Tools.
- Positiver Teilbefund, von mir am Routenzaehler erhoben (nicht im Repo getestet): pro Tool-Aufruf geht genau EIN Upstream-Request raus (route.call_count == 1 in allen vier Faellen), und der gesendete `q`-Parameter ist der unveraenderte Begriff des Aufrufers — z.B. q='any,contains,Quellensteuerverordnung'. Der Server verbreitert also nicht still.
- src/eth_library_mcp/server.py:358-390 (eth_get_resource) ist ein exakter ID-Lookup ohne Fuzzy-Fallback; bei 404 liefert formatting.py:_handle_error einen MMS-ID-Hinweis ohne Aehnlichkeitsvorschlaege (tests/test_tools.py:120-129). Die Sensitive-Data-Ausnahme wird nicht missbraucht.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-003.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Runtime gemessen (respx-Mock auf DISCOVERY_BASE_URL/resources, Antwort {"docs": [], "info": {"total": 0}}): alle vier Such-Tools geben einen nackten String zurueck, kein Objekt. eth_search_resources → "Keine Ergebnisse fuer 'any,contains,Quellensteuerverordnung'. Tipp: Breitere Suche mit 'any,contains,Begriff' versuchen."; eth_search_archive → "Keine Treffer im Archiv 'Hochschularchiv ETH Zuerich' fuer Suche '...'."; eth_search_by_type → "Keine Karten / Maps gefunden fuer Suche: '...'."; eth_search_education → "... Tipp: Englischen Begriff oder breiteres Schlagwort versuchen."
- Kein `match_type`-Feld und kein Aequivalent: Suche nach `match_type` und `suggestion` ueber src/ und tests/ → je 0 Treffer. Negativkontrolle im selben Lauf gegen eine Probe-Datei mit den Zeilen `result.match_type` / `result.suggestions` → je 1 Treffer, das Muster greift also.
- src/eth_library_mcp/server.py:296-300, :452-454, :548-550, :650-654 — die vier Leermengen-Zweige. Zwei davon (resources, education) tragen einen generischen Tipp, zwei (archive, by_type) geben gar keinen naechsten Schritt an.
- Modus-3-Testpaar fehlt vollstaendig: Suche nach `call_count` ueber tests/ und src/ → 0 Treffer; Negativkontrolle gegen eine Probe-Datei mit `assert route.call_count == 1` → 1 Treffer. tests/test_tools.py:72-79 (`test_search_resources_no_hits`) prueft ausschliesslich den Rueckgabewert (`assert "Keine Ergebnisse" in out`), zaehlt keine Route und gibt es nur fuer eines der vier Such-Tools.
- Positiver Teilbefund, von mir am Routenzaehler erhoben (nicht im Repo getestet): pro Tool-Aufruf geht genau EIN Upstream-Request raus (route.call_count == 1 in allen vier Faellen), und der gesendete `q`-Parameter ist der unveraenderte Begriff des Aufrufers — z.B. q='any,contains,Quellensteuerverordnung'. Der Server verbreitert also nicht still.
- src/eth_library_mcp/server.py:358-390 (eth_get_resource) ist ein exakter ID-Lookup ohne Fuzzy-Fallback; bei 404 liefert formatting.py:_handle_error einen MMS-ID-Hinweis ohne Aehnlichkeitsvorschlaege (tests/test_tools.py:120-129). Die Sensitive-Data-Ausnahme wird nicht missbraucht.

### Gaps

- Kriterium 1 unerfuellt: keine Leermenge triggert Fuzzy-Match oder Suggestion-Mechanismus.
- Kriterium 2 unerfuellt: kein `match_type`-Feld (exact/fuzzy/none). Die Antwort ist ein Markdown-/Klartext-String — der Common Failure 'String "No results" als Response'.
- Kriterium 3 nur halb erfuellt: eth_search_archive und eth_search_by_type geben ueberhaupt keinen actionable Hinweis. Die Hinweise der anderen beiden sind generisch ('Breitere Suche ... versuchen'), nicht aus der Eingabe abgeleitet.
- Kriterium 'Vorschlaege sind aus der Eingabe abgeleitet' und 'heuristische Treffer in eigenem Feld' sind gegenstandslos, weil es keine Vorschlaege gibt — das zaehlt als unerfuellt, nicht als n/a (Katalogtext: 'nachweislich unschaedlich und nachweislich nutzlos').
- Kriterium 'Die Antwort sagt, dass nicht verbreitert wurde' unerfuellt: keiner der vier Texte sagt, dass genau einmal und nur mit dem gegebenen Begriff gesucht wurde.
- Modus-3-Testpaar fehlt ganz (weder Vorschlags- noch Zaehler-Haelfte), und damit auch die im Katalog verlangte Gegenprobe gegen eine Fassung, die ihre Vorschlaege selbst absucht.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-003.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-004

## Finding: ARCH-004 — Inversion of Control: Transport-agnostische Server-Logik

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-004
**Katalog-Referenz:** Sec 2.1
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Keine Transport-Internals in Tool-Handlern: Suche nach `request.headers|websocket.|sys.stdin|sys.stdout|.remote_addr` ueber src/*.py → 0 Treffer. Negativkontrolle im selben Lauf gegen eine Probe-Datei mit `ua = request.headers["User-Agent"]` und `sys.stdout.write(ua)` → 2 Treffer, das Muster greift.
- src/eth_library_mcp/server.py:258, :370, :434, :525, :624 — alle fuenf netzsprechenden Tools nehmen ausschliesslich `ctx: Context | None = None` entgegen und nutzen davon nur `ctx.report_progress()` / `ctx.warning()`, also die protokollseitige, transportunabhaengige Schnittstelle.
- Beide Transporte werden aus demselben Code bedient: src/eth_library_mcp/server.py:961-973 — `--http` fuehrt ueber `_run_http` → `build_http_app()` → `mcp.streamable_http_app(...)`, sonst `mcp.run()` (stdio). Der Lifespan ist gemeinsam: client.py:88-101 `lifespan()` wird in server.py:186 an den einen `MCPServer` uebergeben und gilt fuer beide Wege.
- Modulgrenzen belegt: client.py (httpx, Egress-Allow-List, Lifespan), formatting.py (reines Markdown-Rendering, keine HTTP-Aufrufe), logging_config.py, server.py (Tool-Registry). Die Tool-Schicht spricht upstream ausschliesslich ueber `_http_get` (server.py:291, :379, :448, :544, :646).
- Selbst gemessen (respx-Mock, direkte Funktionsaufrufe ohne Transport, und ein echter POST durch den ASGI-Stack via build_http_app()): dasselbe tools/list-Resultat und dieselben Tool-Rueckgaben; die Handler lesen keinen Transport-Zustand.
- Konfiguration NICHT ueber ein Settings-Objekt: Suche nach `BaseSettings|pydantic_settings` in src/ → 0 Treffer (einziger `Settings(`-Treffer ist `TransportSecuritySettings` des SDK, server.py:896). Negativkontrolle gegen eine Probe-Datei mit `from pydantic import SecretStr` / `class S(BaseSettings)` → Treffer. Stattdessen 5 verstreute `os.environ.get(...)`-Aufrufe (client.py:45; server.py:59, :701, :846, :857) plus das Modul-Global `_http_client` (client.py:38).

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-004.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Keine Transport-Internals in Tool-Handlern: Suche nach `request.headers|websocket.|sys.stdin|sys.stdout|.remote_addr` ueber src/*.py → 0 Treffer. Negativkontrolle im selben Lauf gegen eine Probe-Datei mit `ua = request.headers["User-Agent"]` und `sys.stdout.write(ua)` → 2 Treffer, das Muster greift.
- src/eth_library_mcp/server.py:258, :370, :434, :525, :624 — alle fuenf netzsprechenden Tools nehmen ausschliesslich `ctx: Context | None = None` entgegen und nutzen davon nur `ctx.report_progress()` / `ctx.warning()`, also die protokollseitige, transportunabhaengige Schnittstelle.
- Beide Transporte werden aus demselben Code bedient: src/eth_library_mcp/server.py:961-973 — `--http` fuehrt ueber `_run_http` → `build_http_app()` → `mcp.streamable_http_app(...)`, sonst `mcp.run()` (stdio). Der Lifespan ist gemeinsam: client.py:88-101 `lifespan()` wird in server.py:186 an den einen `MCPServer` uebergeben und gilt fuer beide Wege.
- Modulgrenzen belegt: client.py (httpx, Egress-Allow-List, Lifespan), formatting.py (reines Markdown-Rendering, keine HTTP-Aufrufe), logging_config.py, server.py (Tool-Registry). Die Tool-Schicht spricht upstream ausschliesslich ueber `_http_get` (server.py:291, :379, :448, :544, :646).
- Selbst gemessen (respx-Mock, direkte Funktionsaufrufe ohne Transport, und ein echter POST durch den ASGI-Stack via build_http_app()): dasselbe tools/list-Resultat und dieselben Tool-Rueckgaben; die Handler lesen keinen Transport-Zustand.
- Konfiguration NICHT ueber ein Settings-Objekt: Suche nach `BaseSettings|pydantic_settings` in src/ → 0 Treffer (einziger `Settings(`-Treffer ist `TransportSecuritySettings` des SDK, server.py:896). Negativkontrolle gegen eine Probe-Datei mit `from pydantic import SecretStr` / `class S(BaseSettings)` → Treffer. Stattdessen 5 verstreute `os.environ.get(...)`-Aufrufe (client.py:45; server.py:59, :701, :846, :857) plus das Modul-Global `_http_client` (client.py:38).

### Gaps

- Pass-Kriterium 3 unerfuellt: keine Pydantic-Settings-/Settings-Klasse. Konfiguration liegt in verstreuten `os.environ.get`-Aufrufen und Modul-Funktionen (`configured_origins()`, `allowed_hosts()`), dazu ein mutierendes Modul-Global `_http_client` — genau der im Check genannte Flaky-Test-Anti-Pattern.
- Pass-Kriterium 2 nur teilweise: der Transport ist per CLI-Flag `--http`/`--host`/`--port` waehlbar, nicht per ENV-Var. In einer Container-/PaaS-Umgebung, in der nur Env gesetzt werden kann, ist der HTTP-Modus nicht erreichbar, ohne das Kommando zu aendern.
- Kein Test, der dasselbe Tool-Resultat ueber beide Transporte vergleicht (Modus 3 des Checks). Ich habe die Aequivalenz nur fuer tools/list gemessen, nicht fuer einen Tool-Call ueber stdio.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-004.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-005

## Finding: ARCH-005 — Keine Hardcoded Secrets: Env-Vars / Secret Manager only

**Severity:** critical
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-005
**Katalog-Referenz:** Sec 2.1
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Keine hardcodierten Secrets: `git ls-files -z | xargs -0 grep -EIin "(api[_-]?key|password|secret|token)[ ]*[:=][ ]*[\"'][^\"']{16,}[\"']"` ueber alle versionierten Dateien → 0 Treffer. Negativkontrolle mit demselben Muster gegen eine Probe-Datei mit `API_KEY = "sk-1234567890abcdefXYZ"` → 1 Treffer, das Muster greift (eine erste Fassung ohne `-i` fand die Probe NICHT und haette eine falsche Null geliefert).
- Keine Connection-Strings / AWS-Keys: `grep -rEn "(postgres|mysql|mongodb)://[^:]+:[^@]+@|AKIA[0-9A-Z]{16}"` ueber src/, tests/, scripts/ → 0 Treffer; Negativkontrolle gegen `DB = "postgres://u:p@h/db"` → Treffer.
- src/eth_library_mcp/client.py:43-45 — `_get_api_key()` liest `os.environ.get("ETH_LIBRARY_API_KEY")` ohne Default. Der einzige `os.environ.get` mit nicht-leerem Default ist server.py:59 (`ETH_LIBRARY_LOG_LEVEL`, "INFO") — kein Secret.
- .gitignore:29-31 fuehrt `.env`, `.env.*` und `!.env.example`; im Arbeitsbaum existiert nur `.env.example` (214 Bytes, Inhalt `ETH_LIBRARY_API_KEY=replace-with-real-key`), und `git ls-files` listet an Secret-nahen Pfaden nur `.env.example` und `docs/secret-management.md`.
- GEMESSENER LEAK: mit `ETH_LIBRARY_API_KEY=sk-SECRET-TESTKEY-123456` und einem respx-gemockten Aufruf von eth_search_resources schreibt der Prozess auf stderr: `HTTP Request: GET https://api.library.ethz.ch/discovery/v1/resources?...&apikey=sk-SECRET-TESTKEY-123456 "HTTP/1.1 200 OK"`. Ursache: client.py:67-68 haengt den Schluessel als Query-Parameter an, und logging_config.py:26-31 ruft `logging.basicConfig(stream=sys.stderr, level=INFO)`, womit der httpx-Logger auf INFO in denselben stderr-Strom schreibt. Grep auf den Schluessel im aufgezeichneten stderr: 1 Treffer.
- Kein CI-Secret-Scan: `grep -rniE "gitleaks|trufflehog|secret.scan" .github/` → 0 Treffer ueber ci.yml, publish.yml, live-tests.yml, dependabot.yml, pull_request_template.md. Negativkontrolle gegen eine Probe-Datei mit `uses: gitleaks/gitleaks-action@v2` → Treffer.
- Keine `SecretStr`-Repraesentation: `grep -rn "SecretStr"` in src/ → 0 Treffer, Negativkontrolle gegen Probe-Datei → Treffer. Der Schluessel liegt als nacktes `str` vor (client.py:64-68).

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-005.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Keine hardcodierten Secrets: `git ls-files -z | xargs -0 grep -EIin "(api[_-]?key|password|secret|token)[ ]*[:=][ ]*[\"'][^\"']{16,}[\"']"` ueber alle versionierten Dateien → 0 Treffer. Negativkontrolle mit demselben Muster gegen eine Probe-Datei mit `API_KEY = "sk-1234567890abcdefXYZ"` → 1 Treffer, das Muster greift (eine erste Fassung ohne `-i` fand die Probe NICHT und haette eine falsche Null geliefert).
- Keine Connection-Strings / AWS-Keys: `grep -rEn "(postgres|mysql|mongodb)://[^:]+:[^@]+@|AKIA[0-9A-Z]{16}"` ueber src/, tests/, scripts/ → 0 Treffer; Negativkontrolle gegen `DB = "postgres://u:p@h/db"` → Treffer.
- src/eth_library_mcp/client.py:43-45 — `_get_api_key()` liest `os.environ.get("ETH_LIBRARY_API_KEY")` ohne Default. Der einzige `os.environ.get` mit nicht-leerem Default ist server.py:59 (`ETH_LIBRARY_LOG_LEVEL`, "INFO") — kein Secret.
- .gitignore:29-31 fuehrt `.env`, `.env.*` und `!.env.example`; im Arbeitsbaum existiert nur `.env.example` (214 Bytes, Inhalt `ETH_LIBRARY_API_KEY=replace-with-real-key`), und `git ls-files` listet an Secret-nahen Pfaden nur `.env.example` und `docs/secret-management.md`.
- GEMESSENER LEAK: mit `ETH_LIBRARY_API_KEY=sk-SECRET-TESTKEY-123456` und einem respx-gemockten Aufruf von eth_search_resources schreibt der Prozess auf stderr: `HTTP Request: GET https://api.library.ethz.ch/discovery/v1/resources?...&apikey=sk-SECRET-TESTKEY-123456 "HTTP/1.1 200 OK"`. Ursache: client.py:67-68 haengt den Schluessel als Query-Parameter an, und logging_config.py:26-31 ruft `logging.basicConfig(stream=sys.stderr, level=INFO)`, womit der httpx-Logger auf INFO in denselben stderr-Strom schreibt. Grep auf den Schluessel im aufgezeichneten stderr: 1 Treffer.
- Kein CI-Secret-Scan: `grep -rniE "gitleaks|trufflehog|secret.scan" .github/` → 0 Treffer ueber ci.yml, publish.yml, live-tests.yml, dependabot.yml, pull_request_template.md. Negativkontrolle gegen eine Probe-Datei mit `uses: gitleaks/gitleaks-action@v2` → Treffer.
- Keine `SecretStr`-Repraesentation: `grep -rn "SecretStr"` in src/ → 0 Treffer, Negativkontrolle gegen Probe-Datei → Treffer. Der Schluessel liegt als nacktes `str` vor (client.py:64-68).

### Gaps

- Der API-Key landet im Klartext im stderr-Log, sobald er gesetzt ist — gemessen, nicht vermutet. Das verletzt das Pass-Kriterium 'Secrets erscheinen nicht in Log-Outputs' und widerspricht zwei schriftlichen Zusicherungen: docs/secret-management.md:7-9 ('never persisted, logged, or transmitted anywhere other than the upstream API') und SECURITY.md:30 ('it is never logged'). Abhilfe: den Key als Header statt als Query-Parameter senden, oder den `httpx`-Logger in configure_logging() auf WARNING setzen.
- Kein Gitleaks-/Trufflehog-Lauf in der CI (Pass-Kriterium 8 unerfuellt). Ein History-Scan konnte ich mangels Tool in dieser Umgebung nicht fahren — das Urteil stuetzt sich auf Pattern-Suche ueber den aktuellen Baum, nicht ueber die Git-History.
- Keine `SecretStr`-Repraesentation im Speicher (Pass-Kriterium 4). Ein `repr()` eines Settings-Objekts gaebe den Wert preis; praktisch entschaerft, weil es kein solches Objekt gibt und der Wert bei jedem Aufruf frisch aus der Umgebung gelesen wird.
- docs/secret-management.md:8 nennt als Fundstelle `src/eth_library_mcp/server.py`, seit dem Modul-Split von 0.3.0 liegt `_get_api_key()` aber in client.py:43.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `critical`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-005.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-007

## Finding: ARCH-007 — Capability-Aggregation: Composability intern, Atomarität extern

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-007
**Katalog-Referenz:** Sec 2.3
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Gedanklich abgeschlossene Resultate: formatting.py:34-60 (`_format_resource_summary`) rendert pro Treffer Titel, Autor:in, Jahr, Typ, MMS-ID und DOI; die Such-Tools haengen Trefferzahl, Bereichsangabe, Pagination-Hinweis und Quellenangabe an (server.py:302-322). Gemessen an einem respx-Mock mit einem Treffer enthaelt die Antwort von eth_search_resources bereits Titel und 'Treffer'-Zeile — der Aufrufer braucht keinen Folge-Call fuer eine erste vollstaendige Antwort.
- formatting.py:62-113 (`_format_resource_detail`) liefert bei eth_get_resource ein abgeschlossenes Dokument inkl. Mitwirkenden, ISSN/ISBN/DOI, Schlagworten, Beschreibung und bis zu 5 Delivery-Links — kein blosser Pointer.
- Anchor-Demo-Query mit 1 Tool-Call belegt (EXAMPLES.md:9-10, :39-40, :54-55); Synergie-Kriterium zu ARCH-006 erfuellt.
- KEINE interne Parallel-Aggregation: `grep -rn 'asyncio.gather|Promise.all|TaskGroup'` ueber src/ → 0 Treffer, und `import asyncio` kommt in src/ gar nicht vor. Negativkontrolle gegen eine Probe-Datei mit `a, b = await asyncio.gather(x(), y())` → 1 Treffer, das Muster greift. Jedes Tool macht genau einen `_http_get` (server.py:291, 379, 448, 544, 646) — selbst am respx-Routenzaehler bestaetigt (call_count == 1 je Aufruf).
- Die beiden Prompts schieben die Orchestrierung ausdruecklich an das LLM: server.py:779-791 (`research-workflow`) schreibt fuenf nummerierte Schritte ueber vier verschiedene Tools vor ('Starte mit eth_library_info ... Suche mit eth_search_resources ... Suche auch in den relevanten Archiven ... Rufe die vielversprechendsten Ressourcen via eth_get_resource ab'); server.py:793-803 (`education-research`) vier Schritte ueber drei Tools. Das ist genau das Fail-Pattern 'LLM muss jetzt selbst orchestrieren'.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-007.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Gedanklich abgeschlossene Resultate: formatting.py:34-60 (`_format_resource_summary`) rendert pro Treffer Titel, Autor:in, Jahr, Typ, MMS-ID und DOI; die Such-Tools haengen Trefferzahl, Bereichsangabe, Pagination-Hinweis und Quellenangabe an (server.py:302-322). Gemessen an einem respx-Mock mit einem Treffer enthaelt die Antwort von eth_search_resources bereits Titel und 'Treffer'-Zeile — der Aufrufer braucht keinen Folge-Call fuer eine erste vollstaendige Antwort.
- formatting.py:62-113 (`_format_resource_detail`) liefert bei eth_get_resource ein abgeschlossenes Dokument inkl. Mitwirkenden, ISSN/ISBN/DOI, Schlagworten, Beschreibung und bis zu 5 Delivery-Links — kein blosser Pointer.
- Anchor-Demo-Query mit 1 Tool-Call belegt (EXAMPLES.md:9-10, :39-40, :54-55); Synergie-Kriterium zu ARCH-006 erfuellt.
- KEINE interne Parallel-Aggregation: `grep -rn 'asyncio.gather|Promise.all|TaskGroup'` ueber src/ → 0 Treffer, und `import asyncio` kommt in src/ gar nicht vor. Negativkontrolle gegen eine Probe-Datei mit `a, b = await asyncio.gather(x(), y())` → 1 Treffer, das Muster greift. Jedes Tool macht genau einen `_http_get` (server.py:291, 379, 448, 544, 646) — selbst am respx-Routenzaehler bestaetigt (call_count == 1 je Aufruf).
- Die beiden Prompts schieben die Orchestrierung ausdruecklich an das LLM: server.py:779-791 (`research-workflow`) schreibt fuenf nummerierte Schritte ueber vier verschiedene Tools vor ('Starte mit eth_library_info ... Suche mit eth_search_resources ... Suche auch in den relevanten Archiven ... Rufe die vielversprechendsten Ressourcen via eth_get_resource ab'); server.py:793-803 (`education-research`) vier Schritte ueber drei Tools. Das ist genau das Fail-Pattern 'LLM muss jetzt selbst orchestrieren'.

### Gaps

- Pass-Kriterium 2 unerfuellt, wo Aggregation Sinn ergaebe: der Workflow 'Thema recherchieren' (der eigene `research-workflow`-Prompt) verlangt 4-5 Tool-Calls, die der Server in einem Tool parallel (asyncio.gather ueber Discovery-Suche + Archivsuche + Detailabrufe) buendeln koennte. Es gibt kein einziges aggregierendes Tool.
- eth_get_resource setzt eine MMS-ID voraus, die nur aus einem vorherigen Such-Call stammt — die im Check beschriebene Zwei-Schritt-Kette (getXId → getXDetails) besteht hier faktisch, auch wenn der Suchtreffer schon nutzbare Metadaten mitliefert.
- Pass-Kriterium 3 (Beschreibung erwaehnt den aggregierten Charakter) ist gegenstandslos, weil nicht aggregiert wird — das zaehlt nicht als Erfuellung.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-007.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-009

## Finding: ARCH-009 — Tool Annotations: readOnlyHint, destructiveHint, idempotentHint, openWorldHint

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-009
**Katalog-Referenz:** Anhang A5
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- ALLE 6 Tools tragen explizite Annotations, gemessen an `mcp.list_tools()` und zusaetzlich am Draht: der POST `tools/list` durch build_http_app() liefert pro Tool `{"destructiveHint":false,"idempotentHint":true,"openWorldHint":true,"readOnlyHint":true,"title":"..."}`. Kein Tool verlaesst sich auf Defaults durch Weglassen.
- Quelltext-Fundstellen: src/eth_library_mcp/server.py:246-255 (eth_search_resources), :358-366 (eth_get_resource), :422-430 (eth_search_archive), :513-521 (eth_search_by_type), :612-620 (eth_search_education), :689-697 (eth_library_info) — jeweils alle vier Hints plus `title`.
- readOnlyHint konsistent mit dem Verhalten: alle 5 netzsprechenden Tools nutzen ausschliesslich `_http_get` (server.py:291, 379, 448, 544, 646). Suche nach `\.(post|put|patch|delete)\(` ueber src/*.py → 0 Treffer; Negativkontrolle gegen eine Probe-Datei mit `client.post(url)` und `c.delete(u)` → 2 Treffer, das Muster greift. Kein Tool traegt create/update/delete/remove im Namen (gemessene Tool-Liste).
- idempotentHint=True ist korrekt: jeder Aufruf ist ein GET ohne Server-Zustandsaenderung; derselbe Aufruf liefert am gemockten Upstream dasselbe Resultat (selbst gefahren, respx).
- openWorldHint differenziert: 5 Tools True (erreichen api.library.ethz.ch), eth_library_info False — und die Zusicherung ist getestet, nicht nur behauptet (tests/test_tools.py:183-188 `test_library_info_no_network`, ohne respx-Route; ein Netzaufruf wuerde dort scheitern).
- destructiveHint ist bei allen 6 explizit auf False gesetzt statt weggelassen — der Default waere laut Spec True gewesen.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-009.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- ALLE 6 Tools tragen explizite Annotations, gemessen an `mcp.list_tools()` und zusaetzlich am Draht: der POST `tools/list` durch build_http_app() liefert pro Tool `{"destructiveHint":false,"idempotentHint":true,"openWorldHint":true,"readOnlyHint":true,"title":"..."}`. Kein Tool verlaesst sich auf Defaults durch Weglassen.
- Quelltext-Fundstellen: src/eth_library_mcp/server.py:246-255 (eth_search_resources), :358-366 (eth_get_resource), :422-430 (eth_search_archive), :513-521 (eth_search_by_type), :612-620 (eth_search_education), :689-697 (eth_library_info) — jeweils alle vier Hints plus `title`.
- readOnlyHint konsistent mit dem Verhalten: alle 5 netzsprechenden Tools nutzen ausschliesslich `_http_get` (server.py:291, 379, 448, 544, 646). Suche nach `\.(post|put|patch|delete)\(` ueber src/*.py → 0 Treffer; Negativkontrolle gegen eine Probe-Datei mit `client.post(url)` und `c.delete(u)` → 2 Treffer, das Muster greift. Kein Tool traegt create/update/delete/remove im Namen (gemessene Tool-Liste).
- idempotentHint=True ist korrekt: jeder Aufruf ist ein GET ohne Server-Zustandsaenderung; derselbe Aufruf liefert am gemockten Upstream dasselbe Resultat (selbst gefahren, respx).
- openWorldHint differenziert: 5 Tools True (erreichen api.library.ethz.ch), eth_library_info False — und die Zusicherung ist getestet, nicht nur behauptet (tests/test_tools.py:183-188 `test_library_info_no_network`, ohne respx-Route; ein Netzaufruf wuerde dort scheitern).
- destructiveHint ist bei allen 6 explizit auf False gesetzt statt weggelassen — der Default waere laut Spec True gewesen.

### Gaps

- Pass-Kriterium 6 unerfuellt: es gibt keine Annotations-Uebersicht in README.md, README.de.md oder docs/. Gemessen mit whitespace-normalisierter Suche nach readOnlyHint/destructiveHint/idempotentHint/openWorldHint/Annotation ueber README.md, README.de.md, docs/ARCHITECTURE.md, SECURITY.md, SECURITY.de.md: einziger Treffer ist SECURITY.md:29 bzw. SECURITY.de.md — eine Zeile 'Every tool sets readOnlyHint: True', keine Tabelle, und SECURITY.md ist keiner der vom Check akzeptierten Orte. Positivkontrolle: dieselbe Suche findet den Begriff dort, wo er steht (SECURITY.md), also greift sie.
- Damit ist auch nicht dokumentiert, dass destructiveHint/idempotentHint/openWorldHint gesetzt sind und nach welcher Policy — die SECURITY-Zeile nennt nur readOnlyHint.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-009.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-011

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


### ARCH-012

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


### ARCH-013

## Finding: ARCH-013 — Alle Netz-Transportpfade identisch verdrahtet

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-013
**Katalog-Referenz:** Sec 2.1
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/server.py:903 — `build_http_app(host, port)` ist die EINZIGE Stelle, die eine ASGI-App konstruiert; :926 `mcp.streamable_http_app(transport_security=security, host=host)`, :957 `_run_http` ruft `uvicorn.run(build_http_app(host, port), host=host, port=port)`, :973 `mcp.run()` (stdio). Grep nach `sse_app(|http_app(|def .*factory|--factory` ueber src/ findet keinen weiteren Pfad; Negativkontrolle: dasselbe Muster gegen /tmp/psse.py mit `mcp.sse_app()` trifft (1 Zeile), das Muster greift also.
- Dockerfile:35-36 — ENTRYPOINT ["python","-m","eth_library_mcp.server"] + CMD ["--http","--host","0.0.0.0","--port","8000"]; dieser Pfad laeuft durch denselben `__main__`-Block (server.py:962-972) und damit durch denselben Builder. railway.toml, render.yaml, Procfile und docker-compose*.yml existieren nicht (ls: No such file); `--factory`/`gunicorn` kommt nirgends vor.
- Gemessene Naht (uvicorn durch einen Stub ersetzt, `python -m eth_library_mcp.server --http --host 127.0.0.1 --port 8123`): uvicorn.run bekam host='127.0.0.1' port=8123 UND die App trug TransportSecuritySettings(allowed_hosts=['127.0.0.1:8123','[::1]:8123','localhost:8123']). Der Port reist also vollstaendig von argv bis in die Freigabeliste — Fail-Pattern 2 (Port intern gedefaultet) liegt nicht vor.
- Gemessene Routentabelle von build_http_app(): app.routes == [('/mcp', None)] — genau ein Netzweg. GET /sse -> 404, GET /messages -> 404, DELETE /sse -> 404: kein Legacy-SSE-Pfad neben Streamable HTTP. Negativkontrolle derselben Sonde: GET /mcp -> 400 und GET /mcp/ -> 307, die Sonde unterscheidet also 404 von bedienten Pfaden.
- Gemessen mit demselben Stub: `--host 0.0.0.0` ohne ETH_LIBRARY_ALLOWED_HOSTS -> transport_security None plus Log `dns_rebinding_protection_off`; mit ETH_LIBRARY_ALLOWED_HOSTS=mcp.example.ch -> allowed_hosts ['127.0.0.1:8000','[::1]:8000','localhost:8000','mcp.example.ch']. Die Scharfschaltung haengt an der Host-Freigabeliste selbst, nicht an einer sachfremden Bedingung (Auth/CORS/Debug).

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-013.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/server.py:903 — `build_http_app(host, port)` ist die EINZIGE Stelle, die eine ASGI-App konstruiert; :926 `mcp.streamable_http_app(transport_security=security, host=host)`, :957 `_run_http` ruft `uvicorn.run(build_http_app(host, port), host=host, port=port)`, :973 `mcp.run()` (stdio). Grep nach `sse_app(|http_app(|def .*factory|--factory` ueber src/ findet keinen weiteren Pfad; Negativkontrolle: dasselbe Muster gegen /tmp/psse.py mit `mcp.sse_app()` trifft (1 Zeile), das Muster greift also.
- Dockerfile:35-36 — ENTRYPOINT ["python","-m","eth_library_mcp.server"] + CMD ["--http","--host","0.0.0.0","--port","8000"]; dieser Pfad laeuft durch denselben `__main__`-Block (server.py:962-972) und damit durch denselben Builder. railway.toml, render.yaml, Procfile und docker-compose*.yml existieren nicht (ls: No such file); `--factory`/`gunicorn` kommt nirgends vor.
- Gemessene Naht (uvicorn durch einen Stub ersetzt, `python -m eth_library_mcp.server --http --host 127.0.0.1 --port 8123`): uvicorn.run bekam host='127.0.0.1' port=8123 UND die App trug TransportSecuritySettings(allowed_hosts=['127.0.0.1:8123','[::1]:8123','localhost:8123']). Der Port reist also vollstaendig von argv bis in die Freigabeliste — Fail-Pattern 2 (Port intern gedefaultet) liegt nicht vor.
- Gemessene Routentabelle von build_http_app(): app.routes == [('/mcp', None)] — genau ein Netzweg. GET /sse -> 404, GET /messages -> 404, DELETE /sse -> 404: kein Legacy-SSE-Pfad neben Streamable HTTP. Negativkontrolle derselben Sonde: GET /mcp -> 400 und GET /mcp/ -> 307, die Sonde unterscheidet also 404 von bedienten Pfaden.
- Gemessen mit demselben Stub: `--host 0.0.0.0` ohne ETH_LIBRARY_ALLOWED_HOSTS -> transport_security None plus Log `dns_rebinding_protection_off`; mit ETH_LIBRARY_ALLOWED_HOSTS=mcp.example.ch -> allowed_hosts ['127.0.0.1:8000','[::1]:8000','localhost:8000','mcp.example.ch']. Die Scharfschaltung haengt an der Host-Freigabeliste selbst, nicht an einer sachfremden Bedingung (Auth/CORS/Debug).

### Gaps

- Kein Test prueft die Naht, nur den Builder: tests/test_cors.py:50, tests/test_transport_security.py:72/90/102, tests/test_server_identity.py:86/170 und tests/test_protocol_version.py:140 rufen alle `build_http_app(...)` direkt mit expliziten Argumenten auf. Die argv-Auswertung in server.py:962-972 und `_run_http` (server.py:953-957) sind von keinem Test beruehrt (grep nach `_run_http|sys.argv|__main__` ueber tests/ findet nur tests/test_classify_live_run.py:220, ein eigenes `__main__`). Das ist genau das im Check benannte Anti-Pattern «Test ruft den Builder direkt mit allen Parametern».
- Gegenprobe nach Pass-Kriterium 8 (Verdrahtung aus je einem Pfad entfernen, mindestens ein Test muss fallen) ist im Repo nicht gefuehrt und liesse sich mit der heutigen Testlage auch nicht fuehren: fiele `host=`/`transport_security=` in `_run_http` weg, bliebe die Suite gruen, weil kein Test durch diese Funktion laeuft.
- Der ausgelieferte Dockerfile-Default (`--host 0.0.0.0` ohne gesetzte ETH_LIBRARY_ALLOWED_HOSTS) schaltet die DNS-Rebinding-Pruefung ab — gemessen oben. Der Dockerfile setzt die Variable nicht und nennt sie nicht; der Hinweis existiert nur als Laufzeit-Warnung in server.py:911-918.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-013.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-016

## Finding: ARCH-016 — server/discover ist implementiert — der RPC ist MUSS, nicht Kür

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-016
**Katalog-Referenz:** SEP-2575
**Spec-Baseline:** 2026-07-28
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Streamable HTTP GEMESSEN durch build_http_app(): `server/discover` antwortet mit allen DREI Bestandteilen — supportedVersions: ["2026-07-28"] (Liste, kein String), capabilities: {prompts:{listChanged},resources:{listChanged,subscribe},tools:{listChanged}}, und Identitaet in _meta["io.modelcontextprotocol/serverInfo"] = {name: "eth_library_mcp", title: "ETH-Bibliothek Zuerich", version: "0.4.0", description, websiteUrl}.
- stdio GEMESSEN (ARCH-013-Kriterium «ueber jeden bedienten Transportpfad»): derselbe JSON-RPC-Request ueber `mcp.run()` als Subprozess (PYTHONPATH=src, stdin/stdout) lieferte ein inhaltlich identisches Resultat, inklusive supportedVersions, capabilities und serverInfo-Stempel. Beide Pfade bedienen den RPC.
- Die Version im Stempel stammt aus den Paket-Metadaten, nicht aus einem Literal: src/eth_library_mcp/__init__.py:15 `__version__ = _distribution_version("eth-library-mcp")`, server.py:172 `version=__version__`; gemessener Wert 0.4.0 == importlib.metadata.version('eth-library-mcp'). tests/test_server_identity.py:157 vergleicht genau dagegen statt gegen eine Zahl.
- Der RPC stammt aus dem SDK, nicht aus diesem Repo: grep -rnE "server/discover|server_discover|def discover|DiscoverResult" ueber src/ trifft nur server.py:144, und das ist ein Cache-Hint-Schluessel, kein Handler. SDK-Untergrenze gepinnt in pyproject.toml:29 `mcp[cli]>=2.0.0,<3`; installiert und gemessen: mcp 2.2.0.
- Negativkontrolle der Laufzeitsonde: `server/discoverX` durch denselben Stack -> HTTP 404 mit {"code": -32601, "message": "Method not found"}. Die Sonde unterscheidet also einen bedienten von einem unbekannten RPC; das gemessene 200 auf server/discover ist ein positiver Beleg und kein Artefakt.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-016.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Streamable HTTP GEMESSEN durch build_http_app(): `server/discover` antwortet mit allen DREI Bestandteilen — supportedVersions: ["2026-07-28"] (Liste, kein String), capabilities: {prompts:{listChanged},resources:{listChanged,subscribe},tools:{listChanged}}, und Identitaet in _meta["io.modelcontextprotocol/serverInfo"] = {name: "eth_library_mcp", title: "ETH-Bibliothek Zuerich", version: "0.4.0", description, websiteUrl}.
- stdio GEMESSEN (ARCH-013-Kriterium «ueber jeden bedienten Transportpfad»): derselbe JSON-RPC-Request ueber `mcp.run()` als Subprozess (PYTHONPATH=src, stdin/stdout) lieferte ein inhaltlich identisches Resultat, inklusive supportedVersions, capabilities und serverInfo-Stempel. Beide Pfade bedienen den RPC.
- Die Version im Stempel stammt aus den Paket-Metadaten, nicht aus einem Literal: src/eth_library_mcp/__init__.py:15 `__version__ = _distribution_version("eth-library-mcp")`, server.py:172 `version=__version__`; gemessener Wert 0.4.0 == importlib.metadata.version('eth-library-mcp'). tests/test_server_identity.py:157 vergleicht genau dagegen statt gegen eine Zahl.
- Der RPC stammt aus dem SDK, nicht aus diesem Repo: grep -rnE "server/discover|server_discover|def discover|DiscoverResult" ueber src/ trifft nur server.py:144, und das ist ein Cache-Hint-Schluessel, kein Handler. SDK-Untergrenze gepinnt in pyproject.toml:29 `mcp[cli]>=2.0.0,<3`; installiert und gemessen: mcp 2.2.0.
- Negativkontrolle der Laufzeitsonde: `server/discoverX` durch denselben Stack -> HTTP 404 mit {"code": -32601, "message": "Method not found"}. Die Sonde unterscheidet also einen bedienten von einem unbekannten RPC; das gemessene 200 auf server/discover ist ein positiver Beleg und kein Artefakt.

### Gaps

- Kein Test prueft die drei Bestandteile einzeln. Die einzige Zusicherung auf server/discover ist tests/test_server_identity.py:152-157 und prueft ausschliesslich `info.get("version")`; supportedVersions und capabilities sind von keinem Test beruehrt (grep "server/discover" ueber tests/ findet nur diese Stelle plus zwei Docstring-Zeilen). Kriterium «Ein Test ... prueft alle drei Bestandteile einzeln» unerfuellt.
- Keine Gegenprobe gegen einen Server OHNE den Handler. tests/test_server_identity.py:203-234 ist eine Gegenprobe fuer den Versionsstempel (MCPServer ohne `version=`), nicht fuer die Existenz des RPC. Kriterium 7 unerfuellt.
- Die gepinnte Untergrenze ist nicht nachgemessen: beobachtet ist nur, dass mcp 2.2.0 den RPC fuehrt. Ob `>=2.0.0` ihn bereits enthaelt, wurde nicht geprueft (kein Netzzugriff auf den Index); die Konformitaet haengt insoweit an der zufaellig installierten Version.
- Nebenbefund ausserhalb dieses Checks, weil von diesem RPC ausgeliefert: die gemessenen `instructions` (server.py:180) werben weiterhin mit «Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung» — ein Werkzeug, das in 0.4.0 entfernt wurde. Gehoert zu IDENT/FID.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-016.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-018

## Finding: ARCH-018 — resultType auf allen Results — «complete» ist kein Default, den man weglässt

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-018
**Katalog-Referenz:** SEP-2322
**Spec-Baseline:** 2026-07-28
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Am Draht GEMESSEN durch build_http_app(), moderne Aera: `resultType: "complete"` liegt auf tools/list, resources/list, resources/templates/list, prompts/list, server/discover, resources/read, prompts/get und tools/call an. Beispiel tools/list, vollstaendige Schluesselmenge des result: ['_meta','cacheScope','resultType','tools','ttlMs'].
- Fehlerpfad GEMESSEN, getrennt vom Erfolgspfad: tools/call auf ein unbekanntes Werkzeug -> {"content":[{"text":"Unknown tool: does_not_exist",...}],"isError":true,"resultType":"complete",...}; tools/call auf eth_get_resource mit einem Argument, das die Pydantic-Validierung verletzt (mmsid="") -> ebenfalls isError true UND resultType "complete". Beide Ergebniswege tragen das Feld.
- Das Feld stammt aus dem SDK, nicht aus diesem Repo: grep -rnE "resultType|result_type" ueber src/ UND tests/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Wort steht in /usr/local/lib/python3.11/dist-packages/mcp_types/_types.py:167/171/221 und in mcp/server/{connection,runner,session}.py — das Muster greift. Installierte und gemessene SDK-Version: mcp 2.2.0.
- SDK-Untergrenze im Manifest gepinnt: pyproject.toml:29 `"mcp[cli]>=2.0.0,<3"`. Der Server fuehrt kein MRTR (kein tasks/*, gemessen: tasks/list -> -32601), `"input_required"` kommt folglich nirgends vor.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-018.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Am Draht GEMESSEN durch build_http_app(), moderne Aera: `resultType: "complete"` liegt auf tools/list, resources/list, resources/templates/list, prompts/list, server/discover, resources/read, prompts/get und tools/call an. Beispiel tools/list, vollstaendige Schluesselmenge des result: ['_meta','cacheScope','resultType','tools','ttlMs'].
- Fehlerpfad GEMESSEN, getrennt vom Erfolgspfad: tools/call auf ein unbekanntes Werkzeug -> {"content":[{"text":"Unknown tool: does_not_exist",...}],"isError":true,"resultType":"complete",...}; tools/call auf eth_get_resource mit einem Argument, das die Pydantic-Validierung verletzt (mmsid="") -> ebenfalls isError true UND resultType "complete". Beide Ergebniswege tragen das Feld.
- Das Feld stammt aus dem SDK, nicht aus diesem Repo: grep -rnE "resultType|result_type" ueber src/ UND tests/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Wort steht in /usr/local/lib/python3.11/dist-packages/mcp_types/_types.py:167/171/221 und in mcp/server/{connection,runner,session}.py — das Muster greift. Installierte und gemessene SDK-Version: mcp 2.2.0.
- SDK-Untergrenze im Manifest gepinnt: pyproject.toml:29 `"mcp[cli]>=2.0.0,<3"`. Der Server fuehrt kein MRTR (kein tasks/*, gemessen: tasks/list -> -32601), `"input_required"` kommt folglich nirgends vor.

### Gaps

- Kein Test prueft `resultType` am tatsaechlichen Wire-Format — grep ueber tests/ findet das Feld gar nicht. Das im Check benannte Kriterium («nicht am Rueckgabewert der Python-Funktion, sondern am Draht») ist unerfuellt; die Konformitaet ruht vollstaendig darauf, dass das SDK das Feld weiterhin setzt, und nichts im Repo meldet den Tag, an dem es das nicht mehr tut. Die vorhandenen Draht-Tests (tests/test_server_identity.py:86-105, tests/test_cache_hints.py) fahren bereits genau den Stack, in dem die Zusicherung stehen muesste.
- Die gepinnte Untergrenze `>=2.0.0` ist nicht nachgemessen: beobachtet ist nur, dass 2.2.0 das Feld setzt.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-018.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-019

## Finding: ARCH-019 — Roots, Sampling und Logging: keine Neuimplementierung, Bestand mit Fristdatum

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-019
**Katalog-Referenz:** SEP-2577
**Spec-Baseline:** beide
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- BEFUND: Der Server nutzt das deprecatete Logging-Protokoll-Feature an fuenf Stellen — src/eth_library_mcp/server.py:326, :386, :476, :575, :680, jeweils `await ctx.warning(...)`. `mcp.server.mcpserver.Context.warning` traegt im SDK den Dekorator @deprecated("The logging capability is deprecated as of 2026-07-28 (SEP-2577).") und leitet auf `Context.log` -> `session.send_log_message` weiter, also auf `notifications/message`. Quelle: inspect.getsource(Context.warning) auf mcp 2.2.0.
- Zur Laufzeit BEOBACHTET, nicht geschlossen: ein Aufruf von eth_get_resource ueber einen echten `mcp.Client` mit auf Raise gepatchtem `_http_get` erzeugte drei Warnungen `MCPDeprecationWarning: The logging capability is deprecated as of 2026-07-28 (SEP-2577).` (warning -> log -> send_log_message). Der Fehlerpfad jedes der fuenf Tools loest das aus.
- Die Modus-1-Greps des Katalogs finden diese Nutzung NICHT: grep -rnE "logging/setLevel|set_level|LoggingCapability|notifications/message" ueber src/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen mcp/server/connection.py trifft (Zeilen 70, 425) — das Muster greift, es kennt nur die Convenience-Wrapper des SDK nicht.
- Roots und Sampling: keine Nutzung. grep -rnE "roots/list|RootsCapability|list_roots|ListRootsRequest" -> 0, grep -rnE "sampling/createMessage|create_message|CreateMessageRequest|samplingCapability" -> 0 (beide exit 1); Negativkontrollen gegen mcp/shared/peer.py:223 bzw. :158 treffen. Laufzeit GEMESSEN: roots/list, sampling/createMessage und logging/setLevel antworten je mit -32601 "Method not found".
- Kriterium 6 erfuellt, gemessen: die von server/discover ausgelieferten capabilities nennen ausschliesslich prompts, resources und tools — keines der drei deprecateten Features wird angekuendigt.
- Kriterium 5 erfuellt: das Anwendungs-Logging liegt unangetastet auf stderr — src/eth_library_mcp/logging_config.py:26-31 `logging.basicConfig(stream=sys.stderr)` und :46 `structlog.PrintLoggerFactory(file=sys.stderr)`, JSON-Renderer. Das ist genau die von der Spec empfohlene Migration und erfuellt weiterhin OBS-003.
- Historie zur Frage «neue Nutzung»: `git log -S"ctx.warning"` nennt genau zwei Commits — 5e37092 (2026-06-04), der die Aufrufe einfuehrte, und 3de3348 (2026-08-08), der ihre Zahl verringerte (Entfernung von eth_search_persons). Seit der Deprecation am 2026-07-28 ist also nichts Neues dazugekommen; eingefuehrt wurden sie allerdings nach dem Vorlauf-Audit vom 28.5.2026.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-019.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- BEFUND: Der Server nutzt das deprecatete Logging-Protokoll-Feature an fuenf Stellen — src/eth_library_mcp/server.py:326, :386, :476, :575, :680, jeweils `await ctx.warning(...)`. `mcp.server.mcpserver.Context.warning` traegt im SDK den Dekorator @deprecated("The logging capability is deprecated as of 2026-07-28 (SEP-2577).") und leitet auf `Context.log` -> `session.send_log_message` weiter, also auf `notifications/message`. Quelle: inspect.getsource(Context.warning) auf mcp 2.2.0.
- Zur Laufzeit BEOBACHTET, nicht geschlossen: ein Aufruf von eth_get_resource ueber einen echten `mcp.Client` mit auf Raise gepatchtem `_http_get` erzeugte drei Warnungen `MCPDeprecationWarning: The logging capability is deprecated as of 2026-07-28 (SEP-2577).` (warning -> log -> send_log_message). Der Fehlerpfad jedes der fuenf Tools loest das aus.
- Die Modus-1-Greps des Katalogs finden diese Nutzung NICHT: grep -rnE "logging/setLevel|set_level|LoggingCapability|notifications/message" ueber src/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen mcp/server/connection.py trifft (Zeilen 70, 425) — das Muster greift, es kennt nur die Convenience-Wrapper des SDK nicht.
- Roots und Sampling: keine Nutzung. grep -rnE "roots/list|RootsCapability|list_roots|ListRootsRequest" -> 0, grep -rnE "sampling/createMessage|create_message|CreateMessageRequest|samplingCapability" -> 0 (beide exit 1); Negativkontrollen gegen mcp/shared/peer.py:223 bzw. :158 treffen. Laufzeit GEMESSEN: roots/list, sampling/createMessage und logging/setLevel antworten je mit -32601 "Method not found".
- Kriterium 6 erfuellt, gemessen: die von server/discover ausgelieferten capabilities nennen ausschliesslich prompts, resources und tools — keines der drei deprecateten Features wird angekuendigt.
- Kriterium 5 erfuellt: das Anwendungs-Logging liegt unangetastet auf stderr — src/eth_library_mcp/logging_config.py:26-31 `logging.basicConfig(stream=sys.stderr)` und :46 `structlog.PrintLoggerFactory(file=sys.stderr)`, JSON-Renderer. Das ist genau die von der Spec empfohlene Migration und erfuellt weiterhin OBS-003.
- Historie zur Frage «neue Nutzung»: `git log -S"ctx.warning"` nennt genau zwei Commits — 5e37092 (2026-06-04), der die Aufrufe einfuehrte, und 3de3348 (2026-08-08), der ihre Zahl verringerte (Entfernung von eth_search_persons). Seit der Deprecation am 2026-07-28 ist also nichts Neues dazugekommen; eingefuehrt wurden sie allerdings nach dem Vorlauf-Audit vom 28.5.2026.

### Gaps

- Kein dokumentiertes Fristdatum und kein Zielzustand: normalisierte Suche (Zeilenumbrueche geglaettet) nach `deprecat|abkuendig|abkuendig|rueckbau|2027-07-28|SEP-2577` ueber README.md, README.de.md und CHANGELOG.md -> 0 Treffer in allen drei Dateien. Negativkontrolle gegen eine Probedatei mit «Logging deprecated, Rueckbau bis 2027-07-28.» trifft. Damit sind die Kriterien 2 (Nutzung benannt mit Zielzustand und Datum), 3 (Datum nicht nach 2027-07-28) und 4 (Zielzustand entspricht der Spec-Empfehlung) unerfuellt — vorhandene Nutzung ohne Datum ist nach dem Check ein Vorsatz, kein Plan.
- Behebung waere klein und ist benannt: die fuenf `ctx.warning`-Aufrufe geben dieselbe Information bereits doppelt aus — `_handle_error` (formatting.py:161) loggt die Ausnahme auf stderr. Der Rueckbau ist damit ein Loeschen, kein Ersetzen; er braucht nur die Entscheidung und ein Datum im CHANGELOG.
- KATALOG-BEFUND: Die Verifikationsgreps dieses Checks koennen die haeufigste Form der Nutzung im Python-SDK nicht sehen. `Context.warning`, `Context.info`, `Context.debug`, `Context.error` und `Context.log` sind das deprecatete Feature, enthalten aber keinen der gesuchten Namen. Ein Server kann das Feature auf fuenf Zeilen nutzen und Modus 1 mit 0 Treffern bestehen — genau der «Grep meldet 0 Treffer, weil das Muster nie greift»-Fall, den der Check selbst in seiner Failure-Tabelle fuehrt.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-019.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-020

## Finding: ARCH-020 — ttlMs und cacheScope auf List- und Read-Ergebnissen, deterministische Reihenfolge

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-020
**Katalog-Referenz:** SEP-2549
**Spec-Baseline:** 2026-07-28
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Felder am ausgelieferten Result GEMESSEN (Modus 2, nicht am Quelltext entschieden): tools/list, resources/list, resources/templates/list und prompts/list tragen je ttlMs=300000 und cacheScope="public"; server/discover ebenso. Quelle: src/eth_library_mcp/server.py:133 `LIST_CACHE_TTL_MS = 300_000` und :139-145 `CACHE_HINTS`.
- Wertevorrat SEP-2549 eingehalten, am Draht geprueft: beobachtet wurden ausschliesslich "public" und "private", kein dritter Wert wie "session"/"caller"/"none". Modus-1-Grep mit Kontext bestaetigt, dass server.py:139-145 die einzige Quelle ist und dort nur `scope="public"`-Literale stehen; es gibt keine Mapping-Funktion, durch die ein anderer Wert nach draussen laufen koennte.
- resources/read GEMESSEN: ttlMs=0, cacheScope="private". Das ist bewusst so (server.py:130-132: ein Hinweis dort waere eine Zusicherung ueber den INHALT statt ueber das Verzeichnis) und im Repo gegatet — tests/test_cache_hints.py:44-57 haelt 0/private am ausgelieferten Result fest, :93-99 zusaetzlich an der Konfiguration.
- Deterministische Reihenfolge UEBER PROZESSGRENZEN gemessen, nicht innerhalb eines Interpreters: drei frische Prozesse mit PYTHONHASHSEED=random lieferten je dieselbe tools/list-Reihenfolge ['eth_search_resources','eth_get_resource','eth_search_archive','eth_search_by_type','eth_search_education','eth_library_info'], dieselbe resources/list- und dieselbe prompts/list-Reihenfolge. Negativkontrolle: dieselbe Messung ueber eine `set`-Iteration derselben sechs Namen, ebenfalls mit PYTHONHASHSEED=random, ergab drei VERSCHIEDENE Reihenfolgen — das Verfahren erkennt Instabilitaet.
- Negativkontrolle fuer die Hinweise selbst liegt im Repo: tests/test_cache_hints.py:67-77 fragt einen blanken `MCPServer("kontrolle")` ueber denselben Client und erwartet ttl_ms 0 / cache_scope private. Faellt das SDK eines Tages selbst einen Default ein, meldet dieser Test es.
- `public` ist hier sachlich gedeckt: data_class ist Public Open Data, die sechs Tools werden per Dekorator beim Import registriert, es gibt keine Filterung nach Aufrufer (server.py:123-127 begruendet das ausdruecklich) — gemessen dadurch, dass zwei getrennte Verbindungen dieselbe tools/list erhalten.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-020.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Felder am ausgelieferten Result GEMESSEN (Modus 2, nicht am Quelltext entschieden): tools/list, resources/list, resources/templates/list und prompts/list tragen je ttlMs=300000 und cacheScope="public"; server/discover ebenso. Quelle: src/eth_library_mcp/server.py:133 `LIST_CACHE_TTL_MS = 300_000` und :139-145 `CACHE_HINTS`.
- Wertevorrat SEP-2549 eingehalten, am Draht geprueft: beobachtet wurden ausschliesslich "public" und "private", kein dritter Wert wie "session"/"caller"/"none". Modus-1-Grep mit Kontext bestaetigt, dass server.py:139-145 die einzige Quelle ist und dort nur `scope="public"`-Literale stehen; es gibt keine Mapping-Funktion, durch die ein anderer Wert nach draussen laufen koennte.
- resources/read GEMESSEN: ttlMs=0, cacheScope="private". Das ist bewusst so (server.py:130-132: ein Hinweis dort waere eine Zusicherung ueber den INHALT statt ueber das Verzeichnis) und im Repo gegatet — tests/test_cache_hints.py:44-57 haelt 0/private am ausgelieferten Result fest, :93-99 zusaetzlich an der Konfiguration.
- Deterministische Reihenfolge UEBER PROZESSGRENZEN gemessen, nicht innerhalb eines Interpreters: drei frische Prozesse mit PYTHONHASHSEED=random lieferten je dieselbe tools/list-Reihenfolge ['eth_search_resources','eth_get_resource','eth_search_archive','eth_search_by_type','eth_search_education','eth_library_info'], dieselbe resources/list- und dieselbe prompts/list-Reihenfolge. Negativkontrolle: dieselbe Messung ueber eine `set`-Iteration derselben sechs Namen, ebenfalls mit PYTHONHASHSEED=random, ergab drei VERSCHIEDENE Reihenfolgen — das Verfahren erkennt Instabilitaet.
- Negativkontrolle fuer die Hinweise selbst liegt im Repo: tests/test_cache_hints.py:67-77 fragt einen blanken `MCPServer("kontrolle")` ueber denselben Client und erwartet ttl_ms 0 / cache_scope private. Faellt das SDK eines Tages selbst einen Default ein, meldet dieser Test es.
- `public` ist hier sachlich gedeckt: data_class ist Public Open Data, die sechs Tools werden per Dekorator beim Import registriert, es gibt keine Filterung nach Aufrufer (server.py:123-127 begruendet das ausdruecklich) — gemessen dadurch, dass zwei getrennte Verbindungen dieselbe tools/list erhalten.

### Gaps

- Die Reihenfolge stammt aus der Registrierungsreihenfolge (Dekorator-Reihenfolge in server.py), nicht aus einer expliziten Sortierung — Kriterium 7 unerfuellt. Sie ist heute stabil, weil Python-Dicts Einfuegereihenfolge bewahren, aber sie aendert sich mit jeder Umsortierung der Tool-Definitionen, und nichts meldet das: grep ueber tests/ nach `Reihenfolge|order|deterministi|PYTHONHASHSEED` findet keinen einzigen Reihenfolgetest (die Treffer auf `sorted` betreffen Workflow-Globs und Mengendifferenzen).
- resources/read wird mit ttlMs=0 ausgeliefert — im Check das Anti-Pattern «ttlMs: 0 als sicherer Wert». Die Begruendung («Aussage ueber den Inhalt») traegt hier nur halb: die beiden Ressourcen (RESOURCE_TYPES, ARCHIVE_SOURCES, server.py:90-111) sind Import-Zeit-Konstanten, deren Inhalt sich zur Prozesslaufzeit nicht aendern kann. Kriterium 2 damit fuer diese Methode unerfuellt.
- Der Server paginiert Query-Resultate (offset/limit werden an die Discovery-API durchgereicht, server.py:270, :443, :538), aber der Sortierschluessel ist nicht total: `sort` ist Literal['rank','title','author','date'] (server.py:65) ohne eindeutigen Zusatzschluessel — bei Gleichstand entscheidet die Quelle je Abruf neu. Kriterium 8 unerfuellt.
- Kein Test ueber zwei aufeinanderfolgende Seiten (leere Schnittmenge UND vollstaendige Vereinigung): grep ueber tests/ nach `offset|page|pagination|Seite` findet keinen solchen Test — das Muster ist nicht stumm, es trifft anderes (z.B. `Homepage`). Kriterium 9 unerfuellt. Ein solcher Test braeuchte `-m live`; die Live-Suite (tests/test_classify_live_run.py) fuehrt ihn nicht.
- `resources/templates/list` wird bedient (gemessen: ttlMs 300000, cacheScope public), hat aber keinen Test — grep "templates" ueber tests/ -> 0 Treffer. Vier der fuenf CacheableResult-Methoden sind gegatet, diese nicht.
- Nicht erhoben: ob 300000 ms zur Aenderungsfrequenz der Quelle passt. Die Frage stellt sich hier fuer Verzeichnisse, die beim Import feststehen, kaum; fuer Datenresultate setzt der Server gar kein ttlMs (gemessen: tools/call traegt weder ttlMs noch cacheScope), das Kriterium zur `source_freshness`-Ableitung ist damit gegenstandslos.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-020.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-021

## Finding: ARCH-021 — Extensions deklariert und versioniert — Tasks sind kein Kern-Feature mehr

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-021
**Katalog-Referenz:** SEP-2663
**Spec-Baseline:** 2026-07-28
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Keine Extension im Code: grep -rnE "io\.modelcontextprotocol/|extensions" ueber src/ trifft genau zwei Kommentarzeilen — src/eth_library_mcp/__init__.py:55 und src/eth_library_mcp/server.py:148 —, und beide nennen `_meta.io.modelcontextprotocol/serverInfo`, also einen Meta-Schluessel der Kernspec, keine Extension-Deklaration. Negativkontrolle: dasselbe Muster gegen mcp_types/_types.py trifft (Zeilen 53, 59, 62).
- Keine Tasks in keiner Fassung: grep -rnE "tasks/(get|update|result|list)|TaskHandle|task_id" ueber src/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen mcp/server/extension.py:59 trifft. Laufzeit GEMESSEN: `tasks/list` durch build_http_app() -> -32601 "Method not found"; weder die alte noch die Extension-Fassung wird bedient.
- Deklaration deckt sich in BEIDE Richtungen mit dem Code, gemessen an server/discover: die ausgelieferten capabilities bestehen aus prompts, resources und tools — ein `extensions`-Feld fehlt, und es gibt nichts zu deklarieren. Weder «deklariert, nicht implementiert» noch «implementiert, nicht deklariert».
- Kein eigener Namensraum missbraucht: es gibt ueberhaupt keine eigene Erweiterung, also auch keine unter `io.modelcontextprotocol/*` (gedeckt vom ersten Punkt).

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-021.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Keine Extension im Code: grep -rnE "io\.modelcontextprotocol/|extensions" ueber src/ trifft genau zwei Kommentarzeilen — src/eth_library_mcp/__init__.py:55 und src/eth_library_mcp/server.py:148 —, und beide nennen `_meta.io.modelcontextprotocol/serverInfo`, also einen Meta-Schluessel der Kernspec, keine Extension-Deklaration. Negativkontrolle: dasselbe Muster gegen mcp_types/_types.py trifft (Zeilen 53, 59, 62).
- Keine Tasks in keiner Fassung: grep -rnE "tasks/(get|update|result|list)|TaskHandle|task_id" ueber src/ -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen mcp/server/extension.py:59 trifft. Laufzeit GEMESSEN: `tasks/list` durch build_http_app() -> -32601 "Method not found"; weder die alte noch die Extension-Fassung wird bedient.
- Deklaration deckt sich in BEIDE Richtungen mit dem Code, gemessen an server/discover: die ausgelieferten capabilities bestehen aus prompts, resources und tools — ein `extensions`-Feld fehlt, und es gibt nichts zu deklarieren. Weder «deklariert, nicht implementiert» noch «implementiert, nicht deklariert».
- Kein eigener Namensraum missbraucht: es gibt ueberhaupt keine eigene Erweiterung, also auch keine unter `io.modelcontextprotocol/*` (gedeckt vom ersten Punkt).

### Gaps

- Kriterium 1 unerfuellt: Weder README.md noch README.de.md noch CHANGELOG.md sagt in einem Satz, dass dieser Server keine Extension fuehrt. Normalisierte Suche (Zeilenumbrueche geglaettet) nach `extension|erweiterung|tasks` ueber alle drei Dateien -> 0 Treffer; Negativkontrolle gegen eine Probedatei mit «Dieser Server fuehrt keine Extensions.» trifft. Damit bleiben «keine» und «nicht dokumentiert» fuer einen Leser ununterscheidbar — genau die Failure-Zeile «README schweigt zu Extensions» des Checks.
- Behebung ist ein Satz je README, neben dem bestehenden Abschnitt «MCP Protocol Version» / «MCP-Protokollversion» (tests/test_protocol_version.py:62-65 nennt beide Anker). Ein Test, der ihn haelt, liesse sich nach demselben Muster wie test_beide_readmes_nennen_dieselben_beiden_revisionen schreiben.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-021.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### ARCH-022

## Finding: ARCH-022 — Die Versionsquelle importiert das Paket-Root nicht

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-022
**Katalog-Referenz:** Custom (Portfolio-Fundstücke i14y-mcp / bag-health-mcp, 2026-08-03)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Es gibt kein Blatt-Modul fuer die Version: `ls src/eth_library_mcp/_version.py` -> No such file or directory. Die Version wird im Paket-Root selbst ermittelt, src/eth_library_mcp/__init__.py:15 `__version__ = _distribution_version(_DISTRIBUTION)` (in try/except PackageNotFoundError, Fallback "0.0.0+source" :20).
- Zwei Submodule lesen aus dem Root zurueck: src/eth_library_mcp/client.py:21 `from . import __version__` und src/eth_library_mcp/server.py:37 `from eth_library_mcp import DESCRIPTION, HOMEPAGE_URL, __version__`. Negativkontrolle des Musters gegen /tmp/psub.py trifft.
- Der Zyklus existiert dennoch nicht, weil die Gegenrichtung fehlt: grep -nE "^from \.|^import \.|^from eth_library_mcp" ueber src/eth_library_mcp/__init__.py -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen /tmp/pinit.py mit `from .server import mcp` und `import .x` trifft beide Zeilen. Modus 2 verlangt Treffer in BEIDEN Aufrufen fuer einen Zyklus; hier trifft nur einer.
- Doppelmessung in je FRISCHEN Interpretern, beide Ergebnisse: KALT `python -c "import eth_library_mcp.client as m; print(m.__version__)"` -> 0.4.0, kalt_client_exit=0. KALT `python -c "import eth_library_mcp.server as m; print(m.__version__)"` -> 0.4.0, kalt_server_exit=0. WARM `python -c "import eth_library_mcp; import eth_library_mcp.client; print(eth_library_mcp.__version__)"` -> 0.4.0, warm_exit=0. Beide gelingen -> nach der Tabelle des Checks kein Befund aus dieser Messung; ein einzelner Lauf wurde nicht als Beleg gewertet.
- Der Pfad des deklarierten Konsolen-Skripts ist bestimmt und MITGEMESSEN: pyproject.toml `[project.scripts] eth-library-mcp = "eth_library_mcp.server:mcp.run"` importiert das Submodul, ist also der kalte Pfad — das ist die zweite KALT-Messung oben. Zusaetzlich faehrt der Dockerfile `python -m eth_library_mcp.server` (Dockerfile:35), derselbe kalte Einstieg.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-022.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Es gibt kein Blatt-Modul fuer die Version: `ls src/eth_library_mcp/_version.py` -> No such file or directory. Die Version wird im Paket-Root selbst ermittelt, src/eth_library_mcp/__init__.py:15 `__version__ = _distribution_version(_DISTRIBUTION)` (in try/except PackageNotFoundError, Fallback "0.0.0+source" :20).
- Zwei Submodule lesen aus dem Root zurueck: src/eth_library_mcp/client.py:21 `from . import __version__` und src/eth_library_mcp/server.py:37 `from eth_library_mcp import DESCRIPTION, HOMEPAGE_URL, __version__`. Negativkontrolle des Musters gegen /tmp/psub.py trifft.
- Der Zyklus existiert dennoch nicht, weil die Gegenrichtung fehlt: grep -nE "^from \.|^import \.|^from eth_library_mcp" ueber src/eth_library_mcp/__init__.py -> 0 Treffer (exit 1). Negativkontrolle: dasselbe Muster gegen /tmp/pinit.py mit `from .server import mcp` und `import .x` trifft beide Zeilen. Modus 2 verlangt Treffer in BEIDEN Aufrufen fuer einen Zyklus; hier trifft nur einer.
- Doppelmessung in je FRISCHEN Interpretern, beide Ergebnisse: KALT `python -c "import eth_library_mcp.client as m; print(m.__version__)"` -> 0.4.0, kalt_client_exit=0. KALT `python -c "import eth_library_mcp.server as m; print(m.__version__)"` -> 0.4.0, kalt_server_exit=0. WARM `python -c "import eth_library_mcp; import eth_library_mcp.client; print(eth_library_mcp.__version__)"` -> 0.4.0, warm_exit=0. Beide gelingen -> nach der Tabelle des Checks kein Befund aus dieser Messung; ein einzelner Lauf wurde nicht als Beleg gewertet.
- Der Pfad des deklarierten Konsolen-Skripts ist bestimmt und MITGEMESSEN: pyproject.toml `[project.scripts] eth-library-mcp = "eth_library_mcp.server:mcp.run"` importiert das Submodul, ist also der kalte Pfad — das ist die zweite KALT-Messung oben. Zusaetzlich faehrt der Dockerfile `python -m eth_library_mcp.server` (Dockerfile:35), derselbe kalte Einstieg.

### Gaps

- Kriterien 1-3 unerfuellt: kein eigenes Versionsmodul, zwei Submodule lesen `__version__` aus dem Paket-Root, und das Root ermittelt die Version selbst statt aus einem Blatt zu lesen. Der Check verlangt die Entfernung der Rueckrichtung, nicht nur ihre Unschaedlichkeit.
- Die Unschaedlichkeit haengt an einer Eigenschaft, die niemand haelt: sobald `__init__.py` ein Submodul importiert (z.B. `from .server import mcp`, ein ueblicher Komfort-Reexport), entsteht der Zyklus, und ab dann traegt die Zeilenreihenfolge in __init__.py die Korrektheit. Genau das Negativbeispiel des Checks.
- Kein Test haelt den kalten Pfad in einem EIGENEN Prozess fest: grep "subprocess" ueber tests/ trifft nur tests/test_session_start_hook.py (Session-Start-Hook), kein Import-Test. Innerhalb der laufenden Suite ist jeder Import warm, der Zyklus waere dort unsichtbar — Kriterium 8 unerfuellt.
- Behebung ist klein und benannt: `src/eth_library_mcp/_version.py` mit nur `importlib.metadata`, dann `from ._version import __version__` in __init__.py, client.py und server.py. DESCRIPTION/HOMEPAGE_URL (__init__.py:65) laufen sinnvoll mit ins selbe Blatt, weil server.py:37 sie in derselben Zeile aus dem Root holt.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-022.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### DRIFT-001

## Finding: DRIFT-001 — Endpoint- und Ressourcen-URLs an genau einer Stelle konstruiert

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** DRIFT-001
**Katalog-Referenz:** Custom (Portfolio-Fundstück meteoswiss-mcp#33, 2026-07-30)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/client.py:27-28 — DISCOVERY_BASE_URL und PERSONS_BASE_URL stehen als Modul-Konstanten; Gegenprobe: `grep -rnE 'https?://' src/` findet ausserhalb dieser beiden Zeilen KEIN weiteres api.library.ethz.ch-Literal in der Abrufkette (Muster greift: es lieferte 5 Nicht-pyc-Treffer, also ist die Null kein Muster-Fehlschlag)
- src/eth_library_mcp/client.py:70 — `url = f"{base_url}{path}"` ist die EINZIGE Stelle, an der eine vollstaendige Upstream-URL zusammengesetzt wird; alle fuenf Aufrufer gehen ueber `_http_get` (server.py:291, 379, 448, 544, 646), gemessen per `grep -rn '_http_get(' src/`
- Gemessen: keine Fehlermeldung nennt eine URL. Bei erzwungenem 503 lauten die Antworten woertlich "Fehler bei Typ-Suche 'Karten / Maps': HTTP-Fehler 503." — kein URL-Literal, das von der abgerufenen abweichen koennte (formatting.py:112-162)
- tests/test_tools.py:61,74,84,96,112,123,137,155,172 — respx registriert gegen die IMPORTIERTE Konstante `f"{DISCOVERY_BASE_URL}/resources"`, nicht gegen ein wiederholtes URL-Literal; ebenso tests/test_server.py:278 und :289
- BEFUND src/eth_library_mcp/server.py:715 — `**Basis-URL:** https://api.library.ethz.ch` steht als zweites, handgeschriebenes Literal in der Antwort von `eth_library_info`. Gemessen an einem echten tools/call durch build_http_app(): der Text geht so an das Modell. Er behauptet, wovon der Server abruft, stammt aber nicht aus DISCOVERY_BASE_URL — genau die nicht widerlegbare Kopie, vor der dieser Check warnt
- BEFUND src/eth_library_mcp/server.py:291,448,544,646 — das Pfadsegment `"/resources"` ist viermal als Literal wiederholt, dazu `f"/resources/{params.mmsid}"` (379). Es gibt keine benannte Konstruktionsfunktion (`_discovery_resources_path()` o.ae.) und damit keine Stelle, an der die Regeln stuenden

### Expected Behavior

Die Pass-Kriterien stehen in `checks/DRIFT-001.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/client.py:27-28 — DISCOVERY_BASE_URL und PERSONS_BASE_URL stehen als Modul-Konstanten; Gegenprobe: `grep -rnE 'https?://' src/` findet ausserhalb dieser beiden Zeilen KEIN weiteres api.library.ethz.ch-Literal in der Abrufkette (Muster greift: es lieferte 5 Nicht-pyc-Treffer, also ist die Null kein Muster-Fehlschlag)
- src/eth_library_mcp/client.py:70 — `url = f"{base_url}{path}"` ist die EINZIGE Stelle, an der eine vollstaendige Upstream-URL zusammengesetzt wird; alle fuenf Aufrufer gehen ueber `_http_get` (server.py:291, 379, 448, 544, 646), gemessen per `grep -rn '_http_get(' src/`
- Gemessen: keine Fehlermeldung nennt eine URL. Bei erzwungenem 503 lauten die Antworten woertlich "Fehler bei Typ-Suche 'Karten / Maps': HTTP-Fehler 503." — kein URL-Literal, das von der abgerufenen abweichen koennte (formatting.py:112-162)
- tests/test_tools.py:61,74,84,96,112,123,137,155,172 — respx registriert gegen die IMPORTIERTE Konstante `f"{DISCOVERY_BASE_URL}/resources"`, nicht gegen ein wiederholtes URL-Literal; ebenso tests/test_server.py:278 und :289
- BEFUND src/eth_library_mcp/server.py:715 — `**Basis-URL:** https://api.library.ethz.ch` steht als zweites, handgeschriebenes Literal in der Antwort von `eth_library_info`. Gemessen an einem echten tools/call durch build_http_app(): der Text geht so an das Modell. Er behauptet, wovon der Server abruft, stammt aber nicht aus DISCOVERY_BASE_URL — genau die nicht widerlegbare Kopie, vor der dieser Check warnt
- BEFUND src/eth_library_mcp/server.py:291,448,544,646 — das Pfadsegment `"/resources"` ist viermal als Literal wiederholt, dazu `f"/resources/{params.mmsid}"` (379). Es gibt keine benannte Konstruktionsfunktion (`_discovery_resources_path()` o.ae.) und damit keine Stelle, an der die Regeln stuenden

### Gaps

- Keine Konstruktionsfunktion je Ressourcentyp: das Pfadsegment `/resources` wird an fuenf Stellen zusammengesetzt, der Docstring von `_http_get` (client.py:60-63) nennt nur API-Key und Fehlerbehandlung, keine Pfadregeln
- server.py:715 schreibt den Upstream-Host ein zweites Mal aus; aendert sich DISCOVERY_BASE_URL, behauptet `eth_library_info` weiterhin die alte Basis
- Es gibt gar kein `data_source_url`-Provenance-Feld. Die `Quelle:`-Zeile (formatting.py:20) nennt das Entwicklerportal developer.library.ethz.ch, nicht die tatsaechlich abgerufene URL — Kriterium 2 des Checks ist damit weder erfuellt noch widerlegt, es ist unpruefbar
- Kein Test der Form `provenance.data_source_url == str(route.calls[0].request.url)`; die Kopplung Abruf/Provenance ist nirgends festgehalten

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/DRIFT-001.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### DRIFT-002

## Finding: DRIFT-002 — Fallback verengt, erweitert nie — lieber ein Fehler als ein anderer Datensatz

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** DRIFT-002
**Katalog-Referenz:** Custom (Portfolio-Fundstück meteoswiss-mcp#33, 2026-07-30)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/server.py:378 — BEFUND: `doc = data.get("docs", [{}])[0] if data.get("docs") else data`. Der else-Zweig nimmt den ANTWORT-UMSCHLAG selbst als Datensatz. Gemessen mit respx (200, Body `{"info": {"total": 0}, "warnung": "nichts gefunden"}`): `eth_get_resource` liefert `'# Kein Titel\n*Quelle: ETH-Bibliothek (Public Domain) · https://developer.library.ethz.ch*'` — kein Fehlermarker, Ueberschrift und Quellenzeile wie bei einem echten Treffer. Der Aufruf gelingt, die Antwort ist wohlgeformt, der Inhalt ist keiner
- src/eth_library_mcp/server.py:280-285, 442-444, 538-540, 640-644 — die vier Such-Werkzeuge eskalieren dagegen korrekt: `if not docs: return "Keine Ergebnisse fuer ..."` bzw. "Keine Treffer im Archiv ...". Gemessen: bei `{"docs": [], "info": {"total": 0}}` antwortet eth_search_resources mit "Keine Ergebnisse fuer 'any,contains,xyzq'." — kein substituierter Datensatz
- Keine Substitution ueber Granularitaet, Zeitbezug oder Entitaet im gesamten src/: `grep -rnE 'break$|next\(iter\(|\[0\]\s*$' src/` liefert ausser der Zeile 378 keinen Auswahl-Fallback; `_first()` (formatting.py:23-25) waehlt das erste Element EINES FELDES, nicht einen anderen Datensatz
- tests/test_tools.py:73-79 — `test_search_resources_no_hits` haelt den Nicht-Fund fuer die Suchwerkzeuge fest. Fuer `eth_get_resource` existiert kein entsprechender Test: `tests/test_tools.py:109-129` deckt nur Happy-Path und HTTP-404 ab, nicht den 200-ohne-docs-Zweig

### Expected Behavior

Die Pass-Kriterien stehen in `checks/DRIFT-002.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/server.py:378 — BEFUND: `doc = data.get("docs", [{}])[0] if data.get("docs") else data`. Der else-Zweig nimmt den ANTWORT-UMSCHLAG selbst als Datensatz. Gemessen mit respx (200, Body `{"info": {"total": 0}, "warnung": "nichts gefunden"}`): `eth_get_resource` liefert `'# Kein Titel\n*Quelle: ETH-Bibliothek (Public Domain) · https://developer.library.ethz.ch*'` — kein Fehlermarker, Ueberschrift und Quellenzeile wie bei einem echten Treffer. Der Aufruf gelingt, die Antwort ist wohlgeformt, der Inhalt ist keiner
- src/eth_library_mcp/server.py:280-285, 442-444, 538-540, 640-644 — die vier Such-Werkzeuge eskalieren dagegen korrekt: `if not docs: return "Keine Ergebnisse fuer ..."` bzw. "Keine Treffer im Archiv ...". Gemessen: bei `{"docs": [], "info": {"total": 0}}` antwortet eth_search_resources mit "Keine Ergebnisse fuer 'any,contains,xyzq'." — kein substituierter Datensatz
- Keine Substitution ueber Granularitaet, Zeitbezug oder Entitaet im gesamten src/: `grep -rnE 'break$|next\(iter\(|\[0\]\s*$' src/` liefert ausser der Zeile 378 keinen Auswahl-Fallback; `_first()` (formatting.py:23-25) waehlt das erste Element EINES FELDES, nicht einen anderen Datensatz
- tests/test_tools.py:73-79 — `test_search_resources_no_hits` haelt den Nicht-Fund fuer die Suchwerkzeuge fest. Fuer `eth_get_resource` existiert kein entsprechender Test: `tests/test_tools.py:109-129` deckt nur Happy-Path und HTTP-404 ab, nicht den 200-ohne-docs-Zweig

### Gaps

- server.py:378 eskaliert nicht, sondern substituiert: eine 200-Antwort ohne `docs` wird als Ressourcen-Detail gerendert. Wo kein semantisch gleichwertiger Kandidat existiert, gehoerte ein Fehler hin
- Die Abweichung ist in der Antwort nicht ausgewiesen — kein Feld, nicht einmal Prosa; der Konsument kann 'Kein Titel' nicht von 'nichts geliefert' unterscheiden
- Kein Test ueber den leeren Kandidatensatz von `eth_get_resource` (200 ohne `docs`)
- Keine Auswahlfunktion mit Docstring, der begruendet, was bewusst NICHT genommen wird — die Auswahl steht als Inline-Ausdruck in der Tool-Funktion

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/DRIFT-002.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### DRIFT-003

## Finding: DRIFT-003 — Kein Test-Assert wird vom Degradationspfad erfüllt

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** DRIFT-003
**Katalog-Referenz:** Custom (Portfolio-Fundstück meteoswiss-mcp#33/#35/#37, 2026-07-30)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- GEGENPROBE (Modus 2), gemessen: mit einer autouse-Fixture, die `eth_library_mcp.server._http_get` auf einen HTTPStatusError(503) setzt, laufen 4 von 11 Tests in tests/test_tools.py WEITER GRUEN. Zwei davon sind Erfolgspfad-Tests: `test_search_by_type_happy_path` (tests/test_tools.py:153-164) und `test_search_education_happy_path` (tests/test_tools.py:170-179). Ein Totalausfall des Upstreams macht sie nicht rot
- tests/test_tools.py:164 — `assert "Karte" in out`. Der Degradationspfad liefert woertlich "Fehler bei Typ-Suche 'Karten / Maps': HTTP-Fehler 503." — das Stichwort steht in der Fehlermeldung, weil server.py:574 den Typ-Label `RESOURCE_TYPES['maps'] = 'Karten / Maps'` in den Fehlerkontext schreibt
- tests/test_tools.py:179 — `assert "Volksschule" in out`. Der Degradationspfad liefert "Fehler bei Bildungssuche 'Volksschule Zuerich': HTTP-Fehler 503." (server.py:681 setzt `params.topic` in den Kontext). Derselbe Mechanismus wie `assert "KLO" in result or "Zuerich" in result` im Belegfall des Checks
- Kein einziger Test schliesst den Degradationspfad AUS, bevor er Inhalt prueft: `grep -rn 'assert.*not in' tests/` findet nur OBS-002-Leakage-Zusicherungen (test_tools.py:91 'sk-1234', :102 'stacktrace', :103 '<html>'), keine Zusicherung gegen einen Ausfallmarker
- Der Degradationspfad ist nicht maschinell erkennbar: `formatting.py:112-162` liefert einen reinen Markdown-String mit dem deutschen Praefix 'Fehler bei ...'. Gemessen an einem echten tools/call durch build_http_app(): `"isError": false, "resultType": "complete"` — der Ausfall ist auch auf Protokollebene nicht als solcher markiert. Es gibt kein Statusfeld und keinen dokumentierten eindeutigen Marker
- tests/test_tools.py:136-147 und :110-118 — `test_search_archive_happy_path` und `test_get_resource_happy_path` fallen in der Gegenprobe zwar, aber nur zufaellig: ihre zweite Zusicherung ('Archivstueck', 'Detail-Titel') kommt im Fehlertext nicht vor. Die erste Zusicherung von test_search_archive ('Hochschularchiv') steht sehr wohl in "Fehler bei Archivsuche 'Hochschularchiv ETH Zuerich'" — gemessen

### Expected Behavior

Die Pass-Kriterien stehen in `checks/DRIFT-003.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- GEGENPROBE (Modus 2), gemessen: mit einer autouse-Fixture, die `eth_library_mcp.server._http_get` auf einen HTTPStatusError(503) setzt, laufen 4 von 11 Tests in tests/test_tools.py WEITER GRUEN. Zwei davon sind Erfolgspfad-Tests: `test_search_by_type_happy_path` (tests/test_tools.py:153-164) und `test_search_education_happy_path` (tests/test_tools.py:170-179). Ein Totalausfall des Upstreams macht sie nicht rot
- tests/test_tools.py:164 — `assert "Karte" in out`. Der Degradationspfad liefert woertlich "Fehler bei Typ-Suche 'Karten / Maps': HTTP-Fehler 503." — das Stichwort steht in der Fehlermeldung, weil server.py:574 den Typ-Label `RESOURCE_TYPES['maps'] = 'Karten / Maps'` in den Fehlerkontext schreibt
- tests/test_tools.py:179 — `assert "Volksschule" in out`. Der Degradationspfad liefert "Fehler bei Bildungssuche 'Volksschule Zuerich': HTTP-Fehler 503." (server.py:681 setzt `params.topic` in den Kontext). Derselbe Mechanismus wie `assert "KLO" in result or "Zuerich" in result` im Belegfall des Checks
- Kein einziger Test schliesst den Degradationspfad AUS, bevor er Inhalt prueft: `grep -rn 'assert.*not in' tests/` findet nur OBS-002-Leakage-Zusicherungen (test_tools.py:91 'sk-1234', :102 'stacktrace', :103 '<html>'), keine Zusicherung gegen einen Ausfallmarker
- Der Degradationspfad ist nicht maschinell erkennbar: `formatting.py:112-162` liefert einen reinen Markdown-String mit dem deutschen Praefix 'Fehler bei ...'. Gemessen an einem echten tools/call durch build_http_app(): `"isError": false, "resultType": "complete"` — der Ausfall ist auch auf Protokollebene nicht als solcher markiert. Es gibt kein Statusfeld und keinen dokumentierten eindeutigen Marker
- tests/test_tools.py:136-147 und :110-118 — `test_search_archive_happy_path` und `test_get_resource_happy_path` fallen in der Gegenprobe zwar, aber nur zufaellig: ihre zweite Zusicherung ('Archivstueck', 'Detail-Titel') kommt im Fehlertext nicht vor. Die erste Zusicherung von test_search_archive ('Hochschularchiv') steht sehr wohl in "Fehler bei Archivsuche 'Hochschularchiv ETH Zuerich'" — gemessen

### Gaps

- Zwei von fuenf Erfolgspfad-Tests der Werkzeugschicht bestehen einen Totalausfall des Upstreams (gemessen, nicht geschlossen)
- Kein strukturiertes Statusfeld und kein dokumentierter Ausfallmarker; jede Testverschaerfung haengt am deutschen Textliteral 'Fehler bei'
- Keine Gegenprobe im Repo: es existiert kein Test, der den Upstream bricht und zeigt, dass die Erfolgstests dann rot werden
- Modus 3 ohne Befund und mit Gegenkontrolle: `grep -rn 'match=|assertRaisesRegex' tests/ scripts/` liefert 0 Treffer; dieselbe Suche gegen eine Probedatei mit `pytest.raises(E, match="summary.json not found")` liefert 1 — das Muster greift, es gibt hier schlicht keine Regex-Assertion

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/DRIFT-003.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### DRIFT-004

## Finding: DRIFT-004 — Endpoint-Konstanten live verifiziert — ein Mock pinnt die eigene Annahme

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** DRIFT-004
**Katalog-Referenz:** Custom (Portfolio-Fundstück meteoswiss-mcp#35, 2026-07-30)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Endpoint-Konstanten vollstaendig inventarisiert: `grep -rnE '^[A-Z_]+(_BASE|_URL|_ENDPOINT|_API)\s*=\s*"https?://' src/` liefert genau zwei — src/eth_library_mcp/client.py:27 DISCOVERY_BASE_URL und :28 PERSONS_BASE_URL. Kein weiterer Host in der Abrufkette (die uebrigen https-Literale in src/ sind Doku-Links auf developer.library.ethz.ch bzw. GitHub)
- Beide Konstanten sind live abgedeckt und werden IMPORTIERT, nicht kopiert: tests/test_server.py:276-278 (`from eth_library_mcp.client import DISCOVERY_BASE_URL` … `httpx.get(f"{DISCOVERY_BASE_URL}/resources")`) und :287-289 (PERSONS_BASE_URL). Gemessen: `pytest -m live --collect-only` sammelt genau diese zwei ein (tests/test_server.py::TestLiveGatewayRoutes)
- Mocks registrieren gegen die importierte Konstante, nicht gegen ein wiederholtes Literal — tests/test_tools.py:18 importiert DISCOVERY_BASE_URL, alle neun respx-Registrierungen bauen `f"{DISCOVERY_BASE_URL}/..."`. Kein URL-Literal in tests/: `grep -rn 'api.library.ethz.ch' tests/*.py` liefert 0 Treffer, waehrend dasselbe Muster in src/ 3 Treffer hat — das Muster greift also
- BEFUND tests/test_server.py:279 — `assert r.status_code == route_status('discovery_resources')`, also == 401 exakt. Ein transientes 5xx macht den Test rot mit der Begruendung 'fuenf Werkzeuge haengen daran'. tests/test_server.py:290 spiegelbildlich: `assert r.status_code == 404` — ein 503 der Persons-Route liest sich dort als 'die Route ist zurueck'. Die vom Check verlangte Unterscheidung 404 (weg) / 5xx (transient) findet nicht statt
- scripts/classify_live_run.py ordnet clear/finding/unknown ausschliesslich am JUnit-XML ein (Tests, Skips, Failures, Errors) und kann einen Statuscode nicht sehen — die fehlende Unterscheidung wird also auch nicht nachgelagert nachgeholt

### Expected Behavior

Die Pass-Kriterien stehen in `checks/DRIFT-004.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Endpoint-Konstanten vollstaendig inventarisiert: `grep -rnE '^[A-Z_]+(_BASE|_URL|_ENDPOINT|_API)\s*=\s*"https?://' src/` liefert genau zwei — src/eth_library_mcp/client.py:27 DISCOVERY_BASE_URL und :28 PERSONS_BASE_URL. Kein weiterer Host in der Abrufkette (die uebrigen https-Literale in src/ sind Doku-Links auf developer.library.ethz.ch bzw. GitHub)
- Beide Konstanten sind live abgedeckt und werden IMPORTIERT, nicht kopiert: tests/test_server.py:276-278 (`from eth_library_mcp.client import DISCOVERY_BASE_URL` … `httpx.get(f"{DISCOVERY_BASE_URL}/resources")`) und :287-289 (PERSONS_BASE_URL). Gemessen: `pytest -m live --collect-only` sammelt genau diese zwei ein (tests/test_server.py::TestLiveGatewayRoutes)
- Mocks registrieren gegen die importierte Konstante, nicht gegen ein wiederholtes Literal — tests/test_tools.py:18 importiert DISCOVERY_BASE_URL, alle neun respx-Registrierungen bauen `f"{DISCOVERY_BASE_URL}/..."`. Kein URL-Literal in tests/: `grep -rn 'api.library.ethz.ch' tests/*.py` liefert 0 Treffer, waehrend dasselbe Muster in src/ 3 Treffer hat — das Muster greift also
- BEFUND tests/test_server.py:279 — `assert r.status_code == route_status('discovery_resources')`, also == 401 exakt. Ein transientes 5xx macht den Test rot mit der Begruendung 'fuenf Werkzeuge haengen daran'. tests/test_server.py:290 spiegelbildlich: `assert r.status_code == 404` — ein 503 der Persons-Route liest sich dort als 'die Route ist zurueck'. Die vom Check verlangte Unterscheidung 404 (weg) / 5xx (transient) findet nicht statt
- scripts/classify_live_run.py ordnet clear/finding/unknown ausschliesslich am JUnit-XML ein (Tests, Skips, Failures, Errors) und kann einen Statuscode nicht sehen — die fehlende Unterscheidung wird also auch nicht nachgelagert nachgeholt

### Gaps

- Die beiden Live-Tests unterscheiden 404 nicht von 5xx: beide vergleichen auf Gleichheit mit einem festen Code. Ein Ausfall der Quelle erzeugt denselben Befund wie ein abgeschalteter Endpoint — und bei test_persons_route_is_still_gone sogar einen inhaltlich falschen ('die Route ist zurueck')
- Der Live-Test prueft nur den Statuscode der Route, nicht einen minimal gueltigen Aufruf; eine Umbenennung eines Pfadsegments unterhalb von /resources faenge er nicht
- Kein Probe-Manifest ausserhalb der Testsuite (kein scripts/live_probe.manifest.json); die Abdeckung haengt vollstaendig am geplanten Lauf dieses Repos

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/DRIFT-004.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### DRIFT-006

## Finding: DRIFT-006 — Der CHANGELOG darf dem Code nicht widersprechen

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** DRIFT-006
**Katalog-Referenz:** Custom (Portfolio-Fundstück swiss-energy-mcp, 2026-08-01)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- BEFUND src/eth_library_mcp/server.py:179 — die `instructions` des Servers fuehren «Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung.» GEMESSEN an einem echten `initialize` durch build_http_app(): der Satz steht so im Handshake-Resultat. Gleichzeitig gemessen: `hasattr(eth_library_mcp.server, 'eth_search_persons')` ist False, und tests/test_server.py:254-259 verbietet das Werkzeug ausdruecklich («Eine Faehigkeit, die es nicht gibt, darf nicht angeboten werden»). Der Server bewirbt im Handshake genau die Faehigkeit, die sein eigener Test verbietet
- BEFUND src/eth_library_mcp/server.py:713 — `**Version:** 0.3.0` im Rueckgabetext von `eth_library_info`. GEMESSEN an einem tools/call durch build_http_app(): DIESELBE Antwort traegt in `_meta['io.modelcontextprotocol/serverInfo']['version']` den Wert `0.4.0`. Zwei Versionsangaben, eine Antwort, ein Widerspruch. scripts/check_version_sync.py faengt ihn nicht — CI ist gruen
- BEFUND src/eth_library_mcp/server.py:21 — der Modul-Docstring beschreibt «formatting.py — Markdown-Rendering, Persons-Parsing, Error-Mapping». Der HEAD-Commit 32ac730 heisst «refactor: toten Persons-Parser entfernen»; `grep -in person src/eth_library_mcp/formatting.py` liefert 0 Treffer (Gegenkontrolle: dasselbe Muster liefert in server.py 4 Treffer). Die Modulgrenze beschreibt eine Funktion, die es nicht mehr gibt
- BEFUND src/eth_library_mcp/server.py:580 — die Abschnittsueberschrift «TOOL 5: Personen suchen» steht ueber `SearchEducationInput` / `eth_search_education`; die naechste Ueberschrift ist «TOOL 7» (server.py:688). Die Nummerierung und der Titel beschreiben den entfernten Stand
- BEFUND tests/test_tools.py:8-9 — «Run with `pytest -m live` for the (currently absent) live suite.» GEMESSEN: `pytest -m live --collect-only` sammelt zwei Tests ein (tests/test_server.py::TestLiveGatewayRoutes), und README.md:331 datiert ihre Einfuehrung auf 2026-08-08. Zusaetzlich tests/test_tools.py:5 — «against a stubbed Discovery / Persons API response»; Persons-Tests gibt es in der Datei keine
- BEFUND docs/ARCHITECTURE.md:14 und :67, README.md:243, README.de.md:244 — «FastMCP tools, resources, prompts», «FastMCP's structured-output path», «FastMCP-Server, alle Tools». Der Server laeuft auf `mcp.server.mcpserver.MCPServer` (server.py:34); FastMCP ist in mcp 2.0.0 entfallen und `grep -rn 'FastMCP' src/ tests/` liefert 0 Treffer
- BEFUND README.md:53 / README.de.md:53 «Dual transport – stdio for Claude Desktop, Streamable HTTP/SSE for cloud deployment» und README.md:133 / README.de.md:133 «Cloud Deployment (SSE for browser access)». GEMESSEN: `build_http_app().routes` enthaelt genau eine Route, `/mcp`; GET und POST auf `/sse` antworten mit HTTP 404. Eine dokumentierte Faehigkeit, die der Code nicht hat
- Modus 1 gefuehrt, nicht nur gegrept: `[Unreleased]` in CHANGELOG.md ist leer (sed-Auszug zwischen `## [Unreleased]` und `## [0.4.0]` enthaelt keine Zeile) — von dort kommt kein Widerspruch. Modus 2 als Vorsortierung: das Absichtsvokabular findet zwei Stellen, docs/secret-management.md:43 («planned for a future sprint», trifft zu — keine gitleaks-Stufe in ci.yml) und tests/test_tools.py:9 (widerlegt, siehe oben). Gegenkontrolle: dasselbe Muster gegen eine Probedatei mit «noch nicht implementiert» liefert 1 Treffer

### Expected Behavior

Die Pass-Kriterien stehen in `checks/DRIFT-006.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- BEFUND src/eth_library_mcp/server.py:179 — die `instructions` des Servers fuehren «Ebenfalls verfuegbar: Personen-Suche mit Wikidata-Verlinkung.» GEMESSEN an einem echten `initialize` durch build_http_app(): der Satz steht so im Handshake-Resultat. Gleichzeitig gemessen: `hasattr(eth_library_mcp.server, 'eth_search_persons')` ist False, und tests/test_server.py:254-259 verbietet das Werkzeug ausdruecklich («Eine Faehigkeit, die es nicht gibt, darf nicht angeboten werden»). Der Server bewirbt im Handshake genau die Faehigkeit, die sein eigener Test verbietet
- BEFUND src/eth_library_mcp/server.py:713 — `**Version:** 0.3.0` im Rueckgabetext von `eth_library_info`. GEMESSEN an einem tools/call durch build_http_app(): DIESELBE Antwort traegt in `_meta['io.modelcontextprotocol/serverInfo']['version']` den Wert `0.4.0`. Zwei Versionsangaben, eine Antwort, ein Widerspruch. scripts/check_version_sync.py faengt ihn nicht — CI ist gruen
- BEFUND src/eth_library_mcp/server.py:21 — der Modul-Docstring beschreibt «formatting.py — Markdown-Rendering, Persons-Parsing, Error-Mapping». Der HEAD-Commit 32ac730 heisst «refactor: toten Persons-Parser entfernen»; `grep -in person src/eth_library_mcp/formatting.py` liefert 0 Treffer (Gegenkontrolle: dasselbe Muster liefert in server.py 4 Treffer). Die Modulgrenze beschreibt eine Funktion, die es nicht mehr gibt
- BEFUND src/eth_library_mcp/server.py:580 — die Abschnittsueberschrift «TOOL 5: Personen suchen» steht ueber `SearchEducationInput` / `eth_search_education`; die naechste Ueberschrift ist «TOOL 7» (server.py:688). Die Nummerierung und der Titel beschreiben den entfernten Stand
- BEFUND tests/test_tools.py:8-9 — «Run with `pytest -m live` for the (currently absent) live suite.» GEMESSEN: `pytest -m live --collect-only` sammelt zwei Tests ein (tests/test_server.py::TestLiveGatewayRoutes), und README.md:331 datiert ihre Einfuehrung auf 2026-08-08. Zusaetzlich tests/test_tools.py:5 — «against a stubbed Discovery / Persons API response»; Persons-Tests gibt es in der Datei keine
- BEFUND docs/ARCHITECTURE.md:14 und :67, README.md:243, README.de.md:244 — «FastMCP tools, resources, prompts», «FastMCP's structured-output path», «FastMCP-Server, alle Tools». Der Server laeuft auf `mcp.server.mcpserver.MCPServer` (server.py:34); FastMCP ist in mcp 2.0.0 entfallen und `grep -rn 'FastMCP' src/ tests/` liefert 0 Treffer
- BEFUND README.md:53 / README.de.md:53 «Dual transport – stdio for Claude Desktop, Streamable HTTP/SSE for cloud deployment» und README.md:133 / README.de.md:133 «Cloud Deployment (SSE for browser access)». GEMESSEN: `build_http_app().routes` enthaelt genau eine Route, `/mcp`; GET und POST auf `/sse` antworten mit HTTP 404. Eine dokumentierte Faehigkeit, die der Code nicht hat
- Modus 1 gefuehrt, nicht nur gegrept: `[Unreleased]` in CHANGELOG.md ist leer (sed-Auszug zwischen `## [Unreleased]` und `## [0.4.0]` enthaelt keine Zeile) — von dort kommt kein Widerspruch. Modus 2 als Vorsortierung: das Absichtsvokabular findet zwei Stellen, docs/secret-management.md:43 («planned for a future sprint», trifft zu — keine gitleaks-Stufe in ci.yml) und tests/test_tools.py:9 (widerlegt, siehe oben). Gegenkontrolle: dasselbe Muster gegen eine Probedatei mit «noch nicht implementiert» liefert 1 Treffer

### Gaps

- Der Server bewirbt im `initialize`-Handshake eine entfernte Faehigkeit (Personen-Suche). Das ist der teuerste der Befunde: er erreicht jedes Modell bei jeder Verbindung und widerspricht einem Test desselben Repos
- `eth_library_info` meldet Version 0.3.0, waehrend dieselbe Antwort 0.4.0 stempelt; scripts/check_version_sync.py sieht Literale in server.py nicht an
- Vier Doku-Stellen fuehren FastMCP, obwohl die SDK-2.x-Migration abgeschlossen ist — der PR, der die Absicht ausgefuehrt hat, hat die Saetze nicht im selben Diff korrigiert
- README fuehrt SSE als ausgelieferten Transport; gemessen existiert kein SSE-Pfad (siehe SCALE-009)
- Kein Release-Schritt, der `[Unreleased]` liest statt verschiebt — heute folgenlos, weil der Abschnitt leer ist

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/DRIFT-006.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### DRIFT-008

## Finding: DRIFT-008 — Ein Live-Test muss die Quelle erreichen — «markiert» ist nicht «live»

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** DRIFT-008
**Katalog-Referenz:** Custom (Portfolio-Fundstück zh-education-mcp, 2026-08-08)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Vollstaendige Erhebung der autouse-Fixtures: `grep -rn 'autouse' tests/` liefert genau EINE — tests/test_transport_security.py:45 `_saubere_umgebung`, die `ETH_LIBRARY_CORS_ORIGINS` und `ETH_LIBRARY_ALLOWED_HOSTS` per `monkeypatch.delenv` aus der Umgebung nimmt (:52-53). Gegenkontrolle: dasselbe Muster findet im selben Lauf die Fixture, ist also nicht leer gelaufen
- Ihr Geltungsbereich enthaelt nachweislich keinen Live-Test: GEMESSEN `pytest tests/test_transport_security.py -m live --collect-only` -> «no tests collected (10 deselected)». Die Fixture ist in einem Testmodul definiert und wirkt nur dort; es gibt kein conftest.py im Repo (`find . -name conftest.py` liefert 0 Treffer)
- GEMESSEN wo die Live-Tests liegen: `pytest -m live --collect-only` sammelt genau zwei ein, beide in tests/test_server.py::TestLiveGatewayRoutes (test_discovery_route_still_exists, test_persons_route_is_still_gone). tests/test_server.py enthaelt keine Fixture — `grep -n 'fixture' tests/test_server.py` liefert 0 Treffer
- Keine Ersetzung von Namensaufloesung oder Transport irgendwo in tests/: `grep -rn 'getaddrinfo|create_connection|freeze_time|AsyncHTTPTransport' tests/` liefert 0 Treffer in .py-Dateien; `respx` erscheint ausschliesslich als Dekorator `@respx.mock` an einzelnen Nicht-Live-Tests (tests/test_tools.py), nie als autouse
- BEFUND: es gibt keinen Waechter. `grep -rn 'request.keywords' tests/` liefert 0 Treffer, es existiert weder ein `pytest_runtest_call`-Hook noch eine Datei, die den echten `socket.getaddrinfo` vor jeder Fixture festhaelt

### Expected Behavior

Die Pass-Kriterien stehen in `checks/DRIFT-008.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Vollstaendige Erhebung der autouse-Fixtures: `grep -rn 'autouse' tests/` liefert genau EINE — tests/test_transport_security.py:45 `_saubere_umgebung`, die `ETH_LIBRARY_CORS_ORIGINS` und `ETH_LIBRARY_ALLOWED_HOSTS` per `monkeypatch.delenv` aus der Umgebung nimmt (:52-53). Gegenkontrolle: dasselbe Muster findet im selben Lauf die Fixture, ist also nicht leer gelaufen
- Ihr Geltungsbereich enthaelt nachweislich keinen Live-Test: GEMESSEN `pytest tests/test_transport_security.py -m live --collect-only` -> «no tests collected (10 deselected)». Die Fixture ist in einem Testmodul definiert und wirkt nur dort; es gibt kein conftest.py im Repo (`find . -name conftest.py` liefert 0 Treffer)
- GEMESSEN wo die Live-Tests liegen: `pytest -m live --collect-only` sammelt genau zwei ein, beide in tests/test_server.py::TestLiveGatewayRoutes (test_discovery_route_still_exists, test_persons_route_is_still_gone). tests/test_server.py enthaelt keine Fixture — `grep -n 'fixture' tests/test_server.py` liefert 0 Treffer
- Keine Ersetzung von Namensaufloesung oder Transport irgendwo in tests/: `grep -rn 'getaddrinfo|create_connection|freeze_time|AsyncHTTPTransport' tests/` liefert 0 Treffer in .py-Dateien; `respx` erscheint ausschliesslich als Dekorator `@respx.mock` an einzelnen Nicht-Live-Tests (tests/test_tools.py), nie als autouse
- BEFUND: es gibt keinen Waechter. `grep -rn 'request.keywords' tests/` liefert 0 Treffer, es existiert weder ein `pytest_runtest_call`-Hook noch eine Datei, die den echten `socket.getaddrinfo` vor jeder Fixture festhaelt

### Gaps

- Kein suiteweiter Waechter, der einen Live-Test abbricht, dessen Aussenwelt ersetzt wurde — ohne conftest.py gibt es gar keinen Ort dafuer. Der heutige Zustand ist sauber, aber nur durch Zufall der Dateiaufteilung: die erste autouse-Fixture in tests/test_server.py laeuft in dieselbe Falle
- Die einzige autouse-Fixture (test_transport_security.py:45) nimmt Live-Tests nicht aus (`if 'live' in request.keywords: return` fehlt) — heute folgenlos, weil in ihrer Datei kein Live-Test steht, aber vorsorglich verlangt der Check die Zeile auch dort
- Keine Gegenprobe in beide Richtungen: es existiert kein synthetischer Live-Test mit stubbender Fixture, der fallen muesste, und keiner, der gruen bleiben muss
- Der echte Referenzwert (`_REAL_GETADDRINFO`) wird nirgends beim Import festgehalten

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/DRIFT-008.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### FID-001

## Finding: FID-001 — Scope-Defaults: Filter-Parameter explizit senden, nie erben

**Severity:** critical
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** FID-001
**Katalog-Referenz:** Custom (Portfolio-Fundstück termdat-mcp#11)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- src/eth_library_mcp/server.py:274 — `if params.sort:` sendet `sort` nur, wenn der Aufrufer es setzt; `sort: SortOption | None = Field(default="rank")` erlaubt ausdruecklich `None`, dann erbt die Suche die Sortier-Vorgabe des Gateways. Genau das Fail-Pattern `if x: params[...] = x` aus der Check-Definition.
- grep ueber README.md README.de.md CHANGELOG.md EXAMPLES.md docs/ tests/ nach `default-matrix|ground.?truth|recall|referenzquer|reality.?check|known limitation|bekannte einschr|web-ui`: Exit 1, kein Treffer. NEGATIVKONTROLLE: dasselbe Muster gegen /tmp/p1.md mit den Zeilen 'Known Limitations' und 'Ground Truth: 12 vs 7' liefert 2 Treffer — das Muster greift, die Default-Matrix existiert nicht.
- docs/data-sources.md:1-12 — fuehrt die Discovery-API mit Endpoint und Lizenz, nennt aber keinen einzigen optionalen Parameter und keine Spec-URL. Im ganzen Repo liegt keine OpenAPI-/Parameter-Spezifikation, gegen die die Defaults der Quelle gelesen werden koennten.
- src/eth_library_mcp/server.py:293-294, 450-451, 546-547, 648-649 — die vier Such-Werkzeuge senden `limit`/`offset`/`lang` zwar immer explizit, aber es gibt zu keinem Parameter einen Beleg, was sein Weglassen upstream bedeuten wuerde; `qInclude` (facet_rtype/facet_lang/facet_tlevel/facet_data_source) wird nur bei gesetzten Filtern gebaut, ohne Spec-Beleg, dass Weglassen 'unbeschraenkt' heisst.
- tests/fixtures/PROVENANCE.md:35-40 — 'discovery_*.json … NICHT aufgezeichnet', weil ohne API-Key nur HTTP 401 kommt. Es existiert damit keine aufgezeichnete Discovery-Antwort, gegen die ein Recall-Delta je gemessen worden waere.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/FID-001.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/server.py:274 — `if params.sort:` sendet `sort` nur, wenn der Aufrufer es setzt; `sort: SortOption | None = Field(default="rank")` erlaubt ausdruecklich `None`, dann erbt die Suche die Sortier-Vorgabe des Gateways. Genau das Fail-Pattern `if x: params[...] = x` aus der Check-Definition.
- grep ueber README.md README.de.md CHANGELOG.md EXAMPLES.md docs/ tests/ nach `default-matrix|ground.?truth|recall|referenzquer|reality.?check|known limitation|bekannte einschr|web-ui`: Exit 1, kein Treffer. NEGATIVKONTROLLE: dasselbe Muster gegen /tmp/p1.md mit den Zeilen 'Known Limitations' und 'Ground Truth: 12 vs 7' liefert 2 Treffer — das Muster greift, die Default-Matrix existiert nicht.
- docs/data-sources.md:1-12 — fuehrt die Discovery-API mit Endpoint und Lizenz, nennt aber keinen einzigen optionalen Parameter und keine Spec-URL. Im ganzen Repo liegt keine OpenAPI-/Parameter-Spezifikation, gegen die die Defaults der Quelle gelesen werden koennten.
- src/eth_library_mcp/server.py:293-294, 450-451, 546-547, 648-649 — die vier Such-Werkzeuge senden `limit`/`offset`/`lang` zwar immer explizit, aber es gibt zu keinem Parameter einen Beleg, was sein Weglassen upstream bedeuten wuerde; `qInclude` (facet_rtype/facet_lang/facet_tlevel/facet_data_source) wird nur bei gesetzten Filtern gebaut, ohne Spec-Beleg, dass Weglassen 'unbeschraenkt' heisst.
- tests/fixtures/PROVENANCE.md:35-40 — 'discovery_*.json … NICHT aufgezeichnet', weil ohne API-Key nur HTTP 401 kommt. Es existiert damit keine aufgezeichnete Discovery-Antwort, gegen die ein Recall-Delta je gemessen worden waere.

### Gaps

- Keine Default-Matrix: kein Dokument listet die optionalen Parameter der genutzten Discovery-Endpoints mit der Bedeutung ihres Weglassens.
- Kein empirisch gemessenes Recall-Delta (weggelassen vs. explizit maximal) fuer irgendeinen Parameter — weder dokumentiert noch als Test.
- `sort=None` faellt still auf die Gateway-Vorgabe zurueck; die Einschraenkung erscheint in keinem Tool-Result.
- Die empirische Haelfte des Checks war in diesem Lauf nicht messbar: Netzzugriffe auf die ETH-API waren ausgeschlossen und die API verlangt einen Schluessel, den das Repo nicht fuehrt. Der Befund stuetzt sich deshalb auf die nachgewiesene Abwesenheit der geforderten Artefakte, nicht auf ein gemessenes Delta.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `critical`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/FID-001.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### FID-002

## Finding: FID-002 — Recall-Ground-Truth: Referenzqueries gegen die offizielle Oberfläche

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** FID-002
**Katalog-Referenz:** Custom (Portfolio-Fundstück termdat-mcp#11)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- grep ueber README.md README.de.md CHANGELOG.md EXAMPLES.md docs/ tests/ nach `ground.?truth|recall|referenzquer|reality.?check|known limitation|web-ui|weboberfl`: Exit 1, kein Treffer. NEGATIVKONTROLLE: dasselbe Muster findet in /tmp/p1.md ('Known Limitations', 'Ground Truth: 12 vs 7') 2 Zeilen — das Muster greift.
- tests/test_server.py:262-293 — die EINZIGEN beiden `@pytest.mark.live`-Tests sind `test_discovery_route_still_exists` und `test_persons_route_is_still_gone`. Beide messen einen Statuscode (401 = Route da, 404 = Route weg), keiner stellt eine Query und keiner prueft eine Trefferzahl. Ein Recall-Floor-Test existiert nicht.
- `PYTHONPATH=src pytest tests/ -m "not live" -q` -> 128 passed, 2 deselected. Die 2 deselektierten sind genau die beiden Routen-Tests oben; es gibt keine weiteren Live-Tests, in denen ein Recall-Vergleich stecken koennte.
- tests/fixtures/PROVENANCE.md:14-40 — aufgezeichnet ist ausschliesslich `api_routes.json` (Statuscode je Pfad, Stand 2026-08-08). Discovery-Antwortkoerper sind ausdruecklich nicht aufgezeichnet. Es gibt also keine Ersatz-Ground-Truth (Bulk-Dump, veroeffentlichte Bestandszahlen) im Repo.
- README.md/README.de.md fuehren keinen Abschnitt 'Known Limitations' und keine Referenzquery-Tabelle; EXAMPLES.md zeigt Beispielaufrufe ohne Trefferzahlen beider Oberflaechen.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/FID-002.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- grep ueber README.md README.de.md CHANGELOG.md EXAMPLES.md docs/ tests/ nach `ground.?truth|recall|referenzquer|reality.?check|known limitation|web-ui|weboberfl`: Exit 1, kein Treffer. NEGATIVKONTROLLE: dasselbe Muster findet in /tmp/p1.md ('Known Limitations', 'Ground Truth: 12 vs 7') 2 Zeilen — das Muster greift.
- tests/test_server.py:262-293 — die EINZIGEN beiden `@pytest.mark.live`-Tests sind `test_discovery_route_still_exists` und `test_persons_route_is_still_gone`. Beide messen einen Statuscode (401 = Route da, 404 = Route weg), keiner stellt eine Query und keiner prueft eine Trefferzahl. Ein Recall-Floor-Test existiert nicht.
- `PYTHONPATH=src pytest tests/ -m "not live" -q` -> 128 passed, 2 deselected. Die 2 deselektierten sind genau die beiden Routen-Tests oben; es gibt keine weiteren Live-Tests, in denen ein Recall-Vergleich stecken koennte.
- tests/fixtures/PROVENANCE.md:14-40 — aufgezeichnet ist ausschliesslich `api_routes.json` (Statuscode je Pfad, Stand 2026-08-08). Discovery-Antwortkoerper sind ausdruecklich nicht aufgezeichnet. Es gibt also keine Ersatz-Ground-Truth (Bulk-Dump, veroeffentlichte Bestandszahlen) im Repo.
- README.md/README.de.md fuehren keinen Abschnitt 'Known Limitations' und keine Referenzquery-Tabelle; EXAMPLES.md zeigt Beispielaufrufe ohne Trefferzahlen beider Oberflaechen.

### Gaps

- Kein Set von 3-5 Referenzqueries definiert.
- Keine Trefferzahlen der offiziellen Oberflaeche (ETH-Bibliothek Recherchportal) je gegen die Werkzeuge gehalten und dokumentiert.
- Kein Recall-Regressionstest mit Untergrenzen unter `@pytest.mark.live` — der Scope-Kollaps, den FID-001 ermoeglicht, hat kein Fruehwarnsystem.
- Der Reality-Check deckt nur Listen-/Routen-Ebene ab (existiert die Route), nie die Query-Ebene (liefert sie, was die Quelle hat) — genau die Reichweitenluecke, die der Check beschreibt.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/FID-002.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### FID-003

## Finding: FID-003 — Leermenge von Abwesenheit unterscheidbar — keine Konfabulations-Einladung

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** FID-003
**Katalog-Referenz:** Custom (Portfolio-Fundstück termdat-mcp#11)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- GEMESSEN ueber den echten ASGI-Stack (`build_http_app()`, tools/call auf `eth_search_resources`, `_http_get` auf `httpx.ConnectError` gesetzt): das Result traegt `isError: False` und `content[0].text = "Fehler bei Suche nach 'any,contains,Test': Verbindungsfehler. Internetverbindung pruefen."`. POSITIVKONTROLLE im selben Aufrufweg: ein Validierungsfehler (`query=""`) liefert `isError: True` — der Fehlerkanal existiert und funktioniert, der Server benutzt ihn fuer Upstream-Ausfaelle nie.
- src/eth_library_mcp/server.py:326-329, 474-477, 570-573, 676-679 — jedes Werkzeug endet in `except Exception as e: return _handle_error(...)` und gibt einen `str` zurueck. Transport-, Timeout- und Autorisierungsfehler (401, 403, 429, 5xx) erreichen den Aufrufer damit als gewoehnliches, erfolgreiches Tool-Result.
- src/eth_library_mcp/formatting.py:141-143 — der 404-Zweig der Suche lautet woertlich 'Keine Ergebnisse oder Endpunkt nicht gefunden (HTTP 404)'. Gemessen: ein 404 erzeugt genau diesen Text. Das ist die Vermischung, gegen die der Check steht — und BUG-02 war in diesem Repo exakt der Fall 'Route weg, HTTP 404', der hier als moegliche Leermenge angeboten wird.
- GEMESSEN: eine Antwort, deren Felder eine Ebene tiefer liegen (`{"results": {"docs": [...], "info": {...}}}`), erzeugt ZEICHENGLEICH dieselbe Ausgabe wie eine echte Leermenge: "Keine Ergebnisse fuer 'any,contains,Test'. Tipp: Breitere Suche mit 'any,contains,Begriff' versuchen." Der Leermengen-Hinweis wird also auch auf einem Strukturfehler gesetzt (siehe FID-006).
- POSITIVBEFUND: kein Docstring und keine Field-Description in src/ enthaelt eine Leermengen-Ausrede. Normalisierte Suche (`re.sub(r"\s+", " ", text)`, dann case-insensitiv) nach 'usually means', 'likely means', 'bedeutet meist', 'out of scope', 'not that it is wrong', 'wahrscheinlich nicht': null Treffer. NEGATIVKONTROLLE: derselbe Matcher findet die Phrase in 'An empty result\nusually  means out of scope' -> True.
- POSITIVBEFUND: server.py:297-300 setzt bei null Treffern einen konkreten naechsten Schritt ('Breitere Suche mit any,contains,Begriff'); server.py:652-656 nennt zusaetzlich den englischen Begriff bzw. ein breiteres Schlagwort. Die Fehlerpfade 401 und ConnectError nennen Konfiguration (ETH_LIBRARY_API_KEY bzw. Internetverbindung) statt der Query.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/FID-003.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- GEMESSEN ueber den echten ASGI-Stack (`build_http_app()`, tools/call auf `eth_search_resources`, `_http_get` auf `httpx.ConnectError` gesetzt): das Result traegt `isError: False` und `content[0].text = "Fehler bei Suche nach 'any,contains,Test': Verbindungsfehler. Internetverbindung pruefen."`. POSITIVKONTROLLE im selben Aufrufweg: ein Validierungsfehler (`query=""`) liefert `isError: True` — der Fehlerkanal existiert und funktioniert, der Server benutzt ihn fuer Upstream-Ausfaelle nie.
- src/eth_library_mcp/server.py:326-329, 474-477, 570-573, 676-679 — jedes Werkzeug endet in `except Exception as e: return _handle_error(...)` und gibt einen `str` zurueck. Transport-, Timeout- und Autorisierungsfehler (401, 403, 429, 5xx) erreichen den Aufrufer damit als gewoehnliches, erfolgreiches Tool-Result.
- src/eth_library_mcp/formatting.py:141-143 — der 404-Zweig der Suche lautet woertlich 'Keine Ergebnisse oder Endpunkt nicht gefunden (HTTP 404)'. Gemessen: ein 404 erzeugt genau diesen Text. Das ist die Vermischung, gegen die der Check steht — und BUG-02 war in diesem Repo exakt der Fall 'Route weg, HTTP 404', der hier als moegliche Leermenge angeboten wird.
- GEMESSEN: eine Antwort, deren Felder eine Ebene tiefer liegen (`{"results": {"docs": [...], "info": {...}}}`), erzeugt ZEICHENGLEICH dieselbe Ausgabe wie eine echte Leermenge: "Keine Ergebnisse fuer 'any,contains,Test'. Tipp: Breitere Suche mit 'any,contains,Begriff' versuchen." Der Leermengen-Hinweis wird also auch auf einem Strukturfehler gesetzt (siehe FID-006).
- POSITIVBEFUND: kein Docstring und keine Field-Description in src/ enthaelt eine Leermengen-Ausrede. Normalisierte Suche (`re.sub(r"\s+", " ", text)`, dann case-insensitiv) nach 'usually means', 'likely means', 'bedeutet meist', 'out of scope', 'not that it is wrong', 'wahrscheinlich nicht': null Treffer. NEGATIVKONTROLLE: derselbe Matcher findet die Phrase in 'An empty result\nusually  means out of scope' -> True.
- POSITIVBEFUND: server.py:297-300 setzt bei null Treffern einen konkreten naechsten Schritt ('Breitere Suche mit any,contains,Begriff'); server.py:652-656 nennt zusaetzlich den englischen Begriff bzw. ein breiteres Schlagwort. Die Fehlerpfade 401 und ConnectError nennen Konfiguration (ETH_LIBRARY_API_KEY bzw. Internetverbindung) statt der Query.

### Gaps

- Pflichtkriterium verletzt: Transport- und Autorisierungsfehler enden nicht im Fehlerkanal. `isError` bleibt auf allen Upstream-Ausfaellen False (gemessen, mit Positivkontrolle).
- Das leere Result traegt kein maschinenlesbares Feld (`hint`/`next_step`) — die Werkzeuge geben Markdown-`str` zurueck, der Hinweis ist Fliesstext und vom Ergebnis nicht trennbar.
- Der 404-Text fuehrt 'keine Ergebnisse' und 'Endpunkt nicht gefunden' in einem Satz zusammen; das Modell kann eine verschwundene Route nicht von einem leeren Bestand unterscheiden.
- Keine Description sagt, dass keine geratene Antwort an die Stelle eines fehlenden Treffers treten darf.
- Der Leermengen-Hinweis erscheint auch bei einer Strukturabweichung (gemessen) — der naechste Schritt zeigt dann auf die Query, waehrend der Lesepfad ins Leere zeigt.
- Nicht geprueft, weil gegenstandslos: kein Werkzeug gibt `input_required` zurueck, die drei `2026-07-28`-Disjunktheitskriterien sind hier ohne Gegenstand.
- Angrenzend (gehoert nicht in dieses Kriterium, faellt aber hier auf): die `instructions` des Servers bewerben weiterhin 'Personen-Suche mit Wikidata-Verlinkung' — gemessen im `initialize` des publizierten 0.4.0-Artefakts —, obwohl `eth_search_persons` in 0.4.0 entfernt wurde.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/FID-003.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### FID-004

## Finding: FID-004 — Parameter-Gruppen vollständig senden — Teilmengen erben Server-Defaults

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** FID-004
**Katalog-Referenz:** Custom (Portfolio-Fundstück termdat-mcp#11)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- POSITIVBEFUND src/eth_library_mcp/server.py:376 — `"avail": str(params.include_availability).lower()` sendet den einzigen booleschen Schalter des Servers bei JEDEM Request explizit, in beiden Zustaenden ('true' und 'false'). Das ist genau das Pass-Pattern des Checks; der Schalter kann damit verengen und nicht nur erweitern.
- POSITIVBEFUND src/eth_library_mcp/server.py:89-110 — `RESOURCE_TYPES` (10 Eintraege) und `ARCHIVE_SOURCES` (5 Eintraege) fuehren die VOLLSTAENDIGE Wertemenge der Facetten als Modulkonstanten, nicht nur die jeweils angeforderte Teilmenge; die `Literal`-Aliase `ResourceType`/`ArchiveKey` (Zeilen 66-86) erzwingen sie im Schema.
- src/eth_library_mcp/server.py:280-290, 531-541, 634-644 — `qInclude` wird aus der angeforderten Teilmenge gebaut (`facet_rtype`, `facet_lang`, `facet_tlevel`, `facet_data_source`). Nicht gesetzte Facetten werden weggelassen; ob das upstream 'kein Filter' oder eine Vorgabe bedeutet, ist nirgends belegt.
- Kein Live-Test misst die Wirkung eines Filterarguments: die einzigen beiden `@pytest.mark.live`-Tests (tests/test_server.py:262-293) pruefen Statuscodes von Routen, nicht Trefferzahlen mit und ohne Parameter.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/FID-004.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- POSITIVBEFUND src/eth_library_mcp/server.py:376 — `"avail": str(params.include_availability).lower()` sendet den einzigen booleschen Schalter des Servers bei JEDEM Request explizit, in beiden Zustaenden ('true' und 'false'). Das ist genau das Pass-Pattern des Checks; der Schalter kann damit verengen und nicht nur erweitern.
- POSITIVBEFUND src/eth_library_mcp/server.py:89-110 — `RESOURCE_TYPES` (10 Eintraege) und `ARCHIVE_SOURCES` (5 Eintraege) fuehren die VOLLSTAENDIGE Wertemenge der Facetten als Modulkonstanten, nicht nur die jeweils angeforderte Teilmenge; die `Literal`-Aliase `ResourceType`/`ArchiveKey` (Zeilen 66-86) erzwingen sie im Schema.
- src/eth_library_mcp/server.py:280-290, 531-541, 634-644 — `qInclude` wird aus der angeforderten Teilmenge gebaut (`facet_rtype`, `facet_lang`, `facet_tlevel`, `facet_data_source`). Nicht gesetzte Facetten werden weggelassen; ob das upstream 'kein Filter' oder eine Vorgabe bedeutet, ist nirgends belegt.
- Kein Live-Test misst die Wirkung eines Filterarguments: die einzigen beiden `@pytest.mark.live`-Tests (tests/test_server.py:262-293) pruefen Statuscodes von Routen, nicht Trefferzahlen mit und ohne Parameter.

### Gaps

- Kein Live-Wirkungsnachweis: fuer kein Filterargument ist gemessen, dass Einschraenken messbar verengt (`avail`, `open_access_only`, `resource_type`, `language`).
- Keine Tool-Description nennt das Default-Set der Quelle explizit; sie umschreiben es mit 'Standard: alle Inhalte abrufen' bzw. 'Standard: alle Ressourcen dieses Typs' — eine Behauptung ueber die Quelle ohne Beleg.
- Ob das Weglassen einer `facet_*`-Gruppe upstream wirklich 'kein Filter' heisst, ist ohne Parameter-Spezifikation der Discovery-API nicht belegt; die Spec liegt nicht im Repo und war in diesem Lauf nicht abfragbar (keine Netzzugriffe auf die ETH-API).
- `sort` wird nur bei gesetztem Wert gesendet (server.py:274) — das Mitglied faellt bei `None` auf die Gateway-Vorgabe zurueck.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/FID-004.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### FID-005

## Finding: FID-005 — Query-Syntax in der Tool-Description, nicht im README

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** FID-005
**Katalog-Referenz:** Custom (Portfolio-Fundstück termdat-mcp#11)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- POSITIVBEFUND src/eth_library_mcp/server.py:200-210 — die `query`-Description von `eth_search_resources` nennt das Aufrufformat ('Feld,Operator,Wert'), die Felder (any, title, creator, sub), die Operatoren (contains, exact, begins_with), die AND-Verknuepfung mit ';', die booleschen Operatoren (AND, OR, NOT) und ausdruecklich 'Wildcards (*) moeglich'. Gemessen am publizierten Artefakt: dieser Text steht so im `tools/list`-Schema, also im Kontext des Modells.
- GEGENBEFUND, gemessen am `tools/list` des installierten 0.4.0-Pakets: von vier freien Such-Argumenten dokumentiert nur eines die Abfragesprache. `eth_search_archive.query` ('Optionale Einschraenkung innerhalb des Archivs. Standard: alle Inhalte abrufen. Beispiel: any,contains,Zuerich'), `eth_search_by_type.query` ('Optionale Suchanfrage (Standard: alle Ressourcen dieses Typs)') und `eth_search_education.topic` ('Bildungsthema oder paedagogisches Stichwort') nennen weder Operatoren noch Wildcards.
- Suche nach der Matching-Granularitaet in src/ (`lucene|wildcard|fuzzy|ganze woerter|whole word|kompositum|substring|escape`, case-insensitiv): die einzigen Sach-Treffer sind server.py:208 ('Wildcards (*) moeglich') sowie zwei CORS-Stellen (server.py:837, 930), die von der Origin-Wildcard handeln. NEGATIVKONTROLLE: dasselbe Muster findet 'Matching is on whole words' in /tmp/p5.py — es greift.
- Kein Live-Test belegt die Wildcard-Wirkung: tests/test_server.py:262-293 sind die einzigen `@pytest.mark.live`-Tests und messen Routen-Statuscodes.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/FID-005.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- POSITIVBEFUND src/eth_library_mcp/server.py:200-210 — die `query`-Description von `eth_search_resources` nennt das Aufrufformat ('Feld,Operator,Wert'), die Felder (any, title, creator, sub), die Operatoren (contains, exact, begins_with), die AND-Verknuepfung mit ';', die booleschen Operatoren (AND, OR, NOT) und ausdruecklich 'Wildcards (*) moeglich'. Gemessen am publizierten Artefakt: dieser Text steht so im `tools/list`-Schema, also im Kontext des Modells.
- GEGENBEFUND, gemessen am `tools/list` des installierten 0.4.0-Pakets: von vier freien Such-Argumenten dokumentiert nur eines die Abfragesprache. `eth_search_archive.query` ('Optionale Einschraenkung innerhalb des Archivs. Standard: alle Inhalte abrufen. Beispiel: any,contains,Zuerich'), `eth_search_by_type.query` ('Optionale Suchanfrage (Standard: alle Ressourcen dieses Typs)') und `eth_search_education.topic` ('Bildungsthema oder paedagogisches Stichwort') nennen weder Operatoren noch Wildcards.
- Suche nach der Matching-Granularitaet in src/ (`lucene|wildcard|fuzzy|ganze woerter|whole word|kompositum|substring|escape`, case-insensitiv): die einzigen Sach-Treffer sind server.py:208 ('Wildcards (*) moeglich') sowie zwei CORS-Stellen (server.py:837, 930), die von der Origin-Wildcard handeln. NEGATIVKONTROLLE: dasselbe Muster findet 'Matching is on whole words' in /tmp/p5.py — es greift.
- Kein Live-Test belegt die Wildcard-Wirkung: tests/test_server.py:262-293 sind die einzigen `@pytest.mark.live`-Tests und messen Routen-Statuscodes.

### Gaps

- Die Matching-Granularitaet ist nirgends benannt — fuer eine deutschsprachige Quelle der Punkt, den der Check ausdruecklich verlangt: dass ein Kompositum von seinen Bestandteilen nicht gefunden wird ('Schulgeschichte' vs. 'Schulgeschichte*'). Kein Kompositum-Beispiel in irgendeiner Description.
- Drei von vier freien Such-Argumenten nennen die Abfragesprache gar nicht; `eth_search_education.topic` wird intern zu `any,contains,{topic}` gebaut (server.py:620), ohne dass der Aufrufer erfaehrt, dass er dort dieselbe Syntax nicht nutzen kann.
- Kein Wort zum Escaping von Sonderzeichen und kein Wort zum Verhalten bei ungueltiger Syntax.
- Kein `@pytest.mark.live`-Test, der die Wildcard-Wirkung misst; ohne ihn ist 'Wildcards (*) moeglich' eine Behauptung ueber die Quelle.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/FID-005.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### FID-006

## Finding: FID-006 — Antwortstruktur und Feldnamen bestätigen, bevor gezählt wird

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** FID-006
**Katalog-Referenz:** Custom (Portfolio-Fundstücke MCP Registry 2026-07 und zh-education-mcp / BISTA 2026-08-03)
**Spec-Baseline:** beide
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- GEMESSEN: eine Antwort, deren Felder eine Ebene tiefer liegen (`{"results": {"docs": [{...}], "info": {"total": 7}}}`), erzeugt zeichengleich dieselbe Ausgabe wie eine echte Leermenge — "Keine Ergebnisse fuer 'any,contains,Test'. Tipp: Breitere Suche mit 'any,contains,Begriff' versuchen." POSITIVKONTROLLE mit derselben Probe: `{"docs": [doc], "info": {"total": 42}}` liefert '**Treffer:** 42 total, zeige 1-1'. Die Probe unterscheidet also, und die Strukturabweichung ist von 'nichts gefunden' nicht zu trennen.
- src/eth_library_mcp/server.py:293-294, 450-451, 546-547, 648-649 — der Wurzelpfad wird viermal mit stillem Default gelesen: `docs = data.get("docs", [])` und `total = data.get("info", {}).get("total", 0)`. Keine dieser Stellen bestaetigt, dass `docs` ueberhaupt da war.
- src/eth_library_mcp/formatting.py:36, 44, 64, 67, 85 — die gelesenen Felder liegen hinter weiteren stillen Defaults (`doc.get("pnx", {})`, `doc.get("context", {}).get("mmsid", "")`, `doc.get("delivery", {}).get("link", [])`). Kein Zugriff bestaetigt den ersten Eintrag; ein verschobenes `pnx` erzeugt lautlos 'Kein Titel'.
- Kein eigener Fehlertyp fuer Strukturabweichungen: grep ueber src/ nach `SchemaError|UpstreamSchema|UnexpectedPayload|StructureError` liefert null Treffer, und in src/ ist keine `raise`-Stelle fuer eine unerwartete Antwortform vorhanden. Eine Normalisierung an der Parse-Grenze gibt es ebenfalls nicht (`_normalise_keys|_normalize_keys|casefold()` -> null).
- Fest verdrahtete gemischte Schreibweisen: src/eth_library_mcp/formatting.py:100-101 liest `link.get("displayLabel", "Link")` und `link.get("linkURL", "")` — zwei camelCase-Literale, deren Schreibweise nirgends gegen die Quelle bestaetigt wird, mit stillem Default dahinter.
- Der Mock traegt die Annahme: tests/test_tools.py:51-53 baut `_discovery_response()` von Hand als `{"docs": docs, "info": {"total": ...}}` und tests/test_tools.py:37 `_discovery_doc()` als `{"pnx": {...}}` — genau die Form, die der Produktivcode liest. tests/fixtures/PROVENANCE.md:35-40 haelt fest, dass die Discovery-Antwort bewusst NICHT aufgezeichnet ist (ohne API-Key nur 401). Es gibt damit keinen Test, der Struktur oder Feldnamen gegen eine ECHTE Antwort haelt.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/FID-006.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- GEMESSEN: eine Antwort, deren Felder eine Ebene tiefer liegen (`{"results": {"docs": [{...}], "info": {"total": 7}}}`), erzeugt zeichengleich dieselbe Ausgabe wie eine echte Leermenge — "Keine Ergebnisse fuer 'any,contains,Test'. Tipp: Breitere Suche mit 'any,contains,Begriff' versuchen." POSITIVKONTROLLE mit derselben Probe: `{"docs": [doc], "info": {"total": 42}}` liefert '**Treffer:** 42 total, zeige 1-1'. Die Probe unterscheidet also, und die Strukturabweichung ist von 'nichts gefunden' nicht zu trennen.
- src/eth_library_mcp/server.py:293-294, 450-451, 546-547, 648-649 — der Wurzelpfad wird viermal mit stillem Default gelesen: `docs = data.get("docs", [])` und `total = data.get("info", {}).get("total", 0)`. Keine dieser Stellen bestaetigt, dass `docs` ueberhaupt da war.
- src/eth_library_mcp/formatting.py:36, 44, 64, 67, 85 — die gelesenen Felder liegen hinter weiteren stillen Defaults (`doc.get("pnx", {})`, `doc.get("context", {}).get("mmsid", "")`, `doc.get("delivery", {}).get("link", [])`). Kein Zugriff bestaetigt den ersten Eintrag; ein verschobenes `pnx` erzeugt lautlos 'Kein Titel'.
- Kein eigener Fehlertyp fuer Strukturabweichungen: grep ueber src/ nach `SchemaError|UpstreamSchema|UnexpectedPayload|StructureError` liefert null Treffer, und in src/ ist keine `raise`-Stelle fuer eine unerwartete Antwortform vorhanden. Eine Normalisierung an der Parse-Grenze gibt es ebenfalls nicht (`_normalise_keys|_normalize_keys|casefold()` -> null).
- Fest verdrahtete gemischte Schreibweisen: src/eth_library_mcp/formatting.py:100-101 liest `link.get("displayLabel", "Link")` und `link.get("linkURL", "")` — zwei camelCase-Literale, deren Schreibweise nirgends gegen die Quelle bestaetigt wird, mit stillem Default dahinter.
- Der Mock traegt die Annahme: tests/test_tools.py:51-53 baut `_discovery_response()` von Hand als `{"docs": docs, "info": {"total": ...}}` und tests/test_tools.py:37 `_discovery_doc()` als `{"pnx": {...}}` — genau die Form, die der Produktivcode liest. tests/fixtures/PROVENANCE.md:35-40 haelt fest, dass die Discovery-Antwort bewusst NICHT aufgezeichnet ist (ohne API-Key nur 401). Es gibt damit keinen Test, der Struktur oder Feldnamen gegen eine ECHTE Antwort haelt.

### Gaps

- Der Wurzelpfad wird nie bestaetigt; jede Strukturaenderung der Discovery-API wird zu einem gueltigen leeren Ergebnis (gemessen).
- Die gelesenen Felder werden auf dem ersten Eintrag nicht bestaetigt.
- Kein eigener Fehlertyp; eine Abweichung endet im Leermengen-Zweig und traegt dort den Hinweis aus FID-003 — genau die im Check benannte Vermischung.
- Keine Fehlermeldung nennt die tatsaechlich vorhandenen Schluessel.
- Kein Test haelt Struktur und Feldnamen gegen die echte Antwort; die Gegenprobe gegen eine verschobene Antwort existiert nicht (ich habe sie ad hoc gefahren, sie ist nicht im Repo).
- Ob die Discovery-API ihre Schreibweise stabil haelt, ist in diesem Lauf nicht messbar (keine Netzzugriffe auf die ETH-API, kein Schluessel). Der Befund steht auf der fehlenden Bestaetigung, nicht auf einem beobachteten Wechsel.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/FID-006.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### FID-007

## Finding: FID-007 — Eine Zahlenspalte ohne Zahlen

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** FID-007
**Katalog-Referenz:** Custom (Portfolio-Fundstück zh-education-mcp / BISTA, 2026-08-03)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- GEMESSEN, mit Positivkontrolle. Probe gegen `eth_search_resources`, nur `info.total` variiert: `{"total": 42}` -> '**Treffer:** 42 total, zeige 1-1' (Positivkontrolle, die Probe misst die richtige Zeile). `info` fehlt -> '**Treffer:** 0 total, zeige 1-1' — eine Null neben einem angezeigten Treffer, still und plausibel. Das ist Fail-Pattern 2 des Checks.
- GEMESSEN, derselbe Aufbau: `{"total": None}` -> TypeError ('unsupported format string passed to NoneType.__format__'); `{"total": "1 bis 5"}` und sogar `{"total": "42"}` (eine Zahl als String!) -> ValueError ("Cannot specify ',' with 's'."). Alle drei enden am Sammel-`except` und erreichen den Aufrufer als 'Fehler bei Suche nach ...: Unbekannter Fehler. Bitte spaeter erneut versuchen.' Das ist Fail-Pattern 1, und der Nutzende erfaehrt nichts.
- src/eth_library_mcp/server.py:294, 451, 547, 649 — `total = data.get("info", {}).get("total", 0)`: vier Stellen, an denen aus einer fehlenden Zahl still eine Null wird. Genau der `.get(..., 0)`-Fund, den die Check-Verifikation sucht.
- src/eth_library_mcp/server.py:305, 461, 556, 660 — `f"{total:,}"` bzw. `f"**Treffer:** {total:,} total"` formatiert den Quellwert ohne jede Konvertierung und ohne Kenntnis des Falls 'keine Zahl'.
- Der Code kennt keine Unterdrueckungs-/Nicht-Zahl-Marker: grep ueber src/ nach `"1 bis 5"|"<5"|"k\.A\."|isdigit\(\)|suppress|unterdrueck|unterdrück` sowie nach `suppressed|Untergrenze|nicht enthalten` liefert null Treffer. NEGATIVKONTROLLE fuer dieselbe Musterklasse: das Zahlen-Muster `[0-9]+\.[0-9]+\.[0-9]+` findet in /tmp/probe_v.py eine Zeile — die grep-Mechanik greift, die Begriffe fehlen tatsaechlich.
- Kein Live-Test haelt die tatsaechlich vorkommenden Nicht-Zahlen gegen eine Marker-Liste; die einzigen beiden `@pytest.mark.live`-Tests (tests/test_server.py:262-293) messen Routen-Statuscodes.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/FID-007.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- GEMESSEN, mit Positivkontrolle. Probe gegen `eth_search_resources`, nur `info.total` variiert: `{"total": 42}` -> '**Treffer:** 42 total, zeige 1-1' (Positivkontrolle, die Probe misst die richtige Zeile). `info` fehlt -> '**Treffer:** 0 total, zeige 1-1' — eine Null neben einem angezeigten Treffer, still und plausibel. Das ist Fail-Pattern 2 des Checks.
- GEMESSEN, derselbe Aufbau: `{"total": None}` -> TypeError ('unsupported format string passed to NoneType.__format__'); `{"total": "1 bis 5"}` und sogar `{"total": "42"}` (eine Zahl als String!) -> ValueError ("Cannot specify ',' with 's'."). Alle drei enden am Sammel-`except` und erreichen den Aufrufer als 'Fehler bei Suche nach ...: Unbekannter Fehler. Bitte spaeter erneut versuchen.' Das ist Fail-Pattern 1, und der Nutzende erfaehrt nichts.
- src/eth_library_mcp/server.py:294, 451, 547, 649 — `total = data.get("info", {}).get("total", 0)`: vier Stellen, an denen aus einer fehlenden Zahl still eine Null wird. Genau der `.get(..., 0)`-Fund, den die Check-Verifikation sucht.
- src/eth_library_mcp/server.py:305, 461, 556, 660 — `f"{total:,}"` bzw. `f"**Treffer:** {total:,} total"` formatiert den Quellwert ohne jede Konvertierung und ohne Kenntnis des Falls 'keine Zahl'.
- Der Code kennt keine Unterdrueckungs-/Nicht-Zahl-Marker: grep ueber src/ nach `"1 bis 5"|"<5"|"k\.A\."|isdigit\(\)|suppress|unterdrueck|unterdrück` sowie nach `suppressed|Untergrenze|nicht enthalten` liefert null Treffer. NEGATIVKONTROLLE fuer dieselbe Musterklasse: das Zahlen-Muster `[0-9]+\.[0-9]+\.[0-9]+` findet in /tmp/probe_v.py eine Zeile — die grep-Mechanik greift, die Begriffe fehlen tatsaechlich.
- Kein Live-Test haelt die tatsaechlich vorkommenden Nicht-Zahlen gegen eine Marker-Liste; die einzigen beiden `@pytest.mark.live`-Tests (tests/test_server.py:262-293) messen Routen-Statuscodes.

### Gaps

- Keine Konvertierung kennt den Fall 'keine Zahl'; ein nicht-ganzzahliges `info.total` toetet den gesamten Suchaufruf (gemessen) — auch bei einem harmlosen numerischen String.
- Ein fehlendes `info` wird still zu 0 und steht dann neben angezeigten Treffern (gemessen): eine falsche Zahl, der nichts anzusehen ist.
- Kein Tool-Result nennt ausgenommene oder unlesbare Werte, keine Richtungsangabe, keine Marker-Liste an einer Stelle, kein Live-Test, keine Gegenprobe.
- Die generische Fehlermeldung 'Bitte spaeter erneut versuchen' gibt einer deterministischen Absage einen Wiederholungsrat — dieselbe Klasse wie der 400/lotId-Fall in CLAUDE.md.
- Einordnung, damit der Befund nicht ueberdehnt wird: die ETH-Discovery-API ist ein Bibliothekskatalog, und ob sie Fallzahlen unterdrueckt oder Bereichsmarker wie '1 bis 5' schreibt, ist NICHT gemessen — dafuer haette es einen Schluessel und einen Netzzugriff gebraucht, beides war ausgeschlossen. Der Befund steht auf dem, was messbar war: der stillen Null und dem Absturz bei jedem nicht-ganzzahligen Wert.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/FID-007.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### IDENT-002

## Finding: IDENT-002 — __version__ aus der installierten Distribution, nicht von Hand gepflegt

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** IDENT-002
**Katalog-Referenz:** Custom (Portfolio-Sweep 2026-07-29, 30 Server)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- POSITIVBEFUND src/eth_library_mcp/__init__.py:6-19 — `__version__ = _distribution_version("eth-library-mcp")` mit `except PackageNotFoundError` und dem Marker `0.0.0+source`. Der Versionsblock steht vor allen weiteren Definitionen; `__init__.py` importiert kein Submodul, ein Zirkelimport ist ausgeschlossen.
- BEFUND src/eth_library_mcp/server.py:713 — `**Version:** 0.3.0` als Literal im Rueckgabetext von `eth_library_info`. GEMESSEN im Checkout: `asyncio.run(eth_library_info())` liefert die Zeile '**Version:** 0.3.0', waehrend `eth_library_mcp.__version__` '0.4.0' meldet. GEMESSEN auch am AUS DEM INDEX installierten 0.4.0-Paket (tools/call ueber stdio, `isError: False`): dieselbe Zeile '**Version:** 0.3.0'. Die Drift wird also ausgeliefert, nicht bloss gehalten.
- Das Gate sieht dieses Literal nicht. `python scripts/check_version_sync.py` auf sauberem Baum meldet 'Versions-Sync OK (0.4.0; ...; keine hartkodierte Version in src/)' und exitet 0 — obwohl 0.3.0 in src/ steht. NEGATIVKONTROLLE gegen den Detektor selbst (`own_ua_versions` + das `__version__`-Muster aus `find_hardcoded`): 'USER_AGENT = "eth-library-mcp/1.2.3"' -> gemeldet, '__version__ = "1.2.3"' -> gemeldet, '__version__ = "0.0.0+source"' -> korrekt ausgenommen, '**Version:** 0.3.0' -> NICHT gemeldet. Der Detektor greift, er kennt diese Form nur nicht.
- Der Versions-Test ist eine Tautologie: tests/test_server.py:27-40 prueft `__version__ == version("eth-library-mcp")`. Beide Seiten stammen aus denselben installierten Metadaten und koennen nicht widersprechen — der im Check ausdruecklich als Nicht-Behebung benannte Vergleich. Dasselbe in tests/test_server_identity.py:132 und 157 (`info["version"] == _distribution_version(...)`).
- GEGENPROBE gefahren, wie vom Check verlangt: `server.json -> version` auf '0.0.0-verstimmt' gesetzt, `PYTHONPATH=src pytest tests/ -m "not live" -q` -> 128 passed, 2 deselected. Die Suite bleibt vollstaendig GRUEN. Nur das CI-Gate `scripts/check_version_sync.py` schlaegt an (exit 1, 'server.json -> version = 0.0.0-verstimmt'). Es gibt also keinen Test, der die Invariante `__version__` gegen `server.json` haelt. Danach `git checkout server.json`.
- Kein Versions-Literal in tests/: `grep -rnE '__version__\s*==\s*"[0-9]+\.[0-9]|==\s*"v?[0-9]+\.[0-9]+\.[0-9]+"' tests/` -> Exit 1. NEGATIVKONTROLLE: dasselbe Muster findet `assert __version__ == "0.3.0"` in /tmp/pt.py.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/IDENT-002.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- POSITIVBEFUND src/eth_library_mcp/__init__.py:6-19 — `__version__ = _distribution_version("eth-library-mcp")` mit `except PackageNotFoundError` und dem Marker `0.0.0+source`. Der Versionsblock steht vor allen weiteren Definitionen; `__init__.py` importiert kein Submodul, ein Zirkelimport ist ausgeschlossen.
- BEFUND src/eth_library_mcp/server.py:713 — `**Version:** 0.3.0` als Literal im Rueckgabetext von `eth_library_info`. GEMESSEN im Checkout: `asyncio.run(eth_library_info())` liefert die Zeile '**Version:** 0.3.0', waehrend `eth_library_mcp.__version__` '0.4.0' meldet. GEMESSEN auch am AUS DEM INDEX installierten 0.4.0-Paket (tools/call ueber stdio, `isError: False`): dieselbe Zeile '**Version:** 0.3.0'. Die Drift wird also ausgeliefert, nicht bloss gehalten.
- Das Gate sieht dieses Literal nicht. `python scripts/check_version_sync.py` auf sauberem Baum meldet 'Versions-Sync OK (0.4.0; ...; keine hartkodierte Version in src/)' und exitet 0 — obwohl 0.3.0 in src/ steht. NEGATIVKONTROLLE gegen den Detektor selbst (`own_ua_versions` + das `__version__`-Muster aus `find_hardcoded`): 'USER_AGENT = "eth-library-mcp/1.2.3"' -> gemeldet, '__version__ = "1.2.3"' -> gemeldet, '__version__ = "0.0.0+source"' -> korrekt ausgenommen, '**Version:** 0.3.0' -> NICHT gemeldet. Der Detektor greift, er kennt diese Form nur nicht.
- Der Versions-Test ist eine Tautologie: tests/test_server.py:27-40 prueft `__version__ == version("eth-library-mcp")`. Beide Seiten stammen aus denselben installierten Metadaten und koennen nicht widersprechen — der im Check ausdruecklich als Nicht-Behebung benannte Vergleich. Dasselbe in tests/test_server_identity.py:132 und 157 (`info["version"] == _distribution_version(...)`).
- GEGENPROBE gefahren, wie vom Check verlangt: `server.json -> version` auf '0.0.0-verstimmt' gesetzt, `PYTHONPATH=src pytest tests/ -m "not live" -q` -> 128 passed, 2 deselected. Die Suite bleibt vollstaendig GRUEN. Nur das CI-Gate `scripts/check_version_sync.py` schlaegt an (exit 1, 'server.json -> version = 0.0.0-verstimmt'). Es gibt also keinen Test, der die Invariante `__version__` gegen `server.json` haelt. Danach `git checkout server.json`.
- Kein Versions-Literal in tests/: `grep -rnE '__version__\s*==\s*"[0-9]+\.[0-9]|==\s*"v?[0-9]+\.[0-9]+\.[0-9]+"' tests/` -> Exit 1. NEGATIVKONTROLLE: dasselbe Muster findet `assert __version__ == "0.3.0"` in /tmp/pt.py.

### Gaps

- Pflichtkriterium verletzt: ein Versions-Literal unter src/, das nicht der Fallback-Marker ist (server.py:713) — und es ist veraltet und wird ausgeliefert.
- Pflichtkriterium verletzt: der Versions-Test vergleicht zwei Ableitungen derselben Quelle statt einer Invariante zwischen zwei unabhaengig gepflegten Stellen (`__version__` gegen `server.json`).
- Dieser Test war nie rot: das Verstimmen von `server.json` laesst die Suite gruen (gemessen).
- Kein Test vergleicht die INSTALLIERTEN Metadaten gegen `pyproject.toml`; `check_version_sync.py` vergleicht ausschliesslich Dateien miteinander und liest `importlib.metadata` nie. Damit faengt nichts den Editable-Install-Fall, und keine Fehlermeldung nennt ihn.
- `test_import_version` wuerde ohne Installation mit `PackageNotFoundError` scheitern statt uebersprungen zu werden.
- Beobachtet, gehoert zum Editable-Install-Fall: unter /usr/local/lib/python3.11/dist-packages liegen ZWEI dist-info-Verzeichnisse desselben Pakets (`eth_library_mcp-0.3.4.dist-info` und `-0.4.0.dist-info`), beide als editable auf denselben Baum zeigend. `version()` liefert hier 0.4.0, aber die Aufloesung haengt an der Reihenfolge — und kein Test wuerde einen Rueckfall auf 0.3.4 bemerken.
- Aus diesem Check wurde NICHT auf die Identitaet des publizierten Pakets geschlossen; die dortige Messung steht in IDENT-001 (Modus 3) und IDENT-006/007.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/IDENT-002.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### IDENT-003

## Finding: IDENT-003 — Werte, die die Pipeline überschreibt, brauchen einen eigenen Check

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** IDENT-003
**Katalog-Referenz:** Custom (Portfolio-Sweep 2026-07-29, 30 Server)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Committete Fassung stimmt: `pyproject.toml` version = 0.4.0, `server.json -> version` = 0.4.0, `server.json -> packages[0].version` = 0.4.0. `python scripts/check_version_sync.py` exitet 0 und nennt in seiner Ausgabe alle geprueften Stellen einzeln ('server.json -> version, server.json -> packages[0].version, README.de.md -> Versions-Badge, README.md -> Versions-Badge').
- GEGENPROBE, zweifach gefahren: (a) `server.json -> version` auf '0.0.0-verstimmt' -> exit 1 mit Nennung der Stelle; (b) NUR `packages[0].version` verstimmt, `version` korrekt gelassen -> exit 1 mit 'server.json -> packages[0].version = 0.0.0-verstimmt'. Die Package-Ebene wird also wirklich einzeln geprueft und nicht bloss mitgezaehlt. Beide Male `git checkout server.json`.
- Das Gate laeuft in der CI: .github/workflows/ci.yml, Schritt 'Versions-Sync (pyproject <-> server.json / README / src)' -> `python scripts/check_version_sync.py`, als Schritt in einem bestehenden Job, nicht als eigener Job (kein neuer Check-Name, keine Kollision mit Branch-Rulesets). Das Skript nutzt ausschliesslich die Standardbibliothek (Docstring Zeilen 25-28) und braucht keine Projekt-Installation.
- Die ueberschriebenen Werte sind dokumentiert: scripts/check_version_sync.py:11-16 haelt fest, dass `publish.yml` `server.json` beim Veroeffentlichen aus dem Tag-Namen synchronisiert und die committete Version deshalb nie auf das publizierte Artefakt wirkt. Das Inventar ist klein: `grep -rn "sed -i|jq '\.|yq -i|::set-output|GITHUB_REF_NAME" .github/workflows/` trifft genau den einen Schritt in publish.yml:67-71.
- MODUS 3a, die GESCHRIEBENE Seite zurueckgelesen. PyPI: `https://pypi.org/pypi/eth-library-mcp/json` -> info.version 0.4.0, hochgeladen 2026-09-19T17:05:54Z. MCP-Registry: `https://registry.modelcontextprotocol.io/v0/servers?search=eth-library-mcp` -> drei Eintraege (0.3.3, 0.3.4, 0.4.0); der mit `isLatest: true` ist 0.4.0, publishedAt 2026-09-19T17:06:04Z, mit `packages[0].version` = 0.4.0 und der bereinigten Beschreibung 'ETH Library Discovery API'. Beide publizierten Seiten und der Tag v0.4.0 tragen dieselbe Nummer; genau ein Schritt haette abweichen koennen, keiner tat es. HINWEIS ZUR MESSUNG: der ERSTE Eintrag der Registry-Antwort ist 0.3.3 mit der alten Beschreibung 'ETH Library Discovery and Persons APIs' — wer `servers[0]` liest statt `isLatest`, meldet hier eine Drift, die es nicht gibt.
- MODUS 3b, die Transformation ausgefuehrt statt gelesen: `jq --arg v "1.2.3" '.version = $v | .packages[0].version = $v' server.json` gegen den Tag 1.2.3 durchgespielt -> beide Stellen '1.2.3' (OK/OK). `git status --short` danach: server.json unveraendert.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/IDENT-003.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Committete Fassung stimmt: `pyproject.toml` version = 0.4.0, `server.json -> version` = 0.4.0, `server.json -> packages[0].version` = 0.4.0. `python scripts/check_version_sync.py` exitet 0 und nennt in seiner Ausgabe alle geprueften Stellen einzeln ('server.json -> version, server.json -> packages[0].version, README.de.md -> Versions-Badge, README.md -> Versions-Badge').
- GEGENPROBE, zweifach gefahren: (a) `server.json -> version` auf '0.0.0-verstimmt' -> exit 1 mit Nennung der Stelle; (b) NUR `packages[0].version` verstimmt, `version` korrekt gelassen -> exit 1 mit 'server.json -> packages[0].version = 0.0.0-verstimmt'. Die Package-Ebene wird also wirklich einzeln geprueft und nicht bloss mitgezaehlt. Beide Male `git checkout server.json`.
- Das Gate laeuft in der CI: .github/workflows/ci.yml, Schritt 'Versions-Sync (pyproject <-> server.json / README / src)' -> `python scripts/check_version_sync.py`, als Schritt in einem bestehenden Job, nicht als eigener Job (kein neuer Check-Name, keine Kollision mit Branch-Rulesets). Das Skript nutzt ausschliesslich die Standardbibliothek (Docstring Zeilen 25-28) und braucht keine Projekt-Installation.
- Die ueberschriebenen Werte sind dokumentiert: scripts/check_version_sync.py:11-16 haelt fest, dass `publish.yml` `server.json` beim Veroeffentlichen aus dem Tag-Namen synchronisiert und die committete Version deshalb nie auf das publizierte Artefakt wirkt. Das Inventar ist klein: `grep -rn "sed -i|jq '\.|yq -i|::set-output|GITHUB_REF_NAME" .github/workflows/` trifft genau den einen Schritt in publish.yml:67-71.
- MODUS 3a, die GESCHRIEBENE Seite zurueckgelesen. PyPI: `https://pypi.org/pypi/eth-library-mcp/json` -> info.version 0.4.0, hochgeladen 2026-09-19T17:05:54Z. MCP-Registry: `https://registry.modelcontextprotocol.io/v0/servers?search=eth-library-mcp` -> drei Eintraege (0.3.3, 0.3.4, 0.4.0); der mit `isLatest: true` ist 0.4.0, publishedAt 2026-09-19T17:06:04Z, mit `packages[0].version` = 0.4.0 und der bereinigten Beschreibung 'ETH Library Discovery API'. Beide publizierten Seiten und der Tag v0.4.0 tragen dieselbe Nummer; genau ein Schritt haette abweichen koennen, keiner tat es. HINWEIS ZUR MESSUNG: der ERSTE Eintrag der Registry-Antwort ist 0.3.3 mit der alten Beschreibung 'ETH Library Discovery and Persons APIs' — wer `servers[0]` liest statt `isLatest`, meldet hier eine Drift, die es nicht gibt.
- MODUS 3b, die Transformation ausgefuehrt statt gelesen: `jq --arg v "1.2.3" '.version = $v | .packages[0].version = $v' server.json` gegen den Tag 1.2.3 durchgespielt -> beide Stellen '1.2.3' (OK/OK). `git status --short` danach: server.json unveraendert.

### Gaps

- Die Transformation in .github/workflows/publish.yml:70 greift auf `.packages[0].version`, nicht auf `.packages[].version`. Heute folgenlos, weil `server.json` genau einen Package-Eintrag fuehrt — das ist ein Zustand, keine Eigenschaft. Ein zweiter Eintrag waere im PUBLIZIERTEN Manifest desynchron, und kein Check dieses Repos wuerde es sehen, weil alle nur die Datei im Repo lesen.
- Kein expliziter Tag-Schutz um `VERSION="${GITHUB_REF_NAME#v}"`: der Workflow ist heute nur durch seinen Trigger abgesichert (`on: release: types: [published]`, kein `workflow_dispatch`). Kommt je ein Branch-Trigger dazu, schreibt die Zeile den Branch-Namen als Version.
- Die Beschreibung in `server.json` und `pyproject.toml` haelt kein Gate synchron — `check_version_sync.py` prueft ausschliesslich Zahlen; das haelt nur tests/test_server_identity.py:271-294 fest, und auch dort nur `websiteUrl`, nicht `description`.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/IDENT-003.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### IDENT-004

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


### IDENT-006

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


### IDENT-007

## Finding: IDENT-007 — Das veröffentlichte Artefakt startet in einer leeren Umgebung

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** IDENT-007
**Katalog-Referenz:** Custom (Portfolio-Fundstücke zurich-opendata-mcp 0.5.1, 2026-07-31; swiss-energy-mcp, 2026-08-01)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Leere Umgebung, aus dem INDEX installiert: `python -m venv /tmp/verify7` und `/tmp/verify7/bin/pip install --no-cache-dir "eth-library-mcp==0.4.0"` -> exit 0. Kein Checkout, kein Lockfile, kein Constraint aus dem Repo, kein Cache.
- IMPORT: `/tmp/verify7/bin/python -c "import eth_library_mcp; print(eth_library_mcp.__version__)"` -> 'import ok 0.4.0', exit 0.
- AUFGELOESTE KERN-ABHAENGIGKEITEN protokolliert (`pip freeze` im venv, 2026-09-19): mcp==2.2.0, mcp-types==2.2.0, httpx==0.28.1, httpx2==2.13.0, pydantic==2.13.5, pydantic_core==2.46.5, structlog==26.1.0, starlette==1.6.0, uvicorn==0.53.0. Die Deckelung `mcp[cli]>=2.0.0,<3` steht auch in den Index-Metadaten (`requires_dist`), der Resolver bleibt also in 2.x.
- ENTRY POINT startet und beantwortet `initialize`: `/tmp/verify7/bin/eth-library-mcp` ueber stdio -> serverInfo {name: eth_library_mcp, title: 'ETH-Bibliothek Zuerich', version: '0.4.0', description: 'MCP Server for ETH Library Zurich - ...', websiteUrl: 'https://github.com/malkreide/eth-library-mcp'}. `tools/list` -> 6 Werkzeuge (eth_search_resources, eth_get_resource, eth_search_archive, eth_search_by_type, eth_search_education, eth_library_info).
- ECHTER tools/call gegen das installierte Artefakt, stdin bis zur Antwort offen gehalten (der erste Versuch mit einer geschlossenen Pipe bekam keine Antwort — der Prozess fuhr nach 76 ms herunter; das ist die im Check benannte Falle, nicht ein Defekt des Pakets): `tools/call name=eth_library_info` -> `isError: false`, 1722 Zeichen Antworttext. Nicht leer, kein Fehler.
- RELEASE NICHT ZURUECKGEZOGEN: PyPI-Metadaten zu 0.4.0 melden `yanked: false`, `yanked_reason: null`; auch keine der 2 Dateien des Releases ist yanked.
- `TOOL_ERROR` war nicht einschlaegig und musste deshalb nicht gegen eine Egress-Allow-List geprueft werden: der gefahrene Aufruf ist das einzige Werkzeug mit `openWorldHint: False`, das keinen Upstream anspricht.

### Expected Behavior

Die Pass-Kriterien stehen in `checks/IDENT-007.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Leere Umgebung, aus dem INDEX installiert: `python -m venv /tmp/verify7` und `/tmp/verify7/bin/pip install --no-cache-dir "eth-library-mcp==0.4.0"` -> exit 0. Kein Checkout, kein Lockfile, kein Constraint aus dem Repo, kein Cache.
- IMPORT: `/tmp/verify7/bin/python -c "import eth_library_mcp; print(eth_library_mcp.__version__)"` -> 'import ok 0.4.0', exit 0.
- AUFGELOESTE KERN-ABHAENGIGKEITEN protokolliert (`pip freeze` im venv, 2026-09-19): mcp==2.2.0, mcp-types==2.2.0, httpx==0.28.1, httpx2==2.13.0, pydantic==2.13.5, pydantic_core==2.46.5, structlog==26.1.0, starlette==1.6.0, uvicorn==0.53.0. Die Deckelung `mcp[cli]>=2.0.0,<3` steht auch in den Index-Metadaten (`requires_dist`), der Resolver bleibt also in 2.x.
- ENTRY POINT startet und beantwortet `initialize`: `/tmp/verify7/bin/eth-library-mcp` ueber stdio -> serverInfo {name: eth_library_mcp, title: 'ETH-Bibliothek Zuerich', version: '0.4.0', description: 'MCP Server for ETH Library Zurich - ...', websiteUrl: 'https://github.com/malkreide/eth-library-mcp'}. `tools/list` -> 6 Werkzeuge (eth_search_resources, eth_get_resource, eth_search_archive, eth_search_by_type, eth_search_education, eth_library_info).
- ECHTER tools/call gegen das installierte Artefakt, stdin bis zur Antwort offen gehalten (der erste Versuch mit einer geschlossenen Pipe bekam keine Antwort — der Prozess fuhr nach 76 ms herunter; das ist die im Check benannte Falle, nicht ein Defekt des Pakets): `tools/call name=eth_library_info` -> `isError: false`, 1722 Zeichen Antworttext. Nicht leer, kein Fehler.
- RELEASE NICHT ZURUECKGEZOGEN: PyPI-Metadaten zu 0.4.0 melden `yanked: false`, `yanked_reason: null`; auch keine der 2 Dateien des Releases ist yanked.
- `TOOL_ERROR` war nicht einschlaegig und musste deshalb nicht gegen eine Egress-Allow-List geprueft werden: der gefahrene Aufruf ist das einzige Werkzeug mit `openWorldHint: False`, das keinen Upstream anspricht.

### Gaps

- Kein wiederkehrender Lauf prueft das PUBLIZIERTE Paket. Der einzige `schedule:`-Workflow ist .github/workflows/live-tests.yml (taeglich 06:17 UTC), und dessen Install-Schritt lautet `pip install -e ".[dev]"` (Zeile 42) — er prueft den Checkout, also genau das, was die CI schon prueft. Damit ist die Antwort auf diesen Check ein Zeitpunkt (2026-09-19) und kein Zustand: der Vorfall, gegen den er existiert, entsteht ohne Commit.
- Von den 6 Werkzeugen wurde genau eines per `tools/call` gefahren — das einzige ohne Upstream-Aufruf. Die fuenf Discovery-Werkzeuge wurden am Artefakt NICHT ausgeloest, weil Netzzugriffe auf die ETH-API fuer diesen Lauf ausgeschlossen waren und die API ohnehin einen Schluessel verlangt. Der `meteoswiss-mcp`-Fall (Werkzeuge, die listen und nichts liefern) waere damit an diesem Artefakt nicht aufgefallen.
- Am selben, aus dem Index installierten Artefakt gemessen und hier festgehalten, weil es der einzige Ort ist, an dem es sichtbar wird: die Antwort von `eth_library_info` traegt '**Version:** 0.3.0' (Befund unter IDENT-002), und die `instructions` im `initialize` bewerben weiterhin 'Personen-Suche mit Wikidata-Verlinkung' fuer ein Werkzeug, das 0.4.0 entfernt hat. Beides macht das Artefakt nicht funktionsunfaehig und ist deshalb kein Verstoss gegen die Kriterien dieses Checks.
- Geprueft wurde die Wheel-Variante; ein sdist-Build wurde nicht gesondert installiert und gestartet.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/IDENT-007.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### OBS-001

## Finding: OBS-001 — Protocol vs. Execution Errors: korrekte Trennung

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OBS-001
**Katalog-Referenz:** Sec 6.1
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Laufzeitmessung am 2026-09-19 ueber eine echte In-Process-`Client(mcp)`-Sitzung (PYTHONPATH=src, kein Netz): Ein Argument ausserhalb des Bereichs (`limit=9999`) kommt als Tool-Result mit `isError=True` zurueck, Text "1 validation error for eth_search_resourcesArguments / params.limit / Input should be less than or equal to 100 [type=less_than_equal, input_value=9999]" — Validierungsfehler laufen ueber den Execution-Pfad (SEP-1303), nicht ueber JSON-RPC
- Dieselbe Messung, fehlendes Pflichtfeld: `isError=True`, Text nennt Feld und Grund ("params.query / Field required"). Extra-Feld: `isError=True`, "params.quatsch / Extra inputs are not permitted" — das Modell erfaehrt Feldname UND erwarteten Wertebereich und kann den naechsten Versuch korrigieren
- src/eth_library_mcp/server.py:266,323-326 (und analog bei allen sechs Werkzeugen) — jeder Tool-Handler umschliesst den Aufruf mit `try: ... except Exception as e:` und gibt `_handle_error(...)` zurueck, statt die Exception durchzureichen; kein Werkzeug laesst einen Upstream-Fehler als Protokollfehler nach aussen
- src/eth_library_mcp/formatting.py:128-157 — Fallunterscheidung je Upstream-Status (401 mit Registrierungslink, 403, 404 kontextabhaengig search/by-id, 429 mit Wartehinweis, Timeout, ConnectError); jede Meldung ist handlungsleitend formuliert
- Gemessen: `grep -rnE '\-320[0-9][0-9]|isError|is_error|McpError|ErrorData' src/ tests/` -> 0 Treffer. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit `raise McpError(code=-32602)` und `isError` liefert 2 Treffer, es greift also. Der Server belegt damit keinen eigenen Code im auf der Baseline 2026-07-28 reservierten Bereich -32020...-32099
- pyproject.toml:11 + src/eth_library_mcp/server.py:195,335,395,485,584 — alle Eingaben laufen ueber Pydantic-BaseModel mit `ConfigDict(str_strip_whitespace=True, extra="forbid")` und Field-Constraints; die Validierung findet an der Werkzeuggrenze statt und nicht im Handler

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OBS-001.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Laufzeitmessung am 2026-09-19 ueber eine echte In-Process-`Client(mcp)`-Sitzung (PYTHONPATH=src, kein Netz): Ein Argument ausserhalb des Bereichs (`limit=9999`) kommt als Tool-Result mit `isError=True` zurueck, Text "1 validation error for eth_search_resourcesArguments / params.limit / Input should be less than or equal to 100 [type=less_than_equal, input_value=9999]" — Validierungsfehler laufen ueber den Execution-Pfad (SEP-1303), nicht ueber JSON-RPC
- Dieselbe Messung, fehlendes Pflichtfeld: `isError=True`, Text nennt Feld und Grund ("params.query / Field required"). Extra-Feld: `isError=True`, "params.quatsch / Extra inputs are not permitted" — das Modell erfaehrt Feldname UND erwarteten Wertebereich und kann den naechsten Versuch korrigieren
- src/eth_library_mcp/server.py:266,323-326 (und analog bei allen sechs Werkzeugen) — jeder Tool-Handler umschliesst den Aufruf mit `try: ... except Exception as e:` und gibt `_handle_error(...)` zurueck, statt die Exception durchzureichen; kein Werkzeug laesst einen Upstream-Fehler als Protokollfehler nach aussen
- src/eth_library_mcp/formatting.py:128-157 — Fallunterscheidung je Upstream-Status (401 mit Registrierungslink, 403, 404 kontextabhaengig search/by-id, 429 mit Wartehinweis, Timeout, ConnectError); jede Meldung ist handlungsleitend formuliert
- Gemessen: `grep -rnE '\-320[0-9][0-9]|isError|is_error|McpError|ErrorData' src/ tests/` -> 0 Treffer. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit `raise McpError(code=-32602)` und `isError` liefert 2 Treffer, es greift also. Der Server belegt damit keinen eigenen Code im auf der Baseline 2026-07-28 reservierten Bereich -32020...-32099
- pyproject.toml:11 + src/eth_library_mcp/server.py:195,335,395,485,584 — alle Eingaben laufen ueber Pydantic-BaseModel mit `ConfigDict(str_strip_whitespace=True, extra="forbid")` und Field-Constraints; die Validierung findet an der Werkzeuggrenze statt und nicht im Handler

### Gaps

- Ausfuehrungsfehler kommen NICHT mit `isError: true` zurueck. Gemessen ueber dieselbe Client-Sitzung mit respx-gemocktem Upstream: HTTP 401 -> `is_error = False`, Text "Fehler bei Suche nach '...': Kein gueltiger API-Key..."; HTTP 429 -> `is_error = False`; httpx.ConnectError -> `is_error = False`. Der Rueckgabetyp aller sechs Werkzeuge ist `str`, also ist jedes Ergebnis formal ein Erfolg. Das Modell muss den Fehlerfall am deutschen Prosatext erkennen statt am Protokollfeld
- Ein unbekanntes Werkzeug ist ebenfalls kein Protokollfehler: `call_tool("gibt_es_nicht", {})` liefert gemessen `isError=True` ("Unknown tool: gibt_es_nicht") statt eines JSON-RPC-Fehlers -32601. Das ist Verhalten des SDK (mcp 2.x), nicht dieses Repos, faellt aber unter das Pass-Kriterium «standardisierte Fehlercodes fuer Protocol-Level-Errors» und ist hier nirgends dokumentiert
- Damit fallen Execution-Error und Protocol-Error in der Drahtform zusammen: Der Validierungsfehler traegt isError=True, der Upstream-Fehler isError=False, der unbekannte Werkzeugname isError=True. Ein Client kann aus dem Flag nicht ableiten, welche der drei Lagen vorliegt
- Kein Test belegt den Protocol-Error-Pfad (falscher Werkzeugname): `grep -rn 'gibt_es_nicht|Unknown tool|unknown_tool' tests/` findet nichts; tests/test_tools.py:83-133 deckt nur Upstream-Statuscodes ab
- Kein Test belegt, dass ein ungueltiges Argument als Execution-Error zurueckkommt — die in dieser Messung nachgewiesene SEP-1303-Konformitaet ist Verhalten des SDK und durch nichts im Repo festgehalten; ein SDK-Wechsel koennte sie still kippen

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OBS-001.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### OBS-002

## Finding: OBS-002 — Mask Error Details: keine Stacktraces / SQL ans LLM

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OBS-002
**Katalog-Referenz:** Sec 6.2
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Laufzeitmessung 2026-09-19 (In-Process-Client, respx-gemockter Upstream, ETH_LIBRARY_API_KEY=GEHEIM-TESTKEY-123): HTTP 500 mit einem Body aus Stacktrace-Text ('Traceback (most recent call last): File "/srv/app/db.py" ... OperationalError: relation "users" does not exist') liefert im Tool-Result genau "Fehler bei Suche nach 'any,contains,x': HTTP-Fehler 500." — kein Body, kein Pfad, kein Tabellenname, kein Schluessel
- Dieselbe Messung mit einer generischen ValueError, deren Text die vollstaendige URL samt `apikey=GEHEIM-TESTKEY-123` enthaelt: Tool-Result ist "Fehler bei Suche nach 'any,contains,x': Unbekannter Fehler. Bitte spaeter erneut versuchen." — weder Exception-Klasse noch Schluessel gelangen an den LLM
- src/eth_library_mcp/formatting.py:151-153 und 158-162 — beide Maskierungsstellen sind im Code begruendet ("Upstream-Response-Body NICHT durchreichen — er kann Proxy-Errors, Stacktraces oder andere Internals enthalten" / "interne Exception-Klasse + str(e) leaken Implementations-Details an den LLM"); die Details gehen ueber `log.error("unhandled_exception", ...)` ins stderr-Log
- Gemessen: `grep -rnE 'traceback|format_exc|sys\.exc_info' src/ --include=*.py` -> ein einziger Treffer, src/eth_library_mcp/logging_config.py:37 `structlog.processors.format_exc_info` (Log-Prozessor, kein Tool-Return). Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit `traceback.format_exc()` liefert Treffer, es greift
- tests/test_tools.py:83-107 — test_search_resources_http_401_no_key_leak und test_search_resources_http_500_body_not_leaked halten beide Zusicherungen fest; die Mutationsgegenprobe (OPS-010, M3a) bestaetigt, dass der 500er-Test bei wiedereingefuehrtem Body-Leak rot wird

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OBS-002.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Laufzeitmessung 2026-09-19 (In-Process-Client, respx-gemockter Upstream, ETH_LIBRARY_API_KEY=GEHEIM-TESTKEY-123): HTTP 500 mit einem Body aus Stacktrace-Text ('Traceback (most recent call last): File "/srv/app/db.py" ... OperationalError: relation "users" does not exist') liefert im Tool-Result genau "Fehler bei Suche nach 'any,contains,x': HTTP-Fehler 500." — kein Body, kein Pfad, kein Tabellenname, kein Schluessel
- Dieselbe Messung mit einer generischen ValueError, deren Text die vollstaendige URL samt `apikey=GEHEIM-TESTKEY-123` enthaelt: Tool-Result ist "Fehler bei Suche nach 'any,contains,x': Unbekannter Fehler. Bitte spaeter erneut versuchen." — weder Exception-Klasse noch Schluessel gelangen an den LLM
- src/eth_library_mcp/formatting.py:151-153 und 158-162 — beide Maskierungsstellen sind im Code begruendet ("Upstream-Response-Body NICHT durchreichen — er kann Proxy-Errors, Stacktraces oder andere Internals enthalten" / "interne Exception-Klasse + str(e) leaken Implementations-Details an den LLM"); die Details gehen ueber `log.error("unhandled_exception", ...)` ins stderr-Log
- Gemessen: `grep -rnE 'traceback|format_exc|sys\.exc_info' src/ --include=*.py` -> ein einziger Treffer, src/eth_library_mcp/logging_config.py:37 `structlog.processors.format_exc_info` (Log-Prozessor, kein Tool-Return). Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit `traceback.format_exc()` liefert Treffer, es greift
- tests/test_tools.py:83-107 — test_search_resources_http_401_no_key_leak und test_search_resources_http_500_body_not_leaked halten beide Zusicherungen fest; die Mutationsgegenprobe (OPS-010, M3a) bestaetigt, dass der 500er-Test bei wiedereingefuehrtem Body-Leak rot wird

### Gaps

- **Der API-Key steht im Klartext im Log, bei JEDER Anfrage.** Gemessen auf dem Erfolgspfad: `configure_logging` setzt `logging.basicConfig(stream=sys.stderr, level=INFO)` (src/eth_library_mcp/logging_config.py:25-29), womit httpx' eigener INFO-Logger aktiv wird und schreibt: `HTTP Request: GET https://api.library.ethz.ch/discovery/v1/resources?q=...&apikey=GEHEIM-TESTKEY-123 "HTTP/1.1 200 OK"`. Der Schluessel wird in client.py:68 als Query-Parameter gefuehrt und landet damit in jeder Request-Zeile
- Zweiter Weg zum selben Leck: src/eth_library_mcp/formatting.py:161 loggt `exc=str(e)` woertlich. Gemessen mit einer Exception, deren Text die URL samt apikey traegt, ergab das `{"exc_type": "ValueError", "exc": "failed for https://api.library.ethz.ch/discovery/v1/resources?apikey=GEHEIM-TESTKEY-123", "event": "unhandled_exception", "level": "error"}` — httpx-Exceptions fuehren die Request-URL regelmaessig im Text
- Das Pass-Kriterium «Logs sind selbst geschuetzt: kein Klartext-Token» ist damit verletzt. SECURITY.md behauptet fuer den Schluessel «never logged» (README.md:353: "never logged or transmitted to third parties") — die Messung widerspricht dem
- Der Validierungspfad maskiert nicht: gemessen liefert ein ungueltiges Argument den vollen Pydantic-Text samt Versionsverweis "For further information visit https://errors.pydantic.dev/2.13/v/less_than_equal" an den LLM. Das ist zwar handlungsleitend (OBS-001), verraet aber die eingesetzte Pydantic-Version — eine Internale, die der Aufrufer nicht braucht
- Es gibt keinen Schalter entsprechend `mask_error_details`: die Maskierung haengt vollstaendig daran, dass jeder der sechs Handler `except Exception` faengt und `_handle_error` aufruft. Ein siebtes Werkzeug ohne diesen Block faellt auf das SDK-Verhalten zurueck, und kein Test bemerkt es (OPS-010, M3b: die generische Maskierung ist ungedeckt)

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OBS-002.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### OBS-003

## Finding: OBS-003 — Structured Logging mit RFC 5424 Severity-Stufen

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OBS-003
**Katalog-Referenz:** Sec 6.3
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- pyproject.toml:32 — `structlog>=24.0.0,<27.0.0` steht in den Laufzeit-Abhaengigkeiten (nicht im dev-Extra), der strukturierte Logger ist also im Produktivpfad
- src/eth_library_mcp/logging_config.py:31-46 — structlog-Konfiguration mit merge_contextvars, add_log_level, TimeStamper(fmt="iso", utc=True), StackInfoRenderer, format_exc_info und JSONRenderer; Ausgabeformat ist JSON
- Gemessene Ausgabe eines echten stdio-Laufs (stderr): `{"transport": "any", "event": "server_starting", "level": "info", "timestamp": "2026-09-19T17:32:12.514392Z"}` — Event-Name, Level und ISO-Zeitstempel als getrennte Felder, kein f-String
- Vier Severity-Stufen aktiv genutzt, gemessen mit `grep -rnoE 'log\.(debug|info|warning|error|critical)' src/`: debug (client.py:73), info (client.py:92,101; server.py:936), warning (server.py:919,929), error (formatting.py:161)
- src/eth_library_mcp/logging_config.py:8-12 — der Docstring benennt, welche Stufe wofuer steht (debug: Request-Dump, info: Lifecycle, warning: degradiert aber behebbar, error: unbehandelte Exception-Klassen); die Stufenwahl ist also nicht zufaellig
- src/eth_library_mcp/client.py:73 — `log.debug("upstream_request", url=url, has_key=api_key is not None)` gibt den Schluesselzustand als Boolean statt als Wert weiter; die Key-Value-Form ist durchgehalten

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OBS-003.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- pyproject.toml:32 — `structlog>=24.0.0,<27.0.0` steht in den Laufzeit-Abhaengigkeiten (nicht im dev-Extra), der strukturierte Logger ist also im Produktivpfad
- src/eth_library_mcp/logging_config.py:31-46 — structlog-Konfiguration mit merge_contextvars, add_log_level, TimeStamper(fmt="iso", utc=True), StackInfoRenderer, format_exc_info und JSONRenderer; Ausgabeformat ist JSON
- Gemessene Ausgabe eines echten stdio-Laufs (stderr): `{"transport": "any", "event": "server_starting", "level": "info", "timestamp": "2026-09-19T17:32:12.514392Z"}` — Event-Name, Level und ISO-Zeitstempel als getrennte Felder, kein f-String
- Vier Severity-Stufen aktiv genutzt, gemessen mit `grep -rnoE 'log\.(debug|info|warning|error|critical)' src/`: debug (client.py:73), info (client.py:92,101; server.py:936), warning (server.py:919,929), error (formatting.py:161)
- src/eth_library_mcp/logging_config.py:8-12 — der Docstring benennt, welche Stufe wofuer steht (debug: Request-Dump, info: Lifecycle, warning: degradiert aber behebbar, error: unbehandelte Exception-Klassen); die Stufenwahl ist also nicht zufaellig
- src/eth_library_mcp/client.py:73 — `log.debug("upstream_request", url=url, has_key=api_key is not None)` gibt den Schluesselzustand als Boolean statt als Wert weiter; die Key-Value-Form ist durchgehalten

### Gaps

- Kein gebundener Kontext pro Tool-Aufruf. Gemessen: `grep -rn '\.bind(' src/ --include='*.py'` -> 0 Treffer. Es gibt weder `tool=`, noch `session_id`, noch eine Correlation-ID an irgendeinem Log-Eintrag; ein Multi-Step-Workflow ist in den Logs nicht nachvollziehbar
- Die sechs Tool-Handler loggen ueberhaupt nicht: kein tool_invoked, kein tool_succeeded, kein tool_failed. Geloggt wird nur in client.py (Request/Lifespan) und im generischen Zweig von formatting.py:161. Ein 401 oder 429 erzeugt keinen einzigen Log-Eintrag, obwohl der Aufrufer eine Fehlermeldung bekommt
- Der stderr-Strom ist nicht durchgaengig JSON: `logging.basicConfig(format="%(message)s", stream=sys.stderr, level=INFO)` (logging_config.py:25-29) aktiviert httpx' Stdlib-Logger, der eine Klartextzeile schreibt — gemessen `HTTP Request: GET https://api.library.ethz.ch/discovery/v1/resources?...&apikey=... "HTTP/1.1 200 OK"`. Ein Log-Shipper bekommt damit JSON und Plaintext im selben Strom (und den Schluessel im Klartext, siehe OBS-002)
- `notifications/message` wird nur an einer Stelle benutzt (src/eth_library_mcp/server.py:326 u.a., `await ctx.warning(...)`), und die Messung zeigt dazu eine MCPDeprecationWarning: «The logging capability is deprecated as of 2026-07-28 (SEP-2577)». Auf der Profil-Baseline dieses Servers ist der Weg, Logs an den Client zu reichen, also abgekuendigt und nicht ersetzt

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OBS-003.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### OBS-007

## Finding: OBS-007 — Fehler-Details bleiben nach innen diagnostizierbar

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OBS-007
**Katalog-Referenz:** Custom (Portfolio-Fundstück swiss-efv-mcp#16)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/formatting.py:161 — `log.error("unhandled_exception", exc_type=type(e).__name__, exc=str(e))`: der Exception-TYP steht als eigenes Feld, nicht nur `str(e)`. Genau das verlangt das erste Pass-Kriterium, und es ueberlebt auch ein leeres `str(e)`
- Kein Retry-Pfad und kein Einpacken in eine neue Meldung: `grep -rnE 'f".*\{(exc|e|err|error|last_error)[^}]*\}' src/` -> 0 Treffer; der einzige `raise` ohne `from` ist src/eth_library_mcp/client.py:52 (`PermissionError` mit dem Hostnamen im Text, keine eingepackte Fremdexception). Negative Kontrolle: dieselben Muster gegen eine Probedatei mit `raise RuntimeError(f"x: {last_error}")` und `str(exc)` liefern 2 Treffer, sie greifen
- src/eth_library_mcp/server.py:325-326 (und analog in allen sechs Handlern) — `await ctx.warning(f"Discovery-Suche fehlgeschlagen: {type(e).__name__}")`: auch hier steht der Typ und nicht `str(e)`; die Meldung endet nicht auf einem Doppelpunkt
- Laufzeitmessung 2026-09-19 mit den drei stummen httpx-Fehlermodi (`ConnectTimeout("")`, `ReadTimeout("")`, `ConnectError("")`, je `str(exc) == ''`): kein Tool-Result endet auf `:` oder Leerzeichen — die Texte lauten "...: Zeitueberschreitung. ETH-Bibliothek API nicht erreichbar." bzw. "...: Verbindungsfehler. Internetverbindung pruefen." Der im Check beschriebene abgeschnittene Satz kommt hier nicht vor
- src/eth_library_mcp/client.py:52 — die Egress-Absage nennt das Ziel (`host {host!r}`) ohne Query-String, Header oder Token; das Pass-Kriterium «Ziel benannt, ohne Credentials» ist an dieser Stelle erfuellt

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OBS-007.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/formatting.py:161 — `log.error("unhandled_exception", exc_type=type(e).__name__, exc=str(e))`: der Exception-TYP steht als eigenes Feld, nicht nur `str(e)`. Genau das verlangt das erste Pass-Kriterium, und es ueberlebt auch ein leeres `str(e)`
- Kein Retry-Pfad und kein Einpacken in eine neue Meldung: `grep -rnE 'f".*\{(exc|e|err|error|last_error)[^}]*\}' src/` -> 0 Treffer; der einzige `raise` ohne `from` ist src/eth_library_mcp/client.py:52 (`PermissionError` mit dem Hostnamen im Text, keine eingepackte Fremdexception). Negative Kontrolle: dieselben Muster gegen eine Probedatei mit `raise RuntimeError(f"x: {last_error}")` und `str(exc)` liefern 2 Treffer, sie greifen
- src/eth_library_mcp/server.py:325-326 (und analog in allen sechs Handlern) — `await ctx.warning(f"Discovery-Suche fehlgeschlagen: {type(e).__name__}")`: auch hier steht der Typ und nicht `str(e)`; die Meldung endet nicht auf einem Doppelpunkt
- Laufzeitmessung 2026-09-19 mit den drei stummen httpx-Fehlermodi (`ConnectTimeout("")`, `ReadTimeout("")`, `ConnectError("")`, je `str(exc) == ''`): kein Tool-Result endet auf `:` oder Leerzeichen — die Texte lauten "...: Zeitueberschreitung. ETH-Bibliothek API nicht erreichbar." bzw. "...: Verbindungsfehler. Internetverbindung pruefen." Der im Check beschriebene abgeschnittene Satz kommt hier nicht vor
- src/eth_library_mcp/client.py:52 — die Egress-Absage nennt das Ziel (`host {host!r}`) ohne Query-String, Header oder Token; das Pass-Kriterium «Ziel benannt, ohne Credentials» ist an dieser Stelle erfuellt

### Gaps

- **Fuer die drei operativen Fehlermodi wird ueberhaupt nichts geloggt.** Gemessen (httpx-Eigenlogger stummgeschaltet, damit nur Server-Logs sichtbar sind): ConnectTimeout, ReadTimeout und ConnectError erzeugen null stderr-Eintraege. src/eth_library_mcp/formatting.py:154-157 kehrt fuer TimeoutException und ConnectError zurueck, BEVOR die Zeile 161 mit dem Log erreicht wird. Nach innen bleibt genau bei den Fehlern nichts uebrig, wegen derer man das Log liest
- Im Tool-Result sind ConnectTimeout und ReadTimeout nicht unterscheidbar — beide ergeben "Zeitueberschreitung. ETH-Bibliothek API nicht erreichbar.". Das ist nach aussen richtig (OBS-002), aber es gibt keine Stelle nach innen, an der der Unterschied erhalten bliebe. Verbindungsaufbau-Timeout und Lese-Timeout haben verschiedene Ursachen und verschiedene Reaktionen
- Das Ziel steht in keiner Diagnosezeile: `log.debug("upstream_request", url=url, ...)` (src/eth_library_mcp/client.py:73) liegt auf DEBUG und ist beim Default ETH_LIBRARY_LOG_LEVEL=INFO (server.py:59) aus. Im Betrieb ist damit nicht einmal festgehalten, welcher Endpunkt nicht antwortete — zu erfahren waere es nur ueber httpx' Klartextzeile, die den API-Key mitfuehrt (siehe OBS-002)
- Kein Test prueft den Meldungsinhalt fuer `str(exc) == ""`. tests/test_server.py:94-114 fuehrt zwar test_handle_error_timeout und test_handle_error_connect, benutzt dort aber `httpx.TimeoutException("timeout")` und `httpx.ConnectError("connection failed")` — also genau die Faelle MIT Message, die im Betrieb nicht auftreten. Der stumme Fall, um den es OBS-007 geht, ist ungetestet
- `raise PermissionError(...)` in src/eth_library_mcp/client.py:52 traegt kein `from`; das ist hier folgenlos (es wird keine Fremdexception eingepackt), aber der Egress-Fall erreicht ueber den generischen Zweig nur "Unbekannter Fehler" nach aussen und `exc_type=PermissionError` nach innen — die Aussage «Egress verweigert» steht nur im `exc`-Feld

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OBS-007.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### OBS-008

## Finding: OBS-008 — Der Server sagt an, dass er bedient — eine stabile Zeile auf stderr

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OBS-008
**Katalog-Referenz:** Custom (Portfolio-Erhebung 2026-08-03, 42 veröffentlichte Server)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Laufzeitmessung 2026-09-19, offener stdin (Pipe ohne Inhalt), 6 s: `PYTHONPATH=src timeout 6 python -m eth_library_mcp.server` -> exit=124 (der Server lief noch), stdout leer, auf stderr genau eine Zeile: `{"transport": "any", "event": "server_starting", "level": "info", "timestamp": "2026-09-19T17:35:18.633677Z"}`. Es gibt also eine Startzeile, sie steht auf stderr und nicht auf stdout, und sie erscheint ohne jede Anfrage
- Die Zeile stammt aus dem Code des Servers (src/eth_library_mcp/client.py:92, `log.info("server_starting", transport="any")`), nicht aus einem SDK-Banner — der von OBS-008 disqualifizierte Fall liegt hier nicht vor
- Das Marker-Feld ist invariant: `event` traegt genau `server_starting`, ohne Zeitstempel, PID, Port, Hostname oder Werkzeuganzahl. Zeitstempel und `transport` stehen als eigene Felder daneben — Regel 3 des Checks ist eingehalten
- Negative Kontrolle des Messaufbaus: ein erzwungener Fehlstart (`python -m eth_library_mcp.gibt_es_nicht`) erzeugt auf stderr `/usr/local/bin/python: No module named eth_library_mcp.gibt_es_nicht`. Der Aufbau laesst stderr also durch; ein leeres stderr waere ein Ergebnis gewesen und keine stumme Messung
- Zweite Messung mit GESCHLOSSENEM stdin (`</dev/null`): exit=0, stdout leer, stderr `server_starting` gefolgt von `server_stopping`. Der Prozess beendet sich also sauber am EOF und stirbt nicht — der im Check beschriebene zh-education-mcp-Fall (stiller Abbruch in der Initialisierung) liegt nicht vor; die Abweichung vom erwarteten exit=124 ist durch den geschlossenen Eingabekanal erklaert und durch die Gegenmessung mit offenem stdin belegt

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OBS-008.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Laufzeitmessung 2026-09-19, offener stdin (Pipe ohne Inhalt), 6 s: `PYTHONPATH=src timeout 6 python -m eth_library_mcp.server` -> exit=124 (der Server lief noch), stdout leer, auf stderr genau eine Zeile: `{"transport": "any", "event": "server_starting", "level": "info", "timestamp": "2026-09-19T17:35:18.633677Z"}`. Es gibt also eine Startzeile, sie steht auf stderr und nicht auf stdout, und sie erscheint ohne jede Anfrage
- Die Zeile stammt aus dem Code des Servers (src/eth_library_mcp/client.py:92, `log.info("server_starting", transport="any")`), nicht aus einem SDK-Banner — der von OBS-008 disqualifizierte Fall liegt hier nicht vor
- Das Marker-Feld ist invariant: `event` traegt genau `server_starting`, ohne Zeitstempel, PID, Port, Hostname oder Werkzeuganzahl. Zeitstempel und `transport` stehen als eigene Felder daneben — Regel 3 des Checks ist eingehalten
- Negative Kontrolle des Messaufbaus: ein erzwungener Fehlstart (`python -m eth_library_mcp.gibt_es_nicht`) erzeugt auf stderr `/usr/local/bin/python: No module named eth_library_mcp.gibt_es_nicht`. Der Aufbau laesst stderr also durch; ein leeres stderr waere ein Ergebnis gewesen und keine stumme Messung
- Zweite Messung mit GESCHLOSSENEM stdin (`</dev/null`): exit=0, stdout leer, stderr `server_starting` gefolgt von `server_stopping`. Der Prozess beendet sich also sauber am EOF und stirbt nicht — der im Check beschriebene zh-education-mcp-Fall (stiller Abbruch in der Initialisierung) liegt nicht vor; die Abweichung vom erwarteten exit=124 ist durch den geschlossenen Eingabekanal erklaert und durch die Gegenmessung mit offenem stdin belegt

### Gaps

- **Der Marker steht an der falschen Stelle.** src/eth_library_mcp/client.py:90-96: `log.info("server_starting", ...)` in Zeile 92 laeuft VOR `async with httpx.AsyncClient(...)` in Zeile 93 und vor der Zuweisung `_http_client = client`. Er meldet den Eintritt in den Lifespan, nicht den Bedienzustand — genau das von OBS-008 als Befund benannte Muster. Nach dem Aufbau des Clients und vor dem `yield` (client.py:98) steht keine Zeile
- Der Wortlaut sagt selbst, dass er keine Bereitschaft meldet: `server_starting` heisst startend. Ein Monitoring, das darauf greift, erfaehrt, dass der Prozess in den Lifespan eingetreten ist, nicht dass er bedient
- Der Marker ist nirgends dokumentiert. Gemessen: `grep -rniE 'marker|bereitschaft|ready|server_starting' README.md README.de.md docs/*.md` -> 0 Treffer. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit der Zeile `Bereitschaftsmarker (stderr, JSON-Feld \`event\`): \`server ready\`` liefert 1 Treffer, es greift. Ein Monitoring muesste den Wortlaut aus dem Quelltext raten, und die naechste Umformulierung braeche es ohne Aenderungsmeldung
- Kein Test haelt den Marker fest: `grep -rn 'server_starting|server_stopping|READY' tests/*.py` -> 0 Treffer in allen zehn Testdateien. Es gibt keine Zusicherung, dass ueberhaupt etwas auf stderr erscheint, und keine, dass stdout dabei leer bleibt
- `transport="any"` ist fest verdrahtet (client.py:92) und traegt keine Information: derselbe Wert erscheint fuer stdio wie fuer Streamable HTTP. Wer aus der Startzeile lesen will, welcher Transport bedient wird, bekommt keine Antwort

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OBS-008.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### OPS-001

## Finding: OPS-001 — Test-Strategie: Unit-Tests mocked + Live-Tests gemarkert

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OPS-001
**Katalog-Referenz:** Anhang C1
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- pyproject.toml:62-64 — [tool.pytest.ini_options] markers = ["live: live API tests (skipped in CI by default)"]; Marker ist registriert
- .github/workflows/ci.yml:30 — `PYTHONPATH=src pytest tests/ -m "not live"`; die CI schliesst Live-Tests aus
- .github/workflows/live-tests.yml:12-19,28,51 — separater Workflow, cron "17 6 * * *" + workflow_dispatch, `timeout-minutes: 10`, `pytest tests/ -m live --junitxml=live-report.xml`
- tests/test_tools.py:15,59,72,82,94,109,120,135,153,170,195 — `import respx` und 11 mit @respx.mock gemockte Unit-Tests gegen DISCOVERY_BASE_URL
- tests/test_server.py:262 — `@pytest.mark.live` auf class TestLiveGatewayRoutes; gemessen: `pytest -m live --collect-only` sammelt genau 2 Tests (test_discovery_route_still_exists, test_persons_route_is_still_gone), 128 deselected
- Gemessener Lauf: `PYTHONPATH=src pytest tests/ -m "not live" -q` -> 128 passed, 2 deselected, 5.19s
- .github/workflows/live-tests.yml:8-10 — Live-Tests brauchen kein Secret (Routen-Census 401/404), also keine Production-Keys im Lauf
- tests/fixtures/PROVENANCE.md + tests/fixtures/api_routes.json — aufgezeichnete Routen-Antworten mit Aufnahmedatum als Fixture-Grundlage

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OPS-001.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- pyproject.toml:62-64 — [tool.pytest.ini_options] markers = ["live: live API tests (skipped in CI by default)"]; Marker ist registriert
- .github/workflows/ci.yml:30 — `PYTHONPATH=src pytest tests/ -m "not live"`; die CI schliesst Live-Tests aus
- .github/workflows/live-tests.yml:12-19,28,51 — separater Workflow, cron "17 6 * * *" + workflow_dispatch, `timeout-minutes: 10`, `pytest tests/ -m live --junitxml=live-report.xml`
- tests/test_tools.py:15,59,72,82,94,109,120,135,153,170,195 — `import respx` und 11 mit @respx.mock gemockte Unit-Tests gegen DISCOVERY_BASE_URL
- tests/test_server.py:262 — `@pytest.mark.live` auf class TestLiveGatewayRoutes; gemessen: `pytest -m live --collect-only` sammelt genau 2 Tests (test_discovery_route_still_exists, test_persons_route_is_still_gone), 128 deselected
- Gemessener Lauf: `PYTHONPATH=src pytest tests/ -m "not live" -q` -> 128 passed, 2 deselected, 5.19s
- .github/workflows/live-tests.yml:8-10 — Live-Tests brauchen kein Secret (Routen-Census 401/404), also keine Production-Keys im Lauf
- tests/fixtures/PROVENANCE.md + tests/fixtures/api_routes.json — aufgezeichnete Routen-Antworten mit Aufnahmedatum als Fixture-Grundlage

### Gaps

- Pass-Kriterium «1 Live-Test pro Tool» nicht erfüllt: 6 Werkzeuge (eth_search_resources, eth_get_resource, eth_search_archive, eth_search_by_type, eth_search_education, eth_library_info), aber nur 2 Live-Tests, und beide prüfen nur den Statuscode der Route, kein Tool-Verhalten und kein Antwortschema
- Pass-Kriterium «5 Unit-Tests pro Tool» nicht erfüllt: tests/test_tools.py deckt eth_search_resources mit 4, eth_get_resource mit 2 und eth_search_archive / eth_search_by_type / eth_search_education / eth_library_info mit je 1 Test ab
- Es gibt weder tests/test_unit.py noch tests/test_live.py; die Live-Suite liegt als Klasse in tests/test_server.py:262 und ist dadurch aus dem Dateinamen nicht erkennbar
- Kein geteilter Client/Fixture für die Live-Suite (tests/test_server.py:277,288 legen je ein eigenes `httpx.get(..., timeout=45)` an); bei einem toten Host addieren sich die Timeouts pro Test statt einmal zu laufen
- Live-Timeout 45 s (tests/test_server.py:277,288) ist weiter als das Prod-Timeout REQUEST_TIMEOUT = 30.0 (src/eth_library_mcp/client.py:29) — das Pass-Kriterium verlangt engere Test-Timeouts als Prod
- tests/test_server.py:91-92 — test_format_resource_detail besteht nur aus einem Docstring und pruefet nichts; er laeuft in der CI mit und erscheint in der Zaehlung der 128 gruenen Tests wie Abdeckung

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OPS-001.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### OPS-002

## Finding: OPS-002 — Doku-Standard: bilingualer README, ASCII-Diagramm, Limits-Sektion

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OPS-002
**Katalog-Referenz:** Anhang C2
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- README.md:16-18 + README.de.md:16-18 — Abschnitt "### Demo" mit docs/assets/demo.svg (Alt-Text: "Claude using eth_search_archive to find historical school documents")
- README.md:224-232 — "### Example Use Cases": Tabelle mit fünf natürlich-sprachlichen Ankerfragen und dem jeweils zuständigen Werkzeug; README.de.md:225 spiegelt sie als "### Beispiel-Abfragen"
- README.md:64-100 — "## Installation" + "## Quickstart" mit copy-paste-fähigen Befehlen; README.md:399-416 zusätzlich ein generierter uvx-Block
- README.md:156-182 — "## Available Tools" mit Discovery-API-, Utilities- und Resources/Prompts-Unterabschnitten; README.md:102-155 "## Configuration" mit Env-Vars und Claude-Desktop-Config
- README.md:349-359 — "## Safety & Limits" mit sieben expliziten Limits (read-only, keine PII, Auth, Rate-Limits, Datenaktualität, ToS, keine Gewähr); README.de.md:353 identisch als "## Sicherheit & Grenzen"
- README.md:361-387 — Contributing-, Security- und License-Abschnitte mit Verweis auf CONTRIBUTING.md/.de.md, SECURITY.md/.de.md, LICENSE; alle vier Dateien existieren im Repo-Wurzelverzeichnis
- CHANGELOG.md:1-10 — Keep-a-Changelog-Header, "## [Unreleased]", Releases mit Datum (0.4.0 – 2026-09-19, 0.3.4, 0.3.0, 0.2.0, 0.1.0); Abschnitte deutsch: Hinzugefügt(3+3), Geändert(2+1), Entfernt(1), Behoben(5), Sicherheit(1), Brechende Aenderungen(2)
- CHANGELOG.md:10-14 — die Protokollrevision 2026-07-28 ist im Release-Text ausdrücklich genannt (Synergie ARCH-012)

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OPS-002.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- README.md:16-18 + README.de.md:16-18 — Abschnitt "### Demo" mit docs/assets/demo.svg (Alt-Text: "Claude using eth_search_archive to find historical school documents")
- README.md:224-232 — "### Example Use Cases": Tabelle mit fünf natürlich-sprachlichen Ankerfragen und dem jeweils zuständigen Werkzeug; README.de.md:225 spiegelt sie als "### Beispiel-Abfragen"
- README.md:64-100 — "## Installation" + "## Quickstart" mit copy-paste-fähigen Befehlen; README.md:399-416 zusätzlich ein generierter uvx-Block
- README.md:156-182 — "## Available Tools" mit Discovery-API-, Utilities- und Resources/Prompts-Unterabschnitten; README.md:102-155 "## Configuration" mit Env-Vars und Claude-Desktop-Config
- README.md:349-359 — "## Safety & Limits" mit sieben expliziten Limits (read-only, keine PII, Auth, Rate-Limits, Datenaktualität, ToS, keine Gewähr); README.de.md:353 identisch als "## Sicherheit & Grenzen"
- README.md:361-387 — Contributing-, Security- und License-Abschnitte mit Verweis auf CONTRIBUTING.md/.de.md, SECURITY.md/.de.md, LICENSE; alle vier Dateien existieren im Repo-Wurzelverzeichnis
- CHANGELOG.md:1-10 — Keep-a-Changelog-Header, "## [Unreleased]", Releases mit Datum (0.4.0 – 2026-09-19, 0.3.4, 0.3.0, 0.2.0, 0.1.0); Abschnitte deutsch: Hinzugefügt(3+3), Geändert(2+1), Entfernt(1), Behoben(5), Sicherheit(1), Brechende Aenderungen(2)
- CHANGELOG.md:10-14 — die Protokollrevision 2026-07-28 ist im Release-Text ausdrücklich genannt (Synergie ARCH-012)

### Gaps

- Kein ASCII- oder Mermaid-Architekturdiagramm. Gemessen mit `grep -n '─|│|┌|└|═|║|◄|▼|-->|=>' README.md`: 16 Treffer, alle aus dem Datei-Baum "## Project Structure" (README.md:238-256); `grep -n mermaid README.md README.de.md` findet nichts. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit Box-Zeichen liefert 2 Treffer, greift also
- Der einzige ASCII-Block (README.md:236-256, "## Project Structure") ist überdies veraltet: er nennt `server.py # FastMCP server` (FastMCP ist mit mcp 2.0 entfallen) und `tests/ └── test_server.py # Unit tests`, während tests/ zehn Testdateien enthält; client.py, formatting.py und logging_config.py fehlen ganz
- Sektions-Paritaet verletzt: README.md fuehrt eine zweite "## Installation" (README.md:400, im Block <!-- BEGIN GENERATED: install -->), die in README.de.md fehlt — gemessen `grep -cE '^## ' README.md` = 17 gegen 16 in README.de.md, diff zeigt genau diese eine ueberzaehlige Sektion
- Keine Datenfluss-Beschreibung (LLM -> Tool -> Validierung -> HTTPS -> Transformation) in Text- oder Diagrammform; "## Overview" (README.md:22) beschreibt den Zweck, nicht den Weg einer Anfrage

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OPS-002.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### OPS-003

## Finding: OPS-003 — Phasenarchitektur: Read-only First, dann Write, dann Multi-Agent

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OPS-003
**Katalog-Referenz:** Anhang C4
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/server.py:248-251,360-363,424-427,515-518,614-617,691-694 — alle sechs @mcp.tool-Deklarationen tragen annotations mit "readOnlyHint": True und "destructiveHint": False; gemessen: 6x readOnlyHint True, 6x destructiveHint False, 0x destructiveHint True
- Negative Kontrolle zum destructiveHint-Muster: dieselbe grep-Zeile gegen eine Probedatei mit '"destructiveHint": True,' liefert 1 Treffer — die Null im Repo ist also eine Messung, kein blindes Muster
- src/eth_library_mcp/client.py:55-85 — der einzige Ausgangspfad ist _http_get mit client.get(); es gibt keine POST/PUT/PATCH/DELETE-Aufrufe, also faktisch Phase 1 (Read-only-Wrapper)
- SECURITY.md:29 — "Every tool sets readOnlyHint: True; no write, mutate, or delete paths exist (ARCH)"; README.md:351 / README.de.md:355 nennen dasselbe als "Read-only" bzw. "Nur-Lesen"
- Kein Semantic Layer / keine Federation im Baum (src/ enthaelt nur server.py, client.py, formatting.py, logging_config.py, __init__.py) — der Server ist damit weder in Phase 2 noch Phase 3

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OPS-003.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/server.py:248-251,360-363,424-427,515-518,614-617,691-694 — alle sechs @mcp.tool-Deklarationen tragen annotations mit "readOnlyHint": True und "destructiveHint": False; gemessen: 6x readOnlyHint True, 6x destructiveHint False, 0x destructiveHint True
- Negative Kontrolle zum destructiveHint-Muster: dieselbe grep-Zeile gegen eine Probedatei mit '"destructiveHint": True,' liefert 1 Treffer — die Null im Repo ist also eine Messung, kein blindes Muster
- src/eth_library_mcp/client.py:55-85 — der einzige Ausgangspfad ist _http_get mit client.get(); es gibt keine POST/PUT/PATCH/DELETE-Aufrufe, also faktisch Phase 1 (Read-only-Wrapper)
- SECURITY.md:29 — "Every tool sets readOnlyHint: True; no write, mutate, or delete paths exist (ARCH)"; README.md:351 / README.de.md:355 nennen dasselbe als "Read-only" bzw. "Nur-Lesen"
- Kein Semantic Layer / keine Federation im Baum (src/ enthaelt nur server.py, client.py, formatting.py, logging_config.py, __init__.py) — der Server ist damit weder in Phase 2 noch Phase 3

### Gaps

- Die Phase ist nirgends ausdruecklich deklariert. Gemessen: `grep -rcniE 'phase\s*[123]|roadmap' README.md README.de.md docs/ARCHITECTURE.md CONTRIBUTING.md` -> je 0. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit 'Phase 1: Read-only Wrapper' liefert 2 Treffer, greift also
- docs/roadmap.md fehlt; `find . -iname '*roadmap*' -o -iname '*phase*'` (ohne .git) liefert nichts. docs/ enthaelt ARCHITECTURE.md, data-sources.md, network-egress.md, scope-minimization.md, secret-management.md und assets/ — keine Phasenplanung
- Keine dokumentierten Uebergangsvoraussetzungen Phase 1 -> 2 (Audit-Run, ISDS-Klassifikation, DSG-Verarbeitungsverzeichnis) im Repo auffindbar
- CHANGELOG.md dokumentiert keine Phasenuebergaenge (die Releases 0.1.0-0.4.0 nennen keine Phase); das ist hier folgenlos, weil nie eine Phase gewechselt wurde, macht aber die Deklaration nicht entbehrlich

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OPS-003.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### OPS-004

## Finding: OPS-004 — Gemessenes von Geschlossenem trennen; unerklärte Reste bleiben offen

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OPS-004
**Katalog-Referenz:** Custom (Portfolio-Fundstück termdat-mcp#11, Nachlauf)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- audits/2026-09-19T171257-Z-eth-library-mcp/baseline-messung.md:1-4 — der Messteil dieses Laufs nennt Messzeitpunkt, HEAD (32ac730) und Messaufbau (lokaler ASGI-Stack, kein Netz); die Beobachtungen stehen als roher Protokollmitschnitt, nicht als Deutung
- audits/2026-09-19T171257-Z-eth-library-mcp/baseline-messung.md:57-62 — eigener Abschnitt "Nicht gemessen und hier ausdruecklich nicht behauptet: ob SEC-009 an diesem Server ueberhaupt erfuellbar waere ... entscheidet die naechste Katalogfassung, nicht dieser Lauf" — genau die von OPS-004 verlangte Trennung Gemessen/Offen
- audits/2026-09-19T171257-Z-eth-library-mcp/baseline-messung.md:33-52 — zwei Fehlschluesse (HTTP 421 als DNS-Rebinding-Schutz, HTTP 400 als eigener fehlender Envelope) werden als korrigierte Annahmen festgehalten statt stillschweigend ersetzt
- audits/2026-09-19T171257-Z-eth-library-mcp/audit-meta.json:2-16 — Lauf traegt run_id, skill_version 2.3.0, catalog_hash, target_sha 32ac730 und target_dirty=false; jede Zahl dieses Laufs ist damit einem Katalog- und Repo-Stand zuordenbar
- Gemessen: `grep -nEi 'vermutlich|wahrscheinlich|duerfte|scheint|vermutet|anzunehmen|presumably|likely|appears to'` gegen audits/2026-05-28T184347-Z-eth-library-mcp/audit-report.md -> 0 Treffer. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit 'Das ist vermutlich eine Zaehldifferenz.' trifft, das Muster greift also

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OPS-004.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- audits/2026-09-19T171257-Z-eth-library-mcp/baseline-messung.md:1-4 — der Messteil dieses Laufs nennt Messzeitpunkt, HEAD (32ac730) und Messaufbau (lokaler ASGI-Stack, kein Netz); die Beobachtungen stehen als roher Protokollmitschnitt, nicht als Deutung
- audits/2026-09-19T171257-Z-eth-library-mcp/baseline-messung.md:57-62 — eigener Abschnitt "Nicht gemessen und hier ausdruecklich nicht behauptet: ob SEC-009 an diesem Server ueberhaupt erfuellbar waere ... entscheidet die naechste Katalogfassung, nicht dieser Lauf" — genau die von OPS-004 verlangte Trennung Gemessen/Offen
- audits/2026-09-19T171257-Z-eth-library-mcp/baseline-messung.md:33-52 — zwei Fehlschluesse (HTTP 421 als DNS-Rebinding-Schutz, HTTP 400 als eigener fehlender Envelope) werden als korrigierte Annahmen festgehalten statt stillschweigend ersetzt
- audits/2026-09-19T171257-Z-eth-library-mcp/audit-meta.json:2-16 — Lauf traegt run_id, skill_version 2.3.0, catalog_hash, target_sha 32ac730 und target_dirty=false; jede Zahl dieses Laufs ist damit einem Katalog- und Repo-Stand zuordenbar
- Gemessen: `grep -nEi 'vermutlich|wahrscheinlich|duerfte|scheint|vermutet|anzunehmen|presumably|likely|appears to'` gegen audits/2026-05-28T184347-Z-eth-library-mcp/audit-report.md -> 0 Treffer. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit 'Das ist vermutlich eine Zaehldifferenz.' trifft, das Muster greift also

### Gaps

- Der Report dieses Laufs existiert zum Messzeitpunkt noch nicht (audits/2026-09-19T171257-Z-eth-library-mcp/ enthaelt applicability.json, audit-meta.json, baseline-messung.md, leeres findings/ und raw/); ob er die drei Abschnitte tragen wird, ist hier nicht messbar
- Der Vorlauf-Report audits/2026-05-28T184347-Z-eth-library-mcp/audit-report.md hat die von OPS-004 geforderten Abschnitte nicht: `grep -nEi '^#+.*(Gemessen|Geschlossen|Offen|Measured|Inferred)'` -> 0 Treffer bei sieben vorhandenen H2-Ueberschriften (Executive Summary, Profil-Snapshot, Applicability, Findings-Uebersicht, Detail-Findings, Remediation-Plan, Audit-Metadata)
- Die Findings des Vorlaufs (audits/2026-05-28T142641-Z-eth-library-mcp/findings/*.md, 20 Dateien) gliedern in "Observed Behavior / Gaps / Reference" und trennen damit Beleg von Schlussfolgerung nur teilweise; ein Abschnitt fuer das Ungeklaerte fehlt ganz — bei leerem Rest ist fuer den Leser nicht unterscheidbar, ob nichts offen war oder nichts betrachtet wurde
- Der Vorlauf-Report meldet 36 pass / 0 fail / 0 partial bei 38 bewerteten Checks, ohne einen Abschnitt, der offene oder nicht verifizierbare Punkte auffuehrt; ein flaechendeckendes Gruen ohne "Offen"-Abschnitt ist genau die Konstellation, gegen die OPS-004 geschrieben ist

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OPS-004.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### OPS-005

## Finding: OPS-005 — Pipeline unterscheidet «bestanden» von «nicht gelaufen»

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OPS-005
**Katalog-Referenz:** Custom (Portfolio-Fundstück mcp-continuous-auditor#29)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- .github/workflows/ci.yml:3-7,28-30 — committeter Workflow, Trigger push und pull_request auf main, fuehrt `PYTHONPATH=src pytest tests/ -m "not live"` aus; kein .template, sondern aktiv im Repo
- .github/workflows/live-tests.yml:46-53,67-76,122-130 — der einzige continue-on-error-Schritt hat eine sichtbare Folge: PIPESTATUS[0] wird als step-output weitergereicht, scripts/classify_live_run.py ordnet das JUnit-XML ein, und der Schritt "Ergebnis durchreichen" macht den Job bei state != 'clear' mit `exit 1` rot
- .github/workflows/live-tests.yml:55-66 — der Kommentar benennt genau die drei Faelle, die der Exit-Code nicht trennt (null eingesammelt / alle uebersprungen / pytest lief nicht); die Einordnung erfolgt deshalb ueber das JUnit-XML statt ueber den Exit-Code — das ist die von OPS-005 verlangte Unterscheidung «bestanden» vs «nicht gelaufen»
- .github/workflows/ci.yml:42,45 — `ruff check src/ tests/ scripts/` und `ruff format --check src/ tests/ scripts/`: alle drei Verzeichnisse mit eigenen .py-Dateien (gemessen src 5, tests 12, scripts 4) sind abgedeckt, insbesondere scripts/ mit den Pruefskripten der uebrigen Gates
- Gemessener Lauf `PYTHONPATH=src pytest tests/ -m "not live" -q -rs`: 128 passed, 0 skipped — kein Abhaengigkeits-Skip verschwindet in der gruenen Suite
- pyproject.toml:66-72 — der [tool.ruff]-Regelsatz (line-length 100, select E/F/W/I/UP) wird von .github/workflows/ci.yml:42,45 auch tatsaechlich aufgerufen; kein Regelsatz ohne Aufruf
- Gemessen: `grep -rnE '^\s*#.*(ruff|mypy|pytest).*(deaktiviert|disabled|TODO|vorerst|ausstehend)' .github/workflows/` -> 0 Treffer, kein per Kommentar stillgelegtes Gate. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit '# ruff format vorerst deaktiviert' liefert 1 Treffer
- Gemessen mit ruff 0.16.5 (`ruff --version`, entspricht dem Pin in pyproject.toml:44): `ruff format --check src/ tests/ scripts/` -> '22 files already formatted', exit 0

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OPS-005.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- .github/workflows/ci.yml:3-7,28-30 — committeter Workflow, Trigger push und pull_request auf main, fuehrt `PYTHONPATH=src pytest tests/ -m "not live"` aus; kein .template, sondern aktiv im Repo
- .github/workflows/live-tests.yml:46-53,67-76,122-130 — der einzige continue-on-error-Schritt hat eine sichtbare Folge: PIPESTATUS[0] wird als step-output weitergereicht, scripts/classify_live_run.py ordnet das JUnit-XML ein, und der Schritt "Ergebnis durchreichen" macht den Job bei state != 'clear' mit `exit 1` rot
- .github/workflows/live-tests.yml:55-66 — der Kommentar benennt genau die drei Faelle, die der Exit-Code nicht trennt (null eingesammelt / alle uebersprungen / pytest lief nicht); die Einordnung erfolgt deshalb ueber das JUnit-XML statt ueber den Exit-Code — das ist die von OPS-005 verlangte Unterscheidung «bestanden» vs «nicht gelaufen»
- .github/workflows/ci.yml:42,45 — `ruff check src/ tests/ scripts/` und `ruff format --check src/ tests/ scripts/`: alle drei Verzeichnisse mit eigenen .py-Dateien (gemessen src 5, tests 12, scripts 4) sind abgedeckt, insbesondere scripts/ mit den Pruefskripten der uebrigen Gates
- Gemessener Lauf `PYTHONPATH=src pytest tests/ -m "not live" -q -rs`: 128 passed, 0 skipped — kein Abhaengigkeits-Skip verschwindet in der gruenen Suite
- pyproject.toml:66-72 — der [tool.ruff]-Regelsatz (line-length 100, select E/F/W/I/UP) wird von .github/workflows/ci.yml:42,45 auch tatsaechlich aufgerufen; kein Regelsatz ohne Aufruf
- Gemessen: `grep -rnE '^\s*#.*(ruff|mypy|pytest).*(deaktiviert|disabled|TODO|vorerst|ausstehend)' .github/workflows/` -> 0 Treffer, kein per Kommentar stillgelegtes Gate. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit '# ruff format vorerst deaktiviert' liefert 1 Treffer
- Gemessen mit ruff 0.16.5 (`ruff --version`, entspricht dem Pin in pyproject.toml:44): `ruff format --check src/ tests/ scripts/` -> '22 files already formatted', exit 0

### Gaps

- Kein `defaults.run.shell: bash -euo pipefail {0}` und kein `shell:`-Eintrag in irgendeinem der drei Workflows. Gemessen: `grep -n 'pipefail|shell:|defaults:' .github/workflows/*.yml` -> 0 Treffer; negative Kontrolle gegen eine Probedatei mit dem defaults-Block liefert 2 Treffer, das Muster greift also
- .github/workflows/publish.yml:74-75 — `curl -L "...mcp-publisher_....tar.gz" | tar xz mcp-publisher` ohne pipefail: scheitert curl (404 auf den latest-Asset-Namen, Netzfehler, Proxy), bestimmt `tar` den Exit-Code und der Schritt kann gruen bleiben; der naechste Schritt `./mcp-publisher login github-oidc` scheitert dann mit einer Meldung, die nach einem Auth-Problem aussieht
- scripts/check_version_sync.py ist ein portfolioweit kopiertes Pruefskript und nur unter der lokalen line-length stabil: `ruff format --check --line-length 88 scripts/` meldet scripts/check_version_sync.py:121 als umzuformatieren (exit 1), `--line-length 120` meldet scripts/record_fixtures.py:151 (exit 1), waehrend 100 (Repo-Konfiguration) und 110 bestehen. Genau die von OPS-005 Modus 3 beschriebene Lage
- Kein Workflow-Schritt erzwingt diese Format-Stabilitaet ueber mehrere line-length-Werte; der Geltungsbereich des Formatnachweises ist damit auf die eigene Konfiguration beschraenkt, wird aber wie ein allgemeiner gelesen
- `ruff format --check` laeuft nur ueber src/ tests/ scripts/ — die Live-Workflow-Shell-Bloecke (.github/workflows/live-tests.yml:83-113) sind von keinem Linter erfasst; das ist kein Python, aber der laengste ungeprüfte Codeblock des Repos

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OPS-005.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### OPS-007

## Finding: OPS-007 — Dokumentierte Befehle laufen auf den Plattformen, die das Repo behauptet

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OPS-007
**Katalog-Referenz:** Custom (Portfolio-Fundstück mcp-audit-skill#70/#71, 2026-08-02)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Gemessen: `grep -rnE '^\s*[a-z].*(&&|\|\|)' README.md README.de.md CONTRIBUTING.md CONTRIBUTING.de.md EXAMPLES.md SECURITY*.md docs/*.md` -> 0 Treffer; keine Shell-Verkettung in einem dokumentierten Befehl. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit 'pip install pre-commit && pre-commit install' liefert 1 Treffer, es greift also
- README.md:84-85 und README.de.md:84-85 — der Quickstart nennt die Windows-Variante ueberhaupt: `export ETH_LIBRARY_API_KEY=...   # macOS / Linux` mit `# $env:ETH_LIBRARY_API_KEY = "..."  # Windows (PowerShell)`; die Plattform ist also im Blick
- README.md:130-131 / README.de.md:130-131 — Claude-Desktop-Konfigurationspfade fuer macOS UND Windows (`%APPDATA%\Claude\claude_desktop_config.json`) benannt
- Die Suche deckte beide Sprachfassungen ab (README.md, README.de.md, CONTRIBUTING.md, CONTRIBUTING.de.md, SECURITY.md, SECURITY.de.md, EXAMPLES.md, docs/*.md) — der in OPS-007 beschriebene Fall, dass der Bruch in der uebersetzten Datei sitzt, ist damit mitgeprueft

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OPS-007.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Gemessen: `grep -rnE '^\s*[a-z].*(&&|\|\|)' README.md README.de.md CONTRIBUTING.md CONTRIBUTING.de.md EXAMPLES.md SECURITY*.md docs/*.md` -> 0 Treffer; keine Shell-Verkettung in einem dokumentierten Befehl. Negative Kontrolle: dasselbe Muster gegen eine Probedatei mit 'pip install pre-commit && pre-commit install' liefert 1 Treffer, es greift also
- README.md:84-85 und README.de.md:84-85 — der Quickstart nennt die Windows-Variante ueberhaupt: `export ETH_LIBRARY_API_KEY=...   # macOS / Linux` mit `# $env:ETH_LIBRARY_API_KEY = "..."  # Windows (PowerShell)`; die Plattform ist also im Blick
- README.md:130-131 / README.de.md:130-131 — Claude-Desktop-Konfigurationspfade fuer macOS UND Windows (`%APPDATA%\Claude\claude_desktop_config.json`) benannt
- Die Suche deckte beide Sprachfassungen ab (README.md, README.de.md, CONTRIBUTING.md, CONTRIBUTING.de.md, SECURITY.md, SECURITY.de.md, EXAMPLES.md, docs/*.md) — der in OPS-007 beschriebene Fall, dass der Bruch in der uebersetzten Datei sitzt, ist damit mitgeprueft

### Gaps

- Die behaupteten Plattformen stehen an keiner einzigen Stelle. Gemessen: `grep -rnE 'runs-on:|os: *\[' .github/workflows/` -> ausschliesslich `ubuntu-latest` (5 Jobs, kein Matrix-OS), waehrend README.md:85,131 Windows und README.md:130 macOS ansprechen und pyproject.toml:18-26 keinen 'Operating System'-Classifier fuehrt. Die Zusage ist aus Prosa zusammenzusuchen und wird von keinem CI-Feld gedeckt
- README.md:82-89 / README.de.md:82-89 — die PowerShell-Variante ist keine gleichrangige Fassung, sondern eine auskommentierte Zeile INNERHALB eines ```bash-Blocks. Wer den Block in PowerShell einfuegt, fuehrt `export ETH_LIBRARY_API_KEY=...` aus (dort kein gueltiger Befehl) und die `$env:`-Zeile gar nicht, weil `#` auch in PowerShell auskommentiert — genau das von OPS-007 verbotene 'Fussnote zu einem POSIX-Original'
- CONTRIBUTING.md:48 und CONTRIBUTING.de.md:48 — `PYTHONPATH=. pytest tests/ -m "not live"` benutzt das POSIX-Praefix `VAR=wert befehl`, das PowerShell nicht kennt; dasselbe bei CONTRIBUTING.md:51 / CONTRIBUTING.de.md:51 (`ETH_LIBRARY_API_KEY=dein_key pytest ...`). Ein Windows-Beitragender bekommt hier keinen Hinweis und keine zweite Fassung
- Derselbe Befehl steht ausserdem in zwei Schreibweisen im Repo: CONTRIBUTING*.md:48 `PYTHONPATH=.`, README*.md:321,325 und .github/workflows/ci.yml:30 / live-tests.yml:51 `PYTHONPATH=src`. Gemessen laeuft `PYTHONPATH=. python -m pytest tests/ -m "not live" --collect-only` zwar (128 Tests eingesammelt), aber nur weil das Paket editierbar installiert ist — ohne `pip install -e` faellt genau diese Fassung um
- CONTRIBUTING.md:54 / CONTRIBUTING.de.md:54 behaupten, die `@pytest.mark.live`-Tests brauchten einen gueltigen API-Key; .github/workflows/live-tests.yml:8-10 und README.md:324 sagen ausdruecklich das Gegenteil ("these need NO API key"). Der dokumentierte Befehl laeuft also, meldet aber eine falsche Voraussetzung

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OPS-007.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### OPS-009

## Finding: OPS-009 — Herkunft der Fixture: aufgezeichnet, nicht ausgedacht

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OPS-009
**Katalog-Referenz:** Custom (Katalog-Lücke gegen mcp-data-fidelity-skill, 2026-08-07)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- tests/fixtures/PROVENANCE.md:1-5 — "Erzeugt von `scripts/record_fixtures.py`. Nicht von Hand pflegen. Aufgezeichnet am **2026-08-08** von `api.library.ethz.ch`"; Aufnahmedatum, Quelle und erzeugendes Werkzeug stehen benannt da
- tests/fixtures/PROVENANCE.md:28-33 — je Datei Quelle (`https://api.library.ethz.ch/…`), Aufnahmedatum 2026-08-08, Auswahlregel, Groesse 1133 B und SHA-256 98b2d19e...; die Herkunft nennt den Endpunkt, nicht bloss «die API»
- tests/fixtures/api_routes.json:2 — `"recorded_at": "2026-08-08"` im Datenkopf selbst; die sechs Routeneintraege tragen je url, status und eine why-Begruendung
- scripts/record_fixtures.py:133-168 — wiederholbarer Aufnahmeweg gegen die echte Quelle, dokumentiert in README.md:327-328 und README.de.md:330-331 (`python scripts/record_fixtures.py`); tests/fixture_data.py:33-36 verweist im Fehlerfall ausdruecklich darauf
- scripts/record_fixtures.py:142-155 — drei Positivkontrollen VOR dem Schreiben: Discovery muss ohne Schluessel 401 liefern, ein erfundener Pfad muss 404 liefern, und die Personen-Route darf nicht wieder 401 antworten. Das ist die von OPS-009 verlangte Gegenprobe, im Aufzeichner statt im Test
- tests/test_server.py:262-292 — die Live-Tests halten die Aufnahme gegen die Quelle auf genau der Ebene, die der Code liest: `assert r.status_code == route_status("discovery_resources")` und `assert r.status_code == 404` fuer die Personen-Route
- tests/fixture_data.py:40-48 — der Loader wirft bei unbekanntem Namen FileNotFoundError bzw. KeyError statt ein leeres Dict zurueckzugeben; ein Tippfehler erzeugt also keinen gruenen Test ohne Pruefgegenstand
- tests/fixtures/PROVENANCE.md:39-52 — die NICHT aufgezeichneten Discovery-Payloads sind als solche gefuehrt, mit Grund (ETH_LIBRARY_API_KEY fehlt, API antwortet 401 FailedToResolveAPIKey) und mit dem Satz «Sie sind damit ausgedacht und tragen kein Datum»

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OPS-009.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- tests/fixtures/PROVENANCE.md:1-5 — "Erzeugt von `scripts/record_fixtures.py`. Nicht von Hand pflegen. Aufgezeichnet am **2026-08-08** von `api.library.ethz.ch`"; Aufnahmedatum, Quelle und erzeugendes Werkzeug stehen benannt da
- tests/fixtures/PROVENANCE.md:28-33 — je Datei Quelle (`https://api.library.ethz.ch/…`), Aufnahmedatum 2026-08-08, Auswahlregel, Groesse 1133 B und SHA-256 98b2d19e...; die Herkunft nennt den Endpunkt, nicht bloss «die API»
- tests/fixtures/api_routes.json:2 — `"recorded_at": "2026-08-08"` im Datenkopf selbst; die sechs Routeneintraege tragen je url, status und eine why-Begruendung
- scripts/record_fixtures.py:133-168 — wiederholbarer Aufnahmeweg gegen die echte Quelle, dokumentiert in README.md:327-328 und README.de.md:330-331 (`python scripts/record_fixtures.py`); tests/fixture_data.py:33-36 verweist im Fehlerfall ausdruecklich darauf
- scripts/record_fixtures.py:142-155 — drei Positivkontrollen VOR dem Schreiben: Discovery muss ohne Schluessel 401 liefern, ein erfundener Pfad muss 404 liefern, und die Personen-Route darf nicht wieder 401 antworten. Das ist die von OPS-009 verlangte Gegenprobe, im Aufzeichner statt im Test
- tests/test_server.py:262-292 — die Live-Tests halten die Aufnahme gegen die Quelle auf genau der Ebene, die der Code liest: `assert r.status_code == route_status("discovery_resources")` und `assert r.status_code == 404` fuer die Personen-Route
- tests/fixture_data.py:40-48 — der Loader wirft bei unbekanntem Namen FileNotFoundError bzw. KeyError statt ein leeres Dict zurueckzugeben; ein Tippfehler erzeugt also keinen gruenen Test ohne Pruefgegenstand
- tests/fixtures/PROVENANCE.md:39-52 — die NICHT aufgezeichneten Discovery-Payloads sind als solche gefuehrt, mit Grund (ETH_LIBRARY_API_KEY fehlt, API antwortet 401 FailedToResolveAPIKey) und mit dem Satz «Sie sind damit ausgedacht und tragen kein Datum»

### Gaps

- Der Hauptendpunkt hat keine aufgezeichnete Antwort: tests/test_tools.py:34-51 (`_discovery_doc`, `_discovery_response`) sind handgeschriebene Literale, die die Discovery-Antwortstruktur (pnx.display.title/creator/creationdate/type, pnx.addata, context.mmsid, delivery.link) BEHAUPTEN. Alle 11 respx-Tests in tests/test_tools.py laufen gegen diese Annahme; keiner kann sie widerlegen
- Damit ist das Pass-Kriterium «fuer JEDEN externen Endpunkt mindestens eine Fixture von der echten Quelle» nicht erfuellt: aufgezeichnet ist nur der Routen-Zensus (Statuscodes), nicht der Antwortkoerper von GET /discovery/v1/resources und /discovery/v1/resources/{id}
- Nur der Happy Path ist als Literal vorhanden; die Fehlerpfade (401, 404, 500) werden in tests/test_tools.py:82-133 ebenfalls ueber respx-Literale erzeugt und sind damit gleichfalls ausgedacht
- tests/test_tools.py:8-9 — der Docstring sagt «Run with `pytest -m live` for the (currently absent) live suite»; die Live-Suite existiert seit tests/test_server.py:262. Die Datei, die die ausgedachten Fixtures traegt, beschreibt den Stand vor der Aufzeichnung
- Der Abstand zwischen Aufnahmedatum (2026-08-08) und Auditdatum (2026-09-19) betraegt 42 Tage. Das ist kein Befund (die Aufnahme traegt ihr Datum), aber es gibt keinen Mechanismus, der ihn irgendwo sichtbar macht oder ab einer Schwelle meldet

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OPS-009.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### OPS-010

## Finding: OPS-010 — Gegenprobe als Abnahmekriterium — auch die Uhr und der Patch

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** OPS-010
**Katalog-Referenz:** Custom (Katalog-Lücke gegen mcp-transport-hardening-skill Regel 6, 2026-08-07)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- Gefahrene Mutationen am 2026-09-19 gegen HEAD 32ac730, in einer Kopie unter /tmp (das Repo blieb unveraendert), je Mutation `PYTHONPATH=src pytest tests/ -m "not live" -q`. Ausgangslage: 128 passed. M5 (Positivkontrolle der Methode): configured_origins() gibt wieder `["*"]` zurueck (src/eth_library_mcp/server.py:845-847) -> 6 failed (test_cors.py 4x, test_transport_security.py 2x). Die Mutationsmethode schlaegt also an
- M3a: src/eth_library_mcp/formatting.py:153 `return f"{prefix}HTTP-Fehler {status}."` -> `... {status}: {e.response.text[:200]}"` -> 1 failed: tests/test_tools.py::test_search_resources_http_500_body_not_leaked. Diese Zusicherung ist gedeckt
- Kein Test patcht ein fremdes Modul global. Gemessen: `grep -rcE 'monkeypatch\.setattr\(\s*[A-Za-z_.]+\.(asyncio|time|random|os|httpx)\s*,' tests/*.py` -> 0 in allen 10 Dateien; negative Kontrolle mit der Zeile `monkeypatch.setattr(modul.asyncio, "sleep", _instant)` liefert 1 Treffer, das Muster greift. Der einzige setattr-Treffer, tests/test_tools.py:200, faellt auf einen EIGENEN Namen (`server.DISCOVERY_BASE_URL`)
- Keine Fake-Uhr im Repo: `grep -rnE 'freeze_time|time_machine|FakeClock|autojump' tests/` -> 0; `time.monotonic()` kommt nur in tests/test_session_start_hook.py:237-239 vor und misst dort echte Zeit. Die Untervariante (a) kann hier nicht zuschlagen
- Die Negativkontroll-Praxis ist im Testcode sichtbar und benannt: tests/test_cache_hints.py:69, tests/test_cors.py:94,183,220, tests/test_server.py:233-247, tests/test_server_identity.py:200-212,250, tests/test_transport_security.py:79,103 — je mit Begruendung, was ohne die Kontrolle nicht belegt waere

### Expected Behavior

Die Pass-Kriterien stehen in `checks/OPS-010.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Gefahrene Mutationen am 2026-09-19 gegen HEAD 32ac730, in einer Kopie unter /tmp (das Repo blieb unveraendert), je Mutation `PYTHONPATH=src pytest tests/ -m "not live" -q`. Ausgangslage: 128 passed. M5 (Positivkontrolle der Methode): configured_origins() gibt wieder `["*"]` zurueck (src/eth_library_mcp/server.py:845-847) -> 6 failed (test_cors.py 4x, test_transport_security.py 2x). Die Mutationsmethode schlaegt also an
- M3a: src/eth_library_mcp/formatting.py:153 `return f"{prefix}HTTP-Fehler {status}."` -> `... {status}: {e.response.text[:200]}"` -> 1 failed: tests/test_tools.py::test_search_resources_http_500_body_not_leaked. Diese Zusicherung ist gedeckt
- Kein Test patcht ein fremdes Modul global. Gemessen: `grep -rcE 'monkeypatch\.setattr\(\s*[A-Za-z_.]+\.(asyncio|time|random|os|httpx)\s*,' tests/*.py` -> 0 in allen 10 Dateien; negative Kontrolle mit der Zeile `monkeypatch.setattr(modul.asyncio, "sleep", _instant)` liefert 1 Treffer, das Muster greift. Der einzige setattr-Treffer, tests/test_tools.py:200, faellt auf einen EIGENEN Namen (`server.DISCOVERY_BASE_URL`)
- Keine Fake-Uhr im Repo: `grep -rnE 'freeze_time|time_machine|FakeClock|autojump' tests/` -> 0; `time.monotonic()` kommt nur in tests/test_session_start_hook.py:237-239 vor und misst dort echte Zeit. Die Untervariante (a) kann hier nicht zuschlagen
- Die Negativkontroll-Praxis ist im Testcode sichtbar und benannt: tests/test_cache_hints.py:69, tests/test_cors.py:94,183,220, tests/test_server.py:233-247, tests/test_server_identity.py:200-212,250, tests/test_transport_security.py:79,103 — je mit Begruendung, was ohne die Kontrolle nicht belegt waere

### Gaps

- M1 (ungedeckt): src/eth_library_mcp/client.py:51-52 — `raise PermissionError(f"Egress denied: ...")` durch `return` ersetzt -> 128 passed, 0 failed. Der einzige zugehoerige Test, tests/test_tools.py:195-201, akzeptiert `"Unbekannter Fehler" in out or "Egress denied" in out`; ohne die Egress-Pruefung laeuft die Anfrage in respx' AllMockedAssertionError und erzeugt genau "Unbekannter Fehler". Der Test kann die Zusicherung nicht widerlegen
- M2 (ungedeckt): src/eth_library_mcp/server.py:250 `"readOnlyHint": True,` aus eth_search_resources geloescht -> 128 passed. Kein Test haelt die Tool-Annotationen (ARCH-009, Grundlage der Phase-1-Aussage aus OPS-003) fest
- M3b (ungedeckt): src/eth_library_mcp/formatting.py:162 `return f"{prefix}Unbekannter Fehler. Bitte spaeter erneut versuchen."` -> `return f"{prefix}{type(e).__name__}: {e}"` -> 128 passed. Der generische Zweig von _handle_error ist der Zweig, der Exception-Klassennamen und interne Fehlertexte an den LLM gaebe, und er ist ungeprueft — waehrend der HTTP-Status-Zweig daneben (M3a) gedeckt ist
- M4 (ungedeckt): src/eth_library_mcp/formatting.py:105-107 — das Anhaengen von SOURCE_ATTRIBUTION (CH-004-Quellenangabe je Datensatz) entfernt -> 128 passed. Die Quellenangabe kann still verschwinden
- Bilanz der gefahrenen Mutationen: 2 von 6 schlagen an, 4 nicht. Die vier ungedeckten Zusicherungen sind Egress-Allow-List, Tool-Annotationen, generische Fehlermaskierung und Quellenangabe — alle vier tragen anderswo im Katalog eigene Checks
- Kein Pass-Kriterium der Dokumentationsseite ist erfuellt: nirgends im Repo steht, welcher Test bei welcher gebrochenen Zusicherung rot wird; es gibt keinen datierten Nachweis eines gefahrenen Mutationslaufs; die nicht anschlagenden Mutationen sind nirgends als Befund festgehalten
- `grep -cniE 'gegenprobe|gegenkontrolle|mutation' CONTRIBUTING.md CONTRIBUTING.de.md` -> je 0: der Weg, eine Gegenprobe zu fahren, steht nicht im CONTRIBUTING. CLAUDE.md (Abschnitt «Tests») verlangt ihn zwar («Jede neue Zusicherung einzeln neutralisieren und zeigen, dass genau die zugehoerigen Tests fallen»), aber CLAUDE.md ist die Agenten-Anweisung, nicht die Beitragsanleitung
- tests/test_server.py:91-92 — `def test_format_resource_detail():` hat ausser dem Docstring KEINEN Koerper: der Test kann nicht fallen und zaehlt trotzdem als einer der 128 gruenen. Per AST ueber alle 10 Testdateien gemessen, er ist der einzige seiner Art (die 19 unittest-Tests in tests/test_classify_live_run.py nutzen self.assertEqual und sind keine Fundstellen — belegt durch die Mutation oben, die einen von ihnen rot bekam)

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/OPS-010.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SCALE-009

## Finding: SCALE-009 — Legacy HTTP+SSE abgeschaltet — mit Datum, nicht mit Vorsatz

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SCALE-009
**Katalog-Referenz:** SEP-2596
**Spec-Baseline:** beide
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Kein Legacy-Pfad im Code: `grep -rnE 'sse_app|SseServerTransport|/sse|text/event-stream|EventSourceResponse' src/ --include='*.py'` liefert 0 Treffer. Negative Kontrolle: dasselbe Muster gegen das installierte SDK findet mcp/server/sse.py und mcp/server/mcpserver/server.py — es greift also
- GEMESSEN an der zusammengebauten App: `build_http_app().routes` enthaelt genau eine Route, `('/mcp', [])`. Kein zweiter Transportpfad
- GEMESSEN am laufenden Stack: `GET /sse` mit `Accept: text/event-stream` -> HTTP 404; `POST /sse` mit vollstaendigem modernen Envelope -> HTTP 404
- GEGENPROBE gefuehrt (vom Check ausdruecklich verlangt): derselbe Aufruf gegen einen Server MIT offenem SSE-Pfad — `MCPServer('probe').sse_app()` hat die Routen `['/sse', '/messages']`, und `GET /sse` bleibt dort als langlebiger text/event-stream-Strom offen statt 404 zu liefern. Die 404 oben ist damit eine Messung und kein Tippfehler in der URL
- Deployment-Konfiguration ohne Legacy-Route: Dockerfile ENTRYPOINT/CMD ist `python -m eth_library_mcp.server --http --host 0.0.0.0 --port 8000`, server.json:15-18 deklariert `"transport": {"type": "stdio"}`, claude_desktop_config.json startet stdio. Es gibt keine Ingress-/Compose-Datei mit einer /sse-Route (`find . -name 'docker-compose*' -o -name 'ingress*'` leer)
- BEFUND README.md:53 und README.de.md:53 — «Dual transport – stdio for Claude Desktop, Streamable HTTP/SSE for cloud deployment». Dazu README.md:133 und README.de.md:133 als eigener Abschnitt «Cloud Deployment (SSE for browser access)» bzw. «Cloud-Deployment (SSE fuer Browser-Zugriff)». Das README fuehrt SSE als gleichwertigen ausgelieferten Transport, obwohl gemessen keiner existiert

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SCALE-009.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Kein Legacy-Pfad im Code: `grep -rnE 'sse_app|SseServerTransport|/sse|text/event-stream|EventSourceResponse' src/ --include='*.py'` liefert 0 Treffer. Negative Kontrolle: dasselbe Muster gegen das installierte SDK findet mcp/server/sse.py und mcp/server/mcpserver/server.py — es greift also
- GEMESSEN an der zusammengebauten App: `build_http_app().routes` enthaelt genau eine Route, `('/mcp', [])`. Kein zweiter Transportpfad
- GEMESSEN am laufenden Stack: `GET /sse` mit `Accept: text/event-stream` -> HTTP 404; `POST /sse` mit vollstaendigem modernen Envelope -> HTTP 404
- GEGENPROBE gefuehrt (vom Check ausdruecklich verlangt): derselbe Aufruf gegen einen Server MIT offenem SSE-Pfad — `MCPServer('probe').sse_app()` hat die Routen `['/sse', '/messages']`, und `GET /sse` bleibt dort als langlebiger text/event-stream-Strom offen statt 404 zu liefern. Die 404 oben ist damit eine Messung und kein Tippfehler in der URL
- Deployment-Konfiguration ohne Legacy-Route: Dockerfile ENTRYPOINT/CMD ist `python -m eth_library_mcp.server --http --host 0.0.0.0 --port 8000`, server.json:15-18 deklariert `"transport": {"type": "stdio"}`, claude_desktop_config.json startet stdio. Es gibt keine Ingress-/Compose-Datei mit einer /sse-Route (`find . -name 'docker-compose*' -o -name 'ingress*'` leer)
- BEFUND README.md:53 und README.de.md:53 — «Dual transport – stdio for Claude Desktop, Streamable HTTP/SSE for cloud deployment». Dazu README.md:133 und README.de.md:133 als eigener Abschnitt «Cloud Deployment (SSE for browser access)» bzw. «Cloud-Deployment (SSE fuer Browser-Zugriff)». Das README fuehrt SSE als gleichwertigen ausgelieferten Transport, obwohl gemessen keiner existiert

### Gaps

- Das README nennt SSE als unterstuetzten Transport (4 Stellen in beiden Sprachfassungen). Wer danach deployt, sucht einen Endpunkt, den es nicht gibt — und wer den Check spaeter wiederholt, liest die Doku als Beleg fuer einen offenen Legacy-Pfad, den der Code nicht hat. Der Abschnittstitel «Cloud Deployment (SSE …)» beschreibt tatsaechlich Streamable HTTP
- Kein Abschaltdatum im CHANGELOG — hier folgerichtig, weil nichts offen ist, aber damit auch kein Nachweis, wann der Pfad geschlossen wurde
- Gemessen wurde am lokal zusammengebauten ASGI-Stack; eine ausgelieferte HTTP-Instanz existiert nicht (Deployment local-stdio), der Punkt «an der ausgelieferten Instanz geprueft» ist damit so weit erfuellt, wie er hier erfuellbar ist

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SCALE-009.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SCALE-010

## Finding: SCALE-010 — subscriptions/listen statt GET-Endpunkt und resources/subscribe

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SCALE-010
**Katalog-Referenz:** SEP-2575
**Spec-Baseline:** 2026-07-28
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Kein alter Abonnementmechanismus im Code: `grep -rnE 'resources/(un)?subscribe|resource_subscribe|handle_get' src/ --include='*.py'` liefert 0 Treffer; ebenso 0 fuer die neuen Bezeichner `subscriptions/listen|subscriptionId|toolsListChanged|resourcesListChanged`. Negative Kontrolle: dasselbe Muster gegen das SDK liefert Treffer (u. a. mcp/server/connection.py) — das Muster greift
- GEMESSEN am `initialize`-Resultat durch build_http_app(): `capabilities = {"experimental": {}, "prompts": {"listChanged": false}, "resources": {"listChanged": false, "subscribe": false}, "tools": {"listChanged": false}}`. Der Server erklaert maschinenlesbar, dass er weder Aenderungsbenachrichtigungen noch Ressourcen-Abonnements fuehrt — das ist staerker als ein Satz Prosa, aber es steht nirgends auch in der Doku
- Request-bezogene Benachrichtigungen bleiben, wo sie hingehoeren: src/eth_library_mcp/server.py:289 ruft `ctx.report_progress(0, params.limit, 'Suche laeuft')`. GEMESSEN durch einen echten tools/call (limit=60): `Context.report_progress` wurde mit `(0, 60, 'Suche laeuft')` aufgerufen. Nichts davon laeuft ueber einen Abonnementstrom; `grep -rn 'subscriptions/listen' src/` ist leer
- BEFUND, gemessen: `GET /mcp` wird weiterhin bedient. Ohne Session-ID antwortet der Server HTTP 400 `{"code": -32600, "message": "Bad Request: Missing session ID"}`; MIT gueltiger `Mcp-Session-Id` (aus einem `initialize`) bleibt die Anfrage nach 5 s ohne Antwort offen — der serverinitiierte Strom ist da. Der vom Check verlangte 405 kommt in keinem der beiden Faelle
- src/eth_library_mcp/server.py:829 — `CORS_ALLOW_METHODS = ["GET", "POST", "DELETE", "OPTIONS"]`. Der GET-Pfad ist nicht bloss ein SDK-Rest, er ist am Endpunkt ausdruecklich freigegeben. Zur Gegenkontrolle mitgemessen: `DELETE /mcp` mit Session-ID -> HTTP 200, die Freigabeliste wirkt also

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SCALE-010.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Kein alter Abonnementmechanismus im Code: `grep -rnE 'resources/(un)?subscribe|resource_subscribe|handle_get' src/ --include='*.py'` liefert 0 Treffer; ebenso 0 fuer die neuen Bezeichner `subscriptions/listen|subscriptionId|toolsListChanged|resourcesListChanged`. Negative Kontrolle: dasselbe Muster gegen das SDK liefert Treffer (u. a. mcp/server/connection.py) — das Muster greift
- GEMESSEN am `initialize`-Resultat durch build_http_app(): `capabilities = {"experimental": {}, "prompts": {"listChanged": false}, "resources": {"listChanged": false, "subscribe": false}, "tools": {"listChanged": false}}`. Der Server erklaert maschinenlesbar, dass er weder Aenderungsbenachrichtigungen noch Ressourcen-Abonnements fuehrt — das ist staerker als ein Satz Prosa, aber es steht nirgends auch in der Doku
- Request-bezogene Benachrichtigungen bleiben, wo sie hingehoeren: src/eth_library_mcp/server.py:289 ruft `ctx.report_progress(0, params.limit, 'Suche laeuft')`. GEMESSEN durch einen echten tools/call (limit=60): `Context.report_progress` wurde mit `(0, 60, 'Suche laeuft')` aufgerufen. Nichts davon laeuft ueber einen Abonnementstrom; `grep -rn 'subscriptions/listen' src/` ist leer
- BEFUND, gemessen: `GET /mcp` wird weiterhin bedient. Ohne Session-ID antwortet der Server HTTP 400 `{"code": -32600, "message": "Bad Request: Missing session ID"}`; MIT gueltiger `Mcp-Session-Id` (aus einem `initialize`) bleibt die Anfrage nach 5 s ohne Antwort offen — der serverinitiierte Strom ist da. Der vom Check verlangte 405 kommt in keinem der beiden Faelle
- src/eth_library_mcp/server.py:829 — `CORS_ALLOW_METHODS = ["GET", "POST", "DELETE", "OPTIONS"]`. Der GET-Pfad ist nicht bloss ein SDK-Rest, er ist am Endpunkt ausdruecklich freigegeben. Zur Gegenkontrolle mitgemessen: `DELETE /mcp` mit Session-ID -> HTTP 200, die Freigabeliste wirkt also

### Gaps

- Ein GET auf /mcp antwortet nicht mit 405: mit gueltiger Session-ID oeffnet sich der serverinitiierte Strom, den Spec 2026-07-28 (SEP-2575) gestrichen hat. Ursache ist das SDK bzw. der bewusst weiterbediente Legacy-Handshake beider Epochen — der Befund bleibt, weil der Server auf der 2026-07-28-Baseline gefuehrt wird
- Weder README noch CONTRIBUTING sagen mit einem Satz, dass dieser Server keine Aenderungsbenachrichtigungen fuehrt. Belegt ist es nur ueber die `capabilities` im Handshake — wer die Doku liest, erfaehrt es nicht
- Kein Test, der festhaelt, dass `notifications/progress` auf dem Antwortstrom seines Requests laeuft und nicht anderswo; die Messung stammt aus diesem Audit, nicht aus der Suite
- `ctx.report_progress` wird nur ein einziges Mal mit progress=0 aufgerufen und nie fortgeschrieben — gemessen kam im Antwortstrom kein `notifications/progress` an (der Client hatte keinen progressToken gesetzt). Der Fortschrittspfad ist damit vorhanden, aber unbelegt in Betrieb

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SCALE-010.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### SDK-002

## Finding: SDK-002 — Pydantic v2 / TypedDict / Dataclass als Tool-Returns

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SDK-002
**Katalog-Referenz:** Sec 3.1
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Pydantic v2 gedeckelt und installiert: pyproject.toml:31 `pydantic>=2.0.0,<3.0.0`; gemessen `importlib.metadata.version('pydantic')` -> 2.13.5. Keine v1-Syntax: `grep -rn 'parse_obj|class Config' src/` liefert 0 Treffer
- Alle sechs Werkzeuge tragen eine EXPLIZITE Return-Annotation — server.py:259 `-> str` (eth_search_resources), :371 (eth_get_resource), :435 (eth_search_archive), :526 (eth_search_by_type), :625 (eth_search_education), :699 (eth_library_info). Keines ist unannotiert; auch die Resources (:763, :769) und Prompts (:780, :794) sind annotiert
- Eingaben sind durchgaengig Pydantic-v2-Modelle mit `ConfigDict(str_strip_whitespace=True, extra='forbid')` und Literal-Typen statt `str`: SortOption (server.py:65), ResourceType (:67), ArchiveKey (:80). Defaults ueber `Field(default=...)`. Kein mutable Default in einem Feld: `grep -rn '= \[\]' src/` liefert drei Treffer (formatting.py:69, server.py:277, :630), alle drei sind lokale Variablen in Funktionskoerpern, kein Feld-Default. Keine v1-Syntax: `grep -rnE 'parse_obj|class Config' src/` -> 0
- BEFUND, gemessen am `tools/list`-Resultat durch build_http_app(): jedes Werkzeug meldet `outputSchema: {"properties": {"result": {"title": "Result", "type": "string"}}, "required": ["result"], ...}`. Das SDK umhuellt einen nackten String — das Manifest sagt dem Modell nur «es kommt Text», nicht welche Felder
- BEFUND: kein Response-Envelope. `grep -rE '"source"|"license"|"provenance"|"count"' src/` liefert 0 Treffer; die Quellenangabe ist eine Markdown-Zeile am Ende des Texts (formatting.py:20, angehaengt in server.py:321, 472, 568, 676 und formatting.py:107). Gegenkontrolle: dasselbe Muster findet in einem Probetext mit `"source": "x"` einen Treffer
- Die Entscheidung ist begruendet dokumentiert — docs/ARCHITECTURE.md:67: «FastMCP's structured-output path is still maturing; Markdown remains …». Die Begruendung steht, ist aber an FastMCP gebunden und damit seit der SDK-2.x-Migration ueberholt (siehe DRIFT-006)

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SDK-002.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Pydantic v2 gedeckelt und installiert: pyproject.toml:31 `pydantic>=2.0.0,<3.0.0`; gemessen `importlib.metadata.version('pydantic')` -> 2.13.5. Keine v1-Syntax: `grep -rn 'parse_obj|class Config' src/` liefert 0 Treffer
- Alle sechs Werkzeuge tragen eine EXPLIZITE Return-Annotation — server.py:259 `-> str` (eth_search_resources), :371 (eth_get_resource), :435 (eth_search_archive), :526 (eth_search_by_type), :625 (eth_search_education), :699 (eth_library_info). Keines ist unannotiert; auch die Resources (:763, :769) und Prompts (:780, :794) sind annotiert
- Eingaben sind durchgaengig Pydantic-v2-Modelle mit `ConfigDict(str_strip_whitespace=True, extra='forbid')` und Literal-Typen statt `str`: SortOption (server.py:65), ResourceType (:67), ArchiveKey (:80). Defaults ueber `Field(default=...)`. Kein mutable Default in einem Feld: `grep -rn '= \[\]' src/` liefert drei Treffer (formatting.py:69, server.py:277, :630), alle drei sind lokale Variablen in Funktionskoerpern, kein Feld-Default. Keine v1-Syntax: `grep -rnE 'parse_obj|class Config' src/` -> 0
- BEFUND, gemessen am `tools/list`-Resultat durch build_http_app(): jedes Werkzeug meldet `outputSchema: {"properties": {"result": {"title": "Result", "type": "string"}}, "required": ["result"], ...}`. Das SDK umhuellt einen nackten String — das Manifest sagt dem Modell nur «es kommt Text», nicht welche Felder
- BEFUND: kein Response-Envelope. `grep -rE '"source"|"license"|"provenance"|"count"' src/` liefert 0 Treffer; die Quellenangabe ist eine Markdown-Zeile am Ende des Texts (formatting.py:20, angehaengt in server.py:321, 472, 568, 676 und formatting.py:107). Gegenkontrolle: dasselbe Muster findet in einem Probetext mit `"source": "x"` einen Treffer
- Die Entscheidung ist begruendet dokumentiert — docs/ARCHITECTURE.md:67: «FastMCP's structured-output path is still maturing; Markdown remains …». Die Begruendung steht, ist aber an FastMCP gebunden und damit seit der SDK-2.x-Migration ueberholt (siehe DRIFT-006)

### Gaps

- Such- und Listenwerkzeuge liefern Markdown-Strings statt eines konsistenten Envelopes mit `source`, `provenance`, `results`, `count`. Ein Konsument kann Treffer nicht von Fehlermeldung unterscheiden, ohne den Text zu lesen — dasselbe Loch, das DRIFT-003 auf der Testseite trifft
- Kein BaseModel/TypedDict/Dataclass als Return-Typ; das exponierte outputSchema ist `{result: string}` und traegt keine Feldinformation
- Die Begruendung in docs/ARCHITECTURE.md:67 beruft sich auf FastMCP, das es unter mcp 2.x nicht mehr gibt — die Entscheidung ist damit gegen einen Zustand begruendet, der nicht mehr besteht, und gehoert neu gefasst
- Kein Provenance-Feld je Datensatz (siehe CH-004): die Quellenzeile steht einmal je Antwort, nicht je Treffer

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SDK-002.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### SDK-003

## Finding: SDK-003 — Context Injection für Progress Reports und Logging

**Severity:** medium
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SDK-003
**Katalog-Referenz:** Sec 3.1
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Context-Parameter auf allen fuenf netzberuehrenden Werkzeugen: server.py:244, 370, 431, 527, 629 jeweils `ctx: Context | None = None`. `eth_library_info` (server.py:699) hat keinen — korrekt, es ruft nichts ab (openWorldHint=False)
- GEMESSEN, dass der Context wirklich injiziert wird und der Code kein toter Zweig ist: bei einem echten `tools/call` durch build_http_app() (limit=60, Upstream auf 503 gesetzt) wurde `Context.report_progress` mit `(0, 60, 'Suche laeuft')` aufgerufen und `Context.warning` mit `'Discovery-Suche fehlgeschlagen: HTTPStatusError'`
- Fehlerfaelle werden nicht stumm geschluckt: server.py:326, 386, 476, 575, 680 rufen je `await ctx.warning(f'... fehlgeschlagen: {type(e).__name__}')`, bevor `_handle_error` die Nutzerantwort baut
- Kein stdout-Bruch fuer stdio: `grep -rn 'print(' src/` liefert 0 Treffer; logging_config.py schreibt strukturiertes JSON auf stderr (docs/ARCHITECTURE.md:77 «All output goes to stderr (mandatory for stdio transport …)»)
- Baseline 2026-07-28, Teil 1 erfuellt: `grep -rn 'setLevel|logLevel|set_level' src/` liefert 0 Treffer — es gibt keinen `logging/setLevel`-Handler mehr, also auch keinen toten Code, der eine Faehigkeit vortaeuscht. Gegenkontrolle: dasselbe Muster findet im SDK Treffer
- Baseline 2026-07-28, Teil 2 gemessen (aber nicht im Repo belegt): ein `tools/call` OHNE `io.modelcontextprotocol/logLevel` im `_meta`, dessen Werkzeug `ctx.warning()` ausloest, liefert eine Antwort, die kein `notifications/message` enthaelt — das SDK unterdrueckt es. Das Verhalten stimmt; der vom Check verlangte Test dazu fehlt

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SDK-003.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Context-Parameter auf allen fuenf netzberuehrenden Werkzeugen: server.py:244, 370, 431, 527, 629 jeweils `ctx: Context | None = None`. `eth_library_info` (server.py:699) hat keinen — korrekt, es ruft nichts ab (openWorldHint=False)
- GEMESSEN, dass der Context wirklich injiziert wird und der Code kein toter Zweig ist: bei einem echten `tools/call` durch build_http_app() (limit=60, Upstream auf 503 gesetzt) wurde `Context.report_progress` mit `(0, 60, 'Suche laeuft')` aufgerufen und `Context.warning` mit `'Discovery-Suche fehlgeschlagen: HTTPStatusError'`
- Fehlerfaelle werden nicht stumm geschluckt: server.py:326, 386, 476, 575, 680 rufen je `await ctx.warning(f'... fehlgeschlagen: {type(e).__name__}')`, bevor `_handle_error` die Nutzerantwort baut
- Kein stdout-Bruch fuer stdio: `grep -rn 'print(' src/` liefert 0 Treffer; logging_config.py schreibt strukturiertes JSON auf stderr (docs/ARCHITECTURE.md:77 «All output goes to stderr (mandatory for stdio transport …)»)
- Baseline 2026-07-28, Teil 1 erfuellt: `grep -rn 'setLevel|logLevel|set_level' src/` liefert 0 Treffer — es gibt keinen `logging/setLevel`-Handler mehr, also auch keinen toten Code, der eine Faehigkeit vortaeuscht. Gegenkontrolle: dasselbe Muster findet im SDK Treffer
- Baseline 2026-07-28, Teil 2 gemessen (aber nicht im Repo belegt): ein `tools/call` OHNE `io.modelcontextprotocol/logLevel` im `_meta`, dessen Werkzeug `ctx.warning()` ausloest, liefert eine Antwort, die kein `notifications/message` enthaelt — das SDK unterdrueckt es. Das Verhalten stimmt; der vom Check verlangte Test dazu fehlt

### Gaps

- Der Check verlangt ausdruecklich einen Test, «der einen Request OHNE das logLevel-Feld stellt und prueft, dass keine Meldung kommt». Den gibt es nicht: `grep -rn 'notifications/message|logLevel' tests/` liefert 0 Treffer. Die Zusicherung haengt allein am SDK-Verhalten, das dieses Audit gemessen hat
- Kein Datum fuer den Ausstieg aus dem deprecateten Logging-Feature (ARCH-019): weder CHANGELOG noch README noch docs/ nennen eines. Der Zielzustand stderr ist faktisch schon da (logging_config.py), aber die Migration ist nirgends terminiert
- `ctx.report_progress` wird genau einmal und nur mit progress=0 aufgerufen (server.py:288-289, nur bei limit>50); es gibt keine Fortschreibung und keine Abschlussmeldung. Fuer einen einzelnen Upstream-Aufruf vertretbar, aber der Aufruf informiert den Client ueber nichts
- Kein Test deckt den ctx-Pfad ab: tests/test_tools.py ruft alle Werkzeuge ohne `ctx` auf (Default None), sodass report_progress/warning in der Suite nie laufen

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `medium`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SDK-003.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

S (< 1d) — Schaetzung nach Severity, nicht gemessen.


### SEC-003

## Finding: SEC-003 — Progressive Scope-Minimierung: Least-Privilege-Modell

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SEC-003
**Katalog-Referenz:** Sec 4.3
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- docs/scope-minimization.md:1-32 — Kriterium 1 in der fuer dieses Auth-Modell moeglichen Form: der einzige Credential (`ETH_LIBRARY_API_KEY`) ist mit Operation und Privileg tabelliert (discovery/v1/resources, search+read, read-only), plus dokumentierter Weg fuer einen kuenftigen Split. Kein Omnibus-Scope, weil die Upstream-API keine Scopes fuehrt
- LAUFZEITMESSUNG zu Kriterium 7 (ungueltige Origin -> 403, nicht 400): mit `ETH_LIBRARY_CORS_ORIGINS=https://client.example` gegen `build_http_app('127.0.0.1', 8000)` ein echtes `initialize` gepostet. Erlaubte Origin -> HTTP 200, `https://woanders.example` -> HTTP 403. Das Paar schliesst aus, dass der Transport pauschal abweist
- src/eth_library_mcp/server.py:168-187 — `MCPServer(...)` ohne `auth=`: der Server validiert keine eingehenden Tokens, es gibt also keinen Ort, an dem pro Tool-Call ein Scope geprueft werden koennte. grep -rniE 'scope' src/ findet nur `cacheScope`/`scope="public"` aus den Cache-Hints (server.py:140-144), keinen Autorisierungs-Scope. NEGATIVE KONTROLLE: dasselbe Muster findet in docs/scope-minimization.md die Scope-Dokumentation, greift also

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SEC-003.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- docs/scope-minimization.md:1-32 — Kriterium 1 in der fuer dieses Auth-Modell moeglichen Form: der einzige Credential (`ETH_LIBRARY_API_KEY`) ist mit Operation und Privileg tabelliert (discovery/v1/resources, search+read, read-only), plus dokumentierter Weg fuer einen kuenftigen Split. Kein Omnibus-Scope, weil die Upstream-API keine Scopes fuehrt
- LAUFZEITMESSUNG zu Kriterium 7 (ungueltige Origin -> 403, nicht 400): mit `ETH_LIBRARY_CORS_ORIGINS=https://client.example` gegen `build_http_app('127.0.0.1', 8000)` ein echtes `initialize` gepostet. Erlaubte Origin -> HTTP 200, `https://woanders.example` -> HTTP 403. Das Paar schliesst aus, dass der Transport pauschal abweist
- src/eth_library_mcp/server.py:168-187 — `MCPServer(...)` ohne `auth=`: der Server validiert keine eingehenden Tokens, es gibt also keinen Ort, an dem pro Tool-Call ein Scope geprueft werden koennte. grep -rniE 'scope' src/ findet nur `cacheScope`/`scope="public"` aus den Cache-Hints (server.py:140-144), keinen Autorisierungs-Scope. NEGATIVE KONTROLLE: dasselbe Muster findet in docs/scope-minimization.md die Scope-Dokumentation, greift also

### Gaps

- Kriterien 2, 3, 4, 8, 9, 10 (dokumentierte Scopes je Tool, serverseitige Scope-Validierung je Tool-Call, 403 mit `WWW-Authenticate`, minimaler Login-Scope, Granularitaet lesen/schreiben x Datenklasse, explizite Admin-Scopes) sind unerfuellt und im aktuellen Auth-Modell nicht erfuellbar: der Server hat keine eingehende Autorisierung
- Kriterien 5 und 6 unerfuellt: `/.well-known/oauth-protected-resource` wird nicht bedient. grep -rn 'well-known' src/ liefert 0 Treffer. RFC 9728/SEP-985 verlangt den Endpunkt nur fuer geschuetzte Ressourcen — dieser Server ist keine, wodurch das Kriterium gegenstandslos, aber auch nicht positiv belegbar ist
- Der Check greift ueber `auth_model != "none"` und trifft damit auch API-Key-Server, deren Schluessel ausschliesslich upstream wirkt. Die Pass-Kriterien sind durchgaengig OAuth-Scope-spezifisch; ein solcher Server kann sie strukturell nicht erfuellen und ist deshalb dauerhaft `partial`. KATALOG-HINWEIS, nicht Befund gegen diesen Server

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SEC-003.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SEC-004

## Finding: SEC-004 — SSRF-Prevention: HTTPS-Enforcement + IP-Blocklisting

**Severity:** critical
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SEC-004
**Katalog-Referenz:** Sec 4.4
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/server.py:291, 379, 448, 544, 646 — alle 5 datenabrufenden Tools rufen `_http_get(DISCOVERY_BASE_URL, <pfad>, …)`. Die Basis-URL ist die Modulkonstante `client.py:27` (`https://api.library.ethz.ch/discovery/v1`); kein Tool-Parameter liefert Schema oder Host. Die SSRF-Grundvoraussetzung (URL aus Tool-Argumenten) besteht damit nicht
- src/eth_library_mcp/client.py:48-52, 71 — `_check_egress_allowed(url)` laeuft vor jedem ausgehenden Request und vergleicht `urlparse(url).hostname` gegen ein `frozenset` mit genau einem Eintrag. LAUFZEITMESSUNG ueber `PYTHONPATH=src python -c`: `http://169.254.169.254/latest/meta-data/` -> PermissionError, `http://127.0.0.1:8000/admin` -> PermissionError, `https://evil.example/x` -> PermissionError, `file:///etc/passwd` -> PermissionError (hostname ''), `https://api.library.ethz.ch@evil.example/x` -> PermissionError. Deny-by-default deckt die Blocklist-Ziele des Checks (Metadata-IP, Loopback, Fremdhost, Userinfo-Trick) mit ab
- NEGATIVE KONTROLLE derselben Messung: `https://api.library.ethz.ch/discovery/v1/resources` wird durchgelassen — der Guard weist nicht pauschal alles ab, die vier Blockaden sind also Messungen und kein Dauer-Nein
- GEMESSENE LUECKE: `_check_egress_allowed('http://api.library.ethz.ch/discovery/v1/resources')` wird DURCHGELASSEN. Das Schema wird nirgends geprueft; HTTPS ergibt sich allein daraus, dass die Konstante in client.py:27 zufaellig `https://` beginnt
- src/eth_library_mcp/server.py:340-347 — `mmsid` ist `str` mit `min_length=5/max_length=50` ohne `pattern` und geht unmaskiert in den Pfad (`f"/resources/{params.mmsid}"`). GEMESSEN: `GetResourceInput(mmsid='../../secret')` wird akzeptiert. Der Host bleibt dabei fix, eine SSRF auf einen fremden Host ist damit nicht moeglich — wohl aber ein Pfadwechsel innerhalb von api.library.ethz.ch

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SEC-004.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/server.py:291, 379, 448, 544, 646 — alle 5 datenabrufenden Tools rufen `_http_get(DISCOVERY_BASE_URL, <pfad>, …)`. Die Basis-URL ist die Modulkonstante `client.py:27` (`https://api.library.ethz.ch/discovery/v1`); kein Tool-Parameter liefert Schema oder Host. Die SSRF-Grundvoraussetzung (URL aus Tool-Argumenten) besteht damit nicht
- src/eth_library_mcp/client.py:48-52, 71 — `_check_egress_allowed(url)` laeuft vor jedem ausgehenden Request und vergleicht `urlparse(url).hostname` gegen ein `frozenset` mit genau einem Eintrag. LAUFZEITMESSUNG ueber `PYTHONPATH=src python -c`: `http://169.254.169.254/latest/meta-data/` -> PermissionError, `http://127.0.0.1:8000/admin` -> PermissionError, `https://evil.example/x` -> PermissionError, `file:///etc/passwd` -> PermissionError (hostname ''), `https://api.library.ethz.ch@evil.example/x` -> PermissionError. Deny-by-default deckt die Blocklist-Ziele des Checks (Metadata-IP, Loopback, Fremdhost, Userinfo-Trick) mit ab
- NEGATIVE KONTROLLE derselben Messung: `https://api.library.ethz.ch/discovery/v1/resources` wird durchgelassen — der Guard weist nicht pauschal alles ab, die vier Blockaden sind also Messungen und kein Dauer-Nein
- GEMESSENE LUECKE: `_check_egress_allowed('http://api.library.ethz.ch/discovery/v1/resources')` wird DURCHGELASSEN. Das Schema wird nirgends geprueft; HTTPS ergibt sich allein daraus, dass die Konstante in client.py:27 zufaellig `https://` beginnt
- src/eth_library_mcp/server.py:340-347 — `mmsid` ist `str` mit `min_length=5/max_length=50` ohne `pattern` und geht unmaskiert in den Pfad (`f"/resources/{params.mmsid}"`). GEMESSEN: `GetResourceInput(mmsid='../../secret')` wird akzeptiert. Der Host bleibt dabei fix, eine SSRF auf einen fremden Host ist damit nicht moeglich — wohl aber ein Pfadwechsel innerhalb von api.library.ethz.ch

### Gaps

- Kriterium 1 unerfuellt: keine HTTPS-Schema-Validierung vor dem Request. Ein spaeterer Commit, der eine Basis-URL auf `http://` setzt, laeuft durch den Guard hindurch — gemessen, nicht geschlossen
- Kriterien 2-4 unerfuellt in der vom Check verlangten Form: es gibt keine Aufloesung mit anschliessender IP-Blocklist-Pruefung (`getaddrinfo`/`ipaddress` kommen in src/ nicht vor). Die Metadata-IP, `::1` und `fe80::/10` sind nur mittelbar durch die Host-Allow-List gesperrt, nicht explizit gelistet. Fuer den heutigen Codepfad genuegt das; bei der ersten Erweiterung um einen zweiten Host faellt der Schutz auf Namensvergleich zurueck
- Kriterium 5 unerfuellt: kein Egress-Proxy (Smokescreen o.ae.) als Defense-in-Depth; docs/network-egress.md:34-47 fuehrt Netzwerk-Layer-Kontrollen ausdruecklich nur als Empfehlung
- `mmsid` ohne `pattern` (z.B. `^[0-9]{5,50}$`) laesst Pfadsegmente wie `../` in den URL-Pfad; Auswirkung heute auf denselben Host begrenzt, aber unnoetig

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `critical`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SEC-004.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SEC-005

## Finding: SEC-005 — DNS-Rebinding **egress**: DNS-Pinning gegen TOCTOU

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SEC-005
**Katalog-Referenz:** Sec 4.4
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/client.py:48-52, 70-85 — GEMESSEN am Code: es gibt genau eine Stelle, an der ein Hostname verarbeitet wird. `_check_egress_allowed` arbeitet rein auf der URL-Zeichenkette (`urlparse(...).hostname`), loest also gar nicht auf; danach bekommt httpx den Hostnamen und loest ihn einmal beim Verbindungsaufbau auf. Das im Check beschriebene TOCTOU-Fenster (pruefende Aufloesung + zweite benutzende Aufloesung) existiert hier nicht, weil die erste Aufloesung fehlt
- Kriterien 3 und 4 erfuellt: httpx bekommt die Original-URL, setzt daraus `Host` und SNI und prueft das Zertifikat gegen den Hostnamen. grep -rnE 'verify\s*=\s*False|ssl_verify|VERIFY_NONE|trust_env' src/ scripts/ liefert 0 Treffer (Exit 1) — die Zertifikatspruefung wird nirgends abgeschaltet. NEGATIVE KONTROLLE: dasselbe Muster gegen eine Sondendatei mit `httpx.AsyncClient(verify=False)` liefert 1 Treffer
- grep -rE 'getaddrinfo|gethostbyname|dns\.resolve' src/ liefert 0 Treffer — es existiert kein eigener Resolver-Pfad, an dem gepinnt werden koennte oder muesste
- docs/ARCHITECTURE.md:90-102 — der Zustand ist als bewusst akzeptiertes Risiko dokumentiert («There is no DNS-pinning in the httpx client»), mit Begruendung (keine nutzergelieferte URL erreicht den Client) und einem benannten Wiedervorlage-Ausloeser («If a future feature accepts URLs from tool input …»)

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SEC-005.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/client.py:48-52, 70-85 — GEMESSEN am Code: es gibt genau eine Stelle, an der ein Hostname verarbeitet wird. `_check_egress_allowed` arbeitet rein auf der URL-Zeichenkette (`urlparse(...).hostname`), loest also gar nicht auf; danach bekommt httpx den Hostnamen und loest ihn einmal beim Verbindungsaufbau auf. Das im Check beschriebene TOCTOU-Fenster (pruefende Aufloesung + zweite benutzende Aufloesung) existiert hier nicht, weil die erste Aufloesung fehlt
- Kriterien 3 und 4 erfuellt: httpx bekommt die Original-URL, setzt daraus `Host` und SNI und prueft das Zertifikat gegen den Hostnamen. grep -rnE 'verify\s*=\s*False|ssl_verify|VERIFY_NONE|trust_env' src/ scripts/ liefert 0 Treffer (Exit 1) — die Zertifikatspruefung wird nirgends abgeschaltet. NEGATIVE KONTROLLE: dasselbe Muster gegen eine Sondendatei mit `httpx.AsyncClient(verify=False)` liefert 1 Treffer
- grep -rE 'getaddrinfo|gethostbyname|dns\.resolve' src/ liefert 0 Treffer — es existiert kein eigener Resolver-Pfad, an dem gepinnt werden koennte oder muesste
- docs/ARCHITECTURE.md:90-102 — der Zustand ist als bewusst akzeptiertes Risiko dokumentiert («There is no DNS-pinning in the httpx client»), mit Begruendung (keine nutzergelieferte URL erreicht den Client) und einem benannten Wiedervorlage-Ausloeser («If a future feature accepts URLs from tool input …»)

### Gaps

- Kein DNS-Pinning im engeren Sinn: die aufgeloeste IP wird nicht festgehalten und nicht gegen eine Blockliste geprueft. Loest `api.library.ethz.ch` durch DNS-Kompromittierung auf eine interne Adresse auf, verhindert nichts im Prozess den Request — die Host-Allow-List vergleicht Namen, keine Adressen
- Kriterium 5 unerfuellt: kein Test belegt, dass pro Request genau eine DNS-Aufloesung stattfindet. grep -rniE 'getaddrinfo|dns' tests/ --include='*.py' liefert 0 Treffer (auch die eingehende Haelfte in test_transport_security.py nennt DNS nicht beim Namen). Der Befund oben ist damit eine Code-Lesung plus Mustermessung, kein gegatetes Verhalten
- Der pro-Prozess geteilte `httpx.AsyncClient` (client.py:88-101) haelt Verbindungen offen; wie lange eine einmal aufgeloeste Adresse weiterverwendet wird, ist damit vom Pool abhaengig und nirgends festgelegt oder gemessen

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SEC-005.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SEC-007

## Finding: SEC-007 — Container-Sandboxing: Docker / chroot mit minimalen Privilegien

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SEC-007
**Katalog-Referenz:** Sec 4.5
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Dockerfile:20, 27 — `useradd --uid 1000 --create-home --shell /usr/sbin/nologin app` und `USER 1000`: der Prozess laeuft nicht als root, die Login-Shell ist `nologin`
- Dockerfile:9-25 — Multi-Stage-Build: das Wheel entsteht in `python:3.14-slim AS builder`, das Laufzeit-Image installiert nur `/tmp/wheels/*.whl` und loescht das Verzeichnis danach. Weder `build` noch pip-Cache noch Quellbaum liegen in der finalen Schicht
- .dockerignore (13 Zeilen) — schliesst `.git/`, `.github/`, `audits/`, `tests/`, `docs/`, `.env` und `.env.*` aus dem Build-Kontext aus; ein versehentlich vorhandenes `.env` kann nicht in eine Schicht geraten
- Dockerfile:32-33 — `PYTHONUNBUFFERED=1`, `PYTHONDONTWRITEBYTECODE=1`; keine einzige `ENV`-Zeile traegt ein Geheimnis, und `ARG` kommt gar nicht vor (gemessen an der Datei, 36 Zeilen)
- Kein Kubernetes-Manifest im Baum: `ls docker-compose*.yml railway.toml render.yaml k8s helm` meldet fuer alle fuenf «No such file or directory». Die Kriterien 2-5 (runAsNonRoot, readOnlyRootFilesystem, capabilities.drop, seccomp) haben damit keinen Ort, an dem sie stehen koennten — sie sind unbelegt, nicht verletzt

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SEC-007.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Dockerfile:20, 27 — `useradd --uid 1000 --create-home --shell /usr/sbin/nologin app` und `USER 1000`: der Prozess laeuft nicht als root, die Login-Shell ist `nologin`
- Dockerfile:9-25 — Multi-Stage-Build: das Wheel entsteht in `python:3.14-slim AS builder`, das Laufzeit-Image installiert nur `/tmp/wheels/*.whl` und loescht das Verzeichnis danach. Weder `build` noch pip-Cache noch Quellbaum liegen in der finalen Schicht
- .dockerignore (13 Zeilen) — schliesst `.git/`, `.github/`, `audits/`, `tests/`, `docs/`, `.env` und `.env.*` aus dem Build-Kontext aus; ein versehentlich vorhandenes `.env` kann nicht in eine Schicht geraten
- Dockerfile:32-33 — `PYTHONUNBUFFERED=1`, `PYTHONDONTWRITEBYTECODE=1`; keine einzige `ENV`-Zeile traegt ein Geheimnis, und `ARG` kommt gar nicht vor (gemessen an der Datei, 36 Zeilen)
- Kein Kubernetes-Manifest im Baum: `ls docker-compose*.yml railway.toml render.yaml k8s helm` meldet fuer alle fuenf «No such file or directory». Die Kriterien 2-5 (runAsNonRoot, readOnlyRootFilesystem, capabilities.drop, seccomp) haben damit keinen Ort, an dem sie stehen koennten — sie sind unbelegt, nicht verletzt

### Gaps

- Kriterium 1 woertlich verfehlt: gefordert ist UID >= 10000, Dockerfile:20/27 setzt 1000. UID 1000 kollidiert in einem User-Namespace typischerweise mit dem ersten Host-Benutzer — genau der Fall, gegen den die Schwelle gesetzt ist
- `--read-only --tmpfs /tmp` steht nur als Kommentar in Dockerfile:6 und wird nirgends erzwungen: es gibt kein Compose-File und kein Manifest, das die Runtime-Flags setzt. Wer `docker run` von Hand aufruft, bekommt ein schreibbares Root-Dateisystem
- Kein seccomp-Profil benannt (Kriterium 5) und keine `HEALTHCHECK`-Zeile, obwohl Dockerfile:7 einen «Health-check via the streamable-http transport endpoint» ankuendigt — die Datei behauptet hier mehr, als sie enthaelt
- Dockerfile:36 startet den Container mit `--host 0.0.0.0` und ohne `ETH_LIBRARY_ALLOWED_HOSTS`; der Container laeuft damit im gemessenen Fail-open-Zustand der eingehenden Host-Pruefung (siehe SEC-024). Das Image traegt keinen Default fuer die Variable und keinen Hinweis darauf

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SEC-007.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SEC-018

## Finding: SEC-018 — Input-Validation an Tool-Boundaries (Pydantic strict / Zod)

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SEC-018
**Katalog-Referenz:** Sec 3 / Sec 4 (Defense-in-Depth)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Alle 5 argumentfuehrenden Tools nehmen ein Pydantic-Modell: SearchResourcesInput (server.py:195-243), GetResourceInput (335-355), SearchArchiveInput (395-418), SearchByTypeInput (485-510), SearchEducationInput (584-609). Das sechste Tool `eth_library_info` (server.py:699) nimmt gar keine Argumente — GEMESSEN ueber `mcp.list_tools()`: 6 Tools, 5 davon mit `properties`, eines mit 0
- Numerische Constraints vorhanden: `limit` traegt ueberall `ge`/`le` (1-100 bzw. 1-50), `offset` traegt `ge=0`. LAUFZEITMESSUNG: `SearchResourcesInput(query='a', limit=0)` -> ValidationError `greater_than_equal`, `limit=101` -> `less_than_equal`
- String-Constraints vorhanden: `query` min_length=1/max_length=500, `topic` 2-300, `mmsid` 5-50. LAUFZEITMESSUNG: leerer `query` -> `string_too_short`, 501 Zeichen -> `string_too_long`
- `extra="forbid"` ist in allen 5 `model_config`-Zeilen explizit gesetzt (server.py:198, 338, 398, 488, 587). LAUFZEITMESSUNG: ein unbekanntes Feld -> `extra_forbidden`
- Whitelist statt Blacklist bei den Aufzaehlungen: `SortOption`, `ResourceType`, `ArchiveKey` sind `Literal`-Typen (server.py:65-86), die Werte stammen aus den Konstanten-Dicts
- Kriterium 6 erfuellt: LAUFZEITMESSUNG ueber `await mcp.call_tool('eth_search_resources', {...})` mit zu langem String, Out-of-Range-Zahl und unbekanntem Feld — jedes Mal `ToolError: Error executing tool … 1 validation error …`, kein Server-Crash, kein Traceback an den Aufrufer

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SEC-018.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Alle 5 argumentfuehrenden Tools nehmen ein Pydantic-Modell: SearchResourcesInput (server.py:195-243), GetResourceInput (335-355), SearchArchiveInput (395-418), SearchByTypeInput (485-510), SearchEducationInput (584-609). Das sechste Tool `eth_library_info` (server.py:699) nimmt gar keine Argumente — GEMESSEN ueber `mcp.list_tools()`: 6 Tools, 5 davon mit `properties`, eines mit 0
- Numerische Constraints vorhanden: `limit` traegt ueberall `ge`/`le` (1-100 bzw. 1-50), `offset` traegt `ge=0`. LAUFZEITMESSUNG: `SearchResourcesInput(query='a', limit=0)` -> ValidationError `greater_than_equal`, `limit=101` -> `less_than_equal`
- String-Constraints vorhanden: `query` min_length=1/max_length=500, `topic` 2-300, `mmsid` 5-50. LAUFZEITMESSUNG: leerer `query` -> `string_too_short`, 501 Zeichen -> `string_too_long`
- `extra="forbid"` ist in allen 5 `model_config`-Zeilen explizit gesetzt (server.py:198, 338, 398, 488, 587). LAUFZEITMESSUNG: ein unbekanntes Feld -> `extra_forbidden`
- Whitelist statt Blacklist bei den Aufzaehlungen: `SortOption`, `ResourceType`, `ArchiveKey` sind `Literal`-Typen (server.py:65-86), die Werte stammen aus den Konstanten-Dicts
- Kriterium 6 erfuellt: LAUFZEITMESSUNG ueber `await mcp.call_tool('eth_search_resources', {...})` mit zu langem String, Out-of-Range-Zahl und unbekanntem Feld — jedes Mal `ToolError: Error executing tool … 1 validation error …`, kein Server-Crash, kein Traceback an den Aufrufer

### Gaps

- Kriterium 5 zur Haelfte unerfuellt: `strict=True` ist in KEINEM der 5 `ConfigDict` gesetzt (nur `str_strip_whitespace=True, extra="forbid"`). LAUFZEITMESSUNG der Folge: `SearchResourcesInput(query='a', limit='10')` wird AKZEPTIERT und zu `limit=10` gecastet, `open_access_only='yes'` wird zu `True`. Ein Client, der Typen verwechselt, bekommt keinen Fehler, sondern eine stille Umdeutung
- Kriterium 3 (`pattern`) nirgends genutzt. Besonders bei `mmsid`, das unmaskiert in den URL-Pfad geht (server.py:379): LAUFZEITMESSUNG `GetResourceInput(mmsid='../../secret')` wird akzeptiert. Eine Alma-MMS-ID ist rein numerisch, `^[0-9]{5,50}$` waere die passende Whitelist
- `offset` hat `ge=0`, aber kein `le` (server.py:219-223, 418, 510) — der Range ist nach oben unbegrenzt; `offset=10**18` geht als Query-Parameter an den Upstream
- Kriterium 7 unerfuellt: tests/test_tools.py (203 Zeilen, 11 Tests) deckt ausschliesslich Happy-Path, HTTP-Fehlerbilder und die Egress-Sperre ab. Kein Test fuer zu lange Strings, Out-of-Range-Zahlen oder unbekannte Felder — die drei Messungen oben sind meine, nicht die der CI

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SEC-018.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SEC-019

## Finding: SEC-019 — Lethal Trifecta vermeiden: Server-Separation Read vs Write/Send

**Severity:** critical
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SEC-019
**Katalog-Referenz:** Anhang B1
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Faehigkeit 1 (private Daten) NEIN — gemessen an der Egress-Allow-List `client.py:33` (genau `api.library.ethz.ch`) und docs/data-sources.md: ausschliesslich bibliografische Public-Domain-Metadaten; keine PII-Quelle im Baum
- Faehigkeit 2 (untrusted Content) JA, eingeschraenkt — die Upstream-Antwort wird in `formatting.py:34-109` unveraendert in den Markdown-Text gerendert (Titel, Creator, Beschreibung, `linkURL`) und landet so im Modellkontext. Quelle ist ein einziger, allow-gelisteter Host
- Faehigkeit 3 (externe Kommunikation) NEIN — grep -rnE 'httpx\.post|\.post\(|smtplib|send_mail|webhook|slack' src/ liefert 0 Treffer (Exit 1). NEGATIVE KONTROLLE: dasselbe Muster gegen eine Sondendatei mit `await client.post("x")` liefert 1 Treffer. Der einzige ausgehende Aufruf ist `client.get` in client.py:76 und 83
- Alle 6 Tools tragen `readOnlyHint: True` und `destructiveHint: False` (server.py:250-253, 362-365, 426-429, 517-520, 616-619, 693-696) — gemessen an den Dekoratoren, nicht an der README-Behauptung
- Damit 1 von 3 Trifecta-Faehigkeiten: Kriterium 2 (hoechstens zwei) ist erfuellt, Kriterien 3-5 sind gegenstandslos

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SEC-019.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Faehigkeit 1 (private Daten) NEIN — gemessen an der Egress-Allow-List `client.py:33` (genau `api.library.ethz.ch`) und docs/data-sources.md: ausschliesslich bibliografische Public-Domain-Metadaten; keine PII-Quelle im Baum
- Faehigkeit 2 (untrusted Content) JA, eingeschraenkt — die Upstream-Antwort wird in `formatting.py:34-109` unveraendert in den Markdown-Text gerendert (Titel, Creator, Beschreibung, `linkURL`) und landet so im Modellkontext. Quelle ist ein einziger, allow-gelisteter Host
- Faehigkeit 3 (externe Kommunikation) NEIN — grep -rnE 'httpx\.post|\.post\(|smtplib|send_mail|webhook|slack' src/ liefert 0 Treffer (Exit 1). NEGATIVE KONTROLLE: dasselbe Muster gegen eine Sondendatei mit `await client.post("x")` liefert 1 Treffer. Der einzige ausgehende Aufruf ist `client.get` in client.py:76 und 83
- Alle 6 Tools tragen `readOnlyHint: True` und `destructiveHint: False` (server.py:250-253, 362-365, 426-429, 517-520, 616-619, 693-696) — gemessen an den Dekoratoren, nicht an der README-Behauptung
- Damit 1 von 3 Trifecta-Faehigkeiten: Kriterium 2 (hoechstens zwei) ist erfuellt, Kriterien 3-5 sind gegenstandslos

### Gaps

- Kriterium 1 unerfuellt: grep -rniE 'trifecta' ueber alle *.md ausserhalb von audits/ liefert 0 Treffer (Exit 1) — es gibt keine Trifecta-Bewertung in README oder docs/. NEGATIVE KONTROLLE: dasselbe Muster findet den Begriff in audits/2026-05-28*/verification-results.json, greift also. SECURITY.md:18-19 sagt die Substanz («read-only, no-PII, public-domain-metadata, nur HTTP GET»), benennt aber die drei Faehigkeiten nicht einzeln und traegt keine Tabelle, an der eine kuenftige Erweiterung auffiele
- Kein ADR im Baum: `find . -iname '*adr*' -o -iname '*architecture*'` (ohne .git/audits) liefert genau docs/ARCHITECTURE.md; dessen Abschnitte (Modullayout, Tool-Inventar, Logging, SEC-005, SCALE-002) fuehren keine Server-Separation und keine Trifecta-Begruendung. Bei 1 von 3 Faehigkeiten ist ein ADR laut Kriterium 3 auch nicht gefordert — es fehlt damit nur die Bewertung selbst
- Die Re-Evaluation-Trigger in SECURITY.md:75-85 nennen Write-Faehigkeit und PII — genau die Trifecta-Achsen — ohne sie so zu benennen. Der Satz waere die natuerliche Stelle fuer die fehlende Bewertung

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `critical`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SEC-019.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SEC-021

## Finding: SEC-021 — Egress-Allow-List: Code-Layer und Network-Layer

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SEC-021
**Katalog-Referenz:** Anhang B5 + B12
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/client.py:31-33 — `ALLOWED_EGRESS_HOSTS: frozenset[str] = frozenset({"api.library.ethz.ch"})`: Kriterium 1 erfuellt, die Liste ist ein `frozenset` im Code und zur Laufzeit nicht mutierbar
- src/eth_library_mcp/client.py:70-71 — `_check_egress_allowed(url)` steht VOR der Verzweigung in den gepoolten und den Einzel-Client (Zeilen 75-85); beide ausgehenden Pfade laufen also durch die Pruefung. Es gibt keinen zweiten HTTP-Client im Baum: grep -rnE 'httpx\.' src/ trifft ausschliesslich client.py:35, 38, 80, 90, 93 (Clientaufbau und Kommentare) und formatting.py:128, 154, 156 (isinstance-Fehlerabbildung) — kein weiterer Aufrufort
- LAUFZEITMESSUNG des Pre-Request-Checks: `_check_egress_allowed` gegen 7 URLs — `https://api.library.ethz.ch/...` durchgelassen; `https://evil.example/x`, `http://169.254.169.254/latest/meta-data/`, `http://127.0.0.1:8000/admin`, `file:///etc/passwd`, `https://api.library.ethz.ch@evil.example/x` je `PermissionError: Egress denied: host … not in ALLOWED_EGRESS_HOSTS`. Das erste Ergebnis ist die NEGATIVE KONTROLLE: der Guard sagt nicht zu allem Nein
- docs/network-egress.md:7-13 — Kriterium 3 erfuellt: Tabelle Host x Nutzer x Zweck (`api.library.ethz.ch` | all 6 tools | Bibliographic lookups), plus die Aussage, dass jeder Aufruf durch `_check_egress_allowed()` laeuft
- docs/network-egress.md:26-32 — Kriterium 5 erfuellt: vierschrittiges Update-Verfahren fuer neue Hosts, inklusive der Anweisung, Allow-List-Wachstum im PR als sicherheitsrelevanten Diff zu behandeln
- tests/test_tools.py:195-203 — `test_egress_blocked_for_unknown_host` haelt die Sperre gegatet, indem es `DISCOVERY_BASE_URL` auf `https://evil.example.com/v1` umbiegt und eine Fehlermeldung statt eines Requests erwartet

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SEC-021.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/client.py:31-33 — `ALLOWED_EGRESS_HOSTS: frozenset[str] = frozenset({"api.library.ethz.ch"})`: Kriterium 1 erfuellt, die Liste ist ein `frozenset` im Code und zur Laufzeit nicht mutierbar
- src/eth_library_mcp/client.py:70-71 — `_check_egress_allowed(url)` steht VOR der Verzweigung in den gepoolten und den Einzel-Client (Zeilen 75-85); beide ausgehenden Pfade laufen also durch die Pruefung. Es gibt keinen zweiten HTTP-Client im Baum: grep -rnE 'httpx\.' src/ trifft ausschliesslich client.py:35, 38, 80, 90, 93 (Clientaufbau und Kommentare) und formatting.py:128, 154, 156 (isinstance-Fehlerabbildung) — kein weiterer Aufrufort
- LAUFZEITMESSUNG des Pre-Request-Checks: `_check_egress_allowed` gegen 7 URLs — `https://api.library.ethz.ch/...` durchgelassen; `https://evil.example/x`, `http://169.254.169.254/latest/meta-data/`, `http://127.0.0.1:8000/admin`, `file:///etc/passwd`, `https://api.library.ethz.ch@evil.example/x` je `PermissionError: Egress denied: host … not in ALLOWED_EGRESS_HOSTS`. Das erste Ergebnis ist die NEGATIVE KONTROLLE: der Guard sagt nicht zu allem Nein
- docs/network-egress.md:7-13 — Kriterium 3 erfuellt: Tabelle Host x Nutzer x Zweck (`api.library.ethz.ch` | all 6 tools | Bibliographic lookups), plus die Aussage, dass jeder Aufruf durch `_check_egress_allowed()` laeuft
- docs/network-egress.md:26-32 — Kriterium 5 erfuellt: vierschrittiges Update-Verfahren fuer neue Hosts, inklusive der Anweisung, Allow-List-Wachstum im PR als sicherheitsrelevanten Diff zu behandeln
- tests/test_tools.py:195-203 — `test_egress_blocked_for_unknown_host` haelt die Sperre gegatet, indem es `DISCOVERY_BASE_URL` auf `https://evil.example.com/v1` umbiegt und eine Fehlermeldung statt eines Requests erwartet

### Gaps

- Kriterium 2 unerfuellt: keine Network-Layer-Egress-Kontrolle. docs/network-egress.md:34-47 fuehrt NetworkPolicy, Security Group und Tailscale-ACL ausdruecklich nur als Empfehlung und schliesst mit «does not require network-layer egress controls» fuer das aktuelle Profil. Es gibt kein k8s-/Compose-/railway-Manifest im Baum (alle fuenf `ls`-Kandidaten fehlen), also auch keinen Ort dafuer
- Kriterium 6 damit gegenstandslos: ohne Network-Layer gibt es keinen DNS-Pfad, der explizit freigegeben werden muesste — unbelegt, nicht verletzt
- Der Guard prueft nur den Host, nicht das Schema: `_check_egress_allowed('http://api.library.ethz.ch/...')` wird GEMESSEN durchgelassen. Eine Allow-List, die Klartext-HTTP gegen denselben Host erlaubt, deckt den Abhoerfall nicht (siehe SEC-004)
- Die Sperre ist ein `PermissionError`, der ueber `except Exception` in `_handle_error` landet und dort als «Unbekannter Fehler. Bitte spaeter erneut versuchen.» herauskommt — die Allow-List wirkt, meldet sich aber nicht als solche (Befund gefuehrt unter SEC-028)

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SEC-021.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SEC-024

## Finding: SEC-024 — Inbound Host/Origin-Allow-List (DNS-Rebinding auf den eigenen Endpoint)

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SEC-024
**Katalog-Referenz:** Sec 4.4
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- Evidence 1 erfuellt: src/eth_library_mcp/server.py:896-900 baut `TransportSecuritySettings(enable_dns_rebinding_protection=True, allowed_hosts=…, allowed_origins=…)`, und server.py:926 verdrahtet es (`mcp.streamable_http_app(transport_security=security, host=host)`). `build_http_app` ist der einzige Pfad, ueber den eine App entsteht: grep -rnE 'streamable_http_app\(|build_http_app|mcp\.run\(|sse_app\(' src/ liefert genau vier Zeilen — server.py:903 (Definition), 926 (Verdrahtung), 957 (`uvicorn.run(build_http_app(host, port), …)`) und 973 (`mcp.run()`, stdio). Kein zweiter Netzpfad (Kriterium 10)
- Kriterium 2 erfuellt: die Liste kommt aus `ETH_LIBRARY_ALLOWED_HOSTS` (server.py:850-858), nicht aus dem Code; README.md:111 und README.de.md:111 dokumentieren die Variable samt Folge ihres Fehlens (421)
- LAUFZEITMESSUNG des tragenden Paares (Kriterium 3 und 8, Substanz): mit `ETH_LIBRARY_ALLOWED_HOSTS=mcp.example.ch:8000` gegen `build_http_app('0.0.0.0', 8000)` ein echtes `initialize` gepostet — `Host: mcp.example.ch:8000` -> HTTP 200, `Host: mcp.example.ch:9999` -> HTTP 421 «Invalid Host header», `Host: evil.example:8000` -> HTTP 421, `Host: 127.0.0.1:8000` -> HTTP 200. Gleicher Name, anderer Port wird abgewiesen, waehrend der richtige Port bedient wird: eine zurueckgefallene Loopback-Default-Policy ist damit ausgeschlossen, die uebergebene Liste greift portgenau
- Kriterium 4 erfuellt: dieselbe Messung ergab `allowed_hosts = ['127.0.0.1:8000', '[::1]:8000', 'localhost:8000', 'mcp.example.ch:8000']` — Loopback in allen drei Schreibweisen mit dem tatsaechlich bedienten Port (server.py:881, 885); tests/test_transport_security.py:133-141 gatet das
- Kriterien 5 und 6 erfuellt: server.py:894-895 uebernimmt die konfigurierten CORS-Origins in `allowed_origins` und filtert `*` heraus. LAUFZEITMESSUNG mit `ETH_LIBRARY_CORS_ORIGINS=https://client.example`: erlaubte Origin -> 200, `https://woanders.example` -> 403 (nicht 400). tests/test_transport_security.py:121-130 gatet die `*`-Filterung
- Kriterium 7 erfuellt und LAUFZEITMESSUNG: Start mit `--host 0.0.0.0` bei leerem `ETH_LIBRARY_ALLOWED_HOSTS` schreibt `{"event": "dns_rebinding_protection_off", "level": "warning", "host": "0.0.0.0", "hint": "Bind ist nicht Loopback und ETH_LIBRARY_ALLOWED_HOSTS ist leer…"}` (server.py:918-925); der Loopback-Start schreibt sie nicht

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SEC-024.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Evidence 1 erfuellt: src/eth_library_mcp/server.py:896-900 baut `TransportSecuritySettings(enable_dns_rebinding_protection=True, allowed_hosts=…, allowed_origins=…)`, und server.py:926 verdrahtet es (`mcp.streamable_http_app(transport_security=security, host=host)`). `build_http_app` ist der einzige Pfad, ueber den eine App entsteht: grep -rnE 'streamable_http_app\(|build_http_app|mcp\.run\(|sse_app\(' src/ liefert genau vier Zeilen — server.py:903 (Definition), 926 (Verdrahtung), 957 (`uvicorn.run(build_http_app(host, port), …)`) und 973 (`mcp.run()`, stdio). Kein zweiter Netzpfad (Kriterium 10)
- Kriterium 2 erfuellt: die Liste kommt aus `ETH_LIBRARY_ALLOWED_HOSTS` (server.py:850-858), nicht aus dem Code; README.md:111 und README.de.md:111 dokumentieren die Variable samt Folge ihres Fehlens (421)
- LAUFZEITMESSUNG des tragenden Paares (Kriterium 3 und 8, Substanz): mit `ETH_LIBRARY_ALLOWED_HOSTS=mcp.example.ch:8000` gegen `build_http_app('0.0.0.0', 8000)` ein echtes `initialize` gepostet — `Host: mcp.example.ch:8000` -> HTTP 200, `Host: mcp.example.ch:9999` -> HTTP 421 «Invalid Host header», `Host: evil.example:8000` -> HTTP 421, `Host: 127.0.0.1:8000` -> HTTP 200. Gleicher Name, anderer Port wird abgewiesen, waehrend der richtige Port bedient wird: eine zurueckgefallene Loopback-Default-Policy ist damit ausgeschlossen, die uebergebene Liste greift portgenau
- Kriterium 4 erfuellt: dieselbe Messung ergab `allowed_hosts = ['127.0.0.1:8000', '[::1]:8000', 'localhost:8000', 'mcp.example.ch:8000']` — Loopback in allen drei Schreibweisen mit dem tatsaechlich bedienten Port (server.py:881, 885); tests/test_transport_security.py:133-141 gatet das
- Kriterien 5 und 6 erfuellt: server.py:894-895 uebernimmt die konfigurierten CORS-Origins in `allowed_origins` und filtert `*` heraus. LAUFZEITMESSUNG mit `ETH_LIBRARY_CORS_ORIGINS=https://client.example`: erlaubte Origin -> 200, `https://woanders.example` -> 403 (nicht 400). tests/test_transport_security.py:121-130 gatet die `*`-Filterung
- Kriterium 7 erfuellt und LAUFZEITMESSUNG: Start mit `--host 0.0.0.0` bei leerem `ETH_LIBRARY_ALLOWED_HOSTS` schreibt `{"event": "dns_rebinding_protection_off", "level": "warning", "host": "0.0.0.0", "hint": "Bind ist nicht Loopback und ETH_LIBRARY_ALLOWED_HOSTS ist leer…"}` (server.py:918-925); der Loopback-Start schreibt sie nicht

### Gaps

- Evidence 2 als REPO-TEST fehlt: tests/test_transport_security.py:96-104 faehrt das Paar «erlaubter Name 200 / fremder Name 421», nicht das Paar «richtiger Port 200 / falscher Port 421». Der Eintrag im Test traegt ueberdies gar keinen Port (`ETH_LIBRARY_ALLOWED_HOSTS=mcp.example.ch`), sodass die Portgenauigkeit in der CI nirgends behauptet wird. Die Messung oben ist meine; faellt die Portgenauigkeit kuenftig weg, faellt kein Test
- Kein Hinweis fuer Betreiber, dass ein Eintrag seinen Port tragen muss: README.md:111 nennt nur «Comma-separated hostnames». Wer auf Port 8000 hinter einem Proxy ohne Port-Rewrite bedient und `mcp.example.ch` eintraegt, bekommt gemessen 421 auf jede Anfrage — die dokumentierte Konfiguration erzeugt dann genau den Fehler, den die Variable beheben soll
- Kriterium 9 (gueltiges Auth-Token rettet keinen fremden Host) ist gegenstandslos: der Server nimmt keine Authentisierung entgegen (`MCPServer(...)` ohne `auth=`, server.py:168-187). Unbelegt, nicht verletzt
- Der Dockerfile-Default (Zeile 36: `--host 0.0.0.0` ohne `ETH_LIBRARY_ALLOWED_HOSTS`) liefert das Image im Fail-open-Zustand aus; die Warnung sagt es, aber nichts im Image setzt die Variable oder verlangt sie

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SEC-024.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


### SEC-028

## Finding: SEC-028 — Egress-Guard: Policy-Verstoss und Auflösungsfehler sind unterscheidbar

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** SEC-028
**Katalog-Referenz:** Custom (Katalog-Lücke, aufgefallen bei zh-education-mcp, 2026-08-03)
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in diesem Lauf am Baum gemessen worden.

- Die Typen sind intern verschieden (Kriterium 1, halb erfuellt): der Policy-Verstoss ist `PermissionError` aus src/eth_library_mcp/client.py:52, der Aufloesungs-/Verbindungsfehler kommt als `httpx.ConnectError` bzw. `httpx.TimeoutException` aus dem Client. Es sind zwei Typen — aber kein gemeinsamer Basistyp und kein `retryable`-Diskriminator; grep -rnE 'class \w*(Egress|Blocked|Policy|Resolve)\w*(Error|Exception)' src/ liefert 0 Treffer, es gibt keine eigene Fehlertaxonomie
- BEFUND, gemessen: die beiden Lagen laufen vor der Ausgabe wieder zusammen. `_handle_error` (src/eth_library_mcp/formatting.py:112-162) behandelt `httpx.HTTPStatusError`, `httpx.TimeoutException` und `httpx.ConnectError` einzeln und faengt alles uebrige im Schlusszweig (Zeilen 158-162). LAUFZEITMESSUNG: `_handle_error(PermissionError("Egress denied: host 'evil.example' not in ALLOWED_EGRESS_HOSTS"), 'Suche')` -> «Fehler bei Suche: Unbekannter Fehler. Bitte spaeter erneut versuchen.» — identisch mit dem Ergebnis fuer `ValueError('boom')`
- Damit verletzt der deterministische Fall die Umkehrung von Kriterium 3: die Meldung nennt weder die Egress-Policy noch die Allow-List und gibt stattdessen einen WIEDERHOLUNGSRAT («Bitte spaeter erneut versuchen») fuer eine Absage, die bei jedem Versuch gleich ausfaellt. Fuer das Modell liest sich eine Konfigurationsentscheidung wie eine Stoerung
- NEGATIVE KONTROLLE derselben Messung: der transiente Fall wird sehr wohl unterschieden — `httpx.ConnectError` -> «Verbindungsfehler. Internetverbindung pruefen.», `httpx.TimeoutException` -> «Zeitueberschreitung. ETH-Bibliothek API nicht erreichbar.». `_handle_error` ist also nicht durchgehend generisch; es fehlt genau der Zweig fuer den Policy-Verstoss
- Kriterium 4 verletzt: jeder Tool-Handler faengt mit `except Exception as e` und reicht an `_handle_error` weiter (server.py:324-327, 384-387, 474-477, 573-576, 678-681). Das ist das Sammel-`except`, das die Typen zusammenfuehrt
- Kriterium 5 verletzt, und der vorhandene Test pinnt den Zustand fest: tests/test_tools.py:195-203 (`test_egress_blocked_for_unknown_host`) akzeptiert ausdruecklich `"Unbekannter Fehler" in out or "Egress denied" in out`. Der Test bleibt gruen, wenn die beiden Lagen zusammenfallen — er kann die Unterscheidung nicht widerlegen. Einen Test fuer den transienten Fall mit Wiederholung gibt es nicht

### Expected Behavior

Die Pass-Kriterien stehen in `checks/SEC-028.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- Die Typen sind intern verschieden (Kriterium 1, halb erfuellt): der Policy-Verstoss ist `PermissionError` aus src/eth_library_mcp/client.py:52, der Aufloesungs-/Verbindungsfehler kommt als `httpx.ConnectError` bzw. `httpx.TimeoutException` aus dem Client. Es sind zwei Typen — aber kein gemeinsamer Basistyp und kein `retryable`-Diskriminator; grep -rnE 'class \w*(Egress|Blocked|Policy|Resolve)\w*(Error|Exception)' src/ liefert 0 Treffer, es gibt keine eigene Fehlertaxonomie
- BEFUND, gemessen: die beiden Lagen laufen vor der Ausgabe wieder zusammen. `_handle_error` (src/eth_library_mcp/formatting.py:112-162) behandelt `httpx.HTTPStatusError`, `httpx.TimeoutException` und `httpx.ConnectError` einzeln und faengt alles uebrige im Schlusszweig (Zeilen 158-162). LAUFZEITMESSUNG: `_handle_error(PermissionError("Egress denied: host 'evil.example' not in ALLOWED_EGRESS_HOSTS"), 'Suche')` -> «Fehler bei Suche: Unbekannter Fehler. Bitte spaeter erneut versuchen.» — identisch mit dem Ergebnis fuer `ValueError('boom')`
- Damit verletzt der deterministische Fall die Umkehrung von Kriterium 3: die Meldung nennt weder die Egress-Policy noch die Allow-List und gibt stattdessen einen WIEDERHOLUNGSRAT («Bitte spaeter erneut versuchen») fuer eine Absage, die bei jedem Versuch gleich ausfaellt. Fuer das Modell liest sich eine Konfigurationsentscheidung wie eine Stoerung
- NEGATIVE KONTROLLE derselben Messung: der transiente Fall wird sehr wohl unterschieden — `httpx.ConnectError` -> «Verbindungsfehler. Internetverbindung pruefen.», `httpx.TimeoutException` -> «Zeitueberschreitung. ETH-Bibliothek API nicht erreichbar.». `_handle_error` ist also nicht durchgehend generisch; es fehlt genau der Zweig fuer den Policy-Verstoss
- Kriterium 4 verletzt: jeder Tool-Handler faengt mit `except Exception as e` und reicht an `_handle_error` weiter (server.py:324-327, 384-387, 474-477, 573-576, 678-681). Das ist das Sammel-`except`, das die Typen zusammenfuehrt
- Kriterium 5 verletzt, und der vorhandene Test pinnt den Zustand fest: tests/test_tools.py:195-203 (`test_egress_blocked_for_unknown_host`) akzeptiert ausdruecklich `"Unbekannter Fehler" in out or "Egress denied" in out`. Der Test bleibt gruen, wenn die beiden Lagen zusammenfallen — er kann die Unterscheidung nicht widerlegen. Einen Test fuer den transienten Fall mit Wiederholung gibt es nicht

### Gaps

- Kriterium 2 unerfuellt: es gibt gar keine Retry-Politik im Code — grep -rniE 'retry|backoff|max_attempts|tenacity' src/ liefert 0 Treffer, `_http_get` (client.py:55-85) versucht genau einmal. Die faktische Wiederholungsentscheidung faellt damit beim aufrufenden Modell, gesteuert durch den Meldungstext — genau die Steuerung ueber Prosa, die der Check als untauglich benennt
- Behebung in einem Schritt: einen eigenen Typ (z.B. `EgressPolicyViolation(PermissionError)` mit `retryable = False`) in client.py einfuehren und in `_handle_error` vor dem Schlusszweig einen `isinstance`-Zweig ergaenzen, der den geblockten Host nennt und keinen Wiederholungsrat gibt. Dazu die Gegenprobe des Checks: beide Typen testweise wieder zusammenlegen — beide Tests muessen fallen
- tests/test_tools.py:203 ist mit zu ergaenzen: die `or`-Verknuepfung macht die Zusicherung heute unwiderlegbar
- Anzumerken: der Policy-Verstoss wird immerhin strukturiert protokolliert (`log.error('unhandled_exception', exc_type='PermissionError', exc='Egress denied: …')`, formatting.py:161) — der Betreiber kann ihn im stderr-Log finden. Nur der Aufrufer kann es nicht

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/SEC-028.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.


---

## 6. Remediation-Plan

### Empfohlene Reihenfolge

1. **ARCH-005** (critical, partial)
2. **FID-001** (critical, fail)
3. **SEC-004** (critical, partial)
4. **SEC-019** (critical, partial)
5. **ARCH-004** (high, partial)
6. **ARCH-009** (high, partial)
7. **ARCH-013** (high, partial)
8. **ARCH-016** (high, partial)
9. **DRIFT-002** (high, partial)
10. **DRIFT-003** (high, fail)
11. **DRIFT-004** (high, partial)
12. **DRIFT-008** (high, partial)
13. **FID-002** (high, fail)
14. **FID-003** (high, fail)
15. **FID-006** (high, fail)
16. **FID-007** (high, fail)
17. **IDENT-006** (high, partial)
18. **IDENT-007** (high, partial)
19. **OBS-001** (high, partial)
20. **OBS-002** (high, partial)
21. **OPS-001** (high, partial)
22. **OPS-003** (high, partial)
23. **OPS-004** (high, partial)
24. **OPS-005** (high, partial)
25. **OPS-009** (high, partial)
26. **OPS-010** (high, fail)
27. **SCALE-009** (high, partial)
28. **SEC-003** (high, partial)
29. **SEC-005** (high, partial)
30. **SEC-007** (high, partial)
31. **SEC-018** (high, partial)
32. **SEC-021** (high, partial)
33. **SEC-024** (high, partial)
34. **SEC-028** (high, fail)
35. **ARCH-001** (medium, partial)
36. **ARCH-002** (medium, fail)
37. **ARCH-003** (medium, fail)
38. **ARCH-007** (medium, partial)
39. **ARCH-011** (medium, partial)
40. **ARCH-012** (medium, partial)
41. **ARCH-018** (medium, partial)
42. **ARCH-019** (medium, partial)
43. **ARCH-020** (medium, partial)
44. **ARCH-021** (medium, partial)
45. **ARCH-022** (medium, partial)
46. **DRIFT-001** (medium, partial)
47. **DRIFT-006** (medium, fail)
48. **FID-004** (medium, partial)
49. **FID-005** (medium, partial)
50. **IDENT-002** (medium, fail)
51. **IDENT-003** (medium, partial)
52. **OBS-003** (medium, partial)
53. **OBS-007** (medium, partial)
54. **OBS-008** (medium, partial)
55. **OPS-002** (medium, partial)
56. **OPS-007** (medium, partial)
57. **SCALE-010** (medium, partial)
58. **SDK-002** (medium, partial)
59. **SDK-003** (medium, partial)
60. **IDENT-004** (low, partial)

---

## 7. Audit-Metadata

| Feld | Wert |
|---|---|
| skill_version | `2.3.0` |
| policy | `fail-or-partial` |


_Generated by tools/build_report.py — do not edit by hand._
