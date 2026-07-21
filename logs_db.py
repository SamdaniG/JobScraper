from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "logs" / "logs.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize():
    with sqlite3.connect(DB_PATH) as conn:
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
