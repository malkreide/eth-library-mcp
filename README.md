> 🇨🇭 **Part of the [Swiss Public Data MCP Portfolio](https://github.com/malkreide)**

# 🏛️ eth-library-mcp

![Version](https://img.shields.io/badge/version-0.2.0-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple)](https://modelcontextprotocol.io/)
[![Data Source](https://img.shields.io/badge/Data-ETH%20Library%20Zurich-red)](https://developer.library.ethz.ch)
[![CI](https://github.com/malkreide/eth-library-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/malkreide/eth-library-mcp/actions/workflows/ci.yml)

> MCP server giving AI models direct access to 30M+ resources at ETH Library Zurich – books, maps, images, archival material, and linked-data person records.

[🇩🇪 Deutsche Version](README.de.md)

---

## Overview

**eth-library-mcp** connects AI assistants like Claude to the largest natural-science library in Switzerland. It exposes full-text search, archive-level queries, resource-type filtering, and person lookups via the ETH Library's Discovery and Persons APIs – all through a single, standardised MCP interface.

**7 Tools · 3 APIs · 2 Resources · 2 Prompts**

> ⚠️ **Known issue (BUG-02):** The tool `eth_search_persons` is currently non-functional because the Persons API endpoint returns HTTP 404. The correct URL needs to be verified at [developer.library.ethz.ch](https://developer.library.ethz.ch). All other 6 tools work correctly.

**Anchor demo query:** *"Find historical documents about Zurich school history in the ETH Library archives."*

---

## Features

- 🔍 **Full-text search** over 30M+ resources with fields, operators, and facets
- 📖 **Resource details** – full metadata via MMS-ID
- 🗂️ **Archive search** – ETH University Archives, Max Frisch, Thomas Mann, Graphische Sammlung, Bildarchiv
- 🏷️ **Resource type filter** – books, maps, images, archival material and more
- 🎓 **Education search** – curated workflow optimised for pedagogy and school history
- 👤 **Person search** with linked-data enrichment (Wikidata, GND, Metagrid) *(BUG-02: currently unavailable)*
- 📋 **Server overview** – all resource types and archives at a glance
- 🗣️ **Built-in prompts** – structured research and education-research workflows
- ☁️ **Dual transport** – stdio for Claude Desktop, Streamable HTTP/SSE for cloud deployment

---

## Prerequisites

- Python 3.11+
- A free API key from [developer.library.ethz.ch](https://developer.library.ethz.ch)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/malkreide/eth-library-mcp.git
cd eth-library-mcp

# Install
pip install -e .

# Or with uv (recommended)
uv pip install -e .
```

---

## Quickstart

```bash
# Set the API key
export ETH_LIBRARY_API_KEY=your_key_here   # macOS / Linux
# $env:ETH_LIBRARY_API_KEY = "your_key_here"  # Windows (PowerShell)

# Start the server (stdio mode for Claude Desktop)
python -m eth_library_mcp.server
```

> Without an API key the server returns a helpful error message with the registration link – no crashes.

Try it immediately in Claude Desktop:

> *"Find books about Swiss education history in the ETH Library."*
> *"Search the Max Frisch archive for manuscripts about Zurich."*

---

## Configuration

### Environment Variables

| Variable | Description | Required |
|---|---|---|
| `ETH_LIBRARY_API_KEY` | API key for Discovery & Persons API | ✅ |

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "eth-library": {
      "command": "python",
      "args": ["-m", "eth_library_mcp.server"],
      "env": {
        "ETH_LIBRARY_API_KEY": "your_key_here"
      }
    }
  }
}
```

**Config file locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### Cloud Deployment (SSE for browser access)

For use via **claude.ai in the browser** (e.g. on managed workstations without local software):

```bash
MCP_TRANSPORT=sse PORT=8000 python -m eth_library_mcp.server
```

> 💡 *"stdio for the developer laptop, SSE for the browser."*

---

## Available Tools

### Discovery API (api.library.ethz.ch)

| Tool | Description |
|---|---|
| `eth_search_resources` | Full-text search over 30M+ resources with fields, operators, facets |
| `eth_get_resource` | Full metadata for a specific resource via MMS-ID |
| `eth_search_archive` | Search within a specific archive (University Archives, Max Frisch, Thomas Mann, etc.) |
| `eth_search_by_type` | Filter by resource type (books, maps, images, archival material, etc.) |
| `eth_search_education` | Curated search for education topics (pedagogy, school history, etc.) |

### Persons API

| Tool | Description |
|---|---|
| `eth_search_persons` | Person search with linked-data enrichment (Wikidata, GND, Metagrid) — ⚠️ BUG-02 |

### Utilities

| Tool | Description |
|---|---|
| `eth_library_info` | Server overview: all types and archives at a glance |

### Resources & Prompts

| Item | Type | Description |
|---|---|---|
| `eth://resource-types` | Resource | All available resource types |
| `eth://archives` | Resource | All available archives and collections |
| `research-workflow` | Prompt | Structured research workflow |
| `education-research` | Prompt | Education topics workflow (Schulamt-optimised) |

### Query Syntax

The Discovery API uses structured queries:

```
field,operator,value
```

| Field | Meaning |
|---|---|
| `any` | All fields (recommended for starters) |
| `title` | Title only |
| `creator` | Author / creator |
| `sub` | Subject headings / topics |

| Operator | Meaning |
|---|---|
| `contains` | Term is present |
| `exact` | Exact match |
| `begins_with` | Starts with |

**Examples:**

```
any,contains,Volksschule Zürich
title,contains,Pädagogik
creator,exact,Einstein Albert
sub,contains,Bildungsforschung
title,contains,Schule;sub,contains,Geschichte
```

### Available Archives

| Identifier | Description |
|---|---|
| `ETH_Hochschularchiv` | Institutional memory of ETH Zurich |
| `ETH_MaxFrischArchiv` | Estate of Swiss author Max Frisch |
| `ETH_ThomasMannArchiv` | Letters and documents of Thomas Mann |
| `ETH_GraphischeSammlung` | Prints, drawings, graphic works |
| `ETH_Bildarchiv` | Science/technology history, Swissair (E-Pics) |

### Example Use Cases

| Query | Tool |
|---|---|
| *"Find books about Zurich school history"* | `eth_search_education` |
| *"What's in the Max Frisch archive?"* | `eth_search_archive` |
| *"Find historical maps of Switzerland"* | `eth_search_by_type` |
| *"Get full metadata for resource ID 991170525863705501"* | `eth_get_resource` |
| *"Which archives does the ETH Library hold?"* | `eth_library_info` |

---

## Project Structure

```
eth-library-mcp/
├── eth_library_mcp/           # Main package
│   └── server.py              # FastMCP server, tool definitions
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md                  # This file (English)
├── README.de.md               # German version
├── TEST_PLAN.md
├── claude_desktop_config.json # Example Claude Desktop configuration
└── pyproject.toml             # Build configuration
```

---

## Known Limitations

- **BUG-02 (Persons API):** `eth_search_persons` returns HTTP 404 – correct endpoint URL to be verified at [developer.library.ethz.ch](https://developer.library.ethz.ch)
- **Bibliographic metadata:** Licensed as Public Domain – free for all uses, no restrictions
- **Rate limits:** Governed by the ETH Library API terms; no built-in throttling in this server version

---

## Testing

```bash
# Unit tests (no API key required)
PYTHONPATH=. pytest tests/ -m "not live"

# Integration tests (API key required)
ETH_LIBRARY_API_KEY=xxx pytest tests/ -m "live"
```

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md)

---

## License

- **Server code:** MIT License — see [LICENSE](LICENSE)
- **Bibliographic metadata:** Public Domain (no restrictions)
- **API documentation:** [developer.library.ethz.ch](https://developer.library.ethz.ch)

---

## Author

malkreide · [github.com/malkreide](https://github.com/malkreide)

---

## Credits & Related Projects

- **Data:** [ETH Library Zurich](https://library.ethz.ch) – Discovery & Persons APIs
- **Protocol:** [Model Context Protocol](https://modelcontextprotocol.io/) – Anthropic / Linux Foundation
- **Related:** [swiss-transport-mcp](https://github.com/malkreide/swiss-transport-mcp) – MCP server for Swiss public transport
- **Related:** [zurich-opendata-mcp](https://github.com/malkreide/zurich-opendata-mcp) – MCP server for Zurich city open data
- **Portfolio:** [Swiss Public Data MCP Portfolio](https://github.com/malkreide)
