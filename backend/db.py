import sqlite3
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "campus_customs.db"

_shared_connection: ContextVar[sqlite3.Connection | None] = ContextVar(
    "_shared_connection", default=None
)


def get_connection() -> sqlite3.Connection:
    """The active request-scoped connection (see `request_scope`), or a fresh one."""
    shared = _shared_connection.get()
    if shared is not None:
        return shared

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def release_connection(conn: sqlite3.Connection) -> None:
    """Close `conn`, unless it's the shared connection a `request_scope` owns."""
    if conn is not _shared_connection.get():
        conn.close()


@contextmanager
def request_scope():
    """Open one connection for the duration of a single chat turn.

    Without this, every tool call, user lookup, history load, and save in
    a single agent run opens its own short-lived connection — 5+ per
    message. Everything inside this block (including nested tool calls)
    gets the same connection from `get_connection()` instead.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    token = _shared_connection.set(conn)
    try:
        yield conn
    finally:
        _shared_connection.reset(token)
        conn.close()
