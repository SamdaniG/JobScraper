from pathlib import Path
import  logging.config
import json
import logging
from datetime import datetime

NEW_LEVEL = 25
UPDATED_LEVEL = 26
FILLED_LEVEL = 27

logging.addLevelName(NEW_LEVEL, "NEW")
logging.addLevelName(UPDATED_LEVEL, "UPDATED")
logging.addLevelName(FILLED_LEVEL, "FILLED")
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
    json_log_file = logs_dir / "logs.jsonl"
    logging_config["handlers"]["file"]["filename"] = str(log_file)
    logging_config["handlers"]["json_file"]["filename"] = str(json_log_file)

    logging.config.dictConfig(config=logging_config)
    #logger = logging.getLogger("scraper")
    # logger = logging.LoggerAdapter(
    #     logging.getLogger("scraper"),
    #     {"executor": args.source}
    # )
    logger = CustomLoggerAdapter(
        logging.getLogger("scraper"),
        {"executor": args.source}
    )
    #logger.info("Script started")
    return logger

class CustomLoggerAdapter(logging.LoggerAdapter):
    def new(self, msg, *args, **kwargs):
        self.log(NEW_LEVEL, msg, *args, **kwargs)

    def updated(self, msg, *args, **kwargs):
        self.log(UPDATED_LEVEL, msg, *args, **kwargs)

    def filled(self, msg, *args, **kwargs):
        self.log(FILLED_LEVEL, msg, *args, **kwargs)

    def process(self, msg, kwargs):
        # get extra passed in log call
        extra = kwargs.get("extra", {})

        # merge with adapter-level extra
        kwargs["extra"] = {**self.extra, **extra}

        return msg, kwargs

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp":        datetime.utcnow().isoformat(),
            "event":            record.levelname,  # or use record.event if you prefer
            "job_id":           getattr(record, "job_id", None),
            "job_name":         getattr(record, "job_name", None),
            "location":         getattr(record, "location", None),
            "source":           getattr(record, "source", None),
            "executor":         getattr(record, "executor", None),
        }

        # Only for UPDATED
        if record.levelname == "UPDATED":
            log_record.update({
                "field":        getattr(record, "field", None),
                "old_val":      getattr(record, "old_val", None),
                "new_val":      getattr(record, "new_val", None),
            })

        return json.dumps(log_record)

class EventOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {25, 27}