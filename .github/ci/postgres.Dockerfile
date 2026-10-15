# Test-only runtime. No application database or credentials are copied in.
FROM postgres:17.11-bookworm@sha256:91eb910c44c7ed13f7f1a4ccadaa9ca72ef14cddc04cacb6e070e48eb44731a3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       postgresql-plpython3-17=17.11-1.pgdg12+2 python3-pip \
    && test "$(postgres --version)" = 'postgres (PostgreSQL) 17.11 (Debian 17.11-1.pgdg12+2)' \
    && python3 -m pip install --no-cache-dir --only-binary=:all: --no-deps \
       --target /usr/local/lib/python3.11/dist-packages \
       emoji==2.16.0 regex==2026.9.29 \
    && rm -rf /var/lib/apt/lists/*
