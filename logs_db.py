from pathlib import Path
import sqlite3

LOG_DB = Path(__file__).resolve().parent / "logs" / "logs.db"

def get_connection(db):
    return sqlite3.connect(db)

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
                scraper_count INTEGER
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
                timestamp TEXT NOT NULL
            );
        """)

