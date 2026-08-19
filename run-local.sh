#!/usr/bin/env bash
# Run the worker stack natively (no Docker):
#   - PHP-FPM  (executes bot.php)
#   - Caddy    (public :PORT + internal :9000 PHP proxy)
#   - uvicorn  (FastAPI worker API)
#
# One-time install of PHP 8.2 FPM + Caddy first (see instructions).
# Usage:  ./run-local.sh          # start
#         ./run-local.sh --stop   # stop
set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKER_BASE_DIR="${WORKER_BASE_DIR:-$REPO_DIR/.local_data}"
PORT="${PORT:-8080}"
export WORKER_BASE_DIR
export INTERNAL_SECRET="${INTERNAL_SECRET:-localdev}"

stop() {
  echo "Stopping local worker..."
  [ -f "$WORKER_BASE_DIR/uvicorn.pid" ] && kill "$(cat "$WORKER_BASE_DIR/uvicorn.pid")" 2>/dev/null || true
  [ -f "$WORKER_BASE_DIR/caddy.pid" ] && kill "$(cat "$WORKER_BASE_DIR/caddy.pid")" 2>/dev/null || true
  sudo service php8.2-fpm stop 2>/dev/null || true
  echo "Stopped."
  exit 0
}
[ "${1:-}" = "--stop" ] && stop

mkdir -p "$WORKER_BASE_DIR"

# Caddyfile expects the bootstrap prepend at /tmp/_bootstrap.php
if ! cp "$REPO_DIR/bootstrap.php" /tmp/_bootstrap.php 2>/dev/null; then
  sudo cp "$REPO_DIR/bootstrap.php" /tmp/_bootstrap.php
fi

# Apply the same PHP security config as production (open_basedir is set per
# request by Caddy; this adds display_errors + disable_functions).
if [ -d /etc/php/8.2/fpm ]; then
  sudo cp "$REPO_DIR/php.ini" /etc/php/8.2/fpm/conf.d/99-custom-security.ini 2>/dev/null || true
  sudo cp "$REPO_DIR/php-fpm.conf" /etc/php/8.2/fpm/pool.d/zz-custom.conf 2>/dev/null || true
  sudo service php8.2-fpm restart 2>/dev/null || true
else
  echo "WARN: PHP 8.2 FPM not found at /etc/php/8.2/fpm — install it first (see instructions)."
fi

# Caddy: public on $PORT, internal PHP proxy on :9000
sudo env WORKER_BASE_DIR="$WORKER_BASE_DIR" PORT="$PORT" caddy run \
  --config "$REPO_DIR/Caddyfile" --adapter caddyfile \
  > "$WORKER_BASE_DIR/caddy.log" 2>&1 &
echo $! > "$WORKER_BASE_DIR/caddy.pid"

# uvicorn (FastAPI) — must run from the worker dir (main.py is here)
cd "$REPO_DIR"
WORKER_BASE_DIR="$WORKER_BASE_DIR" INTERNAL_SECRET="$INTERNAL_SECRET" \
  python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 \
  > "$WORKER_BASE_DIR/uvicorn.log" 2>&1 &
echo $! > "$WORKER_BASE_DIR/uvicorn.pid"

echo "Local worker starting:"
echo "  Public : http://localhost:$PORT   (health: curl http://localhost:$PORT/health)"
echo "  Logs   : $WORKER_BASE_DIR/caddy.log, $WORKER_BASE_DIR/uvicorn.log"
echo "  Stop   : $0 --stop"
echo
echo "For Telegram to actually deliver updates, set CF_WEBHOOK_BASE (or"
echo "RAILWAY_PUBLIC_DOMAIN) to a PUBLIC https URL (Cloudflare/ngrok tunnel)"
echo "before deploying a bot, since localhost is not reachable by Telegram."
