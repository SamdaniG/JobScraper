from scrapers._myworkday_JB import MyworkdayBase
import json

class LumentumScraper(MyworkdayBase):
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

if __name__=='__main__':
    test=LumentumScraper()
    yolo, yolo_data=test.scrape_jobs()
    print(json.dumps(yolo_data,indent=4))
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