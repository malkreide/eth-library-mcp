# Data sources & licensing

This server aggregates data from the upstream APIs listed below. Every
tool response carries the line
`Quelle: ETH-Bibliothek (Public Domain) · https://developer.library.ethz.ch`
as required by audit check `CH-004` (OGD-CH licence compliance).

## Upstream APIs

| API | Endpoint | Returned data | Licence |
|---|---|---|---|
| Discovery | `https://api.library.ethz.ch/discovery/v1` | Bibliographic metadata for books, journals, archival material, images, maps, scores, databases, audios, videos | Public Domain (CC0) |

## Linked-data sources — no longer surfaced

These sources were reachable only through the Persons API, whose tool was
removed in `0.4.0` (BUG-02: the API is absent from the gateway, not locked).
No tool surfaces them today. The table is kept so the licence position stays
on record should the API ever return:

| Source | Identifier in output | Licence |
|---|---|---|
| [Wikidata](https://www.wikidata.org/) | `wikidata`, `wikidataUrl` | CC0 |
| [Metagrid](https://metagrid.ch/) | (aggregator) | CC0 |
| [DNB Entityfacts](https://www.dnb.de/entityfacts) | `gnd`, `gndId` | CC0 |
| [beacon.findbuch.de](https://beacon.findbuch.de/) | (aggregator) | CC0 |

## Attribution requirement

All upstream data is Public Domain and does **not** require attribution
under copyright law. The `Quelle:` line is included anyway as a courtesy
to data consumers — provenance is information the LLM should preserve.

If a downstream consumer republishes tool output verbatim, the canonical
recommendation is to keep the `Quelle:` line intact and link back to
[developer.library.ethz.ch](https://developer.library.ethz.ch).
