from scrapers._ats_ripplingJB import ATSRippling
import json

class OctasicScraper(ATSRippling):
    name = 'octasic'
    jobBoardSlug = 'octasic-inc'

    params={}
if __name__=='__main__':
    test=OctasicScraper()
    yol=test.scrape_jobs()
    print(yol)
    # print(json.dumps(yol, indent=4))
    # print(test.scrape_jd(yol['ff9a00a9b8']))