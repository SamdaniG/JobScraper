from api_scrapers.base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
import json
from utils import api_get_exact_posting_date


class GMScraper(ApiJobBoardScraper):
    name='gm_api'
    base_domain= 'https://generalmotors.wd5.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/generalmotors/Careers_GM/jobs'

    payload = {
        "appliedFacets":
            {
                "Location_Country": ["a30a87ed25634629aa6c3958aa2b91ea"]
            },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    #application path
    #base_domain + /en-GB/Careers_GM + externalPath
    #https://generalmotors.wd5.myworkdayjobs.com/wday/cxs/generalmotors/Careers_GM/ + externalPath
    jd_url = base_domain + '/wday/cxs/generalmotors/Careers_GM'
    url_lang='/en-US/Careers_GM'

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
            # print(json.dumps(job_list[0],indent=4))

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
                    work_policy=        job.get('remoteType',"")
                )
                job_data[hash_id]=job_deets.to_dict()


            if len(job_list) < self.payload['limit']:
                break

            offset += self.payload['limit']
        return current_jobs_id, job_data

    def scrape_jd(self,driver=None, source:dict = None):
        # final=source['url'].split('/LITE/job/')[-1]
        # print(f'{final=}')
        final = self.jd_url + source['url'].split(self.url_lang)[1]
        resp=rq.get(final)
        # print(resp)
        dat=resp.json()
        jd=self.clean_html(dat['jobPostingInfo']['jobDescription'])

        return jd




if __name__=='__main__':
    test=GMScraper()
    yolo, yolo_data=test.scrape_jobs()
    # print(json.dumps(yolo_data['093ebd0ddc'],indent=4))
    print(yolo_data)
    a=dict()

    # print(test.scrape_jd(source=yolo_data["093ebd0ddc"]))


'''Sample Skeleton
{
    "title": "Senior Software Developer, Body Systems",
    "externalPath": "/job/Markham-Ontario-Canada/Senior-Software-Developer--Body-Systems_JR-202518139",
    "locationsText": "2 Locations",
    "postedOn": "Posted 30+ Days Ago",
    "remoteType": "Hybrid",
    "bulletFields": [
        "JR-202518139"
    ]
}
'''