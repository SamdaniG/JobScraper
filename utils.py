# utils.py
import hashlib

def sha256_hex(s: str, length: int = 10) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:length]

def get_text_or_none(parent, by, value, default="meh"):
    elems = parent.find_elements(by, value)
    return elems[0].text.strip() if elems else default
