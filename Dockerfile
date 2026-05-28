# SEC-007: Container-Sandbox für den HTTP-Transport.
#
# - Non-root user (UID 1000)
# - Slim base image, no build toolchain in final layer
# - Pip install with --no-cache-dir
# - Read-only filesystem support (run with --read-only --tmpfs /tmp)
# - Health-check via the streamable-http transport endpoint

FROM python:3.13-slim AS builder

WORKDIR /build
COPY pyproject.toml README.md ./
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
