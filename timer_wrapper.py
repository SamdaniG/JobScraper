from functools import wraps
import time

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

            if isinstance(output, tuple) and len(output) == 4:
                name, _, _, job_board = output
                # job_board = args[0]().jobBoard

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
