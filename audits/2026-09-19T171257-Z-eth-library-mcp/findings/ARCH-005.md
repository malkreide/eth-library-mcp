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
