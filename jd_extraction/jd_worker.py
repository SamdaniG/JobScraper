from log_starter import get_q_connection
import sqlite3
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrapers.__base import ApiJobBoardScraper
from jd_extraction.jd_init import jd_initialize, get_jd_connection
import re
import hashlib
from datetime import  datetime
from storage import get_jobs_connection
from timer_wrapper import time_taken

def normalize_jd(jd):
    return " ".join(jd.split())

def hash_jd(jd):

    return hashlib.sha256(
        jd.encode("utf-8")
    ).hexdigest()

def extract_salaries(text):
    results = []

    currency = r"(USD|CAD)"
    amount = r"\$\d+(?:,\d{3})*(?:\.\d+)?[Kk]?"
    salary = rf"{amount}(?:\s*-\s*{amount})?"
    prefix = rf"(?:{currency}\s*)?({salary})"
    suffix = rf"({salary})(?:\s*{currency})?"

    # Matches: USD $60, CAD $120K, or just $60
    for curr, sal in re.findall(prefix, text, flags=re.IGNORECASE):
        results.append({
            "currency": curr.upper() if curr else None,
            "salary": sal
        })

    # Matches: $60 USD, $120K CAD, or just $60
    for sal, curr in re.findall(suffix, text, flags=re.IGNORECASE):
        results.append({
            "currency": curr.upper() if curr else None,
            "salary": sal
        })

    # Remove duplicates and convert to string
    unique = []
    seen = set()

    for item in results:
        value = (
            f"{item['salary']} {item['currency']}"
            if item["currency"]
            else item["salary"]
        )

        if value not in seen:
            seen.add(value)
            unique.append(value)

    return " & ".join(unique)

def get_pending_tasks(limit=50):

    with get_q_connection() as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT
                id,
                hash_id,
                info,
                task,
                uuid
            FROM q
            WHERE status='pending'
            ORDER BY id desc
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return [dict(row) for row in rows]

def mark_processing(ids):

    with get_q_connection() as conn:
        conn.executemany(
            """
            UPDATE q
            SET status='processing'
            WHERE id=?
            """,
            [(i,) for i in ids]
        )

def scrape_jd_worker(task):

    job = json.loads(task["info"])
    source = job.get("source")

    if not source:
        return {
            "id": task["id"],
            "hash_id": task["hash_id"],
            "jd": None,
            "error": "Missing source",
            "uuid": task["uuid"]
        }

    try:
        scraper = ApiJobBoardScraper.registry[source]()
        jd = scraper.scrape_jd(job)

        return {
            "id": task["id"],
            "hash_id": task["hash_id"],
            "jd": jd,
            "error": None,
            "uuid": task["uuid"]
        }

    except Exception as e:

        return {
            "id": task["id"],
            "hash_id": task["hash_id"],
            "jd": None,
            "error": str(e),
            "uuid": task["uuid"]
        }

def reset_processing_tasks():
    with get_q_connection() as conn:
        conn.execute(
            """
            UPDATE q
            SET status='pending'
            WHERE status='processing'
            """
        )

def remove_task(q_id):
    with get_q_connection() as conn:
        conn.execute(
            """
            DELETE FROM q
            WHERE id=?
            """,
            (q_id,)
        )

def retry_task(q_id, error):

    with get_q_connection() as conn:
        conn.execute(
            """
            UPDATE q
            SET 
                status='pending',
                retry_count=retry_count+1,
                error=?
            WHERE id=?
            """,
            (error, q_id)
        )

def update_job_jd(hash_id, salary):

    with get_jobs_connection() as conn:
        conn.execute(
            """
            UPDATE jobs
            SET
                jd_avail='YES',
                salary_extracted=?
            WHERE hash_id=?
            """,
            (
                salary,
                hash_id
            )
        )

def save_jd(
    hash_id,
    jd,
    jd_hash,
    uuid=None
):
    timestamp = datetime.now().isoformat()

    with get_jd_connection() as conn:
        conn.execute(
            """
                INSERT INTO jd (
                    hash_id,
                    jd,
                    jd_hash,
                    created_at,
                    updated_at,
                    uuid
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(hash_id) DO UPDATE SET
                    jd=excluded.jd,
                    jd_hash=excluded.jd_hash,
                    updated_at=excluded.updated_at,
                    uuid=excluded.uuid
            """,
            (
                hash_id,
                jd,
                jd_hash,
                timestamp,
                timestamp,
                uuid
            )
        )


@time_taken
def jd_worker(logger=None):
    # task = get_pending_tasks()
    reset_processing_tasks()
    jd_initialize()
    tasks = get_pending_tasks(1000)
    results=[]

    ids = [
        task["id"]
        for task in tasks
    ]

    mark_processing(ids)

    with ThreadPoolExecutor(max_workers=20) as executor:

        futures = [
            executor.submit(scrape_jd_worker, task)
            for task in tasks
        ]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    for r in results:

        # FAILURE
        if r["error"] is not None:
            retry_task(
                r["id"],
                r["error"]
            )

            continue

        # SUCCESS

        jd_hash = hash_jd(r["jd"])
        salary = extract_salaries(r["jd"])

        r["salary"] = salary
        r["hash_jd"] = jd_hash
        r["timestamp"] = datetime.now().isoformat()

        # 1. Save full JD
        save_jd(
            hash_id=r["hash_id"],
            jd=r["jd"],
            jd_hash=jd_hash,
            uuid=r["uuid"]
        )

        # 2. Update jobs table
        update_job_jd(
            hash_id=r["hash_id"],
            salary=salary
        )

        # 3. Remove completed queue task
        remove_task(
            r["id"]
        )

        # print(json.dumps(r, indent=4))

if __name__=='__main__':
    jd_worker()

