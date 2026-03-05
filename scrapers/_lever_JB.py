from scrapers.__base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
from datetime import datetime

DATE_FMT = "%a %d-%b-%Y"

class LeverBase(ApiJobBoardScraper):
    name='level'
    base_domain = ''
    param = {}

    def scrape_jobs(self):
        current_jobs_id=[]
        job_data={}

        resp=rq.get(url=self.base_domain, params= self.param)
        resp.raise_for_status()
        job_list=resp.json()
        # print(json.dumps(job_list[0],indent=4))

        for job in job_list:
            job_id=job['id']
            job_title=job['text']
            url = job['hostedUrl']
            hash_id=sha256_hex(url)
            current_jobs_id.append(hash_id)

            job_deets=Job(
                job_id=     job_id,
                job_name=   job_title,
                source=     self.name,
                location="; ".join(job["categories"].get('allLocations','')),
                posted_date=(datetime.fromtimestamp(job['createdAt'] / 1000)).strftime(DATE_FMT),
                url=        url,
                work_policy=job["workplaceType"]
            )
            job_data[hash_id]=job_deets.to_dict()

        return current_jobs_id, job_data

    def scrape_jd(self, source:dict=None):
        job_id = source['job_id']

        resp = rq.get(
            url=f"{self.base_domain}/{job_id}",
            params={'mode': 'json'}
        )
        resp.raise_for_status()

        data = resp.json()
        sections = []

        # Main description (HTML)
        if data.get("description"):
            sections.append(data["description"])

        # Structured blocks
        for block in data.get("lists", []):
            if block.get("text"):
                sections.append(block["text"])
            if block.get("content"):
                sections.append(block["content"])

        jd = "\n".join(sections)

        return self.clean_html(jd)
