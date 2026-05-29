import aiosqlite
import time
import secrets
import os
from datetime import datetime

from .data_manager import DATA_DIR # Import the corrected DATA_DIR
from .config import settings

# --- Use the dynamic database path from central settings ---
DB_NAME = settings.DB_PATH

# --- 🔽🔽 [تعديل] المرحلة الأولى: إضافة نظام API المطورين 🔽🔽 ---

async def init_db():
    """Initializes the database and creates/updates tables."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute('PRAGMA journal_mode=WAL')
        await db.execute('PRAGMA synchronous=NORMAL')
        # --- AI & Developer API Tables ---
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                service TEXT NOT NULL,
                api_key TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'active',
                last_used_ts INTEGER,
                added_ts INTEGER NOT NULL,
                nickname TEXT
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_user_id_service ON user_api_keys (user_id, service)')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS ai_usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                key_id INTEGER,
                model_used TEXT NOT NULL,
                is_fallback BOOLEAN NOT NULL,
                status TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                FOREIGN KEY (key_id) REFERENCES user_api_keys (id) ON DELETE SET NULL
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS developer_api_keys (
                user_id INTEGER PRIMARY KEY,
                api_key TEXT NOT NULL UNIQUE,
                is_enabled BOOLEAN NOT NULL DEFAULT 1,
                created_ts INTEGER NOT NULL,
                last_used_ts INTEGER,
                total_requests INTEGER NOT NULL DEFAULT 0
            )
        ''')
        await db.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_dev_api_key ON developer_api_keys (api_key)')

        # --- Webhook Dispatcher Tables ---
        await db.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT NOT NULL,
                owner_id INTEGER NOT NULL,
                path TEXT NOT NULL,
                raw_data TEXT NOT NULL,
                created_at REAL NOT NULL,
                tries INTEGER DEFAULT 0,
                reported INTEGER DEFAULT 0
            )
        """)
        await db.execute("CREATE INDEX IF NOT EXISTS idx_queue_token ON queue (token)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_queue_owner ON queue (owner_id)")
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS webhook_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT NOT NULL,
                ts REAL NOT NULL,
                status INTEGER NOT NULL,
                response TEXT
            )
        """)
        await db.execute("CREATE INDEX IF NOT EXISTS idx_logs_token ON webhook_logs (token)")
        
        # --- 4. جدول الإحصائيات اليومية (بديل stats.json) ---
        await db.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                user_id INTEGER,
                stat_date TEXT,
                stat_name TEXT,
                count INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, stat_date, stat_name)
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats (stat_date)')

        # --- Marketplace Tables ---
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_products (
                product_id TEXT PRIMARY KEY,
                owner_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                tags TEXT,
                version TEXT DEFAULT '1.0.0',
                price REAL DEFAULT 0,
                currency TEXT DEFAULT 'USD',
                is_free BOOLEAN DEFAULT 1,
                status TEXT DEFAULT 'active',
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL,
                downloads INTEGER DEFAULT 0,
                views INTEGER DEFAULT 0,
                file_count INTEGER DEFAULT 0,
                total_size INTEGER DEFAULT 0,
                preview_image TEXT,
                demo_url TEXT,
                support_url TEXT,
                changelog TEXT
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_mp_owner ON marketplace_products (owner_id)')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_mp_category ON marketplace_products (category)')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_mp_status ON marketplace_products (status)')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_mp_created ON marketplace_products (created_at DESC)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                created_at INTEGER NOT NULL,
                updated_at INTEGER,
                FOREIGN KEY(product_id) REFERENCES marketplace_products(product_id) ON DELETE CASCADE,
                UNIQUE(product_id, user_id)
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_review_product ON marketplace_reviews (product_id)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_comments (
                comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                comment TEXT NOT NULL,
                parent_id INTEGER,
                created_at INTEGER NOT NULL,
                updated_at INTEGER,
                is_deleted BOOLEAN DEFAULT 0,
                is_developer_hearted BOOLEAN DEFAULT 0,
                FOREIGN KEY(product_id) REFERENCES marketplace_products(product_id) ON DELETE CASCADE,
                FOREIGN KEY(parent_id) REFERENCES marketplace_comments(comment_id) ON DELETE CASCADE
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_comment_product ON marketplace_comments (product_id)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_comment_reactions (
                reaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                reaction INTEGER NOT NULL,
                created_at INTEGER NOT NULL,
                FOREIGN KEY(comment_id) REFERENCES marketplace_comments(comment_id) ON DELETE CASCADE,
                UNIQUE(comment_id, user_id)
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_comment_react ON marketplace_comment_reactions (comment_id)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                downloaded_at INTEGER NOT NULL,
                version TEXT,
                FOREIGN KEY(product_id) REFERENCES marketplace_products(product_id) ON DELETE CASCADE
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_download_product ON marketplace_downloads (product_id)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_categories (
                category_id TEXT PRIMARY KEY,
                name_ar TEXT NOT NULL,
                name_en TEXT NOT NULL,
                icon TEXT,
                description TEXT,
                product_count INTEGER DEFAULT 0,
                display_order INTEGER DEFAULT 0
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                last_viewed_at INTEGER NOT NULL,
                UNIQUE(product_id, user_id),
                FOREIGN KEY(product_id) REFERENCES marketplace_products(product_id) ON DELETE CASCADE
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_view_product ON marketplace_views (product_id)')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_view_user ON marketplace_views (user_id)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_bans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                ban_type TEXT NOT NULL,
                banned_until INTEGER NOT NULL,
                reason TEXT,
                created_at INTEGER NOT NULL
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_ban_user ON marketplace_bans (user_id)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_warnings (
                user_id INTEGER PRIMARY KEY,
                warning_count INTEGER DEFAULT 0,
                last_warning_at INTEGER NOT NULL
            )
        ''')
        
        # --- Top Developers Tables ---
        await db.execute('''
            CREATE TABLE IF NOT EXISTS top_developers (
                user_id INTEGER PRIMARY KEY,
                rank INTEGER NOT NULL,
                downloads INTEGER NOT NULL,
                products INTEGER NOT NULL,
                rating_percentage REAL,
                granted_at INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                last_checked INTEGER NOT NULL
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_top_dev_rank ON top_developers (rank, is_active)')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_top_dev_active ON top_developers (is_active, last_checked)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS top_developers_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                rank INTEGER NOT NULL,
                downloads INTEGER NOT NULL,
                products INTEGER NOT NULL,
                rating_percentage REAL,
                recorded_at INTEGER NOT NULL,
                event_type TEXT NOT NULL
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_history_user ON top_developers_history (user_id, recorded_at)')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_history_event ON top_developers_history (event_type, recorded_at)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER NOT NULL,
                action_type TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                reason TEXT,
                metadata TEXT,
                created_at INTEGER NOT NULL
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_admin_log_admin ON marketplace_admin_logs (admin_id)')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_admin_log_created ON marketplace_admin_logs (created_at)')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_featured (
                product_id TEXT PRIMARY KEY,
                featured_at INTEGER NOT NULL,
                featured_by INTEGER NOT NULL,
                priority INTEGER DEFAULT 0,
                FOREIGN KEY(product_id) REFERENCES marketplace_products(product_id) ON DELETE CASCADE
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS marketplace_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reporter_id INTEGER NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                reviewed_by INTEGER,
                reviewed_at INTEGER,
                admin_notes TEXT,
                created_at INTEGER NOT NULL
            )
        ''')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_report_status ON marketplace_reports (status)')
        await db.execute('CREATE INDEX IF NOT EXISTS idx_report_created ON marketplace_reports (created_at)')

        # --- Migrations ---
        # Add is_developer_hearted to marketplace_comments if it doesn't exist
        try:
            await db.execute("ALTER TABLE marketplace_comments ADD COLUMN is_developer_hearted BOOLEAN DEFAULT 0")
        except aiosqlite.OperationalError:
            pass # Column already exists

        await db.commit()
    print("✅ Database initialized successfully (Advanced Storage + Stats + Marketplace Ready).")

# --- دوال مفاتيح المطورين (Developer API Keys) ---

def _generate_api_key():
    """Generates a secure, unique API key."""
    return "prod_" + secrets.token_urlsafe(32)

async def get_or_create_dev_api_key(user_id: int):
    """
    Fetches the current developer API key for a user.
    If it doesn't exist, it creates one.
    Returns the full API key string.
    """
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT api_key FROM developer_api_keys WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row['api_key']
        
        # If not found, create a new one
        new_key = _generate_api_key()
        now = int(time.time())
        await db.execute(
            "INSERT INTO developer_api_keys (user_id, api_key, created_ts) VALUES (?, ?, ?)",
            (user_id, new_key, now)
        )
        await db.commit()
        return new_key

async def regenerate_dev_api_key(user_id: int):
    """Generates a new key for the user, replacing the old one."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        new_key = _generate_api_key()
        now = int(time.time())
        await db.execute(
            """
            INSERT OR REPLACE INTO developer_api_keys 
            (user_id, api_key, is_enabled, created_ts, last_used_ts, total_requests)
            VALUES (?, ?, 1, ?, (SELECT last_used_ts FROM developer_api_keys WHERE user_id = ?), (SELECT total_requests FROM developer_api_keys WHERE user_id = ?))
            """,
            (user_id, new_key, now, user_id, user_id)
        )
        await db.commit()
        return new_key

