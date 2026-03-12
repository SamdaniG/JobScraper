from scrapers._ats_ripplingJB import ATSRippling
import json

class KrakenRoboticsScraper(ATSRippling):
    name = 'kraken robotics'
    jobBoardSlug = 'kraken-robotics-inc'
    # url = base_domain + f'{jobBoardSlug}' + '/jobs'


if __name__=='__main__':
    test=KrakenRoboticsScraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    # print(json.dumps(yol, indent=4))
    # print(test.scrape_jd(yol['ff9a00a9b8']))