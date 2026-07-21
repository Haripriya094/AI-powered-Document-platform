from contextlib import contextmanager
from typing import Any, Optional

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from backend.utills.logger import logger


class PostgresConnect:
    """Manages a pooled connection to PostgreSQL and exposes query helpers."""

    def __init__(
        self,
        host: str,
        port: int,
        dbname: str,
        user: str,
        password: str,
        minconn: int = 1,
        maxconn: int = 10,
    ):
        self._pool = pool.ThreadedConnectionPool(
            minconn,
            maxconn,
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )
        logger.info("PostgresConnect pool initialized (min=%s, max=%s)", minconn, maxconn)

    @contextmanager
    def _get_connection(self):
        connection = self._pool.getconn()
        try:
            yield connection
        finally:
            self._pool.putconn(connection)

    @contextmanager
    def _get_cursor(self, connection, dict_cursor: bool = True):
        cursor_factory = RealDictCursor if dict_cursor else None
        cursor = connection.cursor(cursor_factory=cursor_factory)
        try:
            yield cursor
        finally:
            cursor.close()

    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[dict]:
        try:
            with self._get_connection() as connection:
                with self._get_cursor(connection) as cursor:
                    cursor.execute(query, params or ())
                    return cursor.fetchone()
        except Exception as exc:
            logger.error(f"PostgreSQL fetch_one error: {exc}")
            raise PostgresException(f"fetch_one failed: {exc}")

    def fetch_all(self, query: str, params: Optional[tuple] = None) -> list[dict]:
        try:
            with self._get_connection() as connection:
                with self._get_cursor(connection) as cursor:
                    cursor.execute(query, params or ())
                    return cursor.fetchall()
        except Exception as exc:
            logger.error(f"PostgreSQL fetch_all error: {exc}")
            raise PostgresException(f"fetch_all failed: {exc}")

    def execute(self, query: str, params: Optional[tuple] = None) -> int:
        """For single INSERT/UPDATE/DELETE. Returns affected row count."""
        try:
            with self._get_connection() as connection:
                with self._get_cursor(connection, dict_cursor=False) as cursor:
                    cursor.execute(query, params or ())
                    connection.commit()
                    return cursor.rowcount
        except Exception as exc:
            logger.error(f"PostgreSQL execute error: {exc}")
            try:
                if connection is not None:
                    connection.rollback()
            except Exception:
                pass
            raise PostgresException(f"execute failed: {exc}")

    def execute_many(self, query: str, values: list[tuple]) -> int:
        """Bulk INSERT/UPDATE. Returns affected row count."""
        try:
            with self._get_connection() as connection:
                with self._get_cursor(connection, dict_cursor=False) as cursor:
                    cursor.executemany(query, values)
                    connection.commit()
                    return cursor.rowcount
        except Exception as exc:
            logger.error(f"PostgreSQL execute_many error: {exc}")
            try:
                if connection is not None:
                    connection.rollback()
            except Exception:
                pass
            raise PostgresException(f"execute_many failed: {exc}")

    def health_check(self) -> bool:
        """Return True when the DB connection is alive and responsive."""
        try:
            with self._get_connection() as connection:
                with self._get_cursor(connection, dict_cursor=False) as cursor:
                    cursor.execute("SELECT 1")
                    return cursor.fetchone() is not None
        except Exception as exc:
            logger.error(f"PostgreSQL health_check failed: {exc}")
            return False

    def close(self) -> None:
        """Close all pooled connections."""
        try:
            self._pool.closeall()
            logger.info("PostgresConnect pool closed")
        except Exception as exc:
            logger.error(f"Error closing PostgreSQL pool: {exc}")


class PostgresException(Exception):
    """Raised for PostgreSQL operation failures in PostgresConnect."""
    pass
