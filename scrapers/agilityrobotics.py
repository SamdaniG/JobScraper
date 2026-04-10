from scrapers._greenhouse_JB import GreenhouseScraper
import json

class AgilityRoboticsScraper(GreenhouseScraper):
    name= 'agilityrobotics'


if __name__=='__main__':
    test=AgilityRoboticsScraper()
    yol=test.scrape_jobs()
    print(yol)
    # print(test.scrape_jd(yol['9568969768']))