async def get_user_by_dev_api_key(api_key: str):
    """
    Authenticates an API key and returns the user's details.
    This is the core authentication function for the API server.
    Returns a dictionary with user info or None if not found/invalid.
    """
    if not api_key or not api_key.startswith("prod_"):
        return None
        
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM developer_api_keys WHERE api_key = ?", (api_key,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def log_api_request(api_key: str):
    """Logs a successful API request, updating stats."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute(
            "UPDATE developer_api_keys SET last_used_ts = ?, total_requests = total_requests + 1 WHERE api_key = ?",
            (int(time.time()), api_key)
        )
        await db.commit()

async def get_dev_api_stats(user_id: int):
    """Fetches usage statistics for a user's developer API key."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT last_used_ts, total_requests, is_enabled, api_key FROM developer_api_keys WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
            
async def toggle_dev_api_key(user_id: int, is_enabled: bool):
    """Enables or disables a user's developer API key."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        cursor = await db.execute(
            "UPDATE developer_api_keys SET is_enabled = ? WHERE user_id = ?",
            (is_enabled, user_id)
        )
        await db.commit()
        return cursor.rowcount > 0

# --- 🔼🔼 [نهاية التعديل] 🔼🔼 ---


# --- دوال مفاتيح AI (موجودة سابقاً) ---

async def add_user_key(user_id, service, api_key, nickname):
    """Adds a new AI API key for a user and returns its ID."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        cursor = await db.execute(
            "INSERT INTO user_api_keys (user_id, service, api_key, nickname, added_ts) VALUES (?, ?, ?, ?, ?)",
            (user_id, service, api_key, nickname, int(time.time()))
        )
        await db.commit()
        return cursor.lastrowid

