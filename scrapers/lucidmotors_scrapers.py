from scrapers._greenhouse_JB import GreenhouseScraper
import json

class LucidMotorsScraper(GreenhouseScraper):
    name = 'lucidmotors'


if __name__=='__main__':
    test=LucidMotorsScraper()
    yol=test.scrape_jobs()
    # print(len(yo))
    # print(json.dumps(yol,indent=4))
    print(test.scrape_jd(yol["33dbd03f66"]))