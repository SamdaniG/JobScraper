# emailer.py
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import email_info as ei

def send_email(subject: str, body: str, source:str = ""):
    msg = EmailMessage()
    msg["From"] = formataddr((f"{source} Job Alert", ei.email))
    msg["To"] = ei.receivers_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(ei.host_address, ei.port_address) as connection:
        connection.starttls()
        connection.login(ei.email, ei.password)
        connection.send_message(msg)

