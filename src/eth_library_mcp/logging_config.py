"""
OBS-003: Structured JSON logging on stderr.

stdio-Transport (default) reserves stdout for the JSON-RPC protocol, so all
logs go to stderr. Structured JSON output makes the logs ingestible by
log shippers (Datadog, CloudWatch, Loki) without per-source parsers.

Severity levels actually used by this server:
- debug:   per-request URL + param dump (off by default)
- info:    server lifecycle (lifespan startup/shutdown)
- warning: degraded but recoverable upstream behaviour
- error:   unhandled exception classes inside _handle_error

## Warum hier redigiert wird (OBS-002, Audit 2026-09-19)

Der eigene Log dieses Servers war nie das Problem: `client.py` schreibt
`has_key=True` statt des Werts. Das Leck lag eine Ebene tiefer. `basicConfig`
unten stellt den Root-Logger auf INFO, und damit wird httpx' eigener Logger
scharf, der bei jeder Anfrage die **vollstaendige** URL protokolliert --
einschliesslich `?apikey=...`, weil `client.py` den Schluessel als
Query-Parameter anhaengt. Gemessen am 19.9.2026:

    HTTP Request: GET https://api.library.ethz.ch/discovery/v1/resources
    ?q=test&apikey=sk-GEHEIM-TESTSCHLUESSEL-999 "HTTP/1.1 200 OK"

`SECURITY.md` und `docs/secret-management.md` sagten zu diesem Zeitpunkt beide
woertlich, der Schluessel werde nie geloggt. Er wurde bei jeder einzelnen
Anfrage geloggt.

**Warum nicht einfach httpx stummschalten.** Das waere der kleinere Eingriff
und wuerde genau den einen gemessenen Pfad schliessen -- bis der naechste
Aufrufer eine URL loggt. Die Ursache ist nicht httpx, sondern dass ein
Geheimnis in der URL steht und irgendwer sie ausgibt. Redigiert wird deshalb
am Ausgang, nicht an der einen bekannten Quelle.

**Warum zwei Stellen.** Die beiden Logwege dieses Servers teilen sich keinen
Ausgang: structlog schreibt ueber `PrintLoggerFactory` direkt nach stderr und
kommt an den stdlib-Handlern gar nicht vorbei. Eine Absicherung im
stdlib-Zweig allein deckte also httpx ab und die eigenen Zeilen nicht; ein
structlog-Prozessor allein umgekehrt. Beide benutzen dieselbe Funktion, damit
sie nicht auseinanderlaufen koennen.

**Was hier nicht behoben wird.** Der Schluessel steht weiterhin in der URL.
Ihn in einen Header zu verschieben waere die Behebung an der Wurzel, aendert
aber die Authentisierung gegenueber der Quelle -- und ob die ETH-API einen
Header akzeptiert, ist ohne Schluessel und ohne Netzzugang nicht pruefbar.
Eine Vermutung darueber gehoert nicht in den Auslieferungspfad. Die Redaktion
hier ist deshalb die Absicherung, nicht der Ersatz dafuer.
"""

from __future__ import annotations

import logging
import os
import re
import sys
import traceback
from typing import Any

import structlog

# Deckt die gaengigen Schreibweisen ab, mit denen ein Geheimnis in einer
# Query-Zeichenkette steht. Der Wert laeuft bis zum naechsten Trennzeichen;
# `[^&\s"'#]` statt `.` sorgt dafuer, dass nicht der ganze Rest der Zeile
# mitverschwindet und der Log unlesbar wird.
_GEHEIMNIS_PARAMETER = re.compile(
    r"(?i)\b(apikey|api_key|api-key|access_token|token|key)=([^&\s\"'#]+)"
)

PLATZHALTER = "<redigiert>"


