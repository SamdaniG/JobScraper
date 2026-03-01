import json

from scrapers.base import ApiJobBoardScraper, Job
import requests as rq
from utils import sha256_hex
from datetime import datetime

DATE_FMT = "%a %d-%b-%Y"

class WaabiScraper(ApiJobBoardScraper):
    name='waabi'
    base_domain = f'https://api.lever.co/v0/postings/{name}'
    param = {
        'mode':'json',
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
            url = job['hostedUrl']
            hash_id=sha256_hex(url)
            current_jobs_id.append(hash_id)

            job_deets=Job(
                job_id=     job_id,
                job_name=   job_title,
                source=     self.name,
                location=job["categories"].get('allLocations',''),
                posted_date=(datetime.fromtimestamp(job['createdAt'] / 1000)).strftime(DATE_FMT),
                url=        url,
                work_policy=job["workplaceType"]
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
    test=WaabiScraper()
    yo,yol = test.scrape_jobs()
    # print(yo)
    # print(yol)
    print(json.dumps(yol['236263088d'],indent=4))

    jd_test=test.scrape_jd(source=yol['236263088d'])
    # print(jd_test)


'''Sample Skeleton
{
    "additionalPlain": "The US hourly range for this role is: $60 USD and the Canada hourly range for this role is: $60-$65 CAD in addition to competitive perks & benefits. Waabi US Inc. and Waabi Canada Inc.'s yearly salary ranges are determined based on several factors in accordance with the Company\u2019s compensation practices. The salary base range is reflective of the minimum and maximum target for new hire salaries for the position across all US and Canada locations.\u00a0\n\n\nPerks/Benefits:\nWaabi provides a competitive benefits package that includes:\n- Daily drinks, snacks and catered meals (when in office)\n- Regularly scheduled team building activities and social events\n- As we grow, this list continues to evolve!\u00a0\n\nWaabi is a technology start-up building technologies to transform the way the world moves. Join our talented team to be a part of the future and to make an impact!\n\nWaabi is an equal opportunity employer. We celebrate diversity and are committed to creating a supportive, inclusive, and accessible workplace for all our employees. We seek applicants of all backgrounds and identities, across race, color, ethnicity, national origin or ancestry, age, citizenship, religion, sex, sexual orientation, gender identity or expression, military or veteran status, marital status, pregnancy or parental status, caregiver status, disability, or any other characteristic protected by law. We make workplace accommodations for qualified individuals with disabilities as required by applicable law. If reasonable accommodation is needed to participate in the job application or interview process please let our recruiting team know.\n\n",
    "additional": "<div><span style=\"font-size: 16px;\">The US hourly range for this role is: $60 USD and the Canada hourly range for this role is: $60-$65 CAD in addition to competitive perks &amp; benefits. Waabi US Inc. and Waabi Canada Inc.'s yearly salary ranges are determined based on several factors in accordance with the Company\u2019s compensation practices. The salary base range is reflective of the minimum and maximum target for new hire salaries for the position across all US and Canada locations.&nbsp;</span></div><div><br></div><div><b><span style=\"font-size: 16px\">Perks/Benefits:</span></b></div><div><span style=\"font-size: 16px\">Waabi provides a competitive benefits package that includes:</span></div><div><span style=\"font-size: 16px\">- Daily drinks, snacks and catered meals (when in office)</span></div><div><span style=\"font-size: 16px\">- Regularly scheduled team building activities and social events</span></div><div><span style=\"font-size: 16px\">- As we grow, this list continues to evolve!&nbsp;</span></div><div><br></div><div><span style=\"font-size: 16px\">Waabi is a technology start-up building technologies to transform the way the world moves. Join our talented team to be a part of the future and to make an impact!</span></div><div><br></div><div><span style=\"font-size: 16px\">Waabi is an equal opportunity employer. We celebrate diversity and are committed to creating a supportive, inclusive, and accessible workplace for all our employees. We seek applicants of all backgrounds and identities, across race, color, ethnicity, national origin or ancestry, age, citizenship, religion, sex, sexual orientation, gender identity or expression, military or veteran status, marital status, pregnancy or parental status, caregiver status, disability, or any other characteristic protected by law. We make workplace accommodations for qualified individuals with disabilities as required by applicable law. If reasonable accommodation is needed to participate in the job application or interview process please let our recruiting team know.</span></div><div><br></div>",
    "categories": {
        "commitment": "Intern",
        "department": "Internships / Co-ops",
        "location": "Toronto, ON",
        "team": "Research",
        "allLocations": [
            "Toronto, ON",
            "Pittsburgh, PA",
            "San Francisco, CA"
        ]
    },
    "createdAt": 1766095153993,
    "descriptionPlain": "Waabi, founded by AI visionary Raquel Urtasun, is the leader in Physical AI. With a world-class team, we're unlocking the next era of autonomous transportation with technology that's powering commercial autonomous trucks and robotaxis. Waabi is backed by and partners with world leaders in AI, automotive, logistics, and deep tech.\n\nWith offices in Toronto, San Francisco, Dallas, and Pittsburgh, Waabi is growing quickly and looking for diverse, innovative and collaborative candidates who want to impact the world in a positive way. To learn more visit: www.waabi.ai\n\n\nYou will...\n- Be part of a team of multidisciplinary Research Scientists and Engineers using an AI-first approach to enable safe self-driving at scale.\n-\u00a0Lead or Contribute to an AI research project, pushing the frontiers of the field by developing new algorithms for Autonomous Vehicle (AV). This includes topics such as perception, prediction, motion planning, controls, simulation, mapping, localization, core AI, etc.\n- Design, implement, train, and optimize novel algorithms on self-driving vehicles and various production systems.\u00a0\n- Be encouraged to submit and publish work externally at top machine learning, computer vision, and robotics conferences (NeurIPS, ICLR, ICML, CVPR, etc.), post to our company blog.\n\nQualifications:\n- Pursuing PhD degree in Computer Science, Engineering, AI, Machine Learning, Computer Vision, Robotics and/or similar technical field(s) of study.\n- Demonstrated research/software engineering experience: through previous internships, work experience, coding competitions, and/or research projects and papers.\n- At least one publication in top Machine Learning, Computer Vision, or Robotics conferences. \n- Strong quantitative background and coursework in or working knowledge of linear algebra, calculus, and probability.\n- Proficient in reading and coding in Python and/or C++..\n- Open-minded and collaborative team player with willingness to help others.\n- Passionate about self-driving technologies, solving hard problems, and creating innovative solutions.\n\nApplication Instructions:\n- To be considered for an internship/co-op, please add your most up to date academic transcripts alongside with your resume for further review.\n",
    "description": "<div><span style=\"font-size: 16px;\">Waabi, founded by AI visionary Raquel Urtasun, is the leader in Physical AI. With a world-class team, we're unlocking the next era of autonomous transportation with technology that's powering commercial autonomous trucks and robotaxis. Waabi is backed by and partners with world leaders in AI, automotive, logistics, and deep tech.</span></div><div><br></div><div><span style=\"font-size: 16px\">With offices in Toronto, San Francisco, Dallas, and Pittsburgh, Waabi is growing quickly and looking for diverse, innovative and collaborative candidates who want to impact the world in a positive way. To learn more visit: </span><a style=\"font-size: 16px\" href=\"http://www.waabi.ai\">www.waabi.ai</a></div><div><br></div><div><b style=\"font-size: 16px;\">You will...</b></div><div><span style=\"font-size: 16px;\">- Be part of a team of multidisciplinary Research Scientists and Engineers using an AI-first approach to enable safe self-driving at scale.</span></div><div><span style=\"font-size: 16px;\">-&nbsp;Lead or Contribute to an AI research project, pushing the frontiers of the field by developing new algorithms for Autonomous Vehicle (AV). This includes topics such as perception, prediction, motion planning, controls, simulation, mapping, localization, core AI, etc.</span></div><div><span style=\"font-size: 16px;\">- Design, implement, train, and optimize novel algorithms on self-driving vehicles and various production systems.&nbsp;</span></div><div><span style=\"font-size: 16px;\">- Be encouraged to submit and publish work externally at top machine learning, computer vision, and robotics conferences (NeurIPS, ICLR, ICML, CVPR, etc.), post to our company blog.</span></div><div><br></div><div><b style=\"font-size: 16px;\">Qualifications:</b></div><div><span style=\"font-size: 16px;\">- Pursuing PhD degree in Computer Science, Engineering, AI, Machine Learning, Computer Vision, Robotics and/or similar technical field(s) of study.</span></div><div><span style=\"font-size: 16px;\">- Demonstrated research/software engineering experience: through previous internships, work experience, coding competitions, and/or research projects and papers.</span></div><div><span style=\"font-size: 16px;\">- At least one publication in top Machine Learning, Computer Vision, or Robotics conferences. </span></div><div><span style=\"font-size: 16px;\">- Strong quantitative background and coursework in or working knowledge of linear algebra, calculus, and probability.</span></div><div><span style=\"font-size: 16px;\">- Proficient in reading and coding in Python and/or C++..</span></div><div><span style=\"font-size: 16px;\">- Open-minded and collaborative team player with willingness to help others.</span></div><div><span style=\"font-size: 16px;\">- Passionate about self-driving technologies, solving hard problems, and creating innovative solutions.</span></div><div><br></div><div><b style=\"font-size: 16px;\">Application Instructions:</b></div><div><b style=\"font-size: 16px;\">- </b><span style=\"font-size: 16px;\">To be considered for an internship/co-op, please add your most up to date academic transcripts alongside with your resume for further review.</span></div>",
    "id": "62700386-b9db-4c78-aec3-5ef59cbe841e",
    "lists": [],
    "text": "2026 Intern, PhD Research Scientist",
    "country": "CA",
    "workplaceType": "onsite",
    "opening": "<div><span style=\"font-size: 16px;\">Waabi, founded by AI visionary Raquel Urtasun, is the leader in Physical AI. With a world-class team, we're unlocking the next era of autonomous transportation with technology that's powering commercial autonomous trucks and robotaxis. Waabi is backed by and partners with world leaders in AI, automotive, logistics, and deep tech.</span></div><div><br></div><div><span style=\"font-size: 16px\">With offices in Toronto, San Francisco, Dallas, and Pittsburgh, Waabi is growing quickly and looking for diverse, innovative and collaborative candidates who want to impact the world in a positive way. To learn more visit: </span><a href=\"http://www.waabi.ai\" style=\"font-size: 16px\">www.waabi.ai</a></div>",
    "openingPlain": "Waabi, founded by AI visionary Raquel Urtasun, is the leader in Physical AI. With a world-class team, we're unlocking the next era of autonomous transportation with technology that's powering commercial autonomous trucks and robotaxis. Waabi is backed by and partners with world leaders in AI, automotive, logistics, and deep tech.\n\nWith offices in Toronto, San Francisco, Dallas, and Pittsburgh, Waabi is growing quickly and looking for diverse, innovative and collaborative candidates who want to impact the world in a positive way. To learn more visit: www.waabi.ai\n",
    "descriptionBody": "<div><b style=\"font-size: 16px;\">You will...</b></div><div><span style=\"font-size: 16px;\">- Be part of a team of multidisciplinary Research Scientists and Engineers using an AI-first approach to enable safe self-driving at scale.</span></div><div><span style=\"font-size: 16px;\">-&nbsp;Lead or Contribute to an AI research project, pushing the frontiers of the field by developing new algorithms for Autonomous Vehicle (AV). This includes topics such as perception, prediction, motion planning, controls, simulation, mapping, localization, core AI, etc.</span></div><div><span style=\"font-size: 16px;\">- Design, implement, train, and optimize novel algorithms on self-driving vehicles and various production systems.&nbsp;</span></div><div><span style=\"font-size: 16px;\">- Be encouraged to submit and publish work externally at top machine learning, computer vision, and robotics conferences (NeurIPS, ICLR, ICML, CVPR, etc.), post to our company blog.</span></div><div><br></div><div><b style=\"font-size: 16px;\">Qualifications:</b></div><div><span style=\"font-size: 16px;\">- Pursuing PhD degree in Computer Science, Engineering, AI, Machine Learning, Computer Vision, Robotics and/or similar technical field(s) of study.</span></div><div><span style=\"font-size: 16px;\">- Demonstrated research/software engineering experience: through previous internships, work experience, coding competitions, and/or research projects and papers.</span></div><div><span style=\"font-size: 16px;\">- At least one publication in top Machine Learning, Computer Vision, or Robotics conferences. </span></div><div><span style=\"font-size: 16px;\">- Strong quantitative background and coursework in or working knowledge of linear algebra, calculus, and probability.</span></div><div><span style=\"font-size: 16px;\">- Proficient in reading and coding in Python and/or C++..</span></div><div><span style=\"font-size: 16px;\">- Open-minded and collaborative team player with willingness to help others.</span></div><div><span style=\"font-size: 16px;\">- Passionate about self-driving technologies, solving hard problems, and creating innovative solutions.</span></div><div><br></div><div><b style=\"font-size: 16px;\">Application Instructions:</b></div><div><b style=\"font-size: 16px;\">- </b><span style=\"font-size: 16px;\">To be considered for an internship/co-op, please add your most up to date academic transcripts alongside with your resume for further review.</span></div>",
    "descriptionBodyPlain": "You will...\n- Be part of a team of multidisciplinary Research Scientists and Engineers using an AI-first approach to enable safe self-driving at scale.\n-\u00a0Lead or Contribute to an AI research project, pushing the frontiers of the field by developing new algorithms for Autonomous Vehicle (AV). This includes topics such as perception, prediction, motion planning, controls, simulation, mapping, localization, core AI, etc.\n- Design, implement, train, and optimize novel algorithms on self-driving vehicles and various production systems.\u00a0\n- Be encouraged to submit and publish work externally at top machine learning, computer vision, and robotics conferences (NeurIPS, ICLR, ICML, CVPR, etc.), post to our company blog.\n\nQualifications:\n- Pursuing PhD degree in Computer Science, Engineering, AI, Machine Learning, Computer Vision, Robotics and/or similar technical field(s) of study.\n- Demonstrated research/software engineering experience: through previous internships, work experience, coding competitions, and/or research projects and papers.\n- At least one publication in top Machine Learning, Computer Vision, or Robotics conferences. \n- Strong quantitative background and coursework in or working knowledge of linear algebra, calculus, and probability.\n- Proficient in reading and coding in Python and/or C++..\n- Open-minded and collaborative team player with willingness to help others.\n- Passionate about self-driving technologies, solving hard problems, and creating innovative solutions.\n\nApplication Instructions:\n- To be considered for an internship/co-op, please add your most up to date academic transcripts alongside with your resume for further review.\n",
    "hostedUrl": "https://jobs.lever.co/waabi/62700386-b9db-4c78-aec3-5ef59cbe841e",
    "applyUrl": "https://jobs.lever.co/waabi/62700386-b9db-4c78-aec3-5ef59cbe841e/apply"
}

'''