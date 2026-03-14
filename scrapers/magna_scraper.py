from scrapers._myworkday_JB import MyworkdayBase
import json

class MagnaScraper(MyworkdayBase):
    name='magna'
    base_domain = 'https://wd3.myworkdaysite.com'
    url = base_domain + '/wday/cxs/magna/Magna/jobs'

    payload = {
        'appliedFacets': {
            'Country': ["a30a87ed25634629aa6c3958aa2b91ea"]
        },
        'limit': 20,
        'offset': 0,
        'searchText': ""
    }
    jd_url = base_domain + '/wday/cxs/magna/Magna'
    url_lang = '/en-US/recruiting/magna/Magna'


if __name__=='__main__':
    test= MagnaScraper()
    yo, yol = test.scrape_jobs()
    print(yo)
    # print(yol)
    print(yol['bf33335a3e'])
    print(test.scrape_jd(yol['bf33335a3e']))