def redigiere_geheimnisse(text: str) -> str:
    """Entfernt API-Schluessel aus einer Logzeile.

    Zwei Wege, und beide werden gebraucht:

    1. Der **Wert** aus der Umgebung wird woertlich ersetzt. Das greift auch
       dort, wo der Parameter anders heisst, als dieses Modul erwartet -- der
       Fall, den eine reine Musterliste nie vollstaendig abdeckt.
    2. Das **Muster** `schluessel=wert` greift zusaetzlich dort, wo der Wert
       nicht identisch aus der Umgebung stammt: URL-kodiert, aus einer
       Konfiguration eines anderen Dienstes, oder in einem Test.

    Wer nur den ersten Weg baut, verliert jede Kodierung; wer nur den zweiten
    baut, verliert jeden unbekannten Parameternamen.
    """
    if not text:
        return text

    schluessel = os.environ.get("ETH_LIBRARY_API_KEY")
    # Die Laengenpruefung ist kein Schoenheitsfehler: Bei einem leeren oder
    # einzeichigen Wert wuerde `str.replace` die halbe Zeile zerlegen.
    if schluessel and len(schluessel) > 3 and schluessel in text:
        text = text.replace(schluessel, PLATZHALTER)

    return _GEHEIMNIS_PARAMETER.sub(rf"\1={PLATZHALTER}", text)


def _redigiere_wert(wert: Any) -> Any:
    """Redigiert ein einzelnes Log-Argument, ohne seinen Typ unnoetig zu aendern.

    httpx uebergibt seine URL als `httpx.URL`-Objekt, nicht als Zeichenkette --
    wer nur `isinstance(wert, str)` prueft, laesst genau den gemessenen Fall
    durch. Deshalb wird jeder Wert ueber seine Textform geprueft und nur dann
    ersetzt, wenn dabei wirklich etwas redigiert wurde.
    """
    if isinstance(wert, str):
        return redigiere_geheimnisse(wert)

    text = str(wert)
    redigiert = redigiere_geheimnisse(text)
    return redigiert if redigiert != text else wert


# Felder, die `redigiere_datensatz` nicht ueber ihre Textform anfassen darf.
# `exc_info` ist ein Tripel `(Typ, Wert, Traceback)`; durch `str()` gedreht und
# als Zeichenkette zurueckgeschrieben waere es kaputt, und der Formatter kaeme
# nicht mehr an den Traceback. Es wird stattdessen ueber `exc_text` behandelt.
# `msg` und `args` haben ihre eigene, typbewusste Behandlung weiter oben.
_EIGENE_BEHANDLUNG = frozenset({"msg", "args", "exc_info", "exc_text"})


def redigiere_datensatz(record: logging.LogRecord) -> logging.LogRecord:
    """Redigiert einen stdlib-Datensatz vollstaendig, an Ort und Stelle.

    ## Die drei Wege, auf denen ein Geheimnis in eine Logzeile kommt

    **1. Nachricht und Argumente.** Der gemessene httpx-Fall: die URL steht als
    `httpx.URL`-Objekt in `record.args`.

    **2. Die Ausnahme.** `logging.Formatter.format()` haengt den Traceback
    **nach** der Formatierung der Nachricht an, aus `record.exc_info`. Eine
    Fassung, die nur `msg` und `args` anfasst, laesst ihn unberuehrt -- und
    httpx-Ausnahmen fuehren die vollstaendige URL in ihrem Text. Gemessen am
    20.9.2026:

        ValueError: request failed for url ...&apikey=sk-LECK-TEST-12345

    Behoben wird das nicht durch Aendern der Ausnahme -- die gehoert dem
    Aufrufer und wird anderswo weiterverwendet --, sondern ueber `exc_text`:
    Der Formatter benutzt dieses Feld, wenn es gesetzt ist, und ruft
    `formatException` dann gar nicht erst auf. Wir formatieren also selbst,
    redigieren das Ergebnis und legen es dort ab.

    **3. `extra`.** `Logger.makeRecord` mischt die `extra`-Felder erst **nach**
    der Datensatz-Fabrik in `record.__dict__`. Ein strukturierter Handler, der
    das Dictionary serialisiert, gibt sie unredigiert aus. Gemessen am selben
    Tag: `extra_url=https://...&apikey=sk-LECK-TEST-12345`.

    Die Wege 2 und 3 hat ein Codex-Review auf PR #63 gefunden, nachdem Weg 1
    behoben war. Beide sind danach nachgemessen worden, nicht uebernommen.
    """
    if isinstance(record.msg, str):
        record.msg = redigiere_geheimnisse(record.msg)

    if record.args:
        if isinstance(record.args, dict):
            record.args = {k: _redigiere_wert(v) for k, v in record.args.items()}
        else:
            record.args = tuple(_redigiere_wert(v) for v in record.args)

    if record.exc_info and not record.exc_text:
        roh = "".join(traceback.format_exception(*record.exc_info))
        record.exc_text = redigiere_geheimnisse(roh.rstrip("\n"))
    elif record.exc_text:
        record.exc_text = redigiere_geheimnisse(record.exc_text)

    # Alles Uebrige aus `record.__dict__` -- das sind genau die `extra`-Felder
    # plus die Standardfelder, bei denen die Redaktion folgenlos durchlaeuft.
    for schluessel, wert in record.__dict__.items():
        if schluessel not in _EIGENE_BEHANDLUNG:
            record.__dict__[schluessel] = _redigiere_wert(wert)

    return record


