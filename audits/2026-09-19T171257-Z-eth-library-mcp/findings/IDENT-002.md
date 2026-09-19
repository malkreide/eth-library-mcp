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
