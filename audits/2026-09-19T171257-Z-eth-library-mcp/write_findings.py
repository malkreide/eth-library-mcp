#!/usr/bin/env python3
"""Schreibt je Finding ein Dokument aus den gemessenen Belegen.

Warum nicht `carry_forward.py`: Der Helfer uebernimmt *unveraenderte* Findings
aus einem Vorlauf. Der einzige Vorlauf dieses Servers ist vom 28.5.2026 und
beschreibt einen Zustand vor der SDK-2.x-Migration, vor der Entfernung von
`eth_search_persons` und vor der Spec-2026-07-28-Arbeit. Von 68 damals
ausgewerteten Checks sind 52 heute neu; die uebrigen messen an einem Baum, den
es so nicht mehr gibt. Ein Uebertrag waere kein Uebertrag, sondern das
Weiterreichen einer Aussage, die niemand mehr geprueft hat -- genau die
Herkunftsklasse `uebernommen`, die SKILL.md 4.1 kein Gate speisen laesst.

Die Inhalte stammen deshalb ausschliesslich aus `verification-results.json`,
also aus den Messungen dieses Laufs. Dieses Skript formuliert nichts hinzu: Wo
ein Feld leer ist, steht das im Dokument, statt dass eine Luecke mit einer
plausiblen Vermutung gefuellt wird.

Der Titel je Check kommt aus der Katalog-Frontmatter, nicht aus dem Gedaechtnis.

Aufruf:

    python write_findings.py <audit_dir> --catalog-dir <checks/> [--policy ...]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

POLICY_STATUSES = {
    "fail-or-partial": {"fail", "partial"},
    "fail-only": {"fail"},
    "needs-attention": {"fail", "partial", "todo"},
}

_FRONTMATTER = re.compile(r"^---\s*$(.*?)^---\s*$", re.M | re.S)

_AUFWAND = {"critical": "M (1-3d)", "high": "M (1-3d)", "medium": "S (< 1d)", "low": "S (< 1d)"}


def katalog(catalog_dir: Path) -> dict[str, dict[str, str]]:
    meta: dict[str, dict[str, str]] = {}
    for pfad in sorted(catalog_dir.glob("*.md")):
        treffer = _FRONTMATTER.search(pfad.read_text(encoding="utf-8"))
        if not treffer:
            continue
        felder: dict[str, str] = {}
        for zeile in treffer.group(1).splitlines():
            schluessel, trenner, wert = zeile.partition(":")
            if trenner:
                felder[schluessel.strip()] = wert.strip().strip("\"'")
        if "id" in felder:
            meta[felder["id"]] = felder
    return meta


def liste(eintraege: list[str], leertext: str) -> str:
    if not eintraege:
        return leertext
    return "\n".join(f"- {e}" for e in eintraege)


def dokument(check_id: str, ergebnis: dict, front: dict, server: str, run_id: str) -> str:
    titel = front.get("title", "(kein Titel in der Katalog-Frontmatter)")
    severity = ergebnis["severity"]
    status = ergebnis["status"]
    evidenz = ergebnis.get("evidence") or []
    luecken = ergebnis.get("gaps") or []

    if status == "fail":
        beobachtet = (
            "Der Check ist **nicht** erfuellt. Die folgenden Punkte sind in "
            "diesem Lauf am Baum gemessen worden."
        )
    else:
        beobachtet = (
            "Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen "
            "sind belegt, einzelne Kriterien nicht. Beides steht unten."
        )

    return f"""## Finding: {check_id} — {titel}

**Severity:** {severity}
**Status:** open
**Server:** {server}
**Check-Reference:** {check_id}
**Katalog-Referenz:** {front.get("pdf_ref", "(keine)")}
**Spec-Baseline:** {front.get("spec_baseline", "(keine)")}
**Audit-Lauf:** {run_id}

### Observed Behavior

{beobachtet}

{liste(evidenz, "_Keine Evidenz erfasst._")}

### Expected Behavior

Die Pass-Kriterien stehen in `checks/{check_id}.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

{liste(evidenz, "_Keine Evidenz erfasst._")}

### Gaps

{liste(luecken, "_Keine Luecken vermerkt._")}

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `{severity}`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/{check_id}.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

{_AUFWAND.get(severity, "S (< 1d)")} — Schaetzung nach Severity, nicht gemessen.
"""


def main() -> int:
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("audit_dir", type=Path)
    zerleger.add_argument("--catalog-dir", type=Path, required=True)
    zerleger.add_argument("--policy", default="fail-or-partial", choices=sorted(POLICY_STATUSES))
    argumente = zerleger.parse_args()

    ergebnisse_datei = argumente.audit_dir / "verification-results.json"
    daten = json.loads(ergebnisse_datei.read_text(encoding="utf-8"))
    kopf = daten["audit_meta"]
    front_alle = katalog(argumente.catalog_dir)
    betroffen = POLICY_STATUSES[argumente.policy]

    ziel = argumente.audit_dir / "findings"
    ziel.mkdir(exist_ok=True)

    geschrieben = 0
    ohne_frontmatter: list[str] = []
    for check_id, ergebnis in sorted(daten["results"].items()):
        if ergebnis["status"] not in betroffen:
            continue
        front = front_alle.get(check_id)
        if front is None:
            ohne_frontmatter.append(check_id)
            front = {}
        text = dokument(
            check_id, ergebnis, front, kopf.get("server_name", "?"), kopf.get("run_id", "?")
        )
        (ziel / f"{check_id}.md").write_text(text, encoding="utf-8")
        geschrieben += 1

    if ohne_frontmatter:
        print(
            "Ohne Katalog-Frontmatter (Titel fehlt): " + ", ".join(ohne_frontmatter),
            file=sys.stderr,
        )
    print(f"{geschrieben} Finding-Dokumente geschrieben nach {ziel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
