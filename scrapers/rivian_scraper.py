import json
from scrapers.__base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
import re
from datetime import datetime

FMT='%Y-%m-%dT%H:%M:%S%z'
DATE_FMT = "%a %d-%b-%Y"
class RivianScraper(ApiJobBoardScraper):
    name = 'rivian'
    base_domain = 'https://careers.rivianvw.tech/'
    url = base_domain + 'api/jobs'
    params = {
        'locations': 'Toronto,Ontario,Canada|Vancouver,British Columbia,Canada',
        'page': 1,
        'limit': 100,
        'sortBy': 'posted_date',
        'descending': 'true',
        'internal': 'false'  ,
        'tags2':'Rivian and VW Group Technology'
     }
    click_link = base_domain + 'rivian-vw-group-technology/jobs/'

    def scrape_jobs(self):
        current_jobs_id=[]
        job_data={}

        resp = rq.get(url=self.url, params=self.params)
        # print(resp.raise_for_status())
        dat=resp.json()
        jobs_list=dat['jobs']
        # print(json.dumps(jobs_list[0],indent=4))

        for job in jobs_list:
            job=job['data']
            job_id = job['slug']
            url= self.click_link + job_id
            hash_id=sha256_hex(url)
            current_jobs_id.append(hash_id)

            job_deets=Job(
                job_id=             job_id,
                job_name=           job['title'],
                source=             self.name,
                location=           job['location_name'],
                posted_date=        datetime.strptime(job['posted_date'],FMT).strftime(DATE_FMT),
                url=                url,
                work_policy=        job['tags1'][0],
            )
            job_data[hash_id]=job_deets.to_dict()

        return current_jobs_id,job_data

    def scrape_jd(self, source: dict=None):
        job_id=source['job_id']
        jd=''
        resp = rq.get(url=self.url, params=self.params)
        dat = resp.json()
        jobs_list = dat['jobs']

        for job in jobs_list:
            if job['data']['slug']==job_id:
                resource=job['data']


        resp=                   resource['responsibilities']
        quali=                  resource['qualifications']
        jd += re.sub(r"\.\s*", "\n", resp.strip()) + '\n\n'
        jd += re.sub(r"\.\s*", "\n", quali.strip()) + '\n\n'
        jd += resource['description']

        return jd


if __name__=='__main__':
    test=RivianScraper()
    yo,yol=test.scrape_jobs()
    print(yo[1])
    # print(json.dumps(yol['283d25d951'],indent=4))

    print(test.scrape_jd(source=yol['283d25d951']))




