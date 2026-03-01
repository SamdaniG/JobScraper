import json

from api_scrapers.base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
from datetime import datetime

DATE_FMT = "%a %d-%b-%Y"

class KeplerScraper(ApiJobBoardScraper):
    name='kepler'
    base_domain = f'https://api.lever.co/v0/postings/{name}'
    param = {
        'mode':'json',
        'location': 'Toronto, Ontario'
    }


    def scrape_jobs(self):
        current_jobs_id=[]
        job_data={}

        resp=rq.get(url=self.base_domain, params= self.param)
        resp.raise_for_status()
        job_list=resp.json()
        # print(json.dumps(job_list[0],indent=4))

        for job in job_list:
            job_id=job['id']
            job_title=job['text']
            hash_id=sha256_hex(job_id+job_title)
            current_jobs_id.append(hash_id)

            job_deets=Job(
                job_id=     job_id,
                job_name=   job_title,
                source=     self.name,
                location=   job['categories']['location'],
                posted_date=(datetime.fromtimestamp(job['createdAt'] / 1000)).strftime(DATE_FMT),
                url=        job['hostedUrl']
            )
            job_data[hash_id]=job_deets.to_dict()
            # job_data[hash_id]={
            #     'job_id': job_id,
            #     'job_name': job_title,
            #     'source': self.name,
            #     'location': job['categories']['location'],
            #     'posted_date':(datetime.fromtimestamp(job['createdAt'] / 1000)).strftime(DATE_FMT),
            #     'filled_date':"",
            #     'url':job['hostedUrl']
            # }

        return current_jobs_id, job_data

    def scrape_jd(self, source:dict=None):
        job_id = source['job_id']

        resp = rq.get(
            url=f"{self.base_domain}/{job_id}",
            params={'mode': 'json'}
        )
        resp.raise_for_status()

        data = resp.json()
        sections = []

        # Main description (HTML)
        if data.get("description"):
            sections.append(data["description"])

        # Structured blocks
        for block in data.get("lists", []):
            if block.get("text"):
                sections.append(block["text"])
            if block.get("content"):
                sections.append(block["content"])

        jd = "\n".join(sections)

        return self.clean_html(jd)

if __name__=='__main__':
    test=KeplerScraper()
    yo,yol = test.scrape_jobs()
    # print(yo)
    # print(yol)
    # 79c709d47c
    jd_test=test.scrape_jd(source=yol['79c709d47c'])
    # print(jd_test)



