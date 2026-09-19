## Finding: ARCH-013 — Alle Netz-Transportpfade identisch verdrahtet

**Severity:** high
**Status:** open
**Server:** eth-library-mcp
**Check-Reference:** ARCH-013
**Katalog-Referenz:** Sec 2.1
**Spec-Baseline:** (keine)
**Audit-Lauf:** 2026-09-19T171257-Z-eth-library-mcp

### Observed Behavior

Der Check ist **teilweise** erfuellt: Die tragenden Zusicherungen sind belegt, einzelne Kriterien nicht. Beides steht unten.

- src/eth_library_mcp/server.py:903 — `build_http_app(host, port)` ist die EINZIGE Stelle, die eine ASGI-App konstruiert; :926 `mcp.streamable_http_app(transport_security=security, host=host)`, :957 `_run_http` ruft `uvicorn.run(build_http_app(host, port), host=host, port=port)`, :973 `mcp.run()` (stdio). Grep nach `sse_app(|http_app(|def .*factory|--factory` ueber src/ findet keinen weiteren Pfad; Negativkontrolle: dasselbe Muster gegen /tmp/psse.py mit `mcp.sse_app()` trifft (1 Zeile), das Muster greift also.
- Dockerfile:35-36 — ENTRYPOINT ["python","-m","eth_library_mcp.server"] + CMD ["--http","--host","0.0.0.0","--port","8000"]; dieser Pfad laeuft durch denselben `__main__`-Block (server.py:962-972) und damit durch denselben Builder. railway.toml, render.yaml, Procfile und docker-compose*.yml existieren nicht (ls: No such file); `--factory`/`gunicorn` kommt nirgends vor.
- Gemessene Naht (uvicorn durch einen Stub ersetzt, `python -m eth_library_mcp.server --http --host 127.0.0.1 --port 8123`): uvicorn.run bekam host='127.0.0.1' port=8123 UND die App trug TransportSecuritySettings(allowed_hosts=['127.0.0.1:8123','[::1]:8123','localhost:8123']). Der Port reist also vollstaendig von argv bis in die Freigabeliste — Fail-Pattern 2 (Port intern gedefaultet) liegt nicht vor.
- Gemessene Routentabelle von build_http_app(): app.routes == [('/mcp', None)] — genau ein Netzweg. GET /sse -> 404, GET /messages -> 404, DELETE /sse -> 404: kein Legacy-SSE-Pfad neben Streamable HTTP. Negativkontrolle derselben Sonde: GET /mcp -> 400 und GET /mcp/ -> 307, die Sonde unterscheidet also 404 von bedienten Pfaden.
- Gemessen mit demselben Stub: `--host 0.0.0.0` ohne ETH_LIBRARY_ALLOWED_HOSTS -> transport_security None plus Log `dns_rebinding_protection_off`; mit ETH_LIBRARY_ALLOWED_HOSTS=mcp.example.ch -> allowed_hosts ['127.0.0.1:8000','[::1]:8000','localhost:8000','mcp.example.ch']. Die Scharfschaltung haengt an der Host-Freigabeliste selbst, nicht an einer sachfremden Bedingung (Auth/CORS/Debug).

### Expected Behavior

Die Pass-Kriterien stehen in `checks/ARCH-013.md` des Katalogs
(Skill mcp-audit 2.3.0). Sie werden hier bewusst nicht paraphrasiert: Eine
zweite, von Hand gepflegte Fassung derselben Kriterien driftet vom Katalog ab,
und dann prueft der Report eine Anforderung, die niemand mehr gestellt hat.

### Evidence

