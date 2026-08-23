# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier dokumentiert.
Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

---

## [Unreleased]

### Behoben

- **Browser-Clients scheiterten am Preflight.** Spec `2026-07-28` routet eine
  Streamable-HTTP-Anfrage über `Mcp-Method`, `Mcp-Name` und
  `Mcp-Protocol-Version`; die CORS-Freigabeliste nannte keinen davon, dafür mit
  `Mcp-Session-Id` den Session-Header, der für sich genommen keine Anfrage
  routet. Ein Browser darf einen nicht safelisteten Header nicht senden, wenn
  der Server ihn nicht nennt: die Anfrage starb vor dem ersten MCP-Byte,
  während stdio und Python weiterliefen. Deshalb war nichts rot.

### Hinzugefügt

- **`build_http_app()`**, herausgezogen aus `_run_http`, damit die CORS-Schicht
  überhaupt prüfbar ist. `_run_http` ruft die neue Funktion auf; am Verhalten
  ändert sich nichts.

- **Frischehinweise auf den auflistenden Methoden** (SEP-2549, Spec
  `2026-07-28`): `tools/list`, `resources/list`, `resources/templates/list`,
  `prompts/list` und `server/discover` antworten mit `ttlMs` 300000 und
  `cacheScope` `public`. `resources/read` und `prompts/get` bleiben ohne
  Hinweis: das wäre eine Zusicherung über den Inhalt statt über das Verzeichnis.

- **Protokoll-Gate: beide Spec-Aeren gepinnt und geprueft**
  (`tests/test_protocol_version.py`). `mcp` 2.x bedient zwei Aeren ueber
  denselben Server — den `initialize`-Handshake, der bei `2025-11-25`
  deckelt, und den Pro-Request-Envelope, der `2026-07-28` erreicht.
  `LATEST_PROTOCOL_VERSION` ist ein Alias auf die **moderne** Aera; wer nur
  dagegen pinnt, laesst genau die Aera frei wandern, die heutige Clients
  aushandeln. Beide sind jetzt einzeln gepinnt, ein Dependabot-Bump von
  `mcp` kann keine davon still verschieben.

  Nachgemessen statt aus Konstantennamen geschlossen: ein echter `initialize`
  durch den zusammengebauten ASGI-Stack. Ein Client, der ueber den Handshake
  nach `2026-07-28` fragt, bekommt `2025-11-25` zurueck.

  Beide READMEs beschreiben die Aeren; ein Test haelt jede Sprache einzeln
  dagegen — im Portfolio sind EN und DE desselben Repos schon dreimal
  auseinandergelaufen, weil nur eine Fassung nachgezogen wurde.

- **`Mcp-Session-Id` ist weiterhin freigegeben — und das steht jetzt in einem
  Test statt in einem Satz.** Der Docstring von `tests/test_cors.py` nannte den
  Header die Spur einer Mechanik, die `2026-07-28` abgeschafft habe. Das stimmt
  nicht: `mcp` 2.x bedient beide Protokoll-Aeren, die Session gehoert zur
  Handshake-Aera, und der Server gibt den Header nicht ohne Grund auch in
  `expose_headers` frei.

  Nachgemessen statt aus Spec-Text geschlossen: `MCP_SESSION_ID_HEADER` steht
  unveraendert in `mcp/server/streamable_http.py`, und ein echter `initialize`
  durch den zusammengebauten ASGI-Stack bekommt eine Session-ID im
  Antwort-Header zurueck.

  `test_der_session_header_ist_weiterhin_freigegeben` haelt beides fest. Die
  Gegenprobe zeigt, dass es die Luecke wirklich gab: nimmt man den Header aus
  der Freigabeliste, faellt genau dieser eine Test, und die sieben bestehenden
  bleiben gruen.

### Behoben — BUG-02 ist erledigt, durch Entfernen des Werkzeugs

Im Code und in beiden READMEs stand seit laengerem dieselbe Notiz:

