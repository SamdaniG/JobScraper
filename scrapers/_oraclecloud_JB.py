from scrapers.__base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
from datetime import datetime

FMT='%Y-%m-%d'
DATE_FMT = "%a %d-%b-%Y"

class OracleCloudScraper(ApiJobBoardScraper):
    name="oraclecloud"
    base_domain=""

    url = ''

    params = {}
    jd_url= ''

    def scrape_jobs(self):
        resp=rq.get(url=self.url,params=self.params)
        # print(resp)
        # print(resp.raise_for_status())
        current_jobs_id=[]
        job_data = {}

        dat = resp.json()
        job_list=dat['items'][0]['requisitionList']
        # print(json.dumps(job_list[0],indent=4))

        for job in job_list:
            # print(json.dumps(job,indent=4))
            hash_id = sha256_hex(job["Id"] + job["Title"] + job["PostedDate"])
            # print(hash_id)
            current_jobs_id.append(hash_id)
            job_deets=Job(
                job_name=job["Title"],
                job_id=     job["Id"],

                source=     self.name,
                work_policy=job.get("WorkplaceType") or None,
                location=   job['PrimaryLocation'],
                posted_date=datetime.strptime(job['PostedDate'],FMT).strftime(DATE_FMT),
                url=        f"{self.base_domain}/hcmUI/CandidateExperience/"
                f"en/sites/CX_1/job/{job['Id']}"
            )
            job_data[hash_id]=job_deets.to_dict()
            # print(job_data)
            # print(job_data[hash_id]['posted_date'])
            # print("************")

        return current_jobs_id, job_data

    def scrape_jd(self, source= dict):
        job_id=source["job_id"]
        jd_params = {
            "onlyData": "true",
            "expand": 'all',
            "finder": f'ById;Id="{job_id}",siteNumber=CX_1'
        }
        resp=rq.get(url=self.jd_url,params=jd_params)
        dat=resp.json()
        items=dat.get("items","")
        if items=="":
            return ""

        item=dat['items'][0]
        fields = [
            "ExternalQualificationsStr",
            "InternalQualificationsStr",
            "InternalResponsibilitiesStr",
            "ExternalDescriptionStr",
        ]

        raw_info = "\n\n".join(item.get(field, "") for field in fields)

        info = self.clean_html(raw_info)

        return info


