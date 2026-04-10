from scrapers._lever_JB import LeverBase

class ZooxScraper(LeverBase):
    name = 'zoox'

if __name__=='__main__':
    test=ZooxScraper()
    yo=test.scrape_jobs()
    # print(yo)
    print(test.scrape_jd(yo['af75c2302a']))