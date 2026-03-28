from scrapers.__base import ApiJobBoardScraper, Job
import json
from utils import sha256_hex
from datetime import datetime

FMT='%Y-%m-%dT%H:%M:%S.%f%z'
DATE_FMT = "%a %d-%b-%Y"

class GeneralDynamicsScraper(ApiJobBoardScraper):
    name = 'general dynamics'
    job_slug = 'GDMSI'
    params ={
        'country' : 'ca'
    }
    @property
    def url(self):
        return f'https://api.smartrecruiters.com/v1/companies/{self.job_slug}/postings'

    apply_url = f'https://jobs.smartrecruiters.com/{job_slug}/'
    jobBoard = 'general_dynamics'

    def scrape_jobs(self, **kwargs):
        job_data = {}

        resp = self.session.get(url= self.url, params= self.params)
        # print(resp.raise_for_status())
        dat = resp.json()
        # print(json.dumps( dat, indent=4))
        jobs_list=dat.get('content',[])

        for job in jobs_list:
            job_id =        job.get('id')
            job_name=       job.get('name')
            hash_id=        sha256_hex(job_id)

            job_deets=Job(
                job_id=         job_id,
                job_name=       job_name,
                source=         self.name,
                location=       job.get('location',{}).get('fullLocation',{}),
                posted_date=    datetime.strptime(job.get('releasedDate', ''),FMT).strftime(DATE_FMT),
                url=            f'{self.apply_url}{job_id}',
                job_board=      self.jobBoard
            )
            job_data[hash_id]=job_deets.to_dict()

        return job_data




    def scrape_jd(self, source: dict=None):
        job_id=source.get('job_id')
        resp=self.session.get(url = f'{self.url}/{job_id}')
        # print(resp.raise_for_status())
        dat=resp.json()
        # print(json.dumps(dat, indent=4))
        jd_list = dat.get('jobAd', {}).get('sections', {})
        jd = '\n'.join(value.get('text', "") for key, value in jd_list.items())

        return self.clean_html(jd)

        # pass

if __name__=='__main__':
    test=GeneralDynamicsScraper()
    yo,yol = test.scrape_jobs()
    print(yo)
    print(json.dumps(yol,indent=4))
    print(test.scrape_jd(yol['a02dac47ab']))


"""
{
    "id": "744000114856507",
    "name": "Junior Hardware Engineering Developer ",
    "uuid": "289a5c18-0906-4df7-a416-c2877e3434f6",
    "jobAdId": "8faab9df-0a75-48cd-b028-c3e4d49259e0",
    "defaultJobAd": true,
    "refNumber": "REF1162U",
    "company": {
        "identifier": "GDMSI",
        "name": "General Dynamics Missions System International"
    },
    "releasedDate": "2026-03-15T18:37:49.976Z",
    "location": {
        "city": "Ottawa",
        "region": "ON",
        "country": "ca",
        "address": "1941 Robertson Road",
        "postalCode": "K2H 5B7",
        "remote": false,
        "hybrid": true,
        "latitude": "45.3281309",
        "longitude": "-75.8259704",
        "fullLocation": "Ottawa, ON, Canada"
    },
    "industry": {
        "id": "defense_and_space",
        "label": "Defense And Space"
    },
    "department": {},
    "function": {
        "id": "engineering",
        "label": "Engineering"
    },
    "typeOfEmployment": {
        "id": "permanent",
        "label": "Full-time"
    },
    "experienceLevel": {
        "id": "entry_level",
        "label": "Entry Level"
    },
    "customField": [
        {
            "fieldId": "64791a5d4769c1356cbdf914",
            "fieldLabel": "Employment Type",
            "valueId": "444fc188-f89b-4404-acfe-0499dfd18f85",
            "valueLabel": "Fulltime-Regular"
        },
        {
            "fieldId": "653a9d0277e2434834993067",
            "fieldLabel": "Work Group",
            "valueId": "0c5d82d6-937a-41f6-a06d-a28c3684f68a",
            "valueLabel": "SEAC"
        },
        {
            "fieldId": "640efc2ab8145a4e44523d82",
            "fieldLabel": "Brands",
            "valueId": "0fbdf90a-9775-460d-93fb-0366a1b1519c",
            "valueLabel": "General Dynamics Mission Systems - Canada"
        },
        {
            "fieldId": "COUNTRY",
            "fieldLabel": "Country/Region",
            "valueId": "ca",
            "valueLabel": "Canada"
        },
        {
            "fieldId": "64791bf1671abc67852f856f",
            "fieldLabel": "Number of Openings",
            "valueLabel": "1"
        }
    ],
    "visibility": "PUBLIC",
    "ref": "https://api.smartrecruiters.com/v1/companies/GDMSI/postings/744000114856507",
    "language": {
        "code": "en",
        "label": "English",
        "labelNative": "English (US)"
    }
}
"""