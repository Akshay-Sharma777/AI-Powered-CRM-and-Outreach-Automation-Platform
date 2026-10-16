"""
Database Connection and Pooling Module.
Direct SQL execution using psycopg3 and psycopg_pool.
STRICTLY NO ORM.
"""

import time
import logging
from contextlib import contextmanager
from typing import Generator, Optional
import psycopg
from psycopg_pool import ConnectionPool

from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)

_pool: Optional[ConnectionPool] = None


def init_db_pool() -> ConnectionPool:
    """Initializes the global psycopg connection pool."""
    global _pool
    if _pool is not None:
        return _pool

    settings = get_settings()
    logger.info("Initializing PostgreSQL direct connection pool...")

    # Retry once on connection startup to handle Neon idle sleep
    attempts = 2
    for attempt in range(1, attempts + 1):
        try:
            _pool = ConnectionPool(
                conninfo=settings.DATABASE_URL,
                min_size=settings.DB_MIN_CONNECTIONS,
                max_size=settings.DB_MAX_CONNECTIONS,
                timeout=settings.DB_TIMEOUT_SECONDS,
                open=True
            )
            # Verify connectivity
            with _pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
            logger.info("Database connection pool initialized successfully.")
            return _pool
        except Exception as exc:
            if attempt < attempts:
                logger.warning("Neon wake-up delay on first connection attempt (%s). Retrying in 2s...", exc)
                time.sleep(2)
            else:
                logger.error("Failed to initialize database connection pool: %s", exc)
                raise exc


def close_db_pool() -> None:
    """Closes all connections in the pool on shutdown."""
    global _pool
    if _pool is not None:
        logger.info("Closing database connection pool...")
        _pool.close()
        _pool = None


def get_pool() -> ConnectionPool:
    """Returns the initialized connection pool or initializes on first call."""
    global _pool
    if _pool is None:
        _pool = init_db_pool()
    return _pool


@contextmanager
def get_conn() -> Generator[psycopg.Connection, None, None]:
    """Context manager for acquiring a single connection from the pool."""
    pool = get_pool()
    with pool.connection() as conn:
        yield conn


@contextmanager
def transaction() -> Generator[psycopg.Connection, None, None]:
    """
    Context manager for atomic database transactions.
    Commits on successful block execution, automatically rolls back on exceptions.
    """
    pool = get_pool()
    with pool.connection() as conn:
        with conn.transaction():
            yield conn
