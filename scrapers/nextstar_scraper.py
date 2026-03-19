from scrapers._adp_JB import ADPBase
import json

class NextStarSraper(ADPBase):
    name= 'nextstar'
    params={
        'cid': '8aa53a99-a3f5-4260-aae3-17ca04fdef62',
        "lang": "en_CA",
        "locale": "en_CA",
        '$top': 100
    }
if __name__=='__main__':
    test=NextStarSraper()
    yo,yol=test.scrape_jobs()
    # print(yo)
    # print(json.dumps(yol,indent=4))
    print(test.scrape_jd(yol['4344f9563f']))



'''Sample skeleton
{
    "itemID": "9205981880694_1",
    "postingInstructions": [],
    "links": [],
    "additionalProperties": {},
    "requisitionTitle": "Senior Financial Analyst (FP&A)",
    "postDate": "2026-02-20T13:38:00.000-05:00",
    "screeningRequirements": [],
    "organizationalUnits": [],
    "payGradeRange": {
        "minimumRate": {
            "amountValue": 70000.0,
            "currencyCode": "CAD"
        },
        "maximumRate": {
            "amountValue": 95000.0,
            "currencyCode": "CAD"
        }
    },
    "workLevelCode": {
        "shortName": "Full Time Permanent"
    },
    "sponsoredVisaTypeCodes": [],
    "customFieldGroup": {
        "codeFields": [
            {
                "codeValue": "AN",
                "shortName": "Annually",
                "nameCode": {
                    "codeValue": "SalaryType"
                }
            },
            {
                "codeValue": "RANGE",
                "shortName": "RANGE",
                "nameCode": {
                    "codeValue": "SalaryRangeType"
                }
            }
        ],
        "dateFields": [
            {
                "dateValue": "2026-02-20T13:38Z",
                "nameCode": {
                    "codeValue": "PostingDate"
                }
            },
            {
                "dateValue": "2026-03-05T19:51Z",
                "nameCode": {
                    "codeValue": "CurrentServerDateTime"
                }
            }
        ],
        "indicatorFields": [
            {
                "indicatorValue": false,
                "nameCode": {
                    "codeValue": "PriortyStatusFlag"
                }
            },
            {
                "indicatorValue": false,
                "nameCode": {
                    "codeValue": "InternalPostingFlag"
                }
            },
            {
                "indicatorValue": true,
                "nameCode": {
                    "codeValue": "MinValue"
                }
            },
            {
                "indicatorValue": false,
                "nameCode": {
                    "codeValue": "IsVsidApplicable"
                }
            },
            {
                "indicatorValue": false,
                "nameCode": {
                    "codeValue": "IsSassDlReqForExtPostFlag"
                }
            },
            {
                "indicatorValue": false,
                "nameCode": {
                    "codeValue": "IsSassDlReqForIntPostFlag"
                }
            },
            {
                "indicatorValue": false,
                "nameCode": {
                    "codeValue": "IsMonetaryFlag"
                }
            },
            {
                "indicatorValue": false,
                "nameCode": {
                    "codeValue": "IsNonMonetaryFlag"
                }
            }
        ],
        "numberFields": [
            {
                "numberValue": 0.0,
                "categoryCode": {
                    "codeValue": "ApplicantCount"
                }
            },
            {
                "categoryCode": {
                    "codeValue": "AwardAmount"
                }
            }
        ],
        "stringFields": [
            {
                "stringValue": "992165",
                "nameCode": {
                    "codeValue": "ExternalJobID"
                }
            },
            {
                "nameCode": {
                    "codeValue": "CareerCenterRefId"
                }
            },
            {
                "nameCode": {
                    "codeValue": "GuidelineOid"
                }
            },
            {
                "nameCode": {
                    "codeValue": "CurrencySymbolOrCode"
                }
            },
            {
                "stringValue": "",
                "nameCode": {
                    "codeValue": "HomeDepartment"
                }
            },
            {
                "stringValue": "Specialist",
                "nameCode": {
                    "codeValue": "JobClass"
                }
            },
            {
                "stringValue": "70000.00 To 95000.00 (CAD) Annually",
                "nameCode": {
                    "codeValue": "SalaryRange"
                }
            }
        ]
    },
    "clientRequisitionID": "1502",
    "requisitionLocations": [
        {
            "aliasNames": [],
            "address": {
                "cityName": "Windsor",
                "countrySubdivisionLevel1": {
                    "codeValue": "ON"
                },
                "postalCode": "N8N 5E8"
            },
            "nameCode": {
                "shortName": " Windsor, ON, CA"
            }
        }
    ]
}
'''