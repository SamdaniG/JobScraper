import time
from datetime import date
from diff import diff_jobs, updating_db
from storage import load_db, save_db
from log_starter import set_logger
from scrapers.__base import ApiJobBoardScraper
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from functools import wraps
###Adding parser arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--source",
    default="manual",
    help="Who triggered the script (manual, scheduler, api, ci, etc.)"
)
parser.add_argument(
    "--company",
    nargs="+",
    help="Run specific company scrapers"
)
args = parser.parse_args()
logger=set_logger(args)

####Activating Email
EMAIL_ACTIVE = False
EMAIL_DELAY_SECONDS=5
if args.source == 'scheduler':
    EMAIL_ACTIVE = True

#Initiating variables
db = load_db()
# all_current_job_ids = set()
all_scraped_jobs = {}
successful_scrapers = set()

def time_taken(func):
    """This is a python decorator to calculate the time taken to run every function, gives us a useful metric to keep track"""
    @wraps(func)
    def wrapper(*args):
        start = time.time()
        #print(f"Started the timer!")
        results = func(*args)
        end = time.time()
        logger.debug(f"\t\tTime taken to run the {args[0]().name}: {end - start:.4f}s")
        return results
    return wrapper

@time_taken
def run_scraper(Scraper):
    scraper = Scraper()
    try:
        scraped_jobs_db = scraper.scrape_jobs()
        return scraper.name,scraped_jobs_db, None
    except Exception as e:
        return scraper.name, None, e

if args.company:
    scrapers_to_run = []

    for c in args.company:
        if c not in ApiJobBoardScraper.registry:
            available = ", ".join(ApiJobBoardScraper.registry.keys())
            raise ValueError(f"Unknown scraper: {c}. Available: {available}")

        scrapers_to_run.append(ApiJobBoardScraper.registry[c])
else:
    scrapers_to_run = ApiJobBoardScraper.registry.values()

logger.info(f"Running {len(scrapers_to_run)} scraper(s)")
i=1
with ThreadPoolExecutor(max_workers=min(15,len(scrapers_to_run))) as executor:
    futures = [
        executor.submit(run_scraper, Scraper)
        for Scraper in scrapers_to_run
    ]

    for future in as_completed(futures):
        name, scraped_jobs_db, error = future.result()

        if error:
            logger.error(f"{name} failed: {error}")
            continue

        logger.info(f"{i:02d}: {name}")

        successful_scrapers.add(name)
        # all_current_job_ids.add(current_jobs_id)
        all_scraped_jobs.update(scraped_jobs_db)
        i+=1

logger.info(f"Checking the new/old jobs created.")
new_jobs, filled_jobs, updated_jobs = diff_jobs(db,all_scraped_jobs,successful_scrapers,)
logger.info(
    "Diff complete | new_jobs=%d filled_jobs=%d updated_jobs=%d",
    len(new_jobs),
    len(filled_jobs),
    len(updated_jobs)
)

db = updating_db(db,all_scraped_jobs, new_jobs, updated_jobs, logger)

# new_jobs, filled_jobs = diff_jobs(db, current_jobs_id, date.today())
# print(f"{new_jobs= }\n{filled_jobs= }")
if EMAIL_ACTIVE:
    from emailer import send_email

    scraper_map = {s.name: s() for s in scrapers_to_run}

    # 1️⃣ Email filled jobs
    if filled_jobs:
        lines = []
        html_lines = []
        logger.debug("Emailing filled jobs")
        for j in filled_jobs:
            job = db[j]
            logger.filled(
                f'{job["source"]} - '
                f'{job.get("job_id","")} - '
                f'{job["job_name"]}',
                extra={
                "job_name":job["job_name"],
                "source":job["source"],
                "job_id":job.get('job_id', ""),
                "location":job.get('location',"")
            }
            )

            text_line = (
                f'{job["source"]} - '
                f'{job.get("job_id", job["url"])} - '
                f'{job["job_name"]}'
            )

            html_line = (
                f'{job["source"]} - '
                f'{job.get("job_id", job["url"])} - '
                f'<a href="{job["url"]}">{job["job_name"]}</a>'
            )

            lines.append(text_line)
            html_lines.append(html_line)

        text_body = "\n".join(lines)
        html_body = "<br>".join(html_lines)

        send_email("Filled Positions", text_body, html_body, "System")
        if len(new_jobs) > 1:
            time.sleep(EMAIL_DELAY_SECONDS)

    # 2️⃣ Email new jobs with correct scraper
    filled_email_composing = ""
    try:
        for job_id in new_jobs:
            job = db[job_id]
            scraper = scraper_map.get(job["source"])

            if not scraper:
                logger.warning(
                    "No scraper found for source=%s (job_id=%s)",
                    job["source"],
                    job_id,
                )
                continue

            logger.new(
                "%s (%s) (%s)",
                job["job_name"],
                job["source"],
                job.get('job_id', ""),
                extra={
                    "job_name": job["job_name"],
                    "source": job["source"],
                    "job_id": job.get('job_id', ""),
                    "location": job.get('location', "")
                }

            )

            try:
                jd_content = scraper.scrape_jd(job)
            except Exception as e:
                logger.error(f'This error popped up: {e}')
                continue
            text_body = job['url'] + '\n'
            text_body += jd_content

            html_link = f"""
            <p> {job["source"]} - 
            <a href="{job['url']}">{job["job_name"]}</a>
            </p>
            """
            html_body=html_link + f"""
            <pre>
            {jd_content}
            </pre>
            """

            send_email(job["job_name"], text_body, html_body, job["source"])
            filled_email_composing += html_link + "\n"
    except Exception as e:
        logger.error(f"The following error occurred: {e}")

    if new_jobs:
        send_email("New Jobs List",html_body=filled_email_composing,body="", source= 'new')

else:
    if filled_jobs:
        # logger.filled('Filled Jobs')
        for j in filled_jobs:
            job = db[j]
            logger.filled(
                f'{job["source"]} - '
                f'{job.get("job_id","")} - '
                f'{job["job_name"]}',
                extra={
                "job_name":job["job_name"],
                "source":job["source"],
                "job_id":job.get('job_id', ""),
                "location": job.get('location', "")
            }
            )
    if new_jobs:
        # logger.info('New jobs')
        for job_id in new_jobs:
            job = db[job_id]
            logger.new(
                "%s (%s) (%s)",
                job["job_name"],
                job["source"],
                job.get('job_id',""),
                extra={
                "job_name" : job["job_name"],
                "source" : job["source"],
                "job_id" : job.get('job_id',""),
                "location": job.get('location', "")
            }

            )

logger.info(f"Writing data to my database!\n-------------------")
save_db(db)

