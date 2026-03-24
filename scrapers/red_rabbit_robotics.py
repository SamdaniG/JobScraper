import json
from utils import sha256_hex
from scrapers.__base import ApiJobBoardScraper, Job
from datetime import datetime

FMT='%Y-%m-%dT%H:%M:%S.%f%z'
DATE_FMT = "%a %d-%b-%Y"
class RedRabbitRoboticsScraper(ApiJobBoardScraper):
    name='redrabbitrobotics'

    company_slug = 'red-rabbit-robotics'
    base_domain = f'https://apply.workable.com/'
    url = base_domain + f'api/v3/accounts/{company_slug}/jobs'

    #https://apply.workable.com/api/v2/accounts/red-rabbit-robotics/jobs/5B8938477D
    jd_url = base_domain + f'api/v2/accounts/{company_slug}/jobs/'

    def scrape_jobs(self, **kwargs):
        job_data={}

        resp = self.session.post(url= self.url,
                                 timeout=30)
        # print(resp.raise_for_status())
        dat=resp.json()
        # print(json.dumps(dat,indent=4))
        job_list=dat.get('results',"")

        for job in job_list:
            job_id=     job.get('id')
            hash_id=    sha256_hex(str(job_id))

            job_deets=Job(
                job_id=         job_id,
                job_name=       job.get('title'),
                source=         self.name,
                posted_date=    datetime.strptime(job.get('published', ''), FMT).strftime(DATE_FMT),
                url=            f'{self.base_domain}{self.company_slug}/j/{job.get("shortcode")}',
                work_policy=    job.get('workplace'),
                location=       '; '.join(f'{x.get('city')}, {x.get('region')}' for x in job.get('locations',{}))
            )

            job_data[hash_id]=job_deets.to_dict()

        return job_data

    def scrape_jd(self, source: dict=None):
        shortcode =             source.get('url').split('/j/')[1]
        # print(shortcode)
        jd_url=                   self.jd_url + shortcode
        resp=               self.session.get(url=jd_url)
        # print(resp.raise_for_status())
        dat=                resp.json()
        jd=                 dat.get('description',"") + dat.get('requirements',"")

        return self.clean_html(jd)


if __name__=='__main__':
    test=RedRabbitRoboticsScraper()
    yol=test.scrape_jobs()
    # print(json.dumps(yol,indent=4))
    print(test.scrape_jd(yol['955c683604']))