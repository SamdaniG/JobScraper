from scrapers._myworkday_JB import MyworkdayBase

class NavCanadaScraper(MyworkdayBase):
    name='navcanada'
    base_domain = 'https://navcanada.wd10.myworkdayjobs.com'
    url = base_domain +  '/wday/cxs/navcanada/NAV_Careers/jobs'

    payload = {
        # 'locationCountry': ["a30a87ed25634629aa6c3958aa2b91ea"],
        "appliedFacets":
            {},
        'limit': 20,
        'offset': 0,
        'searchText': ""
    }
    jd_url = base_domain + '/wday/cxs/navcanada/NAV_Careers'
    url_lang = '/en-US/NAV_Careers'

if __name__=='__main__':
    test=NavCanadaScraper()
    yol=test.scrape_jobs()
    # print(yo)
    print(yol)
    # print(test.scrape_jd(yol['ccc41cce97']))