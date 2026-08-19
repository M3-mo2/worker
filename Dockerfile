FROM python:3.11-slim-bookworm

# Debian bookworm already ships PHP 8.2 in its main repo, so we DON'T need the
# external sury PHP repo (it was a slow/flaky external apt fetch during build).
# Only Caddy still requires an external repo (cloudsmith).
RUN apt-get update && apt-get install -y \
    apt-transport-https curl gnupg ca-certificates lsb-release debian-keyring debian-archive-keyring \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt-get update && apt-get install -y \
    php8.2-fpm php8.2-cli php8.2-curl php8.2-mbstring php8.2-xml php8.2-zip php8.2-gd php8.2-sqlite3 \
    caddy \
    && rm -rf /var/lib/apt/lists/*

# Install supervisord
RUN pip install --no-cache-dir supervisor

WORKDIR /app

# PHP security config
RUN mkdir -p /etc/php/8.2/fpm/conf.d /etc/php/8.2/fpm/pool.d
COPY worker/php.ini /etc/php/8.2/fpm/conf.d/99-custom-security.ini
COPY worker/php-fpm.conf /etc/php/8.2/fpm/pool.d/zz-custom.conf

# Compatibility prepend: pins CWD to the bot's folder AND injects
# framework-expected globals/constants (ID, TOKEN, $update, ...).
# Hosted read-only in /opt/phpcompat (NOT /tmp) so it is outside every bot's
# open_basedir and not writable by user PHP. The COPY creates /opt/phpcompat.
COPY worker/compat.php /opt/phpcompat/_compat.php
RUN chmod 644 /opt/phpcompat/_compat.php

# Caddy config
COPY worker/Caddyfile /app/Caddyfile

# Supervisord config
COPY worker/supervisord.conf /app/supervisord.conf

# Python deps
COPY worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY worker/main.py /app/main.py

# Create required directories
RUN mkdir -p /app/data /app/user_bots /app/logs

CMD ["supervisord", "-c", "/app/supervisord.conf"]
