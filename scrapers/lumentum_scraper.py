from scrapers.base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
import json
from utils import api_get_exact_posting_date


class LumentumScraper(ApiJobBoardScraper):
    name='lumentum'
    base_domain= 'https://lumentum.wd5.myworkdayjobs.com/'
    url = base_domain + 'wday/cxs/lumentum/LITE/jobs'

    payload={
        "appliedFacets":
             {"locations":
                  ["1fb4c923bb630100a0fa8c8bd49a0000","01232ead616f01726660254a6810e472"]},
         "limit":20,
         "offset":0,
         "searchText":""
    }

    jd_url = base_domain + 'wday/cxs/lumentum/LITE/job/'

    def scrape_jobs(self):
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
            # print(json.dumps(job_list[0],indent=4))

            for job in job_list:
                job_id=job["bulletFields"][0]
                job_title=job['title']
                hash_id= sha256_hex(job_id+job_title)
                current_jobs_id.append(hash_id)

                job_deets=Job(
                    job_name=   job_title,
                    job_id=     job_id,
                    source=     self.name,
                    location=   job['locationsText'],
                    posted_date=api_get_exact_posting_date(job['postedOn']),
                    url=        f"{self.base_domain}LITE{job['externalPath']}"
                )
                job_data[hash_id]=job_deets.to_dict()
                # job_data[hash_id]={
                #     'job_id' : job_id,
                #     'job_name': job_title,
                #     'source' : self.name,
                #     "location": job['locationsText'],
                #     "posted_date": api_get_exact_posting_date(job['postedOn']),#to be worked
                #     "filled_date": "",
                #     "url": f"{self.base_domain}LITE{job['externalPath']}"
                #
                # }

            if len(job_list) < self.payload['limit']:
                break

            offset += self.payload['limit']
        return current_jobs_id, job_data

    def scrape_jd(self, source:dict = None):
        final=source['url'].split('/LITE/job/')[-1]
        # print(f'{final=}')
        resp=rq.get(self.jd_url + final)
        # print(resp)
        dat=resp.json()
        jd=self.clean_html(dat['jobPostingInfo']['jobDescription'])

        return jd




if __name__=='__main__':
    test=LumentumScraper()
    yolo, yolo_data=test.scrape_jobs()
    # print(json.dumps(yolo_data,indent=4))
    a=dict()
    a["0863acf5a9"]= {
        "job_id": "2024989",
        "job_name": "Electrical Engineer/FPGA Designer",
        "source": "lumentum",
        "location": "Canada - Ottawa (Bill Leathem)",
        "posted_date": "Thu 01-Jan-2026",
        "filled_date": "",
        "url": "https://lumentum.wd5.myworkdayjobs.com/LITE/job/Canada---Ottawa-Bill-Leathem/Electrical-Engineer-FPGA-Designer_2024989"
    }
    # print(test.scrape_jd(source=a["0863acf5a9"]))

'''sample skeleton
{
    "title": "Optical Engineer Co-op/Intern Student",
    "externalPath": "/job/Canada---Ottawa-Bill-Leathem/Optical-Engineer-Co-op-Intern-Student_20251045",
    "locationsText": "Canada - Ottawa (Bill Leathem)",
    "postedOn": "Posted Yesterday",
    "bulletFields": [
        "20251045"
    ]
}
'''