async def get_user_keys(user_id):
    """Fetches all AI API keys for a given user."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM user_api_keys WHERE user_id = ? ORDER BY service, nickname", (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def delete_user_key(key_id, user_id):
    """Deletes a specific AI key if it belongs to the user."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        cursor = await db.execute(
            "DELETE FROM user_api_keys WHERE id = ? AND user_id = ?",
            (key_id, user_id)
        )
        await db.commit()
        return cursor.rowcount > 0

async def get_active_key_for_user(user_id, service):
    """Gets the best available active AI key for a user and a specific service."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM user_api_keys WHERE user_id = ? AND service = ? AND status = 'active' ORDER BY last_used_ts ASC LIMIT 1",
            (user_id, service)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                await db.execute("UPDATE user_api_keys SET last_used_ts = ? WHERE id = ?", (int(time.time()), row['id']))
                await db.commit()
                return dict(row)
    return None

async def set_key_status(key_id, status):
    """Updates the status of an AI API key (e.g., to 'exhausted' or 'invalid')."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("UPDATE user_api_keys SET status = ? WHERE id = ?", (status, key_id))
        await db.commit()

async def log_ai_usage(user_id, model_used, status, key_id=None, is_fallback=False):
    """Logs an AI model usage event."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute(
            "INSERT INTO ai_usage_logs (user_id, key_id, model_used, is_fallback, status, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, key_id, model_used, is_fallback, status, int(time.time()))
        )
        await db.commit()

async def get_ai_usage_count_for_user(user_id, is_fallback=None, from_ts=0):
    """Counts AI usage for a user since a specific timestamp."""
    query = "SELECT COUNT(*) FROM ai_usage_logs WHERE user_id = ? AND timestamp >= ?"
    params = [user_id, from_ts]
    
    if is_fallback is not None:
        query += " AND is_fallback = ?"
        params.append(is_fallback)
        
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute(query, tuple(params)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def get_general_ai_stats():
    """Fetches general AI statistics from the database."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute("SELECT COUNT(*) FROM user_api_keys") as cursor:
            total_keys = (await cursor.fetchone())[0]

        async with db.execute("SELECT status, COUNT(*) FROM ai_usage_logs GROUP BY status") as cursor:
            calls_by_status = {status: count for status, count in await cursor.fetchall()}

        today_start_ts = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        async with db.execute("SELECT COUNT(*) FROM ai_usage_logs WHERE timestamp >= ?", (today_start_ts,)) as cursor:
            calls_today = (await cursor.fetchone())[0]

    return {
        "total_user_keys": total_keys,
        "successful_calls": calls_by_status.get('success', 0),
        "failed_calls": calls_by_status.get('failure', 0),
        "calls_today": calls_today
    }