- src/eth_library_mcp/server.py:903 — `build_http_app(host, port)` ist die EINZIGE Stelle, die eine ASGI-App konstruiert; :926 `mcp.streamable_http_app(transport_security=security, host=host)`, :957 `_run_http` ruft `uvicorn.run(build_http_app(host, port), host=host, port=port)`, :973 `mcp.run()` (stdio). Grep nach `sse_app(|http_app(|def .*factory|--factory` ueber src/ findet keinen weiteren Pfad; Negativkontrolle: dasselbe Muster gegen /tmp/psse.py mit `mcp.sse_app()` trifft (1 Zeile), das Muster greift also.
- Dockerfile:35-36 — ENTRYPOINT ["python","-m","eth_library_mcp.server"] + CMD ["--http","--host","0.0.0.0","--port","8000"]; dieser Pfad laeuft durch denselben `__main__`-Block (server.py:962-972) und damit durch denselben Builder. railway.toml, render.yaml, Procfile und docker-compose*.yml existieren nicht (ls: No such file); `--factory`/`gunicorn` kommt nirgends vor.
- Gemessene Naht (uvicorn durch einen Stub ersetzt, `python -m eth_library_mcp.server --http --host 127.0.0.1 --port 8123`): uvicorn.run bekam host='127.0.0.1' port=8123 UND die App trug TransportSecuritySettings(allowed_hosts=['127.0.0.1:8123','[::1]:8123','localhost:8123']). Der Port reist also vollstaendig von argv bis in die Freigabeliste — Fail-Pattern 2 (Port intern gedefaultet) liegt nicht vor.
- Gemessene Routentabelle von build_http_app(): app.routes == [('/mcp', None)] — genau ein Netzweg. GET /sse -> 404, GET /messages -> 404, DELETE /sse -> 404: kein Legacy-SSE-Pfad neben Streamable HTTP. Negativkontrolle derselben Sonde: GET /mcp -> 400 und GET /mcp/ -> 307, die Sonde unterscheidet also 404 von bedienten Pfaden.
- Gemessen mit demselben Stub: `--host 0.0.0.0` ohne ETH_LIBRARY_ALLOWED_HOSTS -> transport_security None plus Log `dns_rebinding_protection_off`; mit ETH_LIBRARY_ALLOWED_HOSTS=mcp.example.ch -> allowed_hosts ['127.0.0.1:8000','[::1]:8000','localhost:8000','mcp.example.ch']. Die Scharfschaltung haengt an der Host-Freigabeliste selbst, nicht an einer sachfremden Bedingung (Auth/CORS/Debug).

### Gaps

- Kein Test prueft die Naht, nur den Builder: tests/test_cors.py:50, tests/test_transport_security.py:72/90/102, tests/test_server_identity.py:86/170 und tests/test_protocol_version.py:140 rufen alle `build_http_app(...)` direkt mit expliziten Argumenten auf. Die argv-Auswertung in server.py:962-972 und `_run_http` (server.py:953-957) sind von keinem Test beruehrt (grep nach `_run_http|sys.argv|__main__` ueber tests/ findet nur tests/test_classify_live_run.py:220, ein eigenes `__main__`). Das ist genau das im Check benannte Anti-Pattern «Test ruft den Builder direkt mit allen Parametern».
- Gegenprobe nach Pass-Kriterium 8 (Verdrahtung aus je einem Pfad entfernen, mindestens ein Test muss fallen) ist im Repo nicht gefuehrt und liesse sich mit der heutigen Testlage auch nicht fuehren: fiele `host=`/`transport_security=` in `_run_http` weg, bliebe die Suite gruen, weil kein Test durch diese Funktion laeuft.
- Der ausgelieferte Dockerfile-Default (`--host 0.0.0.0` ohne gesetzte ETH_LIBRARY_ALLOWED_HOSTS) schaltet die DNS-Rebinding-Pruefung ab — gemessen oben. Der Dockerfile setzt die Variable nicht und nennt sie nicht; der Hinweis existiert nur als Laufzeit-Warnung in server.py:911-918.

### Risk Description

Ergibt sich aus den Luecken oben und der Severity `high`. Wo eine Luecke
nur die Dokumentation betrifft, ist das Risiko ein anderes als bei einer
Verhaltensluecke — der Report unterscheidet das in der Findings-Tabelle, dieses
Dokument fuehrt beide Arten unvermischt auf, statt sie zu einer Erzaehlung zu
verbinden.

### Remediation

Die Behebung steht im Abschnitt «Remediation» von `checks/ARCH-013.md`. Was
an diesem Server konkret zu tun ist, folgt aus den Luecken oben.

### Effort Estimate

M (1-3d) — Schaetzung nach Severity, nicht gemessen.
