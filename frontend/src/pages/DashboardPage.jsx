import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const response = await apiRequest("/api/dashboard");
        setData(response);
      } catch (err) {
        setError(err.message);
      }
    };

    loadDashboard();
  }, []);

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!data) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="page">
      <header className="page-header">
        <h2>Dashboard</h2>
        <p>Your upcoming academic highlights.</p>
      </header>

      <div className="grid">
        <section className="card">
          <h3>Today's classes</h3>
          {data.todays_classes?.length ? (
            <ul>
              {data.todays_classes.map((item) => (
                <li key={item.id}>
                  <strong>{item.course_name}</strong> · {item.start_time} - {item.end_time}
                </li>
              ))}
            </ul>
          ) : (
            <p>No classes scheduled today.</p>
          )}
        </section>

        <section className="card">
          <h3>Next class</h3>
          {data.next_class ? (
            <div>
              <strong>{data.next_class.course_name}</strong>
              <div>
                {data.next_class.day_of_week} · {data.next_class.start_time}
              </div>
            </div>
          ) : (
            <p>No upcoming class today.</p>
          )}
        </section>

        <section className="card">
          <h3>Upcoming assignments</h3>
          {data.upcoming_assignments?.length ? (
            <ul>
              {data.upcoming_assignments.map((assignment) => (
                <li key={assignment.id}>
                  <strong>{assignment.title}</strong> · {assignment.course_name}
                  <div>Due {assignment.due_date}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p>No assignments due soon.</p>
          )}
        </section>

        <section className="card">
          <h3>Upcoming reminders</h3>
          {data.upcoming_reminders?.length ? (
            <ul>
              {data.upcoming_reminders.map((reminder) => (
                <li key={reminder.id}>
                  {reminder.message}
                  <div>{new Date(reminder.reminder_time).toLocaleString()}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p>No reminders yet.</p>
          )}
        </section>

        <section className="card accent">
          <h3>Study suggestion</h3>
          <p>{data.study_suggestion || "You're on track!"}</p>
        </section>
      </div>
    </div>
  );
}
