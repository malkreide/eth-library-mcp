#!/usr/bin/env python3
"""Setzt die Einzelergebnisse aus `raw/` zu `verification-results.json` zusammen.

Der Skill mcp-audit 2.3.0 hat fuer diesen Schritt keinen Helfer: `raw/` ist dort
als Ablage fuer Task-Agent-Rohausgaben gedacht, und das Zusammenfuehren stand
bisher als Inline-Snippet im Lauf. Genau das verbietet SKILL.md 0.3, und aus dem
genannten Grund -- ein Schritt ohne eigene Datei ist ein Schritt ohne Test.

Dieses Skript prueft deshalb mehr, als es zusammensetzt:

- Jede erwartete ID muss eine Datei haben, und keine Datei eine unerwartete ID.
  Ein Lauf, der 80 von 85 Ergebnissen aggregiert, sieht in `summary.json`
  genauso aus wie ein vollstaendiger -- nur kleiner. Das ist die Fehlerklasse
  aus OPS-005 (was nicht gelaufen ist, sieht aus wie bestanden).
- `status` muss aus dem Vokabular stammen. Ein Tippfehler wie `passed` wuerde
  sonst als eigener Status durchgereicht und taucht in keiner Zaehlung auf.
- `severity` und `category` muessen zur Katalog-Frontmatter passen. Ein Agent,
  der die Severity aus dem Gedaechtnis eintraegt statt aus der Datei, verschiebt
  sonst still das Production-Readiness-Urteil.
- `pass` mit leerer Evidenz wird hier schon abgelehnt, nicht erst im Aggregator.
  Ein unbelegtes `fail` beschaeftigt jemanden weiter; ein unbelegtes `pass`
  beendet die Beschaeftigung, und nichts widerspricht ihm je.

Aufruf:

    python assemble_results.py <audit_dir> --catalog-dir <checks/> [--out DATEI]

Exit 0 nur, wenn alle Pruefungen durchlaufen; sonst 1 mit Begruendung je ID.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VALID_STATUSES = {"pass", "fail", "partial", "not_verified", "todo", "n/a"}

_FRONTMATTER = re.compile(r"^---\s*$(.*?)^---\s*$", re.M | re.S)


def katalog_metadaten(catalog_dir: Path) -> dict[str, dict[str, str]]:
    """Liest `category` und `severity` je Check aus der Frontmatter."""
    meta: dict[str, dict[str, str]] = {}
    for pfad in sorted(catalog_dir.glob("*.md")):
        text = pfad.read_text(encoding="utf-8")
        treffer = _FRONTMATTER.search(text)
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


def erwartete_ids(audit_dir: Path) -> set[str]:
    daten = json.loads((audit_dir / "applicability.json").read_text(encoding="utf-8"))
    return {k for k, v in daten.items() if v.get("applicable")}


def sammle(audit_dir: Path, catalog_dir: Path) -> tuple[dict, list[str]]:
    erwartet = erwartete_ids(audit_dir)
    katalog = katalog_metadaten(catalog_dir)
    roh = audit_dir / "raw"

    vorhanden = {p.stem for p in roh.glob("*.json")}
    fehler: list[str] = []
    for fehlend in sorted(erwartet - vorhanden):
        fehler.append(f"{fehlend}: kein Ergebnis unter raw/")
    for ueberzaehlig in sorted(vorhanden - erwartet):
        fehler.append(f"{ueberzaehlig}: Ergebnis vorhanden, aber nicht anwendbar")

    ergebnisse: dict[str, dict] = {}
    for check_id in sorted(erwartet & vorhanden):
        pfad = roh / f"{check_id}.json"
        try:
            eintrag = json.loads(pfad.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fehler.append(f"{check_id}: kein gueltiges JSON ({exc})")
            continue

        status = eintrag.get("status")
        if status not in VALID_STATUSES:
            fehler.append(f"{check_id}: Status {status!r} steht nicht im Vokabular")
            continue

        soll = katalog.get(check_id, {})
        for feld in ("category", "severity"):
            ist_wert = eintrag.get(feld)
            soll_wert = soll.get(feld)
            if soll_wert and ist_wert != soll_wert:
                fehler.append(
                    f"{check_id}: {feld} ist {ist_wert!r}, der Katalog sagt {soll_wert!r}"
                )

        evidenz = eintrag.get("evidence") or []
        if status == "pass" and not evidenz:
            fehler.append(f"{check_id}: pass ohne Evidenz")

        ergebnisse[check_id] = {
            "status": status,
            "category": soll.get("category", eintrag.get("category")),
            "severity": soll.get("severity", eintrag.get("severity")),
            "evidence": evidenz,
            "gaps": eintrag.get("gaps") or [],
        }

    meta = json.loads((audit_dir / "audit-meta.json").read_text(encoding="utf-8"))
    kopf = meta.get("audit_meta", meta)
    dokument = {
        "audit_meta": {
            "server_name": kopf.get("server_name"),
            "run_id": kopf.get("run_id"),
            "skill_version": kopf.get("skill_version"),
            "catalog_hash": kopf.get("catalog_hash"),
            "target_sha": kopf.get("target_sha"),
            "policy": "fail-or-partial",
        },
        "results": ergebnisse,
    }
    return dokument, fehler


def main() -> int:
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("audit_dir", type=Path)
    zerleger.add_argument("--catalog-dir", type=Path, required=True)
    zerleger.add_argument("--out", type=Path, default=None)
    argumente = zerleger.parse_args()

    dokument, fehler = sammle(argumente.audit_dir, argumente.catalog_dir)
    if fehler:
        print("Zusammensetzen abgebrochen:", file=sys.stderr)
        for zeile in fehler:
            print(f"  - {zeile}", file=sys.stderr)
        return 1

    ziel = argumente.out or argumente.audit_dir / "verification-results.json"
    ziel.write_text(json.dumps(dokument, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(dokument['results'])} Ergebnisse geschrieben nach {ziel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
