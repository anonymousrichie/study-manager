create table if not exists timetable (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  course_name text not null,
  day_of_week text not null,
  start_time time not null,
  end_time time not null,
  lecturer text,
  location text,
  created_at timestamptz not null default now()
);

create table if not exists assignments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  course_name text not null,
  title text not null,
  description text,
  due_date date not null,
  attachment_url text,
  created_at timestamptz not null default now()
);

create table if not exists reminders (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  type text not null,
  reference_id uuid not null,
  reminder_time timestamptz not null,
  message text not null,
  sent boolean not null default false,
  created_at timestamptz not null default now()
);

create index if not exists reminders_due_idx on reminders (reminder_time) where sent = false;
create index if not exists timetable_user_idx on timetable (user_id);
create index if not exists assignments_user_idx on assignments (user_id);
create index if not exists reminders_user_idx on reminders (user_id);
