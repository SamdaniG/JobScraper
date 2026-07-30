from scrapers._lever_JB import LeverBase
import json

class DexterityScraper(LeverBase):
    name='dexterity'

if __name__=='__main__':
    test=DexterityScraper()
    yol = test.scrape_jobs()
    # print(yol)
    # print(json.dumps(yol,indent=4))
    # print(json.dumps(yol['e688f67be8'],indent=4))

    jd_test=test.scrape_jd(source=yol['e688f67be8'])
    print(jd_test)
