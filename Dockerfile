# SEC-007: Container-Sandbox für den HTTP-Transport.
#
# - Non-root user (UID 1000)
# - Slim base image, no build toolchain in final layer
# - Pip install with --no-cache-dir
# - Read-only filesystem support (run with --read-only --tmpfs /tmp)
# - Health-check via the streamable-http transport endpoint
#
# BASIS-IMAGE: python:3.13-slim, und die Zahl ist kein Zufall.
#
# Die CI-Matrix faehrt 3.11, 3.12 und 3.13; die Classifier in pyproject.toml
# nennen dieselben drei. Ein Container auf 3.14 liefe damit auf einer Version,
# die KEIN Gate prueft -- ein Bruch fiele erst im Betrieb auf, und das Grün der
# CI sagte bis dahin etwas ueber eine andere Laufzeit aus als die ausgelieferte.
#
# Genau das war zwischen dem 28.8. und dem 20.9.2026 der Fall: Dependabot hob
# das Image von 3.13 auf 3.14 (Commit 2719b9d), die Matrix blieb stehen, und
# niemand hat die Verbindung bemerkt -- es gab keinen Docker-Build in der CI,
# der sie haette herstellen koennen.
#
# Die Zeile allein haelt das nicht: `.github/dependabot.yml` fuehrt das
# `docker`-Oekosystem und machte denselben PR sonst im naechsten Monat wieder
# auf. Der Pin hat dort deshalb einen `ignore`-Eintrag, samt Begruendung, wann
# er faellt -- naemlich wenn die Matrix 3.14 mitfaehrt und nicht vorher.
#
# Was der `ignore` NICHT einfriert: Sicherheitsaktualisierungen des Images.
# `3.13-slim` ist ein bewegliches Tag; Docker Hub baut es neu, und ein `docker
# build` ohne Cache zieht die aktuelle Fassung. Festgenagelt ist die
# Python-Minor-Version, nicht der Stand des Basis-Systems.

FROM python:3.13-slim AS builder

WORKDIR /build
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/
RUN pip install --no-cache-dir --upgrade pip build && \
    python -m build --wheel --outdir /wheels

FROM python:3.13-slim

# Non-root user
RUN useradd --uid 1000 --create-home --shell /usr/sbin/nologin app

WORKDIR /app
COPY --from=builder /wheels/*.whl /tmp/wheels/
RUN pip install --no-cache-dir /tmp/wheels/*.whl && \
    rm -rf /tmp/wheels

USER 1000

# Streamable-HTTP transport; bind to all interfaces inside the container
# (the container itself is the sandbox; expose only via reverse proxy).
EXPOSE 8000
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["python", "-m", "eth_library_mcp.server"]
CMD ["--http", "--host", "0.0.0.0", "--port", "8000"]
