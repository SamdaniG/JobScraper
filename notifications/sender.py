import time
from notifications.emailer import send_email

EMAIL_DELAY_SECONDS = 5

def send_batch_email(subject, text_body, html_body, source, email_active):
    if not email_active:
        return
    send_email(subject, text_body, html_body, source)


def send_emails_with_delay(email_list, email_active):
    if not email_active:
        return

    for i, (subject, text, html, source) in enumerate(email_list):
        send_email(subject, text, html, source)

        if i < len(email_list) - 1:
            time.sleep(EMAIL_DELAY_SECONDS)