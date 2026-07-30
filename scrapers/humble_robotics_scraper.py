from scrapers._lever_JB import LeverBase
import json

class HumbleRoboticsScraper(LeverBase):
    name='humble-robotics'

if __name__=='__main__':
    test=HumbleRoboticsScraper()
    yol = test.scrape_jobs()
    # print(yol)
    # print(json.dumps(yol,indent=4))
    print(test.scrape_jd(yol['73c9801df2']))

