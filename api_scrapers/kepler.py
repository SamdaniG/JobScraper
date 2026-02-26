from api_scrapers.base import ApiJobBoardScraper
import requests as rq
from utils import sha256_hex
from datetime import datetime

DATE_FMT = "%a %d-%b-%Y"

class KeplerScraper(ApiJobBoardScraper):
    name='kepler'
    base_domain = 'https://api.lever.co/v0/postings/kepler'
    param = {
        'mode':'json',
        'location': 'Toronto, Ontario'
    }


    def scrape_jobs(self, driver=None):
        current_jobs_id=[]
        job_data={}

        resp=rq.get(url=self.base_domain, params= self.param)
        resp.raise_for_status()
        job_list=resp.json()

        for job in job_list:
            job_id=job['id']
            job_title=job['text']
            hash_id=sha256_hex(job_id+job_title)
            current_jobs_id.append(hash_id)

            job_data[hash_id]={
                'job_id': job_id,
                'job_name': job_title,
                'source': self.name,
                'location': job['categories']['location'],
                'posted_date':(datetime.fromtimestamp(job['createdAt'] / 1000)).strftime(DATE_FMT),
                'filled_date':"",
                'url':job['hostedUrl']
            }

        return current_jobs_id, job_data

    def scrape_jd(self, driver=None, source:dict=None):
        job_id = source['job_id']

        resp = rq.get(
            url=f"{self.base_domain}/{job_id}",
            params={'mode': 'json'}
        )
        resp.raise_for_status()

        data = resp.json()
        sections = []

        # Main description (HTML)
        if data.get("description"):
            sections.append(data["description"])

        # Structured blocks
        for block in data.get("lists", []):
            if block.get("text"):
                sections.append(block["text"])
            if block.get("content"):
                sections.append(block["content"])

        jd = "\n".join(sections)

        return self.clean_html(jd)

if __name__=='__main__':
    test=KeplerScraper()
    yo,yol = test.scrape_jobs()
    # print(yo[0])
    # print(yol)
    # 79c709d47c
    jd_test=test.scrape_jd(source=yol['79c709d47c'])
    print(jd_test)



