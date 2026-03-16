from __future__ import annotations

from datetime import date, datetime, time, timedelta

DAY_INDEX = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def normalize_day(day_of_week: str) -> str:
    return day_of_week.strip().lower()


def next_occurrence(target_day: str, start_time: time) -> datetime:
    now = datetime.now()
    target_index = DAY_INDEX.get(normalize_day(target_day))
    if target_index is None:
        return datetime.combine(date.today(), start_time)

    days_ahead = (target_index - now.weekday()) % 7
    candidate_date = date.today() + timedelta(days=days_ahead)
    candidate = datetime.combine(candidate_date, start_time)

    if candidate <= now:
        candidate = candidate + timedelta(days=7)

    return candidate


def build_class_reminders(course_name: str, day_of_week: str, start_time: time) -> list[dict]:
    next_class = next_occurrence(day_of_week, start_time)
    reminders = []
    for minutes_before in (30, 10):
        reminder_time = next_class - timedelta(minutes=minutes_before)
        if reminder_time > datetime.now():
            reminders.append(
                {
                    "reminder_time": reminder_time,
                    "message": f"Upcoming class: {course_name} in {minutes_before} minutes.",
                }
            )
    return reminders


def build_assignment_reminders(course_name: str, title: str, due_date: date) -> list[dict]:
    base_time = time(hour=9, minute=0)
    due_datetime = datetime.combine(due_date, base_time)
    offsets = [timedelta(days=3), timedelta(days=1), timedelta(days=0)]

    reminders = []
    for offset in offsets:
        reminder_time = due_datetime - offset
        if reminder_time > datetime.now():
            if offset.days == 0:
                label = "today"
            else:
                label = f"in {offset.days} day{'s' if offset.days != 1 else ''}"
            reminders.append(
                {
                    "reminder_time": reminder_time,
                    "message": f"Assignment '{title}' for {course_name} is due {label}.",
                }
            )

    return reminders
