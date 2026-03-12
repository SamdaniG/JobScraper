from scrapers._eightfoldaiJB import EightfoldaiBase
class BostonScientificScraper(EightfoldaiBase):
    name='bostonscientific'

if __name__=='__main__':
    test=BostonScientificScraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    print(yol)