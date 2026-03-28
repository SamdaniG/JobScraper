import time
from diff import diff_jobs, updating_db
from storage import load_db, save_db
from log_starter import set_logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from cli.main import cli_main
from notifications.notify import notify

def time_taken(func):
    """This is a python decorator to calculate the time taken to run every function, gives us a useful metric to keep track"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = kwargs.get("logger")
        start = time.perf_counter()
        # print(f"Started the timer!")
        output = func(*args, **kwargs)
        if isinstance(output, tuple) and len(output) == 3:
            name, result, error = output
        else:
            name = func.__name__

        end = time.perf_counter()
        logger.timer(f"Time taken to run the {name}: {end - start:.4f}s",
                     extra={
                         "source": name,
                         "timer": end - start
                     })
        return output
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
    EMAIL_ACTIVE = False
    if args.source == 'scheduler':
        EMAIL_ACTIVE = True

    # Initiating variables
    db = load_db()
    # all_current_job_ids = set()
    all_scraped_jobs = {}
    successful_scrapers = set()

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

    logger.info(f"Checking the new/old jobs created.")
    new_jobs, filled_jobs, updated_jobs = diff_jobs(db, all_scraped_jobs, successful_scrapers, )
    logger.info(
        "Diff complete | new_jobs=%d filled_jobs=%d updated_jobs=%d",
        len(new_jobs),
        len(filled_jobs),
        len(updated_jobs)
    )

    db = updating_db(db, all_scraped_jobs, new_jobs, updated_jobs, logger)

    notify(db, scrapers_to_run, filled_jobs, new_jobs, logger, EMAIL_ACTIVE)

    logger.info(f"Writing data to my database!\n-------------------")
    save_db(db)


if __name__=='__main__':
    args, scrapers_to_run = cli_main()
    logger = set_logger(args)

    main(args, scrapers_to_run, logger=logger)
