from scrapers._greenhouse_JB import GreenhouseScraper
import json

class KodiakScraper(GreenhouseScraper):
    name='kodiak'


if __name__=='__main__':
    test=KodiakScraper()
    yo,yol=test.scrape_jobs()
    print(len(yo))
    # print(yo)
    print(json.dumps(yol,indent=4))
    # print(test.scrape_jd(yol['292a17b88b']))