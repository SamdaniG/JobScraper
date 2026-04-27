from scrapers._bamboohr_JB import BambooHRBase

class TrilliumRailScraper(BambooHRBase):
    name = 'trp'


if __name__=='__main__':
    test=TrilliumRailScraper()

    yol=test.scrape_jobs()
    print(set(yol))
    print(yol)
    # print(yol['844354a354'])
    print(test.scrape_jd(yol['844354a354']))


