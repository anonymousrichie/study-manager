import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { supabase } from "../services/supabase";

export default function Layout() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await supabase.auth.signOut();
    navigate("/login");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-title">Student Manager</div>
          <div className="brand-subtitle">Academic MVP</div>
        </div>
        <nav className="nav">
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/timetable">Timetable</NavLink>
          <NavLink to="/assignments">Assignments</NavLink>
        </nav>
        <button className="btn ghost" onClick={handleLogout}>
          Log out
        </button>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
