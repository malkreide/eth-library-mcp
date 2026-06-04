# Mitwirken an eth-library-mcp

🌐 **[English](CONTRIBUTING.md)** | **Deutsch**

Vielen Dank für Ihr Interesse an einem Beitrag zu **eth-library-mcp**! Dieser Server ist Teil des [Swiss Public Data MCP Portfolios](https://github.com/malkreide), und Beiträge, die den Zugang zu offenen Schweizer Daten für KI-Assistenten stärken, sind besonders willkommen.

---

## Wie man beiträgt

### Probleme melden

Nutzen Sie die [GitHub Issues](https://github.com/malkreide/eth-library-mcp/issues), um Fehler zu melden oder Features vorzuschlagen.

Bitte geben Sie bei einem Bug-Report an:
- Python-Version (`python --version`)
- Betriebssystem
- Schritte zur Reproduktion des Problems
- Erwartetes vs. tatsächliches Verhalten
- Relevante Fehlermeldungen oder Logs

### Offene Issues

| ID | Beschreibung | Priorität |
|---|---|---|
| **BUG-02** | `eth_search_persons` gibt HTTP 404 zurück – die korrekte Persons-API-Endpunkt-URL muss via [developer.library.ethz.ch](https://developer.library.ethz.ch) verifiziert werden | Hoch |

Wenn Sie BUG-02 gelöst haben oder eine verifizierte, funktionierende Endpunkt-URL kennen, eröffnen Sie bitte einen Pull Request oder kommentieren Sie direkt im Issue.

---

## Entwicklungsumgebung einrichten

```bash
# Klonen und im Editable-Modus installieren
git clone https://github.com/malkreide/eth-library-mcp.git
cd eth-library-mcp
pip install -e ".[dev]"

# Oder mit uv
uv pip install -e ".[dev]"
```

### Tests ausführen

```bash
# Unit-Tests (kein API-Key erforderlich)
PYTHONPATH=. pytest tests/ -m "not live"

# Integrationstests (erfordern einen gültigen API-Key)
ETH_LIBRARY_API_KEY=dein_key pytest tests/ -m "live"
```

Mit `@pytest.mark.live` markierte Tests rufen die echte ETH-Bibliothek-API auf und benötigen einen gültigen Key von [developer.library.ethz.ch](https://developer.library.ethz.ch).

### Code-Stil

Dieses Projekt verwendet [Ruff](https://docs.astral.sh/ruff/) für Linting und Formatierung:

```bash
ruff check .
ruff format .
```

---

## Richtlinien für Pull Requests

1. **Forken** Sie das Repository und erstellen Sie einen Feature-Branch von `main`:
   ```bash
   git checkout -b fix/bug-02-persons-api
   ```

2. **Schreiben Sie Tests** für jedes neue Tool und jeden Bugfix. Live-Tests gehören mit dem Marker `@pytest.mark.live` nach `tests/`.

3. **Aktualisieren Sie die Dokumentation** – wenn Sie ein Tool hinzufügen oder ändern, aktualisieren Sie sowohl `README.md` (Englisch) als auch `README.de.md` (Deutsch). Behalten Sie die Sprachumschalt-Links am Anfang jeder Datei bei.

4. **Aktualisieren Sie `CHANGELOG.md`** – fügen Sie einen Eintrag unter `[Unreleased]` im Stil von [Conventional Commits](https://www.conventionalcommits.org/) hinzu:
   - `fix:` – Bugfix
   - `feat:` – neues Feature oder Tool
   - `docs:` – nur Dokumentation
   - `refactor:` – Codeänderung ohne funktionale Auswirkung

5. **Eröffnen Sie einen Pull Request** gegen `main` mit einer klaren Beschreibung, was und warum geändert wurde.

---

## Commit-Message-Konvention

```
<typ>: <kurze Beschreibung>

# Beispiele
fix: resolve BUG-02 Persons API 404 with updated endpoint
feat: add eth_search_collections tool for collection-level browsing
docs: add query syntax examples to README
```

---

## Ein neues Tool hinzufügen

Neue Tools gehören in `src/eth_library_mcp/server.py`. Folgen Sie dem bestehenden Muster:

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

Nach dem Hinzufügen eines Tools:
- Tragen Sie es in die Tabelle **Available Tools** in `README.md` und `README.de.md` ein
- Fügen Sie mindestens einen Unit-Test in `tests/` hinzu
- Ergänzen Sie eine Beispielabfrage in der Tabelle **Example Use Cases** der README-Dateien

---

## Hinweise zu Daten & Lizenzierung

- **Server-Code:** MIT-Lizenz
- **Bibliografische Metadaten** der ETH-Bibliothek-API: **Public Domain** – keine Einschränkungen bei der Weiterverwendung
- API-Antworten nicht im Repository einbetten oder cachen

---

## Fragen

Eröffnen Sie eine [GitHub Discussion](https://github.com/malkreide/eth-library-mcp/discussions) oder kontaktieren Sie die Maintainerin über GitHub.
