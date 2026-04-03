from scrapers._lever_JB import LeverBase
import json

class PlusAiScraper(LeverBase):
    name = 'plus-2'

if __name__=='__main__':
    test=PlusAiScraper()
    yol=test.scrape_jobs()
    print(set(yol))
    print(test.scrape_jd(yol['fea61a8b89']))