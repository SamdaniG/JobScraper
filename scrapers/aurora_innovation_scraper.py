from scrapers._greenhouse_JB import GreenhouseScraper
import json

class AurouraInnovationScraper(GreenhouseScraper):
    name= 'aurorainnovation'


if __name__=='__main__':
    test=AurouraInnovationScraper()
    yo=test.scrape_jobs()
    print(yo)
    print(len(list(yo)))
    # print(test.scrape_jd(yol['9568969768']))