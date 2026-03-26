# diff.py
from datetime import timedelta
from datetime import date
DATE_FMT = "%a %d-%b-%Y"

def diff_jobs(db: dict, current_jobs_db: dict, successful_sources: set):
    today = date.today().strftime(DATE_FMT)

    db_ids = set(db)
    current_ids = set(current_jobs_db)

    # New jobs
    new_jobs = current_ids - db_ids

    # Updated jobs
    common_ids = current_ids & db_ids
    update_jobs = {
        job_id for job_id in common_ids
        if current_jobs_db[job_id] != db[job_id]
        }

    # Filled jobs
    filled_jobs = set()
    missing_ids = db_ids - current_ids

    for job_id in missing_ids:
        job = db[job_id]

        if job["source"] not in successful_sources:
            continue

        if job.get("filled_date", "") == "":
            job["filled_date"] = today
            filled_jobs.add(job_id)

    return new_jobs, filled_jobs, update_jobs

def dict_changes(old: dict, new: dict, ignore=None):
    ignore = {"filled_date"}
    if ignore is None:
        ignore = set()

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

def updating_db(db,all_scraped_jobs, new_jobs, updated_jobs, logger):
    for job_id in new_jobs:
        db[job_id]=all_scraped_jobs[job_id]

    for job_id in updated_jobs:
        # from diff import dict_changes
        old = db[job_id]
        new = all_scraped_jobs[job_id]

        changes = dict_changes(old, new)#, ignore={"filled_date"})

        if changes:
            for field, (old_val, new_val) in changes.items():
                logger.updated(
                    f"{old["source"]} {job_id} {old["job_name"]} updated:"
                    f"\n\t\t\t\t\t\t\t\t {field}: {old_val} -> {new_val}",
                    extra=
                    {
                       "job_name" : old["job_name"],
                       "source" : old["source"],
                       "job_id" : job_id,
                       "field" : field,
                       "old_val": old_val,
                       "new_val": new_val,
                       "location": old['location']
                    })
        # db[job_id].clear()
        db[job_id].update(new)
        db[job_id].pop("filled_date", None)

    return db