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
