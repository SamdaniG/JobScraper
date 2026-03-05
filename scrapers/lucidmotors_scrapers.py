from scrapers._greenhouse_JB import GreenhouseScraper
import json

class LucidMotorsScraper(GreenhouseScraper):
    name = 'lucidmotors'


if __name__=='__main__':
    test=LucidMotorsScraper()
    yo,yol=test.scrape_jobs()
    print(len(yo))
    # print(json.dumps(yol,indent=4))