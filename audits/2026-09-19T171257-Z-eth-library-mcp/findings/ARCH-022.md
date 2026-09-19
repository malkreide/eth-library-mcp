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
