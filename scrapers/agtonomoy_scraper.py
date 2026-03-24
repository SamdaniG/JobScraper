from scrapers._lever_JB import LeverBase
import json

class AgtonomyScraper(LeverBase):
    name = 'promiserobotics'

if __name__=='__main__':
    test=AgtonomyScraper()
    yol=test.scrape_jobs()
    print(set(yol))
    print(test.scrape_jd(yol['fea61a8b89']))