import json

from scrapers._eightfoldaiJB import EightfoldaiBase
class EatonScraper(EightfoldaiBase):
    name='eaton'

if __name__=='__main__':
    test=EatonScraper()
    yo,yol=test.scrape_jobs()
    # print(yo)
    # print(yol)
    print(json.dumps(yol['7168f48ce5'],indent=4))
    print(test.scrape_jd(yol['7168f48ce5']))