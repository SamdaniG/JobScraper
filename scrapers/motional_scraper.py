from scrapers._greenhouse_JB import GreenhouseScraper
import json

class MotionalScraper(GreenhouseScraper):
    name= 'motional'


if __name__=='__main__':
    test=MotionalScraper()
    yol=test.scrape_jobs()
    # print(yol)
    # print(test.scrape_jd(yol['9568969768']))