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

def get_jd(hash_id):

    with get_jd_connection() as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute(
            """
            SELECT
                hash_id,
                jd,
                created_at,
                updated_at,
                uuid
            FROM jd
            WHERE hash_id=?
            """,
            (hash_id,)
        ).fetchone()

    return dict(row) if row else None

if __name__=='__main__':
    # jd_initialize()
    print(JD_DB)