from abc import ABC, abstractmethod

from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class JobBoardScraper(ABC):
    name = "base"
    url = ""
    jd_locator=""

    @abstractmethod
    def scrape_jobs(self, driver):
        raise NotImplementedError


    def scrape_jd(self, driver: WebDriver, source):
        url=source["url"]
        # raise  NotImplementedError

        original_window = driver.current_window_handle

        driver.switch_to.new_window('tab')
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        info = f"{url}\n"

        descriptions = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, self.jd_locator)
            )
        )

        for desc in descriptions:
            info += desc.text

        driver.close()
        driver.switch_to.window(original_window)

        return info
