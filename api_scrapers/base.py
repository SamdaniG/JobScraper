from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import re

class ApiJobBoardScraper(ABC):
    name="base"
    url=""
    jd_url=""
    base_domain=''

    @abstractmethod
    def scrape_jobs(self, driver):
        raise NotImplementedError

    @abstractmethod
    def scrape_jd(self,driver=None, source= dict):
        raise NotImplementedError

    def clean_html(self, raw_html: str) -> str:
        soup = BeautifulSoup(raw_html, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        lines = [line.strip() for line in text.splitlines()]
        text = "\n".join(line for line in lines if line)

        # Fix colon formatting
        text = re.sub(r"\n\s*:", ":", text)

        # Collapse multiple blank lines
        text = re.sub(r"\n{2,}", "\n\n", text)

        return text.strip()