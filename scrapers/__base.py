from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass, asdict
from typing import Optional

class ApiJobBoardScraper(ABC):
    name="base"
    url=""
    jd_url=""
    base_domain=''
    registry={}

    def __init__(self):
        self.session=requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        })

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Don't register abstract base classes
        if cls.name and cls.name != "base":
            ApiJobBoardScraper.registry[cls.name] = cls

    @abstractmethod
    def scrape_jobs(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def scrape_jd(self, source: dict=None):
        raise NotImplementedError

    def clean_html(self, raw_html: str) -> str:
        soup = BeautifulSoup(raw_html, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        lines = [line.strip() for line in text.splitlines()]
        text = "\n".join(line for line in lines if line)

        # Fix colon formatting
        text = re.sub(r"\n\s*:", ":", text)

        # Collapse multiple blank lines
        text = re.sub(r"\n{2,}", "\n\n", text)

        return text.strip()

class BaseModel:
    def to_dict(self):
        return {
            k: v
            for k, v in asdict(self).items()
            if v is not None
        }

@dataclass(kw_only=True)
class Job(BaseModel):
    job_id: str
    internal_job_id: Optional[str] = None
    job_name: str
    source: str
    work_policy: Optional[str] = None
    location: str
    secondary_loc: Optional[str] = None
    creation_date: str = None
    posted_date: str
    updated_date: Optional[str] = None
    filled_date: Optional[str] = None
    url: str
    comp : Optional[str] = None
    hiring_manger: Optional[str] = None


'''
ashbyhq : Aerovect, Cobot
oraclecloud : Ford, linamar, Metrolinx
myworkday : GM, Honda, lumentum, multimatic, Caterpillar, kiongroup
lever : Kepler, Waabi, intersect, zoox, Cyngn
eightfold ai: Trimble, Boston Scientific, Eaton
bamboohr: ZTR
rivianvw :Rivian
greenhouse: Kodiak, Applied Intuition, Lucid Motors, Gatik, Nuro
ADP: NextStar, GAstops, Kongsberg Geospatial
smartrecruiter: GeneralDynamics,
rmk successfactors? : alstom, apotex, bwxt, celestica, epiroc, komatsu
ats rippling - kraken robotics, blue water autonomy
'''