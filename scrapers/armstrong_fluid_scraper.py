from scrapers._bamboohr_JB import BambooHRBase

class ArmstrongFluidScraper(BambooHRBase):
    name = 'armstrongfluidtechnology'


if __name__=='__main__':
    test=ArmstrongFluidScraper()

    yol=test.scrape_jobs()
    print(set(yol))
    print(yol)
    # print(yol['844354a354'])
    # print(test.scrape_jd(yol['ee88071533']))
