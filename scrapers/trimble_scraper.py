from scrapers._eightfoldaiJB import EightfoldaiBase
class TrimbleScraper(EightfoldaiBase):
    name='trimble'

if __name__=='__main__':
    test=TrimbleScraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    # print(json.dumps(yol,indent=4))

    # print(test.scrape_jd(yol['5b91f632e7']))


'''Sample Skeleton
{'atsJobId': 'R53402',
  'creationTs': 1765324800,
  'department': 'Sales Accounts',
  'displayJobId': 'R53402',
  'id': 171837903639,
  'isHot': 0,
  'locationFlexibility': None,
  'locations': ['Canada - Remote'],
  'name': 'Sales Manager, Canada',
  'positionUrl': '/careers/job/171837903639',
  'postedTs': 1765756800,
  'solrScore': None,
  'standardizedLocations': ['CA'],
  'stars': 0,
  'workLocationOption': 'onsite'}
'''