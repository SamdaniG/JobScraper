import json
from scrapers.__base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
from datetime import datetime
from bs4 import BeautifulSoup

FMT='%Y-%m-%dT%H:%M:%S.%fZ'
DATE_FMT = "%a %d-%b-%Y"


class UltiproScraper(ApiJobBoardScraper):
    name = 'base'
    base_domain = 'https://recruiting.ultipro.ca/'

    jobBoard = 'ultipro'
    base_active = True
    company_active = True

    company_hex=""
    company_id=""

    jd_params = {}

    @property
    def base_url(self):
        return  (self.base_domain + self.company_hex +
                '/JobBoard/' + self.company_id)

    @property
    def data_url(self):
        return (self.base_url +
                "/JobBoardView/LoadSearchResults")

    @property
    def jd_url(self):
        return self.base_url + "/OpportunityDetail"

    payload = {
        "opportunitySearch": {
            "Top": 500,
            "Skip": 0,
            "QueryString": "",
            "OrderBy": [
                {
                    "Value": "postedDateDesc",
                    "PropertyName": "PostedDate",
                    "Ascending": False,
                }
            ],
            "Filters": []
        }
    }

    def scrape_jobs(self):
        job_data = {}
        resp = self.session.get(url=self.data_url, json= self.payload ,timeout=30)#,params=self.params)
        # print(resp.raise_for_status())
        dat=resp.json()
        # print(json.dumps(dat,indent=4))
        jobs_list=dat.get("opportunities")
        # print(json.dumps(jobs_list[0],indent=4))

        for job in jobs_list:
            job_id=         job['Id']
            job_name =      job['Title']
            hash_id=        sha256_hex(str(job_id))
            # current_jobs_id.append(hash_id)

            job_deets=Job(
                job_id=         job_id,
                job_name=       job_name,
                source=         self.name,
                location=       job['Locations'][0]['LocalizedDescription'],
                posted_date=    datetime.strptime(job['PostedDate'],FMT).strftime(DATE_FMT),
                url=            self.base_url + "/OpportunityDetail?opportunityId=" + job_id,
                job_board=      self.jobBoard

            )
            job_data[hash_id]=job_deets.to_dict()


        return  job_data

    def scrape_jd(self, source: dict=None):
        jd_params = {
            "opportunityId": source['job_id']
        }


        resp=self.session.get(self.jd_url, params = jd_params, timeout=30)

        soup = BeautifulSoup(resp.text, "html.parser")
        script = soup.find(
            "script",
            string=lambda text: text and "CandidateOpportunityDetail(" in text
        )

        if script is None:
            return "Not found"

        marker = "CandidateOpportunityDetail("

        start = script.string.find(marker) + len(marker)

        json_text = script.string[start:]

        decoder = json.JSONDecoder()

        opportunity, end = decoder.raw_decode(json_text)

        jd = opportunity["Description"]

        return self.clean_html(jd)

