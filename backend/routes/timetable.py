from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from database import get_supabase
from models.schemas import TimetableCreate
from services.auth import get_current_user
from services.reminders import build_class_reminders

router = APIRouter(prefix="/api/timetable", tags=["timetable"])


@router.post("")
def create_timetable(payload: TimetableCreate, user=Depends(get_current_user)):
    supabase = get_supabase()
    data = payload.model_dump()
    data["user_id"] = user["user_id"]

    result = supabase.table("timetable").insert(data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create timetable entry")

    entry = result.data[0]
    reminders = build_class_reminders(
        course_name=entry["course_name"],
        day_of_week=entry["day_of_week"],
        start_time=payload.start_time,
    )

    for reminder in reminders:
        supabase.table("reminders").insert(
            {
                "user_id": user["user_id"],
                "type": "class",
                "reference_id": entry["id"],
                "reminder_time": reminder["reminder_time"].isoformat(),
                "message": reminder["message"],
                "sent": False,
            }
        ).execute()

    return entry


@router.get("")
def list_timetable(user=Depends(get_current_user)):
    supabase = get_supabase()
    result = (
        supabase.table("timetable")
        .select("*")
        .eq("user_id", user["user_id"])
        .order("day_of_week")
        .execute()
    )
    return result.data or []


@router.delete("/{entry_id}")
def delete_timetable(entry_id: str, user=Depends(get_current_user)):
    supabase = get_supabase()
    delete_response = (
        supabase.table("timetable")
        .delete()
        .eq("id", entry_id)
        .eq("user_id", user["user_id"])
        .execute()
    )

    if not delete_response.data:
        raise HTTPException(status_code=404, detail="Timetable entry not found")

    supabase.table("reminders").delete().eq("reference_id", entry_id).eq("type", "class").execute()

    return {"status": "deleted"}
