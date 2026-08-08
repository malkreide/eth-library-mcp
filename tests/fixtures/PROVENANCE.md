# Herkunft der Fixtures

**Erzeugt von `scripts/record_fixtures.py`. Nicht von Hand pflegen.**

Aufgezeichnet am **2026-08-08** von `api.library.ethz.ch`.

Ohne Datum ist «aufgezeichnet» nach zwei Jahren von «ausgedacht» nicht
mehr zu unterscheiden — die Datei sieht gleich aus.

## Was hier aufgezeichnet ist, ist der Vertrag und nicht die Antwort

Die Discovery-API verlangt einen Schluessel; ohne ihn gibt es keine
Antwort, die man datieren koennte. Aufzeichenbar ist trotzdem etwas,
und zwar genau das, woran der Befund haengt: **welche Routen das
Gateway fuehrt.** Es routet vor der Schluesselpruefung, also
unterscheidet es selbst zwischen «Route da, Schluessel fehlt» (401)
und «Route gibt es nicht» (404).

Die beiden `control_*`-Zeilen in `api_routes.json` gehoeren zur
Messung und sind kein Beiwerk. Ohne sie belegt die Aufzeichnung nur,
dass jemand einen 404 bekommen hat; mit ihnen belegt sie, was das
Gateway unterscheidet. Der Unterschied zwischen der eigenen
Adressliste und dem Bestand der Quelle ist in diesem Portfolio schon
zweimal verwechselt worden.

## `api_routes.json`

- **Quelle:** `https://api.library.ethz.ch/…`
- **Aufgezeichnet:** 2026-08-08
- **Auswahl:** Statuscode je Pfad, ohne API-Key abgefragt — samt zweier Kontrollen mit erfundenen Pfaden. Erst die Kontrollen machen aus «ich bekomme 404» die Aussage «diese Route fuehrt das Gateway nicht»: Es routet vor der Schluesselpruefung, also heisst 401 «Route da» und 404 «Route weg»
- **Groesse:** 1133 B
- **SHA-256:** `98b2d19ebf07d192f37c5d6d105dc433ee648d7bd9f5c4f06589ed94633bd1f4`

## NICHT aufgezeichnet

### `discovery_*.json`

- **Quelle:** `https://api.library.ethz.ch/discovery/v1/resources`
- **Grund:** ETH_LIBRARY_API_KEY nicht gesetzt — die Discovery-API antwortet ohne Schluessel mit HTTP 401 (`FailedToResolveAPIKey`). NICHT aufgezeichnet.

Diese Payloads stehen weiterhin als Literale im Testmodul. Sie sind
damit **ausgedacht** und tragen kein Datum — das ist der
Ist-Zustand und keine Nachlaessigkeit dieses Laufs. Wer einen
Schluessel hat, setzt `ETH_LIBRARY_API_KEY` und laesst das Skript
erneut laufen.

Die 401 ist am Pfad des Servers selbst gemessen, nicht an einem
benachbarten — und die Kontrollen oben zeigen, dass sie
«Schluessel fehlt» heisst und nicht «Route weg».
