import sqlite3
from pathlib import Path

# JD_DB = Path(__file__).resolve().parent / "jd_extraction" / "jd.db"
JD_DB = Path(__file__).resolve().parent.parent / "DBs" / "jd.db"


def get_jd_connection(db=JD_DB):
    return sqlite3.connect(db)

def jd_initialize(db=JD_DB):

    with sqlite3.connect(db) as conn:

        conn.execute("PRAGMA journal_mode=WAL;")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jd (
                hash_id TEXT PRIMARY KEY,
                jd TEXT NOT NULL,
                jd_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT DEFAULT NULL,
                uuid TEXT
            );
            """
        )


if __name__=='__main__':
    # jd_initialize()
    print(JD_DB)