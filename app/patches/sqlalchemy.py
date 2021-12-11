from sqlalchemy.orm import Session


def add_decorator(method):  # type: ignore
    """
    Flush session to Database for Create/Update queries
    Useful for instant retrieving Autoincrement IDs

    So instead
    session.add(obj)
    session.flush()

    We can write just
    session.add(obj)

    But this solution requires more DB calls.
    To optimize code with large amount of session.add calls use

    with session.no_autoflush:
        ...
    """

    def wrapper(self, instance, _warn=True):  # type: ignore
        method(self, instance, _warn)
        if self.autoflush:
            self.flush()

    return wrapper


def patch() -> None:
    Session.add = add_decorator(Session.add)  # type: ignore
