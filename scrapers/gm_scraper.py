from scrapers._myworkday_JB import MyworkdayBase
import json
class GMScraper(MyworkdayBase):
    name='gm'
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



if __name__=='__main__':
    test=GMScraper()
    yolo, yolo_data=test.scrape_jobs()
    # print(json.dumps(yolo_data['093ebd0ddc'],indent=4))
    # print(len(yolo))
    # print(json.dumps(yolo_data,indent=4))
    job_names=[yolo_data[job]['job_name'] for job in yolo_data]
    print(json.dumps(job_names,indent=4))
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