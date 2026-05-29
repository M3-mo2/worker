# bot/services/php_engine.py
# Manages the local PHP engine (Caddy + PHP-FPM) without Docker.
# Replaces bot/services/docker.py for Railway deployment.

import asyncio
import os
import logging
import subprocess
import time
from typing import Tuple, List, Optional
import aiohttp

from bot.core.config import settings

logger = logging.getLogger("PhpEngine")

# Track managed processes for cleanup
_php_fpm_process: Optional[subprocess.Popen] = None
_caddy_process: Optional[subprocess.Popen] = None


def _is_fpm_socket_active() -> bool:
    """Check if PHP-FPM socket is already listening (managed by supervisord)."""
    import socket
    sock_path = "/run/php/php8.2-fpm.sock"
    if not os.path.exists(sock_path):
        return False
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect(sock_path)
        s.close()
        return True
    except (ConnectionRefusedError, FileNotFoundError, OSError):
        return False


def _is_port_open(port: int) -> bool:
    """Check if a TCP port is already listening."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('127.0.0.1', port)) == 0
    except OSError:
        return False


def setup_php_engine() -> bool:
    """
    Starts PHP-FPM and Caddy as local processes.
    Skips if they are already running (managed by supervisord).
    Returns True if both are available.
    """
    global _php_fpm_process, _caddy_process

    # --- Start PHP-FPM ---
    if _is_fpm_socket_active():
        logger.info("PHP-FPM socket already active (managed by supervisord). Skipping start.")
    else:
        fpm_started = False
        for fpm_cmd in ["php-fpm8.2", "php-fpm"]:
            try:
                _php_fpm_process = subprocess.Popen(
                    [fpm_cmd, "--nodaemonize"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                logger.info(f"PHP-FPM started via '{fpm_cmd}' (PID: {_php_fpm_process.pid})")
                fpm_started = True
                break
            except FileNotFoundError:
                continue
            except Exception as e:
                logger.error(f"Failed to start PHP-FPM with '{fpm_cmd}': {e}")
                return False
        if not fpm_started:
            logger.error("PHP-FPM not found. Install php8.2-fpm.")
            return False

        # Brief wait for FPM to initialize
        time.sleep(2)

        if _php_fpm_process.poll() is not None:
            stderr = _php_fpm_process.stderr.read().decode() if _php_fpm_process.stderr else ""
            if "already listen" in stderr:
                logger.info("PHP-FPM socket already in use. Assuming managed externally.")
            else:
                logger.error(f"PHP-FPM exited immediately. stderr: {stderr[:500]}")
                return False

    # --- Start Caddy ---
    caddy_port = settings.php_engine.CADDY_PORT
    if _is_port_open(caddy_port):
        logger.info(f"Caddy already listening on port {caddy_port}. Skipping start.")
    else:
        caddyfile_path = os.path.join(settings.PROJECT_ROOT, "Caddyfile.railway")
        if not os.path.exists(caddyfile_path):
            logger.error(f"Caddyfile not found at {caddyfile_path}")
            return False

        try:
            _caddy_process = subprocess.Popen(
                ["caddy", "run", "--config", caddyfile_path, "--adapter", "caddyfile"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logger.info(f"Caddy started (PID: {_caddy_process.pid})")
        except Exception as e:
            logger.error(f"Failed to start Caddy: {e}")
            return False

        # Brief wait for Caddy to initialize
        time.sleep(2)

        if _caddy_process.poll() is not None:
            stderr = _caddy_process.stderr.read().decode() if _caddy_process.stderr else ""
            logger.error(f"Caddy exited immediately. stderr: {stderr[:500]}")
            return False

    logger.info("PHP Engine (Caddy + PHP-FPM) is running.")
    return True


async def execute_php_via_http(
    file_path_host: str,
    php_flags: Optional[List[str]] = None,
    timeout: int = 10
) -> Tuple[int, str, str]:
    """
    Executes a PHP script. Replaces execute_php_in_docker().

    - For lint (php_flags contains '-l'): runs `php -l` locally via subprocess.
      This is safe because linting only parses, it does not execute code.
    - For execution: sends HTTP request to local Caddy, which enforces
      open_basedir + disable_functions (same security as webhook flow).

    :param file_path_host: Absolute path to the PHP file on the host.
    :param php_flags: Optional PHP flags.
    :param timeout: Timeout in seconds.
    :return: Tuple of (exit_code, stdout, stderr).
    """
    upload_dir = os.path.abspath(settings.UPLOAD_DIR)
    if not file_path_host.startswith(upload_dir):
        return 1, "", "Error: File path is not within allowed user bots directory."

    rel_path = os.path.relpath(file_path_host, upload_dir).replace(os.sep, "/")

    # Check if this is a lint-only request
    is_lint = php_flags and "-l" in php_flags

    if is_lint:
        return await _run_php_locally(file_path_host, ["-l"], timeout)

    # For execution: send HTTP request to Caddy
    caddy_port = settings.php_engine.CADDY_PORT
    caddy_url = f"http://127.0.0.1:{caddy_port}/{rel_path}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                caddy_url,
                json={},
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as resp:
                body = await resp.text()
                exit_code = 0 if 200 <= resp.status < 300 else 1

                # Detect PHP errors in response body
                error_signatures = [
                    '<b>warning</b>', '<b>fatal error</b>',
                    '<b>parse error</b>', '<b>notice</b>',
                    'uncaught exception'
                ]
                body_lower = body.lower()
                if any(sig in body_lower for sig in error_signatures):
                    return exit_code, "", body

                return exit_code, body, ""
    except asyncio.TimeoutError:
        return 1, "", f"Execution timed out after {timeout} seconds."
    except Exception as e:
        return 1, "", f"HTTP execution failed: {e}"


async def _run_php_locally(
    file_path_host: str,
    php_flags: List[str],
    timeout: int
) -> Tuple[int, str, str]:
    """Runs PHP CLI directly (for linting only - does NOT execute code)."""
    cmd = ["php"]
    cmd.extend(php_flags)
    cmd.append(file_path_host)

    try:
        result = await asyncio.to_thread(
            subprocess.run, cmd, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", f"Execution timed out after {timeout} seconds."
    except Exception as e:
        return 1, "", f"PHP execution failed: {e}"


def get_php_container_name_for_tier(tier: str) -> str:
    """
    Backward compatibility stub.
    Returns a dummy name since we no longer use Docker containers.
    Callers should migrate to execute_php_via_http() directly.
    """
    return "local"


def shutdown_php_engine():
    """Gracefully stop managed processes."""
    global _php_fpm_process, _caddy_process
    for proc_name, proc in [("Caddy", _caddy_process), ("PHP-FPM", _php_fpm_process)]:
        if proc and proc.poll() is None:
            logger.info(f"Stopping {proc_name} (PID: {proc.pid})")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


print("✅ PHP Engine service module initialized.")
