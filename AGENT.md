AGENT.md
Project: Student Academic Manager

This document provides instructions for an AI development agent responsible for building the Student Academic Manager MVP.

The goal is to build a minimal working product that helps students organize their timetable, track assignments, and receive reminders.

Focus only on MVP features. Avoid building advanced features unless specified.

1. Project Goal

Build a web application that allows students to:

Manage their academic timetable

Track assignments

Automatically receive reminders for classes and deadlines

View upcoming academic tasks in a dashboard

The system should be simple, reliable, and easy to extend later.

2. Tech Stack

The agent must use the following technologies.

Frontend

React

JavaScript

HTML

CSS

Backend

Python

FastAPI

Database

Supabase (PostgreSQL)

Authentication

Supabase Auth

Background Jobs

APScheduler for reminder checking

3. Project Architecture

Use a separated frontend and backend architecture.

project-root
¦
+-- backend
¦   +-- main.py
¦   +-- database.py
¦   +-- models
¦   +-- routes
¦   +-- services
¦   +-- scheduler
¦
+-- frontend
¦   +-- src
¦   +-- components
¦   +-- pages
¦   +-- services
¦
+-- docs
4. Database Design (Supabase)

The system stores users, timetable data, assignments, and reminders.

users

Handled by Supabase authentication.

Fields managed by Supabase.

timetable
id
user_id
course_name
day_of_week
start_time
end_time
lecturer
location
created_at

Purpose:
Stores all scheduled classes for a user.

assignments
id
user_id
course_name
title
description
due_date
attachment_url
created_at

Purpose:
Stores assignment details and deadlines.

reminders
id
user_id
type
reference_id
reminder_time
message
sent
created_at

Where:

type = "class" or "assignment"

reference_id links to either:

timetable entry

assignment entry

5. Authentication

Use Supabase Authentication.

Features required:

User signup

User login

Session persistence

Logout

The backend should verify the Supabase JWT token for protected endpoints.

6. Backend API (FastAPI)

Create REST endpoints.

Base path:

/api
Timetable Routes
POST   /api/timetable
GET    /api/timetable
DELETE /api/timetable/{id}

Functions:

Create class schedule

Retrieve all classes

Delete class

When a timetable entry is created:

The system must automatically create reminders:

30 minutes before class

10 minutes before class

Assignment Routes
POST   /api/assignments
GET    /api/assignments
DELETE /api/assignments/{id}

Functions:

Add assignment

Retrieve assignments

Delete assignment

When an assignment is created:

Automatically generate reminders:

3 days before due date

1 day before due date

On the due date

Dashboard Route
GET /api/dashboard

Return:

TODAY's classes

next upcoming class

upcoming assignments

upcoming reminders

7. Reminder System

Use APScheduler to run a background task.

Scheduler interval:

Every 60 seconds

The scheduler should:

Query the reminders table.

SELECT * FROM reminders
WHERE reminder_time <= current_time
AND sent = false

Send notification.

For MVP use:

Email
or

Console logging

Mark reminder as sent.

sent = true
8. Simple Study Suggestion Logic

Add a basic rule-based suggestion system.

Example rule:

If assignment due in 2 days or less:

Return suggestion:

"Consider studying for this course today."

Implement this logic in the dashboard service.

No machine learning is required for MVP.

9. Frontend Pages

The frontend must include the following pages.

Login Page

Features:

Login

Signup

Authentication via Supabase

Dashboard Page

Display:

Today'S classes

Upcoming assignments

Study suggestion

Timetable Page

Features:

Add class

View weekly timetable

Delete class

Assignments Page

Features:

Add assignment

View assignments

Delete assignment

10. UI Requirements

Keep UI simple.

Recommended layout:

Left sidebar navigation

Main content area

Clean card-based dashboard

Use responsive design.

11. Error Handling

The system must handle:

Missing fields

Unauthorized requests

Invalid tokens

Database errors

Return proper HTTP responses.

Examples:

400 Bad Request

401 Unauthorized

404 Not Found

500 Server Error

12. Security

The agent must ensure:

JWT validation for protected routes

User can only access their own data

Input validation for all API requests

13. MVP Completion Criteria

The MVP is complete when a user can:

Sign up and log in

Add classes to timetable

Add assignments

Automatically generate reminders

View upcoming tasks in dashboard

14. Future Improvements (Do Not Implement Yet)

These features may be added later:

OCR timetable scanning

AI timetable parsing

Google Calendar integration

Push notifications

Study analytics

GPA tracking

Group study planning

15. Development Priorities

The agent must implement features in this order:

Supabase setup

Authentication

Database schema

Backend API

Reminder scheduler

Frontend pages

Dashboard logic
