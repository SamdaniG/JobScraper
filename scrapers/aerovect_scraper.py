from scrapers._ashbyhq_JB import AshbyhqBase

class AerovectScraper(AshbyhqBase):
    name = 'aerovect'
    url_payload={
        'operationName': "ApiJobBoardWithTeams",
        'variables':
            {
                'organizationHostedJobsPageName': "AeroVect"
            },
        'query':
            "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) "
            "{\n  jobBoard: jobBoardWithTeams(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  ) "
            "{\n    teams {\n      id\n      name\n      externalName\n      parentTeamId\n      __typename\n    }\n    "
            "jobPostings {\n      id\n      title\n      teamId\n      locationId\n      locationName\n      workplaceType\n      "
            "employmentType\n      secondaryLocations {\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }\n      "
            "compensationTierSummary\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation "
            "{\n  locationId\n  locationName\n  __typename\n}"
    }

    jd_payload={
        'operationName':    "ApiJobPosting",
        'query'        :    "query ApiJobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {\n  jobPosting(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n    jobPostingId: $jobPostingId\n  ) {\n    id\n    title\n    departmentName\n    departmentExternalName\n    locationName\n    locationAddress\n    workplaceType\n    employmentType\n    descriptionHtml\n    isListed\n    isConfidential\n    teamNames\n    applicationForm {\n      ...FormRenderParts\n      __typename\n    }\n    surveyForms {\n      ...FormRenderParts\n      __typename\n    }\n    secondaryLocationNames\n    compensationTierSummary\n    compensationTiers {\n      id\n      title\n      tierSummary\n      __typename\n    }\n    applicationDeadline\n    compensationTierGuideUrl\n    scrapeableCompensationSalarySummary\n    compensationPhilosophyHtml\n    applicationLimitCalloutHtml\n    shouldAskForTextingConsent\n    candidateTextingPrivacyPolicyUrl\n    candidateTextingTermsAndConditionsUrl\n    legalEntityNameForTextingConsent\n    automatedProcessingLegalNotice {\n      automatedProcessingLegalNoticeRuleId\n      automatedProcessingLegalNoticeHtml\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment JSONBoxParts on JSONBox {\n  value\n  __typename\n}\n\nfragment FileParts on File {\n  id\n  filename\n  __typename\n}\n\nfragment FormFieldEntryParts on FormFieldEntry {\n  id\n  field\n  fieldValue {\n    ... on JSONBox {\n      ...JSONBoxParts\n      __typename\n    }\n    ... on File {\n      ...FileParts\n      __typename\n    }\n    ... on FileList {\n      files {\n        ...FileParts\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  isRequired\n  descriptionHtml\n  isHidden\n  __typename\n}\n\nfragment FormRenderParts on FormRender {\n  id\n  formControls {\n    identifier\n    title\n    __typename\n  }\n  errorMessages\n  sections {\n    title\n    descriptionHtml\n    fieldEntries {\n      ...FormFieldEntryParts\n      __typename\n    }\n    isHidden\n    __typename\n  }\n  sourceFormDefinitionId\n  __typename\n}",
        'variables'    : {
            'organizationHostedJobsPageName': "AeroVect",
            'jobPostingId': "meh"}
    }

if __name__=='__main__':
    test=AerovectScraper()
    yo,yol=test.scrape_jobs()
    print(yo)
    print(test.scrape_jd(yol['c5e20fd8a6']))


'''Sample skeleton
{
    "__typename": "JobPostingBriefsWithIdsAndTeamId",
    "id": "b64c2eda-5794-43ad-ac2a-5909c6520160",
    "title": "Autonomous GSE Operator (Atlanta)",
    "teamId": "2186ff36-be96-4a0b-acb1-543082bbdba0",
    "locationId": "20e4a3a8-5a5e-447e-8f84-56591f8063d6",
    "locationName": "Atlanta",
    "workplaceType": null,
    "employmentType": "FullTime",
    "secondaryLocations": [],
    "compensationTierSummary": "$60K \u2013 $67K \u2022 Offers Equity"
}
'''