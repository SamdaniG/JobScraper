import json
from scrapers.__base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
from datetime import datetime

FMT='%Y-%m-%dT%H:%M:%S%z'
DATE_FMT = "%a %d-%b-%Y"

class GreenhouseScraper(ApiJobBoardScraper):
    name = 'base'
    base_domain = 'https://boards-api.greenhouse.io/v1/boards/'
    # url = base_domain+ f'{name}/jobs'

    @property
    def url(self):
        return self.base_domain + f'{self.name}/jobs'


    def scrape_jobs(self):
        current_jobs_id=[]
        job_data = {}
        # self.params['page'] = 1
        url = self.base_domain + f'{self.name}/jobs'
        resp = self.session.get(url=self.url, timeout=30)#,params=self.params)
        # print(resp.raise_for_status())
        dat=resp.json()
        # print(json.dumps(dat,indent=4))
        jobs_list=dat['jobs']

        for job in jobs_list:
            job_id=         job['id']
            job_name =      job['title']
            hash_id=        sha256_hex(str(job_id))
            current_jobs_id.append(hash_id)


            keywords = ["hiring manager", "hr", "recruiter"]
            hm_details = None

            for m in job.get("metadata") or []:
                if any(k in (m.get("name") or "").lower() for k in keywords):
                    v = m.get("value") or {}
                    hm_details = f"{v.get('name', '')}; {v.get('email', '')}".strip() or None
                    break

            job_deets=Job(
                job_id=         job_id,
                internal_job_id=job['internal_job_id'],
                job_name=       job_name,
                source=         self.name,
                location=       job['location']['name'],
                posted_date=    datetime.strptime(job['first_published'],FMT).strftime(DATE_FMT),
                updated_date =  datetime.strptime(job['updated_at'],FMT).strftime(DATE_FMT),
                url=            job['absolute_url'],
                hiring_manger=  hm_details
            )
            job_data[hash_id]=job_deets.to_dict()


        return  current_jobs_id,job_data

    def scrape_jd(self, source: dict=None):
        job_id=source['job_id']
        jd_url = self.base_domain + f"{self.name}/jobs/{job_id}"

        resp=self.session.get(jd_url, timeout=30)
        dat=resp.json()
        jd=dat['content']
        # print(json.dumps(dat,indent=4))

        return self.clean_html(jd)

