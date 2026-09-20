# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier dokumentiert.
Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

---

## [Unreleased]

### Behoben — ein Fehlschlag der Quelle sah aus wie eine Antwort (FID-003, SEC-028)

Zwei `high`-Befunde des Re-Audits, beide an derselben Stelle: Ein Transport-,
Autorisierungs- oder Policy-Fehler erreichte den Aufrufer als **gewoehnliches,
erfolgreiches Tool-Result**.

Gemessen am 19.9.2026 ueber den echten ASGI-Stack: `httpx.ConnectError` ergab
`isError: False` mit «Verbindungsfehler. Internetverbindung pruefen.» im
Ergebnisfeld. Die Positivkontrolle derselben Messung zeigte, dass der
Fehlerkanal existiert und funktioniert — ein Validierungsfehler kam sehr wohl
mit `isError: True` an. Der Server hat ihn fuer Ausfaelle der Quelle nur nie
benutzt.

Was sich am Draht aendert:

| Ausgang | vorher | jetzt |
|---|---|---|
| Treffer | `isError: false` | unveraendert, dazu `returned`/`total` |
| Null Treffer | `isError: false`, Hinweis im Fliesstext | dazu `hint` als Feld |
| 401 / 403 / 404 / 429 / 5xx | **`isError: false`** | `isError: true` |
| Zeitueberschreitung, Verbindungsfehler | **`isError: false`** | `isError: true` |
| Gesperrter Host (Egress) | **`isError: false`**, «Unbekannter Fehler» | `isError: true`, nennt Host und Allow-List |

- **Der 404 auf einer Suche ist keine Leermenge mehr.** Der Zweig lautete
  woertlich «Keine Ergebnisse oder Endpunkt nicht gefunden (HTTP 404). Bitte
  Suchanfrage oder API-Endpunkt pruefen.» — eine Aussage ueber den Bestand und
  eine ueber die Konfiguration in einem Satz. `BUG-02` war in diesem Repo genau
  der zweite Fall («Route weg, HTTP 404») und wurde hier als moegliche
  Leermenge angeboten. Die Meldung sagt jetzt, dass nicht gesucht wurde, und
  zeigt auf Basis-URL und Endpunkt statt auf die Query.
- **Der Leermengen-Hinweis steht in einem Feld**, nicht nur im Text:
  `structuredContent` traegt `returned`, `total` und `hint`. `hint` ist
  ausschliesslich bei `returned == 0` gesetzt; `ergebnis()` weist die
  Kombination «Hinweis neben Treffern» als Fehler ab, statt sie einer
  Konvention zu ueberlassen.
- **Zwei Werkzeuge nannten bei null Treffern ueberhaupt keinen naechsten
  Schritt.** `eth_search_archive` und `eth_search_by_type` meldeten bloss
  «Keine Treffer»; beide nennen jetzt den Filter, der die Suche einschraenkt,
  und eine Abfrage, die man woertlich absetzen kann.
- **`eth_get_resource` erfindet keine leere Huelle mehr.** Antwortete die
  Quelle mit `docs: []`, lief das in `_format_resource_detail(data)` und
  erzeugte ein Dokument mit der Ueberschrift «Kein Titel» — etwas, das wie ein
  Datensatz aussah. Jetzt: Leermenge mit Hinweis auf die Herkunft der MMS-ID.

**SEC-028 — der Policy-Verstoss ist keine Stoerung.** `_handle_error` mit
einem `PermissionError` aus dem Egress-Guard ergab gemessen «Fehler bei Suche:
Unbekannter Fehler. Bitte spaeter erneut versuchen.» — zeichengleich mit dem
Ergebnis fuer ein `ValueError('boom')`, und mit einem **Wiederholungsrat fuer
eine Absage, die bei jedem Versuch gleich ausfaellt**. Fuer das Modell las sich
eine Konfigurationsentscheidung wie ein Ausfall.

- Neue Typen in `client.py`: `EgressError(PermissionError)` als Basis,
  `EgressPolicyViolation` mit `retryable = False`. Die Basis bleibt bewusst
  `PermissionError`, damit ein bestehendes `except PermissionError` weiter
  greift — die Unterscheidung entsteht eine Ebene darunter, nicht durch
  Wegnehmen.
- `retryable` ist ein **Feld, das Code liest**: `_handle_error` entscheidet
  daran, ob die Meldung einen Wiederholungsrat traegt. Eine Unterscheidung
  ueber den Meldungstext braeche bei der ersten Umformulierung.
- Einen `EgressResolutionError` fuer die transiente Haelfte des Checks gibt es
  bewusst **nicht**: Dieser Guard loest nichts auf, er vergleicht den Hostnamen
  gegen ein `frozenset`. Ein DNS-Aussetzer kommt als `httpx.ConnectError` an
  und hat dort laengst einen eigenen Zweig. Eine Klasse ohne Gegenstand waere
  die Fixture, die die Annahme ihres Autors kodiert und sie nicht widerlegen
  kann — kein Test koennte sie je ausloesen.

**Was das kostet, ausdruecklich benannt.** Die fuenf datenliefernden Werkzeuge
sind von `-> str` auf `-> CallToolResult` umgestellt. Damit faellt ihr
`outputSchema` aus `tools/list`: Das SDK leitet das Schema aus der
Rueckgabe-Annotation ab und bietet keinen Weg, eines von Hand zu deklarieren.
Verloren geht `{"result": {"type": "string"}}` — ein Schema, das sagte, das
Werkzeug gebe eine Zeichenkette zurueck, und sonst nichts. Der Markdown-Block
bleibt unveraendert; eine Rueckgabe als Pydantic-Modell haette beides
deklariert und den Textblock zu einem JSON-Dump gemacht. Die Form von
`structuredContent` steht in `docs/ARCHITECTURE.md` und in jeder
Werkzeugbeschreibung.

