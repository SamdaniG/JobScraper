from scrapers._greenhouse_JB import GreenhouseScraper
import json

class AppliedIntuitionScraper(GreenhouseScraper):
    name= 'appliedintuition'


if __name__=='__main__':
    test=AppliedIntuitionScraper()
    yo,yol=test.scrape_jobs()
    # print(yo)
    print(test.scrape_jd(yol['9568969768']))