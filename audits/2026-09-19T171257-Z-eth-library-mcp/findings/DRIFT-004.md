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
