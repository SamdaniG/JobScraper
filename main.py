import time
from diff import diff_jobs, updating_db, normalize_job
from storage import load_db, save_db, init_db
from log_starter import set_logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from cli.main import cli_main
from notifications.emailer import send_email

def time_taken(func):
    """This is a python decorator to calculate the time taken to run every function, gives us a useful metric to keep track"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = kwargs.get("logger")
        start = time.perf_counter()
        output = None
        name = func.__name__
        try:
            output = func(*args, **kwargs)
            return output

        finally:
            scraper_count = None
            job_board = None

            if isinstance(output, tuple) and len(output) == 3:
                name, _, _ = output
                job_board = args[0]().jobBoard

            elif len(args) > 1:
                scrapers_to_run = args[1]
                scraper_count = len(scrapers_to_run)

            end = time.perf_counter()

            extra_data = {
                "source": name,
                "timer": end - start,
            }

            if scraper_count is not None:
                extra_data["scraper_count"] = scraper_count
            if job_board is not None:
                extra_data["jobBoard"] = job_board
            logger.timer(
                f"Time taken to run {name}: {end - start:.4f}s",
                extra=extra_data
            )
    return wrapper

@time_taken
def run_scraper(Scraper, logger= None):
    scraper = Scraper()
    try:
        scraped_jobs_db = scraper.scrape_jobs()
        return scraper.name, scraped_jobs_db, None
    except Exception as e:
        return scraper.name, None, e

@time_taken
def main(args, scrapers_to_run, logger= None):
    logger.info(
        "Running %d scraper(s) | mode=%s",
        len(scrapers_to_run),
        "company" if args.company else "jobboard" if args.jobboard else "all"
    )

    ####Activating Email
    EMAIL_ACTIVE = True
    if args.source == 'scheduler':
        EMAIL_ACTIVE = True

    # Initiating variables
    db = load_db()
    # all_current_job_ids = set()
    all_scraped_jobs = {}
    successful_scrapers = set()
    normalized_jobs = {}

    i = 1
    with ThreadPoolExecutor(max_workers=min(15, len(scrapers_to_run))) as executor:
        futures = [
            executor.submit(run_scraper, Scraper, logger=logger)
            for Scraper in scrapers_to_run
        ]

        for future in as_completed(futures):
            name, scraped_jobs_db, error = future.result()

            if error:
                logger.error(f"{name} failed: {error}")
                continue

            logger.info(f"{i:02d}: {name}")

            successful_scrapers.add(name)
            # all_current_job_ids.add(current_jobs_id)
            all_scraped_jobs.update(scraped_jobs_db)
            i += 1

    for job_id, scraped_job in all_scraped_jobs.items():
        old_job = db.get(job_id)

        normalized_jobs[job_id] = normalize_job(
            old_job,
            scraped_job
        )

    logger.info(f"Checking the new/old jobs created.")
    new_jobs, filled_jobs, updated_jobs = diff_jobs(db, normalized_jobs, successful_scrapers, )
    logger.info(
        "Diff complete | new_jobs=%d filled_jobs=%d updated_jobs=%d",
        len(new_jobs),
        len(filled_jobs),
        len(updated_jobs)
    )

    db = updating_db(db, normalized_jobs, new_jobs, updated_jobs, logger)
    send_individual_new_job = len(new_jobs)<= -1

    if filled_jobs:
        logger.debug("Processing filled jobs")

        lines = []
        html_lines = []

        for j in filled_jobs:
            job = db[j]

            logger.filled(
                f'{job["source"]} - '
                f'{str(job.get("job_id", ""))[:10]} - '
                f'{job["job_name"]}',
                extra={
                    "job_name": job["job_name"],
                    "source": job["source"],
                    "job_id": job.get("job_id", ""),
                    "location": job.get("location", "")
                }
            )

            if EMAIL_ACTIVE:
                lines.append(
                    f'{job["source"]} - '
                    f'{job.get("job_id", job["url"])} - '
                    f'{job["job_name"]}'
                )

                html_lines.append(
                    f'{job["source"]} - '
                    f'{job.get("job_id", job["url"])} - '
                    f'<a href="{job["url"]}">{job["job_name"]}</a>'
                )

        if EMAIL_ACTIVE:
            send_email(
                f"Filled Positions ({len(filled_jobs)})",
                "\n".join(lines),
                "<br>".join(html_lines),
                "System"
            )

    # 2️⃣ New jobs
    if new_jobs:
        logger.debug("Processing new jobs")

        if EMAIL_ACTIVE:
            scraper_map = {s.name: s() for s in scrapers_to_run}

        summary_links = []

        for job_id in new_jobs:
            job = db[job_id]

            logger.new(
                f'{job["source"]} - '
                f'{str(job.get("job_id", ""))[:10]} - '
                f'{job["job_name"]}',
                extra={
                    "job_name": job["job_name"],
                    "source": job["source"],
                    "job_id": job.get("job_id", ""),
                    "location": job.get("location", "")
                }
            )

            if not EMAIL_ACTIVE:
                continue

            scraper = scraper_map.get(job["source"])

            if not scraper:
                logger.warning(
                    "No scraper found for source=%s (job_id=%s)",
                    job["source"],
                    job_id
                )
                continue

            try:
                jd_content = (
                    scraper.scrape_jd(job)
                    if send_individual_new_job
                    else ""
                )

            except Exception as e:
                logger.error(
                    "JD scrape failed: %s for %s",
                    e,
                    job
                )
                continue

            text_body = job["url"] + "\n" + jd_content

            html_link = (
                f'<p>{job["source"]} - '
                f'<a href="{job["url"]}">{job["job_name"]}</a></p>'
            )

            summary_links.append(html_link)

            if send_individual_new_job:
                html_body = (
                        html_link +
                        f"<pre>{jd_content}</pre>"
                )

                send_email(
                    job["job_name"],
                    text_body,
                    html_body,
                    job["source"]
                )

        if EMAIL_ACTIVE and summary_links:
            send_email(
                f"New Jobs List ({len(new_jobs)})",
                "",
                "\n".join(summary_links),
                "new"
            )

    # logger.info(f"Writing data to my database!\n-------------------")
    logger.info(
        "Writing data to my database (N%d F%d U%d)",
        len(new_jobs),
        len(filled_jobs),
        len(updated_jobs)
    )
    save_db(db)

if __name__=='__main__':
    init_db()

    args, scrapers_to_run = cli_main()
    logger = set_logger(args)

    main(args, scrapers_to_run, logger=logger)
