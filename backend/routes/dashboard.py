from __future__ import annotations

from datetime import date, datetime, time as time_type

from fastapi import APIRouter, Depends

from database import get_supabase
from services.auth import get_current_user
from services.dashboard import build_study_suggestion

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("")
def get_dashboard(user=Depends(get_current_user)):
    supabase = get_supabase()
    today_name = datetime.now().strftime("%A")
    today_date = date.today()
    now_time = datetime.now().time()

    timetable = (
        supabase.table("timetable")
        .select("*")
        .eq("user_id", user["user_id"])
        .execute()
    ).data or []

    todays_classes = [
        item for item in timetable if str(item.get("day_of_week", "")).lower() == today_name.lower()
    ]

    upcoming_assignments = (
        supabase.table("assignments")
        .select("*")
        .eq("user_id", user["user_id"])
        .gte("due_date", today_date.isoformat())
        .order("due_date")
        .limit(5)
        .execute()
    ).data or []

    upcoming_reminders = (
        supabase.table("reminders")
        .select("*")
        .eq("user_id", user["user_id"])
        .eq("sent", False)
        .order("reminder_time")
        .limit(5)
        .execute()
    ).data or []

    suggestion = build_study_suggestion(upcoming_assignments)

    next_class = None
    if todays_classes:
        def parse_start_time(entry: dict) -> time_type | None:
            raw = entry.get("start_time")
            if not raw:
                return None
            if isinstance(raw, str):
                try:
                    return time_type.fromisoformat(raw)
                except ValueError:
                    return None
            if isinstance(raw, time_type):
                return raw
            return None

        upcoming_today = [
            item for item in todays_classes
            if (parse_start_time(item) or time_type.min) >= now_time
        ]
        candidates = upcoming_today or todays_classes
        next_class = sorted(candidates, key=lambda x: x.get("start_time") or "")[0]

    return {
        "todays_classes": todays_classes,
        "next_class": next_class,
        "upcoming_assignments": upcoming_assignments,
        "upcoming_reminders": upcoming_reminders,
        "study_suggestion": suggestion,
    }
