from pydantic import BaseModel, root_validator


class _ValidatedDateComponents(BaseModel):
    # year: int
    # month: int = 1
    # day: int = 1

    @root_validator()
    def check_valid_date(cls, values):
        # year = values.get("year")
        # month = values.get("month")
        # day = values.get("day")
        #
        # specified_date = datetime.datetime(year=year, month=month, day=day)
        # now = datetime.datetime.utcnow()
        # if specified_date > now:
        #     raise ValueError("Document publish date should not be in the future")

        # TODO check event "publish", once available

        return values
