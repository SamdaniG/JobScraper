from scrapers.__base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
from utils import api_get_exact_posting_date
import json

class MyworkdayBase(ApiJobBoardScraper):
    name='base'
    base_domain = ''
    url = ''
    payload = {}
    jd_url = ''
    url_lang=''

    def scrape_jobs(self):
        current_jobs_id=[]
        job_data = {}
        offset = 0

        while True:
            payload = {
                **self.payload,
                "offset": offset
            }

            resp=rq.post(url=self.url, json= payload, timeout=30)
            # print(resp.raise_for_status())
            # print(resp.text)
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
        resp=rq.get(final, timeout=30)
        # print(resp)
        dat=resp.json()
        jd=self.clean_html(dat['jobPostingInfo']['jobDescription'])

        return jd
