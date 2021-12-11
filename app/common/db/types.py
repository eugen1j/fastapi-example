import sqlalchemy as sa


class DateTime(sa.DateTime):
    def __init__(self, timezone: bool = True) -> None:
        super().__init__(timezone)
