import datetime
import json

from scrapers.__base import ApiJobBoardScraper,Job
import requests as rq
from utils import sha256_hex
from datetime import datetime

FMT='%Y-%m-%d'
DATE_FMT = "%a %d-%b-%Y"

class ZTRScraper(ApiJobBoardScraper):
    base_domain='https://ztr.bamboohr.com/careers/'
    url = base_domain + 'list/'
    name = 'ztr'


    def scrape_jobs(self, **kwargs):
        current_jobs_id=[]
        job_data={}

        resp=rq.get(url= self.url)
        # print(resp.raise_for_status())
        dat=resp.json()
        job_list=dat['result']
        # print(json.dumps(job_list[0], indent=4))
        for job in job_list:
            job_id=             job['id']
            job_name=           job["jobOpeningName"]
            hash_id=sha256_hex(job_id + job_name)
            current_jobs_id.append(hash_id)

            job_deets=Job(
                job_id=             job_id,
                job_name=           job_name,
                source=             self.name,
                location=           job['location']['city'],
                posted_date=        "",#self.scrape_posted_date(job_id),
                url=                self.base_domain + job_id,
            )
            job_data[hash_id]=job_deets.to_dict()

        return current_jobs_id, job_data

    def scrape_posted_date(self,job_id):
        # id=source['job_id']
        jd_url= self.base_domain + job_id +'/detail'
        resp=rq.get(jd_url)
        # resp.raise_for_status()

        data=resp.json()
        date_=data['result']['jobOpening']['datePosted']
        date_=datetime.strptime(date_,FMT).strftime(DATE_FMT)

        # print(json.dumps(data,indent=4))

        return date_


    def scrape_jd(self, source: dict=None):
        id=source['job_id']
        jd_url= self.base_domain + id +'/detail'
        resp=rq.get(jd_url)
        resp.raise_for_status()

        data=resp.json()
        # print(data)
        jd=data['result']['jobOpening']['description']


        # print(json.dumps(data,indent=4))

        return self.clean_html(jd)

if __name__=='__main__':
    test=ZTRScraper()

    yo,yol=test.scrape_jobs()
    print(yo)
    print(yol)
    # print(yol['844354a354'])
    print(test.scrape_jd(yol['844354a354']))



'''Sample skeleton
{
    "id": "232",
    "jobOpeningName": "Electrical Technologist",
    "departmentId": "19011",
    "departmentLabel": "Canada",
    "employmentStatusLabel": "Full-Time",
    "location": {
        "city": "London",
        "state": "Ontario"
    },
    "atsLocation": {
        "country": null,
        "state": null,
        "province": null,
        "city": null
    },
    "isRemote": null,
    "locationType": "0"
}
'''