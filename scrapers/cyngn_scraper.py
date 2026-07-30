from scrapers._lever_JB import LeverBase
import json

class CyngnScraper(LeverBase):
    name='cyngn'

if __name__=='__main__':
    test=CyngnScraper()
    yol = test.scrape_jobs()
    # print(yo)
    # print(json.dumps(yol,indent=4))
    print(test.scrape_jd(yol["706f93bff3"]))

'''
['additional', 'additionalPlain', 'categories', 
'createdAt', 'descriptionPlain', 'description', 'id', 
'lists', 'salaryRange', 'text', 'country', 'workplaceType', 'opening', 'openingPlain', 
'descriptionBody', 'descriptionBodyPlain', 'hostedUrl', 'applyUrl']
'''

'''

'''