"""
Base Scraper Class.
Provides resilient extraction framework, error capture, and human-like request pacing.
"""

import abc
import logging
import random
import time
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class BaseScraper(abc.ABC):
    def __init__(self, source_id: str, base_url: str):
        self.source_id = source_id
        self.base_url = base_url

    def human_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Injects human-like random pause between page transitions."""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    @abc.abstractmethod
    def fetch(self, url: str) -> str:
        """Retrieves raw HTML or JSON from approved target source."""
        pass

    @abc.abstractmethod
    def parse(self, content: str) -> List[Dict[str, Any]]:
        """Parses raw content into standardized lead extraction dictionaries."""
        pass

    def run(self) -> List[Dict[str, Any]]:
        """Executes scrape workflow with exception handling."""
        logger.info("Executing scraper for source: %s (%s)", self.source_id, self.base_url)
        try:
            content = self.fetch(self.base_url)
            results = self.parse(content)
            logger.info("Scraper [%s] extracted %d records.", self.source_id, len(results))
            return results
        except Exception as exc:
            logger.error("Scraper [%s] encountered error: %s", self.source_id, exc)
            raise exc
