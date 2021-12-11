from app.patches import sqlalchemy, sqlmodel


def patch() -> None:
    sqlmodel.patch()
    sqlalchemy.patch()