**Gegenprobe.** `scripts/gegenprobe.py` faehrt jetzt **13 von 13** Mutationen,
alle schlagen an — die sechs aus OPS-010 plus sieben neue:

| Mutation | Tests rot |
|---|---|
| M5 Fehlerkanal: `raise ToolError` -> `return ergebnis` (Stand 0.4.1) | 7 |
| M6 Egress-Zweig in `_handle_error` abgeschaltet | 5 |
| M7 Wiederholungsrat unbedingt statt am Diskriminator | 2 |
| M8 `hint` im strukturierten Feld auf `None` | 3 |
| M9 Waechter «kein Hinweis neben Treffern» abgeschaltet | 1 |
| M10 404-Wortlaut von 0.4.1 wiederhergestellt | 1 |
| M11 Verbindungsfehler nennt wieder die Allow-List | 1 |

192 Tests (vorher 164), alle Gates gruen auf 3.11, 3.12 und 3.13.

**Nicht behoben, und warum.** Die Gaps von FID-003 nennen ausserdem, dass der
Leermengen-Hinweis auch bei einer *Strukturabweichung* der Antwort erscheint —
wenn die Felder eine Ebene tiefer liegen, zaehlt der Leser null Treffer und
haengt den Hinweis an. Das ist der Gegenstand von **FID-006** («Struktur
bestaetigen, bevor gezaehlt wird») und ein eigener Befund; er bleibt offen.

### Behoben — vier Zusicherungen waren behauptet, nicht geprueft (OPS-010)

Der Re-Audit vom 19.9.2026 fuhr sechs Mutationen gegen die Suite. Zwei
schlugen an, **vier nicht**: Egress-Allow-List, Werkzeug-Annotationen,
generische Fehlermaskierung und die Quellenangabe je Antwort liessen sich alle
entfernen, ohne dass ein einziger Test rot wurde. Alle vier standen im Code,
waren in der Doku beschrieben und von nichts festgehalten.

Nach diesem Stand schlagen **6 von 6** an:

| Mutation | vorher | jetzt |
|---|---|---|
| Egress-Pruefung entschaerft | 0 rot | 2 rot |
| `readOnlyHint` geloescht | 0 rot | 1 rot |
| Maskierung gibt `{Typ}: {e}` aus | 0 rot | 1 rot |
| Quellenangabe nicht angehaengt | 0 rot | 2 rot |
| CORS-Wildcard (Positivkontrolle) | 1 rot | 1 rot |
| Upstream-Body durchgereicht (Positivkontrolle) | 1 rot | 1 rot |

- **`scripts/gegenprobe.py`** faehrt genau diese Mutationen und meldet, welcher
  Test dabei faellt. Es gibt das Skript, weil die Handarbeit gemessen vier von
  sechs Luecken uebersehen hat -- und weil CLAUDE.md die Gegenprobe zwar
  verlangt, aber als Agenten-Anweisung, nicht als Beitragsanleitung.

  Drei Eigenschaften, die je eine Messung gekostet haben: Es zieht die
  **Grundlast** ab (die Arbeitskopie hat kein `.git`, also fallen dort 13 Tests
  in jedem Lauf -- der erste Lauf meldete allein deshalb fuer jede Mutation
  «OK»), es fuehrt **Positivkontrollen** mit (bleiben die stumm, hat der Lauf
  nichts gemessen), und es scheitert **laut** an einem veralteten Suchmuster
  statt still zu ueberspringen.

- **`tests/test_zusicherungen.py`**, 17 Faelle, jeder mit Positivkontrolle. Die
  Egress-Sperre wird an der **Routen-Zaehlung** gemessen und nicht am
  Rueckgabetext: Eine gesperrte und eine gescheiterte Anfrage erzeugen
  denselben Text (SEC-028), die Zahl der ausgehenden Anfragen unterscheidet sie
  eindeutig. Die Annotationen werden am Draht ueber `tools/list` gemessen, nicht
  im Quelltext -- eine Annotation, die unterwegs verlorengeht, ist fuer einen
  Client nicht vorhanden.

- **`tests/test_tools.py`**: Das `or` in
  `assert "Unbekannter Fehler" in out or "Egress denied" in out` ist weg. Es
  machte den Test unabhaengig davon gruen, ob die Sperre existiert -- ohne sie
  laeuft die Anfrage in respx' `AllMockedAssertionError` und erzeugt genau den
  ersten Text.

- **`tests/test_server.py`**: `test_format_resource_detail()` hatte ausser dem
  Docstring keinen Koerper. Er konnte nicht fallen und zaehlte trotzdem als
  einer der gruenen; per AST ueber alle Testdateien war er der einzige seiner
  Art. Jetzt mit Koerper -- und der deckte sofort auf, dass er nicht einmal
  seinen Import brauchte.

- **`CONTRIBUTING.md` / `.de.md`** beschreiben die Gegenprobe. Bis hierhin
  ergab `grep -cniE 'gegenprobe|mutation'` dort je **0**.


## [0.4.1] – 2026-09-19

Ein Sicherheitsfix und vier Stellen, an denen 0.4.0 etwas Falsches ueber sich
selbst gesagt hat. Alle fuenf stammen aus dem Re-Audit gegen den 120-Check-
Katalog (`audits/2026-09-19T171257-Z-eth-library-mcp/`).

