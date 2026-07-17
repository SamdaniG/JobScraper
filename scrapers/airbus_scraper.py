from scrapers._myworkday_JB import MyworkdayBase

class AirbusScraper(MyworkdayBase):
    name='airbus'
    base_domain = 'https://ag.wd3.myworkdayjobs.com'
    url = base_domain +  '/wday/cxs/ag/Airbus/jobs'

    payload = {
        # 'locationCountry': ["a30a87ed25634629aa6c3958aa2b91ea"],
        "appliedFacets":
            {
                "locationCountry": ["a30a87ed25634629aa6c3958aa2b91ea"]
            },
        'limit': 20,
        'offset': 0,
        'searchText': ""
    }
    jd_url = base_domain + '/wday/cxs/ag/Airbus'
    url_lang ='/en-US/Airbus'

if __name__=='__main__':
    test=AirbusScraper()
    yol=test.scrape_jobs()
    # print(yo)
    # print(yol)
    print(test.scrape_jd(yol['ccc41cce97']))