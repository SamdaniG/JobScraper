from scrapers._lever_JB import LeverBase
import json

class IntersectScraper(LeverBase):
    name='intersect'

if __name__=='__main__':
    test=IntersectScraper()
    yol = test.scrape_jobs()
    # print(yo)
    # print(json.dumps(yol,indent=4))
    # print(json.dumps(yol['236263088d'],indent=4))
    print(test.scrape_jd(source=yol['a7428a9a26']))
