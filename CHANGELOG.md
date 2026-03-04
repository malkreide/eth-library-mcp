# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier dokumentiert.
Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

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
