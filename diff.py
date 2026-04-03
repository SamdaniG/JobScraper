# diff.py
from datetime import timedelta
from datetime import date
DATE_FMT = "%a %d-%b-%Y"
DEFAULT_DATE = "Thu 01-Jan-2026"

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
        new = all_scraped_jobs[job_id].copy()

        old_date = old.get("posted_date",None)
        new_date = new.get("posted_date",None)

        # ✅ Fix bad API date BEFORE updating
        if new_date == DEFAULT_DATE and old_date is not None:
            new["posted_date"] = old_date

        changes = dict_changes(old, new)#, ignore={"filled_date"})

        if changes:
            for field, (old_val, new_val) in changes.items():
                logger.updated(
                    f'{old["source"]} - {job_id} - {old["job_name"]} updated:'
                    f"\n\t\t\t\t\t\t {field}: {old_val} -> {new_val}",
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
        db[job_id].clear()
        db[job_id].update(new)
        db[job_id].pop("filled_date", None)
        #
        # if new_date is not None and new_date == "Thu 01-Jan-2026":
        #     db[job_id]["posted_date"]=old_date

    return db