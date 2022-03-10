import datetime
import typing as t

from pydantic import BaseModel, root_validator, validator


class _ValidatedDateComponents(BaseModel):
    year: int
    month: t.Optional[int] = None
    day: t.Optional[int] = None

    @validator("month", "day", pre=True, always=True)
    def set_date(cls, val):  # noqa: D102
        return val or 1

    @root_validator()
    def check_valid_date(cls, values):
        year = values.get("year")
        month = values.get("month")
        day = values.get("day")

        specified_date = datetime.datetime(year=year, month=month, day=day)
        now = datetime.datetime.utcnow()
        if specified_date > now:
            raise ValueError("Action creation date should not be in the future")

        return values
