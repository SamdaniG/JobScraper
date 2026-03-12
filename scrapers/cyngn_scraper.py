from scrapers._lever_JB import LeverBase
import json

class CyngnScraper(LeverBase):
    name='cyngn'

if __name__=='__main__':
    test=CyngnScraper()
    yo,yol = test.scrape_jobs()
    print(yo)
    # print(json.dumps(yol,indent=4))