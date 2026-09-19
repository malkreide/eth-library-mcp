# Baseline-Messung: welche Protokollepoche dieser Server tatsaechlich bedient

Gemessen am 2026-09-19 gegen HEAD `32ac730`, lokal durch den echten ASGI-Stack
(`build_http_app()`, Host `127.0.0.1:8000`, kein Netz).

## Handshake-Epoche (2025-11-25)

```
POST /mcp  method=initialize  protocolVersion=2025-11-25
  -> HTTP 200
  -> Mcp-Session-Id: bd69c99c811f4e9398e4feb3c2096c32   (32 Hexzeichen)
zweiter Handshake
  -> Mcp-Session-Id: c4cb8e8c79d2427db65fff8de352b9cc   (verschieden)
POST /mcp  mit erfundener Mcp-Session-Id
  -> HTTP 404
```

## Moderne Epoche (2026-07-28, Pro-Request-Envelope)

```
POST /mcp  tools/list  params._meta{protocolVersion, clientCapabilities}
           Header MCP-Protocol-Version + Mcp-Method
  -> HTTP 200, 6 Werkzeuge, KEIN Mcp-Session-Id
  -> _meta["io.modelcontextprotocol/serverInfo"] =
     {name, title, version 0.4.0, description, websiteUrl}
  -> zweite Anfrage auf derselben Verbindung: identisch, weiterhin sessionlos
```

## Zwei Fehlschluesse, die unterwegs vermieden wurden

**HTTP 421 ist hier kein Nein.** Der erste Versuch lief gegen `http://test` und
bekam auf *jede* Anfrage 421. Das sieht aus wie ein Server, der nichts
beantwortet; tatsaechlich ist es der DNS-Rebinding-Schutz
(`TransportSecuritySettings`), der den Host-Kopf verwirft. Mit
`127.0.0.1:8000` antworten dieselben Anfragen mit 200.

**HTTP 400 war die eigene Anfrage.** Ein `tools/list` ohne
`params._meta` bekommt:

```
-32602  params._meta must be an object carrying the required
        'io.modelcontextprotocol/protocolVersion' and
        'io.modelcontextprotocol/clientCapabilities' envelope keys
```

Der Statuscode allein haette «moderne Epoche wird nicht bedient» nahegelegt.
Die Meldung benennt den fehlenden Parameter — genau die Lage, die CLAUDE.md
unter `lotId` fuehrt. Mit dem Envelope antwortet dieselbe Route mit 200.

## Folge fuer die Baseline-Wahl

Das Profil traegt `mcp_spec_version: "2026-07-28"`, und der Katalog kennt je
Profil genau eine Baseline. Gemessen bedient derselbe Prozess aber beide
Epochen, und die aeltere vergibt nachweislich Session-IDs. Die Baseline-Wahl
laesst deshalb drei Checks fallen, deren Gegenstand an diesem Server lebt:

| Check | Severity | Gegenstand | Im Vorlauf 28.5.2026 |
|---|---|---|---|
| SEC-009 | **critical** | Session-ID kryptographisch an eine Identitaet binden | war anwendbar |
| SDK-004 | high | CORS-Exposure von `Mcp-Session-Id` | war anwendbar |
| SCALE-002 | high | Stateful Load Balancing fuer Streamable HTTP | war anwendbar |

Das ist kein Befund gegen den Server, sondern gegen das Katalogmodell: Es
unterstellt, dass ein Server eine Epoche spricht. Waehrend der Migration
sprechen Server beide, und die Baseline-Stufe nimmt dann eine Haelfte aus der
Messung, ohne dass irgendwo etwas rot wird — dieselbe Fehlerklasse, die
`OPS-005` beschreibt («was nicht gelaufen ist, sieht aus wie bestanden»).

Nicht gemessen und hier ausdruecklich nicht behauptet: ob SEC-009 an diesem
Server ueberhaupt erfuellbar waere. Der Check verlangt eine Bindung
`user_id:session_id`; dieser Server kennt keine Nutzeridentitaet, die
Authentisierung laeuft ueber einen gemeinsamen API-Key gegen die Upstream-API.
Ob das ein `n/a`, ein `partial` oder ein Befund ist, entscheidet die naechste
Katalogfassung, nicht dieser Lauf.
