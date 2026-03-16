from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from database import get_supabase
from models.schemas import AssignmentCreate
from services.auth import get_current_user
from services.reminders import build_assignment_reminders

router = APIRouter(prefix="/api/assignments", tags=["assignments"])


@router.post("")
def create_assignment(payload: AssignmentCreate, user=Depends(get_current_user)):
    supabase = get_supabase()
    data = payload.model_dump()
    data["user_id"] = user["user_id"]

    result = supabase.table("assignments").insert(data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create assignment")

    entry = result.data[0]
    reminders = build_assignment_reminders(
        course_name=entry["course_name"],
        title=entry["title"],
        due_date=payload.due_date,
    )

    for reminder in reminders:
        supabase.table("reminders").insert(
            {
                "user_id": user["user_id"],
                "type": "assignment",
                "reference_id": entry["id"],
                "reminder_time": reminder["reminder_time"].isoformat(),
                "message": reminder["message"],
                "sent": False,
            }
        ).execute()

    return entry


@router.get("")
def list_assignments(user=Depends(get_current_user)):
    supabase = get_supabase()
    result = (
        supabase.table("assignments")
        .select("*")
        .eq("user_id", user["user_id"])
        .order("due_date")
        .execute()
    )
    return result.data or []


@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: str, user=Depends(get_current_user)):
    supabase = get_supabase()
    delete_response = (
        supabase.table("assignments")
        .delete()
        .eq("id", assignment_id)
        .eq("user_id", user["user_id"])
        .execute()
    )

    if not delete_response.data:
        raise HTTPException(status_code=404, detail="Assignment not found")

    supabase.table("reminders").delete().eq("reference_id", assignment_id).eq("type", "assignment").execute()

    return {"status": "deleted"}
