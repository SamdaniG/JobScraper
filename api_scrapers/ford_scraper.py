import json

from api_scrapers.base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
import re
from datetime import datetime

FMT='%Y-%m-%d'
DATE_FMT = "%a %d-%b-%Y"

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
                work_policy=job['WorkplaceType'],
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



''' Sample structure
{
    "Id": "59456",
    "Title": "Senior Engineering Specialist",
    "PostedDate": "2026-02-27",
    "PostingEndDate": null,
    "Language": "US",
    "PrimaryLocationCountry": "CA",
    "GeographyId": 100000032213871,
    "HotJobFlag": false,
    "WorkplaceTypeCode": "ORA_ON_SITE",
    "JobFamily": null,
    "JobFunction": null,
    "WorkerType": null,
    "ContractType": null,
    "ManagerLevel": null,
    "JobSchedule": null,
    "JobShift": null,
    "JobType": null,
    "StudyLevel": null,
    "DomesticTravelRequired": null,
    "InternationalTravelRequired": null,
    "WorkDurationYears": null,
    "WorkDurationMonths": null,
    "WorkHours": null,
    "WorkDays": null,
    "LegalEmployer": null,
    "BusinessUnit": null,
    "Department": null,
    "Organization": null,
    "MediaThumbURL": null,
    "ShortDescriptionStr": "Senior Engineering Specialist",
    "PrimaryLocation": "Windsor, ON, Canada",
    "Distance": 1772150400000.0,
    "TrendingFlag": false,
    "BeFirstToApplyFlag": false,
    "Relevancy": 9,
    "WorkplaceType": "On-site",
    "ExternalQualificationsStr": null,
    "ExternalResponsibilitiesStr": null,
    "secondaryLocations": [],
    "otherWorkLocations": [],
    "workLocation": [
        {
            "LocationId": 300000005673716,
            "LocationName": "Windsor Engine Plant #1",
            "AddressLine1": "100 Henry Ford Centre Drive",
            "AddressLine2": "PO Box 1634 Stn a",
            "AddressLine3": null,
            "AddressLine4": null,
            "Building": "WEP",
            "TownOrCity": "Windsor",
            "PostalCode": "N9A 7E8",
            "Country": "CA",
            "Region1": "Ontario",
            "Region2": "ON",
            "Region3": null,
            "Latitude": 42.31785,
            "Longitude": -83.03387
        }
    ],
    "requisitionFlexFields": []
}

'''