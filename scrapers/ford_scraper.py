from scrapers._oraclecloud_JB import OracleCloudScraper
class FordScraper(OracleCloudScraper):
    name="ford"
    base_domain="https://efds.fa.em5.oraclecloud.com"
    params = {
        "onlyData": "true",
        "expand": "requisitionList.workLocation,"
                  "requisitionList.otherWorkLocations,"
                  "requisitionList.secondaryLocations,"
                  "flexFieldsFacet.values,"
                  "requisitionList.requisitionFlexFields",
        "finder": (
            "findReqs;"
            "siteNumber=CX_1,"
            "facetsList=LOCATIONS;WORK_LOCATIONS;WORKPLACE_TYPES;"
            "TITLES;CATEGORIES;ORGANIZATIONS;POSTING_DATES;FLEX_FIELDS,"
            "limit=100,"
            "lastSelectedFacet=LOCATIONS,"
            "selectedLocationsFacet=300000000425151,"
            "sortBy=POSTING_DATES_DESC"
        )
    }

if __name__=='__main__':
    test=FordScraper()
    yo=test.scrape_jobs()
    # print(yo)
    print(test.scrape_jd(yo["6819358f55"]))



''' Sample structure
{
    "Id": "59456",
    "Title": "Senior Engineering Specialist",
    "PostedDate": "2026-02-27",
    "PostingEndDate": null,
    "Language": "US",
    "PrimaryLocationCountry": "CA",
    "GeographyId": 100000032213871,
    "HotJobFlag": false,
    "WorkplaceTypeCode": "ORA_ON_SITE",
    "JobFamily": null,
    "JobFunction": null,
    "WorkerType": null,
    "ContractType": null,
    "ManagerLevel": null,
    "JobSchedule": null,
    "JobShift": null,
    "JobType": null,
    "StudyLevel": null,
    "DomesticTravelRequired": null,
    "InternationalTravelRequired": null,
    "WorkDurationYears": null,
    "WorkDurationMonths": null,
    "WorkHours": null,
    "WorkDays": null,
    "LegalEmployer": null,
    "BusinessUnit": null,
    "Department": null,
    "Organization": null,
    "MediaThumbURL": null,
    "ShortDescriptionStr": "Senior Engineering Specialist",
    "PrimaryLocation": "Windsor, ON, Canada",
    "Distance": 1772150400000.0,
    "TrendingFlag": false,
    "BeFirstToApplyFlag": false,
    "Relevancy": 9,
    "WorkplaceType": "On-site",
    "ExternalQualificationsStr": null,
    "ExternalResponsibilitiesStr": null,
    "secondaryLocations": [],
    "otherWorkLocations": [],
    "workLocation": [
        {
            "LocationId": 300000005673716,
            "LocationName": "Windsor Engine Plant #1",
            "AddressLine1": "100 Henry Ford Centre Drive",
            "AddressLine2": "PO Box 1634 Stn a",
            "AddressLine3": null,
            "AddressLine4": null,
            "Building": "WEP",
            "TownOrCity": "Windsor",
            "PostalCode": "N9A 7E8",
            "Country": "CA",
            "Region1": "Ontario",
            "Region2": "ON",
            "Region3": null,
            "Latitude": 42.31785,
            "Longitude": -83.03387
        }
    ],
    "requisitionFlexFields": []
}

'''