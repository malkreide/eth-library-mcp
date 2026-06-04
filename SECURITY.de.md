# Sicherheitsrichtlinie & Sicherheitsstatus

🌐 **[English](SECURITY.md)** | **Deutsch**

`eth-library-mcp` wurde gegen den internen MCP-Best-Practice-Audit-Katalog
gehärtet. Dieses Dokument fasst den Sicherheitsstatus zusammen und hält die
**akzeptierten Restrisiken** für jene Kontrollen fest, die bewusst auf der
Portfolio-/Gateway-Ebene statt in diesem einzelnen Server behandelt werden.

## Eine Schwachstelle melden

Bitte eröffnen Sie ein privates Security Advisory im GitHub-Repository oder
kontaktieren Sie die in `README.md` genannte Maintainerin. Melden Sie
ausnutzbare Schwachstellen nicht über öffentliche Issues.

## Statusübersicht

Dies ist ein **Nur-Lese-**, **PII-freier**, **Public-Domain-Metadaten**-MCP-Server.
Alle 7 Tools stellen ausschliesslich HTTP-GET-Anfragen an eine feste Allow-List
von Endpunkten der ETH-Bibliothek (Discovery- & Persons-API — siehe `README.md`).
Bereits umgesetzte Härtung:

| Bereich | Kontrolle |
|---|---|
| Egress | HTTPS zu einer festen Allow-List (`ALLOWED_EGRESS_HOSTS`) von ETH-Bibliothek-Hosts; jeder Outbound-Call gegen einen nicht gelisteten Host wirft `PermissionError`; keine benutzergesteuerten URLs (SEC-004/021) |
| TLS | Zertifikatsprüfung standardmässig aktiv (httpx-Default); nie deaktiviert (SEC-005) |
| Binding | Standardmässig stdio-Transport; der optionale `--http`-Transport bindet an `127.0.0.1` — `--host 0.0.0.0` muss explizit übergeben werden, nur hinter einem Reverse-Proxy (SEC-016 / SDK-004) |
| CORS | Der HTTP-Transport wrappt die Starlette-App in `CORSMiddleware`; `Mcp-Session-Id` ist in `allow_headers` / `expose_headers` (SDK-004) |
| Tools | Jedes Tool setzt `readOnlyHint: True`; es existieren keine Schreib-, Mutations- oder Löschpfade (ARCH) |
| Secrets | Der einzige `ETH_LIBRARY_API_KEY` wird ausschliesslich aus der Umgebung gelesen; er wird weder geloggt noch an Dritte übermittelt. `.gitignore` + `.env.example` verhindern versehentliche Secret-Commits (ARCH-005 / SEC-013) |
| Fehler | Upstream-Fehlerbodies und Exception-Klassennamen werden nie an den LLM geleakt; das Modell erhält eine generische, nicht-leckende Meldung. Details landen im strukturierten stderr-Log (OBS-002) |
| Logging | Strukturiertes JSON-Logging via `structlog`, auf stderr gepinnt; der stdio-JSON-RPC-stdout-Stream bleibt sauber (OBS-003/004) |
| Sandbox | Multi-stage-`Dockerfile` auf Slim-Base, läuft als Non-Root UID 1000; empfohlene Laufzeit `--read-only --tmpfs /tmp` (SEC-007) |
| Dependencies | Upper Bounds auf alle Dependencies gepinnt (`mcp[cli]>=1.0.0,<2.0.0`, `httpx>=0.27.0,<1.0.0`, `pydantic>=2.0.0,<3.0.0`) (ARCH-012) |
| Resilienz | Ein 30s-Timeout pro Anfrage (`REQUEST_TIMEOUT`) begrenzt jeden Upstream-Aufruf (SCALE-002/003) |

Das Audit (`audits/2026-05-28T142641-Z-eth-library-mcp/`) fand 20 Findings
(3 Critical, 12 High, 5 Medium). Der Re-Audit
(`audits/2026-05-28T184347-Z-eth-library-mcp/`, identischer Katalog) bestätigt
seit `0.3.0` **36/36 anwendbare Checks PASS, 0 Findings**. Die Härtungshistorie
steht in `CHANGELOG.md`.

> ℹ️ **Hinweis (BUG-02):** Das Tool `eth_search_persons` gibt derzeit HTTP 404
> zurück, weil die Persons-API-Endpunkt-URL verifiziert werden muss. Das ist ein
> Funktionsfehler, kein Sicherheitsproblem — das Tool bleibt nur lesend und
> egress-gegated wie jedes andere Tool.

## Akzeptierte Restrisiken (Kontrollen auf Portfolio-Ebene)

Die folgenden Audit-Checks sind bewusst **nicht** innerhalb dieses Servers
umgesetzt. Es handelt sich um portfolioweite Belange, die am besten auf einer
MCP-Gateway-/Host-Ebene durchgesetzt werden; das Restrisiko ist hier gering,
weil der Server nur lesend arbeitet und nur eine kleine Menge vertrauenswürdiger
Public-Data-Anbieter erreicht.

### SEC-014 — Tool-Allow-Listing über ein MCP-Gateway

**Status:** akzeptiertes Risiko (Portfolio-Ebene).
Eine Tool-bezogene Allow-List gehört zum MCP-Host/-Gateway, das mehrere Server
aggregiert, nicht zu einem einzelnen Server mit festem, nur lesendem Tool-Set.
Sobald ein zentrales Gateway für das Portfolio eingeführt wird, sollte das
Tool-Allow-Listing dort konfiguriert werden. Bis dahin ist das Risiko begrenzt:
Jedes Tool ist nur lesend und auf die obigen festen Endpunkte beschränkt.

### SEC-015 — Pre-Flight-Erkennung von Tool-Poisoning

**Status:** akzeptiertes Risiko (Portfolio-Ebene) — mit lokaler Absicherung.
Tool-Poisoning (bösartige Tool-Beschreibungen / Rug-Pulls) ist ein
Supply-Chain- und Host-seitiges Thema. Die Tool-Definitionen dieses Servers sind
versionskontrolliert, im Repo verfasst und via PR reviewt; es gibt keine
dynamische oder entfernte Tool-Registrierung. Server-übergreifende
Poisoning-Erkennung bleibt eine Gateway-/Host-Verantwortung auf Portfolio-Ebene.

## Trigger für eine Neubewertung

Diese Akzeptanzen sollten neu bewertet werden, falls der Server jemals:

- **Schreib**-Fähigkeit erhält oder **PII** verarbeitet, oder
- ein **Authentifizierungs**-Modell über den Upstream-API-Key hinaus erhält
  (dann gebundene, TTL-versehene, serverseitig invalidierbare Session-IDs
  implementieren und vor dem Merge neu auditieren), oder
- Tools **dynamisch** / aus entfernten Quellen registriert, oder
- hinter einem gemeinsamen MCP-Gateway aggregiert wird (dann das
  Tool-Allow-Listing und die Tool-Poisoning-Erkennung des Gateways aktivieren).
