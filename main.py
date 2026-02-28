# main.py
import time
from selenium import webdriver
from datetime import date
from diff import diff_jobs
# from scrapers.rivian_scraper import RivianScraper
from storage import load_db, save_db
from log_starter import set_logger
from scrapers.gm_scraper import GMScraper
from api_scrapers.ford_scraper import FordScraper
from api_scrapers.lumentum_scraper import LumentumScraper
from api_scrapers.kepler_scraper import KeplerScraper
from api_scrapers.waabi_scraper import WaabiScraper
from api_scrapers.rivian_scraper import RivianScraper

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

#Adding headless options to chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

#driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
driver.minimize_window()

db = load_db()

all_current_job_ids = []
all_scraped_jobs = {}

scrapers = [RivianScraper(), GMScraper(), WaabiScraper(), FordScraper(), LumentumScraper(),KeplerScraper()]
# scrapers = []
logger.info(f"Scraping the jobs from the site")

for scraper in scrapers:
    logger.info(f"Running {scraper.name} scraper now.")
    # driver.get(scraper.url)
    current_jobs_id, scraped_jobs_db = scraper.scrape_jobs(driver)

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
        logger.debug("Emailing filled jobs")

        for j in filled_jobs:
            logger.info(
                f'{db[j]["source"]} - '
                f'{db[j].get("job_id","")} - '
                f'{db[j]["job_name"]}'
            )

        body = "\n".join(
            f'{db[j]["source"]} - '
            f'{db[j].get("job_id",{db[j]["url"]})} - '
            f'{db[j]["job_name"]}'
            for j in filled_jobs
        )
        send_email("Filled Positions", body)

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
            "Emailing new job: %s (%s)",
            job["job_name"],
            job["source"],
        )

        jd = scraper.scrape_jd(driver, job)
        send_email(job["job_name"], jd, job["source"])

        if len(new_jobs) > 1:
            time.sleep(EMAIL_DELAY_SECONDS)


logger.info(f"Writing data to my database!\n-------------------")
save_db(db)
driver.quit()
