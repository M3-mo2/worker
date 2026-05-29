# bot_v2/bot/services/docker.py
# Encapsulates direct interactions with Docker containers.

import asyncio
import subprocess
import os
from typing import Tuple, List, Optional

# Local Imports from bot_v2 core
from bot.core.config import settings

async def execute_php_in_docker(
    file_path_host: str,
    container_name: str = settings.docker.DOCKER_CONTAINER_NAME_FREE, # Default to free tier container
    php_flags: Optional[List[str]] = None,
    timeout: int = 10
) -> Tuple[int, str, str]:
    """
    Executes a PHP script inside a Docker container.

    :param file_path_host: Absolute path to the PHP file on the host.
    :param container_name: The name of the Docker container to execute in.
    :param php_flags: Optional list of PHP flags (e.g., ["-d", "display_errors=1"]).
    :param timeout: Timeout for the Docker command.
    :return: Tuple of (exit_code, stdout, stderr).
    """
    upload_dir = os.path.abspath(settings.UPLOAD_DIR)
    if not file_path_host.startswith(upload_dir):
        return 1, "", "Error: File path is not within allowed user bots directory."

    rel_path = os.path.relpath(file_path_host, upload_dir)
    container_path = os.path.join("/app/user_bots", rel_path).replace('\\', '/')

    cmd = ["docker", "exec", container_name, "php"]
    if php_flags:
        cmd.extend(php_flags)
    cmd.append(container_path)

    try:
        result = await asyncio.to_thread(subprocess.run, cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", f"Execution timed out after {timeout} seconds."
    except Exception as e:
        return 1, "", f"Docker execution failed: {e}"


async def get_php_container_name_for_tier(tier: str) -> str:
    """
    Returns the appropriate Docker container name based on the user's tier.
    :param tier: 'free' or 'pro'.
    :return: Docker container name.
    """
    if tier == 'pro':
        return settings.docker.DOCKER_CONTAINER_NAME_PAID
    return settings.docker.DOCKER_CONTAINER_NAME_FREE


def check_docker() -> bool:
    """Checks if Docker is installed and the daemon is running."""
    try:
        subprocess.run(['docker', 'info'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def setup_docker_network() -> bool:
    """Checks for and creates the docker network with a static subnet."""
    network_name = settings.docker.DOCKER_NETWORK_NAME
    subnet = settings.docker.DOCKER_SUBNET

    try:
        subprocess.run(['docker', 'network', 'inspect', network_name], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Creating Docker network '{network_name}' with subnet {subnet}...")
        try:
            subprocess.run(['docker', 'network', 'create', f'--subnet={subnet}', network_name], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"--- DOCKER NETWORK CREATION FAILED ---\n{e.stderr.decode()}")
            return False

def setup_php_engine() -> bool:
    """Builds the PHP engine image and runs containers for free and paid tiers."""
    if not check_docker():
        print("--- DOCKER ERROR: Docker is not running or not installed ---")
        return False

    if not setup_docker_network():
        return False

    image_name = settings.docker.DOCKER_IMAGE_NAME
    print(f"Building PHP engine image ({image_name})...")
    
    # Determine the absolute path to the project root (where Dockerfile is located)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_file_dir, '..', '..'))
    dockerfile_path = os.path.join(project_root, 'docker', 'Dockerfile')

    if not os.path.exists(dockerfile_path):
        print(f"❌ CRITICAL: Dockerfile not found at: {dockerfile_path}")
        return False

    try:
        subprocess.run(['docker', 'build', '-f', 'docker/Dockerfile', '-t', image_name, '.'], cwd=project_root, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"--- DOCKER BUILD FAILED ---\n{e.stderr.decode()}")
        return False

    host_bots_dir = os.path.abspath(settings.UPLOAD_DIR)
    network_name = settings.docker.DOCKER_NETWORK_NAME
    
    gateway_ip = settings.docker.GATEWAY_IP

    def _run_container(name, port, cpus, memory):
        subprocess.run(['docker', 'rm', '-f', name], capture_output=True)
        cmd = [
            'docker', 'run', '-d', '--name', name, '--network', network_name,
            '--add-host', f'api.host:{gateway_ip}', '-p', f'127.0.0.1:{port}:8000',
            '--cpus', str(cpus), '--memory', memory, '--restart', 'always',
            '--security-opt=no-new-privileges', '--pids-limit', '512',
            '-v', f'{host_bots_dir}:/app/user_bots', image_name
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Container '{name}' started on port {port}.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"--- FAILED TO START {name} ---\n{e.stderr.decode()}")
            return False

    free_ok = _run_container(settings.docker.DOCKER_CONTAINER_NAME_FREE, settings.docker.PHP_ENGINE_FREE_PORT, 0.2, '100m')
    paid_ok = _run_container(settings.docker.DOCKER_CONTAINER_NAME_PAID, settings.docker.PHP_ENGINE_PAID_PORT, 1.6, '4g')
    
    return free_ok and paid_ok

print("✅ Docker Service module initialized.")
