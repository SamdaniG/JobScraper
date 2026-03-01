from pathlib import Path
import  logging.config
import json

def set_logger(args):
    """This sets up the logging module!"""
    parent_dir=Path(__file__).resolve().parent
    logs_dir = parent_dir / "logs"
    logs_dir.mkdir(exist_ok=True)

    config_file = logs_dir / "log_config.json"

    if args.source == 'scheduler':
        log_file = logs_dir / f"scheduler_logs.log"
    else:
        log_file = logs_dir/ f"logs.log"

    with open(config_file, "r") as f:
        logging_config = json.load(f)

    logging_config["handlers"]["file"]["filename"] = log_file
    logging.config.dictConfig(config=logging_config)
    #logger = logging.getLogger("scraper")
    logger = logging.LoggerAdapter(
        logging.getLogger("scraper"),
        {"executor": args.source}
    )
    #logger.info("Script started")
    return logger