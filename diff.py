# diff.py
from datetime import timedelta

DATE_FMT = "%a %d-%b-%Y"

def diff_jobs(db: dict, current_jobs_id: list, today, successful_sources, current_jobs_db: dict):
    new_jobs = []
    filled_jobs = []
    update_jobs = []
    current_jobs_id=set(current_jobs_id)

    for job_id in current_jobs_id:
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
            db[job_id]["filled_date"] = today.strftime(DATE_FMT)
            filled_jobs.append(job_id)

    return new_jobs, filled_jobs, update_jobs

def dict_changes(old: dict, new: dict, ignore=None):
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
            logger.info(
                "%s %s %s updated:",
                old["source"],
                job_id,
                old["job_name"]
            )

            for field, (old_val, new_val) in changes.items():
                logger.info("  %s: %s -> %s", field, old_val, new_val)

        db[job_id].update(new)
        db[job_id].pop("filled_date", None)

    return db