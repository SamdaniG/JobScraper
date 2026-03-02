from scrapers.base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
import json
from utils import api_get_exact_posting_date


class HondaScraper(ApiJobBoardScraper):
    name='honda'
    base_domain = 'https://ch.wd3.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/ch/Honda_Canada/jobs'

    payload = {
        'appliedFacets': {},
        'limit': 20,
        'offset': 0,
        'searchText': ""
    }
    #https://ch.wd3.myworkdayjobs.com/wday/cxs/ch/Honda_Canada/job/Markham-Ontario/Specialist--Contract---Sourcing_R1171
    # base_domain + /wday/cxs/ch/Honda_Canada + externalPath
    jd_url = base_domain + '/wday/cxs/ch/Honda_Canada'

    #applying url
    #https://ch.wd3.myworkdayjobs.com/en-US/Honda_Canada/job/Markham-Ontario/Specialist--Contract---Sourcing_R1171
    #base domain + /en-US/Honda_Canada + externalPath
    url_lang='/en-US/Honda_Canada'

    def scrape_jobs(self, driver= None):
        current_jobs_id=[]
        job_data = {}
        offset = 0

        while True:
            payload = {
                **self.payload,
                "offset": offset
            }

            resp=rq.post(url=self.url, json= payload)
            # print(resp.raise_for_status())
            # print(resp)
            dat=resp.json()
            job_list=dat.get('jobPostings', [])
            # print(json.dumps(job_list,indent=4))

            for job in job_list:
                path=job.get('externalPath', 0)
                if path==0:
                    continue
                url = self.base_domain + self.url_lang + job['externalPath']
                job_id=                 job.get('bulletFields',"00")[0]
                job_title=              job.get('title',"")
                hash_id= sha256_hex(url)
                current_jobs_id.append(hash_id)

                job_deets=Job(
                    job_name=   job_title,
                    job_id=     job_id,
                    source=     self.name,
                    location=           job.get('locationsText',""),
                    posted_date=        api_get_exact_posting_date(job['postedOn']),
                    url=        url,
                    # work_policy=        job.get('remoteType',"")
                )
                job_data[hash_id]=job_deets.to_dict()


            if len(job_list) < self.payload['limit']:
                break

            offset += self.payload['limit']
        return current_jobs_id, job_data

    def scrape_jd(self, source:dict = None):
        # final=source['url'].split('/LITE/job/')[-1]
        # print(f'{final=}')
        final = self.jd_url + source['url'].split(self.url_lang)[1]
        resp=rq.get(final)
        # print(resp)
        dat=resp.json()
        jd=self.clean_html(dat['jobPostingInfo']['jobDescription'])

        return jd

if __name__=='__main__':
    test=HondaScraper()
    yo, yolo = test.scrape_jobs()
    print(yo)
    # print(json.dumps(yolo,indent=4))
    print(test.scrape_jd(source= yolo['ace5ac7b6c']))

'''Sample Skeleton
    {
        "title": "Specialist, Contract & Sourcing",
        "externalPath": "/job/Markham-Ontario/Specialist--Contract---Sourcing_R1171",
        "locationsText": "Markham, Ontario",
        "postedOn": "Posted 9 Days Ago",
        "bulletFields": [
            "R1171"
        ]
    }'''