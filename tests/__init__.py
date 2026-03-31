"""Smoke-Tests für eth-library-mcp (kein Netzwerk)."""


def test_import_server():
    """Stellt sicher, dass der MCP-Server importierbar ist."""
    from eth_library_mcp.server import mcp

    assert mcp is not None


def test_import_api_client():
    """Stellt sicher, dass der API-Client importierbar ist."""
    import eth_library_mcp.api_client  # noqa: F401
