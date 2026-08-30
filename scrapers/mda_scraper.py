from scrapers._ultipro_JB import UltiproScraper
import json

class MDAScraper(UltiproScraper):
    name = "mda space"
    company_hex = "MAC5000MCDW"
    company_id = '664818ff-3594-4bec-9f30-3394e59e19f3'


if __name__ == '__main__':
    test= MDAScraper()
    yol=test.scrape_jobs()
    print(json.dumps(yol,indent=4))
    # print(test.scrape_jd(yol["b71feba140"]))