def _installiere_makerecord_haken() -> None:
    """Redigiert nach dem Einmischen von `extra`.

    Die Datensatz-Fabrik allein genuegt dafuer nicht, und das ist keine
    Nachlaessigkeit der Fabrik, sondern die Reihenfolge in CPython:

        rv = _logRecordFactory(...)      # hier laeuft unsere Fabrik
        if extra is not None:
            for key in extra:
                rv.__dict__[key] = extra[key]   # erst hier kommt extra dazu
        return rv

    `Logger.makeRecord` ist die einzige Stelle, an der der Datensatz
    **vollstaendig** ist und trotzdem noch keinen Handler gesehen hat. Ein
    Filter am Handler waere wieder von der Handler-Reihenfolge abhaengig --
    genau das Problem, das die Fabrik geloest hat.
    """
    vorhanden = logging.Logger.makeRecord
    if getattr(vorhanden, "_redigiert", False):
        return

    def makeRecord(self: logging.Logger, *args: Any, **kwargs: Any) -> logging.LogRecord:
        return redigiere_datensatz(vorhanden(self, *args, **kwargs))

    makeRecord._redigiert = True  # type: ignore[attr-defined]
    logging.Logger.makeRecord = makeRecord  # type: ignore[method-assign]


def _installiere_datensatz_fabrik() -> None:
    """Haengt die Redaktion in die Erzeugung jedes Logdatensatzes ein.

    ## Warum hier und nicht als Filter am Handler

    Die erste Fassung war ein `logging.Filter` am Root-Handler. Sie hat
    funktioniert, und ein Test hat trotzdem etwas Wichtigeres gezeigt: Ein
    Filter am *Handler* laeuft erst, wenn dieser Handler an der Reihe ist.
    Haengt ein zweiter Handler am selben Logger -- pytest tut das, ein
    Log-Shipper tut das, ein Debug-Handler tut das --, dann entscheidet die
    **Reihenfolge**, ob er den Datensatz vor oder nach der Redaktion sieht.
    Ein Geheimnisschutz, der von der Handler-Reihenfolge abhaengt, ist kein
    Schutz, sondern ein Zufall, der meistens gutgeht.

    Ein Filter am *Logger* loest das nicht: Filter am Root-Logger greifen nur
    bei Datensaetzen, die direkt auf Root geloggt werden, nicht bei
    weitergereichten. Der httpx-Logger reicht weiter.

    Die Fabrik laeuft in `Logger.makeRecord`, also bevor irgendein Filter und
    irgendein Handler den Datensatz zu sehen bekommt. Damit gibt es genau
    einen Zeitpunkt, an dem redigiert wird, und keinen Weg daran vorbei.
    """
    vorhandene = logging.getLogRecordFactory()
    if getattr(vorhandene, "_redigiert", False):
        return

    def fabrik(*args: Any, **kwargs: Any) -> logging.LogRecord:
        return redigiere_datensatz(vorhandene(*args, **kwargs))

    fabrik._redigiert = True  # type: ignore[attr-defined]
    logging.setLogRecordFactory(fabrik)


def _redaktions_prozessor(_logger: Any, _name: str, ereignis: dict) -> dict:
    """structlog-Prozessor mit derselben Aufgabe fuer die eigenen Logzeilen.

    Laeuft vor dem JSONRenderer, sieht also noch das Ereignis-Dictionary und
    nicht die fertige Zeile.
    """
    for schluessel, wert in ereignis.items():
        ereignis[schluessel] = _redigiere_wert(wert)
    return ereignis


def configure_logging(level: str = "INFO") -> None:
    """Idempotently configure stderr-bound structlog with JSON output."""
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=getattr(logging, level.upper(), logging.INFO),
    )

    _installiere_datensatz_fabrik()
    _installiere_makerecord_haken()

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            _redaktions_prozessor,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = "eth_library_mcp") -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
