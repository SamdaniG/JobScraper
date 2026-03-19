from scrapers.__base import ApiJobBoardScraper,Job
import requests as rq
import json
from utils import sha256_hex


class ATSRippling(ApiJobBoardScraper):
    name = 'base'
    base_domain = 'https://ats.rippling.com/api/v2/board/'
    jobBoardSlug = ''

    @property
    def url(self):
        return f'{self.base_domain}{self.jobBoardSlug}/jobs'

    params = {
        # city
    'country': 'CA',
    'groupJobsByLocation': 'true',
    'page':    0,
    'pageSize':    20,
    # searchQuery
    # state
    # workplaceType
    }

    def scrape_jobs(self, **kwargs):
        # current_jobs_id=[]
        job_data = {}
        resp=self.session.get(url=self.url,params=self.params, timeout=30)
        # print(resp.raise_for_status())
        dat=resp.json()
        # print(json.dumps(dat,indent=4))

        jobs_list=dat['items']

        for job in jobs_list:
            job_id =            job.get('id',"")
            job_name =          job.get('name',"")
            hash_id=            sha256_hex(job_id)
            # current_jobs_id.append(hash_id)

            job_deets= Job(
                job_id=         job_id,
                job_name=       job_name,
                source=         self.name,
                work_policy=    '; '.join([x.get('workplaceType','') for x in job.get('locations',[])]),
                location=       '; '.join([x.get('name','') for x in job.get('locations',[])]),
                url=            job.get('url',''),
                posted_date=    ''
            )

            job_data[hash_id]=job_deets.to_dict()

        return job_data


    def scrape_jd(self, source: dict=None):
        job_id = source['job_id']
        jd_url= self.url + f'/{job_id}'
        resp=self.session.get(url=jd_url, timeout=30)
        # print(resp.raise_for_status())
        dat=resp.json()
        # print(json.dumps(dat,indent=4))

        jd = (dat.get('description',[]).get('company',"") +
              dat.get('description', []).get('role', ""))
        # print(json.dumps(jd,indent=4))

        return self.clean_html(jd)



