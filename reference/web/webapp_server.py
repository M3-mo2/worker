from flask import Flask, request, render_template_string, abort
import os
import sys
import logging
from waitress import serve
from urllib.parse import quote
from cryptography.fernet import Fernet, InvalidToken
from bot.core.config import settings
from bot.utils.dev_logger import log_step

# --- Logging Setup for Debugging 502 Errors ---
log_dir = os.path.join(settings.PROJECT_ROOT, 'data')
os.makedirs(log_dir, exist_ok=True)

# Setup Logger with both File and Console handlers
logger = logging.getLogger('webapp_server')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_dir, 'webapp_server.log'))
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('✅ [WebApp] %(message)s'))
logger.addHandler(console_handler)

app = Flask(__name__)

# --- Security Configuration ---
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max file size
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for security

# --- Encryption Setup ---
try:
    # Resolve path relative to this script to match the exact structure provided
    # Script: .../bot_v2/web/webapp_server.py -> Key: .../bot_v2/encryption.key
    key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'encryption.key'))
    logger.info(f"Loading encryption key from: {key_path}")

    with open(key_path, 'rb') as key_file:
        ENCRYPTION_KEY = key_file.read()
    cipher_suite = Fernet(ENCRYPTION_KEY)
    logger.info("Encryption key loaded successfully.")
    print(f"✅ [WebApp] Encryption key loaded successfully from {key_path}")
except Exception as e:
    logger.error(f"CRITICAL: Failed to load encryption key: {e}")
    logger.error(f"WebApp Server CRITICAL: encryption.key not found at {key_path}!")
    print(f"❌ [WebApp] CRITICAL: Failed to load encryption key from {key_path}: {e}")
    ENCRYPTION_KEY = None
    cipher_suite = None

BOTS_DIR = settings.UPLOAD_DIR
MAX_EDITOR_SIZE = 512 * 1024  # 512 KB Limit for editing

