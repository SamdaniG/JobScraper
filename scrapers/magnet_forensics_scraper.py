from scrapers._lever_JB import LeverBase
import json

class MagnetForensicsScraper(LeverBase):
    name='magnetforensics'

if __name__=='__main__':
    test=MagnetForensicsScraper()
    yol = test.scrape_jobs()
    # print(yo)
    print(json.dumps(yol,indent=4))
    # print(test.scrape_jd(yol["706f93bff3"]))

