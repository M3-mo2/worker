# Worker Hardening & Log Retrieval — Implementation Plan

## Context

We are improving the existing PHP worker (`/home/macro/Workspaces/worker/worker`) and its
companion Telegram bot (`/home/macro/Workspaces/php-hosting`). The goals, in the owner's words:

1. Make the worker **more secure**, with **clear isolation between users** and a **clear folder per user**.
2. Run **reliably on Railway without issues** (deployed bots must survive restarts).
3. Let a user **request their bot's logs from the Telegram bot**, returned by the worker.

This plan also serves as the security/isolation baseline for any future `php-platform` rewrite,
so doing it here either perfects the current worker or de-risks the new one.

## Current state — key findings (from exploration)

- **CRITICAL — `disable_functions` is shadowed.** `worker/php-fpm.conf` sets
  `php_admin_value[disable_functions]` to only 6 functions. In PHP-FPM a pool
  `php_admin_value` **overrides** (does not merge with) `php.ini`'s `disable_functions`, so the
  comprehensive list in `worker/php.ini` is silently discarded. As a result `getenv`, `putenv`,
  `ini_set`, `eval`, `pcntl_*`, `posix_*`, `symlink`, `link`, `assert`, `unserialize`,
  `set_time_limit`, `ignore_user_abort`, `scandir`/`opendir`/`readdir`/`DirectoryIterator`,
  `phpinfo`, etc. are currently **ENABLED**.
- **CRITICAL — Secrets leak to user PHP.** `clear_env = no` plus an enabled `getenv()` means any
  deployed bot can read `INTERNAL_SECRET`, `CF_WEBHOOK_BASE`, `MAIN_BOT_URL`,
  `RAILWAY_PUBLIC_DOMAIN`, etc. via `getenv()`. This is an active vulnerability.
- **CRITICAL — Bots vanish on Railway restart.** `WORKER_BASE_DIR` defaults to `/app`, which is the
  ephemeral image filesystem. No volume is mounted, so `user_bots/` and `data/bots.json` are lost on
  any restart/redeploy → the worker returns `ok` for now-unknown users → silent total outage.
- **HIGH — No per-user resource/process isolation.** A single `[www]` PHP-FPM pool (Debian default
  `pm=dynamic, pm.max_children=5`) serves all users. No per-user CPU/memory limits, no
  `request_terminate_timeout`. One runaway or infinite-loop bot starves every other user
  (noisy-neighbor DoS), and `set_time_limit(0)` is currently allowed.
- **MEDIUM — Weak defense-in-depth.** User dirs are `chmod 0o777` and `/tmp` is in every user's
  `open_basedir`, enabling cross-user temp-file discovery/writes.
- **Logs — nothing persisted.** The worker only DMs the owner on error via `_notify_owner`
  (`main.py`); there is no per-user log file. Webhook responses/FPM stderr go only to ephemeral
  container stdout.

## Phased plan

### Phase A — Urgent security hardening (do first, regardless of the rest)

- **A1. Restore `disable_functions`.** Remove the short override from `php-fpm.conf` (or move the
  full consolidated list into it) so `eval`, `ini_set`, `getenv`, `putenv`, `pcntl_*`, `posix_*`,
  `symlink`, `link`, `assert`, `unserialize`, `create_function`, `set_time_limit`,
  `ignore_user_abort`, `scandir`/`opendir`/`readdir`/`DirectoryIterator`, `phpinfo` are disabled.
  Keep `curl`, `file_get_contents`, `file_put_contents`, `fopen`, `error_log` as needed by legit bots.
- **A2. `clear_env = yes`** + `variables_order = "GPCS"` in the `[www]` pool.
- **A3. Tighten perms.** In `/deploy`, `chmod` the user dir `0o777 → 0o755` and `chown www-data:www-data`
  the dir + `bot.php` + `config.json`. PHP-FPM (the only writer) keeps access; cross-user writes
  now need *both* a perms bug and an `open_basedir` bug.
- **A4. Remove shared `/tmp` from `open_basedir`.** Host `_compat.php` read-only in `/opt/phpcompat`
  (`chmod 755`, not writable) and set `open_basedir = {root}:/opt/phpcompat`. Give each user its own
  `sys_temp_dir`/`session.save_path` (passed per request in `PHP_ADMIN_VALUE`). Eliminates the
  cross-user `/tmp` vector.
- **A5. Bind internal Caddy to `127.0.0.1:9000`** (currently `:9000`) — belt-and-suspenders with the
  existing `not client_ip 127.0.0.1` matcher.
- **A6. `display_errors = Off`, `log_errors = On`.** Reduces path/code disclosure to end users;
  error detection still works via response-body parsing for now.

### Phase B — Log retrieval feature

- **Worker:** per-user `user_bots/<id>/error.log`; `_append_user_log(user_id, kind, message)` with
  `MAX_LOG_BYTES` rotation (keep tail) and token-shape redaction (`\d+:[A-Za-z0-9_-]{30,}`); hook into
  the `/webhook` error/timeout/non-200 paths (same place `_notify_owner` is called); new
  `GET /logs/{user_id}` endpoint guarded by `verify_secret`, returning last `?lines=` lines (default
  500), redacted, capped ~50 KB. Ensure the file is created `0o666`/group-writable so `www-data` can
  append. Users' own PHP can append via `error_log(..., 3, "error.log")`.
