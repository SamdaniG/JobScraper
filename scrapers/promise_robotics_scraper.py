from scrapers._lever_JB import LeverBase
import json

class PromiseRoboticsScraper(LeverBase):
    name='promiserobotics'

if __name__=='__main__':
    test=PromiseRoboticsScraper()
    yol = test.scrape_jobs()
    print(yol)
    # print(json.dumps(yol,indent=4))
    # print(json.dumps(yol['236263088d'],indent=4))

    # jd_test=test.scrape_jd(source=yol['236263088d'])
    # print(jd_test)