### 🔐 Sicherheit — der API-Schluessel stand im Klartext im Log

- **`ETH_LIBRARY_API_KEY` wurde bei **jeder** Anfrage nach stderr
  protokolliert.** Nicht vom eigenen Log dieses Servers — `client.py` schreibt
  `has_key=True` statt des Werts —, sondern von httpx: `configure_logging()`
  stellt den Root-Logger auf INFO, und httpx gibt dabei die vollstaendige URL
  aus, samt des als Query-Parameter angehaengten Schluessels. Gemessen:

  ```
  HTTP Request: GET .../resources?q=test&apikey=sk-GEHEIM-… "HTTP/1.1 200 OK"
  ```

  `SECURITY.md` und `docs/secret-management.md` sagten beide woertlich, der
  Schluessel werde nie geloggt. Beide Saetze waren seit `0.1.0` falsch.

  **Wer 0.4.0 oder frueher produktiv betrieben hat, sollte den Schluessel als
  kompromittiert behandeln** und ihn unter developer.library.ethz.ch neu
  ausstellen lassen — jedenfalls dann, wenn die stderr-Ausgabe irgendwo
  aufgezeichnet wurde: in einem Log-Shipper, einer Container-Runtime, einer
  CI-Ausgabe oder einem Terminal-Mitschnitt.

- **Redigiert wird jetzt bei der Erzeugung jedes Logdatensatzes**
  (`logging.setLogRecordFactory`), beim Einmischen von `extra`
  (`Logger.makeRecord`) und zusaetzlich als structlog-Prozessor. Drei Stellen,
  weil die drei Wege sich keinen gemeinsamen Punkt teilen, an dem alles
  vorbeikaeme:

  | Weg | Wo das Geheimnis steht | Wo redigiert wird |
  |---|---|---|
  | httpx-Anfragezeile | `record.args` (als `httpx.URL`-Objekt) | Datensatz-Fabrik |
  | Ausnahme-Traceback | `record.exc_info`, vom Formatter **nach** der Nachricht angehaengt | `record.exc_text` in der Fabrik |
  | `extra`-Felder | `record.__dict__`, **nach** der Fabrik eingemischt | `Logger.makeRecord` |
  | eigene Logzeilen | structlog-Ereignis | structlog-Prozessor |

  Die beiden mittleren Wege hat ein Codex-Review auf PR #63 gefunden, nachdem
  der erste behoben war. Beide sind danach nachgemessen worden statt
  uebernommen — vor dem Fix gab der Traceback
  `ValueError: request failed for url ...&apikey=sk-LECK-TEST-12345` aus und
  das `extra`-Feld dieselbe URL.

  **Der Traceback wird nicht durch Aendern der Ausnahme entschaerft.** Die
  gehoert dem Aufrufer und wird anderswo weiterverwendet. Stattdessen
  formatiert die Fabrik den Traceback selbst, redigiert ihn und legt ihn in
  `record.exc_text` ab — ein Feld, das der Formatter benutzt, wenn es gesetzt
  ist, statt `formatException` aufzurufen.

  **`exc_info` bleibt dabei ausdruecklich unberuehrt.** Wer `record.__dict__`
  stumpf ueber `str()` redigiert, macht aus dem `(Typ, Wert, Traceback)`-Tripel
  eine Zeichenkette. Nichts schlaegt fehl — aber jeder Handler, der danach
  `formatException` aufruft, bekommt Schrott. Ein Test haelt das Tripel fest.

  Die erste Fassung war ein Filter am Handler. Sie funktionierte — und ein Test
  zeigte, dass sie von der **Handler-Reihenfolge** abhing: Ein zweiter Handler
  am selben Logger haette den Datensatz vor der Redaktion zu sehen bekommen.
  Ein Geheimnisschutz, der von einer Reihenfolge abhaengt, ist keiner.

  **Was hier nicht behoben ist:** Der Schluessel steht weiterhin in der URL. Ihn
  in einen Header zu verschieben waere die Behebung an der Wurzel, aendert aber
  die Authentisierung gegenueber der Quelle — und ob die ETH-API einen Header
  akzeptiert, ist ohne Schluessel und ohne Netzzugang nicht pruefbar. Eine
  Vermutung darueber gehoert nicht in den Auslieferungspfad.

### Behoben — vier Stellen, die 0.4.0 uebersehen hat

Der 0.4.0-Eintrag unten fuehrt dieselbe Aufraeumarbeit fuer `pyproject.toml`,
`server.json`, beide READMEs, `EXAMPLES.md` und `docs/` auf. Diese vier standen
nicht auf der Liste:

- **Die `instructions` bewarben `eth_search_persons`** («Ebenfalls verfuegbar:
  Personen-Suche mit Wikidata-Verlinkung») — also das Werkzeug, das derselbe
  Release entfernt hat. Sie gehen im Handshake und in `server/discover` an jeden
  Client. Der Server stellte sich mit einer Faehigkeit vor, die sein eigener
  Test (`test_no_tool_still_offers_the_persons_api`) verbietet.
- **`eth_library_info` meldete `**Version:** 0.3.0`**, waehrend das Paket bei
  0.4.0 stand. Das ist die einzige Versionsangabe, die ein Nutzer dieses Servers
  zu sehen bekommt.
- **`SECURITY.md` und `SECURITY.de.md` nannten `mcp[cli]>=1.0.0,<2.0.0`**,
  gepinnt ist `>=2.0.0,<3` — die Deckel der Vorgaenger-Major.
