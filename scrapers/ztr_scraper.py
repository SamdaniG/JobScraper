from scrapers._bamboohr_JB import BambooHRBase

class ZTRScraper(BambooHRBase):
    name = 'ztr'


if __name__=='__main__':
    test=ZTRScraper()

    yol=test.scrape_jobs()
    print(set(yol))
    print(yol)
    # print(yol['844354a354'])
    print(test.scrape_jd(yol['844354a354']))



'''Sample skeleton
{
    "id": "232",
    "jobOpeningName": "Electrical Technologist",
    "departmentId": "19011",
    "departmentLabel": "Canada",
    "employmentStatusLabel": "Full-Time",
    "location": {
        "city": "London",
        "state": "Ontario"
    },
    "atsLocation": {
        "country": null,
        "state": null,
        "province": null,
        "city": null
    },
    "isRemote": null,
    "locationType": "0"
}
'''