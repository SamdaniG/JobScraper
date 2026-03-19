from scrapers._myworkday_JB import MyworkdayBase

class KionGroupScraper(MyworkdayBase):
    name='kiongroup'
    base_domain = 'https://kiongroup.wd3.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/kiongroup/KION_SCS/jobs'

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
    jd_url = base_domain + '/wday/cxs/kiongroup/KION_SCS'
    url_lang ='/en-US/KION_SCS'

if __name__=='__main__':
    test=KionGroupScraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    print(yol)
    print(test.scrape_jd(yol['66e3e54e63']))