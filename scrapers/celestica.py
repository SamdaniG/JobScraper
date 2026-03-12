# import requests
#
# url = "https://career5.successfactors.eu/career"
#
# params = {
#     "company": "celestica",
#     "career_ns": "job_listing_summary",
#     "navBarLevel": "JOB_SEARCH",
#     "page": 1,
#     "format": "json"
# }
#
# r = requests.get(url, params=params)
# print(r.raise_for_status())
# data = r.json()
#
# for job in data["jobs"]:
#     print(job["title"], job["location"])
