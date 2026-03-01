from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import sha256_hex, get_text_or_none
from legacy_scrapers.base import JobBoardScraper
import time


class RivianScraper(JobBoardScraper):
    name= "rivian"
    url = "https://careers.rivianvw.tech/rivian-vw-group-technology/jobs?locations=Toronto,Ontario,Canada%7CVancouver,British%20Columbia,Canada&page=1&limit=100&sortBy=posted_date&descending=true"
    jd_locator = ".main-description-body"

    def scrape_jobs(self, driver):
        driver.get(self.url)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait = WebDriverWait(driver, 10)
        time.sleep(3)
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,".search-results")
            )
        )

        job_titles = wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, ".mat-expansion-panel-header")
            )
        )

        current_jobs_id = []
        job_data = {}

        for job_title in job_titles:
            url=job_title.find_element(
                By.CSS_SELECTOR,
                ".job-title-link").get_attribute("href")
            hash_id=sha256_hex(url)
            current_jobs_id.append(hash_id)

            job_data[hash_id] = {
                "job_name": get_text_or_none(
                    job_title,By.CSS_SELECTOR,".job-title-link"
                ),
                "source": self.name,
                "location": get_text_or_none(
                    job_title, By.CSS_SELECTOR, ".label-value.location"
                ),
                "posted_date": "Thu 01-Jan-2026",
                "filled_date": "",
                "url": url
            }

        return current_jobs_id, job_data

