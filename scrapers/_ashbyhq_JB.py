import json

from scrapers.__base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex


class AshbyhqBase(ApiJobBoardScraper):
    name = 'base'
    base_domain = 'https://jobs.ashbyhq.com/'
    url = base_domain + 'api/non-user-graphql'
    jobBoard = 'ashbyhq'
    base_active = True
    company_active = True

    url_params={
        'op': 'ApiJobBoardWithTeams'
    }
    jd_params={
        'op' :    'ApiJobPosting'
    }
    url_name=''
    @property
    def apply_url(self):
        return self.base_domain + f'{self.url_name}/'

    jd_payload={}
    url_payload = {}

    def scrape_jobs(self, **kwargs):
        # current_jobs_id=[]
        job_data = {}

        resp=self.session.post(url= self.url,
                     params=self.url_params,
                     json= self.url_payload, timeout=30)

        dat=resp.json()
        # print(json.dumps(dat,indent=4))
        job_list= dat['data']['jobBoard']['jobPostings']
        # print(json.dumps( job_list[0],indent=4))

        for job in job_list:
            job_id=job['id']
            hash_id=sha256_hex(job_id)
            # current_jobs_id.append(hash_id)

            secondary = job.get("secondaryLocations")

            secondary_loc = (
                ", ".join(x["locationName"].strip() for x in secondary)
                if secondary
                else None
            )

            job_deets= Job(
                job_id =                job_id,
                job_name=               job['title'],
                source=                 self.name,
                location=               job['locationName'],
                secondary_loc=          secondary_loc,
                posted_date=            job.get('posted_date',None),
                url =                   self.apply_url + job_id,
                work_policy=            job['employmentType'],
                comp=                   job['compensationTierSummary'],
                job_board=              self.jobBoard

            )
            job_data[hash_id]=job_deets.to_dict()

        return job_data

    def scrape_jd(self, source: dict=None):
        job_id=source['job_id']
        self.jd_payload['variables']['jobPostingId']=job_id
        # print(json.dumps(self.jd_payload, indent=4))
        resp=   self.session.post(self.url,
                        params=     self.jd_params,
                        json=       self.jd_payload, timeout=30)
        # print(resp.raise_for_status())
        dat=resp.json()
        # print(json.dumps(dat,indent=4))
        jd=dat['data'].get('jobPosting',{}).get('descriptionHtml',"Not Available")

        return self.clean_html(jd)

