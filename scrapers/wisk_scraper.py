import json

from scrapers._myworkday_JB import MyworkdayBase

class WiskScraper(MyworkdayBase):
    name='wisk'
    base_domain = 'https://wisk.wd108.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/wisk/Wisk_Careers/jobs'

    payload = {
        # 'locationCountry': ["a30a87ed25634629aa6c3958aa2b91ea"],
        "appliedFacets":
            {},
        'limit': 20,
        'offset': 0,
        'searchText': ""
    }
    jd_url = base_domain + '/wday/cxs/wisk/Wisk_Careers'
    url_lang = '/en-US/Wisk_Careers'

if __name__=='__main__':
    test=WiskScraper()
    yol=test.scrape_jobs()
    # print(yo)
    # print(len(yol))
    # print(json.dumps(yol,indent=4))
    print(test.scrape_jd(yol['bb4a2b319b']))