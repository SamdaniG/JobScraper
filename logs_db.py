from pathlib import Path
import sqlite3

LOG_DB = Path(__file__).resolve().parent / "logs" / "logs.db"

def get_logs_connection(db=LOG_DB):
    return sqlite3.connect(db)

def migrate():
    with sqlite3.connect(LOG_DB) as conn:

        # timers
        columns = [
            row[1] for row in conn.execute(
                "PRAGMA table_info(timers)"
            )
        ]

        if "uuid" not in columns and "run_uuid" in columns:
            conn.execute(
                "ALTER TABLE timers RENAME COLUMN run_uuid TO uuid"
            )


        # history
        columns = [
            row[1] for row in conn.execute(
                "PRAGMA table_info(history)"
            )
        ]

        if "uuid" not in columns and "run_uuid" in columns:
            conn.execute(
                "ALTER TABLE history RENAME COLUMN run_uuid TO uuid"
            )

def initialize():

    with sqlite3.connect(LOG_DB) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS timers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
    
                timestamp TEXT NOT NULL,
                source TEXT,
                job_board TEXT,
                executor TEXT,
    
                time_taken REAL,
                scraper_count INTEGER,
                uuid TEXT
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                
                hash_id TEXT NOT NULL,
                job_name TEXT NOT NULL,
                source TEXT NOT NULL,
                
                event TEXT NOT NULL,
                field TEXT DEFAULT NULL,
                old_val TEXT DEFAULT NULL,
                new_val TEXT DEFAULT NULL,
                timestamp TEXT NOT NULL,
                uuid TEXT
            );
        """)

    migrate()

