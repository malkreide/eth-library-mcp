# Contributing to eth-library-mcp

Thank you for your interest in contributing to **eth-library-mcp**! This server is part of the [Swiss Public Data MCP Portfolio](https://github.com/malkreide) and contributions that strengthen Swiss open-data accessibility for AI assistants are especially welcome.

---

## How to Contribute

### Reporting Issues

Use [GitHub Issues](https://github.com/malkreide/eth-library-mcp/issues) to report bugs or request features.

When reporting a bug, please include:
- Python version (`python --version`)
- Operating system
- Steps to reproduce the issue
- Expected vs. actual behaviour
- Relevant error messages or logs

### Open Issues

| ID | Description | Priority |
|---|---|---|
| **BUG-02** | `eth_search_persons` returns HTTP 404 – correct Persons API endpoint URL needs verification at [developer.library.ethz.ch](https://developer.library.ethz.ch) | High |

If you have resolved BUG-02 or have a verified working endpoint URL, please open a pull request or comment on the issue directly.

---

## Development Setup

```bash
# Clone and install in editable mode
git clone https://github.com/malkreide/eth-library-mcp.git
cd eth-library-mcp
pip install -e ".[dev]"

# Or with uv
uv pip install -e ".[dev]"
```

### Running Tests

```bash
# Unit tests (no API key required)
PYTHONPATH=. pytest tests/ -m "not live"

# Integration tests (requires a valid API key)
ETH_LIBRARY_API_KEY=your_key pytest tests/ -m "live"
```

Tests marked `@pytest.mark.live` call the real ETH Library API and require a valid key from [developer.library.ethz.ch](https://developer.library.ethz.ch).

### Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
ruff check .
ruff format .
```

---

## Pull Request Guidelines

1. **Fork** the repository and create a feature branch from `main`:
   ```bash
   git checkout -b fix/bug-02-persons-api
   ```

2. **Write tests** for any new tool or bug fix. Live tests go in `tests/` with the `@pytest.mark.live` marker.

3. **Update documentation** – if you add or change a tool, update both `README.md` (English) and `README.de.md` (German). Keep the language toggle links at the top of each file.

4. **Update `CHANGELOG.md`** – add an entry under `[Unreleased]` using [Conventional Commits](https://www.conventionalcommits.org/) style:
   - `fix:` – bug fix
   - `feat:` – new feature or tool
   - `docs:` – documentation only
   - `refactor:` – code change with no functional impact

5. **Open a Pull Request** against `main` with a clear description of what changed and why.

---

## Commit Message Convention

```
<type>: <short description>

# Examples
fix: resolve BUG-02 Persons API 404 with updated endpoint
feat: add eth_search_collections tool for collection-level browsing
docs: add query syntax examples to README
```

---

## Adding a New Tool

New tools go in `src/eth_library_mcp/server.py`. Follow the existing pattern:

```python
@mcp.tool()
async def eth_your_new_tool(param: str) -> str:
    """
    One-line description for the AI model.

    Args:
        param: What this parameter does.

    Returns:
        JSON string with results.
    """
    ...
```

After adding a tool:
- Add it to the **Available Tools** table in `README.md` and `README.de.md`
- Add at least one unit test in `tests/`
- Add an example query to the **Example Use Cases** table in the README files

---

## Data & Licensing Notes

- **Server code:** MIT License
- **Bibliographic metadata** returned by the ETH Library API: **Public Domain** – no restrictions on reuse
- Do not embed or cache API responses in the repository

---

## Questions

Open a [GitHub Discussion](https://github.com/malkreide/eth-library-mcp/discussions) or contact the maintainer via GitHub.
