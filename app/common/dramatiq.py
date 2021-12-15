from contextvars import ContextVar
from typing import Optional, Dict

from dramatiq import Middleware
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

_Session: Optional[sessionmaker] = None
_session: ContextVar[Optional[Session]] = ContextVar("_session", default=None)


class MissingSessionError(Exception):
    """Exception raised for when the user tries to
    access a database session before it is created."""

    def __init__(self):
        msg = """
        No session found! Either you are not currently in a request context,
        or you need to manually create a session context by using a `db` instance as
        a context manager e.g.:

        with db():
            db.session.query(User).all()
        """

        super().__init__(msg)


class SessionNotInitialisedError(Exception):
    """Exception raised when the user creates a new DB session without first initialising it."""

    def __init__(self):
        msg = """
        Session not initialised! Ensure that DBSessionMiddleware has been initialised before
        attempting database access.
        """

        super().__init__(msg)


class DBSessionMeta(type):
    # using this metaclass means that we can access db.session as a property at a class level,
    # rather than db().session
    @property
    def session(self) -> Session:
        """Return an instance of Session local to the current async context."""
        if _Session is None:
            raise SessionNotInitialisedError

        s = _session.get()
        if s is None:
            raise MissingSessionError

        return s


class DbSessionMiddleware(Middleware, metaclass=DBSessionMeta):
    def __init__(self, engine: Engine, session_args: Dict = None):
        global _Session
        session_args = session_args or {}
        _Session = sessionmaker(bind=engine, **session_args)

    def before_process_message(self, broker, message):
        s = _Session()
        _session.set(s)

    def after_process_message(self, broker, message, *, result=None, exception=None):
        DbSessionMiddleware.session.close()
        _session.set(None)


db: DBSessionMeta = DbSessionMiddleware
