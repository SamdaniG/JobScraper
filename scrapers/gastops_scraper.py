from scrapers._adp_JB import ADPBase
import json

class GAStopsSraper(ADPBase):
    name= 'gastops'
    params={
        'cid': '44dfb970-4042-4c3d-8525-e26b418cc3b1',
        'ccId': '19000101_000003',
        "lang": "en_CA",
        "locale": "en_CA",
        '$top': 100
    }

if __name__=='__main__':
    test=GAStopsSraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    print(yol)
    print(json.dumps(yol,indent=4))
    # print(test.scrape_jd(yol['4344f9563f']))