# --- Webhook Queue Functions ---

async def add_update_to_queue(token: str, owner_id: int, path: str, raw_data: str) -> int:
    """Adds a received update to the processing queue."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        cursor = await db.execute(
            "INSERT INTO queue (token, owner_id, path, raw_data, created_at, tries) VALUES (?, ?, ?, ?, ?, 0)",
            (token, owner_id, path, raw_data, time.time())
        )
        await db.commit()
        return cursor.lastrowid

async def delete_update_from_queue(row_id: int):
    """Deletes an update from the queue, typically after successful processing."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("DELETE FROM queue WHERE id = ?", (row_id,))
        await db.commit()

async def increment_queue_tries(row_id: int):
    """Increments the try counter for a queued update, typically after a failed delivery attempt."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("UPDATE queue SET tries = tries + 1 WHERE id = ?", (row_id,))
        await db.commit()

async def log_webhook_request(token: str, status: int, response: str):
    """Logs the result of a webhook forwarding attempt and cleans up old logs."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        # Insert the new log entry
        await db.execute(
            "INSERT INTO webhook_logs (token, ts, status, response) VALUES (?, ?, ?, ?)",
            (token, time.time(), status, response)
        )
        # Keep only the most recent 20 logs for this token
        await db.execute("""
            DELETE FROM webhook_logs WHERE id NOT IN (
                SELECT id FROM webhook_logs WHERE token = ? ORDER BY id DESC LIMIT 20
            ) AND token = ?
        """, (token, token))
        await db.commit()


# --- دوال الإحصائيات الجديدة (Stats Functions) ---

async def increment_stat(user_id: int, stat_name: str, amount: int = 1):
    """زيادة عداد إحصائية معينة للمستخدم لليوم الحالي"""
    today = datetime.now().strftime('%Y-%m-%d')
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("""
            INSERT INTO daily_stats (user_id, stat_date, stat_name, count)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, stat_date, stat_name) DO UPDATE SET count = count + ?
        """, (user_id, today, stat_name, amount, amount))
        await db.commit()

