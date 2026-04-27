from scrapers._greenhouse_JB import GreenhouseScraper
import json

class MayMobilityScraper(GreenhouseScraper):
    name='maymobility'


if __name__=='__main__':
    test=MayMobilityScraper()
    yol=test.scrape_jobs()
    print(len(yol))
    # print(yo)
    print(json.dumps(yol,indent=4))
    # print(test.scrape_jd(yol['292a17b88b']))