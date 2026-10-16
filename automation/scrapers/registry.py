"""
Approved Scraper Registry.
Maps validated source keys to their respective Scraper implementation classes.
Unlisted or disabled sources cannot be executed.
"""

from typing import Dict, Type, Any
from automation.scrapers.base import BaseScraper


SCRAPER_REGISTRY: Dict[str, Dict[str, Any]] = {
    "internshala": {
        "name": "Internshala",
        "base_url": "https://internshala.com",
        "category": "internship"
    },
    "naukri": {
        "name": "Naukri Freshers",
        "base_url": "https://www.naukri.com/fresher-jobs",
        "category": "job"
    },
    "apna": {
        "name": "Apna Jobs",
        "base_url": "https://apna.co",
        "category": "job"
    },
    "workindia": {
        "name": "WorkIndia",
        "base_url": "https://www.workindia.in",
        "category": "job"
    },
    "shine": {
        "name": "Shine Freshers",
        "base_url": "https://www.shine.com",
        "category": "job"
    },
    "hackathons": {
        "name": "Devpost & Unstop",
        "base_url": "https://unstop.com",
        "category": "hackathon"
    },
    "college_tpo": {
        "name": "College TPO Directories",
        "base_url": "https://colleges.example.edu",
        "category": "college_tpo"
    },
    "startups": {
        "name": "YC Workatastartup",
        "base_url": "https://workatastartup.com",
        "category": "startup"
    }
}


def is_source_approved(source_id: str) -> bool:
    """Verifies whether a source key is in the approved registry."""
    return source_id.lower() in SCRAPER_REGISTRY
