# Student Academic Manager (MVP)

This project contains a FastAPI backend and a React frontend for managing student timetables, assignments, and reminders.

## Setup Overview

1. Create Supabase tables using `docs/schema.sql`.
2. Configure environment variables in `backend/.env` (see `backend/.env.example`).
3. Install backend dependencies: `pip install -r backend/requirements.txt`.
4. Start backend: `uvicorn backend.main:app --reload`.
5. Configure frontend env in `frontend/.env` (see `frontend/.env.example`).
6. Install frontend deps: `npm install`.
7. Start frontend: `npm run dev`.

## Notes

- Supabase Auth handles signup/login in the frontend.
- Backend expects a Supabase JWT in the `Authorization: Bearer <token>` header.
- The reminder scheduler runs every 60 seconds and logs reminders to the console by default.
