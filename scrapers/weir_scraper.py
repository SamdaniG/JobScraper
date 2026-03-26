import json

from scrapers._myworkday_JB import MyworkdayBase

class WeirScraper(MyworkdayBase):
    name='weir'
    base_domain = 'https://weir.wd3.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/weir/Weir_External_Careers/jobs'

    payload = {
        # 'locationCountry': ["a30a87ed25634629aa6c3958aa2b91ea"],
        "appliedFacets":
            {
                "Country": ["a30a87ed25634629aa6c3958aa2b91ea"]
            },
        'limit': 20,
        'offset': 0,
        'searchText': ""
    }
    jd_url = base_domain + '/wday/cxs/weir/Weir_External_Careers'
    url_lang ='/en-US/Weir_External_Careers'

if __name__=='__main__':
    test=WeirScraper()
    yol=test.scrape_jobs()
    # print(yo)
    print(len(yol))
    print(json.dumps(yol,indent=4))
    # print(test.scrape_jd(yol['66e3e54e63']))