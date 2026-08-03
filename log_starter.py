from pathlib import Path
import  logging.config
import json
import logging
from datetime import datetime
from logs_db import initialize, get_connection

LOG_DB = Path(__file__).resolve().parent / "logs" / "logs.db"

NEW_LEVEL = 25
UPDATED_LEVEL = 26
FILLED_LEVEL = 27
TIMER_LEVEL = 28

logging.addLevelName(NEW_LEVEL, "NEW")
logging.addLevelName(UPDATED_LEVEL, "UPDATED")
logging.addLevelName(FILLED_LEVEL, "FILLED")
logging.addLevelName(TIMER_LEVEL, "TIMER")

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
    json_log_file = logs_dir / "event_logs.jsonl"
    logging_config["handlers"]["file"]["filename"] = str(log_file)
    logging_config["handlers"]["json_file"]["filename"] = str(json_log_file)

    timer_log_file = logs_dir / "timer.jsonl"
    logging_config["handlers"]["timer_file"]["filename"] = str(timer_log_file)
    initialize()
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

    def timer(self, msg, *args, **kwargs):
        self.log(TIMER_LEVEL, msg, *args, **kwargs)

    def process(self, msg, kwargs):
        # get extra passed in log call
        extra = kwargs.get("extra", {})

        # merge with adapter-level extra
        kwargs["extra"] = {**self.extra, **extra}

        return msg, kwargs

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "event":            record.levelname,  # or use record.event if you prefer
            "hash_id":           getattr(record, "hash_id", None),
            "job_name":         getattr(record, "job_name", None),
            "location":         getattr(record, "location", None),
            "source":           getattr(record, "source", None),
            "executor":         getattr(record, "executor", None),
            "timestamp": datetime.utcnow().isoformat()
        }

        # Only for UPDATED
        if record.levelname == "UPDATED":
            log_record.update({
                "field":        getattr(record, "field", None),
                "old_val":      getattr(record, "old_val", None),
                "new_val":      getattr(record, "new_val", None),
            })

        return json.dumps(log_record)

class JsonTimerFormatter(logging.Formatter):
    def format(self, record):
        timer_record = {
            "source":           getattr(record, "source", None),
            "time_taken":       getattr(record, "timer", None),
            "timestamp":        datetime.utcfromtimestamp(record.created).isoformat()
        }
        if hasattr(record, "jobBoard"):
            timer_record["job_board"] = record.jobBoard

        if hasattr(record, "scraper_count"):
            timer_record["scrapers_run"] = record.scraper_count

        if hasattr(record, "executor"):
            timer_record["executor"] = record.executor

        return json.dumps(timer_record)

class EventOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {25, 27}

class TimerOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {28}

class NoTimerFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != TIMER_LEVEL

class LogsFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {25, 26, 27}


class SQLiteHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        try:
            with get_connection(LOG_DB) as conn:
                conn.execute(
                    """
                    INSERT INTO timers (
                        timestamp,
                        source,
                        job_board,
                        executor,
                        time_taken,
                        scraper_count
                    )
                    VALUES (?,?,?,?,?,?)
                    """,
                    (
                        datetime.utcfromtimestamp(record.created).isoformat(),
                        getattr(record, "source", None),
                        getattr(record, "jobBoard", None),
                        getattr(record, "executor", None),
                        getattr(record, "timer", None),
                        getattr(record, "scraper_count", None),
                    )
                )
        except Exception as e:
            self.handleError(record)

class HistorySQLHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        try:
            with get_connection(LOG_DB) as conn:
                conn.execute(
                    """
                    INSERT INTO history (
                        hash_id,
                        job_name,
                        
                        source,
                        event,
                        
                        field,
                        old_val,
                        
                        new_val,       
                        timestamp
                    )
                    VALUES (?,?,?,?,?,?,?,?)
                    """,
                    (
                        getattr(record, "hash_id", None),
                        getattr(record, "job_name", None),

                        getattr(record, "source", None),
                        getattr(record, "levelname", None),

                        getattr(record, "field", None),
                        getattr(record, "old_val", None),

                        getattr(record, "new_val", None),
                        datetime.utcfromtimestamp(record.created).isoformat()
                    )
                )
        except Exception as e:
            self.handleError(record)
