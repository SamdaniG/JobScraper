from scrapers._lever_JB import LeverBase
import json

class AgtonomyScraper(LeverBase):
    name = 'agtonomy'

if __name__=='__main__':
    test=AgtonomyScraper()
    yo,yol=test.scrape_jobs()
    print(yo)