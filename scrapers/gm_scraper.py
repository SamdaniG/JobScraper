import json
import time
from datetime import date

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from utils import sha256_hex, get_text_or_none, get_exact_posting_date
from diff import DATE_FMT
from scrapers.base import JobBoardScraper


class GMScraper(JobBoardScraper):
    name = "gm"
    #url = "https://generalmotors.wd5.myworkdayjobs.com/Careers_GM"
    url= 'https://generalmotors.wd5.myworkdayjobs.com/Careers_GM?Location_Country=a30a87ed25634629aa6c3958aa2b91ea'
    jd_locator = '[data-automation-id="jobPostingDescription"]'

    def scrape_jobs(self, driver):
        driver.get(self.url)
        wait = WebDriverWait(driver, 10)

        #self.filtering_by_country(driver)

        current_jobs_id = []
        job_data = {}
        flag = True
        #time.sleep(3)


        while flag:
            job_titles = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".css-1q2dra3")
                )
            )

            for job_title in job_titles:
                try:
                    url = job_title.find_element(
                        By.CSS_SELECTOR,
                        '.css-19uc56f'
                    ).get_attribute("href")

                    hash_id = sha256_hex(url)
                    current_jobs_id.append(hash_id)


                    job_data[hash_id] = {
                        "job_id": job_title.find_element(
                            By.CSS_SELECTOR,
                            '[data-automation-id="subtitle"]'
                        ).text,
                        "job_name": get_text_or_none(
                            job_title,
                            By.CSS_SELECTOR,
                            '.css-19uc56f'
                        ),
                        "source":self.name,
                        "work_policy": get_text_or_none(
                            job_title,
                            By.CSS_SELECTOR,
                            '[data-automation-id="remoteType"] .css-129m7dg'
                        ),
                        "location": get_text_or_none(
                            job_title,
                            By.CSS_SELECTOR,
                            '[data-automation-id="locations"] .css-129m7dg'
                        ),
                        "posted_date": get_exact_posting_date(
                            job_title,
                            By.CSS_SELECTOR,
                            '.css-zoser8 .css-129m7dg'
                        ),
                        "filled_date": "",
                        "url": url
                    }

                except Exception as e:
                    print(f"Found an error skipping this, error is {e}")


            next_page_button = driver.find_elements(
                By.CSS_SELECTOR,
                '[data-uxi-widget-type="stepToNextButton"]'
            )

            if next_page_button:
                next_page_button[0].click()
                time.sleep(5)
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(job_titles[0])
                )
            else:
                flag = False

        return current_jobs_id, job_data

    def filtering_by_country(self, driver, country="Canada", timeout=10):
        wait = WebDriverWait(driver, timeout)

        country_selector = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-uxi-element-id="filter_Location_Country"]')
            )
        )
        country_selector.click()

        country_option = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#a30a87ed25634629aa6c3958aa2b91ea')
            )
        )
        country_option.click()

        view_jobs = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.css-wfmr0b')
            )
        )
        view_jobs.click()

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.css-1q2dra3')
            )
        )
