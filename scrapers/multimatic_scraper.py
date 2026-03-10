from scrapers._myworkday_JB import MyworkdayBase

class MultimaticScraper(MyworkdayBase):
    name='multimatic'
    base_domain = 'https://multimatic.wd10.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/multimatic/MMEC/jobs'

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

    jd_url = base_domain + '/wday/cxs/multimatic/MMEC'

    url_lang ='/en-US/MMEC'

if __name__=='__main__':
    test=MultimaticScraper()
    yo,yol = test.scrape_jobs()
    print(yo)
    # print(len(yo))
    # print(yol)
    print(test.scrape_jd(yol['216575625f']))