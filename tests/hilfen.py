"""Lesehilfen fuer Werkzeug-Ergebnisse und der Weg durch den echten ASGI-Stack.

Zwei Gruppen:

*Lesen.* Seit FID-003 geben die fuenf datenliefernden Werkzeuge ein
`CallToolResult` zurueck statt eines `str`: Der Markdown-Block bleibt, daneben
steht `structuredContent` mit `returned`, `total` und `hint`. `text()` und
`strukturiert()` lesen beides, damit eine spaetere Formatsaenderung an genau
einer Stelle nachzuziehen ist.

*Messen.* `werkzeuge_am_draht()` und `aufruf_am_draht()` schicken `tools/list`
bzw. `tools/call` durch `build_http_app()`. Der Umweg ist Absicht: Ein direkter
Funktionsaufruf zeigt den Rueckgabewert, nicht das, was beim Client ankommt --
und genau dort sassen beide Befunde, die diese Tests decken. `isError` etwa
entsteht erst in der SDK-Schicht und ist an der Funktion gar nicht zu sehen.

Der Host `127.0.0.1:8000` ist kein Detail: Der DNS-Rebinding-Schutz des
Transports weist jeden anderen Host-Header mit HTTP 421 ab, und das sieht beim
Messen wie ein stummer Server aus.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
from mcp.types import CallToolResult

from eth_library_mcp.server import build_http_app

MODERN = "2026-07-28"


def text(ergebnis: CallToolResult) -> str:
    """Der Markdown-Block, den das Modell liest."""
    return "\n".join(
        block.text for block in ergebnis.content if getattr(block, "text", None) is not None
    )


def strukturiert(ergebnis: CallToolResult) -> dict[str, Any]:
    """Die maschinenlesbaren Felder neben dem Text."""
    return ergebnis.structured_content or {}


def _umschlag(methode: str, parameter: dict[str, Any] | None = None) -> dict[str, Any]:
    from mcp_types import CLIENT_CAPABILITIES_META_KEY, PROTOCOL_VERSION_META_KEY

    inhalt: dict[str, Any] = dict(parameter or {})
    inhalt["_meta"] = {
        PROTOCOL_VERSION_META_KEY: MODERN,
        CLIENT_CAPABILITIES_META_KEY: {},
    }
    return {"jsonrpc": "2.0", "id": 1, "method": methode, "params": inhalt}


def _auspacken(antwort: httpx.Response) -> dict[str, Any]:
    koerper = antwort.text
    for zeile in koerper.splitlines():
        if zeile.startswith("data: "):
            koerper = zeile[len("data: ") :]
    return json.loads(koerper)


async def _sende(methode: str, parameter: dict[str, Any], kopfzeilen: dict[str, str]) -> Any:
    app = build_http_app()
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as c:
            antwort = await c.post(
                "/mcp",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "Host": "127.0.0.1:8000",
                    "MCP-Protocol-Version": MODERN,
                    **kopfzeilen,
                },
                json=_umschlag(methode, parameter),
            )
    return _auspacken(antwort)


async def werkzeuge_am_draht() -> list[dict[str, Any]]:
    """`tools/list` durch den echten ASGI-Stack."""
    nutzlast = await _sende("tools/list", {}, {"Mcp-Method": "tools/list"})
    assert "result" in nutzlast, f"tools/list antwortete mit {nutzlast!r}"
    return nutzlast["result"]["tools"]


async def aufruf_am_draht(name: str, argumente: dict[str, Any]) -> dict[str, Any]:
    """`tools/call` durch den echten ASGI-Stack; gibt das rohe Result zurueck.

    Die Kopfzeile `Mcp-Name` muss den Werkzeugnamen wiederholen, sonst
    antwortet der Server mit HTTP 400 und `-32020`. Gemessen, nachdem genau
    das eine erste Fassung dieser Hilfe stumm aussehen liess.
    """
    nutzlast = await _sende(
        "tools/call",
        {"name": name, "arguments": argumente},
        {"Mcp-Method": "tools/call", "Mcp-Name": name},
    )
    assert "result" in nutzlast, f"tools/call antwortete mit {nutzlast!r}"
    return nutzlast["result"]
