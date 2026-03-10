# diff.py
from datetime import timedelta

DATE_FMT = "%a %d-%b-%Y"

def diff_jobs(db: dict, current_jobs_id: list, today, successful_sources):
    new_jobs = []
    filled_jobs = []

    for job_id in current_jobs_id:
        if job_id not in db:
            new_jobs.append(job_id)

    for job_id,job in db.items():

        source = job["source"]

        if source not in successful_sources:
            continue

        # if job_id not in current_jobs_id:
        if job_id not in current_jobs_id and job.get("filled_date","") == "":
            db[job_id]["filled_date"] = today.strftime(DATE_FMT)
            filled_jobs.append(job_id)

    return new_jobs, filled_jobs
