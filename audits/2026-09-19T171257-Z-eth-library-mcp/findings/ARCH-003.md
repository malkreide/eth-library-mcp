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
