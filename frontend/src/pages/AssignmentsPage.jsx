import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

export default function AssignmentsPage() {
  const [assignments, setAssignments] = useState([]);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({
    course_name: "",
    title: "",
    description: "",
    due_date: "",
    attachment_url: "",
  });

  const loadAssignments = async () => {
    try {
      const data = await apiRequest("/api/assignments");
      setAssignments(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    loadAssignments();
  }, []);

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    try {
      await apiRequest("/api/assignments", { method: "POST", body: form });
      setForm({
        course_name: "",
        title: "",
        description: "",
        due_date: "",
        attachment_url: "",
      });
      loadAssignments();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      await apiRequest(`/api/assignments/${id}`, { method: "DELETE" });
      setAssignments((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h2>Assignments</h2>
        <p>Track your deadlines and coursework.</p>
      </header>

      <div className="split">
        <section className="card">
          <h3>Add assignment</h3>
          <form className="form" onSubmit={handleSubmit}>
            <label>
              Course name
              <input name="course_name" value={form.course_name} onChange={handleChange} required />
            </label>
            <label>
              Title
              <input name="title" value={form.title} onChange={handleChange} required />
            </label>
            <label>
              Description
              <textarea name="description" value={form.description} onChange={handleChange} rows={3} />
            </label>
            <label>
              Due date
              <input type="date" name="due_date" value={form.due_date} onChange={handleChange} required />
            </label>
            <label>
              Attachment URL (optional)
              <input name="attachment_url" value={form.attachment_url} onChange={handleChange} />
            </label>
            {error && <div className="error">{error}</div>}
            <button className="btn primary" type="submit">
              Add assignment
            </button>
          </form>
        </section>

        <section className="card">
          <h3>Your assignments</h3>
          {assignments.length ? (
            <ul>
              {assignments.map((assignment) => (
                <li key={assignment.id} className="list-item">
                  <div>
                    <strong>{assignment.title}</strong>
                    <div>{assignment.course_name}</div>
                    <div className="muted">Due {assignment.due_date}</div>
                  </div>
                  <button className="btn ghost" onClick={() => handleDelete(assignment.id)}>
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p>No assignments yet.</p>
          )}
        </section>
      </div>
    </div>
  );
}