- **Bot:** add `WorkerService.logs(user_id, lines=500)` to `core/worker.py` (mirrors `status()`); add a
  `📄 سجلّات` button → `manage:logs:<id>` in `bot_actions_keyboard` (`core/keyboards.py`); add a
  `cb_logs` handler in `features/manage/handlers.py` using `verify_bot_ownership` + `ws.logs`; send as a
  `.txt` document when >~3500 chars (Telegram's 4096/msg limit + raw log text breaks HTML parse), else
  as `<code>` text; add Arabic `LOGS_EMPTY` / `LOGS_CAPTION` to `features/manage/messages.py`.

### Phase C — Railway durability

- **C1. Volume.** Declare a Railway volume, mount at e.g. `/data`, set `WORKER_BASE_DIR=/data` via env so
  `user_bots/` and `data/` survive restarts. (Volumes are single-attach → consistent with the
  single-instance model; external storage is needed only if scaling past one instance.)
- **C2. Per-request resource caps** via the existing `PHP_ADMIN_VALUE`: `memory_limit`, `max_execution_time`.
- **C3. `request_terminate_timeout`** (e.g. 25s, below the worker's 30s `httpx` timeout) in the pool.
- **C4. Healthcheck readiness.** Make `/health` also verify the `:9000` socket / FPM is ready before
  marking healthy, to avoid early routing to a not-ready stack.

### Phase D — True per-user isolation (only if scale demands)

- **Per-user PHP-FPM pools:** separate socket `php8.2-fpm-<id>.sock` with own `pm.max_children`,
  `open_basedir`, `memory_limit`, created/removed on deploy/stop with an FPM reload; Caddy routes
  `user_id →` that socket. Heaviest effort; defer unless multi-tenant scale is imminent.

## Open questions to resolve in brainstorming (start with Phase A)

1. **Exact final `disable_functions` list** — which file functions (`chmod`/`copy`/`unlink`/`rename`)
   must stay enabled for legitimate bots? We need a concrete allow/deny split.
2. **Redaction scope** — token shape only, or also redact long numeric chat IDs / usernames?
3. **A5 / A6 scope** — ship localhost bind and `display_errors = Off` now, or keep the error body
   visible for detection until Phase B's log file is the primary signal?
4. **Phase D trigger** — is there a bounded user count assumption, or do we need real multi-tenant
   isolation from day one?

## Verification

- **A1:** in-container `php-fpm8.2 -i | grep disable_functions` shows the full list (not just 6).
- **A2:** a deployed bot calling `getenv('INTERNAL_SECRET')` returns empty/`false`.
- **Compile:** `python -m compileall worker` after edits.
- **B:** trigger a PHP error, request logs from the bot, confirm the file is written and delivered
  (text or document).
- **C1:** restart the Railway service, confirm deployed bots persist via the volume.

---

## Phase A — Detailed Specification (approved)

Approved via brainstorming. Decisions: minimal write-set for file functions; `display_errors=Off` (A6) deferred to after Phase B; Railway volume pulled into this build.

### A1 — `disable_functions` (authoritative in `php-fpm.conf`)
`php_admin_value[disable_functions]` in the `[www]` pool replaces the 6-function override with the full consolidated deny list:
```
exec,passthru,shell_exec,system,proc_open,popen,proc_close,proc_nice,proc_terminate,proc_get_status,pcntl_*,posix_*,getenv,putenv,ini_set,set_time_limit,ignore_user_abort,chmod,chown,rename,unlink,link,symlink,readlink,touch,assert,unserialize,phpinfo,scandir,opendir,readdir,closedir,rewinddir,glob,DirectoryIterator,RecursiveDirectoryIterator,FilesystemIterator,dl
```
Kept enabled: `curl_*`, `json_*`, `file_get_contents`, `file_put_contents`, `fopen`/`fwrite`, `error_log`, `copy`, `is_*`, `file_exists`, `realpath`, `basename`, `dirname`. `eval` is a construct and cannot be disabled via `disable_functions` (documented limitation). Remove the partial `disable_functions` line from `php.ini` so there is one source of truth.

### A2 — `php-fpm.conf`
`clear_env = yes`, `variables_order = "GPCS"` (stop `getenv()` from seeing worker secrets).

### A3 — `/deploy` perms (`main.py`)
`chmod(user_dir, 0o755)` (was 0o777); `os.chown(user_dir/bot_file/config_file, www-data, www-data)` wrapped in try/except (root-only; warn on failure, matching existing chmod pattern). Files stay `0o644`.

### A4 — `Caddyfile` internal server
Bind `127.0.0.1:9000`. `PHP_ADMIN_VALUE`:
```
open_basedir={http.vars.root}:/opt/phpcompat \n auto_prepend_file=/opt/phpcompat/_compat.php \n sys_temp_dir={http.vars.root} \n session.save_path={http.vars.root}
```
Drops shared `/tmp`; prepend hosted read-only in `/opt/phpcompat`; each bot gets its own temp + session dir inside its folder.

### A5 — `Dockerfile`
Copy `worker/compat.php` → `/opt/phpcompat/_compat.php` (`chmod 644`); remove old `/tmp/_compat.php` copy.

### Volume (pulled from Phase C)
Code already derives `BOTS_DIR`/`DATA_FILE` from `WORKER_BASE_DIR`. Manual Railway step: create a volume mounted at `/data`, set `WORKER_BASE_DIR=/data`. Confirm no hardcoded `/app` paths remain in `main.py`.

### Out of scope (stay in Phase C)
Per-request `memory_limit`/`max_execution_time`, `request_terminate_timeout`, `/health` readiness check.
