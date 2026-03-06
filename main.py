import time
from datetime import date
from diff import diff_jobs
from storage import load_db, save_db
from log_starter import set_logger
from scrapers.gm_scraper import GMScraper
from scrapers.ford_scraper import FordScraper
from scrapers.lumentum_scraper import LumentumScraper
from scrapers.kepler_scraper import KeplerScraper
from scrapers.waabi_scraper import WaabiScraper
from scrapers.rivian_scraper import RivianScraper
from scrapers.linamar_scraper import LinamarScraper
from scrapers.honda_scraper import HondaScraper
from scrapers.trimble_scraper import TrimbleScraper
from scrapers.ztr_scraper import ZTRScraper
from scrapers.aerovect_scraper import AerovectScraper
from scrapers.cobot_scraper import CobotScraper
from scrapers.kodiak_scraper import KodiakScraper
from scrapers.lucidmotors_scrapers import LucidMotorsScraper
from scrapers.appliedintuition_scraper import AppliedIntuitionScraper
from scrapers.gatik_scraper import GatikScraper
from scrapers.nuro import NuroScraper
from scrapers.nextstar_scraper import NextStarSraper
from scrapers.gastops_scraper import GAStopsSraper

import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "--source",
    default="manual",
    help="Who triggered the script (manual, scheduler, api, ci, etc.)"
)

args = parser.parse_args()
logger=set_logger(args)

EMAIL_ACTIVE = False
EMAIL_DELAY_SECONDS=5
if args.source == 'scheduler':
    EMAIL_ACTIVE = True

db = load_db()

all_current_job_ids = []
all_scraped_jobs = {}

scrapers = [RivianScraper(), GMScraper(), WaabiScraper(),
            FordScraper(), LumentumScraper(), KeplerScraper(),
            LinamarScraper(), HondaScraper(), TrimbleScraper(),
            ZTRScraper(), AerovectScraper(), CobotScraper(),
            KodiakScraper(), LucidMotorsScraper(), AppliedIntuitionScraper(),
            GatikScraper(), NuroScraper(), NextStarSraper(),
            GAStopsSraper()]
logger.info(f"Scraping the jobs from the site")

for scraper in scrapers:
    logger.info(f"Running {scraper.name} scraper now.")
    # driver.get(scraper.url)
    current_jobs_id, scraped_jobs_db = scraper.scrape_jobs()

    all_current_job_ids.extend(current_jobs_id)
    all_scraped_jobs.update(scraped_jobs_db)
# logger.info(f"Scraping the jobs from the site")
# current_jobs_id, scraped_jobs_db = scrape_jobs(driver)

logger.info(f"Checking the new/old jobs created.")
new_jobs, filled_jobs = diff_jobs(db, all_current_job_ids, date.today())
logger.info(
    "Diff complete | new_jobs=%d filled_jobs=%d",
    len(new_jobs),
    len(filled_jobs),
)

for job_id, data in all_scraped_jobs.items():
    if job_id not in db:
        db[job_id] = data

# new_jobs, filled_jobs = diff_jobs(db, current_jobs_id, date.today())
# print(f"{new_jobs= }\n{filled_jobs= }")
if EMAIL_ACTIVE:
    from emailer import send_email

    scraper_map = {s.name: s for s in scrapers}

    # 1️⃣ Email filled jobs
    if filled_jobs:
        lines = []
        html_lines = []
        logger.debug("Emailing filled jobs")
        for j in filled_jobs:
            job = db[j]
            logger.info(
                f'{job["source"]} - '
                f'{job.get("job_id","")} - '
                f'{job["job_name"]}'
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


    # 2️⃣ Email new jobs with correct scraper
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

        logger.debug(
            "Emailing new job: %s (%s) (%s)",
            job["job_name"],
            job["source"],
            job.get('job_id',"")
        )
        jd_content = scraper.scrape_jd(job)
        text_body = job['url'] + '\n'
        text_body += jd_content

        html_body = f"""
        <p>
        <a href="{job['url']}">View Job Posting</a>
        </p>
        <pre>
        {jd_content}
        </pre>
        """

        send_email(job["job_name"], text_body, html_body, job["source"])

        if len(new_jobs) > 1:
            time.sleep(EMAIL_DELAY_SECONDS)


logger.info(f"Writing data to my database!\n-------------------")
save_db(db)

