# diff.py
from datetime import timedelta
from datetime import date, datetime
import json

DATE_FMT = "%a %d-%b-%Y"
DEFAULT_DATE = "Thu 01-Jan-2026"

ENRICHED_FIELDS = {
    "salary_extractor",
    "jd"
}

def normalize_job(old: dict | None, scraped: dict) -> dict:
    """
    Returns a normalized version of the scraped job.
    Does NOT modify either input dictionary.
    """

    new = scraped.copy()

    # New jobs don't need normalization
    if old is None:
        new.pop("filled_date", None)
        return new

    # preserve enrichment fields
    for field in ENRICHED_FIELDS:
        if field in old:
            new[field] = old[field]

    old_date = old.get("posted_date")
    new_date = new.get("posted_date")

    # API default -> keep old
    if new_date == DEFAULT_DATE and old_date:
        new["posted_date"] = old_date

    # old had default, scraper has actual
    elif old_date == DEFAULT_DATE and new_date:
        new["posted_date"] = new_date

    # compare dates
    elif old_date and new_date and old_date != new_date:
        try:
            old_dt = datetime.strptime(old_date, DATE_FMT)
            new_dt = datetime.strptime(new_date, DATE_FMT)

            diff_days = abs((new_dt - old_dt).days)

            if diff_days == 1:
                new["posted_date"] = new_date

            elif diff_days > 1:
                new["posted_date"] = old_date

        except Exception:
            new["posted_date"] = old_date

    new.pop("filled_date", None)

    return new

def diff_jobs(db: dict, current_jobs_db: dict, successful_sources: set):
    today = date.today().strftime(DATE_FMT)
    current_jobs_id=set(current_jobs_db)
    new_jobs = []
    update_jobs=[]
    filled_jobs=[]

    for job_id in current_jobs_db:
        if job_id not in db:
            new_jobs.append(job_id)
            continue

        if current_jobs_db[job_id]!=db[job_id]:
            update_jobs.append(job_id)

    for job_id,job in db.items():
        source = job["source"]
        if source not in successful_sources:
            continue
        # if job_id not in current_jobs_id:
        if job_id not in current_jobs_id and job.get("filled_date","") == "":
            db[job_id]["filled_date"] = today
            filled_jobs.append(job_id)

    return new_jobs, filled_jobs, update_jobs

def dict_changes(old: dict, new: dict, ignore=None):
    # ignore = {"filled_date"}
    if ignore is None:
        ignore = {"filled_date"}

    changes = {}

    keys = old.keys() | new.keys()

    for k in keys:
        if k in ignore:
            continue

        old_val = old.get(k)
        new_val = new.get(k)

        if old_val != new_val:
            changes[k] = (old_val, new_val)

    return changes

def updating_db(db, all_scraped_jobs, new_jobs, updated_jobs, logger):

    for job_id in new_jobs:
        db[job_id] = all_scraped_jobs[job_id]

    for job_id in updated_jobs:

        old = db[job_id]
        new = all_scraped_jobs[job_id]

        changes = dict_changes(old, new)

        if changes:
            for field, (old_val, new_val) in changes.items():
                logger.updated(
                    f'{old["source"]} - {job_id:.10s} - {old["job_name"]} updated:'
                    f"\n\t\t\t\t\t\t {field}: {old_val} -> {new_val}",
                    extra={
                        "job_name": old["job_name"],
                        "source": old["source"],
                        "hash_id": job_id,
                        "field": field,
                        "old_val": old_val,
                        "new_val": new_val,
                        "location": old["location"],
                        "info": json.dumps(new)
                    },
                )

        db[job_id] = new

    return db