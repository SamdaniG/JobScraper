from scrapers._myworkday_JB import MyworkdayBase
import json
class MarvellScraper(MyworkdayBase):
    name='marvell careers'
    base_domain= 'https://marvell.wd1.myworkdayjobs.com'
    url = base_domain + '/wday/cxs/marvell/MarvellCareers/jobs'

    payload = {
        "appliedFacets":
            {
                "Country": ["a30a87ed25634629aa6c3958aa2b91ea"]
            },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    url_lang = '/en-US/MarvellCareers'
    jd_url = base_domain + '/wday/cxs/marvell/MarvellCareers'

if __name__=='__main__':
    test=MarvellScraper()
    yo,yol=test.scrape_jobs()
    # print(yo)
    print(yol)