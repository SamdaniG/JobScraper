# utils.py
import hashlib
from datetime import timedelta, date
from dataclasses import dataclass, field
from uuid import uuid4

DATE_FMT = "%a %d-%b-%Y"

@dataclass
class RunContext:
    run_uuid: str = field(default_factory=lambda: str(uuid4()))

def sha256_hex(s: str, length: int = 10) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:length]

def get_text_or_none(parent, by, value, default="meh"):
    elems = parent.find_elements(by, value)
    return elems[0].text.strip() if elems else default

def get_exact_posting_date(parent, by, value, default_date="Thu 01-Jan-2026"):
    elems = parent.find_elements(by, value)
    if not elems:
        return default_date

    text = elems[0].text.strip().lower()
    today = date.today()

    # Explicit 30+ days case
    if "30+" in text:
        return default_date

    if "yesterday" in text:
        return (today - timedelta(days=1)).strftime(DATE_FMT)

    if "today" in text:
        return today.strftime(DATE_FMT)

    # Handle "X days ago"
    for part in text.split():
        if part.isdigit():
            return (today - timedelta(days=int(part))).strftime(DATE_FMT)

    return default_date

def api_get_exact_posting_date(text, default_date="Thu 01-Jan-2026"):
    today = date.today()

    # Explicit 30+ days case
    if text is None:
        return None
    text = text.lower()
    if "30+" in text:
        return default_date

    if "yesterday" in text:
        return (today - timedelta(days=1)).strftime(DATE_FMT)

    if "today" in text:
        return today.strftime(DATE_FMT)

    # Handle "X days ago"
    for part in text.split():
        if part.isdigit():
            return (today - timedelta(days=int(part))).strftime(DATE_FMT)

    return default_date
