# storage.py
import json
from json import JSONDecodeError
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_JSON_PATH = BASE_DIR / "db.json"


DATE_FMT = "%a %d-%b-%Y"
UTC_FMT = "%Y-%m-%dT%H:%M:%SZ"
DB_NAME = BASE_DIR / "DBs" / "jobs.db"

def to_utc(date_str):
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, DATE_FMT)
        dt = dt.replace(tzinfo=ZoneInfo("America/Toronto"))
        return dt.astimezone(ZoneInfo("UTC")).strftime(UTC_FMT)
    except Exception:
        return None  # or keep original if you prefer


def get_jobs_connection(db=DB_NAME):
    return sqlite3.connect(db)

def init_db():
    conn = get_jobs_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        hash_id TEXT PRIMARY KEY,
        job_id TEXT DEFAULT NULL,
        internal_job_id TEXT DEFAULT NULL,
        job_name TEXT NOT NULL,
        source TEXT NOT NULL,
        job_board TEXT NOT NULL,
        work_policy TEXT DEFAULT NULL,
        location TEXT DEFAULT NULL,
        secondary_loc TEXT DEFAULT NULL,
        creation_date TEXT DEFAULT NULL,
        posted_date TEXT DEFAULT NULL,
        updated_date TEXT DEFAULT NULL,
        filled_date TEXT DEFAULT NULL,
        url TEXT NOT NULL,
        comp TEXT DEFAULT NULL,
        hiring_manager TEXT DEFAULT NULL
    )
    """)

    conn.commit()
    conn.close()

def load_db(path=DB_JSON_PATH):
    try:
        with open(path, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Missing database: {path}"
        )

    except JSONDecodeError as e:
        raise RuntimeError(
            f"Corrupted database: {path}"
        ) from e


#
# def save_db(db: dict, path="db.json"):
#     with open(path, "w") as f:
#         json.dump(db, f, indent=4)
#
#
def save_db(db: dict):

    temp_path = DB_JSON_PATH.with_suffix(".tmp")

    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)

        temp_path.replace(DB_JSON_PATH)

    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise

    # 2️⃣ Save to SQL
    conn = get_jobs_connection()
    cursor = conn.cursor()
    i=1
    for hash,job in db.items():
        try:
            cursor.execute("""
            INSERT INTO jobs (
                hash_id, job_id, internal_job_id, job_name, source, job_board,
                work_policy, location, secondary_loc,
                creation_date, posted_date, updated_date, filled_date,
                url, comp, hiring_manager
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(hash_id) DO UPDATE SET
                job_id=excluded.job_id,
                internal_job_id=excluded.internal_job_id,
                job_name=excluded.job_name,
                source=excluded.source,
                job_board=excluded.job_board,
                work_policy=excluded.work_policy,
                location=excluded.location,
                secondary_loc=excluded.secondary_loc,
                creation_date=excluded.creation_date,
                posted_date=excluded.posted_date,
                updated_date=excluded.updated_date,
                filled_date=excluded.filled_date,
                url=excluded.url,
                comp=excluded.comp,
                hiring_manager=excluded.hiring_manager
            """, (
                hash,
                job.get("job_id"),
                job.get("internal_job_id"),
                job["job_name"],
                job["source"],
                job["job_board"],
                job.get("work_policy"),
                job.get("location"),
                job.get("secondary_loc"),
                to_utc(job.get("creation_date")),
                to_utc(job.get("posted_date")),
                to_utc(job.get("updated_date")),
                to_utc(job.get("filled_date")),
                job["url"],
                job.get("comp"),
                job.get("hiring_manager"),
            ))

        except Exception as e:
            print(f'{i} The following error occurred: {e}, for the following {hash}')
            i += 1

    conn.commit()
    conn.close()

def migrate_jobs(db=None):
    conn = get_jobs_connection(db) if db else get_jobs_connection()
    cursor = conn.cursor()

    columns = {
        row[1]
        for row in cursor.execute("PRAGMA table_info(jobs)")
    }

    if "jd" not in columns:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN jd TEXT DEFAULT 'NA'
        """)

    if "salary_extractor" not in columns:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN salary_extractor TEXT DEFAULT 'NO    '
        """)

    conn.commit()
    conn.close()

if __name__=='__main__':
    migrate_jobs()