import json
from scrapers._oraclecloud_JB import OracleCloudScraper

class LinamarScraper(OracleCloudScraper):
    name="linamar"
    base_domain="https://fa-epmd-saasfaprod1.fa.ocs.oraclecloud.com"

    url = (base_domain +
           "/hcmRestApi/resources/latest/recruitingCEJobRequisitions")

    params = {
        "onlyData": "true",
        "expand": "requisitionList.workLocation,"
                  "requisitionList.otherWorkLocations,"
                  "requisitionList.secondaryLocations,"
                  "flexFieldsFacet.values,"
                  "requisitionList.requisitionFlexFields",
        "finder": (
            "findReqs;"
            "siteNumber=CX_3001,"
            "facetsList=LOCATIONS;WORK_LOCATIONS;WORKPLACE_TYPES;"
            "TITLES;CATEGORIES;ORGANIZATIONS;POSTING_DATES;FLEX_FIELDS,"
            "limit=100,"
            "locationId = 300000000396101,"
            "sortBy=POSTING_DATES_DESC"
        )
    }
    jd_url= (base_domain +
       "/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails")

if __name__=='__main__':
    test=LinamarScraper()
    yo, yol = test.scrape_jobs()
    print(json.dumps(yol,indent=4))
    # print(yol['c48319fc55'])
    # print(test.scrape_jd(yol['c48319fc55']))

'''Sample Skeleton
{
    "Id": "12142",
    "Title": "Quality Inspector - Level 1",
    "PostedDate": "2026-02-27",
    "PostingEndDate": null,
    "Language": "US",
    "PrimaryLocationCountry": "CA",
    "GeographyId": 100000884541373,
    "HotJobFlag": false,
    "WorkplaceTypeCode": null,
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
    "ShortDescriptionStr": "",
    "PrimaryLocation": "Guelph, ON, Canada",
    "Distance": 1772150400000.0,
    "TrendingFlag": false,
    "BeFirstToApplyFlag": false,
    "Relevancy": 9,
    "WorkplaceType": "",
    "ExternalQualificationsStr": null,
    "ExternalResponsibilitiesStr": null,
    "secondaryLocations": [],
    "otherWorkLocations": [],
    "workLocation": [
        {
            "LocationId": 300000059353492,
            "LocationName": "Linamar Gear",
            "AddressLine1": "32 Independence Place",
            "AddressLine2": null,
            "AddressLine3": null,
            "AddressLine4": null,
            "Building": null,
            "TownOrCity": "Guelph",
            "PostalCode": "N1K 1H8",
            "Country": "CA",
            "Region1": null,
            "Region2": null,
            "Region3": "Ontario",
            "Latitude": 43.53113,
            "Longitude": -80.30884
        }
    ],
    "requisitionFlexFields": []
}
'''