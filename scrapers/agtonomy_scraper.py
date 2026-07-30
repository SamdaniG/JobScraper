from scrapers._lever_JB import LeverBase
import json

class AgtonomyScraper(LeverBase):
    name = 'agtonomy'

if __name__=='__main__':
    test=AgtonomyScraper()
    yol=test.scrape_jobs()
    # print(set(yol))
    # print(yol)
    print(test.scrape_jd(yol['384954537d']))

'''
['additionalPlain', 'additional', 'categories', 
'createdAt', 'descriptionPlain', 'description', 
'id', 'lists', 'salaryRange', 'salaryDescription', 
'salaryDescriptionPlain', 'text', 'workplaceType', 
'opening', 'openingPlain', 'descriptionBody', 
'descriptionBodyPlain', 'country', 'hostedUrl', 'applyUrl']

'''