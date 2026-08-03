from scrapers._adp_JB import ADPBase
import json

class NanometricsSraper(ADPBase):
    name= 'nanometrics'
    params={
        'cid': '3d178141-59e5-45ba-a347-db3cfa0b5d08',
        'ccId': '19000101_000001',
        "lang": "en_CA",
        "locale": "en_CA",
        '$top': 100
    }


if __name__=='__main__':
    test=NanometricsSraper()
    yol=test.scrape_jobs()
    # print(yo)
    # print(yol)
    # print(json.dumps(yol,indent=4))
    print(test.scrape_jd(yol['ee197dabeb']))