- **`README.de.md` nannte Protokollversion `2025-06-18`.** Die englische Fassung
  war in 0.4.0 auf `2026-07-28` nachgezogen worden, die deutsche nicht; sie
  widersprach sich damit selbst, weil ihr eigener Abschnitt weiter unten
  `2026-07-28` fuehrt.

Ausserhalb dieses Repos liegt eine fuenfte Stelle: Die **Repository-Beschreibung
auf GitHub** sagt weiterhin «via Discovery & Persons API». Sie hat kein Gate und
laesst sich nur in den Repository-Einstellungen aendern.

### Geaendert — Gates, die jetzt hinsehen

- **`scripts/check_version_sync.py` erkennt eine dritte Form.** Bisher kannte es
  den User-Agent und die `__version__`-Zuweisung. Die Zahl in
  `eth_library_info` stand in keiner von beiden Formen, und das Gate meldete
  ausdruecklich «keine hartkodierte Version in src/» und exitete 0. Es war nicht
  zu schwach eingestellt — es hat an dieser Stelle nicht hingesehen. Das ist die
  teuerste Sorte Fehlbefund, weil ein gruenes Gate die Beschaeftigung mit der
  Frage beendet.
- **Neue Tests** (`tests/test_geheimnis_redaktion.py`,
  `tests/test_selbstauskunft.py`, 15 Faelle). Jede Zusicherung ist einzeln
  neutralisiert und die zugehoerigen Tests fallen gesehen worden.

  Die Gegenprobe hat dabei einen Fehler in einem der neuen Tests selbst
  gefunden: Der Deckel-Vergleich trennte den Paketnamen auf der einen Seite an
  `[` und auf der anderen nicht, fand `mcp[cli]` deshalb nie im Woerterbuch und
  uebersprang ihn stillschweigend. Er blieb gruen, als die Mutation genau den
  Deckel zuruecksetzte, gegen den er geschrieben ist — dieselbe Fehlerklasse,
  gegen die dieser Release antritt, im Werkzeug dagegen.

## [0.4.0] – 2026-09-19

Zwei brechende Aenderungen, beide bewusst: Die CORS-Wildcard ist gefallen, und
ein Werkzeug ist verschwunden, weil die API dahinter verschwunden ist. Dazu die
Protokollrevision `2026-07-28`, die jetzt nicht mehr nur bedient, sondern auch
gemessen wird.

### ⚠️ Brechende Aenderungen

- **`allow_origins` ist nicht mehr `["*"]`.** Ohne gesetzte
  `ETH_LIBRARY_CORS_ORIGINS` laesst der Server keine Browser-Origin mehr durch.
  Wer den bisherigen Zustand behalten will, setzt die Variable ausdruecklich —
  Einzelheiten unter «Geaendert».
- **Das Werkzeug `eth_search_persons` ist entfernt.** Die Werkzeugliste
  schrumpft von 7 auf 6. Kein Ersatz: Die Persons-API ist vom Gateway
  verschwunden, nicht gesperrt. Einzelheiten unter «BUG-02 ist erledigt».

### Geaendert — die Metadaten nennen keine entfernte API mehr

- **Beschreibung in `pyproject.toml` und `server.json`.** Beide sagten
  «Discovery **and Persons** APIs». Seit dem `serverInfo`-Eintrag oben geht die
  `pyproject`-Beschreibung nicht mehr nur an PyPI, sondern haengt als
  `description` an jeder Antwort der modernen Aera — der Server haette sich mit
  diesem Release jedem Client mit einer Faehigkeit vorgestellt, die derselbe
  Release entfernt. `server.json` haette dasselbe an die MCP-Registry gemeldet.

- **Dieselbe Behauptung in der Dokumentation.** `SECURITY.md`/`.de` sprachen von
  «alle 7 Tools» und trugen einen BUG-02-Hinweis, der das Werkzeug noch als
  vorhanden, aber defekt beschrieb. `EXAMPLES.md` verwies fuer den
  Anwendungsfall «nach Personen suchen» auf ein Werkzeug, das es nicht gibt —
  dort steht jetzt der Ersatzweg (`eth_search_resources` mit
  `creator,contains,<Name>`). Die READMEs fuehrten eine leere
  Persons-Tabelle und nannten den API-Key fuer eine API, die nicht mehr
  angesprochen wird. In `docs/` beschrieben Scope-, Datenquellen-, Egress- und
  Architektur-Notiz die Persons-API als laufend.

  Zwei Nebenbefunde beim Nachmessen: Die Egress-Allow-List bleibt unveraendert,
  weil Discovery und Persons sich **denselben** Host `api.library.ethz.ch`
  teilten — es gab keinen Persons-Eintrag zu streichen. Und
  `docs/network-egress.md` nannte fuer `ALLOWED_EGRESS_HOSTS` die falsche Datei
  (`server.py` statt `client.py`, seit dem Modul-Split von `0.3.0`).

### Behoben

