# Testplan: eth-library-mcp

## Zusammenfassung

Dieses Dokument beschreibt den vollstandigen Testplan fur den ETH Library MCP Server.
Der Server besteht aus 2 Quelldateien (~1'181 Zeilen), 7 MCP-Tools, 2 Resources,
2 Prompts und nutzt 2 externe APIs.

**Testframework:** pytest + pytest-asyncio (bereits als Dev-Dependencies definiert)
**Gesamtanzahl Testfalle:** 84

---

## Teststruktur

```
tests/
  conftest.py                    # Shared fixtures (Mock-API-Responses, httpx mock client)
  test_api_client.py             # Unit-Tests fur api_client.py
  test_input_validation.py       # Pydantic-Model-Validierung
  test_tools.py                  # Tool-Funktionen mit gemockter API
  test_server_config.py          # Server-Konfiguration, Resources, Prompts
  test_error_handling.py         # Fehlerbehandlung & Edge Cases
  test_integration.py            # Optionale Integration-Tests (echte API)
```

---

## Kategorie 1: api_client.py - Hilfsfunktionen (14 Tests)

### 1.1 `get_api_key()` (3 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 1 | API-Key gesetzt | `ETH_LIBRARY_API_KEY=test123` | Gibt `"test123"` zuruck | `monkeypatch.setenv()`, Ruckgabewert prufen |
| 2 | API-Key nicht gesetzt | Env-Variable nicht vorhanden | Gibt `None` zuruck | `monkeypatch.delenv()`, Ruckgabewert prufen |
| 3 | API-Key leer | `ETH_LIBRARY_API_KEY=""` | Gibt `""` zuruck | `monkeypatch.setenv()`, Ruckgabewert prufen |

### 1.2 `eth_api_request()` (5 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 4 | Erfolgreicher Request | Gultiger Endpunkt, Mock 200 | JSON-Dict zuruckgegeben | `httpx.AsyncClient` mocken mit `respx` oder `unittest.mock.patch` |
| 5 | API-Key wird angehangt | Key gesetzt + Request | `apikey`-Param im Request | Mock pruft gesendete Query-Parameter |
| 6 | Kein API-Key | Key nicht gesetzt | Request ohne `apikey`-Param | Mock pruft, dass kein `apikey` gesendet wird |
| 7 | Timeout | Langsamer Server | Wirft `httpx.TimeoutException` | Mock wirft TimeoutException |
| 8 | HTTP-Fehler | Mock 500 Response | Wirft `httpx.HTTPStatusError` | Mock gibt Status 500 zuruck |

### 1.3 `format_resource_summary()` (3 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 9 | Vollstandiges Dokument | Doc mit allen Feldern | Markdown mit Titel, Autor, Jahr, Typ, MMS-ID | String-Assertions auf Ruckgabewert |
| 10 | Minimales Dokument | Doc nur mit Titel | Markdown ohne Fehler, fehlende Felder leer | String enthalt Titel, keine Exception |
| 11 | Leeres Dokument | Leeres Dict `{}` | Kein Absturz, leere/Standard-Werte | Keine Exception, Ruckgabewert ist String |

### 1.4 `format_resource_detail()` (3 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 12 | Vollstandiges Dokument | Doc mit allen Metadaten | Detailliertes Markdown mit allen Feldern | Prufe Titel, ISBN, DOI, Subjects etc. im Output |
| 13 | Subjects > 10 | Doc mit 15 Subjects | Nur erste 10 angezeigt | Zahle Subject-Eintrage im Output |
| 14 | Beschreibung > 500 Zeichen | Doc mit langer Description | Abgeschnitten auf 500 Zeichen | `len()` auf Description-Teil prufen |

---

## Kategorie 2: Input-Validierung / Pydantic-Modelle (21 Tests)

### 2.1 `SearchResourcesInput` (6 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 15 | Gultige Minimalanfrage | `query="any,contains,test"` | Modell wird erstellt | Pydantic-Konstruktor, kein Fehler |
| 16 | Alle Parameter | Alle Felder gesetzt | Modell wird erstellt | Alle Felder setzen, Werte prufen |
| 17 | Query zu lang | 501 Zeichen | `ValidationError` | `pytest.raises(ValidationError)` |
| 18 | Query leer | `query=""` | `ValidationError` | `pytest.raises(ValidationError)` |
| 19 | Ungultiger Sort | `sort="invalid"` | `ValidationError` | `pytest.raises(ValidationError)` |
| 20 | Ungultiger ResourceType | `resource_type="xyz"` | `ValidationError` | `pytest.raises(ValidationError)` |

### 2.2 `GetResourceInput` (4 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 21 | Gultige MMS-ID | `mmsid="990075811280205503"` | Modell wird erstellt | Pydantic-Konstruktor |
| 22 | MMS-ID zu kurz | `mmsid="12"` | `ValidationError` | `pytest.raises(ValidationError)` |
| 23 | MMS-ID zu lang | 51 Zeichen | `ValidationError` | `pytest.raises(ValidationError)` |
| 24 | Unbekanntes Feld | `extra_field="x"` | `ValidationError` (extra="forbid") | `pytest.raises(ValidationError)` |

### 2.3 `SearchArchiveInput` (3 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 25 | Gultiges Archiv | `archive="ETH_Bildarchiv"` | Modell wird erstellt | Pydantic-Konstruktor |
| 26 | Ungultiges Archiv | `archive="FAKE_Archive"` | `ValidationError` | `pytest.raises(ValidationError)` |
| 27 | Limit uber Maximum | `limit=101` | `ValidationError` | `pytest.raises(ValidationError)` |

### 2.4 `SearchByTypeInput` (2 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 28 | Gultiger Typ | `resource_type="maps"` | Modell wird erstellt | Pydantic-Konstruktor |
| 29 | Negativer Offset | `offset=-1` | `ValidationError` | `pytest.raises(ValidationError)` |

### 2.5 `SearchPersonsInput` (3 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 30 | Gultige Anfrage | `query="Einstein"` | Modell wird erstellt | Pydantic-Konstruktor |
| 31 | Query zu kurz | `query="A"` (1 Zeichen, min=2) | `ValidationError` | `pytest.raises(ValidationError)` |
| 32 | Limit uber 50 | `limit=51` | `ValidationError` | `pytest.raises(ValidationError)` |

### 2.6 `SearchEducationInput` (3 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 33 | Gultiges Topic | `topic="Volksschule Zurich"` | Modell wird erstellt | Pydantic-Konstruktor |
| 34 | Topic zu kurz | `topic="A"` (1 Zeichen, min=2) | `ValidationError` | `pytest.raises(ValidationError)` |
| 35 | Topic zu lang | 301 Zeichen | `ValidationError` | `pytest.raises(ValidationError)` |

---

## Kategorie 3: Tool-Funktionen mit Mock-API (28 Tests)

### 3.1 `eth_search_resources` (6 Tests)

| # | Testfall | Setup | Erwartetes Ergebnis | Wie testen |
|---|---------|-------|---------------------|------------|
| 36 | Erfolgreiche Suche | Mock: 3 Docs, total=3 | Markdown mit 3 Ergebnissen | `async` call, Ruckgabe-String prufen |
| 37 | Keine Ergebnisse | Mock: 0 Docs, total=0 | Hilfreiche "keine Ergebnisse"-Meldung | String enthalt Hinweis auf breitere Suche |
| 38 | Paginierung | Mock: total=50, limit=10 | Paginierungshinweis im Output | String enthalt Offset-Hinweis |
| 39 | Open-Access-Filter | `open_access_only=True` | `qInclude` enthalt `open_access` | Mock pruft gesendete Parameter |
| 40 | Sprach-Filter | `language="de"` | `qInclude` enthalt `facet_lang` | Mock pruft gesendete Parameter |
| 41 | API-Fehler | Mock wirft Exception | Fehler-String zuruckgegeben | Ruckgabe ist Fehlermeldung, kein Crash |

### 3.2 `eth_get_resource` (5 Tests)

| # | Testfall | Setup | Erwartetes Ergebnis | Wie testen |
|---|---------|-------|---------------------|------------|
| 42 | Erfolgreicher Abruf | Mock: vollstandiges Doc | Detailliertes Markdown | Prufe alle Metadaten-Felder |
| 43 | Mit Verfugbarkeit | `include_availability=True` | `avail=true` im Request | Mock pruft Parameter |
| 44 | Ohne Verfugbarkeit | `include_availability=False` | `avail=false` im Request | Mock pruft Parameter |
| 45 | Nicht gefunden (404) | Mock: HTTPStatusError 404 | "MMS-ID prufen"-Meldung | String enthalt MMS-ID-Hinweis |
| 46 | Response ohne `docs`-Wrapper | Mock: Doc direkt (ohne `docs` Array) | Funktioniert trotzdem | Ruckgabe enthalt Titel |

### 3.3 `eth_search_archive` (4 Tests)

| # | Testfall | Setup | Erwartetes Ergebnis | Wie testen |
|---|---------|-------|---------------------|------------|
| 47 | Erfolgreiche Archivsuche | Mock: 2 Docs | Markdown mit Archiv-Header | String enthalt Archivnamen |
| 48 | Leeres Archiv | Mock: 0 Docs | "Keine Ergebnisse"-Meldung | Hilfreiche Meldung |
| 49 | Facet-Filter korrekt | `archive="ETH_Bildarchiv"` | `qInclude` enthalt `facet_data_source` | Mock pruft Parameter |
| 50 | Standard-Query | Kein `query` angegeben | Default `any,contains,"*"` wird verwendet | Mock pruft `q`-Parameter |

### 3.4 `eth_search_by_type` (4 Tests)

| # | Testfall | Setup | Erwartetes Ergebnis | Wie testen |
|---|---------|-------|---------------------|------------|
| 51 | Erfolgreiche Typ-Suche | Mock: 5 Docs, type=maps | Markdown mit Typ-Label | String enthalt "Karten / Maps" |
| 52 | Mit Open-Access | `open_access_only=True` | Beide Facets in qInclude | Mock pruft Parameter |
| 53 | Paginierung | Mock: total=100, limit=20 | Paginierungshinweis | String enthalt Offset-Hinweis |
| 54 | Leere Ergebnisse | Mock: 0 Docs | Hilfreiche Meldung | String enthalt Hinweis |

### 3.5 `eth_search_persons` (5 Tests)

| # | Testfall | Setup | Erwartetes Ergebnis | Wie testen |
|---|---------|-------|---------------------|------------|
| 55 | Erfolgreiche Suche | Mock: 2 Personen | Markdown mit Namen, Daten | String enthalt Personennamen |
| 56 | Mit Wikidata-Links | Mock: Person mit Wikidata-URL | Link im Output | String enthalt Wikidata-URL |
| 57 | Leere Ergebnisse | Mock: leere Liste | "Keine Personen"-Meldung | Hilfreiche Meldung |
| 58 | 404-Fehler (BUG-02) | Mock: HTTPStatusError 404 | Fehlermeldung (Endpunkt) | String enthalt Endpunkt-Hinweis |
| 59 | Alternative Response-Keys | Mock: `{"hits": [...]}` | Personen korrekt geparst | `parse_persons_response()` |

### 3.6 `eth_search_education` (4 Tests)

| # | Testfall | Setup | Erwartetes Ergebnis | Wie testen |
|---|---------|-------|---------------------|------------|
| 60 | Erfolgreiche Suche | Mock: 3 Docs | Markdown mit Bildungs-Ergebnissen | String enthalt Topic |
| 61 | Mit Typ-Filter | `resource_type="books"` | Facet-Filter enthalt books | Mock pruft Parameter |
| 62 | Nur Open Access | `open_access_only=True` | OA-Facet gesetzt | Mock pruft Parameter |
| 63 | Paginierungshinweis | Mock: total > limit | Verweis auf eth_search_resources | String enthalt Hinweis |

---

## Kategorie 4: parse_persons_response() (6 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 64 | Direkte Liste | `[{"name": "A"}, {"name": "B"}]` | Liste mit 2 Personen | Prufe Lange und Inhalt |
| 65 | Wrapper `persons` | `{"persons": [...]}` | Korrekt entpackt | Prufe Lange |
| 66 | Wrapper `results` | `{"results": [...]}` | Korrekt entpackt | Prufe Lange |
| 67 | Wrapper `data` | `{"data": [...]}` | Korrekt entpackt | Prufe Lange |
| 68 | Wrapper `items` | `{"items": [...]}` | Korrekt entpackt | Prufe Lange |
| 69 | Unbekannte Struktur | `{"unknown_key": [...]}` | Leere Liste + Warning-Log | Prufe Ruckgabe `[]`, prufe Log |

---

## Kategorie 5: Fehlerbehandlung - handle_api_error() (8 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 70 | HTTP 401 | HTTPStatusError(401) | "API-Key"-Hinweis | String enthalt "API-Key" oder "developer.library.ethz.ch" |
| 71 | HTTP 403 | HTTPStatusError(403) | "Zugriff verweigert" | String enthalt "403" |
| 72 | HTTP 404 (Suche) | HTTPStatusError(404), `is_search=True` | "Endpunkt/Query prufen" | String enthalt Such-Hinweis |
| 73 | HTTP 404 (ID) | HTTPStatusError(404), `is_search=False` | "MMS-ID prufen" | String enthalt ID-Hinweis |
| 74 | HTTP 429 | HTTPStatusError(429) | "Rate-Limit" | String enthalt "Rate-Limit" |
| 75 | HTTP 500 | HTTPStatusError(500) | "HTTP-Fehler 500" | String enthalt Status-Code |
| 76 | Timeout | TimeoutException | "Timeout" | String enthalt "Timeout" |
| 77 | Connection Error | ConnectError | "Verbindungsfehler" | String enthalt Verbindungs-Hinweis |

---

## Kategorie 6: Server-Konfiguration, Resources & Prompts (7 Tests)

### 6.1 Server-Start & Konfiguration (3 Tests)

| # | Testfall | Setup | Erwartetes Ergebnis | Wie testen |
|---|---------|-------|---------------------|------------|
| 78 | `eth_library_info` mit Key | `ETH_LIBRARY_API_KEY` gesetzt | "Konfiguriert" im Output | `monkeypatch.setenv()` |
| 79 | `eth_library_info` ohne Key | Key nicht gesetzt | "Nicht gesetzt" + Registrierungslink | `monkeypatch.delenv()` |
| 80 | Server-Name korrekt | - | Name ist "eth_library_mcp" | MCP-Server-Instanz prufen |

### 6.2 MCP Resources (2 Tests)

| # | Testfall | Erwartetes Ergebnis | Wie testen |
|---|---------|---------------------|------------|
| 81 | `eth://resource-types` | JSON mit 10 Resource-Types | Resource-Handler aufrufen, JSON parsen |
| 82 | `eth://archives` | JSON mit 5 Archiven | Resource-Handler aufrufen, JSON parsen |

### 6.3 MCP Prompts (2 Tests)

| # | Testfall | Eingabe | Erwartetes Ergebnis | Wie testen |
|---|---------|---------|---------------------|------------|
| 83 | `research-workflow` | `topic="Quantenphysik"` | Workflow-Text mit Topic | Prompt-Handler aufrufen, String prufen |
| 84 | `education-research` | `topic="Volksschule"` | Bildungs-Workflow mit Topic | Prompt-Handler aufrufen, String prufen |

---

## Optionale Integrationstests (mit echter API)

Diese Tests werden nur ausgefuhrt, wenn `ETH_LIBRARY_API_KEY` gesetzt ist.
Sie sind mit `@pytest.mark.integration` markiert und werden mit
`pytest -m integration` ausgefuhrt.

| # | Testfall | Beschreibung |
|---|---------|-------------|
| I-1 | Einfache Suche | `eth_search_resources(query="any,contains,Einstein")` gibt Ergebnisse |
| I-2 | Resource abrufen | `eth_get_resource(mmsid=bekannte_id)` gibt Metadaten |
| I-3 | Archivsuche | `eth_search_archive(archive="ETH_Bildarchiv")` gibt Ergebnisse |
| I-4 | Typ-Suche | `eth_search_by_type(resource_type="books", query="any,contains,Zurich")` |
| I-5 | Bildungssuche | `eth_search_education(topic="Padagogik")` gibt Ergebnisse |

---

## Testausfuhrung

```bash
# Dev-Dependencies installieren
pip install -e ".[dev]"

# Alle Unit-Tests ausfuhren
pytest tests/ -v

# Nur eine Kategorie
pytest tests/test_api_client.py -v
pytest tests/test_input_validation.py -v
pytest tests/test_tools.py -v
pytest tests/test_error_handling.py -v

# Mit Coverage
pytest tests/ --cov=eth_library_mcp --cov-report=term-missing

# Integrationstests (benotigt API-Key)
ETH_LIBRARY_API_KEY=dein-key pytest tests/test_integration.py -m integration -v
```

---

## Mock-Strategie

### Warum Mocking?

- Die ETH Library API ist eine externe Abhangigkeit
- Rate-Limits und Verfugbarkeit konnen Tests unzuverlassig machen
- Unit-Tests mussen schnell und deterministisch sein

### Wie mocken?

1. **`unittest.mock.AsyncMock`** fur `eth_api_request()` - alle Tool-Tests mocken
   diese zentrale Funktion
2. **`monkeypatch.setenv/delenv`** fur Umgebungsvariablen (API-Key, Transport)
3. **`httpx.MockTransport`** oder **`respx`** fur HTTP-Level-Tests von
   `eth_api_request()` selbst
4. **Fixture `sample_doc`** in `conftest.py` - wiederverwendbare API-Response-
   Strukturen fur konsistente Tests

### Beispiel conftest.py Fixture

```python
@pytest.fixture
def sample_doc():
    """Realistische API-Response-Struktur fur einen einzelnen Eintrag."""
    return {
        "pnx": {
            "display": {
                "title": ["Quantenphysik fur Anfanger"],
                "creator": ["Einstein, Albert"],
                "creationdate": ["1925"],
                "type": ["book"],
                "language": ["ger"],
                "publisher": ["Springer"],
                "subject": ["Physik", "Quantenmechanik"],
                "description": ["Ein Lehrbuch..."],
            },
            "addata": {
                "doi": ["10.1234/example"],
                "isbn": ["978-3-123456-78-9"],
            },
        },
        "delivery": {
            "link": [
                {"linkURL": "https://example.com/fulltext", "linkType": "http"}
            ]
        },
        "context": {"mmsId": "990075811280205503"},
    }


@pytest.fixture
def sample_search_response(sample_doc):
    """Mock-Antwort fur eine Suchanfrage."""
    return {
        "docs": [sample_doc],
        "info": {"total": 1},
    }
```

---

## Ubersicht nach Testdatei

| Datei | Anzahl Tests | Beschreibung |
|-------|-------------|-------------|
| `test_api_client.py` | 14 | Hilfsfunktionen: get_api_key, eth_api_request, format_* |
| `test_input_validation.py` | 21 | Pydantic-Modell-Validierung fur alle 6 Input-Klassen |
| `test_tools.py` | 28 | Tool-Funktionen mit gemockter API |
| `test_error_handling.py` | 8 | handle_api_error() mit allen Fehlertypen |
| `test_server_config.py` | 7 | Server-Info, Resources, Prompts |
| `test_parse_persons.py` | 6 | parse_persons_response() Varianten |
| **Gesamt** | **84** | |
| `test_integration.py` | 5 | Optional, mit echter API |
