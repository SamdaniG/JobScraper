from scrapers._lever_JB import LeverBase
import json

class FieldAIScraper(LeverBase):
    name='field-ai'

if __name__=='__main__':
    test=FieldAIScraper()
    yol = test.scrape_jobs()
    # print(yol)
    # print(json.dumps(yol,indent=4))
    # print(json.dumps(yol['e51725e030'],indent=4))

    jd_test=test.scrape_jd(source=yol['e51725e030'])
    print(jd_test)
