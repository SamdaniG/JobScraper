from scrapers._eightfoldaiJB import EightfoldaiBase
class EatonScraper(EightfoldaiBase):
    name='eaton'

if __name__=='__main__':
    test=EatonScraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    print(yol)