from scrapers._lever_JB import LeverBase
import json

class FieldAIScraper(LeverBase):
    name='field-ai'

if __name__=='__main__':
    test=FieldAIScraper()
    yol = test.scrape_jobs()
    print(yol)
    # print(json.dumps(yol,indent=4))
    # print(json.dumps(yol['236263088d'],indent=4))

    # jd_test=test.scrape_jd(source=yol['236263088d'])
    # print(jd_test)
