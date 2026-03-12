from scrapers._myworkday_JB import MyworkdayBase
import json
class CaterpillarScraper(MyworkdayBase):
    name='caterpillar'
    base_domain= 'https://cat.wd5.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/cat/CaterpillarCareers/jobs'

    payload = {
        "appliedFacets":
            {
                "locationCountry": ["a30a87ed25634629aa6c3958aa2b91ea"]
            },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    #application path
    #base_domain + /en-GB/Careers_GM + externalPath
    #https://generalmotors.wd5.myworkdayjobs.com/wday/cxs/generalmotors/Careers_GM/ + externalPath
    jd_url = base_domain + '/wday/cxs/cat/CaterpillarCareers'
    url_lang='/en-US/CaterpillarCareers'



if __name__=='__main__':
    test=CaterpillarScraper()
    yolo, yolo_data=test.scrape_jobs()
    # print(json.dumps(yolo_data['093ebd0ddc'],indent=4))
    # print(yolo)
    # print(yolo_data)
    print(json.dumps(yolo_data,indent=4))
    # job_names=[yolo_data[job]['job_name'] for job in yolo_data]
    # print(json.dumps(job_names,indent=4))
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