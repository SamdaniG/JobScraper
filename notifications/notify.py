# from emailer import send_email
# EMAIL_DELAY_SECONDS = 5
# import time

from notifications.formatter import format_filled_jobs, process_new_jobs
from notifications.sender import send_batch_email, send_emails_with_delay

def build_scraper_map(scrapers_to_run):
    return {s.name: s() for s in scrapers_to_run}

def notify(db, scrapers_to_run, filled_jobs, new_jobs, logger, email_active):
    scraper_map = build_scraper_map(scrapers_to_run)

    # 1️⃣ Filled jobs
    if filled_jobs:
        text_body, html_body = format_filled_jobs(db, filled_jobs, logger)
        send_batch_email("Filled Positions", text_body, html_body, "System", email_active)

    # 2️⃣ New jobs
    if new_jobs:
        emails, combined_html = process_new_jobs(
            db, new_jobs, scraper_map, logger
        )

        send_emails_with_delay(emails, email_active)

        send_batch_email(
            "New Jobs List",
            text_body="",
            html_body=combined_html,
            source="new",
            email_active=email_active
        )