> ⚠ BUG-02: Der Persons-API-Endpunkt (`/persons/v1/persons`) gibt aktuell HTTP
> 404 zurueck. Die korrekte URL muss via `developer.library.ethz.ch`
> verifiziert werden.

Verifiziert ist sie jetzt, und **es gibt keine korrekte URL**. Die Persons-API
ist vom Gateway verschwunden, nicht bloss verschlossen.

Entscheiden laesst sich das ohne API-Key, weil das Gateway **vor** der
Schluesselpruefung routet:

| Pfad | Antwort ohne Key | heisst |
|---|---|---|
| `/discovery/v1/resources` | **401** | Route da, Schluessel fehlt |
| `/discovery/v1/resources/991` | **401** | auch Unterpfade |
| `/discovery/v1/<erfunden>` — KONTROLLE | **404** | Route nicht da |
| `/persons/v1/persons` | **404** | |
| `/persons/v1` | **404** | |
| `/persons/v2/persons` — KONTROLLE | **404** | |

Die beiden Kontrollzeilen sind der ganze Punkt. Ohne sie belegt die Messung
nur, dass jemand einen 404 bekommen hat — mit ihnen belegt sie, was das Gateway
unterscheidet. Genau diesen Unterschied, die eigene Adressliste gegen den
Bestand der Quelle, hat dieses Portfolio schon zweimal verwechselt.

`eth_search_persons` ist deshalb **entfernt** und nicht mit einer schoeneren
Fehlermeldung versehen worden. Eine Faehigkeit anzubieten, die es nicht geben
kann, ist derselbe Fehler wie ein leeres Ergebnis, nur lauter — und das Werkzeug
stand mit Warnhinweis in der Werkzeugliste, also dort, wo ein Modell zuerst
hinsieht. Mit ihm fallen `SearchPersonsInput`, der Persons-Parser-Aufruf und die
Zaehlung «7 Tools · 3 APIs» weg, die auf beiden READMEs stand. Es sind sechs
Werkzeuge und eine API.

### Hinzugefuegt — aufgezeichnet wird der Vertrag, nicht die Antwort

**`scripts/record_fixtures.py`** zeichnet auf, was ohne Schluessel aufzeichenbar
ist: die Routen-Erhebung samt Kontrollen, mit Datum und SHA-256 in
`tests/fixtures/PROVENANCE.md`.

Die Discovery-Payloads bleiben **NICHT aufgezeichnet** — die API verlangt einen
Schluessel, und ein Datum anzuschreiben, das sie nie hatten, waere schlimmer als
die Luecke. Die 401 ist dabei am Pfad des Servers selbst gemessen, nicht an
einem benachbarten, und die Kontrollen zeigen, dass sie «Schluessel fehlt»
heisst und nicht «Route weg».

Das Skript bricht ab, wenn die Unterscheidung nicht mehr traegt: wenn Discovery
nicht mehr mit 401 antwortet, wenn ein erfundener Pfad nicht mehr 404 gibt, oder
wenn die Personen-API zurueckkommt — im letzten Fall gehoert das Werkzeug
wiederhergestellt und nicht die Fixture nachgezogen.

**`tests/fixture_data.py`** behandelt einen fehlenden Namen als Fehler statt als
leere Struktur.

### Hinzugefuegt — die ersten Live-Tests dieses Repositoriums

`pytest -m live` sammelte hier bisher **null** Tests ein. Nichts in diesem Repo
war je gegen die Quelle gehalten worden — bei 11 Inline-Payloads, dem groessten
Wert der unteren Haelfte der Portfolio-Rangfolge.

Die zwei neuen Live-Tests brauchen **keinen** API-Key und sagen trotzdem etwas:
Sie melden, wenn die Personen-API zurueckkommt (dann gehoert das Werkzeug wieder
her) und wenn Discovery seine Route verliert (dann sind fuenf Werkzeuge
betroffen). Ein Live-Test, der nur mit Zugangsdaten laeuft, laeuft in der Praxis
nie.

---

## [0.3.4] – 2026-07-31

### Hinzugefuegt

