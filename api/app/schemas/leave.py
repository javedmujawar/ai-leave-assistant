from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class LeaveApplication(BaseModel):
    leave_type: Literal["casual", "sick", "earned"]
    from_date: date
    to_date: date
    reason: str = Field(min_length=3, max_length=500)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.to_date < self.from_date:
            raise ValueError("to_date cannot be before from_date")

        return self


class LeaveCancellation(BaseModel):
    leave_id: int
