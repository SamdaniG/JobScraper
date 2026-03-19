from scrapers._myworkday_JB import MyworkdayBase
import json

class HondaScraper(MyworkdayBase):
    name='honda'
    base_domain = 'https://ch.wd3.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/ch/Honda_Canada/jobs'

    payload = {
        'appliedFacets': {},
        'limit': 20,
        'offset': 0,
        'searchText': ""
    }
    #https://ch.wd3.myworkdayjobs.com/wday/cxs/ch/Honda_Canada/job/Markham-Ontario/Specialist--Contract---Sourcing_R1171
    # base_domain + /wday/cxs/ch/Honda_Canada + externalPath
    jd_url = base_domain + '/wday/cxs/ch/Honda_Canada'

    #applying url
    #https://ch.wd3.myworkdayjobs.com/en-US/Honda_Canada/job/Markham-Ontario/Specialist--Contract---Sourcing_R1171
    #base domain + /en-US/Honda_Canada + externalPath
    url_lang='/en-US/Honda_Canada'

if __name__=='__main__':
    test=HondaScraper()
    yo, yolo = test.scrape_jobs()
    # print(yo)
    print(json.dumps(yolo,indent=4))
    # print(test.scrape_jd(source= yolo['ace5ac7b6c']))

'''Sample Skeleton
    {
        "title": "Specialist, Contract & Sourcing",
        "externalPath": "/job/Markham-Ontario/Specialist--Contract---Sourcing_R1171",
        "locationsText": "Markham, Ontario",
        "postedOn": "Posted 9 Days Ago",
        "bulletFields": [
            "R1171"
        ]
    }'''