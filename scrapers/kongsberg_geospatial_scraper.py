from scrapers._adp_JB import ADPBase
import json

class KongsbergGeospatialSraper(ADPBase):
    name= 'kongsberg geospatial'
    base_domain = 'https://workforcenow.adp.com/mascsr/default'
    url = base_domain + '/careercenter/public/events/staffing/v1/job-requisitions'

    params={
        'cid': '8fd13316-1f93-4d98-b39c-59a884b85873',
        'ccId': '9201247417322_3',
        "lang": "en_CA",
        "locale": "en_CA",
        '$top': 100
    }
    apply_url = base_domain + f'/mdf/recruitment/recruitment.html?cid={params['cid']}&ccId={params['ccId']}&jobId='

if __name__=='__main__':
    test=KongsbergGeospatialSraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    print(yol)
    print(json.dumps(yol,indent=4))
    # print(test.scrape_jd(yol['4344f9563f']))
