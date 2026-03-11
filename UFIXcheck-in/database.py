import aiosqlite

DB_NAME = "ufixeld.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT,
            shift_type TEXT,
            shift_start TEXT,
            shift_end TEXT,
            weekly_late INTEGER DEFAULT 0
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            checkin TEXT,
            checkout TEXT,
            late_minutes INTEGER
        )
        """)
        await db.commit()


async def add_employee(employee_id, name, shift_type, shift_start, shift_end):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?, ?, ?)",
            (employee_id, name, shift_type, shift_start, shift_end, 0)
        )
        await db.commit()