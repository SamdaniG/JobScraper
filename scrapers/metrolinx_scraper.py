from scrapers._oraclecloud_JB import OracleCloudScraper
class MetrolinxScraper(OracleCloudScraper):
    name="metrolinx"
    base_domain='https://ehtc.fa.ca2.oraclecloud.com'
    params = {
        "onlyData": "true",

        "expand": (
            "requisitionList.workLocation,"
            "requisitionList.otherWorkLocations,"
            "requisitionList.secondaryLocations,"
            "flexFieldsFacet.values,"
            "requisitionList.requisitionFlexFields"
        ),

        "finder": (
            "findReqs;"
            "siteNumber=CX_1,"
            "facetsList=LOCATIONS;WORK_LOCATIONS;WORKPLACE_TYPES;"
            "TITLES;CATEGORIES;ORGANIZATIONS;POSTING_DATES;FLEX_FIELDS,"
            "limit=100,"
            "sortBy=POSTING_DATES_DESC"
        )
    }

if __name__=='__main__':
    test=MetrolinxScraper()
    yo,yol=test.scrape_jobs()
    # print(yo)
    print(len(yo))
    # print(yol)
