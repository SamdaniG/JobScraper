from scrapers._greenhouse_JB import GreenhouseScraper
import json

class GatikScraper(GreenhouseScraper):
    name='gatikaiinc'


if __name__=='__main__':
    test=GatikScraper()
    yo,yol=test.scrape_jobs()

    # print(yo)
    # print(json.dumps(yol,indent=4))
    # print(test.scrape_jd(yol['e6650ab1f2']))
