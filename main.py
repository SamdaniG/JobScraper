import time
from datetime import date
from diff import diff_jobs, updating_db
from storage import load_db, save_db
from log_starter import set_logger
from scrapers.__base import ApiJobBoardScraper
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from functools import wraps

def format_job_board_registry():
    lines = []
    lines.append("\t\t\tAVAILABLE JOB BOARDS ")
    lines.append("=" * 80)

    for board, scrapers in ApiJobBoardScraper.job_board_registry.items():
        lines.append(f"\t\t{board} ({len(scrapers)})")
        lines.append(" •".join(x.name for x in scrapers))

    lines.append("\n" + "="*80)
    return "\n".join(lines)

###Adding parser arguments
parser = argparse.ArgumentParser(
    description=f"Job scraper runner. \n"
                f"{format_job_board_registry()}",
    formatter_class=argparse.RawTextHelpFormatter
)
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
parser.add_argument(
    "--jobboard",
    help="Run all scrapers under a specific job board"
)
parser.add_argument(
    "--list",
    action="store_true",
    help="List all job boards and their companies"
)
args = parser.parse_args()
if args.list:
    print(format_job_board_registry())
    exit(0)
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
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        #print(f"Started the timer!")
        name, result, error= func(*args, **kwargs)
        end = time.perf_counter()
        logger.timer(f"Time taken to run the {name}: {end - start:.4f}s",
                     extra={
                         "source"               : name,
                         "timer"                : end - start
                     })
        return name, result, error
    return wrapper

@time_taken
def run_scraper(Scraper):
    scraper = Scraper()
    try:
        scraped_jobs_db = scraper.scrape_jobs()
        return scraper.name,scraped_jobs_db, None
    except Exception as e:
        return scraper.name, None, e


if args.company and args.jobboard:
    raise ValueError("Use either --company or --jobboard, not both.")

if args.company:
    scrapers_to_run = []

    for c in args.company:
        c=c.lower()
        if c not in ApiJobBoardScraper.registry:
            available = ", ".join(ApiJobBoardScraper.registry.keys())
            raise ValueError(f"Unknown scraper: {c}.\n "
                             f"{format_job_board_registry()}")

        scrapers_to_run.append(ApiJobBoardScraper.registry[c])

elif args.jobboard:
    jobboard = args.jobboard.lower()

    if jobboard not in ApiJobBoardScraper.job_board_registry:
        available = ", ".join(ApiJobBoardScraper.job_board_registry.keys())
        raise ValueError(
            f"Unknown job board: {jobboard}. \n"
            f"{format_job_board_registry()}"
        )

    scrapers_to_run = list(ApiJobBoardScraper.job_board_registry[jobboard])

else:
    scrapers_to_run = list(ApiJobBoardScraper.registry.values())

logger.info(
    "Running %d scraper(s) | mode=%s",
    len(scrapers_to_run),
    "company" if args.company else "jobboard" if args.jobboard else "all"
)
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
                f"{job["job_name"]} ({job["source"]}) ({job.get('job_id',"")})",
                extra={
                "job_name" : job["job_name"],
                "source" : job["source"],
                "job_id" : job.get('job_id',""),
                "location": job.get('location', "")
            })

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
                f"{job["job_name"]} ({job["source"]} ({job.get('job_id',"")})",
                extra={
                "job_name" : job["job_name"],
                "source" : job["source"],
                "job_id" : job.get('job_id',""),
                "location": job.get('location', "")
            }

            )

logger.info(f"Writing data to my database!\n-------------------")
save_db(db)

