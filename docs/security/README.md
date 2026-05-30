# Security Mechanisms Documentation

## Overview

This document provides a comprehensive reference for **all security and protection mechanisms** found in the reference Telegram Bot Hosting platform (`/reference/`). The goal is to extract these mechanisms into a standalone, reusable security service.

---

## Table of Contents

1. [Network Layer](#1-network-layer)
2. [User Authentication & Authorization](#2-user-authentication--authorization)
3. [Input Validation & Sanitization](#3-input-validation--sanitization)
4. [PHP Sandboxing & Function Restrictions](#4-php-sandboxing--function-restrictions)
5. [File Security](#5-file-security)
6. [Encryption & Cryptography](#6-encryption--cryptography)
7. [Rate Limiting](#7-rate-limiting)
8. [Content Moderation](#8-content-moderation)
9. [User & Process Isolation](#9-user--process-isolation)
10. [Logging & Monitoring](#10-logging--monitoring)
11. [Session & State Management](#11-session--state-management)
12. [Bot Detection & Analysis](#12-bot-detection--analysis)
13. [Quota System](#13-quota-system)

---

## 1. Network Layer

### 1.1 Caddy Path Traversal Block

- **File:** `reference/Caddyfile.railway` (lines 3-6)
- **Also in:** `reference/docker/Caddyfile.txt` (lines 3-6)
- **Type:** Web server level protection

Blocks any URL containing `..` at the reverse proxy level before it reaches any application code.

```caddyfile
@path_traversal path_regexp \.\.
handle @path_traversal {
    respond "Path Traversal Attempt Denied" 403
}
```

### 1.2 Webhook Payload Size Limit

- **File:** `reference/web/webhook.py` (lines 30-31, 245-246)
- **Type:** Request size enforcement

```python
MAX_PAYLOAD_BYTES = 1024 * 1024  # 1 MB
```

Rejects payloads exceeding 1 MB with HTTP 413.

### 1.3 Request Timeout

- **File:** `reference/web/internal_api_server.py` (lines 29, 169-171)
- **Type:** Timeout enforcement

```python
REQUEST_TIMEOUT = 10  # seconds
```

Applied to every request via `before_request` hook.

### 1.4 Caddy URL-Based Routing (Attack Surface Reduction)

- **File:** `reference/Caddyfile.railway` (lines 1-50)
- **Type:** Routing / isolation

```
/webhook*   → webhook server (port 4000)
/webapp*    → webapp server (port 4005)
/api*       → internal API (port 4003)
/{user_id}  → PHP-FPM (with per-user open_basedir)
everything  → 404
```

Only specific URL patterns reach specific services. Everything else gets a 404.

---

## 2. User Authentication & Authorization

### 2.1 User Status Hierarchy

- **File:** `reference/bot/services/user_service.py` (lines 12-29)
- **Type:** Role-based access control

Priority order (highest to lowest):

1. `sudo` — hardcoded `SUDO_USERS` in config
2. `admin` — loaded from `admins.json`
3. `banned` — loaded from `banned_users.json`
4. `user` — default role

```python
def check_user_status(user_id: int) -> str:
    if user_id in settings.telegram.SUDO_USERS:
        return 'sudo'
    admins = load_admin_list()
    if str(user_id) in admins:
        return 'admin'
    banned = load_banned_list()
    if str(user_id) in banned:
        return 'banned'
    return 'user'
```

### 2.2 Banned User Checks (Pervasive)

- **Files:** Nearly every handler (`files.py`, `bots.py`, `billing.py`, `profile.py`, `main_menu.py`, etc.)
- **Type:** Access gate

Almost every handler begins with:

```python
if check_user_status(sender_id) == 'banned':
    return await event.answer("🚫 أنت محظور.", alert=True)
```

### 2.3 Developer API Key Authentication

- **File:** `reference/bot/core/database.py` (lines 315-371)
- **Type:** API authentication

- Keys generated with `secrets.token_urlsafe(32)` prefixed with `prod_`
- `get_user_by_dev_api_key()` validates prefix and queries database
- Checks `is_enabled` flag before authorizing
- Logs every API request with timestamp and increments counter

```python
api_key = f"prod_{secrets.token_urlsafe(32)}"
```

### 2.4 Webhook Secret Token Verification

- **File:** `reference/bot/handlers/bots.py` (line 155)
- **File:** `reference/web/webhook.py` (lines 221-242)
- **Type:** Webhook authentication

- Secret generated with `os.urandom(24).hex()` (48-char hex string)
- Verified using **constant-time comparison** (`hmac.compare_digest`) to prevent timing attacks

```python
# Generation
secret = os.urandom(24).hex()

# Verification
if not hmac.compare_digest(incoming_secret, stored_secret):
    return web.Response(status=403)
```

### 2.5 WebApp Authentication (HMAC-signed URLs)

- **File:** `reference/bot/handlers/web_app.py` (lines 19-57)
- **Type:** URL authentication

Uses Telegram's `WebAppData` protocol with HMAC-SHA256:

```python
secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
hash_value = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
```

### 2.6 Force Subscribe (Channel Subscription Gate)

- **File:** `reference/bot/utils/decorators.py` (lines 21-106)
- **Type:** Access gate decorator

`@force_subscribe_required` decorator checks if user is subscribed to all configured channels. `SUDO_USERS` are exempt. Uses `GetParticipantRequest` to verify membership.

### 2.7 Maintenance Mode Bypass

- **File:** `reference/bot/utils/decorators.py` (lines 109-137)
- **Type:** Access gate decorator

`@maintenance_check` decorator blocks normal users when `bot_status = False`. SUDO_USERS and admins bypass this.

### 2.8 Ownership Verification

- **File:** `reference/bot/handlers/files.py` (lines 777-778, 834-838)
- **Type:** Authorization

Before allowing file deletion, verifies the cached `owner_id` matches `sender_id`:

```python
if cache_entry.get('owner_id') != sender_id:
    return await event.answer("🚫 هذا الطلب لا يخصك.", alert=True)
```

### 2.9 Internal API Secret

- **File:** `reference/bot/core/config.py` (line 78)
- **Type:** Service-to-service authentication

```python
INTERNAL_SECRET = 'change_this_internal_secret'
```

Passed as `X-Internal-Secret` header for internal service communication.

---

## 3. Input Validation & Sanitization

### 3.1 File/Folder Name Validation

- **File:** `reference/bot/handlers/files.py` (lines 151-192)
- **Type:** Input validation

`validate_name()` enforces:

- No empty names
- No hidden files (starting with `.`)
- Only `[a-zA-Z0-9_\-\.]` allowed
- No `..` (path traversal)
- No Windows reserved names (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
- Max 255 characters

### 3.2 Path Traversal Protection (User Directory Navigation)

- **File:** `reference/bot/services/file_service.py` (lines 27-42)
- **Type:** Path confinement

```python
def set_current_path(user_id: int, new_path: str):
    root = get_user_root(user_id)
    if os.path.commonpath([root, new_path]) == root and os.path.isdir(new_path):
        user_current_working_directory[user_id] = new_path
```

Ensures resolved path is within the user's root directory.

### 3.3 Path Traversal Protection (Internal API)

- **File:** `reference/web/internal_api_server.py` (lines 83-99)
- **Type:** Path sanitization

Checks for `..` in path segments and verifies absolute path is within user directory using `os.path.commonprefix()`.

### 3.4 HTML Escaping (Telegram Messages)

- **File:** `reference/bot/handlers/files.py` (lines 320, 345-346, 545, 547, 629, 631, 1294, 1310, 1335, 1468)
- **Type:** XSS prevention

User-generated content (file names, paths, directory trees) is escaped with `html.escape()` before inclusion in Telegram HTML messages.

### 3.5 PHP Error Sanitization

- **File:** `reference/bot/utils/text.py` (lines 36-53)
- **Type:** Information leakage prevention

Strips server-internal paths from PHP error output before displaying to users:

```python
sanitized_text = re.sub(r'/app/user_bots/\d+/', './', text_output)
```

### 3.6 JSON Validation on Webhook Input

- **File:** `reference/web/webhook.py` (lines 257-261)
- **Type:** Input validation

Validates incoming webhook payload is valid JSON before processing.

### 3.7 Webhook Path Validation

- **File:** `reference/web/webhook.py` (lines 264-266)
- **Type:** Path traversal prevention

```python
if '..' in rel_path or '//' in rel_path or rel_path.startswith('/'):
    return web.json_response({"ok": True})
```

### 3.8 Telegram Token Format Validation

- **File:** `reference/web/internal_api_server.py` (line 22)
- **Type:** Input format validation

```python
TELEGRAM_TOKEN_REGEX = re.compile(r'^\d{8,10}:[a-zA-Z0-9_-]{35}$')
```

---

## 4. PHP Sandboxing & Function Restrictions

### 4.1 Massive disable_functions List (70+ Functions)

- **File:** `reference/docker/custom.ini` (line 6)
- **Type:** Function restriction

```
disable_functions = stream_wrapper_restore,stream_wrapper_register,unserialize,ini_set,glob,
proc_terminate,fsockopen,stream_socket_client,ini_get,get_cfg_var,create_function,getenv,
get_defined_vars,get_defined_functions,get_loaded_extensions,get_current_user,ini_get_all,
escapeshellarg,assert,eval,exec,passthru,shell_exec,system,proc_open,popen,parse_ini_file,
show_source,pcntl_exec,pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,
pcntl_wifstopped,pcntl_wifsignaled,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,
pcntl_signal,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,
pcntl_sigwaitinfo,putenv,apache_setenv,dl,posix_kill,posix_mkfifo,posix_setpgid,posix_setsid,
posix_setuid,ini_alter,ini_restore,openlog,syslog,highlight_file,phpinfo,readlink,symlink,link
```

**Categories blocked:**
- Command execution: `exec`, `passthru`, `shell_exec`, `system`, `proc_open`, `popen`, `pcntl_exec`, `eval`, `assert`
- Network: `fsockopen`, `stream_socket_client`
- Process control: all `pcntl_*` functions
- Environment: `putenv`, `apache_setenv`, `getenv`
- Filesystem: `symlink`, `link`, `readlink`
- Information disclosure: `phpinfo`, `highlight_file`, `get_defined_vars`, `get_defined_functions`, `get_loaded_extensions`
- Configuration: `ini_set`, `ini_alter`, `ini_restore`, `ini_get`, `ini_get_all`, `get_cfg_var`
- Serialization: `unserialize`
- System: `dl`, `posix_kill`, `posix_setuid`, `posix_setsid`

### 4.2 PHP-FPM Pool-Level Restrictions

- **File:** `reference/docker/php-fpm-custom.conf` (line 4)
- **Type:** Double-layer function restriction

```
php_admin_value[disable_functions] = exec,passthru,shell_exec,system,proc_open,popen
```

Additional `disable_functions` at the FPM pool level as a second layer.

### 4.3 Dynamic open_basedir (Per-User Jail)

- **File:** `reference/Caddyfile.railway` (lines 41-43)
- **Also in:** `reference/docker/Caddyfile.txt` (lines 21-23)
- **Type:** Directory restriction

```
php_fastcgi unix//run/php/php8.2-fpm.sock {
    env PHP_ADMIN_VALUE "open_basedir={http.vars.root}:/tmp/ \n auto_prepend_file={http.vars.root}/host_bootstrap.php"
}
```

Each user's PHP execution is restricted to their own directory + `/tmp/`.

### 4.4 allow_url_include Disabled

- **File:** `reference/docker/custom.ini` (line 14)
- **Type:** Remote code inclusion prevention

```ini
allow_url_include = Off
```

### 4.5 .user.ini Disabled

- **File:** `reference/docker/custom.ini` (line 13)
- **Type:** Configuration override prevention

```ini
user_ini.filename =
```

Prevents users from overriding PHP settings via `.user.ini` files.

### 4.6 Host Bootstrap Auto-Provisioning

- **File:** `reference/config/host_bootstrap.php` (lines 1-55)
- **File:** `reference/bot/handlers/main_menu.py` (lines 143-174)
- **Type:** Controlled environment injection

The `host_bootstrap.php` file is auto-prepended to every PHP execution via Caddy's `auto_prepend_file`. Provides helper functions with the user's API key. If deleted, auto-restored on next `/start`.

---

## 5. File Security

### 5.1 Dangerous Function Detection (Marketplace)

- **File:** `reference/bot/services/marketplace_service.py` (lines 37-41, 86-95)
- **Type:** Static analysis

PHP files uploaded to marketplace are scanned for:

```python
DANGEROUS_FUNCTIONS = [
    'eval', 'exec', 'system', 'shell_exec', 'passthru',
    'proc_open', 'popen', 'pcntl_exec', 'assert'
]
```

If any found, upload is rejected.

### 5.2 Marketplace File Extension Whitelist

- **File:** `reference/bot/services/marketplace_service.py` (lines 24-35)
- **Type:** Extension filtering

```python
ALLOWED_EXTENSIONS = [
    '.php', '.py', '.js', '.html', '.css', '.sql',
    '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.env',
    '.txt', '.md', '.rst',
    '.example', '.sample', '.template', '.dist',
    '.zip'
]
```

### 5.3 File Size Limits

- **File:** `reference/bot/services/marketplace_service.py` (lines 22-23)
- **Type:** Resource limit

- `MAX_FILE_SIZE = 10 MB` per file
- `MAX_TOTAL_SIZE = 50 MB` total per marketplace product

### 5.4 Extension Enforcement on Rename

- **File:** `reference/bot/handlers/files.py` (lines 925-938)
- **Type:** Extension control

Users cannot change file extensions except to `.bak` or `.txt`. Prevents renaming to bypass execution restrictions.

### 5.5 WebApp Symlink Protection

- **File:** `reference/web/webapp_server.py` (lines 159-161)
- **Type:** Symlink attack prevention

```python
if os.path.islink(file_path):
    return abort(403, "محاولة وصول غير مسموح بها (Symlinks).")
```

### 5.6 System File Protection

- **File:** `reference/bot/handlers/files.py` (lines 746-749)
- **Type:** Critical file protection

`host_bootstrap.php` cannot be deleted by users:

```python
if file_name == 'host_bootstrap.php' and current_path == user_root:
    return await event.answer("🚫 لا يمكن حذف ملف النظام هذا", alert=True)
```

---

## 6. Encryption & Cryptography

### 6.1 Fernet Encryption (File Paths)

- **File:** `reference/encryption.key` (line 1)
- **File:** `reference/bot/handlers/files.py` (lines 966-971, 1088-1093)
- **Type:** Path encryption

File paths are encrypted with Fernet before being included in editor URLs:

```python
from cryptography.fernet import Fernet
cipher_suite = Fernet(ENCRYPTION_KEY)
encrypted_path = cipher_suite.encrypt(relative_path.encode('utf-8')).decode('utf-8')
editor_url = f"{settings.web.EDITOR_BASE_URL}/webapp/edit/{quote(encrypted_path)}"
```

### 6.2 Encrypted Path Decryption & Validation

- **File:** `reference/web/webapp_server.py` (lines 132-153)
- **Type:** Path decryption + validation

```python
decrypted_path = cipher_suite.decrypt(encrypted_path.encode('utf-8')).decode('utf-8')
file_path = os.path.abspath(os.path.join(BOTS_DIR, decrypted_path))
if not file_path.startswith(BOTS_DIR):
    return abort(403)
```

### 6.3 Secure API Key Generation

- **File:** `reference/bot/core/database.py` (lines 315-317)
- **Type:** Cryptographic key generation

```python
api_key = f"prod_{secrets.token_urlsafe(32)}"
```

### 6.4 Webhook Secret Generation

- **File:** `reference/bot/handlers/bots.py` (line 155)
- **Type:** Secret generation

```python
secret = os.urandom(24).hex()  # 48-char hex string
```

### 6.5 Constant-Time Secret Comparison

- **File:** `reference/web/webhook.py` (lines 117-121)
- **Type:** Timing attack prevention

```python
if not hmac.compare_digest(incoming_secret, stored_secret):
    return web.Response(status=403)
```

---

## 7. Rate Limiting

### 7.1 Internal API Rate Limiting (Per-User + Per-IP)

- **File:** `reference/web/internal_api_server.py` (lines 24-81, 176-206)
- **Type:** Two-tier rate limiting

```python
RATE_LIMIT_SECONDS = 60
RATE_LIMIT_REQUESTS = 20        # per user
IP_RATE_LIMIT_REQUESTS = 50     # per IP
```

- Uses in-memory dictionaries (`rate_limit_tracker`, `ip_rate_limit_tracker`)
- Old timestamps pruned on each check
- Returns HTTP 429 when exceeded

### 7.2 Marketplace View Cooldown (Anti-View-Botting)

- **File:** `reference/bot/core/database.py` (lines 713-749)
- **Type:** View rate limiting

`marketplace_views` table tracks `last_viewed_at` per (product_id, user_id). 10-hour cooldown between views.

### 7.3 Subscription Channel Anti-Flood

- **File:** `reference/bot/utils/decorators.py` (line 50)
- **Type:** API flood prevention

0.1-second delay between channel subscription checks.

### 7.4 AI Task Queue Cooldown

- **File:** `reference/bot/tasks/ai_queue.py` (lines 29, 53)
- **Type:** External API rate limiting

Background worker processes AI tasks sequentially with delays to avoid API rate limits from Gemini/Groq.

---

## 8. Content Moderation

### 8.1 Profanity Filter (Multi-Language)

- **File:** `reference/bot/services/profanity_filter.py` (lines 1-335)
- **Type:** Content filtering

**Features:**
- Three severity levels: Critical (permanent ban), High (3-day ban), Low (warning)
- Multi-language dictionaries: Arabic and English profanity words
- Obfuscation detection: catches `f*ck`, `f.u.c.k`, `f_u_c_k` patterns
- Whitelist: safe words that might trigger false positives (e.g., "class", "click")
- Applied to marketplace product titles and descriptions

### 8.2 Marketplace Ban System (3-Tier)

- **File:** `reference/bot/services/profanity_filter.py` (lines 145-308)
- **Type:** Progressive punishment

| Tier | Duration | Trigger | Consequences |
|------|----------|---------|--------------|
| Permanent | 100 years | Critical profanity | Deletes all products, comments, reviews |
| Temporary | 3 days | High severity | Blocks comments and uploads |
| Warning | 4 days | 3 low-severity offenses | Blocks comments only |

Ban types stored in `marketplace_bans` table with `ban_type` field.

### 8.3 Marketplace Report System

- **File:** `reference/bot/core/database.py` (lines 286-301)
- **Type:** User reporting

`marketplace_reports` table allows users to report products/comments. Reports have `status` (pending/reviewed), `reviewed_by`, and `admin_notes`.

---

## 9. User & Process Isolation

### 9.1 User Directory Isolation

- **File:** `reference/bot/services/file_service.py` (lines 11, 17-21)
- **Type:** Filesystem isolation

Each user gets their own directory:

```python
USER_BOTS_ROOT_DIR = os.path.abspath(settings.UPLOAD_DIR)

def get_user_root(user_id: int) -> str:
    path = os.path.join(USER_BOTS_ROOT_DIR, str(user_id))
    os.makedirs(path, exist_ok=True)
    return path
```

### 9.2 Docker Container Isolation

- **File:** `reference/docker/Dockerfile` (lines 1-39)
- **Type:** Container isolation

Uses `php:8.2-fpm-bullseye` as base image. Runs as non-root `www-data` user.

### 9.3 Supervisord Process Management

- **File:** `reference/supervisord.conf` (lines 1-33)
- **Type:** Process management

Manages three processes with auto-restart: `php-fpm8.2`, `caddy`, `python -m bot`.

---

## 10. Logging & Monitoring

### 10.1 Developer Action Logging

- **File:** `reference/bot/handlers/files.py` (lines 219-237)
- **Type:** Audit logging

Logs all file operations to `files_log.txt` with timestamps when `DEV_MODE = True`:

```python
async def log_action(action: str, details: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{action}] {details}\n"
```

### 10.2 Developer Step Logger

- **File:** `reference/bot/utils/dev_logger.py` (lines 1-46)
- **Type:** Debug logging

`log_step()` logs execution flow with caller info (filename, function, line number) and data dumps. Controlled by `DEV_MODE` flag.

### 10.3 Webhook Dispatch Logging

- **File:** `reference/web/webhook.py` (lines 52-66)
- **Type:** Webhook audit logging

Logs webhook events to `webhook_dispatch_log.txt` when `DEV_MODE` is enabled. Logs token info, IP addresses, payload sizes, and secret match results.

### 10.4 Webhook Logs Table (Database)

- **File:** `reference/bot/core/database.py` (lines 74-83, 522-536)
- **Type:** Database logging

`webhook_logs` table stores delivery status for each webhook. Auto-pruned to keep only 20 most recent logs per token.

### 10.5 AI Usage Logging

- **File:** `reference/bot/core/database.py` (lines 34-45, 454-461)
- **Type:** Usage tracking

`ai_usage_logs` table tracks every AI request with `user_id`, `key_id`, `model_used`, `is_fallback`, `status`, `timestamp`.

### 10.6 Daily Statistics System

- **File:** `reference/bot/core/database.py` (lines 86-95, 541-595)
- **Type:** Analytics

`daily_stats` table tracks per-user, per-day, per-stat counters. Supports time-range queries for day/week/month/year.

### 10.7 Admin Action Logging

- **File:** `reference/bot/core/database.py` (lines 261-274)
- **Type:** Admin audit trail

`marketplace_admin_logs` table tracks all admin actions with `admin_id`, `action_type`, `target_type`, `target_id`, `reason`, `metadata`, `created_at`.

### 10.8 Admin Notifications

- **Files:** Multiple handlers (`main_menu.py`, `billing.py`, etc.)
- **Type:** Real-time alerting

Admins are notified of: new user registrations, code redemptions, folder deletion errors.

---

## 11. Session & State Management

### 11.1 Conversation State Manager

- **File:** `reference/bot/core/state.py`
- **Type:** Multi-step operation tracking

`conversation_manager` tracks user conversation states for multi-step operations (folder creation, file rename, marketplace upload). States include `status`, `context`, and `message_id`.

### 11.2 Delete Confirmation Cache (Time-Limited)

- **File:** `reference/bot/handlers/files.py` (lines 135-141)
- **Type:** Confirmation expiry

```python
DELETE_CONFIRMATION_CACHE = {}

async def cleanup_delete_cache(key: str, delay: int = 600):
    await asyncio.sleep(delay)
    if key in DELETE_CONFIRMATION_CACHE:
        del DELETE_CONFIRMATION_CACHE[key]
```

10-minute expiry on delete confirmations.

### 11.3 Telegram Client Session Rotation

- **File:** `reference/bot/core/client.py` (lines 27-39)
- **Type:** Session management

`reset_client()` can rotate the Telegram session name using `secrets.token_hex(6)`.

### 11.4 Subscription Expiry Check

- **File:** `reference/bot/handlers/main_menu.py` (lines 103-108)
- **Type:** Time-based authorization

On every `/start` and main menu display, `check_subscription_expiry()` verifies if the user's PRO subscription has expired and auto-downgrades them.

### 11.5 Atomic JSON File Writes

- **File:** `reference/bot/core/data_manager.py` (lines 58-74)
- **Type:** Data integrity

All JSON data files written atomically using temp file + `os.replace()`:

```python
temp_path = f"{file_path}.tmp"
with open(temp_path, 'w', ...) as f:
    json.dump(data, f, ...)
    f.flush()
    os.fsync(f.fileno())
os.replace(temp_path, file_path)
```

### 11.6 Thread-Safe Statistics

- **File:** `reference/bot/core/data_manager.py` (line 36)
- **File:** `reference/bot/services/user_service.py` (lines 47-48)
- **Type:** Concurrency safety

`stats_lock = threading.Lock()` for thread-safe access to statistics data.

### 11.7 SQLite WAL Mode

- **File:** `reference/bot/core/database.py` (lines 18-19)
- **Type:** Database concurrency

```python
await db.execute('PRAGMA journal_mode=WAL')
await db.execute('PRAGMA synchronous=NORMAL')
```

---

## 12. Bot Detection & Analysis

### 12.1 Telegram Bot Detector (Static Analysis)

- **File:** `reference/bot/utils/bot_detector.py` (lines 1-607)
- **Type:** Code analysis

Comprehensive static analysis to detect if a PHP file is a Telegram bot:

- **Input pattern detection** (lines 10-17): Detects `php://input`, `$HTTP_RAW_POST_DATA`
- **Token pattern detection** (line 39): `r'\d{6,14}:[a-zA-Z0-9_\-]{35,75}'`
- **Recursive include chain tracing** (lines 197-269): Traces `include`/`require` up to 10 levels deep
- **PSR-4 autoloader detection** (lines 148-194): Resolves namespace-to-directory mappings
- **Dependency map building** (lines 328-371): Builds full dependency graph for multi-file projects

### 12.2 Security Scanner (Test Tool)

- **File:** `reference/test-security/security-scanner.php` (lines 1-216)
- **Type:** Security testing

Read-only PHP security scanner that tests:

- Disabled functions list
- open_basedir configuration
- Sensitive file access (`/etc/passwd`, `/etc/shadow`, `.env`, `.git/config`)
- Directory traversal
- Writable directories
- Network capabilities
- Command execution capabilities

### 12.3 Security Bot (Penetration Test Tool)

- **File:** `reference/test-security/bot.php` (lines 1-1297)
- **Type:** Penetration testing

Comprehensive penetration testing Telegram bot that tests:

- 15+ file reading bypass methods
- Shell execution attempts
- Symlink attacks
- Reverse shell attempts
- Stress/DoS testing
- Data exfiltration methods

---

## 13. Quota System

### 13.1 Storage/Files/Folders Quotas

- **File:** `reference/bot/services/quota_service.py` (lines 1-96)
- **Type:** Resource limiting

| Plan | Storage | Files | Folders |
|------|---------|-------|---------|
| Free | 50 MB | 30 | 5 |
| PRO | 1000 MB | 500 | 50 |

Checked before every file/folder creation and bot execution.

---

## Summary: Security Layers Map

```
┌─────────────────────────────────────────────────────────────┐
│                      NETWORK LAYER                          │
│  Caddy path traversal block │ Payload size limit (1MB)      │
│  Request timeout (10s) │ URL-based routing                  │
├─────────────────────────────────────────────────────────────┤
│                   AUTHENTICATION LAYER                      │
│  SUDO/Admin/Banned hierarchy │ API key auth (prod_*)        │
│  Webhook secret (os.urandom + hmac.compare_digest)          │
│  HMAC WebApp URLs │ Force subscribe gate                    │
├─────────────────────────────────────────────────────────────┤
│                   AUTHORIZATION LAYER                       │
│  Ownership checks │ 3-tier marketplace ban                  │
│  Maintenance mode bypass │ Subscription expiry              │
├─────────────────────────────────────────────────────────────┤
│                 INPUT VALIDATION LAYER                      │
│  Name validation ([a-zA-Z0-9_\-\.]) │ Path traversal block  │
│  HTML escaping │ PHP error sanitization │ Token regex        │
│  JSON validation │ Webhook path validation                  │
├─────────────────────────────────────────────────────────────┤
│                 PHP SANDBOXING LAYER                        │
│  70+ disabled functions │ Dynamic open_basedir (per-user)   │
│  allow_url_include=Off │ .user.ini disabled                 │
│  FPM pool-level disable_functions │ host_bootstrap.php      │
├─────────────────────────────────────────────────────────────┤
│                   FILE SECURITY LAYER                       │
│  Dangerous function scanner │ Extension whitelist           │
│  Symlink blocking │ Size limits (10MB/50MB)                 │
│  Extension enforcement on rename │ System file protection   │
├─────────────────────────────────────────────────────────────┤
│                  ENCRYPTION LAYER                           │
│  Fernet (file paths) │ HMAC-SHA256 (WebApp auth)            │
│  secrets.token_urlsafe (API keys) │ os.urandom (webhooks)   │
├─────────────────────────────────────────────────────────────┤
│                  RATE LIMITING LAYER                        │
│  Per-user (20/min) │ Per-IP (50/min) │ View cooldown (10h)  │
│  AI task queue delays │ Subscription check anti-flood       │
├─────────────────────────────────────────────────────────────┤
│                CONTENT MODERATION LAYER                     │
│  Multi-lang profanity filter │ Obfuscation detection        │
│  3-tier ban system │ Report system │ Whitelist              │
├─────────────────────────────────────────────────────────────┤
│                   ISOLATION LAYER                           │
│  Per-user directories │ Docker www-data (non-root)          │
│  Dynamic open_basedir │ Caddy URL routing                   │
├─────────────────────────────────────────────────────────────┤
│                LOGGING & MONITORING LAYER                   │
│  File operation logs │ Webhook logs │ AI usage logs         │
│  Admin action logs │ Daily stats │ Admin notifications      │
│  Dev step logger │ WebApp server logging                    │
├─────────────────────────────────────────────────────────────┤
│              SESSION & STATE MANAGEMENT LAYER               │
│  Conversation state manager │ Delete confirmation cache     │
│  Session rotation │ Subscription expiry check               │
│  Atomic JSON writes │ Thread-safe stats │ SQLite WAL         │
└─────────────────────────────────────────────────────────────┘
```

---

## File Index

| File | Security Mechanisms |
|------|---------------------|
| `reference/Caddyfile.railway` | Path traversal block, URL routing, dynamic open_basedir, auto_prepend_file |
| `reference/docker/custom.ini` | 70+ disabled functions, allow_url_include=Off, .user.ini disabled |
| `reference/docker/php-fpm-custom.conf` | Pool-level disable_functions |
| `reference/docker/Dockerfile` | Non-root user (www-data) |
| `reference/supervisord.conf` | Process management with auto-restart |
| `reference/encryption.key` | Fernet encryption key |
| `reference/bot/services/user_service.py` | User status hierarchy (sudo/admin/banned/user) |
| `reference/bot/services/file_service.py` | User directory isolation, path confinement |
| `reference/bot/services/marketplace_service.py` | Dangerous function scanner, extension whitelist, size limits |
| `reference/bot/services/profanity_filter.py` | Multi-language profanity filter, 3-tier ban system |
| `reference/bot/services/quota_service.py` | Storage/file/folder quotas |
| `reference/bot/handlers/files.py` | Name validation, ownership checks, Fernet encryption, system file protection |
| `reference/bot/handlers/bots.py` | Webhook secret generation, bot ownership |
| `reference/bot/handlers/web_app.py` | HMAC WebApp authentication |
| `reference/bot/handlers/main_menu.py` | Subscription expiry, admin notifications, host_bootstrap restore |
| `reference/bot/utils/decorators.py` | Force subscribe, maintenance mode, ban checks |
| `reference/bot/utils/text.py` | PHP error sanitization |
| `reference/bot/utils/dev_logger.py` | Developer step logging |
| `reference/bot/utils/bot_detector.py` | Static analysis for Telegram bot detection |
| `reference/bot/core/database.py` | API key gen, webhook logs, AI usage logs, daily stats, admin logs |
| `reference/bot/core/data_manager.py` | Atomic JSON writes, thread-safe stats |
| `reference/bot/core/client.py` | Session rotation |
| `reference/bot/core/state.py` | Conversation state management |
| `reference/bot/core/config.py` | Internal API secret |
| `reference/bot/tasks/ai_queue.py` | AI task queue cooldown |
| `reference/web/webhook.py` | Payload size limit, HMAC verification, path validation, JSON validation |
| `reference/web/internal_api_server.py` | Rate limiting (per-user + per-IP), path sanitization, token regex |
| `reference/web/webapp_server.py` | Symlink protection, encrypted path decryption |
| `reference/config/host_bootstrap.php` | Auto-prepended PHP bootstrap |
| `reference/test-security/security-scanner.php` | Security testing tool |
| `reference/test-security/bot.php` | Penetration testing bot |
