from scrapers._greenhouse_JB import GreenhouseScraper
import json

class ScoutMotorsScraper(GreenhouseScraper):
    name= 'scoutmotors'


if __name__=='__main__':
    test=ScoutMotorsScraper()
    yol=test.scrape_jobs()
    print(yol)
    # print(test.scrape_jd(yol['9568969768']))