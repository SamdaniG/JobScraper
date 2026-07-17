from scrapers.__base import ApiJobBoardScraper
import argparse
# from log_starter import set_logger
from storage import get_connection
import json
from tabulate import tabulate
from storage import load_db

def format_job_board_registry():
    lines = []
    lines.append(f"\t\t\tAVAILABLE JOB BOARDS {len(ApiJobBoardScraper.registry)}")
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
        "--source","-s",
        default="manual",
        help="Who triggered the script (manual, scheduler, api, ci, etc.)"
    )
    parser.add_argument(
        "--company","-c",
        nargs="+",
        help="Run specific company scrapers"
    )
    parser.add_argument(
        "--jobboard","-j",
        help="Run all scrapers under a specific job board"
    )
    parser.add_argument(
        "--list","-l",
        action="store_true",
        help="List all job boards and their companies"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Run SQL query on jobs database"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print query results"
    )
    parser.add_argument(
        "--format",
        choices=["pretty", "grid", "github", "psql", "simple", "heavy_grid"],
        default="pretty",
        help="Output format for query results"
    )
    parser.add_argument(
        "--jd","-jd",
        type = str,
        nargs= "+",
        help="Get the job description from a valid hash_id!"
    )

    args = parser.parse_args()
    if args.list:
        print(format_job_board_registry())
        exit(0)

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

    if args.query:
        conn = get_connection()

        # Make output readable
        conn.row_factory = lambda cursor, row: {
            col[0]: row[idx] for idx, col in enumerate(cursor.description)
        }

        cursor = conn.cursor()

        try:
            cursor.execute(args.query)
            rows = cursor.fetchall()
            if args.pretty:
                print(tabulate(rows, headers="keys", tablefmt=args.format))
            else:
                print(json.dumps(rows, indent=4))
        except Exception as e:
            print("❌ SQL Error:", e)

        conn.close()
        exit(0)

    if args.jd:
        # print(f"{args.jd= }, {len(args.jd)= }")
        db=load_db()
        db_keys=set(db)
        # print(list(db)[:10])
        # id_set=set(load_db())
        for id in args.jd:
            # print(i)
            if id not in db_keys:
                print(f"{id} is an incorrect hash_id!")
            elif db[id].get("filled_date", None) is not None:
                print(f"{id}: {db[id]["job_name"]} - This job has been closed!")
            else:
                source_name=db[id]["source"]
                scraper=ApiJobBoardScraper.registry[source_name]()
                # yo=scraper.scrape_jobs()
                try:
                    jd = scraper.scrape_jd(db[id])
                    print(f"\n{'=' * 70}")
                    print(f"Hash ID  : {id}")
                    print(f"Company  : {source_name}")
                    print(f"URL      : {db[id]['url']}")
                    print(f"{'=' * 70}\n")
                    print(jd)
                except Exception as e:
                    print(f"{id}: We could not scrape the jd currrently due to: {e}")


        exit(0)


    return args, scrapers_to_run