def detect_mode_by_filename(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    mapping = {
        'php': 'php',
        'py': 'python',
        'js': 'javascript',
        'html': 'html',
        'css': 'css',
        'json': 'json',
        'sh': 'sh',
        'txt': 'text'
    }
    return mapping.get(ext, 'text')

def build_file_tree(root_path, current_file_path):
    tree = []
    try:
        items = sorted(os.listdir(root_path), key=lambda s: s.lower())
    except OSError:
        return []

    dirs = []
    files = []
    for item in items:
        path = os.path.join(root_path, item)
        if os.path.isdir(path):
            dirs.append(item)
        else:
            files.append(item)
    
    # Process directories first
    for d in dirs:
        abs_path = os.path.join(root_path, d)
        children = build_file_tree(abs_path, current_file_path)
        
        is_expanded = False
        # Check if current file is inside this directory to expand it by default
        if current_file_path.startswith(abs_path + os.sep):
            is_expanded = True
            
        tree.append({
            'name': d,
            'type': 'folder',
            'children': children,
            'expanded': is_expanded
        })

    # Process files
    for f in files:
        if not f.endswith(('.php', '.json', '.txt', '.py', '.html', '.css', '.js', '.sh')):
            continue
            
        abs_path = os.path.join(root_path, f)
        rel_p = os.path.relpath(abs_path, BOTS_DIR)
        rel_p_normalized = rel_p.replace(os.path.sep, '/')
        
        try:
            enc_p = cipher_suite.encrypt(rel_p_normalized.encode('utf-8')).decode('utf-8')
            url = f"{settings.web.BASE_URL}/webapp/edit/{quote(enc_p)}"
            is_active = (abs_path == current_file_path)
            
            tree.append({
                'name': f,
                'type': 'file',
                'url': url,
                'active': is_active
            })
        except Exception:
            pass
            
    return tree

# --- Health Check Route ---
@app.route('/ping')
def ping():
    return "pong", 200

@app.route("/webapp/edit/<encrypted_path>", methods=["GET","POST"])
@app.route("/edit/<encrypted_path>", methods=["GET","POST"])
def edit_file(encrypted_path):
    log_step("webapp_entry", f"Request to edit file", {"method": request.method, "encrypted_path": encrypted_path})
    
    if not cipher_suite:
        log_step("webapp_error", "Encryption not configured")
        return abort(500, "Encryption is not configured on the server.")

    try:
        decrypted_path = cipher_suite.decrypt(encrypted_path.encode('utf-8')).decode('utf-8')
        log_step("webapp_decrypt", "Path decrypted successfully", {"decrypted_path": decrypted_path})
    except InvalidToken:
        log_step("webapp_error", "Invalid encryption token")
        return abort(403, "رابط غير صالح أو تم التلاعب به.")

    file_path = os.path.abspath(os.path.join(BOTS_DIR, decrypted_path))
    log_step("webapp_path_check", "Resolved absolute path", {"file_path": file_path})

    if not file_path.startswith(BOTS_DIR):
        log_step("webapp_security", "Path traversal attempt blocked", {"file_path": file_path})
        return abort(403, "محاولة وصول غير مسموح بها.")

    if not os.path.exists(file_path):
        log_step("webapp_error", "File not found", {"file_path": file_path})
        return abort(404, "الملف غير موجود")
    
    if os.path.islink(file_path):
        log_step("webapp_security", "Symlink access blocked", {"file_path": file_path})
        return abort(403, "محاولة وصول غير مسموح بها (Symlinks).")

    if request.method == "POST":
        log_step("webapp_save", "Saving file content", {"file_path": file_path})
        new_content = request.form.get("code", "")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return "OK"

    # --- 1. Large File Protection (The Fix) ---
    file_stat = os.stat(file_path)
    is_read_only = False
    warning_msg = ""

    if file_stat.st_size > MAX_EDITOR_SIZE:
        is_read_only = True
        warning_msg = f"⚠️ الملف كبير جداً ({file_stat.st_size / 1024:.1f} KB). وضع القراءة فقط (أول 10KB)."
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            code_content = f.read(10240) # Read only first 10KB
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()

    filename = os.path.basename(decrypted_path)
    ace_mode = detect_mode_by_filename(filename)

    user_id_for_settings = abs(hash(decrypted_path))

    # --- 2. File Tree Generation (Sidebar) ---
    # Assuming path structure: user_id/path/to/file
    # Ensure we handle paths correctly regardless of OS separator
    user_id_str = decrypted_path.replace('\\', '/').split('/')[0]
    user_root_abs = os.path.join(BOTS_DIR, user_id_str)
    
    file_tree = []
    if os.path.exists(user_root_abs):
        file_tree = build_file_tree(user_root_abs, file_path)

    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <title>تعديل الملف - {{ filename }}</title>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <style>
            :root {
                --font-size: 14px;
                --font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace;
            }
            body { margin:0; font-family: Arial, sans-serif; background:#1e1e1e; color:#eee; }
            header {
                padding:6px 10px;
                background:#111;
                display:flex;
                align-items:center;
                gap:8px;
                border-bottom: 1px solid #333;
                height: 40px;
                flex-shrink: 0;
                position: sticky;
                top: 0;
                z-index: 60; /* Higher than sidebar */
                box-sizing: content-box;
            }
            header h3 { 
                margin:0; 
                font-size:15px; 
                flex-grow:1; 
                color:#ccc; 
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                min-width: 0; /* Allow shrinking in flex container */
                max-width: 40%; /* Limit width to prevent pushing buttons */
            }
            
            /* Layout Container */
            #main-container { display: flex; }
            
            /* Sidebar */
            #sidebar {
                position: absolute;
                top: 53px; /* Below header (40px height + 12px padding + 1px border) */
                right: 0;
                bottom: 0;
                width: 250px;
                background: #252526;
                border-left: 1px solid #444;
                overflow-y: auto;
                z-index: 50;
                box-shadow: -3px 0 12px rgba(0,0,0,0.4);
                display: block; /* Always block, visibility controlled by transform */
                transform: translateX(100%); /* Hidden off-screen to the right */
                transition: transform 0.25s ease-out;
            }
            #sidebar.open {
                transform: translateX(0); /* Slide into view */
            }
            
            /* Tree View Styles */
            ul.tree-list { list-style: none; padding: 0; margin: 0; }
            ul.tree-list li { margin: 0; padding: 0; }
            
            .tree-item {
                display: flex;
                align-items: center;
                padding: 4px 10px;
                cursor: pointer;
                font-size: 13px;
                color: #cccccc;
                text-decoration: none;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                border-left: 2px solid transparent;
            }
            .tree-item:hover { background-color: #2a2d2e; color: #ffffff; }
            .tree-item.active { background-color: #37373d; color: #ffffff; border-left-color: #007acc; }

            .tree-item .label {
                flex-grow: 1;
                min-width: 0; /* Allow text to truncate within flex item */
                overflow: hidden;
                white-space: nowrap;
                text-overflow: ellipsis;
            }
            
            .tree-children { padding-right: 14px; }
            
            .icon { margin-left: 6px; width: 16px; text-align: center; display: inline-block; }
            .folder-arrow {
                font-size: 10px; margin-left: 5px; transition: transform 0.2s;
                display: inline-block; width: 10px; text-align: center; color: #999;
            }
            /* RTL: Arrow points left (<) normally. Rotate -90deg to point down. */
            .folder.expanded .folder-arrow { transform: rotate(-90deg); }

            /* Editor Area */
            #editor { 
                flex-grow: 1;
                position: relative;
                font-size: var(--font-size);
                font-family: var(--font-family);
            }
            
            /* Custom Cursor with Tail */
            .ace_cursor {
                border-left: 2px solid #007acc !important;
            }
            .ace_cursor::after {
                content: '';
                position: absolute;
                top: 100%;
                left: -5px;
                width: 10px;
                height: 10px;
                background: #007acc;
                border-radius: 50% 50% 50% 0;
                transform: rotate(45deg);
                margin-top: -4px;
                pointer-events: none;
            }

            .btn {
                padding:6px 12px;
                background:#333;
                color:#fff;
                border:none;
                border-radius:4px;
                cursor:pointer;
                font-size:14px;
                transition: background 0.2s;
            }
            .btn:disabled { background:#222; cursor:not-allowed; color:#777; }
            .btn:hover:enabled { background:#555; }
            .btn-green { background:#2e8b57; }
            .btn-green:disabled { background:#2e8b57aa; color:#ccc; }
            .btn-icon { font-size: 20px; padding: 2px 8px; }

            /* Warning Banner */
            #warning-banner {
                background: #5a1e1e; color: #fff; padding: 5px; text-align: center; font-size: 12px;
                display: none;
            }

            /* Settings Panel */
            #settings-panel {
                display: none;
                position: absolute;
                top: 45px;
                left: 10px;
                background: #2a2a2a;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
                width: 280px;
                z-index: 200;
            }
            .settings-group { margin-bottom: 15px; }
            .settings-group label { display: block; margin-bottom: 5px; color: #aaa; font-size: 13px; }
            .settings-group select, .settings-group .font-size-control {
                width: 100%;
                background: #1e1e1e;
                color: #eee;
                border: 1px solid #555;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            .font-size-control { display: flex; align-items: center; justify-content: space-between; }
            .font-size-control button { font-size: 18px; padding: 0 12px; cursor: pointer; background: #333; border: none; color: #fff; }
            
            /* Toast notification */
            #toast {
                visibility:hidden; min-width: 200px; background-color: #333; color: #fff;
                text-align: center; border-radius: 6px; padding: 12px; position: fixed;
                z-index: 100; left: 50%; top: 50%; transform: translate(-50%, -50%);
                font-size: 14px; opacity: 0; transition: opacity 0.5s, visibility 0.5s;
            }
            #toast.show { visibility: visible; opacity: 0.95; }

            /* Responsive */
            @media (min-width: 768px) {
                #sidebar { display: block; }
            }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ext-language_tools.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ext-emmet.js"></script>
    </head>
    <body>
        {% macro render_tree(nodes) %}
        <ul class="tree-list">
        {% for node in nodes %}
            <li>
                {% if node.type == 'folder' %}
                    <div class="tree-item folder {% if node.expanded %}expanded{% endif %}" onclick="toggleFolder(this)">
                        <span class="folder-arrow">◀</span>
                        <span class="icon">📁</span> 
                        <span class="label">{{ node.name }}</span>
                    </div>
                    <div class="tree-children" style="{% if not node.expanded %}display:none;{% endif %}">
                        {{ render_tree(node.children) }}
                    </div>
                {% else %}
                    <a href="{{ node.url }}" class="tree-item file {% if node.active %}active{% endif %}">
                        <span class="icon">
                        {% if node.name.endswith('.php') %}🐘
                        {% elif node.name.endswith('.py') %}🐍
                        {% elif node.name.endswith('.js') %}📜
                        {% elif node.name.endswith('.html') %}🌐
                        {% elif node.name.endswith('.css') %}🎨
                        {% elif node.name.endswith('.json') %}⚙️
                        {% elif node.name.endswith('.sh') %}💻
                        {% else %}📄{% endif %}
                        </span> 
                        <span class="label">{{ node.name }}</span>
                    </a>
                {% endif %}
            </li>
        {% endfor %}
        </ul>
        {% endmacro %}

        <header>
            <button id="sidebar-toggle" class="btn btn-icon">☰</button>
            <h3>📄 {{ filename }}</h3>
            <button id="undo-btn" class="btn" disabled>↩️ رجوع</button>
            <button id="redo-btn" class="btn" disabled>↪️ أمام</button>
            <button id="settings-btn" class="btn btn-icon">⚙️</button>
            <button id="save-btn" class="btn btn-green" disabled>💾 حفظ</button>
        </header>

        {% if warning_msg %}
        <div id="warning-banner" style="display:block">{{ warning_msg }}</div>
        {% endif %}

        <div id="main-container">
            <div id="editor"></div>
            <div id="sidebar">
                {{ render_tree(file_tree) }}
            </div>
        </div>

        <div id="settings-panel">
            <div class="settings-group">
                <label for="theme-select">الثيم (Theme)</label>
                <select id="theme-select"></select>
            </div>
            <div class="settings-group">
                <label for="font-select">نوع الخط (Font)</label>
                <select id="font-select">
                    <option value="'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace">Default</option>
                    <option value="'Fira Code', monospace">Fira Code</option>
                    <option value="'JetBrains Mono', monospace">JetBrains Mono</option>
                    <option value="'Source Code Pro', monospace">Source Code Pro</option>
                    <option value="monospace">Monospace</option>
                </select>
            </div>
            <div class="settings-group">
                <label>حجم الخط (Font Size)</label>
                <div class="font-size-control">
                    <button id="decrease-font-btn">-</button>
                    <span id="current-font-size">14px</span>
                    <button id="increase-font-btn">+</button>
                </div>
            </div>
        </div>

        <div id="editor"></div>
        <div id="toast">تم الحفظ بنجاح ✅</div>

        <script>
            var code = {{ code_content | tojson }};
            var mode = "{{ ace_mode }}";
            var userId = {{ user_id }};
            var isReadOnly = {{ 'true' if is_read_only else 'false' }};
            var isDirty = false;
            var currentFilePath = "{{ filename }}"; // Simple key for local storage

            var editor = ace.edit("editor");
            ace.require("ace/ext/language_tools");
            editor.setTheme("ace/theme/monokai");
            editor.session.setMode("ace/mode/" + mode);
            editor.session.setUseWrapMode(true);
            editor.setReadOnly(isReadOnly);
            editor.setValue(code, -1);

            // --- Auto-resize editor to fit content ---
            editor.setOptions({
                autoScrollEditorIntoView: true,
                maxLines: Infinity,
                minLines: 40 // Set a minimum height
            });

            // إعادة تعيين مدير التراجع لمنع التراجع عن تحميل الملف الأولي
            editor.session.getUndoManager().reset();
            
            // Enable VSCode-like features
            editor.setOptions({
                enableBasicAutocompletion: true,
                enableSnippets: true,
                enableLiveAutocompletion: true,
                enableEmmet: true
            });

            // --- Auto-Save Recovery ---
            if (!isReadOnly) {
                var savedDraft = localStorage.getItem("draft_" + currentFilePath);
                if (savedDraft && savedDraft !== code) {
                    if (confirm("⚠️ وجدنا نسخة غير محفوظة من عملك السابق. هل تريد استعادتها؟")) {
                        editor.setValue(savedDraft, -1);
                        isDirty = true;
                    }
                }
            }

            // --- UI Elements ---
            var undoBtn = document.getElementById("undo-btn");
            var redoBtn = document.getElementById("redo-btn");
            var saveBtn = document.getElementById("save-btn");
            var toast = document.getElementById("toast");
            var settingsBtn = document.getElementById("settings-btn");
            var settingsPanel = document.getElementById("settings-panel");
            var themeSelect = document.getElementById("theme-select");
            var fontSelect = document.getElementById("font-select");
            var decreaseFontBtn = document.getElementById("decrease-font-btn");
            var increaseFontBtn = document.getElementById("increase-font-btn");
            var currentFontSizeSpan = document.getElementById("current-font-size");
            var sidebarToggle = document.getElementById("sidebar-toggle");

            // --- Settings Logic ---
            const themes = {
                "مظلم (Dark)": [
                    "monokai", "chaos", "dracula", "gob", "gruvbox", "solarized_dark", "tomorrow_night"
                ],
                "فاتح (Light)": [
                    "chrome", "clouds", "crimson_editor", "dawn", "eclipse", "solarized_light", "sqlserver"
                ]
            };

            function populateThemes() {
                for (const group in themes) {
                    const optgroup = document.createElement('optgroup');
                    optgroup.label = group;
                    themes[group].forEach(theme => {
                        const option = document.createElement('option');
                        option.value = "ace/theme/" + theme;
                        option.textContent = theme.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                        optgroup.appendChild(option);
                    });
                    themeSelect.appendChild(optgroup);
                }
            }
            populateThemes();

            function saveSetting(key, value) {
                localStorage.setItem(`editor_${userId}_${key}`, value);
            }

            function loadSettings() {
                const getSetting = (key, defaultValue) => localStorage.getItem(`editor_${userId}_${key}`) || defaultValue;

                // Theme
                const savedTheme = getSetting("theme", "ace/theme/monokai");
                editor.setTheme(savedTheme);
                themeSelect.value = savedTheme;

                // Font Size
                const savedFontSize = parseInt(getSetting("fontSize", "14"), 10);
                editor.setFontSize(savedFontSize);
                document.documentElement.style.setProperty('--font-size', savedFontSize + 'px');
                currentFontSizeSpan.textContent = savedFontSize + 'px';

                // Font Family
                const savedFontFamily = getSetting("fontFamily", fontSelect.options[0].value);
                document.getElementById('editor').style.fontFamily = savedFontFamily;
                fontSelect.value = savedFontFamily;
            }
            
            themeSelect.onchange = () => {
                editor.setTheme(themeSelect.value);
                saveSetting("theme", themeSelect.value);
            };

            fontSelect.onchange = () => {
                const family = fontSelect.value;
                document.getElementById('editor').style.fontFamily = family;
                saveSetting("fontFamily", family);
            };

            function changeFontSize(delta) {
                let currentSize = editor.getFontSize();
                let newSize = currentSize + delta;
                if (newSize >= 8 && newSize <= 40) { // Min/max font size
                    editor.setFontSize(newSize);
                    document.documentElement.style.setProperty('--font-size', newSize + 'px');
                    currentFontSizeSpan.textContent = newSize + 'px';
                    saveSetting("fontSize", newSize);
                }
            }
            increaseFontBtn.onclick = () => changeFontSize(1);
            decreaseFontBtn.onclick = () => changeFontSize(-1);

            // --- Tree View Logic ---
            function toggleFolder(element) {
                element.classList.toggle("expanded");
                var children = element.nextElementSibling;
                if (children.style.display === "none") {
                    children.style.display = "block";
                } else {
                    children.style.display = "none";
                }
            }

            // --- Editor & Buttons Logic ---
            function updateUndoRedoState() {
                undoBtn.disabled = !editor.session.getUndoManager().hasUndo();
                redoBtn.disabled = !editor.session.getUndoManager().hasRedo();
            }

            editor.session.on('change', function() {
                isDirty = true;
                saveBtn.disabled = false;
                if (!isReadOnly) {
                    localStorage.setItem("draft_" + currentFilePath, editor.getValue());
                }
                updateUndoRedoState();
            });
            updateUndoRedoState();

            if (isReadOnly) saveBtn.disabled = true;

            undoBtn.onclick = () => {
                editor.undo();
                updateUndoRedoState();
            };
            redoBtn.onclick = () => {
                editor.redo();
                updateUndoRedoState();
            };

            sidebarToggle.onclick = () => {
                document.getElementById("sidebar").classList.toggle("open");
            };

            settingsBtn.onclick = () => {
                settingsPanel.style.display = settingsPanel.style.display === 'block' ? 'none' : 'block';
            };
            
            document.addEventListener('click', function(event) {
                if (!settingsPanel.contains(event.target) && !settingsBtn.contains(event.target)) {
                    settingsPanel.style.display = 'none';
                }
            });

            function showToast(msg) {
                toast.textContent = msg;
                toast.classList.add("show");
                setTimeout(() => toast.classList.remove("show"), 2000);
            }

            saveBtn.onclick = function() {
                if (isReadOnly) return;
                var contentToSave = editor.getValue();
                var xhr = new XMLHttpRequest();
                xhr.open("POST", window.location.pathname, true);
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
                xhr.onload = function () {
                    if (xhr.status >= 200 && xhr.status < 300) {
                        isDirty = false;
                        localStorage.removeItem("draft_" + currentFilePath); // Clear draft on success
                        saveBtn.disabled = true;
                        showToast("✅ تم الحفظ بنجاح");
                    } else {
                        showToast("❌ فشل الحفظ");
                    }
                };
                xhr.send("code=" + encodeURIComponent(contentToSave));
            };

            document.addEventListener("keydown", function(evt) {
                if ((evt.ctrlKey || evt.metaKey) && evt.key.toLowerCase() === 's') {
                    evt.preventDefault();
                    if (!saveBtn.disabled) saveBtn.click();
                }
            });
            
            // Load settings on start
            loadSettings();
        </script>
    </body>
    </html>
    """
    return render_template_string(html, filename=filename, code_content=code_content, ace_mode=ace_mode, user_id=user_id_for_settings, file_tree=file_tree, is_read_only=is_read_only, warning_msg=warning_msg)

if __name__ == "__main__":
    host = settings.web.WEBAPP_HOST
    port = settings.web.WEBAPP_PORT
    logger.info(f"🚀 Starting WebApp Server (Waitress) on http://{host}:{port}")
    try:
        serve(app, host=host, port=port, threads=8)
    except Exception as e:
        logger.critical(f"Failed to start WebApp: {e}")
        sys.exit(1)
