from contextlib import contextmanager
from typing import Any, Iterator, Sequence

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


class PostgresUtility:
    """Manage pooled PostgreSQL connections and common query operations."""

    def __init__(
        self,
        dsn: str,
        *,
        min_size: int = 1,
        max_size: int = 10,
    ) -> None:
        if not dsn:
            raise ValueError("A PostgreSQL DSN is required")
        if min_size < 1 or max_size < min_size:
            raise ValueError("Pool sizes must satisfy 1 <= min_size <= max_size")

        self._pool = ConnectionPool(
            conninfo=dsn,
            min_size=min_size,
            max_size=max_size,
            kwargs={"row_factory": dict_row},
            open=False,
        )
        self._pool.open(wait=True)

    @contextmanager
    def connection(self) -> Iterator[Connection[Any]]:
        """Yield a connection and commit or roll back its transaction."""
        with self._pool.connection() as connection:
            yield connection

    def execute(
        self,
        query: str,
        params: Sequence[Any] | None = None,
    ) -> int:
        """Execute a write query and return the affected row count."""
        with self.connection() as connection:
            cursor = connection.execute(query, params)
            return cursor.rowcount

    def fetch_one(
        self,
        query: str,
        params: Sequence[Any] | None = None,
    ) -> dict[str, Any] | None:
        """Execute a query and return its first row as a dictionary."""
        with self.connection() as connection:
            return connection.execute(query, params).fetchone()

    def fetch_all(
        self,
        query: str,
        params: Sequence[Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute a query and return all rows as dictionaries."""
        with self.connection() as connection:
            return list(connection.execute(query, params).fetchall())

    def close(self) -> None:
        """Close all connections managed by the pool."""
        self._pool.close()

    def __enter__(self) -> "PostgresUtility":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()
