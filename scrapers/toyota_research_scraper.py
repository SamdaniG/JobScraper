from scrapers._lever_JB import LeverBase
import json

class ToyotoResearchScraper(LeverBase):
    name='tri'

if __name__=='__main__':
    test=ToyotoResearchScraper()
    yol = test.scrape_jobs()
    # print(yol)
    # print(json.dumps(yol,indent=4))
    # print(json.dumps(yol['236263088d'],indent=4))

    jd_test=test.scrape_jd(source=yol['75a3db2b29'])
    print(jd_test)
