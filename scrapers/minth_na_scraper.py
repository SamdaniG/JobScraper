from scrapers._adp_JB import ADPBase
import json

class MinthNASraper(ADPBase):
    name= 'minth'
    params={
        'cid': 'ac537a1a-b883-4fca-bc60-3a683b447964',
        'ccId': '19000101_000001',
        "lang": "en_CA",
        "locale": "en_CA",
        '$top': 100
    }
    """
    cid=&timeStamp=1775092035904&ccId=19000101_000001&lang=en_CA&ccId=19000101_000001&locale=en_CA&$top=10
    """

if __name__=='__main__':
    test=MinthNASraper()
    yol=test.scrape_jobs()
    # print(yo)
    # print(yol)
    # print(json.dumps(yol,indent=4))
    # print(test.scrape_jd(yol['cfd0a1d5cf']))
