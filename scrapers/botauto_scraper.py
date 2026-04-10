from scrapers._greenhouse_JB import GreenhouseScraper
import json

class BotAutoScraper(GreenhouseScraper):
    name= 'botauto'


if __name__=='__main__':
    test=BotAutoScraper()
    yol=test.scrape_jobs()
    print(yol)
    # print(test.scrape_jd(yol['9568969768']))