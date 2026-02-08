# main.py
import time

from selenium import webdriver
from datetime import date

from scraper import scrape_jobs,scrape_jd
from diff import diff_jobs
from storage import load_db, save_db
from log_starter import set_logger

logger=set_logger()

EMAIL_ACTIVE = False
EMAIL_DELAY_SECONDS=5
URL = "https://jobs.lever.co/waabi"

#Adding headless options to chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
driver.get(URL)


db = load_db()

logger.info(f"Scraping the jobs from the site")
current_jobs_id, scraped_jobs_db = scrape_jobs(driver)

logger.info(f"Checking the new/old jobs created.")
new_jobs, filled_jobs = diff_jobs(db, current_jobs_id, date.today())
logger.info(
    "Diff complete | new_jobs=%d filled_jobs=%d",
    len(new_jobs),
    len(filled_jobs),
)


# merge new jobs into db
for job_id, data in scraped_jobs_db.items():
    if job_id not in db:
        db[job_id] = data

# new_jobs, filled_jobs = diff_jobs(db, current_jobs_id, date.today())
# print(f"{new_jobs= }\n{filled_jobs= }")

if EMAIL_ACTIVE:
    from emailer import send_email
    if filled_jobs:
        logger.debug(f"Emailing the filled jobs.")
        body = "\n".join(db[j]["job_name"] for j in filled_jobs)
        send_email("Waabi Filled Positions", body)

    for job_id in new_jobs:
        logger.debug(f"Emailing about the new job, {db[job_id]['job_name']}")
        jd=scrape_jd(driver, db[job_id]["url"])
        send_email(f"Waabi {db[job_id]['job_name']}", jd)
        if len(new_jobs)>1:
            time.sleep(EMAIL_DELAY_SECONDS)

logger.info(f"Writing data to my database!\n-------------------")
save_db(db)
driver.quit()
