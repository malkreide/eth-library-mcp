# ETH Library MCP Server 🏛️

![Version](https://img.shields.io/badge/version-0.2.0-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/malkreide/eth-library-mcp/actions/workflows/ci.yml/badge.svg)

> MCP-Server für die ETH-Bibliothek Zürich – Ermöglicht Claude und anderen KI-Assistenten den direkten Zugriff auf 30+ Millionen Ressourcen der grössten naturwissenschaftlichen Bibliothek der Schweiz.

**7 Tools · 3 APIs · 2 Resources · 2 Prompts**

> ⚠️ **Bekanntes Problem (BUG-02):** Das Tool `eth_search_persons` ist aktuell nicht funktionsfähig, da der Persons-API-Endpunkt HTTP 404 zurückgibt. Die korrekte URL muss via [developer.library.ethz.ch](https://developer.library.ethz.ch) verifiziert werden. Alle anderen 6 Tools funktionieren einwandfrei.

---

## ✨ Features

### Discovery API (api.library.ethz.ch)

- **`eth_search_resources`** – Volltextsuche über 30+ Millionen Ressourcen mit Feldern, Operatoren, Facetten
- **`eth_get_resource`** – Vollständige Metadaten einer Ressource via MMS-ID abrufen
- **`eth_search_archive`** – Spezifische Archive durchsuchen (Hochschularchiv, Max Frisch, Thomas Mann, etc.)
- **`eth_search_by_type`** – Nach Ressourcentyp filtern (Bücher, Karten, Bilder, Archivmaterial, etc.)
- **`eth_search_education`** – Kuratierte Suche nach Bildungsthemen (Pädagogik, Schulgeschichte, etc.)

### Persons API

- **`eth_search_persons`** – Personensuche mit Linked-Data-Anreicherung (Wikidata, GND, Metagrid)

### Hilfsmittel

- **`eth_library_info`** – Server-Übersicht, alle Typen und Archive auf einen Blick
- **Resource:** `eth://resource-types` – Alle verfügbaren Ressourcentypen
- **Resource:** `eth://archives` – Alle verfügbaren Archive und Sammlungen
- **Prompt:** `research-workflow` – Strukturierter Recherche-Workflow
- **Prompt:** `education-research` – Bildungsthemen-Workflow (Schulamt-optimiert)

---

## 🗂️ Verfügbare Archive

| Kennung | Beschreibung |
|---------|-------------|
| `ETH_Hochschularchiv` | Institutionelles Gedächtnis der ETH Zürich |
| `ETH_MaxFrischArchiv` | Nachlass des Schweizer Autors Max Frisch |
| `ETH_ThomasMannArchiv` | Briefe und Dokumente von Thomas Mann |
| `ETH_GraphischeSammlung` | Drucke, Zeichnungen, grafische Werke |
| `ETH_Bildarchiv` | Wissenschafts-/Technikgeschichte, Swissair (E-Pics) |

---

## 🚀 Installation

### Voraussetzungen

- Python 3.11+
- pip oder uv
- Kostenloser API-Key: [developer.library.ethz.ch](https://developer.library.ethz.ch)

### Installation

```bash
# Klonen
git clone https://github.com/malkreide/eth-library-mcp.git
cd eth-library-mcp

# Installieren
pip install -e .

# Oder mit uv (empfohlen)
uv pip install -e .
```

### API-Key einrichten

```bash
# Windows (PowerShell)
$env:ETH_LIBRARY_API_KEY = "dein-api-key"

# macOS/Linux
export ETH_LIBRARY_API_KEY="dein-api-key"
```

> **Hinweis:** Ohne API-Key gibt der Server eine hilfreiche Fehlermeldung mit Registrierungslink – keine Abstürze.

---

## ⚙️ Konfiguration Claude Desktop

Datei öffnen:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "eth-library": {
      "command": "python",
      "args": ["-m", "eth_library_mcp.server"],
      "env": {
        "ETH_LIBRARY_API_KEY": "dein-api-key"
      }
    }
  }
}
```

---

## 🔍 Query-Syntax

Die Discovery API nutzt eine strukturierte Suchanfrage:

```
Feld,Operator,Wert
```

**Felder:**
- `any` – Alle Felder (empfohlen für Einstieg)
- `title` – Nur im Titel
- `creator` – Autor/Urheber
- `sub` – Schlagworte/Themen

**Operatoren:**
- `contains` – Begriff kommt vor
- `exact` – Exakte Übereinstimmung
- `begins_with` – Beginnt mit

**Beispiele:**
```
any,contains,Volksschule Zürich
title,contains,Pädagogik
creator,exact,Einstein Albert
sub,contains,Bildungsforschung
title,contains,Schule;sub,contains,Geschichte
```

---

## ☁️ Cloud-Deployment (Render.com)

```bash
MCP_TRANSPORT=sse PORT=8000 python -m eth_library_mcp.server
```

---

## 📄 Lizenz

- **Bibliografische Metadaten:** Public Domain (frei nutzbar, keine Einschränkungen)
- **Server-Code:** MIT Licence
- **API-Dokumentation:** [developer.library.ethz.ch](https://developer.library.ethz.ch)
- **Kontakt ETH-Bibliothek:** api@library.ethz.ch

---

*Entwickelt vals Teil der MCP-Server-Ökosystems für Schweizer Open Data.*
