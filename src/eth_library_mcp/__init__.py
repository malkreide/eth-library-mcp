"""ETH Library MCP Server."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import metadata as _distribution_metadata
from importlib.metadata import version as _distribution_version

_DISTRIBUTION = "eth-library-mcp"

try:
    # Read the version from the installed distribution metadata, which is built
    # from pyproject.toml. Hand-maintaining the literal here let the numbers
    # drift apart: pyproject said 0.3.3, this said 0.3.0. A value nobody
    # has to remember to bump cannot go stale.
    __version__ = _distribution_version(_DISTRIBUTION)
except PackageNotFoundError:
    # Running from the source tree without an install (e.g. a bare checkout).
    # Deliberately not a plausible-looking number: an obviously non-release
    # marker is better than a wrong version in the User-Agent.
    __version__ = "0.0.0+source"


def _identity() -> tuple[str | None, str | None]:
    """Kurzbeschreibung und Homepage aus den Paket-Metadaten.

    Dieselbe Begruendung wie bei `__version__` eine Ebene hoeher: beide Werte
    stehen schon in `pyproject.toml` und in `server.json`. Ein drittes Literal
    in `src/` waere eine Kopie, die niemand mitbewegt — und anders als bei der
    Versionsnummer gibt es dafuer kein Gate, das die Drift meldete
    (`scripts/check_version_sync.py` prueft ausschliesslich Zahlen).

    `Home-page` ist seit PEP 621 leer; die Homepage steht als `Project-URL`
    mit dem Label davor. Aus dem Kopf gelesen statt geraten: die Messung auf
    diesem Repo lieferte `Home-page: None` und drei `Project-URL`-Zeilen.
    """
    try:
        meta = _distribution_metadata(_DISTRIBUTION)
    except PackageNotFoundError:
        # Ohne Installation gibt es nichts zu melden. `None` laesst die Felder
        # aus der Server-Identitaet fallen; ein erfundener Platzhalter waere
        # eine Behauptung ueber einen Server, den niemand installiert hat.
        return None, None

    summary = meta["Summary"] or None
    homepage = None
    for entry in meta.get_all("Project-URL") or ():
        label, _, url = str(entry).partition(",")
        if label.strip().lower() == "homepage":
            homepage = url.strip() or None
            break
    return summary, homepage


# Beschreibung und Homepage dieser Distribution — Teil der Identitaet, die Spec
# 2026-07-28 in jede Antwort stempelt
# (`_meta.io.modelcontextprotocol/serverInfo`). Bewusst ein Kommentar und kein
# String unter der Zuweisung: an einer Mehrfachzuweisung haengt kein `__doc__`,
# ein String dort saehe nur wie Doku aus.
DESCRIPTION, HOMEPAGE_URL = _identity()
