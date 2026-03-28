from scrapers.__base import ApiJobBoardScraper
import argparse
# from log_starter import set_logger

def format_job_board_registry():
    lines = []
    lines.append("\t\t\tAVAILABLE JOB BOARDS ")
    lines.append("=" * 80)

    for board, scrapers in ApiJobBoardScraper.job_board_registry.items():
        lines.append(f"\t\t{board} ({len(scrapers)})")
        lines.append(" •".join(x.name for x in scrapers))

    lines.append("\n" + "="*80)
    return "\n".join(lines)


def cli_main():
    parser = argparse.ArgumentParser(
        description=f"Job scraper runner. \n"
                    f"{format_job_board_registry()}",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--source",
        default="manual",
        help="Who triggered the script (manual, scheduler, api, ci, etc.)"
    )
    parser.add_argument(
        "--company",
        nargs="+",
        help="Run specific company scrapers"
    )
    parser.add_argument(
        "--jobboard",
        help="Run all scrapers under a specific job board"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all job boards and their companies"
    )
    args = parser.parse_args()
    if args.list:
        print(format_job_board_registry())
        exit(0)
    #
    # logger=set_logger(args)

    if args.company and args.jobboard:
        raise ValueError("Use either --company or --jobboard, not both.")

    if args.company:
        scrapers_to_run = []

        for c in args.company:
            c = c.lower()
            if c not in ApiJobBoardScraper.registry:
                available = ", ".join(ApiJobBoardScraper.registry.keys())
                raise ValueError(f"Unknown scraper: {c}.\n "
                                 f"{format_job_board_registry()}")

            scrapers_to_run.append(ApiJobBoardScraper.registry[c])

    elif args.jobboard:
        jobboard = args.jobboard.lower()

        if jobboard not in ApiJobBoardScraper.job_board_registry:
            available = ", ".join(ApiJobBoardScraper.job_board_registry.keys())
            raise ValueError(
                f"Unknown job board: {jobboard}. \n"
                f"{format_job_board_registry()}"
            )

        scrapers_to_run = list(ApiJobBoardScraper.job_board_registry[jobboard])

    else:
        scrapers_to_run = list(ApiJobBoardScraper.registry.values())
    #
    # logger.info(
    #     "Running %d scraper(s) | mode=%s",
    #     len(scrapers_to_run),
    #     "company" if args.company else "jobboard" if args.jobboard else "all"
    # )

    return args, scrapers_to_run

