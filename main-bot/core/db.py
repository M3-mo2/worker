import logging
from config import DATABASE_URL

pool = None
db_type = "sqlite"


def _row_to_dict(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


async def init():
    global pool, db_type

    if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
        db_type = "postgres"
        import asyncpg
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS workers (
                    id SERIAL PRIMARY KEY,
                    url TEXT NOT NULL UNIQUE,
                    secret TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    bots_count INTEGER DEFAULT 0,
                    last_health_check TIMESTAMP,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS bots (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    worker_id INTEGER REFERENCES workers(id),
                    bot_token TEXT NOT NULL,
                    bot_username TEXT,
                    status TEXT DEFAULT 'running',
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_bots_user ON bots(user_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_bots_status ON bots(user_id, status)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_bots_worker ON bots(worker_id)")
        logging.info("PostgreSQL connected")
    else:
        db_type = "sqlite"
        import aiosqlite
        import os
        os.makedirs("data", exist_ok=True)
        pool = await aiosqlite.connect("data/hosting.db")
        await pool.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE,
                secret TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                bots_count INTEGER DEFAULT 0,
                last_health_check TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await pool.execute("""
            CREATE TABLE IF NOT EXISTS bots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                worker_id INTEGER REFERENCES workers(id),
                bot_token TEXT NOT NULL,
                bot_username TEXT,
                status TEXT DEFAULT 'running',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await pool.execute("CREATE INDEX IF NOT EXISTS idx_bots_user ON bots(user_id)")
        await pool.execute("CREATE INDEX IF NOT EXISTS idx_bots_status ON bots(user_id, status)")
        await pool.execute("CREATE INDEX IF NOT EXISTS idx_bots_worker ON bots(worker_id)")
        await pool.commit()
        logging.info("SQLite connected (local dev)")


async def close():
    global pool
    if pool:
        await pool.close()
        pool = None
        logging.info("Database closed")


# ==================== Workers ====================

async def add_worker(url: str, secret: str) -> int:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO workers (url, secret) VALUES ($1, $2) RETURNING id",
                url, secret
            )
            return row["id"]
    else:
        cursor = await pool.execute(
            "INSERT INTO workers (url, secret) VALUES (?, ?)",
            (url, secret)
        )
        await pool.commit()
        return cursor.lastrowid


async def get_all_workers() -> list[dict]:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM workers ORDER BY bots_count ASC")
            return [dict(r) for r in rows]
    else:
        pool.row_factory = _row_to_dict
        cursor = await pool.execute("SELECT * FROM workers ORDER BY bots_count ASC")
        rows = await cursor.fetchall()
        pool.row_factory = None
        return rows


async def get_active_workers() -> list[dict]:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM workers WHERE status = 'active' ORDER BY bots_count ASC"
            )
            return [dict(r) for r in rows]
    else:
        pool.row_factory = _row_to_dict
        cursor = await pool.execute(
            "SELECT * FROM workers WHERE status = 'active' ORDER BY bots_count ASC"
        )
        rows = await cursor.fetchall()
        pool.row_factory = None
        return rows


async def get_worker_by_id(worker_id: int) -> dict | None:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM workers WHERE id = $1", worker_id)
            return dict(row) if row else None
    else:
        pool.row_factory = _row_to_dict
        cursor = await pool.execute("SELECT * FROM workers WHERE id = ?", (worker_id,))
        row = await cursor.fetchone()
        pool.row_factory = None
        return row


async def get_worker_by_url(url: str) -> dict | None:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM workers WHERE url = $1", url)
            return dict(row) if row else None
    else:
        pool.row_factory = _row_to_dict
        cursor = await pool.execute("SELECT * FROM workers WHERE url = ?", (url,))
        row = await cursor.fetchone()
        pool.row_factory = None
        return row


async def update_worker_status(worker_id: int, status: str):
    if db_type == "postgres":
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE workers SET status = $1 WHERE id = $2",
                status, worker_id
            )
    else:
        await pool.execute(
            "UPDATE workers SET status = ? WHERE id = ?",
            (status, worker_id)
        )
        await pool.commit()


async def update_worker_health(worker_id: int):
    from datetime import datetime
    if db_type == "postgres":
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE workers SET last_health_check = NOW() WHERE id = $1",
                worker_id
            )
    else:
        await pool.execute(
            "UPDATE workers SET last_health_check = CURRENT_TIMESTAMP WHERE id = ?",
            (worker_id,)
        )
        await pool.commit()


async def increment_worker_bots(worker_id: int):
    if db_type == "postgres":
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE workers SET bots_count = bots_count + 1 WHERE id = $1",
                worker_id
            )
    else:
        await pool.execute(
            "UPDATE workers SET bots_count = bots_count + 1 WHERE id = ?",
            (worker_id,)
        )
        await pool.commit()


async def decrement_worker_bots(worker_id: int):
    if db_type == "postgres":
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE workers SET bots_count = GREATEST(bots_count - 1, 0) WHERE id = $1",
                worker_id
            )
    else:
        await pool.execute(
            "UPDATE workers SET bots_count = MAX(bots_count - 1, 0) WHERE id = ?",
            (worker_id,)
        )
        await pool.commit()


async def delete_worker(worker_id: int):
    if db_type == "postgres":
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM workers WHERE id = $1", worker_id)
    else:
        await pool.execute("DELETE FROM workers WHERE id = ?", (worker_id,))
        await pool.commit()


async def count_workers() -> int:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT COUNT(*) as cnt FROM workers")
            return row["cnt"]
    else:
        cursor = await pool.execute("SELECT COUNT(*) FROM workers")
        row = await cursor.fetchone()
        return row[0]


# ==================== Bots ====================

async def add_bot(user_id: int, bot_token: str, bot_username: str = None, worker_id: int = None) -> int:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO bots (user_id, worker_id, bot_token, bot_username) VALUES ($1, $2, $3, $4) RETURNING id",
                user_id, worker_id, bot_token, bot_username
            )
            return row["id"]
    else:
        cursor = await pool.execute(
            "INSERT INTO bots (user_id, worker_id, bot_token, bot_username) VALUES (?, ?, ?, ?)",
            (user_id, worker_id, bot_token, bot_username)
        )
        await pool.commit()
        return cursor.lastrowid


async def get_user_bots(user_id: int) -> list[dict]:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM bots WHERE user_id = $1 ORDER BY created_at DESC",
                user_id
            )
            return [dict(r) for r in rows]
    else:
        pool.row_factory = _row_to_dict
        cursor = await pool.execute(
            "SELECT * FROM bots WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        rows = await cursor.fetchall()
        pool.row_factory = None
        return rows


async def get_bot_by_id(bot_id: int) -> dict | None:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM bots WHERE id = $1", bot_id)
            return dict(row) if row else None
    else:
        pool.row_factory = _row_to_dict
        cursor = await pool.execute("SELECT * FROM bots WHERE id = ?", (bot_id,))
        row = await cursor.fetchone()
        pool.row_factory = None
        return row


async def get_active_bot(user_id: int) -> dict | None:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM bots WHERE user_id = $1 AND status = 'running' ORDER BY created_at DESC LIMIT 1",
                user_id
            )
            return dict(row) if row else None
    else:
        pool.row_factory = _row_to_dict
        cursor = await pool.execute(
            "SELECT * FROM bots WHERE user_id = ? AND status = 'running' ORDER BY created_at DESC LIMIT 1",
            (user_id,)
        )
        row = await cursor.fetchone()
        pool.row_factory = None
        return row


async def update_status(bot_id: int, status: str):
    if db_type == "postgres":
        async with pool.acquire() as conn:
            await conn.execute("UPDATE bots SET status = $1 WHERE id = $2", status, bot_id)
    else:
        await pool.execute("UPDATE bots SET status = ? WHERE id = ?", (status, bot_id))
        await pool.commit()


async def update_bot_username(bot_id: int, bot_username: str):
    if db_type == "postgres":
        async with pool.acquire() as conn:
            await conn.execute("UPDATE bots SET bot_username = $1 WHERE id = $2", bot_username, bot_id)
    else:
        await pool.execute("UPDATE bots SET bot_username = ? WHERE id = ?", (bot_username, bot_id))
        await pool.commit()


async def delete_bot(bot_id: int):
    bot = await get_bot_by_id(bot_id)
    if bot and bot.get("worker_id"):
        await decrement_worker_bots(bot["worker_id"])
    if db_type == "postgres":
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM bots WHERE id = $1", bot_id)
    else:
        await pool.execute("DELETE FROM bots WHERE id = ?", (bot_id,))
        await pool.commit()


async def count_user_bots(user_id: int) -> int:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT COUNT(*) as cnt FROM bots WHERE user_id = $1", user_id)
            return row["cnt"]
    else:
        cursor = await pool.execute("SELECT COUNT(*) FROM bots WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return row[0]


async def get_bots_by_worker(worker_id: int) -> list[dict]:
    if db_type == "postgres":
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM bots WHERE worker_id = $1 AND status = 'running'",
                worker_id
            )
            return [dict(r) for r in rows]
    else:
        pool.row_factory = _row_to_dict
        cursor = await pool.execute(
            "SELECT * FROM bots WHERE worker_id = ? AND status = 'running'",
            (worker_id,)
        )
        rows = await cursor.fetchall()
        pool.row_factory = None
        return rows
