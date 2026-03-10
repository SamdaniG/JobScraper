from scrapers._lever_JB import LeverBase

class ZooxScraper(LeverBase):
    name = 'zoox'
    base_domain = f'https://api.lever.co/v0/postings/{name}'
    param = {
        'mode':'json',
    }


if __name__=='__main__':
    test=ZooxScraper()
    yo,yol=test.scrape_jobs()
    print(yo)