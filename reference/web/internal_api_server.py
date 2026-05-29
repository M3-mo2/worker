# internal_api_server.py (Async Version using Quart)
import os
import re
import uvicorn
import logging
import time
import httpx
import json
from collections import defaultdict
from pathlib import Path

from quart import Quart, request, jsonify
from werkzeug.exceptions import HTTPException

from bot.core.config import settings
from bot.core import database
from bot.core.data_manager import load_all_users, load_bots_data, save_all_users

# --- Settings ---
BOTS_DIR = settings.UPLOAD_DIR
MAX_PATH_LENGTH = 255
TELEGRAM_TOKEN_REGEX = re.compile(r'^\d{8,10}:[a-zA-Z0-9_-]{35}$')

# Enhanced Rate Limiting
RATE_LIMIT_SECONDS = 60
RATE_LIMIT_REQUESTS = 20  # Per user
IP_RATE_LIMIT_REQUESTS = 50  # Per IP
MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB
REQUEST_TIMEOUT = 10  # seconds

# --- In-memory store for rate limiting ---
rate_limit_tracker = {}  # { "user_id": [timestamp1, ...] }
ip_rate_limit_tracker = defaultdict(list)  # { "ip": [timestamp1, ...] }

app = Quart(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

# --- Security and Helper Functions ---

def get_client_ip():
    """Gets the real client IP address."""
    # Check for proxy headers
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr

def check_ip_rate_limit(ip_address):
    """Checks if an IP has exceeded the request limit."""
    current_time = time.time()
    
    # Clean old timestamps
    ip_rate_limit_tracker[ip_address] = [
        t for t in ip_rate_limit_tracker[ip_address] 
        if t > current_time - RATE_LIMIT_SECONDS
    ]
    
    if len(ip_rate_limit_tracker[ip_address]) >= IP_RATE_LIMIT_REQUESTS:
        return False  # Limit exceeded
    
    ip_rate_limit_tracker[ip_address].append(current_time)
    return True

def check_rate_limit(user_id):
    """Checks if a user has exceeded their request limit."""
    current_time = time.time()
    if user_id not in rate_limit_tracker:
        rate_limit_tracker[user_id] = []

    request_timestamps = [t for t in rate_limit_tracker[user_id] if t > current_time - RATE_LIMIT_SECONDS]
    
    if len(request_timestamps) >= RATE_LIMIT_REQUESTS:
        return False  # Limit exceeded

    request_timestamps.append(current_time)
    rate_limit_tracker[user_id] = request_timestamps
    return True

def validate_and_sanitize_path(user_id, relative_path):
    """
    Validates that a path is safe and within the user's directory.
    Returns the absolute, safe path or raises a ValueError.
    """
    if not isinstance(relative_path, str) or '..' in relative_path.split(os.path.sep) or len(relative_path) > MAX_PATH_LENGTH:
        raise ValueError("Path is invalid or contains traversal characters.")

    user_dir = os.path.abspath(os.path.join(BOTS_DIR, str(user_id)))
    os.makedirs(user_dir, exist_ok=True)

    absolute_path = os.path.abspath(os.path.join(user_dir, relative_path))

    if os.path.commonprefix([absolute_path, user_dir]) != user_dir:
        raise ValueError("Path traversal attempt detected.")
        
    return absolute_path

def get_user_id_from_request():
    """استخراج user_id من query parameters مع التحقق."""
    user_id = request.args.get('user_id')
    if not user_id or not user_id.isdigit():
        raise ValueError("Invalid or missing user_id parameter")
    return int(user_id)

def build_file_tree(root_path, max_depth=5, current_depth=0):
    """بناء شجرة الملفات بشكل آمن."""
    if current_depth >= max_depth:
        return []
    
    tree = []
    try:
        items = sorted(os.listdir(root_path), key=lambda s: s.lower())
    except OSError:
        return []

    for item in items:
        if item.startswith('.'):
            continue
            
        path = os.path.join(root_path, item)
        try:
            if os.path.isdir(path) and not os.path.islink(path):
                tree.append({
                    'name': item,
                    'type': 'folder',
                    'path': os.path.relpath(path, os.path.join(BOTS_DIR))
                })
            elif os.path.isfile(path) and not os.path.islink(path):
                file_size = os.path.getsize(path)
                tree.append({
                    'name': item,
                    'type': 'file',
                    'path': os.path.relpath(path, os.path.join(BOTS_DIR)),
                    'size': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2)
                })
        except (OSError, ValueError):
            continue
    
    return tree

