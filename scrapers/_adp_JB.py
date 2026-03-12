from scrapers.__base import ApiJobBoardScraper,Job
import requests as rq
import json
from utils import sha256_hex
from datetime import datetime

FMT='%Y-%m-%dT%H:%M:%S.%f%z'
DATE_FMT = "%a %d-%b-%Y"

class ADPBase(ApiJobBoardScraper):
    name= 'base'
    base_domain = 'https://workforcenow.adp.com/mascsr/default'
    url = base_domain + '/careercenter/public/events/staffing/v1/job-requisitions'
    # params = {
    #     'cid': '',
    #     "lang": "en_CA",
    #     "locale": "en_CA",
    #     '$top': 100
    # }
    params={}
    @property
    def apply_url(self):
        return (self.base_domain +
                f'/mdf/recruitment/recruitment.html?cid={self.params['cid']}&jobId=')

    def scrape_jobs(self, **kwargs):
        current_jobs_id=[]
        job_data = {}
        resp=self.session.get(url=self.url,params=self.params, timeout=30)
        # print(resp.raise_for_status())
        dat=resp.json()

        jobs_list=dat['jobRequisitions']
        # print(json.dumps(jobs_list[0], indent=4))

        for job in jobs_list:
            job_id =                job['itemID']
            job_name=               job.get('requisitionTitle',"")
            hash_id=                sha256_hex(job_id)
            current_jobs_id.append(hash_id)
            application_id = job['customFieldGroup']['stringFields'][0]['stringValue']
            # safe location extraction
            loc = job.get('requisitionLocations') or []
            if loc:
                addr = loc[0].get('address', {})
                location = f"{addr.get('cityName','')} {addr.get('countrySubdivisionLevel1',{}).get('codeValue','')}"
            else:
                location = ""

            job_deets = Job(
                job_id=job_id,
                job_name=job_name,
                source=self.name,
                work_policy=job.get('workLevelCode', {}).get('shortName', None),
                location=location,
                posted_date=datetime.strptime(job.get('postDate', ''),FMT).strftime(DATE_FMT),
                url= self.apply_url + application_id
            )

            job_data[hash_id] = job_deets.to_dict()

        return current_jobs_id, job_data

    def scrape_jd(self, source: dict = None):
        job_id = source["job_id"]
        url = f"{self.url}/{job_id}"
        resp = self.session.get(url,self.params, timeout=30)
        dat = resp.json()
        print(dat)
        jd = dat.get("jobDescription", "")

        return self.clean_html(jd)