from __future__ import annotations

from datetime import date


def build_study_suggestion(assignments: list[dict]) -> str | None:
    today = date.today()
    for assignment in assignments:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
        if isinstance(due_date, str):
            try:
                due_date = date.fromisoformat(due_date)
            except ValueError:
                continue
        if (due_date - today).days <= 2:
            course_name = assignment.get("course_name", "this course")
            return f"Consider studying for {course_name} today."
    return None
