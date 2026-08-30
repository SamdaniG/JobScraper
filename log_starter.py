from pathlib import Path
import  logging.config
import json
import logging
from datetime import datetime, timezone
from logs_db import logs_initialize, get_logs_connection, get_q_connection, q_initialize, summary_initialize, get_summary_connection
from utils import RunContext

NEW_LEVEL = 25
UPDATED_LEVEL = 26
FILLED_LEVEL = 27
TIMER_LEVEL = 28
FINISHED_LEVEL = 29

logging.addLevelName(NEW_LEVEL, "NEW")
logging.addLevelName(UPDATED_LEVEL, "UPDATED")
logging.addLevelName(FILLED_LEVEL, "FILLED")
logging.addLevelName(TIMER_LEVEL, "TIMER")
logging.addLevelName(FINISHED_LEVEL, "FINISHED")

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
    timer_log_file = logs_dir / "timer.jsonl"

    logging_config["handlers"]["file"]["filename"] = str(log_file)
    logging_config["handlers"]["json_file"]["filename"] = str(json_log_file)
    logging_config["handlers"]["timer_file"]["filename"] = str(timer_log_file)

    logs_initialize()
    q_initialize()
    summary_initialize()

    context = RunContext()

    logging.config.dictConfig(config=logging_config)

    logger = CustomLoggerAdapter(
        logging.getLogger("scraper"),
        {"executor": args.source},
        context
    )
    #logger.info("Script started")
    return logger

class CustomLoggerAdapter(logging.LoggerAdapter):

    def __init__(self, logger, extra, context):
        super().__init__(logger, extra)
        self.context = context

    def new(self, msg, *args, **kwargs):
        self.log(NEW_LEVEL, msg, *args, **kwargs)

    def updated(self, msg, *args, **kwargs):
        self.log(UPDATED_LEVEL, msg, *args, **kwargs)

    def filled(self, msg, *args, **kwargs):
        self.log(FILLED_LEVEL, msg, *args, **kwargs)

    def timer(self, msg, *args, **kwargs):
        self.log(TIMER_LEVEL, msg, *args, **kwargs)

    def finish(self, msg, *args, **kwargs):
        self.context.finished_at = datetime.now(timezone.utc)

        self.context.runtime = (
                self.context.finished_at - self.context.started_at
        ).total_seconds()

        self.log(FINISHED_LEVEL, msg, *args, **kwargs)

    def process(self, msg, kwargs):
        # get extra passed in log call
        extra = kwargs.get("extra", {})

        if extra.get("summary_flag"):
            self.context.summary = {
                "new": extra.get("new_jobs", 0),
                "filled": extra.get("filled_jobs", 0),
                "updated": extra.get("updated_jobs", 0),
            }

        kwargs["extra"] = {
            **self.extra,
            "uuid": self.context.uuid,
            "started_at": self.context.started_at.isoformat(),
            "finished_at": (
                self.context.finished_at.isoformat()
                if self.context.finished_at
                else None
            ),
            "runtime": getattr(self.context, "runtime", None),
            **extra
        }

        if self.context.summary:
            kwargs["extra"]["summary"] = self.context.summary

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
            "timestamp": datetime.utcnow().isoformat(),
            "uuid": getattr(record, "uuid", None),
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
            "timestamp":        datetime.utcfromtimestamp(record.created).isoformat(),
            "uuid":         getattr(record, "uuid", None),
        }
        if hasattr(record, "jobBoard"):
            timer_record["job_board"] = record.jobBoard

        if hasattr(record, "scraper_count"):
            timer_record["scrapers_run"] = record.scraper_count

        if hasattr(record, "executor"):
            timer_record["executor"] = record.executor

        return json.dumps(timer_record)

class TimerSQLHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.events = {}
        self.flag = False

    def emit(self, record):
        uuid = getattr(record, "uuid", None)

        if not uuid:
            return

        if uuid not in self.events:
            self.events[uuid] = []

        if record.levelno == TIMER_LEVEL:
            self.events[uuid].append(record)

        elif record.levelno == FINISHED_LEVEL:
            self._flush(uuid)
            self.flag = True

        if self.flag:
            self._flush(uuid)

    def _flush(self, uuid):

        events = self.events.pop(uuid, None)

        if not events:
            return

        try:
            with get_logs_connection() as conn:

                conn.executemany(
                    """
                    INSERT INTO timers (
                        timestamp,
                        source,
                        job_board,
                        executor,
                        time_taken,
                        scraper_count,
                        uuid
                    )
                    VALUES (?,?,?,?,?,?,?)
                    """,
                    [
                        (
                            datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
                            getattr(record, "source", None),
                            getattr(record, "jobBoard", None),
                            getattr(record, "executor", None),
                            getattr(record, "timer", None),
                            getattr(record, "scraper_count", None),
                            getattr(record, "uuid", None)
                        )
                        for record in events
                    ]
                )

        except Exception:
            self.handleError(events[-1])

class HistorySQLHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.events = {}

    def emit(self, record):

        uuid = getattr(record, "uuid", None)

        if not uuid:
            return

        if uuid not in self.events:
            self.events[uuid] = []

        if record.levelno in {
            NEW_LEVEL,
            UPDATED_LEVEL,
            FILLED_LEVEL
        }:
            self.events[uuid].append(record)

        elif record.levelno == FINISHED_LEVEL:
            self.flush_events(uuid)

    def flush_events(self, uuid):

        events = self.events.pop(uuid, None)

        if not events:
            return

        try:
            with get_logs_connection() as conn:

                conn.executemany(
                    """
                    INSERT INTO history (
                        hash_id,
                        job_name,
                        source,
                        event,
                        field,
                        old_val,
                        new_val,
                        timestamp,
                        uuid
                    )
                    VALUES (?,?,?,?,?,?,?,?,?)
                    """,
                    [
                        (
                            getattr(record, "hash_id", None),
                            getattr(record, "job_name", None),
                            getattr(record, "source", None),
                            getattr(record, "levelname", None),
                            getattr(record, "field", None),
                            getattr(record, "old_val", None),
                            getattr(record, "new_val", None),
                            datetime.fromtimestamp(
                                record.created,tz=timezone.utc
                            ).isoformat(),
                            getattr(record, "uuid", None)
                        )
                        for record in events
                    ]
                )

        except Exception:
            self.handleError(events[-1])

class QSQLHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.events = {}

    def emit(self, record):

        uuid = getattr(record, "uuid", None)

        if not uuid:
            return

        if uuid not in self.events:
            self.events[uuid] = []

        if record.levelno in {
            NEW_LEVEL,
            UPDATED_LEVEL
        }:
            self.events[uuid].append(record)

        elif record.levelno == FINISHED_LEVEL:
            self.flush_events(uuid)

    def flush_events(self, uuid):

        events = self.events.pop(uuid, None)

        if not events:
            return

        try:
            with get_q_connection() as conn:

                conn.executemany(
                    """
                    INSERT INTO q (
                        hash_id,
                        info,
                        event,
                        task,
                        created_at,
                        uuid
                    )
                    VALUES (?,?,?,?,?,?)
                    """,
                    [
                        (
                            getattr(record, "hash_id", None),
                            getattr(record, "info", None),
                            getattr(record, "levelname", None),
                            (
                                "extract_jd"
                                if record.levelno == NEW_LEVEL
                                else "update_jd"
                            ),
                            datetime.fromtimestamp(
                                record.created, tz=timezone.utc
                            ).isoformat(),
                            getattr(record, "uuid", None)
                        )
                        for record in events
                    ]
                )

        except Exception:
            self.handleError(events[-1])

class SummarySQLHandler(logging.Handler):

    def emit(self, record):
        try:
            summary = getattr(record, "summary", None)

            if not summary:
                return

            with get_summary_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO run_summary (
                        uuid,
                        executor,
                        new,
                        filled,
                        updated,
                        started_at,
                        finished_at,
                        runtime
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.uuid,
                        record.executor,
                        summary["new"],
                        summary["filled"],
                        summary["updated"],
                        record.started_at,
                        record.finished_at,
                        record.runtime
                    )
                )

        except Exception:
            self.handleError(record)

class EventOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {NEW_LEVEL, FILLED_LEVEL}

class TimerOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {TIMER_LEVEL, FINISHED_LEVEL}

class NoTimerFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != TIMER_LEVEL

class LogsFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {NEW_LEVEL, UPDATED_LEVEL, FILLED_LEVEL, FINISHED_LEVEL}

class QFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {NEW_LEVEL, UPDATED_LEVEL, FINISHED_LEVEL}

class EmailFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in {NEW_LEVEL, FILLED_LEVEL, FINISHED_LEVEL}

class SummaryFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == FINISHED_LEVEL