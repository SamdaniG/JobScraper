from scrapers._eightfoldaiJB import EightfoldaiBase
class EatonScraper(EightfoldaiBase):
    name='eaton'
    base_domain= f'https://{name}.eightfold.ai'
    url = base_domain + '/api/pcsx/search'
    params = {
        'domain' : f'{name}.com',
        # query =
        'location' : 'Canada',
        'start' : 0,
        'sort_by' : 'distance',
        'filter_include_remote' : 1
    }
    jd_url = base_domain + '/api/pcsx/position_details'
    jd_params={
        'position_id' : 'sample',
        'domain' : f'{name}.com',
        'hl' : 'en'
    }

if __name__=='__main__':
    test=EatonScraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    print(yol)