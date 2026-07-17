from prompt_toolkit.cache import FastDictCache

from scrapers.__base import ApiJobBoardScraper,Job
import requests as rq
import json
from utils import sha256_hex
from datetime import datetime
from bs4 import BeautifulSoup as bs

FMT='%Y-%m-%dT%H:%M:%S.%f%z'
DATE_FMT = "%a %d-%b-%Y"

class PowerCo(ApiJobBoardScraper):
    name = 'PowerCo'
    base_domain = 'https://careers.powerco.de/'
    url = base_domain + 'search/'
    jobBoard = 'API'
    base_active = True
    company_active = False

    params = {
        "createNewAlert" :    "false",
        "q":"",
        "optionsFacetsDD_location" :    "St.Thomas, CA"
    }

    # def scrape_jobs(self, **kwargs):
    #     resp=self.session.get(url= self.url,
    #                           params= self.params)
    #     # print(resp.text)
    #     soup = bs(resp.text,"html.parser")
    #     print(soup.prettify())
    #
    #     data_rows = soup.find_all(class_="data-row")
    #
    #     for row in data_rows:
    #         title = row.text
    #         # print(title)
    def scrape_jobs(self, **kwargs):
        url = "https://career5.successfactors.eu/careersection/rest/jobboard/search"

        # Step 1: bootstrap session
        self.session.get("https://careers.powerco.de/search/")

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://careers.powerco.de",
            "Referer": "https://careers.powerco.de/search/"
        }

        payload = {
            "company": "PowerCoSEp",
            "locale": "en_US",
            "searchText": "",
            "pageSize": 20,
            "pageNumber": 1,
            "sortBy": "date",
            "facetFilters": {}
        }

        resp = self.session.post(url, headers=headers, json=payload)

        # print(resp.status_code)
        # print(resp.text[:1000])  # debug

        data = resp.json()

        for job in data.get("jobList", []):
            print(job.get("title"))

    def scrape_jd(self, source: dict=None):
        pass

if __name__ == '__main__':
    test= PowerCo()
    yo=test.scrape_jobs()
    print(yo)

