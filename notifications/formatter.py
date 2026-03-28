def format_filled_jobs(db, filled_jobs, logger):
    text_lines = []
    html_lines = []

    for j in filled_jobs:
        job = db[j]

        logger.filled(
            f'{job["source"]} - {job.get("job_id","")} - {job["job_name"]}',
            extra={
                "job_name": job["job_name"],
                "source": job["source"],
                "job_id": job.get('job_id', ""),
                "location": job.get('location', "")
            }
        )

        text_lines.append(
            f'{job["source"]} - {job.get("job_id", job["url"])} - {job["job_name"]}'
        )

        html_lines.append(
            f'{job["source"]} - {job.get("job_id", job["url"])} - '
            f'<a href="{job["url"]}">{job["job_name"]}</a>'
        )

    return "\n".join(text_lines), "<br>".join(html_lines)

def process_new_jobs(db, new_jobs, scraper_map, logger):
    emails = []
    combined_html = []

    for job_id in new_jobs:
        job = db[job_id]
        scraper = scraper_map.get(job["source"])

        if not scraper:
            logger.warning(
                "No scraper found for source=%s (job_id=%s)",
                job["source"],
                job_id,
            )
            continue

        logger.new(
            f'{job["job_name"]} ({job["source"]}) ({job.get("job_id","")})',
            extra={
                "job_name": job["job_name"],
                "source": job["source"],
                "job_id": job.get('job_id', ""),
                "location": job.get('location', "")
            }
        )

        try:
            jd_content = scraper.scrape_jd(job)
        except Exception as e:
            logger.error(f"JD scrape failed: {e}")
            continue

        text_body = f"{job['url']}\n{jd_content}"

        html_link = (
            f'<p>{job["source"]} - '
            f'<a href="{job["url"]}">{job["job_name"]}</a></p>'
        )

        html_body = html_link + f"<pre>{jd_content}</pre>"

        emails.append((job["job_name"], text_body, html_body, job["source"]))
        combined_html.append(html_link)

    return emails, "\n".join(combined_html)