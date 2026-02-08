# scraper.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date

from utils import sha256_hex, get_text_or_none
from diff import DATE_FMT

def scrape_jobs(driver):
    wait = WebDriverWait(driver, 10)

    job_titles = wait.until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "posting-title")
        )
    )

    current_jobs_id = []
    job_data = {}

    for job_title in job_titles:
        url = job_title.get_attribute("href")
        hash_id = sha256_hex(url)
        current_jobs_id.append(hash_id)

        job_data[hash_id] = {
            "job_name": get_text_or_none(job_title, By.CSS_SELECTOR, "h5"),
            "work_policy": get_text_or_none(job_title, By.CSS_SELECTOR, ".workplaceTypes")[:-2],
            "location": get_text_or_none(job_title, By.CSS_SELECTOR, ".location"),
            "commitment": get_text_or_none(job_title, By.CSS_SELECTOR, ".commitment"),
            "posted_date": date.today().strftime(DATE_FMT),
            "filled_date": "",
            "url": url
        }

    return current_jobs_id, job_data

def scrape_jd(driver, url):
    original_window = driver.current_window_handle

    driver.switch_to.new_window('tab')
    driver.get(url=url)
    wait = WebDriverWait(driver, 10)
    info = f"{url}\n"
    #descriptions = driver.find_elements(By.CLASS_NAME, value="section-wrapper")
    descriptions =    wait.until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "section-wrapper")
        )
    )
    for desc in descriptions:
        info += desc.text
    driver.close()
    driver.switch_to.window(original_window)

    return info