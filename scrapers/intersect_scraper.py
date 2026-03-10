from scrapers._lever_JB import LeverBase
import json

class IntersectScraper(LeverBase):
    name='intersect'
    base_domain = f'https://api.lever.co/v0/postings/{name}'
    param = {
        'mode':'json',
    }

if __name__=='__main__':
    test=IntersectScraper()
    yo,yol = test.scrape_jobs()
    print(yo)
    # print(json.dumps(yol,indent=4))
    # print(json.dumps(yol['236263088d'],indent=4))

    # jd_test=test.scrape_jd(source=yol['236263088d'])
    # print(jd_test)