'''Sample skeleton
{
    "additionalPlain": "Use of AI in Recruitment\nAt Kepler Communications, all hiring decisions are made by people. Human recruiters are involved in every step of our recruitment process. We use AI-based tools (such as Lever AI and HireEZ) to assist with the initial review of applications by ranking candidates based on job-relevant criteria. These tools support - but do not replace - human judgment.\n\nEmployment Equity & Accommodation Statement\u00a0\nKepler Communications is an equal opportunity employer committed to building a diverse and inclusive workplace. We welcome applications from all qualified individuals, including women, Indigenous peoples, persons with disabilities, members of visible minorities, and people of all sexual orientations and gender identities.\u00a0\n\nIf you require accommodation during any stage of the recruitment process, please contact our People & Culture team at accommodation@kepler.space, and we will work with you to meet your needs.\u00a0\n",
    "additional": "<div><span style=\"font-size: 15px\"><b>Use of AI in Recruitment</b></span></div><div><span style=\"font-size: 15px\">At Kepler Communications, all hiring decisions are made by people. Human recruiters are involved in every step of our recruitment process. We use AI-based tools (such as Lever AI and HireEZ) to assist with the initial review of applications by ranking candidates based on job-relevant criteria. These tools support - but do not replace - human judgment.</span></div><div><br></div><div><b style=\"font-size: 12pt\">Employment Equity &amp; Accommodation Statement</b><span style=\"font-size: 12pt\">&nbsp;</span></div><div><span style=\"font-size: 12pt\">Kepler Communications is an equal opportunity employer committed to building a diverse and inclusive workplace. We welcome applications from all qualified individuals, including women, Indigenous peoples, persons with disabilities, members of visible minorities, and people of all sexual orientations and gender identities.&nbsp;</span></div><div><br></div><div><span style=\"font-size: 12pt\">If you require accommodation during any stage of the recruitment process, please contact our People &amp; Culture team at </span><a style=\"font-size: 12pt\" href=\"mailto:accommodation@kepler.space\">accommodation@kepler.space</a><span style=\"font-size: 12pt\">, and we will work with you to meet your needs.&nbsp;</span></div>",
    "categories": {
        "commitment": "Full-time Regular",
        "department": "Sales & Business Operations",
        "location": "Toronto, Ontario",
        "team": "Global Sales",
        "allLocations": [
            "Toronto, Ontario"
        ]
    },
    "createdAt": 1751461040734,
    "descriptionPlain": "At Kepler Communications, we're not just imagining the future of on-demand space connectivity - we're leading it!\n\nOur mission is to provide real-time Internet access\u00a0for\u00a0space-based assets, enabling a new era of data-driven exploration and innovation.\u00a0With 33 satellites launched to date, Kepler\u00a0operates\u00a0the first commercial optical data relay constellation, enabling real-time, continuous space communications while supporting advanced on-orbit\u00a0compute\u00a0and hosted payload capabilities.\u00a0\n\nIndustry-leading technology is only part of the story. What sets Kepler apart is our team: bold thinkers, skilled builders, and passionate problem-solvers who thrive on pushing the boundaries of\u00a0what\u2019s\u00a0possible in space. We believe great ideas come from diverse perspectives, and\u00a0we\u2019re\u00a0committed to creating an environment where you can grow, lead, and make a global impact.\u00a0\n\nIf\u00a0you\u2019re\u00a0ready to reach higher, move faster, and do work that shapes the future space economy - this is your launchpad. Come build the future with Kepler!\u00a0\n\n\nWhat We Offer:\n* Competitive compensation\u00a0with a robust equity plan to share in our success.\u00a0\n* Comprehensive coverage for health, dental, and vision insurance\u2014including dependents.\u00a0\n* Unlimited vacation, supportive parental leave policy,\u00a0and company-wide holiday shutdown.\u00a0\n* Semi-annual company-wide parties\u00a0and frequent in-office team events.\u00a0\n* Relocation packages\u00a0available for approved roles.\u00a0\n* $1,500 annual professional development fund\u00a0to support your growth.\u00a0\n* Fully stocked Toronto office kitchen\u00a0with snacks, drinks, games and top-notch kitchen appliances.\u00a0\n* Town Halls, Celebration Calls, and Company-wide events\u00a0to stay connected and engaged.\u00a0\n* We\u2019re a certified\u00a0Great Place to Work\u00ae, five years in a row!\n\n\nKepler is hiring a Director of Sales to lead the growth of our satellite communications and space infrastructure solutions across Canadian and allied government sectors. This individual will own customer relationships and strategic capture activities with defense and government organizations looking to leverage Kepler\u2019s secure, low latency space network with advanced compute for routing mission critical data. This role blends technical solutioning with strategic account leadership and will be instrumental in shaping how national customers access, move, and compute data in space.\u00a0\n",
    "description": "<div><span style=\"font-size: 16px\"><b>At <a href=\"https://kepler.space/\">Kepler Communications</a>, we're not just imagining the future of on-demand space connectivity - <i>we're leading it!</i></b></span></div><div><br></div><div><span style=\"font-size: 12pt\">Our mission is to provide real-time Internet access&nbsp;for&nbsp;space-based assets, enabling a new era of data-driven exploration and innovation.&nbsp;With <b>33 satellites launched to date</b><i>, </i>Kepler&nbsp;operates&nbsp;the first commercial optical data relay constellation, enabling real-time, continuous space communications while supporting advanced on-orbit&nbsp;compute&nbsp;and hosted payload capabilities.&nbsp;</span></div><div><br></div><div><span style=\"font-size: 12pt\">Industry-leading technology is only part of the story. <b>What sets Kepler apart is our team: </b>bold thinkers, skilled builders, and passionate problem-solvers who thrive on pushing the boundaries of&nbsp;what\u2019s&nbsp;possible in space. We believe great ideas come from diverse perspectives, and&nbsp;we\u2019re&nbsp;committed to creating an environment where you can grow, lead, and make a global impact.&nbsp;</span></div><div><br></div><div><span style=\"font-size: 12pt\">If&nbsp;you\u2019re&nbsp;ready to reach higher, move faster, and do work that shapes the future space economy - this is your launchpad. <b>Come build the future with Kepler!&nbsp;</b></span></div><div><br></div><div><br></div><div><b><u>What We Offer:</u></b></div><div><b>* Competitive compensation</b>&nbsp;with a robust equity plan to share in our success.&nbsp;</div><div><b>* Comprehensive coverage for health, dental, and vision insurance</b>\u2014including dependents.&nbsp;</div><div><b>* Unlimited vacation, supportive parental leave policy,</b>&nbsp;and company-wide holiday shutdown.&nbsp;</div><div><b>* Semi-annual company-wide parties</b>&nbsp;and frequent in-office team events.&nbsp;</div><div><b>* Relocation packages</b>&nbsp;available for approved roles.&nbsp;</div><div><b>* $1,500 annual professional development fund</b>&nbsp;to support your growth.&nbsp;</div><div><b>* Fully stocked Toronto office kitchen</b>&nbsp;with snacks, drinks, games and top-notch kitchen appliances.&nbsp;</div><div><b>* Town Halls, Celebration Calls, and Company-wide events</b>&nbsp;to stay connected and engaged.&nbsp;</div><div><b>* We\u2019re a certified&nbsp;<a href=\"https://www.greatplacetowork.ca/en/certification-menu/certified-organizations-updated#certified-organizations2/view-sub-list-details70/5f3438830d6f2900170827a4/\">Great Place to Work</a></b>\u00ae, five years in a row!</div><div><br></div><div><span style=\"font-size: 16px;\">Kepler is hiring a </span><b style=\"font-size: 16px;\">Director of Sales</b><span style=\"font-size: 16px;\"> to lead the growth of our satellite communications and space infrastructure solutions across Canadian and allied government sectors. This individual will own customer relationships and strategic capture activities with defense and government organizations looking to leverage Kepler\u2019s secure, low latency space network with advanced compute for routing mission critical data. This role blends technical solutioning with strategic account leadership and will be instrumental in shaping how national customers access, move, and compute data in space.&nbsp;</span></div>",
    "id": "0d614893-12fb-4daf-9491-dda0d09681cb",
    "lists": [
        {
            "text": "Key Responsibilities:",
            "content": "<li>Lead Kepler\u2019s Canadian business capture and customer engagement strategy focused on secure, resilient satellite communications for Canadian government and defense use&nbsp;</li><li>Build and maintain executive-level relationships with key Canadian stakeholders such as DND, CAF, CANSOFCOM, and procurement organizations, as well as international counterparts in allied nations&nbsp;</li><li>Identify and develop revenue-generating opportunities tied to space-based connectivity, ground station integration, and in-space compute and storage use cases&nbsp;</li><li>Navigate and influence procurement cycles for space-based ISR, C4ISR, Arctic comms, and situational awareness programs&nbsp;</li><li>Partner with Product and Engineering to align Kepler\u2019s capabilities including inter-satellite links, software-defined networking, and data relay nodes with mission-critical customer requirements&nbsp;</li><li>Lead capture efforts from ideation to proposal submission&nbsp;</li><li>Represent Kepler at Canadian and international space, defense, and technology conferences&nbsp;</li><li>Support long-term strategy, go-to-market planning, and cross-functional resource alignment as part of the Kepler leadership team&nbsp;</li><li>Nurture prospective opportunities through Canadian industrial participation programs (ITB/IRB)&nbsp;</li><li>Provide recurring input to executive leadership on market conditions, pipeline progress, and customer priorities&nbsp;</li>"
        },
        {
            "text": "Required Skills & Qualifications: ",
            "content": "<li>12+ years of experience in satellite communications, space systems, or high-technology business development within the government or defense sector&nbsp;</li><li>Bachelor\u2019s degree in engineering, aerospace, defense studies, or a related field&nbsp;</li><li>Proven record of success in business capture and customer relationship management in Canada and/or Five Eyes/Allied government environments&nbsp;</li><li>Strong understanding of space networks, and secure communications systems&nbsp;</li><li>Familiarity with space-based mission applications such as real-time Earth observation, ISR, and Arctic communications&nbsp;</li><li>Experience navigating public sector procurement cycles and defense acquisition frameworks&nbsp;</li><li>Ability to communicate credibly with operational and technical leader</li>"
        },
        {
            "text": "Bonus Points: ",
            "content": "<li>MBA and/or master\u2019s degree in engineering, aerospace, defense studies, or a related field&nbsp;</li><li>Background in military operations, defense or service&nbsp;&nbsp;</li><li>DND security clearance</li><li>Prior senior leadership roles at satellite operators, ground segment providers, or defense primes&nbsp;</li><li>Exposure to edge computing in space, data center virtualization, or cloud-integrated satellite solutions&nbsp;</li><li>Experience with international capture programs, especially within NATO, Five Eyes, or UN missions&nbsp;</li><li>Understanding of Controlled Goods Program, ITAR/CGP, and national export control frameworks&nbsp;</li><li>Strong existing network within the Canadian space and defense ecosystem&nbsp;</li>"
        }
    ],
    "text": "Director of Sales - ISR & Government of Canada Solutions",
    "country": "CA",
    "workplaceType": "remote",
    "opening": "<div><span style=\"font-size: 16px\"><b>At <a href=\"https://kepler.space/\">Kepler Communications</a>, we're not just imagining the future of on-demand space connectivity - <i>we're leading it!</i></b></span></div><div><br></div><div><span style=\"font-size: 12pt\">Our mission is to provide real-time Internet access&nbsp;for&nbsp;space-based assets, enabling a new era of data-driven exploration and innovation.&nbsp;With <b>33 satellites launched to date</b><i>, </i>Kepler&nbsp;operates&nbsp;the first commercial optical data relay constellation, enabling real-time, continuous space communications while supporting advanced on-orbit&nbsp;compute&nbsp;and hosted payload capabilities.&nbsp;</span></div><div><br></div><div><span style=\"font-size: 12pt\">Industry-leading technology is only part of the story. <b>What sets Kepler apart is our team: </b>bold thinkers, skilled builders, and passionate problem-solvers who thrive on pushing the boundaries of&nbsp;what\u2019s&nbsp;possible in space. We believe great ideas come from diverse perspectives, and&nbsp;we\u2019re&nbsp;committed to creating an environment where you can grow, lead, and make a global impact.&nbsp;</span></div><div><br></div><div><span style=\"font-size: 12pt\">If&nbsp;you\u2019re&nbsp;ready to reach higher, move faster, and do work that shapes the future space economy - this is your launchpad. <b>Come build the future with Kepler!&nbsp;</b></span></div><div><br></div><div><br></div><div><b><u>What We Offer:</u></b></div><div><b>* Competitive compensation</b>&nbsp;with a robust equity plan to share in our success.&nbsp;</div><div><b>* Comprehensive coverage for health, dental, and vision insurance</b>\u2014including dependents.&nbsp;</div><div><b>* Unlimited vacation, supportive parental leave policy,</b>&nbsp;and company-wide holiday shutdown.&nbsp;</div><div><b>* Semi-annual company-wide parties</b>&nbsp;and frequent in-office team events.&nbsp;</div><div><b>* Relocation packages</b>&nbsp;available for approved roles.&nbsp;</div><div><b>* $1,500 annual professional development fund</b>&nbsp;to support your growth.&nbsp;</div><div><b>* Fully stocked Toronto office kitchen</b>&nbsp;with snacks, drinks, games and top-notch kitchen appliances.&nbsp;</div><div><b>* Town Halls, Celebration Calls, and Company-wide events</b>&nbsp;to stay connected and engaged.&nbsp;</div><div><b>* We\u2019re a certified&nbsp;<a href=\"https://www.greatplacetowork.ca/en/certification-menu/certified-organizations-updated#certified-organizations2/view-sub-list-details70/5f3438830d6f2900170827a4/\">Great Place to Work</a></b>\u00ae, five years in a row!</div>",
    "openingPlain": "At Kepler Communications, we're not just imagining the future of on-demand space connectivity - we're leading it!\n\nOur mission is to provide real-time Internet access\u00a0for\u00a0space-based assets, enabling a new era of data-driven exploration and innovation.\u00a0With 33 satellites launched to date, Kepler\u00a0operates\u00a0the first commercial optical data relay constellation, enabling real-time, continuous space communications while supporting advanced on-orbit\u00a0compute\u00a0and hosted payload capabilities.\u00a0\n\nIndustry-leading technology is only part of the story. What sets Kepler apart is our team: bold thinkers, skilled builders, and passionate problem-solvers who thrive on pushing the boundaries of\u00a0what\u2019s\u00a0possible in space. We believe great ideas come from diverse perspectives, and\u00a0we\u2019re\u00a0committed to creating an environment where you can grow, lead, and make a global impact.\u00a0\n\nIf\u00a0you\u2019re\u00a0ready to reach higher, move faster, and do work that shapes the future space economy - this is your launchpad. Come build the future with Kepler!\u00a0\n\n\nWhat We Offer:\n* Competitive compensation\u00a0with a robust equity plan to share in our success.\u00a0\n* Comprehensive coverage for health, dental, and vision insurance\u2014including dependents.\u00a0\n* Unlimited vacation, supportive parental leave policy,\u00a0and company-wide holiday shutdown.\u00a0\n* Semi-annual company-wide parties\u00a0and frequent in-office team events.\u00a0\n* Relocation packages\u00a0available for approved roles.\u00a0\n* $1,500 annual professional development fund\u00a0to support your growth.\u00a0\n* Fully stocked Toronto office kitchen\u00a0with snacks, drinks, games and top-notch kitchen appliances.\u00a0\n* Town Halls, Celebration Calls, and Company-wide events\u00a0to stay connected and engaged.\u00a0\n* We\u2019re a certified\u00a0Great Place to Work\u00ae, five years in a row!\n",
    "descriptionBody": "<div><span style=\"font-size: 16px;\">Kepler is hiring a </span><b style=\"font-size: 16px;\">Director of Sales</b><span style=\"font-size: 16px;\"> to lead the growth of our satellite communications and space infrastructure solutions across Canadian and allied government sectors. This individual will own customer relationships and strategic capture activities with defense and government organizations looking to leverage Kepler\u2019s secure, low latency space network with advanced compute for routing mission critical data. This role blends technical solutioning with strategic account leadership and will be instrumental in shaping how national customers access, move, and compute data in space.&nbsp;</span></div>",
    "descriptionBodyPlain": "Kepler is hiring a Director of Sales to lead the growth of our satellite communications and space infrastructure solutions across Canadian and allied government sectors. This individual will own customer relationships and strategic capture activities with defense and government organizations looking to leverage Kepler\u2019s secure, low latency space network with advanced compute for routing mission critical data. This role blends technical solutioning with strategic account leadership and will be instrumental in shaping how national customers access, move, and compute data in space.\u00a0\n",
    "hostedUrl": "https://jobs.lever.co/kepler/0d614893-12fb-4daf-9491-dda0d09681cb",
    "applyUrl": "https://jobs.lever.co/kepler/0d614893-12fb-4daf-9491-dda0d09681cb/apply"
}
'''

