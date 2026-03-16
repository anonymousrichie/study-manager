from __future__ import annotations

from datetime import datetime

from database import get_supabase
from services.notifications import send_notification


def process_due_reminders() -> None:
    supabase = get_supabase()
    now = datetime.now().isoformat()

    response = (
        supabase.table("reminders")
        .select("id,user_id,message,reminder_time")
        .lte("reminder_time", now)
        .eq("sent", False)
        .execute()
    )

    reminders = response.data or []
    if not reminders:
        return

    for reminder in reminders:
        send_notification(None, "Reminder", reminder.get("message", ""))
        (
            supabase.table("reminders")
            .update({"sent": True})
            .eq("id", reminder["id"])
            .execute()
        )
