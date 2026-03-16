from __future__ import annotations

import os
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.assignments import router as assignments_router
from routes.dashboard import router as dashboard_router
from routes.timetable import router as timetable_router
from scheduler.worker import process_due_reminders

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

app = FastAPI(title="Student Academic Manager API")

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(timetable_router)
app.include_router(assignments_router)
app.include_router(dashboard_router)

scheduler = BackgroundScheduler()


@app.on_event("startup")
def start_scheduler() -> None:
    scheduler.add_job(process_due_reminders, "interval", seconds=60, id="reminder_job", replace_existing=True)
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown()


@app.get("/")
def health() -> dict:
    return {"status": "ok"}
