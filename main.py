import email_info as ei
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from json import JSONDecodeError

from selenium import webdriver
from selenium.webdriver.common.by import By
import hashlib
import json
from datetime import date, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



url="https://jobs.lever.co/waabi"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver=webdriver.Chrome(options=chrome_options)

driver.get(url=url)
driver.maximize_window()


with open("db.json","r") as f:
    try:
        db=json.load(f)
    except JSONDecodeError:
        db={}

# print(type(db))
# print(db.keys())

def get_text_or_none(parent, by, value):
    elems = parent.find_elements(by, value)
    return elems[0].text.strip() if elems else "meh"

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:10]

def send_email(subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = formataddr(("Waabi Job Alert", ei.email))
    msg["To"] = ei.receivers_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(ei.host_address, ei.port_address) as connection:
        connection.starttls()
        connection.login(user=ei.email, password=ei.password)
        connection.send_message(msg)

def diff_jobs(db: dict, current_jobs: list, today: date):
    new_jobs = []
    filled_jobs = []

    for job_id in current_jobs:
        if job_id not in db:
            new_jobs.append(job_id)

    for job_id in db.keys():
        if job_id not in current_jobs and db[job_id]["filled_date"] == "":
            db[job_id]["filled_date"] = (
                today - timedelta(days=1)
            ).strftime("%a %d-%b-%Y")
            filled_jobs.append(job_id)

    return new_jobs, filled_jobs

#db={}

wait = WebDriverWait(driver, 10)

job_titles = wait.until(
    EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "posting-title")
    )
)


current_jobs=[]
new_job_alert=[]
old_job_filled_alert=[]
"""
for index,job_title in enumerate(job_titles):
    url=job_title.get_attribute("href")
    job_id=sha256_hex(url)
    #print(f"{url}\t{job_id}")
    current_jobs.append(job_id)
    if job_id not in db.keys():
    # print(f"{url}\n{job_id}")
        db[job_id]=dict()
        # db[job_id]["index"]=index
        db[job_id]["job_name"]=get_text_or_none(job_title,By.CSS_SELECTOR,"h5")
        db[job_id]["work_policy"]=get_text_or_none(job_title,By.CSS_SELECTOR,".workplaceTypes")[:-2]
        db[job_id]["location"]=get_text_or_none(job_title,By.CSS_SELECTOR,".location")
        db[job_id]["commitment"]=get_text_or_none(job_title,By.CSS_SELECTOR,".commitment")
        db[job_id]["posted_date"]=date.today().strftime("%a %d-%b-%Y")
        db[job_id]["filled_date"]=""
        db[job_id]["url"]=url
        new_job_alert.append(job_id)

        # print(json.dumps(db[job_id], indent=4))


    # if index>3:
    #     break

for old_job in db.keys():
    if old_job not in current_jobs and db[old_job]["filled_date"]=="":
        db[old_job]["filled_date"]=(date.today() - timedelta(days=1)).strftime("%a %d-%b-%Y")
        old_job_filled_alert.append(old_job)
"""



for job_title in job_titles:
    url = job_title.get_attribute("href")
    job_id = sha256_hex(url)
    current_jobs.append(job_id)

    if job_id not in db.keys():
    # print(f"{url}\n{job_id}")
        db[job_id]=dict()
        # db[job_id]["index"]=index
        db[job_id]["job_name"]=get_text_or_none(job_title,By.CSS_SELECTOR,"h5")
        db[job_id]["work_policy"]=get_text_or_none(job_title,By.CSS_SELECTOR,".workplaceTypes")[:-2]
        db[job_id]["location"]=get_text_or_none(job_title,By.CSS_SELECTOR,".location")
        db[job_id]["commitment"]=get_text_or_none(job_title,By.CSS_SELECTOR,".commitment")
        db[job_id]["posted_date"]=date.today().strftime("%a %d-%b-%Y")
        db[job_id]["filled_date"]=""
        db[job_id]["url"]=url

new_job_alert, old_job_filled_alert = diff_jobs(
    db=db,
    current_jobs=current_jobs,
    today=date.today()
)

# print(json.dumps(db,indent=4))
print(f"{old_job_filled_alert= }\n{new_job_alert= }")

# if old_job_filled_alert:
#     info=""
#     for filled_job in old_job_filled_alert:
#         info+=db[filled_job]["job_name"]
#         info+="\n"


if old_job_filled_alert:
    body = "\n".join(db[j]["job_name"] for j in old_job_filled_alert)
    send_email("Waabi Filled Positions", body)

for new_job in new_job_alert:
    #getting the jd
    driver.switch_to.new_window('tab')
    driver.get(url=db[new_job]["url"])

    info = ""
    #descriptions = driver.find_elements(By.CLASS_NAME, value="section-wrapper")
    descriptions =    wait.until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "section-wrapper")
        )
    )
    for desc in descriptions:
        info += desc.text

    send_email(
        f"Waabi {db[new_job]['job_name']}",
        info
    )

    # msg = EmailMessage()
    # #msg["From"] = ei.email
    # msg["From"]= formataddr(("Waabi Job Alert",ei.email))
    # msg["To"] = ei.receivers_email
    # msg["Subject"] = f"Waabi {db[new_job]['job_name']}"
    # msg.set_content(info)
    #
    # with smtplib.SMTP(ei.host_address,ei.port_address) as connection:
    #     connection.starttls()
    #     connection.login(user=ei.email,password=ei.password)
    #     connection.set_debuglevel(1)
    #     connection.send_message(msg)

with open("db.json","w") as f:
    json.dump(db,f,indent=4)
driver.quit()
