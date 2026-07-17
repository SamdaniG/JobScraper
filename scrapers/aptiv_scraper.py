from scrapers._myworkday_JB import MyworkdayBase

class AptivScraper(MyworkdayBase):
    name='aptiv'
    base_domain = 'https://aptiv.wd5.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/aptiv/APTIV_CAREERS/jobs'

    payload = {
        # 'locationCountry': ["a30a87ed25634629aa6c3958aa2b91ea"],
        "appliedFacets":
            {
                # "locationCountry": ["a30a87ed25634629aa6c3958aa2b91ea"],
                "Country": ["a30a87ed25634629aa6c3958aa2b91ea"]
            },
        'limit': 20,
        'offset': 0,
        'searchText': ""
    }
    jd_url = base_domain + '/wday/cxs/aptiv/APTIV_CAREERS'
    url_lang ='/en-US/APTIV_CAREERS'

if __name__=='__main__':
    test=AptivScraper()
    yol=test.scrape_jobs()
    # print(yo)
    # print(yol)
    print(test.scrape_jd(yol['3a19b9a30a']))