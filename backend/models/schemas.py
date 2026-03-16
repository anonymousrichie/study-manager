from __future__ import annotations

from datetime import date, time
from pydantic import BaseModel, Field


class TimetableCreate(BaseModel):
    course_name: str = Field(min_length=1)
    day_of_week: str = Field(min_length=1)
    start_time: time
    end_time: time
    lecturer: str | None = None
    location: str | None = None


class AssignmentCreate(BaseModel):
    course_name: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str | None = None
    due_date: date
    attachment_url: str | None = None
