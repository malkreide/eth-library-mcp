[🇬🇧 English Version](README.md)

> 🇨🇭 **Teil des [Swiss Public Data MCP Portfolios](https://github.com/malkreide)**

# 🏛️ eth-library-mcp

![Version](https://img.shields.io/badge/version-0.2.0-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple)](https://modelcontextprotocol.io/)
[![Datenquelle](https://img.shields.io/badge/Daten-ETH%20Bibliothek%20Z%C3%BCrich-red)](https://developer.library.ethz.ch)
[![CI](https://github.com/malkreide/eth-library-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/malkreide/eth-library-mcp/actions/workflows/ci.yml)

> MCP-Server, der KI-Modellen direkten Zugriff auf 30+ Millionen Ressourcen der ETH-Bibliothek Zürich gibt – Bücher, Karten, Bilder, Archivmaterial und Linked-Data-Personeneinträge.

---

## Übersicht

**eth-library-mcp** verbindet KI-Assistenten wie Claude mit der grössten naturwissenschaftlichen Bibliothek der Schweiz. Der Server erschliesst Volltextsuche, archivspezifische Abfragen, Ressourcentyp-Filterung und Personensuche über die Discovery- und Persons-APIs der ETH-Bibliothek – alles über eine einzige, standardisierte MCP-Schnittstelle.

**7 Tools · 3 APIs · 2 Resources · 2 Prompts**

> ⚠️ **Bekanntes Problem (BUG-02):** Das Tool `eth_search_persons` ist aktuell nicht funktionsfähig, da der Persons-API-Endpunkt HTTP 404 zurückgibt. Die korrekte URL muss via [developer.library.ethz.ch](https://developer.library.ethz.ch) verifiziert werden. Alle anderen 6 Tools funktionieren einwandfrei.

**Anker-Demo-Abfrage:** *«Finde historische Dokumente zur Schulgeschichte Zürichs in den ETH-Archiven.»*

---

## Funktionen

- 🔍 **Volltextsuche** über 30+ Millionen Ressourcen mit Feldern, Operatoren und Facetten
- 📖 **Ressourcendetails** – vollständige Metadaten via MMS-ID
- 🗂️ **Archivsuche** – ETH Hochschularchiv, Max Frisch, Thomas Mann, Graphische Sammlung, Bildarchiv
- 🏷️ **Ressourcentyp-Filter** – Bücher, Karten, Bilder, Archivmaterial und mehr
- 🎓 **Bildungssuche** – kuratierter Workflow für Pädagogik und Schulgeschichte
- 👤 **Personensuche** mit Linked-Data-Anreicherung (Wikidata, GND, Metagrid) *(BUG-02: derzeit nicht verfügbar)*
- 📋 **Server-Übersicht** – alle Ressourcentypen und Archive auf einen Blick
- 🗣️ **Eingebaute Prompts** – strukturierter Recherche- und Bildungsrecherche-Workflow
- ☁️ **Dual Transport** – stdio für Claude Desktop, Streamable HTTP/SSE für Cloud-Deployment

---

## Voraussetzungen

- Python 3.11+
- Kostenloser API-Key von [developer.library.ethz.ch](https://developer.library.ethz.ch)

---

## Installation

```bash
# Repository klonen
git clone https://github.com/malkreide/eth-library-mcp.git
cd eth-library-mcp

# Installieren
pip install -e .

# Oder mit uv (empfohlen)
uv pip install -e .
```

---

## Schnellstart

```bash
# API-Key setzen
export ETH_LIBRARY_API_KEY=dein_key_hier   # macOS / Linux
# $env:ETH_LIBRARY_API_KEY = "dein_key_hier"  # Windows (PowerShell)

# Server starten (stdio-Modus für Claude Desktop)
python -m eth_library_mcp.server
```

> Ohne API-Key gibt der Server eine hilfreiche Fehlermeldung mit Registrierungslink – keine Abstürze.

Sofort in Claude Desktop ausprobieren:

> *«Finde Bücher zur Geschichte der Schweizer Bildung in der ETH-Bibliothek.»*
> *«Suche im Max-Frisch-Archiv nach Manuskripten über Zürich.»*

---

## Konfiguration

### Umgebungsvariablen

| Variable | Beschreibung | Erforderlich |
|---|---|---|
| `ETH_LIBRARY_API_KEY` | API-Key für Discovery & Persons API | ✅ |

### Claude Desktop Konfiguration

```json
{
  "mcpServers": {
    "eth-library": {
      "command": "python",
      "args": ["-m", "eth_library_mcp.server"],
      "env": {
        "ETH_LIBRARY_API_KEY": "dein_key_hier"
      }
    }
  }
}
```

**Pfad zur Konfigurationsdatei:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### Cloud-Deployment (SSE für Browser-Zugriff)

Für den Einsatz via **claude.ai im Browser** (z. B. auf verwalteten Arbeitsplätzen ohne lokale Software-Installation):

```bash
MCP_TRANSPORT=sse PORT=8000 python -m eth_library_mcp.server
```

> 💡 *«stdio für den Entwickler-Laptop, SSE für den Browser.»*

---

## Verfügbare Tools

### Discovery API (api.library.ethz.ch)

| Tool | Beschreibung |
|---|---|
| `eth_search_resources` | Volltextsuche über 30+ Millionen Ressourcen mit Feldern, Operatoren, Facetten |
| `eth_get_resource` | Vollständige Metadaten einer Ressource via MMS-ID |
| `eth_search_archive` | Spezifisches Archiv durchsuchen (Hochschularchiv, Max Frisch, Thomas Mann, etc.) |
| `eth_search_by_type` | Nach Ressourcentyp filtern (Bücher, Karten, Bilder, Archivmaterial, etc.) |
| `eth_search_education` | Kuratierte Suche nach Bildungsthemen (Pädagogik, Schulgeschichte, etc.) |

### Persons API

| Tool | Beschreibung |
|---|---|
| `eth_search_persons` | Personensuche mit Linked-Data-Anreicherung (Wikidata, GND, Metagrid) — ⚠️ BUG-02 |

### Hilfsmittel

| Tool | Beschreibung |
|---|---|
| `eth_library_info` | Server-Übersicht: alle Typen und Archive auf einen Blick |

### Resources & Prompts

| Element | Typ | Beschreibung |
|---|---|---|
| `eth://resource-types` | Resource | Alle verfügbaren Ressourcentypen |
| `eth://archives` | Resource | Alle verfügbaren Archive und Sammlungen |
| `research-workflow` | Prompt | Strukturierter Recherche-Workflow |
| `education-research` | Prompt | Bildungsthemen-Workflow (Schulamt-optimiert) |

### Abfrage-Syntax

Die Discovery API nutzt strukturierte Suchanfragen:

```
Feld,Operator,Wert
```

| Feld | Bedeutung |
|---|---|
| `any` | Alle Felder (empfohlen für Einstieg) |
| `title` | Nur im Titel |
| `creator` | Autor / Urheber |
| `sub` | Schlagworte / Themen |

| Operator | Bedeutung |
|---|---|
| `contains` | Begriff kommt vor |
| `exact` | Exakte Übereinstimmung |
| `begins_with` | Beginnt mit |

**Beispiele:**

```
any,contains,Volksschule Zürich
title,contains,Pädagogik
creator,exact,Einstein Albert
sub,contains,Bildungsforschung
title,contains,Schule;sub,contains,Geschichte
```

### Verfügbare Archive

| Kennung | Beschreibung |
|---|---|
| `ETH_Hochschularchiv` | Institutionelles Gedächtnis der ETH Zürich |
| `ETH_MaxFrischArchiv` | Nachlass des Schweizer Autors Max Frisch |
| `ETH_ThomasMannArchiv` | Briefe und Dokumente von Thomas Mann |
| `ETH_GraphischeSammlung` | Drucke, Zeichnungen, grafische Werke |
| `ETH_Bildarchiv` | Wissenschafts-/Technikgeschichte, Swissair (E-Pics) |

### Beispiel-Abfragen

| Abfrage | Tool |
|---|---|
| *«Bücher zur Schulgeschichte Zürichs finden»* | `eth_search_education` |
| *«Was enthält das Max-Frisch-Archiv?»* | `eth_search_archive` |
| *«Historische Karten der Schweiz finden»* | `eth_search_by_type` |
| *«Vollständige Metadaten für Ressource 991170525863705501»* | `eth_get_resource` |
| *«Welche Archive hält die ETH-Bibliothek?»* | `eth_library_info` |

---

## Projektstruktur

```
eth-library-mcp/
├── eth_library_mcp/           # Hauptpaket
│   └── server.py              # FastMCP-Server, Tool-Definitionen
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md                  # Englische Hauptversion
├── README.de.md               # Diese Datei (Deutsch)
├── TEST_PLAN.md
├── claude_desktop_config.json # Beispielkonfiguration Claude Desktop
└── pyproject.toml             # Build-Konfiguration
```

---

## Bekannte Einschränkungen

- **BUG-02 (Persons API):** `eth_search_persons` gibt HTTP 404 zurück – korrekte Endpunkt-URL muss via [developer.library.ethz.ch](https://developer.library.ethz.ch) verifiziert werden
- **Bibliografische Metadaten:** Public Domain – frei nutzbar, keine Einschränkungen
- **Rate Limits:** Gemäss den API-Nutzungsbedingungen der ETH-Bibliothek; kein eingebautes Throttling in dieser Version

---

## Tests

```bash
# Unit-Tests (kein API-Key erforderlich)
PYTHONPATH=. pytest tests/ -m "not live"

# Integrationstests (API-Key erforderlich)
ETH_LIBRARY_API_KEY=xxx pytest tests/ -m "live"
```

---

## Mitwirken

Beiträge sind willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Hinweise.

---

## Changelog

Siehe [CHANGELOG.md](CHANGELOG.md)

---

## Lizenz

- **Server-Code:** MIT-Lizenz – siehe [LICENSE](LICENSE)
- **Bibliografische Metadaten:** Public Domain (keine Einschränkungen)
- **API-Dokumentation:** [developer.library.ethz.ch](https://developer.library.ethz.ch)

---

## Autor

malkreide · [github.com/malkreide](https://github.com/malkreide)

---

## Credits & Verwandte Projekte

- **Daten:** [ETH-Bibliothek Zürich](https://library.ethz.ch) – Discovery & Persons APIs
- **Protokoll:** [Model Context Protocol](https://modelcontextprotocol.io/) – Anthropic / Linux Foundation
- **Verwandt:** [swiss-transport-mcp](https://github.com/malkreide/swiss-transport-mcp) – MCP-Server für den Schweizer ÖV
- **Verwandt:** [zurich-opendata-mcp](https://github.com/malkreide/zurich-opendata-mcp) – MCP-Server für Zürcher Stadtdaten
- **Portfolio:** [Swiss Public Data MCP Portfolio](https://github.com/malkreide)
