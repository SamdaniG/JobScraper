from scrapers._ats_ripplingJB import ATSRippling
import json

class BlueWaterAutonomy(ATSRippling):
    name = 'blue water autonomy'
    jobBoardSlug = 'blue-water-autonomy'

    params = {}
if __name__=='__main__':
    test=BlueWaterAutonomy()
    yo,yol=test.scrape_jobs()
    # print(yo)
    # print(json.dumps(yol, indent=4))
    print(test.scrape_jd(yol['93aeee2448']))