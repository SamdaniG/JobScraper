from api_scrapers.base import ApiJobBoardScraper
import requests as rq
from utils import sha256_hex
import re

class FordScraper(ApiJobBoardScraper):
    name="ford"
    base_domain="https://efds.fa.em5.oraclecloud.com"

    url = (base_domain +
           "/hcmRestApi/resources/latest/recruitingCEJobRequisitions")

    params = {
        "onlyData": "true",
        "expand": "requisitionList.workLocation,"
                  "requisitionList.otherWorkLocations,"
                  "requisitionList.secondaryLocations,"
                  "flexFieldsFacet.values,"
                  "requisitionList.requisitionFlexFields",
        "finder": (
            "findReqs;"
            "siteNumber=CX_1,"
            "facetsList=LOCATIONS;WORK_LOCATIONS;WORKPLACE_TYPES;"
            "TITLES;CATEGORIES;ORGANIZATIONS;POSTING_DATES;FLEX_FIELDS,"
            "limit=100,"
            "lastSelectedFacet=LOCATIONS,"
            "selectedLocationsFacet=300000000425151,"
            "sortBy=POSTING_DATES_DESC"
        )
    }
    jd_url= (base_domain +
       "/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails")

    # def clean_html(self, html_text) -> str:
    #     if not html_text:
    #         return ""
    #     return re.sub(r"<.*?>", "", html_text)

    def scrape_jobs(self, driver = None):
        resp=rq.get(url=self.url,params=self.params)
        # print(resp)
        # print(resp.raise_for_status())
        current_jobs_id=[]
        job_data = {}

        dat = resp.json()
        job_list=dat['items'][0]['requisitionList']

        for job in job_list:
            # print(json.dumps(job,indent=4))
            hash_id = sha256_hex(job["Id"] + job["Title"] + job["PostedDate"])
            # print(hash_id)
            current_jobs_id.append(hash_id)
            #
            # apply_url = (
            #     f"{self.base_domain}/hcmUI/CandidateExperience/"
            #     f"en/sites/CX_1/job/{job_id}"
            # )

            job_data[hash_id] = {
                "job_id": job["Id"],
                "job_name": job["Title"],
                "source": self.name,
                "work_policy": job["WorkplaceType"],
                "location": job['PrimaryLocation'],
                "posted_date": job['PostedDate'],
                "filled_date": "",
                "url": f"{self.base_domain}/hcmUI/CandidateExperience/"
                f"en/sites/CX_1/job/{job['Id']}"
            }
            # print(job_data)
            # print("************")

        return current_jobs_id, job_data

    def scrape_jd(self,driver=None, source= dict):
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
        # info = (
        #         item.get("ExternalQualificationsStr","") + "\n\n" +
        #         item.get("InternalQualificationsStr","") + "\n\n" +
        #         item.get("InternalResponsibilitiesStr","") + "\n\n" +
        #         item.get("ExternalDescriptionStr","")
        #         )
        #
        # return info

        fields = [
            "ExternalQualificationsStr",
            "InternalQualificationsStr",
            "InternalResponsibilitiesStr",
            "ExternalDescriptionStr",
        ]

        raw_info = "\n\n".join(item.get(field, "") for field in fields)

        info = self.clean_html(raw_info)

        return info



if __name__=='__main__':
    test=FordScraper()
    test.scrape_jobs()
