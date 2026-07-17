from scrapers._ats_ripplingJB import ATSRippling
import json

class BlueWaterAutonomyScraper(ATSRippling):
    name = 'canada rocket company'
    jobBoardSlug = 'canada-rocket-company'
    # url = base_domain + f'{jobBoardSlug}' + '/jobs'

    params={}
if __name__=='__main__':
    test=BlueWaterAutonomyScraper()
    yo=test.scrape_jobs()
    # print(yo)
    print(json.dumps(yo, indent=4))
    # print(test.scrape_jd(yol['ff9a00a9b8']))