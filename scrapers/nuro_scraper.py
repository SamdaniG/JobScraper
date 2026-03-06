from scrapers._greenhouse_JB import GreenhouseScraper
import json

class NuroScraper(GreenhouseScraper):
    name='nuro'

if __name__=='__main__':
    test=NuroScraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    print(json.dumps(yol,indent=4))