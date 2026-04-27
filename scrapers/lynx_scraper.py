from scrapers._ats_ripplingJB import ATSRippling
import json

class LynxScraper(ATSRippling):
    name = 'lynx'
    jobBoardSlug = 'lynx-software-technologies'
    # url = base_domain + f'{jobBoardSlug}' + '/jobs'


if __name__=='__main__':
    test=LynxScraper()
    yo=test.scrape_jobs()
    print(yo)
    print(json.dumps(yo, indent=4))
    # print(test.scrape_jd(yol['ff9a00a9b8']))