- **Der Server nennt jetzt seinen Namen.** Bisher ging gegenueber jedem
  Upstream der httpx-Default hinaus: der Betreiber der Datenquelle sah
  eine Bibliothek, nicht uns, und hatte keinen Weg, uns bei Fehlverhalten
  zu erreichen. Neu traegt jeden der 2 HTTP-Clients
  `eth-library-mcp/<version> (+github.com/malkreide/eth-library-mcp)`.

  Die Version stammt aus `importlib.metadata` und kann nicht getrennt vom
  Paket driften.

## [0.3.0] – 2026-05-29

Audit-Härtungs-Release. Über drei Remediation-Sprints wurden alle 20 Findings aus dem [mcp-audit-skill](https://github.com/malkreide/mcp-audit-skill)-Audit (run-id `2026-05-28T142641-Z-eth-library-mcp`, 38/68 Checks anwendbar) behoben. Ein Re-Audit (run-id `2026-05-28T184347-Z-eth-library-mcp`, identischer Catalog-Hash `091f446b…`) bestätigt: 36/36 anwendbare Checks PASS, 0 Findings, Production-Readiness erreicht.

### ⚠️ Breaking Changes

- **HTTP-Default-Bind** (`SEC-016`): `python -m eth_library_mcp.server --http` bindet jetzt auf `127.0.0.1` statt `0.0.0.0`. Für Public-Exposure muss `--host 0.0.0.0` explizit übergeben werden — und nur hinter Reverse-Proxy/Firewall. Migration: bestehende Deploy-Skripte um `--host 0.0.0.0` ergänzen oder hinter den Proxy verlagern.

### Hinzugefügt

- **Container-Sandbox** (`SEC-007`): `Dockerfile` (multi-stage, slim-base, non-root UID 1000) + `.dockerignore`. Empfohlene Laufzeit: `--read-only --tmpfs /tmp`.
- **Egress-Allow-List** (`SEC-021`): `ALLOWED_EGRESS_HOSTS` als `frozenset` mit Runtime-Gate in `_http_get`. Jeder Outbound-Call gegen einen nicht gelisteten Host wirft `PermissionError`. Doku: `docs/network-egress.md`.
- **CORS-Middleware** (`SDK-004`): HTTP-Transport wrappt die Starlette-App in `CORSMiddleware`. `Mcp-Session-Id` ist in `allow_headers` und `expose_headers` — Browser-MCP-Clients können den Header lesen.
- **Strukturiertes Logging** (`OBS-003`): `structlog` mit JSON-Output auf stderr. Vier Severity-Stufen aktiv genutzt (debug/info/warning/error). Ingestion via Datadog/CloudWatch/Loki ohne Custom-Parser möglich.
- **FastMCP Lifespan + Connection Pool** (`SDK-001`): `@asynccontextmanager`-Lifespan verwaltet einen geteilten `httpx.AsyncClient`. Spart TLS-Handshake pro Tool-Call.
- **Context-Injection** (`SDK-003`): Alle 6 Such-/Get-Tools akzeptieren `ctx: Context`. `ctx.warning()` auf Error-Pfaden, `ctx.report_progress()` für `limit > 50`, `ctx.info()` für Persons-No-Results.
- **Source-Attribution** (`CH-004`): Jede formatierte Ressource trägt eine `Quelle: ETH-Bibliothek (Public Domain) · …`-Zeile.
- **Tool-Layer-Tests** (`OPS-001`): `tests/test_tools.py` mit `respx`-Mocks deckt alle 7 Tools ab (13 neue Tests, 38 total). Regression-Tests für OBS-002 (kein Body-Leak) und SEC-021 (Egress-Block).
- **Stderr-Logging explizit** (`OBS-004`): `logging.basicConfig(stream=sys.stderr)` + `structlog.PrintLoggerFactory(file=sys.stderr)`. stdio JSON-RPC-stdout bleibt sauber.
- **Doku**: `docs/ARCHITECTURE.md`, `docs/data-sources.md`, `docs/network-egress.md`, `docs/scope-minimization.md`, `docs/secret-management.md`.
- **`.gitignore`** und **`.env.example`** (`ARCH-005`): Verhindert versehentliche Secret-Commits.
- **Audit-Artefakte** unter `audits/`: Profil, Verification-Results, Summary, Findings, Reports beider Audit-Läufe.

### Geändert

- **Modul-Split** (`ARCH-004`): `server.py` (1107 LOC) aufgeteilt in `client.py` (httpx + Lifespan + Egress), `formatting.py` (Markdown-Rendering, Error-Mapping), `logging_config.py` (structlog) und `server.py` (898 LOC — nur noch FastMCP-Tools). `server.py` re-exportiert die alten Namen — Import-Pfade bleiben kompatibel.
- **Error-Handling** (`OBS-002`): `_handle_error` leakt keinen Upstream-Response-Body (`e.response.text`) und keinen Exception-Klassennamen mehr an den LLM. Details landen im strukturierten stderr-Log.
- **Versionspinning** (`ARCH-012`): Upper Bounds auf alle Dependencies (`mcp[cli]>=1.0.0,<2.0.0`, `httpx>=0.27.0,<1.0.0`, `pydantic>=2.0.0,<3.0.0`).
- **README**: MCP Protocol Version 2025-06-18 deklariert; Cloud-Deployment-Sektion mit `--host`-Warnung erweitert.

### Sicherheit

| Audit-Check | Vorher | Jetzt |
|---|---|---|
| critical findings | 3 | 0 |
| high findings | 12 | 0 |
| medium findings | 5 | 0 |
| Production-readiness | nein | **ja** |

Vollständige Reports unter `audits/2026-05-28T184347-Z-eth-library-mcp/audit-report.md`.

### Dependencies

- **+** `structlog>=24.0.0,<26.0.0`

---

## [0.2.0] – 2026-03-04

### Behoben
- **BUG-01** `pyproject.toml`: Falscher Package-Pfad `src/eth_library_mcp` → `eth_library_mcp` (Installation via `pip install -e .` schlug fehl)
- **BUG-03** `sort`-Parameter: Beliebige Strings akzeptiert → `Literal["rank","title","author","date"]` (verhindert ungültige API-Anfragen)
- **BUG-04** `resource_type`-Parameter: Beliebige Strings akzeptiert → vollständiger `Literal`-Typ mit allen 10 gültigen Werten (verhindert stille Leerantworten)
- **BUG-06** Persons-Response-Parsing: Nur `persons`/`results`-Keys unterstützt → robustes Parsing mit `data`, `items`, `hits` + Logging bei unbekannter Struktur
- **BUG-07** HTTP-404-Fehlermeldung: Generische "ID prüfen"-Meldung auch bei Suchen → kontext-spezifische Meldungen (`is_search`-Parameter in `handle_api_error`)

### Entfernt
- **BUG-05** Ungenutzte Konstanten `RESEARCH_BASE_URL` und `ETHORAMA_BASE_URL` aus `api_client.py` entfernt

### Bekannte Probleme
- **BUG-02** Persons-API-Endpunkt (`/persons/v1/persons`) gibt HTTP 404 zurück. Die korrekte URL muss via [developer.library.ethz.ch](https://developer.library.ethz.ch) verifiziert werden. Das Tool `eth_search_persons` ist strukturell korrekt implementiert, aber erst nach URL-Verifikation funktionsfähig.

---

## [0.1.0] – 2026-03-01

### Hinzugefügt
- Initiale Implementierung mit 7 Tools, 3 APIs, 2 Resources, 2 Prompts
- Discovery API: `eth_search_resources`, `eth_get_resource`, `eth_search_archive`, `eth_search_by_type`, `eth_search_education`
- Persons API: `eth_search_persons`
- Dual Transport: stdio (lokal) + SSE (Cloud/Render.com)
- Graceful Degradation ohne API-Key (hilfreiche Fehlermeldung mit Registrierungslink)
- Schulamt-spezifisches Tool `eth_search_education` für Bildungsthemen
