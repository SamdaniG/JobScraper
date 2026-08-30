from pathlib import Path
import sqlite3

LOG_DB = Path(__file__).resolve().parent / "DBs" / "logs.db"
Q_DB = Path(__file__).resolve().parent / "DBs" / "q.db"
RunSum = Path(__file__).resolve().parent / "DBs" / "summary.db"

def get_logs_connection(db=LOG_DB):
    return sqlite3.connect(db)

def get_q_connection(db=Q_DB):
    return sqlite3.connect(db)

def get_summary_connection(db=RunSum):
    return sqlite3.connect(db)

def logs_initialize(db=LOG_DB):

    with sqlite3.connect(db) as conn:
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

def q_initialize(db=Q_DB):
    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS q (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                hash_id TEXT NOT NULL,
                info TEXT,

                event TEXT NOT NULL,

                status TEXT DEFAULT 'pending',
                task TEXT NOT NULL,
                retry_count INTEGER DEFAULT 0,

                created_at TEXT NOT NULL,
                processed_at TEXT NULL,
                error TEXT DEFAULT NULL,

                uuid TEXT
            );
        """)

def summary_initialize(db=RunSum):
    with sqlite3.connect(db) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS run_summary (
                uuid TEXT PRIMARY KEY,

                executor TEXT NOT NULL,

                new INTEGER DEFAULT 0,
                filled INTEGER DEFAULT 0,
                updated INTEGER DEFAULT 0,

                started_at TEXT NOT NULL,
                finished_at TEXT NOT NULL,
                runtime REAL NOT NULL
            );
            """
        )

def q_migrate(db=Q_DB):
    with sqlite3.connect(db) as conn:

        # Check existing columns
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(q)")
        }

        # Already migrated
        if "info" in columns:
            return

        conn.execute("BEGIN")

        # Add new column
        conn.execute("""
            ALTER TABLE q
            ADD COLUMN info TEXT
        """)

        # Populate info JSON from existing columns
        conn.execute("""
            UPDATE q
            SET info = json_object(
                'job_name', job_name,
                'source', source
            )
        """)

        # Create new table
        conn.execute("""
            CREATE TABLE q_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                hash_id TEXT NOT NULL,
                info TEXT,

                event TEXT NOT NULL,

                status TEXT DEFAULT 'pending',
                task TEXT NOT NULL,
                retry_count INTEGER DEFAULT 0,

                created_at TEXT NOT NULL,
                processed_at TEXT,
                error TEXT DEFAULT NULL,

                uuid TEXT
            );
        """)

        # Copy data
        conn.execute("""
            INSERT INTO q_new (
                id,
                hash_id,
                info,
                event,
                status,
                task,
                retry_count,
                created_at,
                processed_at,
                error,
                uuid
            )
            SELECT
                id,
                hash_id,
                info,
                event,
                status,
                task,
                retry_count,
                created_at,
                processed_at,
                error,
                uuid
            FROM q;
        """)

        # Remove old table
        conn.execute("""
            DROP TABLE q;
        """)

        # Rename
        conn.execute("""
            ALTER TABLE q_new
            RENAME TO q;
        """)

        conn.commit()

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

if __name__=='__main__':
    q_migrate()