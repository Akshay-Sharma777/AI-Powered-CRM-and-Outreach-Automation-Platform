"""
Exponential Backoff with Jitter Retry Helper.
Used for network requests, external provider APIs, and database reconnection.
NEVER USED FOR BLIND EMAIL SEND RETRIES.
"""

import asyncio
import logging
import random
import time
from typing import Callable, Tuple, Type, TypeVar, Any

logger = logging.getLogger(__name__)
T = TypeVar("T")


def retry_with_backoff(
    func: Callable[..., T],
    args: Tuple = (),
    kwargs: dict = None,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> T:
    """
    Synchronous retry function with full jitter exponential backoff.
    Delay = min(max_delay, base_delay * (2 ** (attempt - 1)) + uniform(0, 1))
    """
    if kwargs is None:
        kwargs = {}

    attempt = 1
    while True:
        try:
            return func(*args, **kwargs)
        except retryable_exceptions as exc:
            if attempt >= max_attempts:
                logger.error("Exceeded max retry attempts (%d) for %s. Error: %s", max_attempts, func.__name__, exc)
                raise exc

            # Calculate jittered exponential backoff
            delay = min(max_delay, (base_delay * (2 ** (attempt - 1))) + random.uniform(0.1, 1.0))
            logger.warning(
                "Attempt %d/%d failed for %s (%s). Retrying in %.2fs...",
                attempt, max_attempts, func.__name__, exc, delay
            )
            time.sleep(delay)
            attempt += 1


async def async_retry_with_backoff(
    coro_func: Callable[..., Any],
    args: Tuple = (),
    kwargs: dict = None,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Any:
    """Async variant with bounded exponential backoff with jitter."""
    if kwargs is None:
        kwargs = {}

    attempt = 1
    while True:
        try:
            return await coro_func(*args, **kwargs)
        except retryable_exceptions as exc:
            if attempt >= max_attempts:
                logger.error("Exceeded max async retry attempts (%d) for %s: %s", max_attempts, coro_func.__name__, exc)
                raise exc

            delay = min(max_delay, (base_delay * (2 ** (attempt - 1))) + random.uniform(0.1, 1.0))
            logger.warning(
                "Async attempt %d/%d failed for %s (%s). Retrying in %.2fs...",
                attempt, max_attempts, coro_func.__name__, exc, delay
            )
            await asyncio.sleep(delay)
            attempt += 1