'''Sample skeleton
{
    "data": {
        "slug": "29397",
        "language": "en-us",
        "languages": [
            "en-us"
        ],
        "req_id": "29397",
        "title": "Sr. Engineering Manager, Infotainment Applications",
        "description": "About Us Rivian and Volkswagen Group Technologies is a joint venture between two industry leaders with a clear vision for automotive\u2019s next chapter. From operating systems to zonal controllers to cloud and connectivity solutions, we\u2019re addressing the challenges of electric vehicles through technology that will set the standards for software-defined vehicles around the world. The road to the future is uncharted. By combining our expertise across connectivity, AI, security and more, we\u2019ll map a new way forward. Working together, we\u2019ll create a future that\u2019s more connected, more intelligent, more sustainable for everyone. Role Summary Rivian and Volkswagen Group Technologies is building electric vehicles that provide rich, immersive in-vehicle infotainment user experiences throughout a customer journey. Our mission is to empower our customers on these journeys with best in class infotainment applications that keep them informed and entertained at all times. We\u2019re seeking a hands-on, technical engineering lead to help us realize this vision. In this role, you\u2019ll build and manage a skilled team of android and embedded engineers based in various offices who develop our infotainment applications and platform. You and your team will partner closely with a large array of cross functional partners, including product, design, and other engineering teams. At Rivian and Volkswagen Group Technologies everyone is responsible for the quality of the product, and this role will allow you to have an outsized impact. You\u2019ll also be responsible for pushing forward technical initiatives, working with product and program on quarterly planning activities, gaining alignment on priorities with cross functional partners and following through on delivery. Responsibilities Guide the architecture, development, and maintenance of a modern android application. Lead, manage, and hire a cross discipline team of engineers working on both Android and Embedded software. Drive the implementation of best practices in architecture, optimized performance, stability, and scalability. Ensure technical quality and or standards across the team through processes (architecture, code reviews, documentation) and culture (engineering excellence). Collaborate with cross-functional teams, product, design and other stakeholders to understand and translate business requirements into technical solutions. Interfaces with key external partners and executive level stakeholders. Foster a culture of continuous learning by providing training and support to enhance skills within your team and the broader infotainment community, promoting collaboration to meet evolving needs. Act as a liaison between technical teams and senior leadership, effectively communicating the value proposition and impact of initiatives, ensuring the balance of short and long-term needs to support team scalability. Define key metrics and KPIs and implement them to ensure maximum productivity, quality, visibility and predictability for the organization. Qualifications Bachelor's degree in Computer Science, Engineering, or similar. Combined 8+ years of experience as a software engineer and manager. 3+ years of experience in managing and leading engineering teams, with a proven ability to mentor and grow technical talent. Strong technical and strategic vision, with the ability to translate broad objectives into actionable engineering plans. Strong knowledge of Android application and/or framework experience, including Android design principles, technologies, development, and application interface guidelines. Direct experience building best-in-class modern android or infotainment applications. Strong project management skills with demonstrated success delivering. Excellent communication and interpersonal skills essential for collaborating with cross-functional teams and senior leadership. Proactive commitment to staying updated with modern data practices and philosophies. Pay Disclosure * Salary range for Vancouver applicants: $174,200 - $230,880 CAD. \u2014 The posted salary represents the lowest and highest ranges RV Tech reasonably and in good faith expects to pay for the position. Any posted salary range pertains only to the estimated starting pay for the role. Actual starting pay is based on a number of factors, including, but not limited to, the candidate\u2019s experience, skillset, qualifications, specific competencies, relevant education, and location. Total Rewards Total compensation packages for this position include base salary, eligibility for an annual performance bonus, and eligibility for equity. In addition, our benefits package has been designed to support the health and wellness of our employees. Benefit offerings include Flex Time Off, retirement savings plans as well as medical, vision and dental coverage. For more information on RV Tech\u2019s comprehensive benefits package for full-time employees, check out our Global Benefits Site. External candidates can apply for this role through the RV Tech Careers site (https://rivianvw.tech/#careers). If you are a current employee, please apply through our internal job board (https://internal-careers-rivian.icims.com/). Equal Opportunity Rivian and Volkswagen Group Technologies is committed to creating a diverse environment and is proud to be an equal opportunity employer. All qualified applicants will receive consideration for employment without regard to race, color, religion, national origin, ancestry, sex, sexual orientation, gender, gender expression, gender identity, genetic information or characteristics, physical or mental disability, marital/domestic partner status, age, military/veteran status, medical condition, or any other characteristic protected by law. We are also committed to ensuring compliance with all applicable fair employment practice laws regarding citizenship and immigration status. Rivian and Volkswagen Group Technologies is committed to ensuring that our hiring process is accessible for persons with disabilities. If you have a disability or limitation, such as those covered by the Americans with Disabilities Act, that requires accommodations to assist you in the search and application process, please email us at candidateaccommodations@rivian.com. Candidate Data Privacy Rivian and VW Group Technologies (\u201cRivian and Volkswagen Group Technologies\u201d) may collect, use and disclose your personal information or personal data (within the meaning of the applicable data protection laws) when you apply for employment and/or participate in our recruitment processes (\u201cCandidate Personal Data\u201d). This data includes contact, demographic, communications, educational, professional, employment, social media/website, network/device, recruiting system usage/interaction, security and preference information. Rivian and Volkswagen Group Technologies may use your Candidate Personal Data for the purposes of (i) tracking interactions with our recruiting system; (ii) carrying out, analyzing and improving our application and recruitment process, including assessing you and your application and conducting employment, background and reference checks; (iii) establishing an employment relationship or entering into an employment contract with you; (iv) complying with our legal, regulatory and corporate governance obligations; (v) recordkeeping; (vi) ensuring network and information security and preventing fraud; and (vii) as otherwise required or permitted by applicable law. Rivian and Volkswagen Group Technologies may share your Candidate Personal Data with (i) internal personnel who have a need to know such information in order to perform their duties, including individuals on our People Team, Finance, Legal, and the team(s) with the position(s) for which you are applying; (ii) Rivian and Volkswagen Group Technologies affiliates; and (iii) Rivian and Volkswagen Group Technologies\u2019 service providers, including providers of background checks, staffing services, and cloud services. Rivian and Volkswagen Group Technologies may transfer or store internationally your Candidate Personal Data, including to or in the United States, Canada, and the European Union and in the cloud, and this data may be subject to the laws and accessible to the courts, law enforcement and national security authorities of such jurisdictions. Please see our Candidate Data Privacy Notice (English) and Candidate Data Privacy Notice (Serbian) for more information. Please note this job posting represents an open, active vacancy. Additionally, we are currently not accepting applications from third party application services.",
        "location_name": "1038 - 1050 Homer Street (Vancouver British Columbia)",
        "street_address": "1038 Homer Street",
        "city": "Vancouver",
        "state": "British Columbia",
        "country": "Canada",
        "country_code": "CA",
        "postal_code": "V6B 2W9",
        "location_type": "LAT_LNG",
        "latitude": 49.2768204,
        "longitude": -123.1206486,
        "categories": [
            {
                "name": "Software Engineering"
            }
        ],
        "tags1": [
            "Full Time"
        ],
        "tags2": [
            "Rivian and VW Group Technology"
        ],
        "promotion_value": 0,
        "employment_type": "FULL_TIME",
        "qualifications": "Bachelor's degree in Computer Science, Engineering, or similar. Combined 8+ years of experience as a software engineer and manager. 3+ years of experience in managing and leading engineering teams, with a proven ability to mentor and grow technical talent. Strong technical and strategic vision, with the ability to translate broad objectives into actionable engineering plans. Strong knowledge of Android application and/or framework experience, including Android design principles, technologies, development, and application interface guidelines. Direct experience building best-in-class modern android or infotainment applications. Strong project management skills with demonstrated success delivering. Excellent communication and interpersonal skills essential for collaborating with cross-functional teams and senior leadership. Proactive commitment to staying updated with modern data practices and philosophies.",
        "hiring_organization": "Rivian and VW Group Technology",
        "hiring_organization_logo": "https://rivian.icims.com/icims2/servlet/icims2?module=AppInert&action=download&id=506921&hashed=-1093731181",
        "responsibilities": "Guide the architecture, development, and maintenance of a modern android application. Lead, manage, and hire a cross discipline team of engineers working on both Android and Embedded software. Drive the implementation of best practices in architecture, optimized performance, stability, and scalability. Ensure technical quality and or standards across the team through processes (architecture, code reviews, documentation) and culture (engineering excellence). Collaborate with cross-functional teams, product, design and other stakeholders to understand and translate business requirements into technical solutions. Interfaces with key external partners and executive level stakeholders. Foster a culture of continuous learning by providing training and support to enhance skills within your team and the broader infotainment community, promoting collaboration to meet evolving needs. Act as a liaison between technical teams and senior leadership, effectively communicating the value proposition and impact of initiatives, ensuring the balance of short and long-term needs to support team scalability. Define key metrics and KPIs and implement them to ensure maximum productivity, quality, visibility and predictability for the organization.",
        "posted_date": "2026-02-25T17:19:00+0000",
        "apply_url": "https://ca-careers-rivianvwtech.icims.com/jobs/29397/login",
        "internal": false,
        "external": false,
        "searchable": true,
        "applyable": true,
        "li_easy_applyable": true,
        "ats_code": "icims",
        "meta_data": {
            "last_mod": "2026-02-25T21:27:30.903+00:00",
            "icims": {
                "jps_is_public": true,
                "date_updated": "2026-02-25T17:19:43Z",
                "primary_posted_site_object": {
                    "site": "ca-careers-rivianvwtech",
                    "tenantId": "13315",
                    "siteId": "eea68e9f-3633-46cb-a2c3-56d478db5eb6",
                    "datePosted": "2026-02-25T17:19:00+0000",
                    "siteType": "ATTRACT"
                },
                "config_keys": {
                    "jobposting.external.company.name": "Rivian and VW Group Technology",
                    "jobposting.external.indeed.screenerquestions": "1",
                    "jobposting.external.company.url": "https://www.rivianvw.tech",
                    "icims.external.xml.feeds": "icims.advantageai.xml.enabled,icims.adzuna.xml.enabled,icims.allyenergy.xml.enabled,icims.careerbuilder.xml.enabled,icims.careerjet.xml.enabled,icims.craigslist.xml.enabled,icims.cv-library.xml.enabled,icims.direct-employers.xml.enabled,icims.hiringcafe.xml.enabled,icims.indeed.xml.enabled,icims.inhersight.xml.enabled,icims.itjobscafe.xml.enabled,icims.jobbio.xml.enabled,icims.jobget.xml.enabled,icims.jobgether.xml.enabled,icims.linkedin.xml.enabled,icims.monster.xml.enabled,icims.offerup.xml.enabled,icims.pallet-labs.xml.enabled,icims.propellum.xml.enabled,icims.puck.xml.enabled,icims.qkly.xml.enabled,icims.recruitnet.xml.enabled,icims.referio.xml.enabled,icims.resume-library.xml.enabled,icims.retailappointment.xml.enabled,icims.snagajob.xml.enabled,icims.stealthstartup.xml.enabled,icims.unpostedjobs.xml.enabled,icims.upward.xml.enabled,icims.ziprecruiter.xml.enabled,icims.zippia.xml.enabled,icims.nexxt.xml.enabled",
                    "portal.id": "886971",
                    "ccc.attract.portal.url": "https://careers.rivianvw.tech",
                    "jobposting.external.indeed.email": "",
                    "icims.config.web.indeed.easy.apply": "0"
                },
                "revision_int": 1,
                "uuid": "2537abe4-7d54-401c-aadf-3316210d14f7"
            },
            "googlejobs": {
                "jobName": "projects/helpful-passage-853/jobs/103146909647938246",
                "jobTitleSnippet": "",
                "companyName": "projects/helpful-passage-853/companies/b90d7ee9-4966-4467-8239-d2f1416df2bd",
                "searchTextSnippet": "",
                "derivedInfo": {
                    "jobCategories": [
                        "MANAGEMENT",
                        "COMPUTER_AND_IT"
                    ],
                    "locations": [
                        {
                            "radiusInMiles": 7.018693679578997e-05,
                            "postalAddress": {
                                "regionCode": "CA",
                                "sortingCode": "",
                                "recipients": [],
                                "organization": "",
                                "postalCode": "V6B 2X5",
                                "locality": "Vancouver",
                                "sublocality": "",
                                "addressLines": [
                                    "1038 Homer St, Vancouver, BC V6B 2X5, Canada"
                                ],
                                "administrativeArea": "BC",
                                "languageCode": "",
                                "revision": 0
                            },
                            "locationType": "STREET_ADDRESS",
                            "latLng": {
                                "latitude": 49.2768204,
                                "longitude": -123.1206486
                            }
                        }
                    ]
                },
                "jobHash": "f25b9106dbc359c45bcd354d945858b3",
                "jobSummary": "Guide the architecture, development, and maintenance of a modern android application. Lead, manage, and hire a cross discipline team of engineers working on both Android and Embedded software. Drive the implementation of best practices in architecture, optimized performance, stability, and scalability. Ensure technical quality and or standards across the team through processes (architecture, code reviews, documentation) and culture (engineering excellence). Collaborate with cross-functional teams, product, design and other stakeholders to understand and translate business requirements into technical solutions. Interfaces with key external partners and executive level stakeholders. Foster a culture of continuous learning by providing training and support to enhance skills within your team and the broader infotainment community, promoting collaboration to meet evolving needs. Act as a liaison between technical teams and senior leadership, effectively communicating the value proposition and impact of initiatives, ensuring the balance of short and long-term needs to support team scalability. Define key metrics and KPIs and implement them to ensure maximum productivity, quality, visibility and predictability for the organization."
            },
            "import_id": "d2bcf1a9-c896-4145-afdd-1c30c6de12ee",
            "redirectOnApply": true,
            "import_source": "ImporterService",
            "canonical_url": "https://careers.rivian.com/jobs/29397?lang=en-us",
            "client_code": "rivian",
            "gdpr": false
        },
        "update_date": "2026-02-25T21:27:30+0000",
        "create_date": "2026-02-25T17:19:51+0000",
        "category": [
            " Software Engineering"
        ],
        "full_location": "Vancouver, Canada",
        "short_location": "Vancouver, Canada",
        "multipleLocations": false
    }
}
'''