from datetime import datetime
from pprint import pprint

from scrapers.base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
import json
from utils import api_get_exact_posting_date

DATE_FMT = "%a %d-%b-%Y"

class TrimbleScraper(ApiJobBoardScraper):
    name='trimble'
    base_domain= 'https://trimble.eightfold.ai'
    url = base_domain + '/api/pcsx/search'
    params = {
        'domain' : 'trimble.com',
        # query =
        'location' : 'Canada',
        'start' : 0,
        'sort_by' : 'distance',
        'filter_include_remote' : 1
    }
    jd_url = base_domain + '/api/pcsx/position_details'
    jd_params={
        'position_id' : 'sample',
        'domain' : 'trimble.com',
        'hl' : 'en'
    }

    def scrape_jobs(self, **kwargs):
        current_jobs_id=[]
        job_data = {}

        resp=rq.get(url=self.url,params=self.params)
        # print(resp.raise_for_status())
        dat=resp.json()
        # print(json.dumps(dat,indent=4))
        job_list=dat['data']['positions']
        # pprint(job_list)
        for job in job_list:
            job_id=             job['atsJobId']
            job_name=           job['name']
            hash_id=            sha256_hex(job_id)
            current_jobs_id.append(hash_id)
            job_deets=Job(
                job_name=           job_name,
                job_id=             job_id,
                source=             self.name,
                location=           "; ".join(job["locations"]),
                posted_date=        datetime.fromtimestamp(job['postedTs']).strftime(DATE_FMT),
                creation_date=      datetime.fromtimestamp(job['creationTs']).strftime(DATE_FMT),
                url=                self.base_domain + job['positionUrl']
            )
            job_data[hash_id]=job_deets.to_dict()

        return current_jobs_id, job_data

    def scrape_jd(self, source: dict=None):
        jd_params= self.jd_params
        jd_params['position_id']=source['url'].split('job/')[1]
        # print(jd_params)
        resp = rq.get(
            url=self.jd_url,
            params=jd_params
        )
        # print(resp.raise_for_status())

        dat = resp.json()
        # print(json.dumps(dat,indent=4))
        jd=dat['data']['jobDescription']


        return self.clean_html(jd)

if __name__=='__main__':
    test=TrimbleScraper()
    yo,yol=test.scrape_jobs()
    # print(yo)
    # print(json.dumps(yol,indent=4))

    # print(test.scrape_jd(yol['5b91f632e7']))


'''Sample Skeleton
{'atsJobId': 'R53402',
  'creationTs': 1765324800,
  'department': 'Sales Accounts',
  'displayJobId': 'R53402',
  'id': 171837903639,
  'isHot': 0,
  'locationFlexibility': None,
  'locations': ['Canada - Remote'],
  'name': 'Sales Manager, Canada',
  'positionUrl': '/careers/job/171837903639',
  'postedTs': 1765756800,
  'solrScore': None,
  'standardizedLocations': ['CA'],
  'stars': 0,
  'workLocationOption': 'onsite'}
'''