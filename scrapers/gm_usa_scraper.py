from scrapers._myworkday_JB import MyworkdayBase
import json
class GMUScraper(MyworkdayBase):
    name='gm_usa'
    base_domain= 'https://generalmotors.wd5.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/generalmotors/Careers_GM/jobs'

    payload = {
        "appliedFacets":
            {
                "Location_Country": ["bc33aa3152ec42d4995f4791a106ed09"]
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



if __name__=='__main__':
    test=GMUScraper()
    yolo_data=test.scrape_jobs()
    # print(json.dumps(yolo_data['093ebd0ddc'],indent=4))
    print(len(yolo_data))
    # print(yolo_data)
    print(json.dumps(yolo_data,indent=4))
    # job_names=[yolo_data[job]['job_name'] for job in yolo_data]
    # print(json.dumps(job_names,indent=4))
    # a=dict()

    # print(test.scrape_jd(source=yolo_data["5b09294d40"]))


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