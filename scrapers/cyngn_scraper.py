from scrapers._lever_JB import LeverBase
import json

class CyngnScraper(LeverBase):
    name='cyngn'
    base_domain = f'https://api.lever.co/v0/postings/{name}'
    param = {
        'mode':'json',
    }

if __name__=='__main__':
    test=CyngnScraper()
    yo,yol = test.scrape_jobs()
    print(yo)
    # print(json.dumps(yol,indent=4))