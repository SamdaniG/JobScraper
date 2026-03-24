from scrapers._greenhouse_JB import GreenhouseScraper
import json

class TorcRoboticsScraper(GreenhouseScraper):
    name= 'torcrobotics'


if __name__=='__main__':
    test=TorcRoboticsScraper()
    yol=test.scrape_jobs()
    print(set(yol))
    print(yol)
    print(test.scrape_jd(yol['e39cda8a34']))