# --- General Error Handling ---
@app.errorhandler(HTTPException)
async def handle_http_exception(e):
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "error": e.description,
    }).get_data()
    response.content_type = "application/json"
    return response

@app.errorhandler(Exception)
async def handle_generic_exception(e):
    app.logger.error("An unexpected error occurred on the internal API server", exc_info=True)
    return jsonify({"error": "Internal Server Error"}), 500

@app.errorhandler(413)
async def handle_payload_too_large(e):
    """Handle request payload too large."""
    return jsonify({"error": "Request payload too large. Maximum size is 1 MB."}), 413

# --- Request timeout handler ---
@app.before_request
async def before_request():
    """Set timeout for all requests."""
    request.timeout = REQUEST_TIMEOUT

# --- Main API Endpoint ---
@app.route('/api/request_action', methods=['POST'])
async def request_action():
    # 0. IP Rate Limiting (First line of defense)
    client_ip = get_client_ip()
    if not check_ip_rate_limit(client_ip):
        app.logger.warning(f"IP rate limit exceeded for {client_ip}")
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    
    # 1. Basic Request Validation
    if not request.is_json:
        return jsonify({"error": "Invalid request: Content-Type must be application/json"}), 400
    
    data = await request.get_json()
    api_key = data.get('api_key')
    action = data.get('action')
    payload = data.get('payload')

    if not all([api_key, action, payload]):
        return jsonify({"error": "Missing required fields: api_key, action, payload"}), 400

    # 2. Authentication & Authorization (using the new database functions)
    user_creds = await database.get_user_by_dev_api_key(api_key)
    if not user_creds:
        return jsonify({"error": "Authentication failed: Invalid API key"}), 401

    if not user_creds['is_enabled']:
        return jsonify({"error": "Authorization failed: API key is disabled"}), 403

    user_id = user_creds['user_id']

    # 3. Rate Limiting
    if not check_rate_limit(user_id):
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

    # 4. Process Action
    main_bot_api_url = f"http://127.0.0.1:{settings.web.MAIN_BOT_INTERNAL_API_PORT}/execute_action"
    headers = {"X-Internal-Secret": settings.INTERNAL_SECRET}
    
    # This data will be forwarded to the main bot process
    data_to_forward = {
        "action": action,
        "user_id": user_id,
        "payload": {}
    }

    try:
        if action == 'set_webhook':
            bot_token = payload.get('new_bot_token')
            bot_path = payload.get('new_bot_path')

            if not bot_token or not bot_path:
                return jsonify({"error": "Payload for 'set_webhook' must contain 'new_bot_token' and 'new_bot_path'"}), 400
            
            if not TELEGRAM_TOKEN_REGEX.match(bot_token):
                return jsonify({"error": "Invalid 'new_bot_token' format."}), 400

            sanitized_path = validate_and_sanitize_path(user_id, bot_path)
            if not os.path.isfile(sanitized_path):
                return jsonify({"error": f"File not found at specified path: {bot_path}"}), 404

            data_to_forward['payload'] = {"bot_token": bot_token, "bot_path": sanitized_path}

        elif action == 'delete_webhook':
            bot_token = payload.get('bot_token')
            if not bot_token:
                return jsonify({"error": "Payload for 'delete_webhook' must contain 'bot_token'"}), 400
            
            data_to_forward['payload'] = {"bot_token": bot_token}
        
        else:
            return jsonify({"error": f"Unsupported action: {action}"}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 403  # Path validation errors

    # 5. Call the Main Bot's Internal API for immediate execution
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(main_bot_api_url, json=data_to_forward, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status() # Raise an exception for 4xx/5xx responses
            
            # If successful, log the API request in the database
            await database.log_api_request(api_key)
            
            # Return the response from the main bot directly to the user
            return jsonify(response.json()), response.status_code

    except httpx.RequestError as e:
        app.logger.error(f"Could not connect to main bot internal API: {e}")
        return jsonify({"error": "Internal communication error. The main bot might be down."}), 503
    except httpx.HTTPStatusError as e:
        app.logger.error(f"Error response from main bot internal API: {e.response.status_code} - {e.response.text}")
        # Return the specific error from the main bot
        return jsonify(e.response.json()), e.response.status_code


# ===== New WebApp API Endpoints =====

@app.route('/api/user/info', methods=['GET'])
async def get_user_info():
    """جلب معلومات المستخدم من query parameters والـ database."""
    try:
        user_id = get_user_id_from_request()
        
        # جلب بيانات المستخدم من JSON
        all_users = load_all_users()
        user_data = all_users.get(str(user_id), {})
        
        # بناء الرد مع البيانات المتاحة
        response = {
            "user_id": user_id,
            "username": request.args.get('username', 'anonymous'),
            "first_name": request.args.get('first_name', ''),
            "last_name": request.args.get('last_name', ''),
            "points": int(request.args.get('points', 0)),
            "plan": request.args.get('plan', 'free').lower(),
            "is_premium": request.args.get('is_premium', 'false').lower() == 'true',
            # من الـ database
            "total_points": user_data.get('points', 0),
            "files_count": user_data.get('files_count', 0),
            "bots_count": user_data.get('bots_count', 0),
            "joined_date": user_data.get('joined_date', None),
        }
        
        return jsonify(response), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error fetching user info: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/user/files', methods=['GET'])
async def get_user_files():
    """جلب قائمة ملفات المستخدم."""
    try:
        user_id = get_user_id_from_request()
        
        # التحقق من أن مجلد المستخدم موجود
        user_dir = os.path.abspath(os.path.join(BOTS_DIR, str(user_id)))
        os.makedirs(user_dir, exist_ok=True)
        
        # بناء شجرة الملفات
        files_tree = build_file_tree(user_dir)
        
        # حساب استخدام التخزين
        total_size = 0
        def get_dir_size(path):
            total = 0
            try:
                for entry in os.scandir(path):
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += get_dir_size(entry.path)
            except OSError:
                pass
            return total
        
        total_size = get_dir_size(user_dir)
        
        return jsonify({
            "user_id": user_id,
            "files": files_tree,
            "total_files": len(files_tree),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "total_size_gb": round(total_size / (1024 * 1024 * 1024), 2),
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error fetching user files: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/user/bots', methods=['GET'])
async def get_user_bots():
    """جلب بيانات بوتات المستخدم."""
    try:
        user_id = get_user_id_from_request()
        
        bots_data = load_bots_data()
        user_bots = bots_data.get(str(user_id), {})
        
        bots_list = []
        for bot_id, bot_info in user_bots.items():
            bots_list.append({
                "id": bot_id,
                "token": bot_info.get('token', ''),
                "webhook": bot_info.get('webhook', ''),
                "status": bot_info.get('status', 'inactive'),
                "users_count": bot_info.get('users_count', 0),
                "uptime": bot_info.get('uptime', 0),
                "last_update": bot_info.get('last_update', None),
            })
        
        return jsonify({
            "user_id": user_id,
            "bots": bots_list,
            "total_bots": len(bots_list),
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error fetching user bots: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/user/stats', methods=['GET'])
async def get_user_stats():
    """جلب الإحصائيات للمستخدم."""
    try:
        user_id = get_user_id_from_request()
        all_users = load_all_users()
        bots_data = load_bots_data()
        user_data = all_users.get(str(user_id), {})
        user_bots = bots_data.get(str(user_id), {})
        
        # حساب استخدام التخزين
        user_dir = os.path.abspath(os.path.join(BOTS_DIR, str(user_id)))
        total_size = 0
        def get_dir_size(path):
            total = 0
            try:
                for entry in os.scandir(path):
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += get_dir_size(entry.path)
            except OSError:
                        pass
            return total
        
        if os.path.exists(user_dir):
            total_size = get_dir_size(user_dir)
        
        return jsonify({
            "user_id": user_id,
            "total_files": len(os.listdir(user_dir)) if os.path.exists(user_dir) else 0,
            "total_bots": len(user_bots),
            "storage_mb": round(total_size / (1024 * 1024), 2),
            "storage_gb": round(total_size / (1024 * 1024 * 1024), 2),
            "points": user_data.get('points', 0),
            "uptime_percent": user_data.get('uptime', 0),
            "api_requests": user_data.get('api_requests', 0),
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error fetching user stats: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/files/read', methods=['GET'])
async def read_file():
    """قراءة محتوى ملف."""
    try:
        user_id = get_user_id_from_request()
        file_path = request.args.get('path', '')
        
        if not file_path:
            return jsonify({"error": "Missing file path"}), 400
        
        # التحقق من الأمان
        safe_path = validate_and_sanitize_path(user_id, file_path)
        
        if not os.path.isfile(safe_path):
            return jsonify({"error": "File not found"}), 404
        
        # حماية من الملفات الكبيرة جداً
        file_size = os.path.getsize(safe_path)
        if file_size > 5 * 1024 * 1024:  # 5 MB limit
            return jsonify({"error": "File is too large (>5MB)", "size_mb": round(file_size / (1024 * 1024), 2)}), 413
        
        try:
            with open(safe_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            return jsonify({"error": f"Unable to read file: {str(e)}"}), 400
        
        return jsonify({
            "path": file_path,
            "content": content,
            "size_bytes": file_size,
            "size_kb": round(file_size / 1024, 2),
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        app.logger.error(f"Error reading file: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/files/write', methods=['POST'])
async def write_file():
    """حفظ محتوى ملف."""
    try:
        user_id = get_user_id_from_request()
        data = await request.get_json()
        file_path = data.get('path', '')
        content = data.get('content', '')
        
        if not file_path:
            return jsonify({"error": "Missing file path"}), 400
        
        # التحقق من الأمان
        safe_path = validate_and_sanitize_path(user_id, file_path)
        
        # التأكد من أن المجلد الأب موجود
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        
        try:
            with open(safe_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            return jsonify({"error": f"Unable to write file: {str(e)}"}), 400
        
        return jsonify({
            "path": file_path,
            "message": "File saved successfully",
            "size_bytes": len(content.encode('utf-8')),
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        app.logger.error(f"Error writing file: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/files/delete', methods=['DELETE'])
async def delete_file():
    """حذف ملف."""
    try:
        user_id = get_user_id_from_request()
        file_path = request.args.get('path', '')
        
        if not file_path:
            return jsonify({"error": "Missing file path"}), 400
        
        # التحقق من الأمان
        safe_path = validate_and_sanitize_path(user_id, file_path)
        
        if not os.path.isfile(safe_path):
            return jsonify({"error": "File not found"}), 404
        
        try:
            os.remove(safe_path)
        except Exception as e:
            return jsonify({"error": f"Unable to delete file: {str(e)}"}), 400
        
        return jsonify({
            "path": file_path,
            "message": "File deleted successfully",
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        app.logger.error(f"Error deleting file: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/health', methods=['GET'])
async def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "internal_api_server",
        "timestamp": time.time(),
    }), 200


if __name__ == '__main__':
    host = settings.web.INTERNAL_API_HOST
    port = settings.web.INTERNAL_API_PORT
    app.logger.info(f"Starting Internal API Server (Uvicorn) on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")