- **Der Server meldete allen Clients die leere Version `""`.** Spec `2026-07-28`
  stempelt den `Implementation`-Block in **jedes** Resultat der modernen Aera
  (`_meta.io.modelcontextprotocol/serverInfo`, spec #3002); die Revisionen davor
  fuehrten ihn nur im `initialize`-Resultat. Aus einem einmaligen Feld wurde
  damit eine Angabe, die bei jedem Aufruf wiederholt wird — und `version` ist im
  `Implementation` dieser Revision ein **Pflichtfeld**.

  Das SDK setzt nichts ein und sagt es selbst
  (`mcp/server/lowlevel/server.py::server_info`):

  ```
  An unversioned server reports an empty `version`;
  the SDK never substitutes its own.
  ```

  Gemessen am zusammengebauten ASGI-Stack, vorher:

  ```
  modern  server/discover -> _meta.serverInfo = {"name": "eth_library_mcp", "version": ""}
  legacy  initialize      ->       serverInfo = {"name": "eth_library_mcp", "version": ""}
  ```

  In beiden Aeren, bei jedem Aufruf — waehrend `server.json` der Registry
  `0.3.4` meldete. Das Manifest sagte mehr ueber diesen Server aus als der
  Server selbst.

  Neu deklariert `MCPServer` `version`, `title`, `description` und
  `website_url`. Drei der vier Werte kommen aus den Paket-Metadaten
  (`importlib.metadata`) und koennen deshalb nicht von `pyproject.toml`
  wegdriften — dieselbe Begruendung wie bei `__version__`, mit dem Unterschied,
  dass `scripts/check_version_sync.py` ausschliesslich Zahlen synchron haelt und
  eine handgepflegte Beschreibung in `src/` also gar kein Gate haette. `title`
  ist der einzige Wert ohne Quelle ausserhalb: `name` ist der programmatische
  Bezeichner, `title` der Anzeigename fuer Menschen.

  `icons` bleibt ungesetzt — das Repo fuehrt keine, und ein erfundener Pfad
  waere eine Zusicherung ueber eine Datei, die es nicht gibt.

  Gefunden hat es keine der bestehenden Suiten, und zwar aus einem benennbaren
  Grund: `tests/test_protocol_version.py` fuhr ausschliesslich
  `initialize`-Anfragen. Die moderne Aera, die die README seit zwei Fassungen
  als bedient auswies, war damit **nie** gemessen worden — der Stempel, den nur
  sie traegt, konnte gar nicht auffallen. `tests/test_server_identity.py` fuehrt
  jetzt einen echten modernen POST durch `build_http_app()`, samt
  Negativkontrolle gegen einen `MCPServer` ohne Identitaet: faellt sie, setzt
  das SDK inzwischen selbst eine Version ein und die uebrigen Zusicherungen
  messen nicht mehr diesen Server.

- **`ETH_LIBRARY_CORS_ORIGINS` war wirkungslos.** Die Variable wurde eine
  Version zuvor eingeführt, konnte aber nicht tun, was sie versprach:
  `build_http_app` übergab weder `transport_security=` noch `host=`. Das ist
  nicht «ungeschützt», sondern falsch geschützt — `streamable_http_app`
  synthetisiert bei fehlendem `transport_security` und Loopback-`host` selbst
  eine Freigabeliste (`mcp/server/mcpserver/server.py`), und die kennt nur
  Loopback.

  Gemessen am zusammengebauten ASGI-Stack, mit gesetzter Variable:

  ```
  Host 127.0.0.1:8000, Origin https://client.example -> 403 Invalid Origin
  Host testserver,     Origin https://client.example -> 421 Invalid Host
  Host mcp.example.ch, ohne Origin                   -> 421 Invalid Host
  ```

  CORS liess durch, das SDK wies ab. Danach jeweils `200`, und eine fremde
  Origin bleibt bei `403`.

  Damit ist auch der in `README.md` dokumentierte Bind `--http --host 0.0.0.0`
  wieder benutzbar: er antwortete zuvor auf **jede** Anfrage 421, unabhängig
  von der Origin. Dafür gibt es neu `ETH_LIBRARY_ALLOWED_HOSTS` — unter welchem
  Namen der Prozess erreichbar ist, kann er aus der Bind-Adresse nicht
  ableiten. Bleibt die Variable auf einem Nicht-Loopback-Bind leer, wird der
  Schutz mit einer Warnung abgeschaltet, statt ihn mit einer geratenen Liste
  zu simulieren.

  Die bestehende CORS-Suite konnte das nicht finden: sie schickt ausschliesslich
  Preflights, und die beantwortet `CORSMiddleware`, bevor die App erreicht wird.
  `tests/test_transport_security.py` schickt deshalb echte `initialize`-Anfragen.

### Geändert

- **BRECHEND: `allow_origins` war das Literal `["*"]`.** Jede Website im Netz
  durfte diesen Server aus dem Browser eines Besuchers aufrufen, und es gab
  keine Umgebungsvariable, mit der man das haette einschraenken koennen — die
  Wildcard stand fest verdrahtet in `build_http_app`.

  Gemessen vorher am zusammengebauten ASGI-Stack: ein Preflight von
  `https://evil.example` bekam `Access-Control-Allow-Origin: *`, genau wie
  `https://client.example`. Danach ohne Konfiguration gar kein
  `Access-Control-Allow-Origin` mehr.

  Neu liest `configured_origins()` die Variable `ETH_LIBRARY_CORS_ORIGINS`
  (kommasepariert, Default leer). Die Wildcard bleibt erreichbar, muss aber
  verlangt werden, und der Server protokolliert sie dann als `warning`; ein
  leerer Wert wird als `info` vermerkt.

  **Wer den bisherigen Zustand behalten will, setzt
  `ETH_LIBRARY_CORS_ORIGINS=*`.** stdio- und Nicht-Browser-Clients sind
  unberuehrt — CORS regelt ausschliesslich Browser.

### Behoben

- **`DELETE` fehlte in `allow_methods`.** Auf streamable-http beendet die
  Methode eine Session ausdrücklich; der Preflight wies sie mit 400 ab. Ein
  Browser-Client konnte damit Sessions öffnen, aber nie schliessen — sie liefen
  erst am Timeout aus. Das SDK bedient sie sehr wohl: `_handle_delete_request`
  in `mcp.server.streamable_http`, und dessen eigene 405-Antwort wirbt mit
  `Allow: GET, POST, DELETE`. Die Freigabeliste war schmaler als der Server.

  Gemessen vorher: `Preflight DELETE -> 400` bei
  `Access-Control-Allow-Methods: GET, POST, OPTIONS`. Danach `200` und
  `GET, POST, DELETE, OPTIONS`.

### Behoben

- **Browser-Clients scheiterten am Preflight.** Spec `2026-07-28` routet eine
  Streamable-HTTP-Anfrage über `Mcp-Method`, `Mcp-Name` und
  `Mcp-Protocol-Version`; die CORS-Freigabeliste nannte keinen davon, dafür mit
  `Mcp-Session-Id` den Session-Header, der für sich genommen keine Anfrage
  routet. Ein Browser darf einen nicht safelisteten Header nicht senden, wenn
  der Server ihn nicht nennt: die Anfrage starb vor dem ersten MCP-Byte,
  während stdio und Python weiterliefen. Deshalb war nichts rot.

### Hinzugefügt

- **`build_http_app()`**, herausgezogen aus `_run_http`, damit die CORS-Schicht
  überhaupt prüfbar ist. `_run_http` ruft die neue Funktion auf; am Verhalten
  ändert sich nichts.

- **Frischehinweise auf den auflistenden Methoden** (SEP-2549, Spec
  `2026-07-28`): `tools/list`, `resources/list`, `resources/templates/list`,
  `prompts/list` und `server/discover` antworten mit `ttlMs` 300000 und
  `cacheScope` `public`. `resources/read` und `prompts/get` bleiben ohne
  Hinweis: das wäre eine Zusicherung über den Inhalt statt über das Verzeichnis.

- **Protokoll-Gate: beide Spec-Aeren gepinnt und geprueft**
  (`tests/test_protocol_version.py`). `mcp` 2.x bedient zwei Aeren ueber
  denselben Server — den `initialize`-Handshake, der bei `2025-11-25`
  deckelt, und den Pro-Request-Envelope, der `2026-07-28` erreicht.
  `LATEST_PROTOCOL_VERSION` ist ein Alias auf die **moderne** Aera; wer nur
  dagegen pinnt, laesst genau die Aera frei wandern, die heutige Clients
  aushandeln. Beide sind jetzt einzeln gepinnt, ein Dependabot-Bump von
  `mcp` kann keine davon still verschieben.

  Nachgemessen statt aus Konstantennamen geschlossen: ein echter `initialize`
  durch den zusammengebauten ASGI-Stack. Ein Client, der ueber den Handshake
  nach `2026-07-28` fragt, bekommt `2025-11-25` zurueck.

  Beide READMEs beschreiben die Aeren; ein Test haelt jede Sprache einzeln
  dagegen — im Portfolio sind EN und DE desselben Repos schon dreimal
  auseinandergelaufen, weil nur eine Fassung nachgezogen wurde.

- **`Mcp-Session-Id` ist weiterhin freigegeben — und das steht jetzt in einem
  Test statt in einem Satz.** Der Docstring von `tests/test_cors.py` nannte den
  Header die Spur einer Mechanik, die `2026-07-28` abgeschafft habe. Das stimmt
  nicht: `mcp` 2.x bedient beide Protokoll-Aeren, die Session gehoert zur
  Handshake-Aera, und der Server gibt den Header nicht ohne Grund auch in
  `expose_headers` frei.

  Nachgemessen statt aus Spec-Text geschlossen: `MCP_SESSION_ID_HEADER` steht
  unveraendert in `mcp/server/streamable_http.py`, und ein echter `initialize`
  durch den zusammengebauten ASGI-Stack bekommt eine Session-ID im
  Antwort-Header zurueck.

  `test_der_session_header_ist_weiterhin_freigegeben` haelt beides fest. Die
  Gegenprobe zeigt, dass es die Luecke wirklich gab: nimmt man den Header aus
  der Freigabeliste, faellt genau dieser eine Test, und die sieben bestehenden
  bleiben gruen.

### Behoben — BUG-02 ist erledigt, durch Entfernen des Werkzeugs

Im Code und in beiden READMEs stand seit laengerem dieselbe Notiz:

> ⚠ BUG-02: Der Persons-API-Endpunkt (`/persons/v1/persons`) gibt aktuell HTTP
> 404 zurueck. Die korrekte URL muss via `developer.library.ethz.ch`
> verifiziert werden.

Verifiziert ist sie jetzt, und **es gibt keine korrekte URL**. Die Persons-API
ist vom Gateway verschwunden, nicht bloss verschlossen.

Entscheiden laesst sich das ohne API-Key, weil das Gateway **vor** der
Schluesselpruefung routet:

| Pfad | Antwort ohne Key | heisst |
|---|---|---|
| `/discovery/v1/resources` | **401** | Route da, Schluessel fehlt |
| `/discovery/v1/resources/991` | **401** | auch Unterpfade |
| `/discovery/v1/<erfunden>` — KONTROLLE | **404** | Route nicht da |
| `/persons/v1/persons` | **404** | |
| `/persons/v1` | **404** | |
| `/persons/v2/persons` — KONTROLLE | **404** | |

Die beiden Kontrollzeilen sind der ganze Punkt. Ohne sie belegt die Messung
nur, dass jemand einen 404 bekommen hat — mit ihnen belegt sie, was das Gateway
unterscheidet. Genau diesen Unterschied, die eigene Adressliste gegen den
Bestand der Quelle, hat dieses Portfolio schon zweimal verwechselt.

`eth_search_persons` ist deshalb **entfernt** und nicht mit einer schoeneren
Fehlermeldung versehen worden. Eine Faehigkeit anzubieten, die es nicht geben
kann, ist derselbe Fehler wie ein leeres Ergebnis, nur lauter — und das Werkzeug
stand mit Warnhinweis in der Werkzeugliste, also dort, wo ein Modell zuerst
hinsieht. Mit ihm fallen `SearchPersonsInput`, der Persons-Parser-Aufruf und die
Zaehlung «7 Tools · 3 APIs» weg, die auf beiden READMEs stand. Es sind sechs
Werkzeuge und eine API.

### Hinzugefuegt — aufgezeichnet wird der Vertrag, nicht die Antwort

**`scripts/record_fixtures.py`** zeichnet auf, was ohne Schluessel aufzeichenbar
ist: die Routen-Erhebung samt Kontrollen, mit Datum und SHA-256 in
`tests/fixtures/PROVENANCE.md`.

Die Discovery-Payloads bleiben **NICHT aufgezeichnet** — die API verlangt einen
Schluessel, und ein Datum anzuschreiben, das sie nie hatten, waere schlimmer als
die Luecke. Die 401 ist dabei am Pfad des Servers selbst gemessen, nicht an
einem benachbarten, und die Kontrollen zeigen, dass sie «Schluessel fehlt»
heisst und nicht «Route weg».

Das Skript bricht ab, wenn die Unterscheidung nicht mehr traegt: wenn Discovery
nicht mehr mit 401 antwortet, wenn ein erfundener Pfad nicht mehr 404 gibt, oder
wenn die Personen-API zurueckkommt — im letzten Fall gehoert das Werkzeug
wiederhergestellt und nicht die Fixture nachgezogen.

**`tests/fixture_data.py`** behandelt einen fehlenden Namen als Fehler statt als
leere Struktur.

### Hinzugefuegt — die ersten Live-Tests dieses Repositoriums

`pytest -m live` sammelte hier bisher **null** Tests ein. Nichts in diesem Repo
war je gegen die Quelle gehalten worden — bei 11 Inline-Payloads, dem groessten
Wert der unteren Haelfte der Portfolio-Rangfolge.

Die zwei neuen Live-Tests brauchen **keinen** API-Key und sagen trotzdem etwas:
Sie melden, wenn die Personen-API zurueckkommt (dann gehoert das Werkzeug wieder
her) und wenn Discovery seine Route verliert (dann sind fuenf Werkzeuge
betroffen). Ein Live-Test, der nur mit Zugangsdaten laeuft, laeuft in der Praxis
nie.

---

## [0.3.4] – 2026-07-31

### Hinzugefuegt

- **Der Server nennt jetzt seinen Namen.** Bisher ging gegenueber jedem
  Upstream der httpx-Default hinaus: der Betreiber der Datenquelle sah
  eine Bibliothek, nicht uns, und hatte keinen Weg, uns bei Fehlverhalten
  zu erreichen. Neu traegt jeden der 2 HTTP-Clients
  `eth-library-mcp/<version> (+github.com/malkreide/eth-library-mcp)`.

  Die Version stammt aus `importlib.metadata` und kann nicht getrennt vom
  Paket driften.

## [0.3.0] – 2026-05-29

Audit-Härtungs-Release. Über drei Remediation-Sprints wurden alle 20 Findings aus dem [mcp-audit-skill](https://github.com/malkreide/mcp-audit-skill)-Audit (run-id `2026-05-28T142641-Z-eth-library-mcp`, 38/68 Checks anwendbar) behoben. Ein Re-Audit (run-id `2026-05-28T184347-Z-eth-library-mcp`, identischer Catalog-Hash `091f446b…`) bestätigt: 36/36 anwendbare Checks PASS, 0 Findings, Production-Readiness erreicht.

### ⚠️ Breaking Changes

- **HTTP-Default-Bind** (`SEC-016`): `python -m eth_library_mcp.server --http` bindet jetzt auf `127.0.0.1` statt `0.0.0.0`. Für Public-Exposure muss `--host 0.0.0.0` explizit übergeben werden — und nur hinter Reverse-Proxy/Firewall. Migration: bestehende Deploy-Skripte um `--host 0.0.0.0` ergänzen oder hinter den Proxy verlagern.

### Hinzugefügt

- **Container-Sandbox** (`SEC-007`): `Dockerfile` (multi-stage, slim-base, non-root UID 1000) + `.dockerignore`. Empfohlene Laufzeit: `--read-only --tmpfs /tmp`.
- **Egress-Allow-List** (`SEC-021`): `ALLOWED_EGRESS_HOSTS` als `frozenset` mit Runtime-Gate in `_http_get`. Jeder Outbound-Call gegen einen nicht gelisteten Host wirft `PermissionError`. Doku: `docs/network-egress.md`.
- **CORS-Middleware** (`SDK-004`): HTTP-Transport wrappt die Starlette-App in `CORSMiddleware`. `Mcp-Session-Id` ist in `allow_headers` und `expose_headers` — Browser-MCP-Clients können den Header lesen.
- **Strukturiertes Logging** (`OBS-003`): `structlog` mit JSON-Output auf stderr. Vier Severity-Stufen aktiv genutzt (debug/info/warning/error). Ingestion via Datadog/CloudWatch/Loki ohne Custom-Parser möglich.
- **FastMCP Lifespan + Connection Pool** (`SDK-001`): `@asynccontextmanager`-Lifespan verwaltet einen geteilten `httpx.AsyncClient`. Spart TLS-Handshake pro Tool-Call.
- **Context-Injection** (`SDK-003`): Alle 6 Such-/Get-Tools akzeptieren `ctx: Context`. `ctx.warning()` auf Error-Pfaden, `ctx.report_progress()` für `limit > 50`, `ctx.info()` für Persons-No-Results.
- **Source-Attribution** (`CH-004`): Jede formatierte Ressource trägt eine `Quelle: ETH-Bibliothek (Public Domain) · …`-Zeile.
- **Tool-Layer-Tests** (`OPS-001`): `tests/test_tools.py` mit `respx`-Mocks deckt alle 7 Tools ab (13 neue Tests, 38 total). Regression-Tests für OBS-002 (kein Body-Leak) und SEC-021 (Egress-Block).
- **Stderr-Logging explizit** (`OBS-004`): `logging.basicConfig(stream=sys.stderr)` + `structlog.PrintLoggerFactory(file=sys.stderr)`. stdio JSON-RPC-stdout bleibt sauber.
- **Doku**: `docs/ARCHITECTURE.md`, `docs/data-sources.md`, `docs/network-egress.md`, `docs/scope-minimization.md`, `docs/secret-management.md`.
- **`.gitignore`** und **`.env.example`** (`ARCH-005`): Verhindert versehentliche Secret-Commits.
- **Audit-Artefakte** unter `audits/`: Profil, Verification-Results, Summary, Findings, Reports beider Audit-Läufe.

### Geändert

- **Modul-Split** (`ARCH-004`): `server.py` (1107 LOC) aufgeteilt in `client.py` (httpx + Lifespan + Egress), `formatting.py` (Markdown-Rendering, Error-Mapping), `logging_config.py` (structlog) und `server.py` (898 LOC — nur noch FastMCP-Tools). `server.py` re-exportiert die alten Namen — Import-Pfade bleiben kompatibel.
- **Error-Handling** (`OBS-002`): `_handle_error` leakt keinen Upstream-Response-Body (`e.response.text`) und keinen Exception-Klassennamen mehr an den LLM. Details landen im strukturierten stderr-Log.
- **Versionspinning** (`ARCH-012`): Upper Bounds auf alle Dependencies (`mcp[cli]>=1.0.0,<2.0.0`, `httpx>=0.27.0,<1.0.0`, `pydantic>=2.0.0,<3.0.0`).
- **README**: MCP Protocol Version 2025-06-18 deklariert; Cloud-Deployment-Sektion mit `--host`-Warnung erweitert.

### Sicherheit

| Audit-Check | Vorher | Jetzt |
|---|---|---|
| critical findings | 3 | 0 |
| high findings | 12 | 0 |
| medium findings | 5 | 0 |
| Production-readiness | nein | **ja** |

Vollständige Reports unter `audits/2026-05-28T184347-Z-eth-library-mcp/audit-report.md`.

### Dependencies

- **+** `structlog>=24.0.0,<26.0.0`

---

## [0.2.0] – 2026-03-04

### Behoben
- **BUG-01** `pyproject.toml`: Falscher Package-Pfad `src/eth_library_mcp` → `eth_library_mcp` (Installation via `pip install -e .` schlug fehl)
- **BUG-03** `sort`-Parameter: Beliebige Strings akzeptiert → `Literal["rank","title","author","date"]` (verhindert ungültige API-Anfragen)
- **BUG-04** `resource_type`-Parameter: Beliebige Strings akzeptiert → vollständiger `Literal`-Typ mit allen 10 gültigen Werten (verhindert stille Leerantworten)
- **BUG-06** Persons-Response-Parsing: Nur `persons`/`results`-Keys unterstützt → robustes Parsing mit `data`, `items`, `hits` + Logging bei unbekannter Struktur
- **BUG-07** HTTP-404-Fehlermeldung: Generische "ID prüfen"-Meldung auch bei Suchen → kontext-spezifische Meldungen (`is_search`-Parameter in `handle_api_error`)

### Entfernt
- **BUG-05** Ungenutzte Konstanten `RESEARCH_BASE_URL` und `ETHORAMA_BASE_URL` aus `api_client.py` entfernt

### Bekannte Probleme
- **BUG-02** Persons-API-Endpunkt (`/persons/v1/persons`) gibt HTTP 404 zurück. Die korrekte URL muss via [developer.library.ethz.ch](https://developer.library.ethz.ch) verifiziert werden. Das Tool `eth_search_persons` ist strukturell korrekt implementiert, aber erst nach URL-Verifikation funktionsfähig.

---

## [0.1.0] – 2026-03-01

### Hinzugefügt
- Initiale Implementierung mit 7 Tools, 3 APIs, 2 Resources, 2 Prompts
- Discovery API: `eth_search_resources`, `eth_get_resource`, `eth_search_archive`, `eth_search_by_type`, `eth_search_education`
- Persons API: `eth_search_persons`
- Dual Transport: stdio (lokal) + SSE (Cloud/Render.com)
- Graceful Degradation ohne API-Key (hilfreiche Fehlermeldung mit Registrierungslink)
- Schulamt-spezifisches Tool `eth_search_education` für Bildungsthemen