async def count_events(stat_name: str, user_id: int, start_ts: int, end_ts: int) -> int:
    """حساب مجموع الأحداث في فترة زمنية معينة"""
    start_date = datetime.fromtimestamp(start_ts).strftime('%Y-%m-%d')
    end_date = datetime.fromtimestamp(end_ts).strftime('%Y-%m-%d')
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute("""
            SELECT SUM(count) FROM daily_stats 
            WHERE user_id = ? AND stat_name = ? AND stat_date >= ? AND stat_date <= ?
        """, (user_id, stat_name, start_date, end_date)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result and result[0] else 0

async def get_total_stat(user_id: int, stat_name: str) -> int:
    """الحصول على الإجمالي الكلي لإحصائية معينة"""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute("SELECT SUM(count) FROM daily_stats WHERE user_id = ? AND stat_name = ?", (user_id, stat_name)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result and result[0] else 0

async def get_user_stat_names(user_id: int) -> list:
    """الحصول على قائمة أسماء الإحصائيات المسجلة للمستخدم"""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute("SELECT DISTINCT stat_name FROM daily_stats WHERE user_id = ?", (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def get_global_total_stat(stat_name: str) -> int:
    """الحصول على الإجمالي الكلي لإحصائية معينة لجميع المستخدمين"""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute("SELECT SUM(count) FROM daily_stats WHERE stat_name = ?", (stat_name,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result and result[0] else 0

async def count_global_events(stat_name: str, start_ts: int, end_ts: int) -> int:
    """حساب مجموع الأحداث لجميع المستخدمين في فترة زمنية معينة"""
    start_date = datetime.fromtimestamp(start_ts).strftime('%Y-%m-%d')
    end_date = datetime.fromtimestamp(end_ts).strftime('%Y-%m-%d')
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute("""
            SELECT SUM(count) FROM daily_stats 
            WHERE stat_name = ? AND stat_date >= ? AND stat_date <= ?
        """, (stat_name, start_date, end_date)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result and result[0] else 0


# ===== Marketplace Functions =====

# --- Products ---
async def create_marketplace_product(product_data: dict) -> str:
    """Creates a new marketplace product and triggers top developers check."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("""
            INSERT INTO marketplace_products 
            (product_id, owner_id, title, description, category, tags, version, 
             price, currency, is_free, status, created_at, updated_at, file_count, total_size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product_data['product_id'], product_data['owner_id'], product_data['title'],
            product_data['description'], product_data['category'], product_data.get('tags'),
            product_data.get('version', '1.0.0'), product_data.get('price', 0),
            product_data.get('currency', 'USD'), product_data.get('is_free', True),
            product_data.get('status', 'active'), product_data['created_at'],
            product_data['updated_at'], product_data.get('file_count', 0),
            product_data.get('total_size', 0)
        ))
        await db.commit()
    
    # Trigger top developers check
    try:
        from bot.tasks.top_developers_checker import trigger_top_developers_check
        import asyncio
        asyncio.create_task(trigger_top_developers_check())
    except Exception as e:
        print(f"[TopDev] Failed to trigger check: {e}")
    
    return product_data['product_id']

async def get_marketplace_product(product_id: str) -> dict:
    """Gets a marketplace product by ID."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM marketplace_products WHERE product_id = ?", (product_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def update_marketplace_product(product_id: str, updates: dict):
    """Updates a marketplace product."""
    updates['updated_at'] = int(time.time())
    set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [product_id]
    
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute(f"UPDATE marketplace_products SET {set_clause} WHERE product_id = ?", values)
        await db.commit()

async def delete_marketplace_product(product_id: str):
    """Deletes a marketplace product."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("DELETE FROM marketplace_products WHERE product_id = ?", (product_id,))
        await db.commit()

async def search_marketplace_products(category=None, search_term=None, sort_by='created_at', limit=20, offset=0, status='active'):
    """Searches marketplace products with enhanced ranking algorithms."""
    from bot.services.ranking_engine import build_search_query, normalize_sort_mode
    
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        
        # Normalize sort mode
        mode = normalize_sort_mode(sort_by)
        
        # Build query
        query, params = build_search_query(
            mode=mode,
            category=category,
            search_term=search_term,
            status=status
        )
        
        # Add pagination
        params.extend([limit, offset])
        
        async with db.execute(query, tuple(params)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_user_products(user_id: int, status=None):
    """Gets all products by a user."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        if status:
            query = "SELECT * FROM marketplace_products WHERE owner_id = ? AND status = ? ORDER BY created_at DESC"
            params = (user_id, status)
        else:
            query = "SELECT * FROM marketplace_products WHERE owner_id = ? ORDER BY created_at DESC"
            params = (user_id,)
        
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def count_marketplace_products(category=None, search_term=None, status='active'):
    """Counts total products matching filters."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        query = "SELECT COUNT(*) FROM marketplace_products WHERE status = ?"
        params = [status]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if search_term:
            query += " AND (title LIKE ? OR description LIKE ? OR tags LIKE ?)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        
        async with db.execute(query, tuple(params)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def increment_product_views(product_id: str, user_id: int):
    """Increments product view count with 10-hour cooldown per user."""
    import time
    
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        current_time = int(time.time())
        ten_hours_ago = current_time - (10 * 60 * 60)
        
        # Check last view
        async with db.execute(
            "SELECT last_viewed_at FROM marketplace_views WHERE product_id = ? AND user_id = ?",
            (product_id, user_id)
        ) as cursor:
            row = await cursor.fetchone()
        
        if row:
            last_viewed = row[0]
            if last_viewed > ten_hours_ago:
                # Less than 10 hours, don't count
                return False
            else:
                # More than 10 hours, update and count
                await db.execute(
                    "UPDATE marketplace_views SET last_viewed_at = ? WHERE product_id = ? AND user_id = ?",
                    (current_time, product_id, user_id)
                )
        else:
            # First view, insert
            await db.execute(
                "INSERT INTO marketplace_views (product_id, user_id, last_viewed_at) VALUES (?, ?, ?)",
                (product_id, user_id, current_time)
            )
        
        # Increment view count
        await db.execute("UPDATE marketplace_products SET views = views + 1 WHERE product_id = ?", (product_id,))
        await db.commit()
        return True

async def increment_product_downloads(product_id: str):
    """Increments product download count and triggers top developers check."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("UPDATE marketplace_products SET downloads = downloads + 1 WHERE product_id = ?", (product_id,))
        await db.commit()
    
    # Trigger top developers check
    try:
        from bot.tasks.top_developers_checker import trigger_top_developers_check
        import asyncio
        asyncio.create_task(trigger_top_developers_check())
    except Exception as e:
        print(f"[TopDev] Failed to trigger check: {e}")

# --- Reviews ---
async def add_product_review(product_id: str, user_id: int, rating: int, comment: str = None):
    """Adds or updates a product review and triggers top developers check."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        now = int(time.time())
        await db.execute("""
            INSERT INTO marketplace_reviews (product_id, user_id, rating, comment, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(product_id, user_id) DO UPDATE SET
                rating = excluded.rating,
                comment = excluded.comment,
                updated_at = ?
        """, (product_id, user_id, rating, comment, now, now))
        await db.commit()
    
    # Trigger top developers check
    try:
        from bot.tasks.top_developers_checker import trigger_top_developers_check
        import asyncio
        asyncio.create_task(trigger_top_developers_check())
    except Exception as e:
        print(f"[TopDev] Failed to trigger check: {e}")

async def get_product_reviews(product_id: str, limit=50):
    """Gets all reviews for a product."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM marketplace_reviews WHERE product_id = ? ORDER BY created_at DESC LIMIT ?",
            (product_id, limit)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_user_review(product_id: str, user_id: int):
    """Gets a user's review for a product."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM marketplace_reviews WHERE product_id = ? AND user_id = ?",
            (product_id, user_id)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def delete_product_review(product_id: str, user_id: int):
    """Deletes a user's review."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("DELETE FROM marketplace_reviews WHERE product_id = ? AND user_id = ?", (product_id, user_id))
        await db.commit()

async def get_product_rating_stats(product_id: str):
    """Gets rating statistics for a product."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN rating = 2 THEN 1 ELSE 0 END) as likes,
                SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as dislikes
            FROM marketplace_reviews WHERE product_id = ?
        """, (product_id,)) as cursor:
            row = await cursor.fetchone()
            total = row[0] or 0
            likes = row[1] or 0
            dislikes = row[2] or 0
            rating = (likes / total * 5.0) if total > 0 else 0.0
            return {
                'total': total,
                'likes': likes,
                'dislikes': dislikes,
                'rating': round(rating, 1)
            }

# --- Comments ---
async def add_product_comment(product_id: str, user_id: int, comment: str, parent_id: int = None):
    """Adds a comment to a product."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        now = int(time.time())
        cursor = await db.execute("""
            INSERT INTO marketplace_comments (product_id, user_id, comment, parent_id, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, user_id, comment, parent_id, now))
        await db.commit()
        return cursor.lastrowid

async def get_product_comments(product_id: str, limit=50):
    """Gets all comments for a product."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT * FROM marketplace_comments 
            WHERE product_id = ? AND is_deleted = 0 
            ORDER BY created_at DESC LIMIT ?
        """, (product_id, limit)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def delete_product_comment(comment_id: int):
    """Soft deletes a comment."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute("UPDATE marketplace_comments SET is_deleted = 1 WHERE comment_id = ?", (comment_id,))
        await db.commit()

async def count_product_comments(product_id: str):
    """Counts comments for a product."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM marketplace_comments WHERE product_id = ? AND is_deleted = 0",
            (product_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

# --- Downloads ---
async def log_product_download(product_id: str, user_id: int, version: str):
    """Logs a product download."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        now = int(time.time())
        await db.execute("""
            INSERT INTO marketplace_downloads (product_id, user_id, downloaded_at, version)
            VALUES (?, ?, ?, ?)
        """, (product_id, user_id, now, version))
        await db.commit()

async def check_user_downloaded(user_id: int, product_id: str) -> bool:
    """Checks if user has downloaded a product."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute("""
            SELECT COUNT(*) FROM marketplace_downloads 
            WHERE user_id = ? AND product_id = ?
        """, (user_id, product_id)) as cursor:
            result = await cursor.fetchone()
            return result[0] > 0

async def get_user_download_count(user_id: int, product_id: str) -> int:
    """Get how many times user downloaded a product."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute("""
            SELECT COUNT(*) FROM marketplace_downloads 
            WHERE user_id = ? AND product_id = ?
        """, (user_id, product_id)) as cursor:
            result = await cursor.fetchone()
            return result[0]

async def get_user_downloads(user_id: int, limit=50):
    """Gets user's download history."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT d.*, p.title, p.category 
            FROM marketplace_downloads d
            JOIN marketplace_products p ON d.product_id = p.product_id
            WHERE d.user_id = ?
            ORDER BY d.downloaded_at DESC LIMIT ?
        """, (user_id, limit)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

# --- Categories ---
async def get_marketplace_categories():
    """Gets all marketplace categories."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM marketplace_categories ORDER BY display_order") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_marketplace_category(category_id: str):
    """Gets a specific category."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM marketplace_categories WHERE category_id = ?", (category_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def update_category_product_count(category_id: str):
    """Updates product count for a category."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM marketplace_products WHERE category = ? AND status = 'active'",
            (category_id,)
        ) as cursor:
            count = (await cursor.fetchone())[0]
        
        await db.execute("UPDATE marketplace_categories SET product_count = ? WHERE category_id = ?", (count, category_id))
        await db.commit()

async def init_marketplace_categories():
    """Initializes default categories."""
    categories = [
        ('general', 'بوتات عامة', 'General Bots', '🤖', 'بوتات متنوعة للاستخدام العام', 0),
        ('store', 'بوتات متاجر', 'Store Bots', '🛍️', 'بوتات لإدارة المتاجر والمبيعات', 1),
        ('stats', 'إحصائيات', 'Statistics', '📊', 'بوتات للإحصائيات والتحليلات', 2),
        ('games', 'ألعاب', 'Games', '🎮', 'بوتات ألعاب تفاعلية', 3),
        ('tools', 'أدوات', 'Tools', '🔧', 'أدوات مساعدة ومفيدة', 4),
        ('chat', 'دردشة', 'Chat', '💬', 'بوتات للدردشة والتواصل', 5),
        ('news', 'أخبار', 'News', '📰', 'بوتات الأخبار والتحديثات', 6),
        ('education', 'تعليمية', 'Educational', '🎓', 'بوتات تعليمية', 7),
    ]
    
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        for cat in categories:
            await db.execute("""
                INSERT OR IGNORE INTO marketplace_categories 
                (category_id, name_ar, name_en, icon, description, display_order)
                VALUES (?, ?, ?, ?, ?, ?)
            """, cat)
        await db.commit()

# --- Stats ---
async def get_marketplace_stats():
    """Gets general marketplace statistics."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        stats = {}
        
        # Total products
        async with db.execute("SELECT COUNT(*) FROM marketplace_products WHERE status = 'active'") as cursor:
            stats['total_products'] = (await cursor.fetchone())[0]
        
        # Total downloads
        async with db.execute("SELECT SUM(downloads) FROM marketplace_products WHERE status = 'active'") as cursor:
            stats['total_downloads'] = (await cursor.fetchone())[0] or 0
        
        # Total developers
        async with db.execute("SELECT COUNT(DISTINCT owner_id) FROM marketplace_products WHERE status = 'active'") as cursor:
            stats['total_developers'] = (await cursor.fetchone())[0]
        
        return stats
